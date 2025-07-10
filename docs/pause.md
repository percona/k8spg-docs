# Pause/resume and standby mode for a PostgreSQL cluster

## Pause and resume

Sometimes you may need to temporarily pause your cluster and restart it later, such as during maintenance.

The `deploy/cr.yaml` file contains a special `spec.pause` key for this.
Setting it to `true` gracefully stops the cluster:

```yaml
spec:
  .......
  pause: true
```

To start the cluster after it was paused, revert the `spec.pause`
key to `false`.

**Troubleshooting tip**

If you're pausing the cluster when there is a running backup, the Operator won't pause it for you. It will print a warning about running backups. In this case delete a running backup job and retry.

## Put in standby mode

You can also put the cluster into a [standby :octicons-link-external-16:](https://www.postgresql.org/docs/current/warm-standby.html) (read-only) mode instead of completely shutting it down. This is done by a special `spec.standby` key. Set it to `true` for read-only state. To resume the normal cluster operation, set it to `false`.

    ```yaml
    spec:
      .......
      standby: false
    ```
