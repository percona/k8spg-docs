> For the complete documentation index, see [llms.txt](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/llms.txt).

# Major version upgrade

Major version upgrade allows you to jump from one database major version to another (for example, upgrade from PostgreSQL 17.x to PostgreSQL 18.x).

This feature is generally available starting with the Operator version 2.9.0.

## Considerations

1. A major upgrade introduces a downtime because the whole cluster is shut down during the upgrade. This flow is planned to be improved in future releases.
1. During the upgrade, the Operator duplicates the data on each PVC and doesn’t remove the old version data automatically. Make sure your PVC has enough free space to store data.
1. If the new image uses a different UBI major, it ships a different `glibc` collation library. After the upgrade, [identify and rebuild indexes](#check-collation) affected by the collation change.

## Before you start

### Check operating system and collation libraries version

Check the operating system used by the PostgreSQL container:

```
kubectl exec -n <namespace> <postgres-pod> -c database -- \
  cat /etc/os-release
```

Check the `glibc` version:

```
kubectl exec -n <namespace> <postgres-pod> -c database -- \
  getconf GNU_LIBC_VERSION
```

Example:

```
glibc 2.34
```

### Check the locale provider in each database

```
SELECT datname, datlocprovider, datcollversion FROM pg_database;
```

Sample output

```
   datname  | datlocprovider | datcollversion
-----------+----------------+----------------
postgres  | c              | 2.34
template1 | c              | 2.34
template0 | c              |
cluster1  | c              | 2.34
(4 rows)
```

`c` is libc (`glibc`). `i` is ICU. If the provider is `i` and the source and target images ship different ICU libraries, treat that the same as a `glibc` change.

If `glibc` or ICU differs, run the collation checks **after** PostgreSQL starts on the target image. See [Check collation](#check-collation)

### Update PMM

1. [Update PMM Server](https://docs.percona.com/percona-monitoring-and-management/3/pmm-upgrade/index.html) **before** upgrading PMM Client.
1. PMM2 has reached its end-of-life stage and is no longer supported in the Operator. See [PMM upgrade documentation](https://docs.percona.com/percona-monitoring-and-management/3/pmm-upgrade/migrating_from_pmm_2.html) for how to migrate from version 2 to version 3.

## Upgrade steps

To start the upgrade, you need to create a special `PerconaPGUpgrade` resource. This resource refers to the special *Operator upgrade image* and contains the information about the existing and target major versions. Find the example `PerconaPGUpgrade` configuration file in `deploy/upgrade.yaml`:

```
apiVersion: pgv2.percona.com/v2
kind: PerconaPGUpgrade
metadata:
  name: cluster1-17-to-18
spec:
  postgresClusterName: cluster1
  image: docker.io/percona/percona-distribution-postgresql-upgrade:18.6-17.11-16.15-15.19-14.24-3
  fromPostgresVersion: 17
  toPostgresVersion: 18
  toPostgresImage: docker.io/percona/percona-distribution-postgresql:18.6.1-3
  toPgBouncerImage: docker.io/percona/percona-pgbouncer:1.25.2-8
  toPgBackRestImage: docker.io/percona/percona-pgbackrest:2.59.1-2
```

As you can see, the manifest includes image names for the database cluster components (PostgreSQL, pgBouncer, and pgBackRest). You can find them [in the list of certified images](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/images.html) for the current Operator release. For older versions, please refer to the [old releases documentation archive](https://docs.percona.com/legacy-documentation/) .

Apply this manifest to start the upgrade:

```
kubectl apply -f deploy/upgrade.yaml -n <namespace>
```

During the upgrade flow, the Operator:

1. Pauses the cluster, making it unavailable for the duration of the upgrade,
1. Annotates the cluster with a special `pgv2.percona.com/allow-upgrade`: `<PerconaPGUpgrade.Name>` annotation,
1. Creates jobs to migrate the data,
1. Starts up the cluster after the upgrade finishes.

## Post-upgrade steps

1. The `pgaudit` extension is not upgraded automatically. If you use this extension, you must drop and recreate it **in each database** where it is installed. [Connect to PostgreSQL](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/connect.html) with the privileges of the superuser and run the following commands:

   ```
   DROP EXTENSION pgaudit;
   CREATE EXTENSION pgaudit;
   ```

   Repeat for every database where the `pgaudit` extension is installed.

1. A successful major upgrade invalidates existing [logical replicas](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/logical-replication.html). After the cluster is `ready`, [reseed](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/logical-replication.html#reseed-a-logical-replica) each logical replica.

## Check collation

If the new image uses a different UBI major (for example, UBI 8 to UBI 9), `glibc` collation rules change.

Scan for indexes that rely on collations other than `C` or `POSIX` and whose collations were provided by the operating system (`c`) or dynamic libraries (`d`). [Connect to PostgreSQL](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/connect.html) with the privileges of the superuser or the database owner and run the following query:

```
SELECT DISTINCT
    indrelid::regclass::text,
    indexrelid::regclass::text,
    collname,
    pg_get_indexdef(indexrelid)
FROM (
    SELECT
        indexrelid,
        indrelid,
        indcollation[i] coll
    FROM
        pg_index,
        generate_subscripts(indcollation, 1) g(i)
) s
JOIN pg_collation c ON coll = c.oid
WHERE
    collprovider IN ('d', 'c')
    AND collname NOT IN ('C', 'POSIX');
```

If you see affected indexes, find the databases whose collation version changed:

```
SELECT datname, datlocprovider, datcollate, datcollversion
FROM pg_database;
```

Sample output

```
datname   | datlocprovider | datcollate  | datcollversion
----------+----------------+-------------+----------------
postgres  | c              | en_US.utf-8 | 2.28
template1 | c              | en_US.utf-8 | 2.28
template0 | c              | en_US.utf-8 |
cluster1  | c              | en_US.utf-8 | 2.28
```

Rebuild affected indexes first. [REINDEX](https://www.postgresql.org/docs/current/sql-reindex.html) updates the index using the current collation rules:

```
REINDEX INDEX CONCURRENTLY <index_name>;
```

Repeat for every affected index, or rebuild all indexes in a database with `REINDEX DATABASE <database_name>;`.

Then refresh collation metadata. `ALTER DATABASE ... REFRESH COLLATION VERSION` only updates PostgreSQL’s recorded metadata. It does not rebuild indexes created using the previous collation rules:

```
ALTER DATABASE cluster1 REFRESH COLLATION VERSION;
```

This command requires the privileges of a superuser or a database owner. **Repeat for every affected database.**

## Cleanup

1. You can remove old version data at your discretion by [executing into containers](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/debug-shell.html) and running the following commands (example for PostgreSQL 17):

   ```
   rm -rf /pgdata/pg17
   rm -rf /pgdata/pg17_wal
   ```

1. You can also delete the `PerconaPGUpgrade` resource (this will clean up the jobs and Pods created during the upgrade):

   ```
   kubectl delete perconapgupgrade cluster1-17-to-18
   ```

## Troubleshooting upgrade issues

If the upgrade fails for some reason, the cluster will stay in paused mode. Resume the cluster [manually](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/pause.html) to check what went wrong with upgrade (it will start with the old version). You can check the `PerconaPGUpgrade` resource with `kubectl get perconapgupgrade -o yaml` command, and [check the logs](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/debug-logs.html) of the upgraded Pods to debug the issue.

### Failed first restore after the upgrade

After a major upgrade, PostgreSQL starts a new WAL timeline. PostgreSQL treats the upgraded cluster as a new logical generation, so it increments the timeline ID and begins writing WAL from that new point.

In clusters with very low write traffic, the upgraded primary may generate very few WAL segments after the upgrade.

When you make a first restore after the upgrade, the restored replicas need to replay WAL from the primary to catch up. To do that, PostgreSQL uses the `pg_rewind` tool. `pg_rewind` searches a common WAL ancestor — a point in history where both the primary and the replica share the same WAL record. If there are few WAL records, there may not be a common WAL ancestor and the replica may fail to rejoin the primary. When this happens, you see the `could not find common ancestor of the source and target cluster's timelines` error in `pg_rewind`.

To address this issue, you must manually [reinitialize](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/reinit.html) the failed replica. Before doing so, check if this replica has any transactions that are not replicated anywhere else. Then remove its data directory and let the instance perform a full copy from the primary.

Alternatively, you can automate replica reinitialization with Patroni. Update the cluster configuration by setting the `spec.patroni.removeDataDirectoryOnDivergedTimelines` in the Custom Resource before the upgrade. When timeline divergence is detected, the Operator instructs Patroni to automatically remove the replica’s data and resync it from the primary.

Warning

The `removeDataDirectoryOnDivergedTimelines` option can lead to data loss. When the Operator resyncs the replica automatically, some transactions may be lost. The risk is usually small but not zero. Use this option only if you understand and accept this trade-off.
