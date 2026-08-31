# Cluster clone with point-in-time recovery

Restore a backup to a **new** cluster and bring it forward to a specific moment using archived WAL. You define the restore in the Custom Resource of the new cluster under `spec.dataSource`.

For how point-in-time recovery works and how to use the latest restorable time, see [Point-in-time recovery](backups-pitr.md). For a full clone without a target time, see [Restore the backup to a new cluster](backups-clone.md).

If you create a new cluster from a PVC snapshot, see [Create a new cluster from a PVC snapshot](backups-pvc-usage.md#create-a-new-cluster-from-a-pvc-snapshot). 

## What you need

To perform a point-in-time recovery, ensure you have:

* A backup that completed before your chosen target time. Restores cannot go back further than your available backups.
* All relevant WAL files archived successfully
* The `--type=time` and `--target` options included in the `dataSource.postgresCluster.options` section of your cluster spec

## Make a clone with point-in-time recovery

Add the `dataSource.postgresCluster` section to the Custom Resource of the *new* cluster. Define these key fields:

* `clusterName` – name of the source cluster
* `clusterNamespace` – namespace of the source cluster (required when cloning to a different namespace; requires the Operator in [cluster-wide mode](cluster-wide.md#install-the-operator-cluster-wide))
* `repoName` – name of the pgBackRest repository in the source cluster containing the backup to use for the restore
* `options` – `pgBackRest` options for point-in-time recovery:

    * `--type=time`: Instructs pgBackRest to initiate a point-in-time recovery.
    * `--target`: The timestamp up to which to restore the data. To get the timestamp, run this command on the **source cluster**:

        ```bash
        kubectl get pg-backup <backup_name> -n <namespace> \
          -o jsonpath='{.status.latestRestorableTime}'
        ```

        See [Latest restorable time](backups-pitr.md#latest-restorable-time) for more information.

    * `--set` (optional): Allows you to specify a particular backup as the starting point for point-in-time recovery. For more information on how to do this, see [Specify a base backup for point-in-time restore](backups-pitr-inplace.md#specify-a-base-backup-for-point-in-time-restore).

You also need to configure the storage and backup settings for the new cluster:

* In the `instances` section, define the `dataVolumeClaimSpec` for your new cluster, which sets up the PVC. This determines the storage resources (size, access mode, etc.) allocated for your cloned database data.
* In the `backups.pgbackrest.repos` section, set up a backup repository for the new cluster. The repo name must match the one used in `repoName` above. Also configure the backup storage. This ensures the new cluster both restores data and is able to perform its own backups independently.

The following example creates a cluster named `cluster2` as a point-in-time clone of `cluster1` in the `percona-db-1` namespace:

  ```yaml
  apiVersion: pgv2.percona.com/v2
  kind: PerconaPGCluster
  metadata:
    name: cluster2
  spec:
    crVersion: {{ release }}
    dataSource:
      postgresCluster:
        clusterName: cluster1
        clusterNamespace: percona-db-1
        repoName: repo1
        options:
        - --type=time
        - --target="2025-11-30 15:12:11+03"
    instances:
      - name: instance1
        replicas: 1
        dataVolumeClaimSpec:
          accessModes:
            - ReadWriteOnce
          resources:
            requests:
              storage: 1Gi
    backups:
      pgbackrest:
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

Deploy the new cluster:

```bash
kubectl apply -f deploy/cr.yaml -n percona-db-2
```

The new cluster will be restored to the specified point in time and then promoted. You can start accessing it from that specific timestamp.

## Related topics

* [Point-in-time recovery](backups-pitr.md)
* [In-place restore with point-in-time recovery](backups-pitr-inplace.md)
* [In-place restore with point-in-time recovery from a PVC snapshot](backups-pvc-usage.md#in-place-restore-with-point-in-time-recovery)
* [Create a new cluster from a PVC snapshot](backups-pvc-usage.md#create-a-new-cluster-from-a-pvc-snapshot)
* [Clone from an existing cluster](backups-clone.md#clone-from-an-existing-cluster)
