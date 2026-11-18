> For the complete documentation index, see [llms.txt](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/llms.txt).

# About backups

In this section you will learn how to set up and manage backups of your data using the Operator.

You can make backups in two ways:

- *On-demand*. You can do them manually at any moment.
- *Schedule backups*. Configure backups and their schedule in the [deploy/cr.yaml](https://github.com/percona/percona-postgresql-operator/blob/main/deploy/cr.yaml) file. The Operator makes them automatically according to the schedule.

## What you need to know

### Backup methods

By default, the Operator uses the open source [pgBackRest](https://pgbackrest.org/) backup and restore utility to make backups.

Starting with version 2.9.0, the Operator also supports [PVC snapshots](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/backups-pvc-snapshots.html) - storage-level copies of your data volumes. PVC snapshots offer much faster backups and restores. When used with `pgBackRest` WAL archiving, they maintain data consistency and enable you to make a [point-in-time recovery](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/backups-pvc-usage.html#in-place-restore-with-point-in-time-recovery) of your database.

This feature is in the tech preview stage. You must explicitly enable it for the Operator deployment.

### Backup repositories

When the Operator creates a new PostgreSQL cluster, it also creates a special *pgBackRest repository* to facilitate the usage of the pgBackRest features. You can notice an additional `repo-host` Pod after the cluster creation.

A pgBackRest repository consists of the following Kubernetes objects:

- A Deployment,
- A Secret that contains information specific to the PostgreSQL cluster (e.g. SSH keys, AWS S3 keys, etc.),
- A Pod with a number of supporting scripts,
- A Service.

In the `/deploy/cr.yml` file, pgBackRest repositories are listed in the `backups.pgbackrest.repos` subsection. You can have up to 4 repositories as `repo1`, `repo2`, `repo3`, and `repo4`.

### Backup types

You can make the following types of backups:

- `full`: A full backup of all the contents of the PostgreSQL cluster,
- `differential`: A backup of only the files that have changed since the last full backup,
- `incremental`: Default. A backup of only the files that have changed since the last full or differential backup.

### Backup storage

You have the following options to store PostgreSQL backups:

- Cloud storage:

  - [Amazon S3](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/backups-storage-s3.html) or any S3-compatible storage
  - [Google Cloud Storage](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/backups-storage-gcs.html)
  - [Azure Blob Storage](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/backups-storage-azure.html)

- A [Persistent Volume](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/backups-storage-pv.html) attached to the pgBackRest Pod.

## Next steps

Ready to move forward? [Configure backup storage](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/backups-storage.html)
