# Restore Resource Options

A Restore resource is a Kubernetes object that tells the Operator how to restore your database from a specific backup. The `deploy/restore.yaml` file is a template for creating restore resources. It defines the `PerconaPGRestore` resource.

This document describes all available options that you can use to customize a restore.

## `apiVersion`

Specifies the API version of the Custom Resource.
`pgv2.percona.com` indicates the group, and `v2` is the version of the API.

## `kind`

Defines the type of resource being created: `PerconaPGRestore`.

## `metadata`

The metadata part of the `deploy/restore.yaml` contains metadata about the resource, such as its name and other attributes. It includes the following keys:

* `name` - The name of the restore resource used to identify it in your deployment. You use this name to track the restore operation status and view information about it.

## `spec`

This subsection includes the configuration of a restore resource.

### `pgCluster`

Specifies the name of the PostgreSQL cluster to restore.

| Value type  | Example    |
| ----------- | ---------- |
| :material-code-string: string     | `restore1` |

### `repoName`

Specifies the name of one of the 4 pgBackRest repositories, already configured in the `backups.pgbackrest.repos` subsection of the `deploy/cr.yaml` file.

| Value type  | Example    |
| ----------- | ---------- |
| :material-code-string: string     | `repo1` |

### `volumeSnapshotBackupName`

Specifies the name of a PVC snapshot-based backup to restore from. See [Configure and use PVC snapshots](backups-pvc-setup.md) to learn more.

| Value type  | Example    |
| ----------- | ---------- |
| :material-code-string: string     | `backup1` |

### `options`

Specify the [command line options supported by `pgBackRest` :octicons-external-link-16:](https://pgbackrest.org/configuration.html). For example, to make a [point-in-time restore](backups-pitr.md) or to restore from a specific backup.

| Value type  | Example    |
| ----------- | ---------- |
| :material-code-string: string     | `--type=time` <br> `--target=YYYY-MM-DD HH:MM:DD +00` <br> `--set=20240628-074416F` (backup name) |

To restore from a specific backup, use the `--set` option with the backup label. You can find the backup label in the `status.backupName` field of the `PerconaPGBackup` resource. For the full restore workflow, see [Restore to the same cluster](backups-restore-inplace.md) or [Restore to a new cluster](backups-clone.md). For point-in-time recovery, see [Point-in-time recovery](backups-pitr.md).

### `containerOptions.env.name`

Specifies the name of a custom environment variable that you pass to backup containers for restore Pods.

| Value type  | Example    |
| ----------- | ---------- |
| :material-code-string: string     | `MY_ENV` |

### `containerOptions.env.value`

Specifies the value for a custom environment variable that you pass to backup containers for restore Pods.

| Value type  | Example    |
| ----------- | ---------- |
| :material-code-string: string     | `1000` |

### `containerOptions.envFrom.secretRef.name`

Name of a Secret, key/values of which are used as environment variables for restore Pods.

| Value type  | Example    |
| ----------- | ---------- |
| :material-code-string: string     | `restore-env-secret` |
