# Reinitialize replicas

When you create a new Percona PostgreSQL cluster, the Operator uses the `basebackup` method to create replicas for it. After the database instances are ready, the Operator automatically creates a full backup. Once this backup finishes successfully, the Operator updates the Patroni configuration and **prepends** (puts as the first method)  `pgBackRest` in the `create_replica_methods` list so that new replicas are created using it.

!!! warning

    The Operator doesn't run `patronictl reload` in old replicas even if Patroni instance configurations are updated to put `pgBackRest` as the first method in the `create_replica_methods` list. For this configuration to run into force, you need to either restart the Pods or manually run `patronictl reload <cluster_name>` on all old replicas.

You may need to reinitialize cluster replicas. For example, if the data on the replica becomes corrupted or inconsistent with the primary node. Reinitialization ensures the replica is rebuilt with the correct data. Or, if the replica falls significantly behind the primary or encounters issues that prevent successful synchronization, reinitialization can reset the replica to match the current state of the primary.

This document provides the ways how to do it.

## Reinitialize by deleting replica Pod and its PersistentVolumeClaim

You can force reinitialization by deleting the Pod and its PersistentVolumeClaim:

```{.bash data-prompt="$"}
$ kubectl delete pvc/cluster1-instance1-24b8-pgdata pod/cluster1-instance1-24b8-0
```

??? example "Expected output"

    ```{text .no-copy}
    persistentvolumeclaim "cluster1-instance1-24b8-pgdata" deleted
    pod "cluster1-instance1-24b8-0" deleted
    ```

The Operator will reinitialize a replica using the method configured in this instance's Patroni configuration. This configuration is stored within the ConfigMap for the instance. Use the following command to find it: 


```{.bash data-prompt="$"}
$ kubectl get cm cluster1-instance1-24b8-config
```

??? example "Expected output"

    ```{text .no-copy}
    NAME                             DATA   AGE
    cluster1-instance1-24b8-config   1      95m
    ```

## Reinitialize with `patronictl reinit`

You can reinitialize a replica using the `patronictl reinit` command. Note that configuration in ConfigMap might not have been applied to a running Patroni instance. The recommended approach is to first run `patronictl reload <cluster_name>` and then run `patronictl reinit`.

For example:

1. List and verify Patroni configuration:

    ```{.bash data-prompt="$"}
    $ kubectl exec -it cluster1-instance1-24b8-0 -- cat /etc/patroni/~postgres-operator_instance.yaml
    ```

2. Find the cluster name:

    ```{.bash data-prompt="$"}
    $ kubectl exec -it cluster1-instance1-24b8-0 -- patronictl list
    ```

    ??? example "Expected output"
        
        ```{.text .no-copy}
        Cluster: cluster1-ha (7523193408153182293) -------------------------+---------+-----------+----+-----------+
        | Member                    | Host                                    | Role    | State     | TL | Lag in MB |
        +---------------------------+-----------------------------------------+---------+-----------+----+-----------+
        | cluster1-instance1-24b8-0 | cluster1-instance1-bw58-0.cluster1-pods | Replica | streaming |  3 |         0 |
        | cluster1-instance1-84xm-0 | cluster1-instance1-tmqj-0.cluster1-pods | Leader  | running   |  3 |           |
        | cluster1-instance1-nv28-0 | cluster1-instance1-xf85-0.cluster1-pods | Replica | streaming |  3 |         0 |
        +---------------------------+-----------------------------------------+---------+-----------+----+-----------+
        ```

3. Reload the configuration:

    ```{.bash data-prompt="$"}
    $ kubectl exec -it cluster1-instance1-24b8-0 -- patronictl reload cluster1-ha cluster1-instance1-24b8-0
    ```
    
    ??? example "Expected output"

        ```{text .no-copy}
        + Cluster: cluster1-ha (7487948770079264836) -------------------------+---------+-----------+----+-----------+
        | Member                    | Host                                    | Role    | State     | TL | Lag in MB |
        +---------------------------+-----------------------------------------+---------+-----------+----+-----------+
        | cluster1-instance1-24b8-0 | cluster1-instance1-24b8-0.cluster1-pods | Replica | streaming |  1 |         0 |
        | cluster1-instance1-84xm-0 | cluster1-instance1-84xm-0.cluster1-pods | Leader  | running   |  1 |           |
        | cluster1-instance1-nv28-0 | cluster1-instance1-nv28-0.cluster1-pods | Replica | streaming |  1 |         0 |
        +---------------------------+-----------------------------------------+---------+-----------+----+-----------+
        Are you sure you want to reload members cluster1-instance1-24b8-0? [y/N]: y
        Reload request received for member cluster1-instance1-24b8-0 and will be processed within 10 seconds
        ```

3. Reinitialize the replica:

    ```{.bash data-prompt="$"}
    $ kubectl exec -it cluster1-instance1-24b8-0 -- patronictl reinit cluster1-ha cluster1-instance1-24b8-0
    ```

    ??? example "Expected output"

    ```{text .no-copy}
    + Cluster: cluster1-ha (7487948770079264836) -------------------------+---------+-----------+----+-----------+
    | Member                    | Host                                    | Role    | State     | TL | Lag in MB |
    +---------------------------+-----------------------------------------+---------+-----------+----+-----------+
    | cluster1-instance1-24b8-0 | cluster1-instance1-24b8-0.cluster1-pods | Replica | streaming |  1 |         0 |
    | cluster1-instance1-84xm-0 | cluster1-instance1-84xm-0.cluster1-pods | Leader  | running   |  1 |           |
    | cluster1-instance1-nv28-0 | cluster1-instance1-nv28-0.cluster1-pods | Replica | streaming |  1 |         0 |
    +---------------------------+-----------------------------------------+---------+-----------+----+-----------+
    Are you sure you want to reinitialize members cluster1-instance1-24b8-0? [y/N]: y
    Success: reinitialize for member cluster1-instance1-24b8-0
    ```

## Configure `create_replica_methods` 

The Operator uses `basebackup` and `pgBackRest` methods to create replicas by default. These methods are defined within the `create_replica_methods` configuration block of a Patroni instance.

If you want to change `create_replica_methods` list for any reason, you can use the `spec.patroni.create_replica_methods` option in the `deploy/cr.yaml` Custom Resource manifest:

```yaml
apiVersion: pgv2.percona.com/v2
kind: PerconaPGCluster
metadata:
  name: cluster1
spec:
  patroni:
    createReplicaMethods:
    - basebackup
    - pgbackrest
  ...
```

Apply this configuration:

```{.bash data-prompt="$"}
$ kubectl apply -f deploy/cr.yaml
```

The Operator updates Patroni instances' ConfigMaps. You can check their configuration with this command:

```{.bash data-prompt="$"}
$ kubectl get configmap cluster1-instance1-24b8-config -o yaml
```

??? example "Expected output"

    ```yaml
    apiVersion: v1
    kind: ConfigMap
    metadata:
      name: cluster1-instance1-24b8-config
    data:
      patroni.yaml: |
        # Generated by postgres-operator. DO NOT EDIT UNLESS YOU KNOW WHAT YOU'RE DOING.
        # If you want to override the config, annotate this ConfigMap with pgv2.percona.com/override-config=true
        kubernetes: {}
        postgresql:
          basebackup:
          - waldir=/pgdata/pg17_wal
          create_replica_methods:
          - basebackup
          - pgbackrest
          pgbackrest:
            command: '''bash'' ''-ceu'' ''--'' ''install --directory --mode=0700 "${PGDATA?}"
              && exec "$@"'' ''-'' ''pgbackrest'' ''restore'' ''--delta'' ''--stanza=db''
              ''--repo=1'' ''--link-map=pg_wal=/pgdata/pg17_wal'' ''--type=standby'''
            keep_data: true
            no_leader: true
            no_params: true
          pgpass: /tmp/.pgpass
          use_unix_socket: true
        restapi: {}
        tags: {}
    ```

After the ConfigMap is updated, it takes some time for changes to appear in mounted files in containers. You can verify the updates by manually checking the file:

```{.bash data-prompt="$"}
$ kubectl exec -it cluster1-instance1-24b8-0 -- cat /etc/patroni/~postgres-operator_instance.yaml
```

??? example "Expected output"

    ```yaml
    # Generated by postgres-operator. DO NOT EDIT UNLESS YOU KNOW WHAT YOU'RE DOING.
    # If you want to override the config, annotate this ConfigMap with pgv2.percona.com/override-config=true
    kubernetes: {}
    postgresql:
      basebackup:
      - waldir=/pgdata/pg17_wal
      create_replica_methods:
      - basebackup
      - pgbackrest
      pgbackrest:
        command: '''bash'' ''-ceu'' ''--'' ''install --directory --mode=0700 "${PGDATA?}"
          && exec "$@"'' ''-'' ''pgbackrest'' ''restore'' ''--delta'' ''--stanza=db''
          ''--repo=1'' ''--link-map=pg_wal=/pgdata/pg17_wal'' ''--type=standby'''
        keep_data: true
        no_leader: true
        no_params: true
      pgpass: /tmp/.pgpass
      use_unix_socket: true
    restapi: {}
    tags: {}
    ```

Though the Operator updates the ConfigMaps, it doesn't automatically apply the new configuration for Patroni. To make Patroni aware of the changes, reload its configuration on every instance with the `patronictl reload <cluster_name> <pod-name>` command. 