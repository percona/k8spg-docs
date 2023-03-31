# Monitoring

Percona Monitoring and Management (PMM) [provides an excellent
solution](https://www.percona.com/doc/percona-monitoring-and-management/2.x/setting-up/client/postgresql.html)
to monitor Percona Distribution for PostgreSQL.

!!! note

    Only PMM 2.x versions are supported by the Operator.

PMM is a client/server application. [PMM Client](https://www.percona.com/doc/percona-monitoring-and-management/2.x/details/architecture.html#pmm-client) runs on each node with the
database you wish to monitor: it collects needed metrics and sends gathered data
to [PMM Server](https://www.percona.com/doc/percona-monitoring-and-management/2.x/details/architecture.html#pmm-server). As a user, you connect to PMM Server to see database metrics on
a [number](https://www.percona.com/doc/percona-monitoring-and-management/2.x/details/dashboards/dashboard-postgresql-instances-overview.html) [of](https://www.percona.com/doc/percona-monitoring-and-management/2.x/details/dashboards/dashboard-postgresql-instance-summary.html) [dashboards](https://www.percona.com/doc/percona-monitoring-and-management/2.x/details/dashboards/dashboard-postgresql-instances-compare.html).

That’s why PMM Server and PMM Client need to be installed separately.

## Installing the PMM Server

PMM Server runs as a *Docker image*, a *virtual appliance*, or on an *AWS instance*.
Please refer to the [official PMM documentation](https://www.percona.com/doc/percona-monitoring-and-management/2.x/setting-up/server/index.html)
for the installation instructions.

## Installing the PMM Client

The following steps are needed for the PMM client installation in your
Kubernetes-based environment:


1. The PMM client installation is initiated by updating the `pmm`
    section in the
    [deploy/cr.yaml](https://github.com/percona/percona-postgresql-operator/blob/v{{ release }}/deploy/cr.yaml)
    file.

    * set `pmm.enabled=true`
    * set the `pmm.serverHost` key to your PMM Server hostname,
    * check that  the `serverUser` key contains your PMM Server user name
        (`admin` by default),
    * make sure the `pmmserver` key in the
        [deploy/pmm-secret.yaml](https://github.com/percona/percona-postgresql-operator/blob/v{{ release }}/deploy/pmm-secret.yaml)
        secrets file contains the password specified for the PMM Server during its
        installation.

    Apply changes with the `kubectl apply -f deploy/pmm-secret.yaml` command.

    !!! info

        You use `deploy/pmm-secret.yaml` file to *create* Secrets Object.
        The file contains all values for each key/value pair in a convenient
        plain text format. But the resulting Secrets contain passwords stored
        as base64-encoded strings. If you want to *update* password field,
        you’ll need to encode the value into base64 format. To do this, you can
        run `echo -n "password" | base64 --wrap=0` (or just
        `echo -n "password" | base64` in case of Apple macOS) in your local
        shell to get valid values. For example, setting the PMM Server user’s
        password to `new_password` in the `cluster1-pmm-secret` object can be
        done with the following command:

        === "in Linux"

            ``` {.bash data-prompt="$" }
            $ kubectl patch secret/cluster1-pmm-secret -p '{"data":{"pmmserver": '$(echo -n new_password | base64 --wrap=0)'}}'
            ```

        === "in macOS"

            ``` {.bash data-prompt="$" }
            $ kubectl patch secret/cluster1-pmm-secret -p '{"data":{"pmmserver": '$(echo -n new_password | base64)'}}'
            ```

    When done, apply the edited `deploy/cr.yaml` file:

    ``` {.bash data-prompt="$" }
    $ kubectl apply -f deploy/cr.yaml
    ```

2. Check that corresponding Pods are not in a cycle of stopping and restarting.
    This cycle occurs if there are errors on the previous steps:

    ``` {.bash data-prompt="$" }
    $ kubectl get pods
    $ kubectl logs cluster1-7b7f7898d5-7f5pz -c pmm-client
    ```

3. Now you can access PMM via *https* in a web browser, with the
    login/password authentication, and the browser is configured to show
    Percona Distribution for PostgreSQL metrics.
