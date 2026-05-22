# Configure storage for backups

Configure backup storage for your [backup repositories](backups.md#backup-repositories) in the `backups.pgbackrest.repos` section of the [deploy/cr.yaml](https://github.com/percona/percona-postgresql-operator/blob/main/deploy/cr.yaml) configuration file.

You can use the following storage types with the Operator:

* **Amazon S3 or S3-compatible storage** — Use native AWS S3 buckets on Amazon EKS or any other Kubernetes platform. Or, use compatible services like MinIO and others that expose an S3-compatible API. On EKS, you can authenticate with [S3 access keys](backups-storage-s3.md) or [IAM roles for Service Accounts](backups-storage-s3.md#__tabbed_1_2).
* **Google Cloud Storage** — Use Google Cloud object storage.
* **Azure Blob Storage** (tech preview) — Use Microsoft Azure Blob Storage.
* **Persistent Volume** — Use a [persistent volume attached to the pgBackRest Pod](backups-storage-pv.md) that is created together with the PostgreSQL cluster.

For cloud object storage, you typically create a [Kubernetes Secret :octicons-link-external-16:](https://kubernetes.io/docs/concepts/configuration/secret/) with credentials and reference it in `backups.pgbackrest.configuration`. If you use IAM roles on Amazon EKS, you don't need to create a Secret.

## Storage setup guides

Select the appropriate guide below based on your chosen storage type:

* [Amazon S3 storage](backups-storage-s3.md)
* [Google Cloud Storage](backups-storage-gcs.md)
* [Microsoft Azure Blob Storage](backups-storage-azure.md)
* [Persistent Volume](backups-storage-pv.md)

## Next steps

[Make an on-demand backup](backups-ondemand.md){.md-button}
[Make a scheduled backup](backups-schedule.md){.md-button}
