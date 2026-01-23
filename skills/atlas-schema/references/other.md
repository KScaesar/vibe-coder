# Atlas-Schema - Other

**Pages:** 9

---

## Atlas Guides

**URL:** https://atlasgo.io/guides

**Contents:**
- Atlas Guides
- Deploying to Kubernetes​
      - GitOps with Argo CD
      - GitOps with Flux CD
      - GitOps with Atlas Cloud
- Deploying Schema Migrations​
      - Introduction
      - Modern Database CI/CD
      - Atlas Registry
      - Container Images

Practical guides for using Atlas in your workflow. Learn how to deploy schema changes, integrate Atlas with your tools, and work with databases, ORMs, CI/CD platforms, testing, and compliance.

Guides for using Atlas with PostgreSQL, MySQL, ClickHouse, SQL Server, and more

Use your ORM of choice to define your desired schema

Learn how to use Atlas with Cursor, Claude Code and GitHub Copilot

Deploy database migrations to Kubernetes clusters using GitOps principles with Argo CD, Flux CD, or directly from Atlas Cloud's Schema Registry.

Deploying to Kubernetes with the Atlas Operator and Argo CD

Deploying to Kubernetes with the Atlas Operator and Flux CD

Deploying to Kubernetes from Atlas Schema Registry

Comprehensive guides for deploying schema migrations across various platforms and environments, including cloud providers, container platforms, and integration with secrets management.

Getting started with deploying schema migrations

Complete guide to setting up CI/CD workflows for database schema changes with Atlas

Using Atlas Registry to deploy, read, and view migrations

Creating container images for migrations

Deploying to AWS with ECS/Fargate

Deploying to Kubernetes with the Atlas Operator and Fly.io

Deploying schema migrations to Google CloudSQL using Atlas

Using Atlas to implement IAM Authentication and Secret Stores

Using SSL Certs with the Atlas Operator

Connecting to your database from GitHub Actions

Integrate Atlas with your preferred CI/CD platform to automate database migrations as part of your deployment pipeline.

Setting up CI/CD for databases on GitHub Actions

Setting up CI/CD for databases on GitLab

Setting up CI/CD with Azure DevOps and GitHub

Setting up CI/CD with Azure DevOps and Azure Repos

Learn how to use Atlas with AI coding assistants like Cursor, Claude Code, and GitHub Copilot to generate and manage database migrations more effectively.

Using Atlas with AI agents for database migration management

Configure GitHub Copilot with Atlas-specific instructions

Set up Cursor with Atlas-specific rules

Set up Claude Code with Atlas-specific instructions

Ensure your database migrations meet compliance requirements and follow security best practices with Atlas's approval workflows and audit capabilities.

Enforcing reviewed and approved schema migrations for compliance

Managing environment promotion workflows for database changes

Manage database schemas in multi-tenant architectures where each tenant has their own database. Learn how to define target groups, deploy migrations across multiple databases, and use the Atlas Cloud Control Plane for centralized management.

Utilizing Atlas to manage database schemas in Database-per-Tenant architectures

Defining target groups

Deploying migrations to Database-per-Tenant architecture

Staged deployments with canary patterns, parallelism, and error handling

Using the Atlas Cloud Control Plane to manage migrations across multiple databases

Compare Atlas with other migration tools and learn how to migrate from existing tools to Atlas.

Comparing Atlas with Flyway and migrating from Flyway

Comparing Atlas with Liquibase

Using Atlas schema inspect as an alternative to Flyway's snapshot command

Using Atlas Migrate Down as an alternative to Flyway's undo scripts

Step-by-step guide to migrate your Flyway-based project to Atlas

Working with golang-migrate and Atlas

Importing existing migrations from goose

Comprehensive testing guides for ensuring your database migrations work correctly across different scenarios and database objects.

Creating Atlas integration tests with docker-compose

Creating Atlas integration tests with GitHub Actions

Testing data migrations with Atlas

Testing views with Atlas

Testing functions with Atlas

Testing domains with Atlas

Testing stored procedures with Atlas

Testing triggers with Atlas

Additional resources for specific use cases and advanced features, including Docker deployment, Terraform integration, template directories, and programmatic inspection.

Learn how to run Atlas in Docker containers

Managing named databases with Terraform and Atlas

Using template directories for dynamic migration generation

Using Go templates for programmatic inspection output

---

## Database Guides

**URL:** https://atlasgo.io/databases

**Contents:**
- Database Guides
  - PostgreSQL​
      - Getting Started with PostgreSQL
      - Serial Type Columns
      - Partial Indexes
      - Included Columns
      - Index Operator Classes
      - Optimal Data Alignment (PG110)
      - Descending Indexes
      - Functional Indexes

All common open-source relational database management systems are supported in all versions of Atlas. Additionally, the Pro Plan includes support for ClickHouse, SQL Server, Redshift, and Aurora DSQL. Atlas Pro support for Oracle, Spanner, Snowflake and Databricks is currently in beta. Choose your database to get started.

For more details on the specific features supported by our RDBMS drivers, take a look at our docs.

Learn how to set up and use Atlas with your PostgreSQL database

Understanding serial type columns in PostgreSQL with Atlas

Implementing partial indexes in PostgreSQL with Atlas

Working with covering indexes in PostgreSQL

Understanding index operator classes in PostgreSQL

Achieving optimal data alignment in PostgreSQL with Atlas

Implementing descending indexes in PostgreSQL with Atlas

Creating functional indexes in PostgreSQL with Atlas

Creating and managing unlogged tables in PostgreSQL with Atlas

Represent your PostgreSQL schema using HCL

Learn how to set up and use Atlas with your MySQL database

Working with descending indexes in MySQL with Atlas

Working with functional indexes in MySQL with Atlas

Working with prefix indexes in MySQL with Atlas

Working with CHECK constraints in MySQL with Atlas

Working with generated columns in MySQL with Atlas

Managing MySQL schemas on RDS with Terraform

Detecting inline REFERENCES clauses for MySQL

Detecting dropping non-virtual columns for MySQL databases with Atlas's linting capabilities

Detecting dropping foreign keys in MySQL databases, using Atlas's linting capabilities

Represent your MySQL schema using HCL

Implementing partial indexes in SQLite with Atlas

Creating descending indexes in SQLite with Atlas

Creating functional indexes in SQLite with Atlas

Working with Turso in SQLite with Atlas

Represent your SQLite schema using HCL

Learn how to set up and use Atlas with your ClickHouse database

How Atlas manages schema changes in ClickHouse cluster mode

Managing ClickHouse Cloud databases using Atlas

Managing ClickHouse settings with Atlas

Represent your ClickHouse schema using HCL

Learn how to set up and use Atlas with your SQL Server database

Represent your SQL Server schema using HCL

Learn how to set up and use Atlas with your Redshift database

Represent your Redshift schema using HCL

Learn how to set up and use Atlas with AWS Aurora DSQL

Learn how to set up and use Atlas with your Oracle database

Learn how to set up and use Atlas with your Spanner database

Learn how to set up and use Atlas with your Snowflake database

Learn how to set up and use Atlas with your Databricks database

---

## One doc tagged with "documentation"

**URL:** https://atlasgo.io/tags/documentation

**Contents:**
- Welcome to the Atlas Documentation

The official Atlas documentation. Learn how to manage and migrate your database schemas with modern DevOps principles using declarative and versioned workflows.

---

## Contributing

**URL:** https://atlasgo.io/contributing

**Contents:**
- Contributing
  - How to Contribute​
  - Contributing code to Atlas​
    - Code-generation​
    - Linting​
    - Formatting​
    - Unit-tests​
    - Integration tests​

Atlas is a community project, we welcome contributions of all kinds and sizes!

Here are some ways in which you can help:

As we are still starting out, we don't have an official code-style or guidelines on composing your code. As general advice, read through the area of the code that you are modifying and try to keep your code similar to what others have written in the same place.

Some of the code in the Atlas repository is generated. The CI process verifies that all generated files are checked-in by running go generate ./... and then running git status --porcelain. Therefore, before committing changes to Atlas, please run:

Your code will be linted using golangci-lint during CI. To install in locally, follow this guide.

Format your code using the standard fmt command:

Your code should be covered in unit-tests, see the codebase for examples. To run tests:

Some features, especially those that interact directly with a database must be verified in an integration test. There is extensive infrastructure for integration tests under internal/integration/ that runs tests under a matrix of database dialect (Postres, MySQL, etc.) and versions. To run the integration tests, first use the docker-compose.yml file to spin up databases to test against:

Then run the tests, from with the integration directory:

**Examples:**

Example 1 (shell):
```shell
go generate ./...
```

Example 2 (shell):
```shell
golangci-lint run
```

Example 3 (shell):
```shell
go fmt ./...
```

Example 4 (shell):
```shell
go test ./...
```

---

## 

**URL:** https://atlasgo.io/blog

**Contents:**
- Announcing Atlas v1.0: A Milestone in Database Schema Management

We're excited to announce Atlas v1.0 - just in time for the holidays! 🎄

v1.0 is a milestone release. Atlas has been production-ready for a few years now, running at some of the top companies in the industry, and reaching 1.0 is our commitment to long-term stability and compatibility. It reflects what Atlas has become: a schema management product built for real production use that both platform engineers and developers love.

Here's what's in this release:

---

## 

**URL:** https://atlasgo.io/faq

**Contents:**
- Installing Atlas on Windows and Setting up PATH
  - Question​

How do I install Atlas on Windows and set up the PATH environment variable so I can run atlas from any directory?

---

## Trust Center

**URL:** https://atlasgo.io/trust

**Contents:**
- Trust Center
- SOC 2 Type II (Since 2022)​
  - Our commitment to process only metadata​
- Legal documents​
      - Terms of use
      - Privacy Policy
      - Data Privacy and the CLI
      - Atlas End-user License Agreement (EULA)
      - Atlas SaaS agreement

Ariga, the company behind Atlas, continuously evaluates the security and compliance needs of our customers and is continuously expanding the program as additional reports are requested. If your compliance team needs access to our report or other documents, drop us a line!

System and Organization Controls (SOC) 2 is a report focusing on security, availability, confidentiality, processing integrity and privacy criteria contained in the Trust Services Criteria (TSC) as applied to an organization's systems and is designed to provide assurance about these controls to relying parties (our customers). Ariga works with independent external auditors to undergo an audit at least once per year addressing security, availability, confidentiality and processing integrity of Ariga

As a schema management tool, Atlas interacts with critical and sensitive data assets of our customers. This naturally raises concerns for compliance and security teams, as they are entrusted with protecting data on behalf of their own customers.

As part of our SOC 2 audit, we introduced Control #70 which states: "The company does not process or store records from the customer's managed databases, but only handles information schema and metadata related to them."

By incorporating this control, we have established a clear, auditable process that reinforces our promise to our customers and ensures that this principle remains at the core of how we operate moving forward.

Ariga respects the privacy of users of its websites and our social media pages and is committed to protect the personal information that our users share with us. We believe that you have a right to know our practices regarding the information we may collect and use when you visit and/or use our Sites and Social Media. Please read the following carefully to understand our views and practices regarding your personal information and how we will treat it.

Legal terms and conditions for using Ariga's services and products

How Ariga collects, uses, and protects user data and privacy

How data privacy is maintained when using the Atlas Command Line Interface (CLI)

This agreement governs the usage of non-community binaries we distribute

Terms and conditions for using the Atlas SaaS product

If your compliance team, needs access to our report or other documents, drop us a line!

---

## Atlas Integrations

**URL:** https://atlasgo.io/integrations

**Contents:**
- Atlas Integrations
  - Platform Integrations​
      - Kubernetes Operator
      - Terraform Provider
  - CI/CD Platforms​
      - GitHub Actions
      - GitLab CI Components
      - CircleCI Orbs
      - Bitbucket Pipes
      - Azure DevOps

Atlas integrates with the tools you already use, whether you want to manage your schema with Terraform, deploy migrations in Kubernetes, or run checks in your CI pipeline.

Deploy and manage your database migrations in Kubernetes.

Manage your database schema as code with Terraform.

Run Atlas in your GitHub workflows to validate schemas, deploy migrations, and catch issues before they hit production.

Use Atlas in your GitLab pipelines with ready-to-use CI components for schema management.

Validate and deploy your schema in CircleCI with our official orbs.

Use Atlas pipes for Bitbucket Pipelines to manage your schema changes with confidence.

Run Atlas tasks on Azure Pipelines to keep your schema changes in sync with your application deployments.

Build Atlas into your Go applications. Programmatically manage schemas and migrations with our SDK.

---

## Getting Support

**URL:** https://atlasgo.io/support

**Contents:**
- Getting Support
- Community Support​
- Commercial Support​

We invest a lot of time and resources in this documentation to make Atlas as easy to use as possible. However, sometimes you may encounter some issues that you could use some help with. We are here to help you!

Atlas is a community project, and we have a community of users and developers that are happy to help you out. You can reach out to the community in the following ways:

At Ariga, the company building Atlas, we constantly monitor both channels and will try to help you out as soon as possible. However, we are a small team and we can't guarantee a response time. If you need a guaranteed response time, consider commercial support.

Commercial support by the team that builds Atlas is available to all paying users of Atlas Cloud and as a separate subscription for self-hosted users.

Commercial support includes:

If you are interested in commercial support, please write us at hello@ariga.io or reach out to us via Intercom (click the conversation bubble on the lower right part of the screen).

---
