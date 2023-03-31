# Scale Percona Distribution for PostgreSQL on Kubernetes and OpenShift

One of the great advantages brought by Kubernetes and the OpenShift
platform is the ease of an application scaling. Scaling an application
results in adding or removing the Pods and scheduling them to available
Kubernetes nodes.

Size of the cluster is dynamically controlled by a [pgReplicas.REPLICA-NAME.size key](operator.md#pgreplicas-size) in the [Custom Resource options](operator.md#operator-custom-resource-options) configuration.  That’s why scaling the cluster needs nothing more but changing
this option and applying the updated configuration file. This may be done in a
specifically saved config, or on the fly, using the following command:

``` {.bash data-prompt="$" }
$ kubectl scale --replicas=5 perconapgcluster/cluster1
```

In this example we have changed the number of PostgreSQL Replicas to `5`
instances.
