# Percona Operator for PostgreSQL 2.4.0

* **Date**

    June 26, 2024

* **Installation**

    [Installing Percona Operator for PostgreSQL](../System-Requirements.md#installation-guidelines) 

## Release Highlights

## Supporting PostgreSQL tablespaces 
    
Tablespaces allow DBAs to store a database on multiple file systems within the same server and to control where (on which file systems) specific parts of the database are stored. You can think about it as if you were giving names to your disk mounts and then using those names as additional parameters when creating database objects.

PostgreSQL supports this feature, allowing you to store data outside of the primary data directory. Tablespaces support was present in Percona Operator for PostgreSQL 1.x, and starting from this version, Percona Operator for PostgreSQL 2.x [is also able](../tablespaces.md) to bring this feature to your Kubernetes environment, when needed.

## Using cloud roles to authenticate on the object storage for backups

Using AWS EC2 instances for backups makes it possible to automate access to AWS S3 buckets based on [IAM roles  :octicons-link-external-16:](https://kubernetes-on-aws.readthedocs.io/en/latest/user-guide/iam-roles.html) for Service Accounts with no need to specify the S3 credentials explicitly. Now Operator [allows to use this feature](backups-storage.md#iam).


use arn role to access S3 bucket (create/restore backups) 

Check how works if we add annotations both to spec and in backup 

To test it you need to add a special annotation to the Custom Resource:

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
* {{ k8spgjira(503) }} and {{ k8spgjira(513) }}: It is now possible to specify [resources for the side car containers](../operator.md#instancescontainersresourceslimitscpu) of DB instance pods

## Improvements

 {{ k8spgjira(259) }}: Users can now change the default loglevel for log messages from pgBackRest to simplify fixing backup/restore issues **ToDo: DOC missing**
* {{ k8spgjira(303) }}: A set of e2e tests was added to cover scheduled backups, users management, upgrade consistency, single-pod functioning and s3 backups based migration
* {{ k8spgjira(542) }}: Documentation now includes HowTo on [creating a DR cluster using streaming replication](../standby-streaming.md)
* {{ k8spgjira(506) }}: The `pg-backup` objects have now a new `backupName` status field, which [simplifies](../restore.md) obtain the backup name for restore

* {{ k8spgjira(514) }}: The new `securityContext` Custom Resource subsections allow to configure securityContext for PostgreSQL instances pgBouncer, and pgBackRest Pods
* {{ k8spgjira(518) }}: The `kubectl get pg-backup` command now shows Latest restorable time to make it easier to pick a point-in-time recovery target
* {{ k8spgjira(519) }}: The new `extensions.storage.endpoint` Custom Resource option allows to specify  a custom S3 object storage endpoint for installing custom extensions
* {{ k8spgjira(550) }}: The default size for `/tmp` mount point in PMM container was increased from 1.5G to 2G **REMOVE?**
* {{ k8spgjira(585) }}: The namespace field was added to the Operator and database Helm chart templates

## Bugs Fixed

* {{ k8spgjira(462) }}: Backup with the same name is stuck
* {{ k8spgjira(470) }}: Liveness and Readiness checks are not detecting postgresql hang
* {{ k8spgjira(512) }}: Steps described in the Changing the Primary documentation don't work and the server roles don't change.
* {{ k8spgjira(559) }}: First full backup is falsely reported as incremental
* {{ k8spgjira(522) }}: Cluster is broken if PG_VERSION file is missing during upgrade from 2.2.0 to 2.3.1
* {{ k8spgjira(490) }}: replication broken when master killed on older PG
* {{ k8spgjira(492) }}: Restore job created by PerconaPGRestore doesn't inherit .spec.instances[].tolerations
* {{ k8spgjira(502) }}: Backup jobs not being cleaned up since 2.3.1
* {{ k8spgjira(510) }}: Cluster state set to paused while pods are still running
* {{ k8spgjira(531) }}: Scheduled backups do not work for a second database in cluster-wide
* {{ k8spgjira(534) }}: use_slots defaults at false
* {{ k8spgjira(535) }}: When we try to run backup with non-existent repo operator crashes.
* {{ k8spgjira(540) }}: pg-db helm - issue with backups.pgbackrest.configuration key
* {{ k8spgjira(543) }}: operator crash loop due to nil pointer - pgbouncer
* {{ k8spgjira(547) }}: pgbackrest container can't use pgbackrest 2.50
* {{ k8spgjira(575) }}: Documentation is misleading in terms of enabling built-in extensions
* {{ k8spgjira(580) }}: Unable to tell which exact version an image provides
* {{ k8spgjira(582) }}: Documentation is incomplete
* {{ k8spgjira(583) }}: perconapgclusters hardcoded version was not updated

## Supported platforms

The Operator was developed and tested with PostgreSQL versions 12.19, 13.15, 14.12, 15.7, and 16.3. Other options may also work but have not been tested. The Operator 2.4.0 provides connection pooling based on pgBouncer 1.22.1 and high-availability implementation based on Patroni 3.3.0.

The following platforms were tested and are officially supported by the Operator
2.4.0:

* [Google Kubernetes Engine (GKE) :octicons-link-external-16:](https://cloud.google.com/kubernetes-engine) 1.27 - 1.29
* [Amazon Elastic Container Service for Kubernetes (EKS) :octicons-link-external-16:](https://aws.amazon.com) 1.27 - 1.30
* [OpenShift :octicons-link-external-16:](https://www.redhat.com/en/technologies/cloud-computing/openshift) 4.12.59 - 4.15.18
* [Minikube :octicons-link-external-16:](https://github.com/kubernetes/minikube) 1.33.1

This list only includes the platforms that the Percona Operators are specifically tested on as part of the release process. Other Kubernetes flavors and versions depend on the backward compatibility offered by Kubernetes itself.
