> For the complete documentation index, see [llms.txt](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/llms.txt).

# Persistent Volume

Percona Operator for PostgreSQL uses [Kubernetes Persistent Volumes](https://kubernetes.io/docs/concepts/storage/persistent-volumes/) for PostgreSQL data. You can use the same mechanism for backups on a volume attached to the pgBackRest Pod.

The Operator creates a Persistent Volume when it provisions the cluster. The default backup repository on a volume is `repo1` in `backups.pgbackrest.repos`:

```
...
backups:
  pgbackrest:
    ...
    global:
      repo1-path: /pgbackrest/postgres-operator/cluster1/repo1
    ...
    repos:
    - name: repo1
      volume:
        volumeClaimSpec:
          accessModes:
          - ReadWriteOnce
          resources:
            requests:
              storage: 1Gi
```

This configuration is enough to run backups. To use a specific [Storage Class](https://kubernetes.io/docs/concepts/storage/storage-classes/) , set it in `volumeClaimSpec` as described in the [Operator Custom Resource options](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/operator.html#backupspgbackrestreposvolumevolumeclaimspecstorageclassname).

## Next steps

[Make an on-demand backup](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/backups-ondemand.html) [Make a scheduled backup](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/backups-schedule.html)
