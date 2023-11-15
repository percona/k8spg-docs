# Creating a private S3-compatible cloud for backups

As it is mentioned in [backups](backups.md), any cloud storage which
implements the S3 API can be used for backups. The one way to setup and
implement the S3 API storage on Kubernetes or OpenShift is
[Minio](https://www.minio.io/) - the S3-compatible object storage server
deployed via Docker on your own infrastructure.

Setting up Minio to be used with Percona Operator for PostgreSQL backups involves
the following steps:

1. Install Minio in your Kubernetes or OpenShift
    environment and create the correspondent Kubernetes Service as
    follows:

    ``` {.bash data-prompt="$" }
    $ helm install \
      --name minio-service \
      --version 8.0.5 \
      --set accessKey=some-access-key \
      --set secretKey=some-secret-key \
      --set service.type=ClusterIP \
      --set configPath=/tmp/.minio/ \
      --set persistence.size=2G \
      --set environment.MINIO_REGION=us-east-1 \
      stable/minio
    ```

    Don’t forget to substitute default `some-access-key` and `some-secret-key`
    strings in this command with actual unique key values. The values can be
    used later for access control. The `storageClass` option is needed if you
    are using the special [Kubernetes Storage Class](https://kubernetes.io/docs/concepts/storage/storage-classes/)
    for backups. Otherwise, this setting may be omitted. You may also notice the
    `MINIO_REGION` value which is may not be used within a private cloud. Use
    the same region value here and on later steps (`us-east-1` is a good default
    choice).

2. Create an S3 bucket for backups:

    ``` {.bash data-prompt="$" }
    $ kubectl run -i --rm aws-cli --image=perconalab/awscli --restart=Never -- \
      bash -c 'AWS_ACCESS_KEY_ID=some-access-key \
      AWS_SECRET_ACCESS_KEY=some-secret-key \
      AWS_DEFAULT_REGION=us-east-1 \
      /usr/bin/aws \
      --endpoint-url http://minio-service:9000 \
      s3 mb s3://operator-testing'
    ```

    This command creates the bucket named `operator-testing` with
    the selected access and secret keys (substitute `some-access-key`
    and `some-secret-key` with the values used on the previous step).

3. Now edit the backup section of the [deploy/cr.yaml](https://github.com/percona/percona-postgresql-operator/blob/1.x/deploy/cr.yaml)
    file to set proper values for your newly created  storage as follows (you
    can find more on these options in [backup and restore documentation](backups.md#configuring-the-s3-compatible-backup-storage)).

    ```yaml
    ...
    backup:
      ...
      storages:
        minio:
          type: s3
          bucket: operator-testing
          region: us-east-1
          endpointUrl: http://minio-service:9000
          uriStyle: "path"
          verifyTLS: false
    ```

    You will also need to supply pgBackRest with base64-encoded access and 
    secret keys stored in [Kubernetes Secrets](https://kubernetes.io/docs/concepts/configuration/secret/).
    
    !!! note

        You can encode needed data to base64 with the following command:

        === "in Linux"

            ``` {.bash data-prompt="$" }
            $ echo -n 'plain-text-string' | base64 --wrap=0
            ```

        === "in macOS"

            ``` {.bash data-prompt="$" }
            $ echo -n 'plain-text-string' | base64
            ```

    Edit the `deploy/backup/cluster1-backrest-repo-config-secret.yaml`
    configuration file: set `name`, `aws-s3-key`, and `aws-s3-key-secret` with
    proper cluster name, key, and key secret.

    ```yaml
    apiVersion: v1
    kind: Secret
    metadata:
      name: <cluster-name>-backrest-repo-config
    type: Opaque
    data:
      aws-s3-key: c29tZS1hY2Nlc3Mta2V5
      aws-s3-key-secret: c29tZS1zZWNyZXQta2V5
    ```

    When done, create the secret as follows:

    ``` {.bash data-prompt="$" }
    $ kubectl apply -f deploy/backup/cluster1-backrest-repo-config-secret.yaml
    ```

    Finally, create or update the cluster:

    ``` {.bash data-prompt="$" }
    $ kubectl apply -f deploy/cr.yaml
    ```

4. When the setup process is completed, you can make [on-demand](backups.md#making-on-demand-backup)
    and [scheduled](backups.md#scheduling-backups) backups and/or backup restore following the
    official [backup/restore documentation](backups.md).
