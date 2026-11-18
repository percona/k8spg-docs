> For the complete documentation index, see [llms.txt](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/llms.txt).

# Install Percona Distribution for PostgreSQL on Kubernetes

Following steps will allow you to install the Operator and use it to manage Percona Distribution for PostgreSQL in a Kubernetes-based environment.

1. First of all, clone the percona-postgresql-operator repository:

   ```
   git clone -b v3.1.0 https://github.com/percona/percona-postgresql-operator
   cd percona-postgresql-operator
   ```

   Note

   It is crucial to specify the right branch with `-b` option while cloning the code on this step. Please be careful.

1. The Custom Resource Definition for Percona Distribution for PostgreSQL should be created from the `deploy/crd.yaml` file. Custom Resource Definition extends the standard set of resources which Kubernetes “knows” about with the new items (in our case ones which are the core of the Operator). [Apply it](https://kubernetes.io/docs/reference/using-api/server-side-apply/) as follows:

   ```
   kubectl apply --server-side -f deploy/crd.yaml
   ```

   This step should be done only once; it does not need to be repeated with any other Operator deployments.

1. Create the Kubernetes namespace for your cluster if needed (for example, let’s name it `postgres-operator`):

   ```
   kubectl create namespace postgres-operator
   ```

   Note

   To use a different namespace, specify another name instead of `postgres-operator` in the above command, and modify the `-n postgres-operator` parameter with it in the following two steps. You can also omit this parameter completely to deploy everything in the `default` namespace.

1. The role-based access control (RBAC) for Percona Distribution for PostgreSQL is configured with the `deploy/rbac.yaml` file. Role-based access is based on defined roles and the available actions which correspond to each role. The role and actions are defined for Kubernetes resources in the yaml file. Further details about users and roles can be found in [Kubernetes documentation](https://kubernetes.io/docs/reference/access-authn-authz/rbac/#default-roles-and-role-bindings) .

   ```
   kubectl apply -f deploy/rbac.yaml -n postgres-operator
   ```

   Note

   Setting RBAC requires your user to have cluster-admin role privileges. For example, those using Google Kubernetes Engine can grant user needed privileges with the following command:

   ```
   $ kubectl create clusterrolebinding cluster-admin-binding --clusterrole=cluster-admin --user=$(gcloud config get-value core/account)
   ```

1. Start the Operator within Kubernetes:

   ```
   kubectl apply -f deploy/operator.yaml -n postgres-operator
   ```

   Optionally, you can add PostgreSQL Users secrets and TLS certificates to Kubernetes. If you don’t, the Operator will create the needed users and certificates automatically, when you create the database cluster. You can see documentation on [Users](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/users.html) and [TLS certificates](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/TLS.html) if still want to create them yourself.

1. After the Operator is started Percona Distribution for PostgreSQL cluster can be created at any time with the following command:

   ```
   kubectl apply -f deploy/cr.yaml -n postgres-operator
   ```

   The creation process may take some time. When the process is over your cluster will obtain the `ready` status. You can check it with the following command:

   ```
   kubectl get pg -n postgres-operator
   ```

   Expected output

   ```
   NAME       ENDPOINT                         STATUS   POSTGRES   PGBOUNCER   AGE
   cluster1   cluster1-pgbouncer.default.svc   ready    3          3           30m
   ```

## Verifying the cluster operation

When creation process is over, the output of the `kubectl get pg` command shows the cluster status as `ready`. You can now try to connect to the cluster.

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

## Deleting the cluster

If you need to delete the cluster (for example, to clean up the testing deployment before adopting it for production use), check [this HowTo](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/delete.html).
