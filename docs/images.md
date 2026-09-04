# Percona certified images

This page lists Percona’s certified Docker images that you can use with Percona Operator for PostgreSQL {{release}}. 

To find images for a specific Operator version, see [Retrieve Percona certified images](image-query.md).

To run the Operator against upstream-built PostgreSQL images instead of Percona Distribution images, see [Deploy a cluster with community PostgreSQL images](install-community.md) (tech preview).

## Image path

Each certified image uses this path:

```text
<registry>/<namespace>/<image-name>:<tag>
```

For example, `docker.io` is the registry, `percona` is the publisher, `percona-distribution-postgresql` is the component, and `{{postgresrecommended}}` is the tag:

```text
docker.io/percona/percona-distribution-postgresql:{{postgresrecommended}}
```

The same pattern applies to other components, for example:

```text
docker.io/percona/percona-pgbouncer:{{pgbouncerrecommended}}
docker.io/percona/percona-pgbackrest:{{pgbackrestrecommended}}
```

## UBI version tags

Starting with Operator 3.1.0, Percona Distribution images are
available on UBI 8, UBI 9, and UBI 10.

UBI 9 is the default. Those tags have no OS version, for example
`{{postgresrecommended}}`. For UBI 8 and UBI 10, the `-ubi8` or
`-ubi10` suffix is added to the tag:

```
docker.io/percona/percona-distribution-postgresql:{{postgresrecommended}}
docker.io/percona/percona-distribution-postgresql:{{postgresrecommended}}-ubi8
docker.io/percona/percona-distribution-postgresql:{{postgresrecommended}}-ubi10
```

## Images reference

The following tables list the images that you can use with the Percona Operator for PostgreSQL {{release}}. They omit `docker.io/`. You can add it if your cluster requires an explicit registry.

--8<-- "Kubernetes-Operator-for-PostgreSQL-RN{{release}}.md:images"

Keep every PostgreSQL instance in a cluster on the same UBI version. Switching UBI majors changes collation libraries. See [Minor version upgrade](update-db-minor.md) and [Major version upgrade](update-db-major.md).

For older versions, please refer to the [old releases documentation archive :octicons-link-external-16:](https://docs.percona.com/legacy-documentation/).
