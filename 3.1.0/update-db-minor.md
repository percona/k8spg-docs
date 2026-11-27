> For the complete documentation index, see [llms.txt](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/llms.txt).

# Minor version upgrade of Percona Distribution for PostgreSQL

A minor version upgrade is the upgrade within the same major version. For example, from 17.5.2 to 17.6.1.

## Considerations

1. Upgrading a PostgreSQL cluster may result in downtime, as well as in [failover](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/change-primary.html) caused by updating the primary instance.
1. Starting with the Operator 2.6.0, Percona Distribution for PostgreSQL images are based on Red Hat Universal Base Image (UBI) 9. Each UBI major version ships a different version of `glibc` and ICU collation libraries, and a new image build within one UBI major can update `glibc` as well. A different `glibc` build can change the sorting rules of some locales and corrupt the objects that depend on them, such as text-based indexes. Before the upgrade, [check whether the change affects the locales your databases use](#assess-the-collation-risk). See the [glibc collation limitation](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/limitations.html#glibc-collation-changes-between-images).
1. [Logical replicas](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/logical-replication.html) can keep replicating after a minor upgrade if you [configured replication slots](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/ha-deploy.html#persist-replication-slots-across-failover). Without slots, a failover during the upgrade can break replication. [Reseed](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/logical-replication.html#reseed-a-logical-replica) the replica if the status becomes `broken`.

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

If you need a repair, plan a maintenance window and stop application traffic before the upgrade. The Operator restarts the Pods on the new image one by one, replicas first and the primary last. Replicas then run on the new `glibc` with indexes that the old one built, while applications stay connected. [Repair the data](#after-the-pods-restart) before you let applications back in.

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

If the [collation risk assessment](#assess-the-collation-risk) showed that a locale you use changed, or you couldn’t confirm that it didn’t, follow [Repair data after a collation change](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/collation-repair.html) when all Pods run on the new image. Keep the applications stopped until the repair is done.
