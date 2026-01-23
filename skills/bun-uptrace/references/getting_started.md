# Bun-Uptrace - Getting Started

**Pages:** 31

---

## # Migrations [PostgreSQL MySQL]

**URL:** https://bun.uptrace.dev/guide/migrations.html

**Contents:**
- # Migrations [PostgreSQL MySQL]
- # Migration names
- # Migration status
- # Migration groups and rollbacks
- # Go-based migrations
- # SQL-based migrations

You can write migrations to change database schema or data. A migration can be a regular Go function or a text file with SQL commands.

You should put each migration into a separate file. A migration file names consists of an unique migration name (20210505110026) and a comment (add_foo_column), for example, 20210505110026_add_foo_column.go.

Bun stores the completed migration names in the bun_migrations table to decide which migrations to run. It also uses that information to rollback migrations.

When a migration fails, Bun still marks the migration as applied so you can rollback the partially applied migration to cleanup the database and try to run the migration again.

When there are multiple migrations to run, Bun runs migrations together as a group. During rollbacks, Bun reverts the last migration group (not a single migration). Usually that is desirable, because it rolls the db back to the last known stable state.

To rollback a single migration, you need to rollback the last group, delete the migration(s) you want to skip, and run migrations again. Alternatively, you can add a new migration with the changes you need.

A Go-based migration is a regular Go function that can execute arbitrary code. Each such function must be registered in a migration collection that is created in main.go file:

Then, in a separate files, you should define and register migrations using MustRegister method, for example, in 20210505110026_test_migration.go:

See bun-starter-kit and exampleopen in new window for details.

A SQL-based migration is a file with .up.sql extension that contains one or more SQL commands. You can use --bun:split line as a separator to create migrations with multiple statements.

You can register such migrations using Discover method:

To create a transactional migration, use .tx.up.sql extension.

See bun-starter-kit and exampleopen in new window for details.

**Examples:**

Example 1 (go):
```go
package migrations

import (
	"github.com/uptrace/bun/migrate"
)

// A collection of migrations.
var Migrations = migrate.NewMigrations()
```

Example 2 (go):
```go
package migrations

import (
	"context"
	"fmt"

	"github.com/uptrace/bun"
)

func init() {
	Migrations.MustRegister(func(ctx context.Context, db *bun.DB) error {
		fmt.Print(" [up migration] ")
		return nil
	}, func(ctx context.Context, db *bun.DB) error {
		fmt.Print(" [down migration] ")
		return nil
	})
}
```

Example 3 (sql):
```sql
SELECT 1

--bun:split

SELECT 2
```

Example 4 (go):
```go
//go:embed *.sql
var sqlMigrations embed.FS

func init() {
	if err := Migrations.Discover(sqlMigrations); err != nil {
		panic(err)
	}
}
```

---

## # Model and query hooks

**URL:** https://bun.uptrace.dev/guide/hooks.html

**Contents:**
- # Model and query hooks
- # Introduction
- # Disclaimer
- # Model hooks
  - # BeforeAppendModel
  - # Before/AfterScanRow
  - # Model query hooks
- # Query hooks

Hooks are user-defined functions that are called before and/or after certain operations, for example, before every processed query.

To ensure that your model implements a hook interface, use compile time checksopen in new window, for example, var _ bun.QueryHook = (*MyHook)(nil).

It may sound like a good idea to use hooks for validation or caching because this way you can't forget to sanitize data or check permissions. It gives false sense of safety.

Don't do that. Code that uses hooks is harder to read, understand, and debug. It is more complex and error-prone. Instead, prefer writing simple code like thisopen in new window even if that means repeating yourself:

To update certain fields before inserting or updating a model, use bun.BeforeAppendModelHook which is called just before constructing a query. For exampleopen in new window:

Bun also calls BeforeScanRow and AfterScanRow hooks before and after scanning row values. For exampleopen in new window:

You can also define model query hooks that are called before and after executing certain type of queries on a certain model. Such hooks are called once for a query and using a nil model. To access the query data, use query.GetModel().Value().

Bun supports query hooks which are called before and after executing a query. Bun uses query hooks for logging queries and for performance monitoring.

**Examples:**

Example 1 (go):
```go
func InsertUser(ctx context.Context, db *bun.DB, user *User) error {
	// before insert

	if _, err := db.NewInsert().Model(user).Exec(ctx); err != nil {
		return err
	}

	// after insert

	return nil
}
```

Example 2 (go):
```go
type Model struct {
    ID        int64
    CreatedAt time.Time
    UpdatedAt time.Time
}

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

Example 3 (go):
```go
type Model struct{}

var _ bun.BeforeScanRowHook = (*Model)(nil)

func (m *Model) BeforeScanRow(ctx context.Context) error { return nil }

var _ bun.AfterScanRowHook = (*Model)(nil)

func (m *Model) AfterScanRow(ctx context.Context) error { return nil }
```

Example 4 (go):
```go
var _ bun.BeforeSelectHook = (*Model)(nil)

func (*Model) BeforeSelect(ctx context.Context, query *bun.SelectQuery) error { return nil }

var _ bun.AfterSelectHook = (*Model)(nil)

func (*Model) AfterSelect(ctx context.Context, query *bun.SelectQuery) error { return nil }

var _ bun.BeforeInsertHook = (*Model)(nil)

func (*Model) BeforeInsert(ctx context.Context, query *bun.InsertQuery) error { nil }

var _ bun.AfterInsertHook = (*Model)(nil)

func (*Model) AfterInsert(ctx context.Context, query *bun.InsertQuery) error { return nil }

var _ bun.BeforeUpdateHook = (*Model)(nil)

func (*Model) BeforeUpdate(ctx context.Context, query *bun.UpdateQuery) error { return nil }

var _ bun.AfterUpdateHook = (*Model)(nil)

func (*Model) AfterUpdate(ctx context.Context, query *bun.UpdateQuery) error { return nil }

var _ bun.BeforeDeleteHook = (*Model)(nil)

func (*Model) BeforeDelete(ctx context.Context, query *bun.DeleteQuery) error { return nil }

var _ bun.AfterDeleteHook = (*Model)(nil)

func (*Model) AfterDelete(ctx context.Context, query *bun.DeleteQuery) error { return nil }

var _ bun.BeforeCreateTableHook = (*Model)(nil)

func (*Model) BeforeCreateTable(ctx context.Context, query *CreateTableQuery) error { return nil }

var _ bun.AfterCreateTableHook = (*Model)(nil)

func (*Model) AfterCreateTable(ctx context.Context, query *CreateTableQuery) error { return nil }

var _ bun.BeforeDropTableHook = (*Model)(nil)

func (*Model) BeforeDropTable(ctx context.Context, query *DropTableQuery) error { return nil }

var _ bun.AfterDropTableHook = (*Model)(nil)

func (*Model) AfterDropTable(ctx context.Context, query *DropTableQuery) error { return nil }
```

---

## # Golang ORM for PostgreSQL and MySQL

**URL:** https://bun.uptrace.dev/guide/golang-orm.html

**Contents:**
- # Golang ORM for PostgreSQL and MySQL
- # Why Choose Bun?
- # Installation
- # Quick Start
- # Connecting to Different Databases
  - # PostgreSQL
  - # MySQL
  - # SQLite
- # Connection Pool Configuration
- # Using Bun with Existing Code

Bun is a SQL-first Golang ORM (Object-Relational Mapping) that supports PostgreSQL, MySQL, MSSQL, and SQLite. It aims to provide a simple and efficient way to work with databases while utilizing Go's type safety and reducing boilerplate code.

Bun stands out from other Go ORMs by being SQL-first rather than trying to hide SQL from you. This approach offers several advantages:

To install Bun and the database driver you need:

Here's a complete example to get you started:

Configure your database connection pool for optimal performance:

Learning all Bun capabilities may take some time, but you can start using it right away by executing manually crafted queries and allowing Bun to scan results for you:

If you already have code that uses *sql.Tx or *sql.Conn, you can still use Bun query builder without rewriting the existing code:

Bun uses struct-based models to construct queries and scan results. Models define your database schema using Go structs with struct tags.

Bun provides flexible scanning options for different use cases:

Bun supports various relationship types with automatic JOIN generation:

A: Bun provides migration support through the bun/migrate package:

A: Absolutely! Bun is built on top of database/sql and can coexist with existing code. You can gradually migrate to Bun's query builder while keeping your current SQL queries.

A: Use pointer types or sql.Null* types:

A: Bun adds minimal overhead over raw SQL. In most cases, the performance difference is negligible (< 5%), while providing significant benefits in terms of type safety and developer productivity.

A: Use WhereGroup for complex logic:

By now, you should have a comprehensive understanding of Bun's capabilities. To continue learning:

Read the Core Documentation

Explore Advanced Features

Production Considerations

**Examples:**

Example 1 (bash):
```bash
# Core Bun package
go get github.com/uptrace/bun@latest

# Database drivers (choose one or more)
go get github.com/uptrace/bun/driver/pgdriver        # PostgreSQL
go get github.com/uptrace/bun/driver/sqliteshim     # SQLite
go get github.com/go-sql-driver/mysql               # MySQL
go get github.com/denisenkom/go-mssqldb             # SQL Server
```

Example 2 (go):
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

// User model
type User struct {
    bun.BaseModel `bun:"table:users,alias:u"`

    ID    int64  `bun:",pk,autoincrement"`
    Name  string `bun:",notnull"`
    Email string `bun:",unique"`
}

func main() {
    ctx := context.Background()

    // Open database connection
    sqldb, err := sql.Open(sqliteshim.ShimName, "file::memory:?cache=shared")
    if err != nil {
        panic(err)
    }
    defer sqldb.Close()

    // Create Bun database instance
    db := bun.NewDB(sqldb, sqlitedialect.New())

    // Add query debugging (optional)
    db.AddQueryHook(bundebug.NewQueryHook(
        bundebug.WithVerbose(true),
    ))

    // Create table
    _, err = db.NewCreateTable().Model((*User)(nil)).IfNotExists().Exec(ctx)
    if err != nil {
        panic(err)
    }

    // Insert user
    user := &User{Name: "John Doe", Email: "john@example.com"}
    _, err = db.NewInsert().Model(user).Exec(ctx)
    if err != nil {
        panic(err)
    }

    // Select user
    var selectedUser User
    err = db.NewSelect().Model(&selectedUser).Where("email = ?", "john@example.com").Scan(ctx)
    if err != nil {
        panic(err)
    }

    fmt.Printf("User: %+v\n", selectedUser)
}
```

Example 3 (go):
```go
import (
    "github.com/uptrace/bun"
    "github.com/uptrace/bun/dialect/pgdialect"
    "github.com/uptrace/bun/driver/pgdriver"
)

// Using pgdriver (recommended)
sqldb := sql.OpenDB(pgdriver.NewConnector(
    pgdriver.WithDSN("postgres://user:password@localhost:5432/dbname?sslmode=disable"),
))
db := bun.NewDB(sqldb, pgdialect.New())

// Or using lib/pq
import _ "github.com/lib/pq"
sqldb, err := sql.Open("postgres", "postgres://user:password@localhost/dbname?sslmode=disable")
db := bun.NewDB(sqldb, pgdialect.New())
```

Example 4 (go):
```go
import (
    "github.com/uptrace/bun/dialect/mysqldialect"
    _ "github.com/go-sql-driver/mysql"
)

sqldb, err := sql.Open("mysql", "user:password@tcp(localhost:3306)/dbname?parseTime=true")
if err != nil {
    panic(err)
}
db := bun.NewDB(sqldb, mysqldialect.New())
```

---

## # ORM: Table relationships

**URL:** https://bun.uptrace.dev/guide/relations.html

**Contents:**
- # ORM: Table relationships
- # Introduction
- # Has one relation
- # Belongs to relation
- # Has many relation
- # Polymorphic has many relation
- # Many to many relation

Bun can help you join and query other tables if you are using one of the 4 supported table relations:

For example, you can define Author belongs to Book relation:

And then use Relation method to join tables:

You can query from parent the child and vice versa in an has-one/belongs-to relation:

To select only book ID and the associated author id:

To select a book and join the author without selecting it:

To simulate INNER JOIN instead of LEFT JOIN:

To define a has-one relationship, add bun:"rel:has-one" tag to the field. In the following exampleopen in new window, we have User model that has one Profile model.

You can specify multiple join columns, for example, join:id=user_id,join:vendor_id=vendor_id.

To define a belongs-to relationship, you need to add bun:"rel:belongs-to" tag to the field. In the the following exampleopen in new window we define Profile model that belongs to User model.

You can specify multiple join columns, for example, join:profile_id=id,join:vendor_id=vendor_id.

To define a has-many relationship, add bun:"rel:has-many" to the field. In the following exampleopen in new window, we have User model that has many Profile models.

You can specify multiple join columns, for example, join:id=user_id,join:vendor_id=vendor_id.

You can also define a polymorphic has-many relationship by using type virtual column and polymorphic option.

In the following exampleopen in new window, we store all comments in a single table but use trackable_type column to save the model table to which this comment belongs to.

To override polymorphic model name that Bun stores in the database, you can use polymorphic:model_name:

The Bun will generate the following query:

To define a many-to-many relationship, add bun:"m2m:order_to_items" to the field. You also need to define two has-one relationships on the intermediary model and manually register the model (db.RegisterModel).

In the following exampleopen in new window, we have Order model that can have many items and each Item can be added to multiple orders. We also use OrderToItem model as an intermediary table to join orders and items.

**Examples:**

Example 1 (go):
```go
type Book struct {
	ID		 int64
	AuthorID int64
	Author	 Author `bun:"rel:belongs-to,join:author_id=id"`
}

type Author struct {
	ID int64
}
```

Example 2 (go):
```go
err := db.NewSelect().
	Model(book).
	Relation("Author").
	Where("id = 1").
	Scan(ctx)
```

Example 3 (sql):
```sql
SELECT
  "book"."id", "book"."title", "book"."text",
  "author"."id" AS "author__id", "author"."name" AS "author__name"
FROM "books"
LEFT JOIN "users" AS "author" ON "author"."id" = "book"."author_id"
WHERE id = 1
```

Example 4 (go):
```go
type Profile struct {
	ID     int64 `bun:",pk"`
	Lang   string
	UserID int64
	User *User `bun:"rel:belongs-to"`
}

type User struct {
	ID      int64 `bun:",pk"`
	Name    string
	Profile *Profile `bun:"rel:has-one"`
}

err := db.NewSelect().
	Model(&user).
	Where("id = 1").
	Relation("Profile").
	Scan(ctx)

err := db.NewSelect().
	Model(&profile).
	Where("id = 1").
	Relation("User").
	Scan(ctx)
```

---

## Supported PostgreSQL drivers

**URL:** https://bun.uptrace.dev/postgres/

**Contents:**
- Supported PostgreSQL drivers
- # Supported drivers
  - # pgdriver
    - # pgdriver.Error
    - # Debugging
  - # pgx
- # PgBouncer
- # ZFS
- # Backups
- # Monitoring your database

Bun comes with its own PostgreSQL driver called pgdriveropen in new window that allows connecting to a PostgreSQL database using a DSN (connection string):

You can specify the following options in a DSN:

pgdriver treats all unknown options as PostgreSQL configuration parameters, for example, ?search_path=my_search_path executes the following query whenever a connection is created:

In addition to DSN, you can also use pgdriver.Optionopen in new window to configure the driver:

Or use a DSN and driver options together:

pgdriver exposes Erroropen in new window type to work with PostgreSQL errors:

If you suspect an issue with pgdriver, try to replace it with pgx and check if the problem goes away.

As an alternative to pgdriver, you can also use pgxopen in new window with pgdialect. With pgx, you can disable implicit prepared statements, because Bun does not benefit from using them:

Starting from v5, you can also use pgxpool like this:

To achieve better performance, you can use a server-side connection pool like PgBounceropen in new window. The pool that comes with sql.DB is a client-side pool and it doesn't replace a server-side pool provided by PgBouncer.

If you store large amounts of data (> 100 gigabytes), consider using ZFS filesystem which enables 2-3x data compression and efficient ARC cache. See:

To backup PostgreSQL database, consider using PgBackRest with S3.

**Examples:**

Example 1 (go):
```go
import (
	"github.com/uptrace/bun"
	"github.com/uptrace/bun/dialect/pgdialect"
	"github.com/uptrace/bun/driver/pgdriver"
)

dsn := "postgres://postgres:@localhost:5432/test?sslmode=disable"
// dsn := "unix://user:pass@dbname/var/run/postgresql/.s.PGSQL.5432"
sqldb := sql.OpenDB(pgdriver.NewConnector(pgdriver.WithDSN(dsn)))

db := bun.NewDB(sqldb, pgdialect.New())
```

Example 2 (sql):
```sql
SET search_path TO 'my_search_path'
```

Example 3 (go):
```go
pgconn := pgdriver.NewConnector(
	pgdriver.WithNetwork("tcp"),
	pgdriver.WithAddr("localhost:5437"),
	pgdriver.WithTLSConfig(&tls.Config{InsecureSkipVerify: true}),
	pgdriver.WithUser("test"),
	pgdriver.WithPassword("test"),
	pgdriver.WithDatabase("test"),
	pgdriver.WithApplicationName("myapp"),
	pgdriver.WithTimeout(5 * time.Second),
	pgdriver.WithDialTimeout(5 * time.Second),
	pgdriver.WithReadTimeout(5 * time.Second),
	pgdriver.WithWriteTimeout(5 * time.Second),
	pgdriver.WithConnParams(map[string]interface{}{
		"search_path": "my_search_path",
	}),
)
```

Example 4 (go):
```go
pgconn := pgdriver.NewConnector(
    pgdriver.WithDSN("postgres://postgres:@localhost:5432/test?sslmode=verify-full"),
    pgdriver.WithTLSConfig(tlsConfig),
)
```

---

## # Fixtures

**URL:** https://bun.uptrace.dev/guide/fixtures.html

**Contents:**
- # Fixtures
- # Creating fixtures
- # Loading fixtures
- # Retrieving fixture data
- # Field names
- # Source code

You can use fixtures to load initial data into a database for testing or demonstration purposes. You can write fixtures in YAML format and load them on demand from tests or Go-based migrations.

A fixture is a plain YAML file with the ability to use text/templateopen in new window expressions to generate values. Bun unmarshals YAML data into Go models using yaml.v3open in new window and then saves the model in a database.

Here is how a fixture for a User model might look like:

A single fixture can contain data for multiple models. You can also use the _id field to name rows and reference them from other models using text/template syntax:

Assuming the fixture is stored in testdata/fixture.yml, you can load it with the following code:

By using fixture.WithRecreateTables() option, you can make bun drop existing tables and replace them with new ones. Or you can use fixture.WithTruncateTables() option to truncate tables.

You can also register and use in fixtures custom template functions:

Later you can retrieve the loaded models using Row and MustRow methods:

You can also retrieve rows without _id field by a primary key:

Bun uses SQL column names to find the matching struct field and then calls yaml.v3open in new window to unmarshal the data. So when unmarshaling into a struct field, you may need to use yaml tag to override the default YAML field name.

You can find the source code for the example above on GitHubopen in new window.

**Examples:**

Example 1 (yaml):
```yaml
- model: User
  rows:
    - name: John Smith
      email: john@smith.com
      created_at: '{{ now }}'
    - name: Jonh Doe
      email: john@doe.com
      created_at: '{{ now }}'
```

Example 2 (yaml):
```yaml
- model: User
  rows:
    - _id: smith
      name: John Smith
      email: john@smith.com
      created_at: '{{ now }}'
    - _id: doe
      name: Jonh Doe
      email: john@doe.com
      created_at: '{{ now }}'

- model: Org
  rows:
    - name: "{{ $.User.smith.Name }}'s Org"
      owner_id: '{{ $.User.smith.ID }}'
    - name: "{{ $.User.doe.Name }}'s Org"
      owner_id: '{{ $.User.doe.ID }}'
```

Example 3 (go):
```go
// Let the db know about the models.
db.RegisterModel((*User)(nil), (*Org)(nil))

fixture := dbfixture.New(db)
err := fixture.Load(ctx, os.DirFS("testdata"), "fixture.yml")
```

Example 4 (go):
```go
fixture := dbfixture.New(db, dbfixture.WithRecreateTables())
fixture := dbfixture.New(db, dbfixture.WithTruncateTables())
```

---

## # Database SQL transactions

**URL:** https://bun.uptrace.dev/guide/transactions.html

**Contents:**
- # Database SQL transactions
- # Starting transactions
- # Running queries in a transaction
- # RunInTx
- # IDB interface
- # PostgreSQL advisory locks

bun.Tx is a thin wrapper around sql.Tx. In addition to the features provided by sql.Tx, bun.Tx also supports query hooks and provides helpers to build queries.

To start a transaction:

To commit/rollback the transaction:

Just like with bun.DB, you can use bun.Tx to run queries:

Bun provides RunInTx helpers that runs the provided function in a transaction. If the function returns an error, the transaction is rolled back. Otherwise, the transaction is committed.

Bun provides bun.IDB interface so the same methods can work with *bun.DB, bun.Tx, and bun.Conn. The following exampleopen in new window demonstrates how InsertUser uses the bun.IDB to support transactions:

You can acquire a PostgreSQL advisory lock using the following code:

**Examples:**

Example 1 (go):
```go
type Tx struct {
	*sql.Tx
	db *DB
}
```

Example 2 (go):
```go
tx, err := db.BeginTx(ctx, &sql.TxOptions{})
```

Example 3 (go):
```go
err := tx.Commit()

err := tx.Rollback()
```

Example 4 (go):
```go
res, err := tx.NewInsert().Model(&models).Exec(ctx)

res, err := tx.NewUpdate().Model(&models).Column("col1", "col2").Exec(ctx)

err := tx.NewSelect().Model(&models).Limit(100).Scan(ctx)
```

---

## Golang Merge PostgreSQL MySQL

**URL:** https://bun.uptrace.dev/guide/query-merge.html

**Contents:**
- Golang Merge PostgreSQL MySQL
- # API
- # Example

To see the full list of supported methods, see MergeQueryopen in new window.

To create a MERGE query for MSSQL RDMBS:

**Examples:**

Example 1 (go):
```go
db.NewMerge().
	Model(&strct).
	Model(&slice).

	Table("table1", "table2"). // quotes table names
	TableExpr("table1 AS t1"). // arbitrary unsafe expression
	TableExpr("(?) AS alias", subquery).
	ModelTableExpr("table1 AS t1"). // overrides model table name

    On(expr string, args ...any).
    When(expr string, args ...any).
    WhenInsert(expr string, func(q *bun.InsertQuery) *bun.InsertQuery).
    WhenUpdate(expr string, func(q *bun.UpdateQuery) *bun.UpdateQuery).
    WhenDelete(expr string).
```

Example 2 (go):
```go
type Model struct {
	ID    int64 `bun:",pk,autoincrement"`
	Name  string
	Value string
}

newModels := []*Model{
	{Name: "A", Value: "world"},
	{Name: "B", Value: "test"},
}

return db.NewMerge().
	Model(new(Model)).
	With("_data", db.NewValues(&newModels)).
	Using("_data").
	On("?TableAlias.name = _data.name").
	WhenUpdate("MATCHED", func(q *bun.UpdateQuery) *bun.UpdateQuery {
		return q.Set("value = _data.value")
	}).
	WhenInsert("NOT MATCHED", func(q *bun.InsertQuery) *bun.InsertQuery {
		return q.Value("name", "_data.name").Value("value", "_data.value")
	}).
	Returning("$action")
```

---

## Golang Truncate Table PostgreSQL MySQL

**URL:** https://bun.uptrace.dev/guide/query-truncate-table.html

**Contents:**
- Golang Truncate Table PostgreSQL MySQL
- # API
- # Example

To see the full list of supported methods, see TruncateTableQueryopen in new window.

**Examples:**

Example 1 (go):
```go
db.NewTruncateTable().

	Model(&strct).

	Table("table1"). // quotes table names
	TableExpr("table1"). // arbitrary unsafe expression
	ModelTableExpr("table1"). // overrides model table name

	ContinueIdentity().
	Cascade().
	Restrict().

	Exec(ctx)
```

Example 2 (go):
```go
_, err := db.NewTruncateTable().Model((*Book)(nil)).Exec(ctx)
if err != nil {
	panic(err)
}
```

---

## Drivers and dialects

**URL:** https://bun.uptrace.dev/guide/drivers.html

**Contents:**
- Drivers and dialects
- # Bun: Supported Drivers and Dialects
- # PostgreSQL
- # MySQL
  - # Connection String Options
  - # MySQL-Specific Features
- # SQL Server (MSSQL)
  - # Alternative Connection Formats
  - # SQL Server Features
- # SQLite

Bun is a lightweight Go ORM that works with multiple database systems through a unified interface. To connect to any database, you need two key components:

This two-layer architecture allows Bun to provide a consistent API while supporting the unique features and syntax of different database systems.

PostgreSQL is Bun's primary supported database with full feature compatibility.

See the dedicated PostgreSQL section for comprehensive setup instructions, advanced configuration options, and PostgreSQL-specific features.

Bun supports MySQL 5.0+ and MariaDB using the popular go-sql-driver/mysqlopen in new window driver.

Common MySQL connection parameters:

Example with additional options:

Bun supports Microsoft SQL Server v2019.CU4 and later, starting from Bun v1.1.x.

SQL Server supports multiple connection string formats:

SQLite is perfect for development, testing, and lightweight applications. Bun uses a smart shim driver that automatically selects the best SQLite implementation for your platform.

When using SQLite in-memory databases, you must configure the connection pool to prevent the database from being destroyed when connections close:

The sqliteshim automatically chooses between:

Oracle Database support allows integration with enterprise Oracle systems.

Note: Oracle support requires CGO and the Oracle Client libraries to be installed on your system.

Bun provides elegant ways to handle differences between database systems while keeping your code maintainable.

Use feature detection to write portable code that adapts to database capabilities:

For more complex database-specific logic, check the dialect directly:

Proper connection pool configuration is crucial for production applications:

"driver: bad connection" errors:

SQLite "database is locked" errors:

MySQL charset/encoding issues:

SQL Server connection timeout:

Use build tags and interfaces to test against multiple databases:

When switching between databases, consider:

Q: Can I use multiple databases in the same application? A: Yes! Create separate *bun.DB instances for each database:

Q: How do I handle database-specific SQL functions? A: Use the dialect checking or wrap functions in helper methods:

Q: Which database should I choose for my project?

**Examples:**

Example 1 (go):
```go
import (
    "database/sql"

    "github.com/uptrace/bun"
    "github.com/uptrace/bun/dialect/mysqldialect"
    _ "github.com/go-sql-driver/mysql"
)

func connectMySQL() *bun.DB {
    // Basic connection
    sqldb, err := sql.Open("mysql", "root:password@tcp(localhost:3306)/mydb?parseTime=true")
    if err != nil {
        panic(err)
    }

    return bun.NewDB(sqldb, mysqldialect.New())
}
```

Example 2 (go):
```go
dsn := "user:pass@tcp(localhost:3306)/dbname?parseTime=true&charset=utf8mb4&timeout=30s"
sqldb, err := sql.Open("mysql", dsn)
```

Example 3 (go):
```go
import (
    "database/sql"

    "github.com/uptrace/bun"
    "github.com/uptrace/bun/dialect/mssqldialect"
    _ "github.com/denisenkom/go-mssqldb"
)

func connectSQLServer() *bun.DB {
    // Using connection string format
    dsn := "sqlserver://sa:MyPassword123@localhost:1433?database=mydb&connection+timeout=30"
    sqldb, err := sql.Open("sqlserver", dsn)
    if err != nil {
        panic(err)
    }

    return bun.NewDB(sqldb, mssqldialect.New())
}
```

Example 4 (go):
```go
// URL format (recommended)
"sqlserver://user:pass@localhost:1433?database=mydb"

// ADO.NET format
"server=localhost;user id=sa;password=MyPass;database=mydb"

// ODBC format
"driver=sql server;server=localhost;database=mydb;uid=sa;pwd=MyPass"
```

---

## SQL Placeholders

**URL:** https://bun.uptrace.dev/guide/placeholders.html

**Contents:**
- SQL Placeholders
- # Introduction
- # Basic and positional placeholders
- # bun.Ident
- # bun.Safe
- # IN
- # Model placeholders
- # Global placeholders

Bun recognizes ? in queries as placeholders and replaces them with provided args. Bun quotes and escapes stringly values and removes null bytes.

To use basic placeholders:

To use positional placeholders:

To quote SQL identifiers, for example, a column or a table name, use bun.Ident:

To disable quotation altogether, use bun.Safe:

Provides a bun.In helper to generate IN (...) queries:

For composite (multiple) keys you can use nested slices:

Bun also supports the following model placeholders:

See placeholdersopen in new window example for details.

Bun also supports global placeholders:

**Examples:**

Example 1 (go):
```go
// SELECT 'foo', 'bar'
db.ColumnExpr("?, ?", 'foo', 'bar')
```

Example 2 (go):
```go
// SELECT 'foo', 'bar', 'foo'
db.ColumnExpr("?0, ?1, ?0", 'foo', 'bar')
```

Example 3 (go):
```go
q.ColumnExpr("? = ?", bun.Ident("foo"), "bar")
```

Example 4 (sql):
```sql
"foo" = 'bar' -- PostgreSQL
`foo` = 'bar' -- MySQL
```

---

## Golang Create Table PostgreSQL MySQL

**URL:** https://bun.uptrace.dev/guide/query-create-table.html

**Contents:**
- Golang Create Table PostgreSQL MySQL
- # API
- # Example
- # ResetModel
- # Hooks

To see the full list of supported methods, see CreateTableQueryopen in new window.

Bun provides ResetModel method to quickly drop and create tables:

You can also modify query from the bun.BeforeCreateTableHook hook.

To create an index on the table, you can use bun.AfterCreateTableHook hook:

See exampleopen in new window for details.

**Examples:**

Example 1 (go):
```go
db.NewCreateTable().

	Model(&strct).

	Table("table1"). // quotes table names
	TableExpr("table1"). // arbitrary unsafe expression
	ModelTableExpr("table1"). // overrides model table name

	Temp().
	IfNotExists().
	Varchar(100). // turns VARCHAR into VARCHAR(100)

	WithForeignKeys().
	ForeignKey(`(fkey) REFERENCES table1 (pkey) ON DELETE CASCADE`).
	PartitionBy("HASH (id)").
	TableSpace("fasttablespace").

	Exec(ctx)
```

Example 2 (go):
```go
_, err := db.NewCreateTable().
	Model((*Book)(nil)).
	ForeignKey(`("author_id") REFERENCES "users" ("id") ON DELETE CASCADE`).
	Exec(ctx)
if err != nil {
	panic(err)
}
```

Example 3 (go):
```go
err := db.ResetModel(ctx, (*Model1)(nil), (*Model2)(nil))
```

Example 4 (sql):
```sql
DROP TABLE IF EXISTS model1 CASCADE;
CREATE TABLE model1 (...);

DROP TABLE IF EXISTS model2 CASCADE;
CREATE TABLE model2 (...);
```

---

## Golang Common Table Expressions PostgreSQL MySQL

**URL:** https://bun.uptrace.dev/guide/query-common-table-expressions.html

**Contents:**
- Golang Common Table Expressions PostgreSQL MySQL
- # WITH
- # VALUES
- # WithOrder

Most Bun queries support CTEs via With method:

For example, you can use CTEs to bulk-delete rows that match some predicates:

Or copy data between tables:

Bun also provides ValuesQueryopen in new window to help building CTEs:

You can also use WithOrderopen in new window to include row rank in values:

**Examples:**

Example 1 (go):
```go
q1 := db.NewSelect()
q2 := db.NewSelect()

q := db.NewInsert().
    With("q1", q1).
    With("q2", q2).
    Table("q1", "q2")
```

Example 2 (go):
```go
const limit = 1000

for {
	subq := db.NewSelect().
		Model((*Comment)(nil)).
		Where("created_at < now() - interval '90 day'").
		Limit(limit)

	res, err := db.NewDelete().
		With("todo", subq).
		Model((*Comment)(nil)).
		Table("todo").
		Where("comment.id = todo.id").
		Exec(ctx)
	if err != nil {
		panic(err)
	}

	num, err := res.RowsAffected()
	if err != nil {
		panic(err)
	}
	if num < limit {
		break
	}
}
```

Example 3 (sql):
```sql
WITH todo AS (
    SELECT * FROM comments
    WHERE created_at < now() - interval '90 day'
    LIMIT 1000
)
DELETE FROM comments AS comment USING todo
WHERE comment.id = todo.id
```

Example 4 (go):
```go
src := db.NewSelect().Model((*Comment)(nil))

res, err := db.NewInsert().
    With("src", src).
    Table("comments_backup", "src").
    Exec(ctx)
```

---

## Golang Select PostgreSQL MySQL

**URL:** https://bun.uptrace.dev/guide/query-select.html

**Contents:**
- Golang Select PostgreSQL MySQL
- # API
- # Example
- # Count rows
- # EXISTS
- # Joins
- # Subqueries
- # Raw queries

To see the full list of supported methods, see SelectQueryopen in new window.

To select into a struct, define a model and use SelectQueryopen in new window:

Bun provides Countopen in new window helper to generate count(*) queries:

Because selecting and counting rows is a common operation, Bun also provides ScanAndCountopen in new window:

You can also use Existsopen in new window helper to use the corresponding EXISTS SQL operator:

To select a book and manually join the book author:

To generate complex joins, use JoinOn:

You can use Bun queries (including INSERT, UPDATE, and DELETE queries) as a subquery:

Bun also allows you to execute and scan arbitrary raw queries:

**Examples:**

Example 1 (go):
```go
db.NewSelect().
	With("cte_name", subquery).

	Model(&strct).
	Model(&slice).

	Column("col1", "col2"). // quotes column names
	ColumnExpr("col1, col2"). // arbitrary unsafe expression
	ColumnExpr("count(*)").
	ColumnExpr("count(?)", bun.Ident("id")).
	ColumnExpr("(?) AS alias", subquery).
	ExcludeColumn("col1"). // all columns except col1
	ExcludeColumn("*"). // exclude all columns

	Table("table1", "table2"). // quotes table names
	TableExpr("table1 AS t1"). // arbitrary unsafe expression
	TableExpr("(?) AS alias", subquery).
	ModelTableExpr("table1 AS t1"). // overrides model table name

	Join("JOIN table2 AS t2 ON t2.id = t1.id").
	Join("LEFT JOIN table2 AS t2").JoinOn("t2.id = t1.id").

	WherePK(). // where using primary keys
	Where("id = ?", 123).
	Where("name LIKE ?", "my%").
	Where("? = 123", bun.Ident("id")).
	Where("id IN (?)", bun.In([]int64{1, 2, 3})).
	Where("id IN (?)", subquery).
	Where("FALSE").WhereOr("TRUE").
	WhereGroup(" AND ", func(q *bun.SelectQuery) *bun.SelectQuery {
		return q.WhereOr("id = 1").
			WhereOr("id = 2")
	}).

	Group("col1", "col2"). // quotes column names
	GroupExpr("lower(col1)"). // arbitrary unsafe expression

	Order("col1 ASC", "col2 DESC"). // quotes column names
	OrderExpr("col1 ASC NULLS FIRST"). // arbitrary unsafe expression

    Having("column_name > ?", 123).

	Limit(100).
	Offset(100).

	For("UPDATE").
	For("SHARE").

	Scan(ctx)
```

Example 2 (go):
```go
book := new(Book)
err := db.NewSelect().Model(book).Where("id = ?", 123).Scan(ctx)
```

Example 3 (go):
```go
count, err := db.NewSelect().Model((*User)(nil)).Count(ctx)
```

Example 4 (go):
```go
var users []User
count, err := db.NewSelect().Model(&users).Limit(20).ScanAndCount(ctx)
if err != nil {
	panic(err)
}
fmt.Println(users, count)
```

---

## # Running Bun in production

**URL:** https://bun.uptrace.dev/guide/running-bun-in-production.html

**Contents:**
- # Running Bun in production
- # database/sql
- # bun.WithDiscardUnknownColumns
- # PostgreSQL

Bun uses sql.DB to communicate with database management systems. You should create one sql.DB and one bun.DB when your app starts and close them when your app exits.

The sql package creates and frees connections automatically; it also maintains a pool of idle connections. To maximize pool performance, you can configure sql.DB to not close idle connections:

To make your app more resilient to errors during migrations, you can tweak Bun to discard unknown columns in production:

See PostgreSQL section.

**Examples:**

Example 1 (go):
```go
maxOpenConns := 4 * runtime.GOMAXPROCS(0)
sqldb.SetMaxOpenConns(maxOpenConns)
sqldb.SetMaxIdleConns(maxOpenConns)
```

Example 2 (go):
```go
db := bun.NewDB(sqldb, pgdialect.New(), bun.WithDiscardUnknownColumns())
```

---

## # Extending Bun with custom types

**URL:** https://bun.uptrace.dev/guide/custom-types.html

**Contents:**
- # Extending Bun with custom types
- # sql.Scanner
- # driver.Valuer
- # Conclusion

Bun uses database/sql to work with different DBMS and so you can extend it with custom types using sql.Scanner and driver.Valuer interfaces.

In this tutorial we will write a simple type to work with time that does not have a date:

sql.Scanneropen in new window assigns a value from a database driver. The value can be one of the following types:

You can find the full example at GitHubopen in new window.

driver.Valueropen in new window returns a value for a database driver. The value must be one of the following types:

You can find the full example at GitHubopen in new window.

You can easily extend Bun with custom types to fully utilize your DBMS capabilities, for example, bunbigopen in new window adds support for big.Int to Bun.

**Examples:**

Example 1 (go):
```go
const timeFormat = "15:04:05.999999999"

type Time struct {
	time.Time
}
```

Example 2 (go):
```go
var _ sql.Scanner = (*Time)(nil)

// Scan scans the time parsing it if necessary using timeFormat.
func (tm *Time) Scan(src interface{}) (err error) {
	switch src := src.(type) {
	case time.Time:
		*tm = NewTime(src)
		return nil
	case string:
		tm.Time, err = time.ParseInLocation(timeFormat, src, time.UTC)
		return err
	case []byte:
		tm.Time, err = time.ParseInLocation(timeFormat, string(src), time.UTC)
		return err
	case nil:
		tm.Time = time.Time{}
		return nil
	default:
		return fmt.Errorf("unsupported data type: %T", src)
	}
}
```

Example 3 (go):
```go
var _ driver.Valuer = (*Time)(nil)

// Value formats the value using timeFormat.
func (tm Time) Value() (driver.Value, error) {
	return tm.UTC().Format(timeFormat), nil
}
```

---

## Golang Update PostgreSQL MySQL

**URL:** https://bun.uptrace.dev/guide/query-update.html

**Contents:**
- Golang Update PostgreSQL MySQL
- # API
- # Example
- # Bulk-update
- # Maps
- # Omit zero values
- # FQN

To see the full list of supported methods, see API referenceopen in new window.

To update a row, define a model and use UpdateQueryopen in new window:

To update a single column:

To bulk-update books, you can use a CTE:

Alternatively, you can use Bulk helper which creates a CTE for you:

To update using a map[string]interface{}:

You can also tell Bun to omit zero struct fields, for example, the following query does not update email column because it contains an empty value:

Multi-table updates differ in PostgreSQL and MySQL:

Bun helps you write queries for both databases by providing SetColumn method:

If you have a slice of models to update, use Bulk method:

**Examples:**

Example 1 (go):
```go
db.NewUpdate().
	With("cte_name", subquery).

	Model(&strct).
	Model(&slice).
	Model(&map). // only map[string]interface{}

	Column("col1", "col2"). // list of columns to update
	ExcludeColumn("col1"). // all columns except col1
	ExcludeColumn("*"). // exclude all columns

	Table("table1", "table2"). // quotes table names
	TableExpr("table1 AS t1"). // arbitrary unsafe expression
	TableExpr("(?) AS alias", subquery).
	ModelTableExpr("table1 AS t1"). // overrides model table name

	Value("col1", "expr1", arg1, arg2). // overrides column value

    // Generates `SET col1 = 'value1'`
	Set("col1 = ?", "value1").
    SetColumn("col1", "?", "value1").

	OmitZero() // don't update struct fields having zero values

	WherePK(). // where using primary keys
	Where("id = ?", 123).
	Where("name LIKE ?", "my%").
	Where("? = 123", bun.Ident("id")).
	Where("id IN (?)", bun.In([]int64{1, 2, 3})).
	Where("id IN (?)", subquery).
	Where("FALSE").WhereOr("TRUE").
	WhereGroup(" AND ", func(q *bun.SelectQuery) *bun.SelectQuery {
		return q.WhereOr("id = 1").
			WhereOr("id = 2")
	}).

	Returning("*").
	Returning("col1, col2").
	Returning("NULL"). // don't return anything

	Exec(ctx)
```

Example 2 (go):
```go
book := &Book{ID: 123, Title: "hello"}

res, err := db.NewUpdate().Model(book).WherePK().Exec(ctx)
```

Example 3 (go):
```go
book.Title = "hello"

res, err := db.NewUpdate().
	Model(book).
	Column("title").
	Where("id = ?", 123).
	Exec(ctx)
```

Example 4 (sql):
```sql
UPDATE books SET title = 'my title' WHERE id = 123
```

---

## # Cursor Pagination for PostgreSQL/MySQL

**URL:** https://bun.uptrace.dev/guide/cursor-pagination.html

**Contents:**
- # Cursor Pagination for PostgreSQL/MySQL
- # Introduction
- # Understanding the Problem with Offset Pagination
  - # Performance Degradation
  - # Consistency Issues
- # How Cursor Pagination Works
  - # Visual Representation
- # Cursor vs Offset Pagination
  - # When to Use Each Approach
- # Implementation Guide

Learn how to implement high-performance cursor pagination for PostgreSQL and MySQL databases. This guide covers everything from basic concepts to production-ready Go implementations, helping you build scalable applications that handle millions of records efficiently.

Perfect for: Backend developers, database architects, and teams building data-intensive applications with large datasets.

When building applications that display large datasets—such as social media feeds, search results, or transaction logs—pagination becomes crucial for both performance and user experience. Traditional pagination approaches can become problematic at scale, leading to slow queries and inconsistent results.

Cursor pagination solves these issues by using a pointer (cursor) to track position within the dataset, rather than calculating offsets. This approach is used by major platforms like GitHub, Twitter, and Facebook for their APIs.

Traditional pagination uses LIMIT and OFFSET clauses:

As the offset grows, performance degrades significantly:

The database must read and discard all rows before the offset, making deep pagination extremely expensive.

Consider this scenario:

Offset pagination cannot handle data mutations gracefully.

Cursor pagination uses a unique identifier (cursor) to mark the position in the dataset:

Use Offset Pagination when:

Use Cursor Pagination when:

First, define your data model:

For complex sorting, you may need composite cursors:

For API responses, encode cursors to prevent tampering:

Combine cursors with filters:

Problem: Using non-unique columns as cursors can cause inconsistent results.

Solution: Always include a unique tie-breaker:

Ensure proper indexes exist for cursor columns:

Handle null values in cursor columns:

Always validate cursors from clients:

To monitor cursor pagination performance, use OpenTelemetry instrumentation:

For comprehensive monitoring, consider using Uptraceopen in new window, an OpenTelemetry APMopen in new window that supports distributed tracing, metrics, and logs.

A: Yes! You can use any unique, sortable value:

A: You need a separate query:

Note: This can be expensive for large tables. Consider:

A: Yes, encode the cursor in the URL:

A: The pagination continues normally. The query WHERE id > deleted_id will start from the next available record. This is one of cursor pagination's advantages—it handles data mutations gracefully.

A: Store the current cursor on the client side:

A: Yes, but ensure the cursor column comes from the main table:

For a complete working example, see the Bun cursor pagination exampleopen in new window on GitHub.

**Examples:**

Example 1 (sql):
```sql
-- Page 1: First 10 entries
SELECT * FROM entries ORDER BY id ASC LIMIT 10 OFFSET 0;

-- Page 100: Entries 991-1000
SELECT * FROM entries ORDER BY id ASC LIMIT 10 OFFSET 990;

-- Page 10,000: Entries 99,991-100,000
SELECT * FROM entries ORDER BY id ASC LIMIT 10 OFFSET 99990;
```

Example 2 (sql):
```sql
-- First page: Start from the beginning
SELECT * FROM entries ORDER BY id ASC LIMIT 10;

-- Next page: Continue after the last ID from the previous page
SELECT * FROM entries WHERE id > 10 ORDER BY id ASC LIMIT 10;

-- Another page: Continue after ID 20
SELECT * FROM entries WHERE id > 20 ORDER BY id ASC LIMIT 10;
```

Example 3 (yaml):
```yaml
Dataset: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, ...]

Page 1: [1, 2, 3, 4, 5] → cursor_end = 5
Page 2: [6, 7, 8, 9, 10] → cursor_end = 10 (WHERE id > 5)
Page 3: [11, 12, 13, 14, 15] → cursor_end = 15 (WHERE id > 10)
```

Example 4 (go):
```go
type Entry struct {
    ID        int64     `json:"id" bun:",pk"`
    Title     string    `json:"title"`
    Content   string    `json:"content"`
    CreatedAt time.Time `json:"created_at"`
}
```

---

## # Soft deletes in PostgreSQL and MySQL

**URL:** https://bun.uptrace.dev/guide/soft-deletes.html

**Contents:**
- # Soft deletes in PostgreSQL and MySQL
- # Introduction
- # Using table views
- # Using Bun models
- # Unique indexes

Soft delete is a technique used in databases to mark records as deleted without physically removing them from the database. Instead of permanently deleting data, a flag or a separate column is used to indicate that a record is "deleted" or no longer active. This approach allows for the possibility of later recovering or restoring the deleted data if needed.

Soft deletes allow marking rows as deleted without actually deleting them from a database. You can achieve that by using an auxiliary flag column and modifying queries to check the flag value.

For example, to soft delete a row using deleted_at timestamptz column as a flag:

To select undeleted (live) rows:

By implementing soft delete, you retain the deleted data in the database, allowing for potential future retrieval or analysis. It also maintains data integrity by preserving relationships and references to the deleted records. However, it's important to note that soft delete does consume storage space, so consider periodically purging or archiving the deleted data if it's no longer needed.

You can also implement soft deletes using table views. Given the following table schema:

You can create a view that omits deleted users:

PostgreSQL views support inserts and deletes without any gotchas so you can use them in models:

To query deleted rows, use ModelTableExpr to change the table:

Bun supports soft deletes using time.Time column as a flag that reports whether the row is deleted or not. Bun automatically adjust queries to check the flag.

To enable soft deletes on a model, add DeletedAt field with soft_delete tag:

For such models Bun updates rows instead of deleting them:

Bun also automatically excludes soft-deleted rows from SELECT queries results:

To select soft-deleted rows:

To select all rows including soft-deleted rows:

Finally, to actually delete rows from a database, whether previously soft deleted or not:

Using soft deletes with unique indexes can cause conflicts on insert queries because soft-deleted rows are included in unique indexes just like normal rows.

With some DBMS, you can exclude soft-deleted rows from an index:

Alternatively, you can include deleted_at column to indexed columns using coalesce function to convert NULL time because NULL is not equal to any other value including itself:

If your DBMS does not allow to use expressions in indexed columns, you can configure Bun to append zero time as 1970-01-01 00:00:00+00:00 by removing nullzero option:

**Examples:**

Example 1 (sql):
```sql
UPDATE users SET deleted_at = now() WHERE id = 1
```

Example 2 (sql):
```sql
SELECT * FROM users WHERE deleted_at IS NULL
```

Example 3 (sql):
```sql
CREATE TABLE all_users (
  id int8 PRIMARY KEY GENERATED BY DEFAULT AS IDENTITY,
  name varchar(500),

  created_at timestamptz NOT NULL DEFAULT now(),
  deleted_at timestamptz
);
```

Example 4 (sql):
```sql
CREATE VIEW users AS
SELECT * FROM all_users
WHERE deleted_at IS NULL
```

---

## Golang Insert PostgreSQL MySQL

**URL:** https://bun.uptrace.dev/guide/query-insert.html

**Contents:**
- Golang Insert PostgreSQL MySQL
- # API
- # Example
- # Bulk-insert
- # Upsert
- # Maps
- # INSERT ... SELECT

To see the full list of supported methods, see InsertQueryopen in new window.

To insert data, define a model and use InsertQueryopen in new window:

To bulk-insert models, use a slice:

To insert a new book or update the existing one:

To ignore duplicates, use Ignore with all databases:

To insert a map[string]interface{}:

To copy rows between tables:

You can also specify columns to copy:

**Examples:**

Example 1 (go):
```go
db.NewInsert().
    With("cte_name", subquery).

    Model(&strct).
    Model(&slice).
    Model(&map). // only map[string]interface{}

    Column("col1", "col2"). // list of columns to insert
    ExcludeColumn("col1"). // all columns except col1
    ExcludeColumn("*"). // exclude all columns

    Table("table1", "table2"). // quotes table names
    TableExpr("table1 AS t1"). // arbitrary unsafe expression
    TableExpr("(?) AS subq", subquery).
    ModelTableExpr("table1 AS t1"). // overrides model table name

    Value("col1", "expr1", arg1, arg2). // overrides column value

    On("CONFLICT (id) DO UPDATE").
	Set("col1 = EXCLUDED.col1").

    WherePK(). // where using primary keys
    Where("id = ?", 123).
    Where("name LIKE ?", "my%").
    Where("? = 123", bun.Ident("id")).
    Where("id IN (?)", bun.In([]int64{1, 2, 3})).
    Where("id IN (?)", subquery).
    Where("FALSE").WhereOr("TRUE").
    WhereGroup(" AND ", func(q *bun.SelectQuery) *bun.SelectQuery {
        return q.WhereOr("id = 1").
            WhereOr("id = 2")
    }).

    Returning("*").
    Returning("col1, col2").
    Returning("NULL"). // don't return anything

    Exec(ctx)
```

Example 2 (go):
```go
book := &Book{Title: "hello"}

res, err := db.NewInsert().Model(book).Exec(ctx)
```

Example 3 (go):
```go
books := []Book{book1, book2}
res, err := db.NewInsert().Model(&books).Exec(ctx)
if err != nil {
    panic(err)
}

for _, book := range books {
    fmt.Println(book.ID) // book id is scanned automatically
}
```

Example 4 (go):
```go
_, err := db.NewInsert().
	Model(&book).
	On("CONFLICT (id) DO UPDATE").
	Set("title = EXCLUDED.title").
	Exec(ctx)
```

---

## # What is Bun?

**URL:** https://bun.uptrace.dev/guide/

**Contents:**
- # What is Bun?
- # Key Features
- # Quick Start
- # How Bun Works
  - # Architecture Overview
  - # Database Dialects
- # Query Building Examples
  - # Basic CRUD Operations
  - # Advanced Query Examples
- # Why Choose Bun?

Bun is a SQL-first database client for Go that bridges the gap between raw SQL and Go's type system. The "SQL-first" philosophy means that Bun prioritizes SQL familiarity while providing the safety and convenience of Go's type system.

Here's a simple example to get you started:

Bun is built on top of Go's standard sql.DB, extending it with additional functionality while maintaining full compatibility:

This design means you can:

Bun uses dialects to handle database-specific features and SQL syntax differences:

Example with different databases:

Joins and Relationships

Aggregations and Grouping

Here's the original complex query example with additional context:

This generates clean, readable SQL:

Bun excels at powering REST APIs where you need efficient database operations with type safety.

The query builder makes it easy to construct complex analytical queries with CTEs, window functions, and aggregations.

Lightweight nature makes it perfect for microservices where you want database access without heavy ORM overhead.

SQL-first approach makes it easy to work with existing databases and complex schemas.

Q: Can I use raw SQL with Bun? A: Yes! You can always fall back to raw SQL when needed:

Q: How does Bun handle database connections? A: Bun wraps the standard sql.DB, so it uses Go's built-in connection pooling. You can configure pool settings on the underlying sql.DB.

Q: Can I use Bun with an existing database? A: Absolutely! Bun works great with existing databases. You just need to define Go structs that match your table schemas.

Q: Is Bun suitable for high-traffic applications? A: Yes, Bun is designed for performance and has minimal overhead compared to heavier ORMs.

**Examples:**

Example 1 (go):
```go
package main

import (
    "context"
    "database/sql"
    "fmt"

    "github.com/uptrace/bun"
    "github.com/uptrace/bun/dialect/pgdialect"
    "github.com/uptrace/bun/driver/pgdriver"
)

type User struct {
    ID    int64  `bun:"id,pk,autoincrement"`
    Name  string `bun:"name,notnull"`
    Email string `bun:"email,unique"`
}

func main() {
    // Connect to database
    sqldb := sql.OpenDB(pgdriver.NewConnector(pgdriver.WithDSN("postgres://user:pass@localhost/dbname")))
    db := bun.NewDB(sqldb, pgdialect.New())
    defer db.Close()

    ctx := context.Background()

    // Create a user
    user := &User{Name: "John Doe", Email: "john@example.com"}
    _, err := db.NewInsert().Model(user).Exec(ctx)
    if err != nil {
        panic(err)
    }

    // Query users
    var users []User
    err = db.NewSelect().Model(&users).Where("name LIKE ?", "%John%").Scan(ctx)
    if err != nil {
        panic(err)
    }

    fmt.Printf("Found %d users\n", len(users))
}
```

Example 2 (go):
```go
type DB struct {
    *sql.DB  // Embedded standard database connection
    dialect  schema.Dialect
    hooks    []QueryHook
    // ... other fields
}
```

Example 3 (go):
```go
// PostgreSQL
sqldb := sql.OpenDB(pgdriver.NewConnector(pgdriver.WithDSN("postgres://...")))
db := bun.NewDB(sqldb, pgdialect.New())

// MySQL
sqldb := sql.Open("mysql", "user:password@tcp(localhost:3306)/dbname")
db := bun.NewDB(sqldb, mysqldialect.New())

// SQLite
sqldb := sql.Open("sqlite3", ":memory:")
db := bun.NewDB(sqldb, sqlitedialect.New())
```

Example 4 (go):
```go
user := &User{Name: "Alice", Email: "alice@example.com"}

// Single insert
_, err := db.NewInsert().Model(user).Exec(ctx)

// Bulk insert
users := []*User{
    {Name: "Bob", Email: "bob@example.com"},
    {Name: "Carol", Email: "carol@example.com"},
}
_, err := db.NewInsert().Model(&users).Exec(ctx)
```

---

## # Bun Starter Kit

**URL:** https://bun.uptrace.dev/guide/starter-kit.html

**Contents:**
- # Bun Starter Kit
- # App structure
- # Starting the app
- # Migrations

Bun starter kitopen in new window consists of:

You can also check bun-realworld-appopen in new window which is a JSON API built with Bun starter kit.

The starter kit has the following structure:

The main entrypoints are:

You should keep HTTP handlers and DB models in the same package, but split the app into logically isolated packages. Each package should have init.go file with the module initialization logic.

The kit provides convenience methods to start/stop the app:

It also provides hooks to execute custom code on the app start/stop. You usually add hooks from the init function in your module's init.go file.

The kit also provides a CLI to manage migrations:

**Examples:**

Example 1 (bash):
```bash
├─ bunapp
│  └─ app.go
│  └─ config.go
│  └─ router.go
│  └─ start.go
│  └─ hook.go
│  └─ embed
│     └─ config
│        └─ dev.yaml
│        └─ test.yaml
├─ cmd
│  └─ bun
│     └─ main.go
│     └─ migrations
│        └─ main.go
│        └─ 20210505110026_init.go
├─ example
│  └─ init.go
│  └─ example_handler.go
│  └─ example_handler_test.go
├─ .gitignore
└─ go.mod
```

Example 2 (go):
```go
func main() {
	ctx, app, err := bunapp.Start(ctx, "service_name", "environment_name")
	if err != nil {
		panic(err)
	}
	defer app.Stop()
}
```

Example 3 (go):
```go
func init() {
	bunapp.OnStart("hook.name", func(ctx context.Context, app *bunapp.App) error {
		app.Router().GET("/endpoint", handler)

		app.OnStop("hook.name", func(ctx context.Context, app *bunapp.App) error {
			log.Println("stopping...")
		})

		return nil
	})
}
```

Example 4 (bash):
```bash
go run cmd/bun/main.go

NAME:
   bun db - manage database migrations

USAGE:
   bun db [global options] command [command options] [arguments...]

COMMANDS:
   init        create migration tables
   migrate     migrate database
   rollback    rollback the last migration group
   unlock      unlock migrations
   create_go   create a Go migration
   create_sql  create a SQL migration
   help, h     Shows a list of commands or help for one command

GLOBAL OPTIONS:
   --help, -h  show help (default: false)
```

---

## Writing Queries

**URL:** https://bun.uptrace.dev/guide/queries.html

**Contents:**
- Writing Queries
- # Design
- # Scan and Exec
- # bun.IDB
- # Scanning rows
- # Scanonly
- # Ignoring unknown columns
- # See also

Bun's goal is to help you write idiomatic SQL, not to hide it behind awkward constructs. It is a good idea to start writing and testing queries using CLI for your database (for example, psql), and then re-construct resulting queries using Bun's query builder.

The main features are:

For example, the following Go code:

Unsurprisingly generates the following query:

You can create queries using bun.DBopen in new window, bun.Txopen in new window, or bun.Connopen in new window:

Once you have a query, you can execute it with Exec:

Or use Scan which does the same but omits the sql.Result (only available for selects):

By default Exec scans columns into the model, but you can specify a different destination too:

Bun provides bun.IDB interface which you can use to accept bun.DB, bun.Tx, and bun.Conn:

To execute custom query and scan all rows:

Sometimes, you want to ignore some fields when inserting or updating data, but still be able to scan columns into the ignored fields. You can achieve that with scanonly option:

To discard unknown SQL columns, you can use WithDiscardUnknownColumns db option:

If you want to ignore a single column, just underscore it:

**Examples:**

Example 1 (go):
```go
err := db.NewSelect().
	Model(book).
	ColumnExpr("lower(name)").
	Where("? = ?", bun.Ident("id"), "some-id").
	Scan(ctx)
```

Example 2 (sql):
```sql
SELECT lower(name)
FROM "books"
WHERE "id" = 'some-id'
```

Example 3 (go):
```go
result, err := db.NewInsert().Model(&user).Exec(ctx)
```

Example 4 (go):
```go
err := db.NewSelect().Model(&user).Where("id = 1").Scan(ctx)
```

---

## # Logging queries

**URL:** https://bun.uptrace.dev/guide/debugging.html

**Contents:**
- # Logging queries
- # bundebug
- # Logrus hook
- # Zap hook

For quick debugging, you can print executed queries to stdout. First, you need to install bundebug package:

Then add the provided query hook which by default only prints failed queries:

To print all queries, use WithVerbose option:

You can also disable the hook by default and use environment variables to enable it when needed:

You can also use logrusbunopen in new window to log executed queries using Logrusopen in new window

Use QueryHookOptions to adjust log levels and behavior:

You can also use bunzapopen in new window to log executed queries using Zapopen in new window

**Examples:**

Example 1 (bash):
```bash
go get github.com/uptrace/bun/extra/bundebug
```

Example 2 (go):
```go
import "github.com/uptrace/bun/extra/bundebug"

db := bun.NewDB(sqldb, dialect)
db.AddQueryHook(bundebug.NewQueryHook())
```

Example 3 (go):
```go
bundebug.NewQueryHook(bundebug.WithVerbose(true))
```

Example 4 (go):
```go
bundebug.NewQueryHook(
    // disable the hook
    bundebug.WithEnabled(false),

    // BUNDEBUG=1 logs failed queries
    // BUNDEBUG=2 logs all queries
    bundebug.FromEnv("BUNDEBUG"),
)
```

---

## Defining models

**URL:** https://bun.uptrace.dev/guide/models.html

**Contents:**
- Defining models
- # Quick Start
- # Mapping Tables to Structs
  - # Basic Model Structure
  - # Why Use bun.BaseModel?
- # Complete Struct Tags Reference
  - # Table-Level Tags
  - # Field-Level Tags
  - # Primary Keys and Identity
  - # Data Types and Validation

Models in Bun are Go structs that represent database tables. They serve as the bridge between your Go application and the database, defining how data is structured, validated, and manipulated. This guide covers everything you need to know about creating and working with Bun models.

The simplest model maps a Go struct to a database table:

This creates a users table with three columns: id (primary key), name (required), and email (unique).

For each database table, you define a corresponding Go struct (model). Bun automatically maps exported struct fields to table columns while ignoring unexported fields.

The bun.BaseModel field provides:

Bun uses sensible defaults but allows fine-grained control through struct tags. Here's the complete reference:

Bun automatically converts struct names to table names and field names to column names using these rules:

Override defaults when needed:

Use ModelTableExpr for runtime table selection while maintaining consistent aliases:

Use Cases for ModelTableExpr:

Convert Go zero values to SQL NULL:

Create variations of existing models:

Create flattened table structures:

Generated table structure:

Use snake_case for all database identifiers:

When you must use SQL keywords, quote them:

Cause: Mismatch between struct field names and database columns.

Cause: Missing nullzero tag or incorrect NULL handling.

Cause: Database-specific autoincrement syntax.

Q: When should I use pointers vs sql.Null* types? A: Use pointers for simplicity and when you control the data flow. Use sql.Null* when you need to distinguish between zero values and NULL, or when working with existing APIs that use these types.

Q: Can I have multiple primary keys? A: Yes, Bun supports composite primary keys:

Q: How do I handle database migrations with model changes? A: Use Bun's migration system. When you change model fields, create corresponding migration files to alter the database schema.

Q: What's the difference between nullzero and using pointers? A: nullzero converts Go zero values to SQL NULL at query time. Pointers represent NULL as nil and allow distinguishing between zero values and NULL.

Q: Can I use the same struct for different tables? A: Yes, use ModelTableExpr() to specify different tables at runtime while keeping the same struct definition.

Q: How do I debug struct tag issues? A: Enable Bun's debug mode to see generated SQL queries:

**Examples:**

Example 1 (go):
```go
type User struct {
    bun.BaseModel `bun:"table:users,alias:u"`

    ID   int64  `bun:"id,pk,autoincrement"`
    Name string `bun:"name,notnull"`
    Email string `bun:"email,unique"`
}
```

Example 2 (go):
```go
type User struct {
    bun.BaseModel `bun:"table:users,alias:u"`

    // Exported fields become database columns
    ID       int64     `bun:"id,pk,autoincrement"`
    Name     string    `bun:"name,notnull"`
    Email    string    `bun:"email,unique"`
    IsActive bool      `bun:"is_active,default:true"`

    // Unexported fields are ignored by Bun
    password string
    cache    map[string]interface{}
}
```

Example 3 (go):
```go
// Single primary key
type User struct {
    ID int64 `bun:"id,pk,autoincrement"`
}

// Composite primary key
type UserRole struct {
    UserID int64 `bun:"user_id,pk"`
    RoleID int64 `bun:"role_id,pk"`
}
```

Example 4 (go):
```go
type Product struct {
    bun.BaseModel `bun:"table:products,alias:p"`

    ID          int64           `bun:"id,pk,autoincrement"`
    SKU         string          `bun:"sku,unique,notnull"`
    Name        string          `bun:"name,notnull"`
    Description *string         `bun:"description"` // nullable
    Price       decimal.Decimal `bun:"type:decimal(10,2),notnull"`
    Stock       int             `bun:"stock,default:0"`
    Tags        []string        `bun:"tags,array"` // PostgreSQL array
    Metadata    map[string]any  `bun:"metadata,type:jsonb"`

    CreatedAt time.Time `bun:"created_at,nullzero,notnull,default:current_timestamp"`
    UpdatedAt time.Time `bun:"updated_at,nullzero,notnull,default:current_timestamp"`
    DeletedAt bun.NullTime `bun:"deleted_at,soft_delete"`
}
```

---

## Bun Performance Monitoring

**URL:** https://bun.uptrace.dev/guide/performance-monitoring.html

**Contents:**
- Bun Performance Monitoring
- # What is OpenTelemetry?
- # OpenTelemetry Instrumentation
- # Uptrace
- # Prometheus
- # Conclusion

Bun uses OpenTelemetry to monitor database performance and errors through OpenTelemetry tracingopen in new window and OpenTelemetry metricsopen in new window.

OpenTelemetry is designed to be language- and framework-agnostic, supporting multiple programming languages and frameworks. It provides language-specific software development kits (SDKs) that simplify the integration of telemetry collection into applications written in different languages.

OpenTelemetry also provides exporters and integrations to send telemetry data to various OpenTelemetry backendopen in new window systems and observability platforms, including popular tools like Prometheus, Grafana, Jaeger, Zipkin, and Elasticsearch.

By using OpenTelemetry, developers can adopt a standardized approach to observability, making it easier to collect and analyze telemetry data across different components of a distributed system. This helps improve troubleshooting, performance optimization, and application monitoring by providing valuable insights into application behavior and performance.

Bun includes OpenTelemetry instrumentation called bunotelopen in new window, which is distributed as a separate module:

To instrument a Bun database, you need to add the hook provided by bunotel:

To enable tracing, you must use an active span contextopen in new window when executing queries:

Uptrace is an open-source APMopen in new window for OpenTelemetry that supports distributed tracing, metrics, and logs. You can use it to monitor applications and troubleshoot issues.

Uptrace includes an intuitive query builder, rich dashboards, alerting rules, notifications, and integrations for most languages and frameworks.

Uptrace can process billions of spans and metrics on a single server, allowing you to monitor your applications at 10x lower cost.

You can try Uptrace in just a few minutes by visiting the cloud demoopen in new window (no login required) or running it locally with Dockeropen in new window. The source code is available on GitHubopen in new window.

OpenTelemetry integrates with Prometheus, a popular monitoring and alerting system, to collect and export telemetry data.

By integrating OpenTelemetry with Prometheus, you can leverage Prometheus's powerful monitoring and alerting capabilities while benefiting from the flexibility and standardization provided by OpenTelemetry. This integration enables you to collect, store, visualize, and analyze metrics from your applications and systems, gaining valuable insights into their performance and behavior.

You can send OpenTelemetry metrics to Prometheus using the OpenTelemetry Prometheus exporteropen in new window.

Monitoring SQL performance is crucial for optimizing query execution, improving application responsiveness, ensuring scalability, troubleshooting issues, and maintaining database security and compliance. It enables you to proactively manage and optimize your SQL infrastructure, leading to better application performance, efficient resource utilization, and enhanced user satisfaction.

**Examples:**

Example 1 (bash):
```bash
go get github.com/uptrace/bun/extra/bunotel
```

Example 2 (go):
```go
import "github.com/uptrace/bun/extra/bunotel"

db := bun.NewDB(sqldb, dialect)
db.AddQueryHook(bunotel.NewQueryHook(bunotel.WithDBName("mydb")))
```

Example 3 (go):
```go
ctx := req.Context()
err := db.NewSelect().Scan(ctx)
```

---

## Golang Where PostgreSQL MySQL

**URL:** https://bun.uptrace.dev/guide/query-where.html

**Contents:**
- Golang Where PostgreSQL MySQL
- # Basics
- # QueryBuilder
- # WHERE IN
- # WherePK
- # WHERE VALUES
- # Grouping

You can use arbitrary unsafe expressions in Where:

To safely build dynamic WHERE clauses, use placeholders and bun.Ident:

Bun provides QueryBuilderopen in new window interface which supports common methods required to build queries, for example:

Both the QueryBuilder and ApplyQueryBuilder functions return a struct of QueryBuilder interface type. Once your query is built you need to retrieve the original Query struct in order to be able to call Scan or Exec functions. To do that you have to Unwrap() your query builder struct and then cast it to desired type like so:

If you already have a list of ids, use bun.In:

You can also use subqueries:

WherePK allows to auto-generate a WHERE clause using model primary keys:

WherePK also accepts a list of columns that can be used instead of primary keys to indentify rows:

You can build complex queries using CTE and VALUES:

You can use WhereOr to join conditions with logical OR:

To group conditions with parentheses, use WhereGroup:

**Examples:**

Example 1 (go):
```go
q = q.Where("column LIKE 'hello%'")
```

Example 2 (go):
```go
q = q.Where("? LIKE ?", bun.Ident("mycolumn"), "hello%")
```

Example 3 (go):
```go
func addWhere(q bun.QueryBuilder) bun.QueryBuilder {
    return q.Where("id = ?", 123)
}

qb := db.NewSelect().QueryBuilder()
addWhere(qb)

qb := db.NewUpdate().QueryBuilder()
addWhere(qb)

qb := db.NewDelete().QueryBuilder()
addWhere(qb)

// Alternatively.

db.NewSelect().ApplyQueryBuilder(addWhere)
db.NewUpdate().ApplyQueryBuilder(addWhere)
db.NewDelete().ApplyQueryBuilder(addWhere)
```

Example 4 (go):
```go
qb := db.NewSelect().QueryBuilder().Where("id = ?", 123)

selectQuery = qb.Unwrap().(*bun.SelectQuery)
```

---

## Golang Drop Table PostgreSQL MySQL

**URL:** https://bun.uptrace.dev/guide/query-drop-table.html

**Contents:**
- Golang Drop Table PostgreSQL MySQL
- # API
- # Example

To see the full list of supported methods, see DropTableQueryopen in new window.

To drop PostgreSQL/MySQL table:

**Examples:**

Example 1 (go):
```go
db.NewDropTable().

	Model(&strct).

	Table("table1"). // quotes table names
	TableExpr("table1"). // arbitrary unsafe expression
	ModelTableExpr("table1"). // overrides model table name

	IfExists().

	Cascade().
	Restrict().

	Exec(ctx)
```

Example 2 (go):
```go
_, err := db.NewDropTable().Model((*Book)(nil)).IfExists().Exec(ctx)
if err != nil {
	panic(err)
}
```

---

## # Writing complex parameterized queries

**URL:** https://bun.uptrace.dev/guide/complex-queries.html

**Contents:**
- # Writing complex parameterized queries
- # Divide and conquer
- # Parsing request params
- # Params validation
- # Query generation
- # Query execution

A parameterized query is a query that is built dynamically based on incoming request params. Building complex database queries can be challenging but you can achieve better results by following the recommendations presented in this article.

The first and the main recommendation is to split the whole process into isolated steps:

The first think you need to do is to create a data structure that will hold incoming params, for example:

And a factory method that will parse the params from an http.Request or JSON payload:

The purpose of this step is to ensure you have enough data to build a query or to set default values:

At this step you have enough data to build a query using Bun API. It is best to keep all query generation logic in a single method so it can be easily followed.

Lastly, you need to execute the generated query and, optionally, do some post-processing. The end result may look like this:

**Examples:**

Example 1 (go):
```go
type ArticleFilter struct {
	CategoryID int64
	Search	   string
	Page	   int
}
```

Example 2 (go):
```go
func articleFilterFromRequest(req *http.Request) (*ArticleFilter, error) {
	query := req.URL.Query()

	f := new(ArticleFilter)
	f.Search = query.Get("search")

	categoryID, err := strconv.ParseInt(query.Get("category_id"), 10, 64)
	if err != nil {
		return nil, err
	}
	f.CategoryID = categoryID

	page, err := strconv.Atoi(query.Get("page"))
	if err != nil {
		return nil, err
	}
	f.Page = page

	return f, nil
}
```

Example 3 (go):
```go
func (f *ArticleFilter) Validate() error {
	if f.CategoryID == 0 {
		return errors.New("category id is required")
	}
	if f.Page == 0 {
		f.Page = 1
	} else f.Page > 1000 {
		return errors.New("you can't paginate past page #1000")
	}
	return nil
}
```

Example 4 (go):
```go
func articleFilterQuery(q *bun.SelectQuery, f *ArticleFilter) (*bun.SelectQuery, error) {
	q = q.Where("category_id = ?", f.CategoryID).
		Limit(10).
		Offset(10 * (f.Page - 1))
	if f.Search != "" {
		q = q.Where("title LIKE ?", "%"+f.Search+"%")
	}
	return q, nil
}
```

---

## # Migrating from go-pg

**URL:** https://bun.uptrace.dev/guide/pg-migration.html

**Contents:**
- # Migrating from go-pg
- # New features
- # Go zero values and NULL
- # Other changes
- # Ignored columns
- # pg.Listener
- # Porting migrations
- # Monitoring performance

Bun is a rewrite of go-pgopen in new window that works with PostgreSQL, MySQL, and SQLite. It consists of:

Bun's query builder tries to be compatible with go-pg's builder, but some rarely used APIs are removed (for example, WhereOrNotGroup). In most cases, you won't need to rewrite your queries.

go-pg is still maintained and there is no urgency in rewriting go-pg apps in Bun, but new projects should prefer Bun over go-pg. And once you are familiar with the updated API, you should be able to migrate a 80-100k lines go-pg app to Bun within a single day.

*pg.Query is split into smaller structs, for example, bun.SelectQueryopen in new window, bun.InsertQueryopen in new window, bun.UpdateQueryopen in new window, bun.DeleteQueryopen in new window and so on. This is one of the reasons Bun inserts/updates data faster than go-pg.

To create VALUES (1, 'one') statement, use db.NewValues(&rows).

Bulk UPDATE queries should be rewrited using CTE and VALUES statement:

Alternatively, you can use UpdateQuery.Bulk helper that does the same:

To create an index, use db.NewCreateIndex().

To drop an index, use db.NewDropIndex().

To truncate a table, use db.NewTruncateTable().

To overwrite model table name, use q.Model((*MyModel)(nil)).ModelTableExpr("my_table_name").

To provide initial data, use fixtures.

Unlike go-pg, Bun does not marshal Go zero values as SQL NULLs by default. To get the old behavior, use nullzero tag option:

For time.Time fields you can use bun.NullTime:

Unlike go-pg, Bun does not allow scanning into explicitly ignored fields. For example, the following code does not work:

But you can fix it by adding scanonly option:

You have 2 options if you need pg.Listener:

Bun supports migrations via bun/migrate package. Because it uses timestamp-based migration names, you need to rename your migration files, for example, 1_initial.up.sql should be renamed to 20210505110026_initial.up.sql.

After you are done porting migrations, you need to initialize Bun tables (use starter kit):

And probably mark existing migrations as completed:

You can check the status of migrations with:

To monitor Bun performance, you can use OpenTelemetry instrumentation that comes with Bun.

OpenTelemetry is an open source project that aims to provide a unified set of APIs, libraries, agents, and instrumentation to enable observability in modern software applications. It allows developers to collect, instrument, and export telemetry data from their applications to gain insight into the performance and behavior of distributed systems.

Uptrace is a OpenTelemetry APMopen in new window that supports distributed tracing, metrics, and logs. You can use it to monitor applications and troubleshoot issues.

Uptrace comes with an intuitive query builder, rich dashboards, alerting rules with notifications, and integrations for most languages and frameworks.

Uptrace can process billions of spans and metrics on a single server and allows you to monitor your applications at 10x lower cost.

In just a few minutes, you can try Uptrace by visiting the cloud demoopen in new window (no login required) or running it locally with Dockeropen in new window. The source code is available on GitHubopen in new window.

**Examples:**

Example 1 (go):
```go
err := db.ModelContext(ctx, &users).Select()
err := db.ModelContext(ctx, &users).Select(&var1, &var2)
res, err := db.ModelContext(ctx, &users).Insert()
res, err := db.ModelContext(ctx, &user).WherePK().Update()
res, err := db.ModelContext(ctx, &users).WherePK().Delete()
```

Example 2 (go):
```go
err := db.NewSelect().Model(&users).Scan(ctx)
err := db.NewSelect().Model(&users).Scan(ctx, &var1, &var2)
res, err := db.NewInsert().Model(&users).Exec(ctx)
res, err := db.NewUpdate().Model(&users).WherePK().Exec(ctx)
res, err := db.NewDelete().Model(&users).WherePK().Exec(ctx)
```

Example 3 (go):
```go
db.NewUpdate().
    With("_data", db.NewValues(&rows)).
    Model((*Model)(nil)).
    Table("_data").
    Set("model.name = _data.name").
    Where("model.id = _data.id").
    Exec(ctx)
```

Example 4 (go):
```go
err := db.NewUpdate().Model(&rows).Bulk().Exec(ctx)
```

---

## Golang Delete Rows PostgreSQL MySQL

**URL:** https://bun.uptrace.dev/guide/query-delete.html

**Contents:**
- Golang Delete Rows PostgreSQL MySQL
- # API
- # Example
- # Bulk-delete
- # DELETE ... USING

To see the full list of supported methods, see DeleteQueryopen in new window.

To delete a row, define a model and use DeleteQueryopen in new window:

To bulk-delete books by a primary key:

To delete rows using another table:

**Examples:**

Example 1 (go):
```go
db.NewDelete().
    With("cte_name", subquery).

    Model(&strct).
    Model(&slice).

    Table("table1", "table2"). // quotes table names
    TableExpr("table1 AS t1"). // arbitrary unsafe expression
    TableExpr("(?) AS alias", subquery).
    ModelTableExpr("table1 AS t1"). // overrides model table name

    WherePK(). // where using primary keys
    Where("id = ?", 123).
    Where("name LIKE ?", "my%").
    Where("? = 123", bun.Ident("id")).
    Where("id IN (?)", bun.In([]int64{1, 2, 3})).
    Where("id IN (?)", subquery).
    Where("FALSE").WhereOr("TRUE").
    WhereGroup(" AND ", func(q *bun.SelectQuery) *bun.SelectQuery {
        return q.WhereOr("id = 1").
            WhereOr("id = 2")
    }).

    Returning("*").
    Returning("col1, col2").
    Returning("NULL"). // don't return anything

    Exec(ctx)
```

Example 2 (go):
```go
res, err := db.NewDelete().Where("id = ?", 123).Exec(ctx)
```

Example 3 (go):
```go
books := []*Book{book1, book2} // slice of books with ids
res, err := db.NewDelete().Model(&books).WherePK().Exec(ctx)
```

Example 4 (sql):
```sql
DELETE FROM "books" WHERE id IN (1, 2)
```

---
