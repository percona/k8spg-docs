# Major version upgrade

Major version upgrade allows you to jump from one database major version to another (for example, upgrade from PostgreSQL 17.x to PostgreSQL 18.x).

This feature is generally available starting with the Operator version 2.9.0.

## Considerations

1. A major upgrade introduces a downtime because the whole cluster is shut down during the upgrade. This flow is planned to be improved in future releases.
2. During the upgrade, the Operator duplicates the data on each PVC and doesn't remove the old version data automatically. Make sure your PVC has enough free space to store data.
3. Starting with the Operator 2.6.0, PostgreSQL images are based on Red Hat Universal Base Image (UBI) 9 instead of UBI 8. UBI 9 has a different version of collation library `glibc` and this introduces a collation mismatch in PostgreSQL. Collation defines how text is sorted and compared based on language-specific rules such as case sensitivity, character order and the like. PostgreSQL stores the collation version used at database creation. When the collation version changes, this may result in corruption of database objects that use it like text-based indexes. Therefore, you need to identify and reindex objects affected by the collation mismatch.

## Upgrade steps

To start the upgrade, you need to create a special `PerconaPGUpgrade` resource. This resource refers to the special *Operator upgrade image* and contains the information about the existing and target major versions. Find the example `PerconaPGUpgrade` configuration file in `deploy/upgrade.yaml`:

```yaml
apiVersion: pgv2.percona.com/v2
kind: PerconaPGUpgrade
metadata:
  name: cluster1-17-to-18
spec:
  postgresClusterName: cluster1
  image: docker.io/percona/percona-postgresql-operator:{{ release }}-upgrade
  fromPostgresVersion: 17
  toPostgresVersion: 18
  toPostgresImage: docker.io/percona/percona-distribution-postgresql:{{ postgres18recommended }}
  toPgBouncerImage: docker.io/percona/percona-pgbouncer:{{ pgbouncerrecommended }}
  toPgBackRestImage: docker.io/percona/percona-pgbackrest:{{ pgbackrestrecommended }}
```

As you can see, the manifest includes image names for the database cluster components (PostgreSQL, pgBouncer, and pgBackRest). You can find them [in the list of certified images](images.md) for the current Operator release. For older versions, please refer to the [old releases documentation archive :octicons-link-external-16:](https://docs.percona.com/legacy-documentation/).

Apply this manifest to start the upgrade:

```bash
kubectl apply -f deploy/upgrade.yaml -n <namespace>
```

During the upgrade flow, the Operator:

1. Pauses the cluster, making it unavailable for the duration of the upgrade,
2. Annotates the cluster with a special `pgv2.percona.com/allow-upgrade`: `<PerconaPGUpgrade.Name>` annotation,
3. Creates jobs to migrate the data,
4. Starts up the cluster after the upgrade finishes.

## Post-upgrade steps

--8<-- "collation.txt"

## Cleanup

1. You can remove old version data at your discretion by [executing into containers](debug-shell.md) and running the following commands (example for PostgreSQL 17):

    ```bash
    rm -rf /pgdata/pg17
    rm -rf /pgdata/pg17_wal
    ```

2. You can also delete the `PerconaPGUpgrade` resource (this will clean up the jobs and Pods created during the upgrade):

    ```bash
    kubectl delete perconapgupgrade cluster1-17-to-18
    ```

## Troubleshooting upgrade issues

If the upgrade fails for some reason, the cluster will stay in paused mode. Resume the cluster [manually](pause.md) to check what went wrong with upgrade (it will start with the old version). You can check the `PerconaPGUpgrade` resource with `kubectl get perconapgupgrade -o yaml` command, and [check the logs](debug-logs.md) of the upgraded Pods to debug the issue.

### Failed first restore after the upgrade

During the restore, the Operator first restores the primary node. Then replicas rejoin it and start streaming data from a primary. PostgreSQL uses the pg_rewind tool to sync data with the primary.

It may happen that the primary and replica nodes have diverged too much and pg_rewind cannot find the common WAL point in their timeline history to start syncing the data from. This happens more often in clusters with low write traffic. In this case you may see the `could not find common ancestor of the source and target cluster's timelines` error in `pg_rewind`.

To address this issue, you must manually [reinitialize](reinit.md) the failed replica. Before doing so, check if this replica has any transactions that are not replicated anywhere else. Then remove its data directory and let the instance perform a full copy from the primary.

Alternatively, you can automate replica reinitialization with Patroni. Update the cluster configuration by setting the `spec.patroni.removeDataDirectoryOnDivergedTimelines` in the Custom Resource before the upgrade. When timeline divergence is detected, the Operator instructs Patroni
   to automatically remove the replica's data and resync it from the primary.

!!! warning

    The `removeDataDirectoryOnDivergedTimelines` option can lead to data loss.
    When the Operator resyncs the replica automatically, some transactions may
    be lost. The risk is usually small but not zero. Use this option only if you
    understand and accept this trade-off.

