> For the complete documentation index, see [llms.txt](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/llms.txt).

# Configure storage for backups

Configure backup storage for your [backup repositories](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/backups.html#backup-repositories) in the `backups.pgbackrest.repos` section of the [deploy/cr.yaml](https://github.com/percona/percona-postgresql-operator/blob/main/deploy/cr.yaml) configuration file.

You can use the following storage types with the Operator:

- **Amazon S3 or S3-compatible storage** — Use native AWS S3 buckets on Amazon EKS or any other Kubernetes platform. Or, use compatible services like MinIO and others that expose an S3-compatible API. On EKS, you can authenticate with [S3 access keys](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/backups-storage-s3.html) or [IAM roles for Service Accounts](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/backups-storage-s3.html#__tabbed_1_2).
- **Google Cloud Storage** — Use Google Cloud object storage.
- **Azure Blob Storage** (tech preview) — Use Microsoft Azure Blob Storage.
- **Persistent Volume** — Use a [persistent volume attached to the pgBackRest Pod](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/backups-storage-pv.html) that is created together with the PostgreSQL cluster.

For cloud object storage, you typically create a [Kubernetes Secret](https://kubernetes.io/docs/concepts/configuration/secret/) with credentials and reference it in `backups.pgbackrest.configuration`. If you use IAM roles on Amazon EKS, you don’t need to create a Secret.

## Storage setup guides

Select the appropriate guide below based on your chosen storage type:

- [Amazon S3 storage](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/backups-storage-s3.html)
- [Google Cloud Storage](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/backups-storage-gcs.html)
- [Microsoft Azure Blob Storage](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/backups-storage-azure.html)
- [Persistent Volume](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/backups-storage-pv.html)

## Next steps

[Make an on-demand backup](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/backups-ondemand.html) [Make a scheduled backup](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/backups-schedule.html)
