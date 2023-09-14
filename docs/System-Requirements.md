# System requirements

The Operator is validated for deployment on Kubernetes, GKE and EKS clusters.
The Operator is cloud native and storage agnostic, working with a wide variety
of storage classes, hostPath, and NFS.

## Supported versions

The Operator {{ release }} is developed, tested and based on:

* PostgreSQL 12.14, 13.10, 14.7, and 15.2 as the database. Other versions may also work but have not been tested. 
* pgBouncer 1.18.0 for connection pooling
* Patroni 3.0.1 for high-availability.

## Supported platforms

The following platforms were tested and are officially supported by the Operator
{{ release }}:

* [Google Kubernetes Engine (GKE)](https://cloud.google.com/kubernetes-engine) 1.23 - 1.26

* [Amazon Elastic Container Service for Kubernetes (EKS)](https://aws.amazon.com) 1.23 - 1.27

* [Minikube](https://github.com/kubernetes/minikube) 1.30.1 (based on Kubernetes 1.27)

Other Kubernetes platforms may also work but have not been tested.

## Installation guidelines

Choose how you wish to install Percona Operator for PostgreSQL:

* [with Helm](helm.md)
* [with `kubectl`](kubectl.md)
* [on Minikube](minikube.md)
* [on Google Kubernetes Engine (GKE)](gke.md)
* [on Amazon Elastic Kubernetes Service (AWS EKS)](eks.md)
* [in a Kubernetes-based environment](kubernetes.md)
