# System requirements

The Operator is validated for deployment on Kubernetes, GKE and EKS clusters.
The Operator is cloud native and storage agnostic, working with a wide variety
of storage classes, hostPath, and NFS.

## Supported versions

The Operator {{ release }} is developed, tested and based on:

* PostgreSQL 12.20, 13.16, 14.13, 15.8, and 16.4 as the database. Other versions may also work but have not been tested. 
* pgBouncer 1.23.1 for connection pooling
* Patroni 3.3.2 for high-availability.

## Supported platforms

The following platforms were tested and are officially supported by the Operator
{{ release }}:

* [Google Kubernetes Engine (GKE) :octicons-link-external-16:](https://cloud.google.com/kubernetes-engine) 1.28 - 1.30
* [Amazon Elastic Container Service for Kubernetes (EKS) :octicons-link-external-16:](https://aws.amazon.com) 1.28 - 1.30
* [OpenShift :octicons-link-external-16:](https://www.redhat.com/en/technologies/cloud-computing/openshift) 4.13.46 - 4.16.7
* [Azure Kubernetes Service (AKS) :octicons-link-external-16:](https://azure.microsoft.com/en-us/services/kubernetes-service/) 1.28 - 1.30
* [Minikube :octicons-link-external-16:](https://github.com/kubernetes/minikube) 1.34.0 with Kubernetes 1.31.0

Other Kubernetes platforms may also work but have not been tested.

## Installation guidelines

Choose how you wish to install Percona Operator for PostgreSQL:

* [with Helm](helm.md)
* [with `kubectl`](kubectl.md)
* [on Minikube](minikube.md)
* [on Google Kubernetes Engine (GKE)](gke.md)
* [on Amazon Elastic Kubernetes Service (AWS EKS)](eks.md)
* [on Azure Kubernetes Service (AKS)](aks.md)
* [in a general Kubernetes-based environment](kubernetes.md)
