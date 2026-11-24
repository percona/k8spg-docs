# Exec into the container

Use `kubectl exec` to run a command in a container or to open an interactive shell. The container must be in the `Running` state. A shell session works when the container image includes a shell.

The examples use the `database` container on a PostgreSQL instance Pod. Replace `cluster1` with your cluster name.

## Set the Pod name

Export the name of an instance Pod. The commands on this page use `$POD`.

```bash
export POD=$(kubectl get pods \
  -l postgres-operator.crunchydata.com/cluster=cluster1,postgres-operator.crunchydata.com/data=postgres \
  -o jsonpath='{.items[0].metadata.name}')
echo "$POD"
```

??? example "Sample output"

    ``` {.text .no-copy}
    cluster1-instance1-b5mr-0
    ```

This selects the first instance Pod. Set `POD` to another instance Pod name when you need a specific Pod.

## Run a command

Run `date` in the `database` container:

```bash
kubectl exec -ti "$POD" -c database -- date
```

??? example "Expected output"

    ``` {.text .no-copy}
    Wed Jun 14 11:18:47 UTC 2023
    ```

Exec fails when the command is not in the container image. The `time` command is not in the `database` container:

```bash
kubectl exec -ti "$POD" -c database -- time
```

??? example "Expected output"

    ``` {.text .no-copy}
    OCI runtime exec failed: exec failed: unable to start container process: exec: "time": executable file not found in $PATH: unknown command terminated with exit code 126
    ```

## Print logs

How you print logs depends on whether [persistent logging](persistent-logging.md) is enabled. The log directory is `/pgdata/pg<major-version>/log`. The examples use PostgreSQL 18. The shell inside the container expands the `*` in the file name, so the command runs `cat` through `bash -c`.

=== "Persistent logging off"

    Print the PostgreSQL server log files from the `database` container. File names match `postgresql-*.log`.

    ```bash
    kubectl exec -ti "$POD" -c database -- bash -c 'cat /pgdata/pg18/log/postgresql-*.log'
    ```

=== "Persistent logging on"

    PostgreSQL and pgBackRest keep logs on the instance data volume, and the `logs` sidecar streams them. The files remain available after a Pod restart.

    Read the stream from the `logs` container. See [Check the logs](debug-logs.md) for more `kubectl logs` options.

    ```bash
    kubectl logs "$POD" -c logs
    ```

## Open a shell

Open a shell in the `database` container and run commands there:

1. Start the shell:

    ```bash
    kubectl exec -ti "$POD" -c database -- bash
    ```

2. Print the hostname:

    ```bash
    hostname
    ```

    ??? example "Expected output"

        ``` {.text .no-copy}
        cluster1-instance1-b5mr-0
        ```

3. List the log files:

    ```bash
    ls /pgdata/pg18/log/
    ```

    ??? example "Expected output"

        ``` {.text .no-copy}
        postgresql-Wed.log
        ```

4. Leave the shell:

    ```bash
    exit
    ```
