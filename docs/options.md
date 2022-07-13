# Changing PostgreSQL Options

You may require a configuration change for your application. PostgreSQL
allows customizing the database with configuration files.
You can use a [ConfigMap](https://kubernetes.io/docs/tasks/configure-pod-container/configure-pod-configmap/#create-a-configmap)
to provide the PostgreSQL configuration options specific to the following
configuration files:


* PostgreSQL main configuration, [postgresql.conf](https://www.postgresql.org/docs/current/config-setting.html),
* client authentication configuration, [pg_hba.conf](https://www.postgresql.org/docs/current/auth-pg-hba-conf.html),
* user name configuration, [pg_ident.conf](https://www.postgresql.org/docs/current/auth-username-maps.html).

Configuration options may be applied in two ways:

* globally to all database servers in the cluster via [Patroni Distributed Configuration Store (DCS)](https://patroni.readthedocs.io/en/latest/dynamic_configuration.html),
* locally to each database server (Primary and Replica) within the cluster.

!!! note

    PostgreSQL cluster is managed by the Operator, and so there is no need
    to set custom configuration options in common usage scenarios. Also, changing
    certain options may cause PostgreSQL cluster malfunction. Do not customize
    configuration unless you know what you are doing!

Use the `kubectl` command to create the ConfigMap from external
resources, for more information, see [Configure a Pod to use a
ConfigMap](https://kubernetes.io/docs/tasks/configure-pod-container/configure-pod-configmap/#create-a-configmap).

You can either create a PostgreSQL Cluster With Custom Configuration, or
use ConfigMap to set options for the already existing cluster.

To create a cluster with custom options, you should first place these options
in a `postgres-ha.yaml` file under specific `bootstrap` section, then
use `kubectl create configmap` command with this file to create a ConfigMap,
and finally put the ConfigMap name to [pgPrimary.customconfig](operator.md#pgprimary-customconfig)
key in the `deploy/cr.yaml` configuration file.

In both cases, the `postgres-ha.yaml` file doesn’t fully overwrite PostgreSQL
configuration files: options present in `postgres-ha.yaml` will be
overwritten, while non-present options will be left intact.

## Creating a cluster with custom options

For example, you can create a cluster with a custom `max_connections` option
in a `postgresql.conf` configuration file using the following `postgres-ha.yaml`
contents:

```yaml
---
bootstrap:
  dcs:
    postgresql:
      parameters:
        max_connections: 30
```

!!! note

    `dsc.postgresql` subsection means that option will be applied
    globally to `postgresql.conf` of all database servers.

You can create a ConfigMap from this file. The syntax for `kubectl create configmap` command is:

```bash
kubectl -n <namespace> create configmap <configmap-name> --from-file=postgres-ha.yaml
```

ConfigMap name should include your cluster name and a dash as a prefix
(`cluster1-` by default).

The following example defines `cluster1-custom-config` as the ConfigMap name:

```bash
$ kubectl create -n pgo configmap cluster1-custom-config --from-file=postgres-ha.yaml
```

To view the created ConfigMap, use the following command:

```bash
$ kubectl describe configmaps cluster1-custom-config
```

Don’t forget to put the name of your ConfigMap to the `deploy/cr.yaml`
configuration file:

```yaml
spec:
  ...
  pgPrimary:
    ...
      customconfig: "cluster1-custom-config"
```

Now you can create the cluster following the [regular installation instructions](index.md#operator-install).

## Modifying options for the existing cluster

If you need to update cluster’s configuration settings, you should modify
settings in the `<clusterName>-pgha-config` ConfigMap.

!!! note

    This ConfigMap contains `<clusterName>-dcs-config` configuration
    applied globally to `postgresql.conf` of all database servers, and
    local configurations for the PostgreSQL cluster database servers:
    `<clusterName>-local-config` for the current primary,
    `<clusterName>-repl1-local-config` for the first replica, and so on.

For example, let’s change the `max_connections` option in a globally applied
`postgresql.conf` configuration file for the cluster named `cluster1`.
Edit the `cluster1-pgha-config` ConfigMap with the following command:

```bash
$ kubectl edit -n pgo configmap cluster1-pgha-config
```

This will open the ConfigMap in a local text editor of your choice. Make sure
to modify it as follows:

```yaml
...
cluster1-dcs-config: |
  postgresql:
    parameters:
     ...
     max_connections: 50
     ...
```

Now [restart the cluster](pause.md#operator-pause) to ensure the update took effect.

You can check if the changes are applied by querying the appropriate Pods of
your cluster using the `kubectl exec` command with a specific Pod name.

First find out names of your Pods in a common way, using the `kubectl get pods`
command:

```bash
$ kubectl get pods
NAME                                              READY   STATUS    RESTARTS   AGE
backrest-backup-cluster1-j275w                    0/1     Completed 0          10m
cluster1-85486d645f-gpxzb                         1/1     Running   0          10m
cluster1-backrest-shared-repo-6495464548-c8wvl    1/1     Running   0          10m
cluster1-pgbouncer-fc45869f7-s86rf                1/1     Running   0          10m
pgo-deploy-rhv6k                                  0/1     Completed 0          5m
postgres-operator-8646c68b57-z8m62                4/4     Running   1          5m
```

Now let’s check the `cluster1-85486d645f-gpxzb` Pod for the current
`max_connections` value:

```bash
$ kubectl -n pgo exec -it cluster1-85486d645f-gpxzb -- psql -c 'show max_connections;'
  max_connections
  -----------------
  50
  (1 row)
```
