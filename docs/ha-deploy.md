# High availability

High availability (HA) ensures that your PostgreSQL database remains accessible even in the event of node or pod failures. With the Percona Operator for PostgreSQL, high availability is achieved by running multiple PostgreSQL nodes in a cluster, using the Patroni framework for automated failover and PostgreSQL streaming replication for data consistency.

A PostgreSQL cluster consists of the following members:

- A Primary node handles all write operations. The Primary continuously streams changes to its Standby nodes.
- Read-only (Standby in PostgreSQL terminology) replicas that continuously receive and replay changes from the Primary node. If the Primary fails, one of the Standbys can be automatically promoted to become the new Primary.

**Data replication**

Percona Operator leverages PostgreSQL streaming replication to keep Standby nodes up-to-date.

By default, **asynchronous replication** is used: the Primary sends changes to Standbys, but does not wait for confirmation before committing transactions. This offers better performance but presents a risk of minimal data loss (transactions not yet copied to a Standby could be lost in a failure).

**Synchronous replication** is also supported. In this replication type the Primary waits for at least one Standby to acknowledge receipt of data before marking a transaction as committed. This minimizes the risk of data loss, but can be slightly slower since each transaction must wait for a confirmation.

**Minimum and recommended number of nodes for high availability:**

The absolute minimum that can technically work for high availability is **2 nodes**. But this does not provide full high availability or protection against split-brain scenarios since the loss of either node can impact availability and data safety.

The recommended number of nodes for high availability setups is **3 or more PostgreSQL nodes**.

## Adding nodes to a cluster

There are two ways how to control the number replicas in your HA cluster:

1. Through changing `spec.instances.replicas` value
2. By adding new entry into `spec.instances`

### Using `spec.instances.replicas`

For example, you have the following Custom Resource manifest:

```yaml
spec:
...
  instances:
    - name: instance1
      replicas: 2
```

This will provision a cluster with two nodes - one Primary and one Replica.
Add the node by changing the manifest...

```yaml hl_lines="5"
spec:
...
  instances:
    - name: instance1
      replicas: 3
```

...and applying the Custom Resource:

```bash
kubectl apply -f deploy/cr.yaml
```

The Operator will provision a new replica node. It will be ready and available
once data is synchronized from Primary.

### Using `spec.instances`

Each instance's entry has its own set of parameters, like resources, storage
configuration, sidecars, etc. When you add a new entry into instances, this
creates replica PostgreSQL nodes, but with a new set of parameters. This can be
useful in various cases:

* Test or migrate to new hardware
* Blue-green deployment of a new configuration
* Try out new versions of your sidecar containers

For example, you have the following Custom Resource manifest:

```yaml
spec:
...
  instances:
    - name: instance1
      replicas: 2
      dataVolumeClaimSpec:
        storageClassName: old-ssd
        accessModes:
        - ReadWriteOnce
        resources:
          requests:
            storage: 100Gi
```

Now you have a goal to migrate to new disks, which are coming with the `new-ssd`
storage class. You can create a new instance entry. This will instruct the
Operator to create additional nodes with the new configuration keeping your
existing nodes intact.

```yaml
spec:
...
  instances:
    - name: instance1
      replicas: 2
      dataVolumeClaimSpec:
        storageClassName: old-ssd
        accessModes:
        - ReadWriteOnce
        resources:
          requests:
            storage: 100Gi
    - name: instance2
      replicas: 2
      dataVolumeClaimSpec:
        storageClassName: new-ssd
        accessModes:
        - ReadWriteOnce
        resources:
          requests:
            storage: 100Gi
```

### Using Synchronous replication

Synchronous replication offers the ability to confirm that all changes made by a transaction have been transferred to one or more synchronous standby servers. When requesting synchronous replication, each commit of a write transaction will wait until confirmation is received that the commit has been written to the write-ahead log on disk of both the primary and standby server. The drawbacks of synchronous replication are increased latency and reduced throughput on writes.

You can turn on synchronous replication by customizing the `patroni.dynamicConfiguration` Custom Resource option.

* Enable synchronous replication by setting `synchronous_mode` option to `on`.
* Use `synchronous_node_count` option to set the number of replicas (PostgreSQL standby servers) which should operate in syncrhonous mode (the default value is `1`).

The result in your `deploy/cr.yaml` manifest may look as follows:

```yaml
...
  patroni:
    dynamicConfiguration:
      synchronous_mode: "on"
      synchronous_node_count: 2
      ...
```

You will have the desired amount of replicas switched to synchronous replication after applying changes as usual, with `kubectl apply -f deploy/cr.yaml` command.

Find more options useful to tune how your database cluster should operate in synchronous mode [in the official Patroni documentation :octicons-link-external-16:](https://patroni.readthedocs.io/en/latest/replication_modes.html#synchronous-mode).

## Logical replicas and failover

[Logical replicas](logical-replication.md) are not Patroni members and are not promoted during failover. Their replication slots live on the PostgreSQL instance that created them. After failover, the new primary often does not have those slots, and the logical replica status becomes `broken` with reason `SourceSlotMissing`.

The Operator tells Patroni not to drop logical `pgoutput` slots on the current primary. That does not copy slots to other instances.

### Persist replication slots across failover

To keep logical replication slots available on the new primary after failover, enable Patroni permanent slots and define a slot for **each** database the logical replica replicates.

1. Bootstrap the logical replica first and wait until it is healthy. If you configure replication slots before bootstrap finishes, creation can fail with an error that the slot already exists.
2. Find the slot name the Operator created. 
    
    * Identify the primary Pod and exec into it:
        
        ```bash
        PRIMARY=$(kubectl get pod -n <namespace> \
        --selector postgres-operator.crunchydata.com/cluster=cluster1,postgres-operator.crunchydata.com/role=primary \
        -o jsonpath='{.items[0].metadata.name}')
        kubectl exec -it $PRIMARY -n <namespace> -c database -- psql
        ```

    * Use the following statement to find the replication slot:

        ```sql
        SELECT * FROM pg_replication_slots;
        ```

        ??? example "Sample output"

            ```text
            slot_name                               |  plugin  | slot_type | datoid | database  | temporary | active | active_pid | xmin | catalog_xmin | restart_lsn | confirmed_flush_lsn | wal_status | safe_wal_size | two_phase | two_phase_at | inactive_since | conflicting | invalidation_reason | failover | synced
            ---------------------------------------------------+----------+-----------+--------+-----------+-----------+--------+------------+------+--------------+-------------+---------------------+------------+---------------+-----------+--------------+----------------+-------------+---------------------+----------+--------
            pgo_lr_slot_analytics_cluster1_50651e49 | pgoutput | logical   |  16410 | cluster1 | f         | t
                |       1700 |      |          800 | 0/A0003A0   | 0/B000000           | reserved   |
              | f         |              |                | f           |                     | f        | f
            pgo_lr_slot_analytics_myapp_b751042e    | pgoutput | logical   |  16433 | myapp    | f         | t
                |       1701 |      |          800 | 0/A0003A0   | 0/B000000           | reserved   |
              | f         |              |                | f           |                     | f        | f
            (2 rows)
            ```

3. Add the same slot name under `patroni.dynamicConfiguration`. Example for a logical replica that replicates the `myapp` database (replace the slot name with the value from the query):

    ```yaml
    spec:
      patroni:
        dynamicConfiguration:
          postgresql:
            use_slots: true
          slots:
            pgo_lr_slot_myapp_cluster1_875a65d6:
              type: logical
              database: myapp
              plugin: pgoutput
    ```

4. Apply the change:

    ```bash
    kubectl apply -f deploy/cr.yaml -n <namespace>
    ```

!!! warning

    With `use_slots: true`, WAL can accumulate on the primary if a logical replica falls behind. Monitor disk usage and replica lag.

Permanent Patroni slots help the slot survive failover. They do **not** guarantee that logical replication keeps running. Subscriptions are created with `disable_on_error`, so an error during failover can disable the subscription, and the Operator does not re-enable it automatically.

### If the subscription is disabled after failover

Check the logical replica status:

```bash
kubectl get pg <cluster-name> -o yaml | yq '.status.logicalReplicas'
```

A disabled subscription looks like this:

```yaml
- databases:
    - myapp
  message: subscription "pgo_lr_sub_myapp_cluster1_875a65d6" on database "myapp" is disabled, most likely because applying a change from the primary failed; check the logical replica's logs for the error
  name: l1
  reason: SubscriptionDisabled
  state: broken
```

Check the logical replica Pod logs for the underlying error (for example a closed SSL connection during failover). To re-enable the subscription, exec into the logical replica Pod as the subscription owner and run:

```sql
\c myapp
SELECT * FROM pg_subscription;
SET default_transaction_read_only = off;
ALTER SUBSCRIPTION "pgo_lr_sub_myapp_cluster1_875a65d6" ENABLE;
ALTER SUBSCRIPTION "pgo_lr_sub_myapp_cluster1_875a65d6"  SET (disable_on_error = false);
```

Repeat for each disabled subscription. If you need the database name for a subscription, use:

```sql
SELECT datname FROM pg_database WHERE oid = <pg_subscription.subdbid>;
```

If re-enabling does not restore replication, or the reason is `SourceSlotMissing`, [reseed the logical replica](logical-replication.md#reseed-a-logical-replica).
