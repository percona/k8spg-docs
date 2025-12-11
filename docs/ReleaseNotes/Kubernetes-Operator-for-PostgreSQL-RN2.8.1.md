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
* PostGIS:
   * version 3.5.4 for PostgreSQL 18, 
   * version 3.3.8 for PostgreSQL 17, 16, 15, 14, and 13
* PMM Client 3.5.0

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
| percona/percona-postgresql-operator:2.8.0  (x86_64)  | e34a185e1b295ff627facd3cfbdfc31f32bab714eac550de5e6da00abd9053e2 |
| percona/percona-postgresql-operator:2.8.0 (ARM64)  | 18445bd761ac3f77901f0e9eddd79b295d28b779779a29bb2d69eb51c32e3815 |
| percona/percona-distribution-postgresql:17.6-1   | ce91a339a511d91d9f1946708d7ca326572796b642d2a022a1d52a2adff8a08b |
| percona/percona-distribution-postgresql:16.10-1    | ba1aede456a938f85c9614bb70c50ce264ec68b659917a3a0847112e42bc9259 |
| percona/percona-distribution-postgresql:15.14-1       | 8280ba2410235e8266761004a2f180fe3999203e69772eb822959cf1849bd967 |
| percona/percona-distribution-postgresql:14.19-1    | 052e7fd765b790ad2321675e8f2b273fe705512afda5004c4d2a4da78489bfb0 |
| percona/percona-distribution-postgresql:13.22-1     | 2989dcc4919c8381dc970b2286dadec45c8a53067b48f2bcfff7c7c042b3a654 |
| percona/percona-postgresql-operator:2.8.0-ppg17.6-postgres-gis3.3.8   | 3322136e6e54214255601586be8f610677fe51a494d3a002cabfacd233258fab |
| percona/percona-postgresql-operator:2.8.0-ppg16.10-postgres-gis3.3.8  | 2d5f9ac5a84129e81b9ab8df25abce712223c358847afed3637fb7063a3e4a8f |
| percona/percona-postgresql-operator:2.8.0-ppg15.14-postgres-gis3.3.8  | e7f5fda3cf7d2fab028b3fb70636c9b3b11fe6b89a9f31970d2792bd8f48d8ca |
| percona/percona-postgresql-operator:2.8.0-ppg14.19-postgres-gis3.3.8  | 3f69534a0df0b608d68808df04618222e4a20c1d1567462e4482f07b86349806 |
| percona/percona-postgresql-operator:2.8.0-ppg13.22-postgres-gis3.3.8  | cd5a2a1057708fac5dda28d0ce47006cdbf865e6ffef1ac2df74065b95258fd3 |
| percona/percona-pgbouncer:1.24.1-1 (x86_64)  | 39bd093ec83ca4eaeb93b43b286d39daae4cc4b3b32956d627d242d30a5ad6f5 |
| percona/percona-pgbouncer:1.24.1-1 (ARM64)    | 84d34843180d852182790ce6175f1407a0438b3a415a21741212701706808ac0 |
| percona/percona-pgbackrest:2.56.0-1  (x86_64)   | 387469090be8e009e17cc07903aa28aa1c748ce1cc385bd69e88de3762657877 |
| percona/percona-pgbackrest:2.56.0-1 (ARM64)   | 29290808bdeb17a49c90f2ce3ccc75f3bfab43e96e160320baf16cb557d165ee |
| percona/pmm-client:2.44.1-1         | 52a8fb5e8f912eef1ff8a117ea323c401e278908ce29928dafc23fac1db4f1e3 |
| percona/pmm-client:3.4.1 (x86_64)   | 1c59d7188f8404e0294f4bfb3d2c3600107f808a023668a170a6b8036c56619b |
| percona/pmm-client:3.4.1 (ARM64)    | 2d23ba3e6f0ae88201be15272c5038d7c38f382ad8222cd93f094b5a20b854a5 |

--8<-- [end:images]
