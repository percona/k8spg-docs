# Percona Operator for PostgreSQL 2.4.0

* **Date**

    June 24, 2024

* **Installation**

    [Installing Percona Operator for PostgreSQL](../System-Requirements.md#installation-guidelines) 

## Release Highlights


## New features

K8SPG-138 Allow using cloud roles to authenticate on the object storage
K8SPG-254 Add support for major version upgrade
K8SPG-459 Allow configuring tablespace volumes
K8SPG-479 PostgreSQL operator upgrade 1.x to 2.x ability to specify tolerations for data move jobs
K8SPG-503 Provide option to specify resources for the side car containers of DB instance pods

## Improvements

* {{ k8spgjira(175) }}:  Provide protection from standby cluster promotion when the old primary is active
K8SPG-259 Change the default loglevel from pgbackrest
K8SPG-303 Add e2e tests
K8SPG-542 Create documentation on how to create a DR cluster using streaming replication
K8SPG-539 Steps for setting up Streaming replication for DR cluster.
K8SPG-506 Add backup name from 'pgbackrest info' output into pg-backup object
K8SPG-508 mprove bundle generation
K8SPG-513 pgbouncer-config container in pgbouncer pods are killed by OOM and there is no way to control the Resource / Limits
K8SPG-514 Provide ability to add securitycontext for all the pods managed with the operator
K8SPG-518 Provide the latest transaction information
K8SPG-519 Add support for endpointUrl for customExtensions
K8SPG-438 Update operator documentation about restores
K8SPG-550 Increase default /tmp size for PMM container
K8SPG-585 Helm - add namespace reference to templates

## Bugs Fixed

K8SPG-462 Backup with the same name is stuck
K8SPG-470 Liveness and Readiness checks are not detecting postgresql hang
K8SPG-512 Steps described in the Changing the Primary documentation don't work and the server roles don't change.
K8SPG-559 First full backup is falsely reported as incremental
K8SPG-522 Cluster is broken if PG_VERSION file is missing during upgrade from 2.2.0 to 2.3.1
K8SPG-490 replication broken when master killed on older PG
K8SPG-492 Restore job created by PerconaPGRestore doesn't inherit .spec.instances[].tolerations
K8SPG-502 Backup jobs not being cleaned up since 2.3.1
K8SPG-510 Cluster state set to paused while pods are still running
K8SPG-531 Scheduled backups do not work for a second database in cluster-wide
K8SPG-534 use_slots defaults at false
K8SPG-535 When we try to run backup with non-existent repo operator crashes.
K8SPG-540 pg-db helm - issue with backups.pgbackrest.configuration key
K8SPG-543 operator crash loop due to nil pointer - pgbouncer
K8SPG-547 pgbackrest container can't use pgbackrest 2.50
K8SPG-575 Documentation is misleading in terms of enabling built-in extensions
K8SPG-580 Unable to tell which exact version an image provides
K8SPG-582 Documentation is incomplete
K8SPG-583 perconapgclusters hardcoded version was not updated

## Supported platforms

The Operator was developed and tested with PostgreSQL versions 12.17, 13.13, 14.10, 15.5, and 16.1. Other options may also work but have not been tested. The Operator 2.3.0 provides connection pooling based on pgBouncer 1.21.0 and high-availability implementation based on Patroni 3.1.0.

The following platforms were tested and are officially supported by the Operator
2.4.0:

* [Google Kubernetes Engine (GKE) :octicons-link-external-16:](https://cloud.google.com/kubernetes-engine) 1.24 - 1.28
* [Amazon Elastic Container Service for Kubernetes (EKS) :octicons-link-external-16:](https://aws.amazon.com) 1.24 - 1.28
* [OpenShift :octicons-link-external-16:](https://www.redhat.com/en/technologies/cloud-computing/openshift) 4.11.55 - 4.14.6
* [Minikube :octicons-link-external-16:](https://github.com/kubernetes/minikube) 1.32

This list only includes the platforms that the Percona Operators are specifically tested on as part of the release process. Other Kubernetes flavors and versions depend on the backward compatibility offered by Kubernetes itself.
