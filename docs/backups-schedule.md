# Make scheduled backups

Backups schedule is defined on the per-repository basis in the
`backups.pgbackrest.repos` subsection of the `deploy/cr.yaml` file. 

You can supply each repository with a `schedules.<backup type>` key equal to an
actual schedule that you specify in crontab format.

1. Before you start, make sure you have [configured a backup storage](backup-storage.md).

2. Configure backup schedule in the `deploy/cr.yaml` file. The schedule is specified in crontab format as explained in
[Custom Resource options](operator.md#backups-pgbackrest-repos-schedules-full). The repository name must be the same as the one you defined in the [backup storage configuration](backup-storage.md). The following example shows the schedule for `repo1` repository:

   ```yaml
   ...
   backups:
     pgbackrest:
     ...
           repos:
           - name: repo1
             schedules:
               full: "0 0 * * 6"
               differential: "0 1 * * 1-6"
             ...
   ```

3. Update the cluster:

    ``` {.bash data-prompt="$" }
    $ kubectl apply -f deploy/cr.yaml
    ```

