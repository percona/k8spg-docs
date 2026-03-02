# Configure DNS suffix for service discovery

In Kubernetes, services are assigned a DNS name to be accessible within the cluster. The domain name follows the pattern `<service-name>.<namespace>.svc.<cluster-domain>`. The default cluster domain is `cluster.local`, so a typical FQDN looks like `<service-name>.<namespace>.svc.cluster.local`.

When you refer to a service using only its short name, Kubernetes automatically expands it with this domain so the name resolves inside the cluster. This enables workloads to communicate without the need to specify fully-qualified domain names.

A vcluster or clusters with custom DNS configuration can use a different domain instead of `cluster.local`. In that case, the Operator must know which suffix to use when generating service names. Otherwise, it produces hostnames using the default domain and they do not match the cluster's DNS configuration and service resolution fails.

## User value

The `clusterServiceDNSSuffix` option lets you set the cluster domain as the value the Operator uses when generating service names. As a result, the Operator produces hostnames that match your cluster's DNS configuration, ensuring correct service resolution and discovery.

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
