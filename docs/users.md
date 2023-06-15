# Users

Operator provides a feature to manage users and databases in your PostgreSQL cluster. This document describes this feature, defaults and ways to fine tune your users. 

## Defaults

When you create a PostgreSQL cluster with Operator and do not specify any additional users or databases, Operator will do the following:

- Create a database that matches the name of the PostgreSQL cluster.
- Create an unprivileged PostgreSQL user with the name of the cluster. This user has access to the database created in the previous step.
- Create a Secret with the login credentials and connection details for the PostgreSQL user in relation to the database. This is stored in a Secret named `<clusterName>-pguser-<clusterName>`. These credentials include:
  - `user`: The name of the user account.
  - `password`: The password for the user account.
  - `dbname`: The name of the database that the user has access to by default.
  - `host`: The name of the host of the database. This references the Service of the primary PostgreSQL instance.
  - `port`: The port that the database is listening on.
  - `uri`: A PostgreSQL connection URI that provides all the information for logging into the PostgreSQL database via pgBouncer
  - `jdbc-uri`: A PostgreSQL JDBC connection URI that provides all the information for logging into the PostgreSQL database via the JDBC driver.

As an example, using our `cluster1` PostgreSQL cluster, we would see the following created:

- A database named `cluster1`.
- A PostgreSQL user named `cluster1`.
- A Secret named `cluster1-pguser-cluster1` that contains the user credentials and connection information.

## Custom Users and Databases

Users and databases can be customized in `spec.users` section in the custom resource. Section can be changed at the cluster creation and adjusted over time. Note the following:

- If `spec.users` is set during cluster creation, Operator will not create any default users or databases except for PostgreSQL. If you want additional databases, you will need to specify them.
- For any users added in `spec.users`, Operator will created a Secret of the format `<clusterName>-pguser-<userName>`. This will contain the user credentials.
- If no databases are specified, `dbname` and `uri` will not be present in the Secret.
- If at least one `spec.users.databases` is specified, the first database in the list will be populated into the connection credentials.
- To prevent accidental data loss, Operator does not automatically drop users.
- Similarly, to prevent accidental data loss Operator does not automatically drop databases. We will see how to drop a database below.
- Role attributes are not automatically dropped if you remove them. You will have to set the inverse attribute to drop them (e.g. `NOSUPERUSER`).
- The special `postgres` user can be added as one of the custom users; however, the privileges of the users cannot be adjusted.

### Creating a New User

Change `PerconaPGCluster` custom resource or your YAML manifest:

```yaml
spec:
  users:
    - name: perconapg
```

Apply the changes, the new user is created:
- The user will only be able to connect to the default `postgres` database.
- The credentials are populated in the secret `<clusterName>-pguser-perconapg`. There are no connection credentials.
- The user is unprivileged.

Let's create a new database `pgtest` and let `perconapg` user access it:
```yaml
spec:
  users:
    - name: perconapg
      databases: 
        - pgtest 
```

Inspect the `<clusterName>-pguser-perconapg` secret. You should see `dbname` and `uri` populated. The database is also created.

### Adjusting privileges

We can set role privileges by using the standard [role attributes](https://www.postgresql.org/docs/current/role-attributes.html) that PostgreSQL provides and adding them to the `spec.users.options`. Let’s say we want the `perconapg` to become a superuser. You can add the following to the spec:

```yaml
spec:
  users:
    - name: perconapg
      databases:
        - pgtest
      options: "SUPERUSER"
```

Revoke the superuser privilege by doing the following:

```yaml
spec:
  users:
    - name: perconapg
      databases:
        - pgtest
      options: "NOSUPERUSER"
```

If you want to add multiple privileges, you can add each privilege with a space between them in options, e.g.:

```yaml
spec:
  users:
    - name: perconapg
      databases:
        - pgtest
      options: "CREATEDB CREATEROLE"
```

### `postgres` User

By default, operator does not create `postgres` user. You can create it by doing the following:

```yaml
spec:
  users:
    - name: postgres
```

This will create a Secret of the pattern `<clusterName>-pguser-postgres` that contains the credentials of the postgres account. 

### Deleting users and databases

Operator does not delete users and databases automatically. After you remove the user from the custom resource, it will still exist in your cluster. To remove a user and all of its objects, as a superuser you will need to run `DROP OWNED` in each database the user has objects in, and `DROP ROLE` in your PostgreSQL cluster.

```
DROP OWNED BY perconapg;
DROP ROLE perconapg;
```

For databases, you must run the `DROP DATABASE` command as a superuser:
```
DROP DATABASE pgtest;
```

### Managing user passwords

If you want to rotate user's password, just remove the old password in the
correspondent Secret: the Operator will immediately generate a new password
and save it to the appropriate Secret. You can remove the old password with the
`kubectl patch secret` command:

``` {.bash data-prompt="$" }
$ kubectl patch secret <clusterName>-pguser-<userName> -p '{"data":{"password":""}}'
```

Also, you can set a custom password for the user. Do it as follows:

``` {.bash data-prompt="$" }
$ kubectl patch secret <clusterName>-pguser-<userName> -p '{"stringData":{"password":"<custom_password>", "verifier":""}}'
```

### Superuser and pgBouncer

For security reasons we do not allow superusers to connect to cluster through pgBouncer. You can connect through `primary` service. Read more in [exposure documentation](expose.md)

