# *Percona Operator for PostgreSQL* 1.3.0


* **Date**

    August 4, 2022


* **Installation**

    [Percona Operator for PostgreSQL](index.md#installation-guides)


## Release Highlights


* The [automated upgrade](update.md#automatic-upgrade) is now disabled by default to prevent an unplanned downtimes for user applications and to provide defaults more focused on strict user’s control over the cluster

* [Flexible anti-affinity configuration](constraints.md) is now available, which allows the Operator to isolate PostgreSQL cluster instances on different Kubernetes nodes or to increase its availability by placing PostgreSQL instances in different availability zones


* Various cleanups in the [deploy/cr.yaml](https://github.com/percona/percona-postgresql-operator/blob/main/deploy/cr.yaml) configuration file simplify the deployment of the cluster, making no need in going into YAML manifests and tuning them

## Improvements


* {{ k8spgjira(155) }}: Flexible anti-affinity configuration

* {{ k8spgjira(196) }}: Add possibility for postgres user to connect to PostgreSQL through PgBouncer with a new `pgBouncer.exposePostgresUser` Custom Resource option

* {{ k8spgjira(218) }}: The [automated upgrade](update.md#automatic-upgrade) is now disabled by default to prevent an unplanned downtimes for user applications and to provide defaults more focused on strict user’s contol over the cluster; also the user is now able to [turn off sending data to the Version Service server](telemetry.md)

* {{ k8spgjira(226) }}: A new [build and testing](https://github.com/percona/percona-postgresql-operator/blob/main/e2e-tests/README.md) guide allows user to easily experiment with the source code of the Operator

## Bugs Fixed

* {{ k8spgjira(178) }}: Fix the bug in the [instruction](options.md#modifying-options-for-the-existing-cluster) on passing custom configuration options for PostgreSQL which made it usable for the new cluster only

* {{ k8spgjira(193) }}: Fix the bug which caused the Operator crash without pgReplicas section in Custom Resource definition

* {{ k8spgjira(197) }}: Fix the bug which caused the Operator to make connection requests to Version Service even with disabled Smart Update

* {{ k8spgjira(207) }}: Fix the bug due to which restoring S3 backup from storage with self-signed certificates didn’t work, by introducing the special [backup.storages.verifyTLS](operator.md/#backup-storages-verifytls) option to address this issue

## Supported platforms

The following platforms were tested and are officially supported by the Operator
1.3.0:


* [Google Kubernetes Engine (GKE)](https://cloud.google.com/kubernetes-engine) 1.21 - 1.24

* [Amazon Elastic Container Service for Kubernetes (EKS)](https://aws.amazon.com) 1.20 - 1.22

* [OpenShift](https://www.redhat.com/en/technologies/cloud-computing/openshift) 4.7 - 4.10

This list only includes the platforms that the Percona Operators are specifically tested on as part of the release process. Other Kubernetes flavors and versions depend on the backward compatibility offered by Kubernetes itself.
