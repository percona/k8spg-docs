# Deploy a standby cluster for Disaster Recovery

Disaster recovery is not optional for businesses operating in the digital age. With the ever-increasing reliance on data, system outages or data loss can be catastrophic, causing significant business disruptions and financial losses.

With multi-cloud or multi-regional PostgreSQL deployments, the complexity of managing disaster recovery only increases. This is where the Percona Operators come in, providing a solution to streamline disaster recovery for PostgreSQL clusters running on Kubernetes. With the Percona Operators, businesses can manage multi-cloud or hybrid-cloud PostgreSQL deployments with ease, ensuring that critical data is always available and secure, no matter what happens.

Operators automate routine tasks and remove toil. Percona Operator for PostgreSQL supports the following types of standby clusters:

1. A repo-based standby that recovers WAL files from a `pgBackRest` repo stored in external storage. For this setup, you reference the `pgBackRest` repo name and the cloud-based backup configuration that matches the one from the primary site. Refer to the [Standby cluster deployment based on pgBackRest](standby-backup.md) tutorial for the setup steps.
2. A streaming standby receives WAL files by connecting to the primary over the network. The primary site must be accessible over the network and allow secure authentication with TLS. The standby cluster must securely authenticate to the primary. For this reason, both sites must have the same custom TLS certificates. For the setup, you provide the host and port of the primary cluster and the certificates. Learn more about the setup in the [Standby cluster deployment based on streaming replication](standby-streaming.md) tutorial.
3. Streaming standby with external repository is the combination of two previous types and is configured with the options from both types. In this setup, the standby cluster streams WAL records from the primary. If the streaming replication falls behind, the cluster recovers WAL from the backup repo.
