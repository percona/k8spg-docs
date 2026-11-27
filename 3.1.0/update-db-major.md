> For the complete documentation index, see [llms.txt](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/llms.txt).

# Major version upgrade

Major version upgrade allows you to jump from one database major version to another (for example, upgrade from PostgreSQL 17.x to PostgreSQL 18.x).

This feature is generally available starting with the Operator version 2.9.0.

## Considerations

1. A major upgrade introduces a downtime because the whole cluster is shut down during the upgrade. This flow is planned to be improved in future releases.
1. During the upgrade, the Operator duplicates the data on each PVC and doesn’t remove the old version data automatically. Make sure your PVC has enough free space to store data.
1. If the target image ships a different `glibc` build, the sorting rules of some locales can change. Before the upgrade, [check whether the change affects the locales your databases use](#assess-the-collation-risk). See the [glibc collation limitation](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/limitations.html#glibc-collation-changes-between-images). The upgrade runs `pg_upgrade --link`, which keeps every index as it is. The example `PerconaPGUpgrade` uses UBI 9 images. If your cluster runs on `-ubi8` or `-ubi10` images, use the upgrade and PostgreSQL images with the same suffix. Otherwise, the upgrade also changes the operating system.

## Before you start

### Check operating system and glibc

Check the operating system used by the PostgreSQL container:

```
kubectl exec -n <namespace> <postgres-pod> -c database -- \
  cat /etc/os-release
```

Check the `glibc` package build. The output includes the release number after the version, so it shows a change that the version alone hides:

```
kubectl exec -n <namespace> <postgres-pod> -c database -- \
  rpm -q glibc
```

Sample output

```
glibc-2.34-275.el9_8.x86_64
```

If the cluster with the target image doesn’t exist yet, start a temporary Pod from the image and run the same command:

```
kubectl run glibc-check -n <namespace> --rm -i --restart=Never \
  --image=<postgres-image> --command -- \
  rpm -q glibc
```

Run the commands for the current image and for the target image, then compare the full output. If the output is the same, the collation rules are the same. If any part differs, including the release number, assess whether the change affects the locales your databases use.

Also check that every locale your databases use exists in the target image:

```
kubectl run locale-check -n <namespace> --rm -i --restart=Never \
  --image=<postgres-image> --command -- \
  locale -a
```

A locale that is missing from the list can’t be used on that image.

### Assess the collation risk

A `glibc` change usually updates the sorting rules of only a few locales. Your data is at risk only if your databases use one of those locales. Run this assessment before you change the image, so you know whether you need to plan downtime for a repair.

1. If the `glibc` build is the same in the current and the target image, and the ICU libraries match, stop here. The collation rules don’t change.

1. [Connect to PostgreSQL](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/connect.html) and list the default locale and locale provider of each database:

   ```
   SELECT datname, datlocprovider, datcollate, datcollversion
   FROM pg_database
   WHERE datallowconn;
   ```

   Sample output

   ```
     datname  | datlocprovider | datcollate  | datcollversion
   -----------+----------------+-------------+----------------
    postgres  | c              | en_US.UTF-8 | 2.34
    template1 | c              | en_US.UTF-8 | 2.34
    cluster1  | c              | en_US.UTF-8 | 2.34
   ```

   The `datlocprovider` column shows the locale provider: `c` is libc (`glibc`), `i` is ICU, and `b` is the PostgreSQL built-in provider, available starting with PostgreSQL 17. The built-in provider doesn’t depend on `glibc` or ICU.

   PostgreSQL 14 has only the libc provider and no `datlocprovider` column. On PostgreSQL 14, run `SELECT datname, datcollate FROM pg_database WHERE datallowconn;` instead.

1. In every database, list the collations that columns, indexes, constraints, generated columns, views and partition keys use. Any of them can set a collation that differs from the database default:

   ```
   SELECT c.collname AS collation, c.collprovider, c.collcollate AS locale,
          count(*) AS objects
   FROM pg_depend d
   JOIN pg_collation c
     ON d.refclassid = 'pg_collation'::regclass AND d.refobjid = c.oid
   WHERE c.collname NOT IN ('C', 'POSIX', 'default')
   GROUP BY 1, 2, 3
   UNION ALL
   SELECT 'default', 'd', datcollate, NULL
   FROM pg_database WHERE datname = current_database()
   ORDER BY 1;
   ```

   Sample output

   ```
    collation  | collprovider |   locale    | objects
   ------------+--------------+-------------+---------
    C.utf8     | c            | C.utf8      |       1
    default    | d            | en_US.UTF-8 |
    sv_SE.utf8 | c            | sv_SE.utf8  |       2
   ```

   If every locale on the list is `C` or `POSIX`, or the database uses the built-in provider, this database isn’t affected.

1. For each `glibc` locale on your list, find out whether its sorting rules changed between the two images.

   The Operator creates clusters with the `en_US.UTF-8` locale. In the PostgreSQL images of Operator 3.1.0, `en_US.UTF-8` sorts the same on the UBI 8, UBI 9 and UBI 10 tags. A cluster that uses only `en_US.UTF-8` doesn’t need a repair when it moves between these images. `C.UTF-8` is different: it sorts differently on UBI 8 than on UBI 9 and UBI 10. The difference affects only strings with unassigned Unicode code points, but PostgreSQL doesn’t warn about it.

   For other locales, and for images of later Operator releases, compare the sort order yourself.

   1. Export the distinct values of the text columns that use the locale to one file on your workstation. Only values in indexes, partition keys and constraints can break, so export only those columns. In `psql`, run:

      ```
      \copy (SELECT <column> FROM <table> UNION SELECT <column> FROM <other_table>) TO 'values.txt'
      ```

      List every such column with that locale in the query. Include values with accented letters, punctuation and non-Latin characters if your data has them.

   1. Sort the same file in a temporary Pod of the current image and of the target image. The command prints a checksum of the sorted output, or a message if the image doesn’t have the locale:

      ```
      kubectl run sort-check -n <namespace> --rm -i --restart=Never \
        --image=<postgres-image> --command -- \
        sh -c 'if LC_ALL=<locale> locale 2>&1 >/dev/null | grep -q .; then echo "Locale <locale> is missing in this image"; else LC_ALL=<locale> sort | md5sum; fi' \
        < values.txt
      ```

   1. Compare the checksum lines of the two runs. Different checksums mean the rules changed for your data. `kubectl` also prints a `pod "sort-check" deleted` line, which you can ignore.

   Use one file for both images. Don’t export the data again from each server: a server can return rows in the order of its existing index, which is the old order. If the image doesn’t have the locale, `sort` silently uses byte order, so both checksums would match even if the rules changed. The command checks this for you.

   Matching checksums prove only that the rules didn’t change for the values in your file. For ICU collations, compare the ICU versions of both images.

1. Decide:

   - No locale on your list changed: you don’t need to repair anything.
   - A locale on your list changed, or you can’t confirm that it didn’t: plan a repair. [Repair data after a collation change](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/collation-repair.html) tells you whether you need the full procedure or a targeted repair, and how to rehearse it. Stop writes before you change the image: from the moment a Pod starts on the new image, the old indexes let duplicate keys in.

If you need a repair, stop application traffic before you start the upgrade. The Operator starts the cluster as soon as the upgrade finishes, so applications can connect before you [repair the affected objects](#check-collation).

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

1. If the [collation risk assessment](#assess-the-collation-risk) showed that a locale you use changed, or you couldn’t confirm that it didn’t, [repair the affected objects](#check-collation) before applications connect.

## Repair collation-affected objects

If the [collation risk assessment](#assess-the-collation-risk) showed that a locale you use changed, or you couldn’t confirm that it didn’t, follow [Repair data after a collation change](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/collation-repair.html) as soon as the cluster is ready. Keep the applications stopped until the repair is done.

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
