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
| PostgreSQL versions    |          12 - 16            |            14 - 16          |                      13 - 16                        |     12 - 16                 | 11 - 15 |
| Kubernetes conformance | Various versions are tested | Various versions are tested |             Various versions are tested             | Various versions are tested | AWS EKS |

## Maintenance

| Feature/Product  |   Percona Operator for PostgreSQL   |        Stackgres        |       CrunchyData       |   CloudNativePG (EDB)   |            Zalando            |
|------------------|:-----------------------:|:-----------------------:|:-----------------------:|:-----------------------:|:-----------------------------:|
| Operator upgrade |         :white_check_mark:         |         :white_check_mark:         |         :white_check_mark:         |         :white_check_mark:         |            :white_check_mark:            |
| Database upgrade |    Automated and safe   |          Automated and safe         |          Manual         |          Manual         |             Manual            |
| Compute scaling  | Horizontal and vertical | Horizontal and vertical | Horizontal and vertical | Horizontal and vertical |    Horizontal and vertical    |
| Storage scaling  |          Manual         |          Manual         |          Manual         |          Manual         | Manual, automated for AWS EBS |

## PostgreSQL topologies

| Feature/Product    | Percona Operator for PostgreSQL | Stackgres | CrunchyData | CloudNativePG (EDB) | Zalando |
|--------------------|:-------------------:|:---------:|:-----------:|:-------------------:|:-------:|
| Warm standby       |       :white_check_mark:       |  :white_check_mark:  |   :white_check_mark:   |       :white_check_mark:       | :white_check_mark: |
| Hot standby        |       :white_check_mark:       |  :white_check_mark:  |   :white_check_mark:   |       :white_check_mark:       | :white_check_mark: |
| Connection pooling |       :white_check_mark:       |  :white_check_mark:  |   :white_check_mark:   |       :white_check_mark:       | :white_check_mark: |
| Delayed replica    |        :no_entry_sign:         |   :no_entry_sign:    |    :no_entry_sign:     |        :no_entry_sign:         |  :no_entry_sign:   |

## Backups

| Feature/Product   | Percona Operator for PostgreSQL | Stackgres | CrunchyData | CloudNativePG (EDB) | Zalando |
|-------------------|:-------------------------------:|:---------:|:-----------:|:-------------------:|:-------:|
| Scheduled backups |             :white_check_mark:             |  :white_check_mark:  |   :white_check_mark:   |       :white_check_mark:       | :white_check_mark: |
| WAL archiving     |             :white_check_mark:             |  :white_check_mark:  |   :white_check_mark:   |       :white_check_mark:       | :white_check_mark: |
| PITR              |             :white_check_mark:             |  :white_check_mark:  |   :white_check_mark:   |       :white_check_mark:       | :white_check_mark: |
| GCS               |             :white_check_mark:             |  :white_check_mark:  |   :white_check_mark:   |       :white_check_mark:       | :white_check_mark: |
| S3                |             :white_check_mark:             |  :white_check_mark:  |   :white_check_mark:   |       :white_check_mark:       | :white_check_mark: |
| Azure             |             :white_check_mark:             |  :white_check_mark:  |   :white_check_mark:   |       :white_check_mark:       | :white_check_mark: |

## Monitoring

| Feature/Product |  Percona Operator for PostgreSQL  |               Stackgres               |           CrunchyData          |          CloudNativePG (EDB)          |  Zalando |
|-----------------|:---------------------------------:|:-------------------------------------:|:------------------------------:|:-------------------------------------:|:--------:|
| Solution        | Percona Monitoring and Management and sidecars | Exposing metrics in Prometheus format | Prometheus stack and pgMonitor | Exposing metrics in Prometheus format | Sidecars |

## Miscellaneous

| Feature/Product                    | Percona Operator for PostgreSQL |       Stackgres       |      CrunchyData      |  CloudNativePG (EDB)  |        Zalando        |
|------------------------------------|:-------------------------------:|:---------------------:|:---------------------:|:---------------------:|:---------------------:|
| Customize PostgreSQL configuration |             :white_check_mark:             |        :white_check_mark:        |        :white_check_mark:        |        :white_check_mark:        |        :white_check_mark:        |
| Helm                               |             :white_check_mark:             |        :white_check_mark:        |        :white_check_mark:        |        :white_check_mark:        |        :white_check_mark:        |
| Transport encryption               |             :white_check_mark:             |        :white_check_mark:        |        :white_check_mark:        |        :white_check_mark:        |        :white_check_mark:        |
| Data-at-rest encryption            |      Through storage class      | Through storage class | Through storage class | Through storage class | Through storage class |
| Create users/roles                 |           :white_check_mark:    |        :white_check_mark:        |        :white_check_mark:        |        :white_check_mark:        |       limited     |
