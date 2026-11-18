> For the complete documentation index, see [llms.txt](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/llms.txt).

# Deploy a cluster with community PostgreSQL images

Version added: [3.1.0](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/ReleaseNotes/Kubernetes-Operator-for-PostgreSQL-RN3.1.0.html)

You can run the Operator against **community PostgreSQL images**. Use community images when you need extensions that are not included in Percona Distribution for PostgreSQL, such as TimescaleDB or Citus.

Community PostgreSQL images are built from the official PostgreSQL packages on [download.postgresql.org](https://www.postgresql.org/download/) (the PGDG repositories), so you can pull them from a registry you control instead of relying only on Percona Distribution images.

You can also [build and publish your own community images](#build-your-own-community-images) and point the Operator at them.

This guide walks you through deploying the Operator and a PostgreSQL cluster using community PostgreSQL images. The image tags in this guide are for evaluation. For production environments, you should build, sign, and use your own images to ensure security and compliance.

The flow consist of two steps:

- First, install the Percona Operator for PostgreSQL Deployment.
- Next, use the Operator to create a PostgreSQL cluster.

## Known limitations

Community images do not include Percona-specific features such as Transparent Data Encryption (TDE). Those features ship only with Percona Distribution for PostgreSQL images.

If you need TDE or other Percona-specific features, follow the [Quickstart](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/kubectl.html) and deploy the cluster with [Percona certified images](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/images.html).

## Prerequisites

To deploy a cluster with community images, you need the following:

1. The **kubectl** tool to manage and deploy applications on Kubernetes. If it is not already installed, [follow the official installation instructions](https://kubernetes.io/docs/tasks/tools/install-kubectl/) .
1. A Kubernetes environment. You can deploy it on [Minikube](https://github.com/kubernetes/minikube) for testing or use any cloud provider of your choice. Check the list of our [officially supported platforms](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/System-Requirements.html#supported-platforms).

## Procedure

Here’s a sequence of steps to follow:

1. Clone the `percona-postgresql-operator` repository. You will edit the cluster Custom Resource. Specify your desired version with the `-b` flag:

   ```
   git clone -b v3.1.0 https://github.com/percona/percona-postgresql-operator
   cd percona-postgresql-operator
   ```

1. Create the Kubernetes namespace for your cluster and export it as an environment variable. Isolating workloads in a custom namespace is a good practice. Replace the `<my-namespace>` placeholder with your value:

   ```
   kubectl create namespace <my-namespace>
   export NAMESPACE=<my-namespace>
   ```

   Expected output

   ```
   namespace/<my-namespace> was created
   ```

1. Create the Operator Deployment with the following command:

   ```
   kubectl apply --server-side -f deploy/bundle.yaml -n $NAMESPACE
   ```

   Expected output

   ```
   customresourcedefinition.apiextensions.k8s.io/crunchybridgeclusters.postgres-operator.crunchydata.com serverside-applied
   customresourcedefinition.apiextensions.k8s.io/perconapgbackups.pgv2.percona.com serverside-applied
   customresourcedefinition.apiextensions.k8s.io/perconapgclusters.pgv2.percona.com serverside-applied
   customresourcedefinition.apiextensions.k8s.io/perconapgrestores.pgv2.percona.com serverside-applied
   customresourcedefinition.apiextensions.k8s.io/perconapgupgrades.pgv2.percona.com serverside-applied
   customresourcedefinition.apiextensions.k8s.io/pgadmins.postgres-operator.crunchydata.com serverside-applied
   customresourcedefinition.apiextensions.k8s.io/pgupgrades.postgres-operator.crunchydata.com serverside-applied
   customresourcedefinition.apiextensions.k8s.io/postgresclusters.postgres-operator.crunchydata.com serverside-applied
   serviceaccount/percona-postgresql-operator serverside-applied
   role.rbac.authorization.k8s.io/percona-postgresql-operator serverside-applied
   rolebinding.rbac.authorization.k8s.io/service-account-percona-postgresql-operator serverside-applied
   deployment.apps/percona-postgresql-operator serverside-applied
   ```

   At this point, the Operator Pod is up and running.

1. Edit `deploy/cr.yaml` and point the cluster at community images. Change these fields:

   - `postgresVersion` - Set to the required major version
   - `spec.image`, `spec.proxy.pgBouncer.image`, and `spec.backups.pgbackrest.image` - specify the community images for PostgreSQL, pgBouncer and pgbackrest.
   - Keep the rest of `deploy/cr.yaml` unchanged. The Operator manages instances, backups, replication and the rest of the cluster lifecycle the same way.

   This is the example for PostgreSQL 18:

   ```
   apiVersion: pgv2.percona.com/v2
   kind: PerconaPGCluster
   metadata:
     name: cluster1
   spec:
     image: docker.io/percona/percona-postgresql-operator:postgresql18.6-1-community-ubi9
     postgresVersion: 18
     proxy:
       pgBouncer:
         image: docker.io/percona/percona-postgresql-operator:pgbouncer1.25.2-43-community
     backups:
       pgbackrest:
         image: docker.io/percona/percona-postgresql-operator:pgbackrest2.59.1-1-community
   ```

1. Deploy the cluster:

   ```
   kubectl apply -f deploy/cr.yaml -n $NAMESPACE
   ```

   Expected output

   ```
   perconapgcluster.pgv2.percona.com/cluster1 created
   ```

1. Check the Operator and cluster Pods status:

   ```
   kubectl get pg -n $NAMESPACE
   ```

   The creation process may take some time. When the process is over, your cluster obtains the `ready` status.

   Expected output

   ```
   NAME       ENDPOINT                                   STATUS   POSTGRES   PGBOUNCER   AGE
   cluster1   cluster1-pgbouncer.postgres-operator.svc   ready    3          3           143m
   ```

You have successfully deployed the Operator with a PostgreSQL cluster that uses community images.

## Available community images

Published evaluation images live under `docker.io/percona/percona-postgresql-operator`. Use the UBI 9 tags in the example above, or the UBI 8 tags if you need Enterprise Linux 8.

See [PostgreSQL community images](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/images-community.html) for the full list of tags and digests, including the shared pgBouncer and pgBackRest images.

## Build your own community images

The Dockerfile, package list, and sample build targets ship in [percona-docker/postgresql-containers/community](https://github.com/percona/percona-docker/tree/main/postgresql-containers/community) repository.

To build and push UBI9 images to your registry, use the following commands:

```
docker buildx create --use --name multiarch
git clone https://github.com/percona/percona-docker
cd percona-docker/postgresql-containers/community
make all TAG=1.0.0 REGISTRY=myrepo/percona-postgresql-operator
```

To build a single PostgreSQL major version, run:

```
make postgres17 TAG=1.0.0 REGISTRY=myrepo/percona-postgresql-operator
```

To build UBI8 variants, run:

```
make all-ubi8 TAG=1.0.0-ubi8 REGISTRY=myrepo/percona-postgresql-operator
```

`make all` builds the PostgreSQL, pgBouncer, and pgBackRest images so that they stay version-aligned. After the images are in your registry, set `spec.image`, `spec.proxy.pgBouncer.image`, and `spec.backups.pgbackrest.image` in your Custom Resource to those paths.

For full build and contribution details, see the [community containers README](https://github.com/percona/percona-docker/blob/main/postgresql-containers/community/README.md) and [CONTRIBUTING.md](https://github.com/percona/percona-docker/blob/main/postgresql-containers/community/CONTRIBUTING.md) .

## See also

Percona Blog: [Community Docker Images: keeping the operator open without a vendor registry lock-in](https://www.percona.com/blog/postgresql-community-images-operator/)

## Next steps

[Connect to PostgreSQL](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/connect.html)
