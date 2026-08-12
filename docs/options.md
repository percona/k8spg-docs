# Changing PostgreSQL options

You can pass PostgreSQL parameters to cluster instances through the Custom Resource.
The Operator applies them with
[Patroni dynamic configuration :octicons-link-external-16:](https://patroni.readthedocs.io/en/latest/dynamic_configuration.html).

Operator defaults for some PostgreSQL parameters can differ from upstream PostgreSQL defaults. Before you change
a parameter, check whether the Operator already sets it and whether you can
override that value. See [Immutable options](immutable-options.md) for the list of parameters that you can and cannot override.

To inspect the effective Patroni configuration for a running cluster, use
`patronictl show-config` inside a PostgreSQL Pod. See
[Manage a database manually](manage-manually.md#override-postgresql-parameters).

This page shows how to pass additional options to PostgreSQL.

## How to pass PostgreSQL options

Add parameters under `patroni.dynamicConfiguration.postgresql.parameters` in your
`deploy/cr.yaml` Custom Resource:

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

The Operator applies the changes to new clusters at creation time and to existing
clusters at runtime.

Most options take effect without a PostgreSQL server restart. Some options, such
as `shared_buffers` or `wal_level`, have the
[postmaster context :octicons-link-external-16:](https://www.postgresql.org/docs/current/view-pg-settings.html)
and require a restart. For those options, Patroni performs a rolling restart of
all PostgreSQL Pods after you apply the change. To check whether an option requires
a restart, run in PostgreSQL: `SELECT name, context FROM pg_settings;`

!!! important

    The Operator does not validate the options it passes to Patroni. Invalid
    values can make the cluster unavailable. Also, only PostgreSQL parameters in
    the `patroni.dynamicConfiguration.postgresql.parameters` subsection are applied.
    Other Patroni options in the `patroni.dynamicConfiguration` subsection are
    ignored.

### Example: override an Operator default (`wal_level`)

The Operator sets `wal_level` to `logical` by default. That value supports
logical replication and also increases WAL volume and I/O compared with
`replica`.

Supported values in Operator-managed clusters are:

* `logical` (Operator default) — required for logical replication
* `replica` — enough for physical replication and most workloads that do not
  need logical replication

Both values allow point-in-time recovery. The value `minimal` is rejected by
validation rules because other required settings, such as `hot_standby`, need
more WAL data.

Read more about what `wal_level` controls in the
[PostgreSQL documentation :octicons-link-external-16:](https://www.postgresql.org/docs/current/runtime-config-wal.html#RUNTIME-CONFIG-WAL-SETTINGS).

To lower WAL overhead when you do not need logical replication, set the `wal_level` to `replica` under `patroni.dynamicConfiguration.postgresql.parameters` in the Custom Resource:

```yaml
...
patroni:
  dynamicConfiguration:
    postgresql:
      parameters:
        wal_level: replica
```

`wal_level` has the postmaster context. After you change it, Patroni restarts
all PostgreSQL instances.

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
