# 3. Connect to the PostgreSQL cluster

When the [installation](kubectl.md) is done, we can connect to the cluster. 

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
    the [name of your Percona Distribution for PostgreSQL Cluster](operator.md#metadata-name). The default variant is:

    === ":simple-kubernetes: via kubectl" 

        `cluster1-pguser-cluster1`

    === ":simple-helm: via Helm"

        `cluster1-pg-db-pguser-cluster1-pg-db`

2. Retrieve the pgBouncer URI from your secret, decode and pass it as the `PGBOUNCER_URI` environment variable. Replace the `<secret>`, `<namespace>` placeholders with your Secret object and namespace accordingly:

    ``` {.bash data-prompt="$" }
    $ PGBOUNCER_URI=$(kubectl get secret <secret> --namespace <namespace> -o jsonpath='{.data.pgbouncer-uri}' | base64 --decode)
    ```

    The following example shows how to pass the pgBouncer URI from the default Secret object `cluster1-pguser-cluster1`:

    ``` {.bash data-prompt="$" }
    $ PGBOUNCER_URI=$(kubectl get secret cluster1-pguser-cluster1 --namespace <namespace> -o jsonpath='{.data.pgbouncer-uri}' | base64 --decode)
    ```

3. Create a Pod where you start a container with Percona Distribution for PostgreSQL and connect to the database. The following command does it, naming the Pod `pg-client` and connects you to the `cluster1` database:

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
