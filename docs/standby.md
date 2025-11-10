# How to deploy a standby cluster for Disaster Recovery

Disaster recovery is not optional for businesses operating in the digital age. With the ever-increasing reliance on data, system outages or data loss can be catastrophic, causing significant business disruptions and financial losses.

With multi-cloud or multi-regional PostgreSQL deployments, the complexity of managing disaster recovery only increases. This is where the Percona Operators come in, providing a solution to streamline disaster recovery for PostgreSQL clusters running on Kubernetes. With the Percona Operators, businesses can manage multi-cloud or hybrid-cloud PostgreSQL deployments with ease, ensuring that critical data is always available and secure, no matter what happens.

Operators automate routine tasks and remove toil. For standby, the [Percona Operator for PostgreSQL version 2](index.md) provides the following options:

1. [pgBackrest repo based standby](standby-backup.md). The standby cluster will be connected to a pgBackRest cloud repo, so it will receive WAL files from the repo and apply them to the database.
2. [Streaming replication](standby-streaming.md). The standby cluster will use an authenticated network connection to the primary cluster to receive WAL records directly.
3. Combination of (1) and (2). The standby cluster is configured for both repo-based standby and streaming replicaton. It bootstraps from the pgBackRest repo and continues to receive WAL files as they are pushed to the repo, and can also directly receive them from primary. Using this approach ensures the cluster will still be up to date with the pgBackRest repo if streaming falls behind.
