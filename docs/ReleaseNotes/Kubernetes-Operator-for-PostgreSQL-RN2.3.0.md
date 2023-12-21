# Percona Operator for PostgreSQL 2.3.0

* **Date**

    December 21, 2023

* **Installation**

    [Installing Percona Operator for PostgreSQL](../System-Requirements.md#installation-guidelines) 

## Release Highlights

### PostGIS support

Modern businesses heavily rely on location-based data to gain valuable insights and make data-driven decisions. However, integrating geospatial functionality into the existing database systems has often posed a challenge for enterprises. PostGIS, an open-source software extension for PostgreSQL, addresses this difficulty by equipping users with extensive geospatial operations for handling geographic data efficiently. Percona Operator now supports PostGIS, available through a separate container image. You can read more about PostGIS and how to use it with the Operator in our [documentation](../postgis.md).

## OpenShift and PostgreSQL 16 support

The Operator [is now compatible](../openshift.md) with the OpenShift platform empowering enterprise customers with seamless on-premise or cloud deployments on the platform of their choice. Also, PostgreSQL 16 was added to the range of supported database versions and is used by default starting with this release.

### Experimental support for custom PostgreSQL extensions

One of great features of PostgreSQL is support for [Extensions](https://www.postgresql.org/download/products/6-postgresql-extensions/), which allow adding new functionality to the database on a plugin basis. Starting from this release, users can add custom PostgreSQL extensions dynamically, without the need to rebuild the container image (see [this HowTo](../custom-extensions.md) on how to create and connect yours). 


## New features

* {{ k8spgjira(311) }} and {{ k8spgjira(389) }}:  A new `loadBalancerSourceRanges` Custom Resource option allows to customize the range of IP addresses from which the load balancer should be reachable
* {{ k8spgjira(375) }}:  Experimental support for custom PostgreSQL extensions [was added](../custom-extensions.md) to the Operator
* {{ k8spgjira(391) }}:  The Operator [is now compatible](../openshift.md) with the OpenShift platform
* {{ k8spgjira(434) }}:  The Operator now supports Percona Distribution for PostgreSQL version 16 and uses it as default database version

## Improvements

* {{ k8spgjira(413) }}:  The Operator documentation now includes a [comptibility matrix](../versions.md) for each Operator version, specifying exact versions of all core components as well as supported versions of the database and platforms
* {{ k8spgjira(332) }}:  Creating backups and [pausing the cluster](../pause.md) do not interfere with each other: the Operator either postpones the pausing until the active backup ends, or postpones the scheduled backup on the paused cluster
* {{ k8spgjira(370) }}:  [Logging management](../debug-logs.md) is now aligned with other Percona Operators, allowing to use structured logging and to control log level
* {{ k8spgjira(372) }}:  The multi-namespace (cluster-wide) mode of the Operator was improved, making it possible to customize the list of Kubernetes namespaces under the Operator's control
* {{ k8spgjira(400) }}:  The documentation now explains how to allow application users to connect to a database cluster [without TLS](../TLS.md#connect-to-the-database-cluster-without-tls) (for example, for testing or demonstration purposes)
* {{ k8spgjira(410) }}:  Scheduled backups now create `pg-backup` object to simplify backup management and tracking
* {{ k8spgjira(416) }}:   PostgreSQL custom configuration is now supported in the Helm chart
* {{ k8spgjira(422) }} and {{ k8spgjira(447) }}: The user can now see backup type and status in the output of `kubectl get pg-backup` and `kubectl get pg-restore` commands
* {{ k8spgjira(458) }}:  Affinity configuration examples were added to the `default/cr.yaml` configuration file

## Bugs Fixed

* {{ k8spgjira(435) }}:  Fix a bug with insufficient size of /tmp filesystem which caused PostgreSQL Pods to be recreated every few days due to running out of free space on it
* {{ k8spgjira(453) }}:  Bug in `pg_stat_monitor` PostgreSQL extensions could hang PostgreSQL
* {{ k8spgjira(279) }}:  Fix regression which made the Operator to crash after creating a backup if there was no backups.pgbackrest.manual section in the Custom Resource
* {{ k8spgjira(310) }}:  Documentation didn't explain how to apply pgBackRest `verifyTLS` option which can be used to explicitly enable or disable TLS verification for it
* {{ k8spgjira(432) }}:  Fix a bug due to which backup jobs and Pods were not deleted on deleting the backup object
* {{ k8spgjira(442) }}:  The Operator didn’t allow to append custom items to the PostgreSQL `shared_preload_libraries` option
* {{ k8spgjira(443) }}:  Fix a bug due to which only English locale was installed in the PostgreSQL image, missing other languages support
* {{ k8spgjira(450) }}:  Fix a bug which prevented PostgreSQL to initialize the database on Kubernetes working nodes with enabled huge memory pages if Pod resource limits didn’t allow using them
* {{ k8spgjira(401) }}:  Fix a bug which caused Operator crash if deployed with no `pmm` section in the `deploy/cr.yaml` configuration file

## Supported platforms

The Operator was developed and tested with PostgreSQL versions 12.17, 13.13, 14.10, 15.5, and 16.1. Other options may also work but have not been tested. The Operator 2.3.0 provides connection pooling based on pgBouncer 1.21.0 and high-availability implementation based on Patroni 3.1.0.

The following platforms were tested and are officially supported by the Operator
2.3.0:

* [Google Kubernetes Engine (GKE)](https://cloud.google.com/kubernetes-engine) 1.24 - 1.28
* [Amazon Elastic Container Service for Kubernetes (EKS)](https://aws.amazon.com) 1.24 - 1.28
* [OpenShift](https://www.redhat.com/en/technologies/cloud-computing/openshift) 4.11.55 - 4.14.6
* [Minikube](https://github.com/kubernetes/minikube) 1.32

This list only includes the platforms that the Percona Operators are specifically tested on as part of the release process. Other Kubernetes flavors and versions depend on the backward compatibility offered by Kubernetes itself.
