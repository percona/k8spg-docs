# Migrate using Standby

This method allows you to migrate from version 1,x to version 2.x by creating a new version 2.x PostgreSQL cluster in a "standby" mode, mirroring the version 1.x cluster to it continuously. This method can provide minimal downtime, but requires additional computing resources to run two clusters in parallel.

This method only works if the version 1.x cluster uses [Amazon S3 or S3-compatible storage](https://en.wikipedia.org/wiki/Amazon_S3#S3_API_and_competing_services), or [Google Cloud storage (GCS)](https://cloud.google.com/storage) for backups. For more information on standby clusters, please refer to [this article].


## Migrate to version 2

There is no need to perform any additional configuration on version 1.x cluster, you will only need to configure  the version 2.x one.

1. Configure `spec.backups.pgbackrest.repos` Custom Resource option to point to the backup storage system. For example, for GCS, the repository would be defined similar to the following:

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

2. Create and configure any required secrets or desired custom pgBackrest configuration as described in [the backup documentation for the version 2.x](backups.md).

3. Set the repository path in `backups.pgbackrest.global` section of the Custom Resource configuration file. By default it will be `/backrestrepo/&lt;clusterName>-backrest-shared-repo`:

    ```yaml
          spec:
          backups:
            pgbackrest:
              global:
                repo1: /backrestrepo/cluster1-backrest-shared-repo
    ```

4. Enable the standby mode in `spec.standby` and point to the repository:

    ```yaml
    spec:
      standby:
        enabled: true
        repoName: repo1
    ```

5. Create the version 2.x cluster:

    ```{.bash data-prompt="$"}
    $ kubectl apply -f deploy/cr.yaml
    ```

## Promote version 2.x cluster

Once the standby cluster is up and running, you can promote it.

1. Delete version 1.x cluster, but ensure that `spec.keepBackups` is set to `true`.

    ```{.bash data-prompt="$"}
    $ kubectl delete perconapgcluster cluster1
    ```

2. Promote version 2.x cluster by disabling the standby mode:

    ```yaml
    spec:
      standby:
        enabled: false
    ```

You can use version 2.x cluster now. Also the 2.x version is now managing the object storage with backups, so you should not start your old cluster.

## Create the replication user

Right after disabling standby, run the following SQL commands as a PostgreSQL superuser. For example, you can login as the `postgres` user, or exec into the Pod and use `psql`:

- add the managed replication user
    
   ```sql
   CREATE ROLE _crunchyrepl WITH LOGIN REPLICATION;
   ```

- allow for the replication user to execute the functions required as part of "rewinding"

   ```sql
   GRANT EXECUTE ON function pg_catalog.pg_ls_dir(text, boolean, boolean) TO _crunchyrepl;
   GRANT EXECUTE ON function pg_catalog.pg_stat_file(text, boolean) TO _crunchyrepl;
   GRANT EXECUTE ON function pg_catalog.pg_read_binary_file(text) TO _crunchyrepl;
   GRANT EXECUTE ON function pg_catalog.pg_read_binary_file(text, bigint, bigint, boolean) TO _crunchyrepl;
   ```

The above step will be automated in upcoming releases.
