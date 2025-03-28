# Percona Operator for PostgreSQL 2.6.0 ({{date.2_6_0}})

[Installation](../System-Requirements.md#installation-guidelines){.md-button} 

## **Release Highlights**

This release provides the following features and improvements:

### **Backup improvements**

This release implemented several improvements to the backup/restore process:

* A new [delete-backups](../operator.md#finalizers-delete-backups) finalizer was implemented to automatically remove all backups when deleting the cluster. This finalizer is off by default. It's experimental and, therefore, is not recommended for production environments.

* Backup logic was improved and now allows retrying a failed backup in the same backup Pod for a specified number of times before deleting this Pod and creating a new one. This should be beneficial in case of short connectivity issues or timeouts. This behavior is controlled by the new [backups.pgbackrest.jobs.backoffLimit](../operator.md#backupspgbackrestjobsbackofflimit) and [backups.pgbackrest.jobs.restartPolicy](../operator.md#backupspgbackrestjobsrestartpolicy) Custom Resource options.

* You can now [overwrite](../backups-restore.md#use-custom-restore-command) the default restore command for `pgBackRest` via the [patroni.dynamicConfiguration](../operator.md#patronidynamicconfiguration) Custom Resource option. Particularly, this allows to control and filter files restored to `pg_wal` directory without editing these files in the backup repository storage.

### PostgreSQL 17 support

PostgreSQL 17 is now supported by the Operator in addition to versions 13 - 16. The appropriate images are now included in the [list of Percona-certified images](../images.md). See these blogposts for details about the latest PostgreSQL 17 features with the added security and functionality improvements:

* [Encrypt PostgreSQL Data at Rest on Kubernetes :octicons-link-external-16:](https://www.percona.com/blog/encrypt-postgresql-data-at-rest-on-kubernetes/) by Ege Gunes
* [The Powerful Features Released in PostgreSQL 17 Beta 2 :octicons-link-external-16:](https://www.percona.com/blog/the-powerful-features-released-in-postgresql-17-beta-2/) by Shivam Dhapatkar
* [PostgreSQL 17: Two Small Improvements That Will Have a Major Impact :octicons-link-external-16:](https://www.percona.com/blog/postgresql-17-two-small-improvements-that-will-have-a-major-impact/) by David Stokes.

PostgreSQL 17 is currently not recommended for production environments due to the [known limitation](#known-limitations).

### `pgvector` is added to the PostgreSQL image

To support you with your AI journey, we've added the `pgvector` extension to the PostgreSQL images shipped with our Operator. Now, you can easily use Percona Distribution for PostgreSQL as a vector database by simply enabling it in your [Custom Resource options](../operator.md#extensionsbuiltinpgvector). No more [custom extension installations :octicons-link-external-16:](https://www.percona.com/blog/create-an-ai-expert-with-open-source-tools-and-pgvector/) needed.


## New features

* {{ k8spgjira(628) }}: The custom `restore_command` [can be now passed](../backups-restore.md#use-custom-restore-command) to pgBackRest via the [patroni.dynamicConfiguration](../operator.md#patronidynamicconfiguration) Custom Resource option
* {{ k8spgjira(619) }}: New `backups.pgbackrest.jobs.backoffLimit` and `backups.pgbackrest.jobs.restartPolicy` Custom Resource options allow to retry backup in the backup Pod for a specified number of times before abandoning the Pod and creating the new one
* {{ k8spgjira(648) }}: PostgreSQL 17 is now supported by the Operator

## Improvements

* {{ k8spgjira(487) }}: New `spec.metadata.labels` and `spec.metadata.annotations` Custom Resource options allow setting labels and annotation globally for all Kubernetes objects created by the Operator
* {{ k8spgjira(554) }}: New `tlsOnly` Custom Resource option allows the user to enforce TLS connections for the database cluster
* {{ k8spgjira(586) }}: The new experimental `finalizers.delete-backups` finalizer (off by default) removes all backups of the cluster at cluster deletion event
* {{ k8spgjira(634) }}: The new `autoCreateUserSchema` Custom Resource option enhances the declarative user management by automatically creating per-user schemas 
* {{ k8spgjira(652) }}: Improve security and meet compliance requirements by using PostgreSQL images built based on Red Hat Universal Base Image (UBI) 9 instead of UBI 8
* {{ k8spgjira(692) }}: Patroni versions 4.x are now supported by the Operator in addition to versions 3.x
* {{ k8spgjira(699) }}: The `pgvector` extension is now included within the PostgreSQL image used by the Operator
* {{ k8spgjira(701) }}: The `extensions.image` Custom Resource option is now optional, and can be omitted for builtin PostgreSQL extensions
* {{ k8spgjira(702) }}: A retry logic was implemented to fix intermittent Pod exec failures caused by timeouts (Thanks to dcaputo-harmoni for contribution)
* {{ k8spgjira(711) }}: The new [README.md  :octicons-link-external-16:](https://github.com/percona/percona-docker/blob/main/postgresql-containers/README.md) explains how to build your own images for the PostgreSQL cluster components used by the Operator

## Bugs Fixed

* {{ k8spgjira(594) }}: Fix a bug where extension was still appearing in pg_extension table after being removed from Custom Resource and physically deleted by the Operator
* {{ k8spgjira(637) }}: Fix a bug where restore was failing with "waiting for another restore to finish" if the pg-restore object of a previous unfinished restore was manually deleted
* {{ k8spgjira(638) }}: Fix a bug that caused flooding the logs with no completed backups found error at cluster initialization.
* {{ k8spgjira(645) }}: Fix a bug where creating sidecar containers for pgBouncer did not work
* {{ k8spgjira(681) }}: Fixed a bug where the "Last Recoverable Time" information field was missing from the output of the `kubectl get pg-backup` command due to misdetection cases
* {{ k8spgjira(713) }}: Fix a bug where The cluster not found errors were appearing in the Operator logs on cluster deletion

## Deprecation, Change, Rename and Removal

* The new versions of Percona distribution for PostgreSQL used by the Operator come with Patroni 4.x, which introduces breaking changes compared to previously used 3.x versions.  

    To maintain backward compatibility, the Operator detects the Patroni version used in the image. It is also possible to disable this auto-detection feature by manually setting the Patroni version via the [following annotation set in the metadata part](../annotations.md#customizing-patroni-version) of the Custom Resource:   

    ```
    pgv2.percona.com/custom-patroni-version: "4"
    ```

* PostgreSQL 12 is no longer supported by the Operator 2.6.0 and newer versions.

## Known limitations

PostgreSQL 17.2 image and images for other database cluster components based on PostgreSQL 17 contain the known [CVE-2025-1094 :octicons-link-external-16:](https://www.postgresql.org/support/security/CVE-2025-1094/) - a vulnerability in the libpq PostgreSQL client library, which makes images used by the Operator vulnerable to SQL injection within the PostgreSQL interactive terminal due to the lack of neutralizing quoting. Images for PostgreSQL 17 will be available soon, while images for other PosgreSQL versions have already been fixed.

## Supported platforms

The Operator {{ release }} is developed, tested and based on:

* PostgreSQL 13.18, 14.15, 15.10, 16.6, and 17.2 as the database. Other versions may also work but have not been tested. 
* pgBouncer for connection pooling:

    * version 1.23.1 - for PostgreSQL 17.2  
    * version 1.24.0 - for PostgreSQL 13.18, 14.15, 15.10, 16.6 

* Patroni for high-availability:

    * version 4.0.3 - for PostgreSQL 17.2  
    * version 4.0.4 - for PostgreSQL 13.18, 14.15, 15.10, 16.6 


Percona Operators are designed for compatibility with all [CNCF-certified :octicons-link-external-16:](https://www.cncf.io/training/certification/software-conformance/) Kubernetes distributions. 

Our release process includes targeted testing and validation on major cloud provider platforms and OpenShift, as detailed below for Operator version {{release}}:

* [Google Kubernetes Engine (GKE) :octicons-link-external-16:](https://cloud.google.com/kubernetes-engine) 1.29 - 1.31
* [Amazon Elastic Container Service for Kubernetes (EKS) :octicons-link-external-16:](https://aws.amazon.com) 1.29 - 1.32
* [OpenShift :octicons-link-external-16:](https://www.redhat.com/en/technologies/cloud-computing/openshift) 4.14.48 - 4.17.19
* [Azure Kubernetes Service (AKS) :octicons-link-external-16:](https://azure.microsoft.com/en-us/services/kubernetes-service/) 1.29 - 1.31
* [Minikube :octicons-link-external-16:](https://github.com/kubernetes/minikube) 1.35.0 with Kubernetes 1.32.0

This list only includes the platforms that the Percona Operators are specifically tested on as part of the release process. Other Kubernetes flavors and versions depend on the backward compatibility offered by Kubernetes itself.
