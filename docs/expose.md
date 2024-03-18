# Exposing cluster

The Operator provides entry points for accessing the database by client applications. The database cluster is exposed with regular Kubernetes [Service objects :octicons-link-external-16:](https://kubernetes.io/docs/concepts/services-networking/service/) configured by the Operator.

This document describes the usage of [Custom Resource manifest options](operator.md) to expose the clusters deployed with the Operator. 

## PgBouncer

We recommend exposing the cluster through PgBouncer, which is enabled by default.
You can disable pgBouncer by setting `proxy.pgBouncer.replicas` to 0.

The following example deploys two pgBouncer nodes exposed through a LoadBalancer Service object:

```yaml
proxy:
  pgBouncer:
    replicas: 2
    image: percona/percona-postgresql-operator:{{ release }}-ppg14-pgbouncer
    expose:
      type: LoadBalancer
```

The Service will be called `<clusterName>-pgbouncer`:

``` {.bash data-prompt="$" }
$ kubectl get service
```

???+ example "Expected output"

    ``` {.text .no-copy}
    NAME                 TYPE           CLUSTER-IP     EXTERNAL-IP     PORT(S)          AGE
    cluster1-pgbouncer   LoadBalancer   10.88.8.48     34.133.38.186   5432:30601/TCP   20m
    ```

You can connect to the database using the External IP of the load balancer and
port `5432`.

If your application runs inside the Kubernetes cluster as well, you might want to
use the Cluster IP Service type in `proxy.pgBouncer.expose.type`, which is the
default. In this case to connect to the database use the internal domain name -
`cluster1-pgbouncer.<namespace>.svc.cluster.local`.

## Exposing the cluster without PgBouncer

You can connect to the cluster without a proxy. For that use `<clusterName>-ha`
Service object:

``` {.bash data-prompt="$" }
$ kubectl get service
```

???+ example "Expected output"

    ``` {.text .no-copy}
    NAME                 TYPE        CLUSTER-IP    EXTERNAL-IP   PORT(S)    AGE
    cluster1-ha          ClusterIP   10.88.8.121   <none>        5432/TCP   115s
    ```

This service points to the active primary. In case of failover to the replica
node, will change the endpoint automatically.

To change the Service type, use `expose.type` in the Custom Resource manifest.
For example, the following manifest will expose this service through a load
balancer:

```yaml
spec:
...
  expose:
    type: LoadBalancer
```
