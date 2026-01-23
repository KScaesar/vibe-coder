# Atlas-Schema - Hcl Reference

**Pages:** 1

---

## PostgreSQL Schema

**URL:** https://atlasgo.io/hcl/postgres

**Contents:**
- PostgreSQL Schema
- aggregate​
  - aggregate attributes​
  - aggregate blocks​
    - aggregate.arg​
      - aggregate.arg attributes​
      - aggregate.arg constraints​
  - aggregate constraints​
- cast​
  - cast attributes​

List of object references

Aggregate initial value can be one of:

enum (SAFE, UNSAFE, RESTRICTED)

Object reference to schema

Object reference to function

Aggregate state type can be one of:

Aggregate argument default value can be one of:

Aggregate argument mode can be one of:

Aggregate argument type can be one of:

The cast block describes a type cast in the database.

enum (ASSIGNMENT, IMPLICIT)

Cast source type can be one of:

Cast target type can be one of:

Cast method (INOUT, function reference, or function expression) can be one of:

The collation block describes a collation in the schema.

Collation provider can be one of:

Object reference to schema

The composite block describes a composite type in the schema.

Object reference to schema

Field collation can be one of:

Field type can be one of:

The domain block describes a DOMAIN type in the schema.

Domain default value can be one of:

Object reference to schema

Domain type can be one of:

The enum block describes an ENUM type in the schema.

Object reference to schema

The event_trigger block describes an event trigger in the database.

Object reference to function

Event trigger on can be one of:

The extension block describes an extension in the database.

The depends_on attribute specifies the extensions that this extension depends on.

List of object reference to extension

Object reference to schema

List of object references

Object reference to schema

The reference or a name of an existing foreign server to use for the foreign table can be one of:

Column collation can be one of:

Column type can be one of:

The function block describes a function in a database schema.

List of object references

Function language can be one of:

enum (SAFE, UNSAFE, RESTRICTED)

Function return type can be one of:

Function return_set type can be one of:

Object reference to schema

enum (DEFINER, INVOKER)

enum (VOLATILE, STABLE, IMMUTABLE)

Function argument default value can be one of:

Function argument mode can be one of:

Function argument type can be one of:

The config_params block describes the configuration parameters to be set when the function is entered.

Function return_table column type can be one of:

The materialized block describes a materialized view in a database schema.

List of object references

Object reference to schema

Column type can be one of:

Index columns can be one of:

Index included columns can be one of:

Index key type can be one of:

Index columns can be one of:

Index operator class can be one of:

The partition block describes a partition in the schema.

Parent table can be one of:

Object reference to schema

Column default value can be one of:

Column type can be one of:

Foreign key columns can be one of:

enum (INITIALLY_IMMEDIATE, INITIALLY_DEFERRED)

enum (NO_ACTION, RESTRICT, CASCADE, SET_NULL, SET_DEFAULT)

enum (NO_ACTION, RESTRICT, CASCADE, SET_NULL, SET_DEFAULT)

Foreign key reference columns can be one of:

The index on a partitioned table to which this index is attached.

Object reference to table.index

Index columns can be one of:

Index included columns can be one of:

Index key type can be one of:

Index columns can be one of:

Index operator class can be one of:

Partition columns can be one of:

enum (RANGE, LIST, HASH)

Partition columns can be one of:

The permission block describes permissions (privileges) granted on database objects.

Permission target resource can be one of:

List of strings or/and enums (SELECT, INSERT, UPDATE, DELETE, TRUNCATE, REFERENCES, TRIGGER, CREATE, CONNECT, TEMPORARY, EXECUTE, USAGE, SET, ALTER_SYSTEM, MAINTAIN, ALL)

Permission grantee can be one of:

The policy block describes a row-level security policy for a table.

enum (PERMISSIVE, RESTRICTIVE)

enum (ALL, SELECT, INSERT, UPDATE, DELETE)

Object reference to table

List of strings or/and enums (PUBLIC, CURRENT_ROLE, CURRENT_USER, SESSION_USER)

The procedure block describes a procedure in a database schema.

List of object references

Procedure language can be one of:

Object reference to schema

enum (DEFINER, INVOKER)

Procedure argument default value can be one of:

Procedure argument mode can be one of:

Procedure argument type can be one of:

The config_params block describes the configuration parameters to be set when the procedure is entered.

The range block describes a range type in the schema.

Object reference to schema

Range subtype can be one of:

Range subtype difference function can be one of:

The role block describes a database role.

List of object reference to role

The schema block describes a database schema.

The sequence block describes a sequence in a database schema.

Object reference to table.column

Object reference to schema

The server block describes a foreign server in the database.

The depends_on attribute specifies the extensions that this server depends on.

List of object reference to extension

Foreign data wrapper can be one of:

The table block describes a table in a database schema.

Table access method can be one of:

List of object references

Replica identity for logical replication can be one of:

Object reference to schema

Column collation can be one of:

Column default value can be one of:

Column type can be one of:

enum (ALWAYS, BY_DEFAULT)

enum (INITIALLY_IMMEDIATE, INITIALLY_DEFERRED)

Index included columns can be one of:

Index key type can be one of:

Index columns can be one of:

Exclude element operator can be one of:

Foreign key columns can be one of:

enum (INITIALLY_IMMEDIATE, INITIALLY_DEFERRED)

enum (NO_ACTION, RESTRICT, CASCADE, SET_NULL, SET_DEFAULT)

enum (NO_ACTION, RESTRICT, CASCADE, SET_NULL, SET_DEFAULT)

Foreign key reference columns can be one of:

Index columns can be one of:

Index included columns can be one of:

Index key type can be one of:

Index columns can be one of:

Index operator class can be one of:

Partition columns can be one of:

enum (RANGE, LIST, HASH)

Partition columns can be one of:

Primary key columns can be one of:

enum (INITIALLY_IMMEDIATE, INITIALLY_DEFERRED)

Primary key included columns can be one of:

Index key type can be one of:

Index columns can be one of:

enum (INITIALLY_IMMEDIATE, INITIALLY_DEFERRED)

Index included columns can be one of:

The trigger block describes a trigger on a table in a database schema.

enum (INITIALLY_IMMEDIATE, INITIALLY_DEFERRED)

enum (ROW, STATEMENT)

enum (ROW, STATEMENT)

Object reference to table

Trigger on can be one of:

Trigger update_of columns can be one of:

Trigger update_of columns can be one of:

Object reference to function

Object reference to procedure

Trigger update_of columns can be one of:

The user block describes a database user.

List of object reference to role

The view block describes a view in a database schema.

enum (LOCAL, CASCADED)

List of object references

Object reference to schema

Column type can be one of:

**Examples:**

Example 1 (markdown):
```markdown
# Binary coercion cast (WITHOUT FUNCTION)cast {  source = text  target = composite.my_type}# I/O conversion cast (WITH INOUT)cast {  source = int4  target = composite.my_type  with   = INOUT}# Function-based cast (WITH FUNCTION)cast {  source = int4  target = composite.my_type  with   = function.int4_to_my_type  as     = IMPLICIT}
```

Example 2 (sql):
```sql
collation "french" {  schema   = schema.public  locale   = "fr-x-icu"  provider = icu}collation "german" {  schema = schema.public  from   = "german_phonebook"}
```

Example 3 (unknown):
```unknown
composite "address" {  schema = schema.public  field "street" {    type = text  }  field "city" {    type = text  }}
```

Example 4 (unknown):
```unknown
domain "us_postal_code" {  schema = schema.public  type   = text  null   = true  check "us_postal_code_check" {    expr = "..."  }}
```

---
