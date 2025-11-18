# 3 Insert sample data

The next step after [connecting to the cluster](connect.md) is to insert some sample data to PostgreSQL.

When you start a PostgreSQL container and connect to the database, a user is created with the username that matches the name of your cluster. Also, a database and a schema named after the name of this user are created so that you can [create a table](#create-a-table) right away.

## Create a schema (for Operator version earlier than 2.6.0)

In Operator versions earlier than 2.6.0, you must create a new schema to insert the data. This is because your user cannot access the default schema called `public` due to PostgreSQL restrictions (instroduced starting with PostgreSQL 15).

A schema stores database objects like tables, views, indexes and allows organizing them into logical groups.

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

!!! tip

    If the schema has not been automatically set to the one you created, set it manually using the following SQL statement:

    ```sql
    SET schema 'demo';
    ```

    Replace the `demo` schema name with your value if you used another name.

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

[:fontawesome-brands-amazon: Make a backup :material-arrow-right:](backup-tutorial.md){.md-button}
