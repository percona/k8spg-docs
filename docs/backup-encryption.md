# Configure backup encryption

Backup encryption is a security best practice that helps protect your organization's confidential information and prevents unauthorized access.

The pgBackRest tool used by the Operator allows encrypting backups using AES-256
encryption. The approach is **repository-based**: pgBackRest encrypts the whole
repository where it stores backups. Encryption is automatically enabled if a
user-supplied encryption key was passed to pgBackRest with the
`-repo-cypher-pass` option *when configuring the backup storage*.

<i warning>:material-alert: Limitation:</i> You cannot change encryption settings after the backups are established. Create a new repository to enable encryption or change the encryption key.

This document describes how to configure backup encryption.

## Prerequisites

So, you need the encryption key to encrypt backups. 
You should use a long, random encryption key. For example,
you can generate it using OpenSSL as follows:

```{.bash data-prompt="$"}
$ openssl rand -base64 48
```

## Configure backup storage

You can follow the general [backup storage configuration](backups-storage.md)
instruction. The only difference is one of the initial steps - the one where you encode your cloud credentials and the pgBackRest repo name to be used for backups.
Here you should also add your backup encryption key to the `repo2-cipher-pass` option and encode it together with the storage credentials
and the pgBackRest repository name. The following example shows how this can be done for S3-compatible storage (other cloud storages are configured similarly).

1. Encode the storage configuration file.

    === ":simple-linux: Linux"         

          ``` {.bash data-prompt="$" }
          $ cat <<EOF | base64 --wrap=0
          [global]
          repo2-s3-key=<YOUR_AWS_S3_KEY>
          repo2-s3-key-secret=<YOUR_AWS_S3_KEY_SECRET>
          repo2-cipher-pass=<YOUR_ENCRYPTION_KEY>
          EOF
          ```         

    === ":simple-apple: macOS"         

         ``` {.bash data-prompt="$" }
         $ cat <<EOF | base64
         [global]
         repo2-s3-key=<YOUR_AWS_S3_KEY>
         repo2-s3-key-secret=<YOUR_AWS_S3_KEY_SECRET>
         repo2-cipher-pass=<YOUR_ENCRYPTION_KEY>
         EOF
         ``` 

2. Create the Secrets configuration file, the Secrets object and modify the cluster configuration as described in steps 2-5 of the [S3-compatible backup storage configuration](backups-storage.md). Follow the instructions relevant to the backup storage you are using. 

## Make a backup

[Make an on-demand backup](backups-ondemand.md){.md-button}
[Make a scheduled backup](backups-schedule.md){.md-button}
