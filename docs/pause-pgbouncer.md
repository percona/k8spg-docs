# Pause and resume pgBouncer connections

!!! note "Version added: [3.1.0](ReleaseNotes/Kubernetes-Operator-for-PostgreSQL-RN3.1.0.md)"

You can pause client traffic through `pgBouncer` without dropping application
connections. Active queries finish, `pgBouncer` disconnects from the server and queues new client connections until you resume. 

## When to pause `pgBouncer`

* **Database restarts**: Restart PostgreSQL without forcing clients to reconnect.
* **Planned maintenance**: Soften connection errors during a minor upgrade or a restart-required config change. Expect brief latency, not invisible downtime; long pauses can still hit app timeouts.
* **Planned switchovers**: Pause, change the primary, then resume to avoid a reconnect storm. For emergencies, rely on Patroni failover—PAUSE waits for in-flight work.
* **Drain traffic**: Stop backend work while client sessions stay open and queued.

## How it works

1. Set `spec.proxy.pgBouncer.paused` to `true` on the Custom Resource.
2. The Operator connects to each `pgBouncer` Pod as the internal admin user
   `_crunchypgbounceradmin` and issues `PAUSE`.
3. `pgBouncer` waits for current server connections to finish (per your pool
   mode), disconnects from PostgreSQL, and queues new client queries.
4. The Operator sets the `PGBouncerPaused` condition to `True`.
5. Perform the maintenance or switchover.
6. Set `paused` back to `false`. The Operator issues `RESUME` and removes
   the `PGBouncerPaused` condition.

If a `pgBouncer` Pod restarts while paused, a startup probe re-applies `PAUSE`
so the intended state survives restarts.

Note that with `spec.proxy.pgBouncer.paused` you control only the connection pooler. To pause the entire cluster, use the [cluster pause feature](pause.md).

## Before you start

* Check that pgBouncer is enabled with a non-zero replica
  count.
* By default, pgBouncer uses the `session` pooling mode. In `session` mode, `PAUSE` waits until clients fully disconnect, which may significantly delay or even block the pause operation. Change the pooling mode from session to `transaction` or `statement` by setting the `spec.proxy.pgBouncer.config.global.pool_mode` option in the Custom Resource.

* Keep the paused window short. Queued clients still observe latency, and
  client-side timeouts still apply.

## Pause pgBouncer

For the following steps, the cluster name is `cluster1`. Replace the
`<namespace>` placeholder with your value.

1. Confirm that pgBouncer Pods are ready:

    ```bash
    kubectl get pg cluster1 -n <namespace> \
      -o jsonpath='{.status.pgbouncer.ready}/{.status.pgbouncer.size}{"\n"}'
    ```

2. Set `proxy.pgBouncer.paused` to `true`:

    === "Patch running cluster"

        ```bash
        kubectl -n <namespace> patch pg cluster1 --type=merge --patch '{
          "spec": {
            "proxy": {
              "pgBouncer": {
                "paused": true
              }
            }
          }
        }'
        ```

    === "Edit Custom Resource"

        1. Edit the deploy/cr.yaml manifest:
           
            ```yaml
            spec:
              proxy:
                pgBouncer:
                  paused: true
            ```

        2. Apply the change:

            ```bash
            kubectl apply -f deploy/cr.yaml -n <namespace>
            ```

3. Wait until the Operator reports that pgBouncer is paused:

    ```bash
    kubectl get pg cluster1 -n <namespace> \
      -o jsonpath='{range .status.conditions[?(@.type=="PGBouncerPaused")]}{.status}{"\n"}{.reason}{"\n"}{.message}{"\n"}{end}'
    ```

    ??? example "Sample output"

        ```{.text .no-copy}
        True
        Paused
        pgbouncer is paused
        ```

4. Run your maintenance, restart, or planned switchover.

## Resume pgBouncer

Set `proxy.pgBouncer.paused` back to `false`:

```bash
kubectl -n <namespace> patch pg cluster1 --type=merge --patch '{
  "spec": {
    "proxy": {
      "pgBouncer": {
        "paused": false
      }
    }
  }
}'
```

Confirm that the `PGBouncerPaused` condition is gone:

```bash
kubectl get pg cluster1 -n <namespace> -o yaml | grep -A3 PGBouncerPaused || true
```

After resume, queued client queries proceed against PostgreSQL again.

## Considerations

* Pausing pgBouncer does not pause the PostgreSQL cluster and does not stop Operator reconciliation. Use [cluster pause](pause.md) when you need that.
* The Operator manages the `_crunchypgbounceradmin` user and stores its password in the pgBouncer Secret under `pgbouncer-admin-password`. Do not reuse or override this reserved user. See [Users](users.md#system-users-for-pgbouncer).
* Do not leave pgBouncer paused longer than your applications can tolerate.
* If pgBouncer Pods are not ready, the Operator cannot complete pause or resume. Check Pod status before you start.
