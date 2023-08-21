## Configure backup storage

You can configure backup storage for your repositories in the
`backups.pgbackrest.repos` section of the `deploy/cr.yaml` configuration file.

=== "S3-compatible backup storage"

     Provide some S3-related information, such as proper S3 bucket name, endpoint, etc. to use S3-compatible storage for backups. Pass this
     information to pgBackRest via the following `deploy/cr.yaml`
     options in the `backups.pgbackrest.repos` subsection:     

     * `bucket` specifies the AWS S3 bucket that should be utilized,
     for example `my-postgresql-backups-example`,
     * `endpoint` specifies the S3 endpoint that should be utilized,
     for example `s3.amazonaws.com`,
     * `region` specifies the AWS S3 region that should be utilized,
     for example `us-east-1`.     

     You also need to supply pgBackRest with the base64-encoded AWS S3 key and AWS S3 key
     secret stored along with other sensitive information in [Kubernetes Secrets](https://kubernetes.io/docs/concepts/configuration/secret/).     

     1. Put your AWS S3 key and AWS S3 key secret into the base64-encoded pgBackRest configuration with your pgBackRest repository name. In case of the `repo1` repository it can be done as follows:     

        === "in Linux"     

             ``` {.bash data-prompt="$" }
             $ cat <<EOF | base64 --wrap=0
             [global]
             repo1-s3-key=<YOUR_AWS_S3_KEY>
             repo1-s3-key-secret=<YOUR_AWS_S3_KEY_SECRET>
             EOF
             ```     

        === "in macOS"     

             ``` {.bash data-prompt="$" }
             $ cat <<EOF | base64
             [global]
             repo1-s3-key=<YOUR_AWS_S3_KEY>
             repo1-s3-key-secret=<YOUR_AWS_S3_KEY_SECRET>
             EOF
             ```     

     2. Create the Secret configuration file with the resulted base64-encoded string
         as the following `cluster1-pgbackrest-secrets.yaml` example:     

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

         When done, create the Secrets object from this yaml file:     

         ``` {.bash data-prompt="$" }
         $ kubectl apply -f cluster1-pgbackrest-secrets.yaml
         ```     

     3. Update your `deploy/cr.yaml` configuration with the S3 credentials
         Secret in the `backups.pgbackrest.configuration` subsection, and put all
         other S3 related information into the options of one of your repositories
         in the `backups.pgbackrest.repos` subsection. For example, the S3 storage
         for the `repo1` repository would look as follows.     

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
             - name: repo1
               s3:
                 bucket: "<YOUR_AWS_S3_BUCKET_NAME>"
                 endpoint: "<YOUR_AWS_S3_ENDPOINT>"
                 region: "<YOUR_AWS_S3_REGION>"
         ```     

     4. Create or update the cluster:     

         ``` {.bash data-prompt="$" }
         $ kubectl apply -f deploy/cr.yaml
         ```

=== "Google Cloud Storage"

    You can configure [Google Cloud Storage](https://cloud.google.com/storage) as
    an object store for backups similarly to S3 storage.    

    Provide the following information in order to use Google Cloud Storage (GCS) for backups:    

    * a proper GCS bucket name. Pass the bucket name to `pgBackRest` via the
    `gcs.bucket` key in the `backups.pgbackrest.repos` subsection of
    `deploy/cr.yaml`.
    * your service account key for the Operator to access the storage.    
    
    Procedure: 

    1. Create your service account key following the [official Google Cloud instructions](https://cloud.google.com/iam/docs/creating-managing-service-account-keys).
    2. Export this key from your Google Cloud account.    

        You can find your key in the Google Cloud console (select *IAM & Admin*
        → *Service Accounts* in the left menu panel, then click your account and
        open the *KEYS* tab):    

        ![image](assets/images/gcs-service-account.svg)    

        Click the *ADD KEY* button, chose *Create new key* and chose *JSON* as a key
        type. These actions will result in downloading a file in JSON format with
        your new private key and related information.    

    3. Now you should create the [Kubernetes Secret](https://kubernetes.io/docs/concepts/configuration/secret/)
        using base64-encoded versions of two files: the file containing the
        private key you have just downloaded, and the special `gcs.conf` configuration file.    

        The content of the `gcs.conf` file depends on the repository
        name. In case of the `repo1` repository, it looks as follows:    

        ```
        [global]
        repo1-gcs-key=/etc/pgbackrest/conf.d/gcs-key.json
        ```    

        You can encode a text file with the `base64 --wrap=0 <filename>`
        command (or just `base64 <filename>` in case of Apple macOS).
        When done, create the following yaml file with your cluster name
        and base64-encoded files contents as the following
        `cluster1-pgbackrest-secrets.yaml` example:    

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

        !!! note    

            This Secret can store credentials for several repositories presented as
            separate data keys.    

        Create the Secrets object from this YAML file:    

        ``` {.bash data-prompt="$" }
        $ kubectl apply -f cluster1-pgbackrest-secrets.yaml
        ```    

    4. Update your `deploy/cr.yaml` configuration with your GCS credentials
        Secret in the `backups.pgbackrest.configuration` subsection, and put GCS
        bucket name into the `bucket` option of one of your repositories
        in the `backups.pgbackrest.repos` subsection. For example, GCS storage
        for the `repo3` repository would look as follows.    

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
            - name: repo3
              gcs:
                bucket: "<YOUR_GCS_BUCKET_NAME>"
        ```    

    5. Create or update the cluster:    

        ``` {.bash data-prompt="$" }
        $ kubectl apply -f deploy/cr.yaml
        ```

=== "Azure Blob Storage (tech preview)"

    In order to use [Microsoft Azure Blob Storage](https://azure.microsoft.com/en-us/services/storage/blobs/) for backups you need to provide a proper Azure container name. It can be passed to
    `pgBackRest` via the `azure.container` key in the `backups.pgbackrest.repos`
    subsection of `deploy/cr.yaml`.    

    The Operator will also need a [Kubernetes Secret](https://kubernetes.io/docs/concepts/configuration/secret/)
    with your Azure Storage credentials to access the storage.    

    1. Put your Azure storage account name and key into the base64-encoded pgBackRest
        configuration with your pgBackRest repository name. In case of the `repo1`
        repository it can be done as follows:    

        === "in Linux"    

            ``` {.bash data-prompt="$" }
            $ cat <<EOF | base64 --wrap=0
            [global]
            repo1-azure-account=<AZURE_STORAGE_ACCOUNT_NAME>
            repo1-azure-key=<AZURE_STORAGE_ACCOUNT_KEY>
            EOF
            ```    

        === "in macOS"    

            ``` {.bash data-prompt="$" }
            $ cat <<EOF | base64
            [global]
            repo1-azure-account=<AZURE_STORAGE_ACCOUNT_NAME>
            repo1-azure-key=<AZURE_STORAGE_ACCOUNT_KEY>
            EOF
            ```    

    2. Create the Secret configuration file with the resulted base64-encoded string
        as the following `cluster1-pgbackrest-secrets.yaml` example:    

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

        When done, create the Secrets object from this yaml file:    

        ``` {.bash data-prompt="$" }
        $ kubectl apply -f cluster1-pgbackrest-secrets.yaml
        ```    

    3. Update your `deploy/cr.yaml` configuration with the Azure Storage credentials
        Secret in the `backups.pgbackrest.configuration` subsection, and put Azure
        container name into the options of one of your repositories
        in the `backups.pgbackrest.repos` subsection. For example, the Azure storage
        for the `repo1` repository would look as follows.    

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
            - name: repo1
              azure:
                container: "<YOUR_AZURE_CONTAINER>"
        ```    

    4. Finally, create or update the cluster:    

        ``` {.bash data-prompt="$" }
        $ kubectl apply -f deploy/cr.yaml
        ```

