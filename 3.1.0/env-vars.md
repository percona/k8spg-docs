> For the complete documentation index, see [llms.txt](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/llms.txt).

# Define environment variables

You can configure environment variables in Percona Operator for PostgreSQL for the following purposes:

1. **Operator environment variables** – To control the Operator’s behavior, such as logging, telemetry, and which namespaces it watches. You set these in the Operator Deployment (for example in `deploy/bundle.yaml` or via the [Helm chart](https://github.com/percona/percona-helm-charts/tree/main/charts/pg-operator) values).
1. **Cluster component environment variables** – To customize the behavior of cluster components (PostgreSQL, pgBackRest, pgBouncer). You define these in your cluster Custom Resource and, when needed, store sensitive values in [Kubernetes Secrets](https://kubernetes.io/docs/concepts/configuration/secret/).
1. **Backup and restore environment variables** – To customize backup and restore flows. You can specify the environment variables either directly in the backup / restore manifest, or reference a [Kubernetes Secret](https://kubernetes.io/docs/concepts/configuration/secret/) that stores sensitive values.

## When to use environment variables

| Type                                     | Use cases                                                                                                                                                                                                                                                                                                                                                                                     |
| ---------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Operator environment variables           | - Control logging for debugging and log aggregation - Manage telemetry - Configure which namespaces the Operator watches (single-namespace vs cluster-wide) - Set the number of concurrent reconciliation workers for multi-cluster environments - Enable feature gates such as auto-growable volumes - Set the cert-manager namespace used for Operator-managed `ClusterIssuer` CA resources |
| Cluster component environment variables  | - Customize PostgreSQL, pgBackRest, or pgBouncer behavior - Pass configuration or secrets into Pods - Integrate with external systems or monitoring.                                                                                                                                                                                                                                          |
| Backup and restore environment variables | - Customize backup and restore operations - Pass configuration or secrets into backup / restore Jobs                                                                                                                                                                                                                                                                                          |

## Next steps

[Configure Operator environment variables](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/env-var-operator.html) [Environment variables for cluster components](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/env-var-cluster.html)
