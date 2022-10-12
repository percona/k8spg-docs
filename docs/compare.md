# Compare various solutions to deploy PostgreSQL in Kubernetes

There are multiple ways to deploy and manage PostgreSQL in Kubernetes. Here we will focus on comparing the following open source solutions:

* [Crunchy Data PostgreSQL Operator (PGO)](https://github.com/CrunchyData/postgres-operator)
* [CloudNative PG](https://github.com/cloudnative-pg/cloudnative-pg) from Enterprise DB 
* [Stackgres](https://github.com/ongres/stackgres) from OnGres
* [Zalando Postgres Operator](https://github.com/zalando/postgres-operator)
* [Percona Operator for PostgreSQL](https://github.com/percona/percona-postgresql-operator/)

## Generic

| Feature/Product        | Percona Operator for PostgreSQL |        Stackgres        |                     CrunchyData                     |     CloudNativePG (EDB)     | Zalando |
|------------------------|:---------------------------:|:---------------------------:|:---------------------------------------------------:|:---------------------------:|:-------:|
| Open-source license    |          Apache 2.0         |            AGPL 3           | Apache 2.0, but images are under Developer Program  |          Apache 2.0         |   MIT   |
| PostgreSQL versions    |          12, 13, 14         |              14             |                      12, 13, 14                     |     11 - 14, 15 in Beta     | 11 - 14 |
| Kubernetes conformance | Various versions are tested | Various versions are tested |             Various versions are tested             | Various versions are tested | AWS EKS |

## Maintenance

| Feature/Product  |   Percona Operator for PostgreSQL   |        Stackgres        |       CrunchyData       |   CloudNativePG (EDB)   |            Zalando            |
|------------------|:-----------------------:|:-----------------------:|:-----------------------:|:-----------------------:|:-----------------------------:|
| Operator upgrade |         :check:         |         :check:         |         :check:         |         :check:         |            :check:            |
| Database upgrade |    Automated and safe   |          Manual         |          Manual         |          Manual         |             Manual            |
| Compute scaling  | Horizontal and vertical | Horizontal and vertical | Horizontal and vertical | Horizontal and vertical |    Horizontal and vertical    |
| Storage scaling  |          Manual         |          Manual         |          Manual         |          Manual         | Manual, automated for AWS EBS |

## PostgreSQL topologies

| Feature/Product    | Percona Operator for PostgreSQL | Stackgres | CrunchyData | CloudNativePG (EDB) | Zalando |
|--------------------|:-------------------:|:---------:|:-----------:|:-------------------:|:-------:|
| Warm standby       |       :check:       |  :check:  |   :check:   |       :check:       | :check: |
| Hot standby        |       :check:       |  :check:  |   :check:   |       :check:       | :check: |
| Connection pooling |       :check:       |  :check:  |   :check:   |       :check:       | :check: |
| Delayed replica    |        :no:         |   :no:    |    :no:     |        :no:         |  :no:   |
| Tablespaces        |       :check:       |   :no:    |   :check:   |        :no:         |  :no:   |

## Backups

| Feature/Product   | Percona Operator for PostgreSQL | Stackgres | CrunchyData | CloudNativePG (EDB) | Zalando |
|-------------------|:-------------------------------:|:---------:|:-----------:|:-------------------:|:-------:|
| Scheduled backups |             :check:             |  :check:  |   :check:   |       :check:       | :check: |
| WAL archiving     |             :check:             |  :check:  |   :check:   |       :check:       | :check: |
| PITR              |             :check:             |  :check:  |   :check:   |       :check:       | :check: |
| GCS               |             :check:             |  :check:  |   :check:   |       :check:       | :check: |
| S3                |             :check:             |  :check:  |   :check:   |       :check:       | :check: |
| Azure             |              :no:               |  :check:  |   :check:   |       :check:       | :check: |

## Monitoring

| Feature/Product |  Percona Operator for PostgreSQL  |               Stackgres               |           CrunchyData          |          CloudNativePG (EDB)          |  Zalando |
|-----------------|:---------------------------------:|:-------------------------------------:|:------------------------------:|:-------------------------------------:|:--------:|
| Solution        | Percona Monitoring and Management | Exposing metrics in Prometheus format | Prometheus stack and pgMonitor | Exposing metrics in Prometheus format | Sidecars |

## Miscellaneous

| Feature/Product                    | Percona Operator for PostgreSQL |       Stackgres       |      CrunchyData      |  CloudNativePG (EDB)  |        Zalando        |
|------------------------------------|:-------------------------------:|:---------------------:|:---------------------:|:---------------------:|:---------------------:|
| Customize PostgreSQL configuration |             :check:             |        :check:        |        :check:        |        :check:        |        :check:        |
| Helm                               |             :check:             |        :check:        |        :check:        |        :check:        |        :check:        |
| Transport encryption               |             :check:             |        :check:        |        :check:        |        :check:        |                       |
| Data-at-rest encryption            |      Through storage class      | Through storage class | Through storage class | Through storage class | Through storage class |
| Create users/roles                 |           :check:, limited          |        :check:        |        :check:        |        :check:        |      :check:, limited     |
