# Configure concurrency for a cluster reconciliation

Reconciliation is the process by which the Operator continuously compares the desired state with the actual state of the cluster. The desired state is defined in a Kubernetes custom resource, like PostgresCluster. 

If the actual state does not match the desired state, the Operator takes actions to bring the system into alignment—such as creating, updating, or deleting Kubernetes resources (Pods, Services, ConfigMaps, etc.) or performing database-specific operations like scaling, backups, or failover.

Reconciliation is triggered by a variety of events, including:

- Changes to the cluster configuration
- Changes to the cluster state
- Changes to the cluster resources

By default, the Operator has one reconciliation worker. This means that if you deploy or update 2 clusters at the same time, the Operator will reconcile them sequentially. 

The `PGO_WORKERS` environment variable in the `percona-postgresql-operator` deployment controls the number of concurrent workers that can reconcile resources in PostgresSQL clusters in parallel.

Thus, to extend the previous example, if you set the number of reconciliation workers to `2`, the Operator will reconcile both clusters in parallel. This also helps you with benchmarking the Operator performance.

The general recommendation is to set the number of concurrent workers equal to the number of PostgreSQL clusters. When the number of workers is greater, the excessive workers will remain idle.

## Set the number of reconciliation workers 

1. Check the index of the `PGO_WORKERS` environment variable using the following command: 
    
    ```bash
    kubectl get deployment percona-postgresql-operator -o jsonpath='{.spec.template.spec.containers[0].env[?(@.name=="PGO_WORKERS")].value}'
    ```

    ??? example "Sample output"

        ```{.json .no-copy}
        [
          {
            "name": "WATCH_NAMESPACE",
            "valueFrom": {
              "fieldRef": {
                "apiVersion": "v1",
                "fieldPath": "metadata.namespace"
              }
            }
          },
          {
            "name": "PGO_NAMESPACE",
            "valueFrom": {
              "fieldRef": {
                "apiVersion": "v1",
                "fieldPath": "metadata.namespace"
              }
            }
          },
          {
            "name": "LOG_STRUCTURED",
            "value": "false"
          },
          {
            "name": "LOG_LEVEL",
            "value": "INFO"
          },
          {
            "name": "DISABLE_TELEMETRY",
            "value": "false"
          },
          {
            "name": "PGO_WORKERS",
            "value": "2"
          }
        ]
        ```

        The index is zero-based, thus `PGO_WORKERS` has index 5.

2. List deployments to find the right one:

    ```bash
    kubectl get deployment
    ```
   
    ??? example "Sample output"

        ```{.text .no-copy}
        NAME                          READY   UP-TO-DATE   AVAILABLE   AGE
        cluster1-pgbouncer            3/3     3            3           3h49m
        percona-postgresql-operator   0/1     1            0           3h50m
        ```

3. To set a new value, run the following command to patch the deployment:

    ```bash
    kubectl patch deployment percona-postgresql-operator \
      --type='json' \
      -p='[{"op": "replace", "path": "/spec/template/spec/containers/0/env/5", "value": {"name": "PGO_WORKERS", "value": "2"}}]'
    ```

The command does the following:

- Patches the deployment to update the `PGO_WORKERS` environment variable
- Sets the value to `2`

The value can be set to any number greater than 0.

## Verify the change

To verify that the change has been applied, run the following command:

```bash
kubectl get deployment percona-postgresql-operator -o jsonpath='{.spec.template.spec.containers[0].env[?(@.name=="PGO_WORKERS")].value}'
```

The output should be `2`.