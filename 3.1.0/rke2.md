> For the complete documentation index, see [llms.txt](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/llms.txt).

# Install Percona Operator for PostgreSQL on Rancher Kubernetes Engine (RKE2)

This guide shows you how to deploy Percona Operator for PostgreSQL on [Rancher Kubernetes Engine (RKE2)](https://docs.rke2.io/) . RKE2 is a CNCF-certified Kubernetes distribution that you can run standalone or manage with the [Rancher](https://ranchermanager.docs.rancher.com/) Kubernetes management platform.

The document assumes some experience with the platform. For more information, see the [RKE2 official documentation](https://docs.rke2.io/) .

## Prerequisites

The following tools and access are required:

1. **Linux hosts** that meet the [RKE2 requirements](https://docs.rke2.io/install/requirements) . For a production-like setup, use at least 3 nodes so the Operator can schedule instance Pods according to the [system requirements](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/System-Requirements.html).
1. **Root or sudo** access on each host to install and start RKE2 services.
1. **kubectl** to manage and deploy applications on Kubernetes. Install it [following the official installation instructions](https://kubernetes.io/docs/tasks/tools/install-kubectl/) . RKE2 also ships a `kubectl` binary under `/var/lib/rancher/rke2/bin/` on server nodes.
1. Optionally, a **Rancher** management server if you prefer to provision and manage the RKE2 cluster from the Rancher UI instead of installing RKE2 manually. See the [Rancher documentation](https://ranchermanager.docs.rancher.com/) .

## Create the RKE2 cluster

You can create the cluster [with the RKE2 installation script](https://docs.rke2.io/install/quickstart) or [provision it through Rancher](https://ranchermanager.docs.rancher.com/how-to-guides/new-user-guides/launch-kubernetes-with-rancher) . Both approaches give you a standard Kubernetes API endpoint that the Operator uses.

## Configure kubectl access

On a server node, RKE2 writes the kubeconfig to `/etc/rancher/rke2/rke2.yaml`. Copy it to your workstation and point `kubectl` at it:

```
mkdir -p ~/.kube
sudo cat /etc/rancher/rke2/rke2.yaml > ~/.kube/rke2.yaml
export KUBECONFIG=~/.kube/rke2.yaml
```

If you connect from a remote machine, replace `127.0.0.1` in the kubeconfig `server:` URL with the reachable address of your RKE2 server node.

Verify that the nodes are ready:

```
kubectl get nodes
```

## Configure storage

Percona Distribution for PostgreSQL needs PersistentVolumes for database data. Confirm that your cluster has a default StorageClass (or note the StorageClass name to set in the Custom Resource):

```
kubectl get storageclass
```

RKE2 does not always ship a default StorageClass. For testing, you can install the [Local Path Provisioner](https://github.com/rancher/local-path-provisioner) . For production, use a CSI driver appropriate for your infrastructure, such as [Longhorn](https://longhorn.io/) when you manage the cluster with Rancher.

## Install the Operator and deploy your PostgreSQL cluster

1. Create the Kubernetes namespace for your cluster. It is a good practice to isolate workloads in Kubernetes by installing the Operator in a custom namespace.

   ```
   kubectl create namespace <namespace name>
   kubectl config set-context $(kubectl config current-context) --namespace=<namespace name>
   ```

   At success, you will see the message that `namespace/<namespace name>` was created, and the context was modified.

1. Deploy the Operator using the following command:

   ```
   kubectl apply --server-side -f https://raw.githubusercontent.com/percona/percona-postgresql-operator/v3.1.0/deploy/bundle.yaml -n <namespace name>
   ```

   Expected output

   ```
   customresourcedefinition.apiextensions.k8s.io/crunchybridgeclusters.postgres-operator.crunchydata.com serverside-applied
   customresourcedefinition.apiextensions.k8s.io/perconapgbackups.pgv2.percona.com serverside-applied
   customresourcedefinition.apiextensions.k8s.io/perconapgclusters.pgv2.percona.com serverside-applied
   customresourcedefinition.apiextensions.k8s.io/perconapgrestores.pgv2.percona.com serverside-applied
   customresourcedefinition.apiextensions.k8s.io/perconapgupgrades.pgv2.percona.com serverside-applied
   customresourcedefinition.apiextensions.k8s.io/pgadmins.postgres-operator.crunchydata.com serverside-applied
   customresourcedefinition.apiextensions.k8s.io/pgupgrades.postgres-operator.crunchydata.com serverside-applied
   customresourcedefinition.apiextensions.k8s.io/postgresclusters.postgres-operator.crunchydata.com serverside-applied
   serviceaccount/percona-postgresql-operator serverside-applied
   role.rbac.authorization.k8s.io/percona-postgresql-operator serverside-applied
   rolebinding.rbac.authorization.k8s.io/service-account-percona-postgresql-operator serverside-applied
   deployment.apps/percona-postgresql-operator serverside-applied
   ```

   At this point, the Operator Pod is up and running.

1. The Operator has been started, and you can deploy Percona Distribution for PostgreSQL:

   ```
   kubectl apply -f https://raw.githubusercontent.com/percona/percona-postgresql-operator/v3.1.0/deploy/cr.yaml
   ```

   Expected output

   ```
   perconapgcluster.pgv2.percona.com/cluster1 created
   ```

   It may take some time to create the database cluster. When the process is over your cluster will obtain the `ready` status. You can check it with the following command:

   ```
   kubectl get pg
   ```

   Expected output

   ```
   NAME       ENDPOINT                         STATUS   POSTGRES   PGBOUNCER   AGE
   cluster1   cluster1-pgbouncer.default.svc   ready    3          3           30m
   ```

## Verifying the cluster operation

After the cluster status is `ready`, you can try to connect to the cluster.

When the Operator deploys a database cluster, it generates several [Secrets](https://kubernetes.io/docs/concepts/configuration/secret/) . Among them there is the Secret with the credentials of the default PostgreSQL user. This default user has the same username as the cluster name.

1. Use `kubectl get secrets -n <namespace>` command to see the list of Secrets objects. The Secrets object you are interested in is named in the format `<cluster_name>-pguser-<cluster_name>` (where the `<cluster_name>` is the [name of your Percona Distribution for PostgreSQL Cluster](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/operator.html#metadata-name)). For example, if your cluster name is `cluster1`, the Secret name will be `cluster1-pguser-cluster1`.

1. Use the following command to get the password of this user. Replace the `<cluster_name>` and `<namespace>` placeholders with your values:

   ```
   kubectl get secret <cluster_name>-<user_name>-<cluster_name> -n <namespace> --template='{{.data.password | base64decode}}{{"\n"}}'
   ```

1. To connect to PostgreSQL, you will use the `pgbouncer` service as the entry point to your cluster. To find this service, use the following command:

   ```
   kubectl get svc -n <namespace>
   ```

   Look for the service named `<cluster-name>-pgbouncer`.

   Sample output

   ```
   cluster1-ha          ClusterIP   34.118.234.155   <none>        5432/TCP   51m
   cluster1-ha-config   ClusterIP   None             <none>        <none>     51m
   cluster1-pgbouncer   ClusterIP   34.118.239.5     <none>        5432/TCP   51m
   cluster1-pods        ClusterIP   None             <none>        <none>     51m
   cluster1-primary     ClusterIP   None             <none>        5432/TCP   51m
   cluster1-replicas    ClusterIP   34.118.234.19    <none>        5432/TCP   51m
   ```

1. Create a pod and start Percona Distribution for PostgreSQL inside. The following command will do this, naming the new Pod `pg-client`:

   ```
   kubectl run -n <namespace> -i --rm --tty pg-client --image=percona/percona-distribution-postgresql:18.6.1-3 --restart=Never -- bash -il
   ```

   It may require some time to execute the command and deploy the corresponding Pod.

1. Run a container with `psql` tool and connect its console output to your terminal. Substitute the `<namespace>` placeholder with your value in the following command to connect as a `cluster1` user to the `cluster1` database via the PostgreSQL interactive terminal.

   ```
   [postgres@pg-client /]$ PGPASSWORD='pguser_password' psql -h cluster1-pgbouncer.<namespace>.svc.cluster.local -p 5432 -U cluster1 cluster1
   ```

   Sample output

   ```
   psql (18.6.1-3)
   SSL connection (protocol: TLSv1.3, cipher: TLS_AES_256_GCM_SHA384, bits: 256, compression: off)
   Type "help" for help.
   pgdb=>
   ```

## Troubleshooting

If `kubectl get pg` command doesn’t show `ready` status too long, you can check the creation process with the `kubectl get pods` command:

```
kubectl get pods
```

Expected output

```
NAME                                           READY   STATUS      RESTARTS   AGE
cluster1-backup-4vwt-p5d9j                     0/1     Completed   0          97m
cluster1-instance1-b5mr-0                      4/4     Running     0          99m
cluster1-instance1-b8p7-0                      4/4     Running     0          99m
cluster1-instance1-w7q2-0                      4/4     Running     0          99m
cluster1-pgbouncer-79bbf55c45-62xlk            2/2     Running     0          99m
cluster1-pgbouncer-79bbf55c45-9g4cb            2/2     Running     0          99m
cluster1-pgbouncer-79bbf55c45-9nrmd            2/2     Running     0          99m
cluster1-repo-host-0                           2/2     Running     0          99m
percona-postgresql-operator-79cd8586f5-2qzcs   1/1     Running     0          120m
```

If the command output had shown some errors, you can examine the problematic Pod with the `kubectl describe <pod name>` command as follows:

```
kubectl describe pod cluster1-instance1-XXXX-0
```

Review the detailed information for `Warning` statements and then correct the configuration. An example of a warning is as follows:

`Warning FailedScheduling 68s (x4 over 2m22s) default-scheduler 0/1 nodes are available: 1 node(s) didn’t match pod affinity/anti-affinity, 1 node(s) didn’t satisfy existing pods anti-affinity rules.`

If Pods stay in the `Pending` state because volumes cannot be provisioned, confirm that a StorageClass exists and that your Custom Resource references the correct one.

## Removing the RKE2 cluster

To tear down a manually installed RKE2 cluster, run the uninstall script on each node (agent nodes first, then server nodes):

```
/usr/local/bin/rke2-uninstall.sh
```

If you provisioned the cluster with Rancher, delete the cluster from the Rancher UI instead.

Warning

After deleting the cluster, all data stored in it will be lost!
