> For the complete documentation index, see [llms.txt](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/llms.txt).

# Define environment variables for cluster components

To pass environment variables into PostgreSQL, pgBackRest, or pgBouncer Pods, use the Custom Resource options described in [Custom Resource options](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/operator.html). For example:

- **PostgreSQL instances:** use `spec.instances[].env`, `spec.instances[].envFrom`, or reference a Secret via `spec.instances[].envVarsSecret`.
- **pgBackRest:** use the relevant `spec.backups.pgbackrest.*` or restore job options and any supported env or Secret references.
- **pgBouncer:** use `spec.proxy.pgbouncer.env`, `spec.proxy.pgbouncer.envFrom`, or `spec.proxy.pgbouncer.envVarsSecret`.

Sensitive values (passwords, API keys) should be stored in [Kubernetes Secrets](https://kubernetes.io/docs/concepts/configuration/secret/) and referenced by name in the cluster spec. For more options, see [Secrets options](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/secret-options.html) and the [Custom Resource options](https://docs.percona.com/percona-operator-for-postgresql/3.1.0/operator.html) reference.
