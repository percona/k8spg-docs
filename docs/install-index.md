# Install Percona Operator for PostgreSQL 

## Supported PostgreSQL versions

The Operator was developed and tested with PostgreSQL versions 12.14, 13.10, 14.7, and 15.2. Other options may also work but have not been tested. The Operator provides connection pooling based on [`pgBouncer`](https://www.pgbouncer.org/) 1.18.0 and high-availability implementation based on [`Patroni`](https://patroni.readthedocs.io/en/latest/) 3.0.1.

## Supported platforms

* [Google Kubernetes Engine (GKE)](https://cloud.google.com/kubernetes-engine) 1.23 - 1.26

* [Amazon Elastic Container Service for Kubernetes (EKS)](https://aws.amazon.com) 1.23 - 1.27

* [Minikube](https://github.com/kubernetes/minikube) 1.30.1 (based on Kubernetes 1.27)

This list includes the platforms that the Percona Operators are specifically tested on as part of the release process. Other Kubernetes flavors and versions depend on the backward compatibility offered by Kubernetes itself.

## Installation guidelines

Choose how you wish to install Percona Operator for PostgreSQL:

* [with Helm](helm.md)
* [with `kubectl`](kubectl.md)
* [on Minikube](minikube.md)
* [on Google Kubernetes Engine (GKE)](gke.md)
* [on Amazon Elastic Kubernetes Service (AWS EKS)](eks.md)
* [in a Kubernetes-based environment](kubernetes.md)