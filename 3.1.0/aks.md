> For the complete documentation index, see [llms.txt](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/llms.txt).

# Install Install Percona Distribution for PostgreSQL on Azure Kubernetes Service (AKS)

This guide shows you how to deploy Percona Operator for PostgreSQL on Microsoft Azure Kubernetes Service (AKS). The document assumes some experience with the platform. For more information on the AKS, see the [Microsoft AKS official documentation](https://azure.microsoft.com/en-us/services/kubernetes-service/) .

## Prerequisites

The following tools are used in this guide and therefore should be preinstalled:

1. **Azure Command Line Interface (Azure CLI)** for interacting with the different parts of AKS. You can install it following the [official installation instructions for your system](https://docs.microsoft.com/en-us/cli/azure/install-azure-cli) .
1. **kubectl** to manage and deploy applications on Kubernetes. Install it [following the official installation instructions](https://kubernetes.io/docs/tasks/tools/install-kubectl/) .

Also, you need to sign in with Azure CLI using your credentials according to the [official guide](https://docs.microsoft.com/en-us/cli/azure/authenticate-azure-cli) .

## Create and configure the AKS cluster

To create your Kubernetes cluster, you will need the following data:

- name of your AKS cluster,
- an [Azure resource group](https://docs.microsoft.com/en-us/azure/azure-resource-manager/management/overview) , in which resources of your cluster will be deployed and managed.
- the amount of nodes you would like tho have.

You can create your cluster via command line using `az aks create` command. The following command will create a 3-node cluster named `cluster1` within some [already existing](https://docs.microsoft.com/en-us/azure/aks/learn/quick-kubernetes-deploy-cli#create-a-resource-group) resource group named `my-resource-group`:

```
az aks create --resource-group my-resource-group --name  cluster1 --enable-managed-identity --node-count 3 --node-vm-size Standard_B4ms --node-osdisk-size 30 --network-plugin kubenet  --generate-ssh-keys --outbound-type loadbalancer
```

Other parameters in the above example specify that we are creating a cluster with machine type of [Standard_B4ms](https://azureprice.net/vm/Standard_B4ms) and OS disk size reduced to 30 GiB. You can see detailed information about cluster creation options in the [AKS official documentation](https://docs.microsoft.com/en-us/cli/azure/aks?view=azure-cli-latest) .

You may wait a few minutes for the cluster to be generated.

Now you should configure the command-line access to your newly created cluster to make `kubectl` be able to use it.

```
az aks get-credentials --resource-group my-resource-group --name  cluster1
```

## Install the Operator and deploy your PostgreSQL cluster

1. Create the Kubernetes namespace for your cluster. It is a good practice to isolate workloads in Kubernetes by installing the Operator in a custom namespace. For example, let’s name it `postgres-operator`:

   ```
   kubectl create namespace postgres-operator
   ```

   Expected output

   ```
   namespace/postgres-operator was created
   ```

   We will use this namespace further on in this document. If you used another name, make sure to replace it in the following commands.

1. Deploy the Operator[using](https://kubernetes.io/docs/reference/using-api/server-side-apply/) the following command:

   ```
   kubectl apply --server-side -f https://raw.githubusercontent.com/percona/percona-postgresql-operator/v3.1.0/deploy/bundle.yaml -n postgres-operator
   ```

   Expected output

   ```
   customresourcedefinition.apiextensions.k8s.io/perconapgbackups.pgv2.percona.com serverside-applied
   customresourcedefinition.apiextensions.k8s.io/perconapgclusters.pgv2.percona.com serverside-applied
   customresourcedefinition.apiextensions.k8s.io/perconapgrestores.pgv2.percona.com serverside-applied
   customresourcedefinition.apiextensions.k8s.io/postgresclusters.postgres-operator.crunchydata.com serverside-applied
   serviceaccount/percona-postgresql-operator serverside-applied
   role.rbac.authorization.k8s.io/percona-postgresql-operator serverside-applied
   rolebinding.rbac.authorization.k8s.io/service-account-percona-postgresql-operator serverside-applied
   deployment.apps/percona-postgresql-operator serverside-applied
   ```

   At this point, the Operator Pod is up and running.

1. The operator has been started, and you can deploy Percona Distribution for PostgreSQL:

   ```
   kubectl apply -f https://raw.githubusercontent.com/percona/percona-postgresql-operator/v3.1.0/deploy/cr.yaml -n postgres-operator
   ```

   Expected output

   ```
   perconapgcluster.pgv2.percona.com/cluster1 created
   ```

   Note

   This deploys default Percona Distribution for PostgreSQL configuration. Please see [deploy/cr.yaml](https://raw.githubusercontent.com/percona/percona-postgresql-operator/v3.1.0/deploy/cr.yaml) and [Custom Resource Options](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/operator.html) for the configuration options. You can clone the repository with all manifests and source code by executing the following command:

   ```
   git clone -b v3.1.0 https://github.com/percona/percona-postgresql-operator
   ```

   After editing the needed options, apply your modified `deploy/cr.yaml` file as follows:

   ```
   kubectl apply -f deploy/cr.yaml -n postgres-operator
   ```

   The creation process may take some time. When the process is over your cluster will obtain the `ready` status. You can check it with the following command:

   ```
   kubectl get pg
   ```

   Expected output

   ```
   NAME       ENDPOINT                         STATUS   POSTGRES   PGBOUNCER   AGE
   cluster1   cluster1-pgbouncer.default.svc   ready    3          3           30m
   ```

## Verifying the cluster operation

It may take ten minutes to get the cluster started. When `kubectl get pg` command finally shows you the cluster status as `ready`, you can try to connect to the cluster.

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

## Removing the AKS cluster

To delete your cluster, you will need the following data:

- name of your AKS cluster,
- AWS region in which you have deployed your cluster.

You can clean up the cluster with the `az aks delete` command as follows (with real names instead of `<resource group>` and `<cluster name>` placeholders):

```
az aks delete --name <cluster name> --resource-group <resource group> --yes --no-wait
```

It may take ten minutes to get the cluster actually deleted after executing this command.

Warning

After deleting the cluster, all data stored in it will be lost!
