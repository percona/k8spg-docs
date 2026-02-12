# Define environment variables for cluster components

To pass environment variables into PostgreSQL, pgBackRest, or pgBouncer Pods, use the Custom Resource options described in [Custom Resource options](operator.md). For example:

- **PostgreSQL instances:** use `spec.instances[].env`, `spec.instances[].envFrom`, or reference a Secret via `spec.instances[].envVarsSecret`.
- **pgBackRest:** use the relevant `spec.backups.pgbackrest.*` or restore job options and any supported env or Secret references.
- **pgBouncer:** use `spec.proxy.pgbouncer.env`, `spec.proxy.pgbouncer.envFrom`, or `spec.proxy.pgbouncer.envVarsSecret`.

Sensitive values (passwords, API keys) should be stored in [Kubernetes Secrets](https://kubernetes.io/docs/concepts/configuration/secret/) and referenced by name in the cluster spec. For more options, see [Secrets options](secret-options.md) and the [Custom Resource options](operator.md) reference.
