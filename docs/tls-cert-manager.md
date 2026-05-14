# Configure TLS security with the Operator using cert-manager

Starting with version 2.9.0, the Percona Operator for PostgreSQL integrates with [cert-manager :octicons-link-external-16:](https://cert-manager.io/) for TLS certificate management. 

When the Operator creates a database cluster, it checks if the cert-manager is installed and if you haven't provided custom TLS secrets. If these conditions are met, the Operator creates the self-signed Issuer resource within the cert-manager and requests a certificate from it. The cert-manager generates certificates and stores them in Kubernetes Secrets. The Operator uses these Secrets for TLS in the cluster. The cert-manager manages the certificate lifecycle.

The Percona Operator self-signed issuer is local to the Operator namespace. This self-signed issuer is created because Percona Distribution for PostgreSQL requires all certificates issued by the same CA (Certificate authority). 

If cert-manager is not installed or not ready, the Operator falls back to its built-in certificate generation.

This approach gives you:

* **Automatic renewal** – cert-manager renews certificates before they expire (by default, 30 days before expiry)
* **Configurable validity** – you can set certificate and CA validity durations via Custom Resource options
* **Centralized management** – use cert-manager’s tooling and policies for all TLS certificates in the cluster

## Certificate lifecycle management

The cert-manager handles:

* **Issuance** – creates certificates when the cluster is created
* **Renewal** – renews certificates before expiry (default: 30 days before). You can configure the certificate duration in the Custom Resource
* **Rotation** – updates Secrets when certificates are renewed

The Operator does not renew certificates when using cert-manager; cert-manager does. You do not need to restart the cluster when certificates are renewed.

## Prerequisites

To use cert-manager with the Operator, ensure the following:

1. You have deployed the Operator. Check if it runs with `kubectl get deploy -n <namespace>` command.
2. Your Custom Resource does **not** include these options:

    * `secrets.customTLSSecret`
    * `secrets.customReplicationTLSSecret`
    * `secrets.customRootCATLSSecret`

    If you provide any of these, the Operator uses your custom certificates and does not create cert-manager resources.

## Install cert-manager

Install cert-manager before deploying the Operator and cluster. You can use either kubectl or Helm.

By default the cert-manager is installed in the `cert-manager` namespace. 

===  "with kubectl"

     ```bash
     kubectl apply -f https://github.com/cert-manager/cert-manager/releases/download/v{{certmanagerrecommended}}/cert-manager.yaml 
     ```
 
     ??? example "Expected output"

         ```{.text .no-copy}
         namespace/cert-manager created
         customresourcedefinition.apiextensions.k8s.io/certificaterequests.cert-manager.io created
         customresourcedefinition.apiextensions.k8s.io/certificates.cert-manager.io created
         customresourcedefinition.apiextensions.k8s.io/challenges.acme.cert-manager.io created
         customresourcedefinition.apiextensions.k8s.io/clusterissuers.cert-manager.io created
         customresourcedefinition.apiextensions.k8s.io/issuers.cert-manager.io created
         customresourcedefinition.apiextensions.k8s.io/orders.acme.cert-manager.io created
         serviceaccount/cert-manager-cainjector created
         serviceaccount/cert-manager created
         serviceaccount/cert-manager-webhook created
         clusterrole.rbac.authorization.k8s.io/cert-manager-cainjector created
         clusterrole.rbac.authorization.k8s.io/cert-manager-controller-issuers created
         clusterrole.rbac.authorization.k8s.io/cert-manager-controller-clusterissuers created
         clusterrole.rbac.authorization.k8s.io/cert-manager-controller-certificates created
         clusterrole.rbac.authorization.k8s.io/cert-manager-controller-orders created
         clusterrole.rbac.authorization.k8s.io/cert-manager-controller-challenges created
         clusterrole.rbac.authorization.k8s.io/cert-manager-controller-ingress-shim created
         clusterrole.rbac.authorization.k8s.io/cert-manager-cluster-view created
         clusterrole.rbac.authorization.k8s.io/cert-manager-view created
         clusterrole.rbac.authorization.k8s.io/cert-manager-edit created
         clusterrole.rbac.authorization.k8s.io/cert-manager-controller-approve:cert-manager-io created
         clusterrole.rbac.authorization.k8s.io/cert-manager-controller-certificatesigningrequests created
         clusterrole.rbac.authorization.k8s.io/cert-manager-webhook:subjectaccessreviews created
         clusterrolebinding.rbac.authorization.k8s.io/cert-manager-cainjector created
         clusterrolebinding.rbac.authorization.k8s.io/cert-manager-controller-issuers created
         clusterrolebinding.rbac.authorization.k8s.io/cert-manager-controller-clusterissuers created
         clusterrolebinding.rbac.authorization.k8s.io/cert-manager-controller-certificates created
         clusterrolebinding.rbac.authorization.k8s.io/cert-manager-controller-orders created
         clusterrolebinding.rbac.authorization.k8s.io/cert-manager-controller-challenges created
         clusterrolebinding.rbac.authorization.k8s.io/cert-manager-controller-ingress-shim created
         clusterrolebinding.rbac.authorization.k8s.io/cert-manager-controller-approve:cert-manager-io created
         clusterrolebinding.rbac.authorization.k8s.io/cert-manager-controller-certificatesigningrequests created
         clusterrolebinding.rbac.authorization.k8s.io/cert-manager-webhook:subjectaccessreviews created
         role.rbac.authorization.k8s.io/cert-manager-cainjector:leaderelection created
         role.rbac.authorization.k8s.io/cert-manager:leaderelection created
         role.rbac.authorization.k8s.io/cert-manager-tokenrequest created
         role.rbac.authorization.k8s.io/cert-manager-webhook:dynamic-serving created
         rolebinding.rbac.authorization.k8s.io/cert-manager-cainjector:leaderelection created
         rolebinding.rbac.authorization.k8s.io/cert-manager:leaderelection created
         rolebinding.rbac.authorization.k8s.io/cert-manager-cert-manager-tokenrequest created
         rolebinding.rbac.authorization.k8s.io/cert-manager-webhook:dynamic-serving created
         service/cert-manager-cainjector created
         service/cert-manager created
         service/cert-manager-webhook created
         deployment.apps/cert-manager-cainjector created
         deployment.apps/cert-manager created
         deployment.apps/cert-manager-webhook created
         mutatingwebhookconfiguration.admissionregistration.k8s.io/cert-manager-webhook created
         validatingwebhookconfiguration.admissionregistration.k8s.io/cert-manager-webhook created
         ```


=== "with Helm"

    1. Add the Helm chart and update the repositories

        ```bash
        helm repo add jetstack https://charts.jetstack.io --force-update
        helm repo update
        ```
    
    2. Install cert-manager with default parameters:

        ```bash
        helm install cert-manager jetstack/cert-manager \
          --namespace cert-manager \
          --create-namespace \
          --version v{{certmanagerrecommended}} \
          --set crds.enabled=true
        ```

        ??? example "Expected output"

            ```{.text .no-copy}
            Pulled: quay.io/jetstack/charts/cert-manager:v1.19.4
            Digest: sha256:135b97727e98ab0af229c2dceaf2e2c3c074a7b83495c6e09a1697c85e5ef6c7
            NAME: cert-manager
            LAST DEPLOYED: Wed Feb 25 16:43:23 2026
            NAMESPACE: cert-manager
            STATUS: deployed
            REVISION: 1
            TEST SUITE: None
            NOTES:
            ```

        You can customize the Helm installation by passing the TLS options via `values.yaml` or `--set`. See the [percona-helm-charts :octicons-link-external-16:](https://github.com/percona/percona-helm-charts) repository for the available parameters.

Verify that cert-manager is running:

```bash
kubectl get pods -n cert-manager
```

??? example "Expected output"

    ```{.text .no-copy}
    cert-manager-548f7cf98c-kjrvx             1/1     Running   0          22s
    cert-manager-cainjector-8798f647f-kv9j4   1/1     Running   0          23s
    cert-manager-webhook-6c8678dc46-whmxp     1/1     Running   0          22s
    ```

## Configure the certificate validity

1. Add the `tls` section to your Custom Resource to set certificate validity durations. These options apply only when cert-manager is used.

    ```yaml
    spec:
      tls:
        certValidityDuration: 2160h   # 90 days for TLS certificates (default: 8760h / 1 year)
        caValidityDuration: 26280h    # 3 years for the CA certificate (default: 8760h / 1 year)
        pgBackRestCertValidityDuration: 2160H # 90 days for TLS certificates 
    ```

    Use [Go duration format :octicons-link-external-16:](https://pkg.go.dev/time#ParseDuration) (e.g. `2160h`, `8760h`).


2. Deploy the cluster:

    ```bash
    kubectl apply -f deploy/cr.yaml -n <namespace>
    ```

Once you create the database with the Operator, it will automatically trigger the cert-manager to create certificates. Whenever you check certificates for expiration, you will find that they are valid and short-term.

## Verify cert-manager resources

After the cluster is created, you can inspect the cert-manager resources:

```bash
# List Issuers
kubectl get issuers -n <namespace>

# List Certificates
kubectl get certificates -n <namespace>

# Check certificate status
kubectl get certificate <cluster-name>-cluster-ca-cert -n <namespace> -o yaml
```

The Operator creates Issuers and Certificates in the same namespace as the cluster. Secrets created by cert-manager follow the same naming as with built-in certificate generation (e.g. `<cluster-name>-cluster-ca-cert`, `<cluster-name>-cluster-cert`, `<cluster-name>-replication-cert`).

## Related

If you want to stop using cert-manager for an existing cluster and use your own TLS Secrets instead, see [Migrate from cert-manager to custom TLS certificates](tls-migrate-from-cert-manager.md).

