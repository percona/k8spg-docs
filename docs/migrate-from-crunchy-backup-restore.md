# Migrate from Crunchy to Percona Operator for PostgreSQL using backup and restore

You can migrate by taking a full `pgBackRest` backup on your Crunchy `PostgresCluster` and creating a new `PerconaPGCluster` that restores from that backup before its first start. This path is straightforward when you can accept downtime between the final backup and an application cutover.

| Benefits  | Trade-offs  | 
| ----------| ----------- | 
| - A clear cutover point <br> - Room to rehearse restore and validation before switching applications <br> - The option to roll back to Crunchy until you decommission the source cluster and redirect traffic  | - Writes stop from the cutover until the Percona cluster is ready. <br> - Downtime spans the restore and validation time. The restore replays the WAL archived after the migration backup, so a recent backup shortens it. |

For **near-zero downtime**, use [Migrate from Crunchy using a standby cluster](migrate-from-crunchy-standby.md) instead.

--8<-- "crunchy-pgo-version.txt"

## Before you migrate

Complete the [Pre-migration compatibility checks](migrate-checklist.md). Physical methods require a matching PostgreSQL major version and CPU architecture.

## Prerequisites

Ensure you have the following:

- A Kubernetes or OpenShift cluster with permissions to create namespaces, CRDs, Roles, and Deployments.
- [Helm](https://helm.sh/) 3.x (if you install operators or optional in-cluster object storage with Helm).
- `kubectl` or `oc`.
- [yq](https://github.com/mikefarah/yq) YAML processor (optional, for manifest tricks used in other migration guides).
- A remote backup storage reachable from Pods in both the Crunchy and Percona namespaces.

## Before you start

1. Create or choose namespaces for Crunchy and Percona and export them.

    ```bash
    export CRUNCHY_NS=postgres-operator
    export NAMESPACE=pgo
    ```

2. Clone the Percona Operator repository at the release you will deploy so you can base your `PerconaPGCluster` manifest on the default `deploy/cr.yaml`:

    ```bash
    git clone -b v{{release}} https://github.com/percona/percona-postgresql-operator
    ```

## Configure Crunchy PostgreSQL cluster for remote backups

If you already run Crunchy PGO, configure the  `PostgresCluster` object so that `pgBackRest` writes backups and WAL (Write-Ahead Logs) to remote storage that the Percona cluster can access and read. This ensures that Percona can restore from your latest backups when you perform the migration.

If you are deploying Crunchy for testing or migration rehearsal, make sure your `PostgresCluster` manifest configures `pgBackRest` to use the same remote object storage (for example, S3 or S3-compatible, Google Cloud Storage, or compatible endpoint) for both backups and WAL archives. The Percona PostgreSQL cluster will need access to this storage location for a successful restore.

This involves:

- Creating a Secret with the required credentials for your object storage (e.g., S3 access keys or GCS service account).
- Referencing that Secret under the `spec.backups.pgbackrest.configuration` section in your Crunchy `PostgresCluster` manifest.
- Adding an object storage repository under `spec.backups.pgbackrest.repos` with the bucket, region, endpoint, and other storage details. Note its path: you need it on the Percona side under `spec.dataSource.pgbackrest`. If you don't set `repo<N>-path`, Crunchy uses `/pgbackrest/repo<N>`, for example, `/pgbackrest/repo2`.
- Adding the `spec.backups.pgbackrest.manual` section, so that you can start a backup to this repository on demand.
- Ensuring network access between Crunchy and Percona namespaces to the object storage endpoint.

See the [standby migration guide](migrate-from-crunchy-standby.md#adapt-the-configuration-for-crunchy-postgresql-cluster) for an example manifest that creates the required Secret and configures remote backups and WAL archiving.

### Clusters that already have a backup repository

Many existing Crunchy clusters use a volume (PVC) repository as `repo1`, and keep backups in object storage in `repo2` or a higher-numbered repository. Check which repositories your cluster has:

```bash
kubectl get postgrescluster.postgres-operator.crunchydata.com crunchy-source \
  -n "${CRUNCHY_NS}" \
  -o jsonpath='{range .spec.backups.pgbackrest.repos[*]}{.name}{"\t"}{.s3.bucket}{.gcs.bucket}{.azure.container}{.volume.volumeClaimSpec.resources.requests.storage}{"\n"}{end}'
```

??? example "Sample output"

    ```{.text .no-copy}
    repo1   2Gi
    repo2   my-backup-bucket
    ```

A bucket or container name means an object storage repository. A storage size means a volume repository. In this example, `repo1` is a volume repository and `repo2` is in object storage.

* If the cluster already has an object storage repository, use it for the migration. You don't need to rename it to `repo1`.
* If the cluster only has a volume repository, add an object storage repository with the next free name, for example, `repo2`. Don't replace or remove `repo1`. The Percona cluster can't restore from a volume repository of another cluster: neither `dataSource.pgbackrest` with a `volume` repository nor `dataSource.postgresCluster` can read it.

Changing `spec.backups` on an existing Crunchy cluster restarts its PostgreSQL Pods. Plan this change for a maintenance window.

The rest of this guide uses `repo1` in object storage. If your repository has a different name, set `manual.repoName` to it, use it in the `stanzaCreated` wait command, and see [how to reference it on the Percona side](#create-the-percona-postgresql-cluster-from-the-crunchy-backup).

Here's the example configuration of the Crunchy `PostgresCluster` object:

```yaml title="postgres.yaml"
apiVersion: postgres-operator.crunchydata.com/v1beta1
kind: PostgresCluster
metadata:
  name: crunchy-source
spec:
  postgresVersion: 18
  instances:
    - name: instance1
      replicas: 3
      dataVolumeClaimSpec:
        accessModes:
          - ReadWriteOnce
        resources:
          requests:
            storage: 10Gi
  backups:
    pgbackrest:
      configuration:
        - secret:
            name: crunchy-pgbackrest-secret
      manual:
        repoName: repo1
        options:
          - --type=full
      global:
        repo1-path: /crunchy-to-percona/repo1
        repo1-s3-uri-style: path
        repo1-s3-verify-tls: "n"
      repos:
        - name: repo1
          s3:
            bucket: <YOUR-BUCKET-HERE>
            endpoint: s3.amazonaws.com
            region: <YOUR-REGION-HERE>
  proxy:
    pgBouncer:
      replicas: 1
```

Apply the configuration to create a new or update an existing cluster:

```bash
kubectl apply -f postgres.yaml -n $CRUNCHY_NS
```

Wait until all PostgreSQL instances of the cluster are ready. Set the number to the `replicas` value of the `instance1` instance set (`3` in this example):

```bash
kubectl wait postgrescluster.postgres-operator.crunchydata.com/crunchy-source \
  -n "${CRUNCHY_NS}" \
  --for=jsonpath='{.status.instances[?(@.name=="instance1")].readyReplicas}'=3 \
  --timeout=600s
```

??? example "Expected output"

    ```{.text .no-copy}
    postgrescluster.postgres-operator.crunchydata.com/crunchy-source condition met
    ```

This command waits on the cluster status, so you can run it right after `kubectl apply`. A `kubectl wait pod` command fails with `no matching resources found` if the Pods don't exist yet.

Wait for the `pgBackRest` stanza to be created. The stanza initializes the backup and restore infrastructure for further backup or restore operations. Specify the repository that stores backups in the object storage (`repo1` in this example):

```bash
kubectl wait postgrescluster.postgres-operator.crunchydata.com/crunchy-source \
  -n "${CRUNCHY_NS}" \
  --for=jsonpath='{.status.pgbackrest.repos[?(@.name=="repo1")].stanzaCreated}'=true \
  --timeout=300s
```

??? example "Expected output"

    ```text
    postgrescluster.postgres-operator.crunchydata.com/crunchy-source condition met
    ```

The `stanzaCreated` status confirms that `pgBackRest` has scanned the configuration and the data directory and is ready to manage backups for your cluster.

## Create the migration backup

Add a few test records to your database, then trigger a full backup.

This backup is the starting point for the restore of `cluster1` on Percona. You don't need to stop application writes for it: the restore replays the WAL that Crunchy archives after the backup. You stop writes later, at the [cutover](#prepare-the-cutover).

1. Identify the primary Pod of the Crunchy PostgreSQL cluster and export it as an environment variable:

    ```bash
    CRUNCHY_PRIMARY=$(kubectl get pod \
        -l postgres-operator.crunchydata.com/cluster=crunchy-source,postgres-operator.crunchydata.com/role=master \
        -n "${CRUNCHY_NS}" \
        -o jsonpath='{.items[0].metadata.name}')
    ```

2. Connect to the Crunchy PostgreSQL cluster and insert some sample data. Use the following command to exec to the primary Pod, create a database and a table and insert some data to it:

    ```bash
    kubectl exec -n "${CRUNCHY_NS}" "${CRUNCHY_PRIMARY}" -c database -- bash -c "
        psql -c 'CREATE DATABASE migrationtest;'
        psql -d migrationtest -c 'CREATE TABLE migration_data (id int PRIMARY KEY, value text);'
        psql -d migrationtest -c \"INSERT INTO migration_data VALUES (1, 'initial-data-before-migration');\"
      "
    ```

3. Start a full backup. The annotation value identifies this backup request, so save it in a variable:

    ```bash
    BACKUP_ID=$(date +%s)
    kubectl annotate postgrescluster.postgres-operator.crunchydata.com crunchy-source \
      -n "${CRUNCHY_NS}" \
      --overwrite \
      postgres-operator.crunchydata.com/pgbackrest-backup="${BACKUP_ID}"
    ```

    The `--overwrite` flag lets you re-run the command if the cluster already has this annotation from an earlier backup.

4. Wait until the Crunchy Operator picks up this backup request:

    ```bash
    kubectl wait postgrescluster.postgres-operator.crunchydata.com/crunchy-source \
      -n "${CRUNCHY_NS}" \
      --for=jsonpath='{.status.pgbackrest.manualBackup.id}'="${BACKUP_ID}" \
      --timeout=120s
    ```

5. Wait for the backup to finish:

    ```bash
    kubectl wait postgrescluster.postgres-operator.crunchydata.com/crunchy-source \
      -n "${CRUNCHY_NS}" \
      --for=jsonpath='{.status.pgbackrest.manualBackup.finished}'=true \
      --timeout=600s
    ```

    On a newly created Crunchy cluster, the Crunchy Operator first completes its automatic initial backup and starts your backup only after that. The timeout covers both backups. For a large cluster, increase it.

    ??? example "Expected output"

        ```{.text .no-copy}
        postgrescluster.postgres-operator.crunchydata.com/crunchy-source condition met
        ```

6. Check that the backup succeeded:

    ```bash
    kubectl get postgrescluster.postgres-operator.crunchydata.com crunchy-source \
      -n "${CRUNCHY_NS}" \
      -o jsonpath='{.status.pgbackrest.manualBackup.succeeded}{"\n"}'
    ```

    The output is `1` for a successful backup.

    If the backup fails, the Crunchy Operator retries it. During the retries, `finished` stays `false` and the previous wait times out, while `status.pgbackrest.manualBackup.failed` counts the failed attempts. Check it with:

    ```bash
    kubectl get postgrescluster.postgres-operator.crunchydata.com crunchy-source \
      -n "${CRUNCHY_NS}" \
      -o jsonpath='{.status.pgbackrest.manualBackup}{"\n"}'
    ```

    To find the backup Job and check its logs, run:

    ```bash
    kubectl get job -n "${CRUNCHY_NS}" \
      -l postgres-operator.crunchydata.com/cluster=crunchy-source,postgres-operator.crunchydata.com/pgbackrest-backup=manual
    ```

    After you fix the cause, start the backup again with a new `BACKUP_ID` value.

## Prepare pgBackRest credentials in the Percona namespace

Create a Secret in `$NAMESPACE` with the **same** credentials and storage information such as endpoint and region that you used to configure `pgBackRest` in the Crunchy PostgreSQL cluster.

The following example command creates a Secret with the name `percona-pgbackrest-secret` for the Percona cluster; keep that name if you copy the manifest below.

```bash
kubectl apply -n "$NAMESPACE" -f - <<EOF
apiVersion: v1
kind: Secret
metadata:
  name: percona-pgbackrest-secret
stringData:
  s3.conf: |
    [global]
    repo1-s3-key=<your-access-key>
    repo1-s3-key-secret=<your-access-secret>
EOF
``` 

If you use different Secret names, use your name consistently in `spec.dataSource.pgbackrest.configuration` and `spec.backups.pgbackrest.configuration` on `PerconaPGCluster` `cluster1`.

## Deploy Percona Operator for PostgreSQL

1. Deploy Percona Operator for PostgreSQL:

    ```bash
    kubectl apply --server-side -f https://raw.githubusercontent.com/percona/percona-postgresql-operator/v{{release}}/deploy/bundle.yaml -n $NAMESPACE
    ```

2. Wait for the Percona Operator Deployment to become available:

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

## Prepare the cutover

The Percona cluster restores the migration backup and then replays the WAL that Crunchy archived after it. Writes are carried over up to the last archived WAL file. Crunchy archives the current WAL file when it is full or after `archive_timeout` (60 seconds by default), so the last writes can still be in a WAL file that isn't archived yet. To carry over every write, make Crunchy archive the current WAL file after you stop writes:

1. Stop application writes to the Crunchy cluster. This is the start of the downtime.

2. Switch to a new WAL file, so that Crunchy archives the current one. Save the name of the archived file:

    ```bash
    WAL_FILE=$(kubectl -n "${CRUNCHY_NS}" exec "${CRUNCHY_PRIMARY}" -c database -- \
      psql -tAc "SELECT pg_walfile_name(pg_switch_wal());")
    echo "${WAL_FILE}"
    ```

3. Wait until Crunchy reports this file as archived:

    ```bash
    until [ "$(kubectl -n "${CRUNCHY_NS}" exec "${CRUNCHY_PRIMARY}" -c database -- \
      psql -tAc "SELECT last_archived_wal >= '${WAL_FILE}' FROM pg_stat_archiver;")" = "t" ]; do
      echo "Waiting for ${WAL_FILE} to be archived..."
      sleep 2
    done
    ```

Now the repository contains every write. Create the Percona cluster in the next section. You don't need a new backup.

??? note "Restore up to a specific point in time instead"

    To restore only up to a specific moment, for example, if you can't stop writes, add point-in-time recovery options to `spec.dataSource.pgbackrest`:

    ```yaml
    dataSource:
      pgbackrest:
        options:
          - --type=time
          - --target="2026-10-15 10:05:55+00"
    ```

    PostgreSQL compares the target with the **commit** time of each transaction. A transaction that commits after the target isn't restored, even if your application recorded an earlier timestamp for it. Set the target to the commit time of the last transaction you need, or later. You don't need to add `--target-action=promote`: the Operator adds it.

## Create the Percona PostgreSQL cluster from the Crunchy backup

1. Edit the `deploy/cr.yaml` manifest and specify the following:

    1. Set `spec.postgresVersion` to the same major version as `crunchy-source`.
    2. The `spec.dataSource.pgbackrest` configuration to reference the Secret with the credentials to the object store and to point at the **same** repository path and object store settings as the Crunchy repository you back up to. (See [Understand the `dataSource` options](backups-clone.md#understand-the-datasource-options) for more information about these options.)

        The repository name in `repo.name` and the `repo<N>-` prefix of the options in `global` and in the Secret must match each other. They don't need to match the repository name on Crunchy. For example, to restore from a Crunchy `repo2` with the default path, either use `repo2` everywhere (`repo.name: repo2`, `repo2-path: /pgbackrest/repo2`, and `repo2-s3-key` in the Secret), or use `repo1` everywhere and set `repo1-path: /pgbackrest/repo2`. See [Clone from cloud storage](backups-clone.md#clone-from-cloud-storage-s3-gcs-azure-blob) for details.

    3. Under `spec.backups.pgbackrest`, use a **different** `repo<N>-path` than the Crunchy cluster so new backups do not overwrite the migration archive.
    4. Set the storage size in `spec.instances[].dataVolumeClaimSpec` so that it fits the Crunchy data and WAL. The default `deploy/cr.yaml` requests only 1Gi.
    5. If the Crunchy cluster uses tablespace volumes (`spec.instances[].tablespaceVolumes`), add a `tablespaceVolumes` entry with **the same name** for each tablespace to the Percona instance. The restore writes each tablespace to its original location under `/tablespaces/<name>`, where the Operator mounts the tablespace volume, so the volume must exist. For example:

        ```yaml
        instances:
          - name: instance1
            tablespaceVolumes:
              - name: ts1
                dataVolumeClaimSpec:
                  accessModes:
                    - ReadWriteOnce
                  resources:
                    requests:
                      storage: 5Gi
        ```

        To store the tablespaces on the data volume instead, add `--tablespace-map-all=/pgdata/tablespaces` to `spec.dataSource.pgbackrest.options`. The tablespace locations then change to `/pgdata/tablespaces/<name>`.

    The following fragment shows the important pieces; merge them with the rest of `deploy/cr.yaml` (images, users, resources) for your environment:

    ```yaml
    metadata:
      name: cluster1
    spec:
      ....
      dataSource:
        pgbackrest:
          stanza: db
          configuration:
            - secret:
                name: percona-pgbackrest-secret
          global:
            # The path of the Crunchy repository: its repo<N>-path value, or /pgbackrest/repo<N> if it isn't set
            repo1-path: /crunchy-to-percona/repo1
            repo1-s3-uri-style: path
            repo1-s3-verify-tls: "n" # Omit or set to "y" for AWS S3 with valid TLS
          repo:
            name: repo1
            s3:
              bucket: <YOUR_BUCKET_HERE>
              endpoint: s3.amazonaws.com
              region: <YOUR_REGION_HERE>
      backups:
        pgbackrest:
          configuration:
            - secret:
                name: percona-pgbackrest-secret
          global:
            # Must be different from the Crunchy repo1-path
            repo1-path: /percona/cluster1/repo1
            repo1-s3-uri-style: path
            repo1-s3-verify-tls: "n"
          repos:
            - name: repo1
            # The storage is shared, use the same settings here 
              s3:
                bucket: <YOUR_BUCKET_HERE>
                endpoint: s3.amazonaws.com
                region: <YOUR_REGION_HERE>
       # The rest of your configuration
    ```

2. Apply the manifest:

    ```bash
    kubectl apply -f deploy/cr.yaml -n "${NAMESPACE}"
    ```

3. Wait until the cluster reports the `Ready` state:

    ```bash
    kubectl wait perconapgcluster/cluster1 \
      -n "${NAMESPACE}" \
      --for=jsonpath='{.status.state}'=ready \
      --timeout=600s
    ```

    The Percona Operator deploys the cluster and bootstraps it from the storage referenced in the `dataSource` section.

    The cluster can report `ready` as soon as the primary starts, and then report `initializing` again for a minute or two while the replicas start. The primary accepts connections during this time.

4. Verify that the data was restored successfully:
    
    - Identify the primary Pod and export it as an environment variable:

        ```bash
        PERCONA_PRIMARY=$(kubectl get pod -n "${NAMESPACE}" \
        --selector postgres-operator.crunchydata.com/cluster=cluster1,postgres-operator.crunchydata.com/role=primary \
        -o jsonpath='{.items[0].metadata.name}')
        ```
    
    - Verify the data insertion:

        ```bash
        kubectl exec -n "${NAMESPACE}" "${PERCONA_PRIMARY}" -c database -- bash -c \
         "psql -q -t -d migrationtest -c 'SELECT id, value FROM migration_data ORDER BY id;'"
        ```

        ??? example "Expected output"

            ```{.sql .no-copy}
            1 | initial-data-before-migration
            ```
    
    - Exec into the Pod and check that it is not in recovery state:

        ```bash
        kubectl -n "${NAMESPACE}" exec "${PERCONA_PRIMARY}" -c database -- \
          psql -t -c "SELECT pg_is_in_recovery();"
        ```

        You should see `f`: the instance is read-write.

5. Wait until the new cluster’s `pgBackRest` stanza exists for ongoing backups:

    ```bash
    kubectl wait perconapgcluster/cluster1 \
      -n "${NAMESPACE}" \
      --for=jsonpath='{.status.pgbackrest.repos[0].stanzaCreated}'=true \
      --timeout=300s
    ```

    ??? example "Expected output"

        ```{.text .no-copy}
        perconapgcluster.pgv2.percona.com/cluster1 condition met
        ```

## Take a post-migration backup

Create a baseline backup on Percona's own repository path so future restores do not depend on the Crunchy archive.

1. Create the `post-migration-backup.yaml` configuration file. Set `--type=full` in `options`: without it, `pgBackRest` makes an incremental backup on top of the full backup that the Operator takes automatically after the cluster starts.

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

2. Apply the configuration to start the backup:
   
    ```bash
    kubectl apply -f post-migration-backup.yaml -n "${NAMESPACE}"
    ```

3. Wait for the backup job to complete:

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

## Decommission the Crunchy cluster

After traffic runs on Percona and you are satisfied with validation, you can delete the Crunchy PostgreSQL cluster. Deleting it also deletes its user Secrets and its data volumes. The backups in object storage stay.

```bash
kubectl delete postgrescluster.postgres-operator.crunchydata.com crunchy-source -n "${CRUNCHY_NS}"
```

Uninstall Crunchy Operator from its namespace when no `PostgresCluster` resources remain.

## Rollback

Until you move write traffic to `cluster1`, rollback is to point applications back at the Crunchy `pgBouncer` Service. After cutover, new writes exist only on Percona; reconciling them back to Crunchy is a manual process.

After you delete the `crunchy-source` cluster, rollback means restoring a new Crunchy cluster from the Crunchy repository in object storage, if you still have that repository.

## Troubleshooting

### Restore fails with `no backup set found to restore`

The restore Job log shows `unable to load info file '<path>/backup/db/backup.info' or '<path>/backup/db/backup.info.copy'`, followed by `ERROR: [075]: no backup set found to restore`. The `pgBackRest` path in `spec.dataSource.pgbackrest.global` doesn't point to the Crunchy repository. Compare it with the path of the Crunchy repository. If the Crunchy cluster doesn't set `repo<N>-path`, the path is `/pgbackrest/repo<N>`.

```bash
kubectl get postgrescluster.postgres-operator.crunchydata.com crunchy-source -n "${CRUNCHY_NS}" \
  -o jsonpath='{.spec.backups.pgbackrest.global}{"\n"}'

kubectl get perconapgcluster cluster1 -n "${NAMESPACE}" \
  -o jsonpath='{.spec.dataSource.pgbackrest.global}{"\n"}'
```

If the log shows `restore command requires option: repo1-s3-key`, the `repo<N>-` prefix of the Secret keys doesn't match `repo.name` in `spec.dataSource.pgbackrest`.

### Restore fails with `Read-only file system` for `/tablespaces`

The restore Job log shows `ERROR: [047]: unable to create path '/tablespaces': [30] Read-only file system`, or the same error for `/tablespaces/<name>`. The Crunchy cluster uses tablespace volumes, and the Percona instance has no `tablespaceVolumes` entry with the same name. Add the entries, or map the tablespaces to the data volume with `--tablespace-map-all`. See [Create the Percona PostgreSQL cluster from the Crunchy backup](#create-the-percona-postgresql-cluster-from-the-crunchy-backup).

### Restore job failures (TLS, endpoint)

`pgBackRest` uses HTTPS for S3-compatible endpoints. Fix TLS trust (correct CA or `repo1-s3-verify-tls`) and confirm network reachability from the restore Pod to the bucket endpoint. See [Configure backup storage](backups-storage.md).

### Cluster stuck in restore

Inspect the logs of the restore Job. The Job and its Pods exist only while the restore runs or fails:

```bash
kubectl logs \
  -l postgres-operator.crunchydata.com/cluster=cluster1,postgres-operator.crunchydata.com/pgbackrest-restore \
  -n "${NAMESPACE}" \
  -c pgbackrest-restore \
  --tail=-1
```

Without `--tail=-1`, `kubectl logs` with a label selector shows only the last 10 lines of each Pod.

### Wrong or incomplete data

If the latest writes are missing, the WAL file that contains them wasn't archived when the restore finished. Delete `cluster1` on Percona, follow [Prepare the cutover](#prepare-the-cutover), and re-apply the restore manifest so it bootstraps again.


