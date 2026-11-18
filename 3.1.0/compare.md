> For the complete documentation index, see [llms.txt](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/llms.txt).

# Compare various solutions to deploy PostgreSQL in Kubernetes

There are multiple ways to deploy and manage PostgreSQL in Kubernetes. Here we will focus on comparing the following open source solutions:

- [Crunchy Data PostgreSQL Operator (PGO)](https://github.com/CrunchyData/postgres-operator)
- [CloudNative PG](https://github.com/cloudnative-pg/cloudnative-pg) , vendor-neutral, originally created by Enterprise DB
- [Stackgres](https://github.com/ongres/stackgres) from OnGres
- [Zalando Postgres Operator](https://github.com/zalando/postgres-operator)
- [Percona Operator for PostgreSQL](https://github.com/percona/percona-postgresql-operator/)

## Generic

| Feature/Product        | Percona Operator for PostgreSQL                                | Stackgres                                                           | CrunchyData                                        | CloudNativePG               | Zalando                                                                                              |
| ---------------------- | -------------------------------------------------------------- | ------------------------------------------------------------------- | -------------------------------------------------- | --------------------------- | ---------------------------------------------------------------------------------------------------- |
| Open-source license    | Apache 2.0                                                     | AGPL 3                                                              | Apache 2.0, but images are under Developer Program | Apache 2.0                  | MIT                                                                                                  |
| PostgreSQL versions    | 13 - 18                                                        | 14 - 18                                                             | 14 - 18                                            | 14 - 18                     | 14 - 18                                                                                              |
| Kubernetes conformance | Various versions are tested                                    | Various versions are tested                                         | Various versions are tested                        | Various versions are tested | AWS EKS                                                                                              |
| Helm                   |                                                                |                                                                     |                                                    |                             |                                                                                                      |
| Web-based GUI          | [Percona Everest](https://docs.percona.com/everest/index.html) | [Admin UI](https://stackgres.io/doc/latest/administration/adminui/) |                                                    |                             | [Postgres Operator UI](https://github.com/zalando/postgres-operator/blob/master/docs/operator-ui.md) |

## Maintenance

| Feature/Product  | Percona Operator for PostgreSQL | Stackgres | CrunchyData           | CloudNativePG | Zalando                        |
| ---------------- | ------------------------------- | --------- | --------------------- | ------------- | ------------------------------ |
| Operator upgrade |                                 |           |                       |               |                                |
| Database upgrade | Automated                       | Automated | Automated             | Automated     | Automated                      |
| Storage scaling  | Automatic (auto-grow)           | Manual    | Automatic (auto-grow) | Manual        | Manual (live resize)[1](#fn:1) |

## PostgreSQL topologies

| Feature/Product    | Percona Operator for PostgreSQL | Stackgres | CrunchyData | CloudNativePG | Zalando |
| ------------------ | ------------------------------- | --------- | ----------- | ------------- | ------- |
| Warm standby       |                                 |           |             |               |         |
| Hot standby        |                                 |           |             |               |         |
| Connection pooling |                                 |           |             |               |         |
| Delayed replica    |                                 |           |             |               |         |

## Backups

| Feature/Product        | Percona Operator for PostgreSQL | Stackgres | CrunchyData     | CloudNativePG | Zalando |
| ---------------------- | ------------------------------- | --------- | --------------- | ------------- | ------- |
| Scheduled backups      |                                 |           |                 |               |         |
| WAL archiving          |                                 |           |                 |               |         |
| PITR                   |                                 |           |                 |               |         |
| GCS                    |                                 |           |                 |               |         |
| S3                     |                                 |           |                 |               |         |
| Azure                  |                                 |           |                 |               |         |
| Snapshot-based backups | (tech preview)                  |           | (feature-gated) |               |         |

## Monitoring

| Feature/Product | Percona Operator for PostgreSQL                | Stackgres                             | CrunchyData                    | CloudNativePG                          | Zalando  |
| --------------- | ---------------------------------------------- | ------------------------------------- | ------------------------------ | -------------------------------------- | -------- |
| Solution        | Percona Monitoring and Management and sidecars | Exposing metrics in Prometheus format | Prometheus stack and pgMonitor | Prometheus metrics & Grafana dashboard | Sidecars |

## Security & Authentication

| Feature/Product                   | Percona Operator for PostgreSQL                           | Stackgres                                                                    | CrunchyData                      | CloudNativePG                                      | Zalando               |
| --------------------------------- | --------------------------------------------------------- | ---------------------------------------------------------------------------- | -------------------------------- | -------------------------------------------------- | --------------------- |
| Transport encryption              |                                                           |                                                                              |                                  |                                                    |                       |
| Data-at-rest encryption           | Through storage class, or native TDE (`pg_tde`)[2](#fn:2) | Through storage class                                                        | Through storage class            | Through storage class                              | Through storage class |
| Create users/roles                |                                                           |                                                                              |                                  |                                                    | limited               |
| LDAP authentication               | Simple bind / search+bind                                 |                                                                              | TLS-enabled LDAP (custom pg_hba) | Simple bind / search+bind (dedicated `ldap` field) |                       |
| Certificate (mTLS) authentication | (cert-manager)                                            | Partial (CA not passed to PgBouncer — client verification broken) [3](#fn:3) | (MFA/SSO with cert-manager)      | (auto-issued via cnpg plugin)                      | (custom `spec.tls`)   |

## Extensibility & Customization

| Feature/Product                                   | Percona Operator for PostgreSQL | Stackgres              | CrunchyData             | CloudNativePG                            | Zalando                 |
| ------------------------------------------------- | ------------------------------- | ---------------------- | ----------------------- | ---------------------------------------- | ----------------------- |
| Customize PostgreSQL configuration                |                                 |                        |                         |                                          |                         |
| Sidecar containers for customization              |                                 |                        |                         |                                          |                         |
| Extension installation (without rebuilding image) | (tar archive)                   | (extension repository) | (custom image required) | (Image Volumes, PG 18+ / K8s 1.33+ only) | (custom image required) |

______________________________________________________________________

1. Live EBS resize (no pod restart) via direct AWS API integration; other clouds use standard K8s PVC resize. [↩](#fnref:1 "Jump back to footnote 1 in the text")
1. Percona’s `pg_tde` provides table/tablespace-level encryption with KMS integration (HashiCorp Vault). [↩](#fnref:2 "Jump back to footnote 2 in the text")
1. Reported against StackGres 1.17.1 in [gitlab.com/ongresinc/stackgres#3056](https://gitlab.com/ongresinc/stackgres/-/issues/3056) — no CA secret selector exists for PgBouncer, so `client_tls_ca_file` never gets set and TLS handshakes fail under `sslmode=require`/`prefer`. Open/unresolved as of this writing; re-check before relying on this if you’re on a newer version. [↩](#fnref:3 "Jump back to footnote 3 in the text")
