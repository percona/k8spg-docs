# Configure backup storage

Configure backup storage for your [backup repositories](backups.md#backup-repositories) in the `backups.pgbackrest.repos` section of the `deploy/cr.yaml` configuration file.

Follow the instructions relevant to the cloud storage or Persistent Volume you are using for backups.

=== ":simple-amazons3: S3-compatible backup storage"

    To use [Amazon S3 :octicons-link-external-16:](https://aws.amazon.com/s3/) or any [S3-compatible storage :octicons-link-external-16:](https://en.wikipedia.org/wiki/Amazon_S3#S3_API_and_competing_services) for backups, you need to have the following S3-related information:

    * The name of S3 bucket;
    * The region - the location of the bucket
    * S3 credentials such as S3 key and secret to access the storage. These are stored in an encoded form in [Kubernetes Secrets :octicons-link-external-16:](https://kubernetes.io/docs/concepts/configuration/secret/) along with other sensitive information. 
    * For S3-compatible storage other than native Amazon S3, you will also need to specify the endpoint - the actual URI to access the bucket - and the URI style (see below).

    !!! note

        The pgBackRest tool does backups based on write-ahead logs (WAL) archiving.
        If you are using an S3 storage in a region located far away from the region of your PostgreSQL cluster deployment, it could lead to the delay and impossibility to create a new replica/join delayed replica if the primary restarts. A new WAL file is archived in 60 seconds at the backup start [by default :octicons-link-external-16:](https://www.postgresql.org/docs/current/runtime-config-wal.html#GUC-ARCHIVE-TIMEOUT), causing both full and incremental backups fail in case of long delay.

        To prevent issues with PostgreSQL archiving and have faster restores, it's recommended to use the same S3 region for both the Operator and backup options. Additionally, you can replicate the S3 bucket to another region with tools like [Amazon S3 Cross Region Replication :octicons-link-external-16:](https://docs.aws.amazon.com/AmazonS3/latest/userguide/replication.html).

    **Configuration steps**
    {.power-number}

    1. Encode the S3 credentials and the pgBackRest repository name that you will use for backups. In this example, we use AWS S3 key and S3 key secret and `repo2`. 

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

        !!! note     

            This Secret can store credentials for several repositories presented as
            separate data keys.     

    3. Create the Secrets object from this YAML file. Replace the `<namespace>` placeholder with your value:

        ``` {.bash data-prompt="$" }
        $ kubectl apply -f cluster1-pgbackrest-secrets.yaml -n <namespace>
        ```     

    4. Update your `deploy/cr.yaml` configuration. Specify the Secret file you created in the `backups.pgbackrest.configuration` subsection, and put all other S3 related information in the `backups.pgbackrest.repos` subsection under the repository name that you intend to use for backups. This name must match the name you used when you encoded S3 credentials on step 1.

        Provide pgBackRest the directory path for backup on the storage. You can pass it in the [backups.pgbackrest.global](https://docs.percona.com/percona-operator-for-postgresql/2.0/operator.html#backups-pgbackrest-global) subsection via the pgBackRest `path` option (prefix it's name with the repository name, for example `repo1-path`). Also, if your S3-compatible storage requires additional [repository options :octicons-link-external-16:](https://pgbackrest.org/configuration.html#section-repository) for the pgBackRest tool, you can specify these parameters in the same `backups.pgbackrest.global` subsection with standard pgBackRest option names, also prefixed with the repository name.

        === ":fontawesome-brands-aws: Amazon S3 storage"

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
                global:
                  repo2-path: /pgbackrest/postgres-operator/cluster1/repo2
                ...
                repos:
                - name: repo2
                  s3:
                    bucket: "<YOUR_AWS_S3_BUCKET_NAME>"
                    region: "<YOUR_AWS_S3_REGION>"
            ```

            ??? note "Using AWS EC2 instances for backups makes it possible to automate access to AWS S3 buckets based on [IAM roles](https://kubernetes-on-aws.readthedocs.io/en/latest/user-guide/iam-roles.html) for Service Accounts with no need to specify the S3 credentials explicitly."

                To use this feature, add annotation to the spec part of the Custom Resource and also add pgBackRest custom configuration option to the backups subsection as follows:

                ```yaml
                spec:
                  crVersion: {{ release }}
                  metadata:
                    annotations:
                      eks.amazonaws.com/role-arn: arn:aws:iam::1191:role/role-pgbackrest-access-s3-bucket
                  ...
                  backups:
                    pgbackrest:
                      image: percona/percona-postgresql-operator:{{ release }}-ppg16-pgbackrest
                      global:
                        repo2-s3-key-type: web-id
                ```

        === ":simple-amazons3: S3-compatible storage"

            For example, the S3-compatible storage for the `repo2` repository looks as follows:

            ```yaml
            ...
            backups:
              pgbackrest:
                ...
                configuration:
                  - secret:
                      name: cluster1-pgbackrest-secrets
                ...
                global:
                  repo2-path: /pgbackrest/postgres-operator/cluster1/repo2
                  repo2-storage-verify-tls=y
                  repo2-s3-uri-style: path
                ...
                repos:
                - name: repo2
                  s3:
                    bucket: "<YOUR_AWS_S3_BUCKET_NAME>"
                    endpoint: "<YOUR_AWS_S3_ENDPOINT>"
                    region: "<YOUR_AWS_S3_REGION>"
            ```

            The `repo2-storage-verify-tls` option in the above example enables TLS verification for pgBackRest (when set to `y` or simply omitted) or disables it, when set to `n`.

            The `repo2-s3-uri-style` option [should be set to `path`  :octicons-link-external-16:](https://pgbackrest.org/configuration.html#section-repository/option-repo-s3-uri-style) if you use S3-compatible storage (otherwise you might see "host not found error" in your backup job logs), and is not needed for Amazon S3.

    5. Create or update the cluster. Replace the `<namespace>` placeholder with your value:

        ``` {.bash data-prompt="$" }
        $ kubectl apply -f deploy/cr.yaml -n <namespace>
        ```

=== ":simple-googlecloud: Google Cloud Storage"

    To use [Google Cloud Storage (GCS) :octicons-link-external-16:](https://cloud.google.com/storage) as
    an object store for backups, you need the following information:

    * a proper GCS bucket name. Pass the bucket name to `pgBackRest` via the
    `gcs.bucket` key in the `backups.pgbackrest.repos` subsection of
    `deploy/cr.yaml`.
    * your service account key for the Operator to access the storage.
    
    **Configuration steps** 
    {.power-number}

    1. Create your service account key following the [official Google Cloud instructions :octicons-link-external-16:](https://cloud.google.com/iam/docs/creating-managing-service-account-keys).
    2. Export this key from your Google Cloud account.

        You can find your key in the Google Cloud console (select *IAM & Admin*
        → *Service Accounts* in the left menu panel, then click your account and
        open the *KEYS* tab):    

        ![image](assets/images/gcs-service-account.svg)    

        Click the *ADD KEY* button, choose *Create new key* and choose *JSON* as a key
        type. These actions will result in downloading a file in JSON format with
        your new private key and related information (for example, `gcs-key.json`).    

    3. Create the [Kubernetes Secret :octicons-link-external-16:](https://kubernetes.io/docs/concepts/configuration/secret/). The Secret consists of 
         base64-encoded versions of two files: the `gcs-key.json` file with the Google service account key you have just downloaded, and the special `gcs.conf` configuration file.    

        * Create the `gcs.conf` configuration file. The file contents depends on the repository
        name for backups in the `deploy/cr.yaml` file. In case of the `repo3` repository, it looks as follows:    

        ```
        [global]
        repo3-gcs-key=/etc/pgbackrest/conf.d/gcs-key.json
        ```    

        * Encode both `gcs-key.json` and `gcs.conf` files. 

            === ":simple-linux: Linux"

                ```
                base64 --wrap=0 <filename>
                ```

            === ":simple-apple: MacOS"
                
                ```
                base64 -i <filename>
                ```

        * Create the Kubernetes Secret configuration file and specify your cluster name
        and the base64-encoded contents of the files from previous steps. The following is the example of the
        `cluster1-pgbackrest-secrets.yaml` Secret file:    

            ```yaml
            apiVersion: v1
            kind: Secret
            metadata:
              name: cluster1-pgbackrest-secrets
            type: Opaque
            data:
              gcs-key.json: <base64-encoded-json-file-contents>
              gcs.conf: <base64-encoded-conf-file-contents>
            ```       

          <i info>:material-information: Info </i>   This Secret can store credentials for several repositories presented as
               separate data keys.    

    4. Create the Secrets object from the Secret configuration file. Replace the `<namespace>` placeholder with your value:

        ``` {.bash data-prompt="$" }
        $ kubectl apply -f cluster1-pgbackrest-secrets.yaml -n <namespace>
        ```    

    5. Update your `deploy/cr.yaml` configuration. Specify your GCS credentials Secret in the `backups.pgbackrest.configuration` subsection, and put GCS bucket name into the `bucket` option in the `backups.pgbackrest.repos` subsection. The repository name must be the same as the name you specified when you created the `gcs.conf` file. 

        Also, provide pgBackRest the directory path for backup on the storage. You can pass it in the [backups.pgbackrest.global](https://docs.percona.com/percona-operator-for-postgresql/2.0/operator.html#backups-pgbackrest-global) subsection via the pgBackRest `path` option (prefix it's name with the repository name, for example `repo3-path`).

        For example, GCS storage configuration for the `repo3` repository would look as follows:

        ```yaml
        ...
        backups:
          pgbackrest:
            ...
            configuration:
              - secret:
                  name: cluster1-pgbackrest-secrets
            ...
            global:
              repo3-path: /pgbackrest/postgres-operator/cluster1/repo3
            ...
            repos:
            - name: repo3
              gcs:
                bucket: "<YOUR_GCS_BUCKET_NAME>"
        ```    

    6. Create or update the cluster. Replace the `<namespace>` placeholder with your value:

        ``` {.bash data-prompt="$" }
        $ kubectl apply -f deploy/cr.yaml -n <namespace>
        ```

=== ":material-microsoft-azure: Azure Blob Storage (tech preview)"

    To use [Microsoft Azure Blob Storage :octicons-link-external-16:](https://azure.microsoft.com/en-us/services/storage/blobs/) for storing backups, you need the following:

    * a proper Azure container name. 
    * Azure Storage credentials. These are stored in an encoded form in the [Kubernetes Secret :octicons-link-external-16:](https://kubernetes.io/docs/concepts/configuration/secret/).

    **Configuration steps**
    {.power-number}

    1. Encode the Azure Storage credentials and the pgBackRest repo name that you will use for backups with base64. In this example, we are using `repo4`.

        === ":simple-linux: Linux"    

            ``` {.bash data-prompt="$" }
            $ cat <<EOF | base64 --wrap=0
            [global]
            repo4-azure-account=<AZURE_STORAGE_ACCOUNT_NAME>
            repo4-azure-key=<AZURE_STORAGE_ACCOUNT_KEY>
            EOF
            ```    

        === ":simple-apple: macOS"    

            ``` {.bash data-prompt="$" }
            $ cat <<EOF | base64
            [global]
            repo4-azure-account=<AZURE_STORAGE_ACCOUNT_NAME>
            repo4-azure-key=<AZURE_STORAGE_ACCOUNT_KEY>
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
          azure.conf: <base64-encoded-configuration-contents>
        ```    

        !!! note    

            This Secret can store credentials for several repositories presented as
            separate data keys.    

    3. Create the Secrets object from this yaml file. Replace the `<namespace>` placeholder with your value:

        ``` {.bash data-prompt="$" }
        $ kubectl apply -f cluster1-pgbackrest-secrets.yaml -n <namespace>
        ```    

    4. Update your deploy/cr.yaml configuration. Specify the Secret file you have created in the previous step in the `backups.pgbackrest.configuration` subsection. Put Azure container name in the `backups.pgbackrest.repos` subsection under the repository name that you intend to use for backups. This name must match the name you used when you encoded Azure credentials on step 1.

        Also, provide pgBackRest the directory path for backup on the storage. You can pass it in the [backups.pgbackrest.global](https://docs.percona.com/percona-operator-for-postgresql/2.0/operator.html#backups-pgbackrest-global) subsection via the pgBackRest `path` option (prefix it's name with the repository name, for example `repo4-path`).

        For example, the Azure storage for the `repo4` repository looks as follows.

        ```yaml
        ...
        backups:
          pgbackrest:
            ...
            configuration:
              - secret:
                  name: cluster1-pgbackrest-secrets
            ...
            global:
              repo4-path: /pgbackrest/postgres-operator/cluster1/repo4
            ...
            repos:
            - name: repo4
              azure:
                container: "<YOUR_AZURE_CONTAINER>"
        ```    

    5. Create or update the cluster. Replace the `<namespace>` placeholder with your value:

        ``` {.bash data-prompt="$" }
        $ kubectl apply -f deploy/cr.yaml -n <namespace>
        ```
=== ":octicons-database-16: Persistent Volume"

    Percona Operator for PostgreSQL uses [Kubernetes Persistent Volumes](https://en.wikipedia.org/wiki/Amazon_S3#S3_API_and_competing_services) to store Postgres data. You can also use them to store backups. A Persistent volume is created at the same time when the Operator creates PostgreSQL cluster for you. You can find the Persistent Volume configuration in the `backups.pgbackrest.repos` section of the `cr.yaml` file under the `repo1` name:

    ```yaml
            ...
backups:
  pgbackrest:
    ...
    global:
      repo1-path: /pgbackrest/postgres-operator/cluster1/repo1
    ...
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

    This configuration is sufficient to make a backup.

## Next steps

* [Make an on-demand backup](backups-ondemand.md)
* [Make a scheduled backup](backups-schedule.md)

