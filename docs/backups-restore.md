# Restore options: in-place restore vs cluster clone

You can restore your PostgreSQL data from a backup in these ways:

* [**In-place restore**](backups-restore-inplace.md) – restore data into the same cluster using the [PerconaPGRestore](restore-options.md) custom resource. By default, the Operator restores the most recent backup. You can specify what backup to restore from using the `--set` option. 
* [**Cluster clone**](backups-clone.md) – create a new cluster from a backup using the `dataSource` option in the Custom Resource of a **new** cluster. Use this approach to deploy a copy of your cluster in a new namespace or a different Kubernetes cluster to:

    - Test your disaster recovery strategy
    - Analyze the data without affecting the production cluster
    - Restore the database from a cloud storage when the source cluster no longer exists.

Both approaches support full restore and point-in-time recovery. Choose the method that fits your scenario.

## Next steps

* [In-place restore](backups-restore-inplace.md) – restore to the same cluster
* [Cluster clone](backups-clone.md) – restore to a new cluster
* [Restore options reference](restore-options.md) – PerconaPGRestore spec