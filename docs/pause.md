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

