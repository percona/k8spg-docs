# Disaster recovery for PostgreSQL on Kubernetes

Disaster recovery is not optional for businesses operating in the digital age. With the ever-increasing reliance on data, system outages or data loss can be catastrophic, causing significant business disruptions and financial losses.

With multi-cloud or multi-regional PostgreSQL deployments, the complexity of managing disaster recovery only increases. This is where the Percona Operators come in, providing a solution to streamline disaster recovery for PostgreSQL clusters running on Kubernetes. With the Percona Operators, businesses can manage multi-cloud or hybrid-cloud PostgreSQL deployments with ease, ensuring that critical data is always available and secure, no matter what happens.


## Solution overview

Operators automate routine tasks and remove toil. For standby, the [Percona Operator for PostgreSQL version 2](https://docs.percona.com/percona-operator-for-postgresql/2.0/index.html) provides the following options:

1. pgBackrest repo based standby
2. Streaming replication
3. Combination of (1) and (2)

This document describes the pgBackRest repo-based standby as the simplest one. The following is the architecture diagram:

![image]()

1. This solution describes two Kubernetes clusters in different regions, clouds or running in hybrid mode (on-premises and cloud). One cluster is Main and the other is Disaster Recovery (DR)

2. Each cluster includes the following components:

   1. Percona Operator
   2. PostgreSQL cluster
   3. pgBackrest
   4. pgBouncer

3. pgBackrest on the Main site streams backups and Write Ahead Logs (WALs) to the object storage

4. pgBackrest on the DR site takes these backups and streams them to the standby cluster



