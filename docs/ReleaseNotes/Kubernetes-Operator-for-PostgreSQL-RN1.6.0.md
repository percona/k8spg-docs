# *Percona Operator for PostgreSQL* 1.6.0

* **Date**

    May 23, 2024

* **Installation**

    [Percona Operator for PostgreSQL](../index.md#installation-guides)

## Release Highlights

Percona Operator for PostgreSQL* 1.6.0 is the last release of the 1.x branch,
as far as the Operator 1.x goes end-of-life in July, 2024. It contains last 
fixes components version updates.

We strongly recommend switching to [Percona Operator for PostgreSQL 2.x](https://docs.percona.com/percona-operator-for-postgresql/2.0/index.html).
The Operator version 2 has newer PostgreSQL versions, new features and improvements.

## Bugs Fixed

* {{ k8spgjira(547) }}: Fix dependency issue which made pgbackrest-repo container incompatible with pgBackRest 2.50, resulting in the older 2.48 version being used instead

* {{ k8spgjira(490) }}: Fix a bug whre replication would break in case of primary instance outage for PostgreSQL 14 and older versions.

## Supported platforms

The Operator was developed and tested with PostgreSQL versions 12.18, 13.14, and 14.11. Other options may also work but have not been tested. The Operator 1.6.0 provides connection pooling based on pgBouncer 1.22.0 and high-availability implementation based on Patroni 3.2.2.

The following platforms were tested and are officially supported in this release:

* [Google Kubernetes Engine (GKE)](https://cloud.google.com/kubernetes-engine) 1.26-1.29

* [Amazon Elastic Container Service for Kubernetes (EKS)](https://aws.amazon.com) 1.26-1.29

* [OpenShift](https://www.redhat.com/en/technologies/cloud-computing/openshift) 4.12.57 - 4.15.13

* [Minikube](https://minikube.sigs.k8s.io/docs/) 1.33

