# Point-in-time recovery

Point-in-time recovery (PITR) lets you restore your database to the state it was in before a change occurred. For example, before accidental data deletion or corruption.

This document explains how point-in-time recovery works with the Operator and how to use the latest restorable time when you choose a restore target. If you already know the concept and want the steps, jump to a tutorial:

* [In-place restore with point-in-time recovery](backups-pitr-inplace.md)
* [Restore to a new cluster with point-in-time recovery](backups-pitr-cluster-clone.md)
* [In-place restore with point-in-time recovery from a PVC snapshot](backups-pvc-usage.md#in-place-restore-with-point-in-time-recovery)

## How it works

Point-in-time recovery combines a base backup with Write-Ahead Log (WAL) archives:

1. The Operator restores a backup that finished **before** your target time.
2. PostgreSQL then replays archived WAL to bring the database forward to that time.

The Operator automatically creates an initial full backup when it creates a new cluster for you. That backup is the starting point for point-in-time recovery. It is required internally and does not appear when you run `kubectl get pg-backup`.

By default, the Operator uses the latest successful full backup as the base. You can point restore at another backup by its ID. See [Specify a base backup for point-in-time restore](backups-pitr-inplace.md#specify-a-base-backup-for-point-in-time-restore).

## What you need

To make a point-in-time restore, you need the following:

* A backup that finished before your target time. You cannot restore to a time where there was no backup.
* All relevant WAL files successfully archived to the backup repository.
* The `--type=time` and `--target` options in your restore configuration. You specify them either in the `PerconaPGRestore` object for in-place restore, or in the `dataSource` options in the target cluster's Custom Resource during a cluster clone.

## Latest restorable time

By default, the Operator tracks the latest restorable time for a backup. This behavior is controlled by the [backups.trackLatestRestorableTime](operator.md#backupstracklatestrestorabletime) Custom Resource option. 

When tracking is enabled, the Operator records the timestamp of the latest committed transaction that has been archived to the backup repository. That value appears on the latest successful backup as `status.latestRestorableTime`. Use it as a safe upper bound when you choose a point-in-time restore target.

The Operator updates this field as WAL is archived. 

To view the latest restorable time, run:

```bash
kubectl get pg-backup <backup_name> -n $NAMESPACE \
  -o jsonpath='{.status.latestRestorableTime}'
```

??? example "Sample output"

    ```{.text .no-copy}
    2025-06-13 18:52:33.238533+0000
    ```

Consider the following:

* The field advances only when archived WAL contains `COMMIT` records. Some internal database activity increases commit counters without writing those records to WAL, so an idle cluster may not refresh the value.
* The timestamp reflects the last archived WAL with commits, not the current tip of the primary. By default, PostgreSQL switches WAL every 60 seconds. This interval is defined by the `archive_timeout` option.
* If the field is empty or stale while you test on an idle cluster, create a small write transaction (for example, an `INSERT` or `UPDATE`) and wait for the next WAL archive.

### Disable latest restorable time tracking

Set `backups.trackLatestRestorableTime` to `false` if you do not need this helper. For example, to reduce archive overhead or S3 API usage from status checks or if a restricted security policy conflicts with the tracking archive command.

```yaml
spec:
  backups:
    trackLatestRestorableTime: false
```

Backups and restores continue to work. When tracking is disabled, the Operator also does not inject the tracking logic into `archive_command`.

## Next steps

[In-place point-in-time restore](backups-pitr-inplace.md){.md-button}
[Clone with point-in-time recovery](backups-pitr-cluster-clone.md){.md-button}
[Point-in-time restore from a PVC snapshot](backups-pvc-usage.md#in-place-restore-with-point-in-time-recovery){.md-button}
