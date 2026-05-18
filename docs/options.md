# Changing PostgreSQL options

You may need to pass specific options to PostgreSQL instances directly, beyond the default configuration and options, available in the Custom Resource. For this purpose, use the [PostgreSQL dynamic configuration method
:octicons-link-external-16:](https://patroni.readthedocs.io/en/latest/dynamic_configuration.html) provided by Patroni. You can pass PostgreSQL options to Patroni through the Custom Resource. The Operator uses
[Patroni dynamic configuration :octicons-link-external-16:](https://patroni.readthedocs.io/en/latest/dynamic_configuration.html)
to apply your changes.

Add your PostgreSQL options to the `patroni.dynamicConfiguration.postgresql.parameters`
section in your `deploy/cr.yaml` Custom Resource:

```yaml
...
patroni:
  dynamicConfiguration:
    postgresql:
      parameters:
        max_parallel_workers: 2
        max_worker_processes: 2
        shared_buffers: 1GB
        work_mem: 2MB
```

Apply the updated Custom Resource:

```bash
kubectl apply -f deploy/cr.yaml
```

This dynamically applies the changes to PostgreSQL instances both for new clusters during cluster creation and existing clusters at runtime.

Most options take effect without
a PostgreSQL server restart. Some options, such as `wal_level` and `shared_buffers`, have the
[postmaster context :octicons-link-external-16:](https://www.postgresql.org/docs/current/view-pg-settings.html)
and require a PostgreSQL restart. For these options, Patroni performs a rolling
restart of all instances after you apply the change. To check whether an option
requires a restart, run in PostgreSQL: `SELECT name, context FROM pg_settings;`

!!! note

    The Operator does not validate the options it passes to Patroni. Invalid
    values can make the cluster unavailable. Also, only PostgreSQL parameters in the
    `patroni.dynamicConfiguration.postgresql.parameters` subsection are applied. Other Patroni options in
    `patroni.dynamicConfiguration` subsection are ignored.

## Configuring wal_level

The `wal_level` option controls how much information is written to PostgreSQL WAL
files. You can set it in `patroni.dynamicConfiguration.postgresql.parameters`:


* `replica` (PostgreSQL default) — sufficient for physical replication and most
  workloads
* `logical` (Operator default) — required for logical replication; increases WAL volume and I/O.

Read more about `wal_level` values in [PostgreSQL documentation :octicons-link-external-16:](https://www.postgresql.org/docs/current/runtime-config-wal.html#RUNTIME-CONFIG-WAL-SETTINGS).

!!! note
    
    Though the `wal_level` option can also have the value `minimal`, it will be rejected by the validation rules, since other parameters, such as `hot_standby`, require more WAL data. 

```yaml
...
patroni:
  dynamicConfiguration:
    postgresql:
      parameters:
        wal_level: replica
```

Use `replica` when you need physical replication or no replication. Use
`logical` when you need logical replication. Both values allow for point-in-time recovery.

The `wal_level` parameter has the
postmaster context. After you change it, Patroni restarts all PostgreSQL instances.

!!! note

    The Operator manages certain PostgreSQL parameters (such as `archive_mode`, `archive_command`, `restore_command`, and TLS settings) internally and reverts any user changes. Other parameters (such as `wal_level`, `archive_timeout`, `jit`) can be overridden. See [Immutable options](immutable-options.md) for the full list.


## Using host-based authentication (pg_hba)

PostgreSQL Host-Based Authentication (pg_hba) controls database access based on
the client IP or hostname. Configure it in the
`patroni.dynamicConfiguration.postgresql.pg_hba` section of the Custom Resource:

```yaml
...
patroni:
  dynamicConfiguration:
    postgresql:
      pg_hba:
      - host    all all 0.0.0.0/0 md5
```

This example allows all hosts to connect to any database using MD5 password
authentication.

You can use both `parameters` and `pg_hba` in the same configuration:

```yaml
...
patroni:
  dynamicConfiguration:
    postgresql:
      parameters:
        max_parallel_workers: 2
        max_worker_processes: 2
        shared_buffers: 1GB
        work_mem: 2MB
      pg_hba:
      - local   all all trust
      - host    all all 0.0.0.0/0 md5
      - host    all all ::1/128   md5
      - host    all mytest 123.123.123.123/32 reject
```

Apply the changes with `kubectl apply -f deploy/cr.yaml`.
