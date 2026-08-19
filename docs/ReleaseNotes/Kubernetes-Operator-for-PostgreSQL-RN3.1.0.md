# Percona Operator for PostgreSQL 3.1.0 ({{date.3_1_0}})

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

* [Declarative logical replicas for read-only workloads](#define-logical-replicas-declaratively)

### Images and platforms

* [Community PostgreSQL images and custom registries](#support-for-community-postgresql-images)
* [PostgreSQL 19 support](#support-of-postgresql-19-tech-preview) (tech preview)
* [Official support for Rancher Kubernetes Engine (RKE2)](#official-support-for-rancher-kubernetes-engine-rke2)
* [Full ARM64 support for Operator images](#the-operator-is-now-fully-supported-on-arm64-architectures)

### Upgrade notes

* [PMM2 support removed](#deprecation-change-rename-and-removal) — upgrade to PMM3
* [Operator 2.8.0 support dropped from CRDs](#deprecation-change-rename-and-removal)
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

### Define logical replicas declaratively

You can now add a read-only logical replica in the same cluster and point reporting or other heavy reads at this replica instead of the primary. The replica has its own volume and Service, so those queries do not compete with your high-availability set.

Declare the replica in the Custom Resource when you create the cluster or later during runtime. You can also define which databases receive the changes after the replica is bootstrapped.

The Operator creates the volume, copies the data, converts the physical replica to the logical one and keeps the databases you list in sync. It also creates a Service you can connect to. 

Patroni does not manage nor promote it, so it stays a stable read endpoint.

Logical replicas require PostgreSQL 17 or later. See [Deploy a logical replica](deploy-replica.md).

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

Starting with this release, you can control the Operator’s behavior with the `spec.tls.certManagementPolicy` option in the Custom Resource. Available policies are:

* `auto` (default) — Keeps the existing behavior. If TLS Secrets are missing, the Operator creates new certificates automatically.
* `userProvidedOnly` — Certificate lifecycle stays entirely under your control. The Operator does not create or replace TLS certificates, if a TLS Secret is temporarily unavailable. In this way, your applications can keep using the existing certificates while you restore access to the Secret.
  
```yaml
spec:
  tls:
    mode: preferTLS
    certManagementPolicy: userProvidedOnly
    allowInvalidCertificates: false
  secrets:
    ssl: my-cluster-name-ssl
    sslInternal: my-cluster-name-ssl-internal
```

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

### Support for community PostgreSQL images

With this release, you can deploy PostgreSQL Community images or your own PostgreSQL images under your own registry and tags with the Operator. To do this, define them under the `spec.image`, `spec.proxy.pgBouncer.image`, and `spec.backups.pgbackrest.image` options in the Custom Resource. The Operator automates database deployment and management with these images the same way it does for Percona Distribution for PostgreSQL.

This compatibility gives you full control and transparency over your infrastructure enabling you to use extensions not available in Percona images. However, you cannot use features such as [Transparent data encryption](#transparent-data-encryption-support-with-pg_tde) that are available only in Percona images, and you are fully responsible for the image lifecycle and support.

Community packages are available for UBI8 and UBI9 base images, allowing you to quickly spin them up for testing and evaluation before building your own pipeline. These images are not bound to a specific Operator version, but you must use Operator version 3.1.0 or later to deploy community or custom PostgreSQL images.

For more information about using community images and building your own ones, refer to the Percona Blog: [Community Docker Images: keeping the operator open without a vendor registry lock in](https://www.percona.com/blog/postgresql-community-images-operator/) by Slava Sarzhan and our [documentation](../install-community.md).

### Support of PostgreSQL 19 (tech preview)

With this release, the Operator supports deployment of Community PostgreSQL 19. This support is currently in the tech preview stage because this major version is not officially released yet. However, you can already deploy it and evaluate the features coming with this version. This allows you to stay on top of upcoming enhancements and gives you enough time to prepare your upgrade and migration plans before the final release lands. See [Deploy the Operator with Community images](install-community.md) for guidelines.

### Official support for Rancher Kubernetes Engine (RKE2)

[Rancher Kubernetes Engine (RKE2) :octicons-link-external-16:](https://docs.rke2.io/) is now an officially supported platform. Every Operator release is now tested on RKE2 to ensure that you can run it on Rancher-managed Kubernetes clusters with confidence.

### The Operator is now fully supported on ARM64 architectures

All Operator images are now available for ARM64, giving you native support on ARM based clusters with no extra setup.

## Deprecation, Change, Rename and Removal

* Removed support for PMM2. This Operator release no longer supports PMM2 as it has reached the end-of-life state. Upgrade to PMM3 as soon as possible. For how to upgrade, refer to [PMM documentation :octicons-link-external-16:](https://docs.percona.com/percona-monitoring-and-management/3/pmm-upgrade/migrating_from_pmm_2.html).

* The support of version 2.8.0 is dropped from CRDs. 
* The `extensions.builtin` section is deprecated and will be removed after version 3.4.0. We encourage you to use `extensions.<extension>.enabled`. You can still use the old form during the transition. If both forms are set at the same time, `extensions.builtin` takes precedence.
* `pg_cron` and `set_user` extensions have been added to the list of built-in extensions. Your existing setup via the `extensions.custom` remains unchanged and works as expected after the upgrade. To switch to using built-in extensions, do the following:
   * Remove the extension from the `extensions.custom` list
   * Set `extensions.pg_cron.enabled` or `extensions.set_user.enabled` to `true`. 
   
   You must do these changes simultaneously for the same reconciliation loop. Just removing the extension `extensions.custom` list instructs the Operator to delete it.



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

* [K8SPG-951](https://perconadev.atlassian.net/browse/K8SPG-951) - Added the support of custom CA issuer so you can plug in your own cert-manager Issuer or ClusterIssuer instead of the hardcoded self-signed CA. This lets you issue cluster TLS certificates from Vault, ACME, or an existing corporate CA.

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

This Operator version is developed, tested and based on:

--8<-- [start:software]

* PostgreSQL 14.23-1, 15.18-1, 16.14-1, 17.10-1, 18.4-1 as the database. Other versions may also work but have not been tested.
* pgBackRest 2.58.0-2 for backup and recovery
* pgBouncer 1.25.2-1 for connection pooling
* Patroni version 4.1.3 for high-availability
* PostGIS version 3.5.6
* PMM Client version 2.44.1-1 and 3.7.1


--8<-- [end:software]

## Supported platforms

Percona Operators are designed for compatibility with all [CNCF-certified :octicons-link-external-16:](https://www.cncf.io/training/certification/software-conformance/) Kubernetes distributions. 

Our release process includes targeted testing and validation on major cloud provider platforms and OpenShift, as detailed below:

--8<-- [start:platforms]

* [Google Kubernetes Engine (GKE) :octicons-link-external-16:](https://cloud.google.com/kubernetes-engine) 1.33 - 1.35
* [Amazon Elastic Container Service for Kubernetes (EKS) :octicons-link-external-16:](https://aws.amazon.com) 1.33 - 1.35
* [OpenShift :octicons-link-external-16:](https://www.redhat.com/en/technologies/cloud-computing/openshift) 4.18 - 4.21
* [Azure Kubernetes Service (AKS) :octicons-link-external-16:](https://azure.microsoft.com/en-us/services/kubernetes-service/) 1.33 - 1.35
* [Minikube :octicons-link-external-16:](https://github.com/kubernetes/minikube) 1.38.1 with Kubernetes v1.35.1

--8<-- [end:platforms]

This list only includes the platforms that the Percona Operators are specifically tested on as part of the release process. Other Kubernetes flavors and versions depend on the backward compatibility offered by Kubernetes itself.

## Percona certified images

Find Percona's certified Docker images that you can use with the Percona Operator for PostgreSQL in the following table.


--8<-- [start:images]

| Image                                                                | Digest                                                           |
|:---------------------------------------------------------------------|:-----------------------------------------------------------------|
| percona/percona-postgresql-operator:3.0.0 (x86_64)                    | 3bcbaec261b2e67c81b3812a4b220c859434b6791c53ee1fb7ecb66bd179de56 |
| percona/percona-postgresql-operator:3.0.0 (ARM64)                    | 5aacf965c3d7bc89a23e1292ae47c2ef89d590e77677d793e15f56b11e5d67f7 |
| percona/percona-distribution-postgresql-upgrade:18.4-17.10-16.14-15.18-14.23-1 (x86_64) | 31a9612320d3b08cb74d5e98f86b054c4562e4b900140152b28476be62f086f5 |
| percona/percona-distribution-postgresql-upgrade:18.4-17.10-16.14-15.18-14.23-1 (ARM64) | 81a831086fc4aaee83af8d86b1422b64ce77e200a8f27627c27282c9af6ad9b8 |
| percona/percona-distribution-postgresql:18.4-1 (x86_64)               | ca25cc5e291cf2307d9ec4c29811c6f6d93171f98dd2cb4c69d2036f07517a7d |
| percona/percona-distribution-postgresql:18.4-1 (ARM64)               | fae3368e04b80f4eb887621724074db4db279ca59743aacb47de51b468d514f5 |
| percona/percona-distribution-postgresql:17.10-1 (x86_64)               | 720bf87ef8cda340f833981a674d5dc71283cb39af3fd4ef97eff4ccf910b87a |
| percona/percona-distribution-postgresql:17.10-1 (ARM64)               | 6416424e58765b9434f18905f0338d466cb79bafc42e6a5570030c71a1323eee |
| percona/percona-distribution-postgresql:16.14-1 (x86_64)              | ad84dc4fa537a5ba03c7c1f51f9a1ee959132155b6943d02cb0d614fc57e4271 |
| percona/percona-distribution-postgresql:16.14-1 (ARM64)              | f377d7fd5e5e3eae56ef5886aa77691c436269bae5decb706130061286080465 |
| percona/percona-distribution-postgresql:15.18-1 (x86_64)              | 60728795a6e954d9255526a208e8e9e8e93278d4c1e89004f2999a6ccb196eea |
| percona/percona-distribution-postgresql:15.18-1 (ARM64)              | 78b1b7488a897ffaf609c8d1edc6c5a27b76a3c697bbb24db5f2dec3fd66ee34 |
| percona/percona-distribution-postgresql:14.23-1 (x86_64)               | d04d3e1c41fd0c9fe438ab04081c555e1edafaed9a33f2979c7b0080045ff5fd |
| percona/percona-distribution-postgresql:14.23-1 (ARM64)              | 88925bdfc04d7dec629230c3b0f31daf7f9aed8757b2456a4439475a6b3175f5 |
| percona/percona-distribution-postgresql-with-postgis:18.4-2 (x86_64)   | 763d037b012a8856ff5ede045631d2f9b9a792b5e8281b756cfb3e017b0395e9 |
| percona/percona-distribution-postgresql-with-postgis:18.4-2 (ARM64)  | 5f7561ebfc4f7d3e237953b1aae2b41d6bb01d7e7c55e04e2666dd5775cc671a |
| percona/percona-distribution-postgresql-with-postgis:17.10-2 (x86_64)   | fcaccb00ea6937e43c7b4b27a36191faed94dae1cf7ab5ccdc73bb0444984ada |
| percona/percona-distribution-postgresql-with-postgis:17.10-2 (ARM64)  | 7e28bb3effd1492057005f8c6c9bd6c3c3aba4ed45f8a01a771adb6e7458537e |
| percona/percona-distribution-postgresql-with-postgis:16.14-2 (x86_64) | 97222e27f34ee5151ed86bf124598004c13ba1c4034eb591641a6eafddd17df1 |
| percona/percona-distribution-postgresql-with-postgis:16.14-2 (ARM64) | 251e8fe4fae00ca7562f3ea66620dcfdb1c0bd7989bb501922ac16326da0dc53 |
| percona/percona-distribution-postgresql-with-postgis:15.18-2 (x86_64) | 36651cb8711644763676e6ff6b7756647af55402fbae9a1bcf6336392e78bfc5 |
| percona/percona-distribution-postgresql-with-postgis:15.18-2 (ARM64) | a4a557f1490bdb1611d3d1026de227608112e6e2b752e98eab95b660193d53e8 |
| percona/percona-distribution-postgresql-with-postgis:14.23-2 (x86_64) | 5d418d47c8442620ddf4063c9d147fda932153a7d9b7e0098ba58d9ecd640b9d |
| percona/percona-distribution-postgresql-with-postgis:14.23-2 (ARM64) | 947af4d80224fa0b7031448beec3fb965b5d321e4fa5d742753dba9079667799 |
| percona/percona-pgbackrest:2.58.0-2 (x86_64)                          | 0b792f3d0bcfdd7a72c8d74f1c905469486f106db8f9299b5216d23dacf80501 |
| percona/percona-pgbackrest:2.58.0-2 (ARM64)                          | 97361155cdce8642ce47ebe83766a0c7b825930adb6c055d78476756db02fa9f |
| percona/percona-pgbouncer:1.25.2-1 (x86_64)                          | 25881754364b7a2aaad716bfc77d292a7a0f145c200162cc392874e09bae7918 |
| percona/percona-pgbouncer:1.25.2-1 (ARM64)                           | 8f1bbf2159b6089c235dd512aa397ee53cd84e7e34554238e7981c45bf33767f |
| percona/pmm-client:3.7.1 (x86_64)                                    | 8b98629a469bf6360b14eb3ea121687737870261296f64e4587f6a6723a6845b |
| percona/pmm-client:3.7.1 (ARM64)                                     | 9951a74522a6bd70531457628daca758ffa3363941938539d164e592188e23e3 |
| percona/pmm-client:2.44.1-1 (x86_64)                                  | 52a8fb5e8f912eef1ff8a117ea323c401e278908ce29928dafc23fac1db4f1e3 |
| percona/pmm-client:2.44.1-1 (ARM64)                                  | 390bfd12f981e8b3890550c4927a3ece071377065e001894458047602c744e3b |


--8<-- [end:images]
