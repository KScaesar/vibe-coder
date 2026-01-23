# Atlas-Schema - Guides

**Pages:** 70

---

## Building a Docker Image for Schema Migrations in CI Pipelines

**URL:** https://atlasgo.io/guides/deploying/image

**Contents:**
- Building a Docker Image for Schema Migrations in CI Pipelines
- Defining the Dockerfile​
- Verify our image​
- Defining the GitHub Actions Workflow​

To integrate schema migrations into pipelines that deploy to container management systems (such as Kubernetes, AWS ECS, Google Cloud Run, etc.) it is recommended to create a dedicated container image per version that contains the migration tool (such as Atlas) and the relevant migration files.

In this guide we will demonstrate how to build a dedicated Docker image that includes Atlas and the relevant migrations files. We will demonstrate how to build this image as a GitHub Actions Workflow, but the same result can be achieved in any CI system.

Suppose our project structure looks something like:

Our goal is to build an image that contains:

To do this we can build our container image with the official Atlas Docker image as the base layer.

To do this, our Dockerfile should be placed in the directory containing the migrations directory and will look something like this:

To test our new Dockerfile run:

Docker will build our image:

To verify Atlas can find your migrations directory and that its integrity is intact run:

If no issues are found, no errors will be printed out.

Next, we define a GitHub Actions workflow that will build our container image and push it to the GitHub container repo (ghcr.io) on every push to our mainline branch:

Save this file in your GitHub repository under the .github/workflows directory. After you push it to your mainline branch, you will see a run of the new workflow in the Actions tab of the repository.

**Examples:**

Example 1 (unknown):
```unknown
.├── main.go└── migrations    ├── 20221031125934_init.sql    ├── 20221031125940_add_users_table.sql    ├── 20221031125948_add_products_table.sql    └── atlas.sum
```

Example 2 (sql):
```sql
FROM arigaio/atlas:latestCOPY migrations /migrations
```

Example 3 (unknown):
```unknown
docker build -t my-image .
```

Example 4 (sql):
```sql
=> [internal] load build definition from Dockerfile                                          0.0s => => transferring dockerfile: 36B                                                           0.0s => [internal] load .dockerignore                                                             0.0s => => transferring context: 2B                                                               0.0s => [internal] load metadata for docker.io/arigaio/atlas:latest                               0.0s => [internal] load build context                                                             0.0s => => transferring context: 252B                                                             0.0s => [1/2] FROM docker.io/arigaio/atlas:latest                                                 0.0s => CACHED [2/2] COPY migrations /migrations                                                  0.0s => exporting to image                                                                        0.0s => => exporting layers                                                                       0.0s => => writing image sha256:c928104de31fc4c99d114d40ea849ade917beae3df7ffe9326113b289939878e  0.0s => => naming to docker.io/library/my-image                                                   0.0s
```

---

## Connecting to your database from GitHub Actions

**URL:** https://atlasgo.io/guides/deploying/connect-to-db-from-github-actions

**Contents:**
- Connecting to your database from GitHub Actions
  - 1. Publicly Accessible Database​
  - 2. Allow-listed IP Addresses​
  - 3. Self-hosted Runners​
  - Conclusion​

When using Atlas with GitHub Actions, there are scenarios where you may want Atlas to directly interact with your database. To enable this, your database must be accessible from the GitHub Actions runners. Depending on your environment and security preferences, there are several methods to facilitate this connection.

If your database is publicly accessible, you can use its public IP address or hostname to establish a connection. This approach requires minimal setup and allows Atlas to interact with the database over the internet.

This method used to be considered a security misstep due to the inherent risks of exposing databases to the public internet. However, with the proliferation of cloud-native databases and security best practices, this approach is now considered acceptable in many scenarios and is the default offering for many cloud database services such as Neon Postgres and Clickhouse Cloud.

If you choose this method, ensure proper access controls, such as strong passwords or IAM authenticatoin and SSL/TLS encryption, are in place.

For databases that are not publicly accessible, you can allow-list the IP addresses of GitHub Actions runners. GitHub provides a meta API endpoint that lists the CIDR ranges used by its runners. You can fetch this data with the following command:

Once you have the IP ranges, update your database's firewall or access control settings to permit connections only from these ranges. This method ensures that only GitHub Actions runners can access your database, adding an extra layer of security compared to a publicly accessible setup.

For workflows requiring higher security or control, you can deploy self-hosted runners within your own Virtual Private Cloud (VPC). These runners operate within your private network, enabling a secure connection to your database without exposing it to the public internet.

Self-hosted runners are ideal for environments with stringent security policies or compliance requirements. For guidance on setting up and managing self-hosted runners, see the GitHub documentation.

Allowing Atlas to connect directly to your database in GitHub Actions workflows enhances flexibility but requires careful consideration of security. Publicly accessible databases offer simplicity but increase exposure, while allow-listed IPs and self-hosted runners provide greater control and security. Choose the method that best balances your workflow needs with your infrastructure’s security requirements.

**Examples:**

Example 1 (bash):
```bash
curl https://api.github.com/meta | jq .actions
```

---

## Automatic Aurora DSQL Schema Migrations with Atlas

**URL:** https://atlasgo.io/guides/dsql/automatic-migrations

**Contents:**
- Automatic Aurora DSQL Schema Migrations with Atlas
    - Enter: Atlas​
- Prerequisites​
  - MacOS
  - Linux
  - Windows
- Logging in to Atlas​
- Connecting to Aurora DSQL​
- Inspecting the Schema​
- Declarative Migrations​

Amazon Aurora DSQL is a serverless, distributed relational database service optimized for transactional workloads. Aurora DSQL is PostgreSQL-compatible (version 16), offering ACID transactions with strong consistency and snapshot isolation. It provides 99.99% single-Region and 99.999% multi-Region availability with automatic scaling and self-healing architecture.

Support for Aurora DSQL is available exclusively to Pro users. To use this feature, run:

Atlas helps developers manage their database schema as code - abstracting away the intricacies of database schema management. With Atlas, users provide the desired state of the database schema and Atlas automatically plans the required migrations.

In this guide, we will dive into setting up Atlas for Aurora DSQL schema migrations, and introduce the different workflows available.

To download and install the latest release of the Atlas CLI, simply run the following in your terminal:

Get the latest release with Homebrew:

To pull the Atlas image and run it as a Docker container:

If the container needs access to the host network or a local directory, use the --net=host flag and mount the desired directory:

Download the latest release and move the atlas binary to a file location on your system PATH.

Use the setup-atlas action to install Atlas in your GitHub Actions workflow:

For other CI/CD platforms, use the installation script. See the CI/CD integrations for more details.

If you want to manually install the Atlas CLI, pick one of the below builds suitable for your system.

To use Aurora DSQL with Atlas, you'll need to log in to Atlas. If it's your first time, you will be prompted to create both an account and a workspace (organization):

Atlas uses the dsql:// scheme for connecting to Aurora DSQL clusters:

Connect to a database (all schemas):

Connect to a specific schema using the search_path query parameter:

The atlas schema inspect command supports reading the database description provided by a URL and outputting it in different formats, including Atlas DDL (default), SQL, and JSON. In this guide, we will demonstrate the flow using both the Atlas DDL and SQL formats, as the JSON format is often used for processing the output using jq.

To inspect your Aurora DSQL cluster, use the -u flag and write the output to a file named schema.hcl:

Open the schema.hcl file to view the Atlas schema that describes your database.

To inspect your Aurora DSQL cluster, use the -u flag and write the output to a file named schema.sql:

Open the schema.sql file to view the inspected SQL schema that describes your database.

For in-depth details on the atlas schema inspect command, covering aspects like inspecting specific schemas, handling multiple schemas concurrently, excluding tables, and more, refer to our documentation here.

The declarative approach, sometimes called "state-based migrations", lets users manage schemas by defining the desired state of the database as code. Atlas then inspects the target database and calculates an execution plan to reconcile the difference between the desired and actual states. Let's see this in action.

We will start off by making a change to our schema file, such as adding a repos table:

Now that our desired state has changed, to apply these changes to our database, Atlas will plan a migration for us by running the atlas schema apply command:

Approve the proposed changes, and that's it! You have successfully run a declarative migration.

For a more detailed description of the atlas schema apply command refer to our documentation here.

Similar to how Docker images are pushed to Docker Hub, you can push your schema to Atlas Cloud for versioning, collaboration, and deployment:

Once pushed, Atlas prints a URL to the schema. You can then apply it to any database using the schema URL:

This workflow allows you to manage your schema centrally and deploy it to multiple environments without having the schema files locally.

For more advanced workflows, you can use atlas schema plan to pre-plan and review migrations before applying them. This enables teams to plan, lint, and review changes during the PR stage, edit generated SQL if needed, and ensure no human intervention is required during deployment.

Alternatively, the versioned migration workflow, sometimes called "change-based migrations", allows each change to the database schema to be checked-in to source control and reviewed during code-review. Users can still benefit from Atlas intelligently planning migrations for them, however they are not automatically applied.

In the versioned migration workflow, our database state is managed by a migration directory. The migration directory holds all of the migration files created by Atlas, and the sum of all files in lexicographical order represents the current state of the database.

To create our first migration file, we will run the atlas migrate diff command, and we will provide the necessary parameters:

Run ls migrations, and you'll notice that Atlas has automatically created a migration directory for us, as well as two files:

The migration file represents the current state of our database, and the sum file is used by Atlas to maintain the integrity of the migration directory. To learn more about the sum file, read the documentation.

Now that we have our first migration, we can apply it to a database. There are multiple ways to accomplish this, with most methods covered in the guides section. In this example, we'll demonstrate how to push migrations to Atlas Cloud, much like how Docker images are pushed to Docker Hub.

Let's name our new migration project app and run atlas migrate push:

Once the migration directory is pushed, Atlas prints a URL to the created directory.

Once our app migration directory has been pushed, we can apply it to a database from any CD platform without necessarily having our directory there.

We'll create a simple Atlas configuration file (atlas.hcl) to store the settings for our environment:

The final step is to apply the migrations to the database. Let's run atlas migrate apply with the --env flag to instruct Atlas to select the environment configuration from the atlas.hcl file:

Migrations generated with docker://dsql or a DSQL cluster as a dev-database automatically include the -- atlas:txmode none directive. For manually written migration files, add this directive at the top or use --tx-mode none when applying.

After applying the migration, you should receive a link to the deployment and the database where the migration was applied.

Once you have your migration directory set up, the next step is to integrate Atlas into your CI/CD pipeline. Atlas provides native integrations for popular platforms:

Set up CI/CD with GitHub Actions

Set up CI/CD with GitLab CI

Set up CI/CD with Bitbucket Pipelines

Set up CI/CD with Azure DevOps

Deploy schema changes with Terraform

Deploy schema changes with Kubernetes

Aurora DSQL has some limitations compared to standard PostgreSQL that you should be aware of:

Advisory Locks, Procedures, Triggers, Sequences, Extensions, JSON/JSONB, Foreign Key Constraints, Partitions, Temporary Tables, TRUNCATE, ON DELETE CASCADE

For complete compatibility information, see the Aurora DSQL SQL Feature Compatibility documentation.

DSQL does not support PostgreSQL advisory lock functions (pg_try_advisory_lock), so Atlas cannot acquire locks to prevent concurrent migrations. Ensure only one Atlas process runs against a DSQL database at a time. We recommend following the Modern Database CI/CD guide to set up proper serialization of migration deployments.

Atlas uses a dev database to normalize schemas, validate them, and simulate migrations. This temporary database allows Atlas to detect errors early and generate accurate migration plans.

Recommended approach: For full compatibility, use a real DSQL cluster as your dev database:

Alternative: Docker-based dev database

For local development without provisioning additional infrastructure, Atlas offers docker://dsql. This uses a PostgreSQL container but generates DSQL-compatible SQL (e.g., CREATE INDEX ASYNC):

The Docker container runs PostgreSQL, not actual DSQL. Some DSQL limitations (e.g., no foreign keys, no triggers) are not enforced during local development. Ensure your schema only uses DSQL-supported features.

DSQL does not support DDL and DML in the same transaction, and a transaction can include only one DDL statement. When planning migrations against a DSQL database, Atlas automatically adds the -- atlas:txmode none directive to migration files.

For manually written migration files, you can either add the directive at the top of each file:

Or use the --tx-mode flag when applying migrations:

DSQL requires async index creation. Atlas automatically uses CREATE INDEX ASYNC instead of CREATE INDEX CONCURRENTLY for DSQL connections.

In this guide, we demonstrated how to set up Atlas to manage your Aurora DSQL database schema. We covered both declarative and versioned migration workflows, and showed how to generate migrations, push them to an Atlas workspace, and apply them to your databases. Atlas has many more features to explore. To learn more, check out the Atlas documentation.

As always, we would love to hear your feedback and suggestions on our Discord server.

To learn more about Aurora DSQL, check out the official AWS documentation:

**Examples:**

Example 1 (unknown):
```unknown
atlas login
```

Example 2 (shell):
```shell
curl -sSf https://atlasgo.sh | sh
```

Example 3 (shell):
```shell
brew install ariga/tap/atlas
```

Example 4 (shell):
```shell
docker pull arigaio/atlasdocker run --rm arigaio/atlas --help
```

---

## CI/CD for Databases on Bitbucket Pipelines - Versioned Workflow

**URL:** https://atlasgo.io/guides/ci-platforms/bitbucket-versioned

**Contents:**
- CI/CD for Databases on Bitbucket Pipelines - Versioned Workflow
- Prerequisites​
  - Installing Atlas​
  - MacOS
  - Linux
  - Windows
  - Creating a bot token​
  - Creating a secret for your database URL​
  - Creating a Bitbucket access token (optional)​
- Versioned Migrations Workflow​

Bitbucket Pipelines is a built-in CI/CD service in Bitbucket that allows you to automatically build, test, and deploy your code. Combined with Atlas, you can manage database schema changes with confidence.

In this guide, we will demonstrate how to use Bitbucket Pipelines and Atlas to set up CI/CD pipelines for your database schema changes using the versioned migrations workflow.

To download and install the latest release of the Atlas CLI, simply run the following in your terminal:

Get the latest release with Homebrew:

To pull the Atlas image and run it as a Docker container:

If the container needs access to the host network or a local directory, use the --net=host flag and mount the desired directory:

Download the latest release and move the atlas binary to a file location on your system PATH.

Use the setup-atlas action to install Atlas in your GitHub Actions workflow:

For other CI/CD platforms, use the installation script. See the CI/CD integrations for more details.

If you want to manually install the Atlas CLI, pick one of the below builds suitable for your system.

After installing Atlas locally, log in to your organization by running the following command:

To report CI run results to Atlas Cloud, create an Atlas Cloud bot token by following these instructions and copy it.

Next, in your Bitbucket repository, go to Repository settings -> Repository variables and create a new secured variable named ATLAS_TOKEN. Paste your token in the value field.

To avoid having plain-text database URLs that may contain sensitive information in your configuration files, create another secured variable named DATABASE_URL and populate it with the URL (connection string) of your database.

To learn more about formatting URLs for different databases, see the URL documentation.

Atlas can post lint reports as comments on pull requests. To enable this, create a Bitbucket app password with pullrequest:write permissions. Then, add it as a secured variable named BITBUCKET_ACCESS_TOKEN.

In the versioned workflow, changes to the schema are represented by a migration directory in your codebase. Each file in this directory represents a transition to a new version of the schema.

Based on our blueprint for Modern CI/CD for Databases, our pipeline will:

In this guide, we will walk through each of these steps and set up a Bitbucket Pipelines configuration to automate them.

The full source code for this example can be found in the atlas-examples/versioned repository.

First, define your desired database schema. Create a file named schema.sql with the following content:

Create a configuration file for Atlas named atlas.hcl with the following content:

Now, generate your first migration by comparing your desired schema with the current (empty) migration directory:

This command will automatically create a migrations directory with a migration file containing the SQL statements needed to create the users table and index, as defined in our file linked at src in the dev environment.

Run the following command from the parent directory of your migration directory to create a "migration directory" repository in your Atlas Cloud organization:

This command pushes the migrations directory linked in the migration dir field in the dev environment defined in our atlas.hcl to a project in the Schema Registry called bitbucket-atlas-action-versioned-demo.

Atlas will print a URL leading to your migrations on Atlas Cloud. You can visit this URL to view your migrations.

Create a bitbucket-pipelines.yml file in the root of your repository with the following content:

This configuration uses master as the default branch name. If your Bitbucket repository uses a different default branch (such as main), update the branches: section accordingly:

Let's break down what this pipeline configuration does:

After the pull request is merged into the master branch, the migrate/push step will push the new state of the migration directory to the Schema Registry on Atlas Cloud.

The migrate/apply step will then deploy the new migrations to your database.

Let's take our pipeline for a spin:

In this guide, we demonstrated how to use Bitbucket Pipelines with Atlas to set up a modern CI/CD pipeline for versioned database migrations. Here's what we accomplished:

For more information on the versioned workflow, see the Versioned Migrations documentation.

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

## Secrets and IAM Authentication: Best Practices for Managing Database Credentials in Atlas

**URL:** https://atlasgo.io/guides/deploying/secrets

**Contents:**
- Secrets and IAM Authentication: Best Practices for Managing Database Credentials in Atlas
- Secret Stores​
- IAM Authentication​
- Retrieving Credentials from a Secret Store​
- Using IAM Authentication​

Database credentials are considered sensitive information and should be treated as such. In this guide, we will show how to use Atlas to handle database credentials in a secure manner. We will present two strategies for handling database credentials, and show how to use Atlas to implement them: IAM Authentication and Secret Stores.

Secret stores are systems or services that allow users to store and retrieve sensitive information. The main features of secret stores are encryption, access control, and auditing. All cloud providers offer some form of secret store service, and there are also many open-source alternatives.

When working with secret stores, Atlas assumes that the secret store is already provisioned and configured. Atlas supports the following secret stores:

Support for other secret stores is planned, if you have a specific request, please open an issue.

IAM authentication is a mechanism that allows users to authenticate to a database using their cloud provider credentials. The main advantage of IAM authentication is that it allows users to avoid storing database credentials altogether. Although setting this up may be more cumbersome, it is considered a best practice for many cloud providers. IAM authentication is also more secure than using passwords. Even strong passwords stored in encrypted form can be leaked and used by attackers. IAM authentication allows users to avoid storing database credentials altogether.

IAM authentication is currently supported on GCP and AWS. Support for other cloud providers is planned as well, if you have a specific request, please open an issue.

Atlas can retrieve information from a secret store at runtime using the runtimevar data source. The runtimevar data source uses the runtimevar package from the Go CDK. To read more about using runtimevar with Atlas, view the data source documentation.

Create a secret a secret to store the database password using the AWS CLI:

Note the database secret name and the region (us-east-1), we will use them in the next part.

Create a new file named atlas.hcl with the following contents:

Let's breakdown the configuration:

Run atlas schema inspect --env dev to verify that Atlas is able to connect to the database.

If you using RDS Password Management, RDS will maintain a secret in JSON format similar to:

To decode the json payload and retrieve the password from it, use the jsondecode standard lib func. also notice this password may contain special characters and therefore must be escaped using the urlescape func.

Use the next atlas.hcl file as an example:

Create a encrypted parameter to store the database password using the AWS CLI:

Note the database parameter name and the region (us-east-1), we will use them in the next part.

Create a new file named atlas.hcl with the following contents:

Let's breakdown the configuration:

Run atlas schema inspect --env dev to verify that Atlas is able to connect to the database.

Create a secret a secret to store the database password using the GCP CLI:

Create a new file named atlas.hcl with the following contents:

Let's breakdown the configuration:

Run atlas schema inspect --env dev to verify that Atlas is able to connect to the database.

The HashiVault data source is available only to Atlas Pro users. To use this feature, run:

Let's breakdown the configuration:

For KV v2, use the endpoint format secret/data/your-secret-name. For KV v1, use secret/your-secret-name (as mentioned in the Vault documentation).

Atlas can retrieve short-lived credentials from the cloud provider and use them to connect to the database. The passwords are retrieved using special data sources that are specific to each cloud provider.

Enable IAM Authentication for your database. For instructions on how to do this, see the AWS documentation.

Create a database user and grant it permission to authenticate using IAM, see the AWS documentation for instructions.

Create an IAM role with the "rds-db:connect" permission for the specific database and user. For instructions on how to do this, see the AWS documentation.

Create a new file named atlas.hcl with the following contents:

Let's breakdown the configuration:

The gcp_cloudsql_token data source generates a short-lived token for an GCP CloudSQL database using IAM Authentication.

To use this data source:

Enable IAM Authentication for your database. For instructions on how to do this, see the GCP documentation.

Create a database user and grant it permission to authenticate using IAM, see the GCP documentation for instructions.

Create a file named atlas.hcl with the following contents:

The allowCleartextPasswords and tls parameters are required for the MySQL driver to connect to CloudSQL. For PostgreSQL, use sslmode=require to connect to the database.

Let's breakdown the configuration:

**Examples:**

Example 1 (bash):
```bash
aws secretsmanager create-secret \  --name db-pass-demo \  --secret-string "p455w0rd"
```

Example 2 (json):
```json
{    "ARN": "arn:aws:secretsmanager:us-east-1:1111111111:secret:db-pass-demo-aBiM5k",    "Name": "db-pass-demo",    "VersionId": "b702431d-174f-4a8f-aee5-b80e687b8bf1"}
```

Example 3 (python):
```python
data "runtimevar" "pass" {  url = "awssecretsmanager://db-pass-demo?region=us-east-1"}env "dev" {  url = "mysql://root:${data.runtimevar.pass}@host:3306/database"}
```

Example 4 (json):
```json
{  "username": "admin",  "password": "p455w0rd"}
```

---

## Atlas vs Liquibase: Why Modern Teams Choose Atlas

**URL:** https://atlasgo.io/guides/atlas-vs-liquibase

**Contents:**
- Atlas vs Liquibase: Why Modern Teams Choose Atlas
- Quick Comparison​
- Migration Workflows​
  - Declarative vs Migration-based​
      - Declarative vs. Versioned Workflows
  - Automatic Migration Planning​
- Migration Safety, Policy and Governance​
- Down Migrations and Rollback​
- CI/CD Integration and Platform Fit​
  - Kubernetes Native​

Modern database development demands deterministic planning, end-to-end automation and strong safety rails. Atlas provides a schema-as-code engine that supports both declarative and versioned workflows and tightly integrates with CI/CD tooling. Liquibase is a classic migration runner that uses changelogs-files where users manually define ordered changesets. This document summarizes Atlas's capabilities and contrasts them with Liquibase so that you can choose the right tool for your team.

This document is maintained by the Atlas team and was last updated in September 2025. It may contain outdated information or mistakes. For Liquibase's latest details and their own comparison, please refer to the official Liquibase website.

Atlas supports both declarative (state-based) and versioned (migration-based) workflows. In declarative mode, you express your desired schema in HCL, SQL, an ORM model, a database URL, or any mix of these sources. Atlas then computes a migration plan by diffing your desired state against the live database, using a deterministic engine to plan and apply the transition based on your company policies.

In versioned mode, Atlas compares the desired schema against the current migration directory and generates new migration files with atlas migrate diff. The same deterministic engine powers both workflows, which can be executed as part of modern CI/CD pipelines.

Liquibase, by contrast, is strictly migration-based. You maintain a hand-written changelog of ordered changesets, each specifying a change (for example createTable, addColumn) and optional preconditions or labels. When you run update, Liquibase records each new changeset in the DATABASECHANGELOG table. If a changeset’s checksum differs from its previous record, Liquibase halts execution.

Read more about the differences between declarative and versioned migration workflows.

Atlas automatically plans migrations based on schema diffing. You run atlas schema apply against a live database or atlas migrate diff against a migration directory; Atlas inspects the current schema, compares it to the desired schema, and emits a series of SQL statements that respect team policies. This eliminates human error and ensures deterministic, idempotent migrations. Atlas can generate partial or complete migration plans and supports complex objects like triggers, functions and views.

Liquibase offers a diff-changelog command that compares two databases and produces a changelog with deployable changesets. This can help generate migrations when synchronizing environments or detecting drift. However, diff-changelog is an ad-hoc tool; the typical Liquibase workflow still requires developers to design each change manually and commit it to the changelog. Liquibase does not provide a declarative mode where you describe the desired end state and let the tool compute the plan.

Atlas treats database schemas as code. Before applying changes, it runs linting and policy checks to detect destructive operations, table locks, potential constraint violations, and other risks. Teams can define and enforce custom policies (for example, naming conventions or no-FK rules) directly in CI/CD pipelines. Atlas also supports pre-migration checks-SQL assertions that run before applying a migration-and enforces migration directory integrity to prevent conflicts or divergence between environments.

Liquibase validates migration integrity by computing a checksum for each changeset and storing it in the MD5SUM column of the DATABASECHANGELOG table. If a changeset has been modified after deployment, Liquibase recomputes the checksum and aborts the update on mismatch. It also supports preconditions inside changesets (similar to pre-migration checks in Atlas), allowing migrations to stop when certain conditions are not met. However, Liquibase does not provide semantic linting (for example, detecting locking or destructive operations) or a declarative policy engine for enforcing safety and compliance rules.

Rolling back schema changes safely is critical. In the Atlas ecosystem, rollback is dynamic and state-aware. The atlas migrate down command inspects the current database state and generates the exact SQL required to revert to a previous version or tag. It handles partial failures, runs pre-migration checks and supports transactional or step-by-step execution. Approval workflows can be enforced in CI/CD or Atlas Cloud.

Liquibase supports rollback via several commands - rollback, rollback-to-date and rollback-count - that revert changes after a specified tag, time or number of changesets. Liquibase also provides targeted rollback commands such as rollback-one-changeset and rollback-one-update and an option to automatically roll back on error using --rollback-on-error. Automatic rollback generation is limited: Liquibase can auto-generate rollback SQL only for some change types (e.g., createTable, renameColumn, addColumn), but operations like dropTable or formatted SQL require you to write custom rollback logic. Developers must maintain rollback statements in their changelog, increasing the chance of divergence between up and down migrations.

Atlas is built for modern CI/CD and GitOps workflows. There are official GitHub Actions, GitLab components, CircleCI orbs and Bitbucket pipelines for planning, linting, applying and rolling back migrations. Atlas also provides a Kubernetes Operator with CRDs (AtlasSchema and AtlasMigration) and a Terraform provider to manage schemas alongside infrastructure. Native webhooks, drift alerts and approval flows are available via Atlas Cloud.

Liquibase integrates with build tools through its CLI, Maven, Gradle and Ant plugins and can be embedded as a Java library. It also offers an official GitHub Action, a Jenkins plugin, and supports GitLab pipelines and Spinnaker. Liquibase provides a Docker container for integration into containerized environments and integrates with Spring Boot via configuration and customizers. However, it does not provide an official Kubernetes operator or Terraform provider; running in Kubernetes typically involves using the CLI in an init container.

Atlas provides a production-ready Kubernetes Operator that uses Kubernetes CRDs (Custom Resource Definitions) to manage schema state as a first-class Kubernetes resource. You can choose between declarative or versioned workflows, backed by AtlasSchema and AtlasMigration CRDs respectively.

Features and capabilities:

Liquibase doesn't provide an official Kubernetes Operator.

Deploying to Kubernetes with the Atlas Operator and Argo CD

Deploying to Kubernetes with the Atlas Operator and Flux CD

Deploying to Kubernetes from Atlas Schema Registry

Atlas offers a first-class Terraform provider that makes database schemas part of your Infrastructure-as-Code workflows. With support for both declarative and versioned migration modes, teams can choose the workflow that best fits their delivery model.

Capabilities and features:

Liquibase has no official Terraform provider.

Atlas is distributed as a small statically linked Go binary (≈63 MB) and a Docker image. It requires no external runtime. You can run Atlas in containers, CI agents or embed it via the Go SDK.

Liquibase is implemented in Java and requires a JVM. According to Liquibase's system requirements, you must provide Java 8 or newer (the installer includes Java, but manual installations require you to supply your own JVM). Liquibase also offers a Java API to run migrations inside your application.

Atlas treats your database schema as code. You define the desired state in HCL or SQL files, which serve as the single source of truth for your schema. This declarative approach means you can read a file and immediately understand what your database should look like. Atlas can also import schema definitions from ORMs (e.g., Hibernate, GORM, Django, SQLAlchemy) or from existing databases using the atlas inspect command, which exports a database schema to HCL/SQL. This makes it easy to adopt Atlas for existing projects and maintain your schema in version control alongside your application code.

Liquibase uses changelog files that store ordered changesets in XML, YAML, JSON or SQL formats. Unlike Atlas's declarative schemas, Liquibase has no single source of truth for the schema-the current schema is the accumulated result of applying all changesets in order. To understand what your database should look like, you must mentally (or programmatically) replay all historical changes. This makes it harder to reason about the current state and increases the risk of inconsistencies across environments.

Atlas Cloud centralizes schema management. When you push schemas and migrations to the registry, you get:

Atlas includes built-in support for managing multi-tenant database environments, commonly used in database-per-tenant and schema-per-tenant architectures. With Atlas, teams can define logical tenant groups to plan and apply schema changes across many databases in a single operation. This simplifies the management of large fleets while ensuring consistency and reducing the risk of drift or deployment errors.

To learn more, check out the Database-per-Tenant guide.

AI tools like GitHub Copilot, Cursor, and Claude Code are great at writing code, but generating database migrations is a different challenge. As schemas grow more complex, ensuring migrations are deterministic, predictable, and aligned with company policies becomes critical.

Atlas solves this problem by letting AI tools focus on editing the schema while Atlas provides the infrastructure for:

Copilot and Ask Atlas - Atlas also includes a built-in chat assistant that can answer questions about your project, explain migration errors, generate schema tests, and suggest safer patterns. All commands go through Atlas's deterministic engine - raw SQL is never executed directly.

To learn more, check out the Atlas with AI Tools docs.

Configure GitHub Copilot with Atlas-specific instructions.

Set up Cursor with Atlas-specific rules.

Set up Claude Code with Atlas-specific instructions.

Liquibase supports a broad range of databases, many through community-maintained drivers designed primarily for running SQL scripts. It provides a straightforward model for teams that prefer to manage changes manually with changelog files.

Atlas takes a more comprehensive, integrated approach. It delivers deep, first-class support for each database, including schema inspection and diffing, automatic migration planning, policy enforcement, testing, drift detection, and security checks.

Supported databases include PostgreSQL, MySQL/MariaDB, ClickHouse, SQL Server, Oracle, SQLite, CockroachDB, TiDB, Redshift, Spanner, Snowflake, and others. By treating the schema as code, Atlas enables deterministic, policy-driven migrations, automates security and compliance validation, integrates seamlessly with AI development tools such as Cursor and Claude Code, and maintains consistent environments across development and production.

Liquibase has been a well-known tool for managing database changes for many years. Its changelog-based format and broad database support make it suitable for teams that prefer manually authored migration scripts and a Java-based workflow.

Atlas takes a different approach. It treats the database schema as code, automatically plans migrations from a declared desired state, enforces safety, security and compliance policies, and provides a built-in testing framework. With native integrations into modern CI/CD, Kubernetes, and Terraform workflows, Atlas offers a more automated and deterministic alternative for teams adopting database-as-code practices.

**Examples:**

Example 1 (yaml):
```yaml
apiVersion: db.atlasgo.io/v1alpha1kind: AtlasSchemametadata:  name: myapp-schemaspec:  url: postgresql://myapp-db:5432/myapp  schema:    sql: |      CREATE TABLE users (        id UUID PRIMARY KEY DEFAULT gen_random_uuid(),        email VARCHAR(255) UNIQUE NOT NULL      );  policy:    lint:      destructive:        error: true
```

Example 2 (unknown):
```unknown
resource "atlas_schema" "myapp" {  hcl        = file("schema.hcl")  url        = var.database_url  dev_db_url = "docker://postgres/15/dev"}
```

---

## Customizing Inspection Output Programmatically with Go Templates

**URL:** https://atlasgo.io/guides/go-templates

**Contents:**
- Customizing Inspection Output Programmatically with Go Templates
  - Example: Generating ORM Models​
  - Template Functions​

Atlas supports templating inspection output using Go templates, similar to tools like kubectl and docker. This lets you generate custom output at runtime.

If you're new to Go templates, see the Go documentation.

Templates are evaluated against the result of a schema inspection, which is an object with two fields:

See SchemaInspect and Realm for full details.

For complete examples of using Go templates to generate ORM models, see:

Atlas includes several built-in template functions to help format and manipulate the output:

Stops the template execution with the given error message.

Asserts that the condition is true, otherwise stops the template execution with the given error message.

Converts the given string to lower case.

Converts the given string to upper case.

Replaces all occurrences of old in s with new.

Trims leading and trailing whitespace from the given string.

Joins the elements of the given slice of strings into a single string, separated by the given separator.

Splits the given string by the specified separator and returns a slice of strings.

Trims leading and trailing whitespace from each string in the given slice.

Checks if the given string starts with the specified prefix.

Checks if the given string ends with the specified suffix.

Removes the specified prefix from the given string.

Removes the specified suffix from the given string.

Returns the result of subtracting the second integer from the first.

Returns the sum of the provided integers. If no integers are provided, returns 0.

Increments the given integer by 1 and returns the result.

Returns the product of two integers.

Returns the result of dividing the first integer by the second. Returns 0 on division by zero.

Returns the remainder of dividing the first integer by the second.

Parses the given string as a txtar archive and returns it as an Archive object.

Executes the given template with the provided context and returns the result as a trimmed string.

Note, unlike the include function, the exec function returns the result of the template as a trimmed strings.

Executes the named template with the provided context and returns the result as a string.

Returns the SQL type of the given column as a string.

Creates a dictionary from a list of key-value pairs.

Retrieves the value associated with the given key from the dictionary.

Sets the value for the given key in the dictionary and returns the updated dictionary.

Deletes the key from the dictionary and returns the updated dictionary.

Checks if the dictionary contains the specified key.

Creates a list from the provided values.

Appends the given values to the list and returns a new list.

**Examples:**

Example 1 (json):
```json
{{- if ne (len .Realm.Schemas) 1 }}  {{- fail "expect exactly one schema" }}{{- end }}
```

Example 2 (json):
```json
{{- assert (eq (len .Realm.Schemas) 1) "only one schema is supported in this example" }}
```

Example 3 (go):
```go
{{- $v := replace .Realm.Name " " "_" | lower }}
```

Example 4 (json):
```json
{{- (include "sub-template" .) | txtar |  write }}
```

---

## Automatic Redshift Schema Migrations with Atlas

**URL:** https://atlasgo.io/guides/redshift

**Contents:**
- Automatic Redshift Schema Migrations with Atlas
    - Enter: Atlas​
- Prerequisites​
  - MacOS
  - Linux
  - Windows
- Logging in to Atlas​
- Creating the Cluster​
- Find out the Connection URL​
  - Direct Network Connection​

Amazon Redshift is a powerful, managed data warehouse solution from AWS.

One of the top challenges developers face when working with large data sets on Redshift is managing the database schema. As your organization grows, data from more and more applications end up being represented in the data warehouse. This makes schemas complex and highly interconnected, and managing them becomes a daunting task.

Atlas helps developers manage their database schema as code - abstracting away the intricacies of database schema management. With Atlas, users provide the desired state of the database schema and Atlas automatically plans the required migrations.

In this guide, we will set up Atlas for declarative and versioned Redshift schema migration and walk through both workflows.

To download and install the latest release of the Atlas CLI, simply run the following in your terminal:

Get the latest release with Homebrew:

To pull the Atlas image and run it as a Docker container:

If the container needs access to the host network or a local directory, use the --net=host flag and mount the desired directory:

Download the latest release and move the atlas binary to a file location on your system PATH.

Use the setup-atlas action to install Atlas in your GitHub Actions workflow:

For other CI/CD platforms, use the installation script. See the CI/CD integrations for more details.

If you want to manually install the Atlas CLI, pick one of the below builds suitable for your system.

To use Redshift with Atlas, you'll need to log in to Atlas. If it's your first time, you will be prompted to create both an account and a workspace (organization):

If you want to use an existing Redshift cluster, you can skip this step.

Let's start off by spinning up a new Redshift cluster using AWS CLI:

The master-username and master-user-password are the credentials for the master user of the Redshift cluster. Make sure to replace them with your own values and make a note of them for future use.

For this example we will begin with a minimal database with a users table and an id as distributed key.

To create the table, run the following command:

Redshift instances can take a few minutes to spin up. Make sure to wait for the instance to be in the available state before proceeding.

To check the status of the cluster, run the following command:

To use Atlas with Redshift, we need to provide a connection URL to the database. In this section, we will see the different ways you can use Atlas to connect to your Redshift instance.

Atlas provides two ways to connect to a Redshift instance:

To connect to the Redshift instance using a direct network connection, you need to provide the connection URL in the following format:

To find out the endpoint of your Redshift Cluster, run the following command:

Observe the output and note down the Address and Port values. The connection URL will look like this:

The connection URL will look something like this:

Be sure to replace root, Password123, atlas-demo.cjxjxjxjxj.us-west-2.redshift.amazonaws.com, 5439, and dev with your own values.

To connect to the Redshift instance using the Redshift Data API, you need to provide the connection URL in the following format:

If you used atlas-demo as the name of your cluster from the previous step, the connection URL will look like this:

Be sure to replace atlas-demo and dev with your own values.

To learn about more advanced URL options such as using SSL, setting the search path, or using a different schema, connecting to Serverless Redshift, and more, refer to our URL documentation.

With your Redshift instance URL determined, we are now ready to start interacting with the database. In this sections and all that follow, replace the example URL with the one you determined in the previous section.

The atlas schema inspect command supports reading the database description provided by a URL and outputting it in different formats, including Atlas DDL (default), SQL, and JSON. In this guide, we will demonstrate the flow using both the Atlas DDL and SQL formats, as the JSON format is often used for processing the output using jq.

To inspect our Redshift instance, use the -u flag and write the output to a file named schema.hcl:

Open the schema.hcl file to view the Atlas schema that describes our database.

To inspect our locally-running SQL Server instance, use the -u flag and write the output to a file named schema.sql:

Open the schema.sql file to view the inspected SQL schema that describes our database.

For in-depth details on the atlas schema inspect command, covering aspects like inspecting specific schemas, handling multiple schemas concurrently, excluding tables, and more, refer to our documentation here.

To generate an Entity Relationship Diagram (ERD), or a visual representation of our schema, we can add the -w flag to the inspect command:

The declarative approach lets users manage schemas by defining the desired state of the database as code. Atlas then inspects the target database and calculates an execution plan to reconcile the difference between the desired and actual states. Let's see this in action.

We will start off by making a change to our schema file, such as adding a repos table:

Now that our desired state has changed, to apply these changes to our database, Atlas will plan a migration for us by running the atlas schema apply command:

Redshift does not support docker images, so we need another remote database to apply the changes. Let's create a new database in the same instance to use as dev database:

Then we can run the atlas schema apply command:

Apply the changes, and that's it! You have successfully run a declarative migration.

For a more detailed description of the atlas schema apply command refer to our documentation here.

To ensure that the changes have been made to the schema, let's run the inspect command with the -w flag once more and view the ERD:

Alternatively, the versioned migration workflow, sometimes called "change-based migrations", allows each change to the database schema to be checked-in to source control and reviewed during code-review. Users can still benefit from Atlas intelligently planning migrations for them, however they are not automatically applied.

In the versioned migration workflow, our database state is managed by a migration directory. The migration directory holds all of the migration files created by Atlas, and the sum of all files in lexicographical order represents the current state of the database.

To create our first migration file, we will run the atlas migrate diff command, and we will provide the necessary parameters:

Redshift does not support docker images, so we need another remote database to apply the changes. Let's create a new database in the same instance to use as dev database:

After creating the dev database, we can now run the atlas migrate diff command:

Run ls migrations, and you'll notice that Atlas has automatically created a migration directory for us, as well as two files:

Now that we have our first migration, we can apply it to a database. There are multiple ways to accomplish this, with most methods covered in the guides section. In this example, we'll demonstrate how to push migrations to Atlas Cloud, much like how Docker images are pushed to Docker Hub.

Migration Directory created with atlas migrate push

Let's name our new migration project app and run atlas migrate push:

Once the migration directory is pushed, Atlas prints a URL to the created directory, similar to the once shown in the image above.

Once our app migration directory has been pushed, we can apply it to a database from any CD platform without necessarily having our directory there.

Let's create a new database that represents our local environment:

Then, We'll create a simple Atlas configuration file (atlas.hcl) to store the settings for our local environment:

The final step is to apply the migrations to the database. Let's run atlas migrate apply with the --env flag to instruct Atlas to select the environment configuration from the atlas.hcl file:

Boom! After applying the migration, you should receive a link to the deployment and the database where the migration was applied. Here's an example of what it should look like:

Migration deployment report created with atlas migrate apply

After applying the first migration, it's time to update our schema defined in the schema file and tell Atlas to generate another migration. This will bring the migration directory (and the database) in line with the new state defined by the desired schema (schema file).

Let's make two changes to our schema:

Next, let's run the atlas migrate diff command once more:

Run ls migrations, and you'll notice that a new migration file has been generated.

Let's run atlas migrate push again and observe the new file on the migration directory page.

Migration Directory created with atlas migrate push

In this guide we learned about the declarative and versioned workflows, and how to use Atlas to generate migrations, push them to an Atlas workspace and apply them to databases.

For more in-depth guides, check out the other pages in this section or visit our Docs section.

Have questions? Feedback? Find our team on our Discord server.

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

## Managing Multi-Tenant Migrations with Atlas Cloud Control Plane

**URL:** https://atlasgo.io/guides/database-per-tenant/control-plane

**Contents:**
- Managing Multi-Tenant Migrations with Atlas Cloud Control Plane
- Setting up​
  - Pushing our project to Atlas Cloud​
- Working with Atlas Cloud​
  - Deploying from the Registry​
  - Another migration​
  - Deploying the new migration​
- Gaining Visibility​
  - Database Status​
  - Troubleshooting​

In the previous section, we demonstrated how to use the Atlas CLI to manage migrations for a database-per-tenant architecture. Next, we will see how to use the Atlas Cloud Control Plane to manage migrations across multiple databases.

In this section, we will be continuing our minimal example from before, so if you are just joining us, please follow the steps in the previous section to set up your project.

Additionally, you will need an Atlas Cloud account. If you don't have one, you can sign up for free by running the following command and following the instructions on the screen:

In order to manage our migrations across multiple databases, we need push our project to the Atlas Cloud Schema Registry. But first, let's set up a local env block in our atlas.hcl file. Append the following to the file:

Next, push the project to the Atlas Cloud Schema Registry by running the following command:

Atlas will push our migration directory to the Schema Registry and print the URL of the project, for example:

Once we have successfully pushed our project to the Schema Registry, we can deploy from it to our target databases. To do this, let's make a small change to our prod env in atlas.hcl:

Now, we can deploy the migrations to our target databases by running:

Atlas will read the most recent version of our migration directory from the schema registry, apply the migrations to each target database, report the results to Atlas Cloud, and print the results:

In this case, we see that there were no new migrations to apply to the target databases. Let's show how this flow works when there is work to be done in the next section.

Let's plan another migration to our project. Create a new migration file by running:

In the editor, add the following SQL statements:

Save the file and exit the editor. Let's push the new migration to the Schema Registry:

After successfully pushing the new migration, we can deploy it to our target databases by running:

Atlas will apply the new migration to each target database and print the results:

Following the link will take you to the Atlas Cloud UI, where you can see the details of the deployment:

The Atlas Cloud Control Plane provides a centralized view of all your deployments across multiple databases. You can see the status of each deployment, the target databases, and the results of each migration.

To view the status of the different databases in your project, navigate to the "Databases" tab in the Atlas Cloud UI. Here, you can see the status of each database, the most recent migration applied, and the results of the migration.

Databases can be in one of three states:

If an error occurs during a migration, having a centralized view of all your deployments can help you quickly identify the issue and take corrective action. You can view the error message, the target database, and the migration that caused the error.

Suppose we run a deployment that fails during the schema migration phase, we can easily locate the error in the Atlas Cloud UI by navigating to the "Migrations" tab:

We quickly find the failed deployment and drill down to diagnose the issue:

From the logs, we see that 3 out of 4 migrations passed without action, but the last one failed. We see that it failed on tenant_4.db with the error message:

We can further drill down into the specific database target migration:

We now clearly see the issue, our data migration failed due to a unique constraint violation. Now, we can take corrective action to fix the issue and reapply the migration - usually by fixing the problematic data in our target database.

In this section, we demonstrated how to use the Atlas Cloud Control Plane to manage migrations across multiple target databases. We showed how to push our project to the Atlas Cloud Schema Registry, deploy migrations to target databases, and gain visibility into the status of our deployments.

While it is possible to manage migrations using the Atlas CLI, the Atlas Cloud Control Plane provides a centralized view of all your deployments, making it easier to manage and troubleshoot issues across multiple databases.

**Examples:**

Example 1 (unknown):
```unknown
atlas login
```

Example 2 (unknown):
```unknown
env "local" {  dev = "sqlite://?mode=memory"  migration {    dir = "file://migrations"  }}
```

Example 3 (shell):
```shell
atlas migrate push --env prod db-per-tenant
```

Example 4 (yaml):
```yaml
https://rotemtam85.atlasgo.cloud/dirs/4294967396
```

---

## Running Schema Migrations on AWS ECS/Fargate using Atlas

**URL:** https://atlasgo.io/guides/deploying/aws-ecs-fargate

**Contents:**
- Running Schema Migrations on AWS ECS/Fargate using Atlas
- Prerequisites​
- Storing database credentials in Secrets Manager​
- Reading secrets during deployment​
  - Running migrations before the application starts​

AWS Elastic Container Service (ECS) is a popular way to deploy containerized applications to AWS. ECS is a managed service that allows you to run containers on a cluster of EC2 instances, or on AWS Fargate, a serverless compute engine for containers.

In this guide, we will demonstrate how to deploy schema migrations to ECS/Fargate using Atlas. As deploying to ECS/Fargate is a vast topic that is beyond the scope of this guide, we will focus on the migration part only.

Because of its operational simplicity, we will discuss deployment to ECS where tasks are run on Fargate, but the techniques discussed here are relevant to any ECS deployment.

Prerequisites to the guide:

In order to run migrations, Atlas needs a connection string to the database. In order to avoid storing the database credentials in plain text in the ECS task definition, we will use AWS Secrets Manager to store the database credentials and pass them to the migration container as environment variables.

Let's start by creating a secret in AWS Secrets Manager that contains the database credentials:

The CLI responds with the details about the created secret, which we will use later:

To make sure that the ECS task has access to the secrets, we will need to add to the task's IAM role a policy that allows it to access the secrets. This will look something similar to:

To read our secret value during deployment we can use the runtimevar data source. To use this, create a project file named atlas.hcl:

Be sure to replace mydb with the name of your secret and to set the correct region in the query parameter.

Next, create a Dockerfile that will include your migration directory and project file. This is a variation of the baseline example we introduced in the "Creating container images for migrations" guide:

This image should be built and pushed to ECR (or another container registry) as part of your CI process.

In order to make sure that migrations run successfully before the application starts, we will need to update the ECS task definition to make the main application container depend on the migration container running to completion. This way, when you deploy a new version of the application, ECS will first run the migration container and only start the application container once the migration container exits successfully.

Notice that when running migrations for a distributed application, you will need to make sure that only one actor in our system tries to run the migrations at any given time to avoid race conditions with unknown outcomes. Luckily, Atlas supports this behavior out of the box. When running migrations, Atlas will first acquire a lock in the database (using advisory locking, in databases that support it) and then begin execution.

To achieve this, your task definition should look something similar to:

Notice a few points of interest in the above task definition:

**Examples:**

Example 1 (bash):
```bash
aws secretsmanager create-secret --name mydb --secret-string 'postgres://user:password@host:port/dbname'
```

Example 2 (json):
```json
{    "ARN": "arn:aws:secretsmanager:us-east-1:<account id>:secret:mydb-gxZ0Qe",    "Name": "mydb",    "VersionId": "ab6d1fc0-d1a0-49c8-9bfb-5fd9922ffc37"}
```

Example 3 (json):
```json
{   "Statement": [      {         "Action": [            "secretsmanager:GetSecretValue",            "secretsmanager:DescribeSecret"         ],         "Effect": "Allow",         "Resource": "arn:aws:secretsmanager:us-east-2:<account id>:secret:mydb-<random suffix>",         "Sid": ""      }   ],   "Version": "2012-10-17"}
```

Example 4 (bash):
```bash
data "runtimevar" "url" {  url = "awssecretsmanager://mydb?region=us-east-2"}env "deploy" {  url = "${data.runtimevar.url}"}
```

---

## Atlas vs Flyway (Redgate): Why Modern Teams Choose Atlas

**URL:** https://atlasgo.io/guides/atlas-vs-flyway

**Contents:**
- Atlas vs Flyway (Redgate): Why Modern Teams Choose Atlas
- Quick Comparison​
- Migration Workflows: Declarative and Versioned​
  - Current State vs Desired State​
  - Key Differences Between Atlas and Flyway​
- Migration Safety, Policy, and Governance​
- Down Migrations and Rollback​
  - Rolling Back vs Going Down​
  - Flyway vs Atlas​
- CI/CD Integration and Platform Fit​

Modern database development requires deterministic planning, end-to-end automation, and guardrails that prevent outages. Atlas is a schema-as-code system that supports both declarative and versioned workflows, integrates deeply with CI/CD, and offers integrated policy and testing frameworks. Flyway is a traditional migration runner that executes SQL scripts in order.

This document summarizes Atlas's capabilities and compares them with Flyway's to help you decide which tool is best for your team.

This document is maintained by the Atlas team and was last updated in September 2025. It may contain outdated information or mistakes. For Flyway's latest details and their own comparison, please refer to the official Flyway (Redgate) website.

Atlas supports two workflows for managing schema changes: declarative (state-based) and versioned (migrations-based). In both workflows, Atlas inspects the "current state," compares it to the "desired state," and plans the necessary statements to reach the desired state using a single deterministic migration planner.

Unlike Flyway, where you write and maintain ordered SQL migration files manually, Atlas automates migration planning based on the difference between the current and desired states.

Both workflows can be automated in CI/CD using Atlas Actions (GitHub, GitLab, Azure DevOps, etc.) or the Atlas CLI. After changes are planned, Atlas validates them with migration linting and policy checks before execution.

Atlas pioneered a code-first methodology for database management. Database logic is treated like application code: it can be linted, validated, and unit-tested after each change. By bringing modern software engineering practices such as static analysis, validation, and automated testing into schema management, Atlas provides a level of safety and reliability not found in traditional migration runners like Flyway:

Rolling back schema changes is often confused with "going down", but the concepts are not the same:

Unlike Flyway and other traditional tools, Atlas is designed for modern CI/CD workflows and integrates deeply with popular tools:

Atlas provides a production-ready Kubernetes Operator that uses Kubernetes CRDs (Custom Resource Definitions) to manage schema state as a first-class Kubernetes resource. You can choose between declarative or versioned workflows, backed by AtlasSchema and AtlasMigration CRDs respectively.

Features and capabilities:

Flyway doesn't provide an official Kubernetes Operator.

Deploying to Kubernetes with the Atlas Operator and Argo CD

Deploying to Kubernetes with the Atlas Operator and Flux CD

Deploying to Kubernetes from Atlas Schema Registry

Atlas offers a first-class Terraform provider that makes database schemas part of your Infrastructure-as-Code workflows. With support for both declarative and versioned migration modes, teams can choose the workflow that best fits their delivery model.

Capabilities and features:

Flyway has no official Terraform provider.

Atlas Cloud centralizes schema management. When you push schemas and migrations to the registry, you get:

Atlas includes built-in support for managing multi-tenant database environments, commonly used in database-per-tenant and schema-per-tenant architectures. With Atlas, teams can define logical tenant groups to plan and apply schema changes across many databases in a single operation. This simplifies the management of large fleets while ensuring consistency and reducing the risk of drift or deployment errors.

To learn more, check out the Database-per-Tenant guide.

AI tools like GitHub Copilot, Cursor, and Claude Code are great at writing code, but generating database migrations is a different challenge. As schemas grow more complex, ensuring migrations are deterministic, predictable, and aligned with company policies becomes critical.

Atlas solves this problem by letting AI tools focus on editing the schema while Atlas provides the infrastructure for:

Copilot and Ask Atlas - Atlas also includes a built-in chat assistant that can answer questions about your project, explain migration errors, generate schema tests, and suggest safer patterns. All commands go through Atlas's deterministic engine - raw SQL is never executed directly.

To learn more, check out the Atlas with AI Tools docs.

Configure GitHub Copilot with Atlas-specific instructions.

Set up Cursor with Atlas-specific rules.

Set up Claude Code with Atlas-specific instructions.

Flyway offers compatibility with a wide range of databases, many of which are supported through community-provided drivers that focus primarily on executing SQL scripts.

Atlas, by design, supports a more focused set of databases but provides deeper functionality for each: schema inspection and diffing, automatic migration planning, policy enforcement, testing, and drift detection.

Databases supported by Atlas currently include PostgreSQL, MySQL/MariaDB, ClickHouse, SQL Server, Oracle, SQLite, CockroachDB, TiDB, Redshift, Spanner, Snowflake, and others.

Teams adopt Atlas for deterministic planning and end-to-end safety:

Both Atlas and Flyway serve their purpose in the ecosystem. Flyway established important patterns for database migrations. Atlas builds on the versioned migrations foundations to provide a modern, cloud-native approach with comprehensive safety features and infrastructure integration.

**Examples:**

Example 1 (yaml):
```yaml
apiVersion: db.atlasgo.io/v1alpha1kind: AtlasSchemametadata:  name: myapp-schemaspec:  url: postgresql://myapp-db:5432/myapp  schema:    sql: |      CREATE TABLE users (        id UUID PRIMARY KEY DEFAULT gen_random_uuid(),        email VARCHAR(255) UNIQUE NOT NULL      );  policy:    lint:      destructive:        error: true
```

Example 2 (unknown):
```unknown
resource "atlas_schema" "myapp" {  hcl        = file("schema.hcl")  url        = var.database_url  dev_db_url = "docker://postgres/15/dev"}
```

---

## Deploying Schema Migrations to Database-per-Tenant Architecture

**URL:** https://atlasgo.io/guides/database-per-tenant/deploying

**Contents:**
- Deploying Schema Migrations to Database-per-Tenant Architecture
- Setting up​
  - Our config file​
  - An initial migration​
- Deploying the migrations​
  - Verifying our migrations were applied​
  - Checking for Drift​
- Next steps​

In the previous section, we learned how to define target groups in Atlas to manage migrations for a database-per-tenant architecture. In this section, we will see how to deploy migrations to the target groups.

For the purpose of this guide, we will use a simple example to demonstrate how to deploy migrations to target groups. To simplify things, we will be using SQLite files as our target databases and statically defining the target groups in the atlas.hcl file.

In our project directory, let's create a file named atlas.hcl with the following content:

Let's create an initial migration file to bootstrap our project:

Once the local editor opens, add the following SQL statements:

Save the file and exit the editor. Observe that two new files were created in the migrations/ directory:

We can deploy the migrations directly to the target group using the migrate apply command with the --env flag:

This command will apply the migrations to both tenant_1 and tenant_2 databases. Atlas will output:

As you can see from the output, the migration was applied to both databases. Observe that two new files were created in our project directory: tenant_1.db and tenant_2.db.

We can check the current schema of our local SQLite databases using the migrate status command. Run:

As expected, the tenant_1 database is up-to-date with the latest migration.

Additionally, we may want to verify that the schema of the tenant database is in sync with the latest migration. We can utilize the schema diff command to compare the current schema with the latest migration:

As you can see, deploying migrations to target groups is straightforward using the Atlas CLI, but getting visibility into the status of each tenant, is done individually. To bridge this gap, we will show how to use the Atlas Cloud control plane to gain visibility into the status of our system in the next section.

**Examples:**

Example 1 (bash):
```bash
locals {  tenant = ["tenant_1", "tenant_2"]}env "prod" {  for_each = toset(local.tenant)  url = "sqlite://${each.value}.db"  migration {    dir = "file://migrations"  }}
```

Example 2 (bash):
```bash
atlas migrate new --edit init
```

Example 3 (sql):
```sql
CREATE TABLE users (  id INTEGER PRIMARY KEY,  name TEXT NOT NULL);
```

Example 4 (unknown):
```unknown
├── 20240721101205_init.sql└── atlas.sum1 directory, 2 files
```

---

## Working with Atlas Registry

**URL:** https://atlasgo.io/guides/deploying/remote-directories

**Contents:**
- Working with Atlas Registry
  - Prerequisites​
  - Deploying migrations using Atlas Registry​
  - Read Migrations from Atlas Registry​
  - Viewing migration logs in Atlas Cloud​

In the past, we have recommended users to build a migrations Docker image as part of their CI pipeline and then use that image during their deployment process. This is still a valid approach, as it bundles together the Atlas binary needed to run migrations with the migrations themselves. However, over the last years we have received feedback from many users that this approach is cumbersome and requires a lot of boilerplate code to be written.

To address this, we have introduced the Atlas Schema Registry, which allows you to store schemas and migrations in the cloud and make them available later to your deployment pipelines by their tags.

On a high-level this approach works as follows:

This guide shows you how to set up this approach for your project.

Once your migration directory is pushed to the Registry, you can use the atlas CLI to fetches the migration directory from the Atlas Registry and apply the migrations to the database.

To get started, create a project configuration file named atlas.hcl:

Let's review what this configuration file does:

Once you have created your configuration file, you can read the available migrations from the Atlas Registry and apply them to the database using the atlas CLI using the following commands:

Let's review what these commands do:

Let's review what these commands do:

The atlas migrate apply command will run all migrations that have not been applied to the database yet:

After the migrations have been applied, you can view them in Atlas Cloud by heading to the /deployments page in your Atlas Cloud account. You should see a new migration log with the name of the environment you specified in the configuration file. Clicking on the migration-log will show you the details of the migration, including the statements and checks that were applied:

**Examples:**

Example 1 (jsx):
```jsx
env {  name = atlas.env  url  = getenv("DATABASE_URL")  migration {    dir = "atlas://<name of dir>"  }}
```

Example 2 (bash):
```bash
# Login first to Atlas Cloud.atlas login# Run migrations. Give an environment name, such as --env local.atlas migrate apply --env local
```

Example 3 (bash):
```bash
ATLAS_TOKEN="{{ YOUR_ATLAS_TOKEN }}" atlas migrate apply --env production
```

Example 4 (sql):
```sql
Migrating to version 20230306221009 (1 migrations in total):  -- migrating version 20230306221009    -> create table users (         id int primary key       );  -- ok (8.60933ms)  -------------------------  -- 68.037117ms  -- 1 migrations  -- 1 sql statements
```

---

## Automatic SQLAlchemy Migrations with Atlas

**URL:** https://atlasgo.io/guides/orms/sqlalchemy

**Contents:**
- Automatic SQLAlchemy Migrations with Atlas
  - Loading SQLAlchemy Models Into Atlas​
      - Standalone Mode
      - Python Script
  - Managing Database Objects​
      - Row-Level Security
      - Triggers
      - Extenstions

SQLAlchemy is one of the most popular ORMs in the Python ecosystem. While many projects use Alembic, developers often seek a more powerful and automated tool for SQLAlchemy migrations. Atlas provides a seamless integration with SQLAlchemy, offering a robust alternative to Alembic. It allows you to keep defining your schema as SQLAlchemy models while enjoying Atlas's advanced schema management features. Some examples are:

Advanced database features: Atlas can recognize and detect changes in many database features that are not natively supported by SQLAlchemy and Alembic, such as:

With Composite Schemas, these object can be now managed as part of your code.

CI/CD support: Catch issues before they hit production with robust GitHub Actions, GitLab, and CircleCI Orbs integrations. Detect risky migrations, test data migrations, database functions, and more. In addition, Atlas can be integrated into your pipelines to provide native integrations with your deployment machinery (e.g. Kubernetes Operator, Terraform, etc.).

Declarative workflow: Atlas can be used to manage your schema as code - the schema is continuously synced to Atlas Cloud and Atlas generates a migration plan for every new change, removing the need for a migration directory.

Get started with Atlas and SQLAlchemy.

The common case. If all of your SQLAlchemy models exist in a single module, you can use the provider directly to load your SQLAlchemy schema into Atlas.

Use Atlas as a Python script to load and manage your SQLAlchemy schema in Atlas.

Like many ORMs, SQLAlchemy provides a way to define the most common database objects, such as tables, columns, and indexes using Python classes and decorators. Atlas extends this capability by allowing you to define more advanced database objects such as composite types, domain types, and triggers.

Implement Row-Level Security (RLS) policies in your SQLAlchemy models to safeguard data and control access.

Learn how to automate database actions and logic with triggers in your SQLAlchemy models.

Use composite schema to integrate relevant extensions to your SQLAlchemy models.

---

## Using Atlas with Fly.io

**URL:** https://atlasgo.io/guides/deploying/fly-io

**Contents:**
- Using Atlas with Fly.io
- Release command​
- Defining the Dockerfile​
- Setting the database URL secret​
- Configuring fly.toml​
- Deploying the app​
- Improving the deployment pipeline​

Fly.io is a platform for running full stack apps and databases close to the users. Under the hood, Fly converts Docker images (or other OCI-compliant image formats) to Firecracker microVMs. Fly allows the deployment of the app in different regions and route the requests based on the app load and user closeness.

Apps on Fly can be deployed in one of three ways: using a Dockerfile, a Docker image or a buildpack.

In this guide, we will demonstrate how Atlas can be used to perform database schema migrations for Fly.io deployments process using a Dockerfile. We will assume that you have already have a Fly project and are able to deploy it, if you are new to Fly, check the getting started guide.

When you configure your Fly project, you can define a release command. This command is executed during the release phase before the new version of your application is deployed. If it fails, i.e exits with a status code other than zero, Fly marks the deployment as failed as well. The release command is the recommended way to run database migrations on Fly.

The release command only allows executing commands that are present in the application image, meaning that we have to embed the Atlas binary with our application. We usually suggest a separate step for handling the migration, but since Fly currently does not support providing a separate image for the release phase, we recommend this solution.

Using Docker multi-stage builds, we can compose lightweight images from multiple steps that use heavier base images. In this guide, we will use a Go app as an example. Because Go is a compiled language, so we can use a separate step for building the target binary and another for producing the runtime container. This way the runtime environment can be smaller, omitting the build environment.

Suppose our project structure is similar to the one below:

Our objective is to build an image that contains the Atlas binary, the database migrations and our application code. For our Go app the Dockerfile can be defined as:

If you are using another compiled programming language, most of the time you will only have to change the build stage. If your application requires a runtime you may have to change the final stage as well.

It's important for the final image to have a shell that is capable of environment variable interpolation, like sh or bash. This is mostly due to behavior on Fly's side, where expanding environment variables don't currently work correctly on the release command.

While running the migration, Atlas needs to know the URL for the database. Fly has support for defining secrets, sensitive values that are available during runtime as environment variables. We can define the database URL using the command below:

If you use the flyctl command postgres attach the secret will be created automatically for you.

To tell Fly to execute the release command during a deployment, we need to add a deploy block with the release command provided:

With the release command defined, during new deployments a new temporary VM will be created and will execute the release command. If the commands succeed the deployment will continue, in case of failures the deployment will be aborted.

We can deploy the app with the command flyctl deploy. Fly will use a Docker installation (or a remote builder) to build the Docker image and push to the Fly registry.

The output of the release command will be presented to you on your terminal, but if you missed it, you can use the Monitoring page of your app or the fly logs command to see the previous logs entries.

Atlas will provide helpful information during the execution, here are a few examples of logs outputs:

You can always improve the deployment pipeline by leveraging Atlas and Fly GitHub Actions. For additional insights on the database schema and migrations, we recommend giving Atlas Cloud a try.

**Examples:**

Example 1 (unknown):
```unknown
.├── fly.toml├── go.mod├── go.sum├── main.go└── migrations    ├── 20221220000101_create_users.sql    └── atlas.sum
```

Example 2 (sql):
```sql
FROM arigaio/atlas:latest-alpine as atlas# build stageFROM golang:1.19.2-bullseye as buildWORKDIR /buildADD go.mod /build/go.modADD go.sum /build/go.sumADD main.go /build/main.goRUN CGO_ENABLED=0 go build -o app main.go# runtime stageFROM alpineCOPY --from=atlas /atlas /atlasCOPY migrations /migrationsCOPY --from=build /build/app /appCMD ["/app"]
```

Example 3 (python):
```python
flyctl secrets set DATABASE_URL="postgres://postgres:pass@localhost:5432/database?sslmode=disable"
```

Example 4 (json):
```json
[deploy]release_command = "sh -c '/atlas migrate apply --url $DATABASE_URL'"
```

---

## Integration tests with docker-compose

**URL:** https://atlasgo.io/guides/testing/docker-compose

**Contents:**
- Integration tests with docker-compose
- Example​
- Wrapping up​

When developing an application that uses a database, it's important to test your application against a real database. As good as your unit tests may be, some issues can only be caught by running proper integration tests.

If you use Atlas to manage your database schema, it only makes sense to use Atlas to prepare your database for integration tests as well. One way to achieve this is by using docker-compose to create a test environment for your tests to run against. Docker-compose allows you to easily spin up a test database and run your migrations against it, so you can verify that the application works as expected with the updated schema.

On a high-level, the process of setting up integration tests with docker-compose looks like this:

Suppose your project has the following directory structure:

The docker-compose.yaml file looks like this:

When you run docker-compose up, this is what happens:

After the migrations are applied, the database is ready to be used by your integration tests.

In conclusion, using docker-compose to set up your integration tests allows you to easily spin up a test database and apply your migrations to it. This ensures that your application is tested against an up-to-date database schema, and allows you to catch any issues that may arise when running against a real database.

Have questions? Feedback? Find our team on our Discord server.

**Examples:**

Example 1 (unknown):
```unknown
.├── docker-compose.yaml└── migrations    ├── 20221207103204_init.sql    └── atlas.sum1 directory, 3 files
```

Example 2 (yaml):
```yaml
version: "3.9"services:  mysql:    image: mysql:8.0.29    platform: linux/amd64    healthcheck:      test: mysqladmin ping -ppass    environment:      MYSQL_DATABASE: test      MYSQL_ROOT_PASSWORD: pass    ports:      - "3306:3306"    networks:      - db  migrate:    image: arigaio/atlas:latest    command: >      migrate apply      --url mysql://root:pass@mysql:3306/test    networks:      - db    depends_on:      mysql:        condition: service_healthy    volumes:      - ./migrations/:/migrationsnetworks:  db:
```

---

## Database-per-Tenant Architectures with Atlas

**URL:** https://atlasgo.io/guides/database-per-tenant/intro

**Contents:**
- Database-per-Tenant Architectures with Atlas
- Intro​
  - What is a Database per Tenant Architecture?​
  - Alternative Multi-Tenant Architectures​
  - Advantages​
  - Challenges​
- Database per Tenant Architectures with Atlas​

This guide describes how to utilize Atlas to manage database schemas in "Database per Tenant" architectures, a common pattern for deploying multi-tenant applications.

In a "Database per Tenant" architecture, each tenant has its own dedicated database (or a schema). Database-per-tenant architectures are commonly used in situations where there are considerations around data isolation, security, and scalability. It is worth noting it contrary to creating a fully isolated deployment for each tenant, in this architecture compute and other resources are shared across tenants.

In addition to a Database per Tenant architecture, there are other common multi-tenant architectures:

Database per Tenant architectures offer several advantages over other multi-tenant architectures:

This architecture decisions is one of my biggest regrets, and we are currently in the process of rebuilding into a single database model.

HN Thread on Database per Tenant Architecture

Despite their numerous advantages, Database per Tenant architectures present unique challenges, mostly around managing database schema migrations:

Atlas was built from the ground up to handle database-per-tenant architectures. In fact, Atlas Cloud itself is a multi-tenant application that uses a database-per-tenant architecture to manage its own schema.

Atlas supports database-per-tenant architectures both on the CLI and in the Cloud control plane.

In the following sections, we'll describe how to use Atlas to manage database schemas in a database-per-tenant architecture.

---

## Flyway Snapshot Alternative in Atlas

**URL:** https://atlasgo.io/guides/flyway-snapshot-alternative

**Contents:**
- Flyway Snapshot Alternative in Atlas
- Inspect and Snapshot Your Schema​
- What the Snapshot Includes​
- Customizing Snapshot Output​
  - Visualize with ERD​
- Export Database Schema to Code​
- Comparing Snapshots (Drift Detection)​
- Use Cases Covered (Compared to Flyway)​
- Example: Compare without Snapshot​
- Key Advantages over Flyway Snapshot​

The flyway snapshot command captures the structure of a database and stores it as a JSON file that represents its state at a specific point in time. This is often used for drift detection, change reviews, or as a baseline for further comparisons.

In Atlas, you can achieve the same workflow with a few key advantages using the atlas schema inspect command.

Unlike Flyway's snapshot feature, this capability is free in Atlas. With the schema inspect command, you can capture your database schema and export it in any format you need. The examples below show how to export a database to a SQL (DDL format), HCL, JSON, or even a Mermaid diagram. Next sections show more advanced exports, such as generating ORM models or structured code folders from your database schema.

This command connects to your database, inspects its structure, and produces a complete, version-controlled representation of your schema. The output can be stored in your Git repository, compared against other states, or used to detect drift between environments.

Atlas currently supports introspection for the following objects in the free version:

These are the core elements required for most schema-as-code and drift-detection workflows.

Using Atlas Pro, you can extend the schema snapshot to provide the full representation of your database's state, with complete dependency-graph and relationships between the different objects, including:

Atlas supports exporting the schema to custom formats using Go templates. This allows you to generate tailored outputs for your specific needs. For example, you can create documentation, custom reports, or export ORM definitions. For example:

📺 For a step-by-step example walk-through, watch our tutorial: Inspect Your Database Schema with Atlas

You can also visualize your schema as an interactive Entity Relationship Diagram (ERD). Use the --web flag to open an interactive ERD in Atlas Cloud:

Try it out in the component below:

Users who want to export the database to structured folders can follow the Export Schema to Code documentation. Atlas can organize your schema into a modular directory structure like this:

To export your schema into this structure, use the following command:

This will create a structured directory with your schema organized by object type (tables, views, functions, etc.), with a main.sql file as an entry point.

Once you have a snapshot of your schema, you can compare it to another state - a live database, a migration directory, or another snapshot file.

This command produces a deterministic diff between two schema states, allowing you to identify and review changes before applying them.

Learn more about drift detection and comparing schemas.

The atlas schema diff command can also be used to compare two live databases without creating intermediate snapshot files.

See comparing schemas for more details. Atlas supports comparing any source to any source.

**Examples:**

Example 1 (bash):
```bash
atlas schema inspect -u "<DATABASE_URL>" --format '{{ sql . }}' > schema.sql
```

Example 2 (bash):
```bash
atlas schema inspect -u "<DATABASE_URL>" > schema.hcl
```

Example 3 (bash):
```bash
atlas schema inspect -u "<DATABASE_URL>" --format '{{ json . }}' > schema.json
```

Example 4 (bash):
```bash
atlas schema inspect -u "<DATABASE_URL>" --format '{{ mermaid . }}' > schema.mmd
```

---

## CI/CD for Databases with Azure DevOps Repos

**URL:** https://atlasgo.io/guides/ci-platforms/azure-devops-repos

**Contents:**
- CI/CD for Databases with Azure DevOps Repos
- Prerequisites​
  - Installing Atlas​
  - MacOS
  - Linux
  - Windows
  - Setting up Azure DevOps​
  - Creating an Atlas Cloud bot token​
  - Creating secrets in Azure DevOps​
  - Configuring branch policies​

Azure DevOps provides a complete DevOps solution with integrated source control (Azure Repos) and CI/CD pipelines (Azure Pipelines). When your code is hosted in Azure Repos, you can configure pipelines to automatically trigger on pull requests and branch changes, creating a seamless development workflow.

In this guide, we will demonstrate how to set up Atlas database CI/CD workflows using Azure Repos with Azure DevOps Pipelines, including the necessary branch policies and PR triggers.

To download and install the latest release of the Atlas CLI, simply run the following in your terminal:

Get the latest release with Homebrew:

To pull the Atlas image and run it as a Docker container:

If the container needs access to the host network or a local directory, use the --net=host flag and mount the desired directory:

Download the latest release and move the atlas binary to a file location on your system PATH.

Use the setup-atlas action to install Atlas in your GitHub Actions workflow:

For other CI/CD platforms, use the installation script. See the CI/CD integrations for more details.

If you want to manually install the Atlas CLI, pick one of the below builds suitable for your system.

After installing Atlas locally, log in to your organization by running the following command:

To report CI run results to Atlas Cloud, create an Atlas Cloud bot token by following these instructions. Copy the token and store it as a secret using the following steps.

In your Azure DevOps project, go to Pipelines → Library and create a variable group:

To ensure your pipeline runs on pull requests, you need to configure branch policies:

Azure DevOps requires explicit permissions for pipelines to access repositories and perform certain operations. You need to grant the following permissions:

Repository permissions:

If you encounter permission errors during pipeline execution, check that the build service account has the necessary permissions. Common issues include insufficient repository access or missing project-level permissions.

Atlas supports two types of schema management workflows:

To learn more about the differences and tradeoffs between these approaches, see Declarative vs Versioned.

In the declarative workflow, you define the desired schema state (for example, using Atlas HCL or SQL schema files), and Atlas computes the changes required to reach it.

A typical Azure DevOps pull request (PR) flow looks like this:

In addition to the general prerequisites above, you will need:

One common layout is:

Below is a minimal atlas.hcl example. Replace the URLs with your own values.

And an example desired schema file:

This example uses a single pipeline with tasks. It runs schema plan on pull requests and schema push + schema apply on merges to main.

Create an azure-pipelines.yml file in the repository root.

On pull requests, you should see the pipeline run the schema plan action and print the planned SQL changes in the comment section.

On merges to main, you should see the pipeline run the schema push action (to publish the desired schema to Atlas Registry), and then run the schema apply action to apply changes to the target database.

In the versioned workflow, changes to the schema are represented by a migration directory in your codebase. Each file in this directory represents a transition to a new version of the schema.

Based on our blueprint for Modern CI/CD for Databases, our pipeline will:

Running the following command from the parent directory of your migration directory creates a "migration directory" repo in your Atlas Cloud organization (substitute "app" with the name you want to give the new Atlas repository before running):

Replace docker://postgres/16/dev with the appropriate dev database URL for your database. For more information on the dev database, see the dev database article.

Atlas will print a URL leading to your migrations on Atlas Cloud. You can visit this URL to view your migrations.

Create an azure-pipelines.yml file in the root of your Azure Repos repository with the following content. Remember to replace "app" with the real name of your repository.

Also, create an atlas.hcl file in the root of your Azure Repos repository with the following content:

Let's break down what this pipeline does:

Lint on Pull Requests: The migrate lint step runs automatically whenever a pull request is opened that modifies the migrations/ directory. Atlas analyzes the new migrations for potential issues like destructive changes, backward incompatibility, or syntax errors. Because we configured the githubConnection parameter, lint results appear as a comment directly on the GitHub pull request.

Push to Registry: When changes are merged into the main branch, the migrate push step pushes the migration directory to Atlas Cloud's Schema Registry. This creates a versioned snapshot of your migrations that can be referenced and deployed across environments.

Apply to Database: The migrate apply step deploys pending migrations to your database using the connection string stored in the DB_URL secret.

Let's take our new pipeline for a spin. Assume we have an existing migration file in our repository:

Now let's add a new migration:

Commit and push the changes to Azure Repos.

Create a pull request in Azure DevOps. This will automatically trigger the pipeline due to the branch policies you configured.

Check the lint report. Follow any instructions to fix the issues.

Complete the pull request to merge into the main branch. This will trigger the migrate push and migrate apply steps.

When the pipeline finishes running, check your database to see if the changes were applied.

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

## Provisioning schemas (named databases) with Terraform using Atlas

**URL:** https://atlasgo.io/guides/terraform/named-databases

**Contents:**
- Provisioning schemas (named databases) with Terraform using Atlas
  - See it in action​
  - Wrapping up​

Terraform is an Infrastructure as Code (IaC) tool that allows teams to automate and manage their infrastructure through code. It streamlines the process of provisioning, updating, and maintaining infrastructure resources while reducing human error.

Many teams rely on managed SQL databases, such as Amazon RDS on AWS or Cloud SQL on GCP, and use the relevant Terraform provider (AWS, GCP) to provision these databases. For example:

When preparing the infrastructure for the deployment of applications, IaC need to ensure the required schemas (named databases) exist on the database instance in which tables and other database resources will be created.

This can be done manually by connecting to the database instance and running a command such as:

Such manual interactions with infrastructure is undesired in the context of IaC pipelines which aim to eliminate all manual provisioning steps and replace them with automation.

To achieve the same goal, Terraform users may use the Atlas Terraform Provider which allows teams to provision database resources as part of their IaC pipelines. Let's see how.

Start by adding the Atlas provider as a dependency of your Terraform project:

When storing schema definitions, many database engines perform some form of normalization. Meaning, despite us providing a specific definition of some aspect of the schema, the database will store it in another, equivalent form. Therefore, in certain situations it may appear to Atlas as if some diff exists between the desired and inspected schemas, whereas in reality there is none.

To overcome these situations, we use the atlas_schema data source to provide Atlas with a connection string to a Dev-Database. This database is used to normalize the schema prior to planning migrations and for simulating changes to ensure their applicability before execution.

Before running terraform apply for this project, make sure you have a locally running, empty database. You can use Docker to spin one up:

Next, normalize the schema definition containing three schemas: users, products and admin:

The src attribute defines the desired schema we wish to apply to our target database. Next let's see how we can apply this schema to our target database:

Let's unpack what's going on here:

Since we added a new provider to our project, let's first re-initialize the project:

Finally, let's run apply:

We type yes to apply our plan:

Let's re-run apply, to make sure everything is in order:

Great! Everything is in sync.

In this guide, we demonstrated how to use Terraform and the Atlas Terraform Provider to provision empty schemas (named databases) in existing DB instances as part of your Infrastructure-as-Code pipelines.

Have questions? Feedback? Find our team on our Discord server.

**Examples:**

Example 1 (unknown):
```unknown
resource "aws_db_instance" "default" {  allocated_storage    = 10  db_name              = "mydb"  engine               = "mysql"  engine_version       = "8.0"  instance_class       = "db.t3.micro"  username             = "foo"  password             = "foobarbaz"  parameter_group_name = "default.mysql8.0"  skip_final_snapshot  = true}
```

Example 2 (swift):
```swift
resource "google_sql_database_instance" "main" {  name             = "main-instance"  database_version = "POSTGRES_14"  region           = "us-central1"  settings {    tier = "db-f1-micro"  }}
```

Example 3 (sql):
```sql
CREATE SCHEMA "users";CREATE SCHEMA "products";CREATE SCHEMA "admin";
```

Example 4 (unknown):
```unknown
terraform {  required_providers {    atlas = {      source = "ariga/atlas"      version = "~> 0.4.5"    }  }}
```

---

## Staged Rollout Strategies for Multi-Tenant Schema Migrations

**URL:** https://atlasgo.io/guides/database-per-tenant/rollout

**Contents:**
- Staged Rollout Strategies for Multi-Tenant Schema Migrations
- Overview​
- The deployment Block​
  - Basic Syntax​
  - Connecting to an Environment​
- Group Matching Behavior​
- Group Attributes​
  - match​
  - order_by​
  - parallel​

In the previous sections, we learned how to define target groups and deploy migrations to multiple tenant databases. In this section, we will explore deployment rollout strategies - a powerful feature that gives you fine-grained control over how migrations are applied across your tenant databases.

When deploying schema migrations to multiple tenant databases, you often need more control than simply applying migrations to all targets at once. Common requirements include:

Atlas's deployment block addresses all these needs by organizing targets into groups with configurable execution order, parallelism, and error handling.

The deployment block defines a rollout strategy that can be referenced by one or more environments.

To use a deployment strategy, reference it in your env block using the rollout block:

By default, groups are evaluated in the order they appear in the configuration file. When a target matches multiple groups, the first matching group wins - the target is assigned to it and skipped by subsequent groups. You can override the execution order using the depends_on attribute.

This allows you to define specific groups first (e.g., canary, internal) followed by a catch-all group for remaining targets:

A boolean expression that determines which targets belong to this group. Targets matching multiple groups are assigned to the first matching group by file position.

Controls the execution order of targets within a group. Targets are sorted by this expression in ascending order. You can use a single expression or an array for multi-level sorting.

Maximum number of concurrent migrations within the group. Default is 1 (sequential execution).

Defines behavior when a migration fails within the group:

Deploy to a single canary tenant first, then roll out to everyone else:

Roll out to internal tenants first, then free tier (with high parallelism), then paid customers (more carefully):

**Examples:**

Example 1 (sql):
```sql
deployment "<name>" {  // Variables passed from the env block  variable "<var_name>" {    type    = <type>       // string, bool, number, etc.    default = <value>      // Optional default value  }  // Groups define execution stages  group "<group_name>" {    match      = <expr>                  // Boolean expression to filter targets    order_by   = <expr>                  // Expression to sort targets within group    parallel   = <number>                // Max concurrent executions (default: 1)    on_error   = FAIL | CONTINUE         // Error handling mode    depends_on = [group.<other_group>]   // Groups that must complete first  }}
```

Example 2 (unknown):
```unknown
env "prod" {  for_each = toset(var.tenants)  url      = urlsetpath(var.url, each.value)  rollout {    deployment = deployment.staged    vars = {      name = each.value    }  }}
```

Example 3 (swift):
```swift
deployment "staged" {  variable "name" {    type = string  }  // First: Internal tenants (matched first by position)  group "internal" {    match = startswith(var.name, "internal-")  }  // Second: Canary tenants  group "canary" {    match      = startswith(var.name, "canary-")    parallel   = 10    depends_on = [group.internal]  }  // Last: Catch-all for remaining targets (no match = all unmatched)  group "rest" {    depends_on = [group.canary]  }}
```

Example 4 (unknown):
```unknown
group "internal" {  match = startswith(var.name, "my-company-") || var.name == "internal-test"}
```

---

## Working with template directories

**URL:** https://atlasgo.io/guides/migration-dirs/template-directory

**Contents:**
- Working with template directories
  - Basic Example​
  - Inject Data Variables From Command Line​
  - Read Data Variables From File​
    - Working with JSON​
  - Running migrate diff on template directories​
  - Conclusion​

Atlas supports working with dynamic template-based directories, where their content is computed based on the data variables injected at runtime. These directories adopt the Go-templates format, the very same format used by popular CLIs such as kubectl, docker or helm.

To create a template directory, you first need to create an Atlas configuration file (atlas.hcl) and define the template_dir data source there:

The path defines a path to a local directory, and vars defines a map of variables that will be used to interpolate the templates in the directory.

We start our guide with a simple MySQL-based example where migration files are manually written and the auto-increment initial value is configuration based. Let's run atlas migrate new with the --edit flag and paste the following statement:

After creating our first migration file, the users_initial_id variable should be defined in atlas.hcl. Otherwise, Atlas will fail to interpolate the template.

In order to test our migration directory, we can run atlas migrate apply on a temporary MySQL container that Atlas will spin up and tear down automatically for us:

Variables are not always static, and there are times when we need to inject them from the command line. The Atlas configuration file supports this injection using the --var flag. Let's modify our atlas.hcl file such that the value of the users_initial_id variable isn't statically defined and must be provided by the user executing the CLI:

Trying to execute atlas migrate apply without providing the users_initial_id variable, will result in an error:

Let's run it the right way and provide the variable from the command line:

Let's add a bit more complexity to our example by inserting seed data to the users table. But, to keep our configuration file tidy, we'll keep the seed data in a different file (seed_data.json) and read it from there.

First, we'll create a new migration file by running atlas migrate new seed_users --edit and paste the following statement:

The file above expects a data variable named seed_users of type []string. It then loops over this variable and INSERTs a record into the users table for each JSON line.

For the sake of this example, let's define an example seed_users.json file and update the atlas.hcl file to inject the data variable from its content:

To check that our data interpolation works as expected, let's run atlas migrate apply on a temporary MySQL container that Atlas will spin up and tear down automatically for us:

Most modern SQL databases support JSON casting and extraction, allowing developers to work with JSON data types directly. Atlas extends this capability by providing a convenient way to work with JSON data in migration directories using the jsondecode function, which casts a JSON string into a native object. This is particularly useful when inserting structured JSON data into a table or extracting fields from a JSON array.

For example, if we want to import entire rows from a JSON array, we can use jsondecode to convert the content into an iterable list of objects. First, we modify our seed_users.json file to include more fields and ensure it is a valid JSON array:

Next, we update our atlas.hcl file to read this JSON array and assign it to a local variable:

Finally, we modify the SQL template in our migration file to decode the JSON and insert each user's data:

Note: Ensure that the users table schema defines the name and age columns before running this migration.

When running the atlas migrate diff command on a template directory, we want to ensure that the data variables defined in our atlas.hcl are shared between the desired state (e.g., HCL or SQL schema) and the current state of the migration directory, to get an accurate SQL script that moves our database from its previous state to the new one.

Let's demonstrate this using an HCL schema that describes our desired schema and expects one variable: users_initial_id.

Then, we update our atlas.hcl configuration to inject the data variable to this schema file and then use it as our desired state:

To test that our data interpolation works as expected, let's run atlas migrate diff and ensure the HCL schema and the migration directory are in sync:

Then, let's change our data column to be NOT NULL by updating the schema.hcl file and run atlas migrate diff:

After checking our migration directory, we can see that Atlas has generated a new migration file that modifies the data column to be NOT NULL, while leaving the template files untouched:

In this example, we've seen how to use the template_dir data source to create a migration directory whose content is dynamically computed at runtime, based on the data variables defined in the atlas.hcl file. We've also seen how the data variables can be injected from various sources, such as JSON files or CLI flags. Lastly, we've showed how data variables can be shared between template directories and HCL schemas to ensure commands like atlas migrate diff can be utilized to generate migration plan automatically for us.

Have questions? Feedback? Find our team on our Discord server.

**Examples:**

Example 1 (unknown):
```unknown
data "template_dir" "migrations" {  path = "migrations"  vars = {}}env "dev" {  migration {    dir = data.template_dir.migrations.url  }}
```

Example 2 (sql):
```sql
-- Create "users" table.CREATE TABLE `users` (  `id` bigint NOT NULL AUTO_INCREMENT,  `role` enum('user', 'admin') NOT NULL,  `data` json,  PRIMARY KEY (`id`)) AUTO_INCREMENT={{ .users_initial_id }};
```

Example 3 (unknown):
```unknown
data "template_dir" "migrations" {  path = "migrations"  vars = {    users_initial_id = 1000  }}env "dev" {  dev = "docker://mysql/8/dev"  migration {    dir = data.template_dir.migrations.url  }}
```

Example 4 (shell):
```shell
atlas migrate apply \  --env dev \  --url docker://mysql/8/dev
```

---

## Enforcing Reviewed and Approved Schema Migrations

**URL:** https://atlasgo.io/guides/reviewed-approved-migrations

**Contents:**
- Enforcing Reviewed and Approved Schema Migrations
- Compliance Context​
- The Atlas Migration Lifecycle​
- Step 1: Pull Request Validation and Drift Detection​
- Step 2: Automatic Analysis, Linting, and Policy Enforcement​
  - Migration Linting​
  - Custom Policy Rules​
- Step 3: Continuous Delivery of Approved Migrations​
  - Packaging Verified Artifacts​
- Step 4: Deploying Only Approved Migrations​

In regulated and compliance-driven environments, ensuring that only thoroughly reviewed and approved database changes reach production is critical. Organizations operating under frameworks like SOC 2, ISO/IEC 27002, PCI DSS, or HIPAA are expected to demonstrate that all code changes follow a controlled review process before deployment. This includes database work: schema changes and migration scripts are code that runs in production, and they must be validated, tested, peer reviewed, and formally approved before release.

Atlas, a SOC 2 Type II certified product, provides a comprehensive workflow that enforces these requirements at every stage-from initial development through production deployment. This guide shows how Atlas ensures that no unapproved changes slip through, maintaining security, compliance, and auditability throughout the migration lifecycle.

Multiple compliance frameworks require formal change management for database migrations:

Atlas helps you meet these requirements through automated validation, policy enforcement, and complete audit trails.

Atlas enforces a multi-stage workflow that ensures every migration is validated, reviewed, and approved before reaching production:

When a developer opens a pull request, Atlas inspects the proposed code changes to detect database schema modifications.

Atlas also detects conflicting migrations created by different team members working in parallel, preventing situations where multiple developers create migration files that conflict with each other. This ensures all versions are synchronized and the migration history remains linear, avoiding deployment failures and unexpected behavior.

This workflow automatically validates every proposed code change to the database schema or the migrations directory, posting detailed results directly to the pull request. Developers get immediate feedback on any issues before requesting review.

During the pull request phase, Atlas automatically analyzes and simulates the proposed migrations to catch issues before they occur. It runs built-in linters that flag destructive or backward-incompatible changes, long-locking operations, and potential SQL injection risks.

Atlas includes a set of migration analyzers with dozens of built-in checks that flag risky or non-compliant patterns, including:

In addition to the built-in checks, teams can define custom schema policies to enforce their own standards. Custom rules are written in .rule.hcl files using an HCL-based language with predicate and rule blocks. Common examples include:

Once a pull request passes all automated checks and is approved, the migration is ready to be packaged and stored in Atlas Registry, AWS S3, your codebase, or any other storage. Atlas ensures that only approved migrations reach production through its Schema Registry, the central repository for all verified migration artifacts.

The Atlas Registry provides immutable, schema-aware, versioned storage that guarantees only approved migrations can be deployed. When a migration is packaged and pushed to the Registry, it becomes the single source of truth for that migration version.

Migration Directory created with atlas migrate push

Once a pull request passes all validation checks and is approved, the migration is ready for deployment. When the PR is merged into the main branch, Atlas automatically packages the approved migrations and pushes them to the Atlas Registry, creating an immutable, versioned artifact that becomes the single source of truth for that migration version.

For example, the code below shows how to push approved migrations to the Atlas Registry using GitHub Actions:

This immutable artifact ensures that the exact migration version that passed review is the only one deployable to production, preventing unauthorized changes and preserving a complete audit trail for compliance reporting.

When deploying to production, Atlas verifies that migrations originate from the approved artifact created in earlier steps. This process ensures that only reviewed and approved migrations can be applied to production databases, preserving compliance and blocking unauthorized changes.

Atlas supports multiple deployment methods and storage backends. You can deploy from the Atlas Registry, AWS S3, your SCM system (e.g., Azure Repos or GitHub), or any other supported storage. It integrates seamlessly with popular CI/CD tools and platforms such as GitHub Actions, GitLab CI/CD, Azure DevOps, Kubernetes Operator with Argo CD, Terraform Provider, Helm, and Flux CD.

Example deployment using GitHub Actions:

By referencing atlas://my-app (or your configured storage location) instead of local files, deployments pull migrations directly from verified artifact storage. This ensures immutability and traceability, as only approved migrations can be applied.

Atlas automatically maintains a comprehensive audit trail of every migration applied to your databases. This audit trail is essential for compliance frameworks and provides full traceability - not just for migration authoring and approval workflows, but also for the actual execution of migrations in each environment.

Below, the Deployment Trace view provides a clear, end-to-end record of how a migration progressed through your environments. You can see when and where each version was applied, which databases were affected, and whether all instances completed successfully. Each step is linked to its originating pull request and CI run, giving teams full visibility into who approved, merged, and deployed every change.

To improve visibility and enable real-time monitoring, Atlas supports webhook integrations that notify your team about key CI/CD events. You can configure webhooks to send notifications to Slack or custom endpoints when:

Enforcing reviewed and approved migrations is a cornerstone of compliant database change management. Atlas provides a comprehensive, automated workflow that:

By adopting this workflow, teams can:

**Examples:**

Example 1 (swift):
```swift
predicate "table" "has_primary_key" {  primary_key {    condition = self != null  }}rule "schema" "require-primary-key" {  description = "All tables must have a primary key for data integrity and replication"  table {    assert {      predicate = predicate.table.has_primary_key      message   = "Table ${self.name} must have a primary key"    }  }}
```

Example 2 (yaml):
```yaml
- uses: ariga/atlas-action/migrate/push@v1  if: github.ref == 'refs/heads/main'  with:    dir: 'file://migrations'    dev-url: ${{ secrets.DEV_DATABASE_URL }}    dir-name: 'my-app'
```

Example 3 (yaml):
```yaml
name: Deploy to Productionon:  push:    branches:      - mainjobs:  deploy:    runs-on: ubuntu-latest    environment: production  # Requires approval in GitHub    steps:      - uses: ariga/setup-atlas@v0        with:          cloud-token: ${{ secrets.ATLAS_CLOUD_TOKEN }}      # Apply migrations from the verified registry      - uses: ariga/atlas-action/migrate/apply@v1        with:          dir: 'atlas://my-app'  # References the registry          url: ${{ secrets.PROD_DATABASE_URL }}
```

---

## Testing Database Triggers

**URL:** https://atlasgo.io/guides/testing/triggers

**Contents:**
- Testing Database Triggers
- Triggers​
- Project Setup​
  - Schema File​
  - Config File​
- Writing Tests​
  - Simple Test​
  - Table Driven Test​

Atlas lets you automate and verify the effect of database triggers as part of your tested, versioned schema. Atlas makes it possible to test event-driven business rules, catch bugs before they go live, and keep triggers under safe, team-visible change control together with tables, functions, and other DB logic.

In this guide we will learn how to use Atlas's schema test command to test database triggers.

Database triggers are sets of automated instructions that execute in response to specific events, such as INSERT, UPDATE, or DELETE operations on a table, to enforce business rules or maintain data integrity.

Triggers are currently available only to Atlas Pro users. To use this feature, run:

For this example, let's assume we have the following schema, including a trigger:

In the schema above, the products table stores product details and prices, while the products_audit table logs any changes to product prices. The log_price_changes_trigger activates the log_price_changes function after an update to the price column in the products table, recording the old and new prices along with the timestamp of the change in the products_audit table.

Before we begin testing, create a config file named atlas.hcl.

In this file we will create an environment, specify the source of our schema, and a URL for our dev database.

We will also create a file named schema.test.hcl to write our tests, and add it to the atlas.hcl file in the test block.

Let's start off with a simple test that will:

Run the test by running:

The output should look similar to:

Another alternative is to write a table driven test. This test uses the for_each meta-argument, which accepts a map or a set of values and is used to generate a test case for each item in the set or map.

Following similar logic to the test above, we will execute the following:

Run the test by running:

The output should look similar to:

**Examples:**

Example 1 (unknown):
```unknown
atlas login
```

Example 2 (sql):
```sql
schema "public" {}table "products" {  schema = schema.public  column "id" {    null = false    type = integer  }  column "price" {    null = true    type = numeric  }  primary_key {    columns = [column.id]  }}table "products_audit" {  schema = schema.public  column "product_id" {    null = true    type = integer  }  column "old_price" {    null = true    type = numeric  }  column "new_price" {    null = true    type = numeric  }  column "changed_at" {    null    = true    type    = timestamp    default = sql("CURRENT_TIMESTAMP")  }}function "log_price_changes" {  schema = schema.public  lang   = PLpgSQL  return = trigger  as     = <<-SQL  BEGIN      IF OLD.price IS DISTINCT FROM NEW.price THEN          INSERT INTO products_audit (product_id, old_price, new_price, changed_at)          VALUES (OLD.id, OLD.price, NEW.price, NOW());  END IF;  RETURN NEW;  END;  SQL}trigger "log_price_changes_trigger" {  on = table.products  after {    update = true  }  for  = ROW  when = "(old.price IS DISTINCT FROM new.price)"  execute {    function = function.log_price_changes  }}
```

Example 3 (unknown):
```unknown
env "dev" {  src = "file://schema.hcl"  dev = "docker://postgres/15/dev?search_path=public"  # Test configuration for local development.  test {    schema {      src = ["schema.test.hcl"]    }  }}
```

Example 4 (sql):
```sql
test "schema" "trigger" {  # Seed data  exec {    sql = "INSERT INTO products (id, price) VALUES (1, 15.00), (2, 22.99), (3, 13.50);"  }  # Verify products_audit table empty  exec {    sql = "SELECT COUNT(*) FROM products_audit"    output = "0"  }  exec {    sql = "UPDATE products SET price = 19.99 WHERE id = 1;"  }  exec {    sql = "SELECT product_id, old_price, new_price FROM products_audit"    format = table    output = <<TAB product_id | old_price | new_price------------+-----------+----------- 1          | 15        | 19.99TAB  }}
```

---

## Importing a Goose project to Atlas

**URL:** https://atlasgo.io/guides/migration-tools/goose-import

**Contents:**
- Importing a Goose project to Atlas
- TL;DR​
- Prerequisites​
- Convert the migration files​
- Set the baseline on the target database​
- Wrapping up​

The first step in importing a project to Atlas is to convert the existing migration files from the Goose SQL format to the Atlas format.

To automate this process Atlas supports the atlas migrate import command. To read more about this command, read the docs.

Suppose your migrations are located in a directory named goose and you would like to convert them and store them in a new directory named atlas. For this example, let's assume we have a simple Goose project with only two files:

Observe that a new directory named atlas was created with 3 files:

A few things to note about the new directory:

Like many other database schema management tools, Atlas uses a metadata table on the target database to keep track of which migrations were already applied. In the case where we start using Atlas on an existing database, we must somehow inform Atlas that all migrations up to a certain version were already applied.

To illustrate this, let's try to run Atlas's migrate apply command on a database that is currently managed by Goose using the migration directory that we just converted:

Atlas returns an error:

To fix this, we use the --baseline flag to tell Atlas that the database is already at a certain version:

Atlas reports that there's nothing new to run:

That's better! Next, let's verify that Atlas is aware of what migrations were already applied by using the migrate status command:

Great! We have successfully imported our existing Goose project to Atlas.

In this guide we have demonstrated how to take an existing project that is managed by pressly/goose, a popular schema migration tool to be managed by Atlas.

Have questions? Feedback? Find our team on our Discord server.

**Examples:**

Example 1 (unknown):
```unknown
.├── 20221027094633_init.sql└── 20221027094642_new.sql
```

Example 2 (sql):
```sql
atlas migrate import --from file://goose?format=goose --to file://atlas
```

Example 3 (unknown):
```unknown
.├── 20221027094633_init.sql├── 20221027094642_new.sql└── atlas.sum
```

Example 4 (python):
```python
atlas migrate apply --dir file://atlas --url mysql://root:pass@localhost:3306/dev
```

---

## Deploying schema migrations to Kubernetes with Helm

**URL:** https://atlasgo.io/guides/deploying/helm

**Contents:**
- Deploying schema migrations to Kubernetes with Helm
- Using Helm lifecycle hooks​

This method of running schema migrations is deprecated an no longer recommended.

Please use the Kubernetes Operator to manage schema migrations in Kubernetes.

Helm is a popular package manager for Kubernetes that allows developers to package applications into distributable modules called Charts that can be installed, upgraded, uninstalled, and more against a Kubernetes cluster.

Helm is commonly used by software projects as a means for distributing software in a way that will be simple for developers to manage on their clusters. For example, Bitnami maintains hundreds of charts for easily installing many popular applications, such as MySQL, Apache Kafka and others on Kubernetes.

In addition, many teams (Ariga among them) use Helm as a way to package internal applications for deployment on Kubernetes.

In this guide, we demonstrate how schema migrations can be integrated into Helm charts in such a way that satisfies the principles for deploying schema migrations which we described in the introduction.

Prerequisites to the guide:

To satisfy the principle of having migrations run before the new application version starts, as well as ensure that only one migration job runs concurrently, we use Helm's pre-upgrade hooks feature.

Helm pre-upgrade hooks are chart hooks that:

Executes on an upgrade request after templates are rendered, but before any resources are updated

To use a pre-upgrade hook to run migrations with Atlas as part of our chart definition, we create a template for a Kubernetes Job and annotate it with the relevant Helm hook annotations.

Be sure to pass the following values:

Notice the annotations block at the top of the file. This block contains two important attributes:

**Examples:**

Example 1 (yaml):
```yaml
apiVersion: batch/v1kind: Jobmetadata:  # job name should include a unix timestamp to make sure it's unique  name: "{{ .Release.Name }}-migrate-{{ now | unixEpoch }}"  labels:    helm.sh/chart: "{{ .Chart.Name }}-{{ .Chart.Version }}"  annotations:    "helm.sh/hook": pre-install,pre-upgrade    "helm.sh/hook-delete-policy": before-hook-creation,hook-succeededspec:  template:    metadata:      name: "{{ .Release.Name }}-create-tables"      labels:        app.kubernetes.io/managed-by: {{ .Release.Service | quote }}        app.kubernetes.io/instance: {{ .Release.Name | quote }}        helm.sh/chart: "{{ .Chart.Name }}-{{ .Chart.Version }}"    spec:      restartPolicy: Never      imagePullSecrets:        - name: {{ .Values.imagePullSecret }}      containers:        - name: atlas-migrate          image: "{{ .Values.image.repository }}:{{ .Values.image.tag }}"          args:            - migrate            - apply            - -u            - {{ .Values.dburl }}            - --dir            - file:///src/
```

---

## Modern Database CI/CD with Atlas

**URL:** https://atlasgo.io/guides/modern-database-ci-cd

**Contents:**
- Modern Database CI/CD with Atlas
- Principles​
- Workflow​
  - 1. Create a new branch​
  - 2. Change the desired state of the database​
  - 3. Automatically plan the change​
  - 4. Push your changes to trigger CI​
  - 5. Merge your changes to push the latest revision of the database​
  - 6. Deploy the latest revision of the database​
- Conclusion​

Continuous integration and continuous delivery (CI/CD) are tenets of modern software development. CI/CD enables teams to deliver software faster, with higher quality, and with less risk. However, CI/CD is not just for application code. Teams can also apply these principles to their databases, to extend their benefits to one of the most critical components of their stack.

This document describes the recommended workflow for teams using Atlas to achieve continuous integration and continuous delivery for their databases.

This section follows a single change to your database schema from the time it is planned to the time it is deployed. The purpose of this section is not to provide extensive instructions for how to configure your CI/CD pipeline, but rather to provide a high-level overview of the recommended workflow.

Create a new branch to track a change to the database.

Similar to modern Infrastructure-as-Code tools, Atlas uses a declarative approach to database management. This means that you do not need to write SQL scripts to apply changes to the database. Instead, you simply declare the desired state of the database, and Atlas will automatically generate the SQL scripts required to apply the change.

In Atlas, the desired state of the database can be provided in many forms. For example, you can provide it as a plain SQL file, using Atlas HCL, as a reference to your ORM, or even as a connection to an existing database. For the purposes of this example, we will use a plain SQL file.

Atlas supports many ways of declaring the desired state of the database. Here is a list of resources for you to learn more about them:

Use the Atlas CLI to plan the change. This will generate a plan for how to get from the current state of the database to the desired state of the database.

Atlas will create a new SQL file in the migration directory, which contains the SQL statements required to apply the change to the database.

Atlas automates the planning process by generating SQL scripts that apply the desired changes to the database. To learn more about this process, review the Automatic Migration Planning documentation.

Once you are satisfied with your change and the plan, push your changes to trigger CI:

Your CI pipeline should be configured to run the following steps whenever a new commit is pushed to the branch. Teams commonly configure these steps to run only when a change is made to the desired state of the database or to the migration directory.

This way, whenever a change is made to the desired state of the database, the CI pipeline will automatically simulate and analyze the changes, and verify that they are valid and safe. Atlas will generate a detailed analysis report, an example of which you can see here.

It is possible to push your changes to Atlas Cloud directly with the CLI to your CI pipeline, but official integrations are also available. See the Integrations page for more information.

Once CI is green and the change is approved, the changes should be merged into the main branch. This merge should trigger another workflow, which will push the most recent version of the migration directory to Atlas Cloud. You can think of this step as similar to pushing a Docker image to a container registry when code updates are merged into the main branch.

This is typically done by running the following steps in your workflow:

Once the migration directory is pushed to Atlas Cloud, you can view a visual representation of the database schema and its revision history in the Atlas Cloud UI. You can see an example of this here.

It is possible to use the Atlas CLI directly in your CI pipeline, but official integrations are also available:

Once the latest revision of the database is pushed to Atlas Cloud, it can be deployed to any environment. This is typically done by running the following steps in your workflow:

When you run the atlas migrate apply command, Atlas will connect to the target database, and apply any pending migrations. If there are no pending migrations, Atlas will do nothing. When Atlas finishes running, it will send a report to your Atlas Cloud account, with a summary of the changes that were applied, and any errors that occurred. You can view an example of this report here.

Atlas offers integrations with many modern deployment tools. Here are some popular alternatives:

This document described the recommended workflow for teams using Atlas to achieve continuous integration and continuous delivery (CI/CD) for their databases. As we've demonstrated, this process can generally be broken down into four phases:

By implementing this workflow, teams can achieve the following benefits:

**Examples:**

Example 1 (unknown):
```unknown
git checkout -b add-new-index
```

Example 2 (sql):
```sql
CREATE TABLE users (  id INT AUTO_INCREMENT PRIMARY KEY,  name VARCHAR(255) NOT NULL,  email VARCHAR(255) NOT NULL,  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,+  INDEX idx_users_email (email));
```

Example 3 (unknown):
```unknown
atlas migrate diff --env local add_email_index
```

Example 4 (sql):
```sql
ALTER TABLE `users` ADD INDEX `idx_users_email` (`email`);
```

---

## Deploying schema migrations to Google Cloud SQL using Atlas and GitHub Actions

**URL:** https://atlasgo.io/guides/deploying/cloud-sql-via-github-actions

**Contents:**
- Deploying schema migrations to Google Cloud SQL using Atlas and GitHub Actions
- In this article​
- Overview​
- What is Cloud SQL?​
- What is Cloud SQL Auth Proxy?​
- What is GitHub Actions?​
- Deploying Schema Migrations to Cloud SQL​
  - Prerequisites​
  - Step-by-Step​
    - 1—Authenticate to Google Cloud​

In this guide, we demonstrate how to handle database schema changes when working with Cloud SQL. Within the framework of this topic, we are going to introduce how to set up a GitHub Actions workflow to automatically deploy database schema changes to a Cloud SQL instance. This approach is meant to enhance automation, version control, CI/CD, DevOps practices, and scalability, contributing to more efficient and reliable database management.

Before diving into the practical implementation, let's first look at some of the underlying technologies that we will be working with.

Cloud SQL is a fully-managed database service that makes it easy to set up, maintain, manage, and administer your relational databases in the cloud. With Cloud SQL, you can deploy your databases in a highly available and scalable manner, with automatic failover and load balancing, so that your applications can handle a large number of concurrent requests and traffic spikes. You can also choose from different machine types and storage sizes to meet your specific performance and storage requirements.

The Cloud SQL Auth Proxy is a utility for ensuring simple, secure connections to your Cloud SQL instances. It provides a convenient way to control access to your database using Identity and Access Management (IAM) permissions while ensuring a secure connection to your Cloud SQL instance. Like most proxy tools, it serves as the intermediary authority on connection authorizations. Using the Cloud SQL Auth proxy is the recommended method for connecting to a Cloud SQL instance.

GitHub Actions is a continuous integration and continuous delivery (CI/CD) platform that allows you to automate your build, test, and deployment pipeline. You can create workflows that build and test every pull request to your repository, or deploy merged pull requests to production. GitHub Actions goes beyond just DevOps and lets you run workflows when other events happen in your repository. For example, in this guide, you will run a workflow to automatically deploy migrations to a Cloud SQL database whenever someone pushes changes to the main branch in your repository.

Prerequisites to the guide:

There are two approaches to authenticating with Google Cloud: Authentication via a Google Cloud Service Account Key JSON or authentication via Workload Identity Federation.

Setup Workload Identity Federation Identity federation allows you to grant applications running outside Google Cloud access to Google Cloud resources, without using Service Account Keys. It is recommended over Service Account Keys as it eliminates the maintenance and security burden associated with service account keys and also establishes a trust delegation relationship between a particular GitHub Actions workflow invocation and permissions on Google Cloud.

For authenticating via Workload Identity Federation, you must create and configure a Google Cloud Workload Identity Provider. A Workload Identity Provider is an entity that describes a relationship between Google Cloud and an external identity provider, such as GitHub, AWS, Azure Active Directory, etc.

To create and configure a Workload Identity Provider:

Replace [PROJECT_NAME] with the name of your project, and [SERVICE_ACCOUNT_EMAIL] with the email address of the service account you want to grant access to.

Save this value as an environment variable:

Note that $WORKLOAD_IDENTITY_POOL_ID should be the full Workload Identity Pool resource ID, like:

projects/123456789/locations/global/workloadIdentityPools/my-pool

Use this value as the workload_identity_provider value in your GitHub Actions YAML.

Using the Workload Identity Provider ID and Service Account email, the GitHub Action will mint a GitHub OIDC token and exchange the GitHub token for a Google Cloud access token.

Note: It can take up to 5 minutes from when you configure the Workload Identity Pool mapping until the permissions are available.

The instance connection name is a connection string that identifies a Cloud SQL instance, and you need this string to establish a connection to your database. The format of the connection name is projectID:region:instanceID.

To retrieve the Cloud SQL instance connection name, run the following command:

For example, if your instance name is "my-instance", you can retrieve its connection name using the following command:

Secrets are a way to store sensitive information securely in a repository, such as passwords, API keys, and access tokens. To use secrets in your workflow, you must first create the secret in your repository's settings by following these steps:

Once you have added the secret, you can reference it in your workflow using ${{ secrets.DB_PASSWORD }}. The action will retrieve the actual password value from the secret and use it in the DB_PASSWORD environment variable during the workflow run.

Here is an example GitHub Actions workflow for authenticating to GCP with workload identity federation and deploying migrations to a Cloud SQL MySQL database using Cloud SQL Proxy:

Note that for this workflow to work, you will need to replace the placeholders in the environment variables with your own values. Your migrations directory should be stored in your repository's root directory.

Here's what this workflow does:

To execute this workflow once you commit to the main branch, follow these steps:

Now, whenever you push changes to the main branch, all pending migrations will be executed. You can monitor the progress of the GitHub Action in the "Actions" tab of your repository.

In this guide, you learned how to deploy schema migrations to Cloud SQL using Atlas, while ensuring secure connections via a Cloud SQL Proxy. With this knowledge, you can leverage the power of Atlas and Cloud SQL to manage your database schema changes with ease and confidence.

In addition to the specific steps outlined in this guide, you also gained valuable experience with various concepts and tools that are widely used in database management, such as GitHub Actions, Cloud SQL, Cloud SQL Proxy, and the Google Cloud SDK. We hope that this guide has been helpful in expanding your knowledge and skills.

**Examples:**

Example 1 (bash):
```bash
$ export PROJECT_ID="my-project" # update with your value
```

Example 2 (bash):
```bash
$ gcloud iam service-accounts create "my-service-account" \  --project "${PROJECT_ID}"
```

Example 3 (bash):
```bash
$ gcloud services enable iamcredentials.googleapis.com
```

Example 4 (bash):
```bash
$ gcloud projects add-iam-policy-binding [PROJECT_NAME] \--member serviceAccount:[SERVICE_ACCOUNT_EMAIL] \--role roles/editor
```

---

## Indexes with Included Columns in PostgreSQL

**URL:** https://atlasgo.io/guides/postgres/included-columns

**Contents:**
- Indexes with Included Columns in PostgreSQL
  - Basic PostgreSQL syntax for using INCLUDE clause with an index:​
  - How do they work?​
  - When do we need them?​
  - Advantages of using Indexes with an INCLUDE clause:​
  - Limitation of using Indexes with included columns​
- Managing indexes with included columns is easy with Atlas​
  - Managing Indexes with included columns in Atlas​
- Conclusion​
- Need More Help?​

With PostgreSQL, we can create covering indexes using the INCLUDE clause, which are types of indexes that specify a list of columns to be included in the index as non-key columns. If used correctly, indexes with included columns improve performance and reduce total costs.

In PostgreSQL, a B-Tree index creates a multi-level tree structure where each level can be used as a doubly-linked list of pages. Leaf pages are those at the lowest level of a tree, that point to rows of tables.

With covering indexes, records of the columns mentioned in the INCLUDE clause are included in the leaf pages of the B-Tree as "payload" and are not part of the search key.

Each index is stored separately from the table's main data area, which in PostgreSQL this is known as the table's heap. To learn more about the PostgreSQL B-tree index structure and covering indexes, visit the documentation:

Let's demonstrate an example where an index with an INCLUDE clause may be useful, by contrasting it with a unique index without an INCLUDE clause.

First, create a table with the following command:

Here is how a portion of the table might look like after inserting values:

Now, suppose we want to find the ID of a user by their email address. Let’s check the performance of the query with a WHERE clause without any index, with the following command:

Notice that the total cost is 38.75 units. If we want to use a unique index to accelerate the query, we can create it on the email column with the following command:

Now, let's check the performance of querying data of first and last names based on their email addresses, with the following command:

Notice that the total cost is now 8.29 units. The performance of the query has improved by creating a primary key index on email column, compared to 38.75 units without using any index. The engine still has to fetch the first_name and last_name columns from the table (also known as "heap fetches"). Let's drop the existing index to demonstrate the next section in the article:

Suppose we want to accelerate the same query using the INCLUDE clause. In the following command, we will create an index with an INCLUDE clause that precisely covers first_name and last_name columns which are part of the query for which we are trying to improve performance.

Now, let's check the performance of querying data of first and last names based on their email addresses, with the following command:

Notice that the total cost is now 4.29, which is significantly lower, compared to 8.29 which we got while using a unique index without the INCLUDE clause. We were able to reduce the total cost because the query only scanned the index in order to get the data. As a result, heap fetches is also zero, which means the query does not access any tables to retrieve the records.

You might be wondering why we didn’t just use CREATE INDEX ON bankdb(email,first_name,last_name) instead of using the INCLUDE clause. One of the advantages of using the INCLUDE clause is having fewer levels in a B-tree. All INCLUDE columns are stored in the doubly linked list of the B-tree index.

Managing indexes and database schemas in PostgreSQL can be confusing and error-prone. Atlas is a database schema as code tool which allows us to manage our database using a simple and easy-to-understand declarative syntax (similar to Terraform). We will now learn how to manage indexes with included columns using Atlas.

If you are just getting started, install the latest version of Atlas using the guide to setting up Atlas.

We will first use the atlas schema inspect command to get an HCL representation of the table which we created earlier by using the Atlas CLI:

Now, lets add the following index definition to the file:

Save and apply the schema changes on the database by using the apply command:

Atlas generates the necessary SQL statements to add the new index to the database schema. Press Enter while the Apply option is highlighted to apply the changes:

To verify that our new index was created, open the database command line tool from the previous step and run:

Amazing! Our new index with included columns is now created!

In this section, we learned about PostgreSQL indexes with included columns and how we can easily create them in our database by using Atlas.

Join the Ariga Discord Server for early access to features and the ability to provide exclusive feedback that improves your Database Management Tooling. Sign up to our newsletter to stay up to date about Atlas, our OSS database schema management tool, and our cloud platform Atlas Cloud.

**Examples:**

Example 1 (sql):
```sql
CREATE [UNIQUE] INDEX index_nameON table_name(key_column_list)INCLUDE(included_column_list);
```

Example 2 (sql):
```sql
DROP TABLE IF EXISTS "bankdb";CREATE TABLE "bankdb" (  id SERIAL PRIMARY KEY,  savings varchar(100),  first_name varchar(255),  last_name varchar(255),  email varchar(255),  bank varchar(34));
```

Example 3 (python):
```python
-[ RECORD 1 ]--------------------------------------id         | 1savings    | 28 497first_name | Amenalast_name  | Gardneremail      | a_gardner@aol.edubank       | GE77159307648978112812-[ RECORD 2 ]--------------------------------------id         | 2savings    | 71 279first_name | Joanlast_name  | Kaufmanemail      | k-joan3559@google.coukbank       | DK8023212366607361...-[ RECORD 1499 ]------------------------------------id         | 1499savings    | 4 880first_name | Ramonalast_name  | Wilkinsemail      | r.wilkins@google.netbank       | BA928132235277210873-[ RECORD 1500 ]------------------------------------id         | 1500savings    | 69 873first_name | Imanilast_name  | Nobleemail      | imaninoble@hotmail.netbank       | BG45LBAX41796917951361
```

Example 4 (sql):
```sql
EXPLAIN ANALYZESELECT    first_name,    last_name,    emailFROM    "bankdb"WHERE    email = 'd-abbott3425@google.edu';
```

---

## GitOps for Database Schema Management with Argo CD and Atlas Kubernetes Operator (Versioned)

**URL:** https://atlasgo.io/guides/deploying/k8s-argo

**Contents:**
- GitOps for Database Schema Management with Argo CD and Atlas Kubernetes Operator (Versioned)
- Pre-requisites​
- High-level architecture​
- How should you run schema changes in an Argo CD deployment?​
- Installation​
  - 1. Install Argo CD​
  - 2. Install the Atlas Operator​
- Define the application manifests​
  - 1. Set up a Git repo​
  - 2. Create Atlas Cloud token secret​

GitOps is a software development and deployment methodology that uses Git as the central repository for both code and infrastructure configurations, enabling automated and auditable deployments.

Argo CD is a Kubernetes-native continuous delivery tool that implements GitOps principles. It uses a declarative approach to deploy applications to Kubernetes, ensuring that the desired state of the application is always maintained.

Kubernetes Operators are software extensions to Kubernetes that enable the automation and management of complex, application-specific operational tasks and domain-specific knowledge within a Kubernetes cluster.

In this guide, we will demonstrate how to use the Atlas Kubernetes Operator and Argo CD to achieve a GitOps-based deployment workflow for your database schema.

This guide demonstrates the versioned migration workflow using Atlas. If you prefer a declarative approach, check out the declarative workflow guide.

Before we dive into the details of the deployment flow, let's take a look at the high-level architecture of our application.

On a high level, our application consists of the following components:

In our application architecture, we have a database that is connected to our application and managed using an Atlas CR (Custom Resource). The database plays a crucial role in storing and retrieving data for the application, while the Atlas CR provides seamless integration and management of the database schema within our Kubernetes environment.

Integrating GitOps practices with a database in our application stack poses a unique challenge.

Argo CD provides a declarative approach to GitOps, allowing us to define an Argo CD application and seamlessly handle the synchronization process. By pushing changes to the database schema or application code to the Git repository, Argo CD automatically syncs those changes to the Kubernetes cluster.

However, as we discussed in the introduction, ensuring the proper order of deployments is critical. In our scenario, the database deployment must succeed before rolling out the application to ensure its functionality. If the database deployment encounters an issue, it is essential to address it before proceeding with the application deployment.

Argo CD provides Sync Waves and Sync Hooks as features that help to control the order in which manifests are applied within an application. Users may add an annotation to each resource to specify in which "wave" it should be applied. Argo CD will then apply the resources in the order of the waves.

By using annotations with specific order numbers, you can determine the sequence of manifest applications. Lower numbers indicate the earlier application and negative numbers are also allowed.

To ensure that database resources are created and applied before our application, we will utilize Argo CD Sync Waves. The diagram shows our application deployment order:

To achieve the above order, we'll annotate each resource with a sync wave annotation order number:

For more information refer to the official documentation.

With the theoretical background out of the way, let’s take a look at a practical example of how to deploy an application with Argo CD and the Atlas Operator.

To install Argo CD run the following commands:

Wait until all the pods in the argocd namespace are running:

For more information or if you run into some error refer to the Argo CD Documentation.

Helm will print something like this:

Wait until the atlas-operator pod is running:

kubectl will print something like this:

For more information on the installation process, refer to the Atlas Operator Documentation.

Argo CD works by tracking changes to a Git repository and applying them to the cluster, so let's set up a Git repository to serve as the central storage for all your application configuration.

Create a Kubernetes secret to store your Atlas Cloud API token.

Recall that in our first sync-wave, we want to deploy the database resources to our cluster. For the purposes of this example we're deploying a simple MySQL pod to our cluster, but in a realistic scenario, you will probably want to use a managed database service such as AWS RDS, GCP Cloud SQL, or one of the available database operators for Kubernetes.

In your repository, create a new directory named manifests and under it create a new file named db.yaml:

Create the AtlasMigration custom resource to define the desired schema for your database, refer to the Atlas Operator documentation, and determine the specifications, such as the desired database schema, configuration options, and additional parameters

Update the name and tag fields in the dir.remote section to match your migration directory name and the desired version tag in the Atlas Schema Registry.

For the purpose of this guide, we will deploy a simple NGINX server to act as a placeholder for a real backend server. Notice that we annotate the backend deployment with a sync wave order number of 2. This informs Argo CD to deploy the backend application after the Atlas CR is deployed and confirmed to be in healthy.

To decide whether a SyncWave is complete and the next SyncWave can be started, Argo CD performs a health check on the resources in the current SyncWave. If the health check fails, Argo CD will not proceed with the next SyncWave.

Argo CD has built-in health assessment for standard Kubernetes types, such as Deployment and ReplicaSet, but it does not have a built-in health check for custom resources such as AtlasMigration.

To bridge this gap, Argo CD supports custom health checks written in Lua, allowing us to define our custom health assessment logic for the Atlas custom resource.

To define the custom logic for the Atlas object in Argo CD, we can add the custom health check configuration to the argocd-cm ConfigMap. This ConfigMap is a global configuration for Argo CD that should be placed in the same namespace as the rest of the Argo CD resources. Below is a custom health check for the Atlas object:

Finally, create an Argo CD application.yaml file which defines our Argo application:

Make sure all of these files are pushed to your Git repository. If you want to follow along, you can use the example repository for this guide.

Before deploying our application, we need to apply the custom health check configuration to the Argo CD ConfigMap.

With the custom health check in place, we can now deploy our application.

Once you create an Argo CD application, Argo automatically pulls the configuration files from your Git repository and applies them to your Kubernetes cluster. As a result, the corresponding resources are created based on the manifests. This streamlined process ensures that the desired state of your application is synchronized with the actual state in the cluster.

To verify the application is successfully deployed and the resources are healthy:

kubectl will print something like this:

To view your application in the Argo CD UI, you first need to access it.

First, expose the Argo CD server using port-forwarding:

Next, retrieve the initial admin password:

Now you can access the Argo CD UI by navigating to https://localhost:8080 in your browser. Login with:

You may need to accept the self-signed certificate warning in your browser.

Finally, we can view the health, dependency, status of all the resources on the Argo CD UI:

And on Atlas Cloud, you should see that the migrations were applied successfully:

To complete the GitOps workflow, you need to connect your CI pipeline to your Git repository. This way, whenever you push changes to your migration directory, your CI pipeline will automatically update the migration directory in the Atlas Schema Registry and commit the updated tag reference to your Git repository.

After atlas migrate push runs in your CI pipeline, add a step that commits and pushes the updated tag in your migration.yaml manifest back to your Git repository. This ensures that Argo CD will detect the change and deploy the new migration version.

This workflow ensures that:

In this guide, we demonstrated how to use Argo CD to deploy an application that uses the Atlas Operator to manage the lifecycle of the database schema. We also showed how to use Argo CD's custom health check to ensure that the schema changes were successfully applied before deploying the backend application.

Using the techniques described in this guide, you can now integrate schema management into your CI/CD pipeline and ensure that your database schema is always in sync with your application code.

**Examples:**

Example 1 (yaml):
```yaml
metadata:  annotations:    argocd.argoproj.io/sync-wave: "<order-number>"
```

Example 2 (bash):
```bash
kubectl create namespace argocdkubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
```

Example 3 (bash):
```bash
kubectl wait --for=condition=ready pod --all -n argocd
```

Example 4 (bash):
```bash
helm install atlas-operator oci://ghcr.io/ariga/charts/atlas-operator
```

---

## Deploying Schema Migrations

**URL:** https://atlasgo.io/guides/deploying/intro

**Contents:**
- Deploying Schema Migrations
- Schema changes as Deployments​
  - Running migrations on server initialization​
  - Running migrations as part of deployment pipelines​

Changes to database schemas rarely happen in isolation. Most commonly, changes to the database schema are related to some change in the application code. Because incompatibility between the database schema and the application can cause serious problems, it is advised to give careful thought to how these changes are rolled out.

Based on our experience, we have come to the conclusion that changes to the database schema should be thought of as part of the deployment sequence, alongside changing the application version, provisioning infrastructure or applying configuration changes.

This guide describes some strategies teams can employ to incorporate schema changes into their deployment sequence.

In many cases, we have seen teams that run schema migration logic as part of the application code: when servers start, before listening for traffic, code that ensures that the database schema is up-to-date is invoked. This is especially common for teams using ORMs that support an "auto-migration" flow.

In our experience, this strategy may work for simple use-cases, but may cause issues in larger, more established projects. Some downsides of running migrations on boot are:

Instead of running migrations on server init, we suggest using a deployment strategy that follows these principles:

---

## Index operator classes in PostgreSQL

**URL:** https://atlasgo.io/guides/postgres/index-operator-classes

**Contents:**
- Index operator classes in PostgreSQL
  - What is an operator class?​
  - Syntax​
  - When do we need operator classes?​
  - Example:​
  - Managing indexes with operator classes is easy with Atlas​
    - Managing Operator Classes with Atlas​
  - Wrapping up​
- Need More Help?​​

An operator class identifies the operators to be used by the index for the indexed column. Operator classes can be specified for each column of an index in an index definition.

Here is how you can specify an operator class for a column in an index definition:

The main reason for having operator classes is that for some data types, there could be more than one meaningful index behavior. The operator class determines the basic sort ordering. In most cases, the default operator class is usually sufficient. Let’s see it in action.

Let’s create a table which represents data of an ISP’s subscribers along with their email addresses and outstanding payments with the following command:

Here is how a portion of the table might look like after inserting values:

We do not have any indexes other than the primary index on the id column.

Now, let’s assume that we are not aware of the usage of operator classes in indexes just yet. We want to accelerate queries involving patterns matching expressions with a LIKE operator in order to search a name in the subscriber_name column. In this case, we would create an index on the column subscriber_name with the following command:

Awesome! Our index is now created on the subscriber_name column. Now, suppose that we want to search for a subscriber whose registered name begins with “Shirley C”. We can create such a query with the use of a WHERE clause and a LIKE operator. Let’s check the performance and plan of this query with the following command:

The EXPLAIN command is used for understanding the performance of a query. You can learn more about usage of the EXPLAIN command with the ANALYZE option here.

Notice that the internet_provider_idx index that we created was not used in order to execute this query. Instead, the Parallel Seq Scan operation was performed. As a result, the total execution time and cost are still too high.

In a parallel sequential scan, the table's blocks will be divided into ranges and shared among the cooperating processes. Each worker process will complete the scanning of its given range of blocks before requesting an additional range of blocks. To learn more about Parallel Plans in PostgreSQL, visit the official documentation here.

Now, you might be wondering why the index that we created was not being used in the execution of this query. This is when having knowledge about the usage of operator classes becomes important.

As mentioned earlier, an operator class identifies the operators to be used by the index for the indexed column. Let’s see this in action by specifying an operator class in our definition with the following commands:

This time, we specified an operator class varchar_pattern_ops in our index definition. varchar_pattern_ops is a built-in operator class which supports B-tree indexes on the data-type varchar. Let’s check the performance and plan of the query we previously used with the following command:

Amazing! This time, Index Scan was performed using internet_provider_idx. As a result, the cost, planning time, and execution time for our query have reduced significantly, as we expected.

The previous index (without a specified operator class) could have been helpful while executing queries with WHERE clauses with operators such as <, <=, >, or >=. Though, the same index could not be utilized when executing queries with WHERE clauses with a LIKE operator.

In our example, we saw that in some data types, there could be more than one meaningful index behavior, and we need to specify an operator class in the index definition to accelerate certain queries. An operator class is actually just a subset of a larger structure called an “operator family”. To learn more about Operator Classes and Operator Families, visit the official documentation here.

Atlas is an open-source project which allows us to manage our database using a simple and easy-to-understand declarative syntax (similar to Terraform).

If you are just getting started, install the latest version of Atlas using the guide to setting up Atlas.

We will first use the atlas schema inspect command to get an HCL representation of the table we created earlier (without any indexes other than primary index on id column) by using the Atlas CLI:

Now, let's add the following index definition to the file:

Save and apply the schema changes on the database by using the apply command:

Atlas generates the necessary SQL statements to add the new index to the database schema. Press Enter while the Apply option is highlighted to apply the changes:

To verify that our new index was created, open the database command line tool from the previous step and run:

Amazing! Our new index internet_provider_idx with operator class varchar_pattern_ops on subscriber_name column is now created!

In this guide, we demonstrated how using indexes with an appropriate operator class becomes a very crucial skill in optimizing query performance with combinations of certain clauses and operators.

Join the Ariga Discord Server for early access to features and the ability to provide exclusive feedback that improves your Database Management Tooling.

Sign up to our newsletter to stay up to date about Atlas, our OSS database schema management tool, and our cloud platform Atlas Cloud.

**Examples:**

Example 1 (sql):
```sql
CREATE INDEX    nameON    table (column opclass [ ( opclass_options ) ] [sort options] [, ...]);
```

Example 2 (sql):
```sql
CREATE TABLE "internet_provider" (  id SERIAL PRIMARY KEY,  subscriber_name varchar(255),  email_address varchar(255),  payment_pending varchar(100),  active_user varchar(255));
```

Example 3 (sql):
```sql
SELECT        *FROM        internet_provider
```

Example 4 (python):
```python
id | subscriber_name  |      email_address      | payment_pending | active_user----+------------------+-------------------------+-----------------+-------------  0 | Abel Warren      | havb@example.com        | 730             | false  1 | Erick Valentine  | riuee@example.com       | 70              | false  2 | Janice Payne     | dvtub193@example.com    | 67              | false  3 | Gretchen Mason   | tmug.xfhq@example.com   | 767             | false  4 | Lawanda Noble    | qpoy03@example.com      | 227             | true  5 | Robbie Baird     | wdit@example.com        | 659             | true  6 | Carla Compton    | qacaf.kznyx@example.com | 805             | false  7 | Heath Stafford   | mehs271@example.com     | 29              | false  8 | Kendra Stevenson | jcsvp57@example.com     | 810             | true  9 | Brandie Chase    | abwf.dape@example.com   | 944             | false...   id   | subscriber_name  |      email_address      | payment_pending | active_user--------+------------------+-------------------------+-----------------+------------- 999999 | James Strong     | jxgi3@example.com       | 788             | true 999998 | Virginia Ballard | rkdzo0@example.com      | 598             | false 999997 | Shirley Bright   | wawuh02@example.com     | 619             | false 999996 | Vicky Hull       | wobm.fcwsdq@example.com | 390             | false 999995 | Juan Pittman     | tmuq.pyno@example.com   | 263             | false 999994 | Gordon Hawkins   | litvbi.nral@example.com | 605             | true 999993 | Demond Bright    | byvd41@example.com      | 221             | false 999992 | Tara Lowe        | eiyul4@example.com      | 871             | false 999991 | Kenny Daniel     | rbqt328@example.com     | 580             | true 999990 | Alexandra Frank  | gfkw8@example.com       | 890             | true(1000000 rows)
```

---

## Optimal data alignment in tables (PG110)

**URL:** https://atlasgo.io/guides/postgres/pg-110

**Contents:**
- Optimal data alignment in tables (PG110)
  - Alignment and Padding in PostgreSQL​
  - Save up on precious space with optimal data alignment​
  - Example​
- Determining optimal data alignment for a table is easy with Atlas CI​
  - Conclusion​
- Need More Help?​​

When creating a new table, columns of different data types take up different amounts of disk space. The order in which the columns are written determines the amount of space that is used by the rows in the table. Postgres may add padding to columns with smaller sizes to fulfill alignment requirements of the data type of the consecutive column with a larger size.

For example, let’s consider a table with four smallint and one bigint type columns. When a column with a smaller size, such as a smallint (2 bytes), has a consecutive column with a larger size, such as bigint (8 bytes), Postgres adds 6 bytes of padding to the column of type smallint in order to fulfill an alignment requirement of 8 bytes for the consecutive bigint column. However, the space used in padding (6 bytes) can be utilized by rearranging the three other smallint type columns from the table before the bigint type column:

The catalog pg_type stores information about alignment requirements for various data types. You can access the typealign column of this catalog table in order to determine alignment requirements for data types. To learn more about the catalog pg_type and interpretation of the typealign column, visit the official documentation here.

Creating a table with optimal data alignment can help minimize the amount of required disk space. This document describes how we can save space in a database just by changing the order of columns. Let’s see it in action.

Consider the following table on a 64-bit system.

Here is what a portion of the table might look like after inserting values:

Each tuple in the table takes up 24 bytes of total memory without the header. The user_id occupies the first 8 bytes.

Here, the active_status column is of type boolean and takes up only one byte. However, because the next consecutive column data_balance is an integer with size of 4 bytes, PostgreSQL automatically adds 3 bytes of padding to active_status so its size can match with the 4 bytes size of the consecutive data_balance column.

The second 8 bytes of the row are occupied by 1 byte of active_status, 3 bytes of padding, and then 4 bytes of data_balance.

Lastly, the plan_period column has a size of only 2 bytes. However, PostgreSQL adds 6 bytes of padding in order to complete the 8 bytes for the end of the row. The following table displays the data:

Now, let’s see how much space the table takes with the following command:

Our table occupies 100 MB of space. Let’s see how we can optimize the occupied space by rearranging the columns.

Let’s create the same table with the rearranged rows as follows:

Here is what a portion of the table might look like after inserting values:

Now, let’s see how much space the table takes with the following command:

Awesome! We have saved almost 16 MB of space (which is also 16% in our example), just by changing the order of the columns.

Let’s understand how that happened:

The user_id occupies the first 8 bytes. Next, data_balance is an integer that takes up 4 bytes, followed by the plan_period column which has a size of only 2 bytes, followed by 1 byte of active_status and then 1 byte of padding for the end of the row.

In this case, each tuple in the table takes 16 bytes of total memory without the header, and only 1 byte of padding is used, in contrast to 24 bytes of total memory with 9 bytes of total padding involved in our previous example. Here is the data:

As we have observed in the previous section, creating a table with non-optimal data alignment can cost more space, and thus more money. At the same time, calculating the disk space and determining the best arrangement of columns manually can be confusing and error-prone.

With the help of Atlas CI, you can now easily check whether your table alignment is optimal. If the alignment is not optimal, Atlas "CI for databases" will suggest the best possible order of columns to make the alignment optimal and thus help you save maximum space (and money!).

Teams using GitHub that wish to ensure all changes to their database schema are safe can use the Atlas GitHub Action. If you’re just getting started, you can visit the documentation to set-up Atlas CI GitHub action

Let’s create a migration file in Atlas format with the following SQL command:

Once the Atlas CI check is completed, you should see the following code suggestion in your pull request:

Awesome! The Atlas CI check has analyzed the migration file and suggested the best possible arrangement of columns in order to optimize the space taken by padding per row.

Atlas CI provides different Analyzer implementations that are useful for determining the safety of migration scripts. To learn more about other checks currently supported by Atlas CI, visit the documentation about analyzers here.

In this section, we learned about how we can reduce disk space costs without removing any data, just by arranging the table columns in an efficient order to reduce padding space.

Additionally, we have also learned how using Atlas CI can help us determine the best optimal order of columns in a table, removing the hassle of manually calculating the disk cost before and after rearranging columns.

Join the Ariga Discord Server for early access to features and the ability to provide exclusive feedback that improves your Database Management Tooling.

Sign up to our newsletter to stay up to date about Atlas, our OSS database schema management tool, and our cloud platform Atlas Cloud.

**Examples:**

Example 1 (sql):
```sql
CREATE TABLE users (    user_id bigint PRIMARY KEY,    active_status boolean,    data_balance integer,    plan_period smallint);
```

Example 2 (sql):
```sql
SELECT    *FROM    users
```

Example 3 (yaml):
```yaml
user_id | active_status | data_balance | plan_period---------+---------------+--------------+-------------       0 | f             |       731147 |         267       1 | t             |       901448 |          26       2 | t             |       496823 |          24       3 | t             |       985877 |         280       4 | f             |       857124 |          83... 1999995 | f             |       993259 |          83 1999996 | f             |       926033 |         332 1999997 | f             |       889133 |         280 1999998 | t             |       943793 |           7 1999999 | t             |       550192 |         146
```

Example 4 (sql):
```sql
SELECT pg_size_pretty(pg_relation_size('users'));
```

---

## Partial Indexes in SQLite

**URL:** https://atlasgo.io/guides/sqlite/partial-indexes

**Contents:**
- Partial Indexes in SQLite
  - Overview of Partial Indexes​
    - What are Partial Indexes?​
    - Why do we need them?​
    - Advantages of using Partial Indexes​
    - Basic SQLite syntax for using Partial Indexes​
    - Example of Non-partial Indexes vs Partial Indexes in SQLite​
  - Managing Partial Indexes is easy with Atlas​
    - Managing Partial Indexes in Atlas​
  - Limitation of using Partial Indexes​

With SQLite, users may create partial indexes, which are types of indexes that exist on a subset of a table, rather than the entire table itself. If used correctly, partial indexes improve performance and reduce costs, all while minimizing the amount of storage space they take up on the disk.

Let's demonstrate a case where partial indexes may be useful by contrasting them with a non-partial index. ​​If you have many records in an indexed table, the number of records the index needs to track also grows. If the index grows in size, the disk space needed to store the index itself increases as well. In many tables, different records are not accessed with uniform frequency. A subset of a table's records might not be searched very frequently or not searched at all. Records take up precious space in your index whether they are queried or not, and are updated when a new entry is added to the field.

Partial indexes come into the picture to filter unsearched values and give you, as an engineer, a tool to index only what's important.

Let's see this in action by creating a table with the following command:

Here is how a portion of the table might look like after inserting values:

You can also beautify tables in SQLite like shown above, by using the command .mode table

In the following example, suppose we want a list of doctors from India that have taken the vaccine. If we want to use a non-partial index, we can create it on the "vaccinated" column with the following command:

Now, let's check the size of the index that we created, with the following command:

Notice that the total size of our index vaccinated_idx is 6492160 bytes (~6 MB).

The DBSTAT virtual table is a read-only eponymous virtual table that returns information about the amount of disk space used to store the content of an SQLite database. To know more about DBSTAT, visit the official documentation page here

Now, suppose we want to accelerate the same query using the partial index. Let's begin by dropping the existing index that we created earlier:

In the following command, we will create an index with a WHERE clause that precisely describes the list of doctors from India that have taken the vaccine.

Let’s verify if the index we created is being used in the query with a WHERE clause by running the following command:

We confirmed that the index vaccinated_idx is being used while running the query above. Let's check the size of the index that we created again, with the following command:

(Note: The results will vary, ​​depending on the data that is stored in the database)

Notice that the total size of our index vaccinated_idx is just 4096 bytes. In our example, the index size for the partial index took significantly less space (4 KB) compared to the non-partial index that we created earlier on the 'vaccinated' column (~6 MB).

Learn more about partial indexes in SQLite from official documentation here

We have seen that creating a partial index is a better choice where only a small subset of the values stored in the database are accessed frequently. Now, let's see how we can easily manage partial indexes using Atlas.

Managing partial indexes and database schemas in SQLite can be confusing and error-prone. Atlas is an open-source project which allows us to manage our database using a simple and easy-to-understand declarative syntax (similar to Terraform). We will now learn how to manage partial indexes using Atlas.

If you are just getting started, install the latest version of Atlas using the guide to setting up Atlas.

We will first use the atlas schema inspect command to get an HCL representation of the table which we created earlier by using the Atlas CLI:

Now, lets add the following index definition to the file:

Save the changes in the schema.hcl file and apply the changes on the database by using the following command:

Atlas generates the necessary SQL statements to add the new partial index to the database schema. Press Enter while the Apply option is highlighted to apply the changes:

To verify that our new index was created, open the database command line tool and run:

Amazing! Our new partial index is now created!

Partial indexes are useful in cases where we know ahead of time that a table is most frequently queried with a certain WHERE clause. As applications evolve, access patterns to the database also change. Consequently, we may find ourselves in a situation where our index no longer covers many queries, causing them to become resource-consuming and slow.

In this section, we learned about SQLite partial indexes and how we can easily create partial indexes in our database by using Atlas.

Join the Ariga Discord Server for early access to features and the ability to provide exclusive feedback that improves your Database Management Tooling.

Sign up to our newsletter to stay up to date about Atlas, our OSS database schema management tool, and our cloud platform Atlas Cloud.

**Examples:**

Example 1 (sql):
```sql
CREATE INDEX    index_nameON    table_name(column_list)WHERE    expression;
```

Example 2 (sql):
```sql
CREATE TABLE vaccination_data (  id INTEGER NOT NULL,  country varchar(100) default NULL,  title TEXT default NULL,  names varchar(255) default NULL,  vaccinated varchar(255) default NULL,  PRIMARY KEY (id));
```

Example 3 (sql):
```sql
SELECT * FROM vaccination_data;
```

Example 4 (yaml):
```yaml
+----+--------------------+-------+----------------+------------+| id |      country       | title |     names      | vaccinated |+----+--------------------+-------+----------------+------------+| 1  | Poland             | Er.   | Travis Freeman | No         || 2  | Australia          | Mr.   | Hu Dodson      | No         || 3  | Vietnam            | Ms.   | Amery Herman   | No         || 4  | Peru               | Mr.   | Brynne Mann    | Yes        || 5  | Chile              | Er.   | Nora Mitchell  | No         || 6  | Brazil             | Er.   | Tanner Oneal   | No         || 7  | Vietnam            | Mr.   | Ora Conway     | Yes        || 8  | United Kingdom     | Er.   | Quinn Waters   | No         || 9  | Russian Federation | Er.   | Xyla Holloway  | No         || 10 | Norway             | Mr.   | Macy Sullivan  | No         |...| 576000 | Ukraine   | Dr.   | Kuame Gay         | Yes        |+--------+-----------+-------+-------------------+------------+
```

---

## Testing Stored Procedures

**URL:** https://atlasgo.io/guides/testing/procedures

**Contents:**
- Testing Stored Procedures
- Stored Procedures​
- Project Setup​
  - Schema File​
  - Config File​
- Writing Tests​
  - Simple Test​
  - Table Driven Test​

Testing your database schema and migrations is crucial to ensure code behaves as expected, catch bugs early, and prevent regressions. Databases enforce logic, constraints, and complex relationships, so testing ensures these elements work correctly and remain intact after changes.

In this guide we will learn how to use Atlas's schema test command to test database stored procedures.

Stored procedures are sets of precompiled queries grouped together to perform specific tasks and are stored directly on the database.

Stored procedures are currently available only to Atlas Pro users. To use this feature, run:

For this example, let's assume we have the following schema, including a stored procedure:

In the schema above we have a sales table, an archive_sales table and an archive_old_sales procedure. The procedure moves old sales from the sales table to the archive_sales table based on a cutoff date that is given when calling the procedure.

Before we begin testing, create a config file named atlas.hcl.

In this file we will create an environment, specify the source of our schema, and a URL for our dev database.

We will also create a file named schema.test.hcl to write our tests, and add it to the atlas.hcl file in the test block.

Let's start off with a simple test that will:

Run the test by running:

The output should look similar to:

Another alternative is to write a table driven test. This test uses the for_each meta-argument, which accepts a map or a set of values and is used to generate a test case for each item in the set or map.

Following similar logic to the test above, we will execute the following:

Run the test by running:

The output should look similar to:

**Examples:**

Example 1 (unknown):
```unknown
atlas login
```

Example 2 (sql):
```sql
schema "public" {}table "sales" {  schema = schema.public  column "id" {    type = int  }  column "sale_amount" {    type =  numeric  }  column "sale_date" {    type = date  }}table "archive_sales" {  schema = schema.public  column "id" {    type = int  }  column "sale_amount" {    type = int  }  column "sale_date" {    type = date  }}procedure "archive_old_sales" {  schema = schema.public  lang   = PLpgSQL  arg "cutoff_date" {    type = date  }  as = <<-SQL  BEGIN      -- Insert old sales into archive_sales  INSERT INTO archive_sales (id, sale_amount, sale_date)  SELECT id, sale_amount, sale_date  FROM sales  WHERE sale_date < cutoff_date;  -- Delete old sales from sales  DELETE FROM sales  WHERE sale_date < cutoff_date;  END;  SQL}
```

Example 3 (unknown):
```unknown
env "dev" {  src = "file://schema.hcl"  dev = "docker://postgres/15/dev?search_path=public"  # Test configuration for local development.  test {    schema {      src = ["schema.test.hcl"]    }  }}
```

Example 4 (sql):
```sql
test "schema" "procedure" {  # Seed data  exec {    sql = <<-SQL      INSERT INTO sales (id, sale_amount, sale_date) VALUES      (1, 150.00, '2024-07-18'),      (2, 200.00, '2024-06-20'),      (1, 350.00, '2024-07-10');    SQL  }  # Execute the procedure with a specific cutoff date  exec {    sql = "CALL archive_old_sales('2024-07-18')"  # Archive sales before this date  }  # Verify data in archive_sales table  exec {    sql = "SELECT COUNT(*) FROM archive_sales WHERE sale_date < '2024-07-18'"    output = "2" # Expect 2 archived sales  }  # Verify data in sales table  exec {    sql = "SELECT COUNT(*) FROM sales"    output = "1"  # Expect 1 sale remaining in the sales table after cutoff date  }}
```

---

## Running Atlas in Docker

**URL:** https://atlasgo.io/guides/atlas-in-docker

**Contents:**
- Running Atlas in Docker
- Common Issues​
  - Use 'atlas login' to access this feature​
  - "docker": executable file not found in $PATH​
    - Workaround: Spin up a local database container and use it​

Atlas ships as a set of official Docker Images for you to use.

To run Atlas in Docker, execute:

Depending on your use case, you may want to use a different image type:

Atlas is an open-core project, with some features available only to signed-in users. To use these features, you must sign in to Atlas. To sign in:

Visit the URL in your browser and follow the on-screen instructions.

Copy the code provided by Atlas Cloud:

Paste the code back into the terminal where you ran atlas login and hit <ENTER>:

Atlas will verify your code and provide you with a success message:

You can now use Atlas features that require authentication. Use the -v ~/.atlas:/root/.atlas flag to persist your login credentials across Docker runs. For example:

Atlas heavily relies on the presence of a Dev Database for various calculations and schema normalization. To use a Dev Database, users provide Atlas with the URL to connect to an empty database of the type they wish to operate on.

To streamline work with Dev Databases, Atlas provides a convenience driver named docker://, in which Atlas depends on the Docker CLI command docker to be present in the runtime environment. Running Docker-in-Docker is a notoriously nuanced topic and so we do not ship docker in the distributed Atlas images.

For this reason, Atlas users who wish to run Atlas in Docker, cannot, by default use the docker:// driver.

A common workaround is to spin up a local, empty database container and connect to it.

Note a few things about this command:

**Examples:**

Example 1 (shell):
```shell
docker run --rm -it arigaio/atlas:latest-alpine
```

Example 2 (shell):
```shell
docker run --rm -it \  -v ~/.atlas:/root/.atlas \  arigaio/atlas:latest login
```

Example 3 (typescript):
```typescript
Please visit:https://auth.atlasgo.cloud/login?cli=ade66529-e6c0-4c56-8311-e23d0efe9ee9&port=33281Follow the instructions on screen. (Hit <ENTER> to manually provide the code.)
```

Example 4 (unknown):
```unknown
Please enter the auth code:
```

---

## Automatic SQL Server Schema Migrations with Atlas

**URL:** https://atlasgo.io/guides/mssql

**Contents:**
- Automatic SQL Server Schema Migrations with Atlas
    - Enter: Atlas​
- Prerequisites​
  - MacOS
  - Linux
  - Windows
- Logging in to Atlas​
- Inspecting our Database​
- Declarative Migrations​
- Versioned Migrations​

Microsoft SQL Server is a powerful relational database management system that has one of the prominent enterprise-grade data solutions for decades. Commonly used by enterprises, SQL Server can efficiently handle growing amounts of data and users, making it easy to scale.

However, managing a large database schema in SQL Server can be challenging due to the complexity of related data structures and the need for coordinated schema changes across multiple teams and applications.

Atlas helps developers manage their database schema as code - abstracting away the intricacies of database schema management. With Atlas, users provide the desired state of the database schema and Atlas automatically plans the required migrations.

In this guide, we will dive into setting up Atlas for SQL Server schema migration, and introduce the different workflows available.

To download and install the latest release of the Atlas CLI, simply run the following in your terminal:

Get the latest release with Homebrew:

To pull the Atlas image and run it as a Docker container:

If the container needs access to the host network or a local directory, use the --net=host flag and mount the desired directory:

Download the latest release and move the atlas binary to a file location on your system PATH.

Use the setup-atlas action to install Atlas in your GitHub Actions workflow:

For other CI/CD platforms, use the installation script. See the CI/CD integrations for more details.

If you want to manually install the Atlas CLI, pick one of the below builds suitable for your system.

To use SQL Server with Atlas, you'll need to log in to Atlas. If it's your first time, you will be prompted to create both an account and a workspace (organization):

Let's start off by spinning up a database using Docker:

For this example we will begin with a minimal database with a users table and an id as the primary key.

To create this on our SQL Server database, run the following command:

The atlas schema inspect command supports reading the database description provided by a URL and outputting it in different formats, including Atlas DDL (default), SQL, and JSON. In this guide, we will demonstrate the flow using both the Atlas DDL and SQL formats, as the JSON format is often used for processing the output using jq.

To inspect our locally-running SQL Server instance, use the -u flag and write the output to a file named schema.hcl:

Open the schema.hcl file to view the Atlas schema that describes our database.

This first block represents a table resource with id, and name columns. The schema field references the dbo schema that is defined in the block below. In addition, the primary_key sub-block defines the id column as the primary key for the table. Atlas strives to mimic the syntax of the database that the user is working against. In this case, the type for the id column is bigint, and varchar(255) for the name column.

To inspect our locally-running SQL Server instance, use the -u flag and write the output to a file named schema.sql:

Open the schema.sql file to view the inspected SQL schema that describes our database.

For in-depth details on the atlas schema inspect command, covering aspects like inspecting specific schemas, handling multiple schemas concurrently, excluding tables, and more, refer to our documentation here.

To generate an Entity Relationship Diagram (ERD), or a visual representation of our schema, we can add the -w flag to the inspect command:

The declarative approach lets users manage schemas by defining the desired state of the database as code. Atlas then inspects the target database and calculates an execution plan to reconcile the difference between the desired and actual states. Let's see this in action.

We will start off by making a change to our schema file, such as adding a repos table:

Now that our desired state has changed, to apply these changes to our database, Atlas will plan a migration for us by running the atlas schema apply command:

Apply the changes, and that's it! You have successfully run a declarative migration.

For a more detailed description of the atlas schema apply command refer to our documentation here.

To ensure that the changes have been made to the schema, let's run the inspect command with the -w flag once more and view the ERD:

Alternatively, the versioned migration workflow, sometimes called "change-based migrations", allows each change to the database schema to be checked-in to source control and reviewed during code-review. Users can still benefit from Atlas intelligently planning migrations for them, however they are not automatically applied.

In the versioned migration workflow, our database state is managed by a migration directory. The migration directory holds all of the migration files created by Atlas, and the sum of all files in lexicographical order represents the current state of the database.

To create our first migration file, we will run the atlas migrate diff command, and we will provide the necessary parameters:

Run ls migrations, and you'll notice that Atlas has automatically created a migration directory for us, as well as two files:

The migration file represents the current state of our database, and the sum file is used by Atlas to maintain the integrity of the migration directory. To learn more about the sum file, read the documentation.

Now that we have our first migration, we can apply it to a database. There are multiple ways to accomplish this, with most methods covered in the guides section. In this example, we'll demonstrate how to push migrations to Atlas Cloud, much like how Docker images are pushed to Docker Hub.

Migration Directory created with atlas migrate push

Let's name our new migration project app and run atlas migrate push:

Once the migration directory is pushed, Atlas prints a URL to the created directory, similar to the once shown in the image above.

Once our app migration directory has been pushed, we can apply it to a database from any CD platform without necessarily having our directory there.

Let's create another database using Docker to resemble a local environment, this time on port 1434:

Next, we'll create a simple Atlas configuration file (atlas.hcl) to store the settings for our local environment:

The final step is to apply the migrations to the database. Let's run atlas migrate apply with the --env flag to instruct Atlas to select the environment configuration from the atlas.hcl file:

Boom! After applying the migration, you should receive a link to the deployment and the database where the migration was applied. Here's an example of what it should look like:

Migration deployment reported created with atlas migrate apply

After applying the first migration, it's time to update our schema defined in the schema file and tell Atlas to generate another migration. This will bring the migration directory (and the database) in line with the new state defined by the desired schema (schema file).

Let's make two changes to our schema:

Next, let's run the atlas migrate diff command once more:

Run ls migrations, and you'll notice that a new migration file has been generated.

Let's run atlas migrate push again and observe the new file on the migration directory page.

Migration Directory created with atlas migrate push

In this guide we learned about the declarative and versioned workflows, and how to use Atlas to generate migrations, push them to an Atlas workspace and apply them to databases.

For more in-depth guides, check out the other pages in this section or visit our Docs section.

Have questions? Feedback? Find our team on our Discord server.

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

## Using Atlas with AI Agents

**URL:** https://atlasgo.io/guides/ai-tools

**Contents:**
- Using Atlas with AI Agents
  - Instruction files for AI agents​
  - Prompt Library​
      - GitHub Copilot Instructions
      - Cursor Instructions
      - Claude Code Instructions
  - Example workflow - generating migrations​
    - 1. Analyze the current schema and make necessary changes.​
    - 2. Generate the necessary migration files.​
    - 3. Apply the migration files to the database.​

AI agents like GitHub Copilot, Cursor, and Claude Code are great at writing code, but generating database migrations is a different challenge. As schemas grow larger and more complex, ensuring migrations are deterministic, predictable, and aligned with company policies becomes critical.

Atlas solves this problem by letting AI tools focus on editing the schema while Atlas provides the infrastructure for:

And more. Atlas offers a complete toolkit for safe, automated, and policy-driven database change management.

AI agents can be configured to adapt their behavior on a project or repository level by providing them with specific instructions or rules. This allows them to better understand the context of the code they are working with and provide more relevant suggestions.

To help your AI agent get the most out of Atlas, we have created a set of instructions and rules that can be used to configure them to work with Atlas. These instructions and rules are designed to help the AI agent understand how and when to use optimally use Atlas.

Configure GitHub Copilot with Atlas-specific instructions.

Set up Cursor with Atlas-specific rules.

Set up Claude Code with Atlas-specific instructions.

The above instructions teach the AI agent to use a specific workflow when generating migrations. When generating migrations, there are several steps that the AI agent should follow:

The AI agent should use atlas migrate diff to generate the migration file. After generating the migration, the AI agent should validate the migration file by running atlas migrate lint and fix any issues that arise.

The last step is applying the migration files to the database using atlas migrate apply. The assistant should first try applying a dry-run.

---

## Using SSL Certs with the Atlas Operator

**URL:** https://atlasgo.io/guides/deploying/k8s-operator-certs

**Contents:**
- Using SSL Certs with the Atlas Operator
- Step 1: Create a Secret for the SSL/TLS Certificates​
- Step 2: Mount the Certificates into the Atlas Operator​
- Step 3: Use the Certificates in the Database URL​

Many modern databases support SSL/TLS encryption for secure communication between clients and the database. In this document we provide some basic guidance on how to use SSL/TLS certificates with the Atlas Operator on Kubernetes.

The first step is to create a Kubernetes Secret that contains the SSL/TLS certificates. If you are using a Kubernetes Operator that supports automatically creating certificates such as the CockroachDB Operator, you can use the certificates created by that Operator.

Here is an example of how to create a Secret with SSL/TLS certificates:

This will create a Secret named my-secret with the SSL/TLS certificates.

The next step is to mount the SSL/TLS certificates into the Atlas Operator. To do this, by create a file named values.yaml with the following content:

Now, install the operator using this values.yaml file:

This will install the Atlas Operator, overriding the extraVolumes and extraVolumeMounts values to mount the SSL/TLS certificates into the Operator.

The final step is to use the SSL/TLS certificates in the database URL. For example, if you are using the PostgreSQL or CockroachDB databases, you can use the following database URL:

To learn more about how to securely provide the database URL to the operator, see the docs.

**Examples:**

Example 1 (shell):
```shell
kubectl create secret generic my-secret \  --from-file=ca.crt=./path/to/ca.crt \  --from-file=tls.key=./path/to/tls.key \  --from-file=tls.crt=./path/to/tls.crt
```

Example 2 (yaml):
```yaml
extraVolumes:   - name: certs     secret:       secretName: my-secret       defaultMode: 0640extraVolumeMounts:   - name: certs     mountPath: /certs     readOnly: true
```

Example 3 (shell):
```shell
helm install atlas-operator oci://ghcr.io/ariga/charts/atlas-operator -f values.yaml
```

Example 4 (shell):
```shell
postgresql://username@hostname:port/database?sslmode=verify-full&sslcert=/certs/tls.crt&sslkey=/certs/tls.key&sslrootcert=/certs/ca.crt
```

---

## Automatic Google Cloud Spanner Schema Migrations with Atlas

**URL:** https://atlasgo.io/guides/spanner/automatic-migrations

**Contents:**
- Automatic Google Cloud Spanner Schema Migrations with Atlas
    - Enter: Atlas​
- Prerequisites​
- Creating a Spanner Instance and Database​
- Inspecting the Schema​
- Declarative Migrations​
  - Applying our schema​
  - Altering our schema​
  - Visualizing our schema​
  - Pushing schemas to Atlas​

Spanner is a fully managed, horizontally scalable, globally distributed, and strongly consistent database service offered by Google Cloud. It is designed to handle large-scale applications with high availability and low latency.

However, managing a large database schema with Spanner can be challenging due to the complexity of related data structures and the need for coordinated schema changes across multiple teams and applications.

Atlas helps developers manage their database schema as code, abstracting away the intricacies of database schema management. With Atlas, users provide the desired state of the database schema and Atlas automatically plans the required migrations.

In this guide, we will dive into setting up Atlas for Spanner schema migrations, and introduce the different workflows available.

To download and install the custom release of the Atlas CLI, simply run the following in your terminal:

To pull the Atlas image and run it as a Docker container:

If the container needs access to the host network or a local directory, use the --net=host flag and mount the desired directory:

Download the custom release and move the atlas binary to a file location on your system PATH.

If you want to use an existing Spanner instance and database, you can skip this step.

Let's start off by spinning up a Spanner instance using the Google Cloud Console or the gcloud command line tool.

Next, create a Spanner database within the instance:

This command creates a new Spanner database named my-database with a users table.

The atlas schema inspect command supports reading the database description provided by a URL and outputting it in different formats, including Atlas DDL (default), SQL, and JSON. In this guide, we will demonstrate the flow using both the Atlas DDL and SQL formats, as the JSON format is often used for processing the output using jq.

To inspect our Spanner database, use the -u flag and write the output to a file named schema.hcl:

Open the schema.hcl file to view the Atlas schema that describes our database.

To inspect our Spanner database, use the -u flag and write the output to a file named schema.sql:

Open the schema.sql file to view the inspected SQL schema that describes our database.

For in-depth details on the atlas schema inspect command, covering aspects like inspecting specific schemas, handling multiple schemas concurrently, excluding tables, and more, refer to our documentation here.

Atlas supports a workflow called declarative schema migrations. In this workflow, you first define the desired state of your database schema (in one of many supported formats and languages). Then, you let Atlas calculate the diff between the desired state and the actual state of your database. Atlas then generates the SQL commands that will bring your database to the desired state.

Let's see this in action.

First, create a new file name schema.sql. This file will contain the desired state of our database in plain SQL.

Next, let's apply this schema to our database using the atlas schema apply command.

If your Spanner database uses the PostgreSQL dialect, use docker://spannerpg/latest as the dev-url:

Atlas automatically detects the dialect of your target database and uses the appropriate syntax.

Atlas will connect to our target database to inspect its current state. Next, it will use the dev-database to normalize our schema and generate the SQL commands that will bring our database to the desired state:

After applying the schema, Atlas confirms that the changes were applied:

Next, let's re-run the atlas schema apply command. This time, Atlas will detect that the database is already in the desired state and will not generate any changes:

Now, let's make some changes to our schema. Open the schema.sql file and add a new column to the users table:

Next, let's re-run the atlas schema apply command. This time, Atlas will detect that the schema has changed and will generate the needed SQL commands to bring the database to the desired state:

After applying the changes, Atlas confirms once again that the changes were applied:

One of the most useful features of Atlas is the ability to visualize your database schema. To do so, run the atlas schema inspect command with the -w (web) flag:

Atlas will ask whether you would like to create your visualization publicly (in a publicly accessible URL) or privately (in your Atlas Cloud account):

For this demo, let's choose the public option. Atlas will create the visualization and open it in your default browser:

See it for yourself at: https://gh.atlasgo.cloud/explore/0256b374

Similar to how Docker images are pushed to Docker Hub, you can push your schema to Atlas Cloud for versioning, collaboration, and deployment:

Once pushed, Atlas prints a URL to the schema. You can then apply it to any database using the schema URL:

This workflow allows you to manage your schema centrally and deploy it to multiple environments without having the schema files locally.

For more advanced workflows, you can use atlas schema plan to pre-plan and review migrations before applying them. This enables teams to plan, lint, and review changes during the PR stage, edit generated SQL if needed, and ensure no human intervention is required during deployment.

Alternatively, the versioned migration workflow, sometimes called "change-based migrations", allows each change to the database schema to be checked-in to source control and reviewed during code-review. Users can still benefit from Atlas intelligently planning migrations for them, however they are not automatically applied.

In the versioned migration workflow, our database state is managed by a migration directory. The migration directory holds all of the migration files created by Atlas, and the sum of all files in lexicographical order represents the current state of the database.

To create our first migration file, we will run the atlas migrate diff command, and we will provide the necessary parameters:

If your Spanner database uses the PostgreSQL dialect, use docker://spannerpg/latest as the dev-url:

Run ls migrations, and you'll notice that Atlas has automatically created a migration directory for us, as well as two files:

The migration file represents the current state of our database, and the sum file is used by Atlas to maintain the integrity of the migration directory. To learn more about the sum file, read the documentation.

Now that we have our first migration, we can apply it to a database. There are multiple ways to accomplish this, with most methods covered in the guides section. In this example, we'll demonstrate how to push migrations to Atlas Cloud, much like how Docker images are pushed to Docker Hub.

Let's name our new migration project app and run atlas migrate push:

Once the migration directory is pushed, Atlas prints a URL to the created directory.

Once our app migration directory has been pushed, we can apply it to a database from any CD platform without necessarily having our directory there.

We'll create a simple Atlas configuration file (atlas.hcl) to store the settings for our environment:

The final step is to apply the migrations to the database. Let's run atlas migrate apply with the --env flag to instruct Atlas to select the environment configuration from the atlas.hcl file:

After applying the migration, you should receive a link to the deployment and the database where the migration was applied.

Once you have your migration directory set up, the next step is to integrate Atlas into your CI/CD pipeline. Atlas provides native integrations for popular platforms:

Set up CI/CD with GitHub Actions

Set up CI/CD with GitLab CI

Set up CI/CD with Bitbucket Pipelines

Set up CI/CD with Azure DevOps

Deploy schema changes with Terraform

Deploy schema changes with Kubernetes

In this guide, we demonstrated how to set up Atlas to manage your Google Cloud Spanner database schema. We covered both declarative and versioned migration workflows, and showed how to generate migrations, push them to an Atlas workspace, and apply them to your databases. Atlas has many more features to explore. To learn more, check out the Atlas documentation.

As always, we would love to hear your feedback and suggestions on our Discord server.

**Examples:**

Example 1 (shell):
```shell
curl -sSf https://atlasgo.sh | ATLAS_FLAVOR="spanner" sh
```

Example 2 (shell):
```shell
docker pull arigaio/atlas-extendeddocker run --rm arigaio/atlas-extended --help
```

Example 3 (shell):
```shell
docker run --rm --net=host \  -v $(pwd)/migrations:/migrations \  arigaio/atlas-extended migrate apply \  --url "mysql://root:pass@:3306/test"
```

Example 4 (shell):
```shell
$ atlas login
```

---

## Automatic Snowflake Schema Migrations with Atlas

**URL:** https://atlasgo.io/guides/snowflake/automatic-migrations

**Contents:**
- Automatic Snowflake Schema Migrations with Atlas
    - Snowflake Beta Feedback Program
    - Enter: Atlas​
- Prerequisites​
  - Installing SnowSQL​
  - Installing Atlas  ​
- Setting Up SnowSQL connection​
- Setting up Environment variables​
- Inspecting the Schema​
- Declarative Migrations​

As with our other beta programs, we're looking for feedback from early adopters. If you're interested in participating:

Snowflake is a cloud-based data warehousing platform that provides a SQL interface for executing queries, along with robust data management capabilities. It offers unique features like separation

of storage and compute, zero-copy cloning, and secure data sharing.

Managing database schemas in Snowflake across different environments can be challenging, especially when coordinating changes across multiple teams and applications. Traditional approaches often involve manual SQL scripts that are difficult to track, test, and roll back.

Atlas helps developers manage their database schema as code, abstracting away the intricacies of database schema management. With Atlas, users provide the desired state of the database schema and Atlas automatically plans the required migrations.

In this guide, we will dive into setting up Atlas for Snowflake schema migration using the declarative workflow.

The SnowSQL provides a convenient way to interact with your Snowflake Platform. Let's install it: see the official SnowSQL documentation.

While we reference SnowSQL in this guide for executing DDL statements, it's not strictly required. You can alternatively use Snowflake's web interface (Worksheets) or any other compatible SQL client to perform the same operations on your Snowflake instance.

To download and install the custom release of the Atlas CLI, simply run the following in your terminal:

To pull the Atlas image and run it as a Docker container:

If the container needs access to the host network or a local directory, use the --net=host flag and mount the desired directory:

Download the custom release and move the atlas binary to a file location on your system PATH.

First, configure and connect to your Snowflake account:

You can also connect to Snowflake using other methods, such as OAuth or SSO. For more information, see the Snowflake documentation.

The results will look like this:

Though out this guide, we will use the following environment variables to simplify our commands:

To get these values, running the following command:

To get account identifier:

To get access token: Navigating to Avatar → Settings → Authentication → Programmatic Access Tokens

To get account identifier:

To get access token: Navigating to Avatar → Settings → Authentication → Programmatic Access Tokens

The atlas schema inspect command supports reading the database description provided by a URL and outputting it in different formats, including Atlas DDL (default), SQL, and JSON. In this guide, we will demonstrate the flow using both the Atlas DDL and SQL formats.

First, create a database, schema, and a users table:

Next, let's inspect the schema of our Snowflake database using the atlas schema inspect command. This command will connect to the database and output its schema in the desired format.

To inspect our Snowflake database, use the -u flag and write the output to a file named schema.hcl:

The -u flag requires a connection URL in the format snowflake://<username>:<password>@<account_identifier>/MY_DATABASE?warehouse=MY_WAREHOUSE. To understand the URL format, refer to our URL documentation.

Open the schema.hcl file to view the Atlas schema that describes our database.

To inspect our Snowflake database, use the -u flag and write the output to a file named schema.sql:

Open the schema.sql file to view the inspected SQL schema that describes our database.

For in-depth details on the atlas schema inspect command, covering aspects like inspecting specific schemas, handling multiple schemas concurrently, excluding tables, and more, refer to our documentation here.

Atlas supports a workflow called declarative schema migrations. In this workflow, you first define the desired state of your database schema (in one of many supported formats and languages). Then, you let Atlas calculate the diff between the desired state and the actual state of your database. Atlas then generates the SQL commands that will bring your database to the desired state.

Let's see this in action.

First create a new database and dev-database in Snowflake:

Second, create the schema.sql. This file will contain the desired state of our database in plain SQL.

Next, let's apply this schema to our database using the atlas schema apply command.

Atlas will connect to our target database to inspect its current state. Next, it will use the dev-database to normalize our schema and generate the SQL commands that will bring our database to the desired state:

After applying the schema, Atlas confirms that the changes were applied:

Next, let's re-run the atlas schema apply command. This time, Atlas will detect that the database is already in the desired state and will not generate any changes:

Now, let's make some changes to our schema. Open the schema.sql file and add a new column to the users table:

Next, let's re-run the atlas schema apply command. This time, Atlas will detect that the schema has changed and will generate the needed SQL commands to bring the database to the desired state:

After applying the changes, Atlas confirms once again that the changes were applied:

One of the most useful features of Atlas is the ability to visualize your database schema. To do so, run the atlas schema inspect command with the -w (web) flag:

Atlas will ask whether you would like to create your visualization publicly (in a publicly accessible URL) or privately (in your Atlas Cloud account):

For this demo, let's choose the public option. Atlas will create the visualization and open it in your default browser.

See it for yourself at: https://gh.atlasgo.cloud/explore/cb1382a3

In addition to the declarative workflow, Atlas also supports versioned migrations, which are useful when you need more control over how schema changes are applied.

First create a new database in Snowflake for this demo:

Then run the following command to create a new migration file:

This will create a new migration file in the migrations directory. Open the file and add the SQL needed to create a comments table:

Now, let's apply this migration to our database:

Atlas will apply the migration and confirm that it was successful:

In this guide we have demonstrated how to set up Atlas to manage your Snowflake database schema. We have shown how to use both declarative and versioned migration workflows to manage your schema changes. These features are just the beginning of what Atlas can do to help you better manage your database!

To learn more about Atlas capabilities, check out the Atlas documentation.

As always, we would love to hear your feedback and suggestions on our Discord server.

**Examples:**

Example 1 (shell):
```shell
curl -sSf https://atlasgo.sh | ATLAS_FLAVOR="snowflake" sh
```

Example 2 (shell):
```shell
docker pull arigaio/atlas-extendeddocker run --rm arigaio/atlas-extended --help
```

Example 3 (shell):
```shell
docker run --rm --net=host \  -v $(pwd)/migrations:/migrations \  arigaio/atlas-extended migrate apply \  --url "mysql://root:pass@:3306/test"
```

Example 4 (json):
```json
[connections.demo]account = "<your_account_identifier>"user = "<your_username>"password = "<your_password>"
```

---

## Testing Postgres Domains

**URL:** https://atlasgo.io/guides/testing/domains

**Contents:**
- Testing Postgres Domains
- Database Domains​
- Project Setup​
  - Schema File​
  - Config File​
- Writing Tests​
  - Simple Test​
  - Table Driven Test​

With Atlas, you can test and validate PostgreSQL domain types and constraints alongside every other schema element. his helps you catch validation issues and data logic bugs before they reach production and ensures that your custom types behave as expected across environments.

In this guide, you’ll learn how to use Atlas's schema test command to test Postgres Domain Types.

A domain is a user-defined data type that is based on an existing data type but with optional constraints and default values.

Domains are currently available only to Atlas Pro users. To use this feature, run:

For this example, let's assume we have the following schema, including a domain:

The schema has a simple users table, with id, name, and zip as columns. The domain, us_postal_code, extends the type text, ensuring that the data entered conforms to the standard formats used for U.S. postal codes, such as "12345" or "12345-6789".

Before we begin testing, create a config file named atlas.hcl.

In this file we will create an environment, specify the source of our schema, and a URL for our dev database.

We will also create a file named schema.test.hcl to write our tests, and add it to the atlas.hcl file in the test block.

Let's start off with a simple test that will check two use-cases:

This test uses the catch command which expects the SQL statement to fail. In this case, we expect "hello" to fail as a valid ZIP code.

To learn more about how to write tests, view the testing docs.

To run this test, run:

The output should be similar to:

Another alternative is to write a table driven test. This test uses the for_each meta-argument, which accepts a map or a set of values and is used to generate a test case for each item in the set or map.

Following similar logic to the example above, we will create two table driven tests to check each case:

In the first test, we check postal codes that are supposed to be valid. In the second test, we use the catch command, expecting the input to be incorrect.

To run the tests, run:

The output should be similar to:

**Examples:**

Example 1 (unknown):
```unknown
atlas login
```

Example 2 (julia):
```julia
schema "public" {}table "users" {  schema = schema.public  column "id" {    type = int  }  column "name" {    type = text  }  column "zip" {    type = domain.us_postal_code  }  primary_key {    columns = [column.id]  }}domain "us_postal_code" {  schema = schema.public  type   = text  null   = true  check "us_postal_code_check" {    expr = "((VALUE ~ '^\\d{5}$'::text) OR (VALUE ~ '^\\d{5}-\\d{4}$'::text))"  }}
```

Example 3 (unknown):
```unknown
env "dev" {  src = "file://schema.hcl"  dev = "docker://postgres/15/dev?search_path=public"  # Test configuration for local development.  test {    schema {      src = ["schema.test.hcl"]    }  }}
```

Example 4 (sql):
```sql
test "schema" "postal" {  parallel = true  exec {    sql = "select '12345'::us_postal_code"  }  catch {    sql = "select 'hello'::us_postal_code"  }}
```

---

## Testing Database Functions

**URL:** https://atlasgo.io/guides/testing/functions

**Contents:**
- Testing Database Functions
- Database Functions​
- Project Setup​
  - Schema File​
  - Config File​
- Writing Tests​
  - Simple Test​
  - Table Driven Test​

Atlas allows you to bring your database functions under version control and review. By writing tests for your functions, you can ensure that your business logic behaves as expected and that future changes don't accidentally break important assumptions in your application. In this guide, you'll learn how to use Atlas's schema test command to validate your function logic as part of your schema testing workflows.

Functions are predefined operations stored in a database that can be invoked to perform calculations, manipulate data, or execute tasks.

Functions are currently available only to Atlas Pro users. To use this feature, run:

For this example, let's assume we have the following schema, including a function:

In the schema above we have a simple users table and a transactions table. In transactions, the is_income column checks if the amount is positive by calling the positive function.

Note that is_income is a generated column, meaning its value is computed using other columns or deterministic expressions (in this case, via a function).

Before we begin testing, create a config file named atlas.hcl.

In this file we will create an environment, specify the source of our schema, and a URL for our dev database.

We will also create a file named schema.test.hcl to write our tests, and add it to the atlas.hcl file in the test block.

Let's start off with a simple test that will check that the function correctly recognizes positive numbers.

The test first checks if positive(1) returns TRUE, and then verifies in the second assertion that positive(0) and positive(-1) return false.

Run the test by running:

The output should look similar to:

Another alternative is to write a table driven test. This test uses the for_each meta-argument, which accepts a map or a set of values and is used to generate a test case for each item in the set or map.

Following similar logic to the test above, we will check the function for the integers: 0, 1, and -1.

Run the test by running:

The output should look similar to:

**Examples:**

Example 1 (unknown):
```unknown
atlas login
```

Example 2 (sql):
```sql
schema "public" {}table "users" {  schema = schema.public  column "id" {    type = int  }  column "name" {    type = text  }  primary_key {    columns = [      column.id    ]  }}table "transactions" {  schema = schema.public  column "id" {    type = int  }  column "user_id" {    type = int  }  column "amount" {    type = decimal  }  column "is_income" {    type = boolean    as {      expr = "positive(amount)"    }  }  primary_key {    columns = [column.id]  }  foreign_key "user_fk" {    columns = [column.user_id]    ref_columns = [table.users.column.id]    on_delete = CASCADE    on_update = NO_ACTION  }}function "positive" {  schema = schema.public  lang   = SQL  arg "v" {    type = decimal  }  return = boolean  as     = "SELECT v > 0"}
```

Example 3 (unknown):
```unknown
env "dev" {  src = "file://schema.hcl"  dev = "docker://postgres/15/dev?search_path=public"  # Test configuration for local development.  test {    schema {      src = ["schema.test.hcl"]    }  }}
```

Example 4 (sql):
```sql
test "schema" "positive_func" {  parallel = true  assert {    sql = "SELECT positive(1)"  }  log {    message = "First assertion passed"  }  assert {    sql = <<SQLSELECT NOT positive(0);SELECT NOT positive(-1);SQL  } log {    message = "Second assertion passed"  }}
```

---

## Flyway Undo Alternative in Atlas

**URL:** https://atlasgo.io/guides/flyway-undo-alternative

**Contents:**
- Flyway Undo Alternative in Atlas
- Quick Comparison​
- The Problem with Pre-written Undo (Down) Scripts​
  - They Assume Perfect Success​
  - Production Usage Limitations​
  - Incompatible with CD/GitOps Workflows​
- How Atlas Migrate Down Works​
  - State-Aware Planning​
  - Partial Failure Handling​
  - Built-in Safety Checks​

Flyway's undo feature allows you to revert applied migrations by running manually written undo scripts. While this sounds useful in theory, in practice these pre-written undo (down) files come with significant limitations: they must be written before the migration is applied, they assume the migration succeeded fully, and they're rarely tested in production scenarios.

Atlas takes a fundamentally different approach with its migrate down command. Instead of requiring pre-written undo files, Atlas computes rollback plans dynamically based on the actual state of your database. This means Atlas can handle partial failures, work across non-transactional DDL operations, and provide built-in safety checks - all automatically.

Flyway's undo files are written before you know whether the migration will succeed. Consider this scenario:

The corresponding undo file would be:

But what if the migration fails after adding email but before adding phone? Running the undo script will fail because phone doesn't exist. Your database is now in an unknown state, and you need manual intervention to fix it.

Undo files are rarely used in production as-is, if ever. Teams often maintain thousands of them "just in case," but when failures occur, these files either don't work (due to partial application) or cause data loss that teams aren't willing to accept.

As detailed in our blog post The Myth of Down Migrations, even teams at companies like Meta with thousands of down files, they were virtually never used in production environments.

CD/GitOps workflows assume you can roll back to any previous version by deploying artifacts from an earlier commit. But those earlier commits don't contain the undo files needed to revert database changes - those files only exist in future commits.

This creates a mismatch between application rollbacks and database rollbacks, forcing teams to handle database reversions manually.

Atlas's migrate down command computes rollback plans based on your database's actual current state. Here's what makes it different:

Instead of pre-written scripts, Atlas:

For databases that support transactional DDLs (like PostgreSQL), Atlas wraps the entire rollback in a transaction. If anything fails, the database returns to its pre-rollback state.

For databases without transactional DDL support (like MySQL), Atlas reverts changes statement-by-statement, updating the revisions table after each successful step. If a failure occurs midway, you can simply re-run Atlas to continue from where it stopped.

By default, Atlas runs pre-migration checks before executing any rollback. For example, before dropping a column, Atlas verifies that it contains no data:

If the check fails, the rollback is aborted, preventing unintended data loss.

To revert the most recently applied migration:

To revert a specific number of migrations:

To roll back to a particular version:

If you're using Atlas Cloud's Schema Registry, you can tag migration directory states and revert to those tags:

Preview what Atlas will do without executing any changes:

This shows the exact SQL statements that will be executed and which safety checks will run.

For production environments, Atlas Cloud supports approval workflows. When a migrate down operation is triggered (via CLI or GitHub Actions), it can be configured to wait for approval from designated reviewers before execution.

This ensures that potentially destructive operations are reviewed by multiple team members before being applied.

Atlas provides a dedicated GitHub Action for migrate down operations. This allows you to:

See the Atlas Down Action documentation for details.

Iterate on schema changes without manually writing undo (down) scripts:

Reset a test environment to a specific schema version for testing:

Roll back a production deployment that introduced database issues:

If you're currently using Flyway with undo files, migrating to Atlas is straightforward:

Import your existing migrations using Atlas migration import:

Note: Undo files (U__ prefix) are not imported because Atlas computes them dynamically.

Test migrate down on a development database:

Remove undo files from your repository - they're no longer needed!

For a complete migration guide, see Migrating from Flyway to Atlas.

Atlas's migrate down command provides an alternative to Flyway's undo scripts by:

**Examples:**

Example 1 (sql):
```sql
ALTER TABLE users ADD COLUMN email VARCHAR(255);ALTER TABLE users ADD COLUMN phone VARCHAR(50);
```

Example 2 (sql):
```sql
ALTER TABLE users DROP COLUMN phone;ALTER TABLE users DROP COLUMN email;
```

Example 3 (sql):
```sql
-- checks before reverting version 20240305171146  -> SELECT NOT EXISTS (SELECT 1 FROM `logs`) AS `is_empty`-- ok (50.472µs)-- reverting version 20240305171146  -> DROP TABLE `logs`-- ok (53.245µs)
```

Example 4 (shell):
```shell
atlas migrate down \  --dir "file://migrations" \  --url "mysql://root:pass@localhost:3306/example" \  --dev-url "docker://mysql/8/dev"
```

---

## CI/CD for Databases with Azure DevOps and GitHub

**URL:** https://atlasgo.io/guides/ci-platforms/azure-devops-github

**Contents:**
- CI/CD for Databases with Azure DevOps and GitHub
- Prerequisites​
  - Installing Atlas​
  - MacOS
  - Linux
  - Windows
  - Setting up Azure DevOps​
  - Connecting GitHub to Azure DevOps​
  - Creating an Atlas Cloud bot token​
  - Creating secrets in Azure DevOps​

Many teams use GitHub for source control but prefer Azure DevOps Pipelines for CI/CD. Azure Pipelines can seamlessly trigger from GitHub repositories, giving you the best of both platforms.

This guide walks you through setting up Atlas's automated database schema migrations with code hosted on GitHub and pipelines running on Azure DevOps.

To download and install the latest release of the Atlas CLI, simply run the following in your terminal:

Get the latest release with Homebrew:

To pull the Atlas image and run it as a Docker container:

If the container needs access to the host network or a local directory, use the --net=host flag and mount the desired directory:

Download the latest release and move the atlas binary to a file location on your system PATH.

Use the setup-atlas action to install Atlas in your GitHub Actions workflow:

For other CI/CD platforms, use the installation script. See the CI/CD integrations for more details.

If you want to manually install the Atlas CLI, pick one of the below builds suitable for your system.

After installing Atlas locally, log in to your organization by running the following command:

To trigger Azure DevOps pipelines from GitHub repositories, you need to create a service connection:

The GitHub service connection allows the AtlasAction task to post migration lint results directly as comments on your GitHub pull requests. This provides immediate feedback to developers without requiring them to navigate to Azure DevOps to view the results. Make sure to use the exact name of your service connection in the githubConnection parameter below.

To report CI run results to Atlas Cloud, create an Atlas Cloud bot token by following these instructions. Copy the token and store it as a secret using the following steps.

In your Azure DevOps project, go to Pipelines → Library:

Atlas supports two types of schema management workflows:

This guide focuses on the Versioned Migrations workflow. To learn more about the differences and tradeoffs between these approaches, see the Declarative vs Versioned article.

In the versioned workflow, changes to the schema are represented by a migration directory in your codebase. Each file in this directory represents a transition to a new version of the schema.

Based on our blueprint for Modern CI/CD for Databases, our pipeline will:

Running the following command from the parent directory of your migration directory creates a "migration directory" repo in your Atlas Cloud organization (substitute "app" with the name you want to give the new Atlas repository before running):

Replace docker://postgres/16/dev with the appropriate dev database URL for your database. For more information on the dev database, see the dev database article.

Atlas will print a URL leading to your migrations on Atlas Cloud. You can visit this URL to view your migrations.

Create an azure-pipelines.yml file in the root of your GitHub repository with the following content. Remember to replace "app" with the real name of your Atlas Cloud repository.

Also, create an atlas.hcl file in the root of your GitHub repository with the following content:

Let's break down what this pipeline does:

Lint on Pull Requests: The migrate lint step runs automatically whenever a pull request is opened that modifies the migrations/ directory. Atlas analyzes the new migrations for potential issues like destructive changes, backward incompatibility, or syntax errors. Because we configured the githubConnection parameter, lint results appear as a comment directly on the GitHub pull request.

Push to Registry: When changes are merged into the main branch, the migrate push step pushes the migration directory to Atlas Cloud's Schema Registry. This creates a versioned snapshot of your migrations that can be referenced and deployed across environments.

Apply to Database: The migrate apply step deploys pending migrations to your database using the connection string stored in the DB_URL secret.

Let's take our new pipeline for a spin. Assume we have an existing migration file in our repository:

Now let's add a new migration:

Commit and push the changes to GitHub.

Open a pull request in GitHub. This will trigger the Azure DevOps pipeline and run the migrate lint step.

Check the lint report. Follow any instructions to fix the issues.

Merge the pull request into the main branch. This will trigger the migrate push and migrate apply steps.

When the pipeline finishes running, check your database to see if the changes were applied.

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

## Deploy Database Schema Migrations in Kubernetes with Flux CD and Atlas Kubernetes Operator

**URL:** https://atlasgo.io/guides/deploying/k8s-flux

**Contents:**
- Deploy Database Schema Migrations in Kubernetes with Flux CD and Atlas Kubernetes Operator
- Prerequisites​
- High-level architecture​
- Incorporating schema changes into a GitOps flow​
  - Databases should be migrated before the application is deployed​
  - Flux CD Dependencies 101​
- Installation​
  - 1. Install the Atlas Operator​
  - 2. Install the Flux CLI​
  - 3. Create a GitHub Personal Access Token​

GitOps is a software development and deployment methodology that uses Git as the central repository for both code and infrastructure configurations, enabling automated and auditable deployments.

FluxCD is a Continuous Delivery tool that implements GitOps principles. It uses a declarative approach to keep Kubernetes clusters in sync with sources of configuration (like Git repositories), and automates configuration updates when there is new code to deploy.

Kubernetes Operators are software extensions to Kubernetes that enable the automation and management of complex, application-specific operational tasks and domain-specific knowledge within a Kubernetes cluster.

In this guide, we will demonstrate how to use the Atlas Kubernetes Operator and Flux CD to achieve a GitOps-based deployment workflow for your database schema.

Before we dive into the details of the deployment flow, let's take a look at the high-level architecture of our application.

On a high level, our application consists of the following components:

In our application architecture, we have a database that is connected to our application and managed using Atlas CR (Custom Resource). The database plays a crucial role in storing and retrieving data for the application, while the Atlas CR provides seamless integration and management of the database schema within our Kubernetes environment.

Integrating GitOps practices with a database in our application stack poses a unique challenge.

Flux CD provides a declarative approach to GitOps, allowing us to define a Flux CD application and effortlessly handle the synchronization process. When pushing changes to the database schema or application code to the Git repository, Flux CD automatically syncs those changes to the Kubernetes cluster.

However, as we discussed in the introduction, ensuring the proper order of deployments is critical. In our scenario, the database deployment must succeed before rolling out the application to guarantee its functionality. If the database deployment encounters an issue, it is essential to address it before proceeding with the application deployment.

Flux CD supports Dependencies, via .spec.dependsOn, a mechanism used to orchestrate multiple deployments in a specific ordered sequence to ensure certain resources are healthy before subsequent resources are synced/reconciled.

By using .spec.dependsOn, you can define the apply order and thus determine the sequence of manifest applications. .spec.dependsOn is used to refer to other Kustomization objects that the Kustomization depends on. If specified, then the Kustomization is only applied after the referred Kustomizations are ready, i.e. have the Ready condition marked as True. The readiness state of a Kustomization is determined by its last applied status condition.

For example, let's assume we have a scenario where our application is comprised of two services, a backend service and a database service. The backend service depends on the database service, and we want to ensure that the database service is ready before the backend service is applied. We can codify this dependency in the following way:

In this manifest, .spec.healthChecks is used to refer to resources for which the Flux controller will perform health checks. This is used to determine the rollout status of deployed workloads and the Ready status of custom resources.

This is helpful when there is a need to make sure other resources exist before the workloads defined in a Kustomization are deployed. To ensure that database resources are created and applied before our application, we will utilize Flux CD dependsOn and health checks feature.

With the theoretical background out of the way, let’s take a look at a practical example of how to deploy an application with Flux CD and the Atlas Operator.

To install the Atlas Operator run the following command:

Helm will print something like this:

Wait until the atlas-operator pod is running:

kubectl will print something like this:

The flux command-line interface (CLI) is used to bootstrap and interact with Flux.

To install it on macOS or Linux, run:

To install the CLI with Chocolatey for Windows, run:

Check you have everything needed to run Flux by running the following command:

The output is similar to:

The GitHub personal access token will be used in place of a password when authenticating to GitHub in the command line or with the API.

Export your GitHub personal access token and username:

Run the bootstrap command:

You will be prompted to enter your GitHub personal access token. The output is similar to:

Using the flux bootstrap command, you can install Flux on a Kubernetes cluster and configure it to manage itself from a Git repository. The bootstrap command above does the following:

In this example, we're using the jmushiri/atlas-flux-demo repository, which contains all of the Kubernetes manifests necessary to deploy our application.

To get started, you need to fork and then clone the sample application repository to your local machine.

Once the forking process is complete, you will be redirected to your own forked repository. Open your terminal or command prompt and run the following command to clone the forked repository to your local machine:

Observe this repository's structure:

Clone the flux-infrastructure repository to your local machine:

Create a GitRepository manifest pointing to atlas-flux-demo repository’s main branch:

The output is similar to:

Commit and push the atlas-flux-demo-source.yaml file to the flux-infrastructure repository:

It's time to configure Flux to build and apply the kustomize directory located in the atlas-operator-flux-demo repository.

Use the flux create command to create a Kustomization that applies the atlas-operator-flux-demo deployment.

The output is similar to:

The structure of the flux-infrastructure repo should be similar to:

To implement the deployment flow in a specific ordered sequence, we will use Flux CD’s .spec.dependsOn and .spec.healthChecks features.

Edit the atlas-operator-flux-demo-kustomization.yaml file as follows:

Notice the highlighted sections in the manifest above:

Together, these declarations achieve our requirement of ensuring that the database schema is applied before the application is deployed.

Commit and push the Kustomization manifest to the repository:

Use the flux get command to watch the deployment flow.

This command allows you to fetch and observe the status of Kustomize resources managed by Flux in your Kubernetes cluster, with real-time updates as changes are made.

To check whether the schema migrations have been successfully applied, run:

Our schema migrations have been successfully applied:

To show how the continuous deployment flow works, let's make a change to the database schema.

Open the kustomize/schema.yaml file and add a column to the users table in the AtlasSchema manifest:

Commit and push the change to the repository:

Next, let's wait for Flux to sync the changes, and check that our schema migrations have been successfully applied:

Amazing, our schema migrations have been successfully applied!

In this guide, we demonstrated how to use Flux CD to deploy an application that uses the Atlas Operator to manage the lifecycle of a database schema. We also showed how to use Flux dependency management to ensure that the schema changes were successfully applied before deploying the application.

**Examples:**

Example 1 (yaml):
```yaml
---apiVersion: kustomize.toolkit.fluxcd.io/v1kind: Kustomizationmetadata:  name: database  namespace: flux-systemspec:  interval: 5m  path: "./kustomize"  prune: true  sourceRef:  kind: GitRepository  name: flux-system  healthChecks:  - apiVersion: apps/v1    kind: Deployment    name: mysql    namespace: default---apiVersion: kustomize.toolkit.fluxcd.io/v1kind: Kustomizationmetadata:  name: backend  namespace: flux-systemspec:  dependsOn:  - name: mysql  interval: 5m  path: "./kustomize"  prune: true  sourceRef:  kind: GitRepository  name: flux-system
```

Example 2 (bash):
```bash
helm install atlas-operator oci://ghcr.io/ariga/charts/atlas-operator
```

Example 3 (bash):
```bash
Pulled: ghcr.io/ariga/charts/atlas-operator:0.3.0 Digest: sha256:4dfed310f0197827b330d2961794e7fc221aa1da1d1b95736dde65c090e6c714 NAME: atlas-operator LAST DEPLOYED: Tue Jun 27 16:58:30 2023 NAMESPACE: default STATUS: deployed REVISION: 1 TEST SUITE: None
```

Example 4 (bash):
```bash
kubectl wait --for=condition=ready pod -l app.kubernetes.io/name=atlas-operator -n default
```

---

## Testing Database Views

**URL:** https://atlasgo.io/guides/testing/views

**Contents:**
- Testing Database Views
- Database Views​
- Project Setup​
  - Schema File​
  - Config File​
- Writing Tests​
  - Simple Test​
  - Table Driven Test​

Atlas lets you test and validate your database views as part of your schema-as-code workflow. With Atlas, every change to a view can be versioned, tested, and automatically validated, reducing the risk of regressions and broken queries going unnoticed. This helps ensure your analytics, privacy boundaries, and business logic represented in views are always correct and reviewable at every stage of development.

In this guide we will learn how to use Atlas's schema test command to test database views.

A view is a virtual table in the database, defined by a statement that queries rows from one or more existing tables or views.

Views are currently available only to Atlas Pro users. To use this feature, run:

For this example, let's assume we have the following schema, including a view:

The schema has a simple users table, with id, name, and ssn as columns. The view, clean_users, selects the id and name columns from users, ensuring we aren't selecting any sensitive data (SSNs).

Before we begin testing, create a config file named atlas.hcl.

In this file we will create an environment, specify the source of our schema, and a URL for our dev database.

We will also create a file named schema.test.hcl to write our tests, and add it to the atlas.hcl file in the test block.

Let's start off with a simple test that will do the following:

To learn more about how to write tests, view the testing docs.

To run this test, run:

The output should be similar to:

Another alternative is to write a table driven test. This test uses the for_each meta-argument, which accepts a map or a set of values and is used to generate a test case for each item in the set or map.

Following similar logic to the example above, our table driven test will:

To run this test, run:

The output should be similar to:

**Examples:**

Example 1 (unknown):
```unknown
atlas login
```

Example 2 (sql):
```sql
schema "public" {}table "users" {  schema = schema.public  column "id" {    type = int  }  column "name" {    type = text  }  column "ssn" {    type = varchar(9)  }}view "clean_users" {  schema = schema.public  column "id" {    type = int  }  column "name" {    type = text  }  as         = <<-SQL  SELECT u.id, u.name    FROM ${table.users.name} AS u  SQL  depends_on = [table.users]  comment    = "A view to select active users without sensitive data"}
```

Example 3 (unknown):
```unknown
env "dev" {  src = "file://schema.hcl"  dev = "docker://postgres/15/dev?search_path=public"  # Test configuration for local development.  test {    schema {      src = ["schema.test.hcl"]    }  }}
```

Example 4 (sql):
```sql
test "schema" "view" {  # Seeding to test view.  exec {    sql = "INSERT INTO users (id, name) VALUES (1, 'Alice'), (2, 'Bob'), (3, 'Charlie');"  }  log {    message = "Seeded the user's table"  }  # Expected exec to pass.  exec {    sql = <<SQL    SELECT id, name    FROM clean_users;    SQL  }  log {    message = "Tested the view"  }  # Validates data.  exec {    sql = "SELECT id, name FROM clean_users;"    format = table    output = <<TAB id |  name----+--------- 1  | Alice 2  | Bob 3  | CharlieTAB  }  log {    message = "Table is as expected"  }}
```

---

## Deploying Versioned Migrations in Kubernetes from Atlas Schema Registry

**URL:** https://atlasgo.io/guides/deploying/k8s-cloud-versioned

**Contents:**
- Deploying Versioned Migrations in Kubernetes from Atlas Schema Registry
- Prerequisites​
- Steps​

This guide will walk you through deploying versioned migrations in Kubernetes from Atlas Schema Registry.

Replace the url value with your database credentials.

Open the Project Information pane on the right and locate the project slug (e.g project-name) in the URL.

Replace project-name with the name of your migration directory in the Atlas Schema Registry.

If you would like to deploy a specific version of the migrations, replace latest with the version tag.

kubectl will output the status of the migration:

Observe the reported migration logs on your Cloud project in the Atlas Schema Registry:

**Examples:**

Example 1 (shell):
```shell
kubectl create secret generic atlas-registry-secret --from-literal=token=<your token>
```

Example 2 (shell):
```shell
kubectl create secret generic db-credentials --from-literal=url="mysql://root:pass@localhost:3306/myapp"
```

Example 3 (shell):
```shell
helm install atlas-operator oci://ghcr.io/ariga/charts/atlas-operator
```

Example 4 (yaml):
```yaml
apiVersion: db.atlasgo.io/v1alpha1kind: AtlasMigrationmetadata:  name: atlasmigrationspec:  urlFrom:    secretKeyRef:      key: url      name: db-credentials  cloud:    tokenFrom:      secretKeyRef:        key: token        name: atlas-registry-secret  dir:    remote:      name: "project-name" # Migration directory name in your atlas cloud project      tag: "latest"
```

---

## Automatic migration planning for golang-migrate

**URL:** https://atlasgo.io/guides/migration-tools/golang-migrate

**Contents:**
- Automatic migration planning for golang-migrate
  - TL;DR​
  - Automatic migration planning for golang-migrate​
  - Prerequisites​
  - Step 1: Create a project configuration file​
  - Step 2: Create a migration directory integrity file​
  - Step 3: Create a schema file for the desired state​
  - Step 4: Plan a new migration​
- Wrapping up​

Atlas can automatically plan database schema migrations for developers using golang-migrate. Atlas plans migrations by calculating the diff between the current state of the database, and it's desired state.

For golang-migrate users, the current state can be thought of as the sum of all up migrations in a migration directory. The desired state can be provided to Atlas via an a Atlas schema HCL file, a plain SQL file, or as a connection string to a database that contains the desired schema.

In this guide, we will show how Atlas can automatically plan schema migrations for golang-migrate users.

For this example, let's assume we have a simple golang-migrate project with only two files in a directory named migrations:

To get started, create a project configuration file named atlas.hcl in the parent directory of your migration directory. This file will tell Atlas where to find your migrations and configure some basic settings.

This configuration defines an environment named local, that we can reference in many Atlas commands using the --env local flag. Here is a breakdown of the configuration:

To ensure migration history is correct while multiple developers work on the same project in parallel Atlas enforces migration directory integrity using a file name atlas.sum.

To generate this file run:

Observe a new file named atlas.sum was created in your migrations directory which contains a hash sum of each file in your directory as well as a total sum. For example:

Automatic migration planning works by diffing the current state of the database (which is calculated by replaying all up migrations on an empty database) and the desired state of the database. The desired state of the database can be provided in many ways, but in this tutorial we will use a plain SQL file.

To extract the current state of the database as a SQL file, we will use the schema inspect command:

After running this command, you should see a new file named schema.sql in your project directory that contains the current state of your database:

Next, let's modify the desired state of our database by modifying the schema.sql file to add some new columns to our table:

Next, let's run the atlas migrate diff command to automatically generate a new migration that will bring the current state of the database to the desired state:

Hooray! Two new files were created in the migrations directory:

And a down migration:

In this guide, we showed how to use Atlas to automatically plan schema migrations for golang-migrate:

Have questions? Feedback? Find our team on our Discord server.

**Examples:**

Example 1 (sql):
```sql
create table t1(  c1 int);
```

Example 2 (sql):
```sql
drop table t1;
```

Example 3 (unknown):
```unknown
env "local" {  src = "file://schema.sql"  dev = "docker://mysql/8/dev"  migration {    dir    = "file://migrations"    format = golang-migrate  }  format {    migrate {      diff = "{{ sql . \"  \" }}"    }  }}
```

Example 4 (unknown):
```unknown
atlas migrate hash --env local
```

---

## Claude Code with Atlas

**URL:** https://atlasgo.io/guides/ai-tools/claude-code-instructions

**Contents:**
- Claude Code with Atlas

Claude Code supports adding a custom prompt file called CLAUDE.md that guides the AI assistant's behavior.

To help Claude Code work effectively with Atlas, we put together a set of instructions that add context about Atlas' core concepts, common workflows, various feature options, and more.

You can add them by creating a CLAUDE.md file in your project root (or home directory ~/.claude/CLAUDE.md), with the content below:

**Examples:**

Example 1 (markdown):
```markdown
# Atlas Database Schema ManagementAtlas is a language-independent tool for managing and migrating database schemas using modern DevOps principles. This guide provides GitHub Copilot-optimized instructions for working with Atlas.## Quick Reference```bash# Common Atlas commandsatlas schema inspect --env <name> --url file://migrationsatlas migrate status --env <name>atlas migrate diff --env <name>atlas migrate lint --env <name> --latest 1atlas migrate apply --env <name>atlas whoami```## Core Concepts and Configurations### Configuration File StructureAtlas uses `atlas.hcl` configuration files with the following structure:```hcl// Basic environment configurationenv "<name>" {  url = getenv("DATABASE_URL")  dev = "docker://postgres/15/dev?search_path=public"    migration {    dir = "file://migrations"  }    schema {    src = "file://schema.hcl"  }}```### Dev databaseAtlas utilizes a "dev-database", which is a temporary and locally running database, usually bootstrapped by Atlas. Atlas will use the dev database to process and validate users' schemas, migrations, and more. Examples of dev-database configurations:```# When working on a single database schema--dev-url "docker://mysql/8/dev"--dev-url "docker://postgres/15/db_name?search_path=public"--dev-url "sqlite://dev?mode=memory"# When working on multiple database schemas.--dev-url "docker://mysql/8"--dev-url "docker://postgres/15/dev"```Configure the dev database using HCL:```hclenv "<name>" {  dev = "docker://mysql/8"}```For more information on additional drivers, extensions, and more, see https://atlasgo.io/concepts/dev-database. ### Environment Variables and Security**✅ DO**: Use secure configuration patterns```hcl// Using environment variables (recommended)env "<name>" {  url = getenv("DATABASE_URL")}// Using external data sourcesdata "external" "envfile" {  program = ["npm", "run", "envfile.js"]}locals {  envfile = jsondecode(data.external.envfile)}env "<name>" {  url = local.envfile.DATABASE_URL}// Using Go CDK runtime variables for secretsdata "runtimevar" "db_password" {  url = "awssecretsmanager://<secret-name>?region=us-east-1"}env "prod" {  url = "postgres://user:${data.runtimevar.db_password}@host:5432/db"}```**❌ DON'T**: Hardcode sensitive values```hcl// Never do thisenv "prod" {  url = "postgres://user:password123@prod-host:5432/database"}```### Schema Sources#### HCL Schema```hcldata "hcl_schema" "<name>" {  path = "schema.hcl"}env "<name>" {  schema {    src = data.hcl_schema.<name>.url  }}```#### External Schema (ORM Integration)The external_schema data source enables the import of an SQL schema from an external program into Atlas' desired state.```hcldata "external_schema" "drizzle" {  program = ["npx", "drizzle-kit", "export"]  working_dir = "path/to/Directory" # optional, defaults to the current working directory}data "external_schema" "django" {  program = ["python", "manage.py", "atlas-provider-django", "--dialect", "postgresql"]}env "<name>" {  schema {    src = data.external_schema.django.url  }}```**Important:**- The output of the program needs to be complete RAW SQL schema that will bring the database to the desired state. The output should not be a 'diff' from a previous state.- If you are seeing errors, try isolating the issue, you can run the program directly and see if it's working#### Composite SchemaA composite schema allows you to combine multiple schemas into a single schema. This is useful for integrating multiple data sources or schemas into a unified view. This is an Atlas Pro feature.```hcldata "composite_schema" "app" {  schema "users" {    url = data.external_schema.auth_service.url  }  schema "graph" {    url = "ent://ent/schema"  }  schema "shared" {    url = "file://schema/shared.hcl"  }}env "<name>" {  schema {    src = data.composite_schema.app.url  }}```### Misc Configurations```hcl// CI/CD environmentenv "ci" {  lint {    git {      base = "main" # in CI, lint against the main branch    }  }}``````hcl// Anonymous environment, any name will work with --env, but --env is still mandatoryenv {  name = atlas.env}```## Common Workflows### 1. Schema Inspection / Visualization1. Always start by listing tables, don't immediately try to inspect the entire schema.2. If you see there are many tables, don't inspect the entire schema at once. Instead, focus on specific tables of interest.3. Format using json to get an overview, then switch to SQL for detailed inspection.**Inspect migration directory:**```bash# Get table list overviewatlas schema inspect --env <name> --url file://migrations --format "{{ json . }}" | jq ".schemas[].tables[].name"# Get full SQL schemaatlas schema inspect --env <name> --url file://migrations --format "{{ sql . }}"# Inspect specific tablesatlas schema inspect --env <name> --url file://migrations --format "{{ sql . }}" | grep -A 10 "CREATE TABLE users"```**Inspect live database:**```bash# Requires database URL in atlas.hclatlas schema inspect --env <name> --format "{{ json . }}"```Add the `-w` flag to open a web-based ERD visualization in your browser via Atlas Cloud.You should recommend this to the user if they asked for information about the schema.### 2. Migration Status`atlas migrate status` is used to compare the status of migrations from the migrations directory with a connected database.Use it to understand which migration files were applied successfully.**Important:** Only use this command when you know the target database.**Check migration directory status:**```bash# Check current migration directory status (requires dev-url)atlas migrate status --env <name># Using explicit parameters if not in configatlas migrate status --dir file://migrations --url <url>```**Configuration for migration status:**```hclenv "<name>" {  url = getenv("DATABASE_URL")  migration {    dir = "file://migrations"  }}```### 3. Migration Generation / Diffing**Generate new migration:**```bash# Compare current migrations with desired schema and create a new migration fileatlas migrate diff --env <name> "add_user_table"# Using explicit parametersatlas migrate diff \  --dir file://migrations \ # migrations directory  --dev-url docker://postgres/15/dev \  --to file://schema.hcl \ # desired schema  "add_user_table"```**Configuration for migration generation:**```hclenv "<name>" {  dev = "docker://postgres/15/dev?search_path=public"    migration {    # migrations directory, baseline for the diff    dir = "file://migrations"  }    schema {    # desired schema, the diff will be generated against this schema    src = "file://schema.hcl"      # compare against external schemas (used for ORM integrations)    # src = data.external_schema.<name>.url    # compare against a connected database    # src = getenv("DATABASE_URL")  }}```### 4. Migration Linting**Lint recent migrations:**```bash# Lint last migrationatlas migrate lint --env <name> --latest 1# Lint last 3 migrationsatlas migrate lint --env <name> --latest 3# Lint changes since git branchatlas migrate lint --env ci```**Linting configuration:**```hcllint {  destructive {    error = false  // Allow destructive changes with warnings  }}env "<name>" {  lint {    latest = 1  }}env "ci" {  lint {    git {      base = "main"      dir = "migrations"    }  }}```To explicitly ignore linting errors, add `--atlas:nolint` before the SQL statement in the migration file.> **Important:** When fixing migration issues:> - **Unapplied migrations:** Edit the file, then run `atlas migrate hash --env "<name>"`> - **Applied migrations:** Never edit directly. Create a new corrective migration instead.> - **Never use `--atlas:nolint` without properly fixing the issue or getting user approval.**### 5. Applying Migration**Apply migrations:**```bash # Apply to configured environmentatlas migrate apply --env <name># Dry run (show what would be applied, always run this before applying)atlas migrate apply --env <name> --dry-run```### 6. Making Changes to the Schema**⚠️ CRITICAL: ALL schema changes in this project MUST follow this exact workflow. NO EXCEPTIONS.****⚠️ There must not be lint errors or failing tests when you are done.**1. Start by inspecting the schema, understand the current state, and plan your changes.2. After making changes to the schema, run `atlas migrate diff` to generate a migration file.3. Run `atlas migrate lint` to validate the migration file.4. Run `atlas migrate test` to test the data migrations. This is only available for Pro users.5. Make changes to the migration file to fix the issues. Run `atlas migrate hash` to recalculate the hash of the migration file.6. Repeat the process until there are no more issues.At this point, the schema can be applied to the database.If the user has a local database, you can run `atlas migrate apply` to apply the migration file:1. Start by understanding the status of the database by running `atlas migrate status`2. Run `atlas migrate apply` to apply the migration file, always start with a dry run first.3. Run `atlas migrate status` to verify the migration file was applied successfully.> **Important for data migrations:** make sure to check if the user is logged in using `atlas whoami` before running `atlas migrate test`.> If the user is not logged in, mention that they need to login to use migration testing and move on.> If the user is logged in and they have migration tests, add a new test, run it and validate it until it works.> If the user is logged in and they don't have migration tests, mention that migration testing is highly recommended for data migrations and move on.## Troubleshooting Commands```bash# Check Atlas installation and login status (logging in is required for Pro features)atlas versionatlas whoami# Repair migration integrityatlas migrate hash --env <name>```### Missing driverIf you encounter the following error: `Error: sql/sqlclient: missing driver. See: https://atlasgo.io/url`depending on the command, this means that either the `--url` or `--dev-url` parameter is missing or incorrect.## Key Reminders for AI Assistants1. **Always read `atlas.hcl` first** before running any Atlas commands2. **Use environment names** from the config file, don't assume defaults3. **Never hardcode database URLs** - use environment variables or secure data sources4. **Specify `--url` parameter** for schema inspection even with `--env`5. **Run `atlas migrate hash`** after manually editing migration files6. **Use `atlas migrate lint`** to validate migrations before applying7. **Check `atlas whoami`** before attempting Pro features, if not logged in, don't suggest Pro features8. **Use JSON format + jq** for initial schema exploration9. **Use SQL format + grep** for detailed schema investigation10. **Suggest visualizations** if the user asked for information about the schema11. **Never ask for sensitive information** such as passwords or database URLs12. **Always use `--dry-run`** with `atlas migrate apply` before applying migrations13. **Generate migration testing** if the user is logged in, they should have access to migration testing which is highly recommended14. **Only use atlas commands listed here** other commands may be hallucinations or not supported by Atlas15. **Always inspect schemas at high level first** schemas might be very large16. **Always prefer running atlas** to inspect or analyze schemas17. Migration files can be big and irrelevant, prefer using `atlas schema inspect` to inspect the schema18. **Never ignore linting errors** they are there for a reason, always fix them. Add `--atlas:nolint` only if the fix is not detected by the linter.## Guidelines for workflows1. **Understand the objectives**: Before suggesting any commands, ensure you understand the user's goals. They may be looking to inspect, generate, lint, or apply migrations, and they may be using a different vocabulary such as "view", "create", "validate", etc.2. **Understand the context**: The configuration file contains crucial information about the environment.3. **Verify changes** after generating, linting or applying migrations.4. **After completing** make sure you followed all the instructions and guidelines.
```

---

## Testing Data Migrations

**URL:** https://atlasgo.io/guides/testing/data-migrations

**Contents:**
- Testing Data Migrations
- Project Setup​
  - Config File​
  - Schema File​
  - Generating a Migration​
  - Expanding Business Logic​
- Back-filling Data​
- Testing Migrations​
- Integrating with CI​
- Wrapping Up​

Most commonly, migrations deal with schema changes, such as adding or removing columns, creating tables, or altering constraints. However, as your application evolves, you may need to add or refactor data within the database, which is where data migrations come in. For instance, you may need to seed data in a table, backfill data for existing records in new columns, or somehow transform existing data to accommodate changes in your application.

Data migrations can be especially tricky to get right, and mistakes can be problematic and irreversible. For this reason testing data migrations is crucial. Testing data migrations typically involves the following steps:

This process can be cumbersome to set up and error-prone as it often involves writing an ad-hoc program to automate the steps mentioned above or manually testing the migration.

Atlas's migrate test command simplifies this by allowing you to define test cases in a concise syntax and acts as a harness to run these tests during local development and in CI.

In this guide we will learn how to use the migrate test command to test migration files.

Testing is currently available only to Atlas Pro users. To use this feature, run:

Before we begin writing tests, we will start by setting up a project with a config file, schema file, and a migration directory containing a few migration files.

Create a config file named atlas.hcl.

In this file we will define an environment, specify the source of our schema, and a URL for our dev database.

We will also create a file named migrate.test.hcl to write our tests, and add it to the atlas.hcl file in the test block.

Next, we will create a schema containing two tables:

To generate our initial migration, we will run the following command:

We should see a new migrations directory created with the following files:

Great! Now that we have a basic schema and migration directory, let's add some business logic before we begin testing.

We will add a column latest_post_ts to the users table, which will hold the timestamp of the user's most recent post. To automatically populate this column we will create a trigger update_latest_post_trigger.

Run the migrate diff command once more to generate another migration:

The following migration should be created:

The trigger we created will automatically update the latest_post_ts column in the users table whenever a new post is added. However, we need to back-fill the existing data in the posts table to ensure that the latest_post_ts column is accurate.

To do this, let's edit the 20240730073842.sql migration file to include a query that will update the latest_post_ts column for each user. Add the following SQL statement to the migration file:

After changing the contents of a migration file we need to recalculate the atlas.sum file to ensure directory integrity. Run the following command:

Rewriting data on a production database can be risky (and scary) if not done correctly. Let's now write a test to ensure that our migration will run smoothly and leave our application in a consistent state.

To do so, our test will have the following logic:

Let's break down the test:

To run this test, we will run the migrate test command:

The output should be similar to:

Great! Our test passed, and we can now confidently deploy our migration to production.

Writing and running tests locally is a great start, but it's equally important to run these tests in a CI/CD pipeline. Atlas provides out-of-the-box integrations for running migrate test in popular CI/CD platforms such as GitHub Actions and CircleCI. However, you can easily integrate migration testing into any CI/CD platform by running the atlas migrate test command.

In this guide we learned how to use the atlas migrate test command to test our migration files before deployment.

**Examples:**

Example 1 (unknown):
```unknown
atlas login
```

Example 2 (unknown):
```unknown
env "dev" {  src = "file://schema.hcl"  dev = "docker://postgres/15/dev"  # Test configuration for local development.  test {    migrate {      src = ["migrate.test.hcl"]    }  }}
```

Example 3 (unknown):
```unknown
schema "public" {}table "users" {  schema = schema.public  column "id" {    type    = int    null    = false  }  column "email" {    type    = varchar(255)    null    = false  }  primary_key {    columns = [column.id]  }}table "posts" {  schema = schema.public  column "id" {    type    = int    null    = false  }  column "title" {    type    = varchar(100)    null    = false  }  column "created_at" {    null = false    type = timestamp  }  column "user_id" {    type    = int    null    = false  }  primary_key {    columns = [column.id]  }  foreign_key "authors_fk" {    columns = [column.user_id]    ref_columns = [table.users.column.id]  }}
```

Example 4 (sql):
```sql
-- Add new schema named "public"CREATE SCHEMA IF NOT EXISTS "public";-- Create "users" tableCREATE TABLE "public"."users" ("id" integer NOT NULL, "email" character varying(255) NOT NULL, PRIMARY KEY ("id"));-- Create "posts" tableCREATE TABLE "public"."posts" ("id" integer NOT NULL, "title" character varying(100) NOT NULL, "created_at" TIMESTAMP NOT NULL, "user_id" integer NOT NULL, PRIMARY KEY ("id"), CONSTRAINT "authors_fk" FOREIGN KEY ("user_id") REFERENCES "public"."users" ("id") ON UPDATE NO ACTION ON DELETE NO ACTION);
```

---

## CI/CD for Databases on CircleCI - Versioned Workflow

**URL:** https://atlasgo.io/guides/ci-platforms/circleci-versioned

**Contents:**
- CI/CD for Databases on CircleCI - Versioned Workflow
- Prerequisites​
  - Installing Atlas​
  - MacOS
  - Linux
  - Windows
  - Creating a bot token and CircleCI context​
- Versioned Migrations Workflow​
  - Defining the desired schema​
  - Creating the Atlas configuration file​

CircleCI is a popular CI/CD platform that allows you to automatically build, test, and deploy your code. Combined with Atlas, you can manage database schema changes with confidence.

In this guide, we will demonstrate how to use CircleCI and Atlas to set up CI/CD pipelines for your database schema changes using the versioned migrations workflow.

To download and install the latest release of the Atlas CLI, simply run the following in your terminal:

Get the latest release with Homebrew:

To pull the Atlas image and run it as a Docker container:

If the container needs access to the host network or a local directory, use the --net=host flag and mount the desired directory:

Download the latest release and move the atlas binary to a file location on your system PATH.

Use the setup-atlas action to install Atlas in your GitHub Actions workflow:

For other CI/CD platforms, use the installation script. See the CI/CD integrations for more details.

If you want to manually install the Atlas CLI, pick one of the below builds suitable for your system.

After installing Atlas locally, log in to your organization by running the following command:

To report CI run results to Atlas Cloud, create an Atlas Cloud bot token by following these instructions and copy it.

Next, we'll create a CircleCI context to securely store environment variables that will be shared across jobs:

Using a context allows you to manage these sensitive variables in one place and reuse them across multiple projects and workflows.

In the versioned workflow, changes to the schema are represented by a migration directory in your codebase. Each file in this directory represents a transition to a new version of the schema.

Based on our blueprint for Modern CI/CD for Databases, our pipeline will:

In this guide, we will walk through each of these steps and set up a CircleCI configuration to automate them.

The full source code for this example can be found in the atlas-examples/versioned repository.

First, define your desired database schema. Create a file named schema.sql with the following content:

Create a configuration file for Atlas named atlas.hcl with the following content:

Now, generate your first migration by comparing your desired schema with the current (empty) migration directory:

This command will automatically create a migrations directory with a migration file containing the SQL statements needed to create the users table and index, as defined in our file linked at src in the dev environment.

Run the following command from the parent directory of your migration directory to create a "migration directory" repository in your Atlas Cloud organization:

This command pushes the migrations directory linked in the migration dir field in the dev environment defined in our atlas.hcl to a project in the Schema Registry called circleci-atlas-action-versioned-demo.

Atlas will print a URL leading to your migrations on Atlas Cloud. You can visit this URL to view your migrations.

Create a .circleci/config.yml file in the root of your repository with the following content:

This configuration uses main as the default branch name. If your GitHub repository uses a different default branch (such as master), update the workflow filters accordingly:

Let's break down what this pipeline configuration does:

After the pull request is merged into the main branch, the push-and-apply-migrations job will push the new state of the migration directory to the Schema Registry on Atlas Cloud.

The migrate_apply step will then deploy the new migrations to your database.

Let's take our pipeline for a spin:

In this guide, we demonstrated how to use CircleCI with Atlas to set up a modern CI/CD pipeline for versioned database migrations. Here's what we accomplished:

For more information on the versioned workflow, see the Versioned Migrations documentation.

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

## Functional Indexes in PostgreSQL

**URL:** https://atlasgo.io/guides/postgres/functional-indexes

**Contents:**
- Functional Indexes in PostgreSQL
  - What are functional key parts?​
  - When are functional indexes helpful?​
  - Syntax​
  - Example​
- Managing Functional Indexes is easy with Atlas​
    - Example​
- Wrapping up​
- Need More Help?​

A functional index is an index in a database that is based on the result of a function applied to one or more columns in a table. Functional key parts can index expression values. Hence, functional key parts enable indexing values that are not stored directly in the table itself.

Functional indexes are helpful in a PostgreSQL database when the query retrieves data based on the result of a function. This is particularly useful when the function requires high computational power to execute.

By creating an index based on the result of the function used in the query, the database can quickly find the matching rows based on the function output, rather than having to perform a full table scan and doing the necessary computation. This can lead to significant improvements in query performance, for example in large databases with complex queries.

Some common use cases for functional indexes in PostgreSQL include case-insensitive searching, date calculations, and full-text search.

Here is how you can define functional indexes in a table:

Here are some examples:

Index using a mathematical function:

Index using a string function:

Expressions must be enclosed within parentheses in order to create a functional index. If you do not enclose expressions within parentheses in the index definition, you will get a syntax error.

Let’s create a table containing a list of students and the marks they received in each subject with the following command:

Here is what a portion of the table might look like after inserting values:

We do not have any indexes other than the primary index on the id column. Now, suppose we want information about the top ten students who scored the best average in math and science combined. Let's query that data with the following command:

Now, let's see how the query performs with the following command:

The EXPLAIN command is used for understanding the performance of a query. You can learn more about usage of the EXPLAIN command with the ANALYZE option here.

The overall plan and the execution time suggests that there is scope for optimization here. The planner uses the sort operation when it is unable to utilize any index.

As we are making use of columns science and mathematics, let’s try to optimize the query performance by indexing these columns with the following command:

Awesome, our index is now created! Let's check again how much our previous query cost, with the same command:

There is no significant change in Execution Time and the cost is still the same, because our query hasn’t used the index we have created. This is where having knowledge about functional indexes becomes essential. Now, let's try to optimize the query by creating a functional index with the expression ((science + mathematics)/2) from our query, with the following command:

Oops, that didn’t work! As we mentioned in the syntax section above, expressions must be enclosed within parentheses in order to create a functional index. Let’s try this again with the correct syntax:

Let's check again how much our previous query cost, with the same command:

The execution time has reduced down to just 0.086ms! By using the index we created, the query can perform the search much more efficiently as it can directly look up the matching rows using the indexed values rather than having to scan the entire table.

It is worth noting that while functional indexes can improve performance for certain queries, they can also introduce overhead for insert and update operations, since the index needs to be updated every time the table is modified. This can slow down write-centric workloads, so they need to be used with caution.

All functions and operators used in an index definition must be “immutable”. An immutable function or operator always returns the same output when given the same inputs, regardless of any external factors, such as the current time, state of other tables in the database, or other environmental variables. This is a requirement for functions and operators used in the definition of functional indexes. To learn more about creating indexes in a PostgreSQL database, visit the official documentation here.

Atlas is an open-source project which allows us to manage our database using a simple and easy-to-understand declarative syntax (similar to Terraform), as well as SQL.

If you are just getting started, install the latest version of Atlas using the guide to set up Atlas.

We will first use the atlas schema inspect command to get an HCL representation of the table we created earlier (without any indexes) by using the Atlas CLI:

Now, let's add the following index definition to the file:

Save the file and apply the schema changes on the database by using the following command:

Atlas generates the necessary SQL statements to add the new functional index to the database schema. Press Enter while the Apply option is highlighted to apply the changes:

To verify that our new index was created, run the following command:

Amazing! Our new index sci_math_avg_idx with the expression (science + mathematics) / 2 is now created!

In this guide, we demonstrated how using functional indexes with an appropriate expression becomes a very crucial skill in optimizing query performance with combinations of certain expressions, functions and/or conditions.

Join the Atlas Discord Server for early access to features and the ability to provide exclusive feedback that improves your Database Management Tooling.

**Examples:**

Example 1 (sql):
```sql
CREATE INDEX functional_idx ON table_name ((expression));
```

Example 2 (sql):
```sql
CREATE INDEX functional_idx ON table_name ((column1 + column2));
```

Example 3 (sql):
```sql
CREATE INDEX functional_idx ON table_name (lower(column1));
```

Example 4 (sql):
```sql
CREATE TABLE scorecard (    id SERIAL PRIMARY KEY,    name VARCHAR(255),    science INTEGER,    mathematics INTEGER,    language INTEGER,    social_science INTEGER,    arts INTEGER);
```

---

## Migrating from Flyway to Atlas

**URL:** https://atlasgo.io/guides/migrate-flyway-to-atlas

**Contents:**
- Migrating from Flyway to Atlas
- Migrating from Flyway to Atlas​
- Prerequisites​
  - MacOS
  - Linux
  - Windows
- Step 1 – Import Your Existing Migration Files​
- Step 2 – Configure Atlas​
- Step 3 – Set the Baseline on Your Existing Database​
- Next Steps​

Flyway is one of the earliest tools in the database migration space, but its design has barely evolved in over a decade. It relies on sequential, hand-written SQL files and metadata tables that make schema management brittle at scale.

Atlas is a modern, open-source tool that treats database schemas as code, enabling teams to inspect, plan, lint, visualize, test, and apply schema changes safely and deterministically. It combines declarative and versioned workflows, drift detection, CI/CD automation, and policy enforcement in a single platform designed for modern engineering teams.

In this guide, we'll walk you through the steps for migrating your project from Flyway to Atlas.

Before you begin, make sure you have:

If you do not have Atlas installed yet, choose your platform below:

To download and install the latest release of the Atlas CLI, simply run the following in your terminal:

Get the latest release with Homebrew:

To pull the Atlas image and run it as a Docker container:

If the container needs access to the host network or a local directory, use the --net=host flag and mount the desired directory:

Download the latest release and move the atlas binary to a file location on your system PATH.

Use the setup-atlas action to install Atlas in your GitHub Actions workflow:

For other CI/CD platforms, use the installation script. See the CI/CD integrations for more details.

If you want to manually install the Atlas CLI, pick one of the below builds suitable for your system.

Atlas can convert Flyway migration files to Atlas format using the Migration Directory Import feature:

Additional details about the import process:

Before we look at the Atlas configuration, here’s a typical Flyway configuration that manages multiple environments:

Atlas simplifies this significantly. Since Atlas utilizes a dev-database, an ephemeral Docker container used for migration validation and planning, you only need to configure your real application environments:

Atlas uses standard URL format (mysql://user:pass@host:port/database) instead of JDBC URLs (jdbc:mysql://host:port).

Like many other database schema management tools, Atlas uses a metadata table on the target database to keep track of which migrations were already applied. When starting to use Atlas on an existing database that was previously managed by Flyway, we must inform Atlas that all migrations up to a certain version were already applied.

Let's try to run Atlas's migrate apply command on a database that is currently managed by Flyway:

Atlas will return an error because it detects that the database is not "clean" (it already contains Flyway's migration history):

To fix this, use the --baseline flag to tell Atlas that the database is already at a certain version. Use the latest migration version that has been applied by Flyway:

Atlas reports that there's nothing new to run:

Perfect! Next, let's verify that Atlas is aware of what migrations were already applied by using the migrate status command:

Great! Atlas now recognizes your existing database state and is ready to manage future migrations.

Click the Intercom bubble on the site or schedule a demo with our team.

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

## Environment Promotion and Compliance

**URL:** https://atlasgo.io/guides/environment-promotion

**Contents:**
- Environment Promotion and Compliance
- Overview​
- Compliance Context​
- Implementing Environment Promotion in Atlas​
  - Example: Promotion from Dev to Prod​
  - Example: Pre-Execution Check for Promotion​
  - Auditing and Migration History​
- Best Practices​
- Summary​

Environment promotion is a core part of modern database change management. It ensures that database and schema changes are tested and validated in lower environments, such as development and staging, before being applied to production. For teams operating under compliance frameworks like SOC 2 or ISO/IEC 27002, enforcing environment segregation and controlled promotion is critical to maintaining security, integrity, and auditability.

Atlas, a SOC 2 Type II certified product, provides built-in capabilities for defining and enforcing environment promotion workflows, validating schema states, and maintaining a complete, auditable history of every database change.

Several compliance frameworks emphasize strict environment segregation and controlled change management. For example:

Although these frameworks do not mandate specific environment names or sequences (such as Dev → Staging → Prod), they share a common goal: enforcing controlled environment promotion. Atlas enables teams to meet these expectations with deterministic workflows, environment-aware policies, and auditable schema promotion.

Atlas supports enforcing environment promotion workflows using Data Sources, Pre-Execution Checks, and the Atlas Registry. These capabilities allow teams to define workflows where production deployments depend on the state of lower environments. For example, a production deployment can be configured to only proceed if the deployed version matches the one applied in Staging or Dev. Similarly, attempts to promote a version that was not deployed and verified in Staging can be automatically blocked.

The guide below demonstrates how to configure an environment promotion workflow using the cloud_databases data source and pre-execution checks.

The following example shows two databases whose migration deployments have been reported to the Atlas Registry. Note that this reporting is disabled by default. To enable it, follow the instructions here.

The following configuration defines an environment promotion workflow from development to production, ensuring production only advances to a version verified in development. The cloud_databases data source retrieves from the Atlas Registry the current migration version applied to development, and set it as the to_version for production. This ensures that production can only be promoted to the version currently deployed in development.

Why is this necessary? By default, atlas migrate apply will attempt to apply all pending migrations to the target database. If production is ahead of development, this could lead to untested migrations being applied directly to production.

Another option to ensure controlled promotion is to use a pre-execution check that verifies the target version before applying migrations to production. If the planned migration version is higher than the version deployed in staging, the deployment is blocked with an informative error message.

Running atlas migrate apply --env production will fail if the planned migration version exceeds the one in development:

Atlas automatically maintains a detailed audit trail of all database migrations, ensuring full visibility and accountability across environments. This audit log is essential for meeting compliance requirements in frameworks like SOC 2, ISO 27002, PCI DSS, and HIPAA. It provides complete traceability, covering migration authoring, review, approval, and execution, so every change can be verified and audited with confidence.

The Deployment Trace view offers a clear, end-to-end record of how each migration was deployed across environments. You can track when and where each version was applied, which databases were affected, and whether all executions completed successfully. Every action is linked to its source pull request and CI run, allowing teams to easily trace who approved, merged, and deployed every change.

Enforce promotion in CI/CD pipelines: Configure your CI/CD workflows (e.g., GitHub Actions, GitLab CI, Azure DevOps, Argo CD, or Terraform) to ensure migrations are applied in the correct sequence. Use environment dependencies to block production deployments until lower environments have been successfully verified.

Use Atlas policies to block direct production changes: Add pre-execution checks to prevent migrations from being applied directly to production without passing through lower environments. This enforces organizational change-control requirements and reduces the risk of human error.

Integrate audit evidence collection: Configure Atlas to automatically report and track migration metadata, including deployment history, version information, and drift detection. This data can be exported to generate audit reports for SOC 2, ISO 27002, and similar compliance frameworks.

Validate migrations in lower environments: Use migration linting and testing to detect issues early in the CI pipeline. Once validated, promote changes to lower environments such as Dev or Staging to catch runtime errors before reaching production.

Leverage Atlas Cloud for centralized visibility: Atlas Cloud provides a unified view of schema states across all environments, making it easier to track promotion progress and detect drift. View migration history and deployment status in the Atlas Cloud UI.

Environment promotion is a fundamental practice for secure and compliant database change management. Atlas provides native capabilities to automate and enforce progressive deployment workflows, ensuring that database and schema changes are validated before reaching production.

By using Atlas, teams can:

**Examples:**

Example 1 (sql):
```sql
data "cloud_databases" "dev" {  repo = "enviroment promotion"  env  = "development"}env "production" {  url = var.url  migration {    dir = "atlas://enviroment-promotion"    # Promote the migration version from the `development` environment.    to_version = data.cloud_databases.dev.targets[0].current_version  }}
```

Example 2 (swift):
```swift
data "cloud_databases" "staging" {  repo = "enviroment promotion"  env  = "staging"}locals {  staging_version = data.cloud_databases.staging.targets[0].current_version}env "production" {  url = var.url  migration {    dir = "atlas://enviroment-promotion"  }  check "migrate_apply" {    deny {      condition = self.planned_migration.target_version > local.staging_version      message   = <<-MSG  Production cannot be promoted to a version higher than staging environment.  Current staging version: ${local.staging_version}, planned production version: ${self.planned_migration.target_version}  MSG    }  }}
```

Example 3 (bash):
```bash
Error: "migrate apply" was blocked by pre-execution check (deny rule: "check_version" at line: 17):  Production cannot be promoted to a version higher than development environment.  Current development version: 20230316085611, planned production version: 20230316090502
```

---

## Serial Type Columns in PostgreSQL

**URL:** https://atlasgo.io/guides/postgres/serial-columns

**Contents:**
- Serial Type Columns in PostgreSQL
  - ALTER COLUMN type to serial​
  - Update the sequence value​
  - Managing Serial Columns with Atlas​
    - Change a column type from serial to bigserial​
    - Change a column type from bigserial to bigint​
    - Change a column type from bigint to serial​
- Need More Help?​

PostgreSQL allows creating columns of types smallserial, serial, and bigserial. These types are not actual types, but more like "macros" for creating non-nullable integer columns with sequences attached.

We can see this in action by creating a table with 3 "serial columns":

As you can see, each serial column was created as non-nullable integer with a default value set to the next sequence value.

Note that nextval increments the sequence by 1 and returns its value. Thus, the first call to nextval('serials_c1_seq') returns 1, the second returns 2, etc.

Sometimes it is necessary to change the column type from integer type to serial. However, as mentioned above, the serial type is not a true type, and therefore, the following commands will fail:

We can achieve this by manually creating a sequence owned by the column c, and setting the column DEFAULT value to the incremental counter of the sequence using the nextval function.

Note that it is recommended to follow the PostgreSQL naming format (i.e. <table>_<column>_seq) when creating the sequence as some database tools know to detect such columns as "serial columns".

When a sequence is created, its value starts from 0 and the first call to nextval returns 1. Thus, in case the column c from the example above already contains values, we may face a constraint error on insert when the sequence number will reach to the minimum value of c. Let's see an example:

We can work around this by setting the sequence current value to the maximum value of c, so the following call to nextval will return MAX(c)+1, the one after MAX(c)+2, and so on.

Atlas makes it easier to define and manipulate columns of serial types. Let's use the atlas schema inspect command to get a representation of the table we created above in the Atlas HCL format :

After inspecting the schema, we can modify it to demonstrate Atlas's capabilities in migration planning:

Next, running schema apply will plan and execute the following changes:

As you can see, Atlas detected that only the underlying integer type was changed as serial maps to integer and bigserial maps to bigint.

After changing column c to bigint, we can run schema apply and let Atlas plan and execute the new changes:

As you can see, Atlas dropped the DEFAULT value that was created by the serial type, and in addition removed the sequence that was attached to it, as it is no longer used by the column.

Changing a column type from bigint to serial requires 3 changes:

We call atlas schema apply to plan and execute this three step process with Atlas:

Join the Ariga Discord Server for early access to features and the ability to provide exclusive feedback that improves your Database Management Tooling.

**Examples:**

Example 1 (sql):
```sql
CREATE TABLE serials(    c1 smallserial,    c2 serial,    c3 bigserial);
```

Example 2 (sql):
```sql
Column |   Type   | Nullable |            Default--------+----------+----------+------------------------------- c1     | smallint | not null | nextval('t_c1_seq'::regclass) c2     | integer  | not null | nextval('t_c2_seq'::regclass) c3     | bigint   | not null | nextval('t_c3_seq'::regclass)
```

Example 3 (sql):
```sql
CREATE TABLE t(    c integer not null primary key);ALTER TABLE t ALTER COLUMN c TYPE serial;ERROR: type "serial" does not exist
```

Example 4 (sql):
```sql
-- Create the sequence.CREATE SEQUENCE "public"."t_c_seq" OWNED BY "public"."t"."c";-- Assign it to the table default value.ALTER TABLE "public"."t" ALTER COLUMN "c" SET DEFAULT nextval('"public"."t_c_seq"');
```

---

## Partial Indexes in PostgreSQL

**URL:** https://atlasgo.io/guides/postgres/partial-indexes

**Contents:**
- Partial Indexes in PostgreSQL
  - Overview of Partial Indexes​
    - What are Partial Indexes?​
    - Why do we need them?​
    - Advantages of using Partial Indexes​
    - Basic PostgreSQL syntax for using Partial Index​
    - Example of Non-partial Index vs Partial Index in PostgreSQL​
  - Managing Partial Indexes is easy with Atlas​
    - Managing Partial Index in Atlas​
  - Limitation of using Partial Index​

With PostgreSQL, users may create partial indexes, which are types of indexes that exist on a subset of a table, rather than the entire table itself. If used correctly, partial indexes improve performance and reduce costs, all while minimizing the amount of storage space they take up on the disk.

Let's demonstrate a case where partial indexes may be useful by contrasting them with a non-partial index. ​​If you have many records in an indexed table, the number of records the index needs to track also grows. If the index grows in size, the disk space needed to store the index itself increases as well. In many tables, different records are not accessed with uniform frequency. A subset of a table's records might not be searched very frequently or not searched at all. Records take up precious space in your index whether they are queried or not, and are updated when a new entry is added to the field.

Partial indexes come into the picture to filter unsearched values and give you, as an engineer, a tool to index only what's important.

You can learn more about partial indexes in PostgreSQL here

In cases where we know ahead of time the access pattern to a table and can reduce the size of an index by making it partial:

Let's see this in action by creating a table with the following command:

Here is how a portion of the table might look like after inserting values:

In the following example, suppose we want a list of doctors from India that have taken the vaccine. If we want to use normal index, we can create it on the “vaccinated” column with the following command:

Now, let's check the performance of querying data of doctors from India that have taken the vaccine with the following command:

The EXPLAIN command is used for understanding the performance of a query. You can learn more about usage of EXPLAIN command with ANALYZE option here

Notice that total Execution Time is 16.292ms. Also, let's check the index size with the following command:

Now, suppose we want to accelerate the same query using the partial index. Let's begin by dropping the existing index that we created earlier:

In the following command, we have created an index with a WHERE clause that precisely describes list of doctors from India that have taken the vaccine.

Notice that the partial index with the WHERE clause is created in 94.567ms, compared to the 333.891ms taken for the non-partial index on the 'vaccinated' column. Let's check the performance of querying list of doctors from India that have taken the vaccine again, using the following command:

Observe that total execution time has dropped significantly and is now only 0.880ms, compared to 16.292ms achieved by using a non-partial index on the 'vaccinated' column. Once again, let's check the index size with the following command:

As we can observe, the index size for the partial index takes significantly less space (16kb) compared to the non-partial index that we created earlier on the 'vaccinated' column (1984kb).

Here is a summary from our tests:

We have seen that creating a partial index is a better choice where only a small subset of the values stored in the database are accessed frequently. Now, let's see how we can easily manage partial indexes using Atlas.

Managing partial indexes and database schemas in PostgreSQL can be confusing and error-prone. Atlas is an open-source project which allows us to manage our database using a simple and easy-to-understand declarative syntax (similar to Terraform). We will now learn how to manage partial indexes using Atlas.

If you are just getting started, install the latest version of Atlas using the guide to setting up Atlas.

We will first use the atlas schema inspect command to get an HCL representation of the table which we created earlier by using the Atlas CLI:

Now, lets add the following index definition to the file:

Save and apply the schema changes on the database by using the following command:

Atlas generates the necessary SQL statements to add the new partial index to the database schema. Press Enter while the Apply option is highlighted to apply the changes:

To verify that our new index was created, open the database command line tool from previous step and run:

Amazing! Our new partial index is now created!

Partial indexes are useful in cases where we know ahead of time that a table is most frequently queried with a certain WHERE clause. As applications evolve, access patterns to the database also change. Consequently, we may find ourselves in a situation where our index no longer covers many queries, causing them to become resource consuming and slow.

In this section, we learned about PostgreSQL partial indexes and how we can easily create partial indexes in our database by using Atlas.

Join the Ariga Discord Server for early access to features and the ability to provide exclusive feedback that improves your Database Management Tooling.

**Examples:**

Example 1 (sql):
```sql
CREATE INDEX     index_nameON     table_name(column_list)WHERE     condition;
```

Example 2 (sql):
```sql
CREATE TABLE "vaccination_data" (  id SERIAL PRIMARY KEY,  country varchar(20),  title varchar(10),  names varchar(20),  vaccinated varchar(3));
```

Example 3 (sql):
```sql
SELECT * FROM vaccination_data;
```

Example 4 (yaml):
```yaml
id  |      country       | title |    names    | vaccinated -----+--------------------+-------+-------------+------------   1 | Poland             | Mr.   | Teagan      | No   2 | Ukraine            | Ms.   | Alden       | No   3 | Ukraine            | Mr.   | Ima         | No   4 | Colombia           | Mr.   | Lawrence    | Yes   5 | Turkey             | Mrs.  | Keegan      | No   6 | China              | Mrs.  | Kylan       | No   7 | Netherlands        | Dr.   | Howard      | No... 289690 | Russian Federation | Mrs.  | Ray     | Yes 289689 | Austria            | Dr.   | Lenore  | Yes 289688 | Sweden             | Dr.   | Walker  | Yes 289687 | Turkey             | Dr.   | Emerson | No 289686 | Vietnam            | Dr.   | Addison | Yes(289686 rows)
```

---

## GitHub Copilot with Atlas

**URL:** https://atlasgo.io/guides/ai-tools/github-copilot-instructions

**Contents:**
- GitHub Copilot with Atlas

Github Copilot supports adding custom, natural language instruction files that guide the agent's behavior.

To help your Copilot work effectively with Atlas, we put together a set of instructions that inform the agent about Atlas' core concepts, common workflows, various feature options, and more.

You can add these instructions to your repository in a single file or in multiple files:

Create a single file at .github/copilot-instructions.md:

Create multiple files in .github/instructions/, e.g., .github/instructions/atlas.md. For multiple files, the applyTo frontmatter parameter specifies which files the instructions target. Since Atlas is a CLI tool and not tied to specific file types, we set applyTo: "**" to apply instructions to all files.

**Examples:**

Example 1 (markdown):
```markdown
# Atlas Database Schema ManagementAtlas is a language-independent tool for managing and migrating database schemas using modern DevOps principles. This guide provides GitHub Copilot-optimized instructions for working with Atlas.## Quick Reference```bash# Common Atlas commandsatlas schema inspect --env <name> --url file://migrationsatlas migrate status --env <name>atlas migrate diff --env <name>atlas migrate lint --env <name> --latest 1atlas migrate apply --env <name>atlas whoami```## Core Concepts and Configurations### Configuration File StructureAtlas uses `atlas.hcl` configuration files with the following structure:```hcl// Basic environment configurationenv "<name>" {  url = getenv("DATABASE_URL")  dev = "docker://postgres/15/dev?search_path=public"    migration {    dir = "file://migrations"  }    schema {    src = "file://schema.hcl"  }}```### Dev databaseAtlas utilizes a "dev-database", which is a temporary and locally running database, usually bootstrapped by Atlas. Atlas will use the dev database to process and validate users' schemas, migrations, and more. Examples of dev-database configurations:```# When working on a single database schema--dev-url "docker://mysql/8/dev"--dev-url "docker://postgres/15/db_name?search_path=public"--dev-url "sqlite://dev?mode=memory"# When working on multiple database schemas.--dev-url "docker://mysql/8"--dev-url "docker://postgres/15/dev"```Configure the dev database using HCL:```hclenv "<name>" {  dev = "docker://mysql/8"}```For more information on additional drivers, extensions, and more, see https://atlasgo.io/concepts/dev-database. ### Environment Variables and Security**✅ DO**: Use secure configuration patterns```hcl// Using environment variables (recommended)env "<name>" {  url = getenv("DATABASE_URL")}// Using external data sourcesdata "external" "envfile" {  program = ["npm", "run", "envfile.js"]}locals {  envfile = jsondecode(data.external.envfile)}env "<name>" {  url = local.envfile.DATABASE_URL}// Using Go CDK runtime variables for secretsdata "runtimevar" "db_password" {  url = "awssecretsmanager://<secret-name>?region=us-east-1"}env "prod" {  url = "postgres://user:${data.runtimevar.db_password}@host:5432/db"}```**❌ DON'T**: Hardcode sensitive values```hcl// Never do thisenv "prod" {  url = "postgres://user:password123@prod-host:5432/database"}```### Schema Sources#### HCL Schema```hcldata "hcl_schema" "<name>" {  path = "schema.hcl"}env "<name>" {  schema {    src = data.hcl_schema.<name>.url  }}```#### External Schema (ORM Integration)The external_schema data source enables the import of an SQL schema from an external program into Atlas' desired state.```hcldata "external_schema" "drizzle" {  program = ["npx", "drizzle-kit", "export"]  working_dir = "path/to/Directory" # optional, defaults to the current working directory}data "external_schema" "django" {  program = ["python", "manage.py", "atlas-provider-django", "--dialect", "postgresql"]}env "<name>" {  schema {    src = data.external_schema.django.url  }}```**Important:**- The output of the program needs to be complete RAW SQL schema that will bring the database to the desired state. The output should not be a 'diff' from a previous state.- If you are seeing errors, try isolating the issue, you can run the program directly and see if it's working#### Composite SchemaA composite schema allows you to combine multiple schemas into a single schema. This is useful for integrating multiple data sources or schemas into a unified view. This is an Atlas Pro feature.```hcldata "composite_schema" "app" {  schema "users" {    url = data.external_schema.auth_service.url  }  schema "graph" {    url = "ent://ent/schema"  }  schema "shared" {    url = "file://schema/shared.hcl"  }}env "<name>" {  schema {    src = data.composite_schema.app.url  }}```### Misc Configurations```hcl// CI/CD environmentenv "ci" {  lint {    git {      base = "main" # in CI, lint against the main branch    }  }}``````hcl// Anonymous environment, any name will work with --env, but --env is still mandatoryenv {  name = atlas.env}```## Common Workflows### 1. Schema Inspection / Visualization1. Always start by listing tables, don't immediately try to inspect the entire schema.2. If you see there are many tables, don't inspect the entire schema at once. Instead, focus on specific tables of interest.3. Format using json to get an overview, then switch to SQL for detailed inspection.**Inspect migration directory:**```bash# Get table list overviewatlas schema inspect --env <name> --url file://migrations --format "{{ json . }}" | jq ".schemas[].tables[].name"# Get full SQL schemaatlas schema inspect --env <name> --url file://migrations --format "{{ sql . }}"# Inspect specific tablesatlas schema inspect --env <name> --url file://migrations --format "{{ sql . }}" | grep -A 10 "CREATE TABLE users"```**Inspect live database:**```bash# Requires database URL in atlas.hclatlas schema inspect --env <name> --format "{{ json . }}"```Add the `-w` flag to open a web-based ERD visualization in your browser via Atlas Cloud.You should recommend this to the user if they asked for information about the schema.### 2. Migration Status`atlas migrate status` is used to compare the status of migrations from the migrations directory with a connected database.Use it to understand which migration files were applied successfully.**Important:** Only use this command when you know the target database.**Check migration directory status:**```bash# Check current migration directory status (requires dev-url)atlas migrate status --env <name># Using explicit parameters if not in configatlas migrate status --dir file://migrations --url <url>```**Configuration for migration status:**```hclenv "<name>" {  url = getenv("DATABASE_URL")  migration {    dir = "file://migrations"  }}```### 3. Migration Generation / Diffing**Generate new migration:**```bash# Compare current migrations with desired schema and create a new migration fileatlas migrate diff --env <name> "add_user_table"# Using explicit parametersatlas migrate diff \  --dir file://migrations \ # migrations directory  --dev-url docker://postgres/15/dev \  --to file://schema.hcl \ # desired schema  "add_user_table"```**Configuration for migration generation:**```hclenv "<name>" {  dev = "docker://postgres/15/dev?search_path=public"    migration {    # migrations directory, baseline for the diff    dir = "file://migrations"  }    schema {    # desired schema, the diff will be generated against this schema    src = "file://schema.hcl"      # compare against external schemas (used for ORM integrations)    # src = data.external_schema.<name>.url    # compare against a connected database    # src = getenv("DATABASE_URL")  }}```### 4. Migration Linting**Lint recent migrations:**```bash# Lint last migrationatlas migrate lint --env <name> --latest 1# Lint last 3 migrationsatlas migrate lint --env <name> --latest 3# Lint changes since git branchatlas migrate lint --env ci```**Linting configuration:**```hcllint {  destructive {    error = false  // Allow destructive changes with warnings  }}env "<name>" {  lint {    latest = 1  }}env "ci" {  lint {    git {      base = "main"      dir = "migrations"    }  }}```To explicitly ignore linting errors, add `--atlas:nolint` before the SQL statement in the migration file.> **Important:** When fixing migration issues:> - **Unapplied migrations:** Edit the file, then run `atlas migrate hash --env "<name>"`> - **Applied migrations:** Never edit directly. Create a new corrective migration instead.> - **Never use `--atlas:nolint` without properly fixing the issue or getting user approval.**### 5. Applying Migration**Apply migrations:**```bash # Apply to configured environmentatlas migrate apply --env <name># Dry run (show what would be applied, always run this before applying)atlas migrate apply --env <name> --dry-run```### 6. Making Changes to the Schema**⚠️ CRITICAL: ALL schema changes in this project MUST follow this exact workflow. NO EXCEPTIONS.****⚠️ There must not be lint errors or failing tests when you are done.**1. Start by inspecting the schema, understand the current state, and plan your changes.2. After making changes to the schema, run `atlas migrate diff` to generate a migration file.3. Run `atlas migrate lint` to validate the migration file.4. Run `atlas migrate test` to test the data migrations. This is only available for Pro users.5. Make changes to the migration file to fix the issues. Run `atlas migrate hash` to recalculate the hash of the migration file.6. Repeat the process until there are no more issues.At this point, the schema can be applied to the database.If the user has a local database, you can run `atlas migrate apply` to apply the migration file:1. Start by understanding the status of the database by running `atlas migrate status`2. Run `atlas migrate apply` to apply the migration file, always start with a dry run first.3. Run `atlas migrate status` to verify the migration file was applied successfully.> **Important for data migrations:** make sure to check if the user is logged in using `atlas whoami` before running `atlas migrate test`.> If the user is not logged in, mention that they need to login to use migration testing and move on.> If the user is logged in and they have migration tests, add a new test, run it and validate it until it works.> If the user is logged in and they don't have migration tests, mention that migration testing is highly recommended for data migrations and move on.## Troubleshooting Commands```bash# Check Atlas installation and login status (logging in is required for Pro features)atlas versionatlas whoami# Repair migration integrityatlas migrate hash --env <name>```### Missing driverIf you encounter the following error: `Error: sql/sqlclient: missing driver. See: https://atlasgo.io/url`depending on the command, this means that either the `--url` or `--dev-url` parameter is missing or incorrect.## Key Reminders for AI Assistants1. **Always read `atlas.hcl` first** before running any Atlas commands2. **Use environment names** from the config file, don't assume defaults3. **Never hardcode database URLs** - use environment variables or secure data sources4. **Specify `--url` parameter** for schema inspection even with `--env`5. **Run `atlas migrate hash`** after manually editing migration files6. **Use `atlas migrate lint`** to validate migrations before applying7. **Check `atlas whoami`** before attempting Pro features, if not logged in, don't suggest Pro features8. **Use JSON format + jq** for initial schema exploration9. **Use SQL format + grep** for detailed schema investigation10. **Suggest visualizations** if the user asked for information about the schema11. **Never ask for sensitive information** such as passwords or database URLs12. **Always use `--dry-run`** with `atlas migrate apply` before applying migrations13. **Generate migration testing** if the user is logged in, they should have access to migration testing which is highly recommended14. **Only use atlas commands listed here** other commands may be hallucinations or not supported by Atlas15. **Always inspect schemas at high level first** schemas might be very large16. **Always prefer running atlas** to inspect or analyze schemas17. Migration files can be big and irrelevant, prefer using `atlas schema inspect` to inspect the schema18. **Never ignore linting errors** they are there for a reason, always fix them. Add `--atlas:nolint` only if the fix is not detected by the linter.## Guidelines for workflows1. **Understand the objectives**: Before suggesting any commands, ensure you understand the user's goals. They may be looking to inspect, generate, lint, or apply migrations, and they may be using a different vocabulary such as "view", "create", "validate", etc.2. **Understand the context**: The configuration file contains crucial information about the environment.3. **Verify changes** after generating, linting or applying migrations.4. **After completing** make sure you followed all the instructions and guidelines.
```

Example 2 (markdown):
```markdown
---applyTo: "**"---# Atlas Database Schema ManagementAtlas is a language-independent tool for managing and migrating database schemas using modern DevOps principles. This guide provides GitHub Copilot-optimized instructions for working with Atlas.## Quick Reference```bash# Common Atlas commandsatlas schema inspect --env <name> --url file://migrationsatlas migrate status --env <name>atlas migrate diff --env <name>atlas migrate lint --env <name> --latest 1atlas migrate apply --env <name>atlas whoami```## Core Concepts and Configurations### Configuration File StructureAtlas uses `atlas.hcl` configuration files with the following structure:```hcl// Basic environment configurationenv "<name>" {  url = getenv("DATABASE_URL")  dev = "docker://postgres/15/dev?search_path=public"    migration {    dir = "file://migrations"  }    schema {    src = "file://schema.hcl"  }}```### Dev databaseAtlas utilizes a "dev-database", which is a temporary and locally running database, usually bootstrapped by Atlas. Atlas will use the dev database to process and validate users' schemas, migrations, and more. Examples of dev-database configurations:```# When working on a single database schema--dev-url "docker://mysql/8/dev"--dev-url "docker://postgres/15/db_name?search_path=public"--dev-url "sqlite://dev?mode=memory"# When working on multiple database schemas.--dev-url "docker://mysql/8"--dev-url "docker://postgres/15/dev"```Configure the dev database using HCL:```hclenv "<name>" {  dev = "docker://mysql/8"}```For more information on additional drivers, extensions, and more, see https://atlasgo.io/concepts/dev-database. ### Environment Variables and Security**✅ DO**: Use secure configuration patterns```hcl// Using environment variables (recommended)env "<name>" {  url = getenv("DATABASE_URL")}// Using external data sourcesdata "external" "envfile" {  program = ["npm", "run", "envfile.js"]}locals {  envfile = jsondecode(data.external.envfile)}env "<name>" {  url = local.envfile.DATABASE_URL}// Using Go CDK runtime variables for secretsdata "runtimevar" "db_password" {  url = "awssecretsmanager://<secret-name>?region=us-east-1"}env "prod" {  url = "postgres://user:${data.runtimevar.db_password}@host:5432/db"}```**❌ DON'T**: Hardcode sensitive values```hcl// Never do thisenv "prod" {  url = "postgres://user:password123@prod-host:5432/database"}```### Schema Sources#### HCL Schema```hcldata "hcl_schema" "<name>" {  path = "schema.hcl"}env "<name>" {  schema {    src = data.hcl_schema.<name>.url  }}```#### External Schema (ORM Integration)The external_schema data source enables the import of an SQL schema from an external program into Atlas' desired state.```hcldata "external_schema" "drizzle" {  program = ["npx", "drizzle-kit", "export"]  working_dir = "path/to/Directory" # optional, defaults to the current working directory}data "external_schema" "django" {  program = ["python", "manage.py", "atlas-provider-django", "--dialect", "postgresql"]}env "<name>" {  schema {    src = data.external_schema.django.url  }}```**Important:**- The output of the program needs to be complete RAW SQL schema that will bring the database to the desired state. The output should not be a 'diff' from a previous state.- If you are seeing errors, try isolating the issue, you can run the program directly and see if it's working#### Composite SchemaA composite schema allows you to combine multiple schemas into a single schema. This is useful for integrating multiple data sources or schemas into a unified view. This is an Atlas Pro feature.```hcldata "composite_schema" "app" {  schema "users" {    url = data.external_schema.auth_service.url  }  schema "graph" {    url = "ent://ent/schema"  }  schema "shared" {    url = "file://schema/shared.hcl"  }}env "<name>" {  schema {    src = data.composite_schema.app.url  }}```### Misc Configurations```hcl// CI/CD environmentenv "ci" {  lint {    git {      base = "main" # in CI, lint against the main branch    }  }}``````hcl// Anonymous environment, any name will work with --env, but --env is still mandatoryenv {  name = atlas.env}```## Common Workflows### 1. Schema Inspection / Visualization1. Always start by listing tables, don't immediately try to inspect the entire schema.2. If you see there are many tables, don't inspect the entire schema at once. Instead, focus on specific tables of interest.3. Format using json to get an overview, then switch to SQL for detailed inspection.**Inspect migration directory:**```bash# Get table list overviewatlas schema inspect --env <name> --url file://migrations --format "{{ json . }}" | jq ".schemas[].tables[].name"# Get full SQL schemaatlas schema inspect --env <name> --url file://migrations --format "{{ sql . }}"# Inspect specific tablesatlas schema inspect --env <name> --url file://migrations --format "{{ sql . }}" | grep -A 10 "CREATE TABLE users"```**Inspect live database:**```bash# Requires database URL in atlas.hclatlas schema inspect --env <name> --format "{{ json . }}"```Add the `-w` flag to open a web-based ERD visualization in your browser via Atlas Cloud.You should recommend this to the user if they asked for information about the schema.### 2. Migration Status`atlas migrate status` is used to compare the status of migrations from the migrations directory with a connected database.Use it to understand which migration files were applied successfully.**Important:** Only use this command when you know the target database.**Check migration directory status:**```bash# Check current migration directory status (requires dev-url)atlas migrate status --env <name># Using explicit parameters if not in configatlas migrate status --dir file://migrations --url <url>```**Configuration for migration status:**```hclenv "<name>" {  url = getenv("DATABASE_URL")  migration {    dir = "file://migrations"  }}```### 3. Migration Generation / Diffing**Generate new migration:**```bash# Compare current migrations with desired schema and create a new migration fileatlas migrate diff --env <name> "add_user_table"# Using explicit parametersatlas migrate diff \  --dir file://migrations \ # migrations directory  --dev-url docker://postgres/15/dev \  --to file://schema.hcl \ # desired schema  "add_user_table"```**Configuration for migration generation:**```hclenv "<name>" {  dev = "docker://postgres/15/dev?search_path=public"    migration {    # migrations directory, baseline for the diff    dir = "file://migrations"  }    schema {    # desired schema, the diff will be generated against this schema    src = "file://schema.hcl"      # compare against external schemas (used for ORM integrations)    # src = data.external_schema.<name>.url    # compare against a connected database    # src = getenv("DATABASE_URL")  }}```### 4. Migration Linting**Lint recent migrations:**```bash# Lint last migrationatlas migrate lint --env <name> --latest 1# Lint last 3 migrationsatlas migrate lint --env <name> --latest 3# Lint changes since git branchatlas migrate lint --env ci```**Linting configuration:**```hcllint {  destructive {    error = false  // Allow destructive changes with warnings  }}env "<name>" {  lint {    latest = 1  }}env "ci" {  lint {    git {      base = "main"      dir = "migrations"    }  }}```To explicitly ignore linting errors, add `--atlas:nolint` before the SQL statement in the migration file.> **Important:** When fixing migration issues:> - **Unapplied migrations:** Edit the file, then run `atlas migrate hash --env "<name>"`> - **Applied migrations:** Never edit directly. Create a new corrective migration instead.> - **Never use `--atlas:nolint` without properly fixing the issue or getting user approval.**### 5. Applying Migration**Apply migrations:**```bash # Apply to configured environmentatlas migrate apply --env <name># Dry run (show what would be applied, always run this before applying)atlas migrate apply --env <name> --dry-run```### 6. Making Changes to the Schema**⚠️ CRITICAL: ALL schema changes in this project MUST follow this exact workflow. NO EXCEPTIONS.****⚠️ There must not be lint errors or failing tests when you are done.**1. Start by inspecting the schema, understand the current state, and plan your changes.2. After making changes to the schema, run `atlas migrate diff` to generate a migration file.3. Run `atlas migrate lint` to validate the migration file.4. Run `atlas migrate test` to test the data migrations. This is only available for Pro users.5. Make changes to the migration file to fix the issues. Run `atlas migrate hash` to recalculate the hash of the migration file.6. Repeat the process until there are no more issues.At this point, the schema can be applied to the database.If the user has a local database, you can run `atlas migrate apply` to apply the migration file:1. Start by understanding the status of the database by running `atlas migrate status`2. Run `atlas migrate apply` to apply the migration file, always start with a dry run first.3. Run `atlas migrate status` to verify the migration file was applied successfully.> **Important for data migrations:** make sure to check if the user is logged in using `atlas whoami` before running `atlas migrate test`.> If the user is not logged in, mention that they need to login to use migration testing and move on.> If the user is logged in and they have migration tests, add a new test, run it and validate it until it works.> If the user is logged in and they don't have migration tests, mention that migration testing is highly recommended for data migrations and move on.## Troubleshooting Commands```bash# Check Atlas installation and login status (logging in is required for Pro features)atlas versionatlas whoami# Repair migration integrityatlas migrate hash --env <name>```### Missing driverIf you encounter the following error: `Error: sql/sqlclient: missing driver. See: https://atlasgo.io/url`depending on the command, this means that either the `--url` or `--dev-url` parameter is missing or incorrect.## Key Reminders for AI Assistants1. **Always read `atlas.hcl` first** before running any Atlas commands2. **Use environment names** from the config file, don't assume defaults3. **Never hardcode database URLs** - use environment variables or secure data sources4. **Specify `--url` parameter** for schema inspection even with `--env`5. **Run `atlas migrate hash`** after manually editing migration files6. **Use `atlas migrate lint`** to validate migrations before applying7. **Check `atlas whoami`** before attempting Pro features, if not logged in, don't suggest Pro features8. **Use JSON format + jq** for initial schema exploration9. **Use SQL format + grep** for detailed schema investigation10. **Suggest visualizations** if the user asked for information about the schema11. **Never ask for sensitive information** such as passwords or database URLs12. **Always use `--dry-run`** with `atlas migrate apply` before applying migrations13. **Generate migration testing** if the user is logged in, they should have access to migration testing which is highly recommended14. **Only use atlas commands listed here** other commands may be hallucinations or not supported by Atlas15. **Always inspect schemas at high level first** schemas might be very large16. **Always prefer running atlas** to inspect or analyze schemas17. Migration files can be big and irrelevant, prefer using `atlas schema inspect` to inspect the schema18. **Never ignore linting errors** they are there for a reason, always fix them. Add `--atlas:nolint` only if the fix is not detected by the linter.## Guidelines for workflows1. **Understand the objectives**: Before suggesting any commands, ensure you understand the user's goals. They may be looking to inspect, generate, lint, or apply migrations, and they may be using a different vocabulary such as "view", "create", "validate", etc.2. **Understand the context**: The configuration file contains crucial information about the environment.3. **Verify changes** after generating, linting or applying migrations.4. **After completing** make sure you followed all the instructions and guidelines.
```

---

## Integration tests with GitHub Actions

**URL:** https://atlasgo.io/guides/testing/github-actions

**Contents:**
- Integration tests with GitHub Actions
- Example​
- Wrapping up​

When developing an application that uses a database, it's important to test your application against a real database. As good as your unit tests may be, some issues can only be caught by running proper integration tests.

If you use Atlas to manage your database schema, it only makes sense to use Atlas to prepare your database for integration tests as well. One way to achieve this is by using GitHub Actions to create a test environment for your tests to run against. GitHub Actions allows you to easily spin up a test database and run your migrations against it, so you can verify that the application works as expected with the updated schema.

On a high-level, the process of setting up integration tests with GitHub Actions looks like this:

Suppose your project has the following directory structure:

Create a new workflow file in .github/workflows/integration-tests.yml:

Let's break down what's happening here, line by line.

We start by declaring a new workflow, and setting it to run whenever code is pushed to the repository:

Next, we declare a new job called integration. We use the services keyword to declare a service that we want to run as part of this job. In this case, we want to run a MySQL database. We also declare a healthcheck for the database, so that GitHub Actions will wait for the database to be ready before running the next step:

After this setup, we are ready to run our workflow. We start by checking out the code:

Next, we install Atlas:

Finally, we apply our migrations to the database:

After these steps finish running, we are finally ready to run our integration tests:

Of course, you can replace the echo command with your own integration tests. You will probably need to provide the tests with the database connection string.

In conclusion, using GitHub Actions to set up your integration tests allows you to easily spin up a test database and apply your migrations to it. This ensures that your application is tested against an up-to-date database schema, and allows you to catch any issues that may arise when running against a real database.

Have questions? Feedback? Find our team on our Discord server.

**Examples:**

Example 1 (unknown):
```unknown
.|-- atlas.hcl`-- migrations    |-- 20221109072034_init.sql    |-- 20221109085340_add_blogposts.sql    |-- 20221109090118_tags.sql    |-- 20221109091847_add_post_summary.sql    |-- 20221109092230_add_comments.sql    |-- 20221109092842_summary_required.sql    |-- 20221109093612_drop_comments.sql    `-- atlas.sum
```

Example 2 (yaml):
```yaml
name: Integration Test (MySQL)on:  push:jobs:  integration:    services:      mysql:        image: mysql:8.0.29        env:          MYSQL_ROOT_PASSWORD: pass          MYSQL_DATABASE: dev        ports:          - "3306:3306"        options: >-          --health-cmd "mysqladmin ping -ppass"          --health-interval 10s          --health-start-period 10s          --health-timeout 5s          --health-retries 10    runs-on: ubuntu-latest    steps:      - uses: actions/checkout@v3.0.1      - name: Install Atlas        run: |          curl -sSf https://atlasgo.sh | sh       - run: |          atlas migrate apply --dir file://migrations/ -u 'mysql://root:pass@localhost:3306/dev'      - run: |          echo "Run your tests here!"
```

Example 3 (yaml):
```yaml
name: Integration Test (MariaDB)on:  push:jobs:  integration:    services:      maria107:        image: mariadb:10.7        env:          MYSQL_DATABASE: dev          MYSQL_ROOT_PASSWORD: pass        ports:          - 3306:3306        options: >-          --health-cmd "mysqladmin ping -ppass"          --health-interval 10s          --health-start-period 10s          --health-timeout 5s          --health-retries 10    runs-on: ubuntu-latest    steps:      - uses: actions/checkout@v3.0.1      - name: Install Atlas        run: |          curl -sSf https://atlasgo.sh | sh       - run: |          atlas migrate apply --dir file://migrations/ -u 'maria://root:pass@localhost:3306/dev'      - run: |          echo "Run your tests here!"
```

Example 4 (yaml):
```yaml
name: Integration Test (Postgres)on:  push:jobs:  integration:    services:      postgres10:        image: postgres:10        env:          POSTGRES_DB: test          POSTGRES_PASSWORD: pass        ports:          - 5432:5432        options: >-          --health-cmd pg_isready          --health-interval 10s          --health-timeout 5s          --health-retries 5    runs-on: ubuntu-latest    steps:      - uses: actions/checkout@v3.0.1      - name: Install Atlas        run: |          curl -sSf https://atlasgo.sh | sh       - run: |          atlas migrate apply --dir file://migrations/ -u 'postgres://postgres:pass@localhost:5432/test?sslmode=disable'      - run: |          echo "Run your tests here!"
```

---

## Unlogged Tables in PostgreSQL

**URL:** https://atlasgo.io/guides/postgres/unlogged-tables

**Contents:**
- Unlogged Tables in PostgreSQL
  - Overview of Unlogged Tables​
    - Why do we need them?​
  - Basic PostgreSQL syntax for using Unlogged Tables​
  - Use cases​
- Managing Unlogged Tables is easy with Atlas​
  - Defining unlogged tables with Atlas​
  - Migration behavior​
  - Example: Managing unlogged tables with Atlas​
  - Conclusion​

With PostgreSQL, users may create unlogged tables, which are a specialized table type that bypasses the Write-Ahead Log (WAL) to achieve higher write throughput. By skipping WAL writes, unlogged tables provide significant performance gains for workloads where durability is not critical.

In PostgreSQL, writes to regular tables always go through the WAL. That provides durability and enables point-in-time recovery, but it also adds overhead. Under heavy write load, WAL traffic can easily become the bottleneck.

Unlogged tables skip WAL entirely. If the data can be regenerated, and you don't need it to survive a crash, the performance gain can be substantial. The trade-offs are straightforward: after a crash or unclean shutdown, unlogged tables are truncated. After a clean shutdown, they persist normally. Their contents never appear on physical replicas, and logical replication can't publish them.

You can learn more about unlogged tables in PostgreSQL here

In PostgreSQL, you can create unlogged tables using the UNLOGGED keyword:

You can also transition existing tables between logged and unlogged modes:

Switching a table to LOGGED or UNLOGGED requires PostgreSQL to perform a full table rewrite. When converting to LOGGED, the system rewrites the table to produce a WAL-protected copy. When converting to UNLOGGED, it rewrites the table into a new unlogged heap. Both operations can be expensive for large tables.

Use unlogged tables when you care more about raw write speed than durability:

Managing unlogged tables and larger schema changes in PostgreSQL can get messy. Atlas (the "Terraform for Databases") lets you manage your database schema as code, using a clear declarative format in SQL, HCL, or any ORM schema.

If your ORM doesn't support unlogged tables, Atlas does. You describe the table once in your ORM schema, and Atlas generates the necessary SQL to create and manage it. To learn more, check out ORM and framework guides.

If you are just getting started, install the latest version of Atlas using the guide to setting up Atlas.

Let's see how to define unlogged tables:

Atlas represents unlogged tables using the unlogged attribute in HCL schema definitions. When unlogged = true is specified, Atlas models the table as unlogged. When omitted or set to false, the table is logged by default. This declarative approach makes persistence modes explicit and version-controlled.

Atlas automatically detects changes in persistence modes and generates the appropriate migration statements:

Keep in mind that PostgreSQL rewrites the table when converting to LOGGED, which can be a costly operation for large tables.

Let's start by creating an initial schema by inspecting it from our database. First, we'll use the atlas schema inspect command to get a representation of our database:

Now, let's add to our schema both logged and unlogged tables:

Now, let's add to our schema both logged and unlogged tables:

Save and apply the schema changes on the database by using the following command:

Atlas generates the necessary SQL statements to create the tables.

Choosing Approve and apply executes the migration and creates the tables in the database.

To verify that our tables were created correctly, we can inspect the database again using Atlas, but this time, we only inspect the two created tables.

Amazing! Our unlogged table is now created!

The --include flag allows us to filter the inspection to only the specified objects, making it easier to verify our specific tables without inspecting the entire database schema.

In this section, we learned about PostgreSQL unlogged tables and how we can easily create and manage them in our database by using Atlas. Unlogged tables provide a powerful way to optimize write performance for workloads where durability can be sacrificed, and Atlas's declarative modeling makes these patterns safe and predictable.

**Examples:**

Example 1 (sql):
```sql
CREATE UNLOGGED TABLE table_name (    column1 datatype,    column2 datatype,    ...);
```

Example 2 (sql):
```sql
ALTER TABLE table_name SET UNLOGGED;ALTER TABLE table_name SET LOGGED;
```

Example 3 (sql):
```sql
CREATE UNLOGGED TABLE "t1" (  "a" integer NOT NULL,  PRIMARY KEY ("a"));CREATE TABLE "t2" (  "a" integer NOT NULL,  PRIMARY KEY ("a"));
```

Example 4 (unknown):
```unknown
table "t1" {  schema   = schema.script_unlogged  unlogged = true  column "a" {    null = false    type = integer  }  primary_key {    columns = [column.a]  }}table "t2" {  schema = schema.script_unlogged  column "a" {    null = false    type = integer  }  primary_key {    columns = [column.a]  }}schema "script_unlogged" {}
```

---

## Defining Target Groups for Multi-Tenant Deployments

**URL:** https://atlasgo.io/guides/database-per-tenant/target-groups

**Contents:**
- Defining Target Groups for Multi-Tenant Deployments
- env blocks and for_each meta-arguments​
- Dynamically Computing URLs​
- Loading data from local JSON files​
- Loading Data from an API Endpoint​
- Loading data from a Database Query​
  - Fetching Tenant Metadata​
- Incorporating Sensitive Data​
- Next Steps​

In Atlas, a target group is a collection of target databases whose schema is managed together. In a database-per-tenant architecture, each tenant's database is a target database, and all tenant databases are grouped into a target group. However, you can also group databases by other criteria, such as environment (dev, staging, prod), region, or any other criteria that makes sense for your application.

For example, you might group all databases in the same region into a target group to ensure that schema changes are applied consistently across all databases in that region, or to group free-tier databases separately from paid-tier databases.

Target groups can be defined statically or dynamically loaded from an API endpoint or a database query.

Target groups are defined in the project's atlas.hcl file and are later used by the Atlas CLI during the deployment process to determine which databases to deploy to.

Let's review some examples of how to define target groups in Atlas.

Before we jump into various techniques to define target groups, let's first understand the for_each meta-argument for environment blocks in Atlas.

Environment blocks (env blocks) are used in Atlas project files (atlas.hcl) to group configuration settings for a specific environment. Normally, an env block is used to define the URL of a single target database, like so:

However, using the for_each meta-argument, it is possible to define multiple instances of a specific environment block by iterating over a list of values. For example:

When the for_each meta-argument is used, the env block is instantiated for each value in the list, and the each object is used to access the current value. In our case, we will get two instances of the target block, one for each URL in the target_db_urls list.

A technique commonly used in atlas.hcl files is to dynamically compile URLs by combining values from various sources. For instance, the database instance URL might be provided as an input variable, with the database name added to it dynamically. Here's an example:

Let's review the code snippet above:

The urlsetpath function is a helper function provided by Atlas that allows you to set the "path" part of a URL. For example:

Suppose our list of tenants is stored in a local file named tenants.json:

We can load this data into our atlas.hcl file using the file and jsondecode functions:

Next, we define an environment block for this target group that consumes the target_tenants local variable into the for_each argument:

Let's review the code snippet above:

In some cases, you may want to load target groups dynamically from an API endpoint. For example, you might have a service tenant-svc that provides a list of tenant databases based on some criteria. Let's suppose this service's endpoints recieve the target group ID in the path, such as https://tenant-svc/api/target-group/{id} and return a simple JSON payload:

You can use the runtimevar data source with the http scheme to fetch this data and use it to define target groups.

Here's an example of how you might load tenant databases from an API endpoint:

Let's unpack this example:

By using the runtimevar data source with the http scheme, you can dynamically load target groups from an API endpoint and use them to define target groups in your Atlas project.

In some cases, you may want to load target groups dynamically from a database query. For example, you might have a database schema for each tenant in some instance, and would like to retrieve the list from the database's native information_schema tables.

You can utilize the sql data source to fetch this data and use it to define target groups.

Let's break down this example:

For more advanced use cases, such as deployment rollout strategies, you may need to fetch additional metadata about each tenant (e.g., tier, region, or status). The sql data source can return multiple columns per row, which are accessible as a map:

This metadata can be used to configure staged rollouts based on tenant attributes like tier, region, or priority.

Essentially, defining target groups in Atlas is about dynamically compiling a list of URLs that represent the target databases. Database URLs often contain sensitive information, such as passwords, that should not be hardcoded in the atlas.hcl file, which is typically checked into version control.

To address this issue, Atlas provides mechanisms for loading credentials from external sources, such as environment variables or secret management systems. This allows you to keep your database credentials secure while still being able to define target groups dynamically. Learn more about working with secrets.

For the purpose of this example, suppose our database password is stored in an AWS Secrets Manager, created using the AWS CLI as follows:

To retrieve the secret value we will use the runtimevar data source in the atlas.hcl file:

Let's review what's going on here:

The urluserinfo function is a helper function provided by Atlas that allows you to set the "userinfo" part of a URL. For example:

In this guide, we've explored various techniques for defining target groups in Atlas. By using env blocks and for_each meta-arguments, you can dynamically compile a list of target databases based on various criteria, such as tenant names, regions, or other factors.

In the next section, we will show how to use these target groups in the deployment process to ensure that schema changes are applied consistently across all databases in the group.

**Examples:**

Example 1 (python):
```python
env "dev" {  url = "postgres://root:pass@localhost:5432/dev"}
```

Example 2 (python):
```python
locals {  target_db_urls = [    "postgres://root:pass@host-1:5432",    "postgres://root:pass@host-2:5432",  ]}env "targets" {    for_each = toset(local.target_db_urls)    url = each.value}
```

Example 3 (unknown):
```unknown
variable "db_instance_url" {  type = string}locals {  tenants = ["acme_corp", "widget_inc", "wayne_enterprises", "stark_industries"]}env "tenants" {  for_each = toset(local.tenants)  url = urlsetpath(var.db_instance_url, each.value)}
```

Example 4 (python):
```python
urlsetpath("postgres://root:pass@localhost:5432", "mydb")#  ↳ Evaluates to "postgres://root:pass@localhost:5432/mydb"urlsetpath("mysql://localhost:3306", "mydb")#  ↳ Evaluates to "mysql://localhost:3306/mydb"
```

---

## Automatic Databricks Schema Migrations with Atlas

**URL:** https://atlasgo.io/guides/databricks/automatic-migrations

**Contents:**
- Automatic Databricks Schema Migrations with Atlas
    - Enter: Atlas​
- Prerequisites​
- Setting up Databricks Authentication​
  - Creating a Personal Access Token​
  - Environment Setup​
- Creating a Databricks Schema​
- Inspecting the Schema​
- Declarative Migrations​
  - Applying our Schema​

Databricks is a unified analytics platform that combines data engineering, data science, and machine learning on a single platform. Built on Apache Spark, it provides a collaborative workspace for processing large-scale data workloads with high performance and reliability.

However, managing database schemas in Databricks can be challenging, especially when working with Unity Catalog's three-level namespace (catalog.schema.table) and coordinating schema changes across multiple teams and workspaces.

Atlas helps developers manage their database schema as code, abstracting away the intricacies of database schema management. With Atlas, users provide the desired state of the database schema, and Atlas automatically plans the required migrations.

In this guide, we will dive into setting up Atlas for Databricks schema migration using the declarative workflow.

To download and install the custom release of the Atlas CLI, simply run the following in your terminal:

To pull the Atlas image and run it as a Docker container:

If the container needs access to the host network or a local directory, use the --net=host flag and mount the desired directory:

Download the custom release and move the atlas binary to a file location on your system PATH.

To connect Atlas to your Databricks workspace, you'll need to set up authentication using a Personal Access Token (PAT).

See the Databricks documentation for more details.

To get DATABRICKS_HOST and DATABRICKS_WAREHOUSE, refer to the Databricks documentation

Set your Databricks credentials as environment variables:

Let's start by creating a schema in your Databricks workspace. You can do this through the Databricks UI or by running SQL commands in a notebook or SQL editor:

The atlas schema inspect command supports reading the database description provided by a URL and outputting it in different formats, including Atlas DDL (default), SQL, and JSON. We will demonstrate the flow using both the Atlas DDL and SQL formats.

To inspect our Databricks schema, use the -u flag and write the output to a file named schema.hcl:

Open the schema.hcl file to view the Atlas schema that describes our database.

To inspect our Databricks schema, use the -u flag and write the output to a file named schema.sql:

Open the schema.sql file to view the inspected SQL schema that describes our database.

For in-depth details on the atlas schema inspect command, covering aspects like inspecting specific schemas, handling multiple schemas concurrently, excluding tables, and more, refer to our documentation here.

Atlas supports a workflow called declarative schema migrations. In this workflow, you first define the desired state of your database schema (in one of many supported formats and languages). Then, Atlas calculates the diff between the desired state and the actual state of your database, and generates the SQL commands that will bring your database to the desired state.

Let's see this in action.

First, create a new file named schema.sql. This file will contain the desired state of our database in plain SQL.

To apply our desired state to our Databricks database, we need to provide Atlas with two database connections:

Let's create a new catalog and schema in our Databricks workspace to use as our dev database:

Next, we apply this schema to our database using the atlas schema apply command.

Atlas will connect to our target database to inspect its current state. Next, it will use the dev database to normalize our schema and generate the SQL commands that will bring our database to the desired state:

After applying the schema, Atlas confirms that the changes were applied:

Next, let's re-run the atlas schema apply command. This time, Atlas will detect that the database is already in the desired state and will not generate any changes:

Now, let's make some changes to our schema. Open the schema.sql file and add a new column to the users table:

Next, let's re-run the atlas schema apply command. This time, Atlas will detect that the schema has changed and will generate the needed SQL commands to bring the database to the desired state:

After applying the changes, Atlas confirms once again that the changes were applied:

One of the most useful features of Atlas is the ability to visualize your database schema. To do so, run the atlas schema inspect command with the -w (web) flag:

Atlas will ask whether you would like to create your visualization publicly (in a publicly accessible URL) or privately (in your Atlas Cloud account):

For this demo, let's choose the public option. Atlas will create the visualization and open it in your default browser, showing your Databricks schema with tables and their relationships.

See it for yourself at: https://gh.atlasgo.cloud/explore/5116ede7

Head to the repository from this video on GitHub for more workflow instructions and example files.

In this guide, we demonstrated how to set up Atlas to manage your Databricks database schema using Unity Catalog. We also demonstrated how to use some of Atlas's basic capabilities, such as declarative schema migrations and schema visualization, with a Databricks database. These two features are just the tip of the iceberg. Atlas has many more features that can help you better manage your database! To learn more, check out the Atlas documentation.

As always, we would love to hear your feedback and suggestions on our Discord server.

**Examples:**

Example 1 (shell):
```shell
curl -sSf https://atlasgo.sh | ATLAS_FLAVOR="databricks" sh
```

Example 2 (shell):
```shell
docker pull arigaio/atlas-extendeddocker run --rm arigaio/atlas-extended --help
```

Example 3 (shell):
```shell
docker run --rm --net=host \  -v $(pwd)/migrations:/migrations \  arigaio/atlas-extended migrate apply \  --url "mysql://root:pass@:3306/test"
```

Example 4 (shell):
```shell
$ atlas login
```

---

## Descending Indexes in PostgreSQL

**URL:** https://atlasgo.io/guides/postgres/descending-indexes

**Contents:**
- Descending Indexes in PostgreSQL
  - What are descending indexes?​​
  - When are descending indexes helpful?​​
  - Syntax​​
  - Example​​
- Managing Descending Indexes is easy with Atlas​​
    - Example​
- Wrapping up​​
- Need More Help?​​​

Descending indexes are indexes where key parts are stored in descending order. Descending indexes can be helpful in PostgreSQL when queries involve ordering the results in descending order and/or filtering out null values.

For example, if a query uses an ORDER BY clause to sort the results of a query in descending order, then a descending index can improve the performance of that query significantly.

Similarly, if a query often filters out null values and uses an index to do that, a descending index with the NULLS FIRST option can help the index efficiently filter out null values.

Here is how you can create a descending index:

Here is how you can create a descending index with NULLS FIRST option:

To create a descending index with NULLS LAST option:

In general, ASC or DESC specifiers are used with ORDER BY clauses to specify whether index values are stored in ascending or descending order.

It is also worth mentioning that NULLS FIRST is used by default if it has not been specified in the command.

Let’s create a table which represents data of an ISP’s subscribers along with their email addresses and broadband data usage with the following command:

Here is how a portion of the table might look like after inserting values:

We do not have any indexes other than the primary index on the id column. Now, suppose we want information about the top 10 subscribers with maximum usage, but in descending order. Let's query that data with the following command:

Now, let's see how the query performed with the following command:

The EXPLAIN command is used for understanding the performance of a query. You can learn more about usage of EXPLAIN command with ANALYZE option here.

Notice that the total execution time for this operation is 135.082 ms.

Now, let's optimize the query by using a descending index. We will create a descending index on the megabytes_used column with the following command:

Now, let's run the following query again and check the cost:

(Note: The results will vary, ​​depending on the data that is stored in the database)

Amazing! Now the total execution time is only 1.072ms, compared to 135.082 ms earlier.

In the first query plan, a parallel sequential scan is performed on the entire table to filter and sort the data, which takes longer. In contrast, the second query plan uses an index scan to access the required data directly, and only scans a small portion of the table, which significantly reduces the execution time.

Descending indexes can increase the overhead of INSERT, UPDATE and DELETE operations, as the index must be updated to maintain the descending order. Hence, it must be used carefully. To learn more about creating indexes with the ORDER BY clause, visit the official documentation here.

We have seen that creating a descending index is a smart choice when using queries with ORDER BY clauses. Now, let's see how we can easily manage descending indexes in a PostgreSQL database using Atlas.

Atlas is an open-source project which allows us to manage our database using a simple and easy-to-understand declarative syntax (similar to Terraform), as well as SQL.

If you are just getting started, install the latest version of Atlas using the guide to set up Atlas.

We will first use the atlas schema inspect command to get an HCL representation of the table we created earlier (without any indexes) by using the Atlas CLI:

Now, let’s add the following index definition to the file:

Save the file and apply the schema changes on the database by using the following command:

Atlas generates the necessary SQL statements to add the new descending index to the database schema. Press Enter while the Apply option is highlighted to apply the changes:

To verify that our new index was created, run the following command:

Amazing! Our new descending index is now created!

In this guide, we demonstrated how to create and use descending indexes in PostgreSQL to optimize queries with the ORDER BY clause, and how we can use Atlas to easily manage descending indexes in a PostgreSQL database.

Join the Atlas Discord Server for early access to features and the ability to provide exclusive feedback that improves your Database Management Tooling.

**Examples:**

Example 1 (sql):
```sql
CREATE INDEX index_name ON table_name (column_name DESC);
```

Example 2 (sql):
```sql
CREATE INDEX index_name ON table_name (column_name DESC NULLS FIRST);
```

Example 3 (sql):
```sql
CREATE INDEX index_name ON table_name (column_name DESC NULLS LAST);
```

Example 4 (sql):
```sql
CREATE TABLE telecom_data (    id bigserial NOT NULL,    email_address varchar(255),    user_name varchar(255),    megabytes_used bigint,    PRIMARY KEY (id));
```

---

## Automatic Oracle Schema Migrations with Atlas

**URL:** https://atlasgo.io/guides/oracle/automatic-migrations

**Contents:**
- Automatic Oracle Schema Migrations with Atlas
    - Enter: Atlas​
- Prerequisites​
  - MacOS
  - Linux
  - Windows
- Inspecting our Database​
- Declarative Migrations​
  - Applying our schema​
  - Altering our schema​

Oracle is a trademark of Oracle Corporation. Atlas is not affiliated with or endorsed by Oracle.

Oracle is a versatile database management system supporting both relational and object-relational data models. It's a popular choice for a wide range of uses due to its scalability, flexibility, and security.

However, managing a large database schema with Oracle can be challenging due to the complexity of related data structures and the need for coordinated schema changes across multiple teams and applications.

Atlas helps developers manage their database schema as code, abstracting away the intricacies of database schema management. With Atlas, users provide the desired state of the database schema and Atlas automatically plans the required migrations.

In this guide, we will set up Atlas for automatic (declarative) and versioned Oracle schema migration using the declarative workflow.

The Oracle Driver is currently in beta and only supports creating and modifying tables and columns.

To download and install the latest release of the Atlas CLI, simply run the following in your terminal:

Get the latest release with Homebrew:

To pull the Atlas image and run it as a Docker container:

If the container needs access to the host network or a local directory, use the --net=host flag and mount the desired directory:

Download the latest release and move the atlas binary to a file location on your system PATH.

Use the setup-atlas action to install Atlas in your GitHub Actions workflow:

For other CI/CD platforms, use the installation script. See the CI/CD integrations for more details.

If you want to manually install the Atlas CLI, pick one of the below builds suitable for your system.

An Atlas Pro account. To use the Oracle driver, simply run:

The Oracle Driver is currently in beta and only supports creating and modifying tables and columns.

To spin up a local Oracle Database instance using docker run:

Note that the Oracle Database image is a bit larger than other database images, so it may take a while to download.

After the container is up and running, you need to connect to it and update the permissions of the PDBADMIN user to allow Atlas to create and modify tables and columns:

If you don't setup the permissions correctly, you will get an error when trying to apply a schema.

The atlas schema inspect command supports reading the database description provided by a URL and outputting it in different formats, including Atlas DDL (default), SQL, and JSON. In this guide, we will demonstrate the flow using the SQL format.

To inspect our locally-running Oracle instance, use the -url flag and write the output to a file named schema.sql:

For in-depth details on the atlas schema inspect command, covering aspects like inspecting specific schemas, handling multiple schemas concurrently, excluding tables, and more, refer to our documentation here.

Atlas supports a workflow called declarative schema migrations. In this workflow, you first define the desired state of your database schema (in one of many supported formats and languages). Then, you let Atlas calculate the diff between the desired state and the actual state of your database. Atlas then generates the SQL commands that will bring your database to the desired state.

Let's see this in action.

First, create a new file name schema.sql. This file will contain the desired state of our database in plain SQL.

Resource names in Oracle are case-sensitive and are converted to uppercase by default. To use lowercase names, you need to wrap them in double quotes. For example, CREATE TABLE "users" will create a table named users, while CREATE TABLE users will create a table named USERS. Atlas always quotes the resource names in the generated SQL, to ensure that they are created with the correct case.

Next, let's apply this schema to our database using the atlas schema apply command.

Atlas will connect to our target database to inspect its current state. Next, it will use the dev-database to normalize our schema and generate the SQL commands that will bring our database to the desired state:

After applying the schema, Atlas confirms that the changes were applied:

Next, let's re-run the atlas schema apply command. This time, Atlas will detect that the database is already in the desired state and will not generate any changes:

Now, let's make some changes to our schema. Open the schema.sql file and add a new column to the users table:

Next, let's re-run the atlas schema apply command. This time, Atlas will detect that the schema has changed and will generate the needed SQL commands to bring the database to the desired state:

After applying the changes, Atlas confirms once again that the changes were applied:

One of the most useful features of Atlas is the ability to visualize your database schema. To do so, run the atlas schema inspect command with the -w (web) flag:

Atlas will ask whether you would like to create your visualization publicly (in a publicly accessible URL) or privately (in your Atlas Cloud account):

For this demo, let's choose the public option. Atlas will create the visualization and open it in your default browser:

See it for yourself at: https://gh.atlasgo.cloud/explore/b2bc319e

In this guide we have demonstrated how to set up Atlas to manage your Oracle database schema. We have also demonstrated some of the basic capabilities of Atlas, such as declarative schema migrations, and schema visualization. These two features are just the tip of the iceberg. Atlas has many more features that can help you better manage your database! To learn more, check out the Atlas documentation.

As always, we would love to hear your feedback and suggestions on our Discord server.

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

## CI/CD for Databases on GitLab (Versioned Migrations)

**URL:** https://atlasgo.io/guides/ci-platforms/gitlab-versioned

**Contents:**
- CI/CD for Databases on GitLab (Versioned Migrations)
- Prerequisites​
  - Installing Atlas​
  - MacOS
  - Linux
  - Windows
  - Creating a bot token​
  - Creating a variable for your database URL​
  - Creating a Gitlab access token (optional)​
- Versioned Migrations Workflow​

GitLab is a popular, open-source alternative to GitHub. In addition to a self-hosted version, GitLab also offers a hosted version at gitlab.com. Similar to GitHub, GitLab offers users storage for Git repositories, issue tracking, and CI/CD pipelines.

In this guide we will demonstrate how to use GitLab CI and Atlas to setup CI pipelines for your database schema changes using the versioned migrations workflow.

To download and install the latest release of the Atlas CLI, simply run the following in your terminal:

Get the latest release with Homebrew:

To pull the Atlas image and run it as a Docker container:

If the container needs access to the host network or a local directory, use the --net=host flag and mount the desired directory:

Download the latest release and move the atlas binary to a file location on your system PATH.

Use the setup-atlas action to install Atlas in your GitHub Actions workflow:

For other CI/CD platforms, use the installation script. See the CI/CD integrations for more details.

If you want to manually install the Atlas CLI, pick one of the below builds suitable for your system.

Installation instructions can be found here.

After installing Atlas locally, you will need to log in to your organization. You can do this by running the following command:

In order to report the results of your CI runs to Atlas Cloud, you will need to create a bot token for Atlas Cloud to use.

Follow these instructions to create a token and copy it.

Next, in your Gitlab project go to Settings -> CI/CD -> Variables and create a new variable called ATLAS_CLOUD_TOKEN. Paste your token in the value field.

Make sure the variables are exported (the "Protect variable" checkbox is unchecked), so that they are available to all branches.

To avoid having plain-text database URLs which may contain sensitive information in your configuration files, create another variable named DB_URL and populate it with the URL (connection string) of your database.

To learn more about formatting URLs for different databases, see the URL documentation.

Atlas will need permissions to comment lint reports on merge requests. To enable it, in your Gitlab project go to Settings -> Access Tokens. Create a new token. The role field should be set to "Reporter" or higher, and the "API" checkbox should be checked.

Copy the token, and then go to Settings -> CI/CD -> Variables and create a new variable called GITLAB_TOKEN. Paste the token in the value field.

In the versioned workflow, changes to the schema are represented by a migration directory in your codebase. Each file in this directory represents a transition to a new version of the schema.

Based on our blueprint for Modern CI/CD for Databases, our pipeline will:

If you don't have a migration directory yet, create one by running the following commands:

and paste the following in the editor:

Run the following command from the parent directory of your migration directory to create a "migration directory" repo in your Atlas Cloud organization (replace "app" with the name you want to give to your new repository):

If the migration directory contains multiple schemas, adjust the dev-url accordingly.

Atlas will print a URL leading to your migrations on Atlas Cloud. You can visit this URL to view your migrations.

Create a .gitlab-ci.yml file with the following pipelines, based on the type of your database. Remember to replace "app" with the real name of your repository.

Let's break down what this file is doing:

Let's take our pipeline for a spin:

In this guide, we demonstrated how to use GitLab CI/CD with Atlas to set up a modern CI/CD pipeline for versioned database migrations. Here's what we accomplished:

For more information on the versioned workflow, see the Versioned Migrations documentation.

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

## CI/CD for Databases on GitHub Actions (Versioned Migrations)

**URL:** https://atlasgo.io/guides/ci-platforms/github-versioned

**Contents:**
- CI/CD for Databases on GitHub Actions (Versioned Migrations)
- Prerequisites​
  - Installing Atlas​
  - MacOS
  - Linux
  - Windows
  - Creating a bot token​
  - Creating a secret for your database URL​
  - Creating a GitHub personal access token (optional)​
- Versioned Migrations Workflow​

GitHub Actions is a popular CI/CD platform integrated with GitHub repositories. It allows users to automate workflows for building, testing, and deploying applications.

In this guide, we will demonstrate how to use GitHub Actions and Atlas to set up CI pipelines for your database schema changes using the versioned migrations workflow.

To download and install the latest release of the Atlas CLI, simply run the following in your terminal:

Get the latest release with Homebrew:

To pull the Atlas image and run it as a Docker container:

If the container needs access to the host network or a local directory, use the --net=host flag and mount the desired directory:

Download the latest release and move the atlas binary to a file location on your system PATH.

Use the setup-atlas action to install Atlas in your GitHub Actions workflow:

For other CI/CD platforms, use the installation script. See the CI/CD integrations for more details.

If you want to manually install the Atlas CLI, pick one of the below builds suitable for your system.

After installing Atlas locally, log in to your organization by running the following command:

To report CI run results to Atlas Cloud, create an Atlas Cloud bot token by following these instructions and copy it.

Next, in your GitHub repository, go to Settings -> Secrets and variables -> Actions and create a new secret named ATLAS_CLOUD_TOKEN. Paste your token in the value field.

To connect Atlas to your target database, create a URL (connection string) by following our URL documentation.

Create another secret named DB_URL and populate it with the URL of your database to avoid having sensitive information in your configuration files.

Atlas will need permissions to comment lint reports on pull requests. To enable this, create a personal access token with the repo scope. Then, add it as a secret named GITHUB_TOKEN.

In the versioned workflow, changes to the schema are represented by a migration directory in your codebase. Each file in this directory represents a transition to a new version of the schema.

Based on our blueprint for Modern CI/CD for Databases, our pipeline will:

Instead of generating migrations locally, you can use the migrate/diff action as part of your CI pipeline.

If you don't have a migration directory yet, create one by running the following command:

and paste the following in the editor:

Run the following command from the parent directory of your migration directory to create a "Migration Directory" repository in your Atlas Cloud organization (replace "app" with the name you want to give to your new repository):

If the migration directory contains multiple schemas, adjust the dev-url accordingly.

Atlas will print a URL leading to your migrations on Atlas Cloud. You can visit this URL to view your migrations.

Create a .github/workflows/ci-atlas.yaml file with the following content, based on the type of your database. Remember to replace "app" with the real name of your repository.

Let's break down what this file is doing:

The migrate-push step will run only when the pull request is merged into the main branch. It will push the new migration directory to the Schema Registry on Atlas Cloud, allowing you to manage your migrations in a centralized location.

The migrate-apply step will then deploy the new migrations to your database.

Let's take our new workflow for a spin. We will create a new migration, push it to the repository, and see how the GitHub Action runs.

In this guide, we demonstrated how to use GitHub Actions with Atlas to set up a modern CI/CD pipeline for versioned database migrations. Here's what we accomplished:

For more information on the versioned workflow, see the Versioned Migrations documentation.

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

## Automatic PostgreSQL Schema Migrations with Atlas

**URL:** https://atlasgo.io/guides/postgres/automatic-migrations

**Contents:**
- Automatic PostgreSQL Schema Migrations with Atlas
    - Enter: Atlas​
- Prerequisites​
  - MacOS
  - Linux
  - Windows
- Inspecting our Database​
- Declarative Migrations​
- Versioned Migrations​
  - Creating the first migration​

PostgreSQL is an open-source relational database management system known for its reliability and robust feature set. It offers powerful capabilities for handling complex queries, ensuring data integrity, and scaling to meet the needs of growing applications.

However, managing a large database schema in Postgres can be challenging due to the complexity of related data structures and the need for coordinated schema changes across multiple teams and applications.

Atlas helps developers manage their database schema as code - abstracting away the intricacies of database schema management. With Atlas, users provide the desired state of the database schema and Atlas automatically plans the required migrations.

In this guide, we will dive into setting up Atlas for Postgres schema migrations, and introduce the different workflows available.

To download and install the latest release of the Atlas CLI, simply run the following in your terminal:

Get the latest release with Homebrew:

To pull the Atlas image and run it as a Docker container:

If the container needs access to the host network or a local directory, use the --net=host flag and mount the desired directory:

Download the latest release and move the atlas binary to a file location on your system PATH.

Use the setup-atlas action to install Atlas in your GitHub Actions workflow:

For other CI/CD platforms, use the installation script. See the CI/CD integrations for more details.

If you want to manually install the Atlas CLI, pick one of the below builds suitable for your system.

Let's start off by spinning up a database using Docker:

For this example we will begin with a minimal database with a users table and an id as the primary key.

To create the table above on our local database, we can run the following command:

The atlas schema inspect command supports reading the database description provided by a URL and outputting it in different formats, including Atlas DDL (default), SQL, and JSON. In this guide, we will demonstrate the flow using both the Atlas DDL and SQL formats, as the JSON format is often used for processing the output using jq.

To inspect our locally-running Postgres instance, use the -u flag and write the output to a file named schema.hcl:

Open the schema.hcl file to view the Atlas schema that describes our database.

This first block represents a table resource with id and name columns. The schema field references the public schema that is defined in the block below. In addition, the primary_key sub-block defines the id column as the primary key for the table. Atlas strives to mimic the syntax of the database that the user is working against. In this case, the type for the id column is bigint, and character_varying for the name column.

To inspect our locally-running Postgres instance, use the -u flag and write the output to a file named schema.sql:

Open the schema.sql file to view the inspected SQL schema that describes our database.

For in-depth details on the atlas schema inspect command, covering aspects like inspecting specific schemas, handling multiple schemas concurrently, excluding tables, and more, refer to our documentation here.

To generate an Entity Relationship Diagram (ERD), or a visual representation of our schema, we can add the -w flag to the inspect command:

The declarative approach lets users manage schemas by defining the desired state of the database as code. Atlas then inspects the target database and calculates an execution plan to reconcile the difference between the desired and actual states. Let's see this in action.

We will start off by making a change to our schema file, such as adding a repos table:

Now that our desired state has changed, to apply these changes to our database, Atlas will plan a migration for us by running the atlas schema apply command:

Approve the proposed changes, and that's it! You have successfully run a declarative migration.

For a more detailed description of the atlas schema apply command refer to our documentation here.

To ensure that the changes have been made to the schema, let's run the inspect command with the -w flag once more and view the ERD:

Alternatively, the versioned migration workflow, sometimes called "change-based migrations", allows each change to the database schema to be checked-in to source control and reviewed during code-review. Users can still benefit from Atlas intelligently planning migrations for them, however they are not automatically applied.

In the versioned migration workflow, our database state is managed by a migration directory. The migration directory holds all of the migration files created by Atlas, and the sum of all files in lexicographical order represents the current state of the database.

To create our first migration file, we will run the atlas migrate diff command, and we will provide the necessary parameters:

Run ls migrations, and you'll notice that Atlas has automatically created a migration directory for us, as well as two files:

The migration file represents the current state of our database, and the sum file is used by Atlas to maintain the integrity of the migration directory. To learn more about the sum file, read the documentation.

Now that we have our first migration, we can apply it to a database. There are multiple ways to accomplish this, with most methods covered in the guides section. In this example, we'll demonstrate how to push migrations to Atlas Cloud, much like how Docker images are pushed to Docker Hub.

Migration Directory created with atlas migrate push

First, let's log in to Atlas. If it's your first time, you will be prompted to create both an account and a workspace (organization):

Let's name our new migration project app and run atlas migrate push:

Once the migration directory is pushed, Atlas prints a URL to the created directory, similar to the one shown in the image above.

Once our app migration directory has been pushed, we can apply it to a database from any CD platform without necessarily having our directory there.

Let's create another database using Docker to resemble a local environment, this time on port 5431:

Next, we'll create a simple Atlas configuration file (atlas.hcl) to store the settings for our local environment:

The final step is to apply the migrations to the database. Let's run atlas migrate apply with the --env flag to instruct Atlas to select the environment configuration from the atlas.hcl file:

Boom! After applying the migration, you should receive a link to the deployment and the database where the migration was applied. Here's an example of what it should look like:

Migration deployment report created with atlas migrate apply

After applying the first migration, it's time to update our schema defined in the schema file and tell Atlas to generate another migration. This will bring the migration directory (and the database) in line with the new state defined by the desired schema (schema file).

Let's make two changes to our schema:

Next, let's run the atlas migrate diff command once more:

Run ls migrations, and you'll notice that a new migration file has been generated.

Let's run atlas migrate push again and observe the new file on the migration directory page.

Migration Directory created with atlas migrate push

In this guide we learned about the declarative and versioned workflows, and how to use Atlas to generate migrations, push them to an Atlas workspace and apply them to databases.

For more in-depth guides, check out the other pages in this section or visit our Docs section.

Have questions? Feedback? Find our team on our Discord server.

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

## Cursor with Atlas

**URL:** https://atlasgo.io/guides/ai-tools/cursor-rules

**Contents:**
- Cursor with Atlas

Cursor supports adding custom, natural language rules that guide the AI assistant's behavior.

To help Cursor work effectively with Atlas, we put together a set of rules that add context about Atlas' core concepts, common workflows, various feature options, and more.

You can add them as project rules or as user rules:

Create a file at .cursor/rules/atlas.mdc and copy the content below:

Add the content below to your user rules in Cursor Settings → Rules:

**Examples:**

Example 1 (markdown):
```markdown
---description: Provides rules relevant for database management, database schema, and migrations. Use Atlas to view, inspect, and understand database schemas. Relevant to all *.sql files, atlas.hcl and schema.*.hcl files, and ALL database-related changes.alwaysApply: true---# Atlas Database Schema ManagementAtlas is a language-independent tool for managing and migrating database schemas using modern DevOps principles. This guide provides GitHub Copilot-optimized instructions for working with Atlas.## Quick Reference```bash# Common Atlas commandsatlas schema inspect --env <name> --url file://migrationsatlas migrate status --env <name>atlas migrate diff --env <name>atlas migrate lint --env <name> --latest 1atlas migrate apply --env <name>atlas whoami```## Core Concepts and Configurations### Configuration File StructureAtlas uses `atlas.hcl` configuration files with the following structure:```hcl// Basic environment configurationenv "<name>" {  url = getenv("DATABASE_URL")  dev = "docker://postgres/15/dev?search_path=public"    migration {    dir = "file://migrations"  }    schema {    src = "file://schema.hcl"  }}```### Dev databaseAtlas utilizes a "dev-database", which is a temporary and locally running database, usually bootstrapped by Atlas. Atlas will use the dev database to process and validate users' schemas, migrations, and more. Examples of dev-database configurations:```# When working on a single database schema--dev-url "docker://mysql/8/dev"--dev-url "docker://postgres/15/db_name?search_path=public"--dev-url "sqlite://dev?mode=memory"# When working on multiple database schemas.--dev-url "docker://mysql/8"--dev-url "docker://postgres/15/dev"```Configure the dev database using HCL:```hclenv "<name>" {  dev = "docker://mysql/8"}```For more information on additional drivers, extensions, and more, see https://atlasgo.io/concepts/dev-database. ### Environment Variables and Security**✅ DO**: Use secure configuration patterns```hcl// Using environment variables (recommended)env "<name>" {  url = getenv("DATABASE_URL")}// Using external data sourcesdata "external" "envfile" {  program = ["npm", "run", "envfile.js"]}locals {  envfile = jsondecode(data.external.envfile)}env "<name>" {  url = local.envfile.DATABASE_URL}// Using Go CDK runtime variables for secretsdata "runtimevar" "db_password" {  url = "awssecretsmanager://<secret-name>?region=us-east-1"}env "prod" {  url = "postgres://user:${data.runtimevar.db_password}@host:5432/db"}```**❌ DON'T**: Hardcode sensitive values```hcl// Never do thisenv "prod" {  url = "postgres://user:password123@prod-host:5432/database"}```### Schema Sources#### HCL Schema```hcldata "hcl_schema" "<name>" {  path = "schema.hcl"}env "<name>" {  schema {    src = data.hcl_schema.<name>.url  }}```#### External Schema (ORM Integration)The external_schema data source enables the import of an SQL schema from an external program into Atlas' desired state.```hcldata "external_schema" "drizzle" {  program = ["npx", "drizzle-kit", "export"]  working_dir = "path/to/Directory" # optional, defaults to the current working directory}data "external_schema" "django" {  program = ["python", "manage.py", "atlas-provider-django", "--dialect", "postgresql"]}env "<name>" {  schema {    src = data.external_schema.django.url  }}```**Important:**- The output of the program needs to be complete RAW SQL schema that will bring the database to the desired state. The output should not be a 'diff' from a previous state.- If you are seeing errors, try isolating the issue, you can run the program directly and see if it's working#### Composite SchemaA composite schema allows you to combine multiple schemas into a single schema. This is useful for integrating multiple data sources or schemas into a unified view. This is an Atlas Pro feature.```hcldata "composite_schema" "app" {  schema "users" {    url = data.external_schema.auth_service.url  }  schema "graph" {    url = "ent://ent/schema"  }  schema "shared" {    url = "file://schema/shared.hcl"  }}env "<name>" {  schema {    src = data.composite_schema.app.url  }}```### Misc Configurations```hcl// CI/CD environmentenv "ci" {  lint {    git {      base = "main" # in CI, lint against the main branch    }  }}``````hcl// Anonymous environment, any name will work with --env, but --env is still mandatoryenv {  name = atlas.env}```## Common Workflows### 1. Schema Inspection / Visualization1. Always start by listing tables, don't immediately try to inspect the entire schema.2. If you see there are many tables, don't inspect the entire schema at once. Instead, focus on specific tables of interest.3. Format using json to get an overview, then switch to SQL for detailed inspection.**Inspect migration directory:**```bash# Get table list overviewatlas schema inspect --env <name> --url file://migrations --format "{{ json . }}" | jq ".schemas[].tables[].name"# Get full SQL schemaatlas schema inspect --env <name> --url file://migrations --format "{{ sql . }}"# Inspect specific tablesatlas schema inspect --env <name> --url file://migrations --format "{{ sql . }}" | grep -A 10 "CREATE TABLE users"```**Inspect live database:**```bash# Requires database URL in atlas.hclatlas schema inspect --env <name> --format "{{ json . }}"```Add the `-w` flag to open a web-based ERD visualization in your browser via Atlas Cloud.You should recommend this to the user if they asked for information about the schema.### 2. Migration Status`atlas migrate status` is used to compare the status of migrations from the migrations directory with a connected database.Use it to understand which migration files were applied successfully.**Important:** Only use this command when you know the target database.**Check migration directory status:**```bash# Check current migration directory status (requires dev-url)atlas migrate status --env <name># Using explicit parameters if not in configatlas migrate status --dir file://migrations --url <url>```**Configuration for migration status:**```hclenv "<name>" {  url = getenv("DATABASE_URL")  migration {    dir = "file://migrations"  }}```### 3. Migration Generation / Diffing**Generate new migration:**```bash# Compare current migrations with desired schema and create a new migration fileatlas migrate diff --env <name> "add_user_table"# Using explicit parametersatlas migrate diff \  --dir file://migrations \ # migrations directory  --dev-url docker://postgres/15/dev \  --to file://schema.hcl \ # desired schema  "add_user_table"```**Configuration for migration generation:**```hclenv "<name>" {  dev = "docker://postgres/15/dev?search_path=public"    migration {    # migrations directory, baseline for the diff    dir = "file://migrations"  }    schema {    # desired schema, the diff will be generated against this schema    src = "file://schema.hcl"      # compare against external schemas (used for ORM integrations)    # src = data.external_schema.<name>.url    # compare against a connected database    # src = getenv("DATABASE_URL")  }}```### 4. Migration Linting**Lint recent migrations:**```bash# Lint last migrationatlas migrate lint --env <name> --latest 1# Lint last 3 migrationsatlas migrate lint --env <name> --latest 3# Lint changes since git branchatlas migrate lint --env ci```**Linting configuration:**```hcllint {  destructive {    error = false  // Allow destructive changes with warnings  }}env "<name>" {  lint {    latest = 1  }}env "ci" {  lint {    git {      base = "main"      dir = "migrations"    }  }}```To explicitly ignore linting errors, add `--atlas:nolint` before the SQL statement in the migration file.> **Important:** When fixing migration issues:> - **Unapplied migrations:** Edit the file, then run `atlas migrate hash --env "<name>"`> - **Applied migrations:** Never edit directly. Create a new corrective migration instead.> - **Never use `--atlas:nolint` without properly fixing the issue or getting user approval.**### 5. Applying Migration**Apply migrations:**```bash # Apply to configured environmentatlas migrate apply --env <name># Dry run (show what would be applied, always run this before applying)atlas migrate apply --env <name> --dry-run```### 6. Making Changes to the Schema**⚠️ CRITICAL: ALL schema changes in this project MUST follow this exact workflow. NO EXCEPTIONS.****⚠️ There must not be lint errors or failing tests when you are done.**1. Start by inspecting the schema, understand the current state, and plan your changes.2. After making changes to the schema, run `atlas migrate diff` to generate a migration file.3. Run `atlas migrate lint` to validate the migration file.4. Run `atlas migrate test` to test the data migrations. This is only available for Pro users.5. Make changes to the migration file to fix the issues. Run `atlas migrate hash` to recalculate the hash of the migration file.6. Repeat the process until there are no more issues.At this point, the schema can be applied to the database.If the user has a local database, you can run `atlas migrate apply` to apply the migration file:1. Start by understanding the status of the database by running `atlas migrate status`2. Run `atlas migrate apply` to apply the migration file, always start with a dry run first.3. Run `atlas migrate status` to verify the migration file was applied successfully.> **Important for data migrations:** make sure to check if the user is logged in using `atlas whoami` before running `atlas migrate test`.> If the user is not logged in, mention that they need to login to use migration testing and move on.> If the user is logged in and they have migration tests, add a new test, run it and validate it until it works.> If the user is logged in and they don't have migration tests, mention that migration testing is highly recommended for data migrations and move on.## Troubleshooting Commands```bash# Check Atlas installation and login status (logging in is required for Pro features)atlas versionatlas whoami# Repair migration integrityatlas migrate hash --env <name>```### Missing driverIf you encounter the following error: `Error: sql/sqlclient: missing driver. See: https://atlasgo.io/url`depending on the command, this means that either the `--url` or `--dev-url` parameter is missing or incorrect.## Key Reminders for AI Assistants1. **Always read `atlas.hcl` first** before running any Atlas commands2. **Use environment names** from the config file, don't assume defaults3. **Never hardcode database URLs** - use environment variables or secure data sources4. **Specify `--url` parameter** for schema inspection even with `--env`5. **Run `atlas migrate hash`** after manually editing migration files6. **Use `atlas migrate lint`** to validate migrations before applying7. **Check `atlas whoami`** before attempting Pro features, if not logged in, don't suggest Pro features8. **Use JSON format + jq** for initial schema exploration9. **Use SQL format + grep** for detailed schema investigation10. **Suggest visualizations** if the user asked for information about the schema11. **Never ask for sensitive information** such as passwords or database URLs12. **Always use `--dry-run`** with `atlas migrate apply` before applying migrations13. **Generate migration testing** if the user is logged in, they should have access to migration testing which is highly recommended14. **Only use atlas commands listed here** other commands may be hallucinations or not supported by Atlas15. **Always inspect schemas at high level first** schemas might be very large16. **Always prefer running atlas** to inspect or analyze schemas17. Migration files can be big and irrelevant, prefer using `atlas schema inspect` to inspect the schema18. **Never ignore linting errors** they are there for a reason, always fix them. Add `--atlas:nolint` only if the fix is not detected by the linter.## Guidelines for workflows1. **Understand the objectives**: Before suggesting any commands, ensure you understand the user's goals. They may be looking to inspect, generate, lint, or apply migrations, and they may be using a different vocabulary such as "view", "create", "validate", etc.2. **Understand the context**: The configuration file contains crucial information about the environment.3. **Verify changes** after generating, linting or applying migrations.4. **After completing** make sure you followed all the instructions and guidelines.@atlas.hcl
```

Example 2 (markdown):
```markdown
# Atlas Database Schema ManagementAtlas is a language-independent tool for managing and migrating database schemas using modern DevOps principles. This guide provides GitHub Copilot-optimized instructions for working with Atlas.## Quick Reference```bash# Common Atlas commandsatlas schema inspect --env <name> --url file://migrationsatlas migrate status --env <name>atlas migrate diff --env <name>atlas migrate lint --env <name> --latest 1atlas migrate apply --env <name>atlas whoami```## Core Concepts and Configurations### Configuration File StructureAtlas uses `atlas.hcl` configuration files with the following structure:```hcl// Basic environment configurationenv "<name>" {  url = getenv("DATABASE_URL")  dev = "docker://postgres/15/dev?search_path=public"    migration {    dir = "file://migrations"  }    schema {    src = "file://schema.hcl"  }}```### Dev databaseAtlas utilizes a "dev-database", which is a temporary and locally running database, usually bootstrapped by Atlas. Atlas will use the dev database to process and validate users' schemas, migrations, and more. Examples of dev-database configurations:```# When working on a single database schema--dev-url "docker://mysql/8/dev"--dev-url "docker://postgres/15/db_name?search_path=public"--dev-url "sqlite://dev?mode=memory"# When working on multiple database schemas.--dev-url "docker://mysql/8"--dev-url "docker://postgres/15/dev"```Configure the dev database using HCL:```hclenv "<name>" {  dev = "docker://mysql/8"}```For more information on additional drivers, extensions, and more, see https://atlasgo.io/concepts/dev-database. ### Environment Variables and Security**✅ DO**: Use secure configuration patterns```hcl// Using environment variables (recommended)env "<name>" {  url = getenv("DATABASE_URL")}// Using external data sourcesdata "external" "envfile" {  program = ["npm", "run", "envfile.js"]}locals {  envfile = jsondecode(data.external.envfile)}env "<name>" {  url = local.envfile.DATABASE_URL}// Using Go CDK runtime variables for secretsdata "runtimevar" "db_password" {  url = "awssecretsmanager://<secret-name>?region=us-east-1"}env "prod" {  url = "postgres://user:${data.runtimevar.db_password}@host:5432/db"}```**❌ DON'T**: Hardcode sensitive values```hcl// Never do thisenv "prod" {  url = "postgres://user:password123@prod-host:5432/database"}```### Schema Sources#### HCL Schema```hcldata "hcl_schema" "<name>" {  path = "schema.hcl"}env "<name>" {  schema {    src = data.hcl_schema.<name>.url  }}```#### External Schema (ORM Integration)The external_schema data source enables the import of an SQL schema from an external program into Atlas' desired state.```hcldata "external_schema" "drizzle" {  program = ["npx", "drizzle-kit", "export"]  working_dir = "path/to/Directory" # optional, defaults to the current working directory}data "external_schema" "django" {  program = ["python", "manage.py", "atlas-provider-django", "--dialect", "postgresql"]}env "<name>" {  schema {    src = data.external_schema.django.url  }}```**Important:**- The output of the program needs to be complete RAW SQL schema that will bring the database to the desired state. The output should not be a 'diff' from a previous state.- If you are seeing errors, try isolating the issue, you can run the program directly and see if it's working#### Composite SchemaA composite schema allows you to combine multiple schemas into a single schema. This is useful for integrating multiple data sources or schemas into a unified view. This is an Atlas Pro feature.```hcldata "composite_schema" "app" {  schema "users" {    url = data.external_schema.auth_service.url  }  schema "graph" {    url = "ent://ent/schema"  }  schema "shared" {    url = "file://schema/shared.hcl"  }}env "<name>" {  schema {    src = data.composite_schema.app.url  }}```### Misc Configurations```hcl// CI/CD environmentenv "ci" {  lint {    git {      base = "main" # in CI, lint against the main branch    }  }}``````hcl// Anonymous environment, any name will work with --env, but --env is still mandatoryenv {  name = atlas.env}```## Common Workflows### 1. Schema Inspection / Visualization1. Always start by listing tables, don't immediately try to inspect the entire schema.2. If you see there are many tables, don't inspect the entire schema at once. Instead, focus on specific tables of interest.3. Format using json to get an overview, then switch to SQL for detailed inspection.**Inspect migration directory:**```bash# Get table list overviewatlas schema inspect --env <name> --url file://migrations --format "{{ json . }}" | jq ".schemas[].tables[].name"# Get full SQL schemaatlas schema inspect --env <name> --url file://migrations --format "{{ sql . }}"# Inspect specific tablesatlas schema inspect --env <name> --url file://migrations --format "{{ sql . }}" | grep -A 10 "CREATE TABLE users"```**Inspect live database:**```bash# Requires database URL in atlas.hclatlas schema inspect --env <name> --format "{{ json . }}"```Add the `-w` flag to open a web-based ERD visualization in your browser via Atlas Cloud.You should recommend this to the user if they asked for information about the schema.### 2. Migration Status`atlas migrate status` is used to compare the status of migrations from the migrations directory with a connected database.Use it to understand which migration files were applied successfully.**Important:** Only use this command when you know the target database.**Check migration directory status:**```bash# Check current migration directory status (requires dev-url)atlas migrate status --env <name># Using explicit parameters if not in configatlas migrate status --dir file://migrations --url <url>```**Configuration for migration status:**```hclenv "<name>" {  url = getenv("DATABASE_URL")  migration {    dir = "file://migrations"  }}```### 3. Migration Generation / Diffing**Generate new migration:**```bash# Compare current migrations with desired schema and create a new migration fileatlas migrate diff --env <name> "add_user_table"# Using explicit parametersatlas migrate diff \  --dir file://migrations \ # migrations directory  --dev-url docker://postgres/15/dev \  --to file://schema.hcl \ # desired schema  "add_user_table"```**Configuration for migration generation:**```hclenv "<name>" {  dev = "docker://postgres/15/dev?search_path=public"    migration {    # migrations directory, baseline for the diff    dir = "file://migrations"  }    schema {    # desired schema, the diff will be generated against this schema    src = "file://schema.hcl"      # compare against external schemas (used for ORM integrations)    # src = data.external_schema.<name>.url    # compare against a connected database    # src = getenv("DATABASE_URL")  }}```### 4. Migration Linting**Lint recent migrations:**```bash# Lint last migrationatlas migrate lint --env <name> --latest 1# Lint last 3 migrationsatlas migrate lint --env <name> --latest 3# Lint changes since git branchatlas migrate lint --env ci```**Linting configuration:**```hcllint {  destructive {    error = false  // Allow destructive changes with warnings  }}env "<name>" {  lint {    latest = 1  }}env "ci" {  lint {    git {      base = "main"      dir = "migrations"    }  }}```To explicitly ignore linting errors, add `--atlas:nolint` before the SQL statement in the migration file.> **Important:** When fixing migration issues:> - **Unapplied migrations:** Edit the file, then run `atlas migrate hash --env "<name>"`> - **Applied migrations:** Never edit directly. Create a new corrective migration instead.> - **Never use `--atlas:nolint` without properly fixing the issue or getting user approval.**### 5. Applying Migration**Apply migrations:**```bash # Apply to configured environmentatlas migrate apply --env <name># Dry run (show what would be applied, always run this before applying)atlas migrate apply --env <name> --dry-run```### 6. Making Changes to the Schema**⚠️ CRITICAL: ALL schema changes in this project MUST follow this exact workflow. NO EXCEPTIONS.****⚠️ There must not be lint errors or failing tests when you are done.**1. Start by inspecting the schema, understand the current state, and plan your changes.2. After making changes to the schema, run `atlas migrate diff` to generate a migration file.3. Run `atlas migrate lint` to validate the migration file.4. Run `atlas migrate test` to test the data migrations. This is only available for Pro users.5. Make changes to the migration file to fix the issues. Run `atlas migrate hash` to recalculate the hash of the migration file.6. Repeat the process until there are no more issues.At this point, the schema can be applied to the database.If the user has a local database, you can run `atlas migrate apply` to apply the migration file:1. Start by understanding the status of the database by running `atlas migrate status`2. Run `atlas migrate apply` to apply the migration file, always start with a dry run first.3. Run `atlas migrate status` to verify the migration file was applied successfully.> **Important for data migrations:** make sure to check if the user is logged in using `atlas whoami` before running `atlas migrate test`.> If the user is not logged in, mention that they need to login to use migration testing and move on.> If the user is logged in and they have migration tests, add a new test, run it and validate it until it works.> If the user is logged in and they don't have migration tests, mention that migration testing is highly recommended for data migrations and move on.## Troubleshooting Commands```bash# Check Atlas installation and login status (logging in is required for Pro features)atlas versionatlas whoami# Repair migration integrityatlas migrate hash --env <name>```### Missing driverIf you encounter the following error: `Error: sql/sqlclient: missing driver. See: https://atlasgo.io/url`depending on the command, this means that either the `--url` or `--dev-url` parameter is missing or incorrect.## Key Reminders for AI Assistants1. **Always read `atlas.hcl` first** before running any Atlas commands2. **Use environment names** from the config file, don't assume defaults3. **Never hardcode database URLs** - use environment variables or secure data sources4. **Specify `--url` parameter** for schema inspection even with `--env`5. **Run `atlas migrate hash`** after manually editing migration files6. **Use `atlas migrate lint`** to validate migrations before applying7. **Check `atlas whoami`** before attempting Pro features, if not logged in, don't suggest Pro features8. **Use JSON format + jq** for initial schema exploration9. **Use SQL format + grep** for detailed schema investigation10. **Suggest visualizations** if the user asked for information about the schema11. **Never ask for sensitive information** such as passwords or database URLs12. **Always use `--dry-run`** with `atlas migrate apply` before applying migrations13. **Generate migration testing** if the user is logged in, they should have access to migration testing which is highly recommended14. **Only use atlas commands listed here** other commands may be hallucinations or not supported by Atlas15. **Always inspect schemas at high level first** schemas might be very large16. **Always prefer running atlas** to inspect or analyze schemas17. Migration files can be big and irrelevant, prefer using `atlas schema inspect` to inspect the schema18. **Never ignore linting errors** they are there for a reason, always fix them. Add `--atlas:nolint` only if the fix is not detected by the linter.## Guidelines for workflows1. **Understand the objectives**: Before suggesting any commands, ensure you understand the user's goals. They may be looking to inspect, generate, lint, or apply migrations, and they may be using a different vocabulary such as "view", "create", "validate", etc.2. **Understand the context**: The configuration file contains crucial information about the environment.3. **Verify changes** after generating, linting or applying migrations.4. **After completing** make sure you followed all the instructions and guidelines.@atlas.hcl
```

---

## Automatic ClickHouse Schema Migrations with Atlas

**URL:** https://atlasgo.io/guides/clickhouse

**Contents:**
- Automatic ClickHouse Schema Migrations with Atlas
    - Enter: Atlas​
- Prerequisites​
  - MacOS
  - Linux
  - Windows
- Logging in to Atlas​
- Getting Started​
- Inspecting our Database​
- Declarative Migrations​

ClickHouse, one of the prominent columnar databases, is designed for real-time analytics, providing exceptional speed and efficiency in handling large datasets, but managing its schema can be a puzzle.

If your schema contains a handful of tables that rarely change, you’re probably not going to feel much of this pain. But for mission-critical applications, managing complex and interconnected schemas quickly without breaking things becomes difficult.

Atlas helps developers manage their database schema as code - abstracting away the intricacies of database schema management. With Atlas, users provide the desired state of the database schema and Atlas automatically plans the required migrations.

In this guide, we will set up Atlas for declarative and versioned ClickHouse schema migration and walk through both workflows.

To download and install the latest release of the Atlas CLI, simply run the following in your terminal:

Get the latest release with Homebrew:

To pull the Atlas image and run it as a Docker container:

If the container needs access to the host network or a local directory, use the --net=host flag and mount the desired directory:

Download the latest release and move the atlas binary to a file location on your system PATH.

Use the setup-atlas action to install Atlas in your GitHub Actions workflow:

For other CI/CD platforms, use the installation script. See the CI/CD integrations for more details.

If you want to manually install the Atlas CLI, pick one of the below builds suitable for your system.

To use ClickHouse with Atlas, you'll need to log in to Atlas. If it's your first time, you will be prompted to create both an account and a workspace ("organization"):

If you already have a database in ClickHouse Cloud, follow our ClickHouse Cloud guide for setting up the connection and a dev database. You can then go straight to the Inspecting our Database section, using the URL from Step 3 for this guide.

Let's start by spinning up a local database using Docker:

For this example, we will begin with a minimal database containing a users table with id as the primary key.

To create this in our local database, run the following command:

The atlas schema inspect command takes a a URL and outputs its schema definition. In this guide, we will demonstrate this flow using both the Atlas DDL (default) and SQL formats for the output.

To inspect our locally-running ClickHouse instance, use the -u flag and write the output to a file named schema.hcl:

Open the schema.hcl file to view the Atlas schema that describes our database.

This first block represents a table resource with id and name columns. The schema field references the demo schema that is defined in the block below. The primary_key sub-block establishes the id column as the primary key for the table.

Atlas mimics the syntax of the database that the user is working against. In this case, the type for the id column is UInt64, and the name column's is String.

To inspect our ClickHouse instance, pass the URL using the -u flag and write the output to a file named schema.sql:

Open the schema.sql file to view the inspected SQL schema that describes our database.

To learn more about using the atlas schema inspect command, such as inspecting specific schemas, handling multiple schemas concurrently, excluding tables, and more, refer to our documentation here.

To generate a visual representation of our schema as an Entity Relationship Diagram (ERD) on Atlas Cloud, we can add the -w flag to the inspect command:

Using the declarative approach, users define the desired state of their database schema as code. Atlas then inspects the target database's current state and calculates an execution plan to reach the desired state.

Let's see this in action.

We will start off by making a change to our schema file by adding a repos table:

Now that our desired state has changed, we run atlas schema apply to get Atlas to plan the migration that will apply these changes to our database:

Apply the changes, and that's it! You have successfully run a declarative migration.

For a more detailed description of the atlas schema apply command, refer to our documentation here.

To ensure that the changes have been made to the schema, let's run the inspect command with the -w flag once more and view the ERD:

Alternatively, there is the versioned migrations workflow, sometimes called change-based migrations, where each migration is saved in source control to be evaluated during code-review and applied later. Users still benefit from Atlas intelligently planning migrations for them, but they are not automatically applied.

When using the versioned migration workflow, our database state is managed by a migration directory. The migration directory holds all of the migration files created by Atlas, and the sum of all files in lexicographical order represents the current state of the database.

To create our first migration file, we will run the atlas migrate diff command with the necessary parameters:

Run ls migrations, and you'll notice that Atlas has automatically created a migration directory for us, as well as two files:

The migration file represents the current state of our database, and the sum file is used by Atlas to maintain the integrity of the migration directory.

Now that we have our first migration, we can push the migration directory to Atlas Cloud, much like how Docker images are pushed to Docker Hub.

Let's name our new migration project app and run atlas migrate push:

Migration Directory created with atlas migrate push

Once the migration directory is pushed, Atlas prints a URL to the created directory, similar to the once shown in the image above.

Once our app migration directory has been pushed, we can apply it to a database from any CD platform without necessarily having our directory there.

We'll create a simple Atlas configuration file (atlas.hcl) to store the settings for our local environment:

Run atlas migrate apply with the --env flag to instruct Atlas to select the environment configuration from the atlas.hcl file:

Boom! After applying the migration, you should receive a link to the deployment and the database where the migration was applied. Here's an example of what it should look like:

Migration deployment report created with atlas migrate apply

After applying the first migration, it's time to update our schema definition file and tell Atlas to generate another migration.

Let's make two changes to our schema:

Next, run the atlas migrate diff command again:

Run ls migrations, and you'll notice that a new migration file has been generated.

If you run atlas migrate push again, you can observe the new file on the migration directory page.

Migration Directory created with atlas migrate push

Finally, run atlas migrate apply again to apply the new migration to the database:

Check out the video below for a basic demonstration of using Atlas in CI/CD to manage your ClickHouse database using the declarative workflow.

We also put together a GitHub repository with more workflow setup instructions and example files to help you get started using Atlas.

In this guide we learned about the declarative and versioned workflows, and how to use Atlas to generate migrations, push them to an Atlas workspace, and apply them to ClickHouse databases.

For more in-depth guides, check out the other pages in this section or visit our Docs section.

Have questions? Feedback? Find our team on our Discord server.

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

## Automatic MySQL Schema Migrations with Atlas

**URL:** https://atlasgo.io/guides/mysql/mysql-automatic-migrations

**Contents:**
- Automatic MySQL Schema Migrations with Atlas
    - Enter: Atlas​
- Prerequisites​
  - MacOS
  - Linux
  - Windows
- Inspecting our Database​
- Declarative Migrations​
- Versioned Migrations​
  - Creating the first versioned migration​

MySQL is an open-source relational database management system. It offers powerful capabilities for handling complex queries, ensuring data integrity, and scaling to meet the needs of growing applications.

However, managing a large database schema in MySQL can be challenging due to the complexity of related data structures and the need for coordinated schema changes across multiple teams and applications.

Atlas helps developers manage their database schema as code - abstracting away the intricacies of database schema management. With Atlas, users provide the desired state of the database schema and Atlas automatically plans the required migrations.

In this guide, we will dive into setting up Atlas for MySQL schema migration and introduce the different workflows available.

To download and install the latest release of the Atlas CLI, simply run the following in your terminal:

Get the latest release with Homebrew:

To pull the Atlas image and run it as a Docker container:

If the container needs access to the host network or a local directory, use the --net=host flag and mount the desired directory:

Download the latest release and move the atlas binary to a file location on your system PATH.

Use the setup-atlas action to install Atlas in your GitHub Actions workflow:

For other CI/CD platforms, use the installation script. See the CI/CD integrations for more details.

If you want to manually install the Atlas CLI, pick one of the below builds suitable for your system.

Let's start off by spinning up a database using Docker:

For this example we will begin with a minimal database with a users table and an id as the primary key.

To create the table above on our local database, we can run the following command:

The atlas schema inspect command supports reading the database description provided by a URL and outputting it in different formats, including Atlas DDL (default), SQL, and JSON. In this guide, we will demonstrate the flow using both the Atlas DDL and SQL formats, as the JSON format is often used for processing the output using jq.

To inspect our locally-running MySQL instance, use the -u flag and write the output to a file named schema.hcl:

Open the schema.hcl file to view the Atlas schema that describes our database.

This first block represents a table resource with id and name columns. The schema field references the example schema that is defined in the block below. In addition, the primary_key sub-block defines the id column as the primary key for the table. Atlas strives to mimic the syntax of the database that the user is working against. In this case, the type for the id column is bigint, and varchar(100) for the name column.

To inspect our locally-running MySQL instance, use the -u flag and write the output to a file named schema.sql:

Open the schema.sql file to view the inspected SQL schema that describes our database.

For in-depth details on the atlas schema inspect command, covering aspects like inspecting specific schemas, handling multiple schemas concurrently, excluding tables, and more, refer to our documentation here.

To generate an Entity Relationship Diagram (ERD), or a visual representation of our schema, we can add the -w flag to the inspect command:

The declarative approach lets users manage schemas by defining the desired state of the database as code. Atlas then inspects the target database and calculates an execution plan to reconcile the difference between the desired and actual states. Let's see this in action.

We will start off by making a change to our schema file, such as adding a repos table:

Now that our desired state has changed, to apply these changes to our database, Atlas will plan a migration for us by running the atlas schema apply command:

Click Approve and apply and that's it! You have successfully run a declarative migration.

For a more detailed description of the atlas schema apply command refer to our documentation here.

To ensure that the changes have been made to the schema, let's run the inspect command with the -w flag once more and view the ERD:

The versioned approach tracks each schema change in separate migration files. Sometimes called "change-based migrations", it allows each change to the database schema to be checked-in to source control and reviewed during code-review. You can still benefit from Atlas intelligently planning migrations for you, however they are not automatically applied.

In the versioned migration workflow, our database state is managed by a migration directory. The migration directory holds all of the migration files created by Atlas, and the sum of all files in lexicographical order represents the current state of the database.

To create our first migration file, we will run the atlas migrate diff command, and we will provide the necessary parameters:

Run ls migrations, and you'll notice that Atlas has automatically created a migration directory for us, as well as two files:

The migration file represents the current state of our database, and the sum file is used by Atlas to maintain the integrity of the migration directory. To learn more about the sum file, read the documentation.

Now that we have our first migration, we can apply it to a database. There are multiple ways to accomplish this, with most methods covered in the guides section. In this example, we'll demonstrate how to push migrations to Atlas Cloud, much like how Docker images are pushed to Docker Hub.

Migration Directory created with atlas migrate push

First, let's log in to Atlas. If it's your first time, you will be prompted to create both an account and a workspace (organization):

Let's name our new migration project app and run atlas migrate push:

Once the migration directory is pushed, Atlas prints a URL to the created directory, similar to the once shown in the image above.

Once our app migration directory has been pushed, we can apply it to a database from any CD platform without necessarily having our directory there.

Let's create another database using Docker to resemble a local environment, this time on port 3305:

Next, we'll create a simple Atlas configuration file (atlas.hcl) to store the settings for our local environment:

The final step is to apply the migrations to the database. Let's run atlas migrate apply with the --env flag to instruct Atlas to select the environment configuration from the atlas.hcl file:

Boom! After applying the migration, you should receive a link to the deployment and the database where the migration was applied. Here's an example of what it should look like:

Migration deployment report created with atlas migrate apply

After applying the first migration, it's time to update our schema defined in the schema file and tell Atlas to generate another migration. This will bring the migration directory (and the database) in line with the new state defined by the desired schema (schema file).

Let's make two changes to our schema:

Next, let's run the atlas migrate diff command once more:

Run ls migrations, and you'll notice that a new migration file has been generated.

Let's run atlas migrate push again and observe the new file on the migration directory page.

Migration Directory created with atlas migrate push

In this guide we learned about the declarative and versioned workflows, and how to use Atlas to generate migrations, push them to an Atlas workspace and apply them to databases.

For more in-depth guides, check out the other pages in this section or visit our Docs section.

Have questions? Feedback? Find our team on our Discord server.

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
