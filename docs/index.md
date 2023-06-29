# Percona Operator for PostgreSQL

!!! note

    This is version {{ release }} of the Percona Operator for PostgreSQL. It is a **tech preview release** and it is **not recommended for production environments.**
    As of today, we recommend using [Percona Operator for PostgreSQL 1.x](https://www.percona.com/https://docs.percona.com/percona-operator-for-postgresql/index.html), which is production-ready and contains everything you need to quickly and consistently deploy and scale PostgreSQL clusters in a Kubernetes-based environment, on-premises or in the cloud.

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

# Features

* [System Requirements](System-Requirements.md)

* [Design and architecture](architecture.md)

* [Comparison with other solutions](compare.md)

# Quickstart

* [Install with kubectl](kubectl.md)

# Installation

* [Install on Minikube](minikube.md)

* [Install on Google Kubernetes Engine (GKE)](gke.md)

* [Install on Amazon Elastic Kubernetes Service (AWS EKS)](eks.md)

* [Generic Kubernetes installation](kubernetes.md)

# Configuration

* [Application and system users](users.md)

* [Exposing the cluster](expose.md)

* [Anti-affinity and tolerations](constraints.md)

* [Telemetry](telemetry.md)

# Management

* [Backup and restore](backups.md)

* [High availability and scaling](scaling.md)

* [Monitor with Percona Monitoring and Management (PMM)](monitoring.md)

* [Add sidecar containers](sidecar.md)

* [Restart or pause the cluster](pause.md)

# HOWTOs

* [Percona Operator for PostgreSQL single-namespace and multi-namespace deployment](cluster-wide.md)

# Troubleshooting

* [Initial troubleshooting](debug.md)

* [Exec into the container](debug-shell.md)

* [Check the logs](debug-logs.md)

# Reference

* [Custom Resource options](operator.md)

* [Percona certified images](images.md)

* [Release Notes](ReleaseNotes/index.md)
