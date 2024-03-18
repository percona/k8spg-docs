# Binding Percona Distribution for PostgreSQL components to specific Kubernetes/OpenShift Nodes

The operator does good job automatically assigning new Pods to nodes
with sufficient resources to achieve balanced distribution across the cluster.
Still there are situations when it is worth to ensure that pods will land
on specific nodes: for example, to get speed advantages of the SSD
equipped machine, or to reduce network costs choosing nodes in a same
availability zone.

Appropriate sections of the
[deploy/cr.yaml :material-arrow-top-right:](https://github.com/percona/percona-postgresql-operator/blob/main/deploy/cr.yaml)
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

You can see the explanation of these affinity options [in Kubernetes documentation :material-arrow-top-right:](https://kubernetes.io/docs/concepts/scheduling-eviction/assign-pod-node/#inter-pod-affinity-and-anti-affinity).

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

You can see the explanation of these affinity options [in Kubernetes documentation :material-arrow-top-right:](https://kubernetes.io/docs/concepts/scheduling-eviction/topology-spread-constraints/).


## Tolerations

*Tolerations* allow Pods having them to be able to land onto nodes with matching
*taints*. Toleration is expressed as a `key` with and `operator`, which is
either `exists` or `equal` (the latter variant also requires a `value` the key
is equal to). Moreover, toleration should have a specified `effect`, which may
be a self-explanatory `NoSchedule`, less strict `PreferNoSchedule`, or
`NoExecute`. The last variant means that if a *taint* with `NoExecute` is
assigned to node, then any Pod not tolerating this *taint* will be removed from
the node, immediately or after the `tolerationSeconds` interval, like in the
following example.

You can use `instances.tolerations` and `backups.pgbackrest.jobs.tolerations`
subsections in the `deploy/cr.yaml` configuration file as follows:

```yaml
tolerations:
- effect: NoSchedule
  key: role
  operator: Equal
  value: connection-poolers
```

The [Kubernetes Taints and Toleratins :material-arrow-top-right:](https://kubernetes.io/docs/concepts/configuration/taint-and-toleration/)
contains more examples on this topic.
