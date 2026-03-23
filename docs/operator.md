# Custom Resource options

The Cluster is configured via the
[deploy/cr.yaml :octicons-link-external-16:](https://github.com/percona/percona-postgresql-operator/blob/main/deploy/cr.yaml) file.

## `metadata`

The metadata part of this file contains the following keys:

* <a name="metadata-name"></a> `name` (`cluster1` by default) sets the name of your Percona Distribution
for PostgreSQL Cluster; it should include only [URL-compatible characters :octicons-link-external-16:](https://datatracker.ietf.org/doc/html/rfc3986#section-2.3), not exceed 22 characters, start with an alphabetic character, and end with an alphanumeric character;

* <a name="metadata-annotations-patroni-check"></a> `annotations.pgv2.percona.com/custom-patroni-version` [Kubernetes annotation  :octicons-link-external-16:](https://kubernetes.io/docs/concepts/overview/working-with-objects/annotations/) which allows turning off automatic Patroni version detection by the Operator. You can use this annotation to set the version manually ("3" for Patroni 3.x, "4" for Patroni 4.x).

* <a name="finalizers-delete-ssl"></a> `finalizers.percona.com/delete-ssl` if present, activates the [Finalizer :octicons-link-external-16:](https://kubernetes.io/docs/tasks/extend-kubernetes/custom-resources/custom-resource-definitions/#finalizers) which deletes [objects, created for SSL](TLS.md) (Secret, certificate, and issuer) after the cluster deletion event (off by default).

* <a name="finalizers-delete-pvc"></a> `finalizers.percona.com/delete-pvc` if present, activates the [Finalizer :octicons-link-external-16:](https://kubernetes.io/docs/tasks/extend-kubernetes/custom-resources/custom-resource-definitions/#finalizers) which deletes [Persistent Volume Claims :octicons-link-external-16:](https://kubernetes.io/docs/concepts/storage/persistent-volumes/) for the database cluster Pods and user Secrets after the deletion event (off by default).

* <a name="finalizers-delete-backups"></a> `finalizers.percona.com/delete-backups` if present, activates the [Finalizer :octicons-link-external-16:](https://kubernetes.io/docs/tasks/extend-kubernetes/custom-resources/custom-resource-definitions/#finalizers) which deletes all the [backups](backups.md) of the database cluster from all configured repos on cluster deletion event (off by default). **`delete-backups` finalizer is in tech preview state, and it is not yet recommended for production environments.**

## Top level `spec` elements

The spec part of the [deploy/cr.yaml :octicons-link-external-16:](https://github.com/percona/percona-postgresql-operator/blob/main/deploy/cr.yaml) file contains the following:

### `crVersion`

Version of the Operator the Custom Resource belongs to.

| Value type | Example |
| ---------- | ------- |
| :material-code-string: string | `{{ release }}` |

### `metadata.annotations`

The [Kubernetes annotations  :octicons-link-external-16:](https://kubernetes.io/docs/concepts/overview/working-with-objects/annotations/) metadata to be set at a global level for all resources created by the Operator.

| Value type  | Example    |
| ----------- | ---------- |
| :material-label-outline: label    | `example-annotation: value` |

### `metadata.labels`

The [Kubernetes labels  :octicons-link-external-16:](https://kubernetes.io/docs/concepts/overview/working-with-objects/labels/) metadata to be set at a global level for all resources created by the Operator.

| Value type  | Example    |
| ----------- | ---------- |
| :material-label-outline: label       | `example-label: value` |

### `tlsOnly`

Enforce the Operator to use only Transport Layer Security (TLS) for both internal and external communications.

| Value type | Example |
| ---------- | ------- |
| :material-toggle-switch-outline: boolean | `false` |

### `tls.certValidityDuration`

Validity duration for TLS certificates (cluster, instance, and PgBouncer). Used only when [cert-manager](tls-cert-manager.md) manages certificates. Format: Go duration (e.g. `2160h`). Default: `8760h` (1 year).

| Value type | Example |
| ---------- | ------- |
| :material-code-string: string | `2160h` |

### `tls.caValidityDuration`

Validity duration for the root CA certificate. Used only when [cert-manager](tls-cert-manager.md) manages certificates. Format: Go duration (e.g. `26280h`). Default: `8760h` (1 year).

| Value type | Example |
| ---------- | ------- |
| :material-code-string: string | `26280h` |

### `tls.pgBackRestCertValidityDuration`

Validity duration for the `pgBackRest` client and repository host certificates

### `standby.enabled`

Enables or disables running the cluster in a standby mode (read-only copy of an existing cluster, useful for disaster recovery, etc).

| Value type | Example |
| ---------- | ------- |
| :material-toggle-switch-outline: boolean | `false` |

### `standby.host`

Host address of the primary cluster this standby cluster connects to.

| Value type | Example |
| ---------- | ------- |
| :material-code-string: string | `"<primary-ip>"` |

### `standby.port`

Port number used by a standby copy to connect to the primary cluster.

| Value type | Example |
| ---------- | ------- |
| :material-code-string: string | `"<primary-port>"` |

### `openshift`

Set to `true` if the cluster is being deployed on OpenShift, set to `false` otherwise, or  unset it for auto-detection.

| Value type | Example |
| ---------- | ------- |
| :material-toggle-switch-outline: boolean | `true` |

### `autoCreateUserSchema`

If set to `true`, the cluster will have automatically created schemas for the [custom user](users.md#custom-users-and-databases) defined in the `spec.users` subsection for all of the databases listed for this specific user.

| Value type | Example |
| ---------- | ------- |
| :material-toggle-switch-outline: boolean | `true` |

### `standby.repoName`

Name of the pgBackRest repository in the primary cluster this standby cluster connects to.

| Value type | Example |
| ---------- | ------- |
| :material-code-string: string | `repo1` |

### `secrets.customRootCATLSSecret.name`

Name of the secret with the custom root CA certificate and key for secure connections to the PostgreSQL server, see [Transport Layer Security (TLS)](TLS.md) for details.

| Value type | Example |
| ---------- | ------- |
| :material-code-string: string | `cluster1-ca-cert` |

### `secrets.customRootCATLSSecret.items`
 
 Key-value pairs of the `key` (a key from the `secrets.customRootCATLSSecret.name` secret) and the `path` (name on the file system) for the custom root certificate and key. See [Transport Layer Security (TLS)](TLS.md) for details.

| Value type | Example |
| ---------- | ------- |
| :material-text-long: subdoc      | <pre>- key: "tls.crt"<br>  path: "root.crt"<br>- key: "tls.key"<br>  path: "root.key"</pre> |

### `secrets.customTLSSecret.name`

A secret with TLS certificate generated for *external* communications, see [Transport Layer Security (TLS)](TLS.md) for details.

| Value type | Example |
| ---------- | ------- |
| :material-code-string: string | `cluster1-cert` |

### `secrets.customReplicationTLSSecret.name`

A secret with TLS certificate generated for *internal* communications, see [Transport Layer Security (TLS)](TLS.md) for details.

| Value type | Example |
| ---------- | ------- |
| :material-code-string: string | `replication1-cert` |

### `users.name`

The name of the PostgreSQL user.

| Value type | Example |
| ---------- | ------- |
| :material-code-string: string | `rhino` |

### `users.databases`

Databases accessible by a specific PostgreSQL user with rights to create objects in them (the option is ignored for `postgres` user; also, modifying it can't be used to revoke the already given access).

| Value type | Example |
| ---------- | ------- |
| :material-code-string: string | `zoo` |

### `users.password.type`

The set of characters used for password generation: can be either `ASCII` (default) or `AlphaNumeric`.

| Value type | Example |
| ---------- | ------- |
| :material-code-string: string | `ASCII` |

### `users.options`

The `ALTER ROLE` options other than password (the option is ignored for `postgres` user).

| Value type | Example |
| ---------- | ------- |
| :material-code-string: string | `"SUPERUSER"` |

### `users.secretName`

The custom name of the user's Secret; if not specified, the default `<clusterName>-pguser-<userName>` variant will be used.

| Value type | Example |
| ---------- | ------- |
| :material-code-string: string | `"rhino-credentials"` |

### `users.grantPublicSchemaAccess`

Grants access to the `public` schema to the user for all databases associated with this user. 

| Value type | Example |
| ---------- | ------- |
| :material-code-string: string | `false` |

### `databaseInitSQL.key`

Data key for the [Custom configuration options ConfigMap :octicons-link-external-16:](https://kubernetes.io/docs/concepts/configuration/configmap/) with the init SQL file, which will be executed at cluster creation time.

| Value type | Example |
| ---------- | ------- |
| :material-code-string: string | `init.sql` |

### `databaseInitSQL.name`

Name of the [ConfigMap :octicons-link-external-16:](https://kubernetes.io/docs/concepts/configuration/configmap/) with the init SQL file, which will be executed at cluster creation time.

| Value type | Example |
| ---------- | ------- |
| :material-code-string: string | `cluster1-init-sql` |

### `pause`

Setting it to `true` gracefully stops the cluster, scaling workloads to zero and suspending CronJobs; setting it to `false` after shut down starts the cluster back.

| Value type | Example |
| ---------- | ------- |
| :material-code-string: string | `false` |

### `unmanaged`

Setting it to `true` stops the Operator's activity including the rollout and reconciliation of changes made in the Custom Resource; setting it to `false` starts the Operator's activity back.

| Value type | Example |
| ---------- | ------- |
| :material-code-string: string | `false` |

## `dataSource` subsection

Contains the configuration options for restoring from a backup onto a new cluster. For usage examples, see [Restore the backup to a new cluster (cluster clone)](backups-clone.md).

### `dataSource.postgresCluster.clusterName`

Name of an existing cluster to use as the data source when restoring backup to a new cluster. 

| Value type | Example |
| ---------- | ------- |
| :material-code-string: string | `cluster1` |

## `dataSource.postgresCluster.clusterNamespace`

Namespace of an existing cluster used as a data source (is needed if the new cluster will be created in a different namespace; needs the Operator deployed [in multi-namespace/cluster-wide mode](cluster-wide.md#install-the-operator-cluster-wide)).

| Value type | Example |
| ---------- | ------- |
| :material-code-string: string | `cluster1-namespace` |

### `dataSource.postgresCluster.repoName`

Name of the pgBackRest repository in the source cluster that contains the backup to be restored to a new cluster.

| Value type | Example |
| ---------- | ------- |
| :material-code-string: string | `repo1` |

### `dataSource.postgresCluster.options`

The pgBackRest command-line options for the pgBackRest restore command.

| Value type | Example |
| ---------- | ------- |
| :material-code-string: string | |

### `dataSource.postgresCluster.tolerations.effect`

The [Kubernetes Pod tolerations :octicons-link-external-16:](https://kubernetes.io/docs/concepts/configuration/taint-and-toleration/#concepts) effect for data migration.

| Value type | Example |
| ---------- | ------- |
| :material-code-string: string | `NoSchedule` |

### `dataSource.postgresCluster.tolerations.key`

The [Kubernetes Pod tolerations :octicons-link-external-16:](https://kubernetes.io/docs/concepts/configuration/taint-and-toleration/#concepts) key for data migration.

| Value type | Example |
| ---------- | ------- |
| :material-code-string: string | `role` |

### `dataSource.postgresCluster.tolerations.operator`

The [Kubernetes Pod tolerations :octicons-link-external-16:](https://kubernetes.io/docs/concepts/configuration/taint-and-toleration/#concepts) operator for data migration.

| Value type | Example |
| ---------- | ------- |
| :material-code-string: string | `Equal` |

### `dataSource.postgresCluster.tolerations.value`

The [Kubernetes Pod tolerations :octicons-link-external-16:](https://kubernetes.io/docs/concepts/configuration/taint-and-toleration/#concepts) value for data migration.

| Value type | Example |
| ---------- | ------- |
| :material-code-string: string | `connection-poolers` |

### `dataSource.pgbackrest.stanza`

Name of the [pgBackRest stanza :octicons-link-external-16:](https://pgbackrest.org/command.html) to use as the data source when restoring backup to a new cluster.

| Value type | Example |
| ---------- | ------- |
| :material-code-string: string | `db` |

### `dataSource.pgbackrest.configuration.secret.name`

Name of the [Kubernetes Secret object :octicons-link-external-16:](https://kubernetes.io/docs/concepts/configuration/secret/#using-imagepullsecrets) with custom pgBackRest configuration, which will be added to the pgBackRest configuration generated by the Operator.

| Value type | Example |
| ---------- | ------- |
| :material-code-string: string | `pgo-s3-creds` |

### `dataSource.pgbackrest.global`

Settings, which are to be included in the `global` section of the pgBackRest configuration generated by the Operator.

| Value type | Example |
| ---------- | ------- |
| :material-text-long: subdoc | `/pgbackrest/postgres-operator/hippo/repo1` |

### `dataSource.pgbackrest.repo.name`

Name of the pgBackRest repository.

| Value type | Example |
| ---------- | ------- |
| :material-code-string: string | `repo1` |

### `dataSource.pgbackrest.repo.s3.bucket`

The [Amazon S3 bucket :octicons-link-external-16:](https://docs.aws.amazon.com/AmazonS3/latest/dev/UsingBucket.html) or [Google Cloud Storage bucket :octicons-link-external-16:](https://cloud.google.com/storage/docs/key-terms#buckets)
name used for backups. Bucket name should follow [Amazon naming rules](https://docs.aws.amazon.com/AmazonS3/latest/userguide/bucketnamingrules.html) or [Google naming rules](https://cloud.google.com/storage/docs/buckets), and additionally, it can't contain dots.

| Value type | Example |
| ---------- | ------- |
| :material-code-string: string | `"my-bucket"` |

### `dataSource.pgbackrest.repo.s3.endpoint`

The endpoint URL of the S3-compatible storage to be used for backups (not needed for the original Amazon S3 cloud).

| Value type | Example |
| ---------- | ------- |
| :material-code-string: string | `"s3.ca-central-1.amazonaws.com"` |

### `dataSource.pgbackrest.repo.s3.region`

The [AWS region :octicons-link-external-16:](https://docs.aws.amazon.com/general/latest/gr/rande.html) to use for Amazon and all S3-compatible storages.

| Value type | Example |
| ---------- | ------- |
| :material-toggle-switch-outline: boolean | `"ca-central-1"` |

### `dataSource.pgbackrest.tolerations.effect`

The [Kubernetes Pod tolerations :octicons-link-external-16:](https://kubernetes.io/docs/concepts/configuration/taint-and-toleration/#concepts) effect for pgBackRest at data migration.

| Value type | Example |
| ---------- | ------- |
| :material-code-string: string | `NoSchedule` |

### `dataSource.pgbackrest.tolerations.key`

The [Kubernetes Pod tolerations :octicons-link-external-16:](https://kubernetes.io/docs/concepts/configuration/taint-and-toleration/#concepts) key for pgBackRest at data migration.

| Value type | Example |
| ---------- | ------- |
| :material-code-string: string | `role` |

### `dataSource.pgbackrest.tolerations.operator`

The [Kubernetes Pod tolerations :octicons-link-external-16:](https://kubernetes.io/docs/concepts/configuration/taint-and-toleration/#concepts) operator for pgBackRest at data migration.

| Value type | Example |
| ---------- | ------- |
| :material-code-string: string | `Equal` |

### `dataSource.pgbackrest.tolerations.value`

The [Kubernetes Pod tolerations :octicons-link-external-16:](https://kubernetes.io/docs/concepts/configuration/taint-and-toleration/#concepts) value for pgBackRest at data migration.

| Value type | Example |
| ---------- | ------- |
| :material-code-string: string | `connection-poolers` |

### `dataSource.volumes.pgDataVolume.pvcName`

The PostgreSQL data volume name for the [Persistent Volume Claim :octicons-link-external-16:](https://kubernetes.io/docs/concepts/storage/persistent-volumes/) used for data migration.

| Value type | Example |
| ---------- | ------- |
| :material-code-string: string | `cluster1` |

### `dataSource.volumes.pgDataVolume.directory`

The mount point for PostgreSQL data volume used for data migration.

| Value type | Example |
| ---------- | ------- |
| :material-code-string: string | `cluster1` |

### `dataSource.volumes.pgDataVolume.tolerations.effect`

The [Kubernetes Pod tolerations :octicons-link-external-16:](https://kubernetes.io/docs/concepts/configuration/taint-and-toleration/#concepts) effect for PostgreSQL data volume used for data migration.

| Value type | Example |
| ---------- | ------- |
| :material-code-string: string | `NoSchedule` |

### `dataSource.volumes.pgDataVolume.tolerations.key`

The [Kubernetes Pod tolerations :octicons-link-external-16:](https://kubernetes.io/docs/concepts/configuration/taint-and-toleration/#concepts) key for PostgreSQL data volume used for data migration.

| Value type | Example |
| ---------- | ------- |
| :material-code-string: string | `role` |

### `dataSource.volumes.pgDataVolume.tolerations.operator`

The [Kubernetes Pod tolerations :octicons-link-external-16:](https://kubernetes.io/docs/concepts/configuration/taint-and-toleration/#concepts) operator for PostgreSQL data volume used for data migration.

| Value type | Example |
| ---------- | ------- |
| :material-code-string: string | `Equal` |

### `dataSource.volumes.pgDataVolume.tolerations.value`

The [Kubernetes Pod tolerations :octicons-link-external-16:](https://kubernetes.io/docs/concepts/configuration/taint-and-toleration/#concepts) value for PostgreSQL data volume used for data migration.

| Value type | Example |
| ---------- | ------- |
| :material-code-string: string | `connection-poolers` |

### `dataSource.volumes.pgDataVolume.annotations`

The [Kubernetes annotations :octicons-link-external-16:](https://kubernetes.io/docs/concepts/overview/working-with-objects/annotations/) metadata for PostgreSQL data volume used for data migration.

| Value type | Example |
| ---------- | ------- |
| :material-label-outline: label | `test-annotation: value` |

### `dataSource.volumes.pgDataVolume.labels`

The [Kubernetes labels :octicons-link-external-16:](https://kubernetes.io/docs/concepts/overview/working-with-objects/labels/) for PostgreSQL data volume used for data migration.

| Value type | Example |
| ---------- | ------- |
| :material-label-outline: label | `test-label: value` |

### `dataSource.volumes.pgWALVolume.pvcName`

The PostgreSQL write-ahead logs volume name for the [Persistent Volume Claim :octicons-link-external-16:](https://kubernetes.io/docs/concepts/storage/persistent-volumes/) used for data migration.

| Value type | Example |
| ---------- | ------- |
| :material-code-string: string | `cluster1` |

### `dataSource.volumes.pgWALVolume.directory`

The mount point for PostgreSQL write-ahead logs volume used for data migration.

| Value type | Example |
| ---------- | ------- |
| :material-code-string: string | `cluster1` |

### `dataSource.volumes.pgWALVolume.tolerations.effect`

The [Kubernetes Pod tolerations :octicons-link-external-16:](https://kubernetes.io/docs/concepts/configuration/taint-and-toleration/#concepts) effect for PostgreSQL write-ahead logs volume used for data migration.

| Value type | Example |
| ---------- | ------- |
| :material-code-string: string | `NoSchedule` |

### `dataSource.volumes.pgWALVolume.tolerations.key`

The [Kubernetes Pod tolerations :octicons-link-external-16:](https://kubernetes.io/docs/concepts/configuration/taint-and-toleration/#concepts) key for PostgreSQL write-ahead logs volume used for data migration.

| Value type | Example |
| ---------- | ------- |
| :material-code-string: string | `role` |

### `dataSource.volumes.pgWALVolume.tolerations.operator`

The [Kubernetes Pod tolerations :octicons-link-external-16:](https://kubernetes.io/docs/concepts/configuration/taint-and-toleration/#concepts) operator for PostgreSQL write-ahead logs volume used for data migration.

| Value type | Example |
| ---------- | ------- |
| :material-code-string: string | `Equal` |

### `dataSource.volumes.pgWALVolume.tolerations.value`

The [Kubernetes Pod tolerations :octicons-link-external-16:](https://kubernetes.io/docs/concepts/configuration/taint-and-toleration/#concepts) value for PostgreSQL write-ahead logs volume used for data migration.

| Value type | Example |
| ---------- | ------- |
| :material-code-string: string | `connection-poolers` |

### `dataSource.volumes.pgWALVolume.annotations`

The [Kubernetes annotations :octicons-link-external-16:](https://kubernetes.io/docs/concepts/overview/working-with-objects/annotations/) metadata for PostgreSQL write-ahead logs volume used for data migration.

| Value type | Example |
| ---------- | ------- |
| :material-label-outline: label | `test-annotation: value` |

### `dataSource.volumes.pgWALVolume.labels`

The [Kubernetes labels :octicons-link-external-16:](https://kubernetes.io/docs/concepts/overview/working-with-objects/labels/) for PostgreSQL write-ahead logs volume used for data migration.

| Value type | Example |
| ---------- | ------- |
| :material-label-outline: label | `test-label: value` |

### `dataSource.volumes.pgBackRestVolume.pvcName`

The pgBackRest volume name for the [Persistent Volume Claim :octicons-link-external-16:](https://kubernetes.io/docs/concepts/storage/persistent-volumes/) used for data migration.

| Value type | Example |
| ---------- | ------- |
| :material-code-string: string | `cluster1` |

### `dataSource.volumes.pgBackRestVolume.directory`

The mount point for pgBackRest volume used for data migration.

| Value type | Example |
| ---------- | ------- |
| :material-code-string: string | `cluster1` |

### `dataSource.volumes.pgBackRestVolume.tolerations.effect`

The [Kubernetes Pod tolerations :octicons-link-external-16:](https://kubernetes.io/docs/concepts/configuration/taint-and-toleration/#concepts) effect pgBackRest volume used for data migration.

| Value type | Example |
| ---------- | ------- |
| :material-code-string: string | `NoSchedule` |

### `dataSource.volumes.pgBackRestVolume.tolerations.key`

The [Kubernetes Pod tolerations :octicons-link-external-16:](https://kubernetes.io/docs/concepts/configuration/taint-and-toleration/#concepts) key for pgBackRest volume used for data migration.

| Value type | Example |
| ---------- | ------- |
| :material-code-string: string | `role` |

### `dataSource.volumes.pgBackRestVolume.tolerations.operator`

The [Kubernetes Pod tolerations :octicons-link-external-16:](https://kubernetes.io/docs/concepts/configuration/taint-and-toleration/#concepts) operator for pgBackRest volume used for data migration.

| Value type | Example |
| ---------- | ------- |
| :material-code-string: string | `Equal` |

### `dataSource.volumes.pgBackRestVolume.tolerations.value`

The [Kubernetes Pod tolerations :octicons-link-external-16:](https://kubernetes.io/docs/concepts/configuration/taint-and-toleration/#concepts) value for pgBackRest volume used for data migration.

| Value type | Example |
| ---------- | ------- |
| :material-code-string: string | `connection-poolers` |

### `dataSource.volumes.pgBackRestVolume.annotations`

The [Kubernetes annotations :octicons-link-external-16:](https://kubernetes.io/docs/concepts/overview/working-with-objects/annotations/) metadata for pgBackRest volume used for data migration.

| Value type | Example |
| ---------- | ------- |
| :material-label-outline: label | `test-annotation: value` |

### `dataSource.volumes.pgBackRestVolume.labels`

The [Kubernetes labels :octicons-link-external-16:](https://kubernetes.io/docs/concepts/overview/working-with-objects/labels/) for pgBackRest volume used for data migration.

| Value type | Example |
| ---------- | ------- |
| :material-label-outline: label | `test-label: value` |

### `image`

The PostgreSQL Docker image to use.

| Value type | Example |
| ---------- | ------- |
| :material-code-string: string | `perconalab/percona-postgresql-operator:{{release}}-ppg{{postgresrecommended}}-postgres` |

### `imagePullPolicy`

This option is used to set the [policy :octicons-link-external-16:](https://kubernetes.io/docs/concepts/containers/images/#updating-images) for updating PostgreSQL images.

| Value type | Example |
| ---------- | ------- |
| :material-code-string: string | `Always` |

### `postgresVersion`

The major version of PostgreSQL to use.

| Value type | Example |
| ---------- | ------- |
| :material-numeric-1-box: int | `16` |

### `port`

The port number for PostgreSQL.

| Value type | Example |
| ---------- | ------- |
| :material-numeric-1-box: int | `5432` |

### `expose.annotations`

The [Kubernetes annotations :octicons-link-external-16:](https://kubernetes.io/docs/concepts/overview/working-with-objects/annotations/) metadata for PostgreSQL primary.

| Value type | Example |
| ---------- | ------- |
| :material-label-outline: label | `my-annotation: value1` |

### `expose.labels`

Set [labels :octicons-link-external-16:](https://kubernetes.io/docs/concepts/overview/working-with-objects/labels/) for the PostgreSQL primary.

| Value type | Example |
| ---------- | ------- |
| :material-label-outline: label | `my-label: value2` |

### `expose.type`

Specifies the type of [Kubernetes Service :octicons-link-external-16:](https://kubernetes.io/docs/concepts/services-networking/service/#publishing-services-service-types) for PostgreSQL primary.

| Value type | Example |
| ---------- | ------- |
| :material-code-string: string | `LoadBalancer` |

### `expose.loadBalancerClass`

Define the implementation of the load balancer you want to use. This setting enables you to select a custom or specific load balancer class instead of the default one provided by the cloud provider.

| Value type  | Example    |
| ----------- | ---------- |
| :material-code-string: string     | `eks.amazonaws.com/nlb`|

### `expose.loadBalancerSourceRanges`

The range of client IP addresses from which the load balancer should be reachable (if not set, there is no limitations).

| Value type | Example |
| ---------- | ------- |
| :material-code-string: string | `"10.0.0.0/8"` |

### `exposeReplicas.annotations`

The [Kubernetes annotations :octicons-link-external-16:](https://kubernetes.io/docs/concepts/overview/working-with-objects/annotations/) metadata for PostgreSQL replicas.

| Value type | Example |
| ---------- | ------- |
| :material-label-outline: label | `my-annotation: value1` |

### `exposeReplicas.labels`

Set [labels :octicons-link-external-16:](https://kubernetes.io/docs/concepts/overview/working-with-objects/labels/) for the PostgreSQL replicas.

| Value type | Example |
| ---------- | ------- |
| :material-label-outline: label | `my-label: value2` |

### `exposeReplicas.type`

Specifies the type of [Kubernetes Service :octicons-link-external-16:](https://kubernetes.io/docs/concepts/services-networking/service/#publishing-services-service-types) for PostgreSQL replicas.

| Value type | Example |
| ---------- | ------- |
| :material-code-string: string | `LoadBalancer` |

### `exposeReplicas.loadBalancerClass`

Define the implementation of the load balancer you want to use. This setting enables you to select a custom or specific load balancer class instead of the default one provided by the cloud provider.

| Value type  | Example    |
| ----------- | ---------- |
| :material-code-string: string     | `eks.amazonaws.com/nlb`|

### `exposeReplicas.loadBalancerSourceRanges`

The range of client IP addresses from which the load balancer should be reachable (if not set, there is no limitations).

| Value type | Example |
| ---------- | ------- |
| :material-code-string: string | `"10.0.0.0/8"` |

## <a name="operator-instances-section"></a>Instances section

The `instances` section in the [deploy/cr.yaml :octicons-link-external-16:](https://github.com/percona/percona-postgresql-operator/blob/main/deploy/cr.yaml)
file contains configuration options for PostgreSQL instances. This section contains at least one *cluster instance* with a number of *PostgreSQL instances* in it (cluster instances are groups of PostgreSQL instances used for fine-grained resources assignment).

### `instances.metadata.labels`

Set [labels :octicons-link-external-16:](https://kubernetes.io/docs/concepts/overview/working-with-objects/labels/) for PostgreSQL Pods.

| Value type | Example |
| ---------- | ------- |
| :material-label-outline: label | `pg-cluster-label: cluster1` |

### `instances.name`

The name of the PostgreSQL instance.

| Value type | Example |
| ---------- | ------- |
| :material-code-string: string | `rs 0` |

### `instances.replicas`

The number of Replicas to create for the PostgreSQL instance.

| Value type | Example |
| ---------- | ------- |
| :material-numeric-1-box: int | `3` |

### `instances.env.name`

Name of an environment variable for PostgreSQL Pods. Read more about defining environment variables in [Kubernetes documentation :octicons-link-external-16:](https://kubernetes.io/docs/tasks/inject-data-application/define-environment-variable-container/).

| Value type | Example |
| ---------- | ------- |
| :material-code-string: string | `MY_ENV` |

### `instances.env.value`

The value for an environment variable.

| Value type | Example |
| ---------- | ------- |
| :material-code-string: string | `1000` |

### `instances.envFrom.secretRefName`

Name of a Secret or a ConfigMap, key/values of which are used as environment variables for PostgreSQL Pods.

| Value type | Example |
| ---------- | ------- |
| :material-code-string: string | `instance-env-secret` |


### `instances.initContainer.image`

Defines an image for an init container to run before the main container in the Pod. The init container is typically used for setup tasks such as initializing filesystems, setting permissions, or preparing configuration.

| Value type | Example |
| ---------- | ------- |
| :material-code-string: string | `perconalab/percona-postgresql-operator:{{release}}` |

### `instances.initContainer.resources.limits.cpu`

[Kubernetes CPU limits :octicons-link-external-16:](https://kubernetes.io/docs/concepts/configuration/manage-compute-resources-container/#resource-requests-and-limits-of-pod-and-container) for an init container.

| Value type | Example |
| ---------- | ------- |
| :material-code-string: string | `2.0` |

### `instances.initContainer.resources.limits.memory`

The [Kubernetes memory limits :octicons-link-external-16:](https://kubernetes.io/docs/concepts/configuration/manage-compute-resources-container/#resource-requests-and-limits-of-pod-and-container) for an init container.

| Value type | Example |
| ---------- | ------- |
| :material-code-string: string | `4Gi` |

### `instances.initContainer.securityContext`

Security settings for the init container. These settings control privileges, user/group IDs, and other security-related options. For more details, see the [Kubernetes documentation on SecurityContext :octicons-link-external-16:](https://kubernetes.io/docs/tasks/configure-pod-container/security-context/)

| Value type  | Example    |
| ----------- | ---------- |
| :material-text-long: subdoc     | <pre>runAsUser: 1001<br>runAsGroup: 1001<br>runAsNonRoot: true <br>privileged: false<br>allowPrivilegeEscalation: false<br>readOnlyRootFilesystem: true </pre> |

### `instances.resources.requests.cpu`

[Kubernetes CPU requests :octicons-link-external-16:](https://kubernetes.io/docs/concepts/configuration/manage-compute-resources-container/#resource-requests-and-limits-of-pod-and-container) for a PostgreSQL instance. It must not exceed the limit.

If you specify a limit and don't specify a request, Kubernetes uses the specified limit as the requested value for a resource.

| Value type | Example |
| ---------- | ------- |
| :material-code-string: string | `1.0` |

### `instances.resources.requests.memory`

[Kubernetes memory requests :octicons-link-external-16:](https://kubernetes.io/docs/concepts/configuration/manage-compute-resources-container/#resource-requests-and-limits-of-pod-and-container) for a PostgreSQL instance. It must not exceed the limit.

If you specify a limit and don't specify a request, Kubernetes uses the specified limit as the requested value for a resource.

| Value type | Example |
| ---------- | ------- |
| :material-code-string: string | `3Gi` |

### `instances.resources.limits.cpu`

[Kubernetes CPU limits :octicons-link-external-16:](https://kubernetes.io/docs/concepts/configuration/manage-compute-resources-container/#resource-requests-and-limits-of-pod-and-container) for a PostgreSQL instance.

| Value type | Example |
| ---------- | ------- |
| :material-code-string: string | `2.0` |

### `instances.resources.limits.memory`

The [Kubernetes memory limits :octicons-link-external-16:](https://kubernetes.io/docs/concepts/configuration/manage-compute-resources-container/#resource-requests-and-limits-of-pod-and-container) for a PostgreSQL instance.

| Value type | Example |
| ---------- | ------- |
| :material-code-string: string | `4Gi` |

### `instances.containers.replicaCertCopy.resources.requests.cpu`

[Kubernetes CPU requests :octicons-link-external-16:](https://kubernetes.io/docs/concepts/configuration/manage-compute-resources-container/#resource-requests-and-limits-of-pod-and-container) for a `replica-cert-copy` sidecar container. It must not exceed the limit.

If you specify a limit and don't specify a request, Kubernetes uses the specified limit as the requested value for a resource.

| Value type | Example |
| ---------- | ------- |
| :material-code-string: string | `100m` |

### `instances.containers.replicaCertCopy.resources.requests.memory`

[Kubernetes memory requests :octicons-link-external-16:](https://kubernetes.io/docs/concepts/configuration/manage-compute-resources-container/#resource-requests-and-limits-of-pod-and-container) for a `replica-cert-copy` sidecar container. It must not exceed the limit.

If you specify a limit and don't specify a request, Kubernetes uses the specified limit as the requested value for a resource.

| Value type | Example |
| ---------- | ------- |
| :material-code-string: string | `120Mi` |

### `instances.containers.replicaCertCopy.resources.limits.cpu`

[Kubernetes CPU limits :octicons-link-external-16:](https://kubernetes.io/docs/concepts/configuration/manage-compute-resources-container/#resource-requests-and-limits-of-pod-and-container) for `replica-cert-copy` sidecar container.

| Value type | Example |
| ---------- | ------- |
| :material-code-string: string | `200m` |

### `instances.containers.replicaCertCopy.resources.limits.memory`

The [Kubernetes memory limits :octicons-link-external-16:](https://kubernetes.io/docs/concepts/configuration/manage-compute-resources-container/#resource-requests-and-limits-of-pod-and-container) for `replica-cert-copy` sidecar container.

| Value type | Example |
| ---------- | ------- |
| :material-code-string: string | `128Mi` |

### `instances.topologySpreadConstraints.maxSkew`

The degree to which Pods may be unevenly distributed under the [Kubernetes Pod Topology Spread Constraints :octicons-link-external-16:](https://kubernetes.io/docs/concepts/scheduling-eviction/topology-spread-constraints/).

| Value type | Example |
| ---------- | ------- |
| :material-numeric-1-box: int | `1` |

### `instances.topologySpreadConstraints.topologyKey`

The key of node labels for the [Kubernetes Pod Topology Spread Constraints :octicons-link-external-16:](https://kubernetes.io/docs/concepts/scheduling-eviction/topology-spread-constraints/).

| Value type | Example |
| ---------- | ------- |
| :material-code-string: string | `my-node-label` |

### `instances.topologySpreadConstraints.whenUnsatisfiable`

What to do with a Pod if it doesn't satisfy the [Kubernetes Pod Topology Spread Constraints :octicons-link-external-16:](https://kubernetes.io/docs/concepts/scheduling-eviction/topology-spread-constraints/).

| Value type | Example |
| ---------- | ------- |
| :material-code-string: string | `DoNotSchedule` |

### `instances.topologySpreadConstraints.labelSelector.matchLabels`

The Label selector for the [Kubernetes Pod Topology Spread Constraints :octicons-link-external-16:](https://kubernetes.io/docs/concepts/scheduling-eviction/topology-spread-constraints/).

| Value type | Example |
| ---------- | ------- |
| :material-label-outline: label | `postgres-operator.crunchydata.com/instance-set: instance1` |

### `instances.tolerations.effect`

The [Kubernetes Pod tolerations :octicons-link-external-16:](https://kubernetes.io/docs/concepts/configuration/taint-and-toleration/#concepts) effect for the PostgreSQL instance.

| Value type | Example |
| ---------- | ------- |
| :material-code-string: string | `NoSchedule` |

### `instances.tolerations.key`

The [Kubernetes Pod tolerations :octicons-link-external-16:](https://kubernetes.io/docs/concepts/configuration/taint-and-toleration/#concepts) key for the PostgreSQL instance.

| Value type | Example |
| ---------- | ------- |
| :material-code-string: string | `role` |

### `instances.tolerations.operator`

The [Kubernetes Pod tolerations :octicons-link-external-16:](https://kubernetes.io/docs/concepts/configuration/taint-and-toleration/#concepts) operator for the PostgreSQL instance.

| Value type | Example |
| ---------- | ------- |
| :material-code-string: string | `Equal` |

### `instances.tolerations.value`

The [Kubernetes Pod tolerations :octicons-link-external-16:](https://kubernetes.io/docs/concepts/configuration/taint-and-toleration/#concepts) value for the PostgreSQL instance.

| Value type | Example |
| ---------- | ------- |
| :material-code-string: string | `connection-poolers` |

### `instances.priorityClassName`

The [Kubernetes Pod priority class :octicons-link-external-16:](https://kubernetes.io/docs/concepts/configuration/pod-priority-preemption/#priorityclass) for PostgreSQL instance Pods.

| Value type | Example |
| ---------- | ------- |
| :material-code-string: string | `high-priority` |

### `instances.securityContext`

A custom [Kubernetes Security Context for a Pod :octicons-link-external-16:](https://kubernetes.io/docs/tasks/configure-pod-container/security-context/) to be used instead of the default one.

| Value type  | Example    |
| ----------- | ---------- |
| :material-text-long: subdoc      | <pre>fsGroup: 1001<br>runAsUser: 1001<br>runAsNonRoot: true<br>fsGroupChangePolicy: "OnRootMismatch"<br>runAsGroup: 1001<br>seLinuxOptions:<br>  type: spc_t<br>  level: s0:c123,c456<br>seccompProfile:<br>  type: Localhost<br>  localhostProfile: localhost/profile.json<br>supplementalGroups:<br>- 1001<br>sysctls:<br>- name: net.ipv4.tcp_keepalive_time<br>  value: "600"<br>- name: net.ipv4.tcp_keepalive_intvl<br>  value: "60"</pre> |

### `instances.walVolumeClaimSpec.accessModes`

The [Kubernetes PersistentVolumeClaim :octicons-link-external-16:](https://kubernetes.io/docs/concepts/storage/persistent-volumes/#persistentvolumeclaims) access modes for the PostgreSQL Write-ahead Log storage.

| Value type | Example |
| ---------- | ------- |
| :material-code-string: string | `ReadWriteOnce` |

### `instances.walVolumeClaimSpec.storageClassName`

Set the [Kubernetes storage class :octicons-link-external-16:](https://kubernetes.io/docs/concepts/storage/storage-classes/) to use with the PostgreSQL Write-ahead Log storage [PersistentVolumeClaim :octicons-link-external-16:](https://kubernetes.io/docs/concepts/storage/persistent-volumes/#persistentvolumeclaims).

| Value type | Example |
| ---------- | ------- |
| :material-code-string: string | `standard` |

### `instances.walVolumeClaimSpec.resources.requests.storage`

The [Kubernetes storage requests :octicons-link-external-16:](https://kubernetes.io/docs/concepts/configuration/manage-compute-resources-container/#resource-requests-and-limits-of-pod-and-container) for the storage the PostgreSQL instance will use.

| Value type | Example |
| ---------- | ------- |
| :material-code-string: string | `1Gi` |

### `instances.dataVolumeClaimSpec.accessModes`

The [Kubernetes PersistentVolumeClaim :octicons-link-external-16:](https://kubernetes.io/docs/concepts/storage/persistent-volumes/#persistentvolumeclaims) access modes for the PostgreSQL storage.

| Value type | Example |
| ---------- | ------- |
| :material-code-string: string | `ReadWriteOnce` |

### `instances.dataVolumeClaimSpec.storageClassName`

Set the [Kubernetes storage class :octicons-link-external-16:](https://kubernetes.io/docs/concepts/storage/storage-classes/) to use with PostgreSQL Cluster [PersistentVolumeClaim :octicons-link-external-16:](https://kubernetes.io/docs/concepts/storage/persistent-volumes/#persistentvolumeclaims) for the PostgreSQL storage.

| Value type | Example |
| ---------- | ------- |
| :material-code-string: string | `standard` |

### `instances.dataVolumeClaimSpec.resources.requests.storage`

The [Kubernetes storage requests :octicons-link-external-16:](https://kubernetes.io/docs/concepts/configuration/manage-compute-resources-container/#resource-requests-and-limits-of-pod-and-container) for the storage the PostgreSQL instance will use.

| Value type | Example |
| ---------- | ------- |
| :material-code-string: string | `1Gi` |

### `instances.dataVolumeClaimSpec.resources.limits.storage`

The [Kubernetes storage limits :octicons-link-external-16:](https://kubernetes.io/docs/concepts/configuration/manage-compute-resources-container/#resource-requests-and-limits-of-pod-and-container) for the storage the PostgreSQL instance will use.

| Value type | Example |
| ---------- | ------- |
| :material-code-string: string | `5Gi` |

### `instances.tablespaceVolumes.name`

Name for the custom [tablespace volume](tablespaces.md).

| Value type | Example |
| ---------- | ------- |
| :material-code-string: string | `user` |

### `instances.tablespaceVolumes.dataVolumeClaimSpec.accessModes`

The [Kubernetes PersistentVolumeClaim :octicons-link-external-16:](https://kubernetes.io/docs/concepts/storage/persistent-volumes/#persistentvolumeclaims) access modes for the tablespace volume.

| Value type | Example |
| ---------- | ------- |
| :material-code-string: string | `ReadWriteOnce` |

### `instances.tablespaceVolumes.dataVolumeClaimSpec.resources.requests.storage`

The [Kubernetes storage requests :octicons-link-external-16:](https://kubernetes.io/docs/concepts/configuration/manage-compute-resources-container/#resource-requests-and-limits-of-pod-and-container) for the tablespace volume.

| Value type | Example |
| ---------- | ------- |
| :material-code-string: string | `1Gi` |

## `instances.sidecars` subsection

The `instances.sidecars` subsection in the [deploy/cr.yaml :octicons-link-external-16:](https://github.com/percona/percona-postgresql-operator/blob/main/deploy/cr.yaml)
file contains configuration options for [custom sidecar containers](sidecar.md) which can be added to PostgreSQL Pods.

### `instances.sidecars.image`

Image for the [custom sidecar container](sidecar.md) for PostgreSQL Pods.

| Value type | Example |
| ---------- | ------- |
| :material-code-string: string | `busybox:latest` |

### `instances.sidecars.name`

Name of the [custom sidecar container](sidecar.md) for PostgreSQL Pods.

| Value type | Example |
| ---------- | ------- |
| :material-code-string: string | `testcontainer` |

### `instances.sidecars.imagePullPolicy`

This option is used to set the [policy :octicons-link-external-16:](https://kubernetes.io/docs/concepts/containers/images/#updating-images) for the PostgreSQL Pod sidecar container.

| Value type | Example |
| ---------- | ------- |
| :material-code-string: string | `Always` |

### `instances.sidecars.env`

The [environment variables set as key-value pairs :octicons-link-external-16:](https://kubernetes.io/docs/tasks/inject-data-application/define-environment-variable-container/) for the [custom sidecar container](sidecar.md) for PostgreSQL Pods.

| Value type | Example |
| ---------- | ------- |
| :material-text-long: subdoc |  |

### `instances.sidecars.envFrom`

The [environment variables set as key-value pairs in ConfigMaps :octicons-link-external-16:](https://kubernetes.io/docs/tasks/inject-data-application/define-environment-variable-container/) for the [custom sidecar container](sidecar.md) for PostgreSQL Pods.

| Value type | Example |
| ---------- | ------- |
| :material-text-long: subdoc | |

### `instances.sidecars.command`

Command for the [custom sidecar container](sidecar.md) for PostgreSQL Pods.

| Value type | Example |
| ---------- | ------- |
| :material-application-array-outline: array | `["/bin/sh"]` |

### `instances.sidecars.args`

Command arguments for the [custom sidecar container](sidecar.md) for PostgreSQL Pods.

| Value type | Example |
| ---------- | ------- |
| :material-application-array-outline: array | `["-c", "while true; do trap 'exit 0' SIGINT SIGTERM SIGQUIT SIGKILL; done;"]` |

## Backup section

The `backup` section in the
[deploy/cr.yaml :octicons-link-external-16:](https://github.com/percona/percona-postgresql-operator/blob/main/deploy/cr.yaml)
file contains the following configuration options for the regular
Percona Distribution for PostgreSQL backups.

### `backups.enabled`

Enables to turn on/off backups for the cluster. Use this option with caution. Read more in [Disable backups](backups-disable.md).

| Value type | Example |
| ---------- | ------- |
| :material-code-string: string | `true` |

### `backups.trackLatestRestorableTime`

Enables or disables [tracking the latest restorable time](backups-restore-inplace.md#restore-the-cluster-with-point-in-time-recovery) for latest successful backup (on by default). It can be turned off to reduce the S3 API usage.

| Value type | Example |
| ---------- | ------- |
| :material-toggle-switch-outline: boolean | `true` |

### `backups.pgbackrest.metadata.labels`

Set [labels :octicons-link-external-16:](https://kubernetes.io/docs/concepts/overview/working-with-objects/labels/) for pgBackRest Pods.

| Value type | Example |
| ---------- | ------- |
| :material-label-outline: label | `pg-cluster-label: cluster1` |

### `backups.pgbackrest.image`

The Docker image for [pgBackRest](backups.md#backup-repositories).

| Value type | Example |
| ---------- | ------- |
| :material-code-string: string | `docker.io/percona/percona-pgbackrest:{{pgbackrestrecommended}}` |

### `backups.pgbackrest.env.name`

Name of an environment variable for pgBackRest Pods. Read more about defining environment variables in [Kubernetes documentation :octicons-link-external-16:](https://kubernetes.io/docs/tasks/inject-data-application/define-environment-variable-container/).

| Value type | Example |
| ---------- | ------- |
| :material-code-string: string | `MY_ENV` |

### `backups.pgbackrest.env.value`

The value for an environment variable.

| Value type | Example |
| ---------- | ------- |
| :material-code-string: string | `1000` |

### `backups.pgbackrest.envFrom.secretRefName`

Name of a Secret or a ConfigMap, key/values of which are used as environment variables for pgBouncer Pods.

| Value type | Example |
| ---------- | ------- |
| :material-code-string: string | `repo-host-env-secret` |

### `backups.pgbackrest.containers.pgbackrest.resources.requests.cpu`

[Kubernetes CPU requests :octicons-link-external-16:](https://kubernetes.io/docs/concepts/configuration/manage-compute-resources-container/#resource-requests-and-limits-of-pod-and-container) for a `pgBackRest` container. It must not exceed the limit.

If you specify a limit and don't specify a request, Kubernetes uses the specified limit as the requested value for a resource.

| Value type | Example |
| ---------- | ------- |
| :material-code-string: string | `150m` |

### `backups.pgbackrest.containers.pgbackrest.resources.requests.memory`

[Kubernetes memory requests :octicons-link-external-16:](https://kubernetes.io/docs/concepts/configuration/manage-compute-resources-container/#resource-requests-and-limits-of-pod-and-container) for a `pgBackRest` container. It must not exceed the limit.

If you specify a limit and don't specify a request, Kubernetes uses the specified limit as the requested value for a resource.

| Value type | Example |
| ---------- | ------- |
| :material-code-string: string | `120Mi` |


### `backups.pgbackrest.containers.pgbackrest.resources.limits.cpu`

[Kubernetes CPU limits :octicons-link-external-16:](https://kubernetes.io/docs/concepts/configuration/manage-compute-resources-container/#resource-requests-and-limits-of-pod-and-container) for a pgBackRest container.

| Value type | Example |
| ---------- | ------- |
| :material-code-string: string | `1.0` |

### `backups.pgbackrest.containers.pgbackrest.resources.limits.memory`

The [Kubernetes memory limits :octicons-link-external-16:](https://kubernetes.io/docs/concepts/configuration/manage-compute-resources-container/#resource-requests-and-limits-of-pod-and-container) for a pgBackRest container.

| Value type | Example |
| ---------- | ------- |
| :material-code-string: string | `1Gi` |


### `backups.pgbackrest.containers.pgbackrestConfig.resources.limits.cpu`

[Kubernetes CPU limits :octicons-link-external-16:](https://kubernetes.io/docs/concepts/configuration/manage-compute-resources-container/#resource-requests-and-limits-of-pod-and-container) for `pgbackrest-config` sidecar container.

| Value type | Example |
| ---------- | ------- |
| :material-code-string: string | `1.0` |

### `backups.pgbackrest.containers.pgbackrestConfig.resources.limits.memory`

The [Kubernetes memory limits :octicons-link-external-16:](https://kubernetes.io/docs/concepts/configuration/manage-compute-resources-container/#resource-requests-and-limits-of-pod-and-container) for `pgbackrest-config` sidecar container.

| Value type | Example |
| ---------- | ------- |
| :material-code-string: string | `1Gi` |

### `backups.pgbackrest.containers.pgbackrestConfig.resources.requests.cpu`

[Kubernetes CPU requests :octicons-link-external-16:](https://kubernetes.io/docs/concepts/configuration/manage-compute-resources-container/#resource-requests-and-limits-of-pod-and-container) for a `pgbackrest-config` sidecar container. It must not exceed the limit.

If you specify a limit and don't specify a request, Kubernetes uses the specified limit as the requested value for a resource.

| Value type | Example |
| ---------- | ------- |
| :material-code-string: string | `150m` |

### `backups.pgbackrest.containers.pgbackrestConfig.resources.requests.memory`

[Kubernetes memory requests :octicons-link-external-16:](https://kubernetes.io/docs/concepts/configuration/manage-compute-resources-container/#resource-requests-and-limits-of-pod-and-container) for a `pgbackrest-config` sidecar container. It must not exceed the limit.

If you specify a limit and don't specify a request, Kubernetes uses the specified limit as the requested value for a resource.

| Value type | Example |
| ---------- | ------- |
| :material-code-string: string | `120Mi` |

### `backups.pgbackrest.configuration.secret.name`

Name of the [Kubernetes Secret object :octicons-link-external-16:](https://kubernetes.io/docs/concepts/configuration/secret/#using-imagepullsecrets) with custom pgBackRest configuration, which will be added to the pgBackRest configuration generated by the Operator.

| Value type | Example |
| ---------- | ------- |
| :material-code-string: string | `cluster1-pgbackrest-secrets` |

### `backups.pgbackrest.jobs.backoffLimit`

The number of retries to make a backup with incremental pauses of 10 seconds, 20 seconds, etc. between retries. By default it's `0`, which means that pgBackRest job Pod fails after first unsuccessful attempt (causing creation of a new Pod on failure).

| Value type  | Example    |
| ----------- | ---------- |
| :material-numeric-1-box: int     | `2` |

### `backups.pgbackrest.jobs.restartPolicy`

The [Kubernetes Pod restart policy :octicons-link-external-16:](https://kubernetes.io/docs/concepts/workloads/pods/pod-lifecycle/#restart-policy) for pgBackRest jobs.

| Value type | Example |
| ---------- | ------- |
| :material-code-string: string | `OnFailure` |

### `backups.pgbackrest.jobs.priorityClassName`

The [Kubernetes Pod priority class :octicons-link-external-16:](https://kubernetes.io/docs/concepts/configuration/pod-priority-preemption/#priorityclass) for pgBackRest jobs.

| Value type | Example |
| ---------- | ------- |
| :material-code-string: string | `high-priority` |

### `backups.pgbackrest.jobs.resources.limits.cpu`

[Kubernetes CPU limits :octicons-link-external-16:](https://kubernetes.io/docs/concepts/configuration/manage-compute-resources-container/#resource-requests-and-limits-of-pod-and-container) for a pgBackRest job.

| Value type | Example |
| ---------- | ------- |
| :material-numeric-1-box: int | `200` |

### `backups.pgbackrest.jobs.resources.limits.memory`

The [Kubernetes memory limits :octicons-link-external-16:](https://kubernetes.io/docs/concepts/configuration/manage-compute-resources-container/#resource-requests-and-limits-of-pod-and-container) for a pgBackRest job.

| Value type | Example |
| ---------- | ------- |
| :material-code-string: string | `128Mi` |

### `backups.pgbackrest.jobs.resources.requests.cpu`

[Kubernetes CPU requests :octicons-link-external-16:](https://kubernetes.io/docs/concepts/configuration/manage-compute-resources-container/#resource-requests-and-limits-of-pod-and-container) for a pgBackRest job. It must not exceed the limit.

If you specify a limit and don't specify a request, Kubernetes uses the specified limit as the requested value for a resource.

|Value type | Example |
| ---------- | ------- |
| :material-code-string: string | `150m` |

### `backups.pgbackrest.jobs.resources.requests.memory`

[Kubernetes memory requests :octicons-link-external-16:](https://kubernetes.io/docs/concepts/configuration/manage-compute-resources-container/#resource-requests-and-limits-of-pod-and-container) for pgBackRest job. It must not exceed the limit.

If you specify a limit and don't specify a request, Kubernetes uses the specified limit as the requested value for a resource.

| Value type | Example |
| ---------- | ------- |
| :material-code-string: string | `120Mi` |

### `backups.pgbackrest.jobs.tolerations.effect`

The [Kubernetes Pod tolerations :octicons-link-external-16:](https://kubernetes.io/docs/concepts/configuration/taint-and-toleration/#concepts) effect for a backup job.

| Value type | Example |
| ---------- | ------- |
| :material-code-string: string | `NoSchedule` |

### `backups.pgbackrest.jobs.tolerations.key`

The [Kubernetes Pod tolerations :octicons-link-external-16:](https://kubernetes.io/docs/concepts/configuration/taint-and-toleration/#concepts) key for a backup job.

| Value type | Example |
| ---------- | ------- |
| :material-code-string: string | `role` |

### `backups.pgbackrest.jobs.tolerations.operator`

The [Kubernetes Pod tolerations :octicons-link-external-16:](https://kubernetes.io/docs/concepts/configuration/taint-and-toleration/#concepts) operator for a backup job.

| Value type | Example |
| ---------- | ------- |
| :material-code-string: string | `Equal` |

### `backups.pgbackrest.jobs.tolerations.value`

The [Kubernetes Pod tolerations :octicons-link-external-16:](https://kubernetes.io/docs/concepts/configuration/taint-and-toleration/#concepts) value for a backup job.

| Value type | Example |
| ---------- | ------- |
| :material-code-string: string | `connection-poolers` |

### `backups.pgbackrest.jobs.securityContext`

A custom [Kubernetes Security Context for a Pod :octicons-link-external-16:](https://kubernetes.io/docs/tasks/configure-pod-container/security-context/) to be used instead of the default one.

| Value type  | Example    |
| ----------- | ---------- |
| :material-text-long: subdoc      | <pre>fsGroup: 1001<br>runAsUser: 1001<br>runAsNonRoot: true<br>fsGroupChangePolicy: "OnRootMismatch"<br>runAsGroup: 1001<br>seLinuxOptions:<br>  type: spc_t<br>  level: s0:c123,c456<br>seccompProfile:<br>  type: Localhost<br>  localhostProfile: localhost/profile.json<br>supplementalGroups:<br>- 1001<br>sysctls:<br>- name: net.ipv4.tcp_keepalive_time<br>  value: "600"<br>- name: net.ipv4.tcp_keepalive_intvl<br>  value: "60"</pre> |

### `backups.pgbackrest.global`

Settings, which are to be included in the `global` section of the pgBackRest configuration generated by the Operator.

| Value type | Example |
| ---------- | ------- |
| :material-text-long: subdoc | <pre>repo1-retention-full: "14"<br>repo1-retention-full-type: time<br>repo1-path: /pgbackrest/postgres-operator/cluster1/repo1<br>repo1-cipher-type: aes-256-cbc<br>repo1-s3-uri-style: path<br>repo2-path: /pgbackrest/postgres-operator/cluster1-multi-repo/repo2<br>repo3-path: /pgbackrest/postgres-operator/cluster1-multi-repo/repo3<br>repo4-path: /pgbackrest/postgres-operator/cluster1-multi-repo/repo4</pre> |

### `backups.pgbackrest.repoHost.sidecars.name`

The name of a [custom sidecar container](sidecar.md) for pgBackRest Pods.

| Value type | Example |
| ---------- | ------- |
| :material-code-string: string | `testcontainer` |

### `backups.pgbackrest.repoHost.sidecars.image`

The image used to deploy a [custom sidecar container](sidecar.md) for pgBackRest Pods.

| Value type | Example |
| ---------- | ------- |
| :material-code-string: string | `busybox:latest` |

### `backups.pgbackrest.repoHost.sidecars.command`

The command to use inside a custom sidecar container for pgBackRest Pods

| Value type | Example |
| ---------- | ------- |
| :material-code-string: string | `["sleep", "30d"]` |

### `backups.pgbackrest.repoHost.sidecars.securityContext`

Security settings for the sifecar container. These settings control privileges, user/group IDs, and other security-related options. For more details, see the [Kubernetes documentation on SecurityContext :octicons-link-external-16:](https://kubernetes.io/docs/tasks/configure-pod-container/security-context/)

| Value type | Example |
| ---------- | ------- |
| :material-code-string: string | `{}` |

### `backups.pgbackrest.repoHost.resources.requests.cpu`

[Kubernetes CPU requests :octicons-link-external-16:](https://kubernetes.io/docs/concepts/configuration/manage-compute-resources-container/#resource-requests-and-limits-of-pod-and-container) for a pgBackRest repo. It must not exceed the limit.

If you specify a limit and don't specify a request, Kubernetes uses the specified limit as the requested value for a resource.

|Value type | Example |
| ---------- | ------- |
| :material-code-string: string | `150m` |

### `backups.pgbackrest.repoHost.resources.requests.memory`

[Kubernetes memory requests :octicons-link-external-16:](https://kubernetes.io/docs/concepts/configuration/manage-compute-resources-container/#resource-requests-and-limits-of-pod-and-container) for pgBackRest repo. It must not exceed the limit.

If you specify a limit and don't specify a request, Kubernetes uses the specified limit as the requested value for a resource.

| Value type | Example |
| ---------- | ------- |
| :material-code-string: string | `120Mi` |

### `backups.pgbackrest.repoHost.resources.limits.cpu`

[Kubernetes CPU limits :octicons-link-external-16:](https://kubernetes.io/docs/concepts/configuration/manage-compute-resources-container/#resource-requests-and-limits-of-pod-and-container) for a pgBackRest repo.

| Value type | Example |
| ---------- | ------- |
| :material-numeric-1-box: int | `200` |

### `backups.pgbackrest.repoHost.resources.limits.memory`

The [Kubernetes memory limits :octicons-link-external-16:](https://kubernetes.io/docs/concepts/configuration/manage-compute-resources-container/#resource-requests-and-limits-of-pod-and-container) for a pgBackRest repo.

| Value type | Example |
| ---------- | ------- |
| :material-code-string: string | `128Mi` |


### `backups.pgbackrest.repoHost.priorityClassName`

The [Kubernetes Pod priority class :octicons-link-external-16:](https://kubernetes.io/docs/concepts/configuration/pod-priority-preemption/#priorityclass) for pgBackRest repo.

| Value type | Example |
| ---------- | ------- |
| :material-code-string: string | `high-priority` |

### `backups.pgbackrest.repoHost.topologySpreadConstraints.maxSkew`

The degree to which Pods may be unevenly distributed under the [Kubernetes Pod Topology Spread Constraints :octicons-link-external-16:](https://kubernetes.io/docs/concepts/scheduling-eviction/topology-spread-constraints/).

| Value type | Example |
| ---------- | ------- |
| :material-numeric-1-box: int | `1` |

### `backups.pgbackrest.repoHost.topologySpreadConstraints.topologyKey`

The key of node labels for the [Kubernetes Pod Topology Spread Constraints :octicons-link-external-16:](https://kubernetes.io/docs/concepts/scheduling-eviction/topology-spread-constraints/).

| Value type | Example |
| ---------- | ------- |
| :material-code-string: string | `my-node-label` |

### `backups.pgbackrest.repoHost.topologySpreadConstraints.whenUnsatisfiable`

What to do with a Pod if it doesn't satisfy the [Kubernetes Pod Topology Spread Constraints :octicons-link-external-16:](https://kubernetes.io/docs/concepts/scheduling-eviction/topology-spread-constraints/).

| Value type | Example |
| ---------- | ------- |
| :material-code-string: string | `ScheduleAnyway` |

### `backups.pgbackrest.repoHost.topologySpreadConstraints.labelSelector.matchLabels`

The Label selector for the [Kubernetes Pod Topology Spread Constraints :octicons-link-external-16:](https://kubernetes.io/docs/concepts/scheduling-eviction/topology-spread-constraints/).

| Value type | Example |
| ---------- | ------- |
| :material-label-outline: label | `postgres-operator.crunchydata.com/pgbackrest: ""` |

### `backups.pgbackrest.repoHost.affinity.podAntiAffinity`

[Pod anti-affinity](constraints.md#affinity-and-anti-affinity), allows setting the standard Kubernetes affinity constraints of any complexity.

| Value type | Example |
| ---------- | ------- |
| :material-text-long: subdoc | |

### `backups.pgbackrest.repoHost.tolerations.effect`

The [Kubernetes Pod tolerations :octicons-link-external-16:](https://kubernetes.io/docs/concepts/configuration/taint-and-toleration/#concepts) effect for pgBackRest repo.

| Value type | Example |
| ---------- | ------- |
| :material-code-string: string | `NoSchedule` |

### `backups.pgbackrest.repoHost.tolerations.key`

The [Kubernetes Pod tolerations :octicons-link-external-16:](https://kubernetes.io/docs/concepts/configuration/taint-and-toleration/#concepts) key for pgBackRest repo.

| Value type | Example |
| ---------- | ------- |
| :material-code-string: string | `role` |

### `backups.pgbackrest.repoHost.tolerations.operator`

The [Kubernetes Pod tolerations :octicons-link-external-16:](https://kubernetes.io/docs/concepts/configuration/taint-and-toleration/#concepts) operator for pgBackRest repo.

| Value type | Example |
| ---------- | ------- |
| :material-code-string: string | `Equal` |

### `backups.pgbackrest.repoHost.tolerations.value`

The [Kubernetes Pod tolerations :octicons-link-external-16:](https://kubernetes.io/docs/concepts/configuration/taint-and-toleration/#concepts) value for pgBackRest repo.

| Value type | Example |
| ---------- | ------- |
| :material-code-string: string | `connection-poolers` |


### 'backups.pgbackrest.repoHost.securityContext'

A custom [Kubernetes Security Context for a Pod :octicons-link-external-16:](https://kubernetes.io/docs/tasks/configure-pod-container/security-context/) to be used instead of the default one.

| Value type  | Example    |
| ----------- | ---------- |
| :material-text-long: subdoc      | <pre>fsGroup: 1001<br>runAsUser: 1001<br>runAsNonRoot: true<br>fsGroupChangePolicy: "OnRootMismatch"<br>runAsGroup: 1001<br>seLinuxOptions:<br>  type: spc_t<br>  level: s0:c123,c456<br>seccompProfile:<br>  type: Localhost<br>  localhostProfile: localhost/profile.json<br>supplementalGroups:<br>- 1001<br>sysctls:<br>- name: net.ipv4.tcp_keepalive_time<br>  value: "600"<br>- name: net.ipv4.tcp_keepalive_intvl<br>  value: "60"</pre> |

### `backups.pgbackrest.manual.repoName`

Name of the pgBackRest repository for on-demand backups.

| Value type | Example |
| ---------- | ------- |
| :material-code-string: string | `repo1` |

### `backups.pgbackrest.manual.options`

The on-demand backup command-line options which will be passed to pgBackRest for on-demand backups.

| Value type | Example |
| ---------- | ------- |
| :material-code-string: string | `--type=full` |

### `backups.pgbackrest.manual.initialDelaySeconds`

The time to delay a backup start after the backup Pod is scheduled. The backup process wait for the defined time before it connectsto the API server to start a backup.

| Value type | Example |
| ---------- | ------- |
| :material-numeric-1-box: int | `120` | 

### `backups.pgbackrest.repos.name`

Name of the pgBackRest repository for backups.

| Value type | Example |
| ---------- | ------- |
| :material-code-string: string | `repo1` |

### `backups.pgbackrest.repos.schedules.full`

Scheduled time to make a full backup specified in the [crontab format :octicons-link-external-16:](https://en.wikipedia.org/wiki/Cron).

| Value type | Example |
| ---------- | ------- |
| :material-code-string: string | `0 0 \* \* 6` |

### `backups.pgbackrest.repos.schedules.differential`

Scheduled time to make a differential backup specified in the [crontab format :octicons-link-external-16:](https://en.wikipedia.org/wiki/Cron).

| Value type | Example |
| ---------- | ------- |
| :material-code-string: string | `0 0 \* \* 6` |

### `backups.pgbackrest.repos.volume.volumeClaimSpec.accessModes`

The [Kubernetes PersistentVolumeClaim :octicons-link-external-16:](https://kubernetes.io/docs/concepts/storage/persistent-volumes/#persistentvolumeclaims) access modes for the pgBackRest Storage.

| Value type | Example |
| ---------- | ------- |
| :material-code-string: string | `ReadWriteOnce` |


### `backups.pgbackrest.repos.volume.volumeClaimSpec.storageClassName`

Set the [Kubernetes Storage Class :octicons-link-external-16:](https://kubernetes.io/docs/concepts/storage/storage-classes/) to use with the Percona Operator for PostgreSQL backups stored on [Persistent Volume](backups-storage.md#__tabbed_1_4).

| Value type | Example |
| ---------- | ------- |
| :material-code-string: string | `standard` |

### `backups.pgbackrest.repos.volume.volumeClaimSpec.resources.requests.storage`

The [Kubernetes storage requests :octicons-link-external-16:](https://kubernetes.io/docs/concepts/configuration/manage-compute-resources-container/#resource-requests-and-limits-of-pod-and-container) for the pgBackRest storage.

| Value type | Example |
| ---------- | ------- |
| :material-code-string: string | `1Gi` |

### `backups.pgbackrest.repos.s3.bucket`

The [Amazon S3 bucket :octicons-link-external-16:](https://docs.aws.amazon.com/AmazonS3/latest/dev/UsingBucket.html) 
name used for backups

| Value type | Example |
| ---------- | ------- |
| :material-code-string: string | `"my-bucket"` |
.

### `backups.pgbackrest.repos.s3.endpoint`

The endpoint URL of the S3-compatible storage to be used for backups (not needed for the original Amazon S3 cloud).

| Value type | Example |
| ---------- | ------- |
| :material-code-string: string | `"s3.ca-central-1.amazonaws.com"` |

### `backups.pgbackrest.repos.s3.region`

The [AWS region :octicons-link-external-16:](https://docs.aws.amazon.com/general/latest/gr/rande.html) to use for Amazon and all S3-compatible storages.

| Value type | Example |
| ---------- | ------- |
| :material-code-string: string | `"ca-central-1"` |

### `backups.pgbackrest.repos.gcs.bucket`

The [Google Cloud Storage bucket :octicons-link-external-16:](https://cloud.google.com/storage/docs/key-terms#buckets)
name used for backups.

| Value type | Example |
| ---------- | ------- |
| :material-code-string: string | `"my-bucket"` |

### `backups.pgbackrest.repos.azure.container`

Name of the [Azure Blob Storage container :octicons-link-external-16:](https://docs.microsoft.com/en-us/azure/storage/blobs/storage-blobs-introduction#containers) for backups.

| Value type | Example |
| ---------- | ------- |
| :material-code-string: string | `my-container` |

### `backups.restore.tolerations.effect`

The [Kubernetes Pod tolerations :octicons-link-external-16:](https://kubernetes.io/docs/concepts/configuration/taint-and-toleration/#concepts) effect for the backup restore job.

| Value type | Example |
| ---------- | ------- |
| :material-code-string: string | `NoSchedule` |

### `backups.restore.tolerations.key`

The [Kubernetes Pod tolerations :octicons-link-external-16:](https://kubernetes.io/docs/concepts/configuration/taint-and-toleration/#concepts) key for the backup restore job.

| Value type | Example |
| ---------- | ------- |
| :material-code-string: string | `role` |

### `backups.restore.tolerations.operator`

The [Kubernetes Pod tolerations :octicons-link-external-16:](https://kubernetes.io/docs/concepts/configuration/taint-and-toleration/#concepts) operator for the backup restore job.

| Value type | Example |
| ---------- | ------- |
| :material-code-string: string | `Equal` |

### `backups.restore.tolerations.value`

The [Kubernetes Pod tolerations :octicons-link-external-16:](https://kubernetes.io/docs/concepts/configuration/taint-and-toleration/#concepts) value for the backup restore job.

| Value type | Example |
| ---------- | ------- |
| :material-code-string: string | `connection-poolers` |

## PMM section

The `pmm` section in the [deploy/cr.yaml :octicons-link-external-16:](https://github.com/percona/percona-postgresql-operator/blob/main/deploy/cr.yaml)
file contains configuration options for Percona Monitoring and Management.

### `pmm.enabled`

Enables or disables [monitoring Percona Distribution for PostgreSQL cluster with PMM :octicons-link-external-16:](https://docs.percona.com/percona-monitoring-and-management/2/setting-up/client/postgresql.html).

| Value type | Example |
| ---------- | ------- |
| :material-toggle-switch-outline: boolean | `false` |

### `pmm.image`

[Percona Monitoring and Management (PMM) Client :octicons-link-external-16:](https://docs.percona.com/percona-monitoring-and-management/2/details/architecture.html#pmm-client) Docker image.

| Value type | Example |
| ---------- | ------- |
| :material-code-string: string | `percona/pmm-client:{{ pmm3recommended }}` |

### `pmm.imagePullPolicy`

This option is used to set the [policy :octicons-link-external-16:](https://kubernetes.io/docs/concepts/containers/images/#updating-images) for updating PMM Client images.

| Value type | Example |
| ---------- | ------- |
| :material-code-string: string | `IfNotPresent` |

### `pmm.secret`

Name of the [Kubernetes Secret object :octicons-link-external-16:](https://kubernetes.io/docs/concepts/configuration/secret/#using-imagepullsecrets) for the PMM Server password.

| Value type | Example |
| ---------- | ------- |
| :material-code-string: string | `cluster1-pmm-secret` |

### `pmm.serverHost`

Address of the PMM Server to collect data from the cluster.

| Value type | Example |
| ---------- | ------- |
| :material-code-string: string | `monitoring-service` |

### pmm.customClusterName

A custom name to define for a cluster. PMM Server uses this name to properly parse the metrics and display them on dashboards. Using a custom name is useful for clusters deployed in different data centers - PMM Server connects them and monitors them as one deployment. Another use case is for clusters deployed with the same name in different namespaces - PMM treats each cluster separately.

| Value type  | Example    |
| ----------- | ---------- |
| :material-code-string: string     | `postgresql-cluster` |

### `pmm.resources.requests.cpu`

[Kubernetes CPU requests :octicons-link-external-16:](https://kubernetes.io/docs/concepts/configuration/manage-compute-resources-container/#resource-requests-and-limits-of-pod-and-container) for a PMM Client container. It must not exceed the limit.

If you specify a limit and don't specify a request, Kubernetes uses the specified limit as the requested value for a resource.

|Value type | Example |
| ---------- | ------- |
| :material-code-string: string | `150m` |

### `pmm.resources.requests.memory`

[Kubernetes memory requests :octicons-link-external-16:](https://kubernetes.io/docs/concepts/configuration/manage-compute-resources-container/#resource-requests-and-limits-of-pod-and-container) for PMM Client container. It must not exceed the limit.

If you specify a limit and don't specify a request, Kubernetes uses the specified limit as the requested value for a resource.

| Value type | Example |
| ---------- | ------- |
| :material-code-string: string | `120Mi` |

### `pmm.resources.limits.cpu`

[Kubernetes CPU limits :octicons-link-external-16:](https://kubernetes.io/docs/concepts/configuration/manage-compute-resources-container/#resource-requests-and-limits-of-pod-and-container) for a PMM Client container.

| Value type | Example |
| ---------- | ------- |
| :material-numeric-1-box: int | `200` |

### `pmm.resources.limits.memory`

The [Kubernetes memory limits :octicons-link-external-16:](https://kubernetes.io/docs/concepts/configuration/manage-compute-resources-container/#resource-requests-and-limits-of-pod-and-container) for a PMM Client container.

| Value type | Example |
| ---------- | ------- |
| :material-code-string: string | `128Mi` |

### `pmm.querySource`

Query source to track PostgreSQL statistics. Either pg_stat_monitor (`pgstatmonitor`, the default value) or pg_stat_statements (`pgstatstatements`) can be used.

| Value type | Example |
| ---------- | ------- |
| :material-code-string: string | `pgstatmonitor` |

### `pmm.postgresParams`

Additional parameters which will be passed to the `pmm-admin add postgresql` command for PostgreSQL Pods.

| Value type | Example |
| ---------- | ------- |
| :material-code-string: string |  |

## Proxy section

The `proxy` section in the [deploy/cr.yaml :octicons-link-external-16:](https://github.com/percona/percona-postgresql-operator/blob/main/deploy/cr.yaml)
file contains configuration options for the [pgBouncer :octicons-link-external-16:](http://pgbouncer.github.io/) connection pooler for PostgreSQL.

### `proxy.pgBouncer.metadata.labels`

Set [labels :octicons-link-external-16:](https://kubernetes.io/docs/concepts/overview/working-with-objects/labels/) for pgBouncer Pods.

| Value type | Example |
| ---------- | ------- |
| :material-label-outline: label | `pg-cluster-label: cluster1` |

### `proxy.pgBouncer.replicas`

The number of the pgBouncer Pods to provide connection pooling.

| Value type | Example |
| ---------- | ------- |
| :material-numeric-1-box: int | `3` |

### `proxy.pgBouncer.image`

Docker image for the [pgBouncer :octicons-link-external-16:](http://pgbouncer.github.io/) connection pooler.

| Value type | Example |
| ---------- | ------- |
| :material-code-string: string | `docker.io/percona/percona-pgbouncer:{{pgbouncerrecommended}}` |

### `proxy.pgBouncer.env.name`

Name of an environment variable for pgBouncer Pods. Read more about defining environment variables in [Kubernetes documentation :octicons-link-external-16:](https://kubernetes.io/docs/tasks/inject-data-application/define-environment-variable-container/).

| Value type | Example |
| ---------- | ------- |
| :material-code-string: string | `MY_ENV` |

### `proxy.pgBouncer.env.value`

The value for an environment variable.

| Value type | Example |
| ---------- | ------- |
| :material-code-string: string | `1000` |

### `proxy.pgBouncer.envFrom.secretRefName`

Name of a Secret or a ConfigMap, key/values of which are used as environment variables for pgBouncer Pods.

| Value type | Example |
| ---------- | ------- |
| :material-code-string: string | `pgbouncer-env-secret` |

### `proxy.pgBouncer.exposeSuperusers`

Enables or disables [exposing superuser user through pgBouncer](users.md#superuser-and-pgbouncer).

| Value type | Example |
| ---------- | ------- |
| :material-toggle-switch-outline: boolean | `false` |

### `proxy.pgBouncer.resources.requests.cpu`

[Kubernetes CPU requests :octicons-link-external-16:](https://kubernetes.io/docs/concepts/configuration/manage-compute-resources-container/#resource-requests-and-limits-of-pod-and-container) for a pgBouncer container. It must not exceed the limit.

If you specify a limit and don't specify a request, Kubernetes uses the specified limit as the requested value for a resource.

| Value type | Example |
| ---------- | ------- |
| :material-code-string: string | `150m` |

### `proxy.pgBouncer.resources.requests.memory`

[Kubernetes memory requests :octicons-link-external-16:](https://kubernetes.io/docs/concepts/configuration/manage-compute-resources-container/#resource-requests-and-limits-of-pod-and-container) for a pgBouncer container. It must not exceed the limit.

If you specify a limit and don't specify a request, Kubernetes uses the specified limit as the requested value for a resource.

 Value type | Example |
| ---------- | ------- |
| :material-code-string: string | `120Mi` |

### `proxy.pgBouncer.resources.limits.cpu`

[Kubernetes CPU limits :octicons-link-external-16:](https://kubernetes.io/docs/concepts/configuration/manage-compute-resources-container/#resource-requests-and-limits-of-pod-and-container) for a pgBouncer container.

| Value type | Example |
| ---------- | ------- |
| :material-code-string: string | `200m` |

### `proxy.pgBouncer.resources.limits.memory`

The [Kubernetes memory limits :octicons-link-external-16:](https://kubernetes.io/docs/concepts/configuration/manage-compute-resources-container/#resource-requests-and-limits-of-pod-and-container) for a pgBouncer container.

| Value type | Example |
| ---------- | ------- |
| :material-code-string: string | `128Mi` |

### `proxy.pgBouncer.containers.pgbouncerConfig.resources.limits.cpu`

[Kubernetes CPU limits :octicons-link-external-16:](https://kubernetes.io/docs/concepts/configuration/manage-compute-resources-container/#resource-requests-and-limits-of-pod-and-container) for `pgbouncer-config` sidecar container.

| Value type | Example |
| ---------- | ------- |
| :material-code-string: string | `1.0` |

### `proxy.pgBouncer.containers.pgbouncerConfig.resources.limits.memory`

The [Kubernetes memory limits :octicons-link-external-16:](https://kubernetes.io/docs/concepts/configuration/manage-compute-resources-container/#resource-requests-and-limits-of-pod-and-container) for `pgbouncer-config` sidecar container.

| Value type | Example |
| ---------- | ------- |
| :material-code-string: string | `1Gi` |

### `proxy.pgBouncer.containers.pgbouncerConfig.resources.requests.cpu`

[Kubernetes CPU requests :octicons-link-external-16:](https://kubernetes.io/docs/concepts/configuration/manage-compute-resources-container/#resource-requests-and-limits-of-pod-and-container) for a `pgbouncer-config` sidecar container. It must not exceed the limit.

If you specify a limit and don't specify a request, Kubernetes uses the specified limit as the requested value for a resource.

 Value type | Example |
| ---------- | ------- |
| :material-code-string: string | `150m` |

### `proxy.pgBouncer.containers.pgbouncerConfig.resources.requests.memory`

[Kubernetes memory requests :octicons-link-external-16:](https://kubernetes.io/docs/concepts/configuration/manage-compute-resources-container/#resource-requests-and-limits-of-pod-and-container) for a `pgbouncer-config` sidecar container. It must not exceed the limit.

If you specify a limit and don't specify a request, Kubernetes uses the specified limit as the requested value for a resource.

 Value type | Example |
| ---------- | ------- |
| :material-code-string: string | `120Mi` |

### `proxy.pgBouncer.expose.type`

Specifies the type of [Kubernetes Service :octicons-link-external-16:](https://kubernetes.io/docs/concepts/services-networking/service/#publishing-services-service-types) for pgBouncer.

| Value type | Example |
| ---------- | ------- |
| :material-code-string: string | `ClusterIP` |

### `proxy.pgBouncer.expose.annotations`

The [Kubernetes annotations :octicons-link-external-16:](https://kubernetes.io/docs/concepts/overview/working-with-objects/annotations/) metadata for pgBouncer.

| Value type | Example |
| ---------- | ------- |
| :material-label-outline: label | `my-annotation: value1` |

### `proxy.pgBouncer.expose.labels`

Set [labels :octicons-link-external-16:](https://kubernetes.io/docs/concepts/overview/working-with-objects/labels/) for the pgBouncer Service.

| Value type | Example |
| ---------- | ------- |
| :material-label-outline: label | `pg-cluster-label: cluster1` |

### `proxy.pgBouncer.expose.loadBalancerClass`

Define the implementation of the load balancer you want to use. This setting enables you to select a custom or specific load balancer class instead of the default one provided by the cloud provider.

| Value type  | Example    |
| ----------- | ---------- |
| :material-code-string: string     | `eks.amazonaws.com/nlb`|

### `proxy.pgBouncer.expose.loadBalancerSourceRanges`

The range of client IP addresses from which the load balancer should be reachable (if not set, there is no limitations).

| Value type | Example |
| ---------- | ------- |
| :material-code-string: string | `"10.0.0.0/8"` |

### `proxy.pgBouncer.affinity.podAntiAffinity`

[Pod anti-affinity](constraints.md#affinity-and-anti-affinity), allows setting the standard Kubernetes affinity constraints of any complexity.

| Value type | Example |
| ---------- | ------- |
| :material-text-long: subdoc | |

### 'proxy.pgBouncer.securityContext'

A custom [Kubernetes Security Context for a Pod :octicons-link-external-16:](https://kubernetes.io/docs/tasks/configure-pod-container/security-context/) to be used instead of the default one.

| Value type  | Example    |
| ----------- | ---------- |
| :material-text-long: subdoc      | <pre>fsGroup: 1001<br>runAsUser: 1001<br>runAsNonRoot: true<br>fsGroupChangePolicy: "OnRootMismatch"<br>runAsGroup: 1001<br>seLinuxOptions:<br>  type: spc_t<br>  level: s0:c123,c456<br>seccompProfile:<br>  type: Localhost<br>  localhostProfile: localhost/profile.json<br>supplementalGroups:<br>- 1001<br>sysctls:<br>- name: net.ipv4.tcp_keepalive_time<br>  value: "600"<br>- name: net.ipv4.tcp_keepalive_intvl<br>  value: "60"</pre> |

### `proxy.pgBouncer.config`

Custom configuration options for pgBouncer. Please note that configuration changes are automatically applied to the running instances without validation, so having an invalid config can make the cluster unavailable.

| Value type | Example |
| ---------- | ------- |
| :material-text-long: subdoc | <pre>global:<br>pool_mode: transaction</pre> |

## proxy.pgBouncer.sidecars subsection

The `proxy.pgBouncer.sidecars` subsection in the [deploy/cr.yaml :octicons-link-external-16:](https://github.com/percona/percona-postgresql-operator/blob/main/deploy/cr.yaml)
file contains configuration options for [custom sidecar containers](sidecar.md) which can be added to pgBouncer Pods.

### `proxy.pgBouncer.sidecars.image`

Image for the [custom sidecar container](sidecar.md) for pgBouncer Pods.

| Value type | Example |
| ---------- | ------- |
| :material-code-string: string | `mycontainer1:latest` |

### `proxy.pgBouncer.sidecars.name`

Name of the [custom sidecar container](sidecar.md) for pgBouncer Pods.

| Value type | Example |
| ---------- | ------- |
| :material-code-string: string | `testcontainer` |

### `proxy.pgBouncer.sidecars.imagePullPolicy`

This option is used to set the [policy :octicons-link-external-16:](https://kubernetes.io/docs/concepts/containers/images/#updating-images) for the pgBouncer Pod sidecar container.

| Value type | Example |
| ---------- | ------- |
| :material-code-string: string | `Always` |

### `proxy.pgBouncer.sidecars.env`

The [environment variables set as key-value pairs :octicons-link-external-16:](https://kubernetes.io/docs/tasks/inject-data-application/define-environment-variable-container/) for the [custom sidecar container](sidecar.md) for pgBouncer Pods.

| Value type | Example |
| ---------- | ------- |
| :material-text-long: subdoc |  |

### `proxy.pgBouncer.sidecars.envFrom`

The [environment variables set as key-value pairs in ConfigMaps :octicons-link-external-16:](https://kubernetes.io/docs/tasks/inject-data-application/define-environment-variable-container/) for the [custom sidecar container](sidecar.md) for pgBouncer Pods.

| Value type | Example |
| ---------- | ------- |
| :material-text-long: subdoc | |

### `proxy.pgBouncer.sidecars.command`

Command for the [custom sidecar container](sidecar.md) for pgBouncer Pods.

| Value type | Example |
| ---------- | ------- |
| :material-application-array-outline: array | `["/bin/sh"]` |

### `proxy.pgBouncer.sidecars.args`

Command arguments for the [custom sidecar container](sidecar.md) for pgBouncer Pods.

| Value type | Example |
| ---------- | ------- |
| :material-application-array-outline: array | `["-c", "while true; do trap 'exit 0' SIGINT SIGTERM SIGQUIT SIGKILL; done;"]` |

## Patroni Section

The `patroni` section in the [deploy/cr.yaml :octicons-link-external-16:](https://github.com/percona/percona-postgresql-operator/blob/main/deploy/cr.yaml)
file contains configuration options to customize the PostgreSQL high-availability implementation based on [Patroni :octicons-link-external-16:](https://patroni.readthedocs.io/).

| Value type | Example |
| ---------- | ------- |
| :material-numeric-1-box: int | `3` |

### `patroni.syncPeriodSeconds`

How often to perform [liveness/readiness probes  :octicons-link-external-16:](https://kubernetes.io/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes/#configure-probes) for the patroni container (in seconds).

| Value type | Example |
| ---------- | ------- |
| :material-numeric-1-box: int | `3` |

### `patroni.leaderLeaseDurationSeconds`

Initial delay for [liveness/readiness probes  :octicons-link-external-16:](https://kubernetes.io/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes/#configure-probes) for the patroni container (in seconds).

### `patroni.dynamicConfiguration`

Custom PostgreSQL configuration options. Please note that configuration changes are automatically applied to the running instances without validation, so having an invalid config can make the cluster unavailable.

| Value type | Example |
| ---------- | ------- |
| :material-text-long: subdoc | <pre>postgresql:<br>  parameters:<br>    max_parallel_workers: 2<br>    max_worker_processes: 2<br>    shared_buffers: 1GB<br>    work_mem: 2MB</pre> |

### `patroni.switchover.enabled`

Enables or disables [manual change of the cluster primary instance](change-primary.md).

| Value type | Example |
| ---------- | ------- |
| :material-code-string: string | <pre>true</pre> |

### `patroni.switchover.targetInstance`

The name of the Pod that should be [set as the new primary](change-primary.md). When not specified, the new primary will be selected randomly.

| Value type | Example |
| ---------- | ------- |
| :material-code-string: string |  |

### `patroni.createReplicaMethods`

Defines available replica creation methods and the order of executing them during a cluster start or reinitialisation. Patroni will stop on the first one that returns 0. 

By default, `pg_basebackup` is used to create replicas during a new cluster deployment. After the Operator makes an initial backup, it updates the Patroni ConfigMap assign the `pgBackRest` as the first item in the list. This configuration is not propagated to Patroni itself until you restart the database instance Pods or manually reload Patroni configuration.

In the same way, after you define the replica set methods and apply the configuration, the Operator updates the Patroni ConfigMap. You must manually reload Patroni configuration of every database instance to make Patroni aware of the changes. Read more about setting replica methods in the [Configure create_replica_methods](reinit.md#configure-create_replica_methods) section.

| Value type | Example |
| ---------- | ------- |
| :material-code-string: string | - pgbackrest <br> - basebackup |

## Custom extensions Section

The `extensions` section in the [deploy/cr.yaml :octicons-link-external-16:](https://github.com/percona/percona-postgresql-operator/blob/main/deploy/cr.yaml)
file contains configuration options to [manage PostgreSQL extensions](custom-extensions.md).

### `extensions.image`

Image for the custom PostgreSQL extension loader sidecar container.

| Value type | Example |
| ---------- | ------- |
| :material-code-string: string | `docker.io/percona/percona-postgresql-operator:{{ release }}` |

### `extensions.imagePullPolicy`

[Policy :octicons-link-external-16:](https://kubernetes.io/docs/concepts/containers/images/#updating-images) for the custom extension sidecar container.

| Value type | Example |
| ---------- | ------- |
| :material-code-string: string | `Always` |

### `extensions.storage.type`

The cloud storage type used for backups. Only `s3` type is currently supported.

| Value type | Example |
| ---------- | ------- |
| :material-code-string: string | `s3` |

### `extensions.storage.bucket`

The [Amazon S3 bucket :octicons-link-external-16:](https://docs.aws.amazon.com/AmazonS3/latest/dev/UsingBucket.html) name for prepackaged PostgreSQL custom extensions.

| Value type | Example |
| ---------- | ------- |
| :material-code-string: string | `pg-extensions` |

### `extensions.storage.region`

The [AWS region :octicons-link-external-16:](https://docs.aws.amazon.com/general/latest/gr/rande.html) to use.

| Value type | Example |
| ---------- | ------- |
| :material-code-string: string | `eu-central-1` |

### `extensions.storage.endpoint`

The [S3 endpoint :octicons-link-external-16:](https://docs.aws.amazon.com/general/latest/gr/s3.html) to use.

| Value type | Example |
| ---------- | ------- |
| :material-code-string: string | `s3.eu-central-1.amazonaws.com` |

### `extensions.storage.forcePathStyle`

When set to `true`, enforces path-style access method of constructing S3 URLs, where the bucket name appears in the path portion of the URL. Default `false` value means the Operator uses the virtual-hosted-style for accessing S3 storage, where the bucket name is part of the domain name.

| Value type | Example |
| ---------- | ------- |
| :material-toggle-switch-outline: boolean | `false` |

### `extensions.storage.disableSSL`

When set to `true`, instructs the Operator to skip TLS verification when accessing the storage. Can be used if your storage endpoint uses self-signed certificates or doesn’t support TLS to allow successful downloads.

| Value type | Example |
| ---------- | ------- |
| :material-toggle-switch-outline: boolean | `false` |

### `extensions.storage.secret.name`

The [Kubernetes secret :octicons-link-external-16:](https://kubernetes.io/docs/concepts/configuration/secret/) for the custom extensions storage. It should contain `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY` keys.

| Value type | Example |
| ---------- | ------- |
| :material-code-string: string | `cluster1-extensions-secret` |

### `extensions.builtin.pg_stat_monitor`

Enable or disable [pg_stat_monitor :octicons-link-external-16:](https://docs.percona.com/pg-stat-monitor/index.html) PostgreSQL extension.

| Value type | Example |
| ---------- | ------- |
| :material-toggle-switch-outline: boolean | `true` |

### `extensions.builtin.pg_stat_statements`

Enable or disable [pg_stat_statements :octicons-link-external-16:](https://www.postgresql.org/docs/current/pgstatstatements.html) PostgreSQL extension.

| Value type | Example |
| ---------- | ------- |
| :material-toggle-switch-outline: boolean | `false` |

### `extensions.builtin.pg_audit`

Enable or disable [PGAudit :octicons-link-external-16:](https://www.pgaudit.org/) PostgreSQL extension.

| Value type | Example |
| ---------- | ------- |
| :material-toggle-switch-outline: boolean | `true` |

### `extensions.builtin.pgvector`

Enable or disable [pgvector :octicons-link-external-16:](https://github.com/pgvector/pgvector) PostgreSQL extension. **This extension is not compatible with PostgreSQL 12!**

| Value type | Example |
| ---------- | ------- |
| :material-toggle-switch-outline: boolean | `false` |

### `extensions.builtin.pg_repack`

Enable or disable [pg_repack :octicons-link-external-16:](https://github.com/reorg/pg_repack) PostgreSQL extension. 

| Value type | Example |
| ---------- | ------- |
| :material-toggle-switch-outline: boolean | `false` |

### `extensions.custom.name`

Name of the PostgreSQL custom extension.

| Value type | Example |
| ---------- | ------- |
| :material-code-string: string | `pg_cron` |

### `extensions.custom.version`

Version of the PostgreSQL custom extension.

| Value type | Example |
| ---------- | ------- |
| :material-code-string: string | `1.6.1` |

