> For the complete documentation index, see [llms.txt](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/llms.txt).

# Change the PostgreSQL primary instance

The Operator uses PostgreSQL high-availability implementation based on the [Patroni template](https://patroni.readthedocs.io/en/latest/faq.html#concepts-and-requirements) . This means that each PostgreSQL cluster includes one member available for read/write transactions (PostgreSQL primary instance, or leader in terms of Patroni) and a number of replicas which can serve read requests only (standby members of the cluster).

You may wish to manually change the primary instance in your PostgreSQL cluster to achieve more control and meet specific requirements in various scenarios like planned maintenance, testing failover procedures, load balancing and performance optimization activities. Primary instance is re-elected during the automatic failover (Patroni’s “leader race” mechanism), but still there are use cases to control this process manually.

In Percona Operator, the primary instance election can be controlled by the `patroni.switchover` section of the Custom Resource manifest. It allows you to enable switchover targeting a specific PostgreSQL instance as the new primary, or just running a failover if PostgreSQL cluster has entered a bad state.

This document provides instructions how to change the primary instance manually.

For the following steps, we assume that you have the PostgreSQL cluster up and running. The cluster name is `cluster1`.

1. Check the information about the [cluster instances](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/operator.html#operator-instances-section). Cluster instances are defined in the `spec.instances` Custom Resource section. By default you have one cluster instance named `instance1` with 3 PostgreSQL instances in it. You can check which cluster instances you have. Do this using Kubernetes Labels as follows (replace the `<namespace>` placeholder with your value):

   ```
   kubectl get pods -n <namespace> -l postgres-operator.crunchydata.com/cluster=cluster1 \ 
       -L postgres-operator.crunchydata.com/instance \
       -L postgres-operator.crunchydata.com/role | grep instance1
   ```

   Sample output

   ```
   cluster1-instance1-bmdp-0             4/4     Running   0          2m23s   cluster1-instance1-bmdp   replica
   cluster1-instance1-fm7w-0             4/4     Running   0          2m22s   cluster1-instance1-fm7w   replica
   cluster1-instance1-ttm9-0             4/4     Running   0          2m22s   cluster1-instance1-ttm9   master
   ```

   PostgreSQL primary is labeled as `master`, while other PostgreSQL instances are labeled as `replica`.

   Remove the old annotation before you enable switchover again

   A switchover is requested with the `postgres-operator.crunchydata.com/trigger-switchover` annotation. If you did a switchover on this cluster before, that annotation is probably still there. When you set `patroni.switchover.enabled` to `true`, the Operator treats an annotation it hasn’t acted on as a new request and switches over at once, before you set a new annotation in step 3.

   Remove the old annotation before step 2:

   ```
   kubectl annotate -n <namespace> pg cluster1 postgres-operator.crunchydata.com/trigger-switchover-
   ```

   The trailing `-` removes the annotation.

1. Update the following options in the `patroni.switchover` subsection of the Custom Resource:

   ```
   patroni:
     switchover:
       enabled: true
       targetInstance: <instance-name>
   ```

   You can do it with `kubectl patch` command, specifying the name of the instance that you want to be the new primary. For example, let’s set the `cluster1-instance1-bmdp` as a new PostgreSQL primary:

   ```
   kubectl -n <namespace> patch pg cluster1 --type=merge --patch '{
     "spec": {
       "patroni": {
         "switchover": {
           "enabled": true,
           "targetInstance": "cluster1-instance1-bmdp"
         }
       }
     }
   }'
   ```

1. Trigger the switchover by adding the annotation to your Custom Resource. The recommended way is to set the annotation with the timestamp, so you know when switchover took place. Replace the `<namespace>` placeholder with your value:

   ```
   kubectl annotate --overwrite -n <namespace> pg cluster1 postgres-operator.crunchydata.com/trigger-switchover="$(date)"
   ```

   The `--overwrite` flag replaces the value if the annotation already exists. Use a value that you haven’t used before, such as the timestamp. The Operator switches over only when the annotation differs from the one it acted on last.

1. Verify that the cluster was annotated (replace the `<namespace>` placeholder with your value, as usual):

   ```
   kubectl get pg cluster1 -o yaml -n <namespace>
   ```

   Sample output

   ```
   apiVersion: pgv2.percona.com/v2
   kind: PerconaPGCluster
   metadata:
     annotations:
       kubectl.kubernetes.io/last-applied-configuration: |
         {....
         "patroni":{"switchover":{"enabled":true,"targetInstance":"cluster1-instance1-bmdp"}},}
   ```

1. Now, check instances of your cluster once again to make sure the switchover took place:

   ```
   kubectl get pods -n <namespace> -l postgres-operator.crunchydata.com/cluster=cluster1 \
       -L postgres-operator.crunchydata.com/instance \
       -L postgres-operator.crunchydata.com/role | grep instance1
   ```

   Sample output

   ```
   cluster1-instance1-bmdp-0             4/4     Running     0          24m   cluster1-instance1-bmdp   master
   cluster1-instance1-fm7w-0             4/4     Running     0          24m   cluster1-instance1-fm7w   replica
   cluster1-instance1-ttm9-0             4/4     Running     0          23m   cluster1-instance1-ttm9   replica
   ```

1. If you use pgBouncer, check its Pods. After a switchover under client traffic, a pgBouncer Pod can stay on the demoted primary. List the pgBouncer Pods and delete the one that stays on the old primary. The Deployment creates a replacement:

   ```
   kubectl get pods -n <namespace> \
     -l postgres-operator.crunchydata.com/cluster=cluster1,postgres-operator.crunchydata.com/role=pgbouncer

   kubectl delete pod <pgbouncer-pod-name> -n <namespace>
   ```

1. Set `patroni.switchover.enabled` Custom Resource option to `false` once the switchover is done:

   ```
   kubectl -n <namespace> patch pg cluster1 --type=merge --patch '{
     "spec": {
       "patroni": {
         "switchover": {
           "enabled": false
         }
       }
     }
   }'
   ```

1. Remove the annotation, so that it doesn’t trigger a switchover the next time you enable switchover:

   ```
   kubectl annotate -n <namespace> pg cluster1 postgres-operator.crunchydata.com/trigger-switchover-
   ```

   Setting `patroni.switchover.enabled` to `false` clears the Operator’s record of the last completed switchover, but it leaves the annotation on the cluster. Without this step, the next time you set `enabled` to `true`, the Operator sees an annotation it hasn’t acted on and switches over immediately.
