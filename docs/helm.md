# Install Percona Distribution for PostgreSQL using Helm

[Helm](https://github.com/helm/helm) is the package manager for Kubernetes. 
A Helm [chart](https://helm.sh/docs/topics/charts/) is a package that contains all the necessary resources to deploy an application to a Kubernetes cluster.

Percona Helm charts can be found in [percona/percona-helm-charts](https://github.com/percona/percona-helm-charts) repository in Github.

## Pre-requisites

1. Helm v3 up and running. Install Helm following its [official installation instructions](https://docs.helm.sh/using_helm/#installing-helm).
2. A Kubernetes environment. You can deploy it on [Minikube](https://github.com/kubernetes/minikube) for testing purposes or on [any supported platform](System-Requirements.md#officially-supported-platforms)

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

2. Install the Percona Operator for PostgreSQL:

    ``` {.bash data-prompt="$" }
    $ helm install my-operator percona/pg-operator
    ```

    The `my-operator` parameter in the above example is the name of [a new release object](https://helm.sh/docs/intro/using_helm/#three-big-concepts)
    which is created for the Operator when you install its Helm chart (use any
    name you like).

    !!! note

        If nothing explicitly specified, `helm install` command will work
        with the `default` namespace and the latest version of the Helm
        chart. 

        * To use different namespace, provide its name with
            the following additional parameter: `--namespace my-namespace`.

        * To use different Helm chart version, provide it as follows:
            `--version {{ release }}`

3. Install PostgreSQL:

    ```{.bash data-prompt="$" }
    $ helm install my-db percona/pg-db
    ```

    The `my-db` parameter in the above example is the name of [a new release object](https://helm.sh/docs/intro/using_helm/#three-big-concepts)
    which is created for the Percona Distribution for PostgreSQL when you install
    its Helm chart (use any name you like).

## Installing Percona Distribution for PostgreSQL with customized parameters

The command above installs Percona Distribution for PostgreSQL with [default parameters](operator.md#operator-custom-resource-options).
Custom options can be passed to a `helm install` command as a
`--set key=value[,key=value]` argument. The options passed with a chart can be
any of the Operator’s [Custom Resource options](operator.md#operator-custom-resource-options).

The following example will deploy a PostgreSQL 14 based cluster
in the `my-namespace` namespace, with enabled [Percona Monitoring and Management (PMM)](https://www.percona.com/doc/percona-monitoring-and-management/2.x/index.html):

``` {.bash data-prompt="$" }
$ helm install my-db percona/pg-db --version {{ release }} --namespace my-namespace \
  --set postgresVersion=14 \
  --set pmm.enabled=true
```

## Next steps

[Connect to PostgreSQL](connect.md)
