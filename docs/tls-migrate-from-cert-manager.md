# Migrate from cert-manager to custom TLS certificates

When [cert-manager](https://cert-manager.io/) is installed in the cluster and your PostgreSQL Custom Resource does **not** reference custom TLS Secrets, the Percona Operator for PostgreSQL creates cert-manager `Issuer` and `Certificate` resources and delegates certificate issuance and renewal to cert-manager when it creates a **new** cluster. The Operator does not perform its own built-in certificate rotation in that mode.

If you prefer **not** to use cert-manager for this cluster, you can instead supply Kubernetes Secrets with your own TLS material and point the Custom Resource at them under `spec.secrets`. This guide describes how to move an **existing** cluster from cert-manager-managed certificates to **custom** certificates **without rotating the cluster CA**, so clients and replicas that already trust the current CA keep working.

For background on cert-manager integration, see [Configure TLS security with the Operator using cert-manager](tls-cert-manager.md). For certificate layout, Secret keys, and Common Name (CN) rules, see [Generate certificates manually](tls-manual.md).

!!! warning "Do not rotate the cluster CA in this migration"

    Re-sign **only** the PostgreSQL server and replication certificates with the **same** CA that already backs your cluster. Generating a new CA or changing the root CA requires updating trust everywhere and is out of scope for this procedure.

## Prerequisites

* A running cluster that currently uses cert-manager (Secrets such as `<cluster-name>-cluster-ca-cert`, `<cluster-name>-cluster-cert`, and `<cluster-name>-replication-cert` exist in the cluster namespace).
* `kubectl` and `openssl` (or another PKI toolchain you use to issue TLS certificates).
* Permission to create Secrets and patch the `pg` Custom Resource in the namespace.

## 1. Identify the current CA

1. Set the cluster name and namespace (replace placeholders):

    ```bash
    export CLUSTER=<cluster-name>
    export NAMESPACE=<namespace>
    ```

2. Record the CA certificate fingerprint so you can confirm it is unchanged after migration. Use `root.crt` for the Operator 2.9.0 split state, or `tls.crt` if cert-manager already manages the CA:

    ```bash
    kubectl get secret "${CLUSTER}-cluster-ca-cert" -n "${NAMESPACE}" \
      -o jsonpath='{.data.tls\.crt}' | base64 -d \
      | openssl x509 -fingerprint -sha256 -noout
    ```

3. Decode the CA certificate and private key to local files. You will use them only to sign new leaf certificates; you are **not** replacing the CA in the cluster trust store.

    === "cert-manager or post-recovery Secret (`tls.crt` / `tls.key`)"

        ```bash
        kubectl get secret "${CLUSTER}-cluster-ca-cert" -n "${NAMESPACE}" \
          -o jsonpath='{.data.tls\.crt}' | base64 -d > cluster-ca.crt
        kubectl get secret "${CLUSTER}-cluster-ca-cert" -n "${NAMESPACE}" \
          -o jsonpath='{.data.tls\.key}' | base64 -d > cluster-ca.key
        ```

    === "Operator 2.9.0 split state (`root.crt` / `root.key`)"

        If the root CA Secret still uses internal-PKI key names after the 2.9.0 upgrade, extract the CA with:

        ```bash
        kubectl get secret "${CLUSTER}-cluster-ca-cert" -n "${NAMESPACE}" \
          -o jsonpath='{.data.root\.crt}' | base64 -d > cluster-ca.crt
        kubectl get secret "${CLUSTER}-cluster-ca-cert" -n "${NAMESPACE}" \
          -o jsonpath='{.data.root\.key}' | base64 -d > cluster-ca.key
        ```

    Inspect the Secret with `kubectl get secret ... -o yaml` if you are unsure which key names it uses.

## 2. Generate new certificates with the same CA certificate

Issue **new** TLS certificates for:

* **External (client) traffic** — signed with the existing CA, with a CN (and Subject Alternative Names, if you use them) that match your primary Service. The usual form is `<cluster-name>-primary.<namespace>.svc.cluster.local`. Inspect the current certificate for reference:

    ```bash
    kubectl get secret "${CLUSTER}-cluster-cert" -n "${NAMESPACE}" \
      -o jsonpath='{.data.tls\.crt}' | base64 -d | openssl x509 -text -noout
    ```

* **Replication** — signed with the **same** CA, with CN matching the replication user (by default **`_crunchyrepl`**).

Each resulting certificate must be paired with its private key. Follow the steps in [Generate certificates](tls-manual.md#generate-certificates) for concrete `openssl` or CFSSL examples.

## 3. Create Kubernetes Secrets

Create generic Secrets that include `tls.crt`, `tls.key`, and `ca.crt` for each certificate. The `ca.crt` content in both Secrets must be the same. Use **new** Secret names so you do not overwrite active TLS Secrets before the Custom Resource is updated.

Example (adjust paths and names):

```bash
kubectl create secret generic "${CLUSTER}-custom-tls" -n "${NAMESPACE}" \
  --from-file=ca.crt=cluster-ca.crt \
  --from-file=tls.crt=server.crt \
  --from-file=tls.key=server.key

kubectl create secret generic "${CLUSTER}-custom-replication-tls" -n "${NAMESPACE}" \
  --from-file=ca.crt=cluster-ca.crt \
  --from-file=tls.crt=replication.crt \
  --from-file=tls.key=replication.key
```

Optionally, if you use a dedicated root CA Secret in the Custom Resource, create it as described in [Provide a pre-existing custom root CA certificate to the Operator](tls-manual.md#provide-a-pre-existing-custom-root-ca-certificate-to-the-operator). For many migrations it is enough that each leaf Secret includes the same `ca.crt`.

## 4. Update the PostgreSQL Custom Resource

At this stage, you need to update the cluster configuration to reference the new certificates. To do so, you must pause the cluster to prevent the Operator from automatically reconciling (making changes or reverting your edits) while you update the certificate references. Note that pausing the cluster will make it temporarily unavailable to users and applications, resulting in some planned downtime.

1. [Pause the cluster](pause.md) so the Operator does not reconcile conflicting TLS state while you change references:

    ```bash
    kubectl patch -n "${NAMESPACE}" "pg/${CLUSTER}" --type merge --patch '{
      "spec": { "pause": true }
    }'
    ```

2. Point `spec.secrets` at your new Secrets (names must match what you created):

    ```bash
    kubectl patch -n "${NAMESPACE}" "pg/${CLUSTER}" --type merge --patch "{
      \"spec\": {
        \"secrets\": {
          \"customTLSSecret\": { \"name\": \"${CLUSTER}-custom-tls\" },
          \"customReplicationTLSSecret\": { \"name\": \"${CLUSTER}-custom-replication-tls\" }
        }
      }
    }"
    ```

    If you also set `customRootCATLSSecret`, use the manifest shape from [tls-manual.md](tls-manual.md#provide-a-pre-existing-custom-root-ca-certificate-to-the-operator).

3. Resume reconciliation:

    ```bash
    kubectl patch -n "${NAMESPACE}" "pg/${CLUSTER}" --type merge --patch '{
      "spec": { "pause": false }
    }'
    ```

The Operator reconciles the cluster and may restart or reload database Pods so they load the new Secrets.

## 5. Verify the migration

* **CA unchanged** — Compare the SHA-256 fingerprint of `ca.crt` inside your new Secrets (or the CA Secret you kept) with the fingerprint you recorded in step 1.
* **Server certificate** — Decode `tls.crt` from `${CLUSTER}-custom-tls` and confirm dates, SANs/CN, and issuer match expectations.
* **Replication certificate** — Confirm `${CLUSTER}-custom-replication-tls` is present, signed by the same CA, and uses the correct replication CN (`_crunchyrepl` by default).
* **Cluster status** — `kubectl get pg "${CLUSTER}" -n "${NAMESPACE}"` should return to **Ready** (and Pods healthy) after reconciliation.

For connection checks, see [Check TLS communication to a cluster](tls-verify-communication.md).

## Optional: remove cert-manager objects for this cluster

After the cluster runs on custom Secrets, you can delete cert-manager **namespaced** resources the Operator had created for it (for example `Certificate`, `CertificateRequest`, and `Issuer` in `${NAMESPACE}`). List them first:

```bash
kubectl get certificates,certificaterequests,issuers -n "${NAMESPACE}"
```

Delete only resources that belong to this cluster and are no longer required.

When **all** PostgreSQL clusters in the environment use custom TLS (or no longer need cert-manager), you may uninstall or scale down the cert-manager deployment. Coordinate with your platform team; other workloads may still depend on cert-manager.

## Known limitation after removing cert-manager CRDs

If you delete cert-manager CustomResourceDefinitions from the cluster while the Percona Operator is still running, the Operator process may continue to register watches on cert-manager API types and log errors about missing resources.

**Restart the Operator** (for example, restart its Deployment in the Operator namespace) **after** the cert-manager CRDs are removed so a fresh process starts **without** those watches.

## Ongoing lifecycle with custom certificates

With custom Secrets, **you** control rotation and expiry. The Operator does not renew those certificates for you. Plan updates using [Update TLS/SSL certificates](tls-update.md).

Options under `spec.tls` that tune cert-manager validity apply only when cert-manager manages the cluster; they do not apply once you fully rely on custom Secrets for TLS material.
