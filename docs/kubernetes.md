# Install Percona Distribution for PostgreSQL on Kubernetes

Following steps will allow you to install the Operator and use it to manage
Percona Distribution for PostgreSQL in a Kubernetes-based environment.

1. First of all, clone the percona-postgresql-operator repository:

    ``` {.bash data-prompt="$" }
    $ git clone -b v{{ release }} https://github.com/percona/percona-postgresql-operator
    $ cd percona-postgresql-operator
    ```

    !!! note

        It is crucial to specify the right branch with `-b` option while cloning the
        code on this step. Please be careful.

2. The next thing to do is to add the `postgres-operator` namespace to
    Kubernetes, not forgetting to set the correspondent context for further
    steps:

    ``` {.bash data-prompt="$" }
    $ kubectl create namespace postgres-operator
    $ kubectl config set-context $(kubectl config current-context) --namespace=postgres-operator
    ```

    !!! note

        To use different namespace, you should edit *all occurrences* of
        the `namespace: postgres-operator` line in both `deploy/cr.yaml` and
        `deploy/bundle.yaml` configuration files.

3. Deploy the operator with the following command:

    ``` {.bash data-prompt="$" }
    $ kubectl apply -f deploy/bundle.yaml
    ```

4. After the operator is started Percona Distribution for PostgreSQL can be
    created at any time with the following command:

    ``` {.bash data-prompt="$" }
    $ kubectl apply -f deploy/cr.yaml
    ```

    Creation process will take some time. The process is over when both
    Operator and replica set Pods have reached their Running status:

    ``` {.bash data-prompt="$" }
    $ kubectl get pods
    ```
    ??? example "Expected output"

        ``` {.text .no-copy}
        
        NAME                                           READY   STATUS      RESTARTS   AGE
        cluster1-backup-7hsq-9ch48                     0/1     Completed   0          35s
        cluster1-instance1-mtnz-0                      4/4     Running     0          87s
        cluster1-pgbouncer-f4dcfffc8-lrs2d             2/2     Running     0          87s
        cluster1-repo-host-0                           2/2     Running     0          87s
        percona-postgresql-operator-75fd989d98-wvx4h   1/1     Running     0          109s
        ```

5. During previous steps, the Operator has generated several
    [secrets](https://kubernetes.io/docs/concepts/configuration/secret/),
    including the one with password for default `pguser` user named after the
    cluster.

    Use `kubectl get secrets` command to see the list of Secrets objects. The
    Secrets object you are interested in is named as
    `<cluster_name>-pguser-<cluster_name>`, so the default variant will be
    `cluster1-pguser-cluster1`. You can use the following command to get the
    password of this user:
    
    ``` {.bash data-prompt="$" }
    $ kubectl get secret cluster1-pguser-cluster1 --template='{{.data.password | base64decode}}{{"\n"}}'
    ```

6. Check connectivity to newly created cluster. Run a new Pod to use it as a
    client and connect its console output to your terminal (running it may
    require some time to deploy). When you see the command line prompt of the
    newly created Pod, run `psql` tool using the password obtained from the
    Secret. The following command will do this, naming the new Pod `pg-client`:

    ``` {.bash data-prompt="$" data-prompt-second="[postgres@pg-client /]$"}
    $ kubectl run -i --rm --tty pg-client --image=perconalab/percona-distribution-postgresql:{{ postgresrecommended }} --restart=Never -- bash -il
    [postgres@pg-client /]$ PGPASSWORD='pguser_password' psql -h cluster1-pgbouncer -p 5432 -U cluster1 cluster1
    ```

    This command will connect you as a `cluster1` user to a `cluster1` database
    via the PostgreSQL interactive terminal.

    ``` {.bash data-prompt="$" data-prompt-second="pgdb=>"}
    $ psql ({{ postgresrecommended }})
    Type "help" for help.
    pgdb=>
    ```
