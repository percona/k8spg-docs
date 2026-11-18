> For the complete documentation index, see [llms.txt](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/llms.txt).

# TLS certificate management policy

Version added: [3.1.0](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/ReleaseNotes/Kubernetes-Operator-for-PostgreSQL-RN3.1.0.html)

You can control how the Operator creates and manages TLS certificates: who issues them, whether cert-manager is used, and what happens when TLS Secrets are missing.

Depending on the [TLS source](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/TLS.html#how-the-operator-chooses-tls-source), the Operator either uses the TLS Secrets you referenced in the Custom Resource, or it uses the Secrets that it generated itself or through the cert-manager.

The Operator has the following policies to manage TLS certificates. You define a policy via the `spec.tls.certManagementPolicy` option in the Custom Resource **when you create a cluster**:

- `auto` (default) — The Operator creates new certificates, either self-signed or via [cert-manager](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/tls-cert-manager.html), and restarts the database Pods. If cert-manager is installed, the Operator uses it and honors the Issuer or ClusterIssuer settings, if defined in `spec.tls.issuerConf`. New certificates have a new CA, so clients must reconnect.

  **When to use:** You want the Operator to own certificate creation, including cert-manager and a custom issuer.

- `userProvidedOnly` — The Operator never creates or replaces TLS Secrets. You own the certificate lifecycle and must restore Secrets if they go missing. This avoids an unexpected new CA, which can drop clients that still trust the old one.

  **When to use:** You manage TLS Secrets yourself [manually](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/tls-manual.html) or outside the Operator Kubernetes Secrets synced from AWS Secrets Manager or via [External Secrets Operator](https://external-secrets.io/)and must keep the existing CA if a Secret is lost.

- `operatorProvidedOnly` — The Operator always creates and manages TLS with its own PKI. It does not create cert-manager `Certificate` or `Issuer` objects, even if cert-manager is installed, and it ignores `spec.tls.issuerConf`.

  **When to use:** You run cert-manager for other workloads, but this cluster must stay on Operator-generated certificates.

## What happens when TLS Secrets are missing

The following table explains how the Operator responds under each policy when it cannot access TLS Secrets.

| Situation                                           | `auto`                                                           | `userProvidedOnly`                                                 | `operatorProvidedOnly`                                            |
| --------------------------------------------------- | ---------------------------------------------------------------- | ------------------------------------------------------------------ | ----------------------------------------------------------------- |
| Cluster created without TLS Secrets                 | Operator or cert-manager creates Secrets and starts the cluster  | Cluster stays in `initializing` until you create Secrets           | Operator creates Secrets with internal PKI and starts the cluster |
| TLS Secret deleted while cluster is running         | Operator or cert-manager may create new Secrets and restart Pods | Pods keep running; Operator logs an error; `TLSSecretsReady=False` | Operator recreates Secrets with internal PKI and restarts Pods    |
| TLS Secrets restored                                | Normal operation                                                 | `TLSSecretsReady=True`; no forced restart from this policy alone   | Normal operation                                                  |
| cert-manager installed or `spec.tls.issuerConf` set | Used                                                             | Ignored                                                            | Ignored                                                           |

## Configure the userProvidedOnly policy

This example sets `userProvidedOnly` when you create the cluster. Use it when you already manage TLS Secrets yourself and you do not want the Operator to create replacements if those Secrets go missing.

Important

You can set the TLS management policy only during the cluster creation. Changing it on a running cluster is not supported.

1. Create the TLS Secrets in the cluster namespace, or make sure your sync tool creates them before the database Pods must start. See [Generate TLS certificates manually](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/tls-manual.html).

1. Deploy the Operator if you haven’t done it before.

1. Edit the `deploy/cr.yaml` Custom Resource:

   - Reference the Secret names

   - Set `spec.tls.certManagementPolicy` to `userProvidedOnly`

     ```
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

1. Apply the manifest:

   ```
   kubectl apply -f deploy/cr.yaml -n <namespace>
   ```

For Helm installations, set the equivalent value in your Helm values file for `tls.certManagementPolicy`.

## Monitor the cluster state

Check the cluster state for the following conditions: `TLSSecretsReady` and `Progressing`.

Run the following command:

```
kubectl -n <namespace> get perconapgcluster cluster1 -o jsonpath='{range .status.conditions[?(@.type=="TLSSecretsReady" || @.type=="Progressing")]}{.type}{"\t"}{.status}{"\t"}{.reason}{"\t"}{.message}{"\n"}{end}'
```

What you should see depends on the policy. See [Custom resource statuses](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/cr-statuses.html#conditions) for the full list of conditions.

### auto

`TLSSecretsReady` is `True` when the required Secrets exist. If a Secret is missing, the Operator or cert-manager creates a replacement.

### userProvidedOnly

If a required TLS Secret is missing, the Operator does not create a replacement. It sets these conditions on the `PerconaPGCluster`:

- `TLSSecretsReady=False` with reason `TLSSecretsMissing`. The message lists the missing Secret names.
- `Progressing=False` with reason `Paused`. Reconciliation stays paused until the Secrets exist.

Sample output when a Secret is missing

```
False
TLSSecretsMissing
Missing user-provided TLS secrets: cluster1-cluster-cert, cluster1-replication-cert. certManagementPolicy is userProvidedOnly
```

Treat `TLSSecretsReady=False` as a blocked state. Existing Pods may keep running with certificates already mounted, but you should restore the Secrets promptly. See [Restore TLS Secrets](#restore-tls-secrets).

### operatorProvidedOnly

`TLSSecretsReady` is `True` with reason `TLSSecretsFound` and the message `certManagementPolicy is operatorProvidedOnly`. If a Secret is missing, the Operator recreates it with internal PKI, so this condition does not stay `False`.

## Restore TLS Secrets

1. Find the missing Secret names in the `TLSSecretsReady` message, or check the expected names. If you referenced custom Secrets, use `spec.secrets.customTLSSecret` and `spec.secrets.customReplicationTLSSecret` instead.

   ```
   kubectl -n <namespace> get secret \
     cluster1-cluster-ca-cert \
     cluster1-cluster-cert \
     cluster1-replication-cert \
     cluster1-pgbackrest \
     cluster1-pgbouncer
   ```

1. Recreate or re-sync the Secrets. Label each one with the cluster name so the Operator watches it:

   ```
   metadata:
     labels:
       postgres-operator.crunchydata.com/cluster: cluster1
   ```

1. If the cluster never finished creating, restore cluster-level Secrets first. After `TLSSecretsReady` is `True`, the Operator creates the instance StatefulSet. Then create `<statefulset-name>-certs` (for example, `cluster1-instance1-abcd-certs`).

1. Confirm `TLSSecretsReady` is `True`. Restoring Secrets does not force a restart. Pods keep the certificates already loaded until you [update certificates](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/tls-update.html).

## Rotate certificates with userProvidedOnly

Certificate rotation remains your responsibility. Follow the steps in [Update certificates](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/tls-update.html) for your certificate source.

The Operator picks up new Secret content and reconciles Pods according to its normal TLS update flow.
