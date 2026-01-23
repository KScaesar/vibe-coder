# Atlas-Schema - Declarative Workflow

**Pages:** 4

---

## Setup CI/CD for Declarative Migrations

**URL:** https://atlasgo.io/declarative/setup-cicd

**Contents:**
- Setup CI/CD for Declarative Migrations
- Choose Your Workflow​
      - Declarative (State-based) Migrations (Used in this guide)
      - Versioned Migrations
- Prerequisites​
  - Installing Atlas​
  - MacOS
  - Linux
  - Windows
  - Atlas Pro for CI/CD​

Continuous integration and continuous deployment (CI/CD) became a standard requirement in modern engineering. When applied to database schemas, CI/CD ensures that changes are validated, tested, reviewed, and shipped safely across environments.

This doc introduces how to set up a CI/CD pipeline for declarative (state-based) database schema migrations with Atlas. It covers automated planning, validation and pre-approval workflows, ad-hoc approval policies, and deployment of schema changes so the final migrations are correct, predictable, and safe to apply for production.

For a deeper understanding of the principles behind this workflow, see our Modern Database CI/CD blueprint.

Atlas supports two types of schema management workflows: declarative (state-based) migrations, and versioned migrations. This guide focuses on setting up CI/CD for declarative migrations.

Define the desired state of your database, and Atlas automatically calculates the migration plan. Schema changes are planned, reviewed, and approved before deployment.

Changes are defined as explicit migration files (SQL scripts) that are applied in sequence. Each migration is tracked, version-controlled, and reviewable in pull requests.

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

The Schema Registry allows you to store, version, and maintain a single source of truth for your database schemas and migration plans. If you prefer not to use the Schema Registry, you can use an alternative storage solution accessible from your CI/CD pipeline.

If you haven't set up a declarative migrations project yet, define your desired schema before configuring CI/CD. Choose one of the following options:

Define your desired schema using HCL, SQL, or through an ORM. Atlas will automatically plan and apply migrations to bring your database to the desired state.

Import an existing database to code, then use it as your desired state. Atlas will manage schema changes going forward using declarative migrations.

Atlas provides native integrations for all popular CI/CD platforms, with support for code comments, code suggestions, PR and run summaries, PR status updates, and more. Choose your CI platform to get started:

Set up CI/CD pipelines using GitHub Actions with Atlas. Supports schema management with declarative migrations.

Integrate Atlas with GitLab CI/CD pipelines using GitLab CI components. Full support for versioned and declarative workflows.

Automate database migrations with CircleCI Orbs. Complete CI/CD integration for declarative workflows.

Set up CI/CD using Bitbucket Pipes. Full support for declarative migrations and schema management.

Use Azure DevOps Pipelines with Atlas. Supports GitHub and Azure Repos repositories with declarative migrations.

CI validates and plans schema changes before merging to the main branch, ensuring they are safe, correct, and ready for production. The workflow follows this pattern:

Atlas generates migration plans by comparing your desired schema state (defined in HCL, SQL, or ORM) against the current database state. The atlas schema plan command creates a migration plan that shows exactly what SQL statements will be executed to bring the database to the desired state.

Atlas automatically posts plan results as comments on your pull/merge requests, providing immediate feedback to developers. For example:

The schema-plan functionality is available to all CI platforms:

To learn more about schema planning, see the Pre-planning Schema Migrations guide.

Pre-approval workflows ensure that all schema changes are reviewed and approved before being applied to production. This workflow combines schema planning during development with automatic approval on merge:

This creates a seamless workflow where schema changes are reviewed during development and automatically approved when merged, ensuring only reviewed changes can be deployed.

While pre-approval workflows catch most schema changes during development, some scenarios require additional safety checks:

Ad-hoc approval acts as a final checkpoint. When atlas schema apply runs, it performs an additional check to detect any differences between the desired schema and the actual database state. If differences are found and no pre-approved plan exists, Atlas can pause and require manual approval before applying changes.

You can configure ad-hoc approval behavior using the lint.review policy. The policy can be set to one of the following values:

Configure the policy in your atlas.hcl file:

When ad-hoc approval is required, Atlas pauses the deployment and provides a link to review and approve the migration plan. Here's how it looks in different platforms:

When approval is required, Atlas provides a link to the migration plan in the Atlas Registry. Clicking the link opens the plan in the registry UI where you can review the proposed changes and approve or reject them:

Ad-hoc approval is available on:

When a pull request is merged into the main branch, Atlas lets you push your schema definition to the Atlas Schema Registry. This creates an immutable, versioned artifact (like pushing a Docker image to a container registry) that becomes the single source of truth for your schema.

The registry stores the exact schema state that passed review and planning, ensuring only approved schemas can be deployed. Once in the registry, schemas can be deployed to any environment without needing access to your source code repository, using URLs like atlas://myapp?tag=latest.

Schema created with atlas schema push

The schema-push functionality is available on most CI platforms:

Once your schema is validated and pushed to the registry, you can deploy it to your environments. Choose the deployment method based on your infrastructure needs:

Deploy schemas directly from your CI/CD pipeline. Simple and straightforward deployment for any environment.

Native Kubernetes resource management using the Atlas Operator. Deploy schemas as Kubernetes resources with declarative workflows.

Infrastructure as Code deployment using the Atlas Terraform Provider. Manage schemas alongside your infrastructure.

GitOps deployment for Kubernetes using ArgoCD. Deploy schemas declaratively with full GitOps workflow.

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

## Declarative Schema Migrations

**URL:** https://atlasgo.io/declarative/apply

**Contents:**
- Declarative Schema Migrations
      - Declarative vs. Versioned Workflows
- Overview​
- Flags​
- Approval Policy​
- Review Policy​
- Diff Policy​
- Transaction Configuration​
- Pre & Post Deployment Scripts​
- Examples​

With Atlas's declarative schema migrations (sometimes called state-based migrations), users don't need to manually craft SQL migration scripts. Instead, Atlas automatically plans and applies schema changes, safely transitioning the database from its current state to the desired state.

The desired schema state can be defined using an HCL or SQL schema definition, a database URL, external schemas like ORM, or a combination of these.

Read more about declarative workflows

By default, the atlas schema apply command manages only schemas, tables, and their associated indexes and constraints such as foreign keys and checks.

Views, materialized views, functions, procedures, triggers, sequences, domains, extensions, and additional database features are available to Atlas Pro users. To include these resources in schema migrations, use the following command:

When running schema apply, users may supply multiple parameters:

See detailed usage examples in the Examples section.

The schema apply command requires user review and approval before executing the migration against the target database.

Approving the migration can occur manually either locally or in CI, or automatically with the linting review policy. It can also be completely skipped, which is not recommended in production environments.

Let's cover all the options:

Manual Review (default): The atlas schema apply command will print the SQL statements it is going to run and prompt the user for approval. Users can review the migration plan and either approve or reject it.

Atlas Pro users can set the --dev-url flag to run an analysis and simulation of the proposed changes on the dev database and get a detailed linting report when reviewing the migration.

Using Review Policy: Atlas ships with an analysis engine that can detect the impact of proposed changes to the target database. For example, Atlas can detect irreversible destructive changes that can result in data loss or data-dependent changes that may fail due to data integrity constraints.

Users can configure Atlas to automatically approve migrations that pass the analysis engine checks (for example, no destructive changes were detected) and require manual review for migrations that fail the checks. Read more on how to configure the Review Policy for your project below.

Skip Review: The --auto-approve flag can be used to skip the review process and automatically apply the migration to the target database. Although this option is convenient for experimentation and development, it is not recommended for production environments, as it may lead to unexpected changes.

Atlas Pro users can define the cases in which their schema changes require manual review and approval. How does this work?

The review policy can be set to one of the following values:

The typical workflow for applying schema changes without manual review is to run atlas schema plan to pre-plan the migration and use the review policy as a fall-back for schema transitions that were not pre-planned but are still safe to apply.

The atlas schema plan command can be integrated into the CI/CD pipeline to ensure that all schema changes are reviewed and approved before being applied to the database.

Atlas allows configuring the schema diffing policy in project configuration to fine-tune or modify suggested changes before applying them to the database:

To instruct Atlas to skip destructive statements, specifically DROP SCHEMA or DROP TABLE in this example, via a CLI variable, define a variable in the project configuration and set its value dynamically when running the migrate diff command:

The usage is as follows:

To instruct Atlas to create and drop indexes concurrently, set the concurrent_index option in the diff block of the environment configuration.

Note that such migrations are tagged with atlas:txmode none to ensure they do not run within a transaction.

To instruct Atlas to create materialized views without populating them (using the WITH NO DATA clause), set the with_no_data option in the materialized block of the diff configuration:

To control this behavior via a CLI variable:

Run the command with the variable:

Atlas Pro users can control how Atlas generates CREATE and DROP table statements by configuring the add_table and drop_table blocks in the diff configuration, respectively:

Similar to the migrate apply command, the schema apply command allows configuring the transaction mode for declarative migrations using the --tx-mode flag. The following options are available:

To run custom scripts before or after a migration (for example, taking snapshots, seeding lookup tables, or cleaning up after deployment), refer to the pre/post deployment hooks documentation.

The following example demonstrates how to use Atlas DDL (HCL) as the desired state:

The following example demonstrates how to use an SQL schema file as the desired state:

The following example demonstrates how to use Sequelize models as the desired state:

To see this in action, check out our Declarative Migrations for Sequelize.js video.

For more ORM examples, go to our ORM guides.

The following example demonstrates how to use the migration directory as the desired state.

The URL for the migration directory can also contain two optional query parameters:

For example, "file://migrations?format=golang-migrate&version=20250909104354“

The Atlas configuration language provides built-in support for executing declarative workflows in multi-tenant environments. Using the for_each meta-argument, users can define a single env block that is expanded to N instances – one for each tenant:

Read more about defining declarative workflows using project files in multi-tenant environments.

When applying schema changes to multiple tenants, you can use Atlas's deployment block to define staged rollout strategies with fine-grained control over execution order, parallelism, and error handling:

This configuration first applies schema changes to canary tenants, then to all free-tier tenants in parallel (up to 10 at a time), and finally to paid tenants (up to 3 at a time).

Read more about deployment rollout strategies for multi-tenant environments.

A common deployment pattern involves the same schema replicated across multiple database servers (e.g., a regional deployment with identical databases in US, EU, and APAC). This section explains how the plan/approve/apply workflow operates in this scenario.

When atlas schema apply runs against a database, Atlas checks whether there is a pre-planned migration stored in the Atlas Registry that matches the schema transition:

Plans are matched by schema state transition, not by database URL. If all your databases are in the same state (S1), a single approved plan (S1 → S2) works for all of them.

Assuming your CI/CD pipeline is already configured with schema/plan and schema/plan/approve actions, your typical workflow creates and approves plans during the PR/merge process. However, databases may occasionally diverge due to manual changes, partial failures, or different timing of previous migrations.

When a database is in a different state than expected and no matching pre-approved plan exists, Atlas computes the migration, runs analysis (linting), and handles it based on your Review Policy:

When auto-approval doesn't pass, Atlas can use ad-hoc approvals: it automatically creates a plan, provides you a link to review it in Atlas Registry, and waits for your approval before continuing. This ensures no unexpected changes are applied without explicit review.

For more information on setting up ad-hoc approvals in your CI/CD pipeline:

Set up ad-hoc approvals in GitHub Actions workflows

Set up ad-hoc approvals with the Atlas Kubernetes Operator

CLI Command Reference

**Examples:**

Example 1 (shell):
```shell
atlas login
```

Example 2 (unknown):
```unknown
lint {  review = ERROR // ERROR | WARNING | ALWAYS  destructive {    error = false  }}
```

Example 3 (unknown):
```unknown
env "prod" {  lint {    review = ERROR // ERROR | WARNING | ALWAYS    destructive {      error = false    }  }}
```

Example 4 (unknown):
```unknown
variable "destructive" {  type    = bool  default = false}env "local" {  diff {    skip {      drop_schema = !var.destructive      drop_table  = !var.destructive    }  }}
```

---

## Pre-planning Schema Migrations

**URL:** https://atlasgo.io/declarative/plan

**Contents:**
- Pre-planning Schema Migrations
- Overview​
  - How does it work?​
- Local Example​
  - Setup​
  - Changing the Schema​
  - Data-Dependent Changes​
- Atlas Registry​
  - Edit a Plan​
    - Example​

When using the declarative workflow, users have the option to save migration plans to be reviewed and approved before applying them to the database.

Note: If you are not familiar with the atlas schema apply command, please refer to the Applying Schema Changes guide first.

The atlas schema plan command is available exclusively to Pro users. To use this feature, run:

Declarative schema changes can be approved in one of the following ways:

These options depend on the database state and cannot predict whether the migration will succeed, fail, or abort. This is where atlas schema plan becomes useful.

The atlas schema plan command allows users to pre-plan, review, and approve migrations before executing atlas schema apply on the database. This enables users to preview and modify SQL changes, involve team members in the review process, and ensure that no human intervention is required during the atlas schema apply phase.

In short (more details below), atlas schema plan generates a migration plan for the specified Schema Transition (State1 -> State2) and stores it in the Atlas Registry.

During atlas schema apply, Atlas checks if there is an approved migration plan for this specific schema transition and applies it without recalculating SQL changes at runtime or requiring user approval.

Let's consider a simple example. We have a table users with two columns id and name, and we want to add a new column email to the table.

First, you should have your schema-as-code definition of our current schema state (schema.sql in this example) and an atlas.hcl configuration file containing the name of the Atlas Registry schema repository we will be using (app).

Run atlas schema push to create the schema in Atlas Registry:

Then, run atlas schema apply to align the database with the schema state:

At this stage, we want to add a non-nullable email column to the users table. Let's update the schema.sql file and then run atlas schema plan to generate a migration plan.

We run atlas schema plan to generate a migration plan for adding the email column to the users table:

The output looks like this:

Atlas detects data-dependent changes in the migration plan and provides a diagnostic message. In this case, it warns that adding the non-nullable email column, will fail if the users table is not empty. The recommended solution is to provide a default value for the new column.

We'll "Abort" this plan and fix it by adding a default value to the email column:

Now, we run atlas schema plan again to generate a new migration plan and approve it:

Once approved, the migration plan will be pushed to the Atlas Registry and can be applied using atlas schema apply.

At this stage, we can run atlas schema apply to apply the changes to the database on any environment without re-calculating the SQL changes at runtime or requiring human intervention.

Atlas Registry allows you to store, version, and maintain a single source of truth for your database schemas and its migration plans. It is similar to Docker Hub, but for your schemas and migrations.

In addition to functioning as storage, it is schema-aware and provides extra capabilities such as ER diagrams, SQL diffing, schema docs, and more.

Schema pushed with atlas schema push

One of the first questions that come to mind when comparing the declarative approach to the versioned approach is: Can I edit a migration plan?

There are three ways to edit a migration plan:

Save, edit, and push:

Pull, edit, and push:

Let's edit the migration plan from the example above by changing all email columns with 'unknown' value to a computed email value:

Note that the from and to are fingerprints of the schema states. They are used to identify the states in the schema transition. We will ignore them for now (without changing them, of course) and focus on the migration attribute.

Once approved, the migration plan will be pushed to the Atlas Registry.

Note that if your manual changes are not in sync with the desired state (i.e., do not bring the database to the desired state), Atlas will detect the schema drift and reject this migration plan.

Running atlas schema apply will apply the changes to the database, including the new UPDATE statement.

By default, atlas schema plan pushes plans in an APPROVED state to the Atlas Registry. However, in some cases, we may prefer to create the plan in a PENDING state and approve it later after it passes the team's review.

There are two ways to create a plan in a PENDING state and approve it after review:

Users can protect their registry schemas by limiting who can push changes, push approved plans, or approve existing plans. To enable this for your schema, go to the schema repository settings in the Atlas Registry and enable the Protected Flows option.

To pull a plan from the Atlas Registry, use the atlas schema plan pull command:

To lint a plan (remote or local) before pushing it to the Atlas Registry, use the atlas schema plan lint command:

Running atlas schema apply searches for a migration plan in the Atlas Registry and applies it to the database, if it exists. However, in unusual cases, you may have multiple (approved) migration plans for the same schema transition (e.g., one per environment).

In that case, running atlas schema apply will abort with the following error:

In this case, we either delete the conflicting plans from the Atlas Registry or provide the plan URL explicitly using the --plan flag:

To list all plans in the Atlas Registry for the given schema transition, use the atlas schema plan list command:

Atlas provides an official GitHub Actions integration to automatically plan, review, and approve declarative schema migrations within PR workflows.

Plan Generated by atlas schema plan

Let's see how this works by going through an example:

Let's create a schema repository named demo in Atlas Registry with the following SQL schema:

To create the schema repository in the Atlas Registry, run the following command:

To keep our schema repository up-to-date with the latest changes, we can set up the schema/push GitHub Action. This automatically pushes the schema to the Atlas Registry whenever changes are made to schema.sql:

To push the schema to Atlas Registry from your GitHub Action, set up a GitHub secret named ATLAS_TOKEN using your Atlas Cloud token. To create a token, follow these instructions.

The last step is to update our workflow file with the schema/plan and schema/plan/approve Actions:

To avoid a race condition between the push and plan workflows, we can merge them into a single workflow.

In addition to the local edit flow, you can comment Atlas directives directly on the PR to control the generated migration. These directives, similar to GitHub Slash Commands, are parsed by the schema/plan action and translated into Atlas migration directives.

Migration linting flags destructive changes as errors unless configured otherwise. However, you can use the /atlas:nolint destructive directive in the PR description to append this directive to the plan and ignore linting diagnostics for destructive changes.

The schema apply command executes migration plans within a transaction unless set to none using the --txmode flag. Some migrations, however, cannot be run in a transaction. In such cases, you can use the /atlas:txmode none directive in the PR description to set the transaction mode to none, and Atlas will respect this during the schema apply stage.

Adding directives in the PR

CLI Command Reference

**Examples:**

Example 1 (unknown):
```unknown
atlas login
```

Example 2 (sql):
```sql
CREATE TABLE users (  id INTEGER PRIMARY KEY AUTOINCREMENT,  name TEXT);
```

Example 3 (unknown):
```unknown
env "local" {  # URL to the target database  url = "sqlite://main.db"  # URL to the dev-database  dev = "sqlite://dev?mode=memory"  schema {    # Desired schema state    src = "file://schema.sql"    # Atlas Registry config    repo {      name = "app"    }  }}
```

Example 4 (bash):
```bash
> atlas schema push --env localSchema: app  -- Atlas URL: atlas://app  -- Cloud URL: https://a8m.atlasgo.cloud/schemas/141733920781
```

---

## Database Schema Diff - Comparing Schemas

**URL:** https://atlasgo.io/declarative/diff

**Contents:**
- Database Schema Diff - Comparing Schemas
- Flags​
- Diff Policy​
- Examples​
  - Compare databases​
  - Compare database schemas​
  - Compare HCL schemas​
  - Compare SQL schemas​
  - Compare migration directories​
  - Compare SQL to HCL​

It is sometimes useful to be able to calculate the diff between two schemas. For instance, as you are developing you may want to calculate how to move from an existing database to some other state that you are interested in. Alternatively, you may be diagnosing some issue and want to verify there is no difference between a local copy of a schema and a remote one.

To accommodate these types of use-cases, Atlas offers the schema diff that accepts two schema states: --from and --to, calculates the differences between them, and generates a plan of SQL statements that can be used to migrate the "from" schema to the state defined by the "to" schema. A state can be specified using a database URL, an HCL or SQL schema, or a migration directory.

By default, running atlas schema diff diffs only schemas, tables, and their associated indexes and constraints such as foreign keys and checks.

Views, materialized views, functions, procedures, triggers, sequences, domains, extensions, and additional features are available to Atlas Pro users. To include these resources in the schema diffing, use the following command:

Atlas allows configuring the schema diffing policy in project configuration to fine-tune or modify suggested changes before they are printed:

To instruct Atlas to create and drop indexes concurrently, set the concurrent_index option in the diff block of the environment configuration. Note that such migrations are tagged with atlas:txmode none to ensure they do not run within a transaction.

The usage is as follows:

To instruct Atlas to create materialized views without populating them (using the WITH NO DATA clause), set the with_no_data option in the materialized block of the diff configuration:

To control this behavior via a CLI variable, define a variable in the project configuration and set its value dynamically when running the migrate diff command:

Run the command with the variable:

Compare two MySQL schemas/databases named example:

Compare two MariaDB schemas/databases named example:

Compare two PostgreSQL schemas named public under the example database:

Compare two SQL Server schemas:

Compare two ClickHouse schemas/named-databases:

Compare two Redshift clusters with a schema named public under the example database:

If the DDL statements only include qualified tables (e.g., schema.table), you can omit the database name from the --dev-url:

If the DDL statements only include qualified tables (e.g., schema.table), you can omit the database name from the --dev-url:

If the DDL statements only include qualified tables (e.g., schema.table), you can omit the database name from the --dev-url:

If the DDL statements only include qualified tables (e.g., schema.table), you can omit the database name from the --dev-url:

The schema diff command can also be used to compare external schemas defined in data sources, such as ORM schemas, with a database, HCL or SQL schemas, or even with other ORM schemas.

For example, the code below uses atlas schema diff to load the ORM schemas from GORM and Sequelize and detect schema drift between their SQL representations:

Starting in v0.35, the schema diff command uses two-space indentation for generated SQL by default. You can change or remove the indentation using the --format flag. For example:

CLI Command Reference

**Examples:**

Example 1 (shell):
```shell
atlas login
```

Example 2 (unknown):
```unknown
env "local" {  diff {    // By default, indexes are not created or dropped concurrently.    concurrent_index {      create = true      drop   = true    }  }}
```

Example 3 (unknown):
```unknown
variable "destructive" {  type    = bool  default = false}env "local" {  diff {    skip {      drop_schema = !var.destructive      drop_table  = !var.destructive    }  }}
```

Example 4 (go):
```go
atlas schema diff --env "local" --var "destructive=true"
```

---
