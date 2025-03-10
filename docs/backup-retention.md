# Backup retention

The Operator supports setting pgBackRest retention policies for full and
differential backups. When a full backup expires according to the retention
policy, pgBackRest cleans up all the files related to this backup and to the
write-ahead log. Thus, the expiration of a full backup with some incremental backups
based on it results in expiring of all these incremental backups.

You can control backup retention by the following `pgBackRest` options:

* `--<repo name>-retention-full` number of full backups to retain,
* `--<repo name>-retention-diff` number of differential backups to retain.

You can also specify retention type for full backups as `<repo name>-retention-full-type`,
setting it to either `count` (the number of full backups to keep) or `time`
(the number of days to keep a backup for).

You can set both backup type and retention policy for each of 4 repositories
as follows.

```yaml
backups:
    pgbackrest:
...
      global:
        repo1-retention-full: "14"
        repo1-retention-full-type: time
        ...
```

Differential retention can be set in a similar way:

```yaml
backups:
    pgbackrest:
...
      global:
        repo1-retention-diff: "3"
        ...
```
