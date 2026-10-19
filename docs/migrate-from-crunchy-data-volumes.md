# Migrate from Crunchy to Percona Operator for PostgreSQL by reusing persistent volumes

This guide shows how to migrate to Percona Operator for PostgreSQL using the persistent volumes of the **primary** PostgreSQL instance of your Crunchy `PostgresCluster`: the data volume and, if the cluster has them, the WAL and tablespace volumes.

In this approach, Percona `PerconaPGCluster` (`cluster1`) starts on the existing `PGDATA` data directory without running a backup-restore cycle over the network.

| Benefits | Trade-offs |
|----------|------------|
| - Avoids large data copies through object storage when the persistent volume already contains the dataset.<br>- Provides a direct migration path when it is important to keep the exact data directory intact.<br>- Allows migrating even if the source cluster is deleted but the PV is preserved | - **Downtime** occurs from the moment you stop writes on Crunchy until the Percona cluster is brought up.<br>- **Rollback is difficult** once Percona has advanced the database on that volume; take a Crunchy `pgBackRest` backup to object storage before destructive steps if you may need to restore Crunchy.<br>- Requires manual management of PV **reclaim policy**, **StorageClass name**, clearing `claimRef`, and setting a **PVC selector** to ensure the new claim binds only to the intended volume. This usually needs cluster-admin privileges. |

If the backing PV was already deleted with the default **Delete** reclaim policy, use [Migrate from Crunchy using backup and restore](migrate-from-crunchy-backup-restore.md) instead.

--8<-- "crunchy-pgo-version.txt::6"

## Before you migrate

Complete the [Pre-migration compatibility checks](migrate-checklist.md). Physical methods require a matching PostgreSQL major version and CPU architecture.

## Prerequisites

Ensure you have the following:

- A Kubernetes or OpenShift cluster with permissions to patch PersistentVolumes, delete `PostgresCluster` resources, and deploy the Percona Operator.
- `kubectl` or `oc`.
- Storage where you can set the PV reclaim policy to `Retain`, change the PV StorageClass name, and clear `claimRef` (cluster-admin privileges are often required).
- Object storage for a Crunchy `pgBackRest` backup that you can roll back to.


## Before you start

1. Create or choose namespaces for Crunchy and Percona and export them as the environment variables.
   
    ```bash
    export CRUNCHY_NS=postgres-operator
    export NAMESPACE=pgo
    ```

2. Clone the Operator repository to edit the manifests during the migration setup:

    ```bash
    git clone -b v{{release}} https://github.com/percona/percona-postgresql-operator
    ```

## Deploy Operators

1. Install Crunchy Operator for PostgreSQL into `$CRUNCHY_NS` if it is not already installed. See the [Crunchy quickstart :octicons-link-external-16:](https://access.crunchydata.com/documentation/postgres-operator/5.8/quickstart) for the steps.

2. Install Percona Operator for PostgreSQL into `$NAMESPACE`:

    ```bash
    kubectl apply --server-side \
      -f https://raw.githubusercontent.com/percona/percona-postgresql-operator/v{{release}}/deploy/bundle.yaml \
      -n "${NAMESPACE}"
    ```

3. Wait for the Percona Operator Deployment to become available:

    ```bash
    kubectl wait deployment percona-postgresql-operator \
      -n "${NAMESPACE}" \
      --for=condition=Available \
      --timeout=120s
    ```

    ??? example "Expected output"
        
        ```text
        deployment.apps/percona-postgresql-operator condition met
        ```

## Deploy the Crunchy source cluster 

If you already have a PostgreSQL cluster running in the Crunchy namespace, make sure it is set up so that only one database server (replica) is running. This means changing the configuration so `instances.replicas` is set to `1`.

If you are deploying Crunchy for testing or migration rehearsal, create it with **one** Postgres instance (`replicas: 1` on the primary set) so a single data PVC represents the primary. 

This is the sample `PostgresCluster` Custom Resource configuration:

```yaml title="postgres.yaml"
apiVersion: postgres-operator.crunchydata.com/v1beta1
kind: PostgresCluster
metadata:
  name: crunchy-source
spec:
  postgresVersion: 18
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
```

1. Apply the configuration to create or update the Crunchy PostgreSQL cluster.

2. Wait until the PostgreSQL instance of the cluster is ready:

    ```bash
    kubectl wait postgrescluster.postgres-operator.crunchydata.com/crunchy-source \
      -n "${CRUNCHY_NS}" \
      --for=jsonpath='{.status.instances[?(@.name=="instance1")].readyReplicas}'=1 \
      --timeout=600s
    ```

    ??? example "Expected output"

        ```{.text .no-copy}
        postgrescluster.postgres-operator.crunchydata.com/crunchy-source condition met
        ```

    This command waits on the cluster status, so you can run it right after you apply the manifest. A `kubectl wait pod` command fails with `no matching resources found` if the Pods don't exist yet.


## Identify the primary's persistent volumes

Identify the primary Pod and every persistent volume it uses. The data volume (`postgres-data`) always exists. The cluster also has a separate WAL volume (`postgres-wal`) if it uses `walVolumeClaimSpec`, and a volume for each tablespace if it uses tablespace volumes. The Percona cluster needs all of them.

1. Identify the primary Pod:

    ```bash
    CRUNCHY_PRIMARY=$(kubectl get pod -n "${CRUNCHY_NS}" \
      --selector postgres-operator.crunchydata.com/cluster=crunchy-source,postgres-operator.crunchydata.com/role=master \
      -o jsonpath='{.items[0].metadata.name}')
    ```

2. List the persistent volume claims (PVCs) of the primary Pod:

    ```bash
    kubectl get pod -n "${CRUNCHY_NS}" "${CRUNCHY_PRIMARY}" \
      -o jsonpath='{range .spec.volumes[?(@.persistentVolumeClaim)]}{.name}{"\t"}{.persistentVolumeClaim.claimName}{"\n"}{end}'
    ```

    ??? example "Sample output"

        ```{.text .no-copy}
        postgres-data   crunchy-source-instance1-gpx4-pgdata
        ```

        A cluster with a separate WAL volume also lists `postgres-wal   crunchy-source-instance1-gpx4-pgwal`. A cluster with tablespace volumes also lists one `tablespace-<name>` volume per tablespace, for example `tablespace-ts1   crunchy-source-instance1-gpx4-ts1-tablespace`.

3. Export the data PVC and the persistent volume (PV) it is bound to:

    ```bash
    PVC_NAME=$(kubectl get pod -n "${CRUNCHY_NS}" "${CRUNCHY_PRIMARY}" \
      -o jsonpath='{.spec.volumes[?(@.name=="postgres-data")].persistentVolumeClaim.claimName}')
    PV_NAME=$(kubectl get pvc -n "${CRUNCHY_NS}" "${PVC_NAME}" \
      -o jsonpath='{.spec.volumeName}')
    ```

4. If the previous step listed a `postgres-wal` volume, export the WAL PVC and PV too:

    ```bash
    WAL_PVC_NAME=$(kubectl get pod -n "${CRUNCHY_NS}" "${CRUNCHY_PRIMARY}" \
      -o jsonpath='{.spec.volumes[?(@.name=="postgres-wal")].persistentVolumeClaim.claimName}')
    WAL_PV_NAME=$(kubectl get pvc -n "${CRUNCHY_NS}" "${WAL_PVC_NAME}" \
      -o jsonpath='{.spec.volumeName}')
    ```

    Run the commands for `WAL_PV_NAME` in the following sections only if you have a WAL volume.

5. If the list shows `tablespace-<name>` volumes, export the PVC and PV of each tablespace. The following example exports the tablespace `ts1`:

    ```bash
    TS_NAME=ts1
    TS_PVC_NAME=$(kubectl get pod -n "${CRUNCHY_NS}" "${CRUNCHY_PRIMARY}" \
      -o jsonpath="{.spec.volumes[?(@.name==\"tablespace-${TS_NAME}\")].persistentVolumeClaim.claimName}")
    TS_PV_NAME=$(kubectl get pvc -n "${CRUNCHY_NS}" "${TS_PVC_NAME}" \
      -o jsonpath='{.spec.volumeName}')
    echo "Tablespace ${TS_NAME}: PVC ${TS_PVC_NAME}, PV ${TS_PV_NAME}"
    ```

    Run the commands for `TS_PV_NAME` in the following sections for each tablespace. Crunchy mounts a tablespace volume at `/tablespaces/<name>`, and the tablespace location is `/tablespaces/<name>/data`. The Percona Operator mounts tablespace volumes at the same path.

6. Verify the retrieved data:
    
    ```bash
    echo "Primary pod: ${CRUNCHY_PRIMARY}"
    echo "PVC:         ${PVC_NAME}"
    echo "PV:          ${PV_NAME}"
    echo "WAL PVC:     ${WAL_PVC_NAME}"
    echo "WAL PV:      ${WAL_PV_NAME}"
    ```

    ??? example "Sample output"

        ```{.text .no-copy}
        Primary pod: crunchy-source-instance1-gpx4-0
        PVC:         crunchy-source-instance1-gpx4-pgdata
        PV:          pvc-32f7bc5d-82c7-4d36-9886-56a581124cbd
        WAL PVC:     crunchy-source-instance1-gpx4-pgwal
        WAL PV:      pvc-6513ae01-fda9-412f-92c6-2fac02eb4c0b   
        ```

    If your Crunchy Pod uses a volume name other than `postgres-data`, adjust the JSONPath filter.


## Back up the Crunchy cluster

Take a full `pgBackRest` backup of the Crunchy cluster to object storage before you change anything. This backup is your only way back to Crunchy: after the Percona cluster starts on the data volume, you can't return to the previous state of that volume.

A backup in a volume repository, such as the PVC-backed `repo1` in the previous example, doesn't help here: Kubernetes deletes the repository volume together with the Crunchy cluster. If your cluster has only a volume repository, add an object storage repository first. See [Configure Crunchy PostgreSQL cluster for remote backups](migrate-from-crunchy-backup-restore.md#configure-crunchy-postgresql-cluster-for-remote-backups) for the configuration and [Create the migration backup](migrate-from-crunchy-backup-restore.md#create-the-migration-backup) for the backup commands.

## Stop writes on the Crunchy cluster

Shut down the Crunchy cluster. This stops PostgreSQL cleanly and marks the **start of downtime**. The cluster object, its user Secrets, and its PVCs stay until you delete the cluster.

1. Shut down the cluster:

    ```bash
    kubectl patch postgrescluster.postgres-operator.crunchydata.com crunchy-source \
      -n "${CRUNCHY_NS}" \
      --type=merge \
      -p '{"spec":{"shutdown":true}}'
    ```

2. Wait until the primary Pod is gone:

    ```bash
    kubectl wait --for=delete pod/"${CRUNCHY_PRIMARY}" \
      -n "${CRUNCHY_NS}" \
      --timeout=300s
    ```

## Retain the PV and remove the Crunchy cluster

The default reclaim policy for a dynamically PersistentVolume is `Delete`. This means that as soon as there are no Persistent Volume Claims (PVC) bound to this PV, Kubernetes deletes it and all data is lost. To prevent this, change the PV reclaim policy to `Retain`.

After you delete the Crunchy cluster and clear the PV's claim reference, the PV becomes `Available`. An `Available` PV can be bound by **any** PVC in the Kubernetes cluster that has no selector, uses the same StorageClass, and requests no more than the PV size. This includes the `repo1` PVC of the new Percona cluster and PVCs of unrelated applications in other namespaces. A label and a selector on the Percona PVC don't prevent this. To keep the PV for the Percona cluster, move it to a StorageClass name that no other PVC uses before you free it.

1. Set the PV reclaim policy to `Retain` so the disk survives PVC deletion:

    ```bash
    kubectl patch pv "${PV_NAME}" \
      -p '{"spec":{"persistentVolumeReclaimPolicy":"Retain"}}'
    ```

2. Isolate the PV: change its StorageClass to a name that no StorageClass object and no other PVC uses. Use a name that is unique for this migration:

    ```bash
    export MIGRATION_CLASS=crunchy-migrated-crunchy-source
    kubectl patch pv "${PV_NAME}" \
      -p "{\"spec\":{\"storageClassName\":\"${MIGRATION_CLASS}\"}}"
    ```

    Because no StorageClass object with this name exists, Kubernetes binds a PVC that requests this class directly to the PV and doesn't try to provision a new volume.

3. Label the PV so the Percona PVC selector binds to it. Use a value that is unique for this migration:

    ```bash
    kubectl label pv "${PV_NAME}" percona-pv-migration=crunchy-source-data
    ```

4. If you have a WAL volume or tablespace volumes, repeat the previous three steps for each of them with a different label value. For the WAL volume:

    ```bash
    kubectl patch pv "${WAL_PV_NAME}" \
      -p '{"spec":{"persistentVolumeReclaimPolicy":"Retain"}}'
    kubectl patch pv "${WAL_PV_NAME}" \
      -p "{\"spec\":{\"storageClassName\":\"${MIGRATION_CLASS}\"}}"
    kubectl label pv "${WAL_PV_NAME}" percona-pv-migration=crunchy-source-wal
    ```

    For each tablespace volume, do the same with its own label value:

    ```bash
    kubectl patch pv "${TS_PV_NAME}" \
      -p '{"spec":{"persistentVolumeReclaimPolicy":"Retain"}}'
    kubectl patch pv "${TS_PV_NAME}" \
      -p "{\"spec\":{\"storageClassName\":\"${MIGRATION_CLASS}\"}}"
    kubectl label pv "${TS_PV_NAME}" percona-pv-migration=crunchy-source-${TS_NAME}
    ```

5. Delete the `PostgresCluster`:

    ```bash
    kubectl delete postgrescluster.postgres-operator.crunchydata.com crunchy-source -n "${CRUNCHY_NS}"
    ```

    The Crunchy Operator removes the cluster and the objects it owns, including the PVCs and the user Secrets. The PVs stay because of the `Retain` policy.

    ??? note "If the Crunchy Operator is no longer running"

        Without the Crunchy Operator, the deletion waits for the Operator's finalizer and doesn't complete. In this case, remove the finalizers so Kubernetes deletes the object:

        ```bash
        kubectl patch postgrescluster.postgres-operator.crunchydata.com crunchy-source -n "${CRUNCHY_NS}" \
          --type=json \
          -p='[{"op":"remove","path":"/metadata/finalizers"}]'
        ```

6. Wait until Kubernetes deletes the data PVC (and the WAL PVC, if you have one). Deleting the `PostgresCluster` removes it in the background, so the PVC can still exist for a few seconds after the previous command returns:

    ```bash
    kubectl wait --for=delete pvc/"${PVC_NAME}" \
      -n "${CRUNCHY_NS}" \
      --timeout=120s
    ```

    The command returns without output if the PVC is already deleted. If you have a WAL volume, also wait for the WAL PVC:

    ```bash
    kubectl wait --for=delete pvc/"${WAL_PVC_NAME}" \
      -n "${CRUNCHY_NS}" \
      --timeout=120s
    ```

    Do the same for each tablespace PVC:

    ```bash
    kubectl wait --for=delete pvc/"${TS_PVC_NAME}" \
      -n "${CRUNCHY_NS}" \
      --timeout=120s
    ```

7. After the data PVC is gone, the PV enters the `Released` state. However, it still references the old claim and cannot be claimed by a new PVC. Therefore, you need to clear its `claimRef`:

    ```bash
    kubectl patch pv "${PV_NAME}" --type=json \
      -p='[{"op":"remove","path":"/spec/claimRef"}]'
    ```

    If you have a WAL volume, clear the `claimRef` of the WAL PV too:

    ```bash
    kubectl patch pv "${WAL_PV_NAME}" --type=json \
      -p='[{"op":"remove","path":"/spec/claimRef"}]'
    ```

    Do the same for each tablespace PV:

    ```bash
    kubectl patch pv "${TS_PV_NAME}" --type=json \
      -p='[{"op":"remove","path":"/spec/claimRef"}]'
    ```

8. Wait until the PV status becomes `Available`:

    ```bash
    kubectl wait pv "${PV_NAME}" \
      --for=jsonpath='{.status.phase}'=Available \
      --timeout=60s
    ```

    ??? example "Expected output"
        
        ```text
        persistentvolume/pvc-32f7bc5d-82c7-4d36-9886-56a581124cbd condition met
        ```

    If you have a WAL volume, wait for the WAL PV too:

    ```bash
    kubectl wait pv "${WAL_PV_NAME}" \
      --for=jsonpath='{.status.phase}'=Available \
      --timeout=60s
    ```

    Wait for each tablespace PV too:

    ```bash
    kubectl wait pv "${TS_PV_NAME}" \
      --for=jsonpath='{.status.phase}'=Available \
      --timeout=60s
    ```

9. Uninstall Crunchy Operator when no `PostgresCluster` resources remain. The Crunchy Operator is often installed in its own namespace, not in the namespace of the cluster.

## Create the Percona cluster bound to the retained volume

1. Edit the `deploy/cr.yaml` and specify the following settings:
    
    * Give a name to your cluster  in the `metadata.name` (for example, `cluster1`)
    * Align `spec.postgresVersion` with the old cluster.
    * For the first cutover, set **one** replica on the instance that should attach to the migrated disk
    * In `dataVolumeClaimSpec`, set `storageClassName` to the StorageClass name you gave the PV, and add a `selector` matching the PV label. This ensures the PVC binds only to the migrated PV.
    * If you have a WAL volume, add `walVolumeClaimSpec` with the same StorageClass name and a selector matching the WAL PV label. Without it, PostgreSQL doesn't start: the `postgres-startup` init container fails with `mv: cannot stat '/pgwal/pg18_wal': No such file or directory`.
    * If you have tablespace volumes, add one `tablespaceVolumes` entry per tablespace. Use **the same name** as in the Crunchy cluster, the migration StorageClass name, and a selector matching the tablespace PV label. Without it, the cluster starts and reports `ready`, but queries on tables in the tablespace fail, and so do backups.

    You don't need node affinity rules, even for node-local storage such as local-path: with the migration StorageClass name, Kubernetes binds the PVC to the PV first, and then schedules the Pod to the node or zone where the PV is.
    
    Here is the example configuration:

    ```yaml
    apiVersion: pgv2.percona.com/v2
    kind: PerconaPGCluster
    metadata:
      name: cluster1
    spec:
      crVersion: {{release}}
      postgresVersion: 18
      instances:
        - name: instance1
          replicas: 1
          dataVolumeClaimSpec:
            storageClassName: crunchy-migrated-crunchy-source
            accessModes:
              - ReadWriteOnce
            resources:
              requests:
                storage: 10Gi
            selector:
              matchLabels:
                percona-pv-migration: crunchy-source-data
          # Only if you have a WAL volume:
          # walVolumeClaimSpec:
          #   storageClassName: crunchy-migrated-crunchy-source
          #   accessModes:
          #     - ReadWriteOnce
          #   resources:
          #     requests:
          #       storage: 5Gi
          #   selector:
          #     matchLabels:
          #       percona-pv-migration: crunchy-source-wal
          # Only if you have tablespace volumes, one entry per tablespace:
          # tablespaceVolumes:
          #   - name: ts1
          #     dataVolumeClaimSpec:
          #       storageClassName: crunchy-migrated-crunchy-source
          #       accessModes:
          #         - ReadWriteOnce
          #       resources:
          #         requests:
          #           storage: 5Gi
          #       selector:
          #         matchLabels:
          #           percona-pv-migration: crunchy-source-ts1
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
    ```

    Tune `storage` and other fields to match your environment and the Operator’s usual `deploy/cr.yaml` requirements (users, images, resources). The `requests.storage` value must not be larger than the PV size. Don't set the migration StorageClass name for the `repo1` volume: it needs a regular StorageClass that can provision a new volume.

2. Apply the manifest:

    ```bash
    kubectl apply -f deploy/cr.yaml -n "${NAMESPACE}"
    ```

    The Percona Operator creates a PersistentVolumeClaim (PVC) using the StorageClass name and the selector you specified in the manifest. This PVC binds to the labelled PersistentVolume (PV) that contains the migrated PostgreSQL data. PostgreSQL then starts directly on the existing `PGDATA` directory, so no backup restore, WAL download, or object storage is needed. 

    By default, `pgBackRest` uses a local, PVC-backed repository (`repo1.volume`) for backups and restores, so you do not need to configure S3 credentials or external storage for this migration path (unless you choose to use S3 for backups).

3. Wait for the cluster to have the `Ready` status:

    ```bash
    kubectl wait perconapgcluster/cluster1 \
      -n "${NAMESPACE}" \
      --for=jsonpath='{.status.state}'=ready \
      --timeout=600s
    ```

    ??? example "Expected output"

        ```text
        perconapgcluster.pgv2.percona.com/cluster1 condition met
        ```

    If the command times out, see [PVC stays `Pending`](#pvc-stays-pending).

4. Verify that the data is intact by checking the primary pod state:

    * Identify the primary pod:

       ```bash
       PERCONA_PRIMARY=$(kubectl get pod -n "${NAMESPACE}" \
         --selector postgres-operator.crunchydata.com/cluster=cluster1,postgres-operator.crunchydata.com/role=primary \
         -o jsonpath='{.items[0].metadata.name}')
       ```
    
    * Check the primary pod state:
       
       ```bash
       kubectl -n "${NAMESPACE}" exec "${PERCONA_PRIMARY}" -c database -- \
         psql -t -c "SELECT pg_is_in_recovery();"
       ```

       Expect `f` for a writable primary.

    About 10-20 seconds after the first start, Patroni restarts PostgreSQL once. Clients that connect at this moment can get one or two connection errors.

## Scale out the cluster

You started the cluster with a single replica, so the Operator created a PersistentVolumeClaim (PVC) that bound to your labelled PersistentVolume (PV) containing the migrated data. Once you have confirmed that the primary instance is healthy, scale out your cluster for high availability. 

While the selector and the migration StorageClass name are present in the cluster configuration, the Operator can't create volumes for new replicas: no other PV carries the label, and no StorageClass object with this name exists. Therefore, you need to remove both. Without `storageClassName`, the Operator creates new PVCs for each replica using your default StorageClass. The existing PVC of the primary keeps its binding.

1. Update the cluster configuration by removing the selector and the StorageClass name and increasing the number of replicas:

    ```bash
    kubectl patch perconapgcluster cluster1 \
      --namespace "${NAMESPACE}" \
      --type=json \
      -p='[
        {"op":"remove","path":"/spec/instances/0/dataVolumeClaimSpec/selector"},
        {"op":"remove","path":"/spec/instances/0/dataVolumeClaimSpec/storageClassName"},
        {"op":"replace","path":"/spec/instances/0/replicas","value":3}
      ]'
    ```

    If you have a WAL volume, use this patch instead. It also removes the selector and the StorageClass name from `walVolumeClaimSpec`:

    ```bash
    kubectl patch perconapgcluster cluster1 \
      --namespace "${NAMESPACE}" \
      --type=json \
      -p='[
        {"op":"remove","path":"/spec/instances/0/dataVolumeClaimSpec/selector"},
        {"op":"remove","path":"/spec/instances/0/dataVolumeClaimSpec/storageClassName"},
        {"op":"remove","path":"/spec/instances/0/walVolumeClaimSpec/selector"},
        {"op":"remove","path":"/spec/instances/0/walVolumeClaimSpec/storageClassName"},
        {"op":"replace","path":"/spec/instances/0/replicas","value":3}
      ]'
    ```

    If you have tablespace volumes, add these two operations to the patch for each `tablespaceVolumes` entry. The index (`0` here) is the position of the entry in the list:

    ```text
    {"op":"remove","path":"/spec/instances/0/tablespaceVolumes/0/dataVolumeClaimSpec/selector"},
    {"op":"remove","path":"/spec/instances/0/tablespaceVolumes/0/dataVolumeClaimSpec/storageClassName"},
    ```

    Otherwise, the tablespace PVCs of the new replicas stay `Pending`. Each replica gets its own new tablespace volume.

2. Wait until all three PostgreSQL instances are ready:
    
    ```bash
    kubectl wait perconapgcluster/cluster1 \
      --namespace "${NAMESPACE}" \
      --for=jsonpath='{.status.postgres.instances[?(@.name=="instance1")].ready}'=3 \
      --timeout=600s
    ```
    
    ??? example "Expected output"

        ```{.text .no-copy}
        perconapgcluster.pgv2.percona.com/cluster1 condition met
        ```

    Don't wait for the `ready` cluster status here. The cluster still reports `ready` from before the patch, so `kubectl wait` for this status returns before the new replicas start.

## Take a post-migration backup

Create a new baseline for further point-in-time restores by making a full backup. You can reuse the volume-based backup repository, such as `repo1`, that this guide uses to keep local backups on persistent storage within your cluster. Or see [Configure backup storage](backups-storage.md) to stream backups there.

1. Create the `post-migration-backup.yaml` configuration file. This example configures backups to a volume-based backup repository following the cluster configuration in this guide. Set `--type=full` in `options`: without it, `pgBackRest` makes an incremental backup on top of the full backup that the Operator takes automatically after the cluster starts.

    ```yaml title="post-migration-backup.yaml"
    apiVersion: pgv2.percona.com/v2
    kind: PerconaPGBackup
    metadata:
      name: post-migration-backup
    spec:
      pgCluster: cluster1
      repoName: repo1
      options:
        - --type=full
    ```

2. Apply the configuration to start a backup:

    ```bash
    kubectl apply -f post-migration-backup.yaml -n "${NAMESPACE}"
    ```

3. Wait for the backup Job to complete:

    ```bash
    kubectl wait perconapgbackup/post-migration-backup \
      -n "${NAMESPACE}" \
      --for=jsonpath='{.status.state}'=Succeeded \
      --timeout=600s
    ```

    ??? example "Expected output"

        ```{.text .no-copy}
        perconapgbackup.pgv2.percona.com/post-migration-backup condition met
        ```

4. Check that the backup is a full backup:

    ```bash
    kubectl get perconapgbackup post-migration-backup \
      -n "${NAMESPACE}" \
      -o jsonpath='{.status.backupType}{"\n"}'
    ```

    The output is `full`.

## Point applications to Percona

1. Discover the `pgBouncer` Service for `cluster1`:

    ```bash
    kubectl get service -n "${NAMESPACE}" \
      -l postgres-operator.crunchydata.com/cluster=cluster1,postgres-operator.crunchydata.com/role=pgbouncer
    ```

2. Update your application's connection string to use the `pgBouncer` service name (from the previous step) as the PostgreSQL host. For example:

    ```
    Host:   cluster1-pgbouncer.<NAMESPACE>.svc.cluster.local
    Port:   5432
    ```

    Replace `<NAMESPACE>` with your cluster's namespace. Update your application configuration to point to this service, ensuring it now connects to your Percona Operator for PostgreSQL deployment.


## Cleanup

1. Remove the migration label from the PV after you no longer need to pin binding:

    ```bash
    kubectl label pv "${PV_NAME}" percona-pv-migration-
    ```

2. The PV still has the `Retain` reclaim policy. With this policy, the disk stays after you delete the Percona cluster and its PVCs. To delete the disk together with the cluster, like the other volumes of the cluster, set the policy back to `Delete`:

    ```bash
    kubectl patch pv "${PV_NAME}" \
      -p '{"spec":{"persistentVolumeReclaimPolicy":"Delete"}}'
    ```

Repeat these steps for the WAL PV and for each tablespace PV if you have them.

## Rollback

PV reuse is the least rollback-friendly path: once `cluster1` runs on the old directory, the previous Crunchy timeline is no longer authoritative. To roll back, restore from the [backup you made on the Crunchy cluster](#back-up-the-crunchy-cluster) to a new Crunchy cluster.

## Troubleshooting

### PVC stays `Pending`

Confirm the PV label, phase, and StorageClass name, and check which PVC the PV is bound to:

```bash
kubectl get pv "${PV_NAME}" --show-labels
kubectl get pv "${PV_NAME}" -o jsonpath='{.status.phase}{"\t"}{.spec.storageClassName}{"\t"}{.spec.claimRef.namespace}/{.spec.claimRef.name}{"\n"}'
```

Check the events of the Percona data PVC:

```bash
kubectl describe pvc -n "${NAMESPACE}" \
  -l postgres-operator.crunchydata.com/cluster=cluster1,postgres-operator.crunchydata.com/role=pgdata
```

For the WAL PVC, use `role=pgwal` instead of `role=pgdata`. For tablespace PVCs, use `role=tablespace`.

The following events point to these causes:

* `claim Selector is not supported` or `claim.Spec.Selector is not supported`. The PVC uses a StorageClass with a provisioner, and no matching PV was available. Either another PVC already took the PV (check `claimRef` in the previous output), or the PVC doesn't use the migration StorageClass name.
* The Pod reports `binding volumes: context deadline exceeded`, and the PVC has the `volume.kubernetes.io/selected-node` annotation with a node other than the PV's node. This happens with node-local storage when the PVC uses a StorageClass with `volumeBindingMode: WaitForFirstConsumer` instead of the migration StorageClass name: the scheduler picked a node where the PV isn't available.

The simplest fix is to [isolate the PV](#retain-the-pv-and-remove-the-crunchy-cluster) with the migration StorageClass name and set this name in the cluster configuration. If you can't change the StorageClass name, recover from a wrong node by pinning the instance to the PV's node:

1. Add the `affinity.nodeAffinity` rule for the PV's node to the instance in the cluster configuration.
2. Delete the Pending Pod. The instance StatefulSet uses the `OnDelete` update strategy, so the Pod doesn't pick up the new rule until you delete it.
3. Remove the stale node annotation from the PVC, or delete the PVC:

    ```bash
    kubectl annotate pvc <data-pvc-name> -n "${NAMESPACE}" volume.kubernetes.io/selected-node-
    ```

Remove the `affinity.nodeAffinity` rule before you [scale out the cluster](#scale-out-the-cluster). Otherwise, all replicas run on the same node as the primary. After you remove the rule, the Operator restarts the Pods and spreads them across nodes.

### PostgreSQL fails to start

Inspect database container logs:

```bash
kubectl -n "${NAMESPACE}" logs "${PERCONA_PRIMARY}" -c database
```

If the Pod is stuck in `Init:CrashLoopBackOff` and the `postgres-startup` init container log shows `mv: cannot stat '/pgwal/pg18_wal': No such file or directory`, the Crunchy cluster used a separate WAL volume, and the Percona instance doesn't have it. Add `walVolumeClaimSpec` bound to the retained WAL PV.

If the Crunchy cluster wasn't shut down cleanly, PostgreSQL runs crash recovery on the first start. Follow the Patroni and PostgreSQL logs for progress.

### Tables in a tablespace can't be read

The cluster reports `ready`, but queries on tables in a tablespace fail with an error like `ERROR:  could not open file "pg_tblspc/16444/PG_18_202506291/5/16445": No such file or directory`, and backups fail with `ERROR: [041]: unable to get info for missing path/file '/pgdata/pg18/pg_tblspc/16444/PG_18_202506291'`. The Crunchy cluster used tablespace volumes, and the Percona instance doesn't have them.

To fix it, delete the `PerconaPGCluster` and the PVCs it left behind, clear the `claimRef` of the data PV (and the WAL PV, if you have one) as in [Retain the PV and remove the Crunchy cluster](#retain-the-pv-and-remove-the-crunchy-cluster), and create the cluster again with `tablespaceVolumes` entries that have the same names and are bound to the retained tablespace PVs.

### PV was deleted

If the dynamic provisioner deleted the volume when the PVC disappeared, data is gone from that path. Use [Migrate from Crunchy using backup and restore](migrate-from-crunchy-backup-restore.md) from your latest remote backup instead.
