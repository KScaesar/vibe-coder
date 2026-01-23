---
name: atlas-schema
description: Atlas is a language-independent tool for managing and migrating database schemas using modern DevOps principles.
---

# Atlas-Schema Skill

Atlas is a language-independent tool for managing and migrating database schemas using modern DevOps principles. It offers two workflows: **Declarative** (state-based) and **Versioned** (migration-based), enabling teams to manage database schemas like application code with features like automatic migration planning, CI/CD integration, and schema validation.

## When to Use This Skill

This skill should be triggered when:

- **Defining Schema as Code**: Managing database schemas using HCL, SQL, or ORM definitions
- **Planning Migrations**: Automatically generating migration scripts for schema changes (versioned workflow)
- **Applying Schema Changes**: Deploying declarative or versioned migrations to databases
- **Setting up CI/CD**: Integrating database schema management into GitHub Actions, GitLab, or other pipelines
- **Connecting to Databases**: Using connection URLs for PostgreSQL, MySQL, MariaDB, SQL Server, SQLite, ClickHouse, and more
- **Inspecting Schemas**: Exporting existing database schemas to code (HCL or SQL)
- **Troubleshooting Migrations**: Handling migration failures, schema drift, or rollback scenarios

## Quick Reference

### Installation

Based on [getting_started.md](references/getting_started.md)

```shell
curl -sSf https://atlasgo.sh | sh
```

### Connection URLs

**Pattern 4: PostgreSQL URL**
Based on [concepts.md](references/concepts.md)

```shell
# Single schema with SSL disabled
postgres://postgres:pass@localhost:5432/database?search_path=public&sslmode=disable

# Multiple schemas (database scope)
postgres://postgres:pass@localhost:5432/database
```

**Pattern 5: MySQL URL**
Based on [concepts.md](references/concepts.md)

```shell
# Single database
mysql://root:pass@localhost:3306/test

# Server scope (all databases)
mysql://root:pass@localhost:3306/
```

**Pattern 6: SQLite URL**
Based on [concepts.md](references/concepts.md)

```shell
# File-based
sqlite://file.db

# In-memory (useful for --dev-url)
sqlite://file?mode=memory&_fk=1
```

**Pattern 7: Docker Dev Database**
Based on [schema_as_code.md](references/schema_as_code.md)

```shell
# MySQL dev database
--dev-url "docker://mysql/8/dev"

# PostgreSQL dev database
--dev-url "docker://postgres/15/dev?search_path=public"
```

### Versioned Migrations Workflow

**Pattern 8: Generate Migration from Schema**
Based on [versioned_workflow.md](references/versioned_workflow.md)

```shell
# From HCL schema
atlas migrate diff create_users \
  --dir "file://migrations" \
  --to "file://schema.hcl" \
  --dev-url "docker://mysql/8/dev"

# From SQL schema
atlas migrate diff add_column \
  --dir "file://migrations" \
  --to "file://schema.sql" \
  --dev-url "docker://postgres/15/dev?search_path=public"
```

**Pattern 9: Apply Versioned Migrations**
Based on [versioned_workflow.md](references/versioned_workflow.md)

```shell
# Apply pending migrations
atlas migrate apply \
  --url "mysql://root:pass@:3306/test" \
  --dir "file://migrations"

# Apply from Atlas Registry
atlas migrate apply \
  --url "mysql://root:pass@:3306/test" \
  --dir "atlas://app"
```

**Pattern 10: Push to Atlas Registry**
Based on [versioned_workflow.md](references/versioned_workflow.md)

```shell
# Login to Atlas
atlas login

# Push migrations
atlas migrate push app \
  --dev-url "docker://postgres/15/dev?search_path=public"
```

### Declarative Workflow

**Pattern 11: Apply Declarative Changes**
Based on [declarative_workflow.md](references/declarative_workflow.md)

```shell
# Apply from HCL schema
atlas schema apply \
  --url "postgres://localhost:5432/db?search_path=public" \
  --to "file://schema.hcl" \
  --dev-url "docker://postgres/15/dev?search_path=public"

# Apply from SQL schema
atlas schema apply \
  --url "mysql://root:pass@:3306/test" \
  --to "file://schema.sql" \
  --dev-url "docker://mysql/8/dev"
```

**Pattern 12: Pre-plan Schema Changes**
Based on [declarative_workflow.md](references/declarative_workflow.md)

```shell
# Generate and approve a migration plan
atlas schema plan \
  --url "mysql://root:pass@:3306/test" \
  --to "file://schema.sql" \
  --dev-url "docker://mysql/8/dev"

# Apply pre-approved plan
atlas schema apply --env prod
```

### Schema Inspection & Export

**Pattern 13: Inspect Database Schema**
Based on [schema_as_code.md](references/schema_as_code.md)

```shell
# Inspect to HCL
atlas schema inspect \
  --url "postgres://localhost:5432/db?search_path=public" \
  > schema.hcl

# Inspect to SQL with split files
atlas schema inspect \
  --url "postgres://localhost:5432/db?search_path=public" \
  --format '{{ sql . | split | write }}'
```

**Pattern 14: Schema Diff**
Based on [declarative_workflow.md](references/declarative_workflow.md)

```shell
# Compare two database states
atlas schema diff \
  --from "mysql://root:pass@:3306/dev" \
  --to "mysql://root:pass@:3306/prod" \
  --dev-url "docker://mysql/8/dev"
```

### Migration Troubleshooting

**Pattern 15: Check Migration Status**
Based on [versioned_workflow.md](references/versioned_workflow.md)

```shell
# View current migration status
atlas migrate status \
  --url "mysql://root:pass@:3306/test" \
  --dir "file://migrations"
```

**Pattern 16: Down Migrations (Rollback)**
Based on [versioned_workflow.md](references/versioned_workflow.md)

```shell
# Revert last migration
atlas migrate down \
  --url "mysql://root:pass@:3306/test" \
  --dir "file://migrations" \
  --dev-url "docker://mysql/8/dev"

# Dry-run to preview changes
atlas migrate down --dry-run \
  --url "mysql://root:pass@:3306/test" \
  --dir "file://migrations" \
  --dev-url "docker://mysql/8/dev"
```

## Core Concepts

### Two Workflows

Atlas supports two distinct migration workflows (Based on [getting_started.md](references/getting_started.md), [versioned_workflow.md](references/versioned_workflow.md), [declarative_workflow.md](references/declarative_workflow.md)):

1. **Versioned Migrations** (Change-based)
   - Define explicit migration files (.sql scripts) applied in sequence
   - Each migration tracked and version-controlled
   - Atlas can auto-generate these files from schema definitions
   - Best for: Teams needing explicit migration review and auditability

2. **Declarative Migrations** (State-based)
   - Define desired schema state (HCL/SQL/ORM)
   - Atlas automatically calculates and applies changes
   - Similar to Terraform's infrastructure-as-code approach
   - Best for: Rapid development and automated environments

### Connection URLs

Atlas uses standard URL format for database connections (Based on [concepts.md](references/concepts.md)):

```
driver://[username[:password]@]address/[schema|database][?param1=value1&...&paramN=valueN]
```

**Key URL Components:**

- **Driver**: `postgres`, `mysql`, `maria`, `sqlite`, `sqlserver`, `clickhouse`, etc.
- **Credentials**: Username and password (URL-encoded if containing special characters)
- **Schema Scope**: Determines if Atlas operates on single schema or multiple schemas
- **Query Parameters**: Database-specific options (e.g., `sslmode`, `search_path`)

**Special URL Schemes:**

- `docker://mysql/8/dev` - Ephemeral dev database in Docker
- `file://schema.sql` - Load schema from file
- `atlas://app` - Load from Atlas Registry
- `env://src` - Reference from data source

### Schema as Code

Atlas supports multiple formats for defining database schemas (Based on [schema_as_code.md](references/schema_as_code.md)):

**SQL Format:**

```sql
CREATE TABLE users (
  id bigint PRIMARY KEY,
  name varchar(255) NOT NULL
);

CREATE TABLE posts (
  id bigint PRIMARY KEY,
  title varchar(255) NOT NULL,
  author_id bigint NOT NULL,
  FOREIGN KEY (author_id) REFERENCES users(id)
);
```

**HCL Format:**

```hcl
schema "public" {}

table "users" {
  schema = schema.public
  column "id" {
    type = bigint
  }
  column "name" {
    type = varchar(255)
    null = false
  }
  primary_key {
    columns = [column.id]
  }
}
```

**ORM Integration:**

- SQLAlchemy, Django, GORM, Ent, Prisma, TypeORM, Sequelize, etc.
- Define schema in ORM, let Atlas generate migrations

### Dev Database

The Dev Database is a temporary database used by Atlas for computation and validation (Based on [schema_as_code.md](references/schema_as_code.md)):

- Required when working with SQL schemas or certain HCL features
- Can be ephemeral Docker container: `docker://mysql/8/dev`
- Atlas ensures it's clean before use and cleans up after
- Never contains production data

## Working with Versioned Migrations

### Creating Migrations

Generate migration files automatically from schema definitions (Based on [versioned_workflow.md](references/versioned_workflow.md)):

```shell
# Initial migration
atlas migrate diff create_users \
  --dir "file://migrations" \
  --to "file://schema.sql" \
  --dev-url "docker://mysql/8/dev"

# Subsequent changes
atlas migrate diff add_email \
  --dir "file://migrations" \
  --to "file://schema.sql" \
  --dev-url "docker://mysql/8/dev"
```

### Migration Directory Structure

```
migrations/
├── 20240101120000_create_users.sql
├── 20240102150000_add_email.sql
└── atlas.sum  # Integrity checksum file
```

### Applying Migrations

```shell
# Apply all pending migrations
atlas migrate apply \
  --url "mysql://root:pass@:3306/test" \
  --dir "file://migrations"

# Apply from Atlas Registry
atlas migrate apply \
  --url "mysql://root:pass@:3306/test" \
  --dir "atlas://app"
```

### Migration Troubleshooting

Common scenarios (Based on [versioned_workflow.md](references/versioned_workflow.md)):

**1. Check Status:**

```shell
atlas migrate status \
  --url "mysql://root:pass@:3306/test" \
  --dir "file://migrations"
```

**2. Handle Schema Drift:**

```shell
# Compare actual vs expected state
atlas schema diff \
  --from "mysql://root:pass@:3306/test" \
  --to "file://migrations?version=20240102150000" \
  --dev-url "docker://mysql/8/dev"
```

**3. Rollback Migrations:**

```shell
# Revert last migration
atlas migrate down \
  --url "mysql://root:pass@:3306/test" \
  --dir "file://migrations" \
  --dev-url "docker://mysql/8/dev"
```

## Working with Declarative Migrations

### Basic Workflow

1. Define desired schema state
2. Let Atlas calculate changes
3. Review and approve
4. Apply to database

(Based on [declarative_workflow.md](references/declarative_workflow.md))

```shell
# Apply changes
atlas schema apply \
  --url "mysql://root:pass@:3306/test" \
  --to "file://schema.sql" \
  --dev-url "docker://mysql/8/dev"
```

### Pre-planning (Pro Feature)

Pre-plan migrations for review before applying (Based on [declarative_workflow.md](references/declarative_workflow.md)):

```shell
# Generate plan
atlas schema plan \
  --url "mysql://root:pass@:3306/test" \
  --to "file://schema.sql" \
  --dev-url "docker://mysql/8/dev"

# Apply approved plan
atlas schema apply --env prod
```

### Review Policies

Control when manual approval is required (Based on [declarative_workflow.md](references/declarative_workflow.md)):

```hcl
lint {
  review = ERROR  # Require review only on errors
  # review = WARNING  # Require review on warnings
  # review = ALWAYS  # Always require review
}
```

## CI/CD Integration

### Setup CI/CD

Atlas integrates with major CI/CD platforms (Based on [versioned_workflow.md](references/versioned_workflow.md), [declarative_workflow.md](references/declarative_workflow.md)):

- GitHub Actions
- GitLab CI Components
- CircleCI Orbs
- Bitbucket Pipes
- Azure DevOps Pipelines

**Common CI Workflow:**

1. **Lint migrations** - Detect destructive changes
2. **Run tests** - Validate schema logic
3. **Push to registry** - Store approved migrations
4. **Deploy** - Apply to target databases

### GitHub Actions Example

```yaml
- uses: ariga/atlas-action/migrate/lint@v1
  with:
    dir: file://migrations
    dev-url: docker://mysql/8/dev

- uses: ariga/atlas-action/migrate/push@v1
  with:
    dir: file://migrations
```

## Other Reference Materials

This skill contains 13 categorized reference files located in `references/`:

**Core References (Primary Focus):**

- `concepts.md` - Connection URLs, database scopes, SSL configuration
- `getting_started.md` - Installation, quickstart, first migrations
- `versioned_workflow.md` - Migration planning, applying, troubleshooting
- `declarative_workflow.md` - Schema apply, plan, review policies
- `schema_as_code.md` - HCL/SQL schemas, inspection, ORM integration

**Additional References:**

- `guides.md` - 70 practical guides (database-specific, CI/CD, deployment)
- `testing.md` - Schema and migration testing
- `integrations.md` - GitHub Actions, Kubernetes, Terraform
- `cloud.md` - Atlas Cloud features and setup
- `linting.md` - Migration linting and policy enforcement
- `hcl_reference.md` - HCL language reference
- `reference.md` - CLI command reference
- `other.md` - FAQ, features, community links

## Working with This Skill

### For Beginners

1. Start with `getting_started.md` for installation and first migration
2. Review `concepts.md` to understand connection URLs
3. Choose workflow: `versioned_workflow.md` or `declarative_workflow.md`
4. Refer to `schema_as_code.md` for defining schemas

### For CI/CD Setup

1. Review workflow setup in `versioned_workflow.md` or `declarative_workflow.md`
2. Check `integrations.md` for platform-specific examples
3. Configure linting policies from `linting.md`
4. Explore `guides.md` for platform-specific deployment guides

### For Specific Databases

Search `guides.md` for database-specific guides:

- PostgreSQL features (partial indexes, serial columns, RLS)
- MySQL/MariaDB specifics
- SQL Server, ClickHouse, Oracle, Spanner, Snowflake

## Notes

- Atlas Pro: Some features require Atlas Pro license (views, triggers, functions, procedures, testing)
- For the most up-to-date information, consult the official Atlas documentation at https://atlasgo.io.
