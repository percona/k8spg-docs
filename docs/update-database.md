# Upgrade Percona Distribution for PostgreSQL

There are two types of PostgreSQL upgrades available through the Operator:

- **Minor upgrade** is upgrading within the same major version. For example, from 15.5 to 15.7 or from 16.1 to 16.3.
- **Major upgrade** is upgrading across major versions, such as from 15.5 to 16.3.

*Major upgrades* are supported starting from Operator **2.4.0** as a tech preview. Starting with Operator **2.9.0**, major upgrades are **generally available (GA)** and fully supported.

Before Operator 2.4.0, only minor upgrades were allowed.

## Image compatibility

When the target PostgreSQL image uses a different UBI major, it ships a different `glibc` (and possibly ICU) collation library. Collation-dependent indexes can become inconsistent until you rebuild them. Both upgrade procedures include those steps after the new image is running.

## Choose an upgrade type

[Run a minor version upgrade](update-db-minor.md){.md-button}
[Run a major version upgrade](update-db-major.md){.md-button}
