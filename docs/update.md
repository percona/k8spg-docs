# Upgrade Percona Operator for PostgreSQL

The upgrade process consists of these steps:

* Upgrade the [Custom Resource Definition (CRD) :octicons-link-external-16:](https://kubernetes.io/docs/concepts/extend-kubernetes/api-extension/custom-resources/) 
* Upgrade the Operator deployment
* Upgrade the database (Percona Distribution for PostgreSQL)

!!! important "Breaking changes for the upgrade to Operator 3.0.0"

    From version **3.0.0**, upstream Crunchy CRDs are renamed and use the API
    group `upstream.pgv2.percona.com` instead of the previous
    `postgres-operator.crunchydata.com` group. This change enables you to
    deploy both Percona and Crunchy Operators in the same Kubernetes cluster
    and provides a way for smooth migration from one to another.
    
    Important points to consider:
    
    * The new CRDs with the API group `upstream.pgv2.percona.com` are created and the Operator migrates all resources to use them automatically. This change affects all PostgreSQL clusters managed by the Operator. 
    * After you upgraded the Operator to version 3.0.0, it can no longer use the previous version CRDs. 
    
    To learn more about this change, see [Upgrading the Operator and CRD](update-operator.md#renamed-upstream-crds-operator-300-and-later).

## Update scenarios

You can either upgrade both the Operator and the database, or you can upgrade only the database. To decide which scenario to choose, read on.

### Full upgrade (CRD, Operator, and the database)

When to use this scenario:

* The new Operator version has changes that are required for new features of the database to work
* The Operator has new features or fixes that enhance automation and management.
* Compatibility improvements between the Operator and the database require synchronized updates.

When going on with this scenario, make sure to test it in a staging or testing environment first. Upgrading the Operator may cause performance degradation.

### Upgrade only the database

When to use this scenario:

* The new version of the database has new features or fixes that are not related to the Operator or other components of your infrastructure
* You have updated the Operator earlier and now want to proceed with the database update.

When choosing this scenario, consider the following:

* Check that the current Operator version supports the new database version.
* Some features may require an Operator upgrade later for full functionality.

## Upgrade from the Operator version 1.x to version 2.x

Upgrades from the Operator version 1.x to 2.x are completely different from the upgrades within 2.x versions due to substantial changes in the architecture.

There are several ways to do such version 1.x to version 2.x upgrade. Choose the method based on your downtime preference and roll back strategy:

|                                                                                                                     | Pros                | Cons        |
| --------------------------------------------------------------------------------------------------------------------| --------------------| ------------|
| [Data Volumes migration](update-data-volumes.md) - re-use the volumes that were created by the Operator version 1.x | The simplest method | - Requires downtime <br> - Impossible to roll back |
| [Backup and restore](update-backup-restore.md) - take the backup with the Operator version 1.x and restore it to the cluster deployed by the Operator version 2.x | Allows you to quickly test version 2.x | Provides significant downtime in case of migration |
| [Replication](update-standby.md) - replicate the data from the Operator version 1.x cluster to the standby cluster deployed by the Operator version 2.x | - Quick test of v2 cluster <br> - Minimal downtime during upgrade | Requires significant computing resources to run two clusters in parallel | 

