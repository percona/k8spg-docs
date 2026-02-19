# Backup Resource Options

A Backup resource is a Kubernetes object that tells the Operator how to create and manage your database backups. The `deploy/backup.yaml` file is a template for creating backup resources when you make an on-demand backup. It defines the `PerconaPGBackup` resource.

This document describes all available options that you can use to customize your backups.

## `apiVersion`

Specifies the API version of the Custom Resource.
`pgv2.percona.com` indicates the group, and `v2` is the version of the API.

## `kind`

Defines the type of resource being created: `PerconaPGBackup`.

## `metadata`

The metadata part of the `deploy/backup.yaml` contains metadata about the resource, such as its name and other attributes. It includes the following keys:

* `name` - The name of the backup resource used to identify it in your deployment. You also use the backup name for the restore operation.

## `spec`

This subsection includes the configuration of a backup resource.

### `pgCluster`

Specifies the name of the PostgreSQL cluster to back up.

| Value type  | Example    |
| ----------- | ---------- |
| :material-code-string: string     | `cluster1` |

### `repoName`

Specifies the name of the `pgBackRest` repository where to save a backup. It must match the name you specified in the `spec.backups.pgBackRest.repos` subsection of the `deploy/cr.yaml` file.

| Value type  | Example    |
| ----------- | ---------- |
| :material-code-string: string     | `repo1` |

### `method`

Specifies what method to use for the backup. When undefined, uses `pgBackRest` by default. Supported value is `VolumeSnapshot`. See [PVC snapshot support](backups-pvc-snapshots.md) to learn more.

| Value type  | Example    |
| ----------- | ---------- |
| :material-code-string: string     | `VolumeSnapshot` |

### `options`

You can customize the backup by specifying different [command line options supported by pgBackRest :octicons-external-link-16:](https://pgbackrest.org/configuration.html).

| Value type  | Example    |
| ----------- | ---------- |
| :material-code-string: string     | `--type=full` |

### `containerOptions.env.name`

Specifies the name of a custom environment variable that you pass to backup containers for manual backups.

| Value type  | Example    |
| ----------- | ---------- |
| :material-code-string: string     | `MY_ENV` |

### `containerOptions.env.value`

Specifies the value for a custom environment variable that you pass to backup containers for manual backups.

| Value type  | Example    |
| ----------- | ---------- |
| :material-code-string: string     | `1000` |

### `containerOptions.envFrom.secretRef.name`

Name of a Secret, key/values of which are used as environment variables for manual backups.

| Value type  | Example    |
| ----------- | ---------- |
| :material-code-string: string     | `backup-env-secret` |
