# Upgrade from Operator v1 to v2

There are multiple ways to upgrade from Percona Operator for PostgreSQL version
1 to version 2. This upgrade, however, is different from a regular upgrade within the same major version.

## Upgrade methods

Choose the method based on your downtime preference and roll back strategy:

* [Data Volumes migration](update-data-volumes.md) - re-use the volumes that were created by Operator v1.

  | Pros               | Cons        |
  | -------------------| ------------|
  | The simplest method| - Requires downtime <br> - Impossible to roll back|
   
* [Backup and restore](update-backup-restore.md) - take the backup that was taken by Operator v1 and restore to the cluster deployed by Operator v2. 
   
  | Pros               | Cons        |
  | -------------------| ------------|
  | Allows you to quickly test v2 | Provides significant downtime in case of migration| 

* [Replication](update-standby.md) - you replicate the data from v1 to the standby cluster deployed by Operator v2. 

  | Pros               | Cons        |
  | -------------------| ------------|
  | - Quick test of v2 cluster <br> - Minimal downtime during upgrade | Requires significant computing resources to run 2 clusters in parallel.| 

