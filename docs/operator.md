# Custom Resource options

The Cluster is configured via the
[deploy/cr.yaml :octicons-link-external-16:](https://github.com/percona/percona-postgresql-operator/blob/main/deploy/cr.yaml) file.

## `metadata`

The metadata part of this file contains the following keys:

* <a name="metadata-name"></a> `name` (`cluster1` by default) sets the name of your Percona Distribution
for PostgreSQL Cluster; it should include only [URL-compatible characters :octicons-link-external-16:](https://datatracker.ietf.org/doc/html/rfc3986#section-2.3), not exceed 22 characters, start with an alphabetic character, and end with an alphanumeric character;

* <a name="finalizers-delete-ssl"></a> `finalizers.percona.com/delete-ssl` if present, activates the [Finalizer :octicons-link-external-16:](https://kubernetes.io/docs/tasks/extend-kubernetes/custom-resources/custom-resource-definitions/#finalizers) which deletes [objects, created for SSL](TLS.md) (Secret, certificate, and issuer) after the cluster deletion event (off by default).

* `finalizers.percona.com/delete-pvc` if present, activates the [Finalizer :octicons-link-external-16:](https://kubernetes.io/docs/tasks/extend-kubernetes/custom-resources/custom-resource-definitions/#finalizers) which deletes [Persistent Volume Claims :octicons-link-external-16:](https://kubernetes.io/docs/concepts/storage/persistent-volumes/) for the database cluster Pods after the deletion event (off by default).

## Toplevel `spec` elements

The spec part of the [deploy/cr.yaml :octicons-link-external-16:](https://github.com/percona/percona-postgresql-operator/blob/main/deploy/cr.yaml) file contains the following:

### `crVersion`

Version of the Operator the Custom Resource belongs to.

| Value type | Example |
| ---------- | ------- |
| :material-code-string: string | `{{ release }}` |

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

Set to `true` if the cluster is being deployed on OpenShift, set to `false` otherwise, or  unset it for autodetection.

| Value type | Example |
| ---------- | ------- |
| :material-toggle-switch-outline: boolean | `true` |

### `standby.repoName`

Name of the pgBackRest repository in the primary cluster this standby cluster connects to.

| Value type | Example |
| ---------- | ------- |
| :material-code-string: string | `repo1` |

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

### `dataSource.postgresCluster.clusterName`

Name of an existing cluster to use as the data source when restoring backup to a new cluster.

| Value type | Example |
| ---------- | ------- |
| :material-code-string: string | `cluster1` |

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
name used for backups.

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
| :material-numeric-1-box: int | `14` |

### `port`

The port number for PostgreSQL.

| Value type | Example |
| ---------- | ------- |
| :material-numeric-1-box: int | `5432` |

### `expose.annotations`

The [Kubernetes annotations :octicons-link-external-16:](https://kubernetes.io/docs/concepts/overview/working-with-objects/annotations/) metadata for PostgreSQL.

| Value type | Example |
| ---------- | ------- |
| :material-label-outline: label | `my-annotation: value1` |

### `expose.labels`

Set [labels :octicons-link-external-16:](https://kubernetes.io/docs/concepts/overview/working-with-objects/labels/) for the PostgreSQL Service.

| Value type | Example |
| ---------- | ------- |
| :material-label-outline: label | `my-label: value2` |

### `expose.type`

Specifies the type of [Kubernetes Service :octicons-link-external-16:](https://kubernetes.io/docs/concepts/services-networking/service/#publishing-services-service-types) for PostgreSQL.

| Value type | Example |
| ---------- | ------- |
| :material-code-string: string | `LoadBalancer` |

### `expose.loadBalancerSourceRanges`

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

The [Kuberentes Pod priority class :octicons-link-external-16:](https://kubernetes.io/docs/concepts/configuration/pod-priority-preemption/#priorityclass) for PostgreSQL instance Pods.

| Value type | Example |
| ---------- | ------- |
| :material-code-string: string | `high-priority` |

### 'instances.securityContext'

A custom [Kubernetes Security Context for a Pod :octicons-link-external-16:](https://kubernetes.io/docs/tasks/configure-pod-container/security-context/) to be used instead of the default one.

| Value type  | Example    |
| ----------- | ---------- |
| :material-text-long: subdoc      | <pre>fsGroup: 1001<br>runAsUser: 1001<br>runAsNonRoot: true<br>fsGroupChangePolicy: "OnRootMismatch"<br>runAsGroup: 1001<br>seLinuxOptions:<br>  type: spc_t<br>  level: s0:c123,c456<br>seccompProfile:<br>  type: Localhost<br>  localhostProfile: localhost/profile.json<br>supplementalGroups:<br>- 1001<br>sysctls:<br>- name: net.ipv4.tcp_keepalive_time<br>  value: "600"<br>- name: net.ipv4.tcp_keepalive_intvl<br>  value: "60"</pre> |

### `instances.walVolumeClaimSpec.accessModes`

The [Kubernetes PersistentVolumeClaim :octicons-link-external-16:](https://kubernetes.io/docs/concepts/storage/persistent-volumes/#persistentvolumeclaims) access modes for the PostgreSQL Write-ahead Log storage.

| Value type | Example |
| ---------- | ------- |
| :material-code-string: string | `ReadWriteOnce` |

### `instances.walVolumeClaimSpec.resources.requests.storage`

The [Kubernetes storage requests :octicons-link-external-16:](https://kubernetes.io/docs/concepts/configuration/manage-compute-resources-container/#resource-requests-and-limits-of-pod-and-container) for the storage the PostgreSQL instance will use.

| Value type | Example |
| ---------- | ------- |
| :material-code-string: string | `1Gi` |

### `instances.dataVolumeClaimSpec.accessModes`

The [Kubernetes PersistentVolumeClaim :octicons-link-external-16:](https://kubernetes.io/docs/concepts/storage/persistent-volumes/#persistentvolumeclaims) access modes for the PostgreSQL Write-ahead Log storage.

| Value type | Example |
| ---------- | ------- |
| :material-code-string: string | `ReadWriteOnce` |

### `instances.dataVolumeClaimSpec.resources.requests.storage`

The [Kubernetes storage requests :octicons-link-external-16:](https://kubernetes.io/docs/concepts/configuration/manage-compute-resources-container/#resource-requests-and-limits-of-pod-and-container) for the storage the PostgreSQL instance will use.

| Value type | Example |
| ---------- | ------- |
| :material-code-string: string | `1Gi` |

## instances.sidecars subsection

The `instances.sidecars` subsection in the [deploy/cr.yaml :octicons-link-external-16:](https://github.com/percona/percona-postgresql-operator/blob/main/deploy/cr.yaml)
file contains configuration options for [custom sidecar containers](sidecar.md) which can be added to PostgreSQL Pods.

### `instances.sidecars.image`

Image for the [custom sidecar container](sidecar.md) for PostgreSQL Pods.

| Value type | Example |
| ---------- | ------- |
| :material-code-string: string | `mycontainer1:latest` |

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

### `backups.pgbackrest.metadata.labels`

Set [labels :octicons-link-external-16:](https://kubernetes.io/docs/concepts/overview/working-with-objects/labels/) for pgBackRest Pods.

| Value type | Example |
| ---------- | ------- |
| :material-label-outline: label | `pg-cluster-label: cluster1` |

### `backups.pgbackrest.image`

The Docker image for [pgBackRest](backups.md#backups-pgbackrest).

| Value type | Example |
| ---------- | ------- |
| :material-code-string: string | `perconalab/percona-postgresql-operator:{{release}}-ppg{{postgresrecommended}}-pgbackrest` |

### `backups.pgbackrest.configuration.secret.name`

Name of the [Kubernetes Secret object :octicons-link-external-16:](https://kubernetes.io/docs/concepts/configuration/secret/#using-imagepullsecrets) with custom pgBackRest configuration, which will be added to the pgBackRest configuration generated by the Operator.

| Value type | Example |
| ---------- | ------- |
| :material-code-string: string | `cluster1-pgbackrest-secrets` |

### `backups.pgbackrest.jobs.priorityClassName`

The [Kuberentes Pod priority class :octicons-link-external-16:](https://kubernetes.io/docs/concepts/configuration/pod-priority-preemption/#priorityclass) for pgBackRest jobs.

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

### `backups.pgbackrest.jobs.tolerations.effect`

The [Kubernetes Pod tolerations :octicons-link-external-16:](https://kubernetes.io/docs/concepts/configuration/taint-and-toleration/#concepts) effect for a pgBackRest job.

| Value type | Example |
| ---------- | ------- |
| :material-code-string: string | `NoSchedule` |

### `backups.pgbackrest.jobs.tolerations.key`

The [Kubernetes Pod tolerations :octicons-link-external-16:](https://kubernetes.io/docs/concepts/configuration/taint-and-toleration/#concepts) key for a pgBackRest job.

| Value type | Example |
| ---------- | ------- |
| :material-code-string: string | `role` |

### `backups.pgbackrest.jobs.tolerations.operator`

The [Kubernetes Pod tolerations :octicons-link-external-16:](https://kubernetes.io/docs/concepts/configuration/taint-and-toleration/#concepts) operator for a pgBackRest job.

| Value type | Example |
| ---------- | ------- |
| :material-code-string: string | `Equal` |

### `backups.pgbackrest.jobs.tolerations.value`

The [Kubernetes Pod tolerations :octicons-link-external-16:](https://kubernetes.io/docs/concepts/configuration/taint-and-toleration/#concepts) value for a pgBackRest job.

| Value type | Example |
| ---------- | ------- |
| :material-code-string: string | `connection-poolers` |

### 'backups.pgbackrest.jobs.securityContext'

A custom [Kubernetes Security Context for a Pod :octicons-link-external-16:](https://kubernetes.io/docs/tasks/configure-pod-container/security-context/) to be used instead of the default one.

| Value type  | Example    |
| ----------- | ---------- |
| :material-text-long: subdoc      | <pre>fsGroup: 1001<br>runAsUser: 1001<br>runAsNonRoot: true<br>fsGroupChangePolicy: "OnRootMismatch"<br>runAsGroup: 1001<br>seLinuxOptions:<br>  type: spc_t<br>  level: s0:c123,c456<br>seccompProfile:<br>  type: Localhost<br>  localhostProfile: localhost/profile.json<br>supplementalGroups:<br>- 1001<br>sysctls:<br>- name: net.ipv4.tcp_keepalive_time<br>  value: "600"<br>- name: net.ipv4.tcp_keepalive_intvl<br>  value: "60"</pre> |

### `backups.pgbackrest.global`

Settings, which are to be included in the `global` section of the pgBackRest configuration generated by the Operator.

| Value type | Example |
| ---------- | ------- |
| :material-text-long: subdoc | `/pgbackrest/postgres-operator/hippo/repo1` |

### `backups.pgbackrest.repoHost.priorityClassName`

The [Kuberentes Pod priority class :octicons-link-external-16:](https://kubernetes.io/docs/concepts/configuration/pod-priority-preemption/#priorityclass) for pgBackRest repo.

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
| :material-toggle-switch-outline: boolean | `"ca-central-1"` |

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

## PMM section

The `pmm` section in the [deploy/cr.yaml :octicons-link-external-16:](https://github.com/percona/percona-postgresql-operator/blob/main/deploy/cr.yaml)
file contains configuration options for Percona Monitoring and Management.

### `pmm.enabled`

Enables or disables [monitoring Percona Distribution for PostgreSQL cluster with PMM :octicons-link-external-16:](https://www.percona.com/doc/percona-monitoring-and-management/2.x/setting-up/client/postgresql.html).

| Value type | Example |
| ---------- | ------- |
| :material-toggle-switch-outline: boolean | `false` |

### `pmm.image`

[Percona Monitoring and Management (PMM) Client :octicons-link-external-16:](https://www.percona.com/doc/percona-monitoring-and-management/2.x/details/architecture.html#pmm-client) Docker image.

| Value type | Example |
| ---------- | ------- |
| :material-code-string: string | `percona/pmm-client:{{ pmm2recommended }}` |

### `pmm.imagePullPolicy`

This option is used to set the [policy :octicons-link-external-16:](https://kubernetes.io/docs/concepts/containers/images/#updating-images) for updating PMM Client images.

| Value type | Example |
| ---------- | ------- |
| :material-code-string: string | `IfNotPresent` |

### `pmm.pmmSecret`

Name of the [Kubernetes Secret object :octicons-link-external-16:](https://kubernetes.io/docs/concepts/configuration/secret/#using-imagepullsecrets) for the PMM Server password.

| Value type | Example |
| ---------- | ------- |
| :material-code-string: string | `cluster1-pmm-secret` |

### `pmm.serverHost`

Address of the PMM Server to collect data from the cluster.

| Value type | Example |
| ---------- | ------- |
| :material-code-string: string | `monitoring-service` |

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
| :material-code-string: string | `perconalab/percona-postgresql-operator:{{release}}-ppg{{postgresrecommended}}-pgbouncer` |

### `proxy.pgBouncer.exposeSuperusers`

Enables or disables [exposing superuser user through pgBouncer](users.md#superuser-and-pgbouncer).

| Value type | Example |
| ---------- | ------- |
| :material-toggle-switch-outline: boolean | `false` |

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

### `proxy.pgBouncer.expose.type`

Specifies the type of [Kubernetes Service :octicons-link-external-16:](https://kubernetes.io/docs/concepts/services-networking/service/#publishing-services-service-types) for pgBouncer.

| Value type | Example |
| ---------- | ------- |
| :material-code-string: string | `ClusterIP` |

### `proxy.pgBouncer.expose.annotations`

The [Kubernetes annotations :octicons-link-external-16:](https://kubernetes.io/docs/concepts/overview/working-with-objects/annotations/) metadata for pgBouncer.

| Value type | Example |
| ---------- | ------- |
| :material-label-outline: label | `pg-cluster-annot: cluster1` |

### `proxy.pgBouncer.expose.labels`

Set [labels :octicons-link-external-16:](https://kubernetes.io/docs/concepts/overview/working-with-objects/labels/) for the pgBouncer Service.

| Value type | Example |
| ---------- | ------- |
| :material-label-outline: label | `pg-cluster-label: cluster1` |

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

## Custom extensions Section

The `extensions` section in the [deploy/cr.yaml :octicons-link-external-16:](https://github.com/percona/percona-postgresql-operator/blob/main/deploy/cr.yaml)
file contains configuration options to [manage PostgreSQL extensions](custom-extensions.md).

### `extensions.image`

Image for the custom PostgreSQL extension loader sidecar container.

| Value type | Example |
| ---------- | ------- |
| :material-code-string: string | `percona/percona-postgresql-operator:{{ release }}` |

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

### `extensions.storage.secret.name`

The [Kubernetes secret :octicons-link-external-16:](https://kubernetes.io/docs/concepts/configuration/secret/) for the custom extensions storage. It should contain `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY` keys.

| Value type | Example |
| ---------- | ------- |
| :material-code-string: string | `cluster1-extensions-secret` |

### `extensions.builtin`

The key-value pairs which enable or disable [Percona Distribution for PostgreSQL builtin extensions :octicons-link-external-16:](https://docs.percona.com/postgresql/16/).

| Value type | Example |
| ---------- | ------- |
| :material-label-outline: label | `pg_stat_monitor: true` |

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

