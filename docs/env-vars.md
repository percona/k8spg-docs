# Define environment variables

You can configure environment variables in Percona Operator for PostgreSQL for the following purposes:

1. **Operator environment variables** – To control the Operator's behavior, such as logging, telemetry, and which namespaces it watches. You set these in the Operator Deployment (for example in `deploy/bundle.yaml` or via the [Helm chart](https://github.com/percona/percona-helm-charts/tree/main/charts/pg-operator) values).
2. **Cluster component environment variables** – To customize the behavior of cluster components (PostgreSQL, pgBackRest, pgBouncer). You define these in your cluster Custom Resource and, when needed, store sensitive values in [Kubernetes Secrets](https://kubernetes.io/docs/concepts/configuration/secret/).
3. **Backup and restore environment variables** – To customize backup and restore flows. You can specify the environment variables either directly in the backup / restore manifest, or reference a [Kubernetes Secret](https://kubernetes.io/docs/concepts/configuration/secret/) that stores sensitive values.

## When to use environment variables

| Type                                  | Use cases |
| ------------------------------------- | --------- |
| Operator environment variables       | - Control logging for debugging and log aggregation <br> - Manage telemetry <br> - Configure which namespaces the Operator watches (single-namespace vs cluster-wide) <br> - Set the number of concurrent reconciliation workers for multi-cluster environments <br> - Enable feature gates such as auto-growable volumes <br> - Set the cert-manager namespace used for Operator-managed `ClusterIssuer` CA resources |
| Cluster component environment variables | - Customize PostgreSQL, pgBackRest, or pgBouncer behavior <br> - Pass configuration or secrets into Pods <br> - Integrate with external systems or monitoring. |
| Backup and restore environment variables | - Customize backup and restore operations <br> - Pass configuration or secrets into backup / restore Jobs |

## Next steps

[Configure Operator environment variables](env-var-operator.md){.md-button}
[Environment variables for cluster components](env-var-cluster.md){.md-button}
