# Using PostgreSQL tablespaces with Percona Operator for PostgreSQL

Tablespaces allow DBAs to store a database on multiple file systems within the
same server and to control where (on which file systems) specific parts of the
database are stored. You can think about it as if you were giving names to your
disk mounts and then using those names as additional parameters when creating
database objects.

PostgreSQL supports this feature, allowing you to
*store data outside of the primary data directory*, and Percona Operator for PostgreSQL is a good
option to bring this to your Kubernetes environment when needed.

## Possible use cases

The most obvious use case for tablespaces is performance optimization. You place
appropriate parts of the database on fast but expensive storage and engage
slower but cheaper storage for lesser-used database objects. The classic example
would be using an SSD for heavily-used indexes and using a large slow HDD for
archive data.

Of course, the Operator [already provides](constraints.md#operator-constraints) you with
[traditional Kubernetes approaches](https://kubernetes.io/docs/concepts/scheduling-eviction/assign-pod-node/)
to achieve this on a per-Pod basis (Tolerations, etc.). But if you would like to
go deeper and make such differentiation at the level of your database objects
(tables and indexes), tablespaces are exactly what you would need for that.

Another well-known use case for tablespaces is quickly adding a new partition to
the database cluster when you run out of space on the initially used one and
cannot extend it (which may look less typical for cloud storage). Finally, you
may need tablespaces when migrating your existing architecture to the cloud.

Each tablespace created by Percona Operator for PostgreSQL corresponds to a
separate Persistent Volume, mounted in a container to the `/tablespaces`
directory.

![image](assets/images/tablespaces.svg)

## Creating a new tablespace

Providing a new tablespace for your database in Kubernetes involves two parts:

1. Configure the new tablespace storage with the Operator,
2. Create database objects in this tablespace with PostgreSQL.

The first part is done in the traditional way of Percona Operators, by modifying
Custom Resource via the `deploy/cr.yaml` configuration file. It has a special
[spec.tablespaceStorages](operator.md#operator-tablespacestorages-section) section
for tablespaces.

The example already present in `deploy/cr.yaml` shows how to create tablespace
storage 1Gb in size (you can see
[official Kubernetes documentation on Persistent Volumes](https://kubernetes.io/docs/concepts/storage/persistent-volumes/) for details):

```yaml
spec:
  instances:
    ...
    tablespaceVolumes:
      - name: user
        dataVolumeClaimSpec:
          accessModes:
            - 'ReadWriteOnce'
          resources:
            requests:
              storage: 1Gi
```

After you apply this by running the `kubectl apply -f deploy/cr.yaml` command,
the new `/tablespaces/user/` mountpoint will appear for your database. Please take into
account that if you add your new tablespace to the already existing PostgreSQL
cluster, it may take time for the Operator to create Persistent Volume Claims
and get Persistent Volumes actually mounted.

Now you should actually create your tablespace on this volume with the
`CREATE TABLESPACE <tablespace name> LOCATION <mount point>` command, and then
create objects in it (of course, your user should have appropriate `CREATE`
privileges to make it possible):

```sql
CREATE TABLESPACE user121
LOCATION '/tablespaces/user/data';
```

Now when the tablespace is created you can append `TABLESPACE <tablespace_name>`
to your `CREATE` SQL statements to implicitly create tables, indexes, or even
entire databases in specific tablespace.

Let’s create an example table in the already mentioned `user121` tablespace:

```sql
CREATE TABLE products (
    product_sku character(10),
    quantity int,
    manufactured_date timestamptz)
TABLESPACE user121;
```

It is also possible to set a default tablespace with the
`SET default_tablespace = <tablespace_name>;` statement. It will affect all
further `CREATE TABLE` and `CREATE INDEX` commands without an explicit
tablespace specifier, until you unset it with an empty string.

As you can see, Percona Operator for PostgreSQL simplifies tablespace creation by carrying on all
necessary modifications with Persistent Volumes and Pods. The same would not be
true for the deletion of an already existing tablespace, which is not automated,
neither by the Operator nor by PostgreSQL.

## Deleting an existing tablespace

Deleting an existing tablespace from your database in Kubernetes also involves
two parts:

* Delete related database objects and tablespace with PostgreSQL,
* Delete tablespace storage in Kubernetes.

To make tablespace deletion with PostgreSQL possible, you should make this
tablespace empty (it is impossible to drop a tablespace until
*all objects in all databases using this tablespace* have been removed).
Tablespaces are listed in the `pg_tablespace` table, and you can use it to
find out which objects are stored in a specific tablespace. The example command
for the `lake` tablespace will look as follows:

```sql
SELECT relname FROM pg_class WHERE reltablespace=(SELECT oid FROM pg_tablespace WHERE spcname='user121');
```

When your tablespace is empty, you can log in to the
*PostgreSQL Primary instance* as a *superuser*, and then execute the
`DROP TABLESPACE <tablespace_name>;` command.

Now, when the PostgreSQL part is finished, you can remove the tablespace entry
from the `tablespaceStorages` section (don’t forget to run the
`kubectl apply -f deploy/cr.yaml` command to apply changes).
