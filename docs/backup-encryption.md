# Configure backup encryption

Backup encryption is a security best practice that helps protect your organization's confidential information and prevents unauthorized access.

You can encrypt the backups using  AES-256 encryption. `pgBackRest` encrypts the whole repository where it stores backups based on a user-provided encryption key passed within the `–repo-cypher-pass` flag.

<i warning>:material-alert: Limitation:</i> You cannot change encryption settings after the backups are established. To change the key or enable encryption requires creating a new repository.

This document describes how to configure backup encryption.

## Prerequisites

To configure backup encryption, you require the encryption key. You can generate it using OpenSSL. 

You should use the a long, random encryption key. Generate it is using the following command:

```{.bash data-prompt="$"}
$ openssl rand -base64 48
```

## Configure backup storage

The backup storage configuration for encrypted backups is the same as for unencrypted ones. The only difference is that you add the encryption key to the storage configuration and encode it together with the storage credentials and the pgBackRest repository name. 

1. Encode the storage configuration file. The following is the example configuration for the S3-compatible storage.

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