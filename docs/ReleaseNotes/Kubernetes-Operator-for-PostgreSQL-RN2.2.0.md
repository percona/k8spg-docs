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

* PostgreSQL 15 is now officially supported by the Operator with the [new exciting features](https://www.percona.com/blog/postgresql-15-new-features-to-be-excited-about/) it brings to developers

* UX improvements related to Custom Resource have been added in this release, including the handy `pg`, `pg-backup`, and `pg-restore` short names useful to quickly query the cluster state with the `kubectl get` command and additional information in the status fields, which now show `name`, `endpoint`, `status`, and `age`

## New Features







* {{ k8spgjira(282) }}: PostgreSQL 15 is now officially supported by the Operator

## Improvements

* {{ k8spgjira(378) }}: Add a field version or crVersion for identifying operator version

* {{ k8spgjira(285) }}: To improve the Operator we capture anonymous telemetry and usage data. In this release we [add more data points](../telemetry.md) to it

* {{ k8spgjira(295) }}: Additional information was added to the status of the Operator Custom Resource, which now shows `name`, `endpoint`, `status`, and `age` fields

* {{ k8spgjira(304) }}: The Operator stops using trust authentication method in `pg_hba.conf` for better security

* {{ k8spgjira(325) }}: Custom Resource options previously named `paused` and `shutdown` were renamed to `unmanaged` and `pause` for better alignment with other Percona Operators

## Bugs Fixed

* {{ k8spgjira(371) }}: Fresh v2 installation complains about deprecated v1

* {{ k8spgjira(373) }}: If pmm is enabled we do not create default user secret cluster1-pguser-cluster1

* {{ k8spgjira(362) }}: Migration v1 to v2 - not possible to install CRDs of both operators

* {{ k8spgjira(334) }}: Fix a bug which prevented password management work via secret 

## Supported platforms

The following platforms were tested and are officially supported by the Operator
2.2.0:

* [Google Kubernetes Engine (GKE)](https://cloud.google.com/kubernetes-engine) 1.23 - 1.25

* [Amazon Elastic Container Service for Kubernetes (EKS)](https://aws.amazon.com) 1.23 - 1.25

This list only includes the platforms that the Percona Operators are specifically tested on as part of the release process. Other Kubernetes flavors and versions depend on the backward compatibility offered by Kubernetes itself.

