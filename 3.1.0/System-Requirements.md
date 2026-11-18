> For the complete documentation index, see [llms.txt](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/llms.txt).

# System requirements

The Operator is validated for deployment on Kubernetes, GKE and EKS clusters. The Operator is cloud native and storage agnostic, working with a wide variety of storage classes, hostPath, and NFS.

## Supported versions

The Operator 3.1.0 is developed and tested with:

### Percona Distribution for PostgreSQL

- **PostgreSQL** 14.24-3, 15.19-3, 16.15-3, 17.11.1-3, 18.6.1-3 as the database. Other versions may also work but have not been tested.
- **pgBackRest** 2.59.1-2 for backup and recovery. As of October 5, 2026, pgBackRest has been updated to version 2.59.1-2.
- **pgBouncer** 1.25.2-8 for connection pooling
- **Patroni** version 4.1.5 for high-availability
- **PostGIS** version 3.5.7
- **PMM Client** version 3.9.1
- **cert-manager** 1.21.1

### PostgreSQL Community

- PostgreSQL 14.24, 15.19, 16.15, 17.11, 18.6, and 19 (tech preview) as the database.
- pgBackRest 2.59.0 for backup and recovery
- pgBouncer 1.25.2 for connection pooling

## Supported platforms

The following platforms were tested and are officially supported by the Operator 3.1.0:

- [Google Kubernetes Engine (GKE)](https://cloud.google.com/kubernetes-engine) 1.34 - 1.35
- [Amazon Elastic Kubernetes Service (EKS)](https://aws.amazon.com) 1.34 - 1.36
- [Azure Kubernetes Service (AKS)](https://azure.microsoft.com/en-us/services/kubernetes-service/) 1.34 - 1.36
- [OpenShift](https://www.redhat.com/en/technologies/cloud-computing/openshift) 4.19.43 - 4.22.10
- [Minikube](https://github.com/kubernetes/minikube) 1.38.1 with Kubernetes v1.35.1
- [Rancher](https://rancher.com/docs/rke2/latest/en/) with Rancher Kubernetes Engine (RKE2) - 1.34 - 1.36

Other Kubernetes platforms may also work but have not been tested.

## Huge pages

We strongly recommend [enabling huge pages](https://kubernetes.io/docs/tasks/manage-hugepages/scheduling-hugepages/) on worker nodes for better stability and performance.

## Installation guidelines

Choose how you wish to install Percona Operator for PostgreSQL:

- [with Helm](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/helm.html)
- [with `kubectl`](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/kubectl.html)
- [on Minikube](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/minikube.html)
- [on Google Kubernetes Engine (GKE)](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/gke.html)
- [on Amazon Elastic Kubernetes Service (AWS EKS)](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/eks.html)
- [on Azure Kubernetes Service (AKS)](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/aks.html)
- [in a general Kubernetes-based environment](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/kubernetes.html)
