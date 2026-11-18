> For the complete documentation index, see [llms.txt](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/llms.txt).

# Install Percona Distribution for PostgreSQL on OpenShift

Percona Operator for PostgreSQL is a [Red Hat Certified Operator](https://connect.redhat.com/en/partner-with-us/red-hat-openshift-certification) . This means that Percona Operator is portable across hybrid clouds and fully supports the Red Hat OpenShift lifecycle.

To install Percona Distribution for PostgreSQL on OpenShift, you need to do the following:

1. First, install the Percona Operator for PostgreSQL Deployment.
1. Next, use the Operator to create Percona Distribution for PostgreSQL cluster.

## Installation options

You can install Percona Operator for PostgreSQL on OpenShift in two ways:

- **Using the [Operator Lifecycle Manager (OLM)](https://docs.redhat.com/en/documentation/openshift_container_platform/4.21/html/operators/understanding-operators#operator-lifecycle-manager-olm)** via the OpenShift web console
- **Using the command-line interface** with `oc` commands

Choose the method that best fits your workflow.

## Install via the Operator Lifecycle Manager (OLM)

Operator Lifecycle Manager (OLM) is a part of the [Operator Framework](https://github.com/operator-framework) that allows you to install, update, and manage the Operators lifecycle on the OpenShift platform.

### Prerequisites

Before you start, ensure you have the following:

1. You can log in to the OLM console
1. You have the ARN role assigned to your OLM user.

### Install the Operator Deployment

Follow these steps to deploy the Operator and Percona Distribution for PostgreSQL cluster:

1. Login to the OLM and navigate to the Software Catalog.

1. Search for the needed Operator and select it. You may need to change the project for your user:

   Then click “Continue”, and “Install”.

1. A new page opens where you specify the ARN role assigned to your user. You also choose the Operator version and the Namespace / OpenShift project you would like to install the Operator into.

   Note

   To install the Operator in [multi-namespace (cluster-wide) mode](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/cluster-wide.html), choose the value with the `-cw` suffix for the version, and select the “All namespaces on the cluster” radio button for the installation mode instead of choosing a specific Namespace:

   Click “Install” button to install the Operator.

1. You can track the installation flow by clicking the link on the updated page. You will be redirected to the Installed Operators tab. Your installed Operator will appear there.

### Deploy Percona Distribution for PostgreSQL

When the installation finishes, you can deploy PostgreSQL cluster.

1. In the “Operator Details” you will see Provided APIs (Custom Resources, available for installation). Click “Create instance” for the `PerconaPGCluster` Custom Resource.
1. You can either go with default settings or edit them as needed. You can use the form or edit the YAML manifest to set needed Custom Resource options.
1. Click the “Create” button to deploy your database cluster.

## Install via the command-line interface

The following steps install the latest version of the Operator with default parameters. To install a specific version, replace the `v3.1.0` tag with your value. See the full list of tags [in the Operator repository](https://github.com/percona/percona-postgresql-operator/tags) on GitHub.

To install the Operator with customized parameters, see [Install Percona Operator for PostgreSQL with customized parameters](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/custom-install.html).

Choose the approach that fits your needs:

- **Quick install** — Apply a single bundle file. Use this when you want to get started quickly with default settings.
- **Step-by-step install** — Run each installation step separately. Use this when you need to customize the installation (for example, apply the [anyuid](https://docs.openshift.com/container-platform/4.21/authentication/managing-security-context-constraints.html) security context constraint).

**Quick install**

The bundle file creates the Custom Resource Definition, sets up RBAC, and installs the Operator Deployment in one go.

1. Create the namespace for your cluster:

   ```
   oc create namespace postgres-operator
   ```

1. Export the namespace as an environment variable:

   ```
   export NAMESPACE=postgres-operator
   ```

1. Apply the bundle to install the Operator:

   ```
   oc apply --server-side -f https://raw.githubusercontent.com/percona/percona-postgresql-operator/v3.1.0/deploy/bundle.yaml -n $NAMESPACE
   ```

**Step-by-step install**

Install the Operator step by step if you wish to have more control over the installation process and modify the manifests before you apply them.

1. Clone the percona-postgresql-operator repository:

   ```
   git clone -b v3.1.0 https://github.com/percona/percona-postgresql-operator
   cd percona-postgresql-operator
   ```

1. Create the Custom Resource Definition (CRD). CRDs are cluster-scoped and apply to all namespaces. You don’t need to repeat this step for additional Operator deployments:

   ```
   oc apply --server-side -f deploy/crd.yaml
   ```

1. Create the namespace for your cluster (for example, `postgres-operator`):

   ```
   oc create namespace postgres-operator
   ```

1. Export the namespace as an environment variable:

   ```
   export NAMESPACE=postgres-operator
   ```

1. Apply RBAC configuration. Your user must have cluster-admin privileges:

   ```
   oc apply -f deploy/rbac.yaml -n $NAMESPACE
   ```

   Note

   For example, if you use Google OpenShift Engine, grant cluster-admin privileges with:

   ```
   oc create clusterrolebinding cluster-admin-binding --clusterrole=cluster-admin --user=$(gcloud config get-value core/account)
   ```

1. If you use the [anyuid](https://docs.openshift.com/container-platform/4.21/authentication/managing-security-context-constraints.html) security context constraint, modify the Operator manifest before applying:

   ```
   sed -i '/disable_auto_failover: "false"/a \ \ \ \ disable_fsgroup: "false"' deploy/operator.yaml
   ```

1. Create the Operator Deployment:

   ```
   oc apply -f deploy/operator.yaml -n $NAMESPACE
   ```

### Install Percona Distribution for PostgreSQL cluster

1. Create the Percona Distribution for PostgreSQL cluster:

   ```
   oc apply -f deploy/cr.yaml -n $NAMESPACE
   ```

1. Check the cluster status. Creation may take a few minutes:

   ```
   oc get pg -n $NAMESPACE
   ```

   Expected output

   ```
   NAME       ENDPOINT                                   STATUS  POSTGRES   PGBOUNCER   AGE
   cluster1   cluster1-pgbouncer.postgres-operator.svc   ready   3          3           143m
   ```

Optionally, you can add PostgreSQL Users secrets and TLS certificates before creating the cluster. If you don’t, the Operator creates them automatically. See [Users](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/users.html) and [TLS certificates](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/TLS.html) for details.

## Verifying the cluster operation

When creation process is over, `oc get pg` command will show you the cluster status as `ready`, and you can try to connect to the cluster.

When the Operator deploys a database cluster, it generates several [Secrets](https://kubernetes.io/docs/concepts/configuration/secret/) . Among them there is the Secret with the credentials of the default PostgreSQL user. This default user has the same username as the cluster name.

1. Use `oc get secrets -n <namespace>` command to see the list of Secrets objects. The Secrets object you are interested in is named in the format `<cluster_name>-pguser-<cluster_name>` (where the `<cluster_name>` is the [name of your Percona Distribution for PostgreSQL Cluster](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/operator.html#metadata-name)). For example, if your cluster name is `cluster1`, the Secret name will be `cluster1-pguser-cluster1`.

1. Use the following command to get the password of this user. Replace the `<cluster_name>` and `<namespace>` placeholders with your values:

   ```
   oc get secret <cluster_name>-<user_name>-<cluster_name> -n <namespace> --template='{{.data.password | base64decode}}{{"\n"}}'
   ```

1. To connect to PostgreSQL, you will use the `pgbouncer` service as the entry point to your cluster. To find this service, use the following command:

   ```
   kubectl get svc -n <namespace>
   ```

   Look for the service named `<cluster-name>-pgbouncer`.

   Sample output

   ```
   cluster1-ha          ClusterIP   34.118.234.155   <none>        5432/TCP   51m
   cluster1-ha-config   ClusterIP   None             <none>        <none>     51m
   cluster1-pgbouncer   ClusterIP   34.118.239.5     <none>        5432/TCP   51m
   cluster1-pods        ClusterIP   None             <none>        <none>     51m
   cluster1-primary     ClusterIP   None             <none>        5432/TCP   51m
   cluster1-replicas    ClusterIP   34.118.234.19    <none>        5432/TCP   51m
   ```

1. Create a pod and start Percona Distribution for PostgreSQL inside. The following command will do this, naming the new Pod `pg-client`:

   ```
   oc run -n <namespace> -i --rm --tty pg-client --image=percona/percona-distribution-postgresql:18.6.1-3 --restart=Never -- bash -il
   ```

   It may require some time to execute the command and deploy the corresponding Pod.

1. Run a container with `psql` tool and connect its console output to your terminal. Substitute the `<namespace>` placeholder with your value in the following command to connect as a `cluster1` user to the `cluster1` database via the PostgreSQL interactive terminal.

   ```
   [postgres@pg-client /]$ PGPASSWORD='pguser_password' psql -h cluster1-pgbouncer.<namespace>.svc.cluster.local -p 5432 -U cluster1 cluster1
   ```

   Sample output

   ```
   psql (18.6.1-3)
   SSL connection (protocol: TLSv1.3, cipher: TLS_AES_256_GCM_SHA384, bits: 256, compression: off)
   Type "help" for help.
   pgdb=>
   ```
