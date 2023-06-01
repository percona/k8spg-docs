# Percona Operator for PostgreSQL 2.2.0 (Tech preview)

* **Date**

    June 15, 2023

* **Installation**

    [Installing Percona Operator for PostgreSQL](https://docs.percona.com/percona-operator-for-postgresql/2.0/index.html#installation-guide) 


The Percona Operator built with best practices of configuration and setup of
[Percona Distribution for PostgreSQL on Kubernetes](https://www.percona.com/doc/postgresql/LATEST/index.html).

Percona Operator for PostgreSQL helps create and manage highly available, enterprise-ready PostgreSQL clusters on Kubernetes. It is 100% open source, free from vendor lock-in, usage restrictions and expensive contracts, and includes enterprise-ready features: backup/restore, high availability, replication, logging, and more.

The benefits of using Percona Operator for PostgreSQL include saving time on database operations via automation of Day-1 and Day-2 operations and deployment of consistent and vetted environment on Kubernetes.

**Percona announces the general availability of Percona Distribution for PostgreSQL Operator 2.2.0.**


## Release Highlights



## Improvements

* {{ k8spgjira(378) }}: Add a field version or crVersion for identifying operator version

* {{ k8spgjira(285) }}: To improve the Operator we capture anonymous telemetry and usage data. In this release we [add more data points](../telemetry.md) to it

* {{ k8spgjira(295) }}: Additional information was added to the status of the Operator Custom Resource, which now shows `name`, `endpoint`, `status`, and `age` fields

* {{ k8spgjira(304) }}: The Operator stops using trust authentication method in `pg_hba.conf` for better security

* {{ k8spgjira(325) }}: Custom Resource options previously named `paused` and `shutdown` were renamed to `unmanaged` and `pause` for better alignment with other Percona Operators

## Bugs Fixed

* {{ k8spgjira(371) }}: Fresh v2 installation complains about deprecated v1

* {{ k8spgjira(373) }}: Fix the bug due to which the Operator did not not create Secrets for the `pguser` if PMM was enabled in the Custom Resource

* {{ k8spgjira(362) }}: It was impossible to install Custom Resource Definitions for both 1.x and 2.x Operators in one environment, preventing the migration of a cluster to the newer Operator version

* {{ k8spgjira(360) }}: Fix a bug due to which manual password changing or resetting via Secret didn't work

## Supported platforms

The following platforms were tested and are officially supported by the Operator
2.2.0:

* [Google Kubernetes Engine (GKE)](https://cloud.google.com/kubernetes-engine) 1.23 - 1.25

* [Amazon Elastic Container Service for Kubernetes (EKS)](https://aws.amazon.com) 1.23 - 1.25

This list only includes the platforms that the Percona Operators are specifically tested on as part of the release process. Other Kubernetes flavors and versions depend on the backward compatibility offered by Kubernetes itself.

