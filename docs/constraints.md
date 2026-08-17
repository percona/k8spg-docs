# Binding Percona Distribution for PostgreSQL components to specific Kubernetes/OpenShift Nodes

The operator does good job automatically assigning new Pods to nodes
with sufficient resources to achieve balanced distribution across the cluster.
Still there are situations when it is worth to ensure that pods will land
on specific nodes: for example, to get speed advantages of the SSD
equipped machine, or to reduce network costs choosing nodes in a same
availability zone.

Appropriate sections of the
[deploy/cr.yaml :octicons-link-external-16:](https://github.com/percona/percona-postgresql-operator/blob/main/deploy/cr.yaml)
file (such as `proxy.pgBouncer`) contain keys which can be used to do this, depending on what is the
best for a particular situation.

## Affinity and anti-affinity

Affinity makes Pod eligible (or not eligible - so called “anti-affinity”) to
be scheduled on the node which already has Pods with specific labels, or has
specific labels itself (so called “Node affinity”).
Particularly, Pod anti-affinity is good to reduce costs making sure several Pods
with intensive data exchange will occupy the same availability zone or even the
same node - or, on the contrary, to make them land on different nodes or even
different availability zones for the high availability and balancing purposes.
Node affinity is useful to assign PostgreSQL instances to specific Kubernetes
Nodes (ones with specific hardware, zone, etc.).

Pod anti-affinity is controlled by the `affinity.podAntiAffinity` subsection, which
can be put into `proxy.pgBouncer` and `backups.pgbackrest.repoHost` sections of
the `deploy/cr.yaml` configuration file.

`podAntiAffinity` allows you to use standard Kubernetes affinity constraints
of any complexity:

```yaml
affinity:
  podAntiAffinity:
    preferredDuringSchedulingIgnoredDuringExecution:
    - weight: 1
      podAffinityTerm:
        labelSelector:
          matchLabels:
            postgres-operator.crunchydata.com/cluster: keycloakdb
            postgres-operator.crunchydata.com/role: pgbouncer
        topologyKey: kubernetes.io/hostname
```

You can see the explanation of these affinity options [in Kubernetes documentation :octicons-link-external-16:](https://kubernetes.io/docs/concepts/scheduling-eviction/assign-pod-node/#inter-pod-affinity-and-anti-affinity).

## Topology Spread Constraints

*Topology Spread Constraints*  allow you to control how Pods are distributed
across the cluster based on regions, zones, nodes, and other topology specifics.
This can be useful for both high availability and resource efficiency.

Pod topology spread constraints are controlled by the
`topologySpreadConstraints` subsection, which can be put into `proxy.pgBouncer`
and `backups.pgbackrest.repoHost` sections of the `deploy/cr.yaml` configuration
file as follows:

```yaml
topologySpreadConstraints:
  - maxSkew: 1
    topologyKey: my-node-label
    whenUnsatisfiable: DoNotSchedule
    labelSelector:
      matchLabels:
        postgres-operator.crunchydata.com/instance-set: instance1
```

You can see the explanation of these affinity options [in Kubernetes documentation :octicons-link-external-16:](https://kubernetes.io/docs/concepts/scheduling-eviction/topology-spread-constraints/).


## Tolerations

You can taint a Kubernetes node to prevent Pods from scheduling on the node unless the Pods tolerate the taint.
A toleration is a Pod setting that matches a taint and enables the Pod to schedule on a tainted node.
Use taints and tolerations to reserve nodes for specific workloads, such as database or backup workloads.

Each toleration is defined by: 
* a `key` 
* an `operator`. The default Kubernetes `operator` is `Exists`. You can set it to `Equal`. `Equal` requires a `value`
* an `effect`:

    * `NoSchedule` — Pods without a matching toleration are not scheduled on the node
    * `PreferNoSchedule` — Kubernetes prefers other nodes, but can still schedule there
    * `NoExecute` — Pods without a matching toleration are evicted, immediately or after `tolerationSeconds`

You can set tolerations in these Custom Resource sections of `deploy/cr.yaml`:

* `instances.tolerations` — PostgreSQL instance Pods
* `proxy.pgBouncer.tolerations` — pgBouncer Pods
* `backups.pgbackrest.repoHost.tolerations` — pgBackRest repository host
* `backups.pgbackrest.jobs.tolerations` — backup jobs
* `backups.pgbackrest.restore.tolerations` — restore jobs. If you do not set `backups.pgbackrest.restore.tolerations`, the Operator applies `backups.pgbackrest.jobs.tolerations` to restore jobs.
* `dataSource.*.tolerations` — data migration and clone jobs (see [Custom Resource options](operator.md))

Example:

```yaml
tolerations:
- effect: NoSchedule
  key: role
  operator: Equal
  value: connection-poolers
```

For more details and examples, see [Kubernetes Taints and Tolerations :octicons-link-external-16:](https://kubernetes.io/docs/concepts/configuration/taint-and-toleration/).
