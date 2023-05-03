# Transport Layer Security (TLS)

The Percona Operator for PostgreSQL uses Transport Layer Security
(TLS) cryptographic protocol for the following types of communication:

* Internal - communication between PostgreSQL instances in the cluster
* External - communication between the client application and the cluster

The internal certificate is also used as an authorization method for PostgreSQL
Replica instances.

TLS security can be configured in several ways:

* the Operator can generate certificates automatically at cluster creation time,
* you can also generate certificates manually.

The following subsections explain how to configure TLS security with the
Operator yourself, as well as how to temporarily disable it if needed.

## Allow the Operator to generate certificates automatically

The Operator is able to generate long-term certificates automatically and
turn on encryption at cluster creation time, if there are no certificate
secrets available. Just deploy your cluster as usual, with the
`kubectl apply -f deploy/cr.yaml` command, and certificates will be generated.

## Check connectivity to the cluster

You can check TLS communication with use of the `psql`, the standard
interactive terminal-based frontend to PostgreSQL. The following command will
spawn a new `pg-client` container, which includes needed command and can be
used for the check (use your real cluster name instead of the `<cluster-name>`
placeholder):

``` {.bash data-prompt="$" }
$ cat <<EOF | kubectl apply -f -
apiVersion: apps/v1
kind: Deployment
metadata:
  name: pg-client
spec:
  replicas: 1
  selector:
    matchLabels:
      name: pg-client
  template:
    metadata:
      labels:
        name: pg-client
    spec:
      containers:
        - name: pg-client
          image: perconalab/percona-distribution-postgresql:{{ postgresrecommended }}
          imagePullPolicy: Always
          command:
          - sleep
          args:
          - "100500"
          volumeMounts:
            - name: ca
              mountPath: "/tmp/tls"
      volumes:
      - name: ca
        secret:
          secretName: <cluster_name>-ssl-ca
          items:
          - key: ca.crt
            path: ca.crt
            mode: 0777
EOF
```

Now get shell access to the newly created container, and launch the PostgreSQL
interactive terminal to check connectivity over the encrypted channel (please
use real cluster-name, [PostgreSQL user login and password](users.md)):

``` {.bash data-prompt="$" data-prompt-second="[postgres@pg-client /]$"}
$ kubectl exec -it deployment/pg-client -- bash -il
[postgres@pg-client /]$ PGSSLMODE=verify-ca PGSSLROOTCERT=/tmp/tls/ca.crt psql postgres://<postgresql-user>:<postgresql-password>@<cluster-name>-pgbouncer.<namespace>.svc.cluster.local
```

Now you should see the prompt of PostgreSQL interactive terminal:

``` {.bash data-prompt="$" data-prompt-second="pgdb=>"}
$ psql ({{ postgresrecommended }})
Type "help" for help.
pgdb=>
```

## Keep certificates after deleting the cluster

In case of cluster deletion, objects, created for SSL (Secret, certificate, and issuer) are not deleted by default.

If the user wants the cleanup of objects created for SSL, there is a [finalizers.percona.com/delete-ssl](operator.md#finalizers-delete-ssl) Custom Resource option, which can be set in `deploy/cr.yaml`: if this finalizer is set, the Operator will delete Secret, certificate and issuer after the cluster deletion event.
