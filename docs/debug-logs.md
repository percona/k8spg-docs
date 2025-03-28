# Check the logs

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

In the following examples we will access containers of the `cluster1-instance1-b5mr-0` Pod.

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

## Increase pgBackRest log verbosity

The pgBackRest tool used for backups [supports different log verbosity levels :octicons-link-external-16:](https://pgbackrest.org/configuration.html#section-log/option-log-level-stderr). By default, it logs warnings and errors, but sometimes fixing backup/restore issues can be simpler when you get more debugging information from it.

Log verbosity is controlled by pgBackRest [--log-level-stderr :octicons-link-external-16:](https://pgbackrest.org/configuration.html#section-log/option-log-level-stderr) option.

You can add it to the `deploy/backup.yaml` file to use it with [on-demand backups](backups-ondemand.md) as follows:

```yaml
apiVersion: pgv2.percona.com/v2
kind: PerconaPGBackup
metadata:
  name: backup1
spec:
  pgCluster: cluster1
  repoName: repo1
  options:
  - --log-level-stderr=debug
```

