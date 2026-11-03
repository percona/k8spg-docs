# Swap roles between the Main and DR sites

A planned switchover turns the DR site into the primary and the Main site into the standby, while both sites stay healthy. Use it for maintenance, for a disaster recovery drill, or to move the primary to another region. If the Main site is already lost, [promote the standby](standby-failover.md) instead.

Stop application writes to the Main site before you start. The swap then loses no data. Writes stay unavailable for about 15 to 25 seconds, plus the time the DR site needs to replay any WAL that it hasn't applied yet.

## What happens to the old primary

The type of your [standby cluster](standby.md#types-of-standby-clusters) decides what the Main site does after DR is promoted:

| Standby type | Main site after the swap | What you do |
| --- | --- | --- |
| Streaming, or streaming with a repository | Follows the new primary on its own | Nothing. Check with `patronictl list` |
| Repo-based | Stays on its old timeline and can't follow DR | [Rebuild the Main site](#rebuild-the-old-primary-of-a-repo-based-standby) |

A repository-based Main site cannot follow because the shutdown checkpoint never reaches the pgBackRest repository. This checkpoint is the final record that PostgreSQL writes when it stops. The DR site never replays that record, so the two sites end up on different timelines. If you plan regular swaps, use a streaming standby and avoid the rebuild.

## Before you start

The examples use the `main` cluster and the `dr` cluster from the [streaming replication tutorial](standby-streaming.md). Set the namespaces of your clusters once, and you can run the commands as they are:

```bash
export MAIN_NAMESPACE=main-pg
export DR_NAMESPACE=dr-pg
```

1. Check that the DR cluster is `ready` and that the `StandbyLagging` condition isn't `True`:

    ```bash
    kubectl get pg dr -n "${DR_NAMESPACE}"
    ```

2. For a streaming standby, check that the Main site can reach the DR `-ha` Service and trusts its certificates. The Main site needs the same [TLS certificates signed by the same CA](standby-streaming.md#configure-dr-site) that the DR site uses. If you copied the Main site certificates to DR when you set up streaming, this is already true.

3. Make sure that the DR cluster has the same user passwords as the Main site. When the Operator promotes DR, it sets the password of each user in `spec.users` to the value in the DR user Secret. Follow [Prepare the user passwords](standby-failover.md#prepare-the-user-passwords) for each user. This covers the first swap. For a swap back, see [Swap back](#swap-back).

4. Make sure you can switch application traffic to the DR site after the swap.

## Swap the roles

1. Stop application writes to the Main site.

    The Operator doesn't stop two clusters from running as primary at the same time. Writes that both sites accept during an overlap are lost on the site that you demote.

2. Get the Main primary Pod and record its current WAL position:

    ```bash
    MAIN_PRIMARY=$(kubectl get pod -n "${MAIN_NAMESPACE}" \
      -l postgres-operator.crunchydata.com/cluster=main,postgres-operator.crunchydata.com/role=primary \
      -o jsonpath='{.items[0].metadata.name}')

    kubectl exec -n "${MAIN_NAMESPACE}" "${MAIN_PRIMARY}" -c database -- \
      psql -t -A -c "SELECT pg_current_wal_lsn();"
    ```

    ??? example "Sample output"

        ```{.text .no-copy}
        0/7034CF8
        ```

    Save this value. Read it after you stop the writes and before you demote the Main site. A value that you read after the demotion is never reached by a repo-based standby, and the wait in step 5 never ends.

    You don't need to run `pg_switch_wal()`. When the Main site shuts down cleanly during the demotion, PostgreSQL switches to a new WAL segment and archives it, so the DR site receives all the writes.

3. Demote the Main site. Set `standby.enabled` to `true` and point the cluster to the repository. For a streaming standby, also set `standby.host` to the DR `-ha` Service:

    === "Repo-based standby"

        ```bash
        kubectl patch pg main -n "${MAIN_NAMESPACE}" --type=merge \
          -p '{"spec":{"standby":{"enabled":true,"repoName":"repo1","host":null,"port":null}}}'
        ```

        The `null` values remove a `host` that the cluster kept from an earlier standby setup, so that the Main site reads only from the repository.

    === "Streaming standby"

        ```bash
        kubectl patch pg main -n "${MAIN_NAMESPACE}" --type=merge \
          -p "{\"spec\":{\"standby\":{\"enabled\":true,\"repoName\":\"repo1\",\"host\":\"dr-ha.${DR_NAMESPACE}.svc\",\"port\":5432}}}"
        ```

        If your standby has no repository, omit `repoName`.

4. Wait for the Main site to stop accepting writes:

    ```bash
    kubectl exec -n "${MAIN_NAMESPACE}" "${MAIN_PRIMARY}" -c database -- \
      psql -t -A -c "SELECT pg_is_in_recovery();"
    ```

    Don't continue until the command returns `t`.

5. Wait until the DR site replays the position that you recorded in step 2. Get the DR primary Pod, then run the check until it returns `t`. Replace `<lsn>` with the saved value:

    ```bash
    DR_PRIMARY=$(kubectl get pod -n "${DR_NAMESPACE}" \
      -l postgres-operator.crunchydata.com/cluster=dr,postgres-operator.crunchydata.com/role=primary \
      -o jsonpath='{.items[0].metadata.name}')

    kubectl exec -n "${DR_NAMESPACE}" "${DR_PRIMARY}" -c database -- \
      psql -t -A -c "SELECT pg_last_wal_replay_lsn() >= '<lsn>'::pg_lsn;"
    ```

    A repo-based standby replays WAL when it fetches a segment from the repository, so this step can take several seconds.

6. Promote the DR site:

    ```bash
    kubectl patch pg dr -n "${DR_NAMESPACE}" --type=merge \
      -p '{"spec":{"standby":{"enabled":false}}}'
    ```

7. Confirm that the DR site accepts writes:

    ```bash
    kubectl exec -n "${DR_NAMESPACE}" "${DR_PRIMARY}" -c database -- \
      psql -t -A -c "SELECT pg_is_in_recovery();"
    ```

    The command returns `f`. Switch your applications to the DR site. The Operator applies the user passwords about 10 seconds later. If your applications connect through pgBouncer, they can fail to log in for up to 30 seconds.

8. Check the Main site. For a streaming standby, `patronictl list` shows the Main member as `Standby Leader` in the `streaming` state on the new timeline:

    ```bash
    kubectl exec -n "${MAIN_NAMESPACE}" "${MAIN_PRIMARY}" -c database -- patronictl list
    ```

    For a repo-based standby, the member stays in `in archive recovery` on the old timeline. The PostgreSQL log repeats `new timeline 2 forked off current database system timeline 1`. Rebuild the Main site as described in the next section.

## Rebuild the old primary of a repo-based standby

Choose one of these ways to bring the Main site back as a standby of DR.

### Recreate the instance

This is the simplest way. After the swap, DR is the primary and holds all the writes that the Main site acknowledged, and the Main site is a standby. The data on the Main volumes has diverged from DR, so you can discard it. The Operator creates new instances, restores the latest backup from the pgBackRest repository, and replays the WAL from the repository until the Main site catches up with DR. Restore time depends on the size of your data.

Recreate every PostgreSQL instance of the Main site. The replicas of the old primary diverge as well, even though they report `streaming` and stay ready. If you recreate only the primary, Patroni makes a diverged replica the new standby leader.

!!! warning

    Delete the Main volumes only after the swap is complete. Check that the DR site accepts writes (step 7), that the Main site is in recovery (step 4), and that the repository has a backup:

    ```bash
    kubectl exec -n "${DR_NAMESPACE}" "${DR_PRIMARY}" -c database -- pgbackrest --stanza=db info
    ```

    If you delete the volumes of a site that is still the only primary, or before DR has replayed the recorded position in step 5, you lose data.

1. Delete the PVCs and the Pods of all Main instances:

    ```bash
    kubectl delete pvc -n "${MAIN_NAMESPACE}" \
      -l postgres-operator.crunchydata.com/cluster=main,postgres-operator.crunchydata.com/data=postgres \
      --wait=false

    kubectl delete pod -n "${MAIN_NAMESPACE}" \
      -l postgres-operator.crunchydata.com/cluster=main,postgres-operator.crunchydata.com/data=postgres
    ```

2. Check that every member is on the DR timeline:

    ```bash
    kubectl exec -n "${MAIN_NAMESPACE}" <main-pod-name> -c database -- patronictl list
    ```

    All members show the same `TL` as DR: one `Standby Leader` and the replicas in the `streaming` state.

`patronictl reinit` doesn't help here, because the Main site is a standby. On the primary it fails with `No replica among provided members`, and on the replicas it fails with `invalid option '--scope=main-ha'`.

### Add a streaming source

With a streaming source, Patroni rewinds the Main site with `pg_rewind` and no restore is needed. The Main site must trust the DR certificates. This way is for a Main site with one PostgreSQL instance. If your site has replicas, recreate every instance instead.

1. Copy the DR TLS Secrets `dr-cluster-cert` and `dr-replication-cert` to the Main namespace.

2. Reference them in the Main cluster and set the DR `-ha` Service as the standby host:

    ```bash
    kubectl patch pg main -n "${MAIN_NAMESPACE}" --type=merge -p "$(cat <<EOF
    {
      "spec": {
        "secrets": {
          "customTLSSecret": {"name": "dr-cluster-cert"},
          "customReplicationTLSSecret": {"name": "dr-replication-cert"}
        },
        "standby": {"enabled": true, "repoName": "repo1", "host": "dr-ha.${DR_NAMESPACE}.svc", "port": 5432}
      }
    }
    EOF
    )"
    ```

    The database Pods restart to load the new certificates.

    If you skip the certificates, the rewind fails with `SSL error: certificate verify failed` and the Main site stays diverged.

## Swap back

The roles are now reversed, and the swap back is the same procedure with the sites exchanged. For a repo-based standby, you rebuild the DR site the same way. To avoid the rebuild, [add a streaming source](standby-streaming.md) to the standby before the next swap.

### Re-apply the user passwords

The Operator applies the passwords from the user Secrets of a cluster only when a Secret changes. A site that was primary before keeps the passwords that the other site set while it was primary, including a password that you changed there. The Operator doesn't re-apply the `pgBouncer` user either, so pgBouncer on the promoted site can't log in to PostgreSQL.

After you promote the site, clear the `verifier` in the Secret of each user, so that the Operator rebuilds it from the password in that Secret and applies it again. Do the same for the `pgBouncer` user. The example uses the Main site:

```bash
kubectl patch secret main-pguser-<user-name> -n "${MAIN_NAMESPACE}" \
  -p '{"stringData":{"verifier":""}}'

kubectl patch secret main-pgbouncer -n "${MAIN_NAMESPACE}" \
  -p '{"stringData":{"pgbouncer-verifier":""}}'
```

The passwords from the Main Secrets apply again, and logins through pgBouncer work after about a minute. To keep a password that you changed on the other site, copy it to the Main Secret first, as in [Prepare the user passwords](standby-failover.md#prepare-the-user-passwords).
