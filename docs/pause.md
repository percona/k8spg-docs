# Pause/resume and standby mode for a PostgreSQL cluster

## Pause and resume the cluster

You can temporarily shut down your PostgreSQL cluster and bring it back later without losing data or configuration. You may want to pause the cluster for maintenance tasks, emergency manual intervention or debugging.

When paused, all changes to the cluster's current state are suspended and no statuses other than the "Progressing" condition are updated until you resume the reconciliation.

### How to pause

 Set the `spec.pause` option to `true` in your `deploy/cr.yaml` Custom Resource:

```yaml
spec:
  pause: true
  # ... rest of your spec
```

Apply the change:

```bash
kubectl apply -f deploy/cr.yaml
```

The Operator will gracefully stop the cluster (primary, replicas, pgBackRest, and related jobs).

### How to resume

Set `spec.pause` back to `false` in the same Custom Resource and apply:

```yaml
spec:
  pause: false
  # ... rest of your spec
```

```bash
kubectl apply -f deploy/cr.yaml
```

The Operator will start the cluster again using the existing data volumes.

### Troubleshooting

**The Operator does not pause the cluster**

If a backup job is running, the Operator will not pause the cluster and will log a warning. Remove a running backup job so you can pause:

```bash
kubectl delete job -l postgres-operator.crunchydata.com/pgbackrest-backup -n <namespace>
```

Then retry pausing the cluster.

## Standby mode

Standby PostgreSQL clusters provide a continuously replicated copy of your primary cluster, forming the backbone of high‑availability and disaster‑recovery strategies. They stay in sync through streaming replication, enabling you to quickly promote a standby if the primary becomes unavailable. Standby clusters can also run in separate regions or environments, helping you maintain business continuity during outages.

The standby mode for a cluster is controlled with the `spec.standby.enabled` option plus the `spec.standby.repoName` and/or `spec.standby.host` and `spec.standby.port` options in the Custom Resource. What options to specify depends on the standby cluster type. 

Read more about the supported types of standby clusters and their setup in the [Deploy a standby cluster for Disaster Recovery](standby.md) documentation.

