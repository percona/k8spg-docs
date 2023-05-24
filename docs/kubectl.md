# Install Percona Distribution for PostgreSQL using kubectl

The [kubectl](https://kubernetes.io/docs/tasks/tools/) command line utility is a tool used before anything else to interact with Kubernetes and containerized applications running on it. Users can run kubectl to deploy applications, manage cluster resources, check logs, etc.

## Pre-requisites

The following tools are used in this guide and therefore should be preinstalled:

1. The **Git** distributed version control system. You can install it following the [official installation instructions](https://github.com/git-guides/install-git).

2. The **kubectl** tool to manage and deploy applications on Kubernetes, included in most Kubernetes distributions. Install it, if not present, [following the official installation instructions](https://kubernetes.io/docs/tasks/tools/install-kubectl/).

## Install the Operator and Percona Distribution for PostgreSQL

The following steps are needed to deploy the Operator and Percona Distribution for PostgreSQL in
your Kubernetes environment:

1. Deploy the Operator with the following command:

    ```{.bash data-prompt="$" }
    $ kubectl apply --server-side -f https://raw.githubusercontent.com/percona/percona-postgresql-operator/v{{ release }}/deploy/bundle.yaml
    ```

    ??? example "Expected output"

        ```{.text .no-copy}
        customresourcedefinition.apiextensions.k8s.io/perconapgbackups.pg.percona.com serverside-applied
        customresourcedefinition.apiextensions.k8s.io/perconapgclusters.pg.percona.com serverside-applied
        customresourcedefinition.apiextensions.k8s.io/perconapgrestores.pg.percona.com serverside-applied
        customresourcedefinition.apiextensions.k8s.io/postgresclusters.postgres-operator.crunchydata.com serverside-applied
        serviceaccount/percona-postgresql-operator serverside-applied
        role.rbac.authorization.k8s.io/percona-postgresql-operator serverside-applied
        rolebinding.rbac.authorization.k8s.io/service-account-percona-postgresql-operator serverside-applied
        deployment.apps/percona-postgresql-operator serverside-applied
        ```

    As the result you will have the Operator Pod up and running.

3. Deploy Percona Distribution for PostgreSQL:

    ```{.bash data-prompt="$" }
    $ kubectl apply -f https://raw.githubusercontent.com/percona/percona-postgresql-operator/v{{ release }}/deploy/cr.yaml
    ```

    ??? example "Expected output"

        ```{.text .no-copy}
        perconapgcluster.pg.percona.com/cluster1 created
        ```

    !!! note

        This deploys default Percona Distribution for PostgreSQL configuration.
        Please see [deploy/cr.yaml](https://raw.githubusercontent.com/percona/percona-postgresql-operator/v{{ release }}/deploy/cr.yaml)
        and [Custom Resource Options](operator.md) for the configuration
        options. You can clone the repository with all manifests and source code
        by executing the following command:

        ```{.bash data-prompt="$" }
        $ git clone -b v{{ release }} https://github.com/percona/percona-postgresql-operator
        ```

        After editing the needed options, apply your modified `deploy/cr.yaml`
        file as follows:

        ```{.bash data-prompt="$" }
        $ kubectl apply -f deploy/cr.yaml
        ```

    Creation process will take some time. The process is over when both
    Operator and replica set Pods have reached their Running status:

    ``` {.bash data-prompt="$" }
    $ kubectl get pg
    ```

    ??? example "Expected output"

        ```{.text .no-copy}
        NAME       ENDPOINT                     STATUS   POSTGRES   PGBOUNCER   AGE
        cluster1   cluster1-pgbouncer.pgo.svc   ready    3          3           143m
        ```

## Verifying the cluster operation

When creation process is over, `kubectl get pg` command will show you the
cluster status as `ready`, and you can try to connect to the cluster.

{% include 'assets/fragments/connectivity.txt' %}
