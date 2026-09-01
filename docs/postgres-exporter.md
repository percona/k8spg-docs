# Expose Prometheus metrics using postgres_exporter

You can expose PostgreSQL metrics in Prometheus format by running
[postgres_exporter :octicons-link-external-16:](https://github.com/prometheus-community/postgres_exporter)
as a sidecar container in each PostgreSQL instance Pod. Prometheus or another
Prometheus-compatible scraper then collects those metrics from the `/metrics` endpoint on port `9187`.

This setup is an alternative to [Percona Monitoring and Management (PMM)](monitoring.md).
Use it when you already scrape targets with Prometheus and want PostgreSQL
metrics in the same pipeline.

The Operator does not deploy `postgres_exporter` for you. You add it as a
[custom sidecar](sidecar.md), then create a Service so Prometheus can discover
the endpoints. You configure the scrape job in your Prometheus stack, not in the
Operator Custom Resource.

## How the setup works

Each PostgreSQL instance Pod gets a `postgres_exporter` sidecar. Containers in a
Pod share a network namespace, so the exporter connects to PostgreSQL on
`localhost:5432` and serves the `/metrics` endpoint on port `9187`.

Prometheus runs outside the Pod, so it cannot scrape `localhost:9187`. It
reaches the exporter only through a Kubernetes Service.

The Services that the Operator creates expose PostgreSQL on port `5432` only.
They do not include sidecar ports. You create a headless Service on port `9187`
so Prometheus can discover every instance Pod and scrape its exporter, instead
of load-balancing to a single Pod.


## Prerequisites

Before you start, check that you have the following:

* A running Percona Distribution for PostgreSQL cluster. This document uses the
  default cluster name `cluster1`.
* A Prometheus or Prometheus-compatible scraper. You configure scrape settings
  there after the exporter is running.

Clone the Operator repository if you do not have the manifests locally:

```bash
git clone -b v{{ release }} https://github.com/percona/percona-postgresql-operator
cd percona-postgresql-operator
```

Export the namespace where your PostgreSQL cluster is running as an environment variable. Replace `<namespace>` with your value:

```bash
export NAMESPACE=<namespace>
```

This example setup uses `postgres_exporter` version 0.20.1. Replace it with your required version.

## Create a monitoring user

Create a dedicated PostgreSQL user for the exporter. Do not use the `postgres`
superuser for this purpose.

1. Add the user to the `spec.users` subsection in the `deploy/cr.yaml`
   configuration file. If you already have users in this list, keep those
   entries and add `pgexporter` next to them:

    ```yaml
    spec:
      users:
        - name: pgexporter
          databases:
            - postgres
    ```

2. Apply the Custom Resource:

    ```bash
    kubectl apply -f deploy/cr.yaml -n $NAMESPACE
    ```

    The Operator creates the Secret `cluster1-pguser-pgexporter` with the `user`
    and `password` keys. For more information about custom users, see
    [Users](users.md).

## Grant monitoring privileges

The `users.options` field accepts only `ALTER ROLE` attributes, such as
`SUPERUSER` or `CREATEDB`. It cannot grant the `pg_monitor` role. You must grant
that privilege yourself.

Connect to the primary instance as the `postgres` user and grant the privileges
that `postgres_exporter` needs.

1. Find the primary Pod:

    ```bash
    PRIMARY=$(kubectl get pod -n $NAMESPACE \
      --selector postgres-operator.crunchydata.com/cluster=cluster1,postgres-operator.crunchydata.com/role=primary \
      -o jsonpath='{.items[0].metadata.name}')
    ```


2. Grant `CONNECT` on the `postgres` database and the `pg_monitor` role:

    ```bash
    kubectl exec -n $NAMESPACE $PRIMARY -c database -- \
      psql -c "GRANT CONNECT ON DATABASE postgres TO pgexporter;"

    kubectl exec -n $NAMESPACE $PRIMARY -c database -- \
      psql -c "GRANT pg_monitor TO pgexporter;"
    ```

!!! note

    For a new cluster, you can put these `GRANT` statements in
    [initialization SQL](initsql.md) instead of running them by hand.

## Add the postgres_exporter sidecar

Add the exporter to the PostgreSQL instance Pods in the Custom Resource.

This example setup uses `prometheus_exporter` version 0.20.1. Replace it with your required version.

1. Edit the `instances` subsection in `deploy/cr.yaml`. Specify the sidecar
   image, the metrics port, and the connection settings. Read the user name and
   password from the Secret that the Operator created for `pgexporter`:

    ```yaml
    spec:
      instances:
      - name: instance1
        replicas: 3
        metadata:
          labels:
            postgres-exporter: "true"
        sidecars:
        - name: postgres-exporter
          image: quay.io/prometheuscommunity/postgres-exporter:v0.20.1
          ports:
            - name: metrics
              containerPort: 9187
              protocol: TCP
          env:
            - name: DATA_SOURCE_URI
              value: "localhost:5432/postgres?sslmode=require"
            - name: DATA_SOURCE_USER
              valueFrom:
                secretKeyRef:
                  name: cluster1-pguser-pgexporter
                  key: user
            - name: DATA_SOURCE_PASS
              valueFrom:
                secretKeyRef:
                  name: cluster1-pguser-pgexporter
                  key: password
          resources:
            requests:
              cpu: 50m
              memory: 64Mi
            limits:
              cpu: 200m
              memory: 128Mi
    ```

    The label `postgres-exporter: "true"` marks instance Pods so that the
    headless Service can select them later.

    The image entrypoint starts `postgres_exporter`. You do not need a custom
    `command`. You can use another tag from the
    [postgres_exporter releases :octicons-link-external-16:](https://github.com/prometheus-community/postgres_exporter/releases).

    `sslmode=require` matches the Operator default, which encrypts PostgreSQL
    connections with TLS.

    Do not reuse the names of [predefined containers](sidecar.md#using-sidecar-containers) for the sidecar. If you also run PMM, do not
    name this sidecar `pmm-client`.

    Find additional sidecar options in the
    [Custom Resource options reference](operator.md#instancessidecars-subsection)
    and the
    [Kubernetes Workload API reference :octicons-link-external-16:](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.30/#container-v1-core).

2. Apply the Custom Resource and wait until the instance Pods roll out:

    ```bash
    kubectl apply -f deploy/cr.yaml -n $NAMESPACE
    kubectl get pods -n $NAMESPACE \
      -l postgres-operator.crunchydata.com/cluster=cluster1
    ```

!!! note

    To avoid putting the password in an environment variable, mount the user
    Secret as a volume and set the `DATA_SOURCE_PASS_FILE` variable to the
    mounted file path. See the
    [postgres_exporter documentation :octicons-link-external-16:](https://github.com/prometheus-community/postgres_exporter#quick-start)
    for details.

## Verify that the exporter is running

Confirm that the sidecar is up and that it can reach PostgreSQL.

1. Find a Pod name and port-forward the metrics port to your machine:

    ```bash
    kubectl port-forward -n $NAMESPACE $PRIMARY 9187:9187
    ```

2. In another terminal, request the metrics endpoint:

    ```bash
    curl -s http://127.0.0.1:9187/metrics | grep '^pg_up'
    ```

    ??? example "Expected output"

        ```{.text .no-copy}
        # HELP pg_up Whether the last scrape of metrics from PostgreSQL was able to connect to the server (1 for yes, 0 for no).
        # TYPE pg_up gauge
        pg_up 1
        ```

    `pg_up 1` means that the exporter connected to PostgreSQL. `pg_up 0` means
    that the scrape ran but the database connection failed.

3. Check that database metrics are present:

    ```bash
    curl -s http://127.0.0.1:9187/metrics | grep '^pg_stat_database_numbackends'
    ```

    ??? example "Expected output"

        ```{.text .no-copy}
        pg_stat_database_numbackends{datid="1",datname="template1"} 0
        pg_stat_database_numbackends{datid="16410",datname="cluster1"} 0
        pg_stat_database_numbackends{datid="16447",datname="mydata"} 0
        pg_stat_database_numbackends{datid="4",datname="template0"} 0
        pg_stat_database_numbackends{datid="5",datname="postgres"} 4
        ```

    You see one series per database. A non-zero value on `postgres` is expected
    because the exporter and some Operator components connect to that database.
    Counters at `0` are normal on an idle cluster.

If `pg_up` is `0`, check the sidecar logs:

```bash
kubectl logs -n $NAMESPACE $PRIMARY -c postgres-exporter
```

A common cause is TLS. If the log says that SSL is not allowed, change
`DATA_SOURCE_URI` to `localhost:5432/postgres?sslmode=disable`. If certificate
verification fails, keep `sslmode=require`. Do not use `verify-full` unless you
also mount the cluster CA certificate into the sidecar.

## Create a headless Service for scrape discovery

The Operator does not add sidecar ports to its Services. Create a headless
Service so that Prometheus can reach port `9187` on every instance Pod.

A `ClusterIP` Service has one virtual IP and load-balances to a single Pod. That
is wrong for metrics: you would scrape a random instance and miss the others. A
headless Service (`clusterIP: None`) has no virtual IP. Kubernetes still creates
an Endpoint for every matching Pod, and Prometheus scrapes each Pod IP.

1. Create the Service manifest. If you use a different cluster name, replace `cluster1` with your value:

    ```yaml title="postgres-exporter-service.yaml"
    apiVersion: v1
    kind: Service
    metadata:
      name: cluster1-postgres-exporter
      labels:
        app.kubernetes.io/name: postgres-exporter
        app.kubernetes.io/instance: cluster1
    spec:
      clusterIP: None
      selector:
        postgres-operator.crunchydata.com/cluster: cluster1
        postgres-exporter: "true"
      ports:
        - name: metrics
          port: 9187
          targetPort: metrics
    ```

2. Apply it in the same namespace as the cluster:

    ```bash
    kubectl apply -f postgres-exporter-service.yaml -n $NAMESPACE
    ```

With three replicas you get three scrape targets: one exporter per instance Pod,
each talking to its local PostgreSQL.

