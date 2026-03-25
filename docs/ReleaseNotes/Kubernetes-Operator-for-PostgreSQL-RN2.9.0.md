# Percona Operator for PostgreSQL 2.9.0 ({{date.2_9_0}})

[Get started with the Operator :material-arrow-right:](../quickstart.md){.md-button}

## What's new at a glance

### Backup and restore

* [Use PVC snapshots for faster backups and restores](#boost-backup-and-restore-performance-with-pvc-snapshot-support)

### Operations

* [Configure WAL lag detection for standby clusters](#improve-replication-for-standby-clusters-with-wal-lag-detection)
* [Mount volumes to sidecar containers](#mount-volumes-to-sidecar-containers)
* [Configure leader election for the Operator](#configurable-leader-election-for-percona-operator-for-postgresql)
* [Troubleshoot with pprof profiling](#troubleshoot-operator-with-pprof-profiling)
* [Specify custom DNS suffix for vcluster or custom DNS setups](#configurable-dns-suffix-for-operator-connections)
* [Configure `wal_level` for replication requirements](#ability-to-configure-wal_level)

### Database and integrations

* [PostgreSQL 18 is now the default version](#postgresql-18-is-now-the-default-version)
* [Major upgrade flow is generally available](#general-availability-for-major-upgrades)
* [LDAP authentication support](#centralize-user-identity-management-with-ldap-authentication-support)
* [Automated TLS certificate management via cert-manager](#automated-tls-certificate-lifecycle-management-via-the-cert-manager)
* [Official PostGIS Docker image](#official-docker-image-for-postgis)

## Release Highlights

This release provides the following features and improvements:

### PostgreSQL 18 is now the default version

Starting with this release PostgreSQL 18 becomes the default and recommended version for new cluster deployments using the Operator. This change enables you to benefit from its latest features, performance improvements, and enhanced security.

### General availability for major upgrades

With this release the major upgrade flow is generally available. This means it has undergone thorough testing and you can use it in production environments.

See our [upgrade guide](../update-db-major.md) for the detailed step-by-step instructions.

### Boost backup and restore performance with PVC snapshot support

You can now use PVC snapshots to speed up backups and restores in your PostgreSQL clusters. A PVC snapshot is a point-in-time copy of your data volumes taken directly at the storage layer. Instead of streaming data to cloud storage, the Operator creates fast, storage level snapshots. This is especially beneficial for large data set owners, boosting their backup and restore performance.

Using PVC snapshots, you benefit from:

* **Faster backups** — Snapshots typically complete in seconds or minutes, no matter how large your database is. Traditional full backups can take hours.
* **Faster restores** — Creating a new cluster from a snapshot is significantly quicker than restoring from cloud storage.
* **Lower resource usage** — Snapshots avoid the CPU and network overhead of transferring data to remote storage.
* **Point-in-time recovery support** - By combining PVC snapshots with `pgBackRest` WAL archiving, you ensure data consistency and can make point-in-time recovery of your PostgreSQL cluster.

The Operator currently supports cold (offline) backups, where one replica is briefly taken offline to create the snapshot. We plan to introduce hot backups in future releases, allowing you to run snapshot backups without downtime.

You can find details about the workflow, requirements, and limitations in [the PVC snapshot support documentation](../backups-pvc-snapshots.md).

PVC snapshot support is released as a tech preview. We don't recommend using it in production yet, but we encourage you to try it out and share your feedback. To enable the feature, turn on the `BackupSnapshots` feature gate in your Operator Deployment.

Refer to our tutorials for [setting up](../backups-pvc-gke.md) and [using](../backups-pvc-usage.md) PVC snapshots.

### Improve replication for standby clusters with WAL lag detection

If your primary cluster has a large volume of WAL files, the standby cluster may not be able to apply them quickly enough. When this happens, the standby can fall behind, experience replication issues, and temporarily miss the most recent data.

To improve the replication, you can now enable replication lag detection for your standby cluster. You set the maximum amount of WAL data the standby is allowed to lag behind. When the amount of WAL files exceeds this threshold, the primary Pod in the standby cluster is marked as `Unready`, the cluster enters the `Initializing` state and the `StandbyLagging` condition is recorded in the cluster status.

This enhancement gives you a clear view of your replication health, speeds up troubleshooting, and helps prevent application downtime during disaster recovery scenarios. To learn more about it, read our [documentation](../standby.md#detect-replication-lag-for-standby-cluster).

### Centralize user identity management with LDAP authentication support

LDAP authentication is now available in Percona Operator for PostgreSQL, giving you a straightforward way to centralize database access around your existing corporate identity systems. Instead of verifying user passwords locally, PostgreSQL delegates it to an LDAP server.

You have the flexibility to make a *simple LDAP bind* where the user Distinguished Name is constructed from the prefix and suffix you provide, or make a *bind and search* for a user using a specific attribute. See our [documentation](../ldap.md) to learn more.

This improvement lets users log in to the database with their existing organizational credentials and not have to remember multiple logins. You benefit from a deployment that is easier to secure, audit and operate at scale.

### Automated TLS certificate lifecycle management via the cert-manager

You can now install and use the `cert-manager` to generate TLS certificates and manage their lifecycle. The Operator automatically detects if the cert-manager is installed in your Kubernetes environment and requests certificates from it when it deploys Percona Distribution for PostgreSQL cluster. You can additionally configure the certificate duration via the Custom Resource to follow your security policies.

With this improvement, you benefit from the following:

* **Automatic renewal** – cert-manager renews certificates before they expire (by default, 30 days before expiry)
* **Configurable validity** – you can set certificate and CA validity durations via Custom Resource options
* **Centralized management** – use cert-manager’s tooling and policies for all TLS certificates in the cluster

Follow our [documentation](../tls-cert-manager.md) on how to install and use the cert-manager in your deployment.

### Troubleshoot Operator with pprof profiling

`pprof` is Go's built-in profiling tool for CPU and memory analysis. You can use it to investigate Operator performance issues, high CPU usage, or memory leaks when troubleshooting. Set the `PPROF_BIND_ADDRESS` environment variable in the Operator’s deployment to an address that the controller should bind to for serving `pprof` metrics. An example value is `127.0.0.1:6060`. Then expose the port from inside the Operator Pod to your local machine so that you can collect CPU or memory profiles.

### Configurable DNS suffix for Operator connections

You can now specify a custom DNS suffix that the Operator uses when it generates service names. This is useful when the Operator runs in a vcluster or in a cluster with a custom DNS configuration. In those setups, the default `cluster.local` suffix can cause incorrect domain name resolution and, as a result, failed connections to external services such as PMM or `pgBackRest`. By setting the `clusterServiceDNSSuffix` in the Custom Resource to your cluster's DNS suffix, the Operator generates hostnames that match your DNS configuration. This ensures the service discoverability and correct communication between workloads.

### Mount volumes to sidecar containers

You can now attach volumes and PersistentVolumeClaims to custom sidecar containers in PostgreSQL instance Pods, pgBouncer Pods, and pgBackRest repo host Pods.

You can either claim storage via Persistent Volume Claim or mount volume Secrets and/or ConfigMaps to sidecars, all via the Custom Resource.

This improvement lets the main application container and sidecars share data without the need for complex API calls for information exchange. You can also update the configuration dynamically, without restarts, which provides additional flexibility in operating sidecars.

For more details and examples, see the [sidecar documentation](../sidecar.md).

### Configurable leader election for Percona Operator for PostgreSQL

You can now tune leader election settings for the Operator Deployment via environment variables. This helps when the Operator hits leader election failures, for example in high-latency or resource-constrained clusters.

* Use the `PGO_CONTROLLER_LEASE_DURATION`, `PGO_CONTROLLER_RENEW_DEADLINE`, `PGO_CONTROLLER_RETRY_PERIOD` environment variables to adjust timing for lease acquisition and renewal.
* Use the `PGO_CONTROLLER_LEADER_ELECTION_ENABLED` environment variable to turn on or off leader election for single-replica deployments
* Use the `PGO_CONTROLLER_LEASE_NAME` environment variable to use a custom Lease resource for a leader lock.

Learn more about available environment variables in our [documentation](../env-var-operator.md).

### Ability to configure wal_level

The `wal_level` setting defines how much information to write to Write Ahead Log (WAL) in PostgreSQL. The Operator sets the default `wal_level` to `logical`. This works well if you use logical replication. However, for clusters that only need physical replication or no replication at all, it can add unnecessary overhead: more WAL data, extra I/O, and higher CPU usage.

You can now choose the right level for your use case. Set `wal_level` in the Custom Resource when you create a cluster or update it later.

```yaml
spec:
  patroni:
    dynamicConfiguration:
      postgresql:
        parameters:
          wal_level: replica
```

If you change the `wal_level` value on an existing cluster, your PostgreSQL Pods will be restarted.

This ability to configure `wal_level` gives you control over WAL behavior and lets you avoid extra overhead when you don’t need logical replication.

### Official Docker image for PostGIS

The Operator now uses the official Percona Docker images for PostGIS, with the image path `percona/percona-distribution-postgresql-with-postgis:<postgresql-version>`.

Pay attention to the image path when you [upgrade the database](../update-db-minor.md).

## Deprecation, Change, Rename and Removal

### Deprecated support for PMM2

The Operator deprecates support for PMM2 as this version entered the end-of-life stage. PMM2 remains available so you can still monitor the health of your database using this version. However, we encourage you to plan migration to PMM3 to enjoy all features and fixes that this version provides. See the [PMM upgrade documentation :octicons-link-external-16:](https://docs.percona.com/percona-monitoring-and-management/3/pmm-upgrade/migrating_from_pmm_2.html) for steps.

The support for PMM2 will be dropped in the Operator in two releases.

### Operators in Red Hat Marketplace catalog are no longer maintained

Red Hat Marketplace was discontinued in April 2025. Percona Operator for PostgreSQL will remain listed in the Marketplace catalog, but it won't be updated beyond OpenShift 4.22.

If you use the Operator from Red Hat Marketplace, switch to the Certified Operator Catalog for future updates and support.

### `pg_stat_monitor` is disabled by default

Starting with this release `pg_stat_monitor` is disabled by default when you deploy a new cluster. If you wish to keep using this extension after upgrading to this version, enable it in the Custom resource before the upgrade.

### Custom Resource changes

* The `exposeSuperusers` default value has changed to `false`

### CRD changes

* The description of the `.spec.majorVersion` option has been updated to include PostgreSQL 18.
* New fields:
  
   * `tls.properties.caValidityDuration`
   * `tls.properties.pgBackRestCertValidityDuration`
   * `tls.properties.certValidityDuration`


## Changelog

### New features

* [K8SPG-374](https://perconadev.atlassian.net/browse/K8SPG-374) - Added the WAL lag detection for standby clusters based on user defined thresholds

* [K8SPG-771](https://perconadev.atlassian.net/browse/K8SPG-771) - Added support of PVC snapshots, which enable storage-level snapshot capabilities and allow for faster backups and restores of large databases.

### Improvements 

* [K8SPG-552](https://perconadev.atlassian.net/browse/K8SPG-552) - Added the ability to automatically create TLS certificates via the cert-manager and configurable certificate duration via the Custom Resource

* [K8SPG-758](https://perconadev.atlassian.net/browse/K8SPG-758) - Added support for pprof profiling tool. You can set up port-forwarding to the Operator controller to perform CPU and memory profiling for easier performance investigation

* [K8SPG-779](https://perconadev.atlassian.net/browse/K8SPG-779) - Added the ability to configure `wal_level` according to replication requirements to avoid extra I/O overhead. 

* [K8SPG-822](https://perconadev.atlassian.net/browse/K8SPG-822) - Improved e2e tests by adding `pg_repack` built-in extension to the testsuite

* [K8SPG-837](https://perconadev.atlassian.net/browse/K8SPG-837) - Updated the base image to RHEL 10 for PostgreSQL Operator

* [K8SPG-840](https://perconadev.atlassian.net/browse/K8SPG-840) - The logic for determining the latest restorable time has been improved to provide more accurate point-in-time recovery options.

* [K8SPG-864](https://perconadev.atlassian.net/browse/K8SPG-864) - Added the ability to add custom volumes, ConfigMaps, and Secrets to sidecar containers, allowing for deeper customization without code changes.

* [K8SPG-873](https://perconadev.atlassian.net/browse/K8SPG-873) - Added `.env` and `.envFrom` fields to backup/restore resources. These new fields allow users to inject custom environment variables into backup and restore jobs for better configuration flexibility.

* [K8SPG-904](https://perconadev.atlassian.net/browse/K8SPG-904) - Users can now initialize a new cluster from an existing data source even if automated backups are currently disabled in the configuration.

* [K8SPG-908](https://perconadev.atlassian.net/browse/K8SPG-908) - The Operator has transitioned to using official PostGIS images to ensure better compatibility and standard support.

* [K8SPG-915](https://perconadev.atlassian.net/browse/K8SPG-915) - Added the ability to tune leader election parameters for the Operator to prevent unnecessary failovers in unstable network environments.

* [K8SPG-956](https://perconadev.atlassian.net/browse/K8SPG-956) - Optimized the `archive_command` to reduce CPU usage by applying resource manager filters in `pg_waldump` during WAL processing.

### Bugs fixed

* [K8SPG-647](https://perconadev.atlassian.net/browse/K8SPG-647) - Resolved a race condition that occasionally prevented secondary nodes from reaching a ready state following a major version upgrade or restore.

* [K8SPG-665](https://perconadev.atlassian.net/browse/K8SPG-665) - Resolved the issue with excessive log messages about superusers being exposed through PGBouncer by changing the default value for the `exposeSuperusers` option to `false`.

* [K8SPG-694](https://perconadev.atlassian.net/browse/K8SPG-694) - Fixed an issue where the Operator incorrectly identified the internal cluster domain when running inside a vcluster environment by adding the ability to specify custom DNS suffix.

* [K8SPG-740](https://perconadev.atlassian.net/browse/K8SPG-740) - Fixed the issue with the Operator failing to clean up outdated backups during the minor upgrade by checking the repo-host pod status before attempting backup cleanup. The cleanup is skipped until the repo-host pod is ready.

* [K8SPG-821](https://perconadev.atlassian.net/browse/K8SPG-821) - Enhanced automated testing for database updates to ensure stability across different OS base images and PostgreSQL versions.

* [K8SPG-901](https://perconadev.atlassian.net/browse/K8SPG-901) - Fixed a crash that occurred when the proxy configuration block was missing from the Custom Resource file.

* [K8SPG-903](https://perconadev.atlassian.net/browse/K8SPG-903) - Improved error reporting for upstream controllers to include stacktraces, making support cases and troubleshooting significantly faster.

* [K8SPG-907](https://perconadev.atlassian.net/browse/K8SPG-907) - Fixed a bug where point-in-time recovery operations would fail with a panic during internal JSON data processing.

* [K8SPG-923](https://perconadev.atlassian.net/browse/K8SPG-923) - Improved documentation on how to fine-tune backup performance via asynchronous replication

* [K8SPG-933](https://perconadev.atlassian.net/browse/K8SPG-933) - Fixed an issue that prevented the successful creation of standby clusters when enabled in the Custom Resource.

* [K8SPG-938](https://perconadev.atlassian.net/browse/K8SPG-938) - Fixed a synchronization issue where cluster status conditions were not correctly reflecting updates from the underlying controllers.

* [K8SPG-939](https://perconadev.atlassian.net/browse/K8SPG-939) - Fixed an issue with Patroni not considering custom labels. Now all Patroni-managed objects correctly inherit and apply all Custom Resource labels for better tracking and reporting

* [K8SPG-943](https://perconadev.atlassian.net/browse/K8SPG-943) - Resolved a nil pointer dereference that could cause the Operator to crash during cluster creation under specific conditions.

* [K8SPG-957](https://perconadev.atlassian.net/browse/K8SPG-957) - Fixed a crash in Amazon EKS environments where the Operator would fail if VolumeSnapshot APIs were not pre-installed.

### Documentation improvements

* Updated OpenShift documentation to better show available installation options
* Updated PostGIS documentation now features simplified deployment steps and clarifies the how to connect to PostgreSQL and enable the extension.
* Improved documentation about cluster-wide setup with a clear explanation of the WATCH_NAMESPACE environment variable
* Added documentation of available environment variables
* Added documentation about immutable options in the Operator
* Added instructions how to override resource names when installing the Operator via Helm 


## Supported software

This Operator version is developed, tested and based on:

--8<-- [start:software]

* PostgreSQL 13.22-1, 14.19-1, 15.14-1, 16.10-1,17.6-1 as the database. Other versions may also work but have not been tested.
* pgBouncer 1.24.1-1 for connection pooling
* Patroni version 4.0.6 for high-availability
* PostGIS version 3.3.8

--8<-- [end:software]

## Supported platforms

Percona Operators are designed for compatibility with all [CNCF-certified :octicons-link-external-16:](https://www.cncf.io/training/certification/software-conformance/) Kubernetes distributions. 

Our release process includes targeted testing and validation on major cloud provider platforms and OpenShift, as detailed below for Operator version 2.8.0:

--8<-- [start:platforms]

* [Google Kubernetes Engine (GKE) :octicons-link-external-16:](https://cloud.google.com/kubernetes-engine) 1.31 - 1.33
* [Amazon Elastic Container Service for Kubernetes (EKS) :octicons-link-external-16:](https://aws.amazon.com) 1.31 - 1.34
* [OpenShift :octicons-link-external-16:](https://www.redhat.com/en/technologies/cloud-computing/openshift) 4.16 - 4.20
* [Azure Kubernetes Service (AKS) :octicons-link-external-16:](https://azure.microsoft.com/en-us/services/kubernetes-service/) 1.32 - 1.34
* [Minikube :octicons-link-external-16:](https://github.com/kubernetes/minikube) 1.37.0 with Kubernetes v1.34.0

--8<-- [end:platforms]

This list only includes the platforms that the Percona Operators are specifically tested on as part of the release process. Other Kubernetes flavors and versions depend on the backward compatibility offered by Kubernetes itself.

## Percona certified images

Find Percona's certified Docker images that you can use with the Percona Operator for PostgreSQL in the following table.


--8<-- [start:images]

| Image                                                                 | Digest                                                           |
|:----------------------------------------------------------------------|:-----------------------------------------------------------------|
| percona/percona-postgresql-operator:2.8.0  (x86_64)  | e34a185e1b295ff627facd3cfbdfc31f32bab714eac550de5e6da00abd9053e2 |
| percona/percona-postgresql-operator:2.8.0 (ARM64)  | 18445bd761ac3f77901f0e9eddd79b295d28b779779a29bb2d69eb51c32e3815 |
| percona/percona-distribution-postgresql:17.6-1   | ce91a339a511d91d9f1946708d7ca326572796b642d2a022a1d52a2adff8a08b |
| percona/percona-distribution-postgresql:16.10-1    | ba1aede456a938f85c9614bb70c50ce264ec68b659917a3a0847112e42bc9259 |
| percona/percona-distribution-postgresql:15.14-1       | 8280ba2410235e8266761004a2f180fe3999203e69772eb822959cf1849bd967 |
| percona/percona-distribution-postgresql:14.19-1    | 052e7fd765b790ad2321675e8f2b273fe705512afda5004c4d2a4da78489bfb0 |
| percona/percona-distribution-postgresql:13.22-1     | 2989dcc4919c8381dc970b2286dadec45c8a53067b48f2bcfff7c7c042b3a654 |
| percona/percona-postgresql-operator:2.8.0-ppg17.6-postgres-gis3.3.8   | 3322136e6e54214255601586be8f610677fe51a494d3a002cabfacd233258fab |
| percona/percona-postgresql-operator:2.8.0-ppg16.10-postgres-gis3.3.8  | 2d5f9ac5a84129e81b9ab8df25abce712223c358847afed3637fb7063a3e4a8f |
| percona/percona-postgresql-operator:2.8.0-ppg15.14-postgres-gis3.3.8  | e7f5fda3cf7d2fab028b3fb70636c9b3b11fe6b89a9f31970d2792bd8f48d8ca |
| percona/percona-postgresql-operator:2.8.0-ppg14.19-postgres-gis3.3.8  | 3f69534a0df0b608d68808df04618222e4a20c1d1567462e4482f07b86349806 |
| percona/percona-postgresql-operator:2.8.0-ppg13.22-postgres-gis3.3.8  | cd5a2a1057708fac5dda28d0ce47006cdbf865e6ffef1ac2df74065b95258fd3 |
| percona/percona-pgbouncer:1.24.1-1 (x86_64)  | 39bd093ec83ca4eaeb93b43b286d39daae4cc4b3b32956d627d242d30a5ad6f5 |
| percona/percona-pgbouncer:1.24.1-1 (ARM64)    | 84d34843180d852182790ce6175f1407a0438b3a415a21741212701706808ac0 |
| percona/percona-pgbackrest:2.56.0-1  (x86_64)   | 387469090be8e009e17cc07903aa28aa1c748ce1cc385bd69e88de3762657877 |
| percona/percona-pgbackrest:2.56.0-1 (ARM64)   | 29290808bdeb17a49c90f2ce3ccc75f3bfab43e96e160320baf16cb557d165ee |
| percona/pmm-client:2.44.1-1         | 52a8fb5e8f912eef1ff8a117ea323c401e278908ce29928dafc23fac1db4f1e3 |
| percona/pmm-client:3.4.1 (x86_64)   | 1c59d7188f8404e0294f4bfb3d2c3600107f808a023668a170a6b8036c56619b |
| percona/pmm-client:3.4.1 (ARM64)    | 2d23ba3e6f0ae88201be15272c5038d7c38f382ad8222cd93f094b5a20b854a5 |

--8<-- [end:images]
