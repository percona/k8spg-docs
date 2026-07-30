# Deploy a standby cluster for Disaster Recovery

A standby cluster is a special type of PostgreSQL cluster designed to maintain a continually updated, read-only copy of your primary PostgreSQL cluster. A standby cluster applies changes made on the primary cluster either through backups or streaming replication. This ensures you always have an up-to-date replica ready to take over if the primary becomes unavailable.

In disaster recovery scenarios, standby clusters are invaluable. They let you minimize downtime and data loss by quickly promoting the standby to a writable primary when needed. This is especially important in multi-cloud or multi-regional environments, where your PostgreSQL workloads may span across various platforms and geographies.

The Percona Operator for PostgreSQL makes it straightforward to deploy and manage standby clusters on Kubernetes. By automating complex tasks and integrating tightly with Kubernetes, the operator helps you protect critical data and achieve high availability, while simplifying your operational experience.

## Types of standby clusters

You can use the Percona Operator for PostgreSQL to set up several types of standby clusters, each suited to different recovery strategies:

1. A repo-based standby that recovers WAL files from a `pgBackRest` repo stored in external storage. For this setup, you reference the `pgBackRest` repo name and the cloud-based backup configuration that matches the one from the primary site. Refer to the [Standby cluster deployment based on pgBackRest](standby-backup.md) tutorial for the setup steps.
2. A streaming standby receives WAL files by connecting to the primary over the network. The primary site must be accessible over the network and allow secure authentication with TLS. The standby cluster must securely authenticate to the primary. For this reason, both sites must have the same custom TLS certificates. For the setup, you provide the host and port of the primary cluster and the certificates. Learn more about the setup in the [Standby cluster deployment based on streaming replication](standby-streaming.md) tutorial.
3. Streaming standby with external repository is the combination of two previous types and is configured with the options from both types. In this setup, the standby cluster streams WAL records from the primary. If the streaming replication falls behind, the cluster recovers WAL from the backup repo.

## Detect replication lag for standby cluster

If your primary cluster has a large volume of WAL files, the standby cluster may not be able to apply them quickly enough. This may cause the standby to fall behind. This lag can result in replication issues and temporarily leave some data unavailable on the standby cluster.

You can enable replication lag detection for any standby type by setting the [`standby.maxAcceptableLag`](operator.md#standbymaxacceptablelag) option in the Custom Resource. 

### How replication lag is detected and handled

The Operator checks the WAL source based on the standby type: from the primary site or from an external repository. 

For a standby cluster configured with both streaming and external repository, the Operator detects the replication lag as follows:

1. The Operator first attempts to check streaming replication lag.
2. If it fails to retrieve the streaming lag, the Operator falls back to checking the WAL replication lag from an external pgBackRest repository. Note the [known limitation for the repo-based standby](#known-limitation-for-a-repo-based-standby-cluster).
3. If streaming lag is successfully detected, this value is used.
   
When the WAL lag exceeds the value you specified in the `standby.maxAcceptableLag` option, the following occurs:

* The primary pod in the standby cluster is marked as `Unready`
* The cluster goes into the `initializing` state
* The `StandbyLagging` condition is set in the cluster status. You can check the conditions with the `kubectl describe pg <cluster-name> -n <namespace>` command. See [Custom resource statuses](cr-statuses.md#conditions) for the full list of conditions.

### Monitor lag in the cluster status

When lag detection is enabled, the cluster status includes a `standby` section that shows the current lag and when it was last computed. Use `kubectl get pg <cluster-name> -n <namespace> -o yaml` and look at `status.standby`:

```yaml
status:
  standby:
    lagBytes: 2343212
    lagLastComputedAt: "2026-02-24T12:07:05Z"
```

* `lagBytes` — the current WAL lag in bytes (if any)
* `lagLastComputedAt` — the timestamp of the last lag check

This helps you understand if replication is lagging or broken. By surfacing the standby lag condition, you get a clear signal when your standby is not ready to serve traffic, enabling faster troubleshooting and preventing application downtime during disaster recovery scenarios.

### Known limitation for a repo-based standby cluster

For WAL lag detection to work in this standby type, the Operator must have access to the primary cluster. Therefore, WAL lag detection is available in these setups:

* Primary and standby clusters are deployed in the same namespace
* Primary and standby are deployed in different namespaces of the same cluster and the Operator is installed in cluster-wide mode.

### Disable replication lag detection

To disable detecting the replication lag, remove the `standby.maxAcceptableLag` from the Custom Resource. The changes apply without restarting the database Pods.