# Scale Percona Distribution for PostgreSQL on Kubernetes

One of the great advantages brought by Kubernetes is the ease of an application scaling. Scaling an application results in adding resources or Pods and scheduling them to available Kubernetes nodes.

Scaling can be [vertical](#vertical-scaling) and horizontal. Vertical scaling adds more compute or storage resources to PostgreSQL nodes; horizontal scaling is about adding more nodes to the cluster. High availability looks technically similar, because it also involves additional nodes, but the reason is maintaining liveness of the system in case of server or network failures.

This document focuses on vertical scaling. For deploying high availability, see the [High availability](ha-deploy.md) guide.

## Vertical scaling

### Scale compute resources

The Operator deploys and manages multiple components, such as PostgreSQL instances, pgBouncer connection pooler, pgBackRest and others. For the full list, refer to the [Architecture](architecture.md) section. 

You can manage CPU or memory for every component separately by editing the corresponding sections in the Custom Resource. We follow the structure for `requests` and `limits` that [Kubernetes provides :octicons-link-external-16:](https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/).

The most common resources to specify are CPU and memory (RAM):

* You can specify a **request** for CPU or memory for a
component's Pod. This tells the Kubernetes scheduler how much CPU or memory the Pod needs. The scheduler places the Pod only on a node that can satisfy all resource requests.
* If you specify a **limit**, this sets the maximum CPU or memory the container may use. If the container exceeds a CPU limit, it may be throttled. If it exceeds a memory limit, it may be terminated.

You can set both `requests` and `limits` in the `resources` section of your Custom Resource. For example, to add more resources to your PostgreSQL instances:

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

If you only set `limits` and omit `requests`, Kubernetes defaults the request to the limit value.

Use our reference documentation for the [Custom Resource options](operator.md) for more details about other components.

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
