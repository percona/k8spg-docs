# Transport layer security (TLS)

The Percona Operator for PostgreSQL uses Transport Layer Security
(TLS) cryptographic protocol for the following types of communication:

* Internal - communication between PostgreSQL instances in the cluster
* External - communication between the client application and the cluster

The internal certificate is also used as an authorization method for PostgreSQL
Replica instances.

These certificates are stored in Secrets. The default Secret names are derived from the cluster name. When you deploy a cluster, you see these Secrets:

| Secret | What it is | Who uses it |
| -------- | ------------ | ------------- |
| `<cluster-name>-cluster-ca-cert` | Root certificate authority (CA) for this cluster | Signs the other certificates. Clients use it to verify the server. |
| `<cluster-name>-cluster-cert` | PostgreSQL **server** certificate | Presented to applications (and used when verifying Postgres on the backend of PgBouncer). |
| `<cluster-name>-replication-cert` | **Client** certificate | Used for streaming replication and `pg_rewind` between instances. Postgres accepts only certificate authentication for this user. |
| `<cluster-name>-pgbouncer` | PgBouncer Secret, including its **frontend** TLS material | Presented to applications that connect through PgBouncer. |

## Ways to provide TLS certificates

You can configure TLS in these ways:

| Approach | Best for | Renewal |
| -------- | -------- | ------- |
| Operator-generated certificates (default) | Quick start, development | Manual |
| cert-manager with Operator-managed issuers | Automated TLS without external PKI | Automatic (cert-manager) |
| cert-manager with your existing `ClusterIssuer` or custom issuer | Production clusters that use the organization's PKI | Automatic (cert-manager) |
| Manual Secrets | Full control, air-gapped or custom PKI workflows | Manual |

* Have the Operator generate certificates automatically during cluster creation,
* Use the [cert-manager](tls-cert-manager.md) to manage certificates and their lifecycle. By default the Operator creates namespace-scoped issuers in the database namespace. Starting with Operator 3.1.0, you can also point it at a [`ClusterIssuer`](tls-cert-manager.md#use-an-existing-clusterissuer) so PostgreSQL certificates are signed by your organization's CA,
* [Generate certificates manually](tls-manual.md).

You can [migrate your running cluster to cert-manager](tls-migrate-to-cert-manager.md) to benefit from automatic renewal and centralized management. 

!!! important "Known limitation for Operator 2.9.0"

    If you had **cert-manager** installed and used the Operator-generated TLS certificates, upgrading the Operator to version **2.9.0** could put the cluster in an inconsistent state: the root CA stayed on internal PKI, but leaf certificates were handed to cert-manager. See [TLS and cert-manager (Operator 2.9.0)](limitations.md#tls-and-cert-manager) for more information. 

    To fix this, either [move fully to cert-manager](limitations.md#switch-to-use-only-the-certificates-managed-by-the-cert-manager) or [switch to custom TLS Secrets](tls-migrate-from-cert-manager.md). This issue is fixed in Operator **3.0.0** and later.

Additionally, you can *force* your database cluster to use only encrypted channels for both internal and external communications. To do this, set the `tlsOnly` Custom Resource option to `true`.

### How the Operator chooses TLS source

The Operator can generate long-term certificates and enable TLS encryption automatically during cluster creation.

Upon cluster creation, the Operator reviews the Custom Resource configuration and chooses a TLS source in this order:

* Your custom TLS certificate Secrets if you created and referenced them in the cluster spec.
* [cert-manager](tls-cert-manager.md), if it is installed and no custom Secrets are specified. The Operator generates certificates and issuer and delegates certificate lifecycle management to cert-manager.
* If neither condition is met, the Operator generates the necessary certificates and Secrets itself.

Operator-generated certificates are not renewed automatically by cert-manager. Plan manual rotation if your security policy requires it.

!!! note

    Beginning with version 2.5.0, the Operator creates a dedicated root CA for each cluster. Earlier versions used a single generated root CA for all database clusters.
    
## TLS configuration

The following sections provide guidelines how to:

* [Configure TLS security with the Operator using cert-manager](tls-cert-manager.md)
* [Generate certificates manually](tls-manual.md)
* [Migrate from Operator-generated certificates to cert-manager](tls-migrate-to-cert-manager.md)
* [Migrate from cert-manager to custom TLS certificates](tls-migrate-from-cert-manager.md)
* [Trust additional CAs for PgBouncer client mTLS](tls-pgbouncer-trusted-cas.md)
* [Update certificates](tls-update.md)
* [Configure the TLS certificate management policy](tls-cert-management-policy.md)
* [Check TLS communication to a cluster](tls-verify-communication.md)

## Keep certificates after deleting the cluster

When you [delete the cluster](delete.md), the Operator handles SSL objects (Secrets, certificates, and issuer) as follows:

* The Operator doesn't delete TLS Secrets, certificates, and issuer it generated by default. 
* The Operator removes the namespace-scoped cert-manager Issuers and Certificates it owns (via owner references) but keeps the Secrets.
* Operator-managed cluster-scoped `ClusterIssuer` resources and CA objects in the cert-manager namespace are not owned by the cluster, so they are not deleted automatically. The Operator never deletes an external issuer that it does not own.

If you want to clean up SSL objects, set the `finalizers.percona.com/delete-ssl` finalizer in the Custom Resource. The Operator deletes the TLS Secrets.

## Logical replica connections

A [logical replica](logical-replication.md) presents the cluster TLS certificate. Prefer `sslmode=verify-ca`. Hostname verification (`sslmode=verify-full`) can fail because the certificate SANs may not include the logical replica Service DNS name (`<cluster-name>-lr-<replica-name>`). If you use custom certificates, add that name to the server certificate. See [Generate certificates manually](tls-manual.md).

