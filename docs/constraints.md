# Binding Percona Distribution for PostgreSQL components to Specific Kubernetes/OpenShift Nodes

The operator does good job automatically assigning new Pods to nodes
with sufficient resources to achieve balanced distribution across the cluster.
Still there are situations when it is worth to ensure that pods will land
on specific nodes: for example, to get speed advantages of the SSD
equipped machine, or to reduce network costs choosing nodes in a same
availability zone.

Appropriate sections of the
[deploy/cr.yaml](https://github.com/percona/percona-postgresql-operator/blob/main/deploy/cr.yaml)
file (such as `pgPrimary` or `pgReplicas`) contain keys which can be used to do this, depending on what is the
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

Pod anti-affinity is controlled by the `antiAffinityType` option, which can
be put into `pgPrimary`, `pgBouncer`, and `backup` sections of the
`deploy/cr.yaml` configuration file. This option can be set to one of two
values:

* `preferred` Pod anti-affinity is a sort of a *soft rule*. It makes
  Kubernetes *trying* to schedule Pods matching the anti-affinity rules to
  different Nodes. If it is not possible, then one or more Pods are scheduled
  to the same Node. This variant is used by default.
* `required` Pod anti-affinity is a sort of a *hard rule*. It forces
  Kubernetes to schedule each Pod matching the anti-affinity rules to different
  Nodes. If it is not possible, then a Pod will not be scheduled at all.

Node affinity can be controlled by the `pgPrimary.affinity.nodeAffinityType`
option in the `deploy/cr.yaml` configuration file. This option can be set to
either `preferred` or `required` similarly to the `antiAffinityType` option.

## Simple approach - configure Node Affinity based on nodeLabel

The Operator provides the `pgPrimary.affinity.nodeLabel` option, which should
contains one or more key-value pairs. If the node is not labeled with each
key-value pair and `nodeAffinityType` is set to `required`, the Pod will not be
able to land on it.

The following example forces Operator to lend Percona Distribution for
PostgreSQL instances on the Nodes having the `kubernetes.io/region: us-central1`
label:

```yaml
affinity:
  nodeAffinityType: required
  nodeLabel:
    kubernetes.io/region: us-central1
```

### Advanced approach - use standard Kubernetes constraints

Previous way can be used with no special knowledge of the Kubernetes way of
assigning Pods to specific Nodes. Still in some cases more complex tuning may be
needed. In this case `pgPrimary.affinity.advanced` option placed in the
`deploy/cr.yaml` file turns off the effect of the `nodeLabel` and allows to use
standard Kubernetes affinity constraints of any complexity:

```yaml
affinity:
   advanced:
     podAffinity:
       requiredDuringSchedulingIgnoredDuringExecution:
       - labelSelector:
           matchExpressions:
           - key: security
             operator: In
             values:
             - S1
         topologyKey: failure-domain.beta.kubernetes.io/zone
     podAntiAffinity:
       preferredDuringSchedulingIgnoredDuringExecution:
       - weight: 100
         podAffinityTerm:
           labelSelector:
             matchExpressions:
             - key: security
               operator: In
               values:
               - S2
           topologyKey: kubernetes.io/hostname
     nodeAffinity:
       requiredDuringSchedulingIgnoredDuringExecution:
         nodeSelectorTerms:
         - matchExpressions:
           - key: kubernetes.io/e2e-az-name
             operator: In
             values:
             - e2e-az1
             - e2e-az2
       preferredDuringSchedulingIgnoredDuringExecution:
       - weight: 1
         preference:
           matchExpressions:
           - key: another-node-label-key
             operator: In
             values:
             - another-node-label-value
```

You can see the explanation of these affinity options [in Kubernetes
documentation](https://kubernetes.io/docs/concepts/scheduling-eviction/assign-pod-node/#inter-pod-affinity-and-anti-affinity).

### Default Affinity rules

The following anti-affinity rules are applied to all Percona Distribution for
PostgreSQL Pods:

```yaml
affinity:
  podAntiAffinity:
    preferredDuringSchedulingIgnoredDuringExecution:
    - podAffinityTerm:
        labelSelector:
          matchExpressions:
          - key: vendor
            operator: In
            values:
            - crunchydata
          - key: pg-pod-anti-affinity
            operator: Exists
          - key: pg-cluster
            operator: In
            values:
            - cluster1
        topologyKey: kubernetes.io/hostname
      weight: 1
```

You can see the explanation of these affinity options [in Kubernetes
documentation](https://kubernetes.io/docs/concepts/scheduling-eviction/assign-pod-node/#inter-pod-affinity-and-anti-affinity).

!!! note

    Setting `required` anti-affinity type will result in placing all Pods on
    separate nodes, so default configuration **will require 7 Kubernetes nodes**
    to deploy the cluster with separate nodes assigned to one PostgreSQL
    primary, two PostgreSQL replica instances, three pgBouncer and one
    pgBackrest Pod.

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

You can use `pgPrimary.tolerations` key in the `deploy/cr.yaml`
configuration file as follows:

```yaml
tolerations:
- key: "node.alpha.kubernetes.io/unreachable"
  operator: "Exists"
  effect: "NoExecute"
  tolerationSeconds: 6000
```

The [Kubernetes Taints and
Toleratins](https://kubernetes.io/docs/concepts/configuration/taint-and-toleration/)
contains more examples on this topic.
