# Upgrade using backup and restore

This method allows you to migrate from the version 1.x to version 2.x cluster by restoring (actually creating) a new version 2.x PostgreSQL cluster using a backup from the version 1.x cluster.

!!! note

    To make sure that all transactions are captured in the backup, you need to stop the old cluster. This brings downtime to the application.


## Prepare the backup {.power-number}

1. Create the backup on the version 1.x cluster, following the [official guide for manual (on-demand) backups](https://docs.percona.com/percona-operator-for-postgresql/1.0/backups.html#making-on-demand-backup).
    This involves preparing the manifest in YAML and applying it in the ususal way:

    ```{.bash data-prompt="$"}
    $ kubectl apply -f deploy/backup/backup.yaml
    ```

2. [Pause](https://docs.percona.com/percona-operator-for-postgresql/1.0/pause.html) or delete the version 1.x cluster to ensure that you have the latest data.
    
    
    !!! warning 
    
        Before deleting the cluster, make sure that the [spec.keepBackups](https://docs.percona.com/percona-operator-for-postgresql/1.0/operator.html#spec-keepbackups) Custom Resource option is set to `true`.
        When it's set, local backups will be kept after the cluster deletion, so you can proceed with deleting your cluster as follows:

        ```{.bash data-prompt="$"}
        $ kubectl delete perconapgcluster cluster1
        ```

## Restore the backup as a version 2.x cluster

**Restore from S3 / Google Cloud Storage for backups repository**
{.power-number}

1. To restore from the S3 or Google Cloud Storage for backups (GCS) repository, you should first configure the `spec.backups.pgbackrest.repos`
    subsection in your version 2.x cluster Custom Resource to point to the backup storage system. Just follow the repository documentation instruction for
    [S3](backups.md#configuring-the-s3-compatible-backup-storage) or [GCS](backups.md#use-google-cloud-storage-for-backups).
    For example, for GCS you can define the repository similar to the following:

    ```yaml
    spec:
      backups:
        pgbackrest:
          repos:
          - name: repo1
            gcs:
              bucket: MY-BUCKET
              region: us-central1
    ```

2. Create and configure any required Secrets or desired custom pgBackrest configuration as described in [the backup documentation for te Operator version 2.x](backups.md).

3. Set the repository path in the `backups.pgbackrest.global` subsection. By default it is `/backrestrepo/&lt;clusterName>-backrest-shared-repo`:

    ```yaml
      spec:
      backups:
        pgbackrest:
          global:
            repo1: /backrestrepo/cluster1-backrest-shared-repo
    ```

4. Set the `spec.dataSource` option to create the version 2.x cluster from the specific repository:
 
    ```yaml
    spec:
      dataSource:
        postgresCluster:
          repoName: repo1
    ```

    You can also provide other pgBackRest restore options, e.g. if you wish to restore to a specific [point-in-time (PITR)](backups.md#restore-the-cluster-with-point-in-time-recovery).

5. Create the version 2.x cluster:

    ```{.bash data-prompt="$"}
    $ kubectl apply -f cr.yaml
    ```

