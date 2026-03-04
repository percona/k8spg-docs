# Using sidecar containers

Sidecar containers are extra containers that run alongside the main container in a Pod. They are often used for logging, proxying, or monitoring.

The Operator uses a set of "predefined" sidecar containers to manage the cluster operation:

* `replica-cert-copy` - is responsible for copying TLS certificates needed for replication between PostgreSQL instances
* `pgbouncer-config` - handles configuration management for `pgBouncer`
* `pgbackrest` - runs the main backup/restore agent
* `pgbackrest-config` - handles configuration management for `pgBackRest`

You can also deploy your own sidecar containers to
the Pod. You can use this feature to run debugging tools, some specific
monitoring solutions, etc.

!!! note

    Custom sidecar containers [can easily access other components of your cluster :octicons-link-external-16:](https://kubernetes.io/docs/concepts/workloads/pods/#resource-sharing-and-communication). Therefore use them with caution, only when you are sure what you are doing.

## Adding a custom sidecar container

You can add sidecar containers to these Pods: 

* a PostgreSQL instance Pod 
* a pgBouncer Pod
* a pgBackRest repo host Pod

To add a sidecar container, use the `instances.sidecars` or `proxy.pgBouncer.sidecars` subsection in the `deploy/cr.yaml` configuration file.  Specify this minimum required information in this subsection:

* the container name
* the container image 
* a command to run

Note that you cannot reuse the name of the predefined containers. For example, PostgreSQL instance Pods cannot have custom sidecar containers named as `database`, `pgbackrest`, `pgbackrest-config`, and `replica-cert-copy`.

Use the `kubectl describe pod` command to check which names are already in use.

Here is the sample configuration of a sidecar container for a PostgreSQL instance Pod:

```yaml
spec:
  instances:
  - name: instance1
    ....
    sidecars:
    - image: busybox:latest
      command: ["sleep", "30d"]
      args: ["-c", "while true; do echo echo $(date -u) 'test' >> /dev/null; sleep 5; done"]
      name: my-sidecar-1
    ....
```

Find additional options suitable for the `sidecars` subsection in the [Custom Resource options reference](operator.md) and the [Kubernetes Workload API reference :octicons-link-external-16:](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.30/#container-v1-core)

Apply your modifications:

```bash
kubectl apply -f deploy/cr.yaml
```

Running `kubectl describe` command for the appropriate Pod can bring you the
information about the newly created container:

```bash
kubectl describe pod cluster1-instance1
```

??? example "Expected output"

    ``` {.text .no-copy}
    Name:            cluster1-instance1-n8v4-0
    ....
    Containers:
    ....
    testcontainer:
    Container ID:  containerd://c2a9dc1057ba30ac25d73e1856d99c04e49fd0942a03501405904510bc15cf5b
    Image:         nginx:latest
    Image ID:      docker.io/library/nginx@sha256:dc53c8f25a10f9109190ed5b59bda2d707a3bde0e45857ce9e1efaa32ff9cbc1
    Port:          <none>
    Host Port:     <none>
    Command:
      sleep
      30d
    State:          Running
      Started:      Thu, 26 Jun 2025 18:13:05 +0200
    Ready:          True
    Restart Count:  0
    Environment:    <none>
    Mounts:
      /tmp from tmp (rw)
      /var/run/secrets/kubernetes.io/serviceaccount from kube-api-access-5l57g (ro)
    ....
    ```

## Getting shell access to a sidecar container

You can login to your sidecar container as follows:

```bash
kubectl exec -it cluster1-instance1n8v4-0 -c testcontainer -- sh
/ #
```

## Mount volumes into sidecar containers

You can mount volumes into sidecar containers using `sidecarVolumes` and
`sidecarPVCs`. These options are available for:

* PostgreSQL instance Pods (`instances[].sidecarVolumes`, `instances[].sidecarPVCs`)
* pgBouncer Pods (`proxy.pgBouncer.sidecarVolumes`, `proxy.pgBouncer.sidecarPVCs`)
* pgBackRest repo host Pods (`backups.pgbackrest.repoHost.sidecarVolumes`, `backups.pgbackrest.repoHost.sidecarPVCs`)

The following subsections describe different [volume types  :octicons-link-external-16:](https://kubernetes.io/docs/concepts/storage/volumes/#volume-types)
that work with sidecar containers. Use `sidecarVolumes` for existing volumes (secret, configMap, NFS, etc.) and `sidecarPVCs` for operator-managed PersistentVolumeClaims.

### Persistent Volume

You can use [Persistent volumes :octicons-link-external-16:](https://kubernetes.io/docs/concepts/storage/persistent-volumes/)
when you need dynamically provisioned storage that does not depend on the Pod
lifecycle. 

The Operator creates and manages the PVCs you define in `sidecarPVCs`. Claim storage with
[persistentVolumeClaim  :octicons-link-external-16:](https://kubernetes.io/docs/concepts/storage/volumes/#persistentvolumeclaim)
and reference it in your sidecar's `volumeMounts`. 

!!! important

    You can use PVCs with sidecar containers only when you deploy a new cluster. Updates to running cluster are not supported.

The following example requests 1Gi storage with `sidecar-volume-claim`
and mounts it to the `testcontainer` sidecar under `/volume0`:

```yaml
spec:
  instances:
  - name: instance1
    sidecars:
    - name: testcontainer
      image: busybox:latest
      command: ["sleep", "30d"]
      volumeMounts:
      - name: sidecar-volume-claim
        mountPath: /volume0
    sidecarPVCs:
    - name: sidecar-volume-claim
      spec:
        resources:
          requests:
            storage: 1Gi
        volumeMode: Filesystem
        accessModes:
          - ReadWriteOnce
```

!!! note

    If you set the `percona.com/delete-pvc` [finalizer](operator.md#finalizers-delete-pvc), the Operator deletes sidecar PVCs when the cluster is removed.

### Secret

You can use a [secret volume  :octicons-link-external-16:](https://kubernetes.io/docs/concepts/storage/volumes/#secret)
to pass the information which needs additional protection (e.g. passwords), to
the sidecar container. Secrets are stored with the Kubernetes API and mounted to the
container as RAM-stored files.

Create the [Secret object  :octicons-link-external-16:](https://kubernetes.io/docs/concepts/configuration/secret/) with the sensitive information that you want to pass to the container.

Define the volume in `sidecarVolumes` and reference the Secret there, Then reference the volume in your sidecar `volumeMounts`:

```yaml
spec:
  instances:
  - name: instance1
    sidecars:
    - name: rs-sidecar-0
      image: busybox
      command: ["/bin/sh"]
      args: ["-c", "while true; do sleep 5; done"]
      volumeMounts:
      - mountPath: /secret
        name: sidecar-secret
    sidecarVolumes:
    - name: sidecar-secret
      secret:
        secretName: mysecret
```

The example creates a `sidecar-secret` volume from the existing
`mysecret` [Secret object  :octicons-link-external-16:](https://kubernetes.io/docs/concepts/configuration/secret/)
and mounts it under `/secret`.


### configMap

You can use a [configMap volume  :octicons-link-external-16:](https://kubernetes.io/docs/concepts/storage/volumes/#configmap)
to pass configuration data to the container. ConfigMaps are stored in the Kubernetes API and mounted as RAM-backed files.

As with the Secret, you must create the [configMap object  :octicons-link-external-16:](https://kubernetes.io/docs/tasks/configure-pod-container/configure-pod-configmap/) first. 

Then define the volume in `sidecarVolumes` and reference your configMap object. Finally, reference the volume in your sidecar `volumeMounts`.

This example creates a `sidecar-config` volume from the existing
`myconfigmap` [configMap object  :octicons-link-external-16:](https://kubernetes.io/docs/tasks/configure-pod-container/configure-pod-configmap/)
and mounts it under `/config`:

```yaml
spec:
  instances:
  - name: instance1
    sidecars:
    - name: rs-sidecar-0
      image: busybox
      command: ["/bin/sh"]
      args: ["-c", "while true; do sleep 5; done"]
      volumeMounts:
      - mountPath: /config
        name: sidecar-config
    sidecarVolumes:
    - name: sidecar-config
      configMap:
        name: myconfigmap
```

### NFS

You can use an [NFS volume  :octicons-link-external-16:](https://kubernetes.io/docs/concepts/storage/volumes/#nfs)
to mount a shared NFS export into your sidecar. Add it to `sidecarVolumes`:

```yaml
spec:
  instances:
  - name: instance1
    sidecarVolumes:
    - name: backup-nfs
      nfs:
        server: "nfs-service.storage.svc.cluster.local"
        path: "/pg-some-name"
```

Reference the volume in your sidecar `volumeMounts` with the same `name`.

