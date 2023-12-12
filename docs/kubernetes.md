# Install Percona Distribution for PostgreSQL on Kubernetes

Following steps will allow you to install the Operator and use it to manage
Percona Distribution for PostgreSQL in a Kubernetes-based environment.
{.power-number}

1. First of all, clone the percona-postgresql-operator repository:

    ``` {.bash data-prompt="$" }
    $ git clone -b v{{ release }} https://github.com/percona/percona-postgresql-operator
    $ cd percona-postgresql-operator
    ```

    !!! note

        It is crucial to specify the right branch with `-b` option while cloning the
        code on this step. Please be careful.

2. The Custom Resource Definition for Percona Distribution for PostgreSQL should
    be created from the `deploy/crd.yaml` file. Custom Resource Definition
    extends the standard set of resources which Kubernetes “knows” about with
    the new items (in our case ones which are the core of the Operator).
    [Apply it](https://kubernetes.io/docs/reference/using-api/server-side-apply/)
    as follows:

    ``` {.bash data-prompt="$" }
    $ kubectl apply --server-side -f deploy/crd.yaml
    ```

    This step should be done only once; it does not need to be repeated with any
    other Operator deployments.

3. Create the Kubernetes namespace for your cluster if needed (for example,
    let's name it `postgres-operator`):

     ``` {.bash data-prompt="$" }
     $ kubectl create namespace postgres-operator
     ```

     !!! note

         To use different namespace, specify other name instead of
         `postgres-operator` in the above command, and modify the 
         `-n postgres-operator` parameter with it in the following two steps.
         You can also omit this parameter completely to deploy everything in the
         `default` namespace.

4. The role-based access control (RBAC) for Percona Distribution for PostgreSQL
    is configured with the `deploy/rbac.yaml` file. Role-based access is based
    on defined roles and the available actions which correspond to each role.
    The role and actions are defined for Kubernetes resources in the yaml file.
    Further details about users and roles can be found in [Kubernetes documentation](https://kubernetes.io/docs/reference/access-authn-authz/rbac/#default-roles-and-role-bindings).

    ``` {.bash data-prompt="$" }
    $ kubectl apply -f deploy/rbac.yaml -n postgres-operator
    ```

    !!! note

        Setting RBAC requires your user to have cluster-admin role
        privileges. For example, those using Google Kubernetes Engine can
        grant user needed privileges with the following command:

        ```default
        $ kubectl create clusterrolebinding cluster-admin-binding --clusterrole=cluster-admin --user=$(gcloud config get-value core/account)
        ```

5. Start the Operator within Kubernetes:

    ``` {.bash data-prompt="$" }
    $ kubectl apply -f deploy/operator.yaml -n postgres-operator
    ```

    Optionally, you can add PostgreSQL Users secrets and TLS certificates to
    Kubernetes. If you don't, the Operator will create the needed users and
    certificates automatically, when you create the database cluster. You can
    see documentation on [Users](users.md) and [TLS certificates](TLS.md) if
    still want to create them yourself.

6. After the Operator is started Percona Distribution for PostgreSQL cluster can
    be created at any time with the following command:

    ``` {.bash data-prompt="$" }
    $ kubectl apply -f deploy/cr.yaml -n postgres-operator
    ```

    The creation process may take some time. When the process is over your
    cluster will obtain the `ready` status. You can check it with the following
    command:

    ``` {.bash data-prompt="$" }
    $ kubectl get pg -n postgres-operator
    ```

    ??? example "Expected output"

        --8<-- "kubectl-get-pg-response.txt"

## Verifying the cluster operation

When creation process is over, `kubectl get pg` command will show you the
cluster status as `ready`, and you can try to connect to the cluster.

{% include 'assets/fragments/connectivity.txt' %}

## Deleting the cluster

If you need to delete the cluster (for example, to clean up the testing
deployment before adopting it for production use), check [this HowTo](delete.md).
