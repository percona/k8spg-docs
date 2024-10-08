# Kubernetes environment troubleshooting

This section provides information on how to troubleshoot Kubernetes environment if you are facing issues with installing Percona Operator for PostgreSQL.

We will use `kubectl` – the command-line tool for interacting with the Kubernetes API.

Let’s start with these basic troubleshooting steps.

## Check connection to Kubernetes cluster

It may happen that `kubectl` you installed locally is not connected to your Kubernetes cluster. 

1. To verify it, run the following command:

    ```{.bash data-prompt="$"}
    $ kubectl cluster-info
    ```    

    If you see the output similar to the following, it means that `kubectl` is connected to your Kubernetes cluster:    

    ??? example "Sample output"    

        ```{.text .no-copy}
        Kubernetes control plane is running at https://127.0.0.1:49475
        CoreDNS is running at https://127.0.0.1:49475/api/v1/namespaces/kube-system/services/kube-dns:dns/proxy 
        ```

2. If you see the errors, do the following:

    === "Google Kubernetes Engine (GKE)"    

        1. Check if you have Google Cloud SDK installed and that you can interact with it by running `gcloud` in your terminal. If not, refer to the Google Cloud SDK Documentation for [installation instructions :octicons-link-external-16:](https://cloud.google.com/sdk/docs/install).
        2. In the Google Cloud Console, select your cluster and then click **Connect**. You will see the connect statement which configures the command-line access. After you have edited the statement, run the following command in your local shell replacing the `<project name>` with your project name:    

           ```{.bash data-prompt="$"}
           $ gcloud container clusters get-credentials cluster-1 --zone us-central1-a --project <project name>
           ```    

        3. Use your Cloud Identity and Access Management (Cloud IAM) to control the access to the cluster. The following command gives you the ability to create Roles and RoleBindings:    

           ```{.bash data-prompt="$"}
           $ kubectl create clusterrolebinding cluster-admin-binding --clusterrole cluster-admin --user $(gcloud config get-value core/account)
           ```    

           !!! note ""    

               You may have the error like the following:    

               ```{.text .no-copy}
               error: failed to create clusterrolebinding: Post “https://34.66.76.82/apis/rbac.authorization.k8s.io/v1/clusterrolebindings?fieldManager=kubectl-create&fieldValidation=Strict”: getting credentials: exec: executable gke-gcloud-auth-plugin not found
               ```    

               In this case, follow these steps:    

               1. Install the `gke-gcloud-auth-plugin` using the following command:    

    			  ```{.bash data-prompt="$"}
    			  $ gcloud components install gke-gcloud-auth-plugin
    			  ```
    		   2. Authenticate to Google Cloud SDK using this command:    

    			  ```{.bash data-prompt="$"}
    			  $ gcloud auth login
    			  ```
    		   
    		   3. Run the `kubectl create clusterrolebinding` command again.    
    

    === "Amazon Elastic Kubernetes Engine (AWS EKS)"    

        1. Check that you have installed the [Amazon EBS CSI driver :octicons-link-external-16:](https://docs.aws.amazon.com/eks/latest/userguide/ebs-csi.html). Otherwise install it using one of the suggested methods: [as an add-on :octicons-link-external-16:](https://docs.aws.amazon.com/eks/latest/userguide/managing-ebs-csi.html) or [as a self-managed installation :octicons-link-external-16:](https://github.com/kubernetes-sigs/aws-ebs-csi-driver)
        2. Enable `kubectl` to communicate with your cluster by adding a new context to the `kubectl` config file. 
           
    	   ```{.bash data-prompt="$"}
    	   $ aws eks --region region update-kubeconfig --name cluster_name
    	   ```    

    === "Minikube"

        1. When deploying Kubernetes locally using Minikube, you may need to allocate additional resources. The recommended minimum resources are 4 CPUs, 30 Gb disk size and 5 GB of RAM. To start Minikube with these resources, run the following command:

		    ```{.bash data-prompt="$"}
		    $ minikube start --memory=5120 --cpus=4 --disk-size=30g
		    ```

        2. To check if your `kubectl` is connected to Minikube, use the following command to check the current context. The current context determines which cluster `kubectl` is interacting with. You can get the current context by running the command:
        
    		```{.bash data-prompt="$"}
    		$ kubectl config current-context
    		```    

    		If the output is `minikube`, then `kubectl` is configured to interact with your Minikube cluster.    

            If the context is other, you need to switch to Minikube context by running the following command:    

    		```{.bash data-prompt="$"}
    		$ kubectl config use-context minikube
    		```


3. Run the `kubectl cluster-info` command again to verify that `kubectl` is connected to your Kubernetes cluster.


## Check Kubernetes Nodes

Check that your Kubernetes cluster nodes are registered correctly. Run the following command:

```{.bash data-prompt="$"}
$ kubectl get nodes
```

All nodes must be listed and must have the `Ready` status that indicates that the node is healthy and can accept pods. 

If you see the nodes in the `NotReady` status, it means that there are issues with the nodes. To get detailed information about a node, run the following commands:

```{.bash data-prompt="$"}
$ kubectl describe node <node-name>
```

Or, you can use the following command:

```{.bash data-prompt="$"}
$ kubectl get node <node-name> -o yaml
```

Both commands provide detailed information about the node, including the resources allocated to it, the pods running on the node, and the events related to the node.

## Check user permissions

It may happen that your user doesn’t have enough permissions for installing the Operator. To check it, use the following script:

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




