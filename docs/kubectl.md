# Install Percona Distribution for PostgreSQL using kubectl

The [kubectl](https://kubernetes.io/docs/tasks/tools/) command line utility is a tool used before anything else to interact with Kubernetes and containerized applications running on it. Users can run kubectl to deploy applications, manage cluster resources, check logs, etc.

## Pre-requisites

To install Percona Distribution for PostgreSQL, you need the following:

1. The **Git** distributed version control system. You can install it following the [official installation instructions](https://github.com/git-guides/install-git).

2. The **kubectl** tool to manage and deploy applications on Kubernetes, included in most Kubernetes distributions. Install it, if not present, [following the official installation instructions](https://kubernetes.io/docs/tasks/tools/install-kubectl/).

3. A Kubernetes environment. You can deploy it on [Minikube](https://github.com/kubernetes/minikube) for testing purposes or using any cloud provider of your choice. Check the list of our [officially supported platforms](System-Requirements.md#officially-supported-platforms).

    !!! note "See also"

        * [Set up Minikube](minikube.md#set-up-minikube)
        * [Create and configure the GKE cluster](gke.md#create-and-configure-the-gke-cluster)
        * [Set up Amazon Elastic Kubernetes Service](eks.md#software-installation)

## Install the Operator and Percona Distribution for PostgreSQL

To deploy the Operator and Percona Distribution for PostgreSQL in
your Kubernetes environment, do the following:

1. Create the Kubernetes namespace for your cluster. It is a good practice to isolate workloads in Kubernetes by installing the Operator in a custom namespace (for example,
   let's name it `postgres-operator`):

    ``` {.bash data-prompt="$" }
    $ kubectl create namespace postgres-operator
    ```

    ??? example "Expected output"

        ``` {.text .no-copy}
        namespace/postgres-operator was created
        ```

    !!! note

        To use different namespace, specify other name instead of
        `postgres-operator` in the above command, and modify the 
        `-n postgres-operator` parameter with it in the following two steps.
        You can also omit this parameter completely to deploy everything in the
        `default` namespace.

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

    As the result you will have the Operator Pod up and running.

3. With the Operator up and running, and you can deploy your Percona Distribution
    for PostgreSQL cluster:

    ``` {.bash data-prompt="$" }
    $ kubectl apply -f https://raw.githubusercontent.com/percona/percona-postgresql-operator/v{{ release }}/deploy/cr.yaml -n postgres-operator
    ```

    ??? example "Expected output"

        ``` {.text .no-copy}
        perconapgcluster.pgv2.percona.com/cluster1 created
        ```

4. Check the Operator and replica set Pods status. The creation process may take some time and is over when both
    Operator and replica set Pods have reached their Running status:
   
    ``` {.bash data-prompt="$" }
    $ kubectl get pg -n postgres-operator
    ```

    ??? example "Expected output"

        ```{.text .no-copy}

        NAME       ENDPOINT                                   STATUS   POSTGRES   PGBOUNCER   AGE
        cluster1   cluster1-pgbouncer.postgres-operator.svc   ready    3          3           143m
        ```

### Deploy Percona Distribution for PostgreSQL with customized parameters

The previous section shows how to deploy default Percona Distribution for PostgreSQL configuration.

To check available configuration options, see [deploy/cr.yaml](https://raw.githubusercontent.com/percona/percona-postgresql-operator/v{{ release }}/deploy/cr.yaml) and [Custom Resource Options](operator.md). 

To customize the configuration, do the following:

1. Clone the repository with all manifests and source code by executing the following command:

    ```{.bash data-prompt="$" }
    $ git clone -b v{{ release }} https://github.com/percona/percona-postgresql-operator
    ```

2. Edit the required options and apply your modified `deploy/cr.yaml` file as follows:

     ```{.bash data-prompt="$" }
     $ kubectl apply -f deploy/cr.yaml -n postgres-operator        
     ```

## Next steps

You have successfully installed and deployed the Operator. Now let's [connect to PostgreSQL](connect.md)