# PVC snapshot support

!!! note "" 

    This feature is in the tech preview stage. The API and behavior may change in future releases.

This document provides an overview of PVC snapshots. If you are familiar with the concept and want to try it out, jump to the [Configure and use PVC snapshots](backups-pvc-setup.md) tutorial. 

By reading this document you will learn the following:

* [What is a PVC snapshot](#overview)
* [How it works](#workflow)
* [Why you need it](#why-to-use-pvc-snapshots)
* [Requirements](#requirements) 
* [Current limitations](#limitations)

## Overview

A PVC snapshot is a point-in-time copy of a [Persistent Volume Claim :octicons-link-external-16:](https://kubernetes.io/docs/concepts/storage/persistent-volumes/) created by the storage provider. It captures the volume contents at a specific moment without copying data block by block. 

PVC snapshots are much faster than streaming data to cloud storage or a backup volume. This is especially beneficial for large datasets. The Operator uses the [Kubernetes VolumeSnapshot API :octicons-link-external-16:](https://kubernetes.io/docs/concepts/storage/volume-snapshots/) to create PVC snapshots at the storage level. When used with pgBackRest WAL archiving, PVC snapshots ensure data consistency and provide support for point-in-time recovery.


## Workflow

The Operator currently supports only cold backups (the `offline` mode). 
A cold backup is also known as an offline backup. 
It is a physical base backup taken when the PostgreSQL instance is shut down. 
This ensures consistency by capturing the entire database exactly as it exists at the moment when it's shut down.

During cold backups, the Operator:

1. Selects a **replica** instance as the snapshot target.
2. Issues a PostgreSQL `CHECKPOINT` on that replica (if checkpoint is enabled).
3. **Suspends** the replica StatefulSet (scales it to zero).
4. Creates Kubernetes `VolumeSnapshot` objects for the data PVC, WAL PVC (if separate), and any tablespace PVCs.
5. Waits for all snapshots to become `ReadyToUse`.
6. **Resumes** the replica StatefulSet.

This approach ensures a crash-consistent snapshot while minimizing the impact on the primary. Only a replica is taken offline, so the cluster continues serving read/write traffic on the primary during the snapshot.

## Why to use PVC snapshots

PVC snapshots can speed up backups and restores, which is especially beneficial for large data sets. With this feature, you get:

* **Much faster backups** – Snapshot creation is typically seconds to minutes, regardless of database size. Traditional full backups scale with data volume and can take hours for large datasets.
* **Much faster restores** – Restoring from a snapshot is significantly faster than restoring from cloud storage. Both in-place restores and restores to a new cluster are supported.
* **Lower resource usage** – Snapshots avoid the CPU and network overhead of streaming data to remote storage.
* **PITR support** – When used with pgBackRest, snapshots integrate with point-in-time recovery for flexible restore targets.

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

   See how to add it in the [Add a VolumeSnapshotClass](#add-volumesnapshotclass) section.

3. You must explicitly enable the `VolumeSnapshots` feature gate in the Operator Deployment. See [Enable the feature gate](#enable-the-feature-gate).

## Limitations

* **Currently only offline mode** – Only offline snapshots are supported; the Operator must stop a replica pod to take a consistent snapshot of the database.
* **At least one replica required** – Your cluster must have at least one replica pod besides the primary. The Operator takes the snapshot from a replica; clusters without replicas cannot use this feature.
* **CSI driver support required** — your Kubernetes cluster’s storage provisioner
must support the Volume Snapshot API.
* **One snapshot backup at a time** – You can only run one snapshot backup at a time on a given cluster; concurrent snapshot backups are not supported.

[Configure PVC snapshots](backups-pvc-setup.md){.md-button}

