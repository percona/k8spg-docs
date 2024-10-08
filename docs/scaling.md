# High availability and scaling

One of the great advantages brought by Kubernetes and the OpenShift platform is the ease of an application scaling. Scaling an application results in adding resources or Pods and scheduling them to available Kubernetes nodes.

Scaling can be vertical and horizontal. Vertical scaling adds more compute or storage resources to PostgreSQL nodes; horizontal scaling is about adding more nodes to the cluster. High availability looks technically similar, because it also involves additional nodes, but the reason is maintaining liveness of the system in case of server or network failures. 

## Vertical scaling

There are multiple components that Operator deploys and manages: PostgreSQL instances, pgBouncer connection pooler, etc. To add or reduce CPU or Memory you need to edit corresponding sections in the Custom Resource. We follow the structure for requests and limits that Kubernetes [provides :octicons-link-external-16:](https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/).

To add more resources to your PostgreSQL instances edit the following section in the Custom Resource:

```yaml
spec:
...
  instances:
  - name: instance1
    replicas: 3
    resources:
      limits:
        cpu: 2.0
        memory: 4Gi
```

Use our reference documentation for the [Custom Resource options](operator.md) for more details about other components.

## High availability

Percona Operator allows you to deploy highly-available PostgreSQL clusters. High-availability implementation is based on the Patroni template, which uses PostgreSQL streaming replication. The cluster includes a number of replicas, one of which is a primary PostgreSQL instance: it is available for writes, and streams changes to other replicas (*standby servers* in terms of PostgreSQL). Streaming replication used in this configuration is *asynchronous* by default, which means transferring data to a different instance without waiting for a confirmation of its receiving. Alternatively, a *synchronous* replication can be used, where the data transfer waits for a confirmation of its successful processing on the standby. If the primary server crashes then some transactions that were committed may not have been replicated to the standby server, causing data loss (the amount of data loss is proportional to the replication delay at the time of failover). Synchronous replication is slower but minimizes the data loss possibility in case if the primary server crash.

There are two ways how to control the number replicas in your HA cluster:

1. Through changing `spec.instances.replicas` value
2. By adding new entry into `spec.instances`

### Using `spec.instances.replicas`

For example, you have the following Custom Resource manifest:

```yaml
spec:
...
  instances:
    - name: instance1
      replicas: 2
```

This will provision a cluster with two nodes - one Primary and one Replica.
Add the node by changing the manifest...

```yaml hl_lines="5"
spec:
...
  instances:
    - name: instance1
      replicas: 3
```

...and applying the Custom Resource:

``` {.bash data-prompt="$" }
$ kubectl apply -f deploy/cr.yaml
```

The Operator will provision a new replica node. It will be ready and available
once data is synchronized from Primary.

### Using `spec.instances`

Each instance's entry has its own set of parameters, like resources, storage
configuration, sidecars, etc. When you add a new entry into instances, this
creates replica PostgreSQL nodes, but with a new set of parameters. This can be
useful in various cases:

* Test or migrate to new hardware
* Blue-green deployment of a new configuration
* Try out new versions of your sidecar containers

For example, you have the following Custom Resource manifest:

```yaml
spec:
...
  instances:
    - name: instance1
      replicas: 2
      dataVolumeClaimSpec:
        storageClassName: old-ssd
        accessModes:
        - ReadWriteOnce
        resources:
          requests:
            storage: 100Gi
```

Now you have a goal to migrate to new disks, which are coming with the `new-ssd`
storage class. You can create a new instance entry. This will instruct the
Operator to create additional nodes with the new configuration keeping your
existing nodes intact.

```yaml
spec:
...
  instances:
    - name: instance1
      replicas: 2
      dataVolumeClaimSpec:
        storageClassName: old-ssd
        accessModes:
        - ReadWriteOnce
        resources:
          requests:
            storage: 100Gi
    - name: instance2
      replicas: 2
      dataVolumeClaimSpec:
        storageClassName: new-ssd
        accessModes:
        - ReadWriteOnce
        resources:
          requests:
            storage: 100Gi
```

### Using Synchronous replication

Synchronous replication offers the ability to confirm that all changes made by a transaction have been transferred to one or more synchronous standby servers. When requesting synchronous replication, each commit of a write transaction will wait until confirmation is received that the commit has been written to the write-ahead log on disk of both the primary and standby server. The drawbacks of synchronous replication are increased latency and reduced throughput on writes.

You can turn on synchronous replication by customizing the `patroni.dynamicConfiguration` Custom Resource option. 

* Enable synchronous replication by setting `synchronous_mode` option to `on`.
* Use `synchronous_node_count` option to set the number of replicas (PostgreSQL standby servers) which should operate in syncrhonous mode (the default value is `1`).

The result in your `deploy/cr.yaml` manifest may look as follows:

```yaml
...
  patroni:
    dynamicConfiguration:
      synchronous_mode: "on"
      synchronous_node_count: 2
      ...
```

You will have the desired amount of replicas switched to synchronous replication after applying changes as usual, with `kubectl apply -f deploy/cr.yaml` command. 

Find more options useful to tune how your database cluster should operate in synchronous mode [in the official Patroni documentation :octicons-link-external-16:](https://patroni.readthedocs.io/en/latest/replication_modes.html#synchronous-mode).
