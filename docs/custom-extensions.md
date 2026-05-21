# Manage PostgreSQL extensions

One of the specific PostgreSQL features is the ability to provide it with additional functionality via [Extensions :octicons-link-external-16:](https://www.postgresql.org/download/products/6-postgresql-extensions/). Percona Distribution for PostgreSQL [comes with a number of extensions :octicons-link-external-16:](https://docs.percona.com/postgresql/latest/extensions.html). These extensions are available for the database cluster managed by the Operator as well.

## Built-in extensions

You can enable or disable built-in extensions in the `extensions` section of your `deploy/cr.yaml` file. Set an option to `true` to enable an extension, or to `false` to disable it. To see which extensions are enabled by default, check the [deploy/cr.yaml :octicons-link-external-16:](https://github.com/percona/percona-postgresql-operator/blob/v{{ release }}/deploy/cr.yaml) Custom Resource manifest.

```yaml
extensions:
  ...
  pg_stat_monitor:
    enabled: false
  pg_stat_statements:
    enabled: false
  pg_audit:
    enabled: true
  pgvector:
    enabled: false
  pg_repack:
    enabled: false
  pg_cron:
    enabled: false
  set_user:
    enabled: false
  pg_tde:
    enabled: false
```

Apply changes after editing with `kubectl apply -f deploy/cr.yaml` command. This causes the Operator to restart the Pods of your cluster.

## Add custom extensions

The needed extension may not be in the list of extensions supplied with Percona Distribution for PostgreSQL, or it's a custom extension developed by the end-user.

To add such a custom extension is not straightforward in a containerized database in a Kubernetes environment. It requires building a custom PostgreSQL image.

Starting with version 2.3, the Operator provides an alternative way to extend Percona Distribution for PostgreSQL by downloading pre-packaged extensions from and external storage on the fly. 

!!! warning "Advanced configuration"

    Custom extensions configuration is an advanced feature that requires careful consideration. Adding custom extensions may violate the immutability of Pod images, which can lead to unexpected behavior and maintenance challenges. Use this feature only if you are certain what you are doing and understand the implications. Or [reach out to our experts](get-help.md#percona-experts) for assistance with adding custom extensions into your infrastructure.

Here's how it works:

1. You build and package a custom extension. The package must have a strict structure. See [Packaging requirements](#packaging-requirements) for details.
2. You upload the extension to a cloud storage. Currently, s3 and s3-compatible storage is supported.
3. In the `extensions` section of the Custom Resource, specify the storage configuration and the extension information.
4. The Operator downloads the extension and installs it.
5. In PostgreSQL, you create the extension for every database where you want to use it.

Understanding which files are required for a given extension may not be easy. To figure this out, you can spin up a Docker container or a virtual machine, install Percona Distribution for PostgreSQL and developer tools there, then build and install the extension from source. Then copy all the installed files to the archive.

Check the [Example configuration](#example-configuration) for the steps that can help you in building and adding your own custom extension.

### Packaging requirements

Custom extensions require specific packaging for the Operator to use them.
The package must be a `.tar.gz` archive that follows this naming format:

`${EXTENSION}-pg${PG_MAJOR}-${EXTENSION_VERSION}`

The archive must be created with `usr` at the root and must include all the required files in the correct directory structure:

1. The control file and any shared library must be in the `LIBDIR` directory
2. All required SQL script files must be in the `SHAREDIR/extension` directory. At least one SQL script is required.

The `SHAREDIR` corresponds to `/usr/pgsql-${PG_MAJOR}/share/extension/` and `LIBDIR` to `/usr/pgsql-${PG_MAJOR}/lib`.

For example, the directory for `pg_stat_kcache` extension should look as follows:

```bash
tree ~/pg_stat_kcache-2.3.2/
/home/user/pg_stat_kcache-2.3.2/
└── usr
    └── pgsql-18
        ├── lib
        │   ├── bitcode
        │   │   ├── pg_stat_kcache
        │   │   │   └── pg_stat_kcache.bc
        │   │   └── pg_stat_kcache.index.bc
        │   └── pg_stat_kcache.so
        └── share
            └── extension
                ├── pg_stat_kcache--2.1.0--2.1.1.sql
                ├── pg_stat_kcache--2.1.0.sql
                ├── pg_stat_kcache--2.1.1--2.1.2.sql
                ├── pg_stat_kcache--2.1.1.sql
                ├── pg_stat_kcache--2.1.2--2.1.3.sql
                ├── pg_stat_kcache--2.1.2.sql
                ├── pg_stat_kcache--2.1.3--2.2.0.sql
                ├── pg_stat_kcache--2.1.3.sql
                ├── pg_stat_kcache--2.2.0--2.2.1.sql
                ├── pg_stat_kcache--2.2.0.sql
                ├── pg_stat_kcache--2.2.1--2.2.2.sql
                ├── pg_stat_kcache--2.2.1.sql
                ├── pg_stat_kcache--2.2.2--2.2.3.sql
                ├── pg_stat_kcache--2.2.2.sql
                ├── pg_stat_kcache--2.2.3--2.3.0.sql
                ├── pg_stat_kcache--2.2.3.sql
                ├── pg_stat_kcache--2.3.0--2.3.1.sql
                ├── pg_stat_kcache--2.3.0.sql
                ├── pg_stat_kcache--2.3.1--2.3.2.sql
                ├── pg_stat_kcache--2.3.1.sql
                ├── pg_stat_kcache--2.3.2.sql
                └── pg_stat_kcache.control           
```

The resulting `.tar` archive has the name `pg_stat_kcache-pg18-2.3.2.tar.gz`.

### Example configuration

The following is an **example workflow** showing how to build and package the [`pg_stat_kcache` :octicons-link-external-16:](https://github.com/powa-team/pg_stat_kcache) extension. This example is intended to illustrate the general process and give you an idea of the required steps. However, the exact workflow and specifics may differ for your custom extension. Always review your extension's build and packaging requirements and adapt accordingly.

#### Considerations

1. You must build your extension on a host **with the same operating system and architecture** as the one used for Percona Distribution for PostgreSQL images to prevent library incompatibility. Otherwise, your extension may not load or may not function correctly.

    To check the operating system, do the following:

    1. Connect to one of the database Pods:

        ```bash
        kubectl exec -it cluster1-instance1-xrcf-0 -n <namespace> -c database -- bash
        ```

    2. List the installed packages:

        ```bash
        rpm -qa|grep percona
        ```

        ??? example "Sample output"

            ```{.text .no-copy}           
            percona-release-1.0-33.noarch
            percona-postgresql18-libs-18.4-2.el9.x86_64
            percona-postgresql18-18.4-2.el9.x86_64
            percona-postgresql-client-common-290-2.el10.noarch
            percona-postgresql18-server-18.4-2.el9.x86_64
            percona-pgvector_18-0.8.3-2.el9.x86_64
            percona-pgvector_18-llvmjit-0.8.3-2.el9.x86_64
            percona-pg_cron_18-1.6.7-2.el9.x86_64
            percona-pg_stat_monitor18-2.3.2-3.el9.x86_64
            percona-pgaudit18-18.0-3.el9.x86_64
            percona-postgresql18-llvmjit-18.4-2.el9.x86_64
            percona-wal2json18-2.6-4.el9.x86_64
            percona-postgresql18-contrib-18.4-2.el9.x86_64
            percona-postgresql-common-290-2.el10.noarch
            percona-pg_oidc_validator18-1.0-3.el9.x86_64
            percona-pg_repack18-1.5.3-3.el9.x86_64
            percona-pgaudit18_set_user-4.2.0-3.el9.x86_64
            percona-pg_tde18-2.2.1-2.el9.x86_64
            percona-pgbackrest-2.58.0-3.el9.x86_64
            percona-patroni-etcd-4.1.3-2.el9.x86_64
            percona-patroni-4.1.3-2.el9.x86_64
            ```

    3. Check the operating system version:

        ```bash
        cat /etc/redhat-release
        ```

        ??? example "Sample output"
            
            ```{.text .no-copy}
            Red Hat Enterprise Linux release 9.8 (Plow)
            ```

2. Your extension must be compatible with PostgreSQL version you are running. To check the version, run the following command:
    
    {% raw %}
    ```bash
    kubectl -n <namespace> get pg cluster1 -o go-template='{{.spec.image}}'
    ```
    {% endraw %}

    ??? example "Sample output"

        ``` {.text .no-copy}
        docker.io/perconalab/percona-postgresql-operator:main-ppg18-postgres
        ```

3. In this example configuration, we use a Docker container to build the `pg_stat_kcache` extension. However, you can use any environment that matches the distribution's operating system, such as a virtual machine or a Kubernetes Pod, not just Docker.
4. We assume you have deployed a Percona Distribution for PostgreSQL cluster in Kubernetes. If not, use the [Quickstart guide](kubectl.md) to deploy it.

#### Prepare your build environment

Run the following commands as the root user or with `sudo` privileges.

1. Start a Docker container and establish a shell session inside. In this example we use a RockyLinux 9 on `x86_64` architecture.

    ```bash
    docker run -it --name pg rockylinux:9 /bin/bash
    ```
  
2. Install basic tools:

    ```bash
    dnf install git make 'dnf-command(config-manager)'
    ```

3. Install additional PostgreSQL packages:

    * Add the Extra Packages for Enterprise Linux by installing the `epel-release` package:

       ```bash
       dnf install -y https://dl.fedoraproject.org/pub/epel/epel-release-latest-9.noarch.rpm
       ```

    * Add the codeready builder repository that contains additional packages for use by developers:

      ```bash
      dnf config-manager --add-repo https://dl.rockylinux.org/pub/rocky/9/CRB/x86_64/os/
      ```

    * Import GPG keys

       ```bash
       rpm --import https://dl.rockylinux.org/pub/rocky/RPM-GPG-KEY-Rocky-9
       ```

    * Install `perl-IPC-Run` to run and interact with child processes:

       ```bash
       dnf install perl-IPC-Run -y
       ```
    

4. Install build tools:

    ```bash
    dnf groupinstall "Development tools"
    ```

    Troubleshooting tip: If development tools fail to install, add BaseOS and AppStream repos:

    ```bash
    dnf config-manager --add-repo https://dl.rockylinux.org/pub/rocky/9/BaseOS/x86_64/os/
    dnf config-manager --add-repo https://dl.rockylinux.org/pub/rocky/9/AppStream/x86_64/os/
    dnf clean all && dnf makecache
    ```

    Then retry the installation.

5. Install PostgreSQL 18 compatible LLVM toolchain and Clang library. Certain extensions such as `pg_stat_kcache` may require LLVM and Clang to build correctly, as they use modern C/C++ features and sometimes depend on LLVM infrastructure for compiling code or enabling advanced extension capabilities. 
    
    ```bash
    dnf install -y llvm-toolset clang
    ```
    
6. Install PostgreSQL developer packages from Percona repositories:

    * Install `percona-release` repository management tool:

       ```bash
       dnf install https://repo.percona.com/yum/percona-release-latest.noarch.rpm
       ```
    
    * Enable PostgreSQL repository:

      ```bash
      percona-release setup ppg18
      ```

    * Disable the `potsgresql` module supplied with the operating system:

       ```bash
       dnf -qy module disable postgresql
       ```

    * Install PostgreSQL developer packages:

       ```bash
       dnf install percona-postgresql18-devel percona-postgresql18-libs percona-postgresql18
       ```

#### Build the extension 

1. Download the extension source:

    ```bash
    git clone https://github.com/powa-team/pg_stat_kcache.git
    ```

2. Navigate to the cloned extension and switch to the desired version. In this example we use `pg_stat_kcache` version 2.3.2:

    ```bash
    cd pg_stat_kcache
    git checkout REL2_3_2
    ```

3. Ensure `pg_config` is in your path:

    ```bash
    export PATH=/usr/pgsql-18/bin:$PATH
    ```

4. Build the extension with PGXS flags neutralized:
    
    ```bash
    make PG_CFLAGS="" CFLAGS="" CPPFLAGS="" USE_PGXS=1
    ```
    
5. Install the extension

    ```bash
    sudo PATH=$PATH make install
    ```

    As the result you should see the binaries in the following paths: `/usr/pgsql-18/share/extension/pg_stat_kcache` and `/usr/pgsql-18/lib/`.

#### Package the extension

1. Create a `.tar` archive of the extension:

    ```bash
    tar -czvf pg_stat_kcache-pg18-2.3.2.tar.gz \
      /usr/pgsql-18/lib/bitcode/* \
      /usr/pgsql-18/lib/pg_stat_kcache.so \
      /usr/pgsql-18/share/extension/pg_stat_kcache*
    ```

2. Check that the package structure follows the [requirements](#packaging-requirements).
3. Copy the archive to the local machine. Run this command on the local machine:

    ```bash
    docker cp pg:/pg_stat_kcache-pg18-2.3.1.tar.gz ./
    ```

### Upload a custom extension to the cloud storage

After packaging the extension, upload it to a cloud storage. In our example we use AWS S3 storage. You can upload the extension via the Amazon web interface or using the `aws` command line tool as shown below:

1. Export the AWS S3 access credentials as the environment variables:
    
    ```bash
    export AWS_ACCESS_KEY_ID=<your-access-key-id-here> 
    export AWS_SECRET_ACCESS_KEY=<your-secret-key-here>
    ```

2. Upload the extension to your storage. Use your value for the bucket and specify your path to the archive:

   ```bash
   aws s3 cp path/to/pg_stat_kcache-pg18-2.3.1.tar.gz s3://my-bucket
   ```

### Create a Secret with the storage credentials

After the upload is complete, place the access credentials for the cloud storage in a Secret.

1. Create a Secrets file with the credentials that the Operator needs
    to access extensions stored on Amazon S3:

    * The `metadata.name` key is the name you will use to refer to
        your Kubernetes Secret.
    * The `data.AWS_ACCESS_KEY_ID` and `data.AWS_SECRET_ACCESS_KEY` keys contain
        base64-encoded credentials used to access the storage.

        To encode credentials, use this command:

        === "in Linux"

            For GNU/Linux:

            ```bash
            echo -n 'plain-text-string' | base64 --wrap=0
            ```

        === "in macOS"

            For Apple macOS:

            ```bash
            echo -n 'plain-text-string' | base64
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

2. Create the Secrets object from this file:

    ```bash
    kubectl apply -f extensions-secret.yaml -n <namespace>
    ```

### Configure the Operator to load and install the custom extension 

Specify both the storage and extension details in the Custom
Resource so the Operator can download and install it.

1. Configure the `extensions` subsection of the Custom Resource as follows:

    * `image` - Specify the Operator image to use when uploading the extension
    * `storage` - Specify storage details such as the bucket where your extension resides, region, endpoint to access the storage and the Secret name with the storage credentials that you created before.
    * `custom` - Specify the extension name and version
    * `pg_stat_kcache` requires `pg_stat_statements` to be installed in PostgreSQL. If you haven't done it before, enable the `pg_stat_statements`:

      ```yaml
      extensions:
        image: docker.io/perconalab/percona-postgresql-operator:{{release}}
        ...
        storage:
          type: s3
          bucket: pg-extensions
          region: eu-central-1
          endpoint: s3.eu-central-1.amazonaws.com
          secret:
            name: cluster1-extensions-secret
        ...
        pg_stat_statements:
            enabled: true
        custom:
        - name: pg_stat_kcache
            version: 2.3.1
        pg_stat_statements: true
      ```
     
2. Some extensions (such as `pg_stat_kcache` in our example) may require additional shared memory. If this is the case, you need to configure PostgreSQL to preload it at startup:

    ```yaml
    ...
    patroni:
      dynamicConfiguration:
        postgresql:
          parameters:
            shared_preload_libraries: "pg_stat_statements,pg_stat_kcache"
            ...
    ```

3. Apply the configuration: 
    
    ```bash
    kubectl apply -f deploy/cr.yaml -n <namespace>
    ```

    This causes the Operator to restart the Pods of your cluster.

#### Enable custom extension in PostgreSQL

The installed extension is not enabled by default. You need to explicitly enable it in PostgreSQL for all databases where you want to use it.

Here's how to do it:

1. Connect to the primary Pod:

    ```bash
    PRIMARY=$(kubectl get pod -n <namespace> \
      --selector postgres-operator.crunchydata.com/cluster=cluster1,postgres-operator.crunchydata.com/role=primary \
      -o jsonpath='{.items[0].metadata.name}')
    kubectl exec -it $PRIMARY -c database -n <namespace> -- psql
    ```

2. Connect to the required database in PostgreSQL and create the extension for this database using the `CREATE EXTENSION` statement:

    ```sql
    CREATE EXTENSION pg_stat_kcache;
    ```

## Update custom extensions

To update your custom extension inside the Operator, do the following:

1. Prepare the `*.tar` archive of the extension's new version. See the [Packaging requirements](#packaging-requirements) section for the archive's structure and naming format
2. Reference the new version of the extension in the Custom Resource. For example, you update `pg_stat_kcache` extension to version 2.3.3. Then your configuration looks like this:

    ```yaml
    extensions:
      ...
      custom:
      - name: pg_stat_kcache
        version: 2.3.3
    ```

3. Apply the configuration for the changes to come into place:

    ```bash
    kubectl apply -f deploy/cr.yaml -n <namespace>
    ```
