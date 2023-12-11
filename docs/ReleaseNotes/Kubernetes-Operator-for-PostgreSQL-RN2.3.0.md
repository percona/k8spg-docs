# Percona Operator for PostgreSQL 2.3.0

* **Date**

    December X, 2023

* **Installation**

    [Installing Percona Operator for PostgreSQL](../System-Requirements.md#installation-guidelines) 

## Release Highlights

### Support for custom PostgreSQL extensions

One of great features of PostgreSQL is support for [Extensions](https://www.postgresql.org/download/products/6-postgresql-extensions/), which allow adding new functionality to the database on a plugin basis. Until now, the Operator used some built-in extensions with Percona Distribution for PostgreSQL, for example, the one used to provide valuable metrics to Percona Monitoring and Management (PMM). Starting from this release, adding custom PostgreSQL extensions is available for the end users (see [this HowTo](../extensions.md) on how to create and connect yours). Also this functionality provides fine more control on built-in extensions, allowing to enable or disable them via the Custom Resource.

## New features

* {{ k8spgjira(311) }}:  A new `loadBalancerSourceRanges` Custom Resource option allows to customize the range of IP addresses from which the load balancer should be reachable
* {{ k8spgjira(375) }}:  Support for custom PostgreSQL extensions [was added](../extensions.md) to the Operator
* {{ k8spgjira(391) }}:  The Operator [is now compatible](../openshift.md) with the OpenShift platform
* {{ k8spgjira(434) }}:  The Operator now supports Percona Distribution for PostgreSQL version 16 and uses it as default database version

## Improvements

* {{ k8spgjira(425) }}:  Asynchronous archiving to prevent "was not archived before 60000ms timeout" error
* {{ k8spgjira(413) }}:  Need essential comptibility and feature Matrix for each Operator version which is currently supported
* {{ k8spgjira(332) }}:  Operators' action on pause during an initial running backup
* {{ k8spgjira(370) }}:  Align logging management with other operators
* {{ k8spgjira(372) }}:  Cluster-wide and namespace list
* {{ k8spgjira(389) }}:  Provide loadBalancerSourceRanges for LoadBalancer
* {{ k8spgjira(400) }}:  Allow to connect with application user without TLS
* {{ k8spgjira(410) }}:  Add pg-backup CRs for scheduled backups
* {{ k8spgjira(411) }}:  Add Destination to the PerconaPGBackupStatus
* {{ k8spgjira(416) }}:  pg_hba customization - support in helm chart
* {{ k8spgjira(417) }}:  Document restore procedures for each possible case
* {{ k8spgjira(419) }}:  Add example for add/updating pg_hba conf entries in Pg operator doc
* {{ k8spgjira(422) }}:  PG Backup Status object to provide information on type of backup
* {{ k8spgjira(430) }}:  Standardize the labels used similar to other percona operators
* {{ k8spgjira(438) }}:  Update operator documentation about restores
* {{ k8spgjira(447) }}:  Add CLUSTER, STATUS and COMPLETED fields for PerconaPGRestore
* {{ k8spgjira(455) }}:  All annotations should be converted to Crunchy API group
* {{ k8spgjira(458) }}:  Configure affinity in default cr.yaml
* {{ k8spgjira(465) }}:  Need documentation on how to create certificates for PG Operator 2.x
* {{ k8spgjira(414) }}:  Add pmm-client upgrade steps in Kubernetes-based environment.

## Bugs Fixed

* {{ k8spgjira(435) }}:  Fix a bug with insufficient size of /tmp fliesystem which caused PostgreSQL Pods to be recreated every few days due to raning out of free space on it
* {{ k8spgjira(453) }}:  Bug in `pg_stat_monitor` PostgreSQL extensions could hang PostgreSQL
* {{ k8spgjira(279) }}:  Fix regression which made the Operator to crash after creating a backup if there was no backups.pgbackrest.manual section in the Custom Resource
* {{ k8spgjira(310) }}:  Documentation didn't explain how to apply  enables TLS verification for pgBackRest `verifyTLS` option which can be used to explicitly enable or disable TLS verification for it
* {{ k8spgjira(432) }}:  Fix a bug due to which backup jobs and Pods were not deleted on deleting the backup object
* {{ k8spgjira(442) }}:  The Operator didn't allow to append custom items to the PostgreSQL shared_preload_libraries option
* {{ k8spgjira(443) }}:  Fix a bug due to which only English locale was installed in the PostgreSQL image, missing other languages support
* {{ k8spgjira(450) }}:  Fix a bug which prevented PostgreSQL to initialize the database on Kubernetes working nodes with enabled huge memory pages id Pod resource limits didn't allow using them
* {{ k8spgjira(401) }}:  Fix a bug which caused Operator crash if deployed with no `pmm` section in the `deploy/cr.yaml` configuration file

## Supported platforms

The Operator was developed and tested with PostgreSQL versions 12.14, 13.10, 14.7, and 15.2. Other options may also work but have not been tested. The Operator 2.2.0 provides connection pooling based on pgBouncer 1.18.0 and high-availability implementation based on Patroni 3.0.1.

The following platforms were tested and are officially supported by the Operator
2.2.0:

* [Google Kubernetes Engine (GKE)](https://cloud.google.com/kubernetes-engine) 1.23 - 1.26

* [Amazon Elastic Container Service for Kubernetes (EKS)](https://aws.amazon.com) 1.23 - 1.27

* [Minikube](https://github.com/kubernetes/minikube) 1.30.1 (based on Kubernetes 1.27)

This list only includes the platforms that the Percona Operators are specifically tested on as part of the release process. Other Kubernetes flavors and versions depend on the backward compatibility offered by Kubernetes itself.
