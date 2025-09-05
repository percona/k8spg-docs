# Retrieve Percona certified images

When preparing for the upgrade, you must have the list of compatible images for a specific Operator version and the database version you wish to update to. You can either manually find the images in the [list of certified images](images.md) or you can get this list by querying the **Version Service** server. 

### What is the Version Service?

The **Version Service** is a centralized repository that the Percona Operator for PostgreSQL connects to at scheduled times to get the latest information on compatible versions and valid image paths. This service is a crucial part of the automatic upgrade process, and it is enabled by default. Its landing page, `check.percona.com`, provides more details about the service itself.

### How to query the Version Service

You can manually query the Version Service using the `curl` command. The basic syntax is:

```{.bash data-prompt="$"}
$ curl https://check.percona.com/versions/v1/pg-operator/<operator-version>/<pg-version> | jq -r '.versions[].matrix'
```

where:

* **`<operator-version>`** is the version of the Percona Operator for PostgreSQL you are using.
* **`<pg-version>`** is the version of PostgreSQL you want to get images for. This part is optional and helps filter the results. It can be a specific PostgresQL version (e.g.16.3), a recommended version (e.g. 16-recommended), or the latest available version (e.g. 16-latest).

For example, to retrieve the list of images for Operator version `2.4.0` for PostgreSQL version `16.3`, use the following command:

```{.bash data-prompt="$"}
$ curl https://check.percona.com/versions/v1/pg-operator/2.4.0/16.3 | jq -r '.versions[].matrix'
```

??? example "Sample output"

    ```{.text .no-copy}
    {
    "pmm": {
        "2.42.0": {
            "imagePath": "percona/pmm-client:2.42.0",
            "imageHash": "14cb96de47e3bc239bf285f22ec6f170b4a1181301b19100f5b7dc22c210bf8c",
            "imageHashArm64": "",
            "status": "recommended",
            "critical": false
        }
    },
    "operator": {
        "2.4.0": {
            "imagePath": "percona/percona-postgresql-operator:2.4.0",
            "imageHash": "3012437bcfe793eaf34258aa44bb3bc404e7702711aefe4183324ee2d6928240",
            "imageHashArm64": "",
            "status": "recommended",
            "critical": false
        }
    },
    "postgresql": {
        "16.3": {
            "imagePath": "percona/percona-postgresql-operator:2.4.0-ppg16.3-postgres",
            "imageHash": "8248b290a88b881f1871fbca0de7da1acace31f94f795d1990e3ca3ca5dd3636",
            "imageHashArm64": "",
            "status": "recommended",
            "critical": false
        }
    },
    "pgbackrest": {
        "16.3": {
            "imagePath": "percona/percona-postgresql-operator:2.4.0-ppg16.3-pgbackrest2.51-1",
            "imageHash": "3e59b19b619e5580292c4fa8f9efedea3e9d05b79af8e186643490b13a6f83a5",
            "imageHashArm64": "",
            "status": "recommended",
            "critical": false
        }
    },
    "pgbackrestRepo": {},
    "pgbadger": {},
    "pgbouncer": {
        "16.3": {
            "imagePath": "percona/percona-postgresql-operator:2.4.0-ppg16.3-pgbouncer1.22.1",
            "imageHash": "37f466cea2330939f16c890a327b1d88b16cd85063ce45aff8255b8108accb08",
            "imageHashArm64": "",
            "status": "recommended",
            "critical": false
        }
    },
    "postgis": {
        "16.3": {
            "imagePath": "percona/percona-postgresql-operator:2.4.0-ppg16.3-postgres-gis3.3.6",
            "imageHash": "7ca3172329ade3be97b9bd837a3315fcb87179357e420f76662a9d0e9a4a74d3",
            "imageHashArm64": "",
            "status": "recommended",
            "critical": false
        }
    }
    }
    ```

To narrow down the results to the recommended version of PostgreSQL 16, you can use:

```{.bash data-prompt="$"}
$ curl https://check.percona.com/versions/v1/pg-operator/2.4.0/16-recommended | jq -r '.versions[].matrix'
```