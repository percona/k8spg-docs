# Connect to the PostgreSQL cluster

The [`pg_bouncer`](http://pgbouncer.github.io/) component of Percona Distribution for PostgreSQL provides the point of entry to the PostgreSQL cluster. We will use the `pg_bouncer` URI to connect to PostgreSQL. 

The `pg_bouncer` URI is stored in the [Secret](https://kubernetes.io/docs/concepts/configuration/secret/) object, which the Operator generates during the installation.

To connect to PostgreSQL, do the following:
{.power-number}

1. List the Secrets objects

    ```{.bash data-prompt="$"}
    $ kubectl get secrets -n <namespace>
    ```

    The Secrets object you are interested in is named as
    `<cluster_name>-pguser-<cluster_name>`. The `<cluster_name>` value is
    the [name of your Percona Distribution for PostgreSQL Cluster](operator.md#metadata-name). The default variant is `cluster1-pguser-cluster1`.

2. Retrieve the pg_bouncer URI of your secret

    ``` {.bash data-prompt="$" }
    $  kubectl get secret cluster1-pguser-cluster1 -n <namespace> -o yaml
    ```

3. Decode the base64-encoded `pgbouncer-uri` string from the secret

    ``` {.bash data-prompt="$" }
    $ echo -n <base64-pgbouncer-uri-string> | base64 --decode
    ```

    The format of the decoded URI is the following:

    ```{.bash .no-copy}
    postgresql://<user>:<password>@<cluster-name>-pgbouncer.<namespace>.svc:5432/<db>
    ```

4. Create a Pod and start a container with Percona Distribution for PostgreSQL. The following command does it, naming the Pod `pg-client`:

    ``` {.bash data-prompt="$" data-prompt-second="[postgres@pg-client /]$"}
    $ kubectl run -i --rm --tty pg-client --image=perconalab/percona-distribution-postgresql:{{ postgresrecommended }} --restart=Never -- bash -il
    ```

    It may take some time to execute the command. As the result you should see the following command prompt `[postgres@pg-client /]` (`pg-client` here is the name of the Pod)

5. Connect to `psql` by passing the retrieved `pgbouncer-uri`. The following command connects you as a `cluster1` user to a `cluster1` database
    via the PostgreSQL interactive terminal. 

    ``` {.bash data-prompt="$" data-prompt-second="[postgres@pg-client /]$"}
    [postgres@pg-client /]$ psql postgresql://cluster1:<password>@cluster1-pgbouncer.<namespace>.svc:5432/cluster1
    ```

    The output resembles the following:

    ``` {.text .no-copy}
    psql ({{ postgresrecommended }})
    SSL connection (protocol: TLSv1.3, cipher: TLS_AES_256_GCM_SHA384, bits: 256, compression: off)
    Type "help" for help.
    pgdb=>
    ```

Congratulations! You have connected to your PostgreSQL cluster.

## Next steps

[Insert testing data :material-arrow-right:](data-insert.md){.md-button}. 
