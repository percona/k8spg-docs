> For the complete documentation index, see [llms.txt](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/llms.txt).

# In-place restore with point-in-time recovery

Restore an existing cluster to a specific moment using a base backup and archived WAL. This operation uses the `PerconaPGRestore` custom resource.

Important

This operation overwrites the current data and is destructive.

For how point-in-time recovery works and how to use the latest restorable time, see [Point-in-time recovery](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/backups-pitr.html). For a full restore to the same cluster (without a target time), see [Restore to an existing PostgreSQL cluster](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/backups-restore-inplace.html).

If you restore from a PVC snapshot and then replay WAL, follow [In-place restore with point-in-time recovery from a PVC snapshot](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/backups-pvc-usage.html#in-place-restore-with-point-in-time-recovery) instead.

## Prepare your environment

Export the namespace where your cluster is running as an environment variable. Replace the `<namespace>` placeholder with your value:

```
export NAMESPACE=<namespace>
```

## Restore to a point in time

To make a point-in-time restore, you need the following:

- A backup that finished before your target time. You cannot restore to the time where there was no backup
- All relevant WAL files must be successfully archived
- The `--type=time` and `--target` options in the `options` subsection of the `deploy/restore.yaml` configuration file

Here’s the sequence of steps to follow:

1. List available backups:

   ```
   kubectl get pg-backup -n $NAMESPACE
   ```

1. Determine the target restore time. Use the [latest restorable time](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/backups-pitr.html#latest-restorable-time) from your backup, or another timestamp that falls after a completed backup and within archived WAL:

   ```
   kubectl get pg-backup <backup_name> -n $NAMESPACE \
     -o jsonpath='{.status.latestRestorableTime}'
   ```

1. Edit the `deploy/restore.yaml` configuration file and specify this information:

   - `pgCluster` - the name of your cluster

   - `repoName` - the name of the pgBackRest repository, where the backup is located. The repo with the same name must already be configured in the `backups.pgbackrest.repos` subsection of the cluster Custom Resource

   - Configure the `options` section:

     - `--type` - set to `time`.
     - `--target` - set the target time that you retrieved at the previous step. The format is `<YYYY-MM-DD HH:MM:DD>`, optionally followed by a timezone offset: “2021-04-16 15:13:32+00” (`+00` here means UTC).

   Here’s the example configuration:

   ```
   apiVersion: pgv2.percona.com/v2
   kind: PerconaPGRestore
   metadata:
     name: restore1
   spec:
     pgCluster: cluster1
     repoName: repo1
     options:
     - --type=time
     - --target="2025-11-30 15:12:11+03"
   ```

1. Start the restore process:

   ```
   kubectl apply -f deploy/restore.yaml -n $NAMESPACE
   ```

## Specify a base backup for point-in-time restore

By default, the Operator uses the latest successful full backup as the base. You can select another base backup by its ID and pass it with the `--set` option in the restore configuration file.

To get the backup ID, do the following:

1. Get the Pod name:

   ```
   kubectl get pods -n $NAMESPACE
   ```

1. Connect to the Pod and get the backup ID with the `pgbackrest --stanza=db info` command:

   ```
   kubectl -n $NAMESPACE exec -it cluster1-instance1-hcgr-0 -c database -- pgbackrest --stanza=db info
   ```

   Find ID of the needed backup in the output:

   ```
   stanza: db
       status: ok
       cipher: none

       db (prior)
           wal archive min/max (16): 0000000F000000000000001C/0000002000000036000000C5

           full backup: 20240401-173403F
               timestamp start/stop: 2024-04-01 17:34:03+00 / 2024-04-01 17:36:57+00
               wal start/stop: 000000120000000000000022 / 000000120000000000000024
               database size: 31MB, database backup size: 31MB
               repo1: backup set size: 4.1MB, backup size: 4.1MB

           incr backup: 20240401-173403F_20240415-201250I
               timestamp start/stop: 2024-04-15 20:12:50+00 / 2024-04-15 20:14:19+00
               wal start/stop: 00000019000000000000005C / 00000019000000000000005D
               database size: 46.0MB, database backup size: 25.7MB
               repo1: backup set size: 6.1MB, backup size: 3.8MB
               backup reference list: 20240401-173403F

           incr backup: 20240401-173403F_20240415-201430I
   ...
   ```

1. Reference this backup ID in the *backup restore* configuration file:

   ```
   apiVersion: pgv2.percona.com/v2
   kind: PerconaPGRestore
   metadata:
     name: restore1
   spec:
     pgCluster: cluster1
     repoName: repo1
     options:
     - --type=time
     - --target="2024-04-01 17:36:57+00"
     - --set="20240401-173403F"
   ```

1. Start the restore:

   ```
   kubectl apply -f deploy/restore.yaml -n $NAMESPACE
   ```

## Related topics

- [Point-in-time recovery](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/backups-pitr.html)
- [Cluster clone with point-in-time recovery](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/backups-pitr-cluster-clone.html)
- [In-place restore with point-in-time recovery from a PVC snapshot](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/backups-pvc-usage.html#in-place-restore-with-point-in-time-recovery)
- [Troubleshoot restore failures](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/debug-restore.html)
