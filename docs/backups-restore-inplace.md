# Restore to an existing PostgreSQL cluster (in-place restore)

To restore data into an existing cluster, use the `PerconaPGRestore` custom resource. 

You can make a full restore or restore the database to a specific point in time. 

!!! important
    
    This operation overwrites the current data and is destructive.

Configure `PerconaPGRestore` custom resource using a *backup restore*
configuration file. The example of the backup configuration file is
[deploy/restore.yaml :octicons-link-external-16:](https://github.com/percona/percona-postgresql-operator/blob/v{{release}}/deploy/restore.yaml).

## Prepare your environment

Export the namespace where your cluster is running as an environment variable. Replace the `<namespace>` placeholder with your value:

```bash
export NAMESPACE=<namespace>
```

## Make a full restore from the latest backup (default)

Specify the following options in the `deploy/restore.yaml` configuration file for the `PerconaPGRestore` object:

* `pgCluster` - the name of your cluster,
* `repoName` - the name of the pgBackRest repository, where the backup is located. The repo with the same name must already be configured in the `backups.pgbackrest.repos` subsection of the cluster Custom Resource,
* `options` (optional) - additional [pgBackRest command line options :octicons-link-external-16:](https://pgbackrest.org/configuration.html).

Here is the example configuration:

```yaml
apiVersion: pgv2.percona.com/v2
kind: PerconaPGRestore
metadata:
  name: restore1
spec:
  pgCluster: cluster1
  repoName: repo1
```

Start the restore process:

```bash
kubectl apply -f deploy/restore.yaml -n $NAMESPACE
```

## Restore from a specific backup

When you have multiple backups, the Operator restores the [latest full backup](#make-a-full-restore-from-the-latest-backup-default) by default.

If you want to restore from a specific previous backup, use the `--set` option with the backup label. 

Here's the sequence of steps to follow:
{.power-number}

1. List available backups:

    ```bash
    kubectl get pg-backup -n $NAMESPACE
    ```

2. Get detailed information about the backup you wish to restore from:

    ```bash
    kubectl describe pg-backup <BACKUP NAME> -n $NAMESPACE
    ```

    ??? example "Sample output"

        ```text hl_lines="18 19"
        Name:         cluster1-backup-c55w-f858g
        Namespace:    default
        Labels:       <none>
        Annotations:  pgv2.percona.com/pgbackrest-backup-job-name: cluster1-backup-c55w
                      pgv2.percona.com/pgbackrest-backup-job-type: replica-create
        API Version:  pgv2.percona.com/v2
        Kind:         PerconaPGBackup
        Metadata:
          Creation Timestamp:  2024-06-28T07:44:08Z
          Generate Name:       cluster1-backup-c55w-
          Generation:          1
          Resource Version:    1199
          UID:                 92a8193c-6cbd-4cdf-82e5-a4623bf7f2d9
        Spec:
          Pg Cluster:  cluster1
          Repo Name:   repo1
        Status:
          Backup Name:  20240628-074416F
          Backup Type:  full
        ...
        ```

    Look for the "Backup Name" in the Status section (for example, `20240628-074416F`). This is the label that you will use with the `--set` option.

3. Modify the `deploy/restore.yaml` configuration file. Specify this information:
    * `pgCluster` - the name of your cluster
    * `repoName` - the name of the pgBackRest repository, where the backup is located. The repo with the same name must already be configured in the `backups.pgbackrest.repos` subsection of the cluster Custom Resource 
    * Configure the `options` section:
    
        * `--type=<type>` - Specify how you wish to restore the data. The `default` type restores the backup and replays WAL up to the end of available WAL. The `immediate` type restores the backup exactly as it was at the backup time, without replaying WAL.
        * `--set=<backup_label>` - Specify the backup label.

    Here's the example configuration to restore from a backup `20240628-074416F`:
    
    ```yaml
    apiVersion: pgv2.percona.com/v2
    kind: PerconaPGRestore
    metadata:
      name: restore1
    spec:
      pgCluster: cluster1
      repoName: repo1
      options:
      - --type=immediate
      - --set=20240628-074416F
    ```

4. Start the restore

    ```bash
    kubectl apply -f deploy/restore.yaml -n $NAMESPACE
    ```

## Restore the cluster with point-in-time recovery

Point-in-time recovery lets you restore your database to the  state it was before a change occurred (for example, before accidental data deletion or corruption).

!!! note

    To support this, the Operator automatically creates an initial full backup when your cluster is first created. This initial backup is used as the starting point for point-in-time recovery. This backup is required internally and does not appear when running `kubectl get pg-backup`.

By default, the Operator uses the latest successful full backup as the base for point-in-time restore. You can specify another  backup to use as the base by referencing its ID. Refer to the [Specify a base backup for point-in-time restore](#specify-a-base-backup-for-point-in-time-restore) section to learn more.

To make a point-in-time restore, you need the following:

* A backup that finished before your target time. You cannot restore to the time where there was no backup 
* All relevant WAL files must be successfully archived
* Use the `--type=time` and `--target` options in the `options` subsection of the `deploy/restore.yaml` configuration file.

Here's the sequence of steps to follow:
{.power-number}

1. List available backups:

    ```bash
    kubectl get pg-backup -n $NAMESPACE
    ```

2. Determine the target restore time. The Operator tracks the latest restorable time for each backup by default. To view this value, run:

    ```bash
    kubectl get pg-backup <backup_name> -n $NAMESPACE -o jsonpath='{.status.latestRestorableTime}'
    ```

3. Edit the `deploy/restore.yaml` configuration file and specify this information:

    * `pgCluster` - the name of your cluster
    * `repoName` - the name of the pgBackRest repository, where the backup is located. The repo with the same name must already be configured in the `backups.pgbackrest.repos` subsection of the cluster Custom Resource
    * Configure the `options` section:
    
        * `--type` - set to `time`,
        * `--target` set the target time that you retrieved at the previous step. The format is `<YYYY-MM-DD HH:MM:DD>`, optionally followed by a timezone offset: `"2021-04-16 15:13:32+00"` (`+00` here means UTC). 
 
    Here's the example configuration:

    ```yaml
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

4. Start the restore process:

    ```bash
    kubectl apply -f deploy/restore.yaml -n $NAMESPACE
     ```

### Specify a base backup for point-in-time restore

You can select a base backup for point-in-time restore. To do this you must get the backup ID and then specify it for the `--set` option in the restore configuration file. 

To get the backup ID, do the following:

1. Get the Pod name:

    ```bash
    kubectl get pods -n $NAMESPACE
    ```

2. Connect to the Pod and get the backupID with the `pgbackrest --stanza=db info` command :

    ```bash
    kubectl -n $NAMESPACE exec -it cluster1-instance1-hcgr-0 -c database -- pgbackrest --stanza=db info
    ```
        
    Find ID of the needed backup in the output:
        
    ```{.text .no-copy hl_lines="8"}
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
        
3. Reference this backup ID to the *backup restore* configuration file:

    ```yaml hl_lines="9"
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

4. Start the restore:

    ```bash
    kubectl apply -f deploy/restore.yaml -n $NAMESPACE
     ```

## Provide pgBackRest with a custom restore command

There may be cases where it is needed to control what files are restored from the backup and apply fine-grained filtering to them. For such scenarios there is a possibility to overwrite the [restore_command used in PosgreSQL archive recovery :octicons-link-external-16:](https://www.postgresql.org/docs/current/runtime-config-wal.html#RUNTIME-CONFIG-WAL-ARCHIVE-RECOVERY). You can do it in the `patroni.dynamicConfiguration` subsection of the Custom Resource as follows:

```yaml
patroni:
  dynamicConfiguration:
    postgresql:
      parameters:
        restore_command: "pgbackrest --stanza=db archive-get %f \"%p\""
```

The `%f` template in the above example is replaced by the name of the file to
retrieve from the archive, and `%p` is replaced by the copy destination path
name on the server. See [PostgreSQL official documentation :octicons-link-external-16:](https://www.postgresql.org/docs/current/runtime-config-wal.html#RUNTIME-CONFIG-WAL-RECOVERY) for more low-level details about this feature.

## Fix the cluster if the restore fails

The restore process overwrites database files. Wrong data or a misconfigured restore can leave your cluster in a non-operational state.

For example, incorrect `pgBackRest` arguments in the [PerconaPGRestore custom resource](#make-a-full-restore-from-the-latest-backup-default) can break the database while the restore hangs.

Here's what you can do:

* You can remove the restore annotation from your cluster Custom Resource to stop the restore:

    ```bash
    kubectl annotate -n $NAMESPACE pg cluster1 postgres-operator.crunchydata.com/pgbackrest-restore-
    ```

* Alternatively, you can delete the cluster [by removing the Custom Resource](delete.md#delete-a-database-cluster) and recreate it. Before you delete the Custom Resource, ensure the [`finalizers.percona.com/delete-pvc` finalizer](operator.md#finalizers-delete-pvc) is not set, or you will lose your data. Then run the same `kubectl apply` command you used to deploy the cluster originally.

Another example that can also cause restore failures is corrupted backup repository or missing files. In that case, [remove the Custom Resource](delete.md#delete-a-database-cluster), [locate and delete the startup PVC](debug-storage.md#check-the-pvc), then recreate the cluster.
