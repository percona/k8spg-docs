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

* [Design and architecture](architecture.md)

* [Comparison with other solutions](compare.md)

# Quickstart guides

* [Install on Minikube](minikube.md)

* [Install on Google Kubernetes Engine (GKE)](gke.md)

* [Install with Helm](helm.md)

# Installation guides

* [Generic Kubernetes installation](kubernetes.md)

* [Install on OpenShift](openshift.md)

# Configuration

* [Application and system users](users.md)

* [Changing PostgreSQL Options](options.md)

* [Anti-affinity and tolerations](constraints.md)

* [Transport Encryption (TLS/SSL)](TLS.md)

* [Telemetry](telemetry.md)

# Management

* [Backup and restore](backups.md)

* [Upgrade Percona Distribution for PostgreSQL and the Operator](update.md)

* [Horizontal and vertical scaling](scaling.md)

* [Monitor with Percona Monitoring and Management (PMM)](monitoring.md)

* [Restart or pause the cluster](pause.md)

# HOWTOs

* [How to deploy a standby cluster for Disaster Recovery](standby.md)

* [Percona Operator for PostgreSQL single-namespace and multi-namespace deployment](cluster-wide.md)

* [Using PostgreSQL tablespaces with Percona Operator for PostgreSQL](tablespace.md)

# Reference

* [Custom Resource options](operator.md)

* [Operator installation options](installation-options.md)

* [Percona certified images](images.md)

* [Frequently Asked Questions](faq.md)

* [Release Notes](ReleaseNotes/index.md)
