# *Percona Operator for PostgreSQL* 1.3.0


* **Date**

    July 28, 2022



* **Installation**

    [Percona Operator for PostgreSQL](https://www.percona.com/doc/kubernetes-operator-for-postgresql/index.html#installation-guide)


## Release Highlights




## Improvements


* {{ k8spgjira(155) }}: Flexible anti-affinity configuration


* {{ k8spgjira(196) }}: Add possibility for `postgres` user to to connect through pgbouncer


* {{ k8spgjira(147) }}: Users now can [pass additional customizations](../operator.md#backup-customconfig) to pgBackRest with the  pgBackRest configuration options provided via ConfigMap


* {{ k8spgjira(218) }}: The automated upgrade is now disabled by default to prevent an unplanned downtimes for user applications and to provide defaults more focused on strict user's contol over the cluster

* {{ k8spgjira(141) }}: A new 'build and testing' guide allows user to easily experiment with the source code of the Operator

## Bugs Fixed


* {{ k8spgjira(178) }}: Fix the bug in the instruction on passing custom configuration options for PostgreSQL which made it usable for the new cluster only


* {{ k8spgjira(193) }}: Fix the bug which caused the Operator crash without pgReplicas section in Custom Resource definition


* {{ k8spgjira(197) }}: Fix the bug which caused the Operator to make connection requests to Version Service even with disabled Smart Update

* {{ k8spgjira(207) }}: Fix the bug due to which restoring S3 backup from storage with self-signed certificates didn't work, by introducing the special [backup.storages.<storage-name>.verifyTLS](operator.md/#backup-storages-verifytls) option to address this issue

## Supported platforms

The following platforms were tested and are officially supported by the Operator
1.3.0:


* [Google Kubernetes Engine (GKE)](https://cloud.google.com/kubernetes-engine) 1.19 - 1.22


* [Amazon Elastic Container Service for Kubernetes (EKS)](https://aws.amazon.com) 1.19 - 1.21


* [OpenShift](https://www.redhat.com/en/technologies/cloud-computing/openshift) 4.7 - 4.9

This list only includes the platforms that the Percona Operators are specifically tested on as part of the release process. Other Kubernetes flavors and versions depend on the backward compatibility offered by Kubernetes itself.
