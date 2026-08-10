# Configure TLS security with the Operator using cert-manager

Percona Operator for PostgreSQL integrates with [cert-manager :octicons-link-external-16:](https://cert-manager.io/) for TLS certificate management.

When the Operator creates a database cluster, it checks whether cert-manager is installed and whether you have provided custom TLS secrets. If cert-manager is available and you have not set custom secrets, the Operator requests certificates from cert-manager, stores them in Kubernetes Secrets, and uses those Secrets for TLS. cert-manager then manages issuance, renewal, and rotation. You do not need to restart the cluster when certificates are renewed.

You can use cert-manager in these ways:

* **Operator-managed issuers (default)** — The Operator creates a namespace-scoped `Issuer` and a local self-signed CA in the database namespace. For [multi-namespace](cluster-wide.md) deployments, configure a cluster-scoped `ClusterIssuer` instead. Managing `ClusterIssuer` resources requires extra RBAC permissions that are not in the default Operator roles. See [Operator-managed issuers with ClusterIssuer scope](#operator-managed-issuers-with-clusterissuer-scope).

* **Your existing issuer** — Point the Operator at a cert-manager `ClusterIssuer` or another issuer your platform already manages (for example Vault or ACME). Certificates are then signed and renewed under your organization's PKI policies. Percona Distribution for PostgreSQL requires all certificates in a cluster to come from the same CA, so that issuer must sign every leaf certificate the Operator requests (cluster, instance, replication, PgBouncer, and pgBackRest).

If cert-manager is not installed or not ready, the Operator falls back to its built-in certificate generation.

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

=== "with kubectl"

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

At this point you are ready to [install the Operator and deploy a Percona Distribution for PostgreSQL cluster](kubernetes.md).

See the sections below for how you can fine-tune the Operator and cert-manager when managing TLS for your cluster:

## Configure the certificate validity

1. Add the `tls` section to your Custom Resource to set certificate validity durations. These options apply only when cert-manager is used.

    ```yaml
    spec:
      tls:
        certValidityDuration: 2160h   # 90 days for TLS certificates (default: 8760h / 1 year)
        caValidityDuration: 26280h    # 3 years for the CA certificate (default: 8760h / 1 year)
        pgBackRestCertValidityDuration: 2160h # 90 days for pgBackRest TLS certificates
    ```

    Use [Go duration format :octicons-link-external-16:](https://pkg.go.dev/time#ParseDuration) (e.g. `2160h`, `8760h`).


2. Deploy the cluster:

    ```bash
    kubectl apply -f deploy/cr.yaml -n <namespace>
    ```

Once you create the database with the Operator, it will automatically trigger the cert-manager to create certificates. Whenever you check certificates for expiration, you will find that they are valid and short-term.

## Operator-managed namespace-scoped issuers (default)

Once you create the database with the Operator and cert-manager is running, the Operator automatically creates:

* a self-signed CA `Issuer` (`<cluster-name>-ca-issuer`) and CA `Certificate` (`<cluster-name>-cluster-ca-cert`) in the database namespace,
* a signing `Issuer` (`<cluster-name>-tls-issuer`) that references the CA,
* leaf TLS `Certificate` resources for the cluster, instances, replication client, PgBouncer, and pgBackRest.

cert-manager issues short-lived certificates and renews them on schedule. You can optionally set [`tls.issuerConf.name`](operator.md#tlsissuerconfname) with `kind: Issuer` to customize the name of the signing `Issuer` the Operator manages.

## Operator-managed issuers with ClusterIssuer scope

!!! admonition "Version added: [3.1.0](ReleaseNotes/Kubernetes-Operator-for-PostgreSQL-RN3.1.0.md)"

If you want the Operator to manage the CA chain and issue certificates across all namespaces, use the `ClusterIssuer` resource rather than namespace-scoped `Issuer` resources.

The Operator requires additional permissions to create and manage the `ClusterIssuer` resource. Default Operator RBAC covers only namespace-scoped objects. Therefore, you must grant cluster-scoped access to let the Operator create and update the shared CA `ClusterIssuer` resources across the Kubernetes cluster.

1. Create a ClusterRole and ClusterRoleBinding. Replace the `<operator-namespace>` placeholder with the namespace where the Operator is deployed:

    ```bash
    kubectl create clusterrole pg-clusterissuer-manager \
      --verb=get,list,watch,create,update,patch \
      --resource=clusterissuers.cert-manager.io

    kubectl create clusterrolebinding pg-clusterissuer-manager \
      --clusterrole=pg-clusterissuer-manager \
      --serviceaccount=<operator-namespace>:percona-postgresql-operator
    ```

2. Configure the Custom Resource. Set `tls.issuerConf.kind` to `ClusterIssuer` and provide a unique `name`. Do not pre-create issuers yourself for this mode:

    ```yaml
    spec:
      tls:
        issuerConf:
          name: shared-pg-issuer   # required: base name for Operator-managed ClusterIssuers
          kind: ClusterIssuer
          group: cert-manager.io
    ```


3. Apply the configuration. Replace the `<namespace>` with the namespace where your cluster is deployed:
   
    ```bash
    kubectl apply -f deploy/cr.yaml -n <namespace>
    ```

    The Operator creates:

    * a self-signed CA `ClusterIssuer` named `<name>-ca-issuer`,
    * a CA `Certificate` and Secret named `<name>-ca-cert` in the cert-manager namespace (`cert-manager` by default),
    * a CA-backed `ClusterIssuer` named `<name>` that signs leaf certificates,
    * leaf `Certificate` resources in the database namespace that reference the CA-backed `ClusterIssuer`.

If you installed cert-manager in a custom namespace, set the [`CERTMANAGER_NAMESPACE`](env-var-operator.md#certmanager_namespace) environment variable on the Operator Deployment.

## Use an existing ClusterIssuer

!!! admonition "Version added: [3.1.0](ReleaseNotes/Kubernetes-Operator-for-PostgreSQL-RN3.1.0.md)"

If your cluster already runs cert-manager with a cluster-wide issuer, such as Let's Encrypt, Smallstep, or an internal CA, you can configure the Operator to request certificates for Percona Distribution for PostgreSQL from that issuer instead of creating its own CA chain.

Configure the Custom Resource as follows:

```yaml
spec:
  tls:
    issuerConf:
      name: my-org-issuer        # name of your existing ClusterIssuer
      kind: ClusterIssuer
      group: cert-manager.io
```

Replace `my-org-issuer` with the name of your existing `ClusterIssuer`.

When you deploy the cluster, the Operator creates `Certificate` resources that reference your `ClusterIssuer` and cert-manager signs the resulting Secrets. The Operator does not create a parallel CA or overwrite your issuer.

Because the Operator does not manage the root CA in this mode, it reads the CA certificate from the issued leaf Secrets (the `ca.crt` key) when it needs CA material for components such as pgBackRest.

## Use a custom issuer kind

!!! admonition "Version added: [3.1.0](ReleaseNotes/Kubernetes-Operator-for-PostgreSQL-RN3.1.0.md)"

If your platform uses a custom cert-manager issuer type, set `tls.issuerConf` to that issuer's `name`, `kind`, and API `group`. The following configuration example showcases a Vault Issuer:

```yaml
spec:
  tls:
    issuerConf:
      name: vault-issuer
      kind: VaultClusterIssuer
      group: vault.example.com
```

The Operator treats this as an external issuer: it creates only the leaf `Certificate` resources and does not manage a CA chain.

## Verify cert-manager resources

After the cluster is created, you can inspect the cert-manager resources:

=== "Namespace-scoped Issuer (default)"

    ```bash
    # List Issuers
    kubectl get issuers -n <namespace>

    # List Certificates
    kubectl get certificates -n <namespace>

    # Check certificate status
    kubectl get certificate <cluster-name>-cluster-ca-cert -n <namespace> -o yaml
    ```

    The Operator creates Issuers and Certificates in the same namespace as the cluster. Secrets created by cert-manager follow the same naming as with built-in certificate generation (for example, `<cluster-name>-cluster-ca-cert`, `<cluster-name>-cluster-cert`, `<cluster-name>-replication-cert`).

=== "ClusterIssuer"

    ```bash
    # List cluster-scoped issuers
    kubectl get clusterissuer

    # List Certificates in the database namespace
    kubectl get certificates -n <namespace>

    # When the Operator manages the CA chain, check the CA Certificate in the cert-manager namespace
    kubectl get certificate <issuer-name>-ca-cert -n cert-manager -o yaml
    ```

    When the Operator manages the CA chain with `ClusterIssuer`, the CA `Certificate` and its Secret are in the cert-manager namespace, not in the database namespace. Leaf certificate Secrets remain in the database namespace.

    When you use an existing organizational issuer, only your issuer appears among cluster issuers; the Operator creates `Certificate` resources in the database namespace that reference it.

## Operator environment variable

When the Operator manages a CA chain with `tls.issuerConf.kind: ClusterIssuer`, it stores the CA `Certificate` in the cert-manager namespace. By default this namespace is `cert-manager`. If you installed cert-manager elsewhere, set the [`CERTMANAGER_NAMESPACE`](env-var-operator.md#certmanager_namespace) environment variable on the Operator Deployment.

For more details on all cert-manager-related Custom Resource options, see the [`tls.issuerConf` options](operator.md#tlsissuerconfname) in the Operator spec reference.

## Related

If you want to stop using cert-manager for an existing cluster and use your own TLS Secrets instead, see [Migrate from cert-manager to custom TLS certificates](tls-migrate-from-cert-manager.md).
