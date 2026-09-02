# Percona Operator images

!!! warning "Mockup for review — not in the site nav"

    Proposed rewrite of [images.md](images.md). Do not add this file to `mkdocs-base.yml`. Open it next to the live page and treat the UBI 8 / UBI 10 digest tables as structure only until those snippets exist.

    **Open questions for review**

    * Split the release-notes `images` snippet into `:images-ubi9`, `:images-ubi8`, and `:images-ubi10`, and keep Operator / PMM outside the UBI tabs?
    * UBI 9 documents one tag with separate x86_64 and ARM64 digests. UBI 8 and UBI 10 currently use an `-arm64` suffix. Confirm the published tag scheme before GA.
    * Keep a short community list on [install-community.md](install-community.md), or point that page here as the single catalog?

This page lists Docker images you can use with Percona Operator for PostgreSQL {{release}}:

* [Certified **Percona Distribution for PostgreSQL** images](#percona-distribution-for-postgresql-images) on UBI 8, UBI 9, and UBI 10
* [**PostgreSQL Community** images](#postgresql-community-images) on UBI 8 and UBI 9

To retrieve Percona certified images for another Operator version, query the [Version Service](image-query.md). To deploy a cluster with community images, see [Deploy a cluster with community PostgreSQL images](install-community.md).

## Image path

Each image uses this path:

```text
<registry>/<namespace>/<image-name>:<tag>
```

For example, `docker.io` is the registry, `percona` is the publisher, `percona-distribution-postgresql` is the component, and `{{postgresrecommended}}` is the tag:

```text
docker.io/percona/percona-distribution-postgresql:{{postgresrecommended}}
docker.io/percona/percona-pgbouncer:{{pgbouncerrecommended}}
docker.io/percona/percona-pgbackrest:{{pgbackrestrecommended}}
```

**PostgreSQL Community** images use the Operator repository and a `-community` tag:

```text
docker.io/percona/percona-postgresql-operator:postgresql{{postgresrecommended}}-community-ubi9
docker.io/percona/percona-postgresql-operator:pgbouncer{{pgbouncerrecommended}}-community
docker.io/percona/percona-postgresql-operator:pgbackrest{{pgbackrestrecommended}}-community
```

## UBI version tags

Percona Distribution images are available on UBI, UBI 9 and UBI 10.

UBI 9 is the default. Those tags have no OS version, for example `{{postgresrecommended}}`. For UBI 8 and UBI 10, add `-ubi8` to the tag, and `-arm64` for ARM64:

```text
docker.io/percona/percona-distribution-postgresql:{{postgresrecommended}}
docker.io/percona/percona-distribution-postgresql:{{postgresrecommended}}-ubi8
docker.io/percona/percona-distribution-postgresql:{{postgresrecommended}}-ubi8-arm64
docker.io/percona/percona-distribution-postgresql:{{postgresrecommended}}-ubi10
docker.io/percona/percona-distribution-postgresql:{{postgresrecommended}}-ubi10-arm64
```

Keep every instance in a cluster on the same UBI version as each ships different `glibc` and ICU library versions. Switching UBI majors changes collation libraries. See [Minor version upgrade](update-db-minor.md) and [Major version upgrade](update-db-major.md).

## Percona Distribution for PostgreSQL images

These images are certified for Operator {{release}}. 

Select a UBI version to see the images for that OS. Operator and PMM Client images are the same for every UBI tab.

=== "UBI 9 (default)"

    Tags have no OS suffix. Each image lists separate digests for x86_64 and ARM64.

    **Images released with Operator {{release}}:**

    --8<-- "Kubernetes-Operator-for-PostgreSQL-RN{{release}}.md:images"

=== "UBI 8"

    Add `-ubi8` to Percona Distribution, pgBouncer, pgBackRest, upgrade, and PostGIS tags. ARM64 tags add `-ubi8-arm64`.

    The Operator and PMM Client images match the UBI 9 tab.

    !!! note "Placeholder for review"

        When the UBI 8 digest table is ready, include it here from the release notes, for example `--8<-- "Kubernetes-Operator-for-PostgreSQL-RN{{release}}.md:images-ubi8"`. The list below shows the expected tags only.

    ```text
    percona/percona-distribution-postgresql-upgrade:18.4-17.10-16.14-15.18-14.23-1-ubi8
    percona/percona-distribution-postgresql-upgrade:18.4-17.10-16.14-15.18-14.23-1-ubi8-arm64
    percona/percona-distribution-postgresql:{{postgresrecommended}}-ubi8
    percona/percona-distribution-postgresql:{{postgresrecommended}}-ubi8-arm64
    percona/percona-distribution-postgresql:{{postgres17recommended}}-ubi8
    percona/percona-distribution-postgresql:{{postgres17recommended}}-ubi8-arm64
    percona/percona-distribution-postgresql:{{postgres16recommended}}-ubi8
    percona/percona-distribution-postgresql:{{postgres16recommended}}-ubi8-arm64
    percona/percona-distribution-postgresql:15.18-1-ubi8
    percona/percona-distribution-postgresql:15.18-1-ubi8-arm64
    percona/percona-distribution-postgresql:14.23-1-ubi8
    percona/percona-distribution-postgresql:14.23-1-ubi8-arm64
    percona/percona-distribution-postgresql-with-postgis:18.4-2-ubi8
    percona/percona-distribution-postgresql-with-postgis:18.4-2-ubi8-arm64
    percona/percona-distribution-postgresql-with-postgis:17.10-2-ubi8
    percona/percona-distribution-postgresql-with-postgis:17.10-2-ubi8-arm64
    percona/percona-distribution-postgresql-with-postgis:16.14-2-ubi8
    percona/percona-distribution-postgresql-with-postgis:16.14-2-ubi8-arm64
    percona/percona-distribution-postgresql-with-postgis:15.18-2-ubi8
    percona/percona-distribution-postgresql-with-postgis:15.18-2-ubi8-arm64
    percona/percona-distribution-postgresql-with-postgis:14.23-2-ubi8
    percona/percona-distribution-postgresql-with-postgis:14.23-2-ubi8-arm64
    percona/percona-pgbackrest:{{pgbackrestrecommended}}-ubi8
    percona/percona-pgbackrest:{{pgbackrestrecommended}}-ubi8-arm64
    percona/percona-pgbouncer:{{pgbouncerrecommended}}-ubi8
    percona/percona-pgbouncer:{{pgbouncerrecommended}}-ubi8-arm64
    ```

=== "UBI 10"

    Add `-ubi10` to Percona Distribution, pgBouncer, pgBackRest, upgrade, and PostGIS tags. ARM64 tags add `-ubi10-arm64`.

    The Operator and PMM Client images match the UBI 9 tab.

    !!! note "Placeholder for review"

        When the UBI 10 digest table is ready, include it here from the release notes, for example `--8<-- "Kubernetes-Operator-for-PostgreSQL-RN{{release}}.md:images-ubi10"`. The list below shows the expected tags only.

    ```text
    percona/percona-distribution-postgresql-upgrade:18.4-17.10-16.14-15.18-14.23-1-ubi10
    percona/percona-distribution-postgresql-upgrade:18.4-17.10-16.14-15.18-14.23-1-ubi10-arm64
    percona/percona-distribution-postgresql:{{postgresrecommended}}-ubi10
    percona/percona-distribution-postgresql:{{postgresrecommended}}-ubi10-arm64
    percona/percona-distribution-postgresql:{{postgres17recommended}}-ubi10
    percona/percona-distribution-postgresql:{{postgres17recommended}}-ubi10-arm64
    percona/percona-distribution-postgresql:{{postgres16recommended}}-ubi10
    percona/percona-distribution-postgresql:{{postgres16recommended}}-ubi10-arm64
    percona/percona-distribution-postgresql:15.18-1-ubi10
    percona/percona-distribution-postgresql:15.18-1-ubi10-arm64
    percona/percona-distribution-postgresql:14.23-1-ubi10
    percona/percona-distribution-postgresql:14.23-1-ubi10-arm64
    percona/percona-distribution-postgresql-with-postgis:18.4-2-ubi10
    percona/percona-distribution-postgresql-with-postgis:18.4-2-ubi10-arm64
    percona/percona-distribution-postgresql-with-postgis:17.10-2-ubi10
    percona/percona-distribution-postgresql-with-postgis:17.10-2-ubi10-arm64
    percona/percona-distribution-postgresql-with-postgis:16.14-2-ubi10
    percona/percona-distribution-postgresql-with-postgis:16.14-2-ubi10-arm64
    percona/percona-distribution-postgresql-with-postgis:15.18-2-ubi10
    percona/percona-distribution-postgresql-with-postgis:15.18-2-ubi10-arm64
    percona/percona-distribution-postgresql-with-postgis:14.23-2-ubi10
    percona/percona-distribution-postgresql-with-postgis:14.23-2-ubi10-arm64
    percona/percona-pgbackrest:{{pgbackrestrecommended}}-ubi10
    percona/percona-pgbackrest:{{pgbackrestrecommended}}-ubi10-arm64
    percona/percona-pgbouncer:{{pgbouncerrecommended}}-ubi10
    percona/percona-pgbouncer:{{pgbouncerrecommended}}-ubi10-arm64
    ```

For images shipped with older Operator versions, query the [Version Service](image-query.md) or see the [old releases documentation archive :octicons-link-external-16:](https://docs.percona.com/legacy-documentation/).

## PostgreSQL Community images

Community images are built from the official PostgreSQL packages on [download.postgresql.org :octicons-link-external-16:](https://www.postgresql.org/download/) (the PGDG repositories). Use them when you need extensions that are not included in Percona Distribution for PostgreSQL, such as TimescaleDB or Citus.

These tags are not bound to a single Operator patch. You must run Operator 3.1.0 or later. They do not include Percona-specific features such as Transparent Data Encryption (TDE).

The tags below are for evaluation. For production, [build and publish your own community images](install-community.md#build-your-own-community-images).

=== "UBI 9 (default)"

    ```text
    percona/percona-postgresql-operator:postgresql{{postgresrecommended}}-community-ubi9
    percona/percona-postgresql-operator:postgresql{{postgres17recommended}}-community-ubi9
    percona/percona-postgresql-operator:postgresql{{postgres16recommended}}-community-ubi9
    percona/percona-postgresql-operator:postgresql15.18-1-community-ubi9
    percona/percona-postgresql-operator:postgresql14.23-1-community-ubi9
    percona/percona-postgresql-operator:postgresql19-community-ubi9
    percona/percona-postgresql-operator:pgbouncer{{pgbouncerrecommended}}-community
    percona/percona-postgresql-operator:pgbackrest{{pgbackrestrecommended}}-community
    percona/percona-postgresql-operator:upgrade-community
    ```

=== "UBI 8"

    PostgreSQL and upgrade tags add `-ubi8`. Use the same pgBouncer and pgBackRest community tags as UBI 9.

    ```text
    percona/percona-postgresql-operator:postgresql{{postgresrecommended}}-community-ubi8
    percona/percona-postgresql-operator:postgresql{{postgres17recommended}}-community-ubi8
    percona/percona-postgresql-operator:postgresql{{postgres16recommended}}-community-ubi8
    percona/percona-postgresql-operator:postgresql15.18-1-community-ubi8
    percona/percona-postgresql-operator:postgresql14.23-1-community-ubi8
    percona/percona-postgresql-operator:upgrade-community-ubi8
    percona/percona-postgresql-operator:pgbouncer{{pgbouncerrecommended}}-community
    percona/percona-postgresql-operator:pgbackrest{{pgbackrestrecommended}}-community
    ```

### PostgreSQL 19 (tech preview)

PostgreSQL 19 is not officially released yet. These extra tags are for evaluation on UBI 9:

```text
percona/percona-postgresql-operator:postgresql19-community-ubi9
percona/percona-postgresql-operator:ppg19-postgres
percona/percona-postgresql-operator:pgbackrest19
percona/percona-postgresql-operator:pgbouncer19
```

To deploy a cluster with these images, see [Deploy a cluster with community PostgreSQL images](install-community.md).
