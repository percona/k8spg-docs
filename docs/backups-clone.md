# Restore the backup to a new cluster (cluster clone)

Apart from [restoring the data on the same database cluster](backups-restore-inplace.md), you can restore a backup to a new cluster and run it alongside the existing one.

This is useful for:

* Cloning a cluster to a new namespace or Kubernetes environment
* Creating a copy for development, testing, or reporting
* Restoring from a cloud storage when the source cluster no longer exists
* Bootstrapping a new cluster from existing data volumes

You can make a full restore or restore the database to a specific point in time. For each restore scenario, you must define the Custom Resource for a **new** cluster with these configuration options:

* `dataSource` section - where to take the data from
* `backups` section. The new cluster needs its own backup configuration.

## Understand the `dataSource` options

The `dataSource` section in the Custom Resource includes three subsections: `dataSource.postgresCluster`, `dataSource.pgbackrest`, and `dataSource.volumes`. Use one of them to tell the Operator where to take the data from when the new cluster starts.

!!! note

    You cannot use both `dataSource.postgresCluster` and `dataSource.pgbackrest` at the same time. If both are present in the Custom Resource, the `dataSource.postgresCluster` option will take precedence and the Operator will use it to restore the data.

### `dataSource.postgresCluster` 

Configure this subsection **to clone an existing cluster** in the same Kubernetes cluster. The source can be in the same namespace or a different one. The key options are:

* `dataSource.postgresCluster.clusterName` is the name of the cluster you restore from. This is the source cluster. The option value corresponds to the `metadata.name` of the source cluster Custom Resource.

* `dataSource.postgresCluster.clusterNamespace` is the namespace where the source cluster is deployed. Use it if namespaces of source and new clusters differ.

* `dataSource.postgresCluster.repoName` is the name of the `pgBackRest` repository on the source cluster where the backup you restore from is located. It must exist on the source.

* `dataSource.postgresCluster.options` are additional `pgBackRest` options that you pass for the restore. For example, you configure them for point-in-time recovery.

Read more about all available options in the [Custom Resource reference](operator.md#datasource-subsection)

| Pros | Cons |
| --- | --- |
| Simplest path when the source cluster still exists | Source cluster must be available |
| Creates an independent copy; the source stays intact | Not for a deleted cluster or a different Kubernetes cluster |
| Supports point-in-time recovery | Needs restore time and storage for a full data copy |
| Works in the same or a different namespace. | Requires the Operator in the [cluster-wide mode](cluster-wide.md#install-the-operator-cluster-wide) for cross-namespace restores | |

### `dataSource.pgbackrest`

Configure this subsection **to restore from a backup repository stored in cloud storage**. Use it when the source cluster no longer exists, or when you restore into a different Kubernetes cluster that can reach the same object storage.

The **new** cluster's Custom Resource structure closely matches the source cluster's `backups.pgbackrest` section, with these main points:

* Define the backup source using a single `repo` object (not an array as in `backups.pgbackrest`).
* Specify `stanza` (usually `db`), required to identify the backup.
* Reference the same Secret for cloud credentials in both the restore and backup configuration.

Key options are:

* `dataSource.pgbackrest.stanza` - the name of `pgBackRest` stanza - a unique identifier for a source PostgreSQL cluster's backup configuration

* `dataSource.pgbackrest.configuration.secret.name` - the name of the Secret object with the credentials to the cloud storage. It must be the same in both source and new clusters because the restore Pod requires the same credentials as the original backup Pod.

* `dataSource.pgbackrest.global` is the location of a backup.

* `dataSource.pgbackrest.repo` is the name of the `pgBackRest` repository. It is the same on both source and new clusters.

For all options, see the [Custom Resource reference](operator.md#datasourcepgbackrestconfigurationsecretname).

| Pros | Cons |
| --- | --- |
| Works without a live source cluster | You must match the repository path, stanza, Secret, and storage settings exactly |
| Fits disaster recovery and multi-cluster restores | Cloud credentials must exist in the target namespace |
| Source cluster may already be deleted | Restore time and network or storage cost |

### `dataSource.volumes`

Configure this subsection **to bootstrap a new cluster from existing PersistentVolumeClaims** instead of restoring from a `pgBackRest` backup. The Operator attaches the volumes you name and starts PostgreSQL on that data.

Use this when you need a fast cutover on the same storage in the **same namespace**. You must stop the source cluster first. Two clusters cannot use the same volumes at the same time. If source and target are in different namespaces, rebind the PersistentVolumes instead — see [Choose your approach](#choose-your-approach). For the same-namespace procedure, see [Restore using data volumes](#restore-using-data-volumes).

Key options are:

* `dataSource.volumes.pgDataVolume` – the PVC (and optional directory) with the PostgreSQL data directory
* `dataSource.volumes.pgWALVolume` – optional; use it if the source cluster stored WAL on a separate volume
* `dataSource.volumes.pgBackRestVolume` – the PVC (and optional directory) for the local pgBackRest repository

For all options, see the [Custom Resource reference](operator.md#datasourcevolumespgdatavolumepvcname).

| Pros | Cons |
| --- | --- |
| Fastest option for large datasets — no full restore copy | Downtime from stopping the source until the new cluster accepts writes |
| No object storage required for bootstrap | Ownership of the volumes moves to the new cluster |
| Avoids double storage during a backup-based restore | Weak rollback once the new cluster writes (take a backup first) |
| Good for same-namespace cutovers when PVCs can be retained | Same PostgreSQL major version; same Kubernetes cluster and compatible storage |

## Clone from an existing cluster

### Make a full data clone

To create an independent copy of your cluster, add the `dataSource.postgresCluster` section to the Custom Resource of the *new* cluster.

Key fields:

* `clusterName` – name of the source cluster
* `clusterNamespace` – namespace of the source cluster (required when cloning to a different namespace; requires the Operator in [cluster-wide mode](cluster-wide.md#install-the-operator-cluster-wide))
* `repoName` – name of the pgBackRest repository in the source cluster containing the backup to use for the restore

You also need to configure the storage and backup settings for the new cluster:

* In the `instances` section, define the `dataVolumeClaimSpec` for your new cluster, which sets up the PVC. This determines the storage resources (size, access mode, etc.) allocated for your cloned database data.
* In the `backups.pgbackrest.repos` section, set up a backup repository for the new cluster. The repo name must match the one used in `repoName` above. Also configure the backup storage. This ensures the new cluster both restores data and is able to perform its own backups independently.

The following example creates a cluster named `cluster2` as a clone of `cluster1` in the `percona-db-1` namespace:

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

This configuration allows your new cluster to both restore data from the source backup and operate as a fully functioning, independently backed-up PostgreSQL cluster. 

### Make a clone with point-in-time recovery

To restore from a backup up to a specific point in time, you need the following:

* A backup that finished before your target time. You cannot restore to the time where there was no backup
* All relevant WAL files must be successfully archived
* Use the `--type=time` and `--target` options in the `options` subsection of the `deploy/restore.yaml` configuration file.

Use the same settings as for [a full data clone](#make-a-full-data-clone). Also, add `pgBackRest` options for point-in-time recovery to `dataSource.postgresCluster.options`. These options are:

* `--type=time`: Instructs pgBackRest to initiate a point-in-time recovery.
* `--target`: The timestamp up to which to restore the data. To get the timestamp, run this command on the **source cluster**: `kubectl get pg-backup <backup_name> -n <namespace> -o jsonpath='{.status.latestRestorableTime}'`
* `--set` (optional): Allows you to specify a particular backup as the starting point for point-in-time recovery. For more information how to do it, refer to the [Specify a base backup for point-in-time restore](backups-restore-inplace.md#specify-a-base-backup-for-point-in-time-restore) section.

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

The new cluster will be restored to the specified point in time and then promoted. You can start accessing it from that specific timestamp.

### Restore specific databases

You might need to restore only specific databases on a new cluster. For example, for performance reasons or due to storage limits. 

!!! important

    Note that **only the specified databases** will be restored and available on a new cluster. All other databases from a backup will **not** be accessible. This means that if you have `db1`, `db2` and `db3` in a backup and you specify only `db1`, you will have access only to this `db1`. `db2` and `db3` will not be restored. 

    Also check [pgBackRest limitations for restoring specific databases](https://pgbackrest.org/user-guide.html#restore/option-db-include)

To restore only specific databases to a new cluster, start with [the basic cluster clone configuration](#make-a-full-data-clone), and add the `--db-include` flag under `options` to list the databases you want to restore. For example, to restore just the `app1` database, use:

```yaml
spec:
  dataSource:
    postgresCluster:
      clusterName: cluster1
      clusterNamespace: percona-db-1
      repoName: repo1
      options:
      - --db-include=app1
```

List additional databases with separate `--db-include` flags as needed.

## Clone from cloud storage (S3, GCS, Azure Blob)

You can create a new cluster when the source cluster no longer exists but backups remain in a cloud storage (AWS S3, Google Cloud Storage, or Azure Blob Storage). This is useful for disaster recovery, for keeping data compressed on cheaper storage and restoring it when needed, or for creating a standalone copy from archived backups.

### Before you start

You need the backup configuration from the original cluster: the path where backups were stored, the Secret with cloud credentials, and the storage settings (bucket, endpoint, region). 

If the source cluster is still running and you plan to delete it, take a full backup first for best results, then delete the cluster once the backup completes.

### Clone from S3 storage

1. Configure the `dataSource.pgbackrest` subsection in the new cluster Custom Resource. 

    **Configure these fields correctly:**

    | Section | Field | Purpose |
    | ------- | ----- | ------- |
    | `dataSource.pgbackrest` | `stanza` | pgBackRest stanza name (usually `db`). Required for cloud restore. |
    | `dataSource.pgbackrest` | `configuration.secret.name` | Secret with cloud credentials. Must match the Secret used by the source cluster. |
    | `dataSource.pgbackrest` | `global.repo1-path` | Path where the **source** cluster stored its backups. Use the same path as in the original cluster's `backups.pgbackrest.global`. |
    | `dataSource.pgbackrest` | `repo` | Storage config (bucket, endpoint, region) matching the source. Single object, not an array. |
    | `backups.pgbackrest` | `global.repo1-path` | Path for the **new** cluster's backups. Use a different path (e.g., with the new cluster name) so the clone backs up to its own location and does not overwrite the original backups. |

    The following example creates `cluster2` from backups that `cluster1` stored in the S3 storage. The source cluster may already be deleted.

    ```yaml
    apiVersion: pgv2.percona.com/v2
    kind: PerconaPGCluster
    metadata:
      name: cluster2
    spec:
      crVersion: {{ release }}
      dataSource:
        pgbackrest:
          stanza: db
          configuration:
            - secret:
                name: cluster1-pgbackrest-secrets
          global:
            repo1-path: /pgbackrest/postgres-operator/cluster1/repo1
          repo:
            name: repo1
            s3:
              bucket: my-bucket
              endpoint: s3.ca-central-1.amazonaws.com
              region: ca-central-1
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
          configuration:
            - secret:
                name: cluster1-pgbackrest-secrets
          global:
            repo1-path: /pgbackrest/postgres-operator/cluster2/repo1
          repos:
          - name: repo1
            s3:
              bucket: my-bucket
              endpoint: s3.ca-central-1.amazonaws.com
              region: ca-central-1
    ```

2. Deploy the cluster:

    ```bash
    kubectl apply -f deploy/cr.yaml -n percona-db-2
    ```

3. Check that the cluster is ready:

    ```bash
    kubectl describe perconapgcluster cluster2 -n percona-db-2
    ```

When the number of ready instances matches the expected instances, the cloned cluster is up and running.

### Clone from cloud, backup to local storage

You can restore from cloud storage but configure the new cluster to use a local Persistent Volume for its own backups. Replace the `backups.pgbackrest` section with a volume-based repo:

```yaml
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

The `dataSource.pgbackrest` section stays the same; only the new cluster's backup destination changes.

### GCS and Azure Blob Storage

For Google Cloud Storage or Azure Blob Storage, use the same structure but replace the `repo.s3` block with `repo.gcs` or `repo.azure` and the matching configuration. See [Google Cloud Storage](backups-storage-gcs.md) and [Microsoft Azure Blob Storage](backups-storage-azure.md) for examples.

## Restore using data volumes

Instead of restoring from a `pgBackRest` backup, you can start a **new** cluster on the PersistentVolumeClaims that already hold your PostgreSQL data. The Operator takes ownership of those volumes and starts PostgreSQL on the existing data directory — with no backup copy over the network.

Use this when:

* Your dataset is large and a full restore would take too long
* You can accept downtime while the source cluster is stopped
* The source and target run in the same Kubernetes cluster, and you can set the PersistentVolume reclaim policy to `Retain` before you delete the source cluster.

!!! important

    This operation moves volume ownership to the new cluster. After the new cluster accepts writes, you cannot roll back by simply restarting the old cluster on the same disks. Take a backup first if you may need a fallback.

### Choose your approach

A PersistentVolumeClaim (PVC) is a namespaced object. How you hand the disks to the target depends on whether source and target share a namespace:

| Source and target | Approach |
| --- | --- |
| Same namespace | Keep the existing PVCs and point `dataSource.volumes` at their names. Follow the procedure in this section. |
| Different namespaces | You cannot reference a PVC from another namespace. Instead, rebind the underlying PersistentVolumes. For the full steps, see [Migrate from Crunchy to Percona Operator for PostgreSQL by reusing persistent volumes](migrate-from-crunchy-data-volumes.md). The same PV rebind pattern applies when you move a Percona cluster between namespaces. |

### Prepare the source cluster

Export the namespace where your source cluster runs:

```bash
export NAMESPACE=<namespace>
```

Complete these steps on the **source** cluster before you create the target.
{.power-number}

1. Stop application writes to the source cluster. Downtime starts here.

2. Identify the primary Pod, its data PVC, and (if you use a local `pgBackRest` repo) the repository PVC:

    ```bash
    PRIMARY=$(kubectl get pod -n $NAMESPACE \
      --selector postgres-operator.crunchydata.com/cluster=cluster1,postgres-operator.crunchydata.com/role=primary \
      -o jsonpath='{.items[0].metadata.name}')

    PGDATA_PVC=$(kubectl get pod -n $NAMESPACE "$PRIMARY" \
      -o jsonpath='{.spec.volumes[?(@.name=="postgres-data")].persistentVolumeClaim.claimName}')

    echo "Primary pod: $PRIMARY"
    echo "Data PVC:    $PGDATA_PVC"
    kubectl get pvc -n $NAMESPACE | grep -E "$PGDATA_PVC |cluster1-repo"
    ```

    ??? example "Sample output"

        ```{.text .no-copy}
        Primary pod: cluster1-instance1-abcd-0
        Data PVC:    cluster1-instance1-abcd-pgdata
        NAME                             STATUS   VOLUME   CAPACITY   ACCESS MODES   STORAGECLASS   AGE
        cluster1-instance1-abcd-pgdata   Bound    ...      10Gi       RWO            standard-rwo   3d
        cluster1-repo1                   Bound    ...      10Gi       RWO            standard-rwo   3d
        ```

    If the source uses a separate WAL volume (`walVolumeClaimSpec`), also note the `*-pgwal` PVC bound to the primary Pod.

3. Confirm the data directory name on the volume. It is usually `pg<major>` (for example `pg18` for PostgreSQL 18):

    ```bash
    kubectl exec -n $NAMESPACE "$PRIMARY" -c database -- \
      ls -1 /pgdata
    ```

    ??? example "Sample output"

        ```{.text .no-copy}
        pg18
        pg18_wal
        pgbackrest
        ```

    You will use that directory name later in `dataSource.volumes.pgDataVolume.directory`.

4. Identify the PersistentVolume your cluster's PVC is bound to and update the PersistentVolume reclaim policy to `Retain` for every volume you plan to reuse (data, and optionally WAL and the local pgBackRest repo). Dynamically provisioned volumes often default to `Delete`, which destroys the disk when its PVC is removed.

    ```bash
    PGDATA_PV=$(kubectl get pvc -n $NAMESPACE "$PGDATA_PVC" \
      -o jsonpath='{.spec.volumeName}')

    kubectl patch pv "$PGDATA_PV" \
      -p '{"spec":{"persistentVolumeReclaimPolicy":"Retain"}}'
    ```

    ??? example "Sample output"

        ```{.text .no-copy}
        persistentvolume/pvc-e57276f9-359d-4ca6-81d8-5ed2114ec50b patched
        ```

    Repeat for the repository PVC (and WAL PVC, if you use one):

    ```bash
    REPO_PVC=cluster1-repo1
    REPO_PV=$(kubectl get pvc -n $NAMESPACE "$REPO_PVC" \
      -o jsonpath='{.spec.volumeName}')

    kubectl patch pv "$REPO_PV" \
      -p '{"spec":{"persistentVolumeReclaimPolicy":"Retain"}}'
    ```

    Confirm the policy:

    ```bash
    kubectl get pv "$PGDATA_PV" "$REPO_PV" \
      -o custom-columns=NAME:.metadata.name,RECLAIM:.spec.persistentVolumeReclaimPolicy
    ```

    ??? example "Sample output"

        ```{.text .no-copy}
        NAME                                       RECLAIM
        pvc-e57276f9-359d-4ca6-81d8-5ed2114ec50b   Retain
        pvc-0f26234a-7a5d-4c38-bd59-ec22e731cb07   Retain
        ```

5. (Recommended) Take a full backup of the source cluster so you can recover with [`dataSource.pgbackrest`](#clone-from-cloud-storage-s3-gcs-azure-blob) or an [in-place restore](backups-restore-inplace.md) if the volume cutover fails.

6. Delete the source cluster Custom Resource:

    ```bash
    kubectl delete perconapgcluster <cluster-name> -n $NAMESPACE
    ```

7. Confirm the data (and repo) PVCs are still present:

    ```bash
    kubectl get pvc -n $NAMESPACE
    ```

### Create the new cluster from the volumes

Create a new `PerconaPGCluster` that points `dataSource.volumes` at the retained PVCs.
{.power-number}

1. Edit `deploy/cr.yaml` for the **new** cluster. Set:

    * A new cluster name (for example `cluster2`), or reuse the old name if you prefer
    * Set the same `postgresVersion` (and matching images) as the source
    * Set the `instances[].replicas ` to `1` for the first start
    * Set the `dataVolumeClaimSpec` storage size and access mode at least as large as the existing data PVC
    * Set the `dataSource.volumes` with the PVC names and directories you collected

    Example configuration:

    ```yaml
    apiVersion: pgv2.percona.com/v2
    kind: PerconaPGCluster
    metadata:
      name: cluster2
    spec:
      crVersion: {{ release }}
      postgresVersion: 18
      dataSource:
        volumes:
          pgDataVolume:
            pvcName: cluster1-instance1-abcd-pgdata
            directory: pg18
          pgBackRestVolume:
            pvcName: cluster1-repo1
          # Include only if the source used a separate WAL volume:
          # pgWALVolume:
          #   pvcName: cluster1-instance1-abcd-pgwal
      instances:
        - name: instance1
          replicas: 1
          dataVolumeClaimSpec:
            accessModes:
              - ReadWriteOnce
            resources:
              requests:
                storage: 10Gi
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
                    storage: 10Gi
      proxy:
        pgBouncer:
          replicas: 1
          image: docker.io/percona/percona-pgbouncer:{{pgbouncerrecommended}}
    ```

    !!! note

        Set `directory` under `pgDataVolume` to the directory you listed under `/pgdata` on the source (for example `pg17`). Add `pgWALVolume` only when the source stored WAL on a separate PVC. If you reuse a local pgBackRest repo PVC, set `pgBackRestVolume.pvcName` to that claim (for example `cluster1-repo1`).

2. Deploy the new cluster:

    ```bash
    kubectl apply -f deploy/cr.yaml -n $NAMESPACE
    ```

3. Wait until the cluster is ready:

    ```bash
    kubectl wait perconapgcluster/cluster2 \
      -n $NAMESPACE \
      --for=jsonpath='{.status.state}'=ready \
      --timeout=600s
    ```

4. Verify that PostgreSQL is writable on the primary:

    ```bash
    PRIMARY=$(kubectl get pod -n $NAMESPACE \
      --selector postgres-operator.crunchydata.com/cluster=cluster2,postgres-operator.crunchydata.com/role=primary \
      -o jsonpath='{.items[0].metadata.name}')

    kubectl exec -n $NAMESPACE "$PRIMARY" -c database -- \
      psql -t -c "SELECT pg_is_in_recovery();"
    ```

    Expect `f` for a primary that can accept writes. Spot-check application data as needed.

5. Remove `spec.dataSource.volumes` from the manifest and re-apply it. The volumes already belong to the new cluster; the bootstrap configuration is no longer required.

6. If you need high availability, increase `instances[].replicas` after the primary is healthy so the Operator creates fresh PVCs for the additional replicas.
