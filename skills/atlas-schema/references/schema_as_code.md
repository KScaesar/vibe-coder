# Atlas-Schema - Schema As Code

**Pages:** 8

---

## SQL Schema: Syntax and Examples

**URL:** https://atlasgo.io/atlas-schema/sql

**Contents:**
- SQL Schema: Syntax and Examples
- Dev Database​
- Schema Definition​
- Schema File​
- Schema Directory​
- atlas Directives​
  - File-Level Directives​
  - Statement-Level Directives​
- Importing System​
- Sensitive Values​

Atlas supports defining your database schema as code, whether with its own HCL language to external ORMs, programs, or the standard SQL. This guide focuses on defining schemas using SQL syntax, but also covers other methods. There are multiple ways to define schemas in SQL, such as using a single SQL schema file, a directory, or Go template-based directory. All of these methods are covered below.

When working with SQL schemas, Atlas requires a URL to a Dev Database, specified via the --dev-url flag (or the dev attribute in atlas.hcl). Typically, this is a temporary database running locally, used to parse and validate the SQL definition. This requirement is necessary as Atlas cannot replicate every database type 'X' in every version 'Y'.

To simplify the process of creating temporary databases for one-time use, Atlas can spin up an ephemeral local Docker container using the special docker driver, and clean it up at the end of the process. Here are a few examples of how to use the docker driver:

Once the dev-database is set, Atlas utilizes it to convert the provided raw SQL files and statements into the Atlas "schema graph", that then can be used by various layers of the engine to diff, plan, and apply changes onto the target database. It's important to note that Atlas loads the raw SQL schema by executing the statements defined in the files one by one. As such, it is expected that files and statements are ordered according to their dependencies. For example, if a VIEW named v1 depends on TABLE named t1, v1 must be defined after t1, either in the same file or in a separate one.

As mentioned above, Atlas uses the dev database to compute the desired state of the database schema. Therefore, before starting its work, Atlas ensures the dev database is clean and there are no leftovers from previous runs. Once done, Atlas cleans up after itself and the dev database is ready for future runs.

An SQL schema defined in a single file is typically named schema.sql and composed of multiple DDL statements separated by a semicolon (;) or a custom delimiter, which can be validly executed onto a database one after the other.

In order to use an SQL schema file as an Atlas state, use the following format: file://path/to/schema.sql.

For larger schemas, you can break the definition into smaller, modular files using the atlas:import directive. This allows you to keep your schema organized while ensuring dependencies are properly resolved.

An SQL schema directory includes one or more schema files, ordered lexicographically according to their dependencies. For example, a table with foreign keys must be defined after the other tables it references, and a view should also be defined after the other tables and views it depends on.

In order to use a schema directory as an Atlas state, use the following format: file://path/to/dir.

SQL files in Atlas support directives, which are standard SQL comments that instruct Atlas on how to handle the SQL file at different stages of execution. For example, directives can control how the file is parsed when read by Atlas, disable linting warnings for specific statements or files, configure the transaction mode for a specific file, and more.

There are two types of directives:

File-level directives appear at the top of the file and should not be associated with any specific statement. To separate file directives from the rest of the content, double new lines (\n\n) are used. For example:

The following file-level directives are supported by Atlas:

Statement-level directives are attached to specific statements within the SQL file. They should be included in the statement comment(s). For example:

The following statement-level directives are supported by Atlas:

Atlas supports importing SQL files and directories into other SQL files using the atlas:import directive. Such directives must be placed at the top of the file and separated from the rest of the content by two blank lines (\n\n). If a file is imported more than once, Atlas will include it only the first time it appears. If an import cycle is detected, Atlas will raise an error.

This feature makes it easy to break large SQL schema definitions into smaller parts while keeping them correct and ordered. Each schema chunk (file) explicitly declares the other schema resources it depends on to function properly. For example:

📺 For a step-by-step example walk-through, watch our 5-minute tutorial: Modular SQL Schema Definitions

Migration files can sometimes include sensitive or PII values, either passed in as input variables (using template-directories) or embedded directly in SQL statements. To prevent these values from being logged, Atlas provides a directive for marking files or specific statements as sensitive. This directive can be set at either the file or statement level.

By default, Atlas masks SQL string literals with the (sensitive) placeholder. However, the -- atlas:sensitive directive can be configured with one or more patterns, giving you more control over which parts should be matched and replaced.

The example below demonstrates how to create a migration with sensitive directives:

Atlas supports computing the desired schemas dynamically using Go templates and injected variables. To set it up for a project, create an atlas.hcl config file, if you don't already have one. Then, declare a new data source of type template_dir that can be used later as an Atlas schema.

**Examples:**

Example 1 (shell):
```shell
# When working on a single database schema.--dev-url "docker://mysql/8/schema"# When working on multiple database schemas.--dev-url "docker://mysql/8"
```

Example 2 (shell):
```shell
# When working on a single database schema.--dev-url "docker://maria/latest/schema"# When working on multiple database schemas.--dev-url "docker://maria/latest"
```

Example 3 (shell):
```shell
# When working on a single database schema, use the auth-created# "public" schema as the search path.--dev-url "docker://postgres/15/dev?search_path=public"# When working on multiple database schemas.--dev-url "docker://postgres/15/dev"
```

Example 4 (shell):
```shell
# Atlas supports working with an in-memory database in SQLite.--dev-url "sqlite://dev?mode=memory"
```

---

## Schema as Code: HCL Syntax

**URL:** https://atlasgo.io/atlas-schema/hcl

**Contents:**
- Schema as Code: HCL Syntax
- Editor Support​
  - File Naming for Editor Support​
- Schema​
- Table​
  - Check​
  - Partitions​
    - Defining Partitions​
    - Computed Partitions​
  - Foreign Tables​

Atlas enables you to define your database schema as code, whether in SQL, through ORMs, custom programs, or the Atlas HCL language. The HCL-based language allows developers to describe database schemas in a declarative manner, and it supports all SQL features supported by Atlas. The main advantages of using HCL are that it enables developers to manage their database schemas like regular code, facilitates sharing and reusing files between projects, allows variable injection, and provides the ability to attach annotations to objects, such as PII or sensitive data.

The Atlas HCL language provides plugins for popular editors like VSCode and JetBrains to enhance your day-to-day editing, navigation, formatting, and testing experience.

To enable your editor to recognize Atlas HCL files and provide syntax support, use the following file extensions:

Name your files accordingly, for example: warehouse_schema.pg.hcl for PostgreSQL, test_users.test.hcl for a test file.

The schema object describes a database schema. A DATABASE in MySQL and SQLite, or a SCHEMA in PostgreSQL. An HCL file can contain 1 or more schema objects.

In MySQL and MariaDB, the schema resource can contain the charset and collate attributes. Read more about them in MySQL or MariaDB websites.

Atlas does not support attached databases, and support only the default database (i.e. main).

In Clickhouse, the schema resource can contain the engine attribute. If not specified, the default engine depends on ClickHouse settings. Use sql() to specify the engine in advanced cases.

Read more about database engines in ClickHouse documentation.

A table describes a table in a SQL database. A table hold its columns, indexes, constraints, and additional attributes that are supported by the different drivers.

A check is a child resource of a table that describes a CHECK constraint.

The partition option is a PostgreSQL-specific option that allows defining partitioned tables. Table partitioning refers to splitting logical large tables into smaller physical ones.

Partitions are available only to Atlas Pro users. To use this feature, run:

The top-level partition block allows defining partitions. The of attribute is used to specify the parent table that the partition belongs to, and the range, list and hash attributes are used to define the partition boundaries.

The HCL language allows defining computed partitions using the for_each meta-argument. This is useful for creating partitions based on dynamic values, such as dates or other computed values. For example, given the logs table below, the following HCL code maintains partitions for the last 7 days, creating a new partition each day and deleting old ones.

The foreign_table option is a PostgreSQL-specific block that allows defining a foreign table. A foreign table is a table that is not local to the current database but is defined in another database.

The row_security option is a PostgreSQL-specific option that allows enabling row-level security policies for a table.

To define row-level security policies for a table, refer to the policy example.

The fulltext option is a SQL Server-specific option that allows enabling full-text index for a table.

To able to use this feature, you need to enable the Full-Text Search feature in SQL Server both on the production server and the devdb. Bellow is example of enabling the feature on the devdb, with custom dockerfile.

The content is taken from this example on the official Microsoft repository.

Then we can run atlas schema inspect --env local --url "env://src" to get the schema in HCL format.

To use full-text indexes in MySQL, you need to create a full-text index on the table.

In some cases, an Atlas DDL document may contain multiple tables of the same name. This usually happens when the same table name appears in two different schemas. In these cases, the table names must be disambiguated by using resource qualifiers. The following document describes a database that contains two schemas named a and b, and both of them contain a table named users.

The engine attribute allows for overriding the default storage engine of the table. Supported by MySQL, MariaDB and ClickHouse.

In ClickHouse, the engine can be specified using either enumerated values or string literals

For complex engines, use the sql() function to specify the engine in advanced cases.

The TimeSeries engine is designed to optimize storage and query performance for time-series data. To create a table with the TimeSeries engine, use the following syntax:

Use the engine block to specify the TimeSeries engine with External Target Tables.

For adjusting the types of columns, specify them explicitly while defining the TimeSeries table.

Inner UUID of the TimeSeries engine is not supported by Atlas currently.

System-Versioned tables are available only to Atlas Pro users. To use this feature, run:

The system_versioned block allows marking a table as a system-versioned temporal table. Supported by SQL Server. This block can be used to define the history table, retention period, and the period unit.

The period block defines the period columns for the system-versioned table. It requires two columns: start and end, which are used to define the period of validity for each row. These columns must be of type datetime2, non-nullable, and have the generated always as row start and row end respectively.

The system_versioned attribute allows marking a table as a system-versioned table. Supported by MariaDB.

The distribution block is a Redshift-specific option that allows specifying the distribution method of the table.

The sort block is a Redshift-specific option that allows specifying the sorting method of the table.

Redshift restricts user access to certain external tables which are used to inspect the sort style. Therefore, Atlas will ignore differences when changing the style to AUTO. You will need to manually adjust the sort style on your target Redshift database after modifying it in the Atlas schema.

To change the sort style to AUTO, run the following SQL command:

A view is a virtual table in the database, defined by a statement that queries rows from one or more existing tables or views.

Views are available only to Atlas Pro users. To use this feature, run:

Atlas's testing framework allows you to write unit tests for your views. The following example demonstrates how to write tests for the clean_users view defined above. For more detail, read the schema testing docs or see the full example.

A materialized view is a table-like structure that holds the results of a query. Unlike a regular view, the results of a materialized view are stored in the database and can be refreshed periodically to reflect changes in the underlying data.

Materialized views are available only to Atlas Pro users. To use this feature, run:

When creating materialized views with TO [db.]table, the view will be created with the same structure as the table or view specified in the TO clause.

The engine and primary_key attributes are required if the TO clause is not specified. In this syntax, populate can be used for the first time to populate the materialized view.

A column is a child resource of a table.

Generated columns are columns whose their values are computed using other columns or by deterministic expressions.

Note, it is recommended to use the --dev-url option when generated columns are used.

Encodings are used to define the compression algorithm for the column data. Supported by ClickHouse and Redshift.

The SQL dialects supported by Atlas (Postgres, MySQL, MariaDB, and SQLite) vary in the types they support. At this point, the Atlas DDL does not attempt to abstract away the differences between various databases. This means that the schema documents are tied to a specific database engine and version. This may change in a future version of Atlas as we plan to add "Virtual Types" support. This section lists the various types that are supported in each database.

For a full list of supported column types, click here.

A primary_key is a child resource of a table, and it defines the table's primary key.

Note, primary key expressions are supported by ClickHouse.

Foreign keys are child resources of a table, and it defines some columns in the table as references to columns in other tables.

If a foreign key references a column in a qualified table, it is referenced using table.<qualifier>.<table_name>.column.<column_name>:

Indexes are child resources of a table, and it defines an index on the table.

Index expressions allow setting indexes over functions or computed expressions. Supported by PostgreSQL, SQLite and MySQL8.

Note, it is recommended to use the --dev-url option when index expressions are used.

Partial indexes allow setting indexes over subset of the table. Supported by PostgreSQL and SQLite.

Note, it is recommended to use the --dev-url option when partial indexes are used.

Index prefixes allow setting an index on the first N characters of string columns. Supported by MySQL and MariaDB.

The unique block allows defining a unique constraint supported by PostgreSQL:

In order to add a unique constraint in non-blocking mode, the index supporting the constraint needs to be created concurrently first and then converted to a unique constraint. To achieve this, follow the steps below:

The exclude block allows defining a exclusion constraint supported by PostgreSQL:

The storage_params block allows configuring the storage parameters of the index. Supported by PostgreSQL.

Atlas supports defining IVFFlat indexes when the vector extension is defined in the schema, enabling efficient similarity searches by organizing vectors into lists and searching only those closest to the query vector. Atlas Pro

Atlas supports defining HNSW indexes when the vector extension is defined in the schema. Atlas Pro

Triggers are available only to Atlas Pro users. To use this feature, run:

The trigger block allows defining SQL triggers in HCL format.

To configure the same trigger for multiple tables/views, users can utilize the for_each meta-argument. By setting it up, a trigger block will be computed for each item in the provided value. Note that for_each accepts either a map or a set of references.

Event Triggers are available only to Atlas Pro users. To use this feature, run:

The event_trigger block allows defining PostgreSQL event trigger functions that automatically execute in response to specific events within the database system, like table creation or schema modifications.

Functions are available only to Atlas Pro users. To use this feature, run:

The function block allows defining functions in HCL format. The lang attribute specifies the language of the function. For example, PLpgSQL, SQL, CRL, etc.

Atlas's testing framework allows you to write unit tests for your functions. The following example demonstrates how to write tests for the positive function defined above. For more detail, read the schema testing docs or see the full example.

The aggregate block defines a function that computes a single result from a set of values. Supported by PostgreSQL.

Procedures are available only to Atlas Pro users. To use this feature, run:

The procedure block allows defining SQL procedure in HCL format.

Atlas's testing framework allows you to write unit tests for your procedures. The following example demonstrates how to write tests for a stored procedure, archive_old_sales, that moves old sales from the sales table to the archive_sales table according to a specified cutoff date. For more detail, read the schema testing docs or see the full example.

Domains are available only to Atlas Pro users. To use this feature, run:

The domain type is a user-defined data type that is based on an existing data type but with optional constraints and default values. Supported by PostgreSQL.

Atlas's testing framework allows you to write unit tests for your domains. The following example demonstrates how to write tests for the us_postal_code domain defined above. For more detail, read the schema testing docs or see the full example.

Composite types are available only to Atlas Pro users. To use this feature, run:

The composite type is a user-defined data type that represents the structure of a row or record. Supported by PostgreSQL.

Range types are available only to Atlas Pro users. To use this feature, run:

Range types in Postgres are types that store a range of values for a specific subtype such as timestamps or numbers, allowing you to query for overlaps, containment, and boundaries.

Using the builtin range types provided by PostgreSQL, such as int4range, numrange, tsrange, and tstzrange, does not require custom definitions

You can use the multirange_name attribute to customize the name of the multirange type that is automatically created by PostgreSQL when defining a range type. If omitted, PostgreSQL generates a default name according to the following rules:

If the range type name contains the substring range, then the multirange type name is formed by replacement of the range substring with multirange in the range type name. Otherwise, the multirange type name is formed by appending a _multirange suffix to the range type name.

Note, Atlas hides the auto-created constructor functions for both the range and multirange types, along with the multirange type itself, since these are PostgreSQL internals that cannot be edited by the user and are automatically removed when the range type is dropped.

Policies are available only to Atlas Pro users. To use this feature, run:

The policy block allows defining row-level security policies. Supported by PostgreSQL.

To enable and force row-level security on a table, refer to the table row-level security example.

To configure the same policy for multiple tables, users can utilize the for_each meta-argument. By setting it up, a policy block will be computed for each item in the provided value. Note that for_each accepts either a map or a set of references.

Sequences are available only to Atlas Pro users. To use this feature, run:

The sequence block allows defining sequence number generator. Supported by PostgreSQL and SQL Server.

Note, a sequence block is printed by Atlas on inspection, or it may be manually defined in the schema only if it represents a PostgreSQL sequence that is not implicitly created by the database for identity or serial columns.

Atlas support define sequence in SQL Server by using sequence block. See more about SQL Server sequence.

The enum type allows storing a set of enumerated values. Supported by PostgreSQL.

Extensions are available only to Atlas Pro users. To use this feature, run:

The extension block allows the definition of PostgreSQL extensions to be loaded into the database. The following arguments are supported:

Although the schema argument is supported, it only indicates where the extension's objects will be installed. However, the extension itself is installed at the database level and cannot be loaded multiple times into different schemas.

Therefore, to avoid conflicts with other schemas, when working with extensions, the scope of the migration should be set to the database, where objects are qualified with the schema name. To learn more about the difference between database and schema scopes, visit this doc.

Foreign-servers are available only to Atlas Pro users. To use this feature, run:

The server block defines a foreign server in the database, containing the connection details needed to access an external data source via a foreign-data wrapper. This feature is supported by PostgreSQL.

Foreign servers are defined at the database level, and their names must be unique within the database.

Therefore, when working with foreign servers, the scope of the migration should be set to the database, where bjects are qualified with the schema name. To learn more about the difference between database and schema scopes, visit this doc.

The comment attribute is an attribute of schema, table, column, and index.

The charset and collate are attributes of schema, table and column and supported by MySQL, MariaDB and PostgreSQL. Read more about them in MySQL, MariaDB and PostgreSQL websites.

SQLServer only support collate attribute on columns.

AUTO_INCREMENT and IDENTITY columns are attributes of the column and table resource, and can be used to generate a unique identity for new rows.

In MySQL/MariaDB the auto_increment attribute can be set on columns and tables.

The auto_increment column can be set on the table to configure a start value other than 1.

PostgreSQL supports serial columns and the generated as identity syntax for versions >= 10.

SQLite allows configuring AUTOINCREMENT columns using the auto_increment attribute.

**Examples:**

Example 1 (markdown):
```markdown
# Schema with attributes.schema "market" {  charset = "utf8mb4"  collate = "utf8mb4_0900_ai_ci"  comment = "A schema comment"}# Schema without attributes.schema "orders" {}
```

Example 2 (unknown):
```unknown
schema "public" {  comment = "A schema comment"}schema "private" {}
```

Example 3 (unknown):
```unknown
schema "main" {}
```

Example 4 (unknown):
```unknown
schema "dbo" {  comment = "A schema comment"}schema "private" {}
```

---

## Schema as Code: ORMs and External Tools

**URL:** https://atlasgo.io/atlas-schema/external

**Contents:**
- Schema as Code: ORMs and External Tools
- Loading an External Schema​
- Supported ORMs​
- Write an external loader​

Atlas supports loading the desired state of your database schema directly from code, enabling true Schema as Code workflows. Whether your schema is generated by popular ORMs or external tools, regardless of programming language, Atlas can seamlessly integrate with it. Once loaded, the schema can be used by the various workflows and commands such as atlas schema and atlas migrate.

Click here for guides on using various ORMs with Atlas

In order to load an external schema, you need first to create an atlas.hcl config file, if you don't already have one and declare a new data source of type external_schema that can be used later as the desired state. Let's explain this with an example.

Given the following atlas.hcl file:

Let's explain what is happening when running atlas with the --env orm command:

Atlas supports loading the desired schema from popular ORMs in various languages. By connecting their ORM to Atlas, developers can manage their Database as Code, allowing them to define and edit the schema using familiar ORM syntax. Atlas automatically plans schema migrations for them, eliminating the need to write them manually and enabling them to extend their ORMs with features not supported natively, such as triggers, row-level security, or functions. The supported ORMs are:

If you are using an ORM that is not listed here and would like to see it supported, let us know!

Most ORMs offer a way to generate a series of DDL statements from model definitions. For example, Java Hibernate enables "schema exporting" using the hbm2ddl option, and Microsoft EF supplies a helper method called GenerateCreateScript that lets users craft a small script to produce DDLs from their EF models. In a similar way, TypeORM users can use the createSchemaBuilder().log() API, and so on.

A fully working implementation can be found in the atlas-provider-gorm repository, which is an external loader for the GORM ORM.

**Examples:**

Example 1 (unknown):
```unknown
data "external_schema" "orm" {  # The first argument is the command to run,  # and the rest are optional arguments.  program = [    "npm",    "run",    "generate-schema"  ]}env "orm" {  src = data.external_schema.orm.url  dev = "docker://mysql/8/dev"}
```

Example 2 (unknown):
```unknown
data "external_schema" "orm" {  # The first argument is the command to run,  # and the rest are optional arguments.  program = [    "npm",    "run",    "generate-schema"  ]}env "orm" {  src = data.external_schema.orm.url  dev = "docker:/maria/latest/dev"}
```

Example 3 (unknown):
```unknown
data "external_schema" "orm" {  # The first argument is the command to run,  # and the rest are optional arguments.  program = [    "npm",    "run",    "generate-schema"  ]}env "orm" {  src = data.external_schema.orm.url  dev = "docker://postgres/15/dev?search_path=public"}
```

Example 4 (unknown):
```unknown
data "external_schema" "orm" {  # The first argument is the command to run,  # and the rest are optional arguments.  program = [    "npm",    "run",    "generate-schema"  ]}env "orm" {  src = data.external_schema.orm.url  dev = "sqlite://dev?mode=memory"}
```

---

## Inspecting Existing Database Schemas

**URL:** https://atlasgo.io/inspect

**Contents:**
- Inspecting Existing Database Schemas
- Flags​
- Inspect a Database​
- Inspect a Single Schema​
- Write the Output to a File​
- Inspect Multiple Schemas​
- Exclude Schemas​
- Exclude Database Objects​
- Exclude Schema Resources​
- Exclude Tables​

Atlas provides a command-line tool to inspect existing database schemas and generate their Atlas HCL definitions. With automatic schema inspection, simply provide a connection string to the target database and Atlas will print out its schema definition.

This allows users to see the current state of their schema and save it as the source of truth, enabling them to manage their schema as code with Atlas.

By default, running atlas schema inspect inspects only schemas, tables, and their associated indexes and constraints such as foreign keys and checks.

Views, materialized views, functions, procedures, triggers, sequences, domains, extensions, and additional database features are available to Atlas Pro users. To include these resources in the inspection, use the following command:

When using schema inspect to inspect an existing database, users may supply multiple parameters:

Exclude schemas that match a glob pattern from the inspection:

Exclude database objects that match a glob pattern from the inspection:

Exclude schema resources (objects) that match a glob pattern from the inspection:

When inspecting a database (multiple schemas), the first glob pattern matches the schema name, and the second matches the object name:

When inspecting a specific schema, the first glob pattern matches the object name:

Exclude tables that match a glob pattern from the inspection:

When inspecting a database (multiple schemas), the first glob pattern matches the schema name, and the second matches the table name:

When inspecting a specific schema, the first glob pattern matches the table name:

By default, the type=table selector excludes all table types, including base tables, partitions, and foreign tables. If you want to exclude a specific type of table, such as partition or foreign_table, you can use more fine-grained selectors like type=partition or type=foreign_table. For example:

Exclude columns, indexes, or foreign-keys that match a glob pattern from the inspection:

When inspecting a database (multiple schemas), the first glob pattern matches the schema name, and the second matches the table name:

When inspecting a specific schema, the first glob pattern matches the table name:

Include only schemas that match a glob pattern during inspection:

Include only schema resources (objects) that match a glob pattern from the inspection:

When inspecting a database (multiple schemas), the first glob pattern matches the schema name, and the second matches the object name:

When inspecting a specific schema, the glob pattern matches the object name:

Include only tables that match a glob pattern from the inspection. All other resources will be excluded:

When inspecting a database (multiple schemas), the first glob pattern matches the schema name, and the second matches the table name:

When inspecting a specific schema, the first glob pattern matches the table name:

Include only triggers that match a glob pattern from the inspection. All other resources will be excluded:

When inspecting a database (multiple schemas), the first glob pattern matches the schema name, and the second matches the table name:

When inspecting a specific schema, the first glob pattern matches the table name:

By default, the output of schema inspect is in the Atlas DDL. However, you can use SQL to describe the desired schema in all commands that are supported by Atlas DDL. To output the schema in SQL format, use the --format flag as follows:

Atlas can output a JSON document that represents the database schema. This representation allows users to use tools like jq to analyze the schema programmatically.

Atlas can generate an Entity Relationship Diagram (ERD) for the inspected schemas. The following command shows how to generate an ERD for inspected schemas:

CLI Command Reference

**Examples:**

Example 1 (shell):
```shell
atlas login
```

Example 2 (shell):
```shell
atlas schema inspect -u "postgres://localhost:5432/database"atlas schema inspect -u "postgres://postgres:pass@localhost:5432/database?sslmode=disable"
```

Example 3 (shell):
```shell
atlas schema inspect -u "mysql://localhost"atlas schema inspect -u "mysql://user:pass@localhost:3306"
```

Example 4 (shell):
```shell
atlas schema inspect -u "maria://localhost"atlas schema inspect -u "maria://user:pass@localhost:3306"
```

---

## Export Database Schema to Code

**URL:** https://atlasgo.io/inspect/database-to-code

**Contents:**
- Export Database Schema to Code
- Split Your Schema into Multiple Files​
  - split​
    - Split Database Scope​
    - Split Schema Scope​
  - write​
  - Examples​
- Video Tutorial​
- Next Steps​
      - Versioned Migrations

The atlas schema inspect command can read an existing schema from a live database or any supported schema format, such as HCL, SQL, or an ORM schema, and generate an equivalent representation in HCL or SQL. This lets you capture the current state of a schema as code so it can be stored, modified, or used in migration workflows in a version-controlled environment.

By default, the entire schema is written to standard output as a single file. For larger projects or cases where you want a structured layout, Atlas provides built-in functions like split and write to automatically organize the output into multiple files and directories. This makes it easy to inspect, edit, and maintain your schema as code in version control systems.

First, specify the format of the output (HCL or SQL) using the --format flag.

Then, pipe it to the split and write functions to separate the schema objects into multiple files and write them to the current directory. The output files will be named according to the object name and type.

The split function splits schema dumps into multiple files and produces a txtar formatted output. The result is then piped to the write function to write the output to files and directories.

The API for the split function depends on the input format used, either hcl or sql:

When used with the sql function, the split function splits the SQL schema dump into multiple files and subdirectories with different formats based on the scope you inspect - either a database or a specific schema.

If you inspect a database scope with more than one schema Atlas will generate a directory for each schema, and subdirectories for each object type defined in that schema. Database-level objects, such as PostgreSQL extensions, will be generated in their own directory alongside the schemas directory.

Each object will be defined in its own file within the its type's directory, along with atlas:import directives pointing to its dependencies.

A main.sql file will also be generated as an "entry point", containing import lines for all files generated by Atlas. This allows you to point to the entire schema just by referencing the main.sql file (e.g., file://path/to/main.sql).

A typical output might look like:

When inspecting a specific schema, Atlas will only generate subdirectories for each object type defined in that schema.

Each object will be defined in its own file within the its type's diretory, along with atlas:import directives pointing to its dependencies.

In addition, a main.sql file will be generated as an "entry point", containing import lines for all files generated by Atlas. This allows you to easily point to the entire schema by referencing the main.sql file (e.g., file://path/to/main.sql).

Note that database objects such as schemas and extensions will not be generated. Additionally, CREATE statements will not be qualified with the schema name, so you can use the generated files in a different schema set by the URL.

A typical output might look like:

The split function takes two optional arguments: strategy and suffix.

The strategy argument states how the output is split. The following strategies are supported:

The suffix argument defines the suffix of the output files, .hcl by default. It is recommended to use a database specific suffix for better editor plugin support, for example:

To work with this directory structure, use the hcl_schema data source in your atlas.hcl project configuration:

The write function takes one argument: path.

The path argument states the directory where the output files will be written. The path can be relative or absolute. If no path is specified, the output files will be written to the current directory.

The write function creates the directory if it does not exist.

Default split and write to the current directory:

Write to the project/ directory:

Customize indentation to \t and write to the project/ directory:

Default split and write to the current directory:

Split by object type and write to the schema/ directory for PostgreSQL:

Split by schema and write to the schema/ directory for MySQL:

To see this process in action, check out our video tutorial that covers the entire process using a PostgreSQL schema and SQL-formatted output.

After exporting your database schema to code, you can leverage this code in various ways to manage and evolve your database schema effectively. Here are some recommended next steps:

Manage your schema changes through versioned migration files. Use the atlas migrate diff command to generate migrations, atlas migrate apply to apply them, and integrate Atlas into your CI/CD pipeline for safe, auditable deployments.

Manage your schema declaratively by defining the desired state as code, and let Atlas plan and apply the changes using atlas schema apply. To review or approve changes before applying them, use atlas schema plan to pre-plan and approve migrations in advance.

**Examples:**

Example 1 (shell):
```shell
# HCL.atlas schema inspect -u '<url>' --format '{{ hcl . | split | write }}'# SQL.atlas schema inspect -u '<url>' --format '{{ sql . | split | write }}'
```

Example 2 (unknown):
```unknown
├── extensions│   ├── hstore.sql│   └── citext.sql├── schemas│   └── public│       ├── public.sql│       ├── tables│       │   ├── profiles.sql│       │   └── users.sql│       ├── functions│       └── types└── main.sql
```

Example 3 (unknown):
```unknown
├── tables│   ├── profiles.sql│   └── users.sql├── functions├── types└── main.sql
```

Example 4 (unknown):
```unknown
data "hcl_schema" "app" {  paths = fileset("schema/**/*.hcl")}env "app" {  src = data.hcl_schema.app.url  dev = "docker://mysql/8/example"}
```

---

## ORM and Framework Guides

**URL:** https://atlasgo.io/orms

**Contents:**
- ORM and Framework Guides
  - Python​
      - SQLAlchemy
      - Django
  - Go​
      - Ent
      - GORM
      - Beego
      - sqlc
      - Bun

Atlas integrates with popular ORMs and frameworks to provide advanced schema management capabilities. Choose your ORM or framework to get started.

When should you prefer Atlas over your ORM's tool?

Python is a popular language for web development, data science, and automation. Atlas can be used to replace the built-in migration tools that ship with popular Python ORMs like SQLAlchemy and Django to accommodate more advanced schema management use-cases.

Replace Alembic with Atlas for your SQLAlchemy projects.

Enhance Django migrations with Atlas.

Go, a statically typed, compiled language, is popular for building web servers, CLIs, and microservices. Go ORMs have traditionally shipped with very basic (or no) schema management capabilities. Atlas can be used to automate both planning, verification and execution of schema changes for Go ORMs like GORM and Beego.

Schema-as-Code up and down the stack with Ent and Atlas.

Manage your GORM database schema with Atlas.

Automate schema migrations for Beego with Atlas.

Generate runtime code and migrations from a single source of truth.

Automate schema migrations for Bun with Atlas.

Over the past decade, Node.js has become a popular choice for building web servers and APIs. Support for migrations in the Node ecosystem has varied over the years, from the mostly manual migration tooling in Sequelize to the more automated capabilities in modern Prisma and Drizzle.

Atlas can be used to automate schema migrations for Node.js ORMs like Sequelize, TypeORM, and Prisma and support advanced schema management use-cases typically not supported by these tools.

Supercharge your Drizzle schema management with Atlas.

Use Atlas for advanced schema management in your Prisma projects.

Automate schema migrations for your Sequelize projects with Atlas.

Automatic migration planning and execution for your TypeORM projects.

Automate migrations for your Doctrine projects with Atlas.

Solve advanced migration use-cases for EF Core with Atlas.

Automate migration planning for your Hibernate projects with Atlas.

---

## Manage Your Database Schema as Code

**URL:** https://atlasgo.io/atlas-schema

**Contents:**
- Manage Your Database Schema as Code
- SQL Syntax​
      - Export Your Database Schema to Code
      - SQL Schema Definition
- HCL Syntax​
      - HCL Syntax
      - HCL Column Types
      - HCL Input Variables
- ORMs and External Integrations​
      - ORMs and Frameworks Portal

Atlas is built on the concept of "Database Schema-as-Code", where teams define the desired state of their database as part of their code, and use an automated tool (such as Atlas) to test, plan, verify and apply database schema changes (migrations) automatically.

Naturally, the first part of setting up your project is to determine how your "schema as code" project is going to be structured. Atlas provides a lot of flexibility around how to define the "desired state" as we describe below.

Atlas offers three main ways to define the desired state of your database schema:

Learn how to export your existing database schema to SQL code using Atlas

Learn how to define your database schema using SQL files, including Atlas importing system, masking sensitive data, and more.

Define your schema using Atlas HCL

How to define HCL column types for various databases

Use input variables in your schema for context-based definitions

Guides to help you get started with using various ORMs with Atlas

Load your desired schema from external programs or ORMs

Using and customizing the Atlas configuration file

Atlas provides commands and tools to ensure your schema definitions are valid and comply with organizational policies before applying them to your databases.

Use the atlas schema validate command to verify that a schema definition can be parsed and loaded correctly by Atlas, and that it is semantically valid, according to the database engine you're using. This fast check is designed for both developers and AI-assisted editors to confirm schema correctness after edits and before running atlas schema apply or atlas migrate diff.

If the schema is valid, the command exits successfully without output. If invalid, it prints a detailed error explaining the problem (for example, unresolved references, syntax issues, or unsupported attributes).

Beyond syntax and semantic validation, Atlas lets teams define custom schema linting rules to encode standards, naming conventions, and compliance requirements. These rules are written in HCL using the Atlas Schema Rule language, and allow teams to enforce any organizational policies around database schemas.

Example rule requiring every column to be NOT NULL or have a default value:

To get started with schema policies, see the Schema Policies Guide.

**Examples:**

Example 1 (sql):
```sql
-- atlas:import ../public.sql-- atlas:import ../tables/user_audit.sql-- create "audit_user_changes" functionCREATE FUNCTION "public"."audit_user_changes" () RETURNS trigger LANGUAGE plpgsql AS $$BEGIN    IF TG_OP = 'INSERT' THEN        INSERT INTO user_audit (user_id, operation, new_values)        VALUES (NEW.id, 'INSERT', to_jsonb(NEW));        RETURN NEW;    // ...    END IF;    RETURN NULL;END;$$;
```

Example 2 (unknown):
```unknown
schema "public" {}table "users" {  schema = schema.public  column "name" {    type = text  }  // ... more}
```

Example 3 (bash):
```bash
atlas schema validate --dev-url docker://mysql/8/dev --url file://srcatlas schema validate --env dev
```

Example 4 (swift):
```swift
predicate "column" "not_null_or_have_default" {  or {    default { ne = null }    null { eq = false }  }}rule "schema" "require-not-null-columns" {  description = "Require columns to be not null or have a default value"  table {    column {      assert {        predicate = predicate.column.not_null_or_have_default        message   = "column ${self.name} must be not null or have a default value"      }    }  }}
```

---

## Atlas Project Configuration (atlas.hcl)

**URL:** https://atlasgo.io/atlas-schema/projects

**Contents:**
- Atlas Project Configuration (atlas.hcl)
  - Config Files​
  - Flags​
  - Projects with Versioned Migrations​
  - Passing Input Values​
- Builtin Functions​
    - file​
    - fileset  ​
    - getenv​
- Project Input Variables​

Atlas config files provide a convenient way to describe and interact with multiple environments when working with Atlas. In addition, they allow you to read data from external sources, define input variables, configure linting and migration policies, and more.

By default, when running an Atlas command with the --env flag, Atlas searches for a file named atlas.hcl in the current working directory. However, by using the -c / --config flag, you can specify the path to a config file in a different location or with a different name.

Once the project configuration has been defined, you can interact with it using one of the following options:

To run the schema apply command using the local configuration defined in atlas.hcl file located in your working directory:

To run the schema apply command using the local configuration defined in atlas.hcl in arbitrary location:

Some commands accept global configuration blocks such as lint and diff policies. If no env is defined, you can instruct Atlas to explicitly use the config file using the -c (or --config) flag:

Will run the schema apply command against the database that is defined for the local environment.

It is possible to define an env block whose name is dynamically set during command execution using the --env flag. This is useful when multiple environments share the same configuration and the arguments are dynamically set during execution:

Environments may declare a migration block to configure how versioned migrations work in the specific environment:

Once defined, migrate commands can use this configuration, for example:

Will run the migrate validate command against the Dev Database defined in the local environment.

Config files may pass input values to variables defined in Atlas HCL schemas. To do this, define an hcl_schema data source, pass it the input values, and then designate it as the desired schema within the env block:

The file function reads the content of a file and returns it as a string. The file path is relative to the project directory or an absolute path.

The fileset function returns the list of files that match the given pattern. The pattern is relative to the project directory.

The getenv function returns the value of the environment variable named by the key. It returns an empty string if the variable is not set.

atlas.hcl file may also declare input variables that can be supplied to the CLI at runtime. For example:

To set the value for this variable at runtime, use the --var flag:

It is worth mentioning that when running Atlas commands within a project using the --env flag, all input values supplied at the command-line are passed only to the config file, and not propagated automatically to children schema files. This is done with the purpose of creating an explicit contract between the environment and the schema file.

Atlas configuration files support various blocks and attributes. Below are the common examples; see the Atlas Config Schema for the full list.

Config files support defining input variables that can be injected through the CLI, read more here.

The locals block allows defining a list of local variables that can be reused multiple times in the project.

The atlas block allows configuring your Atlas account. The supported attributes are:

Atlas Pro users are advised to set the org in atlas.hcl to ensure that any engineer interacting with Atlas in the project context is running in logged-in mode. This ensures Pro features are enabled and the correct migration is generated.

Data sources enable users to retrieve information stored in an external service or database. The currently supported data sources are:

Data sources are evaluated only if they are referenced by top-level blocks like locals or variables, or by the selected environment, for instance, atlas schema apply --env dev.

The sql data source allows executing SQL queries on a database and using the results in the project.

For more advanced use cases, such as fetching tenant metadata for deployment rollout strategies, the sql data source can return multiple columns per row. When a query returns multiple columns, each element in values is a map containing all columns:

The external data source allows the execution of an external program and uses its output in the project.

The data source uses Application Default Credentials by default; if you have authenticated via gcloud auth application-default login, it will use those credentials.

The data source uses Application Default Credentials by default; if you have authenticated via gcloud auth application-default login, it will use those credentials.

The data source provides two ways to work with AWS Parameter Store:

Using local AWS Profiles:

It's common case when you use the hierarchies format for you parameters in AWS Parameter Store. So the url should contain the path to the hierarchy, for example awsparamstore:///production/tenant_a/password?region=<region>&decoder=string - there are three slashes after the protocol.

The data source provides two ways to work with AWS Secrets Manager:

Using local AWS Profiles:

The HashiVault data source is available only to Atlas Pro users. To use this feature, run:

The data source uses HashiCorp Vault to securely retrieve secrets from the KV Secrets Engine (supports both v1 and v2). The data source uses the Vault address and token from the VAULT_ADDR and VAULT_TOKEN environment variables for authentication.

The output from Vault returns only the secret values as a raw JSON object (metadata is not included). Use jsondecode() to parse the response and access individual values.

The hcl_schema data source allows the loading of an Atlas HCL schema from a file or directory, with optional variables.

The external_schema data source enables the import of an SQL schema from an external program into Atlas' desired state. With this data source, users have the flexibility to represent the desired state of the database schema in any language.

By running atlas migrate diff with the given configuration, the external program will be executed and its loaded state will be compared against the current state of the migration directory. In case of a difference between the two states, a new migration file will be created with the necessary SQL statements.

The composite_schema data source allows the composition of multiple Atlas schemas into a unified schema graph. This functionality is useful when projects schemas are split across various sources such as HCL, SQL, or application ORMs. For example, each service have its own database schema, or an ORM schema is extended or relies on other database schemas.

Referring to the url returned by this data source allows reading the entire project schemas as a single unit by any of the Atlas commands, such as migrate diff, schema apply, or schema inspect.

schema - one or more blocks containing the URL to read the schema from.

The name of the schema block represents the database schema to be created in the composed graph. For example, the following schemas refer to the public and private schemas within a PostgreSQL database:

The order of the schema blocks defines the order in which Atlas will load the schemas to compose the entire database graph. This is useful in the case of dependencies between the schemas. For example, the following schemas refer to the inventory and auth schemas, where the auth schema depends on the inventory schema and therefore should be loaded after it:

Defining multiple schema blocks with the same name enables extending the same database schema from multiple sources. For example, the following configuration shows how an ORM schema, which relies on database types that cannot be defined within the ORM itself, can load them separately from another schema source that supports it:

Note, if the schema block is labeled (e.g., schema "public"), the schema will be created if it does not exist, and the computation for loading the state from the URL will be done within the scope of this schema.

If the schema block is unlabeled (e.g., schema { ... }), no schema will be created, and the computation for loading the state from the URL will be done within the scope of the database. Read more about this in Schema vs. Database Scope doc.

By running atlas migrate diff with the given configuration, Atlas loads the inventory schema from the SQLAlchemy schema, the graph schema from ent/schema, and the auth and internal schemas from HCL and SQL schemas defined in Atlas format. Then, the composite schema, which represents these four schemas combined, will be compared against the current state of the migration directory. In case of a difference between the two states, a new migration file will be created with the necessary SQL statements.

The remote_dir data source reads the state of a migration directory from Atlas Cloud. For instructions on how to connect a migration directory to Atlas Cloud, please refer to the cloud documentation.

The remote_dir data source predates the atlas:// URL scheme. The example below is equivalent to executing Atlas with --dir "atlas://myapp".

In case the cloud block was activated with a valid token, Atlas logs migration runs in your cloud account to facilitate the monitoring and troubleshooting of executed migrations. The following is a demonstration of how it appears in action:

The template_dir data source renders a migration directory from a template directory. It does this by parsing the entire directory as Go templates, executing top-level (template) files that have the .sql file extension, and generating an in-memory migration directory from them.

The blob_dir use the gocloud.dev/blob to open the bucket and read the migration directory from it. It is useful for reading migration directories from cloud storage providers such as AWS S3.

Atlas only requires the read permission to the bucket.

You can provide the profile query parameter to use a specific AWS profile from your local AWS credentials file. Or set the credentials using environment variables: AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY.

The cloud_databases lists databases from Atlas Cloud. It can be used to dynamically retrieve migration status for different environments.

This data source is helpful to implement the promotion workflow between environments. For example, as SOC 2 requires that migration files must be deployed to lower environments before being applied to production, the following configuration promotes the migration version from the dev environment to the prod environment.

See the environment promotion guide for a full implementation walkthrough.

The aws_rds_token data source generates a short-lived token for an AWS RDS database using IAM Authentication.

To use this data source:

The gcp_cloudsql_token data source generates a short-lived token for an GCP CloudSQL database using IAM Authentication.

To use this data source:

The allowCleartextPasswords and tls parameters are required for the MySQL driver to connect to CloudSQL. For PostgreSQL, use sslmode=require to connect to the database.

The http data source makes an HTTP GET/HEAD/POST request to the given URL and exports information about the response. The given URL may be either an http or https URL.

url - The URL for the request. Supported schemes are http and https.

method - The HTTP Method for the request. Allowed methods are a subset of methods defined in RFC7231 namely, GET, HEAD, and POST. POST support is only intended for read-only URLs, such as submitting a search. If omitted, the default method is GET.

request_headers - A map of request header field names and values.

request_body - The request body as a string.

request_timeout_ms - The request timeout in milliseconds.

ca_cert_pem - Certificate Authority (CA) in PEM (RFC 1421) format.

client_cert_pem - Client certificate in PEM (RFC 1421) format.

client_key_pem - Client key in PEM (RFC 1421) format.

insecure - Disables verification of the server's certificate chain and hostname. Defaults to false.

retry - Retry request configuration. By default there are no retries. Configuring this block will result in retries if an error is returned by the client (e.g., connection errors) or if a 5xx-range (except 501) status code is received.

attempts - The number of times the request is to be retried. For example, if 2 is specified, the request will be tried a maximum of 3 times.

min_delay_ms - The minimum delay between retry requests in milliseconds.

max_delay_ms - The maximum delay between retry requests in milliseconds.

url - The URL used for the request.

response_headers - A map of response header field names and values. Duplicate headers are concatenated according to RFC2616.

response_body - The response body returned as a string.

response_body_base64 - The response body encoded as base64 (standard) as defined in RFC 4648.

status_code - The HTTP response status code.

client_cert_pem and client_key_pem must be set together.

ca_cert_pem and insecure are mutually exclusive.

When configuring retries, max_delay_ms must be at least min_delay_ms.

The env block defines an environment block that can be selected by using the --env flag.

for_each - A meta-argument that accepts a map or a set of strings and is used to compute an env instance for each set or map item. See the example below.

src - The URL of or reference to for the desired schema of this environment. For example:

url - The URL of the target database.

dev - The URL of the Dev Database.

schemas - A list of strings defines the schemas that Atlas manages.

exclude - A list of strings defines glob patterns used to filter resources on inspection.

migration - A block defines the migration configuration of the env.

schema -The configuration for the desired schema.

format - A block defines the formatting configuration of the env per command (previously named log).

lint - A block defines the migration linting configuration of the env.

diff - A block defines the schema diffing policy.

rollout - A block defines the deployment rollout strategy for multi-tenant environments.

Atlas adopts the for_each meta-argument that Terraform uses for env blocks. Setting the for_each argument will compute an env block for each item in the provided value. Note that for_each accepts a map or a set of strings.

Config files may declare lint blocks to configure how migration linting runs in a specific environment or globally.

Config files may define diff blocks to configure how schema diffing runs in a specific environment or globally.

**Examples:**

Example 1 (python):
```python
// Define an environment named "local"env "local" {  // Declare where the schema definition resides.  // Also supported: ["file://multi.hcl", "file://schema.hcl"].  src = "file://project/schema.hcl"  // Define the URL of the database which is managed  // in this environment.  url = "mysql://user:pass@localhost:3306/schema"  // Define the URL of the Dev Database for this environment  // See: https://atlasgo.io/concepts/dev-database  dev = "docker://mysql/8/dev"}env "dev" {  // ... a different env}
```

Example 2 (python):
```python
// Define an environment named "local"env "local" {  // Declare where the schema definition resides.  // Also supported: ["file://multi.hcl", "file://schema.hcl"].  src = "file://project/schema.hcl"  // Define the URL of the database which is managed  // in this environment.  url = "maria://user:pass@localhost:3306/schema"  // Define the URL of the Dev Database for this environment  // See: https://atlasgo.io/concepts/dev-database  dev = "docker://maria/latest/dev"}env "dev" {  // ... a different env}
```

Example 3 (python):
```python
// Define an environment named "local"env "local" {  // Declare where the schema definition resides.  // Also supported: ["file://multi.hcl", "file://schema.hcl"].  src = "file://project/schema.hcl"  // Define the URL of the database which is managed  // in this environment.  url = "postgres://postgres:pass@localhost:5432/database?search_path=public&sslmode=disable"  // Define the URL of the Dev Database for this environment  // See: https://atlasgo.io/concepts/dev-database  dev = "docker://postgres/15/dev?search_path=public"}env "dev" {  // ... a different env}
```

Example 4 (sql):
```sql
// Define an environment named "local"env "local" {  // Declare where the schema definition resides.  // Also supported: ["file://multi.hcl", "file://schema.hcl"].  src = "file://project/schema.hcl"  // Define the URL of the database which is managed  // in this environment.  url = "sqlite://file.db?_fk=1"  // Define the URL of the Dev Database for this environment  // See: https://atlasgo.io/concepts/dev-database  dev = "sqlite://file?mode=memory&_fk=1"}env "dev" {  // ... a different env}
```

---
