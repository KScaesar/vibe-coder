---
name: bun-uptrace
description: Bun is a SQL-first database client for Go. This skill covers the comprehensive guide, querying, models, migrations, and PostgreSQL specific features.
---

# Bun-Uptrace Skill

Bun is a SQL-first database client for Go. Unlike traditional ORMs that hide SQL behind heavy abstractions, Bun embraces SQL, enhancing it with Go's type safety. This skill synthesizes documentation to help you query, model, and migrate your databases effectively.

## When to Use This Skill

Use this skill when you need to:

- **Set up Database Connections**: Configure Bun for PostgreSQL, MySQL, or SQLite.
- **Write Queries**: Build complex SQL queries using Go's type-safe builder (Select, Insert, Update, Delete).
- **Manage Migrations**: Create and run schema migrations using Go code or SQL files.
- **Implement Hooks**: Add logic before/after model events (e.g., updating timestamps).
- **Optimize Performance**: Tune PostgreSQL settings or optimize specific queries.
- **Use Advanced Features**: Utilize PostgreSQL specific features like Arrays, JSONB, or COPY commands.

## Quick Reference

### 1. Database Connection

Based on [other.md](references/other.md)

**PostgreSQL Connection:**

```go
import (
	"database/sql"
	"github.com/uptrace/bun"
	"github.com/uptrace/bun/dialect/pgdialect"
	"github.com/uptrace/bun/driver/pgdriver"
)

dsn := "postgres://user:pass@localhost:5432/dbname?sslmode=disable"
// pgdriver.NewConnector is recommended over basic sql.Open
sqldb := sql.OpenDB(pgdriver.NewConnector(pgdriver.WithDSN(dsn)))
db := bun.NewDB(sqldb, pgdialect.New())
```

**SQLite Connection (In-Memory):**

```go
import (
    "database/sql"
    "github.com/uptrace/bun"
    "github.com/uptrace/bun/dialect/sqlitedialect"
    "github.com/uptrace/bun/driver/sqliteshim"
)

sqldb, _ := sql.Open(sqliteshim.ShimName, "file::memory:?cache=shared")
db := bun.NewDB(sqldb, sqlitedialect.New())
```

### 2. Complex Query Building (CTEs)

Based on [other.md](references/other.md) - Demonstrating how Bun maps SQL constructs to Go

```go
// Define subqueries
regionalSales := db.NewSelect().
	ColumnExpr("region").
	ColumnExpr("SUM(amount) AS total_sales").
	TableExpr("orders").
	GroupExpr("region")

topRegions := db.NewSelect().
	ColumnExpr("region").
	TableExpr("regional_sales").
	Where("total_sales > (SELECT SUM(total_sales) / 10 FROM regional_sales)")

// Compose main query using CTEs (With)
err := db.NewSelect().
	With("regional_sales", regionalSales).
	With("top_regions", topRegions).
	ColumnExpr("region, product").
	TableExpr("orders").
	Where("region IN (SELECT region FROM top_regions)").
	Scan(ctx, &results)
```

### 3. Migrations

Based on [getting_started.md](references/getting_started.md)

**Go-based Migration Structure:**

```go
package migrations

import (
	"context"
	"fmt"
	"github.com/uptrace/bun"
	"github.com/uptrace/bun/migrate"
)

var Migrations = migrate.NewMigrations()

func init() {
	Migrations.MustRegister(func(ctx context.Context, db *bun.DB) error {
		fmt.Print(" [up migration] ")
		_, err := db.NewCreateTable().Model((*User)(nil)).Exec(ctx)
		return err
	}, func(ctx context.Context, db *bun.DB) error {
		fmt.Print(" [down migration] ")
		_, err := db.NewDropTable().Model((*User)(nil)).Exec(ctx)
		return err
	})
}
```

**SQL-based Migration (`.up.sql`):**

```sql
CREATE TABLE users (id serial PRIMARY KEY, name text);

--bun:split

INSERT INTO users (name) VALUES ('Alice');
```

### 4. Model Hooks

Based on [getting_started.md](references/getting_started.md) - Automatically updating timestamps

```go
type Model struct {
    ID        int64
    CreatedAt time.Time
    UpdatedAt time.Time
}

// Compile-time check
var _ bun.BeforeAppendModelHook = (*Model)(nil)

func (m *Model) BeforeAppendModel(ctx context.Context, query bun.Query) error {
	switch query.(type) {
	case *bun.InsertQuery:
		m.CreatedAt = time.Now()
	case *bun.UpdateQuery:
		m.UpdatedAt = time.Now()
	}
	return nil
}
```

### 5. PostgreSQL Arrays

Based on [postgres.md](references/postgres.md)

```go
import "github.com/uptrace/bun/dialect/pgdialect"

type Article struct {
	ID	 int64
	Tags []string `bun:",array"` // Use array tag
}

// Scanning arrays
var tags []string
err := db.NewSelect().
	Model((*Article)(nil)).
	ColumnExpr("tags").
	Where("id = ?", 1).
	Scan(ctx, pgdialect.Array(&tags))

// Querying with array operators
q.Where("tags @> ?", pgdialect.Array([]string{"foo"}))
```

### 6. Debugging Queries

Based on [other.md](references/other.md) and [getting_started.md](references/getting_started.md)

```go
import "github.com/uptrace/bun/extra/bundebug"

// Print all queries to stdout
db.AddQueryHook(bundebug.NewQueryHook(bundebug.WithVerbose(true)))
```

## Reference Files

This skill synthesizes information from the following files in `references/`:

- **getting_started.md** (High Confidence): The core manual. Covers installation, database connection, migrations (Go & SQL), and hooks.
- **other.md** (High Confidence): Practical examples of complex queries, CTEs, and specific driver setups.
- **postgres.md** (Medium Confidence): Specific features for PostgreSQL users, including array support, `COPY` commands, and ZFS tuning.
- **essentials.md** (Medium Confidence): Best practices for zero-downtime migrations and transaction handling.
- **advanced.md** (Medium Confidence): Performance tuning for PostgreSQL configuration (`max_connections`, `shared_buffers`).

## Working with This Skill

### For Beginners

1. **Installation**: Refer to `getting_started.md` for `go get` commands.
2. **First Query**: Look at `other.md` for simple `NewSelect()` examples.
3. **Debug**: Always enable `bundebug` (see Quick Reference) when learning to see the generated SQL.

### For Intermediate Users (Migrations & Modeling)

1. **Migrations**: `getting_started.md` details the migration system. Remember to use transaction-safe migrations where possible.
2. **Hooks**: Use `BeforeAppendModel` for automatic timestamps, but avoid putting complex business logic in hooks (per `getting_started.md`).
3. **Relationships**: See `other.md` for `With` (CTE) and relationship handling.

### For Advanced Users (Performance & PostgreSQL)

1. **Tuning**: Check `advanced.md` for `postgresql.conf` recommendations based on CPU/RAM.
2. **Bulk Data**: Use `CopyFrom` / `CopyTo` from `postgres.md` for large datasets instead of standard inserts.
3. **Zero-Downtime**: Follow the strategies in `essentials.md` (e.g., splitting long transactions, avoiding `NOT NULL` on new columns).

## Known Discrepancies & Notes

- **Migration Files**: While `getting_started.md` describes the standard migration file format (timestamp_name), `essentials.md` focuses on the _strategy_ (locking, batching) rather than the syntax. Combine both: use the syntax from Getting Started with the safety rules from Essentials.
- **Configuration**: Performance tuning values in `advanced.md` (e.g., `shared_buffers = 20-40% of RAM`) are standard PostgreSQL recommendations and not specific to Bun, but are critical for production deployments.

## Resources

### references/

- `getting_started.md`: Setup, Migrations, Hooks.
- `other.md`: Dialects, Complex Queries.
- `postgres.md`: PG-specific types and tools.
- `advanced.md`: Server configuration.
- `essentials.md`: Operational best practices.
