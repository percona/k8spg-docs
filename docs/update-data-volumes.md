# Upgrade using data volumes

## Prerequisites:

- You have a v1 cluster with `spec.keepData: true` in the Custom Resource
- You have both operators deployed and allow them to control resources in the same namespace
- Old and new clusters must be of the same PostgreSQL major version

This migration method introduces a downtime. Also you can only reverse it by restoring the old cluster from the backup. See [other migration methods](update.md) if you need lower downtime and a roll back plan.

## Prepare v1 cluster for the migration

1. Remove all replicas from the cluster, keeping only primary running. It is required to assure that primary PVC volume does not change.
    
    ```yaml
    pgReplicas:
        hotStandby:
          size: 0
    ```

2. Apply the custom resource.

    ```{.bash data-prompt="$"}
    $ kubectl apply -f cr.yaml
    ```

3. When all replicas are gone, proceed with removing the cluster. Double check that `spec.keepData` is in place, otherwise the Operator will delete the volumes.

    ```{.bash data-prompt="$"}
    $ kubectl delete perconapgcluster cluster1
    ```

4. Find PVC for the primary and `pgBackRest`:

    ```{.bash data-prompt="$"}
    $ kubectl get pvc --selector=pg-cluster=cluster1 -n pgo
    ```

    ??? example "Expected output"

        ```{.text .no-copy}
        NAME                 STATUS   VOLUME                                     CAPACITY   ACCESS MODES   STORAGECLASS   AGE
        cluster1             Bound    pvc-940cdc23-cd4c-4f62-ac3a-dc69850042b0   1Gi        RWO            standard-rwo   57m
        cluster1-pgbr-repo   Bound    pvc-afb00490-5a45-45cb-a1cb-10af8e48bb13   1Gi        RWO            standard-rwo   57m
        ```

       A third PVC used to store write-ahead logs (WAL) may also be present if external WAL volumes were enabled for the cluster.


## Execute the migration to v2

The old cluster is shut down, the volumes are ready to be used to provision the new cluster managed by Operator v2.

1. To list the claims belonging to the old cluster run the following command:

    ```{.bash data-prompt="$"}
    $ kubectl get pvc --selector=pg-cluster=cluster1 -n pgo
    ```

    ??? example "Expected output"

        ```{.text .no-copy}
        NAME                 STATUS   VOLUME                                     CAPACITY   ACCESS MODES   STORAGECLASS   AGE
        cluster1             Bound    pvc-db9bf618-04d5-4807-948d-e32e81098575   1Gi        RWO            standard-rwo   87m
        cluster1-pgbr-repo   Bound    pvc-37d93aa9-bf02-4295-bbbc-c1f834ed6045   1Gi        RWO            standard-rwo   87m
        ```

2. In the custom resource manifest for v2 cluster, change `dataSource.volumes` fields where they point to the PVCs of the v1 cluster:

    ```yaml
    dataSource:
      volumes:
          pgDataVolume:
            pvcName: cluster1
            directory: cluster1
          pgBackRestVolume:
            pvcName: cluster1-pgbr-repo
            directory: cluster1-backrest-shared-repo
    ```

3. Apply the manifest:

    ```{.bash data-prompt="$"}
    $ kubectl apply -f cr.yaml
    ```

The new cluster will be provisioned shortly using the volume of the v1 cluster. You should remove the `spec.datasource.volumes` section from your manifest.
