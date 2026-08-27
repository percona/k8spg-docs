# System requirements

The Operator is validated for deployment on Kubernetes, GKE and EKS clusters.
The Operator is cloud native and storage agnostic, working with a wide variety
of storage classes, hostPath, and NFS.

## Supported versions

The Operator {{ release }} is developed and tested with:

--8<-- "Kubernetes-Operator-for-PostgreSQL-RN{{release}}.md:software"

## Supported platforms

The following platforms were tested and are officially supported by the Operator
{{ release }}:

--8<-- "Kubernetes-Operator-for-PostgreSQL-RN{{release}}.md:platforms"

Other Kubernetes platforms may also work but have not been tested.

## Huge pages

We strongly recommend [enabling huge pages](https://kubernetes.io/docs/tasks/manage-hugepages/scheduling-hugepages/) on worker nodes for better stability and performance.

## Installation guidelines

Choose how you wish to install Percona Operator for PostgreSQL:

* [with Helm](helm.md)
* [with `kubectl`](kubectl.md)
* [on Minikube](minikube.md)
* [on Google Kubernetes Engine (GKE)](gke.md)
* [on Amazon Elastic Kubernetes Service (AWS EKS)](eks.md)
* [on Azure Kubernetes Service (AKS)](aks.md)
* [in a general Kubernetes-based environment](kubernetes.md)
