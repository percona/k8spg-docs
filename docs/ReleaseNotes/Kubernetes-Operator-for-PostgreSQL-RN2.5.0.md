# Percona Operator for PostgreSQL 2.5.0

* **Date**

    September 30, 2024

* **Installation**

    [Installing Percona Operator for PostgreSQL](../System-Requirements.md#installation-guidelines) 

## Release Highlights

Major versions upgrade, introduced in the Operator version 2.4.0 as a tech preview, had undergone some improvements. Now it is possible to upgrade from one PostgreSQL major version to another with custom images of PostgreSQL and, optionally, some other components of the database cluster. The upgrade is still triggered by applying the YAML manifest with the information about the existing and desired major versions, which now includes image names (`toPostgresImage` is required, while `toPgBouncerImage` and `toPgBackRestImage` are optional). The resulting manifest may look as follows:

```yaml
apiVersion: pgv2.percona.com/v2
kind: PerconaPGUpgrade
metadata:
  name: cluster1-15-to-16
spec:
  postgresClusterName: cluster1
  image: percona/percona-postgresql-operator:2.4.1-upgrade
  fromPostgresVersion: 15
  toPostgresVersion: 16
  toPostgresImage: percona/percona-postgresql-operator:2.4.1-ppg16.3-postgres
  toPgBouncerImage: percona/percona-postgresql-operator:2.4.1-ppg16.3-pgbouncer1.22.1
  toPgBackRestImage: percona/percona-postgresql-operator:2.4.1-ppg16.3-pgbackrest2.51-1
```

## Azure Kubernetes Service and Azure Blob Storage support

* [Azure Kubernetes Service (AKS)](../aks.md) is now officially supported platform, so developers and vendors of the solutions based on the Azure platform can take advantage of the official support from Percona or just use officially certified Percona Operator for MysQL images; also, [Azure Blob Storage can now be used for backups](../backups-storage.md#__tabbed_1_2)

## Major versions upgrade improvements


## New features

* {{ k8spxcjira(227) }} and {{ k8spxcjira(157) }}: Add support for the [Azure Kubernetes Service (AKS)](../aks.md) platform and allow [using Azure Blob Storage](../backups-storage.md#__tabbed_1_2) for backups
* {{ k8spgjira(244) }}: Automated storage scaling - track storage size

## Improvements

* {{ k8spgjira(630) }}: A new `backups.trackLatestRestorableTime` Custom Resource option allows to disable latest restorable time tracking for users who need reducing S3 API calls usage
* {{ k8spgjira(605) }} and {{ k8spgjira(593) }}: Documentation now includes information about [upgrading the Operator via Helm](../update.md#upgrade-via-helm) and [using databaseInitSQL commands](../debug-logs.md#use-databaseinitsql-commands)
* {{ k8spgjira(598) }}: Database major version upgrade now [supports custom images](../update.md#major-version-upgrade)
* {{ k8spgjira(588) }}: The Operator didn't stop WAL watcher if the namespace and/or cluster were deleted **BUG FIX?**
* {{ k8spgjira(560) }}: A `pg-restore` Custom Resource is now automatically created at [bootstrapping a new cluster from an existing backup](../backups-restore.md#restore-to-a-new-postgresql-cluster)
* {{ k8spgjira(555) }}: The Operator now creates separate Secret with CA certificate for each cluster
* {{ k8spgjira(553) }}: Provision [of a custom root CA certificate](../TLS.md#provide-custom-root-ca-certificate-to-the-operator) to the Operator is now possible
* {{ k8spgjira(454) }}: Cluster status obtained with kubectl get pg` command is now "ready" not only when all Pods are ready, but also takes into account if all StatefulSets are up to date

## Bugs Fixed

* {{ k8spgjira(629) }}: Fix a bug where Operator was not deleting backup Pods when cleaning outdated backups according to the retention policy
* {{ k8spgjira(587) }}: Fix a bug where restore with wrong pgBackRest argument was putting the cluster in a broken state
* {{ k8spgjira(577) }}: A new `pmm.querySource` Custom Resource option allows to set PMM query source **IMPROVEMENT**
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
