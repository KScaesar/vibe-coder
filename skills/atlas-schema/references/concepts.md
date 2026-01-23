# Atlas-Schema - Concepts

**Pages:** 1

---

## URLs

**URL:** https://atlasgo.io/concepts/url

**Contents:**
- URLs
- Supported Schemes​
    - file​
    - atlas​
    - env​
    - ent​
- SSL/TLS Mode​
    - PostgreSQL​
    - MySQL​
- Non-alphanumeric characters​

Atlas uses a standard URL format to connect to databases and load schemas and migrations from various sources. The format below covers the supported parts of a URL, with subsequent sections providing more detailed examples.

To inspect a database using a URL, refer to one of the examples below:

Connecting to a local PostgreSQL database named database (all schemas):

Connecting to a specific PostgreSQL schema named public:

Connecting to a local PostgreSQL with credentials and SSL disabled:

Connecting to a local MySQL server (all schemas/databases):

Connecting to a specific MySQL schema (database) with a username and password:

Connecting using Unix Sockets:

Connecting to a local MariaDB server (all schemas/databases):

Connecting to a specific MariaDB schema (database) with a username and password:

Connecting using Unix Sockets:

Connecting to a default schema of current user:

Connecting to a local SQLServer database named master (all schemas). The user need to have db_owner role:

Azure Active Directory (AAD) authentication:

Use the fedauth parameter to specify the AAD authentication method. For more information, see the document on the underlying driver.

Connecting to the Oracle Pluggable Database (PDB) named FREEPDB1 and managing all tables of the login user PDBADMIN:

If you want to manage all schemas in the Oracle Pluggable Database (PDB), you can use the mode parameter to specify the scope of the connection.

Connecting to a local SQLite database (file):

Connecting to an in-memory SQLite database (ephemeral). Useful for --dev-url:

Atlas also supports WebSocket connections to remote libsql databases:

Connecting to a local ClickHouse server (all schemas/databases):

Connecting to a specific ClickHouse schema (database) with a username and password:

Connecting to a specific ClickHouse schema with SSL enabled:

To connect ClickHouse Cloud, we need to use native protocol port 9440 with SSL enabled:

Connecting to a specific Redshift cluster with a schema named public:

Connecting to a specific Redshift cluster with a schema named public with SSL disabled:

If you want to connect Redshift though Data API you can use the following URL:

AWS credentials are required to connect to Redshift via Data API. In this protocol, atlas doesn't support changing the schema on URL, the schema is based on default schema of the user. If you want to bind the connection to a specific schema, you can use the following SQL command:

Connecting to Serverless via IAM Identity:

Connecting to Serverless via Secret ARN:

Connecting to provisioned Redshift cluster via IAM Identity:

Connecting to provisioned Redshift cluster with database username

Connecting to provided Redshift cluster via Secret ARN:

Connecting to an Aurora DSQL cluster:

Connecting to spanner database on Google Cloud Platform (GCP):

You must be authenticated with GCP credentials to connect to Spanner.

Connecting to Snowflake database via user and password:

Connecting to Snowflake schema via user and password:

Connecting to Snowflake database via Programmatic Access Token:

Connecting to Snowflake schema via Programmatic Access Token:

Connection to Snowflake database via Multi-factor authentication (MFA)

For another authentication methods or advanced connection options, refer to the Snowflake DSN.

Explanation of the URL parameters:

Connecting to a schema on the default catalog:

To get the connection details of host and warehouse, please refer to the Databricks documentation. For token, please refer to

Connecting to a catalog (database) scope:

Connecting to a specific schema in a specific catalog:

Atlas can spin up an ephemeral local docker container for you by specifying a special URL like below. This can be useful if you need a dev database for schema validation or diffing. However, some images like mysql / mariadb take quite some time to "boot", before they are ready to be used. For a smoother developing experience consider spinning up a longer lived container by yourself.

When the database URL targets a specific schema, Atlas limits its scope to that schema for inspection, diffing, planning, and applying changes. DDL statements are formatted without schema qualifiers and can be executed on any schema - for example, table instead of schema.table.

When no schema is specified, Atlas operates on all schemas and includes schema qualifiers in the generated DDL statements - for example, schema.table instead of table.

For PostgreSQL, use the search_path query parameter to specify the schema scope. For MySQL, specify the schema as the database name in the URL path. For SQL Server, use the mode query parameter. For other drivers, see the examples in the tabs above.

Besides the standard database URLs mentioned above, Atlas supports various schemes for loading schemas and migration states:

The file:// scheme is used to load schema state from a local file or a directory. The supported extensions are .sql and .hcl. For example:

The atlas:// scheme is used to load the state of a remote schema or a migrations directory from the Atlas Cloud, the schema registry, and migrations artifactory of Atlas. For example:

The env:// scheme is useful for referencing the state of a schema after it has been loaded by a data source. For example:

The ent:// scheme is used to load the state an ent schema. For example:

The default SSL mode for Postgres is required. Please follow the Postgres documentation for configuring your SSL connection for your database, or set SSL mode to disable with the search parameter ?sslmode=disable. For local databases, disabling SSL is appropriate when inspecting and applying schema changes.

MySQL does not require TLS by default. However, you can require TLS with the ?tls=true search parameter.

Specify the ?ssl-ca search parameter to use a custom CA certificate, or ?ssl-cert and ?ssl-key to use a custom certificate and key. Follow the MySQL documentation for configuring encrypted connections with your database.

Database URLs often contain passwords and other information which may contain non-alphanumeric characters. These characters must be escaped using standard URL encoding, in order to be parsed correctly. As a convenience, users may use the urlescape function in an atlas.hcl project file to escape these characters automatically.

Suppose your password is h:e!:l:l:o and it is stored as an environment variable named DB_PASSWORD, you can read this value and escape it using the urlescape function:

The urlescape function return the escaped value: h%3Ae%21%3Al%3Al%3Ao.

**Examples:**

Example 1 (yaml):
```yaml
driver://[username[:password]@]address/[schema|database][?param1=value1&...&paramN=valueN]
```

Example 2 (shell):
```shell
postgres://localhost:5432/database
```

Example 3 (shell):
```shell
postgres://localhost:5432/database?search_path=public
```

Example 4 (shell):
```shell
postgres://postgres:pass@localhost:5432/database?search_path=public&sslmode=disable
```

---
