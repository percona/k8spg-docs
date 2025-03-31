# Manual management of database clusters deployed with Percona Operator for PostgreSQL

The purpose of the Operator is to automate database management tasks for you. However, you may need to manage the database cluster manually. For example, to troubleshoot issues or for maintenance. 

Use the following sections to 

## Disabling health check probes for maintenance

Probes are tasks Kubernetes runs to gather information about the health and status of containers running within Pods. They serve as a mechanism to ensure the system is running smoothly by periodically checking the state of applications and services.

Sometimes it's necessary to take a manual control over the `postgres` process for maintenance. This means you need to disable a Kubernetes liveness probe so that it doesn't restart the database container during the maintenance period.

Here's what you need to do:

1. Create a `sleep-forever` file in the data directory with the following command:

    ```{.bash data-prompt="$"}
    $ kubectl exec cluster1-instance1-24b8-0 -- touch /pgdata/pg17/sleep-forever
    ```

2. Now you can stop PostgreSQL:

    ```{.bash data-prompt="$"}
    $ kubectl exec cluster1-instance1-24b8-0 -- patronictl pause
    ```

    ??? example "Expected output"

        ```{text .no-copy}
        Success: cluster management is paused
        ```

    ```{.bash data-prompt="$"}
    $ kubectl exec cluster1-instance1-24b8-0 -- pg_ctl -D /pgdata/pg17 stop
    ```

    ??? example "Expected output"

        ```{text .no-copy}
        waiting for server to shut down.... done
        server stopped
        ```

3. Optionally, you can delete the Pod:

    ```{.bash data-prompt="$"}
    $ kubectl delete pod cluster1-instance1-24b8-0
    ```

4. After the Pod restarts, it won't start PostgreSQL. You can check it with the following command:

   ```{.bash data-prompt="$"}
   $ kubectl logs cluster1-instance1-24b8-0 database
   ```

   ??? example "Expected output"

        ```{text .no-copy}
        The pgdata/sleep-forever file is detected, node entered an infinite sleep
        If you want to exit from the infinite sleep, remove the pgdata/sleep-forever file
        ```

4. Now you can start PostgreSQL manually:

    ```{.bash data-prompt="$"}
    $ kubectl exec cluster1-instance1-24b8-0 -- pg_ctl -D /pgdata/pg17 start
    ```

    ??? example "Expected output"

        ```{text .no-copy}
        waiting for server to start....2025-04-01 16:27:41.850 UTC [1434] LOG:  pgaudit extension initialized
        2025-04-01 16:27:42.075 UTC [1434] LOG:  redirecting log output to logging collector process
        2025-04-01 16:27:42.075 UTC [1434] HINT:  Future log output will appear in directory "log".
         done
        server started
        ```

## Putting a cluster into an unmanaged mode

The Operator reconciles the database cluster to ensure its current state doesn't differ from the state defined in the configuration. It can automatically install, update, or repair the cluster when needed.

By doing this, the Operator might interfere with your operations during  maintenance. Therefore, you can put a cluster in an unmanaged mode to stop the Operator from reconciling the cluster at all.

Edit the `deploy/cr.yaml` Custom Resource manifest and set the `spec.unmanaged` option to `true`:

```yaml
apiVersion: pgv2.percona.com/v2
kind: PerconaPGCluster
metadata:
  name: cluster1
spec:
  unmanaged: true
  ...
```

Apply the changes:

```{.bash data-prompt="$"}
$ kubectl apply -f deploy/cr.yaml -n <namespace>
```

!!! warning

    Putting a cluster in an unmanaged mode doesn't disable any of the health check probes already configured for containers. The Operator is only responsible for configuring the probes, not for running them. Refer to the [Disabling health check probes for maintenance](#disabling-health-check-probes-for-maintenance) section for the steps.

## Overriding Patroni configuration


### Overriding a cluster configuration

The Operator creates a ConfigMap called `<cluster-name>-config` to store Patroni cluster configuration. If you just edit the ConfigMap contents, the Operator will immediately rewrite and remove your changes. To override anything in this ConfigMap and keep the changes, you need to annotate it using a special annotation:

```{.bash data-prompt="$"}
$ kubectl annotate cm cluster1-config pgv2.percona.com/override-config=true
```

??? example "Expected output"

    ```{text .no-copy}
    configmap/cluster1-config annotated
    ```

As long as the ConfigMap has the `pgv2.percona.com/override-config` annotation, the Operator doesn't rewrite your changes. You can edit the ConfigMap's contents however you want.

!!! warning 

    The Operator doesn't validate your changes in configuration. Consult with [Patroni documentation :octicons-link-external-16:](https://patroni.readthedocs.io/en/latest/patroni_configuration.html) to ensure the configuration you define is correct and you don't face problems if you apply an invalid configuration.

It takes some time for your changes of ConfigMap to propagate to running containers. You can verify if changes are propagated by checking the mounted file in containers. For example:

```{.bash data-prompt="$"}
$ kubectl exec -it cluster1-instance1-24b8-0 -- cat /etc/patroni/~postgres-operator_cluster.yaml
```

Operator doesn't apply a new configuration automatically. You must run `patronictl reload` to apply it after your changes are propagated to the container.

!!! warning 

    Don't forget to remove this annotation once you finished. It's not recommended to use this feature to permanently override Patroni configuration. As long as this annotation exists, the Operator won't touch the ConfigMap and you might have problems with your cluster.

### Overriding an instance configuration

Operator creates a ConfigMap called `<pod-name>-config` to store Patroni instance configuration for each Pod.  If you just edit the ConfigMap contents, the Operator will immediately rewrite and remove your changes. To override anything in these ConfigMaps and keep the changes, you need to annotate them using a special annotation:

```{.bash data-prompt="$"}
$ kubectl annotate cm cluster1-instance1-24b8-config pgv2.percona.com/override-config=true
```

??? example "Expected output"

    ```{text .no-copy}
    configmap/cluster1-instance1-24b8-config annotated
    ```

As long as the ConfigMap has the `pgv2.percona.com/override-config` annotation, the Operator doesn't rewrite your changes. You can edit the ConfigMap's contents however you want.

!!! warning 

    The Operator doesn't validate your changes in configuration. Consult with [Patroni documentation :octicons-link-external-16:](https://patroni.readthedocs.io/en/latest/patroni_configuration.html) to ensure the configuration you define is correct and you don't face problems if you apply an invalid configuration.


It takes some time for your changes of ConfigMap to propagate to running containers. You can verify if changes are propagated by checking the mounted file in containers. For example:

```{.bash data-prompt="$"}
$ kubectl exec -it cluster1-instance1-24b8-0 -- cat /etc/patroni/~postgres-operator_cluster.yaml
```

Operator doesn't apply a new configuration automatically. You must run `patronictl reload` to apply it after your changes are propagated to the container.

!!! warning 

    Don't forget to remove this annotation once you finished. It's not recommended to use this feature to permanently override Patroni configuration. As long as this annotation exists, the Operator won't touch the ConfigMap and you might have problems with your cluster.

## Overriding PostgreSQL parameters

Use the `patronictl show-config` command to print PostgreSQL parameters used in the cluster. For example:

```{.bash data-prompt="$"}
$ kubectl exec cluster1-instance1-24b8-0 -- patronictl show-config
```

??? example "Expected output"

    ```{text .no-copy}
    loop_wait: 10
    postgresql:
      parameters:
        archive_command: 'pgbackrest --stanza=db archive-push "%p" && timestamp=$(pg_waldump "%p" | grep -oP "COMMIT \K[^;]+" | sed -E "s/([0-9]{4}-[0-9]{2}-[0-9]{2}) ([0-9]{2}:[0-9]{2}:[0-9]{2}\.[0-9]{6}) (UTC|[\\+\\-][0-9]{2})/\1T\2\3/" | sed "s/UTC/Z/" | tail -n 1 | grep -E "^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}\.[0-9]{6}(Z|[\+\-][0-9]{2})$"); if [ ! -z ${timestamp} ]; then echo ${timestamp} > /pgdata/latest_commit_timestamp.txt; fi'
        archive_mode: 'on'
        archive_timeout: 60s
        huge_pages: 'off'
        jit: 'off'
        password_encryption: scram-sha-256
        restore_command: pgbackrest --stanza=db archive-get %f "%p"
        ssl: 'on'
        ssl_ca_file: /pgconf/tls/ca.crt
        ssl_cert_file: /pgconf/tls/tls.crt
        ssl_key_file: /pgconf/tls/tls.key
        track_commit_timestamp: 'true'
        unix_socket_directories: /tmp/postgres
        wal_level: logical
      pg_hba:
      - local all "postgres" peer
      - hostssl replication "_crunchyrepl" all cert
      - hostssl "postgres" "_crunchyrepl" all cert
      - host all "_crunchyrepl" all reject
      - host all "monitor" "127.0.0.0/8" scram-sha-256
      - host all "monitor" "::1/128" scram-sha-256
      - host all "monitor" all reject
      - hostssl all "_crunchypgbouncer" all scram-sha-256
      - host all "_crunchypgbouncer" all reject
      - hostssl all all all md5
      use_pg_rewind: true
      use_slots: false
    ttl: 30
    ```

Use the `patronictl edit-config` command to change any PostgreSQL parameter.

For example, run the following command to change the `restore_command` parameter:

```{.bash data-prompt="$"}
$ kubectl exec -it cluster1-instance1-24b8-0 -- patronictl edit-config --pg restore_command=/bin/true
```

??? example "Expected output"

    ```{text .no-copy}
    ---
    +++
    @@ -9,7 +9,7 @@
         huge_pages: 'off'
         jit: 'off'
         password_encryption: scram-sha-256
    -    restore_command: pgbackrest --stanza=db archive-get %f "%p"
    +    restore_command: /bin/true
         ssl: 'on'
         ssl_ca_file: /pgconf/tls/ca.crt
         ssl_cert_file: /pgconf/tls/tls.crt    

    Apply these changes? [y/N]:
    ```

This command changes the `shared_preload_libraries` parameter:

```{.bash data-prompt="$"}
$ kubectl exec -it cluster1-instance1-24b8-0 -- patronictl edit-config --pg shared_preload_libraries=""
```

??? example "Expected output"

    ```{text .no-copy}
    ---
    +++
    @@ -11,7 +11,6 @@
         password_encryption: scram-sha-256
         pg_stat_monitor.pgsm_query_max_len: '2048'
         restore_command: pgbackrest --stanza=db archive-get %f "%p"
    -    shared_preload_libraries: pg_stat_monitor
         ssl: 'on'
         ssl_ca_file: /pgconf/tls/ca.crt
         ssl_cert_file: /pgconf/tls/tls.crt    

    Apply these changes? [y/N]:
    ```

!!! warning

    If you update any object controlled by operator, it'll reconcile the cluster and your configuration changes will be reverted. You can [put the cluster in an unmanaged mode](putting-a-cluster-into-an-unmanaged-mode) to prevent this.

## Overriding `pg_hba` entries

You may want to append entries to `pg_hba`. You can use the `spec.patroni.postgresl.pg_hba` field to add your rules. 

```yaml
  patroni:
    dynamicConfiguration:
      postgresql:
        pg_hba:
          local all all trust
          reject all all all
```

The order of parameters matters in `pg_hba.conf`, so consider overriding the list completely. For this, you can use the `patronictl edit-config` command:

```{.bash data-prompt="$"}
$ kubectl exec -it cluster1-instance1-24b8-0 -- patronictl edit-config --set postgresql.pg_hba='[
  "local all all trust",
  "reject all all all"
]'
```

!!! warning

    If you update any object controlled by operator, it'll reconcile the cluster and your configuration changes will be reverted. You can [put the cluster in an unmanaged mode](putting-a-cluster-into-an-unmanaged-mode) to prevent this.