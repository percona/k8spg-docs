# Use PostGIS extension with Percona Distribution for PostgreSQL

[PostGIS :octicons-link-external-16:](https://postgis.net/) is a PostgreSQL extension that adds GIS
capabilities to this database.

You can deploy and manage PostGIS-enabled PostgreSQL starting from the  Operator version 2.3.0. Here's how to do it:

## Prepare your environment

1. Clone the `percona-postgresql-operator` repository because you will need to modify the cluster's Custom Resource. Specify your desired version for the `-b` flag:

    ```bash
    git clone -b v{{ release }} https://github.com/percona/percona-postgresql-operator
    cd percona-postgresql-operator
    ```

2. Create the namespace where the Operator and the cluster will run. Export it as an environment variable. Replace the `<namespace>` placeholder with your value:
    
    ```bash
    kubectl create namespace <namespace>
    export NAMESPACE=<namespace>
    ```

## Deploy Percona Operator for PostgreSQL

Create the Custom Resource Definition, role-based access control (RBAC) and the Operator deployment. To do that in one go, apply the `deploy/bundle.yaml` manifest:
   
```bash
kubectl apply --server-side -f deploy/bundle.yaml -n $NAMESPACE
```

## Deploy PostGIS-enabled database cluster

1. Modify the `deploy/cr.yaml` configuration file. Specify the image for PostGIS in the `spec.image` option. Use `docker.io/percona/percona-distribution-postgresql-with-postgis:{{postgresrecommended}}` instead of `docker.io/percona/percona-distribution-postgresql:{{ postgresrecommended }}`
    
    ```yaml
    apiVersion: pgv2.percona.com/v2
    kind: PerconaPGCluster
    metadata:
      name: cluster1
    spec:
      ...
      image: docker.io/percona/percona-distribution-postgresql-with-postgis:{{postgresrecommended}}
      ...
    ```

2. Create a cluster with the following command:

    ```bash
    kubectl apply -f deploy/cr.yaml -n $NAMESPACE
    ```

    
3. The creation process may take some time. Check the cluster status with the following command:

    ```bash
    kubectl get pg -n $NAMESPACE
    ```

    When the process is over your cluster will obtain the `ready` status.


    ??? example "Expected output"

        --8<-- "kubectl-get-pg-response.txt"

## Enable PostGIS extension

To use the PostGIS extension, you should enable it for specific databases. To do that, your PostgreSQL user must be a superuser because only superusers can create extensions. By default, the Operator creates a standard database user without superuser privileges. You have several options to enable PostGIS in your databases:

1. **Connect as the `postgres` superuser to the primary Pod**. When you execute to the primary Pod and establish the `psql` session, you are connected as the `postgres` user. Then you can create or alter databases and enable the PostGIS extension as needed.

2. **Grant superuser privileges to the default user**. Connect to the database Pod as the `postgres` user and grant superuser privileges to the default Operator-created user. After this, you can log in with this user and enable the PostGIS extension for the databases this user has access to.  

3. **Create a separate superuser**. You can create a dedicated superuser with access to the needed databases via the Custom Resource. Use this user to connect to PostgreSQL and enable the PostGIS extension for the databases this user has access to.  

!!! note

    By default, superusers cannot connect to PostgreSQL via `pgBouncer` due to security restrictions. To connect to PostgreSQL as the superuser you can:

    - Update the `pgBouncer` configuration to allow superuser access (not recommended for general security reasons), or
    - Connect to PostgreSQL primary Pod using the `<cluster-name>-primary` Kubernetes Service bypassing `pgBouncer`.

For details on managing users, roles, and configuring `pgBouncer` access, refer to the [Application and system users](users.md) documentation.

### Option 1. Connect to the primary Pod

1. Find the primary Pod:
    
    ```bash
    kubectl get pods -n $NAMESPACE -l postgres-operator.crunchydata.com/role=primary
    ```

    ??? example "Sample output"
        
        ```{.text .no-copy}
        NAME                        READY   STATUS    RESTARTS   AGE
        cluster1-instance1-ccsr-0   4/4     Running   0          14m
        ```

2. Exec into the primary Pod and establish the `psql` session:

    ```bash
    kubectl -n $NAMESPACE exec -it <primary-pod-name> -- psql
    ```

3. For example, you can create the new database named `mygisdata` as follows:

    ```sql
    CREATE database mygisdata;
    ```

4. Connect to this database and create a schema to separate your spacial data.
   
    ```sql
    \c mygisdata;
    CREATE SCHEMA gis;
    ```

5. Enable the `postgis` extension for this database. Make sure you are connected to the
database you created earlier and run the following command:

    ```sql
    CREATE EXTENSION postgis;
    ```

6. Check that the extension is enabled:

    ```sql
    SELECT postgis_full_version();
    ```
    
    The output should resemble the following:
    
    --8<-- "gis-output.txt"

### Option 2. Grant superuser privileges to default user

1. Connect to the primary Pod following the steps from [Option 1](#option-1-connect-to-the-primary-pod)
2. Grant your default user superuser privileges. The following command updates privileges for the `cluster1` user. Replace with your user name of needed:
   
    ```sql
    ALTER USER cluster1 WITH SUPERUSER;
    ```
   
    Exit the pod.

3. Retrieve the connection string URL from a Secret. List the Secrets:
    
    ```bash
    kubectl get secrets -n $NAMESPACE
    ```
    
    Look for the Secret named after this pattern: `<cluster-name>-pguser-<username>`. For example, if your cluster name is `cluster1`, the Secret name is `cluster1-pguser-cluster1`.

4. The `data.uri` value in the Secret contains the connection string URL to the primary service. Export it as an environment variable:

    ```bash
    URI=$(kubectl get secret `<cluster-name>-pguser-<username>` --namespace $NAMESPACE -o jsonpath='{.data.uri}' | base64 --decode) | echo $URI
    ```

5. Create a Pod where you start Percona Distribution for PostgreSQL and connect to the database. The following command starts a Pod `pg-client` and connects it to the database using the connection string URL:
    
    ```bash
    kubectl run -i --rm --tty pg-client --image=perconalab/percona-distribution-postgresql:{{postgresrecommended}} --restart=Never -- psql $URI
    ```
    
    ??? example "Sample output"
        
        ```{.sql .no-copy}
        cluster1=#
        ```

6. When the Operator creates a user, it also creates the database and schema with the name that matches the username. You are now connected to this database. Create the `postgis` extension for it.
    
    ```sql
    CREATE EXTENSION postgis;
    ```

7. Check that the extension is enabled:

    ```sql
    SELECT postgis_full_version();
    ```

    The output should resemble the following:
    
    --8<-- "gis-output.txt"

### Option 3. Create a dedicated superuser

1. Edit the Custom Resource and add a user that you will use to manage spatial data. For example, this user is called `gis`. List the databases this user has access to and grant it superuser privileges:
    
    ```yaml
    spec:
      users:
        - name: gis
          databases:
            - mygisdata
            - test
          options: "SUPERUSER"
    ```

2. Update the cluster configuration:
    
    ```bash
    kubectl apply -f deploy/cr.yaml -n $NAMESPACE
    ```

3. The Operator creates a user and a Secret object with user credentials named `<cluster-name>-pguser-<username>`. List the Secrets to verify it is created:

    ```bash
    kubectl get secrets -n $NAMESPACE
    ```
      
4. Retrieve the connection string URI to the primary Pod from the Secret and export it as an environment variable:
    
    ```
    URI=$(kubectl get secret `<cluster-name>-pguser-<username>` --namespace $NAMESPACE -o jsonpath='{.data.uri}' | base64 --decode) | echo $URI
    ```

5. Create a Pod where you start Percona Distribution for PostgreSQL and use it to connect to the database. The following command starts a Pod `pg-client` and connects it to the database using the connection string URL:

    ```bash
    kubectl run -i --rm --tty pg-client --image=perconalab/percona-distribution-postgresql:{{postgresrecommended}} --restart=Never -- psql $URI
    ```

    ??? example "Sample output"

        ```{.sql .no-copy}
        mygisdata=#
        ```

6. When the Operator creates a user, it also creates the database and schema with the name that matches the username. You are now connected to this database. Create the `postgis` extension for it.

    ```sql
    CREATE EXTENSION postgis;
    ```

7. Check that the extension is enabled:

    ```sql
    SELECT postgis_full_version();
    ```

    The output should resemble the following:

    --8<-- "gis-output.txt"

You can find more about using PostGIS in the official Percona Distribution for
PostgreSQL [documentation :octicons-link-external-16:](https://docs.percona.com/postgresql/latest/solutions/postgis-deploy.html),
as well as in this [blogpost :octicons-link-external-16:](https://www.percona.com/blog/working-with-postgresql-and-postgis-how-to-become-a-gis-expert/).


