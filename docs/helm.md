# Install Percona Distribution for PostgreSQL using Helm

[Helm :octicons-link-external-16:](https://github.com/helm/helm) is the package manager for Kubernetes. 
A Helm [chart :octicons-link-external-16:](https://helm.sh/docs/topics/charts/) is a package that contains all the necessary resources to deploy an application to a Kubernetes cluster.

You can find Percona Helm charts in [percona/percona-helm-charts :octicons-link-external-16:](https://github.com/percona/percona-helm-charts) repository in Github.

## Prerequisites

To install and deploy the Operator, you need the following:

1. [Helm v3 :octicons-link-external-16:](https://docs.helm.sh/using_helm/#installing-helm).
2. [kubectl :octicons-link-external-16:](https://kubernetes.io/docs/tasks/tools/) command line utility.
3. A Kubernetes environment. You can deploy it locally on [Minikube :octicons-link-external-16:](https://github.com/kubernetes/minikube) for testing purposes or using any cloud provider of your choice. Check the list of our [officially supported platforms](System-Requirements.md#officially-supported-platforms).

    !!! note "See also"

        * [Set up Minikube](minikube.md#set-up-minikube)
        * [Create and configure the GKE cluster](gke.md#create-and-configure-the-gke-cluster)
        * [Set up Amazon Elastic Kubernetes Service](eks.md#software-installation)

## Installation 

Here's a sequence of steps to follow:
{.power-number}

1. Add the Percona’s Helm charts repository and make your Helm client up to
    date with it:

    ``` {.bash data-prompt="$" }
    $ helm repo add percona https://percona.github.io/percona-helm-charts/
    $ helm repo update
    ```

2. It is a good practice to isolate workloads in Kubernetes via namespaces. Create a namespace:

    ```{.bash data-prompt="$" }
    $ kubectl create namespace <my-namespace>
    ```

3. Install the Percona Operator for PostgreSQL:

    ``` {.bash data-prompt="$" }
    $ helm install my-operator percona/pg-operator --namespace <my-namespace> 
    ```

    The `my-namespace` is the name of your namespace. The `my-operator` parameter is the name of [a new release object :octicons-link-external-16:](https://helm.sh/docs/intro/using_helm/#three-big-concepts)
    which is created for the Operator when you install its Helm chart (use any
    name you like).

3. Install Percona Distribution for PostgreSQL:

    ```{.bash data-prompt="$" }
    $ helm install cluster1 percona/pg-db -n <my-namespace>
    ```

    The `cluster1` parameter is the name of [a new release object :octicons-link-external-16:](https://helm.sh/docs/intro/using_helm/#three-big-concepts)
    which is created for the Percona Distribution for PostgreSQL when you install
    its Helm chart (use any name you like).

4. Check the Operator and replica set Pods status. 
   
    ``` {.bash data-prompt="$" }
    $ kubectl get pg -n <my-namespace>
    ```

    The creation process is over when both the
    Operator and replica set Pods report the `ready` status:

    ??? example "Expected output"

        ```{.text .no-copy}

        NAME       ENDPOINT                                   STATUS   POSTGRES   PGBOUNCER   AGE
        cluster1   cluster1-pgbouncer.postgres-operator.svc   ready    3          3           143m
        ``` 

You have successfully installed and deployed the Operator with default parameters. You can check them in the [Custom Resource options reference](operator.md#operator-custom-resource-options).

## Next steps

[Connect to PostgreSQL :material-arrow-right:](connect.md){.md-button}
