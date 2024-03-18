# 4 Make a backup

Now your database [contains some data](data-insert.md), so it's a good time to learn how to manually make a full backup of your data with the Operator. 

!!! note 

    If you are interested to learn more about backups, their types and retention policy, see the [Backups section](backups.md).

## Considerations and prerequisites

* In this tutorial we use the [AWS S3 :octicons-link-external-16:](https://aws.amazon.com/s3/) as the backup storage. You need the following S3-related information:

    * The name of S3 bucket;
    * The endpoint - the URL to access the bucket
    * The region - the location of the bucket
    * S3 credentials such as S3 key and secret to access the storage.

    If you don't have access to AWS, you can use any S3-compatible storage like [MinIO :octicons-link-external-16:](https://min.io/docs/minio/linux/index.html). Also check the list of [supported storages](backups.md#backup-storage).

* The Operator uses the [`pgBackRest` :octicons-link-external-16:](https://pgbackrest.org/) tool to make backups. `pgBackRest` stores the backups and archives WAL segments in repositories. The Operator has up to four `pgBackRest` repositories named `repo1`, `repo2`, `repo3` and `repo4`. In this tutorial we use `repo2` for backups.

* Also, we will use some files from the Operator repository for setting up
    backups. So, clone the percona-postgresql-operator repository:

    ``` {.bash data-prompt="$" }
    $ git clone -b v{{ release }} https://github.com/percona/percona-postgresql-operator
    $ cd percona-postgresql-operator
    ```

    !!! note

        It is important to specify the right branch with `-b` option while
        cloning the code on this step. Please be careful.

## Configure backup storage {.power-number}

1. Encode the S3 credentials and the pgBackRest repository name (`repo2` in our setup).

    === ":simple-linux: Linux"

         ``` {.bash data-prompt="$" }
         $ cat <<EOF | base64 --wrap=0
         [global]
         repo2-s3-key=<YOUR_AWS_S3_KEY>
         repo2-s3-key-secret=<YOUR_AWS_S3_KEY_SECRET>
         EOF
         ```     

    === ":simple-apple: macOS"

         ``` {.bash data-prompt="$" }
         $ cat <<EOF | base64
         [global]
         repo2-s3-key=<YOUR_AWS_S3_KEY>
         repo2-s3-key-secret=<YOUR_AWS_S3_KEY_SECRET>
         EOF
         ```

2. Create the Secret configuration file and specify the base64-encoded string from the previous step. The following is the example of the  `cluster1-pgbackrest-secrets.yaml` Secret file:

    ```yaml
    apiVersion: v1
    kind: Secret
    metadata:
      name: cluster1-pgbackrest-secrets
    type: Opaque
    data:
      s3.conf: <base64-encoded-configuration-contents>
    ```

3. Create the Secrets object from this yaml file. Specify your namespace instead of the `<namespace>` placeholder:

    ``` {.bash data-prompt="$" }
    $ kubectl apply -f cluster1-pgbackrest-secrets.yaml -n <namespace>
    ```

4. Update your `deploy/cr.yaml` configuration. Specify the Secret file you created in the `backups.pgbackrest.configuration` subsection, and put all other S3 related information in the `backups.pgbackrest.repos` subsection under the repository name that you intend to use for backups. This name must match the name you used when you encoded S3 credentials on step 1.

    For example, the S3 storage for the `repo2` repository looks as follows:

    ```yaml
    ...
    backups:
      pgbackrest:
        ...
        configuration:
          - secret:
              name: cluster1-pgbackrest-secrets
        ...
        repos:
        - name: repo2
          s3:
            bucket: "<YOUR_AWS_S3_BUCKET_NAME>"
            endpoint: "<YOUR_AWS_S3_ENDPOINT>"
            region: "<YOUR_AWS_S3_REGION>"
    ```

5. Create or update the cluster. Specify your namespace instead of the `<namespace>` placeholder:

    ``` {.bash data-prompt="$" }
    $ kubectl apply -f deploy/cr.yaml
    ``` 

## Make a backup 

For manual backups, you need a backup configuration file.
{.power-number}

1. Edit the example backup configuration file [deploy/backup.yaml :octicons-link-external-16:](https://github.com/percona/percona-postgresql-operator/blob/main/deploy/backup.yaml). Specify your cluster name and the `repo` name.

    ```yaml
    apiVersion: pgv2.percona.com/v2
    kind: PerconaPGBackup
    metadata:
      name: backup1
    spec:
      pgCluster: cluster2
      repoName: repo1
    #  options:
    #  - --type=full
    ```

2. Apply the configuration. This instructs the Operator to start a backup.

    ``` {.bash data-prompt="$" }
    $ kubectl apply -f deploy/backup.yaml -n <namespace>
    ```

3. List the backup

    ``` {.bash data-prompt="$" }
    $ kubectl get pg-backup -n <namespace>
    ```

Congratulations! You have made the first backup manually. Want to learn more about backups? See the [Backup and restore section](backups.md) for details like types, retention and how to [automatically make backups according to the schedule](backups-schedule.md).

## Next steps

[:material-monitor-dashboard: Monitor the database :material-arrow-right:](monitoring.md){.md-button}
