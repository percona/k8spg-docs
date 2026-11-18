> For the complete documentation index, see [llms.txt](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/llms.txt).

# Restore to an existing PostgreSQL cluster (in-place restore)

To restore data into an existing cluster, use the `PerconaPGRestore` custom resource.

Use this document to make **a full restore**. For a restore to a specific moment, use the [In-place restore with point-in-time recovery](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/backups-pitr-inplace.html) tutorial.

Warning

This operation overwrites the current data and is destructive. Test it on a staging environment first.

An in-place restore also invalidates [logical replicas](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/logical-replication.html). After the restore, [reseed](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/logical-replication.html#reseed-a-logical-replica) each replica.

Configure `PerconaPGRestore` custom resource using a *backup restore* configuration file. The example of the backup configuration file is [deploy/restore.yaml](https://github.com/percona/percona-postgresql-operator/blob/v3.1.0/deploy/restore.yaml) .

## Prepare your environment

Export the namespace where your cluster is running as an environment variable. Replace the `<namespace>` placeholder with your value:

```
export NAMESPACE=<namespace>
```

## Make a full restore from the latest backup (default)

Specify the following options in the `deploy/restore.yaml` configuration file for the `PerconaPGRestore` object:

- `pgCluster` - the name of your cluster,
- `repoName` - the name of the pgBackRest repository, where the backup is located. The repo with the same name must already be configured in the `backups.pgbackrest.repos` subsection of the cluster Custom Resource,
- `options` (optional) - additional [pgBackRest command line options](https://pgbackrest.org/configuration.html) .

Here is the example configuration:

```
apiVersion: pgv2.percona.com/v2
kind: PerconaPGRestore
metadata:
  name: restore1
spec:
  pgCluster: cluster1
  repoName: repo1
```

Start the restore process:

```
kubectl apply -f deploy/restore.yaml -n $NAMESPACE
```

## Restore from a specific backup

When you have multiple backups, the Operator restores the [latest full backup](#make-a-full-restore-from-the-latest-backup-default) by default.

If you want to restore from a specific previous backup, use the `--set` option with the backup label.

Here’s the sequence of steps to follow:

1. List available backups:

   ```
   kubectl get pg-backup -n $NAMESPACE
   ```

1. Get detailed information about the backup you wish to restore from:

   ```
   kubectl describe pg-backup <BACKUP NAME> -n $NAMESPACE
   ```

   Sample output

   ```
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

   Look for the “Backup Name” in the Status section (for example, `20240628-074416F`). This is the label that you will use with the `--set` option.

1. Modify the `deploy/restore.yaml` configuration file. Specify this information:

   - `pgCluster` - the name of your cluster

   - `repoName` - the name of the pgBackRest repository, where the backup is located. The repo with the same name must already be configured in the `backups.pgbackrest.repos` subsection of the cluster Custom Resource

   - Configure the `options` section:

     - `--type=<type>` - Specify how you wish to restore the data. The `default` type restores the backup and replays WAL up to the end of available WAL. The `immediate` type restores the backup exactly as it was at the backup time, without replaying WAL.
     - `--set=<backup_label>` - Specify the backup label.

   Here’s the example configuration to restore from a backup `20240628-074416F`:

   ```
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

1. Start the restore

   ```
   kubectl apply -f deploy/restore.yaml -n $NAMESPACE
   ```

## Provide pgBackRest with a custom restore command

There may be cases where it is needed to control what files are restored from the backup and apply fine-grained filtering to them. For such scenarios there is a possibility to overwrite the [restore_command used in PosgreSQL archive recovery](https://www.postgresql.org/docs/current/runtime-config-wal.html#RUNTIME-CONFIG-WAL-ARCHIVE-RECOVERY) . You can do it in the `patroni.dynamicConfiguration` subsection of the Custom Resource as follows:

```
patroni:
  dynamicConfiguration:
    postgresql:
      parameters:
        restore_command: "pgbackrest --stanza=db archive-get %f \"%p\""
```

The `%f` template in the above example is replaced by the name of the file to retrieve from the archive, and `%p` is replaced by the copy destination path name on the server. See [PostgreSQL official documentation](https://www.postgresql.org/docs/current/runtime-config-wal.html#RUNTIME-CONFIG-WAL-RECOVERY) for more low-level details about this feature.

## Fix the cluster if the restore fails

If the restore fails, see [Troubleshoot restore failures](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/debug-restore.html).
