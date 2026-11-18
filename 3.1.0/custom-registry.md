> For the complete documentation index, see [llms.txt](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/llms.txt).

# Use Docker images from a private registry

Using images from a private Docker registry may be required for privacy, security or other reasons. In these cases, Percona Operator for PostgreSQL allows the use of a custom registry. The following example illustrates how this can be done by the example of the Operator deployed in the OpenShift environment.

## Prerequisites

1. First of all login to the OpenShift and create project.

   ```
   oc login
   Authentication required for https://192.168.1.100:8443 (openshift)
   Username: admin
   Password:
   Login successful.
   oc new-project pg
   Now using project "pg" on server "https://192.168.1.100:8443".
   ```

1. There are two things you will need to configure your custom registry access:

   - the token for your user,
   - your registry IP address.

   The token can be found with the following command:

   ```
   oc whoami -t
   ADO8CqCDappWR4hxjfDqwijEHei31yXAvWg61Jg210s
   ```

   And the following one tells you the registry IP address:

   ```
   kubectl get services/docker-registry -n default
   NAME              TYPE        CLUSTER-IP       EXTERNAL-IP   PORT(S)    AGE
   docker-registry   ClusterIP   172.30.162.173   <none>        5000/TCP   1d
   ```

1. Use the user token and the registry IP address to login to the registry:

   ```
   docker login -u admin -p ADO8CqCDappWR4hxjfDqwijEHei31yXAvWg61Jg210s 172.30.162.173:5000
   ```

   Expected output

   ```
   Login Succeeded
   ```

1. Use the Docker commands to pull the needed image by its SHA digest:

   ```
   docker pull docker.io/perconalab/percona-postgresql-operator@sha256:991d6049059e5eb1a74981290d829a5fb4ab0554993748fde1e67b2f46f26bf0
   ```

   Expected output

   ```
   Trying to pull repository docker.io/perconalab/percona-postgresql-operator ...
   sha256:991d6049059e5eb1a74981290d829a5fb4ab0554993748fde1e67b2f46f26bf0: Pulling from docker.io/perconalab/percona-server-mongodb
   Digest: sha256:991d6049059e5eb1a74981290d829a5fb4ab0554993748fde1e67b2f46f26bf0
   Status: Image is up to date for docker.io/perconalab/percona-postgresql-operator@sha256:991d6049059e5eb1a74981290d829a5fb4ab0554993748fde1e67b2f46f26bf0
   ```

   You can find correct names and SHA digests in the [current list of the Operator-related images officially certified by Percona](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/images.html).

1. The following method can push an image to the custom registry for the example OpenShift `pg` project:

   ```
   docker tag \
       docker.io/perconalab/percona-postgresql-operator@sha256:991d6049059e5eb1a74981290d829a5fb4ab0554993748fde1e67b2f46f26bf0 \
       172.30.162.173:5000/psmdb/percona-postgresql-operator:18.6.1-3
   docker push 172.30.162.173:5000/pg/percona-postgresql-operator:18.6.1-3
   ```

1. Verify the image is available in the OpenShift registry with the following command:

   ```
   oc get is
   ```

   Expected output

   ```
   NAME                              DOCKER REPO                                                             TAGS             UPDATED
   percona-postgresql-operator       docker-registry.default.svc:5000/pg/percona-postgresql-operator  18.6.1-3  2 hours ago
   ```

1. When the custom registry image is available, edit the the `image:` option in `deploy/operator.yaml` configuration file with a Docker Repo + Tag string (it should look like `docker-registry.default.svc:5000/pg/percona-postgresql-operator:18.6.1-3`)

   Note

   If the registry requires authentication, you can specify the `imagePullSecrets` option for all images.

1. Repeat steps 3-5 for other images, and update corresponding options in the `deploy/cr.yaml` file.

1. Now follow the standard Percona Operator for PostgreSQL [installation instruction](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/openshift.html).
