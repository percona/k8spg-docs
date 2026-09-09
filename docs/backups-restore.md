# Restore options: in-place restore vs cluster clone

You can restore PostgreSQL data in these ways:

* [**In-place restore**](backups-restore-inplace.md) – restore
data into the same cluster using the [PerconaPGRestore]
(restore-options.md) custom resource. By default, the Operator
restores the most recent backup. You can specify what backup to
restore from using the `--set` option.
* [**Cluster clone**](backups-clone.md) – create a new cluster using the `spec.dataSource` option in the Custom
Resource of a **new** cluster. The data source can be a source cluster (`postgresCluster`), its data volume (`volumes`) or a `pgBackrest` backup from a cloud storage (`pgbackrest`).

Both approaches support full restore. For a restore to a specific moment, see [Point-in-time recovery](backups-pitr.md).
Choose the method that fits your scenario.

## Choose a restore option

Use this flow to pick a restore path:

```mermaid
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



| Restore option | When to use | Pros | Cons |
| --- | --- | --- | --- |
| [In-place restore](backups-restore-inplace.md) | - Roll the **same** cluster back after a bad migration, accidental `DELETE`/`DROP` or data corruption <br> - You need service restored quickly on the existing endpoints | - Keeps the same cluster name, Services, and app connection strings <br> - Simple to run <br> - Supports full restore and [point-in-time recovery](backups-pitr-inplace.md) | - **Destructive** — overwrites live data; <br> - Introduces downtime; <br> - No side-by-side validation; <br> - A failed restore can leave the cluster non-operational |
| [Cluster clone](backups-clone.md) | - Create a **side** cluster to test disaster recovery, investigate or recover without touching production data; <br> - Spin up a copy for reporting, or rebuild when the source is gone | - Source stays intact for backup-based clones; <br> - You can validate restored data before cutover; <br> - Safer default for most recovery scenarios; <br> - Supports [point-in-time recovery](backups-pitr-cluster-clone.md) | - Needs extra cluster resources and storage; <br> - Apps must switch endpoints for cutover; <br> - Restore from cloud-based backups takes time |

## If you clone: choose a data source

| Method | When to use | Pros | Cons |
| --- | --- | --- | --- |
| [`dataSource.postgresCluster`](backups-clone.md#datasourcepostgrescluster) | - Source still runs in this Kubernetes cluster; <br> - You want a side copy in the same or another namespace | - Easiest clone when the source exists; <br> - supports [point-in-time recovery](backups-pitr-cluster-clone.md); <br> - source stays untouched | - Source must be available; <br> - Doesn't apply for a deleted cluster or another Kubernetes cluster; <br> - Needs restore time and a full data copy |
| [`dataSource.pgbackrest`](backups-clone.md#datasourcepgbackrest) | Source is deleted, you restore into another Kubernetes cluster, or you only have object-storage backups | - Works without a live source; <br> - Fits multi-cluster disaster recovery scenarios | - You must match path, stanza, Secret, and storage settings; <br> - Restore time and network cost |
| [`dataSource.volumes`](backups-clone.md#datasourcevolumes) | - Same-infrastructure cutover on existing disks; <br> - Large dataset where a backup restore is too slow | - Fastest bootstrap; <br> - No object storage required for the cutover | - Source must stop; <br> - Weak rollback after the new cluster writes |

## Next steps

[In-place restore](backups-restore-inplace.md){.md-button}
[Cluster clone](backups-clone.md){.md-button}

