# Add custom PostgreSQL extensions

One of the specific PostgreSQL features is the ability to provide it with additional functionality via [Extensions](https://www.postgresql.org/download/products/6-postgresql-extensions/). Percona Distribution for PostgreSQL [supports a number of extensions](https://docs.percona.com/postgresql/16/), making this list available for the database cluster managed by the Operator as well.

Still there are cases when the needed extension is not in this list, or when it's a custom extension developed by the end-user. 
Adding more extensions is not an easy task in case of a containerized database in Kubernetes-based environment, as normally it would make the user to build a custom PostgreSQL image. 

Still, starting from the Operator version 2.3 there is an alternative way to extend Percona Distribution for PostgreSQL by downloading prepackaged extensions from an external storage on the fly, as defined in the `extensions` section of the Operator Custom Resource.

## Enabling or disabling built-in extensions

Percona Distribution for PostgreSQL [built-in extensions](https://docs.percona.com/postgresql/16/) can be easily enabled or disabled in the `extensions.builtin` subsection of the `deploy/cr.yaml` configuration file as follows:

```yaml
extensions:
  ...
  builtin:
    pg_stat_monitor: true
    pg_audit: true
```

Apply changes after editing with `kubectl apply -f deploy/cr.yaml` command.

!!! note

    Editing this section and applying it is causing Pods restart.

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
/home/user/pg_cron-1.6.1/
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

1. The Operator will need the following data to access extensions stored on the
    Amazon S3:
    
    * the `metadata.name` key is the name which you wll further use to refer
        your Kubernetes Secret,
    * the `data.AWS_ACCESS_KEY_ID` and `data.AWS_SECRET_ACCESS_KEY` keys are
        base64-encoded credentials used to access the storage (obviously these
        keys should contain proper values to make the access possible).

    Create the Secrets file with these base64-encoded keys as follows:

    ```yaml title="extensions-secret.yaml"
    apiVersion: v1
    kind: Secret
    metadata:
      name: cluster1-extensions-secret
    type: Opaque
    data:
      AWS_ACCESS_KEY_ID: <base64 encoded secret>
      AWS_SECRET_ACCESS_KEY: <base64 encoded secret>
    ```

    !!! note

        You can use the following command to get a base64-encoded string
        from a plain text one:

        === "in Linux"

            For GNU/Linux:

            ``` {.bash data-prompt="$" }
            $ echo -n 'plain-text-string' | base64 --wrap=0
            ```

        === "in macOS"

            For Apple macOS:

            ``` {.bash data-prompt="$" }
            $ echo -n 'plain-text-string' | base64
            ```

    Once the editing is over, create the Kubernetes Secret object as follows:

    ``` {.bash data-prompt="$" }
    $ kubectl apply -f extensions-secret.yaml
    ```

2. Storage credentials are specified in the Custom Resource
    `extensions.storage` subsection. The appropriate fragment of the
    `deploy/cr.yaml` configuration file should look as follows:

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

3. When the storage is configured, and the archive with the extension is already
    present in the appropriate bucket, the extension itself can be specified
    to the Operator in the Custom Resource via the `deploy/cr.yaml`
    configuration file as in the following example:

    ```yaml
    extensions:
      ...
      custom:
      - name: pg_cron
        version: 1.6.1
    ```

The installed extension will not be enabled by default. Enabling it in can be
done for desired databases using the `CREATE EXTENSION` statement:

```sql
CREATE EXTENSION pg_cron;
```

Also, some extensions (such as `pg_cron`) can be used only if added to
`shared_preload_libraries`. Users can do it via the `deploy/cr.yaml`
configuration file as follows:

```yaml
...
patroni:
  dynamicConfiguration:
    postgresql:
      parameters:
        shared_preload_libraries: pg_cron
        ...
 ```
