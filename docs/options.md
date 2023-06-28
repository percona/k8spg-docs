# Changing PostgreSQL Options

You may require a configuration change for your application. PostgreSQL
allows the option to configure the database with a configuration file, as many other database
management systems do. You can pass options to PostgreSQL instances using the
specific Custom Resource option via the `deploy/cr.yaml` configuration file.

Often there's no need to add custom options, as the Operator takes care of
providing PostgreSQL with reasonable defaults.

The `patroni` section in the Custom Resource, present in `deploy/cr.yaml` file,
contains configuration options to customize the PostgreSQL high-availability
implementation based on [Patroni](https://patroni.readthedocs.io/).

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

Please note that configuration changes are automatically applied to the running instances
without validation, so having an invalid config can make the cluster unavailable. 
Also, take into account that some PosgreSQL options can't be applied dynamically but
require restarting to be applied.
