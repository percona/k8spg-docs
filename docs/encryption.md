# Data-at-rest encryption

!!! admonition

    This feature is in tech preview stage.

Data-at-rest encryption ensures that data stored on disk remains protected even if the underlying storage is compromised. This process is transparent to your applications, meaning you don't need to change your application code. If an unauthorized user gains access to the storage, they can't read the data files.

The Operator supports transparent data encryption (TDE) via the [pg_tde :octicons-link-external-16:](https://docs.percona.com/pg-tde/index.html) extension. When enabled, `pg_tde` encrypts user data in tables, indexes, and temporary tables on disk so that data remains unreadable without the proper encryption keys, even if someone gains access to the storage.

`pg_tde` can also encrypt write-ahead log (WAL) segments stored on disk. To enable WAL encryption, you must explicitly set this option in the Custom Resource. When WAL encryption is enabled, the Operator automatically reconfigures PostgreSQL and pgBackRest to ensure compatibility. `pg_tde` uses the same global principal key that the Operator sets up in Vault. See [WAL encryption](#wal-encryption) to learn more.

This feature is available with Percona Distribution for PostgreSQL 17 and above. 

To store encryption keys, the Operator uses a key management system (KMS). The Operator currently supports HashiCorp Vault as the key value storage engine (KV v2). Support of KMIP and other key providers will be added in future releases.

## How it works

When you enable `pg_tde` and provide Vault configuration, the Operator automates the setup:

1. Adds `pg_tde` to `shared_preload_libraries` so the extension loads at startup.
2. Mounts the Vault token and CA certificate secrets into the database containers at `/pgconf/tde`.
3. Creates the `pg_tde` extension with the `CREATE EXTENSION pg_tde;` command in all databases.
4. Registers Vault as the key provider, creates a global encryption key and sets it as a default key using the functions provided by `pg_tde`.
5. Sets `pg_tde.wal_encrypt` to `off`. 

For restore, the Operator also enables `pg_tde` in the restore job and mounts the Vault secrets so encrypted backups can be restored.

## WAL encryption

WAL encryption protects write-ahead log segments on the database Pod storage. When you set `extensions.pg_tde.walEncryption` to `true`, the Operator:

1. Sets the PostgreSQL parameter `pg_tde.wal_encrypt` to `on`.
2. Wraps the PostgreSQL `archive_command` with `pg_tde_archive_decrypt` so that pgBackRest archives a decrypted copy of each WAL segment.
3. Wraps the PostgreSQL `restore_command` with `pg_tde_restore_encrypt` so that WAL segments fetched from the repository are encrypted again on disk.
4. Adjusts `pgBackRest` settings to ensure compatibility with encrypted WAL (`archive-async=n`, `checksum-page=n`, and `archive-header-check=n`).

!!! important

    Enable WAL encryption only after `pg_tde` is already enabled and the cluster is ready. Do not set `enabled` and `walEncryption` to `true` at the same time on a new cluster. Patroni fails to bootstrap the cluster when WAL encryption is turned on during the initial cluster creation. For the step-by-step procedure, see [Enable WAL encryption](encryption-setup.md#enable-wal-encryption).

### How WAL encryption interacts with backups

`pg_tde` keeps WAL segments encrypted on the Pod disks. The archive command decrypts each segment before upload, and the restore command encrypts it after download. As a result, WAL files in the pgBackRest repository are stored in plaintext unless you also configure [pgBackRest repository encryption](backup-encryption.md) with `repo-cipher-pass`.

Disabling asynchronous WAL archival (`archive-async=n`) can reduce archive throughput compared to clusters without WAL encryption.

After you change the Vault provider or token, create a new backup. Restoring from backups taken before that change fails. See [Key rotation](#key-rotation).

### Considerations for WAL encryption

1. To enable WAL encryption, you must first enable `pg_tde` in the cluster. Wait for the cluster to become ready with `pg_tde` enabled, and only then enable WAL encryption as a separate step. Creating a new cluster with both `enabled` and `walEncryption` set to `true` causes Patroni bootstrap to fail.
2. The safest time to enable WAL encryption is before the cluster has application writes. 
3. WAL segments in the pgBackRest repository are stored in plaintext unless you configure [pgBackRest repository encryption](backup-encryption.md).
4. WAL encryption disables asynchronous WAL archival in pgBackRest, which can reduce archive performance.

## Status and conditions

The Operator tracks the `pg_tde` configuration with a revision hash and exposes state through conditions in `status.conditions`.

To see the `pg_tde` status, run:

```bash
kubectl get pg <cluster-name> -n <namespace> -o yaml
```

### `PGTDEEnabled`

Indicates that the `pg_tde` extension is created in all databases and added to `shared_preload_libraries`. This condition also controls whether instance Pods carry the Vault volume.

The condition can be `True` and the cluster status `Ready` even when there are issues with the token or key provider configuration. The Operator logs those errors. If encryption fails, check the Operator logs and the `PGTDEVaultProviderReady` condition.

### `PGTDEVaultProviderReady`

Reports whether the Vault key provider in PostgreSQL matches the configuration in the Custom Resource. It becomes `False` while a credential change is in progress and stays `False` if the change stalls or fails. Unlike `PGTDEEnabled`, it does not change Pod mounts or `shared_preload_libraries`; it surfaces stalled Vault credential updates.

### Configuration revision

The Operator stores a hash of the Vault configuration in the underlying `PostgresCluster` status field `status.pgTDERevision`. It uses this hash to detect configuration changes and reconfigure `pg_tde`. The field is cleared when you disable `pg_tde`.

## Global key handling

The global key name is derived from the cluster's `metadata.uid` (for example, `global-master-key-ad19534a-d778-460e-ac87-ca38ef5e6755`), so it changes if you delete and recreate the cluster. `pg_tde` handles this like key rotation as long as both old and new keys remain accessible (for example, you deleted and recreated the cluster without removing PVCs).

If you delete a cluster with `pg_tde` enabled but retain the PVCs, or if you disable and later re-enable `pg_tde`, the Operator may log "already exists" errors for the Vault provider or global key. It handles these errors and continues configuration.

With `pg_tde` enabled you can make backups and restores as usual. For restore, the Operator must have access to the encryption key that was used to encrypt the backup data.

## Key rotation 

To rotate the Vault token, create a new Secret containing the updated token and modify the Custom Resource to reference this new Secret.

When you change Vault token, the Operator updates the key provider in two phases:

1. The Operator keeps the old secret mounted in the Pod and stages the new Secret contents in temporary files in `/pgdata` directory. Then it updates the key provider configuration using the  `pg_tde_change_global_key_provider_vault_v2` function.
2. The Operator mounts the new secret, restarts the Pods, runs the provider change again with the standard credential paths, and cleans up temporary files.

During the change, the `PGTDEVaultProviderReady` condition becomes `False`. When the rotation finishes successfully, it returns to `True`.

!!! important

    If WAL encryption is enabled, create a new backup after you change the Vault provider or token. Restoring from backups taken before that change fails.

## Implementation specifics

1. `pg_tde` is available with PostgreSQL 17 and above. 
2. Vault must use a **KV secrets engine v2** for the mount path. The default for `mountPath` is `secret/data`. You can change it to your actual mount (for example, `tde`).
3. You can configure Vault to communicate with the Operator with
and without TLS. The `caSecret` field is optional; omit it only when you intentionally use HTTP. In practice, Vault usually requires TLS.
4. The Operator does not assume anything about the contents of your secrets; you specify the secret names and keys in the Custom Resource. `tokenSecret` and `caSecret` may point to the same Secret or to different ones.
5. You cannot set `extensions.pg_tde.enabled` to `true` without a `vault` section. After `pg_tde` has been enabled, you cannot remove the `pg_tde` or `vault` sections until you first set `enabled` to `false` and wait for Pod restarts.
6. If you are using a [standby cluster](standby.md), you must [configure `pg_tde`](encryption-setup.md) and the key provider on both the source (primary) and the standby clusters. This means you need to enable the extension and set up the key provider in each cluster’s Custom Resource. This configuration is essential for the standby to be able to write and access encrypted data from the source.

   Initially, the Operator uses the key provider configuration from the source cluster to write data on the standby. If the standby cluster is promoted to become the new primary, it will generate its own key provider configuration. The data previously written remains accessible, provided that the proper key provider setup was completed on the standby before promotion. In summary, both the source and standby clusters require correct `pg_tde` and key provider configuration for seamless operation and failover.

7. The Operator does not drop or rewrite encrypted objects for you. Before you disable `pg_tde`, you must remove encrypted objects yourself. See [Disable encryption](encryption-disable.md) to learn more.
8. If you need to migrate from one Vault instance to another and rotate encryption keys at the same time, ensure you transfer all existing keys from the old Vault to the new Vault instance.

## Known limitations

Only HashiCorp Vault is currently supported as a key provider. Other providers and KMIP support are planned for future releases.

## Next steps

[Configure data-at-rest encryption](encryption-setup.md){.md-button}
