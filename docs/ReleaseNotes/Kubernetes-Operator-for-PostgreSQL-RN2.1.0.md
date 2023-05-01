# Percona Operator for PostgreSQL 2.1.0 (Tech preview)

* **Date**

    May 4, 2023

* **Installation**

    [Installing Percona Operator for PostgreSQL](https://www.percona.com/doc/kubernetes-operator-for-postgresql/2.0/index.html#installation-guide) 


The Percona Operator is based on best practices for configuration and setup of
a [Percona Distribution for PostgreSQL on Kubernetes](https://www.percona.com/doc/postgresql/LATEST/index.html).
The benefits of the Operator are many, but saving time and delivering a
consistent and vetted environment is key.

!!! note

    Version 2.1.0 of the Percona Operator for PostgreSQL is a **tech preview release** and it is **not recommended for production environments.**
    As of today, we recommend using [Percona Operator for PostgreSQL 1.x](https://www.percona.com/https://docs.percona.com/percona-operator-for-postgresql/index.html), which is production-ready and contains everything you need to quickly and consistently deploy and scale PostgreSQL clusters in a Kubernetes-based environment, on-premises or in the cloud.

The *Percona Operator for PostgreSQL 2.x* is based on the 5.x branch of the [Postgres Operator developed by Crunchy Data](https://access.crunchydata.com/documentation/postgres-operator/latest/). Please see the main changes in this version below.

## Release Highlights

* The [automated upgrade](../update.md#automatic-upgrade) is now disabled by default to prevent an unplanned downtimes for user applications and to provide defaults more focused on strict user’s control over the cluster

* [Flexible anti-affinity configuration](../constraints.md) is now available, which allows the Operator to isolate PostgreSQL cluster instances on different Kubernetes nodes or to increase its availability by placing PostgreSQL instances in different availability zones

## New Features

* {{ k8spgjira(158) }}: Restore from a backup to the new cluster

* {{ k8spgjira(282) }}: Add support for PostgreSQL v 15

* {{ k8spgjira(328) }}: PVCs should be preserved on custom resource deletion	Dmitriy Kostiuk	In Doc	MERGED	
* {{ k8spgjira(330) }}: SSL secrets should be preserved on deletion	Dmitriy Kostiuk	In Doc	MERGED	
* {{ k8spgjira(331) }}: Add short name for CRD

## Improvements

* {{ k8spgjira(262) }}: Operator should not try to start PMM if there is no 'pmmserverkey or pmmserver' key in secret

* {{ k8spgjira(272) }}: pmm agent is not deleted from server inventory on pod termination

* {{ k8spgjira(278) }}: Keep finalizers consistent between cluster objects

* {{ k8spgjira(285) }}: More questions answered with telemetry

* {{ k8spgjira(295) }}: PerconaPGCluster CR status inconsistencies with other operators

* {{ k8spgjira(304) }}: Reconsider using trust in pg_hba.conf

* {{ k8spgjira(305) }}: Research migration process

* {{ k8spgjira(306) }}: Ensure feature parity with v1

* {{ k8spgjira(325) }}: Custom resource pause and shutdown alignment	Dmitriy Kostiuk	In Doc	Under Review	

* {{ k8spgjira(327) }}: Consider removing Crunchy status from PostgresClusterStatus

## Bugs Fixed

* {{ k8spgjira(217) }}: Point In Time recovery after a failover results in just 2 node cluster

* {{ k8spgjira(279) }}: Operator will crash after creating backup if there is no manual section in CR

* {{ k8spgjira(298) }}: Can't restart or pause the cluster

* {{ k8spgjira(309) }}: Can't customize the user secrets name

* {{ k8spgjira(321) }}: Update CR template

* {{ k8spgjira(321) }}: Invalid URL

* {{ k8spgjira(334) }}: monitoring user should not have some special characters in it's password

## Supported platforms

The following platforms were tested and are officially supported by the Operator
2.1.0:


* [Google Kubernetes Engine (GKE)](https://cloud.google.com/kubernetes-engine) 1.21 - 1.24

* [Amazon Elastic Container Service for Kubernetes (EKS)](https://aws.amazon.com) 1.20 - 1.22

* [OpenShift](https://www.redhat.com/en/technologies/cloud-computing/openshift) 4.7 - 4.10

This list only includes the platforms that the Percona Operators are specifically tested on as part of the release process. Other Kubernetes flavors and versions depend on the backward compatibility offered by Kubernetes itself.

