# Monitoring

In this section you will learn how to monitor the health of Percona Distribution for PostgreSQL with [Percona Monitoring and Management (PMM)](https://www.percona.com/doc/percona-monitoring-and-management/2.x/setting-up/client/postgresql.html). 
 
!!! note

    Only PMM 2.x versions are supported by the Operator.

PMM is a client/server application. It includes the [PMM Server](https://www.percona.com/doc/percona-monitoring-and-management/2.x/details/architecture.html#pmm-server) and the number of [PMM Clients](https://www.percona.com/doc/percona-monitoring-and-management/2.x/details/architecture.html#pmm-client) running on each node with the
database you wish to monitor. 

A PMM Client collects needed metrics and sends gathered data
to the PMM Server. As a user, you connect to the PMM Server to see database metrics on
a [number](https://www.percona.com/doc/percona-monitoring-and-management/2.x/details/dashboards/dashboard-postgresql-instances-overview.html) [of](https://www.percona.com/doc/percona-monitoring-and-management/2.x/details/dashboards/dashboard-postgresql-instance-summary.html) [dashboards](https://www.percona.com/doc/percona-monitoring-and-management/2.x/details/dashboards/dashboard-postgresql-instances-compare.html).

PMM Server and PMM Client are installed separately.

## Install PMM Server

You must have PMM server up and running. You can run PMM Server as a *Docker image*, a *virtual appliance*, or on an *AWS instance*.
Please refer to the [official PMM documentation](https://www.percona.com/doc/percona-monitoring-and-management/2.x/setting-up/server/index.html)
for the installation instructions.

## Install PMM Client

To install PMM Client as a side-car container in your Kubernetes-based environment, do the following:

1. [Get the PMM API key from PMM Server](https://docs.percona.com/percona-monitoring-and-management/details/api.html#api-keys-and-authentication). The API key must have the role "Admin". You need this key to authorize PMM Client within PMM Server. 

    === "From PMM UI" 

        [Generate the PMM API key](https://docs.percona.com/percona-monitoring-and-management/details/api.html#api-keys-and-authentication){.md-button} 

    === "From command line"

        You can query your PMM Server installation for the API
        Key using `curl` and `jq` utilities. Replace `<login>:<password>@<server_host>` placeholders with your real PMM Server login, password, and hostname in the following command:
        
        ``` {.bash data-prompt="$" }
        $ API_KEY=$(curl --insecure -X POST -H "Content-Type: application/json" -d '{"name":"operator", "role": "Admin"}' "https://<login>:<password>@<server_host>/graph/api/auth/keys" | jq .key)
        ```

    !!! note

        The API key is not rotated. 

2. Specify the API key as the `PMM_SERVER_KEY` value in the [deploy/secrets.yaml](https://github.com/percona/percona-postgresql-operator/blob/main/deploy/secrets.yaml) secrets file.

    ```yaml
    apiVersion: v1
    kind: Secret
    metadata:
      name: cluster1-pmm-secret
    type: Opaque
    stringData:
      PMM_SERVER_KEY: ""
    ``` 

3. Create the Secrets object using the `deploy/secrets.yaml` file.

    ```{.bash data-prompt="$"}
    $ kubectl apply -f deploy/secrets.yaml -n postgres-operator
    ```

4. Update the `pmm` section in the
    [deploy/cr.yaml](https://github.com/percona/percona-postgresql-operator/blob/master/deploy/cr.yaml) file. 

      * Set `pmm.enabled`=`true`.
      * Specify your PMM Server hostname / an IP address for the `pmm.serverHost` option. The PMM Server IP address should be resolvable and reachable from within your cluster.

     ```yaml
       pmm:
         enabled: true
         image: percona/pmm-client:{{pmm2recommended}}
     #    imagePullPolicy: IfNotPresent
         secret: cluster1-pmm-secret
         serverHost: monitoring-service
     ```
    
5. Update the cluster

    ```{.bash data-prompt="$"}
    $ kubectl apply -f deploy/cr.yaml -n postgres-operator
    ```
        
6. Check that corresponding Pods are not in a cycle of stopping and restarting.
    This cycle occurs if there are errors on the previous steps:

    ``` {.bash data-prompt="$" }
    $ kubectl get pods -n postgres-operator
    $ kubectl logs <pod_name> -c pmm-client
    ```

    
### Update the secrets file

The `deploy/secrets.yaml` file contains all values for each key/value pair in a convenient plain text format. But the resulting Secrets Objects contains passwords stored as base64-encoded strings. If you want to *update* the password field, you need to encode the new password into the base64 format and pass it to the Secrets Object.

1. Encode the password

    === "in Linux" 

        ```{.bash data-prompt="$"} 
        $ echo -n "password" | base64 --wrap=0
        ``` 

    === "in macOS" 

        ```{.bash data-prompt="$"} 
        $ echo -n "password" | base64
        ```

2. Update the Secrets Object. For example, use the following command to set the PMM Server user’s
        password to `new_password` in the `cluster1-pmm-secret` Secrets Object 

    === "in Linux"

        ``` {.bash data-prompt="$" }
        $ kubectl patch secret/cluster1-pmm-secret -p '{"data":{"PMM_SERVER_KEY": '$(echo -n new_password | base64 --wrap=0)'}}'
        ```

    === "in macOS"

        ``` {.bash data-prompt="$" }
        $ kubectl patch secret/cluster1-pmm-secret -p '{"data":{"PMM_SERVER_KEY": '$(echo -n new_password | base64)'}}'
        ```

3. Apply the edited `deploy/cr.yaml` file, replace the `<namespace>` placeholder with your namespace:

    ``` {.bash data-prompt="$" }
    $ kubectl apply -f deploy/cr.yaml -n <namespace>
    ```

## Check the metrics

1. Log in to PMM server.

2. Click :simple-postgresql: *PostgreSQL* from the left-hand navigation menu. You land on the Instances Overview page. 

3. Click :simple-postgresql: *PostgreSQL*  →  *Other dashboards* to see the list of available dashboards for you to drill down to the metrics you are interested in. 

## Useful links

* [Prepare for production guide](production.md)
* [Monitor Kubernetes health](monitor-kubernetes.md)
