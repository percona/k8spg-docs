# Percona Operator for PostgreSQL 2.3.0

* **Date**

    December X, 2023

* **Installation**

    [Installing Percona Operator for PostgreSQL](../System-Requirements.md#installation-guidelines) 

## New features

* {{ k8spgjira(311) }}:  Add option to customize load balancer source ranges
* {{ k8spgjira(375) }}:  Add support for more extensions in the Operator
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

* {{ k8spgjira(435) }}:  Pod is recreated when /tmp is filled
* {{ k8spgjira(453) }}:  pg_stat_monitor hangs primary instance and it's impossible to disable it
* {{ k8spgjira(394) }}:  Failing to upgrade from operator v1 to v2 following the documentation
* {{ k8spgjira(279) }}:  Operator will crash after creating backup if there is no manual section in CR
* {{ k8spgjira(310) }}:  Invalid value: "boolean": spec.backups.pgbackrest.global.repo2-storage-verify-tls in body must be of type string: "boolean"
* {{ k8spgjira(407) }}:  Allow perconapgclusters/finalizers in role
* {{ k8spgjira(408) }}:  openshift in helm chart variable is wrong
* {{ k8spgjira(432) }}:  Delete backup job/pod when backup object is deleted
* {{ k8spgjira(433) }}:  Update cr examples in our docs
* {{ k8spgjira(442) }}:  Operator should respect the order of shared_preload_libraries
* {{ k8spgjira(443) }}:  Only english locale is installed, missing other languages support in Postgres
* {{ k8spgjira(450) }}:  Postgresql can't initialize the database because huge pages are enabled on k8s worker nodes
* {{ k8spgjira(456) }}:  [doc] Documentation wrong: Can't deploy PGO 2 in namespace-scope
* {{ k8spgjira(472) }}:  cannot re-enable builtin extensions after disabling
* {{ k8spgjira(482) }}:  pmm agent is failing in openshift with temp folder permission issue
* {{ k8spgjira(401) }}:  Operator crashes if pmm section is not specified

## Supported platforms

The Operator was developed and tested with PostgreSQL versions 12.14, 13.10, 14.7, and 15.2. Other options may also work but have not been tested. The Operator 2.2.0 provides connection pooling based on pgBouncer 1.18.0 and high-availability implementation based on Patroni 3.0.1.

The following platforms were tested and are officially supported by the Operator
2.2.0:

* [Google Kubernetes Engine (GKE)](https://cloud.google.com/kubernetes-engine) 1.23 - 1.26

* [Amazon Elastic Container Service for Kubernetes (EKS)](https://aws.amazon.com) 1.23 - 1.27

* [Minikube](https://github.com/kubernetes/minikube) 1.30.1 (based on Kubernetes 1.27)

This list only includes the platforms that the Percona Operators are specifically tested on as part of the release process. Other Kubernetes flavors and versions depend on the backward compatibility offered by Kubernetes itself.
