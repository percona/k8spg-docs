> For the complete documentation index, see [llms.txt](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/llms.txt).

# Install Percona Operator for PostgreSQL using kubectl

Percona Operator for PostgreSQL is a custom controller that will manage your PostgreSQL clusters inside Kubernetes. The Operator will automatically deploy, maintain, and monitor PostgreSQL databases, so you don’t have to manage these tasks manually.

We recommend installing the Operator with the [kubectl](https://kubernetes.io/docs/tasks/tools/) command line utility. It is the universal way to interact with Kubernetes. Alternatively, you can install the Operator using the [Helm](https://github.com/helm/helm) package manager.

[Install with kubectl](#prerequisites) [Install with Helm](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/helm.html)

## What you will install

- The Operator - the custom controller that uses the custom resources to install and manage the lifecycle of your database cluster. It consists of the following components:

  - the Operator Deployment - the controller Pod
  - The CustomResourceDefinitions (CRDs) add new API types (custom resources) to Kubernetes so that it can understand and manage them
  - Role-based access control (RBAC) is the system that controls who can perform which actions on which resources, using roles and bindings to enforce safe, predictable access.

- The database cluster - the actual Percona Distribution for PostgreSQL cluster that the Operator creates for you when you apply the Custom Resource or install the Helm chart. It includes StatefulSets for PostgreSQL servers, Services and Secrets.

The default Percona Distribution for PostgreSQL configuration includes:

- 3 PostgreSQL servers, one Primary and two replicas.
- 3 pgBouncer instances - a lightweight connection pooler for PostgreSQL that sits between client applications and the database server to manage and reuse connections efficiently.
- a pgBackRest repository host instance – a dedicated instance in your cluster that stores filesystem backups made with pgBackRest - a backup and restore utility.
- a PMM client instance - a monitoring and management tool for PostgreSQL that provides a way to monitor and manage your database. It runs as a sidecar container in the database Pods.

Read more about the default components in [Architecture](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/architecture.html).

## Prerequisites

To install Percona Operator for PostgreSQL, you need the following:

1. The **kubectl** tool to manage and deploy applications on Kubernetes, included in most Kubernetes distributions. Install not already installed, [follow its official installation instructions](https://kubernetes.io/docs/tasks/tools/install-kubectl/) .

1. A Kubernetes environment. You can deploy it on [Minikube](https://github.com/kubernetes/minikube) for testing purposes or using any cloud provider of your choice. Check the list of our [officially supported platforms](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/System-Requirements.html#supported-platforms).

   See also

   - [Set up Minikube](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/minikube.html#set-up-minikube)
   - [Create and configure the GKE cluster](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/gke.html#create-and-configure-the-gke-cluster)
   - [Set up Amazon Elastic Kubernetes Service](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/eks.html#software-installation)
   - [Create and configure the AKS cluster](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/aks.html)

## Procedure

Here’s a sequence of steps to follow:

1. Create the Kubernetes namespace for your cluster. It is a good practice to isolate workloads in Kubernetes by installing the Operator in a custom namespace. For example, let’s name it `postgres-operator`:

   ```
   kubectl create namespace postgres-operator
   ```

   Expected output

   ```
   namespace/postgres-operator was created
   ```

   We will use this namespace further on in this document. If you used another name, make sure to replace it in the following commands.

1. Deploy the Operator [using](https://kubernetes.io/docs/reference/using-api/server-side-apply/) the following command:

   ```
   kubectl apply --server-side -f https://raw.githubusercontent.com/percona/percona-postgresql-operator/v3.1.0/deploy/bundle.yaml -n postgres-operator
   ```

   Expected output

   ```
   customresourcedefinition.apiextensions.k8s.io/crunchybridgeclusters.postgres-operator.crunchydata.com serverside-applied
   customresourcedefinition.apiextensions.k8s.io/perconapgbackups.pgv2.percona.com serverside-applied
   customresourcedefinition.apiextensions.k8s.io/perconapgclusters.pgv2.percona.com serverside-applied
   customresourcedefinition.apiextensions.k8s.io/perconapgrestores.pgv2.percona.com serverside-applied
   customresourcedefinition.apiextensions.k8s.io/perconapgupgrades.pgv2.percona.com serverside-applied
   customresourcedefinition.apiextensions.k8s.io/pgadmins.postgres-operator.crunchydata.com serverside-applied
   customresourcedefinition.apiextensions.k8s.io/pgupgrades.postgres-operator.crunchydata.com serverside-applied
   customresourcedefinition.apiextensions.k8s.io/postgresclusters.postgres-operator.crunchydata.com serverside-applied
   serviceaccount/percona-postgresql-operator serverside-applied
   role.rbac.authorization.k8s.io/percona-postgresql-operator serverside-applied
   rolebinding.rbac.authorization.k8s.io/service-account-percona-postgresql-operator serverside-applied
   deployment.apps/percona-postgresql-operator serverside-applied
   ```

   At this point, the Operator Pod is up and running.

1. Deploy Percona Distribution for PostgreSQL cluster:

   ```
   kubectl apply -f https://raw.githubusercontent.com/percona/percona-postgresql-operator/v3.1.0/deploy/cr.yaml -n postgres-operator
   ```

   Expected output

   ```
   perconapgcluster.pgv2.percona.com/cluster1 created
   ```

1. Check the Operator and replica set Pods status.

   ```
   kubectl get pg -n postgres-operator
   ```

   The creation process may take some time. When the process is over your cluster obtains the ready status.

   Expected output

   ```
   NAME       ENDPOINT                                   STATUS   POSTGRES   PGBOUNCER   AGE
   cluster1   cluster1-pgbouncer.postgres-operator.svc   ready    3          3           143m
   ```

You have successfully installed and deployed the Operator with default parameters. You can check them in the [Custom Resource options reference](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/operator.html).

## Next steps

[Connect to PostgreSQL](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/connect.html)
