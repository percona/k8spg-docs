# Scale Percona Distribution for PostgreSQL on Kubernetes

One of the great advantages brought by Kubernetes is the ease of an application scaling. Scaling an application results in adding resources or Pods and scheduling them to available Kubernetes nodes.

Scaling can be [vertical](#vertical-scaling) and horizontal. Vertical scaling adds more compute or storage resources to PostgreSQL nodes; horizontal scaling is about adding more nodes to the cluster. High availability looks technically similar, because it also involves additional nodes, but the reason is maintaining liveness of the system in case of server or network failures. 

This document focuses on vertical scaling. For deploying high-availability, see [High-availability](ha-deploy.md) guide.

## Vertical scaling

### Scale compute

There are multiple components that the Operator deploys and manages: PostgreSQL instances, pgBouncer connection pooler, pgBackRest and others (see [Architecture](architecture.md) for the full list of components).

You can manage compute resources for a specific component using the corresponding section in the Custom Resource manifest. We follow the structure for [requests and limits  :octicons-link-external-16:](https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/) that Kubernetes provides.

The most common resources to specify are CPU and memory (RAM).

You can specify a **request** for CPU or memory for a component's Pod. In this case, the Kubernetes scheduler uses these values to decide on which Kubernetes node to place the Pod, ensuring the node has at least the requested resources available. The Pod will only be scheduled on a node that can satisfy all its resource requests.

If you specify a **limit** for the resources, this is the maximum amount of CPU or memory the container is allowed to use. If the container tries to use more than the limit, it may be throttled (for CPU) or terminated (for memory).

You can set both `requests` and `limits` in the `resources` section of your Custom Resource. For example:


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

If you only set `limits` and omit `requests`, Kubernetes will default the request to the limit value.

Use our reference documentation for the [Custom Resource options](operator.md) for more details about other components.

### Scale storage

Kubernetes manages storage with a PersistentVolume (PV), a segment of
storage supplied by the administrator, and a PersistentVolumeClaim
(PVC), a request for storage from a user. In Kubernetes v1.11 the
feature was added to allow a user to increase the size of an existing
PVC object (considered stable since Kubernetes v1.24).
The user cannot shrink the size of an existing PVC object.

#### Scaling with Volume Expansion capability

Certain volume types support PVCs expansion (exact details about
PVCs and the supported volume types can be found in [Kubernetes
documentation  :octicons-link-external-16:](https://kubernetes.io/docs/concepts/storage/persistent-volumes/#expanding-persistent-volumes-claims)).

You can run the following command to check if your storage supports the expansion capability:

```bash
kubectl describe sc <storage class name> | grep AllowVolumeExpansion
```

??? example "Expected output"

    ``` {.text .no-copy}
    AllowVolumeExpansion: true
    ```

The Operator versions 2.5.0 and higher will automatically expand such storage
for you when you change the appropriate options in the Custom Resource.

For example, you can do it by editing and applying the `deploy/cr.yaml` file:

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

Apply changes as usual:

```bash
kubectl apply -f cr.yaml
```

#### Automated scaling with auto-growable disk

The Operator 2.5.0 and newer is able to detect if the storage usage on the PVC
reaches a certain threshold, and trigger the PVC resize. Such autoscaling needs
the upstream "auto-growable disk" feature turned on when deploying the Operator.
This is done via the `PGO_FEATURE_GATES` environment variable set in the
`deploy/operator.yaml` manifest (or in the appropriate part of `deploy/bundle.yaml`):

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

When the support for auto-growable disks is turned on, the auto grow
will be working automatically if the maximum value available for the Operator to
scale up is set in the `spec.instances[].dataVolumeClaimSpec.resources.limits.storage`
Custom Resource option:

``` {.text .no-copy}
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
```


