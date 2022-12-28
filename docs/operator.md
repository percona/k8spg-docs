# Custom Resource options

The Cluster is configured via the
[deploy/cr.yaml](https://github.com/percona/percona-postgresql-operator/blob/main/deploy/cr.yaml) file.

The metadata part of this file contains the following keys:

* `name` (`cluster1` by default) sets the name of your Percona Distribution
for PostgreSQL Cluster; it should include only [URL-compatible characters](https://datatracker.ietf.org/doc/html/rfc3986#section-2.3), not exceed 22 characters, start with an alphabetic character, and end with an alphanumeric character;

The spec part of the [deploy/cr.yaml](https://github.com/percona/percona-postgresql-operator/blob/main/deploy/cr.yaml) file contains the following:

|                 | |
|-----------------|-|
| **Key**         | {{ optionlink('standby.enabled') }} |
| **Value**       | boolean |
| **Example**     | `false` |
| **Description** | Enables or disables running the cluster in a standby mode (read-only copy of an existing cluster, useful for disaster recovery, etc) |
|                 | |
| **Key**         | {{ optionlink('standby.host') }} |
| **Value**       | string |
| **Example**     | `"<primary-ip>"` |
| **Description** | Host address of the primary cluster this standby cluster connects to |
|                 | |
| **Key**         | {{ optionlink('standby.port') }} |
| **Value**       | string |
| **Example**     | `"<primary-port>"` |
| **Description** | Port number used by a standby copy to connect to the primary cluster |
| **Key**         | {{ optionlink('openshift') }} |
| **Value**       | boolean |
| **Example**     | `true` |
| **Description** | Set to `true` if the cluster is being deployed on OpenShift, set to `false` otherwise, or  unset it for autodetection |
|                 | |
| **Key**         | {{ optionlink('users.name') }} |
| **Value**       | string |
| **Example**     | `rhino` |
| **Description** | The name of the PostgreSQL user |
|                 | |
| **Key**         | {{ optionlink('users.databases') }} |
| **Value**       | string |
| **Example**     | `zoo` |
| **Description** | Databases accessible by a specific PostgreSQL user with rights to create objects in them (the option is ignored for `postgres` user; also, modifying it can't be used to revoke the already given access) |
|                 | |
| **Key**         | {{ optionlink('users.options') }} |
| **Value**       | string |
| **Example**     | `"SUPERUSER"` |
| **Description** | The `ALTER ROLE` options other than password (the option is ignored for `postgres` user) |
|                 | |
| **Key**         | {{ optionlink('databaseInitSQL.key') }} |
| **Value**       | string |
| **Example**     | `init.sql` |
| **Description** | Data key for the [Custom configuration options ConfigMap](https://kubernetes.io/docs/concepts/configuration/configmap/) with the init SQL file, which will be executed at cluster creation time |
|                 | |
| **Key**         | {{ optionlink('databaseInitSQL.name') }} |
| **Value**       | string |
| **Example**     | `cluster1-init-sql` |
| **Description** | Name of the [ConfigMap](https://kubernetes.io/docs/concepts/configuration/configmap/) with the init SQL file, which will be executed at cluster creation time |
|                 | |
| **Key**         | {{ optionlink('shutdown') }} |
| **Value**       | string |
| **Example**     | `false` |
| **Description** | Setting it to `true` gracefully stops the cluster, scaling workloads are scaled to zero and suspending CronJobs; setting it to `false` after shut down starts the cluster back |
|                 | |
| **Key**         | {{ optionlink('paused') }} |
| **Value**       | string |
| **Example**     | `false` |
| **Description** | Setting it to `true` stops the Operator's activity including the rollout and reconciliation of changes made in the Custom Resource; setting it to `false` starts the Operator's activity back |
|                 | |
| **Key**         | {{ optionlink('dataSource.postgresCluster.clusterName') }} |
| **Value**       | string |
| **Example**     | `cluster1` |
| **Description** | Name of an existing cluster to use as the data source when restoring backup to a new cluster |
|                 | |
| **Key**         | {{ optionlink('dataSource.postgresCluster.repoName') }} |
| **Value**       | string |
| **Example**     | `repo1` |
| **Description** | Name of the pgBackRest repository in the source cluster that contains the backups to be restored to a new cluster |
|                 | |
| **Key**         | {{ optionlink('dataSource.postgresCluster.options') }} |
| **Value**       | string |
| **Example**     | |
| **Description** | The pgBackRest command-line options for the pgBackRest restore command |
|                 | |
| **Key**         | {{ optionlink('dataSource.pgbackrest.stanza') }} |
| **Value**       | string |
| **Example**     | `db` |
| **Description** | Name of the [pgBackRest stanza](https://pgbackrest.org/command.html) to use as the data source when restoring backup to a new cluster |
|                 | |
| **Key**         | {{ optionlink('dataSource.pgbackrest.configuration.secret.name') }} |
| **Value**       | string |
| **Example**     | `pgo-s3-creds` |
| **Description** | Name of the Secret object with custom pgBackRest configuration, which will be added to the pgBackRest configuration generated by the Operator |
|                 | |
| **Key**         | {{ optionlink('dataSource.pgbackrest.global') }} |
| **Value**       | subdoc |
| **Example**     | `/pgbackrest/postgres-operator/hippo/repo1` |
| **Description** | Settings, which are to be included in the `global` section of the pgBackRest configuration generated by the Operator |
|                 | |
| **Key**         | {{ optionlink('dataSource.pgbackrest.repo.name') }} |
| **Value**       | string |
| **Example**     | `repo1` |
| **Description** | Name of the pgBackRest repository |
|                 | |
| **Key**         | {{ optionlink('dataSource.pgbackrest.repo.s3.bucket') }} |
| **Value**       | string |
| **Example**     | `"my-bucket"` |
| **Description** | The [Amazon S3 bucket](https://docs.aws.amazon.com/AmazonS3/latest/dev/UsingBucket.html) or [Google Cloud Storage bucket](https://cloud.google.com/storage/docs/key-terms#buckets)
name used for backups |
|                 | |
| **Key**         | {{ optionlink('dataSource.pgbackrest.repo.s3.endpointURL') }} |
| **Value**       | string |
| **Example**     | `"s3.ca-central-1.amazonaws.com"` |
| **Description** | The endpoint URL of the S3-compatible storage to be used for backups (not needed for the original Amazon S3 cloud) |
|                 | |
| **Key**         | {{ optionlink('dataSource.pgbackrest.repo.s3.region') }} |
| **Value**       | boolean |
| **Example**     | `"ca-central-1"` |
| **Description** | The [AWS region](https://docs.aws.amazon.com/general/latest/gr/rande.html) to use for Amazon and all S3-compatible storages |
|                 | |
| **Key**         | {{ optionlink('image') }} |
| **Value**       | string |
| **Example**     | `perconalab/percona-postgresql-operator:main-ppg14-postgres` |
| **Description** | The PostgreSQL Docker image to use |
|                 | |
| **Key**         | {{ optionlink('imagePullPolicy') }} |
| **Value**       | string |
| **Example**     | `Always` |
| **Description** | This option is used to set the [policy](https://kubernetes.io/docs/concepts/containers/images/#updating-images) for updating PostgreSQL images |
|                 | |
| **Key**         | {{ optionlink('postgresVersion') }} |
| **Value**       | int |
| **Example**     | 14 |
| **Description** | The major version of PostgreSQL to use |
|                 | |
| **Key**         | {{ optionlink('port') }} |
| **Value**       | int |
| **Example**     | 5432 |
| **Description** | The port number for PostgreSQL |
|                 | |
| **Key**         | {{ optionlink('expose.annotations') }} |
| **Value**       | label |
| **Example**     | `my-annotation: value1` |
| **Description** | The [Kubernetes annotations](https://kubernetes.io/docs/concepts/overview/working-with-objects/annotations/) metadata for PostgreSQL |
|                 | |
| **Key**         | {{ optionlink('expose.labels') }} |
| **Value**       | label |
| **Example**     | `my-label: value2` |
| **Description** | Set [labels](https://kubernetes.io/docs/concepts/overview/working-with-objects/labels/) for the PostgreSQL Service |
|                 | |
| **Key**         | {{ optionlink('expose.type') }} |
| **Value**       | string |
| **Example**     | `LoadBalancer` |
| **Description** | Specifies the type of [Kubernetes Service](https://kubernetes.io/docs/concepts/services-networking/service/#publishing-services-service-types) for PostgreSQL |
|                 | |
| **Key**         | {{ optionlink('instances.name') }} |
| **Value**       | string |
| **Example**     | `rs 0` |
| **Description** | The name of the PostgreSQL instance |
|                 | |
| **Key**         | {{ optionlink('instances.replicas') }} |
| **Value**       | int |
| **Example**     | 3 |
| **Description** | The number of Replicas to create for the PostgreSQL instance |
|                 | |
| **Key**         | {{ optionlink('instances.resources.limits.cpu') }} |
| **Value**       | string |
| **Example**     | `2.0` |
| **Description** | [Kubernetes CPU limits](https://kubernetes.io/docs/concepts/configuration/manage-compute-resources-container/#resource-requests-and-limits-of-pod-and-container) for a PostgreSQL instance |
|                 | |
| **Key**         | {{ optionlink('instances.resources.limits.memory') }} |
| **Value**       | string |
| **Example**     | `4Gi` |
| **Description** | The [Kubernetes memory limits](https://kubernetes.io/docs/concepts/configuration/manage-compute-resources-container/#resource-requests-and-limits-of-pod-and-container) for a PostgreSQL instance |
|                 | |
| **Key**         | {{ optionlink('instances.sidecars.image') }} |
| **Value**       | string |
| **Example**     | `mycontainer1:latest` |
| **Description** | Image for the [custom sidecar container](faq.md#faq-sidecar) for PostgreSQL Pods |
|                 | |
| **Key**         | {{ optionlink('instances.sidecars.name') }} |
| **Value**       | string |
| **Example**     | `testcontainer` |
| **Description** | Name of the [custom sidecar container](faq.md#faq-sidecar) for PostgreSQL Pods |
|                 | |
| **Key**         | {{ optionlink('instances.topologySpreadConstraints.maxSkew') }} |
| **Value**       | int |
| **Example**     | 1 |
| **Description** | The degree to which Pods may be unevenly distributed under the [Kubernetes Pod Topology Spread Constraints](https://kubernetes.io/docs/concepts/scheduling-eviction/topology-spread-constraints/) |
|                 | |
| **Key**         | {{ optionlink('instances.topologySpreadConstraints.topologyKey') }} |
| **Value**       | string |
| **Example**     | `my-node-label` |
| **Description** | The key of node labels for the [Kubernetes Pod Topology Spread Constraints](https://kubernetes.io/docs/concepts/scheduling-eviction/topology-spread-constraints/) |
|                 | |
| **Key**         | {{ optionlink('instances.topologySpreadConstraints.whenUnsatisfiable') }} |
| **Value**       | string |
| **Example**     | `DoNotSchedule` |
| **Description** | What to do with a Pod if it doesn't satisfy the [Kubernetes Pod Topology Spread Constraints](https://kubernetes.io/docs/concepts/scheduling-eviction/topology-spread-constraints/) |
|                 | |
| **Key**         | {{ optionlink('instances.topologySpreadConstraints.labelSelector.matchLabels') }} |
| **Value**       | label |
| **Example**     | `postgres-operator.crunchydata.com/instance-set: instance1` |
| **Description** | The Label selector for the [Kubernetes Pod Topology Spread Constraints](https://kubernetes.io/docs/concepts/scheduling-eviction/topology-spread-constraints/) |
|                 | |
| **Key**         | {{ optionlink('instances.tolerations.effect') }} |
| **Value**       | string |
| **Example**     | `NoSchedule` |
| **Description** | The [Kubernetes Pod tolerations](https://kubernetes.io/docs/concepts/configuration/taint-and-toleration/#concepts) effect for the PostgreSQL instance |
|                 | |
| **Key**         | {{ optionlink('instances.tolerations.key') }} |
| **Value**       | string |
| **Example**     | `role` |
| **Description** | The [Kubernetes Pod tolerations](https://kubernetes.io/docs/concepts/configuration/taint-and-toleration/#concepts) key for the PostgreSQL instance |
|                 | |
| **Key**         | {{ optionlink('instances.tolerations.operator') }} |
| **Value**       | string |
| **Example**     | `Equal` |
| **Description** | The [Kubernetes Pod tolerations](https://kubernetes.io/docs/concepts/configuration/taint-and-toleration/#concepts) operator for the PostgreSQL instance |
|                 | |
| **Key**         | {{ optionlink('instances.tolerations.value') }} |
| **Value**       | string |
| **Example**     | `connection-poolers` |
| **Description** | The [Kubernetes Pod tolerations](https://kubernetes.io/docs/concepts/configuration/taint-and-toleration/#concepts) value for the PostgreSQL instance |
|                 | |
| **Key**         | {{ optionlink('instances.priorityClassName') }} |
| **Value**       | string |
| **Example**     | `high-priority` |
| **Description** | The [Kuberentes Pod priority class](https://kubernetes.io/docs/concepts/configuration/pod-priority-preemption/#priorityclass) for PostgreSQL instance Pods |
|                 | |
| **Key**         | {{ optionlink('instances.walVolumeClaimSpec.accessModes') }} |
| **Value**       | string |
| **Example**     | `ReadWriteOnce` |
| **Description** | The [Kubernetes PersistentVolumeClaim](https://kubernetes.io/docs/concepts/storage/persistent-volumes/#persistentvolumeclaims) access modes for the PostgreSQL Write-ahead Log storage |
|                 | |
| **Key**         | {{ optionlink('instances.walVolumeClaimSpec.resources.requests.storage') }} |
| **Value**       | string |
| **Example**     | `1Gi` |
| **Description** | The [Kubernetes storage requests](https://kubernetes.io/docs/concepts/configuration/manage-compute-resources-container/#resource-requests-and-limits-of-pod-and-container) for the storage the PostgreSQL instance will use |
|                 | |
| **Key**         | {{ optionlink('instances.dataVolumeClaimSpec.accessModes') }} |
| **Value**       | string |
| **Example**     | `ReadWriteOnce` |
| **Description** | The [Kubernetes PersistentVolumeClaim](https://kubernetes.io/docs/concepts/storage/persistent-volumes/#persistentvolumeclaims) access modes for the PostgreSQL Write-ahead Log storage |
|                 | |
| **Key**         | {{ optionlink('instances.dataVolumeClaimSpec.resources.requests.storage') }} |
| **Value**       | string |
| **Example**     | `1Gi` |
| **Description** | The [Kubernetes storage requests](https://kubernetes.io/docs/concepts/configuration/manage-compute-resources-container/#resource-requests-and-limits-of-pod-and-container) for the storage the PostgreSQL instance will use |

## Backup Section

The `backup` section in the
[deploy/cr.yaml](https://github.com/percona/percona-postgresql-operator/blob/main/deploy/cr.yaml)
file contains the following configuration options for the regular
Percona Distribution for PostgreSQL backups.

|                 | |
|-----------------|-|

## PMM Section

The `pmm` section in the [deploy/cr.yaml](https://github.com/percona/percona-postgresql-operator/blob/main/deploy/cr.yaml)
file contains configuration options for Percona Monitoring and Management.

|                 | |
|-----------------|-|
| **Key**         | {{ optionlink('pmm.enabled') }} |
| **Value**       | boolean |
| **Example**     | `false` |
| **Description** | Enables or disables [monitoring Percona Distribution for PostgreSQL cluster with PMM](https://www.percona.com/doc/percona-monitoring-and-management/2.x/setting-up/client/postgresql.html) |
|                 | |
| **Key**         | {{ optionlink('pmm.image') }} |
| **Value**       | string |
| **Example**     | `percona/pmm-client:{{ pmm2recommended }}` |
| **Description** | [Percona Monitoring and Management (PMM) Client](https://www.percona.com/doc/percona-monitoring-and-management/2.x/details/architecture.html#pmm-client) Docker image |
|                 | |
| **Key**         | {{ optionlink('pmm.imagePullPolicy') }} |
| **Value**       | string |
| **Example**     | `IfNotPresent` |
| **Description** | This option is used to set the [policy](https://kubernetes.io/docs/concepts/containers/images/#updating-images) for updating PMM Client images |
|                 | |
| **Key**         | {{ optionlink('pmm.pmmSecret') }} |
| **Value**       | string |
| **Example**     | `cluster1-pmm-secret` |
| **Description** | Name of the [Kubernetes Secret object](https://kubernetes.io/docs/concepts/configuration/secret/#using-imagepullsecrets) for the PMM Server password |
|                 | |
| **Key**         | {{ optionlink('pmm.serverHost') }} |
| **Value**       | string |
| **Example**     | `monitoring-service` |
| **Description** | Address of the PMM Server to collect data from the cluster |

## proxy Section

The `proxy` section in the [deploy/cr.yaml](https://github.com/percona/percona-postgresql-operator/blob/main/deploy/cr.yaml)
file contains configuration options for the [pgBouncer](http://pgbouncer.github.io/) connection pooler for PostgreSQL.

|                 | |
|-----------------|-|
| **Key**         | {{ optionlink('proxy.pgBouncer.replicas') }} |
| **Value**       | int |
| **Example**     | `3` |
| **Description** | The number of the pgBouncer Pods to provide connection pooling |
|                 | |
| **Key**         | {{ optionlink('proxy.pgBouncer.image') }} |
| **Value**       | string |
| **Example**     | `perconalab/percona-postgresql-operator:main-ppg14-pgbouncer` |
| **Description** | Docker image for the [pgBouncer](http://pgbouncer.github.io/) connection pooler |
|                 | |
| **Key**         | {{ optionlink('pgBouncer.exposePostgresUser') }} |
| **Value**       | boolean |
| **Example**     | `false` |
| **Description** | Enables or disables [exposing postgres user through pgBouncer](users.md#application-users) |
|                 | |
| **Key**         | {{ optionlink('pgBouncer.resources.limits.cpu') }} |
| **Value**       | int |
| **Example**     | `200m` |
| **Description** | [Kubernetes CPU limits](https://kubernetes.io/docs/concepts/configuration/manage-compute-resources-container/#resource-requests-and-limits-of-pod-and-container) for a pgBouncer container |
|                 | |
| **Key**         | {{ optionlink('pgBouncer.resources.limits.memory') }} |
| **Value**       | int |
| **Example**     | `128Mi` |
| **Description** | The [Kubernetes memory limits](https://kubernetes.io/docs/concepts/configuration/manage-compute-resources-container/#resource-requests-and-limits-of-pod-and-container) for a pgBouncer container |
|                 | |
| **Key**         | {{ optionlink('pgBouncer.expose.type') }} |
| **Value**       | string |
| **Example**     | `ClusterIP` |
| **Description** | Specifies the type of [Kubernetes Service](https://kubernetes.io/docs/concepts/services-networking/service/#publishing-services-service-types) for pgBouncer |
|                 | |
| **Key**         | {{ optionlink('pgBouncer.expose.annotations') }} |
| **Value**       | label |
| **Example**     | `pg-cluster-annot: cluster1` |
| **Description** | The [Kubernetes annotations](https://kubernetes.io/docs/concepts/overview/working-with-objects/annotations/) metadata for pgBouncer |
|                 | |
| **Key**         | {{ optionlink('pgBouncer.expose.labels') }} |
| **Value**       | label |
| **Example**     | `pg-cluster-label: cluster1` |
| **Description** | Set [labels](https://kubernetes.io/docs/concepts/overview/working-with-objects/labels/) for the pgBouncer Service |
|                 | |
| **Key**         | {{ optionlink('pgBouncer.affinity.antiAffinityType') }} |
| **Value**       | string |
| **Example**     | `preferred` |
| **Description** | [Pod anti-affinity type](constraints.md#affinity-and-anti-affinity), can be either `preferred` or `required` |
