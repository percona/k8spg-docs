# Change the PostgreSQL primary instance

The Operator uses PostgreSQL high-availability implementation based on the [Patroni template :octicons-link-external-16:](https://patroni.readthedocs.io/en/latest/faq.html#concepts-and-requirements).
This means that each PostgreSQL cluster includes one member availiable for read/write transactions (PostgreSQL primary instance, or leader in terms of Patroni) and a number of replicas which can serve read requests only (standby members of the cluster).

You may wish to manually change the primary instance in your PostgreSQL cluster to achieve more control and meet specific requirements in various scenarios like planned maintenance, testing failover procedures, load balancing and performance optimization activities and the like.
Primary instance is re-elected during the automatic failover (Patroni's "leader race" mechanism), but still there are use cases to controll this process manually.

In Percona Operator, the primary instance change can be controlled by the `patroni.switchover` section of the `deploy/cr.yaml` manifest. It allows you to enable switchover targeting a specific PostgreSQL instance as the new primary, or just running a failover if PostgreSQL cluster has entered a bad state.

This document provides instructions how to change the primary instance manually. 

For the following steps, we assume that you have the PostgreSQL cluster up and running. The cluster name is `cluster1`. 

1. Check the information about the *cluster instances*. Cluster instances (actually, PostgreSQL clusters created by the Operator in one namespace) are defined in the `spec.instances` Custom Resource section.
    By default you have one cluster instance named `instance1`, which contains a number of PostgreSQL instances (3 by default) and other components.
    You can check what your cluster instances are using Kubernetes Labels as follows (replace the `<namespace>` placeholder with your value):

    ```{.bash data-prompt="$"}
    $ kubectl get pods -n <namespace> -l postgres-operator.crunchydata.com/cluster=cluster1 \ 
        -L postgres-operator.crunchydata.com/instance \
        -L postgres-operator.crunchydata.com/role | grep instance1
    ```

    ???+ example "Sample output"

        ```{.text .no-copy}
        cluster1-instance1-bmdp-0             4/4     Running   0          2m23s   cluster1-instance1-bmdp   replica
        cluster1-instance1-fm7w-0             4/4     Running   0          2m22s   cluster1-instance1-fm7w   replica
        cluster1-instance1-ttm9-0             4/4     Running   0          2m22s   cluster1-instance1-ttm9   master
        ```
    PostgreSQL primary is labeled as `master`, while other PostgreSQL instances are labeled as `replica`.

3. Now update the following options in the `partoni.switchover` subsection of the Custom Resource:

    ```yaml 
    patroni:
      switchover:
        enabled: true
        targetInstance: <instance-name>
    ```

    You can do it with `kubectl patch` command, specifying the name of the instance that you want to be the new primary. For example, let's set the `cluster1-instance1-bmdp` as a new PostgreSQL primary:

    ```{.bash data-prompt="$"}
    $ kubectl -n <namespace> patch pg cluster1 --type=merge --patch '{
    "spec": {
       "patroni": { "switchover": { "enabled": "true" } },
       "patroni": { "switchover": { "targetInstance": "cluster1-instance1-bmdp" } }
    }}'

5. Trigger the switchover by adding the annotation to your Custom Resource. The recommended way is to set the annotation with the timestamp, so you know when switchover took place. Replace the `<namespace>` placeholder with your value:

    ```{.bash data-prompt="$"}
    $ kubectl annotate -n <namespace> pg cluster1 postgres-operator.crunchydata.com/trigger-switchover="$(date)"
    ```

6. Verify that the cluster was annotated (replace the `<namespace>` placeholder with your value, as usual):

    ```{.bash data-prompt="$"}
    $ kubectl get pg cluster1 -o yaml -n <namespace>
    ```

    ??? example "Sample output"

        ```{.text .no-copy}
        apiVersion: pgv2.percona.com/v2
        kind: PerconaPGCluster
        metadata:
          annotations:
            kubectl.kubernetes.io/last-applied-configuration: |
              {....
              "patroni":{"switchover":{"enabled":true,"targetInstance":"cluster1-instance1-bmdp"}},}
        ```

7. Now, check instances of your cluster once again to make sure the switchover took place:

    ```{.bash data-prompt="$"}
    $ kubectl get pods -n <namespace> -l postgres-operator.crunchydata.com/cluster=cluster1 \ 
        -L postgres-operator.crunchydata.com/instance \
        -L postgres-operator.crunchydata.com/role | grep instance1
    ```

    ??? example "Sample output"

        ```{.text .no-copy}
        cluster1-instance1-bmdp-0             4/4     Running     0          24m   cluster1-instance1-bmdp   master
        cluster1-instance1-fm7w-0             4/4     Running     0          24m   cluster1-instance1-fm7w   replica
        cluster1-instance1-ttm9-0             4/4     Running     0          23m   cluster1-instance1-ttm9   replica
        ```

The primary now should be has successfully changed to `cluster1-instance1-bmdp`.
