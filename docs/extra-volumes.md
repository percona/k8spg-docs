# Mount extra volumes into PostgreSQL instances

You can mount additional Kubernetes volumes into the PostgreSQL container so every instance in the cluster sees the same files. Use this in scenarios when PostgreSQL needs files outside the data directory. For example:

* Add full-text search dictionaries, synonym maps, and thesaurus files under the server's shared data directory (SHAREDIR), in `tsearch_data`.

* Add other shared support files that you want to supply without rebuilding the PostgreSQL image

Use a ConfigMap, Secret, PersistentVolumeClaim, emptyDir, or another volume source that Kubernetes supports. The Operator mounts these volumes on the database container for the instance set that you configure. After you apply the change, the Operator
restarts PostgreSQL so the new mounts take effect.


## Add an extra volume

This example mounts full text search dictionary files from a ConfigMap
into `$SHAREDIR/tsearch_data` on every instance. The PostgreSQL version used in this example is 18.

1. Create a ConfigMap with your dictionary files. Keys become file names
   in the mounted directory:

    ```bash
    kubectl create configmap my-fts-dicts \
      --from-file=mydict.dict \
      --from-file=mydict.affix \
      --from-file=mydict.stop \
      -n <namespace>
    ```

2. Edit the `instances` section of your cluster Custom Resource. Add an
   `extraVolumes` entry with a unique name, a volume source, and at least
   one mount path.

    For Percona Distribution for PostgreSQL, `SHAREDIR` is
    `/usr/pgsql-<postgresVersion>/share`. Adjust the path to match your
    PostgreSQL major version:

    ```yaml
    spec:
      instances:
        - name: instance1
          extraVolumes:
            - name: fts-dicts
              volumeSource:
                configMap:
                  name: my-fts-dicts
              mounts:
                - mountPath: /usr/pgsql-18/share/tsearch_data/mydict.dict
                  subPath: mydict.dict
                  readOnly: true
                - mountPath: /usr/pgsql-18/share/tsearch_data/mydict.affix
                  subPath: mydict.affix
                  readOnly: true
                - mountPath: /usr/pgsql-18/share/tsearch_data/mydict.stop
                  subPath: mydict.stop
                  readOnly: true
    ```

    Use `subPath` when you want to add your dictionary files into `tsearch_data` without wiping what PostgreSQL already ships there. If you mount a volume on the whole `tsearch_data` directory, that volume replaces the directory contents for the container, so the built-in files are no longer available there.

3. Apply the Custom Resource:

    ```bash
    kubectl apply -f deploy/cr.yaml -n <namespace>
    ```

The Operator restarts PostgreSQL instance Pods to apply the new mounts.

## Verify the mount

Confirm that the volume appears on an instance Pod:

```bash
kubectl get pod -n <namespace> \
  -l postgres-operator.crunchydata.com/instance-set=instance1 \
  -o jsonpath='{.items[0].spec.volumes[*].name}{"\n"}'
```

The output includes your volume name (for example, `fts-dicts`).

Check that the files are present in the container:

```bash
kubectl exec -n <namespace> <instance-pod> -c database -- \
  ls -l /usr/pgsql-18/share/tsearch_data/mydict.dict
```

## Considerations

* Changing extraVolumes causes PostgreSQL to restart.
* Mounts apply to the PostgreSQL database container for that instance set. They do not mount into sidecar containers. For sidecar mounts, use the sidecar volume options instead. See [Add sidecar](sidecar.md) containers.
* Prefer `subPath` mounts when you add files next to the built-in `tsearch_data` content.