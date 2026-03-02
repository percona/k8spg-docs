# Configure and use PVC snapshots

This document provides step-by-step instructions for configuring and using Persistent Volume Claim (PVC) Snapshots with Percona Operator for PostgreSQL on Kubernetes. 

For a high-level explanation of PVC snapshots, please refer to the [PVC snapshot support](backups-pvc-snapshots.md#overview) chapter.

## Prerequisites

To use PVC snapshots, ensure you have the following prerequisites met:

1. Your Kubernetes cluster must have a CSI driver that supports Volume Snapshots  
   For example, Google Kubernetes Engine (GKE) with `pd.csi.storage.gke.io`, or Amazon EKS with `ebs.csi.aws.com`. Check what driver you have with:

    ```bash
    kubectl get csidriver
    ```

2. Your Kubernetes cluster must have VolumeSnapshot CRDs installed. Most managed Kubernetes providers include these by default. Verify by running:

    ```bash
    kubectl get crd | grep volumesnapshots 
    ```

    ??? example "Expected output"

        ```{.text .no-copy}
        volumesnapshots.snapshot.storage.k8s.io
        ```

3. At least one `VolumeSnapshotClass` must exist and be compatible with the storage class used by your PostgreSQL data volumes. Check it with:

    ```bash
    kubectl get volumesnapshotclasses
    ```

    If you don't have one, you can add it yourself. Refer to the [Add a VolumeSnapshotClass](#add-volumesnapshotclass) section.

4. You must enable the `BackupSnapshots` feature gate for the **Percona Operator for PostgreSQL** deployment.  Refer to the [Enable the feature gate](#enable-the-feature-gate) section for details.

## Before you start

1. Check the [prerequisites](#prerequisites) and [limitations](backups-pvc-snapshots.md#limitations)
2. Clone the Operator repository to be able to edit manifests:

    ```bash
    git clone -b v{{release}} https://github.com/percona/percona-postgresql-operator
    ```

2. Export the namespace where you run your cluster as an environment variable:

    ```bash
    export NAMESPACE=<namespace>
    ```

## Configuration

### Enable the feature gate 

If you have the Operator Deployment up and running, you can edit the `deploy/operator.yaml` manifest. If you deploy the Operator from scratch, edit the `deploy/bundle.yaml` manifest.

1. Edit the `deploy/operator.yaml` or `deploy/bundle.yaml` and set the `PGO_FEATURE_GATES` environment variable for the Operator Deployment to `"BackupSnapshots=true"`:

    ```yaml
    spec:
      containers:
      - name: percona-postgresql-operator
        env:
        - name: PGO_FEATURE_GATES
          value: "BackupSnapshots=true"
    ```

2. Apply the configuration:

    ```bash
    kubectl apply -f deploy/operator.yaml -n $NAMESPACE
    ```

    or

    ```bash
    kubectl apply --server-side -f deploy/bundle.yaml -n $NAMESPACE
    ```

### Add a VolumeSnapshotClass

If your Kubernetes cluster doesn't have a `VolumeSnapshotClass` that matches your CSI driver, create one.

1. Create a VolumeSnapshotClass configuration file with the following configuration:

    ```yaml title="volume-snapshot-class.yaml"
    apiVersion: snapshot.storage.k8s.io/v1
    kind: VolumeSnapshotClass
    metadata:
      name: gke-snapshot-class
    driver: pd.csi.storage.gke.io
    deletionPolicy: Delete
    ```

2. Create the VolumeSnapshotClass resource:

    ```bash
    kubectl apply -f volume-snapshot-class.yaml
    ```

    ??? example "Expected output"

        ```{.text .no-copy}
        volumesnapshotclass.snapshot.storage.k8s.io/gke-snapshot-class created
        ```

### Configure PVC snapshots in your cluster

You must reference the `VolumeSnapshotClass` in your cluster Custom Resource.

1. Check the name of the `VolumeSnapshotClass` that works with your storage. You can list available classes with:

    ```bash
    kubectl get volumesnapshotclasses
    ```

    ??? example "Sample output"

        ```{.text .no-copy}
        NAME                 DRIVER                  DELETIONPOLICY   AGE
        gke-snapshot-class   pd.csi.storage.gke.io   Delete           42s
        ```

  2. Edit the `deploy/cr.yaml` Custom Resource and add the `volumeSnapshots` subsection under `backups`. Specify these keys:
  
      * `className` - the name of the `VolumeSnapshotClass`
      * `mode` -  how to make backups. `offile` is currently the only supported mode.

      ```yaml
      spec:
        backups:
          volumeSnapshots:
            className: <name-of-your-volume-snapshot-class>
            mode: offline
      ```

3. Apply the configuration to update the cluster:

    ```bash
    kubectl apply -f deploy/cr.yaml -n $NAMESPACE
    ```

Once configured, snapshots are created automatically when you [make a manual on-demand backup](#make-an-on-demand-backup-from-a-pvc-snapshot) or when [a scheduled backup runs](#make-a-scheduled-snapshot-based-backup). 

## Use PVC snapshots

Once the PVC snapshots are configured, you can use them to make backups and restores. 

### Make an on-demand backup from a PVC snapshot

1. Configure the `PerconaPGBackup` object. Edit the `deploy/backup.yaml` manifest and specify the following keys:
    
    * `pgCluster` - the name of your cluster. Check it with the `kubectl get pg -n $NAMESPACE` command

    * `method` - the backup method. Specify `volumeSnapshot`.

    Here's the example configuration:

    ```yaml
    apiVersion: pgv2.percona.com/v2
    kind: PerconaPGBackup
    metadata:
      name: my-snapshot-backup
    spec:
      pgCluster: cluster1
      method: volumeSnapshot
    ```

2. Apply the configuration to start a backup:

    ```bash
    kubectl apply -f deploy/backup.yaml -n $NAMESPACE
    ```

3. Check the backup status:

    ```bash
    kubectl get pg-backup my-snapshot-backup -n $NAMESPACE
    ```

    ??? example "Sample output"

        ```text
        NAME      CLUSTER    REPO    DESTINATION   STATUS      TYPE   COMPLETED   AGE
        my-snapshot-backup                      cluster1   repo1                 Succeeded   volumeSnapshot   3m38s       3m53s
        ```

### Make a scheduled snapshot-based backup

1. Configure the backup schedule in your cluster Custom Resource. Edit the `deploy/cr.yaml` manifest. In the `schedule` key in the `volumeSnapshots` subsection under `backups`, specify the schedule in the Cron format for the snapshots to be made automatically. Your updated configuration should look like this:

    ```yaml
    apiVersion: pgv2.percona.com/v2
    kind: PerconaPGCluster
    metadata:
      name: my-cluster
    spec:
      backups:
        volumeSnapshots:
          className: my-snapshot-class
          mode: offline
          schedule: "0 3 * * *"   # Every day at 3:00 AM
    ```

2. Apply the configuration to update the cluster:

    ```bash
    kubectl apply -f deploy/cr.yaml -n $NAMESPACE
    ```

### In-place restore from a PVC snapshot

An in-place restore is a restore to the same cluster using the `PerconaPGRestore` custom resource. You can make a full in-place restore or a point-in-time restore. 

When you create the `PerconaPGRestore` object, the Operator performs the following steps:

1. Suspends all instances in the cluster.
2. Deletes all existing PVCs in the cluster. This removes all existing data, WAL, and tablespaces.
3. Creates new PVCs with the snapshot serving as the data source. This restores the data, WAL, and tablespaces from that snapshot.
4. Spins up a job to configure the restored PVCs to be used by the cluster. 
5. Resumes all instances in the cluster. The cluster starts with the data from the snapshot.

!!! important

    An in-place restore overwrites the current data and is destructive. Any data that was written after the backup was made is lost. Therefore, consider restoring to a new cluster instead. This way you can evaluate the data before switching to the new cluster and don't risk losing data in the existing cluster.

Follow the steps below to make a full in-place restore from a PVC snapshot.

1. Configure the `PerconaPGRestore` object. Edit the `deploy/restore.yaml` manifest and specify the following keys:

    * `pgCluster` - the name of your cluster. Check it with the `kubectl get pg -n $NAMESPACE` command

    * `volumeSnapshotBackupName` - the name of the PVC snapshot backup. Check it with the `kubectl get pg-backup -n $NAMESPACE` command.

    Here's the example configuration:

    ```yaml
    apiVersion: pgv2.percona.com/v2
    kind: PerconaPGRestore
    metadata:
      name: restore1
    spec:
      pgCluster: cluster1
      volumeSnapshotBackupName: my-snapshot-backup
    ```

2. Apply the configuration to start a restore:

    ```bash
    kubectl apply -f deploy/restore.yaml -n $NAMESPACE
    ```

3. Check the restore status:

    ```bash
    kubectl get pg-restore restore1 -n $NAMESPACE
    ```

    ??? example "Sample output"

        ```text
        NAME         CLUSTER      STATUS      COMPLETED              AGE
        restore1     cluster1     Succeeded   2026-02-16T11:00:00Z   2m20s
        ```

### In-place restore with point-in-time recovery

You can make a point-in-time restore from a PVC snapshot and replay WAL files from a WAL archive made with pgBackRest. For this scenario, your cluster must meet the following requirements:

1. Have a `pgBackRest` configuration, including the backup storage and at least one repository. See the [Configure backup storage](backups-storage.md) section for configuration steps.
2. The repository must have at least one WAL archive.

The workflow for point-in-time restore is similar to [a full in-place restore](#in-place-restore-from-a-pvc-snapshot). After the Operator restores the data from the snapshot, it replays the WAL files from the WAL archive to bring the cluster to the target time.

!!! important

    An in-place restore overwrites the current data and is destructive. Any data that was written after the backup was made is lost. Therefore, consider restoring to a new cluster instead. This way you can evaluate the data before switching to the new cluster and don't risk losing data in the existing cluster.

Follow the steps below to make a point-in-time restore from a PVC snapshot.

1. Check the repo name and the target time for the restore. 

    * List the backups:
    
       ```bash
       kubectl get pg-backup -n $NAMESPACE
       ```

    * For a `pgBackRest` backup run the following command to get the target time:

       ```bash
       kubectl get pg-backup <backup_name> -n $NAMESPACE -o jsonpath='{.status.latestRestorableTime}'
       ```

2. Configure the `PerconaPGRestore` object. Edit the `deploy/restore.yaml` manifest and specify the following keys:

    * `pgCluster` - the name of your cluster. Check it with the `kubectl get pg -n $NAMESPACE` command

    * `volumeSnapshotBackupName` - the name of the PVC snapshot backup. 

    * `repoName` - the name of the pgBackRest repository that contains the WAL archives. 

    * `options` - the options for the restore. Specify the following options:

        * `--type=time` - set to `time` to make a point-in-time restore.
        * `--target` - set the target time for the restore. 

    Here's the example configuration:

    ```yaml
    apiVersion: pgv2.percona.com/v2
    kind: PerconaPGRestore
    metadata:
      name: pitr-restore
    spec:
      pgCluster: cluster1
      volumeSnapshotBackupName: my-snapshot-backup
      repoName: repo1
      options:
        - --type=time
        - --target="2026-02-16T11:00:00Z"
    ```

3. Apply the configuration to start a restore:

    ```bash
    kubectl apply -f deploy/restore.yaml -n $NAMESPACE
    ```

4. Check the restore status:

    ```bash
    kubectl get pg-restore pitr-restore -n $NAMESPACE
    ```

### Create a new cluster from a PVC snapshot

You can create a new cluster from a PVC snapshot. This is useful when you want to restore the data to a new cluster and don't want to overwrite the existing data in the existing cluster.

To create a new cluster from a PVC snapshot, you need to configure the `PerconaPGCluster` object and specify an `volumesnapshot` object as the `dataSource`. You also need to configure the `instances` and `backups` sections to set up the new cluster. 

For more information about the `dataSource` options, see the [Understand the `dataSource` options](backups-clone.md#understand-the-datasource-options) section. Also check the [Custom Resource reference](operator.md#datasource-subsection) for all available options.

Follow the steps below to create a new cluster from a PVC snapshot.

1. Create the namespace where a new cluster will be deployed and export it as the environment variable:

    ```bash
    kubectl create namespace <new-namespace>
    export NEW_NAMESPACE=<new-namespace>
    ```

2. Configure the `PerconaPGCluster` object. Edit the `deploy/cr.yaml` manifest and specify the following keys:

    * `dataSource` - the name of the PVC snapshot backup. Check it with the `kubectl get pg-backup my-snapshot-backup -o jsonpath='{.status.snapshot.dataVolumeSnapshotRef}'` command on the **source** cluster.

    * `instances` - the instances configuration for the new cluster.

    * `backups` - the backups configuration for the new cluster.

    Here's the example configuration:

    ```yaml
    apiVersion: pgv2.percona.com/v2
    kind: PerconaPGCluster
    metadata:
      name: new-cluster
    spec:
      instances:
        - name: instance1
          replicas: 3
          dataVolumeClaimSpec:
            accessModes:
              - ReadWriteOnce
            resources:
              requests:
                storage: 10Gi
      dataSource:
        apiGroup: snapshot.storage.k8s.io
        kind: VolumeSnapshot
        name: <name-of-the-pvc-snapshot-backup>
    ```

3. Apply the configuration to create the new cluster:

    ```bash
    kubectl apply -f deploy/cr.yaml -n $NEW_NAMESPACE
    ```

The new cluster will be provisioned shortly using the volume of the source cluster.

