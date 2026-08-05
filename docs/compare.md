# Compare various solutions to deploy PostgreSQL in Kubernetes

There are multiple ways to deploy and manage PostgreSQL in Kubernetes. Here we will focus on comparing the following open source solutions:

* [Crunchy Data PostgreSQL Operator (PGO) :octicons-link-external-16:](https://github.com/CrunchyData/postgres-operator)
* [CloudNative PG :octicons-link-external-16:](https://github.com/cloudnative-pg/cloudnative-pg), vendor-neutral, originally created by Enterprise DB 
* [Stackgres :octicons-link-external-16:](https://github.com/ongres/stackgres) from OnGres
* [Zalando Postgres Operator :octicons-link-external-16:](https://github.com/zalando/postgres-operator)
* [Percona Operator for PostgreSQL :octicons-link-external-16:](https://github.com/percona/percona-postgresql-operator/)

## Generic

| Feature/Product        | Percona Operator for PostgreSQL |        Stackgres        |                     CrunchyData                     |     CloudNativePG            | Zalando |
|------------------------|:---------------------------:|:---------------------------:|:---------------------------------------------------:|:---------------------------:|:-------:|
| Open-source license    |          Apache 2.0         |            AGPL 3           | Apache 2.0, but images are under Developer Program  |          Apache 2.0         |   MIT   |
| PostgreSQL versions    |          13 - 18            |            14 - 18          |                      14 - 18                        |     14 - 18                 | 14 - 18 |
| Kubernetes conformance | Various versions are tested | Various versions are tested |             Various versions are tested             | Various versions are tested | AWS EKS |
| Helm                                 |             :white_check_mark:             |        :white_check_mark:        |        :white_check_mark:        |        :white_check_mark:        |        :white_check_mark:        |
| Web-based GUI          |[Percona Everest](https://docs.percona.com/everest/index.html)|[Admin UI](https://stackgres.io/doc/latest/administration/adminui/)|:no_entry_sign:|:no_entry_sign:| [Postgres Operator UI](https://github.com/zalando/postgres-operator/blob/master/docs/operator-ui.md)|

## Maintenance

| Feature/Product  |   Percona Operator for PostgreSQL   |        Stackgres        |       CrunchyData       |   CloudNativePG   |            Zalando            |
|------------------|:-----------------------:|:-----------------------:|:-----------------------:|:-----------------------:|:-----------------------------:|
| Operator upgrade |         :white_check_mark:         |         :white_check_mark:         |         :white_check_mark:         |         :white_check_mark:         |            :white_check_mark:            |
| Database upgrade | Automated | Automated | Declarative (offline)† | Declarative (offline)† | Automated (offline) |
| Storage scaling  | Automatic (auto-grow) | Manual | Automatic (auto-grow) | Manual | Manual (live resize)‡ |

† Both trigger via a version/image bump in the manifest; the cluster shuts down while pg_upgrade runs.

‡ Live EBS resize (no pod restart) via direct AWS API integration; other clouds use standard K8s PVC resize.

## PostgreSQL topologies

| Feature/Product    | Percona Operator for PostgreSQL | Stackgres | CrunchyData | CloudNativePG  | Zalando |
|--------------------|:-------------------:|:---------:|:-----------:|:-------------------:|:-------:|
| Warm standby       |       :white_check_mark:       |  :white_check_mark:  |   :white_check_mark:   |       :white_check_mark:       | :white_check_mark: |
| Hot standby        |       :white_check_mark:       |  :white_check_mark:  |   :white_check_mark:   |       :white_check_mark:       | :white_check_mark: |
| Connection pooling |       :white_check_mark:       |  :white_check_mark:  |   :white_check_mark:   |       :white_check_mark:       | :white_check_mark: |
| Delayed replica    |        :no_entry_sign:         |   :no_entry_sign:    |    :no_entry_sign:     |        :white_check_mark:        |  :no_entry_sign:   |

## Backups

| Feature/Product   | Percona Operator for PostgreSQL | Stackgres | CrunchyData | CloudNativePG    | Zalando |
|-------------------|:-------------------------------:|:---------:|:-----------:|:-------------------:|:-------:|
| Scheduled backups |             :white_check_mark:             |  :white_check_mark:  |   :white_check_mark:   |       :white_check_mark:       | :white_check_mark: |
| WAL archiving     |             :white_check_mark:             |  :white_check_mark:  |   :white_check_mark:   |       :white_check_mark:       | :white_check_mark: |
| PITR              |             :white_check_mark:             |  :white_check_mark:  |   :white_check_mark:   |       :white_check_mark:       | :white_check_mark: |
| GCS               |             :white_check_mark:             |  :white_check_mark:  |   :white_check_mark:   |       :white_check_mark:       | :white_check_mark: |
| S3                |             :white_check_mark:             |  :white_check_mark:  |   :white_check_mark:   |       :white_check_mark:       | :white_check_mark: |
| Azure             |             :white_check_mark:             |  :white_check_mark:  |   :white_check_mark:   |       :white_check_mark:       | :white_check_mark: |
| Snapshot-based backups | :white_check_mark: (tech preview) | :white_check_mark: | :white_check_mark: (feature-gated) | :white_check_mark: | :no_entry_sign: |

## Monitoring

| Feature/Product |  Percona Operator for PostgreSQL  |               Stackgres               |           CrunchyData          |          CloudNativePG        |  Zalando |
|-----------------|:---------------------------------:|:-------------------------------------:|:------------------------------:|:-------------------------------------:|:--------:|
| Solution        | Percona Monitoring and Management and sidecars | Exposing metrics in Prometheus format | Prometheus stack and pgMonitor | Prometheus metrics & Grafana dashboard | Sidecars |

## Security & Authentication

| Feature/Product | Percona Operator for PostgreSQL | Stackgres | CrunchyData | CloudNativePG | Zalando |
|---|:---:|:---:|:---:|:---:|:---:|
| Transport encryption | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: |
| Data-at-rest encryption | Through storage class, or native TDE (pg_tde)* | Through storage class | Through storage class | Through storage class | Through storage class |
| Create users/roles | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | limited |
| LDAP authentication | Simple bind / search+bind | :no_entry_sign: | TLS-enabled LDAP (custom pg_hba) | Simple bind / search+bind (dedicated `ldap` field) | :no_entry_sign: |
| Certificate (mTLS) authentication | :white_check_mark: (cert-manager) | Partial (CA not passed to PgBouncer — client verification broken) § | :white_check_mark: (MFA/SSO with cert-manager) | :white_check_mark: (auto-issued via cnpg plugin) | :white_check_mark: (custom `spec.tls`) |

\* Percona's pg_tde provides table/tablespace-level encryption with KMS integration (HashiCorp Vault, Thales, Fortanix, OpenBao).

§ Reported against StackGres 1.17.1 in [gitlab.com/ongresinc/stackgres#3056](https://gitlab.com/ongresinc/stackgres/-/issues/3056) — no CA secret selector exists for PgBouncer, so `client_tls_ca_file` never gets set and TLS handshakes fail under `sslmode=require`/`prefer`. Open/unresolved as of this writing; re-check before relying on this if you're on a newer version.

## Extensibility & Customization

| Feature/Product | Percona Operator for PostgreSQL | Stackgres | CrunchyData | CloudNativePG | Zalando |
|---|:---:|:---:|:---:|:---:|:---:|
| Customize PostgreSQL configuration | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: |
| Sidecar containers for customization | :white_check_mark: | :no_entry_sign: | :white_check_mark: | :no_entry_sign: | :white_check_mark: |
| Extension installation (without rebuilding image) | :white_check_mark: (tar archive) | :white_check_mark: (extension repository) | :no_entry_sign: (custom image required) | :white_check_mark: (Image Volumes, PG 18+ / K8s 1.33+ only) | :no_entry_sign: (custom image required) |
