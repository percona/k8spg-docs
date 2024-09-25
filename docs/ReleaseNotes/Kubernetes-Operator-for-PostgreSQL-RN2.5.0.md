# Percona Operator for PostgreSQL 2.5.0

* **Date**

    September 30, 2024

* **Installation**

    [Installing Percona Operator for PostgreSQL](../System-Requirements.md#installation-guidelines) 

## Release Highlights

## Azure Kubernetes Service and Azure Blob Storage support

* [Azure Kubernetes Service (AKS)](../aks.md) is now officially supported platform, so developers and vendors of the solutions based on the Azure platform can take advantage of the official support from Percona or just use officially certified Percona Operator for MysQL images; also, [Azure Blob Storage can now be used for backups](../backups-storage.md#__tabbed_1_2)

## New features

* {{ k8spxcjira(227) }} and {{ k8spxcjira(157) }}: Add support for the [Azure Kubernetes Service (AKS)](../aks.md) platform and allow [using Azure Blob Storage](../backups-storage.md#__tabbed_1_2) for backups
* {{ k8spgjira(244) }}: Automated storage scaling - track storage size

## Improvements

* {{ k8spgjira(445) }}: Confgiure storageClass in CR / volumeClaimSpec
* {{ k8spgjira(630) }}: Add a field to let users disable latest restorable time tracking
* {{ k8spgjira(605) }}: Add information about helm upgrade
* {{ k8spgjira(598) }}: Support custom images in major upgrade
* {{ k8spgjira(593) }}: DOC Task: Document the usage of databaseinitSQL commands
* {{ k8spgjira(588) }}: Operator must stop WAL watcher if namespace or cluster does not exist
* {{ k8spgjira(560) }}: Add pg-restore CR for initial restoration using the dataSource field
* {{ k8spgjira(555) }}: The Operator now creates separate Secret with CA certificate for each cluster
* {{ k8spgjira(553) }}: Allow provision [of a custom root CA certificate](../TLS.md#provide-custom-root-ca-certificate-to-the-operator) to the Operator
* {{ k8spgjira(454) }}: Cluster status must be ready only if all statefulsets are up to date

## Bugs Fixed

* {{ k8spgjira(629) }}: Fix a bug where Operator was not deleting backup Pods when cleaning outdated backups according to the retention policy
* {{ k8spgjira(587) }}: Fix a bug where restore with wrong pgBackRest argument was putting the cluster in a broken state
* {{ k8spgjira(577) }}: A new `pmm.querySource` Custom Resource option allows to set PMM query source
* {{ k8spgjira(499) }}: Fix a bug whre cluster was getting stuck in the init state if pgBackRest secret didn't exist
* {{ k8spgjira(446) }}: Fix a bug due to which dots were not allowed in the s3 bucket name

## Deprecation and removal

* The `plpythonu` extension was removed from the list of built-in PostgreSQL extensions; users who still need it can enable it for their databases via [custom extensions functionality](../custom-extensions.md)

## Supported platforms

The Operator was developed and tested with PostgreSQL versions 12.19, 13.15, 14.12, 15.7, and 16.3. Other options may also work but have not been tested. The Operator 2.5.0 provides connection pooling based on pgBouncer 1.22.1 and high-availability implementation based on Patroni 3.3.0.

The following platforms were tested and are officially supported by the Operator
2.4.0:

* [Google Kubernetes Engine (GKE) :octicons-link-external-16:](https://cloud.google.com/kubernetes-engine) 1.27 - 1.29
* [Amazon Elastic Container Service for Kubernetes (EKS) :octicons-link-external-16:](https://aws.amazon.com) 1.27 - 1.30
* [OpenShift :octicons-link-external-16:](https://www.redhat.com/en/technologies/cloud-computing/openshift) 4.12.59 - 4.15.18
* [Minikube :octicons-link-external-16:](https://github.com/kubernetes/minikube) 1.33.1

This list only includes the platforms that the Percona Operators are specifically tested on as part of the release process. Other Kubernetes flavors and versions depend on the backward compatibility offered by Kubernetes itself.
