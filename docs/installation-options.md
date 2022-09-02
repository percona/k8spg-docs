# The Operator installation options

When installing The Operator, you can customize additional configuration options. These options are specified in `deploy/operator.yaml` file and already have reasonable defaults, so most users have no need modifying them.

## General Configuration

These variables affect the general configuration of the PostgreSQL Operator.

| Name                           | Default    | Required           | Description |
|:-------------------------------|:-----------|:------------------:|:------------|
| archive_mode                   | `true`     | :heavy_check_mark: | If `true`, enables archive logging on all newly created clusters |
| archive_timeout                | `60`       | :heavy_check_mark: | Set to a value in seconds to configure the timeout threshold for archiving |
| ccp_image_pull_secret          | `""`       |                    | Name of a Secret with credentials for the container image registries for the PostgreSQL cluster |
| ccp_image_pull_secret_manifest | `""`       |                    | A path to the Secret manifest to be installed in each namespace (optional) |
| create_rbac                    | `true`     | :heavy_check_mark: | Set to `true` if the installer should create the RBAC resources required to run the PostgreSQL Operator |
| delete_operator_namespace      | `false`    |                    | If `true`, the Operator namespace (one defined using the `pgo_operator_namespace` variable) will be deleted when uninstalling the Operator |
| delete_watched_namespaces      | `false`    |                    | If `true`, the Operator watched namespaces (ones defined using the `namespace` variable) will be deleted when uninstalling the Operator |
| disable_telemetry              | `false`    |                    | If `true`, [gathering telemetry by the Operator](telemetry.md) will be disabled |
| namespace                      | `pgo`      |                    | A comma delimited string of all the namespaces [the Operator should manage](cluster-wide.md#install-the-operator-cluster-wide) |
| namespace_mode                 | `disabled` |                    | Determines which namespace permissions are assigned to the PostgreSQL Operator using a ClusterRole; can be `dynamic`, `readonly`, and `disabled` |
| pgo_image_prefix               | `percona/percona-postgresql-operator` | :heavy_check_mark: | The image prefix used when creating containers for the Operator (apiserver, operator, scheduler, etc.) |
| pgo_image_pull_policy          | `Always`   |                    | The [policy](https://kubernetes.io/docs/concepts/containers/images/#updating-images) for updating the Operator images |
| pgo_image_pull_secret          | `""`       |                    | Name of a Secret with credentials for the Operator's container image registries |
| pgo_image_pull_secret_manifest | `""`       |                    | Optionally provides a path to the Secret manifest to be installed in each namespace |
| pgo_image_tag                  | `{{ release }}` | :heavy_check_mark: | Configures the image tag used when creating the Operator's containers (apiserver, operator, scheduler, etc.) |
| pgo_operator_namespace         | `pgo`      | :heavy_check_mark: | The namespace where the Operator will be deployed |

