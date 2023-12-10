# *Percona Operator for PostgreSQL* 1.5.0

* **Date**

    December 11, 2023

* **Installation**

    [Percona Operator for PostgreSQL](../index.md#installation-guides)

## Release highlights

This release contains a number of fixes and improvements made within the maintenance mode that the Operator 1.x is in.

The Operator 1.x goes end-of-life in July, 2024, so we strongly recommend to use
[Percona Operator for PostgreSQL 2.x](https://docs.percona.com/percona-operator-for-postgresql/2.0/index.html) instead. The Operator version 2 has newer PostgreSQL versions, new features and improvements, which will not find their way to the Operator 1.x version.

## Improvements

* {{ k8spgjira(340) }}: To continuously improve the Operator we capture anonymous telemetry and usage data. In this release we add [more data points](../telemetry.md) to it

## Bugs Fixed

* {{ k8spgjira(420) }}: Fix a bug due to which pausing and unpausing the cluster after modification of Custom Resource could result in wrong scale of replica and backrest repo Pods

* {{ k8spgjira(314) }}: Version Service at check.percona.com was was incorrectly parsing the version string which lead to issues with automated upgrades
  
* {{ k8spgjira(404) }}: Fix a bug due to which upgrading the Operator version 1.3 to 1.4 could cause the cluster to have no replicas

* {{ k8spgjira(464) }}: Our Affinity configuration was not taking components into account. This led to unschedulable Pods that were stuck in Pending state. It is fixed in this release through adding component labels

## Supported platforms

The Operator was developed and tested with PostgreSQL versions 12.16, 13.12, and 14.10. Other options may also work but have not been tested. The Operator 1.5.0 provides connection pooling based on pgBouncer 1.20.0 and high-availability implementation based on Patroni 2.1.4.

The following platforms were tested and are officially supported in this release:


* [Google Kubernetes Engine (GKE)](https://cloud.google.com/kubernetes-engine) 1.24 - 1.28

* [Amazon Elastic Container Service for Kubernetes (EKS)](https://aws.amazon.com) 1.24 - 1.28

* [OpenShift](https://www.redhat.com/en/technologies/cloud-computing/openshift) 4.11 - 4.14

* [Minikube](https://minikube.sigs.k8s.io/docs/) 1.32

