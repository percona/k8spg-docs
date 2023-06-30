# System Requirements

The Operator is validated for deployment on Kubernetes, GKE and EKS clusters.
The Operator is cloud native and storage agnostic, working with a wide variety
of storage classes, hostPath, and NFS.

## Officially supported platforms

The Operator was developed and tested with PostgreSQL versions 12.14, 13.10, 14.7, and 15.2. Other options may also work but have not been tested. The Operator {{ release }} provides connection pooling based on pgBouncer 1.18.0 and high-availability implementation based on Patroni 3.0.1.

The following platforms were tested and are officially supported by the Operator
{{ release }}:

* [Google Kubernetes Engine (GKE)](https://cloud.google.com/kubernetes-engine) 1.23 - 1.26

* [Amazon Elastic Container Service for Kubernetes (EKS)](https://aws.amazon.com) 1.23 - 1.27

* [Minikube](https://github.com/kubernetes/minikube) 1.30.1 (based on Kubernetes 1.27)

Other Kubernetes platforms may also work but have not been tested.
