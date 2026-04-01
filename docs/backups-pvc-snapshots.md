# PVC snapshot support

!!! note "" 

    This feature is in the tech preview stage. The API and behavior may change in future releases.

This document provides an overview of PVC snapshots. If you are familiar with the concept and want to try it out, jump to the [Configure and use PVC snapshots](backups-pvc-setup.md) tutorial. If you run on Amazon EKS, start with [Set up PVC snapshots on EKS](backups-pvc-setup-eks.md). 

By reading this document you will learn the following:

- [PVC snapshot support](#pvc-snapshot-support)
    - [Overview](#overview)
    - [Workflow](#workflow)
    - [Why to use PVC snapshots](#why-to-use-pvc-snapshots)
    - [Requirements](#requirements)
    - [Limitations](#limitations)

## Overview

A PVC snapshot is a point-in-time copy of a [Persistent Volume Claim :octicons-link-external-16:](https://kubernetes.io/docs/concepts/storage/persistent-volumes/) created by the storage provider. It captures the volume contents at a specific moment without copying data block by block. 

PVC snapshots are much faster than streaming data to cloud storage or a backup volume. This is especially beneficial for large datasets. The Operator uses the [Kubernetes VolumeSnapshot API :octicons-link-external-16:](https://kubernetes.io/docs/concepts/storage/volume-snapshots/) to create PVC snapshots at the storage level. When used with `pgBackRest` WAL archiving, PVC snapshots ensure data consistency and provide support for point-in-time recovery.


## Workflow

The Operator currently supports only cold backups (the `offline` mode). 
A cold backup is also known as an offline backup. 
It is a storage-level backup taken from a PostgreSQL replica instance after it is temporarily suspended by the Operator.
This ensures consistency by capturing the entire database exactly as it exists at the moment when the replica is temporarily suspended.

During cold backups, the Operator:

1. Selects a **replica** instance as the snapshot target.
2. Issues a PostgreSQL `CHECKPOINT` on that replica (if checkpoint is enabled).
3. **Suspends** the replica StatefulSet (scales it to zero).
4. Creates Kubernetes `VolumeSnapshot` objects for the data PVC, WAL PVC (if separate), and any tablespace PVCs.
5. Waits for all snapshots to become `ReadyToUse`.
6. **Resumes** the replica StatefulSet.

This approach ensures a crash-consistent snapshot while minimizing the impact on the primary. Only a replica is taken offline, so the cluster continues serving read/write traffic on the primary during the snapshot.

## Why to use PVC snapshots

PVC snapshots speed up backups and restores, which is especially beneficial for large data sets. With this feature, you get:

* **Much faster backups** – Snapshot creation is typically seconds to minutes, regardless of database size. Time it takes to run traditional full backups increases as the size of your database grows.
* **Much faster restores** – Restoring from a snapshot is significantly faster than restoring from cloud storage. Both in-place restores and restores to a new cluster are supported.
* **Lower resource usage** – Snapshots avoid the CPU and network overhead of streaming data to a remote storage.

## Requirements

Before enabling PVC snapshots, ensure the following:

1. Your Kubernetes cluster must have the CSI driver that supports VolumeSnapshot API. An example of such driver for GKE is `pd.csi.storage.gke.io`, for EKS - `ebs.csi.aws.com`.

2. Your Kubernetes cluster must have the VolumeSnapshot CRDs installed. Verify if they are installed with this command:
    
    ```bash
    kubectl get crd volumesnapshots.snapshot.storage.k8s.io
    ```

    !!! example "Expected output"

        `volumesnapshotclasses.snapshot.storage.k8s.io`
        `volumesnapshotcontents.snapshot.storage.k8s.io`
        `volumesnapshots.snapshot.storage.k8s.io`

2. At least one `VolumeSnapshotClass` must exist and be compatible with the storage class used by your PostgreSQL data volumes. Check it with:

   ```bash
   kubectl get volumesnapshotclasses
   ```

   See how to add it in the [Add a VolumeSnapshotClass](backups-pvc-setup.md#add-a-volumesnapshotclass) section.

3. You must explicitly enable the `BackupSnapshots` feature gate in the Operator Deployment. See [Enable the feature gate](backups-pvc-setup.md#enable-the-feature-gate).
5. You must explicitly specify the storage class whose CSI driver supports VolumeSnapshot API in the `spec.instances.[]dataVolumeClaimSpec.storageClassName` option in the Custom Resource for your cluster.

## Limitations

* **Currently only offline mode** – Only offline snapshots are supported; the Operator must stop a replica pod to take a consistent snapshot of the database.
* **At least one replica required** – Your cluster must have at least one replica pod besides the primary. The Operator takes the snapshot from a replica; clusters without replicas cannot use this feature.
* **CSI driver support required** — your Kubernetes cluster’s storage provisioner
must support the Volume Snapshot API.
* **One snapshot backup at a time** – You can only run one snapshot backup at a time on a given cluster; concurrent snapshot backups are not supported.
* **No automatic retention policy for scheduled backups yet** - You must manually delete outdated backup objects. Retention policy is planned to be added in future releases.
* **No automatic retention policy for scheduled backups yet** – You need to manually remove outdated backup objects for now. Automatic retention will be available in a future release.

[Configure PVC snapshots](backups-pvc-setup.md){.md-button}

