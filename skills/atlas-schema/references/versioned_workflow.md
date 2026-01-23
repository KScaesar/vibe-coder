# Atlas-Schema - Versioned Workflow

**Pages:** 11

---

## Migration Troubleshooting

**URL:** https://atlasgo.io/versioned/troubleshoot

**Contents:**
- Migration Troubleshooting
- Retrieve Migration Status​
- Fixing Migration Failures​
- Handling the different types of failures​
  - Connection Loss Failures​
  - Syntax Errors​
  - DDL Semantics​
    - Option 1: Incorrect Migration File​
    - Option 2: Schema Drift​
      - atlas schema diff​

In some cases, applying a migration may fail. This document aims to provide general support for troubleshooting migration failures.

Atlas provides the atlas migrate status command to retrieve information about the migration status of a database. You can either use this command or have a look at the atlas migrate apply output to gather knowledge about the issue that caused the migration failure. An example output can be seen below.

Note, that atlas migrate status does not show information about migration attempts that were rolled back. As long as a migration failure is wrapped with a transaction by a database with transactional DDL support, Atlas will rollback entries to the revision table within the transaction.

In our experience, failures are commonly caused by one of the following issues:

Retry migration execution. Atlas stores information about applied statements alongside the revision information, and therefore knows where to proceed execution, even for partially applied / not rolled back migration files. For very rare cases, where when working without a transaction (or after an implicit commit) a connection loss occurs between a SQL statement and the entry in Atlas schema history table, you might need to manually revert the last applied statement because in those cases Atlas will continue applying one statement early.

Fix the migration file and retry migration execution. Atlas will continue the execution starting with the statement following the last successfully applied one.

Creating or editing schema resources can result in migration failure, e.g. if you are trying to create a table that already exists or to modify a table that does not exist. The cause for this is either an incorrect migration file or a schema drift, e.g. if someone dropped, created or modified a resource.

In case the migration script is incorrect, simply fix the migration file and re-apply the migration. Do not forget to update the migration directory checksum afterwards by running:

For cases with multiple deployments or no (fast) editorial access to the migration file you have to fix the database state to match whatever the migration file is expecting. You can either do this by hand or use one of the atlas schema commands. See Option 2 for more information.

Once the migration/database is fixed, you can retry migration execution.

In case of a schema drift, we still consider the migration files the source of truth. Editing their contents to match the managed database will most likely break other deployments or the local dev. The solution is to fix the database schema. This can be done manually or with the help of the atlas schema apply / atlas schema diff commands. Both commands can read a database state from a migration directory and compare it with the current state of the target database. The only difference is that atlas schema apply can automatically apply the changes to the database, while atlas schema diff will print the SQL for you to check and run manually. You can utilize the atlas schema status command to get information about the currently applied migration version.

Compare the state of the from database (the one with the schema drift), to the desired state given in the migration directory. Note the query parameter version in the connection string to the migration directory, specifying the version to consider the current state of the schema.

Compare the state of the from database (the one with the schema drift), to the desired state given in one or more HCL files.

Compare the state of the from database (the one with the schema drift), to the desired state given by another database (e.g. a local dev copy of the schema).

Once you apply the SQL shown by atlas migrate diff onto your database, the schema drift should have vanished, and you can retry migration applying.

Instead of only showing the SQL on the screen, you can immediately let Atlas apply it (Atlas will prompt for confirmation first).

Migrate the state of the url database (the one with the schema drift), to the desired state given in the migration directory. Note the query parameter version in the connection string to the migration directory, specifying the version to consider the current state of the schema.

Compare the state of the url database (the one with the schema drift), to the desired state given in one or more HCL files.

Compare the state of the url database (the one with the schema drift), to the desired state given by another database (e.g. a local dev copy of the schema).

If the issue is caused by adding or changing a constraint, it may result in a migration failure if the existing data is not valid for the new constraint. For example, changing a column from formerly int NULL to int NOT NULL on a column that contains NULL values will cause the migration to fail. This can be fixed by "fixing" the data and retrying the migration applying.

In any case, we advise to add the executed statements to fix the data to the migration file to not run into this issue again for other deployments.

At Ariga, we advise to favor correctness over performance when it comes to database changes. Wrapping migration execution in a transaction ensures the changes made to the database are rolled back if an error occurs along the way and even in cases where the connection is lost, the changes are not committed. However, some databases (most notably MySQL and MariaDB) do not support transactional DDL. If you are working with a database that does not support transactional DDL, a rollback will not restore the state previous to the migration execution, and you end up with a "broken" database state. However, since Atlas stores its own information about applied statements within the same transaction, it will start execution with the next statement in the migration file on a following migration attempt.

Atlas stores information about applied migrations in the managed database. Sometimes, you want to notify Atlas that you manually applied or rolled back a migration file. Atlas provides the atlas migrate set command for such cases.

Please refrain from manually making changes to the Atlas revision table. Atlas' behavior after such a change is undefined, and it can possibly break your database to a point you cannot recover from.

**Examples:**

Example 1 (sql):
```sql
$ atlas --env local migrate apply 1 --tx-mode noneMigrating to version 2 from 1 (1 migrations in total):  -- migrating version 2    -> INSERT INTO `users` (`id`, `name`) VALUES (1, 'masseelch'), (2, 'rotemtam'), (3, 'a8m');    -> INSERT INTO `groups` (`id`, `name`) VALUES (1, 'Founders'), (2, 'Senior Engineers'), (3, 'Junior Engineers');    -> INSERT INTO `user_groups` (`user_id`, `group_id`) VALUES    -- Founders    (2, 1), (3, 1),    -- Seniors    (1, 2), (2, 2), (3, 2),    -- Constraint error (adding masseelch twice to seniors)    (1, 2);     Error 1062: Duplicate entry '1-2' for key 'user_groups.PRIMARY'  -------------------------  -- 2.521007ms  -- 0 migrations ok (1 with errors)  -- 2 sql statements ok (1 with errors)Error: Execution had errors:Error 1062: Duplicate entry '1-2' for key 'user_groups.PRIMARY'
```

Example 2 (sql):
```sql
$ atlas --env local migrate apply 1 --tx-mode noneError: sql/migrate: executing statement "INSERT INTO `user_groups` (`user_id`, `group_id`) VALUES    -- Founders\n    (2, 1), (3, 1),    -- Seniors\n    (1, 2), (2, 2), (3, 2),    -- Constraint error (adding masseelch twice to seniors)    (1, 2);" from version "2": Error 1062: Duplicate entry '1-2' for key 'user_groups.PRIMARY'
```

Example 3 (sql):
```sql
$ atlas --env local migrate statusMigration Status: PENDING  -- Current Version: 2 (2 statements applied)  -- Next Version:    2 (1 statements left)  -- Executed Files:  2 (last one partially)  -- Pending Files:   2Last migration attempt had errors:  -- SQL:   INSERT INTO `user_groups` (`user_id`, `group_id`) VALUES     -- Founders     (2, 1), (3, 1),     -- Seniors     (1, 2), (2, 2), (3, 2),     -- Constraint error (adding masseelch twice to seniors)     (1, 2);  -- ERROR: Error 1062: Duplicate entry '1-2' for key 'user_groups.PRIMARY'
```

Example 4 (shell):
```shell
atlas migrate hash
```

---

## Down Migrations

**URL:** https://atlasgo.io/versioned/down

**Contents:**
- Down Migrations
  - Migration Approval​
    - Defaults for new Projects​
  - Dry Run​
  - Revert local databases​
  - Revert real environments​
    - Using the Schema Registry​
    - Down Manually​
  - Rollback vs. Down​
  - Pre-planned Down Migrations​

The atlas migrate down command allows reverting applied migrations. Unlike the traditional approach, where down files are "pre-planned," Atlas computes a migration plan based on the current state of the database. Atlas reverts previously applied migrations and executes them until the desired version is reached, regardless of the state of the latest applied migration — whether it succeeded, failed, or was partially applied and left the database in an unknown version.

By default, Atlas generates and executes a set of pre-migration checks to ensure the computed plan does not introduce destructive changes or deletes data. Users can review the plan and run the checks before the plan is applied by using the --dry-run flag or Atlas Cloud as described below.

Users under the Pro plan can protect this flow by configuring Atlas to require approval from one or more reviewers before applying it to the database. Here's how you can do it:

Migration approval policy enabled for the atlas migrate down command

Once set, running atlas migrate down will create a plan that requires approvals before it is applied:

You can enable protected flows by default for newly created projects in the general settings. When a new project is created, protected flows are then enabled with the configured users and their roles.

Migration approval policy enabled by default for newly created projects

Once set, running atlas migrate down will create a plan that requires approvals before it is applied:

The dry-run option allows viewing the SQL statements planned to downgrade the database to its desired version, without executing them. If the down migration plan contains pre-migration checks, Atlas executes the checks on the database and reports the results.

Users who have connected or pushed their migration directory to the Atlas Schema Registry can review the dry-run reports and the pre-migration checks results on their Atlas dashboard.

Dry-run down migration in Atlas Cloud

When experimenting with generating and applying migrations locally, sometimes there is a need to revert the last applied migration or migrations. The following steps demonstrate how to revert the last applied migration, but you can specify the number of migrations to revert as an argument.

1. Assuming a migration file named 20240305171146.sql was last applied to the database and needs to be reverted.

2. Before deleting 20240305171146.sql, run the following command to revert the last applied migration:

3. After downgrading your database to the desired version, you can safely delete the migration file 20240305171146.sql from the migration directory by running atlas migrate rm 20240305171146.

4. After the file was deleted and the database downgraded, you can generate a new migration using the atlas migrate diff command with the optional --edit flag to open the generated file in your default editor.

atlas migrate down only reverts changes applied by the migration directory, and does not touch resources that exist in the schema, but are not managed by the migration directory. If you need to clean the entire database or a schema to its initial state, including the atlas_schema_revisions table, consider using the atlas schema clean command:

Atlas follows a linear migration history model, in which schema changes are "roll-forward" by default rather than rolled back. In practice, that means reverting a schema change, such as table or column addition, requires generating a new migration version to undo the changes. This is due to the fact that the "up" and "down" might not occur consecutively as the schema evolves over time.

However, there are cases that reverting the last applied migration(s) is necessary, such when experimenting on a staging environment or when the entire deployment is rolled back and the schema changes introduced in the new version are not backward compatible for old versions of the application and therefore need to be reverted. To undo applied migration(s) on real environments, there are two approaches:

If the project is connected to the Atlas Schema Registry, you can simply revert to a specific version or a tag (e.g., GitHub commit) using the Atlas GitHub Action or with the following commands:

If this command requires a review, a new plan will be created and Atlas will wait for approval before executing it.

If the project is not connected to the Schema Registry, the steps are identical to the local workflow mentioned above.

Although sometimes people refer to down migrations as rollbacks, Atlas uses these terms differently:

Rollback - A migration that was wrapped in a transaction and all statements that were executed in the transaction context will be rolled back in case of a failure and won't have any effect on the database. By default, Atlas executes each migration file in a transaction; however, users can configure Atlas to execute all pending files in a single transaction using the tx-mode=all flag.

Down - A down migration is when changes were applied to the database and need to be reverted. Atlas computes the necessary changes to downgrade the database to the desired version and executes them.

Note, some databases like MySQL do not support transactional DDLs, causing the database to stay in unclear state in case the migration failed in the middle of the execution. In such cases, "rolling back" the partially applied migrations requires reverting the applied statements, which is what atlas migrate down does.

In addition, since non-transactional DDLs can cause the database to stay in a stale state in case they fail in the middle of the execution, when Atlas generates a down migration plan, it takes the database (+ its version) and the necessary changes into account. If a transactional plan, executable as a single unit, can be created, Atlas will opt for this approach. If not, Atlas reverts each applied statement one at a time, ensuring the database is not left in an unknown state in case a failure occurs midway, for any reason.

By default, Atlas computes the down migration plan dynamically, based on the current state of the database and the target version specified by the user. In some cases, however, teams may want to explicitly define how a migration should be reverted, especially when dealing with non-schema logic such as data migrations or other business-specific operations that Atlas cannot infer automatically (for example, calling a stored procedure or reverting a configuration flag).

In these cases, users can define manual down migrations alongside their regular migration files. These files use the txtar format described below. The following example demonstrates a migration that includes both an "up" and a manual "down" plan:

Atlas supports a text-based archive format for describing complete migration plans. Unlike standard migration files that typically contain only DDL statements (and optional directives), txtar files can include multiple file entries such as:

Each section in the archive begins with a marker line formatted as -- FILENAME -- and continues until the next marker or the end of the file. For example:

Manual down migration files override automatically generated plans. When a migration includes a down.sql section in the txtar format, Atlas uses it to revert the migration instead of computing a plan dynamically. However, a few important details apply:

The default behavior of atlas migrate down is to revert the last applied file. However, you can pass the amount of migrations to revert as an argument, or a target version or a tag as a flag. For instance, atlas migrate down 2 will revert up to 2 pending migrations while atlas migrate down --to-version 1234 will revert all applied migrations after version "1234".

CLI Command Reference

**Examples:**

Example 1 (shell):
```shell
$ atlas migrate down --env prodTo approve the plan visit: https://a8m.atlasgo.cloud/deployments/51539607645
```

Example 2 (shell):
```shell
atlas migrate down \  --url "mysql://root:pass@localhost:3306/example" \  --dir "file://migrations" \  --dry-run
```

Example 3 (shell):
```shell
atlas migrate down \  --dir "file://migrations" \  --url "mysql://root:pass@localhost:3306/example" \  --dev-url "docker://mysql/8/dev"
```

Example 4 (shell):
```shell
atlas migrate down \  --dir "file://migrations" \  --url "mysql://root:pass@localhost:3306/example" \  --dev-url "docker://mariadb/latest/dev"
```

---

## Automatic Schema Migration Planning

**URL:** https://atlasgo.io/versioned/diff

**Contents:**
- Automatic Schema Migration Planning
  - Summary​
  - Generate migrations from HCL schemas​
  - Generate migrations from SQL schemas​
  - Generate migrations from database schemas​
  - Generate migrations with custom qualifiers​
  - Generate migrations with custom formats​
  - Generate migrations for the entire database​
- Diff Policy​
- Indented SQL​

The atlas migrate diff command streamlines the process of writing schema migrations by automatically generating the SQL scripts needed to migrate a database schema from its current state to the new desired state. How does it work?

Developers define the desired state and Atlas maintains the migrations directory, which contains the explicit SQL migration scripts to move from one version to the next. The desired state can be defined using an HCL or SQL schema definition, a database URL, or an external schemas like ORM.

To get started with versioned migrations, run atlas migrate diff. This command generates a new migration file that aligns the migration directory with the state defined by the desired schema. Below are a few examples of how to use this command to generate schema migrations from various sources:

To learn more on how to configure Atlas to read the desired state of a schema from an ORM definition, see the external schema documentation.

Teams that have connected their project to Atlas Cloud (see setup) will get a prompt in the CLI if their migration directory is out of sync with the latest version in Atlas Cloud. This ensures that new migration files are added in a sequential order, preventing unexpected behavior. For example:

Additionally, the atlas migrate lint command helps enforce this requirement during the CI stage. Learn more on how to integrate Atlas into your GitHub Actions or GitLab CI Components.

Suppose we have an Atlas schema with one table and an empty migration directory:

Let's run atlas migrate diff with the necessary parameters to generate a migration script for creating our users table:

If you are working with multiple schemas and want qualified identifiers to appear in the migration files, omit the schema parameter from the --dev-url flag. In PostgreSQL, this corresponds to the search_path; in MySQL/MariaDB, it is the database in the URL path.

Run ls migrations, and you will notice that Atlas created two files. For example, for the MySQL flavor, the following files will be created:

By default, migration files are named with the following format {{ now }}_{{ name }}.sql. If you wish to use a different file format, use the format query parameter in the directory URL.

In addition to the migration directory, Atlas maintains a file name atlas.sum which is used to ensure the integrity of the migration directory and force developers to deal with situations where migration order or contents was modified after the fact.

Let's repeat the process above by changing our HCL schema file and running Atlas migration authoring again. We add a new column name to our HCL schema:

Then, run atlas migrate diff:

If you are working with multiple schemas and want qualified identifiers to appear in the migration files, omit the schema parameter from the --dev-url flag. In PostgreSQL, this corresponds to the search_path; in MySQL/MariaDB, it is the database in the URL path.

You will notice Atlas added a new file to the migration directory. For example, for the MySQL flavor, the following file will be created:

The following diagram explains how Atlas automates database schema changes. Atlas loads the current state by replaying the migration directory onto the provided dev database, compares it against the desired state and writes a new migration script for moving from the current to the desired state.

Atlas allows you to define your desired state using SQL schemas. An SQL schema can be a single file containing CREATE and ALTER statements, or a directory with multiple SQL files. As an example, suppose we have an SQL schema with one table and an empty migration directory:

Let's run atlas migrate diff with the necessary parameters to generate a migration script for creating our users table:

If you are working with multiple schemas and want qualified identifiers to appear in the migration files, omit the schema parameter from the --dev-url flag. In PostgreSQL, this corresponds to the search_path; in MySQL/MariaDB, it is the database in the URL path.

Run ls migrations, and you will notice that Atlas created two files. For example, for the MySQL flavor, the following files will be created:

By default, migration files are named with the following format {{ now }}_{{ name }}.sql. If you wish to use a different file format, use the format query parameter in the directory URL.

In addition to the migration directory, Atlas maintains a file name atlas.sum which is used to ensure the integrity of the migration directory and force developers to deal with situations where migration order or contents was modified after the fact.

Let's repeat the process above by changing our SQL schema file and running Atlas migration authoring again. We add a new column name to our SQL schema:

Then, run atlas migrate diff:

If you are working with multiple schemas and want qualified identifiers to appear in the migration files, omit the schema parameter from the --dev-url flag. In PostgreSQL, this corresponds to the search_path; in MySQL/MariaDB, it is the database in the URL path.

You will notice that Atlas added a new file to the migration directory. For example, for the MySQL flavor, the following file will be created:

To summarize, the example above explains how Atlas loads the current state by replaying the migration directory onto the specified dev-database, compares it to the desired state defined in the SQL schema file, and writes a new migration script for moving from the current to the desired state.

Suppose we have a database with a users table that was created manually or by an ORM like Ent, we can tell Atlas that this is our desired state, and we want to generate a migration script to create this table.

Let's run atlas migrate diff with the necessary parameters to generate a migration script for creating our users table:

Run ls migrations, and you will notice Atlas created 2 files:

By default, migration files are named with the following format {{ now }}_{{ name }}.sql. If you wish to use a different file format, use the format query parameter in the directory URL.

In addition to the migration directory, Atlas maintains a file name atlas.sum which is used to ensure the integrity of the migration directory and force developers to deal with situations where migration order or contents was modified after the fact.

When working on a specific database schema, Atlas generates migration scripts without schema qualifiers to allow executing them multiple times on different schemas. However, in some cases, it is necessary to have those qualifiers. To address this, Atlas allows passing another flag to migrate diff named --qualifier.

Let's run the example above, with the --qualifier flag and compare the output:

Running cat migrations/*.sql will print the same migration script but the users table will be qualified with the market schema:

Some migration tools use a different file format than the one used by Atlas. You can control the format of the migration directory by passing in the format query parameter to the migration directory URL.

Run ls migrations, and you will notice Atlas created 3 files:

In addition to the migration directory, Atlas maintains a file name atlas.sum which is used to ensure the integrity of the migration directory and force developers to deal with situations where migration order or contents was modified after the fact.

Atlas supports generating migrations for databases or multiple schemas. In PostgreSQL, a database can be created with the CREATE DATABASE command and can hold multiple schemas. In MySQL however, a database is an instance with one or more schemas.

Suppose we have an Atlas schema that defines two database schemas where each one contains a single table.

Let's run atlas migrate diff to generate migration scripts for creating the entire schema. However, unlike the previous examples where the --dev-url flag was set to a URL of a specific schema, in this case we omit the schema name from the connection string.

Running cat migrations/*.sql will print the followings:

Running cat migrations/*.sql will print the followings:

As you can see, Atlas generates statements for creating the auth and market schemas, and added them as qualifiers in the created tables.

Atlas allows configuring the schema diffing policy in project configuration to fine-tune or modify suggested changes before they are written to the migration directory:

To instruct Atlas to create and drop indexes concurrently, set the concurrent_index option in the diff block of the environment configuration. Note that such migrations are tagged with atlas:txmode none to ensure they do not run within a transaction.

The usage is as follows:

To instruct Atlas to create materialized views without populating them (using the WITH NO DATA clause), set the with_no_data option in the materialized block of the diff configuration:

To control this behavior via a CLI variable, define a variable in the project configuration and set its value dynamically when running the migrate diff command:

Run the command with the variable:

Users on the Pro tier can control how Atlas generates CREATE and DROP table statements by configuring the add_table and drop_table blocks in the diff configuration.

Starting in v0.35, the migrate diff command uses two-space indentation for generated SQL by default. You can change or remove the indentation using the --format flag. For example:

This option is not recommended for general use. It is intended for use when you encounter limitations in the Atlas schema definition or when your schema references objects that are not part of the desired state (schema) and you want Atlas to ignore their existence.

Atlas allows setting exclusion patterns for the migrations directory. Objects that match the exclusion patterns are not considered during the migrate diff stage.

Using this option, users can (manually) define objects such as tables, functions, and foreign keys in the migration directory that are not part of the desired state (schema), and instruct Atlas not to drop them during the migrate diff stage - essentially, to ignore their existence.

For more examples, see the exclude documentation.

CLI Command Reference

**Examples:**

Example 1 (shell):
```shell
atlas migrate diff create_users \  --dir "file://migrations" \  --to "file://schema.sql" \  --dev-url "docker://mysql/8/dev" # Or: "docker://mariadb/latest/dev"
```

Example 2 (shell):
```shell
atlas migrate diff create_users \  --dir "file://migrations" \  --to "file://schema.sql" \  --dev-url "docker://postgres/15/dev?search_path=public"
```

Example 3 (shell):
```shell
atlas migrate diff create_users \  --dir "file://migrations" \  --to "file://schema.hcl" \  --dev-url "docker://mysql/8/dev" # Or: "docker://mariadb/latest/dev"
```

Example 4 (shell):
```shell
atlas migrate diff create_users \  --dir "file://migrations" \  --to "file://schema.hcl" \  --dev-url "docker://postgres/15/dev?search_path=public"
```

---

## Migration Directory Checkpoints

**URL:** https://atlasgo.io/versioned/checkpoint

**Contents:**
- Migration Directory Checkpoints
  - Generating a Checkpoint​
  - Example​
  - Seeding Data​
  - Data Migrations​
  - Video Tutorial​

Atlas supports checkpoints, which are a way to capture the schema of the database at a certain version. When Atlas detects a checkpoint, it will use it to skip migrations that were applied before the checkpoint was created. Using checkpoints can speed up the process of setting up a database from scratch, especially in large migration directories.

The atlas migrate checkpoint feature is only available to Atlas Pro users. You can create a free account using the atlas login command. To learn more about logged-in features, see Features page.

Atlas can automatically generate a checkpoint for you using the atlas migrate checkpoint command. This command requires a Dev Database URL to be provided. Atlas will replay all migrations on the dev database and then inspect it to generate the checkpoint.

A checkpoint is a SQL file with a structure similar to:

Notice the atlas:checkpoint directive, which indicates that this file is a checkpoint. Following this directive, the checkpoint file contains the SQL statements to create the tables and other objects in the database at the time the checkpoint was created.

Suppose your project has been going on for a while, and you have a migration directory with 100 migrations. Whenever you need to install your application from scratch (such as during development or testing), you need to replay all migrations from start to finish to set up your database. Depending on your setup, this may take a few seconds or more. If you have a checkpoint, you can replay only the migrations that were added since the latest checkpoint, which can be much faster.

Here's a short example. Let's say we have a migration directory with 2 migration files, managing a SQLite database. The first one creates a table named t1:

And the second adds a table named t2 and adds a column named c2 to t1:

To create a checkpoint, we can run the following command:

This will create a SQL file, which is our checkpoint:

Next, let's apply these migrations on a local SQLite database:

As expected, Atlas skipped all of the migrations up to the checkpoint and only applied the last one!

Checkpoints currently do not include INSERT statements or other data seeding operations. If you need to seed data as part of your setup you will need to manually copy these statements into the checkpoint file.

In long running applications, it is sometimes necessary to perform data migrations, which are migrations that modify the data in the database. Checkpoint generation ignores these migrations, as they are not needed for setting up a fresh database (which is the usecase which checkpoints are designed for).

**Examples:**

Example 1 (sql):
```sql
-- atlas:checkpointCREATE TABLE t1 (    -- ...)
```

Example 2 (sql):
```sql
create table t1 ( c1 int );
```

Example 3 (sql):
```sql
create table t2 ( c1 int, c2 int );alter table t1 add column c2 int;
```

Example 4 (shell):
```shell
atlas migrate checkpoint --dev-url "sqlite://file?mode=memory&_fk=1"
```

---

## Manual Migrations

**URL:** https://atlasgo.io/versioned/new

**Contents:**
- Manual Migrations
  - Flags​
  - Migration name​
  - Custom statements delimiter​
    - Using the DELIMITER command used by MySQL client​
    - Using the atlas:delimiter directive to set \n\n\n as a separator:​
    - Using the atlas:delimiter directive to set -- end as a separator:​
  - Recalculating the directory hash​
  - Examples​

In some cases it is desirable to add a migration file manually. This could be done to provision resources that Atlas does not yet capture in its DDL (such as triggers and views) or to seed data with INSERT statements.

To manually add a new migration file to the directory use the migrate new command.

When using migrate new to create a new migration file users may supply the following flags:

Users may optionally add a final positional argument to set the name of the migration file. This name will be appended to the migration version number in the filename as such: <version>_<name>.sql.

The semicolon character (;) is recognized by Atlas as a statement delimiter. In some cases, however, the delimiter may need to be redefined because the semicolon itself is used in one of the DDL statements. For example, a stored program containing semicolon characters.

Atlas maintains a file named atlas.sum in the migration directory. This file is used to ensure the integrity of the migration directory and force developers to deal with situations where migration order or contents was modified after the fact.

After manually editing the contents of a newly created migration file, the checksums for the directory must be recalculated. This can be done by running atlas migrate hash command.

Create and edit a new migration file:

Create a new migration file named "add_user":

Create a new migration file in a specific directory:

**Examples:**

Example 1 (sql):
```sql
DELIMITER //CREATE PROCEDURE dorepeat(p1 INT)    BEGIN    SET @x = 0;    REPEAT SET @x = @x + 1; UNTIL @x > p1 END REPEAT;END//DELIMITER ;CALL dorepeat(100)
```

Example 2 (sql):
```sql
CREATE PROCEDURE dorepeat(p1 INT)    BEGIN    SET @x = 0;    REPEAT SET @x = @x + 1; UNTIL @x > p1 END REPEAT;END
```

Example 3 (sql):
```sql
CALL dorepeat(100);
```

Example 4 (sql):
```sql
-- atlas:delimiter \n\n\nCREATE PROCEDURE dorepeat(p1 INT)BEGIN    SET @x = 0;    REPEAT SET @x = @x + 1; UNTIL @x > p1 END REPEAT;END;CALL dorepeat(1000);
```

---

## Introduction to Versioned Migrations

**URL:** https://atlasgo.io/versioned/intro

**Contents:**
- Introduction to Versioned Migrations
- Creating the first migration​
- Pushing migrations to Atlas Registry​
- Applying migrations​
- Generating another migration​
- Next Steps​

This guide offers a high-level overview of the Atlas versioned migration workflow. It walks you through the steps of creating a migration directory, automatically generating SQL migration from its desired schema, pushing the migration directory to the Atlas Schema Registry, and applying changes to databases. For more in-depth guides, please check out the other pages in this section or visit our guides.

One of Atlas's most popular features is its ability to automatically generate SQL migration scripts based on a desired schema. A schema can be defined in several ways: through Atlas's HCL language, standard SQL, external ORMs or programs. In this guide, we will use a SQL schema to define our desired state.

First, let's create a simple SQL schema containing two tables: users and repos and name it schema.sql:

After creating our desired schema (schema.sql), let's run Atlas to generate the migration script needed to apply it to a database.

Run ls migrations, and you'll notice that Atlas has created two files:

In addition to the migration directory, Atlas maintains a file name atlas.sum which is used to ensure the integrity of the migration directory and force developers to deal with situations where migration order or contents was modified after the fact.

Now that we have our first migration, we can apply it to a database. There are multiple ways to accomplish this, with most methods covered in the guides section. In this example, we'll demonstrate how to push migrations to the Atlas Registry, much like how Docker images are pushed to Docker Hub.

Migration Directory created with atlas migrate push

First, log in to Atlas. If it's your first time, you'll be prompted to create both an account and a workspace (organization):

After logging in, let's name our new migration project atlas-intro and run atlas migrate push:

After our migration directory is pushed, Atlas prints a URL to the created directory, similar to the one shown in the image above.

Once our atlas-intro migration directory has been pushed, we can apply it to a database from any CD platform without needing to pull our migration files from source control. For the sake of this example, let's spin up a local database that represents our production database to apply the migrations to it:

Then, we'll create a simple Atlas configuration file (atlas.hcl) to store the settings for our environment:

The final step is to apply the migrations to the database. Let's run atlas migrate apply with the --env flag to instruct Atlas to select the environment configuration from the atlas.hcl file:

Boom! After applying the migration, you should receive a link to the deployment and the database where the migration was applied. Here's an example of what it should look like:

Migration history of a database schema created with atlas migrate apply

By clicking on the most recent deployment, you can view the full migration report from the latest run:

Migration deployment reported created with atlas migrate apply

After applying the first migration, it's time to update our schema defined in schema.sql and tell Atlas to generate another migration. This will bring the migration directory (and the databases) in line with the new state defined by the desired schema (schema.sql).

Let's make two changes to our schema:

Next, we're ready to run atlas migrate diff again to generate the new migration:

Run ls migrations, and you'll notice that a new migration has been generated. Let's run atlas migrate push again and observe the update on the migration directory page:

Migration Directory updated with atlas migrate push

Migration Directory updated with atlas migrate push

Migration Directory updated with atlas migrate push

Once pushed, you'll notice in the Databases tab that our database is in a Pending state. This means that the latest migration has been pushed but not yet applied to the database.

Database schema public is in Pending mode

Let's apply our latest migration and check our database again:

As you can see below, the database is now In Sync with the migration directory:

Database schema public is in In Sync mode

In this short tutorial we learned how to use atlas to generate migrations, push them to an Atlas workspace and apply them to databases. For more in-depth guides, please check out the other pages in this section or visit our Guides section.

We have a super friendly #getting-started channel on our community chat on Discord.

For web-based, free, and fun (GIFs included) support:

**Examples:**

Example 1 (sql):
```sql
CREATE TABLE "users" (  "id" bigint,  "name" varchar NOT NULL,  PRIMARY KEY ("id"));CREATE TABLE "repos" (  "id" bigint,  "name" varchar NOT NULL,  "owner_id" bigint NOT NULL,  PRIMARY KEY ("id"),  CONSTRAINT "owner_id" FOREIGN KEY ("owner_id") REFERENCES "users" ("id"));
```

Example 2 (sql):
```sql
CREATE TABLE `users` (  `id` bigint,  `name` varchar(255) NOT NULL,  PRIMARY KEY (`id`));CREATE TABLE `repos` (  `id` bigint,  `name` varchar(255) NOT NULL,  `owner_id` bigint NOT NULL,  PRIMARY KEY (`id`),  CONSTRAINT `owner_id` FOREIGN KEY (`owner_id`) REFERENCES `users` (`id`));
```

Example 3 (sql):
```sql
CREATE TABLE [users] (  [id] bigint,  [name] nvarchar(255) NOT NULL,  PRIMARY KEY ([id]));CREATE TABLE [repos] (  [id] bigint,  [name] varchar(255) NOT NULL,  [owner_id] bigint NOT NULL,  PRIMARY KEY ([id]),  CONSTRAINT [owner_id] FOREIGN KEY ([owner_id]) REFERENCES [users] ([id]));
```

Example 4 (sql):
```sql
CREATE TABLE `users` (  `id` UInt64,  `name` String NOT NULL,  PRIMARY KEY (`id`)) ENGINE = MergeTree() ORDER BY id;CREATE TABLE `repos` (  `id` UInt64,  `name` String NOT NULL,  `owner_id` Bigint NOT NULL,  PRIMARY KEY (`id`),) ENGINE = MergeTree() ORDER BY id;
```

---

## Import Existing Databases or Migrations

**URL:** https://atlasgo.io/versioned/import

**Contents:**
- Import Existing Databases or Migrations
- Importing an Existing Database​
      - 1. Export Database to Code
      - 2. Generate a Baseline Migration
      - 3. Apply the Baseline Migration
  - Export Database to Code​
  - Generate a Baseline Migration​
    - Examples​
  - Apply the Baseline Migration​
    - Existing databases​

Atlas provides two ways to start managing existing databases or setups with versioned migrations:

The sections below go over both approaches in detail.

The process for importing an existing database into Atlas versioned migrations involves three steps:

Choose the language that will be used to define the desired schema state, such as SQL or HCL. Use the atlas schema inspect command to import the current database schema into code. This code represents the desired state of the database and can be tested, versioned, and modified going forward - just like IaC (Infrastructure as Code), but for your databases.

Create an initial baseline migration file that represents the current state of the database using the atlas migrate diff command. This migration file serves as the starting point for future migrations. It will not be applied to existing databases but will be marked as already applied.

Run the atlas migrate apply command to apply the migration to the database. On existing databases, the migration will be marked as applied without executing its statements. On new or empty databases, the migration will be executed in full.

The very basic first step to manage your database schemas as code, is to have the state of the database schema (i.e., desired state) represented in code. Atlas allows defining the desired state in various formats, such as SQL, HCL, ORM schema, or a database connection. But for the purpose of this guide, we will focus on exporting the database schema to SQL format. The full document of the atlas schema inspect command can be found here.

By default, the inspection result is written to standard output. To save it into a folder in a structured way, we can use the split and write functions as described in the Export Database Schema to Code document.

At this stage, we expect to have a folder named src with the format of the example below:

Now that we have the current state of the database schema represented in code, we can create a baseline migration file that captures this state. This migration is called a baseline because it serves as the starting point for future migrations. For existing databases that already match this state (such as the one we just inspected), we do not want to apply this migration but only mark it as applied so future migrations can build on top of it. For new databases, this migration will be applied in full.

To generate the baseline migration, use the atlas migrate diff command. This command compares the migrations directory (which does not exist yet and is therefore considered empty) with the desired state defined in the src/ folder created in the previous step. The example below uses the --dev-url flag, which is used internally by Atlas - You can learn more about it in the Dev Database document:

The examples below show how to generate a baseline migration for different databases:

In case your schema is contained within a specific schema (e.g., public), specify the search_path query parameter in the connection URL:

If your schema is spanned across multiple schemas, or you manage database-level objects (like extensions), use a database-scoped URL:

In case your schema is contained within a specific database (e.g., dev), use the database-scoped URL as shown below:

If your schema is spanned across multiple databases, use a server-scoped URL as shown below:

If your schema is contained within a specific schema (e.g., dbo), use the schema-scoped URL as shown below:

If your schema is spanned across multiple schemas, use a database-scoped URL as shown below:

If your schema is contained within a specific database (e.g., dev), use the database-scoped URL as shown below:

If your schema is spanned across multiple databases, use a server-scoped URL as shown below:

When the database URL is set to a specific schema (e.g., mysql://:3306/dev), the scope of the work done by Atlas (inspection, diffing, planning, applying, etc.) is limited to one schema. As a result, DDL statements printed during diffing or planning will be formatted without schema qualifiers and can be executed on any schema. e.g., table instead of schema.table

However, if the database URL does not specify a schema (e.g., mysql://:3306/), Atlas operates on the selected schemas (defaulting to all), and the generated DDL statements include schema qualifiers. e.g., schema.table instead of table.

Once the baseline migration file is created, we can apply it using the atlas migrate apply command. There are two cases: for existing databases, we use the --baseline flag to set the database at this version, and for new (empty) databases, Atlas runs the migration to create the initial schema.

For databases that already contain the schema we inspected, we don't want to execute the baseline migration again. Instead, we mark it as already applied using the --baseline flag. This tells Atlas that the database is already at the baseline version, so future migrations can be applied safely on top of it.

The --baseline flag accepts the migration version as an argument. The version is the timestamp portion from the migration file name. For example, if your baseline migration file is named 20250811074144_baseline.sql, the version to pass to the flag would be 20250811074144.

For new or empty databases, Atlas will execute the baseline migration in full to create the schema from scratch.

📺 For a step-by-step example walk-through, watch our 3-minute tutorial: Versioned Migrations for Existing Databases using Atlas

Atlas supports the generation of custom migration file formats for a variety of existing migration management tools, e.g. Flyway or golang-migrate/migrate. But Atlas has its own format as well and provides a convenient command to import existing migration directories of supported tools into the Atlas format.

When using atlas migrate import to import a migration directory, users must supply multiple parameters:

Importing an existing migration directory has some limitations:

Atlas does not have the concept of rollback migrations. Therefore migrations to undo an applied migration, often called "down" or "undo" migrations, will not be imported into the new migration directory. For migration formats having the rollback migration part of one file separated by some directive, the rollback parts are stripped away.

Flyway has the concept of repeatable migrations, however, Atlas does not. In Flyway repeatable migrations are run last, if their contents did change. Atlas tries to reproduce this behavior by creating versioned migrations out of each repeatable migration file found and giving them the character R as version suffix.

Import existing golang-migrate/migrate migration directory:

Import existing Flyway migration directory:

CLI Command Reference

**Examples:**

Example 1 (shell):
```shell
atlas schema inspect -u '<url>' --format '{{ sql . | split | write "src" }}'
```

Example 2 (unknown):
```unknown
├── tables│   ├── profiles.sql│   └── users.sql├── functions│   ├── tenant_config.sql│   └── tenant_profile.sql├── types└── main.sql
```

Example 3 (shell):
```shell
atlas migrate diff "baseline" \  --to "file://src" \  --dev-url '<dev-url>'
```

Example 4 (shell):
```shell
atlas migrate diff "baseline" \  --to "file://src" \  --dev-url "docker://postgres/16/dev?search_path=public"
```

---

## Setup CI/CD for Versioned Migrations

**URL:** https://atlasgo.io/versioned/setup-cicd

**Contents:**
- Setup CI/CD for Versioned Migrations
- Choose Your Workflow​
      - Versioned Migrations (Used in this guide)
      - Declarative (State-based) Migrations
- Prerequisites​
  - Installing Atlas​
  - MacOS
  - Linux
  - Windows
  - Atlas Pro for CI/CD​

Continuous integration and continuous deployment (CI/CD) are essential practices for modern software development. Applying these principles to your database migrations helps ensure that schema changes are validated, tested, and deployed safely across all environments.

This doc introduces how to set up a CI/CD pipeline for database schema migrations with Atlas. It covers automated validation, testing, policy-based review, and deployment of schema changes so the final migrations are correct, predictable, and safe to apply for production.

For a deeper understanding of the principles behind this workflow, see our Modern Database CI/CD blueprint.

Atlas supports two types of schema management workflows: versioned migrations and declarative (state-based) migrations. This guide focuses on setting up CI/CD for versioned migrations.

Changes are defined as explicit migration files (SQL scripts) that are applied in sequence. Each migration is tracked, version-controlled, and reviewable in pull requests.

Define the desired state of your database, and Atlas automatically calculates the migration plan. This approach is covered in detail in platform-specific guides.

To understand the differences and tradeoffs between these approaches, see Declarative (State-based) vs Versioned Migrations.

Before setting up CI/CD, ensure you have the following:

To download and install the latest release of the Atlas CLI, simply run the following in your terminal:

Get the latest release with Homebrew:

To pull the Atlas image and run it as a Docker container:

If the container needs access to the host network or a local directory, use the --net=host flag and mount the desired directory:

Download the latest release and move the atlas binary to a file location on your system PATH.

Use the setup-atlas action to install Atlas in your GitHub Actions workflow:

For other CI/CD platforms, use the installation script. See the CI/CD integrations for more details.

If you want to manually install the Atlas CLI, pick one of the below builds suitable for your system.

Using Atlas in CI/CD requires Atlas Pro. To activate it in your pipelines, you'll need a bot token from Atlas Cloud.

If you don't have an account yet, sign up for a free trial at auth.atlasgo.cloud or run atlas login in your terminal.

Atlas Cloud does not access your repositories or databases. By default, Atlas Cloud only handles authentication (login) for Atlas Pro, and using the Schema Registry is optional.

The Schema Registry allows you to store, version, and maintain a single source of truth for your database schemas, and database migrations. If you prefer not to use the Schema Registry, you can use alternative storage options such as S3-compatible object storage, or any other storage solution accessible from your CI/CD pipeline.

If you haven't set up a versioned migrations project yet, create a migration directory before configuring CI/CD. Choose one of the following options:

Create your first migration directory by defining your desired schema in SQL, HCL, or through an ORM. Atlas will automatically generate migration files that you can review, version control, and apply to your databases.

Import an existing database to code, then baseline it by generating an initial migration file that represents its current state. This baseline migration serves as the starting point for future migrations and allows Atlas to begin managing your database schema going forward.

Atlas provides native integrations for all popular CI/CD platforms, with support for code comments, code suggestions, PR and run summaries, PR status updates, and more. Choose your CI platform to get started:

Set up CI/CD pipelines using GitHub Actions with Atlas. Supports schema management with versioned migrations.

Integrate Atlas with GitLab CI/CD pipelines using GitLab CI components. Full support for versioned and declarative workflows.

Use Azure DevOps Pipelines with Atlas. Supports GitHub and Azure Repos repositories with versioned migrations.

Automate database migrations with CircleCI Orbs. Complete CI/CD integration for versioned workflows.

Set up CI/CD using Bitbucket Pipes. Full support for versioned migrations and schema management.

CI validates and tests schema changes before merging to the main branch, ensuring they are safe, correct, and ready for production. The workflow follows this pattern:

Atlas validates migrations through linting that catches destructive changes, backward-incompatible operations and changes, and policy violations. It also performs automatic drift detection to ensure migrations align with your schema, and history integrity checks to maintain linear migration order.

Atlas automatically posts lint results as comments on your pull/merge requests, providing immediate feedback to developers:

To learn more about migration linting, see the Migration Linting guide.

When developers define their schema as code (HCL, SQL, or ORM) and make changes, Atlas can automatically generate migration files using the ariga/atlas-action/migrate/diff action. If migrations weren't generated locally, Atlas automatically plans the migrations and commits the files to the working PR.

The diff action also checks for drift between your schema code and migration files, ensuring they stay in sync. To keep your pull request up to date with the latest changes from the main branch, use the ariga/atlas-action/migrate/autorebase action, which automatically rebases your branch and avoids manual rebasing.

The migrate-diff functionality is available on most CI platforms:

This creates a seamless workflow where schema changes automatically become reviewable migration files.

Modern databases contain real application logic: constraints enforce business rules, triggers execute code on events, functions and procedures encapsulate complex operations, and views abstract data access. This is code, and it deserves the same engineering discipline as the rest of your system. Atlas brings software engineering practices to the database, such as version control, static analysis, migrations, and testing, so you can treat database logic with the same rigor as application code.

Schema tests verify that the schema behaves the way you expect. You can write unit tests for functions, triggers, views, procedures, constraints, and more. Atlas testing framework allows you to seed data, run queries, assert results, test failure cases, and run tests in parallel to keep things fast.

Migration tests ensure that your database migrations are semantically correct. They run against isolated databases, let you seed data, apply the migrations, and make assertions. They are especially important for data migrations, where correctness depends on the existing data and small mistakes can slip through without careful comparison of the results.

To learn more about testing, see:

When a pull request is merged into the main branch, Atlas lets you push your migration directory to the Atlas Schema Registry. This creates an immutable, versioned artifact (like pushing a Docker image to a container registry) that becomes the single source of truth for your migrations.

The registry stores the exact migration files that passed review and testing, ensuring only approved migrations can be deployed. Once in the registry, migrations can be deployed to any environment without needing access to your source code repository, using URLs like atlas://myapp?tag=latest or atlas://myapp?version=20231201182011.

Migration Directory created with atlas migrate push

The migrate-push functionality is available on all CI platforms:

Once your migrations are validated and pushed to the registry, you can deploy them to your environments. Choose the deployment method based on your infrastructure needs:

GitOps deployment for Kubernetes using ArgoCD. Deploy migrations declaratively with full GitOps workflow.

Deploy migrations directly from your CI/CD pipeline. Simple and straightforward deployment for any environment.

Infrastructure as Code deployment using the Atlas Terraform Provider. Manage migrations alongside your infrastructure.

Native Kubernetes resource management using the Atlas Operator. Deploy migrations as Kubernetes resources.

GitOps deployment alternative for Kubernetes. Continuous delivery with Git-based configuration.

Additional deployment methods including ECS Fargate, Helm, and more. Find the right solution for your infrastructure.

Enhance your CI/CD pipeline with advanced features, such as environment promotion workflows with compliance support, real-time schema monitoring and drift detection, custom policy rules, and webhook notifications:

Implement progressive deployments across Dev, Staging, and Production with environment segregation and compliance support for SOC 2, ISO 27002, and more.

Get live visibility of your database schema with automated ER diagrams, changelogs, and real-time monitoring. Automatically detect when your schema drifts from its intended state and get instant alerts via Slack or webhooks.

Define custom linting rules to enforce team practices, naming conventions, and compliance requirements. Write rules in HCL to automate policy enforcement.

Set up webhooks to receive notifications about schema changes, drift detection, and deployment events in Slack or custom HTTP endpoints.

Have questions about setting up CI/CD with Atlas? Join our Discord community or book a demo to see Atlas in action.

**Examples:**

Example 1 (shell):
```shell
curl -sSf https://atlasgo.sh | sh
```

Example 2 (shell):
```shell
brew install ariga/tap/atlas
```

Example 3 (shell):
```shell
docker pull arigaio/atlasdocker run --rm arigaio/atlas --help
```

Example 4 (shell):
```shell
docker run --rm --net=host \  -v $(pwd)/migrations:/migrations \  arigaio/atlas migrate apply  --url "mysql://root:pass@:3306/test"
```

---

## Verifying Migration Safety

**URL:** https://atlasgo.io/versioned/lint

**Contents:**
- Verifying Migration Safety
  - Flags​
  - Changeset detection​
    - Compare against the latest state of the migration directory​
    - Analyze the latest N migration files​
    - Compare against a specific branch​
  - nolint directive​
    - Enforce Lint Checks Atlas Pro​
  - Open in the browser​
  - Output​

Atlas helps you ensure safe schema migrations for your database by automatically analyzing migration files for potentially dangerous or breaking changes. It is driven by the atlas migrate lint command, which can be used both locally and in CI pipelines at pull-request (merge-request) time.

Having this setup helps your team work collaboratively on database schemas, ensuring schema migrations are streamlined, safe, best practices are enforced, and no one steps on another's toes. Atlas analyzes every schema migration change in the migration directory for issues like:

While this command is commonly used locally, migration linting is frequently incorporated into CI pipelines, allowing teams to detect changes early before merging them into the main branch. Learn more about how to integrate Atlas into your GitHub Actions, GitLab CI Components, CircleCI, or Bitbucket Pipes workflows.

Starting with v0.38, the atlas migrate lint command is available only to Atlas Pro users. To enable it, run:

When using migrate lint to analyze migrations, users must supply multiple parameters:

When we run the lint command, we need to instruct Atlas on how to decide which set of migration files to analyze. Currently, three ways are supported. Let's go over them one by one:

Teams that have pushed their project to the Atlas Schema Registry (see setup for more details), can simply run the following command to analyze the changes detected by comparing the local state of the migration directory to the latest state, as defined in Atlas Cloud. For example, either by running atlas migrate push or by connecting it to a CI pipeline.

By using this method, Atlas warns you if your local migration directory is not up-to-date with the latest state of the project and rebasing is required. For example, while working on a feature branch, another team member might have pushed a new migration file to the main branch.

Here is an example of how a report of atlas migrate lint looks like:

Users can instruct Atlas to analyze the latest N migration files by running atlas migrate lint --latest N:

Similarly to the previous method, the -w/--web can be used to open the report in the browser, see the changes in ERD format, and more.

Users can instruct Atlas to detect which changes to analyze by comparing the current branch to a specific branch. For example, in order to analyze the changes between the current branch and the main branch, and open the report in the browser, run the following command:

Annotating a statement with the --atlas:nolint directive allows excluding it from the analysis reporting. For example:

Using --atlas:nolint excludes the annotated statement from all linters.

Using --atlas:nolint [names...] excludes reporting specific analyzers for the annotated statements.

Using --atlas:nolint [checks...] excludes reporting specific checks for the annotated statement.

The --atlas:nolint directive can be used to exclude the whole file (given at top) from analysis, or to exclude specific statements in the file from specific checks or analyzers.

Skip a specific analyzer for all statements in the file:

File directives are located at the top of the file and should not be associated with any statement. Hence, double new lines are used to separate file directives from its content.

By default, Atlas supports selectively skipping lint checks or analyzers by annotating statements or files with the -- atlas:nolint directive. This gives developers flexibility during development or CI to silence warnings or errors when they're intentional.

However, in some cases, project leaders might want to enforce that certain lint checks always run, setting stricter policies and preventing developers from skipping them. To support this, Atlas provides the force attribute for each analyzer and check in the atlas.hcl config file. When set, the analyzer will always run and report its diagnostics, even if explicitly excluded using the atlas:nolint directive.

In order to open the migration linting report in the browser, you first need to be logged in to Atlas, then use one of the example commands above with the -w/--web flag. For example:

Users may supply a Go template string as the --format parameter to format the output of the lint command.

CLI Command Reference

**Examples:**

Example 1 (unknown):
```unknown
atlas login
```

Example 2 (shell):
```shell
atlas migrate lint \  --dev-url "docker://mysql/8/dev" \  -w
```

Example 3 (shell):
```shell
atlas migrate lint \  --dev-url "docker://mariadb/latest/dev" \  -w
```

Example 4 (shell):
```shell
atlas migrate lint \  --dev-url "docker://postgres/15/test?search_path=public" \  -w
```

---

## Applying Schema Migrations

**URL:** https://atlasgo.io/versioned/apply

**Contents:**
- Applying Schema Migrations
  - Flags and Arguments​
  - Schema Revision Information​
  - Controlling Advisory Locks Atlas Pro​
  - Transaction Configuration​
    - File level transaction mode​
  - Execution Order​
    - Handling Out-of-Order Errors​
  - Pre-Execution Checks Atlas Pro​
  - Migration Hooks Atlas Pro​

With the atlas migrate apply command, users can apply pending migration files to database(s). The typical flow for introducing schema changes to databases is as follows: Develop ⇨ Check (CI) ⇨ Push (CD) ⇨ Deploy.

By default, atlas migrate apply executes all pending migration files. However, you can pass an optional argument to limit the number of migration files to apply. For instance, atlas migrate apply 2 will apply up to two pending migrations.

The following flags are required:

Users who have connected or pushed their migration directory to the Atlas Schema Registry can read the migrations' state directly from there without needing to have them locally. For example, atlas migrate apply --dir "atlas://app" will apply the pending migrations of the app project based on the most recent pushed state. To see it in action, run the following:

Push a local migration directory and name it app:

Deploy to a local database the remote migration directory named app:

Deploy a specific tag to a local database the remote migration directory named app:

Atlas saves information about the applied migrations on a table called atlas_schema_revisions in the connected database schema (e.g. mysql://user@host/my_schema or postgres://user@host/db?search_path=my_schema). If the database connection is not bound to a specific schema (e.g. mysql://user@host/ or postgres://user@host/db), the table is stored in its own schema called atlas_schema_revisions. This behavior can be changed by setting the schema manually:

Atlas takes an advisory lock while applying migrations to prevent conflicting parallel executions. By default, the lock name is atlas_migrate_execute. However, when multiple apps share the same databases and manage their own schema, this can serialize migration execution and slow down deployments. To address this, you can customize the advisory lock name using the --lock-name option (or migration.lock_name in the atlas.hcl file) to scope the lock per target.

By default, Atlas creates one transaction per migration file and will roll back that transaction if a statement in the wrapped migration fails to execute. However, users can control the transaction behavior using the --tx-mode flag. The following modes are supported:

Please be aware, that non DDL transactional databases like MySQL (due to implicit commits) can not be safely rolled back completely, and you might end up with a mismatched schema and revision table state. For guidance on handling this scenario, see Handling drift between my schema and the atlas_schema_revisions table. More information can be found in the PostgreSQL wiki.

The --atlas:txmode directive can be used to override the transaction mode for a specific migration file:

The --exec-order flag controls how Atlas computes and executes pending migration files to the database. Atlas supports three different order execution modes:

You've encountered this issue because your database is at version Z, but there is a file(s) in your migration directory pending to be applied with version Y, where Y < Z. This indicates it was added out of order, as its version is lower than the current database version. Below are multiple options to resolve it depending on your environment:

Local environment (development): Developers might encounter this issue if they have a migration file that was not yet pushed to the master branch (e.g., version Z), but upon pulling remote changes, new files with versions X and Y were added to the migration directory. In this scenario, there are two cases:

Real environment: If you encountered this issue during deployment, it means that Atlas was not set up in your CI, which is why the issue was not detected beforehand. Let's go through the steps to fix the error and set up Atlas in your CI to prevent this issue from happening again:

Pre-execution checks allow you to define policy rules that are evaluated before migrations are applied via the atlas migrate apply command. These rules are defined in a check block, which can contain both allow and deny clauses:

Rules are evaluated before Atlas begins applying any migration files, allowing teams to prevent dangerous or time-sensitive operations. For example, you can block applying more than X files at once or disallow specific SQL statements during peak hours.

Checks have access to the self.planned_migration object, which exposes the statements and files in the planned migration:

The example below blocks the migration if more than 3 files are pending:

The example below blocks migrations that include CREATE INDEX statements during peak hours. By default, peak hours are defined as 10:00–14:00 UTC in this example, but you can customize this window by setting the start_peak_hour and end_peak_hour variables.

Rather than repeating the checks in every environment, declare them once at the global level so all environments share them. Atlas evaluates the global checks first and only then applies any environment-specific checks. Use the atlas.env variable when you need to tailor logic to the current environment.

Migration hooks let you inject SQL statements that run inside the migration connection and transaction. These are commonly used to configure session-level settings such as statement_timeout or lock_timeout in PostgreSQL to prevent migrations from blocking other ongoing operations.

To run custom scripts before or after a migration (for example, taking snapshots, seeding lookup tables, or cleaning up after deployment), refer to the pre/post deployment hooks documentation.

If you have an existing database project and want to switch over to Atlas Versioned Migrations, you need to provide Atlas with a starting point. The first step is to create a migration file reflecting the current schema state. This can be easily done:

Atlas will generate a "baseline" file from the database schema. For example:

Regardless of whether you added additional migration files after the baseline, you need to specify the baseline version during your first migration execution. Atlas will mark this version as already applied and proceed with the next version after it. For example:

📺 For a step-by-step example walk-through, watch our 3-minute tutorial: Versioned Migrations for Existing Databases using Atlas

If your database contains resources but no revision information yet, Atlas will refuse to execute migration files. One way to override that behavior is by using the --baseline flag. However, in cases where existing tables are not managed by Atlas at all and should not be part of a baseline file, you can run the first migration execution with the --allow-dirty flag to operate on a non-clean database.

Atlas allows users to review and verify the safety of migration plans before applying them to the database.

By using the dry-run option, Atlas prints the migration files and their SQL statements that are pending to be applied without executing them. However, if the migration plan contains pre-migration checks, Atlas executes them on the database and report the results.

Migrations that "roll back" or reverse changes made to the database schema are called "down migrations". These are often used during local development to undo the changes made by corresponding "up migrations". Atlas follows a linear migration history model, in which all migration files are "roll-forward". However, it is still possible to clean or revert schema changes made by specific migration files using the atlas migrate down command. For full details, see the down migration documentation.

In addition to the --dry-run flag Atlas also provides the atlas migrate status command, that provides in-depth information about the migration status of the connected database.

The Atlas configuration language provides built-in support for executing versioned workflows in multi-tenant environments. Using the for_each meta-argument, users can define a single env block that is expanded to N instances, one for each tenant:

Read more about how to define versioned workflows using project files in multi-tenant environments.

In PostgreSQL, there are three ways to isolate tenants: schema-level, database-level, and instance-level.

If tenants are managed at the schema level, the tenant migration URL should set the database name (which may be shared across multiple tenants) and the schema name (the dynamic part). To achieve this, use the urlqueryset function to set the search_path query parameter. For example:

If tenants are managed at the database level - meaning each tenant has its own PostgreSQL database (potentially using multiple schemas), set the URL path dynamically using the urlsetpath function. For example:

If tenants are managed at the instance level the tenant migration should use the full database URL directly. For example:

Unlike PostgreSQL, in MySQL and MariaDB, tenants are typically managed at either the schema (database) level or the instance level.

If tenants are managed at the schema level, the URL path defines the tenant's schema name. You can set it dynamically using the urlsetpath function. For example:

If tenants are managed at the instance level (e.g., the tenant spans multiple schemas), the tenant migration uses the full database URL directly. For example:

In SQL Server, there are two ways to isolate tenants: database-level, and schema-level.

The database-level isolate way can be used when each tenant has its own database; this option is commonly used, and the URL parameter database defines the tenant's database name. You can set it dynamically using the urlqueryset function. For example:

The schema-level isolation way is used when each tenant has its schema, this option is rarely used. The schema is scoped to the login user. You can set it dynamically using the urluserinfo function. For example:

When applying schema migrations to multiple tenants, you can use Atlas's deployment block to define staged rollout strategies with fine-grained control over execution order, parallelism, and error handling:

This configuration first deploys to the canary tenant, then to all free-tier tenants in parallel (up to 10 at a time), and finally to paid tenants (up to 3 at a time).

Read more about deployment rollout strategies for multi-tenant environments.

First time apply with baseline on production environment:

Execute 1 pending migration file, but don't run, but print SQL statements on screen:

Specify revision table schema and custom migration directory path:

Ignore unclean database and run the first 3 migrations:

Run all pending migrations, but do not use a transaction:

Show information about the migration status of a deployment:

CLI Command Reference

**Examples:**

Example 1 (shell):
```shell
atlas login
```

Example 2 (bash):
```bash
atlas migrate push app \  --dev-url "docker://postgres/15/dev?search_path=public"
```

Example 3 (bash):
```bash
atlas migrate push app \  --dev-url "docker://mysql/8/dev"
```

Example 4 (bash):
```bash
atlas migrate push app \  --dev-url "docker://mariadb/latest/dev"
```

---

## Safeguarding Migrations with Pre-Execution Checks

**URL:** https://atlasgo.io/versioned/checks

**Contents:**
- Safeguarding Migrations with Pre-Execution Checks
  - atlas:txtar directive​
  - atlas:assert directive​
  - Examples​
    - Pre-execution checks passed​
    - Pre-execution checks failed​

Atlas supports the concept of pre-migration checks, where each migration version can include a list of assertions (predicates) that must evaluate to true before the migration is applied. For example, before dropping a table, we aim to ensure that no data is deleted and the table must be empty, or we check for the absence of duplicate values before adding a unique index to a table.

Pre-migration checks are available only to Atlas Pro users. To use this feature, run:

Atlas supports a text-based file archive to describe "migration plans". Unlike regular migration files, which mainly contain a list of DDL statements (with optional directives), Atlas txtar files can include multiple file entries such as:

Each file entry in the archive starts with a marker line formatted as -- FILENAME -- and is followed by one or more lines containing the file content (e.g., SQL statements, assertions, etc.). The file ends at the next marker line or when the archive ends. For example:

The code below presents the most standard example of pre-migration checks. The default checks file is named checks.sql, and the migration.sql file contains the actual DDLs to be executed on the database in case the assertions are passed.

The example below presents a case where an archive file includes two check files:

The atlas:txtar file directive is located at the top of the migration file and should not be associated with any statement. Therefore, double new lines (\n\n) are used to separate file directives from its content.

The atlas:assert directive is used in pre-migration check files to control assertion behavior. The directive can be set on both check files and individual assertion statements. For example:

Using the atlas:assert directive on a specific assertion statement indicates that it corresponds to a particular lint check or a set of checks that should not be reported as warnings or errors.

Using the atlas:assert directive with the oneof value on a check file indicates that at least one of the assertions must pass for the check file to be considered successful.

Executing the migration examples defined above will result in the following output:

If the pre-execution checks pass, the migration will be applied, and Atlas will report the results.

If the pre-execution checks fail, the migration will not be applied, and Atlas will exit with an error.

**Examples:**

Example 1 (unknown):
```unknown
atlas login
```

Example 2 (sql):
```sql
-- atlas:txtar-- checks.sql ---- The assertion below must be evaluated to true. Hence, table users must be empty.SELECT NOT EXISTS(SELECT * FROM users);-- migration.sql ---- The statement below will be executed only if the assertion above is evaluated to true.DROP TABLE users;
```

Example 3 (sql):
```sql
-- atlas:txtar-- checks/users.sql ---- All assertions below must be evaluated to true. The tables mentioned below must be empty.SELECT NOT EXISTS(SELECT * FROM internal_users);SELECT NOT EXISTS(SELECT * FROM external_users);-- checks/roles.sql ---- atlas:assert oneof-- At least one of the assertions below must be evaluated to true. Hence, we drop-- the "roles" table only if it is empty, or there are no associations to it.SELECT NOT EXISTS(SELECT * FROM roles);SELECT NOT EXISTS(SELECT * FROM user_roles);-- migration.sql ---- The statements below will be executed only if the check files above are passed.DROP TABLE internal_users;DROP TABLE external_users;DROP TABLE roles;
```

Example 4 (sql):
```sql
-- atlas:txtar-- checks/destructive.sql ---- atlas:assert DS102SELECT NOT EXISTS (SELECT 1 FROM "users") AS "is_empty";-- migration.sql ---- drop "users" tabledrop table users;
```

---
