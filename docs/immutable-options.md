# Immutable options

Percona Operator for PostgreSQL manages certain options internally to ensure cluster health, backup integrity, and security. You cannot change these options through the Custom Resource or other configuration methods. If you try to modify them, the Operator reconciles the cluster and reverts your changes.

There are some options that you can override and some of them have modification limits.

This document lists all of them:

* [PostgreSQL parameters that you cannot override](#postgresql-parameters-that-cannot-be-overridden) 
* [PostgreSQL parameters that you can override](#postgresql-parameters-that-can-be-overridden)
* [Custom Resource options with modification limits](#custom-resource-options-with-modification-limits).

## PostgreSQL parameters that cannot be overridden

The Operator sets and enforces the following PostgreSQL parameters. You cannot override them via `patroni.dynamicConfiguration.postgresql.parameters` or any other method. The Operator reconciles the Patroni configuration and restores these values.

### TLS and security

| Parameter | Value   | Purpose |
| --------- | ------- | ------- | 
| `ssl` | `on` | Always set to `on` for encrypted connections. |
| `ssl_cert_file` |  `/pgconf/tls/tls.crt` | Path to the TLS certificate. The Operator manages certificate paths. |
| `ssl_key_file` | `/pgconf/tls/tls.key` | Path to the TLS private key. |
| `ssl_ca_file` | `/pgconf/tls/ca.crt` | Path to the CA certificate. |

### Cluster internals

| Parameter | Value   | Purpose |
| --------- | ------- | ------- | 
| `unix_socket_directories` | `/tmp/postgres` | Socket path for local connections. The Operator uses a fixed path for Pod communication. |
| `log_file_mode` | `0660` | File permissions for log files. The Operator sets this for Pod security context compatibility. |

### WAL archiving and recovery (pgBackRest parameters)

| Parameter | Value   | Purpose |
| --------- | ------- | --------| 
| `archive_mode` | `on` | Must be `on` for pgBackRest to archive WAL files. The Operator sets this to enable backups. |
| `archive_command` | pgbackrest --stanza=db archive-push "%p" | Command that archives WAL segments to pgBackRest. The Operator configures this for the backup repository. |
| `archive_timeout` | `60s` | Forces a WAL switch after the specified interval. The Operator manages this for backup consistency. |
| `track_commit_timestamp` | `true`  | Enables commit timestamps for point-in-time recovery when [backups.trackLatestRestorableTime](operator.md#backupstracklatestrestorabletime) is enabled and the `crVersion` is 2.8.0 or higher |

### Extension parameters

When you enable built-in extensions, the Operator appends or sets the following parameters. You cannot override these values while the extension is enabled.

**When `spec.extensions.builtin.pg_stat_statements` is `true`:**

| Parameter | Value |
| --------- | ----- |
| `shared_preload_libraries` | Appended with `pg_stat_statements` |
| `pg_stat_statements.track` | `all` |

**When `spec.extensions.builtin.pg_stat_monitor` is `true`:**

| Parameter | Value |
| --------- | ----- |
| `shared_preload_libraries` | Appended with `pg_stat_monitor` |
| `pg_stat_monitor.pgsm_query_max_len` | `2048` |

**When `spec.extensions.builtin.pg_audit` is `true`:**

| Parameter | Value |
| --------- | ----- |
| `shared_preload_libraries` | Appended with `pgaudit` |

!!! note

    To view the full list of parameters the Operator sets, run `patronictl show-config` inside a PostgreSQL Pod. See [Manage a database manually](manage-manually.md#override-postgresql-parameters) for details. Any changes you make via `patronictl edit-config` will be reverted when the Operator reconciles, unless the cluster is in [unmanaged mode](manage-manually.md#stop-reconciliation-by-putting-a-cluster-into-an-unmanaged-mode).

## PostgreSQL parameters that can be overridden

The following parameters are set by the Operator but you can override them via `patroni.dynamicConfiguration.postgresql.parameters`:

| Parameter | Default value |
| --------- | ------------- |
| `wal_level` | `logical` |
| `jit` | `off` |
| `password_encryption` | `scram-sha-256` |
| `archive_timeout` | `60s` |
| `huge_pages` | `try` or `off` (computed from resource limits) |
| `restore_command` | `pgbackrest --stanza=db archive-get %f "%p"`|

## Custom Resource options with modification limits

### `metadata.name`

The cluster name is set at creation time and cannot be changed. Kubernetes Custom Resource names are immutable. To use a different name, create a new cluster and migrate data.

### `users.databases`

You can add databases to a user's access list, but you cannot revoke access to a database once it has been granted. Removing a database from the list does not revoke existing privileges.

### `users.options`

The `ALTER ROLE` options (such as `SUPERUSER`) are ignored for the `postgres` user. The Operator manages the superuser role.

### `databaseInitSQL`

Initialization SQL runs only at cluster creation time. You cannot add or change init SQL for an existing cluster. The Operator executes the script once during bootstrap.

### `dataSource`

The `dataSource` subsection configures restore-from-backup for a *new* cluster. It applies only during initial cluster creation. You cannot change the data source of an existing cluster.

## Backup options

### Backup encryption

You cannot change encryption settings after backups are established. To enable encryption or change the encryption key, create a new repository. See [Backup encryption](backup-encryption.md).

### Storage size

You cannot shrink the size of an existing Persistent Volume Claim (PVC). Kubernetes allows only volume expansion. See [Scale storage](scaling-vertical.md#scale-storage).

## Patroni dynamic configuration

Only the `parameters` and `pg_hba` subsections under `patroni.dynamicConfiguration.postgresql` are applied. All other Patroni dynamic configuration options (such as `use_slots`, `use_pg_rewind`, or `loop_wait`) are ignored. See [Changing PostgreSQL options](options.md).

