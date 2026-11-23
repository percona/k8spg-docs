# Use huge pages with Percona Operator for PostgreSQL

Normally, memory is managed in 4 KiB chunks, also called "pages". When your PostgreSQL workload grows, the CPU has to juggle a lot of these small pages.

Huge pages are memory pages of 2 MiB or 1 GiB instead of the default 4 KiB. PostgreSQL can place its main shared memory segment in huge pages, which makes memory use more predictable and reduces CPU overhead on large instances.

This page explains why huge pages matter for PostgreSQL, how to calculate how many of them your cluster needs and how to request them for PostgreSQL managed by the Operator. Use huge pages when you plan a production cluster with a large `shared_buffers` value or many connections.

<!-- K8SPG-1179 review notes. Remove all HTML comments before merge.
     Labels: CODE = code-confirmed at Operator v3.1.0 or PostgreSQL source, CALC = calculation only,
     JOBIN = from Jobin's doc, pending his answers, LIVE = live-tested 2026-11-20 on GKE, Operator 3.1.0,
     PostgreSQL 14.24 to 18.6. Full report: Claude outputs/k8spg-1179-results/k8spg-1179-test-results.md. -->

## Why use huge pages

PostgreSQL keeps its data cache, `shared_buffers`, in one shared memory segment that every PostgreSQL process maps. Huge pages help in these ways:

* **Lower memory overhead per connection.** Each process keeps its own page table for the shared segment. With 4 KiB pages, an 8 GiB segment needs about 2 million entries per process, and with hundreds of connections the page tables alone can take gigabytes. With 2 MiB pages, the same segment needs 4096 entries.
* **Predictable memory.** The kernel reserves huge pages in advance and never swaps them out.
* **Less CPU time on address translation.** Fewer pages mean fewer misses in the CPU's translation cache. The gain depends on the workload and the hardware.

Huge pages cover only the main shared memory segment. Memory that each connection uses for queries, such as `work_mem`, stays in regular pages. Huge pages don't protect a Pod from being stopped for running out of memory.

## How huge pages work in Kubernetes

Huge pages need preparation on three levels:

1. The Linux worker nodes reserve a pool of huge pages.
2. Kubernetes exposes the pool as schedulable resources named `hugepages-2Mi` or `hugepages-1Gi`.
3. The Custom Resource requests huge pages for each PostgreSQL instance.

Kubernetes treats huge pages differently from CPU and memory:

* **No overcommit.** The `request` must equal the `limit`, and the scheduler places a Pod only on a node that has enough free huge pages. If no node has enough, the Pod stays `Pending`.
* **Counted separately from memory.** A Pod with `memory: 4Gi` and `hugepages-2Mi: 8530Mi` gets 4 GiB of regular memory plus 8530 MiB of huge pages.
* **Hard to correct.** Changing the request recreates the Pods one by one, replicas first, and then switches the primary role to an updated replica. PostgreSQL restarts on every Pod. A cluster with a single instance is unavailable while its Pod restarts.

The number you request must cover PostgreSQL's whole shared memory segment. PostgreSQL requests the segment in one piece at startup. If the Pod has fewer huge pages than the segment needs, PostgreSQL places the whole segment in regular memory instead. The Pod keeps running, but the shared memory now counts against the Pod's memory limit. If you sized that limit on the assumption that shared memory lives in huge pages, Kubernetes stops the database container with the `OOMKilled` reason as soon as the data cache fills up.

So calculate the huge pages requirement **before** you create or restart the cluster.

## Before you start

Make sure that:

* Huge pages are reserved on every node that can run a PostgreSQL Pod, including nodes that host replicas and failover targets. Reserve them at boot time where possible: 1 GiB pages in particular can fail to allocate at runtime on a node with fragmented memory. See the documentation for your platform:

    * [Kubernetes: manage huge pages :octicons-link-external-16:](https://kubernetes.io/docs/tasks/manage-hugepages/scheduling-hugepages/)
    * [Amazon EKS :octicons-link-external-16:](https://docs.aws.amazon.com/eks/latest/userguide/ml-hugepages.html)
    * [Google Kubernetes Engine :octicons-link-external-16:](https://cloud.google.com/kubernetes-engine/docs/how-to/node-system-config#pre-allocated-hugepages)
    * [Linux kernel: HugeTLB pages :octicons-link-external-16:](https://docs.kernel.org/admin-guide/mm/hugetlbpage.html)

* Transparent Huge Pages are disabled on those nodes. See [Disable Transparent Huge Pages on the nodes](#disable-transparent-huge-pages-on-the-nodes).
* The nodes for PostgreSQL are tainted and labeled so that other workloads can't use their huge pages. See [Dedicate the nodes to PostgreSQL](#dedicate-the-nodes-to-postgresql).
* You know the PostgreSQL parameter values for your cluster. You need them to [calculate how many huge pages you need](#calculate-how-many-huge-pages-you-need).

### Check that nodes expose huge pages

Reserving huge pages in the operating system doesn't guarantee that Kubernetes can schedule them. The kubelet reads the pool when it starts, so pages reserved later appear only after a kubelet restart.

1. List the huge pages each node can allocate:

    ```bash
    kubectl get nodes -o custom-columns='NODE:.metadata.name,HUGEPAGES_2MI:.status.allocatable.hugepages-2Mi,HUGEPAGES_1GI:.status.allocatable.hugepages-1Gi'
    ```

    ??? example "Sample output"

        ```{.text .no-copy}
        NODE     HUGEPAGES_2MI   HUGEPAGES_1GI
        node-1   0               0
        node-2   8600Mi          0
        ```

2. If a node shows `0` although you reserved huge pages, check the pool on the node itself. This command starts a temporary debug Pod on the node:

    ```bash
    kubectl debug node/<node-name> -it --profile=general --image=busybox -- grep -i huge /proc/meminfo
    ```

    Because the command finishes quickly, `kubectl` can print a warning that it couldn't attach to the Pod and falls back to its logs. The output still follows the warning.

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

    `HugePages_Total` is the pool size in pages of the default size, `Hugepagesize`. A value of `0` means the node has no huge pages reserved. If the pool is there but `allocatable` shows `0`, restart the kubelet on that node.

3. Delete the debug Pod. Its name starts with `node-debugger-` followed by the node name:

    ```bash
    kubectl get pods -o name | grep node-debugger
    kubectl delete pod <pod-name>
    ```


### Disable Transparent Huge Pages on the nodes

Transparent Huge Pages (THP) is a Linux kernel feature that merges regular pages into larger ones in the background. It can cause CPU spikes and latency jitter, and the [PostgreSQL documentation :octicons-link-external-16:](https://www.postgresql.org/docs/current/runtime-config-resource.html#GUC-HUGE-PAGES) advises against it. THP is separate from the huge pages you reserve for PostgreSQL, and disabling it doesn't affect them.

THP is a kernel setting of the worker node, so a Pod can't change it. Set it where you prepare the nodes, together with huge pages. The setting applies to every Pod on the node, so change it on dedicated PostgreSQL nodes only.

1. Check the current value on a node:

    ```bash
    kubectl debug node/<node-name> -it --profile=general --image=busybox -- cat /sys/kernel/mm/transparent_hugepage/enabled /sys/kernel/mm/transparent_hugepage/defrag
    ```

    ??? example "Sample output"

        ```{.text .no-copy}
        always [madvise] never
        always defer defer+madvise [madvise] never
        ```

    The value in square brackets is the active one. Delete the debug Pod afterwards, as in [Check that nodes expose huge pages](#check-that-nodes-expose-huge-pages).

2. Set `enabled` to `never` in the node configuration of your platform. Where the platform offers it, set `defrag` to `never` as well:

    | Platform | Where to set THP |
    |---|---|
    | Google Kubernetes Engine | `transparentHugepageEnabled: TRANSPARENT_HUGEPAGE_ENABLED_NEVER` and `transparentHugepageDefrag: TRANSPARENT_HUGEPAGE_DEFRAG_NEVER` in the [node system configuration :octicons-link-external-16:](https://cloud.google.com/kubernetes-engine/docs/how-to/node-system-config#transparent_hugepages_thp) |
    | Amazon EKS | `never` in the `transparent` settings of the node class, or a user data script. See [Configure hugepages in Amazon EKS clusters :octicons-link-external-16:](https://docs.aws.amazon.com/eks/latest/userguide/ml-hugepages.html) and the [node class reference :octicons-link-external-16:](https://docs.aws.amazon.com/eks/latest/userguide/create-node-class.html) |
    | Azure Kubernetes Service | `transparentHugePageEnabled` and `transparentHugePageDefrag` in the [custom node configuration :octicons-link-external-16:](https://learn.microsoft.com/en-us/azure/aks/custom-node-configuration) |
    | Red Hat OpenShift | A Tuned profile with `transparent_hugepages=never`. See [Disabling Transparent Huge Pages :octicons-link-external-16:](https://docs.redhat.com/en/documentation/openshift_container_platform/4.15/html/scalability_and_performance/what-huge-pages-do-and-how-they-are-consumed#disable-thp_huge-pages) |
    | Other platforms | The kernel boot parameter `transparent_hugepage=never` in the node image or boot configuration. See [Transparent Hugepage Support :octicons-link-external-16:](https://docs.kernel.org/admin-guide/mm/transhuge.html) |

<!-- Platform options checked against provider docs 2026-11-19: GKE LinuxNodeConfig enums include TRANSPARENT_HUGEPAGE_ENABLED_NEVER and _DEFRAG_NEVER; AKS LinuxOSConfig allows never for both; EKS page shows Auto Mode advancedCompute.hugepages.transparent and Karpenter userData, no never example; OpenShift Tuned profile [vm] transparent_hugepages=never. LIVE: GKE row gives [never] for both values; check command and sample output confirmed. EKS, AKS, OpenShift, kernel rows: links checked only.
     Kernel boot parameter transparent_hugepage= sets enabled only, hence the wording of step 2. -->

### Dedicate the nodes to PostgreSQL

Huge pages reserved on a node are not available as regular memory, and any Pod that requests huge pages can take them. Dedicate the huge pages nodes to PostgreSQL before you create the cluster, so the pages are free when the PostgreSQL Pods start.

1. Add a [taint :octicons-link-external-16:](https://kubernetes.io/docs/concepts/scheduling-eviction/taint-and-toleration/) to each node. The taint keeps off every Pod that doesn't have a matching toleration:

    ```bash
    kubectl taint nodes <node-name> dedicated=postgres:NoSchedule
    ```

2. Add a label to each node. PostgreSQL Pods use it to select these nodes:

    ```bash
    kubectl label nodes <node-name> dedicated=postgres
    ```

You add the matching toleration and node affinity to the Custom Resource when you [request huge pages](#request-huge-pages-in-the-custom-resource).

<!-- LIVE: taint keeps off Pods without a toleration; toleration alone lets Pods land on other nodes; toleration + nodeAffinity keeps them on the dedicated nodes. -->

## Calculate how many huge pages you need

PostgreSQL's main shared memory segment is always larger than `shared_buffers`. It also holds WAL buffers, transaction status caches, lock tables and a record for every process slot. Requesting exactly `shared_buffers` is never enough.

You can estimate the segment size from the PostgreSQL parameters in your Custom Resource, without starting a database. The method in this section gives an upper bound: the result is never lower than what PostgreSQL requests. For `shared_buffers` of several gigabytes, it's about 1% higher. For small `shared_buffers` on PostgreSQL 17 and later, it can be 20% to 30% higher, because the estimate uses the largest possible size of the transaction status caches. If the cluster already runs, [read the size from it](#read-the-size-from-a-running-cluster) to get the exact value. For the exact formula and how it was derived, see [Pre-calculate huge pages for PostgreSQL :octicons-link-external-16:](https://www.percona.com/blog/TODO-huge-pages-post).

<!-- TODO: replace the link when Jobin's post is published.
     CALC: upper-bound method checked against Jobin's exact formula on 9000 random configurations for PostgreSQL 16, 17 and 18.
     Never below the exact value, 0.3% above on average, at most 3.6% above for shared_buffers over 2 GB. JOBIN: method sent to him for confirmation.
     LIVE: never below PostgreSQL in 16 of 16 configuration and version pairs (15 to 18). +1.0% to +1.1% for 8 GB, up to +28% for defaults on 17 and 18. PostgreSQL 15 and 16 give identical sizes. -->

### Parameters that affect the size

Take each value from the parameters you set under `patroni.dynamicConfiguration.postgresql.parameters` in the Custom Resource. For a parameter you don't set, use the default from this table. Neither the Operator nor Patroni changes the PostgreSQL defaults of these parameters.

| Parameter | What it is | Default |
|---|---|---|
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

<!-- CODE: the Operator sets only wal_level, jit, password_encryption and huge_pages as defaults (v3.1.0 internal/postgres/parameters.go, huge_pages.go).
     CODE: defaults checked in PostgreSQL postgresql.conf.sample, REL_14, REL_17, REL_18. shared_buffers: built-in default is 128MB on 17 and 18, 8MB on 14; initdb writes 128MB to postgresql.conf, Patroni keeps it as postgresql.base.conf. LIVE: all defaults in the table confirmed on 14 to 18, including shared_buffers 128MB on 14.
     CODE: Patroni CMDLINE_OPTIONS (v3.0.0, v3.3.0, v4.0.0, master) passes max_connections 100, max_wal_senders 10, max_prepared_transactions 0, max_locks_per_transaction 64, max_worker_processes 8, same as PostgreSQL. Minimums 25, 3, 0, 32, 2: a lower value fails validation and Patroni uses its default instead (patroni/config.py _process_postgresql_parameters). LIVE: Patroni 4.1.5 in the 3.1.0 images; max_connections 20 results in 100, with a warning in the Patroni log only. -->

### Estimate the shared memory size

1. Count the process slots:

    ```{.text .no-copy}
    slots = max_connections + max_worker_processes + max_wal_senders
            + max_prepared_transactions + autovacuum slots
    ```

    Autovacuum slots depend on the PostgreSQL version:

    | PostgreSQL version | Autovacuum slots | Slots with all other parameters at their defaults |
    |---|---|---|
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
    |---|---|
    | Buffer pool | `shared_buffers` × 1.023 |
    | WAL buffers | `wal_buffers`. With the default, `shared_buffers` / 32, at most 16 MiB |
    | Transaction status caches | 34 MiB on PostgreSQL 17 and 18, 5 MiB on PostgreSQL 14 to 16 |
    | Process slots | slots × slot cost |
    | Fixed structures | 3 MiB |
    | Dynamic shared memory | `min_dynamic_shared_memory` |
    | Extensions | The shared memory of each extension in `shared_preload_libraries`. See [What else affects the result](#what-else-affects-the-result) |

    Convert the process slots part from bytes to MiB, dividing by 1048576, before you add up the parts. The buffer pool needs 2.3% more than `shared_buffers` because PostgreSQL also keeps a descriptor and a lookup entry for every 8 KiB buffer.

4. Add a margin of 1% to the total, at least 4 MiB. The margin covers small differences between PostgreSQL minor versions.

5. Divide the result by the huge page size and round up to a whole page to get the number of pages.

6. Multiply the number of pages by the page size to get the value for the Custom Resource.

<!-- CALC/JOBIN: per-slot constants, 34 MiB and 5 MiB caps, 3 MiB fixed part and 1.023 derived from Jobin's formula. 1% margin is Jobin's recommendation. -->

### Example: PostgreSQL 17

This example estimates huge pages for PostgreSQL 17 with `shared_buffers` set to `8GB` and `max_connections` set to `200`. All other parameters have their default values, no preloaded extension reserves shared memory, and the nodes use 2 MiB huge pages.

| Step | Calculation | Result |
|---|---|---|
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

Request `hugepages-2Mi: 8530Mi`. For this configuration, PostgreSQL 17.5 and 17.11 request 4221 pages.

A request equal to `shared_buffers`, `hugepages-2Mi: 8Gi`, gives only 4096 pages. That is 125 pages short, so PostgreSQL would run without huge pages.

<!-- LIVE: every number in the table confirmed; 17.11 requests 4221 pages; 8Gi request gives huge_pages_status off. JOBIN: 4221 on 17.5. -->

### Read the size from a running cluster

If the cluster already runs PostgreSQL 15 or later, PostgreSQL reports its shared memory size for the current configuration. It does so even while huge pages are off.

1. Find the primary Pod:

    ```bash
    kubectl get pods -n <namespace> -l postgres-operator.crunchydata.com/cluster=<cluster-name>,postgres-operator.crunchydata.com/role=primary
    ```

2. Connect to PostgreSQL in the primary Pod:

    ```bash
    kubectl exec -it <primary-pod> -c database -n <namespace> -- psql
    ```

3. Read the shared memory size in MiB:

    ```sql
    SHOW shared_memory_size;
    ```

4. Add the 1% margin, at least 4 MiB, divide by the huge page size in MiB and round up.

The value matches the current configuration only. If you plan to change any parameter from the [parameters table](#parameters-that-affect-the-size), estimate again with the new values.

`SHOW shared_memory_size_in_huge_pages;` returns the result in pages directly, but for the node's default huge page size. Use it only if that is the size you plan to request.

<!-- CODE: PostgreSQL REL_15 to REL_18 ipci.c sets shared_memory_size and shared_memory_size_in_huge_pages at startup regardless of huge_pages=off. In-pages value = size / page size + 1, page size from /proc/meminfo Hugepagesize or huge_page_size. LIVE: values returned on 15 to 18 with huge_pages off; no shared_memory_size on 14. -->

### What else affects the result

* **Huge page size.** Request `hugepages-2Mi` or `hugepages-1Gi` to match
  the pages reserved on your nodes. If the requested size differs from
  the node's default, also set `huge_page_size` under
  `patroni.dynamicConfiguration.postgresql.parameters` to match, using
  `2MB` for 2 MiB pages or `1GB` for 1 GiB pages. With 1 GiB pages, the
  example needs nine pages, so request `hugepages-1Gi: 9Gi`.
* **PostgreSQL version.** Each major version adds or resizes internal structures. Estimate again before you upgrade to a new major version.
* **Extensions.** Extensions in `shared_preload_libraries` can reserve their own shared memory. With its default settings, `pg_stat_monitor` adds about 280 MiB. The Operator enables it when you enable PMM with `pg_stat_monitor` as the query source, or when you enable it in the `extensions` section of the Custom Resource. `pgaudit`, which the Operator enables by default, doesn't add shared memory.
* **Every Pod.** Every PostgreSQL Pod in the cluster needs the same number of huge pages, so every node that can run one must have them free.
* **Parameter changes.** Estimate again before you change any parameter from the table. All of them need a PostgreSQL restart, so the new huge pages request takes effect together with the new value.

<!-- CODE: pg_stat_monitor enabled when PMM querySource = pg_stat_monitor (v3.1.0 perconapgcluster_types.go). pg_stat_monitor reserves pgsm_max 256 MB + pgsm_query_shared_buffer 20 MB (pg_stat_monitor main, hash_query.c). LIVE on 17.11: pg_stat_monitor +278.1 MiB (139 pages), pgaudit 0. JOBIN: pg_tde and pg_cron overhead not measured. -->

## Request huge pages in the Custom Resource

Set the huge pages limit for each instance set in `spec.instances.resources.limits`. Kubernetes sets the request to the same value if you specify only the limit.

1. Edit the `deploy/cr.yaml` Custom Resource. This example uses the values from the [PostgreSQL 17 example](#example-postgresql-17):

    ```yaml
    spec:
      postgresVersion: 17
      instances:
        - name: instance1
          replicas: 3
          resources:
            limits:
              cpu: "2"
              memory: 4Gi
              hugepages-2Mi: 8530Mi
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
      patroni:
        dynamicConfiguration:
          postgresql:
            parameters:
              shared_buffers: 8GB
              max_connections: 200
    ```

    Size `memory` for everything except shared memory: connection memory
    such as `work_mem`, maintenance operations and the other processes in
    the Pod. For 1 GiB pages, replace `hugepages-2Mi: 8530Mi` with
    `hugepages-1Gi: 9Gi` and configure the matching `huge_page_size` as
    described in [What else affects the result](#what-else-affects-the-result).

    Set a `cpu` or `memory` limit together with the huge pages limit. Kubernetes rejects a huge pages limit without one of them, and the Operator reports the error only in its log.

    If the cluster has several instance sets, request huge pages for every set. As soon as one set requests huge pages, the Operator mounts a huge pages volume into the Pods of all instance sets, and the Pods of a set without a huge pages limit can't start.

    The toleration lets the Pods run on the nodes you [dedicated to PostgreSQL](#dedicate-the-nodes-to-postgresql), and the node affinity keeps them there. If you didn't dedicate nodes, omit both. If your instance set already has an `affinity` section, for example with Pod anti-affinity, add `nodeAffinity` to it. See [Binding Percona Distribution for PostgreSQL components to specific nodes](constraints.md) for more affinity and toleration options.

2. Apply the configuration:

    ```bash
    kubectl apply -f deploy/cr.yaml -n <namespace>
    ```

    The Operator recreates the PostgreSQL Pods with the new resources, replicas first. When any instance set has a huge pages limit greater than zero, the Operator sets `huge_pages` to `try` for the cluster and mounts a huge pages volume into the database container.

If no node has enough free huge pages, the Pods stay `Pending`. See [Troubleshooting](#troubleshooting).

<!-- CODE: internal/postgres/huge_pages.go, internal/postgres/reconcile.go (v3.1.0). spec.instances[].tolerations and .affinity exist in v3.1.0 perconapgcluster_types.go; changing tolerations restarts PostgreSQL. Example combines Chetan's and Jobin's examples.
     LIVE: example applies as written, Pods land on dedicated nodes, request equals limit, huge_pages try, volume mounted. Rollout: replicas recreated first, then switchover, then former primary, about 3 min 20 s for 3 Pods.
     LIVE: huge pages limit without cpu or memory rejected: "Forbidden: HugePages require cpu or memory", only in the Operator log, CR reports configured.
     LIVE + CODE: reconcile.go adds the hugepage volume for every instance set when any set requests huge pages (HugePages2MiRequested(inCluster)); a set without a limit fails MountVolume.SetUp, Init:0/4, with try and on. Engineering issue, not filed. -->

## Choose between `try` and `on`

The `huge_pages` parameter controls what PostgreSQL does when it can't get enough huge pages at startup. The Operator sets it to `try` when you request huge pages and to `off` when you don't.

| Value | Behavior | Pros | Cons |
|---|---|---|---|
| `try`, the Operator default | PostgreSQL uses huge pages if it can get them all. Otherwise it places shared memory in regular pages and starts anyway | The cluster starts even when a node is short of huge pages, which is safer during rollout and on mixed nodes | The fallback is silent. Shared memory then counts against the memory limit, and the database container can be stopped with the `OOMKilled` reason. You need to check the status after every restart |
| `on` | PostgreSQL starts only if it gets all the huge pages it needs | A sizing mistake shows up at once as an instance that doesn't start | A replica or failover target on a node without enough free huge pages doesn't start. If you increase a parameter such as `max_connections` without increasing the huge pages limit, the instances don't start after the restart |

Use `try` while you validate your sizing. Consider `on` for production once you calculate the huge pages limit every time you change a parameter.

To set `on`, override the Operator default in the Custom Resource:

```yaml
spec:
  patroni:
    dynamicConfiguration:
      postgresql:
        parameters:
          huge_pages: "on"
```

Keep the quotes around `"on"`. Without them, YAML reads the value as the boolean `true`.

The value applies to all instance sets in the cluster. Every instance set must request huge pages, as described in [Request huge pages in the Custom Resource](#request-huge-pages-in-the-custom-resource).

<!-- CODE: huge_pages is a Default parameter, user parameters override it (internal/patroni/config.go). Cluster-wide: HugePagesRequested checks all instance sets. JOBIN: recommendation on try vs on pending.
     LIVE: try with too few pages gives huge_pages_status off, no log line, then OOMKilled under 4Gi. on with too few pages: container running but not ready, start failed, FATAL could not map anonymous shared memory. Unquoted on stored as boolean true.
     CODE, not tested: restore always runs with try (pgbackrest.go 1404-1413), overriding on; restore Job has no huge pages. Held for developers, not documented. -->

## Verify huge pages are in use

1. Connect to PostgreSQL in a database Pod:

    ```bash
    kubectl exec -it <pod-name> -c database -n <namespace> -- psql
    ```

2. Check the parameter and, on PostgreSQL 17 and later, the actual status:

    ```sql
    SHOW huge_pages;
    SHOW huge_pages_status;
    ```

    `huge_pages` shows `try` or `on`. `huge_pages_status` must show `on`. If it shows `off`, PostgreSQL runs without huge pages. See [Troubleshooting](#troubleshooting).

3. Compare the size PostgreSQL needs with what you requested:

    ```sql
    SHOW shared_memory_size_in_huge_pages;
    ```

    The result must not exceed the number of pages in the Pod's huge pages limit.

4. On PostgreSQL 14 to 16, which don't have `huge_pages_status`, check the huge pages usage of the Pod. For 2 MiB pages on a node with cgroup v2, run:

    ```bash
    kubectl exec <pod-name> -c database -n <namespace> -- cat /sys/fs/cgroup/hugetlb.2MB.current
    ```

    A value greater than `0` means the Pod uses huge pages. The value grows as PostgreSQL fills its data cache. To see the whole reserved segment at once, read `hugetlb.2MB.rsvd.current` instead. It equals `shared_memory_size_in_huge_pages` × 2 MiB. For 1 GiB pages, read the `hugetlb.1GB.*` files.

<!-- CODE: huge_pages_status exists in PostgreSQL 17+ (REL_17 ipci.c). LIVE: huge_pages_status on (17), not on 16; cgroup v2 path works; current 52428800 and rsvd.current 1126170624 (537 pages) on 16; 0 with the try fallback. cgroup v1 not tested.
     The previous version suggested /proc/meminfo inside the container. It shows the node-wide pool, not the Pod's usage, so it moved to node checks. -->

## Troubleshooting

### Pods stay in the Pending state

**Symptom:** After you add or increase the huge pages limit, PostgreSQL Pods stay `Pending`. `kubectl describe pod <pod-name>` shows an event such as `Insufficient hugepages-2Mi`.

**Cause:** No node has enough free huge pages of the requested size.

**Fix:**

1. [Check that nodes expose huge pages](#check-that-nodes-expose-huge-pages) and compare their `allocatable` value with your request.
2. Reserve more huge pages on the nodes, or add nodes with huge pages.
3. If other Pods use the huge pages on the nodes,
   [dedicate the nodes to PostgreSQL](#dedicate-the-nodes-to-postgresql)
   and move those workloads to other nodes. The `NoSchedule` taint does
   not evict existing Pods or release their huge pages allocations.
4. After you correct the request or the nodes, delete the `Pending` Pod:

    ```bash
    kubectl delete pod <pod-name> -n <namespace>
    ```

    The Operator doesn't replace a Pod that never started, so the Pod keeps the old request until you delete it.

<!-- LIVE: event "0/7 nodes are available: 3 Insufficient hugepages-2Mi, ..."; Pending Pod kept the old spec for 9+ minutes (StatefulSet OnDelete) until deleted. Engineering issue, not filed. -->

### PostgreSQL runs without huge pages and the Pod runs out of memory

**Symptom:** `SHOW huge_pages_status;` returns `off`, or the database container restarts with the `OOMKilled` reason.

**Cause:** The huge pages limit is smaller than PostgreSQL's shared memory segment. With `huge_pages` set to `try`, PostgreSQL places the whole segment in regular memory, where it counts against the memory limit.

**Fix:**

1. On PostgreSQL 15 and later, run `SHOW shared_memory_size;` and
   [calculate the huge pages](#calculate-how-many-huge-pages-you-need) again with
   the current parameters. On PostgreSQL 14, use the estimate from that section
   with the current parameter values.
2. Increase the huge pages limit in the Custom Resource and apply it.
3. If you changed a parameter such as `max_connections` or `shared_buffers` recently, include the new value in the calculation.

### PostgreSQL doesn't start with `huge_pages` set to `on`

**Symptom:** The database container is running but not ready, and the cluster stays in the `initializing` state. `kubectl logs <pod-name> -c database -n <namespace>` shows `FATAL:  could not map anonymous shared memory: Cannot allocate memory`.

**Cause:** The huge pages limit is smaller than PostgreSQL's shared memory segment. The `HINT` line that follows the error shows the size PostgreSQL requested, in bytes.

**Fix:**

1. Divide the size from the `HINT` line by the huge page size in bytes and round up.
2. Increase the huge pages limit in the Custom Resource to at least that number of pages and apply it. Or remove `huge_pages: "on"` to fall back to `try`. See [Choose between `try` and `on`](#choose-between-try-and-on) for pros and cons of using either option.

### PostgreSQL fails with a bus error

**Symptom:** PostgreSQL starts and then crashes with `Bus error` in the logs.

**Cause:** Container runtimes that predate the OCI Runtime Specification 1.1 limit the huge pages a container can use, but not the huge pages it can reserve. PostgreSQL's request for huge pages succeeds, and it crashes later when it touches pages beyond the limit.

**Fix:** Upgrade the container runtime on your nodes, or set `huge_pages` to `off` until you can. See [Huge pages and Postgres in containers :octicons-link-external-16:](https://www.crunchydata.com/blog/huge-pages-and-postgres-in-containers) for details.

<!-- JOBIN: Bus error from Jobin's doc and the Crunchy Data post (OCI Runtime Spec 1.1, July 2023). Not reproduced: containerd 2.2.7 sets hugetlb.2MB.rsvd.max to the limit. -->

For other issues, see [Initial troubleshooting](debug.md).

## Stop using huge pages

To stop using huge pages, remove the `hugepages-2Mi` or `hugepages-1Gi` keys from
`spec.instances.resources.limits` for every instance set. Remove the matching
keys from `spec.instances.resources.requests` if you set them explicitly, then
apply the Custom Resource. If you set `huge_pages` to `on`, remove that parameter
too.

Before you apply the change, increase the `memory` limit so it covers `shared_buffers` and the rest of shared memory. Without huge pages, shared memory counts against the memory limit.

The Operator sets `huge_pages` to `off` and recreates the PostgreSQL Pods with the new resources. If a PostgreSQL Pod is `Pending` because of its huge pages request, delete it after you apply the change. See [Pods stay in the Pending state](#pods-stay-in-the-pending-state).

<!-- CODE + LIVE: huge_pages off, no huge pages volume, PostgreSQL starts. Memory advice is new, not in Chetan's doc. -->

## See also

* [Changing PostgreSQL options](options.md) to set `shared_buffers`, `max_connections` and other parameters that affect the huge pages calculation
* [Vertical scaling](scaling-vertical.md) to change CPU and memory resources for PostgreSQL Pods
* [Monitor the database with PMM](monitoring.md) to track memory use, and to see which query source enables `pg_stat_monitor`
* [Huge pages in the PostgreSQL documentation :octicons-link-external-16:](https://www.postgresql.org/docs/17/kernel-resources.html#LINUX-HUGE-PAGES) for how PostgreSQL uses huge pages on Linux
