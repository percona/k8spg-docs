> For the complete documentation index, see [llms.txt](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/llms.txt).

# Minor version upgrade of Percona Distribution for PostgreSQL

A minor version upgrade is the upgrade within the same major version. For example, from 17.5.2 to 17.6.1.

## Considerations

1. Upgrading a PostgreSQL cluster may result in downtime, as well as in [failover](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/change-primary.html) caused by updating the primary instance.
1. Starting with the Operator 2.6.0, Percona Distribution for PostgreSQL images are based on Red Hat Universal Base Image (UBI) 9. Each UBI major version ships a different version of `glibc` and ICU collation libraries. Collation defines how text is sorted and compared based on language-specific rules such as case sensitivity, character order and the like. PostgreSQL stores the collation version used at database creation. When the collation version changes, PostgreSQL reports a collation version mismatch and this may result in corruption of database objects that use it like text-based indexes. Therefore, you need to identify and reindex objects affected by the collation mismatch.
1. [Logical replicas](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/logical-replication.html) can keep replicating after a minor upgrade if you [configured replication slots](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/ha-deploy.html#persist-replication-slots-across-failover). Without slots, a failover during the upgrade can break replication. [Reseed](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/logical-replication.html#reseed-a-logical-replica) the replica if the status becomes `broken`.

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

If `glibc` or ICU differs, run the collation checks **after** PostgreSQL starts on the target image. See [After the Pods restart](#after-the-pods-restart)

### Update PMM

1. [Update PMM Server](https://docs.percona.com/percona-monitoring-and-management/3/pmm-upgrade/index.html) **before** upgrading PMM Client.
1. PMM2 has reached its end-of-life stage and is no longer supported in the Operator. See [PMM upgrade documentation](https://docs.percona.com/percona-monitoring-and-management/3/pmm-upgrade/migrating_from_pmm_2.html) for how to migrate from version 2 to version 3.

## Upgrade steps

To make a minor upgrade of Percona Distribution for PostgreSQL, do the following:

1. Check the version of the Operator you have in your Kubernetes environment. If you need to update it, refer to the [Operator upgrade guide](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/update-operator.html)

1. Check the current version of the Custom Resource and what versions of the database and cluster components are compatible with it. Replace the Operator version with your value in the following command:

   ```
   curl https://check.percona.com/versions/v1/pg-operator/3.1.0 |jq -r '.versions[].matrix'
   ```

   You can also find this information in the [Versions compatibility matrix](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/versions.html).

1. Update the database, the backup and PMM Client image names with a newer version tag. Find the image names [in the list of certified images](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/images.html).

   We recommend to update the PMM Server **before** the upgrade of PMM Client. If you haven’t done it yet, exclude PMM Client from the list of images to update.

   Since this is a working cluster, the way to update the Custom Resource is to [apply a patch](https://kubernetes.io/docs/tasks/run-application/update-api-object-kubectl-patch/) with the `kubectl patch pg` command.

   This example command updates the cluster with the name `cluster1` in the namespace `postgres-operator` to the `3.1.0` version:

   **With PMM Client**

   ```
   kubectl -n postgres-operator patch pg cluster1 --type=merge --patch '{
      "spec": {
         "crVersion":"3.1.0",
         "image": "docker.io/percona/percona-distribution-postgresql:18.6.1-3",
         "proxy": { "pgBouncer": { "image": "docker.io/percona/percona-pgbouncer:1.25.2-8" } },
         "backups": { "pgbackrest":  { "image": "docker.io/percona/percona-pgbackrest:2.59.1-2" } },
         "pmm": { "image": "docker.io/percona/pmm-client:3.9.1" }
      }}'
   ```

   The following image names in the above example were taken from the [list of certified images](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/images.html):

   - `docker.io/percona/percona-distribution-postgresql:18.6.1-3`,
   - `docker.io/percona/percona-pgbouncer:1.25.2-8`,
   - `docker.io/percona/percona-pgbackrest:2.59.1-2`,
   - `docker.io/percona/pmm-client:3.9.1`.

   **Without PMM Client**

   ```
   kubectl patch pg cluster1 -n postgres-operator --type=merge --patch '{
      "spec": {
         "crVersion":"3.1.0",
         "image": "docker.io/percona/percona-distribution-postgresql:18.6.1-3",
         "proxy": { "pgBouncer": { "image": "docker.io/percona/percona-pgbouncer:1.25.2-8" } },
         "backups": { "pgbackrest":  { "image": "docker.io/percona/percona-pgbackrest:2.59.1-2" } }
      }}'
   ```

   The following image names in the above example were taken from the [list of certified images](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/images.html):

   - `docker.io/percona/percona-distribution-postgresql:18.6.1-3`,
   - `docker.io/percona/percona-pgbouncer:1.25.2-8`,
   - `docker.io/percona/percona-pgbackrest:2.59.1-2`

   **with PostGIS**

   When using the [PostGIS](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/postgis.html) extension, make sure to specify the image that contains it for the `kubectl patch command`. Add PMM client image to the list if you also use it.

   ```
   kubectl patch pg cluster1 -n postgres-operator --type=merge --patch '{
      "spec": {
         "crVersion":"3.1.0",
         "image": "docker.io/percona/percona-distribution-postgresql-with-postgis:18.6.1-3",
         "proxy": { "pgBouncer": { "image": "docker.io/percona/percona-pgbouncer:1.25.2-8" } },
         "backups": { "pgbackrest":  { "image": "docker.io/percona/percona-pgbackrest:2.59.1-2" } }
      }}'
   ```

   The following image names in the above example were taken from the [list of certified images](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/images.html):

   - `docker.io/percona/percona-distribution-postgresql-with-postgis:18.6.1-3`,
   - `docker.io/percona/percona-pgbouncer:1.25.2-8`,
   - `docker.io/percona/percona-pgbackrest:2.59.1-2`

1. After you applied the patch, the deployment rollout will be triggered automatically. The update process is successfully finished when all Pods have been restarted.

   Expected output

   ```
   NAME                                           READY   STATUS      RESTARTS   AGE
   cluster1-backup-4vwt-p5d9j                     0/1     Completed   0          97m
   cluster1-instance1-b5mr-0                      4/4     Running     0          99m
   cluster1-instance1-b8p7-0                      4/4     Running     0          99m
   cluster1-instance1-w7q2-0                      4/4     Running     0          99m
   cluster1-pgbouncer-79bbf55c45-62xlk            2/2     Running     0          99m
   cluster1-pgbouncer-79bbf55c45-9g4cb            2/2     Running     0          99m
   cluster1-pgbouncer-79bbf55c45-9nrmd            2/2     Running     0          99m
   cluster1-repo-host-0                           2/2     Running     0          99m
   percona-postgresql-operator-79cd8586f5-2qzcs   1/1     Running     0          120m
   ```

## After the Pods restart

If the new image uses a different UBI major version (for example, UBI 8 to UBI 9), `glibc` collation rules change.

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
