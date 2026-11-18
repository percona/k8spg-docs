> For the complete documentation index, see [llms.txt](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/llms.txt).

# How the Operator works

This page describes how Percona Operator for PostgreSQL plugs into Kubernetes and how it keeps your database cluster in the state you define.

If you are new to the Operator pattern itself, start with [Kubernetes Operators and Percona Operator](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/operator-concepts.html). For the runtime stack (database processes, Patroni, backups), see [Cluster architecture](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/architecture.html).

## How the Operator extends Kubernetes API

Standard Kubernetes resources cover Deployments, Services, and many other kinds. The Operator registers additional Custom Resources, defined via [Custom Resource Definitions (CRDs)](https://kubernetes.io/docs/concepts/extend-kubernetes/api-extension/custom-resources/#customresourcedefinitions) .

These Custom Resources are:

- `PerconaPGCluster` for the database cluster
- `PerconaPGBackup` for backups
- `PerconaPGRestore` for restores
- `PerconaPGUpgrade` for major upgrades

The Operator itself runs as a **Deployment** in the Kubernetes cluster. It has controller logic that watches the Custom Resources that the CRDs define. Whenever you create or change a relevant Custom Resource, the Operator’s reconciliation loop automatically does the following:

- Creates and manages the necessary Kubernetes resources (StatefulSets, Services, Pods)
- Ensures your cluster matches the desired state you’ve defined
- Monitors the cluster health and automatically recovers from failures
- Coordinates upgrades and scaling operations

These operations ensure that your actual database environment always matches your request.

To learn more about features and capabilities that the Operator brings in, see [Features and capabilities](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/features.html).

## Next steps

- [Cluster architecture](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/architecture.html)
