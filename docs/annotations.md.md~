# Labels and annotations

[Labels :material-arrow-top-right:](https://kubernetes.io/docs/concepts/overview/working-with-objects/labels/)
and [annotations :material-arrow-top-right:](https://kubernetes.io/docs/concepts/overview/working-with-objects/annotations/)
are used to attach additional metadata information to Kubernetes resources.

Labels and annotations are rather similar. The difference between them is that
labels are used by Kubernetes to identify and select objects, while annotations
are assigning additional *non-identifying* information to resources.
Therefore, typical role of Annotations is facilitating integration with some
external tools.

## Setting labels and annotations in the Custom Resource

You can set labels and/or annotations as key/value string pairs in the Custom
Resource metadata section of the `deploy/cr.yaml`. For PostgreSQL, pgBouncer and pgBackRest Pods,
use `instances.metadata.annotations`/`instances.metadata.labels`,
`proxy.pgbouncer.metadata.annotations`/`proxy.pgbouncer.metadata.labels`, or
`backups.pgbackrest.metadata.annotations`/`backups.pgbackrest.metadata.labels`
keys as follows:

```yaml
apiVersion: pgv2.percona.com/v2
kind: PerconaPGCluster
...
spec:
...
  instances:
   - name: instance1
     replicas: 3
     metadata:
      annotations:
        my-annotation: value1
      labels:
        my-label: value2
    ...
```

For PostgreSQL and pgBouncer Services, use `expose.annotations`/`expose.labels` or
`proxy.pgbouncer.expose.annotations`/`proxy.pgbouncer.expose.labels` keys as 
follows:

```yaml
apiVersion: pgv2.percona.com/v2
kind: PerconaPGCluster
...
spec:
  ...
  expose:
    annotations:
      my-annotation: value1
    labels:
      my-label: value2
    ...
```

The easiest way to check which labels are attached to a specific object with is
using the additional `--show-labels` option of the `kubectl get` command.
Checking the annotations is not much more difficult: it can be done as in the
following example:

``` {.bash data-prompt="$" }
$ kubectl get service cluster1-pgbouncer -o jsonpath='{.metadata.annotations}'
```

## Settings labels and annotations to the Operator Pod

You can assign labels and/or annotations to the Pod of the Operator itself by
editing the and the [deploy/operator.yaml configuration file :material-arrow-top-right:](https://github.com/percona/percona-server-mongodb-operator/blob/main/deploy/operator.yaml)
before [applying it during the installation](kubernetes.md).

```yaml
apiVersion: apps/v1
kind: Deployment
...
spec:
...
  template:
    metadata:
      labels:
        app.kubernetes.io/component: operator
        app.kubernetes.io/instance: percona-postgresql-operator
        app.kubernetes.io/name: percona-postgresql-operator
        app.kubernetes.io/part-of: percona-postgresql-operator
        pgv2.percona.com/control-plane: postgres-operator
        ...
```


