# Use PostGIS extension with Percona Distribution for PostgreSQL

[PostGIS :material-arrow-top-right:](https://postgis.net/) is a PostgreSQL extension that adds GIS
capabilities to this database.

Starting from the  Operator version 2.3.0 it became possible to deploy and
manage PostGIS-enabled PostgreSQL. 

Due to the large size and domain specifics of this extension, Percona provides
separate PostgreSQL Distribution images with it.

## Deploy the Operator with PostGIS-enabled database cluster

Following steps will allow you to deploy PostgreSQL cluster with these images.

1. Clone the percona-postgresql-operator repository:

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
    [Apply it :material-arrow-top-right:](https://kubernetes.io/docs/reference/using-api/server-side-apply/)
    as follows:

    ``` {.bash data-prompt="$" }
    $ kubectl apply --server-side -f deploy/crd.yaml
    ```

3. Create the Kubernetes namespace for your cluster if needed (for example,
    let's name it `postgres-operator`):

    ``` {.bash data-prompt="$" }
    $ kubectl create namespace postgres-operator
    ```

4. The role-based access control (RBAC) for Percona Distribution for PostgreSQL
    is configured with the `deploy/rbac.yaml` file. Role-based access is based
    on defined roles and the available actions which correspond to each role.
    The role and actions are defined for Kubernetes resources in the yaml file.
    Further details about users and roles can be found in [Kubernetes documentation :material-arrow-top-right:](https://kubernetes.io/docs/reference/access-authn-authz/rbac/#default-roles-and-role-bindings).

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

5.  Start the Operator within Kubernetes:

    ``` {.bash data-prompt="$" }
    $ kubectl apply -f deploy/operator.yaml -n postgres-operator
    ```

6. After the Operator is started, modify the `deploy/cr.yaml` configuration
    file with PostGIS-enabled image - use `percona/percona-postgresql-operator:{{ release }}-ppg{{ postgresrecommended }}-postgres-gis` instead of `percona/percona-postgresql-operator:{{ release }}-ppg{{ postgresrecommended }}-postgres`
    
    ```yaml
    apiVersion: pgv2.percona.com/v2
    kind: PerconaPGCluster
    metadata:
      name: cluster1
    spec:
      ...
      image: percona/percona-postgresql-operator:{{ release }}-ppg{{ postgresrecommended }}-postgres-gis
      ...
    ```

    When done, Percona Distribution for PostgreSQL cluster can be created at any
    time with the following command:

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

## Check PostGIS extension

To use PostGIS extension you should enable it for a specific database. 

For example, you can create the new database named `mygisdata` with the  `psql`
tool as follows:

```sql
CREATE database mygisdata;
\c mygisdata;
CREATE SCHEMA gis;
```

Next, enable the `postgis` extension. Make sure you are connected to the
database you created earlier and run the following command:

```sql
CREATE EXTENSION postgis;
```

Finally, check that the extension is enabled:

```sql
SELECT postgis_full_version();
```
    
The output should resemble the following:

```{.sql .no-copy}
postgis_full_version
    -----------------------------------------------------------------------------------------------------------------------------------------------------------------
 POSTGIS="3.3.3" [EXTENSION] PGSQL="140" GEOS="3.10.2-CAPI-1.16.0" PROJ="8.2.1" LIBXML="2.9.13" LIBJSON="0.15" LIBPROTOBUF="1.3.3" WAGYU="0.5.0 (Internal)"
```

You can find more about using PostGIS in the official Percona Distribution for
PostgreSQL [documentation :material-arrow-top-right:](https://docs.percona.com/postgresql/11/solutions/postgis-deploy.html),
as well as in this [blogpost :material-arrow-top-right:](https://www.percona.com/blog/working-with-postgresql-and-postgis-how-to-become-a-gis-expert/).


