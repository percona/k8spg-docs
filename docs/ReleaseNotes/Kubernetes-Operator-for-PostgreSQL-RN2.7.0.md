# Percona Operator for PostgreSQL 2.7.0 ({{date.2_7_0}})

[Get started with the Operator :material-arrow-right:](../quickstart.md){.md-button}

## **Release Highlights**

This release provides the following features and improvements:

### PMM3 support

The Operator is natively integrated with PMM 3, enabling you to monitor the health and performance of your Percona Distribution for PostgreSQL deployment and at the same time enjoy enhanced performance, new features, and improved security that PMM 3 provides.

Note that the Operator supports both PMM2 and PMM3. The decision on what PMM version is used depends on the authentication method you provide in the Operator configuration: PMM2 uses API keys while PMM3 uses service account token. If the Operator configuration contains both authentication methods with non-empty values, PMM3 takes the priority.

To use PMM, ensure that the PMM client image is compatible with the PMM Server version. Check [Percona certified images](image.md) for the correct client image.

For how to configure monitoring with PMM see the [documentation](monitoring-tutorial.md).

### Improved monitoring for clusters in multi-region or multi-namespace deployments in PMM

Now you can define a custom name for your clusters deployed in different data centers. This name helps Percona Management and Monitoring (PMM) Server to correctly recognize clusters as connected and monitor them as one deployment. Similarly, PMM Server identifies clusters deployed with the same names in different namespaces as separate ones and correctly displays performance metrics for you on dashboards.

To assign a custom name, define this configuration in the Custom Resource manifest for your cluster:

```yaml
spec:
  pmm:
    customClusterName: postgresql-cluster
```

### Added labels to identify the version of the Operator

Custom Resource Definition (CRD) is compatible with the last three Operator versions. To know which Operator version is attached to it, we've added labels to all Custom Resource Definitions. The labels help you identify the current Operator version and decide if you need to update the CRD.
To view the labels, run: `kubectl get crd perconapgclusters.pgv2.percona.com  --show-labels`.

### Grant users access to a public schema

Starting with PostgreSQL 15, a non-database owner cannot access the default `public` schema and cannot create tables in it. We have improved this behavior so that the Operator creates a user and a schema with the name matching the username for all databases listed for this user. This custom schema is set by default enabling you to work in the database right away.

You can explicitly grant access to a `public` schema for a non-superuser setting the `grantPublicSchemaAccess` option to `true`. This grants the user permission to create tables and update in the `public` schema of every database they own. If multiple users are granted access to the `public` schema in the same database, each user can only access the tables they have created themselves. If you want one user to access tables created by another user in the `public` schema, the owner of those tables must connect to PostgreSQL and explicitly grant the necessary privileges to the other user.

Superusers have access to the `public` schema for their databases by default.

## Improved troubleshooting with the ability to override Patroni configuration

You can now override Patroni configuration for the whole cluster as well as for an individual Pod. This gives you more control over the database and simplifies troubleshooting.

Also, you can redefine what method the Operator will use when it creates replica instances in your PostgreSQL cluster. For example, to force the Operator to use `pgbasebackup`, edit the `deploy/cr.yaml` manifest:

```yaml
patroni:
  createReplicaMethods:
    - basebackup
    - pgbackrest
```

Note that after you apply this configuration, the Operator updates the Patroni ConfigMap, but it doesn't apply this configuration to Patroni. You must manually reload the Patroni configuration of every database instance for it to come into force.

Read more about these troubleshooting methods in the [documentation](manage-manually.md#override-patroni-configuration)

## Changelog

### New features

* [K8SPG-615](https://perconadev.atlassian.net/browse/K8SPG-615) - Introduced a custom delay on the entrypoint of the backup pod. The backup process waits the defined time before connecting to the API server

* [K8SPG-708](https://perconadev.atlassian.net/browse/K8SPG-708), [K8SPG-663](https://perconadev.atlassian.net/browse/K8SPG-663)  - Added the sleep-forever feature to keep a database container running.

* [K8SPG-712](https://perconadev.atlassian.net/browse/K8SPG-712) - Added the ability to control every parameter supported by Patroni configuration.

* [K8SPG-725](https://perconadev.atlassian.net/browse/K8SPG-725) - Added the ability to configure resources for the repo-host container

* [K8SPG-719](https://perconadev.atlassian.net/browse/K8SPG-719) - Added support for PMM v3


### Improvements

* [K8SPG-571](https://perconadev.atlassian.net/browse/K8SPG-571) - Add ability to access to a public schema for a non-superuser custom user for every database listed for them. 

* [K8SPG-612](https://perconadev.atlassian.net/browse/K8SPG-612) - Use official `percona-pgbouncer` Docker image

* [K8SPG-613](https://perconadev.atlassian.net/browse/K8SPG-613) - Use official `percona-pgbackrest` Docker image

* [K8SPG-654](https://perconadev.atlassian.net/browse/K8SPG-654) - Added ability to add custom parameters in the Custom Resource and pass them to PMM.

* [K8SPG-675](https://perconadev.atlassian.net/browse/K8SPG-675) - Added ability to define resource requests for CPU and memory

* [K8SPG-704](https://perconadev.atlassian.net/browse/K8SPG-704) - Add the ability to configure  `create_replica_methods` for Patroni

* [K8SPG-710](https://perconadev.atlassian.net/browse/K8SPG-710) - Add the ability to disable backups

* [K8SPG-715](https://perconadev.atlassian.net/browse/K8SPG-715) - Improved custom-extensions e2e test by adding `pgvector` 

* [K8SPG-726](https://perconadev.atlassian.net/browse/K8SPG-726) - Added ability to define  security context for all sidecar containers

* [K8SPG-729](https://perconadev.atlassian.net/browse/K8SPG-729) - Added Labels for Custom Resource Definitions (CRD) to identify the Operator version attached to them

* [K8SPG-732](https://perconadev.atlassian.net/browse/K8SPG-732) - Enhanced readability of `pgbackrest debug logs` by printing log messages on separate lines

* [K8SPG-738](https://perconadev.atlassian.net/browse/K8SPG-738) - Added startup log to the Operator Pod to print commit hash, branch and build time

* [K8SPG-743](https://perconadev.atlassian.net/browse/K8SPG-743) - Disabled client-side rate limiting in the Kubernetes Go client to avoid throttling errors when managing multiple clusters with a single operator. This change leverages Kubernetes' server-side Priority and Fairness mechanisms introduced in v1.20 and later. (Thank you Joshua Sierles for contributing to this issue)

* [K8SPG-744](https://perconadev.atlassian.net/browse/K8SPG-744) - Improve Contributing guide  with the steps how to build the Operator for development purposes

* [K8SPG-717](https://perconadev.atlassian.net/browse/K8SPG-717), [K8SPG-750](https://perconadev.atlassian.net/browse/K8SPG-750) -  Added the ability to define a custom cluster name for pmm-admin component

* [K8SPG-753](https://perconadev.atlassian.net/browse/K8SPG-753) - Added the ability to enable `pg_stat_statements` instead of `pg_stat_monitor`

* [K8SPG-761](https://perconadev.atlassian.net/browse/K8SPG-761) - Add the ability to add concurrent reconciliation workers

## Bugs Fixed

* [K8SPG-532](https://perconadev.atlassian.net/browse/K8SPG-532) - Improved log visibility to include logs about missing data source to INFO logs

* [K8SPG-574](https://perconadev.atlassian.net/browse/K8SPG-574) - Added `pg_repack` to the list of built-in extensions in the Custom Resource

* [K8SPG-661](https://perconadev.atlassian.net/browse/K8SPG-661)  - Added documentation about replica reinitialization in the Operator

* [K8SPG-677](https://perconadev.atlassian.net/browse/K8SPG-677) - Made the `imagePullPolicy` in `pg-db` Helm chart configurable

* [K8SPG-680](https://perconadev.atlassian.net/browse/K8SPG-680) - Prevent scheduled backups to start until the volume expansion is completed with success.

* [K8SPG-698](https://perconadev.atlassian.net/browse/K8SPG-698) - Fixed the issue with `pgbackrest` service account not being created and reconciliation failing by creating the  StatefulSet for this service account first

* [K8SPG-703](https://perconadev.atlassian.net/browse/K8SPG-703) - Fixed the issue with the backup Pod being stuck in a running state due to running jobs being deleted because of the TTL expiration by adding an internal finalizer to keep the job running until it finishes

* [K8SPG-722](https://perconadev.atlassian.net/browse/K8SPG-722) - Documented the replica reinitialization behavior.

* [K8SPG-772](https://perconadev.atlassian.net/browse/K8SPG-772) - Fixed the issue with WAL watcher panicking if some backups have no `CompletedAt` status field by using `CreationTimestamp` as fallback.

* [K8SPG-782](https://perconadev.atlassian.net/browse/K8SPG-782) - Fixed the issue with crashing WALWatcher by assigning Patroni version to status when Patroni label is configured through the Custom resource option

* [K8SPG-785](https://perconadev.atlassian.net/browse/K8SPG-785) - Fixed PMM template in Helm chart (Thank you user Nik for reporting this issue)

* [K8SPG-792](https://perconadev.atlassian.net/browse/K8SPG-792) - Add the ability to configure and use images defined in environment variables when starting a cluster (Thank you Jakub Jaruszewski for reporting this issue)

* [K8SPG-799](https://perconadev.atlassian.net/browse/K8SPG-799) - Fixed teh issue with the cluster being blocked due to inability to pull the image fot the Patroni Version Detector Pod if imagePullSecrets in configured. The issue is fixed by respecting the configuration for the patroni version check pod. (Thank you Baptiste Balmon for reporting this issue)

* [K8SPG-804](https://perconadev.atlassian.net/browse/K8SPG-804) - Fixed an issue where outdated cluster state could cause a duplicate backup job to be created, blocking new backups. The issue was fixed by ensuring `reconcileManualBackup` fetches the latest postgrescluster state.

* [K8SPG-812](https://perconadev.atlassian.net/browse/K8SPG-812) - Fixed image in PerconaPGUpgrade example

## Deprecation, Change, Rename and Removal

* New repositories for `pgBouncer` and `pgBackRest`

   Now the Operator uses the official Percona Docker images for `pgBouncer` and `pgBackRest` components. Pay attention to the new image repositories when you [upgrade the Operator and the database](update.md). Check the [Percona certified images](images.md) for exact image names.


## Supported software

The Operator {{ release }} is developed, tested and based on:

--8<-- [start:software]

* PostgreSQL 13.21, 14.18, 15.13, 16.9, 17.5.2 as the database. Other versions may also work but have not been tested.
* pgBouncer 1.24.1 for connection pooling
* Patroni version 4.0.5 for high-availability
* PostGIS version 3.3.8

--8<-- [end:software]

## Supported platforms

Percona Operators are designed for compatibility with all [CNCF-certified :octicons-link-external-16:](https://www.cncf.io/training/certification/software-conformance/) Kubernetes distributions. 

Our release process includes targeted testing and validation on major cloud provider platforms and OpenShift, as detailed below for Operator version {{release}}:

--8<-- [start:platforms]

* [Google Kubernetes Engine (GKE) :octicons-link-external-16:](https://cloud.google.com/kubernetes-engine) 1.30 - 1.32
* [Amazon Elastic Container Service for Kubernetes (EKS) :octicons-link-external-16:](https://aws.amazon.com) 1.30 - 1.33
* [OpenShift :octicons-link-external-16:](https://www.redhat.com/en/technologies/cloud-computing/openshift) 4.15 - 4.19
* [Azure Kubernetes Service (AKS) :octicons-link-external-16:](https://azure.microsoft.com/en-us/services/kubernetes-service/) 1.30 - 1.33
* [Minikube :octicons-link-external-16:](https://github.com/kubernetes/minikube) 1.36.0 with Kubernetes v1.33.1

--8<-- [end:platforms]

This list only includes the platforms that the Percona Operators are specifically tested on as part of the release process. Other Kubernetes flavors and versions depend on the backward compatibility offered by Kubernetes itself.

## Percona certified images

Find Percona’s certified Docker images that you can use with the Percona Operator for PostgreSQL in the following table.

Images released with the Operator version {{release}}: 

--8<-- [start:images]

| Image                                                                | Digest                                                           |
|:---------------------------------------------------------------------|:-----------------------------------------------------------------|
| percona/percona-postgresql-operator:2.6.0 (x86_64)                   | fb1b6b08e986a21b30ce5e538c54e92e5fd978cd62abf17856c74582a237e931 |
| percona/percona-postgresql-operator:2.6.0 (ARM64)                    | 4e545bebaa66e43c1c0707bb576b4047ca5dd6fc0f4fb326b553cba744b337ae |
|percona/percona-postgresql-operator:2.6.0-ppg17.4-postgres           | 142ea1573c67fdb60a197352c576a1d01da247eee3b3fc0f09e86dd4c916cc82 |
| percona/percona-postgresql-operator:2.6.0-ppg17.2-postgres           | acb876c29ddcb8ca3d157a83e2b0e8410dabbd0c4c35257fa8f66a9f0b981fda |
| percona/percona-postgresql-operator:2.6.0-ppg16.8-postgres           | 7ecc5320ae341778140dd90e1e628ab3552f12cd4fb07e93070b034dc9e6c776 |
| percona/percona-postgresql-operator:2.6.0-ppg15.12-postgres          | db6d09dcb2e6f4c3a10de521fe0b008df0675741ee062fdbcaabfd4a466200d1 |
| percona/percona-postgresql-operator:2.6.0-ppg14.17-postgres          | 31dd06dd76df480da58638c1ae14cbff762b1057701ccc20af9bc86c264b4962 |
| percona/percona-postgresql-operator:2.6.0-ppg13.20-postgres          | 95f25de125cd43e825dea64be943e097459cfda09550877fbf460626913a2e9d |
| percona/percona-postgresql-operator:2.6.0-ppg17.4-postgres-gis3.3.8  | 836884826761a858d183616acff5c069fbad3a47e9014146a6acdfe2d40f6962 |
| percona/percona-postgresql-operator:2.6.0-ppg17.2-postgres-gis3.3.7  | 8bd0c645431cfebd1b365c05ba2e5748d81d00dbf5b76cf2f3f3a411ef1cb14e |
| percona/percona-postgresql-operator:2.6.0-ppg16.8-postgres-gis3.3.8  | 4787f0b40b25d14dc4e724dc97f76a3fe13b97a372437fe803cc2208dbcf102c |
| percona/percona-postgresql-operator:2.6.0-ppg15.12-postgres-gis3.3.8 | fed24afbf62ee384fe5cfdd1b8646ba7e5579aa500e9fc84be5467d66ca6d46b |
| percona/percona-postgresql-operator:2.6.0-ppg14.17-postgres-gis3.3.8 | e243d07702754adaee2cb789d03bc3a2ca142d9c7d93bfe871cb7b47323e8bdf |
| percona/percona-postgresql-operator:2.6.0-ppg13.20-postgres-gis3.3.8 | bb1095f5cd462e7d381fefe39ee1e12c9a1d11ba5a249d0aca065b1e5243efb7 |
| percona/percona-postgresql-operator:2.6.0-ppg17.4-pgbouncer1.24.0    | 01199912786772df11994ff7f4231a117bfc856a5c8fc3fb55e6d2f33c6d4230 |
| percona/percona-postgresql-operator:2.6.0-ppg17.2-pgbouncer1.23.1    | a51586295a2abc228470c0d73087a0de646cd7b58d0c6796c08719ad7635d89f |
| percona/percona-postgresql-operator:2.6.0-ppg16.8-pgbouncer1.24.0    | fbf8c89259d821df04b007f3e750d3f3ed902a9dd366bb0efe72ba3683974b99 |
| percona/percona-postgresql-operator:2.6.0-ppg15.12-pgbouncer1.24.0   | 9ef6204ebf626ee85d2a2afd405ee44ebb5e252bb1ac07ebaed44fa658bfb5f0 |
| percona/percona-postgresql-operator:2.6.0-ppg14.17-pgbouncer1.24.0   | 6ffc19f626b738b096635a0b1a2e4fbb28f800723759c58bd8491e9857b2fc19 |
| percona/percona-postgresql-operator:2.6.0-ppg13.20-pgbouncer1.24.0   | a1c25e9834fbc8ad58477fc47ef868ccf3c696bd488114efc8c7f61c66961356 |
| percona/percona-postgresql-operator:2.6.0-ppg17.4-pgbackrest2.54.2   | 6b4648e00f0cd187ef7d20542d8df93f0a4d2f79df3946343e57bce40ee119aa |
| percona/percona-postgresql-operator:2.6.0-ppg17.2-pgbackrest2.54.0   | a3641d58a49fe4f771f3638c9fa18c71dd2f9aba1054e5693d3756134676cb3e |
| percona/percona-postgresql-operator:2.6.0-ppg16.8-pgbackrest2.54.2   | eca4f0153fd75c87bb35e54e5358da458a502bcc7671a798ddf60f6a87246ba8 |
| percona/percona-postgresql-operator:2.6.0-ppg15.12-pgbackrest2.54.2  | 9d33160904b7862d03c1018e4bf80247ea175918b7b0b4d4907e175045ddf4d1 |
| percona/percona-postgresql-operator:2.6.0-ppg14.17-pgbackrest2.54.2  | 95e904ed80ee3f28519bdb7b0375d4c41421f80fc3631285e3a5cf2ed5a6e67a |
| percona/percona-postgresql-operator:2.6.0-ppg13.20-pgbackrest2.54.2  | 0d4978fdcd22eeec3e7773b11bd6cb20f6df246c3fb8ad73b85f672940b104bb |
| percona/pmm-client:2.44.0 (x86_64)                                   | 19a07dfa8c12a0554308cd11d7d38494ea02a14cfac6c051ce8ff254b7d0a4a7 |
| percona/pmm-client:2.44.0 (ARM64)                                    | 43a542f24bdbd11d0c363c1d5002244b0b4840961a8e219a56df1becad77b068 |

--8<-- [end:images]
