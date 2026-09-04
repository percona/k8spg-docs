# Percona Operator for PostgreSQL 3.1.0 ({{date.3_1_0}})

!!! warning ""

    Operator 2.8.0 and all 2.8.x patch releases have reached end of life. They no longer receive bug fixes, security updates, or support. Upgrade to a [supported Operator version](update-operator.md) to keep your clusters current and protected.

[Get started with the Operator :material-arrow-right:](../quickstart.md){.md-button}

## What's new at a glance

### Security

* [Transparent data encryption with `pg_tde`](#transparent-data-encryption-support-with-pg_tde)
* [Control TLS certificate management for manually provisioned Secrets](#more-control-over-tls-certificate-management)
* [Client mTLS with pgBouncer and additional trusted CAs](#enable-mutual-tls-mtls-between-clients-and-pgbouncer)

### Operations and observability

* [Persistent logging across Pod restarts](#improve-operational-resilience-and-observability-with-persistent-logging-for-postgresql-pods)
* [Configurable log rotation for persistent logs](#configure-log-rotation-for-persistent-logs)
* [Pause and resume pgBouncer without dropping client connections](#pause-and-resume-pgbouncer-connections)
* [Auto-growable disks for pgBackRest repository volumes](#keep-backup-storage-healthy-with-auto-growable-disks-for-pgbackrest)
* [Mount extra volumes into PostgreSQL instances](#mount-extra-volumes-into-postgresql-instances)

### Read scaling

* [Declarative logical replicas for read-only workloads](#define-logical-replicas-declaratively) (tech preview)

### Images and platforms

* [UBI 8, 9, and 10 images](#support-for-ubi-8-ubi-9-and-ubi-10-images-for-percona-distribution-for-postgresql)
* [Community PostgreSQL images and custom registries](#support-for-community-postgresql-images)
* [PostgreSQL 19 support](#support-of-postgresql-19-tech-preview) (tech preview)
* [Official support for Rancher Kubernetes Engine (RKE2)](#official-support-for-rancher-kubernetes-engine-rke2)
* [Full ARM64 support for Operator images](#the-operator-is-now-fully-supported-on-arm64-architectures)

### Upgrade notes

* [PMM2 support removed](#deprecation-change-rename-and-removal) — upgrade to PMM3
* [Operator 2.8.0 has reached end of life](#deprecation-change-rename-and-removal)
* [`extensions.builtin` deprecated](#deprecation-change-rename-and-removal) — use `extensions.<extension>.enabled`
* [`pg_cron` and `set_user` are now built-in extensions](#deprecation-change-rename-and-removal)

## Release highlights

### Transparent data encryption support with `pg_tde`

You can now protect PostgreSQL data at rest with [`pg_tde` :octicons-link-external-16:](https://docs.percona.com/pg-tde/index.html), Percona's fully open source transparent data encryption extension.

Data in tables, indexes, temporary tables, and write-ahead log (WAL) files is encrypted on disk. Without the keys, that data stays unreadable even if storage is compromised.

Enable `pg_tde` in the Custom Resource and configure HashiCorp Vault as the key provider. The Operator installs and configures the extension for you. After setup, you can create encrypted tables or convert existing ones. Backups and restores work as usual when the Operator can reach the encryption key.

This feature is available with PostgreSQL 17 and 18. In this
release, only HashiCorp Vault (KV v2) is supported as a key
provider. KMIP and other providers are planned for later.

See [Data-at-rest encryption](../encryption.md) and [Configure data-at-rest encryption with HashiCorp Vault](../encryption-setup.md).

### Improve operational resilience and observability with persistent logging for PostgreSQL Pods

Debugging distributed systems just got easier. Percona Operator for PostgreSQL now supports persistent logging, so PostgreSQL and pgBackRest logs on the instance data volume stay available even across Pod restarts.

The Operator uses [Fluent Bit :octicons-link-external-16:](https://fluentbit.io/) to collect logs. Fluent Bit runs a `logs` sidecar container on each PostgreSQL instance Pod and mounts the same data volume. It collects logs and streams them to its own stdout as JSON lines. You can additionally configure Fluent Bit outputs such as S3 or Open Telemetry (OTel) envelope and have the logs forwarded there.

[Learn more about persistent logging in the documentation](persistent-logging.md)

### Configure log rotation for persistent logs

You can now customize log rotation for persistent logs. This helps you keep the right amount of data for troubleshooting or compliance, extend the default configuration with your custom settings and schedule rotations to fit your operational windows.

You can configure log rotation in these ways:

* Override the default configuration via the Custom Resource
* Define additional configuration via a ConfigMap. In this case, the Operator adds your options to the default configuration
* Set a new rotation schedule
  
See our [documentation](logrotate.md) for step-by-step instructions for each option.

### Define logical replicas declaratively (tech preview)

You can now add a read-only logical replica in the same cluster and point reporting or other heavy reads at this replica instead of the primary. The replica has its own volume and Service, so those queries do not compete with your high-availability set.

Declare the replica in the Custom Resource when you create the cluster or later during runtime. You can also define which databases receive the changes after the replica is bootstrapped.

The Operator creates the volume, copies the data, converts the physical replica to the logical one and keeps the databases you list in sync. It also creates a Service you can connect to. 

Patroni does not manage nor promote it, so it stays a stable read endpoint.

Logical replication is in the tech preview stage and requires PostgreSQL 17 or later. See [Deploy a logical replica](deploy-replica.md).

### Mount extra volumes into PostgreSQL instances

You can now mount additional Kubernetes volumes into the PostgreSQL container so that every instance in the cluster sees the same files.

This is useful when PostgreSQL needs files outside the data
directory such as for full text search.

Configure the volume and mount path under `instances.extraVolumes` in the Custom Resource. You can use a ConfigMap, Secret, PersistentVolumeClaim, emptyDir, or
another volume source that Kubernetes supports. 

Every instance in the set sees the same mounts, so your assets stay consistent across the cluster. Prefer `subPath` mounts when you add files next to the existing directory, so you do not replace the contents that PostgreSQL already ships.

For steps and examples, see [Mount extra volumes into PostgreSQL instances](../extra-volumes.md).

### More control over TLS certificate management

If you manage TLS certificates manually, such as through Kubernetes Secrets synced from AWS Secrets Manager or via External Secrets, losing access to those Secrets even briefly can lead to a service outage.

By default, the Operator treats a missing TLS Secret as a signal to create new certificates, restart the database Pods, and apply the new CA. Applications that still trust your original CA may lose connectivity.

Starting with this release, set `spec.tls.certManagementPolicy` in the Custom Resource to control the Operator's behavior. The policies are:

* `auto` (default) — If TLS Secrets are missing, the Operator creates certificates. It may use cert-manager when cert-manager is installed.
* `userProvidedOnly` — You own the certificate lifecycle. The Operator does not create or replace TLS certificates if a Secret is temporarily unavailable. Applications can keep using the certificates already loaded while you restore the Secret.
* `operatorProvidedOnly` — The Operator always manages TLS with its own PKI and does not use cert-manager.

For manually provided TLS, use `userProvidedOnly`:

```yaml
spec:
  tls:
    mode: preferTLS
    certManagementPolicy: userProvidedOnly
    allowInvalidCertificates: false
  secrets:
    customTLSSecret:
      name: cluster1-cert
    customReplicationTLSSecret:
      name: replication1-cert
```

See [TLS certificate management policy](../tls-cert-management-policy.md) for more information.

### Enable Mutual TLS (mTLS) between clients and pgBouncer

Mutual TLS (mTLS) needs `pgBouncer` to trust the CA that signed client certificates. Previously, you could only do that by providing TLS material in  `proxy.pgBouncer.customTLSSecret` and you had to manage the full certificate lifecycle yourself.

Now, you can extend the pgBouncer frontend trust bundle with your external CA that signed client certificates. Create the Secret with this CA and add it to the cluster with the`proxy.pgBouncer.additionalTrustedCAs` option. The Operator appends your external CAs to the trust bundle and keeps rotating the pgBouncer and cluster certificates.

With this improvement, you get mTLS for clients that use your corporate or application CA, and keep Operator-managed TLS for the cluster.

See [Trust additional CAs for pgBouncer client mTLS](../tls-pgbouncer-trusted-cas.md) for configuration steps.

### Keep backup storage healthy with auto-growable disks for pgBackRest

A full `pgBackRest` repository volume can interrupt backups. Starting with this release, auto-growable disks cover pgBackRest repository volumes on the repo host, not only PostgreSQL data volumes. The Operator monitors disk usage and expands the PVC automatically up to the limit you set.

Turn on the `AutoGrowVolumes=true` feature gate and set `spec.backups.pgbackrest.repos[].volume.volumeClaimSpec.resources.limits.storage` in the Custom Resource. If you already use automated storage scaling for data volumes, apply the same approach to your backup repos.

```yaml
spec:
  backups:
    pgbackrest:
      repos:
      - name: repo1
        volume:
          volumeClaimSpec:
            resources:
              requests:
                storage: 1Gi
              limits:
                storage: 5Gi
```

See [Automated scaling with auto-growable disks](../scaling.md#automated-scaling-with-auto-growable-disks) for the full setup.

### Pause and resume pgBouncer connections

You can now pause client traffic through pgBouncer without dropping application connections. Active queries finish, then new client requests wait in a queue until you resume. Use this for a short, controlled window to restart PostgreSQL, run a planned switchover, or drain backend load.

Set `proxy.pgBouncer.paused` to `true` in the Custom Resource to pause, and back to `false` to resume. The Operator connects to each `pgBouncer` Pod
and runs the `PAUSE` command. Pods with active connections
remain running until they finish, then the Pod changes its state
to `paused`. If a pgBouncer Pod restarts while paused, a startup
probe re-applies `PAUSE`
so the intended state survives restarts.

### Support for UBI 8, UBI 9, and UBI 10 images for Percona Distribution for PostgreSQL 

You can now choose Red Hat Universal Base Image (UBI) 8, 9, or 10 for Percona Distribution clusters. That lets you migrate to Percona Operator without changing the OS inside the PostgreSQL container, so you can keep working extensions, stay aligned with your Enterprise Linux version, or move to a newer UBI when you are ready.

UBI is the operating system inside the PostgreSQL container. PostgreSQL uses OS-provided `glibc` and ICU libraries to sort and compare text, and each UBI major version ships different library versions. The UBI choice is part of the database runtime.

By default, images that ship with the Operator are based on UBI 9 and have no OS version in the tag, for example `docker.io/percona/percona-distribution-postgresql:{{postgresrecommended}}`. UBI 8 and UBI 10 images add the OS version to the tag:

```text
docker.io/percona/percona-distribution-postgresql:{{postgresrecommended}}-ubi8
docker.io/percona/percona-distribution-postgresql:{{postgresrecommended}}-ubi8-arm64
docker.io/percona/percona-distribution-postgresql:{{postgresrecommended}}-ubi10
docker.io/percona/percona-distribution-postgresql:{{postgresrecommended}}-ubi10-arm64
```

Use UBI 9 as the baseline for PostgreSQL 14–18. This page lists the UBI 9 images. For UBI 8 and UBI 10, see [Percona certified images](../images.md).
Stay on UBI 8 when older extensions or Enterprise Linux 8 requirements still apply. Choose UBI 10 to align with RHEL 10 or OpenShift nodes that run Enterprise Linux 10, and to stay on an OS with a longer remaining support window and newer system libraries. 

!!! important

    Switching UBI major versions changes `glibc` and ICU. PostgreSQL reports a collation version mismatch, and indexes on `text`, `varchar`, `char`, and similar types can return incorrect results until you rebuild them. After you switch, identify affected indexes, run `REINDEX`, then run `ALTER DATABASE ... REFRESH COLLATION VERSION`. See the [minor upgrade](../update-db-minor.md) and [major upgrade](../update-db-major.md) documentation.



Keep every instance in a cluster on the same UBI version. Treat a UBI change as an OS upgrade: take a backup first, and confirm that custom extensions are built for the target UBI.

### Support for community PostgreSQL images

With this release, you can deploy PostgreSQL Community images or your own PostgreSQL images under your own registry and tags with the Operator. To do this, define them under the `spec.image`, `spec.proxy.pgBouncer.image`, and `spec.backups.pgbackrest.image` options in the Custom Resource. The Operator automates database deployment and management with these images the same way it does for Percona Distribution for PostgreSQL.

This compatibility gives you full control and transparency over your infrastructure enabling you to use extensions not available in Percona images. However, you cannot use features such as [Transparent data encryption](#transparent-data-encryption-support-with-pg_tde) that are available only in Percona images, and you are fully responsible for the image lifecycle and support.

Community packages are available for UBI8 and UBI9 base images, allowing you to quickly spin them up for testing and evaluation before building your own pipeline. These images are not bound to a specific Operator version, but you must use Operator version 3.1.0 or later to deploy community or custom PostgreSQL images. Refer to [PostgreSQL Community images](#postgresql-community-images) for the list of available images.

Community images are an experimental project. We want to see how you adopt them so we can decide what to invest in next. Try them out and tell us what works, what is missing, and what you want the Operator to support.

For more information about using community images and building your own ones, refer to the Percona Blog: [Community Docker Images: keeping the operator open without a vendor registry lock in](https://www.percona.com/blog/postgresql-community-images-operator/) by Slava Sarzhan and our [documentation](../install-community.md).

### Support of PostgreSQL 19 (tech preview)

With this release, the Operator supports deployment of Community PostgreSQL 19. This support is currently in the tech preview stage because this major version is not officially released yet. However, you can already deploy it and evaluate the features coming with this version. This allows you to stay on top of upcoming enhancements and gives you enough time to prepare your upgrade and migration plans before the final release lands. See [Deploy the Operator with Community images](install-community.md) for guidelines.

### Official support for Rancher Kubernetes Engine (RKE2)

[Rancher Kubernetes Engine (RKE2) :octicons-link-external-16:](https://docs.rke2.io/) is now an officially supported platform. Every Operator release is now tested on RKE2 to ensure that you can run it on Rancher-managed Kubernetes clusters with confidence.

### The Operator is now fully supported on ARM64 architectures

All Operator images are now available for ARM64, giving you native support on ARM based clusters with no extra setup.

## Deprecation, Change, Rename and Removal

* Removed support for PMM2. This Operator release no longer supports PMM2 as it has reached the end-of-life state. Upgrade to PMM3 as soon as possible. For how to upgrade, refer to [PMM documentation :octicons-link-external-16:](https://docs.percona.com/percona-monitoring-and-management/3/pmm-upgrade/migrating_from_pmm_2.html).

* The Operator version 2.8.0 and all 2.8.x patch versions have reached end of life and are no longer supported. 
* The `extensions.builtin` section is deprecated and will be removed after version 3.4.0. We encourage you to use `extensions.<extension>.enabled`. You can still use the old form during the transition. If both forms are set at the same time, `extensions.builtin` takes precedence.
* `pg_cron` and `set_user` extensions have been added to the list of built-in extensions. Your existing setup via the `extensions.custom` remains unchanged and works as expected after the upgrade. To switch to using built-in extensions, do the following:
  
   * Remove the extension from the `extensions.custom` list
   * Set `extensions.pg_cron.enabled` or `extensions.set_user.enabled` to `true`. 
   
   You must do these changes simultaneously for the same reconciliation loop. Just removing the extension `extensions.custom` list instructs the Operator to delete it.

* Field descriptions were removed from the inherited `CrunchyBridgeCluster` CRD (upstream.pgv2.percona.com/v1beta1). The object schema and cluster behavior are unchanged. Running `kubectl explain` for those fields no longer shows help text.

## Changelog

## New Features

* [K8SPG-911](https://perconadev.atlassian.net/browse/K8SPG-911) - Added native transparent data encryption support via `pg_tde` so you can encrypt data at rest from the Custom Resource.

* [K8SPG-650](https://perconadev.atlassian.net/browse/K8SPG-650) - Added support for declaring additional pgBouncer users in the Custom Resource so monitoring and other integrations can keep dedicated credentials. The Operator now manages the pgBouncer user list for you instead of relying on manual Secret edits that could be overwritten.

* [K8SPG-851](https://perconadev.atlassian.net/browse/K8SPG-851) - Added persistent logging for PostgreSQL and pgBackRest so logs remain available across Pod restarts. Fluent Bit collects logs on the instance data volume and can forward them as JSON or to configured outputs such as S3 or OpenTelemetry.
 
### Improvements

* [K8SPG-440](https://perconadev.atlassian.net/browse/K8SPG-440) - Added the ability to mount extra volumes into PostgreSQL instances so every Pod can share files such as full-text search dictionaries. 

* [K8SPG-691](https://perconadev.atlassian.net/browse/K8SPG-691) - Extended auto-growable disks to pgBackRest repository volumes so a full backup repo no longer blocks backups. The Operator monitors repo-host disk usage and expands the PVC up to the limit you set when the `AutoGrowVolumes` feature gate is enabled.

* [K8SPG-870](https://perconadev.atlassian.net/browse/K8SPG-870) - Added a `status.size` field on full, differential, and incremental `PerconaPGBackup` objects so you can see backup size without inspecting storage directly. This makes backup capacity planning and troubleshooting easier.

* [K8SPG-881](https://perconadev.atlassian.net/browse/K8SPG-881) - Added full ARM64 support for Operator images so you can run natively on ARM-based Kubernetes clusters. No extra setup is required beyond using the ARM64 image digests published with this release.

* [K8SPG-944](https://perconadev.atlassian.net/browse/K8SPG-944) - Removed PMM2 support now that PMM2 has reached end of life. Upgrade monitoring to PMM3 so cluster health checks continue to work with this Operator version.

* [K8SPG-949](https://perconadev.atlassian.net/browse/K8SPG-949) - Added official support for Rancher Kubernetes Engine (RKE2). Every Operator release is now tested on RKE2 so you can run on Rancher-managed clusters with confidence.

* [K8SPG-951](https://perconadev.atlassian.net/browse/K8SPG-951) - Added the support of custom CA issuer so you can plug in your own cert-manager Issuer or ClusterIssuer instead of the hardcoded self-signed CA. This lets you issue cluster TLS certificates from Vault or an existing corporate CA.

* [K8SPG-952](https://perconadev.atlassian.net/browse/K8SPG-952) - Added the ability to provide additional trusted CA to pgBouncer. This way you can enable client mTLS while cluster components communicate using Operator-managed PKI and the Operator continues to manage cluster TLS rotation.

* [K8SPG-1011](https://perconadev.atlassian.net/browse/K8SPG-1011) - Removed the requirement to set a pgBackRest image when backups are disabled. Clusters with `backups.enabled: false` no longer need unused backup image configuration.

* [K8SPG-1040](https://perconadev.atlassian.net/browse/K8SPG-1040) - Added `pg_cron` and `set_user` to the built-in extensions list so you can enable them with `extensions.<name>.enabled`. Existing custom-extension installs continue to work; migrate by updating the Custom Resource in a single apply.

* [K8SPG-1045](https://perconadev.atlassian.net/browse/K8SPG-1045) - Added the ability to define TLS management policy for the Operator. This gives you a control whether the Operator recreates TLS Secrets when they are temporarily missing. Use `userProvidedOnly` to keep manually provisioned certificates stable during Secret sync outages.

* [K8SPG-1047](https://perconadev.atlassian.net/browse/K8SPG-1047) - Updated major-upgrade images to use the official Percona Distribution for PostgreSQL upgrade Dockerfile. This keeps upgrade containers aligned with the same build pipeline as the database images.

* [K8SPG-1051](https://perconadev.atlassian.net/browse/K8SPG-1051) - Added tech-preview support for Community PostgreSQL 19 so you can evaluate the next major version early. Use this to test application compatibility before PostgreSQL 19 is generally available.

* [K8SPG-1053](https://perconadev.atlassian.net/browse/K8SPG-1053) - Relocated the PMM agent config to a writable `/tmp` volume so the PMM sidecar starts when `readOnlyRootFilesystem: true` is enforced. Hardened environments such as OpenShift `restricted-v2` can now monitor clusters without relaxing the root filesystem policy.

* [K8SPG-1056](https://perconadev.atlassian.net/browse/K8SPG-1056) - Added support for Community PostgreSQL images and custom registries so you are not locked to Percona-only tags. Set `spec.image`, `proxy.pgBouncer.image`, and `backups.pgbackrest.image` to deploy and manage community or privately built images.

* [K8SPG-1073](https://perconadev.atlassian.net/browse/K8SPG-1073) - Stopped configuring Patroni's `restore_command` when backups are disabled so replicas no longer call pgBackRest against a missing stanza. WAL fetch failures in backup-less clusters fall back cleanly instead of producing archive errors.

* [K8SPG-1083](https://perconadev.atlassian.net/browse/K8SPG-1083) - Improved Operator telemetry to report the Kubernetes platform in use, such as EKS, GKE, AKS, or Rancher. This helps Percona understand deployment environments and improve platform-specific testing.

* [K8SPG-1085](https://perconadev.atlassian.net/browse/K8SPG-1085) - Improved SmartUpdate logging so rolling instance updates are visible in the Operator logs. You can track when Pods are being restarted during automated updates without extra debugging.

* [K8SPG-1114](https://perconadev.atlassian.net/browse/K8SPG-1114) - Added declarative logical replicas for read-only workloads so you can offload reporting queries from the primary. The Operator creates the volume, bootstraps replication, and exposes a dedicated Service that Patroni does not promote.

* [K8SPG-1115](https://perconadev.atlassian.net/browse/K8SPG-1115) - Added the ability to pause and resume pgBouncer connections from the Custom Resource without dropping clients. Set `proxy.pgBouncer.paused` to queue new requests while active queries finish during planned maintenance.

### Fixed bugs

* [K8SPG-991](https://perconadev.atlassian.net/browse/K8SPG-991) - Fixed the issue where outdated backup cleanup failed during minor upgrades and logged noisy errors. The Operator now handles repo-host readiness more reliably before attempting cleanup.

* [K8SPG-994](https://perconadev.atlassian.net/browse/K8SPG-994) - Fixed a bug where `customRootCATLSSecret` kept only the first certificate from a multi-cert PEM bundle. Intermediate and root CA chains are now preserved so TLS verification works for corporate PKI setups.

* [K8SPG-1010](https://perconadev.atlassian.net/browse/K8SPG-1010) - Fixed an ordering issue where delete finalizers removed Secrets before the underlying `PostgresCluster` was gone, allowing Secrets to be recreated and left behind. Secret cleanup now runs after the cluster is fully deleted.

* [K8SPG-1012](https://perconadev.atlassian.net/browse/K8SPG-1012) - Fixed a bootstrap restore issue where the timeline history file was lost and after point-in-time recovery replicas could fail to rejoin via `pg_rewind`. History files are now archived correctly during restore bootstrap.

* [K8SPG-1049](https://perconadev.atlassian.net/browse/K8SPG-1049) - Fixed restore Jobs that ignored cluster tolerations and could not schedule on tainted nodes. Restore Pods now inherit the same tolerations as the backup jobs. (Thank you @Avapaa for reporting this issue)

* [K8SPG-1058](https://perconadev.atlassian.net/browse/K8SPG-1058) - Fixed `PerconaPGUpgrade` failures when the upgrade resource name was too long for generated Kubernetes object names. Long upgrade names no longer block major version upgrades. (Thank you Jakub Jaruszewski for contributing to this fix)

* [K8SPG-1113](https://perconadev.atlassian.net/browse/K8SPG-1113) - Fixed a bug where `latestRestorableTime` on older backups was overwritten with the newest restorable timestamp. Each backup now keeps its own restorable time for accurate point-in-time recovery choices.

* [K8SPG-1119](https://perconadev.atlassian.net/browse/K8SPG-1119) - Fixed restores from `dataSource.volumes` that failed validation because `repoName` was required. Volume-based bootstraps no longer need a pgBackRest repository name.
 
* [K8SPG-1138](https://perconadev.atlassian.net/browse/K8SPG-1138) - Fixed the issue snapshot restore-prepare job not being scheduled on tainted nodes because of missing tolerations. You can now assign tolerations to snapshot restore jobs. 

### Documentation updates

* [K8SPG-232](https://perconadev.atlassian.net/browse/K8SPG-232) - Expanded restore documentation to explain in-place restore, side-cluster restore, and restore into an external environment. You can choose the right recovery pattern for your topology more easily.

* [K8SPG-793](https://perconadev.atlassian.net/browse/K8SPG-793) - Documented the `trackLatestRestorableTime` logic, including when to use them and how they interact with read-only filesystem policies. Also reorganized point-in-time recovery guides.

* [K8SPG-963](https://perconadev.atlassian.net/browse/K8SPG-963) - Documented Custom Resource statuses and conditions so you can interpret cluster health from `status` without reading Operator source code. 

* [K8SPG-1123](https://perconadev.atlassian.net/browse/K8SPG-1123) - Added documentation for deploying the Operator with Community PostgreSQL images. The guide covers how to set custom image fields and what Percona-only features are unavailable with community builds.

## Supported software

This Operator version is developed and tested with Percona Distribution for PostgreSQL and PostgreSQL Community.

--8<-- [start:software]

### Percona Distribution for PostgreSQL

* PostgreSQL 14.24-1, 15.19-1, 16.15-1, 17.11.1-1, 18.6.1-1 as the database. Other versions may also work but have not been tested.
* pgBackRest 2.59.0-1 for backup and recovery
* pgBouncer 1.25.2-6 for connection pooling
* Patroni version 4.1.5 for high-availability
* PostGIS version 3.5.7
* PMM Client version 3.9.1
* cert-manager 1.21.1

### PostgreSQL Community

* PostgreSQL 14.24, 15.19, 16.15, 17.11, 18.6, and 19 (tech preview) as the database.
* pgBackRest 2.59.0 for backup and recovery
* pgBouncer 1.25.2 for connection pooling


--8<-- [end:software]

## Supported platforms

Percona Operators are designed for compatibility with all [CNCF-certified :octicons-link-external-16:](https://www.cncf.io/training/certification/software-conformance/) Kubernetes distributions. 

Our release process includes targeted testing and validation on major cloud provider platforms and OpenShift, as detailed below:

--8<-- [start:platforms]

* [Google Kubernetes Engine (GKE) :octicons-link-external-16:](https://cloud.google.com/kubernetes-engine) 1.34 - 1.35
* [Amazon Elastic Kubernetes Service (EKS) :octicons-link-external-16:](https://aws.amazon.com) 1.34 - 1.36
* [Azure Kubernetes Service (AKS) :octicons-link-external-16:](https://azure.microsoft.com/en-us/services/kubernetes-service/) 1.34 - 1.36
* [OpenShift :octicons-link-external-16:](https://www.redhat.com/en/technologies/cloud-computing/openshift) 4.19.43 - 4.22.10
* [Minikube :octicons-link-external-16:](https://github.com/kubernetes/minikube) 1.38.1 with Kubernetes v1.35.1
* [Rancher :octicons-link-external-16:](https://rancher.com/docs/rke2/latest/en/) with Rancher Kubernetes Engine (RKE2) - 1.34 - 1.36

--8<-- [end:platforms]

This list only includes the platforms that the Percona Operators are specifically tested on as part of the release process. Other Kubernetes flavors and versions depend on the backward compatibility offered by Kubernetes itself.

## PostgreSQL Community images

Community images are available on UBI 9 and UBI 8. PostgreSQL 19 is a tech preview and ships on UBI 9 only. pgBouncer and pgBackRest community images are compatible with both UBI 8 and 9. See [PostgreSQL community images](../images-community.md).

## Percona certified images

Starting with this release, Percona certified images are available for UBI 8, 9 and 10.

The following tables list the images that you can use with the Percona Operator for PostgreSQL. 

--8<-- [start:images]

The Operator, pgBouncer, pgBackRest, Fluent Bit, and PMM images are the same on every UBI. 

PostgreSQL, PostGIS, and the upgrade images are built separately for each UBI version. The Fluent Bit image is identical for UBI 8 and UBI 9 because both use a compatible version of the `GLIBC` library. For UBI 10, a separate Fluent Bit image is provided due to incompatibility with the earlier `GLIBC` versions.

### Shared images

| Image | Digest |
| :------ | :------- |
| percona/percona-postgresql-operator:3.1.0 (x86_64) | 0f8ae7286e331e2c1d26b3fb8c8df69e9e6076fa4367edc68ed995c639f76af8 |
| percona/percona-postgresql-operator:3.1.0 (ARM64) | 8b48095df20d35558882b7677ea3292695670daa0db70f4c719f161d3ce33596 |
| percona/percona-pgbouncer:1.25.2-6 (x86_64) | 42c8629f5dd0f271e41d704250f04d96fa12a1a678a13c3743f38b64be3c1218 |
| percona/percona-pgbouncer:1.25.2-6 (ARM64) | 6a4cb60c1f9ebc75aa3408955482ba90d5649ce1f0be765e7113bd80f06dcd4f |
| percona/percona-pgbackrest:2.59.0-1 (x86_64) | c43a1e6444d3ea6d7f6421be7d030f6fb8e77692029042a1ab7975a5ac29fb20 |
| percona/percona-pgbackrest:2.59.0-1 (ARM64) | cde0676aabe64866471b6ba91a283ffcb4f507356b9554c175d9048cd4475b1c |
| percona/fluentbit:5.1.1-1 (x86_64) | 332ac2386031925cef314367366abea5cb6ec1ac0bc601b824422753346bc5df |
| percona/fluentbit:5.1.1-1 (ARM64) | 1d528ec4a8c9bab32762c83eb4e33458f2e48d9af94f0aa59bba0ce4e89904dd |
| percona/pmm-client:3.9.1 (x86_64) | 6b4309035f1fc4c0dcb6b7374ac7a01526319374a071759282a21eb016f754bf |
| percona/pmm-client:3.9.1 (ARM64) | ab419b7e10cd81fa44dd198e4a10c44dc056e87ea73fd836a66b6a2356bc4efc |
| percona/pmm-server:3.9.1 (x86_64) | f7011cf6723aba28d06b09bd7f8a1e7e1c6ba84a80a45e62cbfec80f98f20e60 |

### Percona Distribution for PostgreSQL images by UBI

=== "UBI 9 (default)"

    | Image | Digest |
    | :------ | :------- |
    | percona/percona-distribution-postgresql-upgrade:18.6-17.11-16.15-15.19-14.24-1 (x86_64) | 381fd23351231c5daf4e3c0165fb0a7766ff54e6b825fb980146bcd532f92164 |
    | percona/percona-distribution-postgresql-upgrade:18.6-17.11-16.15-15.19-14.24-1 (ARM64) | 9e8fe3a1d195a44e7c3253f58cd0c037d1511679ab54e959f37095fb58680151 |
    | percona/percona-distribution-postgresql:18.6.1-1 (x86_64) | 79ed3ec2a6ed860d0acc6d5ca2c3f42e1be5e09667e7e81ce679ebddf0a0c521 |
    | percona/percona-distribution-postgresql:18.6.1-1 (ARM64) | 7d96ddda9ec9e631d56fe8ea98f3e8253bc749791cebf073508c200e4fdabf78 |
    | percona/percona-distribution-postgresql:17.11.1-1 (x86_64) | 7fc2e29866f325e219a504c0c2338b43a179849914813eddfe88d1808d96632b |
    | percona/percona-distribution-postgresql:17.11.1-1 (ARM64) | 59dec01ddfddd5a67a3d0ce115db91c224e418e72f370855d49398c9c302c144 |
    | percona/percona-distribution-postgresql:16.15-1 (x86_64) | 7c21c743abeeddc83dab34755a077cd82051f361c23b351a1f8db9c330396032 |
    | percona/percona-distribution-postgresql:16.15-1 (ARM64) | b95d8f70e66c1e56a611434379d8e043de5d2d40491cdec09f2d2e01722f9696 |
    | percona/percona-distribution-postgresql:15.19-1 (x86_64) | 34244ac13650a82f5609fa5e0e5dadf8441762f3a3bcc3a7ceb64068906c2115 |
    | percona/percona-distribution-postgresql:15.19-1 (ARM64) | b4f7af493f56a748c8f5dafeaf968954b032b9a2255270cd0a945b376f01e4f0 |
    | percona/percona-distribution-postgresql:14.24-1 (x86_64) | bca1baae17f76318fd60a6b8d89f62b7243188c48c32451c8522b5ed52f40078 |
    | percona/percona-distribution-postgresql:14.24-1 (ARM64) | 8210804c4db24591b342f69c479fc87e36a534aa8e3c2fdc24dc71fdd2147733 |
    | percona/percona-distribution-postgresql-with-postgis:18.6.1-1 (x86_64) | 7fe794a0509a7d9c7435e568cf1a5834425e8e9988ecaab08bf731119c3485f9 |
    | percona/percona-distribution-postgresql-with-postgis:18.6.1-1 (ARM64) | 0a42e39cec3456665ee21591b79a72872d134711949a377b129a1e2e3c86e943 |
    | percona/percona-distribution-postgresql-with-postgis:17.11.1-1 (x86_64) | b29f2d90df44f40439ad571844166a20a0f057fd4bb222cf015d885db0d09744 |
    | percona/percona-distribution-postgresql-with-postgis:17.11.1-1 (ARM64) | e63f73aff4df3a2e2d99dfc44446a9c1c87bea6439652f1bbc0732a351104bf2 |
    | percona/percona-distribution-postgresql-with-postgis:16.15-1 (x86_64) | 5d4fdfb3c86c007b71bcd5a2afcc48e9d2d5c2a4ce31cdf82dc8dbc1e1951088 |
    | percona/percona-distribution-postgresql-with-postgis:16.15-1 (ARM64) | 973ef665ee7f3e4b9f19cf88e707e7271be3a678d082ff9248b1c61abf0b18b9 |
    | percona/percona-distribution-postgresql-with-postgis:15.19-1 (x86_64) | 91f43dbb0dfc6c8ec9d92ddff626d91c3f1ce113f1707f7e64e8f3d0c407de57 |
    | percona/percona-distribution-postgresql-with-postgis:15.19-1 (ARM64) | de946c2a278ac5509c6d45721d0175c79bc02438e5bbb1f80dd29db8f7df837c |
    | percona/percona-distribution-postgresql-with-postgis:14.24-1 (x86_64) | c0ad4e559f3fc14a312aed9177b9455bd313c4ff32dafb285beecf94ff41e368 |
    | percona/percona-distribution-postgresql-with-postgis:14.24-1 (ARM64) | 704442546f927c08f0344e26200b6a1ec67b7edb70b7af12d3cc919992b2bbe0 |

=== "UBI 8"

    | Image | Digest |
    | :------ | :------- |
    | percona/percona-distribution-postgresql-upgrade:18.6-17.11-16.15-15.19-14.24-1-ubi8 (x86_64) | 5fea543eaf38418f372df21fa654f4058e2b4bfb1679a2a867c92219d2cb3e79 |
    | percona/percona-distribution-postgresql-upgrade:18.6-17.11-16.15-15.19-14.24-1-ubi8 (ARM64) | a04db85445a19bc3a98593faf63e0b0247b54e6f55223c1d09c63880756fb5c5 |
    | percona/percona-distribution-postgresql:18.6.1-1-ubi8 (x86_64) | ccfa32792b2e2faa35d970387aa9fb2a2c8f8e20e41218e9c3af939f5f7b34b4 |
    | percona/percona-distribution-postgresql:18.6.1-1-ubi8 (ARM64) | 0c623e089ae1b5285e1a1823d9d7d86894b8c0ed6aa4428acbf4f29989275334 |
    | percona/percona-distribution-postgresql:17.11.1-1-ubi8 (x86_64) | 0334500a8affc9cddacc9d638f83a1405062861e3e1adec3153af24dea4ad976 |
    | percona/percona-distribution-postgresql:17.11.1-1-ubi8 (ARM64) | e92d45633e85bb3357e784bb3e450dd7fc0a364c3bce535df5b8e6374a70966b |
    | percona/percona-distribution-postgresql:16.15-1-ubi8 (x86_64) | 22dfafd64c4e264c54908a8e424b27e5cd143a45e203068908f57d7e955386f7 |
    | percona/percona-distribution-postgresql:16.15-1-ubi8 (ARM64) | 565e01a04897964f4ddb9f43abcf2cfda837e4051b865a514ebced55717524d7 |
    | percona/percona-distribution-postgresql:15.19-1-ubi8 (x86_64) | 11b0f5fb32d2317c1022dc33aed3854dfbcb667a14540b6ec388a169db1d273e |
    | percona/percona-distribution-postgresql:15.19-1-ubi8 (ARM64) | 2167dd99e5d864641b590dd5c09389926b276cedbc0067533754a594d148e00c |
    | percona/percona-distribution-postgresql:14.24-1-ubi8 (x86_64) | d86f4191562f3e382e23d0a146fd50596728a8bc8d1bf808e5edb34e589e75fc |
    | percona/percona-distribution-postgresql:14.24-1-ubi8 (ARM64) | d082df7823039830ac8e876f80b75e5b72957200442d8eb40fe20da7fcf158ce |
    | percona/percona-distribution-postgresql-with-postgis:18.6.1-1-ubi8 (x86_64) | 428f5fe953f34dc0f3c8d371fc5a1211a44320c365bacaafc80facd1621101df |
    | percona/percona-distribution-postgresql-with-postgis:18.6.1-1-ubi8 (ARM64) | 5786d93789d294c8c2fae22b24f94e66f8adfffeee2b46a312f40fcd38ec6ed6 |
    | percona/percona-distribution-postgresql-with-postgis:17.11.1-1-ubi8 (x86_64) | f46f8c8d51ea4e63d25d1bde9f39f5a67675e2660ea0aded1c99e247b9b1aa58 |
    | percona/percona-distribution-postgresql-with-postgis:17.11.1-1-ubi8 (ARM64) | 450aa7578f786e9180a2b0a001637f996b8da35a56015c5ccbd48ca12793f3e6 |
    | percona/percona-distribution-postgresql-with-postgis:16.15-1-ubi8 (x86_64) | 74209572a2503dd31d3bbfd946d740746a450bb1243617fcd5dedb168a7acb12 |
    | percona/percona-distribution-postgresql-with-postgis:16.15-1-ubi8 (ARM64) | ecc718a03d3e0717f96c5bb66e51b5803ace8c55d70e38dca60d10f8c09e10f8 |
    | percona/percona-distribution-postgresql-with-postgis:15.19-1-ubi8 (x86_64) | 00957d831c394f8a717d38ea956d94c3d6e4a169496b72b1952e1e9c9c6701a4 |
    | percona/percona-distribution-postgresql-with-postgis:15.19-1-ubi8 (ARM64) | 88d81ca7a8ed3a449378ec58546d7b4cb64b8638a91b8c7d7e85d527a0135694 |
    | percona/percona-distribution-postgresql-with-postgis:14.24-1-ubi8 (x86_64) | 2fae3ef7ca669da03033523e1af80023ccad1617ae98808a9ce11758c45f24fb |
    | percona/percona-distribution-postgresql-with-postgis:14.24-1-ubi8 (ARM64) | 896a3dd8be9eab2c4966cfed782db5e74c4f04e2a6b3a6e78cf15d212d83d9c6 |

=== "UBI 10"

    | Image | Digest |
    | :------ | :------- |
    | percona/percona-distribution-postgresql-upgrade:18.6-17.11-16.15-15.19-14.24-1-ubi10 (x86_64) | 96ecb9c13a70bd4ef83d6b5d7c0090adcae0e2737ddd411f36416537f66274c6 |
    | percona/percona-distribution-postgresql-upgrade:18.6-17.11-16.15-15.19-14.24-1-ubi10 (ARM64) | a01f6df4bb05b68ea5383a9c174505c1252c8de21de51e34dc9069903012238a |
    | percona/percona-distribution-postgresql:18.6.1-1-ubi10 (x86_64) | 7eb5e275575b7015cf5d52a3478a0f7df4a53ed3fd58330152f7ec59d31f57c8 |
    | percona/percona-distribution-postgresql:18.6.1-1-ubi10 (ARM64) | ec60edcd31bd4e96fca20feec0419f7af039728a57c0e8854edc784b34fb2450 |
    | percona/percona-distribution-postgresql:17.11.1-1-ubi10 (x86_64) | fe1e00fee82c23995cfcdae5778c3396a60f30bcbf690100fa30f550f0ef8fea |
    | percona/percona-distribution-postgresql:17.11.1-1-ubi10 (ARM64) | 10450bf4d5ebfc332e95a8bbfa82bb692406133b6fe28f163db510afec9b6729 |
    | percona/percona-distribution-postgresql:16.15-1-ubi10 (x86_64) | 37428c79747f0d818bc845f34b5f07dac2d7b063ed4e25268ba4dc24d7781059 |
    | percona/percona-distribution-postgresql:16.15-1-ubi10 (ARM64) | 2ac8bea41b904fe3740577e82aff3274caf1c13cfc4b9d28f862e8939793a072 |
    | percona/percona-distribution-postgresql:15.19-1-ubi10 (x86_64) | d210a61c313619f488778b6847411df03a40bbb8a01f98b9d3ecc681e0e0baac |
    | percona/percona-distribution-postgresql:15.19-1-ubi10 (ARM64) | cd086772227a7a6bcc8730dafafcdf39bbfd9a79b7e2664c6abdf8098c69dc4b |
    | percona/percona-distribution-postgresql:14.24-1-ubi10 (x86_64) | b52437159bc53a9ef53e792f33db83c7ee5a1a30a02e7407a8c5a839357bfd41 |
    | percona/percona-distribution-postgresql:14.24-1-ubi10 (ARM64) | 4db8cec87861a3c9ca3227e266f3b7c4349579795a96aa3869c0c52feed2caab |
    | percona/percona-distribution-postgresql-with-postgis:18.6.1-1-ubi10 (x86_64) | baaaa40b7478710bbe341247deeba9b25cd37fa3aad2774d1d8f47d8fd3b7edc |
    | percona/percona-distribution-postgresql-with-postgis:18.6.1-1-ubi10 (ARM64) | 37e15d2b2ab4b4c96880666526da8508b158252ca88e262d52c80912e2282afe |
    | percona/percona-distribution-postgresql-with-postgis:17.11.1-1-ubi10 (x86_64) | f6ca9eee3f1594012d97aa8b45174e88f34bcebd140096b3849228f103d491a5 |
    | percona/percona-distribution-postgresql-with-postgis:17.11.1-1-ubi10 (ARM64) | 7e57f1e29100988e9e697222a8584ec8a3df1548ccf53d14cf7220277e5b4d22 |
    | percona/percona-distribution-postgresql-with-postgis:16.15-1-ubi10 (x86_64) | be7ad829ede65279e3bf43501dc5ce0e65aab191be2990a2777dd3842ebcd66d |
    | percona/percona-distribution-postgresql-with-postgis:16.15-1-ubi10 (ARM64) | b42049d0d9ddb9fbf3890fee82fa179595958e483c90c84242f8c8bd0215174b |
    | percona/percona-distribution-postgresql-with-postgis:15.19-1-ubi10 (x86_64) | ac3edbb3bde34f02c1ff8e93b19f8f2379e9c561bd42b81931b4bc1b6860a0c0 |
    | percona/percona-distribution-postgresql-with-postgis:15.19-1-ubi10 (ARM64) | 6126f0b62370ece4bcde3a38876ee4692dc5602762c2c7536176a8fbec9bbaac |
    | percona/percona-distribution-postgresql-with-postgis:14.24-1-ubi10 (x86_64) | 52993f88d0ec6759c5b6258ec2a9ed0da0638c087fcccae6b61d7213c44d6cbe |
    | percona/percona-distribution-postgresql-with-postgis:14.24-1-ubi10 (ARM64) | 5f73108ca08c8b2830ac28a6ea2ee2a750b7ea7f2ca8f045065cb44eba427190 |
    | percona/fluentbit:5.1.1-1-ubi10 (x86_64) | 6deee2b13c03511605ecfb3fec1d5e5121aee63fa425c5bd4c9b51fe1a76ff7d |
    | percona/fluentbit:5.1.1-1-ubi10 (ARM64) | 77dd38e8bee9ddadfe5e0813519415c780ab044b17832a7faa5e940d8e2b6017 |

--8<-- [end:images]
