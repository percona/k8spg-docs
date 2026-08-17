# Deploy a logical replica

A logical replica is an extra, read-only PostgreSQL instance in the **same** cluster. It has its own volume and Service, so you can point reporting and other heavy reads at it instead of the primary.

The Operator first copies the whole data directory (a physical seed), then keeps selected databases in sync with [logical replication :octicons-link-external-16:](https://www.postgresql.org/docs/current/logical-replication.html): the primary sends row changes, not a byte-for-byte copy of WAL. The replica uses the same PostgreSQL image as the cluster.

It is **not** a high-availability replica. Patroni does not manage it, does not promote it, and does not use it for failover. For a copy you can promote, use a [standby cluster](standby.md).


## How it works

Declare the logical replica in the Custom Resource by adding a `logicalReplicas` entry with the name of the replica, the bootstrap method and the volume configuration.

The cluster must be `ready` and the primary must be able to send logical changes. This means the following conditions must be met:

* `wal_level` must be `logical`,
* the reserved `logicalrepl` user must exist,
* `pg_hba` rules must allow the `logicalrepl` user to connect.

If something is still missing, the replica stays in the `bootstrapping` state and the `ReadyForLogicalReplication` condition says what is waiting.

After you apply the configuration, the Operator waits until the cluster is `ready`. Then, for each replica, it:

1. **Resolves databases.** It records which databases will keep receiving changes. That list does not change later. If a named database does not exist yet, it waits.
2. **Creates a volume** for the replica.
3. **Runs a bootstrap Job.** The Job copies the data directory, removes Patroni settings, and converts the copy into a logical replica. This replica receives row changes later, not WAL replay.
4. **Starts PostgreSQL** on that volume, without Patroni. This instance is not part of failover.
5. **Creates a Service** so you can connect to the replica.
6. **Watches health.** The Operator checks that replication is still running: the primary still has the replication slots, and the replica is still applying changes. If either stops, the replica status becomes `broken`.

[Add a logical replica](#add-a-logical-replica){.md-button}

## Why use logical replicas

Use a logical replica when you need:

* **Reporting without loading the primary.** The replica has its own Pod and volume, so heavy reads do not compete with the high-availability set.
* **Ongoing changes for selected databases.** List them in `spec.logicalReplicas[].databases`. The Operator copies the whole data directory first. After it converts the physical replica into a logical one, later changes apply to every table in those listed databases. Omit `databases` to include changes for all databases except templates and `postgres`.
* **Keep a copy that Patroni will not promote.** Patroni manages
physical replicas and can promote them to primary. A logical
replica never becomes the primary. That is useful when you want
a stable read endpoint that must not take writes during failover.

Do not use a logical replica to filter tables, run a different PostgreSQL major version, accept writes, or fail over. For a copy you can promote, use a [standby cluster](standby.md).

## Availability and requirements

To use logical replicas, the following requirements must be met: 

* The Operator version **3.1.0** or later and
* PostgreSQL **17 or later**.
* `wal_level` must be set to `logical`. 
* Enough free replication slots and WAL senders on the primary. Raise `max_replication_slots` and `max_wal_senders` through [`patroni.dynamicConfiguration`](operator.md#patronidynamicconfiguration) if bootstrap reports that the primary is short of capacity.
* A successful backup in the cluster repository if you use the default `pgbackrest` bootstrap method
* If [backups are disabled](backups-disable.md), you **must** set `bootstrapMethod: pg_basebackup`
* The replica name must be unique and must not collide with an `spec.instances[].name`. The name length is maximum 20 characters.

## Add a logical replica

You can add logical replicas when you create the cluster, or add it later to an existing cluster. The Operator starts bootstrapping the replica only after the cluster is `ready`.

1. Edit `deploy/cr.yaml` and add a `logicalReplicas` entry. This example creates a replica named `analytics` that keeps the `cluster1` database in sync after a full seed from pgBackRest:

    ```yaml
    spec:
      postgresVersion: 17
      logicalReplicas:
        - name: analytics
          databases:
            - cluster1
          bootstrapMethod: pgbackrest
          dataVolumeClaimSpec:
            accessModes:
              - ReadWriteOnce
            resources:
              requests:
                storage: 1Gi
    ```

    `dataVolumeClaimSpec` is required. `bootstrapMethod` defaults to `pgbackrest`. Use `pg_basebackup` if [backups are disabled](backups-disable.md).

    To expose the replica outside the cluster, set `expose.type`. See [Exposing the cluster](expose.md) and [`logicalReplicas` options](operator.md#logicalreplicasname).

2. Apply the Custom Resource:

    ```bash
    kubectl apply -f deploy/cr.yaml -n <namespace>
    ```

3. Wait until the replica is `ready`:

    ```bash
    kubectl get pg <cluster-name> -n <namespace> \
      -o jsonpath='{.status.logicalReplicas}' && echo
    ```

    ??? example "Sample output"

        ```{.text .no-copy}
        [{"name":"analytics","state":"ready","databases":["cluster1"],"seededAt":"2026-08-13T10:15:04Z"}]
        ```

    While bootstrap runs, `state` is `bootstrapping`. If it stays there, check the Job:

    ```bash
    kubectl get job <cluster-name>-lr-<replica-name>-bootstrap -n <namespace>
    kubectl logs job/<cluster-name>-lr-<replica-name>-bootstrap -n <namespace>
    ```

    Status values and reasons are listed in [Custom resource statuses](cr-statuses.md#logical-replica-status).

## Connect to the replica

The replica is not behind pgBouncer. Connect to its Service, named `<cluster-name>-lr-<replica-name>`. For `cluster1` and replica `analytics`:

```bash
kubectl get service cluster1-lr-analytics -n <namespace>
```

From inside the cluster, use `cluster1-lr-analytics.<namespace>.svc.cluster.local`. Point the host at this Service, not at pgBouncer or the HA Service. Use an existing user Secret for credentials (for example `<cluster-name>-pguser-<user>`).

Prefer `sslmode=verify-ca`. See [TLS](TLS.md#logical-replica-connections) if you need hostname verification.

## Reseed a logical replica

Reseed after a failed bootstrap, a missing slot, a disabled subscription, or an [in-place restore](backups-restore-inplace.md). Changing fields on an existing replica does not rebuild it.

1. Remove the replica from `spec.logicalReplicas` and apply the Custom Resource.
2. Wait until it disappears from `status.logicalReplicas`.
3. Add it back and apply again.

```bash
kubectl get pg <cluster-name> -n <namespace> \
  -o jsonpath='{.status.logicalReplicas}' && echo
```

A Patroni failover often breaks replication (`SourceSlotMissing`). Reseed, or see [Logical replicas and failover](ha-deploy.md#logical-replicas-and-failover).

## Remove a logical replica

Remove its entry from `spec.logicalReplicas` and apply the Custom Resource. The Operator always deletes the replica PVC.

If the primary is down during removal, status keeps the replica with reason `AwaitingCleanup` until slots can be dropped on a primary.

## Implementation specifics

[PostgreSQL logical replication restrictions :octicons-link-external-16:](https://www.postgresql.org/docs/current/logical-replication-restrictions.html) still apply. Also keep these Operator behaviors in mind:

* **Do not write to the replica.** A local write can stop replication. [Reseed](#reseed-a-logical-replica) the replica to recover.
* **Schema changes are not replicated.** Apply `ALTER TABLE` on the replica yourself. Add columns on the replica first; drop them on the primary first. Do not change the schema during bootstrap.
* **After seed, only row changes continue** (`INSERT`, `UPDATE`, `DELETE`, `TRUNCATE`) for the databases you named. New tables and databases are ignored. Sequences and large objects drift after the seed. Updates and deletes need a primary key, a non-null unique key, or `REPLICA IDENTITY FULL`.
* **Failover often breaks replication.** Slots stay on the old primary (`SourceSlotMissing`). [Reseed](#reseed-a-logical-replica) a logical replica or see [Logical replicas and failover](ha-deploy.md#logical-replicas-and-failover).
* **A failed bootstrap does not retry** on the same volume. Remove the replica from the spec, wait until it leaves status, then add it back.
* **Connect to the replica Service.** It is not behind pgBouncer, not in PMM, and not in the HA Services (`*-ha`, `*-replicas`).
* **Deleting a replica always deletes its PVC**, even if the cluster `delete-pvc` finalizer is off.
* **Pausing the cluster does not stop the logical replica Pod.** Apply workers fail while the primary is down.
* **`logicalrepl` is reserved.** Do not define it in `spec.users`. See [Users](users.md#considerations).
* **`bootstrapMethod` is read only during bootstrap.** Changing it later has no effect.
