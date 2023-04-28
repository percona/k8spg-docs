# Users

User accounts within the Cluster can be divided into two different groups:

* *application-level users*: the user accounts to be used by the application
    (probably, the unprivileged ones),
* *system-level users*: the accounts needed to automate the cluster deployment
    and management tasks.

The Operator creates needed system users at the cluster deployment time with
generated random passwords. It can manage additional (application-level) users
also if their data are placed into the Custom Resource `users` section. Changes
in this section will be tracked and immediately applied by the Operator.

For example, here is a self-explanatory `deploy/cr.yaml` configuration file
fragment which would add a new `rhino` user with administrative privileges over
the `zoo` database:

```yaml
...
users:
  - name: rhino
    databases:
      - zoo
    options: "SUPERUSER"
    password:
      type: ASCII
...
```

Credentials for users managed by the Operator are stored as [Kubernetes Secrets](https://kubernetes.io/docs/concepts/configuration/secret/) objects.
Each such user has its own dedicated Secret named as
`<cluster_name>-<user_name>-<cluster_name>`.

By default, the Operator creates only `pguser` administrative user (the
superuser), and it would have a Secret named `cluster1-pguser-cluster1` in case
of the default cluster name.

!!! note

    You can connect to PostgreSQL and login as `pguser` to PostgreSQL Pods, but
    [pgBouncer](http://pgbouncer.github.io/) (the connection pooler for
    PostgreSQL) doesn’t allow `pguser` user access by default. That’s done for
    security reasons.


Secrets object for each user contains `password` field stored as `data` - i.e.,
base64-encoded string. You can find out user's password by querying the
correspondent Secret as follows (don't forget to use the real user login and
cluster name instead of the `<cluster_name>-<user_name>-<cluster_name>`
placeholder):

``` {.bash data-prompt="$" }
$ kubectl get secret <cluster_name>-<user_name>-<cluster_name> --template='{{"{{"}}.data.password | base64decode{{"}}"}}{{"{{"}}"\n"{{"}}"}}'
```

!!! note

    The `{{"\n"}}` fragment at the end of the above command provides a newline to
    improve the readability of the command output. In case of automation (for
    example, in a script), this fragment can be safely omitted.

If you want to rotate user's password, just remove the old password in the
correspondent Secret: the Operator will immediately generate a new password
and save it to the appropriate Secret. You can remove the old password with the
`kubectl patch secret command`:

``` {.bash data-prompt="$" }
$ kubectl patch secret <cluster_name>-<user_name>-<cluster_name> -p '{"data":{"password":""}}'
```

Also, you can set a custom password for the user. Do it as follows (use the real
user login and cluster name instead of the
`<cluster_name>-<user_name>-<cluster_name>`,
and new password instead of the `<custom_password>` placeholders):

``` {.bash data-prompt="$" }
$ kubectl patch secret <cluster_name>-<user_name>-<cluster_name> -p '{"stringData":{"password":"<custom_password>", "verifier":""}}'
```

