# Configure DNS suffix for cross-service discovery

When you run the Percona Operator for PostgreSQL inside a [vcluster](https://www.vcluster.com/), the vcluster introduces its own DNS domain (for example, `mycluster.local`). The Operator resolves service names according to that domain, while external services such as PMM, Prometheus exporters or pgBackRest typically live in the host cluster and use a different domain (for example, `svc.cluster.local`).

Without control over the DNS suffix, the Operator constructs internal service names using the wrong domain. As a result, connections to external monitoring and backup endpoints fail.

The `clusterServiceDNSSuffix` option lets you explicitly define which DNS suffix the Operator uses when constructing internal service names. This ensures correct service discovery whether the Operator runs in a vcluster, the host cluster, or a mixed setup.

## How to configure

Add `clusterServiceDNSSuffix` under `spec` in your Custom Resource. For a vcluster setup, set it to the host cluster's DNS suffix so the Operator can reach services there:

```yaml
spec:
  ...
  clusterServiceDNSSuffix: mycluster.local
  # ... rest of your spec
```

Apply the change:

```bash
kubectl apply -f deploy/cr.yaml -n <namespace>
```
