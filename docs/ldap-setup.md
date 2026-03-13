# Configure LDAP authentication

This document walks you through setting up LDAP authentication in your PostgreSQL cluster managed by the Operator. For more information about LDAP authentication, how it works and why you need it, see [LDAP authentication overview](ldap.md).

## Assumptions

1. To enable LDAP authentication, you must configure two components: an LDAP server and the Percona Operator for PostgreSQL.

   The installation and initial setup of the LDAP server are outside the scope of this document. We assume your LDAP server is already running and accessible to the Operator over the network.

2. This guide assumes you are familiar with your LDAP server’s schema.

3. The examples in this document use [OpenLDAP :octicons-external-link-16:](https://www.openldap.org/) as the LDAP server. If you are using Active Directory, please refer to their [official documentation](https://learn.microsoft.com/en-us/previous-versions/windows/desktop/ldap/distinguished-names) for user and group configuration.
4. This example setup uses [Simple bind](ldap.md#bind-modes) mode and the bind user DN `cn=admin,dc=ldap,dc=local`. Make sure to add your own bind user and use it in the commands shown later in this document.

## Prerequisites

Before configuring LDAP authentication, ensure you have:

- A running LDAP server (e.g., OpenLDAP, Active Directory) reachable from the PostgreSQL Pods
- LDAP server hostname or IP and port: `389` for plain LDAP, `636` for LDAPS
- For LDAPS: the CA certificate that signed the LDAP server's TLS certificate

!!! important "LDAPS certificate hostname"

    For LDAPS, the LDAP server certificate must match the hostname that you will specify in the `ldapserver` option in the Custom Resource (either `commonName` or a Subject Alternative Name). If it does not match, PostgreSQL will reject the connection.

Clone the repository, because you will need to modify the default configuration in the cluster Custom Resource:

```bash
git clone -b v{{release}} https://github.com/percona/percona-postgresql-operator
```

## Configure the OpenLDAP server

Add users to your LDAP directory. To do that, use LDIF (LDAP Data Interchange Format) files. LDIF is a standard plain-text format for representing LDAP entries and operations. You create LDIF files to define new users, groups, or other LDAP directory entries, and then apply them to your directory using LDAP utilities like `ldapadd`. LDIF can describe any LDAP entry or modification, making it essential for managing your LDAP Data Information Tree (DIT).

Add the following LDIF portions to your OpenLDAP server. This creates:

- `ou=perconadba,dc=ldap,dc=local` — This is an **organizational unit (OU)** entry in your LDAP directory. An OU acts like a folder or grouping mechanism to organize related LDAP objects, such as users. In this example, "perconadba" is the group under which users will be organized.

- `uid=percona,ou=perconadba,dc=ldap,dc=local` — This is a **user entry** in LDAP, representing the "percona" user. It belongs to the organizational unit "perconadba". This entry will store information like username, password, and other user attributes. This is the account PostgreSQL will try to authenticate against when the client connects using the "percona" username.
- `cn=admin,ou=perconadba,dc=ldap,dc=local` — This is a **group entry** in LDAP, representing a group named "admin" within the organizational unit "perconadba". This entry groups together related users, in this case adding the user `uid=percona,ou=perconadba,dc=ldap,dc=local` as a member. Groups like this can be used to assign roles or manage access collectively within LDAP.

Use the `ldapadd` command to add this structure. Use your LDAP server hostname and your bind user DN and password in the following command:

```bash
ldapadd -x -H ldap://<ldap-server-hostname>:389 -D "cn=admin,dc=ldap,dc=local" -w adminpassword <<EOF
dn: ou=perconadba,dc=ldap,dc=local
objectClass: organizationalUnit
ou: perconadba

dn: uid=percona,ou=perconadba,dc=ldap,dc=local
objectClass: inetOrgPerson
uid: percona
cn: percona
sn: percona
userPassword: mysecretpassw

dn: cn=admin,ou=perconadba,dc=ldap,dc=local
objectClass: groupOfUniqueNames
cn: admin
uniqueMember: uid=percona,ou=perconadba,dc=ldap,dc=local
EOF
```

Verify that the user was added successfully:

```bash
ldapsearch -x \
  -H ldap://<ldap-server-hostname>:389 \
  -D "cn=admin,dc=ldap,dc=local" \
  -w adminpassword \
  -b "ou=perconadba,dc=ldap,dc=local" \
  "(uid=percona)"
``` 

??? example "Expected output"

    ```{.text .no-copy}
    # LDAPv3
    # base <ou=perconadba,dc=ldap,dc=local> with scope subtree
    # filter: (uid=percona)
    # requesting: ALL
    #
    
    # percona, perconadba, ldap.local
    dn: uid=percona,ou=perconadba,dc=ldap,dc=local
    objectClass: inetOrgPerson
    uid: percona
    cn: percona
    sn: percona
    userPassword:: e1NTSEF9TG95OUgyK1BpU3JmbStZZ2Rpd21rYjJOajVzQ0NJYWs=
    
    # search result
    search: 2
    result: 0 Success
    
    # numResponses: 2
    # numEntries: 1
    ```

## Configure the Operator and PostgreSQL

### Plain LDAP 

Use plain LDAP only in trusted networks. In this connection mode, PostgreSQL connects to the LDAP server on port `389`.

1. Export the namespace where your cluster will be running as an environment variable:

    ```bash
    export NAMESPACE=<namespace>
    ```
    
2. Install the Operator deployment, following the steps from the [Quick install guide](kubectl.md)
3. Edit the Custom Resource manifest and specify the following configuration:
    
    * Add the same user to the Custom Resource manifest as you defined in your LDAP directory. Specify the privileges you want this user to have in the `spec.users` section of the manifest. In this example setup this is the user `percona`.
    * Add authentication rules in the `spec.authentication.rules` section. The Operator will create a rule in the `pg_hba.conf` file based on this data:

       * `connection` - set to `host`. 
       * `method` - set to `ldap`
       * `users` - add users that will authenticate using LDAP
       * `options.ldapserver` - the hostname of your LDAP server
       - `options.ldapport` - the port to connect to. Set it to `389` for plain LDAP.
       - `ldapprefix` - The string to prepend the username when forming a DN during simple bind. In our example this is `"uid="`.
       - `ldapsuffix` - The string to append to the username when forming a DN to bind as. In our example this is `",ou=perconadba,dc=ldap,dc=local"`
       
       The example configuration looks like this:

       ```yaml
       spec:
         users:
           - name: percona
             databases:
               - percona 
         # The rest of your configuration
         authentication:
           rules:
             - connection: host
               method: ldap
               users:
                 - percona 
               options:
                 ldapport: 389
                 ldapprefix: uid=
                 ldapscheme: ldap
                 ldapserver: openldap
                 ldapsuffix: ",ou=perconadba,dc=ldap,dc=local"
       ```

4. Apply the configuration to create the cluster:
    
    ```bash
    kubectl apply -f deploy/cr.yaml -n <namespace>
    ```

### LDAPS (LDAP over TLS)

LDAPS encrypts traffic between PostgreSQL and the LDAP server. Use it in production.

For LDAPS connection, you must provide the LDAP server's certificate to PostgreSQL. To do that, create a Secret with this certificate.

1. Export the namespace where your cluster will be running as an environment variable:
    
    ```bash
    export NAMESPACE=<namespace>
    ```

2. Create a Secret with the LDAP server's CA certificate. Specify the path to the CA certificate:
    
    ```bash
    kubectl -n $NAMESPACE create secret generic ldap-ca \
    --from-file=ca.crt=/path/to/ca.crt
    ```

3. Install the Operator deployment, following the steps from the [Quick install guide](kubectl.md#)
4. Edit the Custom Resource manifest and specify the following configuration:
    
    - Add the same user to the Custom Resource manifest as you defined in your LDAP directory. Specify the privileges you want this user to have in the `spec.users` section of the manifest. In this example setup this is the user `percona`.
    - Add authentication rules in the `spec.authentication.rules` section. The Operator will create a rule in the `pg_hba.conf` file based on this data:

       - `connection` - set to `host`.
       - `method` - set to `ldap`
       - `users` - add users that will authenticate using LDAP
       - `options.ldapserver` - the hostname of your LDAP server
       - `options.ldapport` - the port to connect to. Set it to `636` for LDAP over TLS connection type.
       - `ldapprefix` - The string to prepend the username when forming a DN during simple bind. In our example this is `"uid="`.
       - `ldapsuffix` - The string to append to the username when forming a DN to bind as. In our example this is `",ou=perconadba,dc=ldap,dc=local"`

    - Reference the Secret with the LDAP Server CA certificate in the `config.files.secret` option. The Operator mounts the CA certificate at the path `/etc/postgres/ldap/ca.crt` and automatically sets the `LDAPTLS_CACERT` environment value to this path.

    This is the example configuration:

    ```yaml
    spec:
      users:
        - name: percona
          databases:
            - percona
    
      authentication:
        rules:
          - connection: host
            method: ldap
            users:
              - percona
            options:
              ldapscheme: ldaps
              ldapserver: openldap-tls
              ldapport: 636
              ldapprefix: "uid="
              ldapsuffix: ",ou=perconadba,dc=ldap,dc=local"
    
      config:
        files:
          - secret:
              name: ldap-ca
              items:
                - key: ca.crt
                  path: ldap/ca.crt
    ```

5. Apply the configuration:
    
    ```bash
    kubectl apply -f deploy/cr.yaml -n $NAMESPACE
    ```

## Verify LDAP authentication

To verify the LDAP authentication, let's do the following:

* Create a `pg-client` Pod
* Connect to PostgreSQL via `pgBouncer` as the user that has LDAP authentication configured (`percona` in our example)

Here are the steps:

1. List the services:
   
    ```bash
    kubectl get svc -n $NAMESPACE
    ```

    Look for the `<cluster-name>-pgbouncer` service.

2. Create a Pod where you start a container with Percona Distribution for PostgreSQL and establish a shell session inside:
    
    ```bash
    kubectl run -i --rm --tty pg-client --image=perconalab/percona-distribution-postgresql:18 --restart=Never  -- bash
    ```

3. Inside the Pod, connect to PostgreSQL:

    ```bash
    psql "postgres://percona@<cluster-name>-pgbouncer.<namespace>.svc:5432/percona"
    ```

    ??? example "Expected output"

        ```
        Password for user percona:
        ```

4. Specify the LDAP password for the user. 

    ??? example "Expected output"

        ```
        psql (18.3 - Percona Server for PostgreSQL 18.3.1)
        SSL connection (protocol: TLSv1.3, cipher: TLS_AES_256_GCM_SHA384, compression: off, ALPN: postgresql)
        Type "help" for help.
        
        percona=>
        ```

