# Amazon S3 storage

To use [Amazon S3 :octicons-link-external-16:](https://aws.amazon.com/s3/) for backups, you need to have the following information: 

* S3 bucket name
* AWS region where the bucket is located. Check the [Region considerations for pgBackRest](#region-considerations-for-pgbackrest)
* Authentication to the bucket. You can use one of the following options:
  
    * **S3 access keys**. Store your AWS S3 access key and secret key in a Kubernetes Secret and reference it in your cluster configuration. This method works on any Kubernetes platform and requires that you manage the credentials yourself.
    * **IAM role for Service Accounts** (IRSA). Assign an IAM role to the Kubernetes Service Account used by pgBackRest. With IRSA, you don't need to manage static secrets since AWS automatically provides temporary credentials to the Pod, following best practices for security and rotation.

* For S3-compatible storage other than native Amazon S3, also specify:
   
   * The endpoint - the actual URI to access the bucket 
   * The URI style — determines how the Operator accesses the bucket. For most S3-compatible providers, you must set the URI style to `path`. This is required for correct operation with most S3-compatible storage endpoints.

## Region considerations for pgBackRest

pgBackRest archives write-ahead logs (WAL) to backup storage. If the bucket is in a region far from your PostgreSQL cluster, archiving can lag: a new WAL file must be archived within [60 seconds by default :octicons-link-external-16:](https://www.postgresql.org/docs/current/runtime-config-wal.html#GUC-ARCHIVE-TIMEOUT), and long delays can cause backup and replica issues when the primary restarts. Use the same AWS region for the cluster and the bucket when possible, or replicate the bucket with [Amazon S3 Cross-Region Replication :octicons-link-external-16:](https://docs.aws.amazon.com/AmazonS3/latest/userguide/replication.html).

## Configuration steps {.power-number}

Select your authentication method below. If you are using S3-compatible storage, follow the "S3 access keys" instructions.

The examples in the following sections use the `repo2` repository name. Use the same name consistently for Secrets, `global` settings, and `repos` in your configuration.

=== "S3 access keys"

    Follow these steps to authenticate using an AWS S3 access key and secret key. This method works on any Kubernetes environment.
    {.power-number}

    1. Encode the S3 credentials and the pgBackRest repository name that you will use for backups. The following example uses `repo2`:

        === ":simple-linux: Linux"

            ```bash
            cat <<EOF | base64 --wrap=0
            [global]
            repo2-s3-key=<YOUR_AWS_S3_KEY>
            repo2-s3-key-secret=<YOUR_AWS_S3_KEY_SECRET>
            EOF
            ```

        === ":simple-apple: macOS"

            ```bash
            cat <<EOF | base64
            [global]
            repo2-s3-key=<YOUR_AWS_S3_KEY>
            repo2-s3-key-secret=<YOUR_AWS_S3_KEY_SECRET>
            EOF
            ```

    2. Create the Secret manifest and set `data.s3.conf` to the encoded string from the previous step. The following is the example of the  `cluster1-pgbackrest-secrets.yaml` configuration file:

        ```yaml
        apiVersion: v1
        kind: Secret
        metadata:
          name: cluster1-pgbackrest-secrets
        type: Opaque
        data:
          s3.conf: <base64-encoded-configuration-contents>
        ```

        You can store credentials for several repositories in one Secret by adding separate data keys.

    3. Create the Secrets object from this YAML file. Replace `<namespace>` with your namespace:

        ```bash
        kubectl apply -f cluster1-pgbackrest-secrets.yaml -n <namespace>
        ```

    4. Update `deploy/cr.yaml` Custom Resource manifest:
       
        * Reference the Secret in `backups.pgbackrest.configuration`
        * Provide the backup path in [backups.pgbackrest.global](operator.md#backupspgbackrestglobal) with the pgBackRest `path` option. Specify `repo2-path`.  
        * For S3-compatible storage:
          
            * Set `global.repo2-storage-verify-tls` to `y` to enable TLS verification
            * Set the [`global.repo2-s3-uri-style` option :octicons-link-external-16:](https://pgbackrest.org/configuration.html#section-repository/option-repo-s3-uri-style) to `path`. Without it, backup jobs may log a "host not found" error.
            * Specify additional [repository options :octicons-link-external-16:](https://pgbackrest.org/configuration.html#section-repository) in `global`, if your S3-compatible storage requires them.
       
        * Define the S3 bucket, region and endpoint under `repos`

        === ":fontawesome-brands-aws: Amazon S3 storage"
       
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

        === ":simple-minio: S3-compatible storage"

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
                  repo2-storage-verify-tls: "y"
                  repo2-s3-uri-style: path
                ...
                repos:
                - name: repo2
                  s3:
                    bucket: "<YOUR_S3_BUCKET_NAME>"
                    endpoint: "<YOUR_S3_ENDPOINT>"
                    region: "<YOUR_S3_REGION>"
            ```

    5. Apply the cluster Custom Resource:

        ```bash
        kubectl apply -f deploy/cr.yaml -n <namespace>
        ```

=== "IAM role for Service Account"

    On [Amazon EKS :octicons-link-external-16:](https://docs.aws.amazon.com/eks/latest/userguide/iam-roles-for-service-accounts.html), you can grant the Operator access to S3 with [IAM roles for Service Accounts (IRSA) :octicons-link-external-16:](https://kubernetes-on-aws.readthedocs.io/en/latest/user-guide/iam-roles.html). pgBackRest authenticates through the pod identity; therefore, you don't need to create a Secret with s3 credentials and reference it in the Custom Resource.
    {.power-number}

    1. Create an IAM role for your EKS OIDC provider and attach a policy that allows the required S3 bucket access. See the [official AWS documentation :octicons-link-external-16:](https://docs.aws.amazon.com/eks/latest/userguide/associate-service-account-role.html) for details.

    2. Annotate the Custom Resource with the IAM role Amazon Resource Name (ARN) and set `repo2-s3-key-type` to `web-id` in `backups.pgbackrest.global`:

        ```yaml
        spec:
          crVersion: {{ release }}
          metadata:
            annotations:
              eks.amazonaws.com/role-arn: arn:aws:iam::1191:role/role-pgbackrest-access-s3-bucket
          ...
          backups:
            pgbackrest:
              image: percona/pgbackrest:{{pgbackrestrecommended}}
              global:
                repo2-path: /pgbackrest/postgres-operator/cluster1/repo2
                repo2-s3-key-type: web-id
        ```

    3. Apply the cluster Custom Resource:

        ```bash
        kubectl apply -f deploy/cr.yaml -n <namespace>
        ```

If you configure both IRSA and S3 keys in a Secret, the Secret credentials take precedence for authentication.

## Next steps

[Make an on-demand backup](backups-ondemand.md){.md-button}
[Make a scheduled backup](backups-schedule.md){.md-button}
