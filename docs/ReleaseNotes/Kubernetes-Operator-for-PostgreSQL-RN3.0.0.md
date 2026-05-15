# Percona Operator for PostgreSQL 3.0.0 ({{date.3_0_0}})

[Get started with the Operator :material-arrow-right:](../quickstart.md){.md-button}

We are excited to announce the release of Percona Operator for PostgreSQL 3.0.0 — a new major release that marks a new chapter for the Operator and everyone who relies on it.

Version 3.0.0 establishes Percona Operator for PostgreSQL as a **hard fork of the [Crunchy PGO project :octicons-link-external-16:](https://github.com/CrunchyData/postgres-operator)**. This is not just a version bump — it represents a fundamental shift in how the Operator is developed and maintained.

As a hard fork, Percona Operator for PostgreSQL is now fully independent, empowering the Percona team and community to drive and rapidly deliver features and improvements tailored to user needs. This shift brings long-term sustainability, greater flexibility, and a product that evolves in direct response to community feedback and real-world requirements.

## Release highlights

### Crunchy CRD renaming and seamless resource migration

With this release, all Crunchy CRDs are renamed and moved under a new API group `upstream.pgv2.percona.com`. All references to Crunchy CRDs in dependent objects, such as Custom Resources, Deployments, Secrets, ConfigMaps, Jobs, and so on, are updated accordingly.

When you update from the earlier Operator versions to 3.0.0 and newer, new API group CRDs are created alongside the legacy CRDs to keep existing workflows uninterrupted. Then the Operator automatically migrates all resources that depend on the legacy CRDs to the new API group. No manual intervention is required.

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


## Deprecation, Change, Rename and Removal

* The `stable-cw` installation channel for Certified Operator catalogues on OpenShift is deprecated. Switch to using the `stable` channel as it now supports both single-namespace and all-namespace installation modes.

* The support of version 2.7.0 is dropped from CRDs. 

### Documentation updates

* Created [Migration from Crunchy Postgres Operator to Percona Operator for PostgreSQL tutorials](../migration-from-crunchy.md)
* Improved the [major upgrade description](../update-db-major.md#post-upgrade-steps) for users of `pgAudit` extension.
* Database cluster upgrade documentation now uses PostgreSQL 18 as the default example in upgrade commands. If you are upgrading a cluster running PostgreSQL 17 or below, refer to the [certified images list](../images.md) to determine the correct version and image tags.

## Changelog

### Improvements

* [K8SPG-1007](https://perconadev.atlassian.net/browse/K8SPG-1007) - Renamed upstream Custom Resource Definitions (CRDs) to simplify migration from other PostgreSQL operators. This change allows users to install the Percona Operator for PostgreSQL alongside existing installations without resource conflicts or API group overlapping.

* [K8SPG-1019](https://perconadev.atlassian.net/browse/K8SPG-1019) - Improved the codebase with performance optimizations, tooling, language ergonomics, and security by applying Go 1.26 using `go fix`.

* [K8SPG-1022](https://perconadev.atlassian.net/browse/K8SPG-1022) - Updated the major upgrade documentation to include critical instructions for the `pgaudit` extension. Users are now guided to drop and reinstall the extension during the upgrade process to ensure it functions correctly on the new version.

### Fixed bugs

* [K8SPG-737](https://perconadev.atlassian.net/browse/K8SPG-737) - Fixed an issue where disk usage statistics were not accessible by PMM `node_exporter` in PostgreSQL pods. The update ensures the data directory is correctly exposed to the monitoring sidecar, enabling full visibility into storage metrics through PMM.

* [K8SPG-999](https://perconadev.atlassian.net/browse/K8SPG-999) - Fixed a bug where only the first extension was removed when attempting to drop multiple custom extensions. The updated logic ensures all targeted extensions are correctly deleted, maintaining consistency between the Custom Resource specification and the database state. (Thank you Matan Haver for contributing to this issue)

* [K8SPG-1017](https://perconadev.atlassian.net/browse/K8SPG-1017) - Resolved a critical issue where upgrading to version 2.9.0 caused TLS configurations to unexpectedly switch from the internal PKI to cert-manager. This fix prevents unwanted certificate re-issuance and service disruption for clusters that rely on the Operator's internal certificate management.


## Supported software

This Operator version is developed, tested and based on:

--8<-- [start:software]

* PostgreSQL 14.22-1, 15.17-1, 16.13-1, 17.9-1, 18.3-1 as the database. Other versions may also work but have not been tested.
* pgBackRest 2.58.0-1 for backup and recovery
* pgBouncer 1.25.1-1 for connection pooling
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

| Image                                                                 | Digest                                                           |
|:----------------------------------------------------------------------|:-----------------------------------------------------------------|
| Image                                                                | Digest                                                           |
|:---------------------------------------------------------------------|:-----------------------------------------------------------------|
| percona/percona-postgresql-operator:3.0.0 (x86_64)                    | 813b63076f618a9361400fd66f1cf558c9e23c4b3ab934fcc8f210d402a8b4b4 |
| percona/percona-postgresql-operator:3.0.0 (ARM64)                    | f6f9aa1357de651c74b773f2412a654452a7a1305ba379846d6b149deed09359 |
| percona/percona-distribution-postgresql:18.3-2 (x86_64)               | 80c6b3ffdfe8ecbb0f6d1036267f77144a0ecd76a0e7b9cb8ae27faa317baa78 |
| percona/percona-distribution-postgresql:18.3-2 (ARM64)               | 08734fd199b163a78844af3e03e252b20641483601cac91ceef950e26abb5146 |
| percona/percona-distribution-postgresql:17.9-2 (x86_64)               | 69a8e13fee2d100fdac345faac62884b155a8092e02e58dfa5747898992353bd |
| percona/percona-distribution-postgresql:17.9-2 (ARM64)               | d4927eb31dba1d3fbf9bff51f35faa23a0fff896128166c40242cf754a7de80d |
| percona/percona-distribution-postgresql:16.13-2 (x86_64)              | 17ed9742ca524b7c3fc0fde8c122d49252fcebb053d6b5e208c1df35b9211931 |
| percona/percona-distribution-postgresql:16.13-2 (ARM64)              | 8c6317fb1141e20b3ecb1d137b95439f6dbb1ffa2b1d7d5c030ddfa71d54c46a |
| percona/percona-distribution-postgresql:15.17-2 (x86_64)              | 7977cb3884e7ccb14a82d76805fb1ac79a54076112ebc29f2cf1ba17e7b554ac |
| percona/percona-distribution-postgresql:15.17-2 (ARM64)              | aae0d23f40cf24634d8bbed2f49ed1c075d36fe0d9436e8449c7fe9e0025e2b2 |
| percona/percona-distribution-postgresql:14.22-2 (x86_64)               | 102e75eaaa68267dd1252a9e9d1a413e970cf3fde1de2d7ccb461ed4b8858f77 |
| percona/percona-distribution-postgresql:14.22-2 (ARM64)              | 96be250c12e596c31ad164efba5a3431bb6acce1fdbcdbd3a53275bf3a9da1f7 |
| percona/percona-distribution-postgresql-with-postgis:18.3-2 (x86_64)   | dc1aa4fd3cc45769b643acdead09ac2697894cae27c8d2242ae85c22830c89c6 |
| percona/percona-distribution-postgresql-with-postgis:18.3-2 (ARM64)  | 17665e9ace6374093f4cc1797322f5e0a63a34c4f0863eed8515e9f6f4893103 |
| percona/percona-distribution-postgresql-with-postgis:17.9-2 (x86_64)   | 99063117389f49fb43d713f731ab66f904c0db701e858cc1cb4c474bc8dfdd11 |
| percona/percona-distribution-postgresql-with-postgis:17.9-2 (ARM64)  | 4d4f761124f627aeb61fb5153848873703d9bbc78df0f635448b25250c45c4ba |
| percona/percona-distribution-postgresql-with-postgis:16.13-2 (x86_64) | e098e4cd437fd0b10e41711b1b7caefe951b70b5a3be115064a9f6614b8d1b98 |
| percona/percona-distribution-postgresql-with-postgis:16.13-2 (ARM64) | f3db173951d85f77535c8fb3ff67ce9ccd82b4c68036228916ac497caa0221dd |
| percona/percona-distribution-postgresql-with-postgis:15.17-2 (x86_64) | cfafc767f2b91e132588682a8693f6fcc0714c2dd70d98cc30814188e926e0a5 |
| percona/percona-distribution-postgresql-with-postgis:15.17-2 (ARM64) | cd6fe1a91dac13c54653d8d97619aef5c3f4dac3bb30fce731715a4dcf2efd1d |
| percona/percona-distribution-postgresql-with-postgis:14.22-2 (x86_64) | 3d9f1824f9d8790edbc32db22cc272f4ae543615fcdb36ceaac2685508b1149c |
| percona/percona-distribution-postgresql-with-postgis:14.22-2 (ARM64) | 387f00c9094ff911eeb0b421924f03e89345f08ef49db7303f5ff8c9da1aad9c |
| percona/percona-pgbackrest:2.58.0-1 (x86_64)                          | 56542b3615f742a1ff4dec4eff7f53e87228085e50ebb66e3468d943e5a0f02e |
| percona/percona-pgbackrest:2.58.0-1 (ARM64)                          | d0b86dc1b725483999828cbf44b5dbad9616767da70cc1b33d2fef2841cd3f05 |
| percona/percona-pgbouncer:1.25.1-1 (x86_64)                          | 183f1cad97f7064745aedba96c169287ce54f2945073c28797a65bb9dc64cf8d |
| percona/percona-pgbouncer:1.25.1-1 (ARM64)                           | 6f4d7e68678a040516f729dc9a9fdf0a1e20ed3f5e5328a7b4fba23b4084c72a |
| percona/pmm-client:3.7.1 (x86_64)                                    | 8b98629a469bf6360b14eb3ea121687737870261296f64e4587f6a6723a6845b |
| percona/pmm-client:3.7.1 (ARM64)                                     | 9951a74522a6bd70531457628daca758ffa3363941938539d164e592188e23e3 |
| percona/pmm-client:2.44.1-1 (x86_64)                                  | 52a8fb5e8f912eef1ff8a117ea323c401e278908ce29928dafc23fac1db4f1e3 |
| percona/pmm-client:2.44.1-1 (ARM64)                                  | 390bfd12f981e8b3890550c4927a3ece071377065e001894458047602c744e3b |


--8<-- [end:images]
