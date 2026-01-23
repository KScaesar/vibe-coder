# Atlas-Schema - Getting Started

**Pages:** 7

---

## 2 docs tagged with "atlas"

**URL:** https://atlasgo.io/tags/atlas

**Contents:**
- Migrating from Flyway to Atlas

Learn how to migrate your Flyway-based project to Atlas for modern schema management.

---

## Atlas HCL Documentation

**URL:** https://atlasgo.io/hcl/docs

**Contents:**
- Atlas HCL Documentation
  - Driver Schemas​
      - PostgreSQL
      - MySQL
      - MariaDB
      - SQL Server
      - ClickHouse
      - Redshift
      - Oracle
      - Spanner

API Reference for PostgreSQL HCL Schema

API Reference for MySQL HCL Schema

API Reference for MariaDB HCL Schema

API Reference for SQL Server HCL Schema

API Reference for ClickHouse HCL Schema

API Reference for Redshift HCL Schema

API Reference for Oracle HCL Schema

API Reference for Spanner HCL Schema

API Reference for SQLite HCL Schema

API Reference for Atlas Configuration HCL. Also known as: atlas.hcl

API Reference for Atlas Schema Rule HCL

API Reference for Atlas Testing HCL

API Reference for Migration Plan definition in HCL

API Reference for Atlas Functions in HCL

API Reference for Atlas Agent Configuraion HCL

---

## 18 docs tagged with "getting started"

**URL:** https://atlasgo.io/tags/getting-started

**Contents:**
- Connect to your database

In this section we perform read-only operations and make no changes to your database.

---

## Atlas vs Classic Schema Migration Tools: Flyway, Liquibase, and ORMs

**URL:** https://atlasgo.io/atlas-vs-others

**Contents:**
- Atlas vs Classic Schema Migration Tools: Flyway, Liquibase, and ORMs
- Introduction​
  - What are schema migrations?​
  - What are schema migration tools?​
  - Which schema migration tool should you use?​
  - The candidates​
    - Atlas vs Liquibase vs Flyway vs ORMs​
- The Comparison​
  - Summary (tl;dr)​
  - Schema-as-code​

Most server-side applications are backed by a database. This database usually has a schema that reflects the application's data model. Over time, the application's data model evolves and the database schema must follow suit.

Schema migrations are a common approach in our industry to automate database schema changes. Following this approach, the user creates a versioned migration script, which is the set of commands that should be executed on the database to upgrade the schema from one version to the next, thereby migrating the database to the next version.

Over the years, hundreds of tools have been created to facilitate the process of database schema migrations. Migration tools typically provide a structured way of defining migration scripts, versioning them, and a program to execute them on a target database.

Because most database schema changes are not idempotent (they cannot be re-run successfully once applied), migration tools commonly maintain a "Changelog Table" on the target database to keep track of which migrations have already been applied.

Choosing the right migration tool for your project can be daunting due to the sheer number of options available. In this document, we compare Atlas, a modern, database schema-as-code tool to more "classic" options that have been developed over the years.

We will take a high-level look at multiple candidates:

Liquibase and Flyway - are well-established projects that have been around since 2006 and 2010 respectively. Both are written in Java and require a JVM to execute. Both tools have an open-source distribution and are backed by commercial companies.

Liquibase and Flyway alike operate by letting the user define migration scripts (Flyway in plain SQL, Liquibase in XML, SQL, or Java) and execute them on behalf of the user.

ORM-based Solutions - many backend developers use application development frameworks or ORM libraries to interact with their underlying database. Virtually all of them provide some support for schema management which is crucial for supporting developers in any realistic production environment.

ORM-based migration tools vary greatly in quality and sophistication which makes it a bit difficult to treat them as a single group. In relevant categories where certain tools especially stand out, we will try to mention them specifically. ORM tend to provide native programming language based DSLs for defining migrations (such as Sequelize Migrations, with a few exceptions which use plain SQL.

ORMs tend to be community-based projects without a commercial entity backing them (with the exception of Prisma. This means that the level of support and maintenance can vary greatly between different options.

Atlas - is a database schema-as-code tool that applies modern DevOps principles to the ancient art of database schema management. Many of its users call it a "Terraform for Databases" because of its schema-first, declarative approach.

Atlas is an open-core project developed by Ariga and is available under both a commercial and an open-source license.

In case you missed it, this document is written and maintained by the team behind Atlas 😊

To assist you in deciding which database migration tool is right for you, we will compare the different possibilities along these categories:

What is the source-of-truth for your database schema?

One of the most important principles that came from the DevOps movement is the idea that to achieve effective automation, you need to be able to build everything, deterministically, from a single source of truth.

This is especially important when it comes to databases! The database schema is a critical part of our application and we better have a way to ensure it is compatible with the code we are deploying.

Let's compare the approach to defining the source of truth schema between different migration tools:

Flyway and Liquibase are "version-based", which means that to obtain the current source of truth schema, one needs to replay all migrations on an empty database and inspect the result.

ORMs and frameworks are more difficult to classify. On one hand, ORMs and frameworks revolve around a code-first definition of the different entities in the application data model. On the other hand, migrations are defined as revisions, in a version-based approach. Aside from Prisma and Django, most frameworks do not supply a mechanism to ensure that the planned migrations are consistent with the application data model as it is defined in the ORM.

Atlas provides a set of plugins called "schema loaders" for integrating with ORMs such as SQLAlchemy, GORM, Hibernate, Django, Drizzle, EF Core, Sequelize, Prisma, TypeORM, and more.

By using schema loaders, developers can keep defining the application data model using their favorite ORM and programming language while offloading database schema management to Atlas. Atlas extends ORMs by allowing you to augment your ORM schema with advanced database features such as functions, triggers, RLS policies, views, stored procedures, and other constructs using composite schemas.

Who is responsible for planning schema changes?

The next category in our comparison is migration planning. People deliberating which database migration tool to use should ask themselves, who is going to plan the schema changes? If our database is in some version N, and we want to get to version N+1, we need to calculate the plan of going from one version to the next.

Flyway and Liquibase rely on the user to plan schema changes. If a developer wishes to evolve the database schema to a new state, it is on them to look into their target database's documentation and find out the correct way to do so. Sometimes these changes are trivial, but many caveats and unpleasant surprises exist. In complex schemas, manual migration planning slows teams down. Views and other objects can be recreated out of order, dependencies break, and the process becomes fragile, introducing drift and risk.

ORMs and frameworks provide basic "auto migration" functionality that can automatically plan changes, but this is typically limited to local development on disposable databases. When it comes to planning production-grade changes, most frameworks leave planning to the user. While some tools (such as Django) have provided automatic migration planning for many years, they tend to focus on a narrow set of database capabilities, often neglecting advanced features such as functions, triggers, and stored procedures.

Atlas includes a powerful automatic migration planning engine that supports over 98% of all database features. Atlas migration flows come in two flavors:

Declarative (state-based) Migrations - Similar to Terraform, Atlas takes the desired state of the database (defined "as-code"), compares it to a live database, and suggests a migration plan. Plans can be pre-generated, reviewed, and approved during development or CI for automated application without runtime recalculation or manual intervention.

Versioned Migrations - Atlas compares the desired state of the database ("as-code") with the current state of your migration directory and produces a migration file to reconcile between the two. These migration files are then reviewed and validated in the pull-request stage by Atlas.

Both flows support "diffing (planning) policies" that provide Atlas with additional context and considerations about how to plan changes, such as "always create indexes concurrently" or "verify columns are empty before dropping".

Additionally, Atlas detects ambiguous change types such as resource renames (which can also be interpreted as drop-and-add), and prompts the user to disambiguate.

Schema migrations are a risky business. If you are not careful, you can introduce destructive changes, break a data contract with your server or a downstream consumer, lock a table for writes and cause downtime, or trigger a deployment failure due to a constraint violation.

Traditionally, the responsibility for reviewing proposed migrations was placed on humans, usually those with database expertise. As systems grow more complex, people with deep database knowledge are becoming harder to find, which exposes teams to operational risk.

The modern way to de-risk these operations is to automate quality checks during the CI phase of the software development life cycle. Let's see how the different options compare:

Flyway and Liquibase - provide a limited set of automated quality checks as part of their commercial offering.

ORMs and frameworks - generally do not provide automated migration checks. Some notable exceptions exist, such as the ankane/strong_migration Ruby Gem, which adds automated checks for Rails, and the Shadow Database mechanism in Prisma Migrate.

Atlas - provides a native feature called "Migration Linting" available both as a CLI tool and as a CI integration (for example, GitHub Actions, or GitLab Components). Migration Linting works like static code analysis: it performs a semantic analysis of changes and evaluates them through configurable policies.

Atlas ships with over 50 automated checks to detect critical migration risks. In addition, Atlas supports pre-migration checks that enforce predicates before a migration is applied. For example, you can require that a column is empty before dropping it, or that a column is not null before adding a constraint.

To help teams prevent negative outcomes, these checks can also be automatically generated by Atlas during the automatic migration planning phase. These checks are then respected by Atlas in the migration safety verification phase (for example, a migration dropping a table can be automatically approved if it contains no data).

When a project succeeds to the point that it has many developers working on it, it's common to see developers working on different features that require different changes to the database schema. This can lead to conflicts when developers try to merge their changes together.

Classic migration tools don't provide a good way to detect and handle this situation. Because each migration script is created in its own file, common conflict detection tools like git can't help you. Your source control system can't tell you if two developers are working on the same table, or if they are adding columns with the same name.

For this reason, it's common to see teams surprised in production when conflicting migrations are applied. Even worse, in some cases migrations may be applied out of order or skipped entirely, leading to an inconsistent and unknown state of the database.

Atlas supports this by enforcing a linear history and Migration Directory Integrity during local development and in CI.

Atlas provides a built-in testing framework that enables developers to write both unit and integration tests for their database logic, including functions, triggers, procedures, constraints, views, queries, and data migration scripts.

The framework provides modern software engineering principles such as testability and automation to the database layer, helping teams validate behavior and catch issues early, just like in application code. With the atlas copilot command, developers can even auto-generate tests for their database logic, making it easy to get started.

To learn more, check out the testing schemas and testing migrations documentation.

Atlas includes built-in support for managing multi-tenant database environments, commonly used in database-per-tenant architectures. With Atlas, teams can define logical tenant groups, plan and apply schema changes across many databases in a single operation. This simplifies the management of large fleets while ensuring consistency and reducing the risk of drift or deployment errors.

To learn more, check out the Database-per-Tenant guide.

Even with strict CI/CD, production databases sometimes drift from their desired state. To handle this, Atlas continuously compares your live schema against the schema declared in your repository. The moment they diverge, Atlas sends an alert-complete with an ERD, HCL, and SQL diff-so you can remediate issues before they become incidents. Full details are available in the drift-detection guide.

Atlas can emit webhooks whenever a schema change or drift event is detected, letting your team receive rich, structured messages on Slack, Workplace, or any HTTP endpoint. Set-up takes a few clicks in Atlas Cloud and helps engineering, SRE, and security teams stay on top of every change without polling the database. To learn more, check out the webhooks guide.

Certain migrations, especially rollbacks (called "down" migrations"), may warrant a second pair of eyes. Atlas offers built-in, auditable approval flows that can pause execution until a designated reviewer signs off on the change. This lets teams automate confidently by retaining human control where it matters most. This capability extends across the ecosystem–you can use it from the CLI or through the Kubernetes Operator, Terraform Provider, or GitHub Actions suite. See the dedicated docs for down migration approvals and examples for GitHub Actions and Kubernetes.

After planning and verifying the safety of migrations are considered, engineers comparing different migration tools should evaluate the provided deployment strategies.

As you can see, virtually all tools provide a CLI tool that can be used to deploy migrations, making it possible to integrate schema management into CI/CD pipelines.

However, modern deployment solutions often provide a modular plugin system that allows tool creators to develop simple integrations to streamline the deployment process.

For instance, organizations that manage their source code on GitHub often use GitHub Actions to automate their workflows. Tools that provide a native GitHub Actions integration make it easier for these organizations to integrate schema management into their CI/CD pipelines. As of writing this document, Atlas and Liquibase are the only tools that provide a comprehensive GitHub Actions integration.

Similarly, organizations that deploy to Kubernetes benefit from using Operators to extend the Kubernetes API with custom resources. By providing a Kubernetes Operator, a schema management makes it straightforward to include schemas as native Kubernetes resources. Atlas is the only tool that provides a Kubernetes Operator for schema management.

Finally, organizations that manage their infrastructure using Terraform rely on Terraform Providers to manage all of their resources. By providing a Terraform Provider, a schema management tool enables organizations to include schema management in their infrastructure-as-code workflows. Atlas is the only tool under comparison here that provides a Terraform Provider.

Naturally, when comparing migration tools, support for various database engines is a differentiating factor.

While all tools under comparison in this document support popular open-source RDBMSs such as PostgreSQL, MySQL and SQLite, support for other databases varies.

The following table summarizes the support matrix for different databases between the different tools:

We created Atlas to provide a modern, schema-as-code approach to database schema management. Atlas by no means is the best solution in every case and for every team but we hope this document has provided you with some insight into how Atlas compares to other tools and where it may be a good fit for your project.

If you are interested in learning more about Atlas, we recommend you check out the Quickstart Guide and continue exploring the documentation.

If you have any questions or want to learn more about Atlas, you are welcome to join the Atlas Discord server to engage with the community, or book a demo session with a member of the Atlas team.

---

## Quick Introduction

**URL:** https://atlasgo.io/getting-started

**Contents:**
- Quick Introduction
  - Installation​
  - MacOS
  - Linux
  - Windows
  - Start a local database container​
  - Inspecting our database​
  - Declarative Migrations​
  - Versioned Migrations​
  - Next Step: Setup CI/CD​

Atlas is a language-independent tool for managing and migrating database schemas using modern DevOps principles. It offers two workflows:

Declarative: Similar to Terraform, Atlas compares the current state of the database to the desired state, as defined in an HCL, SQL, or ORM schema. Based on this comparison, it generates and executes a migration plan to transition the database to its desired state.

Versioned: Unlike other tools, Atlas automatically plans schema migrations for you. Users can describe their desired database schema in HCL, SQL, or their chosen ORM, and by utilizing Atlas, they can plan, lint, and apply the necessary migrations to the database.

To download and install the latest release of the Atlas CLI, simply run the following in your terminal:

Get the latest release with Homebrew:

To pull the Atlas image and run it as a Docker container:

If the container needs access to the host network or a local directory, use the --net=host flag and mount the desired directory:

Download the latest release and move the atlas binary to a file location on your system PATH.

Use the setup-atlas action to install Atlas in your GitHub Actions workflow:

For other CI/CD platforms, use the installation script. See the CI/CD integrations for more details.

If you want to manually install the Atlas CLI, pick one of the below builds suitable for your system.

The default binaries distributed in official releases are released under the Atlas EULA. If you would like obtain a copy of Atlas Community Edition (under an Apache 2 license) follow the instructions here.

For the purpose of this guide, we will start a local Docker container running MySQL.

For this example, we will start with a schema that represents a users table, in which each user has an ID and a name:

To create the table above on our local database, we can run the following command:

The atlas schema inspect command supports reading the database description provided by a URL and outputting it in three different formats: Atlas DDL (default), SQL, and JSON. In this guide, we will demonstrate the flow using both the Atlas DDL and SQL formats, as the JSON format is often used for processing the output using jq.

To inspect our locally-running MySQL instance, use the -u flag and write the output to a file named schema.hcl:

Open the schema.hcl file to view the Atlas schema that describes our database.

This block represents a table resource with id, and name columns. The schema field references the example schema that is defined elsewhere in this document. In addition, the primary_key sub-block defines the id column as the primary key for the table. Atlas strives to mimic the syntax of the database that the user is working against. In this case, the type for the id column is int, and varchar(100) for the name column.

To inspect our locally-running MySQL instance, use the -u flag and write the output to a file named schema.sql:

Open the schema.sql file to view the inspected SQL schema that describes our database.

Now, consider we want to add a blog_posts table and have our schema represent a simplified blogging system.

Let's add the following to our inspected schema, and use Atlas to plan and apply the changes to our database.

Edit the schema.hcl file and add the following table block:

In addition to the elements we saw in the users table, here we can find a foreign key block, declaring that the author_id column references the id column on the users table.

Edit the schema.sql file and add the following CREATE TABLE statement:

Now, let's apply these changes by running a migration. In Atlas, migrations can be applied in two types of workflows: declarative and versioned.

The declarative approach requires the user to define the desired end schema, and Atlas provides a safe way to alter the database to get there. Let's see this in action.

Continuing the example, in order to apply the changes to our database we will run the apply command:

Atlas presents the plan it created by displaying the SQL statements. For example, for a MySQL database we will see the following:

Apply the changes, and that's it! You have successfully run a declarative migration.

To ensure that the changes have been made to the schema, you can run the inspect command again. This time, we use the --web/-w flag to open the Atlas Web UI and view the schema.

If you are using an old version of Atlas, you may need to replace the --web flag with --visualize.

Alternatively, the versioned migration workflow, sometimes called "change-based migrations", allows each change to the database schema to be checked-in to source control and reviewed during code-review. Users can still benefit from Atlas intelligently planning migrations for them, however they are not automatically applied.

To start, we will calculate the difference between the desired and current state of the database by running the atlas migrate diff command.

To run this command, we need to provide the necessary parameters:

Run ls migrations, and you will notice that Atlas has created two files:

In addition to the migration directory, Atlas maintains a file name atlas.sum which is used to ensure the integrity of the migration directory and force developers to deal with situations where migration order or contents was modified after the fact.

Now that we have our migration files ready, you can use the migrate apply command to apply the changes to the database. To learn more about this process, check out the Versioned Migrations Quickstart Guide

After getting familiar with the basics of Atlas, the next step is to integrate it into your development workflow. Sign up for a free trial to unlock Pro features, then set up your CI/CD pipeline by running the following command, and proceeding with the steps below:

In this short tutorial we learned how to use Atlas to inspect databases, as well as use declarative and versioned migrations. Read more about the use-cases for the two approaches here to help you decide which workflow works best for you.

We have a super friendly #getting-started channel on our community chat on Discord.

For web-based, free, and fun (GIFs included) support:

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

## Welcome to the Atlas Documentation

**URL:** https://atlasgo.io/docs

**Contents:**
- Welcome to the Atlas Documentation
  - Installation​
  - MacOS
  - Linux
  - Windows
  - Schema-as-Code​
      - SQL
      - Atlas HCL
      - ORM
  - Generating Migration​

Atlas is a language-independent tool for managing and migrating database schemas using modern DevOps principles. It offers two workflows:

Declarative: Similar to Terraform, Atlas compares the current state of the database to the desired state, as defined in an HCL, SQL, or ORM schema. Based on this comparison, it generates and executes a migration plan to transition the database to its desired state.

Versioned: Unlike other tools, Atlas automatically plans schema migrations for you. Users can describe their desired database schema in HCL, SQL, or their chosen ORM, and by utilizing Atlas, they can plan, lint, and apply the necessary migrations to the database.

Get started with Atlas in under 5 minutes.

To download and install the latest release of the Atlas CLI, simply run the following in your terminal:

Get the latest release with Homebrew:

To pull the Atlas image and run it as a Docker container:

If the container needs access to the host network or a local directory, use the --net=host flag and mount the desired directory:

Download the latest release and move the atlas binary to a file location on your system PATH.

Use the setup-atlas action to install Atlas in your GitHub Actions workflow:

For other CI/CD platforms, use the installation script. See the CI/CD integrations for more details.

If you want to manually install the Atlas CLI, pick one of the below builds suitable for your system.

The default binaries distributed in official releases are released under the Atlas EULA. If you would like obtain a copy of Atlas Community Edition (under an Apache 2 license) follow the instructions here.

Describe your database schema with native SQL.

The HCL-based language allows developers to describe database schemas in a declarative manner.

Represent your database with your ORM.

Set up a Terraform-like workflow where each migration is calculated as the diff between your desired state and the current state of the database.

Set up a migration directory for your project, creating a version-controlled source of truth of your database schema.

Verify your migration files in your CLI.

Setup automatic migration linting with GitHub Actions.

Setup automatic migration linting with GitLab CI.

Deploy migrations from your CLI.

Setup deployments with GitHub Actions.

Setup deployments with GitLab CI.

Use Atlas with Terraform to manage database schema changes.

Use the Atlas Kubernetes Operator to manage database schema changes.

Test your database schema using familiar software testing paradigms.

Write tests for schema migrations.

Push your database schema to the Cloud to maintain a single source of truth for database schemas with auto-generated documentation.

Simulate and analyze changes to catch destructive changes, backward-incompatibility issues, accidental table locks, and constraint violations way before they reach production.

Gain full visibility into the database schema in your production environments with detailed logs and troubleshooting capabilities.

Learn about Atlas's modern approach to Database CI/CD

Automatic migration planning for SQLAlchemy applications

Working with sensitive info like database passwords

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

## Atlas Cloud: Getting Started with Database Schema Management

**URL:** https://atlasgo.io/cloud/getting-started

**Contents:**
- Atlas Cloud: Getting Started with Database Schema Management
  - Introduction to Atlas Cloud​
  - Atlas Pro: Unlock the Full Power of Atlas​
  - Why Choose Atlas Cloud?​
  - Getting Started with Atlas Cloud​
  - Key Features of Atlas Cloud​
      - Schema Documentation
      - Automatic Pull Request Review
      - Simplify your Pipelines
      - Troubleshooting and Visibility

Atlas Cloud is an online platform for managing your organization's Atlas Pro licenses. It also provides a set of features and products that complement Atlas CLI to allow teams to build robust, end-to-end schema management workflows.

For individuals and teams that want to unlock the full potential of Atlas, the Pro plan provides access to advanced CLI features, access to non-open-source database drivers, and schema management for Pro schema objects, such as views, triggers, extensions, stored procedures, and functions. For a full list of the CLI features that require login access, click here.

User Roles in Atlas Pro:

In an Atlas Pro organization, each member is assigned a role that defines their level of access:

Atlas Cloud provides a centralized platform for your team to collaborate on database schema changes. Here are some of the key benefits:

To start using Atlas Cloud, you first need to log in. If you don't have an account, you can sign up for free.

To start with Atlas Pro, sign up via the UI or CLI:

Once you've logged in, you can start using Pro features in the CLI. Note, new organizations get a 30-day free trial. After that, a license is required to continue using Atlas Pro. To learn more see the pricing page.

Enjoy always up-to-date automatically generated docs and ERD for your schema. Atlas Cloud manages a single source of truth for the database schema in a format that is easy to understand and navigate.

Atlas automatically simulates and reviews your migrations during the CI process to ensure that your migrations are safe to deploy.

De-clutter deployment pipelines by pushing migrations to Atlas Cloud. Atlas seamlessly integrates with modern deployment tools like Kubernetes and Terraform to make it easy to deploy your migrations to production as part of your existing CD process.

Quickly resolve failed migrations with detailed deployment logs. Atlas Cloud provides a unified view for your database schemas and their migrations across all of your environments.

Automatically monitor schema drifts and ensure your database schemas are always in sync with their desired state.

Notify the right people when schema changes are proposed and deployed via Slack and other integrations.

And additional features such as pre-migrations checks, schema monitoring, and more.

Q: What is Atlas Cloud?

A: Atlas Cloud is a platform that takes database schema management to the next level by providing a single source of truth for your database schemas and migrations, along with advanced collaboration, monitoring, deployment, schema change audit logging, and built-in guardrails for safe migrations. It is tightly integrated with the Atlas CLI and helps streamline collaboration, automate CI/CD processes, and monitor databases across all environments.

Q: Is Atlas Cloud free?

A: Atlas Cloud is a commercial product. However, we offer a free Hacker License for non-commercial use. In addition, all new organizations receive a 30-day free trial of the Pro plan to explore all its features. After the trial, a paid license is required to continue using Atlas Pro.

Q: How does Atlas Cloud help with database migrations?

A: Atlas Cloud can automatically review your database migrations in pull requests to check for dangerous changes, ensuring that your migrations are safe to deploy. It also provides a central place to manage and deploy your migrations to different environments.

Q: Can I use Atlas Cloud with my existing database?

A: Yes, Atlas supports a wide range of databases, including PostgreSQL, MySQL, MariaDB, SQLite, SQL Server, ClickHouse, Oracle, Redshift, and more. You can connect Atlas Cloud to your existing database to start managing its schema. For a complete list of supported databases, see the documentation.

Yes, head over to our live demo account to see Atlas Cloud in action.

**Examples:**

Example 1 (shell):
```shell
atlas login
```

---
