# Migrate from Crunchy to Percona Operator for PostgreSQL using a standby cluster

A standby cluster is a PostgreSQL cluster that doesn't have a writable primary. Instead, it applies changes from backups or from streaming replication from another database that acts as the source.

Using a standby cluster when migrating your PostgreSQL workloads, you maintain a live, synchronized copy of your original Crunchy cluster in Percona Operator for PostgreSQL. This approach minimizes downtime and gives you a way to validate the new cluster before switching over.

In this migration guide, we deploy Percona Operator for PostgreSQL as a standby cluster for a Crunchy PostgreSQL cluster by using a combination of backup and streaming replication. This approach ensures a fast initial data sync and keeps your data up to date with minimal downtime during cutover. For more information about standby cluster types, see [standby cluster types](standby.md#types-of-standby-clusters).

Then we cut over the Crunchy PostgreSQL cluster and promote Percona Operator for PostgreSQL.

This migration provides minimal downtime that happens only during the cutover.

--8<-- "crunchy-pgo-version.txt"

## Before you migrate

Complete the [Pre-migration compatibility checks](migrate-checklist.md). Physical methods require a matching PostgreSQL major version and CPU architecture.


## Prerequisites

Ensure you have the following:

- A Kubernetes or OpenShift cluster with permissions to create namespaces, CRDs, Roles, and Deployments.
- [Helm](https://helm.sh/) 3.x.
- `kubectl` or `oc` command line tools
- [yq](https://github.com/mikefarah/yq) YAML processor.
- A remote backup storage reachable from Pods in both the Crunchy and Percona namespaces.


## Before you start

1. Create the namespaces for Crunchy Operator for PostgreSQL and Percona Operator for PostgreSQL and export them as the environment variables. If you already run Crunchy Operator for PostgreSQL, export its namespace as the environment variable.

    ```bash
    export CRUNCHY_NS=postgres-operator
    export NAMESPACE=pgo
    ```

2. Clone the repositories to edit the manifests during the migration setup:   
    
    - For Crunchy PostgreSQL Operator:
  
       ```bash
       git clone https://github.com/CrunchyData/postgres-operator.git
       ```
    
    - For Percona Operator for PostgreSQL:
       
       ```bash
       git clone -b v{{release}} https://github.com/percona/percona-postgresql-operator
       ```

## Deploy Crunchy Operator for PostgreSQL

Skip this step if you already run Crunchy Operator for PostgreSQL.

If you don't, install the Operator Deployment following the [official Crunchy documentation :octicons-link-external-16:](https://access.crunchydata.com/documentation/postgres-operator/5.8/quickstart).

## Adapt the configuration for Crunchy PostgreSQL cluster

Whether you are deploying a new Crunchy PostgreSQL cluster or already have one running, make sure that:

1. `pgBackRest` is configured to send backups to a remote storage that will be accessible by the Percona standby cluster.
2. The Crunchy PostgreSQL cluster is exposed for external access so that the Percona cluster can connect to it for streaming replication. This typically involves making the PostgreSQL HA service accessible over the network.

To meet these requirements, do the following:

1. Create a Secret containing the access credentials for your backup storage. This example configuration uses AWS S3 as the backup storage and the `repo1` as the `pgBackRest` repository for storing backups there:

    ```yaml title="storage-access.yaml"
    apiVersion: v1
    kind: Secret
    metadata:
      name: crunchy-pgbackrest-secret
    stringData:
      s3.conf: |
        [global]
        repo1-s3-key="<your-access-key>"
        repo1-s3-key-secret="<your-access-secret>"
    ```

    For more configuration examples for other storages, see [Configure backup storage](backups-storage.md) 

2. Apply the file to create the Secret:
    
    ```bash
    kubectl apply -f storage-access.yaml -n $CRUNCHY_NS
    ```

3. Edit the `PostgresCluster` Custom Resource configuration to include the following configuration:
    
    For `pgBackRest` configuration:
    
    * The name of the Secret 
    * The name of the bucket
    * The endpoint on the storage
    * The shared path for both Crunchy and Percona standby clusters
  
    For external access, specify the type `LoadBalancer` for the service.

    Here's the example configuration for Crunchy PostgreSQL cluster showing these important settings:

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
            repo1-s3-verify-tls: "n" # Skip if you use AWS S3
          repos:
            - name: repo1
              s3:
                bucket: <YOUR_BUCKET_HERE>
                endpoint: s3.amazonaws.com
                region: <YOUR_REGION_HERE>
      proxy:
        pgBouncer:
          replicas: 1
    ```

4. Apply the configuration to create the new or update the existing Crunchy PostgreSQL cluster:
    
    ```bash
    kubectl apply -f postgres.yaml -n $CRUNCHY_NS
    ```

5. Wait for the cluster to report the "Ready" status:
   
    ```bash
    kubectl wait pod \
        -l postgres-operator.crunchydata.com/cluster=crunchy-source,postgres-operator.crunchydata.com/data=postgres \
        -n "${CRUNCHY_NS}" \
        --for=condition=Ready \
        --timeout=300s
    ```

    ??? example "Sample output"

        ```{.text .no-copy}
        pod/crunchy-source-instance1-n642-0 condition met
        pod/crunchy-source-instance1-shr4-0 condition met
        pod/crunchy-source-instance1-xczk-0 condition met
        ```

## Make a full backup on the Crunchy PostgreSQL cluster before the migration

Make a full backup. This ensures the standby cluster has a recent restore point and needs to replay a small amount of WAL files to synchronize.


2. Make a full backup of your Crunchy PostgreSQL cluster:

    ```bash
    kubectl annotate postgrescluster crunchy-source \
      --namespace "${CRUNCHY_NS}" \
      postgres-operator.crunchydata.com/pgbackrest-backup="$(date +%s)"
    ```

3. Wait for the backup job to complete:

    ```bash
    kubectl wait job \
     -l postgres-operator.crunchydata.com/cluster=crunchy-source \
     -l postgres-operator.crunchydata.com/pgbackrest-backup=manual \
     -n "${CRUNCHY_NS}" \
     --for=condition=complete \
     --timeout=600s
    ```

    ??? example "Expected output"

        ```{.text .no-copy}
        job.batch/crunchy-source-backup-ntns condition met
        ```
   
## Export data for the standby cluster

If the Percona cluster runs in a **different** namespace than Crunchy, copy the Crunchy TLS secrets into the Percona namespace for mutual TLS on the replication connection:

1. Retrieve the Secrets:
    
    ```bash
    kubectl get secrets -n $CRUNCHY_NS
    ```

    ??? example "Expected output"

        ```{.text .no-copy}
        crunchy-source-cluster-cert           Opaque               3      7h29m
        crunchy-source-instance1-khbq-certs   Opaque               6      7h29m
        crunchy-source-instance1-ndrp-certs   Opaque               6      7h29m
        crunchy-source-instance1-xlh6-certs   Opaque               6      7h29m
        crunchy-source-pgbackrest             Opaque               3      7h29m
        crunchy-source-pgbouncer              Opaque               6      7h29m
        crunchy-source-pguser-crunchy-source           Opaque               12     7h29m
        crunchy-source-replication-cert       Opaque               3      7h29m
        ```

    The Secrets we are interested in are `crunchy-source-cluster-cert` and `crunchy-source-replication-cert`

2. Export Secrets to a file:
    
    ```
    kubectl get secret crunchy-source-cluster-cert -o json -n "$CRUNCHY_NS" \
      | yq -o yaml '
    {
      "apiVersion": .apiVersion,
      "kind": .kind,
      "data": .data,
      "metadata": {"name": .metadata.name},
      "type": .type
    }
    ' > ~/crunchy-source-cluster-cert.yaml

    kubectl get secret crunchy-source-replication-cert -o json -n "$CRUNCHY_NS" \
      | yq -o yaml '
    {
      "apiVersion": .apiVersion,
      "kind": .kind,
      "data": .data,
      "metadata": {"name": .metadata.name},
      "type": .type
    }
    ' > ~/crunchy-source-replication-cert.yaml
    ```

## Deploy Percona Operator for PostgreSQL and PostgreSQL cluster in standby mode

1. Deploy Percona Operator for PostgreSQL:

    ```bash
    kubectl apply --server-side -f https://raw.githubusercontent.com/percona/percona-postgresql-operator/v{{release}}/deploy/bundle.yaml -n $NAMESPACE
    ```

2. Import the TLS Secrets using the configuration files you created earlier:

    ```bash
    kubectl apply -f ~/crunchy-source-cluster-cert.yaml -n $NAMESPACE
    kubectl apply -f ~/crunchy-source-replication-cert.yaml -n $NAMESPACE
    ```

3. Create the shared Secret for the backup storage. You can reuse the same Secret configuration file from the [Adapt the configuration for Crunchy PostgreSQL cluster](#adapt-the-configuration-for-crunchy-postgresql-cluster) step:

    ```bash
    echo "apiVersion: v1   
    kind: Secret
    metadata:
      name: percona-pgbackrest-secret
    stringData:
      s3.conf: |
        [global]
        repo1-s3-key="<your-access-key>"
        repo1-s3-key-secret="<your-access-secret>"
    " | kubectl apply -n $NAMESPACE -f -
    ```

4. Edit the `deploy/cr.yaml` and specify the following configuration:
   
    * For the standby cluster:
  
        * Set `standby.enabled` to `true`.
        * Specify the repository name to restore from in the `standby.repoName` option.
        - Specify the name of the service of the Crunchy PostgreSQL to stream data from. The Service name follows the pattern `<service-name>.<namespace>.svc.cluster.local`. 
        * Specify the port of this service.
        
        Replace example names such as `crunchy-source-ha`,
           `crunchy-source-pgbackrest`, and `cluster1-pgbouncer` if you use
           different cluster names. The service name `crunchy-source-ha` in
           the following example is derived from the source `PostgresCluster`
           name `crunchy-source`.
      
          ```yaml
          standby:
           enabled: true                     
           host: crunchy-source-ha.postgres-operator.svc.cluster.local
           port: 5432
           repoName: repo1
          ```

    - For the mutual TLS communication, reference the TLS Secrets you created for the `secrets.customTLSSecret` and `secrets.customReplicationTLSSecret` options

       ```yaml
       secrets:
         customTLSSecret:
           name: crunchy-source-cluster-cert 
         customReplicationTLSSecret:
           name: crunchy-source-replication-cert 
       ```
    
    * Configure the backup storage to exactly match the configuration on the Crunchy PostgreSQL cluster:
  
       ```yaml
       backups:
           pgbackrest:
           ....
             configuration:
               - secret:
                   name: percona-pgbackrest-secret
             global:
               # Must match repo1-path in the Crunchy source cluster exactly.
               repo1-path: /crunchy-to-percona/repo1
               repo1-s3-uri-style: path
               repo1-s3-verify-tls: "n" # Skip for AWS S3
             repos:
               - name: repo1
                 s3:
                   bucket: <YOUR-BUCKET-HERE>
                   endpoint: s3.amazonaws.com
                   region: <YOUR-REGION-HERE>
        #The rest of your configuration
       ```

5. Create the Percona PostgreSQL cluster
    
    ```bash
    kubectl apply -f deploy/cr.yaml -n $NAMESPACE
    ```

    The Percona Operator deploys the cluster and:

    * Restores the base backup from the S3 bucket.
    * Replays WAL from S3 until it catches up with the live Crunchy cluster.
    * Switches to streaming replication from `crunchy-source-ha`.

6. Wait for the cluster to report the `Ready` status:

    ```bash
    kubectl wait perconapgcluster/cluster1 \
      -n $NAMESPACE \
      --for=jsonpath='{.status.state}'=ready \
      --timeout=600s
    ```

    ??? example "Expected output"

        ```{.text .no-copy}
        perconapgcluster.pgv2.percona.com/cluster1 condition met
        ```

7. Verify the data is replicated on the standby. 
    
    * Export one of the Pods as an environment variable

       ```bash
       STANDBY_POD=$(kubectl get pod -n "${NAMESPACE}" \
       -l postgres-operator.crunchydata.com/cluster=cluster1,postgres-operator.crunchydata.com/data=postgres \
       -o jsonpath='{.items[0].metadata.name}')
       ```
    
    * Connect to the pod and verify the cluster is replicating:

       ```bash
       kubectl -n "${NAMESPACE}" exec "${STANDBY_POD}" -c database -- \
       psql -t -c "SELECT pg_is_in_recovery(), pg_last_wal_replay_lsn();"
       ```
       
       You should see `t` for `pg_is_in_recovery()` and a non-null LSN.

    ??? example "Sample output"
           
        ```text
        t                 | 0/14000000
        ```

## Verify streaming replication lag before cutover

On the Crunchy **primary** Pod, confirm the Percona standby is connected and lag is acceptable:

1. Identify the primary:
    
    ```bash
    CRUNCHY_PRIMARY=$(kubectl get pod \
    -l postgres-operator.crunchydata.com/cluster=crunchy-source,postgres-operator.crunchydata.com/role=master \
      -n "${CRUNCHY_NS}" \
      -o jsonpath='{.items[0].metadata.name}')
    ```

2. Exec to the primary and verify the replication lag:
   
    ```bash
    kubectl -n "${CRUNCHY_NS}" exec "${CRUNCHY_PRIMARY}" -c database -- \
      psql -c "
        SELECT client_addr, state,
               pg_wal_lsn_diff(sent_lsn, replay_lsn) AS byte_lag,
               write_lag, flush_lag, replay_lag
        FROM pg_stat_replication;
      "
    ```

    ??? example "Sample output"

        ```{.text .no-copy}
        client_addr |   state   | byte_lag |    write_lag    |    flush_lag    |   replay_lag
        -------------+-----------+----------+-----------------+-----------------+-----------------
          10.76.0.6   | streaming |        0 | 00:00:00.004238 | 00:00:00.00733  | 00:00:00.009044
          10.76.2.9   | streaming |        0 | 00:00:00.011289 | 00:00:00.013495 | 00:00:00.014209
          10.76.2.11  | streaming |        0 | 00:00:00.001273 | 00:00:00.002045 | 00:00:00.002287
        (3 rows)
        ```

Proceed only when `write_lag` and `replay_lag` are null or within your policy (for example a few seconds).

## Cut over the Crunchy PostgreSQL cluster

Now you are ready for the cutover. Note that this step causes downtime as both clusters will be in standby mode and will not accept writes.

1. Patch the Crunchy PostgreSQL cluster to the standby mode. Specify `repo1` so that Patroni archives the final WAL:

    ```bash
    kubectl patch postgrescluster crunchy-source \
      -n $CRUNCHY_NS \
      --type=merge \
      -p '{"spec": {"standby": {"enabled": true, "repoName": "repo1"}}}'
    ```

2. Check that the former primary reports recovery:

    ```bash
    kubectl -n $CRUNCHY_NS exec "${CRUNCHY_PRIMARY}" -c database -- \
      psql -t -c "SELECT pg_is_in_recovery();"
    ```
    
    ??? example "Expected output"

        ```text
        t
        ```

## (Optional) Shut down the Crunchy cluster

After the Percona standby has replayed WAL, shut down Crunchy to avoid split-brain:

```bash
kubectl patch postgrescluster crunchy-source \
  -n $CRUNCHY_NS \
  --type=merge \
  -p '{"spec": {"shutdown": true}}'
```

## Promote Percona PostgreSQL cluster

Before promoting the Percona PostgreSQL cluster, make sure it has finished replaying all WAL (Write-Ahead Log) data. 

After the Crunchy cluster is shut down, no new WAL files will be generated. 
The Percona standby will keep replaying existing WAL files from S3 object storage, and its Log Sequence Number (LSN) will advance each time new WAL is applied.

Once the LSN value stops changing and stays the same across two consecutive checks, it means all available WAL has been replayed and it’s safe to promote the standby cluster to be the new primary.

1. Verify the Percona standby cluster has stopped replaying WAL files by running:
   
    ```bash
    kubectl -n "${NAMESPACE}" exec "${STANDBY_POD}" -c database -- \
      psql -t -c "SELECT pg_last_wal_replay_lsn();"
    ```

    Repeat this command several times until the LSN value stops advancing.

2. Promote the Percona PostgreSQL cluster to be the new primary by patching the cluster:

    ```bash
    kubectl patch perconapgcluster cluster1 \
      -n $NAMESPACE \
      --type=merge \
      -p '{"spec": {"standby": {"enabled": false}}}'
    ```

3. Wait for the cluster to report the `Ready` status:

    ```bash
    kubectl wait perconapgcluster/cluster1 \
      -n $NAMESPACE \
      --for=jsonpath='{.status.state}'=ready \
      --timeout=600s
    ```

4. Confirm the cluster is not in a recovery mode and can accept writes:

    * Identify the primary pod:
      
       ```bash
       PERCONA_PRIMARY=$(kubectl get pod -n $NAMESPACE \
        -l postgres-operator.crunchydata.com/cluster=cluster1,postgres-operator.crunchydata.com/role=primary \
        -o jsonpath='{.items[0].metadata.name}')
       ```
   
    * Connect to the Pod and check if it is in the recovery mode:
     
       ```bash
       kubectl -n $NAMESPACE exec "${PERCONA_PRIMARY}" -c database -- \
        psql -t -c "SELECT pg_is_in_recovery();"
       ```

      You should see `f`. This means the instance is read-write.
    

5. After promoting the Percona cluster, it is important to confirm that the `pgBackRest` stanza has been created. The stanza is required for managing backups and enabling restores; without it, regular backup operations and recovery from backup will not be possible. Waiting for `stanzaCreated` to become true ensures that backup tooling has been initialized properly before proceeding.
   
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

This creates a clean recovery point on the new timeline. Note that after you make the backup, you can no longer roll back to the Crunchy PostgreSQL.

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

## Update the application connection string 

After you migrated to Percona Operator for PostgreSQL, update your application connection string to use the new Percona cluster:

1. Get the `pgBouncer` service exposed by the Percona Operator:

    ```bash
    kubectl get service -n $NAMESPACE cluster1-pgbouncer
    ```

   The output will show the `cluster1-pgbouncer` service, along with its
   ClusterIP and port.

2. Update your application's connection string to use the `pgBouncer` service name (from the previous step) as the PostgreSQL host. For example:

    ```
    Host:   cluster1-pgbouncer.$NAMESPACE.svc.cluster.local
    Port:   5432
    ```

   Replace `${NAMESPACE}` with your cluster's namespace. Update your application configuration to point to this service, ensuring it now connects to your Percona Operator for PostgreSQL deployment.

## Rollback

The standby path is the most rollback-friendly of the [migration options](migrate-from-crunchy.md): Crunchy and Percona share the same `pgBackRest` repository layout until you establish a new baseline on Percona.

### Before the post-migration backup

Until you complete [Take a post-migration backup](#take-a-post-migration-backup), you can usually return write traffic to Crunchy if the Crunchy `PostgresCluster` and its `pgBouncer` Service still exist and you have **not** deleted `crunchy-source`.

Any writes that landed on `cluster1` **after** you promoted Percona are **not** on Crunchy. Treat rollback as abandoning that window unless you copy data out manually.

1. Stop application writes to `cluster1`.

2. Put `cluster1` back into standby so it stops acting as the primary (Patroni will follow the Custom Resource). The `standby.host`, `standby.port`, and `standby.repoName` you configured earlier should still be present; merge only toggles standby on:

    ```bash
    kubectl patch perconapgcluster cluster1 \
      -n "${NAMESPACE}" \
      --type=merge \
      -p '{"spec": {"standby": {"enabled": true, "repoName": "repo1"}}}'
    ```

3. If you applied [(Optional) Shut down the Crunchy cluster](#optional-shut-down-the-crunchy-cluster), clear shutdown before promoting Crunchy again:

    ```bash
    kubectl patch postgrescluster crunchy-source \
      -n "${CRUNCHY_NS}" \
      --type=merge \
      -p '{"spec": {"shutdown": false}}'
    ```

4. Take Crunchy out of standby so Patroni can promote it back to primary:

    ```bash
    kubectl patch postgrescluster crunchy-source \
      -n "${CRUNCHY_NS}" \
      --type=merge \
      -p '{"spec": {"standby": {"enabled": false}}}'
    ```

5. Confirm roles: Crunchy should accept writes and `cluster1` should be in recovery until replication catches up.

    ```bash
    CRUNCHY_PRIMARY=$(kubectl get pod \
      -l postgres-operator.crunchydata.com/cluster=crunchy-source,postgres-operator.crunchydata.com/role=master \
      -n "${CRUNCHY_NS}" \
      -o jsonpath='{.items[0].metadata.name}')

    kubectl -n "${CRUNCHY_NS}" exec "${CRUNCHY_PRIMARY}" -c database -- \
      psql -t -c "SELECT pg_is_in_recovery();"
    ```

    You should see `f` on Crunchy.

    ```bash
    STANDBY_POD=$(kubectl get pod -n "${NAMESPACE}" \
      -l postgres-operator.crunchydata.com/cluster=cluster1,postgres-operator.crunchydata.com/data=postgres \
      -o jsonpath='{.items[0].metadata.name}')

    kubectl -n "${NAMESPACE}" exec "${STANDBY_POD}" -c database -- \
      psql -t -c "SELECT pg_is_in_recovery();"
    ```

    You should see `t` on Percona while it follows Crunchy.

6. Point applications back at the Crunchy `pgBouncer` Service:

    ```bash
    kubectl get service -n "${CRUNCHY_NS}" \
      -l postgres-operator.crunchydata.com/cluster=crunchy-source,postgres-operator.crunchydata.com/role=pgbouncer
    ```

### After the post-migration backup

After you take the post-migration backup, timelines and `pgBackRest` history on Percona have diverged from the pre-cutover Crunchy archive. You should treat Crunchy as a historical reference, not a live paired primary.

Rolling back from here is the same idea as a fresh restore: deploy or restore a Crunchy cluster from the repository state you need, or follow [Migrate from Crunchy using backup and restore](migrate-from-crunchy-backup-restore.md) in reverse order for your environment. Plan the rollback **before** cutover if you require a guaranteed fast path.

## Troubleshooting

### Percona standby cannot resolve or reach the Crunchy primary

Confirm the PostgreSQL HA Service for `crunchy-source` resolves from the Percona database Pod. Replace `crunchy-source-ha` if your Service name differs.

```bash
kubectl -n "${NAMESPACE}" exec "${STANDBY_POD}" -c database -- \
  bash -c "getent hosts crunchy-source-ha.${CRUNCHY_NS}.svc.cluster.local"
```

If DNS fails, check Service names and namespaces. If DNS succeeds but TCP fails, check NetworkPolicies, service mesh rules, and firewalls between namespaces.

### Replication authentication errors

The Percona standby connects to Crunchy as the PostgreSQL role `_crunchyreplication` using the replication TLS material. Ensure `crunchy-source-replication-cert` exists in `"${NAMESPACE}"` and matches what Crunchy generated (re-export from `"${CRUNCHY_NS}"` if you rotated certificates).

```bash
kubectl get secret crunchy-source-replication-cert -n "${NAMESPACE}"
```

Verify the `PerconaPGCluster` still references it under `secrets.customReplicationTLSSecret` and `secrets.customTLSSecret` as in [Deploy Percona Operator for PostgreSQL and PostgreSQL cluster in standby mode](#deploy-percona-operator-for-postgresql-and-postgresql-cluster-in-standby-mode).

### `pgBackRest` restore or WAL archive problems

Symptoms include failed restore Jobs, missing `archive.info`, or the standby never leaving base backup replay.

1. Confirm `repo1-path` is **identical** on Crunchy and on `cluster1` (for example `/crunchy-to-percona/repo1` in this guide).

    ```bash
    kubectl get postgrescluster crunchy-source -n "${CRUNCHY_NS}" \
      -o jsonpath='{.spec.backups.pgbackrest.global.repo1-path}{"\n"}'

    kubectl get perconapgcluster cluster1 -n "${NAMESPACE}" \
      -o jsonpath='{.spec.backups.pgbackrest.global.repo1-path}{"\n"}'
    ```

2. Confirm both clusters use credentials that can read and write the same bucket (equivalent Secrets). See [Configure backup storage](backups-storage.md) for TLS flags such as `repo1-s3-verify-tls` and path-style settings.

3. From a throwaway Pod in `"${NAMESPACE}"`, verify object storage reachability with your endpoint, bucket, and keys (adapt for your provider):

    ```bash
    kubectl run -i --rm s3-check \
      --image=perconalab/awscli \
      --restart=Never \
      -n "${NAMESPACE}" \
      -- bash -c "
        AWS_ACCESS_KEY_ID='<your-access-key>' \
        AWS_SECRET_ACCESS_KEY='<your-secret-key>' \
        AWS_DEFAULT_REGION='<your-region>' \
        aws --endpoint-url 'https://<your-s3-endpoint>' \
            --no-verify-ssl \
            s3 ls s3://<your-bucket>
      "
    ```

### Timeline history file missing after promotion (Crunchy archive)

Some Crunchy PGO configurations using async archive mode can hit a missing timeline history file on the archive after promotion (see [Crunchy PGO issue #4472 :octicons-link-external-16:](https://github.com/CrunchyData/postgres-operator/issues/4472)). If `pgBackRest` or replicas complain about `*.history` on the archive, push the file once from the **new** primary:

```bash
kubectl -n "${NAMESPACE}" exec "${PERCONA_PRIMARY}" -c database -- \
  bash -c "
    pgbackrest --stanza=db --no-archive-async \
      archive-push \"\${PGDATA}/pg_wal/00000002.history\" || true
  "
```

Adjust the filename to match the timeline file reported in your logs.
