# LDAP authentication

!!! admonition "Version added: [2.9.0](ReleaseNotes/Kubernetes-Operator-for-PostgreSQL-RN2.9.0.md)"

Authentication is the process of verifying a client identity. When a user connects to the database they must authenticate themselves against it before doing any actions or accessing any resources.

By default, Percona Operator for PostgreSQL authenticates users with a database password stored in Secrets. You can simplify and centralize user management by enabling **LDAP authentication** with Percona Operator for PostgreSQL. Instead of verifying the passwords locally, your PostgreSQL cluster delegates password verification to an LDAP server. The authorization is done based on the [roles and privileges that you define for users](users.md#adjusting-privileges) in the Custom Resource.

Using LDAP authentication means you can:

- Streamline account management: add, remove, or update users in one place
- Let users log in to the database with their existing organizational credentials and don't have to remember multiple logins
- Easily enforce centralized password policies and improve security

## How LDAP authentication works

1. You configure usernames and passwords in the LDAP server of your choice as Distinguished Names (DNs). You also specify these users in the Custom Resource.
2. You configure the authentication parameters in the Custom Resource. This instructs the Operator to generate authentication rules in `pg_hba.conf`.
3. A client connects to PostgreSQL with a username and a password.
4. The rules in `pg_hba.conf` determine which connections use LDAP.
5. PostgreSQL performs an LDAP bind to verify the user (using either [simple bind or search+bind](#bind-modes)).
6. If the bind succeeds, PostgreSQL grants access according to the privileges you defined for this user.

## Connection and bind modes

### Connection: plain LDAP vs LDAPS

You can connect to the LDAP server over an unencrypted or encrypted channel.

**Plain LDAP** sends credentials over the network without encryption. This connection is available at port `389`. Use it only in trusted networks, for example in development or when the LDAP server runs in the same cluster.

**LDAPS** uses TLS to encrypt traffic between PostgreSQL and the LDAP server. This connection is available at port `636`. Use LDAPS in production. You must provide the CA certificate that signed the LDAP server's certificate so PostgreSQL can verify the connection. You can generate these certificates via the cert-manager or use your custom ones.

!!! note "Encryption scope"

    LDAPS encrypts only the link between PostgreSQL and the LDAP server. To encrypt the connection between the client and PostgreSQL as well, configure [TLS for the database](TLS.md).

### Bind modes

PostgreSQL supports two ways to look up and verify users in LDAP.

**Simple bind** builds the user's Distinguished Name (DN) from a prefix and suffix you configure. The DN format is `<ldapprefix><username><ldapsuffix>`. For example, with `ldapprefix="uid="` and `ldapsuffix=",ou=users,dc=example,dc=com"`, user `alice` becomes `uid=alice,ou=users,dc=example,dc=com`. PostgreSQL then binds to LDAP as that DN with the password the client supplied. This is the simplest mode and works well when your LDAP structure is predictable.

**Search+bind** is more flexible. PostgreSQL first binds to LDAP (with a fixed service account or anonymously), searches for the user under a base DN using an attribute or filter, then re-binds as the found user with the client's password. Use search+bind when users live in different subtrees or when you need custom search logic (for example, matching by `uid` or `mail`). It requires `ldapbasedn` and either `ldapsearchattribute` or `ldapsearchfilter`; optionally `ldapbinddn` and `ldapbindpasswd` for the initial bind.

You cannot mix simple-bind options (`ldapprefix`, `ldapsuffix`) with search+bind options (`ldapbasedn`, `ldapsearchattribute`, etc.) in the same rule.

To learn more, see [PostgreSQL documentation :octicons-link-external-16:](https://www.postgresql.org/docs/current/auth-ldap.html)

## Username mapping

- PostgreSQL expects the LDAP username to match the PostgreSQL username.
- If a username contains special characters (such as `@`), escape them appropriately in both LDAP and PostgreSQL. For example, you can use `user@domain` directly if both LDAP and PostgreSQL support that character in usernames. For accurate rules on escaping special characters, refer to [RFC4514 :octicons-link-external-16:](https://datatracker.ietf.org/doc/html/rfc4514), [RFC4515 :octicons-link-external-16:](https://datatracker.ietf.org/doc/html/rfc4515), [RFC4516 :octicons-link-external-16:](https://datatracker.ietf.org/doc/html/rfc4516), or consult your LDAP server documentation.

## Next steps

[Configure LDAP authentication](ldap-setup.md){.md-button}
