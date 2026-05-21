# Microsoft Azure Blob Storage

!!! admonition

    Azure Blob Storage support is currently in tech preview.

To use [Microsoft Azure Blob Storage :octicons-link-external-16:](https://azure.microsoft.com/en-us/services/storage/blobs/) for backups, you need the following:

* Azure container name
* Azure Storage account name and key, stored in a [Kubernetes Secret :octicons-link-external-16:](https://kubernetes.io/docs/concepts/configuration/secret/)

## Configuration steps {.power-number}

The examples below use the `repo4` repository name.

1. Encode the Azure Storage credentials and the pgBackRest repo name that you will use for backups with base64:

    === ":simple-linux: Linux"

        ```bash
        cat <<EOF | base64 --wrap=0
        [global]
        repo4-azure-account=<AZURE_STORAGE_ACCOUNT_NAME>
        repo4-azure-key=<AZURE_STORAGE_ACCOUNT_KEY>
        EOF
        ```

    === ":simple-apple: macOS"

        ```bash
        cat <<EOF | base64
        [global]
        repo4-azure-account=<AZURE_STORAGE_ACCOUNT_NAME>
        repo4-azure-key=<AZURE_STORAGE_ACCOUNT_KEY>
        EOF
        ```

2. Create the Secret manifest and set `data.azure.conf` to the encoded string. The following is the example of the  cluster1-pgbackrest-secrets.yaml Secret file:

    ```yaml
    apiVersion: v1
    kind: Secret
    metadata:
      name: cluster1-pgbackrest-secrets
    type: Opaque
    data:
      azure.conf: <base64-encoded-configuration-contents>
    ```

    You can store credentials for several repositories in one Secret by adding separate data keys.

3. Create the Secrets object from this yaml file. Replace `<namespace>` with your namespace:

    ```bash
    kubectl apply -f cluster1-pgbackrest-secrets.yaml -n <namespace>
    ```

4. Update the `deploy/cr.yaml` Custom Resource:
    
    * Reference the Secret in `backups.pgbackrest.configuration`
    * Provide the backup directory path in [backups.pgbackrest.global](operator.md#backupspgbackrestglobal) with the pgBackRest `path` option (for example `repo4-path`). The repository name must match the name used when encoding credentials
    * Specify the Azure container name under `repos`

    ```yaml
    ...
    backups:
      pgbackrest:
        ...
        configuration:
          - secret:
              name: cluster1-pgbackrest-secrets
        ...
        global:
          repo4-path: /pgbackrest/postgres-operator/cluster1/repo4
        ...
        repos:
        - name: repo4
          azure:
            container: "<YOUR_AZURE_CONTAINER>"
    ```

5. Apply the cluster Custom Resource:

    ```bash
    kubectl apply -f deploy/cr.yaml -n <namespace>
    ```

## Next steps

[Make an on-demand backup](backups-ondemand.md){.md-button}
[Make a scheduled backup](backups-schedule.md){.md-button}
