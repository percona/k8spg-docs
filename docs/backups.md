# Providing Backups

The Operator allows doing backups in two ways.
*Scheduled backups* are configured in the
[deploy/cr.yaml](https://github.com/percona/percona-postgresql-operator/blob/main/deploy/cr.yaml)
file to be executed automatically in proper time. *On-demand backups*
can be done manually at any moment.

The Operator uses the open source [pgBackRest](https://pgbackrest.org/) backup
and restore utility.

### Backup repositories

A special *pgBackRest repository* is created by the Operator along with
creating a new PostgreSQL cluster to facilitate the usage of the pgBackRest
features in it (you can notice additional `repo-host` Pod after the cluster
creation).

The Operator can use the following variants of cloud storage outside the
Kubernetes cluster to keep PostgreSQL backups:

* Amazon S3, or [any S3-compatible storage](https://en.wikipedia.org/wiki/Amazon_S3#S3_API_and_competing_services),
* [Google Cloud Storage](https://cloud.google.com/storage), 
* [Azure Blob Storage](https://azure.microsoft.com/en-us/services/storage/blobs/)

It is also possible to store backups in Kubernetes, just on a [Persistent Volume](https://kubernetes.io/docs/concepts/storage/persistent-volumes/) attached to the pgBackRest Pod.

Each pgBackRest repository consists of the following Kubernetes objects:

* A Deployment,
* A Secret that contains information that is specific to the PostgreSQL cluster
    (e.g. SSH keys, AWS S3 keys, etc.),
* A Pod with a number of supporting scripts,
* A Service.

You can have up to 4 pgBackRest repositories named as `repo1`, `repo2`, `repo3`,
and `repo4`.

## Backup types

The PostgreSQL Operator supports three types of pgBackRest backups:

* `full`: A full backup of all the contents of the PostgreSQL cluster,
* `differential`: A backup of only the files that have changed since
the last full backup,
* `incremental`: A backup of only the files that have changed since the
last full or differential backup. Incremental backup is the default choice.

## Backup retention

The Operator also supports setting pgBackRest retention policies for full and
differential backups. When a full backup expires according to the retention
policy, pgBackRest cleans up all the files related to this backup and to
write-ahead log. So, expiring of a full backup with some incremental backups
based on it results in expiring all these incremental backups.

Backup retention can be controlled by the following pgBackRest options:

* `--<repo name>-retention-full` how much full backups to retain,
* `--<repo name>-retention-diff` how much differential backups to retain.

Backup retention type can be either `count` (the number of backups to keep) or
`time` (the number of days a backup should be kept for).

You can set both backups type and retention policy for each of 4 repositories
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

## Backup storage

You should configure backup storage for your repositories in the
`backups.pgbackrest.repos` section of the `deploy/cr.yaml` configuration file.

### Configuring the S3-compatible backup storage

In order to use S3-compatible storage for backups you need to provide some
S3-related information, such as proper S3 bucket name, endpoint, etc. This
information can be passed to pgBackRest via the following `deploy/cr.yaml`
options in the `backups.pgbackrest.repos` subsection:

* `bucket` specifies the AWS S3 bucket that should be utilized,
for example `my-postgresql-backups-example`,
* `endpoint` specifies the S3 endpoint that should be utilized,
for example `s3.amazonaws.com`,
* `region` specifies the AWS S3 region that should be utilized,
for example `us-east-1`.

You also need to supply pgBackRest with base64-encoded AWS S3 key and AWS S3 key
secret stored along with other sensitive information in [Kubernetes Secrets](https://kubernetes.io/docs/concepts/configuration/secret/).

1. Put your AWS S3 key and AWS S3 key secret into the base64-encoded pgBackRest
    configuration with your pgBackRest repository name. In case of the `repo1`
    repository it can be done as follows:

    === "in Linux"

        ``` {.bash data-prompt="$" }
        $ cat <<EOF | base64 --wrap=0
        [global]
        repo1-s3-key=<YOUR_AWS_S3_KEY>
        repo1-s3-key-secret=<YOUR_AWS_S3_KEY_SECRET>
        EOF
        ```

    === "in macOS"

        ``` {.bash data-prompt="$" }
        $ cat <<EOF | base64
        [global]
        repo1-s3-key=<YOUR_AWS_S3_KEY>
        repo1-s3-key-secret=<YOUR_AWS_S3_KEY_SECRET>
        EOF
        ```

2. Create the Secret configuration file with the resulted base64-encoded string
    as the following `cluster1-pgbackrest-secrets.yaml` example:

    ```yaml
    apiVersion: v1
    kind: Secret
    metadata:
      name: cluster1-pgbackrest-secrets
    type: Opaque
    data:
      s3.conf: <base64-encoded-configuration-contents>
    ```

    !!! note

        This Secret can store credentials for several repositories presented as
        separate data keys.

    When done, create the Secrets object from this yaml file:

    ``` {.bash data-prompt="$" }
    $ kubectl apply -f cluster1-pgbackrest-secrets.yaml
    ```

3. Update your `deploy/cr.yaml` configuration with the S3 credentials
    Secret in the `backups.pgbackrest.configuration` subsection, and put all
    other S3 related information into the options of one of your repositories
    in the `backups.pgbackrest.repos` subsection. For example, the S3 storage
    for the `repo1` repository would look as follows.

    ```yaml
    ...
    backups:
      pgbackrest:
        ...
        configuration:
          - secret:
              name: cluster1-pgbackrest-secrets
        ...
        repos:
        - name: repo1
          s3:
            bucket: "<YOUR_AWS_S3_BUCKET_NAME>"
            endpoint: "<YOUR_AWS_S3_ENDPOINT>"
            region: "<YOUR_AWS_S3_REGION>"
    ```

4. Finally, create or update the cluster:

    ``` {.bash data-prompt="$" }
    $ kubectl apply -f deploy/cr.yaml
    ```

### Configuring Google Cloud Storage for backups

You can configure [Google Cloud Storage](https://cloud.google.com/storage) as
an object store for backups similarly to S3 storage.

In order to use Google Cloud Storage (GCS) for backups you need to provide a
proper GCS bucket name. Bucket name can be passed to `pgBackRest` via the
`gcs.bucket` key in the `backups.pgbackrest.repos` subsection of
`deploy/cr.yaml`.

The Operator will also need your service account key to access storage.

1. Create your service account key following the [official Google Cloud instructions](https://cloud.google.com/iam/docs/creating-managing-service-account-keys).
2. Export this key from your Google Cloud account.

    You can find your key in the Google Cloud console (select *IAM & Admin*
    → *Service Accounts* in the left menu panel, then click your account and
    open the *KEYS* tab):

    ![image](assets/images/gcs-service-account.svg)

    Click the *ADD KEY* button, chose *Create new key* and chose *JSON* as a key
    type. These actions will result in downloading a file in JSON format with
    your new private key and related information.

3. Now you should create the [Kubernetes Secret](https://kubernetes.io/docs/concepts/configuration/secret/)
    using base64-encoded versions of two files: the file containing the
    private key you have just downloaded, and the special `gcs.conf` configuration file.

    The content of the `gcs.conf` file depends on the repository
    name. In case of the `repo1` repository, it looks as follows:

    ```
    [global]
    repo1-gcs-key=/etc/pgbackrest/conf.d/gcs-key.json
    ```

    You can encode a text file with the `base64 --wrap=0 <filename>`
    command (or just `base64 <filename>` in case of Apple macOS).
    When done, create the following yaml file with your cluster name
    and base64-encoded files contents as the following
    `cluster1-pgbackrest-secrets.yaml` example:

    ```yaml
    apiVersion: v1
    kind: Secret
    metadata:
      name: cluster1-pgbackrest-secrets
    type: Opaque
    data:
      gcs-key.json: <base64-encoded-json-file-contents>
      gcs.conf: <base64-encoded-conf-file-contents>
    ```

    !!! note

        This Secret can store credentials for several repositories presented as
        separate data keys.

    Create the Secrets object from this YAML file:

    ``` {.bash data-prompt="$" }
    $ kubectl apply -f cluster1-pgbackrest-secrets.yaml
    ```

4. Update your `deploy/cr.yaml` configuration with your GCS credentials
    Secret in the `backups.pgbackrest.configuration` subsection, and put GCS
    bucket name into the `bucket` option of one of your repositories
    in the `backups.pgbackrest.repos` subsection. For example, GCS storage
    for the `repo3` repository would look as follows.

    ```yaml
    ...
    backups:
      pgbackrest:
        ...
        configuration:
          - secret:
              name: cluster1-pgbackrest-secrets
        ...
        repos:
        - name: repo3
          gcs:
            bucket: "<YOUR_GCS_BUCKET_NAME>"
    ```

5. Finally, create or update the cluster:

    ``` {.bash data-prompt="$" }
    $ kubectl apply -f deploy/cr.yaml
    ```

### Configuring Azure Blob Storage for backups (tech preview)

In order to use [Microsoft Azure Blob Storage](https://azure.microsoft.com/en-us/services/storage/blobs/) for backups you need to provide a proper Azure container name. It can be passed to
`pgBackRest` via the `azure.container` key in the `backups.pgbackrest.repos`
subsection of `deploy/cr.yaml`.

The Operator will also need a [Kubernetes Secret](https://kubernetes.io/docs/concepts/configuration/secret/)
with your Azure Storage credentials to access the storage.

1. Put your Azure storage account name and key into the base64-encoded pgBackRest
    configuration with your pgBackRest repository name. In case of the `repo1`
    repository it can be done as follows:

    === "in Linux"

        ``` {.bash data-prompt="$" }
        $ cat <<EOF | base64 --wrap=0
        [global]
        repo1-azure-account=<AZURE_STORAGE_ACCOUNT_NAME>
        repo1-azure-key=<AZURE_STORAGE_ACCOUNT_KEY>
        EOF
        ```

    === "in macOS"

        ``` {.bash data-prompt="$" }
        $ cat <<EOF | base64
        [global]
        repo1-azure-account=<AZURE_STORAGE_ACCOUNT_NAME>
        repo1-azure-key=<AZURE_STORAGE_ACCOUNT_KEY>
        EOF
        ```

2. Create the Secret configuration file with the resulted base64-encoded string
    as the following `cluster1-pgbackrest-secrets.yaml` example:

    ```yaml
    apiVersion: v1
    kind: Secret
    metadata:
      name: cluster1-pgbackrest-secrets
    type: Opaque
    data:
      azure.conf: <base64-encoded-configuration-contents>
    ```

    !!! note

        This Secret can store credentials for several repositories presented as
        separate data keys.

    When done, create the Secrets object from this yaml file:

    ``` {.bash data-prompt="$" }
    $ kubectl apply -f cluster1-pgbackrest-secrets.yaml
    ```

3. Update your `deploy/cr.yaml` configuration with the Azure Storage credentials
    Secret in the `backups.pgbackrest.configuration` subsection, and put Azure
    container name into the options of one of your repositories
    in the `backups.pgbackrest.repos` subsection. For example, the Azure storage
    for the `repo1` repository would look as follows.

    ```yaml
    ...
    backups:
      pgbackrest:
        ...
        configuration:
          - secret:
              name: cluster1-pgbackrest-secrets
        ...
        repos:
        - name: repo1
          azure:
            container: "<YOUR_AZURE_CONTAINER>"
    ```

4. Finally, create or update the cluster:

    ``` {.bash data-prompt="$" }
    $ kubectl apply -f deploy/cr.yaml
    ```

## Scheduling backups

Backups schedule is defined on per-repository basis in the
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

## Making on-demand backup

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

## Restore the cluster from a previously saved backup

The Operator supports the ability to perform a full restore on a PostgreSQL
cluster as well as a point-in-time-recovery. There are two types of ways to
restore a cluster:

* restore to a new cluster using the [dataSource.postgresCluster](operator.md#datasource-postgrescluster-clustername)
subsection,
* restore in-place, to an existing cluster (note that this is destructive) using
the [backups.restore](operator.md#backups-restore-enabled) subsection.

### Restore to an existing PostgreSQL cluster

To restore the previously saved backup the user should use a *backup restore*
configuration file. The example of the backup configuration file is
[deploy/restore.yaml](https://github.com/percona/percona-postgresql-operator/blob/main/deploy/restore.yaml):

```yaml
apiVersion: pg.percona.com/v2beta1
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
* `options` passes through any [pgBackRest command line options](https://pgbackrest.org/configuration.html).

The actual restoration process can be started as follows:

``` {.bash data-prompt="$" }
$ kubectl apply -f deploy/restore.yaml
```

### Restore the cluster with point-in-time recovery

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
example means just UTC),
* optional `--set` argument allows you to choose the backup which will be the
starting point for point-in-time recovery (look through the available backups
with the `kubectl get pg-backup` command to find out the proper backup name).
This option must be specified if the target is one or more backups away from the
current moment.

After setting these options in the *backup restore* configuration file,
follow the standard restore instructions.

!!! note

    Make sure you have a backup that is older than your desired point in time.
    You obviously can’t restore from a time where you do not have a backup.
    All relevant write-ahead log files must be successfully pushed before you
    make the restore.

### Restore to a new PostgreSQL cluster

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

