# High availability and scaling

One of the great advantages brought by Kubernetes and the OpenShift platform is the ease of an application scaling. Scaling an application results in adding resources or Pods and scheduling them to available Kubernetes nodes.

Scaling can be vertical and horizontal. Vertical scaling adds more compute or storage resources to PostgreSQL nodes; horizontal scaling is about adding more nodes to the cluster. High availability looks technically similar, because it also involves additional nodes, but the reason is maintaining liveness of the system in case of server or network failures. 

## Vertical scaling

### Scale compute

There are multiple components that Operator deploys and manages: PostgreSQL instances, pgBouncer connection pooler, etc. To add or reduce CPU or Memory you need to edit corresponding sections in the Custom Resource. We follow the structure for requests and limits that Kubernetes [provides :octicons-link-external-16:](https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/).

To add more resources to your PostgreSQL instances edit the following section in the Custom Resource:

```yaml
spec:
...
  instances:
  - name: instance1
    replicas: 3
    resources:
      limits:
        cpu: 2.0
        memory: 4Gi
```

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

``` {.bash data-prompt="$" }
$ kubectl describe sc <storage class name> | grep AllowVolumeExpansion
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

``` {.bash data-prompt="$" }
$ kubectl apply -f cr.yaml
```

#### Automated scaling with auto-growable disk

The Operator 2.5.0 and newer is able to detect if the storage usage on the PVC
reaches a certain threshold, and trigger the PVC resize. Such autoscaling needs
the "auto-growable disk" feature turned on when deploying the Operator.
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

When the support for auto-growable disks is turned on, the
`spec.instances[].dataVolumeClaimSpec.resources.limits.storage` Custom Resource
option sets the maximum value available for the Operator to scale up:

``` {.text .no-copy}
spec:
  ...
  instances:
    ...
    dataVolumeClaimSpec:
      resources:
        limits:
          storage: <MAXIMUM STORAGE SIZE>
```

## High availability

Percona Operator allows you to deploy highly-available PostgreSQL clusters.
There are two ways how to control replicas in your HA cluster:

1. Through changing `spec.instances.replicas` value
2. By adding new entry into `spec.instances`

## Using `spec.instances.replicas`

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

``` {.bash data-prompt="$" }
$ kubectl apply -f deploy/cr.yaml
```

The Operator will provision a new replica node. It will be ready and available
once data is synchronized from Primary.

## Using `spec.instances`

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

## Scaling storage
