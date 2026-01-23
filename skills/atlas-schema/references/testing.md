# Atlas-Schema - Testing

**Pages:** 2

---

## Schema Testing - Test Schema with Atlas

**URL:** https://atlasgo.io/testing/schema

**Contents:**
- Schema Testing - Test Schema with Atlas
  - Introduction to Schema Testing​
    - Schema Test Flags​
    - Examples​
  - The test "schema" block​
    - Example​
  - exec command​
  - catch command​
  - assert command​
  - log command​

The atlas schema test command lets you validate your database schema using familiar software testing paradigms. You can write unit tests and integration tests that seed data, run SQL assertions, and verify the behavior of functions, procedures, constraints, triggers, queries, and views. Tests can assert expected failures, perform cleanup after execution, and support parameterized or table-driven cases. You can integrate external programs like go test, pytest, or jest to extend coverage.

Designed for CI/CD workflows, atlas schema test runs changes against a dedicated test database, supports parallel execution, and works with all supported Atlas drivers, helping teams catch regressions early and ensure correctness throughout the development lifecycle.

Schema testing works only for Atlas Pro users, free and paid. Use the following command to use this feature:

Atlas schema testing is inspired by the popular databases in the way they test their public (and private) APIs. The structure is defined in HCL files (suffixed with a .test.hcl), but the underlying testing logic is written in plain SQL. The following document describes the different structure options, flags, and capabilities supported by the testing framework.

The test "schema" "<name>" block describes a test case. The second label defines the test case name, and the two arguments below are supported:

Before running a test case, Atlas creates the desired schema on the dev-database, making the environment ready for testing, and cleans the schema after the test is done, regardless of its result.

A test case is composed of zero or more commands that are executed in order, and it is aborted if any of the commands fail. The supported commands are:

The exec command expects an SQL statement to pass. If output or match is defined, the output of the SQL statement is compared to the expected value.

The catch command expects an SQL statement to fail. If error is defined, the error message is compared to the expected value.

The assert command expects an SQL statement to pass and the output to be a single row (+column) with a true value.

The log command logs a message to the test output. It can be useful to report the progress of the test case.

The external command runs an external program and expects it to pass. If output or match is defined, the output (stdout) of the program is compared to the expected value.

The cleanup command runs an SQL statement after the test case is done, regardless of its result. Note, cleanup commands are called in the reverse order they are defined.

Test files can be parameterized using variables, and their values can be set through the atlas.hcl config file. For example, given this test file:

Test config can be defined on the env block (or globally) and executed using the --env flag:

Input variables can be defined statically per environment, injected from the CLI using the --var flag, or computed from a data source.

Test blocks support the for_each meta-argument, which accepts a map or a set of values and is used to generate a test case for each item in the set or map. See the example below:

With Atlas schema testing, users can validate the correctness of their SQL queries. To test a query:

Suppose you have a schema file that defines three tables: products, users, and orders, along with a query that returns the top 3 users by total amount spent:

Let's create a test file that seeds the tables with test data and verifies the query's output. The tested SQL query can be defined inline in the test file, injected via variables, read from an external file, or executed through an external program.

Note that because the test seeds data into the database, it cannot run in parallel with other test cases. Therefore, you should not set the parallel attribute in your test case.

While Atlas schema testing provides the flexibility to integrate with external programs for certain validation tasks, its core strength lies in directly testing and asserting the behavior of database schema elements and related logic.

Here are key areas you can effectively test using Atlas's built-in commands:

**Examples:**

Example 1 (shell):
```shell
atlas login
```

Example 2 (shell):
```shell
atlas schema test --dev-url "docker://postgres/15/dev" --url "file://schema.hcl" .
```

Example 3 (shell):
```shell
atlas schema test --env local schema.test.hcl
```

Example 4 (sql):
```sql
test "schema" "postal" {  parallel = true  # The "exec" command is explained below.  exec {    sql = "select '12345'::us_postal_code"  }  # The "catch" command is explained below.  catch {    sql = "select 'hello'::us_postal_code"  }}
```

---

## Testing Migrations

**URL:** https://atlasgo.io/testing/migrate

**Contents:**
- Testing Migrations
  - Introduction​
    - Flags​
    - Examples​
  - The test "migrate" block​
    - Example​
  - migrate command​
  - exec command​
  - catch command​
  - assert command​

The atlas migrate test command allows you to write tests for your schema migrations. This feature enables you to test logic in your migrations, commonly data migrations, in a concise and straightforward way.

The command is similar to atlas schema test but is focused on testing schema migrations. If you are using the declarative migration workflow, refer to the atlas schema plan test documentation.

Migrations testing works only for Atlas Pro users, free and paid. Use the following command to use this feature:

Atlas migration testing is inspired by the popular databases in the way they test their public (and private) APIs. The structure is defined in HCL files (suffixed with a .test.hcl), but the underlying testing logic is written in plain SQL. The following document describes the different structure options, flags, and capabilities supported by the testing framework.

The test "migrate" "<name>" block describes a test case. The second label defines the test case name, and the following arguments are supported:

Every test case starts with the zero state of the migration directory, and calls to the migrate command blocks migrate it to the specified version. At the end of the execution, Atlas cleans up the dev-database and prepares it for the next test case, regardless of the test result.

A test case is composed of zero or more commands that are executed in order, and it is aborted if any of the commands fail. The supported commands are:

The migrate commands migrates the dev-database used by the test case to the desired version.

The strategy for testing a specific version is to execute migrate to the version before it, insert test data, migrate to the tested version to ensure it passes, and then run assertions to verify its correctness.

The exec command expects an SQL statement to pass. If output or match is defined, the output of the SQL statement is compared to the expected value.

The catch command expects an SQL statement to fail. If error is defined, the error message is compared to the expected value.

The assert command expects an SQL statement to pass and the output to be a single row (+column) with a true value.

The log command logs a message to the test output. It can be useful to report the progress of the test case.

The external command runs an external program and expects it to pass. If output or match is defined, the output (stdout) of the program is compared to the expected value.

The example below demonstrates how to run Go tests within an Atlas test case in order to seed the database before testing a migration:

The self object is available in the test case scope and contains the following attributes:

The cleanup command runs an SQL statement after the test case is done, regardless of its result. Note, cleanup commands are called in the reverse order they are defined.

Test files can be parameterized using variables, and their values can be set through the atlas.hcl config file. For example, given this test file:

Test config can be defined on the env block (or globally) and executed using the --env flag:

Input variables can be defined statically per environment, injected from the CLI using the --var flag, or computed from a data source.

**Examples:**

Example 1 (shell):
```shell
atlas login
```

Example 2 (shell):
```shell
atlas migrate test --dev-url "docker://postgres/15/dev" .
```

Example 3 (shell):
```shell
atlas migrate test --env local migrate.test.hcl
```

Example 4 (sql):
```sql
test "migrate" "20240613061102" {  # Migrate to version 20240613061046.  migrate {    to = "20240613061046"  }  # Insert some test data.  exec {    sql = "INSERT INTO users (name) VALUES ('Ada Lovelace')"  }  # Migrate to version 20240613061102.  migrate {    to = "20240613061102"  }  # Verify the correctness of the data migration.  exec {    sql = "SELECT first_name, last_name FROM users"    output = "Ada, Lovelace"  }}
```

---
