# Configure DNS suffix for service discovery

In Kubernetes, services are assigned a DNS name to be accessible within the cluster. The domain name follows the pattern `<service-name>.<namespace>.svc.<cluster-domain>`. The default cluster domain is `cluster.local`, so a typical FQDN looks like `<service-name>.<namespace>.svc.cluster.local`.

When you refer to a service using only its short name, Kubernetes automatically expands it with this domain so the name resolves inside the cluster. This enables workloads to communicate without the need to specify fully-qualified domain names.

Clusters with custom DNS configurations may use a domain suffix different from the default `cluster.local`. This includes scenarios such as running inside a vcluster, which may respond to DNS queries with records that do not match the actual cluster domain.

The Operator tries to auto-detect the cluster's domain suffix by performing a CNAME lookup on the service `kubernetes.default.svc` (that is, a service named `kubernetes` in the `default` namespace). If the lookup returns a value, the Operator uses that as the domain suffix. If the Operator fails to auto-detect the DNS suffix, it falls back to using the default `cluster.local` domain. This may lead to services not resolving properly within the cluster.

To address this, you can set your custom DNS suffix for the Operator to use when it constructs service names. As a result, the Operator produces hostnames that match your cluster's DNS configuration, ensuring correct service resolution and discovery.

## How to configure

Add `clusterServiceDNSSuffix` under `spec` in your Custom Resource. Set it to your cluster's DNS suffix—for example, `cluster.local` for a standard cluster, or the host cluster's suffix when the Operator runs in a vcluster:

```yaml
spec:
  ...
  clusterServiceDNSSuffix: cluster.local
  # ... rest of your spec
```

Apply the change:

```bash
kubectl apply -f deploy/cr.yaml -n <namespace>
```
