# Check the Logs

Logs provide valuable information. It makes sense to check the logs of the
database Pods and the Operator Pod. Following flags are helpful for checking the
logs with the `kubectl logs` command:

| Flag                                |  Description                                                              |
| ----------------------------------- | ------------------------------------------------------------------------- |
| `-c`, `--container=<container-name>`| Print log of a specific container in case of multiple containers in a Pod |
| `-f`, `--follow`                    |  Follows the logs for a live output                                       |
| `--since=<time>`                    | Print logs newer than the specified time, for example: `--since="10s"`    |
| `--timestamps`                      | Print timestamp in the logs (timezone is taken from the container)        |
| `-p`, `--previous`                  | Print previous instantiation of a container. This is extremely useful in case of container restart, where there is a need to check the logs on why the container restarted. Logs of previous instantiation might not be available in all the cases. |

In the following examples we will access containers of the `cluster1-pxc-0` Pod.

* Check logs of the `database` container:

    ``` {.bash data-prompt="$" }
    $ kubectl logs cluster1-instance1-b5mr-0 --container database
    ```

* Check logs of the `pgbackrest` container:

    ``` {.bash data-prompt="$" }
    $ kubectl logs cluster1-instance1-b5mr-0 --container pgbackrest
    ```

* Filter logs of the `database` container which are not older than 600 seconds:

    ``` {.bash data-prompt="$" }
    $ kubectl logs cluster1-instance1-b5mr-0 --container database --since=600s
    ```

* Check logs of a previous instantiation of the `database` container, if any:

    ``` {.bash data-prompt="$" }
    $ kubectl logs cluster1-instance1-b5mr-0 --container database --previous
    ```

