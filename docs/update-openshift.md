# Upgrade the Operator and the database on OpenShift

## Upgrade the Operator via Operator Lifecycle Manager (OLM)

You can upgrade the Operator for PostgreSQL that was [installed on the OpenShift platform using OLM](openshift.md#install-via-the-operator-lifecycle-manager-olm) directly through the Operator Lifecycle Manager.

### Before you start

You must manually update the `initContainer.image` Custom Resource option for each PostgreSQL cluster managed by the Operator. Without this, clusters may enter an error state after the Operator upgrade.

Follow these steps to upgrade the `initContainer.image`:

1. Export the namespace as environment variable

    ```bash
    export NAMESPACE=postgres-operator
    ```

2. Retrieve the current Operator installation image used for `initContainer` by running:

    ```bash
    kubectl get deploy percona-postgresql-operator -n $NAMESPACE -o jsonpath='{.spec.template.spec.containers[*].image}'
    ```

    Find the `image` value in the relevant section of the output, for example:

    ```yaml
    registry.connect.redhat.com/percona/percona-postgresql-operator@sha256:986941a8c5f5d00a0c9cc7bd12acc9f78aa51fdcc98c7d0acddff05392d4b9a0
    ```

3. Update your PostgreSQL cluster's Custom Resource with the image you found above, replacing `cluster1` with your cluster name:

    ```bash
    kubectl patch pg cluster1 -n $NAMESPACE --type=merge --patch '{
        "spec": {
          "initContainer": { "image": "<IMAGE_FROM_STEP_2>" }
        }}'
    ```

    Repeat this command for each cluster managed by the Operator.

### Upgrade the Operator

1. Log in to the OpenShift web console and check the list of installed Operators in your namespace to see if upgrades are available.

    ![image](assets/images/olm4.svg)

2. Click the "Upgrade available" link to review details, click "Preview InstallPlan," and then click "Approve" to upgrade the Operator.

## Upgrade Percona Distribution for PostgreSQL

## Before you start

1. We recommend to [update PMM Server :octicons-link-external-16:](https://docs.percona.com/percona-monitoring-and-management/2/how-to/upgrade.html) **before** upgrading PMM Client.

2. If you are using PMM server version 2, use a PMM client image compatible with PMM 2. If you are using PMM server version 3, use a PMM client image compatible with PMM 3. See [PMM upgrade documentation :octicons-link-external-16:](https://docs.percona.com/percona-monitoring-and-management/3/pmm-upgrade/migrating_from_pmm_2.html) for how to migrate from version 2 to version 3.

## Upgrade steps

1. Find the **new** initial Operator installation image name (it had changed during the Operator upgrade) and other image names for the components of your cluster with the `kubectl get deploy` command:

    ```
    kubectl get deploy percona-postgresql-operator -n $NAMESPACE -o yaml
    ```

    ??? example "Expected output"

        ```{.json .no-copy}
        {
          "initContainer": {
            "image": "registry.connect.redhat.com/percona/percona-postgresql-operator@sha256:ae9b319eaf3367f73d135fdda4ce69f58bcb9a2b05eea71903b7d631bd8b56c2"
          },
          "image": "registry.connect.redhat.com/percona/percona-postgresql-operator-containers@sha256:2092b8badac196100a70e708e18ef6c70f9f398c99431f3905e8394b9cadd91a",
          ...
          "proxy": {
            "pgBouncer": {
              "image": "registry.connect.redhat.com/percona/percona-postgresql-operator-containers@sha256:73916031a5b9a033efdf86597b9df58837336ae208a8743d4c70874d459daeda"
            }
          },
          ...
          "backups": {
            "pgbackrest": {
              "image": "registry.connect.redhat.com/percona/percona-postgresql-operator-containers@sha256:5937c9778be5c94acb4be81d979b6e5503f85dea1196f20f435b19467e56d1d0"
            }
          },
          ....
          "pmm": {
            "enabled": false,
            "image": "registry.connect.redhat.com/percona/percona-postgresql-operator-containers@sha256:05dc00f69ed0fae48453476ace93bd43c046bf07a511cdca16e2fcad29c53805"
          }
        }
        ```

2. [Apply a patch :octicons-link-external-16:](https://kubernetes.io/docs/tasks/run-application/update-api-object-kubectl-patch/) to update your cluster's Custom Resource. Set the `crVersion` field to match the Operator version and update the images as needed. 

    Depending on whether you've already updated the PMM client, either include its image in the list of images to update in your patch command or exclude the PMM client image from the patch.

    If your cluster is named `cluster1`, use the following command as an example:

    === "With PMM Client"

        ```bash
        kubectl patch pg cluster1 -n $NAMESPACE --type=merge --patch '{
        "spec": {
        "crVersion":"{{release}}",
        "initContainer": { "image": "registry.connect.redhat.com/percona/percona-postgresql-operator@sha256:ae9b319eaf3367f73d135fdda4ce69f58bcb9a2b05eea71903b7d631bd8b56c2" },
        "image": "registry.connect.redhat.com/percona/percona-postgresql-operator-containers@sha256:2092b8badac196100a70e708e18ef6c70f9f398c99431f3905e8394b9cadd91a",
        "proxy": { "pgBouncer": { "image": "registry.connect.redhat.com/percona/percona-postgresql-operator-containers@sha256:73916031a5b9a033efdf86597b9df58837336ae208a8743d4c70874d459daeda" } },
        "backups": { "pgbackrest": { "image": "registry.connect.redhat.com/percona/percona-postgresql-operator-containers@sha256:5937c9778be5c94acb4be81d979b6e5503f85dea1196f20f435b19467e56d1d0" } },
        "pmm": { "image": "registry.connect.redhat.com/percona/percona-postgresql-operator-containers@sha256:05dc00f69ed0fae48453476ace93bd43c046bf07a511cdca16e2fcad29c53805" }
        }}'
        ```
    
    === "Without PMM Client"

        ```bash
        kubectl patch pg cluster1 -n $NAMESPACE --type=merge --patch '{
        "spec": {
        "crVersion":"{{release}}",
        "initContainer": { "image": "registry.connect.redhat.com/percona/percona-postgresql-operator@sha256:ae9b319eaf3367f73d135fdda4ce69f58bcb9a2b05eea71903b7d631bd8b56c2" },
        "image": "registry.connect.redhat.com/percona/percona-postgresql-operator-containers@sha256:2092b8badac196100a70e708e18ef6c70f9f398c99431f3905e8394b9cadd91a",
        "proxy": { "pgBouncer": { "image": "registry.connect.redhat.com/percona/percona-postgresql-operator-containers@sha256:73916031a5b9a033efdf86597b9df58837336ae208a8743d4c70874d459daeda" } },
        "backups": { "pgbackrest": { "image": "registry.connect.redhat.com/percona/percona-postgresql-operator-containers@sha256:5937c9778be5c94acb4be81d979b6e5503f85dea1196f20f435b19467e56d1d0" } }
        }}'
        ```

3. The deployment rollout will be automatically triggered by the applied patch.
    You can track the rollout process in real time with the
    `kubectl rollout status` command with the name of your cluster:

    ```bash
    kubectl rollout status deployments percona-postgresql-operator -n postgres-operator
    ```

    ??? example "Expected output"

        ``` {.text .no-copy}
        deployment "percona-postgresql-operator" successfully rolled out
        ```
