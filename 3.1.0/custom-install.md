> For the complete documentation index, see [llms.txt](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/llms.txt).

# Install Percona Operator for PostgreSQL with customized parameters

You can customize the configuration of Percona Distribution for PostgreSQL and install it with customized parameters.

To check available configuration options, see [deploy/cr.yaml](https://raw.githubusercontent.com/percona/percona-postgresql-operator/v3.1.0/deploy/cr.yaml) and [Custom Resource Options](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/operator.html).

**kubectl**

To customize the configuration when installing with `kubectl`, do the following:

1. Clone the repository with all manifests and source code by executing the following command:

   ```
   git clone -b v3.1.0 https://github.com/percona/percona-postgresql-operator
   ```

1. Edit the required options and apply your modified `deploy/cr.yaml` file as follows:

   ```
   kubectl apply -f deploy/cr.yaml -n postgres-operator
   ```

**Helm**

You can install the Operator deployment and the Percona Distribution for PostgreSQL cluster with custom parameters using Helm. Find what options you can customize in the [Operator chart documentation](https://github.com/percona/percona-helm-charts/tree/main/charts/pg-operator#installing-the-chart) and the [Percona Distribution for PostgreSQL chart documentation](https://github.com/percona/percona-helm-charts/tree/main/charts/pg-db#installing-the-chart) .

You can provide custom parameters to Helm using either the `--set` flag or a `values.yaml` file. The `--set` flag is convenient for overriding a small number of parameters directly in the command line, while a `values.yaml` file is preferable when you want to manage many custom settings in one place. Both methods are fully supported by Helm and can be used as needed for your deployment.

**Using `--set` flags**

To pass a custom parameter to Helm, use the `--set key=value` flag with the `helm install` command.

For example, to enable [Percona Monitoring and Management (PMM)](https://docs.percona.com/percona-monitoring-and-management/3/index.html) for the database cluster, run:

```
helm install my-db percona/pg-db --version 3.1.0 --namespace my-namespace \
  --set postgresVersion=18.6.1-3 \
  --set pmm.enabled=true
```

**Using a `values.yaml` file**

Create a `values.yaml` file with your custom parameters and pass it to `helm install` with the `-f` or `--values` flag:

```
helm install my-db percona/pg-db --version 3.1.0 --namespace my-namespace -f values.yaml
```

Example `values.yaml`:

```
postgresVersion: 18.6.1-3
pmm:
  enabled: true
```

## Naming conventions for Helm resources

When you install a chart, Helm creates a release and uses the release name and chart name to generate resource names. By default, resources are named `release-name-chart-name`.

You can override the default naming with the `nameOverride` or `fullnameOverride` options. Pass them using the `--set` flag or in your `values.yaml` file.

| Option             | Effect                                                                   | Example                      |
| ------------------ | ------------------------------------------------------------------------ | ---------------------------- |
| `nameOverride`     | Replaces the chart name but keeps the release name in the generated name | `release-name-name-override` |
| `fullnameOverride` | Replaces the entire generated name with the specified value              | `fullname-override`          |

*Using `nameOverride`* — replaces the chart name but keeps the release name:

```
helm install my-operator percona/pg-operator --namespace my-namespace \
  --set nameOverride=postgres-operator
```

Deployment name: `my-operator-postgres-operator`.

```
helm install cluster1 percona/pg-db -n my-namespace \
  --set nameOverride=postgres
```

Cluster name: `cluster1-postgres`.

*Using `fullnameOverride`* — replaces the full resource name:

```
helm install my-operator percona/pg-operator --namespace my-namespace \
  --set fullnameOverride=percona-postgresql-operator
```

Deployment name: `percona-postgresql-operator`.

```
helm install cluster1 percona/pg-db -n my-namespace \
  --set fullnameOverride=my-db
```

Cluster name: `my-db`.

Cluster name length

For the pg-db chart, the cluster name is limited to 21 characters, must consist of lowercase alphanumeric characters, ‘-’ or ‘.’, and must start and end with an alphanumeric character. Keep this in mind when using `fullnameOverride` or long release names.

## Common Helm values reference

The following table lists commonly used values for the Operator and database charts. For the full list of options, see the chart values files.

| Value                | Charts                                                                                                                                                                                             | Description                                                                                                                              |
| -------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------- |
| `nameOverride`       | [pg-operator](https://github.com/percona/percona-helm-charts/blob/main/charts/pg-operator/values.yaml), [pg-db](https://github.com/percona/percona-helm-charts/blob/main/charts/pg-db/values.yaml) | Replaces the chart name in generated resource names                                                                                      |
| `fullnameOverride`   | [pg-operator](https://github.com/percona/percona-helm-charts/blob/main/charts/pg-operator/values.yaml), [pg-db](https://github.com/percona/percona-helm-charts/blob/main/charts/pg-db/values.yaml) | Replaces the entire generated resource name                                                                                              |
| `watchAllNamespaces` | [pg-operator](https://github.com/percona/percona-helm-charts/blob/main/charts/pg-operator/values.yaml)                                                                                             | Deploy the Operator in cluster-wide mode to watch all namespaces                                                                         |
| `disableTelemetry`   | [pg-operator](https://github.com/percona/percona-helm-charts/blob/main/charts/pg-operator/values.yaml)                                                                                             | Disable telemetry collection. See [Telemetry](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/telemetry.html) for details |
