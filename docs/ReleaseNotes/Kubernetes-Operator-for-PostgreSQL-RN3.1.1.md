# Percona Operator for PostgreSQL 3.1.1 ({{date.3_1_1}})

[Get started with the Operator :material-arrow-right:](../quickstart.md){.md-button}


This release includes the fixes for security vulnerabilities, among which are CVE-2026-111943, CVE-2026-114406. It also adds support for PostgreSQL 19, improves Operator behavior with PgBouncer 1.26 and provides updated images for Percona Distribution for PostgreSQL.

## Release highlights

### Support for PostgreSQL 19

You can deploy PostgreSQL 19 on Kubernetes with the Operator. This release includes Percona Distribution for PostgreSQL 19.0.1, built from PostgreSQL 19.0.

PostgreSQL 19 adds these abilities:

* Reclaim table bloat while reads and writes continue, with `REPACK (CONCURRENTLY)`.
* Pin or adjust a query plan without changing the application, using the `pg_plan_advice` and `pg_stash_advice` extensions.
* Vacuum indexes in parallel, and vacuum the tables that need it first.
* Turn on logical replication without a server restart, and copy sequence values to a subscriber when you refresh the subscription.
* Return the existing row when an insert conflicts, with `INSERT ... ON CONFLICT DO SELECT`.

Read more about PostgreSQL 19 in:

* [Percona Distribution for PostgreSQL 19.0.1 release notes :octicons-link-external-16:](https://docs.percona.com/postgresql/19/release-notes/release-notes-v19.0.1.html)
* [What's left in Postgres 19 :octicons-link-external-16:](https://percona.community/blog/2026/11/20/whats-left-in-postgres-19/)
* [PostgreSQL 19.0 release notes :octicons-link-external-16:](https://www.postgresql.org/docs/release/19.0/)

### Pausing and resuming PgBouncer now works with PgBouncer 1.26

Percona Operator for PostgreSQL can pause and resume PgBouncer during some operations. When it does, it sends PgBouncer the `PAUSE` and `RESUME` commands. Whether the pooler is already paused or isn't paused, the Operator recognizes PgBouncer's reply and treats the command as already done instead of failing.

PgBouncer 1.26 changed the wording of those replies:

* `already suspended/paused` became `already paused`
* `pooler is not paused/suspended` became `pooler is not paused`

The Operator now recognizes both the old and the new wording. Pause and resume work with PgBouncer 1.26 as well as with earlier versions. You don't need to change any configuration.

## Changelog

### New Features

* [K8SPG-1283](https://perconadev.atlassian.net/browse/K8SPG-1283) - Added Percona Distribution for PostgreSQL 19 so you can run PostgreSQL 19 on Kubernetes. The Operator uses PostgreSQL 19 by default, and this release includes the PostgreSQL 19, PostGIS, pgBouncer, pgBackRest, and major-upgrade images.

### Improvements

* [K8SPG-1188](https://perconadev.atlassian.net/browse/K8SPG-1188) -  Fixed the issue where the Operator failed to pause and resume PgBouncer 1.26 because PgBouncer changed the text of its "already paused" and "not paused" replies. The Operator now recognizes both the old and the new text

### Documentation updates

* [K8SPG-1227](https://perconadev.atlassian.net/browse/K8SPG-1227) - Added a Failover and recovery guide that describes how Patroni handles a primary failure, how to recover after permanent node loss, and how to troubleshoot failover.
* [K8SPG-1234](https://perconadev.atlassian.net/browse/K8SPG-1234) - Added documentation for a planned switchover (role swap) between primary and standby clusters and how to handle a split-brain scenario
* [K8SPG-1230](https://perconadev.atlassian.net/browse/K8SPG-1230) - Improved Migration guides from Crunchy Data PGO to Percona Operator for PostgreSQL by adding a page that lists the Custom Resource differences between them
* [K8SPG-1231](https://perconadev.atlassian.net/browse/K8SPG-1231), [K8SPG-1232](https://perconadev.atlassian.net/browse/K8SPG-1232), [K8SPG-1233](https://perconadev.atlassian.net/browse/K8SPG-1233) - Improved the guides for migrating from Crunchy Data PGO: clarified backup strategies, persistent volume handling, expected downtime and configuration requirements, and added examples
* [K8SPG-1228](https://perconadev.atlassian.net/browse/K8SPG-1228) - Documented how the repository number in the Secret, the global path and `repo.name` must match when you restore or clone a cluster from `dataSource.pgbackrest`, and made the required options for cloning from a `PostgresCluster` easier to follow
* [K8SPG-1167](https://perconadev.atlassian.net/browse/K8SPG-1167) - Reworked the restore documentation to make the page that helps you choose a restore method, explained how to get restore values from the source cluster for a cluster clone, and added a restore troubleshooting page
* [K8SPG-154](https://perconadev.atlassian.net/browse/K8SPG-154) - Documented how to configure separate read and write pools for PgBouncer and the known limitation of this setup

## Supported software

This Operator version is developed and tested with Percona Distribution for PostgreSQL and PostgreSQL Community.

--8<-- [start:software]

### Percona Distribution for PostgreSQL

* **PostgreSQL** 14.25-2, 15.20-2, 16.16-2, 17.12.1-2, 18.7.1-2, 19.0.1-2 as the database. Other versions may also work but have not been tested.
* **pgBackRest** 2.60.1-2 for backup and recovery
* **pgBouncer** 1.26.1-2 for connection pooling
* **Patroni** version 4.1.5 for high-availability
* **PostGIS** version 3.5.7
* **PMM Client** version 3.11.0
* **cert-manager** 1.21.1

### PostgreSQL Community

* PostgreSQL 14.24, 15.19, 16.15, 17.11, 18.6, and 19 (tech preview) as the database.
* pgBackRest 2.59.0 for backup and recovery
* pgBouncer 1.25.2 for connection pooling


--8<-- [end:software]

## Supported platforms

Percona Operators are designed for compatibility with all [CNCF-certified :octicons-link-external-16:](https://www.cncf.io/training/certification/software-conformance/) Kubernetes distributions. 

Our release process includes targeted testing and validation on major cloud provider platforms and OpenShift, as detailed below:

--8<-- [start:platforms]

* [Google Kubernetes Engine (GKE) :octicons-link-external-16:](https://cloud.google.com/kubernetes-engine) 1.34 - 1.36
* [Amazon Elastic Kubernetes Service (EKS) :octicons-link-external-16:](https://aws.amazon.com) 1.34 - 1.37
* [Azure Kubernetes Service (AKS) :octicons-link-external-16:](https://azure.microsoft.com/en-us/services/kubernetes-service/) 1.34 - 1.36
* [OpenShift :octicons-link-external-16:](https://www.redhat.com/en/technologies/cloud-computing/openshift) 4.19 - 4.22
* [Minikube :octicons-link-external-16:](https://github.com/kubernetes/minikube) 1.39.0 with Kubernetes v1.37.0
* [Rancher :octicons-link-external-16:](https://rancher.com/docs/rke2/latest/en/) with Rancher Kubernetes Engine (RKE2) - 1.34 - 1.36

--8<-- [end:platforms]

This list only includes the platforms that the Percona Operators are specifically tested on as part of the release process. Other Kubernetes flavors and versions depend on the backward compatibility offered by Kubernetes itself.

## PostgreSQL Community images

Community images are available on UBI 9 and UBI 8. PostgreSQL 19 is a tech preview and ships on UBI 9 only. pgBouncer and pgBackRest community images are compatible with both UBI 8 and 9. See [PostgreSQL community images](../images-community.md).

## Percona certified images

The following tables list the images that you can use with the Percona Operator for PostgreSQL. 

--8<-- [start:images]

The Operator, pgBouncer, pgBackRest, Fluent Bit, and PMM images are the same on every UBI. 

PostgreSQL, PostGIS, and the upgrade images are built separately for each UBI version. The Fluent Bit image is identical for UBI 8 and UBI 9 because both use a compatible version of the `GLIBC` library. For UBI 10, a separate Fluent Bit image is provided due to incompatibility with the earlier `GLIBC` versions.

### Shared images

| Image | Digest |
| :------ | :------- |
| percona/percona-postgresql-operator:3.1.0 (x86_64) | a15ac0f3fc4183e6f3096a2ae5802454846721ba92c4462c472fc5bc33151f52 |
| percona/percona-postgresql-operator:3.1.0 (ARM64) | 29e063555a7ae437be1a04e369424eaa9ac4bcc7bd94ed20b94f952615f4980e |
| percona/percona-pgbouncer:1.25.2-8 (x86_64) | 1cfc120aa41e2e3131962900248a0272b5e9176e839171d9894e21b2024ce2d6 |
| percona/percona-pgbouncer:1.25.2-8 (ARM64) | cc2ce09fb5818e1cc61e6a56f631e9320d35cce965d182c0f2be5ce0c3fcc0c5 |
| percona/percona-pgbackrest:2.59.1-2 (x86_64) | ed613bd66ac18c014674034d020a18705d5ae9bc3c5b95cd43d0861acda866a6 |
| percona/percona-pgbackrest:2.59.1-2 (ARM64) | ac63cad70311b495db24a09e376eceeb29d9123477bd5ef5324ded96828c978b |
| percona/fluentbit:5.1.1-1 (x86_64) | 332ac2386031925cef314367366abea5cb6ec1ac0bc601b824422753346bc5df |
| percona/fluentbit:5.1.1-1 (ARM64) | 1d528ec4a8c9bab32762c83eb4e33458f2e48d9af94f0aa59bba0ce4e89904dd |
| percona/pmm-client:3.9.1 (x86_64) | 6b4309035f1fc4c0dcb6b7374ac7a01526319374a071759282a21eb016f754bf |
| percona/pmm-client:3.9.1 (ARM64) | ab419b7e10cd81fa44dd198e4a10c44dc056e87ea73fd836a66b6a2356bc4efc |
| percona/pmm-server:3.9.1 (x86_64) | f7011cf6723aba28d06b09bd7f8a1e7e1c6ba84a80a45e62cbfec80f98f20e60 |

### Percona Distribution for PostgreSQL images by UBI

=== "UBI 9 (default)"

    | Image | Digest |
    | :------ | :------- |
    | percona/percona-distribution-postgresql-upgrade:18.6-17.11-16.15-15.19-14.24-3 (x86_64) | 313e077dbdd1db878a5cdd2e6633419bd8c5071d2ea387c6c6cae682d5864304 |
    | percona/percona-distribution-postgresql-upgrade:18.6-17.11-16.15-15.19-14.24-3 (ARM64) | 4a063fc89f9c22dc23f4fa094a6e8f3e78bae96f83652aa8f3818be8ee10a5e2 |
    | percona/percona-distribution-postgresql:18.6.1-3 (x86_64) | 91ffd3f3cef11ebbac6e18211869a736dd1c8a7aa733c7a8c951c976c4afcfa4 |
    | percona/percona-distribution-postgresql:18.6.1-3 (ARM64) | 0e9598318eb9bd89ba6d423fb81ab9d94d37938b22203501d50b003fbd4197ae |
    | percona/percona-distribution-postgresql:17.11.1-3 (x86_64) | e80b7d694e25e5bd46a571c30faf1e7db9d5ae477c547e99a7c321923079418b |
    | percona/percona-distribution-postgresql:17.11.1-3 (ARM64) | 797482ccedb17b8f2bf1a873c125b6080f99d07e2d09850167f2fa19c498ae9b |
    | percona/percona-distribution-postgresql:16.15-3 (x86_64) | c4746bb052182bde94f6b80b0f3d42029d0b0c78cba53f43ad5b19cf722d5f3e |
    | percona/percona-distribution-postgresql:16.15-3 (ARM64) | cbc54ef5619bc4b1c4f7268cc2e64e6c288039ef02253b95f057e60bd98d4b80 |
    | percona/percona-distribution-postgresql:15.19-3 (x86_64) | 41a5de1ba4889078b6813f141126e6c29325ae6b849c318cff7acb4cd4e3ab9a |
    | percona/percona-distribution-postgresql:15.19-3 (ARM64) | 38c7d2fe9a8880179874e5577c6d9ac14875805000abfe2ee4dfccf4837f71b7 |
    | percona/percona-distribution-postgresql:14.24-3 (x86_64) | 600a731a7b7ff4e9f22cee7486def38c9b2d9faa3a324896eedd4ed025db422a |
    | percona/percona-distribution-postgresql:14.24-3 (ARM64) | edc65db23d1c183bfa1b1dcc6d7d9470a82251e97464e4daacfa417d82f2352b |
    | percona/percona-distribution-postgresql-with-postgis:18.6.1-3 (x86_64) | 7ac2782afc11321cfd3fb5f5f393b1cf9cada727e32c404cd6f5285604e504e3 |
    | percona/percona-distribution-postgresql-with-postgis:18.6.1-3 (ARM64) | 9c33db4aacb426d6573c03e29c68a48ee35883e5ea4623f48ce82717f54abb60 |
    | percona/percona-distribution-postgresql-with-postgis:17.11.1-3 (x86_64) | 5d391ae90335aa472eccf1b7d72dd22e9331a7e1028e56beab5386f62d71a302 |
    | percona/percona-distribution-postgresql-with-postgis:17.11.1-3 (ARM64) | 18508d2925aa138a9f89fd725be0446c99dce4e4fe914588d8c10a8d71443c88 |
    | percona/percona-distribution-postgresql-with-postgis:16.15-3 (x86_64) | b35ddd1dfa7472622e3ad75d24635216a28c4797701aa71ac5b56431b4616f0f |
    | percona/percona-distribution-postgresql-with-postgis:16.15-3 (ARM64) | baf204a4a74a458c7e4a39563c93ce6c25ba77343ec977b54e54dfc152b7351c |
    | percona/percona-distribution-postgresql-with-postgis:15.19-3 (x86_64) | 6a8e070600f446c4e3d01a4bca38741dace31b7a9e17f830294f9bf2b8f58055 |
    | percona/percona-distribution-postgresql-with-postgis:15.19-3 (ARM64) | c07a7a379c503ba5b5a4117bc1f8809dcdadd821bf3419fe361ca3f0e3349b63 |
    | percona/percona-distribution-postgresql-with-postgis:14.24-3 (x86_64) | 4f4605c90b74d48e35df21c08ddff9985b9d3a733b52fd735524df8203c9ea43 |
    | percona/percona-distribution-postgresql-with-postgis:14.24-3 (ARM64) | a5dee8ca9d8156abd2598e1996f9ae6bfd5770985b256d8c01b8b0c18b743910 |

=== "UBI 8"

    | Image | Digest |
    | :------ | :------- |
    | percona/percona-distribution-postgresql-upgrade:18.6-17.11-16.15-15.19-14.24-3-ubi8 (x86_64) | ac5f270495da920f3df0d989d661b9e3e5610f7a60460c006689af33aec660ef |
    | percona/percona-distribution-postgresql-upgrade:18.6-17.11-16.15-15.19-14.24-3-ubi8 (ARM64) | bc34828429ff2ff30f24d1da3ff8628c5fc881827adf0c4267fa2dea88de04e3 |
    | percona/percona-distribution-postgresql:18.6.1-3-ubi8 (x86_64) | 25bf72cf497b8208a4fe2ba032392f45a7da966cb9962c7ee30fc79bfed3ec4a |
    | percona/percona-distribution-postgresql:18.6.1-3-ubi8 (ARM64) | ef4052027353da4637f080f19bb757b0b1925a640d1c816c123eb5b4faf14d2f |
    | percona/percona-distribution-postgresql:17.11.1-3-ubi8 (x86_64) | 69c823155f3edacdd2a8f19a40bd3e253819b7a80a63f976a74dbffe00599979 |
    | percona/percona-distribution-postgresql:17.11.1-3-ubi8 (ARM64) | 3c0291d71c0674c321284607fd497c94611159ad7f158ab229b24402f5290408 |
    | percona/percona-distribution-postgresql:16.15-3-ubi8 (x86_64) | 5b9888f849a8ba36f6a066968933801df9a045fcf9a7538b9f6ce13963dea94e |
    | percona/percona-distribution-postgresql:16.15-3-ubi8 (ARM64) | e2fc2562f4f1644e9eab17485d32e96e1ea8d09294fbed0746a744814b04a6e6 |
    | percona/percona-distribution-postgresql:15.19-3-ubi8 (x86_64) | f0f564edc98ed6878e5bd6b8c5da8930b38c9319a7f80ea4a5064ec6e6131213 |
    | percona/percona-distribution-postgresql:15.19-3-ubi8 (ARM64) | f8516acc6c247e4e5bfb7354e2fcde2ba68cabe3a35fdf932b7588bf01c7cf14 |
    | percona/percona-distribution-postgresql:14.24-3-ubi8 (x86_64) | 858784721db2d235ecbf9a44ea6904aad28463f80a674ec2da656daffbf4de1f |
    | percona/percona-distribution-postgresql:14.24-3-ubi8 (ARM64) | 9fb51063212b2eddddc0769ac27a8f9c3ccb6ae53a32c6afa8475771e0d6966e |
    | percona/percona-distribution-postgresql-with-postgis:18.6.1-3-ubi8 (x86_64) | c7060d88bb4f2e15aa272b88fcb6b003f76ee11c3d69ab0fdc31554c393818ac |
    | percona/percona-distribution-postgresql-with-postgis:18.6.1-3-ubi8 (ARM64) | 40dd3f1d4370a74ba1de1d3bd490af75c1687e753696176f9049ad35a76c364f |
    | percona/percona-distribution-postgresql-with-postgis:17.11.1-3-ubi8 (x86_64) | 4ff16f0f8a61aa7edfeb0af53ee24bc97d75f477ccffba238d42313495271a71 |
    | percona/percona-distribution-postgresql-with-postgis:17.11.1-3-ubi8 (ARM64) | f9806285af50c823a0f28ceb3adb912a070491d3a0af2871a2fe7a55afff7a58 |
    | percona/percona-distribution-postgresql-with-postgis:16.15-3-ubi8 (x86_64) | e9f069174a741fdaea4decd9caeb1321e04737ac5c8c0d62dde37b7527dbeea1 |
    | percona/percona-distribution-postgresql-with-postgis:16.15-3-ubi8 (ARM64) | 06f50b54389240ab3ef1371fd19804b6e94ad7fd051d22fd02ddb41ef8227cf7 |
    | percona/percona-distribution-postgresql-with-postgis:15.19-3-ubi8 (x86_64) | e4fdc0e84f106f9df545c65978c4571d703319df7f34749a21f360126a34e632 |
    | percona/percona-distribution-postgresql-with-postgis:15.19-3-ubi8 (ARM64) | 82cd6e53ab563c8c2c3c8dfe3a3194b053dba56027f87cc8700f665af616aa92 |
    | percona/percona-distribution-postgresql-with-postgis:14.24-3-ubi8 (x86_64) | c00f6280b72cbd2492cb0923ec5876f0a0002f61d85cc808779ec5173ad7c1bc |
    | percona/percona-distribution-postgresql-with-postgis:14.24-3-ubi8 (ARM64) | d26df1855f2913bea8dca3c69b52554c35c74df690ae1a46565a5f95da7a78f1 |

=== "UBI 10"

    | Image | Digest |
    | :------ | :------- |
    | percona/percona-distribution-postgresql-upgrade:18.6-17.11-16.15-15.19-14.24-3-ubi10 (x86_64) | 32a26957c322d0568927aa4e4a950da87174d2fa1d39c4eaee67580a1511143a |
    | percona/percona-distribution-postgresql-upgrade:18.6-17.11-16.15-15.19-14.24-3-ubi10 (ARM64) | 0e655d4d4cc98c66e0c2fcb0899af54f0a2713f8a5eae9d76d7141abf683a378 |
    | percona/percona-distribution-postgresql:18.6.1-3-ubi10 (x86_64) | 9b3187302d32d66a0c9273c6fd28f586e0c56e10bc49180f00aa82b063df1108 |
    | percona/percona-distribution-postgresql:18.6.1-3-ubi10 (ARM64) | 234554e2305ea171eddbf63d23cfa570e1de6a1800dbe141d7e73d356fd78572 |
    | percona/percona-distribution-postgresql:17.11.1-3-ubi10 (x86_64) | 2d018b5428b96060cdfe226b267afec9600e84c644966cef42324dd0062ae928 |
    | percona/percona-distribution-postgresql:17.11.1-3-ubi10 (ARM64) | 1cf5d1a02288a56bcb2b2e1fb594dfeb77dc8ec8b24755e7c3cd942fddc4c9de |
    | percona/percona-distribution-postgresql:16.15-3-ubi10 (x86_64) | c9bab91d6bc0ceaa63ff098b034717fc50cd681fe2ddba725b3383f9be3eb72a |
    | percona/percona-distribution-postgresql:16.15-3-ubi10 (ARM64) | 8de1292fe4849c8b785df3567e3a5cdc119225625e7a8b8bf5d6d663d4a6478b |
    | percona/percona-distribution-postgresql:15.19-3-ubi10 (x86_64) | 6095a0f4431ad81392c17ab465514e208903cbf06a5fe6f3532e342dbd01a6d3 |
    | percona/percona-distribution-postgresql:15.19-3-ubi10 (ARM64) | 3cd2647c6b3274612b04b6a560ea707dddfc968c591e24e173e17ed4338fa5da |
    | percona/percona-distribution-postgresql:14.24-3-ubi10 (x86_64) | 25a6f697ab55a599e18f8953b46010b184ebf4c709e8c9141d566ccf4659b2d0 |
    | percona/percona-distribution-postgresql:14.24-3-ubi10 (ARM64) | 7116fb94c01ec31ff0d67926a48da4b143f417eb4c4fecab45ed64e9bd5a2e2d |
    | percona/percona-distribution-postgresql-with-postgis:18.6.1-3-ubi10 (x86_64) | ae0d50698dc94da1d9c892b93a58ae420910f01ddbe3c52199d063d4cd8d0aea |
    | percona/percona-distribution-postgresql-with-postgis:18.6.1-3-ubi10 (ARM64) | d56c3d7629d49d9276ec8acd062caa40e0b46a6be8a9336a55fcc71b7576bc67 |
    | percona/percona-distribution-postgresql-with-postgis:17.11.1-3-ubi10 (x86_64) | 7530a7b43be9d727d10036450e415094a66eb73923583da96644164e1d02b3d3 |
    | percona/percona-distribution-postgresql-with-postgis:17.11.1-3-ubi10 (ARM64) | a3c91b4eb2c5e53122aeb020221ee015ed023a36f3c2e560c5fb9ccfbc2ede27 |
    | percona/percona-distribution-postgresql-with-postgis:16.15-3-ubi10 (x86_64) | 54721d6cef5af7b3f89710e406913051ede817f1b1a44b4cf4b167d328ee288e |
    | percona/percona-distribution-postgresql-with-postgis:16.15-3-ubi10 (ARM64) | c2d7769ee6dbfb89ccf94c754e465bcb6c77278d0ba2841a632ab004d856a1d7 |
    | percona/percona-distribution-postgresql-with-postgis:15.19-3-ubi10 (x86_64) | 78354b4cd46255ffa8009ff432b3574616290d766a6abde5e5c8a576467c8c75 |
    | percona/percona-distribution-postgresql-with-postgis:15.19-3-ubi10 (ARM64) | 59ebcafb1e3e1ae80ab0134495ea99a8124f63f896b04b3a86c5299f71d0a0b0 |
    | percona/percona-distribution-postgresql-with-postgis:14.24-3-ubi10 (x86_64) | e40485ad24d1f50ee2967b28ce27e877c17101396c9910736d0d931c35a7f475 |
    | percona/percona-distribution-postgresql-with-postgis:14.24-3-ubi10 (ARM64) | 7e4980cd2dfecf3acf84cd74e3b93e170a9a6fdbe32f2bf962c048e80ca3c052 |
    | percona/fluentbit:5.1.1-1-ubi10 (x86_64) | 6deee2b13c03511605ecfb3fec1d5e5121aee63fa425c5bd4c9b51fe1a76ff7d |
    | percona/fluentbit:5.1.1-1-ubi10 (ARM64) | 77dd38e8bee9ddadfe5e0813519415c780ab044b17832a7faa5e940d8e2b6017 |

--8<-- [end:images]
