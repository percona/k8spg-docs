# Percona Operator for PostgreSQL 2.3.1

* **Date**

    January 23, 2024

* **Installation**

    [Installing Percona Operator for PostgreSQL](../System-Requirements.md#installation-guidelines) 

## Release Highlights

This release provides a number of bug fixes, including fixes for the following vulnerabilities in  PostgreSQL, pgBackRest, and pgBouncer images used by the Operator:

* OpenSSH could cause remote code execution by ssh-agent if a user establishes an SSH connection to a compromised or malicious SSH server and has agent forwarding enabled ([CVE-2023-38408](https://nvd.nist.gov/vuln/detail/CVE-2023-38408)). This vulnerability affects pgBackRest and PostgreSQL images.
* The c-ares library could cause a Denial of Service with 0-byte UDP payload ([CVE-2023-32067](https://nvd.nist.gov/vuln/detail/CVE-2023-32067)). This vulnerability affects pgBouncer image.

**Both Operator 1.x (including version 1.5.0) and Operator 2.x (including version 2.3.0) are affected. The 2.x versions [upgrade](../update.md#update-database-and-operator-version-2x) to 2.3.1 is recommended to resolve these issues**.

## Bugs Fixed

* {{ k8spgjira(493) }}: Fix a regression due to which the Operator could run scheduled backup only one time
* {{ k8spgjira(494) }}: Fix vulnerabilities in PostgreSQL, pgBackRest, and pgBouncer images
* {{ k8spgjira(496) }}: Fix the bug where setting the `pause` Custom Resource option to `true` for the cluster with a backup running would not take effect even after the backup completed

## Supported platforms

The Operator was developed and tested with PostgreSQL versions 12.17, 13.13, 14.10, 15.5, and 16.1. Other options may also work but have not been tested. The Operator 2.3.1 provides connection pooling based on pgBouncer 1.21.0 and high-availability implementation based on Patroni 3.1.0.

The following platforms were tested and are officially supported by the Operator
2.3.1:

* [Google Kubernetes Engine (GKE)](https://cloud.google.com/kubernetes-engine) 1.24 - 1.28
* [Amazon Elastic Container Service for Kubernetes (EKS)](https://aws.amazon.com) 1.24 - 1.28
* [OpenShift](https://www.redhat.com/en/technologies/cloud-computing/openshift) 4.11.55 - 4.14.6
* [Minikube](https://github.com/kubernetes/minikube) 1.32

This list only includes the platforms that the Percona Operators are specifically tested on as part of the release process. Other Kubernetes flavors and versions depend on the backward compatibility offered by Kubernetes itself.
