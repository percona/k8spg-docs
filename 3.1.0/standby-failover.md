> For the complete documentation index, see [llms.txt](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/llms.txt).

# Failover

Promote the standby cluster when the Main site is lost, for example after an outage of its Kubernetes cluster or region. The promotion makes the standby cluster writable, and it starts to push Write Ahead Logs (WALs) to the pgBackRest repository.

Before you promote, make sure that the Main site can’t accept writes. A Main site that you can’t reach isn’t necessarily down: the network can be split, or the site can come back after the promotion. Then both clusters run as primary and accept writes. This is a [split brain](#split-brain). To avoid it, shut down or delete the Main cluster before you promote the standby cluster.

The examples on this page use the `main` cluster and the `dr` cluster from the [streaming replication tutorial](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/standby-streaming.html). Set the namespaces of your clusters once, and you can run the commands as they are:

```
export MAIN_NAMESPACE=main-pg
export DR_NAMESPACE=dr-pg
```

## Prepare the user passwords

Do this before you promote, and preferably when you set up the standby. A standby cluster replicates the users and their passwords from the Main site. While the cluster is read-only, the Operator doesn’t apply the passwords from the Disaster Recovery (DR) cluster’s own user Secrets. When you promote the cluster, the Operator sets the password of every user in `spec.users` to the value in the DR Secret `<cluster-name>-pguser-<user-name>`. If that value differs from the Main site password, applications that use the Main site credentials can’t log in after the promotion.

If you don’t set `spec.users`, there is nothing to copy. The DR cluster creates its own default user and database and leaves the default user of the Main site untouched, so the Main site credentials keep working.

For each user that you define in `spec.users`, copy the password from the Main site Secret to the DR Secret:

```
PASSWORD_B64=$(kubectl get secret main-pguser-<user-name> -n "${MAIN_NAMESPACE}" \
  -o jsonpath='{.data.password}')

kubectl patch secret dr-pguser-<user-name> -n "${DR_NAMESPACE}" \
  -p "{\"data\":{\"password\":\"${PASSWORD_B64}\"},\"stringData\":{\"verifier\":\"\"}}"
```

The command copies the encoded value as it is, so passwords with quotes, backslashes or non-ASCII characters stay intact. The Operator rebuilds the `verifier` from the new password within a few seconds.

The Operator creates the DR Secret together with the DR cluster, so you can run these commands right after you deploy the standby. The change takes effect when you promote the cluster.

### Copy the pgBouncer password

pgBouncer logs in to PostgreSQL as the `_crunchypgbouncer` user. Its password is in the Secret `<cluster-name>-pgbouncer`. When you promote the DR cluster, the Operator applies this user from the DR Secret, in the same way as the other users. Therefore, copy the pgBouncer password from the Main site to the DR site, so that both sites use the same one. This ensures that pgBouncer can authenticate in the new primary:

```
PGBOUNCER_PASSWORD_B64=$(kubectl get secret main-pgbouncer -n "${MAIN_NAMESPACE}" \
  -o jsonpath='{.data.pgbouncer-password}')

PGBOUNCER_VERIFIER_B64=$(kubectl get secret main-pgbouncer -n "${MAIN_NAMESPACE}" \
  -o jsonpath='{.data.pgbouncer-verifier}')

kubectl patch secret dr-pgbouncer -n "${DR_NAMESPACE}" \
  -p "{\"data\":{\"pgbouncer-password\":\"${PGBOUNCER_PASSWORD_B64}\",\"pgbouncer-verifier\":\"${PGBOUNCER_VERIFIER_B64}\"}}"
```

Copy the password and the verifier together. If you copy only the password, the Operator applies the old DR verifier when it promotes the cluster, and pgBouncer can’t log in after you swap back. Don’t set the verifier to an empty string, as you do for the user Secrets. The Operator then generates a new pgBouncer password and discards the one that you copied.

Repeat the copy after you change a password on the Main site. Clear the verifier after a promotion only if the passwords on the two sites differ. If they differ, for example because a password changed on one site after you copied it, see [Swap back](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/standby-switchover.html#swap-back).

## Promote the standby

Once the primary is down or inactive, promote the standby through changing the corresponding section:

```
spec:
  standby:
    enabled: false
```

You can leave the other `standby` options, such as `host` and `repoName`, in the Custom Resource. The Operator ignores them when `standby.enabled` is `false`. They apply again if you set `enabled` back to `true`.

Check that `SELECT pg_is_in_recovery();` returns `f`. Now you can start writing to the cluster.

The cluster status is `ready` before and during the promotion, so don’t use it as a signal. About 10 seconds after the promotion, the Operator applies the user passwords from the DR Secrets. Applications that connect through pgBouncer can fail to log in for up to 30 seconds.

The Operator doesn’t run scheduled backups while the cluster is a standby, and starts them after the promotion.

If both sites are healthy and you want to exchange their roles, follow [Swap roles between the Main and DR sites](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/standby-switchover.html) instead. A planned swap loses no data.

## Split brain

Split brain means that both clusters run as primary and accept writes. It happens when you promote the standby while the Main site is still running, or when the old primary comes back after you promoted the standby.

The Operator doesn’t detect it. Both clusters stay `ready` and no condition or event is set. If the standby uses the same pgBackRest repository as the Main site, archiving also reports no failures, because both clusters successfully push WAL to the same repository on diverging timelines.

### Detect split brain

Run these checks on both sites. First, get the primary Pod of each cluster:

```
MAIN_PRIMARY=$(kubectl get pod -n "${MAIN_NAMESPACE}" \
  -l postgres-operator.crunchydata.com/cluster=main,postgres-operator.crunchydata.com/role=primary \
  -o jsonpath='{.items[0].metadata.name}')

DR_PRIMARY=$(kubectl get pod -n "${DR_NAMESPACE}" \
  -l postgres-operator.crunchydata.com/cluster=dr,postgres-operator.crunchydata.com/role=primary \
  -o jsonpath='{.items[0].metadata.name}')
```

1. Check that no more than one cluster is writable. In a split brain, `pg_is_in_recovery()` returns `f` on both:

   ```
   kubectl exec -n "${MAIN_NAMESPACE}" "${MAIN_PRIMARY}" -c database -- \
     psql -t -A -c "SELECT pg_is_in_recovery();"

   kubectl exec -n "${DR_NAMESPACE}" "${DR_PRIMARY}" -c database -- \
     psql -t -A -c "SELECT pg_is_in_recovery();"
   ```

1. Check the Patroni state. In a split brain, each site lists its own `Leader`. The `TL` (timeline) column usually differs, but both sites can also stay on the same timeline:

   ```
   kubectl exec -n "${MAIN_NAMESPACE}" "${MAIN_PRIMARY}" -c database -- patronictl list

   kubectl exec -n "${DR_NAMESPACE}" "${DR_PRIMARY}" -c database -- patronictl list
   ```

1. For a repo-based standby and for a streaming standby with a repository, both sites may use the same pgBackRest repository. This this case, check whether the old primary still writes WAL to it. Use this check when you can’t reach the Main site. `pgbackrest info` isn’t enough. After a promotion, it lists the backup that the Operator takes after the promotion, whether the old primary still runs or not, and it doesn’t show which site wrote the WAL. First, list the WAL directories. The output has one directory for each PostgreSQL version, for example `18-1`:

   ```
   kubectl exec -n "${DR_NAMESPACE}" "${DR_PRIMARY}" -c database -- \
     pgbackrest --stanza=db repo-ls archive/db
   ```

   Then list the WAL files of the timeline that the Main site was on, twice, a minute apart. The first 8 characters of the directory name are the timeline, so `0000000100000000` is timeline 1:

   ```
   kubectl exec -n "${DR_NAMESPACE}" "${DR_PRIMARY}" -c database -- \
     pgbackrest --stanza=db repo-ls archive/db/<version-directory>/0000000100000000
   ```

   If new files appear on that timeline after the promotion, the old primary still writes. The absence of new files doesn’t prove that the Main site is down, because an idle primary may not archive new WAL. If both sites stay on the same timeline, new files can come from either site, and this check can’t tell them apart. This check doesn’t apply to a streaming standby without a repository.

Checks 1 and 2 are the reliable ones when you can reach both sites. The cluster status from `kubectl get pg` and the `pg_stat_archiver` view don’t show a split brain.

### Recover from split brain

The recovery steps depend on the type of your [standby cluster](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/standby.html#types-of-standby-clusters):

- For a repo-based standby and for a streaming standby with a repository, both sites share the pgBackRest repository. Follow [Recover a repo-based standby or a streaming standby with a repository](#recover-a-repo-based-standby-or-a-streaming-standby-with-a-repository).
- For a streaming standby without a repository, follow [Recover a streaming standby without a repository](#recover-a-streaming-standby-without-a-repository).

In both cases, you choose the cluster that keeps being the Main site, stop the writes to the other cluster, and rebuild the other cluster as a standby of the kept one.

The examples keep the `main` cluster and rebuild the `dr` cluster. If you keep the DR cluster, exchange the cluster names and the namespace variables. Get the primary Pod of each cluster first, as in [Detect split brain](#detect-split-brain).

#### Recover a repo-based standby or a streaming standby with a repository

Taking a new full backup from one cluster isn’t enough. The repository keeps the history and the WAL of the other timeline, so every restore and every new standby that uses the latest backup tries to follow the wrong timeline and fails.

To recover, move the cluster that you keep to a new repository path, create a full backup there, and recreate the other cluster with that path. The old repository path stays untouched, so you keep its history.

1. Stop the application writes to the other cluster, and export the rows that it accepted after the split. The writes that the kept cluster doesn’t have are the rows that were written after you promoted the standby cluster. Select them with a column that records the time or the order of the writes. The example exports one table to a file on your computer:

   ```
   kubectl exec -n "${DR_NAMESPACE}" "${DR_PRIMARY}" -c database -- \
     psql -d <database-name> -c "COPY (SELECT <columns> FROM <table-name> WHERE created_at >= '<promotion-time>') TO STDOUT WITH CSV HEADER" \
     > <table-name>.csv
   ```

   Repeat the command for each table that has new rows. Then pause the other cluster, so that it stops accepting writes:

   ```
   kubectl patch pg dr -n "${DR_NAMESPACE}" --type=merge \
     -p '{"spec":{"pause":true}}'
   ```

   You can delete the cluster instead. In this case, only its PVCs are left to delete.

1. Set a new, unused repository path on the kept cluster:

   ```
   kubectl patch pg main -n "${MAIN_NAMESPACE}" --type=merge \
     -p '{"spec":{"backups":{"pgbackrest":{"global":{"repo1-path":"/pgbackrest/main-new"}}}}}'
   ```

1. Wait until the Pod of the kept cluster uses the new path. The new path reaches the Pod with a delay of up to about a minute. Run this command until the status changes to `missing stanza path`:

   ```
   kubectl exec -n "${MAIN_NAMESPACE}" "${MAIN_PRIMARY}" -c database -- \
     pgbackrest --stanza=db info
   ```

   Sample output

   ```
   stanza: db
       status: error (missing stanza path)
   ```

   If you run `stanza-create` before the status changes, it reports success for the old path and doesn’t create the stanza in the new one.

1. Create the pgBackRest stanza in the new path right away. The Operator doesn’t do it when you change `repo1-path`:

   ```
   kubectl exec -n "${MAIN_NAMESPACE}" "${MAIN_PRIMARY}" -c database -- \
     pgbackrest --stanza=db stanza-create
   ```

   Warning

   Until the stanza exists in the new path, PostgreSQL still reports every WAL segment as archived, but the segments are not stored in any repository. A failure of the kept cluster in this time leaves you without those WAL files.

1. Push the current timeline history file of the kept cluster to the new path. The new path doesn’t have it yet, and a standby that restores from this path needs it to follow the timeline of the kept cluster. Get the timeline number from the `TL` column of `patronictl list`. The history file name has eight digits, for example `00000002.history` for timeline 2. Replace `<version>` with your PostgreSQL major version:

   ```
   kubectl exec -n "${MAIN_NAMESPACE}" "${MAIN_PRIMARY}" -c database -- \
     pgbackrest --stanza=db --no-archive-async archive-push /pgdata/pg<version>/pg_wal/<history-file>
   ```

   If the kept cluster is on timeline 1, it has no history file. Skip this step.

1. Create a full backup in the new path. Save this manifest as `deploy/backup.yaml`:

   ```
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

   Apply the manifest and wait for the backup to complete:

   ```
   kubectl apply -f deploy/backup.yaml -n "${MAIN_NAMESPACE}"

   kubectl wait perconapgbackup/after-split-brain -n "${MAIN_NAMESPACE}" \
     --for=jsonpath='{.status.state}'=Succeeded \
     --timeout=600s
   ```

1. Delete the other cluster and its PVCs, then create it again with the same `repo1-path` as the kept cluster:

   ```
   kubectl delete pg dr -n "${DR_NAMESPACE}"

   kubectl delete pvc -n "${DR_NAMESPACE}" \
     -l postgres-operator.crunchydata.com/cluster=dr
   ```

   Apply the manifest of the cluster again with the new path. Keep the other options of your standby, such as `repoName`. For a streaming standby with a repository, also keep `host` and `port`, and point `host` to the `-ha` Service of the kept cluster:

   ```
   spec:
     backups:
       pgbackrest:
         global:
           repo1-path: /pgbackrest/main-new
     standby:
       enabled: true
       repoName: repo1
   ```

   The Operator restores the data from the new path as a standby of the kept cluster. The user and pgBouncer Secrets stay in the namespace, so the passwords don’t change. Check that every member is on the timeline of the kept cluster. Get a Pod of the rebuilt cluster, then run:

   ```
   kubectl exec -n "${DR_NAMESPACE}" <dr-pod-name> -c database -- patronictl list
   ```

1. Import the exported rows into the kept cluster:

   ```
   kubectl exec -i -n "${MAIN_NAMESPACE}" "${MAIN_PRIMARY}" -c database -- \
     psql -d <database-name> -c "COPY <table-name> (<columns>) FROM STDIN WITH CSV HEADER" \
     < <table-name>.csv
   ```

   Both clusters kept counting from the same sequence values, so the exported rows can have the same primary keys as existing rows. Leave the primary key column out of `<columns>` in both the export and the import, so that the kept cluster assigns new keys.

1. Keep the old repository path as long as you need its history for point-in-time recovery or for an investigation. Then delete it from your storage.

Removing the other timeline’s files from the repository by hand also works, but it needs several manual deletions in the repository. A mistake destroys the history of the cluster that you keep, so this guide doesn’t cover it.

#### Recover a streaming standby without a repository

Delete the cluster that you don’t keep, together with its volumes, and create it again as a streaming standby of the kept cluster. A streaming standby without a repository can’t restore from a backup, so deleting only its PVCs and Pods doesn’t work. The new Pod waits forever with `waiting for standby_leader to bootstrap`.

1. Choose the cluster to keep. Stop the application writes to the other cluster, and export the rows that it accepted after the split.

   The other cluster loses these writes, because you delete its volumes in the next step. The writes that the kept cluster doesn’t have are the rows that were written after you promoted the standby cluster. The cluster is still writable, so you can read its tables right away. Select the rows with a column that records the time or the order of the writes. The example exports one table to a file on your computer:

   ```
   kubectl exec -n "${DR_NAMESPACE}" "${DR_PRIMARY}" -c database -- \
     psql -d <database-name> -c "COPY (SELECT <columns> FROM <table-name> WHERE created_at >= '<promotion-time>') TO STDOUT WITH CSV HEADER" \
     > <table-name>.csv
   ```

   Repeat the command for each table that has new rows.

1. Delete the other cluster and its PVCs:

   ```
   kubectl delete pg dr -n "${DR_NAMESPACE}"

   kubectl delete pvc -n "${DR_NAMESPACE}" \
     -l postgres-operator.crunchydata.com/cluster=dr
   ```

1. Create the cluster again as a streaming standby of the kept cluster. Set `standby.host` to the `-ha` Service of the kept cluster and `standby.port` to `5432`:

   ```
   spec:
     standby:
       enabled: true
       host: main-ha.main-pg.svc
       port: 5432
   ```

   The deletion keeps the user Secrets, the pgBouncer Secret and your TLS Secrets, so the new standby uses them again. If you deleted them, create the TLS Secrets again before you apply the manifest, as in [Configure DR site](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/standby-streaming.html#configure-dr-site). Without them, the cluster doesn’t start. Then copy the user and pgBouncer passwords from the kept cluster again, as in [Prepare the user passwords](#prepare-the-user-passwords). Otherwise, pgBouncer on the new standby can’t log in to PostgreSQL after a promotion.

1. Check that the new standby is on the timeline of the kept cluster. Get a Pod of the rebuilt cluster, then run:

   ```
   kubectl exec -n "${DR_NAMESPACE}" <dr-pod-name> -c database -- patronictl list
   ```

   The member shows as `Standby Leader` in the `streaming` state, and the `TL` column has the same value as the kept cluster.

## Automate the failover

Automated failover consists of multiple steps and is outside of the Operator’s scope. There are a few steps that you can take to reduce the Recovery Time Objective (RTO). To detect the failover we recommend having the 3rd site to monitor both DR and Main sites. In this case you can be sure that Main really failed and it is not a network split situation.

Another aspect of automation is to switch the traffic for the application from Main to Standby after promotion. It can be done through various Kubernetes configurations and heavily depends on how your networking and application are designed. The following options are quite common:

1. Global Load Balancer - various clouds and vendors provide their solutions
1. Multi Cluster Services or MCS - available on most of the public clouds
1. Federation or other multi-cluster solutions
