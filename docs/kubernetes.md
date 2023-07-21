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

2. The next thing to do is to add the `pgo` namespace to Kubernetes,
not forgetting to set the correspondent context for further steps:

    ``` {.bash data-prompt="$" }
    $ kubectl create namespace pgo
    $ kubectl config set-context $(kubectl config current-context) --namespace=pgo
    ```

    !!! note

        To use different namespace, you should edit *all occurrences* of the
        `namespace: pgo` line in both `deploy/cr.yaml` and `deploy/operator.yaml`
        configuration files.

3. Deploy the operator with the following command:

    ``` {.bash data-prompt="$" }
    $ kubectl apply -f deploy/operator.yaml
    ```

    ??? example "Expected output"

        ``` {.text .no-copy}
        
        serviceaccount/pgo-deployer-sa created
        clusterrole.rbac.authorization.k8s.io/pgo-deployer-cr created
        configmap/pgo-deployer-cm created
        clusterrolebinding.rbac.authorization.k8s.io/pgo-deployer-crb created
        job.batch/pgo-deploy created
        ```

    The last line of the command output mentions the `pgo-deploy` Kubernetes
    Job created to carry on the Operator deployment process. It can take several
    minutes to be completed. You can track it with the following command:
    
    ``` {.bash data-prompt="$" }
    $ kubectl get job/pgo-deploy
    ```

    ??? example "Expected output"

        ``` {.text .no-copy}
        NAME         COMPLETIONS   DURATION   AGE
        pgo-deploy   1/1           81s        5m53s
        ```

    When it reaches the COMPLETIONS count of `1/1`, you can safely delete the job
    as follows:
    
    ``` {.bash data-prompt="$" }
    $ kubectl delete  job/pgo-deploy
    ```
    
    !!! note

        Deleting the `pgo-deploy` job will be needed before [upgrading](update.md) the Operator.

4. After the operator is started Percona Distribution for PostgreSQL
can be created at any time with the following command:

    ``` {.bash data-prompt="$" }
    $ kubectl apply -f deploy/cr.yaml
    ```

    Creation process will take some time. The process is over when both
    operator and replica set pod have reached their Running status:

    ``` {.bash data-prompt="$" }
    $ kubectl get pods
    ```
    ??? example "Expected output"

        ``` {.text .no-copy}
        
        NAME                                              READY   STATUS    RESTARTS   AGE
        backrest-backup-cluster1-j275w                    0/1     Completed 0          10m
        cluster1-85486d645f-gpxzb                         1/1     Running   0          10m
        cluster1-backrest-shared-repo-6495464548-c8wvl    1/1     Running   0          10m
        cluster1-pgbouncer-fc45869f7-s86rf                1/1     Running   0          10m
        pgo-deploy-rhv6k                                  0/1     Completed 0          5m
        postgres-operator-8646c68b57-z8m62                4/4     Running   1          5m
        ```

5. During previous steps, the Operator has generated several [secrets](https://kubernetes.io/docs/concepts/configuration/secret/), including the password for the `pguser` user, which you will need to access the cluster.

    Use `kubectl get secrets` command to see the list of Secrets objects (by default Secrets object you are interested in has `cluster1-pguser-secret` name). Then you can use `kubectl get secret cluster1-pguser-secret -o yaml` to look through the YAML file with generated secrets (the actual password will be base64-encoded), or just get the needed password with the following command:

    ``` {.bash data-prompt="$"}
    $ kubectl get secrets cluster1-users -o yaml -o jsonpath='{.data.pguser}' | base64 --decode | tr '\n' ' ' && echo " "
    ```

6. Check connectivity to newly created cluster. Run a new Pod to use it as a client and connect its console output to your terminal (running it may require some time to deploy). When you see the command line prompt of the newly created Pod, run `psql` tool using the password obtained from the secret. The following command will do this, naming the new Pod `pg-client`:

    ``` {.bash data-prompt="$" data-prompt-second="[postgres@pg-client /]$"}
    $ kubectl run -i --rm --tty pg-client --image=perconalab/percona-distribution-postgresql:{{ postgresrecommended }} --restart=Never -- bash -il
    [postgres@pg-client /]$ PGPASSWORD='pguser_password' psql -h cluster1-pgbouncer -p 5432 -U pguser pgdb
    ```

    This command will connect you to the PostgreSQL interactive terminal.

    ``` {.bash data-prompt="$" data-prompt-second="pgdb=>"}
    $ psql ({{ postgresrecommended }})
    Type "help" for help.
    pgdb=>
    ```
