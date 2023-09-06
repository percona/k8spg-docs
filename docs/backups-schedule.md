# Make scheduled backups

Backups schedule is defined on the per-repository basis in the
`backups.pgbackrest.repos` subsection of the `deploy/cr.yaml` file. 
You can supply each repository with a `schedules.<backup type>` key equal to an
actual schedule specified in crontab format.

Here is an example of `deploy/cr.yaml` which uses `repo1` repository for backups:

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

The schedule is specified in crontab format as explained in
[Custom Resource options](operator.md#backups-pgbackrest-repos-schedules-full).