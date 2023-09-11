# Connect to the PostgreSQL cluster

In this tutorial, we will connect to the cluster you have created previously. 

The [`pgBouncer`](http://pgbouncer.github.io/) component of Percona Distribution for PostgreSQL provides the point of entry to the PostgreSQL cluster. We will use the `pgBouncer` URI to connect. 

The `pgBouncer` URI is stored in the [Secret](https://kubernetes.io/docs/concepts/configuration/secret/) object, which the Operator generates during the installation.

To connect to PostgreSQL, do the following:
{.power-number}

1. List the Secrets objects

    ```{.bash data-prompt="$"}
    $ kubectl get secrets -n <namespace>
    ```

    The Secrets object we target is named as
    `<cluster_name>-pguser-<cluster_name>`. The `<cluster_name>` value is
    the [name of your Percona Distribution for PostgreSQL Cluster](operator.md#metadata-name). The default variant is `cluster1-pguser-cluster1`.

2. Retrieve the pgBouncer URI of your secret

    ``` {.bash data-prompt="$" }
    $  kubectl get secret cluster1-pguser-cluster1 -n <namespace> -o yaml
    ```

3. Decode the base64-encoded `pgBouncer` URI string from the secret

    ``` {.bash data-prompt="$" }
    $ PGBOUNCER_URI=`echo -n <base64-pgbouncer-uri-string> | base64 --decode`
    ```

    The format of the decoded URI is the following:

    ```{.text .no-copy}
    postgresql://<user>:<password>@<cluster-name>-pgbouncer.<namespace>.svc:5432/<db>
    ```

4. Create a Pod where you start a container with Percona Distribution for PostgreSQL and connect to the database. The following command does it, naming the Pod `pg-client` and connects you to the `cluster1` database:

    ``` {.bash data-prompt="$"}
    $ kubectl run -i --rm --tty pg-client --image=perconalab/percona-distribution-postgresql:15 --restart=Never -- psql $PGBOUNCER_URI
    ```

    It may take some time to create the Pod and connect to the database. As the result, you should see the following sample output: 

    ??? example "Expected output"

        ``` {.text .no-copy}
        psql ({{ postgresrecommended }})
        SSL connection (protocol: TLSv1.3, cipher: TLS_AES_256_GCM_SHA384, bits: 256, compression: off)
        Type "help" for help.
        cluster1=>
        ```

Congratulations! You have connected to your PostgreSQL cluster.

## Next steps

[Insert testing data :material-arrow-right:](data-insert.md){.md-button}
