# Delete Percona Operator for PostgreSQL

To delete Percona Operator for PostgreSQL from Kubernetes environment means to delete the [CustomRecourceDefinitions (CRDs))](https://kubernetes.io/docs/concepts/extend-kubernetes/api-extension/custom-resources/#customresourcedefinitions) and the [Deployments](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/) related to the Operator.

Here's the sequence of steps to do it:

1. List the CRDs:

    ```{.bash data-prompt="$"}
    $ kubectl get crd
    ```

    ??? example "Sample output"

        ```{.text .no-copy}
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

2. Delete the `percona*.pgv2.percona.com` CRDs

    ```{.bash data-prompt="$"}
    $ kubectl delete crd perconapgbackups.pgv2.percona.com perconapgclusters.pgv2.percona.com perconapgrestores.pgv2.percona.com
    ```

    ??? example "Sample output"

        ```{.text .no-copy}
        customresourcedefinition.apiextensions.k8s.io "perconapgbackups.pgv2.percona.com" deleted
        customresourcedefinition.apiextensions.k8s.io "perconapgclusters.pgv2.percona.com" deleted
        customresourcedefinition.apiextensions.k8s.io "perconapgrestores.pgv2.percona.com" deleted
        ```

3. List the deployments. Replace the `<namespace>` placeholder with your namespace.
    
    ```{.bash data-prompt="$"}
    $ kubectl get deploy -n <namespace>
    ```

    ??? example "Sample output"

        ```{.text .no-copy}
        NAME                          READY   UP-TO-DATE   AVAILABLE   AGE
        percona-postgresql-operator   1/1     1            1           13m
        ```

4. Delete the `percona-*` deployment

    ```{.bash data-prompt="$"}
    $ kubectl delete deploy percona-postgresql-operator -n <namespace>
    ```

5. Check that the Operator is deleted by listing the Pods. As a result you should have no Pods 

    ```{.bash data-prompt="$"}
    $ kubectl get pods -n <namespace>
    ``` 

    ??? example "Sample output"

        ```{.text .no-copy}
        No resources found in <namespace> namespace.
        ```
