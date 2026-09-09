# Scale Percona Distribution for PostgreSQL on Kubernetes

Kubernetes makes it straightforward to give a workload more capacity: you change the Custom Resource, and the Operator reconciles Pods, compute resources and storage to match.

Scaling can be vertical or horizontal:

* **Vertical scaling** adds CPU, memory, or disk to existing PostgreSQL members.
* **Horizontal scaling** adds more PostgreSQL members to the cluster.

Adding members can look similar to [high availability](ha-deploy.md), but the goals differ. Scaling is about capacity while high availability is about surviving failures. 

This document explains scaling. For failover, replication modes, and recommended cluster size, see [High availability](ha-deploy.md).

## Next steps

[Scale horizontally](scaling-horizontal.md){.md-button}
[Scale vertically](scaling-vertical.md){.md-button}
