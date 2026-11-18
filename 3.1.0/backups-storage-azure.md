> For the complete documentation index, see [llms.txt](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/llms.txt).

# Microsoft Azure Blob Storage

Azure Blob Storage support is currently in tech preview.

To use [Microsoft Azure Blob Storage](https://azure.microsoft.com/en-us/services/storage/blobs/) for backups, you need the following:

- Azure container name
- Azure Storage account name and key, stored in a [Kubernetes Secret](https://kubernetes.io/docs/concepts/configuration/secret/)

## Configuration steps

The examples below use the `repo4` repository name.

1. Encode the Azure Storage credentials and the pgBackRest repo name that you will use for backups with base64:

   **Linux**

   ```
   cat <<EOF | base64 --wrap=0
   [global]
   repo4-azure-account=<AZURE_STORAGE_ACCOUNT_NAME>
   repo4-azure-key=<AZURE_STORAGE_ACCOUNT_KEY>
   EOF
   ```

   **macOS**

   ```
   cat <<EOF | base64
   [global]
   repo4-azure-account=<AZURE_STORAGE_ACCOUNT_NAME>
   repo4-azure-key=<AZURE_STORAGE_ACCOUNT_KEY>
   EOF
   ```

1. Create the Secret manifest and set `data.azure.conf` to the encoded string. The following is the example of the cluster1-pgbackrest-secrets.yaml Secret file:

   ```
   apiVersion: v1
   kind: Secret
   metadata:
     name: cluster1-pgbackrest-secrets
   type: Opaque
   data:
     azure.conf: <base64-encoded-configuration-contents>
   ```

   You can store credentials for several repositories in one Secret by adding separate data keys.

1. Create the Secrets object from this yaml file. Replace `<namespace>` with your namespace:

   ```
   kubectl apply -f cluster1-pgbackrest-secrets.yaml -n <namespace>
   ```

1. Update the `deploy/cr.yaml` Custom Resource:

   - Reference the Secret in `backups.pgbackrest.configuration`
   - Provide the backup directory path in [backups.pgbackrest.global](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/operator.html#backupspgbackrestglobal) with the pgBackRest `path` option (for example `repo4-path`). The repository name must match the name used when encoding credentials
   - Specify the Azure container name under `repos`

   ```
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

1. Apply the cluster Custom Resource:

   ```
   kubectl apply -f deploy/cr.yaml -n <namespace>
   ```

## Next steps

[Make an on-demand backup](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/backups-ondemand.html) [Make a scheduled backup](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/backups-schedule.html)
