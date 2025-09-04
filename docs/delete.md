# Delete Percona Operator for PostgreSQL

When cleaning up your Kubernetes environment (e.g., moving from a trial
deployment to a production one, or testing experimental configurations), you may
need to remove some (or all) of the following objects:

* Percona Distribution for PosgreSQL cluster managed by the Operator
* Percona Operator for PostgreSQL itself
* Custom Resource Definition deployed with the Operator
* Resources like PVCs and Secrets

## Delete a database cluster

You can delete the Percona Distribution for PosgreSQL cluster managed by the
Operator by deleting the appropriate Custom Resource.

!!! note

    There are two [finalizers :octicons-link-external-16:](https://kubernetes.io/docs/tasks/extend-kubernetes/custom-resources/custom-resource-definitions/#finalizers) defined in the Custom Resource, which define whether TLS-related objects and data volumes should be deleted or preserved when the cluster is deleted.

    * `finalizers.percona.com/delete-ssl`: if present, deletes [objects, created for SSL](TLS.md) (Secret, certificate, and issuer) when the cluster deletion occurs.
    * `finalizers.percona.com/delete-pvc`: if present, deletes [Persistent Volume Claims :octicons-link-external-16:](https://kubernetes.io/docs/concepts/storage/persistent-volumes/) for the database cluster Pods and user Secrets when the cluster deletion occurs.

    Both finalizers are off by default in the `deploy/cr.yaml` configuration file, and this allows you to recreate the cluster without losing data, credentials for the system users, etc.

Here's a sequence of steps to follow:
{.power-number}

1. List Custom Resources, replacing the `<namespace>` placeholder with your
    namespace.
    
    ``` {.bash data-prompt="$"}
    $ kubectl get pg -n <namespace>
    ```

    ??? example "Sample output"

        --8<-- "kubectl-get-pg-response.txt"

2. Delete the Custom Resource with the name of your cluster (for example, let's
    use the default `cluster1` name).

    ``` {.bash data-prompt="$"}
    $ kubectl delete pg cluster1 -n <namespace>
    ```

    ??? example "Sample output"

        ``` {.text .no-copy}
        perconapgcluster.pgv2.percona.com "cluster1" deleted
        ```

3. Check that the cluster is deleted by listing the available Custom Resources
    once again.

    ``` {.bash data-prompt="$"}
    $ kubectl get pg -n <namespace>
    ``` 

    ??? example "Sample output"

        ``` {.text .no-copy}
        No resources found in <namespace> namespace.
        ```

## Delete the Operator

You can uninstall the Operator by deleting the [Deployments :octicons-link-external-16:](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/)
related to it.
{.power-number}

1. List the deployments. Replace the `<namespace>` placeholder with your
    namespace.
    
    ``` {.bash data-prompt="$"}
    $ kubectl get deploy -n <namespace>
    ```

    ??? example "Sample output"

        ``` {.text .no-copy}
        NAME                          READY   UP-TO-DATE   AVAILABLE   AGE
        percona-postgresql-operator   1/1     1            1           13m
        ```

2. Delete the `percona-*` deployment

    ``` {.bash data-prompt="$"}
    $ kubectl delete deploy percona-postgresql-operator -n <namespace>
    ```

3. Check that the Operator is deleted by listing the Pods. As a result you
    should have no Pods related to it.

    ``` {.bash data-prompt="$"}
    $ kubectl get pods -n <namespace>
    ``` 

    ??? example "Sample output"

        ``` {.text .no-copy}
        No resources found in <namespace> namespace.
        ```

## Delete Custom Resource Definition

If you are not just deleting the Operator and PostgreSQL cluster from a specific
namespace, but want to clean up your entire Kubernetes environment,
you can also delete the [CustomRecourceDefinitions (CRDs) :octicons-link-external-16:](https://kubernetes.io/docs/concepts/extend-kubernetes/api-extension/custom-resources/#customresourcedefinitions). 

!!! warning 

    CRDs in Kubernetes are non-namespaced but are available to the whole
    environment. This means that you shouldn't delete CRD if you still have the
    Operator and database cluster in some namespace.

You can delete CRD as follows:
{.power-number}

1. List the CRDs:

    ``` {.bash data-prompt="$"}
    $ kubectl get crd
    ```

    ??? example "Sample output"

        ``` {.text .no-copy}
        allowlistedv2workloads.auto.gke.io                   2023-09-07T14:15:30Z
        allowlistedworkloads.auto.gke.io                     2023-09-07T14:15:29Z
        audits.warden.gke.io                                 2023-09-07T14:15:32Z
        backendconfigs.cloud.google.com                      2023-09-07T14:15:41Z
        capacityrequests.internal.autoscaling.gke.io         2023-09-07T14:15:25Z
        frontendconfigs.networking.gke.io                    2023-09-07T14:15:41Z
        managedcertificates.networking.gke.io                2023-09-07T14:15:41Z
        memberships.hub.gke.io                               2023-09-07T14:15:30Z
        perconapgbackups.pgv2.percona.com                    2023-09-07T14:28:59Z
        perconapgclusters.pgv2.percona.com                   2023-09-07T14:29:02Z
        perconapgrestores.pgv2.percona.com                   2023-09-07T14:29:03Z
        postgresclusters.postgres-operator.crunchydata.com   2023-09-07T14:29:06Z
        serviceattachments.networking.gke.io                 2023-09-07T14:15:44Z
        servicenetworkendpointgroups.networking.gke.io       2023-09-07T14:15:43Z
        storagestates.migration.k8s.io                       2023-09-07T14:15:53Z
        storageversionmigrations.migration.k8s.io            2023-09-07T14:15:53Z
        updateinfos.nodemanagement.gke.io                    2023-09-07T14:15:55Z
        volumesnapshotclasses.snapshot.storage.k8s.io        2023-09-07T14:15:52Z
        volumesnapshotcontents.snapshot.storage.k8s.io       2023-09-07T14:15:52Z
        volumesnapshots.snapshot.storage.k8s.io              2023-09-07T14:15:52Z
        ```

2. Now delete the `percona*.pgv2.percona.com` CRDs:

    ``` {.bash data-prompt="$"}
    $ kubectl delete crd perconapgbackups.pgv2.percona.com perconapgclusters.pgv2.percona.com perconapgrestores.pgv2.percona.com
    ```

    ??? example "Sample output"

        ``` {.text .no-copy}
        customresourcedefinition.apiextensions.k8s.io "perconapgbackups.pgv2.percona.com" deleted
        customresourcedefinition.apiextensions.k8s.io "perconapgclusters.pgv2.percona.com" deleted
        customresourcedefinition.apiextensions.k8s.io "perconapgrestores.pgv2.percona.com" deleted
        ```

## Clean up resources

By default, TLS-related objects and data volumes remain in Kubernetes environment after you delete the cluster to allow you to recreate it without losing the data.

You can automate resource cleanup by turning on `percona.com/delete-pvc` and/or `percona.com/delete-ssl` [finalizers](operator.md#metadata-name)). You can also delete TLS-related objects and PVCs manually.

To manually clean up resources, do the following:
{.power-number}

1. Delete Persistent Volume Claims.
   
    1. List PVCs. Replace the `<namespace>` placeholder with your namespace:

        ```{.bash data-prompt="$"}
        $ kubectl get pvc -n <namespace>
        ```    

        ??? example "Sample output"

            ```{.text .no-copy}
            NAME                             STATUS   VOLUME                                     CAPACITY   ACCESS MODES   STORAGECLASS   VOLUMEATTRIBUTESCLASS   AGE
            cluster1-instance1-mkwh-pgdata   Bound    pvc-c22220e9-c5e9-40b8-91b5-3d437b40bdec   1Gi        RWO            standard-rwo   <unset>                 4m17s
            cluster1-instance1-nvh4-pgdata   Bound    pvc-61a64aca-5165-4d25-b055-efc455d545b8   1Gi        RWO            standard-rwo   <unset>                 4m17s
            cluster1-instance1-qknb-pgdata   Bound    pvc-87bc6549-ee49-47f5-9f5e-83a315f78fd9   1Gi        RWO            standard-rwo   <unset>                 4m18s
            cluster1-repo1                   Bound    pvc-380e1100-b679-4716-ae8f-78372448b5f0   1Gi        RWO            standard-rwo   <unset>                 4m15s
            ```
        
    2. Delete PVCs related to your cluster. The following command deletes PVCs for the `cluster1` cluster:

        ```{.bash data-prompt="$"}
        kubectl delete pvc cluster1-instance1-mkwh-pgdata cluster1-instance1-nvh4-pgdata cluster1-instance1-qknb-pgdata cluster1-repo1 -n <namespace>
        ```

        ??? example "Sample output"

            ```{.text .no-copy}
            persistentvolumeclaim "cluster1-instance1-mkwh-pgdata" deleted
            persistentvolumeclaim "cluster1-instance1-nvh4-pgdata" deleted
            persistentvolumeclaim "cluster1-instance1-qknb-pgdata" deleted
            persistentvolumeclaim "cluster1-repo1" deleted
            ```

         Note that if your Custom Resource manifest includes the `percona.com/delete-pvc` finalizer, all user Secrets will be automatically deleted when you delete the PVCs. To prevent this from happening, disable the finalizer.

    2. Delete the Secrets

        1. List Secrets:

            ```{.bash data-prompt="$"}
            $ kubectl get secrets -n <namespace>
            ```    

        2. Delete the Secret:
        
            ```{.bash data-prompt="$"}
            $ kubectl delete secret <secret_name> -n <namespace>
            ```
