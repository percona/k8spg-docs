> For the complete documentation index, see [llms.txt](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/llms.txt).

# Percona Operator for PostgreSQL 2.4.0

- **Date**

  June 26, 2024

- **Installation**

  [Installing Percona Operator for PostgreSQL](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/System-Requirements.html#installation-guidelines)

## Release Highlights

## Major versions upgrade (tech preview)

Starting from this release Operator users can automatically upgrade from one PostgreSQL major version to another. Upgrade is triggered by applying the yaml file with the information about the existing and desired major versions, with an example present in `deploy/upgrade.yaml`:

```
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
1. The cluster is specially annotated with `pgv2.percona.com/allow-upgrade`: `<PerconaPGUpgrade.Name>` annotation,
1. Jobs are created to migrate the data,
1. The cluster starts up after the upgrade finishes.

Check official documentation for [more details](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/update-db-major.html), including ones about tracking the upgrade process and side effects for users with custom extensions.

## Supporting PostgreSQL tablespaces

Tablespaces allow DBAs to store a database on multiple file systems within the same server and to control where (on which file systems) specific parts of the database are stored. You can think about it as if you were giving names to your disk mounts and then using those names as additional parameters when creating database objects.

PostgreSQL supports this feature, allowing you to store data outside of the primary data directory. Tablespaces support was present in Percona Operator for PostgreSQL 1.x, and starting from this version, Percona Operator for PostgreSQL 2.x [can also bring](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/tablespaces.html) this feature to your Kubernetes environment, when needed.

## Using cloud roles to authenticate on the object storage for backups

Percona Operator for PostgreSQL has introduced a new feature that allows users to authenticate to AWS S3 buckets via [IAM roles](https://kubernetes-on-aws.readthedocs.io/en/latest/user-guide/iam-roles.html) . [This enhancement](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/backups-storage-s3.html#__tabbed_1_2) significantly improves security by eliminating the need to manage S3 access keys directly, while also streamlining the configuration process for easier backup and restore operations.

To use this feature, add annotation to the `spec` part of the Custom Resource and also add pgBackRest custom configuration option to the `backups` subsection:

```
spec:
  crVersion: 2.4.0
  metadata:
    annotations:
      eks.amazonaws.com/role-arn: arn:aws:iam::1191:role/role-pgbackrest-access-s3-bucket
  ...
  backups:
    pgbackrest:
      image: percona/percona-postgresql-operator:2.4.0-ppg16-pgbackrest
      global:
        repo1-s3-key-type: web-id
        ...
```

## New features

- [K8SPG-138](https://jira.percona.com/browse/K8SPG-138): Users are now able to use AWS [IAM role](https://kubernetes-on-aws.readthedocs.io/en/latest/user-guide/iam-roles.html) to provide access to the S3 bucket used for backups
- [K8SPG-254](https://jira.percona.com/browse/K8SPG-254): Now the Operator [automates](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/update-db-major.html) upgrading PostgreSQL major versions
- [K8SPG-459](https://jira.percona.com/browse/K8SPG-459): PostgreSQL tablespaces [are now supported](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/tablespaces.html) by the Operator
- [K8SPG-479](https://jira.percona.com/browse/K8SPG-479) and [K8SPG-492](https://jira.percona.com/browse/K8SPG-492): It is now possible to specify tolerations for the [backup restore jobs](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/operator.html#backupspgbackrestrestoretolerationseffect) as well as for the [data move jobs](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/operator.html#datasourcepostgresclustertolerationseffect) created when the Operator 1.x is upgraded to 2.x; this is useful in environments with dedicated Kubernetes worker nodes protected by taints
- [K8SPG-503](https://jira.percona.com/browse/K8SPG-503) and [K8SPG-513](https://jira.percona.com/browse/K8SPG-513): It is now possible to specify [resources for the sidecar containers](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/operator.html#instancescontainersreplicacertcopyresourceslimitscpu) of database instance Pods

## Improvements

- [K8SPG-259](https://jira.percona.com/browse/K8SPG-259): Users can now change the default level for log messages for pgBackRest to simplify fixing backup and restore issues
- [K8SPG-542](https://jira.percona.com/browse/K8SPG-542): Documentation now includes HowTo on [creating a disaster recovery cluster using streaming replication](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/standby-streaming.html)
- [K8SPG-506](https://jira.percona.com/browse/K8SPG-506): The `pg-backup` objects now have a new `backupName` status field, which allows users to [obtain the backup](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/backups-restore-inplace.html#restore-from-a-specific-backup) name for restore simpler
- [K8SPG-514](https://jira.percona.com/browse/K8SPG-514): The new `securityContext` Custom Resource subsections allow to configure securityContext for PostgreSQL instances, pgBouncer, and pgBackRest Pods
- [K8SPG-518](https://jira.percona.com/browse/K8SPG-518): The `kubectl get pg-backup` command now shows the latest restorable time to make it easier to pick a point-in-time recovery target
- [K8SPG-519](https://jira.percona.com/browse/K8SPG-519): The new `extensions.storage.endpoint` Custom Resource option allows specifying a custom S3 object storage endpoint for installing custom extensions
- [K8SPG-549](https://jira.percona.com/browse/K8SPG-549): It is now possible to expose replica nodes through a separate Service, useful if you want to balance the load and separate reads and writes traffic
- [K8SPG-550](https://jira.percona.com/browse/K8SPG-550): The default size for `/tmp` mount point in PMM container was increased from 1.5G to 2G
- [K8SPG-585](https://jira.percona.com/browse/K8SPG-585): The namespace field was added to the Operator and database Helm chart templates

## Bugs Fixed

- [K8SPG-462](https://jira.percona.com/browse/K8SPG-462): Fixed a bug where backups could not start if a previous backup had the same name
- [K8SPG-470](https://jira.percona.com/browse/K8SPG-470): Liveness and Readiness probes timeouts [are now configurable](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/operator.html#patronisyncperiodseconds) through Custom Resource
- [K8SPG-559](https://jira.percona.com/browse/K8SPG-559): Fix a bug where the first full backup was incorrectly marked as incremental in the status field
- [K8SPG-490](https://jira.percona.com/browse/K8SPG-490): Fixed broken replication that occurred after the network loss of the primary Pod with PostgreSQL 14 and older versions
- [K8SPG-502](https://jira.percona.com/browse/K8SPG-502): Fix a bug where backup jobs were not cleaned up after completion
- [K8SPG-510](https://jira.percona.com/browse/K8SPG-510): Fix a bug where pausing the cluster immediately set its state to “paused” instead of “stopping” while Pods were still running
- [K8SPG-531](https://jira.percona.com/browse/K8SPG-531): Fix a bug where scheduled backups did not work for a second database with the same name in cluster-wide mode
- [K8SPG-535](https://jira.percona.com/browse/K8SPG-535): Fix a bug where the Operator crashed when attempting to run a backup with a non-existent repository
- [K8SPG-540](https://jira.percona.com/browse/K8SPG-540): Fix a bug in the pg-db Helm chart readme where the key to set the backup secret was incorrectly specified (Thanks to Abhay Tiwari for contribution)
- [K8SPG-543](https://jira.percona.com/browse/K8SPG-543): Fix a bug where applying a cr.yaml file with an empty `spec.proxy` field caused the Operator to crash
- [K8SPG-547](https://jira.percona.com/browse/K8SPG-547): Fix dependency issue that made pgbackrest-repo container incompatible with pgBackRest 2.50, resulting in the older 2.48 version being used instead

## Deprecation and removal

- The `plpythonu` extension was removed from the list of built-in PostgreSQL extensions; users who still need it can enable it for their databases via [custom extensions functionality](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/custom-extensions.html)

## Supported platforms

The Operator was developed and tested with PostgreSQL versions 12.19, 13.15, 14.12, 15.7, and 16.3. Other options may also work but have not been tested. The Operator 2.4.0 provides connection pooling based on pgBouncer 1.22.1 and high-availability implementation based on Patroni 3.3.0.

The following platforms were tested and are officially supported by the Operator 2.4.0:

- [Google Kubernetes Engine (GKE)](https://cloud.google.com/kubernetes-engine) 1.27 - 1.29
- [Amazon Elastic Container Service for Kubernetes (EKS)](https://aws.amazon.com) 1.27 - 1.30
- [OpenShift](https://www.redhat.com/en/technologies/cloud-computing/openshift) 4.12.59 - 4.15.18
- [Minikube](https://github.com/kubernetes/minikube) 1.33.1

This list only includes the platforms that the Percona Operators are specifically tested on as part of the release process. Other Kubernetes flavors and versions depend on the backward compatibility offered by Kubernetes itself.
