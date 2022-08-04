# [Custom Resource options](operator.html#operator-custom-resource-options)

The Cluster is configured via the
[deploy/cr.yaml](https://github.com/percona/percona-postgresql-operator/blob/main/deploy/cr.yaml) file.

The metadata part of this file contains the following keys:


* `name` (`cluster1` by default) sets the name of your Percona Distribution
for PostgreSQL Cluster; it should include only [URL-compatible characters](https://datatracker.ietf.org/doc/html/rfc3986#section-2.3), not exceed 22 characters, start with an alphabetic character, and end with an alphanumeric character;

The spec part of the [deploy/cr.yaml](https://github.com/percona/percona-postgresql-operator/blob/main/deploy/cr.yaml) file contains the following sections:

| Key            | Value type                                 | Default | Description |
| -------------- | ------------------------------------------ | ------- | ----------- |
| pause          | boolean                                    | `false` | Pause/resume: setting it to `true` gracefully stops the cluster, and setting it to `false` after shut down starts the cluster back. |
| upgradeOptions | [subdoc](#upgrade-options-section)         |         | Percona Distribution for PostgreSQL upgrade options section |
| pgPrimary      | [subdoc](#pgprimary-section)               |         | PostgreSQL Primary instance options section |
| walStorage     | [subdoc](#tablespaces-storage-section)     |         | Tablespaces Storage Section |
| walStorage     | [subdoc](#write-ahead-log-storage-section) |         | Write-ahead Log Storage Section |
| backup         | [subdoc](#backup-section)                  |         | Section to configure backups and pgBackRest |
| pmm            | [subdoc](#pmm-section)                     |         | Percona Monitoring and Management section |
| pgBouncer      | [subdoc](#pgbouncer-section)               |         | The [pgBouncer](http://pgbouncer.github.io/) connection pooler section |
| pgReplicas     | [subdoc](#pgreplicas-section)              |         | Section required to manage the replicas within a PostgreSQL cluster |
| pgBadger       | [subdoc](#pgbadger-section)                |         | The [pgBadger](https://github.com/darold/pgbadger) PostgreSQL log analyzer section |

|                 | |
|-----------------|-|
| **Key**         | {{ optionlink('database','spec') }} |
| **Value**       | string |
| **Example**     | `pgdb` |
| **Description** | The name of a database that the PostgreSQL user can log into after the PostgreSQL cluster is created |
|                 | |
| **Key**         | {{ optionlink('disableAutofail','spec') }} |
| **Value**       | boolean |
| **Example**     | `false` |
| **Description** | Turns high availability on or off. By default, every cluster can have high availability if there is at least one replica |
|                 | |
| **Key**         | {{ optionlink('tlsOnly','spec') }} |
| **Value**       | boolean |
| **Example**     | `false` |
| **Description** | Enforece Operator to use only Transport Layer Security (TLS) for both internal and external communications |
|                 | |
| **Key**         | {{ optionlink('sslCA','spec') }} |
| **Value**       | string |
| **Example**     | `cluster1-ssl-ca` |
| **Description** | The name of the secret with TLS  used for both connection encryption (external traffic), and replication (internal traffic) |
|                 | |
| **Key**         | {{ optionlink('sslSecretName','spec') }} |
| **Value**       | string |
| **Example**     | `cluster1-ssl-keypair` |
| **Description** | The name of the secret created to encrypt external communications |
|                 | |
| **Key**         | {{ optionlink('sslReplicationSecretName','spec') }} |
| **Value**       | string |
| **Example**     | `cluster1-ssl-keypair"` |
| **Description** | The name of the secret created to encrypt internal communications |
|                 | |
| **Key**         | {{ optionlink('keepData','spec') }} |
| **Value**       | boolean |
| **Example**     | `true` |
| **Description** | If `true`, PVCs will be kept after the cluster deletion |
|                 | |
| **Key**         | {{ optionlink('keepBackups','spec') }} |
| **Value**       | boolean |
| **Example**     | `true` |
| **Description** | If `true`, local backups will be kept after the cluster deletion |
|                 | |
| **Key**         | {{ optionlink('pgDataSource.restoreFrom') }} |
| **Value**       | string |
| **Example**     | `""` |
| **Description** | The name of a data source PostgreSQL cluster, which is used to [restore backup to a new cluster](backups.md#backups-restore) |
|                 | |
| **Key**         | {{ optionlink('pgDataSource.restoreOpts') }} |
| **Value**       | string |
| **Example**     | `""` |
| **Description** | Custom pgBackRest options to [restore backup to a new cluster](backups.md#backups-restore) |

## Upgrade Options Section

The `upgradeOptions` section in the [deploy/cr.yaml](https://github.com/percona/percona-postgresql-operator/blob/main/deploy/cr.yaml) file contains various configuration options to control Percona Distribution for PostgreSQL upgrades.

|                 | |
|-----------------|-|
| **Key**         | {{ optionlink('upgradeOptions.versionServiceEndpoint') }} |
| **Value**       | string |
| **Example**     | `https://check.percona.com` |
| **Description** | The Version Service URL used to check versions compatibility for upgrade |
|                 | |
| **Key**         | {{ optionlink('upgradeOptions.apply') }} |
| **Value**       | string |
| **Example**     | `disabled` |
| **Description** | Specifies how [updates are processed](update.md#operator-update-smartupdates) by the Operator. `Never` or `Disabled` will completely disable automatic upgrades, otherwise it can be set to `Latest` or `Recommended` or to a specific version number of Percona Distribution for PostgreSQL to have it version-locked (so that the user can control the version running, but use automatic upgrades to move between them).|
|                 | |
| **Key**         | {{ optionlink('upgradeOptions.schedule') }} |
| **Value**       | string |
| **Example**     | `0 2 \* \* \*` |
| **Description** | Scheduled time to check for updates, specified in the [crontab format](https://en.wikipedia.org/wiki/Cron) |

## pgPrimary Section

The pgPrimary section controls the PostgreSQL Primary instance.

|                 | |
|-----------------|-|
| **Key**         | {{ optionlink('pgPrimary.image') }} |
| **Value**       | string |
| **Example**     | `perconalab/percona-postgresql-operator:main-ppg13-postgres-ha` |
| **Description** | The Docker image of the PostgreSQL Primary instance |
|                 | |
| **Key**         | {{ optionlink('pgPrimary.imagePullPolicy') }} |
| **Value**       | string |
| **Example**     | `Always` |
| **Description** | This option is used to set the [policy](https://kubernetes.io/docs/concepts/containers/images/#updating-images) for updating pgPrimary and pgReplicas images |
|                 | |
| **Key**         | {{ optionlink('pgPrimary.resources.requests.memory') }} |
| **Value**       | int |
| **Example**     | `256Mi` |
| **Description** | The [Kubernetes memory requests](https://kubernetes.io/docs/concepts/configuration/manage-compute-resources-container/#resource-requests-and-limits-of-pod-and-container) for a PostgreSQL Primary container |
|                 | |
| **Key**         | {{ optionlink('pgPrimary.resources.requests.cpu') }} |
| **Value**       | string |
| **Example**     | `500m` |
| **Description** | [Kubernetes CPU requests](https://kubernetes.io/docs/concepts/configuration/manage-compute-resources-container/#resource-requests-and-limits-of-pod-and-container) for a PostgreSQL Primary container |
|                 | |
| **Key**         | {{ optionlink('pgPrimary.resources.limits.cpu') }} |
| **Value**       | string |
| **Example**     | `500m` |
| **Description** | [Kubernetes CPU limits](https://kubernetes.io/docs/concepts/configuration/manage-compute-resources-container/#resource-requests-and-limits-of-pod-and-container) for a PostgreSQL Primary container |
|                 | |
| **Key**         | {{ optionlink('pgPrimary.resources.limits.memory') }} |
| **Value**       | string |
| **Example**     | `256Mi` |
| **Description** | The [Kubernetes memory limits](https://kubernetes.io/docs/concepts/configuration/manage-compute-resources-container/#resource-requests-and-limits-of-pod-and-container) for a PostgreSQL Primary container |
|                 | |
| **Key**         | {{ optionlink('pgPrimary.affinity.antiAffinityType') }} |
| **Value**       | string |
| **Example**     | `preferred` |
| **Description** | [Pod anti-affinity type](constraints.md#affinity-and-anti-affinity), can be either `preferred` or `required` |
|                 | |
| **Key**         | {{ optionlink('pgPrimary.affinity.nodeAffinityType') }} |
| **Value**       | string |
| **Example**     | `preferred` |
| **Description** | [Node affinity type](constraints.md#affinity-and-anti-affinity), can be either `preferred` or `required` |
|                 | |
| **Key**         | {{ optionlink('pgPrimary.affinity.nodeLabel') }} |
| **Value**       | label |
| **Example**     | `kubernetes.io/region: us-central1` |
| **Description** | Set [labels](https://kubernetes.io/docs/concepts/overview/working-with-objects/labels/) for [PostgreSQL instances Node affinity](constraints.md#simple-approach-configure-node-affinity-based-on-nodelabel) |
|                 | |
| **Key**         | {{ optionlink('pgPrimary.affinity.advanced') }} |
| **Value**       | subdoc |
| **Example**     | |
| **Description** | [Allows using standard Kubernetes affinity constraints](constraints.md#advanced-approach-use-standard-kubernetes-constraints) for advanced affinity and anti-affinity tuning |
|                 | |
| **Key**         | {{ optionlink('pgPrimary.volumeSpec.size') }} |
| **Value**       | int |
| **Example**     | `1G` |
| **Description** | The [Kubernetes PersistentVolumeClaim](https://kubernetes.io/docs/concepts/storage/persistent-volumes/#persistentvolumeclaims) size for the PostgreSQL Primary storage |
|                 | |
| **Key**         | {{ optionlink('pgPrimary.tolerations') }} |
| **Value**       | subdoc |
| **Example**     | `node.alpha.kubernetes.io/unreachable` |
| **Description** | [Kubernetes Pod tolerations](https://kubernetes.io/docs/concepts/configuration/taint-and-toleration/) |
|                 | |
| **Key**         | {{ optionlink('pgPrimary.volumeSpec.size') }} |
| **Value**       | int |
| **Example**     | `1G` |
| **Description** | The [Kubernetes PersistentVolumeClaim](https://kubernetes.io/docs/concepts/storage/persistent-volumes/#persistentvolumeclaims) size for the PostgreSQL Primary storage |
|                 | |
| **Key**         | {{ optionlink('pgPrimary.volumeSpec.accessmode') }} |
| **Value**       | string |
| **Example**     | `ReadWriteOnce` |
| **Description** | The [Kubernetes PersistentVolumeClaim](https://kubernetes.io/docs/concepts/storage/persistent-volumes/#persistentvolumeclaims) access modes for the PostgreSQL Primary storage |
|                 | |
| **Key**         | {{ optionlink('pgPrimary.volumeSpec.storagetype') }} |
| **Value**       | string |
| **Example**     | `dynamic` |
| **Description** | Type of the PostgreSQL Primary storage provisioning: `create` (the default variant; used if storage is provisioned, e.g. using hostpath) or `dynamic` (for a dynamic storage provisioner, e.g. via a StorageClass) |
|                 | |
| **Key**         | {{ optionlink('pgPrimary.volumeSpec.storageclass') }} |
| **Value**       | string |
| **Example**     | `""` |
| **Description** | Optionally sets the [Kubernetes storage class](https://kubernetes.io/docs/concepts/storage/storage-classes/) to use with the PostgreSQL Primary storage [PersistentVolumeClaim](https://kubernetes.io/docs/concepts/storage/persistent-volumes/#persistentvolumeclaims) |
|                 | |
| **Key**         | {{ optionlink('pgPrimary.volumeSpec.matchLabels') }} |
| **Value**       | string |
| **Example**     | `""` |
| **Description** | A PostgreSQL Primary storage [label selector](https://kubernetes.io/docs/concepts/storage/persistent-volumes/#selector) |
|                 | |
| **Key**         | {{ optionlink('pgPrimary.imagePullPolicy') }} |
| **Value**       | string |
| **Example**     | `Always` |
| **Description** | This option is used to set the [policy](https://kubernetes.io/docs/concepts/containers/images/#updating-images) for updating pgPrimary and pgReplicas images |
|                 | |
| **Key**         | {{ optionlink('pgPrimary.customconfig') }} |
| **Value**       | string |
| **Example**     | `""` |
| **Description** | Name of the [Custom configuration options ConfigMap](options.md#operator-configmaps) for PostgreSQL cluster |

## Tablespaces Storage Section

The `tablespaceStorages` section in the [deploy/cr.yaml](https://github.com/percona/percona-postgresql-operator/blob/main/deploy/cr.yaml)
file contains configuration options for PostgreSQL [Tablespace](https://www.postgresql.org/docs/current/manage-ag-tablespaces.html).

|                 | |
|-----------------|-|
| **Key**         | {{ optionlink('tablespaceStorages.&lt;storage-name&gt;.volumeSpec.size') }} |
| **Value**       | int |
| **Example**     | `1G` |
| **Description** | The [Kubernetes PersistentVolumeClaim](https://kubernetes.io/docs/concepts/storage/persistent-volumes/#persistentvolumeclaims) size for the PostgreSQL Tablespaces storage |
|                 | |
| **Key**         | {{ optionlink('tablespaceStorages.&lt;storage-name&gt;.volumeSpec.accessmode') }} |
| **Value**       | string |
| **Example**     | `ReadWriteOnce` |
| **Description** | The [Kubernetes PersistentVolumeClaim](https://kubernetes.io/docs/concepts/storage/persistent-volumes/#persistentvolumeclaims) access modes for the PostgreSQL Tablespaces storage |
|                 | |
| **Key**         | {{ optionlink('tablespaceStorages.&lt;storage-name&gt;.volumeSpec.storagetype') }} |
| **Value**       | string |
| **Example**     | `dynamic` |
| **Description** | Type of the PostgreSQL Tablespaces storage provisioning: `create` (the default variant; used if storage is provisioned, e.g. using hostpath) or `dynamic` (for a dynamic storage provisioner, e.g. via a StorageClass) |
|                 | |
| **Key**         | {{ optionlink('tablespaceStorages.&lt;storage-name&gt;.volumeSpec.storageclass') }} |
| **Value**       | string |
| **Example**     | `""` |
| **Description** | Optionally sets the [Kubernetes storage class](https://kubernetes.io/docs/concepts/storage/storage-classes/) to use with the PostgreSQL Tablespaces storage [PersistentVolumeClaim](https://kubernetes.io/docs/concepts/storage/persistent-volumes/#persistentvolumeclaims) |
|                 | |
| **Key**         | {{ optionlink('tablespaceStorages.&lt;storage-name&gt;.volumeSpec.matchLabels') }} |
| **Value**       | string |
| **Example**     | `""` |
| **Description** | A PostgreSQL Tablespaces storage [label selector](https://kubernetes.io/docs/concepts/storage/persistent-volumes/#selector) |

## Write-ahead Log Storage Section

The `walStorage` section in the [deploy/cr.yaml](https://github.com/percona/percona-postgresql-operator/blob/main/deploy/cr.yaml)
file contains configuration options for PostgreSQL [write-ahead logging](https://www.postgresql.org/docs/current/wal-intro.html).

|                 | |
|-----------------|-|
| **Key**         | {{ optionlink('walStorage.volumeSpec.size') }} |
| **Value**       | int |
| **Example**     | `1G` |
| **Description** | The [Kubernetes PersistentVolumeClaim](https://kubernetes.io/docs/concepts/storage/persistent-volumes/#persistentvolumeclaims) size for the PostgreSQL Write-ahead Log storage |
|                 | |
| **Key**         | {{ optionlink('walStorage.volumeSpec.accessmode') }} |
| **Value**       | string |
| **Example**     | `ReadWriteOnce` |
| **Description** | The [Kubernetes PersistentVolumeClaim](https://kubernetes.io/docs/concepts/storage/persistent-volumes/#persistentvolumeclaims) access modes for the PostgreSQL Write-ahead Log storage |
|                 | |
| **Key**         | {{ optionlink('walStorage.volumeSpec.storagetype') }} |
| **Value**       | string |
| **Example**     | `dynamic` |
| **Description** | Type of the PostgreSQL Write-ahead Log storage provisioning: `create` (the default variant; used if storage is provisioned, e.g. using hostpath) or `dynamic` (for a dynamic storage provisioner, e.g. via a StorageClass) |
|                 | |
| **Key**         | {{ optionlink('walStorage.volumeSpec.storageclass') }} |
| **Value**       | string |
| **Example**     | `""` |
| **Description** | Optionally sets the [Kubernetes storage class](https://kubernetes.io/docs/concepts/storage/storage-classes/) to use with the PostgreSQL Write-ahead Log storage [PersistentVolumeClaim](https://kubernetes.io/docs/concepts/storage/persistent-volumes/#persistentvolumeclaims) |
|                 | |
| **Key**         | {{ optionlink('walStorage.volumeSpec.matchLabels') }} |
| **Value**       | string |
| **Example**     | `""` |
| **Description** | A PostgreSQL Write-ahead Log storage [label selector](https://kubernetes.io/docs/concepts/storage/persistent-volumes/#selector) |

## Backup Section

The `backup` section in the
[deploy/cr.yaml](https://github.com/percona/percona-postgresql-operator/blob/main/deploy/cr.yaml)
file contains the following configuration options for the regular
Percona Distribution for PostgreSQL backups.

|                 | |
|-----------------|-|
| **Key**         | {{ optionlink('backup.image') }} |
| **Value**       | string |
| **Example**     | `perconalab/percona-postgresql-operator:main-ppg13-pgbackrest` |
| **Description** | The Docker image for [pgBackRest](backups.md#backups-pgbackrest) |
|                 | |
| **Key**         | {{ optionlink('backup.backrestRepoImage') }} |
| **Value**       | string |
| **Example**     | `perconalab/percona-postgresql-operator:main-ppg13-pgbackrest-repo` |
| **Description** | The Docker image for the [BackRest repository](backups.md#backups-pgbackrest-repository) |
|                 | |
| **Key**         | {{ optionlink('backup.resources.requests.cpu') }} |
| **Value**       | string |
| **Example**     | `500m` |
| **Description** | [Kubernetes CPU requests](https://kubernetes.io/docs/concepts/configuration/manage-compute-resources-container/#resource-requests-and-limits-of-pod-and-container) for a pgBackRest container |
|                 | |
| **Key**         | {{ optionlink('backup.resources.requests.memory') }} |
| **Value**       | int |
| **Example**     | `48Mi` |
| **Description** | The [Kubernetes memory requests](https://kubernetes.io/docs/concepts/configuration/manage-compute-resources-container/#resource-requests-and-limits-of-pod-and-container) for a pgBackRest container |
|                 | |
| **Key**         | {{ optionlink('backup.resources.limits.cpu') }} |
| **Value**       | int |
| **Example**     | `1` |
| **Description** | [Kubernetes CPU limits](https://kubernetes.io/docs/concepts/configuration/manage-compute-resources-container/#resource-requests-and-limits-of-pod-and-container) for a pgBackRest container |
|                 | |
| **Key**         | {{ optionlink('backup.resources.limits.memory') }} |
| **Value**       | int |
| **Example**     | `64Mi` |
| **Description** | The [Kubernetes memory limits](https://kubernetes.io/docs/concepts/configuration/manage-compute-resources-container/#resource-requests-and-limits-of-pod-and-container) for a pgBackRest container |
|                 | |
| **Key**         | {{ optionlink('backup.affinity.antiAffinityType') }} |
| **Value**       | string |
| **Example**     | `preferred` |
| **Description** | [Pod anti-affinity type](constraints.md#affinity-and-anti-affinity), can be either `preferred` or `required` |
|                 | |
| **Key**         | {{ optionlink('backup.volumeSpec.size') }} |
| **Value**       | int |
| **Example**     | `1G` |
| **Description** | The [Kubernetes PersistentVolumeClaim](https://kubernetes.io/docs/concepts/storage/persistent-volumes/#persistentvolumeclaims) size for the pgBackRest Storage |
|                 | |
| **Key**         | {{ optionlink('backup.volumeSpec.accessmode') }} |
| **Value**       | string |
| **Example**     | `ReadWriteOnce` |
| **Description** | The [Kubernetes PersistentVolumeClaim](https://kubernetes.io/docs/concepts/storage/persistent-volumes/#persistentvolumeclaims) access modes for the pgBackRest Storage |
|                 | |
| **Key**         | {{ optionlink('backup.volumeSpec.storagetype') }} |
| **Value**       | string |
| **Example**     | `dynamic` |
| **Description** | Type of the pgBackRest storage provisioning: `create` (the default variant; used if storage is provisioned, e.g. using hostpath) or `dynamic` (for a dynamic storage provisioner, e.g. via a StorageClass) |
|                 | |
| **Key**         | {{ optionlink('backup.volumeSpec.storageclass') }} |
| **Value**       | string |
| **Example**     | `""` |
| **Description** | Optionally sets the [Kubernetes storage class](https://kubernetes.io/docs/concepts/storage/storage-classes/) to use with the pgBackRest Storage [PersistentVolumeClaim](https://kubernetes.io/docs/concepts/storage/persistent-volumes/#persistentvolumeclaims) |
|                 | |
| **Key**         | {{ optionlink('backup.volumeSpec.matchLabels') }} |
| **Value**       | string |
| **Example**     | `""` |
| **Description** | A pgBackRest storage [label selector](https://kubernetes.io/docs/concepts/storage/persistent-volumes/#selector) |
|                 | |
| **Key**         | {{ optionlink('backup.storages.&lt;storage-name&gt;.type') }} |
| **Value**       | string |
| **Example**     | `s3` |
| **Description** | Type of the storage used for backups |
|                 | |
| **Key**         | {{ optionlink('backup.storages.&lt;storage-name&gt;.endpointURL') }} |
| **Value**       | string |
| **Example**     | `minio-gateway-svc:9000` |
| **Description** | The endpoint URL of the S3-compatible storage to be used for backups (not needed for the original Amazon S3 cloud) |
|                 | |
| **Key**         | {{ optionlink('backup.storages.&lt;storage-name&gt;.bucket') }} |
| **Value**       | string |
| **Example**     | `""` |
| **Description** | The [Amazon S3 bucket](https://docs.aws.amazon.com/AmazonS3/latest/dev/UsingBucket.html) or [Google Cloud Storage bucket](https://cloud.google.com/storage/docs/key-terms#buckets)
name used for backups |
|                 | |
| **Key**         | {{ optionlink('backup.storages.&lt;storage-name&gt;.region') }} |
| **Value**       | boolean |
| **Example**     | `us-east-1` |
| **Description** | The [AWS region](https://docs.aws.amazon.com/general/latest/gr/rande.html) to use for Amazon and all S3-compatible storages |
|                 | |
| **Key**         | {{ optionlink('backup.storages.&lt;storage-name&gt;.uriStyle') }} |
| **Value**       | string |
| **Example**     | `path` |
| **Description** | Optional parameter that specifies if pgBackRest should use the path or host S3 URI style |
|                 | |
| **Key**         | {{ optionlink('backup.storages.&lt;storage-name&gt;.verifyTLS') }} |
| **Value**       | boolean |
| **Example**     | `false` |
| **Description** | Enables or disables TLS verification for pgBackRest |
|                 | |
| **Key**         | {{ optionlink('backup.storageTypes') }} |
| **Value**       | array |
| **Example**     | `[ "s3" ]` |
| **Description** | The backup storage types for the pgBackRest repository |
|                 | |
| **Key**         | {{ optionlink('backup.repoPath') }} |
| **Value**       | string |
| **Example**     | `""` |
| **Description** | Custom path for pgBackRest repository backups |
|                 | |
| **Key**         | {{ optionlink('backup.schedule.name') }} |
| **Value**       | string |
| **Example**     | `sat-night-backup` |
| **Description** | The backup name |
|                 | |
| **Key**         | {{ optionlink('backup.schedule.schedule') }} |
| **Value**       | string |
| **Example**     | `0 0 \* \* 6` |
| **Description** | Scheduled time to make a backup specified in the
[crontab format](https://en.wikipedia.org/wiki/Cron) |
|                 | |
| **Key**         | {{ optionlink('backup.schedule.keep') }} |
| **Value**       | int |
| **Example**     | `3` |
| **Description** | The amount of most recent backups to store. Older backups are automatically deleted. Set `keep` to zero or completely remove it to disable automatic deletion of backups |
|                 | |
| **Key**         | {{ optionlink('backup.schedule.type') }} |
| **Value**       | string |
| **Example**     | `full` |
| **Description** | The [type](backups.md#backups-pgbackrest-backup-type) of the pgBackRest backup |
|                 | |
| **Key**         | {{ optionlink('backup.schedule.storage') }} |
| **Value**       | string |
| **Example**     | `local` |
| **Description** | The [type](backups.md#backups-pgbackrest-repo-type) of the pgBackRest repository |
|                 | |
| **Key**         | {{ optionlink('backup.customconfig') }} |
| **Value**       | string |
| **Example**     | `""` |
| **Description** | Name of the [ConfigMap](https://kubernetes.io/docs/concepts/configuration/configmap/) to pass custom pgBackRest configuration options |
|                 | |
| **Key**         | {{ optionlink('backup.imagePullPolicy') }} |
| **Value**       | string |
| **Example**     | `Always` |
| **Description** | This option is used to set the [policy](https://kubernetes.io/docs/concepts/containers/images/#updating-images) for updating pgBackRest images | 

## PMM Section

The `pmm` section in the [deploy/cr.yaml](https://github.com/percona/percona-postgresql-operator/blob/main/deploy/cr.yaml)
file contains configuration options for Percona Monitoring and Management.

|                 | |
|-----------------|-|
| **Key**         | {{ optionlink('pmm.enabled') }} |
| **Value**       | boolean |
| **Example**     | `false` |
| **Description** | Enables or disables [monitoring Percona Distribution for PostgreSQL cluster with PMM](https://www.percona.com/doc/percona-monitoring-and-management/2.x/setting-up/client/postgresql.html) |
|                 | |
| **Key**         | {{ optionlink('pmm.image') }} |
| **Value**       | string |
| **Example**     | `percona/pmm-client:{{ pmm2recommended }}` |
| **Description** | [Percona Monitoring and Management (PMM) Client](https://www.percona.com/doc/percona-monitoring-and-management/2.x/details/architecture.html#pmm-client) Docker image |
|                 | |
| **Key**         | {{ optionlink('pmm.serverHost') }} |
| **Value**       | string |
| **Example**     | `monitoring-service` |
| **Description** | Address of the PMM Server to collect data from the cluster |
|                 | |
| **Key**         | {{ optionlink('pmm.serverUser') }} |
| **Value**       | string |
| **Example**     | `admin` |
| **Description** | The [PMM Server User](https://www.percona.com/doc/percona-monitoring-and-management/glossary.option.html). The PMM Server password should be configured using Secrets |
|                 | |
| **Key**         | {{ optionlink('pmm.pmmSecret') }} |
| **Value**       | string |
| **Example**     | `cluster1-pmm-secret` |
| **Description** | Name of the [Kubernetes Secret object](https://kubernetes.io/docs/concepts/configuration/secret/#using-imagepullsecrets) for the PMM Server password |
|                 | |
| **Key**         | {{ optionlink('pmm.resources.requests.memory') }} |
| **Value**       | string |
| **Example**     | `200M` |
| **Description** | The [Kubernetes memory requests](https://kubernetes.io/docs/concepts/configuration/manage-compute-resources-container/#resource-requests-and-limits-of-pod-and-container) for a PMM container |
|                 | |
| **Key**         | {{ optionlink('pmm.resources.requests.cpu') }} |
| **Value**       | string |
| **Example**     | `500m` |
| **Description** | [Kubernetes CPU requests](https://kubernetes.io/docs/concepts/configuration/manage-compute-resources-container/#resource-requests-and-limits-of-pod-and-container) for a PMM container |
|                 | |
| **Key**         | {{ optionlink('pmm.resources.limits.cpu') }} |
| **Value**       | string |
| **Example**     | `500m` |
| **Description** | [Kubernetes CPU limits](https://kubernetes.io/docs/concepts/configuration/manage-compute-resources-container/#resource-requests-and-limits-of-pod-and-container) for a PMM container |
|                 | |
| **Key**         | {{ optionlink('pmm.resources.limits.memory') }} |
| **Value**       | string |
| **Example**     | `200M` |
| **Description** | The [Kubernetes memory limits](https://kubernetes.io/docs/concepts/configuration/manage-compute-resources-container/#resource-requests-and-limits-of-pod-and-container) for a PMM container |
|                 | |
| **Key**         | {{ optionlink('pmm.imagePullPolicy') }} |
| **Value**       | string |
| **Example**     | `Always` |
| **Description** | This option is used to set the [policy](https://kubernetes.io/docs/concepts/containers/images/#updating-images) for updating PMM Client images |

## pgBouncer Section

The `pgBouncer` section in the [deploy/cr.yaml](https://github.com/percona/percona-postgresql-operator/blob/main/deploy/cr.yaml)
file contains configuration options for the [pgBouncer](http://pgbouncer.github.io/) connection pooler for PostgreSQL.

|                 | |
|-----------------|-|
| **Key**         | {{ optionlink('pgBouncer.image') }} |
| **Value**       | string |
| **Example**     | `perconalab/percona-postgresql-operator:main-ppg13-pgbouncer` |
| **Description** | Docker image for the [pgBouncer](http://pgbouncer.github.io/) connection pooler |
|                 | |
| **Key**         | {{ optionlink('pgBouncer.exposePostgresUser') }} |
| **Value**       | boolean |
| **Example**     | `false` |
| **Description** | Enables or disables [exposing postgres user through pgBouncer](users.md#application-users) |
|                 | |
| **Key**         | {{ optionlink('pgBouncer.size') }} |
| **Value**       | int |
| **Example**     | `1G` |
| **Description** | The number of the pgBouncer Pods to provide connection pooling |
|                 | |
| **Key**         | {{ optionlink('pgBouncer.resources.requests.cpu') }} |
| **Value**       | int |
| **Example**     | `1` |
| **Description** | [Kubernetes CPU requests](https://kubernetes.io/docs/concepts/configuration/manage-compute-resources-container/#resource-requests-and-limits-of-pod-and-container) for a pgBouncer container |
|                 | |
| **Key**         | {{ optionlink('pgBouncer.resources.requests.memory') }} |
| **Value**       | int |
| **Example**     | `128Mi` |
| **Description** | The [Kubernetes memory requests](https://kubernetes.io/docs/concepts/configuration/manage-compute-resources-container/#resource-requests-and-limits-of-pod-and-container) for a pgBouncer container |
|                 | |
| **Key**         | {{ optionlink('pgBouncer.resources.limits.cpu') }} |
| **Value**       | int |
| **Example**     | `2` |
| **Description** | [Kubernetes CPU limits](https://kubernetes.io/docs/concepts/configuration/manage-compute-resources-container/#resource-requests-and-limits-of-pod-and-container) for a pgBouncer container |
|                 | |
| **Key**         | {{ optionlink('pgBouncer.resources.limits.memory') }} |
| **Value**       | int |
| **Example**     | `512Mi` |
| **Description** | The [Kubernetes memory limits](https://kubernetes.io/docs/concepts/configuration/manage-compute-resources-container/#resource-requests-and-limits-of-pod-and-container) for a pgBouncer container |
|                 | |
|                 | |
| **Key**         | {{ optionlink('pgBouncer.affinity.antiAffinityType') }} |
| **Value**       | string |
| **Example**     | `preferred` |
| **Description** | [Pod anti-affinity type](constraints.md#affinity-and-anti-affinity), can be either `preferred` or `required` |
| **Key**         | {{ optionlink('pgBouncer.expose.serviceType') }} |
| **Value**       | string |
| **Example**     | `ClusterIP` |
| **Description** | Specifies the type of [Kubernetes Service](https://kubernetes.io/docs/concepts/services-networking/service/#publishing-services-service-types) for pgBouncer |
|                 | |
| **Key**         | {{ optionlink('pgBouncer.expose.loadBalancerSourceRanges') }} |
| **Value**       | string |
| **Example**     | `"10.0.0.0/8"` |
| **Description** | The range of client IP addresses from which the load balancer should be reachable (if not set, there is no limitations) |
|                 | |
| **Key**         | {{ optionlink('pgBouncer.expose.annotations') }} |
| **Value**       | label |
| **Example**     | `pg-cluster-annot: cluster1` |
| **Description** | The [Kubernetes annotations](https://kubernetes.io/docs/concepts/overview/working-with-objects/annotations/) metadata for pgBouncer |
|                 | |
| **Key**         | {{ optionlink('pgBouncer.expose.labels') }} |
| **Value**       | label |
| **Example**     | `pg-cluster-label: cluster1` |
| **Description** | Set [labels](https://kubernetes.io/docs/concepts/overview/working-with-objects/labels/) for the pgBouncer Service |
|                 | |
| **Key**         | {{ optionlink('pgBouncer.imagePullPolicy') }} |
| **Value**       | string |
| **Example**     | `Always` |
| **Description** | This option is used to set the [policy](https://kubernetes.io/docs/concepts/containers/images/#updating-images) for updating pgBouncer images |

## pgReplicas Section

The `pgReplicas` section in the [deploy/cr.yaml](https://github.com/percona/percona-postgresql-operator/blob/main/deploy/cr.yaml)
file stores information required to manage the replicas within a PostgreSQL cluster.

|                 | |
|-----------------|-|
| **Key**         | {{ optionlink('pgReplicas.<replica-name>.size') }} |
| **Value**       | int |
| **Example**     | `1G` |
| **Description** | The number of the PostgreSQL Replica Pods |
|                 | |
| **Key**         | {{ optionlink('pgReplicas.<replica-name>.resources.requests.cpu') }} |
| **Value**       | int |
| **Example**     | `500m` |
| **Description** | [Kubernetes CPU requests](https://kubernetes.io/docs/concepts/configuration/manage-compute-resources-container/#resource-requests-and-limits-of-pod-and-container) for a PostgreSQL Replica container |
|                 | |
| **Key**         | {{ optionlink('pgReplicas.<replica-name>.resources.requests.memory') }} |
| **Value**       | int |
| **Example**     | `256Mi` |
| **Description** | The [Kubernetes memory requests](https://kubernetes.io/docs/concepts/configuration/manage-compute-resources-container/#resource-requests-and-limits-of-pod-and-container) for a PostgreSQL Replica container |
|                 | |
| **Key**         | {{ optionlink('pgReplicas.<replica-name>.resources.limits.cpu') }} |
| **Value**       | int |
| **Example**     | `500m` |
| **Description** | [Kubernetes CPU limits](https://kubernetes.io/docs/concepts/configuration/manage-compute-resources-container/#resource-requests-and-limits-of-pod-and-container) for a PostgreSQL Replica container |
|                 | |
| **Key**         | {{ optionlink('pgReplicas.<replica-name>.resources.limits.memory') }} |
| **Value**       | int |
| **Example**     | `256Mi` |
| **Description** | The [Kubernetes memory limits](https://kubernetes.io/docs/concepts/configuration/manage-compute-resources-container/#resource-requests-and-limits-of-pod-and-container)
for a PostgreSQL Replica container |
|                 | |
| **Key**         | {{ optionlink('pgReplicas.<replica-name>.volumeSpec.accessmode') }} |
| **Value**       | string |
| **Example**     | `ReadWriteOnce` |
| **Description** | The [Kubernetes PersistentVolumeClaim](https://kubernetes.io/docs/concepts/storage/persistent-volumes/#persistentvolumeclaims) access modes for the PostgreSQL Replica storage |
|                 | |
| **Key**         | {{ optionlink('pgReplicas.<replica-name>.volumeSpec.size') }} |
| **Value**       | int |
| **Example**     | `1G` |
| **Description** | The [Kubernetes PersistentVolumeClaim](https://kubernetes.io/docs/concepts/storage/persistent-volumes/#persistentvolumeclaims) size for the PostgreSQL Replica storage |
|                 | |
| **Key**         | {{ optionlink('pgReplicas.<replica-name>.volumeSpec.storagetype') }} |
| **Value**       | string |
| **Example**     | `dynamic` |
| **Description** | Type of the PostgreSQL Replica storage provisioning: `create` (the default variant; used if storage is provisioned, e.g. using hostpath) or `dynamic` (for a dynamic storage provisioner, e.g. via a StorageClass) |
|                 | |
| **Key**         | {{ optionlink('pgReplicas.<replica-name>.volumeSpec.storageclass') }} |
| **Value**       | string |
| **Example**     | `standard` |
| **Description** | Optionally sets the [Kubernetes storage class](https://kubernetes.io/docs/concepts/storage/storage-classes/) to use with the PostgreSQL Replica storage [PersistentVolumeClaim](https://kubernetes.io/docs/concepts/storage/persistent-volumes/#persistentvolumeclaims) |
|                 | |
| **Key**         | {{ optionlink('pgReplicas.<replica-name>.volumeSpec.matchLabels') }} |
| **Value**       | string |
| **Example**     | `""` |
| **Description** | A PostgreSQL Replica storage [label selector](https://kubernetes.io/docs/concepts/storage/persistent-volumes/#selector) |
|                 | |
| **Key**         | {{ optionlink('pgReplicas.<replica-name>.labels') }} |
| **Value**       | label |
| **Example**     | `pg-cluster-label: cluster1` |
| **Description** | Set [labels](https://kubernetes.io/docs/concepts/overview/working-with-objects/labels/) for PostgreSQL Replica Pods |
|                 | |
| **Key**         | {{ optionlink('pgReplicas.<replica-name>.annotations') }} |
| **Value**       | label |
| **Example**     | `pg-cluster-annot: cluster1-1` |
| **Description** | The [Kubernetes annotations](https://kubernetes.io/docs/concepts/overview/working-with-objects/annotations/) metadata for PostgreSQL Replica |
|                 | |
| **Key**         | {{ optionlink('pgReplicas.<replica-name>.expose.serviceType') }} |
| **Value**       | string |
| **Example**     | `ClusterIP` |
| **Description** | Specifies the type of [Kubernetes Service](https://kubernetes.io/docs/concepts/services-networking/service/#publishing-services-service-types) for for PostgreSQL Replica |
|                 | |
| **Key**         | {{ optionlink('pgReplicas.<replica-name>.expose.loadBalancerSourceRanges') }} |
| **Value**       | string |
| **Example**     | `"10.0.0.0/8"` |
| **Description** | The range of client IP addresses from which the load balancer should be reachable (if not set, there is no limitations) |
|                 | |
| **Key**         | {{ optionlink('pgReplicas.<replica-name>.expose.annotations') }} |
| **Value**       | label |
| **Example**     | `pg-cluster-annot: cluster1` |
| **Description** | The [Kubernetes annotations](https://kubernetes.io/docs/concepts/overview/working-with-objects/annotations/) metadata for PostgreSQL Replica |
|                 | |
| **Key**         | {{ optionlink('pgReplicas.<replica-name>.expose.labels') }} |
| **Value**       | label |
| **Example**     | `pg-cluster-label: cluster1` |
| **Description** | Set [labels](https://kubernetes.io/docs/concepts/overview/working-with-objects/labels/) for the PostgreSQL Replica Service |

## pgBadger Section

The `pgBadger` section in the [deploy/cr.yaml](https://github.com/percona/percona-postgresql-operator/blob/main/deploy/cr.yaml)
file contains configuration options for the [pgBadger PostgreSQL log analyzer](https://github.com/darold/pgbadger).

|                 | |
|-----------------|-|
| **Key**         | {{ optionlink('pgBadger.enabled') }} |
| **Value**       | boolean |
| **Example**     | `false` |
| **Description** | Enables or disables the [pgBadger PostgreSQL log analyzer](https://github.com/darold/pgbadger) |
|                 | |
| **Key**         | {{ optionlink('pgBadger.image') }} |
| **Value**       | string |
| **Example**     | `perconalab/percona-postgresql-operator:main-ppg13-pgbadger` |
| **Description** | [pgBadger PostgreSQL log analyzer](https://github.com/darold/pgbadger) Docker image |
|                 | |
| **Key**         | {{ optionlink('pgBadger.port') }} |
| **Value**       | int |
| **Example**     | `10000` |
| **Description** | The port number for pgBadger |
|                 | |
| **Key**         | {{ optionlink('pgBadger.imagePullPolicy') }} |
| **Value**       | string |
| **Example**     | `Always` |
| **Description** | This option is used to set the [policy](https://kubernetes.io/docs/concepts/containers/images/#updating-images) for updating pgBadger images |
