# Using sidecar containers

The Operator allows you to deploy additional (so-called *sidecar*) containers to
the Pod. You can use this feature to run debugging tools, some specific
monitoring solutions, etc.

!!! note

    Custom sidecar containers [can easily access other components of your cluster :octicons-link-external-16:](https://kubernetes.io/docs/concepts/workloads/pods/#resource-sharing-and-communication).
Therefore they should be used carefully and by experienced users only.

## Adding a sidecar container

You can add sidecar containers to PostgreSQL instance and pgBouncer
Pods. Just use `sidecars` subsection in the `instances` or `proxy.pgBouncer`
Custom Resource section in the `deploy/cr.yaml` configuration file. In this
subsection, you should specify at least the name and image of your container,
and possibly a command to run:

```yaml
spec:
  instances:
    ....
    sidecars:
    - image: busybox
      command: ["/bin/sh"]
      args: ["-c", "while true; do echo echo $(date -u) 'test' >> /dev/null; sleep 5; done"]
      name: my-sidecar-1
    ....
```

Apply your modifications as usual:

``` {.bash data-prompt="$" }
$ kubectl apply -f deploy/cr.yaml
```

!!! note

    More options suitable for the `sidecars` subsection can be found in the [Custom Resource options reference](operator.md).

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
    my-sidecar-1:
      Container ID:  docker://f0c3437295d0ec819753c581aae174a0b8d062337f80897144eb8148249ba742
      Image:         busybox
      Image ID:      docker-pullable://busybox@sha256:139abcf41943b8bcd4bc5c42ee71ddc9402c7ad69ad9e177b0a9bc4541f14924
      Port:          <none>
      Host Port:     <none>
      Command:
        /bin/sh
      Args:
        -c
        while true; do echo echo $(date -u) 'test' >> /dev/null; sleep 5; done
      State:          Running
        Started:      Thu, 11 Nov 2021 10:38:15 +0300
      Ready:          True
      Restart Count:  0
      Environment:    <none>
      Mounts:
        /var/run/secrets/kubernetes.io/serviceaccount from kube-api-access-fbrbn (ro)
    ....
    ```

## Getting shell access to a sidecar container

You can login to your sidecar container as follows:

``` {.bash data-prompt="$" }
$ kubectl exec -it cluster1-instance1n8v4-0 -c my-sidecar-1 -- sh
/ #
```
