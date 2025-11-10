# Upgrade Database and Operator

Starting from the version 2.2.0, you can upgrade Percona Operator for PostgreSQL 
to newer 2.x versions.

!!! note

    Upgrades from the Operator version 1.x to 2.x are completely different from the upgrades within 2.x versions due to
    substantial changes in the architecture. Check [available methods for 1.x to 2.x upgrade](update.md#upgrade-from-the-operator-version-1x-to-version-2x)

The upgrade process consists of these steps:

* Upgrade the Operator  
* Upgrade the database (Percona Distribution for PostgreSQL).

## Update scenarios

You can either upgrade both the Operator and the database, or you can upgrade only the database. To decide which scenario to choose, read on.

### Full upgrade (CRD, Operator, and the database)

When to use this scenario:

* The new Operator version has changes that are required for new features of the database to work
* The Operator has new features or fixes that enhance automation and management.
* Compatibility improvements between the Operator and the database require synchronized updates.

When going on with this scenario, make sure to test it in a staging or testing environment first. Upgrading the Operator may cause performance degradation.

### Upgrade only the database

When to use this scenario:

* The new version of the database has new features or fixes that are not related to the Operator or other components of your infrastructure
* You have updated the Operator earlier and now want to proceed with the database update.

When choosing this scenario, consider the following:

* Check that the current Operator version supports the new database version.
* Some features may require an Operator upgrade later for full functionality.

Upgrading to a newer version typically involves two steps:

1. Upgrading the Operator and [Custom Resource Definition (CRD) :octicons-link-external-16:](https://kubernetes.io/docs/concepts/extend-kubernetes/api-extension/custom-resources/),
2. Upgrading the Database Management System (Percona Distribution for PostgreSQL).

Alternatively, it is also possible to carry on minor version upgrades of Percona
Distribution for PostgreSQL *without* the Operator upgrade.

## Upgrading the Operator and CRD

### Considerations

1. The Operator version has three digits separated by a dot (`.`) in the format `major.minor.patch`. Here's how you can understand the version `2.6.0`:

    * `2` - major version
    * `6` - minor version
    * `0` - patch version

    You can only upgrade the Operator to the nearest `major.minor` version. For example, from 2.6.0 to 2.7.0. To upgrade to a newer version, which differs from the current `minor.major` version by more than one, you need to make several incremental upgrades sequentially. 
    
    For example, to upgrade the CRD and Operator from the version 2.4.0 to 2.6.0, first upgrade it from 2.4.0 to 2.5.1, and then from 2.5.1 to 2.6.0.

    Patch versions don't influence the upgrade, so you can safely move from `2.5.0` to `2.5.1`.

2. CRD supports **the last 3 minor versions of the Operator**. This means it is compatible with the newest Operator version and the two previous minor versions. If the Operator is older than the CRD by no more than two versions, you should be able to continue using the old Operator version. But updating the CRD and Operator is the recommended path.

3. Using newer CRD with older Operator is useful to upgrade multiple [single-namespace Operator deployments](cluster-wide.md#namespace-scope) 
in one Kubernetes cluster, where each Operator controls a database cluster in
its own namespace. In this case upgrading Operator deployments will look as follows:

    * upgrade the CRD (not 3 minor versions far from the oldest Operator installation in the Kubernetes cluster) first 
    * upgrade the Operators in each namespace incrementally to the nearest minor version (e.g. first 2.4.0 to 2.5.1, then 2.5.1 to 2.6.0)

### Manual upgrade

You can upgrade the Operator and CRD as follows, considering the Operator uses
`postgres-operator` namespace, and you are upgrading it to the version {{ release }}.

1. Update the CRD for the Operator and the Role-based access control. You must use the [server-side :octicons-link-external-16:](https://kubernetes.io/docs/reference/using-api/server-side-apply/) flag when you update the CRD. Otherwise you can encounter a number of errors caused by applying the CRD client-side: the command may fail, the built-in PostgreSQL extensions can be lost during such upgrade, etc.

    Take the latest versions of the CRD and Role-based access control manifest from the official repository on GitHub with the following commands:


    ``` {.bash data-prompt="$" }
    $ kubectl apply --server-side -f https://raw.githubusercontent.com/percona/percona-postgresql-operator/v{{ release }}/deploy/crd.yaml
    $ kubectl apply -f https://raw.githubusercontent.com/percona/percona-postgresql-operator/v{{ release }}/deploy/rbac.yaml -n postgres-operator
    ```
    
    !!! note

        In case of [cluster-wide installation](cluster-wide.md), use `deploy/cw-rbac.yaml` instead of `deploy/rbac.yaml`.

2. Next, update the Percona Distribution for PostgreSQL. Find the image name for the current Operator release [in the list of certified images](images.md). Then [apply a patch :octicons-link-external-16:](https://kubernetes.io/docs/tasks/run-application/update-api-object-kubectl-patch/) to the Operator Deployment and specify the image name and version. Use the following command to update the Operator Deployment to the `{{ release }}` version:

    ``` {.bash data-prompt="$" }
    $ kubectl -n postgres-operator patch deployment percona-postgresql-operator \
       -p'{"spec":{"template":{"spec":{"containers":[{"name":"operator","image":"docker.io/percona/percona-postgresql-operator:{{ release }}"}]}}}}'
    ```

3. The deployment rollout will be automatically triggered by the applied patch.
    You can track the rollout process in real time with the
    `kubectl rollout status` command with the name of your cluster:

    ``` {.bash data-prompt="$" }
    $ kubectl rollout status deployments percona-postgresql-operator -n postgres-operator
    ```
    
    ??? example "Expected output"

        ``` {.text .no-copy}
        deployment "percona-postgresql-operator" successfully rolled out
        ```

### Upgrade via Helm

If you have [installed the Operator using Helm](helm.md), you can upgrade the
Operator deployment with the `helm upgrade` command.

 The `helm upgrade` command updates only the Operator deployment. The [update flow for the database management system (Percona Distribution for PostgreSQL)](#upgrade-percona-distribution-for-postgresql) is the same for all installation methods, whether it was installed via Helm or `kubectl`.

1. You must have the compatible version of the Custom Resource Definition (CRD) in all namespaces that the Operator manages. Starting with version 2.7.0, you can check it using the following command:

    ``` {.bash data-prompt="$" }
    $ kubectl get crd perconapgclusters.pgv2.percona.com --show-labels
    ```
    
2. Update the [Custom Resource Definition :octicons-link-external-16:](https://kubernetes.io/docs/concepts/extend-kubernetes/api-extension/custom-resources/)
    for the Operator, taking it from the official repository on GitHub. 

    Refer to the [compatibility between CRD and the Operator](#upgrading-the-operator-and-crd) and how you can update the CRD if it is too old. Use the following command and replace the version to the required one until you are safe to update to the latest CRD version.

    ``` {.bash data-prompt="$" }
    $ kubectl apply --server-side --force-conflicts -f https://raw.githubusercontent.com/percona/percona-postgresql-operator/v{{ release }}/deploy/crd.yaml
    ```
    
    If you already have the latest CRD version in one of namespaces, don't re-run intermediate upgrades for it.

3. Upgrade the Operator deployment

    === "With default parameters"

        To upgrade the Operator installed with default parameters, use the following command: 

        ``` {.bash data-prompt="$" }
        $ helm upgrade my-operator percona/pg-operator --version {{ release }}
        ```

        The `my-operator` parameter in the above example is the name of a [release object :octicons-link-external-16:](https://helm.sh/docs/intro/using_helm/#three-big-concepts)
        which you have chosen for the Operator when installing its Helm chart.

    === "With customized parameters"

        If you installed the Operator with some [customized parameters :octicons-link-external-16:](https://github.com/percona/percona-helm-charts/tree/main/charts/pg-operator#installing-the-chart), list these options in the upgrade command.   
    
        1. Get the list of used options in YAML format :
        
            ```{.bash data-prompt="$" }
            $ helm get values my-operator -a > my-values.yaml
            ``` 
        
        2. Pass these options to the upgrade command as follows:

            ``` {.bash data-prompt="$" }
            $ helm upgrade my-operator percona/pg-operator --version {{ release }} -f my-values.yaml
            ```

    During the upgrade, you may see a warning to manually apply the CRD if it has the outdated version. In this case, refer to step 2 to upgrade the CRD and then step 3 to upgrade the deployment.

### Upgrade via Operator Lifecycle Manager (OLM)

If you have [installed the Operator on the OpenShift platform using OLM](openshift.md#install-the-operator-via-the-operator-lifecycle-manager-olm), you can upgrade the Operator within it.

1. List installed Operators for your Namespace to see if there are upgradable items.

    ![image](assets/images/olm4.svg)

2. Click the "Upgrade available" link to see upgrade details, then click "Preview InstallPlan" button, and finally "Approve" to upgrade the Operator.

## Upgrade Percona Distribution for PostgreSQL

### Considerations

1. Starting from the Operator 2.4.0 you can do a *minor* upgrade (for example, from 15.5 to 15.7, or from 16.1 to 16.3) and a *major* upgrade (for example, upgrade from PostgreSQL 15.5 to PostgreSQL 16.3) of Percona Distribution for PostgreSQL. Before the Operator version 2.4.0, you could only do a minor upgrade of Percona Distribution for PostgreSQL. 

2. Starting with the Operator 2.6.0, PostgreSQL images are based on Red Hat Universal Base Image (UBI) 9 instead of UBI 8. UBI 9 has a different version of collation library `glibc` and this introduces a collation mismatch in PostgreSQL. Collation defines how text is sorted and compared based on language-specific rules such as case sensitivity, character order and the like. PostgreSQL stores the collation version used at database creation. When the collation version changes, this may result in corruption of database objects that use it like text-based indexes. Therefore, you need to identify and reindex objects affected by the collation mismatch.

3. Upgrading a PostgreSQL cluster may result in downtime, as well as [failover](change-primary.md) caused by updating the primary instance.

### Minor version upgrade

To make a minor upgrade of Percona Distribution for PostgreSQL (for example, from 16.1 to 16.3) , do the following:
{.power-number}

1. Check the version of the Operator you have in your Kubernetes environment. If you need to update it, refer to the [Operator upgrade guide](#upgrading-the-operator-and-crd)
2. Check the current version of the Custom Resource and what versions of the database and cluster components are compatible with it. Use the following command:
   
    ``` {.bash data-prompt="$" }
    $ curl <https://check.percona.com/versions/v1/pg-operator/{{release}}> |jq -r '.versions[].matrix'
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
        * `docker.io/percona/percona-pgbackrest:{{ pgbackrestrecommended }}`

4. After you applied the patch, the deployment rollout will be triggered automatically.
   The update process is successfully finished when all Pods have been restarted.

    ??? example "Expected output"

        --8<-- "kubectl-get-pods-response.txt"

--8<-- "collation.txt"

### Major version upgrade

Major version upgrade allows you to jump from one database major version to another (for example, upgrade from PostgreSQL 15.5 to PostgreSQL 16.3).

!!! note

    Major version upgrades feature is currently a **tech preview**, and it is **not recommended for production environments.**

    Also, currently the major version upgrade only works if the images in Custom Resource (`deploy/cr.yaml` manifest) are specified without minor version numbers:

    ```yaml
    ...
    image: docker.io/percona/percona-distribution-postgresql:15
    postgresVersion: 15
    ...
    ```
    
    It will not work for images specified like `docker.io/percona/percona-postgresql-operator:2.4.0-ppg15.7-postgres`.

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
  toPostgresImage: docker.io/percona/percona-distribution-postgresql:{{ postgres16recommended }}
  toPgBouncerImage: docker.io/percona/percona-pgbouncer:{{ pgbouncerrecommended }}
  toPgBackRestImage: docker.io/percona/percona-pgbackrest:{{ pgbackrestrecommended }}
```

As you can see, the manifest includes image names for the database cluster components (PostgreSQL, pgBouncer, and pgBackRest). You can find them [in the list of certified images](images.md) for the current Operator release. For older versions, please refer to the [old releases documentation archive :octicons-link-external-16:](https://docs.percona.com/legacy-documentation/).

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

### Upgrade `pg_stat_monitor` (for Operator earlier than 2.6.0)

`pg_stat_monitor` is the built-in extension, which is used to provide query analytics for Percona Monitoring and Management (PMM). If you [enabled it](custom-extensions.md#enabling-or-disabling-built-in-extensions) in the Custom Resource (`deploy/cr.yaml` manifest), you need to manually update it *after the database upgrade* (this manual step is not required for the Operator versions 2.6.0 and newer):

1. Find the primary instance of your PostgreSQL cluster. You can do this using Kubernetes Labels as follows (replace the `<namespace>` placeholder with your value):

    ```{.bash data-prompt="$"}
    $ kubectl get pods -n <namespace> -l postgres-operator.crunchydata.com/cluster=cluster1 \ 
        -L postgres-operator.crunchydata.com/instance \
        -L postgres-operator.crunchydata.com/role | grep instance1
    ```

    ???+ example "Sample output"

        ```{.text .no-copy hl_lines="3"}
        cluster1-instance1-bmdp-0             4/4     Running   0          2m23s   cluster1-instance1-bmdp   replica
        cluster1-instance1-fm7w-0             4/4     Running   0          2m22s   cluster1-instance1-fm7w   replica
        cluster1-instance1-ttm9-0             4/4     Running   0          2m22s   cluster1-instance1-ttm9   master
        ```
    PostgreSQL primary is labeled as `master`, while other PostgreSQL instances are labeled as `replica`.

2. Log in to a primary instance (`cluster1-instance1-ttm9-0` in the above example) as an administrative user:

    ``` {.bash data-prompt="$" }
    kubectl exec  -n <namespace> -ti cluster1-instance1-ttm9-0 -c database -- psql postgres
    ```

3. Execute the following SQL statement:

    ``` {.sql data-prompt="postgres=#" }
    postgres=# alter extension pg_stat_monitor update;
    ```

### Upgrading PostgreSQL extensions

If there are [custom PostgreSQL extensions](custom-extensions.md#adding-custom-extensions) installed in the cluster, they need to be taken into account: you need to build and package each custom extension for the new PostgreSQL major version. During the  upgrade the Operator will install extensions into the upgrade container.


## Upgrade from the Operator version 1.x to version 2.x

The Operator version 2.x has a lot of differences compared to the version 1.x.
This makes upgrading from version 1.x to version 2.x quite different from a normal upgrade. In fact, you have to migrate the cluster from version 1.x to version 2.x.

There are several ways to do such version 1.x to version 2.x upgrade. Choose the method based on your downtime preference and roll back strategy:

|                                                                                                                     | Pros                | Cons        |
| --------------------------------------------------------------------------------------------------------------------| --------------------| ------------|
| [Data Volumes migration](update-data-volumes.md) - re-use the volumes that were created by the Operator version 1.x | The simplest method | - Requires downtime <br> - Impossible to roll back |
| [Backup and restore](update-backup-restore.md) - take the backup with the Operator version 1.x and restore it to the cluster deployed by the Operator version 2.x | Allows you to quickly test version 2.x | Provides significant downtime in case of migration |
| [Replication](update-standby.md) - replicate the data from the Operator version 1.x cluster to the standby cluster deployed by the Operator version 2.x | - Quick test of v2 cluster <br> - Minimal downtime during upgrade | Requires significant computing resources to run two clusters in parallel | 

