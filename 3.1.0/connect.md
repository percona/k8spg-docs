> For the complete documentation index, see [llms.txt](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/llms.txt).

# 2 Connect to the PostgreSQL cluster

When the [installation](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/kubectl.html) is done, we can connect to the cluster.

The [`pgBouncer`](http://pgbouncer.github.io/) component of Percona Distribution for PostgreSQL provides the point of entry to the PostgreSQL cluster. We will use the `pgBouncer` URI to connect.

The `pgBouncer` URI is stored in the [Secret](https://kubernetes.io/docs/concepts/configuration/secret/) object, which the Operator generates during the installation.

To connect to PostgreSQL, do the following:

1. List the Secrets objects

   ```
   kubectl get secrets -n <namespace>
   ```

   The Secrets object we target is named as `<cluster_name>-pguser-<cluster_name>`. The `<cluster_name>` value is the [name of your Percona Distribution for PostgreSQL Cluster](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/operator.html#metadata-name). The default variant is:

   **via kubectl**

   `cluster1-pguser-cluster1`

   **via Helm**

   `cluster1-pg-db-pguser-cluster1-pg-db`

1. Retrieve the pgBouncer URI from your secret, decode and pass it as the `PGBOUNCER_URI` environment variable. Replace the `<secret>`, `<namespace>` placeholders with your Secret object and namespace accordingly:

   ```
   PGBOUNCER_URI=$(kubectl get secret <secret> --namespace <namespace> -o jsonpath='{.data.pgbouncer-uri}' | base64 --decode)
   ```

   The following example shows how to pass the pgBouncer URI from the default Secret object `cluster1-pguser-cluster1`:

   ```
   PGBOUNCER_URI=$(kubectl get secret cluster1-pguser-cluster1 --namespace <namespace> -o jsonpath='{.data.pgbouncer-uri}' | base64 --decode)
   ```

1. Create a Pod where you start a container with Percona Distribution for PostgreSQL and connect to the database. The following command does it, naming the Pod `pg-client` and connects you to the `cluster1` database:

   ```
   kubectl run -i --rm --tty pg-client --image=percona/percona-distribution-postgresql:18.6.1-3 --restart=Never -- psql $PGBOUNCER_URI
   ```

   It may take some time to create the Pod and connect to the database. As the result, you should see the following sample output:

   Expected output

   ```
   psql (18.6.1-3)
   SSL connection (protocol: TLSv1.3, cipher: TLS_AES_256_GCM_SHA384, bits: 256, compression: off)
   Type "help" for help.
   cluster1=>
   ```

Congratulations! You have connected to your PostgreSQL cluster.

## Next steps

[Insert testing data](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/data-insert.html)
