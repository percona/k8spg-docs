# Transport layer security (TLS)

The Percona Operator for PostgreSQL uses Transport Layer Security
(TLS) cryptographic protocol for the following types of communication:

* Internal - communication between PostgreSQL instances in the cluster
* External - communication between the client application and the cluster

The internal certificate is also used as an authorization method for PostgreSQL
Replica instances.

TLS security can be configured in following ways:

* the Operator can generate long-term certificates automatically at cluster
    creation time,
* you can generate certificates manually.

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

## Generate certificates manually

To use custom TLS certificates for a Postgres cluster, you will need to create a
Secret in the Namespace of your cluster that contains the TLS key (`tls.key`),
TLS certificate (`tls.crt`) and the CA certificate (`ca.crt`) to use. The Secret
should contain the following values:

```yaml
data:
  ca.crt: <value>
  tls.crt: <value>
  tls.key: <value>
```

You should generate certificates twice: one set is for external communications,
and another set is for internal ones. A secret created for the external use must
be added to the `secrets.customTLSSecret.name` field of your Custom Resource.
A certificate generated for internal communications must be added to the
 `secrets.customReplicationTLSSecret.name` field.

For example, if you have files named `ca.crt`, `hippo.key`, and `hippo.crt`
stored on your local machine, you could run the following command:

``` {.bash data-prompt="$"}
$ kubectl create secret generic -n postgres-operator hippo.tls \
  --from-file=ca.crt=ca.crt \
  --from-file=tls.key=hippo.key \
  --from-file=tls.crt=hippo.crt
```

Now you can add the custom TLS Secret name to the `secrets.customTLSSecret.name` 
field in your Rustom Resource:

```yaml
secrets:
  customTLSSecret:
    name: hippo.tls
```

Don't forget to apply changes as usual:

``` {.bash data-prompt="$"}
$ kubectl apply -f deploy/cr.yaml
```

## Check your certificates for expiration

1. First, check the necessary secrets names (`cluster1-cluster-cert` and
    `cluster1-replication-cert` by default):

    ``` {.bash data-prompt="$" }
    $ kubectl get secrets
    ```

    You will have the following response:

    ``` {.text .no-copy}
    NAME                            TYPE     DATA   AGE
    cluster1-cluster-cert           Opaque   3      11m
    ...
    cluster1-replication-cert       Opaque   3      11m
    ...

    ```

2. Now use the following command to find out the certificates validity dates,
    substituting Secrets names if necessary:

    ``` {.bash data-prompt="$" }
    $ {
      kubectl get secret/cluster1-replication-cert -o jsonpath='{.data.tls\.crt}' | base64 --decode | openssl x509 -noout -dates
      kubectl get secret/cluster1-cluster-cert -o jsonpath='{.data.ca\.crt}' | base64 --decode | openssl x509 -noout -dates
      }
    ```

    The resulting output will be self-explanatory:

    ``` {.text .no-copy}
    notBefore=Jun 28 10:20:19 2023 GMT
    notAfter=Jun 27 11:20:19 2024 GMT
    notBefore=Jun 28 10:20:18 2023 GMT
    notAfter=Jun 25 11:20:18 2033 GMT
    ```

## Keep certificates after deleting the cluster

In case of cluster deletion, objects, created for SSL (Secret, certificate, and issuer) are not deleted by default.

If the user wants the cleanup of objects created for SSL, there is a [finalizers.percona.com/delete-ssl](operator.md#finalizers-delete-ssl) Custom Resource option, which can be set in `deploy/cr.yaml`: if this finalizer is set, the Operator will delete Secret, certificate and issuer after the cluster deletion event. 
