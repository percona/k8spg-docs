# High availability and scaling

One of the great advantages brought by Kubernetes and the OpenShift platform is the ease of an application scaling. Scaling an application results in adding resources or Pods and scheduling them to available Kubernetes nodes.

Scaling can be vertical and horizontal. Vertical scaling adds more compute or storage resources to PostgreSQL nodes; horizontal scaling is about adding more nodes to the cluster. High availability looks technically similar, because it also involves additional nodes, but the reason is maintaining liveness of the system in case of server or network failures. 

## Vertical scaling

There are multiple components that Operator deploys and manages: PostgreSQL instances, pgBouncer connection pooler, etc. To add or reduce CPU or Memory you need to edit corresponding sections in the Custom Resource. We follow the structure for requests and limits that Kubernetes [provides](https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/).

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

Percona Operator allows you to deploy highly-available PostgreSQL clusters.
There are two ways how to control replicas in your HA cluster:

1. Through changing `spec.instances.replicas` value
2. By adding new entry into `spec.instances`

## Using `spec.instances.replicas`

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

## Using `spec.instances`

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
