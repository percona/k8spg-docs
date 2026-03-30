# Install Percona Operator for PostgreSQL on Digital Ocean Kubernetes Service (DOKS)

This guide shows you how to deploy Percona Operator for PostgreSQL on Digital Ocean Kubernetes Service (DOKS) with default parameters. 

The document assumes some experience with the
platform. For more information on the DOKS, see the [Digital Ocean Kubernetes Service official documentation :octicons-link-external-16:](https://docs.digitalocean.com/products/kubernetes/).


--8<-- "what-you-install.txt"

To customize the installation, refer to [Install Percona Operator for PostgreSQL with customized parameters](custom-install.md).

## Prerequisites

Install and configure the following:

1. [`doctl` Command Line Interface (CLI) :octicons-link-external-16:](https://docs.digitalocean.com/reference/doctl/how-to/install/) to manage DOKS clusters.
2. A [Digital Ocean personal access token :octicons-link-external-16:](https://docs.digitalocean.com/reference/api/create-personal-access-token/) to grant account access to `doctl`
3. [kubectl :octicons-link-external-16:](https://cloud.google.com/kubernetes-engine/docs/quickstart#choosing_a_shell) to manage Kubernetes resources.

## Create a DOKS cluster

1. Decide on the following:

    * Cluster name.
    * Region where you will deploy the cluster
    * Kubernetes version
    * A [node pool](https://docs.digitalocean.com/products/kubernetes/how-to/add-node-pools/) for the cluster to reside on.

2. Create a Digital Ocean cluster following the [official documentation :octicons-link-external-16:](https://docs.digitalocean.com/products/kubernetes/how-to/create-clusters/).
3. Add authentication token or a certificate to your kubectl configuration file to connect. Follow [official documentation :octicons-link-external-16:](https://docs.digitalocean.com/products/kubernetes/how-to/connect-to-cluster/) for steps

## Install the Operator deployment

1. Create a namespace for your cluster and export it as an environment variable to simplify further configuration:
    
    ```bash
    kubectl create namespace <namespace>
    export NAMESPACE=<namespace>
    ```

2. Create the Custom Resource Definition, set up RBAC, and install the Operator Deployment using the the bundle file:
    
    ```bash
    kubectl apply --server-side -f https://raw.githubusercontent.com/percona/percona-postgresql-operator/v{{ release }}/deploy/bundle.yaml -n $NAMESPACE
    ```

    ??? example "Expected output"

        --8<-- "kubectl-apply-bundle-response.txt"

    As the result you will have the Operator Pod up and running.

## Install Percona Distribution for PostgreSQL

1. Create the Percona Distribution for PostgreSQL cluster:

    ```bash
    kubectl apply -f https://raw.githubusercontent.com/percona/percona-postgresql-operator/v{{ release }}/deploy/cr.yaml -n $NAMESPACE
    ```

    ??? example "Expected output"

        ``` {.text .no-copy}
        perconapgcluster.pgv2.percona.com/cluster1 created
        ```

2. Check the cluster status. Creation may take a few minutes:

    ```bash
    kubectl get pg -n $NAMESPACE
    ```

    ??? example "Expected output"

        --8<-- "kubectl-get-pg-response.txt"

## Verifying the cluster operation

When creation process is over, `kubectl get pg` command will show you the
cluster status as `ready`, and you can try to connect to the cluster.

{% include 'assets/fragments/connectivity.txt' %}

## Delete the DOKS cluster

To delete the DOKS cluster, run the following command:

```bash
doctl kubernetes cluster delete <cluster-name>
```

The cluster deletion may take time.

!!! warning

    After deleting the cluster, all data stored in it will be lost!

