# *Percona Operator for PostgreSQL* 1.4.0

* **Date**

    March 31, 2023

* **Installation**

    [Percona Operator for PostgreSQL](../index.md#installation-guides)

## Improvements

* {{ k8spgjira(188) }}: Add Custom Resource options to set static IP address for the pgPrimary, pgReplicas, and pgBouncer LoadBalancers

* {{ k8spgjira(269) }}: It is now possible to define affinity and anti-affinity rules for backup Pods

* {{ k8spgjira(270) }}: The new `schedule.backrestOpts` Custom Resource option allows customizing pgBackRest parameters for scheduled backups

* {{ k8spgjira(292) }}: The Operator now uses units based on the power of 2 (e.g. `GiB` instead of `G`) for the storage size, to make it multiple of the 1024 default kernel block size (thanks to Rodney Karemba for contribution)

## Bugs Fixed

* {{ k8spgjira(286) }}: Fix a bug which caused PMM client connection fail when the `TLSOnly` Custom Resource option was set to require TLS for all connections

* {{ k8spgjira(290) }}: Fix a bug due to which ssh connection used for backups and new replica creation could hang if exceeding the PostgreSQL 60 seconds timeout (e.g. because of network problems); to avoid such orphaned connections, gbackrest archive-push command is now automatically killed after timeout

* {{ k8spgjira(291) }}: Fix a bug which prevented backup schedule in the Custom Resource to be updated  without deleting the existing schedule first and recreating it as a new one

## Supported platforms

The Operator was developed and tested with PostgreSQL versions 12.14, 13.10, and 14.7. Other options may also work but have not been tested. The Operator 1.4.0 provides connection pooling based on pgBouncer 1.18.0 and high-availability implementation based on Patroni 2.1.4.

The following platforms were tested and are officially supported in this release:


* [Google Kubernetes Engine (GKE)](https://cloud.google.com/kubernetes-engine) 1.22 - 1.25

* [Amazon Elastic Container Service for Kubernetes (EKS)](https://aws.amazon.com) 1.22 - 1.25

* [OpenShift](https://www.redhat.com/en/technologies/cloud-computing/openshift) 4.10 - 4.12

* [Minikube](https://minikube.sigs.k8s.io/docs/) 1.28 (based on Kubernetes 1.25)


This list only includes the platforms that the Percona Operators are specifically tested on as part of the release process. Other Kubernetes flavors and versions depend on the backward compatibility offered by Kubernetes itself.
