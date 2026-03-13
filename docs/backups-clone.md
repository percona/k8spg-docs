# Restore the backup to a new cluster (cluster clone)

Apart from [restoring the data on the same database cluster](backups-restore-inplace.md), you can restore a backup to a new cluster and run it alongside the existing one.

This is useful for:

* Cloning a cluster to a new namespace or Kubernetes environment
* Creating a copy for development, testing, or reporting
* Restoring from a cloud storage when the source cluster no longer exists

You can make a full restore or restore the database to a specific point in time. For each restore scenario, you must define the Custom Resource for a **new** cluster with these configuration options:

* `dataSource` section - where to take the data from
*  `backups` section. The new cluster needs its own backup configuration.

## Understand the `dataSource` options

The `dataSource` section in the Custom Resource includes two subsections: `dataSource.postgresCluster` and `dataSource.pgbackrest`.

!!! note

    You cannot use both `dataSource.postgresCluster` and `dataSource.pgbackrest` at the same time. If both are present in the Custom Resource, the `dataSource.postgresCluster` option will take precedence and the Operator will use it to restore the data.

### `dataSource.postgresCluster` 

Configure this subsection **to clone an existing cluster**. The key options are:

* `dataSource.postgresCluster.clusterName` is the name of the cluster you restore from. This is the source cluster. The option value corresponds to the `metadata.name` of the source cluster Custom Resource.

* `dataSource.postgresCluster.clusterNamespace` is the namespace where the source cluster is deployed. Use it if namespaces of source and new clusters differ.

* `dataSource.postgresCluster.repoName` is the name of the `pgBackRest` repository on the source cluster where the backup you restore from is located. It must exist on the source.

* `dataSource.postgresCluster.options` are additional `pgBackRest` options that you pass for the restore. For example, you configure them for point-in-time recovery.

Read more about all available options in the [Custom Resource reference](operator.md#datasource-subsection)

### `dataSource.pgbackrest`

Configure this subsection **to restore from backup repository stored in a cloud storage**.

Its structure closely matches the source cluster's `backups.pgbackrest` section, with these main points:

* Define the backup source using a single `repo` object (not an array as in `backups.pgbackrest`).
* Specify `stanza` (usually `db`), required to identify the backup.
* Reference the same Secret for cloud credentials in both the restore and backup configuration.

Key options are:

* `dataSource.pgbackrest.stanza` - the name of `pgBackRest` stanza - a unique identifier for a source PostgreSQL cluster's backup configuration

* `dataSource.pgbackrest.configuration.secret.name` - the name of the Secret object with the credentials to the cloud storage. It must be the same in both source and new clusters because the restore Pod requires the same credentials as the original backup Pod.

* `dataSource.pgbackrest.global` is the location of a backup.

* `dataSource.pgbackrest.repo` is the name of the `pgBackRest` repository. It is the same on both source and new clusters.

For all options, see the [Custom Resource reference](operator.md#datasourcepgbackrestconfigurationsecretname).

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

For Google Cloud Storage or Azure Blob Storage, use the same structure but replace the `repo.s3` block with `repo.gcs` or `repo.azure` and the matching configuration. See [Configure storage for backups](backups-storage.md) for examples.
