> For the complete documentation index, see [llms.txt](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/llms.txt).

# Percona Operator for PostgreSQL 2.5.0

- **Date**

  October 08, 2024

- **Installation**

  [Installing Percona Operator for PostgreSQL](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/System-Requirements.html#installation-guidelines)

## Release Highlights

### Automated storage scaling

Starting from this release, the Operator is able to detect if the storage usage on the PVC reaches a certain threshold, and trigger the PVC resize. Such autoscaling needs the upstream [auto-growable disk](https://access.crunchydata.com/documentation/postgres-operator/latest/guides/autogrowable-disk) feature turned on when deploying the Operator. This is done via the `PGO_FEATURE_GATES` environment variable set in the `deploy/operator.yaml` manifest (or in the appropriate part of `deploy/bundle.yaml`):

```
- name: PGO_FEATURE_GATES
  value: "AutoGrowVolumes=true"
```

When the support for auto-growable disks is turned on, the `spec.instances[].dataVolumeClaimSpec.resources.limits.storage` Custom Resource option sets the maximum value available for the Operator to scale up.

See [official documentation](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/scaling-vertical.html#scale-storage) for more details and limitations of the feature.

### Major versions upgrade improvements

Major version upgrade, introduced in the Operator version 2.4.0 as a tech preview, had undergone some improvements. Now it is possible to upgrade from one PostgreSQL major version to another with custom images for the database cluster components (PostgreSQL, pgBouncer, and pgBackRest). The upgrade is still triggered by applying the YAML manifest with the information about the existing and desired major versions, which now includes image names. The resulting manifest may look as follows:

```
apiVersion: pgv2.percona.com/v2
kind: PerconaPGUpgrade
metadata:
  name: cluster1-15-to-16
spec:
  postgresClusterName: cluster1
  image: percona/percona-postgresql-operator:2.4.1-upgrade
  fromPostgresVersion: 15
  toPostgresVersion: 16
  toPostgresImage: percona/percona-postgresql-operator:2.5.0-ppg16.4-postgres
  toPgBouncerImage: percona/percona-postgresql-operator:2.5.0-ppg16.4-pgbouncer1.23.1
  toPgBackRestImage: percona/percona-postgresql-operator:2.5.0-ppg16.4-pgbackrest2.53-1
```

### Azure Kubernetes Service and Azure Blob Storage support

[Azure Kubernetes Service (AKS)](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/aks.html) is now an officially supported platform, so developers and vendors of the solutions based on the Azure platform can take advantage of the official support from Percona or just use officially certified Percona Operator for PostgreSQL images; also, [Azure Blob Storage can now be used for backups](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/backups-storage-azure.html).

## New features

- [K8SPG-227](https://jira.percona.com/browse/K8SPG-227) and [K8SPG-157](https://jira.percona.com/browse/K8SPG-157): Add support for the [Azure Kubernetes Service (AKS)](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/aks.html) platform and allow [using Azure Blob Storage](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/backups-storage-azure.html) for backups
- [K8SPG-244](https://jira.percona.com/browse/K8SPG-244): [Automated storage scaling](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/scaling-vertical.html#scale-storage) is now supported

## Improvements

- [K8SPG-630](https://jira.percona.com/browse/K8SPG-630): A new `backups.trackLatestRestorableTime` Custom Resource option allows to disable latest restorable time tracking for users who need reducing S3 API calls usage
- [K8SPG-605](https://jira.percona.com/browse/K8SPG-605) and [K8SPG-593](https://jira.percona.com/browse/K8SPG-593): Documentation now includes information about [upgrading the Operator via Helm](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/update-operator.html#upgrade-via-helm) and [using databaseInitSQL commands](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/initsql.html)
- [K8SPG-598](https://jira.percona.com/browse/K8SPG-598): Database major version upgrade now [supports custom images](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/update-db-major.html)
- [K8SPG-560](https://jira.percona.com/browse/K8SPG-560): A `pg-restore` Custom Resource is now automatically created at [bootstrapping a new cluster from an existing backup](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/backups-clone.html#make-a-full-data-clone)
- [K8SPG-555](https://jira.percona.com/browse/K8SPG-555): The Operator now creates separate Secret with CA certificate for each cluster
- [K8SPG-553](https://jira.percona.com/browse/K8SPG-553): Users can provide the Operator with their own [root CA certificate](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/tls-manual.html#generate-custom-certificates-for-the-operator-yourself)
- [K8SPG-454](https://jira.percona.com/browse/K8SPG-454): Cluster status obtained with `kubectl get pg` command is now “ready” not only when all Pods are ready, but also takes into account if all StatefulSets are up to date
- [K8SPG-577](https://jira.percona.com/browse/K8SPG-577): A new `pmm.querySource` Custom Resource option allows to set PMM query source

## Bugs Fixed

- [K8SPG-629](https://jira.percona.com/browse/K8SPG-629): Fix a bug where the Operator was not deleting backup Pods when cleaning outdated backups according to the retention policy
- [K8SPG-499](https://jira.percona.com/browse/K8SPG-499): Fix a bug where cluster was getting stuck in the init state if pgBackRest secret didn’t exist
- [K8SPG-588](https://jira.percona.com/browse/K8SPG-588): Fix a bug where the Operator didn’t stop WAL watcher if the namespace and/or cluster were deleted
- [K8SPG-644](https://jira.percona.com/browse/K8SPG-644): Fix a bug in the `pg-db` Helm chart which prevented from setting more than one Toleration

## Deprecation, Change, Rename and Removal

With the Operator versions prior to 2.5.0, [autogenerated TLS certificates](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/TLS.html) for all database clusters were based on the same generated root CA. Starting from 2.5.0, the Operator creates root CA on a per-cluster basis.

## Supported platforms

The Operator was developed and tested with PostgreSQL versions 12.20, 13.16, 14.13, 15.8, and 16.4. Other options may also work but have not been tested. The Operator 2.5.0 provides connection pooling based on pgBouncer 1.23.1 and high-availability implementation based on Patroni 3.3.2.

The following platforms were tested and are officially supported by the Operator 2.5.0:

- [Google Kubernetes Engine (GKE)](https://cloud.google.com/kubernetes-engine) 1.28 - 1.30
- [Amazon Elastic Container Service for Kubernetes (EKS)](https://aws.amazon.com) 1.28 - 1.30
- [OpenShift](https://www.redhat.com/en/technologies/cloud-computing/openshift) 4.13.46 - 4.16.7
- [Azure Kubernetes Service (AKS)](https://azure.microsoft.com/en-us/services/kubernetes-service/) 1.28 - 1.30
- [Minikube](https://github.com/kubernetes/minikube) 1.34.0 with Kubernetes 1.31.0

This list only includes the platforms that the Percona Operators are specifically tested on as part of the release process. Other Kubernetes flavors and versions depend on the backward compatibility offered by Kubernetes itself.
