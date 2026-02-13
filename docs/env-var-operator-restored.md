# Configure Operator environment variables

You can configure the Percona Operator for PostgreSQL behavior by setting environment variables in the Operator Deployment. You can set them in the following ways:

* **kubectl** – Edit the Operator Deployment manifest (`deploy/operator.yaml`, `deploy/bundle.yaml`, or `deploy/cw-bundle.yaml`) before applying it, or change the existing Deployment using `kubectl patch` or `kubectl edit`.
* **Helm** – Set environment variables through [Helm](helm.md) values when you install the `percona/pg-operator` chart.
* **OpenShift** – Edit the manifest and apply with `oc apply`. If you installed via the [Operator Lifecycle Manager (OLM)](openshift.md#install-the-operator-via-the-operator-lifecycle-manager-olm), edit the Operator Deployment or Subscription after install to add or change environment variables.

## Available environment variables

### `LOG_STRUCTURED`

Controls whether Operator logs are structured (JSON format) or plain text.

| Value type | Default | Example |
| ---------- | ------- | ------- |
| string     | `"false"` | `"true"` |

When set to `"true"`, the Operator outputs logs in structured JSON format, which helps log aggregation systems. When set to `"false"` (default), logs are plain text.

**Example configuration:**

```yaml
env:
  - name: LOG_STRUCTURED
    value: "true"
```

### `LOG_LEVEL`

Sets the verbosity of Operator logs.

| Value type | Default | Example |
| ---------- | ------- | ------- |
| string     | `"INFO"` | `"DEBUG"` |

Valid values are:

* `"DEBUG"` – Most verbose, includes detailed debugging information
* `"INFO"` – Standard informational messages (default)
* `"ERROR"` – Error messages only

**Example configuration:**

```yaml
env:
  - name: LOG_LEVEL
    value: "DEBUG"
```

### `WATCH_NAMESPACE`

Specifies which namespaces the Operator watches for Custom Resources (PerconaPGCluster and related resources).

| Value type | Default | Example |
| ---------- | ------- | ------- |
| string     | Operator's namespace (from `fieldRef`) | `"pg-operator,percona-db-1"` or `""` |

* If set to a comma-separated list of namespaces, the Operator watches only those namespaces (include the namespace where the Operator runs).
* If set to an empty string (`""`), the Operator watches all namespaces in the cluster.
* If not set (or set from the Deployment's namespace via `fieldRef`), the Operator watches only its own namespace.

**Example configuration for cluster-wide mode:**

```yaml
env:
  - name: WATCH_NAMESPACE
    value: "pg-operator,percona-db-1"
```

See [single-namespace and multi-namespace deployment](cluster-wide.md) for details.

### `DISABLE_TELEMETRY`

Disables the Operator's telemetry data collection.

| Value type | Default | Example |
| ---------- | ------- | ------- |
| string     | `"false"` | `"true"` |

When set to `"true"`, the Operator does not send anonymous telemetry data to Percona.

**Example configuration:**

```yaml
env:
  - name: DISABLE_TELEMETRY
    value: "true"
```

See [Telemetry](telemetry.md) for more information about what data is collected.

### `PGO_WORKERS`

Controls the number of concurrent workers that reconcile PostgreSQL clusters.

| Value type | Default | Example |
| ---------- | ------- | ------- |
| string     | `"1"`   | `"2"`   |

This variable limits how many clusters the Operator reconciles at the same time. Increasing it can improve performance when you run many clusters; set it to the number of clusters for parallel reconciliation.

See [Configure concurrency for a cluster reconciliation](reconciliation-concurrency.md) for step-by-step instructions.

**Example configuration:**

```yaml
env:
  - name: PGO_WORKERS
    value: "2"
```

### `PGO_FEATURE_GATES`

Enables specific features for the Operator.

| Value type | Default | Example |
| ---------- | ------- | ------- |
| string     | `""` (empty) | `"AutoGrowVolumes=true"` |

**Supported values:**

* `AutoGrowVolumes=true` – Enables automatic PVC resize when storage usage reaches a threshold. The Operator can trigger volume expansion for database data volumes. See [Scale your cluster](scaling.md#enable-automatic-storage-resize).

**Example configuration:**

```yaml
env:
  - name: PGO_FEATURE_GATES
    value: "AutoGrowVolumes=true"
```

### Automatic environment variables

The following environment variable is set automatically by Kubernetes and should not be configured manually:

* `PGO_NAMESPACE` – The namespace where the Operator runs (set from `metadata.namespace` via a downward API `fieldRef`).

## Update environment variables

### Using kubectl patch

You can update environment variables in an existing Operator Deployment by applying a patch. To keep existing variables, include the full list in your patch.

1. Get the current environment variables:

    ```bash
    kubectl get deployment percona-postgresql-operator -o jsonpath='{.spec.template.spec.containers[0].env}'
    ```

2. Edit the output to add or change a variable (for example `PGO_WORKERS`), then apply a patch with the full `env` list. Alternatively, patch a single entry by index (see [Configure concurrency for a cluster reconciliation](reconciliation-concurrency.md)).

### Using kubectl edit

You can edit the Deployment directly:

```bash
kubectl edit deployment percona-postgresql-operator -n <namespace>
```

Then update the `env` section in the container specification.

### Using Helm

For Helm installations, set or change environment variables through Helm values (for example `logLevel`, `logStructured`, `disableTelemetry`, `watchNamespace`, `watchAllNamespaces`). Refer to the [pg-operator chart](https://github.com/percona/percona-helm-charts/tree/main/charts/pg-operator) documentation for the exact value names and syntax. To add variables not exposed by the chart, use a chart value that merges extra env entries if supported, or switch to patching the Deployment after install.

## After the update

After you change environment variables, the Operator Pod is restarted so the new configuration takes effect.
