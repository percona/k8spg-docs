# Add custom PostgreSQL extensions

One of the specific PostgreSQL features is the ability to provide it with additional functionality via [Extensions](https://www.postgresql.org/download/products/6-postgresql-extensions/). Percona Distribution for PostgreSQL [supports a number of extensions](https://docs.percona.com/postgresql/16/), making this list available for the database cluster managed by the Operator as well.

Still there are cases when the needed extension is not in this list, or when it's a custom extension developed by the end-user. 
Adding more extensions is not an easy task in case of a containerized database in Kubernetes-based environment, as normally it would make the user to build a custom PostgreSQL image. 

Still, starting from the Operator version 2.3 there is an alternative way to extend Percona Distribution for PostgreSQL by downloading prepackaged extensions from an external storage on the fly, as defined in the `extensions` section of the Operator Custom Resource.

## Enabling or disabling built-in extensions

Percona Distribution for PostgreSQL [builtin extensions](https://docs.percona.com/postgresql/16/) can be easily enabled or disabled in the `extensions.builtin` subsection of the `deploy/cr.yaml` configuration file as follows:

```yaml
extensions:
  ...
  builtin:
    pg_stat_monitor: true
    pg_audit: true
```

Apply changes after editing with `kubectl apply -f deploy/cr.yaml` command.

!!! note

    For obvious reasons, editing this section and applying it is causing Pods
    restart. 

## Adding custom extensions

Custom extensions are downloaded by the Operator from the cloud storage. 
User is in charge for properly packaging extension and uploading it to the storage.

### Packaging custom extensions 

Custom extension needs specific packaging to make the Operator able using it.
The package must be a `.tar.gz` archive with all required files in a the correct
directory structure.

1. Control file must be in `SHAREDIR/extension` directory
2. All required SQL script files must be in `SHAREDIR/extension` directory (there must be at least one SQL script)
3. Any shared library must be in `LIBDIR` 

!!! note 

    In case of Percona Distribution for PostgreSQL images, `SHAREDIR` corresponds to `/usr/pgsql-${PG_MAJOR}/share` and `LIBDIR` to `/usr/pgsql-${PG_MAJOR}/lib`.

For example, the directory for `pg_cron` extension should look as follows:

``` {.bash data-prompt="$" }
$ tree ~/pg_cron-1.6.1/
/home/ege/pg_cron-1.6.1/
└── usr
    └── pgsql-15
        ├── lib
        │   └── pg_cron.so
        └── share
            └── extension
                ├── pg_cron--1.0--1.1.sql
                ├── pg_cron--1.0.sql
                ├── pg_cron--1.1--1.2.sql
                ├── pg_cron--1.2--1.3.sql
                ├── pg_cron--1.3--1.4.sql
                ├── pg_cron--1.4--1.4-1.sql
                ├── pg_cron--1.4-1--1.5.sql
                ├── pg_cron--1.5--1.6.sql
                └── pg_cron.control
```

The archive must be created with `usr` at the root and the name must conform `${EXTENSION}-pg${PG_MAJOR}-${EXTENSION_VERSION}`:

``` {.bash data-prompt="$" }
$ cd pg_cron-1.6.1/
$ tar -czf pg_cron-pg15-1.6.1.tar.gz usr/
```

!!! note

    To understand which files are required for given extension could be not an easy task. One of the option to figure this out would be  building and installing the extension from source on a virtual machine with Percona Distribution for PostgreSQL and copy all the installed files to the archive.

## Configuring custom extension loading

When the extension is packaged, it should be uploaded to the cloud storage
(for now, Amazon S3 is the only supported storage type). When the upload is done,
the storage and extension details should be specified in the Custom Resource
to make the Operator download and install it.

Storage credentials are specified in `extensions.storage` subsection, and configuring it is similar to [setting Amazon S3 storage for backups](backups-storage.md):

```yaml
extensions:
  ...
  storage:
    type: s3
    bucket: pg-extensions
    region: eu-central-1
    secret:
      name: cluster1-extensions-secret
```

When the storage is configured, and archive with extension is already present
in the appropriate bucket, the extension itself can be specified to the Operator
as follows:

```yaml
extensions:
  ...
  custom:
  - name: pg_cron
    version: 1.6.1
```

