> For the complete documentation index, see [llms.txt](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/llms.txt).

# Use PostGIS extension with Percona Distribution for PostgreSQL

[PostGIS](https://postgis.net/) is a PostgreSQL extension that adds GIS capabilities to this database.

You can deploy and manage PostGIS-enabled PostgreSQL starting from the Operator version 2.3.0. Here’s how to do it:

## Prepare your environment

1. Clone the `percona-postgresql-operator` repository because you will need to modify the cluster’s Custom Resource. Specify your desired version for the `-b` flag:

   ```
   git clone -b v3.1.0 https://github.com/percona/percona-postgresql-operator
   cd percona-postgresql-operator
   ```

1. Create the namespace where the Operator and the cluster will run. Export it as an environment variable. Replace the `<namespace>` placeholder with your value:

   ```
   kubectl create namespace <namespace>
   export NAMESPACE=<namespace>
   ```

## Deploy Percona Operator for PostgreSQL

Create the Custom Resource Definition, role-based access control (RBAC) and the Operator deployment. To do that in one go, apply the `deploy/bundle.yaml` manifest:

```
kubectl apply --server-side -f deploy/bundle.yaml -n $NAMESPACE
```

## Deploy PostGIS-enabled database cluster

1. Modify the `deploy/cr.yaml` configuration file. Specify the image for PostGIS in the `spec.image` option. Use `docker.io/percona/percona-distribution-postgresql-with-postgis:18.6.1-3` instead of `docker.io/percona/percona-distribution-postgresql:18.6.1-3`

   ```
   apiVersion: pgv2.percona.com/v2
   kind: PerconaPGCluster
   metadata:
     name: cluster1
   spec:
     ...
     image: docker.io/percona/percona-distribution-postgresql-with-postgis:18.6.1-3
     ...
   ```

1. Create a cluster with the following command:

   ```
   kubectl apply -f deploy/cr.yaml -n $NAMESPACE
   ```

1. The creation process may take some time. Check the cluster status with the following command:

   ```
   kubectl get pg -n $NAMESPACE
   ```

   When the process is over your cluster will obtain the `ready` status.

   Expected output

   ```
   NAME       ENDPOINT                         STATUS   POSTGRES   PGBOUNCER   AGE
   cluster1   cluster1-pgbouncer.default.svc   ready    3          3           30m
   ```

## Enable PostGIS extension

To use the PostGIS extension, you should enable it for specific databases. To do that, your PostgreSQL user must be a superuser because only superusers can create extensions. By default, the Operator creates a standard database user without superuser privileges. You have several options to enable PostGIS in your databases:

1. **Connect as the `postgres` superuser to the primary Pod**. When you execute to the primary Pod and establish the `psql` session, you are connected as the `postgres` user. Then you can create or alter databases and enable the PostGIS extension as needed.
1. **Grant superuser privileges to the default user**. Connect to the database Pod as the `postgres` user and grant superuser privileges to the default Operator-created user. After this, you can log in with this user and enable the PostGIS extension for the databases this user has access to.
1. **Create a separate superuser**. You can create a dedicated superuser with access to the needed databases via the Custom Resource. Use this user to connect to PostgreSQL and enable the PostGIS extension for the databases this user has access to.

Note

By default, superusers cannot connect to PostgreSQL via `pgBouncer` due to security restrictions. To connect to PostgreSQL as the superuser you can:

- Update the `pgBouncer` configuration to allow superuser access (not recommended for general security reasons), or
- Connect to PostgreSQL primary Pod using the `<cluster-name>-primary` Kubernetes Service bypassing `pgBouncer`.

For details on managing users, roles, and configuring `pgBouncer` access, refer to the [Application and system users](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/users.html) documentation.

### Option 1. Connect to the primary Pod

1. Find the primary Pod:

   ```
   kubectl get pods -n $NAMESPACE -l postgres-operator.crunchydata.com/role=primary
   ```

   Sample output

   ```
   NAME                        READY   STATUS    RESTARTS   AGE
   cluster1-instance1-ccsr-0   4/4     Running   0          14m
   ```

1. Exec into the primary Pod and establish the `psql` session:

   ```
   kubectl -n $NAMESPACE exec -it <primary-pod-name> -- psql
   ```

1. For example, you can create the new database named `mygisdata` as follows:

   ```
   CREATE database mygisdata;
   ```

1. Connect to this database and create a schema to separate your spacial data.

   ```
   \c mygisdata;
   CREATE SCHEMA gis;
   ```

1. Enable the `postgis` extension for this database. Make sure you are connected to the database you created earlier and run the following command:

   ```
   CREATE EXTENSION postgis;
   ```

1. Check that the extension is enabled:

   ```
   SELECT postgis_full_version();
   ```

   The output should resemble the following:

   Expected output

   ```
   postgis_full_version
   -----------------------------------------------------------------------------------------------------------------------------------------------------------------
   POSTGIS="3.5.5 0" [EXTENSION] PGSQL="170" GEOS="3.11.2-CAPI-1.17.2" PROJ="9.5.1 NETWORK_ENABLED=OFF
   URL_ENDPOINT=https://cdn.proj.org USER_WRITABLE_DIRECTORY=/tmp/proj DATABASE_PATH=/usr/proj95/share/proj/proj.db" (compiled against PROJ 9.5.1) LIBXML="2.9.13" LIBJSON="0.14" LIBPROTOBUF="1.3.3" WAGYU="0.5.0 (Internal)"
   ```

### Option 2. Grant superuser privileges to default user

1. Connect to the primary Pod following the steps from [Option 1](#option-1-connect-to-the-primary-pod)

1. Grant your default user superuser privileges. The following command updates privileges for the `cluster1` user. Replace with your user name of needed:

   ```
   ALTER USER cluster1 WITH SUPERUSER;
   ```

   Exit the pod.

1. Retrieve the connection string URL from a Secret. List the Secrets:

   ```
   kubectl get secrets -n $NAMESPACE
   ```

   Look for the Secret named after this pattern: `<cluster-name>-pguser-<username>`. For example, if your cluster name is `cluster1`, the Secret name is `cluster1-pguser-cluster1`.

1. The `data.uri` value in the Secret contains the connection string URL to the primary service. Export it as an environment variable:

   ```
   URI=$(kubectl get secret `<cluster-name>-pguser-<username>` --namespace $NAMESPACE -o jsonpath='{.data.uri}' | base64 --decode) | echo $URI
   ```

1. Create a Pod where you start Percona Distribution for PostgreSQL and connect to the database. The following command starts a Pod `pg-client` and connects it to the database using the connection string URL:

   ```
   kubectl run -i --rm --tty pg-client --image=perconalab/percona-distribution-postgresql:18.6.1-3 --restart=Never -- psql $URI
   ```

   Sample output

   ```
   cluster1=#
   ```

1. When the Operator creates a user, it also creates the database and schema with the name that matches the username. You are now connected to this database. Create the `postgis` extension for it.

   ```
   CREATE EXTENSION postgis;
   ```

1. Check that the extension is enabled:

   ```
   SELECT postgis_full_version();
   ```

   The output should resemble the following:

   Expected output

   ```
   postgis_full_version
   -----------------------------------------------------------------------------------------------------------------------------------------------------------------
   POSTGIS="3.5.5 0" [EXTENSION] PGSQL="170" GEOS="3.11.2-CAPI-1.17.2" PROJ="9.5.1 NETWORK_ENABLED=OFF
   URL_ENDPOINT=https://cdn.proj.org USER_WRITABLE_DIRECTORY=/tmp/proj DATABASE_PATH=/usr/proj95/share/proj/proj.db" (compiled against PROJ 9.5.1) LIBXML="2.9.13" LIBJSON="0.14" LIBPROTOBUF="1.3.3" WAGYU="0.5.0 (Internal)"
   ```

### Option 3. Create a dedicated superuser

1. Edit the Custom Resource and add a user that you will use to manage spatial data. For example, this user is called `gis`. List the databases this user has access to and grant it superuser privileges:

   ```
   spec:
     users:
       - name: gis
         databases:
           - mygisdata
           - test
         options: "SUPERUSER"
   ```

1. Update the cluster configuration:

   ```
   kubectl apply -f deploy/cr.yaml -n $NAMESPACE
   ```

1. The Operator creates a user and a Secret object with user credentials named `<cluster-name>-pguser-<username>`. List the Secrets to verify it is created:

   ```
   kubectl get secrets -n $NAMESPACE
   ```

1. Retrieve the connection string URI to the primary Pod from the Secret and export it as an environment variable:

   ```
   URI=$(kubectl get secret `<cluster-name>-pguser-<username>` --namespace $NAMESPACE -o jsonpath='{.data.uri}' | base64 --decode) | echo $URI
   ```

1. Create a Pod where you start Percona Distribution for PostgreSQL and use it to connect to the database. The following command starts a Pod `pg-client` and connects it to the database using the connection string URL:

   ```
   kubectl run -i --rm --tty pg-client --image=perconalab/percona-distribution-postgresql:18.6.1-3 --restart=Never -- psql $URI
   ```

   Sample output

   ```
   mygisdata=#
   ```

1. When the Operator creates a user, it also creates the database and schema with the name that matches the username. You are now connected to this database. Create the `postgis` extension for it.

   ```
   CREATE EXTENSION postgis;
   ```

1. Check that the extension is enabled:

   ```
   SELECT postgis_full_version();
   ```

   The output should resemble the following:

   Expected output

   ```
   postgis_full_version
   -----------------------------------------------------------------------------------------------------------------------------------------------------------------
   POSTGIS="3.5.5 0" [EXTENSION] PGSQL="170" GEOS="3.11.2-CAPI-1.17.2" PROJ="9.5.1 NETWORK_ENABLED=OFF
   URL_ENDPOINT=https://cdn.proj.org USER_WRITABLE_DIRECTORY=/tmp/proj DATABASE_PATH=/usr/proj95/share/proj/proj.db" (compiled against PROJ 9.5.1) LIBXML="2.9.13" LIBJSON="0.14" LIBPROTOBUF="1.3.3" WAGYU="0.5.0 (Internal)"
   ```

You can find more about using PostGIS in the official Percona Distribution for PostgreSQL [documentation](https://docs.percona.com/postgresql/latest/solutions/postgis-deploy.html) , as well as in this [blogpost](https://www.percona.com/blog/working-with-postgresql-and-postgis-how-to-become-a-gis-expert/) .
