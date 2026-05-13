# Migrate from Crunchy to Percona Operator for PostgreSQL by reusing persistent volumes

This guide shows how to migrate to Percona Operator for PostgreSQL using the **primary** PostgreSQL data volume from your Crunchy `PostgresCluster` .
In this approach,  Percona `PerconaPGCluster` (`cluster1`) starts on the existing `PGDATA` data directory without running a backup-restore cycle over the network.

| Benefits | Trade-offs |
|----------|------------|
| - Avoids large data copies through object storage when the persistent volume already contains the dataset.<br>- Provides a direct migration path when it is important to keep the exact data directory intact. <> - Allows migrating even if the source cluster is deleted but the PV is preserved | - **Downtime** occurs from the moment you stop writes on Crunchy until the Percona cluster is brought up.<br>- **Rollback is difficult** once Percona has advanced the database on that volume; take a Crunchy `pgBackRest` backup before destructive steps if you may need to restore Crunchy.<br>- Requires manual management of PV **reclaim policy**, clearing `claimRef`, and setting a **PVC selector** to ensure the new claim binds only to the intended volume. |

If the backing PV was already deleted with the default **Delete** reclaim policy, use [Migrate from Crunchy using backup and restore](migrate-from-crunchy-backup-restore.md) instead.

--8<-- "crunchy-pgo-version.txt::6"

## Prerequisites

Ensure you have the following:

- A Kubernetes or OpenShift cluster with permissions to patch PersistentVolumes, delete `PostgresCluster` resources, and deploy the Percona Operator.
- `kubectl` or `oc`.
- Storage where you can set the PV reclaim policy to `Retain` and clear `claimRef` (cluster-admin privileges are often required).

The PostgreSQL **major version** on the Percona cluster must match the Crunchy source cluster.

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

1. Install Crunchy Operator for PostgreSQL into `$CRUNCHY_NS` if it is not already installed. Ssee the [Crunchy quickstart :octicons-link-external-16:](https://access.crunchydata.com/documentation/postgres-operator/5.8/quickstart))for the steps.

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

2. Wait for the cluster to report the `Ready` status:

    ```bash
    kubectl wait pod \
     -l postgres-operator.crunchydata.com/cluster=crunchy-source,postgres-operator.crunchydata.com/data=postgres \
     -n "${CRUNCHY_NS}" \
     --for=condition=Ready \
     --timeout=300s
    ```

    ??? example "Expected output"

        ```text
        pod/crunchy-source-instance1-gpx4-0 condition met
        ```

## Stop writes and identify the primary's Persistent Volume

Stopping application from writing to the database. This marks the **start of downtime**. 

Next, identify the primary Pod, its data PVC, and backing PV

1. Identify the primary Pod:

    ```bash
    CRUNCHY_PRIMARY=$(kubectl get pod -n "${CRUNCHY_NS}" \
      --selector postgres-operator.crunchydata.com/cluster=crunchy-source,postgres-operator.crunchydata.com/role=master \
      -o jsonpath='{.items[0].metadata.name}')
    ```

2. Retrieve the PVC:

    ```bash
    PVC_NAME=$(kubectl get pod -n "${CRUNCHY_NS}" "${CRUNCHY_PRIMARY}" \
      -o jsonpath='{.spec.volumes[?(@.name=="postgres-data")].persistentVolumeClaim.claimName}')
    ```

3. Retrieve the PV this PVC is bound to:

    ```bash
    PV_NAME=$(kubectl get pvc -n "${CRUNCHY_NS}" "${PVC_NAME}" \
      -o jsonpath='{.spec.volumeName}')
    ```

4. Verify the retrieved data:
    
    ```bash
    echo "Primary pod: ${CRUNCHY_PRIMARY}"
    echo "PVC:         ${PVC_NAME}"
    echo "PV:          ${PV_NAME}"
    ```

    ??? example "Sample output"

        ```{.text .no-copy}
        Primary pod: crunchy-source-instance1-gpx4-0
        PVC:         crunchy-source-instance1-gpx4-pgdata
        PV:          pvc-32f7bc5d-82c7-4d36-9886-56a581124cbd
        ```

    If your Crunchy Pod uses a volume name other than `postgres-data`, adjust the JSONPath filter.

## Retain the PV and remove the Crunchy cluster

The default reclaim policy for a dynamically PersistentVolume is `Delete`. This means that as soon as there are no Persistent Volume Claims (PVC) bound to this PV, Kubernetes deletes it and all data is lost. To prevent this, change the PV reclaim policy to `Retain`.

1. Set the PV reclaim policy to `Retain` so the disk survives PVC deletion:

    ```bash
    kubectl patch pv "${PV_NAME}" \
      -p '{"spec":{"persistentVolumeReclaimPolicy":"Retain"}}'
    ```

2. Patch the Crunchy `PostgresCluster` object to remove finalizers.
   Kubernetes "finalizers" block resource deletion until certain cleanup steps finish, such as the operator deleting related pods, PVCs, and secrets. Since we want to keep the PersistentVolume (PV) and avoid extra cleanup (like deleting the PV or data), we remove the finalizers to force Kubernetes to delete the `PostgresCluster` resource immediately. This lets us proceed with detaching the data volume for migration without waiting for the Crunchy Operator's normal deletion behavior.

    ```bash
    kubectl patch postgrescluster crunchy-source -n "${CRUNCHY_NS}" \
      --type=json \
      -p='[{"op":"remove","path":"/metadata/finalizers"}]'
    ```

3. Now, delete the `PostgresCluster`:

    ```bash
    kubectl delete postgrescluster crunchy-source -n "${CRUNCHY_NS}"
    ```

4. Uninstall Crunchy Operator from `$CRUNCHY_NS` when no `PostgresCluster` resources remain.

5. After the data PVC is gone, the PV enters the `Released` state. However, it still references the old claim and cannot be claimed by a new PVC. Therefore, you need to clear its `claimRef`:

    ```bash
    kubectl patch pv "${PV_NAME}" --type=json \
      -p='[{"op":"remove","path":"/spec/claimRef"}]'
    ```

6. Wait until the PV status becomes `Available`:

    ```bash
    kubectl wait pv "${PV_NAME}" \
      --for=jsonpath='{.status.phase}'=Available \
      --timeout=60s
    ```

    ??? example "Expected output"
        
        ```text
        persistentvolume/pvc-32f7bc5d-82c7-4d36-9886-56a581124cbd condition met
        ```

7. Label the PV so the Percona PVC selector binds to it exclusively, avoiding accidental binding to another released volume:

    ```bash
    kubectl label pv "${PV_NAME}" percona-pv-migration=migrated
    ```

## Create the Percona cluster bound to the retained volume

1. Edit the `deploy/cr.yaml` and specify the following settings:
    
    * Give a name to your cluster  in the `metadata.name` (for example, `cluster1`)
    * Align `spec.postgresVersion` with the old cluster.
    * For the first cutover, set **one** replica on the instance that should attach to the migrated disk
    * Add a `selector` on `dataVolumeClaimSpec` matching the PV label. This ensures the controller binds the PVC to the correct PV that has the specified label.
    
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
            accessModes:
              - ReadWriteOnce
            resources:
              requests:
                storage: 10Gi
            selector:
              matchLabels:
                percona-pv-migration: migrated
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

    Tune `storage`, `storageClassName`, and other fields to match your environment and the Operator’s usual `deploy/cr.yaml` requirements (users, images, resources).

2. Apply the manifest:

    ```bash
    kubectl apply -f deploy/cr-cluster1-pv.yaml -n "${NAMESPACE}"
    ```

    The Percona Operator creates a PersistentVolumeClaim (PVC) using the selector you specified in the manifest. This PVC binds to the labelled PersistentVolume (PV) that contains the migrated PostgreSQL data. PostgreSQL then starts directly on the existing `PGDATA` directory, so no backup restore, WAL download, or object storage is needed. 

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

## Scale out the cluster

You started the cluster with a single replica, so the Operator created a PersistentVolumeClaim (PVC) that bound to your labelled PersistentVolume (PV) containing the migrated data. Once you have confirmed that the primary instance is healthy, scale out your cluster for high availability. 

While the selector is present in the cluster configuration, it blocks the Operator to create new replica PVCs because no other PV carries `percona-pv-migration=migrated`. Therefore, you need to remove the selector. Doing so enables the Operator to create new PVCs for each replica using your default StorageClass.

1. Update the cluster configuration by removing the selector and increasing the number of replicas:

    ```bash
    kubectl patch perconapgcluster cluster1 \
      --namespace "${NAMESPACE}" \
      --type=json \
      -p='[
        {"op":"remove","path":"/spec/instances/0/dataVolumeClaimSpec/selector"},
        {"op":"replace","path":"/spec/instances/0/replicas","value":3}
      ]'
    ```

2. Wait for the cluster to report the `Ready` status:
    
    ```bash
    kubectl wait perconapgcluster/cluster1 \
      --namespace "${NAMESPACE}" \
      --for=jsonpath='{.status.state}'=ready \
      --timeout=300s
    ```
    
    ??? example "Expected output"

        ```text
        perconapgcluster.pgv2.percona.com/cluster1 condition met
        ```

## Take a post-migration backup

Create a new baseline for further point-in-time restores by making a full backup. You can reuse the volume-based backup repository (like the `repo1` shown earlier) to keep local backups on persistent storage within your cluster.Or [Configure backup storage](backups-storage.md) to stream backups there.

1. Edit the `deploy/backup.yaml`. This example configures backups to a volume-based backup repository following the cluster configuration in this guide:

    ```yaml title="deploy/backup.yaml"
    apiVersion: pgv2.percona.com/v2
    kind: PerconaPGBackup
    metadata:
      name: post-migration-backup
    spec:
      pgCluster: cluster1
      repoName: repo1
    ```

2. Apply the configuration to start a backup:

    ```bash
    kubectl apply -f deploy/post-migration-backup.yaml -n "${NAMESPACE}"
    ```

3. Wait for the backup Job to complete:

    ```bash
    kubectl wait perconapgbackup/post-migration-backup \
      -n "${NAMESPACE}" \
      --for=jsonpath='{.status.state}'=Succeeded \
      --timeout=600s
    ```

## Point applications to Percona

1. Discover the `pgBouncer` Service for `cluster1`:

    ```bash
    kubectl get service -n "${NAMESPACE}" \
      -l postgres-operator.crunchydata.com/cluster=cluster1,postgres-operator.crunchydata.com/role=pgbouncer
    ```

2. Update your application's connection string to use the `pgBouncer` service name (from the previous step) as the PostgreSQL host. For example:

    ```
    Host:   cluster1-pgbouncer.$NAMESPACE.svc.cluster.local
    Port:   5432
    ```

   Replace `${NAMESPACE}` with your cluster's namespace. Update your application configuration to point to this service, ensuring it now connects to your Percona Operator for PostgreSQL deployment.

## Cleanup

Remove the migration label from the PV after you no longer need to pin binding:

```bash
kubectl label pv "${PV_NAME}" percona-pv-migration-
```

## Rollback

PV reuse is the least rollback-friendly path: once `cluster1` runs on the old directory, the previous Crunchy timeline is no longer authoritative. If you need a fallback, take a full Crunchy `pgBackRest` backup **before** you delete `crunchy-source`, and treat that backup as your recovery source for a new Crunchy deployment.

## Troubleshooting

### PVC stays `Pending`

Confirm the PV label and phase:

```bash
kubectl get pv "${PV_NAME}" --show-labels
kubectl get pv "${PV_NAME}" -o jsonpath='{.status.phase}{"\n"}'
```

### PostgreSQL fails to start

Inspect database container logs:

```bash
kubectl -n "${NAMESPACE}" logs "${PERCONA_PRIMARY}" -c database
```

Unclean shutdowns may require crash recovery; follow Patroni and PostgreSQL logs for progress.

### PV was deleted

If the dynamic provisioner deleted the volume when the PVC disappeared, data is gone from that path. Use [Migrate from Crunchy using backup and restore](migrate-from-crunchy-backup-restore.md) from your latest remote backup instead.

