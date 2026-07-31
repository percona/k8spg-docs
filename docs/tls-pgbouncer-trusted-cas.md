# Trust additional CAs for PgBouncer client mTLS

To establish a mutual TLS (mTLS) between clients and PgBouncer,  PgBouncer must trust the Certificate Authority (CA) that signed the client certificates. 

By default, pgBouncer trusts only the CA that the Operator manages when it creates TLS material for the cluster. 
Client certificates signed by an external CA fail verification. If you provide your custom CA via the `proxy.pgBouncer.customTLSSecret`, pgBouncer trusts that certificate but you need to manage the whole certificate lifecycle yourself. 

You can extend the PgBouncer CA bundle with your external CA. The Operator appends those CAs to the frontend trust bundle that
  PgBouncer uses for client certificate verification. 
As a result, you establish mTLS for external clients and keep automated certificate
management for the cluster.

The same approach works when you already use
`proxy.pgBouncer.customTLSSecret`. The Operator still merges the
additional CA bundles into the trust material that PgBouncer mounts.

## Configure additional trusted CAs

The following steps use Operator-managed certificates and require clients
to present a certificate that your external CA signed.
{.power-number}

1. Create a Secret that holds the CA certificate that signed your client
certificates. Replace `client-ca.crt` with the path to your CA file:

    ```bash
    kubectl create secret generic client-ca \
      --from-file=ca.crt=client-ca.crt \
      -n <namespace>
    ```

2. Reference the Secret in the cluster and configure pgBouncer to verify client certificated. Edit the `deploy/cr.yaml` and specify the following:
  
    * Add the Secret name under `proxy.pgBouncer.additionalTrustedCAs` 
    * set `proxy.pgBouncer.config.global.client_tls_sslmode` to `verify-ca` or `verify-full`:

    ```yaml
    spec:
      proxy:
        pgBouncer:
          additionalTrustedCAs:
            - name: client-ca
          config:
            global:
              client_tls_sslmode: verify-ca
    ```

    You can also use certificate-based authentication with
    `auth_type: cert` in PgBouncer configuration when that matches your
    security model. In both cases, the CA that signed the client certificate
    must appear in the merged frontend trust bundle.

    !!! note

        Changes under `proxy.pgBouncer.config` apply without validation.
        An invalid PgBouncer configuration can make the pooler unavailable.

3. Apply the configuration
    
    ```bash
    kubectl apply -f deploy/cr.yaml -n <namespace>
    ```

 4. Confirm the merged CA bundle

Check that the `<cluster-name>-pgbouncer` Secret contains more than one
certificate in `pgbouncer-frontend.ca-roots`. For a cluster named
`cluster1`:

```bash
kubectl get secret cluster1-pgbouncer -n <namespace> \
  -o jsonpath='{.data.pgbouncer-frontend\.ca-roots}' \
  | base64 --decode \
  | grep -c 'BEGIN CERTIFICATE'
```

The count is at least `2` when the Operator-managed CA and your external
CA are both present.

Propagation of the updated Secret into PgBouncer Pods and the
configuration reload can take a few minutes.

## Connect with a client certificate

Connect through the PgBouncer Service and present the client certificate
and key. The client also verifies the PgBouncer server certificate with
the cluster CA (from `<cluster-name>-cluster-cert` by default):

```bash
psql "host=<cluster-name>-pgbouncer.<namespace>.svc \
  port=5432 \
  dbname=<database> \
  user=<user> \
  sslmode=verify-full \
  sslrootcert=/path/to/cluster-ca.crt \
  sslcert=/path/to/client.crt \
  sslkey=/path/to/client.key"
```

Without a client certificate, or with a certificate signed by a CA that
is not in `additionalTrustedCAs`, PgBouncer rejects the connection when
`client_tls_sslmode` requires verification.

