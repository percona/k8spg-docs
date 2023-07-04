# Making on-demand backups

To make an on-demand backup, the user should use a backup configuration file.
The example of the backup configuration file is [deploy/backup.yaml](https://github.com/percona/percona-postgresql-operator/blob/main/deploy/backup.yaml):

```yaml
apiVersion: pg.percona.com/v2beta1
kind: PerconaPGBackup
metadata:
  name: backup1
spec:
  pgCluster: cluster1
  repoName: repo1
#  options:
#  - --type=full
```

Fill it with the proper repository name
to be used for this backup, and any needed 
[pgBackRest command line options](https://pgbackrest.org/configuration.html).

When the backup options are configured, execute the actual backup command:

``` {.bash data-prompt="$" }
$ kubectl apply -f deploy/backup.yaml
```