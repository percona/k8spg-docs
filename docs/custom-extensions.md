# Add custom PostgreSQL extensions

One of the specific PostgreSQL features is the ability to provide it with additional functionality via [Extensions :octicons-link-external-16:](https://www.postgresql.org/download/products/6-postgresql-extensions/). Percona Distribution for PostgreSQL [supports a number of extensions :octicons-link-external-16:](https://docs.percona.com/postgresql/latest/extensions.html), making this list available for the database cluster managed by the Operator as well.

However, there are cases when the needed extension is not in this list, or when it's a custom extension developed by the end-user.
Adding more extensions is not straightforward in a containerized database in a Kubernetes environment. It requires building a custom PostgreSQL image.

The Operator version 2.3 and above provides an alternative way to extend Percona Distribution for PostgreSQL by downloading pre-packaged extensions from external storage on the fly, which you configure in the `extensions` section of the Custom Resource.

!!! warning "Advanced configuration"

    Custom extensions configuration is an advanced feature that requires careful consideration. Adding custom extensions may violate the immutability of Pod images, which can lead to unexpected behavior and maintenance challenges. Use this feature only if you are certain what you are doing and understand the implications. Or [reach out to our experts](get-help.md#percona-experts) for assistance with adding custom extensions in your infrastructure.

## Enabling or disabling built-in extensions

You can enable or disable built-in extensions in the `extensions.builtin` section of your `deploy/cr.yaml` file. Set an option to `true` to enable an extension, or to `false` to disable it. To see which extensions are enabled by default, check the [deploy/cr.yaml :octicons-link-external-16:](https://github.com/percona/percona-postgresql-operator/blob/v{{ release }}/deploy/cr.yaml) Custom Resource manifest.

```yaml
extensions:
  ...
  builtin:
    pg_stat_monitor: true
    pg_audit: true
    pgvector: false
    pg_repack: false
```

Apply changes after editing with `kubectl apply -f deploy/cr.yaml` command. This causes the Operator to restart the Pods of your cluster.

## Adding custom extensions

The Operator downloads custom extensions from a cloud storage.
You are responsible for properly packaging the extension and uploading it to the storage.

Understanding which files are required for a given extension may not be easy. One option to figure this out is to spin up virtual machine with Percona Distribution for PostgreSQL and build and install the extension from source there. Then copy all the installed files to the archive.

### Packaging custom extensions

Custom extensions require specific packaging for the Operator to use them.
The package must be a `.tar.gz` archive with all required files in the correct
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

The archive must be created with `usr` at the root, and the name must be in the format  `${EXTENSION}-pg${PG_MAJOR}-${EXTENSION_VERSION}`:

``` {.bash data-prompt="$" }
$ cd pg_cron-1.6.1/
$ tar -czf pg_cron-pg15-1.6.1.tar.gz usr/
```
    
## Upload a custom extension to the cloud storage

After packaging the extension, upload it to a cloud storage. For now, Amazon S3 is the only supported storage type. 

## Configure the Operator to load and install the custom extension 

After the upload is complete,
place the access credentials for the cloud storage in a Secret,
and specify both the storage and extension details in the Custom
Resource so the Operator can download and install it.

1. Create a Secrets file with the credentials that the Operator needs
    to access extensions stored on Amazon S3:

    * The `metadata.name` key is the name you will use to refer to
        your Kubernetes Secret.
    * The `data.AWS_ACCESS_KEY_ID` and `data.AWS_SECRET_ACCESS_KEY` keys contain
        base64-encoded credentials used to access the storage. 
        
        To encode credentials, use this command:

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

     Here's the example Secrets file `extensions-secret.yaml`:
     
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

3. Create the Secrets object from this file:

    ``` {.bash data-prompt="$" }
    $ kubectl apply -f extensions-secret.yaml
    ```

4. Configure the Custom Resource. In the `extensions.storage` subsection of the Custom Resource, specify the following information:

    * storage details such as the bucket where your extension resides, region and endpoint to access the storage
    * the Secret name with the storage credentials that you created before.

      ```yaml
      extensions:
        ...
        storage:
          type: s3
          bucket: pg-extensions
          region: eu-central-1
          endpoint: s3.eu-central-1.amazonaws.com
          secret:
            name: cluster1-extensions-secret
      ```
    
    * In the `extensions.custom` subsection, specify the extension name and version:

       ```yaml
       extensions:
         ...
         custom:
         - name: pg_cron
           version: 1.6.1
       ```

5. Some extensions (such as `pg_cron` in our example) may require access additional shared memory. If this is the case, you need to configure PostgreSQL to preload it at startup:

    ```yaml
    ...
    patroni:
      dynamicConfiguration:
        postgresql:
          parameters:
            shared_preload_libraries: pg_cron
            ...

6. Apply the configuration: 
    
    ```{.bash data-prompt="$"}
    $ kubectl apply -f deploy/cr.yaml -n <namespace>
    ```

    This causes the Operator to restart the Pods of your cluster.

## Enable custom extension in PostgreSQL

The installed extension is not enabled by default. You need to explicitly enable it in PostgreSQL for all databases where you want to use it.

Here's how to do it:

1. Connect to the primary Pod:

    ```{.bash data-prompt="$"}
    $ kubectl exec -it cluster1-instance1-69r8-0 -c database -n pgo -- bash
    ```

2. Connect to the required database in PostgreSQL and create the extension for this database using the `CREATE EXTENSION` statement:

    ```sql
    CREATE EXTENSION pg_cron;
    ```

3. Repeat step 2 for all databases where you want to use your extension.
