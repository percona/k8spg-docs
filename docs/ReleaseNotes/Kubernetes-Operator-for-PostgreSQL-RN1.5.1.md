# *Percona Operator for PostgreSQL* 1.5.1

* **Date**

    January 29, 2024

* **Installation**

    [Percona Operator for PostgreSQL](../index.md#installation-guides)

## Release Highlights

This release provides fixes for the following vulnerabilities in  PostgreSQL, pgBackRest, and pgBouncer images used by the Operator:

* OpenSSH could cause remote code execution by ssh-agent if a user establishes an SSH connection to a compromised or malicious SSH server and has agent forwarding enabled ([CVE-2023-38408](https://nvd.nist.gov/vuln/detail/CVE-2023-38408)). This vulnerability affects pgBackRest and PostgreSQL images.
* The c-ares library could cause a Denial of Service with 0-byte UDP payload ([CVE-2023-32067](https://nvd.nist.gov/vuln/detail/CVE-2023-32067)). This vulnerability affects pgBouncer image.

**Users of the Operator version 1.x are recommended to [upgrade](../update.md) to 1.5.1 to resolve these issues**.

## Bugs Fixed

* {{ k8spgjira(494) }}: Fix vulnerabilities in PostgreSQL, pgBackRest, and pgBouncer images

## Supported platforms

The Operator was developed and tested with PostgreSQL versions 12.16, 13.12, and 14.9. Other options may also work but have not been tested. The Operator 1.5.1 provides connection pooling based on pgBouncer 1.20.0 and high-availability implementation based on Patroni 2.1.4.

The following platforms were tested and are officially supported in this release:

* [Google Kubernetes Engine (GKE)](https://cloud.google.com/kubernetes-engine) 1.24 - 1.28

* [Amazon Elastic Container Service for Kubernetes (EKS)](https://aws.amazon.com) 1.24 - 1.28

* [OpenShift](https://www.redhat.com/en/technologies/cloud-computing/openshift) 4.11 - 4.14

* [Minikube](https://minikube.sigs.k8s.io/docs/) 1.32

