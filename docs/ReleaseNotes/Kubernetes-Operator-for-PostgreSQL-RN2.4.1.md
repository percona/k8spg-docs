# Percona Operator for PostgreSQL 2.4.1

* **Date**

    August 6, 2024

* **Installation**

    [Installing Percona Operator for PostgreSQL](../System-Requirements.md#installation-guidelines) 

## Bugs Fixed

* {{ k8spgjira(616) }}: Fix a bug where it was not possible to create a new cluster after deleting the previous one with the `kubectl delete pg` command

## Supported platforms

The Operator was developed and tested with PostgreSQL versions 12.19, 13.15, 14.12, 15.7, and 16.3. Other options may also work but have not been tested. The Operator 2.4.1 provides connection pooling based on pgBouncer 1.22.1 and high-availability implementation based on Patroni 3.3.0.

The following platforms were tested and are officially supported by the Operator
2.4.1:

* [Google Kubernetes Engine (GKE) :octicons-link-external-16:](https://cloud.google.com/kubernetes-engine) 1.27 - 1.29
* [Amazon Elastic Container Service for Kubernetes (EKS) :octicons-link-external-16:](https://aws.amazon.com) 1.27 - 1.30
* [OpenShift :octicons-link-external-16:](https://www.redhat.com/en/technologies/cloud-computing/openshift) 4.12.59 - 4.15.18
* [Minikube :octicons-link-external-16:](https://github.com/kubernetes/minikube) 1.33.1

This list only includes the platforms that the Percona Operators are specifically tested on as part of the release process. Other Kubernetes flavors and versions depend on the backward compatibility offered by Kubernetes itself.
