# Frequently Asked Questions

## Why do we need to follow “the Kubernetes way” when Kubernetes was never intended to run databases?

As it is well known, the Kubernetes approach is targeted at stateless
applications but provides ways to store state (in Persistent Volumes, etc.) if
the application needs it. Generally, a stateless mode of operation is supposed
to provide better safety, sustainability, and scalability, it makes the
already-deployed components interchangeable. You can find more about substantial
benefits brought by Kubernetes to databases in [this blog post](https://www.percona.com/blog/2020/10/08/the-criticality-of-a-kubernetes-operator-for-databases/).

The architecture of state-centric applications (like databases) should be
composed in a right way to avoid crashes, data loss, or data inconsistencies
during hardware failure. Percona Operator for PostgreSQL
provides out-of-the-box functionality to automate provisioning and management of
highly available PostgreSQL database clusters on Kubernetes.

## How can I contact the developers?

The best place to discuss Percona Operator for PostgreSQL
with developers and other community members is the [community forum](https://forums.percona.com/c/postgresql/percona-kubernetes-operator-for-postgresql/68).

If you would like to report a bug, use the Percona Operator for PostgreSQL [project in JIRA](https://jira.percona.com/projects/K8SPG).

## How can I analyze PostgreSQL logs with pgBadger?

[pgBadger](https://pgbadger.darold.net/) is a report generator for PostgreSQL,
which can analyze PostgreSQL logs and provide you web-based representation with
charts and various statistics. You can configure it via the
[pgBadger Section](operator.md#operator-pgbadger-section) in the [deploy/cr.yaml](https://github.com/percona/percona-postgresql-operator/blob/main/deploy/cr.yaml)
file. The most important option there is [pgBadger.enabled](operator.md#pgbadger-enabled),
which is off by default. When enabled, a separate pgBadger sidecar container
with a specialized HTTP server is added to each PostgreSQL Pod.

You can generate the log report and access it through an exposed port (10000 by
default) and an `/api/badgergenerate` endpoint:
`http://<Pod-address>:10000/api/badgergenerate`. Also, this report
is available in the appropriate pgBadger container as a `/report/index.html`
file.

## How can I set the Operator to control PostgreSQL in several namespaces?

Sometimes it is convenient to have one Operator watching for PostgreSQL Cluster
custom resources in several namespaces.

You can set additional namespace to be watched by the Operator as follows:


1. First of all clean up the installer artifacts:

```bash
$ kubectl delete -f deploy/operator.yaml
```


2. Make changes in the `deploy/operator.yaml` file:


    * Find the `pgo-deployer-cm` ConfigMap. It contains the `values.yaml`
configuration file. Find the `namespace` key in this file (it is set to
`"pgo"` by default) and append your additional namespace to it in a
comma-separated list.

```bash
...
apiVersion: v1
kind: ConfigMap
metadata:
  name: pgo-deployer-cm
data:
  values.yaml: |-
    ...
    namespace: "pgo,myadditionalnamespace"
    ...
```


    * Find the `pgo-deploy` container template in the `pgo-deploy` job spec.
It has `env` element named `DEPLOY_ACTION`, which you should change
from `install` to `update`:

```bash
...
apiVersion: batch/v1
kind: Job
metadata:
name: pgo-deploy
...
    containers:
      - name: pgo-deploy
      ...
      env:
        - name: DEPLOY_ACTION
          value: update
          ...
```


3. Now apply your changes as usual:

```bash
$ kubectl apply -f deploy/operator.yaml
```

**NOTE**: You need to perform cleanup between each `DEPLOY_ACTION`
activity, which can be either `install`, `update`, or `uninstall`.

## How can I store backups on S3-compatible storage with self-issued certificates?

The Operator allows you to store backups on any S3-compatible storage including your private one (for example, a local [MinIO](https://en.wikipedia.org/wiki/MinIO) installation). Backup and restore with a private S3-compatible storage can be done following the [official instruction](backups.md#backups) except the case when you use self-signed certificates and would like to skip TLS verification (which can be reasonable when both your database and storage are located in the same Kubernetes cluster or in the same protected intranet segment).

The  backup.storages. option in the `deploy/cr.yaml` configuration file allows you to skip TLS verification for specific S3-compatible storage. Setting it to `true` is enough to *make a backup*.

*Restoring a backup* without TLS requires you to make two changes in the `parameters` subsection of the `deploy/restore.yaml` file:


* set `backrest-s3-verify-tls` option to `false`,


* add `--no-repo1-storage-verify-tls` value to `backrest-restore-opts` field.

The following example shows how the resulting `parameters` section may look like:

```yaml
...
parameters:
 backrest-restore-from-cluster: cluster1
 backrest-restore-opts: --type=time --target="2022-05-03 15:22:42" --no-repo1-storage-verify-tls
 backrest-storage-type: "s3"
 backrest-s3-verify-tls: "false"
tasktype: restore
```
