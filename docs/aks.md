# Install Install Percona Distribution for PostgreSQL on Azure Kubernetes Service (AKS)

This guide shows you how to deploy Percona Operator for PostgreSQL on Microsoft 
Azure Kubernetes Service (AKS). The document assumes some experience with the
platform. For more information on the AKS, see the [Microsoft AKS official documentation :octicons-link-external-16:](https://azure.microsoft.com/en-us/services/kubernetes-service/).

## Prerequisites

The following tools are used in this guide and therefore should be preinstalled:

1. **Azure Command Line Interface (Azure CLI)** for interacting with the different
    parts of AKS. You can install it following the [official installation instructions for your system :octicons-link-external-16:](https://docs.microsoft.com/en-us/cli/azure/install-azure-cli).

2. **kubectl**  to manage and deploy applications on Kubernetes. Install
    it [following the official installation instructions :octicons-link-external-16:](https://kubernetes.io/docs/tasks/tools/install-kubectl/).

Also, you need to sign in with Azure CLI using your credentials according to the
[official guide :octicons-link-external-16:](https://docs.microsoft.com/en-us/cli/azure/authenticate-azure-cli).

## Create and configure the AKS cluster

To create your Kubernetes cluster, you will need the following data:

* name of your AKS cluster,
* an [Azure resource group :octicons-link-external-16:](https://docs.microsoft.com/en-us/azure/azure-resource-manager/management/overview), in which resources of your cluster will be deployed and managed.
* the amount of nodes you would like tho have.

You can create your cluster via command line using `az aks create` command.
The following command will create a 3-node cluster named ` cluster1` within some [already existing :octicons-link-external-16:](https://docs.microsoft.com/en-us/azure/aks/learn/quick-kubernetes-deploy-cli#create-a-resource-group) resource group named `my-resource-group`:

``` {.bash data-prompt="$" }
$ az aks create --resource-group my-resource-group --name  cluster1 --enable-managed-identity --node-count 3 --node-vm-size Standard_B4ms --node-osdisk-size 30 --network-plugin kubenet  --generate-ssh-keys --outbound-type loadbalancer
```

Other parameters in the above example specify that we are creating a cluster
with machine type of [Standard_B4ms :octicons-link-external-16:](https://azureprice.net/vm/Standard_B4ms)
and OS disk size reduced to 30 GiB. You can see detailed information about
cluster creation options in the [AKS official documentation :octicons-link-external-16:](https://docs.microsoft.com/en-us/cli/azure/aks?view=azure-cli-latest).

You may wait a few minutes for the cluster to be generated.

Now you should configure the command-line access to your newly created cluster
to make `kubectl` be able to use it.

``` {.bash data-prompt="$" } 
az aks get-credentials --resource-group my-resource-group --name  cluster1
```

## Install the Operator and deploy your PostgreSQL cluster

1. Create the Kubernetes namespace for your cluster. It is a good practice to isolate workloads in Kubernetes by installing the Operator in a custom namespace. For example, let's name it `postgres-operator`:

    ``` {.bash data-prompt="$" }
    $ kubectl create namespace postgres-operator
    ```

    ??? example "Expected output"

        ``` {.text .no-copy}
        namespace/postgres-operator was created
        ```

    We will use this namespace further on in this document. If you used another name, make sure to replace it in the following commands. 

2. Deploy the Operator[using :octicons-link-external-16:](https://kubernetes.io/docs/reference/using-api/server-side-apply/) the following command:

    ``` {.bash data-prompt="$" }
    $ kubectl apply --server-side -f https://raw.githubusercontent.com/percona/percona-postgresql-operator/v{{ release }}/deploy/bundle.yaml -n postgres-operator
    ```

    ??? example "Expected output"

        ```{.text .no-copy}
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

3. The operator has been started, and you can deploy Percona Distribution for PostgreSQL:

    ``` {.bash data-prompt="$" }
    $ kubectl apply -f https://raw.githubusercontent.com/percona/percona-postgresql-operator/v{{ release }}/deploy/cr.yaml -n postgres-operator
    ```

    ??? example "Expected output"

        ``` {.text .no-copy}
        perconapgcluster.pgv2.percona.com/cluster1 created
        ```

    !!! note

        This deploys default Percona Distribution for PostgreSQL configuration.
        Please see [deploy/cr.yaml :octicons-link-external-16:](https://raw.githubusercontent.com/percona/percona-postgresql-operator/v{{ release }}/deploy/cr.yaml)
        and [Custom Resource Options](operator.md) for the configuration
        options. You can clone the repository with all manifests and source code
        by executing the following command:

        ```{.bash data-prompt="$" }
        $ git clone -b v{{ release }} https://github.com/percona/percona-postgresql-operator
        ```

        After editing the needed options, apply your modified `deploy/cr.yaml`
        file as follows:

        ```{.bash data-prompt="$" }
        $ kubectl apply -f deploy/cr.yaml -n postgres-operator
        ```

    The creation process may take some time. When the process is over your
    cluster will obtain the `ready` status. You can check it with the following
    command:

    ``` {.bash data-prompt="$" }
    $ kubectl get pg
    ```

    ??? example "Expected output"

        --8<-- "kubectl-get-pg-response.txt"

## Verifying the cluster operation

It may take ten minutes to get the cluster started. When `kubectl get pg`
command finally shows you the cluster status as `ready`, you can try to connect
to the cluster.

{% include 'assets/fragments/connectivity.txt' %}

## Removing the AKS cluster

To delete your cluster, you will need the following data:

* name of your AKS cluster,
* AWS region in which you have deployed your cluster.

You can clean up the cluster with the `az aks delete` command as follows (with
real names instead of `<resource group>` and `<cluster name>` placeholders):

``` {.bash data-prompt="$" }
$ az aks delete --name <cluster name> --resource-group <resource group> --yes --no-wait
```

It may take ten minutes to get the cluster actually deleted after executing this command.

!!! warning

    After deleting the cluster, all data stored in it will be lost!

