# Repair data after a collation change

PostgreSQL sorts text with the locale rules of the `glibc` or ICU library in the database image. When an upgrade, a change of the image tag suffix or a migration from Crunchy moves your data to an image with different rules, the existing indexes, partitions and constraints keep the old order. Queries can then miss rows, and unique indexes can let duplicate keys in.

This page shows how to find and repair those objects. You need it only if the collation risk assessment showed that a locale you use changed. For the background, see the [glibc collation limitation](limitations.md#glibc-collation-changes-between-images).

## When you need this procedure

Run the collation risk assessment before you change the image: on the [minor upgrade](update-db-minor.md#assess-the-collation-risk) or [major upgrade](update-db-major.md#assess-the-collation-risk) page, or in the [pre-migration checks](migrate-checklist.md#assess-the-collation-risk) for a migration. Its result decides what you do here, for each database separately:

| Assessment result for a database | What to do |
| -------------------------------- | ---------- |
| No locale that the database uses changed | Nothing. You don't need this page |
| The default locale of the database changed, or you can't confirm that it didn't | Follow the **full procedure**: every step, for every object in the database |
| Only a collation that some columns or indexes set for themselves changed | Follow the **targeted repair**: every step, but only for the objects that use the changed collation |

Most clusters don't need a repair. The Operator creates clusters with the `en_US.UTF-8` locale, which sorts the same on the UBI 8, UBI 9 and UBI 10 images of Operator 3.1.0.

The full procedure reads every table several times and rebuilds every index. Its duration depends on the size of the database, not on how many rows changed. If a rehearsal shows that it doesn't fit your maintenance window, move the data into a cluster on the target image with `pg_dump` and `pg_restore` instead. `pg_restore` builds every index with the new rules, so the indexes need no repair. Rows that violate a `CHECK` constraint or a partition bound under the new rules make the restore of that table fail.

## Before you start

1. **Rehearse the repair.** [Restore a recent backup to a new cluster](backups-clone.md) that uses the target image, follow this page there, and measure how long it takes. Plan the maintenance window from that time.

2. **Stop writes before you change the image.** From the moment a Pod starts on the new image, the old indexes let duplicate keys in, and `INSERT ... ON CONFLICT` can insert rows it should skip. Scale the applications that write to the database to zero replicas, for example:

    ```bash
    kubectl scale deployment <application> -n <application-namespace> --replicas=0
    ```

    Also stop the applications that read from replicas. Replicas return wrong results until the repair is done. Keep the applications stopped until you finish the [verification](#verify-the-repair).

3. **Check the free space.** Rebuilding indexes and moving rows write a lot of WAL. Make sure the volumes of the PostgreSQL Pods have room for it.

4. **Open one `psql` session on the primary.** Several steps use session settings and the `psql` command `\gexec`, so run all steps of one database in the same session. Find the primary Pod and connect to the database:

    ```bash
    kubectl get pods -n <namespace> -l postgres-operator.crunchydata.com/role=primary
    kubectl exec -it -n <namespace> <primary-pod> -c database -- psql -d <database_name>
    ```

    You need the privileges of the superuser or the database owner.

## Repair the data

Repeat these steps for every database that needs a repair.

--8<-- "collation.txt"

## Verify the repair

1. Check the indexes of all databases with `pg_amcheck` in the `database` container of the primary Pod:

    ```bash
    kubectl exec -n <namespace> <primary-pod> -c database -- \
      pg_amcheck --all --install-missing --heapallindexed
    ```

    No output and exit code 0 mean no errors. If you run the check again, `pg_amcheck` prints `NOTICE:  extension "amcheck" already exists, skipping` for each database. These notices aren't errors.

    Without `--install-missing`, `pg_amcheck` skips every database that doesn't have the `amcheck` extension and prints only a warning. With it, `pg_amcheck` installs the extension in every database, including `template1`. `pg_amcheck` checks only B-tree indexes and doesn't find extra entries in partial indexes, so a clean result doesn't replace the repair steps.

2. Start the applications again.

## See also

- [glibc collation changes between images](limitations.md#glibc-collation-changes-between-images) explains why the sort order changes and what breaks.
- [Minor version upgrade](update-db-minor.md) and [Major version upgrade](update-db-major.md) show when to run this procedure during an upgrade.
- [Pre-migration compatibility checks](migrate-checklist.md#decide-what-to-do-if-the-libraries-differ) show when to run it for each migration method from Crunchy.
