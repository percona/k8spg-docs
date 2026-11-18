> For the complete documentation index, see [llms.txt](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/llms.txt).

# Restore options: in-place restore vs cluster clone

You can restore PostgreSQL data in these ways:

- [**In-place restore**](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/backups-restore-inplace.html) – restore data into the same cluster using the [PerconaPGRestore] (restore-options.md) custom resource. By default, the Operator restores the most recent backup. You can specify what backup to restore from using the `--set` option.
- [**Cluster clone**](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/backups-clone.html) – create a new cluster using the `spec.dataSource` option in the Custom Resource of a **new** cluster. The data source can be a source cluster (`postgresCluster`), its data volume (`volumes`) or a `pgBackrest` backup from a cloud storage (`pgbackrest`).

Both approaches support full restore. For a restore to a specific moment, see [Point-in-time recovery](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/backups-pitr.html). Choose the method that fits your scenario.

## Choose a restore option

Use this flow to pick a restore path:

```
%%{ init : { "theme": "base", "themeVariables": {
  "primaryColor": "#93D0FF",
  "primaryTextColor": "#ffffff",
  "lineColor": "#ffffff",
  "background": "#1e1e1e"
} }}%%
flowchart LR
    q1{Must the same cluster<br/>come back quickly<br/>with the same endpoints?}
    q1 -->|Yes| inplace[In-place restore<br/>PerconaPGRestore]
    q1 -->|No| q2{Is the source cluster<br/>still running in this<br/>Kubernetes cluster?}
    q2 -->|Yes| q3{Reuse existing disks<br/>for a fast cutover?}
    q2 -->|No| pgbackrest[Clone with<br/>dataSource.pgbackrest<br/>object storage]
    q3 -->|Yes| volumes[Clone with<br/>dataSource.volumes]
    q3 -->|No| postgresCluster[Clone with<br/>dataSource.postgresCluster]
```

| Restore option                                                                                                  | When to use                                                                                                                                                                        | Pros                                                                                                                                                                                                                                                                             | Cons                                                                                                                                                    |
| --------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [In-place restore](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/backups-restore-inplace.html) | - Roll the **same** cluster back after a bad migration, accidental `DELETE`/`DROP` or data corruption - You need service restored quickly on the existing endpoints                | - Keeps the same cluster name, Services, and app connection strings - Simple to run - Supports full restore and [point-in-time recovery](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/backups-pitr-inplace.html)                                               | - **Destructive** — overwrites live data; - Introduces downtime; - No side-by-side validation; - A failed restore can leave the cluster non-operational |
| [Cluster clone](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/backups-clone.html)              | - Create a **side** cluster to test disaster recovery, investigate or recover without touching production data; - Spin up a copy for reporting, or rebuild when the source is gone | - Source stays intact for backup-based clones; - You can validate restored data before cutover; - Safer default for most recovery scenarios; - Supports [point-in-time recovery](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/backups-pitr-cluster-clone.html) | - Needs extra cluster resources and storage; - Apps must switch endpoints for cutover; - Restore from cloud-based backups takes time                    |

## If you clone: choose a data source

| Method                                                                                                                                                  | When to use                                                                                             | Pros                                                                                                                                                                                                  | Cons                                                                                                                                                                                                                                                                                                                                           |
| ------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [`dataSource.postgresCluster`](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/backups-clone.html#clone-from-an-existing-cluster)        | - Source still runs in this Kubernetes cluster; - You want a side copy in the same or another namespace | - Easiest clone when the source exists; - supports [point-in-time recovery](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/backups-pitr-cluster-clone.html); - source stays untouched | - Source must be available; - Doesn’t apply for a deleted cluster or another Kubernetes cluster; - Needs restore time and a full data copy; - Restore in another namespace require the Operator in the [cluster-wide mode](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/cluster-wide.html#install-the-operator-cluster-wide) |
| [`dataSource.pgbackrest`](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/backups-clone.html#clone-from-cloud-storage-s3-gcs-azure-blob) | Source is deleted, you restore into another Kubernetes cluster, or you only have object-storage backups | - Works without a live source; - Fits multi-cluster disaster recovery scenarios                                                                                                                       | - You must match path, stanza, Secret, and storage settings between the source and target clusters; - Cloud access credentials must exist in the target namespace; - Restore time and network or storage cost                                                                                                                                  |
| [`dataSource.volumes`](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/backups-clone.html#restore-using-data-volumes)                    | - Same-infrastructure cutover on existing disks; - Large dataset where a backup restore is too slow     | - Fastest bootstrap; - No object storage required for the cutover; - No double storage, unlike a backup-based restore                                                                                 | - Source must stop: downtime lasts until the new cluster accepts writes; - Ownership of the volumes moves to the new cluster; - Weak rollback after the new cluster writes (take a backup first); - Requires the same PostgreSQL major version, the same Kubernetes cluster, and compatible storage                                            |

## Next steps

[In-place restore](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/backups-restore-inplace.html) [Cluster clone](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/backups-clone.html)
