# Making on-demand backups

To make an on-demand backup manually, you need a backup configuration file. You can use the example of the backup configuration file [deploy/backup.yaml :octicons-link-external-16:](https://raw.githubusercontent.com/percona/percona-postgresql-operator/v{{ release }}/deploy/backup.yaml):

```yaml
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

Here's a sequence of steps to follow:
{.power-number}

1. Before you start, make sure you have [configured a backup storage](backups-storage.md).
2. In the `deploy/backup.yaml` configuration file, specify the cluster name and the repository name to be used for backups. The repository name must be the same as the one you defined in the [backup storage configuration](backups-storage.md). It must also match the repository name specified in the `backups.pgbackrest.manual` subsection of the `deploy/cr.yaml` file.
3. If needed, you can add any 
[pgBackRest command line options :octicons-link-external-16:](https://pgbackrest.org/configuration.html).

4. Make a backup with the following command (modify the `-n postgres-operator` parameter if your database cluster resides in a different namespace):

    ``` {.bash data-prompt="$" }
    $ kubectl apply -f deploy/backup.yaml -n postgres-operator
    ```

    ??? example "Expected output"

        ``` {.text .no-copy}
        perconapgbackup.pgv2.percona.com/backup1 created
        ```

5. Making a backup takes time. You can track the process with `kubectl get pg-backup` command. When finished, backup should obtain the `Succeeded` status:

    ``` {.bash data-prompt="$" }
    $ kubectl get pg-backup backup1 -n postgres-operator
    ```
    ???+ example "Expected output"

        ``` {.text .no-copy}
        NAME      CLUSTER    REPO    DESTINATION   STATUS      TYPE   COMPLETED   AGE
        backup1   cluster1   repo1                 Succeeded   incr   3m38s       3m53s
        ```

!!! tip

    To list available backups, run:

    ``` {.bash data-prompt="$" }
    $ kubectl get pg-backup -n postgres-operator
    ```

## Next steps

[Restore from a backup](backups-restore.md)

## Useful links

[Backup retention](backup-retention.md)
