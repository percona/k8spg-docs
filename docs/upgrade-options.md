# Upgrade Resource options

When you upgrade from one major version of Percona Distribution for PostgreSQL to another one (for example, from 17 to 18), the Operator creates a special Upgrade resource, `PerconaPGUpgrade`.

This document describes all available options that you can use to configure the major upgrade flow.

## `apiVersion`

Specifies the API version of the Custom Resource.
`pgv2.percona.com` indicates the group, and `v2` is the version of the API.

## `kind`

Defines the type of resource being created: `PerconaPGUpgrade`.

## `metadata`

The metadata part of the `deploy/upgrade.yaml` contains metadata about the upgrade, such as the name and other attributes. It includes the following keys:

* `name` - The name of the upgrade resource used to identify it in your deployment. You also use the upgrade name to track the upgrade progress.

## `spec`

This subsection includes the configuration of an upgrade resource.

### `postgresClusterName`

Specifies the name of the PostgreSQL cluster to upgrade.

| Value type  | Example    |
| ----------- | ---------- |
| :material-code-string: string     | `cluster1` |

### `image`

Specifies the special upgrade image used for the major upgrade.

| Value type  | Example    |
| ----------- | ---------- |
| :material-code-string: string     | `docker.io/percona/percona-postgresql-operator:{{ upgraderelease }}` |

### `fromPostgresVersion`

Specifies the current major version of PostgreSQL from which you wish to upgrade.

| Value type  | Example    |
| ----------- | ---------- |
| :material-code-string: integer     | `17` |

### `toPostgresVersion`

Specifies the target major version of PostgreSQL to which you wish to upgrade. You can only upgrade to the next major version (for example, from 16 to 17, or from 17 to 18). Skipping major versions (such as upgrading directly from 15 to 17) is not supported.

| Value type  | Example    |
| ----------- | ---------- |
| :material-code-string: integer     | `18` |

### `toPostgresImage`

Specifies the image for the target major version of PostgreSQL.

| Value type  | Example    |
| ----------- | ---------- |
| :material-code-string: string     | `docker.io/percona/percona-distribution-postgresql:{{ postgresrecommended }}` |

### `toPgBouncerImage`

Specifies the image for the `pgBouncer` connection pooler that is compatible with the target major version of PostgreSQL.

| Value type  | Example    |
| ----------- | ---------- |
| :material-code-string: string     | `docker.io/percona/percona-pgbouncer:{{ pgbouncerrecommended }}` |

### `toPgBackRestImage`

Specifies the image for the `pgBackRest` backup and restore solution that is compatible with the target major version of PostgreSQL.

| Value type  | Example    |
| ----------- | ---------- |
| :material-code-string: string     | `docker.io/percona/percona-pgbackrest:{{ pgbackrestrecommended }}` |

