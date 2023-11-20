# Install Percona Distribution for PostgreSQL using kubectl

A Kubernetes Operator is a special type of controller introduced to simplify complex deployments. The Operator extends the Kubernetes API with custom resources.

The [Percona Operator for PostgreSQL](compare.md) is based on best practices for configuration and setup of a Percona Distribution for PostgreSQL cluster in a Kubernetes-based environment on-premises or in the cloud.

We recommend installing the Operator with the [kubectl](https://kubernetes.io/docs/tasks/tools/) command line utility. It is the universal way to interact with Kubernetes. Alternatively, you can install it using the [Helm](https://github.com/helm/helm) package manager.

[:simple-kubernetes: Install with kubectl :material-arrow-down:](#prerequisites){.md-button} [:simple-helm: Install with Helm :material-arrow-right:](helm.md){.md-button}

## Prerequisites

To install Percona Distribution for PostgreSQL, you need the following:

1. The **kubectl** tool to manage and deploy applications on Kubernetes, included in most Kubernetes distributions. Install not already installed, [follow its official installation instructions](https://kubernetes.io/docs/tasks/tools/install-kubectl/).

2. A Kubernetes environment. You can deploy it on [Minikube](https://github.com/kubernetes/minikube) for testing purposes or using any cloud provider of your choice. Check the list of our [officially supported platforms](System-Requirements.md#officially-supported-platforms).

    !!! note "See also"

        * [Set up Minikube](minikube.md#set-up-minikube)
        * [Create and configure the GKE cluster](gke.md#create-and-configure-the-gke-cluster)
        * [Set up Amazon Elastic Kubernetes Service](eks.md#software-installation)

## Procedure 

Here's a sequence of steps to follow:
{.power-number}

1. Create the Kubernetes namespace for your cluster. It is a good practice to isolate workloads in Kubernetes by installing the Operator in a custom namespace. For example, let's name it `postgres-operator`:

    ``` {.bash data-prompt="$" }
    $ kubectl create namespace postgres-operator
    ```

    ??? example "Expected output"

        ``` {.text .no-copy}
        namespace/postgres-operator was created
        ```

    We will use this namespace further on in this document. If you used another name, make sure to replace it in the following commands. 

2. Deploy the Operator [using](https://kubernetes.io/docs/reference/using-api/server-side-apply/)
    the following command:

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

3. Deploy Percona Distribution
    for PostgreSQL cluster:

    ``` {.bash data-prompt="$" }
    $ kubectl apply -f https://raw.githubusercontent.com/percona/percona-postgresql-operator/v{{ release }}/deploy/cr.yaml -n postgres-operator
    ```

    ??? example "Expected output"

        ``` {.text .no-copy}
        perconapgcluster.pgv2.percona.com/cluster1 created
        ```

4. Check the Operator and replica set Pods status. 
   
    ``` {.bash data-prompt="$" }
    $ kubectl get pg -n postgres-operator
    ```

    It may take some time to create the Operator. The creation process is over when both the
    Operator and replica set Pods report the `ready` status:

    ??? example "Expected output"

        ```{.text .no-copy}

        NAME       ENDPOINT                                   STATUS   POSTGRES   PGBOUNCER   AGE
        cluster1   cluster1-pgbouncer.postgres-operator.svc   ready    3          3           143m
        ```

You have successfully installed and deployed the Operator with default parameters. You can check them in the [Custom Resource options reference](operator.md#operator-custom-resource-options). 

## Next steps

[Connect to PostgreSQL :material-arrow-right:](connect.md){.md-button}
