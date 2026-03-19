# Configure the Operator environment variables

You can configure the Percona Operator for PostgreSQL behavior by setting environment variables in the Operator Deployment. You can set them when you install the Operator in the following ways:

* For installations via `kubectl`, edit the Operator Deployment manifest `deploy/operator.yaml` or `deploy/cw-operator.yaml`. Alternatively you can modify the Deployment resource in `deploy/bundle.yaml`, or `deploy/cw-bundle.yaml` files.
* For Helm installations you can set environment variables through Helm values when you install the `percona/pg-operator` chart.
* For installations on OpenShift, you can edit the manifests and apply them with the `oc apply` command. If you installed via the [Operator Lifecycle Manager (OLM)](openshift.md#install-the-operator-via-the-operator-lifecycle-manager-olm), you can configure environment variables through the OLM subscription.

## Available environment variables

### `LOG_LEVEL`

Controls the verbosity of the operator's logging output. This helps with debugging and monitoring the Operator behavior. 

| Value type | Default | Example |
| ---------- | ------- | ------- |
| string     | `"INFO"` | `"DEBUG"` |

Accepted values are:

- `"DEBUG"` – Most verbose, includes detailed debugging information
- `"INFO"` – Standard informational messages (default)
- `"WARN"` – Warning messages only
- `"ERROR"` – Error messages only

**Example configuration:**

```yaml
spec:
  containers:
  - name: percona-postgresql-operator
    env:
    - name: LOG_LEVEL
      value: "DEBUG"
```

### `DISABLE_TELEMETRY`

Controls whether the Operator sends anonymous telemetry data to Percona. Telemetry helps Percona understand usage patterns and improve the Operator. 

| Value type | Default | Example |
| ---------- | ------- | ------- |
| string     | `"false"` | `"true"` |

<<<<<<< K8SPG-758-Doc-Pprof-binding
When set to `"true"`, the Operator does not send anonymous telemetry data to Percona.
=======
When set to `true`, the Operator does not send anonymous telemetry data to Percona.
>>>>>>> 2.0

Learn more about [Telemetry](telemetry.md).

**Example configuration:**

```yaml
spec:
  containers:
  - name: percona-postgresql-operator
    env:
    - name: DISABLE_TELEMETRY
      value: "true"
```

### `PGO_FEATURE_GATES`

Enables experimental or advanced features in the Operator. Feature gates allow you to opt into specific functionality that may not be enabled by default.

The value needs to be a key-value with comma-separated list of feature gates. By default this variable is not set in the Operator.

| Value type | Default | Example |
| ---------- | ------- | ------- |
| string     | `""` (empty) | `"AutoGrowVolumes=true"` |

Following feature gates are present as of Operator version 2.8.1:

1. `AutoGrowVolumes=true` - Enables automatic PVC resize when the storage usage reaches a threshold. The Operator can trigger volume expansion for database data volumes. To learn more, refer to the [Scale your cluster](scaling.md#enable-automatic-storage-resize) chapter.

**Example configuration:**

```yaml
spec:
  containers:
  - name: percona-postgresql-operator
    env:
    - name: PGO_FEATURE_GATES
      value: "AutoGrowVolumes=true"
```

### `LOG_STRUCTURED`

Controls whether the Operator outputs logs in a structured JSON format instead of the plain text. Structured logging is useful for log aggregation tools.

| Value type | Default | Example |
| ---------- | ------- | ------- |
| string     | `"false"` | `"true"` |

When set to `"true"`, the logs are produced in JSON format. When set to `"false"` or not set at all, the Operator outputs plain text logs. This is the default behavior.

**Example configuration:**

```yaml
spec:
  containers:
  - name: percona-postgresql-operator
    env:
    - name: LOG_STRUCTURED
      value: "true"
```

### `PGO_WORKERS`

Specifies the number of worker threads the Operator uses to process events and reconcile resources. This controls the Operator's concurrency. Default value is `1`.

| Value type | Default | Example |
| ---------- | ------- | ------- |
| string     | `"1"`   | `"2"`   |

Keep in mind that concurrent reconciliations are done only on different objects. For the same object reconciliation is always done serially, regardless of the value set in `PGO_WORKERS`. This is defined by how the controller runtime works with the queue to avoid any race conditions or incorrect modification of objects. 

To illustrate how it works:

* If you have two PerconaPGCluster objects (A and B) and set `PGO_WORKERS=1`, a single worker thread will reconcile the clusters serially, one after another.  
* If you set `PGO_WORKERS=4` but only have one PerconaPGCluster object, the Operator still reconciles this object serially.  
* If you set `PGO_WORKERS=4` and have two PerconaPGCluster objects (A and B), the Operator uses two separate threads to reconcile each object in parallel; however, it always processes events for each individual object sequentially.

**Example configuration:**

```yaml
spec:
  containers:
  - name: percona-postgresql-operator
    env:
    - name: PGO_WORKERS
      value: "4"
```

### `WATCH_NAMESPACE`

Specifies which namespaces the Operator watches for Custom Resources (PerconaPGCluster and related resources). This is a critical configuration for determining the Operator's scope of operation. 

By default, the value is set to the Operator's own namespace from the `metadata.namespace` option via a downward API `fieldRef`:

```yaml
- name: WATCH_NAMESPACE
  valueFrom:
    fieldRef:
      apiVersion: v1
      fieldPath: metadata.namespace
```

| Value type | Default | Example |
| ---------- | ------- | ------- |
| string     | Operator's namespace (from `fieldRef`) | `"pg-operator,percona-db-1"` or `""` |

Accepted values:

* If set to a comma-separated list, the Operator watches those specific namespaces. The namespace list must include the namespace where the Operator itself is deployed. Use this approach for the [cluster-wide mode](cluster-wide.md).
* If set to an empty string (`""`), the Operator watches all namespaces in the Kubernetes cluster (cluster-wide mode).

When you deploy the Operator in cluster-wide mode, it should be associated with the appropriate ClusterRole. 

**Example configuration:**

```yaml
spec:
  containers:
  - name: percona-postgresql-operator
    env:
    - name: WATCH_NAMESPACE
      value: "pg-operator,percona-db-1,percona-db-2"
```

### `PGO_NAMESPACE`

Specifies the Kubernetes namespace where the Operator itself is deployed and runs. The value is set automatically by Kubernetes from `metadata.namespace` via a downward API `fieldRef`.

This variable is used by the Operator to refer objects like Secrets for the normal functioning of the Operator.

This is particularly important in [cluster-wide](cluster-wide.md) deployment scenarios where the Operator manages resources across multiple namespaces.

**Example configuration:**

```yaml
spec:
  containers:
  - name: percona-postgresql-operator
    env:
    - name: PGO_NAMESPACE
      value: "pg-operator"
```

<<<<<<< K8SPG-758-Doc-Pprof-binding
### `PPROF_BIND_ADDRESS`

Specifies the TCP address that the controller binds to for serving pprof profiling endpoints. Use this when you need to collect CPU or memory profiles or investigate Operator performance issues.

| Value type | Default | Example |
| ---------- | ------- | ------- |
| string     | `"0"` (disabled) | `"127.0.0.1:6060"` |

When set to `""` or `"0"`, pprof serving is disabled. Set it to an address such as `127.0.0.1:6060` to enable profiling. You can then use `kubectl port-forward` to access the pprof endpoints from your local machine.

See [Profiling the Operator with pprof](troubleshoot-operator.md#profiling-the-operator-with-pprof) for usage instructions.

**Example configuration:**

```yaml
spec:
  containers:
  - name: percona-postgresql-operator
    env:
    - name: PPROF_BIND_ADDRESS
      value: "127.0.0.1:6060"
```

=======
>>>>>>> 2.0
## Update environment variables

### Using kubectl patch

You can update environment variables in an existing Operator Deployment by applying a patch. To keep existing variables, include the full list in your patch.

1. Get the current environment variables:

    ```bash
    kubectl get deployment percona-postgresql-operator -o jsonpath='{.spec.template.spec.containers[0].env}'
    ```

2. Edit the output to add or change a variable (for example `PGO_WORKERS`), then apply a patch with the full `env` list. Alternatively, patch a single entry by index (see [Configure concurrency for a cluster reconciliation](reconciliation-concurrency.md)).


### Using Helm

For Helm installations, set or change environment variables through Helm values (for example `logLevel`, `logStructured`, `disableTelemetry`, `watchNamespace`, `watchAllNamespaces`). Refer to the [pg-operator chart](https://github.com/percona/percona-helm-charts/tree/main/charts/pg-operator) documentation for the exact value names and syntax. To add variables not exposed by the chart, use a chart value that merges extra env entries if supported, or switch to patching the Deployment after install.

## After the update

After you change environment variables, the Operator Pod is restarted so the new configuration takes effect.
