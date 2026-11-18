> For the complete documentation index, see [llms.txt](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/llms.txt).

# Install Percona Distribution for PostgreSQL on Minikube

Installing the Percona Operator for PostgreSQL on [Minikube](https://github.com/kubernetes/minikube) is the easiest way to try it locally without a cloud provider.

Minikube runs Kubernetes on GNU/Linux, Windows, or macOS system using a system-wide hypervisor, such as VirtualBox, KVM/QEMU, VMware Fusion or Hyper-V. Using it is a popular way to test Kubernetes application locally prior to deploying it on a cloud.

This document describes how to deploy the Operator and Percona Distribution for PostgreSQL on Minikube.

## Set up Minikube

1. [Install Minikube](https://kubernetes.io/docs/tasks/tools/install-minikube/) , using a way recommended for your system. This includes the installation of the following three components:

   1. kubectl tool,
   1. a hypervisor, if it is not already installed,
   1. actual minikube package

1. After the installation, initialize and start the Kubernetes cluster. The parameters we pass for the following command increase the virtual machine limits for the CPU cores, memory, and disk, to ensure stable work of the Operator:

   ```
   minikube start --memory=5120 --cpus=4 --disk-size=30g
   ```

   This command downloads needed virtualized images, then initializes and runs the cluster.

1. After Minikube is successfully started, you can optionally run the Kubernetes dashboard, which visually represents the state of your cluster. Executing `minikube dashboard` starts the dashboard and opens it in your default web browser.

## Deploy the Percona Operator for PostgreSQL

1. Create the Kubernetes namespace for your cluster. It is a good practice to isolate workloads in Kubernetes by installing the Operator in a custom namespace. For example, let’s name it `postgres-operator`:

   ```
   kubectl create namespace postgres-operator
   ```

   Expected output

   ```
   namespace/postgres-operator was created
   ```

   We will use this namespace further on in this document. If you used another name, make sure to replace it in the following commands.

1. Deploy the Operator [using](https://kubernetes.io/docs/reference/using-api/server-side-apply/) the following command:

   ```
   kubectl apply --server-side -f https://raw.githubusercontent.com/percona/percona-postgresql-operator/v3.1.0/deploy/bundle.yaml -n postgres-operator
   ```

   Expected output

   ```
   customresourcedefinition.apiextensions.k8s.io/crunchybridgeclusters.postgres-operator.crunchydata.com serverside-applied
   customresourcedefinition.apiextensions.k8s.io/perconapgbackups.pgv2.percona.com serverside-applied
   customresourcedefinition.apiextensions.k8s.io/perconapgclusters.pgv2.percona.com serverside-applied
   customresourcedefinition.apiextensions.k8s.io/perconapgrestores.pgv2.percona.com serverside-applied
   customresourcedefinition.apiextensions.k8s.io/perconapgupgrades.pgv2.percona.com serverside-applied
   customresourcedefinition.apiextensions.k8s.io/pgadmins.postgres-operator.crunchydata.com serverside-applied
   customresourcedefinition.apiextensions.k8s.io/pgupgrades.postgres-operator.crunchydata.com serverside-applied
   customresourcedefinition.apiextensions.k8s.io/postgresclusters.postgres-operator.crunchydata.com serverside-applied
   serviceaccount/percona-postgresql-operator serverside-applied
   role.rbac.authorization.k8s.io/percona-postgresql-operator serverside-applied
   rolebinding.rbac.authorization.k8s.io/service-account-percona-postgresql-operator serverside-applied
   deployment.apps/percona-postgresql-operator serverside-applied
   ```

   As the result you have the Operator Pod up and running.

1. Deploy Percona Distribution for PostgreSQL:

   ```
   kubectl apply -f https://raw.githubusercontent.com/percona/percona-postgresql-operator/v3.1.0/deploy/cr.yaml -n postgres-operator
   ```

   Expected output

   ```
   perconapgcluster.pgv2.percona.com/cluster1 created
   ```

   Note

   This deploys the default Percona Distribution for PostgreSQL configuration. Please see [deploy/cr.yaml](https://raw.githubusercontent.com/percona/percona-postgresql-operator/v3.1.0/deploy/cr.yaml) and [Custom Resource Options](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/operator.html) for the configuration options. You can clone the repository with all manifests and source code by executing the following command:

   ```
   git clone -b v3.1.0 https://github.com/percona/percona-postgresql-operator
   ```

   After editing the needed options, apply your modified `deploy/cr.yaml` file as follows:

   ```
   kubectl apply -f deploy/cr.yaml  -n postgres-operator
   ```

1. The creation process may take some time. When the process is over your cluster will obtain the `ready` status. You can check it with the following command:

   ```
   kubectl get pg -n postgres-operator
   ```

   Expected output

   ```
   NAME       ENDPOINT                         STATUS   POSTGRES   PGBOUNCER   AGE
   cluster1   cluster1-pgbouncer.default.svc   ready    3          3           30m
   ```

## Verify the Percona Distribution for PostgreSQL cluster operation

When creation process is over, the output of the `kubectl get pg` command shows the cluster status as `ready`. You can try to connect to the cluster.

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

## Delete the cluster

If you need to delete the Operator and PostgreSQL cluster (for example, to clean up the testing deployment before adopting it for production use), check [this HowTo](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/delete.html).

If you no longer need the Kubernetes cluster in Minikube, the following are the steps to remove it.

1. Stop the Minikube cluster:

   ```
   minikube stop
   ```

1. Delete the cluster

   ```
   minikube delete
   ```

   This command deletes the virtual machines, and removes all associated files.
