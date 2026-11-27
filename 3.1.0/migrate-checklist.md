> For the complete documentation index, see [llms.txt](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/llms.txt).

# Pre-migration compatibility checks

Important

Read this before you migrate.

Complete these checks **before** you pick a migration method. Verify that source and target environments are compatible. Migration methods such as pgBackRest restore, standby replication or reusing the existing PostgreSQL data volume all reuse the source PGDATA files. For all these methods, CPU architecture and the PostgreSQL major version must match. If they don’t, migrate using `pg_dump` / `pg_restore` instead.

Differences in the operating system, libraries like `glibc`, ICU, or PostgreSQL extensions do not always block reuse of `PGDATA`. But you must take extra steps before or after the migration.

## Decide whether you can reuse the data files

Use this flow to interpret the checks. Then gather the facts in the sections that follow.

```
flowchart TD
    A[Compare PostgreSQL major versions] -->|Different| B[Do not use standby, backup/restore, or volume reuse]
    A -->|Same| C[Compare CPU architecture]
    C -->|Different| D[Prefer logical migration]
    C -->|Same| E[Compare glibc build and ICU]
    E -->|Same| F[Compare extensions]
    E -->|Different| G[Find and repair the objects that the collation change affects before applications connect]
    G --> F
    F --> K[Trial runs]
    K --> L[Fix issues if any]
    L --> M[Migrate]
    M --> N[Validate PostgreSQL and check the logs]
```

## Compare PostgreSQL major versions

The PostgreSQL major version of the source and target database images must match.

Check the source (Crunchy) PostgreSQL version:

```
kubectl exec -n <namespace> <source-postgres-pod> -c database -- \
  postgres --version
```

Sample output

```
postgres (PostgreSQL) 18.6
```

Check the version in the target Percona image as well. Find tags in [Percona certified images](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/images.html). If the Percona cluster is not running yet, start a temporary Pod from the target image:

```
kubectl run pg-image-check --rm -it --restart=Never \
  --image=<percona-postgres-image> -- \
  postgres --version
```

The major versions must match, for example:

```
Source: postgres (PostgreSQL) 18.6
Target: postgres (PostgreSQL) 18.6 - Percona Server for PostgreSQL 18.6.1
```

A difference in the minor version is normally supported by PostgreSQL’s physical storage format, but the target minor version should be equal to or newer than the source.

Do not reuse `PGDATA` or restore a physical backup directly into a different PostgreSQL major version.

## Compare CPU architecture

Check the architecture of both the source and target PostgreSQL containers:

```
kubectl exec -n <namespace> <source-postgres-pod> -c database -- uname -m
kubectl exec -n <namespace> <percona-postgres-pod> -c database -- uname -m
```

Expected output

```
x86_64
```

or:

```
aarch64
```

The source and target must use the same architecture.

For example:

```
x86_64 -> x86_64    OK
ARM64  -> ARM64     OK
x86_64 -> ARM64     Not OK
```

Use `pg_dump` / `pg_restore` when you migrate across incompatible architectures.

## Compare OS, glibc, and ICU

Crunchy and Percona images can ship different operating system releases and different `glibc` builds. A difference changes how PostgreSQL sorts text, while the indexes that you migrate keep the old order. Read the limitation, compare the images and check that the target image includes every locale your databases use, then decide how to migrate.

### Understand the glibc collation limitation

PostgreSQL sorts and compares text using the locale data of the operating system’s C library (`glibc`). If that locale data changes during the lifetime of a database, PostgreSQL treats new data differently than the data it already stored. Existing indexes no longer match the order that PostgreSQL expects. This can lead to incorrect query results and data corruption.

Operating system vendors, including the authors of the GNU C library, update locale data from time to time. They add rules for new languages, correct mistakes, and adjust sorting rules. A new image can ship a `glibc` build with such a change. Switching the image tag suffix, for example from `-ubi8` to the default UBI 9 tag, changes the operating system and always changes the `glibc` version.

Most `glibc` updates change the rules of only a few locales, or none. The risk applies only to databases that use a changed locale. Databases that use the `C` or `POSIX` locale, or the PostgreSQL built-in locale provider, aren’t affected. The libc `C.UTF-8` locale is different: its sort order changed between UBI 8 and UBI 9, and PostgreSQL records no version for it, so it never warns about the change.

PostgreSQL records the upstream `glibc` version of each collation and warns when it changes. It warns for every libc collation, including the ones whose rules didn’t change. PostgreSQL 14 doesn’t record a version for the default collation of a database, so on PostgreSQL 14 you get no warning for it. PostgreSQL can’t see a change in the package build, and it can’t tell whether the locales you use changed. There is no official tool that tells you this either, so assess the locales you use before you move data files to another image.

If the collation changes affect an index, you can see:

- Missed or extra rows in query results
- Wrong results of `ORDER BY` / `LIMIT` and of `min()` / `max()`
- Duplicate keys in `UNIQUE` indexes and primary keys, and `ON CONFLICT` clauses that misfire
- Wrong merge joins
- Runtime errors that report index corruption

The change also affects other objects that depend on the sort order: partition boundaries, constraints and derived values, materialized views, and replication. It can also affect PostgreSQL upgrades.

For more details, see the PostgreSQL wiki page [Locale data changes](https://wiki.postgresql.org/wiki/Locale_data_changes) . For worked examples of each affected object type, tested with PostgreSQL 14 to 18, see the Percona blog post [Ten ways a glibc change can break your PostgreSQL cluster](https://www.percona.com/blog/ten-ways-a-glibc-change-can-break-your-postgresql-cluster/) .

### Check operating system and glibc

Run these commands against the source Crunchy Pod. Repeat them against the target Percona image.

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

Run the queries against the source Crunchy cluster.

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

### Decide what to do if the libraries differ

If the assessment shows that no locale you use changed, continue with the next checks.

If a locale you use changed, or you can’t confirm that it didn’t, all three migration methods carry the risk. Each of them reuses the indexes that the Crunchy image built. Before you point any application to the new cluster, [repair the affected objects](#repair-the-affected-objects).

Important

Rehearse the find and repair steps in every trial run, so that you know what the checks find in your data and how long the repair takes. Repeat them during the production cutover.

Plan downtime for the repair. Duplicate keys and rows that violate a constraint need a decision from you about which data to keep.

When to run the steps depends on the migration method:

| Migration method     | When to repair                                                                                                                                                                                                                                            |
| -------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Standby cluster      | After you promote the standby. A standby is read-only and can’t repair objects, so don’t run application queries that rely on text indexes against it. The repair adds to the cutover downtime, so the standby method no longer gives near-zero downtime. |
| Backup and restore   | After the restore completes and before you point applications to the new cluster                                                                                                                                                                          |
| Reusing data volumes | After the Percona cluster starts and before you point applications to it                                                                                                                                                                                  |

### Repair the affected objects

Follow [Repair data after a collation change](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/collation-repair.html) on the primary of the Percona cluster, at the time the table in [Decide what to do if the libraries differ](#decide-what-to-do-if-the-libraries-differ) gives for your migration method.

## Compare extensions

pgBackRest restores initialize the new cluster from a physical copy of the Crunchy cluster’s data, while volume reuse starts it on the original data directory. In all three cases, the migrated data includes the `pg_extension` catalog, so PostgreSQL retains a record of installed extensions and the objects those extensions created.

The Operator does not read that catalog and copy the Crunchy settings. It applies the extension settings from the `PerconaPGCluster` manifest.

Before you apply the manifest that creates the Percona cluster, set the extension fields there to match what the source database actually uses.

### Record extensions on the source

Record the extension name and version in every application database before you migrate.

Extensions are installed per database. Check every application database, not only `postgres`:

```
SELECT
    extname,
    extversion
FROM pg_extension
ORDER BY extname;
```

Sample output

```
extname             | extversion
--------------------+-----------
plpgsql             | 1.0
pg_stat_statements  | 1.12
postgis             | 3.4.2
pgcrypto            | 1.3
```

Record the libraries PostgreSQL loads at startup:

```
SHOW shared_preload_libraries;
```

### Enable built-in extensions

Percona Distribution for PostgreSQL ships a defined set of extensions. Their versions can differ from the Crunchy image. Compare your list with the [extensions shipped with Percona Distribution for PostgreSQL](https://docs.percona.com/postgresql/latest/extensions.html).

These built-in extensions use the following defaults:

| PostgreSQL extension | `spec.extensions` field | Enabled |
| -------------------- | ----------------------- | ------- |
| `vector`             | `pgvector`              | `false` |
| `pg_stat_statements` | `pg_stat_statements`    | `false` |
| `pg_stat_monitor`    | `pg_stat_monitor`       | `false` |
| `pg_repack`          | `pg_repack`             | `false` |
| `pgaudit`            | `pg_audit`              | `true`  |
| `pg_cron`            | `pg_cron`               | `false` |

Match the spec to the extensions the source database uses. See [Built-in extensions](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/custom-extensions.html#built-in-extensions) for the full list.

Warning

**Enable every built-in extension you are migrating in the manifest that creates the cluster.** The Operator drops a built-in extension that stays disabled. If anything still depends on such disabled extension, the drop fails silently: the cluster still reports `ready`, nothing in its status flags the failure, and the Operator retries the same drop on every reconcile, logging an “Unable to disable …” event each time. You won’t get a clear error telling you to go fix it — the manifest has to be right going in.

On Operator 3.0.0, set the flag under `extensions.builtin`. Starting with version 3.1.0, set `extensions.<name>.enabled`. During the transition, `extensions.builtin` still works. If both forms are set, `extensions.builtin` takes precedence.

The following examples show `pgvector` configuration:

**Operator version 3.0.0**

```
spec:
  extensions:
    builtin:
      pgvector: true
```

**Operator version 3.1.0**

```
spec:
  extensions:
    pgvector:
      enabled: true
```

When you enable a built-in extension that is already installed, the Operator runs `ALTER EXTENSION ... UPDATE`. Compare the extension’s version on the source cluster with the version available in the target cluster’s image. Test that update in a trial run and check the application before you migrate production.

### PostGIS

PostGIS is a separate case. If the source cluster uses PostGIS, deploy the target with the [PostGIS image](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/postgis.html).

A database upgrade does not update PostGIS. Run `SELECT PostGIS_Extensions_Upgrade();` in each database that uses PostGIS. See [Upgrade the PostGIS extension](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/update-extensions.html#upgrade-postgis-extension).

### Install extensions that are not in the Percona image

Compare your `pg_extension` output with the Percona image you deploy. If you use extensions that are not in the Percona image, add them as [custom extensions](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/custom-extensions.html#add-custom-extensions).

An extension that ships a native library needs that library to be present in the target PostgreSQL installation. If the extension requires startup preloading, also list its preload library in `shared_preload_libraries`; a `pg_extension` catalog row does not provide either requirement.

For a preload library the Operator does not append, set `patroni.dynamicConfiguration.postgresql.parameters.shared_preload_libraries`. Include only those libraries. The Operator appends the libraries for built-in extensions you enable. See [Extension parameters](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/immutable-options.html#extension-parameters).

### Match set_user and pg_cron to the Operator version

`set_user` and `pg_cron` are custom extensions on Operator 3.0.0. Starting with version 3.1.0, they are built-in extensions and default to `disabled`. The Operator drops each one that stays disabled.

| Extension  | Operator 3.0.0                                                                      | Operator 3.1.0 and later                                                                                                                              |
| ---------- | ----------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------- |
| `set_user` | Add it under `extensions.custom`. Include `set_user` in `shared_preload_libraries`. | Set `extensions.set_user.enabled` to `true`. The Operator appends `set_user` to `shared_preload_libraries`.                                           |
| `pg_cron`  | Add it under `extensions.custom`. Include `pg_cron` in `shared_preload_libraries`.  | Set `extensions.pg_cron.enabled` to `true`. The Operator appends `pg_cron` to `shared_preload_libraries` and sets `cron.database_name` to `postgres`. |

On Operator 3.0.0, first package and configure both as custom extensions by following [Add custom extensions](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/custom-extensions.html#add-custom-extensions). After you configure `extensions.image` and `extensions.storage`, add these entries:

```
spec:
  extensions:
    custom:
      - name: set_user
        version: "<set_user-version>"
      - name: pg_cron
        version: "<pg_cron-version>"
  patroni:
    dynamicConfiguration:
      postgresql:
        parameters:
          shared_preload_libraries: "set_user,pg_cron"
```

Starting with version 3.1.0, enable the built-in flags. The Operator appends `set_user` and `pg_cron` to `shared_preload_libraries`. Set that parameter for any other preload libraries:

```
spec:
  extensions:
    set_user:
      enabled: true
    pg_cron:
      enabled: true
```

Warning

Starting with version 3.1.0, use the built-in flags for a new cluster. Removing `set_user` or `pg_cron` from `extensions.custom` without setting its `enabled` flag to `true` in the same apply deletes the extension.

If the source cluster schedules `pg_cron` jobs in a database other than `postgres`, those jobs stop running after migration. The Operator sets `cron.database_name` to `postgres`.

On the source cluster, check the current value:

```
SHOW cron.database_name;
```

When the result is `postgres`, the existing jobs keep running. When it is another database, `pg_cron` stops reading the job list stored there. In that database, list the jobs:

```
SELECT jobname, schedule, command, database FROM cron.job;
```

After the Percona cluster is running, connect to the `postgres` database and create each job again with `cron.schedule_in_database`. The last argument is the database where the command runs (`appdb` in this example):

```
SELECT cron.schedule_in_database('weekly-vacuum', '0 4 * * 0', 'VACUUM', 'appdb');
```

You can also [add custom extensions](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/custom-extensions.html#add-custom-extensions) if you need them or if they are missing in Percona images. Evaluate the risk before you add any extension.

After the Percona cluster reports `Ready`, check the database logs. In every database that you recorded earlier, run `\dx` and confirm that each extension is installed at the version you tested.

## Check what else changes after migration

The migration methods in this guide copy the data directory, so the migrated cluster keeps the data itself. The Operator still applies its own naming, defaults, and labels on top of that data. None of this blocks the migration, but missing it causes problems ranging from broken logins to blind monitoring.

### Match passwords for Operator-managed users

The Operator doesn’t copy user credentials from Crunchy during migration. It generates a new password for any user it manages and applies it to the database, overwriting the password that migrated with the data. Existing application logins break the moment the Operator reconciles that user.

To keep the Crunchy passwords, do this **before** you create the cluster:

- Copy the `password` and `verifier` keys into the `<clusterName>-pguser-<userName>` Secret
- List every migrated user in `spec.users`. See [Understanding default user management](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/users.html#understanding-default-user-management) for the naming convention.

### Keep the user schema behavior Crunchy had

Crunchy puts a user’s tables in the `public` schema by default. The Operator’s `autoCreateUserSchema` defaults to `true` and creates a schema named after the user instead. Set it to `false` in the manifest that creates the cluster if your application expects unqualified table names to resolve to `public`.

### Recreate non-extension Postgres settings

The Operator does not carry over Crunchy’s `dynamicConfiguration`. Only `pgaudit` is preloaded by default. If the source cluster set other `postgresql.conf` parameters or preloaded other libraries, add them under `patroni.dynamicConfiguration.postgresql.parameters` and `shared_preload_libraries` the same way you already did for extensions. See [Extension parameters](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/immutable-options.html#extension-parameters).

### Update labels, Services and anything that reads them

The primary Pod’s `postgres-operator.crunchydata.com/role` label changes value from `master` to `primary`, and every Service name follows the new cluster name instead of Crunchy’s. Update NetworkPolicies, alert rules, and any script or dashboard that selects on the old label value or Service name.

### Replace monitoring and admin tools

pgMonitor, its `ccp_*` metrics, and its Grafana dashboards don’t carry over. Replace them with [Percona Monitoring and Management](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/monitor-kubernetes.html) or a [`postgres_exporter` sidecar](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/postgres-exporter.html).

pgAdmin and OpenTelemetry collection have no equivalent in the Operator. Plan an alternative before cutover if you depend on either.

### Rotate TLS certificates after a standby cutover

[Migrating using a standby cluster](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/migrate-from-crunchy-standby.html) keeps Crunchy-issued certificates for mutual TLS during replication. Replace them with the Operator-issued or your own certificates after cutover, so the new primary doesn’t keep trusting Crunchy’s CA indefinitely.

## Before you cut over

Perform at least **three successful trial runs** in a comparable test environment and validate the application after each one. The first run usually exposes missing steps, the second confirms the fixes, and the third shows that the procedure is repeatable and the cutover time is predictable. Capture that as a detailed, environment-specific runbook before you migrate production workloads.

After PostgreSQL starts under Percona Operator for PostgreSQL, check the PostgreSQL logs for errors, then confirm that extensions are complete. If the `glibc` builds differ, also confirm that you repaired the affected objects before applications connect.
