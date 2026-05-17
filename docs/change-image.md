# Change cluster images

Percona Operator for PostgreSQL provides default container images for every supported PostgreSQL version and a number of other components in your clusters, making updates seamless. These defaults are defined in installers and can be overridden to meet your specific needs.

Let's see how the Operator understands what image to use and how you can customize them.

## Specify a PostgreSQL version

When a new cluster is created with default settings, the Crunchy Postgres Operator automatically provisions the latest supported major PostgreSQL version, which is currently version 17. This streamlines deployments by providing users with up-to-date features without requiring manual image configuration.

To deploy a different major version of PostgreSQL, users can override the default by specifying the desired version via the `spec.postgresVersion` key:

```yaml
spec:
  postgresVersion: 16
```

Whether the version is defaulted or explicitly defined, the Operator identifies the appropriate container image using corresponding environment variables. For example: 

```
RELATED_IMAGE_POSTGRES_16
RELATED_IMAGE_POSTGRES_17
```

Using the configuration above, the Operator may resolve and pull the following image: `registry.developers.crunchydata.com/crunchydata/crunchy-postgres-gis:ubi8-16.4-3.3-2`.

In addition to core Postgres images, the Operator reads other environment variables to configure and deploy supporting components:

* `RELATED_IMAGE_POSTGRES_GIS`: PostGIS-enabled PostgreSQL images for spatial data capabilities
* `RELATED_IMAGE_PGBACKREST`: The image name to use for pgBackRest containers.  Utilized to run `pgBackRest` repository hosts and backups.
* `RELATED_IMAGE_PGBOUNCER`: The image used to run PgBouncer version 1.15 or newer for connection pooling
* `RELATED_IMAGE_PGUPGRADE`: The image used to perform in-place major version upgrades

Users can override the default images by specifying the desired image for a PostgreSQL option:

```yaml
spec:
  image: perconalab/percona-postgresql-operator:main-ppg17-postgres
  imagePullPolicy: Always
  postgresVersion: 17
```

In this case the Operator pulls and uses the defined image.

## Configure defaults

Cluster administrators can configure default images to gain control over the exact builds used for cluster initialization, backup operations, connection management, and upgrade workflows.

To do so, set a new value for the desired environment variable in the `installers/olm/config/redhat/related-images.yaml`
