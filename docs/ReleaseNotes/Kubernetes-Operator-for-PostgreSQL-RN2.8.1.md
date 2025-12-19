# Percona Operator for PostgreSQL 2.8.1 ({{date.2_8_1}})

[Get started with the Operator :material-arrow-right:](../quickstart.md){.md-button}

## Release Highlights

This release provides the following features and improvements:

### PostgreSQL 18 support

You can now deploy PostgreSQL 18 on Kubernetes with the Operator. This latest major version of PostgreSQL delivers major improvements in performance, usability, and security, empowering you to make large-scale, mission-critical deployments more reliable and efficient.

Key improvements of PostgreSQL 18 are:

* Asynchronous I/O (AIO) boosts throughput and reduces latency for sequential scans, vacuums, and other heavy operations. This means faster queries and smoother performance under load.
* Queries can now use multicolumn B-tree indexes more effectively. Users benefit from faster lookups without needing redundant indexes.
* Upgrades made via `pg_upgrade` no longer discard optimizer statistics. This reduces downtime and ensures consistent query performance after migrations.
* You can now enforce PRIMARY KEY, UNIQUE, and FOREIGN KEY constraints over ranges of time. This is especially valuable for applications managing time-series or historical data.
* Generated columns are now computed at read time by default. This reduces storage overhead and makes schema design more flexible.

Read more about PostgreSQL 18 in:

* [Percona Blog: Planning Ahead for PostgreSQL 18: What Matters for Your Organization :octicons-link-external-16:](https://www.percona.com/blog/planning-ahead-for-postgresql-18-what-matters-for-your-organization/)
* [PostgreSQL 18.1 release notes :octicons-link-external-16:](https://www.postgresql.org/docs/18/release-18-1.html)

Find PostgreSQL 18 images in the list of [Percona-certified images](#percona-certified-images).


## Supported software

The Operator {{ release }} is developed, tested and based on:

--8<-- [start:software]

* PostgreSQL 18.1-1, 17.7-1, 16.11-1, 15.15-1, 14.20-1, 13.23-1 as the database. Other versions may also work but have not been tested.
* pgBouncer 1.25.0-1 for connection pooling
* Patroni version 4.1.0 for high-availability
* PMM Client 3.5.0
* PostGIS:
   
    * version 3.5.4 for PostgreSQL 18, 
    * version 3.3.8 for PostgreSQL 17, 16, 15, 14, and 13
   
!!! warning "PostgreSQL RPMs rebuilt to disable debug assertions"

    The Percona Server for PostgreSQL (PSP) and Percona Distribution for PostgreSQL (PPG) RPM packages for **PostgreSQL versions 13 through 18 released as part of the Q4 quarterly release** were built with debug assertions enabled (`--enable-cassert`).

    If you installed or updated PostgreSQL RPMs within the last four months, you may be affected: 18.1, 17.6, 17.7, 16.10, 16.11, 15.14, 15.15, 14.19, 14.20, 13.22, 13.23.

    These packages have been rebuilt, and all users running RPM-based installations of the affected releases are **strongly advised** to update to the latest available packages.

    To verify, run `pg_config --configure`. If the output includes `--enable-cassert`, then your installation is affected.

    **We do not recommend using the affected PostgreSQL versions listed above in production.** Percona is working on a fix to fully address this issue. Find more information in [Percona Distribution for PostgreSQL 18.1.1](https://docs.percona.com/postgresql/18/release-notes/release-notes-v18.1.1.html) release notes.
 
--8<-- [end:software]

## Supported platforms

Percona Operators are designed for compatibility with all [CNCF-certified :octicons-link-external-16:](https://www.cncf.io/training/certification/software-conformance/) Kubernetes distributions. 

Our release process includes targeted testing and validation on major cloud provider platforms and OpenShift, as detailed below for Operator version {{release}}:

--8<-- [start:platforms]

* [Google Kubernetes Engine (GKE) :octicons-link-external-16:](https://cloud.google.com/kubernetes-engine) 1.31 - 1.33
* [Amazon Elastic Kubernetes Service (EKS) :octicons-link-external-16:](https://aws.amazon.com) 1.31 - 1.34
* [Azure Kubernetes Service (AKS) :octicons-link-external-16:](https://azure.microsoft.com/en-us/services/kubernetes-service/) 1.32 - 1.34
* [OpenShift :octicons-link-external-16:](https://www.redhat.com/en/technologies/cloud-computing/openshift) 4.16 - 4.20
* [Minikube :octicons-link-external-16:](https://github.com/kubernetes/minikube) 1.37.0 with Kubernetes v1.34.0

--8<-- [end:platforms]

This list only includes the platforms that the Percona Operators are specifically tested on as part of the release process. Other Kubernetes flavors and versions depend on the backward compatibility offered by Kubernetes itself.

## Percona certified images

Find Percona's certified Docker images that you can use with the Percona Operator for PostgreSQL in the following table.


--8<-- [start:images]

| Image                                                                 | Digest                                                           |
|:----------------------------------------------------------------------|:-----------------------------------------------------------------|
| percona/percona-postgresql-operator:2.8.1  (x86_64)  | 018b0063352fff83d7850d732c80ba6a938c425ac2d9ac7e9a0a270361ff3fc0 |
| percona/percona-postgresql-operator:2.8.1 (ARM64)  | ce7e6f612d4cef4ef86f06521549f3e3c4e1fe8ecf794feff6f3205667863792 |
| percona/percona-distribution-postgresql:18.1-1   | 23522ee9c1abda0b9cbb40c4b414328dafc10596506731954a5754e8b6994e76 |
| percona/percona-distribution-postgresql:17.7-1   | c4eec3a4fc8a5d7ba6a631a19f7387f5e34ca9ddcc8ba34bdc6709159be2c3ac |
| percona/percona-distribution-postgresql:16.11-1    | 4cd7092284bf323893c75349a5f6c0f4948d8e602fa213210e3efca28cfc2f1d |
| percona/percona-distribution-postgresql:15.15-1       | 9ace25f15a319ec741ab32502d4818874a981c38dbb22625e8f2f67bf42bb558 |
| percona/percona-distribution-postgresql:14.20-1    | e926d10167ba73da8e2c75218256cd99c68ca9072fd1b9b1ed4b00822a165ab0 |
| percona/percona-distribution-postgresql:13.23-1     | 03d8d76d844495d07d1eae3fe5767a1c8130fba0a29c6c1353e872601380f9da |
| percona/percona-postgresql-operator:2.8.1-ppg18.1-postgres-gis3.5.4   | 706c0aa7c45692d108fbb172cbcd6bf990ee95ff5a77c5e5f79638e45dccd0a9 |
| percona/percona-postgresql-operator:2.8.1-ppg17.7-postgres-gis3.3.8   | 6ceb2c24a279ddc6914ec762cf96f4b89cbd4869aa8a875c4a55fc82685cb3e7 |
| percona/percona-postgresql-operator:2.8.1-ppg16.11-postgres-gis3.3.8  | dca87ac8ddf79ed600f8b7243d7a351ec058a0a65aedbd360ac77fcb061e441c |
| percona/percona-postgresql-operator:2.8.1-ppg15.15-postgres-gis3.3.8  | c82dc9203cbe24b5dbf3cc540d5c13484c543be8b225ad9fdec92fc4c8b6f2ff |
| percona/percona-postgresql-operator:2.8.1-ppg14.20-postgres-gis3.3.8  | 14ec320d529d7c941b23da58d4d0da6249e6eba3b6d10b5d11b36e4d2aaeb929 |
| percona/percona-postgresql-operator:2.8.1-ppg13.23-postgres-gis3.3.8  | 9df1dd41a1369d672b6f8a9653dd358f2cf85f363ceff1ca3389641094494b07 |
| percona/percona-pgbouncer:1.25.0-1 (x86_64)  | bf2f325cc733b96dc360c2386c8931ed9e3513f55cb425e59033e1e56737134f |
| percona/percona-pgbouncer:1.25.0-1 (ARM64)    | 902feac78cf98fbd6a7aece1761371dd1a43faaed88b63be0e0d54dd524b8286 |
| percona/percona-pgbackrest:2.57.0-1  (x86_64)   | 2bf7265f84210671bc5c0928cc772202c0e6054d426eb6ecf86279d69e831b96 |
| percona/percona-pgbackrest:2.57.0-1 (ARM64)   | 59245b25fd5d0c1a2540b465e846b69f4c91b6cd183c3bfd96aa856d3e7ffbf3 |
| percona/pmm-client:2.44.1-1         | 52a8fb5e8f912eef1ff8a117ea323c401e278908ce29928dafc23fac1db4f1e3 |
| percona/pmm-client:3.5.0 (x86_64)   | 352aee74f25b3c1c4cd9dff1f378a0c3940b315e551d170c09953bf168531e4a |
| percona/pmm-client:3.5.0 (ARM64)    | cbbb074d51d90a5f2d6f1d98a05024f6de2ffdcb5acab632324cea4349a820bd |

--8<-- [end:images]
