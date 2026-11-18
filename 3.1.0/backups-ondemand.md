> For the complete documentation index, see [llms.txt](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/llms.txt).

# Making on-demand backups

To make an on-demand backup manually, you need a backup configuration file. You can use the example of the backup configuration file [deploy/backup.yaml](https://raw.githubusercontent.com/percona/percona-postgresql-operator/v3.1.0/deploy/backup.yaml) :

```
apiVersion: pgv2.percona.com/v2
kind: PerconaPGBackup
metadata:
  name: backup1
spec:
  pgCluster: cluster1
  repoName: repo1
#  options:
#  - --type=full
```

Here’s a sequence of steps to follow:

1. Before you start, make sure you have [configured a backup storage](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/backups-storage.html).

1. In the `deploy/backup.yaml` configuration file, specify the cluster name and the repository name to be used for backups. The repository name must be the same as the one you defined in the [backup storage configuration](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/backups-storage.html). It must also match the repository name specified in the `backups.pgbackrest.manual` subsection of the `deploy/cr.yaml` file.

1. If needed, you can add any [pgBackRest command line options](https://pgbackrest.org/configuration.html) .

1. Make a backup with the following command (modify the `-n postgres-operator` parameter if your database cluster resides in a different namespace):

   ```
   kubectl apply -f deploy/backup.yaml -n postgres-operator
   ```

   Expected output

   ```
   perconapgbackup.pgv2.percona.com/backup1 created
   ```

1. Making a backup takes time. Use the `kubectl get pg-backup` command to track the backup progress. When finished, backup should obtain the `Succeeded` status:

   ```
   kubectl get pg-backup backup1 -n postgres-operator
   ```

   Expected output

   ```
   NAME      CLUSTER    REPO    DESTINATION   STATUS      TYPE   COMPLETED   AGE
   backup1   cluster1   repo1                 Succeeded   incr   3m38s       3m53s
   ```

Tip

To list available backups, run:

```
kubectl get pg-backup -n postgres-operator
```

## Next steps

[Restore from a backup](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/backups-restore-inplace.html)

## Useful links

- [Backup retention](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/backup-retention.html)
- [Restore options](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/backups-restore.html)
