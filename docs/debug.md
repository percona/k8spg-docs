# Initial troubleshooting

Percona Operator for PostgreSQL uses [Custom Resources :octicons-link-external-16:](https://kubernetes.io/docs/concepts/extend-kubernetes/api-extension/custom-resources/) to manage options for the various components of the cluster.

* `PerconaPGCluster` Custom Resource with Percona PostgreSQL Cluster options (it has handy `pg` shortname also),

* `PerconaPGBackup` and `PerconaPGRestore` Custom Resources contain options for Percona XtraBackup used to backup Percona XtraDB Cluster and to restore it from backups (`pg-backup` and `pg-restore` shortnames are available for them).


The first thing you can check for the Custom Resource is to query it with `kubectl get` command:


``` {.bash data-prompt="$" }
$ kubectl get pg
```

??? example "Expected output"

    --8<-- "kubectl-get-pg-response.txt"

The Custom Resource should have `Ready` status.

!!! note

    You can check which Percona’s Custom Resources are present and get some information about them as follows:

    ``` {.bash data-prompt="$" }
    $ kubectl api-resources | grep -i percona
    ```

    ??? example "Expected output"

        ``` {.text .no-copy}
        perconapgbackups          pg-backup    pgv2.percona.com/v2            true         PerconaPGBackup
        perconapgclusters         pg           pgv2.percona.com/v2            true         PerconaPGCluster
        perconapgrestores         pg-restore   pgv2.percona.com/v2            true         PerconaPGRestore
        ```

## Check the Pods

If Custom Resource is not getting `Ready` status, it makes sense to check
individual Pods. You can do it as follows:

``` {.bash data-prompt="$" }
$ kubectl get pods
```

???+ example "Expected output"

    --8<-- "kubectl-get-pods-response.txt"

The above command provides the following insights:

* `READY` indicates how many containers in the Pod are ready to serve the
    traffic. In the above example, `cluster1-repo-host-0` container has all two
    containers ready (2/2). For an application to work properly, all containers
    of the Pod should be ready.
* `STATUS` indicates the current status of the Pod. The Pod should be in a
    `Running` state to confirm that the application is working as expected. You
    can find out other possible states in the [official Kubernetes documentation :octicons-link-external-16:](https://kubernetes.io/docs/concepts/workloads/pods/pod-lifecycle/#pod-phase).
* `RESTARTS` indicates how many times containers of Pod were restarted. This is
    impacted by the [Container Restart Policy :octicons-link-external-16:](https://kubernetes.io/docs/concepts/workloads/pods/pod-lifecycle/#restart-policy).
    In an ideal world, the restart count would be zero, meaning no issues from
    the beginning. If the restart count exceeds zero, it may be reasonable to
    check why it happens.
* `AGE`: Indicates how long the Pod is running. Any abnormality in this value
    needs to be checked.

You can find more details about a specific Pod using the
`kubectl describe pods <pod-name>` command.

``` {.bash data-prompt="$" }
$ $ kubectl describe pods cluster1-instance1-b5mr-0
```

??? example "Expected output"

    ``` {.text .no-copy}
    ...
    Name:         cluster1-instance1-b5mr-0
    Namespace:    default
    ...
    Controlled By:  StatefulSet/cluster1-instance1-b5mr
    Init Containers:
     postgres-startup:
    ...
    Containers:
     database:
    ...
     pgbackrest:
    ...
       Restart Count:  0
       Liveness:   http-get https://:8008/liveness delay=3s timeout=5s period=10s #success=1 #failure=3
       Readiness:  http-get https://:8008/readiness delay=3s timeout=5s period=10s #success=1 #failure=3
       Environment:
    ...
       Mounts:
    ...
    Volumes:
    ...
    Events:
    ...
    ```

This gives a lot of information about containers, resources, container status
and also events. So, describe output should be checked to see any abnormalities.

