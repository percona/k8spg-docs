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

* [K8SPG-571](https://perconadev.atlassian.net/browse/K8SPG-571) - Added the ability to access to a public schema for a non-superuser custom user for every database listed for them. 

* [K8SPG-612](https://perconadev.atlassian.net/browse/K8SPG-612) - Updated the `pgBouncer` image to use the official `percona-pgbouncer` Docker image

* [K8SPG-613](https://perconadev.atlassian.net/browse/K8SPG-613) - Updated the `pgBackRest` image to use the official `percona-pgbackrest` Docker image

* [K8SPG-654](https://perconadev.atlassian.net/browse/K8SPG-654) - Added the ability to add custom parameters in the Custom Resource and pass them to PMM.

* [K8SPG-675](https://perconadev.atlassian.net/browse/K8SPG-675) - Added the ability to define resource requests for CPU and memory

* [K8SPG-704](https://perconadev.atlassian.net/browse/K8SPG-704) - Added the ability to configure  `create_replica_methods` for Patroni

* [K8SPG-710](https://perconadev.atlassian.net/browse/K8SPG-710) - Added the ability to disable backups

* [K8SPG-715](https://perconadev.atlassian.net/browse/K8SPG-715) - Improved custom-extensions e2e test by adding `pgvector` 

* [K8SPG-726](https://perconadev.atlassian.net/browse/K8SPG-726) - Added ability to define  security context for all sidecar containers

* [K8SPG-729](https://perconadev.atlassian.net/browse/K8SPG-729) - Added Labels for Custom Resource Definitions (CRD) to identify the Operator version attached to them

* [K8SPG-732](https://perconadev.atlassian.net/browse/K8SPG-732) - Enhanced readability of `pgbackrest debug logs` by printing log messages on separate lines

* [K8SPG-738](https://perconadev.atlassian.net/browse/K8SPG-738) - Added startup log to the Operator Pod to print commit hash, branch and build time

* [K8SPG-743](https://perconadev.atlassian.net/browse/K8SPG-743) - Disabled client-side rate limiting in the Kubernetes Go client to avoid throttling errors when managing multiple clusters with a single operator. This change leverages Kubernetes' server-side Priority and Fairness mechanisms introduced in v1.20 and later. (Thank you Joshua Sierles for contributing to this issue)

* [K8SPG-744](https://perconadev.atlassian.net/browse/K8SPG-744) - Improved Contributing guide  with the steps how to build the Operator for development purposes

* [K8SPG-717](https://perconadev.atlassian.net/browse/K8SPG-717), [K8SPG-750](https://perconadev.atlassian.net/browse/K8SPG-750) -  Added the ability to define a custom cluster name for PMM for filtering

* [K8SPG-753](https://perconadev.atlassian.net/browse/K8SPG-753) - Added the ability to enable `pg_stat_statements` instead of `pg_stat_monitor`

* [K8SPG-761](https://perconadev.atlassian.net/browse/K8SPG-761) - Added the ability to add concurrent reconciliation workers

* [K*SPG-828](https://perconadev.atlassian.net/browse/K8SPG-828) - Added registry name to images due to Openshift 4.19 changes

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

* [K8SPG-799](https://perconadev.atlassian.net/browse/K8SPG-799) - Fixed the issue with the cluster being blocked due to inability to pull the image fot the Patroni Version Detector Pod if imagePullSecrets in configured. The issue is fixed by respecting the configuration for the patroni version check pod. (Thank you Baptiste Balmon for reporting this issue)

* [K8SPG-804](https://perconadev.atlassian.net/browse/K8SPG-804) - Fixed an issue where outdated cluster state could cause a duplicate backup job to be created, blocking new backups. The issue was fixed by ensuring `reconcileManualBackup` fetches the latest postgrescluster state.

* [K8SPG-812](https://perconadev.atlassian.net/browse/K8SPG-812) - Fixed image in PerconaPGUpgrade example

## Deprecation, Change, Rename and Removal

* New repositories for `pgBouncer` and `pgBackRest`

   Now the Operator uses the official Percona Docker images for `pgBouncer` and `pgBackRest` components. Pay attention to the new image repositories when you [upgrade the Operator and the database](update.md). Check the [Percona certified images](images.md) for exact image names.

* Changes in image pulling on OpenShift

   Starting with OpenShift version 4.19, the way Operator images are pulled has changed. Now the registry name must be specified for image paths to ensure the images are pulled successfully. 

   All Custom Resource manifests now include the registry name in image paths. This enables you to successfully install the Operator using the default manifests from Git repositories. If you upgrade the Operator and the database cluster via the command line interface, add the `docker.io` registry name to image paths for all components in the format:

   ```
   "docker.io/percona/percona-postgresql-operator:{{release}}-ppg{{postgresrecommended}}-postgres"
   ```

   Follow our [upgrade documentation](../update.md) for update guidelines.



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

| Image                                                                 | Digest                                                           |
|:----------------------------------------------------------------------|:-----------------------------------------------------------------|
| percona/percona-postgresql-operator:2.7.0 (x86_64)                    | f0910cd1330b9a001ae1b3d088b6f5878b7d0a590e2d70fecb139ebf958002c5 |
| percona/percona-postgresql-operator:2.7.0 (ARM64)                     | ed83c31ab74d7d00567620ab2de38d58e360a64544c0cde2fd82ce16868f1299 |
| percona/percona-postgresql-operator:2.7.0-ppg17.5.2-postgres           | cfb99ebeec00ab6efb4fca4a8da2b8c3b489dd792bd2f907848197ba09bc9553 |
| percona/percona-postgresql-operator:2.7.0-ppg16.9-postgres             | 842e81a9944d54ee589f055b2fd334d381cc0c84067ca553fca6326ff2d61782 |
| percona/percona-postgresql-operator:2.7.0-ppg15.13-postgres            | 9ed463f6739e0a6b48935e4b462cadbc0e77bc1e9911f05ff157433776d1b4cf |
| percona/percona-postgresql-operator:2.7.0-ppg14.18-postgres            | b421a05ea2f994c1e65bb9cd96f9295964d8b63eed9236a7838f318762142b16 |
| percona/percona-postgresql-operator:2.7.0-ppg13.21-postgres            | 1c6ab49d2a0c5aaa3e1c167715d1f101a69025fd2a8357f199610a78b8591fd7 |
| percona/percona-postgresql-operator:2.7.0-ppg17.5.2-postgres-gis3.3.8  | 860ccc180c1ac6be3c34c354d6ba9148b00330e183ba5913954e34d49c95d22f |
| percona/percona-postgresql-operator:2.7.0-ppg16.9-postgres-gis3.3.8    | da9039cab8412b41a90daa0de2e3511449ab9ac771199f5d1dfc4dd186eaf29d |
| percona/percona-postgresql-operator:2.7.0-ppg15.13-postgres-gis3.3.8   | 4b9c2e2d90bf16aae9f0f05d65732e0d3b788de7df028fd6a9edbb44d083797c |
| percona/percona-postgresql-operator:2.7.0-ppg14.18-postgres-gis3.3.8   | 5fe199ae8a5969654f75a7182803fb11a473f7bc1091fb8121fc6b13db535cfd |
| percona/percona-postgresql-operator:2.7.0-ppg13.21-postgres-gis3.3.8   | 541d669678869cc1de11657eb9cc7a6144637d62859add0469160367852c7d95 |
| percona/percona-pgbouncer:1.24.1                                       | 1bf7d3fd38b5fbe0dbb05addba7e28226dc432578c1f569a860529e88ad5b053 |
| percona/percona-pgbouncer:1.24.1 (ARM64)                               | 6d63e3bd41f35ff49febac33151ce893272b74bd982b140546f2360b9f30510b |
| percona/percona-pgbackrest:2.55.0                                      | 034a29072d912581dd93d5ccd5aca58500ece8694a633c8b08c2e4c5c4ac852c |
| percona/percona-pgbackrest:2.55.0 (ARM64)                              | 05e63f79d9029d3fc66c8a334509013b4c0298fde92be619d169a0bafe812e5e |
| percona/pmm-client:2.44.1                                               | 8b2eaddffd626f02a2d5318ffebc0c277fe8457da6083b8cfcada9b6e6168616 |
| percona/pmm-client:2.44.1 (ARM64)                                     | 337fecd4afdb3f6daf2caa2b341b9fe41d0418a0e4ec76980c7f29be9d08b5ea |
| percona/pmm-client:3.2.0                                               | 7b1d1798b6446d6c3d5e4005fd9c07be9f4be5859ac2fae908be387cf7b0f50c |
| percona/pmm-client:3.2.0 (ARM64)                                       | 1a36eb47e39dcd275c5ed62da8415c862e560933f48790bbf9b78f41cd3dfd10 |

--8<-- [end:images]
