# Deploy a standby cluster for Disaster Recovery

Disaster recovery is not optional for businesses operating in the digital age. With the ever-increasing reliance on data, system outages or data loss can be catastrophic, causing significant business disruptions and financial losses.

With multi-cloud or multi-regional PostgreSQL deployments, the complexity of managing disaster recovery only increases. This is where the Percona Operators come in, providing a solution to streamline disaster recovery for PostgreSQL clusters running on Kubernetes. With the Percona Operators, businesses can manage multi-cloud or hybrid-cloud PostgreSQL deployments with ease, ensuring that critical data is always available and secure, no matter what happens.

Operators automate routine tasks and remove toil. Percona Operator for PostgreSQL supports the following types of standby clusters:

1. A repo-based standby that recovers WAL files from a `pgBackRest` repo stored in external storage. For this setup, you reference the `pgBackRest` repo name and the cloud-based backup configuration that matches the one from the primary site. Refer to the [Standby cluster deployment based on pgBackRest](standby-backup.md) tutorial for the setup steps.
2. A streaming standby receives WAL files by connecting to the primary over the network. The primary site must be accessible over the network and allow secure authentication with TLS. The standby cluster must securely authenticate to the primary. For this reason, both sites must have the same custom TLS certificates. For the setup, you provide the host and port of the primary cluster and the certificates. Learn more about the setup in the [Standby cluster deployment based on streaming replication](standby-streaming.md) tutorial.
3. Streaming standby with external repository is the combination of two previous types and is configured with the options from both types. In this setup, the standby cluster streams WAL records from the primary. If the streaming replication falls behind, the cluster recovers WAL from the backup repo.

## Detect replication lag for standby cluster

If your primary cluster has a large volume of WAL files, the standby cluster may not be able to apply them quickly enough. This may cause the standby to fall behind. This lag can result in replication issues and temporarily leave some data unavailable on the standby cluster.

You can enable replication lag detection for any standby type by setting the [`standby.maxAcceptableLag`](operator.md#standbymaxacceptablelag) option in the Custom Resource. When the WAL lag exceeds this value, the following occurs:

* The primary pod in the standby cluster is marked as `Unready`
* The cluster goes into the `initializing` state
* The `StandbyLagging` condition is set in the cluster status. You can check the conditions with the `kubectl describe pg <cluster-name> -n <namespace>` command.

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
* Primary and standby are deployed in different namespaces and the Operator is installed in cluster-wide mode.


