# Scale Percona Distribution for PostgreSQL on Kubernetes

Kubernetes makes it straightforward to give a workload more capacity: you change the Custom Resource, and the Operator reconciles Pods, compute resources and storage to match.

Scaling can be vertical or horizontal:

* **Vertical scaling** adds CPU, memory, or disk to existing PostgreSQL members.
* **Horizontal scaling** adds more PostgreSQL members to the cluster.

Adding members can look similar to [high availability](ha-deploy.md), but the goals differ. Scaling is about capacity while high availability is about surviving failures. 

This document explains scaling. For failover, replication modes, and recommended cluster size, see [High availability](ha-deploy.md).

## Horizontal scaling

Horizontal scaling means adding members to your PostgreSQL cluster. New members join as standbys via streaming replication.

Horizontal scaling enhances your cluster’s **read** capacity and increases the number of available failover candidates. However, it does not increase write throughput. PostgreSQL still has only **one primary** member that handles all write operations. Standbys are read-only.

You can add extra nodes in two ways:

* Change the number of replicas in the existing instance set
* Change the number of instance sets

Key concepts to understand:

* An **instance set** is one entry under `spec.instances`. Members in the same set share the same resources, storage, sidecars, and related settings. The Operator manages each PostgreSQL member as its own StatefulSet within that set.
* **`replicas`** is how many PostgreSQL members belong to that instance set. One member becomes primary; the others are standbys.

### Choose between replicas and instance sets

| Approach | What the Operator does | Prefer when |
|----------|------------------------|-------------|
| Increase `replicas` on one set | Adds or removes members in that instance set | Standard HA and homogeneous read replicas |
| Add another `instances` entry | Creates a new instance set with its own members and settings | Different config/hardware, migration, or staged add/drain of a named group |

### Add replicas in an instance set

Use this approach when you want a cluster of **identical** members for high availability or to serve more read traffic.

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
* If you reduce the number of nodes in the instance set, the Operator keeps the primary and removes a standby. You can set the target count but you cannot define which standby Pod is removed.

### Add an extra instance set

Add another `spec.instances` entry when members need a **different** configuration, or when you want to scale one group independently of another.

Each instance set can have its own configuration for resources, storage class, sidecars, and more. The Operator creates a separate StatefulSet for each configured set. However, all these sets remain part of the same PostgreSQL/Patroni cluster and synchronize the data through replication.

Typical use cases:

* Migrate to new hardware or a new storage class
* Blue-green style rollout of a new configuration
* Try new sidecar versions or sizing next to the existing set
* Control **which group** of members you add, drain, or stop, and in which sequence you apply those Custom Resource changes

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

## Vertical scaling

### Scale compute resources

The Operator deploys and manages several components: PostgreSQL instances, pgBouncer, pgBackRest, and others. See [Architecture](architecture.md) for the full list.

You can manage CPU or memory for every component in the corresponding section of the Custom Resource. The Operator follows the Kubernetes model for [requests and limits :octicons-link-external-16:](https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/):

* A **request** tells the scheduler how much CPU or memory the Pod needs. Kubernetes places the Pod only on a node that can satisfy every request.
* A **limit** is the maximum CPU or memory the container may use. Above the limit, the container may be throttled (CPU) or terminated (memory).

You can set both `requests` and `limits` in the `resources` section. For example:

```yaml
spec:
...
  instances:
  - name: instance1
    replicas: 3
    resources:
      requests:
        cpu: 1.0
        memory: 2Gi
      limits:
        cpu: 2.0
        memory: 4Gi
```

If you set only `limits` and omit `requests`, Kubernetes defaults the request to the limit value.

See the [Custom Resource options](operator.md) for other components.

### Scale storage

Kubernetes manages storage with the following components:

* a PersistentVolume (PV) - a segment of storage supplied by the Kubernetes administrator
* a PersistentVolumeClaim (PVC) - a request for storage from a user

Starting with Kubernetes v1.11, you can increase the size of an existing PVC object (considered stable since Kubernetes v1.24).
Note that you **cannot** shrink the size of an existing PVC object.

Use storage scaling to keep up with growing data while keeping the cluster online. Starting with Operator version 2.5.0, the Operator supports the following scaling options:

* storage resizing with Volume Expansion capability - instruct the Operator to scale the storage by updating the Custom Resource manifest
* automated scaling with auto-growable disks - the Operator monitors storage usage and scales the storage automatically when you enable the `AutoGrowVolumes` feature gate. Starting with Operator version 3.1.0, this also covers pgBackRest repository volumes on the repo host

For either option, the volume type must support PVC expansion.
To check if your storage supports the expansion capability, run the following command:

```bash
kubectl describe sc <storage class name> | grep AllowVolumeExpansion
```

??? example "Expected output"

    ``` {.text .no-copy}
    AllowVolumeExpansion: true
    ```

Find exact details about PVCs and the supported volume types in [Kubernetes documentation :octicons-link-external-16:](https://kubernetes.io/docs/concepts/storage/persistent-volumes/#expanding-persistent-volumes-claims).

#### Storage resizing with Volume Expansion capability

Starting with Operator version 2.5.0, the Operator automatically expands storage that supports Volume Expansion when you change the size in the Custom Resource.

To resize storage, do the following:
{.power-number}

1. Edit the `deploy/cr.yaml` file and set the new size under `instances[].dataVolumeClaimSpec.resources.requests.storage`:

    ``` {.text .no-copy}
    spec:
      ...
      instances:
        ...
        dataVolumeClaimSpec:
          resources:
            requests:
              storage: <NEW STORAGE SIZE>
    ```

2. Apply the changes:

    ```bash
    kubectl apply -f deploy/cr.yaml
    ```

#### Automated scaling with auto-growable disks

Starting with Operator version 2.5.0, the Operator can detect when storage usage on a PVC reaches a certain threshold and trigger a PVC resize. Starting with Operator version 3.1.0, the Operator automatically resizes pgBackRest repository volumes on the repo host.

This autoscaling needs the upstream auto-growable disk feature turned on when you deploy the Operator.

This feature gives you:

* fewer outages from full disks because storage grows with demand
* less guesswork on capacity planning and fewer last-minute fixes
* lower operational effort for developers and platform engineers
* cost control by expanding only when needed
* a more predictable environment so teams can focus on delivery

To enable automated storage resizing, do the following:
{.power-number}

1. Turn on the feature gate via the `PGO_FEATURE_GATES` environment variable in the `deploy/operator.yaml` manifest (or in the appropriate part of `deploy/bundle.yaml`):

    ```yaml
    ...
    subjects:
    - kind: ServiceAccount
      name: percona-postgresql-operator
      namespace: pg-operator
    ...
    spec:
      containers:
      - env:
        - name: PGO_FEATURE_GATES
          value: "AutoGrowVolumes=true"
    ...
    ```

2. Set the maximum storage size the Operator may scale up to for the volumes you want to autoscale.

    * For PostgreSQL data volumes, use the `spec.instances[].dataVolumeClaimSpec.resources.limits.storage` Custom Resource option
    * For pgBackRest repository volumes, use the `spec.backups.pgbackrest.repos[].volume.volumeClaimSpec.resources.limits.storage` Custom Resource option:

    ```yaml
    spec:
      ...
      instances:
        ...
        dataVolumeClaimSpec:
          resources:
            requests:
              storage: 1Gi
            limits:
              storage: 5Gi
      backups:
        pgbackrest:
          repos:
          - name: repo1
            volume:
              volumeClaimSpec:
                accessModes:
                - ReadWriteOnce
                resources:
                  requests:
                    storage: 1Gi
                  limits:
                    storage: 5Gi
    ```

When usage on a volume exceeds 75%, the Operator calculates a new size by increasing the current volume size by 50%, up to the configured limit, and expands the PVC. If the calculated size exceeds the limit, the Operator expands the PVC only up to the limit and records a warning in the logs. 

For pgBackRest repositories, the Operator stores the latest suggested size in the `status.pgbackrest.repos[].desiredRepoVolume` field of the Custom Resource.
