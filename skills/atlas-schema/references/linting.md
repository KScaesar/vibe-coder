# Atlas-Schema - Linting

**Pages:** 1

---

## Migration Analyzers

**URL:** https://atlasgo.io/lint/analyzers

**Contents:**
- Migration Analyzers
- Analyzers​
  - Non-Linear Changes​
    - Relax Non-Linear Errors on Edits​
  - Destructive Changes​
    - Enforce Destructive Change Checks Atlas Pro​
    - Allowlist Drop Rules Atlas Pro​
  - Data-dependent Changes​
  - Backward Incompatible Changes​
  - Naming Conventions Policy​

The database is often the most critical component in software architectures. Being a stateful component, it cannot be easily rebuilt, scaled-out or fixed by a restart. Outages that involve damage to data or simply unavailability of the database are notoriously hard to manage and recover from, often taking long hours of careful work by a team's most senior engineers.

As most outages happen directly as a result of a change to a system, Atlas provides users with means to verify the safety of planned changes before they happen. The sqlcheck package provides interfaces for analyzing the contents of SQL files to generate insights on the safety of many kinds of changes to database schemas. With this package developers may define an Analyzer that can be used to diagnose the impact of SQL statements on the target database.

Using these interfaces, Atlas provides different Analyzer implementations that are useful for determining the safety of migration scripts.

Below are the Analyzer implementations currently supported by Atlas.

Non-additive changes, often referred to as non-linear changes, are changes to the migration directory that are not added in a sequential order. This is a bit like the linear history in version control systems, where migration files are commits and the migration directory is the repository. Let's explain with three examples why ensuring the linearity of the migration directory is important:

Luckily, Atlas detects non-linear and non-additive changes made to a migration directory. To enable this behavior in your project, integrate Atlas into your GitHub Actions or GitLab CI pipelines, and Atlas will automatically detect and report non-linear changes during the CI run.

By default, non-linear changes are reported but not cause migration linting to fail. Users can change this by configuring the non_linear changes detector in the atlas.hcl file:

Users who configured the non_linear change detector to fail migration linting (error = true) can relax or ignore these errors when editing existing migration files by setting the on_edit option to WARN or IGNORE.

This is useful when developers need to update the latest migration files right after they land on the main branch and want to keep CI pipelines unblocked while non-linear checks still apply to older files.

Destructive changes are changes to a database schema that result in loss of data. For instance, consider a statement such as:

This statement is considered destructive because whatever data is stored in the email_address column will be deleted from disk, with no way to recover it. There are definitely situations where this type of change is desired, but they are relatively rare. Using the destructive (GoDoc) Analyzer, teams can detect this type of change and design workflows that prevent it from happening accidentally.

Running migration linting locally on in CI fails with exit code 1 in case destructive changes are detected. However, users can disable this by configuring the destructive analyzer in the atlas.hcl file:

In some teams, destructive changes are considered high-risk and should never be skipped, regardless of whether a developer adds an -- atlas:nolint directive. In these cases, the force option can be set on the destructive analyzer. This guarantees the check always runs and reports diagnostics, even if explicitly excluded.

The destructive analyzer can be configured to allow specific destructive changes, such as dropping a table or column whose name matches a defined pattern. This allows teams following a deprecation workflow, like renaming objects with a drop_ prefix before deletion, to continue using the analyzer while avoiding false positives from intentional drops.

Data-dependent changes are changes to a database schema that may succeed or fail, depending on the data that is stored in the database. For instance, consider a statement such as:

This statement is considered data-dependent because if the orders table contains duplicate values on the name column we will not be able to add a uniqueness constraint. Consider we added two records with the name atlas to the table:

Attempting to add a uniqueness constraint on the name column, will fail:

This type of change is tricky because a developer trying to simulate it locally might succeed in performing it only to be surprised that their migration script fails in production, breaking a deployment sequence or causing other unexpected behavior. Using the data_depend (GoDoc) Analyzer, teams can detect this risk early and account for it in pre-deployment checks to a database.

By default, data-dependent changes are reported but not cause migration linting to fail. Users can change this by configuring the data_depend analyzer in the atlas.hcl file:

Backward-incompatible changes, also known as breaking changes, are schema changes that have the potential to break the contract with applications that rely on the old schema. For instance, renaming a column from email_address to email can cause errors during deployment (migration) phase if applications running the previous version of the schema reference the old column name in their queries.

By default, detected breaking changes are reported but do not cause migration linting to fail. Users can change this by configuring the incompatible analyzer in the atlas.hcl file:

In database schema design, maintaining consistency and readability through naming conventions is a widely common practice. Atlas provides an analyzer that can help enforce naming conventions on a variety of schema resources, including tables, columns, and indexes.

Users can enable this by configuring the naming analyzer in their atlas.hcl file:

By default, detected naming violations are reported but do not cause migration linting to fail. Users can change this by configuring the naming analyzer in the atlas.hcl file:

Schema changes like CREATE INDEX or DROP INDEX can cause the database to lock the table against write operations. Luckily, PostgreSQL provides the CONCURRENTLY option that may be more resource-intensive, but allows normal database operations to continue while the index is built or dropped.

Atlas provides an analyzer that identifies non-concurrent index creation or deletion for tables not created within the same file, and recommends executing them concurrently.

Additionally, since indexes cannot be created or deleted concurrently within a transaction, Atlas ensures the atlas:txmode none directive exists in the file header to prevent this file from running in a transaction. This check can be disabled along with the other ones as follows:

By default, detected concurrent index violations are reported but do not cause migration linting to fail. Users can change this by configuring the concurrent_index analyzer in the atlas.hcl file:

By default, Atlas wraps each migration file in its own transaction (see transaction configuration for more details). If a file includes a statement that starts a transaction (for example, BEGIN or START TRANSACTION), the database will return an error (or fail later when using a connection-pooler like PgBouncer) such as cannot start a transaction within a transaction (SQLite) or pq: unexpected transaction status idle (PostgreSQL).

The nestedtx analyzer flags such statements. You can fix them by either removing the manual transaction control or adding -- atlas:txmode none to the file header to indicate that this migration file should not be wrapped in a transaction by Atlas. When Atlas detects this issue, it automatically adds a code suggestion with this directive to the pull request.

By default, violations are reported as warnings. You can make them fail the lint step by configuring the analyzer in your atlas.hcl file:

The statement analyzer lets you define regular expression rules to permit or reject specific SQL statements in your migration files. It processes each statement sequentially against an ordered list of rules. The supported rule types are allow and deny:

The statement analyzer reports violations as warnings by default. You can make them fail the linting step by setting error = true in the statement block.

To ensure the analyzer cannot be skipped with the -- atlas:nolint directive, set force = true.

The SQL Injection analyzer examines SQL statements in migration files and declarative schemas to detect constructs that could allow untrusted input to be executed as part of an SQL command. It identifies unsafe dynamic SQL patterns, such as string concatenation or variable interpolation, that may bypass proper escaping or identifier quoting.

As more schema code and migrations are edited automatically, including by AI-assisted tools, developers may introduce such patterns unintentionally. This analyzer provides a deterministic way to surface these risks early in the development process, helping teams maintain secure, reviewable, and policy-compliant database changes.

This analyzer performs static analysis on parsed statements and reports potential vulnerabilities based on the following checks:

Static analysis cannot always determine whether a value is derived from a trusted source at runtime. As a result, the analyzer takes a conservative approach and may report false positives, particularly in complex and well-audited dynamic SQL code.

The checks below are built into Atlas; for additional guardrails, see Atlas custom schema linting rules or ask

Destructive change that is reported when a database schema was dropped. For example:

A destructive change is reported when a table is dropped, posing a risk of data loss. For example:

The suggested solution is to back up the data before dropping the table, or add a pre-migration check to ensure that the table is empty before dropping it:

A destructive change is reported when a non-virtual column is dropped, posing a risk of data loss. For example:

The suggest solution to resolve these errors is to add a pre-migration check that ensures the column is empty before dropping it:

Adding a unique index to a table might fail in case one of the indexed columns contain duplicate entries. For example:

Modifying a non-unique index to be unique might fail in case one of the indexed columns contain duplicate entries.

Since index modification is done with DROP and CREATE, this check will be reported only when analyzing changes programmatically or when working with the declarative workflow.

Adding a non-nullable column to a table might fail in case the table is not empty. For example:

Modifying nullable column to non-nullable might fail in case it contains NULL values. For example:

The solution, in this case, is to backfill NULL values with a default value:

Renaming a table is a backward-incompatible change that can cause errors during deployment (migration) if applications running the previous version of the schema refer to the old name in their statements. For example:

Unlike other checks, there is no single correct way to resolve this one. Here are some possible solutions:

It's likely that this change was introduced when you renamed one of the entities in your ORM, and the linter helped you catch the potential problem this could cause. In such cases, most ORM frameworks allow you to rename the entity while still pointing to its previous table name. e.g., here is how you can do it in Ent and in GORM.

If renaming is desired but the previous version of the application uses the old table name, a temporary VIEW can be created to mimic the previous schema version in the deployment phase. However, the downside of this solution is that mutations using the old table name might fail (e.g., if the VIEW is not Updatable/Insertable). Yet, if Atlas detects a consecutive statement with a CREATE VIEW <old_name>, it will ignore this check.

Renaming a column is a backward-incompatible change that can cause errors during deployment (migration) if applications running the previous version of the schema refer to the old column name in their statements. For example:

Unlike other checks, there is no single correct way to resolve this one. Here are some possible solutions:

It's likely that this change was introduced when you renamed a field in one of the entities in your ORM, and the linter helped you catch the potential problem this could cause. In such cases, most ORM frameworks allow you to rename a field while still pointing to its previous column name. e.g., in Ent you can configure it using the StorageKey option, and in GORM you can set it by adding the column struct tag.

If renaming is desired but the previous version of the application uses the old column name, a temporary VIRTUAL generated column can be created to mimic the previous schema version in the deployment phase. However, the downside of this solution is that mutations using the old column name will fail. Yet, if Atlas detects a consecutive command with such a column, it will ignore this check.

Constraint deletion is reported when a foreign-key constraint was dropped. For example:

Constraint deletion is reported when a check constraint was dropped. For example:

Constraint deletion is reported when a primary-key constraint was dropped. For example:

Adding a non-nullable column to a table without a DEFAULT value implicitly sets existing rows with the column zero (default) value. For example:

Adding a column with an inline REFERENCES clause has no actual effect. Users should define a separate FOREIGN KEY specification instead. For example:

Removing enum values from a column changes the column type and requires a table copy. During this process, the table is locked for write operations. In addition, operation may fail if the column contains values that are not in the new enum definition.

Reordering enum values of a colum requires a table copy. During this process, the table is locked for write operations.

Note that since the order of the enum values defines how the table is sorted when using ORDER BY on the column, controlling the ordering behavior can be achieved using the DESC clause or expressions as follows:

Inserting new enum values not at the end requires table copy. During this process, the table is locked for write operations.

If possible, it is recommended to add new enum values at the end of the enum definition.

Exceeding 256 enum values changes storage size and requires a table copy. During this process, the table is locked for write operations.

Removing set values from a column requires a table copy. During this process, the table is locked for write operations. In addition, operation may fail if the column contains values that are not in the new set definition.

Reordering set values of a colum requires a table copy. During this process, the table is locked for write operations.

Inserting new set values not at the end requires table copy. During this process, the table is locked for write operations.

If possible, it is recommended to add new set values at the end of the set definition.

Adding set values to a column changes its storage size and requires a table copy, if the new amount changes the number of bytes needed for the bitmap. The storage size of a set column is 1, 2, 3, 4 or 8 bytes, depending on the number of values: One byte can store up to 8 values, two bytes can store up to 16 etc.

During this process, the table is locked for write operations.

Modifying a nullable column to non-nullable without setting a DEFAULT might fail in case it contains NULL values. The solution is one of the following:

1. Set a DEFAULT value on the modified column:

2. Backfill NULL values with a default value:

This check is reported when a migration file contains multiple statements that cannot safely run within a single transaction. If execution stops midway, the database may end up in an intermediate state between the previous and target versions.

You can resolve this check by splitting non-transactional statements into separate migration versions (files), or by adding the -- atlas:txmode none directive at the top to tell Atlas not to wrap the file in a transaction.

This check fires when a migration file opens its own transaction even though Atlas already wraps the file. For example:

To avoid nested transactions:

A schema has been given a name that violates the naming convention.

A table has been given a name that violates the naming convention.

A column has been given a name that violates the naming convention.

An index has been given a name that violates the naming convention.

A foreign-key constraint has been given a name that violates the naming convention.

A check constraint has been given a name that violates the naming convention.

Possible SQL injection vulnerabilities have been detected in the provided SQL. These issues may allow user-controlled input to be executed as part of an SQL statement, potentially leading to unauthorized data access, data modification, or execution of unintended operations.

Creating a table with optimal data alignment may help minimize the amount of required disk space. For example consider the next Postgres table on a 64-bit system:

Each tuple in the table takes 24 bytes of successive memory without the header. the id attribute takes 8 bytes, the premium takes 1 byte and 3 bytes of padding, the balance takes 4 bytes and the age takes 2 bytes, and lastly 6 bytes of padding allocated for the end of the row. In total 9 bytes of padding are allocated for each row.

Compared to same table with different ordering which only takes 16 bytes in memory with 1 byte of padding:

Creating an index non-concurrently acquires a SHARE lock on the table blocking writes but allowing reads during the operation.

Dropping an index non-concurrently acquires an ACCESS EXCLUSIVE lock on the table blocking both reads and writes during the operation.

Indexes cannot be created or deleted concurrently within a transaction. Add the atlas:txmode none directive to the header to prevent this file from running in a transaction.

Adding a PRIMARY KEY constraint (with its index) acquires an ACCESS EXCLUSIVE lock on the table, blocking all access during the operation. The solution is to add as follows:

Validate the index creation and ensure it is in VALID state. Otherwise, the constraint creation will fail with the following error:

Note, this step can be automated using a pre-migration check on the migration file below.

After validating the index state, add the PRIMARY KEY constraint using the created index:

Adding a UNIQUE constraint (with its index) acquires an ACCESS EXCLUSIVE lock on the table, blocking all access during the operation. The solution is to add as follows:

Note, this step can be automated using a pre-migration check on the migration file below.

A change to the column type that requires adjusting the actual stored data and triggers a rewrite of the table and potentially indexes. During this operation, an ACCESS EXCLUSIVE lock is acquired on the table, preventing any level of access, including SELECT.

Adding a column with a volatile DEFAULT value requires a rewrite of the table. During this operation, an ACCESS EXCLUSIVE lock is acquired on the table, preventing any level of access, including SELECT.

Modifying a column from NULL to NOT NULL requires a full table scan. During this operation, an ACCESS EXCLUSIVE lock is acquired on the table, preventing any level of access, including SELECT.

If the table has a CHECK constraint that ensures NULL cannot exist, such as CHECK (c > 10 AND c IS NOT NULL), the table scan is skipped, and therefore this check is not reported.

Adding a PRIMARY KEY on a nullable columns implicitly sets them to NOT NULL, resulting a full table scan unless there is a CHECK constraint that ensures NULL cannot exist.

Adding a CHECK constraint without the NOT VALID clause requires scanning the table to verify that all rows satisfy the constraint. During this operation, an ACCESS EXCLUSIVE lock is acquired on the table, preventing any level of access, including SELECT.

Adding a FOREIGN KEY constraint without the NOT VALID clause requires a full table scan to verify that all rows satisfy the constraint. During this process, a SHARE ROW EXCLUSIVE lock is acquired on both tables blocking write operations.

To avoid this, the constraint can be added with NOT VALID, which skips the initial table scan and prevents long-running locks. The existing rows can then be validated separately using VALIDATE CONSTRAINT, which only acquires a SHARE UPDATE EXCLUSIVE lock on the modified table and a ROW SHARE lock on the referenced table, minimizing disruptions.

If validation fails, the constraint stays in the NOT VALID state, blocking new violations while allowing time to fix existing data. If the migration runs within a transaction, the constraint will be dropped at the end of the transaction.

Changing a table's logging mode between LOGGED and UNLOGGED requires a full table rewrite. During this operation, an ACCESS EXCLUSIVE lock is acquired on the table, preventing any level of access, including SELECT.

In PostgreSQL, LOGGED tables (the default) write data to the Write-Ahead Log (WAL), providing durability and crash recovery. UNLOGGED tables skip WAL writes for better performance but lose data on a crash or unclean shutdown.

Both operations trigger a complete table rewrite, which can be time-consuming for large tables and will block all access during the process.

Atlas Pro users can customize the behavior of individual checks using the check block. Two options are available: error and skip. Setting a check to error will cause migration linting to fail if the check is violated, while the skip option ignores the check and does not report it.

To set an environment-specific policy, embed the lint block inside an env block:

**Examples:**

Example 1 (unknown):
```unknown
lint {  non_linear {    error = true  }}
```

Example 2 (unknown):
```unknown
lint {  non_linear {    error   = true    on_edit = WARN // IGNORE | ERROR  }}
```

Example 3 (sql):
```sql
ALTER TABLE `users` DROP COLUMN `email_address`;
```

Example 4 (unknown):
```unknown
lint {  destructive {    error = false  }}
```

---
