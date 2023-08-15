# System requirements

The Operator is validated for deployment on Kubernetes, GKE and EKS clusters.
The Operator is cloud native and storage agnostic, working with a wide variety
of storage classes, hostPath, and NFS.

The Operator {{ release }} was developed and tested with PostgreSQL versions 12.14, 13.10, 14.7, and 15.2. Other options may also work but have not been tested. The Operator provides connection pooling based on [`pgBouncer`](https://www.pgbouncer.org/) 1.18.0 and high-availability implementation based on [`Patroni`](https://patroni.readthedocs.io/en/latest/) 3.0.1.

## Supported platforms

The following platforms were tested and are officially supported by the Operator
{{ release }}:

* [Google Kubernetes Engine (GKE)](https://cloud.google.com/kubernetes-engine)
* [Amazon Elastic Container Service for Kubernetes (EKS)](https://aws.amazon.com)
* [Minikube](https://github.com/kubernetes/minikube)

Other Kubernetes platforms may also work but have not been tested.

The version compatibility matrix for different Operator releases is shown below:

| Operator | [PostgreSQL](https://www.postgresql.org/) | [pgBackRest](https://pgbackrest.org/) | [pgBouncer](http://pgbouncer.github.io/) | [GKE](https://cloud.google.com/kubernetes-engine)         | [EKS](https://aws.amazon.com)         | [Openshift](https://www.redhat.com/en/technologies/cloud-computing/openshift)   | [Minikube](https://github.com/kubernetes/minikube)                          |
|:--------|:--------|:-----|:-------|:------------|:------------|:------------|:----------------------------------|
| 2.2.0   | 12 - 15 | 2.43 | 1.18.0 | 1.23 - 1.26 | 1.23 - 1.27 |             | 1.30.1 (based on Kubernetes 1.27) |
| 2.1.0   | 12 - 15 | 2.43 | 1.18.0 | 1.23 - 1.25 | 1.23 - 1.25 |             |                                   |
| 2.0.0   | 12 - 14 | 2.41 | 1.17.0 | 1.22 - 1.25 |             |             |                                   |
| 1.4.0   | 12 - 14 | 2.43 | 1.18.0 | 1.22 - 1.25 | 1.22 - 1.25 | 4.10 - 4.12 | 1.28 (based on Kubernetes 1.25)   |
| 1.3.0   | 12 - 14 | 2.38 | 1.17.0 | 1.21 - 1.24 | 1.20 - 1.22 | 4.7 - 4.10  |                                   |
| 1.2.0   | 12 - 14 | 2.37 | 1.16.1 | 1.19 - 1.22 | 1.19 - 1.21 | 4.7 - 4.10  |                                   |
| 1.1.0   | 12 - 14 | 2.34 | 1.16.0 for PostgreSQL 12; 1.16.1 for other versions | 1.19 - 1.22 | 1.18 - 1.21 | 4.7 - 4.9   |                                   |
| 1.0.0   | 12 - 13 | 2.33 | 1.13.0 | 1.17 - 1.21 | 1.21        | 4.6 - 4.8   |                                   |


## Installation guidelines

Choose how you wish to install Percona Operator for PostgreSQL:

* [with Helm](helm.md)
* [with `kubectl`](kubectl.md)
* [on Minikube](minikube.md)
* [on Google Kubernetes Engine (GKE)](gke.md)
* [on Amazon Elastic Kubernetes Service (AWS EKS)](eks.md)
* [in a Kubernetes-based environment](kubernetes.md)


