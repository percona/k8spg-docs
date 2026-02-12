# Configure the Operator environment variables

You can configure the Percona Operator for PostgreSQL behavior by setting environment variables in the Operator Deployment. You can set them when you install the Operator in the following ways:

* For installations via `kubectl`, edit the Operator Deployment manifest `deploy/operator.yaml` or `deploy/cw-operator.yaml`. Alternatively you can modify the Deployment resource in `deploy/bundle.yaml`, or `deploy/cw-bundle.yaml` files.
* For Helm installations you can set environment variables through Helm values when you install the `percona/pg-operator` chart.
* For installations on OpenShift, you can edit the manifests and apply them with the `oc apply` command. If you installed via the [Operator Lifecycle Manager (OLM)](openshift.md#install-the-operator-via-the-operator-lifecycle-manager-olm), you can configure environment variables through the OLM subscription.

## Available environment variables

### `LOG_LEVEL`

Controls the verbosity of the operator's logging output. This helps with debugging and monitoring operator behavior. Accepted values are `DEBUG`, `INFO`, `ERROR` and the default log level is `INFO`.

**Example Configuration:**

```yaml
spec:
  containers:
  - name: percona-postgresql-operator
    env:
    - name: LOG_LEVEL
      value: "DEBUG"
```

### `DISABLE_TELEMETRY`

Controls whether the operator sends anonymous telemetry data to Percona. Telemetry helps Percona understand usage patterns and improve the operator, if the value is set to `true` , no telemetry data is sent otherwise telemetry data is sent to the server.

Learn more about telemetry at [telemetry](telemetry.md).

**Example Configuration:**

```yaml
spec:
  containers:
  - name: percona-postgresql-operator
    env:
    - name: DISABLE_TELEMETRY
      value: "true"
```

### `PGO_FEATURE_GATES`

Enables experimental or advanced features in the operator. Feature gates allow you to opt into specific functionality that may not be enabled by default.
Value needs to be a key value with comma-separated list of feature gates. By default this variable is not set in the Operator.
Following feature gates are present as of operator version 2.8.1

1. AutoGrowVolumes=true

**Example Configuration:**

```yaml
spec:
  containers:
  - name: percona-postgresql-operator
    env:
    - name: PGO_FEATURE_GATES
      value: "AutoGrowVolumes=true"
```

### `LOG_STRUCTURED`

Controls whether the operator outputs logs in structured format JSON instead of plain text. Structured logging is useful for log aggregation tools .
`"true"` enables structured logging (JSON format).`"false"` or not setting the environment variable uses plain text logging (default).

**Example Configuration:**

```yaml
spec:
  containers:
  - name: percona-postgresql-operator
    env:
    - name: LOG_STRUCTURED
      value: "true"
```

### `PGO_WORKERS`

Specifies the number of worker threads the operator uses to process events and reconcile resources. This controls the operator's concurrency. Default value is 1.
It is important to note that concurrent reconciliations are done only on different objects, for the same object reconciliation is always done serially immaterial of the value set in PGO_WORKERS. This is defined by how the controller runtime works with the queue to avoid any race conditions or incorrect modification of objects.

Example:
PGO_WORKERS=1 , Two PerconaPGCluster objects(A,B) present => One thread only which reconciles both the objects
PGO_WORKERS=4 , One PerconaPGCluster object present => Reconciliation done serially for this object
PGO_WORKERS=4 , Two PerconaPGCluster objects(A,B) present => 2 Separate threads one for each PerconaPGCluster object, however objects A and B are always processed serially.

**Example Configuration:**

```yaml
spec:
  containers:
  - name: percona-postgresql-operator
    env:
    - name: PGO_WORKERS
      value: "4"
```

### `WATCH_NAMESPACE`

Specifies which Kubernetes namespaces the operator should monitor for PostgreSQL cluster resources. This is a critical configuration for determining the operator's scope of operation. If the `WATCH_NAMESPACE` variable is not set, the operator watches only the namespace where it is deployed.

* If set to a value using a literal string or the downward API, a single namespace is managed (namespace-scoped mode).
* If set to a comma-separated list, the operator watches those specific namespaces. The list must include the namespace where the operator itself is deployed (cluster-wide mode).
* If set to an empty string (""), the operator watches all namespaces in the Kubernetes cluster (cluster-wide mode).

In cluster-wide mode, the operator must be associated with an appropriate ClusterRole.
Read more about deployment methods here: (./2.1.6.1_namespace_modes.md)

**Example Configuration:**

```yaml
spec:
  containers:
  - name: percona-postgresql-operator
    env:
    - name: WATCH_NAMESPACE
      value: "pg-operator,percona-db-1,percona-db-2"
```

### `PGO_NAMESPACE`

Specifies the Kubernetes namespace where the operator itself is deployed and runs. This is used by the operator to refer objects like secrets for the normal functioning of the operator.
This is particularly important in cluster-wide deployment scenarios where the operator manages resources across multiple namespaces.

**Example Configuration:**

```yaml
spec:
  containers:
  - name: percona-postgresql-operator
    env:
    - name: PGO_NAMESPACE
      value: "pg-operator"
```

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
