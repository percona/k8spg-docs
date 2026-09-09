# High availability

High availability (HA) keeps your PostgreSQL database accessible when a Pod or node fails. With Percona Operator for PostgreSQL, HA comes from multiple PostgreSQL members in one cluster, [Patroni :octicons-link-external-16:](https://patroni.readthedocs.io/) for automated failover, and PostgreSQL streaming replication for data consistency.

Adding members can also increase read capacity. That is a [horizontal scaling](scaling-horizontal.md) concern. This document focuses on keeping the cluster alive and consistent through failures.

## Understand cluster members

A PostgreSQL cluster includes:

* A **primary** that handles all write operations and streams changes to standbys.
* One or more **standbys** (replicas) that continuously receive and replay changes from the primary. If the primary fails, Patroni can promote a standby to become the new primary.

Standbys can also serve read-only traffic, depending on how you expose the cluster. See [Exposing cluster](expose.md).

## Choose a replication mode

The Operator uses PostgreSQL streaming replication to keep standbys up to date.

By default, the cluster uses **asynchronous replication**: the primary sends changes to standbys but does not wait for confirmation before committing. That favors performance, with a small risk that transactions not yet copied to a standby are lost if the primary fails.

**Synchronous replication** is also supported: the primary waits for at least one standby to acknowledge the data before committing. That reduces the risk of data loss and can add latency on writes. See [Configure synchronous replication](#configure-synchronous-replication).

## Size your high availability cluster

* **Minimum:** 2 PostgreSQL members can provide basic failover, but either loss hurts availability and data safety. This size does not give strong protection against split-brain style failure modes.
* **Recommended:** **3 or more** PostgreSQL members for production HA.

For how to add or remove members, see [Scale horizontally](scaling-horizontal.md).

## Place Pods for resilience

Extra members only help if they do not all fail together. Use [anti-affinity, topology spread constraints, and tolerations](constraints.md) so PostgreSQL Pods land on different Kubernetes nodes or availability zones when your cluster topology allows it.

The Operator and Kubernetes scheduler work together on placement; affinity rules are part of a production HA design, not an optional extra.

## Configure synchronous replication

Synchronous replication confirms that a transaction has reached one or more synchronous standbys before the primary considers the commit complete. The trade-off is higher write latency and lower write throughput.

Turn on synchronous replication with `patroni.dynamicConfiguration`:

* Set `synchronous_mode` to `on`.
* Set `synchronous_node_count` to the number of standbys that should run in synchronous mode (default is `1`).

Example:

```yaml
...
  patroni:
    dynamicConfiguration:
      synchronous_mode: "on"
      synchronous_node_count: 2
      ...
```

Apply the Custom Resource:

```bash
kubectl apply -f deploy/cr.yaml
```

After you apply the configuration, the requested number of standbys operate in synchronous mode.

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
```

Repeat for each disabled subscription. If you need the database name for a subscription, use:

```sql
SELECT datname FROM pg_database WHERE oid = <pg_subscription.subdbid>;
```

If re-enabling does not restore replication, or the reason is `SourceSlotMissing`, [reseed the logical replica](logical-replication.md#reseed-a-logical-replica).
