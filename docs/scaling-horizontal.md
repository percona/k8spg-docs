# Scale a PostgreSQL cluster horizontally

Horizontal scaling means adding members to your PostgreSQL cluster. New members join as standbys via streaming replication.

Horizontal scaling enhances your cluster’s **read** capacity and increases the number of available failover candidates. However, it does not increase write throughput. PostgreSQL still has only **one primary** member that handles all write operations. Standbys are read-only.

You can add extra nodes in two ways:

* Change the number of replicas in the existing instance set
* Change the number of instance sets

Key concepts to understand:

* An **instance set** is one entry under `spec.instances`. Members in the same set share the same resources, storage, sidecars, and related settings. The Operator manages each PostgreSQL member as its own StatefulSet within that set.
* **`replicas`** is how many PostgreSQL members belong to that instance set. One member becomes primary; the others are standbys.

## Choose between replicas and instance sets

| Approach | What the Operator does | Prefer when |
|----------|------------------------|-------------|
| Increase `replicas` on one set | Adds or removes members in that instance set | Standard high availability and read replicas with the same settings (storage, compute resources, affinity rules)|
| Add another `instances` entry | Creates a new instance set with its own members and settings | Different configuration or hardware, migration |

## Add replicas in an instance set

Use this approach when you want a cluster with **identical** members for high availability or to serve more read traffic.

For example, you have three members (one primary and 2 standbys):

```yaml
spec:
...
  instances:
    - name: instance1
      replicas: 3
```

Increase the replica count:

```yaml hl_lines="5"
spec:
...
  instances:
    - name: instance1
      replicas: 5
```

Apply the Custom Resource:

```bash
kubectl apply -f deploy/cr.yaml
```

The Operator adds two more members in the same instance set. The new standbys are ready after they synchronize from the primary.

**Best practices**

* Prefer **3** members for production high availability. Two is a fragile minimum. See [High availability](ha-deploy.md).
* Pair scaling with [anti-affinity and topology spread](constraints.md) so members do not share a single Kubernetes node.
* More replicas do not increase write capacity. Only the primary accepts writes. To spread read load, connect read-only clients to the replica Service or pgBouncer. See [Exposing cluster](expose.md).
* Each new standby needs its own PVC and copies data from the primary. Plan for that storage and network load.
* Raise the replica count gradually. Wait until each new standby finishes syncing before you rely on it.
* If you reduce the number of replicas in the instance set, the Operator keeps the primary and removes a standby Pod. You can set the target count but you cannot define which standby Pod to remove.

## Add an extra instance set

Add another `spec.instances` entry when members need a **different** configuration, or when you want to scale one group independently of another.

Each instance set can have its own configuration for resources, storage class, sidecars, and more. The Operator creates a separate StatefulSet for each configured set. However, all these sets remain part of the same PostgreSQL/Patroni cluster and synchronize the data through replication.

Typical use cases:

* Migrate to new hardware or a new storage class
* Blue-green style rollout of a new configuration
* Try new sidecar versions or sizing next to the existing set
* Control **which group** of members you add, drain, or stop, and in which sequence you apply those Custom Resource changes.

For example, migrate from `old-ssd` to `new-ssd` while keeping the existing instance set intact:

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

Apply the Custom Resource, wait until the new members are healthy and caught up, then scale down or remove the old instance set when you are ready.

**Best practices**

* Extra instance sets fit migration and mixed configuration. For identical members, increasing `replicas` on one set is usually simpler.
* Name instance sets clearly (for example `instance1`, `instance2-new-ssd`).
* Members in each instance set get dedicated PVC. When you deploy several instance sets, you need storage and replication capacity for all of them. Plan for that before you scale.
* Decide which set should host the primary during cutover, then remove the old set deliberately. See [Change the primary](change-primary.md).
* Apply [affinity and topology rules](constraints.md) so new members are spread across failure domains.
* Scale each set on its own: for example, bring `instance2` up first, then set `instance1` replicas to `0` or remove that entry after cutover.
