# Configure and use PVC snapshots

This document provides step-by-step instructions for configuring and using Persistent Volume Claim (PVC) Snapshots with Percona Operator for PostgreSQL on Kubernetes. 

For a high-level explanation of PVC snapshots, please refer to the [PVC snapshot support](backups-pvc-snapshots.md#overview) chapter.

!!! note "Amazon EKS users"

    If you run your cluster on Amazon EKS, refer to the [Set up PVC snapshots on EKS](backups-pvc-setup-eks.md) tutorial. EKS requires specific addons, a gp3 storage class, and a matching VolumeSnapshotClass before you can use PVC snapshots.

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

    If you don't have one, you can add it yourself. Refer to the [Add a VolumeSnapshotClass](#add-a-volumesnapshotclass) section.

4. You must enable the `BackupSnapshots` feature gate for the **Percona Operator for PostgreSQL** deployment.  Refer to the [Enable the feature gate](#enable-the-feature-gate) section for details.

## Before you start

1. Check the [prerequisites](#prerequisites) and [limitations](backups-pvc-snapshots.md#limitations)
2. Clone the Operator repository to be able to edit manifests:

    ```bash
    git clone -b v{{release}} https://github.com/percona/percona-postgresql-operator
    ```

3. Export the namespace where you run your cluster as an environment variable:

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

    === "Google Kubernetes Engine (GKE)"

        ```yaml title="volume-snapshot-class.yaml"
        apiVersion: snapshot.storage.k8s.io/v1
        kind: VolumeSnapshotClass
        metadata:
          name: gke-snapshot-class
        driver: pd.csi.storage.gke.io
        deletionPolicy: Delete
        ```
    
    === "Microsoft Azure Kubernetes Service (AKS)"

        ```yaml title="volume-snapshot-class.yaml"
        apiVersion: snapshot.storage.k8s.io/v1
        kind: VolumeSnapshotClass
        metadata:
          name: aks-snapshot-class
        driver: disk.csi.azure.com
        deletionPolicy: Delete
        ```

    === "OpenShift"

        ```yaml title="volume-snapshot-class.yaml"
        apiVersion: snapshot.storage.k8s.io/v1
        kind: VolumeSnapshotClass
        metadata:
          name: openshift-snapshot-class
        driver: ebs.csi.aws.com
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

2. Edit the `deploy/cr.yaml` Custom Resource. Reference the Storage Class that supports the VolumeSnapshot API in the `spec.instances.[]dataVolumeClaimSpec.storageClassName` option. The Operator then uses this storage class when it creates the cluster.

    Here's the example configuration:

    ```yaml
    spec:
      instances:
      - name: instance1
        dataVolumeClaimSpec: 
          storageClassName: standard
          accessModes:
          - ReadWriteOnce
          resources:
            requests:
              storage: 1Gi
    ```
    
3. Edit the `deploy/cr.yaml` Custom Resource and add the `volumeSnapshots` subsection under `backups`. Specify these keys:
  
    * `className` - the name of the `VolumeSnapshotClass`
    * `mode` -  how to make backups. `offline` is currently the only supported mode.

    ```yaml
    spec:
      backups:
        volumeSnapshots:
          className: <name-of-your-volume-snapshot-class>
          mode: offline
    ```

4. Apply the configuration to update the cluster:

    ```bash
    kubectl apply -f deploy/cr.yaml -n $NAMESPACE
    ```

Once configured, snapshots are created automatically when you [make a manual on-demand backup](backups-pvc-usage.md#make-an-on-demand-backup-from-a-pvc-snapshot) or when [a scheduled backup runs](backups-pvc-usage.md#make-a-scheduled-snapshot-based-backup).



