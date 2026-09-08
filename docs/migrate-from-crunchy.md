# Migrate from Crunchy Postgres Operator to Percona Operator for PostgreSQL

If you run PostgreSQL on Kubernetes with the Crunchy Operator, migrating to Percona Operator for PostgreSQL is straightforward and low-risk because the operational model is familiar.

## Why migrate to Percona Operator for PostgreSQL

Percona Operator for PostgreSQL is based on the Crunchy Operator codebase, so core workflows are already known and predictable for teams that use Crunchy today.

Key benefits include:

- **Truly open source, no vendor lock-in**: Percona Operator for PostgreSQL is a fully open source solution with the mission of keeping software free from proprietary licensing. You keep flexibility in tooling, support, and long-term platform decisions.
- **Known and predictable workflows**: Operational approach is familiar, enabling your team to start using Percona Operator for PostgreSQL without relearning day-2 operations from scratch.
- **One operating model across your database stack**: If you already run Percona Operators for MySQL or MongoDB, adding PostgreSQL gives you a consistent approach to monitoring, backups, upgrades, and security policy.
- **Lower load on SRE and DevOps teams**: A shared workflow across databases reduces operational complexity, context switching, and maintenance overhead.
- **Migration with native PostgreSQL techniques**: The migration methods use standard PostgreSQL approaches, making the process transparent and easier to validate.

## Before you migrate

This guide provides three migration methods. They all move PostgreSQL data physically (restore, replicate, or reuse volumes). 

Before you choose the migration method, ensure your source and target environments are compatible for migration. Complete this [pre-migration compatibility checklist](migrate-checklist.md) first.

## Choose a migration method

This guide provides three migration methods. Pick the one that best matches your requirements for:

- acceptable downtime,
- rollback options,
- infrastructure overhead.

Review the method comparison first, then follow the detailed steps for your selected path.

| Migration Method | Pros                   | Cons                     |
| ---------------- | ---------------------- | ------------------------ |
| [Migrate using a standby cluster](migrate-from-crunchy-standby.md) – set up a new standby cluster in Percona Operator and replicate from Crunchy      | - Near-zero downtime <br> - Validate new cluster while old remains online  | - Requires both clusters running in parallel <br> - Higher resource usage   |
| [Migrate with backup and restore](migrate-from-crunchy-backup-restore.md) – back up data in Crunchy and restore it in Percona Operator        | - Safer migration path <br> - Allows test runs of migration <br> - Can be rolled back | - Introduces downtime, which depends on data size         |
| [Migrate reusing data volumes](migrate-from-crunchy-data-volumes.md) – reuse the Persistent Volume Claims (PVCs) from a Crunchy cluster           | - Simple and straightforward <br> - No need to move large data over the network        | - Requires downtime <br> - Irreversible and requires thorough testing |