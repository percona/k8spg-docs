# Reinitialize replicas

When you create a new Percona PostgreSQL cluster, the Operator uses the `basebackup` method to create replicas for it. After the database instances are ready, the Operator automatically creates a full backup. Once this backup finishes successfully, the Operator updates the Patroni configuration and **prepends** (puts as the first method)  `pgBackRest` in the `create_replica_methods` list so that new replicas are created using it.

!!! warning

    The Operator doesn't run `patronictl reload` in old replicas even if Patroni instance configurations are updated to put `pgBackRest` as the first method in the `create_replica_methods` list. For this configuration to run into force, you need to either restart the Pods or manually run `patronictl reload <cluster_name>` on all old replicas.

You may need to reinitialize cluster replicas. For example, if the data on the replica becomes corrupted or inconsistent with the primary node. Reinitialization ensures the replica is rebuilt with the correct data. Or, if the replica falls significantly behind the primary or encounters issues that prevent successful synchronization, reinitialization can reset the replica to match the current state of the primary.

You can do this:

* Manually by operating the database cluster. This is the recommended approach as you have the full control over the data state in your database.
* Automatically via Patroni. When Patroni notices the timelines between the primary and a replica diverged and the replica cannot stream from a primary, it automatically removes the data directory and recreates the replica to ensure it rejoins the cluster. Note that in this flow the Operator cannot ensure all transactions are replicated somewhere and it might potentially result in data loss. 

This document provides the steps how to do it both ways.

## Reinitialize by deleting replica Pod and its PersistentVolumeClaim

You can force reinitialization by deleting the Pod and its PersistentVolumeClaim:

```bash
kubectl delete pvc/cluster1-instance1-24b8-pgdata pod/cluster1-instance1-24b8-0
```

??? example "Expected output"

    ```{text .no-copy}
    persistentvolumeclaim "cluster1-instance1-24b8-pgdata" deleted
    pod "cluster1-instance1-24b8-0" deleted
    ```

The Operator will reinitialize a replica using the method configured in this instance's Patroni configuration. This configuration is stored within the ConfigMap for the instance. Use the following command to find it: 


```bash
kubectl get cm cluster1-instance1-24b8-config
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

    ```bash
    kubectl exec -it cluster1-instance1-24b8-0 -- cat /etc/patroni/~postgres-operator_instance.yaml
    ```

2. Find the cluster name:

    ```bash
    kubectl exec -it cluster1-instance1-24b8-0 -- patronictl list
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

    ```bash
    kubectl exec -it cluster1-instance1-24b8-0 -- patronictl reload cluster1-ha cluster1-instance1-24b8-0
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

    ```bash
    kubectl exec -it cluster1-instance1-24b8-0 -- patronictl reinit cluster1-ha cluster1-instance1-24b8-0
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

```bash
kubectl apply -f deploy/cr.yaml
```

The Operator updates Patroni instances' ConfigMaps. You can check their configuration with this command:

```bash
kubectl get configmap cluster1-instance1-24b8-config -o yaml
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

```bash
kubectl exec -it cluster1-instance1-24b8-0 -- cat /etc/patroni/~postgres-operator_instance.yaml
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

## Automate replica reinitialization with Patroni

You can instruct Patroni to reinitialize the replica when it detects that the replica's timeline diverges from the primary one. Update the Custom Resource and set the `.spec.patroni.removeDataDirectoryOnDivergedTimelines` option:

```yaml
spec:
  patroni:
    removeDataDirectoryOnDivergedTimeline: true
```

Apply the configuration for the changes to come into force:

```bash
kubectl apply -f deploy/cr.yaml
```

!!! warning

    The `removeDataDirectoryOnDivergedTimelines` option can lead to data loss.
    When the Operator resyncs the replica automatically, some transactions may
    be lost. The risk is usually small but not zero. Use this option only if you
    understand and accept this trade-off.
