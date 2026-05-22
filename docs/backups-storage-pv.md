# Persistent Volume

Percona Operator for PostgreSQL uses [Kubernetes Persistent Volumes :octicons-link-external-16:](https://kubernetes.io/docs/concepts/storage/persistent-volumes/) for PostgreSQL data. You can use the same mechanism for backups on a volume attached to the pgBackRest Pod.

The Operator creates a Persistent Volume when it provisions the cluster. The default backup repository on a volume is `repo1` in `backups.pgbackrest.repos`:

```yaml
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

This configuration is enough to run backups. To use a specific [Storage Class :octicons-link-external-16:](https://kubernetes.io/docs/concepts/storage/storage-classes/), set it in `volumeClaimSpec` as described in the [Operator Custom Resource options](operator.md#backupspgbackrestreposvolumevolumeclaimspecstorageclassname).

## Next steps

[Make an on-demand backup](backups-ondemand.md){.md-button}
[Make a scheduled backup](backups-schedule.md){.md-button}
