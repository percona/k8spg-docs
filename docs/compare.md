# Compare various solutions to deploy PostgreSQL in Kubernetes

There are multiple ways to deploy and manage PostgreSQL in Kubernetes. Here we will focus on comparing the following open source solutions:

* [Crunchy Data PostgreSQL Operator (PGO)](https://github.com/CrunchyData/postgres-operator)
* [CloudNative PG](https://github.com/cloudnative-pg/cloudnative-pg) from Enterprise DB 
* [Stackgres](https://github.com/ongres/stackgres) from OnGres
* [Zalando Postgres Operator](https://github.com/zalando/postgres-operator)
* [Percona Operator for PostgreSQL](https://github.com/percona/percona-postgresql-operator/)

## Generic

| Feature/Product        |     Percona Operator for PostgreSQL    |          Stackgres          |                     CrunchyData                     |     CloudNativePG (EDB)     | Zalando |
|------------------------|:---------------------------:|:---------------------------:|:---------------------------------------------------:|:---------------------------:|:-------:|
| Open-source license    |          Apache 2.0         |            AGPL 3           | Apache 2.0, but images are under Developer Program  |          Apache 2.0         |   MIT   |
| PostgreSQL versions    |          12, 13, 14         |              14             |                      12, 13, 14                     |     11 - 14, 15 in Beta     | 11 - 14 |
| Kubernetes conformance | Various versions are tested | Various versions are tested |             Various versions are tested             | Various versions are tested | AWS EKS |

## Maintenance

| Feature/Product  |   Percona Operator for PostgreSQL   |        Stackgres        |       CrunchyData       |   CloudNativePG (EDB)   |            Zalando            |
|------------------|:-----------------------:|:-----------------------:|:-----------------------:|:-----------------------:|:-----------------------------:|
| Operator upgrade |           Yes           |           Yes           |           Yes           |           Yes           |              Yes              |
| Database upgrade |    Automated and safe   |          Manual         |          Manual         |          Manual         |             Manual            |
| Compute scaling  | Horizontal and vertical | Horizontal and vertical | Horizontal and vertical | Horizontal and vertical |    Horizontal and vertical    |
| Storage scaling  |          Manual         |          Manual         |          Manual         |          Manual         | Manual, automated for AWS EBS |

## PostgreSQL topologies

| Feature/Product    | Percona Operator for PostgreSQL | Stackgres | CrunchyData | CloudNativePG (EDB) | Zalando |
|--------------------|:-------------------:|:---------:|:-----------:|:-------------------:|:-------:|
| Warm standby       |         Yes         |    Yes    |     Yes     |         Yes         |   Yes   |
| Hot standby        |         Yes         |    Yes    |     Yes     |         Yes         |   Yes   |
| Connection pooling |         Yes         |    Yes    |     Yes     |         Yes         |   Yes   |
| Delayed replica    |          No         |     No    |      No     |          No         |    No   |
| Tablespaces        |         Yes         |     No    |     Yes     |          No         |    No   |

## Backups

| Feature/Product   | Percona Operator for PostgreSQL | Stackgres | CrunchyData | CloudNativePG (EDB) | Zalando |
|-------------------|:-------------------------------:|:---------:|:-----------:|:-------------------:|:-------:|
| Scheduled backups |               Yes               |    Yes    |     Yes     |         Yes         |   Yes   |
| WAL archiving     |               Yes               |    Yes    |     Yes     |         Yes         |   Yes   |
| PITR              |               Yes               |    Yes    |     Yes     |         Yes         |   Yes   |
| GCS               |               Yes               |    Yes    |     Yes     |         Yes         |   Yes   |
| S3                |               Yes               |    Yes    |     Yes     |         Yes         |   Yes   |
| Azure             |                No               |    Yes    |     Yes     |         Yes         |   Yes   |

## Monitoring

| Feature/Product |  Percona Operator for PostgreSQL  |               Stackgres               |           CrunchyData          |          CloudNativePG (EDB)          |  Zalando |
|-----------------|:---------------------------------:|:-------------------------------------:|:------------------------------:|:-------------------------------------:|:--------:|
| Solution        | Percona Monitoring and Management | Exposing metrics in Prometheus format | Prometheus stack and pgMonitor | Exposing metrics in Prometheus format | Sidecars |

## Miscellaneous

| Feature/Product                    | Percona Operator for PostgreSQL |       Stackgres       |      CrunchyData      |  CloudNativePG (EDB)  |        Zalando        |
|------------------------------------|:-------------------------------:|:---------------------:|:---------------------:|:---------------------:|:---------------------:|
| Customize PostgreSQL configuration |               Yes               |          Yes          |          Yes          |          Yes          |          Yes          |
| Helm                               |               Yes               |          Yes          |          Yes          |          Yes          |          Yes          |
| Transport encryption               |               Yes               |          Yes          |          Yes          |          Yes          |                       |
| Data-at-rest encryption            |      Through storage class      | Through storage class | Through storage class | Through storage class | Through storage class |
| Create users/roles                 |           Yes, limited          |          Yes          |          Yes          |          Yes          |      Yes, limited     |
