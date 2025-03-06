# Percona Operator for PostgreSQL 2.5.1

* **Date**

    March 03, 2025

* **Installation**

    [Installing Percona Operator for PostgreSQL](../System-Requirements.md#installation-guidelines) 


## Release highlights


This release fixes the [CVE-2025-1094 :octicons-link-external-16:](https://www.postgresql.org/support/security/CVE-2025-1094/), vulnerability in the libpq PostgreSQL client library, which made images used by the Operator vulnerable to SQL injection within the PostgreSQL interactive terminal due to the lack of neutralizing quoting. For now, the fix includes the image of PostgreSQL 16.8 and other database cluster images based on PostgreSQL 16.8. Fixed images for other PostgreSQL versions are to follow in the upcoming days.

*Update from March 04, 2025*: images of PostgreSQL 15.12 and other database cluster components based on PostgreSQL 15.12 were added. 

*Update from March 06, 2025*: images of PostgreSQL 14.17 and other database cluster components based on PostgreSQL 14.17 were added. 

## Supported platforms

The Operator was developed and tested with PostgreSQL versions 14.17, 15.12, and 16.8. Other options may also work but have not been tested. The Operator 2.5.1 provides connection pooling based on pgBouncer 1.24.0 and high-availability implementation based on Patroni 3.3.2.

The following platforms were tested and are officially supported by the Operator 2.5.1:

* [Google Kubernetes Engine (GKE) :octicons-link-external-16:](https://cloud.google.com/kubernetes-engine) 1.28 - 1.30
* [Amazon Elastic Container Service for Kubernetes (EKS) :octicons-link-external-16:](https://aws.amazon.com) 1.28 - 1.30
* [OpenShift :octicons-link-external-16:](https://www.redhat.com/en/technologies/cloud-computing/openshift) 4.13.46 - 4.16.7
* [Azure Kubernetes Service (AKS) :octicons-link-external-16:](https://azure.microsoft.com/en-us/services/kubernetes-service/) 1.28 - 1.30
* [Minikube :octicons-link-external-16:](https://github.com/kubernetes/minikube) 1.34.0 with Kubernetes 1.31.0

This list only includes the platforms that the Percona Operators are specifically tested on as part of the release process. Other Kubernetes flavors and versions depend on the backward compatibility offered by Kubernetes itself.
