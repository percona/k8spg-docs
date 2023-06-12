# Upgrade from the Operator version 1.x to version 2.x

The Operator version 2.x has a lot of differences compared to the version 2.x.
This makes upgrading from version 1.x to version 2.x quite different from a normal upgrade. In fact, you have to migrate the cluster from version 1.x to version 2.x.

There are several ways to do such version 1.x to version 2.x upgrade. Choose the method based on your downtime preference and roll back strategy:

* [Data Volumes migration](update-data-volumes.md) - re-use the volumes that were created by the Operator version 1.x:

  | Pros                | Cons        |
  | --------------------| ------------|
  | The simplest method | - Requires downtime <br> - Impossible to roll back |
   
* [Backup and restore](update-backup-restore.md) - take the backup with the Operator version 1.x and restore it to the cluster deployed by the Operator version 2.x:
   
  | Pros                | Cons        |
  | --------------------| ------------|
  | Allows you to quickly test v2 | Provides significant downtime in case of migration |

* [Replication](update-standby.md) - replicate the data from the Operator version 1.x cluster to the standby cluster deployed by the Operator version 2.x. 

  | Pros               | Cons        |
  | -------------------| ------------|
  | - Quick test of v2 cluster <br> - Minimal downtime during upgrade | Requires significant computing resources to run 2 clusters in parallel | 

|                                                                                                                     | Pros                | Cons        |
| --------------------------------------------------------------------------------------------------------------------| --------------------| ------------|
| [Data Volumes migration](update-data-volumes.md) - re-use the volumes that were created by the Operator version 1.x | The simplest method | - Requires downtime <br> - Impossible to roll back |
| [Backup and restore](update-backup-restore.md) - take the backup with the Operator version 1.x and restore it to the cluster deployed by the Operator version 2.x | Allows you to quickly test version 2.x | Provides significant downtime in case of migration |
| [Replication](update-standby.md) - replicate the data from the Operator version 1.x cluster to the standby cluster deployed by the Operator version 2.x | - Quick test of v2 cluster <br> - Minimal downtime during upgrade | Requires significant computing resources to run two clusters in parallel | 

