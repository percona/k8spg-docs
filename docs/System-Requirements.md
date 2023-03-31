# System Requirements

The Operator is validated for deployment on Kubernetes, GKE and EKS clusters.
The Operator is cloud native and storage agnostic, working with a wide variety
of storage classes, hostPath, and NFS.

## Officially supported platforms

The following platforms were tested and are officially supported by the Operator
{{ release }}:

* [Google Kubernetes Engine (GKE)](https://cloud.google.com/kubernetes-engine) 1.22 - 1.25

* [Amazon Elastic Container Service for Kubernetes (EKS)](https://aws.amazon.com) 1.22 - 1.25

* [OpenShift](https://www.redhat.com/en/technologies/cloud-computing/openshift) 4.10 - 4.12

* [Minikube](https://minikube.sigs.k8s.io/docs/) 1.28 (based on Kubernetes 1.25)

Other Kubernetes platforms may also work but have not been tested.
