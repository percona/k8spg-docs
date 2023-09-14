# Backup retention

The Operator supports setting pgBackRest retention policies for full and
differential backups. When a full backup expires according to the retention
policy, pgBackRest cleans up all the files related to this backup and to the
write-ahead log. Thus, the expiration of a full backup with some incremental backups
based on it results in expiring of all these incremental backups.

You can control backup retention by the following `pgBackRest` options:

* `--<repo name>-retention-full` how much full backups to retain,
* `--<repo name>-retention-diff` how much differential backups to retain.

Backup retention type can be either `count` (the number of backups to keep) or
`time` (the number of days to keep a backup for).

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
