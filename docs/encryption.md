# Data-at-rest encryption

!!! admonition

    This feature is in tech preview stage.

Data-at-rest encryption ensures that data stored on disk remains protected even if the underlying storage is compromised. This process is transparent to your applications, meaning you don't need to change your application code. If an unauthorized user gains access to the storage, they can't read the data files.

The Operator supports transparent data encryption (TDE) via the [pg_tde :octicons-link-external-16:](https://docs.percona.com/pg-tde/index.html) extension. When enabled, `pg_tde` encrypts user data in tables, indexes, and temporary tables on disk so that data remains unreadable without the proper encryption keys, even if someone gains access to the storage.

This feature is available with Percona Distribution for PostgreSQL 17 and above. 

To store encryption keys, the Operator uses a key management system (KMS). The Operator currently supports HashiCorp Vault as the key value storage engine (KV v2). Support of KMIP and other key providers will be added in future releases. WAL encryption is not yet supported.

## How it works

When you enable `pg_tde` and provide Vault configuration, the Operator automates the setup:

1. Adds `pg_tde` to `shared_preload_libraries` so the extension loads at startup.
2. Mounts the Vault token and CA certificate secrets into the database containers.
3. Creates the `pg_tde` extension with the `CREATE EXTENSION pg_tde;` command in all databases.
4. Registers Vault as the key provider, creates a global encryption key and sets it as a default key using the functions provided by `pg_tde`.

## Status and conditions

The Operator tracks the `pg_tde` configuration via a hash and exposes its state through a `PGTDEEnabled` condition in `status.conditions`. The Operator uses the hash to detect changes and reconfigure the `pg_tde` when needed.

To see the `pg_tde` configuration status, run: 

```bash
kubectl get pg <cluster-name> -n <namespace> -o yaml
```

Look for the condition with `type: PGTDEEnabled` under `status.conditions`.

The `PGTDEEnabled` condition indicates that the `pg_tde` extension is created in all databases and added to `shared_preload_libraries`. Note that the condition can be `True` and the cluster status `Ready` even when there are issues with token or key provider configuration. However, the Operator logs these errors and if you encounter issues with encryption, check the Operator logs for details.

## Global key handling

The global key name is determined by the cluster's `metadata.uid`, so it changes if you delete and recreate the cluster. `pg_tde` handles this like key rotation as long as both old and new keys remain accessible (for example, you deleted and recreated the cluster without removing PVCs).

With `pg_tde` enabled you can make backups and restores as usual. For restore, the Operator must have access to the encryption key that was used to encrypt the backup data.

## Implementation specifics

1. `pg_tde` is available with PostgreSQL 17 and above.
2. Vault must use a **KV secrets engine v2** for the mount path.
3. You can configure Vault to communicate with the Operator with and without TLS.
4. The Operator does not assume anything about the contents of your secrets; you specify the secret names and keys in the Custom Resource.
5. If you are using a [standby cluster](standby.md), you must [configure `pg_tde`](encryption-setup.md) and the key provider on both the source (primary) and the standby clusters. This means you need to enable the extension and set up the key provider in each cluster’s Custom Resource. This configuration is essential for the standby to be able to write and access encrypted data from the source.

   Initially, the Operator uses the key provider configuration from the source cluster to write data on the standby. If the standby cluster is promoted to become the new primary, it will generate its own key provider configuration. The data previously written remains accessible, provided that the proper key provider setup was completed on the standby before promotion. In summary, both the source and standby clusters require correct `pg_tde` and key provider configuration for seamless operation and failover.

## Known limitations

1. WAL encryption is not yet supported. It will be added in future releases.
2. Only HashiCorp Vault key provider is currently supported. Other providers and the support of KMIP protocol are planned to be added in future releases.

## Next steps

[Configure data-at-rest encryption](encryption-setup.md){.md-button}
