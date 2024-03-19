# Install Percona Distribution for PostgreSQL with customized parameters

You can customize the configuration of Percona Distribution for PostgreSQL and install it with customized parameters.

To check available configuration options, see [deploy/cr.yaml :octicons-link-external-16:](https://raw.githubusercontent.com/percona/percona-postgresql-operator/v{{ release }}/deploy/cr.yaml) and [Custom Resource Options](operator.md). 

=== ":simple-kubernetes: kubectl"

    To customize the configuration when installing with `kubectl`, do the following:

    1. Clone the repository with all manifests and source code by executing the following command:

        ```{.bash data-prompt="$" }
        $ git clone -b v{{ release }} https://github.com/percona/percona-postgresql-operator
        ```    

    2. Edit the required options and apply your modified `deploy/cr.yaml` file as follows:

         ```{.bash data-prompt="$" }
         $ kubectl apply -f deploy/cr.yaml -n postgres-operator        
         ```

=== ":simple-helm: Helm"    

    To install Percona Distribution for PostgreSQL with custom parameters using Helm, use the following command:
    
    ```{.bash data-prompt="$" }
    $ helm install --set key=value
    ```

    You can pass any of the Operator’s [Custom Resource options](operator.md#operator-custom-resource-options) as a
    `--set key=value[,key=value]` argument.

    The following example deploys a PostgreSQL {{postgresrecommended}} based cluster
    in the `my-namespace` namespace, with enabled [Percona Monitoring and Management (PMM) :octicons-link-external-16:](https://www.percona.com/doc/percona-monitoring-and-management/2.x/index.html):

    ``` {.bash data-prompt="$" }
    $ helm install my-db percona/pg-db --version {{ release }} --namespace my-namespace \
      --set postgresVersion={{postgresrecommended}} \
      --set pmm.enabled=true
    ```
