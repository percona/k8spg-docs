> For the complete documentation index, see [llms.txt](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/llms.txt).

# Percona Operator for PostgreSQL 2.3.0

- **Date**

  December 21, 2023

- **Installation**

  [Installing Percona Operator for PostgreSQL](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/System-Requirements.html#installation-guidelines)

## Release Highlights

### PostGIS support

Modern businesses heavily rely on location-based data to gain valuable insights and make data-driven decisions. However, integrating geospatial functionality into the existing database systems has often posed a challenge for enterprises. PostGIS, an open-source software extension for PostgreSQL, addresses this difficulty by equipping users with extensive geospatial operations for handling geographic data efficiently. Percona Operator now supports PostGIS, available through a separate container image. You can read more about PostGIS and how to use it with the Operator in our [documentation](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/postgis.html).

## OpenShift and PostgreSQL 16 support

The Operator [is now compatible](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/openshift.html) with the OpenShift platform empowering enterprise customers with seamless on-premise or cloud deployments on the platform of their choice. Also, PostgreSQL 16 was added to the range of supported database versions and is used by default starting with this release.

### Experimental support for custom PostgreSQL extensions

One of great features of PostgreSQL is support for [Extensions](https://www.postgresql.org/download/products/6-postgresql-extensions/) , which allow adding new functionality to the database on a plugin basis. Starting from this release, users can add custom PostgreSQL extensions dynamically, without the need to rebuild the container image (see [this HowTo](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/custom-extensions.html) on how to create and connect yours).

## New features

- [K8SPG-311](https://jira.percona.com/browse/K8SPG-311) and [K8SPG-389](https://jira.percona.com/browse/K8SPG-389): A new `loadBalancerSourceRanges` Custom Resource option allows to customize the range of IP addresses from which the load balancer should be reachable
- [K8SPG-375](https://jira.percona.com/browse/K8SPG-375): Experimental support for custom PostgreSQL extensions [was added](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/custom-extensions.html) to the Operator
- [K8SPG-391](https://jira.percona.com/browse/K8SPG-391): The Operator [is now compatible](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/openshift.html) with the OpenShift platform
- [K8SPG-434](https://jira.percona.com/browse/K8SPG-434): The Operator now supports Percona Distribution for PostgreSQL version 16 and uses it as default database version

## Improvements

- [K8SPG-413](https://jira.percona.com/browse/K8SPG-413): The Operator documentation now includes a [comptibility matrix](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/versions.html) for each Operator version, specifying exact versions of all core components as well as supported versions of the database and platforms
- [K8SPG-332](https://jira.percona.com/browse/K8SPG-332): Creating backups and [pausing the cluster](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/pause.html) do not interfere with each other: the Operator either postpones the pausing until the active backup ends, or postpones the scheduled backup on the paused cluster
- [K8SPG-370](https://jira.percona.com/browse/K8SPG-370): [Logging management](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/debug-logs.html) is now aligned with other Percona Operators, allowing to use structured logging and to control log level
- [K8SPG-372](https://jira.percona.com/browse/K8SPG-372): The multi-namespace (cluster-wide) mode of the Operator was improved, making it possible to customize the list of Kubernetes namespaces under the Operator’s control
- [K8SPG-400](https://jira.percona.com/browse/K8SPG-400): The documentation now explains how to allow application users to connect to a database cluster [without TLS](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/TLS.html) (for example, for testing or demonstration purposes)
- [K8SPG-410](https://jira.percona.com/browse/K8SPG-410): Scheduled backups now create `pg-backup` object to simplify backup management and tracking
- [K8SPG-416](https://jira.percona.com/browse/K8SPG-416): PostgreSQL custom configuration is now supported in the Helm chart
- [K8SPG-422](https://jira.percona.com/browse/K8SPG-422) and [K8SPG-447](https://jira.percona.com/browse/K8SPG-447): The user can now see backup type and status in the output of `kubectl get pg-backup` and `kubectl get pg-restore` commands
- [K8SPG-458](https://jira.percona.com/browse/K8SPG-458): Affinity configuration examples were added to the `default/cr.yaml` configuration file

## Bugs Fixed

- [K8SPG-435](https://jira.percona.com/browse/K8SPG-435): Fix a bug with insufficient size of /tmp filesystem which caused PostgreSQL Pods to be recreated every few days due to running out of free space on it
- [K8SPG-453](https://jira.percona.com/browse/K8SPG-453): Bug in `pg_stat_monitor` PostgreSQL extensions could hang PostgreSQL
- [K8SPG-279](https://jira.percona.com/browse/K8SPG-279): Fix regression which made the Operator to crash after creating a backup if there was no backups.pgbackrest.manual section in the Custom Resource
- [K8SPG-310](https://jira.percona.com/browse/K8SPG-310): Documentation didn’t explain how to apply pgBackRest `verifyTLS` option which can be used to explicitly enable or disable TLS verification for it
- [K8SPG-432](https://jira.percona.com/browse/K8SPG-432): Fix a bug due to which backup jobs and Pods were not deleted on deleting the backup object
- [K8SPG-442](https://jira.percona.com/browse/K8SPG-442): The Operator didn’t allow to append custom items to the PostgreSQL `shared_preload_libraries` option
- [K8SPG-443](https://jira.percona.com/browse/K8SPG-443): Fix a bug due to which only English locale was installed in the PostgreSQL image, missing other languages support
- [K8SPG-450](https://jira.percona.com/browse/K8SPG-450): Fix a bug which prevented PostgreSQL to initialize the database on Kubernetes working nodes with enabled huge memory pages if Pod resource limits didn’t allow using them
- [K8SPG-401](https://jira.percona.com/browse/K8SPG-401): Fix a bug which caused Operator crash if deployed with no `pmm` section in the `deploy/cr.yaml` configuration file

## Supported platforms

The Operator was developed and tested with PostgreSQL versions 12.17, 13.13, 14.10, 15.5, and 16.1. Other options may also work but have not been tested. The Operator 2.3.0 provides connection pooling based on pgBouncer 1.21.0 and high-availability implementation based on Patroni 3.1.0.

The following platforms were tested and are officially supported by the Operator 2.3.0:

- [Google Kubernetes Engine (GKE)](https://cloud.google.com/kubernetes-engine) 1.24 - 1.28
- [Amazon Elastic Container Service for Kubernetes (EKS)](https://aws.amazon.com) 1.24 - 1.28
- [OpenShift](https://www.redhat.com/en/technologies/cloud-computing/openshift) 4.11.55 - 4.14.6
- [Minikube](https://github.com/kubernetes/minikube) 1.32

This list only includes the platforms that the Percona Operators are specifically tested on as part of the release process. Other Kubernetes flavors and versions depend on the backward compatibility offered by Kubernetes itself.
