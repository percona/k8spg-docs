> For the complete documentation index, see [llms.txt](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/llms.txt).

# Percona Operator troubleshooting

This section provides information on how to troubleshoot issues when you install Percona Operator for PostgreSQL.

Make sure you have CLI tool `kubectl` installed to interact with Kubernetes API.

## Check connection to Kubernetes cluster

It may happen that `kubectl` you installed locally is not connected to your Kubernetes cluster.

To check connectivity to your Kubernetes API, run the following command:

```
kubectl cluster-info
```

If you see the output similar to the following, it means that `kubectl` is connected to your Kubernetes cluster:

Sample output

```
Kubernetes control plane is running at https://<control-plane-ip>:49475
CoreDNS is running at https://<control-plane-ip>:49475/api/v1/namespaces/kube-system/services/kube-dns:dns/proxy
```

If multiple Kubernetes configurations are present in `kubeconfig`,check if you have set the correct context. If the context is wrong, switch it. Here’s how:

1. Check the current context:

   ```
   kubectl config current-context # Get the current Context
   ```

1. Switch the context :

   ```
   kubectl config use-context <Context-To-Be-Used>
   ```

1. Run the `kubectl cluster-info` command again to verify that `kubectl` is connected to your Kubernetes cluster.

If you are still running into issues, check with your Kubernetes cluster administrator to resolve the connectivity or configuration issues.

## Troubleshoot Operator installation issues

1. Check the Operator logs

   ```
   kubectl logs deploy/<operator-deployment-name>
   ```

1. Installing the Operator requires specific privileges, such as the ability to create custom resource definitions and other Kubernetes objects.

   To verify that you have the necessary privileges, run the following script:

   ```
   bash <(curl -s https://gist.githubusercontent.com/cshiv/6048bdd0174275b48f633549c69d0844/raw/fd547b783a30b827362ee9f9ec03436f9bc79524/check_priviliges.sh)
   ```

   Sample output

   ```
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

1. If you have the necessary privileges but the installation is still failing, review the Kubernetes Events for more details. Keep in mind that Kubernetes Events are retained for only 60 minutes.

   ```
   kubectl get events --sort-by=".lastTimestamp"
   ```

   Events provide good information about affinity issues, resource issues etc.

## Troubleshooting database cluster issues

1. The Operator deployment must be in the `Running` state for the database cluster to function properly. Check the Operator Pod for restarts to identify potential issues.

   ```
   kubectl get pod <operator-pod-name>
   ```

1. Check the status of the database cluster

   ```
   kubectl get pg <database-cluster-name>
   ```

   The cluster should typically be in the `ready` state. It may briefly enter the `initializing` state while reconciling changes. If the cluster remains in the `initializing` state for an extended period, investigate further to identify any underlying issues.

   Additionally, you can describe the database cluster and check the `State` field and the `Conditions` list in the `Status` section. Each condition has a reason and a message that explain what isn’t ready. See [Custom resource statuses](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/cr-statuses.html) for details:

   ```
   kubectl describe pg <database-cluster-name>
   ```

1. Check the Operator logs

   ```
   kubectl logs deploy/<operator-deployment-name>
   ```

1. Check the events

   ```
   kubectl get events --sort-by=".lastTimestamp"
   ```

   Events can provide information like storage class issues, PVC binding issues etc

1. Check for the PVC, PV. Both of them should be in `Bound` status

   ```
   kubectl get pvc
   ```

   ```
   kubectl get pv
   ```

1. Check for logs of database pods / Proxy pods

   ```
   kubectl logs <database-pod-name>
   ```

   ```
   kubectl logs <proxy-pod-name>
   ```

   To check logs of `init` containers or other sidecar containers, use the option `-c` with the container name:

   ```
   kubectl logs <proxy-pod-name> -c postgres-startup
   ```

1. Check for error details. Run the `kubectl describe` command:

   ```
   kubectl describe <database-pod-name>
   ```

   ```
   kubectl describe <proxy-pod-name>
   ```

   Check the information in the `Status` section. The `State` and `State Description` fields explain why the Pod reports errors.

1. To run commands inside a container, use the `kubectl exec` command:

   ```
   kubectl exec <pod-name> -- <command>
   ```

   If you need an interactive shell to run multiple commands, use the `-it` flag for an interactive terminal:

   ```
   kubectl exec -it <pod-name> -- sh
   ```

1. If the pods are not running, it may not be possible to execute commands or open an interactive shell. In such cases, consider using a `sleep-forever` script to prevent the containers from restarting repeatedly.

See the [Disable health check probes for maintenance](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/manage-manually.html#disable-health-check-probes-for-maintenance) section for steps.

## Profiling the Operator with pprof

When you need to investigate Operator performance issues, high CPU usage, or memory leaks, you can collect CPU and memory profiles using Go’s pprof tooling.

1. Enable pprof by setting the `PPROF_BIND_ADDRESS` environment variable in the Operator Deployment. For example, set it to `127.0.0.1:6060` to bind pprof to localhost on port 6060. See [PPROF_BIND_ADDRESS](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/env-var-operator.html#pprof_bind_address) for configuration details.

1. Restart the Operator so the new configuration takes effect.

1. Set up a port-forward to the Operator Pod:

   ```
   kubectl port-forward deploy/percona-postgresql-operator 6060:6060 -n <operator-namespace>
   ```

1. In another terminal, collect profiles using `go tool pprof`:

   **CPU profile** (30 seconds):

   ```
   go tool pprof http://localhost:6060/debug/pprof/profile?seconds=30
   ```

   **Heap (memory) profile**:

   ```
   go tool pprof http://localhost:6060/debug/pprof/heap
   ```

   **Goroutine profile** (useful for deadlock investigation):

   ```
   go tool pprof http://localhost:6060/debug/pprof/goroutine
   ```

1. After collecting a profile, you can analyze it interactively. For example, type `top` to see the functions consuming the most CPU or memory, or `web` to generate a flame graph (requires Graphviz).

Note

Disable pprof when you finish troubleshooting by setting `PPROF_BIND_ADDRESS` to `"0"` or `""`. Keeping it enabled in production is not recommended for security reasons.
