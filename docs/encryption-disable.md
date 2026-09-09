# Disable encryption

Disabling `pg_tde` (Transparent Data Encryption) is generally not recommended, as it removes an important layer of security that protects your data at rest. However, if you must disable encryption, this guide walks you through the steps.

!!! important

    To properly disable encryption in the Operator, you must follow a specific sequence and modify your Custom Resource (CR) twice. Attempting to disable everything in a single step will not work: the Operator needs to drop the `pg_tde` extension before you remove the key provider configuration. The Vault secrets must remain mounted while `DROP EXTENSION` runs.

    Failing to follow the steps in this tutorial in order will result in errors, because removing the Vault configuration before the extension is dropped prevents the Operator from cleaning up properly.

    The Operator does **not** drop or rewrite encrypted objects. You must unencrypt them yourself before disabling the extension. If any encrypted objects remain, `DROP EXTENSION pg_tde` fails with a descriptive error.

1. Export the namespace where your database cluster is deployed as an environment variable. Replace the `<namespace>` placeholder with your value:

    ```bash
    export CLUSTER_NAMESPACE=<namespace>
    ```

2. Unencrypt **all encrypted databases** in your database. 
    
    * Identify the primary pod:    

        ```bash
        export PRIMARY_POD=$(kubectl get pods -n "$CLUSTER_NAMESPACE" \
        -l postgres-operator.crunchydata.com/role=primary \
        -o jsonpath='{.items[0].metadata.name}')
        ```

    * Connect to the primary database Pod as the `postgres` user:

        ```bash
        kubectl -n $CLUSTER_NAMESPACE exec -it $PRIMARY_POD -- psql
        ```

    * Connect to each encrypted database and run the following command to unencrypt **every** encrypted table.

        ```sql
        ALTER TABLE <table_name> SET ACCESS METHOD heap;
        ```

    Repeat for every encrypted table, index, and related object in every database. Leaving encrypted objects behind causes disable to fail.

3. Run the `CHECKPOINT` command in PostgreSQL. It forces an immediate checkpoint to flush dirty pages to disk. Connect to the primary database Pod as the `postgres` user and run:

    ```sql
    CHECKPOINT;
    ```

    This flushes data to disk in all databases.

    Exit the Pod.

4. Edit the Custom Resource and set `extensions.pg_tde.enabled` to `false`. Keep the `vault` section in place.

    ```yaml
    spec:
      extensions:
        pg_tde:
          enabled: false
          vault:
            host: https://vault.vault.svc.cluster.local:8200
            mountPath: tde
            tokenSecret:
              name: cluster1-vault
              key: token
            caSecret:
              name: cluster1-vault
              key: ca.crt
    ```

5. Apply the changes:

    ```bash
    kubectl apply -f deploy/cr.yaml -n $CLUSTER_NAMESPACE
    ```

    This triggers a rolling restart of your database Pods. The Operator runs `DROP EXTENSION pg_tde` in all databases. Vault secrets remain mounted during this step.

6. Wait until the `PGTDEEnabled` condition reports `False`:

    ```bash
    kubectl get pg cluster1 -n $CLUSTER_NAMESPACE -o yaml | yq '.status.conditions.[] | select(.type == "PGTDEEnabled")' 
    ```

    ??? example "Expected output"
        
        ```{.yaml .no-copy}
        lastTransitionTime: "2026-07-28T10:24:15Z"
        message: pg_tde is disabled in PerconaPGCluster
        observedGeneration: 3
        reason: Disabled
        status: "False"
        type: PGTDEEnabled
        ```

    Confirm that Pods have finished restarting and the cluster is ready before continuing.

7. Run `CHECKPOINT` again before you remove the Vault configuration. Even after the extension is dropped, PostgreSQL may still touch encrypted objects during recovery after the next restart and try to read the Vault token. A checkpoint helps avoid that failure.

    ```sql
    CHECKPOINT;
    ```

8. Update the Custom Resource again and remove the entire `extensions.pg_tde` section (or at least all vault-related configuration).

9. Apply the changes:

    ```bash
    kubectl apply -f deploy/cr.yaml -n $CLUSTER_NAMESPACE
    ```

    This triggers another rolling restart so the Operator can remove the Vault secret mounts from the containers.


