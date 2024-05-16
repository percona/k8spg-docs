# System Requirements

The Operator is validated for deployment on Kubernetes, GKE and EKS clusters.
The Operator is cloud native and storage agnostic, working with a wide variety
of storage classes, hostPath, and NFS.

## Officially supported platforms

The Operator was developed and tested with PostgreSQL versions 12.18, 13.14, and
14.11. Other options may also work but have not been tested. The Operator {{ release }}
provides connection pooling based on pgBouncer 1.22.0 and high-availability
implementation based on Patroni 3.2.2.

The following platforms were tested and are officially supported by the Operator
{{ release }}:

* [Google Kubernetes Engine (GKE)](https://cloud.google.com/kubernetes-engine) 1.26-1.29

* [Amazon Elastic Container Service for Kubernetes (EKS)](https://aws.amazon.com) 1.26-1.29

* [OpenShift](https://www.redhat.com/en/technologies/cloud-computing/openshift) 4.12.57 - 4.15.13

* [Minikube](https://minikube.sigs.k8s.io/docs/) 1.33


Other Kubernetes platforms may also work but have not been tested.
