# How the Operator works

This page describes how Percona Operator for PostgreSQL plugs into Kubernetes and how it keeps your database cluster in the state you define.

If you are new to the Operator pattern itself, start with [Kubernetes Operators and Percona Operator](operator-concepts.md). For the runtime stack (database processes, Patroni, backups), see [Cluster architecture](architecture.md).

## How the Operator extends Kubernetes API

Standard Kubernetes resources cover Deployments, Services, and many other kinds. The Operator registers additional Custom Resources, defined via [Custom Resource Definitions (CRDs) :octicons-link-external-16:](https://kubernetes.io/docs/concepts/extend-kubernetes/api-extension/custom-resources/#customresourcedefinitions). 

These Custom Resources are:

* `PerconaPGCluster` for the database cluster
* `PerconaPGBackup` for backups
* `PerconaPGRestore` for restores
* `PerconaPGUpgrade` for major upgrades

The Operator itself runs as a **Deployment** in the Kubernetes cluster. It has controller logic that watches the Custom Resources that the CRDs define. Whenever you create or change a relevant Custom Resource, the Operator's reconciliation loop automatically does the following:

* Creates and manages the necessary Kubernetes resources (StatefulSets, Services, Pods)
* Ensures your cluster matches the desired state you’ve defined
* Monitors the cluster health and automatically recovers from failures
* Coordinates upgrades and scaling operations

These operations ensure that your actual database environment always matches your request.

To learn more about features and capabilities that the Operator brings in, see [Features and capabilities](features.md).

## Next steps

* [Cluster architecture](architecture.md){.md-button}

