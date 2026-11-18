> For the complete documentation index, see [llms.txt](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/llms.txt).

# Install Percona Operator for PostgreSQL using Helm

[Helm](https://github.com/helm/helm) is the package manager for Kubernetes. A Helm [chart](https://helm.sh/docs/topics/charts/) is a package that contains all the necessary files to deploy resources or an application to a Kubernetes cluster.

Helm charts for Percona Operator for PostgreSQL include:

- [Percona Operator for PostgreSQL Deployment](https://github.com/percona/percona-helm-charts/tree/main/charts/pg-operator)
- [Percona Distribution for PostgreSQL](https://github.com/percona/percona-helm-charts/tree/main/charts/pg-db)

You need to install both of them. First you install the Operator Deployment and then you use that to install Percona Distribution for PostgreSQL cluster.

This guide walks you through installing Percona Operator for PostgreSQL with default parameters and names.

To install the Operator with custom parameters or custom resource names, refer to [Install Percona Operator for PostgreSQL with customized parameters](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/custom-install.html).

## Prerequisites

To install and deploy the Operator, you need the following:

1. [Helm v3](https://docs.helm.sh/using_helm/#installing-helm) . Run `helm version` to check the version

1. [kubectl](https://kubernetes.io/docs/tasks/tools/) command line utility.

1. A Kubernetes environment. You can deploy it locally on [Minikube](https://github.com/kubernetes/minikube) for testing purposes or using any cloud provider of your choice. Check the list of our [officially supported platforms](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/System-Requirements.html#supported-platforms).

   See also

   - [Set up Minikube](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/minikube.html#set-up-minikube)
   - [Create and configure the GKE cluster](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/gke.html#create-and-configure-the-gke-cluster)
   - [Set up Amazon Elastic Kubernetes Service](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/eks.html#software-installation)

1. Privileges to create Custom Resource Definitions (CRDs), RBAC resources, and deploy the Operator

## Installation

Here’s a sequence of steps to follow:

1. Add the Percona’s Helm charts repository and make your Helm client up to date with it:

   ```
   helm repo add percona https://percona.github.io/percona-helm-charts/
   helm repo update
   ```

1. It is a good practice to isolate workloads in Kubernetes via namespaces. Create a namespace:

   ```
   kubectl create namespace <my-namespace>
   ```

1. Install the Percona Operator for PostgreSQL:

   ```
   helm install my-operator percona/pg-operator --namespace <my-namespace>
   ```

   The `my-namespace` is the name of your namespace. The `my-operator` parameter is the name of [a new release object](https://helm.sh/docs/intro/using_helm/#three-big-concepts) which is created for the Operator when you install its Helm chart (use any name you like).

1. Install Percona Distribution for PostgreSQL:

   ```
   helm install cluster1 percona/pg-db -n <my-namespace>
   ```

   The `cluster1` parameter is the name of [a new release object](https://helm.sh/docs/intro/using_helm/#three-big-concepts) which is created for the Percona Distribution for PostgreSQL when you install its Helm chart (use any name you like).

1. Check the Operator and replica set Pods status.

   ```
   kubectl get pg -n <my-namespace>
   ```

   The creation process is over when both the Operator and replica set Pods report the `ready` status:

   Expected output

   ```
   NAME       ENDPOINT                                   STATUS   POSTGRES   PGBOUNCER   AGE
   cluster1   cluster1-pgbouncer.postgres-operator.svc   ready    3          3           143m
   ```

You have successfully installed and deployed the Operator with default parameters.

## Next steps

[Connect to PostgreSQL](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/connect.html)
