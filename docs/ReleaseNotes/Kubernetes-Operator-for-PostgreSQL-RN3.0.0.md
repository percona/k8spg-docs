# Percona Operator for PostgreSQL 3.0.0 ({{date.3_0_0}})

[Get started with the Operator :material-arrow-right:](../quickstart.md){.md-button}

We are excited to announce the release of Percona Operator for PostgreSQL 3.0.0 — a new major release that marks a new chapter for the Operator and everyone who relies on it.

Version 3.0.0 establishes Percona Operator for PostgreSQL as a **hard fork of the [Crunchy PGO project :octicons-link-external-16:](https://github.com/CrunchyData/postgres-operator)**. This is not just a version bump — it represents a fundamental shift in how the Operator is developed and maintained.

With 3.0.0, you benefit from Percona Operator for PostgreSQL being fully independent from the upstream Crunchy PGO project. Now, you can:

* Get new features, enhancements, and bug fixes as soon as they’re ready, without having to wait for upstream releases.
* See your needs and feedback prioritized directly, as the Operator evolves based on what matters to you and your workloads.
* Benefit from using a truly open source, transparent, and community-driven solution.

With this shift you get faster innovation, quicker responses, and an Operator that grows with your requirements.

## Release highlights

### Crunchy CRD renaming and seamless resource migration

With this release, all Crunchy CRDs are renamed and moved under a new API group `upstream.pgv2.percona.com`. All references to Crunchy CRDs in dependent objects, such as Custom Resources, Deployments, Secrets, ConfigMaps, Jobs, and so on, are updated accordingly.

When you update from the earlier Operator versions to 3.0.0 and newer, new API group CRDs are created alongside the legacy CRDs to keep existing workflows uninterrupted. Then the Operator automatically migrates all resources that depend on the legacy CRDs to the new API group. No manual intervention is required.

The migration event is recorded in cluster conditions and logs, so you have full visibility into what happened and when.

This change delivers these benefits:

* Safe coexistence of Percona Operator for PostgreSQL and Crunchy PGO
* Cleaner API boundaries and predictable Operator behavior
* Smooth migration from Crunchy Operator to Percona Operator using native PostgreSQL techniques and without re-architecting your deployments

For how to migrate to Percona Operator from Crunchy PGO, see the blog post series by Slava Sarzhan: <https://www.percona.com/blog/migrate-to-freedom-choosing-a-truly-open-source-postgresql-operator/>

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

Improved the [major upgrade description](../update-db-major.md#post-upgrade-steps) for users of `pgAudit` extension.

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
| percona/percona-postgresql-operator:2.9.0                            | 1990ab3568a25fbe4fbb85bc0a524c72458b6d4419f2d96a6ef61874da83ea96 |
| percona/percona-postgresql-operator:2.9.0 (ARM64)                    | 470f0a141973c91474b9337c92773aa467a2145ff5ad74fc4731a11beb446083 |
| percona/percona-distribution-postgresql:18.3-1 (x86_64) | f7f2af7cd155162fcffbd2a09e28918795db4ca1d1119c60b61a0d7c2f146ee7 |
| percona/percona-distribution-postgresql:18.3-1 (ARM64) | 97531c11ffaf33f677f7e8062783e9ce13d1cd2618cb88c56d6387bf92720dcb |
| percona/percona-distribution-postgresql:17.9-1 (x86_64)  | deca076dc5b837d9f7712de4ed007e019900d09c629fcba53d35b7ec47f4b308 |
| percona/percona-distribution-postgresql:17.9-1 (ARM64)  | 921279b3b85c6595ba3cbd67856c456f8f4b711b270f8473ff5acbd82781a43d |
| percona/percona-distribution-postgresql:16.13-1 (x86_64)   | 36ae43818f7e1414332549ef5361ed3874e3f3ad2c430e07dcea7552d8c8b362 |
| percona/percona-distribution-postgresql:16.13-1 (ARM64)  | b4771737ee43d576437fa301bd0f15f7477b0058f3d8d58f5c7e8349412c0c94 |
| percona/percona-distribution-postgresql:15.17-1 (x86_64) | 0b3faf1329c018f155aa9eb182f99b4a008f8f25b549f4cef98581002ca57d01 |
| percona/percona-distribution-postgresql:15.17-1 (ARM64) | 64c9c06271eb24552fba4f766992b9228cfd99fbaafc93313ebba10d91bcda25 |
| percona/percona-distribution-postgresql:14.22-1 (x86_64) | 2e854233f37877edf5a1920de5749a96eb0d81022b2270e00446889a6a3d6140 |
| percona/percona-distribution-postgresql:14.22-1 (ARM64) | 93034300269680d1f024be3f500590f39a3eae91868ec6ec32c5689d76b2e999 |
| percona/percona-distribution-postgresql-with-postgis:18.3-1 (x86_64)  | a2cdf2fa7b76d6f02fb249ce56efda51db476d695ae1b5e276ab89d99ab1d0a5 |
| percona/percona-distribution-postgresql-with-postgis:18.3-1 (ARM64)  | 5058d7a615bf647ff629598e1feae0a9ffcde14dce70f35814d631d90bf57e93 |
| percona/percona-distribution-postgresql-with-postgis:17.9-1 (x86_64) | 964a1a3116db7cd7fed0452376f43b07a9e3b45bf1ba2377307837745d285101 |
| percona/percona-distribution-postgresql-with-postgis:17.9-1 (ARM64) | ecbabb4b2296fd1964b46cbdb71dae9d21157ac59f64ff776aff7d39aac66d1c |
| percona/percona-distribution-postgresql-with-postgis:16.13-1 (x86_64) | 30a64dc854caf5770906e17fc4e32e4a7de3f545478c94719a8c6d7ab41b88d3 |
| percona/percona-distribution-postgresql-with-postgis:16.13-1 (ARM64) | 6936f74de4e6f5206e5367581bcfadb49860d1572a30e9387a0479d988065778 |
| percona/percona-distribution-postgresql-with-postgis:15.17-1 (x86_64) | 1d9a94124bbdd3939e8ad0beb6ef3ffd8db0858ba97ef1822e08f6c891ae2719 |
| percona/percona-distribution-postgresql-with-postgis:15.17-1 (ARM64) | f2b21836b0e0d995b8187e0c770e31f9113bf6770f51d5eae92aa608b88d4d72 |
| percona/percona-distribution-postgresql-with-postgis:14.22-1 (x86_64) | 46cf19acc553c84d643201c4ecd83a69a9d98c7432596a6907fadb093a0cd4df |
| percona/percona-distribution-postgresql-with-postgis:14.22-1 (ARM64) | 9342ff19350446e83041e7775f8f134e0d464233fe3076e0a172a50dfc41b66c |
| percona/percona-pgbouncer:1.25.1-1 (x86_64)  | 183f1cad97f7064745aedba96c169287ce54f2945073c28797a65bb9dc64cf8d |
| percona/percona-pgbouncer:1.25.1-1 (ARM64)    | 6f4d7e68678a040516f729dc9a9fdf0a1e20ed3f5e5328a7b4fba23b4084c72a |
| percona/percona-pgbackrest:2.58.0-1  (x86_64)   | 56542b3615f742a1ff4dec4eff7f53e87228085e50ebb66e3468d943e5a0f02e |
| percona/percona-pgbackrest:2.58.0-1 (ARM64)   | d0b86dc1b725483999828cbf44b5dbad9616767da70cc1b33d2fef2841cd3f05 |
| percona/pmm-client:2.44.1-1 (x86_64)                             | 52a8fb5e8f912eef1ff8a117ea323c401e278908ce29928dafc23fac1db4f1e3 |
| percona/pmm-client:2.44.1-1 (ARM64)                                  | 390bfd12f981e8b3890550c4927a3ece071377065e001894458047602c744e3b |
| percona/pmm-client:3.6.0  (x86_64)                                  | 174fa4675d3ea4d95fd7b45d11f2bcc98b98b703662e6b2614dfe886a7187b23 |
| percona/pmm-client:3.6.0 (ARM64)                                     | 435a9af2083adb68ddab6a97e6d02bd6d31c54562e919ebc09618e886d58d1ae |


--8<-- [end:images]
