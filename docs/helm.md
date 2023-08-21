# Install Percona Distribution for PostgreSQL using Helm

[Helm](https://github.com/helm/helm) is the package manager for Kubernetes. 
A Helm [chart](https://helm.sh/docs/topics/charts/) is a package that contains all the necessary resources to deploy an application to a Kubernetes cluster.

You can find Percona Helm charts in [percona/percona-helm-charts](https://github.com/percona/percona-helm-charts) repository in Github.

## Pre-requisites

To install and deploy the Operator, you need the following:

1. Helm v3 up and running. Install Helm following its [official installation instructions](https://docs.helm.sh/using_helm/#installing-helm).
2. [kubectl](https://kubernetes.io/docs/tasks/tools/) command line utility.
3. A Kubernetes environment. You can deploy it locally on [Minikube](https://github.com/kubernetes/minikube) for testing purposes or using any cloud provider of your choice. Check the list of our [officially supported platforms](System-Requirements.md#officially-supported-platforms).

    !!! note "See also"

        * [Set up Minikube](minikube.md#set-up-minikube)
        * [Create and configure the GKE cluster](gke.md#create-and-configure-the-gke-cluster)
        * [Set up Amazon Elastic Kubernetes Service](eks.md#software-installation)

## Installation

1. Add the Percona’s Helm charts repository and make your Helm client up to
    date with it:

    ``` {.bash data-prompt="$" }
    $ helm repo add percona https://percona.github.io/percona-helm-charts/
    $ helm repo update
    ```

2. It is a good practice though to isolate workloads in Kubernetes via namespaces. Create a namespace:

    ```{.bash data-prompt="$" }
    $ kubectl create namespace <my-namespace>
    ```

3. Install the Percona Operator for PostgreSQL:

    ``` {.bash data-prompt="$" }
    $ helm install my-operator percona/pg-operator --namespace my-namespace 
    ```

    The `my-namespace` is the name of your namespace. The `my-operator` parameter is the name of [a new release object](https://helm.sh/docs/intro/using_helm/#three-big-concepts)
    which is created for the Operator when you install its Helm chart (use any
    name you like).

3. Install Percona Distribution for PostgreSQL:

    ```{.bash data-prompt="$" }
    $ helm install my-db percona/pg-db
    ```

    The `my-db` parameter is the name of [a new release object](https://helm.sh/docs/intro/using_helm/#three-big-concepts)
    which is created for the Percona Distribution for PostgreSQL when you install
    its Helm chart (use any name you like).

You have successfully deployed the Operator with the [default parameters](operator.md#operator-custom-resource-options). 


## Next steps

[Connect to PostgreSQL](connect.md){.md-button}
