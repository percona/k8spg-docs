> For the complete documentation index, see [llms.txt](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/llms.txt).

# Upgrade PostgreSQL extensions

## Upgrade `pg_stat_monitor` (for Operator earlier than 2.6.0)

`pg_stat_monitor` is the built-in extension, which is used to provide query analytics for Percona Monitoring and Management (PMM). If you [enabled it](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/custom-extensions.html#built-in-extensions) in the Custom Resource (`deploy/cr.yaml` manifest), you need to manually update it *after the database upgrade* (this manual step is not required for the Operator versions 2.6.0 and newer):

1. Find the primary instance of your PostgreSQL cluster. You can do this using Kubernetes Labels as follows (replace the `<namespace>` placeholder with your value):

   ```
   kubectl get pods -n <namespace> -l postgres-operator.crunchydata.com/cluster=cluster1 \ 
       -L postgres-operator.crunchydata.com/instance \
       -L postgres-operator.crunchydata.com/role | grep instance1
   ```

   Sample output

   ```
   cluster1-instance1-bmdp-0             4/4     Running   0          2m23s   cluster1-instance1-bmdp   replica
   cluster1-instance1-fm7w-0             4/4     Running   0          2m22s   cluster1-instance1-fm7w   replica
   cluster1-instance1-ttm9-0             4/4     Running   0          2m22s   cluster1-instance1-ttm9   master
   ```

   PostgreSQL primary is labeled as `master`, while other PostgreSQL instances are labeled as `replica`.

1. Log in to a primary instance (`cluster1-instance1-ttm9-0` in the above example) as an administrative user:

   ```
   kubectl exec  -n <namespace> -ti cluster1-instance1-ttm9-0 -c database -- psql postgres
   ```

1. Execute the following SQL statement:

   ```
   postgres=# alter extension pg_stat_monitor update;
   ```

## Upgrade PostGIS extension

When you [upgrade your database](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/update-db-minor.html) to a new version, this process does **not** automatically update the PostGIS extension inside PostgreSQL. You need to manually update the PostGIS extension in every database where it is enabled.

To do this, connect to PostgreSQL as a user with `SUPERUSER` privileges. You can use [the same user you used to enable the PostGIS extension](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/postgis.html#enable-postgis-extension). Then, execute the following SQL command for each relevant database:

```
SELECT PostGIS_Extensions_Upgrade();
```

## Upgrade custom PostgreSQL extensions

If you have installed [custom PostgreSQL extensions](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/custom-extensions.html#add-custom-extensions), you need to build and package each custom extension for the new PostgreSQL major version. During the upgrade, the Operator will install extensions into the upgrade container.

Refer to the [Update custom extensions](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/custom-extensions.html#update-custom-extensions) section for step-by-step instructions.
