# PostgreSQL Community images

Community images are built from official PostgreSQL packages. Use Operator 3.1.0 or later. See [Deploy a cluster with community PostgreSQL images](install-community.md).

Evaluation images live under `percona/percona-postgresql-operator`. You still deploy the certified Operator image from [Percona certified images](images.md).

## Shared images

These pgBouncer and pgBackRest tags have no UBI suffix. Use them with UBI 8 or UBI 9.

| Image | Digest |
|:------|:-------|
| percona/percona-postgresql-operator:pgbouncer1.25.2-43-community (x86_64) | 0930231e5a4b0d1afff20cdc1d70e6345e01f024a7baaa49f9f38940b72dbfbe |
| percona/percona-postgresql-operator:pgbouncer1.25.2-43-community (ARM64) | 5070b7bcc70df1736b5505f23f6da909b9132037deb4b068df170a822a5522e3 |
| percona/percona-postgresql-operator:pgbackrest2.59.1-1-community (x86_64) | b9ebeb49c783538ed76754303d29a06c743bb72ddd397cc2bec55bfbd8a655b5 |
| percona/percona-postgresql-operator:pgbackrest2.59.1-1-community (ARM64) | f7e9f16295f259c8d0af37f190e755908042d3a71a7da609064846099c8bab43 |

## PostgreSQL images by UBI

PostgreSQL and the upgrade image include `-community-ubi9` or `-community-ubi8` in the tag. PostgreSQL 19 is a tech preview and ships on UBI 9 only. Community images are not published for UBI 10.

=== "UBI 9"

    | Image | Digest |
    |:------|:-------|
    | percona/percona-postgresql-operator:postgresql18.6-1-community-ubi9 (x86_64) | cdd0654da7ee1ec2b9cfb5c4d9370101f31d967177095d21851179aac01c1b57 |
    | percona/percona-postgresql-operator:postgresql18.6-1-community-ubi9 (ARM64) | 8d37579f58b5568f28bfd2bb0cbcf697c5600e597eb6fca1de9423cfd534c832 |
    | percona/percona-postgresql-operator:postgresql17.11-1-community-ubi9 (x86_64) | c54d5889e89a05f7cbe0fa47e235672bede3494732c5aef915ce3ff895bf0c5c |
    | percona/percona-postgresql-operator:postgresql17.11-1-community-ubi9 (ARM64) | 86d05cb82b7993cc44fc0a7753cf1d4497efcd68eff93729aead6ba69626a72d |
    | percona/percona-postgresql-operator:postgresql16.15-1-community-ubi9 (x86_64) | b683894e6ebfa71e679557226a0b13a828bdd7a5e9ae8ed9edc9ed6e4d6dbc93 |
    | percona/percona-postgresql-operator:postgresql16.15-1-community-ubi9 (ARM64) | 1c593b7565ef1aeaf476ac4b2652c1cf18781694aa822c325786288255b47747 |
    | percona/percona-postgresql-operator:postgresql15.19-1-community-ubi9 (x86_64) | c011e946b0fb7759f485d06ff6401e0afa4fc08b1c92323cc36a355b22503e90 |
    | percona/percona-postgresql-operator:postgresql15.19-1-community-ubi9 (ARM64) | a220533c0d97548667c6f9e76a732c960715f1ad0e47d13ac9be3584f389c397 |
    | percona/percona-postgresql-operator:postgresql14.24-1-community-ubi9 (x86_64) | c0564bfaaf8a5e035d43ab943412fb57a6a9e409081f8615d4cb4a7a380c06fd |
    | percona/percona-postgresql-operator:postgresql14.24-1-community-ubi9 (ARM64) | 5292b47abb4b24779d3b4a428b4670f98cdbac7886f6d3ad308ca3349d10d98b |
    | percona/percona-postgresql-operator:postgresql19-1-community-ubi9 (x86_64) | 5c24ff3483f49455ca0629a4c5626cbe25d3d93298ef923bb159d90561e432dc |
    | percona/percona-postgresql-operator:postgresql19-1-community-ubi9 (ARM64) | ec4f671a4bf07ab36bf77232c34f33d2eb034faee2c512068d4d5afd0943df02 |
    | percona/percona-postgresql-operator:upgrade18.6-17.11-16.15-15.19-14.24-1-community-ubi9 (x86_64) | 5b9309a1e0837c5ba77d28341e4e4b1967633c9a45ee81c5a946df3f943bacf9 |
    | percona/percona-postgresql-operator:upgrade18.6-17.11-16.15-15.19-14.24-1-community-ubi9 (ARM64) | dbe465c16cefd853d547c36a0f33a4ff192eb2fe4a33272c41b00f3c7bc53ef3 |

=== "UBI 8"

    | Image | Digest |
    |:------|:-------|
    | percona/percona-postgresql-operator:postgresql18.6-1-community-ubi8 (x86_64) | b63188a2eed41ff8d60d9857fff02eb306a6f8bc1db70119f7592bb18441d3d5 |
    | percona/percona-postgresql-operator:postgresql18.6-1-community-ubi8 (ARM64) | eb3253b43c7def2a07a96476567e999ff5c1cd77331a7cd3d139dfdf4c87ad49 |
    | percona/percona-postgresql-operator:postgresql17.11-1-community-ubi8 (x86_64) | 75bea07f021cdb1cee14f36a8552933bd689a51f3bccde3114e55db387032a3b |
    | percona/percona-postgresql-operator:postgresql17.11-1-community-ubi8 (ARM64) | 60a3298140e24588c4424ca4491eb54afc2b64bd50e4c33106cb2740051f04c6 |
    | percona/percona-postgresql-operator:postgresql16.15-1-community-ubi8 (x86_64) | ea566ac5465f33013a6ceb32aa35eda4ac205a735d62948b902550cddb56ceff |
    | percona/percona-postgresql-operator:postgresql16.15-1-community-ubi8 (ARM64) | 5cd75496c59366d779984f3506c9e10cb534a048a875c17a4c972b924ab4aaac |
    | percona/percona-postgresql-operator:postgresql15.19-1-community-ubi8 (x86_64) | 83b218b822e3b97cababc4e1e9ae4bdf606648b3a90506e48fe0f0db1faf3164 |
    | percona/percona-postgresql-operator:postgresql15.19-1-community-ubi8 (ARM64) | e9bcb826bbe38a19756fb9a46efe5da4251ac4b24f0edc49b9a2cd2eb03a2b28 |
    | percona/percona-postgresql-operator:postgresql14.24-1-community-ubi8 (x86_64) | d8cf1c4a3a4da50219aa3c4a7dcc3880e8e75a089c582fb2fe8bd4d0912184b5 |
    | percona/percona-postgresql-operator:postgresql14.24-1-community-ubi8 (ARM64) | 40c15159e96e805301c5b069d2ba7aa29e800d3ca5f7d49831dda5cce45c9e70 |
    | percona/percona-postgresql-operator:upgrade18.6-17.11-16.15-15.19-14.24-1-community-ubi8 (x86_64) | 1eabed961e7f83eaa05afaa4331218f8791f0e7b612300a0c127e8cfb64cde4e |
    | percona/percona-postgresql-operator:upgrade18.6-17.11-16.15-15.19-14.24-1-community-ubi8 (ARM64) | a8e2c70637e78866680daba76f7467ea67d9e9d3b718f8a05eed3139d86d1e68 |
