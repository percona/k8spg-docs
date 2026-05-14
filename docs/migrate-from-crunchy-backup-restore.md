# Migrate from Crunchy to Percona Operator for PostgreSQL using backup and restore

You can migrate by taking a full `pgBackRest` backup on your Crunchy `PostgresCluster` and creating a new `PerconaPGCluster` that restores from that backup before its first start. This path is straightforward when you can accept downtime between the final backup and an application cutover.

| Benefits  | Trade-offs  | 
| ----------| ----------- | 
| - A clear cutover point (the migration backup) <br> - Room to rehearse restore and validation before switching applications <br> - The option to roll back to Crunchy until you decommission the source cluster and redirect traffic  | - Any data written **after** the migration backup and **before** cutover to Percona is not carried over unless you take another backup and re-bootstrap. <br> - Downtime spans at least that backup window plus restore and validation time. |

For **near-zero downtime**, use [Migrate from Crunchy using a standby cluster](migrate-from-crunchy-standby.md) instead.

--8<-- "crunchy-pgo-version.txt"

## Prerequisites

Ensure you have the following:

- A Kubernetes or OpenShift cluster with permissions to create namespaces, CRDs, Roles, and Deployments.
- [Helm](https://helm.sh/) 3.x (if you install operators or optional in-cluster object storage with Helm).
- `kubectl` or `oc`.
- [yq](https://github.com/mikefarah/yq) YAML processor (optional, for manifest tricks used in other migration guides).
- A remote backup storage reachable from Pods in both the Crunchy and Percona namespaces.

The PostgreSQL **major version** on the Percona cluster must match the Crunchy source cluster.

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
- Referencing that Secret under the `spec.backups.pgbackrest.repos` section in your Crunchy `PostgresCluster` manifest.
- Setting options such as `repo1-path`, bucket, region, endpoint, and other storage details to match what you plan to use on the Percona side under `spec.dataSource.pgbackrest`.
- Ensuring network access between Crunchy and Percona namespaces to the object storage endpoint.

See the [standby migration guide](migrate-from-crunchy-standby.md#adapt-the-configuration-for-crunchy-postgresql-cluster) for an example manifest that creates the required Secret and configures remote backups and WAL archiving.

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
            region: <YOUR-ENDPOINT-HERE>
  proxy:
    pgBouncer:
      replicas: 1
```

Apply the configuration to create a new or update an existing cluster:

```bash
kubectl apply -f postgres.yaml -n $CRUNCHY_NS
```

Wait for the cluster to report the "Ready" status:

```bash
kubectl wait pod \
  -l postgres-operator.crunchydata.com/cluster=crunchy-source,postgres-operator.crunchydata.com/data=postgres \
  -n "${CRUNCHY_NS}" \
  --for=condition=Ready \
  --timeout=300s
```

??? example "Expected output"

    ```{.text .no-copy}
    pod/crunchy-source-instance1-9rgg-0 condition met
    pod/crunchy-source-instance1-dz45-0 condition met
    pod/crunchy-source-instance1-p6pl-0 condition met
    ```

Wait for the `pgBackRest` stanza to be created. The stanza initializes the backup and restore infrastructure for further backups or restore operations. 

```bash
kubectl wait postgrescluster/crunchy-source \
  -n "${CRUNCHY_NS}" \
  --for=jsonpath='{.status.pgbackrest.repos[0].stanzaCreated}'=true \
  --timeout=300s
```

??? example "Expected output"

    ```text
    postgrescluster.postgres-operator.crunchydata.com/crunchy-source condition met
    ```

The `stanzaCreated` status confirms that `pgBackRest` has scanned the configuration and the data directory and is ready to manage backups for your cluster.

## Create the migration backup

Add a few test records to your database, then trigger a full backup.

This backup is the restore point for `cluster1` on Percona. **Stop application writes** before you trigger it if you need a consistent cutover; otherwise treat everything after this backup as disposable until cutover.

1. 1. Identify the primary Pod of the the Crunchy PostgreSQL cluster and export it as an environment variable:

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

2. Trigger a full backup:

    ```bash
    kubectl annotate postgrescluster crunchy-source \
      -n "${CRUNCHY_NS}" \
      postgres-operator.crunchydata.com/pgbackrest-backup="$(date +%s)"
    ```

3. Wait for the backup Job to complete:

    ```bash
    kubectl wait job \
      -l postgres-operator.crunchydata.com/pgbackrest-backup=manual,postgres-operator.crunchydata.com/cluster=crunchy-source \
      -n "${CRUNCHY_NS}" \
      --for=condition=Complete \
      --timeout=600s
    ```

    ??? example "Expected output"

        ```{.text .no-copy}
        job.batch/crunchy-source-backup-6pvj condition met
        ```

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
    repo1-s3-key="<your-access-key>"
    repo1-s3-key-secret="<your-access-secret>"
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

## Create the Percona PostgreSQL cluster from the Crunchy backup

1. Edit the `deploy/cr.yaml` manifest and specify the following:

    1. Set `spec.postgresVersion` to the same major version as `crunchy-source`.
    2. The `spec.dataSource.pgbackrest` configuration to reference the Secret with the credentials to the object store and to point at the **same** repository path and object store settings as the Crunchy cluster’s `repo1`. (See [Understand the `dataSource` options](backups-clone.md#understand-the-datasource-options) for more information about these options.)
    3. Under `spec.backups.pgbackrest`, use a **different** `repo1-path` than the Crunchy cluster so new backups do not overwrite the migration archive.

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
            # Must exactly match the pgBackrest settings defined in Crunchy `spec.backups.pgbackrest.global.repo1-path` 
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
    kubectl apply -f deploy/cr-cluster1-restore.yaml -n "${NAMESPACE}"
    ```

3. Wait until the cluster reports the `Ready` state:

    ```bash
    kubectl wait perconapgcluster/cluster1 \
      -n "${NAMESPACE}" \
      --for=jsonpath='{.status.state}'=ready \
      --timeout=300s
    ```

    The Percona Operator deploys the cluster and bootstraps it from the storage referenced in the `dataSource` section.

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

1. Edit the `deploy/backup.yaml` configuration file:

    ```yaml
    apiVersion: pgv2.percona.com/v2
    kind: PerconaPGBackup
    metadata:
      name: post-migration-backup
    spec:
      pgCluster: cluster1
      repoName: repo1
    ```

2. Apply the configuration to start the backup:
   
    ```bash
    kubectl apply -f deploy/post-migration-backup.yaml -n "${NAMESPACE}"
    ```

3. Wait for the backup job to complete:

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

## Decommission the Crunchy cluster

After traffic runs on Percona and you are satisfied with validation, you can delete the Crunchy PostgreSQL cluster:

```bash
kubectl delete postgrescluster crunchy-source -n "${CRUNCHY_NS}"
```

Uninstall Crunchy Operator from its namespace when no `PostgresCluster` resources remain.

## Rollback

Until you move write traffic to `cluster1`, rollback is to point applications back at the Crunchy `pgBouncer` Service. After cutover, new writes exist only on Percona; reconciling them back to Crunchy is a manual process.

After you delete the `crunchy-source` cluster, rollback means restoring a new Crunchy cluster from the **original** `repo1` content in object storage, if you still have that repository.

## Troubleshooting

### `archive.info` missing or restore errors

The value of `spec.dataSource.pgbackrest.global.repo1-path` must match the Crunchy cluster’s `spec.backups.pgbackrest.global.repo1-path` exactly.

```bash
kubectl get postgrescluster crunchy-source -n "${CRUNCHY_NS}" \
  -o jsonpath='{.spec.backups.pgbackrest.global.repo1-path}{"\n"}'

kubectl get perconapgcluster cluster1 -n "${NAMESPACE}" \
  -o jsonpath='{.spec.dataSource.pgbackrest.global.repo1-path}{"\n"}'
```

### Restore job failures (TLS, endpoint)

`pgBackRest` uses HTTPS for S3-compatible endpoints. Fix TLS trust (correct CA or `repo1-s3-verify-tls`) and confirm network reachability from the restore Pod to the bucket endpoint. See [Configure backup storage](backups-storage.md).

### Cluster stuck in restore

Inspect restore Pods or Jobs and `pgBackRest` logs:

```bash
kubectl logs \
  -l postgres-operator.crunchydata.com/cluster=cluster1,postgres-operator.crunchydata.com/pgbackrest-restore=cluster1 \
  -n "${NAMESPACE}" \
  -c pgbackrest
```

### Wrong or incomplete data

If you need a fresher cutover point, stop writes, take another full backup on Crunchy, delete `cluster1` on Percona, and re-apply the restore manifest so it bootstraps again from the newer backup.


