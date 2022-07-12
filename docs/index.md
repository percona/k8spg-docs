# Percona Operator for PostgreSQL

Kubernetes have added a way to manage containerized systems, including database
clusters. This management is achieved by controllers, declared in configuration
files. These controllers provide automation with the ability to create objects,
such as a container or a group of containers called pods, to listen for an
specific event and then perform a task.

This automation adds a level of complexity to the container-based architecture
and stateful applications, such as a database. A Kubernetes Operator is a
special type of controller introduced to simplify complex deployments. The
Operator extends the Kubernetes API with custom resources.

The [Percona Operator for PostgreSQL](https://github.com/percona/percona-postgresql-operator) is based on best practices for configuration and
setup of a Percona Distribution for PostgreSQL cluster. The benefits of the
Operator are many, but saving time and delivering a consistent and vetted
environment is key.

# Requirements


* [System Requirements](System-Requirements.md)


* [Design overview](architecture.md)


# Installation guide


* [Install Percona Distribution for PostgreSQL on Kubernetes](kubernetes.md)


* [Install Percona Distribution for PostgreSQL on OpenShift](openshift.md)


* [Install Percona Distribution for PostgreSQL on Minikube](minikube.md)


* [Install Percona Distribution for PostgreSQL on Google Kubernetes Engine (GKE)](gke.md)


* [Install Percona Distribution for PostgreSQL using Helm](helm.md)


# Configuration and Management


* [Users](users.md)


* [Providing Backups](backups.md)


* [Changing PostgreSQL Options](options.md)


* [Binding Percona Distribution for PostgreSQL components to Specific Kubernetes/OpenShift Nodes](constraints.md)


* [Pause/resume PostgreSQL Cluster](pause.md)


* [Update Percona Operator for PostgreSQL](update.md)


* [Scale Percona Distribution for PostgreSQL on Kubernetes and OpenShift](scaling.md)


* [Transport Layer Security (TLS)](TLS.md)


* [Monitoring](monitoring.md)


# HOWTOs


* [How to deploy a standby cluster for Disaster Recovery](standby.md)


* [Percona Operator for PostgreSQL single-namespace and multi-namespace deployment](cluster-wide.md)


* [Using PostgreSQL tablespaces with Percona Operator for PostgreSQL](tablespace.md)


# Reference


* [Custom Resource options](operator.md)


* [Percona certified images](images.md)


* [Frequently Asked Questions](faq.md)


* [Release Notes](ReleaseNotes/index.md)
