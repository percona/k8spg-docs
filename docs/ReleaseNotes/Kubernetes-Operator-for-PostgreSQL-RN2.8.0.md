# Percona Operator for PostgreSQL 2.8.0 ({{date.2_8_0}})

[Get started with the Operator :material-arrow-right:](../quickstart.md){.md-button}

## Release Highlights

This release provides the following features and improvements:

### Custom PostgreSQL user credentials now fully respected by the Operator

You no longer have to define full login and connection information within a Secret to have the Operator use it. Now you can set only the password. The Operator generates the missing details that it needs automatically using the values from the Custom Resource. Also, if you name your Secret in the format that the Operator expects such as `<clusterName>-pguser-<userName>` — the Operator will automatically detect and use it without needing an explicit reference in the Custom Resource.  

However, if you choose a custom name for the Secret, you must still reference it explicitly in the Custom Resource under the `users[].secretName` field. This ensures the Operator can locate and apply it correctly.

This enhancement makes the management of user credentials more straightforward.

### Ability to use huge pages

PostgreSQL can now use huge pages if they are enabled for your Kubernetes cluster. Instruct the Operator to use huge pages when deploying a PostgreSQL cluster with this configuration:

```yaml
spec:
  instances:
    - name: instance1
      resources:
        limits:
          hugepages-2Mi: 16Mi
          memory: 4Gi
```

This improvement leads to a more efficient memory utilization and improved performance.

### Expanded S3 compatibility for custom extensions 

Some S3-compatible services (like MinIO or Ceph) require path-style access instead of virtual-hosted style. Or they may use self-signed certificates or not support TLS.

To address these issues, you can now fine-tune the Operator with these new options:

* `forcePathStyle` enforces path-style access instead of virtual-hosted style

* `disableSSL` disables SSL verification to allow successful downloads.

```yaml
extensions:
    image: docker.io/perconalab/percona-postgresql-operator:main
    storage:
      .....
      forcePathStyle: false
      disableSSL: false
```

These options give you greater control and flexibility when configuring access to an S3 storage for using custom extensions.

### Changed Patroni version management

The Operator no longer runs a temporary Pod `cluster_name-patroni-version-check` to identify the Patroni version during cluster initialization. 

Instead, it uses the `patronictl` CLI tool to connect to a database Pod and detect the Patroni version. The detected version is recorded in the `pgv2.percona.com/patroni-version` annotation on the cluster resource and is added to the resource status.

The Operator standardizes on Patroni 4 as the only supported version and no longer honors Patroni version overrides via the `pgv2.percona.com/custom-patroni-version` annotation.

However, if your Custom Resource is still at version 2.7.0, the Operator 2.8.0 will continue to run a temporary Pod to check Patroni version and use Patroni 3 if specified via the annotation for backward compatibility. But after you upgrade the Custom Resource to version 2.8.0, the `pgv2.percona.com/custom-patroni-version `annotation is ignored, and Patroni 4 is always used.

This change eliminates ambiguity and ensures your cluster is deployed with a modern high-availability implementation.

## Changelog

### New features

* [K8SPG-730](https://perconadev.atlassian.net/browse/K8SPG-730) - Added the  `status.observedGeneration` field to the Custom Resource Definition to improve observability and ensure the controller successfully reconciled the latest changes to the cluster.

* [K8SPG-752](https://perconadev.atlassian.net/browse/K8SPG-752) - Allowed setting `loadBalancerClass` service type and using a custom implementation of a load balancer rather than the cloud provider default one.

INTERNAL TASK [K8SPG-768](https://perconadev.atlassian.net/browse/K8SPG-768) Introduced a mechanism to prevent excessive logging caused by continuous pod annotation updates for suggested volume sizing. The Operator now skips updating the Pod annotation with the suggested volume size unless the auto-growable disk feature is explicitly configured. This significantly reduces redundant logs and unnecessary load on both the Kubernetes API and the logging pipeline.

* [K8SPG-832](https://perconadev.atlassian.net/browse/K8SPG-832) - Users can now specify custom sidecar containers for the `repo-host` Pod, enabling seamless integration with external tools, storage systems, or observability agents. This enhances flexibility in backup workflows without modifying the Operator’s core logic.

* [K8SPG-833](https://perconadev.atlassian.net/browse/K8SPG-833) - Added the ability to define custom environment variables across all components. This enables tighter integration with external systems, secrets, or runtime configurations.

### Improvements

* [K8SPG-460](https://perconadev.atlassian.net/browse/K8SPG-460) - The Operator now correctly enables and used Huge pages functionality if they are enabled on the OS level.
* [K8SPG-570](https://perconadev.atlassian.net/browse/K8SPG-570) - The Operator now correctly respects custom user passwords defined in secrets when creating new users, and automatically adds any missing credentials.

* [K8SPG-611](https://perconadev.atlassian.net/browse/K8SPG-611) - The operator now uses official Percona PostgreSQL docker images, which are compatible only with specific latest PostgreSQL versions.

* [K8SPG-624](https://perconadev.atlassian.net/browse/K8SPG-624), [K8SPG-728](https://perconadev.atlassian.net/browse/K8SPG-728) - Added the ability to configure the Operator to use path-style access to S3 storage or skip TLS verification to ensure broader compatibility with S3 storage services.

* [K8SPG-718](https://perconadev.atlassian.net/browse/K8SPG-718) - Improved Patroni observability by sending Patroni metrics to PMM.

* [K8SPG-748](https://perconadev.atlassian.net/browse/K8SPG-748) - The PerconaPGCluster status now provides more comprehensive details, including persistent volume resizing and pgBackRest backup conditions.

* [K8SPG-752](https://perconadev.atlassian.net/browse/K8SPG-752)- Allowed setting loadBalancerClass service type and use a custom implementation of a load balancer rather than the cloud provider default one.

* [K8SPG-757](https://perconadev.atlassian.net/browse/K8SPG-757): The Percona PostgreSQL Operator now successfully deploys in environments where `readOnlyRootFilesystem` is enforced.
* [K8SPG-874](https://perconadev.atlassian.net/browse/K8SPG-874)- Improved logging to no longer contain backup-related information when backups are disabled.

* [K8SPG-882](https://perconadev.atlassian.net/browse/K8SPG-882) - The operator no longer deploys a temporary Patroni version check pod, as it now detects the version directly from running database instances.

### Fixed bugs

??? Open - [K8SPG-688](https://perconadev.atlassian.net/browse/K8SPG-688): The operator no longer crashes when updated without first upgrading its Custom Resource Definition (CRD).

- [K8SPG-724](https://perconadev.atlassian.net/browse/K8SPG-724) - Fixed the issue with upgrading custom extension versions. The Operator now correctly uninstalls old versions and installs new ones automatically.

- [K8SPG-777](https://perconadev.atlassian.net/browse/K8SPG-777) - Custom Resource `crVersion` is now automatically assigned if not explicitly defined.

- [K8SPG-778](https://perconadev.atlassian.net/browse/K8SPG-778) -  Backup restores no longer fail due to empty repository name errors during the finalization process.
- [K8SPG-781](https://perconadev.atlassian.net/browse/K8SPG-781)- Error messages for primary pod issues now reveal the specific underlying problem instead of a generic message.
- [K8SPG-803](https://perconadev.atlassian.net/browse/K8SPG-803) -  Outdated backups are now correctly cleaned up, even when pgBackRest debug logging is enabled.
- [K8SPG-826](https://perconadev.atlassian.net/browse/K8SPG-826) - Fixed the issue with cluster monitoring on OpenShift by using the correct folder for PMM3 .
- [K8SPG-835](https://perconadev.atlassian.net/browse/K8SPG-835) - Improved affinity behavior for `patroni-version-check` pod
- [K8SPG-844](https://perconadev.atlassian.net/browse/K8SPG-844) - Fixed the issue with the Operator overriding user configuration with archive commands when the latest restorable time tracking disabled by fully respecting user configuration.
- [K8SPG-869](https://perconadev.atlassian.net/browse/K8SPG-869) - A backup repository is no longer required when configuring a cluster with disabled backups.
- [K8SPG-872](https://perconadev.atlassian.net/browse/K8SPG-872) - Updated DNS records used in certificates to no longer include a trailing period to comply with updated validation standards.
??? In progress - [K8SPG-876](https://perconadev.atlassian.net/browse/K8SPG-876): Fixed an issue where PostgreSQL clusters remained in an "Initialized" state after restoring an S3 backup.
- [K8SPG-879](https://perconadev.atlassian.net/browse/K8SPG-879) - Clusters can now be created successfully on Kubernetes version 1.34.

* [K8SPG-883](https://perconadev.atlassian.net/browse/K8SPG-883): Patroni version information is now displayed in the `status.patroni.version` field instead of `status.patroniVersion `.

- [K8SPG-884](https://perconadev.atlassian.net/browse/K8SPG-884) - Clusters deployed with PostgreSQL 13 now correctly support the `pg_stat_statements` extension.

### Documentation improvements

* Refined the Upgrade guide structure, moving instructions for updating built-in extensions under the Database upgrade section for better clarity.
*  Improved documentation for generating custom TLS certificates used by your cluster and added steps how to safely renew or replace your certificate authorities and secrets.
* Enhanced the Adding custom extensions documentation by including a sample configuration for a custom extension, illustrating the overall workflow as a practical reference.
* Improved the Upgrade document with the steps to change collation version is there is a collation mismatch.
* PostGIS image documentation now accurately reflects the available versions.

## Deprecation, Change, Rename and Removal

* The `patroni.patroniVersion` field in Custom Resource Definition is deprecated and will be removed in future releases. Starting with version 2.8.0, the Operator uses the `patroni.version` field in Custom Resource Definition to populate Patroni version.

   ```yaml
   patroni:
     status:
       systemIdentifier: "7569216022115639385"
     version: 4.0.6
   ```

   Adjust your applications or scripts accordingly to this change if they rely on Patroni version information.

* New fields in the Custom Resource Definition:
   
   * `status.observedGeneration` to track whether the controller has successfully applied the latest changes to the custom resource
   * `patroni` subsection contains these fields for Patroni state: 
      
      * `patroni.version` 
      * `patroni.systemIdentifier`
      * `patroni.switchover`
      * `patroni.switchoverTimeline`

   * `pgBackRest` subsection contains these fields to track the status of backup repository and backup jobs:
      
      * `pgBackRest.manualBackup`
      * `pgBackRest.repoHost`
      * `pgBackRest.repos`

## Supported software

The Operator {{ release }} is developed, tested and based on:

--8<-- [start:software]

* PostgreSQL 13.22, 14.19, 15.14, 16.10, 17.6 as the database. Other versions may also work but have not been tested.
* pgBouncer 1.24.1 for connection pooling
* Patroni version 4.6.0 for high-availability
* PostGIS version 3.3.8

--8<-- [end:software]

## Supported platforms

Percona Operators are designed for compatibility with all [CNCF-certified :octicons-link-external-16:](https://www.cncf.io/training/certification/software-conformance/) Kubernetes distributions. 

Our release process includes targeted testing and validation on major cloud provider platforms and OpenShift, as detailed below for Operator version {{release}}:

--8<-- [start:platforms]

* [Google Kubernetes Engine (GKE) :octicons-link-external-16:](https://cloud.google.com/kubernetes-engine) 1.31 - 1.33
* [Amazon Elastic Container Service for Kubernetes (EKS) :octicons-link-external-16:](https://aws.amazon.com) 1.31 - 1.34
* [OpenShift :octicons-link-external-16:](https://www.redhat.com/en/technologies/cloud-computing/openshift) 4.16 - 4.20
* [Azure Kubernetes Service (AKS) :octicons-link-external-16:](https://azure.microsoft.com/en-us/services/kubernetes-service/) 1.32 - 1.34
* [Minikube :octicons-link-external-16:](https://github.com/kubernetes/minikube) 1.37.0 with Kubernetes v1.34.0

--8<-- [end:platforms]

This list only includes the platforms that the Percona Operators are specifically tested on as part of the release process. Other Kubernetes flavors and versions depend on the backward compatibility offered by Kubernetes itself.

## Percona certified images

Find Percona’s certified Docker images that you can use with the Percona Operator for PostgreSQL in the following table.

Images released with the Operator version {{release}}: 

--8<-- [start:images]

| Image                                                                 | Digest                                                           |
|:----------------------------------------------------------------------|:-----------------------------------------------------------------|
| percona/percona-postgresql-operator:2.7.0 (x86_64)                    | 96e4e3d7e4bcbd4880adebc5ccb958c0f4385298f0becdef2eb14b81fab407e5 |
| percona/percona-postgresql-operator:2.7.0 (ARM64)                     | 055da3233a7765f22b318c97223909c20ecbbc9f34c6a8f7845d04ade51364ca |
| percona/percona-postgresql-operator:2.7.0-ppg17.5.2-postgres           | cfb99ebeec00ab6efb4fca4a8da2b8c3b489dd792bd2f907848197ba09bc9553 |
| percona/percona-postgresql-operator:2.7.0-ppg16.9-postgres             | 0787088575b4e4fec368acbcf4dd7aea49620ec4524451e3b44ed424fb0eeebb |
| percona/percona-postgresql-operator:2.7.0-ppg15.13-postgres            | c93f52ea1d6ec955a368c4539b843a9c57ee4a5acc907f0dfb59ae3018560d1b |
| percona/percona-postgresql-operator:2.7.0-ppg14.18-postgres            | a24059edd9864f7dc9607c3e2964844f417718a5b9f471ceb98c0a0d774a4bca |
| percona/percona-postgresql-operator:2.7.0-ppg13.21-postgres            | 2c9a05399b34cfe79698bdaab66db8fdaece0db7b1fa34441124cccdbe375255 |
| percona/percona-postgresql-operator:2.7.0-ppg17.5.2-postgres-gis3.3.8  | 860ccc180c1ac6be3c34c354d6ba9148b00330e183ba5913954e34d49c95d22f |
| percona/percona-postgresql-operator:2.7.0-ppg16.9-postgres-gis3.3.8    | ca50f560bc7b3e18ec3360dc1a6b8c860e0346472af051cb0d2aec2a7a45d8b3 |
| percona/percona-postgresql-operator:2.7.0-ppg15.13-postgres-gis3.3.8   | bb6707fd12ea430708e2eb22f6c7dadf3ab4258fcfd31e86f1f78c66ba211742 |
| percona/percona-postgresql-operator:2.7.0-ppg14.18-postgres-gis3.3.8   | c3b55d1394d8f0a476cea29340442313c9c08dcd8c83f31ccfc66afdbde42488 |
| percona/percona-postgresql-operator:2.7.0-ppg13.21-postgres-gis3.3.8   | 3df44c1089563b42198ef929e27b9797ef2b04d92736293952163fa7541c0068 |
| percona/percona-pgbouncer:1.24.1                                       | 451431afa3cd288ecda92b6446bec8833fbf376fbd1b7c7e314fc42f3355255f |
| percona/percona-pgbouncer:1.24.1 (ARM64)                               | 479aa893e55c5afe8b97852c90d7551dc55d3fc526773a5a7d992876bbf54cb0 |
| percona/percona-pgbackrest:2.55.0                                      | b0d2defbc7a07cf395b1fa6c6e13d9d3267c3a2d3c52362ac440db26ea4a4bad |
| percona/percona-pgbackrest:2.55.0 (ARM64)                              | bc15d058e7820499bf67ccec2fe51c583fe67a6e3ed55ec28adf3e252828924a |
| percona/pmm-client:2.44.1                                               | 8b2eaddffd626f02a2d5318ffebc0c277fe8457da6083b8cfcada9b6e6168616 |
| percona/pmm-client:2.44.1 (ARM64)                                     | 337fecd4afdb3f6daf2caa2b341b9fe41d0418a0e4ec76980c7f29be9d08b5ea |
| percona/pmm-client:3.3.0                                               | 0f4ef6a814946f83ef1ed26cf3526ff606fc7815007f84995492d3e4eaa15a0e |
| percona/pmm-client:3.3.0 (ARM64)                                       | c03aa678d26faf783c3598b3a139a8f3154e5bf1bc9f5a3c9abf0533922f79d6 |

--8<-- [end:images]
