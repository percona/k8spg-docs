# Transport Layer Security (TLS)

The Percona Operator for PostgreSQL uses Transport Layer Security
(TLS) cryptographic protocol for the following types of communication:

* Internal - communication between PostgreSQL instances in the cluster
* External - communication between the client application and the cluster

The internal certificate is also used as an authorization method for PostgreSQL
Replica instances.

TLS security can be configured in several ways:

* the Operator can generate long-term certificates automatically at cluster
    creation time,
* the Operator can use a specifically installed *cert-manager*, which will
    automatically generate and renew short-term TLS certificates,
* you can also generate certificates manually.

The following subsections explain how to configure TLS security with the
Operator yourself, as well as how to temporarily disable it if needed.

## Install and use the *cert-manager*

### About the *cert-manager*

The [cert-manager](https://cert-manager.io/docs/) is a Kubernetes certificate
management controller which widely used to automate the management and issuance
of TLS certificates. It is community-driven, and open source.

When you have already installed *cert-manager* and deploy the Operator, the
Operator requests a certificate from the *cert-manager*. The *cert-manager* acts
as a self-signed issuer and generates certificates. The Percona Operator
self-signed issuer is local to the Operator namespace.

Self-signed issuer allows you to deploy and use the Operator without creating a
cluster issuer separately.

### Installation of the *cert-manager*

The steps to install the *cert-manager* are the following:

* create a namespace,
* disable resource validations on the cert-manager namespace,
* install the cert-manager.

The following commands perform all the needed actions:

``` {.bash data-prompt="$" }
$ kubectl create namespace cert-manager
$ kubectl label namespace cert-manager certmanager.k8s.io/disable-validation=true
$ kubectl apply -f https://github.com/jetstack/cert-manager/releases/download/v{{ certmanagerrecommended }}/cert-manager.yaml --validate=false
```

After the installation, you can verify the *cert-manager* by running the
following command:

``` {.bash data-prompt="$" }
$ kubectl get pods -n cert-manager
```

The result should display the *cert-manager* and webhook active and running:

``` {.text .no-copy}
NAME                                       READY   STATUS    RESTARTS   AGE
cert-manager-7d59dd4888-tmjqq              1/1     Running   0          3m8s
cert-manager-cainjector-85899d45d9-8ncw9   1/1     Running   0          3m8s
cert-manager-webhook-84fcdcd5d-697k4       1/1     Running   0          3m8s
```

Once you create the database with the Operator, it will automatically trigger
cert-manager to create certificates. Whenever you check certificates for expiration,
you will find that they are valid and short-term.

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

1. First, check the necessary secrets names (`cluster1-ssl` and
    `cluster1-ssl-internal` by default):

    ``` {.bash data-prompt="$" }
    $ kubectl get certificate
    ```

    You will have the following response:

    ``` {.text .no-copy}
    NAME                    READY   SECRET                  AGE
    cluster1-ssl            True    cluster1-ssl            49m
    cluster1-ssl-internal   True    cluster1-ssl-internal   49m
    ```

2. Optionally you can also check that the certificates issuer is up and running:

    ``` {.bash data-prompt="$" }
    $ kubectl get issuer
    ```

    The response should be as follows:

    ``` {.text .no-copy}
    NAME                READY   AGE
    cluster1-psmdb-ca   True    61s
    ```

3. Now use the following command to find out the certificates validity dates,
    substituting Secrets names if necessary:

    ``` {.bash data-prompt="$" }
    $ {
      kubectl get secret/cluster1-ssl-internal -o jsonpath='{.data.tls\.crt}' | base64 --decode | openssl x509 -noout -dates
      kubectl get secret/cluster1-ssl -o jsonpath='{.data.ca\.crt}' | base64 --decode | openssl x509 -noout -dates
      }
    ```

    The resulting output will be self-explanatory:

    ``` {.text .no-copy}
    notBefore=Apr 25 12:09:38 2022 GMT notAfter=Jul 24 12:09:38 2022 GMT
    notBefore=Apr 25 12:09:38 2022 GMT notAfter=Jul 24 12:09:38 2022 GMT
    ```

## Keep certificates after deleting the cluster

In case of cluster deletion, objects, created for SSL (Secret, certificate, and issuer) are not deleted by default.

If the user wants the cleanup of objects created for SSL, there is a [finalizers.percona.com/delete-ssl](operator.md#finalizers-delete-ssl) Custom Resource option, which can be set in `deploy/cr.yaml`: if this finalizer is set, the Operator will delete Secret, certificate and issuer after the cluster deletion event. 
