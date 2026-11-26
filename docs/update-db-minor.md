# Minor version upgrade of Percona Distribution for PostgreSQL

A minor version upgrade is the upgrade within the same major version. For example, from 17.5.2 to 17.6.1.

## Considerations

1. Upgrading a PostgreSQL cluster may result in downtime, as well as in [failover](change-primary.md) caused by updating the primary instance.
2. Starting with the Operator 2.6.0, Percona Distribution for PostgreSQL images are based on Red Hat Universal Base Image (UBI) 9. Each UBI major version ships a different version of `glibc` and ICU collation libraries, and a new image build within one UBI major can update `glibc` as well. A different `glibc` build can change the sorting rules of some locales and corrupt the objects that depend on them, such as text-based indexes. Before the upgrade, [check whether the change affects the locales your databases use](#assess-the-collation-risk). See the [glibc collation limitation](limitations.md#glibc-collation-changes-between-images).
3. [Logical replicas](logical-replication.md) can keep replicating after a minor upgrade if you [configured replication slots](ha-deploy.md#persist-replication-slots-across-failover). Without slots, a failover during the upgrade can break replication. [Reseed](logical-replication.md#reseed-a-logical-replica) the replica if the status becomes `broken`.

## Before you start

### Check operating system and glibc

--8<-- "check-os-glibc.txt"

### Assess the collation risk

--8<-- "collation-assess.txt"

If you need a repair, plan a maintenance window and stop application traffic before the upgrade. The Operator restarts the Pods on the new image one by one, replicas first and the primary last. Replicas then run on the new `glibc` with indexes that the old one built, while applications stay connected. [Repair the data](#after-the-pods-restart) before you let applications back in.

### Update PMM

1. [Update PMM Server :octicons-link-external-16:](https://docs.percona.com/percona-monitoring-and-management/3/pmm-upgrade/index.html) **before** upgrading PMM Client.
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

## After the Pods restart

If the [collation risk assessment](#assess-the-collation-risk) showed that a locale you use changed, or you couldn't confirm that it didn't, follow [Repair data after a collation change](collation-repair.md) when all Pods run on the new image. Keep the applications stopped until the repair is done.
