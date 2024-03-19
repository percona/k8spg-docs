# Install Percona Distribution for PostgreSQL on Minikube

Installing the Percona Operator for PostgreSQL on [Minikube :octicons-link-external-16:](https://github.com/kubernetes/minikube)
is the easiest way to try it locally without a cloud provider. 

Minikube runs
Kubernetes on GNU/Linux, Windows, or macOS system using a system-wide
hypervisor, such as VirtualBox, KVM/QEMU, VMware Fusion or Hyper-V. Using it is
a popular way to test Kubernetes application locally prior to deploying it on a
cloud.

This document describes how to deploy the Operator and Percona Distribution
for PostgreSQL on Minikube.

## Set up Minikube {.power-number}

1. [Install Minikube :octicons-link-external-16:](https://kubernetes.io/docs/tasks/tools/install-minikube/), using a way recommended for your system. This includes the installation of the following three components:

    1. kubectl tool,

    2. a hypervisor, if it is not already installed,

    3. actual minikube package

    
2. After the installation, initialize and start the Kubernetes cluster. The parameters we pass for the following command increase the virtual machine limits for the CPU cores, memory, and disk, to ensure stable work of the Operator:

    ```{.bash data-prompt="$"}
    $ minikube start --memory=5120 --cpus=4 --disk-size=30g
    ```

    This command downloads needed virtualized images, then initializes and runs the
    cluster. 

3. After Minikube is successfully started, you can optionally run the
    Kubernetes dashboard, which visually represents the state of your cluster.
    Executing `minikube dashboard` starts the dashboard and opens it in your
    default web browser.

## Deploy the Percona Operator for PostgreSQL {.power-number}

1. Deploy the Operator [using :octicons-link-external-16:](https://kubernetes.io/docs/reference/using-api/server-side-apply/) the following command:

    ```{.bash data-prompt="$" }
    $ kubectl apply --server-side -f https://raw.githubusercontent.com/percona/percona-postgresql-operator/v{{ release }}/deploy/bundle.yaml
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

    As the result you have the Operator Pod up and running.

2. Deploy Percona Distribution for PostgreSQL:

    ```{.bash data-prompt="$" }
    $ kubectl apply -f https://raw.githubusercontent.com/percona/percona-postgresql-operator/v{{ release }}/deploy/cr.yaml
    ```

    ??? example "Expected output"

        ```{.text .no-copy}
        perconapgcluster.pgv2.percona.com/cluster1 created
        ```

    !!! note 

        This deploys the default Percona Distribution for PostgreSQL configuration.
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
        $ kubectl apply -f deploy/cr.yaml
        ```

3. The creation process may take some time. When the process is over your
    cluster will obtain the `ready` status. You can check it with the following
    command:
   
    ``` {.bash data-prompt="$" }
    $ kubectl get pg -n postgres-operator
    ```
    
    ??? example "Expected output"
   
        --8<-- "kubectl-get-pg-response.txt"

## Verify the Percona Distribution for PostgreSQL cluster operation

When creation process is over, the output of the `kubectl get pg` command shows the cluster status as `ready`. You can try to connect to the cluster.

{% include 'assets/fragments/connectivity.txt' %}

## Delete the cluster

If you need to delete the Operator and PostgreSQL cluster (for example, to clean
up the testing deployment before adopting it for production use), check
[this HowTo](delete.md).

If you no longer need the Kubernetes cluster in Minikube, the following are the
steps to remove it. 
{.power-number}

1. Stop the Minikube cluster:

    ```
    $ minikube stop
    ```

2. Delete the cluster 

    ```
    $ minikube delete
    ```

    This command deletes the virtual machines, and removes all associated files.


