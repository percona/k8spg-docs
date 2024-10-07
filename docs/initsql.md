# How to run initialization SQL commands at cluster creation time

The Operator can execute a custom sequence of PostgreSQL commands when creating the databse cluster. This sequence can include both SQL commands and meta-commands of the PostgreSQL interactive shell (psql). This feature may be useful to push any customizations to the cluster: modify user roles, change error handling, set and use variables, etc.

psql interactive terminal [will execute :octicons-link-external-16:](https://www.postgresql.org/docs/current/app-psql.html#APP-PSQL-OPTION-FILE) these initialization statements when the cluster is created, [after creating custom users and databases](users.md#application-users) specifed in the Custom Resource.

To set SQL initialization sequence you need creating a special [ConfigMap :octicons-link-external-16:](https://kubernetes.io/docs/tasks/configure-pod-container/configure-pod-configmap/#create-a-configmap) with it, and reference this ConfigMap in the `databaseInitSQL` subsection of your Custom Resource options.

The following example uses SQL commands from the [insert data tutorial](data-insert.md) to automate creation of a sample table `Library`:

```sql
CREATE SCHEMA demo;
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

1. Create YAML manifest for the ConfigMap as follows:

    ```yaml title="my_init.yaml"
    apiVersion: v1
    kind: ConfigMap
    metadata:
      name: cluster1-init-sql
      namespace: postgres-operator
    data:
      init.sql: CREATE SCHEMA demo; CREATE TABLE LIBRARY( ID INTEGER NOT NULL, NAME TEXT, SHORT_DESCRIPTION TEXT, AUTHOR TEXT, DESCRIPTION TEXT, CONTENT TEXT, LAST_UPDATED DATE, CREATED DATE );
    ```

    The `namespace` field should point to the namespace of your database cluster, and the `init.sql` key contains the sequence of commands, which will be passed to the psql.

    Create the ConfigMap by applying your manifest:
    
    ``` {.bash data-prompt="$" }
    $ kubectl apply -f my_init.yaml
    ```

2. Update the `databaseInitSQL` part of the `deploy/cr.yaml` Custom Resource manifest as follows:

    ```yaml
    ...
    databaseInitSQL:
      key: init.sql
      name: cluster1-init-sql
    ...
    ```
    
    Now, SQL commands will be executed when you create the cluster by apply the manifest:
    
    ``` {.bash data-prompt="$" }
    $ kubectl apply -f deploy/cr.yaml
    ```

The psql command is executed the standard input and the file flag (`psql -f -`). If the command returns `0` exit code, SQL will not be run again. When psql returns with an error exit code, the Operator will continue attempting to execute it as part of its reconcile loop until success. You can fix errors in the SQL sequence, for example by interactive `kubectl edit configmap cluster1-init-sql -n postgres-namespace` command.

!!! note

    You can use following psql meta-command to make sure that any SQL errors would make psql to return the error code:
    
    ```sql
    \set ON_ERROR_STOP
    \echo Any error will lead to exit code 3
    ```
    
