---
title: Percona PostgreSQL Operator Custom Resource Options
draft: false
weight: 1
description: Custom Resource Options
---

Packages:

- [pg.percona.com/v2beta1](#pgperconacomv2beta1)

<h1 id="pgperconacomv2beta1">pg.percona.com/v2beta1</h1>

Resource Types:

- [PerconaPGCluster](#perconapgcluster)

- [PerconaPGBackup](#perconapgbackup)

- [PerconaPGRestore](#perconapgrestore)




<h2 id="perconapgcluster">PerconaPGCluster</h2>

|                 | |
|-----------------|-|

| **Key**         | PerconaPGCluster.spec |
| **Value**       | object |
| **Required**    | true |
| **Example**     | |
| **Description** |  |
| | || **Key**         | PerconaPGCluster.status |
| **Value**       | object |
| **Required**    | false |
| **Example**     | |
| **Description** |  |
| | |
| **Key**         | PerconaPGCluster.spec.backups |
| **Value**       | object |
| **Required**    | true |
| **Example**     | |
| **Description** | PostgreSQL backup configuration |
| | || **Key**         | PerconaPGCluster.spec.instances |
| **Value**       | []object |
| **Required**    | true |
| **Example**     | |
| **Description** | Specifies one or more sets of PostgreSQL pods that replicate data for this cluster. |
| | || **Key**         | PerconaPGCluster.spec.postgresVersion |
| **Value**       | integer |
| **Required**    | true |
| **Example**     | |
| **Description** | The major version of PostgreSQL installed in the PostgreSQL image |
| | || **Key**         | PerconaPGCluster.spec.dataSource |
| **Value**       | object |
| **Required**    | false |
| **Example**     | |
| **Description** | Specifies a data source for bootstrapping the PostgreSQL cluster. |
| | || **Key**         | PerconaPGCluster.spec.databaseInitSQL |
| **Value**       | object |
| **Required**    | false |
| **Example**     | |
| **Description** | DatabaseInitSQL defines a ConfigMap containing custom SQL that will be run after the cluster is initialized. This ConfigMap must be in the same namespace as the cluster. |
| | || **Key**         | PerconaPGCluster.spec.expose |
| **Value**       | object |
| **Required**    | false |
| **Example**     | |
| **Description** | Specification of the service that exposes the PostgreSQL primary instance. |
| | || **Key**         | PerconaPGCluster.spec.image |
| **Value**       | string |
| **Required**    | false |
| **Example**     | |
| **Description** | The image name to use for PostgreSQL containers. When omitted, the value comes from an operator environment variable. For standard PostgreSQL images, the format is RELATED_IMAGE_POSTGRES_{postgresVersion}, e.g. RELATED_IMAGE_POSTGRES_13. For PostGIS enabled PostgreSQL images, the format is RELATED_IMAGE_POSTGRES_{postgresVersion}_GIS_{postGISVersion}, e.g. RELATED_IMAGE_POSTGRES_13_GIS_3.1. |
| | || **Key**         | PerconaPGCluster.spec.imagePullPolicy |
| **Value**       | enum |
| **Required**    | false |
| **Example**     | |
| **Description** | ImagePullPolicy is used to determine when Kubernetes will attempt to pull (download) container images. More info: https://kubernetes.io/docs/concepts/containers/images/#image-pull-policy |
| | || **Key**         | PerconaPGCluster.spec.imagePullSecrets |
| **Value**       | []object |
| **Required**    | false |
| **Example**     | |
| **Description** | The image pull secrets used to pull from a private registry Changing this value causes all running pods to restart. https://k8s.io/docs/tasks/configure-pod-container/pull-image-private-registry/ |
| | || **Key**         | PerconaPGCluster.spec.openshift |
| **Value**       | boolean |
| **Required**    | false |
| **Example**     | |
| **Description** | Whether or not the PostgreSQL cluster is being deployed to an OpenShift environment. If the field is unset, the operator will automatically detect the environment. |
| | || **Key**         | PerconaPGCluster.spec.patroni |
| **Value**       | object |
| **Required**    | false |
| **Example**     | |
| **Description** |  |
| | || **Key**         | PerconaPGCluster.spec.paused |
| **Value**       | boolean |
| **Required**    | false |
| **Example**     | |
| **Description** | Suspends the rollout and reconciliation of changes made to the PostgresCluster spec. |
| | || **Key**         | PerconaPGCluster.spec.pmm |
| **Value**       | object |
| **Required**    | false |
| **Example**     | |
| **Description** | The specification of PMM sidecars. |
| | || **Key**         | PerconaPGCluster.spec.port |
| **Value**       | integer |
| **Required**    | false |
| **Example**     | |
| **Description** | The port on which PostgreSQL should listen. |
| | || **Key**         | PerconaPGCluster.spec.proxy |
| **Value**       | object |
| **Required**    | false |
| **Example**     | |
| **Description** | The specification of a proxy that connects to PostgreSQL. |
| | || **Key**         | PerconaPGCluster.spec.secrets |
| **Value**       | object |
| **Required**    | false |
| **Example**     | |
| **Description** |  |
| | || **Key**         | PerconaPGCluster.spec.shutdown |
| **Value**       | boolean |
| **Required**    | false |
| **Example**     | |
| **Description** | Whether or not the PostgreSQL cluster should be stopped. When this is true, workloads are scaled to zero and CronJobs are suspended. Other resources, such as Services and Volumes, remain in place. |
| | || **Key**         | PerconaPGCluster.spec.standby |
| **Value**       | object |
| **Required**    | false |
| **Example**     | |
| **Description** | Run this cluster as a read-only copy of an existing cluster or archive. |
| | || **Key**         | PerconaPGCluster.spec.users |
| **Value**       | []object |
| **Required**    | false |
| **Example**     | |
| **Description** | Users to create inside PostgreSQL and the databases they should access. The default creates one user that can access one database matching the PostgresCluster name. An empty list creates no users. Removing a user from this list does NOT drop the user nor revoke their access. |
| | |
| **Key**         | PerconaPGCluster.spec.backups.pgbackrest |
| **Value**       | object |
| **Required**    | true |
| **Example**     | |
| **Description** | pgBackRest archive configuration |
| | |
| **Key**         | PerconaPGCluster.spec.backups.pgbackrest.repos |
| **Value**       | []object |
| **Required**    | true |
| **Example**     | |
| **Description** | Defines a pgBackRest repository |
| | || **Key**         | PerconaPGCluster.spec.backups.pgbackrest.configuration |
| **Value**       | []object |
| **Required**    | false |
| **Example**     | |
| **Description** | Projected volumes containing custom pgBackRest configuration.  These files are mounted under "/etc/pgbackrest/conf.d" alongside any pgBackRest configuration generated by the PostgreSQL Operator: https://pgbackrest.org/configuration.html |
| | || **Key**         | PerconaPGCluster.spec.backups.pgbackrest.global |
| **Value**       | map[string]string |
| **Required**    | false |
| **Example**     | |
| **Description** | Global pgBackRest configuration settings.  These settings are included in the "global" section of the pgBackRest configuration generated by the PostgreSQL Operator, and then mounted under "/etc/pgbackrest/conf.d": https://pgbackrest.org/configuration.html |
| | || **Key**         | PerconaPGCluster.spec.backups.pgbackrest.image |
| **Value**       | string |
| **Required**    | false |
| **Example**     | |
| **Description** | The image name to use for pgBackRest containers.  Utilized to run pgBackRest repository hosts and backups. The image may also be set using the RELATED_IMAGE_PGBACKREST environment variable |
| | || **Key**         | PerconaPGCluster.spec.backups.pgbackrest.jobs |
| **Value**       | object |
| **Required**    | false |
| **Example**     | |
| **Description** | Jobs field allows configuration for all backup jobs |
| | || **Key**         | PerconaPGCluster.spec.backups.pgbackrest.manual |
| **Value**       | object |
| **Required**    | false |
| **Example**     | |
| **Description** | Defines details for manual pgBackRest backup Jobs |
| | || **Key**         | PerconaPGCluster.spec.backups.pgbackrest.metadata |
| **Value**       | object |
| **Required**    | false |
| **Example**     | |
| **Description** | Metadata contains metadata for PostgresCluster resources |
| | || **Key**         | PerconaPGCluster.spec.backups.pgbackrest.repoHost |
| **Value**       | object |
| **Required**    | false |
| **Example**     | |
| **Description** | Defines configuration for a pgBackRest dedicated repository host.  This section is only applicable if at least one "volume" (i.e. PVC-based) repository is defined in the "repos" section, therefore enabling a dedicated repository host Deployment. |
| | || **Key**         | PerconaPGCluster.spec.backups.pgbackrest.restore |
| **Value**       | object |
| **Required**    | false |
| **Example**     | |
| **Description** | Defines details for performing an in-place restore using pgBackRest |
| | || **Key**         | PerconaPGCluster.spec.backups.pgbackrest.sidecars |
| **Value**       | object |
| **Required**    | false |
| **Example**     | |
| **Description** | Configuration for pgBackRest sidecar containers |
| | |
| **Key**         | PerconaPGCluster.spec.backups.pgbackrest.repos[index].name |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | The name of the the repository |
| | || **Key**         | PerconaPGCluster.spec.backups.pgbackrest.repos[index].azure |
| **Value**       | object |
| **Required**    | false |
| **Example**     | |
| **Description** | Represents a pgBackRest repository that is created using Azure storage |
| | || **Key**         | PerconaPGCluster.spec.backups.pgbackrest.repos[index].gcs |
| **Value**       | object |
| **Required**    | false |
| **Example**     | |
| **Description** | Represents a pgBackRest repository that is created using Google Cloud Storage |
| | || **Key**         | PerconaPGCluster.spec.backups.pgbackrest.repos[index].s3 |
| **Value**       | object |
| **Required**    | false |
| **Example**     | |
| **Description** | RepoS3 represents a pgBackRest repository that is created using AWS S3 (or S3-compatible) storage |
| | || **Key**         | PerconaPGCluster.spec.backups.pgbackrest.repos[index].schedules |
| **Value**       | object |
| **Required**    | false |
| **Example**     | |
| **Description** | Defines the schedules for the pgBackRest backups Full, Differential and Incremental backup types are supported: https://pgbackrest.org/user-guide.html#concept/backup |
| | || **Key**         | PerconaPGCluster.spec.backups.pgbackrest.repos[index].volume |
| **Value**       | object |
| **Required**    | false |
| **Example**     | |
| **Description** | Represents a pgBackRest repository that is created using a PersistentVolumeClaim |
| | |
| **Key**         | PerconaPGCluster.spec.backups.pgbackrest.repos[index].azure.container |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | The Azure container utilized for the repository |
| | |
| **Key**         | PerconaPGCluster.spec.backups.pgbackrest.repos[index].gcs.bucket |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | The GCS bucket utilized for the repository |
| | |
| **Key**         | PerconaPGCluster.spec.backups.pgbackrest.repos[index].s3.bucket |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | The S3 bucket utilized for the repository |
| | || **Key**         | PerconaPGCluster.spec.backups.pgbackrest.repos[index].s3.endpoint |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | A valid endpoint corresponding to the specified region |
| | || **Key**         | PerconaPGCluster.spec.backups.pgbackrest.repos[index].s3.region |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | The region corresponding to the S3 bucket |
| | |
| **Key**         | PerconaPGCluster.spec.backups.pgbackrest.repos[index].schedules.differential |
| **Value**       | string |
| **Required**    | false |
| **Example**     | |
| **Description** | Defines the Cron schedule for a differential pgBackRest backup. Follows the standard Cron schedule syntax: https://k8s.io/docs/concepts/workloads/controllers/cron-jobs/#cron-schedule-syntax |
| | || **Key**         | PerconaPGCluster.spec.backups.pgbackrest.repos[index].schedules.full |
| **Value**       | string |
| **Required**    | false |
| **Example**     | |
| **Description** | Defines the Cron schedule for a full pgBackRest backup. Follows the standard Cron schedule syntax: https://k8s.io/docs/concepts/workloads/controllers/cron-jobs/#cron-schedule-syntax |
| | || **Key**         | PerconaPGCluster.spec.backups.pgbackrest.repos[index].schedules.incremental |
| **Value**       | string |
| **Required**    | false |
| **Example**     | |
| **Description** | Defines the Cron schedule for an incremental pgBackRest backup. Follows the standard Cron schedule syntax: https://k8s.io/docs/concepts/workloads/controllers/cron-jobs/#cron-schedule-syntax |
| | |
| **Key**         | PerconaPGCluster.spec.backups.pgbackrest.repos[index].volume.volumeClaimSpec |
| **Value**       | object |
| **Required**    | true |
| **Example**     | |
| **Description** | Defines a PersistentVolumeClaim spec used to create and/or bind a volume |
| | |
| **Key**         | PerconaPGCluster.spec.backups.pgbackrest.repos[index].volume.volumeClaimSpec.accessModes |
| **Value**       | []string |
| **Required**    | false |
| **Example**     | |
| **Description** | accessModes contains the desired access modes the volume should have. More info: https://kubernetes.io/docs/concepts/storage/persistent-volumes#access-modes-1 |
| | || **Key**         | PerconaPGCluster.spec.backups.pgbackrest.repos[index].volume.volumeClaimSpec.dataSource |
| **Value**       | object |
| **Required**    | false |
| **Example**     | |
| **Description** | dataSource field can be used to specify either: * An existing VolumeSnapshot object (snapshot.storage.k8s.io/VolumeSnapshot) * An existing PVC (PersistentVolumeClaim) If the provisioner or an external controller can support the specified data source, it will create a new volume based on the contents of the specified data source. If the AnyVolumeDataSource feature gate is enabled, this field will always have the same contents as the DataSourceRef field. |
| | || **Key**         | PerconaPGCluster.spec.backups.pgbackrest.repos[index].volume.volumeClaimSpec.dataSourceRef |
| **Value**       | object |
| **Required**    | false |
| **Example**     | |
| **Description** | dataSourceRef specifies the object from which to populate the volume with data, if a non-empty volume is desired. This may be any local object from a non-empty API group (non core object) or a PersistentVolumeClaim object. When this field is specified, volume binding will only succeed if the type of the specified object matches some installed volume populator or dynamic provisioner. This field will replace the functionality of the DataSource field and as such if both fields are non-empty, they must have the same value. For backwards compatibility, both fields (DataSource and DataSourceRef) will be set to the same value automatically if one of them is empty and the other is non-empty. There are two important differences between DataSource and DataSourceRef: * While DataSource only allows two specific types of objects, DataSourceRef allows any non-core object, as well as PersistentVolumeClaim objects. * While DataSource ignores disallowed values (dropping them), DataSourceRef preserves all values, and generates an error if a disallowed value is specified. (Beta) Using this field requires the AnyVolumeDataSource feature gate to be enabled. |
| | || **Key**         | PerconaPGCluster.spec.backups.pgbackrest.repos[index].volume.volumeClaimSpec.resources |
| **Value**       | object |
| **Required**    | false |
| **Example**     | |
| **Description** | resources represents the minimum resources the volume should have. If RecoverVolumeExpansionFailure feature is enabled users are allowed to specify resource requirements that are lower than previous value but must still be higher than capacity recorded in the status field of the claim. More info: https://kubernetes.io/docs/concepts/storage/persistent-volumes#resources |
| | || **Key**         | PerconaPGCluster.spec.backups.pgbackrest.repos[index].volume.volumeClaimSpec.selector |
| **Value**       | object |
| **Required**    | false |
| **Example**     | |
| **Description** | selector is a label query over volumes to consider for binding. |
| | || **Key**         | PerconaPGCluster.spec.backups.pgbackrest.repos[index].volume.volumeClaimSpec.storageClassName |
| **Value**       | string |
| **Required**    | false |
| **Example**     | |
| **Description** | storageClassName is the name of the StorageClass required by the claim. More info: https://kubernetes.io/docs/concepts/storage/persistent-volumes#class-1 |
| | || **Key**         | PerconaPGCluster.spec.backups.pgbackrest.repos[index].volume.volumeClaimSpec.volumeMode |
| **Value**       | string |
| **Required**    | false |
| **Example**     | |
| **Description** | volumeMode defines what type of volume is required by the claim. Value of Filesystem is implied when not included in claim spec. |
| | || **Key**         | PerconaPGCluster.spec.backups.pgbackrest.repos[index].volume.volumeClaimSpec.volumeName |
| **Value**       | string |
| **Required**    | false |
| **Example**     | |
| **Description** | volumeName is the binding reference to the PersistentVolume backing this claim. |
| | |
| **Key**         | PerconaPGCluster.spec.backups.pgbackrest.repos[index].volume.volumeClaimSpec.dataSource.kind |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | Kind is the type of resource being referenced |
| | || **Key**         | PerconaPGCluster.spec.backups.pgbackrest.repos[index].volume.volumeClaimSpec.dataSource.name |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | Name is the name of resource being referenced |
| | || **Key**         | PerconaPGCluster.spec.backups.pgbackrest.repos[index].volume.volumeClaimSpec.dataSource.apiGroup |
| **Value**       | string |
| **Required**    | false |
| **Example**     | |
| **Description** | APIGroup is the group for the resource being referenced. If APIGroup is not specified, the specified Kind must be in the core API group. For any other third-party types, APIGroup is required. |
| | |
| **Key**         | PerconaPGCluster.spec.backups.pgbackrest.repos[index].volume.volumeClaimSpec.dataSourceRef.kind |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | Kind is the type of resource being referenced |
| | || **Key**         | PerconaPGCluster.spec.backups.pgbackrest.repos[index].volume.volumeClaimSpec.dataSourceRef.name |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | Name is the name of resource being referenced |
| | || **Key**         | PerconaPGCluster.spec.backups.pgbackrest.repos[index].volume.volumeClaimSpec.dataSourceRef.apiGroup |
| **Value**       | string |
| **Required**    | false |
| **Example**     | |
| **Description** | APIGroup is the group for the resource being referenced. If APIGroup is not specified, the specified Kind must be in the core API group. For any other third-party types, APIGroup is required. |
| | |
| **Key**         | PerconaPGCluster.spec.backups.pgbackrest.repos[index].volume.volumeClaimSpec.resources.limits |
| **Value**       | map[string]int or string |
| **Required**    | false |
| **Example**     | |
| **Description** | Limits describes the maximum amount of compute resources allowed. More info: https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/ |
| | || **Key**         | PerconaPGCluster.spec.backups.pgbackrest.repos[index].volume.volumeClaimSpec.resources.requests |
| **Value**       | map[string]int or string |
| **Required**    | false |
| **Example**     | |
| **Description** | Requests describes the minimum amount of compute resources required. If Requests is omitted for a container, it defaults to Limits if that is explicitly specified, otherwise to an implementation-defined value. More info: https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/ |
| | |
| **Key**         | PerconaPGCluster.spec.backups.pgbackrest.repos[index].volume.volumeClaimSpec.selector.matchExpressions |
| **Value**       | []object |
| **Required**    | false |
| **Example**     | |
| **Description** | matchExpressions is a list of label selector requirements. The requirements are ANDed. |
| | || **Key**         | PerconaPGCluster.spec.backups.pgbackrest.repos[index].volume.volumeClaimSpec.selector.matchLabels |
| **Value**       | map[string]string |
| **Required**    | false |
| **Example**     | |
| **Description** | matchLabels is a map of {key,value} pairs. A single {key,value} in the matchLabels map is equivalent to an element of matchExpressions, whose key field is "key", the operator is "In", and the values array contains only "value". The requirements are ANDed. |
| | |
| **Key**         | PerconaPGCluster.spec.backups.pgbackrest.repos[index].volume.volumeClaimSpec.selector.matchExpressions[index].key |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | key is the label key that the selector applies to. |
| | || **Key**         | PerconaPGCluster.spec.backups.pgbackrest.repos[index].volume.volumeClaimSpec.selector.matchExpressions[index].operator |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | operator represents a key's relationship to a set of values. Valid operators are In, NotIn, Exists and DoesNotExist. |
| | || **Key**         | PerconaPGCluster.spec.backups.pgbackrest.repos[index].volume.volumeClaimSpec.selector.matchExpressions[index].values |
| **Value**       | []string |
| **Required**    | false |
| **Example**     | |
| **Description** | values is an array of string values. If the operator is In or NotIn, the values array must be non-empty. If the operator is Exists or DoesNotExist, the values array must be empty. This array is replaced during a strategic merge patch. |
| | |
| **Key**         | PerconaPGCluster.spec.backups.pgbackrest.configuration[index].configMap |
| **Value**       | object |
| **Required**    | false |
| **Example**     | |
| **Description** | configMap information about the configMap data to project |
| | || **Key**         | PerconaPGCluster.spec.backups.pgbackrest.configuration[index].downwardAPI |
| **Value**       | object |
| **Required**    | false |
| **Example**     | |
| **Description** | downwardAPI information about the downwardAPI data to project |
| | || **Key**         | PerconaPGCluster.spec.backups.pgbackrest.configuration[index].secret |
| **Value**       | object |
| **Required**    | false |
| **Example**     | |
| **Description** | secret information about the secret data to project |
| | || **Key**         | PerconaPGCluster.spec.backups.pgbackrest.configuration[index].serviceAccountToken |
| **Value**       | object |
| **Required**    | false |
| **Example**     | |
| **Description** | serviceAccountToken is information about the serviceAccountToken data to project |
| | |
| **Key**         | PerconaPGCluster.spec.backups.pgbackrest.configuration[index].configMap.items |
| **Value**       | []object |
| **Required**    | false |
| **Example**     | |
| **Description** | items if unspecified, each key-value pair in the Data field of the referenced ConfigMap will be projected into the volume as a file whose name is the key and content is the value. If specified, the listed keys will be projected into the specified paths, and unlisted keys will not be present. If a key is specified which is not present in the ConfigMap, the volume setup will error unless it is marked optional. Paths must be relative and may not contain the '..' path or start with '..'. |
| | || **Key**         | PerconaPGCluster.spec.backups.pgbackrest.configuration[index].configMap.name |
| **Value**       | string |
| **Required**    | false |
| **Example**     | |
| **Description** | Name of the referent. More info: https://kubernetes.io/docs/concepts/overview/working-with-objects/names/#names TODO: Add other useful fields. apiVersion, kind, uid? |
| | || **Key**         | PerconaPGCluster.spec.backups.pgbackrest.configuration[index].configMap.optional |
| **Value**       | boolean |
| **Required**    | false |
| **Example**     | |
| **Description** | optional specify whether the ConfigMap or its keys must be defined |
| | |
| **Key**         | PerconaPGCluster.spec.backups.pgbackrest.configuration[index].configMap.items[index].key |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | key is the key to project. |
| | || **Key**         | PerconaPGCluster.spec.backups.pgbackrest.configuration[index].configMap.items[index].path |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | path is the relative path of the file to map the key to. May not be an absolute path. May not contain the path element '..'. May not start with the string '..'. |
| | || **Key**         | PerconaPGCluster.spec.backups.pgbackrest.configuration[index].configMap.items[index].mode |
| **Value**       | integer |
| **Required**    | false |
| **Example**     | |
| **Description** | mode is Optional: mode bits used to set permissions on this file. Must be an octal value between 0000 and 0777 or a decimal value between 0 and 511. YAML accepts both octal and decimal values, JSON requires decimal values for mode bits. If not specified, the volume defaultMode will be used. This might be in conflict with other options that affect the file mode, like fsGroup, and the result can be other mode bits set. |
| | |
| **Key**         | PerconaPGCluster.spec.backups.pgbackrest.configuration[index].downwardAPI.items |
| **Value**       | []object |
| **Required**    | false |
| **Example**     | |
| **Description** | Items is a list of DownwardAPIVolume file |
| | |
| **Key**         | PerconaPGCluster.spec.backups.pgbackrest.configuration[index].downwardAPI.items[index].path |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | Required: Path is  the relative path name of the file to be created. Must not be absolute or contain the '..' path. Must be utf-8 encoded. The first item of the relative path must not start with '..' |
| | || **Key**         | PerconaPGCluster.spec.backups.pgbackrest.configuration[index].downwardAPI.items[index].fieldRef |
| **Value**       | object |
| **Required**    | false |
| **Example**     | |
| **Description** | Required: Selects a field of the pod: only annotations, labels, name and namespace are supported. |
| | || **Key**         | PerconaPGCluster.spec.backups.pgbackrest.configuration[index].downwardAPI.items[index].mode |
| **Value**       | integer |
| **Required**    | false |
| **Example**     | |
| **Description** | Optional: mode bits used to set permissions on this file, must be an octal value between 0000 and 0777 or a decimal value between 0 and 511. YAML accepts both octal and decimal values, JSON requires decimal values for mode bits. If not specified, the volume defaultMode will be used. This might be in conflict with other options that affect the file mode, like fsGroup, and the result can be other mode bits set. |
| | || **Key**         | PerconaPGCluster.spec.backups.pgbackrest.configuration[index].downwardAPI.items[index].resourceFieldRef |
| **Value**       | object |
| **Required**    | false |
| **Example**     | |
| **Description** | Selects a resource of the container: only resources limits and requests (limits.cpu, limits.memory, requests.cpu and requests.memory) are currently supported. |
| | |
| **Key**         | PerconaPGCluster.spec.backups.pgbackrest.configuration[index].downwardAPI.items[index].fieldRef.fieldPath |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | Path of the field to select in the specified API version. |
| | || **Key**         | PerconaPGCluster.spec.backups.pgbackrest.configuration[index].downwardAPI.items[index].fieldRef.apiVersion |
| **Value**       | string |
| **Required**    | false |
| **Example**     | |
| **Description** | Version of the schema the FieldPath is written in terms of, defaults to "v1". |
| | |
| **Key**         | PerconaPGCluster.spec.backups.pgbackrest.configuration[index].downwardAPI.items[index].resourceFieldRef.resource |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | Required: resource to select |
| | || **Key**         | PerconaPGCluster.spec.backups.pgbackrest.configuration[index].downwardAPI.items[index].resourceFieldRef.containerName |
| **Value**       | string |
| **Required**    | false |
| **Example**     | |
| **Description** | Container name: required for volumes, optional for env vars |
| | || **Key**         | PerconaPGCluster.spec.backups.pgbackrest.configuration[index].downwardAPI.items[index].resourceFieldRef.divisor |
| **Value**       | int or string |
| **Required**    | false |
| **Example**     | |
| **Description** | Specifies the output format of the exposed resources, defaults to "1" |
| | |
| **Key**         | PerconaPGCluster.spec.backups.pgbackrest.configuration[index].secret.items |
| **Value**       | []object |
| **Required**    | false |
| **Example**     | |
| **Description** | items if unspecified, each key-value pair in the Data field of the referenced Secret will be projected into the volume as a file whose name is the key and content is the value. If specified, the listed keys will be projected into the specified paths, and unlisted keys will not be present. If a key is specified which is not present in the Secret, the volume setup will error unless it is marked optional. Paths must be relative and may not contain the '..' path or start with '..'. |
| | || **Key**         | PerconaPGCluster.spec.backups.pgbackrest.configuration[index].secret.name |
| **Value**       | string |
| **Required**    | false |
| **Example**     | |
| **Description** | Name of the referent. More info: https://kubernetes.io/docs/concepts/overview/working-with-objects/names/#names TODO: Add other useful fields. apiVersion, kind, uid? |
| | || **Key**         | PerconaPGCluster.spec.backups.pgbackrest.configuration[index].secret.optional |
| **Value**       | boolean |
| **Required**    | false |
| **Example**     | |
| **Description** | optional field specify whether the Secret or its key must be defined |
| | |
| **Key**         | PerconaPGCluster.spec.backups.pgbackrest.configuration[index].secret.items[index].key |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | key is the key to project. |
| | || **Key**         | PerconaPGCluster.spec.backups.pgbackrest.configuration[index].secret.items[index].path |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | path is the relative path of the file to map the key to. May not be an absolute path. May not contain the path element '..'. May not start with the string '..'. |
| | || **Key**         | PerconaPGCluster.spec.backups.pgbackrest.configuration[index].secret.items[index].mode |
| **Value**       | integer |
| **Required**    | false |
| **Example**     | |
| **Description** | mode is Optional: mode bits used to set permissions on this file. Must be an octal value between 0000 and 0777 or a decimal value between 0 and 511. YAML accepts both octal and decimal values, JSON requires decimal values for mode bits. If not specified, the volume defaultMode will be used. This might be in conflict with other options that affect the file mode, like fsGroup, and the result can be other mode bits set. |
| | |
| **Key**         | PerconaPGCluster.spec.backups.pgbackrest.configuration[index].serviceAccountToken.path |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | path is the path relative to the mount point of the file to project the token into. |
| | || **Key**         | PerconaPGCluster.spec.backups.pgbackrest.configuration[index].serviceAccountToken.audience |
| **Value**       | string |
| **Required**    | false |
| **Example**     | |
| **Description** | audience is the intended audience of the token. A recipient of a token must identify itself with an identifier specified in the audience of the token, and otherwise should reject the token. The audience defaults to the identifier of the apiserver. |
| | || **Key**         | PerconaPGCluster.spec.backups.pgbackrest.configuration[index].serviceAccountToken.expirationSeconds |
| **Value**       | integer |
| **Required**    | false |
| **Example**     | |
| **Description** | expirationSeconds is the requested duration of validity of the service account token. As the token approaches expiration, the kubelet volume plugin will proactively rotate the service account token. The kubelet will start trying to rotate the token if the token is older than 80 percent of its time to live or if the token is older than 24 hours.Defaults to 1 hour and must be at least 10 minutes. |
| | |
| **Key**         | PerconaPGCluster.spec.backups.pgbackrest.jobs.affinity |
| **Value**       | object |
| **Required**    | false |
| **Example**     | |
| **Description** | Scheduling constraints of pgBackRest backup Job pods. More info: https://kubernetes.io/docs/concepts/scheduling-eviction/assign-pod-node |
| | || **Key**         | PerconaPGCluster.spec.backups.pgbackrest.jobs.priorityClassName |
| **Value**       | string |
| **Required**    | false |
| **Example**     | |
| **Description** | Priority class name for the pgBackRest backup Job pods. More info: https://kubernetes.io/docs/concepts/scheduling-eviction/pod-priority-preemption/ |
| | || **Key**         | PerconaPGCluster.spec.backups.pgbackrest.jobs.resources |
| **Value**       | object |
| **Required**    | false |
| **Example**     | |
| **Description** | Resource limits for backup jobs. Includes manual, scheduled and replica create backups |
| | || **Key**         | PerconaPGCluster.spec.backups.pgbackrest.jobs.tolerations |
| **Value**       | []object |
| **Required**    | false |
| **Example**     | |
| **Description** | Tolerations of pgBackRest backup Job pods. More info: https://kubernetes.io/docs/concepts/scheduling-eviction/taint-and-toleration |
| | |
| **Key**         | PerconaPGCluster.spec.backups.pgbackrest.jobs.affinity.nodeAffinity |
| **Value**       | object |
| **Required**    | false |
| **Example**     | |
| **Description** | Describes node affinity scheduling rules for the pod. |
| | || **Key**         | PerconaPGCluster.spec.backups.pgbackrest.jobs.affinity.podAffinity |
| **Value**       | object |
| **Required**    | false |
| **Example**     | |
| **Description** | Describes pod affinity scheduling rules (e.g. co-locate this pod in the same node, zone, etc. as some other pod(s)). |
| | || **Key**         | PerconaPGCluster.spec.backups.pgbackrest.jobs.affinity.podAntiAffinity |
| **Value**       | object |
| **Required**    | false |
| **Example**     | |
| **Description** | Describes pod anti-affinity scheduling rules (e.g. avoid putting this pod in the same node, zone, etc. as some other pod(s)). |
| | |
| **Key**         | PerconaPGCluster.spec.backups.pgbackrest.jobs.affinity.nodeAffinity.preferredDuringSchedulingIgnoredDuringExecution |
| **Value**       | []object |
| **Required**    | false |
| **Example**     | |
| **Description** | The scheduler will prefer to schedule pods to nodes that satisfy the affinity expressions specified by this field, but it may choose a node that violates one or more of the expressions. The node that is most preferred is the one with the greatest sum of weights, i.e. for each node that meets all of the scheduling requirements (resource request, requiredDuringScheduling affinity expressions, etc.), compute a sum by iterating through the elements of this field and adding "weight" to the sum if the node matches the corresponding matchExpressions; the node(s) with the highest sum are the most preferred. |
| | || **Key**         | PerconaPGCluster.spec.backups.pgbackrest.jobs.affinity.nodeAffinity.requiredDuringSchedulingIgnoredDuringExecution |
| **Value**       | object |
| **Required**    | false |
| **Example**     | |
| **Description** | If the affinity requirements specified by this field are not met at scheduling time, the pod will not be scheduled onto the node. If the affinity requirements specified by this field cease to be met at some point during pod execution (e.g. due to an update), the system may or may not try to eventually evict the pod from its node. |
| | |
| **Key**         | PerconaPGCluster.spec.backups.pgbackrest.jobs.affinity.nodeAffinity.preferredDuringSchedulingIgnoredDuringExecution[index].preference |
| **Value**       | object |
| **Required**    | true |
| **Example**     | |
| **Description** | A node selector term, associated with the corresponding weight. |
| | || **Key**         | PerconaPGCluster.spec.backups.pgbackrest.jobs.affinity.nodeAffinity.preferredDuringSchedulingIgnoredDuringExecution[index].weight |
| **Value**       | integer |
| **Required**    | true |
| **Example**     | |
| **Description** | Weight associated with matching the corresponding nodeSelectorTerm, in the range 1-100. |
| | |
| **Key**         | PerconaPGCluster.spec.backups.pgbackrest.jobs.affinity.nodeAffinity.preferredDuringSchedulingIgnoredDuringExecution[index].preference.matchExpressions |
| **Value**       | []object |
| **Required**    | false |
| **Example**     | |
| **Description** | A list of node selector requirements by node's labels. |
| | || **Key**         | PerconaPGCluster.spec.backups.pgbackrest.jobs.affinity.nodeAffinity.preferredDuringSchedulingIgnoredDuringExecution[index].preference.matchFields |
| **Value**       | []object |
| **Required**    | false |
| **Example**     | |
| **Description** | A list of node selector requirements by node's fields. |
| | |
| **Key**         | PerconaPGCluster.spec.backups.pgbackrest.jobs.affinity.nodeAffinity.preferredDuringSchedulingIgnoredDuringExecution[index].preference.matchExpressions[index].key |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | The label key that the selector applies to. |
| | || **Key**         | PerconaPGCluster.spec.backups.pgbackrest.jobs.affinity.nodeAffinity.preferredDuringSchedulingIgnoredDuringExecution[index].preference.matchExpressions[index].operator |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | Represents a key's relationship to a set of values. Valid operators are In, NotIn, Exists, DoesNotExist. Gt, and Lt. |
| | || **Key**         | PerconaPGCluster.spec.backups.pgbackrest.jobs.affinity.nodeAffinity.preferredDuringSchedulingIgnoredDuringExecution[index].preference.matchExpressions[index].values |
| **Value**       | []string |
| **Required**    | false |
| **Example**     | |
| **Description** | An array of string values. If the operator is In or NotIn, the values array must be non-empty. If the operator is Exists or DoesNotExist, the values array must be empty. If the operator is Gt or Lt, the values array must have a single element, which will be interpreted as an integer. This array is replaced during a strategic merge patch. |
| | |
| **Key**         | PerconaPGCluster.spec.backups.pgbackrest.jobs.affinity.nodeAffinity.preferredDuringSchedulingIgnoredDuringExecution[index].preference.matchFields[index].key |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | The label key that the selector applies to. |
| | || **Key**         | PerconaPGCluster.spec.backups.pgbackrest.jobs.affinity.nodeAffinity.preferredDuringSchedulingIgnoredDuringExecution[index].preference.matchFields[index].operator |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | Represents a key's relationship to a set of values. Valid operators are In, NotIn, Exists, DoesNotExist. Gt, and Lt. |
| | || **Key**         | PerconaPGCluster.spec.backups.pgbackrest.jobs.affinity.nodeAffinity.preferredDuringSchedulingIgnoredDuringExecution[index].preference.matchFields[index].values |
| **Value**       | []string |
| **Required**    | false |
| **Example**     | |
| **Description** | An array of string values. If the operator is In or NotIn, the values array must be non-empty. If the operator is Exists or DoesNotExist, the values array must be empty. If the operator is Gt or Lt, the values array must have a single element, which will be interpreted as an integer. This array is replaced during a strategic merge patch. |
| | |
| **Key**         | PerconaPGCluster.spec.backups.pgbackrest.jobs.affinity.nodeAffinity.requiredDuringSchedulingIgnoredDuringExecution.nodeSelectorTerms |
| **Value**       | []object |
| **Required**    | true |
| **Example**     | |
| **Description** | Required. A list of node selector terms. The terms are ORed. |
| | |
| **Key**         | PerconaPGCluster.spec.backups.pgbackrest.jobs.affinity.nodeAffinity.requiredDuringSchedulingIgnoredDuringExecution.nodeSelectorTerms[index].matchExpressions |
| **Value**       | []object |
| **Required**    | false |
| **Example**     | |
| **Description** | A list of node selector requirements by node's labels. |
| | || **Key**         | PerconaPGCluster.spec.backups.pgbackrest.jobs.affinity.nodeAffinity.requiredDuringSchedulingIgnoredDuringExecution.nodeSelectorTerms[index].matchFields |
| **Value**       | []object |
| **Required**    | false |
| **Example**     | |
| **Description** | A list of node selector requirements by node's fields. |
| | |
| **Key**         | PerconaPGCluster.spec.backups.pgbackrest.jobs.affinity.nodeAffinity.requiredDuringSchedulingIgnoredDuringExecution.nodeSelectorTerms[index].matchExpressions[index].key |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | The label key that the selector applies to. |
| | || **Key**         | PerconaPGCluster.spec.backups.pgbackrest.jobs.affinity.nodeAffinity.requiredDuringSchedulingIgnoredDuringExecution.nodeSelectorTerms[index].matchExpressions[index].operator |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | Represents a key's relationship to a set of values. Valid operators are In, NotIn, Exists, DoesNotExist. Gt, and Lt. |
| | || **Key**         | PerconaPGCluster.spec.backups.pgbackrest.jobs.affinity.nodeAffinity.requiredDuringSchedulingIgnoredDuringExecution.nodeSelectorTerms[index].matchExpressions[index].values |
| **Value**       | []string |
| **Required**    | false |
| **Example**     | |
| **Description** | An array of string values. If the operator is In or NotIn, the values array must be non-empty. If the operator is Exists or DoesNotExist, the values array must be empty. If the operator is Gt or Lt, the values array must have a single element, which will be interpreted as an integer. This array is replaced during a strategic merge patch. |
| | |
| **Key**         | PerconaPGCluster.spec.backups.pgbackrest.jobs.affinity.nodeAffinity.requiredDuringSchedulingIgnoredDuringExecution.nodeSelectorTerms[index].matchFields[index].key |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | The label key that the selector applies to. |
| | || **Key**         | PerconaPGCluster.spec.backups.pgbackrest.jobs.affinity.nodeAffinity.requiredDuringSchedulingIgnoredDuringExecution.nodeSelectorTerms[index].matchFields[index].operator |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | Represents a key's relationship to a set of values. Valid operators are In, NotIn, Exists, DoesNotExist. Gt, and Lt. |
| | || **Key**         | PerconaPGCluster.spec.backups.pgbackrest.jobs.affinity.nodeAffinity.requiredDuringSchedulingIgnoredDuringExecution.nodeSelectorTerms[index].matchFields[index].values |
| **Value**       | []string |
| **Required**    | false |
| **Example**     | |
| **Description** | An array of string values. If the operator is In or NotIn, the values array must be non-empty. If the operator is Exists or DoesNotExist, the values array must be empty. If the operator is Gt or Lt, the values array must have a single element, which will be interpreted as an integer. This array is replaced during a strategic merge patch. |
| | |
| **Key**         | PerconaPGCluster.spec.backups.pgbackrest.jobs.affinity.podAffinity.preferredDuringSchedulingIgnoredDuringExecution |
| **Value**       | []object |
| **Required**    | false |
| **Example**     | |
| **Description** | The scheduler will prefer to schedule pods to nodes that satisfy the affinity expressions specified by this field, but it may choose a node that violates one or more of the expressions. The node that is most preferred is the one with the greatest sum of weights, i.e. for each node that meets all of the scheduling requirements (resource request, requiredDuringScheduling affinity expressions, etc.), compute a sum by iterating through the elements of this field and adding "weight" to the sum if the node has pods which matches the corresponding podAffinityTerm; the node(s) with the highest sum are the most preferred. |
| | || **Key**         | PerconaPGCluster.spec.backups.pgbackrest.jobs.affinity.podAffinity.requiredDuringSchedulingIgnoredDuringExecution |
| **Value**       | []object |
| **Required**    | false |
| **Example**     | |
| **Description** | If the affinity requirements specified by this field are not met at scheduling time, the pod will not be scheduled onto the node. If the affinity requirements specified by this field cease to be met at some point during pod execution (e.g. due to a pod label update), the system may or may not try to eventually evict the pod from its node. When there are multiple elements, the lists of nodes corresponding to each podAffinityTerm are intersected, i.e. all terms must be satisfied. |
| | |
| **Key**         | PerconaPGCluster.spec.backups.pgbackrest.jobs.affinity.podAffinity.preferredDuringSchedulingIgnoredDuringExecution[index].podAffinityTerm |
| **Value**       | object |
| **Required**    | true |
| **Example**     | |
| **Description** | Required. A pod affinity term, associated with the corresponding weight. |
| | || **Key**         | PerconaPGCluster.spec.backups.pgbackrest.jobs.affinity.podAffinity.preferredDuringSchedulingIgnoredDuringExecution[index].weight |
| **Value**       | integer |
| **Required**    | true |
| **Example**     | |
| **Description** | weight associated with matching the corresponding podAffinityTerm, in the range 1-100. |
| | |
| **Key**         | PerconaPGCluster.spec.backups.pgbackrest.jobs.affinity.podAffinity.preferredDuringSchedulingIgnoredDuringExecution[index].podAffinityTerm.topologyKey |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | This pod should be co-located (affinity) or not co-located (anti-affinity) with the pods matching the labelSelector in the specified namespaces, where co-located is defined as running on a node whose value of the label with key topologyKey matches that of any node on which any of the selected pods is running. Empty topologyKey is not allowed. |
| | || **Key**         | PerconaPGCluster.spec.backups.pgbackrest.jobs.affinity.podAffinity.preferredDuringSchedulingIgnoredDuringExecution[index].podAffinityTerm.labelSelector |
| **Value**       | object |
| **Required**    | false |
| **Example**     | |
| **Description** | A label query over a set of resources, in this case pods. |
| | || **Key**         | PerconaPGCluster.spec.backups.pgbackrest.jobs.affinity.podAffinity.preferredDuringSchedulingIgnoredDuringExecution[index].podAffinityTerm.namespaceSelector |
| **Value**       | object |
| **Required**    | false |
| **Example**     | |
| **Description** | A label query over the set of namespaces that the term applies to. The term is applied to the union of the namespaces selected by this field and the ones listed in the namespaces field. null selector and null or empty namespaces list means "this pod's namespace". An empty selector ({}) matches all namespaces. |
| | || **Key**         | PerconaPGCluster.spec.backups.pgbackrest.jobs.affinity.podAffinity.preferredDuringSchedulingIgnoredDuringExecution[index].podAffinityTerm.namespaces |
| **Value**       | []string |
| **Required**    | false |
| **Example**     | |
| **Description** | namespaces specifies a static list of namespace names that the term applies to. The term is applied to the union of the namespaces listed in this field and the ones selected by namespaceSelector. null or empty namespaces list and null namespaceSelector means "this pod's namespace". |
| | |
| **Key**         | PerconaPGCluster.spec.backups.pgbackrest.jobs.affinity.podAffinity.preferredDuringSchedulingIgnoredDuringExecution[index].podAffinityTerm.labelSelector.matchExpressions |
| **Value**       | []object |
| **Required**    | false |
| **Example**     | |
| **Description** | matchExpressions is a list of label selector requirements. The requirements are ANDed. |
| | || **Key**         | PerconaPGCluster.spec.backups.pgbackrest.jobs.affinity.podAffinity.preferredDuringSchedulingIgnoredDuringExecution[index].podAffinityTerm.labelSelector.matchLabels |
| **Value**       | map[string]string |
| **Required**    | false |
| **Example**     | |
| **Description** | matchLabels is a map of {key,value} pairs. A single {key,value} in the matchLabels map is equivalent to an element of matchExpressions, whose key field is "key", the operator is "In", and the values array contains only "value". The requirements are ANDed. |
| | |
| **Key**         | PerconaPGCluster.spec.backups.pgbackrest.jobs.affinity.podAffinity.preferredDuringSchedulingIgnoredDuringExecution[index].podAffinityTerm.labelSelector.matchExpressions[index].key |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | key is the label key that the selector applies to. |
| | || **Key**         | PerconaPGCluster.spec.backups.pgbackrest.jobs.affinity.podAffinity.preferredDuringSchedulingIgnoredDuringExecution[index].podAffinityTerm.labelSelector.matchExpressions[index].operator |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | operator represents a key's relationship to a set of values. Valid operators are In, NotIn, Exists and DoesNotExist. |
| | || **Key**         | PerconaPGCluster.spec.backups.pgbackrest.jobs.affinity.podAffinity.preferredDuringSchedulingIgnoredDuringExecution[index].podAffinityTerm.labelSelector.matchExpressions[index].values |
| **Value**       | []string |
| **Required**    | false |
| **Example**     | |
| **Description** | values is an array of string values. If the operator is In or NotIn, the values array must be non-empty. If the operator is Exists or DoesNotExist, the values array must be empty. This array is replaced during a strategic merge patch. |
| | |
| **Key**         | PerconaPGCluster.spec.backups.pgbackrest.jobs.affinity.podAffinity.preferredDuringSchedulingIgnoredDuringExecution[index].podAffinityTerm.namespaceSelector.matchExpressions |
| **Value**       | []object |
| **Required**    | false |
| **Example**     | |
| **Description** | matchExpressions is a list of label selector requirements. The requirements are ANDed. |
| | || **Key**         | PerconaPGCluster.spec.backups.pgbackrest.jobs.affinity.podAffinity.preferredDuringSchedulingIgnoredDuringExecution[index].podAffinityTerm.namespaceSelector.matchLabels |
| **Value**       | map[string]string |
| **Required**    | false |
| **Example**     | |
| **Description** | matchLabels is a map of {key,value} pairs. A single {key,value} in the matchLabels map is equivalent to an element of matchExpressions, whose key field is "key", the operator is "In", and the values array contains only "value". The requirements are ANDed. |
| | |
| **Key**         | PerconaPGCluster.spec.backups.pgbackrest.jobs.affinity.podAffinity.preferredDuringSchedulingIgnoredDuringExecution[index].podAffinityTerm.namespaceSelector.matchExpressions[index].key |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | key is the label key that the selector applies to. |
| | || **Key**         | PerconaPGCluster.spec.backups.pgbackrest.jobs.affinity.podAffinity.preferredDuringSchedulingIgnoredDuringExecution[index].podAffinityTerm.namespaceSelector.matchExpressions[index].operator |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | operator represents a key's relationship to a set of values. Valid operators are In, NotIn, Exists and DoesNotExist. |
| | || **Key**         | PerconaPGCluster.spec.backups.pgbackrest.jobs.affinity.podAffinity.preferredDuringSchedulingIgnoredDuringExecution[index].podAffinityTerm.namespaceSelector.matchExpressions[index].values |
| **Value**       | []string |
| **Required**    | false |
| **Example**     | |
| **Description** | values is an array of string values. If the operator is In or NotIn, the values array must be non-empty. If the operator is Exists or DoesNotExist, the values array must be empty. This array is replaced during a strategic merge patch. |
| | |
| **Key**         | PerconaPGCluster.spec.backups.pgbackrest.jobs.affinity.podAffinity.requiredDuringSchedulingIgnoredDuringExecution[index].topologyKey |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | This pod should be co-located (affinity) or not co-located (anti-affinity) with the pods matching the labelSelector in the specified namespaces, where co-located is defined as running on a node whose value of the label with key topologyKey matches that of any node on which any of the selected pods is running. Empty topologyKey is not allowed. |
| | || **Key**         | PerconaPGCluster.spec.backups.pgbackrest.jobs.affinity.podAffinity.requiredDuringSchedulingIgnoredDuringExecution[index].labelSelector |
| **Value**       | object |
| **Required**    | false |
| **Example**     | |
| **Description** | A label query over a set of resources, in this case pods. |
| | || **Key**         | PerconaPGCluster.spec.backups.pgbackrest.jobs.affinity.podAffinity.requiredDuringSchedulingIgnoredDuringExecution[index].namespaceSelector |
| **Value**       | object |
| **Required**    | false |
| **Example**     | |
| **Description** | A label query over the set of namespaces that the term applies to. The term is applied to the union of the namespaces selected by this field and the ones listed in the namespaces field. null selector and null or empty namespaces list means "this pod's namespace". An empty selector ({}) matches all namespaces. |
| | || **Key**         | PerconaPGCluster.spec.backups.pgbackrest.jobs.affinity.podAffinity.requiredDuringSchedulingIgnoredDuringExecution[index].namespaces |
| **Value**       | []string |
| **Required**    | false |
| **Example**     | |
| **Description** | namespaces specifies a static list of namespace names that the term applies to. The term is applied to the union of the namespaces listed in this field and the ones selected by namespaceSelector. null or empty namespaces list and null namespaceSelector means "this pod's namespace". |
| | |
| **Key**         | PerconaPGCluster.spec.backups.pgbackrest.jobs.affinity.podAffinity.requiredDuringSchedulingIgnoredDuringExecution[index].labelSelector.matchExpressions |
| **Value**       | []object |
| **Required**    | false |
| **Example**     | |
| **Description** | matchExpressions is a list of label selector requirements. The requirements are ANDed. |
| | || **Key**         | PerconaPGCluster.spec.backups.pgbackrest.jobs.affinity.podAffinity.requiredDuringSchedulingIgnoredDuringExecution[index].labelSelector.matchLabels |
| **Value**       | map[string]string |
| **Required**    | false |
| **Example**     | |
| **Description** | matchLabels is a map of {key,value} pairs. A single {key,value} in the matchLabels map is equivalent to an element of matchExpressions, whose key field is "key", the operator is "In", and the values array contains only "value". The requirements are ANDed. |
| | |
| **Key**         | PerconaPGCluster.spec.backups.pgbackrest.jobs.affinity.podAffinity.requiredDuringSchedulingIgnoredDuringExecution[index].labelSelector.matchExpressions[index].key |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | key is the label key that the selector applies to. |
| | || **Key**         | PerconaPGCluster.spec.backups.pgbackrest.jobs.affinity.podAffinity.requiredDuringSchedulingIgnoredDuringExecution[index].labelSelector.matchExpressions[index].operator |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | operator represents a key's relationship to a set of values. Valid operators are In, NotIn, Exists and DoesNotExist. |
| | || **Key**         | PerconaPGCluster.spec.backups.pgbackrest.jobs.affinity.podAffinity.requiredDuringSchedulingIgnoredDuringExecution[index].labelSelector.matchExpressions[index].values |
| **Value**       | []string |
| **Required**    | false |
| **Example**     | |
| **Description** | values is an array of string values. If the operator is In or NotIn, the values array must be non-empty. If the operator is Exists or DoesNotExist, the values array must be empty. This array is replaced during a strategic merge patch. |
| | |
| **Key**         | PerconaPGCluster.spec.backups.pgbackrest.jobs.affinity.podAffinity.requiredDuringSchedulingIgnoredDuringExecution[index].namespaceSelector.matchExpressions |
| **Value**       | []object |
| **Required**    | false |
| **Example**     | |
| **Description** | matchExpressions is a list of label selector requirements. The requirements are ANDed. |
| | || **Key**         | PerconaPGCluster.spec.backups.pgbackrest.jobs.affinity.podAffinity.requiredDuringSchedulingIgnoredDuringExecution[index].namespaceSelector.matchLabels |
| **Value**       | map[string]string |
| **Required**    | false |
| **Example**     | |
| **Description** | matchLabels is a map of {key,value} pairs. A single {key,value} in the matchLabels map is equivalent to an element of matchExpressions, whose key field is "key", the operator is "In", and the values array contains only "value". The requirements are ANDed. |
| | |
| **Key**         | PerconaPGCluster.spec.backups.pgbackrest.jobs.affinity.podAffinity.requiredDuringSchedulingIgnoredDuringExecution[index].namespaceSelector.matchExpressions[index].key |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | key is the label key that the selector applies to. |
| | || **Key**         | PerconaPGCluster.spec.backups.pgbackrest.jobs.affinity.podAffinity.requiredDuringSchedulingIgnoredDuringExecution[index].namespaceSelector.matchExpressions[index].operator |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | operator represents a key's relationship to a set of values. Valid operators are In, NotIn, Exists and DoesNotExist. |
| | || **Key**         | PerconaPGCluster.spec.backups.pgbackrest.jobs.affinity.podAffinity.requiredDuringSchedulingIgnoredDuringExecution[index].namespaceSelector.matchExpressions[index].values |
| **Value**       | []string |
| **Required**    | false |
| **Example**     | |
| **Description** | values is an array of string values. If the operator is In or NotIn, the values array must be non-empty. If the operator is Exists or DoesNotExist, the values array must be empty. This array is replaced during a strategic merge patch. |
| | |
| **Key**         | PerconaPGCluster.spec.backups.pgbackrest.jobs.affinity.podAntiAffinity.preferredDuringSchedulingIgnoredDuringExecution |
| **Value**       | []object |
| **Required**    | false |
| **Example**     | |
| **Description** | The scheduler will prefer to schedule pods to nodes that satisfy the anti-affinity expressions specified by this field, but it may choose a node that violates one or more of the expressions. The node that is most preferred is the one with the greatest sum of weights, i.e. for each node that meets all of the scheduling requirements (resource request, requiredDuringScheduling anti-affinity expressions, etc.), compute a sum by iterating through the elements of this field and adding "weight" to the sum if the node has pods which matches the corresponding podAffinityTerm; the node(s) with the highest sum are the most preferred. |
| | || **Key**         | PerconaPGCluster.spec.backups.pgbackrest.jobs.affinity.podAntiAffinity.requiredDuringSchedulingIgnoredDuringExecution |
| **Value**       | []object |
| **Required**    | false |
| **Example**     | |
| **Description** | If the anti-affinity requirements specified by this field are not met at scheduling time, the pod will not be scheduled onto the node. If the anti-affinity requirements specified by this field cease to be met at some point during pod execution (e.g. due to a pod label update), the system may or may not try to eventually evict the pod from its node. When there are multiple elements, the lists of nodes corresponding to each podAffinityTerm are intersected, i.e. all terms must be satisfied. |
| | |
| **Key**         | PerconaPGCluster.spec.backups.pgbackrest.jobs.affinity.podAntiAffinity.preferredDuringSchedulingIgnoredDuringExecution[index].podAffinityTerm |
| **Value**       | object |
| **Required**    | true |
| **Example**     | |
| **Description** | Required. A pod affinity term, associated with the corresponding weight. |
| | || **Key**         | PerconaPGCluster.spec.backups.pgbackrest.jobs.affinity.podAntiAffinity.preferredDuringSchedulingIgnoredDuringExecution[index].weight |
| **Value**       | integer |
| **Required**    | true |
| **Example**     | |
| **Description** | weight associated with matching the corresponding podAffinityTerm, in the range 1-100. |
| | |
| **Key**         | PerconaPGCluster.spec.backups.pgbackrest.jobs.affinity.podAntiAffinity.preferredDuringSchedulingIgnoredDuringExecution[index].podAffinityTerm.topologyKey |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | This pod should be co-located (affinity) or not co-located (anti-affinity) with the pods matching the labelSelector in the specified namespaces, where co-located is defined as running on a node whose value of the label with key topologyKey matches that of any node on which any of the selected pods is running. Empty topologyKey is not allowed. |
| | || **Key**         | PerconaPGCluster.spec.backups.pgbackrest.jobs.affinity.podAntiAffinity.preferredDuringSchedulingIgnoredDuringExecution[index].podAffinityTerm.labelSelector |
| **Value**       | object |
| **Required**    | false |
| **Example**     | |
| **Description** | A label query over a set of resources, in this case pods. |
| | || **Key**         | PerconaPGCluster.spec.backups.pgbackrest.jobs.affinity.podAntiAffinity.preferredDuringSchedulingIgnoredDuringExecution[index].podAffinityTerm.namespaceSelector |
| **Value**       | object |
| **Required**    | false |
| **Example**     | |
| **Description** | A label query over the set of namespaces that the term applies to. The term is applied to the union of the namespaces selected by this field and the ones listed in the namespaces field. null selector and null or empty namespaces list means "this pod's namespace". An empty selector ({}) matches all namespaces. |
| | || **Key**         | PerconaPGCluster.spec.backups.pgbackrest.jobs.affinity.podAntiAffinity.preferredDuringSchedulingIgnoredDuringExecution[index].podAffinityTerm.namespaces |
| **Value**       | []string |
| **Required**    | false |
| **Example**     | |
| **Description** | namespaces specifies a static list of namespace names that the term applies to. The term is applied to the union of the namespaces listed in this field and the ones selected by namespaceSelector. null or empty namespaces list and null namespaceSelector means "this pod's namespace". |
| | |
| **Key**         | PerconaPGCluster.spec.backups.pgbackrest.jobs.affinity.podAntiAffinity.preferredDuringSchedulingIgnoredDuringExecution[index].podAffinityTerm.labelSelector.matchExpressions |
| **Value**       | []object |
| **Required**    | false |
| **Example**     | |
| **Description** | matchExpressions is a list of label selector requirements. The requirements are ANDed. |
| | || **Key**         | PerconaPGCluster.spec.backups.pgbackrest.jobs.affinity.podAntiAffinity.preferredDuringSchedulingIgnoredDuringExecution[index].podAffinityTerm.labelSelector.matchLabels |
| **Value**       | map[string]string |
| **Required**    | false |
| **Example**     | |
| **Description** | matchLabels is a map of {key,value} pairs. A single {key,value} in the matchLabels map is equivalent to an element of matchExpressions, whose key field is "key", the operator is "In", and the values array contains only "value". The requirements are ANDed. |
| | |
| **Key**         | PerconaPGCluster.spec.backups.pgbackrest.jobs.affinity.podAntiAffinity.preferredDuringSchedulingIgnoredDuringExecution[index].podAffinityTerm.labelSelector.matchExpressions[index].key |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | key is the label key that the selector applies to. |
| | || **Key**         | PerconaPGCluster.spec.backups.pgbackrest.jobs.affinity.podAntiAffinity.preferredDuringSchedulingIgnoredDuringExecution[index].podAffinityTerm.labelSelector.matchExpressions[index].operator |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | operator represents a key's relationship to a set of values. Valid operators are In, NotIn, Exists and DoesNotExist. |
| | || **Key**         | PerconaPGCluster.spec.backups.pgbackrest.jobs.affinity.podAntiAffinity.preferredDuringSchedulingIgnoredDuringExecution[index].podAffinityTerm.labelSelector.matchExpressions[index].values |
| **Value**       | []string |
| **Required**    | false |
| **Example**     | |
| **Description** | values is an array of string values. If the operator is In or NotIn, the values array must be non-empty. If the operator is Exists or DoesNotExist, the values array must be empty. This array is replaced during a strategic merge patch. |
| | |
| **Key**         | PerconaPGCluster.spec.backups.pgbackrest.jobs.affinity.podAntiAffinity.preferredDuringSchedulingIgnoredDuringExecution[index].podAffinityTerm.namespaceSelector.matchExpressions |
| **Value**       | []object |
| **Required**    | false |
| **Example**     | |
| **Description** | matchExpressions is a list of label selector requirements. The requirements are ANDed. |
| | || **Key**         | PerconaPGCluster.spec.backups.pgbackrest.jobs.affinity.podAntiAffinity.preferredDuringSchedulingIgnoredDuringExecution[index].podAffinityTerm.namespaceSelector.matchLabels |
| **Value**       | map[string]string |
| **Required**    | false |
| **Example**     | |
| **Description** | matchLabels is a map of {key,value} pairs. A single {key,value} in the matchLabels map is equivalent to an element of matchExpressions, whose key field is "key", the operator is "In", and the values array contains only "value". The requirements are ANDed. |
| | |
| **Key**         | PerconaPGCluster.spec.backups.pgbackrest.jobs.affinity.podAntiAffinity.preferredDuringSchedulingIgnoredDuringExecution[index].podAffinityTerm.namespaceSelector.matchExpressions[index].key |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | key is the label key that the selector applies to. |
| | || **Key**         | PerconaPGCluster.spec.backups.pgbackrest.jobs.affinity.podAntiAffinity.preferredDuringSchedulingIgnoredDuringExecution[index].podAffinityTerm.namespaceSelector.matchExpressions[index].operator |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | operator represents a key's relationship to a set of values. Valid operators are In, NotIn, Exists and DoesNotExist. |
| | || **Key**         | PerconaPGCluster.spec.backups.pgbackrest.jobs.affinity.podAntiAffinity.preferredDuringSchedulingIgnoredDuringExecution[index].podAffinityTerm.namespaceSelector.matchExpressions[index].values |
| **Value**       | []string |
| **Required**    | false |
| **Example**     | |
| **Description** | values is an array of string values. If the operator is In or NotIn, the values array must be non-empty. If the operator is Exists or DoesNotExist, the values array must be empty. This array is replaced during a strategic merge patch. |
| | |
| **Key**         | PerconaPGCluster.spec.backups.pgbackrest.jobs.affinity.podAntiAffinity.requiredDuringSchedulingIgnoredDuringExecution[index].topologyKey |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | This pod should be co-located (affinity) or not co-located (anti-affinity) with the pods matching the labelSelector in the specified namespaces, where co-located is defined as running on a node whose value of the label with key topologyKey matches that of any node on which any of the selected pods is running. Empty topologyKey is not allowed. |
| | || **Key**         | PerconaPGCluster.spec.backups.pgbackrest.jobs.affinity.podAntiAffinity.requiredDuringSchedulingIgnoredDuringExecution[index].labelSelector |
| **Value**       | object |
| **Required**    | false |
| **Example**     | |
| **Description** | A label query over a set of resources, in this case pods. |
| | || **Key**         | PerconaPGCluster.spec.backups.pgbackrest.jobs.affinity.podAntiAffinity.requiredDuringSchedulingIgnoredDuringExecution[index].namespaceSelector |
| **Value**       | object |
| **Required**    | false |
| **Example**     | |
| **Description** | A label query over the set of namespaces that the term applies to. The term is applied to the union of the namespaces selected by this field and the ones listed in the namespaces field. null selector and null or empty namespaces list means "this pod's namespace". An empty selector ({}) matches all namespaces. |
| | || **Key**         | PerconaPGCluster.spec.backups.pgbackrest.jobs.affinity.podAntiAffinity.requiredDuringSchedulingIgnoredDuringExecution[index].namespaces |
| **Value**       | []string |
| **Required**    | false |
| **Example**     | |
| **Description** | namespaces specifies a static list of namespace names that the term applies to. The term is applied to the union of the namespaces listed in this field and the ones selected by namespaceSelector. null or empty namespaces list and null namespaceSelector means "this pod's namespace". |
| | |
| **Key**         | PerconaPGCluster.spec.backups.pgbackrest.jobs.affinity.podAntiAffinity.requiredDuringSchedulingIgnoredDuringExecution[index].labelSelector.matchExpressions |
| **Value**       | []object |
| **Required**    | false |
| **Example**     | |
| **Description** | matchExpressions is a list of label selector requirements. The requirements are ANDed. |
| | || **Key**         | PerconaPGCluster.spec.backups.pgbackrest.jobs.affinity.podAntiAffinity.requiredDuringSchedulingIgnoredDuringExecution[index].labelSelector.matchLabels |
| **Value**       | map[string]string |
| **Required**    | false |
| **Example**     | |
| **Description** | matchLabels is a map of {key,value} pairs. A single {key,value} in the matchLabels map is equivalent to an element of matchExpressions, whose key field is "key", the operator is "In", and the values array contains only "value". The requirements are ANDed. |
| | |
| **Key**         | PerconaPGCluster.spec.backups.pgbackrest.jobs.affinity.podAntiAffinity.requiredDuringSchedulingIgnoredDuringExecution[index].labelSelector.matchExpressions[index].key |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | key is the label key that the selector applies to. |
| | || **Key**         | PerconaPGCluster.spec.backups.pgbackrest.jobs.affinity.podAntiAffinity.requiredDuringSchedulingIgnoredDuringExecution[index].labelSelector.matchExpressions[index].operator |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | operator represents a key's relationship to a set of values. Valid operators are In, NotIn, Exists and DoesNotExist. |
| | || **Key**         | PerconaPGCluster.spec.backups.pgbackrest.jobs.affinity.podAntiAffinity.requiredDuringSchedulingIgnoredDuringExecution[index].labelSelector.matchExpressions[index].values |
| **Value**       | []string |
| **Required**    | false |
| **Example**     | |
| **Description** | values is an array of string values. If the operator is In or NotIn, the values array must be non-empty. If the operator is Exists or DoesNotExist, the values array must be empty. This array is replaced during a strategic merge patch. |
| | |
| **Key**         | PerconaPGCluster.spec.backups.pgbackrest.jobs.affinity.podAntiAffinity.requiredDuringSchedulingIgnoredDuringExecution[index].namespaceSelector.matchExpressions |
| **Value**       | []object |
| **Required**    | false |
| **Example**     | |
| **Description** | matchExpressions is a list of label selector requirements. The requirements are ANDed. |
| | || **Key**         | PerconaPGCluster.spec.backups.pgbackrest.jobs.affinity.podAntiAffinity.requiredDuringSchedulingIgnoredDuringExecution[index].namespaceSelector.matchLabels |
| **Value**       | map[string]string |
| **Required**    | false |
| **Example**     | |
| **Description** | matchLabels is a map of {key,value} pairs. A single {key,value} in the matchLabels map is equivalent to an element of matchExpressions, whose key field is "key", the operator is "In", and the values array contains only "value". The requirements are ANDed. |
| | |
| **Key**         | PerconaPGCluster.spec.backups.pgbackrest.jobs.affinity.podAntiAffinity.requiredDuringSchedulingIgnoredDuringExecution[index].namespaceSelector.matchExpressions[index].key |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | key is the label key that the selector applies to. |
| | || **Key**         | PerconaPGCluster.spec.backups.pgbackrest.jobs.affinity.podAntiAffinity.requiredDuringSchedulingIgnoredDuringExecution[index].namespaceSelector.matchExpressions[index].operator |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | operator represents a key's relationship to a set of values. Valid operators are In, NotIn, Exists and DoesNotExist. |
| | || **Key**         | PerconaPGCluster.spec.backups.pgbackrest.jobs.affinity.podAntiAffinity.requiredDuringSchedulingIgnoredDuringExecution[index].namespaceSelector.matchExpressions[index].values |
| **Value**       | []string |
| **Required**    | false |
| **Example**     | |
| **Description** | values is an array of string values. If the operator is In or NotIn, the values array must be non-empty. If the operator is Exists or DoesNotExist, the values array must be empty. This array is replaced during a strategic merge patch. |
| | |
| **Key**         | PerconaPGCluster.spec.backups.pgbackrest.jobs.resources.limits |
| **Value**       | map[string]int or string |
| **Required**    | false |
| **Example**     | |
| **Description** | Limits describes the maximum amount of compute resources allowed. More info: https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/ |
| | || **Key**         | PerconaPGCluster.spec.backups.pgbackrest.jobs.resources.requests |
| **Value**       | map[string]int or string |
| **Required**    | false |
| **Example**     | |
| **Description** | Requests describes the minimum amount of compute resources required. If Requests is omitted for a container, it defaults to Limits if that is explicitly specified, otherwise to an implementation-defined value. More info: https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/ |
| | |
| **Key**         | PerconaPGCluster.spec.backups.pgbackrest.jobs.tolerations[index].effect |
| **Value**       | string |
| **Required**    | false |
| **Example**     | |
| **Description** | Effect indicates the taint effect to match. Empty means match all taint effects. When specified, allowed values are NoSchedule, PreferNoSchedule and NoExecute. |
| | || **Key**         | PerconaPGCluster.spec.backups.pgbackrest.jobs.tolerations[index].key |
| **Value**       | string |
| **Required**    | false |
| **Example**     | |
| **Description** | Key is the taint key that the toleration applies to. Empty means match all taint keys. If the key is empty, operator must be Exists; this combination means to match all values and all keys. |
| | || **Key**         | PerconaPGCluster.spec.backups.pgbackrest.jobs.tolerations[index].operator |
| **Value**       | string |
| **Required**    | false |
| **Example**     | |
| **Description** | Operator represents a key's relationship to the value. Valid operators are Exists and Equal. Defaults to Equal. Exists is equivalent to wildcard for value, so that a pod can tolerate all taints of a particular category. |
| | || **Key**         | PerconaPGCluster.spec.backups.pgbackrest.jobs.tolerations[index].tolerationSeconds |
| **Value**       | integer |
| **Required**    | false |
| **Example**     | |
| **Description** | TolerationSeconds represents the period of time the toleration (which must be of effect NoExecute, otherwise this field is ignored) tolerates the taint. By default, it is not set, which means tolerate the taint forever (do not evict). Zero and negative values will be treated as 0 (evict immediately) by the system. |
| | || **Key**         | PerconaPGCluster.spec.backups.pgbackrest.jobs.tolerations[index].value |
| **Value**       | string |
| **Required**    | false |
| **Example**     | |
| **Description** | Value is the taint value the toleration matches to. If the operator is Exists, the value should be empty, otherwise just a regular string. |
| | |
| **Key**         | PerconaPGCluster.spec.backups.pgbackrest.manual.repoName |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | The name of the pgBackRest repo to run the backup command against. |
| | || **Key**         | PerconaPGCluster.spec.backups.pgbackrest.manual.options |
| **Value**       | []string |
| **Required**    | false |
| **Example**     | |
| **Description** | Command line options to include when running the pgBackRest backup command. https://pgbackrest.org/command.html#command-backup |
| | |
| **Key**         | PerconaPGCluster.spec.backups.pgbackrest.metadata.annotations |
| **Value**       | map[string]string |
| **Required**    | false |
| **Example**     | |
| **Description** |  |
| | || **Key**         | PerconaPGCluster.spec.backups.pgbackrest.metadata.labels |
| **Value**       | map[string]string |
| **Required**    | false |
| **Example**     | |
| **Description** |  |
| | |
| **Key**         | PerconaPGCluster.spec.backups.pgbackrest.repoHost.affinity |
| **Value**       | object |
| **Required**    | false |
| **Example**     | |
| **Description** | Scheduling constraints of the Dedicated repo host pod. Changing this value causes repo host to restart. More info: https://kubernetes.io/docs/concepts/scheduling-eviction/assign-pod-node |
| | || **Key**         | PerconaPGCluster.spec.backups.pgbackrest.repoHost.priorityClassName |
| **Value**       | string |
| **Required**    | false |
| **Example**     | |
| **Description** | Priority class name for the pgBackRest repo host pod. Changing this value causes PostgreSQL to restart. More info: https://kubernetes.io/docs/concepts/scheduling-eviction/pod-priority-preemption/ |
| | || **Key**         | PerconaPGCluster.spec.backups.pgbackrest.repoHost.resources |
| **Value**       | object |
| **Required**    | false |
| **Example**     | |
| **Description** | Resource requirements for a pgBackRest repository host |
| | || **Key**         | PerconaPGCluster.spec.backups.pgbackrest.repoHost.sshConfigMap |
| **Value**       | object |
| **Required**    | false |
| **Example**     | |
| **Description** | ConfigMap containing custom SSH configuration. Deprecated: Repository hosts use mTLS for encryption, authentication, and authorization. |
| | || **Key**         | PerconaPGCluster.spec.backups.pgbackrest.repoHost.sshSecret |
| **Value**       | object |
| **Required**    | false |
| **Example**     | |
| **Description** | Secret containing custom SSH keys. Deprecated: Repository hosts use mTLS for encryption, authentication, and authorization. |
| | || **Key**         | PerconaPGCluster.spec.backups.pgbackrest.repoHost.tolerations |
| **Value**       | []object |
| **Required**    | false |
| **Example**     | |
| **Description** | Tolerations of a PgBackRest repo host pod. Changing this value causes a restart. More info: https://kubernetes.io/docs/concepts/scheduling-eviction/taint-and-toleration |
| | || **Key**         | PerconaPGCluster.spec.backups.pgbackrest.repoHost.topologySpreadConstraints |
| **Value**       | []object |
| **Required**    | false |
| **Example**     | |
| **Description** | Topology spread constraints of a Dedicated repo host pod. Changing this value causes the repo host to restart. More info: https://kubernetes.io/docs/concepts/workloads/pods/pod-topology-spread-constraints/ |
| | |
| **Key**         | PerconaPGCluster.spec.backups.pgbackrest.repoHost.affinity.nodeAffinity |
| **Value**       | object |
| **Required**    | false |
| **Example**     | |
| **Description** | Describes node affinity scheduling rules for the pod. |
| | || **Key**         | PerconaPGCluster.spec.backups.pgbackrest.repoHost.affinity.podAffinity |
| **Value**       | object |
| **Required**    | false |
| **Example**     | |
| **Description** | Describes pod affinity scheduling rules (e.g. co-locate this pod in the same node, zone, etc. as some other pod(s)). |
| | || **Key**         | PerconaPGCluster.spec.backups.pgbackrest.repoHost.affinity.podAntiAffinity |
| **Value**       | object |
| **Required**    | false |
| **Example**     | |
| **Description** | Describes pod anti-affinity scheduling rules (e.g. avoid putting this pod in the same node, zone, etc. as some other pod(s)). |
| | |
| **Key**         | PerconaPGCluster.spec.backups.pgbackrest.repoHost.affinity.nodeAffinity.preferredDuringSchedulingIgnoredDuringExecution |
| **Value**       | []object |
| **Required**    | false |
| **Example**     | |
| **Description** | The scheduler will prefer to schedule pods to nodes that satisfy the affinity expressions specified by this field, but it may choose a node that violates one or more of the expressions. The node that is most preferred is the one with the greatest sum of weights, i.e. for each node that meets all of the scheduling requirements (resource request, requiredDuringScheduling affinity expressions, etc.), compute a sum by iterating through the elements of this field and adding "weight" to the sum if the node matches the corresponding matchExpressions; the node(s) with the highest sum are the most preferred. |
| | || **Key**         | PerconaPGCluster.spec.backups.pgbackrest.repoHost.affinity.nodeAffinity.requiredDuringSchedulingIgnoredDuringExecution |
| **Value**       | object |
| **Required**    | false |
| **Example**     | |
| **Description** | If the affinity requirements specified by this field are not met at scheduling time, the pod will not be scheduled onto the node. If the affinity requirements specified by this field cease to be met at some point during pod execution (e.g. due to an update), the system may or may not try to eventually evict the pod from its node. |
| | |
| **Key**         | PerconaPGCluster.spec.backups.pgbackrest.repoHost.affinity.nodeAffinity.preferredDuringSchedulingIgnoredDuringExecution[index].preference |
| **Value**       | object |
| **Required**    | true |
| **Example**     | |
| **Description** | A node selector term, associated with the corresponding weight. |
| | || **Key**         | PerconaPGCluster.spec.backups.pgbackrest.repoHost.affinity.nodeAffinity.preferredDuringSchedulingIgnoredDuringExecution[index].weight |
| **Value**       | integer |
| **Required**    | true |
| **Example**     | |
| **Description** | Weight associated with matching the corresponding nodeSelectorTerm, in the range 1-100. |
| | |
| **Key**         | PerconaPGCluster.spec.backups.pgbackrest.repoHost.affinity.nodeAffinity.preferredDuringSchedulingIgnoredDuringExecution[index].preference.matchExpressions |
| **Value**       | []object |
| **Required**    | false |
| **Example**     | |
| **Description** | A list of node selector requirements by node's labels. |
| | || **Key**         | PerconaPGCluster.spec.backups.pgbackrest.repoHost.affinity.nodeAffinity.preferredDuringSchedulingIgnoredDuringExecution[index].preference.matchFields |
| **Value**       | []object |
| **Required**    | false |
| **Example**     | |
| **Description** | A list of node selector requirements by node's fields. |
| | |
| **Key**         | PerconaPGCluster.spec.backups.pgbackrest.repoHost.affinity.nodeAffinity.preferredDuringSchedulingIgnoredDuringExecution[index].preference.matchExpressions[index].key |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | The label key that the selector applies to. |
| | || **Key**         | PerconaPGCluster.spec.backups.pgbackrest.repoHost.affinity.nodeAffinity.preferredDuringSchedulingIgnoredDuringExecution[index].preference.matchExpressions[index].operator |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | Represents a key's relationship to a set of values. Valid operators are In, NotIn, Exists, DoesNotExist. Gt, and Lt. |
| | || **Key**         | PerconaPGCluster.spec.backups.pgbackrest.repoHost.affinity.nodeAffinity.preferredDuringSchedulingIgnoredDuringExecution[index].preference.matchExpressions[index].values |
| **Value**       | []string |
| **Required**    | false |
| **Example**     | |
| **Description** | An array of string values. If the operator is In or NotIn, the values array must be non-empty. If the operator is Exists or DoesNotExist, the values array must be empty. If the operator is Gt or Lt, the values array must have a single element, which will be interpreted as an integer. This array is replaced during a strategic merge patch. |
| | |
| **Key**         | PerconaPGCluster.spec.backups.pgbackrest.repoHost.affinity.nodeAffinity.preferredDuringSchedulingIgnoredDuringExecution[index].preference.matchFields[index].key |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | The label key that the selector applies to. |
| | || **Key**         | PerconaPGCluster.spec.backups.pgbackrest.repoHost.affinity.nodeAffinity.preferredDuringSchedulingIgnoredDuringExecution[index].preference.matchFields[index].operator |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | Represents a key's relationship to a set of values. Valid operators are In, NotIn, Exists, DoesNotExist. Gt, and Lt. |
| | || **Key**         | PerconaPGCluster.spec.backups.pgbackrest.repoHost.affinity.nodeAffinity.preferredDuringSchedulingIgnoredDuringExecution[index].preference.matchFields[index].values |
| **Value**       | []string |
| **Required**    | false |
| **Example**     | |
| **Description** | An array of string values. If the operator is In or NotIn, the values array must be non-empty. If the operator is Exists or DoesNotExist, the values array must be empty. If the operator is Gt or Lt, the values array must have a single element, which will be interpreted as an integer. This array is replaced during a strategic merge patch. |
| | |
| **Key**         | PerconaPGCluster.spec.backups.pgbackrest.repoHost.affinity.nodeAffinity.requiredDuringSchedulingIgnoredDuringExecution.nodeSelectorTerms |
| **Value**       | []object |
| **Required**    | true |
| **Example**     | |
| **Description** | Required. A list of node selector terms. The terms are ORed. |
| | |
| **Key**         | PerconaPGCluster.spec.backups.pgbackrest.repoHost.affinity.nodeAffinity.requiredDuringSchedulingIgnoredDuringExecution.nodeSelectorTerms[index].matchExpressions |
| **Value**       | []object |
| **Required**    | false |
| **Example**     | |
| **Description** | A list of node selector requirements by node's labels. |
| | || **Key**         | PerconaPGCluster.spec.backups.pgbackrest.repoHost.affinity.nodeAffinity.requiredDuringSchedulingIgnoredDuringExecution.nodeSelectorTerms[index].matchFields |
| **Value**       | []object |
| **Required**    | false |
| **Example**     | |
| **Description** | A list of node selector requirements by node's fields. |
| | |
| **Key**         | PerconaPGCluster.spec.backups.pgbackrest.repoHost.affinity.nodeAffinity.requiredDuringSchedulingIgnoredDuringExecution.nodeSelectorTerms[index].matchExpressions[index].key |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | The label key that the selector applies to. |
| | || **Key**         | PerconaPGCluster.spec.backups.pgbackrest.repoHost.affinity.nodeAffinity.requiredDuringSchedulingIgnoredDuringExecution.nodeSelectorTerms[index].matchExpressions[index].operator |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | Represents a key's relationship to a set of values. Valid operators are In, NotIn, Exists, DoesNotExist. Gt, and Lt. |
| | || **Key**         | PerconaPGCluster.spec.backups.pgbackrest.repoHost.affinity.nodeAffinity.requiredDuringSchedulingIgnoredDuringExecution.nodeSelectorTerms[index].matchExpressions[index].values |
| **Value**       | []string |
| **Required**    | false |
| **Example**     | |
| **Description** | An array of string values. If the operator is In or NotIn, the values array must be non-empty. If the operator is Exists or DoesNotExist, the values array must be empty. If the operator is Gt or Lt, the values array must have a single element, which will be interpreted as an integer. This array is replaced during a strategic merge patch. |
| | |
| **Key**         | PerconaPGCluster.spec.backups.pgbackrest.repoHost.affinity.nodeAffinity.requiredDuringSchedulingIgnoredDuringExecution.nodeSelectorTerms[index].matchFields[index].key |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | The label key that the selector applies to. |
| | || **Key**         | PerconaPGCluster.spec.backups.pgbackrest.repoHost.affinity.nodeAffinity.requiredDuringSchedulingIgnoredDuringExecution.nodeSelectorTerms[index].matchFields[index].operator |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | Represents a key's relationship to a set of values. Valid operators are In, NotIn, Exists, DoesNotExist. Gt, and Lt. |
| | || **Key**         | PerconaPGCluster.spec.backups.pgbackrest.repoHost.affinity.nodeAffinity.requiredDuringSchedulingIgnoredDuringExecution.nodeSelectorTerms[index].matchFields[index].values |
| **Value**       | []string |
| **Required**    | false |
| **Example**     | |
| **Description** | An array of string values. If the operator is In or NotIn, the values array must be non-empty. If the operator is Exists or DoesNotExist, the values array must be empty. If the operator is Gt or Lt, the values array must have a single element, which will be interpreted as an integer. This array is replaced during a strategic merge patch. |
| | |
| **Key**         | PerconaPGCluster.spec.backups.pgbackrest.repoHost.affinity.podAffinity.preferredDuringSchedulingIgnoredDuringExecution |
| **Value**       | []object |
| **Required**    | false |
| **Example**     | |
| **Description** | The scheduler will prefer to schedule pods to nodes that satisfy the affinity expressions specified by this field, but it may choose a node that violates one or more of the expressions. The node that is most preferred is the one with the greatest sum of weights, i.e. for each node that meets all of the scheduling requirements (resource request, requiredDuringScheduling affinity expressions, etc.), compute a sum by iterating through the elements of this field and adding "weight" to the sum if the node has pods which matches the corresponding podAffinityTerm; the node(s) with the highest sum are the most preferred. |
| | || **Key**         | PerconaPGCluster.spec.backups.pgbackrest.repoHost.affinity.podAffinity.requiredDuringSchedulingIgnoredDuringExecution |
| **Value**       | []object |
| **Required**    | false |
| **Example**     | |
| **Description** | If the affinity requirements specified by this field are not met at scheduling time, the pod will not be scheduled onto the node. If the affinity requirements specified by this field cease to be met at some point during pod execution (e.g. due to a pod label update), the system may or may not try to eventually evict the pod from its node. When there are multiple elements, the lists of nodes corresponding to each podAffinityTerm are intersected, i.e. all terms must be satisfied. |
| | |
| **Key**         | PerconaPGCluster.spec.backups.pgbackrest.repoHost.affinity.podAffinity.preferredDuringSchedulingIgnoredDuringExecution[index].podAffinityTerm |
| **Value**       | object |
| **Required**    | true |
| **Example**     | |
| **Description** | Required. A pod affinity term, associated with the corresponding weight. |
| | || **Key**         | PerconaPGCluster.spec.backups.pgbackrest.repoHost.affinity.podAffinity.preferredDuringSchedulingIgnoredDuringExecution[index].weight |
| **Value**       | integer |
| **Required**    | true |
| **Example**     | |
| **Description** | weight associated with matching the corresponding podAffinityTerm, in the range 1-100. |
| | |
| **Key**         | PerconaPGCluster.spec.backups.pgbackrest.repoHost.affinity.podAffinity.preferredDuringSchedulingIgnoredDuringExecution[index].podAffinityTerm.topologyKey |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | This pod should be co-located (affinity) or not co-located (anti-affinity) with the pods matching the labelSelector in the specified namespaces, where co-located is defined as running on a node whose value of the label with key topologyKey matches that of any node on which any of the selected pods is running. Empty topologyKey is not allowed. |
| | || **Key**         | PerconaPGCluster.spec.backups.pgbackrest.repoHost.affinity.podAffinity.preferredDuringSchedulingIgnoredDuringExecution[index].podAffinityTerm.labelSelector |
| **Value**       | object |
| **Required**    | false |
| **Example**     | |
| **Description** | A label query over a set of resources, in this case pods. |
| | || **Key**         | PerconaPGCluster.spec.backups.pgbackrest.repoHost.affinity.podAffinity.preferredDuringSchedulingIgnoredDuringExecution[index].podAffinityTerm.namespaceSelector |
| **Value**       | object |
| **Required**    | false |
| **Example**     | |
| **Description** | A label query over the set of namespaces that the term applies to. The term is applied to the union of the namespaces selected by this field and the ones listed in the namespaces field. null selector and null or empty namespaces list means "this pod's namespace". An empty selector ({}) matches all namespaces. |
| | || **Key**         | PerconaPGCluster.spec.backups.pgbackrest.repoHost.affinity.podAffinity.preferredDuringSchedulingIgnoredDuringExecution[index].podAffinityTerm.namespaces |
| **Value**       | []string |
| **Required**    | false |
| **Example**     | |
| **Description** | namespaces specifies a static list of namespace names that the term applies to. The term is applied to the union of the namespaces listed in this field and the ones selected by namespaceSelector. null or empty namespaces list and null namespaceSelector means "this pod's namespace". |
| | |
| **Key**         | PerconaPGCluster.spec.backups.pgbackrest.repoHost.affinity.podAffinity.preferredDuringSchedulingIgnoredDuringExecution[index].podAffinityTerm.labelSelector.matchExpressions |
| **Value**       | []object |
| **Required**    | false |
| **Example**     | |
| **Description** | matchExpressions is a list of label selector requirements. The requirements are ANDed. |
| | || **Key**         | PerconaPGCluster.spec.backups.pgbackrest.repoHost.affinity.podAffinity.preferredDuringSchedulingIgnoredDuringExecution[index].podAffinityTerm.labelSelector.matchLabels |
| **Value**       | map[string]string |
| **Required**    | false |
| **Example**     | |
| **Description** | matchLabels is a map of {key,value} pairs. A single {key,value} in the matchLabels map is equivalent to an element of matchExpressions, whose key field is "key", the operator is "In", and the values array contains only "value". The requirements are ANDed. |
| | |
| **Key**         | PerconaPGCluster.spec.backups.pgbackrest.repoHost.affinity.podAffinity.preferredDuringSchedulingIgnoredDuringExecution[index].podAffinityTerm.labelSelector.matchExpressions[index].key |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | key is the label key that the selector applies to. |
| | || **Key**         | PerconaPGCluster.spec.backups.pgbackrest.repoHost.affinity.podAffinity.preferredDuringSchedulingIgnoredDuringExecution[index].podAffinityTerm.labelSelector.matchExpressions[index].operator |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | operator represents a key's relationship to a set of values. Valid operators are In, NotIn, Exists and DoesNotExist. |
| | || **Key**         | PerconaPGCluster.spec.backups.pgbackrest.repoHost.affinity.podAffinity.preferredDuringSchedulingIgnoredDuringExecution[index].podAffinityTerm.labelSelector.matchExpressions[index].values |
| **Value**       | []string |
| **Required**    | false |
| **Example**     | |
| **Description** | values is an array of string values. If the operator is In or NotIn, the values array must be non-empty. If the operator is Exists or DoesNotExist, the values array must be empty. This array is replaced during a strategic merge patch. |
| | |
| **Key**         | PerconaPGCluster.spec.backups.pgbackrest.repoHost.affinity.podAffinity.preferredDuringSchedulingIgnoredDuringExecution[index].podAffinityTerm.namespaceSelector.matchExpressions |
| **Value**       | []object |
| **Required**    | false |
| **Example**     | |
| **Description** | matchExpressions is a list of label selector requirements. The requirements are ANDed. |
| | || **Key**         | PerconaPGCluster.spec.backups.pgbackrest.repoHost.affinity.podAffinity.preferredDuringSchedulingIgnoredDuringExecution[index].podAffinityTerm.namespaceSelector.matchLabels |
| **Value**       | map[string]string |
| **Required**    | false |
| **Example**     | |
| **Description** | matchLabels is a map of {key,value} pairs. A single {key,value} in the matchLabels map is equivalent to an element of matchExpressions, whose key field is "key", the operator is "In", and the values array contains only "value". The requirements are ANDed. |
| | |
| **Key**         | PerconaPGCluster.spec.backups.pgbackrest.repoHost.affinity.podAffinity.preferredDuringSchedulingIgnoredDuringExecution[index].podAffinityTerm.namespaceSelector.matchExpressions[index].key |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | key is the label key that the selector applies to. |
| | || **Key**         | PerconaPGCluster.spec.backups.pgbackrest.repoHost.affinity.podAffinity.preferredDuringSchedulingIgnoredDuringExecution[index].podAffinityTerm.namespaceSelector.matchExpressions[index].operator |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | operator represents a key's relationship to a set of values. Valid operators are In, NotIn, Exists and DoesNotExist. |
| | || **Key**         | PerconaPGCluster.spec.backups.pgbackrest.repoHost.affinity.podAffinity.preferredDuringSchedulingIgnoredDuringExecution[index].podAffinityTerm.namespaceSelector.matchExpressions[index].values |
| **Value**       | []string |
| **Required**    | false |
| **Example**     | |
| **Description** | values is an array of string values. If the operator is In or NotIn, the values array must be non-empty. If the operator is Exists or DoesNotExist, the values array must be empty. This array is replaced during a strategic merge patch. |
| | |
| **Key**         | PerconaPGCluster.spec.backups.pgbackrest.repoHost.affinity.podAffinity.requiredDuringSchedulingIgnoredDuringExecution[index].topologyKey |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | This pod should be co-located (affinity) or not co-located (anti-affinity) with the pods matching the labelSelector in the specified namespaces, where co-located is defined as running on a node whose value of the label with key topologyKey matches that of any node on which any of the selected pods is running. Empty topologyKey is not allowed. |
| | || **Key**         | PerconaPGCluster.spec.backups.pgbackrest.repoHost.affinity.podAffinity.requiredDuringSchedulingIgnoredDuringExecution[index].labelSelector |
| **Value**       | object |
| **Required**    | false |
| **Example**     | |
| **Description** | A label query over a set of resources, in this case pods. |
| | || **Key**         | PerconaPGCluster.spec.backups.pgbackrest.repoHost.affinity.podAffinity.requiredDuringSchedulingIgnoredDuringExecution[index].namespaceSelector |
| **Value**       | object |
| **Required**    | false |
| **Example**     | |
| **Description** | A label query over the set of namespaces that the term applies to. The term is applied to the union of the namespaces selected by this field and the ones listed in the namespaces field. null selector and null or empty namespaces list means "this pod's namespace". An empty selector ({}) matches all namespaces. |
| | || **Key**         | PerconaPGCluster.spec.backups.pgbackrest.repoHost.affinity.podAffinity.requiredDuringSchedulingIgnoredDuringExecution[index].namespaces |
| **Value**       | []string |
| **Required**    | false |
| **Example**     | |
| **Description** | namespaces specifies a static list of namespace names that the term applies to. The term is applied to the union of the namespaces listed in this field and the ones selected by namespaceSelector. null or empty namespaces list and null namespaceSelector means "this pod's namespace". |
| | |
| **Key**         | PerconaPGCluster.spec.backups.pgbackrest.repoHost.affinity.podAffinity.requiredDuringSchedulingIgnoredDuringExecution[index].labelSelector.matchExpressions |
| **Value**       | []object |
| **Required**    | false |
| **Example**     | |
| **Description** | matchExpressions is a list of label selector requirements. The requirements are ANDed. |
| | || **Key**         | PerconaPGCluster.spec.backups.pgbackrest.repoHost.affinity.podAffinity.requiredDuringSchedulingIgnoredDuringExecution[index].labelSelector.matchLabels |
| **Value**       | map[string]string |
| **Required**    | false |
| **Example**     | |
| **Description** | matchLabels is a map of {key,value} pairs. A single {key,value} in the matchLabels map is equivalent to an element of matchExpressions, whose key field is "key", the operator is "In", and the values array contains only "value". The requirements are ANDed. |
| | |
| **Key**         | PerconaPGCluster.spec.backups.pgbackrest.repoHost.affinity.podAffinity.requiredDuringSchedulingIgnoredDuringExecution[index].labelSelector.matchExpressions[index].key |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | key is the label key that the selector applies to. |
| | || **Key**         | PerconaPGCluster.spec.backups.pgbackrest.repoHost.affinity.podAffinity.requiredDuringSchedulingIgnoredDuringExecution[index].labelSelector.matchExpressions[index].operator |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | operator represents a key's relationship to a set of values. Valid operators are In, NotIn, Exists and DoesNotExist. |
| | || **Key**         | PerconaPGCluster.spec.backups.pgbackrest.repoHost.affinity.podAffinity.requiredDuringSchedulingIgnoredDuringExecution[index].labelSelector.matchExpressions[index].values |
| **Value**       | []string |
| **Required**    | false |
| **Example**     | |
| **Description** | values is an array of string values. If the operator is In or NotIn, the values array must be non-empty. If the operator is Exists or DoesNotExist, the values array must be empty. This array is replaced during a strategic merge patch. |
| | |
| **Key**         | PerconaPGCluster.spec.backups.pgbackrest.repoHost.affinity.podAffinity.requiredDuringSchedulingIgnoredDuringExecution[index].namespaceSelector.matchExpressions |
| **Value**       | []object |
| **Required**    | false |
| **Example**     | |
| **Description** | matchExpressions is a list of label selector requirements. The requirements are ANDed. |
| | || **Key**         | PerconaPGCluster.spec.backups.pgbackrest.repoHost.affinity.podAffinity.requiredDuringSchedulingIgnoredDuringExecution[index].namespaceSelector.matchLabels |
| **Value**       | map[string]string |
| **Required**    | false |
| **Example**     | |
| **Description** | matchLabels is a map of {key,value} pairs. A single {key,value} in the matchLabels map is equivalent to an element of matchExpressions, whose key field is "key", the operator is "In", and the values array contains only "value". The requirements are ANDed. |
| | |
| **Key**         | PerconaPGCluster.spec.backups.pgbackrest.repoHost.affinity.podAffinity.requiredDuringSchedulingIgnoredDuringExecution[index].namespaceSelector.matchExpressions[index].key |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | key is the label key that the selector applies to. |
| | || **Key**         | PerconaPGCluster.spec.backups.pgbackrest.repoHost.affinity.podAffinity.requiredDuringSchedulingIgnoredDuringExecution[index].namespaceSelector.matchExpressions[index].operator |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | operator represents a key's relationship to a set of values. Valid operators are In, NotIn, Exists and DoesNotExist. |
| | || **Key**         | PerconaPGCluster.spec.backups.pgbackrest.repoHost.affinity.podAffinity.requiredDuringSchedulingIgnoredDuringExecution[index].namespaceSelector.matchExpressions[index].values |
| **Value**       | []string |
| **Required**    | false |
| **Example**     | |
| **Description** | values is an array of string values. If the operator is In or NotIn, the values array must be non-empty. If the operator is Exists or DoesNotExist, the values array must be empty. This array is replaced during a strategic merge patch. |
| | |
| **Key**         | PerconaPGCluster.spec.backups.pgbackrest.repoHost.affinity.podAntiAffinity.preferredDuringSchedulingIgnoredDuringExecution |
| **Value**       | []object |
| **Required**    | false |
| **Example**     | |
| **Description** | The scheduler will prefer to schedule pods to nodes that satisfy the anti-affinity expressions specified by this field, but it may choose a node that violates one or more of the expressions. The node that is most preferred is the one with the greatest sum of weights, i.e. for each node that meets all of the scheduling requirements (resource request, requiredDuringScheduling anti-affinity expressions, etc.), compute a sum by iterating through the elements of this field and adding "weight" to the sum if the node has pods which matches the corresponding podAffinityTerm; the node(s) with the highest sum are the most preferred. |
| | || **Key**         | PerconaPGCluster.spec.backups.pgbackrest.repoHost.affinity.podAntiAffinity.requiredDuringSchedulingIgnoredDuringExecution |
| **Value**       | []object |
| **Required**    | false |
| **Example**     | |
| **Description** | If the anti-affinity requirements specified by this field are not met at scheduling time, the pod will not be scheduled onto the node. If the anti-affinity requirements specified by this field cease to be met at some point during pod execution (e.g. due to a pod label update), the system may or may not try to eventually evict the pod from its node. When there are multiple elements, the lists of nodes corresponding to each podAffinityTerm are intersected, i.e. all terms must be satisfied. |
| | |
| **Key**         | PerconaPGCluster.spec.backups.pgbackrest.repoHost.affinity.podAntiAffinity.preferredDuringSchedulingIgnoredDuringExecution[index].podAffinityTerm |
| **Value**       | object |
| **Required**    | true |
| **Example**     | |
| **Description** | Required. A pod affinity term, associated with the corresponding weight. |
| | || **Key**         | PerconaPGCluster.spec.backups.pgbackrest.repoHost.affinity.podAntiAffinity.preferredDuringSchedulingIgnoredDuringExecution[index].weight |
| **Value**       | integer |
| **Required**    | true |
| **Example**     | |
| **Description** | weight associated with matching the corresponding podAffinityTerm, in the range 1-100. |
| | |
| **Key**         | PerconaPGCluster.spec.backups.pgbackrest.repoHost.affinity.podAntiAffinity.preferredDuringSchedulingIgnoredDuringExecution[index].podAffinityTerm.topologyKey |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | This pod should be co-located (affinity) or not co-located (anti-affinity) with the pods matching the labelSelector in the specified namespaces, where co-located is defined as running on a node whose value of the label with key topologyKey matches that of any node on which any of the selected pods is running. Empty topologyKey is not allowed. |
| | || **Key**         | PerconaPGCluster.spec.backups.pgbackrest.repoHost.affinity.podAntiAffinity.preferredDuringSchedulingIgnoredDuringExecution[index].podAffinityTerm.labelSelector |
| **Value**       | object |
| **Required**    | false |
| **Example**     | |
| **Description** | A label query over a set of resources, in this case pods. |
| | || **Key**         | PerconaPGCluster.spec.backups.pgbackrest.repoHost.affinity.podAntiAffinity.preferredDuringSchedulingIgnoredDuringExecution[index].podAffinityTerm.namespaceSelector |
| **Value**       | object |
| **Required**    | false |
| **Example**     | |
| **Description** | A label query over the set of namespaces that the term applies to. The term is applied to the union of the namespaces selected by this field and the ones listed in the namespaces field. null selector and null or empty namespaces list means "this pod's namespace". An empty selector ({}) matches all namespaces. |
| | || **Key**         | PerconaPGCluster.spec.backups.pgbackrest.repoHost.affinity.podAntiAffinity.preferredDuringSchedulingIgnoredDuringExecution[index].podAffinityTerm.namespaces |
| **Value**       | []string |
| **Required**    | false |
| **Example**     | |
| **Description** | namespaces specifies a static list of namespace names that the term applies to. The term is applied to the union of the namespaces listed in this field and the ones selected by namespaceSelector. null or empty namespaces list and null namespaceSelector means "this pod's namespace". |
| | |
| **Key**         | PerconaPGCluster.spec.backups.pgbackrest.repoHost.affinity.podAntiAffinity.preferredDuringSchedulingIgnoredDuringExecution[index].podAffinityTerm.labelSelector.matchExpressions |
| **Value**       | []object |
| **Required**    | false |
| **Example**     | |
| **Description** | matchExpressions is a list of label selector requirements. The requirements are ANDed. |
| | || **Key**         | PerconaPGCluster.spec.backups.pgbackrest.repoHost.affinity.podAntiAffinity.preferredDuringSchedulingIgnoredDuringExecution[index].podAffinityTerm.labelSelector.matchLabels |
| **Value**       | map[string]string |
| **Required**    | false |
| **Example**     | |
| **Description** | matchLabels is a map of {key,value} pairs. A single {key,value} in the matchLabels map is equivalent to an element of matchExpressions, whose key field is "key", the operator is "In", and the values array contains only "value". The requirements are ANDed. |
| | |
| **Key**         | PerconaPGCluster.spec.backups.pgbackrest.repoHost.affinity.podAntiAffinity.preferredDuringSchedulingIgnoredDuringExecution[index].podAffinityTerm.labelSelector.matchExpressions[index].key |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | key is the label key that the selector applies to. |
| | || **Key**         | PerconaPGCluster.spec.backups.pgbackrest.repoHost.affinity.podAntiAffinity.preferredDuringSchedulingIgnoredDuringExecution[index].podAffinityTerm.labelSelector.matchExpressions[index].operator |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | operator represents a key's relationship to a set of values. Valid operators are In, NotIn, Exists and DoesNotExist. |
| | || **Key**         | PerconaPGCluster.spec.backups.pgbackrest.repoHost.affinity.podAntiAffinity.preferredDuringSchedulingIgnoredDuringExecution[index].podAffinityTerm.labelSelector.matchExpressions[index].values |
| **Value**       | []string |
| **Required**    | false |
| **Example**     | |
| **Description** | values is an array of string values. If the operator is In or NotIn, the values array must be non-empty. If the operator is Exists or DoesNotExist, the values array must be empty. This array is replaced during a strategic merge patch. |
| | |
| **Key**         | PerconaPGCluster.spec.backups.pgbackrest.repoHost.affinity.podAntiAffinity.preferredDuringSchedulingIgnoredDuringExecution[index].podAffinityTerm.namespaceSelector.matchExpressions |
| **Value**       | []object |
| **Required**    | false |
| **Example**     | |
| **Description** | matchExpressions is a list of label selector requirements. The requirements are ANDed. |
| | || **Key**         | PerconaPGCluster.spec.backups.pgbackrest.repoHost.affinity.podAntiAffinity.preferredDuringSchedulingIgnoredDuringExecution[index].podAffinityTerm.namespaceSelector.matchLabels |
| **Value**       | map[string]string |
| **Required**    | false |
| **Example**     | |
| **Description** | matchLabels is a map of {key,value} pairs. A single {key,value} in the matchLabels map is equivalent to an element of matchExpressions, whose key field is "key", the operator is "In", and the values array contains only "value". The requirements are ANDed. |
| | |
| **Key**         | PerconaPGCluster.spec.backups.pgbackrest.repoHost.affinity.podAntiAffinity.preferredDuringSchedulingIgnoredDuringExecution[index].podAffinityTerm.namespaceSelector.matchExpressions[index].key |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | key is the label key that the selector applies to. |
| | || **Key**         | PerconaPGCluster.spec.backups.pgbackrest.repoHost.affinity.podAntiAffinity.preferredDuringSchedulingIgnoredDuringExecution[index].podAffinityTerm.namespaceSelector.matchExpressions[index].operator |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | operator represents a key's relationship to a set of values. Valid operators are In, NotIn, Exists and DoesNotExist. |
| | || **Key**         | PerconaPGCluster.spec.backups.pgbackrest.repoHost.affinity.podAntiAffinity.preferredDuringSchedulingIgnoredDuringExecution[index].podAffinityTerm.namespaceSelector.matchExpressions[index].values |
| **Value**       | []string |
| **Required**    | false |
| **Example**     | |
| **Description** | values is an array of string values. If the operator is In or NotIn, the values array must be non-empty. If the operator is Exists or DoesNotExist, the values array must be empty. This array is replaced during a strategic merge patch. |
| | |
| **Key**         | PerconaPGCluster.spec.backups.pgbackrest.repoHost.affinity.podAntiAffinity.requiredDuringSchedulingIgnoredDuringExecution[index].topologyKey |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | This pod should be co-located (affinity) or not co-located (anti-affinity) with the pods matching the labelSelector in the specified namespaces, where co-located is defined as running on a node whose value of the label with key topologyKey matches that of any node on which any of the selected pods is running. Empty topologyKey is not allowed. |
| | || **Key**         | PerconaPGCluster.spec.backups.pgbackrest.repoHost.affinity.podAntiAffinity.requiredDuringSchedulingIgnoredDuringExecution[index].labelSelector |
| **Value**       | object |
| **Required**    | false |
| **Example**     | |
| **Description** | A label query over a set of resources, in this case pods. |
| | || **Key**         | PerconaPGCluster.spec.backups.pgbackrest.repoHost.affinity.podAntiAffinity.requiredDuringSchedulingIgnoredDuringExecution[index].namespaceSelector |
| **Value**       | object |
| **Required**    | false |
| **Example**     | |
| **Description** | A label query over the set of namespaces that the term applies to. The term is applied to the union of the namespaces selected by this field and the ones listed in the namespaces field. null selector and null or empty namespaces list means "this pod's namespace". An empty selector ({}) matches all namespaces. |
| | || **Key**         | PerconaPGCluster.spec.backups.pgbackrest.repoHost.affinity.podAntiAffinity.requiredDuringSchedulingIgnoredDuringExecution[index].namespaces |
| **Value**       | []string |
| **Required**    | false |
| **Example**     | |
| **Description** | namespaces specifies a static list of namespace names that the term applies to. The term is applied to the union of the namespaces listed in this field and the ones selected by namespaceSelector. null or empty namespaces list and null namespaceSelector means "this pod's namespace". |
| | |
| **Key**         | PerconaPGCluster.spec.backups.pgbackrest.repoHost.affinity.podAntiAffinity.requiredDuringSchedulingIgnoredDuringExecution[index].labelSelector.matchExpressions |
| **Value**       | []object |
| **Required**    | false |
| **Example**     | |
| **Description** | matchExpressions is a list of label selector requirements. The requirements are ANDed. |
| | || **Key**         | PerconaPGCluster.spec.backups.pgbackrest.repoHost.affinity.podAntiAffinity.requiredDuringSchedulingIgnoredDuringExecution[index].labelSelector.matchLabels |
| **Value**       | map[string]string |
| **Required**    | false |
| **Example**     | |
| **Description** | matchLabels is a map of {key,value} pairs. A single {key,value} in the matchLabels map is equivalent to an element of matchExpressions, whose key field is "key", the operator is "In", and the values array contains only "value". The requirements are ANDed. |
| | |
| **Key**         | PerconaPGCluster.spec.backups.pgbackrest.repoHost.affinity.podAntiAffinity.requiredDuringSchedulingIgnoredDuringExecution[index].labelSelector.matchExpressions[index].key |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | key is the label key that the selector applies to. |
| | || **Key**         | PerconaPGCluster.spec.backups.pgbackrest.repoHost.affinity.podAntiAffinity.requiredDuringSchedulingIgnoredDuringExecution[index].labelSelector.matchExpressions[index].operator |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | operator represents a key's relationship to a set of values. Valid operators are In, NotIn, Exists and DoesNotExist. |
| | || **Key**         | PerconaPGCluster.spec.backups.pgbackrest.repoHost.affinity.podAntiAffinity.requiredDuringSchedulingIgnoredDuringExecution[index].labelSelector.matchExpressions[index].values |
| **Value**       | []string |
| **Required**    | false |
| **Example**     | |
| **Description** | values is an array of string values. If the operator is In or NotIn, the values array must be non-empty. If the operator is Exists or DoesNotExist, the values array must be empty. This array is replaced during a strategic merge patch. |
| | |
| **Key**         | PerconaPGCluster.spec.backups.pgbackrest.repoHost.affinity.podAntiAffinity.requiredDuringSchedulingIgnoredDuringExecution[index].namespaceSelector.matchExpressions |
| **Value**       | []object |
| **Required**    | false |
| **Example**     | |
| **Description** | matchExpressions is a list of label selector requirements. The requirements are ANDed. |
| | || **Key**         | PerconaPGCluster.spec.backups.pgbackrest.repoHost.affinity.podAntiAffinity.requiredDuringSchedulingIgnoredDuringExecution[index].namespaceSelector.matchLabels |
| **Value**       | map[string]string |
| **Required**    | false |
| **Example**     | |
| **Description** | matchLabels is a map of {key,value} pairs. A single {key,value} in the matchLabels map is equivalent to an element of matchExpressions, whose key field is "key", the operator is "In", and the values array contains only "value". The requirements are ANDed. |
| | |
| **Key**         | PerconaPGCluster.spec.backups.pgbackrest.repoHost.affinity.podAntiAffinity.requiredDuringSchedulingIgnoredDuringExecution[index].namespaceSelector.matchExpressions[index].key |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | key is the label key that the selector applies to. |
| | || **Key**         | PerconaPGCluster.spec.backups.pgbackrest.repoHost.affinity.podAntiAffinity.requiredDuringSchedulingIgnoredDuringExecution[index].namespaceSelector.matchExpressions[index].operator |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | operator represents a key's relationship to a set of values. Valid operators are In, NotIn, Exists and DoesNotExist. |
| | || **Key**         | PerconaPGCluster.spec.backups.pgbackrest.repoHost.affinity.podAntiAffinity.requiredDuringSchedulingIgnoredDuringExecution[index].namespaceSelector.matchExpressions[index].values |
| **Value**       | []string |
| **Required**    | false |
| **Example**     | |
| **Description** | values is an array of string values. If the operator is In or NotIn, the values array must be non-empty. If the operator is Exists or DoesNotExist, the values array must be empty. This array is replaced during a strategic merge patch. |
| | |
| **Key**         | PerconaPGCluster.spec.backups.pgbackrest.repoHost.resources.limits |
| **Value**       | map[string]int or string |
| **Required**    | false |
| **Example**     | |
| **Description** | Limits describes the maximum amount of compute resources allowed. More info: https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/ |
| | || **Key**         | PerconaPGCluster.spec.backups.pgbackrest.repoHost.resources.requests |
| **Value**       | map[string]int or string |
| **Required**    | false |
| **Example**     | |
| **Description** | Requests describes the minimum amount of compute resources required. If Requests is omitted for a container, it defaults to Limits if that is explicitly specified, otherwise to an implementation-defined value. More info: https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/ |
| | |
| **Key**         | PerconaPGCluster.spec.backups.pgbackrest.repoHost.sshConfigMap.items |
| **Value**       | []object |
| **Required**    | false |
| **Example**     | |
| **Description** | items if unspecified, each key-value pair in the Data field of the referenced ConfigMap will be projected into the volume as a file whose name is the key and content is the value. If specified, the listed keys will be projected into the specified paths, and unlisted keys will not be present. If a key is specified which is not present in the ConfigMap, the volume setup will error unless it is marked optional. Paths must be relative and may not contain the '..' path or start with '..'. |
| | || **Key**         | PerconaPGCluster.spec.backups.pgbackrest.repoHost.sshConfigMap.name |
| **Value**       | string |
| **Required**    | false |
| **Example**     | |
| **Description** | Name of the referent. More info: https://kubernetes.io/docs/concepts/overview/working-with-objects/names/#names TODO: Add other useful fields. apiVersion, kind, uid? |
| | || **Key**         | PerconaPGCluster.spec.backups.pgbackrest.repoHost.sshConfigMap.optional |
| **Value**       | boolean |
| **Required**    | false |
| **Example**     | |
| **Description** | optional specify whether the ConfigMap or its keys must be defined |
| | |
| **Key**         | PerconaPGCluster.spec.backups.pgbackrest.repoHost.sshConfigMap.items[index].key |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | key is the key to project. |
| | || **Key**         | PerconaPGCluster.spec.backups.pgbackrest.repoHost.sshConfigMap.items[index].path |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | path is the relative path of the file to map the key to. May not be an absolute path. May not contain the path element '..'. May not start with the string '..'. |
| | || **Key**         | PerconaPGCluster.spec.backups.pgbackrest.repoHost.sshConfigMap.items[index].mode |
| **Value**       | integer |
| **Required**    | false |
| **Example**     | |
| **Description** | mode is Optional: mode bits used to set permissions on this file. Must be an octal value between 0000 and 0777 or a decimal value between 0 and 511. YAML accepts both octal and decimal values, JSON requires decimal values for mode bits. If not specified, the volume defaultMode will be used. This might be in conflict with other options that affect the file mode, like fsGroup, and the result can be other mode bits set. |
| | |
| **Key**         | PerconaPGCluster.spec.backups.pgbackrest.repoHost.sshSecret.items |
| **Value**       | []object |
| **Required**    | false |
| **Example**     | |
| **Description** | items if unspecified, each key-value pair in the Data field of the referenced Secret will be projected into the volume as a file whose name is the key and content is the value. If specified, the listed keys will be projected into the specified paths, and unlisted keys will not be present. If a key is specified which is not present in the Secret, the volume setup will error unless it is marked optional. Paths must be relative and may not contain the '..' path or start with '..'. |
| | || **Key**         | PerconaPGCluster.spec.backups.pgbackrest.repoHost.sshSecret.name |
| **Value**       | string |
| **Required**    | false |
| **Example**     | |
| **Description** | Name of the referent. More info: https://kubernetes.io/docs/concepts/overview/working-with-objects/names/#names TODO: Add other useful fields. apiVersion, kind, uid? |
| | || **Key**         | PerconaPGCluster.spec.backups.pgbackrest.repoHost.sshSecret.optional |
| **Value**       | boolean |
| **Required**    | false |
| **Example**     | |
| **Description** | optional field specify whether the Secret or its key must be defined |
| | |
| **Key**         | PerconaPGCluster.spec.backups.pgbackrest.repoHost.sshSecret.items[index].key |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | key is the key to project. |
| | || **Key**         | PerconaPGCluster.spec.backups.pgbackrest.repoHost.sshSecret.items[index].path |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | path is the relative path of the file to map the key to. May not be an absolute path. May not contain the path element '..'. May not start with the string '..'. |
| | || **Key**         | PerconaPGCluster.spec.backups.pgbackrest.repoHost.sshSecret.items[index].mode |
| **Value**       | integer |
| **Required**    | false |
| **Example**     | |
| **Description** | mode is Optional: mode bits used to set permissions on this file. Must be an octal value between 0000 and 0777 or a decimal value between 0 and 511. YAML accepts both octal and decimal values, JSON requires decimal values for mode bits. If not specified, the volume defaultMode will be used. This might be in conflict with other options that affect the file mode, like fsGroup, and the result can be other mode bits set. |
| | |
| **Key**         | PerconaPGCluster.spec.backups.pgbackrest.repoHost.tolerations[index].effect |
| **Value**       | string |
| **Required**    | false |
| **Example**     | |
| **Description** | Effect indicates the taint effect to match. Empty means match all taint effects. When specified, allowed values are NoSchedule, PreferNoSchedule and NoExecute. |
| | || **Key**         | PerconaPGCluster.spec.backups.pgbackrest.repoHost.tolerations[index].key |
| **Value**       | string |
| **Required**    | false |
| **Example**     | |
| **Description** | Key is the taint key that the toleration applies to. Empty means match all taint keys. If the key is empty, operator must be Exists; this combination means to match all values and all keys. |
| | || **Key**         | PerconaPGCluster.spec.backups.pgbackrest.repoHost.tolerations[index].operator |
| **Value**       | string |
| **Required**    | false |
| **Example**     | |
| **Description** | Operator represents a key's relationship to the value. Valid operators are Exists and Equal. Defaults to Equal. Exists is equivalent to wildcard for value, so that a pod can tolerate all taints of a particular category. |
| | || **Key**         | PerconaPGCluster.spec.backups.pgbackrest.repoHost.tolerations[index].tolerationSeconds |
| **Value**       | integer |
| **Required**    | false |
| **Example**     | |
| **Description** | TolerationSeconds represents the period of time the toleration (which must be of effect NoExecute, otherwise this field is ignored) tolerates the taint. By default, it is not set, which means tolerate the taint forever (do not evict). Zero and negative values will be treated as 0 (evict immediately) by the system. |
| | || **Key**         | PerconaPGCluster.spec.backups.pgbackrest.repoHost.tolerations[index].value |
| **Value**       | string |
| **Required**    | false |
| **Example**     | |
| **Description** | Value is the taint value the toleration matches to. If the operator is Exists, the value should be empty, otherwise just a regular string. |
| | |
| **Key**         | PerconaPGCluster.spec.backups.pgbackrest.repoHost.topologySpreadConstraints[index].maxSkew |
| **Value**       | integer |
| **Required**    | true |
| **Example**     | |
| **Description** | MaxSkew describes the degree to which pods may be unevenly distributed. When `whenUnsatisfiable=DoNotSchedule`, it is the maximum permitted difference between the number of matching pods in the target topology and the global minimum. The global minimum is the minimum number of matching pods in an eligible domain or zero if the number of eligible domains is less than MinDomains. For example, in a 3-zone cluster, MaxSkew is set to 1, and pods with the same labelSelector spread as 2/2/1: In this case, the global minimum is 1. | zone1 | zone2 | zone3 | |  P P  |  P P  |   P   | - if MaxSkew is 1, incoming pod can only be scheduled to zone3 to become 2/2/2; scheduling it onto zone1(zone2) would make the ActualSkew(3-1) on zone1(zone2) violate MaxSkew(1). - if MaxSkew is 2, incoming pod can be scheduled onto any zone. When `whenUnsatisfiable=ScheduleAnyway`, it is used to give higher precedence to topologies that satisfy it. It's a required field. Default value is 1 and 0 is not allowed. |
| | || **Key**         | PerconaPGCluster.spec.backups.pgbackrest.repoHost.topologySpreadConstraints[index].topologyKey |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | TopologyKey is the key of node labels. Nodes that have a label with this key and identical values are considered to be in the same topology. We consider each <key, value> as a "bucket", and try to put balanced number of pods into each bucket. We define a domain as a particular instance of a topology. Also, we define an eligible domain as a domain whose nodes meet the requirements of nodeAffinityPolicy and nodeTaintsPolicy. e.g. If TopologyKey is "kubernetes.io/hostname", each Node is a domain of that topology. And, if TopologyKey is "topology.kubernetes.io/zone", each zone is a domain of that topology. It's a required field. |
| | || **Key**         | PerconaPGCluster.spec.backups.pgbackrest.repoHost.topologySpreadConstraints[index].whenUnsatisfiable |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | WhenUnsatisfiable indicates how to deal with a pod if it doesn't satisfy the spread constraint. - DoNotSchedule (default) tells the scheduler not to schedule it. - ScheduleAnyway tells the scheduler to schedule the pod in any location, but giving higher precedence to topologies that would help reduce the skew. A constraint is considered "Unsatisfiable" for an incoming pod if and only if every possible node assignment for that pod would violate "MaxSkew" on some topology. For example, in a 3-zone cluster, MaxSkew is set to 1, and pods with the same labelSelector spread as 3/1/1: | zone1 | zone2 | zone3 | | P P P |   P   |   P   | If WhenUnsatisfiable is set to DoNotSchedule, incoming pod can only be scheduled to zone2(zone3) to become 3/2/1(3/1/2) as ActualSkew(2-1) on zone2(zone3) satisfies MaxSkew(1). In other words, the cluster can still be imbalanced, but scheduler won't make it *more* imbalanced. It's a required field. |
| | || **Key**         | PerconaPGCluster.spec.backups.pgbackrest.repoHost.topologySpreadConstraints[index].labelSelector |
| **Value**       | object |
| **Required**    | false |
| **Example**     | |
| **Description** | LabelSelector is used to find matching pods. Pods that match this label selector are counted to determine the number of pods in their corresponding topology domain. |
| | || **Key**         | PerconaPGCluster.spec.backups.pgbackrest.repoHost.topologySpreadConstraints[index].matchLabelKeys |
| **Value**       | []string |
| **Required**    | false |
| **Example**     | |
| **Description** | MatchLabelKeys is a set of pod label keys to select the pods over which spreading will be calculated. The keys are used to lookup values from the incoming pod labels, those key-value labels are ANDed with labelSelector to select the group of existing pods over which spreading will be calculated for the incoming pod. Keys that don't exist in the incoming pod labels will be ignored. A null or empty list means only match against labelSelector. |
| | || **Key**         | PerconaPGCluster.spec.backups.pgbackrest.repoHost.topologySpreadConstraints[index].minDomains |
| **Value**       | integer |
| **Required**    | false |
| **Example**     | |
| **Description** | MinDomains indicates a minimum number of eligible domains. When the number of eligible domains with matching topology keys is less than minDomains, Pod Topology Spread treats "global minimum" as 0, and then the calculation of Skew is performed. And when the number of eligible domains with matching topology keys equals or greater than minDomains, this value has no effect on scheduling. As a result, when the number of eligible domains is less than minDomains, scheduler won't schedule more than maxSkew Pods to those domains. If value is nil, the constraint behaves as if MinDomains is equal to 1. Valid values are integers greater than 0. When value is not nil, WhenUnsatisfiable must be DoNotSchedule. 
 For example, in a 3-zone cluster, MaxSkew is set to 2, MinDomains is set to 5 and pods with the same labelSelector spread as 2/2/2: | zone1 | zone2 | zone3 | |  P P  |  P P  |  P P  | The number of domains is less than 5(MinDomains), so "global minimum" is treated as 0. In this situation, new pod with the same labelSelector cannot be scheduled, because computed skew will be 3(3 - 0) if new Pod is scheduled to any of the three zones, it will violate MaxSkew. 
 This is a beta field and requires the MinDomainsInPodTopologySpread feature gate to be enabled (enabled by default). |
| | || **Key**         | PerconaPGCluster.spec.backups.pgbackrest.repoHost.topologySpreadConstraints[index].nodeAffinityPolicy |
| **Value**       | string |
| **Required**    | false |
| **Example**     | |
| **Description** | NodeAffinityPolicy indicates how we will treat Pod's nodeAffinity/nodeSelector when calculating pod topology spread skew. Options are: - Honor: only nodes matching nodeAffinity/nodeSelector are included in the calculations. - Ignore: nodeAffinity/nodeSelector are ignored. All nodes are included in the calculations. 
 If this value is nil, the behavior is equivalent to the Honor policy. This is a alpha-level feature enabled by the NodeInclusionPolicyInPodTopologySpread feature flag. |
| | || **Key**         | PerconaPGCluster.spec.backups.pgbackrest.repoHost.topologySpreadConstraints[index].nodeTaintsPolicy |
| **Value**       | string |
| **Required**    | false |
| **Example**     | |
| **Description** | NodeTaintsPolicy indicates how we will treat node taints when calculating pod topology spread skew. Options are: - Honor: nodes without taints, along with tainted nodes for which the incoming pod has a toleration, are included. - Ignore: node taints are ignored. All nodes are included. 
 If this value is nil, the behavior is equivalent to the Ignore policy. This is a alpha-level feature enabled by the NodeInclusionPolicyInPodTopologySpread feature flag. |
| | |
| **Key**         | PerconaPGCluster.spec.backups.pgbackrest.repoHost.topologySpreadConstraints[index].labelSelector.matchExpressions |
| **Value**       | []object |
| **Required**    | false |
| **Example**     | |
| **Description** | matchExpressions is a list of label selector requirements. The requirements are ANDed. |
| | || **Key**         | PerconaPGCluster.spec.backups.pgbackrest.repoHost.topologySpreadConstraints[index].labelSelector.matchLabels |
| **Value**       | map[string]string |
| **Required**    | false |
| **Example**     | |
| **Description** | matchLabels is a map of {key,value} pairs. A single {key,value} in the matchLabels map is equivalent to an element of matchExpressions, whose key field is "key", the operator is "In", and the values array contains only "value". The requirements are ANDed. |
| | |
| **Key**         | PerconaPGCluster.spec.backups.pgbackrest.repoHost.topologySpreadConstraints[index].labelSelector.matchExpressions[index].key |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | key is the label key that the selector applies to. |
| | || **Key**         | PerconaPGCluster.spec.backups.pgbackrest.repoHost.topologySpreadConstraints[index].labelSelector.matchExpressions[index].operator |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | operator represents a key's relationship to a set of values. Valid operators are In, NotIn, Exists and DoesNotExist. |
| | || **Key**         | PerconaPGCluster.spec.backups.pgbackrest.repoHost.topologySpreadConstraints[index].labelSelector.matchExpressions[index].values |
| **Value**       | []string |
| **Required**    | false |
| **Example**     | |
| **Description** | values is an array of string values. If the operator is In or NotIn, the values array must be non-empty. If the operator is Exists or DoesNotExist, the values array must be empty. This array is replaced during a strategic merge patch. |
| | |
| **Key**         | PerconaPGCluster.spec.backups.pgbackrest.restore.enabled |
| **Value**       | boolean |
| **Required**    | true |
| **Example**     | |
| **Description** | Whether or not in-place pgBackRest restores are enabled for this PostgresCluster. |
| | || **Key**         | PerconaPGCluster.spec.backups.pgbackrest.restore.repoName |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | The name of the pgBackRest repo within the source PostgresCluster that contains the backups that should be utilized to perform a pgBackRest restore when initializing the data source for the new PostgresCluster. |
| | || **Key**         | PerconaPGCluster.spec.backups.pgbackrest.restore.affinity |
| **Value**       | object |
| **Required**    | false |
| **Example**     | |
| **Description** | Scheduling constraints of the pgBackRest restore Job. More info: https://kubernetes.io/docs/concepts/scheduling-eviction/assign-pod-node |
| | || **Key**         | PerconaPGCluster.spec.backups.pgbackrest.restore.clusterName |
| **Value**       | string |
| **Required**    | false |
| **Example**     | |
| **Description** | The name of an existing PostgresCluster to use as the data source for the new PostgresCluster. Defaults to the name of the PostgresCluster being created if not provided. |
| | || **Key**         | PerconaPGCluster.spec.backups.pgbackrest.restore.clusterNamespace |
| **Value**       | string |
| **Required**    | false |
| **Example**     | |
| **Description** | The namespace of the cluster specified as the data source using the clusterName field. Defaults to the namespace of the PostgresCluster being created if not provided. |
| | || **Key**         | PerconaPGCluster.spec.backups.pgbackrest.restore.options |
| **Value**       | []string |
| **Required**    | false |
| **Example**     | |
| **Description** | Command line options to include when running the pgBackRest restore command. https://pgbackrest.org/command.html#command-restore |
| | || **Key**         | PerconaPGCluster.spec.backups.pgbackrest.restore.priorityClassName |
| **Value**       | string |
| **Required**    | false |
| **Example**     | |
| **Description** | Priority class name for the pgBackRest restore Job pod. Changing this value causes PostgreSQL to restart. More info: https://kubernetes.io/docs/concepts/scheduling-eviction/pod-priority-preemption/ |
| | || **Key**         | PerconaPGCluster.spec.backups.pgbackrest.restore.resources |
| **Value**       | object |
| **Required**    | false |
| **Example**     | |
| **Description** | Resource requirements for the pgBackRest restore Job. |
| | || **Key**         | PerconaPGCluster.spec.backups.pgbackrest.restore.tolerations |
| **Value**       | []object |
| **Required**    | false |
| **Example**     | |
| **Description** | Tolerations of the pgBackRest restore Job. More info: https://kubernetes.io/docs/concepts/scheduling-eviction/taint-and-toleration |
| | |
| **Key**         | PerconaPGCluster.spec.backups.pgbackrest.restore.affinity.nodeAffinity |
| **Value**       | object |
| **Required**    | false |
| **Example**     | |
| **Description** | Describes node affinity scheduling rules for the pod. |
| | || **Key**         | PerconaPGCluster.spec.backups.pgbackrest.restore.affinity.podAffinity |
| **Value**       | object |
| **Required**    | false |
| **Example**     | |
| **Description** | Describes pod affinity scheduling rules (e.g. co-locate this pod in the same node, zone, etc. as some other pod(s)). |
| | || **Key**         | PerconaPGCluster.spec.backups.pgbackrest.restore.affinity.podAntiAffinity |
| **Value**       | object |
| **Required**    | false |
| **Example**     | |
| **Description** | Describes pod anti-affinity scheduling rules (e.g. avoid putting this pod in the same node, zone, etc. as some other pod(s)). |
| | |
| **Key**         | PerconaPGCluster.spec.backups.pgbackrest.restore.affinity.nodeAffinity.preferredDuringSchedulingIgnoredDuringExecution |
| **Value**       | []object |
| **Required**    | false |
| **Example**     | |
| **Description** | The scheduler will prefer to schedule pods to nodes that satisfy the affinity expressions specified by this field, but it may choose a node that violates one or more of the expressions. The node that is most preferred is the one with the greatest sum of weights, i.e. for each node that meets all of the scheduling requirements (resource request, requiredDuringScheduling affinity expressions, etc.), compute a sum by iterating through the elements of this field and adding "weight" to the sum if the node matches the corresponding matchExpressions; the node(s) with the highest sum are the most preferred. |
| | || **Key**         | PerconaPGCluster.spec.backups.pgbackrest.restore.affinity.nodeAffinity.requiredDuringSchedulingIgnoredDuringExecution |
| **Value**       | object |
| **Required**    | false |
| **Example**     | |
| **Description** | If the affinity requirements specified by this field are not met at scheduling time, the pod will not be scheduled onto the node. If the affinity requirements specified by this field cease to be met at some point during pod execution (e.g. due to an update), the system may or may not try to eventually evict the pod from its node. |
| | |
| **Key**         | PerconaPGCluster.spec.backups.pgbackrest.restore.affinity.nodeAffinity.preferredDuringSchedulingIgnoredDuringExecution[index].preference |
| **Value**       | object |
| **Required**    | true |
| **Example**     | |
| **Description** | A node selector term, associated with the corresponding weight. |
| | || **Key**         | PerconaPGCluster.spec.backups.pgbackrest.restore.affinity.nodeAffinity.preferredDuringSchedulingIgnoredDuringExecution[index].weight |
| **Value**       | integer |
| **Required**    | true |
| **Example**     | |
| **Description** | Weight associated with matching the corresponding nodeSelectorTerm, in the range 1-100. |
| | |
| **Key**         | PerconaPGCluster.spec.backups.pgbackrest.restore.affinity.nodeAffinity.preferredDuringSchedulingIgnoredDuringExecution[index].preference.matchExpressions |
| **Value**       | []object |
| **Required**    | false |
| **Example**     | |
| **Description** | A list of node selector requirements by node's labels. |
| | || **Key**         | PerconaPGCluster.spec.backups.pgbackrest.restore.affinity.nodeAffinity.preferredDuringSchedulingIgnoredDuringExecution[index].preference.matchFields |
| **Value**       | []object |
| **Required**    | false |
| **Example**     | |
| **Description** | A list of node selector requirements by node's fields. |
| | |
| **Key**         | PerconaPGCluster.spec.backups.pgbackrest.restore.affinity.nodeAffinity.preferredDuringSchedulingIgnoredDuringExecution[index].preference.matchExpressions[index].key |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | The label key that the selector applies to. |
| | || **Key**         | PerconaPGCluster.spec.backups.pgbackrest.restore.affinity.nodeAffinity.preferredDuringSchedulingIgnoredDuringExecution[index].preference.matchExpressions[index].operator |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | Represents a key's relationship to a set of values. Valid operators are In, NotIn, Exists, DoesNotExist. Gt, and Lt. |
| | || **Key**         | PerconaPGCluster.spec.backups.pgbackrest.restore.affinity.nodeAffinity.preferredDuringSchedulingIgnoredDuringExecution[index].preference.matchExpressions[index].values |
| **Value**       | []string |
| **Required**    | false |
| **Example**     | |
| **Description** | An array of string values. If the operator is In or NotIn, the values array must be non-empty. If the operator is Exists or DoesNotExist, the values array must be empty. If the operator is Gt or Lt, the values array must have a single element, which will be interpreted as an integer. This array is replaced during a strategic merge patch. |
| | |
| **Key**         | PerconaPGCluster.spec.backups.pgbackrest.restore.affinity.nodeAffinity.preferredDuringSchedulingIgnoredDuringExecution[index].preference.matchFields[index].key |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | The label key that the selector applies to. |
| | || **Key**         | PerconaPGCluster.spec.backups.pgbackrest.restore.affinity.nodeAffinity.preferredDuringSchedulingIgnoredDuringExecution[index].preference.matchFields[index].operator |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | Represents a key's relationship to a set of values. Valid operators are In, NotIn, Exists, DoesNotExist. Gt, and Lt. |
| | || **Key**         | PerconaPGCluster.spec.backups.pgbackrest.restore.affinity.nodeAffinity.preferredDuringSchedulingIgnoredDuringExecution[index].preference.matchFields[index].values |
| **Value**       | []string |
| **Required**    | false |
| **Example**     | |
| **Description** | An array of string values. If the operator is In or NotIn, the values array must be non-empty. If the operator is Exists or DoesNotExist, the values array must be empty. If the operator is Gt or Lt, the values array must have a single element, which will be interpreted as an integer. This array is replaced during a strategic merge patch. |
| | |
| **Key**         | PerconaPGCluster.spec.backups.pgbackrest.restore.affinity.nodeAffinity.requiredDuringSchedulingIgnoredDuringExecution.nodeSelectorTerms |
| **Value**       | []object |
| **Required**    | true |
| **Example**     | |
| **Description** | Required. A list of node selector terms. The terms are ORed. |
| | |
| **Key**         | PerconaPGCluster.spec.backups.pgbackrest.restore.affinity.nodeAffinity.requiredDuringSchedulingIgnoredDuringExecution.nodeSelectorTerms[index].matchExpressions |
| **Value**       | []object |
| **Required**    | false |
| **Example**     | |
| **Description** | A list of node selector requirements by node's labels. |
| | || **Key**         | PerconaPGCluster.spec.backups.pgbackrest.restore.affinity.nodeAffinity.requiredDuringSchedulingIgnoredDuringExecution.nodeSelectorTerms[index].matchFields |
| **Value**       | []object |
| **Required**    | false |
| **Example**     | |
| **Description** | A list of node selector requirements by node's fields. |
| | |
| **Key**         | PerconaPGCluster.spec.backups.pgbackrest.restore.affinity.nodeAffinity.requiredDuringSchedulingIgnoredDuringExecution.nodeSelectorTerms[index].matchExpressions[index].key |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | The label key that the selector applies to. |
| | || **Key**         | PerconaPGCluster.spec.backups.pgbackrest.restore.affinity.nodeAffinity.requiredDuringSchedulingIgnoredDuringExecution.nodeSelectorTerms[index].matchExpressions[index].operator |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | Represents a key's relationship to a set of values. Valid operators are In, NotIn, Exists, DoesNotExist. Gt, and Lt. |
| | || **Key**         | PerconaPGCluster.spec.backups.pgbackrest.restore.affinity.nodeAffinity.requiredDuringSchedulingIgnoredDuringExecution.nodeSelectorTerms[index].matchExpressions[index].values |
| **Value**       | []string |
| **Required**    | false |
| **Example**     | |
| **Description** | An array of string values. If the operator is In or NotIn, the values array must be non-empty. If the operator is Exists or DoesNotExist, the values array must be empty. If the operator is Gt or Lt, the values array must have a single element, which will be interpreted as an integer. This array is replaced during a strategic merge patch. |
| | |
| **Key**         | PerconaPGCluster.spec.backups.pgbackrest.restore.affinity.nodeAffinity.requiredDuringSchedulingIgnoredDuringExecution.nodeSelectorTerms[index].matchFields[index].key |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | The label key that the selector applies to. |
| | || **Key**         | PerconaPGCluster.spec.backups.pgbackrest.restore.affinity.nodeAffinity.requiredDuringSchedulingIgnoredDuringExecution.nodeSelectorTerms[index].matchFields[index].operator |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | Represents a key's relationship to a set of values. Valid operators are In, NotIn, Exists, DoesNotExist. Gt, and Lt. |
| | || **Key**         | PerconaPGCluster.spec.backups.pgbackrest.restore.affinity.nodeAffinity.requiredDuringSchedulingIgnoredDuringExecution.nodeSelectorTerms[index].matchFields[index].values |
| **Value**       | []string |
| **Required**    | false |
| **Example**     | |
| **Description** | An array of string values. If the operator is In or NotIn, the values array must be non-empty. If the operator is Exists or DoesNotExist, the values array must be empty. If the operator is Gt or Lt, the values array must have a single element, which will be interpreted as an integer. This array is replaced during a strategic merge patch. |
| | |
| **Key**         | PerconaPGCluster.spec.backups.pgbackrest.restore.affinity.podAffinity.preferredDuringSchedulingIgnoredDuringExecution |
| **Value**       | []object |
| **Required**    | false |
| **Example**     | |
| **Description** | The scheduler will prefer to schedule pods to nodes that satisfy the affinity expressions specified by this field, but it may choose a node that violates one or more of the expressions. The node that is most preferred is the one with the greatest sum of weights, i.e. for each node that meets all of the scheduling requirements (resource request, requiredDuringScheduling affinity expressions, etc.), compute a sum by iterating through the elements of this field and adding "weight" to the sum if the node has pods which matches the corresponding podAffinityTerm; the node(s) with the highest sum are the most preferred. |
| | || **Key**         | PerconaPGCluster.spec.backups.pgbackrest.restore.affinity.podAffinity.requiredDuringSchedulingIgnoredDuringExecution |
| **Value**       | []object |
| **Required**    | false |
| **Example**     | |
| **Description** | If the affinity requirements specified by this field are not met at scheduling time, the pod will not be scheduled onto the node. If the affinity requirements specified by this field cease to be met at some point during pod execution (e.g. due to a pod label update), the system may or may not try to eventually evict the pod from its node. When there are multiple elements, the lists of nodes corresponding to each podAffinityTerm are intersected, i.e. all terms must be satisfied. |
| | |
| **Key**         | PerconaPGCluster.spec.backups.pgbackrest.restore.affinity.podAffinity.preferredDuringSchedulingIgnoredDuringExecution[index].podAffinityTerm |
| **Value**       | object |
| **Required**    | true |
| **Example**     | |
| **Description** | Required. A pod affinity term, associated with the corresponding weight. |
| | || **Key**         | PerconaPGCluster.spec.backups.pgbackrest.restore.affinity.podAffinity.preferredDuringSchedulingIgnoredDuringExecution[index].weight |
| **Value**       | integer |
| **Required**    | true |
| **Example**     | |
| **Description** | weight associated with matching the corresponding podAffinityTerm, in the range 1-100. |
| | |
| **Key**         | PerconaPGCluster.spec.backups.pgbackrest.restore.affinity.podAffinity.preferredDuringSchedulingIgnoredDuringExecution[index].podAffinityTerm.topologyKey |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | This pod should be co-located (affinity) or not co-located (anti-affinity) with the pods matching the labelSelector in the specified namespaces, where co-located is defined as running on a node whose value of the label with key topologyKey matches that of any node on which any of the selected pods is running. Empty topologyKey is not allowed. |
| | || **Key**         | PerconaPGCluster.spec.backups.pgbackrest.restore.affinity.podAffinity.preferredDuringSchedulingIgnoredDuringExecution[index].podAffinityTerm.labelSelector |
| **Value**       | object |
| **Required**    | false |
| **Example**     | |
| **Description** | A label query over a set of resources, in this case pods. |
| | || **Key**         | PerconaPGCluster.spec.backups.pgbackrest.restore.affinity.podAffinity.preferredDuringSchedulingIgnoredDuringExecution[index].podAffinityTerm.namespaceSelector |
| **Value**       | object |
| **Required**    | false |
| **Example**     | |
| **Description** | A label query over the set of namespaces that the term applies to. The term is applied to the union of the namespaces selected by this field and the ones listed in the namespaces field. null selector and null or empty namespaces list means "this pod's namespace". An empty selector ({}) matches all namespaces. |
| | || **Key**         | PerconaPGCluster.spec.backups.pgbackrest.restore.affinity.podAffinity.preferredDuringSchedulingIgnoredDuringExecution[index].podAffinityTerm.namespaces |
| **Value**       | []string |
| **Required**    | false |
| **Example**     | |
| **Description** | namespaces specifies a static list of namespace names that the term applies to. The term is applied to the union of the namespaces listed in this field and the ones selected by namespaceSelector. null or empty namespaces list and null namespaceSelector means "this pod's namespace". |
| | |
| **Key**         | PerconaPGCluster.spec.backups.pgbackrest.restore.affinity.podAffinity.preferredDuringSchedulingIgnoredDuringExecution[index].podAffinityTerm.labelSelector.matchExpressions |
| **Value**       | []object |
| **Required**    | false |
| **Example**     | |
| **Description** | matchExpressions is a list of label selector requirements. The requirements are ANDed. |
| | || **Key**         | PerconaPGCluster.spec.backups.pgbackrest.restore.affinity.podAffinity.preferredDuringSchedulingIgnoredDuringExecution[index].podAffinityTerm.labelSelector.matchLabels |
| **Value**       | map[string]string |
| **Required**    | false |
| **Example**     | |
| **Description** | matchLabels is a map of {key,value} pairs. A single {key,value} in the matchLabels map is equivalent to an element of matchExpressions, whose key field is "key", the operator is "In", and the values array contains only "value". The requirements are ANDed. |
| | |
| **Key**         | PerconaPGCluster.spec.backups.pgbackrest.restore.affinity.podAffinity.preferredDuringSchedulingIgnoredDuringExecution[index].podAffinityTerm.labelSelector.matchExpressions[index].key |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | key is the label key that the selector applies to. |
| | || **Key**         | PerconaPGCluster.spec.backups.pgbackrest.restore.affinity.podAffinity.preferredDuringSchedulingIgnoredDuringExecution[index].podAffinityTerm.labelSelector.matchExpressions[index].operator |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | operator represents a key's relationship to a set of values. Valid operators are In, NotIn, Exists and DoesNotExist. |
| | || **Key**         | PerconaPGCluster.spec.backups.pgbackrest.restore.affinity.podAffinity.preferredDuringSchedulingIgnoredDuringExecution[index].podAffinityTerm.labelSelector.matchExpressions[index].values |
| **Value**       | []string |
| **Required**    | false |
| **Example**     | |
| **Description** | values is an array of string values. If the operator is In or NotIn, the values array must be non-empty. If the operator is Exists or DoesNotExist, the values array must be empty. This array is replaced during a strategic merge patch. |
| | |
| **Key**         | PerconaPGCluster.spec.backups.pgbackrest.restore.affinity.podAffinity.preferredDuringSchedulingIgnoredDuringExecution[index].podAffinityTerm.namespaceSelector.matchExpressions |
| **Value**       | []object |
| **Required**    | false |
| **Example**     | |
| **Description** | matchExpressions is a list of label selector requirements. The requirements are ANDed. |
| | || **Key**         | PerconaPGCluster.spec.backups.pgbackrest.restore.affinity.podAffinity.preferredDuringSchedulingIgnoredDuringExecution[index].podAffinityTerm.namespaceSelector.matchLabels |
| **Value**       | map[string]string |
| **Required**    | false |
| **Example**     | |
| **Description** | matchLabels is a map of {key,value} pairs. A single {key,value} in the matchLabels map is equivalent to an element of matchExpressions, whose key field is "key", the operator is "In", and the values array contains only "value". The requirements are ANDed. |
| | |
| **Key**         | PerconaPGCluster.spec.backups.pgbackrest.restore.affinity.podAffinity.preferredDuringSchedulingIgnoredDuringExecution[index].podAffinityTerm.namespaceSelector.matchExpressions[index].key |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | key is the label key that the selector applies to. |
| | || **Key**         | PerconaPGCluster.spec.backups.pgbackrest.restore.affinity.podAffinity.preferredDuringSchedulingIgnoredDuringExecution[index].podAffinityTerm.namespaceSelector.matchExpressions[index].operator |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | operator represents a key's relationship to a set of values. Valid operators are In, NotIn, Exists and DoesNotExist. |
| | || **Key**         | PerconaPGCluster.spec.backups.pgbackrest.restore.affinity.podAffinity.preferredDuringSchedulingIgnoredDuringExecution[index].podAffinityTerm.namespaceSelector.matchExpressions[index].values |
| **Value**       | []string |
| **Required**    | false |
| **Example**     | |
| **Description** | values is an array of string values. If the operator is In or NotIn, the values array must be non-empty. If the operator is Exists or DoesNotExist, the values array must be empty. This array is replaced during a strategic merge patch. |
| | |
| **Key**         | PerconaPGCluster.spec.backups.pgbackrest.restore.affinity.podAffinity.requiredDuringSchedulingIgnoredDuringExecution[index].topologyKey |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | This pod should be co-located (affinity) or not co-located (anti-affinity) with the pods matching the labelSelector in the specified namespaces, where co-located is defined as running on a node whose value of the label with key topologyKey matches that of any node on which any of the selected pods is running. Empty topologyKey is not allowed. |
| | || **Key**         | PerconaPGCluster.spec.backups.pgbackrest.restore.affinity.podAffinity.requiredDuringSchedulingIgnoredDuringExecution[index].labelSelector |
| **Value**       | object |
| **Required**    | false |
| **Example**     | |
| **Description** | A label query over a set of resources, in this case pods. |
| | || **Key**         | PerconaPGCluster.spec.backups.pgbackrest.restore.affinity.podAffinity.requiredDuringSchedulingIgnoredDuringExecution[index].namespaceSelector |
| **Value**       | object |
| **Required**    | false |
| **Example**     | |
| **Description** | A label query over the set of namespaces that the term applies to. The term is applied to the union of the namespaces selected by this field and the ones listed in the namespaces field. null selector and null or empty namespaces list means "this pod's namespace". An empty selector ({}) matches all namespaces. |
| | || **Key**         | PerconaPGCluster.spec.backups.pgbackrest.restore.affinity.podAffinity.requiredDuringSchedulingIgnoredDuringExecution[index].namespaces |
| **Value**       | []string |
| **Required**    | false |
| **Example**     | |
| **Description** | namespaces specifies a static list of namespace names that the term applies to. The term is applied to the union of the namespaces listed in this field and the ones selected by namespaceSelector. null or empty namespaces list and null namespaceSelector means "this pod's namespace". |
| | |
| **Key**         | PerconaPGCluster.spec.backups.pgbackrest.restore.affinity.podAffinity.requiredDuringSchedulingIgnoredDuringExecution[index].labelSelector.matchExpressions |
| **Value**       | []object |
| **Required**    | false |
| **Example**     | |
| **Description** | matchExpressions is a list of label selector requirements. The requirements are ANDed. |
| | || **Key**         | PerconaPGCluster.spec.backups.pgbackrest.restore.affinity.podAffinity.requiredDuringSchedulingIgnoredDuringExecution[index].labelSelector.matchLabels |
| **Value**       | map[string]string |
| **Required**    | false |
| **Example**     | |
| **Description** | matchLabels is a map of {key,value} pairs. A single {key,value} in the matchLabels map is equivalent to an element of matchExpressions, whose key field is "key", the operator is "In", and the values array contains only "value". The requirements are ANDed. |
| | |
| **Key**         | PerconaPGCluster.spec.backups.pgbackrest.restore.affinity.podAffinity.requiredDuringSchedulingIgnoredDuringExecution[index].labelSelector.matchExpressions[index].key |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | key is the label key that the selector applies to. |
| | || **Key**         | PerconaPGCluster.spec.backups.pgbackrest.restore.affinity.podAffinity.requiredDuringSchedulingIgnoredDuringExecution[index].labelSelector.matchExpressions[index].operator |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | operator represents a key's relationship to a set of values. Valid operators are In, NotIn, Exists and DoesNotExist. |
| | || **Key**         | PerconaPGCluster.spec.backups.pgbackrest.restore.affinity.podAffinity.requiredDuringSchedulingIgnoredDuringExecution[index].labelSelector.matchExpressions[index].values |
| **Value**       | []string |
| **Required**    | false |
| **Example**     | |
| **Description** | values is an array of string values. If the operator is In or NotIn, the values array must be non-empty. If the operator is Exists or DoesNotExist, the values array must be empty. This array is replaced during a strategic merge patch. |
| | |
| **Key**         | PerconaPGCluster.spec.backups.pgbackrest.restore.affinity.podAffinity.requiredDuringSchedulingIgnoredDuringExecution[index].namespaceSelector.matchExpressions |
| **Value**       | []object |
| **Required**    | false |
| **Example**     | |
| **Description** | matchExpressions is a list of label selector requirements. The requirements are ANDed. |
| | || **Key**         | PerconaPGCluster.spec.backups.pgbackrest.restore.affinity.podAffinity.requiredDuringSchedulingIgnoredDuringExecution[index].namespaceSelector.matchLabels |
| **Value**       | map[string]string |
| **Required**    | false |
| **Example**     | |
| **Description** | matchLabels is a map of {key,value} pairs. A single {key,value} in the matchLabels map is equivalent to an element of matchExpressions, whose key field is "key", the operator is "In", and the values array contains only "value". The requirements are ANDed. |
| | |
| **Key**         | PerconaPGCluster.spec.backups.pgbackrest.restore.affinity.podAffinity.requiredDuringSchedulingIgnoredDuringExecution[index].namespaceSelector.matchExpressions[index].key |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | key is the label key that the selector applies to. |
| | || **Key**         | PerconaPGCluster.spec.backups.pgbackrest.restore.affinity.podAffinity.requiredDuringSchedulingIgnoredDuringExecution[index].namespaceSelector.matchExpressions[index].operator |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | operator represents a key's relationship to a set of values. Valid operators are In, NotIn, Exists and DoesNotExist. |
| | || **Key**         | PerconaPGCluster.spec.backups.pgbackrest.restore.affinity.podAffinity.requiredDuringSchedulingIgnoredDuringExecution[index].namespaceSelector.matchExpressions[index].values |
| **Value**       | []string |
| **Required**    | false |
| **Example**     | |
| **Description** | values is an array of string values. If the operator is In or NotIn, the values array must be non-empty. If the operator is Exists or DoesNotExist, the values array must be empty. This array is replaced during a strategic merge patch. |
| | |
| **Key**         | PerconaPGCluster.spec.backups.pgbackrest.restore.affinity.podAntiAffinity.preferredDuringSchedulingIgnoredDuringExecution |
| **Value**       | []object |
| **Required**    | false |
| **Example**     | |
| **Description** | The scheduler will prefer to schedule pods to nodes that satisfy the anti-affinity expressions specified by this field, but it may choose a node that violates one or more of the expressions. The node that is most preferred is the one with the greatest sum of weights, i.e. for each node that meets all of the scheduling requirements (resource request, requiredDuringScheduling anti-affinity expressions, etc.), compute a sum by iterating through the elements of this field and adding "weight" to the sum if the node has pods which matches the corresponding podAffinityTerm; the node(s) with the highest sum are the most preferred. |
| | || **Key**         | PerconaPGCluster.spec.backups.pgbackrest.restore.affinity.podAntiAffinity.requiredDuringSchedulingIgnoredDuringExecution |
| **Value**       | []object |
| **Required**    | false |
| **Example**     | |
| **Description** | If the anti-affinity requirements specified by this field are not met at scheduling time, the pod will not be scheduled onto the node. If the anti-affinity requirements specified by this field cease to be met at some point during pod execution (e.g. due to a pod label update), the system may or may not try to eventually evict the pod from its node. When there are multiple elements, the lists of nodes corresponding to each podAffinityTerm are intersected, i.e. all terms must be satisfied. |
| | |
| **Key**         | PerconaPGCluster.spec.backups.pgbackrest.restore.affinity.podAntiAffinity.preferredDuringSchedulingIgnoredDuringExecution[index].podAffinityTerm |
| **Value**       | object |
| **Required**    | true |
| **Example**     | |
| **Description** | Required. A pod affinity term, associated with the corresponding weight. |
| | || **Key**         | PerconaPGCluster.spec.backups.pgbackrest.restore.affinity.podAntiAffinity.preferredDuringSchedulingIgnoredDuringExecution[index].weight |
| **Value**       | integer |
| **Required**    | true |
| **Example**     | |
| **Description** | weight associated with matching the corresponding podAffinityTerm, in the range 1-100. |
| | |
| **Key**         | PerconaPGCluster.spec.backups.pgbackrest.restore.affinity.podAntiAffinity.preferredDuringSchedulingIgnoredDuringExecution[index].podAffinityTerm.topologyKey |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | This pod should be co-located (affinity) or not co-located (anti-affinity) with the pods matching the labelSelector in the specified namespaces, where co-located is defined as running on a node whose value of the label with key topologyKey matches that of any node on which any of the selected pods is running. Empty topologyKey is not allowed. |
| | || **Key**         | PerconaPGCluster.spec.backups.pgbackrest.restore.affinity.podAntiAffinity.preferredDuringSchedulingIgnoredDuringExecution[index].podAffinityTerm.labelSelector |
| **Value**       | object |
| **Required**    | false |
| **Example**     | |
| **Description** | A label query over a set of resources, in this case pods. |
| | || **Key**         | PerconaPGCluster.spec.backups.pgbackrest.restore.affinity.podAntiAffinity.preferredDuringSchedulingIgnoredDuringExecution[index].podAffinityTerm.namespaceSelector |
| **Value**       | object |
| **Required**    | false |
| **Example**     | |
| **Description** | A label query over the set of namespaces that the term applies to. The term is applied to the union of the namespaces selected by this field and the ones listed in the namespaces field. null selector and null or empty namespaces list means "this pod's namespace". An empty selector ({}) matches all namespaces. |
| | || **Key**         | PerconaPGCluster.spec.backups.pgbackrest.restore.affinity.podAntiAffinity.preferredDuringSchedulingIgnoredDuringExecution[index].podAffinityTerm.namespaces |
| **Value**       | []string |
| **Required**    | false |
| **Example**     | |
| **Description** | namespaces specifies a static list of namespace names that the term applies to. The term is applied to the union of the namespaces listed in this field and the ones selected by namespaceSelector. null or empty namespaces list and null namespaceSelector means "this pod's namespace". |
| | |
| **Key**         | PerconaPGCluster.spec.backups.pgbackrest.restore.affinity.podAntiAffinity.preferredDuringSchedulingIgnoredDuringExecution[index].podAffinityTerm.labelSelector.matchExpressions |
| **Value**       | []object |
| **Required**    | false |
| **Example**     | |
| **Description** | matchExpressions is a list of label selector requirements. The requirements are ANDed. |
| | || **Key**         | PerconaPGCluster.spec.backups.pgbackrest.restore.affinity.podAntiAffinity.preferredDuringSchedulingIgnoredDuringExecution[index].podAffinityTerm.labelSelector.matchLabels |
| **Value**       | map[string]string |
| **Required**    | false |
| **Example**     | |
| **Description** | matchLabels is a map of {key,value} pairs. A single {key,value} in the matchLabels map is equivalent to an element of matchExpressions, whose key field is "key", the operator is "In", and the values array contains only "value". The requirements are ANDed. |
| | |
| **Key**         | PerconaPGCluster.spec.backups.pgbackrest.restore.affinity.podAntiAffinity.preferredDuringSchedulingIgnoredDuringExecution[index].podAffinityTerm.labelSelector.matchExpressions[index].key |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | key is the label key that the selector applies to. |
| | || **Key**         | PerconaPGCluster.spec.backups.pgbackrest.restore.affinity.podAntiAffinity.preferredDuringSchedulingIgnoredDuringExecution[index].podAffinityTerm.labelSelector.matchExpressions[index].operator |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | operator represents a key's relationship to a set of values. Valid operators are In, NotIn, Exists and DoesNotExist. |
| | || **Key**         | PerconaPGCluster.spec.backups.pgbackrest.restore.affinity.podAntiAffinity.preferredDuringSchedulingIgnoredDuringExecution[index].podAffinityTerm.labelSelector.matchExpressions[index].values |
| **Value**       | []string |
| **Required**    | false |
| **Example**     | |
| **Description** | values is an array of string values. If the operator is In or NotIn, the values array must be non-empty. If the operator is Exists or DoesNotExist, the values array must be empty. This array is replaced during a strategic merge patch. |
| | |
| **Key**         | PerconaPGCluster.spec.backups.pgbackrest.restore.affinity.podAntiAffinity.preferredDuringSchedulingIgnoredDuringExecution[index].podAffinityTerm.namespaceSelector.matchExpressions |
| **Value**       | []object |
| **Required**    | false |
| **Example**     | |
| **Description** | matchExpressions is a list of label selector requirements. The requirements are ANDed. |
| | || **Key**         | PerconaPGCluster.spec.backups.pgbackrest.restore.affinity.podAntiAffinity.preferredDuringSchedulingIgnoredDuringExecution[index].podAffinityTerm.namespaceSelector.matchLabels |
| **Value**       | map[string]string |
| **Required**    | false |
| **Example**     | |
| **Description** | matchLabels is a map of {key,value} pairs. A single {key,value} in the matchLabels map is equivalent to an element of matchExpressions, whose key field is "key", the operator is "In", and the values array contains only "value". The requirements are ANDed. |
| | |
| **Key**         | PerconaPGCluster.spec.backups.pgbackrest.restore.affinity.podAntiAffinity.preferredDuringSchedulingIgnoredDuringExecution[index].podAffinityTerm.namespaceSelector.matchExpressions[index].key |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | key is the label key that the selector applies to. |
| | || **Key**         | PerconaPGCluster.spec.backups.pgbackrest.restore.affinity.podAntiAffinity.preferredDuringSchedulingIgnoredDuringExecution[index].podAffinityTerm.namespaceSelector.matchExpressions[index].operator |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | operator represents a key's relationship to a set of values. Valid operators are In, NotIn, Exists and DoesNotExist. |
| | || **Key**         | PerconaPGCluster.spec.backups.pgbackrest.restore.affinity.podAntiAffinity.preferredDuringSchedulingIgnoredDuringExecution[index].podAffinityTerm.namespaceSelector.matchExpressions[index].values |
| **Value**       | []string |
| **Required**    | false |
| **Example**     | |
| **Description** | values is an array of string values. If the operator is In or NotIn, the values array must be non-empty. If the operator is Exists or DoesNotExist, the values array must be empty. This array is replaced during a strategic merge patch. |
| | |
| **Key**         | PerconaPGCluster.spec.backups.pgbackrest.restore.affinity.podAntiAffinity.requiredDuringSchedulingIgnoredDuringExecution[index].topologyKey |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | This pod should be co-located (affinity) or not co-located (anti-affinity) with the pods matching the labelSelector in the specified namespaces, where co-located is defined as running on a node whose value of the label with key topologyKey matches that of any node on which any of the selected pods is running. Empty topologyKey is not allowed. |
| | || **Key**         | PerconaPGCluster.spec.backups.pgbackrest.restore.affinity.podAntiAffinity.requiredDuringSchedulingIgnoredDuringExecution[index].labelSelector |
| **Value**       | object |
| **Required**    | false |
| **Example**     | |
| **Description** | A label query over a set of resources, in this case pods. |
| | || **Key**         | PerconaPGCluster.spec.backups.pgbackrest.restore.affinity.podAntiAffinity.requiredDuringSchedulingIgnoredDuringExecution[index].namespaceSelector |
| **Value**       | object |
| **Required**    | false |
| **Example**     | |
| **Description** | A label query over the set of namespaces that the term applies to. The term is applied to the union of the namespaces selected by this field and the ones listed in the namespaces field. null selector and null or empty namespaces list means "this pod's namespace". An empty selector ({}) matches all namespaces. |
| | || **Key**         | PerconaPGCluster.spec.backups.pgbackrest.restore.affinity.podAntiAffinity.requiredDuringSchedulingIgnoredDuringExecution[index].namespaces |
| **Value**       | []string |
| **Required**    | false |
| **Example**     | |
| **Description** | namespaces specifies a static list of namespace names that the term applies to. The term is applied to the union of the namespaces listed in this field and the ones selected by namespaceSelector. null or empty namespaces list and null namespaceSelector means "this pod's namespace". |
| | |
| **Key**         | PerconaPGCluster.spec.backups.pgbackrest.restore.affinity.podAntiAffinity.requiredDuringSchedulingIgnoredDuringExecution[index].labelSelector.matchExpressions |
| **Value**       | []object |
| **Required**    | false |
| **Example**     | |
| **Description** | matchExpressions is a list of label selector requirements. The requirements are ANDed. |
| | || **Key**         | PerconaPGCluster.spec.backups.pgbackrest.restore.affinity.podAntiAffinity.requiredDuringSchedulingIgnoredDuringExecution[index].labelSelector.matchLabels |
| **Value**       | map[string]string |
| **Required**    | false |
| **Example**     | |
| **Description** | matchLabels is a map of {key,value} pairs. A single {key,value} in the matchLabels map is equivalent to an element of matchExpressions, whose key field is "key", the operator is "In", and the values array contains only "value". The requirements are ANDed. |
| | |
| **Key**         | PerconaPGCluster.spec.backups.pgbackrest.restore.affinity.podAntiAffinity.requiredDuringSchedulingIgnoredDuringExecution[index].labelSelector.matchExpressions[index].key |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | key is the label key that the selector applies to. |
| | || **Key**         | PerconaPGCluster.spec.backups.pgbackrest.restore.affinity.podAntiAffinity.requiredDuringSchedulingIgnoredDuringExecution[index].labelSelector.matchExpressions[index].operator |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | operator represents a key's relationship to a set of values. Valid operators are In, NotIn, Exists and DoesNotExist. |
| | || **Key**         | PerconaPGCluster.spec.backups.pgbackrest.restore.affinity.podAntiAffinity.requiredDuringSchedulingIgnoredDuringExecution[index].labelSelector.matchExpressions[index].values |
| **Value**       | []string |
| **Required**    | false |
| **Example**     | |
| **Description** | values is an array of string values. If the operator is In or NotIn, the values array must be non-empty. If the operator is Exists or DoesNotExist, the values array must be empty. This array is replaced during a strategic merge patch. |
| | |
| **Key**         | PerconaPGCluster.spec.backups.pgbackrest.restore.affinity.podAntiAffinity.requiredDuringSchedulingIgnoredDuringExecution[index].namespaceSelector.matchExpressions |
| **Value**       | []object |
| **Required**    | false |
| **Example**     | |
| **Description** | matchExpressions is a list of label selector requirements. The requirements are ANDed. |
| | || **Key**         | PerconaPGCluster.spec.backups.pgbackrest.restore.affinity.podAntiAffinity.requiredDuringSchedulingIgnoredDuringExecution[index].namespaceSelector.matchLabels |
| **Value**       | map[string]string |
| **Required**    | false |
| **Example**     | |
| **Description** | matchLabels is a map of {key,value} pairs. A single {key,value} in the matchLabels map is equivalent to an element of matchExpressions, whose key field is "key", the operator is "In", and the values array contains only "value". The requirements are ANDed. |
| | |
| **Key**         | PerconaPGCluster.spec.backups.pgbackrest.restore.affinity.podAntiAffinity.requiredDuringSchedulingIgnoredDuringExecution[index].namespaceSelector.matchExpressions[index].key |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | key is the label key that the selector applies to. |
| | || **Key**         | PerconaPGCluster.spec.backups.pgbackrest.restore.affinity.podAntiAffinity.requiredDuringSchedulingIgnoredDuringExecution[index].namespaceSelector.matchExpressions[index].operator |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | operator represents a key's relationship to a set of values. Valid operators are In, NotIn, Exists and DoesNotExist. |
| | || **Key**         | PerconaPGCluster.spec.backups.pgbackrest.restore.affinity.podAntiAffinity.requiredDuringSchedulingIgnoredDuringExecution[index].namespaceSelector.matchExpressions[index].values |
| **Value**       | []string |
| **Required**    | false |
| **Example**     | |
| **Description** | values is an array of string values. If the operator is In or NotIn, the values array must be non-empty. If the operator is Exists or DoesNotExist, the values array must be empty. This array is replaced during a strategic merge patch. |
| | |
| **Key**         | PerconaPGCluster.spec.backups.pgbackrest.restore.resources.limits |
| **Value**       | map[string]int or string |
| **Required**    | false |
| **Example**     | |
| **Description** | Limits describes the maximum amount of compute resources allowed. More info: https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/ |
| | || **Key**         | PerconaPGCluster.spec.backups.pgbackrest.restore.resources.requests |
| **Value**       | map[string]int or string |
| **Required**    | false |
| **Example**     | |
| **Description** | Requests describes the minimum amount of compute resources required. If Requests is omitted for a container, it defaults to Limits if that is explicitly specified, otherwise to an implementation-defined value. More info: https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/ |
| | |
| **Key**         | PerconaPGCluster.spec.backups.pgbackrest.restore.tolerations[index].effect |
| **Value**       | string |
| **Required**    | false |
| **Example**     | |
| **Description** | Effect indicates the taint effect to match. Empty means match all taint effects. When specified, allowed values are NoSchedule, PreferNoSchedule and NoExecute. |
| | || **Key**         | PerconaPGCluster.spec.backups.pgbackrest.restore.tolerations[index].key |
| **Value**       | string |
| **Required**    | false |
| **Example**     | |
| **Description** | Key is the taint key that the toleration applies to. Empty means match all taint keys. If the key is empty, operator must be Exists; this combination means to match all values and all keys. |
| | || **Key**         | PerconaPGCluster.spec.backups.pgbackrest.restore.tolerations[index].operator |
| **Value**       | string |
| **Required**    | false |
| **Example**     | |
| **Description** | Operator represents a key's relationship to the value. Valid operators are Exists and Equal. Defaults to Equal. Exists is equivalent to wildcard for value, so that a pod can tolerate all taints of a particular category. |
| | || **Key**         | PerconaPGCluster.spec.backups.pgbackrest.restore.tolerations[index].tolerationSeconds |
| **Value**       | integer |
| **Required**    | false |
| **Example**     | |
| **Description** | TolerationSeconds represents the period of time the toleration (which must be of effect NoExecute, otherwise this field is ignored) tolerates the taint. By default, it is not set, which means tolerate the taint forever (do not evict). Zero and negative values will be treated as 0 (evict immediately) by the system. |
| | || **Key**         | PerconaPGCluster.spec.backups.pgbackrest.restore.tolerations[index].value |
| **Value**       | string |
| **Required**    | false |
| **Example**     | |
| **Description** | Value is the taint value the toleration matches to. If the operator is Exists, the value should be empty, otherwise just a regular string. |
| | |
| **Key**         | PerconaPGCluster.spec.backups.pgbackrest.sidecars.pgbackrest |
| **Value**       | object |
| **Required**    | false |
| **Example**     | |
| **Description** | Defines the configuration for the pgBackRest sidecar container |
| | || **Key**         | PerconaPGCluster.spec.backups.pgbackrest.sidecars.pgbackrestConfig |
| **Value**       | object |
| **Required**    | false |
| **Example**     | |
| **Description** | Defines the configuration for the pgBackRest config sidecar container |
| | |
| **Key**         | PerconaPGCluster.spec.backups.pgbackrest.sidecars.pgbackrest.resources |
| **Value**       | object |
| **Required**    | false |
| **Example**     | |
| **Description** | Resource requirements for a sidecar container |
| | |
| **Key**         | PerconaPGCluster.spec.backups.pgbackrest.sidecars.pgbackrest.resources.limits |
| **Value**       | map[string]int or string |
| **Required**    | false |
| **Example**     | |
| **Description** | Limits describes the maximum amount of compute resources allowed. More info: https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/ |
| | || **Key**         | PerconaPGCluster.spec.backups.pgbackrest.sidecars.pgbackrest.resources.requests |
| **Value**       | map[string]int or string |
| **Required**    | false |
| **Example**     | |
| **Description** | Requests describes the minimum amount of compute resources required. If Requests is omitted for a container, it defaults to Limits if that is explicitly specified, otherwise to an implementation-defined value. More info: https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/ |
| | |
| **Key**         | PerconaPGCluster.spec.backups.pgbackrest.sidecars.pgbackrestConfig.resources |
| **Value**       | object |
| **Required**    | false |
| **Example**     | |
| **Description** | Resource requirements for a sidecar container |
| | |
| **Key**         | PerconaPGCluster.spec.backups.pgbackrest.sidecars.pgbackrestConfig.resources.limits |
| **Value**       | map[string]int or string |
| **Required**    | false |
| **Example**     | |
| **Description** | Limits describes the maximum amount of compute resources allowed. More info: https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/ |
| | || **Key**         | PerconaPGCluster.spec.backups.pgbackrest.sidecars.pgbackrestConfig.resources.requests |
| **Value**       | map[string]int or string |
| **Required**    | false |
| **Example**     | |
| **Description** | Requests describes the minimum amount of compute resources required. If Requests is omitted for a container, it defaults to Limits if that is explicitly specified, otherwise to an implementation-defined value. More info: https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/ |
| | |
| **Key**         | PerconaPGCluster.spec.instances[index].dataVolumeClaimSpec |
| **Value**       | object |
| **Required**    | true |
| **Example**     | |
| **Description** | Defines a PersistentVolumeClaim for PostgreSQL data. More info: https://kubernetes.io/docs/concepts/storage/persistent-volumes |
| | || **Key**         | PerconaPGCluster.spec.instances[index].affinity |
| **Value**       | object |
| **Required**    | false |
| **Example**     | |
| **Description** | Scheduling constraints of a PostgreSQL pod. Changing this value causes PostgreSQL to restart. More info: https://kubernetes.io/docs/concepts/scheduling-eviction/assign-pod-node |
| | || **Key**         | PerconaPGCluster.spec.instances[index].metadata |
| **Value**       | object |
| **Required**    | false |
| **Example**     | |
| **Description** | Metadata contains metadata for PostgresCluster resources |
| | || **Key**         | PerconaPGCluster.spec.instances[index].minAvailable |
| **Value**       | int or string |
| **Required**    | false |
| **Example**     | |
| **Description** | Minimum number of pods that should be available at a time. Defaults to one when the replicas field is greater than one. |
| | || **Key**         | PerconaPGCluster.spec.instances[index].name |
| **Value**       | string |
| **Required**    | false |
| **Example**     | |
| **Description** | Name that associates this set of PostgreSQL pods. This field is optional when only one instance set is defined. Each instance set in a cluster must have a unique name. The combined length of this and the cluster name must be 46 characters or less. |
| | || **Key**         | PerconaPGCluster.spec.instances[index].priorityClassName |
| **Value**       | string |
| **Required**    | false |
| **Example**     | |
| **Description** | Priority class name for the PostgreSQL pod. Changing this value causes PostgreSQL to restart. More info: https://kubernetes.io/docs/concepts/scheduling-eviction/pod-priority-preemption/ |
| | || **Key**         | PerconaPGCluster.spec.instances[index].replicas |
| **Value**       | integer |
| **Required**    | false |
| **Example**     | |
| **Description** | Number of desired PostgreSQL pods. |
| | || **Key**         | PerconaPGCluster.spec.instances[index].resources |
| **Value**       | object |
| **Required**    | false |
| **Example**     | |
| **Description** | Compute resources of a PostgreSQL container. |
| | || **Key**         | PerconaPGCluster.spec.instances[index].sidecars |
| **Value**       | []object |
| **Required**    | false |
| **Example**     | |
| **Description** | Custom sidecars for PostgreSQL instance pods. Changing this value causes PostgreSQL to restart. |
| | || **Key**         | PerconaPGCluster.spec.instances[index].tolerations |
| **Value**       | []object |
| **Required**    | false |
| **Example**     | |
| **Description** | Tolerations of a PostgreSQL pod. Changing this value causes PostgreSQL to restart. More info: https://kubernetes.io/docs/concepts/scheduling-eviction/taint-and-toleration |
| | || **Key**         | PerconaPGCluster.spec.instances[index].topologySpreadConstraints |
| **Value**       | []object |
| **Required**    | false |
| **Example**     | |
| **Description** | Topology spread constraints of a PostgreSQL pod. Changing this value causes PostgreSQL to restart. More info: https://kubernetes.io/docs/concepts/workloads/pods/pod-topology-spread-constraints/ |
| | || **Key**         | PerconaPGCluster.spec.instances[index].walVolumeClaimSpec |
| **Value**       | object |
| **Required**    | false |
| **Example**     | |
| **Description** | Defines a separate PersistentVolumeClaim for PostgreSQL's write-ahead log. More info: https://www.postgresql.org/docs/current/wal.html |
| | |
| **Key**         | PerconaPGCluster.spec.instances[index].dataVolumeClaimSpec.accessModes |
| **Value**       | []string |
| **Required**    | false |
| **Example**     | |
| **Description** | accessModes contains the desired access modes the volume should have. More info: https://kubernetes.io/docs/concepts/storage/persistent-volumes#access-modes-1 |
| | || **Key**         | PerconaPGCluster.spec.instances[index].dataVolumeClaimSpec.dataSource |
| **Value**       | object |
| **Required**    | false |
| **Example**     | |
| **Description** | dataSource field can be used to specify either: * An existing VolumeSnapshot object (snapshot.storage.k8s.io/VolumeSnapshot) * An existing PVC (PersistentVolumeClaim) If the provisioner or an external controller can support the specified data source, it will create a new volume based on the contents of the specified data source. If the AnyVolumeDataSource feature gate is enabled, this field will always have the same contents as the DataSourceRef field. |
| | || **Key**         | PerconaPGCluster.spec.instances[index].dataVolumeClaimSpec.dataSourceRef |
| **Value**       | object |
| **Required**    | false |
| **Example**     | |
| **Description** | dataSourceRef specifies the object from which to populate the volume with data, if a non-empty volume is desired. This may be any local object from a non-empty API group (non core object) or a PersistentVolumeClaim object. When this field is specified, volume binding will only succeed if the type of the specified object matches some installed volume populator or dynamic provisioner. This field will replace the functionality of the DataSource field and as such if both fields are non-empty, they must have the same value. For backwards compatibility, both fields (DataSource and DataSourceRef) will be set to the same value automatically if one of them is empty and the other is non-empty. There are two important differences between DataSource and DataSourceRef: * While DataSource only allows two specific types of objects, DataSourceRef allows any non-core object, as well as PersistentVolumeClaim objects. * While DataSource ignores disallowed values (dropping them), DataSourceRef preserves all values, and generates an error if a disallowed value is specified. (Beta) Using this field requires the AnyVolumeDataSource feature gate to be enabled. |
| | || **Key**         | PerconaPGCluster.spec.instances[index].dataVolumeClaimSpec.resources |
| **Value**       | object |
| **Required**    | false |
| **Example**     | |
| **Description** | resources represents the minimum resources the volume should have. If RecoverVolumeExpansionFailure feature is enabled users are allowed to specify resource requirements that are lower than previous value but must still be higher than capacity recorded in the status field of the claim. More info: https://kubernetes.io/docs/concepts/storage/persistent-volumes#resources |
| | || **Key**         | PerconaPGCluster.spec.instances[index].dataVolumeClaimSpec.selector |
| **Value**       | object |
| **Required**    | false |
| **Example**     | |
| **Description** | selector is a label query over volumes to consider for binding. |
| | || **Key**         | PerconaPGCluster.spec.instances[index].dataVolumeClaimSpec.storageClassName |
| **Value**       | string |
| **Required**    | false |
| **Example**     | |
| **Description** | storageClassName is the name of the StorageClass required by the claim. More info: https://kubernetes.io/docs/concepts/storage/persistent-volumes#class-1 |
| | || **Key**         | PerconaPGCluster.spec.instances[index].dataVolumeClaimSpec.volumeMode |
| **Value**       | string |
| **Required**    | false |
| **Example**     | |
| **Description** | volumeMode defines what type of volume is required by the claim. Value of Filesystem is implied when not included in claim spec. |
| | || **Key**         | PerconaPGCluster.spec.instances[index].dataVolumeClaimSpec.volumeName |
| **Value**       | string |
| **Required**    | false |
| **Example**     | |
| **Description** | volumeName is the binding reference to the PersistentVolume backing this claim. |
| | |
| **Key**         | PerconaPGCluster.spec.instances[index].dataVolumeClaimSpec.dataSource.kind |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | Kind is the type of resource being referenced |
| | || **Key**         | PerconaPGCluster.spec.instances[index].dataVolumeClaimSpec.dataSource.name |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | Name is the name of resource being referenced |
| | || **Key**         | PerconaPGCluster.spec.instances[index].dataVolumeClaimSpec.dataSource.apiGroup |
| **Value**       | string |
| **Required**    | false |
| **Example**     | |
| **Description** | APIGroup is the group for the resource being referenced. If APIGroup is not specified, the specified Kind must be in the core API group. For any other third-party types, APIGroup is required. |
| | |
| **Key**         | PerconaPGCluster.spec.instances[index].dataVolumeClaimSpec.dataSourceRef.kind |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | Kind is the type of resource being referenced |
| | || **Key**         | PerconaPGCluster.spec.instances[index].dataVolumeClaimSpec.dataSourceRef.name |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | Name is the name of resource being referenced |
| | || **Key**         | PerconaPGCluster.spec.instances[index].dataVolumeClaimSpec.dataSourceRef.apiGroup |
| **Value**       | string |
| **Required**    | false |
| **Example**     | |
| **Description** | APIGroup is the group for the resource being referenced. If APIGroup is not specified, the specified Kind must be in the core API group. For any other third-party types, APIGroup is required. |
| | |
| **Key**         | PerconaPGCluster.spec.instances[index].dataVolumeClaimSpec.resources.limits |
| **Value**       | map[string]int or string |
| **Required**    | false |
| **Example**     | |
| **Description** | Limits describes the maximum amount of compute resources allowed. More info: https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/ |
| | || **Key**         | PerconaPGCluster.spec.instances[index].dataVolumeClaimSpec.resources.requests |
| **Value**       | map[string]int or string |
| **Required**    | false |
| **Example**     | |
| **Description** | Requests describes the minimum amount of compute resources required. If Requests is omitted for a container, it defaults to Limits if that is explicitly specified, otherwise to an implementation-defined value. More info: https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/ |
| | |
| **Key**         | PerconaPGCluster.spec.instances[index].dataVolumeClaimSpec.selector.matchExpressions |
| **Value**       | []object |
| **Required**    | false |
| **Example**     | |
| **Description** | matchExpressions is a list of label selector requirements. The requirements are ANDed. |
| | || **Key**         | PerconaPGCluster.spec.instances[index].dataVolumeClaimSpec.selector.matchLabels |
| **Value**       | map[string]string |
| **Required**    | false |
| **Example**     | |
| **Description** | matchLabels is a map of {key,value} pairs. A single {key,value} in the matchLabels map is equivalent to an element of matchExpressions, whose key field is "key", the operator is "In", and the values array contains only "value". The requirements are ANDed. |
| | |
| **Key**         | PerconaPGCluster.spec.instances[index].dataVolumeClaimSpec.selector.matchExpressions[index].key |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | key is the label key that the selector applies to. |
| | || **Key**         | PerconaPGCluster.spec.instances[index].dataVolumeClaimSpec.selector.matchExpressions[index].operator |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | operator represents a key's relationship to a set of values. Valid operators are In, NotIn, Exists and DoesNotExist. |
| | || **Key**         | PerconaPGCluster.spec.instances[index].dataVolumeClaimSpec.selector.matchExpressions[index].values |
| **Value**       | []string |
| **Required**    | false |
| **Example**     | |
| **Description** | values is an array of string values. If the operator is In or NotIn, the values array must be non-empty. If the operator is Exists or DoesNotExist, the values array must be empty. This array is replaced during a strategic merge patch. |
| | |
| **Key**         | PerconaPGCluster.spec.instances[index].affinity.nodeAffinity |
| **Value**       | object |
| **Required**    | false |
| **Example**     | |
| **Description** | Describes node affinity scheduling rules for the pod. |
| | || **Key**         | PerconaPGCluster.spec.instances[index].affinity.podAffinity |
| **Value**       | object |
| **Required**    | false |
| **Example**     | |
| **Description** | Describes pod affinity scheduling rules (e.g. co-locate this pod in the same node, zone, etc. as some other pod(s)). |
| | || **Key**         | PerconaPGCluster.spec.instances[index].affinity.podAntiAffinity |
| **Value**       | object |
| **Required**    | false |
| **Example**     | |
| **Description** | Describes pod anti-affinity scheduling rules (e.g. avoid putting this pod in the same node, zone, etc. as some other pod(s)). |
| | |
| **Key**         | PerconaPGCluster.spec.instances[index].affinity.nodeAffinity.preferredDuringSchedulingIgnoredDuringExecution |
| **Value**       | []object |
| **Required**    | false |
| **Example**     | |
| **Description** | The scheduler will prefer to schedule pods to nodes that satisfy the affinity expressions specified by this field, but it may choose a node that violates one or more of the expressions. The node that is most preferred is the one with the greatest sum of weights, i.e. for each node that meets all of the scheduling requirements (resource request, requiredDuringScheduling affinity expressions, etc.), compute a sum by iterating through the elements of this field and adding "weight" to the sum if the node matches the corresponding matchExpressions; the node(s) with the highest sum are the most preferred. |
| | || **Key**         | PerconaPGCluster.spec.instances[index].affinity.nodeAffinity.requiredDuringSchedulingIgnoredDuringExecution |
| **Value**       | object |
| **Required**    | false |
| **Example**     | |
| **Description** | If the affinity requirements specified by this field are not met at scheduling time, the pod will not be scheduled onto the node. If the affinity requirements specified by this field cease to be met at some point during pod execution (e.g. due to an update), the system may or may not try to eventually evict the pod from its node. |
| | |
| **Key**         | PerconaPGCluster.spec.instances[index].affinity.nodeAffinity.preferredDuringSchedulingIgnoredDuringExecution[index].preference |
| **Value**       | object |
| **Required**    | true |
| **Example**     | |
| **Description** | A node selector term, associated with the corresponding weight. |
| | || **Key**         | PerconaPGCluster.spec.instances[index].affinity.nodeAffinity.preferredDuringSchedulingIgnoredDuringExecution[index].weight |
| **Value**       | integer |
| **Required**    | true |
| **Example**     | |
| **Description** | Weight associated with matching the corresponding nodeSelectorTerm, in the range 1-100. |
| | |
| **Key**         | PerconaPGCluster.spec.instances[index].affinity.nodeAffinity.preferredDuringSchedulingIgnoredDuringExecution[index].preference.matchExpressions |
| **Value**       | []object |
| **Required**    | false |
| **Example**     | |
| **Description** | A list of node selector requirements by node's labels. |
| | || **Key**         | PerconaPGCluster.spec.instances[index].affinity.nodeAffinity.preferredDuringSchedulingIgnoredDuringExecution[index].preference.matchFields |
| **Value**       | []object |
| **Required**    | false |
| **Example**     | |
| **Description** | A list of node selector requirements by node's fields. |
| | |
| **Key**         | PerconaPGCluster.spec.instances[index].affinity.nodeAffinity.preferredDuringSchedulingIgnoredDuringExecution[index].preference.matchExpressions[index].key |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | The label key that the selector applies to. |
| | || **Key**         | PerconaPGCluster.spec.instances[index].affinity.nodeAffinity.preferredDuringSchedulingIgnoredDuringExecution[index].preference.matchExpressions[index].operator |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | Represents a key's relationship to a set of values. Valid operators are In, NotIn, Exists, DoesNotExist. Gt, and Lt. |
| | || **Key**         | PerconaPGCluster.spec.instances[index].affinity.nodeAffinity.preferredDuringSchedulingIgnoredDuringExecution[index].preference.matchExpressions[index].values |
| **Value**       | []string |
| **Required**    | false |
| **Example**     | |
| **Description** | An array of string values. If the operator is In or NotIn, the values array must be non-empty. If the operator is Exists or DoesNotExist, the values array must be empty. If the operator is Gt or Lt, the values array must have a single element, which will be interpreted as an integer. This array is replaced during a strategic merge patch. |
| | |
| **Key**         | PerconaPGCluster.spec.instances[index].affinity.nodeAffinity.preferredDuringSchedulingIgnoredDuringExecution[index].preference.matchFields[index].key |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | The label key that the selector applies to. |
| | || **Key**         | PerconaPGCluster.spec.instances[index].affinity.nodeAffinity.preferredDuringSchedulingIgnoredDuringExecution[index].preference.matchFields[index].operator |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | Represents a key's relationship to a set of values. Valid operators are In, NotIn, Exists, DoesNotExist. Gt, and Lt. |
| | || **Key**         | PerconaPGCluster.spec.instances[index].affinity.nodeAffinity.preferredDuringSchedulingIgnoredDuringExecution[index].preference.matchFields[index].values |
| **Value**       | []string |
| **Required**    | false |
| **Example**     | |
| **Description** | An array of string values. If the operator is In or NotIn, the values array must be non-empty. If the operator is Exists or DoesNotExist, the values array must be empty. If the operator is Gt or Lt, the values array must have a single element, which will be interpreted as an integer. This array is replaced during a strategic merge patch. |
| | |
| **Key**         | PerconaPGCluster.spec.instances[index].affinity.nodeAffinity.requiredDuringSchedulingIgnoredDuringExecution.nodeSelectorTerms |
| **Value**       | []object |
| **Required**    | true |
| **Example**     | |
| **Description** | Required. A list of node selector terms. The terms are ORed. |
| | |
| **Key**         | PerconaPGCluster.spec.instances[index].affinity.nodeAffinity.requiredDuringSchedulingIgnoredDuringExecution.nodeSelectorTerms[index].matchExpressions |
| **Value**       | []object |
| **Required**    | false |
| **Example**     | |
| **Description** | A list of node selector requirements by node's labels. |
| | || **Key**         | PerconaPGCluster.spec.instances[index].affinity.nodeAffinity.requiredDuringSchedulingIgnoredDuringExecution.nodeSelectorTerms[index].matchFields |
| **Value**       | []object |
| **Required**    | false |
| **Example**     | |
| **Description** | A list of node selector requirements by node's fields. |
| | |
| **Key**         | PerconaPGCluster.spec.instances[index].affinity.nodeAffinity.requiredDuringSchedulingIgnoredDuringExecution.nodeSelectorTerms[index].matchExpressions[index].key |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | The label key that the selector applies to. |
| | || **Key**         | PerconaPGCluster.spec.instances[index].affinity.nodeAffinity.requiredDuringSchedulingIgnoredDuringExecution.nodeSelectorTerms[index].matchExpressions[index].operator |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | Represents a key's relationship to a set of values. Valid operators are In, NotIn, Exists, DoesNotExist. Gt, and Lt. |
| | || **Key**         | PerconaPGCluster.spec.instances[index].affinity.nodeAffinity.requiredDuringSchedulingIgnoredDuringExecution.nodeSelectorTerms[index].matchExpressions[index].values |
| **Value**       | []string |
| **Required**    | false |
| **Example**     | |
| **Description** | An array of string values. If the operator is In or NotIn, the values array must be non-empty. If the operator is Exists or DoesNotExist, the values array must be empty. If the operator is Gt or Lt, the values array must have a single element, which will be interpreted as an integer. This array is replaced during a strategic merge patch. |
| | |
| **Key**         | PerconaPGCluster.spec.instances[index].affinity.nodeAffinity.requiredDuringSchedulingIgnoredDuringExecution.nodeSelectorTerms[index].matchFields[index].key |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | The label key that the selector applies to. |
| | || **Key**         | PerconaPGCluster.spec.instances[index].affinity.nodeAffinity.requiredDuringSchedulingIgnoredDuringExecution.nodeSelectorTerms[index].matchFields[index].operator |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | Represents a key's relationship to a set of values. Valid operators are In, NotIn, Exists, DoesNotExist. Gt, and Lt. |
| | || **Key**         | PerconaPGCluster.spec.instances[index].affinity.nodeAffinity.requiredDuringSchedulingIgnoredDuringExecution.nodeSelectorTerms[index].matchFields[index].values |
| **Value**       | []string |
| **Required**    | false |
| **Example**     | |
| **Description** | An array of string values. If the operator is In or NotIn, the values array must be non-empty. If the operator is Exists or DoesNotExist, the values array must be empty. If the operator is Gt or Lt, the values array must have a single element, which will be interpreted as an integer. This array is replaced during a strategic merge patch. |
| | |
| **Key**         | PerconaPGCluster.spec.instances[index].affinity.podAffinity.preferredDuringSchedulingIgnoredDuringExecution |
| **Value**       | []object |
| **Required**    | false |
| **Example**     | |
| **Description** | The scheduler will prefer to schedule pods to nodes that satisfy the affinity expressions specified by this field, but it may choose a node that violates one or more of the expressions. The node that is most preferred is the one with the greatest sum of weights, i.e. for each node that meets all of the scheduling requirements (resource request, requiredDuringScheduling affinity expressions, etc.), compute a sum by iterating through the elements of this field and adding "weight" to the sum if the node has pods which matches the corresponding podAffinityTerm; the node(s) with the highest sum are the most preferred. |
| | || **Key**         | PerconaPGCluster.spec.instances[index].affinity.podAffinity.requiredDuringSchedulingIgnoredDuringExecution |
| **Value**       | []object |
| **Required**    | false |
| **Example**     | |
| **Description** | If the affinity requirements specified by this field are not met at scheduling time, the pod will not be scheduled onto the node. If the affinity requirements specified by this field cease to be met at some point during pod execution (e.g. due to a pod label update), the system may or may not try to eventually evict the pod from its node. When there are multiple elements, the lists of nodes corresponding to each podAffinityTerm are intersected, i.e. all terms must be satisfied. |
| | |
| **Key**         | PerconaPGCluster.spec.instances[index].affinity.podAffinity.preferredDuringSchedulingIgnoredDuringExecution[index].podAffinityTerm |
| **Value**       | object |
| **Required**    | true |
| **Example**     | |
| **Description** | Required. A pod affinity term, associated with the corresponding weight. |
| | || **Key**         | PerconaPGCluster.spec.instances[index].affinity.podAffinity.preferredDuringSchedulingIgnoredDuringExecution[index].weight |
| **Value**       | integer |
| **Required**    | true |
| **Example**     | |
| **Description** | weight associated with matching the corresponding podAffinityTerm, in the range 1-100. |
| | |
| **Key**         | PerconaPGCluster.spec.instances[index].affinity.podAffinity.preferredDuringSchedulingIgnoredDuringExecution[index].podAffinityTerm.topologyKey |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | This pod should be co-located (affinity) or not co-located (anti-affinity) with the pods matching the labelSelector in the specified namespaces, where co-located is defined as running on a node whose value of the label with key topologyKey matches that of any node on which any of the selected pods is running. Empty topologyKey is not allowed. |
| | || **Key**         | PerconaPGCluster.spec.instances[index].affinity.podAffinity.preferredDuringSchedulingIgnoredDuringExecution[index].podAffinityTerm.labelSelector |
| **Value**       | object |
| **Required**    | false |
| **Example**     | |
| **Description** | A label query over a set of resources, in this case pods. |
| | || **Key**         | PerconaPGCluster.spec.instances[index].affinity.podAffinity.preferredDuringSchedulingIgnoredDuringExecution[index].podAffinityTerm.namespaceSelector |
| **Value**       | object |
| **Required**    | false |
| **Example**     | |
| **Description** | A label query over the set of namespaces that the term applies to. The term is applied to the union of the namespaces selected by this field and the ones listed in the namespaces field. null selector and null or empty namespaces list means "this pod's namespace". An empty selector ({}) matches all namespaces. |
| | || **Key**         | PerconaPGCluster.spec.instances[index].affinity.podAffinity.preferredDuringSchedulingIgnoredDuringExecution[index].podAffinityTerm.namespaces |
| **Value**       | []string |
| **Required**    | false |
| **Example**     | |
| **Description** | namespaces specifies a static list of namespace names that the term applies to. The term is applied to the union of the namespaces listed in this field and the ones selected by namespaceSelector. null or empty namespaces list and null namespaceSelector means "this pod's namespace". |
| | |
| **Key**         | PerconaPGCluster.spec.instances[index].affinity.podAffinity.preferredDuringSchedulingIgnoredDuringExecution[index].podAffinityTerm.labelSelector.matchExpressions |
| **Value**       | []object |
| **Required**    | false |
| **Example**     | |
| **Description** | matchExpressions is a list of label selector requirements. The requirements are ANDed. |
| | || **Key**         | PerconaPGCluster.spec.instances[index].affinity.podAffinity.preferredDuringSchedulingIgnoredDuringExecution[index].podAffinityTerm.labelSelector.matchLabels |
| **Value**       | map[string]string |
| **Required**    | false |
| **Example**     | |
| **Description** | matchLabels is a map of {key,value} pairs. A single {key,value} in the matchLabels map is equivalent to an element of matchExpressions, whose key field is "key", the operator is "In", and the values array contains only "value". The requirements are ANDed. |
| | |
| **Key**         | PerconaPGCluster.spec.instances[index].affinity.podAffinity.preferredDuringSchedulingIgnoredDuringExecution[index].podAffinityTerm.labelSelector.matchExpressions[index].key |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | key is the label key that the selector applies to. |
| | || **Key**         | PerconaPGCluster.spec.instances[index].affinity.podAffinity.preferredDuringSchedulingIgnoredDuringExecution[index].podAffinityTerm.labelSelector.matchExpressions[index].operator |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | operator represents a key's relationship to a set of values. Valid operators are In, NotIn, Exists and DoesNotExist. |
| | || **Key**         | PerconaPGCluster.spec.instances[index].affinity.podAffinity.preferredDuringSchedulingIgnoredDuringExecution[index].podAffinityTerm.labelSelector.matchExpressions[index].values |
| **Value**       | []string |
| **Required**    | false |
| **Example**     | |
| **Description** | values is an array of string values. If the operator is In or NotIn, the values array must be non-empty. If the operator is Exists or DoesNotExist, the values array must be empty. This array is replaced during a strategic merge patch. |
| | |
| **Key**         | PerconaPGCluster.spec.instances[index].affinity.podAffinity.preferredDuringSchedulingIgnoredDuringExecution[index].podAffinityTerm.namespaceSelector.matchExpressions |
| **Value**       | []object |
| **Required**    | false |
| **Example**     | |
| **Description** | matchExpressions is a list of label selector requirements. The requirements are ANDed. |
| | || **Key**         | PerconaPGCluster.spec.instances[index].affinity.podAffinity.preferredDuringSchedulingIgnoredDuringExecution[index].podAffinityTerm.namespaceSelector.matchLabels |
| **Value**       | map[string]string |
| **Required**    | false |
| **Example**     | |
| **Description** | matchLabels is a map of {key,value} pairs. A single {key,value} in the matchLabels map is equivalent to an element of matchExpressions, whose key field is "key", the operator is "In", and the values array contains only "value". The requirements are ANDed. |
| | |
| **Key**         | PerconaPGCluster.spec.instances[index].affinity.podAffinity.preferredDuringSchedulingIgnoredDuringExecution[index].podAffinityTerm.namespaceSelector.matchExpressions[index].key |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | key is the label key that the selector applies to. |
| | || **Key**         | PerconaPGCluster.spec.instances[index].affinity.podAffinity.preferredDuringSchedulingIgnoredDuringExecution[index].podAffinityTerm.namespaceSelector.matchExpressions[index].operator |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | operator represents a key's relationship to a set of values. Valid operators are In, NotIn, Exists and DoesNotExist. |
| | || **Key**         | PerconaPGCluster.spec.instances[index].affinity.podAffinity.preferredDuringSchedulingIgnoredDuringExecution[index].podAffinityTerm.namespaceSelector.matchExpressions[index].values |
| **Value**       | []string |
| **Required**    | false |
| **Example**     | |
| **Description** | values is an array of string values. If the operator is In or NotIn, the values array must be non-empty. If the operator is Exists or DoesNotExist, the values array must be empty. This array is replaced during a strategic merge patch. |
| | |
| **Key**         | PerconaPGCluster.spec.instances[index].affinity.podAffinity.requiredDuringSchedulingIgnoredDuringExecution[index].topologyKey |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | This pod should be co-located (affinity) or not co-located (anti-affinity) with the pods matching the labelSelector in the specified namespaces, where co-located is defined as running on a node whose value of the label with key topologyKey matches that of any node on which any of the selected pods is running. Empty topologyKey is not allowed. |
| | || **Key**         | PerconaPGCluster.spec.instances[index].affinity.podAffinity.requiredDuringSchedulingIgnoredDuringExecution[index].labelSelector |
| **Value**       | object |
| **Required**    | false |
| **Example**     | |
| **Description** | A label query over a set of resources, in this case pods. |
| | || **Key**         | PerconaPGCluster.spec.instances[index].affinity.podAffinity.requiredDuringSchedulingIgnoredDuringExecution[index].namespaceSelector |
| **Value**       | object |
| **Required**    | false |
| **Example**     | |
| **Description** | A label query over the set of namespaces that the term applies to. The term is applied to the union of the namespaces selected by this field and the ones listed in the namespaces field. null selector and null or empty namespaces list means "this pod's namespace". An empty selector ({}) matches all namespaces. |
| | || **Key**         | PerconaPGCluster.spec.instances[index].affinity.podAffinity.requiredDuringSchedulingIgnoredDuringExecution[index].namespaces |
| **Value**       | []string |
| **Required**    | false |
| **Example**     | |
| **Description** | namespaces specifies a static list of namespace names that the term applies to. The term is applied to the union of the namespaces listed in this field and the ones selected by namespaceSelector. null or empty namespaces list and null namespaceSelector means "this pod's namespace". |
| | |
| **Key**         | PerconaPGCluster.spec.instances[index].affinity.podAffinity.requiredDuringSchedulingIgnoredDuringExecution[index].labelSelector.matchExpressions |
| **Value**       | []object |
| **Required**    | false |
| **Example**     | |
| **Description** | matchExpressions is a list of label selector requirements. The requirements are ANDed. |
| | || **Key**         | PerconaPGCluster.spec.instances[index].affinity.podAffinity.requiredDuringSchedulingIgnoredDuringExecution[index].labelSelector.matchLabels |
| **Value**       | map[string]string |
| **Required**    | false |
| **Example**     | |
| **Description** | matchLabels is a map of {key,value} pairs. A single {key,value} in the matchLabels map is equivalent to an element of matchExpressions, whose key field is "key", the operator is "In", and the values array contains only "value". The requirements are ANDed. |
| | |
| **Key**         | PerconaPGCluster.spec.instances[index].affinity.podAffinity.requiredDuringSchedulingIgnoredDuringExecution[index].labelSelector.matchExpressions[index].key |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | key is the label key that the selector applies to. |
| | || **Key**         | PerconaPGCluster.spec.instances[index].affinity.podAffinity.requiredDuringSchedulingIgnoredDuringExecution[index].labelSelector.matchExpressions[index].operator |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | operator represents a key's relationship to a set of values. Valid operators are In, NotIn, Exists and DoesNotExist. |
| | || **Key**         | PerconaPGCluster.spec.instances[index].affinity.podAffinity.requiredDuringSchedulingIgnoredDuringExecution[index].labelSelector.matchExpressions[index].values |
| **Value**       | []string |
| **Required**    | false |
| **Example**     | |
| **Description** | values is an array of string values. If the operator is In or NotIn, the values array must be non-empty. If the operator is Exists or DoesNotExist, the values array must be empty. This array is replaced during a strategic merge patch. |
| | |
| **Key**         | PerconaPGCluster.spec.instances[index].affinity.podAffinity.requiredDuringSchedulingIgnoredDuringExecution[index].namespaceSelector.matchExpressions |
| **Value**       | []object |
| **Required**    | false |
| **Example**     | |
| **Description** | matchExpressions is a list of label selector requirements. The requirements are ANDed. |
| | || **Key**         | PerconaPGCluster.spec.instances[index].affinity.podAffinity.requiredDuringSchedulingIgnoredDuringExecution[index].namespaceSelector.matchLabels |
| **Value**       | map[string]string |
| **Required**    | false |
| **Example**     | |
| **Description** | matchLabels is a map of {key,value} pairs. A single {key,value} in the matchLabels map is equivalent to an element of matchExpressions, whose key field is "key", the operator is "In", and the values array contains only "value". The requirements are ANDed. |
| | |
| **Key**         | PerconaPGCluster.spec.instances[index].affinity.podAffinity.requiredDuringSchedulingIgnoredDuringExecution[index].namespaceSelector.matchExpressions[index].key |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | key is the label key that the selector applies to. |
| | || **Key**         | PerconaPGCluster.spec.instances[index].affinity.podAffinity.requiredDuringSchedulingIgnoredDuringExecution[index].namespaceSelector.matchExpressions[index].operator |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | operator represents a key's relationship to a set of values. Valid operators are In, NotIn, Exists and DoesNotExist. |
| | || **Key**         | PerconaPGCluster.spec.instances[index].affinity.podAffinity.requiredDuringSchedulingIgnoredDuringExecution[index].namespaceSelector.matchExpressions[index].values |
| **Value**       | []string |
| **Required**    | false |
| **Example**     | |
| **Description** | values is an array of string values. If the operator is In or NotIn, the values array must be non-empty. If the operator is Exists or DoesNotExist, the values array must be empty. This array is replaced during a strategic merge patch. |
| | |
| **Key**         | PerconaPGCluster.spec.instances[index].affinity.podAntiAffinity.preferredDuringSchedulingIgnoredDuringExecution |
| **Value**       | []object |
| **Required**    | false |
| **Example**     | |
| **Description** | The scheduler will prefer to schedule pods to nodes that satisfy the anti-affinity expressions specified by this field, but it may choose a node that violates one or more of the expressions. The node that is most preferred is the one with the greatest sum of weights, i.e. for each node that meets all of the scheduling requirements (resource request, requiredDuringScheduling anti-affinity expressions, etc.), compute a sum by iterating through the elements of this field and adding "weight" to the sum if the node has pods which matches the corresponding podAffinityTerm; the node(s) with the highest sum are the most preferred. |
| | || **Key**         | PerconaPGCluster.spec.instances[index].affinity.podAntiAffinity.requiredDuringSchedulingIgnoredDuringExecution |
| **Value**       | []object |
| **Required**    | false |
| **Example**     | |
| **Description** | If the anti-affinity requirements specified by this field are not met at scheduling time, the pod will not be scheduled onto the node. If the anti-affinity requirements specified by this field cease to be met at some point during pod execution (e.g. due to a pod label update), the system may or may not try to eventually evict the pod from its node. When there are multiple elements, the lists of nodes corresponding to each podAffinityTerm are intersected, i.e. all terms must be satisfied. |
| | |
| **Key**         | PerconaPGCluster.spec.instances[index].affinity.podAntiAffinity.preferredDuringSchedulingIgnoredDuringExecution[index].podAffinityTerm |
| **Value**       | object |
| **Required**    | true |
| **Example**     | |
| **Description** | Required. A pod affinity term, associated with the corresponding weight. |
| | || **Key**         | PerconaPGCluster.spec.instances[index].affinity.podAntiAffinity.preferredDuringSchedulingIgnoredDuringExecution[index].weight |
| **Value**       | integer |
| **Required**    | true |
| **Example**     | |
| **Description** | weight associated with matching the corresponding podAffinityTerm, in the range 1-100. |
| | |
| **Key**         | PerconaPGCluster.spec.instances[index].affinity.podAntiAffinity.preferredDuringSchedulingIgnoredDuringExecution[index].podAffinityTerm.topologyKey |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | This pod should be co-located (affinity) or not co-located (anti-affinity) with the pods matching the labelSelector in the specified namespaces, where co-located is defined as running on a node whose value of the label with key topologyKey matches that of any node on which any of the selected pods is running. Empty topologyKey is not allowed. |
| | || **Key**         | PerconaPGCluster.spec.instances[index].affinity.podAntiAffinity.preferredDuringSchedulingIgnoredDuringExecution[index].podAffinityTerm.labelSelector |
| **Value**       | object |
| **Required**    | false |
| **Example**     | |
| **Description** | A label query over a set of resources, in this case pods. |
| | || **Key**         | PerconaPGCluster.spec.instances[index].affinity.podAntiAffinity.preferredDuringSchedulingIgnoredDuringExecution[index].podAffinityTerm.namespaceSelector |
| **Value**       | object |
| **Required**    | false |
| **Example**     | |
| **Description** | A label query over the set of namespaces that the term applies to. The term is applied to the union of the namespaces selected by this field and the ones listed in the namespaces field. null selector and null or empty namespaces list means "this pod's namespace". An empty selector ({}) matches all namespaces. |
| | || **Key**         | PerconaPGCluster.spec.instances[index].affinity.podAntiAffinity.preferredDuringSchedulingIgnoredDuringExecution[index].podAffinityTerm.namespaces |
| **Value**       | []string |
| **Required**    | false |
| **Example**     | |
| **Description** | namespaces specifies a static list of namespace names that the term applies to. The term is applied to the union of the namespaces listed in this field and the ones selected by namespaceSelector. null or empty namespaces list and null namespaceSelector means "this pod's namespace". |
| | |
| **Key**         | PerconaPGCluster.spec.instances[index].affinity.podAntiAffinity.preferredDuringSchedulingIgnoredDuringExecution[index].podAffinityTerm.labelSelector.matchExpressions |
| **Value**       | []object |
| **Required**    | false |
| **Example**     | |
| **Description** | matchExpressions is a list of label selector requirements. The requirements are ANDed. |
| | || **Key**         | PerconaPGCluster.spec.instances[index].affinity.podAntiAffinity.preferredDuringSchedulingIgnoredDuringExecution[index].podAffinityTerm.labelSelector.matchLabels |
| **Value**       | map[string]string |
| **Required**    | false |
| **Example**     | |
| **Description** | matchLabels is a map of {key,value} pairs. A single {key,value} in the matchLabels map is equivalent to an element of matchExpressions, whose key field is "key", the operator is "In", and the values array contains only "value". The requirements are ANDed. |
| | |
| **Key**         | PerconaPGCluster.spec.instances[index].affinity.podAntiAffinity.preferredDuringSchedulingIgnoredDuringExecution[index].podAffinityTerm.labelSelector.matchExpressions[index].key |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | key is the label key that the selector applies to. |
| | || **Key**         | PerconaPGCluster.spec.instances[index].affinity.podAntiAffinity.preferredDuringSchedulingIgnoredDuringExecution[index].podAffinityTerm.labelSelector.matchExpressions[index].operator |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | operator represents a key's relationship to a set of values. Valid operators are In, NotIn, Exists and DoesNotExist. |
| | || **Key**         | PerconaPGCluster.spec.instances[index].affinity.podAntiAffinity.preferredDuringSchedulingIgnoredDuringExecution[index].podAffinityTerm.labelSelector.matchExpressions[index].values |
| **Value**       | []string |
| **Required**    | false |
| **Example**     | |
| **Description** | values is an array of string values. If the operator is In or NotIn, the values array must be non-empty. If the operator is Exists or DoesNotExist, the values array must be empty. This array is replaced during a strategic merge patch. |
| | |
| **Key**         | PerconaPGCluster.spec.instances[index].affinity.podAntiAffinity.preferredDuringSchedulingIgnoredDuringExecution[index].podAffinityTerm.namespaceSelector.matchExpressions |
| **Value**       | []object |
| **Required**    | false |
| **Example**     | |
| **Description** | matchExpressions is a list of label selector requirements. The requirements are ANDed. |
| | || **Key**         | PerconaPGCluster.spec.instances[index].affinity.podAntiAffinity.preferredDuringSchedulingIgnoredDuringExecution[index].podAffinityTerm.namespaceSelector.matchLabels |
| **Value**       | map[string]string |
| **Required**    | false |
| **Example**     | |
| **Description** | matchLabels is a map of {key,value} pairs. A single {key,value} in the matchLabels map is equivalent to an element of matchExpressions, whose key field is "key", the operator is "In", and the values array contains only "value". The requirements are ANDed. |
| | |
| **Key**         | PerconaPGCluster.spec.instances[index].affinity.podAntiAffinity.preferredDuringSchedulingIgnoredDuringExecution[index].podAffinityTerm.namespaceSelector.matchExpressions[index].key |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | key is the label key that the selector applies to. |
| | || **Key**         | PerconaPGCluster.spec.instances[index].affinity.podAntiAffinity.preferredDuringSchedulingIgnoredDuringExecution[index].podAffinityTerm.namespaceSelector.matchExpressions[index].operator |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | operator represents a key's relationship to a set of values. Valid operators are In, NotIn, Exists and DoesNotExist. |
| | || **Key**         | PerconaPGCluster.spec.instances[index].affinity.podAntiAffinity.preferredDuringSchedulingIgnoredDuringExecution[index].podAffinityTerm.namespaceSelector.matchExpressions[index].values |
| **Value**       | []string |
| **Required**    | false |
| **Example**     | |
| **Description** | values is an array of string values. If the operator is In or NotIn, the values array must be non-empty. If the operator is Exists or DoesNotExist, the values array must be empty. This array is replaced during a strategic merge patch. |
| | |
| **Key**         | PerconaPGCluster.spec.instances[index].affinity.podAntiAffinity.requiredDuringSchedulingIgnoredDuringExecution[index].topologyKey |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | This pod should be co-located (affinity) or not co-located (anti-affinity) with the pods matching the labelSelector in the specified namespaces, where co-located is defined as running on a node whose value of the label with key topologyKey matches that of any node on which any of the selected pods is running. Empty topologyKey is not allowed. |
| | || **Key**         | PerconaPGCluster.spec.instances[index].affinity.podAntiAffinity.requiredDuringSchedulingIgnoredDuringExecution[index].labelSelector |
| **Value**       | object |
| **Required**    | false |
| **Example**     | |
| **Description** | A label query over a set of resources, in this case pods. |
| | || **Key**         | PerconaPGCluster.spec.instances[index].affinity.podAntiAffinity.requiredDuringSchedulingIgnoredDuringExecution[index].namespaceSelector |
| **Value**       | object |
| **Required**    | false |
| **Example**     | |
| **Description** | A label query over the set of namespaces that the term applies to. The term is applied to the union of the namespaces selected by this field and the ones listed in the namespaces field. null selector and null or empty namespaces list means "this pod's namespace". An empty selector ({}) matches all namespaces. |
| | || **Key**         | PerconaPGCluster.spec.instances[index].affinity.podAntiAffinity.requiredDuringSchedulingIgnoredDuringExecution[index].namespaces |
| **Value**       | []string |
| **Required**    | false |
| **Example**     | |
| **Description** | namespaces specifies a static list of namespace names that the term applies to. The term is applied to the union of the namespaces listed in this field and the ones selected by namespaceSelector. null or empty namespaces list and null namespaceSelector means "this pod's namespace". |
| | |
| **Key**         | PerconaPGCluster.spec.instances[index].affinity.podAntiAffinity.requiredDuringSchedulingIgnoredDuringExecution[index].labelSelector.matchExpressions |
| **Value**       | []object |
| **Required**    | false |
| **Example**     | |
| **Description** | matchExpressions is a list of label selector requirements. The requirements are ANDed. |
| | || **Key**         | PerconaPGCluster.spec.instances[index].affinity.podAntiAffinity.requiredDuringSchedulingIgnoredDuringExecution[index].labelSelector.matchLabels |
| **Value**       | map[string]string |
| **Required**    | false |
| **Example**     | |
| **Description** | matchLabels is a map of {key,value} pairs. A single {key,value} in the matchLabels map is equivalent to an element of matchExpressions, whose key field is "key", the operator is "In", and the values array contains only "value". The requirements are ANDed. |
| | |
| **Key**         | PerconaPGCluster.spec.instances[index].affinity.podAntiAffinity.requiredDuringSchedulingIgnoredDuringExecution[index].labelSelector.matchExpressions[index].key |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | key is the label key that the selector applies to. |
| | || **Key**         | PerconaPGCluster.spec.instances[index].affinity.podAntiAffinity.requiredDuringSchedulingIgnoredDuringExecution[index].labelSelector.matchExpressions[index].operator |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | operator represents a key's relationship to a set of values. Valid operators are In, NotIn, Exists and DoesNotExist. |
| | || **Key**         | PerconaPGCluster.spec.instances[index].affinity.podAntiAffinity.requiredDuringSchedulingIgnoredDuringExecution[index].labelSelector.matchExpressions[index].values |
| **Value**       | []string |
| **Required**    | false |
| **Example**     | |
| **Description** | values is an array of string values. If the operator is In or NotIn, the values array must be non-empty. If the operator is Exists or DoesNotExist, the values array must be empty. This array is replaced during a strategic merge patch. |
| | |
| **Key**         | PerconaPGCluster.spec.instances[index].affinity.podAntiAffinity.requiredDuringSchedulingIgnoredDuringExecution[index].namespaceSelector.matchExpressions |
| **Value**       | []object |
| **Required**    | false |
| **Example**     | |
| **Description** | matchExpressions is a list of label selector requirements. The requirements are ANDed. |
| | || **Key**         | PerconaPGCluster.spec.instances[index].affinity.podAntiAffinity.requiredDuringSchedulingIgnoredDuringExecution[index].namespaceSelector.matchLabels |
| **Value**       | map[string]string |
| **Required**    | false |
| **Example**     | |
| **Description** | matchLabels is a map of {key,value} pairs. A single {key,value} in the matchLabels map is equivalent to an element of matchExpressions, whose key field is "key", the operator is "In", and the values array contains only "value". The requirements are ANDed. |
| | |
| **Key**         | PerconaPGCluster.spec.instances[index].affinity.podAntiAffinity.requiredDuringSchedulingIgnoredDuringExecution[index].namespaceSelector.matchExpressions[index].key |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | key is the label key that the selector applies to. |
| | || **Key**         | PerconaPGCluster.spec.instances[index].affinity.podAntiAffinity.requiredDuringSchedulingIgnoredDuringExecution[index].namespaceSelector.matchExpressions[index].operator |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | operator represents a key's relationship to a set of values. Valid operators are In, NotIn, Exists and DoesNotExist. |
| | || **Key**         | PerconaPGCluster.spec.instances[index].affinity.podAntiAffinity.requiredDuringSchedulingIgnoredDuringExecution[index].namespaceSelector.matchExpressions[index].values |
| **Value**       | []string |
| **Required**    | false |
| **Example**     | |
| **Description** | values is an array of string values. If the operator is In or NotIn, the values array must be non-empty. If the operator is Exists or DoesNotExist, the values array must be empty. This array is replaced during a strategic merge patch. |
| | |
| **Key**         | PerconaPGCluster.spec.instances[index].metadata.annotations |
| **Value**       | map[string]string |
| **Required**    | false |
| **Example**     | |
| **Description** |  |
| | || **Key**         | PerconaPGCluster.spec.instances[index].metadata.labels |
| **Value**       | map[string]string |
| **Required**    | false |
| **Example**     | |
| **Description** |  |
| | |
| **Key**         | PerconaPGCluster.spec.instances[index].resources.limits |
| **Value**       | map[string]int or string |
| **Required**    | false |
| **Example**     | |
| **Description** | Limits describes the maximum amount of compute resources allowed. More info: https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/ |
| | || **Key**         | PerconaPGCluster.spec.instances[index].resources.requests |
| **Value**       | map[string]int or string |
| **Required**    | false |
| **Example**     | |
| **Description** | Requests describes the minimum amount of compute resources required. If Requests is omitted for a container, it defaults to Limits if that is explicitly specified, otherwise to an implementation-defined value. More info: https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/ |
| | |
| **Key**         | PerconaPGCluster.spec.instances[index].sidecars[index].name |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | Name of the container specified as a DNS_LABEL. Each container in a pod must have a unique name (DNS_LABEL). Cannot be updated. |
| | || **Key**         | PerconaPGCluster.spec.instances[index].sidecars[index].args |
| **Value**       | []string |
| **Required**    | false |
| **Example**     | |
| **Description** | Arguments to the entrypoint. The container image's CMD is used if this is not provided. Variable references $(VAR_NAME) are expanded using the container's environment. If a variable cannot be resolved, the reference in the input string will be unchanged. Double $$ are reduced to a single $, which allows for escaping the $(VAR_NAME) syntax: i.e. "$$(VAR_NAME)" will produce the string literal "$(VAR_NAME)". Escaped references will never be expanded, regardless of whether the variable exists or not. Cannot be updated. More info: https://kubernetes.io/docs/tasks/inject-data-application/define-command-argument-container/#running-a-command-in-a-shell |
| | || **Key**         | PerconaPGCluster.spec.instances[index].sidecars[index].command |
| **Value**       | []string |
| **Required**    | false |
| **Example**     | |
| **Description** | Entrypoint array. Not executed within a shell. The container image's ENTRYPOINT is used if this is not provided. Variable references $(VAR_NAME) are expanded using the container's environment. If a variable cannot be resolved, the reference in the input string will be unchanged. Double $$ are reduced to a single $, which allows for escaping the $(VAR_NAME) syntax: i.e. "$$(VAR_NAME)" will produce the string literal "$(VAR_NAME)". Escaped references will never be expanded, regardless of whether the variable exists or not. Cannot be updated. More info: https://kubernetes.io/docs/tasks/inject-data-application/define-command-argument-container/#running-a-command-in-a-shell |
| | || **Key**         | PerconaPGCluster.spec.instances[index].sidecars[index].env |
| **Value**       | []object |
| **Required**    | false |
| **Example**     | |
| **Description** | List of environment variables to set in the container. Cannot be updated. |
| | || **Key**         | PerconaPGCluster.spec.instances[index].sidecars[index].envFrom |
| **Value**       | []object |
| **Required**    | false |
| **Example**     | |
| **Description** | List of sources to populate environment variables in the container. The keys defined within a source must be a C_IDENTIFIER. All invalid keys will be reported as an event when the container is starting. When a key exists in multiple sources, the value associated with the last source will take precedence. Values defined by an Env with a duplicate key will take precedence. Cannot be updated. |
| | || **Key**         | PerconaPGCluster.spec.instances[index].sidecars[index].image |
| **Value**       | string |
| **Required**    | false |
| **Example**     | |
| **Description** | Container image name. More info: https://kubernetes.io/docs/concepts/containers/images This field is optional to allow higher level config management to default or override container images in workload controllers like Deployments and StatefulSets. |
| | || **Key**         | PerconaPGCluster.spec.instances[index].sidecars[index].imagePullPolicy |
| **Value**       | string |
| **Required**    | false |
| **Example**     | |
| **Description** | Image pull policy. One of Always, Never, IfNotPresent. Defaults to Always if :latest tag is specified, or IfNotPresent otherwise. Cannot be updated. More info: https://kubernetes.io/docs/concepts/containers/images#updating-images |
| | || **Key**         | PerconaPGCluster.spec.instances[index].sidecars[index].lifecycle |
| **Value**       | object |
| **Required**    | false |
| **Example**     | |
| **Description** | Actions that the management system should take in response to container lifecycle events. Cannot be updated. |
| | || **Key**         | PerconaPGCluster.spec.instances[index].sidecars[index].livenessProbe |
| **Value**       | object |
| **Required**    | false |
| **Example**     | |
| **Description** | Periodic probe of container liveness. Container will be restarted if the probe fails. Cannot be updated. More info: https://kubernetes.io/docs/concepts/workloads/pods/pod-lifecycle#container-probes |
| | || **Key**         | PerconaPGCluster.spec.instances[index].sidecars[index].ports |
| **Value**       | []object |
| **Required**    | false |
| **Example**     | |
| **Description** | List of ports to expose from the container. Not specifying a port here DOES NOT prevent that port from being exposed. Any port which is listening on the default "0.0.0.0" address inside a container will be accessible from the network. Modifying this array with strategic merge patch may corrupt the data. For more information See https://github.com/kubernetes/kubernetes/issues/108255. Cannot be updated. |
| | || **Key**         | PerconaPGCluster.spec.instances[index].sidecars[index].readinessProbe |
| **Value**       | object |
| **Required**    | false |
| **Example**     | |
| **Description** | Periodic probe of container service readiness. Container will be removed from service endpoints if the probe fails. Cannot be updated. More info: https://kubernetes.io/docs/concepts/workloads/pods/pod-lifecycle#container-probes |
| | || **Key**         | PerconaPGCluster.spec.instances[index].sidecars[index].resources |
| **Value**       | object |
| **Required**    | false |
| **Example**     | |
| **Description** | Compute Resources required by this container. Cannot be updated. More info: https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/ |
| | || **Key**         | PerconaPGCluster.spec.instances[index].sidecars[index].securityContext |
| **Value**       | object |
| **Required**    | false |
| **Example**     | |
| **Description** | SecurityContext defines the security options the container should be run with. If set, the fields of SecurityContext override the equivalent fields of PodSecurityContext. More info: https://kubernetes.io/docs/tasks/configure-pod-container/security-context/ |
| | || **Key**         | PerconaPGCluster.spec.instances[index].sidecars[index].startupProbe |
| **Value**       | object |
| **Required**    | false |
| **Example**     | |
| **Description** | StartupProbe indicates that the Pod has successfully initialized. If specified, no other probes are executed until this completes successfully. If this probe fails, the Pod will be restarted, just as if the livenessProbe failed. This can be used to provide different probe parameters at the beginning of a Pod's lifecycle, when it might take a long time to load data or warm a cache, than during steady-state operation. This cannot be updated. More info: https://kubernetes.io/docs/concepts/workloads/pods/pod-lifecycle#container-probes |
| | || **Key**         | PerconaPGCluster.spec.instances[index].sidecars[index].stdin |
| **Value**       | boolean |
| **Required**    | false |
| **Example**     | |
| **Description** | Whether this container should allocate a buffer for stdin in the container runtime. If this is not set, reads from stdin in the container will always result in EOF. Default is false. |
| | || **Key**         | PerconaPGCluster.spec.instances[index].sidecars[index].stdinOnce |
| **Value**       | boolean |
| **Required**    | false |
| **Example**     | |
| **Description** | Whether the container runtime should close the stdin channel after it has been opened by a single attach. When stdin is true the stdin stream will remain open across multiple attach sessions. If stdinOnce is set to true, stdin is opened on container start, is empty until the first client attaches to stdin, and then remains open and accepts data until the client disconnects, at which time stdin is closed and remains closed until the container is restarted. If this flag is false, a container processes that reads from stdin will never receive an EOF. Default is false |
| | || **Key**         | PerconaPGCluster.spec.instances[index].sidecars[index].terminationMessagePath |
| **Value**       | string |
| **Required**    | false |
| **Example**     | |
| **Description** | Optional: Path at which the file to which the container's termination message will be written is mounted into the container's filesystem. Message written is intended to be brief final status, such as an assertion failure message. Will be truncated by the node if greater than 4096 bytes. The total message length across all containers will be limited to 12kb. Defaults to /dev/termination-log. Cannot be updated. |
| | || **Key**         | PerconaPGCluster.spec.instances[index].sidecars[index].terminationMessagePolicy |
| **Value**       | string |
| **Required**    | false |
| **Example**     | |
| **Description** | Indicate how the termination message should be populated. File will use the contents of terminationMessagePath to populate the container status message on both success and failure. FallbackToLogsOnError will use the last chunk of container log output if the termination message file is empty and the container exited with an error. The log output is limited to 2048 bytes or 80 lines, whichever is smaller. Defaults to File. Cannot be updated. |
| | || **Key**         | PerconaPGCluster.spec.instances[index].sidecars[index].tty |
| **Value**       | boolean |
| **Required**    | false |
| **Example**     | |
| **Description** | Whether this container should allocate a TTY for itself, also requires 'stdin' to be true. Default is false. |
| | || **Key**         | PerconaPGCluster.spec.instances[index].sidecars[index].volumeDevices |
| **Value**       | []object |
| **Required**    | false |
| **Example**     | |
| **Description** | volumeDevices is the list of block devices to be used by the container. |
| | || **Key**         | PerconaPGCluster.spec.instances[index].sidecars[index].volumeMounts |
| **Value**       | []object |
| **Required**    | false |
| **Example**     | |
| **Description** | Pod volumes to mount into the container's filesystem. Cannot be updated. |
| | || **Key**         | PerconaPGCluster.spec.instances[index].sidecars[index].workingDir |
| **Value**       | string |
| **Required**    | false |
| **Example**     | |
| **Description** | Container's working directory. If not specified, the container runtime's default will be used, which might be configured in the container image. Cannot be updated. |
| | |
| **Key**         | PerconaPGCluster.spec.instances[index].sidecars[index].env[index].name |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | Name of the environment variable. Must be a C_IDENTIFIER. |
| | || **Key**         | PerconaPGCluster.spec.instances[index].sidecars[index].env[index].value |
| **Value**       | string |
| **Required**    | false |
| **Example**     | |
| **Description** | Variable references $(VAR_NAME) are expanded using the previously defined environment variables in the container and any service environment variables. If a variable cannot be resolved, the reference in the input string will be unchanged. Double $$ are reduced to a single $, which allows for escaping the $(VAR_NAME) syntax: i.e. "$$(VAR_NAME)" will produce the string literal "$(VAR_NAME)". Escaped references will never be expanded, regardless of whether the variable exists or not. Defaults to "". |
| | || **Key**         | PerconaPGCluster.spec.instances[index].sidecars[index].env[index].valueFrom |
| **Value**       | object |
| **Required**    | false |
| **Example**     | |
| **Description** | Source for the environment variable's value. Cannot be used if value is not empty. |
| | |
| **Key**         | PerconaPGCluster.spec.instances[index].sidecars[index].env[index].valueFrom.configMapKeyRef |
| **Value**       | object |
| **Required**    | false |
| **Example**     | |
| **Description** | Selects a key of a ConfigMap. |
| | || **Key**         | PerconaPGCluster.spec.instances[index].sidecars[index].env[index].valueFrom.fieldRef |
| **Value**       | object |
| **Required**    | false |
| **Example**     | |
| **Description** | Selects a field of the pod: supports metadata.name, metadata.namespace, `metadata.labels['<KEY>']`, `metadata.annotations['<KEY>']`, spec.nodeName, spec.serviceAccountName, status.hostIP, status.podIP, status.podIPs. |
| | || **Key**         | PerconaPGCluster.spec.instances[index].sidecars[index].env[index].valueFrom.resourceFieldRef |
| **Value**       | object |
| **Required**    | false |
| **Example**     | |
| **Description** | Selects a resource of the container: only resources limits and requests (limits.cpu, limits.memory, limits.ephemeral-storage, requests.cpu, requests.memory and requests.ephemeral-storage) are currently supported. |
| | || **Key**         | PerconaPGCluster.spec.instances[index].sidecars[index].env[index].valueFrom.secretKeyRef |
| **Value**       | object |
| **Required**    | false |
| **Example**     | |
| **Description** | Selects a key of a secret in the pod's namespace |
| | |
| **Key**         | PerconaPGCluster.spec.instances[index].sidecars[index].env[index].valueFrom.configMapKeyRef.key |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | The key to select. |
| | || **Key**         | PerconaPGCluster.spec.instances[index].sidecars[index].env[index].valueFrom.configMapKeyRef.name |
| **Value**       | string |
| **Required**    | false |
| **Example**     | |
| **Description** | Name of the referent. More info: https://kubernetes.io/docs/concepts/overview/working-with-objects/names/#names TODO: Add other useful fields. apiVersion, kind, uid? |
| | || **Key**         | PerconaPGCluster.spec.instances[index].sidecars[index].env[index].valueFrom.configMapKeyRef.optional |
| **Value**       | boolean |
| **Required**    | false |
| **Example**     | |
| **Description** | Specify whether the ConfigMap or its key must be defined |
| | |
| **Key**         | PerconaPGCluster.spec.instances[index].sidecars[index].env[index].valueFrom.fieldRef.fieldPath |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | Path of the field to select in the specified API version. |
| | || **Key**         | PerconaPGCluster.spec.instances[index].sidecars[index].env[index].valueFrom.fieldRef.apiVersion |
| **Value**       | string |
| **Required**    | false |
| **Example**     | |
| **Description** | Version of the schema the FieldPath is written in terms of, defaults to "v1". |
| | |
| **Key**         | PerconaPGCluster.spec.instances[index].sidecars[index].env[index].valueFrom.resourceFieldRef.resource |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | Required: resource to select |
| | || **Key**         | PerconaPGCluster.spec.instances[index].sidecars[index].env[index].valueFrom.resourceFieldRef.containerName |
| **Value**       | string |
| **Required**    | false |
| **Example**     | |
| **Description** | Container name: required for volumes, optional for env vars |
| | || **Key**         | PerconaPGCluster.spec.instances[index].sidecars[index].env[index].valueFrom.resourceFieldRef.divisor |
| **Value**       | int or string |
| **Required**    | false |
| **Example**     | |
| **Description** | Specifies the output format of the exposed resources, defaults to "1" |
| | |
| **Key**         | PerconaPGCluster.spec.instances[index].sidecars[index].env[index].valueFrom.secretKeyRef.key |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | The key of the secret to select from.  Must be a valid secret key. |
| | || **Key**         | PerconaPGCluster.spec.instances[index].sidecars[index].env[index].valueFrom.secretKeyRef.name |
| **Value**       | string |
| **Required**    | false |
| **Example**     | |
| **Description** | Name of the referent. More info: https://kubernetes.io/docs/concepts/overview/working-with-objects/names/#names TODO: Add other useful fields. apiVersion, kind, uid? |
| | || **Key**         | PerconaPGCluster.spec.instances[index].sidecars[index].env[index].valueFrom.secretKeyRef.optional |
| **Value**       | boolean |
| **Required**    | false |
| **Example**     | |
| **Description** | Specify whether the Secret or its key must be defined |
| | |
| **Key**         | PerconaPGCluster.spec.instances[index].sidecars[index].envFrom[index].configMapRef |
| **Value**       | object |
| **Required**    | false |
| **Example**     | |
| **Description** | The ConfigMap to select from |
| | || **Key**         | PerconaPGCluster.spec.instances[index].sidecars[index].envFrom[index].prefix |
| **Value**       | string |
| **Required**    | false |
| **Example**     | |
| **Description** | An optional identifier to prepend to each key in the ConfigMap. Must be a C_IDENTIFIER. |
| | || **Key**         | PerconaPGCluster.spec.instances[index].sidecars[index].envFrom[index].secretRef |
| **Value**       | object |
| **Required**    | false |
| **Example**     | |
| **Description** | The Secret to select from |
| | |
| **Key**         | PerconaPGCluster.spec.instances[index].sidecars[index].envFrom[index].configMapRef.name |
| **Value**       | string |
| **Required**    | false |
| **Example**     | |
| **Description** | Name of the referent. More info: https://kubernetes.io/docs/concepts/overview/working-with-objects/names/#names TODO: Add other useful fields. apiVersion, kind, uid? |
| | || **Key**         | PerconaPGCluster.spec.instances[index].sidecars[index].envFrom[index].configMapRef.optional |
| **Value**       | boolean |
| **Required**    | false |
| **Example**     | |
| **Description** | Specify whether the ConfigMap must be defined |
| | |
| **Key**         | PerconaPGCluster.spec.instances[index].sidecars[index].envFrom[index].secretRef.name |
| **Value**       | string |
| **Required**    | false |
| **Example**     | |
| **Description** | Name of the referent. More info: https://kubernetes.io/docs/concepts/overview/working-with-objects/names/#names TODO: Add other useful fields. apiVersion, kind, uid? |
| | || **Key**         | PerconaPGCluster.spec.instances[index].sidecars[index].envFrom[index].secretRef.optional |
| **Value**       | boolean |
| **Required**    | false |
| **Example**     | |
| **Description** | Specify whether the Secret must be defined |
| | |
| **Key**         | PerconaPGCluster.spec.instances[index].sidecars[index].lifecycle.postStart |
| **Value**       | object |
| **Required**    | false |
| **Example**     | |
| **Description** | PostStart is called immediately after a container is created. If the handler fails, the container is terminated and restarted according to its restart policy. Other management of the container blocks until the hook completes. More info: https://kubernetes.io/docs/concepts/containers/container-lifecycle-hooks/#container-hooks |
| | || **Key**         | PerconaPGCluster.spec.instances[index].sidecars[index].lifecycle.preStop |
| **Value**       | object |
| **Required**    | false |
| **Example**     | |
| **Description** | PreStop is called immediately before a container is terminated due to an API request or management event such as liveness/startup probe failure, preemption, resource contention, etc. The handler is not called if the container crashes or exits. The Pod's termination grace period countdown begins before the PreStop hook is executed. Regardless of the outcome of the handler, the container will eventually terminate within the Pod's termination grace period (unless delayed by finalizers). Other management of the container blocks until the hook completes or until the termination grace period is reached. More info: https://kubernetes.io/docs/concepts/containers/container-lifecycle-hooks/#container-hooks |
| | |
| **Key**         | PerconaPGCluster.spec.instances[index].sidecars[index].lifecycle.postStart.exec |
| **Value**       | object |
| **Required**    | false |
| **Example**     | |
| **Description** | Exec specifies the action to take. |
| | || **Key**         | PerconaPGCluster.spec.instances[index].sidecars[index].lifecycle.postStart.httpGet |
| **Value**       | object |
| **Required**    | false |
| **Example**     | |
| **Description** | HTTPGet specifies the http request to perform. |
| | || **Key**         | PerconaPGCluster.spec.instances[index].sidecars[index].lifecycle.postStart.tcpSocket |
| **Value**       | object |
| **Required**    | false |
| **Example**     | |
| **Description** | Deprecated. TCPSocket is NOT supported as a LifecycleHandler and kept for the backward compatibility. There are no validation of this field and lifecycle hooks will fail in runtime when tcp handler is specified. |
| | |
| **Key**         | PerconaPGCluster.spec.instances[index].sidecars[index].lifecycle.postStart.exec.command |
| **Value**       | []string |
| **Required**    | false |
| **Example**     | |
| **Description** | Command is the command line to execute inside the container, the working directory for the command  is root ('/') in the container's filesystem. The command is simply exec'd, it is not run inside a shell, so traditional shell instructions ('|', etc) won't work. To use a shell, you need to explicitly call out to that shell. Exit status of 0 is treated as live/healthy and non-zero is unhealthy. |
| | |
| **Key**         | PerconaPGCluster.spec.instances[index].sidecars[index].lifecycle.postStart.httpGet.port |
| **Value**       | int or string |
| **Required**    | true |
| **Example**     | |
| **Description** | Name or number of the port to access on the container. Number must be in the range 1 to 65535. Name must be an IANA_SVC_NAME. |
| | || **Key**         | PerconaPGCluster.spec.instances[index].sidecars[index].lifecycle.postStart.httpGet.host |
| **Value**       | string |
| **Required**    | false |
| **Example**     | |
| **Description** | Host name to connect to, defaults to the pod IP. You probably want to set "Host" in httpHeaders instead. |
| | || **Key**         | PerconaPGCluster.spec.instances[index].sidecars[index].lifecycle.postStart.httpGet.httpHeaders |
| **Value**       | []object |
| **Required**    | false |
| **Example**     | |
| **Description** | Custom headers to set in the request. HTTP allows repeated headers. |
| | || **Key**         | PerconaPGCluster.spec.instances[index].sidecars[index].lifecycle.postStart.httpGet.path |
| **Value**       | string |
| **Required**    | false |
| **Example**     | |
| **Description** | Path to access on the HTTP server. |
| | || **Key**         | PerconaPGCluster.spec.instances[index].sidecars[index].lifecycle.postStart.httpGet.scheme |
| **Value**       | string |
| **Required**    | false |
| **Example**     | |
| **Description** | Scheme to use for connecting to the host. Defaults to HTTP. |
| | |
| **Key**         | PerconaPGCluster.spec.instances[index].sidecars[index].lifecycle.postStart.httpGet.httpHeaders[index].name |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | The header field name |
| | || **Key**         | PerconaPGCluster.spec.instances[index].sidecars[index].lifecycle.postStart.httpGet.httpHeaders[index].value |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | The header field value |
| | |
| **Key**         | PerconaPGCluster.spec.instances[index].sidecars[index].lifecycle.postStart.tcpSocket.port |
| **Value**       | int or string |
| **Required**    | true |
| **Example**     | |
| **Description** | Number or name of the port to access on the container. Number must be in the range 1 to 65535. Name must be an IANA_SVC_NAME. |
| | || **Key**         | PerconaPGCluster.spec.instances[index].sidecars[index].lifecycle.postStart.tcpSocket.host |
| **Value**       | string |
| **Required**    | false |
| **Example**     | |
| **Description** | Optional: Host name to connect to, defaults to the pod IP. |
| | |
| **Key**         | PerconaPGCluster.spec.instances[index].sidecars[index].lifecycle.preStop.exec |
| **Value**       | object |
| **Required**    | false |
| **Example**     | |
| **Description** | Exec specifies the action to take. |
| | || **Key**         | PerconaPGCluster.spec.instances[index].sidecars[index].lifecycle.preStop.httpGet |
| **Value**       | object |
| **Required**    | false |
| **Example**     | |
| **Description** | HTTPGet specifies the http request to perform. |
| | || **Key**         | PerconaPGCluster.spec.instances[index].sidecars[index].lifecycle.preStop.tcpSocket |
| **Value**       | object |
| **Required**    | false |
| **Example**     | |
| **Description** | Deprecated. TCPSocket is NOT supported as a LifecycleHandler and kept for the backward compatibility. There are no validation of this field and lifecycle hooks will fail in runtime when tcp handler is specified. |
| | |
| **Key**         | PerconaPGCluster.spec.instances[index].sidecars[index].lifecycle.preStop.exec.command |
| **Value**       | []string |
| **Required**    | false |
| **Example**     | |
| **Description** | Command is the command line to execute inside the container, the working directory for the command  is root ('/') in the container's filesystem. The command is simply exec'd, it is not run inside a shell, so traditional shell instructions ('|', etc) won't work. To use a shell, you need to explicitly call out to that shell. Exit status of 0 is treated as live/healthy and non-zero is unhealthy. |
| | |
| **Key**         | PerconaPGCluster.spec.instances[index].sidecars[index].lifecycle.preStop.httpGet.port |
| **Value**       | int or string |
| **Required**    | true |
| **Example**     | |
| **Description** | Name or number of the port to access on the container. Number must be in the range 1 to 65535. Name must be an IANA_SVC_NAME. |
| | || **Key**         | PerconaPGCluster.spec.instances[index].sidecars[index].lifecycle.preStop.httpGet.host |
| **Value**       | string |
| **Required**    | false |
| **Example**     | |
| **Description** | Host name to connect to, defaults to the pod IP. You probably want to set "Host" in httpHeaders instead. |
| | || **Key**         | PerconaPGCluster.spec.instances[index].sidecars[index].lifecycle.preStop.httpGet.httpHeaders |
| **Value**       | []object |
| **Required**    | false |
| **Example**     | |
| **Description** | Custom headers to set in the request. HTTP allows repeated headers. |
| | || **Key**         | PerconaPGCluster.spec.instances[index].sidecars[index].lifecycle.preStop.httpGet.path |
| **Value**       | string |
| **Required**    | false |
| **Example**     | |
| **Description** | Path to access on the HTTP server. |
| | || **Key**         | PerconaPGCluster.spec.instances[index].sidecars[index].lifecycle.preStop.httpGet.scheme |
| **Value**       | string |
| **Required**    | false |
| **Example**     | |
| **Description** | Scheme to use for connecting to the host. Defaults to HTTP. |
| | |
| **Key**         | PerconaPGCluster.spec.instances[index].sidecars[index].lifecycle.preStop.httpGet.httpHeaders[index].name |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | The header field name |
| | || **Key**         | PerconaPGCluster.spec.instances[index].sidecars[index].lifecycle.preStop.httpGet.httpHeaders[index].value |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | The header field value |
| | |
| **Key**         | PerconaPGCluster.spec.instances[index].sidecars[index].lifecycle.preStop.tcpSocket.port |
| **Value**       | int or string |
| **Required**    | true |
| **Example**     | |
| **Description** | Number or name of the port to access on the container. Number must be in the range 1 to 65535. Name must be an IANA_SVC_NAME. |
| | || **Key**         | PerconaPGCluster.spec.instances[index].sidecars[index].lifecycle.preStop.tcpSocket.host |
| **Value**       | string |
| **Required**    | false |
| **Example**     | |
| **Description** | Optional: Host name to connect to, defaults to the pod IP. |
| | |
| **Key**         | PerconaPGCluster.spec.instances[index].sidecars[index].livenessProbe.exec |
| **Value**       | object |
| **Required**    | false |
| **Example**     | |
| **Description** | Exec specifies the action to take. |
| | || **Key**         | PerconaPGCluster.spec.instances[index].sidecars[index].livenessProbe.failureThreshold |
| **Value**       | integer |
| **Required**    | false |
| **Example**     | |
| **Description** | Minimum consecutive failures for the probe to be considered failed after having succeeded. Defaults to 3. Minimum value is 1. |
| | || **Key**         | PerconaPGCluster.spec.instances[index].sidecars[index].livenessProbe.grpc |
| **Value**       | object |
| **Required**    | false |
| **Example**     | |
| **Description** | GRPC specifies an action involving a GRPC port. This is a beta field and requires enabling GRPCContainerProbe feature gate. |
| | || **Key**         | PerconaPGCluster.spec.instances[index].sidecars[index].livenessProbe.httpGet |
| **Value**       | object |
| **Required**    | false |
| **Example**     | |
| **Description** | HTTPGet specifies the http request to perform. |
| | || **Key**         | PerconaPGCluster.spec.instances[index].sidecars[index].livenessProbe.initialDelaySeconds |
| **Value**       | integer |
| **Required**    | false |
| **Example**     | |
| **Description** | Number of seconds after the container has started before liveness probes are initiated. More info: https://kubernetes.io/docs/concepts/workloads/pods/pod-lifecycle#container-probes |
| | || **Key**         | PerconaPGCluster.spec.instances[index].sidecars[index].livenessProbe.periodSeconds |
| **Value**       | integer |
| **Required**    | false |
| **Example**     | |
| **Description** | How often (in seconds) to perform the probe. Default to 10 seconds. Minimum value is 1. |
| | || **Key**         | PerconaPGCluster.spec.instances[index].sidecars[index].livenessProbe.successThreshold |
| **Value**       | integer |
| **Required**    | false |
| **Example**     | |
| **Description** | Minimum consecutive successes for the probe to be considered successful after having failed. Defaults to 1. Must be 1 for liveness and startup. Minimum value is 1. |
| | || **Key**         | PerconaPGCluster.spec.instances[index].sidecars[index].livenessProbe.tcpSocket |
| **Value**       | object |
| **Required**    | false |
| **Example**     | |
| **Description** | TCPSocket specifies an action involving a TCP port. |
| | || **Key**         | PerconaPGCluster.spec.instances[index].sidecars[index].livenessProbe.terminationGracePeriodSeconds |
| **Value**       | integer |
| **Required**    | false |
| **Example**     | |
| **Description** | Optional duration in seconds the pod needs to terminate gracefully upon probe failure. The grace period is the duration in seconds after the processes running in the pod are sent a termination signal and the time when the processes are forcibly halted with a kill signal. Set this value longer than the expected cleanup time for your process. If this value is nil, the pod's terminationGracePeriodSeconds will be used. Otherwise, this value overrides the value provided by the pod spec. Value must be non-negative integer. The value zero indicates stop immediately via the kill signal (no opportunity to shut down). This is a beta field and requires enabling ProbeTerminationGracePeriod feature gate. Minimum value is 1. spec.terminationGracePeriodSeconds is used if unset. |
| | || **Key**         | PerconaPGCluster.spec.instances[index].sidecars[index].livenessProbe.timeoutSeconds |
| **Value**       | integer |
| **Required**    | false |
| **Example**     | |
| **Description** | Number of seconds after which the probe times out. Defaults to 1 second. Minimum value is 1. More info: https://kubernetes.io/docs/concepts/workloads/pods/pod-lifecycle#container-probes |
| | |
| **Key**         | PerconaPGCluster.spec.instances[index].sidecars[index].livenessProbe.exec.command |
| **Value**       | []string |
| **Required**    | false |
| **Example**     | |
| **Description** | Command is the command line to execute inside the container, the working directory for the command  is root ('/') in the container's filesystem. The command is simply exec'd, it is not run inside a shell, so traditional shell instructions ('|', etc) won't work. To use a shell, you need to explicitly call out to that shell. Exit status of 0 is treated as live/healthy and non-zero is unhealthy. |
| | |
| **Key**         | PerconaPGCluster.spec.instances[index].sidecars[index].livenessProbe.grpc.port |
| **Value**       | integer |
| **Required**    | true |
| **Example**     | |
| **Description** | Port number of the gRPC service. Number must be in the range 1 to 65535. |
| | || **Key**         | PerconaPGCluster.spec.instances[index].sidecars[index].livenessProbe.grpc.service |
| **Value**       | string |
| **Required**    | false |
| **Example**     | |
| **Description** | Service is the name of the service to place in the gRPC HealthCheckRequest (see https://github.com/grpc/grpc/blob/master/doc/health-checking.md). 
 If this is not specified, the default behavior is defined by gRPC. |
| | |
| **Key**         | PerconaPGCluster.spec.instances[index].sidecars[index].livenessProbe.httpGet.port |
| **Value**       | int or string |
| **Required**    | true |
| **Example**     | |
| **Description** | Name or number of the port to access on the container. Number must be in the range 1 to 65535. Name must be an IANA_SVC_NAME. |
| | || **Key**         | PerconaPGCluster.spec.instances[index].sidecars[index].livenessProbe.httpGet.host |
| **Value**       | string |
| **Required**    | false |
| **Example**     | |
| **Description** | Host name to connect to, defaults to the pod IP. You probably want to set "Host" in httpHeaders instead. |
| | || **Key**         | PerconaPGCluster.spec.instances[index].sidecars[index].livenessProbe.httpGet.httpHeaders |
| **Value**       | []object |
| **Required**    | false |
| **Example**     | |
| **Description** | Custom headers to set in the request. HTTP allows repeated headers. |
| | || **Key**         | PerconaPGCluster.spec.instances[index].sidecars[index].livenessProbe.httpGet.path |
| **Value**       | string |
| **Required**    | false |
| **Example**     | |
| **Description** | Path to access on the HTTP server. |
| | || **Key**         | PerconaPGCluster.spec.instances[index].sidecars[index].livenessProbe.httpGet.scheme |
| **Value**       | string |
| **Required**    | false |
| **Example**     | |
| **Description** | Scheme to use for connecting to the host. Defaults to HTTP. |
| | |
| **Key**         | PerconaPGCluster.spec.instances[index].sidecars[index].livenessProbe.httpGet.httpHeaders[index].name |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | The header field name |
| | || **Key**         | PerconaPGCluster.spec.instances[index].sidecars[index].livenessProbe.httpGet.httpHeaders[index].value |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | The header field value |
| | |
| **Key**         | PerconaPGCluster.spec.instances[index].sidecars[index].livenessProbe.tcpSocket.port |
| **Value**       | int or string |
| **Required**    | true |
| **Example**     | |
| **Description** | Number or name of the port to access on the container. Number must be in the range 1 to 65535. Name must be an IANA_SVC_NAME. |
| | || **Key**         | PerconaPGCluster.spec.instances[index].sidecars[index].livenessProbe.tcpSocket.host |
| **Value**       | string |
| **Required**    | false |
| **Example**     | |
| **Description** | Optional: Host name to connect to, defaults to the pod IP. |
| | |
| **Key**         | PerconaPGCluster.spec.instances[index].sidecars[index].ports[index].containerPort |
| **Value**       | integer |
| **Required**    | true |
| **Example**     | |
| **Description** | Number of port to expose on the pod's IP address. This must be a valid port number, 0 < x < 65536. |
| | || **Key**         | PerconaPGCluster.spec.instances[index].sidecars[index].ports[index].hostIP |
| **Value**       | string |
| **Required**    | false |
| **Example**     | |
| **Description** | What host IP to bind the external port to. |
| | || **Key**         | PerconaPGCluster.spec.instances[index].sidecars[index].ports[index].hostPort |
| **Value**       | integer |
| **Required**    | false |
| **Example**     | |
| **Description** | Number of port to expose on the host. If specified, this must be a valid port number, 0 < x < 65536. If HostNetwork is specified, this must match ContainerPort. Most containers do not need this. |
| | || **Key**         | PerconaPGCluster.spec.instances[index].sidecars[index].ports[index].name |
| **Value**       | string |
| **Required**    | false |
| **Example**     | |
| **Description** | If specified, this must be an IANA_SVC_NAME and unique within the pod. Each named port in a pod must have a unique name. Name for the port that can be referred to by services. |
| | || **Key**         | PerconaPGCluster.spec.instances[index].sidecars[index].ports[index].protocol |
| **Value**       | string |
| **Required**    | false |
| **Example**     | |
| **Description** | Protocol for port. Must be UDP, TCP, or SCTP. Defaults to "TCP". |
| | |
| **Key**         | PerconaPGCluster.spec.instances[index].sidecars[index].readinessProbe.exec |
| **Value**       | object |
| **Required**    | false |
| **Example**     | |
| **Description** | Exec specifies the action to take. |
| | || **Key**         | PerconaPGCluster.spec.instances[index].sidecars[index].readinessProbe.failureThreshold |
| **Value**       | integer |
| **Required**    | false |
| **Example**     | |
| **Description** | Minimum consecutive failures for the probe to be considered failed after having succeeded. Defaults to 3. Minimum value is 1. |
| | || **Key**         | PerconaPGCluster.spec.instances[index].sidecars[index].readinessProbe.grpc |
| **Value**       | object |
| **Required**    | false |
| **Example**     | |
| **Description** | GRPC specifies an action involving a GRPC port. This is a beta field and requires enabling GRPCContainerProbe feature gate. |
| | || **Key**         | PerconaPGCluster.spec.instances[index].sidecars[index].readinessProbe.httpGet |
| **Value**       | object |
| **Required**    | false |
| **Example**     | |
| **Description** | HTTPGet specifies the http request to perform. |
| | || **Key**         | PerconaPGCluster.spec.instances[index].sidecars[index].readinessProbe.initialDelaySeconds |
| **Value**       | integer |
| **Required**    | false |
| **Example**     | |
| **Description** | Number of seconds after the container has started before liveness probes are initiated. More info: https://kubernetes.io/docs/concepts/workloads/pods/pod-lifecycle#container-probes |
| | || **Key**         | PerconaPGCluster.spec.instances[index].sidecars[index].readinessProbe.periodSeconds |
| **Value**       | integer |
| **Required**    | false |
| **Example**     | |
| **Description** | How often (in seconds) to perform the probe. Default to 10 seconds. Minimum value is 1. |
| | || **Key**         | PerconaPGCluster.spec.instances[index].sidecars[index].readinessProbe.successThreshold |
| **Value**       | integer |
| **Required**    | false |
| **Example**     | |
| **Description** | Minimum consecutive successes for the probe to be considered successful after having failed. Defaults to 1. Must be 1 for liveness and startup. Minimum value is 1. |
| | || **Key**         | PerconaPGCluster.spec.instances[index].sidecars[index].readinessProbe.tcpSocket |
| **Value**       | object |
| **Required**    | false |
| **Example**     | |
| **Description** | TCPSocket specifies an action involving a TCP port. |
| | || **Key**         | PerconaPGCluster.spec.instances[index].sidecars[index].readinessProbe.terminationGracePeriodSeconds |
| **Value**       | integer |
| **Required**    | false |
| **Example**     | |
| **Description** | Optional duration in seconds the pod needs to terminate gracefully upon probe failure. The grace period is the duration in seconds after the processes running in the pod are sent a termination signal and the time when the processes are forcibly halted with a kill signal. Set this value longer than the expected cleanup time for your process. If this value is nil, the pod's terminationGracePeriodSeconds will be used. Otherwise, this value overrides the value provided by the pod spec. Value must be non-negative integer. The value zero indicates stop immediately via the kill signal (no opportunity to shut down). This is a beta field and requires enabling ProbeTerminationGracePeriod feature gate. Minimum value is 1. spec.terminationGracePeriodSeconds is used if unset. |
| | || **Key**         | PerconaPGCluster.spec.instances[index].sidecars[index].readinessProbe.timeoutSeconds |
| **Value**       | integer |
| **Required**    | false |
| **Example**     | |
| **Description** | Number of seconds after which the probe times out. Defaults to 1 second. Minimum value is 1. More info: https://kubernetes.io/docs/concepts/workloads/pods/pod-lifecycle#container-probes |
| | |
| **Key**         | PerconaPGCluster.spec.instances[index].sidecars[index].readinessProbe.exec.command |
| **Value**       | []string |
| **Required**    | false |
| **Example**     | |
| **Description** | Command is the command line to execute inside the container, the working directory for the command  is root ('/') in the container's filesystem. The command is simply exec'd, it is not run inside a shell, so traditional shell instructions ('|', etc) won't work. To use a shell, you need to explicitly call out to that shell. Exit status of 0 is treated as live/healthy and non-zero is unhealthy. |
| | |
| **Key**         | PerconaPGCluster.spec.instances[index].sidecars[index].readinessProbe.grpc.port |
| **Value**       | integer |
| **Required**    | true |
| **Example**     | |
| **Description** | Port number of the gRPC service. Number must be in the range 1 to 65535. |
| | || **Key**         | PerconaPGCluster.spec.instances[index].sidecars[index].readinessProbe.grpc.service |
| **Value**       | string |
| **Required**    | false |
| **Example**     | |
| **Description** | Service is the name of the service to place in the gRPC HealthCheckRequest (see https://github.com/grpc/grpc/blob/master/doc/health-checking.md). 
 If this is not specified, the default behavior is defined by gRPC. |
| | |
| **Key**         | PerconaPGCluster.spec.instances[index].sidecars[index].readinessProbe.httpGet.port |
| **Value**       | int or string |
| **Required**    | true |
| **Example**     | |
| **Description** | Name or number of the port to access on the container. Number must be in the range 1 to 65535. Name must be an IANA_SVC_NAME. |
| | || **Key**         | PerconaPGCluster.spec.instances[index].sidecars[index].readinessProbe.httpGet.host |
| **Value**       | string |
| **Required**    | false |
| **Example**     | |
| **Description** | Host name to connect to, defaults to the pod IP. You probably want to set "Host" in httpHeaders instead. |
| | || **Key**         | PerconaPGCluster.spec.instances[index].sidecars[index].readinessProbe.httpGet.httpHeaders |
| **Value**       | []object |
| **Required**    | false |
| **Example**     | |
| **Description** | Custom headers to set in the request. HTTP allows repeated headers. |
| | || **Key**         | PerconaPGCluster.spec.instances[index].sidecars[index].readinessProbe.httpGet.path |
| **Value**       | string |
| **Required**    | false |
| **Example**     | |
| **Description** | Path to access on the HTTP server. |
| | || **Key**         | PerconaPGCluster.spec.instances[index].sidecars[index].readinessProbe.httpGet.scheme |
| **Value**       | string |
| **Required**    | false |
| **Example**     | |
| **Description** | Scheme to use for connecting to the host. Defaults to HTTP. |
| | |
| **Key**         | PerconaPGCluster.spec.instances[index].sidecars[index].readinessProbe.httpGet.httpHeaders[index].name |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | The header field name |
| | || **Key**         | PerconaPGCluster.spec.instances[index].sidecars[index].readinessProbe.httpGet.httpHeaders[index].value |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | The header field value |
| | |
| **Key**         | PerconaPGCluster.spec.instances[index].sidecars[index].readinessProbe.tcpSocket.port |
| **Value**       | int or string |
| **Required**    | true |
| **Example**     | |
| **Description** | Number or name of the port to access on the container. Number must be in the range 1 to 65535. Name must be an IANA_SVC_NAME. |
| | || **Key**         | PerconaPGCluster.spec.instances[index].sidecars[index].readinessProbe.tcpSocket.host |
| **Value**       | string |
| **Required**    | false |
| **Example**     | |
| **Description** | Optional: Host name to connect to, defaults to the pod IP. |
| | |
| **Key**         | PerconaPGCluster.spec.instances[index].sidecars[index].resources.limits |
| **Value**       | map[string]int or string |
| **Required**    | false |
| **Example**     | |
| **Description** | Limits describes the maximum amount of compute resources allowed. More info: https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/ |
| | || **Key**         | PerconaPGCluster.spec.instances[index].sidecars[index].resources.requests |
| **Value**       | map[string]int or string |
| **Required**    | false |
| **Example**     | |
| **Description** | Requests describes the minimum amount of compute resources required. If Requests is omitted for a container, it defaults to Limits if that is explicitly specified, otherwise to an implementation-defined value. More info: https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/ |
| | |
| **Key**         | PerconaPGCluster.spec.instances[index].sidecars[index].securityContext.allowPrivilegeEscalation |
| **Value**       | boolean |
| **Required**    | false |
| **Example**     | |
| **Description** | AllowPrivilegeEscalation controls whether a process can gain more privileges than its parent process. This bool directly controls if the no_new_privs flag will be set on the container process. AllowPrivilegeEscalation is true always when the container is: 1) run as Privileged 2) has CAP_SYS_ADMIN Note that this field cannot be set when spec.os.name is windows. |
| | || **Key**         | PerconaPGCluster.spec.instances[index].sidecars[index].securityContext.capabilities |
| **Value**       | object |
| **Required**    | false |
| **Example**     | |
| **Description** | The capabilities to add/drop when running containers. Defaults to the default set of capabilities granted by the container runtime. Note that this field cannot be set when spec.os.name is windows. |
| | || **Key**         | PerconaPGCluster.spec.instances[index].sidecars[index].securityContext.privileged |
| **Value**       | boolean |
| **Required**    | false |
| **Example**     | |
| **Description** | Run container in privileged mode. Processes in privileged containers are essentially equivalent to root on the host. Defaults to false. Note that this field cannot be set when spec.os.name is windows. |
| | || **Key**         | PerconaPGCluster.spec.instances[index].sidecars[index].securityContext.procMount |
| **Value**       | string |
| **Required**    | false |
| **Example**     | |
| **Description** | procMount denotes the type of proc mount to use for the containers. The default is DefaultProcMount which uses the container runtime defaults for readonly paths and masked paths. This requires the ProcMountType feature flag to be enabled. Note that this field cannot be set when spec.os.name is windows. |
| | || **Key**         | PerconaPGCluster.spec.instances[index].sidecars[index].securityContext.readOnlyRootFilesystem |
| **Value**       | boolean |
| **Required**    | false |
| **Example**     | |
| **Description** | Whether this container has a read-only root filesystem. Default is false. Note that this field cannot be set when spec.os.name is windows. |
| | || **Key**         | PerconaPGCluster.spec.instances[index].sidecars[index].securityContext.runAsGroup |
| **Value**       | integer |
| **Required**    | false |
| **Example**     | |
| **Description** | The GID to run the entrypoint of the container process. Uses runtime default if unset. May also be set in PodSecurityContext.  If set in both SecurityContext and PodSecurityContext, the value specified in SecurityContext takes precedence. Note that this field cannot be set when spec.os.name is windows. |
| | || **Key**         | PerconaPGCluster.spec.instances[index].sidecars[index].securityContext.runAsNonRoot |
| **Value**       | boolean |
| **Required**    | false |
| **Example**     | |
| **Description** | Indicates that the container must run as a non-root user. If true, the Kubelet will validate the image at runtime to ensure that it does not run as UID 0 (root) and fail to start the container if it does. If unset or false, no such validation will be performed. May also be set in PodSecurityContext.  If set in both SecurityContext and PodSecurityContext, the value specified in SecurityContext takes precedence. |
| | || **Key**         | PerconaPGCluster.spec.instances[index].sidecars[index].securityContext.runAsUser |
| **Value**       | integer |
| **Required**    | false |
| **Example**     | |
| **Description** | The UID to run the entrypoint of the container process. Defaults to user specified in image metadata if unspecified. May also be set in PodSecurityContext.  If set in both SecurityContext and PodSecurityContext, the value specified in SecurityContext takes precedence. Note that this field cannot be set when spec.os.name is windows. |
| | || **Key**         | PerconaPGCluster.spec.instances[index].sidecars[index].securityContext.seLinuxOptions |
| **Value**       | object |
| **Required**    | false |
| **Example**     | |
| **Description** | The SELinux context to be applied to the container. If unspecified, the container runtime will allocate a random SELinux context for each container.  May also be set in PodSecurityContext.  If set in both SecurityContext and PodSecurityContext, the value specified in SecurityContext takes precedence. Note that this field cannot be set when spec.os.name is windows. |
| | || **Key**         | PerconaPGCluster.spec.instances[index].sidecars[index].securityContext.seccompProfile |
| **Value**       | object |
| **Required**    | false |
| **Example**     | |
| **Description** | The seccomp options to use by this container. If seccomp options are provided at both the pod & container level, the container options override the pod options. Note that this field cannot be set when spec.os.name is windows. |
| | || **Key**         | PerconaPGCluster.spec.instances[index].sidecars[index].securityContext.windowsOptions |
| **Value**       | object |
| **Required**    | false |
| **Example**     | |
| **Description** | The Windows specific settings applied to all containers. If unspecified, the options from the PodSecurityContext will be used. If set in both SecurityContext and PodSecurityContext, the value specified in SecurityContext takes precedence. Note that this field cannot be set when spec.os.name is linux. |
| | |
| **Key**         | PerconaPGCluster.spec.instances[index].sidecars[index].securityContext.capabilities.add |
| **Value**       | []string |
| **Required**    | false |
| **Example**     | |
| **Description** | Added capabilities |
| | || **Key**         | PerconaPGCluster.spec.instances[index].sidecars[index].securityContext.capabilities.drop |
| **Value**       | []string |
| **Required**    | false |
| **Example**     | |
| **Description** | Removed capabilities |
| | |
| **Key**         | PerconaPGCluster.spec.instances[index].sidecars[index].securityContext.seLinuxOptions.level |
| **Value**       | string |
| **Required**    | false |
| **Example**     | |
| **Description** | Level is SELinux level label that applies to the container. |
| | || **Key**         | PerconaPGCluster.spec.instances[index].sidecars[index].securityContext.seLinuxOptions.role |
| **Value**       | string |
| **Required**    | false |
| **Example**     | |
| **Description** | Role is a SELinux role label that applies to the container. |
| | || **Key**         | PerconaPGCluster.spec.instances[index].sidecars[index].securityContext.seLinuxOptions.type |
| **Value**       | string |
| **Required**    | false |
| **Example**     | |
| **Description** | Type is a SELinux type label that applies to the container. |
| | || **Key**         | PerconaPGCluster.spec.instances[index].sidecars[index].securityContext.seLinuxOptions.user |
| **Value**       | string |
| **Required**    | false |
| **Example**     | |
| **Description** | User is a SELinux user label that applies to the container. |
| | |
| **Key**         | PerconaPGCluster.spec.instances[index].sidecars[index].securityContext.seccompProfile.type |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | type indicates which kind of seccomp profile will be applied. Valid options are: 
 Localhost - a profile defined in a file on the node should be used. RuntimeDefault - the container runtime default profile should be used. Unconfined - no profile should be applied. |
| | || **Key**         | PerconaPGCluster.spec.instances[index].sidecars[index].securityContext.seccompProfile.localhostProfile |
| **Value**       | string |
| **Required**    | false |
| **Example**     | |
| **Description** | localhostProfile indicates a profile defined in a file on the node should be used. The profile must be preconfigured on the node to work. Must be a descending path, relative to the kubelet's configured seccomp profile location. Must only be set if type is "Localhost". |
| | |
| **Key**         | PerconaPGCluster.spec.instances[index].sidecars[index].securityContext.windowsOptions.gmsaCredentialSpec |
| **Value**       | string |
| **Required**    | false |
| **Example**     | |
| **Description** | GMSACredentialSpec is where the GMSA admission webhook (https://github.com/kubernetes-sigs/windows-gmsa) inlines the contents of the GMSA credential spec named by the GMSACredentialSpecName field. |
| | || **Key**         | PerconaPGCluster.spec.instances[index].sidecars[index].securityContext.windowsOptions.gmsaCredentialSpecName |
| **Value**       | string |
| **Required**    | false |
| **Example**     | |
| **Description** | GMSACredentialSpecName is the name of the GMSA credential spec to use. |
| | || **Key**         | PerconaPGCluster.spec.instances[index].sidecars[index].securityContext.windowsOptions.hostProcess |
| **Value**       | boolean |
| **Required**    | false |
| **Example**     | |
| **Description** | HostProcess determines if a container should be run as a 'Host Process' container. This field is alpha-level and will only be honored by components that enable the WindowsHostProcessContainers feature flag. Setting this field without the feature flag will result in errors when validating the Pod. All of a Pod's containers must have the same effective HostProcess value (it is not allowed to have a mix of HostProcess containers and non-HostProcess containers).  In addition, if HostProcess is true then HostNetwork must also be set to true. |
| | || **Key**         | PerconaPGCluster.spec.instances[index].sidecars[index].securityContext.windowsOptions.runAsUserName |
| **Value**       | string |
| **Required**    | false |
| **Example**     | |
| **Description** | The UserName in Windows to run the entrypoint of the container process. Defaults to the user specified in image metadata if unspecified. May also be set in PodSecurityContext. If set in both SecurityContext and PodSecurityContext, the value specified in SecurityContext takes precedence. |
| | |
| **Key**         | PerconaPGCluster.spec.instances[index].sidecars[index].startupProbe.exec |
| **Value**       | object |
| **Required**    | false |
| **Example**     | |
| **Description** | Exec specifies the action to take. |
| | || **Key**         | PerconaPGCluster.spec.instances[index].sidecars[index].startupProbe.failureThreshold |
| **Value**       | integer |
| **Required**    | false |
| **Example**     | |
| **Description** | Minimum consecutive failures for the probe to be considered failed after having succeeded. Defaults to 3. Minimum value is 1. |
| | || **Key**         | PerconaPGCluster.spec.instances[index].sidecars[index].startupProbe.grpc |
| **Value**       | object |
| **Required**    | false |
| **Example**     | |
| **Description** | GRPC specifies an action involving a GRPC port. This is a beta field and requires enabling GRPCContainerProbe feature gate. |
| | || **Key**         | PerconaPGCluster.spec.instances[index].sidecars[index].startupProbe.httpGet |
| **Value**       | object |
| **Required**    | false |
| **Example**     | |
| **Description** | HTTPGet specifies the http request to perform. |
| | || **Key**         | PerconaPGCluster.spec.instances[index].sidecars[index].startupProbe.initialDelaySeconds |
| **Value**       | integer |
| **Required**    | false |
| **Example**     | |
| **Description** | Number of seconds after the container has started before liveness probes are initiated. More info: https://kubernetes.io/docs/concepts/workloads/pods/pod-lifecycle#container-probes |
| | || **Key**         | PerconaPGCluster.spec.instances[index].sidecars[index].startupProbe.periodSeconds |
| **Value**       | integer |
| **Required**    | false |
| **Example**     | |
| **Description** | How often (in seconds) to perform the probe. Default to 10 seconds. Minimum value is 1. |
| | || **Key**         | PerconaPGCluster.spec.instances[index].sidecars[index].startupProbe.successThreshold |
| **Value**       | integer |
| **Required**    | false |
| **Example**     | |
| **Description** | Minimum consecutive successes for the probe to be considered successful after having failed. Defaults to 1. Must be 1 for liveness and startup. Minimum value is 1. |
| | || **Key**         | PerconaPGCluster.spec.instances[index].sidecars[index].startupProbe.tcpSocket |
| **Value**       | object |
| **Required**    | false |
| **Example**     | |
| **Description** | TCPSocket specifies an action involving a TCP port. |
| | || **Key**         | PerconaPGCluster.spec.instances[index].sidecars[index].startupProbe.terminationGracePeriodSeconds |
| **Value**       | integer |
| **Required**    | false |
| **Example**     | |
| **Description** | Optional duration in seconds the pod needs to terminate gracefully upon probe failure. The grace period is the duration in seconds after the processes running in the pod are sent a termination signal and the time when the processes are forcibly halted with a kill signal. Set this value longer than the expected cleanup time for your process. If this value is nil, the pod's terminationGracePeriodSeconds will be used. Otherwise, this value overrides the value provided by the pod spec. Value must be non-negative integer. The value zero indicates stop immediately via the kill signal (no opportunity to shut down). This is a beta field and requires enabling ProbeTerminationGracePeriod feature gate. Minimum value is 1. spec.terminationGracePeriodSeconds is used if unset. |
| | || **Key**         | PerconaPGCluster.spec.instances[index].sidecars[index].startupProbe.timeoutSeconds |
| **Value**       | integer |
| **Required**    | false |
| **Example**     | |
| **Description** | Number of seconds after which the probe times out. Defaults to 1 second. Minimum value is 1. More info: https://kubernetes.io/docs/concepts/workloads/pods/pod-lifecycle#container-probes |
| | |
| **Key**         | PerconaPGCluster.spec.instances[index].sidecars[index].startupProbe.exec.command |
| **Value**       | []string |
| **Required**    | false |
| **Example**     | |
| **Description** | Command is the command line to execute inside the container, the working directory for the command  is root ('/') in the container's filesystem. The command is simply exec'd, it is not run inside a shell, so traditional shell instructions ('|', etc) won't work. To use a shell, you need to explicitly call out to that shell. Exit status of 0 is treated as live/healthy and non-zero is unhealthy. |
| | |
| **Key**         | PerconaPGCluster.spec.instances[index].sidecars[index].startupProbe.grpc.port |
| **Value**       | integer |
| **Required**    | true |
| **Example**     | |
| **Description** | Port number of the gRPC service. Number must be in the range 1 to 65535. |
| | || **Key**         | PerconaPGCluster.spec.instances[index].sidecars[index].startupProbe.grpc.service |
| **Value**       | string |
| **Required**    | false |
| **Example**     | |
| **Description** | Service is the name of the service to place in the gRPC HealthCheckRequest (see https://github.com/grpc/grpc/blob/master/doc/health-checking.md). 
 If this is not specified, the default behavior is defined by gRPC. |
| | |
| **Key**         | PerconaPGCluster.spec.instances[index].sidecars[index].startupProbe.httpGet.port |
| **Value**       | int or string |
| **Required**    | true |
| **Example**     | |
| **Description** | Name or number of the port to access on the container. Number must be in the range 1 to 65535. Name must be an IANA_SVC_NAME. |
| | || **Key**         | PerconaPGCluster.spec.instances[index].sidecars[index].startupProbe.httpGet.host |
| **Value**       | string |
| **Required**    | false |
| **Example**     | |
| **Description** | Host name to connect to, defaults to the pod IP. You probably want to set "Host" in httpHeaders instead. |
| | || **Key**         | PerconaPGCluster.spec.instances[index].sidecars[index].startupProbe.httpGet.httpHeaders |
| **Value**       | []object |
| **Required**    | false |
| **Example**     | |
| **Description** | Custom headers to set in the request. HTTP allows repeated headers. |
| | || **Key**         | PerconaPGCluster.spec.instances[index].sidecars[index].startupProbe.httpGet.path |
| **Value**       | string |
| **Required**    | false |
| **Example**     | |
| **Description** | Path to access on the HTTP server. |
| | || **Key**         | PerconaPGCluster.spec.instances[index].sidecars[index].startupProbe.httpGet.scheme |
| **Value**       | string |
| **Required**    | false |
| **Example**     | |
| **Description** | Scheme to use for connecting to the host. Defaults to HTTP. |
| | |
| **Key**         | PerconaPGCluster.spec.instances[index].sidecars[index].startupProbe.httpGet.httpHeaders[index].name |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | The header field name |
| | || **Key**         | PerconaPGCluster.spec.instances[index].sidecars[index].startupProbe.httpGet.httpHeaders[index].value |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | The header field value |
| | |
| **Key**         | PerconaPGCluster.spec.instances[index].sidecars[index].startupProbe.tcpSocket.port |
| **Value**       | int or string |
| **Required**    | true |
| **Example**     | |
| **Description** | Number or name of the port to access on the container. Number must be in the range 1 to 65535. Name must be an IANA_SVC_NAME. |
| | || **Key**         | PerconaPGCluster.spec.instances[index].sidecars[index].startupProbe.tcpSocket.host |
| **Value**       | string |
| **Required**    | false |
| **Example**     | |
| **Description** | Optional: Host name to connect to, defaults to the pod IP. |
| | |
| **Key**         | PerconaPGCluster.spec.instances[index].sidecars[index].volumeDevices[index].devicePath |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | devicePath is the path inside of the container that the device will be mapped to. |
| | || **Key**         | PerconaPGCluster.spec.instances[index].sidecars[index].volumeDevices[index].name |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | name must match the name of a persistentVolumeClaim in the pod |
| | |
| **Key**         | PerconaPGCluster.spec.instances[index].sidecars[index].volumeMounts[index].mountPath |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | Path within the container at which the volume should be mounted.  Must not contain ':'. |
| | || **Key**         | PerconaPGCluster.spec.instances[index].sidecars[index].volumeMounts[index].name |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | This must match the Name of a Volume. |
| | || **Key**         | PerconaPGCluster.spec.instances[index].sidecars[index].volumeMounts[index].mountPropagation |
| **Value**       | string |
| **Required**    | false |
| **Example**     | |
| **Description** | mountPropagation determines how mounts are propagated from the host to container and the other way around. When not set, MountPropagationNone is used. This field is beta in 1.10. |
| | || **Key**         | PerconaPGCluster.spec.instances[index].sidecars[index].volumeMounts[index].readOnly |
| **Value**       | boolean |
| **Required**    | false |
| **Example**     | |
| **Description** | Mounted read-only if true, read-write otherwise (false or unspecified). Defaults to false. |
| | || **Key**         | PerconaPGCluster.spec.instances[index].sidecars[index].volumeMounts[index].subPath |
| **Value**       | string |
| **Required**    | false |
| **Example**     | |
| **Description** | Path within the volume from which the container's volume should be mounted. Defaults to "" (volume's root). |
| | || **Key**         | PerconaPGCluster.spec.instances[index].sidecars[index].volumeMounts[index].subPathExpr |
| **Value**       | string |
| **Required**    | false |
| **Example**     | |
| **Description** | Expanded path within the volume from which the container's volume should be mounted. Behaves similarly to SubPath but environment variable references $(VAR_NAME) are expanded using the container's environment. Defaults to "" (volume's root). SubPathExpr and SubPath are mutually exclusive. |
| | |
| **Key**         | PerconaPGCluster.spec.instances[index].tolerations[index].effect |
| **Value**       | string |
| **Required**    | false |
| **Example**     | |
| **Description** | Effect indicates the taint effect to match. Empty means match all taint effects. When specified, allowed values are NoSchedule, PreferNoSchedule and NoExecute. |
| | || **Key**         | PerconaPGCluster.spec.instances[index].tolerations[index].key |
| **Value**       | string |
| **Required**    | false |
| **Example**     | |
| **Description** | Key is the taint key that the toleration applies to. Empty means match all taint keys. If the key is empty, operator must be Exists; this combination means to match all values and all keys. |
| | || **Key**         | PerconaPGCluster.spec.instances[index].tolerations[index].operator |
| **Value**       | string |
| **Required**    | false |
| **Example**     | |
| **Description** | Operator represents a key's relationship to the value. Valid operators are Exists and Equal. Defaults to Equal. Exists is equivalent to wildcard for value, so that a pod can tolerate all taints of a particular category. |
| | || **Key**         | PerconaPGCluster.spec.instances[index].tolerations[index].tolerationSeconds |
| **Value**       | integer |
| **Required**    | false |
| **Example**     | |
| **Description** | TolerationSeconds represents the period of time the toleration (which must be of effect NoExecute, otherwise this field is ignored) tolerates the taint. By default, it is not set, which means tolerate the taint forever (do not evict). Zero and negative values will be treated as 0 (evict immediately) by the system. |
| | || **Key**         | PerconaPGCluster.spec.instances[index].tolerations[index].value |
| **Value**       | string |
| **Required**    | false |
| **Example**     | |
| **Description** | Value is the taint value the toleration matches to. If the operator is Exists, the value should be empty, otherwise just a regular string. |
| | |
| **Key**         | PerconaPGCluster.spec.instances[index].topologySpreadConstraints[index].maxSkew |
| **Value**       | integer |
| **Required**    | true |
| **Example**     | |
| **Description** | MaxSkew describes the degree to which pods may be unevenly distributed. When `whenUnsatisfiable=DoNotSchedule`, it is the maximum permitted difference between the number of matching pods in the target topology and the global minimum. The global minimum is the minimum number of matching pods in an eligible domain or zero if the number of eligible domains is less than MinDomains. For example, in a 3-zone cluster, MaxSkew is set to 1, and pods with the same labelSelector spread as 2/2/1: In this case, the global minimum is 1. | zone1 | zone2 | zone3 | |  P P  |  P P  |   P   | - if MaxSkew is 1, incoming pod can only be scheduled to zone3 to become 2/2/2; scheduling it onto zone1(zone2) would make the ActualSkew(3-1) on zone1(zone2) violate MaxSkew(1). - if MaxSkew is 2, incoming pod can be scheduled onto any zone. When `whenUnsatisfiable=ScheduleAnyway`, it is used to give higher precedence to topologies that satisfy it. It's a required field. Default value is 1 and 0 is not allowed. |
| | || **Key**         | PerconaPGCluster.spec.instances[index].topologySpreadConstraints[index].topologyKey |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | TopologyKey is the key of node labels. Nodes that have a label with this key and identical values are considered to be in the same topology. We consider each <key, value> as a "bucket", and try to put balanced number of pods into each bucket. We define a domain as a particular instance of a topology. Also, we define an eligible domain as a domain whose nodes meet the requirements of nodeAffinityPolicy and nodeTaintsPolicy. e.g. If TopologyKey is "kubernetes.io/hostname", each Node is a domain of that topology. And, if TopologyKey is "topology.kubernetes.io/zone", each zone is a domain of that topology. It's a required field. |
| | || **Key**         | PerconaPGCluster.spec.instances[index].topologySpreadConstraints[index].whenUnsatisfiable |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | WhenUnsatisfiable indicates how to deal with a pod if it doesn't satisfy the spread constraint. - DoNotSchedule (default) tells the scheduler not to schedule it. - ScheduleAnyway tells the scheduler to schedule the pod in any location, but giving higher precedence to topologies that would help reduce the skew. A constraint is considered "Unsatisfiable" for an incoming pod if and only if every possible node assignment for that pod would violate "MaxSkew" on some topology. For example, in a 3-zone cluster, MaxSkew is set to 1, and pods with the same labelSelector spread as 3/1/1: | zone1 | zone2 | zone3 | | P P P |   P   |   P   | If WhenUnsatisfiable is set to DoNotSchedule, incoming pod can only be scheduled to zone2(zone3) to become 3/2/1(3/1/2) as ActualSkew(2-1) on zone2(zone3) satisfies MaxSkew(1). In other words, the cluster can still be imbalanced, but scheduler won't make it *more* imbalanced. It's a required field. |
| | || **Key**         | PerconaPGCluster.spec.instances[index].topologySpreadConstraints[index].labelSelector |
| **Value**       | object |
| **Required**    | false |
| **Example**     | |
| **Description** | LabelSelector is used to find matching pods. Pods that match this label selector are counted to determine the number of pods in their corresponding topology domain. |
| | || **Key**         | PerconaPGCluster.spec.instances[index].topologySpreadConstraints[index].matchLabelKeys |
| **Value**       | []string |
| **Required**    | false |
| **Example**     | |
| **Description** | MatchLabelKeys is a set of pod label keys to select the pods over which spreading will be calculated. The keys are used to lookup values from the incoming pod labels, those key-value labels are ANDed with labelSelector to select the group of existing pods over which spreading will be calculated for the incoming pod. Keys that don't exist in the incoming pod labels will be ignored. A null or empty list means only match against labelSelector. |
| | || **Key**         | PerconaPGCluster.spec.instances[index].topologySpreadConstraints[index].minDomains |
| **Value**       | integer |
| **Required**    | false |
| **Example**     | |
| **Description** | MinDomains indicates a minimum number of eligible domains. When the number of eligible domains with matching topology keys is less than minDomains, Pod Topology Spread treats "global minimum" as 0, and then the calculation of Skew is performed. And when the number of eligible domains with matching topology keys equals or greater than minDomains, this value has no effect on scheduling. As a result, when the number of eligible domains is less than minDomains, scheduler won't schedule more than maxSkew Pods to those domains. If value is nil, the constraint behaves as if MinDomains is equal to 1. Valid values are integers greater than 0. When value is not nil, WhenUnsatisfiable must be DoNotSchedule. 
 For example, in a 3-zone cluster, MaxSkew is set to 2, MinDomains is set to 5 and pods with the same labelSelector spread as 2/2/2: | zone1 | zone2 | zone3 | |  P P  |  P P  |  P P  | The number of domains is less than 5(MinDomains), so "global minimum" is treated as 0. In this situation, new pod with the same labelSelector cannot be scheduled, because computed skew will be 3(3 - 0) if new Pod is scheduled to any of the three zones, it will violate MaxSkew. 
 This is a beta field and requires the MinDomainsInPodTopologySpread feature gate to be enabled (enabled by default). |
| | || **Key**         | PerconaPGCluster.spec.instances[index].topologySpreadConstraints[index].nodeAffinityPolicy |
| **Value**       | string |
| **Required**    | false |
| **Example**     | |
| **Description** | NodeAffinityPolicy indicates how we will treat Pod's nodeAffinity/nodeSelector when calculating pod topology spread skew. Options are: - Honor: only nodes matching nodeAffinity/nodeSelector are included in the calculations. - Ignore: nodeAffinity/nodeSelector are ignored. All nodes are included in the calculations. 
 If this value is nil, the behavior is equivalent to the Honor policy. This is a alpha-level feature enabled by the NodeInclusionPolicyInPodTopologySpread feature flag. |
| | || **Key**         | PerconaPGCluster.spec.instances[index].topologySpreadConstraints[index].nodeTaintsPolicy |
| **Value**       | string |
| **Required**    | false |
| **Example**     | |
| **Description** | NodeTaintsPolicy indicates how we will treat node taints when calculating pod topology spread skew. Options are: - Honor: nodes without taints, along with tainted nodes for which the incoming pod has a toleration, are included. - Ignore: node taints are ignored. All nodes are included. 
 If this value is nil, the behavior is equivalent to the Ignore policy. This is a alpha-level feature enabled by the NodeInclusionPolicyInPodTopologySpread feature flag. |
| | |
| **Key**         | PerconaPGCluster.spec.instances[index].topologySpreadConstraints[index].labelSelector.matchExpressions |
| **Value**       | []object |
| **Required**    | false |
| **Example**     | |
| **Description** | matchExpressions is a list of label selector requirements. The requirements are ANDed. |
| | || **Key**         | PerconaPGCluster.spec.instances[index].topologySpreadConstraints[index].labelSelector.matchLabels |
| **Value**       | map[string]string |
| **Required**    | false |
| **Example**     | |
| **Description** | matchLabels is a map of {key,value} pairs. A single {key,value} in the matchLabels map is equivalent to an element of matchExpressions, whose key field is "key", the operator is "In", and the values array contains only "value". The requirements are ANDed. |
| | |
| **Key**         | PerconaPGCluster.spec.instances[index].topologySpreadConstraints[index].labelSelector.matchExpressions[index].key |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | key is the label key that the selector applies to. |
| | || **Key**         | PerconaPGCluster.spec.instances[index].topologySpreadConstraints[index].labelSelector.matchExpressions[index].operator |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | operator represents a key's relationship to a set of values. Valid operators are In, NotIn, Exists and DoesNotExist. |
| | || **Key**         | PerconaPGCluster.spec.instances[index].topologySpreadConstraints[index].labelSelector.matchExpressions[index].values |
| **Value**       | []string |
| **Required**    | false |
| **Example**     | |
| **Description** | values is an array of string values. If the operator is In or NotIn, the values array must be non-empty. If the operator is Exists or DoesNotExist, the values array must be empty. This array is replaced during a strategic merge patch. |
| | |
| **Key**         | PerconaPGCluster.spec.instances[index].walVolumeClaimSpec.accessModes |
| **Value**       | []string |
| **Required**    | false |
| **Example**     | |
| **Description** | accessModes contains the desired access modes the volume should have. More info: https://kubernetes.io/docs/concepts/storage/persistent-volumes#access-modes-1 |
| | || **Key**         | PerconaPGCluster.spec.instances[index].walVolumeClaimSpec.dataSource |
| **Value**       | object |
| **Required**    | false |
| **Example**     | |
| **Description** | dataSource field can be used to specify either: * An existing VolumeSnapshot object (snapshot.storage.k8s.io/VolumeSnapshot) * An existing PVC (PersistentVolumeClaim) If the provisioner or an external controller can support the specified data source, it will create a new volume based on the contents of the specified data source. If the AnyVolumeDataSource feature gate is enabled, this field will always have the same contents as the DataSourceRef field. |
| | || **Key**         | PerconaPGCluster.spec.instances[index].walVolumeClaimSpec.dataSourceRef |
| **Value**       | object |
| **Required**    | false |
| **Example**     | |
| **Description** | dataSourceRef specifies the object from which to populate the volume with data, if a non-empty volume is desired. This may be any local object from a non-empty API group (non core object) or a PersistentVolumeClaim object. When this field is specified, volume binding will only succeed if the type of the specified object matches some installed volume populator or dynamic provisioner. This field will replace the functionality of the DataSource field and as such if both fields are non-empty, they must have the same value. For backwards compatibility, both fields (DataSource and DataSourceRef) will be set to the same value automatically if one of them is empty and the other is non-empty. There are two important differences between DataSource and DataSourceRef: * While DataSource only allows two specific types of objects, DataSourceRef allows any non-core object, as well as PersistentVolumeClaim objects. * While DataSource ignores disallowed values (dropping them), DataSourceRef preserves all values, and generates an error if a disallowed value is specified. (Beta) Using this field requires the AnyVolumeDataSource feature gate to be enabled. |
| | || **Key**         | PerconaPGCluster.spec.instances[index].walVolumeClaimSpec.resources |
| **Value**       | object |
| **Required**    | false |
| **Example**     | |
| **Description** | resources represents the minimum resources the volume should have. If RecoverVolumeExpansionFailure feature is enabled users are allowed to specify resource requirements that are lower than previous value but must still be higher than capacity recorded in the status field of the claim. More info: https://kubernetes.io/docs/concepts/storage/persistent-volumes#resources |
| | || **Key**         | PerconaPGCluster.spec.instances[index].walVolumeClaimSpec.selector |
| **Value**       | object |
| **Required**    | false |
| **Example**     | |
| **Description** | selector is a label query over volumes to consider for binding. |
| | || **Key**         | PerconaPGCluster.spec.instances[index].walVolumeClaimSpec.storageClassName |
| **Value**       | string |
| **Required**    | false |
| **Example**     | |
| **Description** | storageClassName is the name of the StorageClass required by the claim. More info: https://kubernetes.io/docs/concepts/storage/persistent-volumes#class-1 |
| | || **Key**         | PerconaPGCluster.spec.instances[index].walVolumeClaimSpec.volumeMode |
| **Value**       | string |
| **Required**    | false |
| **Example**     | |
| **Description** | volumeMode defines what type of volume is required by the claim. Value of Filesystem is implied when not included in claim spec. |
| | || **Key**         | PerconaPGCluster.spec.instances[index].walVolumeClaimSpec.volumeName |
| **Value**       | string |
| **Required**    | false |
| **Example**     | |
| **Description** | volumeName is the binding reference to the PersistentVolume backing this claim. |
| | |
| **Key**         | PerconaPGCluster.spec.instances[index].walVolumeClaimSpec.dataSource.kind |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | Kind is the type of resource being referenced |
| | || **Key**         | PerconaPGCluster.spec.instances[index].walVolumeClaimSpec.dataSource.name |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | Name is the name of resource being referenced |
| | || **Key**         | PerconaPGCluster.spec.instances[index].walVolumeClaimSpec.dataSource.apiGroup |
| **Value**       | string |
| **Required**    | false |
| **Example**     | |
| **Description** | APIGroup is the group for the resource being referenced. If APIGroup is not specified, the specified Kind must be in the core API group. For any other third-party types, APIGroup is required. |
| | |
| **Key**         | PerconaPGCluster.spec.instances[index].walVolumeClaimSpec.dataSourceRef.kind |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | Kind is the type of resource being referenced |
| | || **Key**         | PerconaPGCluster.spec.instances[index].walVolumeClaimSpec.dataSourceRef.name |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | Name is the name of resource being referenced |
| | || **Key**         | PerconaPGCluster.spec.instances[index].walVolumeClaimSpec.dataSourceRef.apiGroup |
| **Value**       | string |
| **Required**    | false |
| **Example**     | |
| **Description** | APIGroup is the group for the resource being referenced. If APIGroup is not specified, the specified Kind must be in the core API group. For any other third-party types, APIGroup is required. |
| | |
| **Key**         | PerconaPGCluster.spec.instances[index].walVolumeClaimSpec.resources.limits |
| **Value**       | map[string]int or string |
| **Required**    | false |
| **Example**     | |
| **Description** | Limits describes the maximum amount of compute resources allowed. More info: https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/ |
| | || **Key**         | PerconaPGCluster.spec.instances[index].walVolumeClaimSpec.resources.requests |
| **Value**       | map[string]int or string |
| **Required**    | false |
| **Example**     | |
| **Description** | Requests describes the minimum amount of compute resources required. If Requests is omitted for a container, it defaults to Limits if that is explicitly specified, otherwise to an implementation-defined value. More info: https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/ |
| | |
| **Key**         | PerconaPGCluster.spec.instances[index].walVolumeClaimSpec.selector.matchExpressions |
| **Value**       | []object |
| **Required**    | false |
| **Example**     | |
| **Description** | matchExpressions is a list of label selector requirements. The requirements are ANDed. |
| | || **Key**         | PerconaPGCluster.spec.instances[index].walVolumeClaimSpec.selector.matchLabels |
| **Value**       | map[string]string |
| **Required**    | false |
| **Example**     | |
| **Description** | matchLabels is a map of {key,value} pairs. A single {key,value} in the matchLabels map is equivalent to an element of matchExpressions, whose key field is "key", the operator is "In", and the values array contains only "value". The requirements are ANDed. |
| | |
| **Key**         | PerconaPGCluster.spec.instances[index].walVolumeClaimSpec.selector.matchExpressions[index].key |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | key is the label key that the selector applies to. |
| | || **Key**         | PerconaPGCluster.spec.instances[index].walVolumeClaimSpec.selector.matchExpressions[index].operator |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | operator represents a key's relationship to a set of values. Valid operators are In, NotIn, Exists and DoesNotExist. |
| | || **Key**         | PerconaPGCluster.spec.instances[index].walVolumeClaimSpec.selector.matchExpressions[index].values |
| **Value**       | []string |
| **Required**    | false |
| **Example**     | |
| **Description** | values is an array of string values. If the operator is In or NotIn, the values array must be non-empty. If the operator is Exists or DoesNotExist, the values array must be empty. This array is replaced during a strategic merge patch. |
| | |
| **Key**         | PerconaPGCluster.spec.dataSource.pgbackrest |
| **Value**       | object |
| **Required**    | false |
| **Example**     | |
| **Description** | Defines a pgBackRest cloud-based data source that can be used to pre-populate the the PostgreSQL data directory for a new PostgreSQL cluster using a pgBackRest restore. The PGBackRest field is incompatible with the PostgresCluster field: only one data source can be used for pre-populating a new PostgreSQL cluster |
| | || **Key**         | PerconaPGCluster.spec.dataSource.postgresCluster |
| **Value**       | object |
| **Required**    | false |
| **Example**     | |
| **Description** | Defines a pgBackRest data source that can be used to pre-populate the PostgreSQL data directory for a new PostgreSQL cluster using a pgBackRest restore. The PGBackRest field is incompatible with the PostgresCluster field: only one data source can be used for pre-populating a new PostgreSQL cluster |
| | || **Key**         | PerconaPGCluster.spec.dataSource.volumes |
| **Value**       | object |
| **Required**    | false |
| **Example**     | |
| **Description** | Defines any existing volumes to reuse for this PostgresCluster. |
| | |
| **Key**         | PerconaPGCluster.spec.dataSource.pgbackrest.repo |
| **Value**       | object |
| **Required**    | true |
| **Example**     | |
| **Description** | Defines a pgBackRest repository |
| | || **Key**         | PerconaPGCluster.spec.dataSource.pgbackrest.stanza |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | The name of an existing pgBackRest stanza to use as the data source for the new PostgresCluster. Defaults to `db` if not provided. |
| | || **Key**         | PerconaPGCluster.spec.dataSource.pgbackrest.affinity |
| **Value**       | object |
| **Required**    | false |
| **Example**     | |
| **Description** | Scheduling constraints of the pgBackRest restore Job. More info: https://kubernetes.io/docs/concepts/scheduling-eviction/assign-pod-node |
| | || **Key**         | PerconaPGCluster.spec.dataSource.pgbackrest.configuration |
| **Value**       | []object |
| **Required**    | false |
| **Example**     | |
| **Description** | Projected volumes containing custom pgBackRest configuration.  These files are mounted under "/etc/pgbackrest/conf.d" alongside any pgBackRest configuration generated by the PostgreSQL Operator: https://pgbackrest.org/configuration.html |
| | || **Key**         | PerconaPGCluster.spec.dataSource.pgbackrest.global |
| **Value**       | map[string]string |
| **Required**    | false |
| **Example**     | |
| **Description** | Global pgBackRest configuration settings.  These settings are included in the "global" section of the pgBackRest configuration generated by the PostgreSQL Operator, and then mounted under "/etc/pgbackrest/conf.d": https://pgbackrest.org/configuration.html |
| | || **Key**         | PerconaPGCluster.spec.dataSource.pgbackrest.options |
| **Value**       | []string |
| **Required**    | false |
| **Example**     | |
| **Description** | Command line options to include when running the pgBackRest restore command. https://pgbackrest.org/command.html#command-restore |
| | || **Key**         | PerconaPGCluster.spec.dataSource.pgbackrest.priorityClassName |
| **Value**       | string |
| **Required**    | false |
| **Example**     | |
| **Description** | Priority class name for the pgBackRest restore Job pod. Changing this value causes PostgreSQL to restart. More info: https://kubernetes.io/docs/concepts/scheduling-eviction/pod-priority-preemption/ |
| | || **Key**         | PerconaPGCluster.spec.dataSource.pgbackrest.resources |
| **Value**       | object |
| **Required**    | false |
| **Example**     | |
| **Description** | Resource requirements for the pgBackRest restore Job. |
| | || **Key**         | PerconaPGCluster.spec.dataSource.pgbackrest.tolerations |
| **Value**       | []object |
| **Required**    | false |
| **Example**     | |
| **Description** | Tolerations of the pgBackRest restore Job. More info: https://kubernetes.io/docs/concepts/scheduling-eviction/taint-and-toleration |
| | |
| **Key**         | PerconaPGCluster.spec.dataSource.pgbackrest.repo.name |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | The name of the the repository |
| | || **Key**         | PerconaPGCluster.spec.dataSource.pgbackrest.repo.azure |
| **Value**       | object |
| **Required**    | false |
| **Example**     | |
| **Description** | Represents a pgBackRest repository that is created using Azure storage |
| | || **Key**         | PerconaPGCluster.spec.dataSource.pgbackrest.repo.gcs |
| **Value**       | object |
| **Required**    | false |
| **Example**     | |
| **Description** | Represents a pgBackRest repository that is created using Google Cloud Storage |
| | || **Key**         | PerconaPGCluster.spec.dataSource.pgbackrest.repo.s3 |
| **Value**       | object |
| **Required**    | false |
| **Example**     | |
| **Description** | RepoS3 represents a pgBackRest repository that is created using AWS S3 (or S3-compatible) storage |
| | || **Key**         | PerconaPGCluster.spec.dataSource.pgbackrest.repo.schedules |
| **Value**       | object |
| **Required**    | false |
| **Example**     | |
| **Description** | Defines the schedules for the pgBackRest backups Full, Differential and Incremental backup types are supported: https://pgbackrest.org/user-guide.html#concept/backup |
| | || **Key**         | PerconaPGCluster.spec.dataSource.pgbackrest.repo.volume |
| **Value**       | object |
| **Required**    | false |
| **Example**     | |
| **Description** | Represents a pgBackRest repository that is created using a PersistentVolumeClaim |
| | |
| **Key**         | PerconaPGCluster.spec.dataSource.pgbackrest.repo.azure.container |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | The Azure container utilized for the repository |
| | |
| **Key**         | PerconaPGCluster.spec.dataSource.pgbackrest.repo.gcs.bucket |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | The GCS bucket utilized for the repository |
| | |
| **Key**         | PerconaPGCluster.spec.dataSource.pgbackrest.repo.s3.bucket |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | The S3 bucket utilized for the repository |
| | || **Key**         | PerconaPGCluster.spec.dataSource.pgbackrest.repo.s3.endpoint |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | A valid endpoint corresponding to the specified region |
| | || **Key**         | PerconaPGCluster.spec.dataSource.pgbackrest.repo.s3.region |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | The region corresponding to the S3 bucket |
| | |
| **Key**         | PerconaPGCluster.spec.dataSource.pgbackrest.repo.schedules.differential |
| **Value**       | string |
| **Required**    | false |
| **Example**     | |
| **Description** | Defines the Cron schedule for a differential pgBackRest backup. Follows the standard Cron schedule syntax: https://k8s.io/docs/concepts/workloads/controllers/cron-jobs/#cron-schedule-syntax |
| | || **Key**         | PerconaPGCluster.spec.dataSource.pgbackrest.repo.schedules.full |
| **Value**       | string |
| **Required**    | false |
| **Example**     | |
| **Description** | Defines the Cron schedule for a full pgBackRest backup. Follows the standard Cron schedule syntax: https://k8s.io/docs/concepts/workloads/controllers/cron-jobs/#cron-schedule-syntax |
| | || **Key**         | PerconaPGCluster.spec.dataSource.pgbackrest.repo.schedules.incremental |
| **Value**       | string |
| **Required**    | false |
| **Example**     | |
| **Description** | Defines the Cron schedule for an incremental pgBackRest backup. Follows the standard Cron schedule syntax: https://k8s.io/docs/concepts/workloads/controllers/cron-jobs/#cron-schedule-syntax |
| | |
| **Key**         | PerconaPGCluster.spec.dataSource.pgbackrest.repo.volume.volumeClaimSpec |
| **Value**       | object |
| **Required**    | true |
| **Example**     | |
| **Description** | Defines a PersistentVolumeClaim spec used to create and/or bind a volume |
| | |
| **Key**         | PerconaPGCluster.spec.dataSource.pgbackrest.repo.volume.volumeClaimSpec.accessModes |
| **Value**       | []string |
| **Required**    | false |
| **Example**     | |
| **Description** | accessModes contains the desired access modes the volume should have. More info: https://kubernetes.io/docs/concepts/storage/persistent-volumes#access-modes-1 |
| | || **Key**         | PerconaPGCluster.spec.dataSource.pgbackrest.repo.volume.volumeClaimSpec.dataSource |
| **Value**       | object |
| **Required**    | false |
| **Example**     | |
| **Description** | dataSource field can be used to specify either: * An existing VolumeSnapshot object (snapshot.storage.k8s.io/VolumeSnapshot) * An existing PVC (PersistentVolumeClaim) If the provisioner or an external controller can support the specified data source, it will create a new volume based on the contents of the specified data source. If the AnyVolumeDataSource feature gate is enabled, this field will always have the same contents as the DataSourceRef field. |
| | || **Key**         | PerconaPGCluster.spec.dataSource.pgbackrest.repo.volume.volumeClaimSpec.dataSourceRef |
| **Value**       | object |
| **Required**    | false |
| **Example**     | |
| **Description** | dataSourceRef specifies the object from which to populate the volume with data, if a non-empty volume is desired. This may be any local object from a non-empty API group (non core object) or a PersistentVolumeClaim object. When this field is specified, volume binding will only succeed if the type of the specified object matches some installed volume populator or dynamic provisioner. This field will replace the functionality of the DataSource field and as such if both fields are non-empty, they must have the same value. For backwards compatibility, both fields (DataSource and DataSourceRef) will be set to the same value automatically if one of them is empty and the other is non-empty. There are two important differences between DataSource and DataSourceRef: * While DataSource only allows two specific types of objects, DataSourceRef allows any non-core object, as well as PersistentVolumeClaim objects. * While DataSource ignores disallowed values (dropping them), DataSourceRef preserves all values, and generates an error if a disallowed value is specified. (Beta) Using this field requires the AnyVolumeDataSource feature gate to be enabled. |
| | || **Key**         | PerconaPGCluster.spec.dataSource.pgbackrest.repo.volume.volumeClaimSpec.resources |
| **Value**       | object |
| **Required**    | false |
| **Example**     | |
| **Description** | resources represents the minimum resources the volume should have. If RecoverVolumeExpansionFailure feature is enabled users are allowed to specify resource requirements that are lower than previous value but must still be higher than capacity recorded in the status field of the claim. More info: https://kubernetes.io/docs/concepts/storage/persistent-volumes#resources |
| | || **Key**         | PerconaPGCluster.spec.dataSource.pgbackrest.repo.volume.volumeClaimSpec.selector |
| **Value**       | object |
| **Required**    | false |
| **Example**     | |
| **Description** | selector is a label query over volumes to consider for binding. |
| | || **Key**         | PerconaPGCluster.spec.dataSource.pgbackrest.repo.volume.volumeClaimSpec.storageClassName |
| **Value**       | string |
| **Required**    | false |
| **Example**     | |
| **Description** | storageClassName is the name of the StorageClass required by the claim. More info: https://kubernetes.io/docs/concepts/storage/persistent-volumes#class-1 |
| | || **Key**         | PerconaPGCluster.spec.dataSource.pgbackrest.repo.volume.volumeClaimSpec.volumeMode |
| **Value**       | string |
| **Required**    | false |
| **Example**     | |
| **Description** | volumeMode defines what type of volume is required by the claim. Value of Filesystem is implied when not included in claim spec. |
| | || **Key**         | PerconaPGCluster.spec.dataSource.pgbackrest.repo.volume.volumeClaimSpec.volumeName |
| **Value**       | string |
| **Required**    | false |
| **Example**     | |
| **Description** | volumeName is the binding reference to the PersistentVolume backing this claim. |
| | |
| **Key**         | PerconaPGCluster.spec.dataSource.pgbackrest.repo.volume.volumeClaimSpec.dataSource.kind |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | Kind is the type of resource being referenced |
| | || **Key**         | PerconaPGCluster.spec.dataSource.pgbackrest.repo.volume.volumeClaimSpec.dataSource.name |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | Name is the name of resource being referenced |
| | || **Key**         | PerconaPGCluster.spec.dataSource.pgbackrest.repo.volume.volumeClaimSpec.dataSource.apiGroup |
| **Value**       | string |
| **Required**    | false |
| **Example**     | |
| **Description** | APIGroup is the group for the resource being referenced. If APIGroup is not specified, the specified Kind must be in the core API group. For any other third-party types, APIGroup is required. |
| | |
| **Key**         | PerconaPGCluster.spec.dataSource.pgbackrest.repo.volume.volumeClaimSpec.dataSourceRef.kind |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | Kind is the type of resource being referenced |
| | || **Key**         | PerconaPGCluster.spec.dataSource.pgbackrest.repo.volume.volumeClaimSpec.dataSourceRef.name |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | Name is the name of resource being referenced |
| | || **Key**         | PerconaPGCluster.spec.dataSource.pgbackrest.repo.volume.volumeClaimSpec.dataSourceRef.apiGroup |
| **Value**       | string |
| **Required**    | false |
| **Example**     | |
| **Description** | APIGroup is the group for the resource being referenced. If APIGroup is not specified, the specified Kind must be in the core API group. For any other third-party types, APIGroup is required. |
| | |
| **Key**         | PerconaPGCluster.spec.dataSource.pgbackrest.repo.volume.volumeClaimSpec.resources.limits |
| **Value**       | map[string]int or string |
| **Required**    | false |
| **Example**     | |
| **Description** | Limits describes the maximum amount of compute resources allowed. More info: https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/ |
| | || **Key**         | PerconaPGCluster.spec.dataSource.pgbackrest.repo.volume.volumeClaimSpec.resources.requests |
| **Value**       | map[string]int or string |
| **Required**    | false |
| **Example**     | |
| **Description** | Requests describes the minimum amount of compute resources required. If Requests is omitted for a container, it defaults to Limits if that is explicitly specified, otherwise to an implementation-defined value. More info: https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/ |
| | |
| **Key**         | PerconaPGCluster.spec.dataSource.pgbackrest.repo.volume.volumeClaimSpec.selector.matchExpressions |
| **Value**       | []object |
| **Required**    | false |
| **Example**     | |
| **Description** | matchExpressions is a list of label selector requirements. The requirements are ANDed. |
| | || **Key**         | PerconaPGCluster.spec.dataSource.pgbackrest.repo.volume.volumeClaimSpec.selector.matchLabels |
| **Value**       | map[string]string |
| **Required**    | false |
| **Example**     | |
| **Description** | matchLabels is a map of {key,value} pairs. A single {key,value} in the matchLabels map is equivalent to an element of matchExpressions, whose key field is "key", the operator is "In", and the values array contains only "value". The requirements are ANDed. |
| | |
| **Key**         | PerconaPGCluster.spec.dataSource.pgbackrest.repo.volume.volumeClaimSpec.selector.matchExpressions[index].key |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | key is the label key that the selector applies to. |
| | || **Key**         | PerconaPGCluster.spec.dataSource.pgbackrest.repo.volume.volumeClaimSpec.selector.matchExpressions[index].operator |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | operator represents a key's relationship to a set of values. Valid operators are In, NotIn, Exists and DoesNotExist. |
| | || **Key**         | PerconaPGCluster.spec.dataSource.pgbackrest.repo.volume.volumeClaimSpec.selector.matchExpressions[index].values |
| **Value**       | []string |
| **Required**    | false |
| **Example**     | |
| **Description** | values is an array of string values. If the operator is In or NotIn, the values array must be non-empty. If the operator is Exists or DoesNotExist, the values array must be empty. This array is replaced during a strategic merge patch. |
| | |
| **Key**         | PerconaPGCluster.spec.dataSource.pgbackrest.affinity.nodeAffinity |
| **Value**       | object |
| **Required**    | false |
| **Example**     | |
| **Description** | Describes node affinity scheduling rules for the pod. |
| | || **Key**         | PerconaPGCluster.spec.dataSource.pgbackrest.affinity.podAffinity |
| **Value**       | object |
| **Required**    | false |
| **Example**     | |
| **Description** | Describes pod affinity scheduling rules (e.g. co-locate this pod in the same node, zone, etc. as some other pod(s)). |
| | || **Key**         | PerconaPGCluster.spec.dataSource.pgbackrest.affinity.podAntiAffinity |
| **Value**       | object |
| **Required**    | false |
| **Example**     | |
| **Description** | Describes pod anti-affinity scheduling rules (e.g. avoid putting this pod in the same node, zone, etc. as some other pod(s)). |
| | |
| **Key**         | PerconaPGCluster.spec.dataSource.pgbackrest.affinity.nodeAffinity.preferredDuringSchedulingIgnoredDuringExecution |
| **Value**       | []object |
| **Required**    | false |
| **Example**     | |
| **Description** | The scheduler will prefer to schedule pods to nodes that satisfy the affinity expressions specified by this field, but it may choose a node that violates one or more of the expressions. The node that is most preferred is the one with the greatest sum of weights, i.e. for each node that meets all of the scheduling requirements (resource request, requiredDuringScheduling affinity expressions, etc.), compute a sum by iterating through the elements of this field and adding "weight" to the sum if the node matches the corresponding matchExpressions; the node(s) with the highest sum are the most preferred. |
| | || **Key**         | PerconaPGCluster.spec.dataSource.pgbackrest.affinity.nodeAffinity.requiredDuringSchedulingIgnoredDuringExecution |
| **Value**       | object |
| **Required**    | false |
| **Example**     | |
| **Description** | If the affinity requirements specified by this field are not met at scheduling time, the pod will not be scheduled onto the node. If the affinity requirements specified by this field cease to be met at some point during pod execution (e.g. due to an update), the system may or may not try to eventually evict the pod from its node. |
| | |
| **Key**         | PerconaPGCluster.spec.dataSource.pgbackrest.affinity.nodeAffinity.preferredDuringSchedulingIgnoredDuringExecution[index].preference |
| **Value**       | object |
| **Required**    | true |
| **Example**     | |
| **Description** | A node selector term, associated with the corresponding weight. |
| | || **Key**         | PerconaPGCluster.spec.dataSource.pgbackrest.affinity.nodeAffinity.preferredDuringSchedulingIgnoredDuringExecution[index].weight |
| **Value**       | integer |
| **Required**    | true |
| **Example**     | |
| **Description** | Weight associated with matching the corresponding nodeSelectorTerm, in the range 1-100. |
| | |
| **Key**         | PerconaPGCluster.spec.dataSource.pgbackrest.affinity.nodeAffinity.preferredDuringSchedulingIgnoredDuringExecution[index].preference.matchExpressions |
| **Value**       | []object |
| **Required**    | false |
| **Example**     | |
| **Description** | A list of node selector requirements by node's labels. |
| | || **Key**         | PerconaPGCluster.spec.dataSource.pgbackrest.affinity.nodeAffinity.preferredDuringSchedulingIgnoredDuringExecution[index].preference.matchFields |
| **Value**       | []object |
| **Required**    | false |
| **Example**     | |
| **Description** | A list of node selector requirements by node's fields. |
| | |
| **Key**         | PerconaPGCluster.spec.dataSource.pgbackrest.affinity.nodeAffinity.preferredDuringSchedulingIgnoredDuringExecution[index].preference.matchExpressions[index].key |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | The label key that the selector applies to. |
| | || **Key**         | PerconaPGCluster.spec.dataSource.pgbackrest.affinity.nodeAffinity.preferredDuringSchedulingIgnoredDuringExecution[index].preference.matchExpressions[index].operator |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | Represents a key's relationship to a set of values. Valid operators are In, NotIn, Exists, DoesNotExist. Gt, and Lt. |
| | || **Key**         | PerconaPGCluster.spec.dataSource.pgbackrest.affinity.nodeAffinity.preferredDuringSchedulingIgnoredDuringExecution[index].preference.matchExpressions[index].values |
| **Value**       | []string |
| **Required**    | false |
| **Example**     | |
| **Description** | An array of string values. If the operator is In or NotIn, the values array must be non-empty. If the operator is Exists or DoesNotExist, the values array must be empty. If the operator is Gt or Lt, the values array must have a single element, which will be interpreted as an integer. This array is replaced during a strategic merge patch. |
| | |
| **Key**         | PerconaPGCluster.spec.dataSource.pgbackrest.affinity.nodeAffinity.preferredDuringSchedulingIgnoredDuringExecution[index].preference.matchFields[index].key |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | The label key that the selector applies to. |
| | || **Key**         | PerconaPGCluster.spec.dataSource.pgbackrest.affinity.nodeAffinity.preferredDuringSchedulingIgnoredDuringExecution[index].preference.matchFields[index].operator |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | Represents a key's relationship to a set of values. Valid operators are In, NotIn, Exists, DoesNotExist. Gt, and Lt. |
| | || **Key**         | PerconaPGCluster.spec.dataSource.pgbackrest.affinity.nodeAffinity.preferredDuringSchedulingIgnoredDuringExecution[index].preference.matchFields[index].values |
| **Value**       | []string |
| **Required**    | false |
| **Example**     | |
| **Description** | An array of string values. If the operator is In or NotIn, the values array must be non-empty. If the operator is Exists or DoesNotExist, the values array must be empty. If the operator is Gt or Lt, the values array must have a single element, which will be interpreted as an integer. This array is replaced during a strategic merge patch. |
| | |
| **Key**         | PerconaPGCluster.spec.dataSource.pgbackrest.affinity.nodeAffinity.requiredDuringSchedulingIgnoredDuringExecution.nodeSelectorTerms |
| **Value**       | []object |
| **Required**    | true |
| **Example**     | |
| **Description** | Required. A list of node selector terms. The terms are ORed. |
| | |
| **Key**         | PerconaPGCluster.spec.dataSource.pgbackrest.affinity.nodeAffinity.requiredDuringSchedulingIgnoredDuringExecution.nodeSelectorTerms[index].matchExpressions |
| **Value**       | []object |
| **Required**    | false |
| **Example**     | |
| **Description** | A list of node selector requirements by node's labels. |
| | || **Key**         | PerconaPGCluster.spec.dataSource.pgbackrest.affinity.nodeAffinity.requiredDuringSchedulingIgnoredDuringExecution.nodeSelectorTerms[index].matchFields |
| **Value**       | []object |
| **Required**    | false |
| **Example**     | |
| **Description** | A list of node selector requirements by node's fields. |
| | |
| **Key**         | PerconaPGCluster.spec.dataSource.pgbackrest.affinity.nodeAffinity.requiredDuringSchedulingIgnoredDuringExecution.nodeSelectorTerms[index].matchExpressions[index].key |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | The label key that the selector applies to. |
| | || **Key**         | PerconaPGCluster.spec.dataSource.pgbackrest.affinity.nodeAffinity.requiredDuringSchedulingIgnoredDuringExecution.nodeSelectorTerms[index].matchExpressions[index].operator |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | Represents a key's relationship to a set of values. Valid operators are In, NotIn, Exists, DoesNotExist. Gt, and Lt. |
| | || **Key**         | PerconaPGCluster.spec.dataSource.pgbackrest.affinity.nodeAffinity.requiredDuringSchedulingIgnoredDuringExecution.nodeSelectorTerms[index].matchExpressions[index].values |
| **Value**       | []string |
| **Required**    | false |
| **Example**     | |
| **Description** | An array of string values. If the operator is In or NotIn, the values array must be non-empty. If the operator is Exists or DoesNotExist, the values array must be empty. If the operator is Gt or Lt, the values array must have a single element, which will be interpreted as an integer. This array is replaced during a strategic merge patch. |
| | |
| **Key**         | PerconaPGCluster.spec.dataSource.pgbackrest.affinity.nodeAffinity.requiredDuringSchedulingIgnoredDuringExecution.nodeSelectorTerms[index].matchFields[index].key |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | The label key that the selector applies to. |
| | || **Key**         | PerconaPGCluster.spec.dataSource.pgbackrest.affinity.nodeAffinity.requiredDuringSchedulingIgnoredDuringExecution.nodeSelectorTerms[index].matchFields[index].operator |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | Represents a key's relationship to a set of values. Valid operators are In, NotIn, Exists, DoesNotExist. Gt, and Lt. |
| | || **Key**         | PerconaPGCluster.spec.dataSource.pgbackrest.affinity.nodeAffinity.requiredDuringSchedulingIgnoredDuringExecution.nodeSelectorTerms[index].matchFields[index].values |
| **Value**       | []string |
| **Required**    | false |
| **Example**     | |
| **Description** | An array of string values. If the operator is In or NotIn, the values array must be non-empty. If the operator is Exists or DoesNotExist, the values array must be empty. If the operator is Gt or Lt, the values array must have a single element, which will be interpreted as an integer. This array is replaced during a strategic merge patch. |
| | |
| **Key**         | PerconaPGCluster.spec.dataSource.pgbackrest.affinity.podAffinity.preferredDuringSchedulingIgnoredDuringExecution |
| **Value**       | []object |
| **Required**    | false |
| **Example**     | |
| **Description** | The scheduler will prefer to schedule pods to nodes that satisfy the affinity expressions specified by this field, but it may choose a node that violates one or more of the expressions. The node that is most preferred is the one with the greatest sum of weights, i.e. for each node that meets all of the scheduling requirements (resource request, requiredDuringScheduling affinity expressions, etc.), compute a sum by iterating through the elements of this field and adding "weight" to the sum if the node has pods which matches the corresponding podAffinityTerm; the node(s) with the highest sum are the most preferred. |
| | || **Key**         | PerconaPGCluster.spec.dataSource.pgbackrest.affinity.podAffinity.requiredDuringSchedulingIgnoredDuringExecution |
| **Value**       | []object |
| **Required**    | false |
| **Example**     | |
| **Description** | If the affinity requirements specified by this field are not met at scheduling time, the pod will not be scheduled onto the node. If the affinity requirements specified by this field cease to be met at some point during pod execution (e.g. due to a pod label update), the system may or may not try to eventually evict the pod from its node. When there are multiple elements, the lists of nodes corresponding to each podAffinityTerm are intersected, i.e. all terms must be satisfied. |
| | |
| **Key**         | PerconaPGCluster.spec.dataSource.pgbackrest.affinity.podAffinity.preferredDuringSchedulingIgnoredDuringExecution[index].podAffinityTerm |
| **Value**       | object |
| **Required**    | true |
| **Example**     | |
| **Description** | Required. A pod affinity term, associated with the corresponding weight. |
| | || **Key**         | PerconaPGCluster.spec.dataSource.pgbackrest.affinity.podAffinity.preferredDuringSchedulingIgnoredDuringExecution[index].weight |
| **Value**       | integer |
| **Required**    | true |
| **Example**     | |
| **Description** | weight associated with matching the corresponding podAffinityTerm, in the range 1-100. |
| | |
| **Key**         | PerconaPGCluster.spec.dataSource.pgbackrest.affinity.podAffinity.preferredDuringSchedulingIgnoredDuringExecution[index].podAffinityTerm.topologyKey |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | This pod should be co-located (affinity) or not co-located (anti-affinity) with the pods matching the labelSelector in the specified namespaces, where co-located is defined as running on a node whose value of the label with key topologyKey matches that of any node on which any of the selected pods is running. Empty topologyKey is not allowed. |
| | || **Key**         | PerconaPGCluster.spec.dataSource.pgbackrest.affinity.podAffinity.preferredDuringSchedulingIgnoredDuringExecution[index].podAffinityTerm.labelSelector |
| **Value**       | object |
| **Required**    | false |
| **Example**     | |
| **Description** | A label query over a set of resources, in this case pods. |
| | || **Key**         | PerconaPGCluster.spec.dataSource.pgbackrest.affinity.podAffinity.preferredDuringSchedulingIgnoredDuringExecution[index].podAffinityTerm.namespaceSelector |
| **Value**       | object |
| **Required**    | false |
| **Example**     | |
| **Description** | A label query over the set of namespaces that the term applies to. The term is applied to the union of the namespaces selected by this field and the ones listed in the namespaces field. null selector and null or empty namespaces list means "this pod's namespace". An empty selector ({}) matches all namespaces. |
| | || **Key**         | PerconaPGCluster.spec.dataSource.pgbackrest.affinity.podAffinity.preferredDuringSchedulingIgnoredDuringExecution[index].podAffinityTerm.namespaces |
| **Value**       | []string |
| **Required**    | false |
| **Example**     | |
| **Description** | namespaces specifies a static list of namespace names that the term applies to. The term is applied to the union of the namespaces listed in this field and the ones selected by namespaceSelector. null or empty namespaces list and null namespaceSelector means "this pod's namespace". |
| | |
| **Key**         | PerconaPGCluster.spec.dataSource.pgbackrest.affinity.podAffinity.preferredDuringSchedulingIgnoredDuringExecution[index].podAffinityTerm.labelSelector.matchExpressions |
| **Value**       | []object |
| **Required**    | false |
| **Example**     | |
| **Description** | matchExpressions is a list of label selector requirements. The requirements are ANDed. |
| | || **Key**         | PerconaPGCluster.spec.dataSource.pgbackrest.affinity.podAffinity.preferredDuringSchedulingIgnoredDuringExecution[index].podAffinityTerm.labelSelector.matchLabels |
| **Value**       | map[string]string |
| **Required**    | false |
| **Example**     | |
| **Description** | matchLabels is a map of {key,value} pairs. A single {key,value} in the matchLabels map is equivalent to an element of matchExpressions, whose key field is "key", the operator is "In", and the values array contains only "value". The requirements are ANDed. |
| | |
| **Key**         | PerconaPGCluster.spec.dataSource.pgbackrest.affinity.podAffinity.preferredDuringSchedulingIgnoredDuringExecution[index].podAffinityTerm.labelSelector.matchExpressions[index].key |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | key is the label key that the selector applies to. |
| | || **Key**         | PerconaPGCluster.spec.dataSource.pgbackrest.affinity.podAffinity.preferredDuringSchedulingIgnoredDuringExecution[index].podAffinityTerm.labelSelector.matchExpressions[index].operator |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | operator represents a key's relationship to a set of values. Valid operators are In, NotIn, Exists and DoesNotExist. |
| | || **Key**         | PerconaPGCluster.spec.dataSource.pgbackrest.affinity.podAffinity.preferredDuringSchedulingIgnoredDuringExecution[index].podAffinityTerm.labelSelector.matchExpressions[index].values |
| **Value**       | []string |
| **Required**    | false |
| **Example**     | |
| **Description** | values is an array of string values. If the operator is In or NotIn, the values array must be non-empty. If the operator is Exists or DoesNotExist, the values array must be empty. This array is replaced during a strategic merge patch. |
| | |
| **Key**         | PerconaPGCluster.spec.dataSource.pgbackrest.affinity.podAffinity.preferredDuringSchedulingIgnoredDuringExecution[index].podAffinityTerm.namespaceSelector.matchExpressions |
| **Value**       | []object |
| **Required**    | false |
| **Example**     | |
| **Description** | matchExpressions is a list of label selector requirements. The requirements are ANDed. |
| | || **Key**         | PerconaPGCluster.spec.dataSource.pgbackrest.affinity.podAffinity.preferredDuringSchedulingIgnoredDuringExecution[index].podAffinityTerm.namespaceSelector.matchLabels |
| **Value**       | map[string]string |
| **Required**    | false |
| **Example**     | |
| **Description** | matchLabels is a map of {key,value} pairs. A single {key,value} in the matchLabels map is equivalent to an element of matchExpressions, whose key field is "key", the operator is "In", and the values array contains only "value". The requirements are ANDed. |
| | |
| **Key**         | PerconaPGCluster.spec.dataSource.pgbackrest.affinity.podAffinity.preferredDuringSchedulingIgnoredDuringExecution[index].podAffinityTerm.namespaceSelector.matchExpressions[index].key |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | key is the label key that the selector applies to. |
| | || **Key**         | PerconaPGCluster.spec.dataSource.pgbackrest.affinity.podAffinity.preferredDuringSchedulingIgnoredDuringExecution[index].podAffinityTerm.namespaceSelector.matchExpressions[index].operator |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | operator represents a key's relationship to a set of values. Valid operators are In, NotIn, Exists and DoesNotExist. |
| | || **Key**         | PerconaPGCluster.spec.dataSource.pgbackrest.affinity.podAffinity.preferredDuringSchedulingIgnoredDuringExecution[index].podAffinityTerm.namespaceSelector.matchExpressions[index].values |
| **Value**       | []string |
| **Required**    | false |
| **Example**     | |
| **Description** | values is an array of string values. If the operator is In or NotIn, the values array must be non-empty. If the operator is Exists or DoesNotExist, the values array must be empty. This array is replaced during a strategic merge patch. |
| | |
| **Key**         | PerconaPGCluster.spec.dataSource.pgbackrest.affinity.podAffinity.requiredDuringSchedulingIgnoredDuringExecution[index].topologyKey |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | This pod should be co-located (affinity) or not co-located (anti-affinity) with the pods matching the labelSelector in the specified namespaces, where co-located is defined as running on a node whose value of the label with key topologyKey matches that of any node on which any of the selected pods is running. Empty topologyKey is not allowed. |
| | || **Key**         | PerconaPGCluster.spec.dataSource.pgbackrest.affinity.podAffinity.requiredDuringSchedulingIgnoredDuringExecution[index].labelSelector |
| **Value**       | object |
| **Required**    | false |
| **Example**     | |
| **Description** | A label query over a set of resources, in this case pods. |
| | || **Key**         | PerconaPGCluster.spec.dataSource.pgbackrest.affinity.podAffinity.requiredDuringSchedulingIgnoredDuringExecution[index].namespaceSelector |
| **Value**       | object |
| **Required**    | false |
| **Example**     | |
| **Description** | A label query over the set of namespaces that the term applies to. The term is applied to the union of the namespaces selected by this field and the ones listed in the namespaces field. null selector and null or empty namespaces list means "this pod's namespace". An empty selector ({}) matches all namespaces. |
| | || **Key**         | PerconaPGCluster.spec.dataSource.pgbackrest.affinity.podAffinity.requiredDuringSchedulingIgnoredDuringExecution[index].namespaces |
| **Value**       | []string |
| **Required**    | false |
| **Example**     | |
| **Description** | namespaces specifies a static list of namespace names that the term applies to. The term is applied to the union of the namespaces listed in this field and the ones selected by namespaceSelector. null or empty namespaces list and null namespaceSelector means "this pod's namespace". |
| | |
| **Key**         | PerconaPGCluster.spec.dataSource.pgbackrest.affinity.podAffinity.requiredDuringSchedulingIgnoredDuringExecution[index].labelSelector.matchExpressions |
| **Value**       | []object |
| **Required**    | false |
| **Example**     | |
| **Description** | matchExpressions is a list of label selector requirements. The requirements are ANDed. |
| | || **Key**         | PerconaPGCluster.spec.dataSource.pgbackrest.affinity.podAffinity.requiredDuringSchedulingIgnoredDuringExecution[index].labelSelector.matchLabels |
| **Value**       | map[string]string |
| **Required**    | false |
| **Example**     | |
| **Description** | matchLabels is a map of {key,value} pairs. A single {key,value} in the matchLabels map is equivalent to an element of matchExpressions, whose key field is "key", the operator is "In", and the values array contains only "value". The requirements are ANDed. |
| | |
| **Key**         | PerconaPGCluster.spec.dataSource.pgbackrest.affinity.podAffinity.requiredDuringSchedulingIgnoredDuringExecution[index].labelSelector.matchExpressions[index].key |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | key is the label key that the selector applies to. |
| | || **Key**         | PerconaPGCluster.spec.dataSource.pgbackrest.affinity.podAffinity.requiredDuringSchedulingIgnoredDuringExecution[index].labelSelector.matchExpressions[index].operator |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | operator represents a key's relationship to a set of values. Valid operators are In, NotIn, Exists and DoesNotExist. |
| | || **Key**         | PerconaPGCluster.spec.dataSource.pgbackrest.affinity.podAffinity.requiredDuringSchedulingIgnoredDuringExecution[index].labelSelector.matchExpressions[index].values |
| **Value**       | []string |
| **Required**    | false |
| **Example**     | |
| **Description** | values is an array of string values. If the operator is In or NotIn, the values array must be non-empty. If the operator is Exists or DoesNotExist, the values array must be empty. This array is replaced during a strategic merge patch. |
| | |
| **Key**         | PerconaPGCluster.spec.dataSource.pgbackrest.affinity.podAffinity.requiredDuringSchedulingIgnoredDuringExecution[index].namespaceSelector.matchExpressions |
| **Value**       | []object |
| **Required**    | false |
| **Example**     | |
| **Description** | matchExpressions is a list of label selector requirements. The requirements are ANDed. |
| | || **Key**         | PerconaPGCluster.spec.dataSource.pgbackrest.affinity.podAffinity.requiredDuringSchedulingIgnoredDuringExecution[index].namespaceSelector.matchLabels |
| **Value**       | map[string]string |
| **Required**    | false |
| **Example**     | |
| **Description** | matchLabels is a map of {key,value} pairs. A single {key,value} in the matchLabels map is equivalent to an element of matchExpressions, whose key field is "key", the operator is "In", and the values array contains only "value". The requirements are ANDed. |
| | |
| **Key**         | PerconaPGCluster.spec.dataSource.pgbackrest.affinity.podAffinity.requiredDuringSchedulingIgnoredDuringExecution[index].namespaceSelector.matchExpressions[index].key |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | key is the label key that the selector applies to. |
| | || **Key**         | PerconaPGCluster.spec.dataSource.pgbackrest.affinity.podAffinity.requiredDuringSchedulingIgnoredDuringExecution[index].namespaceSelector.matchExpressions[index].operator |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | operator represents a key's relationship to a set of values. Valid operators are In, NotIn, Exists and DoesNotExist. |
| | || **Key**         | PerconaPGCluster.spec.dataSource.pgbackrest.affinity.podAffinity.requiredDuringSchedulingIgnoredDuringExecution[index].namespaceSelector.matchExpressions[index].values |
| **Value**       | []string |
| **Required**    | false |
| **Example**     | |
| **Description** | values is an array of string values. If the operator is In or NotIn, the values array must be non-empty. If the operator is Exists or DoesNotExist, the values array must be empty. This array is replaced during a strategic merge patch. |
| | |
| **Key**         | PerconaPGCluster.spec.dataSource.pgbackrest.affinity.podAntiAffinity.preferredDuringSchedulingIgnoredDuringExecution |
| **Value**       | []object |
| **Required**    | false |
| **Example**     | |
| **Description** | The scheduler will prefer to schedule pods to nodes that satisfy the anti-affinity expressions specified by this field, but it may choose a node that violates one or more of the expressions. The node that is most preferred is the one with the greatest sum of weights, i.e. for each node that meets all of the scheduling requirements (resource request, requiredDuringScheduling anti-affinity expressions, etc.), compute a sum by iterating through the elements of this field and adding "weight" to the sum if the node has pods which matches the corresponding podAffinityTerm; the node(s) with the highest sum are the most preferred. |
| | || **Key**         | PerconaPGCluster.spec.dataSource.pgbackrest.affinity.podAntiAffinity.requiredDuringSchedulingIgnoredDuringExecution |
| **Value**       | []object |
| **Required**    | false |
| **Example**     | |
| **Description** | If the anti-affinity requirements specified by this field are not met at scheduling time, the pod will not be scheduled onto the node. If the anti-affinity requirements specified by this field cease to be met at some point during pod execution (e.g. due to a pod label update), the system may or may not try to eventually evict the pod from its node. When there are multiple elements, the lists of nodes corresponding to each podAffinityTerm are intersected, i.e. all terms must be satisfied. |
| | |
| **Key**         | PerconaPGCluster.spec.dataSource.pgbackrest.affinity.podAntiAffinity.preferredDuringSchedulingIgnoredDuringExecution[index].podAffinityTerm |
| **Value**       | object |
| **Required**    | true |
| **Example**     | |
| **Description** | Required. A pod affinity term, associated with the corresponding weight. |
| | || **Key**         | PerconaPGCluster.spec.dataSource.pgbackrest.affinity.podAntiAffinity.preferredDuringSchedulingIgnoredDuringExecution[index].weight |
| **Value**       | integer |
| **Required**    | true |
| **Example**     | |
| **Description** | weight associated with matching the corresponding podAffinityTerm, in the range 1-100. |
| | |
| **Key**         | PerconaPGCluster.spec.dataSource.pgbackrest.affinity.podAntiAffinity.preferredDuringSchedulingIgnoredDuringExecution[index].podAffinityTerm.topologyKey |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | This pod should be co-located (affinity) or not co-located (anti-affinity) with the pods matching the labelSelector in the specified namespaces, where co-located is defined as running on a node whose value of the label with key topologyKey matches that of any node on which any of the selected pods is running. Empty topologyKey is not allowed. |
| | || **Key**         | PerconaPGCluster.spec.dataSource.pgbackrest.affinity.podAntiAffinity.preferredDuringSchedulingIgnoredDuringExecution[index].podAffinityTerm.labelSelector |
| **Value**       | object |
| **Required**    | false |
| **Example**     | |
| **Description** | A label query over a set of resources, in this case pods. |
| | || **Key**         | PerconaPGCluster.spec.dataSource.pgbackrest.affinity.podAntiAffinity.preferredDuringSchedulingIgnoredDuringExecution[index].podAffinityTerm.namespaceSelector |
| **Value**       | object |
| **Required**    | false |
| **Example**     | |
| **Description** | A label query over the set of namespaces that the term applies to. The term is applied to the union of the namespaces selected by this field and the ones listed in the namespaces field. null selector and null or empty namespaces list means "this pod's namespace". An empty selector ({}) matches all namespaces. |
| | || **Key**         | PerconaPGCluster.spec.dataSource.pgbackrest.affinity.podAntiAffinity.preferredDuringSchedulingIgnoredDuringExecution[index].podAffinityTerm.namespaces |
| **Value**       | []string |
| **Required**    | false |
| **Example**     | |
| **Description** | namespaces specifies a static list of namespace names that the term applies to. The term is applied to the union of the namespaces listed in this field and the ones selected by namespaceSelector. null or empty namespaces list and null namespaceSelector means "this pod's namespace". |
| | |
| **Key**         | PerconaPGCluster.spec.dataSource.pgbackrest.affinity.podAntiAffinity.preferredDuringSchedulingIgnoredDuringExecution[index].podAffinityTerm.labelSelector.matchExpressions |
| **Value**       | []object |
| **Required**    | false |
| **Example**     | |
| **Description** | matchExpressions is a list of label selector requirements. The requirements are ANDed. |
| | || **Key**         | PerconaPGCluster.spec.dataSource.pgbackrest.affinity.podAntiAffinity.preferredDuringSchedulingIgnoredDuringExecution[index].podAffinityTerm.labelSelector.matchLabels |
| **Value**       | map[string]string |
| **Required**    | false |
| **Example**     | |
| **Description** | matchLabels is a map of {key,value} pairs. A single {key,value} in the matchLabels map is equivalent to an element of matchExpressions, whose key field is "key", the operator is "In", and the values array contains only "value". The requirements are ANDed. |
| | |
| **Key**         | PerconaPGCluster.spec.dataSource.pgbackrest.affinity.podAntiAffinity.preferredDuringSchedulingIgnoredDuringExecution[index].podAffinityTerm.labelSelector.matchExpressions[index].key |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | key is the label key that the selector applies to. |
| | || **Key**         | PerconaPGCluster.spec.dataSource.pgbackrest.affinity.podAntiAffinity.preferredDuringSchedulingIgnoredDuringExecution[index].podAffinityTerm.labelSelector.matchExpressions[index].operator |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | operator represents a key's relationship to a set of values. Valid operators are In, NotIn, Exists and DoesNotExist. |
| | || **Key**         | PerconaPGCluster.spec.dataSource.pgbackrest.affinity.podAntiAffinity.preferredDuringSchedulingIgnoredDuringExecution[index].podAffinityTerm.labelSelector.matchExpressions[index].values |
| **Value**       | []string |
| **Required**    | false |
| **Example**     | |
| **Description** | values is an array of string values. If the operator is In or NotIn, the values array must be non-empty. If the operator is Exists or DoesNotExist, the values array must be empty. This array is replaced during a strategic merge patch. |
| | |
| **Key**         | PerconaPGCluster.spec.dataSource.pgbackrest.affinity.podAntiAffinity.preferredDuringSchedulingIgnoredDuringExecution[index].podAffinityTerm.namespaceSelector.matchExpressions |
| **Value**       | []object |
| **Required**    | false |
| **Example**     | |
| **Description** | matchExpressions is a list of label selector requirements. The requirements are ANDed. |
| | || **Key**         | PerconaPGCluster.spec.dataSource.pgbackrest.affinity.podAntiAffinity.preferredDuringSchedulingIgnoredDuringExecution[index].podAffinityTerm.namespaceSelector.matchLabels |
| **Value**       | map[string]string |
| **Required**    | false |
| **Example**     | |
| **Description** | matchLabels is a map of {key,value} pairs. A single {key,value} in the matchLabels map is equivalent to an element of matchExpressions, whose key field is "key", the operator is "In", and the values array contains only "value". The requirements are ANDed. |
| | |
| **Key**         | PerconaPGCluster.spec.dataSource.pgbackrest.affinity.podAntiAffinity.preferredDuringSchedulingIgnoredDuringExecution[index].podAffinityTerm.namespaceSelector.matchExpressions[index].key |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | key is the label key that the selector applies to. |
| | || **Key**         | PerconaPGCluster.spec.dataSource.pgbackrest.affinity.podAntiAffinity.preferredDuringSchedulingIgnoredDuringExecution[index].podAffinityTerm.namespaceSelector.matchExpressions[index].operator |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | operator represents a key's relationship to a set of values. Valid operators are In, NotIn, Exists and DoesNotExist. |
| | || **Key**         | PerconaPGCluster.spec.dataSource.pgbackrest.affinity.podAntiAffinity.preferredDuringSchedulingIgnoredDuringExecution[index].podAffinityTerm.namespaceSelector.matchExpressions[index].values |
| **Value**       | []string |
| **Required**    | false |
| **Example**     | |
| **Description** | values is an array of string values. If the operator is In or NotIn, the values array must be non-empty. If the operator is Exists or DoesNotExist, the values array must be empty. This array is replaced during a strategic merge patch. |
| | |
| **Key**         | PerconaPGCluster.spec.dataSource.pgbackrest.affinity.podAntiAffinity.requiredDuringSchedulingIgnoredDuringExecution[index].topologyKey |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | This pod should be co-located (affinity) or not co-located (anti-affinity) with the pods matching the labelSelector in the specified namespaces, where co-located is defined as running on a node whose value of the label with key topologyKey matches that of any node on which any of the selected pods is running. Empty topologyKey is not allowed. |
| | || **Key**         | PerconaPGCluster.spec.dataSource.pgbackrest.affinity.podAntiAffinity.requiredDuringSchedulingIgnoredDuringExecution[index].labelSelector |
| **Value**       | object |
| **Required**    | false |
| **Example**     | |
| **Description** | A label query over a set of resources, in this case pods. |
| | || **Key**         | PerconaPGCluster.spec.dataSource.pgbackrest.affinity.podAntiAffinity.requiredDuringSchedulingIgnoredDuringExecution[index].namespaceSelector |
| **Value**       | object |
| **Required**    | false |
| **Example**     | |
| **Description** | A label query over the set of namespaces that the term applies to. The term is applied to the union of the namespaces selected by this field and the ones listed in the namespaces field. null selector and null or empty namespaces list means "this pod's namespace". An empty selector ({}) matches all namespaces. |
| | || **Key**         | PerconaPGCluster.spec.dataSource.pgbackrest.affinity.podAntiAffinity.requiredDuringSchedulingIgnoredDuringExecution[index].namespaces |
| **Value**       | []string |
| **Required**    | false |
| **Example**     | |
| **Description** | namespaces specifies a static list of namespace names that the term applies to. The term is applied to the union of the namespaces listed in this field and the ones selected by namespaceSelector. null or empty namespaces list and null namespaceSelector means "this pod's namespace". |
| | |
| **Key**         | PerconaPGCluster.spec.dataSource.pgbackrest.affinity.podAntiAffinity.requiredDuringSchedulingIgnoredDuringExecution[index].labelSelector.matchExpressions |
| **Value**       | []object |
| **Required**    | false |
| **Example**     | |
| **Description** | matchExpressions is a list of label selector requirements. The requirements are ANDed. |
| | || **Key**         | PerconaPGCluster.spec.dataSource.pgbackrest.affinity.podAntiAffinity.requiredDuringSchedulingIgnoredDuringExecution[index].labelSelector.matchLabels |
| **Value**       | map[string]string |
| **Required**    | false |
| **Example**     | |
| **Description** | matchLabels is a map of {key,value} pairs. A single {key,value} in the matchLabels map is equivalent to an element of matchExpressions, whose key field is "key", the operator is "In", and the values array contains only "value". The requirements are ANDed. |
| | |
| **Key**         | PerconaPGCluster.spec.dataSource.pgbackrest.affinity.podAntiAffinity.requiredDuringSchedulingIgnoredDuringExecution[index].labelSelector.matchExpressions[index].key |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | key is the label key that the selector applies to. |
| | || **Key**         | PerconaPGCluster.spec.dataSource.pgbackrest.affinity.podAntiAffinity.requiredDuringSchedulingIgnoredDuringExecution[index].labelSelector.matchExpressions[index].operator |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | operator represents a key's relationship to a set of values. Valid operators are In, NotIn, Exists and DoesNotExist. |
| | || **Key**         | PerconaPGCluster.spec.dataSource.pgbackrest.affinity.podAntiAffinity.requiredDuringSchedulingIgnoredDuringExecution[index].labelSelector.matchExpressions[index].values |
| **Value**       | []string |
| **Required**    | false |
| **Example**     | |
| **Description** | values is an array of string values. If the operator is In or NotIn, the values array must be non-empty. If the operator is Exists or DoesNotExist, the values array must be empty. This array is replaced during a strategic merge patch. |
| | |
| **Key**         | PerconaPGCluster.spec.dataSource.pgbackrest.affinity.podAntiAffinity.requiredDuringSchedulingIgnoredDuringExecution[index].namespaceSelector.matchExpressions |
| **Value**       | []object |
| **Required**    | false |
| **Example**     | |
| **Description** | matchExpressions is a list of label selector requirements. The requirements are ANDed. |
| | || **Key**         | PerconaPGCluster.spec.dataSource.pgbackrest.affinity.podAntiAffinity.requiredDuringSchedulingIgnoredDuringExecution[index].namespaceSelector.matchLabels |
| **Value**       | map[string]string |
| **Required**    | false |
| **Example**     | |
| **Description** | matchLabels is a map of {key,value} pairs. A single {key,value} in the matchLabels map is equivalent to an element of matchExpressions, whose key field is "key", the operator is "In", and the values array contains only "value". The requirements are ANDed. |
| | |
| **Key**         | PerconaPGCluster.spec.dataSource.pgbackrest.affinity.podAntiAffinity.requiredDuringSchedulingIgnoredDuringExecution[index].namespaceSelector.matchExpressions[index].key |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | key is the label key that the selector applies to. |
| | || **Key**         | PerconaPGCluster.spec.dataSource.pgbackrest.affinity.podAntiAffinity.requiredDuringSchedulingIgnoredDuringExecution[index].namespaceSelector.matchExpressions[index].operator |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | operator represents a key's relationship to a set of values. Valid operators are In, NotIn, Exists and DoesNotExist. |
| | || **Key**         | PerconaPGCluster.spec.dataSource.pgbackrest.affinity.podAntiAffinity.requiredDuringSchedulingIgnoredDuringExecution[index].namespaceSelector.matchExpressions[index].values |
| **Value**       | []string |
| **Required**    | false |
| **Example**     | |
| **Description** | values is an array of string values. If the operator is In or NotIn, the values array must be non-empty. If the operator is Exists or DoesNotExist, the values array must be empty. This array is replaced during a strategic merge patch. |
| | |
| **Key**         | PerconaPGCluster.spec.dataSource.pgbackrest.configuration[index].configMap |
| **Value**       | object |
| **Required**    | false |
| **Example**     | |
| **Description** | configMap information about the configMap data to project |
| | || **Key**         | PerconaPGCluster.spec.dataSource.pgbackrest.configuration[index].downwardAPI |
| **Value**       | object |
| **Required**    | false |
| **Example**     | |
| **Description** | downwardAPI information about the downwardAPI data to project |
| | || **Key**         | PerconaPGCluster.spec.dataSource.pgbackrest.configuration[index].secret |
| **Value**       | object |
| **Required**    | false |
| **Example**     | |
| **Description** | secret information about the secret data to project |
| | || **Key**         | PerconaPGCluster.spec.dataSource.pgbackrest.configuration[index].serviceAccountToken |
| **Value**       | object |
| **Required**    | false |
| **Example**     | |
| **Description** | serviceAccountToken is information about the serviceAccountToken data to project |
| | |
| **Key**         | PerconaPGCluster.spec.dataSource.pgbackrest.configuration[index].configMap.items |
| **Value**       | []object |
| **Required**    | false |
| **Example**     | |
| **Description** | items if unspecified, each key-value pair in the Data field of the referenced ConfigMap will be projected into the volume as a file whose name is the key and content is the value. If specified, the listed keys will be projected into the specified paths, and unlisted keys will not be present. If a key is specified which is not present in the ConfigMap, the volume setup will error unless it is marked optional. Paths must be relative and may not contain the '..' path or start with '..'. |
| | || **Key**         | PerconaPGCluster.spec.dataSource.pgbackrest.configuration[index].configMap.name |
| **Value**       | string |
| **Required**    | false |
| **Example**     | |
| **Description** | Name of the referent. More info: https://kubernetes.io/docs/concepts/overview/working-with-objects/names/#names TODO: Add other useful fields. apiVersion, kind, uid? |
| | || **Key**         | PerconaPGCluster.spec.dataSource.pgbackrest.configuration[index].configMap.optional |
| **Value**       | boolean |
| **Required**    | false |
| **Example**     | |
| **Description** | optional specify whether the ConfigMap or its keys must be defined |
| | |
| **Key**         | PerconaPGCluster.spec.dataSource.pgbackrest.configuration[index].configMap.items[index].key |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | key is the key to project. |
| | || **Key**         | PerconaPGCluster.spec.dataSource.pgbackrest.configuration[index].configMap.items[index].path |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | path is the relative path of the file to map the key to. May not be an absolute path. May not contain the path element '..'. May not start with the string '..'. |
| | || **Key**         | PerconaPGCluster.spec.dataSource.pgbackrest.configuration[index].configMap.items[index].mode |
| **Value**       | integer |
| **Required**    | false |
| **Example**     | |
| **Description** | mode is Optional: mode bits used to set permissions on this file. Must be an octal value between 0000 and 0777 or a decimal value between 0 and 511. YAML accepts both octal and decimal values, JSON requires decimal values for mode bits. If not specified, the volume defaultMode will be used. This might be in conflict with other options that affect the file mode, like fsGroup, and the result can be other mode bits set. |
| | |
| **Key**         | PerconaPGCluster.spec.dataSource.pgbackrest.configuration[index].downwardAPI.items |
| **Value**       | []object |
| **Required**    | false |
| **Example**     | |
| **Description** | Items is a list of DownwardAPIVolume file |
| | |
| **Key**         | PerconaPGCluster.spec.dataSource.pgbackrest.configuration[index].downwardAPI.items[index].path |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | Required: Path is  the relative path name of the file to be created. Must not be absolute or contain the '..' path. Must be utf-8 encoded. The first item of the relative path must not start with '..' |
| | || **Key**         | PerconaPGCluster.spec.dataSource.pgbackrest.configuration[index].downwardAPI.items[index].fieldRef |
| **Value**       | object |
| **Required**    | false |
| **Example**     | |
| **Description** | Required: Selects a field of the pod: only annotations, labels, name and namespace are supported. |
| | || **Key**         | PerconaPGCluster.spec.dataSource.pgbackrest.configuration[index].downwardAPI.items[index].mode |
| **Value**       | integer |
| **Required**    | false |
| **Example**     | |
| **Description** | Optional: mode bits used to set permissions on this file, must be an octal value between 0000 and 0777 or a decimal value between 0 and 511. YAML accepts both octal and decimal values, JSON requires decimal values for mode bits. If not specified, the volume defaultMode will be used. This might be in conflict with other options that affect the file mode, like fsGroup, and the result can be other mode bits set. |
| | || **Key**         | PerconaPGCluster.spec.dataSource.pgbackrest.configuration[index].downwardAPI.items[index].resourceFieldRef |
| **Value**       | object |
| **Required**    | false |
| **Example**     | |
| **Description** | Selects a resource of the container: only resources limits and requests (limits.cpu, limits.memory, requests.cpu and requests.memory) are currently supported. |
| | |
| **Key**         | PerconaPGCluster.spec.dataSource.pgbackrest.configuration[index].downwardAPI.items[index].fieldRef.fieldPath |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | Path of the field to select in the specified API version. |
| | || **Key**         | PerconaPGCluster.spec.dataSource.pgbackrest.configuration[index].downwardAPI.items[index].fieldRef.apiVersion |
| **Value**       | string |
| **Required**    | false |
| **Example**     | |
| **Description** | Version of the schema the FieldPath is written in terms of, defaults to "v1". |
| | |
| **Key**         | PerconaPGCluster.spec.dataSource.pgbackrest.configuration[index].downwardAPI.items[index].resourceFieldRef.resource |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | Required: resource to select |
| | || **Key**         | PerconaPGCluster.spec.dataSource.pgbackrest.configuration[index].downwardAPI.items[index].resourceFieldRef.containerName |
| **Value**       | string |
| **Required**    | false |
| **Example**     | |
| **Description** | Container name: required for volumes, optional for env vars |
| | || **Key**         | PerconaPGCluster.spec.dataSource.pgbackrest.configuration[index].downwardAPI.items[index].resourceFieldRef.divisor |
| **Value**       | int or string |
| **Required**    | false |
| **Example**     | |
| **Description** | Specifies the output format of the exposed resources, defaults to "1" |
| | |
| **Key**         | PerconaPGCluster.spec.dataSource.pgbackrest.configuration[index].secret.items |
| **Value**       | []object |
| **Required**    | false |
| **Example**     | |
| **Description** | items if unspecified, each key-value pair in the Data field of the referenced Secret will be projected into the volume as a file whose name is the key and content is the value. If specified, the listed keys will be projected into the specified paths, and unlisted keys will not be present. If a key is specified which is not present in the Secret, the volume setup will error unless it is marked optional. Paths must be relative and may not contain the '..' path or start with '..'. |
| | || **Key**         | PerconaPGCluster.spec.dataSource.pgbackrest.configuration[index].secret.name |
| **Value**       | string |
| **Required**    | false |
| **Example**     | |
| **Description** | Name of the referent. More info: https://kubernetes.io/docs/concepts/overview/working-with-objects/names/#names TODO: Add other useful fields. apiVersion, kind, uid? |
| | || **Key**         | PerconaPGCluster.spec.dataSource.pgbackrest.configuration[index].secret.optional |
| **Value**       | boolean |
| **Required**    | false |
| **Example**     | |
| **Description** | optional field specify whether the Secret or its key must be defined |
| | |
| **Key**         | PerconaPGCluster.spec.dataSource.pgbackrest.configuration[index].secret.items[index].key |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | key is the key to project. |
| | || **Key**         | PerconaPGCluster.spec.dataSource.pgbackrest.configuration[index].secret.items[index].path |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | path is the relative path of the file to map the key to. May not be an absolute path. May not contain the path element '..'. May not start with the string '..'. |
| | || **Key**         | PerconaPGCluster.spec.dataSource.pgbackrest.configuration[index].secret.items[index].mode |
| **Value**       | integer |
| **Required**    | false |
| **Example**     | |
| **Description** | mode is Optional: mode bits used to set permissions on this file. Must be an octal value between 0000 and 0777 or a decimal value between 0 and 511. YAML accepts both octal and decimal values, JSON requires decimal values for mode bits. If not specified, the volume defaultMode will be used. This might be in conflict with other options that affect the file mode, like fsGroup, and the result can be other mode bits set. |
| | |
| **Key**         | PerconaPGCluster.spec.dataSource.pgbackrest.configuration[index].serviceAccountToken.path |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | path is the path relative to the mount point of the file to project the token into. |
| | || **Key**         | PerconaPGCluster.spec.dataSource.pgbackrest.configuration[index].serviceAccountToken.audience |
| **Value**       | string |
| **Required**    | false |
| **Example**     | |
| **Description** | audience is the intended audience of the token. A recipient of a token must identify itself with an identifier specified in the audience of the token, and otherwise should reject the token. The audience defaults to the identifier of the apiserver. |
| | || **Key**         | PerconaPGCluster.spec.dataSource.pgbackrest.configuration[index].serviceAccountToken.expirationSeconds |
| **Value**       | integer |
| **Required**    | false |
| **Example**     | |
| **Description** | expirationSeconds is the requested duration of validity of the service account token. As the token approaches expiration, the kubelet volume plugin will proactively rotate the service account token. The kubelet will start trying to rotate the token if the token is older than 80 percent of its time to live or if the token is older than 24 hours.Defaults to 1 hour and must be at least 10 minutes. |
| | |
| **Key**         | PerconaPGCluster.spec.dataSource.pgbackrest.resources.limits |
| **Value**       | map[string]int or string |
| **Required**    | false |
| **Example**     | |
| **Description** | Limits describes the maximum amount of compute resources allowed. More info: https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/ |
| | || **Key**         | PerconaPGCluster.spec.dataSource.pgbackrest.resources.requests |
| **Value**       | map[string]int or string |
| **Required**    | false |
| **Example**     | |
| **Description** | Requests describes the minimum amount of compute resources required. If Requests is omitted for a container, it defaults to Limits if that is explicitly specified, otherwise to an implementation-defined value. More info: https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/ |
| | |
| **Key**         | PerconaPGCluster.spec.dataSource.pgbackrest.tolerations[index].effect |
| **Value**       | string |
| **Required**    | false |
| **Example**     | |
| **Description** | Effect indicates the taint effect to match. Empty means match all taint effects. When specified, allowed values are NoSchedule, PreferNoSchedule and NoExecute. |
| | || **Key**         | PerconaPGCluster.spec.dataSource.pgbackrest.tolerations[index].key |
| **Value**       | string |
| **Required**    | false |
| **Example**     | |
| **Description** | Key is the taint key that the toleration applies to. Empty means match all taint keys. If the key is empty, operator must be Exists; this combination means to match all values and all keys. |
| | || **Key**         | PerconaPGCluster.spec.dataSource.pgbackrest.tolerations[index].operator |
| **Value**       | string |
| **Required**    | false |
| **Example**     | |
| **Description** | Operator represents a key's relationship to the value. Valid operators are Exists and Equal. Defaults to Equal. Exists is equivalent to wildcard for value, so that a pod can tolerate all taints of a particular category. |
| | || **Key**         | PerconaPGCluster.spec.dataSource.pgbackrest.tolerations[index].tolerationSeconds |
| **Value**       | integer |
| **Required**    | false |
| **Example**     | |
| **Description** | TolerationSeconds represents the period of time the toleration (which must be of effect NoExecute, otherwise this field is ignored) tolerates the taint. By default, it is not set, which means tolerate the taint forever (do not evict). Zero and negative values will be treated as 0 (evict immediately) by the system. |
| | || **Key**         | PerconaPGCluster.spec.dataSource.pgbackrest.tolerations[index].value |
| **Value**       | string |
| **Required**    | false |
| **Example**     | |
| **Description** | Value is the taint value the toleration matches to. If the operator is Exists, the value should be empty, otherwise just a regular string. |
| | |
| **Key**         | PerconaPGCluster.spec.dataSource.postgresCluster.repoName |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | The name of the pgBackRest repo within the source PostgresCluster that contains the backups that should be utilized to perform a pgBackRest restore when initializing the data source for the new PostgresCluster. |
| | || **Key**         | PerconaPGCluster.spec.dataSource.postgresCluster.affinity |
| **Value**       | object |
| **Required**    | false |
| **Example**     | |
| **Description** | Scheduling constraints of the pgBackRest restore Job. More info: https://kubernetes.io/docs/concepts/scheduling-eviction/assign-pod-node |
| | || **Key**         | PerconaPGCluster.spec.dataSource.postgresCluster.clusterName |
| **Value**       | string |
| **Required**    | false |
| **Example**     | |
| **Description** | The name of an existing PostgresCluster to use as the data source for the new PostgresCluster. Defaults to the name of the PostgresCluster being created if not provided. |
| | || **Key**         | PerconaPGCluster.spec.dataSource.postgresCluster.clusterNamespace |
| **Value**       | string |
| **Required**    | false |
| **Example**     | |
| **Description** | The namespace of the cluster specified as the data source using the clusterName field. Defaults to the namespace of the PostgresCluster being created if not provided. |
| | || **Key**         | PerconaPGCluster.spec.dataSource.postgresCluster.options |
| **Value**       | []string |
| **Required**    | false |
| **Example**     | |
| **Description** | Command line options to include when running the pgBackRest restore command. https://pgbackrest.org/command.html#command-restore |
| | || **Key**         | PerconaPGCluster.spec.dataSource.postgresCluster.priorityClassName |
| **Value**       | string |
| **Required**    | false |
| **Example**     | |
| **Description** | Priority class name for the pgBackRest restore Job pod. Changing this value causes PostgreSQL to restart. More info: https://kubernetes.io/docs/concepts/scheduling-eviction/pod-priority-preemption/ |
| | || **Key**         | PerconaPGCluster.spec.dataSource.postgresCluster.resources |
| **Value**       | object |
| **Required**    | false |
| **Example**     | |
| **Description** | Resource requirements for the pgBackRest restore Job. |
| | || **Key**         | PerconaPGCluster.spec.dataSource.postgresCluster.tolerations |
| **Value**       | []object |
| **Required**    | false |
| **Example**     | |
| **Description** | Tolerations of the pgBackRest restore Job. More info: https://kubernetes.io/docs/concepts/scheduling-eviction/taint-and-toleration |
| | |
| **Key**         | PerconaPGCluster.spec.dataSource.postgresCluster.affinity.nodeAffinity |
| **Value**       | object |
| **Required**    | false |
| **Example**     | |
| **Description** | Describes node affinity scheduling rules for the pod. |
| | || **Key**         | PerconaPGCluster.spec.dataSource.postgresCluster.affinity.podAffinity |
| **Value**       | object |
| **Required**    | false |
| **Example**     | |
| **Description** | Describes pod affinity scheduling rules (e.g. co-locate this pod in the same node, zone, etc. as some other pod(s)). |
| | || **Key**         | PerconaPGCluster.spec.dataSource.postgresCluster.affinity.podAntiAffinity |
| **Value**       | object |
| **Required**    | false |
| **Example**     | |
| **Description** | Describes pod anti-affinity scheduling rules (e.g. avoid putting this pod in the same node, zone, etc. as some other pod(s)). |
| | |
| **Key**         | PerconaPGCluster.spec.dataSource.postgresCluster.affinity.nodeAffinity.preferredDuringSchedulingIgnoredDuringExecution |
| **Value**       | []object |
| **Required**    | false |
| **Example**     | |
| **Description** | The scheduler will prefer to schedule pods to nodes that satisfy the affinity expressions specified by this field, but it may choose a node that violates one or more of the expressions. The node that is most preferred is the one with the greatest sum of weights, i.e. for each node that meets all of the scheduling requirements (resource request, requiredDuringScheduling affinity expressions, etc.), compute a sum by iterating through the elements of this field and adding "weight" to the sum if the node matches the corresponding matchExpressions; the node(s) with the highest sum are the most preferred. |
| | || **Key**         | PerconaPGCluster.spec.dataSource.postgresCluster.affinity.nodeAffinity.requiredDuringSchedulingIgnoredDuringExecution |
| **Value**       | object |
| **Required**    | false |
| **Example**     | |
| **Description** | If the affinity requirements specified by this field are not met at scheduling time, the pod will not be scheduled onto the node. If the affinity requirements specified by this field cease to be met at some point during pod execution (e.g. due to an update), the system may or may not try to eventually evict the pod from its node. |
| | |
| **Key**         | PerconaPGCluster.spec.dataSource.postgresCluster.affinity.nodeAffinity.preferredDuringSchedulingIgnoredDuringExecution[index].preference |
| **Value**       | object |
| **Required**    | true |
| **Example**     | |
| **Description** | A node selector term, associated with the corresponding weight. |
| | || **Key**         | PerconaPGCluster.spec.dataSource.postgresCluster.affinity.nodeAffinity.preferredDuringSchedulingIgnoredDuringExecution[index].weight |
| **Value**       | integer |
| **Required**    | true |
| **Example**     | |
| **Description** | Weight associated with matching the corresponding nodeSelectorTerm, in the range 1-100. |
| | |
| **Key**         | PerconaPGCluster.spec.dataSource.postgresCluster.affinity.nodeAffinity.preferredDuringSchedulingIgnoredDuringExecution[index].preference.matchExpressions |
| **Value**       | []object |
| **Required**    | false |
| **Example**     | |
| **Description** | A list of node selector requirements by node's labels. |
| | || **Key**         | PerconaPGCluster.spec.dataSource.postgresCluster.affinity.nodeAffinity.preferredDuringSchedulingIgnoredDuringExecution[index].preference.matchFields |
| **Value**       | []object |
| **Required**    | false |
| **Example**     | |
| **Description** | A list of node selector requirements by node's fields. |
| | |
| **Key**         | PerconaPGCluster.spec.dataSource.postgresCluster.affinity.nodeAffinity.preferredDuringSchedulingIgnoredDuringExecution[index].preference.matchExpressions[index].key |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | The label key that the selector applies to. |
| | || **Key**         | PerconaPGCluster.spec.dataSource.postgresCluster.affinity.nodeAffinity.preferredDuringSchedulingIgnoredDuringExecution[index].preference.matchExpressions[index].operator |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | Represents a key's relationship to a set of values. Valid operators are In, NotIn, Exists, DoesNotExist. Gt, and Lt. |
| | || **Key**         | PerconaPGCluster.spec.dataSource.postgresCluster.affinity.nodeAffinity.preferredDuringSchedulingIgnoredDuringExecution[index].preference.matchExpressions[index].values |
| **Value**       | []string |
| **Required**    | false |
| **Example**     | |
| **Description** | An array of string values. If the operator is In or NotIn, the values array must be non-empty. If the operator is Exists or DoesNotExist, the values array must be empty. If the operator is Gt or Lt, the values array must have a single element, which will be interpreted as an integer. This array is replaced during a strategic merge patch. |
| | |
| **Key**         | PerconaPGCluster.spec.dataSource.postgresCluster.affinity.nodeAffinity.preferredDuringSchedulingIgnoredDuringExecution[index].preference.matchFields[index].key |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | The label key that the selector applies to. |
| | || **Key**         | PerconaPGCluster.spec.dataSource.postgresCluster.affinity.nodeAffinity.preferredDuringSchedulingIgnoredDuringExecution[index].preference.matchFields[index].operator |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | Represents a key's relationship to a set of values. Valid operators are In, NotIn, Exists, DoesNotExist. Gt, and Lt. |
| | || **Key**         | PerconaPGCluster.spec.dataSource.postgresCluster.affinity.nodeAffinity.preferredDuringSchedulingIgnoredDuringExecution[index].preference.matchFields[index].values |
| **Value**       | []string |
| **Required**    | false |
| **Example**     | |
| **Description** | An array of string values. If the operator is In or NotIn, the values array must be non-empty. If the operator is Exists or DoesNotExist, the values array must be empty. If the operator is Gt or Lt, the values array must have a single element, which will be interpreted as an integer. This array is replaced during a strategic merge patch. |
| | |
| **Key**         | PerconaPGCluster.spec.dataSource.postgresCluster.affinity.nodeAffinity.requiredDuringSchedulingIgnoredDuringExecution.nodeSelectorTerms |
| **Value**       | []object |
| **Required**    | true |
| **Example**     | |
| **Description** | Required. A list of node selector terms. The terms are ORed. |
| | |
| **Key**         | PerconaPGCluster.spec.dataSource.postgresCluster.affinity.nodeAffinity.requiredDuringSchedulingIgnoredDuringExecution.nodeSelectorTerms[index].matchExpressions |
| **Value**       | []object |
| **Required**    | false |
| **Example**     | |
| **Description** | A list of node selector requirements by node's labels. |
| | || **Key**         | PerconaPGCluster.spec.dataSource.postgresCluster.affinity.nodeAffinity.requiredDuringSchedulingIgnoredDuringExecution.nodeSelectorTerms[index].matchFields |
| **Value**       | []object |
| **Required**    | false |
| **Example**     | |
| **Description** | A list of node selector requirements by node's fields. |
| | |
| **Key**         | PerconaPGCluster.spec.dataSource.postgresCluster.affinity.nodeAffinity.requiredDuringSchedulingIgnoredDuringExecution.nodeSelectorTerms[index].matchExpressions[index].key |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | The label key that the selector applies to. |
| | || **Key**         | PerconaPGCluster.spec.dataSource.postgresCluster.affinity.nodeAffinity.requiredDuringSchedulingIgnoredDuringExecution.nodeSelectorTerms[index].matchExpressions[index].operator |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | Represents a key's relationship to a set of values. Valid operators are In, NotIn, Exists, DoesNotExist. Gt, and Lt. |
| | || **Key**         | PerconaPGCluster.spec.dataSource.postgresCluster.affinity.nodeAffinity.requiredDuringSchedulingIgnoredDuringExecution.nodeSelectorTerms[index].matchExpressions[index].values |
| **Value**       | []string |
| **Required**    | false |
| **Example**     | |
| **Description** | An array of string values. If the operator is In or NotIn, the values array must be non-empty. If the operator is Exists or DoesNotExist, the values array must be empty. If the operator is Gt or Lt, the values array must have a single element, which will be interpreted as an integer. This array is replaced during a strategic merge patch. |
| | |
| **Key**         | PerconaPGCluster.spec.dataSource.postgresCluster.affinity.nodeAffinity.requiredDuringSchedulingIgnoredDuringExecution.nodeSelectorTerms[index].matchFields[index].key |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | The label key that the selector applies to. |
| | || **Key**         | PerconaPGCluster.spec.dataSource.postgresCluster.affinity.nodeAffinity.requiredDuringSchedulingIgnoredDuringExecution.nodeSelectorTerms[index].matchFields[index].operator |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | Represents a key's relationship to a set of values. Valid operators are In, NotIn, Exists, DoesNotExist. Gt, and Lt. |
| | || **Key**         | PerconaPGCluster.spec.dataSource.postgresCluster.affinity.nodeAffinity.requiredDuringSchedulingIgnoredDuringExecution.nodeSelectorTerms[index].matchFields[index].values |
| **Value**       | []string |
| **Required**    | false |
| **Example**     | |
| **Description** | An array of string values. If the operator is In or NotIn, the values array must be non-empty. If the operator is Exists or DoesNotExist, the values array must be empty. If the operator is Gt or Lt, the values array must have a single element, which will be interpreted as an integer. This array is replaced during a strategic merge patch. |
| | |
| **Key**         | PerconaPGCluster.spec.dataSource.postgresCluster.affinity.podAffinity.preferredDuringSchedulingIgnoredDuringExecution |
| **Value**       | []object |
| **Required**    | false |
| **Example**     | |
| **Description** | The scheduler will prefer to schedule pods to nodes that satisfy the affinity expressions specified by this field, but it may choose a node that violates one or more of the expressions. The node that is most preferred is the one with the greatest sum of weights, i.e. for each node that meets all of the scheduling requirements (resource request, requiredDuringScheduling affinity expressions, etc.), compute a sum by iterating through the elements of this field and adding "weight" to the sum if the node has pods which matches the corresponding podAffinityTerm; the node(s) with the highest sum are the most preferred. |
| | || **Key**         | PerconaPGCluster.spec.dataSource.postgresCluster.affinity.podAffinity.requiredDuringSchedulingIgnoredDuringExecution |
| **Value**       | []object |
| **Required**    | false |
| **Example**     | |
| **Description** | If the affinity requirements specified by this field are not met at scheduling time, the pod will not be scheduled onto the node. If the affinity requirements specified by this field cease to be met at some point during pod execution (e.g. due to a pod label update), the system may or may not try to eventually evict the pod from its node. When there are multiple elements, the lists of nodes corresponding to each podAffinityTerm are intersected, i.e. all terms must be satisfied. |
| | |
| **Key**         | PerconaPGCluster.spec.dataSource.postgresCluster.affinity.podAffinity.preferredDuringSchedulingIgnoredDuringExecution[index].podAffinityTerm |
| **Value**       | object |
| **Required**    | true |
| **Example**     | |
| **Description** | Required. A pod affinity term, associated with the corresponding weight. |
| | || **Key**         | PerconaPGCluster.spec.dataSource.postgresCluster.affinity.podAffinity.preferredDuringSchedulingIgnoredDuringExecution[index].weight |
| **Value**       | integer |
| **Required**    | true |
| **Example**     | |
| **Description** | weight associated with matching the corresponding podAffinityTerm, in the range 1-100. |
| | |
| **Key**         | PerconaPGCluster.spec.dataSource.postgresCluster.affinity.podAffinity.preferredDuringSchedulingIgnoredDuringExecution[index].podAffinityTerm.topologyKey |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | This pod should be co-located (affinity) or not co-located (anti-affinity) with the pods matching the labelSelector in the specified namespaces, where co-located is defined as running on a node whose value of the label with key topologyKey matches that of any node on which any of the selected pods is running. Empty topologyKey is not allowed. |
| | || **Key**         | PerconaPGCluster.spec.dataSource.postgresCluster.affinity.podAffinity.preferredDuringSchedulingIgnoredDuringExecution[index].podAffinityTerm.labelSelector |
| **Value**       | object |
| **Required**    | false |
| **Example**     | |
| **Description** | A label query over a set of resources, in this case pods. |
| | || **Key**         | PerconaPGCluster.spec.dataSource.postgresCluster.affinity.podAffinity.preferredDuringSchedulingIgnoredDuringExecution[index].podAffinityTerm.namespaceSelector |
| **Value**       | object |
| **Required**    | false |
| **Example**     | |
| **Description** | A label query over the set of namespaces that the term applies to. The term is applied to the union of the namespaces selected by this field and the ones listed in the namespaces field. null selector and null or empty namespaces list means "this pod's namespace". An empty selector ({}) matches all namespaces. |
| | || **Key**         | PerconaPGCluster.spec.dataSource.postgresCluster.affinity.podAffinity.preferredDuringSchedulingIgnoredDuringExecution[index].podAffinityTerm.namespaces |
| **Value**       | []string |
| **Required**    | false |
| **Example**     | |
| **Description** | namespaces specifies a static list of namespace names that the term applies to. The term is applied to the union of the namespaces listed in this field and the ones selected by namespaceSelector. null or empty namespaces list and null namespaceSelector means "this pod's namespace". |
| | |
| **Key**         | PerconaPGCluster.spec.dataSource.postgresCluster.affinity.podAffinity.preferredDuringSchedulingIgnoredDuringExecution[index].podAffinityTerm.labelSelector.matchExpressions |
| **Value**       | []object |
| **Required**    | false |
| **Example**     | |
| **Description** | matchExpressions is a list of label selector requirements. The requirements are ANDed. |
| | || **Key**         | PerconaPGCluster.spec.dataSource.postgresCluster.affinity.podAffinity.preferredDuringSchedulingIgnoredDuringExecution[index].podAffinityTerm.labelSelector.matchLabels |
| **Value**       | map[string]string |
| **Required**    | false |
| **Example**     | |
| **Description** | matchLabels is a map of {key,value} pairs. A single {key,value} in the matchLabels map is equivalent to an element of matchExpressions, whose key field is "key", the operator is "In", and the values array contains only "value". The requirements are ANDed. |
| | |
| **Key**         | PerconaPGCluster.spec.dataSource.postgresCluster.affinity.podAffinity.preferredDuringSchedulingIgnoredDuringExecution[index].podAffinityTerm.labelSelector.matchExpressions[index].key |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | key is the label key that the selector applies to. |
| | || **Key**         | PerconaPGCluster.spec.dataSource.postgresCluster.affinity.podAffinity.preferredDuringSchedulingIgnoredDuringExecution[index].podAffinityTerm.labelSelector.matchExpressions[index].operator |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | operator represents a key's relationship to a set of values. Valid operators are In, NotIn, Exists and DoesNotExist. |
| | || **Key**         | PerconaPGCluster.spec.dataSource.postgresCluster.affinity.podAffinity.preferredDuringSchedulingIgnoredDuringExecution[index].podAffinityTerm.labelSelector.matchExpressions[index].values |
| **Value**       | []string |
| **Required**    | false |
| **Example**     | |
| **Description** | values is an array of string values. If the operator is In or NotIn, the values array must be non-empty. If the operator is Exists or DoesNotExist, the values array must be empty. This array is replaced during a strategic merge patch. |
| | |
| **Key**         | PerconaPGCluster.spec.dataSource.postgresCluster.affinity.podAffinity.preferredDuringSchedulingIgnoredDuringExecution[index].podAffinityTerm.namespaceSelector.matchExpressions |
| **Value**       | []object |
| **Required**    | false |
| **Example**     | |
| **Description** | matchExpressions is a list of label selector requirements. The requirements are ANDed. |
| | || **Key**         | PerconaPGCluster.spec.dataSource.postgresCluster.affinity.podAffinity.preferredDuringSchedulingIgnoredDuringExecution[index].podAffinityTerm.namespaceSelector.matchLabels |
| **Value**       | map[string]string |
| **Required**    | false |
| **Example**     | |
| **Description** | matchLabels is a map of {key,value} pairs. A single {key,value} in the matchLabels map is equivalent to an element of matchExpressions, whose key field is "key", the operator is "In", and the values array contains only "value". The requirements are ANDed. |
| | |
| **Key**         | PerconaPGCluster.spec.dataSource.postgresCluster.affinity.podAffinity.preferredDuringSchedulingIgnoredDuringExecution[index].podAffinityTerm.namespaceSelector.matchExpressions[index].key |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | key is the label key that the selector applies to. |
| | || **Key**         | PerconaPGCluster.spec.dataSource.postgresCluster.affinity.podAffinity.preferredDuringSchedulingIgnoredDuringExecution[index].podAffinityTerm.namespaceSelector.matchExpressions[index].operator |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | operator represents a key's relationship to a set of values. Valid operators are In, NotIn, Exists and DoesNotExist. |
| | || **Key**         | PerconaPGCluster.spec.dataSource.postgresCluster.affinity.podAffinity.preferredDuringSchedulingIgnoredDuringExecution[index].podAffinityTerm.namespaceSelector.matchExpressions[index].values |
| **Value**       | []string |
| **Required**    | false |
| **Example**     | |
| **Description** | values is an array of string values. If the operator is In or NotIn, the values array must be non-empty. If the operator is Exists or DoesNotExist, the values array must be empty. This array is replaced during a strategic merge patch. |
| | |
| **Key**         | PerconaPGCluster.spec.dataSource.postgresCluster.affinity.podAffinity.requiredDuringSchedulingIgnoredDuringExecution[index].topologyKey |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | This pod should be co-located (affinity) or not co-located (anti-affinity) with the pods matching the labelSelector in the specified namespaces, where co-located is defined as running on a node whose value of the label with key topologyKey matches that of any node on which any of the selected pods is running. Empty topologyKey is not allowed. |
| | || **Key**         | PerconaPGCluster.spec.dataSource.postgresCluster.affinity.podAffinity.requiredDuringSchedulingIgnoredDuringExecution[index].labelSelector |
| **Value**       | object |
| **Required**    | false |
| **Example**     | |
| **Description** | A label query over a set of resources, in this case pods. |
| | || **Key**         | PerconaPGCluster.spec.dataSource.postgresCluster.affinity.podAffinity.requiredDuringSchedulingIgnoredDuringExecution[index].namespaceSelector |
| **Value**       | object |
| **Required**    | false |
| **Example**     | |
| **Description** | A label query over the set of namespaces that the term applies to. The term is applied to the union of the namespaces selected by this field and the ones listed in the namespaces field. null selector and null or empty namespaces list means "this pod's namespace". An empty selector ({}) matches all namespaces. |
| | || **Key**         | PerconaPGCluster.spec.dataSource.postgresCluster.affinity.podAffinity.requiredDuringSchedulingIgnoredDuringExecution[index].namespaces |
| **Value**       | []string |
| **Required**    | false |
| **Example**     | |
| **Description** | namespaces specifies a static list of namespace names that the term applies to. The term is applied to the union of the namespaces listed in this field and the ones selected by namespaceSelector. null or empty namespaces list and null namespaceSelector means "this pod's namespace". |
| | |
| **Key**         | PerconaPGCluster.spec.dataSource.postgresCluster.affinity.podAffinity.requiredDuringSchedulingIgnoredDuringExecution[index].labelSelector.matchExpressions |
| **Value**       | []object |
| **Required**    | false |
| **Example**     | |
| **Description** | matchExpressions is a list of label selector requirements. The requirements are ANDed. |
| | || **Key**         | PerconaPGCluster.spec.dataSource.postgresCluster.affinity.podAffinity.requiredDuringSchedulingIgnoredDuringExecution[index].labelSelector.matchLabels |
| **Value**       | map[string]string |
| **Required**    | false |
| **Example**     | |
| **Description** | matchLabels is a map of {key,value} pairs. A single {key,value} in the matchLabels map is equivalent to an element of matchExpressions, whose key field is "key", the operator is "In", and the values array contains only "value". The requirements are ANDed. |
| | |
| **Key**         | PerconaPGCluster.spec.dataSource.postgresCluster.affinity.podAffinity.requiredDuringSchedulingIgnoredDuringExecution[index].labelSelector.matchExpressions[index].key |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | key is the label key that the selector applies to. |
| | || **Key**         | PerconaPGCluster.spec.dataSource.postgresCluster.affinity.podAffinity.requiredDuringSchedulingIgnoredDuringExecution[index].labelSelector.matchExpressions[index].operator |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | operator represents a key's relationship to a set of values. Valid operators are In, NotIn, Exists and DoesNotExist. |
| | || **Key**         | PerconaPGCluster.spec.dataSource.postgresCluster.affinity.podAffinity.requiredDuringSchedulingIgnoredDuringExecution[index].labelSelector.matchExpressions[index].values |
| **Value**       | []string |
| **Required**    | false |
| **Example**     | |
| **Description** | values is an array of string values. If the operator is In or NotIn, the values array must be non-empty. If the operator is Exists or DoesNotExist, the values array must be empty. This array is replaced during a strategic merge patch. |
| | |
| **Key**         | PerconaPGCluster.spec.dataSource.postgresCluster.affinity.podAffinity.requiredDuringSchedulingIgnoredDuringExecution[index].namespaceSelector.matchExpressions |
| **Value**       | []object |
| **Required**    | false |
| **Example**     | |
| **Description** | matchExpressions is a list of label selector requirements. The requirements are ANDed. |
| | || **Key**         | PerconaPGCluster.spec.dataSource.postgresCluster.affinity.podAffinity.requiredDuringSchedulingIgnoredDuringExecution[index].namespaceSelector.matchLabels |
| **Value**       | map[string]string |
| **Required**    | false |
| **Example**     | |
| **Description** | matchLabels is a map of {key,value} pairs. A single {key,value} in the matchLabels map is equivalent to an element of matchExpressions, whose key field is "key", the operator is "In", and the values array contains only "value". The requirements are ANDed. |
| | |
| **Key**         | PerconaPGCluster.spec.dataSource.postgresCluster.affinity.podAffinity.requiredDuringSchedulingIgnoredDuringExecution[index].namespaceSelector.matchExpressions[index].key |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | key is the label key that the selector applies to. |
| | || **Key**         | PerconaPGCluster.spec.dataSource.postgresCluster.affinity.podAffinity.requiredDuringSchedulingIgnoredDuringExecution[index].namespaceSelector.matchExpressions[index].operator |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | operator represents a key's relationship to a set of values. Valid operators are In, NotIn, Exists and DoesNotExist. |
| | || **Key**         | PerconaPGCluster.spec.dataSource.postgresCluster.affinity.podAffinity.requiredDuringSchedulingIgnoredDuringExecution[index].namespaceSelector.matchExpressions[index].values |
| **Value**       | []string |
| **Required**    | false |
| **Example**     | |
| **Description** | values is an array of string values. If the operator is In or NotIn, the values array must be non-empty. If the operator is Exists or DoesNotExist, the values array must be empty. This array is replaced during a strategic merge patch. |
| | |
| **Key**         | PerconaPGCluster.spec.dataSource.postgresCluster.affinity.podAntiAffinity.preferredDuringSchedulingIgnoredDuringExecution |
| **Value**       | []object |
| **Required**    | false |
| **Example**     | |
| **Description** | The scheduler will prefer to schedule pods to nodes that satisfy the anti-affinity expressions specified by this field, but it may choose a node that violates one or more of the expressions. The node that is most preferred is the one with the greatest sum of weights, i.e. for each node that meets all of the scheduling requirements (resource request, requiredDuringScheduling anti-affinity expressions, etc.), compute a sum by iterating through the elements of this field and adding "weight" to the sum if the node has pods which matches the corresponding podAffinityTerm; the node(s) with the highest sum are the most preferred. |
| | || **Key**         | PerconaPGCluster.spec.dataSource.postgresCluster.affinity.podAntiAffinity.requiredDuringSchedulingIgnoredDuringExecution |
| **Value**       | []object |
| **Required**    | false |
| **Example**     | |
| **Description** | If the anti-affinity requirements specified by this field are not met at scheduling time, the pod will not be scheduled onto the node. If the anti-affinity requirements specified by this field cease to be met at some point during pod execution (e.g. due to a pod label update), the system may or may not try to eventually evict the pod from its node. When there are multiple elements, the lists of nodes corresponding to each podAffinityTerm are intersected, i.e. all terms must be satisfied. |
| | |
| **Key**         | PerconaPGCluster.spec.dataSource.postgresCluster.affinity.podAntiAffinity.preferredDuringSchedulingIgnoredDuringExecution[index].podAffinityTerm |
| **Value**       | object |
| **Required**    | true |
| **Example**     | |
| **Description** | Required. A pod affinity term, associated with the corresponding weight. |
| | || **Key**         | PerconaPGCluster.spec.dataSource.postgresCluster.affinity.podAntiAffinity.preferredDuringSchedulingIgnoredDuringExecution[index].weight |
| **Value**       | integer |
| **Required**    | true |
| **Example**     | |
| **Description** | weight associated with matching the corresponding podAffinityTerm, in the range 1-100. |
| | |
| **Key**         | PerconaPGCluster.spec.dataSource.postgresCluster.affinity.podAntiAffinity.preferredDuringSchedulingIgnoredDuringExecution[index].podAffinityTerm.topologyKey |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | This pod should be co-located (affinity) or not co-located (anti-affinity) with the pods matching the labelSelector in the specified namespaces, where co-located is defined as running on a node whose value of the label with key topologyKey matches that of any node on which any of the selected pods is running. Empty topologyKey is not allowed. |
| | || **Key**         | PerconaPGCluster.spec.dataSource.postgresCluster.affinity.podAntiAffinity.preferredDuringSchedulingIgnoredDuringExecution[index].podAffinityTerm.labelSelector |
| **Value**       | object |
| **Required**    | false |
| **Example**     | |
| **Description** | A label query over a set of resources, in this case pods. |
| | || **Key**         | PerconaPGCluster.spec.dataSource.postgresCluster.affinity.podAntiAffinity.preferredDuringSchedulingIgnoredDuringExecution[index].podAffinityTerm.namespaceSelector |
| **Value**       | object |
| **Required**    | false |
| **Example**     | |
| **Description** | A label query over the set of namespaces that the term applies to. The term is applied to the union of the namespaces selected by this field and the ones listed in the namespaces field. null selector and null or empty namespaces list means "this pod's namespace". An empty selector ({}) matches all namespaces. |
| | || **Key**         | PerconaPGCluster.spec.dataSource.postgresCluster.affinity.podAntiAffinity.preferredDuringSchedulingIgnoredDuringExecution[index].podAffinityTerm.namespaces |
| **Value**       | []string |
| **Required**    | false |
| **Example**     | |
| **Description** | namespaces specifies a static list of namespace names that the term applies to. The term is applied to the union of the namespaces listed in this field and the ones selected by namespaceSelector. null or empty namespaces list and null namespaceSelector means "this pod's namespace". |
| | |
| **Key**         | PerconaPGCluster.spec.dataSource.postgresCluster.affinity.podAntiAffinity.preferredDuringSchedulingIgnoredDuringExecution[index].podAffinityTerm.labelSelector.matchExpressions |
| **Value**       | []object |
| **Required**    | false |
| **Example**     | |
| **Description** | matchExpressions is a list of label selector requirements. The requirements are ANDed. |
| | || **Key**         | PerconaPGCluster.spec.dataSource.postgresCluster.affinity.podAntiAffinity.preferredDuringSchedulingIgnoredDuringExecution[index].podAffinityTerm.labelSelector.matchLabels |
| **Value**       | map[string]string |
| **Required**    | false |
| **Example**     | |
| **Description** | matchLabels is a map of {key,value} pairs. A single {key,value} in the matchLabels map is equivalent to an element of matchExpressions, whose key field is "key", the operator is "In", and the values array contains only "value". The requirements are ANDed. |
| | |
| **Key**         | PerconaPGCluster.spec.dataSource.postgresCluster.affinity.podAntiAffinity.preferredDuringSchedulingIgnoredDuringExecution[index].podAffinityTerm.labelSelector.matchExpressions[index].key |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | key is the label key that the selector applies to. |
| | || **Key**         | PerconaPGCluster.spec.dataSource.postgresCluster.affinity.podAntiAffinity.preferredDuringSchedulingIgnoredDuringExecution[index].podAffinityTerm.labelSelector.matchExpressions[index].operator |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | operator represents a key's relationship to a set of values. Valid operators are In, NotIn, Exists and DoesNotExist. |
| | || **Key**         | PerconaPGCluster.spec.dataSource.postgresCluster.affinity.podAntiAffinity.preferredDuringSchedulingIgnoredDuringExecution[index].podAffinityTerm.labelSelector.matchExpressions[index].values |
| **Value**       | []string |
| **Required**    | false |
| **Example**     | |
| **Description** | values is an array of string values. If the operator is In or NotIn, the values array must be non-empty. If the operator is Exists or DoesNotExist, the values array must be empty. This array is replaced during a strategic merge patch. |
| | |
| **Key**         | PerconaPGCluster.spec.dataSource.postgresCluster.affinity.podAntiAffinity.preferredDuringSchedulingIgnoredDuringExecution[index].podAffinityTerm.namespaceSelector.matchExpressions |
| **Value**       | []object |
| **Required**    | false |
| **Example**     | |
| **Description** | matchExpressions is a list of label selector requirements. The requirements are ANDed. |
| | || **Key**         | PerconaPGCluster.spec.dataSource.postgresCluster.affinity.podAntiAffinity.preferredDuringSchedulingIgnoredDuringExecution[index].podAffinityTerm.namespaceSelector.matchLabels |
| **Value**       | map[string]string |
| **Required**    | false |
| **Example**     | |
| **Description** | matchLabels is a map of {key,value} pairs. A single {key,value} in the matchLabels map is equivalent to an element of matchExpressions, whose key field is "key", the operator is "In", and the values array contains only "value". The requirements are ANDed. |
| | |
| **Key**         | PerconaPGCluster.spec.dataSource.postgresCluster.affinity.podAntiAffinity.preferredDuringSchedulingIgnoredDuringExecution[index].podAffinityTerm.namespaceSelector.matchExpressions[index].key |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | key is the label key that the selector applies to. |
| | || **Key**         | PerconaPGCluster.spec.dataSource.postgresCluster.affinity.podAntiAffinity.preferredDuringSchedulingIgnoredDuringExecution[index].podAffinityTerm.namespaceSelector.matchExpressions[index].operator |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | operator represents a key's relationship to a set of values. Valid operators are In, NotIn, Exists and DoesNotExist. |
| | || **Key**         | PerconaPGCluster.spec.dataSource.postgresCluster.affinity.podAntiAffinity.preferredDuringSchedulingIgnoredDuringExecution[index].podAffinityTerm.namespaceSelector.matchExpressions[index].values |
| **Value**       | []string |
| **Required**    | false |
| **Example**     | |
| **Description** | values is an array of string values. If the operator is In or NotIn, the values array must be non-empty. If the operator is Exists or DoesNotExist, the values array must be empty. This array is replaced during a strategic merge patch. |
| | |
| **Key**         | PerconaPGCluster.spec.dataSource.postgresCluster.affinity.podAntiAffinity.requiredDuringSchedulingIgnoredDuringExecution[index].topologyKey |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | This pod should be co-located (affinity) or not co-located (anti-affinity) with the pods matching the labelSelector in the specified namespaces, where co-located is defined as running on a node whose value of the label with key topologyKey matches that of any node on which any of the selected pods is running. Empty topologyKey is not allowed. |
| | || **Key**         | PerconaPGCluster.spec.dataSource.postgresCluster.affinity.podAntiAffinity.requiredDuringSchedulingIgnoredDuringExecution[index].labelSelector |
| **Value**       | object |
| **Required**    | false |
| **Example**     | |
| **Description** | A label query over a set of resources, in this case pods. |
| | || **Key**         | PerconaPGCluster.spec.dataSource.postgresCluster.affinity.podAntiAffinity.requiredDuringSchedulingIgnoredDuringExecution[index].namespaceSelector |
| **Value**       | object |
| **Required**    | false |
| **Example**     | |
| **Description** | A label query over the set of namespaces that the term applies to. The term is applied to the union of the namespaces selected by this field and the ones listed in the namespaces field. null selector and null or empty namespaces list means "this pod's namespace". An empty selector ({}) matches all namespaces. |
| | || **Key**         | PerconaPGCluster.spec.dataSource.postgresCluster.affinity.podAntiAffinity.requiredDuringSchedulingIgnoredDuringExecution[index].namespaces |
| **Value**       | []string |
| **Required**    | false |
| **Example**     | |
| **Description** | namespaces specifies a static list of namespace names that the term applies to. The term is applied to the union of the namespaces listed in this field and the ones selected by namespaceSelector. null or empty namespaces list and null namespaceSelector means "this pod's namespace". |
| | |
| **Key**         | PerconaPGCluster.spec.dataSource.postgresCluster.affinity.podAntiAffinity.requiredDuringSchedulingIgnoredDuringExecution[index].labelSelector.matchExpressions |
| **Value**       | []object |
| **Required**    | false |
| **Example**     | |
| **Description** | matchExpressions is a list of label selector requirements. The requirements are ANDed. |
| | || **Key**         | PerconaPGCluster.spec.dataSource.postgresCluster.affinity.podAntiAffinity.requiredDuringSchedulingIgnoredDuringExecution[index].labelSelector.matchLabels |
| **Value**       | map[string]string |
| **Required**    | false |
| **Example**     | |
| **Description** | matchLabels is a map of {key,value} pairs. A single {key,value} in the matchLabels map is equivalent to an element of matchExpressions, whose key field is "key", the operator is "In", and the values array contains only "value". The requirements are ANDed. |
| | |
| **Key**         | PerconaPGCluster.spec.dataSource.postgresCluster.affinity.podAntiAffinity.requiredDuringSchedulingIgnoredDuringExecution[index].labelSelector.matchExpressions[index].key |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | key is the label key that the selector applies to. |
| | || **Key**         | PerconaPGCluster.spec.dataSource.postgresCluster.affinity.podAntiAffinity.requiredDuringSchedulingIgnoredDuringExecution[index].labelSelector.matchExpressions[index].operator |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | operator represents a key's relationship to a set of values. Valid operators are In, NotIn, Exists and DoesNotExist. |
| | || **Key**         | PerconaPGCluster.spec.dataSource.postgresCluster.affinity.podAntiAffinity.requiredDuringSchedulingIgnoredDuringExecution[index].labelSelector.matchExpressions[index].values |
| **Value**       | []string |
| **Required**    | false |
| **Example**     | |
| **Description** | values is an array of string values. If the operator is In or NotIn, the values array must be non-empty. If the operator is Exists or DoesNotExist, the values array must be empty. This array is replaced during a strategic merge patch. |
| | |
| **Key**         | PerconaPGCluster.spec.dataSource.postgresCluster.affinity.podAntiAffinity.requiredDuringSchedulingIgnoredDuringExecution[index].namespaceSelector.matchExpressions |
| **Value**       | []object |
| **Required**    | false |
| **Example**     | |
| **Description** | matchExpressions is a list of label selector requirements. The requirements are ANDed. |
| | || **Key**         | PerconaPGCluster.spec.dataSource.postgresCluster.affinity.podAntiAffinity.requiredDuringSchedulingIgnoredDuringExecution[index].namespaceSelector.matchLabels |
| **Value**       | map[string]string |
| **Required**    | false |
| **Example**     | |
| **Description** | matchLabels is a map of {key,value} pairs. A single {key,value} in the matchLabels map is equivalent to an element of matchExpressions, whose key field is "key", the operator is "In", and the values array contains only "value". The requirements are ANDed. |
| | |
| **Key**         | PerconaPGCluster.spec.dataSource.postgresCluster.affinity.podAntiAffinity.requiredDuringSchedulingIgnoredDuringExecution[index].namespaceSelector.matchExpressions[index].key |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | key is the label key that the selector applies to. |
| | || **Key**         | PerconaPGCluster.spec.dataSource.postgresCluster.affinity.podAntiAffinity.requiredDuringSchedulingIgnoredDuringExecution[index].namespaceSelector.matchExpressions[index].operator |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | operator represents a key's relationship to a set of values. Valid operators are In, NotIn, Exists and DoesNotExist. |
| | || **Key**         | PerconaPGCluster.spec.dataSource.postgresCluster.affinity.podAntiAffinity.requiredDuringSchedulingIgnoredDuringExecution[index].namespaceSelector.matchExpressions[index].values |
| **Value**       | []string |
| **Required**    | false |
| **Example**     | |
| **Description** | values is an array of string values. If the operator is In or NotIn, the values array must be non-empty. If the operator is Exists or DoesNotExist, the values array must be empty. This array is replaced during a strategic merge patch. |
| | |
| **Key**         | PerconaPGCluster.spec.dataSource.postgresCluster.resources.limits |
| **Value**       | map[string]int or string |
| **Required**    | false |
| **Example**     | |
| **Description** | Limits describes the maximum amount of compute resources allowed. More info: https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/ |
| | || **Key**         | PerconaPGCluster.spec.dataSource.postgresCluster.resources.requests |
| **Value**       | map[string]int or string |
| **Required**    | false |
| **Example**     | |
| **Description** | Requests describes the minimum amount of compute resources required. If Requests is omitted for a container, it defaults to Limits if that is explicitly specified, otherwise to an implementation-defined value. More info: https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/ |
| | |
| **Key**         | PerconaPGCluster.spec.dataSource.postgresCluster.tolerations[index].effect |
| **Value**       | string |
| **Required**    | false |
| **Example**     | |
| **Description** | Effect indicates the taint effect to match. Empty means match all taint effects. When specified, allowed values are NoSchedule, PreferNoSchedule and NoExecute. |
| | || **Key**         | PerconaPGCluster.spec.dataSource.postgresCluster.tolerations[index].key |
| **Value**       | string |
| **Required**    | false |
| **Example**     | |
| **Description** | Key is the taint key that the toleration applies to. Empty means match all taint keys. If the key is empty, operator must be Exists; this combination means to match all values and all keys. |
| | || **Key**         | PerconaPGCluster.spec.dataSource.postgresCluster.tolerations[index].operator |
| **Value**       | string |
| **Required**    | false |
| **Example**     | |
| **Description** | Operator represents a key's relationship to the value. Valid operators are Exists and Equal. Defaults to Equal. Exists is equivalent to wildcard for value, so that a pod can tolerate all taints of a particular category. |
| | || **Key**         | PerconaPGCluster.spec.dataSource.postgresCluster.tolerations[index].tolerationSeconds |
| **Value**       | integer |
| **Required**    | false |
| **Example**     | |
| **Description** | TolerationSeconds represents the period of time the toleration (which must be of effect NoExecute, otherwise this field is ignored) tolerates the taint. By default, it is not set, which means tolerate the taint forever (do not evict). Zero and negative values will be treated as 0 (evict immediately) by the system. |
| | || **Key**         | PerconaPGCluster.spec.dataSource.postgresCluster.tolerations[index].value |
| **Value**       | string |
| **Required**    | false |
| **Example**     | |
| **Description** | Value is the taint value the toleration matches to. If the operator is Exists, the value should be empty, otherwise just a regular string. |
| | |
| **Key**         | PerconaPGCluster.spec.dataSource.volumes.pgBackRestVolume |
| **Value**       | object |
| **Required**    | false |
| **Example**     | |
| **Description** | Defines the existing pgBackRest repo volume and directory to use in the current PostgresCluster. |
| | || **Key**         | PerconaPGCluster.spec.dataSource.volumes.pgDataVolume |
| **Value**       | object |
| **Required**    | false |
| **Example**     | |
| **Description** | Defines the existing pgData volume and directory to use in the current PostgresCluster. |
| | || **Key**         | PerconaPGCluster.spec.dataSource.volumes.pgWALVolume |
| **Value**       | object |
| **Required**    | false |
| **Example**     | |
| **Description** | Defines the existing pg_wal volume and directory to use in the current PostgresCluster. Note that a defined pg_wal volume MUST be accompanied by a pgData volume. |
| | |
| **Key**         | PerconaPGCluster.spec.dataSource.volumes.pgBackRestVolume.pvcName |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | The existing PVC name. |
| | || **Key**         | PerconaPGCluster.spec.dataSource.volumes.pgBackRestVolume.directory |
| **Value**       | string |
| **Required**    | false |
| **Example**     | |
| **Description** | The existing directory. When not set, a move Job is not created for the associated volume. |
| | |
| **Key**         | PerconaPGCluster.spec.dataSource.volumes.pgDataVolume.pvcName |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | The existing PVC name. |
| | || **Key**         | PerconaPGCluster.spec.dataSource.volumes.pgDataVolume.directory |
| **Value**       | string |
| **Required**    | false |
| **Example**     | |
| **Description** | The existing directory. When not set, a move Job is not created for the associated volume. |
| | |
| **Key**         | PerconaPGCluster.spec.dataSource.volumes.pgWALVolume.pvcName |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | The existing PVC name. |
| | || **Key**         | PerconaPGCluster.spec.dataSource.volumes.pgWALVolume.directory |
| **Value**       | string |
| **Required**    | false |
| **Example**     | |
| **Description** | The existing directory. When not set, a move Job is not created for the associated volume. |
| | |
| **Key**         | PerconaPGCluster.spec.databaseInitSQL.key |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | Key is the ConfigMap data key that points to a SQL string |
| | || **Key**         | PerconaPGCluster.spec.databaseInitSQL.name |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | Name is the name of a ConfigMap |
| | |
| **Key**         | PerconaPGCluster.spec.expose.annotations |
| **Value**       | map[string]string |
| **Required**    | false |
| **Example**     | |
| **Description** |  |
| | || **Key**         | PerconaPGCluster.spec.expose.labels |
| **Value**       | map[string]string |
| **Required**    | false |
| **Example**     | |
| **Description** |  |
| | || **Key**         | PerconaPGCluster.spec.expose.nodePort |
| **Value**       | integer |
| **Required**    | false |
| **Example**     | |
| **Description** | The port on which this service is exposed when type is NodePort or LoadBalancer. Value must be in-range and not in use or the operation will fail. If unspecified, a port will be allocated if this Service requires one. - https://kubernetes.io/docs/concepts/services-networking/service/#type-nodeport |
| | || **Key**         | PerconaPGCluster.spec.expose.type |
| **Value**       | enum |
| **Required**    | false |
| **Example**     | |
| **Description** | More info: https://kubernetes.io/docs/concepts/services-networking/service/#publishing-services-service-types |
| | |
| **Key**         | PerconaPGCluster.spec.imagePullSecrets[index].name |
| **Value**       | string |
| **Required**    | false |
| **Example**     | |
| **Description** | Name of the referent. More info: https://kubernetes.io/docs/concepts/overview/working-with-objects/names/#names TODO: Add other useful fields. apiVersion, kind, uid? |
| | |
| **Key**         | PerconaPGCluster.spec.patroni.dynamicConfiguration |
| **Value**       | object |
| **Required**    | false |
| **Example**     | |
| **Description** | Patroni dynamic configuration settings. Changes to this value will be automatically reloaded without validation. Changes to certain PostgreSQL parameters cause PostgreSQL to restart. More info: https://patroni.readthedocs.io/en/latest/SETTINGS.html |
| | || **Key**         | PerconaPGCluster.spec.patroni.leaderLeaseDurationSeconds |
| **Value**       | integer |
| **Required**    | false |
| **Example**     | |
| **Description** | TTL of the cluster leader lock. "Think of it as the length of time before initiation of the automatic failover process." Changing this value causes PostgreSQL to restart. |
| | || **Key**         | PerconaPGCluster.spec.patroni.port |
| **Value**       | integer |
| **Required**    | false |
| **Example**     | |
| **Description** | The port on which Patroni should listen. Changing this value causes PostgreSQL to restart. |
| | || **Key**         | PerconaPGCluster.spec.patroni.switchover |
| **Value**       | object |
| **Required**    | false |
| **Example**     | |
| **Description** | Switchover gives options to perform ad hoc switchovers in a PostgresCluster. |
| | || **Key**         | PerconaPGCluster.spec.patroni.syncPeriodSeconds |
| **Value**       | integer |
| **Required**    | false |
| **Example**     | |
| **Description** | The interval for refreshing the leader lock and applying dynamicConfiguration. Must be less than leaderLeaseDurationSeconds. Changing this value causes PostgreSQL to restart. |
| | |
| **Key**         | PerconaPGCluster.spec.patroni.switchover.enabled |
| **Value**       | boolean |
| **Required**    | true |
| **Example**     | |
| **Description** | Whether or not the operator should allow switchovers in a PostgresCluster |
| | || **Key**         | PerconaPGCluster.spec.patroni.switchover.targetInstance |
| **Value**       | string |
| **Required**    | false |
| **Example**     | |
| **Description** | The instance that should become primary during a switchover. This field is optional when Type is "Switchover" and required when Type is "Failover". When it is not specified, a healthy replica is automatically selected. |
| | || **Key**         | PerconaPGCluster.spec.patroni.switchover.type |
| **Value**       | enum |
| **Required**    | false |
| **Example**     | |
| **Description** | Type of switchover to perform. Valid options are Switchover and Failover. "Switchover" changes the primary instance of a healthy PostgresCluster. "Failover" forces a particular instance to be primary, regardless of other factors. A TargetInstance must be specified to failover. NOTE: The Failover type is reserved as the "last resort" case. |
| | |
| **Key**         | PerconaPGCluster.spec.pmm.enabled |
| **Value**       | boolean |
| **Required**    | true |
| **Example**     | |
| **Description** |  |
| | || **Key**         | PerconaPGCluster.spec.pmm.image |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** |  |
| | || **Key**         | PerconaPGCluster.spec.pmm.containerSecurityContext |
| **Value**       | object |
| **Required**    | false |
| **Example**     | |
| **Description** | SecurityContext holds security configuration that will be applied to a container. Some fields are present in both SecurityContext and PodSecurityContext.  When both are set, the values in SecurityContext take precedence. |
| | || **Key**         | PerconaPGCluster.spec.pmm.imagePullPolicy |
| **Value**       | enum |
| **Required**    | false |
| **Example**     | |
| **Description** | ImagePullPolicy is used to determine when Kubernetes will attempt to pull (download) container images. More info: https://kubernetes.io/docs/concepts/containers/images/#image-pull-policy |
| | || **Key**         | PerconaPGCluster.spec.pmm.resources |
| **Value**       | object |
| **Required**    | false |
| **Example**     | |
| **Description** | Compute resources of a PMM container. |
| | || **Key**         | PerconaPGCluster.spec.pmm.runtimeClassName |
| **Value**       | string |
| **Required**    | false |
| **Example**     | |
| **Description** |  |
| | || **Key**         | PerconaPGCluster.spec.pmm.secret |
| **Value**       | string |
| **Required**    | false |
| **Example**     | |
| **Description** |  |
| | || **Key**         | PerconaPGCluster.spec.pmm.serverHost |
| **Value**       | string |
| **Required**    | false |
| **Example**     | |
| **Description** |  |
| | |
| **Key**         | PerconaPGCluster.spec.pmm.containerSecurityContext.allowPrivilegeEscalation |
| **Value**       | boolean |
| **Required**    | false |
| **Example**     | |
| **Description** | AllowPrivilegeEscalation controls whether a process can gain more privileges than its parent process. This bool directly controls if the no_new_privs flag will be set on the container process. AllowPrivilegeEscalation is true always when the container is: 1) run as Privileged 2) has CAP_SYS_ADMIN Note that this field cannot be set when spec.os.name is windows. |
| | || **Key**         | PerconaPGCluster.spec.pmm.containerSecurityContext.capabilities |
| **Value**       | object |
| **Required**    | false |
| **Example**     | |
| **Description** | The capabilities to add/drop when running containers. Defaults to the default set of capabilities granted by the container runtime. Note that this field cannot be set when spec.os.name is windows. |
| | || **Key**         | PerconaPGCluster.spec.pmm.containerSecurityContext.privileged |
| **Value**       | boolean |
| **Required**    | false |
| **Example**     | |
| **Description** | Run container in privileged mode. Processes in privileged containers are essentially equivalent to root on the host. Defaults to false. Note that this field cannot be set when spec.os.name is windows. |
| | || **Key**         | PerconaPGCluster.spec.pmm.containerSecurityContext.procMount |
| **Value**       | string |
| **Required**    | false |
| **Example**     | |
| **Description** | procMount denotes the type of proc mount to use for the containers. The default is DefaultProcMount which uses the container runtime defaults for readonly paths and masked paths. This requires the ProcMountType feature flag to be enabled. Note that this field cannot be set when spec.os.name is windows. |
| | || **Key**         | PerconaPGCluster.spec.pmm.containerSecurityContext.readOnlyRootFilesystem |
| **Value**       | boolean |
| **Required**    | false |
| **Example**     | |
| **Description** | Whether this container has a read-only root filesystem. Default is false. Note that this field cannot be set when spec.os.name is windows. |
| | || **Key**         | PerconaPGCluster.spec.pmm.containerSecurityContext.runAsGroup |
| **Value**       | integer |
| **Required**    | false |
| **Example**     | |
| **Description** | The GID to run the entrypoint of the container process. Uses runtime default if unset. May also be set in PodSecurityContext.  If set in both SecurityContext and PodSecurityContext, the value specified in SecurityContext takes precedence. Note that this field cannot be set when spec.os.name is windows. |
| | || **Key**         | PerconaPGCluster.spec.pmm.containerSecurityContext.runAsNonRoot |
| **Value**       | boolean |
| **Required**    | false |
| **Example**     | |
| **Description** | Indicates that the container must run as a non-root user. If true, the Kubelet will validate the image at runtime to ensure that it does not run as UID 0 (root) and fail to start the container if it does. If unset or false, no such validation will be performed. May also be set in PodSecurityContext.  If set in both SecurityContext and PodSecurityContext, the value specified in SecurityContext takes precedence. |
| | || **Key**         | PerconaPGCluster.spec.pmm.containerSecurityContext.runAsUser |
| **Value**       | integer |
| **Required**    | false |
| **Example**     | |
| **Description** | The UID to run the entrypoint of the container process. Defaults to user specified in image metadata if unspecified. May also be set in PodSecurityContext.  If set in both SecurityContext and PodSecurityContext, the value specified in SecurityContext takes precedence. Note that this field cannot be set when spec.os.name is windows. |
| | || **Key**         | PerconaPGCluster.spec.pmm.containerSecurityContext.seLinuxOptions |
| **Value**       | object |
| **Required**    | false |
| **Example**     | |
| **Description** | The SELinux context to be applied to the container. If unspecified, the container runtime will allocate a random SELinux context for each container.  May also be set in PodSecurityContext.  If set in both SecurityContext and PodSecurityContext, the value specified in SecurityContext takes precedence. Note that this field cannot be set when spec.os.name is windows. |
| | || **Key**         | PerconaPGCluster.spec.pmm.containerSecurityContext.seccompProfile |
| **Value**       | object |
| **Required**    | false |
| **Example**     | |
| **Description** | The seccomp options to use by this container. If seccomp options are provided at both the pod & container level, the container options override the pod options. Note that this field cannot be set when spec.os.name is windows. |
| | || **Key**         | PerconaPGCluster.spec.pmm.containerSecurityContext.windowsOptions |
| **Value**       | object |
| **Required**    | false |
| **Example**     | |
| **Description** | The Windows specific settings applied to all containers. If unspecified, the options from the PodSecurityContext will be used. If set in both SecurityContext and PodSecurityContext, the value specified in SecurityContext takes precedence. Note that this field cannot be set when spec.os.name is linux. |
| | |
| **Key**         | PerconaPGCluster.spec.pmm.containerSecurityContext.capabilities.add |
| **Value**       | []string |
| **Required**    | false |
| **Example**     | |
| **Description** | Added capabilities |
| | || **Key**         | PerconaPGCluster.spec.pmm.containerSecurityContext.capabilities.drop |
| **Value**       | []string |
| **Required**    | false |
| **Example**     | |
| **Description** | Removed capabilities |
| | |
| **Key**         | PerconaPGCluster.spec.pmm.containerSecurityContext.seLinuxOptions.level |
| **Value**       | string |
| **Required**    | false |
| **Example**     | |
| **Description** | Level is SELinux level label that applies to the container. |
| | || **Key**         | PerconaPGCluster.spec.pmm.containerSecurityContext.seLinuxOptions.role |
| **Value**       | string |
| **Required**    | false |
| **Example**     | |
| **Description** | Role is a SELinux role label that applies to the container. |
| | || **Key**         | PerconaPGCluster.spec.pmm.containerSecurityContext.seLinuxOptions.type |
| **Value**       | string |
| **Required**    | false |
| **Example**     | |
| **Description** | Type is a SELinux type label that applies to the container. |
| | || **Key**         | PerconaPGCluster.spec.pmm.containerSecurityContext.seLinuxOptions.user |
| **Value**       | string |
| **Required**    | false |
| **Example**     | |
| **Description** | User is a SELinux user label that applies to the container. |
| | |
| **Key**         | PerconaPGCluster.spec.pmm.containerSecurityContext.seccompProfile.type |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | type indicates which kind of seccomp profile will be applied. Valid options are: 
 Localhost - a profile defined in a file on the node should be used. RuntimeDefault - the container runtime default profile should be used. Unconfined - no profile should be applied. |
| | || **Key**         | PerconaPGCluster.spec.pmm.containerSecurityContext.seccompProfile.localhostProfile |
| **Value**       | string |
| **Required**    | false |
| **Example**     | |
| **Description** | localhostProfile indicates a profile defined in a file on the node should be used. The profile must be preconfigured on the node to work. Must be a descending path, relative to the kubelet's configured seccomp profile location. Must only be set if type is "Localhost". |
| | |
| **Key**         | PerconaPGCluster.spec.pmm.containerSecurityContext.windowsOptions.gmsaCredentialSpec |
| **Value**       | string |
| **Required**    | false |
| **Example**     | |
| **Description** | GMSACredentialSpec is where the GMSA admission webhook (https://github.com/kubernetes-sigs/windows-gmsa) inlines the contents of the GMSA credential spec named by the GMSACredentialSpecName field. |
| | || **Key**         | PerconaPGCluster.spec.pmm.containerSecurityContext.windowsOptions.gmsaCredentialSpecName |
| **Value**       | string |
| **Required**    | false |
| **Example**     | |
| **Description** | GMSACredentialSpecName is the name of the GMSA credential spec to use. |
| | || **Key**         | PerconaPGCluster.spec.pmm.containerSecurityContext.windowsOptions.hostProcess |
| **Value**       | boolean |
| **Required**    | false |
| **Example**     | |
| **Description** | HostProcess determines if a container should be run as a 'Host Process' container. This field is alpha-level and will only be honored by components that enable the WindowsHostProcessContainers feature flag. Setting this field without the feature flag will result in errors when validating the Pod. All of a Pod's containers must have the same effective HostProcess value (it is not allowed to have a mix of HostProcess containers and non-HostProcess containers).  In addition, if HostProcess is true then HostNetwork must also be set to true. |
| | || **Key**         | PerconaPGCluster.spec.pmm.containerSecurityContext.windowsOptions.runAsUserName |
| **Value**       | string |
| **Required**    | false |
| **Example**     | |
| **Description** | The UserName in Windows to run the entrypoint of the container process. Defaults to the user specified in image metadata if unspecified. May also be set in PodSecurityContext. If set in both SecurityContext and PodSecurityContext, the value specified in SecurityContext takes precedence. |
| | |
| **Key**         | PerconaPGCluster.spec.pmm.resources.limits |
| **Value**       | map[string]int or string |
| **Required**    | false |
| **Example**     | |
| **Description** | Limits describes the maximum amount of compute resources allowed. More info: https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/ |
| | || **Key**         | PerconaPGCluster.spec.pmm.resources.requests |
| **Value**       | map[string]int or string |
| **Required**    | false |
| **Example**     | |
| **Description** | Requests describes the minimum amount of compute resources required. If Requests is omitted for a container, it defaults to Limits if that is explicitly specified, otherwise to an implementation-defined value. More info: https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/ |
| | |
| **Key**         | PerconaPGCluster.spec.proxy.pgBouncer |
| **Value**       | object |
| **Required**    | true |
| **Example**     | |
| **Description** | Defines a PgBouncer proxy and connection pooler. |
| | |
| **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.affinity |
| **Value**       | object |
| **Required**    | false |
| **Example**     | |
| **Description** | Scheduling constraints of a PgBouncer pod. Changing this value causes PgBouncer to restart. More info: https://kubernetes.io/docs/concepts/scheduling-eviction/assign-pod-node |
| | || **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.config |
| **Value**       | object |
| **Required**    | false |
| **Example**     | |
| **Description** | Configuration settings for the PgBouncer process. Changes to any of these values will be automatically reloaded without validation. Be careful, as you may put PgBouncer into an unusable state. More info: https://www.pgbouncer.org/usage.html#reload |
| | || **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.customTLSSecret |
| **Value**       | object |
| **Required**    | false |
| **Example**     | |
| **Description** | A secret projection containing a certificate and key with which to encrypt connections to PgBouncer. The "tls.crt", "tls.key", and "ca.crt" paths must be PEM-encoded certificates and keys. Changing this value causes PgBouncer to restart. More info: https://kubernetes.io/docs/concepts/configuration/secret/#projection-of-secret-keys-to-specific-paths |
| | || **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.expose |
| **Value**       | object |
| **Required**    | false |
| **Example**     | |
| **Description** | Specification of the service that exposes PgBouncer. |
| | || **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.image |
| **Value**       | string |
| **Required**    | false |
| **Example**     | |
| **Description** | Name of a container image that can run PgBouncer 1.15 or newer. Changing this value causes PgBouncer to restart. The image may also be set using the RELATED_IMAGE_PGBOUNCER environment variable. More info: https://kubernetes.io/docs/concepts/containers/images |
| | || **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.metadata |
| **Value**       | object |
| **Required**    | false |
| **Example**     | |
| **Description** | Metadata contains metadata for PostgresCluster resources |
| | || **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.minAvailable |
| **Value**       | int or string |
| **Required**    | false |
| **Example**     | |
| **Description** | Minimum number of pods that should be available at a time. Defaults to one when the replicas field is greater than one. |
| | || **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.port |
| **Value**       | integer |
| **Required**    | false |
| **Example**     | |
| **Description** | Port on which PgBouncer should listen for client connections. Changing this value causes PgBouncer to restart. |
| | || **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.priorityClassName |
| **Value**       | string |
| **Required**    | false |
| **Example**     | |
| **Description** | Priority class name for the pgBouncer pod. Changing this value causes PostgreSQL to restart. More info: https://kubernetes.io/docs/concepts/scheduling-eviction/pod-priority-preemption/ |
| | || **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.replicas |
| **Value**       | integer |
| **Required**    | false |
| **Example**     | |
| **Description** | Number of desired PgBouncer pods. |
| | || **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.resources |
| **Value**       | object |
| **Required**    | false |
| **Example**     | |
| **Description** | Compute resources of a PgBouncer container. Changing this value causes PgBouncer to restart. More info: https://kubernetes.io/docs/concepts/configuration/manage-resources-containers |
| | || **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.sidecars |
| **Value**       | []object |
| **Required**    | false |
| **Example**     | |
| **Description** | Custom sidecars for a PgBouncer pod. Changing this value causes PgBouncer to restart. |
| | || **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.tolerations |
| **Value**       | []object |
| **Required**    | false |
| **Example**     | |
| **Description** | Tolerations of a PgBouncer pod. Changing this value causes PgBouncer to restart. More info: https://kubernetes.io/docs/concepts/scheduling-eviction/taint-and-toleration |
| | || **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.topologySpreadConstraints |
| **Value**       | []object |
| **Required**    | false |
| **Example**     | |
| **Description** | Topology spread constraints of a PgBouncer pod. Changing this value causes PgBouncer to restart. More info: https://kubernetes.io/docs/concepts/workloads/pods/pod-topology-spread-constraints/ |
| | |
| **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.affinity.nodeAffinity |
| **Value**       | object |
| **Required**    | false |
| **Example**     | |
| **Description** | Describes node affinity scheduling rules for the pod. |
| | || **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.affinity.podAffinity |
| **Value**       | object |
| **Required**    | false |
| **Example**     | |
| **Description** | Describes pod affinity scheduling rules (e.g. co-locate this pod in the same node, zone, etc. as some other pod(s)). |
| | || **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.affinity.podAntiAffinity |
| **Value**       | object |
| **Required**    | false |
| **Example**     | |
| **Description** | Describes pod anti-affinity scheduling rules (e.g. avoid putting this pod in the same node, zone, etc. as some other pod(s)). |
| | |
| **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.affinity.nodeAffinity.preferredDuringSchedulingIgnoredDuringExecution |
| **Value**       | []object |
| **Required**    | false |
| **Example**     | |
| **Description** | The scheduler will prefer to schedule pods to nodes that satisfy the affinity expressions specified by this field, but it may choose a node that violates one or more of the expressions. The node that is most preferred is the one with the greatest sum of weights, i.e. for each node that meets all of the scheduling requirements (resource request, requiredDuringScheduling affinity expressions, etc.), compute a sum by iterating through the elements of this field and adding "weight" to the sum if the node matches the corresponding matchExpressions; the node(s) with the highest sum are the most preferred. |
| | || **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.affinity.nodeAffinity.requiredDuringSchedulingIgnoredDuringExecution |
| **Value**       | object |
| **Required**    | false |
| **Example**     | |
| **Description** | If the affinity requirements specified by this field are not met at scheduling time, the pod will not be scheduled onto the node. If the affinity requirements specified by this field cease to be met at some point during pod execution (e.g. due to an update), the system may or may not try to eventually evict the pod from its node. |
| | |
| **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.affinity.nodeAffinity.preferredDuringSchedulingIgnoredDuringExecution[index].preference |
| **Value**       | object |
| **Required**    | true |
| **Example**     | |
| **Description** | A node selector term, associated with the corresponding weight. |
| | || **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.affinity.nodeAffinity.preferredDuringSchedulingIgnoredDuringExecution[index].weight |
| **Value**       | integer |
| **Required**    | true |
| **Example**     | |
| **Description** | Weight associated with matching the corresponding nodeSelectorTerm, in the range 1-100. |
| | |
| **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.affinity.nodeAffinity.preferredDuringSchedulingIgnoredDuringExecution[index].preference.matchExpressions |
| **Value**       | []object |
| **Required**    | false |
| **Example**     | |
| **Description** | A list of node selector requirements by node's labels. |
| | || **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.affinity.nodeAffinity.preferredDuringSchedulingIgnoredDuringExecution[index].preference.matchFields |
| **Value**       | []object |
| **Required**    | false |
| **Example**     | |
| **Description** | A list of node selector requirements by node's fields. |
| | |
| **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.affinity.nodeAffinity.preferredDuringSchedulingIgnoredDuringExecution[index].preference.matchExpressions[index].key |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | The label key that the selector applies to. |
| | || **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.affinity.nodeAffinity.preferredDuringSchedulingIgnoredDuringExecution[index].preference.matchExpressions[index].operator |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | Represents a key's relationship to a set of values. Valid operators are In, NotIn, Exists, DoesNotExist. Gt, and Lt. |
| | || **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.affinity.nodeAffinity.preferredDuringSchedulingIgnoredDuringExecution[index].preference.matchExpressions[index].values |
| **Value**       | []string |
| **Required**    | false |
| **Example**     | |
| **Description** | An array of string values. If the operator is In or NotIn, the values array must be non-empty. If the operator is Exists or DoesNotExist, the values array must be empty. If the operator is Gt or Lt, the values array must have a single element, which will be interpreted as an integer. This array is replaced during a strategic merge patch. |
| | |
| **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.affinity.nodeAffinity.preferredDuringSchedulingIgnoredDuringExecution[index].preference.matchFields[index].key |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | The label key that the selector applies to. |
| | || **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.affinity.nodeAffinity.preferredDuringSchedulingIgnoredDuringExecution[index].preference.matchFields[index].operator |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | Represents a key's relationship to a set of values. Valid operators are In, NotIn, Exists, DoesNotExist. Gt, and Lt. |
| | || **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.affinity.nodeAffinity.preferredDuringSchedulingIgnoredDuringExecution[index].preference.matchFields[index].values |
| **Value**       | []string |
| **Required**    | false |
| **Example**     | |
| **Description** | An array of string values. If the operator is In or NotIn, the values array must be non-empty. If the operator is Exists or DoesNotExist, the values array must be empty. If the operator is Gt or Lt, the values array must have a single element, which will be interpreted as an integer. This array is replaced during a strategic merge patch. |
| | |
| **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.affinity.nodeAffinity.requiredDuringSchedulingIgnoredDuringExecution.nodeSelectorTerms |
| **Value**       | []object |
| **Required**    | true |
| **Example**     | |
| **Description** | Required. A list of node selector terms. The terms are ORed. |
| | |
| **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.affinity.nodeAffinity.requiredDuringSchedulingIgnoredDuringExecution.nodeSelectorTerms[index].matchExpressions |
| **Value**       | []object |
| **Required**    | false |
| **Example**     | |
| **Description** | A list of node selector requirements by node's labels. |
| | || **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.affinity.nodeAffinity.requiredDuringSchedulingIgnoredDuringExecution.nodeSelectorTerms[index].matchFields |
| **Value**       | []object |
| **Required**    | false |
| **Example**     | |
| **Description** | A list of node selector requirements by node's fields. |
| | |
| **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.affinity.nodeAffinity.requiredDuringSchedulingIgnoredDuringExecution.nodeSelectorTerms[index].matchExpressions[index].key |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | The label key that the selector applies to. |
| | || **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.affinity.nodeAffinity.requiredDuringSchedulingIgnoredDuringExecution.nodeSelectorTerms[index].matchExpressions[index].operator |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | Represents a key's relationship to a set of values. Valid operators are In, NotIn, Exists, DoesNotExist. Gt, and Lt. |
| | || **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.affinity.nodeAffinity.requiredDuringSchedulingIgnoredDuringExecution.nodeSelectorTerms[index].matchExpressions[index].values |
| **Value**       | []string |
| **Required**    | false |
| **Example**     | |
| **Description** | An array of string values. If the operator is In or NotIn, the values array must be non-empty. If the operator is Exists or DoesNotExist, the values array must be empty. If the operator is Gt or Lt, the values array must have a single element, which will be interpreted as an integer. This array is replaced during a strategic merge patch. |
| | |
| **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.affinity.nodeAffinity.requiredDuringSchedulingIgnoredDuringExecution.nodeSelectorTerms[index].matchFields[index].key |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | The label key that the selector applies to. |
| | || **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.affinity.nodeAffinity.requiredDuringSchedulingIgnoredDuringExecution.nodeSelectorTerms[index].matchFields[index].operator |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | Represents a key's relationship to a set of values. Valid operators are In, NotIn, Exists, DoesNotExist. Gt, and Lt. |
| | || **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.affinity.nodeAffinity.requiredDuringSchedulingIgnoredDuringExecution.nodeSelectorTerms[index].matchFields[index].values |
| **Value**       | []string |
| **Required**    | false |
| **Example**     | |
| **Description** | An array of string values. If the operator is In or NotIn, the values array must be non-empty. If the operator is Exists or DoesNotExist, the values array must be empty. If the operator is Gt or Lt, the values array must have a single element, which will be interpreted as an integer. This array is replaced during a strategic merge patch. |
| | |
| **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.affinity.podAffinity.preferredDuringSchedulingIgnoredDuringExecution |
| **Value**       | []object |
| **Required**    | false |
| **Example**     | |
| **Description** | The scheduler will prefer to schedule pods to nodes that satisfy the affinity expressions specified by this field, but it may choose a node that violates one or more of the expressions. The node that is most preferred is the one with the greatest sum of weights, i.e. for each node that meets all of the scheduling requirements (resource request, requiredDuringScheduling affinity expressions, etc.), compute a sum by iterating through the elements of this field and adding "weight" to the sum if the node has pods which matches the corresponding podAffinityTerm; the node(s) with the highest sum are the most preferred. |
| | || **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.affinity.podAffinity.requiredDuringSchedulingIgnoredDuringExecution |
| **Value**       | []object |
| **Required**    | false |
| **Example**     | |
| **Description** | If the affinity requirements specified by this field are not met at scheduling time, the pod will not be scheduled onto the node. If the affinity requirements specified by this field cease to be met at some point during pod execution (e.g. due to a pod label update), the system may or may not try to eventually evict the pod from its node. When there are multiple elements, the lists of nodes corresponding to each podAffinityTerm are intersected, i.e. all terms must be satisfied. |
| | |
| **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.affinity.podAffinity.preferredDuringSchedulingIgnoredDuringExecution[index].podAffinityTerm |
| **Value**       | object |
| **Required**    | true |
| **Example**     | |
| **Description** | Required. A pod affinity term, associated with the corresponding weight. |
| | || **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.affinity.podAffinity.preferredDuringSchedulingIgnoredDuringExecution[index].weight |
| **Value**       | integer |
| **Required**    | true |
| **Example**     | |
| **Description** | weight associated with matching the corresponding podAffinityTerm, in the range 1-100. |
| | |
| **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.affinity.podAffinity.preferredDuringSchedulingIgnoredDuringExecution[index].podAffinityTerm.topologyKey |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | This pod should be co-located (affinity) or not co-located (anti-affinity) with the pods matching the labelSelector in the specified namespaces, where co-located is defined as running on a node whose value of the label with key topologyKey matches that of any node on which any of the selected pods is running. Empty topologyKey is not allowed. |
| | || **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.affinity.podAffinity.preferredDuringSchedulingIgnoredDuringExecution[index].podAffinityTerm.labelSelector |
| **Value**       | object |
| **Required**    | false |
| **Example**     | |
| **Description** | A label query over a set of resources, in this case pods. |
| | || **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.affinity.podAffinity.preferredDuringSchedulingIgnoredDuringExecution[index].podAffinityTerm.namespaceSelector |
| **Value**       | object |
| **Required**    | false |
| **Example**     | |
| **Description** | A label query over the set of namespaces that the term applies to. The term is applied to the union of the namespaces selected by this field and the ones listed in the namespaces field. null selector and null or empty namespaces list means "this pod's namespace". An empty selector ({}) matches all namespaces. |
| | || **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.affinity.podAffinity.preferredDuringSchedulingIgnoredDuringExecution[index].podAffinityTerm.namespaces |
| **Value**       | []string |
| **Required**    | false |
| **Example**     | |
| **Description** | namespaces specifies a static list of namespace names that the term applies to. The term is applied to the union of the namespaces listed in this field and the ones selected by namespaceSelector. null or empty namespaces list and null namespaceSelector means "this pod's namespace". |
| | |
| **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.affinity.podAffinity.preferredDuringSchedulingIgnoredDuringExecution[index].podAffinityTerm.labelSelector.matchExpressions |
| **Value**       | []object |
| **Required**    | false |
| **Example**     | |
| **Description** | matchExpressions is a list of label selector requirements. The requirements are ANDed. |
| | || **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.affinity.podAffinity.preferredDuringSchedulingIgnoredDuringExecution[index].podAffinityTerm.labelSelector.matchLabels |
| **Value**       | map[string]string |
| **Required**    | false |
| **Example**     | |
| **Description** | matchLabels is a map of {key,value} pairs. A single {key,value} in the matchLabels map is equivalent to an element of matchExpressions, whose key field is "key", the operator is "In", and the values array contains only "value". The requirements are ANDed. |
| | |
| **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.affinity.podAffinity.preferredDuringSchedulingIgnoredDuringExecution[index].podAffinityTerm.labelSelector.matchExpressions[index].key |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | key is the label key that the selector applies to. |
| | || **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.affinity.podAffinity.preferredDuringSchedulingIgnoredDuringExecution[index].podAffinityTerm.labelSelector.matchExpressions[index].operator |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | operator represents a key's relationship to a set of values. Valid operators are In, NotIn, Exists and DoesNotExist. |
| | || **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.affinity.podAffinity.preferredDuringSchedulingIgnoredDuringExecution[index].podAffinityTerm.labelSelector.matchExpressions[index].values |
| **Value**       | []string |
| **Required**    | false |
| **Example**     | |
| **Description** | values is an array of string values. If the operator is In or NotIn, the values array must be non-empty. If the operator is Exists or DoesNotExist, the values array must be empty. This array is replaced during a strategic merge patch. |
| | |
| **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.affinity.podAffinity.preferredDuringSchedulingIgnoredDuringExecution[index].podAffinityTerm.namespaceSelector.matchExpressions |
| **Value**       | []object |
| **Required**    | false |
| **Example**     | |
| **Description** | matchExpressions is a list of label selector requirements. The requirements are ANDed. |
| | || **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.affinity.podAffinity.preferredDuringSchedulingIgnoredDuringExecution[index].podAffinityTerm.namespaceSelector.matchLabels |
| **Value**       | map[string]string |
| **Required**    | false |
| **Example**     | |
| **Description** | matchLabels is a map of {key,value} pairs. A single {key,value} in the matchLabels map is equivalent to an element of matchExpressions, whose key field is "key", the operator is "In", and the values array contains only "value". The requirements are ANDed. |
| | |
| **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.affinity.podAffinity.preferredDuringSchedulingIgnoredDuringExecution[index].podAffinityTerm.namespaceSelector.matchExpressions[index].key |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | key is the label key that the selector applies to. |
| | || **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.affinity.podAffinity.preferredDuringSchedulingIgnoredDuringExecution[index].podAffinityTerm.namespaceSelector.matchExpressions[index].operator |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | operator represents a key's relationship to a set of values. Valid operators are In, NotIn, Exists and DoesNotExist. |
| | || **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.affinity.podAffinity.preferredDuringSchedulingIgnoredDuringExecution[index].podAffinityTerm.namespaceSelector.matchExpressions[index].values |
| **Value**       | []string |
| **Required**    | false |
| **Example**     | |
| **Description** | values is an array of string values. If the operator is In or NotIn, the values array must be non-empty. If the operator is Exists or DoesNotExist, the values array must be empty. This array is replaced during a strategic merge patch. |
| | |
| **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.affinity.podAffinity.requiredDuringSchedulingIgnoredDuringExecution[index].topologyKey |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | This pod should be co-located (affinity) or not co-located (anti-affinity) with the pods matching the labelSelector in the specified namespaces, where co-located is defined as running on a node whose value of the label with key topologyKey matches that of any node on which any of the selected pods is running. Empty topologyKey is not allowed. |
| | || **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.affinity.podAffinity.requiredDuringSchedulingIgnoredDuringExecution[index].labelSelector |
| **Value**       | object |
| **Required**    | false |
| **Example**     | |
| **Description** | A label query over a set of resources, in this case pods. |
| | || **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.affinity.podAffinity.requiredDuringSchedulingIgnoredDuringExecution[index].namespaceSelector |
| **Value**       | object |
| **Required**    | false |
| **Example**     | |
| **Description** | A label query over the set of namespaces that the term applies to. The term is applied to the union of the namespaces selected by this field and the ones listed in the namespaces field. null selector and null or empty namespaces list means "this pod's namespace". An empty selector ({}) matches all namespaces. |
| | || **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.affinity.podAffinity.requiredDuringSchedulingIgnoredDuringExecution[index].namespaces |
| **Value**       | []string |
| **Required**    | false |
| **Example**     | |
| **Description** | namespaces specifies a static list of namespace names that the term applies to. The term is applied to the union of the namespaces listed in this field and the ones selected by namespaceSelector. null or empty namespaces list and null namespaceSelector means "this pod's namespace". |
| | |
| **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.affinity.podAffinity.requiredDuringSchedulingIgnoredDuringExecution[index].labelSelector.matchExpressions |
| **Value**       | []object |
| **Required**    | false |
| **Example**     | |
| **Description** | matchExpressions is a list of label selector requirements. The requirements are ANDed. |
| | || **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.affinity.podAffinity.requiredDuringSchedulingIgnoredDuringExecution[index].labelSelector.matchLabels |
| **Value**       | map[string]string |
| **Required**    | false |
| **Example**     | |
| **Description** | matchLabels is a map of {key,value} pairs. A single {key,value} in the matchLabels map is equivalent to an element of matchExpressions, whose key field is "key", the operator is "In", and the values array contains only "value". The requirements are ANDed. |
| | |
| **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.affinity.podAffinity.requiredDuringSchedulingIgnoredDuringExecution[index].labelSelector.matchExpressions[index].key |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | key is the label key that the selector applies to. |
| | || **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.affinity.podAffinity.requiredDuringSchedulingIgnoredDuringExecution[index].labelSelector.matchExpressions[index].operator |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | operator represents a key's relationship to a set of values. Valid operators are In, NotIn, Exists and DoesNotExist. |
| | || **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.affinity.podAffinity.requiredDuringSchedulingIgnoredDuringExecution[index].labelSelector.matchExpressions[index].values |
| **Value**       | []string |
| **Required**    | false |
| **Example**     | |
| **Description** | values is an array of string values. If the operator is In or NotIn, the values array must be non-empty. If the operator is Exists or DoesNotExist, the values array must be empty. This array is replaced during a strategic merge patch. |
| | |
| **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.affinity.podAffinity.requiredDuringSchedulingIgnoredDuringExecution[index].namespaceSelector.matchExpressions |
| **Value**       | []object |
| **Required**    | false |
| **Example**     | |
| **Description** | matchExpressions is a list of label selector requirements. The requirements are ANDed. |
| | || **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.affinity.podAffinity.requiredDuringSchedulingIgnoredDuringExecution[index].namespaceSelector.matchLabels |
| **Value**       | map[string]string |
| **Required**    | false |
| **Example**     | |
| **Description** | matchLabels is a map of {key,value} pairs. A single {key,value} in the matchLabels map is equivalent to an element of matchExpressions, whose key field is "key", the operator is "In", and the values array contains only "value". The requirements are ANDed. |
| | |
| **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.affinity.podAffinity.requiredDuringSchedulingIgnoredDuringExecution[index].namespaceSelector.matchExpressions[index].key |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | key is the label key that the selector applies to. |
| | || **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.affinity.podAffinity.requiredDuringSchedulingIgnoredDuringExecution[index].namespaceSelector.matchExpressions[index].operator |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | operator represents a key's relationship to a set of values. Valid operators are In, NotIn, Exists and DoesNotExist. |
| | || **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.affinity.podAffinity.requiredDuringSchedulingIgnoredDuringExecution[index].namespaceSelector.matchExpressions[index].values |
| **Value**       | []string |
| **Required**    | false |
| **Example**     | |
| **Description** | values is an array of string values. If the operator is In or NotIn, the values array must be non-empty. If the operator is Exists or DoesNotExist, the values array must be empty. This array is replaced during a strategic merge patch. |
| | |
| **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.affinity.podAntiAffinity.preferredDuringSchedulingIgnoredDuringExecution |
| **Value**       | []object |
| **Required**    | false |
| **Example**     | |
| **Description** | The scheduler will prefer to schedule pods to nodes that satisfy the anti-affinity expressions specified by this field, but it may choose a node that violates one or more of the expressions. The node that is most preferred is the one with the greatest sum of weights, i.e. for each node that meets all of the scheduling requirements (resource request, requiredDuringScheduling anti-affinity expressions, etc.), compute a sum by iterating through the elements of this field and adding "weight" to the sum if the node has pods which matches the corresponding podAffinityTerm; the node(s) with the highest sum are the most preferred. |
| | || **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.affinity.podAntiAffinity.requiredDuringSchedulingIgnoredDuringExecution |
| **Value**       | []object |
| **Required**    | false |
| **Example**     | |
| **Description** | If the anti-affinity requirements specified by this field are not met at scheduling time, the pod will not be scheduled onto the node. If the anti-affinity requirements specified by this field cease to be met at some point during pod execution (e.g. due to a pod label update), the system may or may not try to eventually evict the pod from its node. When there are multiple elements, the lists of nodes corresponding to each podAffinityTerm are intersected, i.e. all terms must be satisfied. |
| | |
| **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.affinity.podAntiAffinity.preferredDuringSchedulingIgnoredDuringExecution[index].podAffinityTerm |
| **Value**       | object |
| **Required**    | true |
| **Example**     | |
| **Description** | Required. A pod affinity term, associated with the corresponding weight. |
| | || **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.affinity.podAntiAffinity.preferredDuringSchedulingIgnoredDuringExecution[index].weight |
| **Value**       | integer |
| **Required**    | true |
| **Example**     | |
| **Description** | weight associated with matching the corresponding podAffinityTerm, in the range 1-100. |
| | |
| **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.affinity.podAntiAffinity.preferredDuringSchedulingIgnoredDuringExecution[index].podAffinityTerm.topologyKey |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | This pod should be co-located (affinity) or not co-located (anti-affinity) with the pods matching the labelSelector in the specified namespaces, where co-located is defined as running on a node whose value of the label with key topologyKey matches that of any node on which any of the selected pods is running. Empty topologyKey is not allowed. |
| | || **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.affinity.podAntiAffinity.preferredDuringSchedulingIgnoredDuringExecution[index].podAffinityTerm.labelSelector |
| **Value**       | object |
| **Required**    | false |
| **Example**     | |
| **Description** | A label query over a set of resources, in this case pods. |
| | || **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.affinity.podAntiAffinity.preferredDuringSchedulingIgnoredDuringExecution[index].podAffinityTerm.namespaceSelector |
| **Value**       | object |
| **Required**    | false |
| **Example**     | |
| **Description** | A label query over the set of namespaces that the term applies to. The term is applied to the union of the namespaces selected by this field and the ones listed in the namespaces field. null selector and null or empty namespaces list means "this pod's namespace". An empty selector ({}) matches all namespaces. |
| | || **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.affinity.podAntiAffinity.preferredDuringSchedulingIgnoredDuringExecution[index].podAffinityTerm.namespaces |
| **Value**       | []string |
| **Required**    | false |
| **Example**     | |
| **Description** | namespaces specifies a static list of namespace names that the term applies to. The term is applied to the union of the namespaces listed in this field and the ones selected by namespaceSelector. null or empty namespaces list and null namespaceSelector means "this pod's namespace". |
| | |
| **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.affinity.podAntiAffinity.preferredDuringSchedulingIgnoredDuringExecution[index].podAffinityTerm.labelSelector.matchExpressions |
| **Value**       | []object |
| **Required**    | false |
| **Example**     | |
| **Description** | matchExpressions is a list of label selector requirements. The requirements are ANDed. |
| | || **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.affinity.podAntiAffinity.preferredDuringSchedulingIgnoredDuringExecution[index].podAffinityTerm.labelSelector.matchLabels |
| **Value**       | map[string]string |
| **Required**    | false |
| **Example**     | |
| **Description** | matchLabels is a map of {key,value} pairs. A single {key,value} in the matchLabels map is equivalent to an element of matchExpressions, whose key field is "key", the operator is "In", and the values array contains only "value". The requirements are ANDed. |
| | |
| **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.affinity.podAntiAffinity.preferredDuringSchedulingIgnoredDuringExecution[index].podAffinityTerm.labelSelector.matchExpressions[index].key |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | key is the label key that the selector applies to. |
| | || **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.affinity.podAntiAffinity.preferredDuringSchedulingIgnoredDuringExecution[index].podAffinityTerm.labelSelector.matchExpressions[index].operator |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | operator represents a key's relationship to a set of values. Valid operators are In, NotIn, Exists and DoesNotExist. |
| | || **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.affinity.podAntiAffinity.preferredDuringSchedulingIgnoredDuringExecution[index].podAffinityTerm.labelSelector.matchExpressions[index].values |
| **Value**       | []string |
| **Required**    | false |
| **Example**     | |
| **Description** | values is an array of string values. If the operator is In or NotIn, the values array must be non-empty. If the operator is Exists or DoesNotExist, the values array must be empty. This array is replaced during a strategic merge patch. |
| | |
| **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.affinity.podAntiAffinity.preferredDuringSchedulingIgnoredDuringExecution[index].podAffinityTerm.namespaceSelector.matchExpressions |
| **Value**       | []object |
| **Required**    | false |
| **Example**     | |
| **Description** | matchExpressions is a list of label selector requirements. The requirements are ANDed. |
| | || **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.affinity.podAntiAffinity.preferredDuringSchedulingIgnoredDuringExecution[index].podAffinityTerm.namespaceSelector.matchLabels |
| **Value**       | map[string]string |
| **Required**    | false |
| **Example**     | |
| **Description** | matchLabels is a map of {key,value} pairs. A single {key,value} in the matchLabels map is equivalent to an element of matchExpressions, whose key field is "key", the operator is "In", and the values array contains only "value". The requirements are ANDed. |
| | |
| **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.affinity.podAntiAffinity.preferredDuringSchedulingIgnoredDuringExecution[index].podAffinityTerm.namespaceSelector.matchExpressions[index].key |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | key is the label key that the selector applies to. |
| | || **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.affinity.podAntiAffinity.preferredDuringSchedulingIgnoredDuringExecution[index].podAffinityTerm.namespaceSelector.matchExpressions[index].operator |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | operator represents a key's relationship to a set of values. Valid operators are In, NotIn, Exists and DoesNotExist. |
| | || **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.affinity.podAntiAffinity.preferredDuringSchedulingIgnoredDuringExecution[index].podAffinityTerm.namespaceSelector.matchExpressions[index].values |
| **Value**       | []string |
| **Required**    | false |
| **Example**     | |
| **Description** | values is an array of string values. If the operator is In or NotIn, the values array must be non-empty. If the operator is Exists or DoesNotExist, the values array must be empty. This array is replaced during a strategic merge patch. |
| | |
| **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.affinity.podAntiAffinity.requiredDuringSchedulingIgnoredDuringExecution[index].topologyKey |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | This pod should be co-located (affinity) or not co-located (anti-affinity) with the pods matching the labelSelector in the specified namespaces, where co-located is defined as running on a node whose value of the label with key topologyKey matches that of any node on which any of the selected pods is running. Empty topologyKey is not allowed. |
| | || **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.affinity.podAntiAffinity.requiredDuringSchedulingIgnoredDuringExecution[index].labelSelector |
| **Value**       | object |
| **Required**    | false |
| **Example**     | |
| **Description** | A label query over a set of resources, in this case pods. |
| | || **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.affinity.podAntiAffinity.requiredDuringSchedulingIgnoredDuringExecution[index].namespaceSelector |
| **Value**       | object |
| **Required**    | false |
| **Example**     | |
| **Description** | A label query over the set of namespaces that the term applies to. The term is applied to the union of the namespaces selected by this field and the ones listed in the namespaces field. null selector and null or empty namespaces list means "this pod's namespace". An empty selector ({}) matches all namespaces. |
| | || **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.affinity.podAntiAffinity.requiredDuringSchedulingIgnoredDuringExecution[index].namespaces |
| **Value**       | []string |
| **Required**    | false |
| **Example**     | |
| **Description** | namespaces specifies a static list of namespace names that the term applies to. The term is applied to the union of the namespaces listed in this field and the ones selected by namespaceSelector. null or empty namespaces list and null namespaceSelector means "this pod's namespace". |
| | |
| **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.affinity.podAntiAffinity.requiredDuringSchedulingIgnoredDuringExecution[index].labelSelector.matchExpressions |
| **Value**       | []object |
| **Required**    | false |
| **Example**     | |
| **Description** | matchExpressions is a list of label selector requirements. The requirements are ANDed. |
| | || **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.affinity.podAntiAffinity.requiredDuringSchedulingIgnoredDuringExecution[index].labelSelector.matchLabels |
| **Value**       | map[string]string |
| **Required**    | false |
| **Example**     | |
| **Description** | matchLabels is a map of {key,value} pairs. A single {key,value} in the matchLabels map is equivalent to an element of matchExpressions, whose key field is "key", the operator is "In", and the values array contains only "value". The requirements are ANDed. |
| | |
| **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.affinity.podAntiAffinity.requiredDuringSchedulingIgnoredDuringExecution[index].labelSelector.matchExpressions[index].key |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | key is the label key that the selector applies to. |
| | || **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.affinity.podAntiAffinity.requiredDuringSchedulingIgnoredDuringExecution[index].labelSelector.matchExpressions[index].operator |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | operator represents a key's relationship to a set of values. Valid operators are In, NotIn, Exists and DoesNotExist. |
| | || **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.affinity.podAntiAffinity.requiredDuringSchedulingIgnoredDuringExecution[index].labelSelector.matchExpressions[index].values |
| **Value**       | []string |
| **Required**    | false |
| **Example**     | |
| **Description** | values is an array of string values. If the operator is In or NotIn, the values array must be non-empty. If the operator is Exists or DoesNotExist, the values array must be empty. This array is replaced during a strategic merge patch. |
| | |
| **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.affinity.podAntiAffinity.requiredDuringSchedulingIgnoredDuringExecution[index].namespaceSelector.matchExpressions |
| **Value**       | []object |
| **Required**    | false |
| **Example**     | |
| **Description** | matchExpressions is a list of label selector requirements. The requirements are ANDed. |
| | || **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.affinity.podAntiAffinity.requiredDuringSchedulingIgnoredDuringExecution[index].namespaceSelector.matchLabels |
| **Value**       | map[string]string |
| **Required**    | false |
| **Example**     | |
| **Description** | matchLabels is a map of {key,value} pairs. A single {key,value} in the matchLabels map is equivalent to an element of matchExpressions, whose key field is "key", the operator is "In", and the values array contains only "value". The requirements are ANDed. |
| | |
| **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.affinity.podAntiAffinity.requiredDuringSchedulingIgnoredDuringExecution[index].namespaceSelector.matchExpressions[index].key |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | key is the label key that the selector applies to. |
| | || **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.affinity.podAntiAffinity.requiredDuringSchedulingIgnoredDuringExecution[index].namespaceSelector.matchExpressions[index].operator |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | operator represents a key's relationship to a set of values. Valid operators are In, NotIn, Exists and DoesNotExist. |
| | || **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.affinity.podAntiAffinity.requiredDuringSchedulingIgnoredDuringExecution[index].namespaceSelector.matchExpressions[index].values |
| **Value**       | []string |
| **Required**    | false |
| **Example**     | |
| **Description** | values is an array of string values. If the operator is In or NotIn, the values array must be non-empty. If the operator is Exists or DoesNotExist, the values array must be empty. This array is replaced during a strategic merge patch. |
| | |
| **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.config.databases |
| **Value**       | map[string]string |
| **Required**    | false |
| **Example**     | |
| **Description** | PgBouncer database definitions. The key is the database requested by a client while the value is a libpq-styled connection string. The special key "*" acts as a fallback. When this field is empty, PgBouncer is configured with a single "*" entry that connects to the primary PostgreSQL instance. More info: https://www.pgbouncer.org/config.html#section-databases |
| | || **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.config.files |
| **Value**       | []object |
| **Required**    | false |
| **Example**     | |
| **Description** | Files to mount under "/etc/pgbouncer". When specified, settings in the "pgbouncer.ini" file are loaded before all others. From there, other files may be included by absolute path. Changing these references causes PgBouncer to restart, but changes to the file contents are automatically reloaded. More info: https://www.pgbouncer.org/config.html#include-directive |
| | || **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.config.global |
| **Value**       | map[string]string |
| **Required**    | false |
| **Example**     | |
| **Description** | Settings that apply to the entire PgBouncer process. More info: https://www.pgbouncer.org/config.html |
| | || **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.config.users |
| **Value**       | map[string]string |
| **Required**    | false |
| **Example**     | |
| **Description** | Connection settings specific to particular users. More info: https://www.pgbouncer.org/config.html#section-users |
| | |
| **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.config.files[index].configMap |
| **Value**       | object |
| **Required**    | false |
| **Example**     | |
| **Description** | configMap information about the configMap data to project |
| | || **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.config.files[index].downwardAPI |
| **Value**       | object |
| **Required**    | false |
| **Example**     | |
| **Description** | downwardAPI information about the downwardAPI data to project |
| | || **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.config.files[index].secret |
| **Value**       | object |
| **Required**    | false |
| **Example**     | |
| **Description** | secret information about the secret data to project |
| | || **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.config.files[index].serviceAccountToken |
| **Value**       | object |
| **Required**    | false |
| **Example**     | |
| **Description** | serviceAccountToken is information about the serviceAccountToken data to project |
| | |
| **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.config.files[index].configMap.items |
| **Value**       | []object |
| **Required**    | false |
| **Example**     | |
| **Description** | items if unspecified, each key-value pair in the Data field of the referenced ConfigMap will be projected into the volume as a file whose name is the key and content is the value. If specified, the listed keys will be projected into the specified paths, and unlisted keys will not be present. If a key is specified which is not present in the ConfigMap, the volume setup will error unless it is marked optional. Paths must be relative and may not contain the '..' path or start with '..'. |
| | || **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.config.files[index].configMap.name |
| **Value**       | string |
| **Required**    | false |
| **Example**     | |
| **Description** | Name of the referent. More info: https://kubernetes.io/docs/concepts/overview/working-with-objects/names/#names TODO: Add other useful fields. apiVersion, kind, uid? |
| | || **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.config.files[index].configMap.optional |
| **Value**       | boolean |
| **Required**    | false |
| **Example**     | |
| **Description** | optional specify whether the ConfigMap or its keys must be defined |
| | |
| **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.config.files[index].configMap.items[index].key |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | key is the key to project. |
| | || **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.config.files[index].configMap.items[index].path |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | path is the relative path of the file to map the key to. May not be an absolute path. May not contain the path element '..'. May not start with the string '..'. |
| | || **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.config.files[index].configMap.items[index].mode |
| **Value**       | integer |
| **Required**    | false |
| **Example**     | |
| **Description** | mode is Optional: mode bits used to set permissions on this file. Must be an octal value between 0000 and 0777 or a decimal value between 0 and 511. YAML accepts both octal and decimal values, JSON requires decimal values for mode bits. If not specified, the volume defaultMode will be used. This might be in conflict with other options that affect the file mode, like fsGroup, and the result can be other mode bits set. |
| | |
| **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.config.files[index].downwardAPI.items |
| **Value**       | []object |
| **Required**    | false |
| **Example**     | |
| **Description** | Items is a list of DownwardAPIVolume file |
| | |
| **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.config.files[index].downwardAPI.items[index].path |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | Required: Path is  the relative path name of the file to be created. Must not be absolute or contain the '..' path. Must be utf-8 encoded. The first item of the relative path must not start with '..' |
| | || **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.config.files[index].downwardAPI.items[index].fieldRef |
| **Value**       | object |
| **Required**    | false |
| **Example**     | |
| **Description** | Required: Selects a field of the pod: only annotations, labels, name and namespace are supported. |
| | || **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.config.files[index].downwardAPI.items[index].mode |
| **Value**       | integer |
| **Required**    | false |
| **Example**     | |
| **Description** | Optional: mode bits used to set permissions on this file, must be an octal value between 0000 and 0777 or a decimal value between 0 and 511. YAML accepts both octal and decimal values, JSON requires decimal values for mode bits. If not specified, the volume defaultMode will be used. This might be in conflict with other options that affect the file mode, like fsGroup, and the result can be other mode bits set. |
| | || **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.config.files[index].downwardAPI.items[index].resourceFieldRef |
| **Value**       | object |
| **Required**    | false |
| **Example**     | |
| **Description** | Selects a resource of the container: only resources limits and requests (limits.cpu, limits.memory, requests.cpu and requests.memory) are currently supported. |
| | |
| **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.config.files[index].downwardAPI.items[index].fieldRef.fieldPath |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | Path of the field to select in the specified API version. |
| | || **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.config.files[index].downwardAPI.items[index].fieldRef.apiVersion |
| **Value**       | string |
| **Required**    | false |
| **Example**     | |
| **Description** | Version of the schema the FieldPath is written in terms of, defaults to "v1". |
| | |
| **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.config.files[index].downwardAPI.items[index].resourceFieldRef.resource |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | Required: resource to select |
| | || **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.config.files[index].downwardAPI.items[index].resourceFieldRef.containerName |
| **Value**       | string |
| **Required**    | false |
| **Example**     | |
| **Description** | Container name: required for volumes, optional for env vars |
| | || **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.config.files[index].downwardAPI.items[index].resourceFieldRef.divisor |
| **Value**       | int or string |
| **Required**    | false |
| **Example**     | |
| **Description** | Specifies the output format of the exposed resources, defaults to "1" |
| | |
| **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.config.files[index].secret.items |
| **Value**       | []object |
| **Required**    | false |
| **Example**     | |
| **Description** | items if unspecified, each key-value pair in the Data field of the referenced Secret will be projected into the volume as a file whose name is the key and content is the value. If specified, the listed keys will be projected into the specified paths, and unlisted keys will not be present. If a key is specified which is not present in the Secret, the volume setup will error unless it is marked optional. Paths must be relative and may not contain the '..' path or start with '..'. |
| | || **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.config.files[index].secret.name |
| **Value**       | string |
| **Required**    | false |
| **Example**     | |
| **Description** | Name of the referent. More info: https://kubernetes.io/docs/concepts/overview/working-with-objects/names/#names TODO: Add other useful fields. apiVersion, kind, uid? |
| | || **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.config.files[index].secret.optional |
| **Value**       | boolean |
| **Required**    | false |
| **Example**     | |
| **Description** | optional field specify whether the Secret or its key must be defined |
| | |
| **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.config.files[index].secret.items[index].key |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | key is the key to project. |
| | || **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.config.files[index].secret.items[index].path |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | path is the relative path of the file to map the key to. May not be an absolute path. May not contain the path element '..'. May not start with the string '..'. |
| | || **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.config.files[index].secret.items[index].mode |
| **Value**       | integer |
| **Required**    | false |
| **Example**     | |
| **Description** | mode is Optional: mode bits used to set permissions on this file. Must be an octal value between 0000 and 0777 or a decimal value between 0 and 511. YAML accepts both octal and decimal values, JSON requires decimal values for mode bits. If not specified, the volume defaultMode will be used. This might be in conflict with other options that affect the file mode, like fsGroup, and the result can be other mode bits set. |
| | |
| **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.config.files[index].serviceAccountToken.path |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | path is the path relative to the mount point of the file to project the token into. |
| | || **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.config.files[index].serviceAccountToken.audience |
| **Value**       | string |
| **Required**    | false |
| **Example**     | |
| **Description** | audience is the intended audience of the token. A recipient of a token must identify itself with an identifier specified in the audience of the token, and otherwise should reject the token. The audience defaults to the identifier of the apiserver. |
| | || **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.config.files[index].serviceAccountToken.expirationSeconds |
| **Value**       | integer |
| **Required**    | false |
| **Example**     | |
| **Description** | expirationSeconds is the requested duration of validity of the service account token. As the token approaches expiration, the kubelet volume plugin will proactively rotate the service account token. The kubelet will start trying to rotate the token if the token is older than 80 percent of its time to live or if the token is older than 24 hours.Defaults to 1 hour and must be at least 10 minutes. |
| | |
| **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.customTLSSecret.items |
| **Value**       | []object |
| **Required**    | false |
| **Example**     | |
| **Description** | items if unspecified, each key-value pair in the Data field of the referenced Secret will be projected into the volume as a file whose name is the key and content is the value. If specified, the listed keys will be projected into the specified paths, and unlisted keys will not be present. If a key is specified which is not present in the Secret, the volume setup will error unless it is marked optional. Paths must be relative and may not contain the '..' path or start with '..'. |
| | || **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.customTLSSecret.name |
| **Value**       | string |
| **Required**    | false |
| **Example**     | |
| **Description** | Name of the referent. More info: https://kubernetes.io/docs/concepts/overview/working-with-objects/names/#names TODO: Add other useful fields. apiVersion, kind, uid? |
| | || **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.customTLSSecret.optional |
| **Value**       | boolean |
| **Required**    | false |
| **Example**     | |
| **Description** | optional field specify whether the Secret or its key must be defined |
| | |
| **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.customTLSSecret.items[index].key |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | key is the key to project. |
| | || **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.customTLSSecret.items[index].path |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | path is the relative path of the file to map the key to. May not be an absolute path. May not contain the path element '..'. May not start with the string '..'. |
| | || **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.customTLSSecret.items[index].mode |
| **Value**       | integer |
| **Required**    | false |
| **Example**     | |
| **Description** | mode is Optional: mode bits used to set permissions on this file. Must be an octal value between 0000 and 0777 or a decimal value between 0 and 511. YAML accepts both octal and decimal values, JSON requires decimal values for mode bits. If not specified, the volume defaultMode will be used. This might be in conflict with other options that affect the file mode, like fsGroup, and the result can be other mode bits set. |
| | |
| **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.expose.annotations |
| **Value**       | map[string]string |
| **Required**    | false |
| **Example**     | |
| **Description** |  |
| | || **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.expose.labels |
| **Value**       | map[string]string |
| **Required**    | false |
| **Example**     | |
| **Description** |  |
| | || **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.expose.nodePort |
| **Value**       | integer |
| **Required**    | false |
| **Example**     | |
| **Description** | The port on which this service is exposed when type is NodePort or LoadBalancer. Value must be in-range and not in use or the operation will fail. If unspecified, a port will be allocated if this Service requires one. - https://kubernetes.io/docs/concepts/services-networking/service/#type-nodeport |
| | || **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.expose.type |
| **Value**       | enum |
| **Required**    | false |
| **Example**     | |
| **Description** | More info: https://kubernetes.io/docs/concepts/services-networking/service/#publishing-services-service-types |
| | |
| **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.metadata.annotations |
| **Value**       | map[string]string |
| **Required**    | false |
| **Example**     | |
| **Description** |  |
| | || **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.metadata.labels |
| **Value**       | map[string]string |
| **Required**    | false |
| **Example**     | |
| **Description** |  |
| | |
| **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.resources.limits |
| **Value**       | map[string]int or string |
| **Required**    | false |
| **Example**     | |
| **Description** | Limits describes the maximum amount of compute resources allowed. More info: https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/ |
| | || **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.resources.requests |
| **Value**       | map[string]int or string |
| **Required**    | false |
| **Example**     | |
| **Description** | Requests describes the minimum amount of compute resources required. If Requests is omitted for a container, it defaults to Limits if that is explicitly specified, otherwise to an implementation-defined value. More info: https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/ |
| | |
| **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.sidecars[index].name |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | Name of the container specified as a DNS_LABEL. Each container in a pod must have a unique name (DNS_LABEL). Cannot be updated. |
| | || **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.sidecars[index].args |
| **Value**       | []string |
| **Required**    | false |
| **Example**     | |
| **Description** | Arguments to the entrypoint. The container image's CMD is used if this is not provided. Variable references $(VAR_NAME) are expanded using the container's environment. If a variable cannot be resolved, the reference in the input string will be unchanged. Double $$ are reduced to a single $, which allows for escaping the $(VAR_NAME) syntax: i.e. "$$(VAR_NAME)" will produce the string literal "$(VAR_NAME)". Escaped references will never be expanded, regardless of whether the variable exists or not. Cannot be updated. More info: https://kubernetes.io/docs/tasks/inject-data-application/define-command-argument-container/#running-a-command-in-a-shell |
| | || **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.sidecars[index].command |
| **Value**       | []string |
| **Required**    | false |
| **Example**     | |
| **Description** | Entrypoint array. Not executed within a shell. The container image's ENTRYPOINT is used if this is not provided. Variable references $(VAR_NAME) are expanded using the container's environment. If a variable cannot be resolved, the reference in the input string will be unchanged. Double $$ are reduced to a single $, which allows for escaping the $(VAR_NAME) syntax: i.e. "$$(VAR_NAME)" will produce the string literal "$(VAR_NAME)". Escaped references will never be expanded, regardless of whether the variable exists or not. Cannot be updated. More info: https://kubernetes.io/docs/tasks/inject-data-application/define-command-argument-container/#running-a-command-in-a-shell |
| | || **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.sidecars[index].env |
| **Value**       | []object |
| **Required**    | false |
| **Example**     | |
| **Description** | List of environment variables to set in the container. Cannot be updated. |
| | || **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.sidecars[index].envFrom |
| **Value**       | []object |
| **Required**    | false |
| **Example**     | |
| **Description** | List of sources to populate environment variables in the container. The keys defined within a source must be a C_IDENTIFIER. All invalid keys will be reported as an event when the container is starting. When a key exists in multiple sources, the value associated with the last source will take precedence. Values defined by an Env with a duplicate key will take precedence. Cannot be updated. |
| | || **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.sidecars[index].image |
| **Value**       | string |
| **Required**    | false |
| **Example**     | |
| **Description** | Container image name. More info: https://kubernetes.io/docs/concepts/containers/images This field is optional to allow higher level config management to default or override container images in workload controllers like Deployments and StatefulSets. |
| | || **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.sidecars[index].imagePullPolicy |
| **Value**       | string |
| **Required**    | false |
| **Example**     | |
| **Description** | Image pull policy. One of Always, Never, IfNotPresent. Defaults to Always if :latest tag is specified, or IfNotPresent otherwise. Cannot be updated. More info: https://kubernetes.io/docs/concepts/containers/images#updating-images |
| | || **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.sidecars[index].lifecycle |
| **Value**       | object |
| **Required**    | false |
| **Example**     | |
| **Description** | Actions that the management system should take in response to container lifecycle events. Cannot be updated. |
| | || **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.sidecars[index].livenessProbe |
| **Value**       | object |
| **Required**    | false |
| **Example**     | |
| **Description** | Periodic probe of container liveness. Container will be restarted if the probe fails. Cannot be updated. More info: https://kubernetes.io/docs/concepts/workloads/pods/pod-lifecycle#container-probes |
| | || **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.sidecars[index].ports |
| **Value**       | []object |
| **Required**    | false |
| **Example**     | |
| **Description** | List of ports to expose from the container. Not specifying a port here DOES NOT prevent that port from being exposed. Any port which is listening on the default "0.0.0.0" address inside a container will be accessible from the network. Modifying this array with strategic merge patch may corrupt the data. For more information See https://github.com/kubernetes/kubernetes/issues/108255. Cannot be updated. |
| | || **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.sidecars[index].readinessProbe |
| **Value**       | object |
| **Required**    | false |
| **Example**     | |
| **Description** | Periodic probe of container service readiness. Container will be removed from service endpoints if the probe fails. Cannot be updated. More info: https://kubernetes.io/docs/concepts/workloads/pods/pod-lifecycle#container-probes |
| | || **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.sidecars[index].resources |
| **Value**       | object |
| **Required**    | false |
| **Example**     | |
| **Description** | Compute Resources required by this container. Cannot be updated. More info: https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/ |
| | || **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.sidecars[index].securityContext |
| **Value**       | object |
| **Required**    | false |
| **Example**     | |
| **Description** | SecurityContext defines the security options the container should be run with. If set, the fields of SecurityContext override the equivalent fields of PodSecurityContext. More info: https://kubernetes.io/docs/tasks/configure-pod-container/security-context/ |
| | || **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.sidecars[index].startupProbe |
| **Value**       | object |
| **Required**    | false |
| **Example**     | |
| **Description** | StartupProbe indicates that the Pod has successfully initialized. If specified, no other probes are executed until this completes successfully. If this probe fails, the Pod will be restarted, just as if the livenessProbe failed. This can be used to provide different probe parameters at the beginning of a Pod's lifecycle, when it might take a long time to load data or warm a cache, than during steady-state operation. This cannot be updated. More info: https://kubernetes.io/docs/concepts/workloads/pods/pod-lifecycle#container-probes |
| | || **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.sidecars[index].stdin |
| **Value**       | boolean |
| **Required**    | false |
| **Example**     | |
| **Description** | Whether this container should allocate a buffer for stdin in the container runtime. If this is not set, reads from stdin in the container will always result in EOF. Default is false. |
| | || **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.sidecars[index].stdinOnce |
| **Value**       | boolean |
| **Required**    | false |
| **Example**     | |
| **Description** | Whether the container runtime should close the stdin channel after it has been opened by a single attach. When stdin is true the stdin stream will remain open across multiple attach sessions. If stdinOnce is set to true, stdin is opened on container start, is empty until the first client attaches to stdin, and then remains open and accepts data until the client disconnects, at which time stdin is closed and remains closed until the container is restarted. If this flag is false, a container processes that reads from stdin will never receive an EOF. Default is false |
| | || **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.sidecars[index].terminationMessagePath |
| **Value**       | string |
| **Required**    | false |
| **Example**     | |
| **Description** | Optional: Path at which the file to which the container's termination message will be written is mounted into the container's filesystem. Message written is intended to be brief final status, such as an assertion failure message. Will be truncated by the node if greater than 4096 bytes. The total message length across all containers will be limited to 12kb. Defaults to /dev/termination-log. Cannot be updated. |
| | || **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.sidecars[index].terminationMessagePolicy |
| **Value**       | string |
| **Required**    | false |
| **Example**     | |
| **Description** | Indicate how the termination message should be populated. File will use the contents of terminationMessagePath to populate the container status message on both success and failure. FallbackToLogsOnError will use the last chunk of container log output if the termination message file is empty and the container exited with an error. The log output is limited to 2048 bytes or 80 lines, whichever is smaller. Defaults to File. Cannot be updated. |
| | || **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.sidecars[index].tty |
| **Value**       | boolean |
| **Required**    | false |
| **Example**     | |
| **Description** | Whether this container should allocate a TTY for itself, also requires 'stdin' to be true. Default is false. |
| | || **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.sidecars[index].volumeDevices |
| **Value**       | []object |
| **Required**    | false |
| **Example**     | |
| **Description** | volumeDevices is the list of block devices to be used by the container. |
| | || **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.sidecars[index].volumeMounts |
| **Value**       | []object |
| **Required**    | false |
| **Example**     | |
| **Description** | Pod volumes to mount into the container's filesystem. Cannot be updated. |
| | || **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.sidecars[index].workingDir |
| **Value**       | string |
| **Required**    | false |
| **Example**     | |
| **Description** | Container's working directory. If not specified, the container runtime's default will be used, which might be configured in the container image. Cannot be updated. |
| | |
| **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.sidecars[index].env[index].name |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | Name of the environment variable. Must be a C_IDENTIFIER. |
| | || **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.sidecars[index].env[index].value |
| **Value**       | string |
| **Required**    | false |
| **Example**     | |
| **Description** | Variable references $(VAR_NAME) are expanded using the previously defined environment variables in the container and any service environment variables. If a variable cannot be resolved, the reference in the input string will be unchanged. Double $$ are reduced to a single $, which allows for escaping the $(VAR_NAME) syntax: i.e. "$$(VAR_NAME)" will produce the string literal "$(VAR_NAME)". Escaped references will never be expanded, regardless of whether the variable exists or not. Defaults to "". |
| | || **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.sidecars[index].env[index].valueFrom |
| **Value**       | object |
| **Required**    | false |
| **Example**     | |
| **Description** | Source for the environment variable's value. Cannot be used if value is not empty. |
| | |
| **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.sidecars[index].env[index].valueFrom.configMapKeyRef |
| **Value**       | object |
| **Required**    | false |
| **Example**     | |
| **Description** | Selects a key of a ConfigMap. |
| | || **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.sidecars[index].env[index].valueFrom.fieldRef |
| **Value**       | object |
| **Required**    | false |
| **Example**     | |
| **Description** | Selects a field of the pod: supports metadata.name, metadata.namespace, `metadata.labels['<KEY>']`, `metadata.annotations['<KEY>']`, spec.nodeName, spec.serviceAccountName, status.hostIP, status.podIP, status.podIPs. |
| | || **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.sidecars[index].env[index].valueFrom.resourceFieldRef |
| **Value**       | object |
| **Required**    | false |
| **Example**     | |
| **Description** | Selects a resource of the container: only resources limits and requests (limits.cpu, limits.memory, limits.ephemeral-storage, requests.cpu, requests.memory and requests.ephemeral-storage) are currently supported. |
| | || **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.sidecars[index].env[index].valueFrom.secretKeyRef |
| **Value**       | object |
| **Required**    | false |
| **Example**     | |
| **Description** | Selects a key of a secret in the pod's namespace |
| | |
| **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.sidecars[index].env[index].valueFrom.configMapKeyRef.key |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | The key to select. |
| | || **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.sidecars[index].env[index].valueFrom.configMapKeyRef.name |
| **Value**       | string |
| **Required**    | false |
| **Example**     | |
| **Description** | Name of the referent. More info: https://kubernetes.io/docs/concepts/overview/working-with-objects/names/#names TODO: Add other useful fields. apiVersion, kind, uid? |
| | || **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.sidecars[index].env[index].valueFrom.configMapKeyRef.optional |
| **Value**       | boolean |
| **Required**    | false |
| **Example**     | |
| **Description** | Specify whether the ConfigMap or its key must be defined |
| | |
| **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.sidecars[index].env[index].valueFrom.fieldRef.fieldPath |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | Path of the field to select in the specified API version. |
| | || **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.sidecars[index].env[index].valueFrom.fieldRef.apiVersion |
| **Value**       | string |
| **Required**    | false |
| **Example**     | |
| **Description** | Version of the schema the FieldPath is written in terms of, defaults to "v1". |
| | |
| **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.sidecars[index].env[index].valueFrom.resourceFieldRef.resource |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | Required: resource to select |
| | || **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.sidecars[index].env[index].valueFrom.resourceFieldRef.containerName |
| **Value**       | string |
| **Required**    | false |
| **Example**     | |
| **Description** | Container name: required for volumes, optional for env vars |
| | || **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.sidecars[index].env[index].valueFrom.resourceFieldRef.divisor |
| **Value**       | int or string |
| **Required**    | false |
| **Example**     | |
| **Description** | Specifies the output format of the exposed resources, defaults to "1" |
| | |
| **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.sidecars[index].env[index].valueFrom.secretKeyRef.key |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | The key of the secret to select from.  Must be a valid secret key. |
| | || **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.sidecars[index].env[index].valueFrom.secretKeyRef.name |
| **Value**       | string |
| **Required**    | false |
| **Example**     | |
| **Description** | Name of the referent. More info: https://kubernetes.io/docs/concepts/overview/working-with-objects/names/#names TODO: Add other useful fields. apiVersion, kind, uid? |
| | || **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.sidecars[index].env[index].valueFrom.secretKeyRef.optional |
| **Value**       | boolean |
| **Required**    | false |
| **Example**     | |
| **Description** | Specify whether the Secret or its key must be defined |
| | |
| **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.sidecars[index].envFrom[index].configMapRef |
| **Value**       | object |
| **Required**    | false |
| **Example**     | |
| **Description** | The ConfigMap to select from |
| | || **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.sidecars[index].envFrom[index].prefix |
| **Value**       | string |
| **Required**    | false |
| **Example**     | |
| **Description** | An optional identifier to prepend to each key in the ConfigMap. Must be a C_IDENTIFIER. |
| | || **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.sidecars[index].envFrom[index].secretRef |
| **Value**       | object |
| **Required**    | false |
| **Example**     | |
| **Description** | The Secret to select from |
| | |
| **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.sidecars[index].envFrom[index].configMapRef.name |
| **Value**       | string |
| **Required**    | false |
| **Example**     | |
| **Description** | Name of the referent. More info: https://kubernetes.io/docs/concepts/overview/working-with-objects/names/#names TODO: Add other useful fields. apiVersion, kind, uid? |
| | || **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.sidecars[index].envFrom[index].configMapRef.optional |
| **Value**       | boolean |
| **Required**    | false |
| **Example**     | |
| **Description** | Specify whether the ConfigMap must be defined |
| | |
| **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.sidecars[index].envFrom[index].secretRef.name |
| **Value**       | string |
| **Required**    | false |
| **Example**     | |
| **Description** | Name of the referent. More info: https://kubernetes.io/docs/concepts/overview/working-with-objects/names/#names TODO: Add other useful fields. apiVersion, kind, uid? |
| | || **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.sidecars[index].envFrom[index].secretRef.optional |
| **Value**       | boolean |
| **Required**    | false |
| **Example**     | |
| **Description** | Specify whether the Secret must be defined |
| | |
| **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.sidecars[index].lifecycle.postStart |
| **Value**       | object |
| **Required**    | false |
| **Example**     | |
| **Description** | PostStart is called immediately after a container is created. If the handler fails, the container is terminated and restarted according to its restart policy. Other management of the container blocks until the hook completes. More info: https://kubernetes.io/docs/concepts/containers/container-lifecycle-hooks/#container-hooks |
| | || **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.sidecars[index].lifecycle.preStop |
| **Value**       | object |
| **Required**    | false |
| **Example**     | |
| **Description** | PreStop is called immediately before a container is terminated due to an API request or management event such as liveness/startup probe failure, preemption, resource contention, etc. The handler is not called if the container crashes or exits. The Pod's termination grace period countdown begins before the PreStop hook is executed. Regardless of the outcome of the handler, the container will eventually terminate within the Pod's termination grace period (unless delayed by finalizers). Other management of the container blocks until the hook completes or until the termination grace period is reached. More info: https://kubernetes.io/docs/concepts/containers/container-lifecycle-hooks/#container-hooks |
| | |
| **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.sidecars[index].lifecycle.postStart.exec |
| **Value**       | object |
| **Required**    | false |
| **Example**     | |
| **Description** | Exec specifies the action to take. |
| | || **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.sidecars[index].lifecycle.postStart.httpGet |
| **Value**       | object |
| **Required**    | false |
| **Example**     | |
| **Description** | HTTPGet specifies the http request to perform. |
| | || **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.sidecars[index].lifecycle.postStart.tcpSocket |
| **Value**       | object |
| **Required**    | false |
| **Example**     | |
| **Description** | Deprecated. TCPSocket is NOT supported as a LifecycleHandler and kept for the backward compatibility. There are no validation of this field and lifecycle hooks will fail in runtime when tcp handler is specified. |
| | |
| **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.sidecars[index].lifecycle.postStart.exec.command |
| **Value**       | []string |
| **Required**    | false |
| **Example**     | |
| **Description** | Command is the command line to execute inside the container, the working directory for the command  is root ('/') in the container's filesystem. The command is simply exec'd, it is not run inside a shell, so traditional shell instructions ('|', etc) won't work. To use a shell, you need to explicitly call out to that shell. Exit status of 0 is treated as live/healthy and non-zero is unhealthy. |
| | |
| **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.sidecars[index].lifecycle.postStart.httpGet.port |
| **Value**       | int or string |
| **Required**    | true |
| **Example**     | |
| **Description** | Name or number of the port to access on the container. Number must be in the range 1 to 65535. Name must be an IANA_SVC_NAME. |
| | || **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.sidecars[index].lifecycle.postStart.httpGet.host |
| **Value**       | string |
| **Required**    | false |
| **Example**     | |
| **Description** | Host name to connect to, defaults to the pod IP. You probably want to set "Host" in httpHeaders instead. |
| | || **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.sidecars[index].lifecycle.postStart.httpGet.httpHeaders |
| **Value**       | []object |
| **Required**    | false |
| **Example**     | |
| **Description** | Custom headers to set in the request. HTTP allows repeated headers. |
| | || **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.sidecars[index].lifecycle.postStart.httpGet.path |
| **Value**       | string |
| **Required**    | false |
| **Example**     | |
| **Description** | Path to access on the HTTP server. |
| | || **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.sidecars[index].lifecycle.postStart.httpGet.scheme |
| **Value**       | string |
| **Required**    | false |
| **Example**     | |
| **Description** | Scheme to use for connecting to the host. Defaults to HTTP. |
| | |
| **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.sidecars[index].lifecycle.postStart.httpGet.httpHeaders[index].name |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | The header field name |
| | || **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.sidecars[index].lifecycle.postStart.httpGet.httpHeaders[index].value |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | The header field value |
| | |
| **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.sidecars[index].lifecycle.postStart.tcpSocket.port |
| **Value**       | int or string |
| **Required**    | true |
| **Example**     | |
| **Description** | Number or name of the port to access on the container. Number must be in the range 1 to 65535. Name must be an IANA_SVC_NAME. |
| | || **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.sidecars[index].lifecycle.postStart.tcpSocket.host |
| **Value**       | string |
| **Required**    | false |
| **Example**     | |
| **Description** | Optional: Host name to connect to, defaults to the pod IP. |
| | |
| **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.sidecars[index].lifecycle.preStop.exec |
| **Value**       | object |
| **Required**    | false |
| **Example**     | |
| **Description** | Exec specifies the action to take. |
| | || **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.sidecars[index].lifecycle.preStop.httpGet |
| **Value**       | object |
| **Required**    | false |
| **Example**     | |
| **Description** | HTTPGet specifies the http request to perform. |
| | || **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.sidecars[index].lifecycle.preStop.tcpSocket |
| **Value**       | object |
| **Required**    | false |
| **Example**     | |
| **Description** | Deprecated. TCPSocket is NOT supported as a LifecycleHandler and kept for the backward compatibility. There are no validation of this field and lifecycle hooks will fail in runtime when tcp handler is specified. |
| | |
| **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.sidecars[index].lifecycle.preStop.exec.command |
| **Value**       | []string |
| **Required**    | false |
| **Example**     | |
| **Description** | Command is the command line to execute inside the container, the working directory for the command  is root ('/') in the container's filesystem. The command is simply exec'd, it is not run inside a shell, so traditional shell instructions ('|', etc) won't work. To use a shell, you need to explicitly call out to that shell. Exit status of 0 is treated as live/healthy and non-zero is unhealthy. |
| | |
| **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.sidecars[index].lifecycle.preStop.httpGet.port |
| **Value**       | int or string |
| **Required**    | true |
| **Example**     | |
| **Description** | Name or number of the port to access on the container. Number must be in the range 1 to 65535. Name must be an IANA_SVC_NAME. |
| | || **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.sidecars[index].lifecycle.preStop.httpGet.host |
| **Value**       | string |
| **Required**    | false |
| **Example**     | |
| **Description** | Host name to connect to, defaults to the pod IP. You probably want to set "Host" in httpHeaders instead. |
| | || **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.sidecars[index].lifecycle.preStop.httpGet.httpHeaders |
| **Value**       | []object |
| **Required**    | false |
| **Example**     | |
| **Description** | Custom headers to set in the request. HTTP allows repeated headers. |
| | || **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.sidecars[index].lifecycle.preStop.httpGet.path |
| **Value**       | string |
| **Required**    | false |
| **Example**     | |
| **Description** | Path to access on the HTTP server. |
| | || **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.sidecars[index].lifecycle.preStop.httpGet.scheme |
| **Value**       | string |
| **Required**    | false |
| **Example**     | |
| **Description** | Scheme to use for connecting to the host. Defaults to HTTP. |
| | |
| **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.sidecars[index].lifecycle.preStop.httpGet.httpHeaders[index].name |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | The header field name |
| | || **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.sidecars[index].lifecycle.preStop.httpGet.httpHeaders[index].value |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | The header field value |
| | |
| **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.sidecars[index].lifecycle.preStop.tcpSocket.port |
| **Value**       | int or string |
| **Required**    | true |
| **Example**     | |
| **Description** | Number or name of the port to access on the container. Number must be in the range 1 to 65535. Name must be an IANA_SVC_NAME. |
| | || **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.sidecars[index].lifecycle.preStop.tcpSocket.host |
| **Value**       | string |
| **Required**    | false |
| **Example**     | |
| **Description** | Optional: Host name to connect to, defaults to the pod IP. |
| | |
| **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.sidecars[index].livenessProbe.exec |
| **Value**       | object |
| **Required**    | false |
| **Example**     | |
| **Description** | Exec specifies the action to take. |
| | || **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.sidecars[index].livenessProbe.failureThreshold |
| **Value**       | integer |
| **Required**    | false |
| **Example**     | |
| **Description** | Minimum consecutive failures for the probe to be considered failed after having succeeded. Defaults to 3. Minimum value is 1. |
| | || **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.sidecars[index].livenessProbe.grpc |
| **Value**       | object |
| **Required**    | false |
| **Example**     | |
| **Description** | GRPC specifies an action involving a GRPC port. This is a beta field and requires enabling GRPCContainerProbe feature gate. |
| | || **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.sidecars[index].livenessProbe.httpGet |
| **Value**       | object |
| **Required**    | false |
| **Example**     | |
| **Description** | HTTPGet specifies the http request to perform. |
| | || **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.sidecars[index].livenessProbe.initialDelaySeconds |
| **Value**       | integer |
| **Required**    | false |
| **Example**     | |
| **Description** | Number of seconds after the container has started before liveness probes are initiated. More info: https://kubernetes.io/docs/concepts/workloads/pods/pod-lifecycle#container-probes |
| | || **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.sidecars[index].livenessProbe.periodSeconds |
| **Value**       | integer |
| **Required**    | false |
| **Example**     | |
| **Description** | How often (in seconds) to perform the probe. Default to 10 seconds. Minimum value is 1. |
| | || **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.sidecars[index].livenessProbe.successThreshold |
| **Value**       | integer |
| **Required**    | false |
| **Example**     | |
| **Description** | Minimum consecutive successes for the probe to be considered successful after having failed. Defaults to 1. Must be 1 for liveness and startup. Minimum value is 1. |
| | || **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.sidecars[index].livenessProbe.tcpSocket |
| **Value**       | object |
| **Required**    | false |
| **Example**     | |
| **Description** | TCPSocket specifies an action involving a TCP port. |
| | || **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.sidecars[index].livenessProbe.terminationGracePeriodSeconds |
| **Value**       | integer |
| **Required**    | false |
| **Example**     | |
| **Description** | Optional duration in seconds the pod needs to terminate gracefully upon probe failure. The grace period is the duration in seconds after the processes running in the pod are sent a termination signal and the time when the processes are forcibly halted with a kill signal. Set this value longer than the expected cleanup time for your process. If this value is nil, the pod's terminationGracePeriodSeconds will be used. Otherwise, this value overrides the value provided by the pod spec. Value must be non-negative integer. The value zero indicates stop immediately via the kill signal (no opportunity to shut down). This is a beta field and requires enabling ProbeTerminationGracePeriod feature gate. Minimum value is 1. spec.terminationGracePeriodSeconds is used if unset. |
| | || **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.sidecars[index].livenessProbe.timeoutSeconds |
| **Value**       | integer |
| **Required**    | false |
| **Example**     | |
| **Description** | Number of seconds after which the probe times out. Defaults to 1 second. Minimum value is 1. More info: https://kubernetes.io/docs/concepts/workloads/pods/pod-lifecycle#container-probes |
| | |
| **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.sidecars[index].livenessProbe.exec.command |
| **Value**       | []string |
| **Required**    | false |
| **Example**     | |
| **Description** | Command is the command line to execute inside the container, the working directory for the command  is root ('/') in the container's filesystem. The command is simply exec'd, it is not run inside a shell, so traditional shell instructions ('|', etc) won't work. To use a shell, you need to explicitly call out to that shell. Exit status of 0 is treated as live/healthy and non-zero is unhealthy. |
| | |
| **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.sidecars[index].livenessProbe.grpc.port |
| **Value**       | integer |
| **Required**    | true |
| **Example**     | |
| **Description** | Port number of the gRPC service. Number must be in the range 1 to 65535. |
| | || **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.sidecars[index].livenessProbe.grpc.service |
| **Value**       | string |
| **Required**    | false |
| **Example**     | |
| **Description** | Service is the name of the service to place in the gRPC HealthCheckRequest (see https://github.com/grpc/grpc/blob/master/doc/health-checking.md). 
 If this is not specified, the default behavior is defined by gRPC. |
| | |
| **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.sidecars[index].livenessProbe.httpGet.port |
| **Value**       | int or string |
| **Required**    | true |
| **Example**     | |
| **Description** | Name or number of the port to access on the container. Number must be in the range 1 to 65535. Name must be an IANA_SVC_NAME. |
| | || **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.sidecars[index].livenessProbe.httpGet.host |
| **Value**       | string |
| **Required**    | false |
| **Example**     | |
| **Description** | Host name to connect to, defaults to the pod IP. You probably want to set "Host" in httpHeaders instead. |
| | || **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.sidecars[index].livenessProbe.httpGet.httpHeaders |
| **Value**       | []object |
| **Required**    | false |
| **Example**     | |
| **Description** | Custom headers to set in the request. HTTP allows repeated headers. |
| | || **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.sidecars[index].livenessProbe.httpGet.path |
| **Value**       | string |
| **Required**    | false |
| **Example**     | |
| **Description** | Path to access on the HTTP server. |
| | || **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.sidecars[index].livenessProbe.httpGet.scheme |
| **Value**       | string |
| **Required**    | false |
| **Example**     | |
| **Description** | Scheme to use for connecting to the host. Defaults to HTTP. |
| | |
| **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.sidecars[index].livenessProbe.httpGet.httpHeaders[index].name |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | The header field name |
| | || **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.sidecars[index].livenessProbe.httpGet.httpHeaders[index].value |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | The header field value |
| | |
| **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.sidecars[index].livenessProbe.tcpSocket.port |
| **Value**       | int or string |
| **Required**    | true |
| **Example**     | |
| **Description** | Number or name of the port to access on the container. Number must be in the range 1 to 65535. Name must be an IANA_SVC_NAME. |
| | || **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.sidecars[index].livenessProbe.tcpSocket.host |
| **Value**       | string |
| **Required**    | false |
| **Example**     | |
| **Description** | Optional: Host name to connect to, defaults to the pod IP. |
| | |
| **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.sidecars[index].ports[index].containerPort |
| **Value**       | integer |
| **Required**    | true |
| **Example**     | |
| **Description** | Number of port to expose on the pod's IP address. This must be a valid port number, 0 < x < 65536. |
| | || **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.sidecars[index].ports[index].hostIP |
| **Value**       | string |
| **Required**    | false |
| **Example**     | |
| **Description** | What host IP to bind the external port to. |
| | || **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.sidecars[index].ports[index].hostPort |
| **Value**       | integer |
| **Required**    | false |
| **Example**     | |
| **Description** | Number of port to expose on the host. If specified, this must be a valid port number, 0 < x < 65536. If HostNetwork is specified, this must match ContainerPort. Most containers do not need this. |
| | || **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.sidecars[index].ports[index].name |
| **Value**       | string |
| **Required**    | false |
| **Example**     | |
| **Description** | If specified, this must be an IANA_SVC_NAME and unique within the pod. Each named port in a pod must have a unique name. Name for the port that can be referred to by services. |
| | || **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.sidecars[index].ports[index].protocol |
| **Value**       | string |
| **Required**    | false |
| **Example**     | |
| **Description** | Protocol for port. Must be UDP, TCP, or SCTP. Defaults to "TCP". |
| | |
| **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.sidecars[index].readinessProbe.exec |
| **Value**       | object |
| **Required**    | false |
| **Example**     | |
| **Description** | Exec specifies the action to take. |
| | || **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.sidecars[index].readinessProbe.failureThreshold |
| **Value**       | integer |
| **Required**    | false |
| **Example**     | |
| **Description** | Minimum consecutive failures for the probe to be considered failed after having succeeded. Defaults to 3. Minimum value is 1. |
| | || **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.sidecars[index].readinessProbe.grpc |
| **Value**       | object |
| **Required**    | false |
| **Example**     | |
| **Description** | GRPC specifies an action involving a GRPC port. This is a beta field and requires enabling GRPCContainerProbe feature gate. |
| | || **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.sidecars[index].readinessProbe.httpGet |
| **Value**       | object |
| **Required**    | false |
| **Example**     | |
| **Description** | HTTPGet specifies the http request to perform. |
| | || **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.sidecars[index].readinessProbe.initialDelaySeconds |
| **Value**       | integer |
| **Required**    | false |
| **Example**     | |
| **Description** | Number of seconds after the container has started before liveness probes are initiated. More info: https://kubernetes.io/docs/concepts/workloads/pods/pod-lifecycle#container-probes |
| | || **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.sidecars[index].readinessProbe.periodSeconds |
| **Value**       | integer |
| **Required**    | false |
| **Example**     | |
| **Description** | How often (in seconds) to perform the probe. Default to 10 seconds. Minimum value is 1. |
| | || **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.sidecars[index].readinessProbe.successThreshold |
| **Value**       | integer |
| **Required**    | false |
| **Example**     | |
| **Description** | Minimum consecutive successes for the probe to be considered successful after having failed. Defaults to 1. Must be 1 for liveness and startup. Minimum value is 1. |
| | || **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.sidecars[index].readinessProbe.tcpSocket |
| **Value**       | object |
| **Required**    | false |
| **Example**     | |
| **Description** | TCPSocket specifies an action involving a TCP port. |
| | || **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.sidecars[index].readinessProbe.terminationGracePeriodSeconds |
| **Value**       | integer |
| **Required**    | false |
| **Example**     | |
| **Description** | Optional duration in seconds the pod needs to terminate gracefully upon probe failure. The grace period is the duration in seconds after the processes running in the pod are sent a termination signal and the time when the processes are forcibly halted with a kill signal. Set this value longer than the expected cleanup time for your process. If this value is nil, the pod's terminationGracePeriodSeconds will be used. Otherwise, this value overrides the value provided by the pod spec. Value must be non-negative integer. The value zero indicates stop immediately via the kill signal (no opportunity to shut down). This is a beta field and requires enabling ProbeTerminationGracePeriod feature gate. Minimum value is 1. spec.terminationGracePeriodSeconds is used if unset. |
| | || **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.sidecars[index].readinessProbe.timeoutSeconds |
| **Value**       | integer |
| **Required**    | false |
| **Example**     | |
| **Description** | Number of seconds after which the probe times out. Defaults to 1 second. Minimum value is 1. More info: https://kubernetes.io/docs/concepts/workloads/pods/pod-lifecycle#container-probes |
| | |
| **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.sidecars[index].readinessProbe.exec.command |
| **Value**       | []string |
| **Required**    | false |
| **Example**     | |
| **Description** | Command is the command line to execute inside the container, the working directory for the command  is root ('/') in the container's filesystem. The command is simply exec'd, it is not run inside a shell, so traditional shell instructions ('|', etc) won't work. To use a shell, you need to explicitly call out to that shell. Exit status of 0 is treated as live/healthy and non-zero is unhealthy. |
| | |
| **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.sidecars[index].readinessProbe.grpc.port |
| **Value**       | integer |
| **Required**    | true |
| **Example**     | |
| **Description** | Port number of the gRPC service. Number must be in the range 1 to 65535. |
| | || **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.sidecars[index].readinessProbe.grpc.service |
| **Value**       | string |
| **Required**    | false |
| **Example**     | |
| **Description** | Service is the name of the service to place in the gRPC HealthCheckRequest (see https://github.com/grpc/grpc/blob/master/doc/health-checking.md). 
 If this is not specified, the default behavior is defined by gRPC. |
| | |
| **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.sidecars[index].readinessProbe.httpGet.port |
| **Value**       | int or string |
| **Required**    | true |
| **Example**     | |
| **Description** | Name or number of the port to access on the container. Number must be in the range 1 to 65535. Name must be an IANA_SVC_NAME. |
| | || **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.sidecars[index].readinessProbe.httpGet.host |
| **Value**       | string |
| **Required**    | false |
| **Example**     | |
| **Description** | Host name to connect to, defaults to the pod IP. You probably want to set "Host" in httpHeaders instead. |
| | || **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.sidecars[index].readinessProbe.httpGet.httpHeaders |
| **Value**       | []object |
| **Required**    | false |
| **Example**     | |
| **Description** | Custom headers to set in the request. HTTP allows repeated headers. |
| | || **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.sidecars[index].readinessProbe.httpGet.path |
| **Value**       | string |
| **Required**    | false |
| **Example**     | |
| **Description** | Path to access on the HTTP server. |
| | || **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.sidecars[index].readinessProbe.httpGet.scheme |
| **Value**       | string |
| **Required**    | false |
| **Example**     | |
| **Description** | Scheme to use for connecting to the host. Defaults to HTTP. |
| | |
| **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.sidecars[index].readinessProbe.httpGet.httpHeaders[index].name |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | The header field name |
| | || **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.sidecars[index].readinessProbe.httpGet.httpHeaders[index].value |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | The header field value |
| | |
| **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.sidecars[index].readinessProbe.tcpSocket.port |
| **Value**       | int or string |
| **Required**    | true |
| **Example**     | |
| **Description** | Number or name of the port to access on the container. Number must be in the range 1 to 65535. Name must be an IANA_SVC_NAME. |
| | || **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.sidecars[index].readinessProbe.tcpSocket.host |
| **Value**       | string |
| **Required**    | false |
| **Example**     | |
| **Description** | Optional: Host name to connect to, defaults to the pod IP. |
| | |
| **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.sidecars[index].resources.limits |
| **Value**       | map[string]int or string |
| **Required**    | false |
| **Example**     | |
| **Description** | Limits describes the maximum amount of compute resources allowed. More info: https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/ |
| | || **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.sidecars[index].resources.requests |
| **Value**       | map[string]int or string |
| **Required**    | false |
| **Example**     | |
| **Description** | Requests describes the minimum amount of compute resources required. If Requests is omitted for a container, it defaults to Limits if that is explicitly specified, otherwise to an implementation-defined value. More info: https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/ |
| | |
| **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.sidecars[index].securityContext.allowPrivilegeEscalation |
| **Value**       | boolean |
| **Required**    | false |
| **Example**     | |
| **Description** | AllowPrivilegeEscalation controls whether a process can gain more privileges than its parent process. This bool directly controls if the no_new_privs flag will be set on the container process. AllowPrivilegeEscalation is true always when the container is: 1) run as Privileged 2) has CAP_SYS_ADMIN Note that this field cannot be set when spec.os.name is windows. |
| | || **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.sidecars[index].securityContext.capabilities |
| **Value**       | object |
| **Required**    | false |
| **Example**     | |
| **Description** | The capabilities to add/drop when running containers. Defaults to the default set of capabilities granted by the container runtime. Note that this field cannot be set when spec.os.name is windows. |
| | || **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.sidecars[index].securityContext.privileged |
| **Value**       | boolean |
| **Required**    | false |
| **Example**     | |
| **Description** | Run container in privileged mode. Processes in privileged containers are essentially equivalent to root on the host. Defaults to false. Note that this field cannot be set when spec.os.name is windows. |
| | || **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.sidecars[index].securityContext.procMount |
| **Value**       | string |
| **Required**    | false |
| **Example**     | |
| **Description** | procMount denotes the type of proc mount to use for the containers. The default is DefaultProcMount which uses the container runtime defaults for readonly paths and masked paths. This requires the ProcMountType feature flag to be enabled. Note that this field cannot be set when spec.os.name is windows. |
| | || **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.sidecars[index].securityContext.readOnlyRootFilesystem |
| **Value**       | boolean |
| **Required**    | false |
| **Example**     | |
| **Description** | Whether this container has a read-only root filesystem. Default is false. Note that this field cannot be set when spec.os.name is windows. |
| | || **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.sidecars[index].securityContext.runAsGroup |
| **Value**       | integer |
| **Required**    | false |
| **Example**     | |
| **Description** | The GID to run the entrypoint of the container process. Uses runtime default if unset. May also be set in PodSecurityContext.  If set in both SecurityContext and PodSecurityContext, the value specified in SecurityContext takes precedence. Note that this field cannot be set when spec.os.name is windows. |
| | || **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.sidecars[index].securityContext.runAsNonRoot |
| **Value**       | boolean |
| **Required**    | false |
| **Example**     | |
| **Description** | Indicates that the container must run as a non-root user. If true, the Kubelet will validate the image at runtime to ensure that it does not run as UID 0 (root) and fail to start the container if it does. If unset or false, no such validation will be performed. May also be set in PodSecurityContext.  If set in both SecurityContext and PodSecurityContext, the value specified in SecurityContext takes precedence. |
| | || **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.sidecars[index].securityContext.runAsUser |
| **Value**       | integer |
| **Required**    | false |
| **Example**     | |
| **Description** | The UID to run the entrypoint of the container process. Defaults to user specified in image metadata if unspecified. May also be set in PodSecurityContext.  If set in both SecurityContext and PodSecurityContext, the value specified in SecurityContext takes precedence. Note that this field cannot be set when spec.os.name is windows. |
| | || **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.sidecars[index].securityContext.seLinuxOptions |
| **Value**       | object |
| **Required**    | false |
| **Example**     | |
| **Description** | The SELinux context to be applied to the container. If unspecified, the container runtime will allocate a random SELinux context for each container.  May also be set in PodSecurityContext.  If set in both SecurityContext and PodSecurityContext, the value specified in SecurityContext takes precedence. Note that this field cannot be set when spec.os.name is windows. |
| | || **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.sidecars[index].securityContext.seccompProfile |
| **Value**       | object |
| **Required**    | false |
| **Example**     | |
| **Description** | The seccomp options to use by this container. If seccomp options are provided at both the pod & container level, the container options override the pod options. Note that this field cannot be set when spec.os.name is windows. |
| | || **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.sidecars[index].securityContext.windowsOptions |
| **Value**       | object |
| **Required**    | false |
| **Example**     | |
| **Description** | The Windows specific settings applied to all containers. If unspecified, the options from the PodSecurityContext will be used. If set in both SecurityContext and PodSecurityContext, the value specified in SecurityContext takes precedence. Note that this field cannot be set when spec.os.name is linux. |
| | |
| **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.sidecars[index].securityContext.capabilities.add |
| **Value**       | []string |
| **Required**    | false |
| **Example**     | |
| **Description** | Added capabilities |
| | || **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.sidecars[index].securityContext.capabilities.drop |
| **Value**       | []string |
| **Required**    | false |
| **Example**     | |
| **Description** | Removed capabilities |
| | |
| **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.sidecars[index].securityContext.seLinuxOptions.level |
| **Value**       | string |
| **Required**    | false |
| **Example**     | |
| **Description** | Level is SELinux level label that applies to the container. |
| | || **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.sidecars[index].securityContext.seLinuxOptions.role |
| **Value**       | string |
| **Required**    | false |
| **Example**     | |
| **Description** | Role is a SELinux role label that applies to the container. |
| | || **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.sidecars[index].securityContext.seLinuxOptions.type |
| **Value**       | string |
| **Required**    | false |
| **Example**     | |
| **Description** | Type is a SELinux type label that applies to the container. |
| | || **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.sidecars[index].securityContext.seLinuxOptions.user |
| **Value**       | string |
| **Required**    | false |
| **Example**     | |
| **Description** | User is a SELinux user label that applies to the container. |
| | |
| **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.sidecars[index].securityContext.seccompProfile.type |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | type indicates which kind of seccomp profile will be applied. Valid options are: 
 Localhost - a profile defined in a file on the node should be used. RuntimeDefault - the container runtime default profile should be used. Unconfined - no profile should be applied. |
| | || **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.sidecars[index].securityContext.seccompProfile.localhostProfile |
| **Value**       | string |
| **Required**    | false |
| **Example**     | |
| **Description** | localhostProfile indicates a profile defined in a file on the node should be used. The profile must be preconfigured on the node to work. Must be a descending path, relative to the kubelet's configured seccomp profile location. Must only be set if type is "Localhost". |
| | |
| **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.sidecars[index].securityContext.windowsOptions.gmsaCredentialSpec |
| **Value**       | string |
| **Required**    | false |
| **Example**     | |
| **Description** | GMSACredentialSpec is where the GMSA admission webhook (https://github.com/kubernetes-sigs/windows-gmsa) inlines the contents of the GMSA credential spec named by the GMSACredentialSpecName field. |
| | || **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.sidecars[index].securityContext.windowsOptions.gmsaCredentialSpecName |
| **Value**       | string |
| **Required**    | false |
| **Example**     | |
| **Description** | GMSACredentialSpecName is the name of the GMSA credential spec to use. |
| | || **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.sidecars[index].securityContext.windowsOptions.hostProcess |
| **Value**       | boolean |
| **Required**    | false |
| **Example**     | |
| **Description** | HostProcess determines if a container should be run as a 'Host Process' container. This field is alpha-level and will only be honored by components that enable the WindowsHostProcessContainers feature flag. Setting this field without the feature flag will result in errors when validating the Pod. All of a Pod's containers must have the same effective HostProcess value (it is not allowed to have a mix of HostProcess containers and non-HostProcess containers).  In addition, if HostProcess is true then HostNetwork must also be set to true. |
| | || **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.sidecars[index].securityContext.windowsOptions.runAsUserName |
| **Value**       | string |
| **Required**    | false |
| **Example**     | |
| **Description** | The UserName in Windows to run the entrypoint of the container process. Defaults to the user specified in image metadata if unspecified. May also be set in PodSecurityContext. If set in both SecurityContext and PodSecurityContext, the value specified in SecurityContext takes precedence. |
| | |
| **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.sidecars[index].startupProbe.exec |
| **Value**       | object |
| **Required**    | false |
| **Example**     | |
| **Description** | Exec specifies the action to take. |
| | || **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.sidecars[index].startupProbe.failureThreshold |
| **Value**       | integer |
| **Required**    | false |
| **Example**     | |
| **Description** | Minimum consecutive failures for the probe to be considered failed after having succeeded. Defaults to 3. Minimum value is 1. |
| | || **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.sidecars[index].startupProbe.grpc |
| **Value**       | object |
| **Required**    | false |
| **Example**     | |
| **Description** | GRPC specifies an action involving a GRPC port. This is a beta field and requires enabling GRPCContainerProbe feature gate. |
| | || **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.sidecars[index].startupProbe.httpGet |
| **Value**       | object |
| **Required**    | false |
| **Example**     | |
| **Description** | HTTPGet specifies the http request to perform. |
| | || **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.sidecars[index].startupProbe.initialDelaySeconds |
| **Value**       | integer |
| **Required**    | false |
| **Example**     | |
| **Description** | Number of seconds after the container has started before liveness probes are initiated. More info: https://kubernetes.io/docs/concepts/workloads/pods/pod-lifecycle#container-probes |
| | || **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.sidecars[index].startupProbe.periodSeconds |
| **Value**       | integer |
| **Required**    | false |
| **Example**     | |
| **Description** | How often (in seconds) to perform the probe. Default to 10 seconds. Minimum value is 1. |
| | || **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.sidecars[index].startupProbe.successThreshold |
| **Value**       | integer |
| **Required**    | false |
| **Example**     | |
| **Description** | Minimum consecutive successes for the probe to be considered successful after having failed. Defaults to 1. Must be 1 for liveness and startup. Minimum value is 1. |
| | || **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.sidecars[index].startupProbe.tcpSocket |
| **Value**       | object |
| **Required**    | false |
| **Example**     | |
| **Description** | TCPSocket specifies an action involving a TCP port. |
| | || **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.sidecars[index].startupProbe.terminationGracePeriodSeconds |
| **Value**       | integer |
| **Required**    | false |
| **Example**     | |
| **Description** | Optional duration in seconds the pod needs to terminate gracefully upon probe failure. The grace period is the duration in seconds after the processes running in the pod are sent a termination signal and the time when the processes are forcibly halted with a kill signal. Set this value longer than the expected cleanup time for your process. If this value is nil, the pod's terminationGracePeriodSeconds will be used. Otherwise, this value overrides the value provided by the pod spec. Value must be non-negative integer. The value zero indicates stop immediately via the kill signal (no opportunity to shut down). This is a beta field and requires enabling ProbeTerminationGracePeriod feature gate. Minimum value is 1. spec.terminationGracePeriodSeconds is used if unset. |
| | || **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.sidecars[index].startupProbe.timeoutSeconds |
| **Value**       | integer |
| **Required**    | false |
| **Example**     | |
| **Description** | Number of seconds after which the probe times out. Defaults to 1 second. Minimum value is 1. More info: https://kubernetes.io/docs/concepts/workloads/pods/pod-lifecycle#container-probes |
| | |
| **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.sidecars[index].startupProbe.exec.command |
| **Value**       | []string |
| **Required**    | false |
| **Example**     | |
| **Description** | Command is the command line to execute inside the container, the working directory for the command  is root ('/') in the container's filesystem. The command is simply exec'd, it is not run inside a shell, so traditional shell instructions ('|', etc) won't work. To use a shell, you need to explicitly call out to that shell. Exit status of 0 is treated as live/healthy and non-zero is unhealthy. |
| | |
| **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.sidecars[index].startupProbe.grpc.port |
| **Value**       | integer |
| **Required**    | true |
| **Example**     | |
| **Description** | Port number of the gRPC service. Number must be in the range 1 to 65535. |
| | || **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.sidecars[index].startupProbe.grpc.service |
| **Value**       | string |
| **Required**    | false |
| **Example**     | |
| **Description** | Service is the name of the service to place in the gRPC HealthCheckRequest (see https://github.com/grpc/grpc/blob/master/doc/health-checking.md). 
 If this is not specified, the default behavior is defined by gRPC. |
| | |
| **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.sidecars[index].startupProbe.httpGet.port |
| **Value**       | int or string |
| **Required**    | true |
| **Example**     | |
| **Description** | Name or number of the port to access on the container. Number must be in the range 1 to 65535. Name must be an IANA_SVC_NAME. |
| | || **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.sidecars[index].startupProbe.httpGet.host |
| **Value**       | string |
| **Required**    | false |
| **Example**     | |
| **Description** | Host name to connect to, defaults to the pod IP. You probably want to set "Host" in httpHeaders instead. |
| | || **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.sidecars[index].startupProbe.httpGet.httpHeaders |
| **Value**       | []object |
| **Required**    | false |
| **Example**     | |
| **Description** | Custom headers to set in the request. HTTP allows repeated headers. |
| | || **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.sidecars[index].startupProbe.httpGet.path |
| **Value**       | string |
| **Required**    | false |
| **Example**     | |
| **Description** | Path to access on the HTTP server. |
| | || **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.sidecars[index].startupProbe.httpGet.scheme |
| **Value**       | string |
| **Required**    | false |
| **Example**     | |
| **Description** | Scheme to use for connecting to the host. Defaults to HTTP. |
| | |
| **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.sidecars[index].startupProbe.httpGet.httpHeaders[index].name |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | The header field name |
| | || **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.sidecars[index].startupProbe.httpGet.httpHeaders[index].value |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | The header field value |
| | |
| **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.sidecars[index].startupProbe.tcpSocket.port |
| **Value**       | int or string |
| **Required**    | true |
| **Example**     | |
| **Description** | Number or name of the port to access on the container. Number must be in the range 1 to 65535. Name must be an IANA_SVC_NAME. |
| | || **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.sidecars[index].startupProbe.tcpSocket.host |
| **Value**       | string |
| **Required**    | false |
| **Example**     | |
| **Description** | Optional: Host name to connect to, defaults to the pod IP. |
| | |
| **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.sidecars[index].volumeDevices[index].devicePath |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | devicePath is the path inside of the container that the device will be mapped to. |
| | || **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.sidecars[index].volumeDevices[index].name |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | name must match the name of a persistentVolumeClaim in the pod |
| | |
| **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.sidecars[index].volumeMounts[index].mountPath |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | Path within the container at which the volume should be mounted.  Must not contain ':'. |
| | || **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.sidecars[index].volumeMounts[index].name |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | This must match the Name of a Volume. |
| | || **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.sidecars[index].volumeMounts[index].mountPropagation |
| **Value**       | string |
| **Required**    | false |
| **Example**     | |
| **Description** | mountPropagation determines how mounts are propagated from the host to container and the other way around. When not set, MountPropagationNone is used. This field is beta in 1.10. |
| | || **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.sidecars[index].volumeMounts[index].readOnly |
| **Value**       | boolean |
| **Required**    | false |
| **Example**     | |
| **Description** | Mounted read-only if true, read-write otherwise (false or unspecified). Defaults to false. |
| | || **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.sidecars[index].volumeMounts[index].subPath |
| **Value**       | string |
| **Required**    | false |
| **Example**     | |
| **Description** | Path within the volume from which the container's volume should be mounted. Defaults to "" (volume's root). |
| | || **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.sidecars[index].volumeMounts[index].subPathExpr |
| **Value**       | string |
| **Required**    | false |
| **Example**     | |
| **Description** | Expanded path within the volume from which the container's volume should be mounted. Behaves similarly to SubPath but environment variable references $(VAR_NAME) are expanded using the container's environment. Defaults to "" (volume's root). SubPathExpr and SubPath are mutually exclusive. |
| | |
| **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.tolerations[index].effect |
| **Value**       | string |
| **Required**    | false |
| **Example**     | |
| **Description** | Effect indicates the taint effect to match. Empty means match all taint effects. When specified, allowed values are NoSchedule, PreferNoSchedule and NoExecute. |
| | || **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.tolerations[index].key |
| **Value**       | string |
| **Required**    | false |
| **Example**     | |
| **Description** | Key is the taint key that the toleration applies to. Empty means match all taint keys. If the key is empty, operator must be Exists; this combination means to match all values and all keys. |
| | || **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.tolerations[index].operator |
| **Value**       | string |
| **Required**    | false |
| **Example**     | |
| **Description** | Operator represents a key's relationship to the value. Valid operators are Exists and Equal. Defaults to Equal. Exists is equivalent to wildcard for value, so that a pod can tolerate all taints of a particular category. |
| | || **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.tolerations[index].tolerationSeconds |
| **Value**       | integer |
| **Required**    | false |
| **Example**     | |
| **Description** | TolerationSeconds represents the period of time the toleration (which must be of effect NoExecute, otherwise this field is ignored) tolerates the taint. By default, it is not set, which means tolerate the taint forever (do not evict). Zero and negative values will be treated as 0 (evict immediately) by the system. |
| | || **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.tolerations[index].value |
| **Value**       | string |
| **Required**    | false |
| **Example**     | |
| **Description** | Value is the taint value the toleration matches to. If the operator is Exists, the value should be empty, otherwise just a regular string. |
| | |
| **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.topologySpreadConstraints[index].maxSkew |
| **Value**       | integer |
| **Required**    | true |
| **Example**     | |
| **Description** | MaxSkew describes the degree to which pods may be unevenly distributed. When `whenUnsatisfiable=DoNotSchedule`, it is the maximum permitted difference between the number of matching pods in the target topology and the global minimum. The global minimum is the minimum number of matching pods in an eligible domain or zero if the number of eligible domains is less than MinDomains. For example, in a 3-zone cluster, MaxSkew is set to 1, and pods with the same labelSelector spread as 2/2/1: In this case, the global minimum is 1. | zone1 | zone2 | zone3 | |  P P  |  P P  |   P   | - if MaxSkew is 1, incoming pod can only be scheduled to zone3 to become 2/2/2; scheduling it onto zone1(zone2) would make the ActualSkew(3-1) on zone1(zone2) violate MaxSkew(1). - if MaxSkew is 2, incoming pod can be scheduled onto any zone. When `whenUnsatisfiable=ScheduleAnyway`, it is used to give higher precedence to topologies that satisfy it. It's a required field. Default value is 1 and 0 is not allowed. |
| | || **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.topologySpreadConstraints[index].topologyKey |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | TopologyKey is the key of node labels. Nodes that have a label with this key and identical values are considered to be in the same topology. We consider each <key, value> as a "bucket", and try to put balanced number of pods into each bucket. We define a domain as a particular instance of a topology. Also, we define an eligible domain as a domain whose nodes meet the requirements of nodeAffinityPolicy and nodeTaintsPolicy. e.g. If TopologyKey is "kubernetes.io/hostname", each Node is a domain of that topology. And, if TopologyKey is "topology.kubernetes.io/zone", each zone is a domain of that topology. It's a required field. |
| | || **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.topologySpreadConstraints[index].whenUnsatisfiable |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | WhenUnsatisfiable indicates how to deal with a pod if it doesn't satisfy the spread constraint. - DoNotSchedule (default) tells the scheduler not to schedule it. - ScheduleAnyway tells the scheduler to schedule the pod in any location, but giving higher precedence to topologies that would help reduce the skew. A constraint is considered "Unsatisfiable" for an incoming pod if and only if every possible node assignment for that pod would violate "MaxSkew" on some topology. For example, in a 3-zone cluster, MaxSkew is set to 1, and pods with the same labelSelector spread as 3/1/1: | zone1 | zone2 | zone3 | | P P P |   P   |   P   | If WhenUnsatisfiable is set to DoNotSchedule, incoming pod can only be scheduled to zone2(zone3) to become 3/2/1(3/1/2) as ActualSkew(2-1) on zone2(zone3) satisfies MaxSkew(1). In other words, the cluster can still be imbalanced, but scheduler won't make it *more* imbalanced. It's a required field. |
| | || **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.topologySpreadConstraints[index].labelSelector |
| **Value**       | object |
| **Required**    | false |
| **Example**     | |
| **Description** | LabelSelector is used to find matching pods. Pods that match this label selector are counted to determine the number of pods in their corresponding topology domain. |
| | || **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.topologySpreadConstraints[index].matchLabelKeys |
| **Value**       | []string |
| **Required**    | false |
| **Example**     | |
| **Description** | MatchLabelKeys is a set of pod label keys to select the pods over which spreading will be calculated. The keys are used to lookup values from the incoming pod labels, those key-value labels are ANDed with labelSelector to select the group of existing pods over which spreading will be calculated for the incoming pod. Keys that don't exist in the incoming pod labels will be ignored. A null or empty list means only match against labelSelector. |
| | || **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.topologySpreadConstraints[index].minDomains |
| **Value**       | integer |
| **Required**    | false |
| **Example**     | |
| **Description** | MinDomains indicates a minimum number of eligible domains. When the number of eligible domains with matching topology keys is less than minDomains, Pod Topology Spread treats "global minimum" as 0, and then the calculation of Skew is performed. And when the number of eligible domains with matching topology keys equals or greater than minDomains, this value has no effect on scheduling. As a result, when the number of eligible domains is less than minDomains, scheduler won't schedule more than maxSkew Pods to those domains. If value is nil, the constraint behaves as if MinDomains is equal to 1. Valid values are integers greater than 0. When value is not nil, WhenUnsatisfiable must be DoNotSchedule. 
 For example, in a 3-zone cluster, MaxSkew is set to 2, MinDomains is set to 5 and pods with the same labelSelector spread as 2/2/2: | zone1 | zone2 | zone3 | |  P P  |  P P  |  P P  | The number of domains is less than 5(MinDomains), so "global minimum" is treated as 0. In this situation, new pod with the same labelSelector cannot be scheduled, because computed skew will be 3(3 - 0) if new Pod is scheduled to any of the three zones, it will violate MaxSkew. 
 This is a beta field and requires the MinDomainsInPodTopologySpread feature gate to be enabled (enabled by default). |
| | || **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.topologySpreadConstraints[index].nodeAffinityPolicy |
| **Value**       | string |
| **Required**    | false |
| **Example**     | |
| **Description** | NodeAffinityPolicy indicates how we will treat Pod's nodeAffinity/nodeSelector when calculating pod topology spread skew. Options are: - Honor: only nodes matching nodeAffinity/nodeSelector are included in the calculations. - Ignore: nodeAffinity/nodeSelector are ignored. All nodes are included in the calculations. 
 If this value is nil, the behavior is equivalent to the Honor policy. This is a alpha-level feature enabled by the NodeInclusionPolicyInPodTopologySpread feature flag. |
| | || **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.topologySpreadConstraints[index].nodeTaintsPolicy |
| **Value**       | string |
| **Required**    | false |
| **Example**     | |
| **Description** | NodeTaintsPolicy indicates how we will treat node taints when calculating pod topology spread skew. Options are: - Honor: nodes without taints, along with tainted nodes for which the incoming pod has a toleration, are included. - Ignore: node taints are ignored. All nodes are included. 
 If this value is nil, the behavior is equivalent to the Ignore policy. This is a alpha-level feature enabled by the NodeInclusionPolicyInPodTopologySpread feature flag. |
| | |
| **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.topologySpreadConstraints[index].labelSelector.matchExpressions |
| **Value**       | []object |
| **Required**    | false |
| **Example**     | |
| **Description** | matchExpressions is a list of label selector requirements. The requirements are ANDed. |
| | || **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.topologySpreadConstraints[index].labelSelector.matchLabels |
| **Value**       | map[string]string |
| **Required**    | false |
| **Example**     | |
| **Description** | matchLabels is a map of {key,value} pairs. A single {key,value} in the matchLabels map is equivalent to an element of matchExpressions, whose key field is "key", the operator is "In", and the values array contains only "value". The requirements are ANDed. |
| | |
| **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.topologySpreadConstraints[index].labelSelector.matchExpressions[index].key |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | key is the label key that the selector applies to. |
| | || **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.topologySpreadConstraints[index].labelSelector.matchExpressions[index].operator |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | operator represents a key's relationship to a set of values. Valid operators are In, NotIn, Exists and DoesNotExist. |
| | || **Key**         | PerconaPGCluster.spec.proxy.pgBouncer.topologySpreadConstraints[index].labelSelector.matchExpressions[index].values |
| **Value**       | []string |
| **Required**    | false |
| **Example**     | |
| **Description** | values is an array of string values. If the operator is In or NotIn, the values array must be non-empty. If the operator is Exists or DoesNotExist, the values array must be empty. This array is replaced during a strategic merge patch. |
| | |
| **Key**         | PerconaPGCluster.spec.secrets.customReplicationTLSSecret |
| **Value**       | object |
| **Required**    | false |
| **Example**     | |
| **Description** | The secret containing the replication client certificates and keys for secure connections to the PostgreSQL server. It will need to contain the client TLS certificate, TLS key and the Certificate Authority certificate with the data keys set to tls.crt, tls.key and ca.crt, respectively. NOTE: If CustomReplicationClientTLSSecret is provided, CustomTLSSecret MUST be provided and the ca.crt provided must be the same. |
| | || **Key**         | PerconaPGCluster.spec.secrets.customTLSSecret |
| **Value**       | object |
| **Required**    | false |
| **Example**     | |
| **Description** | The secret containing the Certificates and Keys to encrypt PostgreSQL traffic will need to contain the server TLS certificate, TLS key and the Certificate Authority certificate with the data keys set to tls.crt, tls.key and ca.crt, respectively. It will then be mounted as a volume projection to the '/pgconf/tls' directory. For more information on Kubernetes secret projections, please see https://k8s.io/docs/concepts/configuration/secret/#projection-of-secret-keys-to-specific-paths NOTE: If CustomTLSSecret is provided, CustomReplicationClientTLSSecret MUST be provided and the ca.crt provided must be the same. |
| | |
| **Key**         | PerconaPGCluster.spec.secrets.customReplicationTLSSecret.items |
| **Value**       | []object |
| **Required**    | false |
| **Example**     | |
| **Description** | items if unspecified, each key-value pair in the Data field of the referenced Secret will be projected into the volume as a file whose name is the key and content is the value. If specified, the listed keys will be projected into the specified paths, and unlisted keys will not be present. If a key is specified which is not present in the Secret, the volume setup will error unless it is marked optional. Paths must be relative and may not contain the '..' path or start with '..'. |
| | || **Key**         | PerconaPGCluster.spec.secrets.customReplicationTLSSecret.name |
| **Value**       | string |
| **Required**    | false |
| **Example**     | |
| **Description** | Name of the referent. More info: https://kubernetes.io/docs/concepts/overview/working-with-objects/names/#names TODO: Add other useful fields. apiVersion, kind, uid? |
| | || **Key**         | PerconaPGCluster.spec.secrets.customReplicationTLSSecret.optional |
| **Value**       | boolean |
| **Required**    | false |
| **Example**     | |
| **Description** | optional field specify whether the Secret or its key must be defined |
| | |
| **Key**         | PerconaPGCluster.spec.secrets.customReplicationTLSSecret.items[index].key |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | key is the key to project. |
| | || **Key**         | PerconaPGCluster.spec.secrets.customReplicationTLSSecret.items[index].path |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | path is the relative path of the file to map the key to. May not be an absolute path. May not contain the path element '..'. May not start with the string '..'. |
| | || **Key**         | PerconaPGCluster.spec.secrets.customReplicationTLSSecret.items[index].mode |
| **Value**       | integer |
| **Required**    | false |
| **Example**     | |
| **Description** | mode is Optional: mode bits used to set permissions on this file. Must be an octal value between 0000 and 0777 or a decimal value between 0 and 511. YAML accepts both octal and decimal values, JSON requires decimal values for mode bits. If not specified, the volume defaultMode will be used. This might be in conflict with other options that affect the file mode, like fsGroup, and the result can be other mode bits set. |
| | |
| **Key**         | PerconaPGCluster.spec.secrets.customTLSSecret.items |
| **Value**       | []object |
| **Required**    | false |
| **Example**     | |
| **Description** | items if unspecified, each key-value pair in the Data field of the referenced Secret will be projected into the volume as a file whose name is the key and content is the value. If specified, the listed keys will be projected into the specified paths, and unlisted keys will not be present. If a key is specified which is not present in the Secret, the volume setup will error unless it is marked optional. Paths must be relative and may not contain the '..' path or start with '..'. |
| | || **Key**         | PerconaPGCluster.spec.secrets.customTLSSecret.name |
| **Value**       | string |
| **Required**    | false |
| **Example**     | |
| **Description** | Name of the referent. More info: https://kubernetes.io/docs/concepts/overview/working-with-objects/names/#names TODO: Add other useful fields. apiVersion, kind, uid? |
| | || **Key**         | PerconaPGCluster.spec.secrets.customTLSSecret.optional |
| **Value**       | boolean |
| **Required**    | false |
| **Example**     | |
| **Description** | optional field specify whether the Secret or its key must be defined |
| | |
| **Key**         | PerconaPGCluster.spec.secrets.customTLSSecret.items[index].key |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | key is the key to project. |
| | || **Key**         | PerconaPGCluster.spec.secrets.customTLSSecret.items[index].path |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | path is the relative path of the file to map the key to. May not be an absolute path. May not contain the path element '..'. May not start with the string '..'. |
| | || **Key**         | PerconaPGCluster.spec.secrets.customTLSSecret.items[index].mode |
| **Value**       | integer |
| **Required**    | false |
| **Example**     | |
| **Description** | mode is Optional: mode bits used to set permissions on this file. Must be an octal value between 0000 and 0777 or a decimal value between 0 and 511. YAML accepts both octal and decimal values, JSON requires decimal values for mode bits. If not specified, the volume defaultMode will be used. This might be in conflict with other options that affect the file mode, like fsGroup, and the result can be other mode bits set. |
| | |
| **Key**         | PerconaPGCluster.spec.standby.enabled |
| **Value**       | boolean |
| **Required**    | false |
| **Example**     | |
| **Description** | Whether or not the PostgreSQL cluster should be read-only. When this is true, WAL files are applied from a pgBackRest repository or another PostgreSQL server. |
| | || **Key**         | PerconaPGCluster.spec.standby.host |
| **Value**       | string |
| **Required**    | false |
| **Example**     | |
| **Description** | Network address of the PostgreSQL server to follow via streaming replication. |
| | || **Key**         | PerconaPGCluster.spec.standby.port |
| **Value**       | integer |
| **Required**    | false |
| **Example**     | |
| **Description** | Network port of the PostgreSQL server to follow via streaming replication. |
| | || **Key**         | PerconaPGCluster.spec.standby.repoName |
| **Value**       | string |
| **Required**    | false |
| **Example**     | |
| **Description** | The name of the pgBackRest repository to follow for WAL files. |
| | |
| **Key**         | PerconaPGCluster.spec.users[index].name |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | The name of this PostgreSQL user. The value may contain only lowercase letters, numbers, and hyphen so that it fits into Kubernetes metadata. |
| | || **Key**         | PerconaPGCluster.spec.users[index].databases |
| **Value**       | []string |
| **Required**    | false |
| **Example**     | |
| **Description** | Databases to which this user can connect and create objects. Removing a database from this list does NOT revoke access. This field is ignored for the "postgres" user. |
| | || **Key**         | PerconaPGCluster.spec.users[index].options |
| **Value**       | string |
| **Required**    | false |
| **Example**     | |
| **Description** | ALTER ROLE options except for PASSWORD. This field is ignored for the "postgres" user. More info: https://www.postgresql.org/docs/current/role-attributes.html |
| | || **Key**         | PerconaPGCluster.spec.users[index].password |
| **Value**       | object |
| **Required**    | false |
| **Example**     | |
| **Description** | Properties of the password generated for this user. |
| | |
| **Key**         | PerconaPGCluster.spec.users[index].password.type |
| **Value**       | enum |
| **Required**    | true |
| **Example**     | |
| **Description** | Type of password to generate. Defaults to ASCII. Valid options are ASCII and AlphaNumeric. "ASCII" passwords contain letters, numbers, and symbols from the US-ASCII character set. "AlphaNumeric" passwords contain letters and numbers from the US-ASCII character set. |
| | |
| **Key**         | PerconaPGCluster.status.conditions |
| **Value**       | []object |
| **Required**    | false |
| **Example**     | |
| **Description** | conditions represent the observations of postgrescluster's current state. Known .status.conditions.type are: "PersistentVolumeResizing", "Progressing", "ProxyAvailable" |
| | || **Key**         | PerconaPGCluster.status.databaseInitSQL |
| **Value**       | string |
| **Required**    | false |
| **Example**     | |
| **Description** | DatabaseInitSQL state of custom database initialization in the cluster |
| | || **Key**         | PerconaPGCluster.status.databaseRevision |
| **Value**       | string |
| **Required**    | false |
| **Example**     | |
| **Description** | Identifies the databases that have been installed into PostgreSQL. |
| | || **Key**         | PerconaPGCluster.status.instances |
| **Value**       | []object |
| **Required**    | false |
| **Example**     | |
| **Description** | Current state of PostgreSQL instances. |
| | || **Key**         | PerconaPGCluster.status.monitoring |
| **Value**       | object |
| **Required**    | false |
| **Example**     | |
| **Description** | Current state of PostgreSQL cluster monitoring tool configuration |
| | || **Key**         | PerconaPGCluster.status.observedGeneration |
| **Value**       | integer |
| **Required**    | false |
| **Example**     | |
| **Description** | observedGeneration represents the .metadata.generation on which the status was based. |
| | || **Key**         | PerconaPGCluster.status.patroni |
| **Value**       | object |
| **Required**    | false |
| **Example**     | |
| **Description** |  |
| | || **Key**         | PerconaPGCluster.status.pgbackrest |
| **Value**       | object |
| **Required**    | false |
| **Example**     | |
| **Description** | Status information for pgBackRest |
| | || **Key**         | PerconaPGCluster.status.postgresVersion |
| **Value**       | integer |
| **Required**    | false |
| **Example**     | |
| **Description** | Stores the current PostgreSQL major version following a successful major PostgreSQL upgrade. |
| | || **Key**         | PerconaPGCluster.status.proxy |
| **Value**       | object |
| **Required**    | false |
| **Example**     | |
| **Description** | Current state of the PostgreSQL proxy. |
| | || **Key**         | PerconaPGCluster.status.startupInstance |
| **Value**       | string |
| **Required**    | false |
| **Example**     | |
| **Description** | The instance that should be started first when bootstrapping and/or starting a PostgresCluster. |
| | || **Key**         | PerconaPGCluster.status.startupInstanceSet |
| **Value**       | string |
| **Required**    | false |
| **Example**     | |
| **Description** | The instance set associated with the startupInstance |
| | || **Key**         | PerconaPGCluster.status.userInterface |
| **Value**       | object |
| **Required**    | false |
| **Example**     | |
| **Description** | Current state of the PostgreSQL user interface. |
| | || **Key**         | PerconaPGCluster.status.usersRevision |
| **Value**       | string |
| **Required**    | false |
| **Example**     | |
| **Description** | Identifies the users that have been installed into PostgreSQL. |
| | |
| **Key**         | PerconaPGCluster.status.conditions[index].lastTransitionTime |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | lastTransitionTime is the last time the condition transitioned from one status to another. This should be when the underlying condition changed.  If that is not known, then using the time when the API field changed is acceptable. |
| | || **Key**         | PerconaPGCluster.status.conditions[index].message |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | message is a human readable message indicating details about the transition. This may be an empty string. |
| | || **Key**         | PerconaPGCluster.status.conditions[index].reason |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | reason contains a programmatic identifier indicating the reason for the condition's last transition. Producers of specific condition types may define expected values and meanings for this field, and whether the values are considered a guaranteed API. The value should be a CamelCase string. This field may not be empty. |
| | || **Key**         | PerconaPGCluster.status.conditions[index].status |
| **Value**       | enum |
| **Required**    | true |
| **Example**     | |
| **Description** | status of the condition, one of True, False, Unknown. |
| | || **Key**         | PerconaPGCluster.status.conditions[index].type |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | type of condition in CamelCase or in foo.example.com/CamelCase. --- Many .condition.type values are consistent across resources like Available, but because arbitrary conditions can be useful (see .node.status.conditions), the ability to deconflict is important. The regex it matches is (dns1123SubdomainFmt/)?(qualifiedNameFmt) |
| | || **Key**         | PerconaPGCluster.status.conditions[index].observedGeneration |
| **Value**       | integer |
| **Required**    | false |
| **Example**     | |
| **Description** | observedGeneration represents the .metadata.generation that the condition was set based upon. For instance, if .metadata.generation is currently 12, but the .status.conditions[x].observedGeneration is 9, the condition is out of date with respect to the current state of the instance. |
| | |
| **Key**         | PerconaPGCluster.status.instances[index].name |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** |  |
| | || **Key**         | PerconaPGCluster.status.instances[index].readyReplicas |
| **Value**       | integer |
| **Required**    | false |
| **Example**     | |
| **Description** | Total number of ready pods. |
| | || **Key**         | PerconaPGCluster.status.instances[index].replicas |
| **Value**       | integer |
| **Required**    | false |
| **Example**     | |
| **Description** | Total number of pods. |
| | || **Key**         | PerconaPGCluster.status.instances[index].updatedReplicas |
| **Value**       | integer |
| **Required**    | false |
| **Example**     | |
| **Description** | Total number of pods that have the desired specification. |
| | |
| **Key**         | PerconaPGCluster.status.monitoring.exporterConfiguration |
| **Value**       | string |
| **Required**    | false |
| **Example**     | |
| **Description** |  |
| | |
| **Key**         | PerconaPGCluster.status.patroni.switchover |
| **Value**       | string |
| **Required**    | false |
| **Example**     | |
| **Description** | Tracks the execution of the switchover requests. |
| | || **Key**         | PerconaPGCluster.status.patroni.switchoverTimeline |
| **Value**       | integer |
| **Required**    | false |
| **Example**     | |
| **Description** | Tracks the current timeline during switchovers |
| | || **Key**         | PerconaPGCluster.status.patroni.systemIdentifier |
| **Value**       | string |
| **Required**    | false |
| **Example**     | |
| **Description** | The PostgreSQL system identifier reported by Patroni. |
| | |
| **Key**         | PerconaPGCluster.status.pgbackrest.manualBackup |
| **Value**       | object |
| **Required**    | false |
| **Example**     | |
| **Description** | Status information for manual backups |
| | || **Key**         | PerconaPGCluster.status.pgbackrest.repoHost |
| **Value**       | object |
| **Required**    | false |
| **Example**     | |
| **Description** | Status information for the pgBackRest dedicated repository host |
| | || **Key**         | PerconaPGCluster.status.pgbackrest.repos |
| **Value**       | []object |
| **Required**    | false |
| **Example**     | |
| **Description** | Status information for pgBackRest repositories |
| | || **Key**         | PerconaPGCluster.status.pgbackrest.restore |
| **Value**       | object |
| **Required**    | false |
| **Example**     | |
| **Description** | Status information for in-place restores |
| | || **Key**         | PerconaPGCluster.status.pgbackrest.scheduledBackups |
| **Value**       | []object |
| **Required**    | false |
| **Example**     | |
| **Description** | Status information for scheduled backups |
| | |
| **Key**         | PerconaPGCluster.status.pgbackrest.manualBackup.finished |
| **Value**       | boolean |
| **Required**    | true |
| **Example**     | |
| **Description** | Specifies whether or not the Job is finished executing (does not indicate success or failure). |
| | || **Key**         | PerconaPGCluster.status.pgbackrest.manualBackup.id |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | A unique identifier for the manual backup as provided using the "pgbackrest-backup" annotation when initiating a backup. |
| | || **Key**         | PerconaPGCluster.status.pgbackrest.manualBackup.active |
| **Value**       | integer |
| **Required**    | false |
| **Example**     | |
| **Description** | The number of actively running manual backup Pods. |
| | || **Key**         | PerconaPGCluster.status.pgbackrest.manualBackup.completionTime |
| **Value**       | string |
| **Required**    | false |
| **Example**     | |
| **Description** | Represents the time the manual backup Job was determined by the Job controller to be completed.  This field is only set if the backup completed successfully. Additionally, it is represented in RFC3339 form and is in UTC. |
| | || **Key**         | PerconaPGCluster.status.pgbackrest.manualBackup.failed |
| **Value**       | integer |
| **Required**    | false |
| **Example**     | |
| **Description** | The number of Pods for the manual backup Job that reached the "Failed" phase. |
| | || **Key**         | PerconaPGCluster.status.pgbackrest.manualBackup.startTime |
| **Value**       | string |
| **Required**    | false |
| **Example**     | |
| **Description** | Represents the time the manual backup Job was acknowledged by the Job controller. It is represented in RFC3339 form and is in UTC. |
| | || **Key**         | PerconaPGCluster.status.pgbackrest.manualBackup.succeeded |
| **Value**       | integer |
| **Required**    | false |
| **Example**     | |
| **Description** | The number of Pods for the manual backup Job that reached the "Succeeded" phase. |
| | |
| **Key**         | PerconaPGCluster.status.pgbackrest.repoHost.apiVersion |
| **Value**       | string |
| **Required**    | false |
| **Example**     | |
| **Description** | APIVersion defines the versioned schema of this representation of an object. Servers should convert recognized schemas to the latest internal value, and may reject unrecognized values. More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources |
| | || **Key**         | PerconaPGCluster.status.pgbackrest.repoHost.kind |
| **Value**       | string |
| **Required**    | false |
| **Example**     | |
| **Description** | Kind is a string value representing the REST resource this object represents. Servers may infer this from the endpoint the client submits requests to. Cannot be updated. In CamelCase. More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#types-kinds |
| | || **Key**         | PerconaPGCluster.status.pgbackrest.repoHost.ready |
| **Value**       | boolean |
| **Required**    | false |
| **Example**     | |
| **Description** | Whether or not the pgBackRest repository host is ready for use |
| | |
| **Key**         | PerconaPGCluster.status.pgbackrest.repos[index].name |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | The name of the pgBackRest repository |
| | || **Key**         | PerconaPGCluster.status.pgbackrest.repos[index].bound |
| **Value**       | boolean |
| **Required**    | false |
| **Example**     | |
| **Description** | Whether or not the pgBackRest repository PersistentVolumeClaim is bound to a volume |
| | || **Key**         | PerconaPGCluster.status.pgbackrest.repos[index].replicaCreateBackupComplete |
| **Value**       | boolean |
| **Required**    | false |
| **Example**     | |
| **Description** | ReplicaCreateBackupReady indicates whether a backup exists in the repository as needed to bootstrap replicas. |
| | || **Key**         | PerconaPGCluster.status.pgbackrest.repos[index].repoOptionsHash |
| **Value**       | string |
| **Required**    | false |
| **Example**     | |
| **Description** | A hash of the required fields in the spec for defining an Azure, GCS or S3 repository, Utilizd to detect changes to these fields and then execute pgBackRest stanza-create commands accordingly. |
| | || **Key**         | PerconaPGCluster.status.pgbackrest.repos[index].stanzaCreated |
| **Value**       | boolean |
| **Required**    | false |
| **Example**     | |
| **Description** | Specifies whether or not a stanza has been successfully created for the repository |
| | || **Key**         | PerconaPGCluster.status.pgbackrest.repos[index].volume |
| **Value**       | string |
| **Required**    | false |
| **Example**     | |
| **Description** | The name of the volume the containing the pgBackRest repository |
| | |
| **Key**         | PerconaPGCluster.status.pgbackrest.restore.finished |
| **Value**       | boolean |
| **Required**    | true |
| **Example**     | |
| **Description** | Specifies whether or not the Job is finished executing (does not indicate success or failure). |
| | || **Key**         | PerconaPGCluster.status.pgbackrest.restore.id |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | A unique identifier for the manual backup as provided using the "pgbackrest-backup" annotation when initiating a backup. |
| | || **Key**         | PerconaPGCluster.status.pgbackrest.restore.active |
| **Value**       | integer |
| **Required**    | false |
| **Example**     | |
| **Description** | The number of actively running manual backup Pods. |
| | || **Key**         | PerconaPGCluster.status.pgbackrest.restore.completionTime |
| **Value**       | string |
| **Required**    | false |
| **Example**     | |
| **Description** | Represents the time the manual backup Job was determined by the Job controller to be completed.  This field is only set if the backup completed successfully. Additionally, it is represented in RFC3339 form and is in UTC. |
| | || **Key**         | PerconaPGCluster.status.pgbackrest.restore.failed |
| **Value**       | integer |
| **Required**    | false |
| **Example**     | |
| **Description** | The number of Pods for the manual backup Job that reached the "Failed" phase. |
| | || **Key**         | PerconaPGCluster.status.pgbackrest.restore.startTime |
| **Value**       | string |
| **Required**    | false |
| **Example**     | |
| **Description** | Represents the time the manual backup Job was acknowledged by the Job controller. It is represented in RFC3339 form and is in UTC. |
| | || **Key**         | PerconaPGCluster.status.pgbackrest.restore.succeeded |
| **Value**       | integer |
| **Required**    | false |
| **Example**     | |
| **Description** | The number of Pods for the manual backup Job that reached the "Succeeded" phase. |
| | |
| **Key**         | PerconaPGCluster.status.pgbackrest.scheduledBackups[index].active |
| **Value**       | integer |
| **Required**    | false |
| **Example**     | |
| **Description** | The number of actively running manual backup Pods. |
| | || **Key**         | PerconaPGCluster.status.pgbackrest.scheduledBackups[index].completionTime |
| **Value**       | string |
| **Required**    | false |
| **Example**     | |
| **Description** | Represents the time the manual backup Job was determined by the Job controller to be completed.  This field is only set if the backup completed successfully. Additionally, it is represented in RFC3339 form and is in UTC. |
| | || **Key**         | PerconaPGCluster.status.pgbackrest.scheduledBackups[index].cronJobName |
| **Value**       | string |
| **Required**    | false |
| **Example**     | |
| **Description** | The name of the associated pgBackRest scheduled backup CronJob |
| | || **Key**         | PerconaPGCluster.status.pgbackrest.scheduledBackups[index].failed |
| **Value**       | integer |
| **Required**    | false |
| **Example**     | |
| **Description** | The number of Pods for the manual backup Job that reached the "Failed" phase. |
| | || **Key**         | PerconaPGCluster.status.pgbackrest.scheduledBackups[index].repo |
| **Value**       | string |
| **Required**    | false |
| **Example**     | |
| **Description** | The name of the associated pgBackRest repository |
| | || **Key**         | PerconaPGCluster.status.pgbackrest.scheduledBackups[index].startTime |
| **Value**       | string |
| **Required**    | false |
| **Example**     | |
| **Description** | Represents the time the manual backup Job was acknowledged by the Job controller. It is represented in RFC3339 form and is in UTC. |
| | || **Key**         | PerconaPGCluster.status.pgbackrest.scheduledBackups[index].succeeded |
| **Value**       | integer |
| **Required**    | false |
| **Example**     | |
| **Description** | The number of Pods for the manual backup Job that reached the "Succeeded" phase. |
| | || **Key**         | PerconaPGCluster.status.pgbackrest.scheduledBackups[index].type |
| **Value**       | string |
| **Required**    | false |
| **Example**     | |
| **Description** | The pgBackRest backup type for this Job |
| | |
| **Key**         | PerconaPGCluster.status.proxy.pgBouncer |
| **Value**       | object |
| **Required**    | false |
| **Example**     | |
| **Description** |  |
| | |
| **Key**         | PerconaPGCluster.status.proxy.pgBouncer.postgresRevision |
| **Value**       | string |
| **Required**    | false |
| **Example**     | |
| **Description** | Identifies the revision of PgBouncer assets that have been installed into PostgreSQL. |
| | || **Key**         | PerconaPGCluster.status.proxy.pgBouncer.readyReplicas |
| **Value**       | integer |
| **Required**    | false |
| **Example**     | |
| **Description** | Total number of ready pods. |
| | || **Key**         | PerconaPGCluster.status.proxy.pgBouncer.replicas |
| **Value**       | integer |
| **Required**    | false |
| **Example**     | |
| **Description** | Total number of non-terminated pods. |
| | |
| **Key**         | PerconaPGCluster.status.userInterface.pgAdmin |
| **Value**       | object |
| **Required**    | false |
| **Example**     | |
| **Description** | The state of the pgAdmin user interface. |
| | |
| **Key**         | PerconaPGCluster.status.userInterface.pgAdmin.usersRevision |
| **Value**       | string |
| **Required**    | false |
| **Example**     | |
| **Description** | Hash that indicates which users have been installed into pgAdmin. |
| | |

<h2 id="perconapgbackup">PerconaPGBackup</h2>

|                 | |
|-----------------|-|

| **Key**         | PerconaPGBackup.spec |
| **Value**       | object |
| **Required**    | true |
| **Example**     | |
| **Description** |  |
| | || **Key**         | PerconaPGBackup.status |
| **Value**       | object |
| **Required**    | false |
| **Example**     | |
| **Description** |  |
| | |
| **Key**         | PerconaPGBackup.spec.pgCluster |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** |  |
| | || **Key**         | PerconaPGBackup.spec.repoName |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | The name of the pgBackRest repo to run the backup command against. |
| | || **Key**         | PerconaPGBackup.spec.options |
| **Value**       | []string |
| **Required**    | false |
| **Example**     | |
| **Description** | Command line options to include when running the pgBackRest backup command. https://pgbackrest.org/command.html#command-backup |
| | |
| **Key**         | PerconaPGBackup.status.completed |
| **Value**       | string |
| **Required**    | false |
| **Example**     | |
| **Description** |  |
| | || **Key**         | PerconaPGBackup.status.jobName |
| **Value**       | string |
| **Required**    | false |
| **Example**     | |
| **Description** |  |
| | || **Key**         | PerconaPGBackup.status.state |
| **Value**       | string |
| **Required**    | false |
| **Example**     | |
| **Description** |  |
| | |

<h2 id="perconapgrestore">PerconaPGRestore</h2>

|                 | |
|-----------------|-|

| **Key**         | PerconaPGRestore.spec |
| **Value**       | object |
| **Required**    | true |
| **Example**     | |
| **Description** |  |
| | || **Key**         | PerconaPGRestore.status |
| **Value**       | object |
| **Required**    | false |
| **Example**     | |
| **Description** |  |
| | |
| **Key**         | PerconaPGRestore.spec.pgCluster |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | The name of the PerconaPGCluster to perform restore. |
| | || **Key**         | PerconaPGRestore.spec.repoName |
| **Value**       | string |
| **Required**    | true |
| **Example**     | |
| **Description** | The name of the pgBackRest repo within the source PostgresCluster that contains the backups that should be utilized to perform a pgBackRest restore when initializing the data source for the new PostgresCluster. |
| | || **Key**         | PerconaPGRestore.spec.options |
| **Value**       | []string |
| **Required**    | false |
| **Example**     | |
| **Description** | Command line options to include when running the pgBackRest restore command. https://pgbackrest.org/command.html#command-restore |
| | |
| **Key**         | PerconaPGRestore.status.completed |
| **Value**       | string |
| **Required**    | false |
| **Example**     | |
| **Description** |  |
| | || **Key**         | PerconaPGRestore.status.jobName |
| **Value**       | string |
| **Required**    | false |
| **Example**     | |
| **Description** |  |
| | || **Key**         | PerconaPGRestore.status.state |
| **Value**       | string |
| **Required**    | false |
| **Example**     | |
| **Description** |  |
| | |
