# Architecture

This document provides a high-level overview of Percona Operator for PostgreSQL architecture, explaining how the various components connect to create a production-ready PostgreSQL cluster on Kubernetes. See also [How the Operator works](operator-how-it-works.md).

## Components 

The StatefulSet, deployed with the Operator includes the following components:

* [**Percona Distribution for PostgreSQL** :octicons-link-external-16:](https://docs.percona.com/postgresql/latest/index.html) - a suite of open source software, tools and services required to deploy and maintain a reliable production cluster for PostgreSQL. It includes the set of extensions such as  [pgAudit :octicons-link-external-16:](https://www.pgaudit.org/) for audit logging, [`pg_stat_monitor` :octicons-link-external-16:](https://docs.percona.com/pg-stat-monitor/index.html) for query performance statistics and [additional supplied modules and extensions :octicons-link-external-16:](https://www.postgresql.org/docs/current/contrib.html).
  
* [**Patroni** :octicons-link-external-16:](https://patroni.readthedocs.io/) - a high-availability solution for PostgreSQL that automates replication and **failover**. It maintains the cluster state and coordinates leader election to ensure that a healthy primary node is always available. Patroni simplifies building and operating resilient PostgreSQL clusters by handling node monitoring, failover, and recovery automatically. 

* [**pgBouncer** :octicons-link-external-16:](http://pgbouncer.github.io/) is a **lightweight connection pooler** in front of PostgreSQL. It sits between client applications and the database server to manage and reuse connections efficiently. Instead of each client opening its own database connection, pgBouncer maintains a pool of connections and serves them to clients on demand, significantly reducing connection overhead and improving performance, especially for applications with many short-lived or concurrent connections.

* [**pgBackRest** :octicons-link-external-16:](https://pgbackrest.org/) is a backup and restore tool. It handles **full, incremental, and differential** backups, compression and encryption, parallel processing, and point-in-time recovery using WAL archives. 
  
* LLVM (for JIT compilation).

![Operator overview](assets/images/pgo.svg)

### How components work together

This workflow shows how cluster components work together:

1. Your **application** uses a Kubernetes **Service** aimed at pgBouncer.
2. **pgBouncer** accepts many client connections and forwards work through a smaller set of server connections to PostgreSQL Pods.
3. **PostgreSQL** executes queries. **Writes** go to the **primary**. **Reads** can target the primary or **replicas**.
4. Primary streams WAL to replicas via instance Services
5. Patroni monitors the cluster state and coordinates the leader elections if the primary node fails
6. pgBackRest makes backups according the schedule that you defined or when you manually create a backup object. pgBackRest saves backups to the backup storage your configured. To learn more about backups, their workflow and setup, refer to the [About backups](backups.md)
7. PMM Client collects performance metrics and sends them to the PMM Server for you to see and analyze. See [Monitor the database with PMM](monitoring.md) to learn more.


## Default cluster configuration

The default Percona Distribution for PostgreSQL configuration includes:

* 3 PostgreSQL servers, one primary and two replicas.
* 3 pgBouncer instances.
* a pgBackRest repository host instance – a dedicated instance in your cluster that stores filesystem backups made with pgBackRest .
* a PMM client instance - a monitoring and management tool for PostgreSQL that provides a way to monitor and manage your database. It runs as a sidecar container in the database Pods.

### Primary, replicas, and high availability

Each PostgreSQL cluster has **one primary** instance that accepts read/write transactions. **Replicas** are standbys: they replicate from the primary and typically serve **read-only** traffic (depending on how you expose them).

The Operator provides high availability through multiple layers of protection:

#### Pod distribution

The Operator uses [node affinity and anti-affinity :octicons-link-external-16:](https://kubernetes.io/docs/concepts/configuration/assign-pod-node/#affinity-and-anti-affinity) to distribute PostgreSQL instances across separate worker nodes when possible. This prevents a single node failure from taking down multiple database instances.

#### Automatic recovery

If a node fails, Kubernetes automatically reschedules the affected Pod on another healthy node. Patroni handles which PostgreSQL instance is primary and ensures replication continuity. For more on HA behavior and operations, see [High-availability](ha-deploy.md).

## Storage and persistent volumes

Stateful workloads rely on durable disk. Kubernetes attaches storage through **PersistentVolumeClaims (PVCs)**; the cluster’s CSI driver provisions **PersistentVolumes** and can **reattach** storage if a Pod moves to another node (subject to your storage class and platform).

If a node fails, the expectation is that the volume can be mounted elsewhere and the Pod recreated, while Patroni and PostgreSQL recover the database layer. For storage troubleshooting, see [Check storage](debug-storage.md).

## Next steps 

For a comparison of Percona’s approach with other deployment models, see [Comparison with other solutions](compare.md).
