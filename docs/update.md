# Upgrade Database and Operator

## Upgrade from the Operator version 1.x to version 2.x

The Operator version 2.x has a lot of differences compared to the version 1.x.
This makes upgrading from version 1.x to version 2.x quite different from a normal upgrade. In fact, you have to migrate the cluster from version 1.x to version 2.x.

There are several ways to do such version 1.x to version 2.x upgrade. Choose the method based on your downtime preference and roll back strategy:

|                                                                                                                     | Pros                | Cons        |
| --------------------------------------------------------------------------------------------------------------------| --------------------| ------------|
| [Data Volumes migration](update-data-volumes.md) - re-use the volumes that were created by the Operator version 1.x | The simplest method | - Requires downtime <br> - Impossible to roll back |
| [Backup and restore](update-backup-restore.md) - take the backup with the Operator version 1.x and restore it to the cluster deployed by the Operator version 2.x | Allows you to quickly test version 2.x | Provides significant downtime in case of migration |
| [Replication](update-standby.md) - replicate the data from the Operator version 1.x cluster to the standby cluster deployed by the Operator version 2.x | - Quick test of v2 cluster <br> - Minimal downtime during upgrade | Requires significant computing resources to run two clusters in parallel | 

## Update Database and Operator version 2.x

Starting from the version 2.2.0 Percona Operator for PostgreSQL allows upgrades
to newer 2.x versions. The upgradable components of the cluster are
the following ones:

* the Operator;
* [Custom Resource Definition (CRD)](operator.md),
* Database Management System (Percona Distribution for PostgreSQL).

The list of recommended upgrade scenarios includes two variants:

* Upgrade to the new versions of the Operator *and* Percona Distribution for PostgreSQL,
* Minor Percona Distribution for PostgreSQL version upgrade *without* the Operator upgrade.

### Upgrading the Operator and CRD

!!! note

    The Operator supports **last 3 versions of the CRD**, so it is technically
    possible to skip upgrading the CRD and just upgrade the Operator. If the CRD
    is older than the new Operator version *by no more than three releases*, you
    will be able to continue using the old CRD and even carry on Percona Distribution
    for PostgreSQL minor version upgrades with it. But the recommended way is to
    update the Operator *and* CRD.

Only the incremental update to a nearest version of the Operator is supported
(for example, update from 2.2.0 to 2.3.0). To update to a newer version, which
differs from the current version by more than one, make several incremental
updates sequentially.

Considering the Operator uses `postgres-operator` namespace, upgrade to the version {{ release }} includes the following steps.

1. Update the [Custom Resource Definition](https://kubernetes.io/docs/concepts/extend-kubernetes/api-extension/custom-resources/)
    for the Operator, taking it from the official repository on Github, and do
    the same for the Role-based access control:

    ``` {.bash data-prompt="$" }
    $ kubectl apply --server-side -f https://raw.githubusercontent.com/percona/percona-postgresql-operator/v{{ release }}/deploy/crd.yaml
    $ kubectl apply -f https://raw.githubusercontent.com/percona/percona-postgresql-operator/v{{ release }}/deploy/rbac.yaml -n postgres-operator
    ```
    !!! note

        In case of [cluster-wide installation](cluster-wide.md), use `deploy/cw-rbac.yaml` instead of `deploy/rbac.yaml`.

3. Now you should [apply a patch](https://kubernetes.io/docs/tasks/run-application/update-api-object-kubectl-patch/)
    to your deployment, supplying necessary image name with a newer version
    tag. You can find the proper
    image name for the current Operator release [in the list of certified images](images.md#custom-registry-images).
    updating to the `{{ release }}` version should look as follows:

    ``` {.bash data-prompt="$" }
    $ kubectl -n postgres-operator patch deployment percona-postgresql-operator \
       -p'{"spec":{"template":{"spec":{"containers":[{"name":"operator","image":"percona/percona-postgresql-operator:{{ release }}"}]}}}}'
    ```

4. The deployment rollout will be automatically triggered by the applied patch.
    You can track the rollout process in real time with the
    `kubectl rollout status` command with the name of your cluster:

    ``` {.bash data-prompt="$" }
    $ kubectl rollout status deployments percona-postgresql-operator
    ```

## Upgrading Percona Distribution for PostgreSQL

Upgrading Percona Distribution for PostgreSQL can be done as follows:

1. [Apply a patch](https://kubernetes.io/docs/tasks/run-application/update-api-object-kubectl-patch/)
    to your Custom Resource, setting necessary Custom Resource version and image
    names with a newer version tag.

    !!! note

        Check the version of the Operator you have in your Kubernetes
        environment. Please refer to the [Operator upgrade guide](update.md#upgrading-the-operator-and-crd)
        to upgrade the Operator and CRD, if needed.

    Patching Custom Resource is done with the `kubectl patch pg` command.
    Actual image names can be found [in the list of certified images](images.md#custom-registry-images).
    For example, updating `cluster1` cluster to the `{{ release }}` version
    should look as follows:

    ``` {.bash data-prompt="$" }
    $ kubectl -n postgres-operator patch pg cluster1 --type=merge --patch '{
       "spec": {
          "crVersion":"{{ release }}",
          "image": "percona/percona-postgresql-operator:{{ release }}-ppg15-postgres",
          "proxy": { "pgBouncer": { "image": "percona/percona-postgresql-operator:{{ release }}-ppg15-pgbouncer" } },
          "backups": { "pgbackrest":  { "image": "percona/percona-postgresql-operator:{{ release }}-ppg15-pgbackrest" } },
          "pmm": { "image": "percona/pmm-client:{{ pmm2recommended }}" }
       }}'
    ```

    !!! warning

        The above command upgrades various components of the cluster including PMM Client. It is [highly recommended](https://docs.percona.com/percona-monitoring-and-management/how-to/upgrade.html) to upgrade PMM Server **before** upgrading PMM Client. If it wasn't done and you would like to avoid PMM Client upgrade, remove it from the list of images, reducing the last of two patch commands as follows:
    
        ``` {.bash data-prompt="$" }
        $ kubectl -n postgres-operator patch pg cluster1 --type=merge --patch '{
           "spec": {
              "crVersion":"{{ release }}",
              "image": "percona/percona-postgresql-operator:{{ release }}-ppg15-postgres",
              "proxy": { "pgBouncer": { "image": "percona/percona-postgresql-operator:{{ release }}-ppg15-pgbouncer" } },
              "backups": { "pgbackrest":  { "image": "percona/percona-postgresql-operator:{{ release }}-ppg15-pgbackrest" } }
           }}'
        ```

The deployment rollout will be automatically triggered by the applied patch.
The update process is successfully finished when all Pods have been restarted.


