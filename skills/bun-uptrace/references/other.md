# Bun-Uptrace - Other

**Pages:** 1

---

## Bun

**URL:** https://bun.uptrace.dev/

**Contents:**
- # Why Bun? Because SQL shouldn't be scary.
  - # Complex queries made elegant
- # Start building in 60 seconds
- # Real-world examples that matter
  - # Type-safe model definitions
  - # Relationships made simple
  - # Migrations that scale

Traditional ORMs force you to learn their DSL and hide your SQL behind layers of abstraction. Bun takes a different approach: embrace SQL, enhance it with Go's type safety.

Transform this complex analytical query from a maintenance nightmare into readable, maintainable Go code:

The generated SQL is exactly what you'd write by hand:

Choose your database and get running immediately:

Ready to write better SQL with Go? Get started in 5 minutes →

**Examples:**

Example 1 (go):
```go
// Build complex queries step by step
regionalSales := db.NewSelect().
	ColumnExpr("region").
	ColumnExpr("SUM(amount) AS total_sales").
	TableExpr("orders").
	GroupExpr("region")

topRegions := db.NewSelect().
	ColumnExpr("region").
	TableExpr("regional_sales").
	Where("total_sales > (SELECT SUM(total_sales) / 10 FROM regional_sales)")

// Compose them into a final query
var results []RegionProduct
err := db.NewSelect().
	With("regional_sales", regionalSales).
	With("top_regions", topRegions).
	ColumnExpr("region, product").
	ColumnExpr("SUM(quantity) AS product_units").
	ColumnExpr("SUM(amount) AS product_sales").
	TableExpr("orders").
	Where("region IN (SELECT region FROM top_regions)").
	GroupExpr("region, product").
	Scan(ctx, &results)
```

Example 2 (sql):
```sql
WITH regional_sales AS (
    SELECT region, SUM(amount) AS total_sales
    FROM orders GROUP BY region
), top_regions AS (
    SELECT region FROM regional_sales
    WHERE total_sales > (SELECT SUM(total_sales)/10 FROM regional_sales)
)
SELECT region, product,
       SUM(quantity) AS product_units,
       SUM(amount) AS product_sales
FROM orders
WHERE region IN (SELECT region FROM top_regions)
GROUP BY region, product
```

Example 3 (go):
```go
package main

import (
	"context"
	"database/sql"
	"fmt"

	"github.com/uptrace/bun"
	"github.com/uptrace/bun/dialect/pgdialect"
	"github.com/uptrace/bun/driver/pgdriver"
	"github.com/uptrace/bun/extra/bundebug"
)

func main() {
	ctx := context.Background()

	// Open a PostgreSQL database
	dsn := "postgres://postgres:@localhost:5432/test?sslmode=disable"
	pgdb := sql.OpenDB(pgdriver.NewConnector(pgdriver.WithDSN(dsn)))

	// Create a Bun db on top of it
	db := bun.NewDB(pgdb, pgdialect.New())

	// Optional: Print queries during development
	db.AddQueryHook(bundebug.NewQueryHook(bundebug.WithVerbose(true)))

	var rnd float64
	// Select a random number - it's that simple!
	if err := db.NewSelect().ColumnExpr("random()").Scan(ctx, &rnd); err != nil {
		panic(err)
	}

	fmt.Println("Random number:", rnd)
}
```

Example 4 (go):
```go
package main

import (
	"context"
	"database/sql"
	"fmt"

	"github.com/uptrace/bun"
	"github.com/uptrace/bun/dialect/sqlitedialect"
	"github.com/uptrace/bun/driver/sqliteshim"
	"github.com/uptrace/bun/extra/bundebug"
)

func main() {
	ctx := context.Background()

	// Perfect for development and testing
	sqlite, err := sql.Open(sqliteshim.ShimName, "file::memory:?cache=shared")
	if err != nil {
		panic(err)
	}

	db := bun.NewDB(sqlite, sqlitedialect.New())
	db.AddQueryHook(bundebug.NewQueryHook(bundebug.WithVerbose(true)))

	var rnd int64
	if err := db.NewSelect().ColumnExpr("random()").Scan(ctx, &rnd); err != nil {
		panic(err)
	}

	fmt.Println("Random number:", rnd)
}
```

---
