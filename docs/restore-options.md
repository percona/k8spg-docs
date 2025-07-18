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

### `options`

Specify the [command line options supported by pgBackRest :octicons-external-link-16:](https://pgbackrest.org/configuration.html). For example, to make a point-in-time restore.

| Value type  | Example    |
| ----------- | ---------- |
| :material-code-string: string     | `--type=time` <br> `--target=YYYY-MM-DD HH:MM:DD +00` |
