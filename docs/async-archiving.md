# Speed-up backups with pgBackRest asynchronous archiving

Backing up a database with high write-ahead logs (WAL) generation can be rather
slow, because PostgreSQL archiving process is sequential, without any
parallelism or batching. In extreme cases backup can be even considered
unsuccessful by the Operator because of the timeout.

The pgBackRest tool used by the Operator solves this problem
by using the [WAL asynchronous archiving :octicons-link-external-16:](https://pgbackrest.org/user-guide-centos7.html#async-archiving) feature.

Asynchronous archiving is enabled by default in the `pgBackRest` configuration. It requires the spool path to store transient data. The spool path may differ depending on the image and version. An example spool path is `/pgdata/pgbackrest-spool`. 

You can further fine-tune asynchronous archiving by setting the max number of parallel processes for `archive-push` and `archive-get` commands.

Be sure not to set a high `process-max` value because it may affect normal database operations.
 
Your storage configuration file may look as follows:

```ini title="s3.conf"
[global]
repo2-s3-key=REPLACE-WITH-AWS-ACCESS-KEY
repo2-s3-key-secret=REPLACE-WITH-AWS-SECRET-KEY
repo2-storage-verify-tls=n
repo2-s3-uri-style=path

[global:archive-get]
process-max=2

[global:archive-push]
process-max=4
```

No modifications are needed aside of setting these additional parameters.
You can find more information about WAL asynchronous archiving in
[gpBackRest official documentation :octicons-link-external-16:](https://pgbackrest.org/user-guide-centos7.html#async-archiving)
and in [this blog post :octicons-link-external-16:](https://www.percona.com/blog/how-pgbackrest-is-addressing-slow-postgresql-wal-archiving-using-asynchronous-feature/).