# Versions compatibility

Versions of the cluster components and platforms tested with different Operator releases are shown below. Other version combinations may also work but have not been tested.

Cluster components:

| Operator | [PostgreSQL :octicons-link-external-16:](https://www.postgresql.org/) | [pgBackRest :octicons-link-external-16:](https://pgbackrest.org/) | [pgBouncer :octicons-link-external-16:](http://pgbouncer.github.io/) |
|:---------|:--------|:-----|:-------|
| [2.3.1](ReleaseNotes/Kubernetes-Operator-for-PostgreSQL-RN2.3.1.md) | 12 - 16 | 2.48 | 1.18.0 |
| [2.3.0](ReleaseNotes/Kubernetes-Operator-for-PostgreSQL-RN2.3.0.md) | 12 - 16 | 2.48 | 1.18.0 |
| [2.2.0](ReleaseNotes/Kubernetes-Operator-for-PostgreSQL-RN2.2.0.md) | 12 - 15 | 2.43 | 1.18.0 |
| [2.1.0](ReleaseNotes/Kubernetes-Operator-for-PostgreSQL-RN2.1.0.md) | 12 - 15 | 2.43 | 1.18.0 |
| [2.0.0](ReleaseNotes/Kubernetes-Operator-for-PostgreSQL-RN2.0.0.md) | 12 - 14 | 2.41 | 1.17.0 |
| [1.5.1](https://docs.percona.com/percona-operator-for-postgresql/1.0/ReleaseNotes/Kubernetes-Operator-for-PostgreSQL-RN1.5.1.html) | 12 - 14 | 2.47 | 1.20.0 |
| [1.5.0](https://docs.percona.com/percona-operator-for-postgresql/1.0/ReleaseNotes/Kubernetes-Operator-for-PostgreSQL-RN1.5.0.html) | 12 - 14 | 2.47 | 1.20.0 |
| [1.4.0](https://docs.percona.com/percona-operator-for-postgresql/1.0/ReleaseNotes/Kubernetes-Operator-for-PostgreSQL-RN1.4.0.html) | 12 - 14 | 2.43 | 1.18.0 |
| [1.3.0](https://docs.percona.com/percona-operator-for-postgresql/1.0/ReleaseNotes/Kubernetes-Operator-for-PostgreSQL-RN1.3.0.html) | 12 - 14 | 2.38 | 1.17.0 |
| [1.2.0](https://docs.percona.com/percona-operator-for-postgresql/1.0/ReleaseNotes/Kubernetes-Operator-for-PostgreSQL-RN1.2.0.html) | 12 - 14 | 2.37 | 1.16.1 |
| [1.1.0](https://docs.percona.com/percona-operator-for-postgresql/1.0/ReleaseNotes/Kubernetes-Operator-for-PostgreSQL-RN1.1.0.html) | 12 - 14 | 2.34 | 1.16.0 for PostgreSQL 12, <br> 1.16.1 for other versions |
| [1.0.0](https://docs.percona.com/percona-operator-for-postgresql/1.0/ReleaseNotes/Kubernetes-Operator-for-PostgreSQL-RN1.0.0.html) | 12 - 13 | 2.33 | 1.13.0 |

Platforms:

| Operator | [GKE :octicons-link-external-16:](https://cloud.google.com/kubernetes-engine)         | [EKS :octicons-link-external-16:](https://aws.amazon.com)         | [Openshift :octicons-link-external-16:](https://www.redhat.com/en/technologies/cloud-computing/openshift) | [Minikube :octicons-link-external-16:](https://github.com/kubernetes/minikube)                          |
|:--------|:------------|:------------|:------------|:----------------------------------|
| [2.3.1](ReleaseNotes/Kubernetes-Operator-for-PostgreSQL-RN2.3.1.md) | 1.24 - 1.28 | 1.24 - 1.28 | 4.11.55 - 4.14.6 | 1.32   |
| [2.3.0](ReleaseNotes/Kubernetes-Operator-for-PostgreSQL-RN2.3.0.md) | 1.24 - 1.28 | 1.24 - 1.28 | 4.11.55 - 4.14.6 | 1.32   |
| [2.2.0](ReleaseNotes/Kubernetes-Operator-for-PostgreSQL-RN2.2.0.md) | 1.23 - 1.26 | 1.23 - 1.27 | -                | 1.30.1 |
| [2.1.0](ReleaseNotes/Kubernetes-Operator-for-PostgreSQL-RN2.1.0.md) | 1.23 - 1.25 | 1.23 - 1.25 | -                | -      |
| [2.0.0](ReleaseNotes/Kubernetes-Operator-for-PostgreSQL-RN2.0.0.md) | 1.22 - 1.25 |      -      | -                | -      |
| [1.5.1](https://docs.percona.com/percona-operator-for-postgresql/1.0/ReleaseNotes/Kubernetes-Operator-for-PostgreSQL-RN1.5.1.html) | 1.24 - 1.28 | 1.24 - 1.28 | 4.11 - 4.14 | 1.32 |
| [1.5.0](https://docs.percona.com/percona-operator-for-postgresql/1.0/ReleaseNotes/Kubernetes-Operator-for-PostgreSQL-RN1.5.0.html) | 1.24 - 1.28 | 1.24 - 1.28 | 4.11 - 4.14 | 1.32 |
| [1.4.0](https://docs.percona.com/percona-operator-for-postgresql/1.0/ReleaseNotes/Kubernetes-Operator-for-PostgreSQL-RN1.4.0.html) | 1.22 - 1.25 | 1.22 - 1.25 | 4.10 - 4.12 | 1.28 |
| [1.3.0](https://docs.percona.com/percona-operator-for-postgresql/1.0/ReleaseNotes/Kubernetes-Operator-for-PostgreSQL-RN1.3.0.html) | 1.21 - 1.24 | 1.20 - 1.22 | 4.7 - 4.10  | -    |
| [1.2.0](https://docs.percona.com/percona-operator-for-postgresql/1.0/ReleaseNotes/Kubernetes-Operator-for-PostgreSQL-RN1.2.0.html) | 1.19 - 1.22 | 1.19 - 1.21 | 4.7 - 4.10  | -    |
| [1.1.0](https://docs.percona.com/percona-operator-for-postgresql/1.0/ReleaseNotes/Kubernetes-Operator-for-PostgreSQL-RN1.1.0.html) | 1.19 - 1.22 | 1.18 - 1.21 | 4.7 - 4.9   | -    |
| [1.0.0](https://docs.percona.com/percona-operator-for-postgresql/1.0/ReleaseNotes/Kubernetes-Operator-for-PostgreSQL-RN1.0.0.html) | 1.17 - 1.21 | 1.21        | 4.6 - 4.8   | -    |

