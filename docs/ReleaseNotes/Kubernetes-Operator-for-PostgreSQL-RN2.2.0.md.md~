# Percona Operator for PostgreSQL 2.2.0

* **Date**

    June 30, 2023

* **Installation**

    [Installing Percona Operator for PostgreSQL](../System-Requirements.md#installation-guidelines) 


**Percona announces the general availability of Percona Operator for PostgreSQL 2.2.0.**

Starting with this release, Percona Operator for PostgreSQL version 2 is out of technical preview and can be used in production with all the improvements it brings over the version 1 in terms of architecture, backup and recovery features, and overall flexibility.

We prepared a detailed [migration guide](../update.md) which allows existing Operator 1.x users to move their PostgreSQL clusters to the Operator 2.x. Also, [see this blog post :material-arrow-top-right:](https://www.percona.com/blog/announcing-the-general-availability-of-percona-operator-for-postgresql-version-2/) to find out more about the Operator 2.x features and benefits.

## Improvements

* {{ k8spgjira(378) }}:  A new `crVersion` Custom Resource option was added to indicate the API version this Custom Resource corresponds to

* {{ k8spgjira(359) }}: The new `users.secretName` option allows to define a custom Secret name for the users defined in the Custom Resource (thanks to Vishal Anarase for contributing)

* {{ k8spgjira(301) }}: [Amazon Elastic Container Service for Kubernetes (EKS) :material-arrow-top-right:](https://aws.amazon.com) was [added](../eks.md) to the list of officially supported platforms

* {{ k8spgjira(302) }}: [Minikube :material-arrow-top-right:](https://github.com/kubernetes/minikube) is now [officially supported by the Operator](../minikube.md) to enable ease of testing and developing

* {{ k8spgjira(326) }}: Both the Operator and database [can be now installed](../helm.md) with the Helm package manager

* {{ k8spgjira(342) }}: There is now no need in manual restart of PostgreSQL Pods after the monitor user password changed in Secrets 

* {{ k8spgjira(345) }}: The new `proxy.pgBouncer.exposeSuperusers` Custom Resource option [makes it possible](../users.md) for administrative users to connect to PostgreSQL through PgBouncer

* {{ k8spgjira(355) }}: The Operator [can now be deployed](../cluster-wide.md) in multi-namespace ("cluster-wide") mode to track Custom Resources and manage database clusters in several namespaces

## Bugs Fixed

* {{ k8spgjira(373) }}: Fix the bug due to which the Operator did not not create Secrets for the `pguser` user if PMM was enabled in the Custom Resource

* {{ k8spgjira(362) }}: It was impossible to install Custom Resource Definitions for both 1.x and 2.x Operators in one environment, preventing the migration of a cluster to the newer Operator version

* {{ k8spgjira(360) }}: Fix a bug due to which manual password changing or resetting via Secret didn't work

Known limitations

* Query analytics (QAN) will not be available in Percona Monitoring and Management (PMM) due to bugs [PMM-12024 :material-arrow-top-right:](https://jira.percona.com/browse/PMM-12024) and [PMM-11938 :material-arrow-top-right:](https://jira.percona.com/browse/PMM-11938). The fixes are included in the upcoming PMM 2.38, so QAN can be used as soon as it is released and both PMM Client and PMM Server are upgraded.

## Supported platforms

The Operator was developed and tested with PostgreSQL versions 12.14, 13.10, 14.7, and 15.2. Other options may also work but have not been tested. The Operator 2.2.0 provides connection pooling based on pgBouncer 1.18.0 and high-availability implementation based on Patroni 3.0.1.

The following platforms were tested and are officially supported by the Operator
2.2.0:

* [Google Kubernetes Engine (GKE) :material-arrow-top-right:](https://cloud.google.com/kubernetes-engine) 1.23 - 1.26

* [Amazon Elastic Container Service for Kubernetes (EKS) :material-arrow-top-right:](https://aws.amazon.com) 1.23 - 1.27

* [Minikube :material-arrow-top-right:](https://github.com/kubernetes/minikube) 1.30.1 (based on Kubernetes 1.27)

This list only includes the platforms that the Percona Operators are specifically tested on as part of the release process. Other Kubernetes flavors and versions depend on the backward compatibility offered by Kubernetes itself.

