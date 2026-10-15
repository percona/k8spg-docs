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
2. The Percona cluster can reach the Crunchy primary Service for streaming replication. If both clusters run in the same Kubernetes cluster, the `<clusterName>-ha` Service is reachable from other namespaces and needs no changes. If they run in different Kubernetes clusters, expose the Service outside the cluster, for example with `spec.service.type: LoadBalancer` in the `PostgresCluster` Custom Resource.

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

5. Wait until all PostgreSQL instances of the cluster are ready. Set the number to the `replicas` value of the `instance1` instance set (`3` in this example):
   
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

## Make a full backup on the Crunchy PostgreSQL cluster before the migration

Make a full backup. This ensures the standby cluster has a recent restore point and needs to replay a small amount of WAL files to synchronize.

1. Start a full backup of your Crunchy PostgreSQL cluster. The annotation value identifies this backup request, so save it in a variable:

    ```bash
    BACKUP_ID=$(date +%s)
    kubectl annotate postgrescluster.postgres-operator.crunchydata.com crunchy-source \
      --namespace "${CRUNCHY_NS}" \
      --overwrite \
      postgres-operator.crunchydata.com/pgbackrest-backup="${BACKUP_ID}"
    ```

    The `--overwrite` flag lets you re-run the command if the cluster already has this annotation from an earlier backup.

2. Wait until the Crunchy Operator picks up this backup request:

    ```bash
    kubectl wait postgrescluster.postgres-operator.crunchydata.com/crunchy-source \
      -n "${CRUNCHY_NS}" \
      --for=jsonpath='{.status.pgbackrest.manualBackup.id}'="${BACKUP_ID}" \
      --timeout=120s
    ```

3. Wait for the backup to finish:

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

4. Check that the backup succeeded:

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
   
## Export data for the standby cluster

If the Percona cluster runs in a **different** namespace than Crunchy, copy the Crunchy TLS secrets into the Percona namespace for mutual TLS on the replication connection:

1. Retrieve the Secrets:
    
    ```bash
    kubectl get secrets -n $CRUNCHY_NS
    ```

    ??? example "Expected output"

        ```{.text .no-copy}
        crunchy-pgbackrest-secret             Opaque               1      7h29m
        crunchy-source-cluster-cert           Opaque               3      7h29m
        crunchy-source-instance1-khbq-certs   Opaque               6      7h29m
        crunchy-source-instance1-ndrp-certs   Opaque               6      7h29m
        crunchy-source-instance1-xlh6-certs   Opaque               6      7h29m
        crunchy-source-pgbackrest             Opaque               3      7h29m
        crunchy-source-pgbouncer              Opaque               6      7h29m
        crunchy-source-pguser-crunchy-source           Opaque               12     7h29m
        crunchy-source-replication-cert       Opaque               3      7h29m
        pgo-root-cacert                       Opaque               2      7h29m
        ```

    The Secrets we are interested in are `crunchy-source-cluster-cert` and `crunchy-source-replication-cert`

2. Export Secrets to a file:
    
    ```bash 
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
        * Specify the name of the service of the Crunchy PostgreSQL to stream data from. The Service name follows the pattern `<service-name>.<namespace>.svc.cluster.local`. 
        * Specify the port of this service.
        
        Replace example names such as `crunchy-source-ha`,
           `crunchy-source-pgbackrest`, and `cluster1-pgbouncer` if you use
           different cluster names. The service name `crunchy-source-ha` in
           the following example is derived from the source `PostgresCluster`
           name `crunchy-source`. Replace `<CRUNCHY_NS>` with the namespace of the Crunchy cluster.
      
          ```yaml
          standby:
           enabled: true                     
           host: crunchy-source-ha.<CRUNCHY_NS>.svc.cluster.local
           port: 5432
           repoName: repo1
          ```

    * For the mutual TLS communication, reference the TLS Secrets you created for the `secrets.customTLSSecret` and `secrets.customReplicationTLSSecret` options

        ```yaml
        secrets:
          customTLSSecret:
            name: crunchy-source-cluster-cert 
          customReplicationTLSSecret:
            name: crunchy-source-replication-cert 
        ```

        !!! warning "pgBouncer doesn't work while the cluster uses the Crunchy certificates"

            The Crunchy server certificate is issued only for the `crunchy-source-primary` and `crunchy-source-replicas` host names. With this certificate, Percona pgBouncer service `cluster1-pgbouncer` can't connect to PostgreSQL, and clients that connect to `cluster1-primary` with `sslmode=verify-full` fail on the host name check. The Operator also doesn't renew these certificates. They expire one year after Crunchy issued them.

            Keep these certificates only for the migration. After the cutover, [switch the cluster to Operator-managed certificates](#switch-to-operator-managed-tls-certificates).
    
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
    
    * Export the standby leader Pod as an environment variable. The standby leader replicates from Crunchy, and the other Pods replicate from it. The Operator labels the standby leader with `role=primary`:

       ```bash
       STANDBY_POD=$(kubectl get pod -n "${NAMESPACE}" \
       -l postgres-operator.crunchydata.com/cluster=cluster1,postgres-operator.crunchydata.com/role=primary \
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
        SELECT application_name, client_addr, state,
               pg_wal_lsn_diff(sent_lsn, replay_lsn) AS byte_lag,
               write_lag, flush_lag, replay_lag
        FROM pg_stat_replication;
      "
    ```

    The output also lists the Crunchy replicas. The Percona standby leader is the row whose `application_name` starts with `cluster1-instance1`.

    ??? example "Sample output"

        ```{.text .no-copy}
           application_name         | client_addr |   state   | byte_lag |    write_lag    |    flush_lag    |   replay_lag
        ----------------------------+-------------+-----------+----------+-----------------+-----------------+-----------------
         crunchy-source-instance1-n642-0 | 10.76.0.6   | streaming |        0 | 00:00:00.004238 | 00:00:00.00733  | 00:00:00.009044
         crunchy-source-instance1-shr4-0 | 10.76.2.9   | streaming |        0 | 00:00:00.011289 | 00:00:00.013495 | 00:00:00.014209
         cluster1-instance1-lfnc-0       | 10.76.2.11  | streaming |        0 | 00:00:00.001273 | 00:00:00.002045 | 00:00:00.002287
        (3 rows)
        ```

Proceed only when `write_lag` and `replay_lag` are null or within your policy (for example a few seconds).

## Cut over the Crunchy PostgreSQL cluster

Now you are ready for the cutover. Note that this step causes downtime as both clusters will be in standby mode and will not accept writes.

1. Patch the Crunchy PostgreSQL cluster to the standby mode. Patroni shuts down the primary cleanly, which archives its last WAL segment to the shared repository. The `repoName` option makes Crunchy a standby that follows this repository, which is what [Rollback](#rollback) relies on:

    ```bash
    kubectl patch postgrescluster crunchy-source \
      -n $CRUNCHY_NS \
      --type=merge \
      -p '{"spec": {"standby": {"enabled": true, "repoName": "repo1"}}}'
    ```

2. Wait until the former primary reports recovery. Right after the patch, the check can still return `f` or a connection error for a few seconds while Patroni restarts PostgreSQL:

    ```bash
    until [ "$(kubectl -n "${CRUNCHY_NS}" exec "${CRUNCHY_PRIMARY}" -c database -- \
      psql -tAc 'SELECT pg_is_in_recovery();' 2>/dev/null)" = "t" ]; do
      echo "Waiting for ${CRUNCHY_PRIMARY} to enter recovery..."
      sleep 2
    done
    echo "${CRUNCHY_PRIMARY} is in recovery"
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

3. Wait until the cluster leaves recovery mode and accepts writes. Don't rely on the cluster `ready` status for this: it stays `ready` during the promotion, so `kubectl wait` for this status returns immediately.

    * Identify the primary Pod:
      
       ```bash
       PERCONA_PRIMARY=$(kubectl get pod -n $NAMESPACE \
        -l postgres-operator.crunchydata.com/cluster=cluster1,postgres-operator.crunchydata.com/role=primary \
        -o jsonpath='{.items[0].metadata.name}')
       ```
   
    * Check the recovery mode until the Pod reports `f`, which means the instance is read-write:
     
       ```bash
       until [ "$(kubectl -n "${NAMESPACE}" exec "${PERCONA_PRIMARY}" -c database -- \
         psql -tAc 'SELECT pg_is_in_recovery();' 2>/dev/null)" = "f" ]; do
         echo "Waiting for ${PERCONA_PRIMARY} to accept writes..."
         sleep 2
       done
       echo "${PERCONA_PRIMARY} accepts writes"
       ```

      The promotion usually takes a few seconds.
    

4. After promoting the Percona cluster, it is important to confirm that the `pgBackRest` stanza has been created. The stanza is required for managing backups and enabling restores. Without it, regular backup operations and recovery from backup will not be possible. Waiting for `stanzaCreated` to become `true` ensures that backup tooling has been initialized properly before proceeding.
   
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

After the promotion, `cluster1` still archives WAL to the repository path it shares with Crunchy, and the Operator has already taken an incremental backup there on top of Crunchy's full backup. Move `cluster1` to its own repository path and take a full backup there. This gives the Percona cluster backups that don't depend on the Crunchy archive.

!!! warning "This step ends the rollback window"

    After you change the repository path, Crunchy no longer receives the WAL from `cluster1`. If you roll back after this point, Crunchy doesn't get the writes made on `cluster1`. Do this step only when you no longer need [Rollback](#rollback). Until then, `cluster1` can keep using the shared path.

Do this step before you point applications to `cluster1`. The WAL that `cluster1` generates between the path change and the stanza creation isn't stored in either repository.

1. Change the repository path. Use a path that no other cluster uses:

    ```bash
    kubectl patch perconapgcluster cluster1 \
      -n "${NAMESPACE}" \
      --type=merge \
      -p '{"spec":{"backups":{"pgbackrest":{"global":{"repo1-path":"/percona/cluster1/repo1"}}}}}'
    ```

2. Wait until the `pgBackRest` configuration on the primary Pod shows the new path:

    ```bash
    until kubectl -n "${NAMESPACE}" exec "${PERCONA_PRIMARY}" -c database -- \
      grep -qE 'repo1-path *= */percona/cluster1/repo1$' /etc/pgbackrest/conf.d/pgbackrest_instance.conf 2>/dev/null; do
      echo "Waiting for the new repository path..."
      sleep 5
    done
    ```

3. Create the `pgBackRest` stanza in the new path. The Operator doesn't do it when only the path changes:

    ```bash
    kubectl -n "${NAMESPACE}" exec "${PERCONA_PRIMARY}" -c database -- \
      pgbackrest --stanza=db stanza-create
    ```

    Until the stanza exists, WAL archiving to the new path fails. In Operator versions 3.0.0 and 3.1.0, `pg_stat_archiver` doesn't show these failures, so don't use it to check archiving.

4. Wait until the repository host Pod also has the new path. Backups run from this Pod, and it gets the new configuration up to a minute later than the primary:

    ```bash
    until kubectl -n "${NAMESPACE}" exec cluster1-repo-host-0 -c pgbackrest -- \
      grep -qE 'repo1-path *= */percona/cluster1/repo1$' /etc/pgbackrest/conf.d/pgbackrest_repo.conf 2>/dev/null; do
      echo "Waiting for the repository host..."
      sleep 5
    done
    ```

Then take a full backup in the new path:

1. Create the `post-migration-backup.yaml` configuration file. Set `--type=full` in `options`: without it, `pgBackRest` makes an incremental backup on top of the last full backup in the repository.

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

## Switch to Operator-managed TLS certificates

The cluster still uses the TLS certificates imported from Crunchy. They don't cover the `cluster1` host names, so `cluster1-pgbouncer` can't connect to PostgreSQL, and the Operator doesn't renew them. Replace them with certificates that the Operator issues and renews.

Like the repository path change, this step ends the rollback window: replication between the clusters relies on the Crunchy certificates.

1. Remove the references to the Crunchy certificates from the cluster configuration:

    ```bash
    kubectl patch perconapgcluster cluster1 \
      -n "${NAMESPACE}" \
      --type=json \
      -p='[
        {"op":"remove","path":"/spec/secrets/customTLSSecret"},
        {"op":"remove","path":"/spec/secrets/customReplicationTLSSecret"}
      ]'
    ```

    The Operator creates the `cluster1-cluster-cert` and `cluster1-replication-cert` Secrets, restarts the pgBouncer Pods and then restarts the PostgreSQL Pods one by one.

2. Watch the PostgreSQL Pods:

    ```bash
    kubectl get pod -n "${NAMESPACE}" -w \
      -l postgres-operator.crunchydata.com/cluster=cluster1,postgres-operator.crunchydata.com/data=postgres
    ```

    The restart can stop after the first replica: the restarted replica trusts only the new certificate authority, so it can't connect to the primary that still uses the Crunchy certificate. The replica stays not ready, and its `database` container log shows `certificate verify failed`. If this happens, finish the switch manually:

    1. Delete the other replica Pod that still runs with the old certificates, so that it restarts with the new ones:

        ```bash
        kubectl delete pod <old-replica-pod> -n "${NAMESPACE}"
        ```

    2. The replicas with the new certificates can't stream from the primary, so they replay WAL only from the backup repository and lag behind. Patroni refuses a switchover to a lagging replica. Make the primary archive its current WAL file, then check that the lag of the replica you switch to is `0`:

        ```bash
        kubectl -n "${NAMESPACE}" exec "${PERCONA_PRIMARY}" -c database -- \
          psql -c "SELECT pg_switch_wal();"
        kubectl -n "${NAMESPACE}" exec "${PERCONA_PRIMARY}" -c database -- \
          patronictl list
        ```

        Repeat `patronictl list` until the replay lag of the replica (the last `Lag` column) shows `0`. The first `Lag` column can keep growing: the replica doesn't stream from the primary, so its received position doesn't move.

    3. Make the replica that runs with the new certificates the primary. Writes stop for about 10 seconds during the switchover:

        ```bash
        kubectl -n "${NAMESPACE}" exec "${PERCONA_PRIMARY}" -c database -- \
          patronictl switchover --candidate <new-replica-pod> --force
        ```

        Check the output for `Successfully switched over`. The command exits with code `0` even when the switchover fails, for example with `Switchover failed, details: 503`. In this case, repeat the previous step and try again.

        The Operator then restarts the former primary with the new certificates.

3. After all PostgreSQL Pods are restarted and ready, check that the cluster reports the `ready` state:

    ```bash
    kubectl get perconapgcluster cluster1 -n "${NAMESPACE}"
    ```

4. Check that clients can connect with full certificate verification. Save the certificate authority of the cluster to a file:

    ```bash
    kubectl get secret cluster1-cluster-cert -n "${NAMESPACE}" \
      -o jsonpath='{.data.ca\.crt}' | base64 --decode > cluster1-ca.crt
    ```

    Use this file as `sslrootcert` with `sslmode=verify-full` when you connect to `cluster1-primary` or `cluster1-pgbouncer`. Applications that trusted the Crunchy certificate authority must use this one instead.

## Update the application connection string 

After you migrated to Percona Operator for PostgreSQL, update your application connection string to use the new Percona cluster. If you must send traffic to `cluster1` before you [switch the TLS certificates](#switch-to-operator-managed-tls-certificates), use the `cluster1-primary` Service with `sslmode=require` instead of pgBouncer.

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

The standby path is the most rollback-friendly of the [migration options](migrate-from-crunchy.md): Crunchy and Percona share the same `pgBackRest` repository until you move `cluster1` to its own repository path.

### Before you move cluster1 to its own repository

You can return write traffic to Crunchy while `cluster1` still archives WAL to the shared repository and uses the Crunchy certificates. In other words, before you complete [Take a post-migration backup](#take-a-post-migration-backup) and [Switch to Operator-managed TLS certificates](#switch-to-operator-managed-tls-certificates). The Crunchy `PostgresCluster` must still exist.

**What happens to the writes made on `cluster1` after the promotion:**

* If the WAL of `cluster1` reaches the shared repository before Crunchy is promoted, Crunchy replays it, and these writes are on Crunchy after the rollback. This is the normal case when you follow the steps below and WAL archiving works. Don't copy these writes to Crunchy manually: you would duplicate them.
* If some of this WAL is missing from the repository, for example, because archiving failed or `cluster1` stopped without a clean shutdown, the writes in it are lost. Crunchy can then reuse sequence values that `cluster1` already used, and `cluster1` ends up on a timeline that diverged from Crunchy. In this case, delete `cluster1` and create it again as a standby.

To roll back, do the following:

1. Stop application writes to `cluster1`.

2. Put `cluster1` back into standby so it stops acting as the primary (Patroni will follow the Custom Resource). The `standby.host`, `standby.port`, and `standby.repoName` you configured earlier should still be present; merge only toggles standby on:

    ```bash
    kubectl patch perconapgcluster cluster1 \
      -n "${NAMESPACE}" \
      --type=merge \
      -p '{"spec": {"standby": {"enabled": true, "repoName": "repo1"}}}'
    ```

3. Wait until every `cluster1` Pod is in recovery. A single check right after the patch isn't enough: the primary keeps returning `f`, and then a connection error, for a few seconds while Patroni demotes it.

    ```bash
    for pod in $(kubectl get pod -n "${NAMESPACE}" -o name \
      -l postgres-operator.crunchydata.com/cluster=cluster1,postgres-operator.crunchydata.com/data=postgres); do
      until [ "$(kubectl -n "${NAMESPACE}" exec "${pod}" -c database -- \
        psql -tAc 'SELECT pg_is_in_recovery();' 2>/dev/null)" = "t" ]; do
        echo "Waiting for ${pod} to enter recovery..."
        sleep 2
      done
      echo "${pod} is in recovery"
    done
    ```

    !!! danger "Don't promote Crunchy while cluster1 is still a primary"

        If you take Crunchy out of standby while `cluster1` still accepts writes, both clusters accept writes and archive WAL to the same `pgBackRest` stanza on different timelines. Neither Operator reports an error. When `cluster1` later follows Crunchy again, `pg_rewind` discards the writes made on `cluster1` in the meantime.

4. Check that the last WAL of `cluster1` is in the shared repository. Find the current timeline of `cluster1` and compare it with the newest WAL file in the repository:

    ```bash
    kubectl -n "${NAMESPACE}" exec "${STANDBY_POD}" -c database -- \
      psql -tAc "SELECT lpad(to_hex(timeline_id), 8, '0') FROM pg_control_checkpoint();"

    kubectl -n "${NAMESPACE}" exec "${STANDBY_POD}" -c database -- \
      pgbackrest --stanza=db info
    ```

    `STANDBY_POD` is the Pod you set in [Deploy Percona Operator for PostgreSQL and PostgreSQL cluster in standby mode](#deploy-percona-operator-for-postgresql-and-postgresql-cluster-in-standby-mode). In the `pgbackrest info` output, find the line `wal archive min/max (<version>): <oldest>/<newest>`. The WAL file name after the `/` must start with this timeline, for example `00000004` for timeline `00000004`. If the newest file belongs to an older timeline, the WAL of `cluster1` isn't in the repository, and the writes made on `cluster1` will be lost after the rollback. Check WAL archiving on `cluster1` before you continue. In Operator versions 3.0.0 and 3.1.0, `pg_stat_archiver` doesn't show failed archive attempts, so use the `pgBackRest` output.

5. If you applied [(Optional) Shut down the Crunchy cluster](#optional-shut-down-the-crunchy-cluster), clear shutdown before promoting Crunchy again:

    ```bash
    kubectl patch postgrescluster crunchy-source \
      -n "${CRUNCHY_NS}" \
      --type=merge \
      -p '{"spec": {"shutdown": false}}'
    ```

6. Take Crunchy out of standby so Patroni can promote it back to primary:

    ```bash
    kubectl patch postgrescluster crunchy-source \
      -n "${CRUNCHY_NS}" \
      --type=merge \
      -p '{"spec": {"standby": {"enabled": false}}}'
    ```

7. Confirm roles: Crunchy should accept writes and `cluster1` should be in recovery until replication catches up. If you shut down Crunchy, its Pods start again first, and the primary appears after 15-30 seconds, so wait for it:

    ```bash
    until CRUNCHY_PRIMARY=$(kubectl get pod \
      -l postgres-operator.crunchydata.com/cluster=crunchy-source,postgres-operator.crunchydata.com/role=master \
      -n "${CRUNCHY_NS}" \
      -o jsonpath='{.items[0].metadata.name}' 2>/dev/null) && [ -n "${CRUNCHY_PRIMARY}" ]; do
      echo "Waiting for the Crunchy primary Pod..."
      sleep 2
    done

    until [ "$(kubectl -n "${CRUNCHY_NS}" exec "${CRUNCHY_PRIMARY}" -c database -- \
      psql -tAc 'SELECT pg_is_in_recovery();' 2>/dev/null)" = "f" ]; do
      echo "Waiting for ${CRUNCHY_PRIMARY} to accept writes..."
      sleep 2
    done
    echo "${CRUNCHY_PRIMARY} accepts writes"
    ```

    Check that `cluster1` follows Crunchy:

    ```bash
    kubectl -n "${NAMESPACE}" exec "${STANDBY_POD}" -c database -- \
      psql -t -c "SELECT pg_is_in_recovery();"
    ```

    You should see `t` on Percona while it follows Crunchy.

8. Restore the password of the Crunchy pgBouncer user. After the promotion, the Percona Operator set a new password for the `_crunchypgbouncer` role, and the rollback carried this password back to Crunchy. Until you restore it, the Crunchy pgBouncer fails to authenticate. Set the role password back to the value from the Crunchy pgBouncer Secret:

    ```bash
    VERIFIER=$(kubectl get secret crunchy-source-pgbouncer -n "${CRUNCHY_NS}" \
      -o jsonpath='{.data.pgbouncer-verifier}' | base64 --decode)
    kubectl -n "${CRUNCHY_NS}" exec "${CRUNCHY_PRIMARY}" -c database -- \
      psql -c "ALTER ROLE \"_crunchypgbouncer\" PASSWORD '${VERIFIER}';"
    ```

    pgBouncer keeps rejecting connections for about 30 seconds after the change with `server login has been failing`. This is pgBouncer's retry delay. Retry the connection after that.

9. Point applications back at the Crunchy `pgBouncer` Service:

    ```bash
    kubectl get service -n "${CRUNCHY_NS}" \
      -l postgres-operator.crunchydata.com/cluster=crunchy-source,postgres-operator.crunchydata.com/role=pgbouncer
    ```

!!! note "If you migrate to Percona again after a rollback"

    Step 8 sets the Crunchy password for `_crunchypgbouncer`, and `cluster1` replicates it. After you promote `cluster1` again, the Operator doesn't reset this password, so `cluster1-pgbouncer` fails to authenticate. After the promotion, set the password from the Percona pgBouncer Secret on the `cluster1` primary:

    ```bash
    VERIFIER=$(kubectl get secret cluster1-pgbouncer -n "${NAMESPACE}" \
      -o jsonpath='{.data.pgbouncer-verifier}' | base64 --decode)
    kubectl -n "${NAMESPACE}" exec "${PERCONA_PRIMARY}" -c database -- \
      psql -c "ALTER ROLE \"_crunchypgbouncer\" PASSWORD '${VERIFIER}';"
    ```

### After you move cluster1 to its own repository

After `cluster1` archives WAL to its own repository path, Crunchy no longer receives its writes. You should treat Crunchy as a historical reference, not a live paired primary.

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

The Percona standby connects to Crunchy as the PostgreSQL role `_crunchyrepl` using the replication TLS material. Ensure `crunchy-source-replication-cert` exists in `"${NAMESPACE}"` and matches what Crunchy generated (re-export from `"${CRUNCHY_NS}"` if you rotated certificates).

```bash
kubectl get secret crunchy-source-replication-cert -n "${NAMESPACE}"
```

Verify the `PerconaPGCluster` still references it under `secrets.customReplicationTLSSecret` and `secrets.customTLSSecret` as in [Deploy Percona Operator for PostgreSQL and PostgreSQL cluster in standby mode](#deploy-percona-operator-for-postgresql-and-postgresql-cluster-in-standby-mode).

### `pgBackRest` restore or WAL archive problems

Symptoms include failed restore Jobs, missing `archive.info`, or the standby never leaving base backup replay.

1. Confirm `repo1-path` is **identical** on Crunchy and on `cluster1` (for example `/crunchy-to-percona/repo1` in this guide). This applies until you [move `cluster1` to its own repository path](#take-a-post-migration-backup). After the move, the paths differ on purpose.

    ```bash
    kubectl get postgrescluster crunchy-source -n "${CRUNCHY_NS}" \
      -o jsonpath='{.spec.backups.pgbackrest.global.repo1-path}{"\n"}'

    kubectl get perconapgcluster cluster1 -n "${NAMESPACE}" \
      -o jsonpath='{.spec.backups.pgbackrest.global.repo1-path}{"\n"}'
    ```

2. Confirm both clusters use credentials that can read and write the same bucket (equivalent Secrets). See [Configure backup storage](backups-storage.md) for TLS flags such as `repo1-s3-verify-tls` and path-style settings.

3. From a throwaway Pod in `"${NAMESPACE}"`, verify object storage reachability with your endpoint, bucket, and keys (adapt for your provider):

    ```bash
    kubectl run s3-check \
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

    The command finishes quickly, so read its output from the Pod logs, and then delete the Pod:

    ```bash
    kubectl wait pod/s3-check -n "${NAMESPACE}" \
      --for=jsonpath='{.status.phase}'=Succeeded --timeout=120s
    kubectl logs s3-check -n "${NAMESPACE}"
    kubectl delete pod s3-check -n "${NAMESPACE}"
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
