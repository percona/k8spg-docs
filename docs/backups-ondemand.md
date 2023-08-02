# Making on-demand backups

To make an on-demand backup manually, you need a backup configuration file. You can use the example of the backup configuration file [deploy/backup.yaml](https://github.com/percona/percona-postgresql-operator/blob/main/deploy/backup.yaml):

```yaml
apiVersion: pg.percona.com/v2beta1
kind: PerconaPGBackup
metadata:
  name: backup1
spec:
  pgCluster: cluster1
  repoName: repo1
#  options:
#  - --type=full
```

1. Before you start, make sure you have [configured a backup storage](backup-storage.md).
2. In the `deploy/backup.yaml` configuration file, specify the cluster name and the repository name to be used for backups. The repository name must be the same as the one you defined in the [backup storage configuration](backup-storage.md). 
3. If needed, you can add any 
[pgBackRest command line options](https://pgbackrest.org/configuration.html).

4. Make a backup with the following command:

    ``` {.bash data-prompt="$" }
    $ kubectl apply -f deploy/backup.yaml
    ```

!!! tip

    To list the backup, run:

    ``` {.bash data-prompt="$" }
    $ kubectl get pg-backup
    ```    