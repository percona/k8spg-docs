# Failover and recovery

This page describes what happens to a Percona Distribution for PostgreSQL cluster managed by the Operator when a component fails, how long writes are unavailable, and what data you can lose. Use it in two ways:

* **During an incident:** find your scenario in the [summary table](#summary), check whether recovery is automatic, and follow the scenario's **Act** steps if it is not.
* **For high-availability planning:** read the scenario details to understand the expected downtime and data-loss window before you choose replication mode, client timeouts, and Pod placement.

Most of the recovery times in this guide come down to one setting: `patroni.leaderLeaseDurationSeconds` (30 seconds by default). Lower it for faster failover, at the cost of more unnecessary failovers if the Kubernetes API server responds slowly. See [Reduce failover time and data loss](#reduce-failover-time-and-data-loss).

## Summary

| Scenario | Recovery | Write outage | Acknowledged writes lost |
| --- | --- | --- | --- |
| [Primary Pod deleted](#primary-pod-deleted), or [with the Operator down](#primary-pod-deleted-with-the-operator-down) | Automatic, Operator not required | ~13 s direct, ~7 s through pgBouncer (~9 s / ~6 s if the Operator is also down) | None |
| [PostgreSQL process crashes](#postgresql-crash) | Automatic, no failover | ~5 s | None |
| [Planned switchover](#planned-switchover) | You trigger it, automatic execution | ~8 s direct, ~16 s through pgBouncer | None |
| [Node hosting the primary powered off](#node-hosting-the-primary-is-powered-off) | Automatic | ~28 s, about one leader-lease duration | None expected, possible under asynchronous replication |
| [Primary Pod network-partitioned](#network-partition) | Automatic | ~33 s direct; through pgBouncer, as long as the partition lasts unless the client has its own timeout | Yes, writes the isolated primary acknowledged just before it demotes itself |
| [Node's kubelet loses the Kubernetes API server](#node-loses-the-kubernetes-api-server) | No impact while disconnected; failover on reconnection if eviction is pending | None while disconnected; ~9 s on reconnection if the eviction toleration elapsed | None |
| [Node with the primary and the repo host lost](#node-with-the-primary-and-the-repo-host-lost) | Automatic, but promotion can stall | ~95 s, about three times an ordinary node loss | None from the stall itself |
| [Primary PostgreSQL frozen](#frozen-primary) | Automatic | ~35 s direct, ~41 s through pgBouncer | Possible, writes acknowledged right before the freeze |
| [Node permanently lost](#permanent-node-loss) | Usually automatic; manual in one specific case | ~100 s automatic; ~67 s once you act, if you act in the right order | Possible, see the scenario for details |

"Write outage" is the time from the failure to the first successful `COMMIT` on the new primary, for a client that reconnects on error. "Acknowledged writes lost" means a transaction's `COMMIT` returned success to the client, but the write is missing after recovery.

## How failover works

This workflow explains why every scenario in this guide behaves the way it does.

* **Patroni, not the Operator, decides which instance is the primary.** Each database Pod runs Patroni. Patroni stores the leader lock in the annotations of the `<cluster-name>-ha` Kubernetes Endpoints object, so the Kubernetes API server is its distributed configuration store (DCS).
* **The leader lock expires after `patroni.leaderLeaseDurationSeconds`** (Patroni `ttl`, default `30`). The primary renews the lock every `patroni.syncPeriodSeconds` (Patroni `loop_wait`, default `10`). When the primary disappears without releasing the lock, replicas wait for the lock to expire before one promotes itself. This is why every *unplanned* failover on this page takes about one lease duration. See [`patroni.leaderLeaseDurationSeconds`](operator.md#patronileaderleasedurationseconds).
* **A primary that can't reach the Kubernetes API demotes itself.** If the primary can't renew the lock, Patroni demotes it to read-only after its own retry timeout (about 10 seconds by default). This happens well before the lock actually expires and a replica takes over. It prevents two writable primaries at once.
* **Clients reach the primary through the `<cluster-name>-ha` Service.** Patroni updates that Service's Endpoints directly. A Pod's Kubernetes readiness state does not route traffic to the primary. `<cluster-name>-primary` and pgBouncer both resolve to the same `<cluster-name>-ha` Service underneath.
* **Replication is asynchronous by default.** The primary acknowledges a `COMMIT` before any replica has the data. Whatever it acknowledged but hadn't yet streamed is lost when a replica takes over. To trade write latency for zero loss of acknowledged writes on failover, turn on [synchronous replication](ha-deploy.md#configure-synchronous-replication).
* **The Operator is not in the failover path.** If the Operator is down, Patroni still fails over on its own, and the StatefulSet controller still recreates deleted Pods.

## Check the cluster state during an incident

Run these first, whatever the scenario. Replace `<namespace>` and `cluster1` with your values.

1. Check the cluster state:

    ```bash
    kubectl get pg cluster1 -n <namespace>
    ```

    `ready` means all PostgreSQL Pods are ready. It does **not** mean no failover happened. The state stays `ready` through a fast failover. `initializing` with fewer ready Pods than the cluster size means at least one Pod isn't ready. See [Custom resource statuses](cr-statuses.md).

2. Check which instance holds the leader lock. This is the source of truth for which Pod accepts writes:

    ```bash
    kubectl get endpoints cluster1-ha -n <namespace> \
      -o jsonpath='{.metadata.annotations.leader}{"\n"}{.subsets[*].addresses[*].ip}{"\n"}'
    ```

3. Check the Patroni view of the cluster, from any running database Pod:

    ```bash
    kubectl exec -n <namespace> <pod-name> -c database -- patronictl list
    ```

    A healthy cluster shows one `Leader` in `running` state and the replicas `streaming`, on the same timeline (`TL`), with lag at or near `0`.

!!! warning "Don't rely on the `role` label alone during a network partition"

    Each Patroni instance updates its own Pod's `postgres-operator.crunchydata.com/role` label. A Pod that can't reach the Kubernetes API can't update its own label. So during a partition, both the isolated old primary and the new primary can carry `role=primary` at the same time, and the selector `postgres-operator.crunchydata.com/role=primary` can return two Pods. Use the `cluster1-ha` Endpoints `leader` annotation instead. It's always a single Pod.

## Primary Pod lost or switched over

**Automatic once triggered. No data lost.**

Patroni demotes the old primary and promotes a replica right away. It never waits for the leader lock to expire, which makes this the fastest recovery on this page. Three things trigger it:

### Primary Pod deleted

Kubernetes sends `SIGTERM` to the Pod. The StatefulSet controller, not the Operator, recreates it, and it rejoins as a replica roughly a minute later. A direct client reconnecting on error gets a successful `COMMIT` again in about 13 seconds; through pgBouncer, about 7 seconds.

### Primary Pod deleted with the Operator down

Failover works the same way because Patroni and the StatefulSet controller do
not need the Operator. Recovery is about 9 seconds direct and about 6 seconds
through pgBouncer. While the Operator is down, the PerconaPGCluster status is
not refreshed and can report a stale `ready` state. Restore the Operator to
resume reconciliation and status updates.

### Planned switchover

You ask the Operator to move the primary role to a specific replica. See [Change the PostgreSQL primary instance](change-primary.md) for the procedure. Direct clients recover in about 8 seconds. pgBouncer recovers more slowly, about 16 seconds, because it caches a failed server login for `server_login_retry` seconds (15 by default) and returns `server login has been failing` to new connections until that passes.

**Confirm:** run the [cluster state checks](#check-the-cluster-state-during-an-incident).
`patronictl list` shows the new or target Pod as `Leader`. Check Pod readiness
directly while the Operator is down because the custom resource status can be
stale. After restoring the Operator, confirm that `kubectl get pg` reports
`ready`.

**Act:** nothing needed for an involuntary Pod loss. After a planned switchover, set `patroni.switchover.enabled` back to `false`. If the Operator is down, restore its Deployment when you can; it's needed for configuration changes, backups, and scaling, not for failover.

**What you can lose:** nothing. The clean shutdown or demotion always streams all WAL to the replicas first.

## PostgreSQL crash

**Automatic. No failover, no data lost.**

If the `postgres` process dies but the Pod and Patroni stay up, Patroni restarts PostgreSQL in place and runs crash recovery. The same Pod keeps the leader lock the whole time, so there's no failover at all. Writes resume in about 5 seconds, on the same Pod, whether the client connects directly or through pgBouncer.

**Confirm:** run the [cluster state checks](#check-the-cluster-state-during-an-incident). `patronictl list` shows the same `Leader`, on the same timeline, as before.

**Act:** nothing needed. If it keeps crashing, check the PostgreSQL logs. See [Check the logs](debug-logs.md).

**What you can lose:** nothing. Crash recovery replays the WAL, so every acknowledged commit survives.

## Node hosting the primary is powered off

**Automatic. No action needed for the database.**

A replica takes over about 28 seconds after the power-off, consistent with the default lease (see [How failover works](#how-failover-works)). What happens to the Pod that was on the dead node depends on your platform. If the node comes back, or your platform replaces it under the same name, the Pod restarts and rejoins as a replica, and the cluster reports all Pods ready about two minutes after the power-off. If the node is gone for good, see [Recover from permanent node loss](#permanent-node-loss).

**Confirm:** run the [cluster state checks](#check-the-cluster-state-during-an-incident) once the node is back or replaced.

**Act:** nothing for the database itself. If the node never returns and the Pod stays stuck, follow [Recover from permanent node loss](#permanent-node-loss).

!!! warning "Clients without a query timeout can hang for many minutes"

    A client with an open connection through pgBouncer gets no error at all when the node loses power. pgBouncer keeps waiting on its dead server connection. Direct clients, and pgBouncer clients with their own query timeout, recover as soon as failover completes. Set a client-side statement or query timeout in your application or connection pool, so a request to a dead primary fails and retries instead of hanging indefinitely.

**What you can lose:** under asynchronous replication, any transaction the primary acknowledged but hadn't yet streamed to a replica when it lost power. Use [synchronous replication](ha-deploy.md#configure-synchronous-replication) to close this window.

## Network partition

**Automatic. Some acknowledged writes can be lost.**

The primary Pod is cut off from the replicas, the Operator, and the Kubernetes API server, but keeps running. Clients that can still reach it, for example on the same node, can keep writing to it for a while:

1. The isolated primary can't renew the leader lock. It keeps accepting and acknowledging writes from clients that can still reach it for about 12-14 seconds, then Patroni demotes it to read-only on its own. This stops two Pods from both accepting writes at once.
2. Once the lock fully expires, a replica promotes itself and the `cluster1-ha` Endpoints switch to it, about 28 seconds after the partition starts.
3. The isolated Pod's liveness probe keeps failing, so the kubelet repeatedly restarts its `database` container. It shows `CrashLoopBackOff` until the partition heals.
4. When the partition heals, the old primary rewinds its data with `pg_rewind` and rejoins as a replica, within seconds of the network recovering.

At no point do both the old and new primary accept writes. The old primary is already read-only well before the new one is promoted. A direct client reconnecting on error gets a successful `COMMIT` again after about 33 seconds. Through pgBouncer with a client-side timeout, recovery takes about 37-42 seconds. Through pgBouncer with no timeout at all, there's no bound on recovery time. The client stays stuck on its dead server connection for the entire length of the partition, however long that runs, and recovers only a few seconds after the network heals.

**Confirm:** run the [cluster state checks](#check-the-cluster-state-during-an-incident). The `cluster1-ha` Endpoints `leader` annotation names a single Pod, and `patronictl list` shows the other two `streaming` on the new timeline. Don't trust the `role` label until the partition heals.

**Act:** nothing needed for failover. Fix the network. The old primary rejoins on its own once it heals. A pgBouncer client with no query timeout won't get an error, and won't recover, until the partition itself heals, however long that takes.

**What you can lose:** any write the isolated primary acknowledged in the roughly 12-14 second window before it demotes itself. At a steady 5 commits a second, that window is enough to lose 55-65 acknowledged writes. Scale that to your own write rate to estimate your exposure. Writes from clients that couldn't reach the isolated primary at all aren't lost. They simply failed instead of being acknowledged. To prevent this loss entirely, use [synchronous replication](ha-deploy.md#configure-synchronous-replication).

## Node loses the Kubernetes API server

**No impact at first; automatic once it's resolved.**

If only the kubelet on the primary's node loses its connection to the Kubernetes API server, Patroni keeps renewing the leader lock normally, since Pod-to-Pod traffic and the Pods' own API access still work. The primary keeps serving writes without interruption for as long as the outage runs. Kubernetes, meanwhile, loses track of the node. It marks the node `NotReady` after its usual grace period, and would evict the node's Pods after the default toleration for an unreachable node (5 minutes). But the kubelet can't carry out that eviction until it reconnects. When it does, it carries out the pending eviction at once and terminates the primary Pod. That causes a failover at that moment, exactly as if you had [deleted the primary Pod](#primary-pod-deleted): a direct client recovers in about 9 seconds, pgBouncer in about 16.

**Confirm:** run the [cluster state checks](#check-the-cluster-state-during-an-incident). The node shows `Ready` again, and if the toleration window passed, `patronictl list` shows a new leader.

**Act:**

* If the kubelet reconnects within about 5 minutes of the node going `NotReady`, nothing happens. There's no failover at all.
* If the outage runs longer than that, expect a failover the moment the kubelet reconnects, on top of however long the outage itself ran. To choose that moment yourself instead, do a [planned switchover](#planned-switchover) to a replica on a healthy node before you restore the node's connectivity.

**What you can lose:** nothing. When the delayed failover happens, it's a clean shutdown, just like deleting the primary Pod.

## Node with the primary and the repo host lost

**Automatic, but promotion can stall.**

Losing the lock works the same as any other power-off: a replica takes over the leader lock in about 32-34 seconds, consistent with the default lease. But if that node also hosted your pgBackRest repo host, the new primary's promotion needs to replay WAL via `restore_command`, which tries the now-unreachable repo first and only falls back to another configured repository after its own connection-timeout default (60 seconds). With a single repository configured, there's nowhere to fall back to, and promotion stalls until that 60-second timeout passes. This is the one scenario on this page where the lease duration alone doesn't predict recovery time. Write access actually returns about 95 seconds after the node goes down, roughly three times as long as an ordinary node loss. A pgBouncer client with no query timeout gets no error at all until that resolves.

**Confirm:** run the [cluster state checks](#check-the-cluster-state-during-an-incident), plus `pgbackrest info` (or the cluster's backup status) once the repo host Pod is back, to confirm archiving has caught up.

**Act:** configure more than one backup repository, so there's somewhere for `restore_command` to fall back to, and keep the repo host off the primary's node with [anti-affinity](constraints.md) so a single node loss doesn't cost you both at once. If the node is gone for good, the repo host rebuilds the same way a lost instance does. See [Recover from permanent node loss](#permanent-node-loss).

**What you can lose:** the stall itself doesn't lose acknowledged writes. But if the repo host has to be rebuilt from scratch, its own backup history doesn't survive. Keep at least one repository in object storage (S3, GCS, or Azure), not only local volumes, so a rebuilt repo host isn't your only copy.

## Frozen primary

**Automatic.**

All PostgreSQL processes on the primary stop responding. A stalled disk or a paused process are typical causes. Patroni itself keeps running but can't confirm PostgreSQL is healthy, so it stops renewing the leader lock, and a replica promotes about 26 seconds later, consistent with the default lease. A direct client recovers in about 35 seconds; through pgBouncer, about 41 seconds. The kubelet then restarts the frozen `database` container once its liveness probe fails enough times in a row, a count derived from your `patroni.syncPeriodSeconds` and `patroni.leaderLeaseDurationSeconds`. In practice, with the defaults, that's around 86-89 seconds. The old primary rejoins as a replica afterward.

!!! note

    This describes PostgreSQL freezing while the kubelet keeps running. If the whole node or virtual machine pauses, the kubelet pauses with it and can't restart the container. In that case the old primary can resume as a writable primary for a short time on already-open connections. It can accept and acknowledge a few more commits before Patroni notices it lost the lock and demotes it. Those commits are lost.

**Confirm:** run the [cluster state checks](#check-the-cluster-state-during-an-incident).
`patronictl list` shows the new `Leader` in `running` state and the old primary
rejoining as a replica once the kubelet restarts its container.

**Act:** nothing needed for failover itself. Investigate the underlying cause, such as storage latency.

**What you can lose:** any transaction acknowledged right before the freeze that hadn't yet streamed to a replica. Typically that's just one or two writes at moderate write rates, since Patroni stops trusting the primary within a few seconds of it going unresponsive. The exact number depends on how close to the freeze the write landed and your write rate.

## Permanent node loss

**Usually automatic. Manual only if a Pod gets stuck, and the order you act in matters.**

When Kubernetes cleanly and permanently removes a node, meaning it actually deregisters the node and not just marks it unreachable, its own node controller deletes the Node object and reschedules the affected Pods on its own, without getting stuck. Pods are rescheduled within about 7 seconds. The Node object itself is gone around 54 seconds later. The cluster reports `ready` again about 100 seconds after the node was removed. No manual steps are needed in that case.

The Pod can get stuck in `Terminating` when the node disappears *without* a clean deregistration, so Kubernetes doesn't know to clean up after it. If that happens:

!!! warning "Delete the PVC before the Pod, not after"

    Deleting the stuck Pod first lets Kubernetes immediately reattach a new Pod to the *same*, about-to-be-deleted PersistentVolumeClaim. That leaves the PVC stuck in `Terminating` while the cluster still reports `ready` with all instances. It looks healthy. It isn't, and it stays that way until you notice and delete the Pod a second time. Delete the PVC first instead. The rebuild completes cleanly in one pass, with the replica back to streaming in about a minute.

**Act:**

1. Confirm the node is genuinely gone for good (`kubectl get nodes`) and the Pod is stuck `Terminating` or `Pending` with no progress.
2. Delete the PVC first: `kubectl delete pvc <pvc-name> -n <namespace> --wait=false`
3. Then force-delete the Pod: `kubectl delete pod <pod-name> -n <namespace> --force --grace-period=0`
4. Wait for the Operator to rebuild the instance from backup, about a minute for a replica. Confirm with the [cluster state checks](#check-the-cluster-state-during-an-incident).

The same two steps work for the repo host Pod specifically. The Operator recreates its pgBackRest stanza on its own. No manual `pgbackrest stanza-create` is needed. Expect the stanza back within about a minute and a full backup completing shortly after.

**What you can lose:** if the repo host is the Pod that was lost and rebuilt, its existing backup history doesn't survive. If it was your only repository, you have no backups until the next scheduled one completes. Configure more than one repository, with at least one in object storage, so losing a node never costs you backup continuity.

## Reduce failover time and data loss

| Goal | What to change | Trade-off |
| --- | --- | --- |
| No loss of acknowledged writes on automatic failover | Turn on [synchronous replication](ha-deploy.md#configure-synchronous-replication) | Higher write latency. Without strict mode, Patroni can accept asynchronous commits when no synchronous standby is available and prevent automatic promotion of an unsafe standby. Set `synchronous_mode_strict: true` to block writes when no synchronous standby is available. |
| Faster unplanned failover | Lower [`patroni.leaderLeaseDurationSeconds`](operator.md#patronileaderleasedurationseconds) and [`patroni.syncPeriodSeconds`](operator.md#patronisyncperiodseconds) | More unnecessary failovers when the Kubernetes API server responds slowly |
| No hung clients | Set a statement or query timeout in your application or connection pool | Long-running queries need a higher timeout |
| Survive the loss of a node or zone | Spread PostgreSQL Pods and the repo host across nodes and zones with [anti-affinity and topology spread constraints](constraints.md) | Needs enough nodes and zones |
| Promotion doesn't stall on a lost repo host | Configure more than one backup repository | Extra storage cost and configuration |
