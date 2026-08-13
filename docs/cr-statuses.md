# Custom resource statuses

Status fields show the current state of a Custom Resource (CR). The Operator sets these fields in the `.status` section of a Custom Resource. You do not edit the status.

Use status values to confirm progress, detect failures and decide when it is safe to run the next action. For example, start a backup after the cluster is ready for backups, or start a restore after a backup has succeeded.

## How to view custom resource statuses

To check the status of your Percona custom resources, use the `kubectl get <resource-type>` or `kubectl describe <resource-type>` commands. See how to use them to get the quick overview, in-depth details, and targeted queries.

### Get a quick overview

List your resources and check their high-level STATUS:

```bash
kubectl get pg -n <namespace>
kubectl get pg-backup -n <namespace>
kubectl get pg-restore -n <namespace>
```

??? example "Sample output for PerconaPGCluster"

    ```{.text .no-copy}
    NAME       ENDPOINT                            STATUS   POSTGRES   PGBOUNCER   AGE
    cluster1   cluster1-pgbouncer.default.svc      ready    3          3           30m
    ```

### View full details

See all status details as well as conditions and events:

```bash
kubectl get pg <cluster-name> -n <namespace> -o yaml
kubectl describe pg <cluster-name> -n <namespace>
```

Check for the `.status` field in the output to find the current state, readiness, messages, and conditions.

### Query a status field directly

You can extract specific status fields using `jsonpath`.

**Example 1. Check whether the cluster is ready for backups:**

```bash
kubectl get pg <cluster-name> -n <namespace> \
  -o jsonpath='{range .status.conditions[?(@.type=="ReadyForBackup")]}{.lastTransitionTime}{"\n"}{.reason}{"\n"}{.status}{"\n"}{.type}{"\n"}{end}'
```

??? example "Sample output"

    ```{.text .no-copy}
    2026-07-22T12:34:56Z
    AllConditionsAreTrue
    True
    ReadyForBackup
    ```

**Example 2. Get the latest restorable backup time:**

```bash
kubectl get pg-backup <backup-name> -n <namespace> \
  -o jsonpath='{.status.latestRestorableTime}'
```

??? example "Sample output"

    ```{.text .no-copy}
    2026-07-22 12:22:17.000000+0000
    ```

**Example 3. Check standby replication lag:**

```bash
kubectl get pg <cluster-name> -n <namespace> \
  -o jsonpath='{.status.standby.lagBytes}{"\n"}{.status.standby.lagLastComputedAt}{"\n"}'
```

??? example "Sample output"

    ```{.text .no-copy}
    2343212
    2026-07-22T12:07:05Z
    ```

## PerconaPGCluster status

The main cluster state is recorded in `status.state`. For component-level readiness, see `status.postgres` and `status.pgbouncer`. Backup repository details appear under `status.pgbackrest`, and Patroni details under `status.patroni`.

Common fields:

* `status.state` – overall cluster state
* `status.postgres.ready` / `status.postgres.size` – number of ready PostgreSQL Pods and the configured size
* `status.postgres.instances` – readiness per instance set
* `status.pgbouncer.ready` / `status.pgbouncer.size` – number of ready PgBouncer Pods and the configured size
* `status.host` – connection endpoint (primary Service or PgBouncer, depending on your proxy configuration)
* `status.pgbackrest` – pgBackRest repository host, repos, and backup or restore job status
* `status.patroni` – Patroni version and status (system identifier, switchover tracking)
* `status.standby` – replication lag for standby clusters when lag detection is enabled
* `status.logicalReplicas` – state of each [logical replica](logical-replication.md)
* `status.conditions` – detailed condition list with reason and message. See [Conditions](#conditions) for details.
* `status.observedGeneration` – the generation of the Custom Resource that the Operator last successfully wrote into status.
* `status.installedCustomExtensions` – names of custom extensions installed from the Custom Resource

### Cluster state values

`status.state` values are:

| Value | Meaning |
| --- | --- |
| `initializing` | The Operator is creating or reconciling the cluster. PostgreSQL Pods, PgBouncer Pods, or the pgBackRest repo host are not ready yet, or an update is still rolling out. |
| `stopping` | The cluster is paused (`spec.pause: true`) but some PostgreSQL Pods are still ready. |
| `paused` | The cluster is paused and no PostgreSQL Pods are ready. |
| `ready` | PostgreSQL and PgBouncer Pods match the desired size, the pgBackRest repo host is ready, and instance updates have finished. |

Unlike some other Percona Operators, `PerconaPGCluster` does not use an `error` value for `status.state`. Investigate problems through conditions, events, and Pod or Job status.

### Conditions

Conditions show more detail about cluster state changes. You can see them in `status.conditions[]`.

Common condition fields:

* `type` – condition type
* `status` – condition status
* `reason` – short reason string
* `message` – human-readable details

`status.conditions[].type` values:

| Value | Meaning |
| --- | --- |
| `ReadyForBackup` | The cluster is ready for backup operations. Set to `True` when the pgBackRest repo host is ready and a replica-create backup is available. |
| `PGBackRestRepoHostReady` | The dedicated pgBackRest repository host is ready. |
| `PGBackRestReplicaCreate` | pgBackRest can be used for replica creation (a suitable backup exists). |
| `PGBackRestReplicaRepoReady` | The pgBackRest repository used for creating replicas is ready. |
| `PGBackRestManualBackupSuccessful` | Indicates whether or not the latest on-demand backup for the current backup ID completed successfully. |
| `PGBackRestoreProgressing` | An in-place pgBackRest restore is in progress. |
| `PostgresDataInitialized` | The PostgreSQL data directory has been initialized (for example, via a restore). |
| `ProxyAvailable` | The PgBouncer Deployment is available. |
| `Progressing` | The cluster is progressing through a reconciliation or change. |
| `PersistentVolumeResizing` | A Persistent Volume resize is in progress. |
| `StandbyLagging` | The standby cluster WAL lag exceeds `spec.standby.maxAcceptableLag`. See [Detect replication lag for standby cluster](standby.md#detect-replication-lag-for-standby-cluster). |
| `ReadyForLogicalReplication` | The primary is ready for logical replica bootstrap. See [Logical replicas](logical-replication.md). |
| `APIGroupMigration` | Migration of child object owner references to the new upstream API group is complete, in progress, or not needed. Relevant for upgrades to Operator 3.0.0 and later. See [Upgrade the Operator](update-operator.md). |
| `RepoDeploymentNotFound` | A pgBackRest repository deployment was not found during reconciliation. |
| `RepoHostCreated` | A pgBackRest repository host was created. |


`status.conditions[].status` values:

| Value | Meaning |
| --- | --- |
| `True` | The condition is currently true. |
| `False` | The condition is currently false. |
| `Unknown` | The Operator could not determine the condition state. |

The Operator sets `reason` and `message` values as free-form strings. Common reasons include:

* `AllConditionsAreTrue`, `PGBackRestRepoHostReady`, `PGBackRestReplicaCreate` (for `ReadyForBackup`)
* `RepoHostReady`, `RepoHostNotReady`, `RepoHostStatusMissing`
* `LagDetected`, `LagNotDetected`, `ErrorGettingLag`, `MainSiteNotFound` (for `StandbyLagging`)
* `APIGroupMigrationCompleted`, `APIGroupMigrationInProgress`, `APIGroupMigrationNotNeeded`
* `ReadyForRestore`, `RestoreInPlaceRequested`, `PGBackRestRestoreComplete`, `PGBackRestRestoreFailed`
* `ManualBackupComplete`, `ManualBackupFailed`

### Standby status

When you enable replication lag detection on a [standby cluster](standby.md), the Operator also populates `status.standby`:

| Field | Meaning |
| --- | --- |
| `status.standby.lagBytes` | Current WAL lag in bytes |
| `status.standby.lagLastComputedAt` | Timestamp of the last lag check |

When lag exceeds your threshold, `status.state` becomes `initializing`, the standby primary Pod is marked unready, and the `StandbyLagging` condition is set to `True`.

### Logical replica status

When you define [logical replicas](logical-replication.md), the Operator populates `status.logicalReplicas[]`:

| Field | Meaning |
| --- | --- |
| `name` | Replica name from the spec |
| `state` | `bootstrapping`, `ready`, `broken`, or `suspended` |
| `reason` | Why the replica is not ready (see below) |
| `message` | Human-readable details |
| `databases` | Databases frozen at bootstrap |
| `seededAt` | When the data directory was copied |
| `invalidatedAt` | When an in-place restore made the replica unusable |

`state` values:

| Value | Meaning |
| --- | --- |
| `bootstrapping` | Waiting for the primary, databases, or volume, or the bootstrap Job is still running |
| `ready` | Slots exist on the primary and apply workers are running |
| `broken` | Replication cannot continue until you [reseed](logical-replication.md#reseed-a-logical-replica) a replica, or teardown is waiting for the primary |
| `suspended` | The Operator stopped the replica because the source cluster is being restored |

Common `reason` values: `PrimaryNotReady`, `WaitingForDatabases`, `WaitingForDataVolume`, `BootstrapFailed`, `SourceSlotMissing`, `SubscriptionDisabled`, `ApplyWorkerDown`, `SourceRestoring`, `SourceRestored`, `AwaitingCleanup`.

**Example. Check logical replica state:**

```bash
kubectl get pg <cluster-name> -n <namespace> \
  -o jsonpath='{.status.logicalReplicas}' && echo
```

## PerconaPGBackup status

Backup progress and results are in `status.state`. You also get destination, type, and timing details that help you validate backups and point-in-time recovery ranges. Backups are managed with `pgBackRest` (or `VolumeSnapshots` when you choose that method).

Common fields are:

* `status.backupName` – pgBackRest backup name
* `status.backupType` – backup type (`full`, `differential`, `incremental`, or `snapshot`)
* `status.completed` – completion timestamp
* `status.crVersion` - the Operator version that took the backup
* `status.conditions` – backup-related conditions (for example, lease acquisition)
* `status.destination` – backup path or URL
* `status.image` - the Operator image
* `status.error` – error details when the backup fails
* `status.jobName` – Kubernetes Job that ran the backup
* `status.latestRestorableTime` – latest point for point-in-time recovery from this backup
* `status.repo` – the details of the pgBackRest repository where the backup is stored
* `status.size` - the size of the backup taken. Applies for full, incremental and differential backups.
* `status.snapshot` – VolumeSnapshot references when the backup method is `volumeSnapshot`
* `status.state` – backup job state
* `status.storageType` – storage backend (`s3`, `gcs`, `azure`, or `filesystem`)

### Backup state values

`status.state` values are:

| Value | Meaning |
| --- | --- |
| `""` | Backup is created but not processed yet. |
| `Starting` | The Operator is preparing the backup Job. |
| `Running` | Backup is in progress. |
| `Succeeded` | Backup completed successfully. |
| `Failed` | Backup failed. Check `status.error` and related Jobs. |

### Backup conditions

`PerconaPGBackup` may include conditions such as:

| Value | Meaning |
| --- | --- |
| `BackupLeaseAcquired` | The backup acquired the lease required to run. When `False`, another backup may still hold the lease. |

## PerconaPGRestore status

Restore progress and results are in `status.state`. Use these fields to confirm when a restore starts, finishes, or fails.

Common fields:

* `status.state` – restore job state
* `status.jobName` – Kubernetes Job that ran the restore
* `status.completed` – completion timestamp

For in-place restores driven through the cluster Custom Resource, also check the `PGBackRestoreProgressing` condition on the related `PerconaPGCluster`.

### Restore state values

`status.state` values are:

| Value | Meaning |
| --- | --- |
| `""` | Restore is created but not processed yet. |
| `Starting` | The Operator is preparing the restore Job. |
| `Running` | Restore is in progress. |
| `Succeeded` | Restore completed successfully. |
| `Failed` | Restore failed. Check Jobs, events, and cluster conditions. |

## PerconaPGUpgrade status

Major PostgreSQL upgrades use the `PerconaPGUpgrade` Custom Resource. Progress is reported through conditions rather than a single `status.state` field.

Common fields:

* `status.conditions` – upgrade progress and result
* `status.observedGeneration` – the resource generation that the Operator last reconciled

`status.conditions[].type` values:

| Value | Meaning |
| --- | --- |
| `Progressing` | A major PostgreSQL upgrade is in progress. |
| `Succeeded` | The major upgrade finished successfully when the condition status is `True`. |
