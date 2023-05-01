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
    $ kubectl apply --server-side  -f deploy/bundle.yaml
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

## Verifying the cluster operation

When creation process is over, you can try to connect to the cluster.

{% include 'assets/fragments/connectivity.txt' %}
