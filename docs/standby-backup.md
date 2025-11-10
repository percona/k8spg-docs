# Standby cluster deployment based on pgBackRest

The pgBackRest repo-based standby is the simplest one. The following is the architecture diagram:

![image](assets/images/dr1.svg)

## pgBackrest repo based standby

1. This solution describes two Kubernetes clusters in different regions, clouds or running in hybrid mode (on-premises and cloud). One cluster is Main and the other is Disaster Recovery (DR)

2. Each cluster includes the following components:

    1. Percona Operator
    2. PostgreSQL cluster
    3. pgBackrest
    4. pgBouncer

3. pgBackrest on the Main site streams backups and Write Ahead Logs (WALs) to the object storage

4. pgBackrest on the DR site takes these backups and streams them to the standby cluster

## Deploy disaster recovery for PostgreSQL on Kubernetes

### Configure Main site

1. Deploy the Operator [using your favorite method](System-Requirements.md#installation-guidelines). Once installed, configure the Custom Resource manifest, so that pgBackrest starts using the Object Storage of your choice. Skip this step if you already have it configured.

2. Configure the `backups.pgbackrest.repos` section by adding the necessary configuration. The below example is for Google Cloud Storage (GCS):

    ```yaml
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

    The `main-pgbackrest-secrets` value contains the keys for GCS. Read more about the configuration in the [backup and restore tutorial](backups.md).

3. Once configured, apply the custom resource:

    ```{.bash data-prompt="$"}
    $ kubectl apply -f deploy/cr.yaml 
    ```

    ??? example "Expected output"

        ```{.bash .no-copy}
        perconapgcluster.pg.percona.com/standby created
        ```

    The backups should appear in the object storage. By default pgBackrest puts them into the pgbackrest folder.


### Configure DR site

The configuration of the disaster recovery site is similar [to that of the Main site](#configure-main-site), with the only difference in standby settings.

The following manifest has `standby.enabled` set to `true` and points to the `repoName` where backups are (GCS in our case):

```yaml
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
```

Deploy the standby cluster by applying the manifest:

```{.bash data-prompt="$"}
$ kubectl apply -f deploy/cr.yaml
```

??? example "Expected output"

    ```{.bash .no-copy}
    perconapgcluster.pg.percona.com/standby created
    ```
