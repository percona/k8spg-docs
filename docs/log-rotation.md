# Log rotation

!!! admonition "Version added: [3.1.0](ReleaseNotes/Kubernetes-Operator-for-PostgreSQL-RN3.1.0.md)"

`logrotate` controls the growth of log files on PostgreSQL instance Pods. Without rotation, PostgreSQL and `pgBackRest` logs can grow until they consume the Persistent Volume and affect database stability. `logrotate` keeps retention and disk usage predictable.

In Percona Operator for PostgreSQL, `logrotate` runs in a dedicated `logrotate` sidecar container on every instance Pod when [persistent logging](persistent-logging.md) is enabled. It reads the log files at the specified path and rotates them according to the set of rules.


By default, `logrotate` rotates logs as follows:

* **PostgreSQL server `*.log` and `*.csv` log files** under `/pgdata/pgNN/log/`:
  
    * Rotates log files when they reach 100 megabytes in size (`size 100M`). This acts as a safety measure to prevent the logs from using too much disk space. The rotation by size does not replace or interfere with PostgreSQL's built-in log rotation, which is based on the age or time of the log files using the `logging_collector` setting. This ensures both rotation methods work together without causing conflicts.
    * Keeps up to 7 rotated files
    * Uses `copytruncate`, which means `logrotate` copies the log file contents to a rotated file and empties the original file in place. This allows processes like PostgreSQL and pgBackRest to keep writing to the same log file without needing to close and reopen it, ensuring uninterrupted logging during rotation.

* **pgBackRest client logs on instance Pods** under `/pgdata/pgbackrest/log/*.log`:
  
    * Rotates daily, or earlier when a file reaches 100 megabytes in size (`maxsize 100M`)
    * Keeps up to 7 rotated files
    * Uses `copytruncate`
    * Skips missing or empty log files and leaves rotated logs uncompressed
    * Runs on schedule. By default, this is once per day at midnight.


## Configure log rotation

You can customize log rotation if you need different retention, size limits, or want to rotate additional files. Configure it in these ways:

* Override the default logrotate configuration via the Custom Resource
* Add additional configuration via a ConfigMap
* Set a custom log rotation schedule

When you change logrotate configuration, the Operator updates the configuration hash and makes a rolling restart of the instance Pods.

### Override the default logrotate configuration

Use the `spec.logcollector.logRotate.configuration` section in the Custom Resource to completely override the default `logrotate` settings for the Operator-managed `postgres.conf` snippet.

!!! important

    You must provide the full `logrotate` configuration because the Operator replaces the default configuration with the one you provide. Refer to the [default configuration :octicons-link-external-16:](https://github.com/percona/percona-postgresql-operator/blob/main/build/postgres-operator/logcollector/logrotate/logrotate.conf) to see the built-in rules and use it as a guide for your custom settings.

Here's an example configuration that rotates PostgreSQL logs hourly and keeps three copies:

```yaml
spec:
  logcollector:
    enabled: true
    image: docker.io/percona/fluentbit:{{logcollector}}
    logRotate:
      schedule: "0 * * * *"
      configuration: |
        /pgdata/pg*/log/*.log
        /pgdata/pg*/log/*.csv {
          hourly
          rotate 3
          missingok
          notifempty
          copytruncate
          sharedscripts
        }
```

Apply the configuration:

```bash
kubectl apply -f deploy/cr.yaml -n <namespace>
```

### Extend the default configuration via ConfigMap

You can pass additional logrotate rules via a ConfigMap. Use `spec.logcollector.logRotate.extraConfig.name` to load additional `.conf` files from that ConfigMap. The file name must end with `.conf`.

!!! important

    The `postgres.conf` key name is reserved for the Operator-managed main configuration. Do not use it in your custom ConfigMap.

For example, you want to record that a log rotation ran. To do that, add a postrotate script to your logrotate configuration. After logrotate finishes rotating the matched files, it appends a timestamped line to a file on the data volume

1. Create a ConfigMap. For example, `custom-logrotate.yaml`:

    ```yaml title="custom-logrotate.yaml"
    apiVersion: v1
    kind: ConfigMap
    metadata:
      name: my-logrotate-extra
      namespace: <namespace>
    data:
      extra.conf: |
        /pgdata/pg18/log/*.log {
            daily
            rotate 7
            missingok
            notifempty
            copytruncate
            sharedscripts
            postrotate
                echo "$(date -u +%FT%TZ) rotated on $POD_NAME" >> /pgdata/logrotate-postrotate.log
            endscript
        }      
    ```

2. Create the ConfigMap:

    ```bash
    kubectl apply -f custom-logrotate.yaml -n <namespace>
    ```

3. Reference it in the Custom Resource:

    ```yaml
    spec:
      logcollector:
        enabled: true
        image: docker.io/percona/fluentbit:{{logcollector}}
        logRotate:
          extraConfig:
            name: my-logrotate-config
    ```

4. Apply the Custom Resource:

    ```bash
    kubectl apply -f deploy/cr.yaml -n <namespace>
    ```

### Set a custom schedule

Use `spec.logcollector.logRotate.schedule` to set the rotation schedule as a [cron :octicons-link-external-16:](https://en.wikipedia.org/wiki/Cron) expression. The default is once per day at midnight (`0 0 * * *`).

This example runs log rotation every 6 hours:

```yaml
spec:
  logcollector:
    enabled: true
    image: docker.io/percona/fluentbit:{{logcollector}}
    logRotate:
      schedule: "0 */6 * * *"
```

Apply the Custom Resource:

```bash
kubectl apply -f deploy/cr.yaml -n <namespace>
```

