# Troubleshooting clusters deployed with Percona Operator for PostgreSQL

## Disabling health check probes for maintenance

Sometimes it's necessary to take manual control over postgres process for maintenance. For this you can create `sleep-forever` file in data directory to disable liveness probes.

For example:
```
kubectl exec cluster1-instance1-24b8-0 -- touch /pgdata/pg17/sleep-forever
```

Then you can delete the pod:
```
kubectl delete pod cluster1-instance1-24b8-0
```

After pod is restarted, it won't start PostgreSQL. You can start it manually.

TODO: I need to test sleep-forever changes to complete these instructions.

## Putting cluster into unmanaged mode

During the maintenance, operator might interfere with your operations. You can put cluster in unmanaged mode to stop operator reconciling cluster at all.

```
apiVersion: pgv2.percona.com/v2
kind: PerconaPGCluster
metadata:
  name: cluster1
spec:
  unmanaged: true
  ...
```

WARNING: This won't disable any of the health check probes already configured for containers. Operator is only responsible for configuring the probes, not for running them.

## Overriding Patroni configuration

### Overriding cluster configuration

Operator creates a ConfigMap called `<cluster-name>-config` to store Patroni cluster configuration. If you edit its contents, operator will immediately rewrite and remove your changes. If you need to override anything in this ConfigMap, you need to annotate it using a special annotation:

```
$ kubectl annotate cm cluster1-config pgv2.percona.com/override-config=true
configmap/cluster1-config annotated
```

As long as the ConfigMap has `pgv2.percona.com/override-config` annotation, operator won't rewrite your changes. You can edit ConfigMap's contents however you want.

WARNING: Operator won't validate your changes in configuration. You'll face problems if you apply an invalid configuration.

After changing the contents of ConfigMap some time is needed for your changes to propagate to running containers. You can verify if changes are propagated by checking the mounted file in containers. For example:

```
$ kubectl exec -it cluster1-instance1-24b8-0 -- cat /etc/patroni/~postgres-operator_cluster.yaml
```

Operator won't apply new configuration automatically. It's up to you to run `patronictl reload` after your changes are propagated to the container.

WARNING: Don't forget to remove this annotation once you finished. It's not recommended to use this feature to permanently override Patroni configuration. As long as this annotation exists, operator won't touch the ConfigMap and you might have problems with your cluster.

### Overriding instance configuration

Operator creates a ConfigMap called `<pod-name>-config` to store Patroni instance configuration for each pod. If you edit their contents, operator will immediately rewrite and remove your changes. If you need to override anything in these ConfigMaps, you need to annotate them using a special annotation:

```
$ kubectl annotate cm cluster1-instance1-24b8-config pgv2.percona.com/override-config=true
configmap/cluster1-instance1-24b8-config annotated
```

As long as the ConfigMap has `pgv2.percona.com/override-config` annotation, operator won't rewrite your changes. You can edit ConfigMap's contents however you want.

WARNING: Operator won't validate your changes in configuration. You'll face problems if you apply an invalid configuration.

After changing the contents of ConfigMap some time is needed for your changes to propagate to running containers. You can verify if changes are propagated by checking the mounted file in containers. For example:

```
$ kubectl exec -it cluster1-instance1-24b8-0 -- cat /etc/patroni/~postgres-operator_instance.yaml
```

Operator won't apply new configuration automatically. It's up to you to run `patronictl reload` after your changes are propagated to the container.

WARNING: Don't forget to remove this annotation once you finished. It's not recommended to use this feature to permanently override Patroni configuration. As long as this annotation exists, operator won't touch the ConfigMap and you might have problems with your cluster.

## Overriding PostgreSQL parameters

You can use `patronictl show-config` to print PostgreSQL parameters used in the cluster. For example:

```
$ kubectl exec cluster1-instance1-24b8-0 -- patronictl show-config
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

If you want to change any parameter, you can use `patronictl edit-config`.

For example to change `restore_command`:

```
$ kubectl exec -it cluster1-instance1-24b8-0 -- patronictl edit-config --pg restore_command=/bin/true
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

Or to change `shared_preload_libraries`:

```
$ kubectl exec -it cluster1-instance1-24b8-0 -- patronictl edit-config --pg shared_preload_libraries=""
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

WARNING: If you update any object controlled by operator, it'll reconcile the cluster and your configuration changes will be reverted. You can put cluster in unmanaged mode as described above to prevent this.

## Overriding pg_hba entries

If you want to append entries to `pg_hba`, you can use `spec.patroni.postgresl.pg_hba` field to add your rules. Since order matters in pg_hba.conf, you might want to override the list completely. For this you can use `patronictl edit-config`:

```
$ kubectl exec -it cluster1-instance1-24b8-0 -- patronictl edit-config --set postgresql.pg_hba='[
  "local all all trust",
  "reject all all all"
]'
```

WARNING: If you update any object controlled by operator, it'll reconcile the cluster and your configuration changes will be reverted. You can put cluster in unmanaged mode as described above to prevent this.
