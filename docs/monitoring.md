# Monitor with Percona Monitoring and Management (PMM)

{% include 'assets/fragments/monitoring.txt' %}

## Run the PMM Client with a read-only root filesystem

Starting with version 3.1.0, set `readOnlyRootFilesystem` to `true` under [`pmm.containerSecurityContext`](operator.md#pmmcontainersecuritycontext) to run the PMM Client container with a read-only root filesystem. The Operator writes the PMM agent configuration to `/tmp/pmm-agent.yaml` on the Pod's `/tmp` volume. That volume stays writable when the root filesystem is read-only. Use this setting on platforms that require a read-only root filesystem, such as the OpenShift `restricted-v2` security context constraint.

If you leave `containerSecurityContext` unset, the container root filesystem stays writable.

```yaml
pmm:
  enabled: true
  image: percona/pmm-client:{{pmm3recommended}}
  secret: cluster1-pmm-secret
  serverHost: monitoring-service
  containerSecurityContext:
    readOnlyRootFilesystem: true
```

Apply the manifest:

```bash
kubectl apply -f deploy/cr.yaml -n postgres-operator
```

## Update the secrets file

The `deploy/secrets.yaml` file contains all values for each key/value pair in a convenient plain text format. But the resulting Secrets Objects contains passwords stored as base64-encoded strings. If you want to *update* the password field, you need to encode the new password into the base64 format and pass it to the Secrets Object.
{.power-number}

To encode a password or any other parameter, run the following command:

=== ":simple-linux: Linux"

    ```bash 
    echo -n "password" | base64 --wrap=0
    ``` 

=== ":simple-apple: macOS"

    ```bash 
    echo -n "password" | base64
    ```

For example, to set the new service account token in the `my-cluster-name-secrets` object, do the following:

=== ":simple-linux: Linux"

    ```bash
    kubectl -n <namespace> patch secret/cluster1-pmm-secret -p '{"data":{"PMM_SERVER_TOKEN": '$(echo -n <new-token> | base64 --wrap=0)'}}'
    ```

=== ":simple-apple: macOS"

    ```bash
    kubectl -n <namespace> patch secret/cluster1-pmm-secret -p '{"data":{"PMM_SERVER_TOKEN": '$(echo -n <new-token> | base64)'}}'
    ```
