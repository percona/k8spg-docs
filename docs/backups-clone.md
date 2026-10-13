# Restore the backup to a new cluster (cluster clone)

Apart from [restoring the data on the same database cluster](backups-restore-inplace.md), you can restore a backup to a new cluster and run it alongside the existing one.

This is useful for:

* Cloning a cluster to a new namespace or Kubernetes environment
* Creating a copy for development, testing, or reporting
* Restoring from a cloud storage when the source cluster no longer exists
* Bootstrapping a new cluster from existing data volumes

Use this page to make a full restore to a new cluster. For a restore to a specific moment, see [Cluster clone with point-in-time recovery](backups-pitr-cluster-clone.md).

For each restore scenario, you must define the Custom Resource for a **new** cluster with these configuration options:

* `dataSource` section - where to take the data from
* `backups` section. The new cluster needs its own backup configuration.

## Choose a `dataSource` option

The `dataSource` section in the Custom Resource includes three subsections: `dataSource.postgresCluster`, `dataSource.pgbackrest`, and `dataSource.volumes`. Use one of them to tell the Operator where to take the data from when the new cluster starts. To compare the options, see [If you clone: choose a data source](backups-restore.md#if-you-clone-choose-a-data-source).

If you already know which option you need, go to its procedure:

* `dataSource.postgresCluster` – [Clone from an existing cluster](#clone-from-an-existing-cluster)
* `dataSource.pgbackrest` – [Clone from cloud storage](#clone-from-cloud-storage-s3-gcs-azure-blob)
* `dataSource.volumes` – [Restore using data volumes](#restore-using-data-volumes)

!!! note

    You cannot use both `dataSource.postgresCluster` and `dataSource.pgbackrest` at the same time. If both are present in the Custom Resource, the `dataSource.postgresCluster` option will take precedence and the Operator will use it to restore the data.

## Clone from an existing cluster

To clone a cluster, configure the `dataSource.postgresCluster` subsection in the Custom Resource of the **new** cluster. The source can be in the same namespace or a different one. The key options are:

* `dataSource.postgresCluster.clusterName` is the name of the cluster you restore from. This is the source cluster. The option value corresponds to the `metadata.name` of the source cluster Custom Resource.
* `dataSource.postgresCluster.clusterNamespace` is the namespace where the source cluster is deployed. Use it if namespaces of source and new clusters differ. Cloning to a different namespace requires the Operator in [cluster-wide mode](cluster-wide.md#install-the-operator-cluster-wide).
* `dataSource.postgresCluster.repoName` is the name of the `pgBackRest` repository on the source cluster where the backup you restore from is located. It must exist on the source.
* `dataSource.postgresCluster.options` are additional `pgBackRest` options that you pass for the restore. For example, you configure them for [point-in-time recovery](backups-pitr-cluster-clone.md) or to [restore specific databases](#restore-specific-databases).

Read more about all available options in the [Custom Resource reference](operator.md#datasource-subsection).

### Make a full data clone

To create an independent copy of your cluster, add the `dataSource.postgresCluster` section to the Custom Resource of the *new* cluster.

You also need to configure the storage and backup settings for the new cluster:

* In the `instances` section, define the `dataVolumeClaimSpec` for your new cluster, which sets up the PVC. This determines the storage resources (size, access mode, etc.) allocated for your cloned database data.
* In the `backups.pgbackrest.repos` section, set up a backup repository for the new cluster. The repo name must match the one used in `repoName` above. Also configure the backup storage. This ensures the new cluster both restores data and is able to perform its own backups independently.

Set `postgresVersion` to the PostgreSQL major version of the source cluster.

The following example creates a cluster named `cluster2` as a clone of `cluster1` in the `percona-db-1` namespace:

```yaml
apiVersion: pgv2.percona.com/v2
kind: PerconaPGCluster
metadata:
  name: cluster2
spec:
  crVersion: {{ release }}
  postgresVersion: 18
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

Wait until the cluster is ready:

```bash
kubectl wait perconapgcluster/cluster2 \
  -n percona-db-2 \
  --for=jsonpath='{.status.state}'=ready \
  --timeout=600s
```

??? example "Sample output"

    ```{.text .no-copy}
    perconapgcluster.pgv2.percona.com/cluster2 condition met
    ```

If the command times out and the cluster stays in the `initializing` state, check the restore Job logs. See [Troubleshoot restore failures](debug-restore.md).

This configuration allows your new cluster to both restore data from the source backup and operate as a fully functioning, independently backed-up PostgreSQL cluster.

To restore the clone to a specific moment, see [Cluster clone with point-in-time recovery](backups-pitr-cluster-clone.md).

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

To clone from cloud storage, configure the `dataSource.pgbackrest` subsection in the Custom Resource of the **new** cluster. 

Key options are:

* `dataSource.pgbackrest.stanza` - the name of `pgBackRest` stanza - a unique identifier for a source PostgreSQL cluster's backup configuration
* `dataSource.pgbackrest.configuration.secret.name` - the name of the Secret object with the credentials to the cloud storage. It must be the same in both source and new clusters because the restore Pod requires the same credentials as the original backup Pod.
* `dataSource.pgbackrest.global` is the location of a backup.
* `dataSource.pgbackrest.repo` is the name of the `pgBackRest` repository. It is the same on both source and new clusters.

For all options, see the [Get the backup settings from the source cluster](#get-the-backup-settings-from-the-source-cluster).

Don't combine `dataSource.pgbackrest` with `dataSource.postgresCluster`. If both are set in the same Custom Resource, `dataSource.postgresCluster` takes precedence and the Operator ignores the `dataSource.pgbackrest` configuration.

### Before you start

You need the backup configuration from the original cluster: the path where backups were stored, the Secret with cloud credentials, and the storage settings (bucket, endpoint, region). 

If the source cluster is still running and you plan to delete it, take a full backup first for best results, then delete the cluster once the backup completes.

### Get the backup settings from the source cluster

The Operator doesn't check the `dataSource.pgbackrest` values before it starts the restore. If the stanza, path, or Secret doesn't match the source, the restore Job fails and the new cluster stays in the `initializing` state. To avoid this, read the values from the running source cluster. Do this before you delete the source cluster, and save the output.

Export the namespace where your **source** cluster runs:

```bash
export NAMESPACE=<namespace>
```

Run these commands against the **source** cluster. The examples use `cluster1`:
{.power-number}

1. Get the name of the Secret with the cloud storage credentials. Use it in `dataSource.pgbackrest.configuration.secret.name`:

    ```bash
    kubectl get pg cluster1 -n $NAMESPACE \
      -o jsonpath='{.spec.backups.pgbackrest.configuration[*].secret.name}'
    ```

    ??? example "Sample output"

        ```{.text .no-copy}
        cluster1-pgbackrest-secrets
        ```

    The `configuration` field is a list. If the command returns several names, use the Secret that holds the credentials file for your cloud storage.

2. Check that the Secret holds the credentials for the repository you restore from. List the keys in the Secret:

    ```bash
    kubectl describe secret cluster1-pgbackrest-secrets -n $NAMESPACE
    ```

    ??? example "Sample output"

        ```{.text .no-copy}
        ...
        Data
        ====
        s3.conf:  104 bytes
        ```

    Decode the credentials file. For S3, the key is `s3.conf`. The output contains your access keys, so don't share it:

    ```bash
    kubectl get secret cluster1-pgbackrest-secrets -n $NAMESPACE \
      -o jsonpath='{.data.s3\.conf}' | base64 --decode
    ```

    ??? example "Sample output"

        ```{.text .no-copy}
        [global]
        repo2-s3-key=<your-access-key>
        repo2-s3-key-secret=<your-secret-key>
        ```

    The `repo<N>` prefix of the options must match the repository name you set in `dataSource.pgbackrest.repo.name`. In this example, it is `repo2`. The Secret stores only credentials. The bucket, endpoint, and region come from the next step.

3. Get the repository settings that the source cluster uses. The Operator stores the generated pgBackRest configuration in the `<cluster-name>-pgbackrest-config` ConfigMap:

    ```bash
    kubectl get configmap cluster1-pgbackrest-config -n $NAMESPACE \
      -o jsonpath='{.data.pgbackrest_instance\.conf}'
    ```

    ??? example "Sample output"

        ```{.text .no-copy hl_lines="5 6 7 8 9 11"}
        [global]
        archive-async = y
        log-path = /pgdata/pgbackrest/log
        ...
        repo2-path = /pgbackrest/postgres-operator/cluster1/repo2
        repo2-s3-bucket = my-bucket
        repo2-s3-endpoint = https://s3.amazonaws.com
        repo2-s3-region = us-east-1
        repo2-type = s3
        spool-path = /pgdata/pgbackrest-spool
        [db]
        pg1-path = /pgdata/pg18
        ...
        ```

    Map the output to the new cluster's Custom Resource as follows:

    * `repo<N>-path` → `dataSource.pgbackrest.global.repo<N>-path`. Keep the same repository number as in the source.
    * `repo<N>-s3-bucket`, `repo<N>-s3-endpoint`, `repo<N>-s3-region` → `dataSource.pgbackrest.repo.s3`
    * `repo<N>` → `dataSource.pgbackrest.repo.name`
    * Section name in square brackets after `[global]` → `dataSource.pgbackrest.stanza`

    The ConfigMap shows the effective path. The `spec.backups.pgbackrest.global` field in the source Custom Resource shows only paths you set explicitly. If you didn't set one, the Operator uses `/pgbackrest/<repo-name>`.

4. Confirm the stanza name and that the repository has backups. Run `pgbackrest info` in the `database` container of the primary Pod. Replace `2` with the number of your repository:

    ```bash
    PRIMARY=$(kubectl get pod -n $NAMESPACE \
      --selector postgres-operator.crunchydata.com/cluster=cluster1,postgres-operator.crunchydata.com/role=primary \
      -o jsonpath='{.items[0].metadata.name}')

    kubectl exec -n $NAMESPACE "$PRIMARY" -c database -- \
      pgbackrest info --repo=2
    ```

    ??? example "Sample output"

        ```{.text .no-copy}
        stanza: db
            status: ok
            cipher: none

            db (current)
                wal archive min/max (18): 000000010000000000000004/00000001000000000000000F

                full backup: 20261012-160223F
                    timestamp start/stop: 2026-10-12 16:02:23+00 / 2026-10-12 16:04:56+00
                    wal start/stop: 00000001000000000000000D / 00000001000000000000000E
                    database size: 39.5MB, database backup size: 39.5MB
                    repo2: backup set size: 6.7MB, backup size: 6.7MB
        ```

    The Operator always creates the stanza named `db`. A different name appears only if the backups were not made by the Operator.

### Clone from S3 storage

1. Configure the `dataSource.pgbackrest` subsection in the new cluster Custom Resource. If you haven't gathered these values yet, see [Get the backup settings from the source cluster](#get-the-backup-settings-from-the-source-cluster).

    **Configure these fields correctly:**

    | Section | Field | Purpose |
    | ------- | ----- | ------- |
    | `dataSource.pgbackrest` | `stanza` | pgBackRest stanza name (usually `db`). Required for cloud restore. |
    | `dataSource.pgbackrest` | `configuration.secret.name` | Secret with cloud credentials. Must match the Secret used by the source cluster. |
    | `dataSource.pgbackrest` | `global.repo<N>-path` | Path where the **source** cluster stored its backups. Use the same path as in the original cluster's `backups.pgbackrest.global`. |
    | `dataSource.pgbackrest` | `repo` | Storage config (bucket, endpoint, region) matching the source. Single object, not an array. |
    | `backups.pgbackrest` | `global.repo<N>-path` | Path for the **new** cluster's backups. Use a different path (e.g., with the new cluster name) so the clone backs up to its own location and does not overwrite the original backups. |

    Set `postgresVersion` to the PostgreSQL major version of the source cluster.

    The following example creates `cluster2` from backups that `cluster1` stored in the S3 storage. The source cluster may already be deleted. It uses the `repo2` values from [Get the backup settings from the source cluster](#get-the-backup-settings-from-the-source-cluster).

    ```yaml
    apiVersion: pgv2.percona.com/v2
    kind: PerconaPGCluster
    metadata:
      name: cluster2
    spec:
      crVersion: {{ release }}
      postgresVersion: 18
      dataSource:
        pgbackrest:
          stanza: db
          configuration:
            - secret:
                name: cluster1-pgbackrest-secrets
          global:
            repo2-path: /pgbackrest/postgres-operator/cluster1/repo2
          repo:
            name: repo2
            s3:
              bucket: my-bucket
              endpoint: https://s3.amazonaws.com
              region: us-east-1
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
            repo2-path: /pgbackrest/postgres-operator/cluster2/repo2
          repos:
          - name: repo2
            s3:
              bucket: my-bucket
              endpoint: https://s3.amazonaws.com
              region: us-east-1
    ```

2. Deploy the cluster:

    ```bash
    kubectl apply -f deploy/cr.yaml -n <target-namespace>
    ```

3. Wait until the cluster is ready:

    ```bash
    kubectl wait perconapgcluster/cluster2 \
      -n <target-namespace> \
      --for=jsonpath='{.status.state}'=ready \
      --timeout=600s
    ```

    ??? example "Sample output"

        ```{.text .no-copy}
        perconapgcluster.pgv2.percona.com/cluster2 condition met
        ```

If the command times out and the cluster stays in the `initializing` state, check the restore Job logs. See [Troubleshoot restore failures](debug-restore.md). To fix a cluster clone, correct the `dataSource.pgbackrest` values in the new cluster's Custom Resource and apply it again. The Operator starts a new restore Job.

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

For Google Cloud Storage or Azure Blob Storage, use the same structure but replace the `repo.s3` block with `repo.gcs` or `repo.azure` and the matching configuration. See [Google Cloud Storage](backups-storage-gcs.md) and [Microsoft Azure Blob Storage](backups-storage-azure.md) for examples. To get the values from the source cluster, follow the steps in [Get the backup settings from the source cluster](#get-the-backup-settings-from-the-source-cluster). The credentials file name in the Secret and the `repo<N>-*` options in the ConfigMap differ for each storage type. If the cluster doesn't become ready, troubleshoot it the same way as for [S3 storage](#clone-from-s3-storage).

## Restore using data volumes

Instead of restoring from a `pgBackRest` backup, you can start a **new** cluster on the PersistentVolumeClaims that already hold your PostgreSQL data. The Operator takes ownership of those volumes and starts PostgreSQL on the existing data directory — with no backup copy over the network.

Use this when:

* Your dataset is large and a full restore would take too long
* You can accept downtime while the source cluster is stopped
* The source and target run in the same Kubernetes cluster, and you can set the PersistentVolume reclaim policy to `Retain` before you delete the source cluster.

!!! important

    This operation moves volume ownership to the new cluster. After the new cluster accepts writes, you cannot roll back by simply restarting the old cluster on the same disks. Take a backup first if you may need a fallback.

Choose the right procedure based on whether your clusters are in the same or different namespaces. Read the [Choose your approach](#choose-your-approach) subsection first to understand which steps to follow.


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
        latest_commit_timestamp.txt
        lost+found
        pg18
        pg18_wal
        pgbackrest
        pgbackrest-spool
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

Key options are:

* `dataSource.volumes.pgDataVolume` – the PVC (and optional directory) with the PostgreSQL data directory
* `dataSource.volumes.pgWALVolume` – optional; use it if the source cluster stored WAL on a separate volume
* `dataSource.volumes.pgBackRestVolume` – the PVC (and optional directory) for the local pgBackRest repository

For all options, see the [Custom Resource reference](operator.md#datasourcevolumespgdatavolumepvcname).
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

        Set `directory` under `pgDataVolume` to the directory you listed under `/pgdata` on the source (for example `pg18`). Add `pgWALVolume` only when the source stored WAL on a separate PVC. If you reuse a local pgBackRest repo PVC, set `pgBackRestVolume.pvcName` to that claim (for example `cluster1-repo1`).

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
