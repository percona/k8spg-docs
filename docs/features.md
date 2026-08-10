# Features and capabilities

Percona Operator for PostgreSQL is a Kubernetes-native controller that automatically manages the full lifecycle of [Percona Distribution for PostgreSQL :octicons-link-external-16:](https://www.percona.com/software/postgresql-distribution) clusters. The Operator offloads your teams from manual day-to-day database management operations empowering them to focus on tasks that matter instead. To learn how the Operator fits into Kubernetes, see [Kubernetes Operator concepts](operator-concepts.md).

Here’s what Percona Operator for PostgreSQL brings to your infrastructure:

## High availability and failover

Run PostgreSQL with confidence: [Patroni :octicons-link-external-16:](https://patroni.readthedocs.io/) provides automatic leader election, failover, and coordination with Distributed Configuration Store, so your cluster stays available through node and Pod failures. For architecture details, see [Cluster architecture](architecture.md).

* **Automatic failover** — Patroni manages leader election and failover to ensure the cluster always has a healthy primary. See [High availability](ha-deploy.md).
* **Zero data loss failover** — WAL-based replication limits data loss during failover; synchronous replication is available when you need stronger guarantees.
* **Health monitoring** — Continuous health checks trigger failover when PostgreSQL is not ready to serve traffic.
* **Manual switchover** — [Promote a replica to primary](change-primary.md) in a controlled way for maintenance.

## Automated backup and restore flows

Safeguard your data at any scale: the Operator automates backups and restores using [pgBackRest :octicons-link-external-16:](https://pgbackrest.org/), a robust open source solution trusted for PostgreSQL in production. Read [About backups](backups.md) for the full workflow.

Also, leverage Kubernetes [PersistentVolumeClaim snapshots](backups-pvc-snapshots.md) for rapid, consistent backup and restore operations. It is especially valuable for large database clusters.

* **Full, incremental, and differential backups** — Select the backup strategy that matches your recovery objectives and storage requirements.
* **Point-in-time recovery (PITR)** — Achieve low Recovery Point Objectives (RPO) by [restoring to any specific time](backups-restore-inplace.md#restore-the-cluster-with-point-in-time-recovery) using WAL archives.
* **Scheduled backups** — Automate backups on your chosen [schedule with cron-like expressions](backups-schedule.md).
* **Flexible storage** — Store backups in S3-compatible object storage or on local PersistentVolumes for hybrid strategies.
* **PVC snapshot support** — Boost backup and restore performance for large datasets with a point-in-time snapshot of your data volume.
* **Encryption** — [Secure backups at rest](backup-encryption.md) where your storage backends and configuration allow it.
* **Retention** — Manage backup lifecycle and [automate old backup cleanup](backup-retention.md) to prevent storage sprawl.

## Connection pooling with pgBouncer

Reduce connection churn and spread read load without extra operational burden.

* **Efficient pooling** — Lower PostgreSQL connection overhead by pooling client connections
* **Transaction-level pooling** — Manage connections at the transaction level efficiently
* **Read balancing** — Distribute read queries across replicas where configured
* **High availability** — Replica pgBouncer instances provide high availability
* **Integrated lifecycle** — Automatically configured and managed by the Operator

## Automated scaling and resource management

Scale your cluster up or down to match demand while keeping changes declarative.

* **Declarative clusters** — Describe desired cluster state in YAML; the Operator automatically reconciles Kubernetes resources to match.
* **Replica scaling** — [Adjust replica count](scaling.md#understand-horizontal-scaling) in the Custom Resource to scale horizontally.
* **Dynamic configuration** — [Update PostgreSQL parameters](options.md) without a full cluster restart.
* **Self-healing** — The Operator automatically detects and recovers from Pod crashes, node issues, and common network problems.
* **Rolling updates** — Apply configuration and image updates with controlled rollouts.
* **Storage expansion** — Automatically [increase storage size](scaling.md#scale-storage) for PostgreSQL instances when supported by your environment and configuration.

## PostgreSQL-specific features

Use PostgreSQL capabilities that operators expect in production.

* **WAL storage** — Optional dedicated volumes for Write-Ahead Logs when you want to separate I/O.
* **Tablespaces** — Custom [tablespaces](tablespaces.md) with dedicated storage.
* **Extensions** — Built-in support for extensions such as pg_stat_monitor, pgAudit, set_user, wal2json, plus ability to extend PostgreSQL with [custom extensions](custom-extensions.md).
* **Users and databases** — Automatically create users, databases, and manage credentials.
* **Init SQL** — Execute [custom SQL scripts during cluster initialization](initsql.md).

## Standby clusters for disaster recovery

Leverage disaster-recovery topologies that fit your RTO and RPO.

* **Backups or streaming** — Deploy your standby cluster based on backups or streaming replication, depending on your architecture
* **Cross-namespace or cross-cluster** — Primary and standby clusters can run in different namespaces or Kubernetes clusters
* **Promotion** — Promote a standby to primary when you need to recover from an outage or drill a failover

## Security and compliance

Keep traffic and data protected with encryption and flexible TLS workflows.

* **TLS for connections** — Encrypt client traffic and traffic between cluster components
* **Certificates** — Comply with your security policy via [custom certificates](tls-manual.md) or automated certificate generation [with cert-manager](tls-cert-manager.md) with configurable lifecycle management.

## Monitoring and observability

Understand performance and troubleshoot faster with metrics and optional Percona tooling.

* **PMM integration** — Connect the cluster to [Percona Monitoring and Management (PMM) :octicons-link-external-16:](https://www.percona.com/software/database-tools/percona-monitoring-and-management) for dashboards and alerting.
* **pg_stat_monitor** — Get query performance insights with fingerprinting when you enable the extension.
* **Broad metrics** — Track connection counts, transaction rates, cache hit ratios, replication lag, and more.
* **Query analytics** — Deeper query analysis in PMM. See [Query Analytics :octicons-link-external-16:](https://docs.percona.com/percona-monitoring-and-management/3/use/qan/index.html#__tabbed_1_2) in the PMM documentation.

## Operator capabilities

Operate at the scale of your platform with flexible reconciliation scope.

* **Selective namespaces** — Reconcile clusters in a single namespace or multi-namespace mode. See [cluster-wide deployment](cluster-wide.md) to learn more.
* **Concurrent reconciliation** — Run [concurrent reconciliations](reconciliation-concurrency.md) to manage many clusters efficiently.
