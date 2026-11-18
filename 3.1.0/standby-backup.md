> For the complete documentation index, see [llms.txt](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/llms.txt).

# Standby cluster deployment based on pgBackRest

The pgBackRest repo-based standby is the simplest one. The following is the architecture diagram:

## pgBackrest repo based standby

1. This solution describes two Kubernetes clusters in different regions, clouds or running in hybrid mode (on-premises and cloud). One cluster is Main and the other is Disaster Recovery (DR)

1. Each cluster includes the following components:

   1. Percona Operator
   1. PostgreSQL cluster
   1. pgBackrest
   1. pgBouncer

1. pgBackrest on the Main site streams backups and Write Ahead Logs (WALs) to the object storage

1. pgBackrest on the DR site takes these backups and streams them to the standby cluster

## Deploy disaster recovery for PostgreSQL on Kubernetes

### Configure Main site

1. Deploy the Operator [using your favorite method](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/System-Requirements.html#installation-guidelines). Once installed, configure the Custom Resource manifest, so that pgBackrest starts using the Object Storage of your choice. Skip this step if you already have it configured.

1. Configure the `backups.pgbackrest.repos` section by adding the necessary configuration. The below example is for Google Cloud Storage (GCS):

   ```
   spec:
     backups:
       configuration:
         - secret:
             name: main-pgbackrest-secrets
       pgbackrest:
         repos:
         - name: repo1
           gcs:
             bucket: MY-BUCKET
   ```

   The `main-pgbackrest-secrets` value contains the keys for GCS. Read more about the configuration in the [backup and restore tutorial](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/backups.html).

1. Once configured, apply the custom resource:

   ```
   kubectl apply -f deploy/cr.yaml
   ```

   Expected output

   ```
   perconapgcluster.pg.percona.com/standby created
   ```

   The backups should appear in the object storage. By default pgBackrest puts them into the pgbackrest folder.

### Configure DR site

The configuration of the disaster recovery site is similar [to that of the Main site](#configure-main-site), with the difference in standby settings.

The following manifest has `standby.enabled` set to `true` and points to the `repoName` where backups are (GCS in our case). Optionally, add `standby.maxAcceptableLag` to enable [replication lag detection](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/standby.html#detect-replication-lag-for-standby-cluster). Check the [known limitation for this standby type](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/standby.html#known-limitation-for-a-repo-based-standby-cluster) and [choose the threshold](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/standby.html#choose-the-lag-threshold) accordingly.

```
metadata:
  name: standby
spec: 
...
  backups:
    configuration:
      - secret:
          name: standby-pgbackrest-secrets
    pgbackrest:
      repos:
      - name: repo1
        gcs:
          bucket: MY-BUCKET
  standby:
    enabled: true
    repoName: repo1
    # maxAcceptableLag: 64Mi  # optional: enables replication lag detection
```

Deploy the standby cluster by applying the manifest:

```
kubectl apply -f deploy/cr.yaml
```

Expected output

```
perconapgcluster.pg.percona.com/standby created
```

### Copy the user and pgBouncer passwords

After you deploy the standby, copy the user passwords and the pgBouncer password from the Main site to the DR site, so that applications and pgBouncer can log in after you promote the DR cluster. Follow [Prepare the user passwords](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/standby-failover.html#prepare-the-user-passwords).
