# Percona Operator for PostgreSQL 2.4.0

* **Date**

    June 24, 2024

* **Installation**

    [Installing Percona Operator for PostgreSQL](../System-Requirements.md#installation-guidelines) 

## Release Highlights

## Supporting PostgreSQL tablespaces 
    
Tablespaces allow DBAs to store a database on multiple file systems within the same server and to control where (on which file systems) specific parts of the database are stored. You can think about it as if you were giving names to your disk mounts and then using those names as additional parameters when creating database objects.

PostgreSQL supports this feature, allowing you to store data outside of the primary data directory. Tablespaces support was present in Percona Operator for PostgreSQL 1.x, and starting from this version, Percona Operator for PostgreSQL 2.x [is also able](../tablespaces.md) to bring this feature to your Kubernetes environment, when needed.


## New features

* {{ k8spgjira(138) }}: Allow using cloud roles to authenticate on the object storage
* {{ k8spgjira(254) }}: Now Operator [automates](../update.md#major-upgrades) upgrading PostgreSQL major versions support for major version upgrade
* {{ k8spgjira(459) }}: PostgreSQL tablespaces [are now supported](../tablespaces.md) by the Operator
* {{ k8spgjira(479) }}: PostgreSQL operator upgrade 1.x to 2.x ability to specify tolerations for data move jobs
* {{ k8spgjira(503) }}: It is now possible to specify resources for the side car containers of DB instance pods

## Improvements

* {{ k8spgjira(175) }}: Provide protection from standby cluster promotion when the old primary is active
* {{ k8spgjira(259) }}: Change the default loglevel from pgbackrest
* {{ k8spgjira(303) }}: Add e2e tests
* {{ k8spgjira(542) }}: Create documentation on how to create a DR cluster using streaming replication
* {{ k8spgjira(539) }}: Steps for setting up Streaming replication for DR cluster.
* {{ k8spgjira(506) }}: Add backup name from 'pgbackrest info' output into pg-backup object
* {{ k8spgjira(508) }}: mprove bundle generation
* {{ k8spgjira(513) }}: pgbouncer-config container in pgbouncer pods are killed by OOM and there is no way to control the Resource / Limits
* {{ k8spgjira(514) }}: Provide ability to add securitycontext for all the pods managed with the operator
* {{ k8spgjira(518) }}: Provide the latest transaction information
* {{ k8spgjira(519) }}: Add support for endpointUrl for customExtensions
* {{ k8spgjira(438) }}: Update operator documentation about restores
* {{ k8spgjira(550) }}: Increase default /tmp size for PMM container
* {{ k8spgjira(585) }}: Helm - add namespace reference to templates

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
