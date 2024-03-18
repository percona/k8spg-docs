# Pause/resume PostgreSQL cluster

There may be external situations when it is needed to pause your
Cluster for a while and then start it back up (some works related to
the maintenance of the enterprise infrastructure, etc.).

The `deploy/cr.yaml` file contains a special `spec.pause` key for this.
Setting it to `true` gracefully stops the cluster:

```yaml
spec:
  .......
  pause: true
```

To start the cluster after it was paused just revert the `spec.pause`
key to `false`.

!!! note

    There is an option also to put the cluster into a [standby :material-arrow-top-right:](https://www.postgresql.org/docs/12/warm-standby.html)
    (read-only) mode instead of completely shutting it down. This is done by a
    special `spec.standby` key, which should be set to `true` for read-only
    state or should be set to `false` for normal cluster operation:

    ```yaml
    spec:
      .......
      standby: false
    ```
