# High availability

High availability (HA) keeps your PostgreSQL database accessible when a Pod or node fails. With Percona Operator for PostgreSQL, HA comes from multiple PostgreSQL members in one cluster, [Patroni :octicons-link-external-16:](https://patroni.readthedocs.io/) for automated failover, and PostgreSQL streaming replication for data consistency.

Adding members can also increase read capacity. That is a [scaling](scaling.md) concern. This document focuses on keeping the cluster alive and consistent through failures.

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

For how to add or remove members, see [Scale your cluster](scaling.md#understand-horizontal-scaling).

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

For more Patroni options, see the [Patroni replication modes documentation :octicons-link-external-16:](https://patroni.readthedocs.io/en/latest/replication_modes.html#synchronous-mode).
