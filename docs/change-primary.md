# Change the PostgreSQL primary instance

You may wish to manually change the primary instance in your PostgreSQL cluster to achieve more control and meet specific requirements in various scenarios like  planned maintenance, testing failover procedures, load balancing and performance optimization activities and the like.

In Percona Operator, the primary instance change is controlled by the `patroni.switchover` section of the `deploy/cr.yaml` manifest. It allows you to enable switchovers in your PostgresClusters, target a specific instance as the new primary, and run a failover if your PostgreSQL cluster has entered a bad state.

This document provides instructions how to change the primary instance. 

For the following steps, we assume that you have the PostgreSQL cluster up and running. The cluster name is `cluster1`. 

1. Check the information about the cluster instances. Replace the `<namespace>` placeholder with your value:

    ```{.bash data-prompt="$"}
    $ kubectl get pods -l -n <namespace> postgres-operator.crunchydata.com/cluster=cluster1 \ 
        -L postgres-operator.crunchydata.com/instance \
        -L postgres-operator.crunchydata.com/role | grep instance1

    ```

    ??? example "Sample output"

        ```{.text .no-copy}
        cluster1-instance1-bmdp-0             4/4     Running   0          2m23s   cluster1-instance1-bmdp   replica
        cluster1-instance1-fm7w-0             4/4     Running   0          2m22s   cluster1-instance1-fm7w   replica
        cluster1-instance1-ttm9-0             4/4     Running   0          2m22s   cluster1-instance1-ttm9   master
        ```

2. Enter the edit mode for your cluster. Replace the `cluster1` with the name of your cluster and the `<namespace>` placeholder with your value:

    ```{.bash data-prompt="$"}
    $ kubectl edit pg cluster1 -n <namespace>
    ```

    This opens the Custom Resource for your cluster.

3. Add the following configuration to the Custom Resource:

    ```yaml 
    patroni:
      switchover:
        enabled: true
        targetInstance: <instance-name>
    ```

    Specify the name of the instance that you want to act as the new primary. In our example, we're targeting the `cluster1-instance1-bmdp` to be the new primary

4. Save the changes and exit the editor. This applies the new configuration. 

5. Trigger the switchover by adding the annotation to your custom resource. The recommended way is to set the annotation with the timestamp, so you know when switchover took place. Replace the `<namespace>` placeholder with your value:

    ```{.bash data-prompt="$"}
    $ kubectl annotate -n <namespace> pg cluster1 postgres-operator.crunchydata.com/trigger-switchover="$(date)"
    ```

6. Verify that the cluster was annotated. Replace the `<namespace>` placeholder with your value:

    ```{.bash data-prompt="$"}
    $ kubectl get pg cluster1 -o yaml -n <namespace>
    ```
 
    You should see the output similar to the following:

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

7. Now, check the roles in your cluster again. Replace the `<namespace>` placeholder with your value:

    ```{.bash data-prompt="$"}
    $ kubectl get pods -l -n <namespace> postgres-operator.crunchydata.com/cluster=cluster1 \ 
        -L postgres-operator.crunchydata.com/instance \
        -L postgres-operator.crunchydata.com/role | grep instance1
    ```

    ??? example "Sample output"

        ```{.text .no-copy}
        cluster1-instance1-bmdp-0             4/4     Running     0          24m   cluster1-instance1-bmdp   master
        cluster1-instance1-fm7w-0             4/4     Running     0          24m   cluster1-instance1-fm7w   replica
        cluster1-instance1-ttm9-0             4/4     Running     0          23m   cluster1-instance1-ttm9   replica
        ```

The primary has successfully changed to `cluster1-instance1-bmdp`.
