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
| [Migrate using a standby cluster](migrate-from-crunchy-standby.md) – set up a new standby cluster in Percona Operator and replicate from Crunchy      | - Shortest downtime: writes stop only during the cutover, usually for seconds <br> - Validate the new cluster while the old one remains online <br> - Roll back to Crunchy until you move the new cluster to its own backup repository | - Requires both clusters running in parallel and higher resource usage <br> - Both clusters need access to the same backup storage, and Percona needs network access to Crunchy <br> - More steps after the cutover: switch TLS certificates and move to a new backup repository path |
| [Migrate with backup and restore](migrate-from-crunchy-backup-restore.md) – back up data in Crunchy and restore it in Percona Operator        | - Allows test runs of the migration <br> - The Crunchy cluster stays unchanged, so you can roll back by pointing applications back to it <br> - Works across Kubernetes clusters that share backup storage | - Downtime lasts for the restore, usually minutes, and grows with the data size <br> - Requires a backup repository in object storage. If the Crunchy cluster only has a volume repository, you must add one |
| [Migrate reusing data volumes](migrate-from-crunchy-data-volumes.md) – reuse the Persistent Volume Claims (PVCs) from a Crunchy cluster           | - No need to move large data over the network <br> - Downtime doesn't grow with the data size | - Requires downtime while the volumes move to the new cluster <br> - Requires permissions to modify PersistentVolumes, usually cluster-admin <br> - Every volume of the primary (data, WAL, tablespaces) must move to the new cluster <br> - Rollback is possible only from a backup taken before the migration |