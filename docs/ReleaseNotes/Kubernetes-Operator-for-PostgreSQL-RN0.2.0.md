# *Percona Distribution for PostgreSQL Operator* 0.2.0


* **Date**

    August 12, 2021



* **Installation**

    [Installing Percona Distribution for PostgreSQL Operator](https://www.percona.com/doc/kubernetes-operator-for-postgresql/index.html#installation-guide)


**Version 0.2.0 of the Percona Distribution for PostgreSQL Operator is a Beta release, and it is not recommended for production environments.**

## New Features and Improvements


* {{ k8spgjira(80) }}: The Custom Resource structure was reworked to provide the
same look and feel as in other Percona Operators. Read more about Custom
Resource options in the [documentation](../operator.md#operator-custom-resource-options)
and review the default  `deploy/cr.yaml` configuration file on [GitHub](https://github.com/percona/percona-postgresql-operator/blob/main/deploy/cr.yaml).


* {{ k8spgjira(53) }}: Merged upstream [CrunchyData Operator v4.7.0](https://github.com/CrunchyData/postgres-operator/releases/tag/v4.7.0)
made it possible to use [Google Cloud Storage as an object store for backups](../backups.md#backups-gcs)
without using third-party tools


* {{ k8spgjira(42) }}: There is no need to specify the name of the pgBackrest
Pod in the backup manifest anymore as it is detected automatically by the
Operator


* {{ k8spgjira(30) }}: Replicas management is now performed through a main
Custom Resource manifest instead of creating separate Kubernetes resources.
This also adds the possibility of scaling up/scaling down replicas via the
‘deploy/cr.yaml’ configuration file


* {{ k8spgjira(66) }}: Helm chart is now [officially provided with the Operator](../helm.md#install-helm)
