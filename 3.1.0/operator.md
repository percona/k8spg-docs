> For the complete documentation index, see [llms.txt](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/llms.txt).

# Custom Resource options

The Cluster is configured via the [deploy/cr.yaml](https://github.com/percona/percona-postgresql-operator/blob/main/deploy/cr.yaml) file.

Note

Some options cannot be changed after creation or have specific modification limits. See [Options with modification limits](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/immutable-options.html#custom-resource-options-with-modification-limits) for details.

## `metadata`

The metadata part of this file contains the following keys:

- `name` (`cluster1` by default) sets the name of your Percona Distribution for PostgreSQL Cluster; it should include only [URL-compatible characters](https://datatracker.ietf.org/doc/html/rfc3986#section-2.3) , not exceed 22 characters, start with an alphabetic character, and end with an alphanumeric character;
- `annotations.pgv2.percona.com/custom-patroni-version` [Kubernetes annotation](https://kubernetes.io/docs/concepts/overview/working-with-objects/annotations/) which allows turning off automatic Patroni version detection by the Operator. You can use this annotation to set the version manually (“3” for Patroni 3.x, “4” for Patroni 4.x).
- `finalizers.percona.com/delete-ssl` if present, activates the [Finalizer](https://kubernetes.io/docs/tasks/extend-kubernetes/custom-resources/custom-resource-definitions/#finalizers) which deletes [objects, created for SSL](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/TLS.html) (Secret, certificate, and issuer) after the cluster deletion event (off by default).
- `finalizers.percona.com/delete-pvc` if present, activates the [Finalizer](https://kubernetes.io/docs/tasks/extend-kubernetes/custom-resources/custom-resource-definitions/#finalizers) which deletes [Persistent Volume Claims](https://kubernetes.io/docs/concepts/storage/persistent-volumes/) for the database cluster Pods and user Secrets after the deletion event (off by default).
- `finalizers.percona.com/delete-backups` if present, activates the [Finalizer](https://kubernetes.io/docs/tasks/extend-kubernetes/custom-resources/custom-resource-definitions/#finalizers) which deletes all the [backups](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/backups.html) of the database cluster from all configured repos on cluster deletion event (off by default). **`delete-backups` finalizer is in tech preview state, and it is not yet recommended for production environments.**

## Top level `spec` elements

The spec part of the [deploy/cr.yaml](https://github.com/percona/percona-postgresql-operator/blob/main/deploy/cr.yaml) file contains the following:

### `crVersion`

Version of the Operator the Custom Resource belongs to.

| Value type | Example |
| ---------- | ------- |
| string     | `3.1.0` |

### `clusterServiceDNSSuffix`

A custom cluster domain to be used as a DNS suffix used when constructing internal service names. Use this when the Operator runs in a vcluster or a cluster with a custom DNS domain so it can correctly resolve services. See [Configure DNS suffix for service discovery](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/dns-suffix.html) for details.

| Value type | Example         |
| ---------- | --------------- |
| string     | `cluster.local` |

### `metadata.annotations`

The [Kubernetes annotations](https://kubernetes.io/docs/concepts/overview/working-with-objects/annotations/) metadata to be set at a global level for all resources created by the Operator.

| Value type | Example                     |
| ---------- | --------------------------- |
| label      | `example-annotation: value` |

### `metadata.labels`

The [Kubernetes labels](https://kubernetes.io/docs/concepts/overview/working-with-objects/labels/) metadata to be set at a global level for all resources created by the Operator.

| Value type | Example                |
| ---------- | ---------------------- |
| label      | `example-label: value` |

### `tlsOnly`

Enforce the Operator to use only Transport Layer Security (TLS) for both internal and external communications.

| Value type | Example |
| ---------- | ------- |
| boolean    | `false` |

### `tls.certManagementPolicy`

Controls how the Operator creates and manages TLS certificates, including when TLS Secrets are missing and whether cert-manager is used. You can set this option only when you create the cluster; you cannot change it later. Supported values are:

- `auto` (default) — If TLS Secrets are missing, the Operator creates new certificates automatically. If [cert-manager](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/tls-cert-manager.html) is installed, the Operator uses it, including `spec.tls.issuerConf` when you set it.
- `userProvidedOnly` — The Operator does not create or replace TLS certificates if a TLS Secret is temporarily unavailable. Certificate lifecycle stays entirely under user control. The Operator reports the `TLSSecretsReady=False` cluster condition and pauses the reconciliation. Restore the Secrets to return the cluster to a healthy state.
- `operatorProvidedOnly` — The Operator always generates and manages TLS with its own PKI. It does not use cert-manager and ignores `spec.tls.issuerConf`. Use this when cert-manager is installed in the cluster but you want PostgreSQL to stay on Operator-generated certificates.

See [Configure the TLS certificate management policy](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/tls-cert-management-policy.html) for details.

| Value type | Example |
| ---------- | ------- |
| string     | `auto`  |

### `tls.certValidityDuration`

Validity duration for TLS certificates (cluster, instance, and PgBouncer). Used only when [cert-manager](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/tls-cert-manager.html) manages certificates. Format: Go duration (e.g. `2160h`). Default: `8760h` (1 year).

| Value type | Example |
| ---------- | ------- |
| string     | `2160h` |

### `tls.caValidityDuration`

Validity duration for the root CA certificate. Used only when [cert-manager](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/tls-cert-manager.html) manages certificates. Format: Go duration (e.g. `26280h`). Default: `8760h` (1 year).

| Value type | Example  |
| ---------- | -------- |
| string     | `26280h` |

### `tls.pgBackRestCertValidityDuration`

Validity duration for the `pgBackRest` client and repository host certificates. Used only when [cert-manager](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/tls-cert-manager.html) manages certificates. Format: Go duration (e.g. `2160h`). Default: `8760h` (1 year).

| Value type | Example |
| ---------- | ------- |
| string     | `2160h` |

The [`tls.issuerConf`](#tlsissuerconfname) options below control which cert-manager issuer signs PostgreSQL TLS certificates.

### `tls.issuerConf.name`

The name of the cert-manager [Issuer or ClusterIssuer](https://cert-manager.io/docs/concepts/issuer/) resource that signs PostgreSQL TLS certificates.

- For Operator-managed namespace-scoped issuers, leave this unset to use the default `<cluster-name>-tls-issuer` name, or set it to customize that Issuer name.
- For Operator-managed `ClusterIssuer` scope, set a unique base name. The Operator creates `<name>-ca-issuer`, `<name>-ca-cert`, and the CA-backed `<name>` ClusterIssuer.
- For an existing organizational `ClusterIssuer` or a custom issuer kind, set this to the name of that issuer. The Operator creates `Certificate` resources that reference it and does not create its own CA chain.

See [Use an existing ClusterIssuer](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/tls-cert-manager.html#use-an-existing-clusterissuer) for setup steps.

| Value type | Example         |
| ---------- | --------------- |
| string     | `my-org-issuer` |

### `tls.issuerConf.kind`

The cert-manager [issuer type](https://cert-manager.io/docs/configuration/) referenced by PostgreSQL `Certificate` resources.

Supported values:

- `Issuer` (default) — namespace-scoped issuer in the database namespace.

- `ClusterIssuer` — cluster-scoped issuer. Available starting with Operator 3.1.0.

  Use this when the Operator should manage a shared CA chain across namespaces, or when your platform team manages a cluster-wide issuer. Read more in the [Operator-managed issuers with ClusterIssuer scope](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/tls-cert-manager.html#operator-managed-issuers-with-clusterissuer-scope) and [Use an existing ClusterIssuer](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/tls-cert-manager.html#use-an-existing-clusterissuer).

- Any other issuer kind (for example, a Vault-backed custom resource). It is treated as an external issuer. See [Use a custom issuer kind](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/tls-cert-manager.html#use-a-custom-issuer-kind).

| Value type | Example         |
| ---------- | --------------- |
| string     | `ClusterIssuer` |

### `tls.issuerConf.group`

The API group for the issuer referenced in `issuerConf`. Use `cert-manager.io` for built-in cert-manager certificate issuers.

| Value type | Example           |
| ---------- | ----------------- |
| string     | `cert-manager.io` |

### `standby.enabled`

Enables or disables running the cluster in a standby mode (read-only copy of an existing cluster, useful for disaster recovery, etc).

| Value type | Example |
| ---------- | ------- |
| boolean    | `false` |

### `standby.host`

Host address of the primary cluster this standby cluster connects to.

| Value type | Example          |
| ---------- | ---------------- |
| string     | `"<primary-ip>"` |

### `standby.port`

Port number used by a standby copy to connect to the primary cluster.

| Value type | Example            |
| ---------- | ------------------ |
| string     | `"<primary-port>"` |

### `openshift`

Set to `true` if the cluster is being deployed on OpenShift, set to `false` otherwise, or unset it for auto-detection.

| Value type | Example |
| ---------- | ------- |
| boolean    | `true`  |

### `autoCreateUserSchema`

If set to `true`, the cluster will have automatically created schemas for the [custom user](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/users.html#custom-users-and-databases) defined in the `spec.users` subsection for all of the databases listed for this specific user.

| Value type | Example |
| ---------- | ------- |
| boolean    | `true`  |

### `standby.repoName`

Name of the pgBackRest repository in the primary cluster this standby cluster connects to.

| Value type | Example |
| ---------- | ------- |
| string     | `repo1` |

### `standby.maxAcceptableLag`

The maximum amount of WAL data that the standby cluster can be behind the primary cluster. It is measured in bytes of WAL data. When the WAL lag exceeds this value, the primary pod in the standby cluster is marked as unready, the cluster goes into the `initializing` state, and a `StandbyLagging` condition is set in the status. If unset, lag is not checked. Use Kubernetes quantity format (for example, `10Mi`, `1Gi`).

| Value type | Example |
| ---------- | ------- |
| string     | `10Mi`  |

### `logicalReplicas.name`

Name of a [logical replica](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/logical-replication.html). Required. This name is used in the StatefulSet, Service, PVC, publications, subscriptions, and replication slots. Must be unique, 20 characters max, match `^[a-z][a-z0-9-]*[a-z0-9]$`, and must not collide with `spec.instances[].name`. Requires Operator 3.1.0 or later and `postgresVersion` 17 or later.

| Value type | Example     |
| ---------- | ----------- |
| string     | `analytics` |

### `logicalReplicas.databases`

Databases that keep receiving changes after the full seed. If omitted, all databases receive changes except templates and `postgres`. Every table in the listed databases is included.

| Value type | Example      |
| ---------- | ------------ |
| array      | `- cluster1` |

### `logicalReplicas.bootstrapMethod`

How the data volume is seeded before conversion: `pgbackrest` (default) or `pg_basebackup`. Use `pg_basebackup` when backups are disabled. The Operator reads this only during bootstrap; changing it later has no effect.

| Value type | Example      |
| ---------- | ------------ |
| string     | `pgbackrest` |

### `logicalReplicas.dataVolumeClaimSpec`

Required. PersistentVolumeClaim spec for the replica data directory.

| Value type | Example                                                                  |
| ---------- | ------------------------------------------------------------------------ |
| subdoc     | `accessModes:   - ReadWriteOnce resources:   requests:     storage: 1Gi` |

### `logicalReplicas.resources`

CPU and memory requests and limits for the logical replica Pod.

### `logicalReplicas.affinity`

Pod affinity and anti-affinity for the logical replica.

### `logicalReplicas.tolerations`

Tolerations for the logical replica Pod.

### `logicalReplicas.priorityClassName`

Priority class for the logical replica Pod.

### `logicalReplicas.metadata`

Labels and annotations for logical replica objects.

### `logicalReplicas.expose`

Service settings for the logical replica (`type`, `annotations`, `labels`, `loadBalancerSourceRanges`). See [Exposing the cluster](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/expose.html).

### `secrets.customRootCATLSSecret.name`

Name of the secret with the custom root CA certificate and key for secure connections to the PostgreSQL server, see [Transport Layer Security (TLS)](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/TLS.html) for details.

| Value type | Example            |
| ---------- | ------------------ |
| string     | `cluster1-ca-cert` |

### `secrets.customRootCATLSSecret.items`

Key-value pairs of the `key` (a key from the `secrets.customRootCATLSSecret.name` secret) and the `path` (name on the file system) for the custom root certificate and key. See [Transport Layer Security (TLS)](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/TLS.html) for details.

| Value type | Example                                                                   |
| ---------- | ------------------------------------------------------------------------- |
| subdoc     | `- key: “tls.crt”   path: “root.crt” - key: “tls.key”   path: “root.key”` |

### `secrets.customTLSSecret.name`

Name of the Secret with the PostgreSQL **server** TLS certificate used for external communications. Use this when you provide certificates yourself. If you set this field, you must also set `secrets.customReplicationTLSSecret`, and both Secrets must use the same `ca.crt`. See [Transport Layer Security (TLS)](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/TLS.html) for details.

| Value type | Example         |
| ---------- | --------------- |
| string     | `cluster1-cert` |

### `secrets.customReplicationTLSSecret.name`

Name of the Secret with the **replication client** TLS certificate (`tls.crt`, `tls.key`, and `ca.crt`) used for streaming replication and `pg_rewind`. Use this when you provide certificates yourself. If you set this field, you must also set `secrets.customTLSSecret`, and both Secrets must use the same `ca.crt`. See [Transport Layer Security (TLS)](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/TLS.html) for details.

| Value type | Example             |
| ---------- | ------------------- |
| string     | `replication1-cert` |

### `users.name`

The name of the PostgreSQL user.

| Value type | Example |
| ---------- | ------- |
| string     | `rhino` |

### `users.databases`

Databases accessible by a specific PostgreSQL user with rights to create objects in them (the option is ignored for `postgres` user; also, modifying it can’t be used to revoke the already given access).

| Value type | Example |
| ---------- | ------- |
| string     | `zoo`   |

### `users.password.type`

The set of characters used for password generation: can be either `ASCII` (default) or `AlphaNumeric`.

| Value type | Example |
| ---------- | ------- |
| string     | `ASCII` |

### `users.options`

The `ALTER ROLE` options other than password (the option is ignored for `postgres` user).

| Value type | Example       |
| ---------- | ------------- |
| string     | `"SUPERUSER"` |

### `users.secretName`

The custom name of the user’s Secret; if not specified, the default `<clusterName>-pguser-<userName>` variant will be used.

| Value type | Example               |
| ---------- | --------------------- |
| string     | `"rhino-credentials"` |

### `users.grantPublicSchemaAccess`

Grants access to the `public` schema to the user for all databases associated with this user.

| Value type | Example |
| ---------- | ------- |
| string     | `false` |

### `authentication.rules`

Defines additional authentication rules for PostgreSQL host-based authentication (`pg_hba.conf`). Rules are applied after mandatory Operator rules and before the default `scram-sha-256` fallback. Use this to configure [LDAP authentication](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/ldap-setup.html).

| Value type | Example                                                                                                          |
| ---------- | ---------------------------------------------------------------------------------------------------------------- |
| array      | See [LDAP authentication](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/LDAP.html) for examples |

### `authentication.rules.connection`

Connection type for the rule: `local`, `host`, `hostssl`, `hostnossl`, `hostgssenc`, or `hostnogssenc`.

| Value type | Example |
| ---------- | ------- |
| string     | `host`  |

### `authentication.rules.method`

Authentication method to use when a connection matches this rule (e.g., `ldap`, `scram-sha-256`, `md5`).

| Value type | Example |
| ---------- | ------- |
| string     | `ldap`  |

### `authentication.rules.users`

Users to match. An empty list matches all users.

| Value type | Example       |
| ---------- | ------------- |
| array      | `["percona"]` |

### `authentication.rules.databases`

Databases to match. An empty list matches all databases.

| Value type | Example       |
| ---------- | ------------- |
| array      | `["percona"]` |

### `authentication.rules.options`

Options for the authentication method. Supported LDAP authentication options are:

- `ldapserver` - the LDAP server hostname
- `ldapport` - the port on which the LDAP server is reachable: `389` for plain LDAP and `636` for LDAPS
- `ldaptls` - Controls the connection type for the LDAP server. `1` is for LDAP over TLS.
- `ldapscheme` - Specifies the connection type. An alternative to `ldaptls`. Must be supported by LDAP server implementations.
- `ldapprefix` - A prefix for the username when constructing the DN. Use this option for Plain LDAP.
- `ldappsuffix` - A suffix for the username when constructing the DN. Use this option for Plain LDAP.
- `ldapbasedn` - The root DN in your LDAP directory tree where to start searching for the user. Use it for search+bind mode.
- `ldapbinddn` - The bind user DN that will be used for initial bind to LDAP server and username search. Use it for search+bind mode.
- `ldapbindpasswd` - The bind user password. Use it for search+bind mode.
- `ldapsearchattribute` - The attribute to match against when searching for the user. When not specified, the `uid` attribute will be used.

To learn more about LDAP, see [LDAP authentication](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/LDAP.html) and the [PostgreSQL auth-ldap documentation](https://www.postgresql.org/docs/current/auth-ldap.html) .

| Value type | Example                                                                                             |
| ---------- | --------------------------------------------------------------------------------------------------- |
| subdoc     | `ldapserver: openldap ldapport: “389” ldapprefix: “uid=” ldapsuffix: “,ou=users,dc=example,dc=com”` |

### `authentication.rules.hba`

The authentication rules specified as a raw `pg_hba.conf` line. When non-empty, this line is used as-is and the structured fields are ignored.

| Value type | Example                         |
| ---------- | ------------------------------- |
| string     | `"host all all 10.0.0.0/8 md5"` |

### `config.files.secret.name`

The name of the Secret object that stores the CA certificates for [LDAP over TLS (LDAPS)](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/ldap-setup.html#ldaps-ldap-over-tls). The Operator mounts this certificate under `/etc/postgres`.

| Value type | Example |
| ---------- | ------- |
| string     | ldap-ca |

### `config.files.secret.items.key`

The CA certificates to use for [LDAP over TLS (LDAPS)](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/ldap-setup.html#ldaps-ldap-over-tls).

| Value type | Example |
| ---------- | ------- |
| string     | ca.crt  |

### `config.files.secret.items.path`

The path to the CA certificates to use for [LDAP over TLS (LDAPS)](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/ldap-setup.html#ldaps-ldap-over-tls).

| Value type | Example     |
| ---------- | ----------- |
| string     | ldap-ca.crt |

### `databaseInitSQL.key`

Data key for the [Custom configuration options ConfigMap](https://kubernetes.io/docs/concepts/configuration/configmap/) with the init SQL file, which will be executed at cluster creation time.

| Value type | Example    |
| ---------- | ---------- |
| string     | `init.sql` |

### `databaseInitSQL.name`

Name of the [ConfigMap](https://kubernetes.io/docs/concepts/configuration/configmap/) with the init SQL file, which will be executed at cluster creation time.

| Value type | Example             |
| ---------- | ------------------- |
| string     | `cluster1-init-sql` |

### `pause`

Setting it to `true` gracefully stops the cluster, scaling workloads to zero and suspending CronJobs; setting it to `false` after shut down starts the cluster back.

| Value type | Example |
| ---------- | ------- |
| string     | `false` |

### `unmanaged`

Setting it to `true` stops the Operator’s activity including the rollout and reconciliation of changes made in the Custom Resource; setting it to `false` starts the Operator’s activity back.

| Value type | Example |
| ---------- | ------- |
| string     | `false` |

## `dataSource` subsection

Contains the configuration options for restoring from a backup onto a new cluster. For usage examples, see [Restore the backup to a new cluster (cluster clone)](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/backups-clone.html).

### `dataSource.postgresCluster.clusterName`

Name of an existing cluster to use as the data source when restoring backup to a new cluster.

| Value type | Example    |
| ---------- | ---------- |
| string     | `cluster1` |

## `dataSource.postgresCluster.clusterNamespace`

Namespace of an existing cluster used as a data source (is needed if the new cluster will be created in a different namespace; needs the Operator deployed [in multi-namespace/cluster-wide mode](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/cluster-wide.html#install-the-operator-cluster-wide)).

| Value type | Example              |
| ---------- | -------------------- |
| string     | `cluster1-namespace` |

### `dataSource.postgresCluster.repoName`

Name of the pgBackRest repository in the source cluster that contains the backup to be restored to a new cluster.

| Value type | Example |
| ---------- | ------- |
| string     | `repo1` |

### `dataSource.postgresCluster.options`

The pgBackRest command-line options for the pgBackRest restore command.

| Value type | Example |
| ---------- | ------- |
| string     |         |

### `dataSource.postgresCluster.tolerations.effect`

The [Kubernetes Pod tolerations](https://kubernetes.io/docs/concepts/configuration/taint-and-toleration/#concepts) effect for data migration.

| Value type | Example      |
| ---------- | ------------ |
| string     | `NoSchedule` |

### `dataSource.postgresCluster.tolerations.key`

The [Kubernetes Pod tolerations](https://kubernetes.io/docs/concepts/configuration/taint-and-toleration/#concepts) key for data migration.

| Value type | Example |
| ---------- | ------- |
| string     | `role`  |

### `dataSource.postgresCluster.tolerations.operator`

The [Kubernetes Pod tolerations](https://kubernetes.io/docs/concepts/configuration/taint-and-toleration/#concepts) operator for data migration.

| Value type | Example |
| ---------- | ------- |
| string     | `Equal` |

### `dataSource.postgresCluster.tolerations.value`

The [Kubernetes Pod tolerations](https://kubernetes.io/docs/concepts/configuration/taint-and-toleration/#concepts) value for data migration.

| Value type | Example              |
| ---------- | -------------------- |
| string     | `connection-poolers` |

### `dataSource.pgbackrest.stanza`

Name of the [pgBackRest stanza](https://pgbackrest.org/command.html) to use as the data source when restoring backup to a new cluster.

| Value type | Example |
| ---------- | ------- |
| string     | `db`    |

### `dataSource.pgbackrest.configuration.secret.name`

Name of the [Kubernetes Secret object](https://kubernetes.io/docs/concepts/configuration/secret/#using-imagepullsecrets) with custom pgBackRest configuration, which will be added to the pgBackRest configuration generated by the Operator.

| Value type | Example        |
| ---------- | -------------- |
| string     | `pgo-s3-creds` |

### `dataSource.pgbackrest.global`

Settings, which are to be included in the `global` section of the pgBackRest configuration generated by the Operator.

| Value type | Example                                     |
| ---------- | ------------------------------------------- |
| subdoc     | `/pgbackrest/postgres-operator/hippo/repo1` |

### `dataSource.pgbackrest.repo.name`

Name of the pgBackRest repository.

| Value type | Example |
| ---------- | ------- |
| string     | `repo1` |

### `dataSource.pgbackrest.repo.s3.bucket`

The [Amazon S3 bucket](https://docs.aws.amazon.com/AmazonS3/latest/dev/UsingBucket.html) or [Google Cloud Storage bucket](https://cloud.google.com/storage/docs/key-terms#buckets) name used for backups. Bucket name should follow [Amazon naming rules](https://docs.aws.amazon.com/AmazonS3/latest/userguide/bucketnamingrules.html) or [Google naming rules](https://cloud.google.com/storage/docs/buckets), and additionally, it can’t contain dots.

| Value type | Example       |
| ---------- | ------------- |
| string     | `"my-bucket"` |

### `dataSource.pgbackrest.repo.s3.endpoint`

The endpoint URL of the S3-compatible storage to be used for backups (not needed for the original Amazon S3 cloud).

| Value type | Example                           |
| ---------- | --------------------------------- |
| string     | `"s3.ca-central-1.amazonaws.com"` |

### `dataSource.pgbackrest.repo.s3.region`

The [AWS region](https://docs.aws.amazon.com/general/latest/gr/rande.html) to use for Amazon and all S3-compatible storages.

| Value type | Example          |
| ---------- | ---------------- |
| boolean    | `"ca-central-1"` |

### `dataSource.pgbackrest.tolerations.effect`

The [Kubernetes Pod tolerations](https://kubernetes.io/docs/concepts/configuration/taint-and-toleration/#concepts) effect for pgBackRest at data migration.

| Value type | Example      |
| ---------- | ------------ |
| string     | `NoSchedule` |

### `dataSource.pgbackrest.tolerations.key`

The [Kubernetes Pod tolerations](https://kubernetes.io/docs/concepts/configuration/taint-and-toleration/#concepts) key for pgBackRest at data migration.

| Value type | Example |
| ---------- | ------- |
| string     | `role`  |

### `dataSource.pgbackrest.tolerations.operator`

The [Kubernetes Pod tolerations](https://kubernetes.io/docs/concepts/configuration/taint-and-toleration/#concepts) operator for pgBackRest at data migration.

| Value type | Example |
| ---------- | ------- |
| string     | `Equal` |

### `dataSource.pgbackrest.tolerations.value`

The [Kubernetes Pod tolerations](https://kubernetes.io/docs/concepts/configuration/taint-and-toleration/#concepts) value for pgBackRest at data migration.

| Value type | Example              |
| ---------- | -------------------- |
| string     | `connection-poolers` |

### `dataSource.volumes.pgDataVolume.pvcName`

The PostgreSQL data volume name for the [Persistent Volume Claim](https://kubernetes.io/docs/concepts/storage/persistent-volumes/) used for data migration.

| Value type | Example    |
| ---------- | ---------- |
| string     | `cluster1` |

### `dataSource.volumes.pgDataVolume.directory`

The mount point for PostgreSQL data volume used for data migration.

| Value type | Example    |
| ---------- | ---------- |
| string     | `cluster1` |

### `dataSource.volumes.pgDataVolume.tolerations.effect`

The [Kubernetes Pod tolerations](https://kubernetes.io/docs/concepts/configuration/taint-and-toleration/#concepts) effect for PostgreSQL data volume used for data migration.

| Value type | Example      |
| ---------- | ------------ |
| string     | `NoSchedule` |

### `dataSource.volumes.pgDataVolume.tolerations.key`

The [Kubernetes Pod tolerations](https://kubernetes.io/docs/concepts/configuration/taint-and-toleration/#concepts) key for PostgreSQL data volume used for data migration.

| Value type | Example |
| ---------- | ------- |
| string     | `role`  |

### `dataSource.volumes.pgDataVolume.tolerations.operator`

The [Kubernetes Pod tolerations](https://kubernetes.io/docs/concepts/configuration/taint-and-toleration/#concepts) operator for PostgreSQL data volume used for data migration.

| Value type | Example |
| ---------- | ------- |
| string     | `Equal` |

### `dataSource.volumes.pgDataVolume.tolerations.value`

The [Kubernetes Pod tolerations](https://kubernetes.io/docs/concepts/configuration/taint-and-toleration/#concepts) value for PostgreSQL data volume used for data migration.

| Value type | Example              |
| ---------- | -------------------- |
| string     | `connection-poolers` |

### `dataSource.volumes.pgDataVolume.annotations`

The [Kubernetes annotations](https://kubernetes.io/docs/concepts/overview/working-with-objects/annotations/) metadata for PostgreSQL data volume used for data migration.

| Value type | Example                  |
| ---------- | ------------------------ |
| label      | `test-annotation: value` |

### `dataSource.volumes.pgDataVolume.labels`

The [Kubernetes labels](https://kubernetes.io/docs/concepts/overview/working-with-objects/labels/) for PostgreSQL data volume used for data migration.

| Value type | Example             |
| ---------- | ------------------- |
| label      | `test-label: value` |

### `dataSource.volumes.pgWALVolume.pvcName`

The PostgreSQL write-ahead logs volume name for the [Persistent Volume Claim](https://kubernetes.io/docs/concepts/storage/persistent-volumes/) used for data migration.

| Value type | Example    |
| ---------- | ---------- |
| string     | `cluster1` |

### `dataSource.volumes.pgWALVolume.directory`

The mount point for PostgreSQL write-ahead logs volume used for data migration.

| Value type | Example    |
| ---------- | ---------- |
| string     | `cluster1` |

### `dataSource.volumes.pgWALVolume.tolerations.effect`

The [Kubernetes Pod tolerations](https://kubernetes.io/docs/concepts/configuration/taint-and-toleration/#concepts) effect for PostgreSQL write-ahead logs volume used for data migration.

| Value type | Example      |
| ---------- | ------------ |
| string     | `NoSchedule` |

### `dataSource.volumes.pgWALVolume.tolerations.key`

The [Kubernetes Pod tolerations](https://kubernetes.io/docs/concepts/configuration/taint-and-toleration/#concepts) key for PostgreSQL write-ahead logs volume used for data migration.

| Value type | Example |
| ---------- | ------- |
| string     | `role`  |

### `dataSource.volumes.pgWALVolume.tolerations.operator`

The [Kubernetes Pod tolerations](https://kubernetes.io/docs/concepts/configuration/taint-and-toleration/#concepts) operator for PostgreSQL write-ahead logs volume used for data migration.

| Value type | Example |
| ---------- | ------- |
| string     | `Equal` |

### `dataSource.volumes.pgWALVolume.tolerations.value`

The [Kubernetes Pod tolerations](https://kubernetes.io/docs/concepts/configuration/taint-and-toleration/#concepts) value for PostgreSQL write-ahead logs volume used for data migration.

| Value type | Example              |
| ---------- | -------------------- |
| string     | `connection-poolers` |

### `dataSource.volumes.pgWALVolume.annotations`

The [Kubernetes annotations](https://kubernetes.io/docs/concepts/overview/working-with-objects/annotations/) metadata for PostgreSQL write-ahead logs volume used for data migration.

| Value type | Example                  |
| ---------- | ------------------------ |
| label      | `test-annotation: value` |

### `dataSource.volumes.pgWALVolume.labels`

The [Kubernetes labels](https://kubernetes.io/docs/concepts/overview/working-with-objects/labels/) for PostgreSQL write-ahead logs volume used for data migration.

| Value type | Example             |
| ---------- | ------------------- |
| label      | `test-label: value` |

### `dataSource.volumes.pgBackRestVolume.pvcName`

The pgBackRest volume name for the [Persistent Volume Claim](https://kubernetes.io/docs/concepts/storage/persistent-volumes/) used for data migration.

| Value type | Example    |
| ---------- | ---------- |
| string     | `cluster1` |

### `dataSource.volumes.pgBackRestVolume.directory`

The mount point for pgBackRest volume used for data migration.

| Value type | Example    |
| ---------- | ---------- |
| string     | `cluster1` |

### `dataSource.volumes.pgBackRestVolume.tolerations.effect`

The [Kubernetes Pod tolerations](https://kubernetes.io/docs/concepts/configuration/taint-and-toleration/#concepts) effect pgBackRest volume used for data migration.

| Value type | Example      |
| ---------- | ------------ |
| string     | `NoSchedule` |

### `dataSource.volumes.pgBackRestVolume.tolerations.key`

The [Kubernetes Pod tolerations](https://kubernetes.io/docs/concepts/configuration/taint-and-toleration/#concepts) key for pgBackRest volume used for data migration.

| Value type | Example |
| ---------- | ------- |
| string     | `role`  |

### `dataSource.volumes.pgBackRestVolume.tolerations.operator`

The [Kubernetes Pod tolerations](https://kubernetes.io/docs/concepts/configuration/taint-and-toleration/#concepts) operator for pgBackRest volume used for data migration.

| Value type | Example |
| ---------- | ------- |
| string     | `Equal` |

### `dataSource.volumes.pgBackRestVolume.tolerations.value`

The [Kubernetes Pod tolerations](https://kubernetes.io/docs/concepts/configuration/taint-and-toleration/#concepts) value for pgBackRest volume used for data migration.

| Value type | Example              |
| ---------- | -------------------- |
| string     | `connection-poolers` |

### `dataSource.volumes.pgBackRestVolume.annotations`

The [Kubernetes annotations](https://kubernetes.io/docs/concepts/overview/working-with-objects/annotations/) metadata for pgBackRest volume used for data migration.

| Value type | Example                  |
| ---------- | ------------------------ |
| label      | `test-annotation: value` |

### `dataSource.volumes.pgBackRestVolume.labels`

The [Kubernetes labels](https://kubernetes.io/docs/concepts/overview/working-with-objects/labels/) for pgBackRest volume used for data migration.

| Value type | Example             |
| ---------- | ------------------- |
| label      | `test-label: value` |

### `dataSource.apiGroup`

The name of the VolumeSnapshot API. It is required for bootstrapping a new cluster from a PVC snapshot.

| Value type | Example                   |
| ---------- | ------------------------- |
| string     | `snapshot.storage.k8s.io` |

### `dataSource.kind`

Specifies what kind of resources serves as the data source

| Value type | Example          |
| ---------- | ---------------- |
| string     | `VolumeSnapshot` |

### `dataSource.name`

Specifies what name of the PVC snapshot backup will be used as a data source for the restore.

| Value type | Example                   |
| ---------- | ------------------------- |
| string     | `my-snapshot-backup-data` |

### `image`

The PostgreSQL Docker image to use.

| Value type | Example                                                             |
| ---------- | ------------------------------------------------------------------- |
| string     | `perconalab/percona-postgresql-operator:3.1.0-ppg18.6.1-3-postgres` |

### `imagePullPolicy`

This option is used to set the [policy](https://kubernetes.io/docs/concepts/containers/images/#updating-images) for updating PostgreSQL images.

| Value type | Example  |
| ---------- | -------- |
| string     | `Always` |

### `postgresVersion`

The major version of PostgreSQL to use.

| Value type | Example |
| ---------- | ------- |
| int        | `16`    |

### `port`

The port number for PostgreSQL.

| Value type | Example |
| ---------- | ------- |
| int        | `5432`  |

### `expose.annotations`

The [Kubernetes annotations](https://kubernetes.io/docs/concepts/overview/working-with-objects/annotations/) metadata for PostgreSQL primary.

| Value type | Example                 |
| ---------- | ----------------------- |
| label      | `my-annotation: value1` |

### `expose.labels`

Set [labels](https://kubernetes.io/docs/concepts/overview/working-with-objects/labels/) for the PostgreSQL primary.

| Value type | Example            |
| ---------- | ------------------ |
| label      | `my-label: value2` |

### `expose.type`

Specifies the type of [Kubernetes Service](https://kubernetes.io/docs/concepts/services-networking/service/#publishing-services-service-types) for PostgreSQL primary.

| Value type | Example        |
| ---------- | -------------- |
| string     | `LoadBalancer` |

### `expose.loadBalancerClass`

Define the implementation of the load balancer you want to use. This setting enables you to select a custom or specific load balancer class instead of the default one provided by the cloud provider.

| Value type | Example                 |
| ---------- | ----------------------- |
| string     | `eks.amazonaws.com/nlb` |

### `expose.loadBalancerSourceRanges`

The range of client IP addresses from which the load balancer should be reachable (if not set, there is no limitations).

| Value type | Example        |
| ---------- | -------------- |
| string     | `"10.0.0.0/8"` |

### `exposeReplicas.annotations`

The [Kubernetes annotations](https://kubernetes.io/docs/concepts/overview/working-with-objects/annotations/) metadata for PostgreSQL replicas.

| Value type | Example                 |
| ---------- | ----------------------- |
| label      | `my-annotation: value1` |

### `exposeReplicas.labels`

Set [labels](https://kubernetes.io/docs/concepts/overview/working-with-objects/labels/) for the PostgreSQL replicas.

| Value type | Example            |
| ---------- | ------------------ |
| label      | `my-label: value2` |

### `exposeReplicas.type`

Specifies the type of [Kubernetes Service](https://kubernetes.io/docs/concepts/services-networking/service/#publishing-services-service-types) for PostgreSQL replicas.

| Value type | Example        |
| ---------- | -------------- |
| string     | `LoadBalancer` |

### `exposeReplicas.loadBalancerClass`

Define the implementation of the load balancer you want to use. This setting enables you to select a custom or specific load balancer class instead of the default one provided by the cloud provider.

| Value type | Example                 |
| ---------- | ----------------------- |
| string     | `eks.amazonaws.com/nlb` |

### `exposeReplicas.loadBalancerSourceRanges`

The range of client IP addresses from which the load balancer should be reachable (if not set, there is no limitations).

| Value type | Example        |
| ---------- | -------------- |
| string     | `"10.0.0.0/8"` |

## Instances section

The `instances` section in the [deploy/cr.yaml](https://github.com/percona/percona-postgresql-operator/blob/main/deploy/cr.yaml) file contains configuration options for PostgreSQL instances. This section contains at least one *cluster instance* with a number of *PostgreSQL instances* in it (cluster instances are groups of PostgreSQL instances used for fine-grained resources assignment).

### `instances.metadata.labels`

Set [labels](https://kubernetes.io/docs/concepts/overview/working-with-objects/labels/) for PostgreSQL Pods.

| Value type | Example                      |
| ---------- | ---------------------------- |
| label      | `pg-cluster-label: cluster1` |

### `instances.name`

The name of the PostgreSQL instance.

| Value type | Example |
| ---------- | ------- |
| string     | `rs 0`  |

### `instances.replicas`

The number of Replicas to create for the PostgreSQL instance.

| Value type | Example |
| ---------- | ------- |
| int        | `3`     |

### `instances.env.name`

Name of an environment variable for PostgreSQL Pods. Read more about defining environment variables in [Kubernetes documentation](https://kubernetes.io/docs/tasks/inject-data-application/define-environment-variable-container/) .

| Value type | Example  |
| ---------- | -------- |
| string     | `MY_ENV` |

### `instances.env.value`

The value for an environment variable.

| Value type | Example |
| ---------- | ------- |
| string     | `1000`  |

### `instances.envFrom.secretRefName`

Name of a Secret or a ConfigMap, key/values of which are used as environment variables for PostgreSQL Pods.

| Value type | Example               |
| ---------- | --------------------- |
| string     | `instance-env-secret` |

### `instances.initContainer.image`

Defines an image for an init container to run before the main container in the Pod. The init container is typically used for setup tasks such as initializing filesystems, setting permissions, or preparing configuration.

| Value type | Example                                        |
| ---------- | ---------------------------------------------- |
| string     | `perconalab/percona-postgresql-operator:3.1.0` |

### `instances.initContainer.resources.limits.cpu`

[Kubernetes CPU limits](https://kubernetes.io/docs/concepts/configuration/manage-compute-resources-container/#resource-requests-and-limits-of-pod-and-container) for an init container.

| Value type | Example |
| ---------- | ------- |
| string     | `2.0`   |

### `instances.initContainer.resources.limits.memory`

The [Kubernetes memory limits](https://kubernetes.io/docs/concepts/configuration/manage-compute-resources-container/#resource-requests-and-limits-of-pod-and-container) for an init container.

| Value type | Example |
| ---------- | ------- |
| string     | `4Gi`   |

### `instances.initContainer.securityContext`

Security settings for the init container. These settings control privileges, user/group IDs, and other security-related options. For more details, see the [Kubernetes documentation on SecurityContext](https://kubernetes.io/docs/tasks/configure-pod-container/security-context/)

| Value type | Example                                                                                                                               |
| ---------- | ------------------------------------------------------------------------------------------------------------------------------------- |
| subdoc     | `runAsUser: 1001 runAsGroup: 1001 runAsNonRoot: true  privileged: false allowPrivilegeEscalation: false readOnlyRootFilesystem: true` |

### `instances.resources.requests.cpu`

[Kubernetes CPU requests](https://kubernetes.io/docs/concepts/configuration/manage-compute-resources-container/#resource-requests-and-limits-of-pod-and-container) for a PostgreSQL instance. It must not exceed the limit.

If you specify a limit and don’t specify a request, Kubernetes uses the specified limit as the requested value for a resource.

| Value type | Example |
| ---------- | ------- |
| string     | `1.0`   |

### `instances.resources.requests.memory`

[Kubernetes memory requests](https://kubernetes.io/docs/concepts/configuration/manage-compute-resources-container/#resource-requests-and-limits-of-pod-and-container) for a PostgreSQL instance. It must not exceed the limit.

If you specify a limit and don’t specify a request, Kubernetes uses the specified limit as the requested value for a resource.

| Value type | Example |
| ---------- | ------- |
| string     | `3Gi`   |

### `instances.resources.limits.cpu`

[Kubernetes CPU limits](https://kubernetes.io/docs/concepts/configuration/manage-compute-resources-container/#resource-requests-and-limits-of-pod-and-container) for a PostgreSQL instance.

| Value type | Example |
| ---------- | ------- |
| string     | `2.0`   |

### `instances.resources.limits.memory`

The [Kubernetes memory limits](https://kubernetes.io/docs/concepts/configuration/manage-compute-resources-container/#resource-requests-and-limits-of-pod-and-container) for a PostgreSQL instance.

| Value type | Example |
| ---------- | ------- |
| string     | `4Gi`   |

### `instances.containers.replicaCertCopy.resources.requests.cpu`

[Kubernetes CPU requests](https://kubernetes.io/docs/concepts/configuration/manage-compute-resources-container/#resource-requests-and-limits-of-pod-and-container) for a `replica-cert-copy` sidecar container. It must not exceed the limit.

If you specify a limit and don’t specify a request, Kubernetes uses the specified limit as the requested value for a resource.

| Value type | Example |
| ---------- | ------- |
| string     | `100m`  |

### `instances.containers.replicaCertCopy.resources.requests.memory`

[Kubernetes memory requests](https://kubernetes.io/docs/concepts/configuration/manage-compute-resources-container/#resource-requests-and-limits-of-pod-and-container) for a `replica-cert-copy` sidecar container. It must not exceed the limit.

If you specify a limit and don’t specify a request, Kubernetes uses the specified limit as the requested value for a resource.

| Value type | Example |
| ---------- | ------- |
| string     | `120Mi` |

### `instances.containers.replicaCertCopy.resources.limits.cpu`

[Kubernetes CPU limits](https://kubernetes.io/docs/concepts/configuration/manage-compute-resources-container/#resource-requests-and-limits-of-pod-and-container) for `replica-cert-copy` sidecar container.

| Value type | Example |
| ---------- | ------- |
| string     | `200m`  |

### `instances.containers.replicaCertCopy.resources.limits.memory`

The [Kubernetes memory limits](https://kubernetes.io/docs/concepts/configuration/manage-compute-resources-container/#resource-requests-and-limits-of-pod-and-container) for `replica-cert-copy` sidecar container.

| Value type | Example |
| ---------- | ------- |
| string     | `128Mi` |

### `instances.topologySpreadConstraints.maxSkew`

The degree to which Pods may be unevenly distributed under the [Kubernetes Pod Topology Spread Constraints](https://kubernetes.io/docs/concepts/scheduling-eviction/topology-spread-constraints/) .

| Value type | Example |
| ---------- | ------- |
| int        | `1`     |

### `instances.topologySpreadConstraints.topologyKey`

The key of node labels for the [Kubernetes Pod Topology Spread Constraints](https://kubernetes.io/docs/concepts/scheduling-eviction/topology-spread-constraints/) .

| Value type | Example         |
| ---------- | --------------- |
| string     | `my-node-label` |

### `instances.topologySpreadConstraints.whenUnsatisfiable`

What to do with a Pod if it doesn’t satisfy the [Kubernetes Pod Topology Spread Constraints](https://kubernetes.io/docs/concepts/scheduling-eviction/topology-spread-constraints/) .

| Value type | Example         |
| ---------- | --------------- |
| string     | `DoNotSchedule` |

### `instances.topologySpreadConstraints.labelSelector.matchLabels`

The Label selector for the [Kubernetes Pod Topology Spread Constraints](https://kubernetes.io/docs/concepts/scheduling-eviction/topology-spread-constraints/) .

| Value type | Example                                                     |
| ---------- | ----------------------------------------------------------- |
| label      | `postgres-operator.crunchydata.com/instance-set: instance1` |

### `instances.tolerations.effect`

The [Kubernetes Pod tolerations](https://kubernetes.io/docs/concepts/configuration/taint-and-toleration/#concepts) effect for the PostgreSQL instance.

| Value type | Example      |
| ---------- | ------------ |
| string     | `NoSchedule` |

### `instances.tolerations.key`

The [Kubernetes Pod tolerations](https://kubernetes.io/docs/concepts/configuration/taint-and-toleration/#concepts) key for the PostgreSQL instance.

| Value type | Example |
| ---------- | ------- |
| string     | `role`  |

### `instances.tolerations.operator`

The [Kubernetes Pod tolerations](https://kubernetes.io/docs/concepts/configuration/taint-and-toleration/#concepts) operator for the PostgreSQL instance.

| Value type | Example |
| ---------- | ------- |
| string     | `Equal` |

### `instances.tolerations.value`

The [Kubernetes Pod tolerations](https://kubernetes.io/docs/concepts/configuration/taint-and-toleration/#concepts) value for the PostgreSQL instance.

| Value type | Example              |
| ---------- | -------------------- |
| string     | `connection-poolers` |

### `instances.priorityClassName`

The [Kubernetes Pod priority class](https://kubernetes.io/docs/concepts/configuration/pod-priority-preemption/#priorityclass) for PostgreSQL instance Pods.

| Value type | Example         |
| ---------- | --------------- |
| string     | `high-priority` |

### `instances.securityContext`

A custom [Kubernetes Security Context for a Pod](https://kubernetes.io/docs/tasks/configure-pod-container/security-context/) to be used instead of the default one.

| Value type | Example                                                                                                                                                                                                                                                                                                                                                                              |
| ---------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| subdoc     | `fsGroup: 1001 runAsUser: 1001 runAsNonRoot: true fsGroupChangePolicy: “OnRootMismatch” runAsGroup: 1001 seLinuxOptions:   type: spc_t   level: s0:c123,c456 seccompProfile:   type: Localhost   localhostProfile: localhost/profile.json supplementalGroups: - 1001 sysctls: - name: net.ipv4.tcp_keepalive_time   value: “600” - name: net.ipv4.tcp_keepalive_intvl   value: “60”` |

### `instances.walVolumeClaimSpec.accessModes`

The [Kubernetes PersistentVolumeClaim](https://kubernetes.io/docs/concepts/storage/persistent-volumes/#persistentvolumeclaims) access modes for the PostgreSQL Write-ahead Log storage.

| Value type | Example         |
| ---------- | --------------- |
| string     | `ReadWriteOnce` |

### `instances.walVolumeClaimSpec.storageClassName`

Set the [Kubernetes storage class](https://kubernetes.io/docs/concepts/storage/storage-classes/) to use with the PostgreSQL Write-ahead Log storage [PersistentVolumeClaim](https://kubernetes.io/docs/concepts/storage/persistent-volumes/#persistentvolumeclaims) .

| Value type | Example    |
| ---------- | ---------- |
| string     | `standard` |

### `instances.walVolumeClaimSpec.resources.requests.storage`

The [Kubernetes storage requests](https://kubernetes.io/docs/concepts/configuration/manage-compute-resources-container/#resource-requests-and-limits-of-pod-and-container) for the storage the PostgreSQL instance will use.

| Value type | Example |
| ---------- | ------- |
| string     | `1Gi`   |

### `instances.dataVolumeClaimSpec.accessModes`

The [Kubernetes PersistentVolumeClaim](https://kubernetes.io/docs/concepts/storage/persistent-volumes/#persistentvolumeclaims) access modes for the PostgreSQL storage.

| Value type | Example         |
| ---------- | --------------- |
| string     | `ReadWriteOnce` |

### `instances.dataVolumeClaimSpec.storageClassName`

Set the [Kubernetes storage class](https://kubernetes.io/docs/concepts/storage/storage-classes/) to use with PostgreSQL Cluster [PersistentVolumeClaim](https://kubernetes.io/docs/concepts/storage/persistent-volumes/#persistentvolumeclaims) for the PostgreSQL storage.

| Value type | Example    |
| ---------- | ---------- |
| string     | `standard` |

### `instances.dataVolumeClaimSpec.resources.requests.storage`

The [Kubernetes storage requests](https://kubernetes.io/docs/concepts/configuration/manage-compute-resources-container/#resource-requests-and-limits-of-pod-and-container) for the storage the PostgreSQL instance will use.

| Value type | Example |
| ---------- | ------- |
| string     | `1Gi`   |

### `instances.dataVolumeClaimSpec.resources.limits.storage`

The [Kubernetes storage limits](https://kubernetes.io/docs/concepts/configuration/manage-compute-resources-container/#resource-requests-and-limits-of-pod-and-container) for the storage the PostgreSQL instance will use. When the [`AutoGrowVolumes`](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/env-var-operator.html#pgo_feature_gates) feature gate is enabled, this value sets the maximum size the Operator may scale the data volume up to. See [Automated scaling with auto-growable disks](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/scaling-vertical.html#automated-scaling-with-auto-growable-disks) for details.

| Value type | Example |
| ---------- | ------- |
| string     | `5Gi`   |

### `instances.tablespaceVolumes.name`

Name for the custom [tablespace volume](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/tablespaces.html).

| Value type | Example |
| ---------- | ------- |
| string     | `user`  |

### `instances.tablespaceVolumes.dataVolumeClaimSpec.accessModes`

The [Kubernetes PersistentVolumeClaim](https://kubernetes.io/docs/concepts/storage/persistent-volumes/#persistentvolumeclaims) access modes for the tablespace volume.

| Value type | Example         |
| ---------- | --------------- |
| string     | `ReadWriteOnce` |

### `instances.tablespaceVolumes.dataVolumeClaimSpec.resources.requests.storage`

The [Kubernetes storage requests](https://kubernetes.io/docs/concepts/configuration/manage-compute-resources-container/#resource-requests-and-limits-of-pod-and-container) for the tablespace volume.

| Value type | Example |
| ---------- | ------- |
| string     | `1Gi`   |

## `instances.extraVolumes` subsection

The `instances.extraVolumes` subsection defines additional volumes that the Operator mounts into the PostgreSQL database container. Use this to supply files that PostgreSQL reads from disk, such as full-text search dictionaries. Changing this option causes PostgreSQL to restart.

### `instances.extraVolumes.name`

The name of the extra volume. Must be unique within the instance Pod.

| Value type | Example     |
| ---------- | ----------- |
| string     | `fts-dicts` |

### `instances.extraVolumes.volumeSource`

The [Kubernetes volume source](https://kubernetes.io/docs/concepts/storage/volumes/) for the extra volume. Supports ConfigMap, Secret, PersistentVolumeClaim, emptyDir, and other volume types.

| Value type | Example                           |
| ---------- | --------------------------------- |
| subdoc     | `configMap:   name: my-fts-dicts` |

### `instances.extraVolumes.mounts.mountPath`

The path within the PostgreSQL container at which the volume is mounted.

| Value type | Example                                        |
| ---------- | ---------------------------------------------- |
| string     | `/usr/pgsql-17/share/tsearch_data/mydict.dict` |

### `instances.extraVolumes.mounts.subPath`

The path within the volume to mount. Defaults to the volume root. Use `subPath` to mount a single file from the volume without replacing the contents of the target directory.

| Value type | Example       |
| ---------- | ------------- |
| string     | `mydict.dict` |

### `instances.extraVolumes.mounts.readOnly`

Mounts the volume as read-only when set to `true`. Defaults to read-write when omitted.

| Value type | Example |
| ---------- | ------- |
| boolean    | `true`  |

## `instances.sidecars` subsection

The `instances.sidecars` subsection in the [deploy/cr.yaml](https://github.com/percona/percona-postgresql-operator/blob/main/deploy/cr.yaml) file contains configuration options for [custom sidecar containers](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/sidecar.html) which can be added to PostgreSQL Pods.

### `instances.sidecars.image`

Image for the [custom sidecar container](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/sidecar.html) for PostgreSQL Pods.

| Value type | Example          |
| ---------- | ---------------- |
| string     | `busybox:latest` |

### `instances.sidecars.name`

Name of the [custom sidecar container](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/sidecar.html) for PostgreSQL Pods.

| Value type | Example         |
| ---------- | --------------- |
| string     | `testcontainer` |

### `instances.sidecars.imagePullPolicy`

This option is used to set the [policy](https://kubernetes.io/docs/concepts/containers/images/#updating-images) for the PostgreSQL Pod sidecar container.

| Value type | Example  |
| ---------- | -------- |
| string     | `Always` |

### `instances.sidecars.env`

The [environment variables set as key-value pairs](https://kubernetes.io/docs/tasks/inject-data-application/define-environment-variable-container/) for the [custom sidecar container](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/sidecar.html) for PostgreSQL Pods.

| Value type | Example |
| ---------- | ------- |
| subdoc     |         |

### `instances.sidecars.envFrom`

The [environment variables set as key-value pairs in ConfigMaps](https://kubernetes.io/docs/tasks/inject-data-application/define-environment-variable-container/) for the [custom sidecar container](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/sidecar.html) for PostgreSQL Pods.

| Value type | Example |
| ---------- | ------- |
| subdoc     |         |

### `instances.sidecars.command`

Command for the [custom sidecar container](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/sidecar.html) for PostgreSQL Pods.

| Value type | Example       |
| ---------- | ------------- |
| array      | `["/bin/sh"]` |

### `instances.sidecars.args`

Command arguments for the [custom sidecar container](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/sidecar.html) for PostgreSQL Pods.

| Value type | Example                                                                        |
| ---------- | ------------------------------------------------------------------------------ |
| array      | `["-c", "while true; do trap 'exit 0' SIGINT SIGTERM SIGQUIT SIGKILL; done;"]` |

### `instances.sidecarVolumes.name`

The name of the [volume](https://kubernetes.io/docs/concepts/storage/volumes/) to attach to PostgreSQL instance Pods for use by [custom sidecar containers](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/sidecar.html). Supports secret, configMap, NFS and other volume types.

| Value type | Example        |
| ---------- | -------------- |
| subdoc     | sidecar-secret |

### `instances.sidecarVolumes.secret.secretName`

The name of the [volume Secret](https://kubernetes.io/docs/concepts/storage/volumes/) to attach to PostgreSQL instance Pods for use by [custom sidecar containers](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/sidecar.html).

| Value type                    | Example  |
| ----------------------------- | -------- |
| :material-text-string: string | mysecret |

### `instances.sidecarVolumes.configMap.name`

The name of the configMap object to attach to PostgreSQL instance Pods for use by [custom sidecar containers](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/sidecar.html).

| Value type                    | Example        |
| ----------------------------- | -------------- |
| :material-text-string: string | sidecar-config |

### `instances.sidecarVolumes.nfs.server`

The hostname of the NFS server that will provide remote filesystem to the [custom sidecar containers](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/sidecar.html) in PostgreSQL instance Pods.

| Value type                    | Example                                 |
| ----------------------------- | --------------------------------------- |
| :material-text-string: string | “nfs-service.storage.svc.cluster.local” |

### `instances.sidecarVolumes.nfs.path`

The path on the NFS server that will be provided as a remote filesystem to the [custom sidecar containers](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/sidecar.html) in PostgreSQL instance Pods.

| Value type                    | Example                                 |
| ----------------------------- | --------------------------------------- |
| :material-text-string: string | “nfs-service.storage.svc.cluster.local” |

### `instances.sidecarPVCs`

[PersistentVolumeClaims](https://kubernetes.io/docs/concepts/storage/persistent-volumes/) that the operator creates and mounts for [custom sidecar containers](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/sidecar.html) in PostgreSQL instance Pods.

You can use PVCs with sidecar containers only when you deploy a new cluster. Updates to running cluster are not supported.

| Value type | Example                                                                                                                                                      |
| ---------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| subdoc     | `- name: sidecar-volume-claim   spec:     resources:       requests:         storage: 1Gi     volumeMode: Filesystem     accessModes:       - ReadWriteOnce` |

## Backup section

The `backup` section in the [deploy/cr.yaml](https://github.com/percona/percona-postgresql-operator/blob/main/deploy/cr.yaml) file contains the following configuration options for the regular Percona Distribution for PostgreSQL backups.

### `backups.enabled`

Enables to turn on/off backups for the cluster. Use this option with caution. Read more in [Disable backups](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/backups-disable.html).

| Value type | Example |
| ---------- | ------- |
| string     | `true`  |

### `backups.trackLatestRestorableTime`

Controls [tracking of the latest restorable time](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/backups-pitr.html#latest-restorable-time) for point-in-time recovery. The default is `true`.

When enabled, the Operator maintains `status.latestRestorableTime` on the latest successful backup. That value is the timestamp of the latest committed transaction archived to the backup repository. Use it when you choose a point-in-time restore target.

When disabled, the Operator stops updating that helper field. Starting with Operator 2.8.0, it also does not inject the tracking logic into `archive_command`. Backups and restores continue to work without the helper. See [Point-in-time recovery](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/backups-pitr.html) for details.

| Value type | Example |
| ---------- | ------- |
| boolean    | `true`  |

### `backups.volumeSnapshots.className`

Name of the [VolumeSnapshotClass](https://kubernetes.io/docs/concepts/storage/volume-snapshots/) to use when creating [PVC snapshots](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/backups-pvc-snapshots.html). When set, the Operator creates a volume snapshot in coordination with each backup. Snapshots enable much faster restores when provisioning new clusters. Requires the `BackupSnapshots=true` feature gate.

| Value type | Example                     |
| ---------- | --------------------------- |
| string     | `csi-gce-pd-snapshot-class` |

### `backups.volumeSnapshots.mode`

Specifies the type of PVC snapshot-based backups.

| Value type | Example   |
| ---------- | --------- |
| string     | `offline` |

### `backups.volumeSnapshots.schedule`

Specifies the schedule in Cron format to run PVC snapshot-based backups automatically.

| Value type | Example       |
| ---------- | ------------- |
| string     | `"0 3 * * *"` |

### `backups.volumeSnapshots.jobs.tolerations.effect`

The [Kubernetes Pod tolerations](https://kubernetes.io/docs/concepts/configuration/taint-and-toleration/#concepts) effect for the Job that prepares volumes before restoring from a [PVC snapshot](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/backups-pvc-snapshots.html). See [Tolerations](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/constraints.html#tolerations).

| Value type | Example      |
| ---------- | ------------ |
| string     | `NoSchedule` |

### `backups.volumeSnapshots.jobs.tolerations.key`

The [Kubernetes Pod tolerations](https://kubernetes.io/docs/concepts/configuration/taint-and-toleration/#concepts) key for the PVC snapshot restore preparation job.

| Value type | Example |
| ---------- | ------- |
| string     | `role`  |

### `backups.volumeSnapshots.jobs.tolerations.operator`

The [Kubernetes Pod tolerations](https://kubernetes.io/docs/concepts/configuration/taint-and-toleration/#concepts) operator for the snapshot restore prepare Job.

| Value type | Example |
| ---------- | ------- |
| string     | `Equal` |

### `backups.volumeSnapshots.jobs.tolerations.value`

The [Kubernetes Pod tolerations](https://kubernetes.io/docs/concepts/configuration/taint-and-toleration/#concepts) value for the snapshot restore prepare Job.

| Value type | Example              |
| ---------- | -------------------- |
| string     | `connection-poolers` |

### `backups.pgbackrest.metadata.labels`

Set [labels](https://kubernetes.io/docs/concepts/overview/working-with-objects/labels/) for pgBackRest Pods.

| Value type | Example                      |
| ---------- | ---------------------------- |
| label      | `pg-cluster-label: cluster1` |

### `backups.pgbackrest.image`

The Docker image for [pgBackRest](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/backups.html#backup-repositories).

| Value type | Example                                         |
| ---------- | ----------------------------------------------- |
| string     | `docker.io/percona/percona-pgbackrest:2.59.1-2` |

### `backups.pgbackrest.env.name`

Name of an environment variable for pgBackRest Pods. Read more about defining environment variables in [Kubernetes documentation](https://kubernetes.io/docs/tasks/inject-data-application/define-environment-variable-container/) .

| Value type | Example  |
| ---------- | -------- |
| string     | `MY_ENV` |

### `backups.pgbackrest.env.value`

The value for an environment variable.

| Value type | Example |
| ---------- | ------- |
| string     | `1000`  |

### `backups.pgbackrest.envFrom.secretRefName`

Name of a Secret or a ConfigMap, key/values of which are used as environment variables for pgBouncer Pods.

| Value type | Example                |
| ---------- | ---------------------- |
| string     | `repo-host-env-secret` |

### `backups.pgbackrest.containers.pgbackrest.resources.requests.cpu`

[Kubernetes CPU requests](https://kubernetes.io/docs/concepts/configuration/manage-compute-resources-container/#resource-requests-and-limits-of-pod-and-container) for a `pgBackRest` container. It must not exceed the limit.

If you specify a limit and don’t specify a request, Kubernetes uses the specified limit as the requested value for a resource.

| Value type | Example |
| ---------- | ------- |
| string     | `150m`  |

### `backups.pgbackrest.containers.pgbackrest.resources.requests.memory`

[Kubernetes memory requests](https://kubernetes.io/docs/concepts/configuration/manage-compute-resources-container/#resource-requests-and-limits-of-pod-and-container) for a `pgBackRest` container. It must not exceed the limit.

If you specify a limit and don’t specify a request, Kubernetes uses the specified limit as the requested value for a resource.

| Value type | Example |
| ---------- | ------- |
| string     | `120Mi` |

### `backups.pgbackrest.containers.pgbackrest.resources.limits.cpu`

[Kubernetes CPU limits](https://kubernetes.io/docs/concepts/configuration/manage-compute-resources-container/#resource-requests-and-limits-of-pod-and-container) for a pgBackRest container.

| Value type | Example |
| ---------- | ------- |
| string     | `1.0`   |

### `backups.pgbackrest.containers.pgbackrest.resources.limits.memory`

The [Kubernetes memory limits](https://kubernetes.io/docs/concepts/configuration/manage-compute-resources-container/#resource-requests-and-limits-of-pod-and-container) for a pgBackRest container.

| Value type | Example |
| ---------- | ------- |
| string     | `1Gi`   |

### `backups.pgbackrest.containers.pgbackrestConfig.resources.limits.cpu`

[Kubernetes CPU limits](https://kubernetes.io/docs/concepts/configuration/manage-compute-resources-container/#resource-requests-and-limits-of-pod-and-container) for `pgbackrest-config` sidecar container.

| Value type | Example |
| ---------- | ------- |
| string     | `1.0`   |

### `backups.pgbackrest.containers.pgbackrestConfig.resources.limits.memory`

The [Kubernetes memory limits](https://kubernetes.io/docs/concepts/configuration/manage-compute-resources-container/#resource-requests-and-limits-of-pod-and-container) for `pgbackrest-config` sidecar container.

| Value type | Example |
| ---------- | ------- |
| string     | `1Gi`   |

### `backups.pgbackrest.containers.pgbackrestConfig.resources.requests.cpu`

[Kubernetes CPU requests](https://kubernetes.io/docs/concepts/configuration/manage-compute-resources-container/#resource-requests-and-limits-of-pod-and-container) for a `pgbackrest-config` sidecar container. It must not exceed the limit.

If you specify a limit and don’t specify a request, Kubernetes uses the specified limit as the requested value for a resource.

| Value type | Example |
| ---------- | ------- |
| string     | `150m`  |

### `backups.pgbackrest.containers.pgbackrestConfig.resources.requests.memory`

[Kubernetes memory requests](https://kubernetes.io/docs/concepts/configuration/manage-compute-resources-container/#resource-requests-and-limits-of-pod-and-container) for a `pgbackrest-config` sidecar container. It must not exceed the limit.

If you specify a limit and don’t specify a request, Kubernetes uses the specified limit as the requested value for a resource.

| Value type | Example |
| ---------- | ------- |
| string     | `120Mi` |

### `backups.pgbackrest.configuration.secret.name`

Name of the [Kubernetes Secret object](https://kubernetes.io/docs/concepts/configuration/secret/#using-imagepullsecrets) with custom pgBackRest configuration, which will be added to the pgBackRest configuration generated by the Operator.

| Value type | Example                       |
| ---------- | ----------------------------- |
| string     | `cluster1-pgbackrest-secrets` |

### `backups.pgbackrest.jobs.backoffLimit`

The number of retries to make a backup with incremental pauses of 10 seconds, 20 seconds, etc. between retries. By default it’s `0`, which means that pgBackRest job Pod fails after first unsuccessful attempt (causing creation of a new Pod on failure).

| Value type | Example |
| ---------- | ------- |
| int        | `2`     |

### `backups.pgbackrest.jobs.restartPolicy`

The [Kubernetes Pod restart policy](https://kubernetes.io/docs/concepts/workloads/pods/pod-lifecycle/#restart-policy) for pgBackRest jobs.

| Value type | Example     |
| ---------- | ----------- |
| string     | `OnFailure` |

### `backups.pgbackrest.jobs.priorityClassName`

The [Kubernetes Pod priority class](https://kubernetes.io/docs/concepts/configuration/pod-priority-preemption/#priorityclass) for pgBackRest jobs.

| Value type | Example         |
| ---------- | --------------- |
| string     | `high-priority` |

### `backups.pgbackrest.jobs.resources.limits.cpu`

[Kubernetes CPU limits](https://kubernetes.io/docs/concepts/configuration/manage-compute-resources-container/#resource-requests-and-limits-of-pod-and-container) for a pgBackRest job.

| Value type | Example |
| ---------- | ------- |
| int        | `200`   |

### `backups.pgbackrest.jobs.resources.limits.memory`

The [Kubernetes memory limits](https://kubernetes.io/docs/concepts/configuration/manage-compute-resources-container/#resource-requests-and-limits-of-pod-and-container) for a pgBackRest job.

| Value type | Example |
| ---------- | ------- |
| string     | `128Mi` |

### `backups.pgbackrest.jobs.resources.requests.cpu`

[Kubernetes CPU requests](https://kubernetes.io/docs/concepts/configuration/manage-compute-resources-container/#resource-requests-and-limits-of-pod-and-container) for a pgBackRest job. It must not exceed the limit.

If you specify a limit and don’t specify a request, Kubernetes uses the specified limit as the requested value for a resource.

| Value type | Example |
| ---------- | ------- |
| string     | `150m`  |

### `backups.pgbackrest.jobs.resources.requests.memory`

[Kubernetes memory requests](https://kubernetes.io/docs/concepts/configuration/manage-compute-resources-container/#resource-requests-and-limits-of-pod-and-container) for pgBackRest job. It must not exceed the limit.

If you specify a limit and don’t specify a request, Kubernetes uses the specified limit as the requested value for a resource.

| Value type | Example |
| ---------- | ------- |
| string     | `120Mi` |

### `backups.pgbackrest.jobs.tolerations.effect`

The [Kubernetes Pod tolerations](https://kubernetes.io/docs/concepts/configuration/taint-and-toleration/#concepts) effect for a backup job.

| Value type | Example      |
| ---------- | ------------ |
| string     | `NoSchedule` |

### `backups.pgbackrest.jobs.tolerations.key`

The [Kubernetes Pod tolerations](https://kubernetes.io/docs/concepts/configuration/taint-and-toleration/#concepts) key for a backup job.

| Value type | Example |
| ---------- | ------- |
| string     | `role`  |

### `backups.pgbackrest.jobs.tolerations.operator`

The [Kubernetes Pod tolerations](https://kubernetes.io/docs/concepts/configuration/taint-and-toleration/#concepts) operator for a backup job.

| Value type | Example |
| ---------- | ------- |
| string     | `Equal` |

### `backups.pgbackrest.jobs.tolerations.value`

The [Kubernetes Pod tolerations](https://kubernetes.io/docs/concepts/configuration/taint-and-toleration/#concepts) value for a backup job.

| Value type | Example              |
| ---------- | -------------------- |
| string     | `connection-poolers` |

### `backups.pgbackrest.jobs.securityContext`

A custom [Kubernetes Security Context for a Pod](https://kubernetes.io/docs/tasks/configure-pod-container/security-context/) to be used instead of the default one.

| Value type | Example                                                                                                                                                                                                                                                                                                                                                                              |
| ---------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| subdoc     | `fsGroup: 1001 runAsUser: 1001 runAsNonRoot: true fsGroupChangePolicy: “OnRootMismatch” runAsGroup: 1001 seLinuxOptions:   type: spc_t   level: s0:c123,c456 seccompProfile:   type: Localhost   localhostProfile: localhost/profile.json supplementalGroups: - 1001 sysctls: - name: net.ipv4.tcp_keepalive_time   value: “600” - name: net.ipv4.tcp_keepalive_intvl   value: “60”` |

### `backups.pgbackrest.global`

Settings, which are to be included in the `global` section of the pgBackRest configuration generated by the Operator.

| Value type | Example                                                                                                                                                                                                                                                                                                                                                                                   |
| ---------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| subdoc     | `repo1-retention-full: “14” repo1-retention-full-type: time repo1-path: /pgbackrest/postgres-operator/cluster1/repo1 repo1-cipher-type: aes-256-cbc repo1-s3-uri-style: path repo2-path: /pgbackrest/postgres-operator/cluster1-multi-repo/repo2 repo3-path: /pgbackrest/postgres-operator/cluster1-multi-repo/repo3 repo4-path: /pgbackrest/postgres-operator/cluster1-multi-repo/repo4` |

### `backups.pgbackrest.repoHost.sidecars.name`

The name of a [custom sidecar container](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/sidecar.html) for pgBackRest Pods.

| Value type | Example         |
| ---------- | --------------- |
| string     | `testcontainer` |

### `backups.pgbackrest.repoHost.sidecars.image`

The image used to deploy a [custom sidecar container](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/sidecar.html) for pgBackRest Pods.

| Value type | Example          |
| ---------- | ---------------- |
| string     | `busybox:latest` |

### `backups.pgbackrest.repoHost.sidecars.command`

The command to use inside a custom sidecar container for pgBackRest Pods

| Value type | Example            |
| ---------- | ------------------ |
| string     | `["sleep", "30d"]` |

### `backups.pgbackrest.repoHost.sidecars.securityContext`

Security settings for the sidecar container. These settings control privileges, user/group IDs, and other security-related options. For more details, see the [Kubernetes documentation on SecurityContext](https://kubernetes.io/docs/tasks/configure-pod-container/security-context/)

| Value type | Example |
| ---------- | ------- |
| string     | `{}`    |

### `backups.pgbackrest.repoHost.sidecarVolumes.name`

The name of the [volume](https://kubernetes.io/docs/concepts/storage/volumes/) to attach to pgBackRest repo host Pods for use by [custom sidecar containers](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/sidecar.html). Supports secret, configMap, NFS and other volume types.

| Value type | Example        |
| ---------- | -------------- |
| subdoc     | sidecar-secret |

### `backups.pgbackrest.repoHost.sidecarVolumes.secret.secretName`

The name of the [volume Secret](https://kubernetes.io/docs/concepts/storage/volumes/) to attach to pgBackRest repo host Pods for use by [custom sidecar containers](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/sidecar.html).

| Value type                    | Example  |
| ----------------------------- | -------- |
| :material-text-string: string | mysecret |

### `backups.pgbackrest.repoHost.sidecarVolumes.configMap.name`

The name of the configMap object to attach to pgBackRest repo host Pods for use by [custom sidecar containers](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/sidecar.html).

| Value type                    | Example        |
| ----------------------------- | -------------- |
| :material-text-string: string | sidecar-config |

### `backups.pgbackrest.repoHost.sidecarVolumes.nfs.server`

The hostname of the NFS server that will provide remote filesystem to the [custom sidecar containers](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/sidecar.html) in pgBackRest repo host Pods Pods.

| Value type                    | Example                                 |
| ----------------------------- | --------------------------------------- |
| :material-text-string: string | “nfs-service.storage.svc.cluster.local” |

### `backups.pgbackrest.repoHost.sidecarVolumes.nfs.path`

The path on the NFS server that will be provided as a remote filesystem to the [custom sidecar containers](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/sidecar.html) in pgBackRest repo host Pods\` Pods.

| Value type                    | Example                                 |
| ----------------------------- | --------------------------------------- |
| :material-text-string: string | “nfs-service.storage.svc.cluster.local” |

### `backups.pgbackrest.repoHost.sidecarPVCs`

[PersistentVolumeClaims](https://kubernetes.io/docs/concepts/storage/persistent-volumes/) that the Operator creates and mounts for [custom sidecar containers](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/sidecar.html) in pgBackRest repo host Pods.

You can use PVCs with sidecar containers only when you deploy a new cluster. Updates to running cluster are not supported.

| Value type | Example                                                                                                                                                      |
| ---------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| subdoc     | `- name: sidecar-volume-claim   spec:     resources:       requests:         storage: 1Gi     volumeMode: Filesystem     accessModes:       - ReadWriteOnce` |

### `backups.pgbackrest.repoHost.resources.requests.cpu`

[Kubernetes CPU requests](https://kubernetes.io/docs/concepts/configuration/manage-compute-resources-container/#resource-requests-and-limits-of-pod-and-container) for a pgBackRest repo. It must not exceed the limit.

If you specify a limit and don’t specify a request, Kubernetes uses the specified limit as the requested value for a resource.

| Value type | Example |
| ---------- | ------- |
| string     | `150m`  |

### `backups.pgbackrest.repoHost.resources.requests.memory`

[Kubernetes memory requests](https://kubernetes.io/docs/concepts/configuration/manage-compute-resources-container/#resource-requests-and-limits-of-pod-and-container) for pgBackRest repo. It must not exceed the limit.

If you specify a limit and don’t specify a request, Kubernetes uses the specified limit as the requested value for a resource.

| Value type | Example |
| ---------- | ------- |
| string     | `120Mi` |

### `backups.pgbackrest.repoHost.resources.limits.cpu`

[Kubernetes CPU limits](https://kubernetes.io/docs/concepts/configuration/manage-compute-resources-container/#resource-requests-and-limits-of-pod-and-container) for a pgBackRest repo.

| Value type | Example |
| ---------- | ------- |
| int        | `200`   |

### `backups.pgbackrest.repoHost.resources.limits.memory`

The [Kubernetes memory limits](https://kubernetes.io/docs/concepts/configuration/manage-compute-resources-container/#resource-requests-and-limits-of-pod-and-container) for a pgBackRest repo.

| Value type | Example |
| ---------- | ------- |
| string     | `128Mi` |

### `backups.pgbackrest.repoHost.priorityClassName`

The [Kubernetes Pod priority class](https://kubernetes.io/docs/concepts/configuration/pod-priority-preemption/#priorityclass) for pgBackRest repo.

| Value type | Example         |
| ---------- | --------------- |
| string     | `high-priority` |

### `backups.pgbackrest.repoHost.topologySpreadConstraints.maxSkew`

The degree to which Pods may be unevenly distributed under the [Kubernetes Pod Topology Spread Constraints](https://kubernetes.io/docs/concepts/scheduling-eviction/topology-spread-constraints/) .

| Value type | Example |
| ---------- | ------- |
| int        | `1`     |

### `backups.pgbackrest.repoHost.topologySpreadConstraints.topologyKey`

The key of node labels for the [Kubernetes Pod Topology Spread Constraints](https://kubernetes.io/docs/concepts/scheduling-eviction/topology-spread-constraints/) .

| Value type | Example         |
| ---------- | --------------- |
| string     | `my-node-label` |

### `backups.pgbackrest.repoHost.topologySpreadConstraints.whenUnsatisfiable`

What to do with a Pod if it doesn’t satisfy the [Kubernetes Pod Topology Spread Constraints](https://kubernetes.io/docs/concepts/scheduling-eviction/topology-spread-constraints/) .

| Value type | Example          |
| ---------- | ---------------- |
| string     | `ScheduleAnyway` |

### `backups.pgbackrest.repoHost.topologySpreadConstraints.labelSelector.matchLabels`

The Label selector for the [Kubernetes Pod Topology Spread Constraints](https://kubernetes.io/docs/concepts/scheduling-eviction/topology-spread-constraints/) .

| Value type | Example                                            |
| ---------- | -------------------------------------------------- |
| label      | `postgres-operator.crunchydata.com/pgbackrest: ""` |

### `backups.pgbackrest.repoHost.affinity.podAntiAffinity`

[Pod anti-affinity](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/constraints.html#affinity-and-anti-affinity), allows setting the standard Kubernetes affinity constraints of any complexity.

| Value type | Example |
| ---------- | ------- |
| subdoc     |         |

### `backups.pgbackrest.repoHost.tolerations.effect`

The [Kubernetes Pod tolerations](https://kubernetes.io/docs/concepts/configuration/taint-and-toleration/#concepts) effect for pgBackRest repo.

| Value type | Example      |
| ---------- | ------------ |
| string     | `NoSchedule` |

### `backups.pgbackrest.repoHost.tolerations.key`

The [Kubernetes Pod tolerations](https://kubernetes.io/docs/concepts/configuration/taint-and-toleration/#concepts) key for pgBackRest repo.

| Value type | Example |
| ---------- | ------- |
| string     | `role`  |

### `backups.pgbackrest.repoHost.tolerations.operator`

The [Kubernetes Pod tolerations](https://kubernetes.io/docs/concepts/configuration/taint-and-toleration/#concepts) operator for pgBackRest repo.

| Value type | Example |
| ---------- | ------- |
| string     | `Equal` |

### `backups.pgbackrest.repoHost.tolerations.value`

The [Kubernetes Pod tolerations](https://kubernetes.io/docs/concepts/configuration/taint-and-toleration/#concepts) value for pgBackRest repo.

| Value type | Example              |
| ---------- | -------------------- |
| string     | `connection-poolers` |

### ‘backups.pgbackrest.repoHost.securityContext’

A custom [Kubernetes Security Context for a Pod](https://kubernetes.io/docs/tasks/configure-pod-container/security-context/) to be used instead of the default one.

| Value type | Example                                                                                                                                                                                                                                                                                                                                                                              |
| ---------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| subdoc     | `fsGroup: 1001 runAsUser: 1001 runAsNonRoot: true fsGroupChangePolicy: “OnRootMismatch” runAsGroup: 1001 seLinuxOptions:   type: spc_t   level: s0:c123,c456 seccompProfile:   type: Localhost   localhostProfile: localhost/profile.json supplementalGroups: - 1001 sysctls: - name: net.ipv4.tcp_keepalive_time   value: “600” - name: net.ipv4.tcp_keepalive_intvl   value: “60”` |

### `backups.pgbackrest.manual.repoName`

Name of the pgBackRest repository for on-demand backups.

| Value type | Example |
| ---------- | ------- |
| string     | `repo1` |

### `backups.pgbackrest.manual.options`

The on-demand backup command-line options which will be passed to pgBackRest for on-demand backups.

| Value type | Example       |
| ---------- | ------------- |
| string     | `--type=full` |

### `backups.pgbackrest.manual.initialDelaySeconds`

The time to delay a backup start after the backup Pod is scheduled. The backup process wait for the defined time before it connectsto the API server to start a backup.

| Value type | Example |
| ---------- | ------- |
| int        | `120`   |

### `backups.pgbackrest.repos.name`

Name of the pgBackRest repository for backups.

| Value type | Example |
| ---------- | ------- |
| string     | `repo1` |

### `backups.pgbackrest.repos.schedules.full`

Scheduled time to make a full backup specified in the [crontab format](https://en.wikipedia.org/wiki/Cron) .

| Value type | Example       |
| ---------- | ------------- |
| string     | `0 0 \* \* 6` |

### `backups.pgbackrest.repos.schedules.differential`

Scheduled time to make a differential backup specified in the [crontab format](https://en.wikipedia.org/wiki/Cron) .

| Value type | Example       |
| ---------- | ------------- |
| string     | `0 0 \* \* 6` |

### `backups.pgbackrest.repos.volume.volumeClaimSpec.accessModes`

The [Kubernetes PersistentVolumeClaim](https://kubernetes.io/docs/concepts/storage/persistent-volumes/#persistentvolumeclaims) access modes for the pgBackRest Storage.

| Value type | Example         |
| ---------- | --------------- |
| string     | `ReadWriteOnce` |

### `backups.pgbackrest.repos.volume.volumeClaimSpec.storageClassName`

Set the [Kubernetes Storage Class](https://kubernetes.io/docs/concepts/storage/storage-classes/) to use with the Percona Operator for PostgreSQL backups stored on [Persistent Volume](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/backups-storage-pv.html).

| Value type | Example    |
| ---------- | ---------- |
| string     | `standard` |

### `backups.pgbackrest.repos.volume.volumeClaimSpec.resources.requests.storage`

The [Kubernetes storage requests](https://kubernetes.io/docs/concepts/configuration/manage-compute-resources-container/#resource-requests-and-limits-of-pod-and-container) for the pgBackRest storage.

| Value type | Example |
| ---------- | ------- |
| string     | `1Gi`   |

### `backups.pgbackrest.repos.volume.volumeClaimSpec.resources.limits.storage`

The [Kubernetes storage limits](https://kubernetes.io/docs/concepts/configuration/manage-compute-resources-container/#resource-requests-and-limits-of-pod-and-container) for the pgBackRest repository volume. Starting with Operator version 3.1.0, when the [`AutoGrowVolumes`](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/env-var-operator.html#pgo_feature_gates) feature gate is enabled, this value sets the maximum size the Operator may scale the repository volume up to. See [Automated scaling with auto-growable disks](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/scaling-vertical.html#automated-scaling-with-auto-growable-disks) for details.

| Value type | Example |
| ---------- | ------- |
| string     | `5Gi`   |

### `backups.pgbackrest.repos.s3.bucket`

The [Amazon S3 bucket](https://docs.aws.amazon.com/AmazonS3/latest/dev/UsingBucket.html) name used for backups

| Value type | Example       |
| ---------- | ------------- |
| string     | `"my-bucket"` |

### `backups.pgbackrest.repos.s3.endpoint`

The endpoint URL of the S3-compatible storage to be used for backups (not needed for the original Amazon S3 cloud).

| Value type | Example                           |
| ---------- | --------------------------------- |
| string     | `"s3.ca-central-1.amazonaws.com"` |

### `backups.pgbackrest.repos.s3.region`

The [AWS region](https://docs.aws.amazon.com/general/latest/gr/rande.html) to use for Amazon and all S3-compatible storages.

| Value type | Example          |
| ---------- | ---------------- |
| string     | `"ca-central-1"` |

### `backups.pgbackrest.repos.gcs.bucket`

The [Google Cloud Storage bucket](https://cloud.google.com/storage/docs/key-terms#buckets) name used for backups.

| Value type | Example       |
| ---------- | ------------- |
| string     | `"my-bucket"` |

### `backups.pgbackrest.repos.azure.container`

Name of the [Azure Blob Storage container](https://docs.microsoft.com/en-us/azure/storage/blobs/storage-blobs-introduction#containers) for backups.

| Value type | Example        |
| ---------- | -------------- |
| string     | `my-container` |

### `backups.pgbackrest.restore.tolerations.effect`

The [Kubernetes Pod tolerations](https://kubernetes.io/docs/concepts/configuration/taint-and-toleration/#concepts) effect for the restore job. Starting with Operator version 3.1.0, if you do not set `backups.pgbackrest.restore.tolerations`, the Operator applies [`backups.pgbackrest.jobs.tolerations`](#backupspgbackrestjobstolerationseffect). See [Tolerations](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/constraints.html#tolerations).

| Value type | Example      |
| ---------- | ------------ |
| string     | `NoSchedule` |

### `backups.pgbackrest.restore.tolerations.key`

The [Kubernetes Pod tolerations](https://kubernetes.io/docs/concepts/configuration/taint-and-toleration/#concepts) key for the restore job.

| Value type | Example |
| ---------- | ------- |
| string     | `role`  |

### `backups.pgbackrest.restore.tolerations.operator`

The [Kubernetes Pod tolerations](https://kubernetes.io/docs/concepts/configuration/taint-and-toleration/#concepts) operator for the restore job.

| Value type | Example |
| ---------- | ------- |
| string     | `Equal` |

### `backups.pgbackrest.restore.tolerations.value`

The [Kubernetes Pod tolerations](https://kubernetes.io/docs/concepts/configuration/taint-and-toleration/#concepts) value for the restore job.

| Value type | Example              |
| ---------- | -------------------- |
| string     | `connection-poolers` |

## PMM section

The `pmm` section in the [deploy/cr.yaml](https://github.com/percona/percona-postgresql-operator/blob/main/deploy/cr.yaml) file contains configuration options for Percona Monitoring and Management.

### `pmm.enabled`

Enables or disables [monitoring Percona Distribution for PostgreSQL cluster with PMM](https://docs.percona.com/percona-monitoring-and-management/3/install-pmm/install-pmm-client/connect-database/postgresql.html) .

| Value type | Example |
| ---------- | ------- |
| boolean    | `false` |

### `pmm.image`

[Percona Monitoring and Management (PMM) Client](https://docs.percona.com/percona-monitoring-and-management/3/reference/index.html#pmm-client) Docker image.

| Value type | Example                    |
| ---------- | -------------------------- |
| string     | `percona/pmm-client:3.9.1` |

### `pmm.imagePullPolicy`

This option is used to set the [policy](https://kubernetes.io/docs/concepts/containers/images/#updating-images) for updating PMM Client images.

| Value type | Example        |
| ---------- | -------------- |
| string     | `IfNotPresent` |

### `pmm.secret`

Name of the [Kubernetes Secret object](https://kubernetes.io/docs/concepts/configuration/secret/#using-imagepullsecrets) for the PMM Server password.

| Value type | Example               |
| ---------- | --------------------- |
| string     | `cluster1-pmm-secret` |

### `pmm.serverHost`

Address of the PMM Server to collect data from the cluster.

| Value type | Example              |
| ---------- | -------------------- |
| string     | `monitoring-service` |

### pmm.customClusterName

A custom name to define for a cluster. PMM Server uses this name to properly parse the metrics and display them on dashboards. Using a custom name is useful for clusters deployed in different data centers - PMM Server connects them and monitors them as one deployment. Another use case is for clusters deployed with the same name in different namespaces - PMM treats each cluster separately.

| Value type | Example              |
| ---------- | -------------------- |
| string     | `postgresql-cluster` |

### `pmm.resources.requests.cpu`

[Kubernetes CPU requests](https://kubernetes.io/docs/concepts/configuration/manage-compute-resources-container/#resource-requests-and-limits-of-pod-and-container) for a PMM Client container. It must not exceed the limit.

If you specify a limit and don’t specify a request, Kubernetes uses the specified limit as the requested value for a resource.

| Value type | Example |
| ---------- | ------- |
| string     | `150m`  |

### `pmm.resources.requests.memory`

[Kubernetes memory requests](https://kubernetes.io/docs/concepts/configuration/manage-compute-resources-container/#resource-requests-and-limits-of-pod-and-container) for PMM Client container. It must not exceed the limit.

If you specify a limit and don’t specify a request, Kubernetes uses the specified limit as the requested value for a resource.

| Value type | Example |
| ---------- | ------- |
| string     | `120Mi` |

### `pmm.resources.limits.cpu`

[Kubernetes CPU limits](https://kubernetes.io/docs/concepts/configuration/manage-compute-resources-container/#resource-requests-and-limits-of-pod-and-container) for a PMM Client container.

| Value type | Example |
| ---------- | ------- |
| int        | `200`   |

### `pmm.resources.limits.memory`

The [Kubernetes memory limits](https://kubernetes.io/docs/concepts/configuration/manage-compute-resources-container/#resource-requests-and-limits-of-pod-and-container) for a PMM Client container.

| Value type | Example |
| ---------- | ------- |
| string     | `128Mi` |

### `pmm.querySource`

Query source to track PostgreSQL statistics. Either pg_stat_monitor (`pgstatmonitor`, the default value) or pg_stat_statements (`pgstatstatements`) can be used.

| Value type | Example         |
| ---------- | --------------- |
| string     | `pgstatmonitor` |

### `pmm.postgresParams`

Additional parameters which will be passed to the `pmm-admin add postgresql` command for PostgreSQL Pods.

| Value type | Example |
| ---------- | ------- |
| string     |         |

### `pmm.containerSecurityContext`

A custom [Kubernetes Security Context](https://kubernetes.io/docs/tasks/configure-pod-container/security-context/) for the PMM Client container on each PostgreSQL instance Pod.

Starting with version 3.1.0, set `readOnlyRootFilesystem` to `true` to run the PMM Client with a read-only root filesystem. The Operator writes the PMM agent configuration to `/tmp/pmm-agent.yaml` file on the Pod’s volume. That volume stays writable when the root filesystem is read-only. If you leave this option unset, the container root filesystem stays writable.

Use this setting when your cluster’s security policy requires a read-only root filesystem. See [Run the PMM Client with a read-only root filesystem](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/monitoring.html#run-the-pmm-client-with-a-read-only-root-filesystem).

| Value type | Example                        |
| ---------- | ------------------------------ |
| subdoc     | `readOnlyRootFilesystem: true` |

## Log collector section

The `logcollector` section in the [deploy/cr.yaml](https://github.com/percona/percona-postgresql-operator/blob/main/deploy/cr.yaml) file contains configuration options for [Fluent Bit](https://fluentbit.io/) log collector and logrotate. Available starting with Operator version 3.1.0. See [Persistent logging](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/persistent-logging.html) and [Log rotation](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/log-rotation.html).

### `logcollector.enabled`

Enables or disables [persistent logging with Fluent Bit](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/persistent-logging.html). Disabled by default.

| Value type | Example |
| ---------- | ------- |
| boolean    | `false` |

### `logcollector.image`

Log collector Docker image to use.

| Value type | Example                                          |
| ---------- | ------------------------------------------------ |
| string     | `docker.io/percona/fluentbit:{{ logcollector }}` |

### `logcollector.imagePullPolicy`

This option is used to set the [policy](https://kubernetes.io/docs/concepts/containers/images/#updating-images) for updating log collector images.

| Value type | Example        |
| ---------- | -------------- |
| string     | `IfNotPresent` |

### `logcollector.configuration`

Extra Fluent Bit configuration merged with the Operator-managed pipeline. Must be in [Fluent Bit YAML configuration format](https://docs.fluentbit.io/manual/administration/configuring-fluent-bit/yaml/) . The classic `.conf` format is not supported. Invalid configuration is ignored by the collector at startup.

| Value type | Example |
| ---------- | ------- |
| subdoc     |         |

### `logcollector.env.name`

The name of a custom environment variable for the `logs` sidecar containers.

| Value type | Example  |
| ---------- | -------- |
| string     | `MY_ENV` |

### `logcollector.env.value`

The value of a custom environment variable for the log collector `logs` sidecar containers.

| Value type | Example    |
| ---------- | ---------- |
| string     | `my-value` |

### `logcollector.envFrom.secretRef.name`

The name of a Secret from which environment variables are loaded for the log collector `logs` sidecar containers (for example, credentials for a remote Fluent Bit output).

| Value type | Example                   |
| ---------- | ------------------------- |
| string     | `my-log-collector-secret` |

### `logcollector.envFrom.configMapRef.name`

The name of a ConfigMap from which environment variables are loaded for the log collector `logs` sidecar containers.

| Value type | Example                   |
| ---------- | ------------------------- |
| string     | `my-log-collector-config` |

### `logcollector.resources.requests.memory`

[Kubernetes memory requests](https://kubernetes.io/docs/concepts/configuration/manage-compute-resources-container/#resource-requests-and-limits-of-pod-and-container) for the log collector `logs` sidecar containers. It must not exceed the limit.

If you specify a limit and don’t specify a request, Kubernetes uses the specified limit as the requested value for a resource.

| Value type | Example |
| ---------- | ------- |
| string     | `150M`  |

### `logcollector.resources.requests.cpu`

[Kubernetes CPU requests](https://kubernetes.io/docs/concepts/configuration/manage-compute-resources-container/#resource-requests-and-limits-of-pod-and-container) for the log collector `logs` sidecar containers. It must not exceed the limit.

If you specify a limit and don’t specify a request, Kubernetes uses the specified limit as the requested value for a resource.

| Value type | Example |
| ---------- | ------- |
| string     | `300m`  |

### `logcollector.resources.limits.memory`

[Kubernetes memory limits](https://kubernetes.io/docs/concepts/configuration/manage-compute-resources-container/#resource-requests-and-limits-of-pod-and-container) for the log collector `logs` sidecar containers.

| Value type | Example |
| ---------- | ------- |
| string     | `200M`  |

### `logcollector.resources.limits.cpu`

[Kubernetes CPU limits](https://kubernetes.io/docs/concepts/configuration/manage-compute-resources-container/#resource-requests-and-limits-of-pod-and-container) for the log collector `logs` sidecar containers.

| Value type | Example |
| ---------- | ------- |
| string     | `350m`  |

### `logcollector.containerSecurityContext`

A custom [Kubernetes Security Context](https://kubernetes.io/docs/tasks/configure-pod-container/security-context/) for the log collector `logs` sidecar containers.

| Value type | Example |
| ---------- | ------- |
| subdoc     |         |

### `logcollector.livenessProbe`

A custom [Kubernetes liveness probe](https://kubernetes.io/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes/#configure-probes) for the `logs` (log collector) sidecar container. When not set, the container has no liveness probe. A `tcpSocket` or `httpGet` probe on port `2020` requires the Fluent Bit HTTP server to be enabled via `logcollector.configuration`:

```
logcollector:
  enabled: true
  configuration: |
    service:
      http_server: on
      http_listen: 0.0.0.0
      http_port: 2020
  livenessProbe:
    tcpSocket:
      port: 2020
    initialDelaySeconds: 30
    periodSeconds: 15
```

| Value type | Example                     |
| ---------- | --------------------------- |
| subdoc     | `tcpSocket: { port: 2020 }` |

### `logcollector.livenessProbe.initialDelaySeconds`

Number of seconds to wait after the `logs` container starts before initiating the liveness probe.

| Value type | Example |
| ---------- | ------- |
| int        | `30`    |

### `logcollector.livenessProbe.periodSeconds`

How often to perform the liveness probe (in seconds).

| Value type | Example |
| ---------- | ------- |
| int        | `15`    |

### `logcollector.readinessProbe`

A custom [Kubernetes readiness probe](https://kubernetes.io/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes/#configure-probes) for the `logs` (logcollector) sidecar container. When not set, the container has no readiness probe. A `tcpSocket` or `httpGet` probe on port `2020` requires the Fluent Bit HTTP server to be enabled via `logcollector.configuration` (`http_server: on` under `service`):

```
logcollector:
  enabled: true
  configuration: |
    service:
      http_server: on
      http_listen: 0.0.0.0
      http_port: 2020
  readinessProbe:
    tcpSocket:
      port: 2020
    initialDelaySeconds: 5
    periodSeconds: 10
```

| Value type | Example                     |
| ---------- | --------------------------- |
| subdoc     | `tcpSocket: { port: 2020 }` |

### `logcollector.readinessProbe.initialDelaySeconds`

Number of seconds to wait after the `logs` container starts before initiating the readiness probe.

| Value type | Example |
| ---------- | ------- |
| int        | `5`     |

### `logcollector.readinessProbe.periodSeconds`

How often to perform the readiness probe (in seconds).

| Value type | Example |
| ---------- | ------- |
| int        | `10`    |

### `logcollector.volumeMounts`

Extra [volume mounts](https://kubernetes.io/docs/concepts/storage/volumes/) for the log collector sidecar containers (for example, a CA bundle for an S3 output).

| Value type | Example                                                          |
| ---------- | ---------------------------------------------------------------- |
| subdoc     | `- name: s3-ca   mountPath: /etc/fluentbit/tls   readOnly: true` |

### `logcollector.volumes`

Extra [volumes](https://kubernetes.io/docs/concepts/storage/volumes/) for the PostgreSQL instance Pods used by the log collector sidecars.

| Value type | Example                                            |
| ---------- | -------------------------------------------------- |
| subdoc     | `- name: s3-ca   secret:     secretName: my-s3-ca` |

### `logcollector.logRotate.configuration`

Overrides the default logrotate configuration used by the `logrotate` sidecar. You must provide the full configuration because the Operator replaces the default configuration with the one you provide. See [Configure log rotation](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/log-rotation.html#configure-log-rotation).

| Value type | Example |
| ---------- | ------- |
| subdoc     |         |

### `logcollector.logRotate.extraConfig.name`

References a ConfigMap containing additional logrotate configuration. The key name must end with `.conf`. The `postgres.conf` key name is reserved for the Operator-managed main configuration.

| Value type | Example               |
| ---------- | --------------------- |
| string     | `my-logrotate-config` |

### `logcollector.logRotate.schedule`

Cron expression for the logrotate schedule (default: `0 0 * * *`).

| Value type | Example       |
| ---------- | ------------- |
| string     | `0 */6 * * *` |

### `logcollector.logRotate.livenessProbe`

A custom [Kubernetes liveness probe](https://kubernetes.io/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes/#configure-probes) for the `logrotate` sidecar container. When not set, the container has no liveness probe.

| Value type | Example                          |
| ---------- | -------------------------------- |
| subdoc     | `exec: { command: [/bin/true] }` |

### `logcollector.logRotate.livenessProbe.initialDelaySeconds`

Number of seconds to wait after the container starts before initiating the liveness probe.

| Value type | Example |
| ---------- | ------- |
| int        | `30`    |

### `logcollector.logRotate.livenessProbe.periodSeconds`

How often to perform the liveness probe (in seconds).

| Value type | Example |
| ---------- | ------- |
| int        | `15`    |

### `logcollector.logRotate.readinessProbe`

A custom [Kubernetes readiness probe](https://kubernetes.io/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes/#configure-probes) for the `logrotate` sidecar container. When not set, the container has no readiness probe.

| Value type | Example                          |
| ---------- | -------------------------------- |
| subdoc     | `exec: { command: [/bin/true] }` |

### `logcollector.logRotate.readinessProbe.initialDelaySeconds`

Number of seconds to wait after the container starts before initiating the readiness probe.

| Value type | Example |
| ---------- | ------- |
| int        | `5`     |

### `logcollector.logRotate.readinessProbe.periodSeconds`

How often to perform the readiness probe (in seconds).

| Value type | Example |
| ---------- | ------- |
| int        | `10`    |

## Proxy section

The `proxy` section in the [deploy/cr.yaml](https://github.com/percona/percona-postgresql-operator/blob/main/deploy/cr.yaml) file contains configuration options for the [pgBouncer](http://pgbouncer.github.io/) connection pooler for PostgreSQL.

### `proxy.pgBouncer.metadata.labels`

Set [labels](https://kubernetes.io/docs/concepts/overview/working-with-objects/labels/) for pgBouncer Pods.

| Value type | Example                      |
| ---------- | ---------------------------- |
| label      | `pg-cluster-label: cluster1` |

### `proxy.pgBouncer.replicas`

The number of the pgBouncer Pods to provide connection pooling.

| Value type | Example |
| ---------- | ------- |
| int        | `3`     |

### `proxy.pgBouncer.image`

Docker image for the [pgBouncer](http://pgbouncer.github.io/) connection pooler.

| Value type | Example                                        |
| ---------- | ---------------------------------------------- |
| string     | `docker.io/percona/percona-pgbouncer:1.25.2-8` |

### `proxy.pgBouncer.env.name`

Name of an environment variable for pgBouncer Pods. Read more about defining environment variables in [Kubernetes documentation](https://kubernetes.io/docs/tasks/inject-data-application/define-environment-variable-container/) .

| Value type | Example  |
| ---------- | -------- |
| string     | `MY_ENV` |

### `proxy.pgBouncer.env.value`

The value for an environment variable.

| Value type | Example |
| ---------- | ------- |
| string     | `1000`  |

### `proxy.pgBouncer.envFrom.secretRefName`

Name of a Secret or a ConfigMap, key/values of which are used as environment variables for pgBouncer Pods.

| Value type | Example                |
| ---------- | ---------------------- |
| string     | `pgbouncer-env-secret` |

### `proxy.pgBouncer.exposeSuperusers`

Enables or disables [exposing superuser user through pgBouncer](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/users.html#superuser-and-pgbouncer).

| Value type | Example |
| ---------- | ------- |
| boolean    | `false` |

### `proxy.pgBouncer.usersSecret.name`

Name of a Secret whose keys and values the Operator appends to the pgBouncer authentication file. Each key is a username and each value is the password. The Secret must be in the same namespace as the cluster. See [Add extra users to the pgBouncer authentication file](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/users.html#add-extra-users-to-the-pgbouncer-authentication-file).

| Value type | Example           |
| ---------- | ----------------- |
| string     | `pgbouncer-users` |

### `proxy.pgBouncer.paused`

Pauses or resumes pgBouncer connections. When `true`, the Operator issues `PAUSE` on every pgBouncer Pod so clients stay connected while backend traffic stops. Set back to `false` to resume. See [Pause and resume pgBouncer connections](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/pause-pgbouncer.html).

| Value type | Example |
| ---------- | ------- |
| boolean    | `true`  |

### `proxy.pgBouncer.resources.requests.cpu`

[Kubernetes CPU requests](https://kubernetes.io/docs/concepts/configuration/manage-compute-resources-container/#resource-requests-and-limits-of-pod-and-container) for a pgBouncer container. It must not exceed the limit.

If you specify a limit and don’t specify a request, Kubernetes uses the specified limit as the requested value for a resource.

| Value type | Example |
| ---------- | ------- |
| string     | `150m`  |

### `proxy.pgBouncer.resources.requests.memory`

[Kubernetes memory requests](https://kubernetes.io/docs/concepts/configuration/manage-compute-resources-container/#resource-requests-and-limits-of-pod-and-container) for a pgBouncer container. It must not exceed the limit.

If you specify a limit and don’t specify a request, Kubernetes uses the specified limit as the requested value for a resource.

| Value type | Example |
| ---------- | ------- |
| string     | `120Mi` |

### `proxy.pgBouncer.resources.limits.cpu`

[Kubernetes CPU limits](https://kubernetes.io/docs/concepts/configuration/manage-compute-resources-container/#resource-requests-and-limits-of-pod-and-container) for a pgBouncer container.

| Value type | Example |
| ---------- | ------- |
| string     | `200m`  |

### `proxy.pgBouncer.resources.limits.memory`

The [Kubernetes memory limits](https://kubernetes.io/docs/concepts/configuration/manage-compute-resources-container/#resource-requests-and-limits-of-pod-and-container) for a pgBouncer container.

| Value type | Example |
| ---------- | ------- |
| string     | `128Mi` |

### `proxy.pgBouncer.containers.pgbouncerConfig.resources.limits.cpu`

[Kubernetes CPU limits](https://kubernetes.io/docs/concepts/configuration/manage-compute-resources-container/#resource-requests-and-limits-of-pod-and-container) for `pgbouncer-config` sidecar container.

| Value type | Example |
| ---------- | ------- |
| string     | `1.0`   |

### `proxy.pgBouncer.containers.pgbouncerConfig.resources.limits.memory`

The [Kubernetes memory limits](https://kubernetes.io/docs/concepts/configuration/manage-compute-resources-container/#resource-requests-and-limits-of-pod-and-container) for `pgbouncer-config` sidecar container.

| Value type | Example |
| ---------- | ------- |
| string     | `1Gi`   |

### `proxy.pgBouncer.containers.pgbouncerConfig.resources.requests.cpu`

[Kubernetes CPU requests](https://kubernetes.io/docs/concepts/configuration/manage-compute-resources-container/#resource-requests-and-limits-of-pod-and-container) for a `pgbouncer-config` sidecar container. It must not exceed the limit.

If you specify a limit and don’t specify a request, Kubernetes uses the specified limit as the requested value for a resource.

| Value type | Example |
| ---------- | ------- |
| string     | `150m`  |

### `proxy.pgBouncer.containers.pgbouncerConfig.resources.requests.memory`

[Kubernetes memory requests](https://kubernetes.io/docs/concepts/configuration/manage-compute-resources-container/#resource-requests-and-limits-of-pod-and-container) for a `pgbouncer-config` sidecar container. It must not exceed the limit.

If you specify a limit and don’t specify a request, Kubernetes uses the specified limit as the requested value for a resource.

| Value type | Example |
| ---------- | ------- |
| string     | `120Mi` |

### `proxy.pgBouncer.expose.type`

Specifies the type of [Kubernetes Service](https://kubernetes.io/docs/concepts/services-networking/service/#publishing-services-service-types) for pgBouncer.

| Value type | Example     |
| ---------- | ----------- |
| string     | `ClusterIP` |

### `proxy.pgBouncer.expose.annotations`

The [Kubernetes annotations](https://kubernetes.io/docs/concepts/overview/working-with-objects/annotations/) metadata for pgBouncer.

| Value type | Example                 |
| ---------- | ----------------------- |
| label      | `my-annotation: value1` |

### `proxy.pgBouncer.expose.labels`

Set [labels](https://kubernetes.io/docs/concepts/overview/working-with-objects/labels/) for the pgBouncer Service.

| Value type | Example                      |
| ---------- | ---------------------------- |
| label      | `pg-cluster-label: cluster1` |

### `proxy.pgBouncer.expose.loadBalancerClass`

Define the implementation of the load balancer you want to use. This setting enables you to select a custom or specific load balancer class instead of the default one provided by the cloud provider.

| Value type | Example                 |
| ---------- | ----------------------- |
| string     | `eks.amazonaws.com/nlb` |

### `proxy.pgBouncer.expose.loadBalancerSourceRanges`

The range of client IP addresses from which the load balancer should be reachable (if not set, there is no limitations).

| Value type | Example        |
| ---------- | -------------- |
| string     | `"10.0.0.0/8"` |

### `proxy.pgBouncer.affinity.podAntiAffinity`

[Pod anti-affinity](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/constraints.html#affinity-and-anti-affinity), allows setting the standard Kubernetes affinity constraints of any complexity.

| Value type | Example |
| ---------- | ------- |
| subdoc     |         |

### ‘proxy.pgBouncer.securityContext’

A custom [Kubernetes Security Context for a Pod](https://kubernetes.io/docs/tasks/configure-pod-container/security-context/) to be used instead of the default one.

| Value type | Example                                                                                                                                                                                                                                                                                                                                                                              |
| ---------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| subdoc     | `fsGroup: 1001 runAsUser: 1001 runAsNonRoot: true fsGroupChangePolicy: “OnRootMismatch” runAsGroup: 1001 seLinuxOptions:   type: spc_t   level: s0:c123,c456 seccompProfile:   type: Localhost   localhostProfile: localhost/profile.json supplementalGroups: - 1001 sysctls: - name: net.ipv4.tcp_keepalive_time   value: “600” - name: net.ipv4.tcp_keepalive_intvl   value: “60”` |

### `proxy.pgBouncer.config`

Custom configuration options for the pgBouncer `pgbouncer.ini` file (for example, `pool_mode` or `stats_users`). To add extra users to the authentication file, use [`proxy.pgBouncer.usersSecret`](#proxypgbounceruserssecretname). Configuration changes are automatically applied to the running instances without validation, so an invalid config can make the cluster unavailable.

| Value type | Example                          |
| ---------- | -------------------------------- |
| subdoc     | `global: pool_mode: transaction` |

### `proxy.pgBouncer.additionalTrustedCAs`

Additional CA bundles that PgBouncer trusts when verifying client certificates. Each item names a Secret in the same namespace as the cluster. The Secret must contain a PEM-encoded CA certificate or bundle in the `ca.crt` key. The Operator appends these CAs to the PgBouncer frontend trust bundle and keeps managing the PgBouncer frontend certificate. See [Trust additional CAs for PgBouncer client mTLS](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/tls-pgbouncer-trusted-cas.html) for details.

| Value type | Example             |
| ---------- | ------------------- |
| array      | `- name: client-ca` |

## proxy.pgBouncer.sidecars subsection

The `proxy.pgBouncer.sidecars` subsection in the [deploy/cr.yaml](https://github.com/percona/percona-postgresql-operator/blob/main/deploy/cr.yaml) file contains configuration options for [custom sidecar containers](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/sidecar.html) which can be added to pgBouncer Pods.

### `proxy.pgBouncer.sidecars.image`

Image for the [custom sidecar container](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/sidecar.html) for pgBouncer Pods.

| Value type | Example               |
| ---------- | --------------------- |
| string     | `mycontainer1:latest` |

### `proxy.pgBouncer.sidecars.name`

Name of the [custom sidecar container](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/sidecar.html) for pgBouncer Pods.

| Value type | Example         |
| ---------- | --------------- |
| string     | `testcontainer` |

### `proxy.pgBouncer.sidecars.imagePullPolicy`

This option is used to set the [policy](https://kubernetes.io/docs/concepts/containers/images/#updating-images) for the pgBouncer Pod sidecar container.

| Value type | Example  |
| ---------- | -------- |
| string     | `Always` |

### `proxy.pgBouncer.sidecars.env`

The [environment variables set as key-value pairs](https://kubernetes.io/docs/tasks/inject-data-application/define-environment-variable-container/) for the [custom sidecar container](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/sidecar.html) for pgBouncer Pods.

| Value type | Example |
| ---------- | ------- |
| subdoc     |         |

### `proxy.pgBouncer.sidecars.envFrom`

The [environment variables set as key-value pairs in ConfigMaps](https://kubernetes.io/docs/tasks/inject-data-application/define-environment-variable-container/) for the [custom sidecar container](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/sidecar.html) for pgBouncer Pods.

| Value type | Example |
| ---------- | ------- |
| subdoc     |         |

### `proxy.pgBouncer.sidecars.command`

Command for the [custom sidecar container](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/sidecar.html) for pgBouncer Pods.

| Value type | Example       |
| ---------- | ------------- |
| array      | `["/bin/sh"]` |

### `proxy.pgBouncer.sidecars.args`

Command arguments for the [custom sidecar container](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/sidecar.html) for pgBouncer Pods.

| Value type | Example                                                                        |
| ---------- | ------------------------------------------------------------------------------ |
| array      | `["-c", "while true; do trap 'exit 0' SIGINT SIGTERM SIGQUIT SIGKILL; done;"]` |

### `proxy.pgBouncer.sidecarVolumes.name`

The name of the [volumes](https://kubernetes.io/docs/concepts/storage/volumes/) to attach to `pgBouncer` Pods for use by [custom sidecar containers](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/sidecar.html). Supports secret, configMap, NFS, and other volume types.

| Value type                    | Example        |
| ----------------------------- | -------------- |
| :material-text-string: string | sidecar-secret |

### `proxy.pgBouncer.sidecarVolumes.secret.secretName`

The name of the [volume Secret](https://kubernetes.io/docs/concepts/storage/volumes/) to attach to `pgBouncer` Pods for use by [custom sidecar containers](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/sidecar.html).

| Value type                    | Example  |
| ----------------------------- | -------- |
| :material-text-string: string | mysecret |

### `proxy.pgBouncer.sidecarVolumes.configMap.name`

The name of the configMap object to attach to `pgBouncer` Pods for use by [custom sidecar containers](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/sidecar.html).

| Value type                    | Example        |
| ----------------------------- | -------------- |
| :material-text-string: string | sidecar-config |

### `proxy.pgBouncer.sidecarVolumes.nfs.server`

The hostname of the NFS server that will provide remote filesystem to the [custom sidecar containers](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/sidecar.html) in `pgBouncer` Pods.

| Value type                    | Example                                 |
| ----------------------------- | --------------------------------------- |
| :material-text-string: string | “nfs-service.storage.svc.cluster.local” |

### `proxy.pgBouncer.sidecarVolumes.nfs.path`

The path on the NFS server that will be provided as a remote filesystem to the [custom sidecar containers](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/sidecar.html) in `pgBouncer` Pods.

| Value type                    | Example                                 |
| ----------------------------- | --------------------------------------- |
| :material-text-string: string | “nfs-service.storage.svc.cluster.local” |

### `proxy.pgBouncer.sidecarPVCs`

[PersistentVolumeClaims](https://kubernetes.io/docs/concepts/storage/persistent-volumes/) that the Operator creates and mounts for [custom sidecar containers](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/sidecar.html) in pgBouncer Pods.

You can use PVCs with sidecar containers only when you deploy a new cluster. Updates to running cluster are not supported.

| Value type | Example                                                                                                                                                      |
| ---------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| subdoc     | `- name: sidecar-volume-claim   spec:     resources:       requests:         storage: 1Gi     volumeMode: Filesystem     accessModes:       - ReadWriteOnce` |

## Patroni Section

The `patroni` section in the [deploy/cr.yaml](https://github.com/percona/percona-postgresql-operator/blob/main/deploy/cr.yaml) file contains configuration options to customize the PostgreSQL high-availability implementation based on [Patroni](https://patroni.readthedocs.io/) .

| Value type | Example |
| ---------- | ------- |
| int        | `3`     |

### `patroni.syncPeriodSeconds`

How often to perform [liveness/readiness probes](https://kubernetes.io/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes/#configure-probes) for the patroni container (in seconds).

| Value type | Example |
| ---------- | ------- |
| int        | `3`     |

### `patroni.leaderLeaseDurationSeconds`

Initial delay for [liveness/readiness probes](https://kubernetes.io/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes/#configure-probes) for the patroni container (in seconds).

### `patroni.dynamicConfiguration`

Custom PostgreSQL configuration options. Please note that configuration changes are automatically applied to the running instances without validation, so having an invalid config can make the cluster unavailable.

| Value type | Example                                                                                                                       |
| ---------- | ----------------------------------------------------------------------------------------------------------------------------- |
| subdoc     | `postgresql:   parameters:     max_parallel_workers: 2     max_worker_processes: 2     shared_buffers: 1GB     work_mem: 2MB` |

### `patroni.switchover.enabled`

Enables or disables [manual change of the cluster primary instance](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/change-primary.html).

| Value type | Example |
| ---------- | ------- |
| string     | `true`  |

### `patroni.switchover.targetInstance`

The name of the Pod that should be [set as the new primary](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/change-primary.html). When not specified, the new primary will be selected randomly.

| Value type | Example |
| ---------- | ------- |
| string     |         |

### `patroni.createReplicaMethods`

Defines available replica creation methods and the order of executing them during a cluster start or reinitialisation. Patroni will stop on the first one that returns 0.

By default, `pg_basebackup` is used to create replicas during a new cluster deployment. After the Operator makes an initial backup, it updates the Patroni ConfigMap assign the `pgBackRest` as the first item in the list. This configuration is not propagated to Patroni itself until you restart the database instance Pods or manually reload Patroni configuration.

In the same way, after you define the replica set methods and apply the configuration, the Operator updates the Patroni ConfigMap. You must manually reload Patroni configuration of every database instance to make Patroni aware of the changes. Read more about setting replica methods in the [Configure create_replica_methods](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/reinit.html#configure-create_replica_methods) section.

| Value type | Example                   |
| ---------- | ------------------------- |
| string     | - pgbackrest - basebackup |

## Custom extensions Section

The `extensions` section in the [deploy/cr.yaml](https://github.com/percona/percona-postgresql-operator/blob/main/deploy/cr.yaml) file contains configuration options to [manage PostgreSQL extensions](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/custom-extensions.html).

### `extensions.image`

Image for the custom PostgreSQL extension loader sidecar container.

| Value type | Example                                               |
| ---------- | ----------------------------------------------------- |
| string     | `docker.io/percona/percona-postgresql-operator:3.1.0` |

### `extensions.imagePullPolicy`

[Policy](https://kubernetes.io/docs/concepts/containers/images/#updating-images) for the custom extension sidecar container.

| Value type | Example  |
| ---------- | -------- |
| string     | `Always` |

### `extensions.storage.type`

The cloud storage type used for backups. Only `s3` type is currently supported.

| Value type | Example |
| ---------- | ------- |
| string     | `s3`    |

### `extensions.storage.bucket`

The [Amazon S3 bucket](https://docs.aws.amazon.com/AmazonS3/latest/dev/UsingBucket.html) name for prepackaged PostgreSQL custom extensions.

| Value type | Example         |
| ---------- | --------------- |
| string     | `pg-extensions` |

### `extensions.storage.region`

The [AWS region](https://docs.aws.amazon.com/general/latest/gr/rande.html) to use.

| Value type | Example        |
| ---------- | -------------- |
| string     | `eu-central-1` |

### `extensions.storage.endpoint`

The [S3 endpoint](https://docs.aws.amazon.com/general/latest/gr/s3.html) to use.

| Value type | Example                         |
| ---------- | ------------------------------- |
| string     | `s3.eu-central-1.amazonaws.com` |

### `extensions.storage.forcePathStyle`

When set to `true`, enforces path-style access method of constructing S3 URLs, where the bucket name appears in the path portion of the URL. Default `false` value means the Operator uses the virtual-hosted-style for accessing S3 storage, where the bucket name is part of the domain name.

| Value type | Example |
| ---------- | ------- |
| boolean    | `false` |

### `extensions.storage.disableSSL`

When set to `true`, instructs the Operator to skip TLS verification when accessing the storage. Can be used if your storage endpoint uses self-signed certificates or doesn’t support TLS to allow successful downloads.

| Value type | Example |
| ---------- | ------- |
| boolean    | `false` |

### `extensions.storage.secret.name`

The [Kubernetes secret](https://kubernetes.io/docs/concepts/configuration/secret/) for the custom extensions storage. It should contain `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY` keys.

| Value type | Example                      |
| ---------- | ---------------------------- |
| string     | `cluster1-extensions-secret` |

### `extensions.builtin.pg_stat_monitor`

Enable or disable [pg_stat_monitor](https://docs.percona.com/pg-stat-monitor/index.html) PostgreSQL extension. Disabled by default starting with version 2.9.0.

This option is deprecated. Use the [`extensions.pg_stat_monitor`](#extensionspg_stat_monitor) option instead.

| Value type | Example |
| ---------- | ------- |
| boolean    | `false` |

### `extensions.builtin.pg_stat_statements`

Enable or disable [pg_stat_statements](https://www.postgresql.org/docs/current/pgstatstatements.html) PostgreSQL extension.

This option is deprecated. Use the [`extensions.pg_stat_statements`](#extensionspg_stat_statements) option instead.

| Value type | Example |
| ---------- | ------- |
| boolean    | `false` |

### `extensions.builtin.pg_audit`

Enable or disable [PGAudit](https://www.pgaudit.org/) PostgreSQL extension.

This option is deprecated. Use the [`extensions.pg_audit`](#extensionspg_audit) option instead.

| Value type | Example |
| ---------- | ------- |
| boolean    | `true`  |

### `extensions.builtin.pgvector`

Enable or disable [pgvector](https://github.com/pgvector/pgvector) PostgreSQL extension. **This extension is not compatible with PostgreSQL 12!**

This option is deprecated. Use the [`extensions.pgvector`](#extensionspgvector) option instead.

| Value type | Example |
| ---------- | ------- |
| boolean    | `false` |

### `extensions.builtin.pg_repack`

Enable or disable [pg_repack](https://github.com/reorg/pg_repack) PostgreSQL extension.

This option is deprecated. Use the [`extensions.pg_repack`](#extensionspg_repack) option instead.

| Value type | Example |
| ---------- | ------- |
| boolean    | `false` |

### `extensions.pg_stat_monitor`

Enable or disable [pg_stat_monitor](https://docs.percona.com/pg-stat-monitor/index.html) PostgreSQL extension.

| Value type | Example |
| ---------- | ------- |
| boolean    | `true`  |

### `extensions.pg_stat_statements`

Enable or disable [pg_stat_statements](https://www.postgresql.org/docs/current/pgstatstatements.html) PostgreSQL extension.

| Value type | Example |
| ---------- | ------- |
| boolean    | `false` |

### `extensions.pg_audit`

Enable or disable [PGAudit](https://www.pgaudit.org/) PostgreSQL extension.

| Value type | Example |
| ---------- | ------- |
| boolean    | `true`  |

### `extensions.pgvector`

Enable or disable [pgvector](https://github.com/pgvector/pgvector) PostgreSQL extension. **This extension is not compatible with PostgreSQL 12!**

| Value type | Example |
| ---------- | ------- |
| boolean    | `false` |

### `extensions.pg_repack`

Enable or disable [pg_repack](https://github.com/reorg/pg_repack) PostgreSQL extension.

| Value type | Example |
| ---------- | ------- |
| boolean    | `false` |

### `extensions.pg_cron`

Enable or disable [pg_cron](https://github.com/citusdata/pg_cron) PostgreSQL extension.

| Value type | Example |
| ---------- | ------- |
| boolean    | `false` |

### `extensions.set_user`

Enable or disable [set_user](https://github.com/pgaudit/set_user) PostgreSQL extension.

| Value type | Example |
| ---------- | ------- |
| boolean    | `false` |

### `extensions.pg_tde.enabled`

Enable or disable [pg_tde](https://docs.percona.com/pg-tde/index.html) PostgreSQL extension for data-at-rest encryption. Read more in [Data-at-rest encryption](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/encryption.html).

This extension is compatible **with Percona Distribution for PostgreSQL 17 and above**. When you set `enabled` to `true`, you must also configure the key provider (`extensions.pg_tde.vault` section). You cannot remove the `pg_tde` or `vault` sections while encryption is still enabled; first set `enabled` to `false` and wait for Pod restarts. See [Disable encryption](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/encryption-disable.html).

| Value type | Example |
| ---------- | ------- |
| boolean    | `false` |

### `extensions.pg_tde.walEncryption`

Encrypt write-ahead log (WAL) segments on disk. Requires `extensions.pg_tde.enabled` to be `true`. You can set `walEncryption` in the same change as enabling `pg_tde`. Read more in [WAL encryption](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/encryption.html#wal-encryption) and [Configure pg_tde](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/encryption-setup.html#configure-pg_tde-in-the-custom-resource-manifest).

| Value type | Example |
| ---------- | ------- |
| boolean    | `false` |

### `extensions.pg_tde.vault.host`

The Vault server name and port. If Vault is deployed in a separate namespace, use the fully qualified name in the format `<service-name>.<namespace>.svc.cluster.local`. Use the HTTPS protocol for encrypted communication with TLS and HTTP protocol for communication without TLS.

| Value type | Example                      |
| ---------- | ---------------------------- |
| string     | `https://vault-service:8200` |

### `extensions.pg_tde.vault.mountPath`

The secrets mount path for a KV secrets engine v2 in Vault. Default path is `secret/data`. Use the path you specified when creating the secrets engine in Vault (for example, `tde`).

| Value type | Example |
| ---------- | ------- |
| string     | `tde`   |

### `extensions.pg_tde.vault.tokenSecret.name`

The name of the Secret object that stores a token to access Vault.

| Value type | Example               |
| ---------- | --------------------- |
| string     | `pg-tde-vault-secret` |

### `extensions.pg_tde.vault.tokenSecret.key`

Specifies the key in the Secret that holds the Vault token.

| Value type | Example |
| ---------- | ------- |
| string     | `token` |

### `extensions.pg_tde.vault.caSecret.name`

The name of the Secret object that stores the CA certificate for TLS verification with Vault. Required for TLS communication with Vault, optional if you use HTTP. You can use the same Secret for the token and the CA certificate.

| Value type | Example               |
| ---------- | --------------------- |
| string     | `pg-tde-vault-secret` |

### `extensions.pg_tde.vault.caSecret.key`

Specifies the key in the Secret that holds the CA certificate for Vault.

| Value type | Example  |
| ---------- | -------- |
| string     | `ca.crt` |

### `extensions.custom.name`

Name of the PostgreSQL custom extension.

| Value type | Example   |
| ---------- | --------- |
| string     | `pg_cron` |

### `extensions.custom.version`

Version of the PostgreSQL custom extension.

| Value type | Example |
| ---------- | ------- |
| string     | `1.6.1` |
