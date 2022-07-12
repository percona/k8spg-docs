# [Custom Resource options](operator.html#operator-custom-resource-options)

The Cluster is configured via the
[deploy/cr.yaml](https://github.com/percona/percona-postgresql-operator/blob/main/deploy/cr.yaml) file.

The metadata part of this file contains the following keys:


* `name` (`cluster1` by default) sets the name of your Percona Distribution
for PostgreSQL Cluster; it should include only [URL-compatible characters](https://datatracker.ietf.org/doc/html/rfc3986#section-2.3), not exceed 22 characters, start with an alphabetic character, and end with an alphanumeric character;

The spec part of the [deploy/cr.yaml](https://github.com/percona/percona-postgresql-operator/blob/main/deploy/cr.yaml) file contains the following sections:

| Key | Value type | Default | Description |
| --- | ---------- | ------- | ----------- |
| pause | boolean  | `false` | Pause/resume: setting it to `true` gracefully stops the cluster, and setting it to `false` after shut down starts the cluster back. |
| upgradeOptions   | subdoc | | Percona Distribution for PostgreSQL upgrade options section |
| pgPrimary | subdoc |         | PostgreSQL Primary instance options section |
| walStorage | subdoc |        | Write-ahead Log Storage Section |
| pmm | subdoc |         | Percona Monitoring and Management section |
| backup | subdoc |      | Section to configure backups and pgBackRest |
| pgBouncer | subdoc |   | The [pgBouncer](http://pgbouncer.github.io/) connection pooler section |
| pgReplicas | subdoc |  | Section required to manage the replicas within a PostgreSQL cluster |
| pgBadger  | subdoc  |  | The [pgBadger](https://github.com/darold/pgbadger) PostgreSQL log analyzer section |

|                 |   |
|-----------------|---|
| **Key**         | [database](operator.html#spec-database) |
| **Value**       | string |
| **Example**     | `pgdb` |
| **Description** | The name of a database that the PostgreSQL user can log into after the PostgreSQL cluster is created |
|                 |   |
| **Key**         | [disableAutofail](operator.html#spec-disableautofail) |
| **Value**       | boolean|
| **Example**     | `false`|
| **Description** | Turns high availability on or off. By default, every cluster can have high availability if there is at least one replica |
|                 |   |
| **Key**         | [tlsOnly](operator.html#spec-tlsonly) |
| **Value**       | boolean |
| **Example**     | `false`    |
| **Description** | Enforece Operator to use only Transport Layer Security (TLS) for both internal and external communications |
|                 |   |
| **Key**         | [sslCA](operator.html#spec-sslca)    |
| **Value**       | string  |
| **Example**     | `cluster1-ssl-ca`   |
| **Description** | The name of the secret with TLS  used for both connection encryption (external traffic), and replication (internal traffic) |
|                 |   |
| **Key**         | [sslSecretName](operator.html#spec-sslsecretname)    |
| **Value**       | string |
| **Example**     | `cluster1-ssl-keypair` |
| **Description** | The name of the secret created to encrypt external communications |
|                 |   |
| **Key**         | [sslReplicationSecretName](operator.html#spec-sslreplicationsecretname)  |
| **Value**       | string |
| **Example**     | `cluster1-ssl-keypair"`    |
| **Description** | The name of the secret created to encrypt internal communications |
|                 |   |
| **Key**         | [keepData](operator.html#spec-keepdata) |
| **Value**       | boolean |
| **Example**     | `true`   |
| **Description** | If `true`, PVCs will be kept after the cluster deletion             |
|                 |   |
| **Key**         | [keepBackups](operator.html#spec-keepbackups)      |
| **Value**       | boolean |
| **Example**     | `true`   |
| **Description** | If `true`, local backups will be kept after the cluster deletion    |
|                 |   |
| **Key**         | [pgDataSource.restoreFrom](operator.html#pgdatasource-restorefrom)  |
| **Value**       | string |
| **Example**     | `""`     |
| **Description** | The name of a data source PostgreSQL cluster, which is used to [restore backup to a new cluster](backups.md#backups-restore) |
|                 |   |
| **Key**         | [pgDataSource.restoreOpts](operator.html#pgdatasource-restoreopts)  |
| **Value**       | string |
| **Example**     | `""`     |
| **Description** | Custom pgBackRest options to [restore backup to a new cluster](backups.md#backups-restore)      |

## [Upgrade Options Section](operator.html#operator-upgradeoptions-section)

The `upgradeOptions` section in the [deploy/cr.yaml](https://github.com/percona/percona-postgresql-operator/blob/main/deploy/cr.yaml) file contains various configuration options to control Percona Distribution for PostgreSQL upgrades.

|                 |   |
|-----------------|---|
| **Key**         | [upgradeOptions.versionServiceEndpoint](operator.html#upgradeoptions-versionserviceendpoint) |
| **Value**       | string |
| **Example**     | `https://check.percona.com`   |
| **Description** | The Version Service URL used to check versions compatibility for upgrade      |
|                 |   |
| **Key**         | [upgradeOptions.apply](operator.html#upgradeoptions-apply)   |
| **Value**       | string |
| **Example**     | `14-recommended`     |
| **Description** | Specifies how [updates are processed](update.md#operator-update-smartupdates) by the Operator. `Never` or `Disabled` will completely disable automatic upgrades, otherwise it can be set to `Latest` or `Recommended` or to a specific version number of Percona Distribution for PostgreSQL to have it version-locked (so that the user can control the version running, but use automatic upgrades to move between them).|
|                 |   |
| **Key**         | [upgradeOptions.schedule](operator.html#upgradeoptions-schedule)    |
| **Value**       | string    |
| **Example**     | `0 2 \* \* \*` |
| **Description** | Scheduled time to check for updates, specified in the [crontab format](https://en.wikipedia.org/wiki/Cron)           |

## [pgPrimary Section](operator.html#operator-pgprimary-section)

The pgPrimary section controls the PostgreSQL Primary instance.

|                 |   |
|-----------------|---|
| **Key**         | [pgPrimary.image](operator.html#pgprimary-image)    |
| **Value**       | string    |
| **Example**     | `perconalab/percona-postgresql-operator:main-ppg13-postgres-ha`  |
| **Description** | The Docker image of the PostgreSQL Primary instance  |
|                 |   |
| **Key**         | [pgPrimary.imagePullPolicy](operator.html#pgprimary-imagepullpolicy)  |
| **Value**       | string    |
| **Example**     | `Always`    |
| **Description** | This option is used to set the [policy](https://kubernetes.io/docs/concepts/containers/images/#updating-images) for updating pgPrimary and pgReplicas images   |
|                 |   |
| **Key**         | [pgPrimary.resources.requests.memory](operator.html#pgprimary-resources-requests-memory)     |
| **Value**       | int       |
| **Example**     | `256Mi`     |
| **Description** | The [Kubernetes memory requests](https://kubernetes.io/docs/concepts/configuration/manage-compute-resources-container/#resource-requests-and-limits-of-pod-and-container) for a PostgreSQL Primary container     |
|                 |   |
| **Key**         | [pgPrimary.resources.requests.cpu](operator.html#pgprimary-resources-requests-cpu)           |
| **Value**       | string    |
| **Example**     | `500m`      |
| **Description** | [Kubernetes CPU requests](https://kubernetes.io/docs/concepts/configuration/manage-compute-resources-container/#resource-requests-and-limits-of-pod-and-container) for a PostgreSQL Primary container     |
|                 |   |
| **Key**         | [pgPrimary.resources.limits.cpu](operator.html#pgprimary-resources-limits-cpu)          |
| **Value**       | string    |
| **Example**     | `500m`      |
| **Description** | [Kubernetes CPU limits](https://kubernetes.io/docs/concepts/configuration/manage-compute-resources-container/#resource-requests-and-limits-of-pod-and-container) for a PostgreSQL Primary container         |
|                 |   |
| **Key**         | [pgPrimary.resources.limits.memory](operator.html#pgprimary-resources-limits-memory)          |
| **Value**       | string    |
| **Example**     | `256Mi`     |
| **Description** | The [Kubernetes memory limits](https://kubernetes.io/docs/concepts/configuration/manage-compute-resources-container/#resource-requests-and-limits-of-pod-and-container) for a PostgreSQL Primary container           |
|                 |   |
| **Key**         | [pgPrimary.tolerations](operator.html#pgprimary-tolerations)   |
| **Value**       | subdoc    |
| **Example**     | `node.alpha.kubernetes.io/unreachable` |
| **Description** | [Kubernetes Pod tolerations](https://kubernetes.io/docs/concepts/configuration/taint-and-toleration/)        |
|                 |   |
| **Key**         | [pgPrimary.volumeSpec.size](operator.html#pgprimary-volumespec-size)  |
| **Value**       | int       |
| **Example**     | `1G`        |
| **Description** | The [Kubernetes PersistentVolumeClaim](https://kubernetes.io/docs/concepts/storage/persistent-volumes/#persistentvolumeclaims) size for the PostgreSQL Primary storage  |
|                 |   |
| **Key**         | [pgPrimary.volumeSpec.accessmode](operator.html#pgprimary-volumespec-accessmode)  |
| **Value**       | string    |
| **Example**     | `ReadWriteOnce` |
| **Description** | The [Kubernetes PersistentVolumeClaim](https://kubernetes.io/docs/concepts/storage/persistent-volumes/#persistentvolumeclaims) access modes for the PostgreSQL Primary storage  |
|                 |   |
| **Key**         | [pgPrimary.volumeSpec.storagetype](operator.html#pgprimary-volumespec-storagetype) |
| **Value**       | string    |
| **Example**     | `dynamic`   |
| **Description** | Type of the PostgreSQL Primary storage provisioning: `create` (the default variant; used if storage is provisioned, e.g. using hostpath) or `dynamic` (for a dynamic storage provisioner, e.g. via a StorageClass) |
|                 |   |
| **Key**         | [pgPrimary.volumeSpec.storageclass](operator.html#pgprimary-volumespec-storageclass)  |
| **Value**       | string    |
| **Example**     | `""`        |
| **Description** | Optionally sets the [Kubernetes storage class](https://kubernetes.io/docs/concepts/storage/storage-classes/) to use with the PostgreSQL Primary storage [PersistentVolumeClaim](https://kubernetes.io/docs/concepts/storage/persistent-volumes/#persistentvolumeclaims) |
|                 |   |
| **Key**         | [pgPrimary.volumeSpec.matchLabels](operator.html#pgprimary-volumespec-matchlabels) |
| **Value**       | string    |
| **Example**     | `""`        |
| **Description** | A PostgreSQL Primary storage [label selector](https://kubernetes.io/docs/concepts/storage/persistent-volumes/#selector)  |
|                 |   |
| **Key**         | [pgPrimary.imagePullPolicy](operator.html#pgprimary-imagepullpolicy)  |
| **Value**       | string    |
| **Example**     | `Always`    |
| **Description** | This option is used to set the [policy](https://kubernetes.io/docs/concepts/containers/images/#updating-images) for updating pgPrimary and pgReplicas images |
|                 |   |
| **Key**         | [pgPrimary.customconfig](operator.html#pgprimary-customconfig)  |
| **Value**       | string    |
| **Example**     | `""`        |
| **Description** | Name of the [Custom configuration options ConfigMap](options.md#operator-configmaps) for PostgreSQL cluster |

## [Tablespaces Storage Section](operator.html#operator-walstorage-section)

The `tablespaceStorages` section in the [deploy/cr.yaml](https://github.com/percona/percona-postgresql-operator/blob/main/deploy/cr.yaml)
file contains configuration options for PostgreSQL [Tablespace](https://www.postgresql.org/docs/current/manage-ag-tablespaces.html).

|                 |   |
|-----------------|---|
| **Key**         | [tablespaceStorages.<storage-name>.volumeSpec.size](operator.html#tablespacestorages-volumespec-size)                |
| **Value**       | int       |
| **Example**     | `1G`        |
| **Description** | The [Kubernetes PersistentVolumeClaim](https://kubernetes.io/docs/concepts/storage/persistent-volumes/#persistentvolumeclaims) size for the PostgreSQL Tablespaces storage  |
|                 |   |
| **Key**         | [tablespaceStorages.<storage-name>.volumeSpec.accessmode](operator.html#tablespacestorages-volumespec-accessmode)          |
| **Value**       | string    |
| **Example**     | `ReadWriteOnce` |
| **Description** | The [Kubernetes PersistentVolumeClaim](https://kubernetes.io/docs/concepts/storage/persistent-volumes/#persistentvolumeclaims) access modes for the PostgreSQL Tablespaces storage  |
|                 |   |
| **Key**         | [tablespaceStorages.<storage-name>.volumeSpec.storagetype](operator.html#tablespacestorages-volumespec-storagetype)         |
| **Value**       | string    |
| **Example**     | `dynamic`   |
| **Description** | Type of the PostgreSQL Tablespaces storage provisioning: `create` (the default variant; used if storage is provisioned, e.g. using hostpath) or `dynamic` (for a dynamic storage provisioner, e.g. via a StorageClass) |
|                 |   |
| **Key**         | [tablespaceStorages.<storage-name>.volumeSpec.storageclass](operator.html#tablespacestorages-storageclass)        |
| **Value**       | string    |
| **Example**     | `""`        |
| **Description** | Optionally sets the [Kubernetes storage class](https://kubernetes.io/docs/concepts/storage/storage-classes/) to use with the PostgreSQL Tablespaces storage [PersistentVolumeClaim](https://kubernetes.io/docs/concepts/storage/persistent-volumes/#persistentvolumeclaims)            |
|                 |   |
| **Key**         | [tablespaceStorages.<storage-name>.volumeSpec.matchLabels](operator.html#tablespacestorages-volumespec-matchlabels)         |
| **Value**       | string    |
| **Example**     | `""`        |
| **Description** | A PostgreSQL Tablespaces storage [label selector](https://kubernetes.io/docs/concepts/storage/persistent-volumes/#selector) |

## [Write-ahead Log Storage Section](operator.html#operator-walstorage-section)

The `walStorage` section in the [deploy/cr.yaml](https://github.com/percona/percona-postgresql-operator/blob/main/deploy/cr.yaml)
file contains configuration options for PostgreSQL [write-ahead logging](https://www.postgresql.org/docs/current/wal-intro.html).

|                 |   |
|-----------------|---|
| **Key**         | [walStorage.volumeSpec.size](operator.html#walstorage-volumespec-size) |
| **Value**       | int       |
| **Example**     | `1G`        |
| **Description** | The [Kubernetes PersistentVolumeClaim](https://kubernetes.io/docs/concepts/storage/persistent-volumes/#persistentvolumeclaims) size for the PostgreSQL Write-ahead Log storage   |
|                 |   |
| **Key**         | [walStorage.volumeSpec.accessmode](operator.html#walstorage-volumespec-accessmode) |
| **Value**       | string    |
| **Example**     | `ReadWriteOnce` |
| **Description** | The [Kubernetes PersistentVolumeClaim](https://kubernetes.io/docs/concepts/storage/persistent-volumes/#persistentvolumeclaims) access modes for the PostgreSQL Write-ahead Log storage |
|                 |   |
| **Key**         | [walStorage.volumeSpec.storagetype](operator.html#walstorage-volumespec-storagetype)  |
| **Value**       | string    |
| **Example**     | `dynamic`   |
| **Description** | Type of the PostgreSQL Write-ahead Log storage provisioning: `create` (the default variant; used if storage is provisioned, e.g. using hostpath) or `dynamic` (for a dynamic storage provisioner, e.g. via a StorageClass) |
|                 |   |
| **Key**         | [walStorage.volumeSpec.storageclass](operator.html#walstorage-storageclass) |
| **Value**       | string    |
| **Example**     | `""`        |
| **Description** | Optionally sets the [Kubernetes storage class](https://kubernetes.io/docs/concepts/storage/storage-classes/) to use with the PostgreSQL Write-ahead Log storage [PersistentVolumeClaim](https://kubernetes.io/docs/concepts/storage/persistent-volumes/#persistentvolumeclaims)        |
|                 |   |
| **Key**         | [walStorage.volumeSpec.matchLabels](operator.html#walstorage-volumespec-matchlabels)  |
| **Value**       | string    |
| **Example**     | `""`        |
| **Description** | A PostgreSQL Write-ahead Log storage [label selector](https://kubernetes.io/docs/concepts/storage/persistent-volumes/#selector)                |

## [Backup Section](operator.html#operator-backup-section)

The `backup` section in the
[deploy/cr.yaml](https://github.com/percona/percona-postgresql-operator/blob/main/deploy/cr.yaml)
file contains the following configuration options for the regular
Percona Distribution for PostgreSQL backups.

|                 |   |
|-----------------|---|
| **Key**         | [backup.image](operator.html#backup-backrestimage)      |
| **Value**       | string    |
| **Example**     | `perconalab/percona-postgresql-operator:main-ppg13-pgbackrest`       |
| **Description** | The Docker image for [pgBackRest](backups.md#backups-pgbackrest)  |
|                 |   |
| **Key**         | [backup.backrestRepoImage](operator.html#backup-backrestrepoimage)   |
| **Value**       | string    |
| **Example**     | `perconalab/percona-postgresql-operator:main-ppg13-pgbackrest-repo`  |
| **Description** | The Docker image for the [BackRest repository](backups.md#backups-pgbackrest-repository) |
|                 |   |
| **Key**         | [backup.resources.requests.cpu](operator.html#backup-resources-requests-cpu)  |
| **Value**       | string    |
| **Example**     | `500m`      |
| **Description** | [Kubernetes CPU requests](https://kubernetes.io/docs/concepts/configuration/manage-compute-resources-container/#resource-requests-and-limits-of-pod-and-container) for a pgBackRest container                 |
|                 |   |
| **Key**         | [backup.resources.requests.memory](operator.html#backup-resources-requests-memory) |
| **Value**       | int       |
| **Example**     | `48Mi`      |
| **Description** | The [Kubernetes memory requests](https://kubernetes.io/docs/concepts/configuration/manage-compute-resources-container/#resource-requests-and-limits-of-pod-and-container) for a pgBackRest container          |
|                 |   |
| **Key**         | [backup.resources.limits.cpu](operator.html#backup-resources-limits-cpu)  |
| **Value**       | int       |
| **Example**     | `1`         |
| **Description** | [Kubernetes CPU limits](https://kubernetes.io/docs/concepts/configuration/manage-compute-resources-container/#resource-requests-and-limits-of-pod-and-container) for a pgBackRest container |
|                 |   |
| **Key**         | [backup.resources.limits.memory](operator.html#backup-resources-limits-memory) |
| **Value**       | int       |
| **Example**     | `64Mi`      |
| **Description** | The [Kubernetes memory limits](https://kubernetes.io/docs/concepts/configuration/manage-compute-resources-container/#resource-requests-and-limits-of-pod-and-container) for a pgBackRest container            |
|                 |   |
| **Key**         | [backup.volumeSpec.size](operator.html#backup-volumespec-size)  |
| **Value**       | int       |
| **Example**     | `1G`        |
| **Description** | The [Kubernetes PersistentVolumeClaim](https://kubernetes.io/docs/concepts/storage/persistent-volumes/#persistentvolumeclaims) size for the pgBackRest Storage |
|                 |   |
| **Key**         | [backup.volumeSpec.accessmode](operator.html#backup-volumespec-accessmode) |
| **Value**       | string    |
| **Example**     | `ReadWriteOnce` |
| **Description** | The [Kubernetes PersistentVolumeClaim](https://kubernetes.io/docs/concepts/storage/persistent-volumes/#persistentvolumeclaims) access modes for the pgBackRest Storage  |
|                 |   |
| **Key**         | [backup.volumeSpec.storagetype](operator.html#backup-volumespec-storagetype)  |
| **Value**       | string    |
| **Example**     | `dynamic`   |
| **Description** | Type of the pgBackRest storage provisioning: `create` (the default variant; used if storage is provisioned, e.g. using hostpath) or `dynamic` (for a dynamic storage provisioner, e.g. via a StorageClass)    |
|                 |   |
| **Key**         | [backup.volumeSpec.storageclass](operator.html#backup-volumespec-storageclass) |
| **Value**       | string    |
| **Example**     | `""`        |
| **Description** | Optionally sets the [Kubernetes storage class](https://kubernetes.io/docs/concepts/storage/storage-classes/) to use with the pgBackRest Storage [PersistentVolumeClaim](https://kubernetes.io/docs/concepts/storage/persistent-volumes/#persistentvolumeclaims)  |
|                 |   |
| **Key**         | [backup.volumeSpec.matchLabels](operator.html#backup-volumespec-matchlabels)  |
| **Value**       | string    |
| **Example**     | `""`        |
| **Description** | A pgBackRest storage [label selector](https://kubernetes.io/docs/concepts/storage/persistent-volumes/#selector)  |
|                 |   |
| **Key**         | [backup.storages.<storage-name>.type](operator.html#backup-storages-type)  |
| **Value**       | string    |
| **Example**     | `s3`        |
| **Description** | Type of the storage used for backups |
|                 |   |
| **Key**         | [backup.storages.<storage-name>.endpointURL](operator.html#backup-storages-endpointurl) |
| **Value**       | string    |
| **Example**     | `minio-gateway-svc:9000`    |
| **Description** | The endpoint URL of the S3-compatible storage to be used for backups (not needed for the original Amazon S3 cloud)           |
|                 |   |
| **Key**         | [backup.storages.<storage-name>.bucket](operator.html#backup-storages-bucket)  |
| **Value**       | string    |
| **Example**     | `""`        |
| **Description** | The [Amazon S3 bucket](https://docs.aws.amazon.com/AmazonS3/latest/dev/UsingBucket.html) or [Google Cloud Storage bucket](https://cloud.google.com/storage/docs/key-terms#buckets)
name used for backups     |
|                 |   |
| **Key**         | [backup.storages.<storage-name>.region](operator.html#backup-storages-region)  |
| **Value**       | boolean   |
| **Example**     | `us-east-1` |
| **Description** | The [AWS region](https://docs.aws.amazon.com/general/latest/gr/rande.html) to use for Amazon and all S3-compatible storages    |
|                 |   |
| **Key**         | [backup.storages.<storage-name>.uriStyle](operator.html#backup-storages-uristyle)  |
| **Value**       | string    |
| **Example**     | `path`      |
| **Description** | Optional parameter that specifies if pgBackRest should use the path or host S3 URI style |
|                 |   |
| **Key**         | [backup.storages.<storage-name>.verifyTLS](operator.html#backup-storages-verifytls) |
| **Value**       | boolean   |
| **Example**     | `false`     |
| **Description** | Enables or disables TLS verification for pgBackRest                |
|                 |   |
| **Key**         | [backup.storageTypes](operator.html#backup-storagetypes) |
| **Value**       | array     |
| **Example**     | `[ "s3" ]`  |
| **Description** | The backup storage types for the pgBackRest repository             |
|                 |   |
| **Key**         | [backup.repoPath](operator.html#backup-repopath)   |
| **Value**       | string    |
| **Example**     | `""`        |
| **Description** | Custom path for pgBackRest repository backups |
|                 |   |
| **Key**         | [backup.schedule.name](operator.html#backup-schedule-name)    |
| **Value**       | string    |
| **Example**     | `sat-night-backup`    |
| **Description** | The backup name     |
|                 |   |
| **Key**         | [backup.schedule.schedule](operator.html#backup-schedule-schedule)   |
| **Value**       | string    |
| **Example**     | `0 0 \* \* 6` |
| **Description** | Scheduled time to make a backup specified in the
[crontab format](https://en.wikipedia.org/wiki/Cron)    |
|                 |   |
| **Key**         | [backup.schedule.keep](operator.html#backup-schedule-keep)    |
| **Value**       | int       |
| **Example**     | `3`         |
| **Description** | The amount of most recent backups to store. Older backups are automatically deleted. Set `keep` to zero or completely remove it to disable automatic deletion of backups |
|                 |   |
| **Key**         | [backup.schedule.type](operator.html#backup-schedule-type)    |
| **Value**       | string    |
| **Example**     | `full`      |
| **Description** | The [type](backups.md#backups-pgbackrest-backup-type) of the pgBackRest backup  |
|                 |   |
| **Key**         | [backup.schedule.storage](operator.html#backup-schedule-storage) |
| **Value**       | string    |
| **Example**     | `local`     |
| **Description** | The [type](backups.md#backups-pgbackrest-repo-type) of the pgBackRest repository  |
|                 |   |
| **Key**         | [backup.customconfig](operator.html#backup-customconfig) |
| **Value**       | string    |
| **Example**     | `""`        |
| **Description** | Name of the [ConfigMap](https://kubernetes.io/docs/concepts/configuration/configmap/) to pass custom pgBackRest configuration options |
|                 |   |
| **Key**         | [backup.imagePullPolicy](operator.html#backup-imagepullpolicy)  |
| **Value**       | string    |
| **Example**     | `Always`    |
| **Description** | This option is used to set the [policy](https://kubernetes.io/docs/concepts/containers/images/#updating-images) for updating pgBackRest images | 

## [PMM Section](operator.html#operator-pmm-section)

The `pmm` section in the [deploy/cr.yaml](https://github.com/percona/percona-postgresql-operator/blob/main/deploy/cr.yaml)
file contains configuration options for Percona Monitoring and Management.

|                 |   |
|-----------------|---|
| **Key**         | [pmm.enabled](operator.html#pmm-enabled) |
| **Value**       | boolean   |
| **Example**     | `false`     |
| **Description** | Enables or disables [monitoring Percona Distribution for PostgreSQL cluster with PMM](https://www.percona.com/doc/percona-monitoring-and-management/2.x/setting-up/client/postgresql.html) |
|                 |   |
| **Key**         | [pmm.image](operator.html#pmm-image) |
| **Value**       | string    |
| **Example**     | `percona/pmm-client:2.24.0` |
| **Description** | [Percona Monitoring and Management (PMM) Client](https://www.percona.com/doc/percona-monitoring-and-management/2.x/details/architecture.html#pmm-client) Docker image        |
|                 |   |
| **Key**         | [pmm.serverHost](operator.html#pmm-serverhost)    |
| **Value**       | string    |
| **Example**     | `monitoring-service`  |
| **Description** | Address of the PMM Server to collect data from the cluster         |
|                 |   |
| **Key**         | [pmm.serverUser](operator.html#pmm-serveruser)    |
| **Value**       | string    |
| **Example**     | `admin`     |
| **Description** | The [PMM Server User](https://www.percona.com/doc/percona-monitoring-and-management/glossary.option.html). The PMM Server password should be configured using Secrets |
|                 |   |
| **Key**         | [pmm.pmmSecret](operator.html#pmm-pmmsecret)     |
| **Value**       | string    |
| **Example**     | `cluster1-pmm-secret` |
| **Description** | Name of the [Kubernetes Secret object](https://kubernetes.io/docs/concepts/configuration/secret/#using-imagepullsecrets) for the PMM Server password   |
|                 |   |
| **Key**         | [pmm.resources.requests.memory](operator.html#pmm-resources-requests-memory)  |
| **Value**       | string    |
| **Example**     | `200M`      |
| **Description** | The [Kubernetes memory requests](https://kubernetes.io/docs/concepts/configuration/manage-compute-resources-container/#resource-requests-and-limits-of-pod-and-container) for a PMM container |
|                 |   |
| **Key**         | [pmm.resources.requests.cpu](operator.html#pmm-resources-requests-cpu) |
| **Value**       | string    |
| **Example**     | `500m`      |
| **Description** | [Kubernetes CPU requests](https://kubernetes.io/docs/concepts/configuration/manage-compute-resources-container/#resource-requests-and-limits-of-pod-and-container) for a PMM container  |
|                 |   |
| **Key**         | [pmm.resources.limits.cpu](operator.html#pmm-resources-limits-cpu)   |
| **Value**       | string    |
| **Example**     | `500m`      |
| **Description** | [Kubernetes CPU limits](https://kubernetes.io/docs/concepts/configuration/manage-compute-resources-container/#resource-requests-and-limits-of-pod-and-container) for a PMM container  |
|                 |   |
| **Key**         | [pmm.resources.limits.memory](operator.html#pmm-resources-limits-memory)  |
| **Value**       | string    |
| **Example**     | `200M`      |
| **Description** | The [Kubernetes memory limits](https://kubernetes.io/docs/concepts/configuration/manage-compute-resources-container/#resource-requests-and-limits-of-pod-and-container) for a PMM container |
|                 |   |
| **Key**         | [pmm.imagePullPolicy](operator.html#pmm-imagepullpolicy) |
| **Value**       | string    |
| **Example**     | `Always`    |
| **Description** | This option is used to set the [policy](https://kubernetes.io/docs/concepts/containers/images/#updating-images) for updating PMM Client images |

## [pgBouncer Section](operator.html#operator-pgbouncer-section)

The `pgBouncer` section in the [deploy/cr.yaml](https://github.com/percona/percona-postgresql-operator/blob/main/deploy/cr.yaml)
file contains configuration options for the [pgBouncer](http://pgbouncer.github.io/) connection pooler for PostgreSQL.

|                 |   |
|-----------------|---|
| **Key**         | [pgBouncer.image](operator.html#pgbouncer-image)   |
| **Value**       | string    |
| **Example**     | `perconalab/percona-postgresql-operator:main-ppg13-pgbouncer`        |
| **Description** | Docker image for the [pgBouncer](http://pgbouncer.github.io/) connection pooler |
|                 |   |
| **Key**         | [pgBouncer.size](operator.html#pgbouncer-size)    |
| **Value**       | int       |
| **Example**     | `1G`        |
| **Description** | The number of the pgBouncer Pods to provide connection pooling     |
|                 |   |
| **Key**         | [pgBouncer.resources.requests.cpu](operator.html#pgbouncer-resources-requests-cpu) |
| **Value**       | int       |
| **Example**     | `1`         |
| **Description** | [Kubernetes CPU requests](https://kubernetes.io/docs/concepts/configuration/manage-compute-resources-container/#resource-requests-and-limits-of-pod-and-container) for a pgBouncer container |
|                 |   |
| **Key**         | [pgBouncer.resources.requests.memory](operator.html#pgbouncer-resources-requests-memory)  |
| **Value**       | int       |
| **Example**     | `128Mi`     |
| **Description** | The [Kubernetes memory requests](https://kubernetes.io/docs/concepts/configuration/manage-compute-resources-container/#resource-requests-and-limits-of-pod-and-container) for a pgBouncer container           |
|                 |   |
| **Key**         | [pgBouncer.resources.limits.cpu](operator.html#pgbouncer-resources-limits-cpu) |
| **Value**       | int       |
| **Example**     | `2`         |
| **Description** | [Kubernetes CPU limits](https://kubernetes.io/docs/concepts/configuration/manage-compute-resources-container/#resource-requests-and-limits-of-pod-and-container) for a pgBouncer container |
|                 |   |
| **Key**         | [pgBouncer.resources.limits.memory](operator.html#pgbouncer-resources-limits-memory)  |
| **Value**       | int       |
| **Example**     | `512Mi`     |
| **Description** | The [Kubernetes memory limits](https://kubernetes.io/docs/concepts/configuration/manage-compute-resources-container/#resource-requests-and-limits-of-pod-and-container) for a pgBouncer container             |
|                 |   |
| **Key**         | [pgBouncer.expose.serviceType](operator.html#pgbouncer-expose-servicetype) |
| **Value**       | string    |
| **Example**     | `ClusterIP` |
| **Description** | Specifies the type of [Kubernetes Service](https://kubernetes.io/docs/concepts/services-networking/service/#publishing-services-service-types) for pgBouncer             |
|                 |   |
| **Key**         | [pgBouncer.expose.loadBalancerSourceRanges](operator.html#pgbouncer-expose-loadbalancersourceranges)  |
| **Value**       | string    |
| **Example**     | `"10.0.0.0/8"` |
| **Description** | The range of client IP addresses from which the load balancer should be reachable (if not set, there is no limitations)      |
|                 |   |
| **Key**         | [pgBouncer.expose.annotations](operator.html#pgbouncer-expose-annotations) |
| **Value**       | label     |
| **Example**     | `pg-cluster-annot: cluster1`   |
| **Description** | The [Kubernetes annotations](https://kubernetes.io/docs/concepts/overview/working-with-objects/annotations/) metadata for pgBouncer |
|                 |   |
| **Key**         | [pgBouncer.expose.labels](operator.html#pgbouncer-expose-labels) |
| **Value**       | label     |
| **Example**     | `pg-cluster-label: cluster1`   |
| **Description** | Set [labels](https://kubernetes.io/docs/concepts/overview/working-with-objects/labels/) for the pgBouncer Service |
|                 |   |
| **Key**         | [pgBouncer.imagePullPolicy](operator.html#pgbouncer-imagepullpolicy)  |
| **Value**       | string    |
| **Example**     | `Always`    |
| **Description** | This option is used to set the [policy](https://kubernetes.io/docs/concepts/containers/images/#updating-images) for updating pgBouncer images |

## [pgReplicas Section](operator.html#operator-pgreplicas-section)

The `pgReplicas` section in the [deploy/cr.yaml](https://github.com/percona/percona-postgresql-operator/blob/main/deploy/cr.yaml)
file stores information required to manage the replicas within a PostgreSQL cluster.

|                 |   |
|-----------------|---|
| **Key**         | [pgReplicas.<replica-name>.size](operator.html#pgreplicas-size) |
| **Value**       | int       |
| **Example**     | `1G`        |
| **Description** | The number of the PostgreSQL Replica Pods  |
|                 |   |
| **Key**         | [pgReplicas.<replica-name>.resources.requests.cpu](operator.html#pgreplicas-resources-requests-cpu)                 |
| **Value**       | int       |
| **Example**     | `500m`      |
| **Description** | [Kubernetes CPU requests](https://kubernetes.io/docs/concepts/configuration/manage-compute-resources-container/#resource-requests-and-limits-of-pod-and-container) for a PostgreSQL Replica container         |
|                 |   |
| **Key**         | [pgReplicas.<replica-name>.resources.requests.memory](operator.html#pgreplicas-resources-requests-memory)              |
| **Value**       | int       |
| **Example**     | `256Mi`     |
| **Description** | The [Kubernetes memory requests](https://kubernetes.io/docs/concepts/configuration/manage-compute-resources-container/#resource-requests-and-limits-of-pod-and-container) for a PostgreSQL Replica container  |
|                 |   |
| **Key**         | [pgReplicas.<replica-name>.resources.limits.cpu](operator.html#pgreplicas-resources-limits-cpu) |
| **Value**       | int       |
| **Example**     | `500m`      |
| **Description** | [Kubernetes CPU limits](https://kubernetes.io/docs/concepts/configuration/manage-compute-resources-container/#resource-requests-and-limits-of-pod-and-container) for a PostgreSQL Replica container           |
|                 |   |
| **Key**         | [pgReplicas.<replica-name>.resources.limits.memory](operator.html#pgreplicas-resources-limits-memory)                |
| **Value**       | int       |
| **Example**     | `256Mi`     |
| **Description** | The [Kubernetes memory limits](https://kubernetes.io/docs/concepts/configuration/manage-compute-resources-container/#resource-requests-and-limits-of-pod-and-container)
for a PostgreSQL Replica container    |
|                 |   |
| **Key**         | [pgReplicas.<replica-name>.volumeSpec.accessmode](operator.html#pgreplicas-volumespec-accessmode) |
| **Value**       | string    |
| **Example**     | `ReadWriteOnce` |
| **Description** | The [Kubernetes PersistentVolumeClaim](https://kubernetes.io/docs/concepts/storage/persistent-volumes/#persistentvolumeclaims) access modes for the PostgreSQL Replica storage   |
|                 |   |
| **Key**         | [pgReplicas.<replica-name>.volumeSpec.size](operator.html#pgreplicas-volumespec-size)  |
| **Value**       | int       |
| **Example**     | `1G`        |
| **Description** | The [Kubernetes PersistentVolumeClaim](https://kubernetes.io/docs/concepts/storage/persistent-volumes/#persistentvolumeclaims) size for the PostgreSQL Replica storage  |
|                 |   |
| **Key**         | [pgReplicas.<replica-name>.volumeSpec.storagetype](operator.html#pgreplicas-volumespec-storagetype)                 |
| **Value**       | string    |
| **Example**     | `dynamic`   |
| **Description** | Type of the PostgreSQL Replica storage provisioning: `create` (the default variant; used if storage is provisioned, e.g. using hostpath) or `dynamic` (for a dynamic storage provisioner, e.g. via a StorageClass) |
|                 |   |
| **Key**         | [pgReplicas.<replica-name>.volumeSpec.storageclass](operator.html#pgreplicas-volumespec-storageclass)                |
| **Value**       | string    |
| **Example**     | `standard`  |
| **Description** | Optionally sets the [Kubernetes storage class](https://kubernetes.io/docs/concepts/storage/storage-classes/) to use with the PostgreSQL Replica storage [PersistentVolumeClaim](https://kubernetes.io/docs/concepts/storage/persistent-volumes/#persistentvolumeclaims)                |
|                 |   |
| **Key**         | [pgReplicas.<replica-name>.volumeSpec.matchLabels](operator.html#pgreplicas-volumespec-matchlabels)                 |
| **Value**       | string    |
| **Example**     | `""`        |
| **Description** | A PostgreSQL Replica storage [label selector](https://kubernetes.io/docs/concepts/storage/persistent-volumes/#selector)  |
|                 |   |
| **Key**         | [pgReplicas.<replica-name>.labels](operator.html#pgbouncer-labels) |
| **Value**       | label     |
| **Example**     | `pg-cluster-label: cluster1`   |
| **Description** | Set [labels](https://kubernetes.io/docs/concepts/overview/working-with-objects/labels/) for PostgreSQL Replica Pods |
|                 |   |
| **Key**         | [pgReplicas.<replica-name>.annotations](operator.html#pgreplicas-annotations)  |
| **Value**       | label     |
| **Example**     | `pg-cluster-annot: cluster1-1` |
| **Description** | The [Kubernetes annotations](https://kubernetes.io/docs/concepts/overview/working-with-objects/annotations/) metadata for PostgreSQL Replica         |
|                 |   |
| **Key**         | [pgReplicas.<replica-name>.expose.serviceType](operator.html#pgreplicas-expose-servicetype) |
| **Value**       | string    |
| **Example**     | `ClusterIP` |
| **Description** | Specifies the type of [Kubernetes Service](https://kubernetes.io/docs/concepts/services-networking/service/#publishing-services-service-types) for for PostgreSQL Replica |
|                 |   |
| **Key**         | [pgReplicas.<replica-name>.expose.loadBalancerSourceRanges](operator.html#pgreplicas-expose-loadbalancersourceranges)        |
| **Value**       | string    |
| **Example**     | `"10.0.0.0/8"` |
| **Description** | The range of client IP addresses from which the load balancer should be reachable (if not set, there is no limitations)      |
|                 |   |
| **Key**         | [pgReplicas.<replica-name>.expose.annotations](operator.html#pgreplicas-expose-annotations) |
| **Value**       | label     |
| **Example**     | `pg-cluster-annot: cluster1`   |
| **Description** | The [Kubernetes annotations](https://kubernetes.io/docs/concepts/overview/working-with-objects/annotations/) metadata for PostgreSQL Replica         |
|                 |   |
| **Key**         | [pgReplicas.<replica-name>.expose.labels](operator.html#pgreplicas-expose-labels)  |
| **Value**       | label     |
| **Example**     | `pg-cluster-label: cluster1`   |
| **Description** | Set [labels](https://kubernetes.io/docs/concepts/overview/working-with-objects/labels/) for the PostgreSQL Replica Service |

## [pgBadger Section](operator.html#operator-pgbadger-section)

The `pgBadger` section in the [deploy/cr.yaml](https://github.com/percona/percona-postgresql-operator/blob/main/deploy/cr.yaml)
file contains configuration options for the [pgBadger PostgreSQL log analyzer](https://github.com/darold/pgbadger).

|                 |   |
|-----------------|---|
| **Key**         | [pgBadger.enabled](operator.html#pgbadger-enabled)  |
| **Value**       | boolean   |
| **Example**     | `false`     |
| **Description** | Enables or disables the
[pgBadger PostgreSQL log analyzer](https://github.com/darold/pgbadger)           |
|                 |   |
| **Key**         | [pgBadger.image](operator.html#pgbadger-image)    |
| **Value**       | string    |
| **Example**     | `perconalab/percona-postgresql-operator:main-ppg13-pgbadger`         |
| **Description** | [pgBadger PostgreSQL log analyzer](https://github.com/darold/pgbadger) Docker image |
|                 |   |
| **Key**         | [pgBadger.port](operator.html#pgbadger-port)     |
| **Value**       | int       |
| **Example**     | `10000`     |
| **Description** | The port number for pgBadger |
|                 |   |
| **Key**         | [pgBadger.imagePullPolicy](operator.html#pgbadger-imagepullpolicy)   |
| **Value**       | string    |
| **Example**     | `Always`    |
| **Description** | This option is used to set the [policy](https://kubernetes.io/docs/concepts/containers/images/#updating-images) for updating pgBadger images |
