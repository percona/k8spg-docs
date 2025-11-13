# Upgrade Percona Distribution for PostgreSQL

## Considerations

1. Starting from the Operator 2.4.0 you can do a *minor* upgrade (for example, from 15.5 to 15.7, or from 16.1 to 16.3) and a *major* upgrade (for example, upgrade from PostgreSQL 15.5 to PostgreSQL 16.3) of Percona Distribution for PostgreSQL. Before the Operator version 2.4.0, you could only do a minor upgrade of Percona Distribution for PostgreSQL. 

2. Starting with the Operator 2.6.0, PostgreSQL images are based on Red Hat Universal Base Image (UBI) 9 instead of UBI 8. UBI 9 has a different version of collation library `glibc` and this introduces a collation mismatch in PostgreSQL. Collation defines how text is sorted and compared based on language-specific rules such as case sensitivity, character order and the like. PostgreSQL stores the collation version used at database creation. When the collation version changes, this may result in corruption of database objects that use it like text-based indexes. Therefore, you need to identify and reindex objects affected by the collation mismatch.

3. Upgrading a PostgreSQL cluster may result in downtime, as well as [failover](change-primary.md) caused by updating the primary instance.

## Before you start

1. We recommend to [update PMM Server :octicons-link-external-16:](https://docs.percona.com/percona-monitoring-and-management/2/how-to/upgrade.html) **before** upgrading PMM Client.

2. If you are using PMM server version 2, use a PMM client image compatible with PMM 2. If you are using PMM server version 3, use a PMM client image compatible with PMM 3. See [PMM upgrade documentation :octicons-link-external-16:](https://docs.percona.com/percona-monitoring-and-management/3/pmm-upgrade/migrating_from_pmm_2.html) for how to migrate from version 2 to version 3.


## Minor version upgrade

To make a minor upgrade of Percona Distribution for PostgreSQL (for example, from 17.5.2 to 17.6.1) , do the following:
{.power-number}

1. Check the version of the Operator you have in your Kubernetes environment. If you need to update it, refer to the [Operator upgrade guide](#upgrading-the-operator-and-crd)
2. Check the current version of the Custom Resource and what versions of the database and cluster components are compatible with it. Replace the Operator version with your value in the following command:
   
    ``` {.bash data-prompt="$" }
    $ curl https://check.percona.com/versions/v1/pg-operator/2.6.0 |jq -r '.versions[].matrix'
    ```

    You can also find this information in the [Versions compatibility matrix](versions.md).

3. Update the database, the backup and PMM Client image names with a newer version tag. Find the image names [in the list of certified images](images.md).

    We recommend to update the PMM Server **before** the upgrade of PMM Client. If you haven't done it yet, exclude PMM Client from the list of images to update.

    Since this is a working cluster, the way to update the Custom Resource is to [apply a patch  :octicons-link-external-16:](https://kubernetes.io/docs/tasks/run-application/update-api-object-kubectl-patch/) with the `kubectl patch pg` command.

    This example command updates the cluster with the name `cluster1` in the namespace `postgres-operator` to the `{{ release }}` version:
    

    === "With PMM Client"

        ``` {.bash data-prompt="$" }
        $ kubectl -n postgres-operator patch pg cluster1 --type=merge --patch '{
           "spec": {
              "crVersion":"{{ release }}",
              "image": "docker.io/percona/percona-distribution-postgresql:{{ postgresrecommended }},
              "proxy": { "pgBouncer": { "image": "docker.io/percona/percona-pgbouncer:{{ pgbouncerrecommended }}" } },
              "backups": { "pgbackrest":  { "image": "docker.io/percona/percona-pgbackrest:{{ pgbackrestrecommended }}" } },
              "pmm": { "image": "docker.io/percona/pmm-client:{{ pmm2recommended }}" }
           }}'
        ```

        The following image names in the above example were taken from the [list of certified images](images.md):
    
        * `docker.io/percona/percona-distribution-postgresql:{{ postgresrecommended }}`,
        * `docker.io/percona/percona-pgbouncer:{{ pgbouncerrecommended }}`,
        * `docker.io/percona/percona-pgbackrest:{{ pgbackrestrecommended }}`,
        * `docker.io/percona/pmm-client:{{ pmm2recommended }}`.

    === "Without PMM Client"

        ``` {.bash data-prompt="$" }
        $ kubectl patch pg cluster1 -n postgres-operator --type=merge --patch '{
           "spec": {
              "crVersion":"{{ release }}",
              "image": "docker.io/percona/percona-distribution-postgresql:{{ postgresrecommended }}",
              "proxy": { "pgBouncer": { "image": "docker.io/percona/percona-pgbouncer:{{ pgbouncerrecommended }}" } },
              "backups": { "pgbackrest":  { "image": "docker.io/percona/percona-pgbackrest:{{ pgbackrestrecommended }}" } }
           }}'
        ```

        The following image names in the above example were taken from the [list of certified images](images.md):
    
        * `docker.io/percona/percona-distribution-postgresql:{{ postgresrecommended }}`,
        * `docker.io/percona/percona-pgbouncer:{{ pgbouncerrecommended }}`,
        * `docker.io/percona/percona-pgbackrest:{{ pgbackrestrecommended }}`,

4. After you applied the patch, the deployment rollout will be triggered automatically.
   The update process is successfully finished when all Pods have been restarted.

    ??? example "Expected output"

        --8<-- "kubectl-get-pods-response.txt"

--8<-- "collation.txt"

## Major version upgrade

Major version upgrade allows you to jump from one database major version to another (for example, upgrade from PostgreSQL 15.5 to PostgreSQL 16.3).

!!! note

    Major version upgrades feature is currently a **tech preview**, and it is **not recommended for production environments.**

    Also, currently the major version upgrade only works if the images in Custom Resource (`deploy/cr.yaml` manifest) are specified without minor version numbers:

    ```yaml
    ...
    image: docker.io/percona/percona-postgresql-operator:{{release}}-ppg15-postgres
    postgresVersion: 15
    ...
    ```
    
    It will not work for images specified like `percona/percona-postgresql-operator:2.4.0-ppg15.7-postgres`.

The upgrade is triggered by applying the YAML file which refers to the special *Operator upgrade image* and contains the information about the existing and desired major versions. An example of this file is present in `deploy/upgrade.yaml`:

```yaml
apiVersion: pgv2.percona.com/v2
kind: PerconaPGUpgrade
metadata:
  name: cluster1-15-to-16
spec:
  postgresClusterName: cluster1
  image: docker.io/percona/percona-postgresql-operator:{{ release }}-upgrade
  fromPostgresVersion: 15
  toPostgresVersion: 16
  toPostgresImage: docker.io/percona/percona-postgresql-operator:{{ release }}-ppg{{ postgres16recommended }}-postgres
  toPgBouncerImage: docker.io/percona/percona-pgbouncer:{{ pgbouncerrecommended }}
  toPgBackRestImage: docker.io/percona/percona-pgbackrest:{{ pgbackrestrecommended }}
```

As you can see, the manifest includes image names for the database cluster components (PostgreSQL, pgBouncer, and pgBackRest). You can find them [in the list of certified images](images.md) for the current Operator release. For older versions, please refer to the [old releases documentation archive :octicons-link-external-16:](https://docs.percona.com/legacy-documentation/)).

After you apply the YAML manifest as usual (by running `kubectl apply -f deploy/upgrade.yaml` command), the actual upgrade takes place:

1. The Operator pauses the cluster, so the cluster will be unavailable for the duration of the upgrade,
2. The cluster is specially annotated with `pgv2.percona.com/allow-upgrade`: `<PerconaPGUpgrade.Name>` annotation,
3. Jobs are created to migrate the data,
4. The cluster starts up after the upgrade finishes.

--8<-- "collation.txt"

!!! note

    If the upgrade fails for some reason, the cluster will stay in paused mode. Resume the cluster [manually](pause.md) to check what went wrong with upgrade (it will start with the old version). You can check the PerconaPGUpgrade resource with `kubectl get perconapgupgrade -o yaml` command, and [check the logs](debug-logs.md) of the upgraded Pods to debug the issue.

During the upgrade data are duplicated in the same PVC for each major upgrade, and old version data are not deleted automatically. Make sure your PVC has enough free space to store data.
You can remove data at your discretion by [executing into containers](debug-shell.md) and running the following commands (example for PostgreSQL 15):

``` {.bash data-prompt="$" }
$ rm -rf /pgdata/pg15
$ rm -rf /pgdata/pg15_wal
```

You can also delete the `PerconaPGUpgrade` resource (this will clean up the jobs and Pods created during the upgrade):

``` {.bash data-prompt="$" }
$ kubectl delete perconapgupgrade cluster1-15-to-16
```