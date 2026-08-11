# Minor version upgrade of Percona Distribution for PostgreSQL

A minor version upgrade is the upgrade within the same major version. For example, from 17.5.2 to 17.6.1.

## Considerations

1. Upgrading a PostgreSQL cluster may result in downtime, as well as in [failover](change-primary.md) caused by updating the primary instance.
2. Starting with the Operator 2.6.0, PostgreSQL images are based on Red Hat Universal Base Image (UBI) 9 instead of UBI 8. UBI 9 has a different version of collation library `glibc` and this introduces a collation mismatch in PostgreSQL. Collation defines how text is sorted and compared based on language-specific rules such as case sensitivity, character order and the like. PostgreSQL stores the collation version used at database creation. When the collation version changes, this may result in corruption of database objects that use it like text-based indexes. Therefore, you need to identify and reindex objects affected by the collation mismatch.

## Before you start

1. We recommend to [update PMM Server :octicons-link-external-16:](https://docs.percona.com/percona-monitoring-and-management/3/pmm-upgrade/index.html) **before** upgrading PMM Client.
2. PMM2 has reached its end-of-life stage and is no longer supported in the Operator. See [PMM upgrade documentation :octicons-link-external-16:](https://docs.percona.com/percona-monitoring-and-management/3/pmm-upgrade/migrating_from_pmm_2.html) for how to migrate from version 2 to version 3.

## Upgrade steps

To make a minor upgrade of Percona Distribution for PostgreSQL, do the following:
{.power-number}

1. Check the version of the Operator you have in your Kubernetes environment. If you need to update it, refer to the [Operator upgrade guide](update-operator.md)
2. Check the current version of the Custom Resource and what versions of the database and cluster components are compatible with it. Replace the Operator version with your value in the following command:
   
    ```bash
    curl https://check.percona.com/versions/v1/pg-operator/{{release}} |jq -r '.versions[].matrix'
    ```

    You can also find this information in the [Versions compatibility matrix](versions.md).

3. Update the database, the backup and PMM Client image names with a newer version tag. Find the image names [in the list of certified images](images.md).

    We recommend to update the PMM Server **before** the upgrade of PMM Client. If you haven't done it yet, exclude PMM Client from the list of images to update.

    Since this is a working cluster, the way to update the Custom Resource is to [apply a patch  :octicons-link-external-16:](https://kubernetes.io/docs/tasks/run-application/update-api-object-kubectl-patch/) with the `kubectl patch pg` command.

    This example command updates the cluster with the name `cluster1` in the namespace `postgres-operator` to the `{{ release }}` version:
    

    === "With PMM Client"

        ```bash
        kubectl -n postgres-operator patch pg cluster1 --type=merge --patch '{
           "spec": {
              "crVersion":"{{ release }}",
              "image": "docker.io/percona/percona-distribution-postgresql:{{ postgresrecommended }}",
              "proxy": { "pgBouncer": { "image": "docker.io/percona/percona-pgbouncer:{{ pgbouncerrecommended }}" } },
              "backups": { "pgbackrest":  { "image": "docker.io/percona/percona-pgbackrest:{{ pgbackrestrecommended }}" } },
              "pmm": { "image": "docker.io/percona/pmm-client:{{ pmm3recommended }}" }
           }}'
        ```

        The following image names in the above example were taken from the [list of certified images](images.md):
    
        * `docker.io/percona/percona-distribution-postgresql:{{ postgresrecommended }}`,
        * `docker.io/percona/percona-pgbouncer:{{ pgbouncerrecommended }}`,
        * `docker.io/percona/percona-pgbackrest:{{ pgbackrestrecommended }}`,
        * `docker.io/percona/pmm-client:{{ pmm3recommended }}`.

    === "Without PMM Client"

        ```bash
        kubectl patch pg cluster1 -n postgres-operator --type=merge --patch '{
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
        * `docker.io/percona/percona-pgbackrest:{{ pgbackrestrecommended }}`
    
    === "with PostGIS"

        When using the [PostGIS](postgis.md) extension, make sure to specify the image that contains it for the `kubectl patch command`. Add PMM client image to the list if you also use it.

        ```bash
        kubectl patch pg cluster1 -n postgres-operator --type=merge --patch '{
           "spec": {
              "crVersion":"{{ release }}",
              "image": "docker.io/percona/percona-distribution-postgresql-with-postgis:{{ postgrespostgisrecommended }}",
              "proxy": { "pgBouncer": { "image": "docker.io/percona/percona-pgbouncer:{{ pgbouncerrecommended }}" } },
              "backups": { "pgbackrest":  { "image": "docker.io/percona/percona-pgbackrest:{{ pgbackrestrecommended }}" } }
           }}'
        ```

        The following image names in the above example were taken from the [list of certified images](images.md):
    
        * `docker.io/percona/percona-distribution-postgresql-with-postgis:{{ postgrespostgisrecommended }}`,
        * `docker.io/percona/percona-pgbouncer:{{ pgbouncerrecommended }}`,
        * `docker.io/percona/percona-pgbackrest:{{ pgbackrestrecommended }}`

4. After you applied the patch, the deployment rollout will be triggered automatically.
   The update process is successfully finished when all Pods have been restarted.

    ??? example "Expected output"

        --8<-- "kubectl-get-pods-response.txt"

--8<-- "collation.txt"