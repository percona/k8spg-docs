# Users

The Percona Operator for PostgreSQL includes built-in functionality to simplify management of users and databases within your PostgreSQL cluster. By default, the Operator creates a single unprivileged user and the database that matches the cluster name. 

However, many production workloads require more granular user access, separate databases for different applications, or restricted privileges for security and compliance. With the Operator, you can define custom users and manage their access to your database cluster resources:

This document explains how you can customize user and database management for your specific use case.

## Understanding default user management

When you create a PostgreSQL cluster with the Operator and do not specify any additional users or databases, the Operator does the following:

1. Creates a database that matches the name of your PostgreSQL cluster.
2. Creates a schema for that database that matches the name of your PostgreSQL cluster.
3. Creates an unprivileged PostgreSQL user with the name of the cluster. This user has access to the database created in the previous step.
4. Creates a Secret with the login credentials and connection details for the PostgreSQL user from the previous step which is in relation to the database. The Secret is named `<clusterName>-pguser-<userName>` and contains the following information:

    - `user`: The name of the user account.
    - `password`: The password for the user account.
    - `dbname`: The name of the database that the user has access to by default.
    - `host`: The name of the host of the database. This references the Service of the primary PostgreSQL instance.
    - `port`: The port that the database is listening on.
    - `uri`: A PostgreSQL connection URI that provides all the information for logging into the PostgreSQL database via pgBouncer
    - `jdbc-uri`: A PostgreSQL JDBC connection URI that provides all the information for logging into the PostgreSQL database via the JDBC driver.

As an example, with the default PostgreSQL cluster name `cluster1`, the Operator creates the following:

- A database named `cluster1`.
- A schema named `cluster1` for the database `cluster1`
- A PostgreSQL user named `cluster1`.
- A Secret named `cluster1-pguser-cluster1` that contains the user credentials and connection information.

## Custom users and databases

You can add and manage custom users and databases using the `spec.users` section in the Custom Resource. You can do this:

* at the cluster creation time 
* at runtime. 

### Considerations

Here's what you need to know:

**Adding custom users and databases:**

- If you define custom users in `spec.users` during cluster creation, the Operator does **not** create any default users or databases (except for the `postgres` database). If you want additional databases, you must specify them explicitly.
- For each user added in `spec.users`, the Operator creates a Secret named `<clusterName>-pguser-<userName>` with that user's credentials. You can override this Secret name using the `spec.users.secretName` option.
    - If you do **not** specify any databases for a custom user, the resulting Secret will **not** include `dbname` or `uri` fields. This means the user will not have access to any database until one is assigned later.
    - If you include at least one database in `spec.users.databases` for the user, the Secret will include connection credentials for the **first** database in the list (`dbname` and `uri`).

- You can add a special `postgres` user as one of the custom users. This user is granted access to the `postgres` database, but its privileges cannot be changed.
- By default, the the top-level `autoCreateUserSchema` option is set to `true`. This means each user will have automatically-created schemas in all databases listed for this user under `users.databases`.
- By default, users without superuser privileges do not have access to the `public` schema. To allow a non-superuser to create and update tables in the `public` schema, set the `grantPublicSchemaAccess` option to `true`. This gives the user permission to create and update tables in the `public` schema of every database they own.
- Your custom superusers automatically have access to the `public` schema for their assigned databases.
- If multiple users are granted access to the `public` schema in the same database, each can only access tables they themselves have created. If you want one user to access tables created by another user, the table owner must explicitly grant privileges via PostgreSQL.

**Behavior when removing or modifying users and databases:**

- The Operator does **not** automatically drop users if you remove them from the Custom Resource, to prevent accidental data loss.
- Similarly, the Operator does **not** automatically drop databases when you remove them from the Custom Resource. (See how to actually drop a database [here](users.md#deleting-users-and-databases).)
- Role attributes (such as SUPERUSER) are not automatically removed if you delete them from the Custom Resource. You must specify the opposite attribute (e.g., `NOSUPERUSER`) to explicitly revoke privileges.

### Creating a new user

Change `PerconaPGCluster` Custom Resource by editing your YAML manifest in the `deploy/cr.yaml` configuration file:

```yaml
...
spec:
  users:
    - name: perconapg
```

After you apply such changes with the usual `kubctl apply -f deploy/cr.yaml` command, the Operator will create the new user as follows:

- The credentials of this user are populated in the `<clusterName>-pguser-perconapg` secret. There are no connection credentials.
- The user is unprivileged.

The following example shows how to create a new `pgtest` database and let `perconapg` user access it. The appropriate Custom Resource fragment will look as follows: 

```yaml
...
spec:
  users:
    - name: perconapg
      databases: 
        - pgtest 
```

If you inspect the `<clusterName>-pguser-perconapg` Secret after applying the changes, you will see `dbname` and `uri` options populated there, and the database `pgtest` is created in PostgreSQL as well.

### Managing user passwords

#### Operator-generated passwords

The Operator generates a random password for each PostgreSQL user it creates. PostgreSQL allows almost any character
in its passwords and the Operator generates passwords in [ASCII](https://en.wikipedia.org/wiki/ASCII) format by default. 

Your application may have stricter requirements to password creation. For example, if you need passwords without special characters, set the `spec.users.password.type` field for that user to `AlphaNumeric`.

To have the Operator generate a new password, remove the existing `password` field from the user Secret.

For example, to generate a new password for the user `cluster1` in the PostgreSQL cluster `cluster1` running in the `postgres-operator` namespace, use the following `kubectl patch` command:

```bash
kubectl patch secret -n postgres-operator cluster1-pguser-cluster1 -p '{"data":{"password":""}}'
```

#### Custom passwords

You may want a complete control over user passwords by setting a specific password for a PostgreSQL user instead of letting Percona Operator for PostgreSQL generate one for you. To do that, create a user Secret and specify the password within.

When you create a user Secret, the way you name it is important:

- If you specify a Secret name using the default naming convention that the Operator expects (`<clusterName>-pguser-<userName>`), the Operator will detect and use it automatically.
- If you use a custom name for your Secret, you must explicitly reference that Secret in the Custom Resource to let the Operator know about it.

The Operator looks for two fields in the Secret:

- `password`: the plaintext password.
- `verifier`: a hashed representation of the password using `SCRAM-SHA-256`.

When the `verifier` changes, the Operator updates the password inside the PostgreSQL cluster. This approach ensures the password is securely passed into the database.

You can set a custom password in these ways:

* You can provide a plaintext password in the `password` field and omit the verifier. The Operator will detect this and automatically generate a SCRAM verifier for your password.
* You can supply both the `password` and the `verifier` yourself. If both are present, the Operator will use them as-is and skip the generation step. Once the Secret contains both values, the Operator will make sure the credentials are correctly applied to PostgreSQL.

Here's how to set a custom password within a Secret with a custom name:

1. Export your namespace as an environment variable

    ```bash
    export NAMESPACE=postgres-operator
    ```
    
2. Create a Secrets object. For example, `cat-credentials`:

    ```bash
    kubectl apply -n $NAMESPACE -f - <<EOF
    apiVersion: v1
    kind: Secret
    metadata:
      name: cat-credentials
    type: Opaque
    data:
      password: $(echo -n 'mySuperStr0ngp@ssword' | base64)
    EOF
    ```

    !!! example "Sample output"

        ```{.text .no-copy}
        secret/cat-credentials created
        ```

2. Add a user and reference the Secret for them in the Custom Resource:

    === "via cr.yaml"

        ```yaml
         users:
          - name: cat
            databases:
              - zoo
            secretName: "cat-credentials"
            grantPublicSchemaAccess: true
        ```

        Apply the configuration:

        ```bash
        kubectl apply -f deploy/cr.yaml -n $NAMESPACE
        ```

    === "via kubectl patch"

        To update a running cluster, use the `kubectl patch` command:

        ```bash
        kubectl patch pg cluster1 -n $NAMESPACE --type=merge --patch '{
        "spec": {
          "users": [
            {
              "name": "cat",
              "databases": ["zoo"],
              "secretName": "cat-credentials",
              "grantPublicSchemaAccess": true
             }
            ]
          }
        }' 
        ```

3. After you update the cluster, the Operator updates the Secret with the login credentials and connection information. View the Secret object to verify this with this command:

    ```bash
    kubectl get secret cat-credentials -o yaml -n $NAMESPACE
    ```

4. Verify that the user is created by [connecting to the database](connect.md) as your custom user. 

#### Password rotation

If you want to rotate a user's password, just remove the old password in the
corresponding Secret: the Operator will immediately generate a new password
and save it to the appropriate Secret. You can remove the old password with the
`kubectl patch secret` command:

``` {.bash data-prompt="$" }
kubectl patch secret <clusterName>-pguser-<userName> -p '{"data":{"password":""}}'
```

In the same way you can update a password with your custom one for the user. Do it as follows:

``` {.bash data-prompt="$" }
kubectl patch secret <clusterName>-pguser-<userName> -p '{"stringData":{"password":"<custom_password>", "verifier":""}}'
```

### Adjusting privileges

You can set role privileges by using the standard [role attributes :octicons-link-external-16:](https://www.postgresql.org/docs/current/role-attributes.html) that PostgreSQL provides and adding them to the `spec.users.options` subsection in the Custom Resource. 

**Grant privileges**

The following example will make the `perconapg` a superuser. You can add the following to the spec in your `deploy/cr.yaml`:

```yaml
...
spec:
  users:
    - name: perconapg
      databases:
        - pgtest
      options: "SUPERUSER"
```

Apply changes with the usual `kubectl apply -f deploy/cr.yaml` command.

If you want to add multiple privileges, you can use a space-separated list as follows:

```yaml
...
spec:
  users:
    - name: perconapg
      databases:
        - pgtest
      options: "CREATEDB CREATEROLE"
```

**Revoke privileges**

To revoke the superuser privilege afterwards, apply the following configuration:

```yaml
...
spec:
  users:
    - name: perconapg
      databases:
        - pgtest
      options: "NOSUPERUSER"
```

### `postgres` User

By default, the Operator does not create the `postgres` user. You can create it by applying the following change to your Custom Resource:

```yaml
...
spec:
  users:
    - name: postgres
```

This will create a Secret named `<clusterName>-pguser-postgres` that contains the credentials of the `postgres` user. The Operator creates a user `postgres` who can access the `postgres` database.

### Deleting users and databases

The Operator does not delete users and databases automatically. After you remove the user from the Custom Resource, it will continue to exist in your cluster. To remove a user and all of its objects, as a superuser you will need to run `DROP OWNED` in each database the user has objects in, and `DROP ROLE` in your PostgreSQL cluster.

```sql
DROP OWNED BY perconapg;
DROP ROLE perconapg;
```

For databases, you should run the `DROP DATABASE` command as a superuser:

```sql
DROP DATABASE pgtest;
```

### Superuser and pgBouncer

For security reasons we do not allow superusers to connect to cluster through pgBouncer by default. As a superuser, you can connect through the `primary` service. Read more about this service in [exposure documentation](expose.md).

Otherwise you can use the [proxy.pgBouncer.exposeSuperusers](operator.md#proxypgbouncerexposesuperusers) Custom Resource option to enable superusers connection via pgBouncer.
