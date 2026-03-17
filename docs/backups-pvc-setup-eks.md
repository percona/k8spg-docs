# Configure PVC snapshots on Amazon EKS

This tutorial walks you through setting up PVC snapshots for Percona Operator for PostgreSQL on Amazon Elastic Kubernetes Service (EKS). EKS has specific requirements that differ from other Kubernetes providers such as GKE.

For a high-level explanation of PVC snapshots, see the [PVC snapshot support](backups-pvc-snapshots.md#overview) chapter. 

## Prerequisites

To proceed with the setup, ensure you have:

* An EKS cluster (or plan to create one)
* `kubectl` configured to access your cluster
* The AWS CLI installed and configured

EKS requires specific addons, a gp3 storage class, and a matching VolumeSnapshotClass before you can use PVC snapshots.

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

### Enable required EKS addons

EKS requires two addons for volume snapshots: the Amazon EBS CSI driver and the snapshot controller. You can enable them when you create the cluster or add them to an existing cluster.

#### Option A: Add addons when creating the cluster

If you deploy the cluster with eksctl or a similar tool, include these addons in your cluster configuration:

```yaml
addons:
  - name: aws-ebs-csi-driver
    wellKnownPolicies:
      ebsCSIController: true
  - name: snapshot-controller
nodeGroups:
  - name: ng-1
    desiredCapacity: 3
    minSize: 3
    maxSize: 3
```

#### Option B: Add addons to an existing cluster

If your cluster already exists, enable the addons with the AWS CLI:

```bash
aws eks create-addon \
  --cluster-name <CLUSTER_NAME> \
  --addon-name aws-ebs-csi-driver \
  --resolve-conflicts OVERWRITE

aws eks create-addon \
  --cluster-name <CLUSTER_NAME> \
  --addon-name snapshot-controller
```

Replace `<CLUSTER_NAME>` with the name of your EKS cluster.

### Create a gp3 storage class

The default `gp2` storage class on EKS doesn't support volume snapshots. You must use `gp3` instead.

1. Create a storage class configuration file:

    ```yaml title="ebs-gp3-storage-class.yaml"
    apiVersion: storage.k8s.io/v1
    kind: StorageClass
    metadata:
      name: ebs-csi-gp3
    provisioner: ebs.csi.aws.com
    volumeBindingMode: WaitForFirstConsumer
    allowVolumeExpansion: true
    parameters:
      type: gp3
    ```

2. Apply the storage class:

    ```bash
    kubectl apply -f ebs-gp3-storage-class.yaml 
    ```

### Create a VolumeSnapshotClass

1. Create a VolumeSnapshotClass configuration file:

    ```yaml title="ebs-gp3-snapshot-class.yaml"
    apiVersion: snapshot.storage.k8s.io/v1
    kind: VolumeSnapshotClass
    metadata:
      name: ebs-csi-gp3
    driver: ebs.csi.aws.com
    deletionPolicy: Delete
    ```

2. Apply the VolumeSnapshotClass:

    ```bash
    kubectl apply -f ebs-gp3-snapshot-class.yaml
    ```

    ??? example "Expected output"

        ```{.text .no-copy}
        volumesnapshotclass.snapshot.storage.k8s.io/ebs-csi-gp3 created
        ```

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

#### Configure PVC snapshots in your cluster

You must reference the `VolumeSnapshotClass` in your cluster Custom Resource.

1. Check the name of the `VolumeSnapshotClass` that works with your storage. You can list available classes with:

    ```bash
    kubectl get volumesnapshotclasses
    ```

2. Edit the `deploy/cr.yaml` Custom Resource and add the `volumeSnapshots` subsection under `backups`. Specify these keys:
  
    * `className` - the name of the `VolumeSnapshotClass`
    * `mode` -  how to make backups. `offline` is currently the only supported mode.

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

Once configured, snapshots are created automatically when you [make a manual on-demand backup](backups-pvc-usage.md#make-an-on-demand-backup-from-a-pvc-snapshot) or when [a scheduled backup runs](backups-pvc-usage.md#make-a-scheduled-snapshot-based-backup).

