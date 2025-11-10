# Using sidecar containers

Sidecar containers are extra containers that run alongside the main container in a Pod. They are often used for logging, proxying, or monitoring.

The Operator uses a set of "predefined" sidecar containers to manage the cluster operation:

* `replica-cert-copy` - is responsible for copying TLS certificates needed for replication between PostgreSQL instances
* `pgbouncer-config` - handles configuration management for `pgBouncer`
* `pgbackrest` - runs the main backup/restore agent
* `pgbackrest-config` - handles configuration management for `pgBackRest`

The Operator allows you to deploy your own sidecar containers to
the Pod. You can use this feature to run debugging tools, some specific
monitoring solutions, etc.

!!! note

    Custom sidecar containers [can easily access other components of your cluster :octicons-link-external-16:](https://kubernetes.io/docs/concepts/workloads/pods/#resource-sharing-and-communication). Therefore use them with caution, only when you are sure what you are doing.

## Adding a custom sidecar container

You can add sidecar containers to these Pods: 

* a PostgreSQL instance Pod 
* a pgBouncer Pod

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

Apply your modifications as usual:

``` {.bash data-prompt="$" }
$ kubectl apply -f deploy/cr.yaml
```

Running `kubectl describe` command for the appropriate Pod can bring you the
information about the newly created container:

``` {.bash data-prompt="$" }
$ kubectl describe pod cluster1-instance1
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

``` {.bash data-prompt="$" }
$ kubectl exec -it cluster1-instance1n8v4-0 -c testcontainer -- sh
/ #
```
