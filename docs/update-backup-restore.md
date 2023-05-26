# Upgrade using backup and restore

This method allows you to migrate from v1 to v2 cluster by creating a new v2 PostgreSQL cluster using a backup from v1 cluster.

To make sure that all transactions are captured in the backup, you would need to stop the old cluster. This will bring downtime to the application.


## Prepare the backup

1. Create the backup manually by applying the manifest. Read more about manual backups in [our documentation](backups.md#making-on-demand-backup).

    ```{.bash data-prompt="$"}
    $ kubectl apply -f deploy/backup/backup.yaml
    ```

2. To ensure that you have the latest data, delete or pause the v1 cluster. If you delete the cluster, make sure that `spec.keepBackups` is set to `true`.

    ```{.bash data-prompt="$"}
    $ kubectl delete perconapgcluster cluster1
    ```

## Restore from backup to v2 cluster

**Restore from S3 / GCS repository**

1. To restore from S3 or GCS repository, configure `spec.backups.pgbackrest.repos` to point to the backup storage system. For example, for GCS, define the repository similar to the following:

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


2. Create and configure any required secrets or desired custom pgBackrest configuration as described in [the backup documentation for v2](https://docs.percona.com/percona-operator-for-postgresql/2.0/backups.html).

3. Set the repository path in `backups.pgbackrest.global` section. By default it is `/backrestrepo/&lt;clusterName>-backrest-shared-repo`:

    ```yaml
      spec:
      backups:
        pgbackrest:
          global:
            repo1: /backrestrepo/cluster1-backrest-shared-repo
    ```

4. Set the `spec.dataSource` to create the v2 cluster from the specific repository:
 
    ```yaml
    spec:
      dataSource:
        postgresCluster:
          repoName: repo1
    ```

    You can also provide other pgBackRest restore options, e.g. if you wish to restore to a specific point-in-time (PITR).

5. Create the v2 cluster:

    ```{.bash data-prompt="$"}
    $ kubectl apply -f cr.yaml
    ```

