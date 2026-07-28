# Install Percona Operator for PostgreSQL on Rancher Kubernetes Engine (RKE2)

This guide shows you how to deploy Percona Operator for PostgreSQL on
[Rancher Kubernetes Engine (RKE2) :octicons-link-external-16:](https://docs.rke2.io/).
RKE2 is a CNCF-certified Kubernetes distribution that you can run standalone or
manage with the [Rancher :octicons-link-external-16:](https://ranchermanager.docs.rancher.com/)
Kubernetes management platform.

The document assumes some experience with the platform. For more information,
see the [RKE2 official documentation :octicons-link-external-16:](https://docs.rke2.io/).

## Prerequisites

The following tools and access are required:

1. **Linux hosts** that meet the [RKE2 requirements :octicons-link-external-16:](https://docs.rke2.io/install/requirements). For a production-like setup, use at least 3 nodes so the Operator can schedule instance Pods according to the [system requirements](System-Requirements.md).

2. **Root or sudo** access on each host to install and start RKE2 services.

3. **kubectl** to manage and deploy applications on Kubernetes. Install it
    [following the official installation instructions :octicons-link-external-16:](https://kubernetes.io/docs/tasks/tools/install-kubectl/).
    RKE2 also ships a `kubectl` binary under `/var/lib/rancher/rke2/bin/` on
    server nodes.

4. Optionally, a **Rancher** management server if you prefer to provision and
    manage the RKE2 cluster from the Rancher UI instead of installing RKE2
    manually. See the [Rancher documentation :octicons-link-external-16:](https://ranchermanager.docs.rancher.com/).

## Create the RKE2 cluster

You can create the cluster [with the RKE2 installation script :octicons-link-external-16:](https://docs.rke2.io/install/quickstart) or [provision it
through Rancher :octicons-link-external-16:](https://ranchermanager.docs.rancher.com/how-to-guides/new-user-guides/launch-kubernetes-with-rancher). Both approaches give you a standard Kubernetes API endpoint
that the Operator uses.


## Configure kubectl access

On a server node, RKE2 writes the kubeconfig to `/etc/rancher/rke2/rke2.yaml`.
Copy it to your workstation and point `kubectl` at it:

```bash
mkdir -p ~/.kube
sudo cat /etc/rancher/rke2/rke2.yaml > ~/.kube/rke2.yaml
export KUBECONFIG=~/.kube/rke2.yaml
```

If you connect from a remote machine, replace `127.0.0.1` in the kubeconfig
`server:` URL with the reachable address of your RKE2 server node.

Verify that the nodes are ready:

```bash
kubectl get nodes
```

## Configure storage

Percona Distribution for PostgreSQL needs PersistentVolumes for database data. Confirm
that your cluster has a default StorageClass (or note the StorageClass name to
set in the Custom Resource):

```bash
kubectl get storageclass
```

RKE2 does not always ship a default StorageClass. For testing, you can install
the [Local Path Provisioner :octicons-link-external-16:](https://github.com/rancher/local-path-provisioner).
For production, use a CSI driver appropriate for your infrastructure, such as
[Longhorn :octicons-link-external-16:](https://longhorn.io/) when you manage the cluster with Rancher.

## Install the Operator and deploy your PostgreSQL cluster

1. Create the Kubernetes namespace for your cluster. It is a good practice to isolate workloads in Kubernetes by installing the Operator in a custom namespace. :

    ```bash
    kubectl create namespace <namespace name>
    kubectl config set-context $(kubectl config current-context) --namespace=<namespace name>
    ```

    At success, you will see the message that `namespace/<namespace name>` was created, and the context was modified.

2. Deploy the Operator using the following command:

    ```bash
    kubectl apply --server-side -f https://raw.githubusercontent.com/percona/percona-postgresql-operator/v{{ release }}/deploy/bundle.yaml -n <namespace name>
    ```

    ??? example "Expected output"

        --8<-- "kubectl-apply-bundle-response.txt"

    At this point, the Operator Pod is up and running.

3. The Operator has been started, and you can deploy Percona Distribution for PostgreSQL:

    ```bash
    kubectl apply -f https://raw.githubusercontent.com/percona/percona-postgresql-operator/v{{ release }}/deploy/cr.yaml 
    ```

    ??? example "Expected output"

        ``` {.text .no-copy}
        perconapgcluster.pgv2.percona.com/cluster1 created
        ```
    It may take some time to create the database cluster. When the process is over your
    cluster will obtain the `ready` status. You can check it with the following
    command:

    ```bash
    kubectl get pg 
    ```

    ??? example "Expected output"

        --8<-- "kubectl-get-pg-response.txt"

## Verifying the cluster operation

After the cluster status is `ready`, you can try to connect
to the cluster.

{% include 'assets/fragments/connectivity.txt' %}

## Troubleshooting

If `kubectl get pg` command doesn't show `ready` status too long, you can
check the creation process with the `kubectl get pods` command:

```bash
kubectl get pods
```

??? example "Expected output"

    --8<-- "kubectl-get-pods-response.txt"

If the command output had shown some errors, you can examine the problematic
Pod with the `kubectl describe <pod name>` command as follows:

```bash
kubectl describe pod cluster1-instance1-XXXX-0 
```

Review the detailed information for `Warning` statements and then correct the
configuration. An example of a warning is as follows:

`Warning  FailedScheduling  68s (x4 over 2m22s)  default-scheduler  0/1 nodes are available: 1 node(s) didn’t match pod affinity/anti-affinity, 1 node(s) didn’t satisfy existing pods anti-affinity rules.`

If Pods stay in the `Pending` state because volumes cannot be provisioned,
confirm that a StorageClass exists and that your Custom Resource references the
correct one.

## Removing the RKE2 cluster

To tear down a manually installed RKE2 cluster, run the uninstall script on each
node (agent nodes first, then server nodes):

```bash
/usr/local/bin/rke2-uninstall.sh
```

If you provisioned the cluster with Rancher, delete the cluster from the Rancher
UI instead.

!!! warning

    After deleting the cluster, all data stored in it will be lost!
