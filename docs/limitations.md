# Known limitations

This page describes known limitations of Percona Operator for PostgreSQL. Understanding these constraints helps you plan deployments and avoid unexpected behavior.

## Replica management

* With the Operator, you can scale your cluster up and down by changing the number of replicas. But you cannot control the order in which the Operator adds, removes or stops replicas, because the Operator manages replicas as a pool rather than as individually addressable instances. 
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

## Upgrades

* A major database upgrade introduces a downtime because the whole cluster is shut down.
* In clusters with very low write traffic, the first restore after a major upgrade can fail with the `could not find common ancestor of the source and target cluster's timelines` error in `pg_rewind`. In this case you must [reinitialize the replica](reinit.md) to ensure it starts properly and starts streaming data from the primary.
* PostGIS extension is not updated automatically after the database update. You must [manually update](update-extensions.md#upgrade-postgis-extension) it for each database where it is enabled. 
* If you have installed [custom PostgreSQL extensions](custom-extensions.md), you need to build and package each custom extension for the new PostgreSQL major version. During the upgrade, the Operator will install extensions into the upgrade container.

