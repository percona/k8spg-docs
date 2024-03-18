# Exec into the containers

If you want to examine the contents of a container "in place" using remote access to it, you can use the `kubectl exec` command. It allows you to run any command or just open an interactive shell session in the container. Of course, you can have shell access to the container only if container supports it and has a “Running” state.

In the following examples we will access the container `database` of the `cluster1-instance1-b5mr-0` Pod.

* Run `date` command:

    ``` {.bash data-prompt="$" }
    $ kubectl exec -ti cluster1-instance1-b5mr-0 -c database -- date
    ```

    ??? example "Expected output"

        ``` {.text .no-copy}
        Wed Jun 14 11:18:47 UTC 2023
        ```

    You will see an error if the command is not present in a container. For
    example, trying to run the `time` command, which is not present in the
    container, by executing `kubectl exec -ti cluster1-instance1-b5mr-0 -c database -- time`
    would show the following result:
    
    ``` {.text .no-copy}
    OCI runtime exec failed: exec failed: unable to start container process: exec: "time": executable file not found in $PATH: unknown command terminated with exit code 126
    ```

* Print log files to a terminal:

    ``` {.bash data-prompt="$" }
    $ kubectl exec -ti cluster1-instance1-b5mr-0 -c database -- cat /pgdata/pg16/log/postgresql-*.log
    ```

* Similarly, opening an Interactive terminal, executing a pair of commands in
    the container, and exiting it may look as follows:

    ```{.bash data-prompt="$" data-prompt-second="bash-4.4$"}
    $ kubectl exec -ti cluster1-instance1-b5mr-0 -c database -- bash
    bash-4.4$ hostname
    cluster1-pxc-0
    bash-4.4$ ls /pgdata/pg16/log/
    postgresql-Wed.log
    bash-4.4$ exit
    exit
    $
    ```

