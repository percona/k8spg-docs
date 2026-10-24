# Crunchy and Percona Custom Resource differences

Percona Operator for PostgreSQL is based on the Crunchy PostgreSQL Operator code, so most options of the Crunchy `PostgresCluster` Custom Resource exist in the Percona `PerconaPGCluster` Custom Resource with the same name. This page lists the options that differ. Use it when you convert a Crunchy manifest for a [migration](migrate-from-crunchy.md).

The comparison covers Crunchy PostgreSQL Operator 5.8 and 6.0 (`v1beta1` API) and Percona Operator for PostgreSQL 3.0.0 and 3.1.0. The Crunchy options are the same in 5.8 and 6.0.

## Options with a different name

| Crunchy `PostgresCluster` | Percona `PerconaPGCluster` | Notes |
| ------------------------- | -------------------------- | ----- |
| `spec.service` | `spec.expose` | The `type` and `nodePort` options are the same. Crunchy sets annotations and labels under `metadata`, Percona sets them directly in `expose.annotations` and `expose.labels`. Percona adds `loadBalancerClass` and `loadBalancerSourceRanges`. Percona doesn't have `externalTrafficPolicy`, `internalTrafficPolicy`, `ipFamilies`, and `ipFamilyPolicy` |
| `spec.replicaService` | `spec.exposeReplicas` | Same differences as for `spec.service` |
| `spec.proxy.pgBouncer.service` | `spec.proxy.pgBouncer.expose` | Same differences as for `spec.service` |
| `spec.shutdown` | `spec.pause` | Both stop the cluster: the Operator scales PostgreSQL, pgBouncer, and the repository host to zero and keeps the Services and volumes. Setting the option back to `false` starts the cluster again |
| `spec.paused` | `spec.unmanaged` | Both stop the Operator from applying changes to the cluster. The running Pods aren't affected. Changes you make in the meantime are applied when you set the option back to `false` |
| `spec.customTLSSecret` | `spec.secrets.customTLSSecret` | |
| `spec.customReplicationTLSSecret` | `spec.secrets.customReplicationTLSSecret` | Percona also has `spec.secrets.customRootCATLSSecret` |
| `spec.instances[].volumes` | `spec.instances[].extraVolumes` | Available in Percona starting with version 3.1.0. See [Add extra volumes](extra-volumes.md) |
| `spec.backups.snapshots` | `spec.backups.volumeSnapshots` | See [PVC snapshots](backups-pvc-snapshots.md) |
| `spec.supplementalGroups` | `spec.instances[].securityContext.supplementalGroups` | Percona sets it per instance set in the Pod security context |
| Annotation `postgres-operator.crunchydata.com/autoCreateUserSchema` | `spec.autoCreateUserSchema` | Percona enables it by default. Set it to `false` to keep the Crunchy default behavior |

## Options without an equivalent

| Crunchy `PostgresCluster` | What to do in Percona |
| ------------------------- | --------------------- |
| `spec.monitoring.pgmonitor` | pgMonitor isn't available. Use [Percona Monitoring and Management](monitor-kubernetes.md) (`spec.pmm`) or a [`postgres_exporter` sidecar](postgres-exporter.md). The metrics and dashboards differ |
| `spec.userInterface` (pgAdmin) | Not available |
| `spec.instrumentation` (OpenTelemetry) | Not available. Starting with version 3.1.0, `spec.logcollector` collects PostgreSQL logs. See [persistent logging](persistent-logging.md) |
| `spec.postGISVersion` | Use the PostGIS image in `spec.image`. See [PostGIS](postgis.md) |
| `spec.disableDefaultPodScheduling` | Not available |
| `spec.instances[].dataVolumeClaimSpec.autoGrow` | Percona doesn't have the `autoGrow` tuning options (`trigger`, `maxGrow`). Automatic volume growth uses `resources.limits.storage` and the `AutoGrowVolumes` feature gate. See [Automated scaling with auto-growable disks](scaling-vertical.md#automated-scaling-with-auto-growable-disks) |
| `spec.backups.pgbackrest.log` | Not available |
| `spec.patroni.logging` | Not available |
| `spec.dataSource.pgbackrest.volumes` | Not available |

## Options with the same name

These options have the same name and structure in both Custom Resources: `authentication`, `config`, `databaseInitSQL`, `image`, `imagePullPolicy`, `imagePullSecrets`, `metadata`, `openshift`, `port`, `postgresVersion`, and `backups.pgbackrest.repos`.

These options have the same name, but some of their fields differ. Percona adds fields to them, and the fields that exist only in Crunchy are listed in the previous sections:

* `dataSource`
* `instances`
* `backups.pgbackrest`
* `backups.pgbackrest.manual`
* `proxy.pgBouncer`
* `patroni`
* `standby`
* `users`

Percona also has options that don't exist in Crunchy, such as `crVersion` (required), `extensions`, `pmm`, `tls`, `tlsOnly`, and `secrets`. See [Custom Resource options](operator.md).

## Differences in Crunchy PostgreSQL Operator 6.0

* **API version.** Crunchy 6.0 serves `postgres-operator.crunchydata.com/v1` in addition to `v1beta1`, and `kubectl` returns objects in `v1` by default. Crunchy 5.8 serves only `v1beta1`. The migration guides use `v1beta1`, which works with both versions.
* **PostgreSQL logs.** Crunchy 6.0 writes the PostgreSQL logs to `/pgdata/logs/postgres`.
* **Feature gates.** The Operators enable different feature gates by default:

    | Feature gate | Crunchy 5.8 | Crunchy 6.0 | Percona 3.0.0 and 3.1.0 |
    | ------------ | :---------: | :---------: | :---------------------: |
    | `AutoGrowVolumes` | | :white_check_mark: | |
    | `InstanceSidecars` | :white_check_mark: | :white_check_mark: | :white_check_mark: |
    | `TablespaceVolumes` | | | :white_check_mark: |
    | `PGBackrestSidecars`, `PGBouncerSidecars` | | | :white_check_mark: |

    If your Crunchy 6.0 cluster relies on automatic volume growth, enable the `AutoGrowVolumes` feature gate for the Percona Operator. See [Operator environment variables](env-var-operator.md).
