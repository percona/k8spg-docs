# Upgrading the Operator and CRD

## Considerations for Kubernetes Cluster versions and upgrades

1. Before upgrading the Kubernetes cluster, have a disaster recovery plan in place. Ensure that a backup is taken prior to the upgrade.

2. Plan your Kubernetes cluster or Operator upgrades with version compatibility in mind.

    The Operator is supported and tested on specific Kubernetes versions. Always refer to the Operator's [release notes](ReleaseNotes/index.md) to verify the supported Kubernetes platforms.

    Note that while the Operator might run on unsupported or untested Kubernetes versions, this is not recommended. Doing so can cause various issues, and in some cases, the Operator may fail if deprecated API versions have been removed.

3. During a Kubernetes cluster upgrade, you must also upgrade the `kubelet`. It is advisable to drain the nodes hosting the database Pods during the upgrade process.

4. During the `kubelet` upgrade, nodes transition between `Ready` and `NotReady` states. Also, in some scenarios, older nodes may be replaced entirely with new nodes. Ensure that nodes hosting database or proxy pods are functioning correctly and remain in a stable state after the upgrade.

5. Regardless of the upgrade approach, pods will be rescheduled or recycled. Plan your Kubernetes cluster upgrade accordingly to minimize downtime and service disruption.

## Considerations for the Operator upgrades

1. The Operator version has three digits separated by a dot (`.`) in the format `major.minor.patch`. Here's how you can understand the version `2.6.0`:

    * `2` - major version
    * `6` - minor version
    * `0` - patch version

    You can upgrade the Operator only to the nearest `major.minor.patch` version. For example, if the next version is 2.7.1, you can go directly from 2.6.0 to 2.7.1 without any intermediate steps.

    To upgrade to a newer version, which differs from the current
    `minor.major` version by more than one, you need to make several
    incremental upgrades sequentially. 
    
    For example, to upgrade the CRD and Operator from the version 2.4.
    0 to 2.6.0, first upgrade it from 2.4.0 to 2.5.1, and then from 2.
    5.1 to 2.6.0.

2. CRD supports **the last 3 minor versions of the Operator**. This means it is compatible with the newest Operator version and the two previous minor versions. If the Operator is older than the CRD by no more than two versions, you should be able to continue using the old Operator version. But updating the CRD and Operator is the recommended path.

3. Using newer CRD with older Operator is useful to upgrade multiple [single-namespace Operator deployments](cluster-wide.md#namespace-scope) 
in one Kubernetes cluster, where each Operator controls a database cluster in
its own namespace. In this case upgrading Operator deployments will look as follows:

    * upgrade the CRD (not 3 minor versions far from the oldest Operator installation in the Kubernetes cluster) first 
    * upgrade the Operators in each namespace incrementally to the nearest minor version (e.g. first 2.4.0 to 2.5.1, then 2.5.1 to 2.6.0)

## Manual upgrade

You can upgrade the Operator and CRD as follows, considering the Operator uses
`postgres-operator` namespace, and you are upgrading it to the version {{ release }}.

1. Update the CRD for the Operator and the Role-based access control. You must use the [server-side :octicons-link-external-16:](https://kubernetes.io/docs/reference/using-api/server-side-apply/) flag when you update the CRD. Otherwise you can encounter a number of errors caused by applying the CRD client-side: the command may fail, the built-in PostgreSQL extensions can be lost during such upgrade, etc.

    Take the latest versions of the CRD and Role-based access control manifest from the official repository on GitHub with the following commands:

    ``` {.bash data-prompt="$" }
    $ kubectl apply --server-side -f https://raw.githubusercontent.com/percona/percona-postgresql-operator/v{{ release }}/deploy/crd.yaml
    $ kubectl apply --server-side -f https://raw.githubusercontent.com/percona/percona-postgresql-operator/v{{ release }}/deploy/rbac.yaml -n postgres-operator
    ```
    
    !!! note

        In case of [cluster-wide installation](cluster-wide.md), use `deploy/cw-rbac.yaml` instead of `deploy/rbac.yaml`.

2. Next, update the Percona Distribution for PostgreSQL Operator Deployment in Kubernetes by changing the container image of the Operator Pod to the latest version. Find the image name for the current Operator release [in the list of certified images](images.md). Use the following command to update the Operator to the `{{ release }}` version:

    ``` {.bash data-prompt="$" }
    $ kubectl -n postgres-operator patch deployment percona-postgresql-operator \
    -p'{"spec":{"template":{"spec":{"containers":[{"name":"operator","image":"docker.io/percona/percona-postgresql-operator:{{release}}}]}}}}'
    ```

3. The deployment rollout will be automatically triggered by the applied patch.
    You can track the rollout process in real time with the
    `kubectl rollout status` command with the name of your cluster:

    ``` {.bash data-prompt="$" }
    $ kubectl rollout status deployments percona-postgresql-operator -n postgres-operator
    ```
    
    ??? example "Expected output"

        ``` {.text .no-copy}
        deployment "percona-postgresql-operator" successfully rolled out
        ```

## Upgrade via Helm

If you have [installed the Operator using Helm](helm.md), you can upgrade the
Operator deployment with the `helm upgrade` command.

 The `helm upgrade` command updates only the Operator deployment. The [update flow for the database management system (Percona Distribution for PostgreSQL)](#upgrade-percona-distribution-for-postgresql) is the same for all installation methods, whether it was installed via Helm or `kubectl`.

1. You must have the compatible version of the Custom Resource Definition (CRD) in all namespaces that the Operator manages. Starting with version 2.7.0, you can check it using the following command:

    ``` {.bash data-prompt="$" }
    $ kubectl get crd perconapgclusters.pgv2.percona.com --show-labels
    ```
    
2. Update the [Custom Resource Definition :octicons-link-external-16:](https://kubernetes.io/docs/concepts/extend-kubernetes/api-extension/custom-resources/)
    for the Operator, taking it from the official repository on GitHub. 

    Refer to the [compatibility between CRD and the Operator](#upgrading-the-operator-and-crd) and how you can update the CRD if it is too old. Use the following command and replace the version to the required one until you are safe to update to the latest CRD version.

    ``` {.bash data-prompt="$" }
    $ kubectl apply --server-side --force-conflicts -f https://raw.githubusercontent.com/percona/percona-postgresql-operator/v{{ release }}/deploy/crd.yaml
    ```
    
    If you already have the latest CRD version in one of namespaces, don't re-run intermediate upgrades for it.

3. Upgrade the Operator deployment

    === "With default parameters"

        To upgrade the Operator installed with default parameters, use the following command: 

        ``` {.bash data-prompt="$" }
        $ helm upgrade my-operator percona/pg-operator --version {{ release }}
        ```

        The `my-operator` parameter in the above example is the name of a [release object :octicons-link-external-16:](https://helm.sh/docs/intro/using_helm/#three-big-concepts)
        which you have chosen for the Operator when installing its Helm chart.

    === "With customized parameters"

        If you installed the Operator with some [customized parameters :octicons-link-external-16:](https://github.com/percona/percona-helm-charts/tree/main/charts/pg-operator#installing-the-chart), list these options in the upgrade command.   
    
        1. Get the list of used options in YAML format :
        
            ```{.bash data-prompt="$" }
            $ helm get values my-operator -a > my-values.yaml
            ``` 
        
        2. Pass these options to the upgrade command as follows:

            ``` {.bash data-prompt="$" }
            $ helm upgrade my-operator percona/pg-operator --version {{ release }} -f my-values.yaml
            ```

    During the upgrade, you may see a warning to manually apply the CRD if it has the outdated version. In this case, refer to step 2 to upgrade the CRD and then step 3 to upgrade the deployment.

## Upgrade via Operator Lifecycle Manager (OLM)

If you have [installed the Operator on the OpenShift platform using OLM](openshift.md#install-the-operator-via-the-operator-lifecycle-manager-olm), you can upgrade the Operator within it.

1. List installed Operators for your Namespace to see if there are upgradable items.

    ![image](assets/images/olm4.svg)

2. Click the "Upgrade available" link to see upgrade details, then click "Preview InstallPlan" button, and finally "Approve" to upgrade the Operator.
