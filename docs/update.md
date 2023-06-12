# Update Percona Operator for PostgreSQL

Percona Operator for PostgreSQL allows upgrades to newer versions.
This includes upgrades of the Operator itself, and upgrades of the Percona
Distribution for PostgreSQL.

## Upgrading the Operator

!!! note

    Only the incremental update to a nearest minor version of the Operator is
    supported. To update to a newer version, which differs from the current
    version by more than one, make several incremental updates sequentially.
    See [documentation archive](https://docs.percona.com/legacy-documentation/)
    for documentation on previous versions of the Operator.

Upgrading the Operator is similar to deploying a new Operator version, but you
should change the `DEPLOY_ACTION` option in the `deploy/operator.yaml` file
before applying it from `install` to `update`:

```yaml hl_lines="7 8"
...
  containers:
    - name: pgo-deploy
      image: percona/percona-postgresql-operator:1.4.0-pgo-deployer
      imagePullPolicy: Always
      env:
        - name: DEPLOY_ACTION
          value: update
...
```

You can automate this with the [yq tool](https://github.com/mikefarah/yq/#install) as
follows, assuming that you are upgrading to the Operator version {{ release }}:

``` {.bash data-prompt="$" }
$  curl -s https://raw.githubusercontent.com/percona/percona-postgresql-operator/v{{ release }}/deploy/operator.yaml | | yq w - "spec.template.spec.containers[0].env[3].value" "update" | kubectl apply -f -
$ kubectl wait --for=condition=Complete job/pgo-deploy --timeout=90s
```

!!! note

    The example above (and other examples in this document) uses [the yq version 3.4.0](https://github.com/mikefarah/yq/releases/tag/3.4.0). Note that the syntax for the yq command may be slightly different in other versions.

## Upgrading Percona Distribution for PostgreSQL

### Automatic upgrade

Starting from version 1.1.0, the Operator does fully automatic upgrades to
the newer versions of Percona PostgreSQL Cluster within the method named *Smart
Updates*.

The Operator will carry on upgrades according to the following algorithm.
It will query a special *Version Service* server at scheduled times to obtain
fresh information about version numbers and valid image paths needed for the
upgrade. If the current version should be upgraded, the Operator updates the CR
to reflect the new image paths and carries on sequential Pods deletion in a safe
order, allowing the cluster Pods to be re-deployed with the new image.

!!! note

    Version Service is in technical preview status and is disabled by
    default for the Operator version 1.1.0. Disabling Version Service
    makes Smart Updates rely on the `image` keys in the [Operator’s Custom Resource](operator.md#operator-custom-resource-options).

The upgrade details are set in the `upgradeOptions` section of the
`deploy/cr.yaml` configuration file. Make the following edits to configure
updates:

1. Set the `apply` option to one of the following values:

    * `recommended` - automatic upgrades will choose the most recent version
        of software flagged as recommended (for clusters created from scratch,
        the Percona Distribution for PostgreSQL 14 version will be selected
        instead of the Percona Distribution for PostgreSQL 13 or 12 version
        regardless of the image path; for already existing clusters, 14 vs. 13 or
        12 branch choice will be preserved),
    * `14-recommended`, `13-recommended`, `12-recommended` - same as above,
        but preserves specific major Percona Distribution for PostgreSQL version
        for newly provisioned clusters (for example, 14 will not be automatically
        used instead of 13),
    * `latest` - automatic upgrades will choose the most recent version of
        the software available,
    * `14-latest`, `13-latest`, `12-latest` - same as above, but preserves
        specific major Percona Distribution for PostgreSQL version for newly
        provisioned clusters (for example, 14 will not be automatically
        used instead of 13),
    * *version number* - specify the desired version explicitly,
    * `never` or `disabled` - disable automatic upgrades

    !!! note

        When automatic upgrades are disabled by the `apply` option,
        Smart Update functionality will continue working for changes triggered
        by other events, such as updating a ConfigMap, rotating a password, or
        changing resource values.

2. Make sure the `versionServiceEndpoint` key is set to a valid Version
    Server URL (otherwise Smart Updates will not occur).

    === "Percona’s Version Service"
         
         You can use the URL of the official Percona’s Version Service (default).
         Set `versionServiceEndpoint` to `https://check.percona.com`.

    === "Version Service inside your cluster"
        
        Alternatively, you can run Version Service inside your cluster. This
        can be done with the `kubectl` command as follows:

        ``` {.bash data-prompt="$" }
        $ kubectl run version-service --image=perconalab/version-service --env="SERVE_HTTP=true" --port 11000 --expose
        ```

    !!! note

        Version Service is never checked if automatic updates are disabled.
        If automatic updates are enabled, but Version Service URL can not be
        reached, upgrades will not occur.

3. Use the `schedule` option to specify the update checks time in CRON format.

    The following example sets the midnight update checks with the official
    Percona’s Version Service:

    ```yaml
    spec:
      upgradeOptions:
        apply: recommended
        versionServiceEndpoint: https://check.percona.com
        schedule: "0 4 * * *"
    ...
    ```

### Semi-automatic upgrade

Semi-automatic update of Percona Distribution for PostgreSQL should be used with the Operator
version 1.0.0 or earlier. For all newer versions, use automatic update
instead.

The following command will allow you to update the Operator to current version
(use the name of your cluster instead of the `<cluster-name>` placeholder).

``` {.bash data-prompt="$" }
$ kubectl patch perconapgcluster/<cluster-name> --type json -p '[{"op": "replace", "path": "/spec/backup/backrestRepoImage", "value": "percona/percona-postgresql-operator:{{ release }}-ppg14-pgbackrest-repo"},{"op":"replace","path":"/spec/backup/image","value":"percona/percona-postgresql-operator:{{ release }}-ppg13-pgbackrest"},{"op":"replace","path":"/spec/pgBadger/image","value":"percona/percona-postgresql-operator:{{ release }}-ppg14-pgbadger"},{"op":"replace","path":"/spec/pgBouncer/image","value":"percona/percona-postgresql-operator:{{ release }}-ppg14-pgbouncer"},{"op":"replace","path":"/spec/pgPrimary/image","value":"percona/percona-postgresql-operator:{{ release }}-ppg14-postgres-ha"},{"op":"replace","path":"/spec/userLabels/pgo-version","value":"v{{ release }}"},{"op":"replace","path":"/metadata/labels/pgo-version","value":"v{{ release }}"}]'
```

!!! note

    The above example is composed in asumption of using PostgreSQL 14 as
    a database management system. For PostgreSQL 13 you should change all
    occurrences of the `ppg14` substring to `ppg13`.

This will carry on the image and the cluster version update.
