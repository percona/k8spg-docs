# TLS certificate management policy

!!! note "Version added: [3.1.0](ReleaseNotes/Kubernetes-Operator-for-PostgreSQL-RN3.1.0.md)"

You can control how the Operator creates and manages TLS certificates: who issues them, whether cert-manager is used, and what happens when TLS Secrets are missing.

The Operator expects and uses these TLS Secrets for PostgreSQL communication:

* Root CA for the cluster used to sign other certificates
* PostgreSQL server certificate, used for external communication
* Replication client certificate, used for communication between PostgreSQL instances in the cluster.

To learn more, see [Transport layer security (TLS)](TLS.md).

Depending on the [TLS source](TLS.md#how-the-operator-chooses-tls-source), the Operator either uses the TLS Secrets you referenced in the Custom Resource, or it uses the default Secrets that it generated itself.

The Operator has three policies to manage TLS certificates. You define a policy via the `spec.tls.certManagementPolicy` option in the Custom Resource:

* `auto` (default) - the Operator creates new certificates, either self-signed or via [cert-manager](tls-cert-manager.md), and restarts the database Pods. If cert-manager is installed, the Operator uses it and also considers the Issuer or ClusterIssuer settings, if you set them in `spec.tls.issuerConf`. The new certificates have a new CA so client applications must reconnect to use it. 
  
    That works well for dev clusters and for setups where the Operator fully owns certificate creation, including Operator-driven cert-manager.

* `userProvidedOnly` - the Operator skips creating new certificates. The certificate lifecycle management is fully under your control and you are responsible for restoring the access to the Secret.  
  
    This policy is useful if you manage TLS certificates outside the Operator, such as through Kubernetes Secrets synced from AWS Secrets Manager or via [External Secrets Operator :octicons-link-external-16:](https://external-secrets.io/). 
    Using this approach prevents an unexpected certificate regeneration with a different CA, which can otherwise cause clients that rely on the original CA to lose connectivity, potentially leading to service outages.

* `operatorProvidedOnly` - the Operator always creates and manages TLS certificates with its own PKI. It does not create cert-manager `Certificate` or `Issuer` objects, even if cert-manager is installed. It also it ignores settings in `spec.tls.issuerConf`.
  
    Use this when cert-manager is present for other workloads but this PostgreSQL cluster must stay on Operator-generated certificates.

## When to use each policy

| Your setup | Recommended policy |
|------------|-------------------|
| Operator-driven cert-manager, including a custom issuer | `auto` (default) |
| Operator self-signed certificates, and you do not want cert-manager to take over | `operatorProvidedOnly` |
| cert-manager is installed cluster-wide, but this cluster must not use it | `operatorProvidedOnly` |
| [Manually generated certificates](tls-manual.md) in production | `userProvidedOnly` |
| External Secrets or GitOps-managed `spec.secrets.customReplicationTLSSecret`/ `spec.secrets.customTLSSecret` Secrets | `userProvidedOnly` |
| You own rotation and must avoid surprise CA changes on Secret loss | `userProvidedOnly` |

The following table explains how the Operator responds under each policy when it cannot access TLS Secrets.

| Situation | `auto` | `userProvidedOnly` | `operatorProvidedOnly` |
|-----------|--------|-------------------|------------------------|
| Cluster created without TLS Secrets | Operator or cert-manager creates Secrets and starts the cluster | Cluster stays in `initializing` until you create Secrets | Operator creates Secrets with internal PKI and starts the cluster |
| TLS Secret deleted while cluster is running | Operator or cert-manager may create new Secrets and restart Pods | Pods keep running; Operator logs an error; `TLSSecretsReady=False` | Operator recreates Secrets with internal PKI and restarts Pods |
| TLS Secrets restored | Normal operation | `TLSSecretsReady=True`; no forced restart from this policy alone | Normal operation |
| cert-manager installed or `spec.tls.issuerConf` set | Used | Ignored | Ignored |

## Configure the userProvidedOnly policy

This section is a configuration example for `userProvidedOnly`. Use it when you already manage TLS Secrets yourself and you do not want the Operator to create replacements if those Secrets go missing.

For `auto` and `operatorProvidedOnly`, set `spec.tls.certManagementPolicy` to the value you need. Those policies do not require custom Secrets. See [When to use each policy](#when-to-use-each-policy) and [Switch between policies](#switch-between-policies).

### Before you start

1. Create the TLS Secrets in the cluster namespace, or make sure your sync tool creates them before the database Pods must start. See [Generate TLS certificates manually](tls-manual.md).
2. Reference the Secret names in the Custom Resource:

    ```yaml
    spec:
      secrets:
        customTLSSecret: 
          name: cluster1-cert
        customReplicationTLSSecret: 
          name: replication1-cert
    ```

3. Run Percona Operator for PostgreSQL version 3.1.0 or later.

### Set the policy

1. Edit the `deploy/cr.yaml` Custom Resource and set `spec.tls.certManagementPolicy` to `userProvidedOnly`. Keep your Secret references:

    ```yaml
    apiVersion: pgv2.percona.com/v2
    kind: PerconaPGCluster
    metadata:
      name: cluster1
    spec:
      tls: 
        certManagementPolicy: userProvidedOnly
      secrets:
        customTLSSecret: 
          name: cluster1-cert
        customReplicationTLSSecret: 
          name: replication1-cert
    ```

2. Apply the manifest:

    ```bash
    kubectl apply -f deploy/cr.yaml -n <namespace>
    ```

For Helm installations, set the equivalent value in your Helm values file for `tls.certManagementPolicy`.

!!! note

    Do not use `userProvidedOnly` if you expect the Operator to create TLS for you. Missing Secrets at deploy time leave the cluster in the `initializing` state until the Secrets exist.

## Monitor the cluster state

The the cluster state for the following conditions: `TLSSecretsReady` and `Progressing`.

Check the `TLSSecretsReady` condition:

```bash
kubectl -n <namespace> get perconapgcluster cluster1 -o jsonpath='{range .status.conditions[?(@.type=="TLSSecretsReady")]}{.status}{"\n"}{.reason}{"\n"}{.message}{"\n"}{end}'
```

To see `TLSSecretsReady` and `Progressing` together, run:

```bash
kubectl -n <namespace> get perconapgcluster cluster1 -o jsonpath='{range .status.conditions[?(@.type=="TLSSecretsReady" || @.type=="Progressing")]}{.type}{"\t"}{.status}{"\t"}{.reason}{"\t"}{.message}{"\n"}{end}'
```

What you should see depends on the policy. See [Custom resource statuses](cr-statuses.md#conditions) for the full list of conditions.

### auto

`TLSSecretsReady` is `True` when the required Secrets exist. If a Secret is missing, the Operator or cert-manager creates a replacement. 

### userProvidedOnly

If a required TLS Secret is missing, the Operator does not create a replacement. It sets these conditions on the `PerconaPGCluster`:

* `TLSSecretsReady=False` with reason `TLSSecretsMissing`. The message lists the missing Secret names.
* `Progressing=False` with reason `Paused`. Reconciliation stays paused until the Secrets exist.

??? example "Sample output when a Secret is missing"

    ```{.text .no-copy}
    False
    TLSSecretsMissing
    Missing user-provided TLS secrets: cluster1-cluster-cert, cluster1-replication-cert. certManagementPolicy is userProvidedOnly
    ```

Treat `TLSSecretsReady=False` as a blocked state. Existing Pods may keep running with certificates already mounted, but you should restore the Secrets promptly. See [Restore TLS Secrets](#restore-tls-secrets).

### operatorProvidedOnly

`TLSSecretsReady` is `True` with reason `TLSSecretsFound` and the message `certManagementPolicy is operatorProvidedOnly`. If a Secret is missing, the Operator recreates it with internal PKI, so this condition does not stay `False`.

## Restore TLS Secrets

1. Confirm which Secrets are missing. Use the `TLSSecretsReady` message, or check the expected Secret names:

    ```bash
    kubectl -n <namespace> get secret \
      cluster1-cluster-ca-cert \
      cluster1-cluster-cert \
      cluster1-replication-cert \
      cluster1-pgbackrest \
      cluster1-pgbouncer
    ```

    If you referenced custom Secrets in the Custom Resource, check those names instead (for example, the Secrets in `spec.secrets.customTLSSecret` and `spec.secrets.customReplicationTLSSecret`).

2. Recreate or re-sync the missing Secrets (from backup, External Secrets, or your certificate pipeline).

    Label each Secret with the cluster name so the Operator watches it and reconciles promptly:

    ```yaml
    metadata:
      labels:
        postgres-operator.crunchydata.com/cluster: cluster1
    ```

3. If the cluster was waiting for TLS Secrets at create time, restore the cluster-level Secrets first. After `TLSSecretsReady` allows progress, the Operator creates the instance StatefulSet. Then create the matching instance certificate Secret named `<statefulset-name>-certs` (for example, `cluster1-instance1-abcd-certs`).

4. Wait for the next reconciliation cycle, then verify:

    ```bash
    kubectl -n <namespace> get perconapgcluster cluster1 -o jsonpath='{.status.conditions[?(@.type=="TLSSecretsReady")].status}'
    ```

    The output should be `True`. `Progressing` should no longer stay `Paused` because of missing TLS Secrets.

Under `userProvidedOnly`, restoring Secrets does not by itself force a rolling restart. Pods continue using the certificates already loaded until you [update certificates](tls-update.md) intentionally.

## Switch between policies

### Change to userProvidedOnly

Safe when TLS Secrets already exist and you want to prevent automatic regeneration if they are lost later. Apply the updated Custom Resource; no immediate Pod restart is required solely for this change.

### Change to operatorProvidedOnly

Use this when you want the Operator to own TLS with internal PKI and to stop using cert-manager for this cluster. Apply the updated Custom Resource. If Secrets are missing, the Operator creates them. If the cluster was already using cert-manager under `auto`, switching can change how certificates are issued and may affect the CA. Plan client trust accordingly.

### Change to auto

If TLS Secrets are **missing** when you switch to `auto`, the Operator creates new certificates. If cert-manager is installed, `auto` can start using it. That may change the CA and trigger a rolling restart. Only switch to `auto` if you intentionally want the Operator (or cert-manager) to take over certificate creation again.

There is no Operator guardrail that blocks `userProvidedOnly` or `operatorProvidedOnly` → `auto` when Secrets are absent. Plan the switch and client CA trust accordingly.

## Rotate certificates with userProvidedOnly

Certificate rotation remains your responsibility:

1. Update the TLS Secrets with new certificate material (same Secret names).
2. Follow the steps in [Update certificates](tls-update.md) for your certificate source.
3. Confirm `TLSSecretsReady=True` after both Secrets are valid.

The Operator picks up new Secret content and reconciles Pods according to its normal TLS update flow.
