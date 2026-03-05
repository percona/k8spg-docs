# Disable encryption

Disabling `pg_tde` (Transparent Data Encryption) is generally not recommended, as it removes an important layer of security that protects your data at rest. However, if you must disable encryption, this guide walks you through the steps.

!!! important

    To properly disable encryption in the Operator, you must follow a specific sequence and modify your Custom Resource (CR) twice. Attempting to disable everything in a single step will not work: the Operator needs to drop the `pg_tde` extension before you remove the key provider configuration.

    Failing to follow the steps in this tutorial in order will result in errors, because removing the Vault configuration before the extension is dropped prevents the Operator from cleaning up properly.

1. Export the namespace where your database cluster is deployed as an environment variable. Replace the `<namespace>` placeholder with your value:
    
    ```bash
    export CLUSTER_NAMESPACE=<namespace>
    ```

2. Unencrypt **all encrypted databases** in your database. Connect to the primary database Pod as the `postgres` user, connect to each encrypted database and run the following command to unencrypt **every** encrypted table

    ```sql
    ALTER TABLE <table_name> SET ACCESS METHOD heap;
    ```

    Exit the Pod.

3. Edit the Custom Resource and set the `extensions.pg_tde.enabled` option to `false`.

    ```yaml
    spec:
      extensions:
        pg_tde:
          enabled: false
    ```

4. Apply the changes:

    ```bash
    kubectl apply -f deploy/cr.yaml -n $CLUSTER_NAMESPACE
    ```
    
    This command triggers the rolling restart of your database Pods. As a result, the Operator runs `DROP EXTENSION pg_tde` in all databases.

5. Run the `CHECKPOINT` command in PostgreSQL. It forces an immediate checkpoint to flush all dirty pages to disk and update all datafiles and indexes. Connect to the primary database Pod as the `postgres` user and run:

    ```sql
    CHECKPOINT;
    ```

    This flushes data to disk in all databases.

    Exit the Pod.

6. Update the Custom Resource again and remove all vault-related configuration from `extensions.pg_tde` section. 

7. Apply the changes:
    
    ```bash
    kubectl apply -f deploy/cr.yaml -n $CLUSTER_NAMESPACE
    ```

    This triggers another rolling restart of the database Pods.

