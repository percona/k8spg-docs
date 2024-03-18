# Percona Operator for PostgreSQL 2.0.0 (Tech preview)

* **Date**

    December 30, 2022

* **Installation**

    [Installing Percona Operator for PostgreSQL](../System-Requirements.md#installation-guidelines) 


The Percona Operator is based on best practices for configuration and setup of
a [Percona Distribution for PostgreSQL on Kubernetes :octicons-link-external-16:](https://www.percona.com/doc/postgresql/LATEST/index.html).
The benefits of the Operator are many, but saving time and delivering a
consistent and vetted environment is key.

!!! note

    Version 2.0.0 of the Percona Operator for PostgreSQL is a **tech preview release** and it is **not recommended for production environments.**
    As of today, we recommend using [Percona Operator for PostgreSQL 1.x :octicons-link-external-16:](https://www.percona.com/https://docs.percona.com/percona-operator-for-postgresql/index.html), which is production-ready and contains everything you need to quickly and consistently deploy and scale PostgreSQL clusters in a Kubernetes-based environment, on-premises or in the cloud.

The *Percona Operator for PostgreSQL 2.x* is based on the 5.x branch of the [Postgres Operator developed by Crunchy Data :octicons-link-external-16:](https://access.crunchydata.com/documentation/postgres-operator/latest/). Please see the main changes in this version below.

## Architecture

[Operator SDK :octicons-link-external-16:](https://sdk.operatorframework.io/) is now used to build and package the Operator. It simplifies the development and brings  more contribution friendliness to the code, resulting in better potential for growing the community. Users now have full control over Custom Resource Definitions that Operator relies on, which simplifies the deployment and management of the operator.

In version 1.x we relied on Deployment resources to run PostgreSQL clusters, whereas in 2.0 Statefulsets are used, which are the de-facto standard for running stateful workloads in Kubernetes. This change improves stability of the clusters and removes a lot of complexity from the Operator.

## Backups

One of the biggest challenges in version 1.x is backups and restores. There are two main problems that our user faced:

* Not possible to change backup configuration for the existing cluster
* Restoration from backup to the newly deployed cluster required workarounds

In this version both these issues are fixed.
In addition to that:

* Run up to 4 pgBackrest repositories
* [Bootstrap the cluster :octicons-link-external-16:](https://docs.percona.com/percona-operator-for-postgresql/2.0/backups.html) from the existing backup through Custom Resource
* [Azure Blob Storage support :octicons-link-external-16:](https://docs.percona.com/percona-operator-for-postgresql/2.0/operator.html#use-azure-blob-storage-for-backups)

## Operations

Deploying complex topologies in Kubernetes is not possible without affinity and anti-affinity rules. In version 1.x there were various limitations and issues, whereas this version comes with substantial [improvements :octicons-link-external-16:](https://docs.percona.com/percona-operator-for-postgresql/2.0/constraints.html) that enables users to craft the topology of their choice. 

Within the same cluster users can deploy [multiple instances :octicons-link-external-16:](https://docs.percona.com/percona-operator-for-postgresql/2.0/operator.html#instances-name). These instances are going to have the same data, but can have different configuration and resources. This can be useful if you plan to migrate to new hardware or need to test the new topology.

Each postgreSQL node can have [sidecar containers :octicons-link-external-16:](https://docs.percona.com/percona-operator-for-postgresql/2.0/operator.html#instances-sidecars-image) now to provide integration with your existing tools or expand the capabilities of the cluster.

## Try it out now

Excited with what you read above?

* We encourage you to install the Operator following [our documentation :octicons-link-external-16:](https://docs.percona.com/percona-operator-for-postgresql/2.0/index.html#quickstart-guides).
* Feel free to share feedback with us on the [forum :octicons-link-external-16:](https://forums.percona.com/c/postgresql/percona-kubernetes-operator-for-postgresql/68) or raise a bug or feature request in [JIRA :octicons-link-external-16:](https://jira.percona.com/projects/K8SPG/issues).
* See the source code in our [Github repository :octicons-link-external-16:](https://github.com/percona/percona-postgresql-operator).

