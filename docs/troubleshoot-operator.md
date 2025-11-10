# Percona Operator Troubleshooting

This section provides information on how to troubleshoot when you are facing issues with Percona Operator for PostgreSQL.

Ensure CLI tool `kubectl` is installed to interact with Kubernetes API


## Check connection to Kubernetes cluster

Check connectivity to your Kubernetes API

1. To verify it, run the following command:

    ```{.bash data-prompt="$"}
    $ kubectl cluster-info
    ```    

    If you see the output similar to the following, it means that `kubectl` is connected to your Kubernetes cluster:    

    ??? example "Sample output"    

        ```{.text .no-copy}
        Kubernetes control plane is running at https://<control-plane-ip>:49475
        CoreDNS is running at https://<control-plane-ip>:49475/api/v1/namespaces/kube-system/services/kube-dns:dns/proxy 
        ```

    If multiple kubernetes configuration are present in kubeconfig,check if you have set the correct context , if not use the right context.
    ```{.bash data-prompt="$"}
    $ kubectl config current-context # Get the current Context
    ```       

    ```{.bash data-prompt="$"}
    $ kubectl config use-context <Context-To-Be-Used> # Switch the context
    ```   
    Run the `kubectl cluster-info` command again to verify that `kubectl` is connected to your Kubernetes cluster.
    If you are still running into issues, check with your kubernetes cluster administrator to resolve the connectivity or configuration issues. 
    

## Operator Installation Issues Troubleshooting

1. Operator installation requires certain priviliges like installing custom resource definitions etc.

To check it, use the following script:

```{.bash data-prompt="$"}
$ bash <(curl -s https://gist.githubusercontent.com/cshiv/6048bdd0174275b48f633549c69d0844/raw/fd547b783a30b827362ee9f9ec03436f9bc79524/check_priviliges.sh)
```

??? example "Sample output"
    
    ```{.text .no-copy}
    Checking privileges to install Percona Operators in kubernetes cluster...
    Warning: Unable to check the privileges for resource 'issuers', check if the resource 'issuers' is present in the cluster
    Warning: Unable to check the privileges for resource 'certificates', check if the resource 'certificates' is present in the cluster    

    Warning: Some resources are not found in the kubernetes cluster.Check the Warning messages before you proceed
    ------------------------------------------------------------------------------------------
    GOOD TO INSTALL: Percona Operator for PostgreSQL
    https://docs.percona.com/percona-operator-for-postgresql/index.html
    ------------------------------------------------------------------------------------------
    GOOD TO INSTALL: Percona Operator for MySQL based on Percona XtraDB Cluster
    https://docs.percona.com/percona-operator-for-postgresql/index.html
    ------------------------------------------------------------------------------------------
    GOOD TO INSTALL: Percona Operator for MongoDB
    https://docs.percona.com/percona-operator-for-mongodb/index.html
    ```

If you have insufficient permissions, the script will show you which ones are missing for installing a particular Operator. In this case, contact the Kubernetes cluster administrator.

2. If the priviliges are present and the installation is still failing, check the events for any information.(It is important to note that Kubernetes Events are stored for only 60 minutes)

    ```{.bash data-prompt="$"}
    $ kubectl get events --sort-by=".lastTimestamp"
    ```  
Events provide good information about affinity issues, resource issues etc.

3. Check the operator logs 

    ```{.bash data-prompt="$"}
    $ kubectl logs deploy/<operator-deployment-name>
    ```  

## Database Cluster Issues Troubleshooting


1. Operator has to be in `Running` state for Database Cluster to work. Check for the number of restarts in the operator pod, check for the restarts. 

    ```{.bash data-prompt="$"}
    $ kubectl get po <operator-pod-name>
    ```  

2. Check the status of Database cluster

    ```{.bash data-prompt="$"}
    $ kubectl get pg <database-cluster-name>
    ```  
    Cluster should ideally be in `Running` state. Cluster will transition to `initializing` state when any reconciliation is done for changes. If the cluster is in initializing state for too long, check for further issues

3. Check the operator logs

    ```{.bash data-prompt="$"}
    $ kubectl logs deploy/<operator-deployment-name>
    ```  

4. Check the events

    ```{.bash data-prompt="$"}
    $ kubectl get events --sort-by=".lastTimestamp"
    ```  

    Events can provide information like storage class issues, PVC binding issues etc

 5. Check for the PVC, PV. Both of them should be in `Bound` status

    ```{.bash data-prompt="$"}
    $ kubectl get pvc
    ```  

    ```{.bash data-prompt="$"}
    $ kubectl get pv
    ```  

6. Check for logs of Database pods / Proxy pods

    ```{.bash data-prompt="$"}
    $ kubectl logs <database-pod-name>
    ```  

    ```{.bash data-prompt="$"}
    $ kubectl logs <proxy-pod-name>
    ```  
    If logs of `init` containers or other side car containers needs to be checked use the option `-c`

    ```{.bash data-prompt="$"}
    $ kubectl logs <proxy-pod-name> -c postgres-startup
    ```    

7. If any commands needs to be executed inside the container, run the command with exec

    ```{.bash data-prompt="$"}
    $ kubectl exec <pod-name> -- <command>
    ```  

    If an interactive terminal is needed for running many commands, use the option `-it` for interactive terminal
    ```{.bash data-prompt="$"}
    $ kubectl exec -ti <pod-name> -- sh
    ```  
    
8. If the Pods are not in a running state, executing a command or an interactive terminal might not be possible. In this situation use `sleep-forever` file to stop the restarting of containers. 
Example: PXC Link (https://docs.percona.com/percona-operator-for-mysql/pxc/debug-shell.html#avoid-the-restart-on-fail-loop-for-percona-xtradb-cluster-containers) , Similar feature for PG will be done this quarter
