# Percona Operator for PostgreSQL 2.8.2 ({{date.2_8_2}})

[Get started with the Operator :material-arrow-right:](../quickstart.md){.md-button}

## Release Highlights

This release provides PostgreSQL images for the updated releases of Percona Distribution for PostgreSQL 18 rebuilt with disabled debug assertions. 

We're updating the images for the remaining PostgreSQL versions as soon as new Percona Distribution for PostgreSQL versions become available.

You can find the latest available images in the [images list](#percona-certified-images).

## Supported software

This version of the Operator is developed, tested and based on:

--8<-- [start:software]

* PostgreSQL 18.1-1, 17.7-1, 16.11-1, 15.15-1, 14.20-1, 13.23-1 as the database. Other versions may also work but have not been tested.
* pgBouncer 1.25.0-1 for connection pooling
* Patroni version 4.1.0 for high-availability
* PMM Client 3.5.0
* PostGIS:
   
    * version 3.5.4 for PostgreSQL 18, 
    * version 3.3.8 for PostgreSQL 17, 16, 15, 14, and 13
   
 
--8<-- [end:software]

## Supported platforms

Percona Operators are designed for compatibility with all [CNCF-certified :octicons-link-external-16:](https://www.cncf.io/training/certification/software-conformance/) Kubernetes distributions. 

Our release process includes targeted testing and validation on major cloud provider platforms and OpenShift, as detailed below for the current Operator version:

--8<-- [start:platforms]

* [Google Kubernetes Engine (GKE) :octicons-link-external-16:](https://cloud.google.com/kubernetes-engine) 1.31 - 1.33
* [Amazon Elastic Kubernetes Service (EKS) :octicons-link-external-16:](https://aws.amazon.com) 1.31 - 1.34
* [Azure Kubernetes Service (AKS) :octicons-link-external-16:](https://azure.microsoft.com/en-us/services/kubernetes-service/) 1.32 - 1.34
* [OpenShift :octicons-link-external-16:](https://www.redhat.com/en/technologies/cloud-computing/openshift) 4.17 - 4.20
* [Minikube :octicons-link-external-16:](https://github.com/kubernetes/minikube) 1.37.0 with Kubernetes v1.34.0

--8<-- [end:platforms]

This list only includes the platforms that the Percona Operators are specifically tested on as part of the release process. Other Kubernetes flavors and versions depend on the backward compatibility offered by Kubernetes itself.

## Percona certified images

Find Percona's certified Docker images that you can use with the Percona Operator for PostgreSQL in the following table.


--8<-- [start:images]

| Image                                                                 | Digest                                                           |
|:----------------------------------------------------------------------|:-----------------------------------------------------------------|
| percona/percona-postgresql-operator:2.8.2  (x86_64)  | 018b0063352fff83d7850d732c80ba6a938c425ac2d9ac7e9a0a270361ff3fc0 |
| percona/percona-postgresql-operator:2.8.2 (ARM64)  | ce7e6f612d4cef4ef86f06521549f3e3c4e1fe8ecf794feff6f3205667863792 |
| percona/percona-distribution-postgresql:18.1-3   | 940859b7c45d1217ba852e8c5e5500832daf61c6914d5af33808251cb23f0102 |
| percona/percona-distribution-postgresql:17.7-2   |  |
| percona/percona-distribution-postgresql:16.11-2    | 80882a55997c58b7a4dd5defc6482d99dc31c11fbd206f788e540a74ffab4823 |
| percona/percona-distribution-postgresql:15.15-2       | 9ace25f15a319ec741ab32502d4818874a981c38dbb22625e8f2f67bf42bb558 |
| percona/percona-distribution-postgresql:14.20-2    |  |
| percona/percona-distribution-postgresql:13.23-2     |  |
| percona/percona-postgresql-operator:2.8.2-ppg18.1-postgres-gis3.5.4   |  |
| percona/percona-postgresql-operator:2.8.2-ppg17.7-postgres-gis3.3.8   |  |
| percona/percona-postgresql-operator:2.8.2-ppg16.11-postgres-gis3.3.8  | dca87ac8ddf79ed600f8b7243d7a351ec058a0a65aedbd360ac77fcb061e441c |
| percona/percona-postgresql-operator:2.8.2-ppg15.15-postgres-gis3.3.8  |  |
| percona/percona-postgresql-operator:2.8.2-ppg14.20-postgres-gis3.3.8  |  |
| percona/percona-postgresql-operator:2.8.2-ppg13.23-postgres-gis3.3.8  |  |
| percona/percona-pgbouncer:1.25.0-1 (x86_64)  | bf2f325cc733b96dc360c2386c8931ed9e3513f55cb425e59033e1e56737134f |
| percona/percona-pgbouncer:1.25.0-1 (ARM64)    | 902feac78cf98fbd6a7aece1761371dd1a43faaed88b63be0e0d54dd524b8286 |
| percona/percona-pgbackrest:2.57.0-1  (x86_64)   | 2bf7265f84210671bc5c0928cc772202c0e6054d426eb6ecf86279d69e831b96 |
| percona/percona-pgbackrest:2.57.0-1 (ARM64)   | 59245b25fd5d0c1a2540b465e846b69f4c91b6cd183c3bfd96aa856d3e7ffbf3 |
| percona/pmm-client:2.44.1-1         | 52a8fb5e8f912eef1ff8a117ea323c401e278908ce29928dafc23fac1db4f1e3 |
| percona/pmm-client:3.5.0 (x86_64)   | 352aee74f25b3c1c4cd9dff1f378a0c3940b315e551d170c09953bf168531e4a |
| percona/pmm-client:3.5.0 (ARM64)    | cbbb074d51d90a5f2d6f1d98a05024f6de2ffdcb5acab632324cea4349a820bd |

--8<-- [end:images]
