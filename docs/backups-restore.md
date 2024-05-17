# Restore the cluster from a previously saved backup

The Operator supports the ability to perform a full restore on a PostgreSQL
cluster as well as a point-in-time-recovery. There are two ways to
restore a cluster:

* restore to a new cluster using the [dataSource.postgresCluster](operator.md#datasource-postgrescluster-clustername)
subsection,
* restore in-place to an existing cluster (note that this is destructive) using
the [backups.restore](operator.md#backups-restore-enabled) subsection.

## Restore to a new PostgreSQL cluster

Restoring to a new PostgreSQL cluster allows you to take a backup and create a
new PostgreSQL cluster that can run alongside an existing one. There are several
scenarios where using this technique is helpful:

* Creating a copy of a PostgreSQL cluster that can be used for other purposes.
    Another way of putting this is *creating a clone*.
* Restore to a point-in-time and inspect the state of the data without affecting
    the current cluster.

To create a new PostgreSQL cluster from either the active one, or a former cluster
whose pgBackRest repository still exists, use the [dataSource.postgresCluster](operator.md#datasource-postgrescluster-clustername) subsection options. The content of this subsection
should copy the `backups` keys of the original cluster - ones needed to carry on
the restore:

* `dataSource.postgresCluster.clusterName` should contain the new cluster name,
* `dataSource.postgresCluster.options` allow you to set the needed pgBackRest
    command line options,
* `dataSource.postgresCluster.repoName` should contain the name of the
    pgBackRest repository, while the actual storage configuration keys for this
    repository should be placed into `dataSource.pgbackrest.repo` subsection,
* `dataSource.pgbackrest.configuration.secret.name` should contain the name of
    a Kubernetes Secret with credentials needed to access cloud storage, if any.
    
## Restore to an existing PostgreSQL cluster

To restore the previously saved backup, use a *backup restore*
configuration file. The example of the backup configuration file is
[deploy/restore.yaml :octicons-link-external-16:](https://github.com/percona/percona-postgresql-operator/blob/main/deploy/restore.yaml):

```yaml
apiVersion: pgv2.percona.com/v2
kind: PerconaPGRestore
metadata:
  name: restore1
spec:
  pgCluster: cluster1
  repoName: repo1
  options:
  - --type=time
  - --target="2022-11-30 15:12:11+03"
```

The following keys are the most important ones:

* `pgCluster` specifies the name of your cluster,
* `repoName` specifies the name of one of the 4 pgBackRest repositories,
    already configured in the `backups.pgbackrest.repos` subsection,
* `options` passes through any [pgBackRest command line options :octicons-link-external-16:](https://pgbackrest.org/configuration.html).

To start the restoration process, run the following command:

``` {.bash data-prompt="$" }
$ kubectl apply -f deploy/restore.yaml
```

## Restore the cluster with point-in-time recovery

Point-in-time recovery functionality allows users to revert the database back to
a state before an unwanted change had occurred.

!!! note

    For this feature to work, the Operator initiates a full backup 
    immediately after the cluster creation, to use it as a basis for
    point-in-time recovery when needed (this backup is not listed in the output
    of the `kubectl get pg-backup` command).

You can set up a point-in-time recovery using the normal restore command of
pgBackRest with few additional `spec.options` fields in `deploy/restore.yaml`:

* set `--type` option to `time`,
* set `--target` to a specific time you would like to restore to. You can use
    the typical string formatted as `<YYYY-MM-DD HH:MM:DD>`, optionally followed
    by a timezone offset: `"2021-04-16 15:13:32+00"` (`+00` in the above
    example means UTC),
* optional `--set` argument followed with a pgBackRest backup ID allows you to
    choose the backup which will be the starting point for point-in-time
    recovery. This option must be specified if the target is one or more backups
    away from the current moment. You can look through the available backups with the 
    [pgBackRest info :octicons-link-external-16:](https://pgbackrest.org/command.html#command-info)
    command to find out the proper backup ID.

    ??? example "pgBackRest backup ID example"

        After obtaining the Pod name with `kubectl get pods` command, you can
        run `pgbackrest --stanza=db info` command on the appropriate Pod as
        follows:

        ``` {.bash data-prompt="$" }
        $ kubectl -n pgo exec -it cluster1-instance1-hcgr-0 -c database -- pgbackrest --stanza=db info
        ```
        
        Then find ID of the needed backup in the output:
        
        ```{.text .no-copy hl_lines="8"}
        stanza: db
            status: ok
            cipher: none
        
            db (prior)
                wal archive min/max (16): 0000000F000000000000001C/0000002000000036000000C5
        
                full backup: 20240401-173403F
                    timestamp start/stop: 2024-04-01 17:34:03+00 / 2024-04-01 17:36:57+00
                    wal start/stop: 000000120000000000000022 / 000000120000000000000024
                    database size: 31MB, database backup size: 31MB
                    repo1: backup set size: 4.1MB, backup size: 4.1MB
        
                incr backup: 20240401-173403F_20240415-201250I
                    timestamp start/stop: 2024-04-15 20:12:50+00 / 2024-04-15 20:14:19+00
                    wal start/stop: 00000019000000000000005C / 00000019000000000000005D
                    database size: 46.0MB, database backup size: 25.7MB
                    repo1: backup set size: 6.1MB, backup size: 3.8MB
                    backup reference list: 20240401-173403F

                incr backup: 20240401-173403F_20240415-201430I
        ...
        ```
        
        Now you can put this backup ID to the *backup restore* configuration
        file as follows:

        ```yaml hl_lines="9"
        apiVersion: pgv2.percona.com/v2
        kind: PerconaPGRestore
        metadata:
          name: restore1
        spec:
          pgCluster: cluster1
          repoName: repo1
          options:
          - --set="20240401-173403F"
        ```

After setting these options in the *backup restore* configuration file,
follow the standard restore instructions.

!!! note

    Make sure you have a backup that is older than your desired point in time.
    You obviously can’t restore from a time where you do not have a backup.
    All relevant write-ahead log files must be successfully pushed before you
    make the restore.

