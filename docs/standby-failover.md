# Failover

In case of the Main site failure or in other cases, you can promote the standby cluster. The promotion effectively allows writing to the cluster. This creates a net effect of pushing Write Ahead Logs (WALs) to the pgBackrest repository. It might create a split-brain situation where two primary instances attempt to write to the same repository. To avoid this, make sure the primary cluster is either deleted or shut down before trying to promote the standby cluster.

The examples on this page use the `main` cluster and the `dr` cluster from the [streaming replication tutorial](standby-streaming.md). Set the namespaces of your clusters once, and you can run the commands as they are:

```bash
export MAIN_NAMESPACE=main-pg
export DR_NAMESPACE=dr-pg
```

## Prepare the user passwords

Do this before you promote, and preferably when you set up the standby. A standby cluster replicates the users and their passwords from the Main site. While the cluster is read-only, the Operator doesn't apply the passwords from the DR cluster's own user Secrets. When you promote the cluster, the Operator sets the password of every user in `spec.users` to the value in the DR Secret `<cluster-name>-pguser-<user-name>`. If that value differs from the Main site password, applications that use the Main site credentials can't log in after the promotion.

If you don't set `spec.users`, there is nothing to copy. The DR cluster creates its own default user and database and leaves the default user of the Main site untouched, so the Main site credentials keep working.

For each user that you define in `spec.users`, copy the password from the Main site Secret to the DR Secret:

```bash
PASSWORD=$(kubectl get secret main-pguser-<user-name> -n "${MAIN_NAMESPACE}" \
  -o jsonpath='{.data.password}' | base64 -d)

kubectl patch secret dr-pguser-<user-name> -n "${DR_NAMESPACE}" \
  -p "{\"stringData\":{\"password\":\"${PASSWORD}\",\"verifier\":\"\"}}"
```

The Operator creates the DR Secret together with the DR cluster, so you can run these commands right after you deploy the standby. The change takes effect when you promote the cluster.

This step covers the first promotion of the DR cluster. If you promote a cluster that was primary before, see [Swap back](standby-switchover.md#swap-back).

## Promote the standby

Once the primary is down or inactive, promote the standby through changing the corresponding section:

```yaml
spec:
  standby:
    enabled: false
```

You can leave the other `standby` options, such as `host` and `repoName`, in the Custom Resource. The Operator ignores them when `enabled` is `false`.

Check that `SELECT pg_is_in_recovery();` returns `f`. Now you can start writing to the cluster.

The cluster status is `ready` before and during the promotion, so don't use it as a signal. About 10 seconds after the promotion, the Operator applies the user passwords from the DR Secrets. Applications that connect through pgBouncer can fail to log in for up to 30 seconds.

The Operator doesn't run scheduled backups while the cluster is a standby, and starts them after the promotion.

If both sites are healthy and you want to exchange their roles, follow [Swap roles between the Main and DR sites](standby-switchover.md) instead. A planned swap loses no data.

## Split brain

Split brain means that both clusters run as primary and write to the same pgBackRest repository. It happens when you promote the standby while the Main site is still running, or when the old primary comes back after you promoted the standby.

The Operator doesn't detect it. Both clusters stay `ready`, no condition or event is set, and archiving reports no failures, because both clusters successfully push WAL to the same repository on diverging timelines.

### Detect split brain

Run these checks on both sites. First, get the primary Pod of each cluster:

```bash
MAIN_PRIMARY=$(kubectl get pod -n "${MAIN_NAMESPACE}" \
  -l postgres-operator.crunchydata.com/cluster=main,postgres-operator.crunchydata.com/role=primary \
  -o jsonpath='{.items[0].metadata.name}')

DR_PRIMARY=$(kubectl get pod -n "${DR_NAMESPACE}" \
  -l postgres-operator.crunchydata.com/cluster=dr,postgres-operator.crunchydata.com/role=primary \
  -o jsonpath='{.items[0].metadata.name}')
```

1. Check that no more than one cluster is writable. In a split brain, `pg_is_in_recovery()` returns `f` on both:

    ```bash
    kubectl exec -n "${MAIN_NAMESPACE}" "${MAIN_PRIMARY}" -c database -- \
      psql -t -A -c "SELECT pg_is_in_recovery();"

    kubectl exec -n "${DR_NAMESPACE}" "${DR_PRIMARY}" -c database -- \
      psql -t -A -c "SELECT pg_is_in_recovery();"
    ```

2. Check the Patroni state. In a split brain, each site lists its own `Leader`, and the `TL` (timeline) column differs:

    ```bash
    kubectl exec -n "${MAIN_NAMESPACE}" "${MAIN_PRIMARY}" -c database -- patronictl list

    kubectl exec -n "${DR_NAMESPACE}" "${DR_PRIMARY}" -c database -- patronictl list
    ```

3. Check the repository. When two timelines write to it, `wal archive min/max` spans two timelines, and the backups of the second timeline appear in the list. Both sites use the same repository, so run this on one of them:

    ```bash
    kubectl exec -n "${MAIN_NAMESPACE}" "${MAIN_PRIMARY}" -c database -- \
      pgbackrest --stanza=db info
    ```

The cluster status from `kubectl get pg` and the `pg_stat_archiver` view don't show a split brain.

### Recover from split brain

Taking a new full backup from one cluster isn't enough. The repository keeps the history and the WAL of the other timeline, so every restore and every new standby that uses the latest backup tries to follow the wrong timeline and fails.

To recover, move the cluster that you keep to a new repository path, create a full backup there, and rebuild the other cluster from it. The old repository path stays untouched, so you keep its history.

The examples keep the `main` cluster and rebuild the `dr` cluster. If you keep the DR cluster, exchange the cluster names and the namespace variables. Get the primary Pod of each cluster first, as in [Detect split brain](#detect-split-brain).

1. Choose the cluster to keep. The writes that the other cluster acknowledged after the split aren't in the cluster that you keep. If you need them, export them before you continue. Both clusters continued their sequences from the same point, so exported rows can use the same primary key values as rows on the kept cluster and conflict when you insert them.

2. Stop the application writes to the other cluster and demote it to a standby. It becomes read-only on its own timeline, so you can still read its data for the export:

    ```bash
    kubectl patch pg dr -n "${DR_NAMESPACE}" --type=merge \
      -p '{"spec":{"standby":{"enabled":true,"repoName":"repo1"}}}'
    ```

3. Move the kept cluster to a new repository path:

    ```bash
    kubectl patch pg main -n "${MAIN_NAMESPACE}" --type=merge \
      -p '{"spec":{"backups":{"pgbackrest":{"global":{"repo1-path":"/pgbackrest/main-new"}}}}}'
    ```

4. Create the pgBackRest stanza in the new path. The Operator doesn't do it when you change `repo1-path`:

    ```bash
    kubectl exec -n "${MAIN_NAMESPACE}" "${MAIN_PRIMARY}" -c database -- \
      pgbackrest --stanza=db stanza-create
    ```

    !!! warning

        Run steps 3 and 4 one after another. Until the stanza exists in the new path, PostgreSQL still reports every WAL segment as archived, but the segments are not stored in any repository. A failure of the kept cluster in this time leaves you without those WAL files.

5. Create a full backup in the new path. Save this manifest as `deploy/backup.yaml`:

    ```yaml
    apiVersion: pgv2.percona.com/v2
    kind: PerconaPGBackup
    metadata:
      name: after-split-brain
    spec:
      pgCluster: main
      repoName: repo1
      options:
        - --type=full
    ```

    ```bash
    kubectl apply -f deploy/backup.yaml -n "${MAIN_NAMESPACE}"

    kubectl wait perconapgbackup/after-split-brain -n "${MAIN_NAMESPACE}" \
      --for=jsonpath='{.status.state}'=Succeeded \
      --timeout=600s
    ```

6. Set the same repository path on the other cluster and rebuild it. Delete its instance PVC and Pod, and the Operator restores the data from the new path as a standby of the kept cluster:

    ```bash
    kubectl patch pg dr -n "${DR_NAMESPACE}" --type=merge \
      -p '{"spec":{"backups":{"pgbackrest":{"global":{"repo1-path":"/pgbackrest/main-new"}}}}}'

    kubectl get pvc -n "${DR_NAMESPACE}" \
      -l postgres-operator.crunchydata.com/cluster=dr,postgres-operator.crunchydata.com/data=postgres

    kubectl delete pvc <pvc-name> -n "${DR_NAMESPACE}" --wait=false
    kubectl delete pod "${DR_PRIMARY}" -n "${DR_NAMESPACE}"
    ```

7. Check the members of the kept cluster. A replica that was created or restored while the split brain lasted may hold the data of the other timeline. It stays not ready, and its log repeats `highest timeline 1 of the primary is behind recovery timeline 2`. Reinitialize it:

    ```bash
    kubectl exec -n "${MAIN_NAMESPACE}" "${MAIN_PRIMARY}" -c database -- \
      patronictl reinit main-ha <replica-pod> --force
    ```

8. Keep the old repository path as long as you need its history for point-in-time recovery or for an investigation. Then delete it from your storage.

Removing the other timeline's files from the repository by hand also works, but it needs several manual deletions in the repository. A mistake destroys the history of the cluster that you keep, so this guide doesn't cover it.

## Automate the failover

Automated failover consists of multiple steps and is outside of the Operator’s scope. There are a few steps that you can take to reduce the Recovery Time Objective (RTO). To detect the failover we recommend having the 3rd site to monitor both DR and Main sites. In this case you can be sure that Main really failed and it is not a network split situation.

Another aspect of automation is to switch the traffic for the application from Main to Standby after promotion. It can be done through various Kubernetes configurations and heavily depends on how your networking and application are designed. The following options are quite common:

1. Global Load Balancer - various clouds and vendors provide their solutions
2. Multi Cluster Services or MCS - available on most of the public clouds
3. Federation or other multi-cluster solutions
