# Configure transparent data encryption (TDE) with HashiCorp Vault

This document guides you through setting up transparent data encryption (TDE) with `pg_tde` and HashiCorp Vault as the key provider. To learn more about TDE and how it works, see [Transparent data encryption](encryption.md).

## Assumptions

1. This guide is provided as a best effort and builds upon procedures described in the official Vault documentation. Since Vault's setup steps may change in future releases, this document may become outdated; we cannot guarantee ongoing accuracy or responsibility for such changes. For the most up-to-date and reliable information, please always refer to [the official Vault documentation](https://developer.hashicorp.com/vault/tutorials/kubernetes/kubernetes-minikube-tls#kubernetes-minikube-tls).
2. In the following sections we deploy the Vault server in High Availability (HA) mode on Kubernetes via Helm with TLS enabled. The HA setup uses Raft storage backend and consists of 3 replicas for redundancy. Using Helm is not mandatory. Any supported Vault deployment (on-premises, in the cloud, or a managed Vault service) works as long as the Operator can reach it.
3. This guide uses Vault Helm chart version 0.30.0. You may want to change it to the required version by setting the `VAULT_HELM_VERSION` variable.

## Prerequisites

To configure TDE, you need the following:

* `kubectl`- Kubernetes command-line interface
* `helm` - Helm package manager
* `jq` - JSON processor
* The Operator and Percona Distribution for PostgreSQL installed. 

## Prepare your environment

1. Create the namespaces for Vault and the database cluster. If you have installed the Operator and Percona Distribution for PostgreSQL, you don't need to create a namespace for them.

    * For Vault server:

       ```bash
       kubectl create namespace vault
       ```

    * For Percona Distribution for PostgreSQL cluster:

       ```bash
       kubectl create namespace pg
       ```

2. Export the namespaces and other variables as environment variables to simplify further configuration:

    ```bash
    export NAMESPACE="vault"
    export CLUSTER_NAMESPACE="pg"
    export VAULT_HELM_VERSION="0.30.0"
    export SERVICE="vault"
    export CSR_NAME="vault-csr"
    export SECRET_NAME_VAULT="vault-secret"
    export POLICY_NAME="tde-policy"
    export WORKDIR="/tmp/vault"
    ```

3. Create a working directory for configuration files:

    ```bash
    mkdir -p $WORKDIR
    ```

---8<--- "vault-generate-tls-certs.txt"

---8<--- "vault-install-tls.txt"

## Configure Vault

---8<--- "vault-enable-kv.txt"

1. (Optional) You can also enable audit. This is not mandatory, but useful:

    ```bash
    vault audit enable file file_path=/vault/vault-audit.log
    ```

    ??? example "Expected output"

        ``` {.text .no-copy}
        Success! Enabled the file audit device at: file/
        ```

## Create a non-root token

Using the root token for authentication is not recommended, as it poses significant security risks. Instead, you should create a dedicated, non-root token for the Operator to use when accessing Vault. The permissions for this token are controlled by an access policy. Before you create a token you must first create the access policy.

1. Create a policy for accessing the kv engine path and define the required permissions in the `capabilities` parameter:

    ```bash
    kubectl -n "$NAMESPACE" exec vault-0 -- sh -c '
    vault policy write '"$POLICY_NAME"' - << "EOF"
    path "tde/data/*" {
      capabilities = ["read", "create", "update", "list"]
    }
    path "tde/metadata/*" {
      capabilities = ["read", "list"]
    }
    path "sys/internal/ui/mounts/*" {
      capabilities = ["read"]
    }
    path "sys/mounts/*" {
      capabilities = ["read"]
    }
    EOF
    '
    ```

2. Now create a token with a policy.

    ```bash
    kubectl -n "${NAMESPACE}" exec pod/vault-0 -- vault token create -policy="${POLICY_NAME}" -format=json > "${WORKDIR}/vault-token.json"
    ```

3. Export the non-root token as an environment variable:

    ```bash
    export NEW_TOKEN=$(jq -r '.auth.client_token' "${WORKDIR}/vault-token.json")
    ```

4. Verify the token:

    ```bash
    echo "New Vault Token: $NEW_TOKEN"
    ```

    ??? example "Sample output"

        ```{.text .no-copy}
        hvs.CAESINO******************************************T2Y
        ```

## Create a Secret for Vault

To enable Vault for the Operator, create a Secret object for it using the Vault token and the path to TLS certificates. Note that you must create the Secret in the namespace where the Operator and the database cluster is running.

For the following command specify the token and the path to the `ca.cert` file (this is `vault.ca` in our example):

```bash
kubectl create secret generic cluster1-vault --from-literal=token=$NEW_TOKEN --from-file=ca.crt=${WORKDIR}/vault.ca -n $CLUSTER_NAMESPACE
```

Check that the Secret is created:

```bash
kubectl get secret -n $CLUSTER_NAMESPACE
```

## Configure `pg_tde` in the Custom Resource manifest

Now, enable the `pg_tde` extension for your cluster and configure Vault as the key provider. Also enable write-ahead log (WAL) segments encryption on disk. When WAL encryption is enabled, the Operator then adjusts PostgreSQL and pgBackRest so that archiving and restore continue to work with encrypted WAL.

To learn how WAL encryption works with backups, see [WAL encryption](encryption.md#wal-encryption).

!!! important

    We recommend that you enable WAL encryption before the cluster has application writes.

For this you need the following information:

* A Vault server name and port. If Vault is deployed in a separate namespace, use the fully qualified name in the format `<service-name>.<namespace>.svc.cluster.local`.
* The Secret name with the Vault token 
* The Secret name with the CA certificate. In our example, the Vault token and the CA certificate are in the same Secret that you created earlier
* The secrets mount path 

!!! note

    Applying the changes for a running cluster will trigger rolling restart of the database Pods.

1. Edit the `deploy/cr.yaml` file and specify the following:

    * Set `extensions.pg_tde.enabled` to `true`
    * Set `extensions.pg_tde.walEncryption` to `true` to encrypt WAL segments on disk. Omit this option if you only need table encryption.
    * Add Vault-specific options under `extensions.pg_tde.vault`:
        
        * `caSecret` is optional if you communicate with Vault over HTTP. Include it for TLS, as shown in the example below
        * `mountPath` – Specify the Vault mount path where you enabled the KV v2 secrets engine for encryption. In this guide, the mount path is `tde`.

    The example configuration looks like this:

    ```yaml
    spec:
      ....
      extensions:
        image: docker.io/perconalab/percona-postgresql-operator:{{release}}
        pg_tde: 
          enabled: true
          walEncryption: true
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

2. Apply the configuration:

    ```bash
    kubectl apply -f deploy/cr.yaml -n $CLUSTER_NAMESPACE
    ```

3. Wait until the cluster is ready:

    ```bash
    kubectl -n $CLUSTER_NAMESPACE wait --for=condition=Ready \
      perconapgcluster/cluster1 --timeout=600s
    ```

4. Check the `pg_tde` status:

    ```bash
    kubectl get pg cluster1 -n $CLUSTER_NAMESPACE -o yaml | yq '.status.conditions.[] | select(.type == "PGTDEEnabled" or .type == "PGTDEVaultProviderReady")'
    ```

    ??? example "Expected output"

        ```{.yaml .no-copy}
          - lastTransitionTime: "2026-03-04T13:29:51Z"
            message: pg_tde is enabled in PerconaPGCluster
            observedGeneration: 1
            reason: Enabled
            status: "True"
            type: PGTDEEnabled
          - lastTransitionTime: "2026-03-04T13:29:51Z"
            message: pg_tde vault key provider matches the spec
            observedGeneration: 1
            reason: Configured
            status: "True"
            type: PGTDEVaultProviderReady
        ```

    If `PGTDEEnabled` is `True` but encryption does not work, check `PGTDEVaultProviderReady` and the Operator logs.

5. Verify that WAL encryption is on. Find the primary Pod and check the setting:

    ```bash
    export PRIMARY_POD=$(kubectl get pods -n "$CLUSTER_NAMESPACE" \
     -l postgres-operator.crunchydata.com/role=primary \
     -o jsonpath='{.items[0].metadata.name}')
    ```

    ```bash
    kubectl -n $CLUSTER_NAMESPACE exec -it $PRIMARY_POD -- \
      psql -c "SHOW pg_tde.wal_encrypt;"
    ```

    ??? example "Expected output"

        ```{.text .no-copy}
         pg_tde.wal_encrypt
        --------------------
         on
        (1 row)
        ```

!!! note

    WAL files that pgBackRest stores in the backup repository are decrypted before upload. To keep repository contents encrypted, configure [backup encryption](backup-encryption.md) with `repo-cipher-pass`.

## Verify the encryption

Check that the encryption is enabled. To do that, create a table in PostgreSQL using the `tde_heap` access method. To learn more, refer to the [Table Access Methods and pg_tde :octicons-link-external-16:](https://docs.percona.com/pg-tde/index/table-access-method.html) documentation.

1. Find the primary Pod in your cluster and export it as an environment variable:

    ```bash
    export PRIMARY_POD=$(kubectl get pods -n "$CLUSTER_NAMESPACE" \
     -l postgres-operator.crunchydata.com/role=primary \
     -o jsonpath='{.items[0].metadata.name}')
    ```

2. Verify the Pod:

    ```bash
    echo $PRIMARY_POD
    ```

    ??? example "Sample output"

        ```{.text .no-copy}
        cluster1-instance1-btdf-0
        ```

3. Execute into the primary PostgreSQL Pod as the `postgres` user and establish the `psql` session.

    ```bash
    kubectl -n $CLUSTER_NAMESPACE exec -it $PRIMARY_POD -- psql
    ```

    ??? example "Sample output"

        ```{.text .no-copy}
        psql (17.7 - Percona Server for PostgreSQL 17.7.1)
        Type "help" for help.

        postgres=#
        ```

4. Inside the Pod, create a table:

    ```sql
    CREATE TABLE secure_data (
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name TEXT,
    amount NUMERIC(10,2),
    created_at DATE
    ) USING tde_heap;
    ```

5. Insert some sample data:

    ```sql
    INSERT INTO secure_data (name, amount, created_at) VALUES
    ('Alice', 1234.56, '2025-08-01'),
    ('Bob', 7890.12, '2025-08-10'),
    ('Charlie', 345.67, '2025-08-19');
    ```

6. Verify if the table is encrypted:

    ```sql
    SELECT pg_tde_is_encrypted(
     'secure_data'
    );
    ```

    ??? example "Expected output"

        ```
         pg_tde_is_encrypted
        ---------------------
         t
        (1 row)
        ```
  

## Troubleshooting

If you encounter issues during the setup, use the following troubleshooting tips:

1. **Certificate Signing Request (CSR) issues**: If you have problems with the CSR, manually delete it and recreate it:

    ```bash
    kubectl delete csr vault-csr || true
    ```

    Then recreate and re-approve it in Kubernetes following the steps in the [Issue the certificate](#issue-the-certificate) section.

2. **Vault policy issues**: Check the mount points and permissions. Ensure that:

    * The mount path in your policy matches the path where you enabled the secrets engine
    * The policy has the required capabilities (`create`, `read`, `update`, `list`) for the paths your application needs
    * You have included the `sys/internal/ui/mounts/` and `sys/mounts/*` paths

3. **Mount point conflicts**: If you encounter issues with a mount point in Vault, you cannot reuse it. You need to:

    * Provide a new mount path when enabling the secrets engine
    * Update your access policy to include the new mount path
    * Update the `mountPath` value in your Custom Resource configuration to match the new mount path

4. Verify that you reference the correct secret name in your Custom Resource.


## Clean up

After you finish the setup and ensure everything works as expected, you can clean up the temporary files:

```bash
rm -rf $WORKDIR
```

## Next steps

[Disable encryption](encryption-disable.md){.md-button}
