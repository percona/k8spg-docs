# *Percona Operator for PostgreSQL* 1.2.0


* **Date**

    April 6, 2022



* **Installation**

    [Percona Operator for PostgreSQL](https://www.percona.com/doc/kubernetes-operator-for-postgresql/index.html#installation-guide)


## Release Highlights


* With this release, the Operator turns to a simplified naming convention and changes its official name to **Percona Operator for PostgreSQL**


* Starting from this release, the Operator [automatically generates](../TLS.md#tls-certs-auto) TLS certificates and turns on encryption by default at cluster creation time. This includes both external certificates which allow users to connect to pgBouncer and PostgreSQL via the encrypted channel, and internal ones used for communication between PostgreSQL cluster nodes


* Various cleanups in the [deploy/cr.yaml](https://github.com/percona/percona-postgresql-operator/blob/main/deploy/cr.yaml) configuration file simplify the deployment of the cluster, making no need in going into YAML manifests and tuning them

## Improvements


* [K8SPG-149](https://jira.percona.com/browse/K8SPG-149): It is now possible to [explicitly set the version of PostgreSQL for newly provisioned clusters](../update.md#operator-update-smartupdates). Before that, all new clusters were started with the latest PostgreSQL version if Version Service was enabled


* [K8SPG-148](https://jira.percona.com/browse/K8SPG-148): Add possibility of specifying `imagePullPolicy` option for all images in the Custom Resource of the cluster to run in air-gapped environments


* [K8SPG-147](https://jira.percona.com/browse/K8SPG-147): Users now can [pass additional customizations](../operator.md#backup-customconfig) to pgBackRest with the  pgBackRest configuration options provided via ConfigMap


* [K8SPG-142](https://jira.percona.com/browse/K8SPG-142): Introduce [deploy/cr-minimal.yaml](https://github.com/percona/percona-postgresql-operator/blob/main/deploy/cr-minimal.yaml) configuration file to deploy minimal viable clusters - useful for developers to deploy PostgreSQL on local Kubernetes clusters, such as [Minikube](../minikube.md#install-minikube)


* [K8SPG-141](https://jira.percona.com/browse/K8SPG-141): YAML manifest cleanup simplifies cluster deployment, reducing it to just two commands


* [K8SPG-112](https://jira.percona.com/browse/K8SPG-112): Enable automated generation of TLS certificates and provide encryption for all new clusters by default


* [K8SPG-161](https://jira.percona.com/browse/K8SPG-161): The Operator documentation now has a how-to that covers [deploying a standby PostgreSQL cluster on Kubernetes](../standby.md#howto-standby)

## Bugs Fixed


* [K8SPG-115](https://jira.percona.com/browse/K8SPG-115): Fix the bug that caused creation a “cloned” cluster with `pgDataSource` to fail due to missing Secrets


* [K8SPG-163](https://jira.percona.com/browse/K8SPG-163): Fix the security vulnerability [CVE-2021-40346](https://nvd.nist.gov/vuln/detail/CVE-2021-20329) by removing the unused dependency in the Operator images


* [K8SPG-152](https://jira.percona.com/browse/K8SPG-152): Fix the bug that prevented deploying the Operator in disabled/readonly namespace mode. It is now possible to deploy several operators in different namespaces in the same cluster

## Options Changes


* [K8SPG-116](https://jira.percona.com/browse/K8SPG-116): The `backrest-restore-from-cluster` parameter was renamed to `backrest-restore-cluster` for clarity in the [deploy/backup/restore.yaml](https://github.com/percona/percona-postgresql-operator/blob/main/deploy/backup/restore.yaml) file used to [restore the cluster from a previously saved backup](../backups.md#backups-restore)

## Supported platforms

The following platforms were tested and are officially supported by the Operator
1.2.0:


* [Google Kubernetes Engine (GKE)](https://cloud.google.com/kubernetes-engine) 1.19 - 1.22


* [Amazon Elastic Container Service for Kubernetes (EKS)](https://aws.amazon.com) 1.19 - 1.21


* [OpenShift](https://www.redhat.com/en/technologies/cloud-computing/openshift) 4.7 - 4.9

This list only includes the platforms that the Percona Operators are specifically tested on as part of the release process. Other Kubernetes flavors and versions depend on the backward compatibility offered by Kubernetes itself.
