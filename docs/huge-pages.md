# Using huge pages with Percona Operator for PostgreSQL

## Overview

Huge Pages (also called large or super pages) are bigger memory blocks that help reduce CPU overhead. Normally, memory is managed in 4kB chunks, also called "pages", but when your PostgreSQL workload grows, the CPU has to juggle a lot of these small pages. By switching to larger pages like 2MiB or 1GiB, you reduce the number of pages the CPU needs to track, which can improve efficiency and performance.

For PostgreSQL clusters managed by Percona Operator for PostgreSQL, enabling huge pages is a recommended optimization, especially for memory-intensive workloads.

## Why to use huge pages in PostgreSQL

PostgreSQL uses shared memory extensively for:

* Shared buffer pool
* WAL buffers
* Dynamic shared memory segments

When huge pages are enabled:

* PostgreSQL can access memory more efficiently.
* The system spends less time managing memory.
* Performance improves, especially under heavy load.

## Configure huge pages for Percona Operator for PostgreSQL

### Enable huge pages in your Kubernetes environment

Before configuring your cluster, make sure huge pages are enabled and available on the Kubernetes nodes. This setup is done outside the Operator and depends on your Kubernetes environment, whether you use a cloud-based Kubernetes like GKE, EKS, etc or use a bare-metal one.

Consult the Kubernetes environment's official documentation for how to enable huge pages there. 

For the further setup, you need to keep in mind the following:

* What page sizes are available (e.g., 2MiB vs 1GiB)
* How many pages are preallocated
* Will other workloads compete for these pages
* Do all nodes that will run PostgreSQL pods have huge pages available 
* When adding more nodes to your cluster, will they have huge pages available

### Request huge pages in your cluster Custom Resource

Once your Kubernetes nodes are ready, you can configure your PostgreSQL cluster to use huge pages.

1. Set the huge pages resource limits in your `deploy/cr.yaml` Custom Resource. 

    This example configuration tells Kubernetes to allocate 16Mi worth of 2MiB huge pages for this instance. If you're using 1GiB pages, change the key to `hugepages-1Gi`.
    
    ```yaml
    spec:
      instances:
        - name: instance1
          resources:
            limits:
              hugepages-2Mi: 16Mi
              memory: 4Gi
    ```   

    !!! important

        Kubernetes requires that `requests` and `limits` for huge pages match. If you only specify `limits`, Kubernetes will assume the same value for `requests`.

2. Apply the configuration

    ```bash
    kubectl apply -f deploy/cr.yaml -n <namespace>
    ```

### Verify huge pages are reserved

After deploying your cluster with huge pages configured, you can verify that they're being used by checking inside the database container:

```bash
cat /proc/meminfo | grep HugePages
```

You should see values for `HugePages_Total`, `HugePages_Free`, and `HugePages_Rsvd`, confirming that huge pages are reserved and in use.

## A note on default behavior

To avoid unexpected startup failures, Percona Operator disables huge pages by default (`huge_pages = off`). This prevents PostgreSQL from trying to use huge pages when none were requested. Once you explicitly configure huge pages in your spec, the Operator sets `huge_pages = try`, allowing PostgreSQL to use them if available.

If huge pages are enabled on your nodes but not requested by your pods, PostgreSQL might fall back to minimal memory settings. To avoid this, either:

- Enable huge pages properly in your pod spec.
- Schedule pods on nodes without huge pages.
- Or manually set `shared_buffers` to a reasonable value:

```yaml
spec:
  config:
    parameters:
      shared_buffers: 128MB
```
