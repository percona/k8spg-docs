# Percona Operator for PostgreSQL single-namespace and multi-namespace deployment

There are two design patterns that you can choose from when deploying Percona Operator for PostgreSQL and PostgreSQL clusters in Kubernetes:

* Namespace-scope - one Operator per Kubernetes namespace,

* Cluster-wide - one Operator can manage clusters in multiple namespaces.

This how-to explains how to configure Percona Operator for PostgreSQL for each scenario.

## Namespace-scope

By default, Percona Operator for PostgreSQL functions in a specific Kubernetes namespace. You can
create one during installation (like it is shown in the
[installation instructions](kubernetes.md#install-kubernetes)) or just use the default namespace. This approach allows several Operators to co-exist in one Kubernetes-based environment, being separated in different namespaces:

![image](assets/images/cluster-wide-1.svg)

Normally this is a recommended approach, as isolation minimizes impact in case of various failure scenarios. This is the default configuration of our Operator.

Let’s say you have a Namespace in your Kubernetes cluster called `percona-db-1`.

1. Create your `percona-db-1` namespace (if it doesn't yet exist) as follows:

    ``` {.bash data-prompt="$" }
    $ kubectl create namespace percona-db-1
    ```

2. Deploy the Operator:

    ``` {.bash data-prompt="$" }
    $ kubectl apply -f deploy/operator.yaml -n percona-db-1
    ```

3. Once Operator is up and running, deploy the database cluster itself:

    ``` {.bash data-prompt="$" }
    $ kubectl apply -f deploy/cr.yaml -n percona-db-1
    ```

You can deploy multiple clusters in this namespace.

### Add more namespaces

What if there is a need to deploy clusters in another namespace? The solution for namespace-scope deployment is to have more than one Operator. We will use the `percona-db-2` namespace as an example.

1. Create your `percona-db-2` namespace (if it doesn't yet exist) as follows:

    ``` {.bash data-prompt="$" }
    $ kubectl create namespace percona-db-2
    ```

2. Deploy the Operator:

    ``` {.bash data-prompt="$" }
    $ kubectl apply -f deploy/operator.yaml -n percona-db-2
    ```

3. Once Operator is up and running deploy the database cluster itself:

    ``` {.bash data-prompt="$" }
    $ kubectl apply -f deploy/cr.yaml -n percona-db-2
    ```

    !!! note

        Cluster names may be the same in different namespaces.

## Install the Operator cluster-wide

Sometimes it is more convenient to have one Operator watching for
Percona Distribution for PostgreSQL custom resources in several namespaces.

We recommend running Percona Operator for PostgreSQL in a traditional way,
limited to a specific namespace, to limit the blast radius. But it is possible
to run it in so-called *cluster-wide* mode, one Operator watching several
namespaces, if needed:

![image](assets/images/cluster-wide-2.svg)

To use the Operator in such cluster-wide mode, you should install it with a
different set of configuration YAML files, which are available in the deploy
folder and have filenames with a special `cw-` prefix: e.g.
`deploy/cw-bundle.yaml`.

Using `cw-*` manifests will create a new namespace (`pg-operator` by default),
deploy the Operator into it. Deployed this way, the Operator will start
monitoring all namespaces for `PerconaPGCluster` custom resources.

1. Clone `percona-postgresql-operator` repository:

    ``` {.bash data-prompt="$" }
    $ git clone -b v{{ release }} https://github.com/percona/percona-postgresql-operator
    $ cd percona-postgresql-operator
    ```

2. Deploy the bundle. It will create the `pg-operator` namespace, and deploy the
    Operator into it.

    ``` {.bash data-prompt="$" }
    $ kubectl apply -f deploy/cw-bundle.yaml –server-side
    ```

    !!! note

        If you want to change the namespace, please edit
        **all** `pg-operator` **namespace entries** in `cw-bundle.yaml` before
        applying. The entries to edit may look as follows:

        ```yaml
        apiVersion: v1
        kind: Namespace
        metadata:
          name: pg-operator
        ...
        ---
        apiVersion: v1
        kind: ServiceAccount
        metadata:
          name: percona-postgresql-operator
          namespace: pg-operator
        ...
        ---
        apiVersion: rbac.authorization.k8s.io/v1
        kind: ClusterRoleBinding
        ...
        subjects:
        - kind: ServiceAccount
          name: percona-postgresql-operator
          namespace: pg-operator
        ---
        apiVersion: apps/v1
        kind: Deployment
        ...
          name: percona-postgresql-operator
          namespace: pg-operator
        ...
        ```

    Right now the operator deployed in cluster-wide mode will monitor all
    namespaces in the cluster, either already existing or newly created ones.

3. Switch to the namespace you have chosen for the cluster (don't forget to
    create it if needed). let's call it `percona-db-1` for example:
    
    ``` {.bash data-prompt="$" }
    $ kubectl create namespace percona-db-1
    $ kubectl config set-context $(kubectl config current-context) --namespace=percona-db-1
    ``
    
4.  Deploy the cluster in the namespace of your choice:

    ``` {.bash data-prompt="$" }
    $ kubectl apply -f deploy/cr.yaml
    ```

## Verifying the cluster operation

When creation process is over, you can try to connect to the cluster.

{% include 'assets/fragments/connectivity.txt' %}


