# Users

User accounts within the Cluster can be divided into two different groups:

* *application-level users*: the unprivileged user accounts,
* *system-level users*: the accounts needed to automate the cluster deployment
and management tasks.

## System Users

Credentials for system users are stored as a [Kubernetes Secrets](https://kubernetes.io/docs/concepts/configuration/secret/) object.
The Operator requires to be deployed before PostgreSQL Cluster is
started. The name of the required secrets (`cluster1-users` by default)
should be set in the `spec.secretsName` option of the `deploy/cr.yaml`
configuration file.

The following table shows system users’ names and purposes.

!!! warning

    These users should not be used to run an application.

The default PostgreSQL instance installation via the Percona Operator for PostgreSQL comes with the
following users:

| Role name          | Attributes                                                 |
|--------------------|------------------------------------------------------------|
| `postgres`         | Superuser, Create role, Create DB, Replication, Bypass RLS |
| `_crunchyrepl`     | Replication                                                |
| `cluster1`         | Non-privileged user                                        |
| `_crunchypgbouncer`| Administrative user for the [pgBouncer connection pooler](http://pgbouncer.github.io/) |

The `postgres` user will be the admin user for the database instance. The
`_crunchyrepl` is used for replication between primary and replicas. The
`cluster1` is the default non-privileged user and is always named after the name
of the cluster.

## Application users

By default you can connect to PostgreSQL as non-privileged `cluster1` user.
Also, you can login as `postgres` (the superuser) to PostgreSQL Pods,
but [pgBouncer](http://pgbouncer.github.io/) (the connection pooler for
PostgreSQL) doesn’t allow `postgres` user access by default. That’s done for
security reasons.
