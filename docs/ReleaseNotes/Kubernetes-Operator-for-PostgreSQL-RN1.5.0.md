# *Percona Operator for PostgreSQL* 1.5.0

* **Date**

    November 30, 2023

* **Installation**

    [Percona Operator for PostgreSQL](../index.md#installation-guides)

## Improvements

* {{ k8spgjira(340) }}: To improve the operator we capture anonymous telemetry and usage data. In this release we add [more data points](../telemetry.md) to it

## Bugs Fixed

* {{ k8spgjira(420) }}: Fix a bug due to which pausing and unpausing the cluster after modification of Custom Resource could result in wrong scale of replica and backrest repo Pods

* {{ k8spgjira(314) }}: The Operator was incorrectly parsing the version string to get major minor versions in case of recent Percona Distribution for PostgreSQL releases, being unable to provide Version Service with this data to check available versions for the database upgrade
  
* {{ k8spgjira(404) }}: Fix a bug due to which upgrading the Operator version 1.3 to 1.4 could cause the cluster to have no replicas

* {{ k8spgjira(464) }}: Fix a bug in the Affinity configuration process that could leads to unscheduled Pods

## Supported platforms

The Operator was developed and tested with PostgreSQL versions 12.14, 13.10, and 14.7. Other options may also work but have not been tested. The Operator 1.4.0 provides connection pooling based on pgBouncer 1.18.0 and high-availability implementation based on Patroni 2.1.4.

The following platforms were tested and are officially supported in this release:


* [Google Kubernetes Engine (GKE)](https://cloud.google.com/kubernetes-engine) 1.22 - 1.25

* [Amazon Elastic Container Service for Kubernetes (EKS)](https://aws.amazon.com) 1.22 - 1.25

* [OpenShift](https://www.redhat.com/en/technologies/cloud-computing/openshift) 4.10 - 4.12

* [Minikube](https://minikube.sigs.k8s.io/docs/) 1.28 (based on Kubernetes 1.25)


	Bug	
