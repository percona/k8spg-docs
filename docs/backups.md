# About backups

In this section you will learn how to set up and manage backups of your data using the Operator.

You can make backups in two ways:

* _On-demand_. You can do them manually at any moment.
* _Schedule backups_. Configure backups and their schedule in the
[deploy/cr.yaml](https://github.com/percona/percona-postgresql-operator/blob/main/deploy/cr.yaml)
file. The Operator makes them automatically in the specified time. 

## Backup storage

You have the following options to store PostgreSQL backups outside the
Kubernetes cluster:

* Cloud storage:

   * Amazon S3, or [any S3-compatible storage](https://en.wikipedia.org/wiki/Amazon_S3#S3_API_and_competing_services),
   * [Google Cloud Storage](https://cloud.google.com/storage), 
   * [Azure Blob Storage](https://azure.microsoft.com/en-us/services/storage/blobs/)

* A [Persistent Volume](https://kubernetes.io/docs/concepts/storage/persistent-volumes/) attached to the pgBackRest Pod.


### Backup repositories

To make backups, the Operator uses the open source [pgBackRest](https://pgbackrest.org/) backup
and restore utility. 

When the Operator creates a new PostgreSQL cluster, it also creates a special *pgBackRest repository* to facilitate the usage of the pgBackRest
features. You can notice an additional `repo-host` Pod after the cluster
creation.

Each pgBackRest repository consists of the following Kubernetes objects:

* A Deployment,
* A Secret that contains information specific to the PostgreSQL cluster
    (e.g. SSH keys, AWS S3 keys, etc.),
* A Pod with a number of supporting scripts,
* A Service.

You can have up to 4 pgBackRest repositories named as `repo1`, `repo2`, `repo3`,
and `repo4`.

## Backup types

The PostgreSQL Operator supports three types of pgBackRest backups:

* `full`: A full backup of all the contents of the PostgreSQL cluster,
* `differential`: A backup of only the files that have changed since
the last full backup,
* `incremental`: A backup of only the files that have changed since the
last full or differential backup. Incremental backup is the default choice.

## Backup retention

The Operator also supports setting pgBackRest retention policies for full and
differential backups. When a full backup expires according to the retention
policy, pgBackRest cleans up all the files related to this backup and to the
write-ahead log. Thus, the expiration of a full backup with some incremental backups
based on it results in expiring of all these incremental backups.

You can control backup retention by the following `pgBackRest` options:

* `--<repo name>-retention-full` how much full backups to retain,
* `--<repo name>-retention-diff` how much differential backups to retain.

Backup retention type can be either `count` (the number of backups to keep) or
`time` (the number of days to keep a backup for).

You can set both backup type and retention policy for each of 4 repositories
as follows.

```yaml
backups:
    pgbackrest:
...
      global:
        repo1-retention-full: "14"
        repo1-retention-full-type: time
        ...
```


