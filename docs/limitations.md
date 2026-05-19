# Known limitations

This page describes known limitations of Percona Operator for PostgreSQL. Understanding these constraints helps you plan deployments and avoid unexpected behavior.

## Replica management

* Delayed replicas are not supported
* The Operator doesn't automatically update Patroni configuration inside running instances when  `create_replica_methods` is updated. You must manually run `patronictl reload` on each replica to make Patroni aware of the change. See [Override Patroni configuration](manage-manually.md#override-patroni-configuration) for details.

## Service control

* By default, stopping a PostgreSQL process in the Operator triggers a Pod restart because Kubernetes treats the stopped process as a failed container.

  You can shut down the entire cluster gracefully by [pausing](pause.md) it and resuming it later to restore its operation. The Operator handles this process for you.

  To have a per-pod service control for maintenance, debugging, or controlled downtime requires manual operation. Refer to the [Manual management of database clusters](manage-manually.md) chapter for details how to do it.

* Due to security considerations, superusers cannot connect to PostgreSQL via `pgBouncer` by default. They can either connect via the primary service bypassing `pgBouncer`, or you must adjust `pgBouncer` configuration exposing it to superusers. Read more about it in the [Superusers and pgBouncer](users.md#superuser-and-pgbouncer) section.

## Backups and restores

* PVC snapshots are in tech preview stage. When you use PVC snapshots as scheduled backups, they are not deleted automatically. You must manually delete them. The retention policy for scheduled backups made from PVC snapshots is planned for future releases.
* When you use the `dataSource` option to restore from a backup on a new cluster, you can use either `dataSource.postgresCluster` or `dataSource.pgbackrest`. You cannot use both options. If both are present, `dataSource.postgresCluster` takes precedence. See [Restore the backup to a new cluster](backups-clone.md#understand-the-datasource-options) to learn more.

## Data management

* Tablespace deletion is not automated; you must remove all objects in all databases using the tablespace before dropping it. For details, see [Delete existing tablespaces](tablespaces.md#deleting-an-existing-tablespace).

## Node memory overcommit

[PostgreSQL :octicons-link-external-16:](https://www.postgresql.org/docs/current/kernel-resources.html) recommends strict virtual memory allocation by setting `vm.overcommit_memory=2` to ensure predictable memory accounting and reduce the risk of the OOM killer terminating the postmaster. However, Kubernetes does not allow Pods or Operators to configure this setting. The kubelet treats `vm.overcommit_memory` as an unsafe `sysctl` and rejects attempts to set it to `2`. Most Kubernetes node OS images also default to `1`.

To avoid node-level OOM events, consider tuning PostgreSQL memory parameters  like `shared_buffers`, `work_mem`, `max_connections`, and so on accordingly.

## TLS and cert-manager

**For the Operator upgraded to version 2.9.0**: If you had cert-manager installed and your cluster used the Operator-generated TLS certificates, the Operator switches TLS management to cert-manager. The Operator creates the cert-manager `Issuer` and `Certificate` resources so that the cert-manager can start start issuing and renewing TLS certificates for your cluster.

However, the Operator hasn't verified if the cert-manager owned the root CA certificate. As a result, the CA Secret remained managed by the Operator's internal PKI and the keys inside it (`root.crt` and `root.key`) differ from what the cert-manager expects (`tls.crt` and `tls.key`). This caused the `Issuer` resource to fail and brought the cluster to the inconsistent state: the CA certificate stayed on the internal PKI, while cert-manager attempted to take ownership of the leaf certificates for the cluster, database instances, pgBouncer and pgBackRest. Those leaf certificates then reported the `Not Ready` status because of the failed `Issuer`.

If you are in this situation, you have these options:

* [Switch the cluster to use only the certificates managed by the cert-manager](#switch-to-use-only-the-certificates-managed-by-the-cert-manager).
* Switch the cluster to use custom certificates only. Refer to the [Migrate from cert-manager to custom TLS certificates](tls-migrate-from-cert-manager.md) for the steps.

### Switch to use only the certificates managed by the cert-manager

To restore the cluster from the inconsistent state, reconfigure it to use only the certificates managed by the cert-manager:

1. Delete the CA Secret `<cluster-name>-ca-cert` that still remains on the Operator's internal PKI:
    
    ```bash
    kubectl delete Secret <cluster-name>-ca-cert> -n <namespace>
    ```

    This makes the Operator to recreate the Secret through the cert-manager, with the correct keys.

2. Trigger the cluster reconciliation by deleting the `pgBouncer` Pod:
   
    ```bash
    kubectl delete pod <cluster-name>-pgbouncer-<hash> -n <namespace>
    ```
    
    The Operator detects the missing root CA Secret, creates cert-manager resources for the CA, and lets cert-manager issue new leaf certificates.
   
3. Check the Issuer and Certificate status:
    
    ```bash
    kubectl get issuers -n <namespace>
    kubectl get certificates -n <namespace>
    ```

    Both Issuer and Certificate resources must report the `Ready` status.

In version 3.0.0, the Operator respects the existing TLS configuration, which resolves this limitation.

## Upgrades

* A major database upgrade introduces a downtime because the whole cluster is shut down.
* In clusters with very low write traffic, the first restore after a major upgrade can fail with the `could not find common ancestor of the source and target cluster's timelines` error in `pg_rewind`. In this case you must [reinitialize the replica](reinit.md) to ensure it starts properly and starts streaming data from the primary.
* PostGIS extension is not updated automatically after the database update. You must [manually update](update-extensions.md#upgrade-postgis-extension) it for each database where it is enabled.
* If you have installed [custom PostgreSQL extensions](custom-extensions.md), you need to build and package each custom extension for the new PostgreSQL major version. During the upgrade, the Operator will install extensions into the upgrade container.
