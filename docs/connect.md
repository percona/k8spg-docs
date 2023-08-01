# Connect to the PostgreSQL cluster

During the installation of Percona Distribution for PostgreSQL, the Operator creates the default PostgreSQL user that has the same login name as the name of the cluster (by default, `cluster1`). Now let's connect to PostgreSQL as this user.

1. Get the password for the PostgreSQL user. The password is stored in the [Secret](https://kubernetes.io/docs/concepts/configuration/secret/) object, which the Operator generates during the installation. 

   * List the Secrets objects

      ```{.bash data-prompt="$"}
      $ kubectl get secrets
      ```

      The Secrets object you are interested in is named as
    `<cluster_name>-pguser-<cluster_name>`. The `<cluster_name>` value is
    the [name of your Percona Distribution for PostgreSQL Cluster](operator.md#metadata-name). The default variant is `cluster1-pguser-cluster1`.

   * Retrieve the credentials of the PostgreSQL user

      ``` {.bash data-prompt="$" }
      $ kubectl get secret <cluster_name>-<user_name>-<cluster_name> --template='{{"{{"}}.data.password | base64decode{{"}}"}}{{"{{"}}"\n"{{"}}"}}'
      ```

2. Create a Pod and start a container with Percona Distribution for PostgreSQL. The following command does it, naming the Pod `pg-client`:

    ``` {.bash data-prompt="$" data-prompt-second="[postgres@pg-client /]$"}
    $ kubectl run -i --rm --tty pg-client --image=perconalab/percona-distribution-postgresql:{{ postgresrecommended }} --restart=Never -- bash -il
    ```

    It may take some time to execute the command. As the result you should see the following command prompt `[postgres@pg-client /]` (`pg-client` here is the name of the Pod)

3. Connect to `psql`. The following command connects you as a `cluster1` user to a `cluster1` database
    via the PostgreSQL interactive terminal. 

    ``` {.bash data-prompt="$" data-prompt-second="[postgres@pg-client /]$"}
    [postgres@pg-client /]$ PGPASSWORD='pguser_password' psql -h cluster1-pgbouncer.postgres-operator.svc -p 5432 -U cluster1 cluster1
    ```

    The output resembles the following:

    ``` {.text .no-copy}
    psql ({{ postgresrecommended }})
    SSL connection (protocol: TLSv1.3, cipher: TLS_AES_256_GCM_SHA384, bits: 256, compression: off)
    Type "help" for help.
    pgdb=>
    ```

## Next steps

Now you have connected to your PostgreSQL cluster. In the next step we will [insert some sample data to the database](data-insert.md). 
