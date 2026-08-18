# Deploy a cluster with community PostgreSQL images

!!! admonition "Version added: [3.1.0](ReleaseNotes/Kubernetes-Operator-for-PostgreSQL-RN3.1.0.md)"

You can run the Operator against **community PostgreSQL images**. Use community
images when you need extensions that are not included in Percona Distribution
for PostgreSQL, such as TimescaleDB or Citus.

Community PostgreSQL images are built from the official
PostgreSQL packages on [download.postgresql.org :octicons-link-external-16:](https://www.postgresql.org/download/)
(the PGDG repositories), so you can pull them from a registry you control
instead of relying only on Percona Distribution images. 

You can also [build and
publish your own community images](#build-your-own-community-images) and point the Operator at them.

This guide walks you through deploying the Operator and a PostgreSQL cluster using community PostgreSQL images. In this example, we use images from the [perconalab](https://hub.docker.com/repository/docker/perconalab/percona-postgresql-operator/) repository, which are intended for testing purposes only. For production environments, you should build, sign, and use your own images to ensure security and compliance.

The flow consist of two steps:

* First, install the Percona Operator for PostgreSQL Deployment.
* Next, use the Operator to create a PostgreSQL cluster.

## Known limitations

Community images do not include Percona-specific features such as Transparent
Data Encryption (TDE). Those features ship only with Percona Distribution for
PostgreSQL images.

If you need TDE or other Percona-specific features, follow the
[Quickstart](kubectl.md) and deploy the cluster with
[Percona certified images](images.md).

## Prerequisites

To deploy a cluster with community images, you need the following:

1. The **kubectl** tool to manage and deploy applications on Kubernetes. If it
   is not already installed, [follow the official installation instructions :octicons-link-external-16:](https://kubernetes.io/docs/tasks/tools/install-kubectl/).

2. A Kubernetes environment. You can deploy it on
   [Minikube :octicons-link-external-16:](https://github.com/kubernetes/minikube) for
   testing or use any cloud provider of your choice. Check the list of our
   [officially supported platforms](System-Requirements.md#supported-platforms).


## Procedure

Here's a sequence of steps to follow:
{.power-number}

1. Clone the `percona-postgresql-operator` repository. You will edit the
   cluster Custom Resource. Specify your desired version with the `-b` flag:

    ```bash
    git clone -b v{{ release }} https://github.com/percona/percona-postgresql-operator
    cd percona-postgresql-operator
    ```

2. Create the Kubernetes namespace for your cluster and export it as an environment variable. Isolating workloads in a
   custom namespace is a good practice. Replace the `<my-namespace>` placeholder with your value:

    ```bash
    kubectl create namespace <my-namespace>
    export NAMESPACE=<my-namespace>
    ```

    ??? example "Expected output"

        ``` {.text .no-copy}
        namespace/<my-namespace> was created
        ```


3. Create the Operator Deployment with the following command:

    ```bash
    kubectl apply --server-side -f deploy/bundle.yaml -n $NAMESPACE
    ```

    ??? example "Expected output"

        --8<-- "kubectl-apply-bundle-response.txt"

    At this point, the Operator Pod is up and running.

4. Edit `deploy/cr.yaml` and point the cluster at community images. Change
   these fields:
    
    * `postgresVersion` - Set to the required major version
    * `spec.image`, `spec.proxy.pgBouncer.image`, and
    `spec.backups.pgbackrest.image` - specify the community images for PostgreSQL, pgBouncer and pgbackrest.
    * Keep the rest of `deploy/cr.yaml`
    unchanged. The Operator manages instances, backups, replication
    and the rest of the cluster lifecycle the same way.
    
    This is the example for PostgreSQL 18:

    ```yaml
    apiVersion: pgv2.percona.com/v2
    kind: PerconaPGCluster
    metadata:
      name: cluster1
    spec:
      image: docker.io/percona/percona-postgresql-operator:postgresql{{postgresrecommended}}-community-ubi9
      postgresVersion: 18
      proxy:
        pgBouncer:
          image: docker.io/percona/percona-postgresql-operator:pgbouncer-community
      backups:
        pgbackrest:
          image: docker.io/percona/percona-postgresql-operator:pgbackrest-community
    ```

5. Deploy the cluster:

    ```bash
    kubectl apply -f deploy/cr.yaml -n $NAMESPACE
    ```

    ??? example "Expected output"

        ``` {.text .no-copy}
        perconapgcluster.pgv2.percona.com/cluster1 created
        ```

6. Check the Operator and cluster Pods status:

    ```bash
    kubectl get pg -n $NAMESPACE
    ```

    The creation process may take some time. When the process is over, your
    cluster obtains the `ready` status.

    ??? example "Expected output"

        ```{.text .no-copy}
        NAME       ENDPOINT                                   STATUS   POSTGRES   PGBOUNCER   AGE
        cluster1   cluster1-pgbouncer.postgres-operator.svc   ready    3          3           143m
        ```

You have successfully deployed the Operator with a PostgreSQL cluster that uses
community images.

## Available community images

The following UBI9 (EL9) images are published for evaluation:

```text
docker.io/perconalab/percona-postgresql-operator:main-postgres14-community
docker.io/perconalab/percona-postgresql-operator:main-postgres15-community
docker.io/perconalab/percona-postgresql-operator:main-postgres16-community
docker.io/perconalab/percona-postgresql-operator:main-postgres17-community
docker.io/perconalab/percona-postgresql-operator:main-postgres18-community
docker.io/perconalab/percona-postgresql-operator:main-pgbackrest-community
docker.io/perconalab/percona-postgresql-operator:main-pgbouncer-community
docker.io/perconalab/percona-postgresql-operator:main-upgrade-community
```

UBI8 (EL8) variants use a `main-ubi8-` prefix, for example
`main-ubi8-postgres18-community`.

## Build your own community images

The Dockerfile, package list, and sample build targets ship in
[percona-docker/postgresql-containers/community :octicons-link-external-16:](https://github.com/percona/percona-docker/tree/main/postgresql-containers/community) repository.

To build and push UBI9 images to your registry, use the following commands:

```bash
docker buildx create --use --name multiarch
git clone https://github.com/percona/percona-docker
cd percona-docker/postgresql-containers/community
make all TAG=1.0.0 REGISTRY=myrepo/percona-postgresql-operator
```

To build a single PostgreSQL major version, run:

```bash
make postgres17 TAG=1.0.0 REGISTRY=myrepo/percona-postgresql-operator
```

To build UBI8 variants, run:

```bash
make all-ubi8 TAG=1.0.0-ubi8 REGISTRY=myrepo/percona-postgresql-operator
```

`make all` builds the PostgreSQL, pgBouncer, and pgBackRest images so that they
stay version-aligned. After the images are in your registry, set
`spec.image`, `spec.proxy.pgBouncer.image`, and
`spec.backups.pgbackrest.image` in your Custom Resource to those paths.

For full build and contribution details, see the
[community containers README :octicons-link-external-16:](https://github.com/percona/percona-docker/blob/main/postgresql-containers/community/README.md)
and
[CONTRIBUTING.md :octicons-link-external-16:](https://github.com/percona/percona-docker/blob/main/postgresql-containers/community/CONTRIBUTING.md).

## See also

Percona Blog: [Community Docker Images: keeping the operator open without a vendor registry lock-in](https://www.percona.com/blog/postgresql-community-images-operator/)

## Next steps

[:simple-postgresql: Connect to PostgreSQL :material-arrow-right:](connect.md){.md-button}
