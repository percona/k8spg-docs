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
| Operator upgrade |         :heavy_check_mark:         |         :heavy_check_mark:         |         :heavy_check_mark:         |         :heavy_check_mark:         |            :heavy_check_mark:            |
| Database upgrade |    Automated and safe   |          Manual         |          Manual         |          Manual         |             Manual            |
| Compute scaling  | Horizontal and vertical | Horizontal and vertical | Horizontal and vertical | Horizontal and vertical |    Horizontal and vertical    |
| Storage scaling  |          Manual         |          Manual         |          Manual         |          Manual         | Manual, automated for AWS EBS |

## PostgreSQL topologies

| Feature/Product    | Percona Operator for PostgreSQL | Stackgres | CrunchyData | CloudNativePG (EDB) | Zalando |
|--------------------|:-------------------:|:---------:|:-----------:|:-------------------:|:-------:|
| Warm standby       |       :heavy_check_mark:       |  :heavy_check_mark:  |   :heavy_check_mark:   |       :heavy_check_mark:       | :heavy_check_mark: |
| Hot standby        |       :heavy_check_mark:       |  :heavy_check_mark:  |   :heavy_check_mark:   |       :heavy_check_mark:       | :heavy_check_mark: |
| Connection pooling |       :heavy_check_mark:       |  :heavy_check_mark:  |   :heavy_check_mark:   |       :heavy_check_mark:       | :heavy_check_mark: |
| Delayed replica    |        :no_entry_sign:         |   :no_entry_sign:    |    :no_entry_sign:     |        :no_entry_sign:         |  :no_entry_sign:   |
| Tablespaces        |       :heavy_check_mark:       |   :no_entry_sign:    |   :heavy_check_mark:   |        :no_entry_sign:         |  :no_entry_sign:   |

## Backups

| Feature/Product   | Percona Operator for PostgreSQL | Stackgres | CrunchyData | CloudNativePG (EDB) | Zalando |
|-------------------|:-------------------------------:|:---------:|:-----------:|:-------------------:|:-------:|
| Scheduled backups |             :heavy_check_mark:             |  :heavy_check_mark:  |   :heavy_check_mark:   |       :heavy_check_mark:       | :heavy_check_mark: |
| WAL archiving     |             :heavy_check_mark:             |  :heavy_check_mark:  |   :heavy_check_mark:   |       :heavy_check_mark:       | :heavy_check_mark: |
| PITR              |             :heavy_check_mark:             |  :heavy_check_mark:  |   :heavy_check_mark:   |       :heavy_check_mark:       | :heavy_check_mark: |
| GCS               |             :heavy_check_mark:             |  :heavy_check_mark:  |   :heavy_check_mark:   |       :heavy_check_mark:       | :heavy_check_mark: |
| S3                |             :heavy_check_mark:             |  :heavy_check_mark:  |   :heavy_check_mark:   |       :heavy_check_mark:       | :heavy_check_mark: |
| Azure             |              :no_entry_sign:               |  :heavy_check_mark:  |   :heavy_check_mark:   |       :heavy_check_mark:       | :heavy_check_mark: |

## Monitoring

| Feature/Product |  Percona Operator for PostgreSQL  |               Stackgres               |           CrunchyData          |          CloudNativePG (EDB)          |  Zalando |
|-----------------|:---------------------------------:|:-------------------------------------:|:------------------------------:|:-------------------------------------:|:--------:|
| Solution        | Percona Monitoring and Management | Exposing metrics in Prometheus format | Prometheus stack and pgMonitor | Exposing metrics in Prometheus format | Sidecars |

## Miscellaneous

| Feature/Product                    | Percona Operator for PostgreSQL |       Stackgres       |      CrunchyData      |  CloudNativePG (EDB)  |        Zalando        |
|------------------------------------|:-------------------------------:|:---------------------:|:---------------------:|:---------------------:|:---------------------:|
| Customize PostgreSQL configuration |             :heavy_check_mark:             |        :heavy_check_mark:        |        :heavy_check_mark:        |        :heavy_check_mark:        |        :heavy_check_mark:        |
| Helm                               |             :heavy_check_mark:             |        :heavy_check_mark:        |        :heavy_check_mark:        |        :heavy_check_mark:        |        :heavy_check_mark:        |
| Transport encryption               |             :heavy_check_mark:             |        :heavy_check_mark:        |        :heavy_check_mark:        |        :heavy_check_mark:        |                       |
| Data-at-rest encryption            |      Through storage class      | Through storage class | Through storage class | Through storage class | Through storage class |
| Create users/roles                 |           limited          |        :heavy_check_mark:        |        :heavy_check_mark:        |        :heavy_check_mark:        |       limited     |
