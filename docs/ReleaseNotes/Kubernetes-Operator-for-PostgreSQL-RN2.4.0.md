# Percona Operator for PostgreSQL 2.4.0

* **Date**

    June 26, 2024

* **Installation**

    [Installing Percona Operator for PostgreSQL](../System-Requirements.md#installation-guidelines) 

## Release Highlights

## Major versions upgrade (tech preview)

Starting from this release Operator users can automatically upgrade from one PostgreSQL major version to another. Upgrade is triggered by applying the yaml file with the information about the existing and desired major versions, with an example present in `deploy/upgrade.yaml`:

```yaml
apiVersion: pgv2.percona.com/v2
kind: PerconaPGUpgrade
metadata:
  name: cluster1-15-to-16
spec:
  postgresClusterName: cluster1
  image: perconalab/percona-postgresql-operator:main-upgrade
  fromPostgresVersion: 15
  toPostgresVersion: 16
```

After applying it as usual, by running `kubectl apply -f deploy/upgrade.yaml` command, the actual upgrade takes place as follows:

1. The cluster is paused for a while,
2. The cluster is specially annotated with `pgv2.percona.com/allow-upgrade`: `<PerconaPGUpgrade.Name>` annotation,
3. Jobs are created to migrate the data,
4. The cluster starts up after the upgrade finishes.

Check official documentation for [more details](../update.md#major-upgrades), including ones about tracking the upgrade process and side effects for users with custom extensions.

## Supporting PostgreSQL tablespaces 
    
Tablespaces allow DBAs to store a database on multiple file systems within the same server and to control where (on which file systems) specific parts of the database are stored. You can think about it as if you were giving names to your disk mounts and then using those names as additional parameters when creating database objects.

PostgreSQL supports this feature, allowing you to store data outside of the primary data directory. Tablespaces support was present in Percona Operator for PostgreSQL 1.x, and starting from this version, Percona Operator for PostgreSQL 2.x [is also able](../tablespaces.md) to bring this feature to your Kubernetes environment, when needed.

## Using cloud roles to authenticate on the object storage for backups

Percona Operator for PostgreSQL has introduced a new feature that allows users to authenticate to AWS S3 buckets via [IAM roles  :octicons-link-external-16:](https://kubernetes-on-aws.readthedocs.io/en/latest/user-guide/iam-roles.html). Now Operator [This enhancement](../backups-storage.md#iam) significantly improves security by eliminating the need to manage S3 access keys directly, while also streamlining the configuration process for easier backup and restore operations.


To use this feature, user should add annotations both to spec and backup subsections of Custom Resource:

```yaml
spec:
  crVersion: 2.3.1
  metadata:
    annotations:
      eks.amazonaws.com/role-arn: arn:aws:iam::1191:role/role-pgbackrest-access-s3-bucket
  ...
  backups:
    pgbackrest:
      image: percona/percona-postgresql-operator:2.3.1-ppg16-pgbackrest
      global:
        repo1-s3-key-type: web-id
```

## New features

* {{ k8spgjira(138) }}: Users are able now to use AWS [IAM role  :octicons-link-external-16:](https://kubernetes-on-aws.readthedocs.io/en/latest/user-guide/iam-roles.html) to provide access to the S3 bucket used for backups
* {{ k8spgjira(254) }}: Now Operator [automates](../update.md#major-upgrades) upgrading PostgreSQL major versions
* {{ k8spgjira(459) }}: PostgreSQL tablespaces [are now supported](../tablespaces.md) by the Operator
* {{ k8spgjira(479) }}: The upgrade path from PostgreSQL Operator version 1.x to 2.x have gained the possibility to [specify tolerations for data move jobs](../operator.md#datasourcevolumespgdatavolumepvcname), which can be useful in environments with dedicated Kubernetes worker nodes protected by taints
* {{ k8spgjira(503) }} and {{ k8spgjira(513) }}: It is now possible to specify [resources for the sidecar containers](../operator.md#instancescontainersresourceslimitscpu) of database instance Pods

## Improvements

* {{ k8spgjira(259) }}: Users can now change the default level for log messages for pgBackRest to simplify fixing backup and restore issues
* {{ k8spgjira(542) }}: Documentation now includes HowTo on [creating a disaster recovery cluster using streaming replication](../standby-streaming.md)
* {{ k8spgjira(506) }}: The `pg-backup` objects have now a new `backupName` status field, which [simplifies](../restore.md) obtain the backup name for restore

* {{ k8spgjira(514) }}: The new `securityContext` Custom Resource subsections allow to configure securityContext for PostgreSQL instances pgBouncer, and pgBackRest Pods
* {{ k8spgjira(518) }}: The `kubectl get pg-backup` command now shows Latest restorable time to make it easier to pick a point-in-time recovery target
* {{ k8spgjira(519) }}: The new `extensions.storage.endpoint` Custom Resource option allows to specify  a custom S3 object storage endpoint for installing custom extensions
* {{ k8spgjira(550) }}: The default size for `/tmp` mount point in PMM container was increased from 1.5G to 2G **REMOVE?**
* {{ k8spgjira(585) }}: The namespace field was added to the Operator and database Helm chart templates
* {{ k8spgjira(549) }}: 

## Bugs Fixed

* {{ k8spgjira(462) }}: Fixed a bug where backups could not start if a previous backup had the same name
* {{ k8spgjira(470) }}: Liveness and Readiness probes timeouts [are now configurable](../operator.md#patroinsyncperiodseconds) through Custom Resource
* {{ k8spgjira(559) }}: First full backup is falsely reported as incremental
* {{ k8spgjira(522) }}: Cluster is broken if PG_VERSION file is missing during upgrade from 2.2.0 to 2.3.1
* {{ k8spgjira(490) }}: Fix broken replication that occurred after the network loss of the master Pod with PostgreSQL 14 and older versions
* {{ k8spgjira(492) }}: Restore job created by PerconaPGRestore doesn't inherit .spec.instances[].tolerations
* {{ k8spgjira(502) }}: Fix a bug where backup jobs were not cleaned up after completion
* {{ k8spgjira(510) }}: Fix a bug where pausing the cluster immediately set its state to “paused” instead of “stopping” while Pods were still running
* {{ k8spgjira(531) }}: Fix a bug where scheduled backups did not work for a second database with the same name in cluster-wide mode
* {{ k8spgjira(535) }}: Fix a bug where the Operator crashed when attempting to run a backup with a non-existent repository
* {{ k8spgjira(543) }}: Fix a bug where applying a cr.yaml with an empty `spec.proxy` field caused the Operator to crash
* {{ k8spgjira(540) }}: Fixed a bug in the pg-db Helm chart readme where the key to set the backup secret was incorrectly specified (Thanks to Abhay Tiwari for contribution)
* {{ k8spgjira(547) }}: Fix dependency issue that made pgbackrest-repo container incompatible with pgBackRest 2.50, resulting in the older 2.48 version being used instead

## Supported platforms

The Operator was developed and tested with PostgreSQL versions 12.19, 13.15, 14.12, 15.7, and 16.3. Other options may also work but have not been tested. The Operator 2.4.0 provides connection pooling based on pgBouncer 1.22.1 and high-availability implementation based on Patroni 3.3.0.

The following platforms were tested and are officially supported by the Operator
2.4.0:

* [Google Kubernetes Engine (GKE) :octicons-link-external-16:](https://cloud.google.com/kubernetes-engine) 1.27 - 1.29
* [Amazon Elastic Container Service for Kubernetes (EKS) :octicons-link-external-16:](https://aws.amazon.com) 1.27 - 1.30
* [OpenShift :octicons-link-external-16:](https://www.redhat.com/en/technologies/cloud-computing/openshift) 4.12.59 - 4.15.18
* [Minikube :octicons-link-external-16:](https://github.com/kubernetes/minikube) 1.33.1

This list only includes the platforms that the Percona Operators are specifically tested on as part of the release process. Other Kubernetes flavors and versions depend on the backward compatibility offered by Kubernetes itself.
