# Insert sample data

In this section you will learn to insert some sample data to PostgreSQL.

## Create a schema

Every database in PostgreSQL has a default schema called `public`. A schema stores database objects like tables, views, indexes and allows organizing them into logical groups. 

When you create a table, it ends up in the `public` schema by default. In PostgreSQL 15, non-database owners cannot access the `public` schema. Therefore, you need to create a new schema to insert the data.

Use the following statement to create a schema

```sql
CREATE SCHEMA demo;
```

## Create a table

After you created a schema, all tables you create end up in this schema if not specified otherwise.

At this step, we will create a sample table `Library` as follows:

```sql
CREATE TABLE LIBRARY(
   ID INTEGER NOT NULL,
   NAME TEXT,
   SHORT_DESCRIPTION TEXT,
   AUTHOR TEXT,
   DESCRIPTION TEXT,
   CONTENT TEXT,
   LAST_UPDATED DATE,
   CREATED DATE
);
```

## Insert the data

PostgreSQL does not have the built-in support to generate random data. However, it provides the `random()` function which generates random numbers and `generate_series()` function which generates the series of rows and populates them with the numbers incremented by 1 (by default).

Combine these functions with a couple of others to populate the table with the data:

```sql
INSERT INTO LIBRARY(id, name, short_description, author,
                              description,content, last_updated, created)
SELECT id, 'name', md5(random()::text), 'name2'
      ,md5(random()::text),md5(random()::text)
      ,NOW() - '1 day'::INTERVAL * (RANDOM()::int * 100)
      ,NOW() - '1 day'::INTERVAL * (RANDOM()::int * 100 + 100)
FROM generate_series(1,100) id;
```

This command does the following:

* Fills in the columns `id`, `name`, `author` with the values `id`, `name` and `name2` respectively;
* generates the random md5 hash sum as the values for the columns `short_description`, `description` and `content`;
* generates the random number of dates from the current date and time within the last 100 days, and
* inserts 100 rows of this data

Now your cluster has some data in it.

## Next steps

[Make a backup :material-arrow-right:](backup-tutorial.md){.md-button}.