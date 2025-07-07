# Disable backups

The recommended approach to deploy and run the database is with the disaster recovery strategy in mind. Therefore, the Operator is designed and running with the backups enabled by default. 

There are some specific use cases when you may wish to run a database without enabled backups. Disabling backups should be a conscious decision based on your data's value and recoverability. These are example use cases where it is considered acceptable are when the data is fully disposable:

* Ephemeral development/testing environments: For clusters that are frequently torn down and rebuilt from application code or test data scripts.

* CI/CD pipeline jobs: For automated pipeline runs where the cluster's entire lifecycle is temporary and tied to a single job.

## Key considerations before disabling backups

Before you proceed with disabling backups, here's what you need to know and carefully assess:

1. Without backups you have no way to restore data. If by mistake you drop a table, that data is lost as you have no option to recover it.
2. You cannot clone a cluster when you [deploy a standby cluster for disaster recovery](standby-streaming.md). This is because cloning is based on restoring a backup on a new cluster.
3. When you run a cluster without backups, `pgBackRest` metrics are unavailable.

## Start a new cluster with disabled backups

To deploy a new cluster without backups, do the following:

1. Clone the Operator repository to be able to edit resource manifests.

    ```{.bash data-prompt="$" }
    $ git clone -b v{{ release }} https://github.com/percona/percona-postgresql-operator
    ``` 

2. Edit the `deploy/cr.yaml` Custom Resource and set the `backups.enabled` option to `false` 

    ```yaml
    spec:
      backups:
        enabled: false
    ```

3. Apply the Custom Resource to start the cluster creation.

    ```{.bash data-prompt="$"}
    $ kubectl apply -f deploy/cr.yaml -n <namespace>
    ```

### Disable backups for a running cluster

Before you start, read the [considerations](#key-considerations-before-disabling-backups) carefully. 

To disable backups for a running cluster, update the `deploy/cr.yaml` Custom Resource manifest with the following configuration:

* Set the `backups.enabled` option to `false`
* Add the annotation `pgv2.percona.com/authorizeBackupRemoval:"true"`

Since it is a running cluster, we will use the `kubectl patch` command to update its configuration:

```{.bash data-prompt="$"}
$ kubectl patch pg cluster1 --type merge \
  -p '{
    "metadata": {
      "annotations": {
        "pgv2.percona.com/authorizeBackupRemoval": "true"
      }
    },
    "spec": {
      "backups": {
        "enabled": false
      }
    }
  }' -n <namespace>
```

!!! warning

    After you apply this configuration and disable backups, the Operator deletes the `repo-host` PVC. Thus, all data that was stored in that PVC will be deleted too. The backups stored on the cloud backup storage remain. 

### Re-enable backups 

To re-enable backups for a running cluster, do the following:

1. Remove the annotation `pgv2.percona.com/authorizeBackupRemoval:"true"`

    ```{.bash data-prompt="$"}
    $ kubectl annotate pg cluster1 pgv2.percona.com/authorizeBackupRemoval-
    ```

2. Apply the patch to your running cluster and enable backups:

    ```{.bash data-prompt="$"}
    $ kubectl patch pg cluster1 --type merge \
      -p '{
        "spec": {
          "backups": {
            "enabled": true
          }
        }
      }'
    ```

