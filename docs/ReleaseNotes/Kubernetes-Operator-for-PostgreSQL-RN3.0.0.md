# Percona Operator for PostgreSQL 3.0.0 ({{date.3_0_0}})

[Get started with the Operator :material-arrow-right:](../quickstart.md){.md-button}

We are excited to announce the release of Percona Operator for PostgreSQL 3.0.0 — a new major release that marks a new chapter for the Operator and everyone who relies on it.

As of version 3.0.0, Percona Operator for PostgreSQL becomes a **hard fork of the [Crunchy PGO project :octicons-link-external-16:](https://github.com/CrunchyData/postgres-operator)**. This marks a significant change in how the Operator is built and maintained going forward.

As a hard fork, Percona Operator for PostgreSQL is now fully independent, empowering the Percona team and community to drive and rapidly deliver features and improvements tailored to user needs. This shift brings long-term sustainability, greater flexibility, and a product that evolves in direct response to community feedback and real-world requirements.

## Release highlights

### Crunchy CRD renaming and seamless resource migration

With this release, all Crunchy CRDs are renamed and moved under a new API group `upstream.pgv2.percona.com`. All references to Crunchy CRDs in dependent objects, such as Custom Resources, Deployments, Secrets, ConfigMaps, Jobs, and so on, are updated accordingly.

When you update from the earlier Operator versions to 3.0.0 and newer, new API group CRDs are created alongside the legacy CRDs to keep existing workflows uninterrupted. Then the Operator automatically migrates all resources that depend on the legacy CRDs to the new API group. No manual intervention is required.

!!! important

    As part of the API group migration, the common name in the `pgBackRest` client certificate is updated. The Operator automatically updates both the `pgBackRest` configuration and the related certificate Secret. However, you may experience brief disruptions to `pgBackRest` operations while Kubernetes propagates these changes to the containers. This process typically completes within 1–2 minutes.

The migration event is recorded in cluster conditions and logs, so you have full visibility into what happened and when.

This change delivers these benefits:

* Safe coexistence of Percona Operator for PostgreSQL and Crunchy PGO
* Cleaner API boundaries and predictable Operator behavior
* Smooth migration from Crunchy Operator to Percona Operator using native PostgreSQL techniques and without re-architecting your deployments

For how to migrate to Percona Operator from Crunchy PGO, see our [documentaton](../migration-from-crunchy.md).

### Improved namespace scoping for Operator OLM installations from Community catalogues

When you install the Operator from a Community catalogue through OpenShift Lifecycle Manager (OLM), it now honors the namespace scope as defined by its `OperatorGroup` settings:

* **All namespaces** — The Operator watches all namespaces, as intended for this mode. In earlier releases, it watched only its own installation namespace, which left PostgreSQL custom resources in other namespaces unmanaged.
* **Single namespace** — The Operator watches only the namespaces listed for the `OperatorGroup` (`olm.targetNamespaces`), so a scoped install stays scoped.

With this change, you get the same namespace coverage your subscription mode promises, so clusters behave the way OpenShift administrators expect.

After you upgrade, the Operator may begin reconciling Percona PostgreSQL custom resources that already exist in namespaces it previously ignored. That is most common when several Operators run in one OpenShift cluster, all in all-namespaces mode, and each installation now actually honors that mode.

Before you upgrade, confirm how the Operator is installed by inspecting the `OperatorGroup`: a single entry under `spec.targetNamespaces` means single-namespace mode; an empty value means all-namespaces mode.

To limit which namespaces an Operator reconciles, set `spec.targetNamespaces` explicitly:

```yaml
spec:
  targetNamespaces:
    - "<namespace-1>"
    - "<namespace-2>"
```

If you run more than one Operator in the same cluster, switch each one to single-namespace mode so their reconciliation work does not overlap in ways you did not intend.

### All-namespace support added to the `stable` channel for Certified Operator catalogues on OpenShift

With this release the `stable` channel now supports both single-namespace and all-namespace installation modes. For this reason, the `stable-cw` channel is now deprecated and will be removed. We encourage users to switch to using the `stable` channel.

If you use OLM console, change the channel to `stable`, preview and approve the Install Plan. 

If you use the command-line, update the subscription and approve the Install Plan in case of manual approval is required.

See our [documentation](../update-openshift.md#before-you-start) for the step-by-step instructions.

### Official Docker image for major version upgrades

Starting with this release, the Operator performs major upgrades using the official Percona Docker image: `percona/percona-distribution-postgresql-upgrade:<available-upgrade-versions>`.

Refer to our [major upgrade documentation](../update-db-major.md) for detailed instructions, including the updated image path.

## Deprecation, Change, Rename and Removal

* The `stable-cw` installation channel for Certified Operator catalogues on OpenShift is deprecated. Switch to using the `stable` channel as it now supports both single-namespace and all-namespace installation modes.

* The support of version 2.7.0 is dropped from CRDs. 


## Changelog

### Improvements

* [K8SPG-1007](https://perconadev.atlassian.net/browse/K8SPG-1007) - Renamed upstream Custom Resource Definitions (CRDs) to simplify migration from other PostgreSQL operators. This change allows users to install the Percona Operator for PostgreSQL alongside existing installations without resource conflicts or API group overlapping.

* [K8SPG-1019](https://perconadev.atlassian.net/browse/K8SPG-1019) - Improved the codebase with performance optimizations, tooling, language ergonomics, and security by applying Go 1.26 using `go fix`.

* [K8SPG-1022](https://perconadev.atlassian.net/browse/K8SPG-1022) - Updated the major upgrade documentation to include critical instructions for the `pgaudit` extension. Users are now guided to drop and reinstall the extension during the upgrade process to ensure it functions correctly on the new version.

### Fixed bugs

* [K8SPG-737](https://perconadev.atlassian.net/browse/K8SPG-737) - Fixed an issue where disk usage statistics were not accessible by PMM `node_exporter` in PostgreSQL pods. The update ensures the data directory is correctly exposed to the monitoring sidecar, enabling full visibility into storage metrics through PMM.

* [K8SPG-999](https://perconadev.atlassian.net/browse/K8SPG-999) - Fixed a bug where only the first extension was removed when attempting to drop multiple custom extensions. The updated logic ensures all targeted extensions are correctly deleted, maintaining consistency between the Custom Resource specification and the database state. (Thank you Matan Haver for contributing to this issue)

* [K8SPG-1017](https://perconadev.atlassian.net/browse/K8SPG-1017) - Resolved a critical issue where upgrading to version 2.9.0 caused TLS configurations to unexpectedly switch from the internal PKI to cert-manager. This fix prevents unwanted certificate re-issuance and service disruption for clusters that rely on the Operator's internal certificate management.

### Documentation updates

* Created [Migration from Crunchy Postgres Operator to Percona Operator for PostgreSQL tutorials](../migration-from-crunchy.md)
* Improved the [major upgrade description](../update-db-major.md#post-upgrade-steps) for users of `pgAudit` extension.
* Database cluster upgrade documentation now uses PostgreSQL 18 as the default example in upgrade commands. If you are upgrading a cluster running PostgreSQL 17 or below, refer to the [certified images list](../images.md) to determine the correct version and image tags.

## Supported software

This Operator version is developed, tested and based on:

--8<-- [start:software]

* PostgreSQL 14.23-1, 15.18-1, 16.14-1, 17.10-1, 18.4-1 as the database. Other versions may also work but have not been tested.
* pgBackRest 2.58.0-2 for backup and recovery
* pgBouncer 1.25.2-1 for connection pooling
* Patroni version 4.1.0 for high-availability
* PostGIS version 3.5.5
* PMM Client version 2.44.1-1 and 3.7.1


--8<-- [end:software]

## Supported platforms

Percona Operators are designed for compatibility with all [CNCF-certified :octicons-link-external-16:](https://www.cncf.io/training/certification/software-conformance/) Kubernetes distributions. 

Our release process includes targeted testing and validation on major cloud provider platforms and OpenShift, as detailed below:

--8<-- [start:platforms]

* [Google Kubernetes Engine (GKE) :octicons-link-external-16:](https://cloud.google.com/kubernetes-engine) 1.33 - 1.35
* [Amazon Elastic Container Service for Kubernetes (EKS) :octicons-link-external-16:](https://aws.amazon.com) 1.33 - 1.35
* [OpenShift :octicons-link-external-16:](https://www.redhat.com/en/technologies/cloud-computing/openshift) 4.18 - 4.21
* [Azure Kubernetes Service (AKS) :octicons-link-external-16:](https://azure.microsoft.com/en-us/services/kubernetes-service/) 1.33 - 1.35
* [Minikube :octicons-link-external-16:](https://github.com/kubernetes/minikube) 1.38.1 with Kubernetes v1.35.1

--8<-- [end:platforms]

This list only includes the platforms that the Percona Operators are specifically tested on as part of the release process. Other Kubernetes flavors and versions depend on the backward compatibility offered by Kubernetes itself.

## Percona certified images

Find Percona's certified Docker images that you can use with the Percona Operator for PostgreSQL in the following table.


--8<-- [start:images]

| Image                                                                | Digest                                                           |
|:---------------------------------------------------------------------|:-----------------------------------------------------------------|
| percona/percona-postgresql-operator:3.0.0 (x86_64)                    | 3bcbaec261b2e67c81b3812a4b220c859434b6791c53ee1fb7ecb66bd179de56 |
| percona/percona-postgresql-operator:3.0.0 (ARM64)                    | 5aacf965c3d7bc89a23e1292ae47c2ef89d590e77677d793e15f56b11e5d67f7 |
| percona/percona-distribution-postgresql-upgrade:18.4-17.10-16.14-15.18-14.23-1 (x86_64) | 31a9612320d3b08cb74d5e98f86b054c4562e4b900140152b28476be62f086f5 |
| percona/percona-distribution-postgresql-upgrade:18.4-17.10-16.14-15.18-14.23-1 (ARM64) | 81a831086fc4aaee83af8d86b1422b64ce77e200a8f27627c27282c9af6ad9b8 |
| percona/percona-distribution-postgresql:18.4-1 (x86_64)               | ca25cc5e291cf2307d9ec4c29811c6f6d93171f98dd2cb4c69d2036f07517a7d |
| percona/percona-distribution-postgresql:18.4-1 (ARM64)               | fae3368e04b80f4eb887621724074db4db279ca59743aacb47de51b468d514f5 |
| percona/percona-distribution-postgresql:17.10-1 (x86_64)               | 720bf87ef8cda340f833981a674d5dc71283cb39af3fd4ef97eff4ccf910b87a |
| percona/percona-distribution-postgresql:17.10-1 (ARM64)               | 6416424e58765b9434f18905f0338d466cb79bafc42e6a5570030c71a1323eee |
| percona/percona-distribution-postgresql:16.14-1 (x86_64)              | ad84dc4fa537a5ba03c7c1f51f9a1ee959132155b6943d02cb0d614fc57e4271 |
| percona/percona-distribution-postgresql:16.14-1 (ARM64)              | f377d7fd5e5e3eae56ef5886aa77691c436269bae5decb706130061286080465 |
| percona/percona-distribution-postgresql:15.18-1 (x86_64)              | 60728795a6e954d9255526a208e8e9e8e93278d4c1e89004f2999a6ccb196eea |
| percona/percona-distribution-postgresql:15.18-1 (ARM64)              | 78b1b7488a897ffaf609c8d1edc6c5a27b76a3c697bbb24db5f2dec3fd66ee34 |
| percona/percona-distribution-postgresql:14.23-1 (x86_64)               | d04d3e1c41fd0c9fe438ab04081c555e1edafaed9a33f2979c7b0080045ff5fd |
| percona/percona-distribution-postgresql:14.23-1 (ARM64)              | 88925bdfc04d7dec629230c3b0f31daf7f9aed8757b2456a4439475a6b3175f5 |
| percona/percona-distribution-postgresql-with-postgis:18.4-1 (x86_64)   | a8e812334907791ca4e0e8df25cdaaa809e6824be2f20f6d802df06b5eff3276 |
| percona/percona-distribution-postgresql-with-postgis:18.4-1 (ARM64)  | 1f9972814c8dd66c3e127f40ef790fd2f2e885d9c15daa39f4b79146c3db7375 |
| percona/percona-distribution-postgresql-with-postgis:17.10-1 (x86_64)   | aa217c9563d5a372f6bd3ce9ac06ec198393cf1299760f458f02aeb94b7e5b51 |
| percona/percona-distribution-postgresql-with-postgis:17.10-1 (ARM64)  | e4c00ec25549c14b9a3665b0481b9a7df173bff8ca92cb79daf1a2abd2ef391e |
| percona/percona-distribution-postgresql-with-postgis:16.14-1 (x86_64) | 771effe967782ca9485d0fc100012f3664cb087c77627e0e68015935634d5b96 |
| percona/percona-distribution-postgresql-with-postgis:16.14-1 (ARM64) | 48608ea56e5943d245f207268a173794c55667904116840f39ccde96507763e8 |
| percona/percona-distribution-postgresql-with-postgis:15.18-1 (x86_64) | 920f2a8b6e4f446e96401be0b0fa253e47ecf9478ad3fee0ed8fa730f24288eb |
| percona/percona-distribution-postgresql-with-postgis:15.18-1 (ARM64) | af1008484a8724588a230cb25fa8eb80b4daa855a01d9a92958a6d213369b947 |
| percona/percona-distribution-postgresql-with-postgis:14.23-1 (x86_64) | d78af8e25de692787b86524a249b6ba58c2311d66e2d2286ea559b17fae147e2 |
| percona/percona-distribution-postgresql-with-postgis:14.23-1 (ARM64) | 08207a301b6b5ffd033ac8def74f08629f133f973b0a974e031146f09e1ff1a1 |
| percona/percona-pgbackrest:2.58.0-2 (x86_64)                          | 0b792f3d0bcfdd7a72c8d74f1c905469486f106db8f9299b5216d23dacf80501 |
| percona/percona-pgbackrest:2.58.0-2 (ARM64)                          | 97361155cdce8642ce47ebe83766a0c7b825930adb6c055d78476756db02fa9f |
| percona/percona-pgbouncer:1.25.2-1 (x86_64)                          | 11ef7e744e13a8508db51bd99a37a351001534747c08d7cf852c5b7c83bafc8d |
| percona/percona-pgbouncer:1.25.2-1 (ARM64)                           | 5790d944f879355194a8a5e9cecc100a959c0bd30d756fdadf4c812c682b579a |
| percona/pmm-client:3.7.1 (x86_64)                                    | 8b98629a469bf6360b14eb3ea121687737870261296f64e4587f6a6723a6845b |
| percona/pmm-client:3.7.1 (ARM64)                                     | 9951a74522a6bd70531457628daca758ffa3363941938539d164e592188e23e3 |
| percona/pmm-client:2.44.1-1 (x86_64)                                  | 52a8fb5e8f912eef1ff8a117ea323c401e278908ce29928dafc23fac1db4f1e3 |
| percona/pmm-client:2.44.1-1 (ARM64)                                  | 390bfd12f981e8b3890550c4927a3ece071377065e001894458047602c744e3b |


--8<-- [end:images]
