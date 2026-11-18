> For the complete documentation index, see [llms.txt](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/llms.txt).

# Make scheduled backups

Backups schedule is defined on the per-repository basis in the `backups.pgbackrest.repos` subsection of the `deploy/cr.yaml` file.

You can supply each repository with a `schedules.<backup type>` key equal to an actual schedule that you specify in crontab format.

1. Before you start, make sure you have [configured a backup storage](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/backups-storage.html).
1. Configure backup schedule in the `deploy/cr.yaml` file. The schedule is specified in crontab format as explained in [Custom Resource options](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/operator.html#backupspgbackrestreposschedulesfull). The repository name must be the same as the one you defined in the [backup storage configuration](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/backups-storage.html). The following example shows the schedule for `repo1` repository:

```
...
backups:
  pgbackrest:
  ...
        repos:
        - name: repo1
          schedules:
            full: "0 0 * * 6"
            differential: "0 1 * * 1-6"
          ...
```

1. Update the cluster:

   ```
   kubectl apply -f deploy/cr.yaml
   ```

## Next steps

[Restore from a backup](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/backups-restore-inplace.html)

## Useful links

- [Backup retention](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/backup-retention.html)
- [Restore options](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/backups-restore.html)
