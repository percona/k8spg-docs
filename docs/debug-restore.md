# Troubleshoot restore failures

This page helps you fix failures for both restore methods: an in-place restore with the `backupName` and a cluster clone with the `dataSource` options. Where the steps differ, select the tab for your restore method.

The restore process overwrites database files. Wrong data or a misconfigured restore can leave your cluster in a non-operational state.

For example, incorrect `pgBackRest` arguments in the [PerconaPGRestore custom resource](backups-restore-inplace.md#make-a-full-restore-from-the-latest-backup-default) can break the database while the restore hangs.

Here's what you can do:

* Check the logs of the restore Job to find the cause. The Operator doesn't validate `pgBackRest` options, the stanza or the repository path before it starts the Job. While the Job fails and retries, the `PerconaPGRestore` object stays in the `Running` status. The Job is named `<cluster-name>-pgbackrest-restore`:

    ```bash
    kubectl logs job/cluster1-pgbackrest-restore -n <namespace> -c pgbackrest-restore
    ```

    ??? example "Sample output"

        ```{.text .no-copy}
        + pgbackrest restore --set=20990101-000000F --stanza=db --pg1-path=/pgdata/pg18 --repo=1 --delta --link-map=pg_wal=/pgdata/pg18_wal
        2026-10-12 16:19:48.515 P00  ERROR: [075]: backup set 20990101-000000F is not valid
        ```

    A wrong stanza or repository path, for example in a [cluster clone from cloud storage](backups-clone.md#get-the-backup-settings-from-the-source-cluster), results in `FileMissingError: unable to open missing file '<repo-path>/backup/<stanza>/backup.info'` followed by `ERROR: [075]: no backup set found to restore`. If the repository number in the Secret's credentials differs from the one in `dataSource.pgbackrest.repo.name`, the log shows `ERROR: [037]: restore command requires option: repo1-s3-key`. See [Match the repository number](backups-clone.md#match-the-repository-number). The Operator deletes the Job after a successful restore.

* Stop the failing restore or correct its configuration:

    === "In-place restore"

        Remove the restore annotation from your cluster Custom Resource to stop the restore:

        ```bash
        kubectl annotate -n <namespace> pg cluster1 postgres-operator.crunchydata.com/pgbackrest-restore-
        ```

        The restore writes directly into the cluster's existing data directory. If the logs show that the restore failed after it started to copy files, the data directory can be partially overwritten. In this case, contact [Percona support](https://www.percona.com/services/support) before you start the cluster on that data.

    === "Cluster clone"

        Correct the `dataSource` values in the new cluster's Custom Resource and apply it again. The Operator starts a new restore Job, even if the previous Job reached its retry limit.


* If correcting the configuration doesn't help, recreate the cluster:

    === "In-place restore"

        Don't delete the cluster's PersistentVolumeClaims (PVCs). They hold your database, and it can be the only intact copy of your data.

        If you need to delete the cluster Custom Resource, first check its finalizers:

        ```bash
        kubectl get pg cluster1 -n <namespace> -o jsonpath='{.metadata.finalizers}'
        ```

        Make sure that neither of these finalizers is set:

        * [`finalizers.percona.com/delete-pvc`](operator.md#finalizers-delete-pvc) deletes the cluster's PVCs
        * [`finalizers.percona.com/delete-backups`](operator.md#finalizers-delete-backups) deletes all backups of the cluster from all configured repositories

        If you're unsure how to recover the cluster, contact [Percona support](https://www.percona.com/services/support).

    === "Cluster clone"

        The new cluster holds only the data the failed restore wrote, so you can delete it together with its PVCs and start over. When you recreate the cluster, the Operator reuses the same PVC names. A restore into a PVC that a failed restore already wrote to can fail again, so delete the PVCs too.

        Delete only the resources of the **new** cluster. The source cluster and its backups must stay untouched.

        1. Check the finalizers of the new cluster. Make sure [`finalizers.percona.com/delete-backups`](operator.md#finalizers-delete-backups) isn't set. If the new cluster's backup configuration points to the same repository path as the source cluster, this finalizer deletes the source cluster's backups.

            ```bash
            kubectl get pg cluster2 -n <target-namespace> -o jsonpath='{.metadata.finalizers}'
            ```

        2. [Delete the new cluster's Custom Resource](delete.md#delete-a-database-cluster):

            ```bash
            kubectl delete pg cluster2 -n <target-namespace>
            ```

        3. List the PVCs of the new cluster and check that every name starts with the new cluster's name:

            ```bash
            kubectl get pvc -n <target-namespace> -l postgres-operator.crunchydata.com/cluster=cluster2
            ```

        4. Delete these PVCs:

            ```bash
            kubectl delete pvc -n <target-namespace> -l postgres-operator.crunchydata.com/cluster=cluster2
            ```

        5. Correct the `dataSource` values and apply the Custom Resource again.

* If the logs show that the backup repository is corrupted or files are missing, don't delete any PVCs of the cluster you restore. Its data volumes can hold the only intact copy of your data. Restore from a different backup set or repository, or contact [Percona support](https://www.percona.com/services/support).
