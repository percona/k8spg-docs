> For the complete documentation index, see [llms.txt](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/llms.txt).

# Percona Operator for PostgreSQL single-namespace and multi-namespace deployment

There are two design patterns that you can choose from when deploying Percona Operator for PostgreSQL and PostgreSQL clusters in Kubernetes:

- Namespace-scope - one Operator per Kubernetes namespace,
- Cluster-wide - one Operator can manage clusters in multiple namespaces.

This how-to explains how to configure Percona Operator for PostgreSQL for each scenario.

## Namespace-scope

By default, Percona Operator for PostgreSQL functions in a specific Kubernetes namespace. You can create one during the installation (like it is shown in the [installation instructions](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/kubernetes.html)) or just use the default namespace. This approach allows several Operators to co-exist in one Kubernetes-based environment, being separated in different namespaces:

Normally this is a recommended approach, as isolation minimizes impact in case of various failure scenarios. This is the default configuration of our Operator.

Let’s say you will use a Kubernetes Namespace called `percona-db-1`.

1. Clone `percona-postgresql-operator` repository:

   ```
   git clone -b v3.1.0 https://github.com/percona/percona-postgresql-operator
   cd percona-postgresql-operator
   ```

1. Create your `percona-db-1` Namespace (if it doesn’t yet exist) as follows:

   ```
   kubectl create namespace percona-db-1
   ```

1. Deploy the Operator [using](https://kubernetes.io/docs/reference/using-api/server-side-apply/) the following command:

   ```
   kubectl apply --server-side -f deploy/bundle.yaml -n percona-db-1
   ```

1. Once Operator is up and running, deploy the database cluster itself:

   ```
   kubectl apply -f deploy/cr.yaml -n percona-db-1
   ```

You can deploy multiple clusters in this namespace.

### Add more namespaces

What if there is a need to deploy clusters in another namespace? The solution for namespace-scope deployment is to have more than one Operator. We will use the `percona-db-2` namespace as an example.

1. Create your `percona-db-2` namespace (if it doesn’t yet exist) as follows:

   ```
   kubectl create namespace percona-db-2
   ```

1. Deploy the Operator:

   ```
   kubectl apply --server-side -f deploy/bundle.yaml -n percona-db-2
   ```

1. Once Operator is up and running deploy the database cluster itself:

   ```
   kubectl apply -f deploy/cr.yaml -n percona-db-2
   ```

   Note

   Cluster names may be the same in different namespaces.

## Install the Operator cluster-wide

Sometimes it is more convenient to have one Operator watching for Percona Distribution for PostgreSQL custom resources in several namespaces.

We recommend running Percona Operator for PostgreSQL in a traditional way, limited to a specific namespace, to limit the blast radius. But it is possible to run it in so-called *cluster-wide* mode, one Operator watching several namespaces, if needed:

To use the Operator in a cluster-wide mode, you should install it with a different set of configuration YAML files, which are available in the deploy folder and have filenames with a special `cw-` prefix: e.g. `deploy/cw-bundle.yaml`.

While using this cluster-wide versions of configuration files, you should set the following information there:

- `subjects.namespace` option should contain the namespace which will host the Operator,

- The [`WATCH_NAMESPACE`](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/env-var-operator.html#watch_namespace) environment variable determines which namespaces the Operator will monitor for custom resources. By default, it is defined by the `metadata.namespace` option via a downward API `fieldRef` and points to the Operator’s own namespace.

  Configure the `WATCH_NAMESPACE` environment variable in the Operator Deployment’s `env` section and choose the option that matches your desired Operator scope:

  - **Comma-separated list of namespaces**: Specify the comma-separated list of namespaces, including the namespace where the Operator itself is running (e.g., `"pg-operator,percona-db-1"`). The Operator will watch only the specified namespaces.
  - **Empty string (`""`)**: Set the `value` to an empty string. The Operator watches **all namespaces** in the cluster.

  For the full list of Operator environment variables, see [Define Operator environment variables](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/env-var-operator.html).

Note

Installing the Operator cluster-wide on OpenShift via the the Operator Lifecycle Manager (OLM) requires [making different selections in the OLM web-based UI](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/openshift.html#install-via-the-operator-lifecycle-manager-olm) instead of patching YAML files.

The following simple example shows how to install Operator cluster-wide on Kubernetes.

1. Clone `percona-postgresql-operator` repository:

   ```
   git clone -b v3.1.0 https://github.com/percona/percona-postgresql-operator
   cd percona-postgresql-operator
   ```

1. Let’s say you will use `pg-operator` namespace for the Operator, and `percona-db-1` namespace for the cluster. Create these namespaces, if needed:

   ```
   kubectl create namespace pg-operator
   kubectl create namespace percona-db-1
   ```

1. Edit the `deploy/cw-bundle.yaml` configuration file to make sure it contains proper namespace name for the Operator:

   ```
   ...
   subjects:
   - kind: ServiceAccount
     name: percona-postgresql-operator
     namespace: pg-operator
   ...
   spec:
     containers:
     - env:
       - name: WATCH_NAMESPACE
         value: "pg-operator,percona-db-1"
   ...
   ```

1. Apply the `deploy/cw-bundle.yaml` file with the following command:

   ```
   kubectl apply --server-side -f deploy/cw-bundle.yaml -n pg-operator
   ```

   With this configuration, the Operator monitors only the specified namespaces.

1. Deploy the cluster in the namespace of your choice:

   ```
   kubectl apply -f deploy/cr.yaml -n percona-db-1
   ```

## Verifying the cluster operation

When creation process is over, connect to the cluster to verify it is operational.

When the Operator deploys a database cluster, it generates several [Secrets](https://kubernetes.io/docs/concepts/configuration/secret/) . Among them there is the Secret with the credentials of the default PostgreSQL user. This default user has the same username as the cluster name.

1. Use `kubectl get secrets -n <namespace>` command to see the list of Secrets objects. The Secrets object you are interested in is named in the format `<cluster_name>-pguser-<cluster_name>` (where the `<cluster_name>` is the [name of your Percona Distribution for PostgreSQL Cluster](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/operator.html#metadata-name)). For example, if your cluster name is `cluster1`, the Secret name will be `cluster1-pguser-cluster1`.

1. Use the following command to get the password of this user. Replace the `<cluster_name>` and `<namespace>` placeholders with your values:

   ```
   kubectl get secret <cluster_name>-<user_name>-<cluster_name> -n <namespace> --template='{{.data.password | base64decode}}{{"\n"}}'
   ```

1. To connect to PostgreSQL, you will use the `pgbouncer` service as the entry point to your cluster. To find this service, use the following command:

   ```
   kubectl get svc -n <namespace>
   ```

   Look for the service named `<cluster-name>-pgbouncer`.

   Sample output

   ```
   cluster1-ha          ClusterIP   34.118.234.155   <none>        5432/TCP   51m
   cluster1-ha-config   ClusterIP   None             <none>        <none>     51m
   cluster1-pgbouncer   ClusterIP   34.118.239.5     <none>        5432/TCP   51m
   cluster1-pods        ClusterIP   None             <none>        <none>     51m
   cluster1-primary     ClusterIP   None             <none>        5432/TCP   51m
   cluster1-replicas    ClusterIP   34.118.234.19    <none>        5432/TCP   51m
   ```

1. Create a pod and start Percona Distribution for PostgreSQL inside. The following command will do this, naming the new Pod `pg-client`:

   ```
   kubectl run -n <namespace> -i --rm --tty pg-client --image=percona/percona-distribution-postgresql:18.6.1-3 --restart=Never -- bash -il
   ```

   It may require some time to execute the command and deploy the corresponding Pod.

1. Run a container with `psql` tool and connect its console output to your terminal. Substitute the `<namespace>` placeholder with your value in the following command to connect as a `cluster1` user to the `cluster1` database via the PostgreSQL interactive terminal.

   ```
   [postgres@pg-client /]$ PGPASSWORD='pguser_password' psql -h cluster1-pgbouncer.<namespace>.svc.cluster.local -p 5432 -U cluster1 cluster1
   ```

   Sample output

   ```
   psql (18.6.1-3)
   SSL connection (protocol: TLSv1.3, cipher: TLS_AES_256_GCM_SHA384, bits: 256, compression: off)
   Type "help" for help.
   pgdb=>
   ```
