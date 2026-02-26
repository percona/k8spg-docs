# Migrate from Operator-generated certificates to cert-manager

You can start using cert-manager for TLS certificates lifecycle management if you have previously deployed your cluster without auto-generated certificates. The use of cert-manager provides automatic certificate renewal, configurable validity periods, and centralized certificate management across your Kubernetes cluster.

Read more about cert-manager in [Configure TLS security with the Operator using cert-manager](tls-cert-manager.md).

## Migration steps

1. Export the namespace where the cluster is running as an environment variable:

    ```bash
    export NAMESPACE=<namespace>
    ```

2. [Pause the cluster](pause.md) to stop reconciliation before you change TLS resources. Run the following command to patch your running cluster:

    ```bash
    kubectl patch -n $NAMESPACE pg cluster1 --type merge --patch '{
    "spec": {
      "pause": true}
      }'
    ```

3. Verify the cluster status:

    ```bash
    kubectl get pg cluster1 -n $NAMESPACE
    ```

    Wait until the cluster status is `Stopped`. You can verify with `kubectl get pods -n $NAMESPACE`.

4. Deploy cert-manager. In this guide we install cert-manager with `kubectl`. Refer to [Configure TLS security with the Operator using cert-manager](tls-cert-manager.md#install-cert-manager) for Helm installation instructions.

    ```bash
    kubectl apply -f https://github.com/cert-manager/cert-manager/releases/download/v{{certmanagerrecommended}}/cert-manager.yaml
    ```

    This command installs cert-manager in the default `cert-manager` namespace.

5. Verify that cert-manager is running:

    ```bash
    kubectl get pods -n cert-manager
    ```

6. Delete the Operator-generated TLS Secrets. Replace `<cluster-name>` with your cluster name:

    ```bash
    kubectl delete secret <cluster-name>-cluster-ca-cert <cluster-name>-cluster-cert <cluster-name>-replication-cert -n $NAMESPACE
    ```

    Example for a cluster named `cluster1`:

    ```bash
    kubectl delete secret cluster1-cluster-ca-cert cluster1-cluster-cert cluster1-replication-cert -n default
    ```

7. Resume the cluster. Set `spec.pause` back to `false`:

    ```bash
    kubectl patch -n $NAMESPACE pg cluster1 --type merge --patch '{
    "spec": {
      "pause": false}
      }'
    ```

The Operator detects the missing Secrets, sees cert-manager installed, requests new certificates from cert-manager, creates the Secrets, and resumes the cluster.

### Verify the migration

After the cluster is running, verify that cert-manager resources were created:

```bash
kubectl get issuers -n $NAMESPACE
kubectl get certificates -n $NAMESPACE
kubectl get secret <cluster-name>-cluster-ca-cert <cluster-name>-cluster-cert <cluster-name>-replication-cert -n $NAMESPACE
```

You can configure certificate validity in the Custom Resource. See [Configure the certificate validity](tls-cert-manager.md#configure-the-certificate-validity) for details.
