# Configure the TLS certificate management policy

!!! note "Version added: [3.1.0](ReleaseNotes/Kubernetes-Operator-for-PostgreSQL-RN3.1.0.md)"

You can control how the Operator behaves when it cannot find TLS Secrets.

The Operator expects and uses these TLS Secrets for PostgreSQL communication:

* Root CA for the cluster used to sign other certificates
* PostgreSQL server certificate, used for external communication
* Replication client certificate, used for communication between PostgreSQL instances in the cluster.

To learn more, see [Transport layer security (TLS)](TLS.md).

Depending on the [TLS source](TLS.md#how-the-operator-chooses-tls-source), the Operator either uses the TLS Secrets you referenced in the Custom Resource, or it uses the default Secrets that it generated itself.

The Operator has two policies to manage TLS certificates. You define a policy via the `spec.tls.certManagementPolicy` option in the Custom Resource:

* `auto` (default) - the Operator creates new certificates, either self-signed or via cert-manager, and restarts the database Pods. The new certificates have a new CA so client applications must reconnect to use it. 
  
    That works well for dev clusters and for setups where the Operator fully owns certificate creation.

* `userProvidedOnly` - the Operator skips creating new certificates. The certificate lifecycle management is fully under your control and you are responsible for restoring the access to the Secret.  
  
    This policy is useful if you manage TLS certificates outside the Operator, such as through Kubernetes Secrets synced from AWS Secrets Manager or via [External Secrets Operator :octicons-link-external-16:](https://external-secrets.io/). 
    Using this approach prevents an unexpected certificate regeneration with a different CA, which can otherwise cause clients that rely on the original CA to lose connectivity, potentially leading to service outages.

## When to use each policy

| Your setup | Recommended policy |
|------------|-------------------|
| Operator self-signed certificates or Operator-driven cert-manager | `auto` (default) |
| [Manually generated certificates](tls-manual.md) in production | `userProvidedOnly` |
| External Secrets or GitOps-managed `spec.secrets.customReplicationTLSSecret`/ `spec.secrets.customTLSSecret` Secrets | `userProvidedOnly` |
| You own rotation and must avoid surprise CA changes on Secret loss | `userProvidedOnly` |

The following table explains how the Operator responds under each policy when it cannot access TLS Secrets.

| Situation | `auto` | `userProvidedOnly` |
|-----------|--------|-------------------|
| Cluster created without TLS Secrets | Operator creates Secrets and starts the cluster | Cluster stays in `initializing` until you create Secrets |
| TLS Secret deleted while cluster is running | Operator may create new Secrets and roll Pods | Pods keep running; Operator logs an error; `TLSSecretsReady=False` |
| TLS Secrets restored | Normal operation | `TLSSecretsReady=True`; no forced restart from this policy alone |

## Configuration

### Prerequisites

Ensure you have:

1. Created both TLS Secrets in the cluster namespace, or that your sync tool created them before the database Pods must start. See [Generate TLS certificates manually](tls-manual.md).
2. Referenced the Secret names in the Custom Resource:

    ```yaml
    spec:
      secrets:
        customTLSSecret: 
          name: cluster1-cert
        customReplicationTLSSecret: 
          name: replication1-cert
    ```

3. Run Percona Operator for PostgreSQL version 3.1.0 or later.

### Configure the certificate management policy

1. Edit the `deploy/cr.yaml` Custom Resource manifest and configure the  `spec.tls.certManagementPolicy` option:

    ```yaml
    apiVersion: pgv2.percona.com/v2
    kind: PerconaPGCluster
    metadata:
      name: cluster1
    spec:
      tls: 
        certManagementPolicy: userProvidedOnly
      secrets:
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

    Do not set the `userProvidedOnly` value if you expect the Operator to bootstrap TLS for you. With this policy, missing Secrets at deploy time leave the cluster in the `initializing` state until the Secrets exist.


## Monitor the cluster state

If a required TLS Secret is missing and `spec.tls.certManagementPolicy` is set to `userProvidedOnly`, the Operator sets these conditions on the `PerconaPGCluster`:

* `TLSSecretsReady=False` with reason `TLSSecretsMissing`. The message lists the missing Secret names.
* `Progressing=False` with reason `Paused`. Reconciliation stays paused until the Secrets exist.

To check the `TLSSecretsReady` condition, run:

```bash
kubectl -n <namespace> get perconapgcluster cluster1 -o jsonpath='{range .status.conditions[?(@.type=="TLSSecretsReady")]}{.status}{"\n"}{.reason}{"\n"}{.message}{"\n"}{end}'
```

??? example "Sample output when a Secret is missing"

    ```{.text .no-copy}
    False
    TLSSecretsMissing
    Missing user-provided TLS secrets: cluster1-cluster-cert, cluster1-replication-cert. certManagementPolicy is userProvidedOnly
    ```

You can also inspect both related conditions:

```bash
kubectl -n <namespace> get perconapgcluster cluster1 -o jsonpath='{range .status.conditions[?(@.type=="TLSSecretsReady" || @.type=="Progressing")]}{.type}{"\t"}{.status}{"\t"}{.reason}{"\t"}{.message}{"\n"}{end}'
```

Treat `TLSSecretsReady=False` as a blocked state: the Operator does not generate replacement Secrets and does not continue reconciliation until you restore them. Existing Pods may keep running with certificates already mounted, but you should restore the Secrets promptly.

See [Custom resource statuses](cr-statuses.md#conditions) for more on cluster conditions.

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

### Change to auto

If TLS Secrets are **missing** when you switch to `auto`, the Operator creates new certificates. That may change the CA and trigger a rolling restart. Only switch back to `auto` if you intentionally want the Operator to take over certificate creation again.

There is no Operator guardrail that blocks `userProvidedOnly` → `auto` when Secrets are absent. Plan the switch and client CA trust accordingly.

## Rotate certificates with userProvidedOnly

Certificate rotation remains your responsibility:

1. Update the TLS Secrets with new certificate material (same Secret names).
2. Follow the steps in [Update certificates](tls-update.md) for your certificate source.
3. Confirm `TLSSecretsReady=True` after both Secrets are valid.

The Operator picks up new Secret content and reconciles Pods according to its normal TLS update flow.
