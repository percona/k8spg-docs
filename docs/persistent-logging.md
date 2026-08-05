# Persistent logging

!!! admonition "Version added: [3.1.0](ReleaseNotes/Kubernetes-Operator-for-PostgreSQL-RN3.1.0.md)"

In a distributed Kubernetes environment, it is often difficult to debug issues because container logs are tied to the lifecycle of individual Pods. If a Pod fails and restarts, its logs in `stdout` and `stderr` may be lost, making it hard to identify the root cause.

Percona Operator for PostgreSQL addresses this with **persistent logging**, ensuring logs are stored persistently, independent of the Pods. This approach helps ensure that logs are available for review even after a Pod restarts.

The Operator uses [Fluent Bit :octicons-link-external-16:](https://fluentbit.io/), a lightweight log processor with versatile output plugins and forwarding features. Fluent Bit runs as a `logs` sidecar container on each PostgreSQL instance Pod. It tails:

* PostgreSQL server logs under `/pgdata/pgNN/log/` (for example `/pgdata/pg18/log/`) — both `*.log` and `*.csv` files
* pgBackRest client logs under `/pgdata/pgbackrest/log/`

By default, Fluent Bit ships collected records as JSON lines to standard output. You can view them with:

```bash
kubectl logs <instance-pod-name> -c logs -n <namespace>
```

You can additionally configure Fluent Bit outputs such as S3 or an OpenTelemetry (OTel) envelope and have the logs forwarded there. Refer to the [Customize Fluent Bit](#customize-fluent-bit) section for details.

Log collection **enabled by default only for new clusters**. After you upgrade your deployment from earlier versions, you must [enable log collector](#enable-log-collector) explicitly in the Custom Resource to use it. When enabled, the Operator also adds a `logrotate` sidecar that manages retention of the on-disk log files. See [Log rotation](log-rotation.md) for details.

## Enable log collector

Enable persistent logging with the `logcollector.enabled` key in the `deploy/cr.yaml` Custom Resource manifest:

```yaml
spec:
  logcollector:
    enabled: true
    image: docker.io/percona/fluentbit:{{logcollector}}
```

Apply the Custom Resource:

```bash
kubectl apply -f deploy/cr.yaml -n <namespace>
```

## Customize Fluent Bit

You can further customize Fluent Bit to add filters, processors (for example OpenTelemetry envelope), or outputs such as S3. 

Add your configuration via the `logcollector.configuration` subsection. You must use the [Fluent Bit YAML configuration format :octicons-link-external-16:](https://docs.fluentbit.io/manual/administration/configuring-fluent-bit/yaml/). 

The following example adds a marker field and an S3 output for PostgreSQL logs:

```yaml
spec:
  logcollector:
    enabled: true
    image: docker.io/perconalab/fluentbit:main-logcollector
    configuration: |
      pipeline:
        filters:
          - name: record_modifier
            match: "*"
            record:
              - cluster_name cluster1
        outputs:
          - name: s3
            match: "*.postgres"
            bucket: my-logs-bucket
            region: us-east-1
            total_file_size: 1M
            upload_timeout: 15s
            use_put_object: on
            s3_key_format: /$TAG/%Y/%m/%d/%H-%M-%S-$UUID
            s3_key_format_tag_delimiters: .
    envFrom:
      - secretRef:
          name: my-log-collector-secret
    volumeMounts:
      - name: s3-ca
        mountPath: /etc/fluentbit/tls
        readOnly: true
    volumes:
      - name: s3-ca
        secret:
          secretName: my-s3-ca
```

Invalid custom Fluent Bit snippets are ignored at collector startup. When you change `logcollector.configuration` or log rotation settings, the Operator updates a configuration hash on the instance metadata and restarts the Pods to apply the new configuration.

