# Use huge pages with Percona Operator for PostgreSQL

Normally, memory is managed in 4 KiB chunks, also called "pages". When your PostgreSQL workload grows, the CPU has to juggle a lot of these small pages.

Huge pages are memory pages of 2 MiB or 1 GiB instead of the default 4 KiB. PostgreSQL can place its main shared memory segment in huge pages, which makes memory use more predictable and reduces CPU overhead on large instances.

This page explains why huge pages matter for PostgreSQL, how to calculate how many of them your cluster needs and how to request them for PostgreSQL managed by the Operator. Use huge pages when you plan a production cluster with a large `shared_buffers` value or many connections.

The page gives two complete procedures:

* [Enable huge pages on a running cluster](#enable-huge-pages-on-a-running-cluster), if your cluster already runs without huge pages
* [Deploy a new cluster with huge pages](#deploy-a-new-cluster-with-huge-pages), if you are creating the cluster

Both procedures start after you [prepare the nodes](#before-you-start-prepare-the-nodes).

## Why to use huge pages

PostgreSQL keeps its data cache, `shared_buffers`, in one shared memory segment that every PostgreSQL process maps. Huge pages help in these ways:

* **Lower memory overhead per connection.** Each process keeps its own page table for the shared segment. With 4 KiB pages, an 8 GiB segment needs about 2 million entries per process, and with hundreds of connections the page tables alone can take gigabytes. With 2 MiB pages, the same segment needs 4096 entries.
* **Predictable memory.** The kernel reserves huge pages in advance and never swaps them out.
* **Less CPU time on address translation.** Fewer pages mean fewer misses in the CPU's translation cache. The gain depends on the workload and the hardware.

Huge pages cover only the main shared memory segment. Memory that each connection uses for queries, such as `work_mem`, stays in regular pages. Huge pages don't protect a Pod from being stopped for running out of memory.

## How huge pages work with Percona Operator for PostgreSQL

Huge pages need preparation on three levels:

1. The Linux worker nodes reserve a pool of huge pages.
2. Kubernetes exposes the pool as schedulable resources named `hugepages-2Mi` or `hugepages-1Gi`.
3. The Custom Resource requests huge pages for each PostgreSQL instance.

Kubernetes treats huge pages differently from CPU and memory:

* **No overcommit.** The `request` must equal the `limit`, and the scheduler places a Pod only on a node that has enough free huge pages. If no node has enough, the Pod stays `Pending`.
* **Counted separately from memory.** A Pod with `memory: 4Gi` and `hugepages-2Mi: 8530Mi` gets 4 GiB of regular memory plus 8530 MiB of huge pages.

When you request huge pages for an instance set, the Operator sets the PostgreSQL parameter `huge_pages` to `try` for the whole cluster and mounts a huge pages volume into the database container.

PostgreSQL requests its whole shared memory segment in one piece at startup. What happens depends on your huge pages request and on the `huge_pages` parameter:

| Situation | Result |
| --- | --- |
| No node has enough free huge pages for the Pod's request | The Pod stays `Pending`. See [Pods stay in the Pending state](#pods-stay-in-the-pending-state) |
| The Pod's request fits the free huge pages on a node and covers the shared memory segment | PostgreSQL places the shared memory in huge pages, and `huge_pages_status` shows `on` |
| The Pod's request fits the free huge pages on a node but is smaller than the shared memory segment, and `huge_pages` is `try`, the Operator default | PostgreSQL places the whole segment in regular memory and starts without a warning. The segment counts against the memory limit. If you sized that limit on the assumption that shared memory lives in huge pages, Kubernetes stops the database container with the `OOMKilled` reason when the data cache fills up |
| The Pod's request fits the free huge pages on a node but is smaller than the shared memory segment, and `huge_pages` is `"on"` | PostgreSQL doesn't start. The database container runs but never becomes ready. See [PostgreSQL doesn't start with `huge_pages` set to `on`](#postgresql-doesnt-start-with-huge_pages-set-to-on) |

So find out how many huge pages PostgreSQL needs **before** you request them. Both procedures on this page start with that step.

## Before you start: prepare the nodes

Before you follow either procedure, make sure that:

* Huge pages are reserved on every node that can run a PostgreSQL Pod, including nodes that host replicas and failover targets. Reserve them at boot time where possible. Each huge page needs physically contiguous memory, and on a node that has run for a while, memory becomes fragmented. A reservation made at runtime can then get fewer pages than you asked for, without an error. 1 GiB pages are the most affected. See the documentation for your platform:

  * [Kubernetes: manage huge pages :octicons-link-external-16:](https://kubernetes.io/docs/tasks/manage-hugepages/scheduling-hugepages/)
  * [Amazon EKS :octicons-link-external-16:](https://docs.aws.amazon.com/eks/latest/userguide/ml-hugepages.html)
  * [Google Kubernetes Engine :octicons-link-external-16:](https://cloud.google.com/kubernetes-engine/docs/how-to/node-system-config#pre-allocated-hugepages)
  * [Linux kernel: HugeTLB pages :octicons-link-external-16:](https://docs.kernel.org/admin-guide/mm/hugetlbpage.html)

* Kubernetes exposes the huge pages on those nodes. See [Check that nodes expose huge pages](#check-that-nodes-expose-huge-pages).
* Transparent Huge Pages are disabled on those nodes. See [Disable Transparent Huge Pages on the nodes](#disable-transparent-huge-pages-on-the-nodes).
* You know the PostgreSQL parameter values for your cluster. Without them, neither PostgreSQL nor the estimate can give you the right number of huge pages. See [Parameters that affect the size](#parameters-that-affect-the-size) for the parameters that matter.

Run the [node check](#check-that-nodes-expose-huge-pages) and note the huge page size and the free huge pages on each node that can run a PostgreSQL Pod. Both procedures use these values.

### Check that nodes expose huge pages

Run this check before either procedure, and again whenever you add nodes or change their huge pages. Reserving huge pages in the operating system doesn't guarantee that Kubernetes can schedule them. The kubelet reads the pool when it starts, so pages reserved later appear only after a kubelet restart.

1. List the huge pages each node can allocate:

    ```bash
    kubectl get nodes -o custom-columns='NODE:.metadata.name,HUGEPAGES_2MI:.status.allocatable.hugepages-2Mi,HUGEPAGES_1GI:.status.allocatable.hugepages-1Gi'
    ```

    ??? example "Sample output"

        ```{.text .no-copy}
        NODE     HUGEPAGES_2MI   HUGEPAGES_1GI
        node-1   0               0
        node-2   8800Mi          0
        ```

2. Check how many huge pages on a node are still free. Pods that already run on the node may have taken some of them:

    ```bash
    kubectl describe node <node-name> | grep -E '^(Capacity|Allocatable):|^Allocated resources:|^  Resource +Requests|^  hugepages-'
    ```

    ??? example "Sample output"

        ```{.text .no-copy}
        Capacity:
          hugepages-1Gi:      0
          hugepages-2Mi:      8800Mi
        Allocatable:
          hugepages-1Gi:      0
          hugepages-2Mi:      8800Mi
        Allocated resources:
          Resource           Requests          Limits
          hugepages-1Gi      0 (0%)            0 (0%)
          hugepages-2Mi      4594Mi (52%)      4594Mi (52%)
        ```

    `Capacity` is the pool the kubelet found on the node. `Allocatable` is the part that Pods can request. Under `Allocated resources`, the `Requests` column shows what Pods on the node already requested. The free huge pages are `Allocatable` minus that value. In the sample, 4206Mi is free, so a second PostgreSQL Pod that requests 4594Mi can't run on this node.

    To read only the capacity and allocatable values of a node, for example in a script, run:

    ```bash
    kubectl get node <node-name> -o jsonpath='{.status.capacity}{"\n"}{.status.allocatable}{"\n"}'
    ```

3. Check the pool and the default huge page size on the node itself. Note `Hugepagesize`: both procedures need it. This command starts a temporary debug Pod on the node:

    ```bash
    kubectl debug node/<node-name> -it --profile=general --image=busybox -- grep -i huge /proc/meminfo
    ```

    The first line of the output names the debug Pod: `Creating debugging pod <debug-pod-name> with container debugger on node <node-name>`. Note the name. You need it to delete the Pod in step 5. Because the command finishes quickly, `kubectl` can also print a warning that it couldn't attach to the Pod and falls back to its logs. The output still follows the warning.

    `kubectl debug node` needs permission to create Pods, and some clusters don't allow Pods that access the node. If the command fails with a permission or policy error, run `grep -i huge /proc/meminfo` directly on the node, for example over SSH, or ask your cluster administrator.

    ??? example "Sample output"

        ```{.text .no-copy}
        AnonHugePages:         0 kB
        ShmemHugePages:        0 kB
        FileHugePages:         0 kB
        HugePages_Total:    4400
        HugePages_Free:     4400
        HugePages_Rsvd:        0
        HugePages_Surp:        0
        Hugepagesize:       2048 kB
        Hugetlb:         9011200 kB
        ```

    `HugePages_Total` is the number of huge pages reserved on the node, in pages of the size shown in `Hugepagesize`. A value of `0` means the node has no huge pages reserved. `Hugepagesize` is the node's default huge page size.

    If `HugePages_Total` is greater than `0` but the commands in steps 1 and 2 still show `0` or a smaller value for the node, Kubernetes hasn't picked up the pool yet. Restart the kubelet on that node with your platform's procedure, for example `sudo systemctl restart kubelet` on a node you manage over SSH. Then run the commands in steps 1 and 2 again.

4. If you use 1 GiB pages, or the node has huge pages of more than one size, check each size. `/proc/meminfo` shows only the default size:

    ```bash
    kubectl debug node/<node-name> -it --profile=general --image=busybox -- sh -c 'for d in /sys/kernel/mm/hugepages/hugepages-*; do echo "$(basename $d): total $(cat $d/nr_hugepages), free $(cat $d/free_hugepages)"; done'
    ```

    ??? example "Sample output"

        ```{.text .no-copy}
        hugepages-1048576kB: total 0, free 0
        hugepages-2048kB: total 4400, free 4400
        ```

    `total` is the number of pages reserved for each size. `free` counts pages that no process uses yet, so it can stay high even when Pods have requested the pages. To see what Pods requested, use the `kubectl describe node` command in step 2.

5. Delete each debug Pod you created, using the name from its `Creating debugging pod` line. The Pods are in your current namespace:

    ```bash
    kubectl delete pod <debug-pod-name>
    ```

### Disable Transparent Huge Pages on the nodes

Transparent Huge Pages (THP) is a Linux kernel feature that merges regular pages into larger ones in the background. It can cause CPU spikes and latency jitter, and the [PostgreSQL documentation :octicons-link-external-16:](https://www.postgresql.org/docs/current/runtime-config-resource.html#GUC-HUGE-PAGES) advises against it. THP is separate from the huge pages you reserve for PostgreSQL, and disabling it doesn't affect them.

THP is a kernel setting of the worker node and applies to every Pod on it, so change it on dedicated PostgreSQL nodes only. Set it where you prepare the nodes, together with huge pages: in the node image, the boot configuration or the node configuration of your platform. A privileged DaemonSet can also change it at runtime, but the setting then applies only after the DaemonSet Pod runs on each node, so prefer the node configuration for production.

1. Check the current value on a node:

    ```bash
    kubectl debug node/<node-name> -it --profile=general --image=busybox -- cat /sys/kernel/mm/transparent_hugepage/enabled /sys/kernel/mm/transparent_hugepage/defrag
    ```

    ??? example "Sample output"

        ```{.text .no-copy}
        always [madvise] never
        always defer defer+madvise [madvise] never
        ```

    The value in square brackets is the active one. Delete the debug Pod afterwards, using the name from its `Creating debugging pod` line. If you can't run `kubectl debug node`, read the same files directly on the node.

2. Set `enabled` to `never` in the same node configuration where you reserve huge pages. Where the platform offers it, set `defrag` to `never` as well:

    | Platform | Where to set THP |
    | --- | --- |
    | Google Kubernetes Engine | `transparentHugepageEnabled: TRANSPARENT_HUGEPAGE_ENABLED_NEVER` and `transparentHugepageDefrag: TRANSPARENT_HUGEPAGE_DEFRAG_NEVER` in the same [node system configuration :octicons-link-external-16:](https://cloud.google.com/kubernetes-engine/docs/how-to/node-system-config#transparent_hugepages_thp) file that reserves huge pages |
    | Amazon EKS | `never` in the `transparent` settings of the same node class that reserves huge pages, or a user data script. See the [node class reference :octicons-link-external-16:](https://docs.aws.amazon.com/eks/latest/userguide/create-node-class.html) |
    | Azure Kubernetes Service | `transparentHugePageEnabled` and `transparentHugePageDefrag` in the [custom node configuration :octicons-link-external-16:](https://learn.microsoft.com/en-us/azure/aks/custom-node-configuration) |
    | Red Hat OpenShift | A Tuned profile with `transparent_hugepages=never`. See [Disabling Transparent Huge Pages :octicons-link-external-16:](https://docs.redhat.com/en/documentation/openshift_container_platform/4.15/html/scalability_and_performance/what-huge-pages-do-and-how-they-are-consumed#disable-thp_huge-pages) |
    | Other platforms | The kernel boot parameter `transparent_hugepage=never` in the node image or boot configuration. See [Transparent Hugepage Support :octicons-link-external-16:](https://docs.kernel.org/admin-guide/mm/transhuge.html) |

### Optional: dedicate the nodes to PostgreSQL

Do this if other workloads run on the huge pages nodes. Huge pages reserved on a node are not available as regular memory, and any Pod that requests huge pages can take them. Dedicating the nodes keeps the pages free for PostgreSQL. Do it before you follow either procedure, because adding tolerations or affinity later restarts the PostgreSQL Pods again.

1. Add a [taint :octicons-link-external-16:](https://kubernetes.io/docs/concepts/scheduling-eviction/taint-and-toleration/) to each node. The taint keeps off every new Pod that doesn't have a matching toleration:

    ```bash
    kubectl taint nodes <node-name> dedicated=postgres:NoSchedule
    ```

2. Add a label to each node. PostgreSQL Pods use it to select these nodes:

    ```bash
    kubectl label nodes <node-name> dedicated=postgres
    ```

3. Move other workloads that already run on these nodes to other nodes, for example with `kubectl drain <node-name> --ignore-daemonsets` followed by `kubectl uncordon <node-name>`. The taint doesn't evict Pods that are already running, and they keep their huge pages.

Both procedures show where to add the matching toleration and node affinity in the Custom Resource.

## Enable huge pages on a running cluster

Follow this procedure if your cluster already runs without huge pages. PostgreSQL 15 and later reports how much shared memory it needs, so you read the number from the cluster instead of calculating it yourself.

Before you start, [prepare and check the nodes](#before-you-start-prepare-the-nodes).

On PostgreSQL 14, which doesn't report the size, [estimate the size](#estimate-without-a-running-database) instead of steps 1 to 4. Take the parameter values from `patroni.dynamicConfiguration.postgresql.parameters` in your Custom Resource and the defaults from the [parameters table](#parameters-that-affect-the-size). Compare the result with the free huge pages on the nodes, then continue from step 5 of this procedure.

1. Find the primary Pod of your cluster:

    ```bash
    kubectl get pods -n <namespace> -l postgres-operator.crunchydata.com/cluster=<cluster-name>,postgres-operator.crunchydata.com/role=primary
    ```

2. Connect to PostgreSQL in the primary Pod:

    ```bash
    kubectl exec -it <primary-pod> -c database -n <namespace> -- psql
    ```

3. Read what PostgreSQL needs:

    ```sql
    SHOW shared_buffers;
    SHOW shared_memory_size;
    SHOW shared_memory_size_in_huge_pages;
    SHOW huge_page_size;
    SHOW huge_pages;
    ```

    On PostgreSQL 17 and later, also run `SHOW huge_pages_status;`. Then exit `psql` with `\q`.

    ??? example "Sample output"

        ```{.text .no-copy}
         shared_buffers
        ----------------
         735MB

         shared_memory_size
        --------------------
         787MB

         shared_memory_size_in_huge_pages
        ----------------------------------
         394

         huge_page_size
        ----------------
         0

         huge_pages
        ------------
         off
        ```

    The values mean the following:

    | Value | Meaning |
    | --- | --- |
    | `shared_buffers` | The data cache. Shared memory is always larger than this value |
    | `shared_memory_size` | The whole shared memory segment, in MB. This is the number you need |
    | `shared_memory_size_in_huge_pages` | The same size in huge pages of the size set by `huge_page_size`, or of the node's default size if `huge_page_size` is `0`. In the sample, 394 pages of 2 MiB |
    | `huge_page_size` | `0` means PostgreSQL uses the node's default huge page size, shown as `Hugepagesize` in [step 3 of the node check](#check-that-nodes-expose-huge-pages) |
    | `huge_pages` | `off` until you request huge pages, then `try` |
    | `huge_pages_status` | PostgreSQL 17 and later. `off` while the cluster runs without huge pages. After you finish this procedure, it must show `on` |

    PostgreSQL reports these values even while huge pages are off. They match the current configuration only. If you also plan to change a parameter from the [parameters table](#parameters-that-affect-the-size), change it first, wait for the cluster to restart, and read the values again.

4. Calculate the huge pages request:

    {% filter indent(4) %}{% include 'assets/fragments/huge-pages-calculate.txt' %}{% endfilter %}

5. Work out the new `memory` limit. In the setup without huge pages, the shared memory counts against the `memory` limit. With huge pages, it moves to the huge pages request, so lower the `memory` limit by the huge pages request. For example, if the instance set has `memory: 25Gi` and you request `hugepages-2Mi: 5Gi`, set `memory: 20Gi`. If the units differ, convert both values to `Mi` first: `1Gi` is `1024Mi`. For example, `memory: 10Gi` and `hugepages-2Mi: 4294Mi` give `memory: 5946Mi`. Keep enough regular memory for connections, `work_mem` and maintenance operations.

6. Edit the `deploy/cr.yaml` Custom Resource of your cluster. In each instance set, set the new `memory` limit and add the huge pages limit:

    ```yaml
    spec:
      instances:
        - name: instance1
          resources:
            limits:
              cpu: "2"
              memory: 20Gi
              hugepages-2Mi: 5Gi
    ```

    Kubernetes sets the request to the same value if you specify only the limit. Follow these rules:

    * Keep a `cpu` or `memory` limit together with the huge pages limit. Kubernetes rejects a huge pages limit without one of them, and the Operator reports the error only in its log.
    * If the cluster has several instance sets, request huge pages for every set. As soon as one set requests huge pages, the Operator mounts a huge pages volume into the Pods of all instance sets, and the Pods of a set without a huge pages limit can't start.
    * For 1 GiB pages, use the `hugepages-1Gi` key. If that isn't the node's default size, see [What else affects the result](#what-else-affects-the-result).

    If you [dedicated the nodes to PostgreSQL](#optional-dedicate-the-nodes-to-postgresql), add the toleration and node affinity to the same instance set:

    ```yaml
          tolerations:
            - key: dedicated
              operator: Equal
              value: postgres
              effect: NoSchedule
          affinity:
            nodeAffinity:
              requiredDuringSchedulingIgnoredDuringExecution:
                nodeSelectorTerms:
                  - matchExpressions:
                      - key: dedicated
                        operator: In
                        values:
                          - postgres
    ```

    If the instance set already has an `affinity` section, for example with Pod anti-affinity, add `nodeAffinity` to it. See [Binding Percona Distribution for PostgreSQL components to specific nodes](constraints.md) for more options.

7. Apply the Custom Resource:

    ```bash
    kubectl apply -f deploy/cr.yaml -n <namespace>
    ```

    The Operator recreates the PostgreSQL Pods one by one, replicas first, and then switches the primary role to an updated replica. PostgreSQL restarts on every Pod. A cluster with a single instance is unavailable while its Pod restarts.

8. Wait until the cluster is ready:

    ```bash
    kubectl get pg <cluster-name> -n <namespace>
    kubectl get pods -n <namespace> -l postgres-operator.crunchydata.com/cluster=<cluster-name>
    ```

    Right after you apply the change, the status can still show `ready` for a few seconds. It then changes to `initializing` while the Operator recreates the Pods, and back to `ready` when all Pods run with the new resources. Check that every PostgreSQL Pod has a recent `AGE`. Ignore backup Job Pods in the `Error` state that started before the restart. If a Pod stays `Pending`, see [Pods stay in the Pending state](#pods-stay-in-the-pending-state).

9. [Verify that PostgreSQL uses huge pages](#verify-that-postgresql-uses-huge-pages).

## Deploy a new cluster with huge pages

Follow this procedure if you are creating a cluster. No PostgreSQL runs yet that could report the size, so you deploy a small temporary cluster with the same settings that you intend to use for a production cluster, read the number from it, and delete it. You then configure and deploy your production cluster in one go, with the right huge pages request.

Before you start, [prepare and check the nodes](#before-you-start-prepare-the-nodes).

If you can't run a temporary cluster, [estimate the size](#estimate-without-a-running-database) instead, with the parameter values you plan to use and the defaults from the [parameters table](#parameters-that-affect-the-size). Compare the result with the free huge pages on the nodes, then continue from step 6 of this procedure.

1. Create the manifest of the temporary cluster, for example `hp-sizing.yaml`. Use the same image and PostgreSQL version as your production cluster, and set the PostgreSQL parameters from the [parameters table](#parameters-that-affect-the-size) and the extensions that you plan to use in production:

    ```yaml title="hp-sizing.yaml"
    apiVersion: pgv2.percona.com/v2
    kind: PerconaPGCluster
    metadata:
      name: hp-sizing
      finalizers:
        - percona.com/delete-pvc
        - percona.com/delete-ssl
    spec:
      crVersion: {{ release }}
      image: docker.io/percona/percona-distribution-postgresql:{{ postgresrecommended }}
      postgresVersion: 18
      instances:
        - name: instance1
          replicas: 1
          dataVolumeClaimSpec:
            accessModes:
              - ReadWriteOnce
            resources:
              requests:
                storage: 1Gi
      backups:
        enabled: false
      patroni:
        dynamicConfiguration:
          postgresql:
            parameters:
              shared_buffers: 4GB
              max_connections: 300
      extensions:
        pg_stat_monitor:
          enabled: true
    ```

    Replace the values under `parameters` and `extensions` with yours. The rest keeps the temporary cluster small and easy to remove:

    * One instance, no huge pages, no `memory` limit and no PgBouncer. The temporary cluster takes no queries, so it doesn't need memory for the whole `shared_buffers`.
    * Backups are disabled, so the temporary cluster doesn't create a backup repository or write to your backup storage.
    * The `percona.com/delete-pvc` and `percona.com/delete-ssl` finalizers make the Operator delete the cluster's volumes, user Secrets and TLS Secrets when you delete the cluster.

2. Deploy the temporary cluster and wait until it's ready:

    ```bash
    kubectl apply -f hp-sizing.yaml -n <namespace>
    kubectl wait pg/hp-sizing --for=jsonpath='{.status.state}'=ready --timeout=10m -n <namespace>
    ```

    The `kubectl wait` command returns `perconapgcluster.pgv2.percona.com/hp-sizing condition met` when the cluster is ready. It usually takes about a minute.

3. Connect to PostgreSQL Pod and read what it needs:

    ```bash
    kubectl get pods -n <namespace> 
    kubectl exec -it <pod-name> -c database -n <namespace> -- psql
    ```

    ```sql
    SHOW shared_memory_size;
    SHOW huge_page_size;
    ```

    `shared_memory_size` is the whole shared memory segment, in MB. `huge_page_size` `0` means PostgreSQL uses the node's default huge page size. Exit `psql` with `\q`. For more about these values, see step 3 of [Enable huge pages on a running cluster](#enable-huge-pages-on-a-running-cluster).

4. Calculate the huge pages request:

    {% filter indent(4) %}{% include 'assets/fragments/huge-pages-calculate.txt' %}{% endfilter %}

5. Delete the temporary cluster:

    ```bash
    kubectl delete pg hp-sizing -n <namespace>
    ```

    Check that nothing is left:

    ```bash
    kubectl get pvc,secret -n <namespace> -l postgres-operator.crunchydata.com/cluster=hp-sizing
    ```

    The command must return `No resources found`. If it lists anything, delete it with `kubectl delete pvc,secret -n <namespace> -l postgres-operator.crunchydata.com/cluster=hp-sizing`.

6. Configure the production cluster in the `deploy/cr.yaml` Custom Resource. Set the same image, PostgreSQL version, parameters and extensions as in `hp-sizing.yaml`, and add the huge pages request to each instance set. Size `memory` for everything except shared memory: connections, `work_mem`, maintenance operations and the other processes in the Pod.

    ```yaml
    spec:
      image: docker.io/percona/percona-distribution-postgresql:{{ postgresrecommended }}
      postgresVersion: 18
      instances:
        - name: instance1
          replicas: 3
          resources:
            limits:
              cpu: "2"
              memory: 4Gi
              hugepages-2Mi: 796Mi
      patroni:
        dynamicConfiguration:
          postgresql:
            parameters:
              shared_buffers: 4GB
              max_connections: 300
      extensions:
        pg_stat_monitor:
          enabled: true
    ```

    Follow these rules:

    * Keep a `cpu` or `memory` limit together with the huge pages limit. Kubernetes rejects a huge pages limit without one of them, and the Operator reports the error only in its log.
    * If the cluster has several instance sets, request huge pages for every set. The Pods of a set without a huge pages limit can't start.
    * For 1 GiB pages, use the `hugepages-1Gi` key. If that isn't the node's default size, see [What else affects the result](#what-else-affects-the-result).

    If you [dedicated the nodes to PostgreSQL](#optional-dedicate-the-nodes-to-postgresql), add the toleration and node affinity to the same instance set:

    ```yaml
          tolerations:
            - key: dedicated
              operator: Equal
              value: postgres
              effect: NoSchedule
          affinity:
            nodeAffinity:
              requiredDuringSchedulingIgnoredDuringExecution:
                nodeSelectorTerms:
                  - matchExpressions:
                      - key: dedicated
                        operator: In
                        values:
                          - postgres
    ```

    If the instance set already has an `affinity` section, for example with Pod anti-affinity, add `nodeAffinity` to it.

7. Deploy the production cluster and wait until it's ready:

    ```bash
    kubectl apply -f deploy/cr.yaml -n <namespace>
    kubectl wait pg/<cluster-name> --for=jsonpath='{.status.state}'=ready --timeout=15m -n <namespace>
    ```

    If the command times out and a Pod stays `Pending`, see [Pods stay in the Pending state](#pods-stay-in-the-pending-state).

8. [Verify that PostgreSQL uses huge pages](#verify-that-postgresql-uses-huge-pages).

## Verify that PostgreSQL uses huge pages

Run these checks at the end of both procedures, and after every change to the parameters or the huge pages request.

1. Connect to PostgreSQL in a database Pod:

    ```bash
    kubectl exec -it <pod-name> -c database -n <namespace> -- psql
    ```

2. Check the parameter:

    ```sql
    SHOW huge_pages;
    ```

    It shows `try`, or `on` if you set it.

3. On PostgreSQL 17 and later, check the actual status:

    ```sql
    SHOW huge_pages_status;
    ```

    It must show `on`. If it shows `off`, PostgreSQL runs without huge pages. See [PostgreSQL runs without huge pages and the Pod runs out of memory](#postgresql-runs-without-huge-pages-and-the-pod-runs-out-of-memory).

4. On PostgreSQL 15 and later, compare the size PostgreSQL needs with what you requested:

    ```sql
    SHOW shared_memory_size_in_huge_pages;
    ```

    The result must not exceed the number of pages in the Pod's huge pages limit.

5. On PostgreSQL 14 to 16, which don't have `huge_pages_status`, check the huge pages the Pod reserved. For 2 MiB pages on a node with cgroup v2, run:

    ```bash
    kubectl exec <pod-name> -c database -n <namespace> -- cat /sys/fs/cgroup/hugetlb.2MB.rsvd.current
    ```

    A value greater than `0` means PostgreSQL placed its shared memory in huge pages. For 1 GiB pages, read `hugetlb.1GB.rsvd.current`.

## Choose between `try` and `on`

The `huge_pages` parameter controls what PostgreSQL does when it can't get enough huge pages at startup. The Operator sets it to `try` when you request huge pages and to `off` when you don't. Keep `try` for most clusters.

| Value | Pros | Cons |
| --- | --- | --- |
| `try`, the Operator default | The cluster starts even when the huge pages request is too small | The fallback is silent. Shared memory then counts against the memory limit, and the database container can be stopped with the `OOMKilled` reason. [Verify](#verify-that-postgresql-uses-huge-pages) after every restart |
| `on` | A sizing mistake shows up at once as an instance that doesn't start | If you increase a parameter such as `max_connections` without increasing the huge pages request, the instances don't start after the restart |

For what each value does when the request is too small, see [How huge pages work with Percona Operator for PostgreSQL](#how-huge-pages-work-with-percona-operator-for-postgresql).

To set `on`, override the Operator default in the Custom Resource:

```yaml
spec:
  patroni:
    dynamicConfiguration:
      postgresql:
        parameters:
          huge_pages: "on"
```

Keep the quotes around `"on"`. Without them, YAML reads the value as the boolean `true`. The value applies to all instance sets in the cluster.

## Huge pages sizing reference

Both procedures read the size from PostgreSQL. This section explains what the size depends on, and how to estimate it when PostgreSQL can't report it.

### Parameters that affect the size

PostgreSQL's main shared memory segment is always larger than `shared_buffers`. It also holds WAL buffers, transaction status caches, lock tables and a record for every process slot. Requesting exactly `shared_buffers` is never enough.

These parameters change the size. Take each value from the parameters you set under `patroni.dynamicConfiguration.postgresql.parameters` in the Custom Resource. For a parameter you don't set, use the default from this table. Neither the Operator nor Patroni changes the PostgreSQL defaults of these parameters.

| Parameter | What it is | Default |
| --- | --- | --- |
| `shared_buffers` | The PostgreSQL data cache, the largest part of shared memory | `128MB` |
| `wal_buffers` | Memory for write-ahead log records that are not yet written to disk | `-1`, which means 1/32 of `shared_buffers`, at most 16 MiB |
| `max_connections` | Client connection slots | `100` |
| `max_worker_processes` | Slots for background workers, such as parallel query workers | `8` |
| `max_wal_senders` | Slots for replication connections | `10` |
| `max_prepared_transactions` | Slots for two-phase commit transactions | `0` |
| `autovacuum_max_workers` | Autovacuum worker slots on PostgreSQL 14 to 17 | `3` |
| `autovacuum_worker_slots` | Autovacuum worker slots on PostgreSQL 18 | `16` |
| `max_locks_per_transaction` | Lock table size per slot | `64` |
| `max_pred_locks_per_transaction` | Predicate lock table size per slot. PostgreSQL reserves it even if you don't use `SERIALIZABLE` transactions | `64` |
| `min_dynamic_shared_memory` | Dynamic shared memory that PostgreSQL reserves at startup | `0` |
| `shared_preload_libraries` | Extensions that PostgreSQL loads at startup. Some of them reserve shared memory | Depends on the extensions you enable |

Patroni enforces a minimum for some of these parameters: 25 for `max_connections`, 3 for `max_wal_senders`, 32 for `max_locks_per_transaction` and 2 for `max_worker_processes`. If you set a lower value, Patroni ignores it and uses the default from this table.

PostgreSQL reserves memory for every slot at startup, whether a process uses it or not. The size depends on the configured limits, not on the number of active connections.

### What else affects the result

* **Huge page size.** Request `hugepages-2Mi` or `hugepages-1Gi` to match the pages reserved on your nodes. If the requested size differs from the node's default, also set `huge_page_size` under `patroni.dynamicConfiguration.postgresql.parameters` to match, using `2MB` for 2 MiB pages or `1GB` for 1 GiB pages.
* **PostgreSQL version.** Each major version adds or resizes internal structures. Read or estimate the size again before you upgrade to a new major version.
* **Extensions.** Extensions in `shared_preload_libraries` can reserve their own shared memory. With its default settings, `pg_stat_monitor` adds about 280 MiB. The Operator enables it when you enable PMM with `pg_stat_monitor` as the query source, or when you enable it in the `extensions` section of the Custom Resource. `pgaudit`, which the Operator enables by default, doesn't add shared memory.
* **Every Pod.** Every PostgreSQL Pod in the cluster needs the same number of huge pages, so every node that can run one must have them free.
* **Parameter changes.** Read or estimate the size again before you change any parameter from the table. All of them need a PostgreSQL restart, so the new huge pages request takes effect together with the new value.

### Estimate without a running database

Use this method only if you can't read the size from PostgreSQL, for example on PostgreSQL 14, which doesn't report it. The result is an upper bound: it's never lower than what PostgreSQL requests. For `shared_buffers` of several gigabytes, it's about 1% higher. For small `shared_buffers` on PostgreSQL 17 and later, it can be 20% to 30% higher, because the estimate uses the largest possible size of the transaction status caches.

1. Count the process slots:

    ```{.text .no-copy}
    slots = max_connections + max_worker_processes + max_wal_senders
            + max_prepared_transactions + autovacuum slots
    ```

    Autovacuum slots depend on the PostgreSQL version:

    | PostgreSQL version | Autovacuum slots | Slots with all other parameters at their defaults |
    | --- | --- | --- |
    | 14, 15, 16 | `autovacuum_max_workers + 1` | `max_connections + 22` |
    | 17 | `autovacuum_max_workers + 2` | `max_connections + 23` |
    | 18 | `autovacuum_worker_slots + 2` | `max_connections + 36` |

2. Calculate the cost of one slot in bytes:

    ```{.text .no-copy}
    slot cost = 8192 + 420 × max_locks_per_transaction + 270 × max_pred_locks_per_transaction
    ```

    On PostgreSQL 18, add 34816 bytes for asynchronous I/O. With the default lock settings, one slot costs about 51 KiB on PostgreSQL 14 to 17 and about 85 KiB on PostgreSQL 18.

3. Add up the parts of shared memory:

    | Part | Estimate |
    | --- | --- |
    | Buffer pool | `shared_buffers` × 1.023 |
    | WAL buffers | `wal_buffers`. With the default, `shared_buffers` / 32, at most 16 MiB |
    | Transaction status caches | 34 MiB on PostgreSQL 17 and 18, 5 MiB on PostgreSQL 14 to 16 |
    | Process slots | slots × slot cost |
    | Fixed structures | 3 MiB |
    | Dynamic shared memory | `min_dynamic_shared_memory` |
    | Extensions | The shared memory of each extension in `shared_preload_libraries`. See [What else affects the result](#what-else-affects-the-result) |

    Convert the process slots part from bytes to MiB, dividing by 1048576, before you add up the parts. The buffer pool needs 2.3% more than `shared_buffers` because PostgreSQL also keeps a descriptor and a lookup entry for every 8 KiB buffer.

4. Add a margin of 1% to the total, at least 4 MiB.

5. Divide the result by the huge page size and round up to a whole page to get the number of pages.

6. Multiply the number of pages by the page size to get the value for the Custom Resource.

7. Return to the procedure you came from: step 5 of [Enable huge pages on a running cluster](#enable-huge-pages-on-a-running-cluster), or step 6 of [Deploy a new cluster with huge pages](#deploy-a-new-cluster-with-huge-pages). Compare the request with the free huge pages on the nodes first.

#### Example: PostgreSQL 17

!!! note

    This example only shows how the estimate works. It uses PostgreSQL 17 with specific parameter values. For your cluster, calculate the size with the steps in this section, using your PostgreSQL version and your parameter values, or read it from PostgreSQL as both procedures describe.

The example uses `shared_buffers` set to `8GB` and `max_connections` set to `200`. All other parameters have their default values, no preloaded extension reserves shared memory, and the nodes use 2 MiB huge pages.

| Step | Calculation | Result |
| --- | --- | --- |
| Process slots | 200 + 8 + 10 + 0 + 3 + 2 | 223 |
| Slot cost | 8192 + 420 × 64 + 270 × 64 | 52352 bytes |
| Buffer pool | 8192 MiB × 1.023 | 8380.4 MiB |
| WAL buffers | 8192 MiB / 32, at most 16 MiB | 16 MiB |
| Transaction status caches | PostgreSQL 17 | 34 MiB |
| Process slots | 223 × 52352 bytes | 11.1 MiB |
| Fixed structures | | 3 MiB |
| Total | | 8444.5 MiB |
| Total with 1% margin | 8444.5 × 1.01 | 8529 MiB |
| Huge pages | 8529 / 2, rounded up | 4265 |

The request is `hugepages-2Mi: 8530Mi`. For this configuration, PostgreSQL 17.5 and 17.11 report 4221 pages, so the estimate is 44 pages higher. A request equal to `shared_buffers`, `hugepages-2Mi: 8Gi`, gives only 4096 pages. That is 125 pages short, so PostgreSQL would run without huge pages.

## Troubleshooting

### Pods stay in the Pending state

**Symptom:** After you add or increase the huge pages limit, PostgreSQL Pods stay `Pending`. `kubectl describe pod <pod-name>` shows an event such as `Insufficient hugepages-2Mi`.

**Cause:** No node has enough free huge pages of the requested size.

**Fix:**

1. [Check that nodes expose huge pages](#check-that-nodes-expose-huge-pages) and compare the free huge pages on each node with your request.
2. Reserve more huge pages on the nodes, or add nodes with huge pages.
3. If other Pods use the huge pages on the nodes, [dedicate the nodes to PostgreSQL](#optional-dedicate-the-nodes-to-postgresql) and move those workloads to other nodes. The `NoSchedule` taint doesn't evict existing Pods or release their huge pages.
4. After you correct the request or the nodes, delete the `Pending` Pod:

    ```bash
    kubectl delete pod <pod-name> -n <namespace>
    ```

    The Operator doesn't replace a Pod that never started, so the Pod keeps the old request until you delete it.

### PostgreSQL runs without huge pages and the Pod runs out of memory

**Symptom:** `SHOW huge_pages_status;` returns `off`, or the database container restarts with the `OOMKilled` reason.

**Cause:** The huge pages limit is smaller than PostgreSQL's shared memory segment. With `huge_pages` set to `try`, PostgreSQL places the whole segment in regular memory, where it counts against the memory limit.

**Fix:**

1. Find out how many huge pages PostgreSQL needs with the current parameters. On PostgreSQL 15 and later, follow steps 1 to 4 of [Enable huge pages on a running cluster](#enable-huge-pages-on-a-running-cluster). On PostgreSQL 14, [estimate the size](#estimate-without-a-running-database).
2. Increase the huge pages limit in the Custom Resource and apply it.
3. [Verify that PostgreSQL uses huge pages](#verify-that-postgresql-uses-huge-pages).

### PostgreSQL doesn't start with `huge_pages` set to `on`

**Symptom:** The database container is running but not ready, and the cluster stays in the `initializing` state. `kubectl logs <pod-name> -c database -n <namespace>` shows `FATAL:  could not map anonymous shared memory: Cannot allocate memory`.

**Cause:** The huge pages limit is smaller than PostgreSQL's shared memory segment. The `HINT` line that follows the error shows the size PostgreSQL requested, in bytes.

**Fix:**

1. Divide the size from the `HINT` line by the huge page size in bytes and round up.
2. Increase the huge pages limit in the Custom Resource to at least that number of pages and apply it. Or remove `huge_pages: "on"` to fall back to `try`. See [Choose between `try` and `on`](#choose-between-try-and-on).

### PostgreSQL fails with a bus error

**Symptom:** PostgreSQL starts and then crashes with `Bus error` in the logs.

**Cause:** Container runtimes that predate the OCI Runtime Specification 1.1 limit the huge pages a container can use, but not the huge pages it can reserve. PostgreSQL's request for huge pages succeeds, and it crashes later when it touches pages beyond the limit.

**Fix:** Upgrade the container runtime on your nodes, or set `huge_pages` to `off` until you can. See [Huge pages and Postgres in containers :octicons-link-external-16:](https://www.crunchydata.com/blog/huge-pages-and-postgres-in-containers) for details.

For other issues, see [Initial troubleshooting](debug.md).

## Stop using huge pages

To stop using huge pages, remove the `hugepages-2Mi` or `hugepages-1Gi` keys from `spec.instances.resources.limits` for every instance set. Remove the matching keys from `spec.instances.resources.requests` if you set them explicitly, then apply the Custom Resource. If you set `huge_pages` to `on`, remove that parameter too.

Before you apply the change, increase the `memory` limit by the huge pages you remove, so it covers `shared_buffers` and the rest of shared memory. Without huge pages, shared memory counts against the memory limit.

The Operator sets `huge_pages` to `off` and recreates the PostgreSQL Pods with the new resources. If a PostgreSQL Pod is `Pending` because of its huge pages request, delete it after you apply the change. See [Pods stay in the Pending state](#pods-stay-in-the-pending-state).

## See also

* [Changing PostgreSQL options](options.md) to set `shared_buffers`, `max_connections` and other parameters that affect the huge pages size
* [Vertical scaling](scaling-vertical.md) to change CPU and memory resources for PostgreSQL Pods
* [Monitor the database with PMM](monitoring.md) to track memory use, and to see which query source enables `pg_stat_monitor`
* [Huge pages in the PostgreSQL documentation :octicons-link-external-16:](https://www.postgresql.org/docs/17/kernel-resources.html#LINUX-HUGE-PAGES) for how PostgreSQL uses huge pages on Linux
