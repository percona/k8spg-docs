# *Percona Operator for PostgreSQL* 1.5.0

* **Date**

    November 30, 2023

* **Installation**

    [Percona Operator for PostgreSQL](../index.md#installation-guides)

## Improvements

* {{ k8spgjira(340) }}: Send the CR-based telemetry when spec.upgradeOptions.apply=disabled

## Bugs Fixed

* {{ k8spgjira(420) }}:	Ending up in multiple shared repo after cluster pause and unpuase	Unassigned	Pending Release	MERGED	

* {{ k8spgjira(314) }}: Unsupported version string is sent to version service
  
* {{ k8spgjira(404) }}: Upgrade from Operator 1.3 to 1.4 is ending up with cluster without any replicas

* {{ k8spgjira(464) }}: Affinity test is failing
  
* {{ k8spgjira(376) }}: Missing documentation for previous versions makes impossible sequential upgrade

## Supported platforms

The Operator was developed and tested with PostgreSQL versions 12.14, 13.10, and 14.7. Other options may also work but have not been tested. The Operator 1.4.0 provides connection pooling based on pgBouncer 1.18.0 and high-availability implementation based on Patroni 2.1.4.

The following platforms were tested and are officially supported in this release:


* [Google Kubernetes Engine (GKE)](https://cloud.google.com/kubernetes-engine) 1.22 - 1.25

* [Amazon Elastic Container Service for Kubernetes (EKS)](https://aws.amazon.com) 1.22 - 1.25

* [OpenShift](https://www.redhat.com/en/technologies/cloud-computing/openshift) 4.10 - 4.12

* [Minikube](https://minikube.sigs.k8s.io/docs/) 1.28 (based on Kubernetes 1.25)


	Bug	
