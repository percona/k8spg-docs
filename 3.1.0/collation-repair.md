> For the complete documentation index, see [llms.txt](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/llms.txt).

# Repair data after a collation change

PostgreSQL sorts text with the locale rules of the `glibc` or ICU library in the database image. When an upgrade, a change of the image tag suffix or a migration from Crunchy moves your data to an image with different rules, the existing indexes, partitions and constraints keep the old order. Queries can then miss rows, and unique indexes can let duplicate keys in.

This page shows how to find and repair those objects. You need it only if the collation risk assessment showed that a locale you use changed. For the background, see the [glibc collation limitation](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/limitations.html#glibc-collation-changes-between-images).

## When you need this procedure

Run the collation risk assessment before you change the image: on the [minor upgrade](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/update-db-minor.html#assess-the-collation-risk) or [major upgrade](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/update-db-major.html#assess-the-collation-risk) page, or in the [pre-migration checks](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/migrate-checklist.html#assess-the-collation-risk) for a migration. Its result decides what you do here, for each database separately:

| Assessment result for a database                                                | What to do                                                                                          |
| ------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------- |
| No locale that the database uses changed                                        | Nothing. You don’t need this page                                                                   |
| The default locale of the database changed, or you can’t confirm that it didn’t | Follow the **full procedure**: every step, for every object in the database                         |
| Only a collation that some columns or indexes set for themselves changed        | Follow the **targeted repair**: every step, but only for the objects that use the changed collation |

Most clusters don’t need a repair. The Operator creates clusters with the `en_US.UTF-8` locale, which sorts the same on the UBI 8, UBI 9 and UBI 10 images of Operator 3.1.0.

The full procedure reads every table several times and rebuilds every index. Its duration depends on the size of the database, not on how many rows changed. If a rehearsal shows that it doesn’t fit your maintenance window, move the data into a cluster on the target image with `pg_dump` and `pg_restore` instead. `pg_restore` builds every index with the new rules, so the indexes need no repair. Rows that violate a `CHECK` constraint or a partition bound under the new rules make the restore of that table fail.

## Before you start

1. **Rehearse the repair.** [Restore a recent backup to a new cluster](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/backups-clone.html) that uses the target image, follow this page there, and measure how long it takes. Plan the maintenance window from that time.

1. **Stop writes before you change the image.** From the moment a Pod starts on the new image, the old indexes let duplicate keys in, and `INSERT ... ON CONFLICT` can insert rows it should skip. Scale the applications that write to the database to zero replicas, for example:

   ```
   kubectl scale deployment <application> -n <application-namespace> --replicas=0
   ```

   Also stop the applications that read from replicas. Replicas return wrong results until the repair is done. Keep the applications stopped until you finish the [verification](#verify-the-repair).

1. **Check the free space.** Rebuilding indexes and moving rows write a lot of WAL. Make sure the volumes of the PostgreSQL Pods have room for it.

1. **Open one `psql` session on the primary.** Several steps use session settings and the `psql` command `\gexec`, so run all steps of one database in the same session. Find the primary Pod and connect to the database:

   ```
   kubectl get pods -n <namespace> -l postgres-operator.crunchydata.com/role=primary
   kubectl exec -it -n <namespace> <primary-pod> -c database -- psql -d <database_name>
   ```

   You need the privileges of the superuser or the database owner.

## Repair the data

Repeat these steps for every database that needs a repair.

Repair in this order, because each step relies on the previous one. In the full procedure, each step covers every object in the database. In the targeted repair, it covers only the objects that use a changed collation.

1. Find the indexes that depend on a `glibc` collation. In the full procedure, the list shows which unique indexes can fail in step 2:

   ```
   WITH db AS (
     SELECT datlocprovider = 'c'
            AND datcollate NOT IN ('C', 'POSIX') AS default_is_libc
     FROM pg_database WHERE datname = current_database()
   ),
   keys AS (
     SELECT i.indexrelid, i.indrelid, i.indisunique, i.indpred,
            k.coll, opc.opcname, opc.opcintype
     FROM pg_index i
     CROSS JOIN LATERAL unnest(i.indcollation::oid[], i.indclass::oid[])
                        AS k(coll, opclass)
     JOIN pg_opclass opc ON opc.oid = k.opclass
   )
   SELECT DISTINCT n.nspname AS schema, t.relname AS table_name,
          ic.relname AS index_name, am.amname AS index_type,
          CASE WHEN k.opcintype = 'jsonb'::regtype THEN 'database default (jsonb)'
               WHEN c.collprovider = 'd' THEN 'database default'
               WHEN c.oid IS NOT NULL THEN c.collname
               ELSE 'predicate only' END AS collation,
          k.indisunique AS is_unique,
          pg_get_expr(k.indpred, k.indrelid) AS partial_predicate
   FROM keys k
   JOIN pg_class ic ON ic.oid = k.indexrelid
   JOIN pg_class t  ON t.oid = k.indrelid
   JOIN pg_namespace n ON n.oid = t.relnamespace
   JOIN pg_am am ON am.oid = ic.relam
   LEFT JOIN pg_collation c ON c.oid = k.coll
   CROSS JOIN db
   WHERE n.nspname NOT IN ('pg_catalog', 'information_schema')
     AND k.opcname NOT IN ('text_pattern_ops', 'varchar_pattern_ops', 'bpchar_pattern_ops')
     AND (   (c.collprovider = 'c' AND c.collcollate NOT IN ('C', 'POSIX'))
          OR (c.collprovider = 'd' AND db.default_is_libc)
          OR (k.opcintype = 'jsonb'::regtype AND am.amname = 'btree'
              AND db.default_is_libc)
          OR k.indpred IS NOT NULL)
   ORDER BY 1, 2, 3;
   ```

   Sample output

   ```
    schema | table_name |     index_name      | index_type |        collation         | is_unique |  partial_predicate
   --------+------------+---------------------+------------+--------------------------+-----------+----------------------
    public | customers  | customers_doc_idx   | btree      | database default (jsonb) | f         |
    public | customers  | customers_email_key | btree      | database default         | t         |
    public | customers  | customers_name_idx  | btree      | sv_SE.utf8               | f         |
    public | customers  | customers_open_idx  | btree      | predicate only           | f         | (status > 'm'::text)
    public | notes      | notes_lower_idx     | btree      | C.utf8                   | f         |
   ```

   On PostgreSQL 14, remove `datlocprovider = 'c' AND` from the `db` part at the beginning of the query.

   The `collation` column names the collation of the index key. `database default` means the default locale of the database. Repair the indexes whose collation uses a locale that changed, and skip the rest. For an index marked `predicate only`, check the `partial_predicate` column: repair the index if its condition compares text with `<`, `>` or `BETWEEN`.

1. Rebuild the indexes. Writes are stopped, so use the plain form of [`REINDEX`](https://www.postgresql.org/docs/current/sql-reindex.html) , which is faster than the concurrent one.

   - Full procedure: rebuild all indexes of the database. `VERBOSE` prints each table as it’s done:

     ```
     REINDEX (VERBOSE) DATABASE <database_name>;
     ```

   - Targeted repair: rebuild each index from the step 1 list whose collation changed:

     ```
     REINDEX INDEX <index_name>;
     ```

   `REINDEX` blocks writes to the table and the queries that use the index while it runs. If the applications must keep reading during the repair, use `REINDEX INDEX CONCURRENTLY <index_name>;` instead. It takes longer, and it can’t rebuild the index of an exclusion constraint, so use the plain form for those.

   A `UNIQUE` index, a primary key or an exclusion constraint fails to rebuild if the old sort order let duplicate keys in. The error names the index and the duplicated key. A failed concurrent rebuild also leaves an invalid index named `<index_name>_ccnew`. Drop it with `DROP INDEX CONCURRENTLY <index_name>_ccnew;`.

   To find the duplicates, turn off index scans in your session, so that PostgreSQL doesn’t read the broken index:

   ```
   SET enable_indexscan = off;
   SET enable_indexonlyscan = off;
   SET enable_bitmapscan = off;
   SELECT <key_columns>, count(*)
   FROM <table_name>
   GROUP BY <key_columns>
   HAVING count(*) > 1;
   ```

   For a partitioned table, run the query on the parent table. Decide which rows to keep, remove the duplicates in the same session, and run the `REINDEX` command again. In the full procedure, `REINDEX DATABASE` stops at the first error, and the tables it already printed are done. Rebuild the failed table and the remaining ones with `REINDEX TABLE <table_name>;`, or run `REINDEX DATABASE` again. Duplicates in different partitions don’t stop the rebuild, because each partition has its own index. They show up in step 3, when you move the rows.

1. Move rows that are in the wrong partition. A range-partitioned table routes each row to a partition by comparing the key with the partition bounds. Rows that were routed with the old rules can be in the wrong partition, and queries through the parent table don’t find them. A new row with the same key can then be inserted into the right partition, even if the key is unique. Do this step after step 2: the queries in this step don’t find misplaced rows through an index that isn’t rebuilt yet.

   1. Find the partitioned tables whose key uses a `glibc` collation:

      ```
      WITH db AS (
        SELECT datlocprovider = 'c' AND datcollate NOT IN ('C', 'POSIX') AS default_is_libc
        FROM pg_database WHERE datname = current_database()
      )
      SELECT p.partrelid::regclass AS partitioned_table,
             CASE p.partstrat WHEN 'r' THEN 'range' WHEN 'l' THEN 'list' ELSE 'hash' END AS strategy,
             coalesce(a.attname, '(expression)') AS key_column,
             CASE WHEN c.collprovider = 'd' THEN 'database default' ELSE c.collname END AS collation
      FROM pg_partitioned_table p
      CROSS JOIN LATERAL unnest(p.partattrs::int2[], p.partcollation::oid[]) AS k(attnum, coll)
      JOIN pg_collation c ON c.oid = k.coll
      LEFT JOIN pg_attribute a ON a.attrelid = p.partrelid AND a.attnum = k.attnum
      CROSS JOIN db
      WHERE ((c.collprovider = 'c' AND c.collcollate NOT IN ('C', 'POSIX'))
             OR (c.collprovider = 'd' AND db.default_is_libc))
        AND NOT (p.partstrat = 'h' AND k.attnum <> 0)   -- plain hash key: bytes
      ORDER BY 1;
      ```

      On PostgreSQL 14, remove `datlocprovider = 'c' AND` from the `db` part at the beginning of the query.

      The query lists range and list partitioned tables, and hash partitioned tables whose key is an expression, such as `lower(sku)`. Only range partitions depend on the sort order. For list and hash tables, check only keys with expressions. A table with sub-partitions is listed once for each level. Run the next steps only for the top-level table. They cover all levels below it.

   1. For each table from the list, count the rows that are outside the bounds of their partition. Run this in `psql`. `\gexec` runs the query that the first query builds:

      ```
      SET enable_indexscan = off;
      SET enable_indexonlyscan = off;
      SET enable_bitmapscan = off;
      SELECT string_agg(
               format('SELECT %L AS partition, count(*) AS misplaced FROM ONLY %s WHERE NOT (%s)',
                      relid, relid, pg_get_partition_constraintdef(relid)),
               ' UNION ALL ') || ' ORDER BY 1'
      FROM pg_partition_tree('<partitioned_table>')
      WHERE isleaf AND pg_get_partition_constraintdef(relid) IS NOT NULL
      \gexec
      ```

      The `SET` commands make the query read every row of the table instead of an index, so run it when the load is low. The count covers the default partition and sub-partitions. A row is counted in the partition that holds it. A non-zero count in the default partition means rows that now belong to a named partition.

   1. For each table with misplaced rows, move the rows through the top-level table, which routes them again with the new rules.

      If another table has a foreign key that references this table, drop that foreign key first. Otherwise the move fails with `violates foreign key constraint`, or, if the foreign key has `ON DELETE CASCADE`, deletes the referencing rows without an error. To find these foreign keys, run:

      ```
      SELECT conrelid::regclass AS table_name, conname AS constraint_name,
             pg_get_constraintdef(oid) AS definition
      FROM pg_constraint
      WHERE contype = 'f' AND confrelid = '<partitioned_table>'::regclass;
      ```

      Save the definitions, and drop each foreign key with `ALTER TABLE <table_name> DROP CONSTRAINT <constraint_name>;`.

      Then run the move in `psql`, in the same session as the previous step, so that index scans stay off. The query builds a statement for each partition, and `\gexec` runs them. Each statement deletes the misplaced rows from one partition and inserts them through the top-level table:

      ```
      SELECT format(
               'WITH moved AS (DELETE FROM ONLY %s WHERE NOT (%s) RETURNING %s) INSERT INTO %s (%s) %s SELECT %s FROM moved',
               t.relid, pg_get_partition_constraintdef(t.relid), cols.list,
               pg_partition_root(t.relid), cols.list,
               CASE WHEN cols.has_identity THEN 'OVERRIDING SYSTEM VALUE' ELSE '' END, cols.list)
      FROM pg_partition_tree('<partitioned_table>') t
      CROSS JOIN LATERAL (
        SELECT string_agg(quote_ident(attname), ', ' ORDER BY attnum) AS list,
               bool_or(attidentity = 'a') AS has_identity
        FROM pg_attribute
        WHERE attrelid = pg_partition_root(t.relid) AND attnum > 0
          AND NOT attisdropped AND attgenerated = ''
      ) cols
      WHERE t.isleaf AND pg_get_partition_constraintdef(t.relid) IS NOT NULL
      \gexec
      ```

      The statements list the columns by name and leave out generated columns, which PostgreSQL computes again. For an identity column defined as `GENERATED ALWAYS`, they add `OVERRIDING SYSTEM VALUE`, so each row keeps its value. A statement for a partition without misplaced rows reports `INSERT 0 0`. For example, for the partition `sales_low` of the table `sales`, the query builds:

      ```
      WITH moved AS (DELETE FROM ONLY sales_low WHERE NOT (((sku IS NOT NULL) AND (sku < 'm'::text COLLATE "C.utf8"))) RETURNING id, sku, qty) INSERT INTO sales (id, sku, qty) OVERRIDING SYSTEM VALUE SELECT id, sku, qty FROM moved
      ```

      Each statement moves all misplaced rows of a partition in one transaction. To move many rows in smaller batches, replace `WHERE NOT (<bounds>)` with `WHERE ctid IN (SELECT ctid FROM ONLY <partition> WHERE NOT (<bounds>) LIMIT 10000)`, and run the statement until it reports `INSERT 0 0`.

      If a statement fails with a duplicate key error, a row with the same key was inserted into the right partition after the `glibc` change. A query through the parent table finds only that new row. To see both rows, query the two partitions with `FROM ONLY`: the partition you’re moving from, and the partition of the index named in the error. Delete the row you don’t want to keep with `DELETE FROM ONLY <partition> WHERE <key_column> = <value>;`, and run the move again.

      When all rows are moved, add the foreign keys back with `NOT VALID`, then validate them:

      ```
      ALTER TABLE <table_name> ADD CONSTRAINT <constraint_name> <definition> NOT VALID;
      ALTER TABLE <table_name> VALIDATE CONSTRAINT <constraint_name>;
      ```

1. Repair the other objects that depend on the sort order of the changed locales. `REINDEX` doesn’t fix them:

   | Object                                                       | What to do                                                                                                                                                                                                                                                                                                           |
   | ------------------------------------------------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
   | Foreign keys that compare text                               | Drop the constraint, add it again with `NOT VALID`, then run `ALTER TABLE ... VALIDATE CONSTRAINT`                                                                                                                                                                                                                   |
   | `CHECK` constraints and domain constraints that compare text | Find the rows that violate the constraint with `SELECT * FROM <table_name> WHERE NOT (<constraint_expression>);` and fix them. `VALIDATE CONSTRAINT` only reports that some row violates the constraint, not which one                                                                                               |
   | Stored generated columns that compare or sort text           | Recompute the values with an update that sets a column used in the expression to itself, for example `UPDATE <table_name> SET <column> = <column>;`. Setting the generated column to `DEFAULT` doesn’t recompute it. Starting with PostgreSQL 17, you can also use `ALTER TABLE ... ALTER COLUMN ... SET EXPRESSION` |
   | Materialized views                                           | Run `REFRESH MATERIALIZED VIEW` without `CONCURRENTLY`. It rebuilds the rows and the view’s indexes. With `CONCURRENTLY`, the view’s broken unique index stays broken                                                                                                                                                |

1. Record the new collation version. `REFRESH COLLATION VERSION` only updates the metadata and doesn’t repair anything, so run it last:

   ```
   ALTER DATABASE <database_name> REFRESH COLLATION VERSION;
   ```

   If a column or an index uses a collation other than the database default, refresh that collation too:

   ```
   ALTER COLLATION <collation_name> REFRESH VERSION;
   ```

   Repeat for every database, including `postgres` and `template1`. If `template1` keeps the old version, `CREATE DATABASE` fails with `template database "template1" has a collation version mismatch`.

   PostgreSQL 14 doesn’t have `ALTER DATABASE ... REFRESH COLLATION VERSION`. On PostgreSQL 14, run only `ALTER COLLATION ... REFRESH VERSION`.

1. Update the planner statistics:

   ```
   ANALYZE;
   ```

## Verify the repair

1. Check the indexes of all databases with `pg_amcheck` in the `database` container of the primary Pod:

   ```
   kubectl exec -n <namespace> <primary-pod> -c database -- \
     pg_amcheck --all --install-missing --heapallindexed
   ```

   No output and exit code 0 mean no errors. If you run the check again, `pg_amcheck` prints `NOTICE: extension "amcheck" already exists, skipping` for each database. These notices aren’t errors.

   Without `--install-missing`, `pg_amcheck` skips every database that doesn’t have the `amcheck` extension and prints only a warning. With it, `pg_amcheck` installs the extension in every database, including `template1`. `pg_amcheck` checks only B-tree indexes and doesn’t find extra entries in partial indexes, so a clean result doesn’t replace the repair steps.

1. Start the applications again.

## See also

- [glibc collation changes between images](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/limitations.html#glibc-collation-changes-between-images) explains why the sort order changes and what breaks.
- [Minor version upgrade](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/update-db-minor.html) and [Major version upgrade](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/update-db-major.html) show when to run this procedure during an upgrade.
- [Pre-migration compatibility checks](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/migrate-checklist.html#decide-what-to-do-if-the-libraries-differ) show when to run it for each migration method from Crunchy.
