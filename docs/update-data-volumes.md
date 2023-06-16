# Upgrade using data volumes

## Prerequisites:

The following conditions should be met for the Volumes-based migration:

- You have a version 1.x cluster with `spec.keepData: true` in the Custom Resource
- You have both Operators deployed and allow them to control resources in the same namespace
- Old and new clusters must be of the same PostgreSQL major version

This migration method has two limitations. First of all, this migration method introduces a downtime. 
Also, you can only reverse such migration by restoring the old cluster from the backup. See [other migration methods](update.md) if you need lower downtime and a roll back plan.

## Prepare version 1.x cluster for the migration

1. Remove all Replicas from the cluster, keeping only primary running. It is required to assure that Volume of the primary [PVC](https://kubernetes.io/docs/concepts/storage/persistent-volumes/) does not change. The `deploy/cr.yaml` configuration file should have it as follows:
    
    ```yaml
    ...
    pgReplicas:
        hotStandby:
          size: 0
    ```

2. Apply the Custom Resource in a usual way:

    ```{.bash data-prompt="$"}
    $ kubectl apply -f deploy/cr.yaml
    ```

3. When all Replicas are gone, proceed with removing the cluster. Double check that `spec.keepData` is in place, otherwise the Operator will delete the volumes!

    ```{.bash data-prompt="$"}
    $ kubectl delete perconapgcluster cluster1
    ```

4. Find PVC for the Primary and `pgBackRest`:

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

5. Permissions for `pgBackRest` repo folders are managed differently in version 1 and version 2. We need to change the ownership of the `backrest` folder on the Persistent Volume to avoid errors during migration. Running a `chown` command within a container fixes this problem. 
    You can use the following manifest to execute it:

    ```yaml title="chown-pod.yaml"
    apiVersion: v1
    kind: Pod
    metadata:
      name: chown-pod
    spec:
      volumes:
        - name: backrestrepo
          persistentVolumeClaim:
            claimName: cluster1-pgbr-repo
      containers:
        - name: task-pv-container
          image: ubuntu
          command:
          - chown
          - -R
          - 26:26
          - /backrestrepo/cluster1-backrest-shared-repo
          volumeMounts:
            - mountPath: "/backrestrepo"
              name: backrestrepo
    ```
    
    Apply it as follows:
    
    ```{.bash data-prompt="$"}
    $ kubectl apply -f chown-pod.yaml -n pgo
    ```

## Execute the migration to vevsion 2.x

The old cluster is shut down, and Volumes are ready to be used to provision the new cluster managed by the Operator version 2.x.

1. Install the Operator version 2 (if not done yet). Pick your favorite method from [our documentaion](index.md).

2. Run the following command to show the names of PVC belonging to the old cluster:

    ```{.bash data-prompt="$"}
    $ kubectl get pvc --selector=pg-cluster=cluster1 -n pgo
    ```

    ??? example "Expected output"

        ```{.text .no-copy}
        NAME                 STATUS   VOLUME                                     CAPACITY   ACCESS MODES   STORAGECLASS   AGE
        cluster1             Bound    pvc-db9bf618-04d5-4807-948d-e32e81098575   1Gi        RWO            standard-rwo   87m
        cluster1-pgbr-repo   Bound    pvc-37d93aa9-bf02-4295-bbbc-c1f834ed6045   1Gi        RWO            standard-rwo   87m
        ```

3. Now edit the Custom Resource manifest (`deploy/cr.yaml` configuration file) of the version 2.x cluster: add fields to the `dataSource.volumes` subsection, pointing to the PVCs of the version 1.x cluster:

    ```yaml
    ...
    dataSource:
      volumes:
          pgDataVolume:
            pvcName: cluster1
            directory: cluster1
          pgBackRestVolume:
            pvcName: cluster1-pgbr-repo
            directory: cluster1-backrest-shared-repo
    ```

4. Apply the manifest:

    ```{.bash data-prompt="$"}
    $ kubectl apply -f deploy/cr.yaml
    ```

The new cluster will be provisioned shortly using the volume of the version 1.x cluster. You should remove the `spec.datasource.volumes` section from your manifest.
