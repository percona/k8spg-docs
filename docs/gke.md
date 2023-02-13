# Install Percona Distribution for PostgreSQL on Google Kubernetes Engine (GKE)

Following steps will allow you to install the Operator and use it to manage
Percona Distribution for PostgreSQL with the Google Kubernetes Engine. The
document assumes some experience with Google Kubernetes Engine (GKE).
For more information on the GKE, see the [Kubernetes Engine Quickstart](https://cloud.google.com/kubernetes-engine/docs/quickstart).

## Prerequisites

All commands from this quickstart can be run either in the **Google Cloud shell** or in **your local shell**.

To use *Google Cloud shell*, you need nothing but a modern web browser.

If you would like to use *your local shell*, install the following:


1. [gcloud](https://cloud.google.com/sdk/docs/quickstarts). This tool is part of the Google Cloud SDK. To install it, select your operating system on the [official Google Cloud SDK documentation page](https://cloud.google.com/sdk/docs) and then follow the instructions.

2. [kubectl](https://cloud.google.com/kubernetes-engine/docs/quickstart#choosing_a_shell). It is the Kubernetes command-line tool you will use to manage and deploy applications. To install the tool, run the following command:

    ``` {.bash data-prompt="$" }
    $ gcloud auth login
    $ gcloud components install kubectl
    ```

## Create and configure the GKE cluster

You can configure the settings using the `gcloud` tool. You can run it either in the [Cloud Shell](https://cloud.google.com/shell/docs/quickstart) or in your local shell (if you have installed Google Cloud SDK locally on the previous step). The following command will create a cluster named `my-cluster-1`:

``` {.bash data-prompt="$" }
$ gcloud container clusters create cluster-1 --project <project name> --zone us-central1-a --cluster-version {{ gkerecommended }} --machine-type n1-standard-4 --num-nodes=3
```

!!! note

    You must edit the following command and other command-line statements to
    replace the `<project name>` placeholder with your project name. You may
    also be required to edit the *zone location*, which is set to `us-central1`
    in the above example. Other parameters specify that we are creating a
    cluster with 3 nodes and with machine type of 4 vCPUs and 45 GB memory.

You may wait a few minutes for the cluster to be generated.

???+ note "When the process is over, you can see it listed in the Google Cloud console"

    Select *Kubernetes Engine* → *Clusters* in the left menu panel:

    ![image](assets/images/gke-quickstart-cluster-connect.svg)

Now you should configure the command-line access to your newly created cluster
to make `kubectl` be able to use it.

In the Google Cloud Console, select your cluster and then click the *Connect*
shown on the above image. You will see the connect statement which configures
the command-line access. After you have edited the statement, you may run the
command in your local shell:

``` {.bash data-prompt="$" }
$ gcloud container clusters get-credentials cluster-1 --zone us-central1-a --project <project name>
```
Finally, use your [Cloud Identity and Access Management (Cloud IAM)](https://cloud.google.com/iam)
to control access to the cluster. The following command will give you the
ability to create Roles and RoleBindings:

``` {.bash data-prompt="$" }
$ kubectl create clusterrolebinding cluster-admin-binding --clusterrole cluster-admin --user $(gcloud config get-value core/account)
```

??? example "Expected output"

    ``` {.text .no-copy}
    clusterrolebinding.rbac.authorization.k8s.io/cluster-admin-binding created
    ```

## Install the Operator and deploy your PostgreSQL cluster

1. First of all, use the following `git clone` command to download the correct branch of the percona-postgresql-operator repository:

    ``` {.bash data-prompt="$" }
    $ git clone -b v{{ release }} https://github.com/percona/percona-postgresql-operator
    $ cd percona-postgresql-operator
    ```

2. The next thing to do is to add the `postgres-operator` namespace to Kubernetes,
not forgetting to set the correspondent context for further steps:

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
    $ kubectl apply -f deploy/bundle.yaml --server-side
    ```

4. After the operator is started Percona Distribution for PostgreSQL
can be created at any time with the following commands:

    ``` {.bash data-prompt="$" }
    $ kubectl apply -f deploy/cr.yaml
    ```

    Creation process will take some time. The process is over when the Operator
    and PostgreSQL Pods have reached their Running status:

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

    Also, you can see the same information when browsing Pods of your cluster in
    Google Cloud console via the *Object Browser*:

    ![image](assets/images/gke-quickstart-object-browser.svg)

5. During previous steps, the Operator has generated several [secrets](https://kubernetes.io/docs/concepts/configuration/secret/), including the password for the default unprivileged user named after the cluster (the `cluster1` user by default).

    Use `kubectl get secrets` command to see the list of Secrets objects. The Secrets object you are interested in is named as `<clusterName>-pguser-<clusterName>`, so the default variant will be `cluster1-pguser-cluster1`. Then `kubectl get secret cluster1-pguser-cluster1 -o yaml` will return the YAML file with generated secrets, including the password which should look as follows:

    ```yaml
    ...
    data:
      ...
      password: cGd1c2VyX3Bhc3N3b3JkCg==
    ```

    Here the actual password is base64-encoded, and `echo 'cGd1c2VyX3Bhc3N3b3JkCg==' | base64 --decode` will bring it back to a human-readable form (in this example it will be a `pguser_password` string).


6. Check connectivity to newly created cluster. Run a new Pod to use it as a client and connect its console output to your terminal (running it may require some time to deploy). When you see the command line prompt of the newly created Pod, run `psql` tool using the password obtained from the secret. The following command will do this, naming the new Pod `pg-client`:

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
