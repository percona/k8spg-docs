# Delete the unneeded backup

The maximum amount of stored backups is controlled by the [retention policies](backup-retention.md).
Older backups are automatically deleted. 

Manual deleting of a previously saved backup requires not more than the backup
name. This name can be taken from the list of available backups returned
by the following command:

``` {.bash data-prompt="$" }
$ kubectl get pg-backup
```

When the name is known, backup can be deleted as follows:

``` {.bash data-prompt="$" }
$ kubectl delete pg-backup/<backup-name>
```

## Delete backups on cluster deletion

You can enable [`percona.com/delete-backups` finalizer](operator.md#finalizers-delete-backups) in the Custom Resource (turned off by default) to ensure that all backups are removed when the cluster is deleted.
If the finalizer is enabled, the Operator will delete all the backups from all the configured repos on cluster deletion. Besides removing all the physical backup files, finalizer will also delete all `pg-backup` objects.

warning !!!

    This `percona.com/delete-backups` finalizer is in tech preview state, and it is not yet recommended for production environments.
