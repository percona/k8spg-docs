# Standby promotion and user passwords: test report

This report checks, on a live cluster, how promoting a standby cluster interacts with PostgreSQL user passwords, and validates the draft text in `docs/standby-failover.md` ("Prepare the user passwords", "Promote the standby") and `docs/standby-switchover.md`. Test-and-validate only: nothing under `docs/` or `mkdocs-base.yml` was changed.

No real password appears in this report. Secrets and role verifiers are compared through the first 12 hex characters of their SHA-256 (or MD5 for `pg_authid`) fingerprints. For logins, the report records only whether they worked.

## Environment

| Item | Value |
|---|---|
| Date | 2026-10-23, 13:52–14:40 UTC |
| Kubernetes | GKE v1.35.8-gke.1439001, context `gke_cloud-dev-112233_us-central1-f_nastena-1` |
| Nodes at start | **4** (`d1hb`, `j335`, `k4fv`, `w2rz`, `n1-standard-4`, preemptible), matching the baseline. No nodes were added |
| Operator | 3.1.0 (`deploy/crd.yaml`, `rbac.yaml`, `operator.yaml` from tag `v3.1.0`), namespace-scoped, one per site. The code paths named in the task are identical in v3.1.0 and `d6b27f8`: `git diff v3.1.0 d6b27f8 -- internal/controller/postgrescluster/postgres.go internal/postgres/users.go` is empty |
| PostgreSQL | `percona-distribution-postgresql:18.6.1-3`, pgBouncer `1.25.2-8`, pgBackRest `2.59.1-2` |
| Sites | Main = cluster `main` in namespace `main-pg`; DR = cluster `dr` in namespace `dr-pg`, as in the doc examples. One instance and one pgBouncer per site |
| Shared repo | SeaweedFS S3 (`pgk8s-eval/lab/manifests/s3-seaweedfs.yaml`) in `pw-s3`, a fresh `repo1-path` per pair (`/pgbackrest/pw/runN`) |
| Client | Pod `client` in `pg-client`. Every login runs over the network: `psql "host=<svc> user=<u> dbname=<db> sslmode=require"` |
| Users | `spec.users: [{name: app1, databases: [app1db]}]` on both sites (except U2b). No Secret was copied between sites unless a test says so. Each site has `repos[0].schedules.full` set |

Cluster spec used for both sites (DR adds `standby: {enabled: true, repoName: repo1}`):

```yaml
spec:
  crVersion: 3.1.0
  image: docker.io/percona/percona-distribution-postgresql:18.6.1-3
  postgresVersion: 18
  users: [{name: app1, databases: [app1db]}]
  instances: [{name: instance1, replicas: 1, dataVolumeClaimSpec: {...2Gi}}]
  proxy: {pgBouncer: {replicas: 1, image: docker.io/percona/percona-pgbouncer:1.25.2-8}}
  backups:
    pgbackrest:
      configuration: [{secret: {name: s3-creds}}]
      global: {repo1-path: /pgbackrest/pw/runN, repo1-s3-uri-style: path, repo1-storage-port: "9000", repo1-storage-verify-tls: "n"}
      repos: [{name: repo1, schedules: {full: "0 3 * * *"}, s3: {bucket: percona, endpoint: s3.pw-s3.svc, region: us-east-1}}]
```

### Which users exist

With `spec.users` set, the Operator creates **no** default user named after the cluster, and no Secret for `postgres`:

```
$ kubectl -n main-pg get secret | grep -E "pguser|pgbouncer"
main-pgbouncer      Opaque   7
main-pguser-app1    Opaque   12

$ psql -c "select rolname, rolcanlogin, rolsuper, (rolpassword is not null) from pg_authid where rolname !~ '^pg_'"
_crunchypgbouncer|t|f|t
_crunchyrepl|t|f|f
app1|t|f|t
postgres|t|t|f
```

Source: the upstream layer adds the `<cluster-name>` user only when `spec.users` is nil (`reconcilePostgresUserSecrets`). `postgres` has no password, so a network login as `postgres` fails on both sites in every phase (`password authentication failed for user "postgres"`). Promotion does not touch it. The default-user question was tested separately in U2b, on a pair with no `spec.users`.

## U1. Baseline before promotion

```
dr-pguser-app1 exists: secret/dr-pguser-app1        (created with the DR cluster, 24 s after kubectl apply)
password fingerprint            main=9f2f0c9f0390  dr=cf164843da75
verifier fingerprint            main=3f8529f6b6e0  dr=99a126472306
pgbouncer-password fingerprint  main=6464c6a7d163  dr=f4faf7906f30
role app1 verifier in DB        main=3f8529f6b6e0  dr=3f8529f6b6e0     <- DR holds Main's verifier
DR in_recovery: t   usersRevision: main=b569d8b5c  dr=[]               <- DR never applied its users
```

Login matrix (from the client pod):

| Target | User / password | Result |
|---|---|---|
| DR direct (`dr-primary.dr-pg.svc`) | app1 / Main's | **OK**, `in_recovery=true` |
| DR direct | app1 / DR's own | **FAIL** `password authentication failed for user "app1"` |
| DR direct | `_crunchypgbouncer` / Main's | OK |
| DR direct | `_crunchypgbouncer` / DR's own | FAIL |
| DR pgBouncer (`dr-pgbouncer.dr-pg.svc`) | app1 / Main's | **FAIL** `password authentication failed for user "_crunchypgbouncer"` |
| DR pgBouncer | app1 / DR's own | FAIL (same) |
| Main direct | app1 / Main's | OK, `in_recovery=false` |
| Main direct | app1 / DR's | FAIL |
| Main pgBouncer | app1 / Main's | OK |

**Answers:**
- `dr-pguser-app1` exists while DR is a standby, with an Operator-generated password that differs from Main's.
- Main's app1 password works on DR (read-only), and DR's own password does not.
- DR's pgBouncer is unusable while DR is a standby, for every user. It authenticates to PostgreSQL as `_crunchypgbouncer` with DR's `dr-pgbouncer` Secret, but the role replicated from Main has Main's verifier.

## U2. Promote with differing Secrets

Procedure: the planned-swap steps without the password preparation.

```bash
LSN=$(kubectl -n main-pg exec <main pod> -c database -- psql -XAt -c "select pg_current_wal_lsn()")   # 0/5000108
kubectl -n main-pg patch pg main --type=merge -p '{"spec":{"standby":{"enabled":true,"repoName":"repo1"}}}'
# wait for pg_is_in_recovery() = t on Main, then pg_last_wal_replay_lsn() >= LSN on DR
kubectl -n dr-pg patch pg dr --type=merge -p '{"spec":{"standby":{"enabled":false}}}'     # T = 13:58:50 UTC
```

Login polling on DR after the patch (each line = a change):

```
+1s  pg_is_in_recovery()=f
+1s  direct app1/Main: OK in_recovery=true  | direct app1/DR: FAIL | bouncer app1/Main: FAIL | bouncer app1/DR: FAIL
+7s  direct app1/Main: FAIL password authentication failed | direct app1/DR: OK in_recovery=false | bouncer: FAIL | FAIL
+20s direct app1/Main: FAIL | direct app1/DR: OK | bouncer app1/Main: FAIL | bouncer app1/DR: OK
+27s direct app1/Main: FAIL | direct app1/DR: OK | bouncer app1/Main: FAIL SASL authentication failed | bouncer app1/DR: OK
```

```
usersRevision after: dr=[756b7d7994]   (before: empty)
role verifiers in DR DB now: app1=99a126472306 (Main secret 3f8529f6b6e0, DR secret 99a126472306)
                             _crunchypgbouncer=56344fb32957 (Main 228f6917a4e1, DR 56344fb32957)
```

The Operator does not log the SQL it executes for users at the default log level. No log line names the `ALTER ROLE`, and a `grep -iE "ALTER ROLE|revision|users"` over the 4 minutes around the change returned nothing. The only Operator-side evidence is `status.usersRevision` on the `postgrescluster` object changing from empty to `756b7d7994`.

**Result: the problem is real.** About 7 s after promotion, the Operator replaced app1's password with the one in `dr-pguser-app1`. From then on:
- applications using Main's credentials fail on DR, directly and through pgBouncer;
- DR's own Secret works.

The Operator also changes `_crunchypgbouncer` to DR's `dr-pgbouncer` password. That is what makes DR's pgBouncer work after +20 s. `postgres` is not in `spec.users` and was not changed: it still has no password, so network logins fail in every phase. `_crunchyrepl` uses certificate authentication and was not checked.

### U2b. Default user named after the cluster (no `spec.users`)

Fresh pair (`run3`) without `spec.users`: Main gets `main-pguser-main`, DR gets `dr-pguser-dr`.

```
Main roles:                 main=1f76ae94d9c8
DR roles (standby):         main=1f76ae94d9c8              databases: postgres,template1,template0,main
DR roles after promotion:   dr=42de414b4117 main=1f76ae94d9c8   databases: ...,main,dr
DR login  main / Main's main-pguser-main password: OK in_recovery=false
DR login  dr   / DR's dr-pguser-dr password:       OK in_recovery=false
DR pgBouncer  main / Main's password:              OK
```

On promotion, DR creates its own default user `dr` and database `dr`. The `main` role replicated from Main is **untouched**, and Main's password for `main` keeps working on DR. DR has no Secret for `main`, so it never manages that user.

## U3. Promote after following the doc's fix

Fresh pair (`run2`), DR schedule set to `*/1 * * * *` for U4. The doc commands, run literally:

```bash
PASSWORD=$(kubectl get secret main-pguser-app1 -n main-pg \
  -o jsonpath='{.data.password}' | base64 -d)

kubectl patch secret dr-pguser-app1 -n dr-pg \
  -p "{\"stringData\":{\"password\":\"${PASSWORD}\",\"verifier\":\"\"}}"
```

```
secret/dr-pguser-app1 patched
before: dr password=5ba83d00bd4f verifier=cdfc1f0e5669 | main password=ccbcdc55c1ab verifier=b60dae5d34da
immediately after: verifier length=0
+1s verifier regenerated: c4cb5d9352e4 (starts with SCRAM-SHA-256$...)
after: dr password=ccbcdc55c1ab ; same password as main: yes ; same verifier string as main: no
uri / jdbc-uri / pgbouncer-uri: contain Main's password = True
DR role app1 verifier in DB (standby) = b60dae5d34da  (unchanged, still Main's)
```

**The patch works on the existing Secret.** The Operator rebuilt `verifier` from the new password within 1–2 s (`generatePostgresUserSecret` regenerates the verifier when it is empty), and the `uri`, `jdbc-uri` and `pgbouncer-uri` keys were rebuilt too. The new verifier is a different string from Main's (new salt) for the same password, which is expected. While DR is a standby, both Main's password and DR's (now identical) password log in to DR directly.

Promotion: same commands as U2, T = 14:06:55 UTC.

```
+0s  pg_is_in_recovery()=f
+0s  direct app1/Main: OK in_recovery=true  | direct app1/DR: OK | bouncer app1/Main: FAIL | bouncer app1/DR: FAIL
+7s  direct app1/Main: OK in_recovery=false | direct app1/DR: OK | bouncer: FAIL | FAIL
+20s direct app1/Main: OK | direct app1/DR: OK | bouncer app1/Main: FAIL | bouncer app1/DR: OK in_recovery=false
+27s direct app1/Main: OK | direct app1/DR: OK | bouncer app1/Main: OK in_recovery=false | bouncer app1/DR: OK
usersRevision after: dr=[7dc8b457c]
role verifiers in DR DB now: app1=c4cb5d9352e4 (DR secret c4cb5d9352e4)
```

**Result: the fix works.** App1 logs in on the promoted DR with Main's password directly at every point, and through DR's pgBouncer from about +27 s. The pgBouncer path needs about 20–27 s after promotion for the `_crunchypgbouncer` change and pgBouncer's `server_login_retry` backoff. The `+20s` row, where pgBouncer accepted one password but not the other, is pgBouncer retry timing, not a password difference.

The doc's fallback ("If the DR Secret doesn't exist yet") was not needed: the Secret existed within about 1 s of creating the DR cluster.

## U4. Other claims

### Scheduled backups while standby

There are **no CronJobs** for scheduled backups in 3.1.0, on either site, with `schedules.full` set:

```
$ kubectl -n dr-pg get cronjob
No resources found in dr-pg namespace.
$ kubectl -n dr-pg get postgrescluster dr -o jsonpath='{.spec.backups.pgbackrest.repos[0].schedules}'
{}
```

The Percona layer removes the schedules from the upstream spec (`perconapgcluster_types.go`: `repo.BackupSchedules.Full = nil` …) and runs them in an Operator-internal cron (`percona/controller/pgcluster/schedule.go`, `robfig/cron`). The upstream `suspend` logic for standbys (`internal/controller/postgrescluster/pgbackrest.go:3520`) is therefore never used. Observed with `*/1 * * * *` on DR:

- **While standby:** the job fires every minute and skips. `ReadyForBackup` is `False / PGBackRestReplicaCreate`, and the Operator logs `ReadyForBackup condition is set to false. Can't start scheduled backup`. No `PerconaPGBackup` was created.
- **After promotion:** `ReadyForBackup: True AllConditionsAreTrue`. Scheduled backups ran (`dr-repo1-full-c6wsv Succeeded full 14:07:58Z` about 1 min after promotion, and `dr-repo1-full-pcbxx` a minute later), plus the automatic post-promotion `dr-backup-lnmk-fz77h incr`.

The behavior the doc describes is right (no scheduled backups while standby, they run after promotion). The mechanism is not a suspended CronJob.

### Leaving `standby.host` and `standby.repoName` after promotion

Tested on the streaming pair (U5a). The promotion patch was only `{"spec":{"standby":{"enabled":false}}}`:

```
spec.standby={"enabled":false,"host":"main-ha.main-pg.svc","port":5432,"repoName":"repo1"} state=ready
pg_is_in_recovery()=f, pg_stat_wal_receiver rows=0
patronictl show-config: no standby_cluster section
patronictl list: dr-instance1-9pjc-0 | Leader | running | 2
```

One Operator `ERROR` in 3 minutes: `reconcile logical replicas: update logical replica status: Operation cannot be fulfilled on perconapgclusters.pgv2.percona.com ...`. This is an optimistic-concurrency conflict that the Operator retries; it is not related to the standby options. **Confirmed.**

### "Wait until `ready` and `pg_is_in_recovery()` returns `f`"

| Run | `pg_is_in_recovery()` = `f` | `state` | Logins with DR Secrets effective (direct) | DR pgBouncer logins |
|---|---|---|---|---|
| U2 repo | +1 s | `ready` the whole time | +7 s | +20 s |
| U3 repo | +0 s | `ready` the whole time | +7 s (same password) | +27 s |
| U5a streaming | +1 s | `ready` the whole time | +12 s | broken (TLS, see U5) |
| U5b streaming | +1 s | `ready` the whole time | +12 s (same password) | broken (TLS) |

The cluster was `ready` before the patch (as a standby) and never left `ready`, so `ready` doesn't signal that promotion has finished. `pg_is_in_recovery()` returned `f` within about 1 s, the polling granularity. The Operator applies the DR user Secrets 7–12 s after that, and logins through pgBouncer need 20–30 s.

## U5. Streaming standby

Run. DR uses `standby: {enabled: true, repoName: repo1, host: main-ha.main-pg.svc, port: 5432}` and `secrets: {customTLSSecret: peer-cluster-cert, customReplicationTLSSecret: peer-replication-cert}`, which are copies of `main-cluster-cert` and `main-replication-cert` as in `docs/standby-streaming.md`. DR streams: `pg_stat_wal_receiver` → `streaming|main-ha.main-pg.svc`.

| Run | Before promotion | After promotion (direct) |
|---|---|---|
| U5a, differing Secrets | app1 / Main's: OK, app1 / DR's: FAIL | +12 s: app1 / Main's: **FAIL**, app1 / DR's: OK. `usersRevision` `[]` → `7f7f9977cd` |
| U5b, doc fix first | verifier regenerated after 2 s, same password as Main | app1 / Main's: **OK** and app1 / DR's: OK throughout. `usersRevision` `[]` → `599868558c` |

The password behavior is identical to the repo-based standby.

**DR's pgBouncer never works in this streaming setup**, before or after promotion, with any password:

```
WARNING TLS handshake error: name `dr-primary' not present in server certificate
LOG S-...: app1db/_crunchypgbouncer@...:5432 closing because: server conn crashed? (age=0s)
pgbouncer.ini: server_tls_sslmode = verify-full
```

The copied `main-cluster-cert` covers only Main's Service names. DR's PostgreSQL presents it, and DR's pgBouncer connects to `dr-primary` with `verify-full`, so hostname verification always fails. This is a `standby-streaming.md` problem rather than a password one. A fix such as certificates with SANs for both clusters, or a shared root CA (`customRootCATLSSecret`), was **not tested**.

## U6. Planned swap

### First reverse step (U3 pair, repo-based)

The U3 promotion *is* the first reverse step of `standby-switchover.md`:
- record LSN `0/6000000`;
- demote Main with `{"standby":{"enabled":true,"repoName":"repo1"}}`;
- wait for `t`, then for DR's replay ≥ LSN;
- promote DR.

App1 logged in on DR with Main's old password directly and through pgBouncer (U3 table).

As the doc says, the repo-based Main stayed on the old timeline (`Standby Leader | in archive recovery | 1`). It was rebuilt with the doc's "Recreate the instance" steps (delete PVC and Pod) and came back as `Standby Leader | in archive recovery | 2`.

### Swap back (U6)

Same procedure with the sites exchanged: demote DR, wait, Main replayed `0/E0000F8`, promote Main.

```
Main usersRevision before: 6fc7dc65d6   after: 6fc7dc65d6       <- unchanged: the Operator did not re-apply Main's users
Main DB app1 verifier=c4cb5d9352e4 (Main secret b60dae5d34da, DR secret c4cb5d9352e4)   <- still DR's
Main direct   app1 / Main pw   OK in_recovery=false     (works only because the passwords are now equal)
Main direct   _crunchypgbouncer / Main pw   FAIL ;  / DR pw   OK
Main pgBouncer  app1 / Main pw  FAIL password authentication failed for user "_crunchypgbouncer" (server_login_retry)
```

Main's pgBouncer stayed broken for the 4 minutes it was watched (`postgresRevision=794fcdc46c` unchanged).

The Operator caches a hash of the user SQL in `status.usersRevision`, and of the pgBouncer SQL in `status.proxy.pgBouncer.postgresRevision`. It re-runs the SQL only when the hash changes. Main's Secrets had not changed since Main was last primary, so promoting Main again re-applied nothing. App1 and `_crunchypgbouncer` keep the verifiers that DR wrote.

Workaround, tested: clear the verifiers so that the Operator regenerates them, the hash changes, and the SQL runs again:

```bash
kubectl -n main-pg patch secret main-pgbouncer -p '{"stringData":{"pgbouncer-verifier":""}}'
# +58s: Main pgBouncer app1 / Main pw: OK      postgresRevision -> 686f77655
kubectl -n main-pg patch secret main-pguser-app1 -p '{"stringData":{"verifier":""}}'
# usersRevision -> 85464cd998; Main DB app1 verifier = Main secret (51373ef5fd2c)
```

Afterwards all Main rows of the matrix were OK (app1 direct and through pgBouncer, `_crunchypgbouncer` with Main's password).

### U6b. Swap back when DR changed a password while primary

This was run on the U5b streaming pair to show the impact of the cached revision when the passwords differ. While DR was primary, `dr-pguser-app1` was given a new random password (redacted), which the Operator applied on DR. Then DR was demoted and Main promoted:

```
on DR before swap back: app1/new DR pw: OK   app1/Main pw: FAIL
Main usersRevision before promotion: 656dff9f76   after: 656dff9f76
on Main: app1 / Main's own Secret pw: FAIL password authentication failed for user "app1"
on Main: app1 / DR's new pw:          OK
on Main via pgBouncer: app1 / Main pw: FAIL password authentication failed for user "_crunchypgbouncer"
Main DB app1 verifier=e9d43fb6cb55  Main secret=94978f531b44  DR secret=e9d43fb6cb55
```

**After a swap back, the old Main does not restore passwords from its own Secrets.** Applications that use Main's Secret fail on Main until the Secrets are aligned again, for example with the verifier-clearing workaround above or by copying DR's password into Main's Secret.

## Validation table

| # | Doc claim | Status | Correct content / evidence |
|---|---|---|---|
| F1 | (failover) "A standby cluster replicates the users and their passwords from the Main site." | CONFIRMED | DR's `app1` verifier = Main's (U1) |
| F2 | "While the cluster is read-only, the Operator doesn't apply the passwords from the DR cluster's own user Secrets." | CONFIRMED | `usersRevision` empty on DR; DR's own password fails (U1). The Operator still **creates** `dr-pguser-app1` while standby |
| F3 | "When you promote the cluster, the Operator sets the password of every user in `spec.users` to the value in the DR Secret `<cluster-name>-pguser-<user-name>`." | CORRECTED | True for the first promotion: applied 7–12 s after promotion (U2, U5a). Additions: (1) it also sets `_crunchypgbouncer` to the DR `<cluster-name>-pgbouncer` Secret; (2) without `spec.users`, it creates the DR's own default user and database (`dr`) and leaves Main's default user (`main`) untouched; (3) it runs only when the hash of the user SQL differs from `status.usersRevision`, so a cluster promoted again after a swap back does **not** re-apply its Secrets (U6, U6b) |
| F4 | "If that value differs from the Main site password, applications that use the Main site credentials can't log in after the promotion." | CONFIRMED | U2: app1 with Main's password fails from +7 s, directly and through pgBouncer. U5a: same with streaming |
| F5 | "For each user that you define in `spec.users`, copy the password from the Main site Secret to the DR Secret." + the two commands | CONFIRMED | The patch works on the existing Secret; `verifier` is regenerated in 1–2 s, and `uri`/`jdbc-uri`/`pgbouncer-uri` are rebuilt; after promotion app1 works with Main's password directly and through pgBouncer (U3, U5b). Gap: it does not cover the pgBouncer user. That doesn't matter for the first promotion, but it does on swap back (S4) |
| F6 | "If the DR Secret doesn't exist yet, create it as described in Custom passwords." | UNVERIFIED | The situation didn't occur: the Operator created `dr-pguser-app1` within about 1 s of creating the DR cluster, also while standby |
| F7 | "Do this before you promote, and preferably when you set up the standby." | CONFIRMED | Patching while standby changes nothing in the DR database (the verifier stays Main's) and takes effect at promotion (U3) |
| P1 | "You can leave the other `standby` options, such as `host` and `repoName`, in the Custom Resource. The Operator ignores them when `enabled` is `false`." | CONFIRMED | U5a: `ready`, `f`, no WAL receiver, no `standby_cluster` in Patroni; the one Operator error is an unrelated update conflict |
| P2 | "Wait until the cluster is `ready` and `SELECT pg_is_in_recovery();` returns `f`." | CORRECTED | `state` is already `ready` while standby and never leaves it, so it isn't a signal. `pg_is_in_recovery()` returns `f` within about 1 s. The DR user Secrets take effect 7–12 s later, and pgBouncer logins 20–30 s after promotion |
| P3 | "The Operator also resumes the scheduled backups, which are suspended while the cluster is a standby." | CONFIRMED (behavior) | No scheduled backups run while standby (the internal cron skips: `ReadyForBackup condition is set to false. Can't start scheduled backup`); they run after promotion (first one about 1 min later). Note for reviewers: 3.1.0 has no CronJobs and no `spec.suspend`; the schedule runs inside the Operator |
| S1 | (switchover, Before you start 3) "Make sure that the DR cluster has the same user passwords as the Main site. When the Operator promotes DR, it sets the password of each user in `spec.users` to the value in the DR user Secret. Follow Prepare the user passwords for each user." | CORRECTED | Correct for the first swap (U3). Missing: (1) the swap back. When the old Main is promoted again, the Operator doesn't re-apply Main's Secrets (`usersRevision` unchanged), so Main keeps whatever passwords DR set, including any password changed on DR while it was primary (U6b), and the `_crunchypgbouncer` password, which breaks Main's pgBouncer (U6). Before swapping back, make Main's Secrets match DR, or after promoting Main, clear `verifier` in each `main-pguser-<user>` Secret and `pgbouncer-verifier` in `main-pgbouncer` so the Operator re-applies them (tested, 58 s for pgBouncer). (2) DR's pgBouncer doesn't work while DR is a standby (U1) |
| S2 | (Before you start 2) "If you copied the Main site certificates to DR when you set up streaming, this is already true." | CONFIRMED with a side effect | Replication and the reverse direction work with copied certificates. But DR's pgBouncer can't connect to DR's PostgreSQL with Main's copied `customTLSSecret` (`name 'dr-primary' not present in server certificate`, `server_tls_sslmode = verify-full`), so pgBouncer on DR is broken in that setup (U5). This affects `standby-streaming.md`. The alternative setup was not tested |
| S3 | Swap steps 1–7 (record LSN before demotion, demote, wait for `t`, wait for replay ≥ LSN, promote, confirm `f`) | CONFIRMED | U3 (`0/6000000`), U6 (`0/E0000F8`), U5a/b; promotion `f` within about 1 s |
| S4 | "The roles are now reversed, and the swap back is the same procedure with the sites exchanged." | CORRECTED | The procedure works, but passwords and pgBouncer don't follow automatically: see S1. App1 still worked on Main after the swap back only because the passwords had been made identical in U3; Main's pgBouncer failed until `pgbouncer-verifier` was cleared |
| S5 | Repo-based: Main "stays on its old timeline and can't follow DR"; "Recreate the instance" (delete PVC and Pod) | CONFIRMED | U6: `Standby Leader | in archive recovery | 1` → after PVC and Pod delete `... | 2` |

## Summary

The password problem is real.
- **First promotion.** When a DR standby is promoted, the Operator runs `ALTER ROLE … PASSWORD <verifier>` from the DR cluster's own Secrets, 7–12 s after `pg_is_in_recovery()` turns `f`. It does this for every user in `spec.users`, and for the pgBouncer user `_crunchypgbouncer`. Applications that use Main's credentials then fail on DR, directly and through pgBouncer. This happens for both repo-based and streaming standbys.
- **Users not affected.** `postgres` is unaffected (not in `spec.users`; `_crunchyrepl` was not checked). When `spec.users` is unset, DR creates its own default user (`dr`) and leaves Main's (`main`) untouched.
- **The doc's fix works.** Copying the password into the DR Secret and clearing `verifier` works on the existing Secret, the Operator rebuilds the verifier in 1–2 s, and app1 keeps working on the promoted DR with Main's password, directly and through pgBouncer.
- **What the doc misses: the swap back.** The Operator re-applies users only when the hash of the SQL changes, so a cluster that was primary before and is promoted again keeps the passwords DR set. That includes `_crunchypgbouncer`, which leaves the old Main's pgBouncer broken until its Secrets' verifiers are cleared.
- **Unrelated finding.** The streaming setup in `standby-streaming.md` (copying Main's `cluster-cert` to DR) breaks DR's pgBouncer because of TLS hostname verification.
- **Scheduled backups.** They behave as the doc says, but through an Operator-internal cron, not suspended CronJobs.

## Cleanup and node count

No nodes were added. These resources were created by this test (13:52–13:54 UTC) and deleted at the end:

- Namespaces `main-pg`, `dr-pg`, `pw-s3`, `pg-client`, with everything in them: both Operators, the `main`/`dr` clusters (deleted first so finalizers clear), PVCs and their PVs, user Secrets (they survive cluster deletion and were deleted with the namespace), SeaweedFS with its data, and the client pod.
- CRDs from Operator v3.1.0 `deploy/crd.yaml`: `perconapgclusters`, `perconapgbackups`, `perconapgrestores`, `perconapgupgrades` (`pgv2.percona.com`), and `postgresclusters`, `pgupgrades`, `pgadmins`, `crunchybridgeclusters` (`upstream.pgv2.percona.com`).

**Final node count: 4** (`d1hb`, `j335`, `k4fv`, `w2rz`, all `Ready`), unchanged. After cleanup: 0 test namespaces, 0 Percona CRDs, 0 PVs left.
