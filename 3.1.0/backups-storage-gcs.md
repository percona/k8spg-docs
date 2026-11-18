> For the complete documentation index, see [llms.txt](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/llms.txt).

# Google Cloud Storage

To use [Google Cloud Storage (GCS)](https://cloud.google.com/storage) for backups, configure a pgBackRest repository in `backups.pgbackrest.repos` and provide:

- A GCS bucket name which you will reference in the `gcs.bucket` option under the repository entry
- A Google service account key, which the Operator will use to access the storage.

## Configuration steps

The following example configuration uses the `repo3` repository name.

1. Create a service account key following the [Google Cloud instructions](https://cloud.google.com/iam/docs/creating-managing-service-account-keys) .

1. Download the key from the Google Cloud console (*IAM & Admin* → *Service Accounts* → your account → *KEYS* → *ADD KEY* → *Create new key* → *JSON*). The downloaded file is typically named `gcs-key.json`.

1. Prepare the Secret data:

   - Create `gcs.conf` for repository `repo3`:

     ```
     [global]
     repo3-gcs-key=/etc/pgbackrest/conf.d/gcs-key.json
     ```

   - Encode both `gcs-key.json` and `gcs.conf` files using base64:

     **Linux**

     ```
     base64 --wrap=0 <filename>
     ```

     **macOS**

     ```
     base64 -i <filename>
     ```

   - Create the Secret manifest. For example, `cluster1-pgbackrest-secrets.yaml`:

     ```
     apiVersion: v1
     kind: Secret
     metadata:
       name: cluster1-pgbackrest-secrets
     type: Opaque
     data:
       gcs-key.json: <base64-encoded-json-file-contents>
       gcs.conf: <base64-encoded-conf-file-contents>
     ```

     You can store credentials for several repositories in one Secret by adding separate data keys.

1. Apply the Secret. Replace `<namespace>` with your namespace:

   ```
   kubectl apply -f cluster1-pgbackrest-secrets.yaml -n <namespace>
   ```

1. Update `deploy/cr.yaml` Custom Resource manifest:

   - Reference the Secret in `backups.pgbackrest.configuration`
   - Provide the backup path in [backups.pgbackrest.global](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/operator.html#backupspgbackrestglobal) with the pgBackRest `path` option. The repository name must match the name in `gcs.conf` (`repo3-path` in this example)
   - Define the GCS bucket under `repos`.

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
         repo3-path: /pgbackrest/postgres-operator/cluster1/repo3
       ...
       repos:
       - name: repo3
         gcs:
           bucket: "<YOUR_GCS_BUCKET_NAME>"
   ```

1. Apply the cluster Custom Resource. Replace the `<namespace>` placeholder with your value:

   ```
   kubectl apply -f deploy/cr.yaml -n <namespace>
   ```

## Next steps

[Make an on-demand backup](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/backups-ondemand.html) [Make a scheduled backup](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/backups-schedule.html)
