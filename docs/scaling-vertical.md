# Scale a PostgreSQL cluster vertically

Vertical scaling adds CPU, memory, or disk to existing PostgreSQL members. Use it when the cluster needs more resources per Pod rather than more members. For adding members, see [Scale horizontally](scaling-horizontal.md).

## Scale compute resources

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

## Scale storage

Kubernetes manages storage with the following components:

* a PersistentVolume (PV) - a segment of storage supplied by the Kubernetes administrator
* a PersistentVolumeClaim (PVC) - a request for storage from a user

Starting with Kubernetes v1.11, you can increase the size of an existing PVC object (considered stable since Kubernetes v1.24).
Note that you **cannot shrink** the size of an existing PVC object.

Use storage scaling to keep up with growing data while keeping the cluster online. Starting with Operator version 2.5.0, the Operator supports the following scaling options:

* storage resizing with Volume Expansion capability - instruct the Operator to scale the storage by updating the Custom Resource manifest
* automated scaling with auto-growable disks - the Operator monitors storage usage and scales the storage automatically when you enable the `AutoGrowVolumes` feature gate. Starting with Operator version 3.1.0, this also covers pgBackRest repository volumes on the repo host.

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

### Storage resizing with Volume Expansion capability

Starting with Operator version 2.5.0, the Operator automatically expands storage that supports Volume Expansion when you change the size in the Custom Resource.

To resize storage, do the following:
{.power-number}

1. Edit the `deploy/cr.yaml` file and set the new size under `instances[].dataVolumeClaimSpec.resources.requests.storage`:

    ```yaml
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

### Automated scaling with auto-growable disks

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

1. Turn on the feature gate via the `PGO_FEATURE_GATES` environment variable in the `deploy/operator.yaml` manifest (or in the appropriate part of `deploy/bundle.yaml` / `deploy/cw-bundle.yaml`):

    ```yaml
    ...
    subjects:
    - kind: ServiceAccount
      name: percona-postgresql-operator
      namespace: <operator-namespace>
    ...
    spec:
      containers:
      - env:
        - name: PGO_FEATURE_GATES
          value: "AutoGrowVolumes=true"
    ...
    ```

2. Edit the cluster Custom Resource. Set the maximum storage size the Operator may scale up to for the volumes you want to autoscale.

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
