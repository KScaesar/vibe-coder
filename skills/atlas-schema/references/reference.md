# Atlas-Schema - Reference

**Pages:** 3

---

## Feature Compatibility

**URL:** https://atlasgo.io/features

**Contents:**
- Feature Compatibility
- Atlas is Open-Core​
  - Pro Plan​
- Feature Availability​
  - CLI Features​
  - Database Support​
  - Database Features​
  - Data Sources​
  - Linting rules​

Atlas is an open-core project. The core engine is open-source and available on GitHub under the Apache 2.0 license. Open-source features cover the core functionality of Atlas, including database inspection, diffing, migration planning and execution, and more. For the basic and common use cases, the open-source version of Atlas is more than enough.

In addition, Atlas also offers a number of advanced features that are only available in proprietary versions. The vast majority of these features are available in the Pro Plan of Atlas, which you can use for free by creating an Atlas account.

We provide a free 30-day trial for new users, after which a license is required to continue using Atlas Pro.

Users can upgrade to the Pro Plan for $9/seat per month.

To learn more about our plans and pricing, visit the Atlas Pricing Page.

Create your Atlas Pro account by running the command below and following the instructions on the screen:

The following sections clarify which features are available to users who use the open-source version of Atlas and which are exclusively available to those on the Atlas Pro Plan.

All common open-source RDBMS are supported in all versions of Atlas. In addition, Atlas supports SQL Server, ClickHouse and Redshift in the Pro Plan.

Most common database features are supported in all versions of Atlas. More advanced features are available to users of the Pro Plan.

The following features are supported by the PostgreSQL driver in all versions of Atlas:

Some features are only available in the Pro Plan. For example:

The following features are supported by the MySQL driver in all versions of Atlas:

Some features are only available in the Pro Plan. For example:

The following features are supported by the MariaDB driver in all versions of Atlas:

Some features are only available in the Pro Plan. For example:

The following features are supported by the SQLite driver in all versions of Atlas:

Some features are only available in the Pro Plan. For example:

The SQL Server driver is only available to Atlas users with the Pro Plan. It supports the following features:

The ClickHouse driver is only available to Atlas users with the Pro Plan. It supports the following features:

The Redshift driver is only available to Atlas users with the Pro Plan. It supports the following features:

The Oracle driver is only available to Atlas users with the Pro Plan. It supports the following features:

The Google Cloud Spanner driver is only available to Atlas users with the Pro Plan. It supports the following features:

The Snowflake driver is only available to Atlas users with the Pro Plan. It supports the following features:

The Databricks driver is only available to Atlas users with the Pro Plan. It supports the following features:

Data sources are a powerful feature of Atlas that allows you to load data from external sources into your Atlas Project.

Migration and schema linting help teams automate the verification of schema changes, ensuring they are safe and won't introduce any issues. Atlas community version includes a basic set of linting rules, while the Pro Plan provides a more advanced suite for deeper validation.

For more a detailed breakdown on linting rules, visit the Migration Linting page.

**Examples:**

Example 1 (bash):
```bash
atlas login
```

---

## Community Edition

**URL:** https://atlasgo.io/community-edition

**Contents:**
- Community Edition
- Obtaining Community Binaries​
- Community vs Other Editions​
  - License​
  - Features Unavailable in the Community Edition​
    - Versioned Migrations​
    - Declarative Migrations​
    - Integrations and Providers​
    - Database Features​
    - Drivers​

Users that want to use the Community Edition of Atlas which is built directly from the Atlas GitHub repository and licensed under the Apache 2.0 license can do so by following the instructions below.

To download and install the latest release of the Atlas CLI, simply run the following in your terminal:

To pull the Atlas image and run it as a Docker container:

If the container needs access to the host network or a local directory, use the --net=host flag and mount the desired directory:

Download the latest release and move the atlas binary to a file location on your system PATH.

If you want to manually install the Atlas CLI, pick one of the below builds suitable for your system.

The Community Edition of Atlas is licensed under the Apache 2.0 license, while the Open Edition is based on both the open-source codebase with some additional proprietary features. Usage of the Open Edition is free under the terms of the Atlas EULA.

The Community Edition does not support the following commands and integrations:

The following database features are not supported in the Community Edition:

The following drivers are not supported in the Community Edition:

**Examples:**

Example 1 (shell):
```shell
curl -sSf https://atlasgo.sh | sh -s -- --community
```

Example 2 (shell):
```shell
docker pull arigaio/atlas:latest-communitydocker run --rm arigaio/atlas:latest-community --help
```

Example 3 (shell):
```shell
docker run --rm --net=host \-v $(pwd)/migrations:/migrations \arigaio/atlas:latest-community migrate apply--url "mysql://root:pass@:3306/test"
```

---

## CLI Reference

**URL:** https://atlasgo.io/cli-reference

**Contents:**
- CLI Reference
- Introduction​
- Supported Version Policy​
- Distributed Binaries​
- atlas ask​
    - Usage​
- atlas copilot​
    - Usage​
    - Flags​
- atlas license​

This document serves as reference documentation for all available commands in the Atlas CLI. Similar information can be obtained by running any atlas command with the -h or --help flags.

For a more detailed introduction to the CLI capabilities, head over to the Getting Started page.

To ensure the best performance, security and compatibility with the Atlas Cloud service, the Atlas team will only support the two most recent minor versions of the CLI. For example, if the latest version is v0.31, the supported versions will be v0.30 and v0.31 (in addition to any patch releases and the "canary" release which is built twice a day).

As part of our Supported Version Policy mentioned above, binaries for versions that were published more than 6 months ago will be removed from the CDN and Docker Hub.

The binaries and Docker images distributed in official releases are released in two flavors:

For instructions on how to install Atlas Community, see this guide.

Use Atlas AI to resolve the latest error

Start an interactive session with Atlas Copilot

Display license information

Log in to Atlas Cloud.

'atlas login' authenticates the CLI against Atlas Cloud.

Logout from Atlas Cloud.

'atlas logout' removes locally-stored credentials.

Manage versioned migration files

'atlas migrate' wraps several sub-commands for migration management.

Applies pending migration files on the connected database.

'atlas migrate apply' reads the migration state of the connected database and computes what migrations are pending. It then attempts to apply the pending migration files in the correct order onto the database. The first argument denotes the maximum number of migration files to apply. As a safety measure 'atlas migrate apply' will abort with an error, if:

If run with the "--dry-run" flag, atlas will not execute any SQL.

Generate a checkpoint file representing the state of the migration directory.

The 'atlas migrate checkpoint' command uses the dev-database to calculate the current state of the migration directory by executing its files. It then creates a checkpoint file that represents this state, enabling new environments to bypass previous files and immediately skip to this checkpoint when executing the 'atlas migrate apply' command.

Compute the diff between the migration directory and a desired state and create a new migration file.

The 'atlas migrate diff' command uses the dev-database to calculate the current state of the migration directory by executing its files. It then compares its state to the desired state and create a new migration file containing SQL statements for moving from the current to the desired state. The desired state can be another another database, an HCL, SQL, or ORM schema. See: https://atlasgo.io/versioned/diff

Reverting applied migration files from the database

Edit a migration file by its name or version and update the atlas.sum file.

Hash (re-)creates an integrity hash file for the migration directory.

'atlas migrate hash' computes the integrity hash sum of the migration directory and stores it in the atlas.sum file. This command should be used whenever a manual change in the migration directory was made.

Import a migration directory from another migration management tool to the Atlas format.

Run analysis on the migration directory

List all migration files in the directory.

Creates a new empty migration file in the migration directory.

'atlas migrate new' creates a new migration according to the configured formatter without any statements in it.

Push a migration directory with an optional tag to the Atlas Registry

The 'atlas migrate push' command allows you to push your migration directory to the Atlas Registry. If no repository exists in the registry for the pushed directory, a new one is created. Otherwise, the directory state will be updated. Read more: https://atlasgo.io/registry

Rebase one or more migration file on top of all other files and update the atlas.sum file.

Remove a migration file from the migration directory. Does not work for remote directories.

Set the current version of the migration history table.

'atlas migrate set' edits the revision table to consider all migrations up to and including the given version to be applied. This command is usually used after manually making changes to the managed database.

Show the contents of one or more migration files.

Get information about the current migration status.

'atlas migrate status' reports information about the current status of a connected database compared to the migration directory.

Run migration tests against the given directory

Validates the migration directories checksum and SQL statements.

'atlas migrate validate' computes the integrity hash sum of the migration directory and compares it to the atlas.sum file. If there is a mismatch it will be reported. If the --dev-url flag is given, the migration files are executed on the connected database in order to validate SQL semantics.

Work with atlas schemas.

The atlas schema command groups subcommands working with declarative Atlas schemas.

Apply an atlas schema to a target database.

'atlas schema apply' plans and executes a database migration to bring a given database to the state described in the provided Atlas schema. Before running the migration, Atlas will print the migration plan and prompt the user for approval.

The schema is provided by one or more URLs (to a HCL file or directory, database or migration directory) using the "--to, -t" flag: atlas schema apply -u URL --to "file://file1.hcl" --to "file://file2.hcl" atlas schema apply -u URL --to "file://schema/" --to "file://override.hcl"

As a convenience, schema URLs may also be provided via an environment definition in the project file (see: https://atlasgo.io/cli/projects).

If run with the "--dry-run" flag, atlas will exit after printing out the planned migration.

Removes all objects from the connected database.

'atlas schema clean' drops all objects in the connected database and leaves it in an empty state. As a safety feature, 'atlas schema clean' will ask for confirmation before attempting to execute any SQL.

Calculate and print the diff between two schemas.

'atlas schema diff' reads the state of two given schema definitions, calculates the difference in their schemas, and prints a plan of SQL statements to migrate the "from" database to the schema of the "to" database. The database states can be read from a connected database, an HCL project or a migration directory.

Formats Atlas HCL files

'atlas schema fmt' formats all ".hcl" files under the given paths using canonical HCL layout style as defined by the github.com/hashicorp/hcl/v2/hclwrite package. Unless stated otherwise, the fmt command will use the current directory.

After running, the command will print the names of the files it has formatted. If all files in the directory are formatted, no input will be printed out.

Inspect a database and print its schema in Atlas DDL syntax.

'atlas schema inspect' connects to the given database and inspects its schema. It then prints to the screen the schema of that database in Atlas DDL syntax. This output can be saved to a file, commonly by redirecting the output to a file named with a ".hcl" suffix:

atlas schema inspect -u "mysql://user:pass@localhost:3306/dbname" > schema.hcl

This file can then be edited and used with the atlas schema apply command to plan and execute schema migrations against the given database. In cases where users wish to inspect all multiple schemas in a given database (for instance a MySQL server may contain multiple named databases), omit the relevant part from the url, e.g. "mysql://user:pass@localhost:3306/". To select specific schemas from the databases, users may use the "--schema" (or "-s" shorthand) flag.

Plan a declarative migration for the schema transition

The 'atlas schema plan' command allows users to pre-plan, review, and approve migrations before executing 'atlas schema apply' on the database. This enables users to preview and modify SQL changes, involve team members in the review process, and ensure that no human intervention is required during the atlas schema apply phase. Read more: https://atlasgo.io/declarative/plan

Approve a migration plan by its registry URL

Run analysis (migration linting) on a plan file

List all plans in the registry for the given schema transition

Create a new plan file for the schema transition

Pull a plan file from the registry

Push a plan file to the registry

delete a migration plan by its registry URL

Run schema plan tests

Validate a plan file against the schema transition

Push the schema with an optional tag to the Atlas Registry

The 'atlas schema push' command allows you to push your schema definition to the Atlas Registry. If no repository exists in the registry for the schema, a new one is created. Otherwise, a new version is generated. Read more: https://atlasgo.io/registry

Inspect a database and print its schema statistics

'atlas schema stats inspect' connects to the given database and inspects its schema statistics. It then prints the statistics as OpenMetrics format. For more information about the format, see:

https://prometheus.io/docs/specs/om/open_metrics_spec

Run schema tests against the desired schema

Prints this Atlas CLI version information.

Show the current user and organization.

'atlas whoami' shows the current user and organization.

**Examples:**

Example 1 (bash):
```bash
atlas copilot [flags]
```

Example 2 (sql):
```sql
-c, --config string        select config (project) file using URL format (default "file://atlas.hcl")      --env string           set which env from the config file to use  -r, --resume string        resume a session by providing an identifier      --var <name>=<value>   input variables (default [])
```

Example 3 (bash):
```bash
atlas license
```

Example 4 (bash):
```bash
atlas login [org] [flags]
```

---
