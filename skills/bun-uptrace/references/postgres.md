# Bun-Uptrace - Postgres

**Pages:** 9

---

## # Copy data between tables and files

**URL:** https://bun.uptrace.dev/postgres/copy-data.html

**Contents:**
- # Copy data between tables and files
- # COPY TO
- # COPY FROM

PostgreSQL allows to efficiently copy data between tables and files using COPY TO and COPY FROM commands.

To copy data from a table to an io.Writer:

To copy data from an io.Reader to a table:

**Examples:**

Example 1 (go):
```go
import "github.com/uptrace/bun/driver/pgdriver"

conn, err := db.Conn(ctx)
if err != nil {
	panic(err)
}
defer conn.Close()

var buf bytes.Buffer

res, err := pgdriver.CopyTo(ctx, conn, &buf, "COPY table_name TO STDOUT")
if err != nil {
	panic(err)
}

fmt.Println(buf.String())
```

Example 2 (go):
```go
import "github.com/uptrace/bun/driver/pgdriver"

conn, err := db.Conn(ctx)
if err != nil {
	panic(err)
}
defer conn.Close()

file, err := os.Open("data.csv")
if err != nil {
	panic(err)
}

res, err := pgdriver.CopyFrom(ctx, conn, file, "COPY table_name FROM STDIN")
if err != nil {
	panic(err)
}
```

---

## # Working with PostgreSQL arrays

**URL:** https://bun.uptrace.dev/postgres/postgres-arrays.html

**Contents:**
- # Working with PostgreSQL arrays

pgdialect supports PostgreSQL one-dimensional arrays using array struct field tag:

To scan a PostgreSQL array into a variable, use pgdialect.Array:

You can also use pgdialect.Array to insert/update arrays:

**Examples:**

Example 1 (go):
```go
type Article struct {
	ID	 int64
	Tags []string `bun:",array"`
}
```

Example 2 (go):
```go
import "github.com/uptrace/bun/dialect/pgdialect"

var tags []string

err := db.NewSelect().
	Model((*Article)(nil)).
	ColumnExpr("tags").
	Where("id = 1").
	Scan(ctx, pgdialect.Array(&tags))
```

Example 3 (go):
```go
res, err := db.NewUpdate().
    Model(&article).
    Set("tags = ?", pgdialect.Array([]string{"foo", "bar"})).
    WherePK().
    Exec(ctx)
```

Example 4 (go):
```go
q.Where("tags @> ?", pgdialect.Array([]string{"foo"}))
```

---

## # PostgreSQL data types

**URL:** https://bun.uptrace.dev/postgres/postgres-data-types.html

**Contents:**
- # PostgreSQL data types
- # timestamptz vs timestamp
- # JSONB
- # Arrays
- # UUID
- # See also

TLDR You should prefer using timestamptz over timestamp. None of the types store the provided timezone, but timestamptz at least properly parses the time with a timezone. To save user timezone, create a separate column for it.

Let's use the following table as an example:

The first difference between timestamptz and timestamp is that timestamp discards/ignores the provided timezone:

timestamp also ignores the server/session timezone:

Bun uses JSONB data type to store maps and slices. To change the default type, use type struct tag option:

To enable json.Decoder.UseNumber option:

You can also use json.RawMessage to work with raw bytes:

See Working with PostgreSQL arrays.

See Generating UUIDs in PostgreSQL.

See Don't do thisopen in new window for more tips.

**Examples:**

Example 1 (sql):
```sql
CREATE TABLE test (
  t1 timestamptz,
  t2 timestamp
);
```

Example 2 (sql):
```sql
INSERT INTO test VALUES ('2021-01-01 02:00:00+02', '2021-01-01 02:00:00+02') RETURNING *;

           t1           |         t2
------------------------+---------------------
 2021-01-01 00:00:00+00 | 2021-01-01 02:00:00
```

Example 3 (sql):
```sql
SET timezone = 'America/Los_Angeles';
```

Example 4 (sql):
```sql
SELECT * FROM test;

           t1           |         t2
------------------------+---------------------
 2020-12-31 16:00:00-08 | 2021-01-01 02:00:00
```

---

## PostgreSQL Table Partitioning

**URL:** https://bun.uptrace.dev/postgres/table-partition.html

**Contents:**
- PostgreSQL Table Partitioning
- # Why partition a table?
- # Partitioning methods
  - # Partition by range
  - # Partition by list
  - # Partition by hash
- # Managing partitions
- # Using partitioned tables with Bun
- # PostgreSQL monitoring

This tutorial explains how to use PostgreSQL Table Partitioningopen in new window with Bun.

Table partitioning allows to split one large table into smaller ones bringing the following benefits:

Let's suppose we have a table:

You can partition that table by providing columns to use as the partition key:

PostgreSQL supports several partitioning methods which only differ in the way they specify row values for the partition key.

Partitioning by range allows to specify a range of values for the partition, for example, we can store data for each month in a separate partition:

List partitioning allows to specify a list of values for the partition, for example, we can store small fraction of the frequently accessed data in the hot partition and move the rest to the cold partition:

You can then move rows between partitions by updating the hot column:

Partitioning by hash allows to uniformly distribute rows into a set of tables, for example, we can create 3 partitions for our table and pick a partition for the row using a hash and a remainder of division:

Thanks to using hashes, the partitions will receive approximately the same amount of rows.

PostgreSQL allows to detach and attach partitions:

You can use those commands to partition an existing table without moving any data:

Bun allows to create partitioned tables:

And query partitions directly using ModelTableExpr:

You can even create separate models for partitions:

To monitor PostgreSQLopen in new window, you can use OpenTelemetry PostgreSQLopen in new window receiver that comes with OpenTelemetry Collector.

OpenTelemetry Collectoropen in new window is commonly used for monitoring and observability purposes in modern software applications and distributed systems. It plays a crucial role in gathering telemetry data from various sources, processing that data, and exporting it to monitoring and observability backends for analysis and visualization.

Uptrace is a Grafana alternativeopen in new window that supports distributed tracing, metrics, and logs. You can use it to monitor applications and troubleshoot issues.

Uptrace comes with an intuitive query builder, rich dashboards, alerting rules with notifications, and integrations for most languages and frameworks.

Uptrace can process billions of spans and metrics on a single server and allows you to monitor your applications at 10x lower cost.

In just a few minutes, you can try Uptrace by visiting the cloud demoopen in new window (no login required) or running it locally with Dockeropen in new window. The source code is available on GitHubopen in new window.

**Examples:**

Example 1 (sql):
```sql
CREATE TABLE measurements (
  id int8 NOT NULL,
  value float8 NOT NULL,
  date timestamptz NOT NULL
);
```

Example 2 (sql):
```sql
CREATE TABLE measurements (
  id int8 NOT NULL,
  value float8 NOT NULL,
  date timestamptz NOT NULL
) PARTITION BY RANGE (date);
```

Example 3 (sql):
```sql
CREATE TABLE measurements_y2021m01 PARTITION OF measurements
FOR VALUES FROM ('2021-01-01') TO ('2021-02-01');
```

Example 4 (sql):
```sql
CREATE TABLE measurements (
  id int8 PRIMARY KEY,
  value float8 NOT NULL,
  date timestamptz NOT NULL,
  hot boolean
) PARTITION BY LIST (hot);

CREATE TABLE measurements_hot PARTITION OF measurements
FOR VALUES IN (TRUE);

CREATE TABLE measurements_cold PARTITION OF measurements
FOR VALUES IN (NULL);
```

---

## Faceted search using PostgreSQL full text search

**URL:** https://bun.uptrace.dev/postgres/faceted-full-text-search-tsvector.html

**Contents:**
- Faceted search using PostgreSQL full text search
- # Creating a table
- # Creating facets from tags
- # Constructing a facet
- # Retrieving document stats
- # Conclusion
- # See also

Faceted search or faceted navigation allows users to narrow down search results by applying multiple filters generated from some attributes or tags. In this article we will implement faceted search using PostgreSQL full text searchopen in new window and ts_stat function.

GitHub search is a good example of faceted navigation (see the image on the right).

Let's start by creating books table with a name, tags (attributes), and a text search vector:

tsvectoropen in new window is a sorted list of distinct normalized words (lexemes) that are used for searching. You can create a tsvector using to_tsvector function:

You can use to_tsvector when inserting rows to the table:

Once you have some data, you can search over books using a tsvector and a tsquery:

That query can be slow if your dataset is large, but you can make it faster by adding an inverted index on tsv column:

And check that PostgreSQL uses the index:

We will be using the following dataset to test our queries:

You can insert those books using the following query:

And then filter books by tags:

Let's start by defining a facet we are expecting to get in the end:

We could easily achieve that result with the following query:

But it is rather slow and inefficient because we need to select all tags to build the facet. Can we do better? Yes, using ts_stat function to get the required data directly from the tsv column.

The function ts_stat allows to retrieve document statistics that are maitained by PostgreSQL full text search engine in tsvector columns.

As you can see, PostgreSQL already maintains the stats we need to build the facet only using the tsv column:

To build a refined facet, you can use a fast filter over the same tsv column that is covered by the index we created earlier:

PostgreSQL provides everything you need to build fast faceted search for datasets up to 1 million rows. With larger datasets the processing time becomes an issue and you may need to shard your database.

You can also check pg-faceted-searchopen in new window example that demonstrates how to implement faceted search using Go and Bun database client.

**Examples:**

Example 1 (sql):
```sql
CREATE TABLE books (
  id bigint PRIMARY KEY GENERATED BY DEFAULT AS IDENTITY,
  name varchar(1000),
  tags jsonb,
  tsv tsvector
);
```

Example 2 (sql):
```sql
SELECT to_tsvector('english', 'The Fat Rats');

   to_tsvector
-----------------
 'fat':2 'rat':3
```

Example 3 (sql):
```sql
INSERT INTO books (name, tsv)
VALUES
  ('hello word', to_tsvector('english', 'hello world')),
  ('foo bar', to_tsvector('english', 'foo bar'))
RETURNING *;

 id |    name    | attrs |         tsv
----+------------+-------+---------------------
  1 | hello word |       | 'hello':1 'world':2
  2 | foo bar    |       | 'bar':2 'foo':1
```

Example 4 (sql):
```sql
SELECT * FROM books
WHERE tsv @@ websearch_to_tsquery('english', 'hello');

 id |    name    | tags |         tsv
----+------------+------+---------------------
  1 | hello word |      | 'hello':1 'world':2
```

---

## 

**URL:** https://bun.uptrace.dev/postgres/tuning-zfs-aws-ebs.html

**Contents:**
- # Overview
- # Basic ZFS setup
- # ZFS config
- # ZFS ARC size
- # ZFS recordsize
- # ARC and shared_buffers
- # TOAST compression
- # Alignment Shift
- # PostgreSQL full page writes
- # PostgreSQL block size and WAL size

This guide explains how to run PostgreSQL using ZFS filesystem. If you also need to install ZFS, see Installing ZFS on Ubuntuopen in new window.

The main reason to use PostgreSQL with ZFS (instead of ext4/xfs) is data compression. Using LZ4, you can achieve 2-3x compression ratio which means that you need to write and read 2-3x less data. ZSTD offers even better compression at the expense of slightly higher CPU usage.

The second reason is Adaptive Replacement Cache (ARC). ARC is a page replacement algorithm with slightly better characteristics than Linux page cache. Since it caches compressed blocks, you can also fit more data in the same RAM.

First, you need to create a separate pool for PostgreSQL:

And 2 datasets for PostgreSQL data and a write-ahead log (WAL):

Consider starting with the following ZFS configuration and tune it as you learn more:

By default, ZFS uses 50% of RAM for Adaptive Replacement Cache (ARC). You can consider increasing ARC to 70-80% of RAM, but make sure to leave enough memory for PostgreSQL shared_buffers:

To persist the ARC size change through Linux restarts, create /etc/modprobe.d/zfs.conf:

recordsize is the size of the largest block of data that ZFS will write and read. ZFS compresses each block individually and compression is better for larger blocks. Use the default recordsize=128k and decrease it to 32-64k if you need more TPS (transactions per second).

Setting recordsize=8k to match PostgreSQL block size reduces compression efficiency which is one of the main reasons to use ZFS in the first place. While recordsize=8k improves the average transaction rate as reported by pgbench, good pgbench result is not an indicator of good production performance. Measure performance of your queries before lowering recordsize.

Since ARC caches compressed blocks, prefer using it over PostgreSQL shared_buffers for caching hot data. But making shared_buffers too small will negatively affect write speed. So consider lowering shared_buffers as long as your write speed does not suffer too much and leave the rest of the RAM for ARC.

To not compress data twice, you can disable PostgreSQL TOASTopen in new window compression by setting column storage to EXTERNAL. But it does not make much difference:

Use the default ashift value with Amazon Elastic Block Store and other cloud storages because EBS volume is not a single physical device but a logical volume that spans numerous distributed devices.

But if you know the sector size of the drive, it is worth it to configure ashift properly:

Because ZFS always writes full blocks, you can disable full page writes in PostgreSQL via full_page_writes = off setting.

The default PostgreSQL block size is 8k and it does not match ZFS record size (by default 128k). The result is that while PostgreSQL writes data in 8k blocks, ZFS has to work with 128k records (known as write amplification). You can improve this situation by increasing PostgreSQL block size to 32k and WAL block size to 64k. This requires re-compiling PostgreSQL and re-initializing a database.

Quote from @mercenary_sysadminopen in new window:

logbias=throughput with no SLOG will likely improve performance if your workload is lots of big block writes, which is a workload that usually isn't suffering from performance issues much in the first place.

Logbias=throughput with no SLOG and small block writes will result in the most horrific fragmentation imaginable, which will penalize you both in the initial writes AND when you reread that data from metal later.

Another one from @taratarabobara open in new window:

logbias=throughput will fragment every. Single. Block. Written to your pool.

Normally ZFS writes data and metadata near sequentially, so they can be read with a single read IOP later. Indirect syncs (logbias=throughput) cause metadata and data to be spaced apart, and data spaced apart from data. Fragmentation results, along with very pool IO merge.

If you want to see this in action, do "zfs send dataset >/dev/null" while watching "zpool iostat -r 1" in another window. You will see many, many 4K reads that cannot be aggregated with anything else. This is the cost of indirect sync, and you pay it at every single read.

It should only be used in very specific circumstances.

If you are going to use ZFS snapshots, create a separate dataset for PostgreSQL WAL files. This way snapshots of your main dataset are smaller. Don't forget to backup WAL files separately so you can use Point-in-Time Recoveryopen in new window.

But usually it is easier and cheaper to store backups on S3 using pgbackrest. Another popular option is EBS snapshots.

**Examples:**

Example 1 (bash):
```bash
zpool create -o autoexpand=on pg /dev/nvme1n1
```

Example 2 (bash):
```bash
# Move PostgreSQL files to a temp location.
mv /var/lib/postgresql/14/main/pg_wal /tmp/pg_wal
mv /var/lib/postgresql /tmp/postgresql

# Create datasets.
zfs create pg/data -o mountpoint=/var/lib/postgresql
zfs create pg/wal-14 -o mountpoint=/var/lib/postgresql/14/main/pg_wal

# Move PostgreSQL files back.
cp -r /tmp/postgresql/* /var/lib/postgresql
cp -r /tmp/pg_wal/* /var/lib/postgresql/14/main/pg_wal

# Fix permissions.
chmod 0750 /var/lib/postgresql
chmod 0750 /var/lib/postgresql/14/main/pg_wal
```

Example 3 (bash):
```bash
# same as default
zfs set recordsize=128k pg

# enable lz4 compression
zfs set compression=lz4 pg
# or zstd compression
#zfs set compression=zstd-3 pg

# disable access time updates
zfs set atime=off pg

# enable improved extended attributes
zfs set xattr=sa pg

# same as default
zfs set logbias=latency pg

# reduce amount of metadata (may improve random writes)
zfs set redundant_metadata=most pg
```

Example 4 (bash):
```bash
# set ARC cache to 1GB
echo 1073741824 >> /sys/module/zfs/parameters/zfs_arc_max
```

---

## # PostgreSQL: Generating UUID primary keys

**URL:** https://bun.uptrace.dev/postgres/postgres-uuid-generate.html

**Contents:**
- # PostgreSQL: Generating UUID primary keys
- # What is UUID?
- # When to use UUIDs?
- # UUID in PostgreSQL
- # UUID in Go
- # Generating UUIDs
- # Using UUIDs in models
- # Monitoring performance

A universally unique identifier (UUID) is a 128-bit number that is generated in a way that makes it very unlikely that the same identifier will be generated by anyone else in the known universe (globally unique).

In PostgreSQL, you can generate UUIDs using the uuid_generate_v4 function from the uuid-ossp extension.

UUID stands for Universally Unique Identifier. It is a 128-bit identifier used to uniquely identify information in computer systems and applications. UUIDs are often represented as a string of 36 characters, typically in a format such as "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx", where each "x" represents a hexadecimal digit.

The purpose of UUIDs is to provide a way to generate identifiers that are highly unlikely to collide with other identifiers, even if they are created on different systems or at different times. This makes UUIDs particularly useful in scenarios where there is a need to uniquely identify objects, entities, or resources in distributed systems, databases, or other applications.

You can use UUIDs when you need to generate a globally unique indentifier without using an id generation service, for example, OpenTelemetryopen in new window uses 16-bytes identifiers as a trace id.

Usually, UUIDs are generated by taking 16 random bytes and the uniqueness is based on the sheer quantity, not the generation algorithm. Such identifiers are proven to be unique, but are larger and slightly slower than 64-bit sequential numbers.

UUIDs are slightly slower than 64-bit sequential identifiers. Use them only when you don't have an easy way to generate smaller sequential identifiers.

PostgreSQL requires an extension to support UUID column type. The extenstion comes with postgresql-contrib-* package:

Then you need to install the extension in each database where you are going to use it:

For working with UUIDs in Go you need to install google/uuidopen in new window package.

satori/go.uuidopen in new window works too, but it does not look maintained any more.

You can use uuid.UUID type in Bun models like this:

UUID field name also works well:

To monitor PostgreSQLopen in new window, you can use OpenTelemetry PostgreSQLopen in new window receiver that comes with OpenTelemetry Collector.

OpenTelemetry Collectoropen in new window is a valuable component for monitoring applications and infrastructure in distributed environments. It enables efficient data collection, processing, and export to improve observability, troubleshooting, and performance of software systems.

Uptrace is an open source APMopen in new window for OpenTelemetry that supports distributed tracing, metrics, and logs. You can use it to monitor applications and troubleshoot issues.

Uptrace comes with an intuitive query builder, rich dashboards, alerting rules, notifications, and integrations for most languages and frameworks.

Uptrace can process billions of spans and metrics on a single server and allows you to monitor your applications at 10x lower cost.

In just a few minutes, you can try Uptrace by visiting the cloud demoopen in new window (no login required) or running it locally with Dockeropen in new window. The source code is available on GitHubopen in new window.

**Examples:**

Example 1 (bash):
```bash
sudo apt install postgresql-contrib-14
```

Example 2 (sql):
```sql
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
```

Example 3 (bash):
```bash
go get github.com/google/uuid
```

Example 4 (sql):
```sql
SELECT uuid_generate_v4();
```

---

## pgBackRest: PostgreSQL S3 backups

**URL:** https://bun.uptrace.dev/postgres/pgbackrest-s3-backups.html

**Contents:**
- pgBackRest: PostgreSQL S3 backups
- # Introduction
- # Installation
- # Terms
- # Configuration
- # Full backup
- # Differential backup
- # Incremental backup
- # Backup restore
- # PostgreSQL monitoring

This tutorial explains how to backup PostgreSQL database using pgBackRestopen in new window and S3.

pgBackRest is a modern PostgreSQL Backup & Restore solution that has all the features you may ever need:

Ubuntu provides pre-compiled packages for pgbackrest:

Stanza is a pgBackRest configuration for a PostgreSQL database cluster. Most db servers only have one db cluster and therefore one stanza.

Repository is where pgBackRest stores backups and archives WAL segments.

Let's create a basic directory structure for configs and logs:

And save the following config in /etc/pgbackrest/pgbackrest.conf:

For point-in-time recoveryopen in new window, you also need to configure PostgreSQL to upload WAL files to S3:

Full backup copies all files in a database cluster.

Differential backup only copies files that have changed since the last full backup. It is smaller than a full backup, but to restore it you will need the base full backup.

Incremental backup only copies files that have changed since the last backup (full, differential, or incremental). It is smaller than a full or differential backup, but to restore it you will need all dependant backups.

To restore the cluster from the last backup:

To view all available backups:

To monitor PostgreSQLopen in new window, you can use OpenTelemetry PostgreSQLopen in new window receiver that comes with OpenTelemetry Collector.

OpenTelemetry Collectoropen in new window is designed to collect, process, and export telemetry data from multiple sources. It acts as a centralized and flexible data pipeline that simplifies the management of telemetry data in distributed systems.

Uptrace is a OpenTelemetry backendopen in new window that supports distributed tracing, metrics, and logs. You can use it to monitor applications and troubleshoot issues.

Uptrace comes with an intuitive query builder, rich dashboards, alerting rules with notifications, and integrations for most languages and frameworks.

Uptrace can process billions of spans and metrics on a single server and allows you to monitor your applications at 10x lower cost.

In just a few minutes, you can try Uptrace by visiting the cloud demoopen in new window (no login required) or running it locally with Dockeropen in new window. The source code is available on GitHubopen in new window.

pgBackRest is a reliable backup tool that requires miminum configuration. To achieve a good balance between backup size and restoration time, you can create a full backup weekly and a differential/incremental backup daily.

**Examples:**

Example 1 (bash):
```bash
sudo apt install pgbackrest
```

Example 2 (bash):
```bash
mkdir -m 770 /var/log/pgbackrest
chown postgres:postgres /var/log/pgbackrest
mkdir /etc/pgbackrest
```

Example 3 (bash):
```bash
[demo]
pg1-path=/var/lib/postgresql/14/main

[global]
repo1-retention-full=3 # keep last 3 backups
repo1-type=s3
repo1-path=/s3-path
repo1-s3-region=us-east-1
repo1-s3-endpoint=s3.amazonaws.com
repo1-s3-bucket=s3_bucket_name
repo1-s3-key=$AWS_ACCESS_KEY
repo1-s3-key-secret=$AWS_SECRET_KEY

# Force a checkpoint to start backup immediately.
start-fast=y
# Use delta restore.
delta=y

# Enable ZSTD compression.
compress-type=zst
compress-level=6

log-level-console=info
log-level-file=debug
```

Example 4 (bash):
```bash
archive_mode = on
archive_command = 'pgbackrest --stanza=demo archive-push %p'
archive_timeout = 300
```

---

## # PostgreSQL listen and notify

**URL:** https://bun.uptrace.dev/postgres/listen-notify.html

**Contents:**
- # PostgreSQL listen and notify
- # Listen/notify
- # pgdriver.Listener

PostgreSQL supports publish/subscribe messaging pattern using NOTIFYopen in new window and LISTENopen in new window commands, for example, you can subscribe for notifications using LISTEN command:

And then send notifications with optional textual payload:

Together with table triggers, you can send notifications whenever rows are updated/deleted to invalidate a cache or reindex the table:

pgdriver provides Listeneropen in new window which allows to listen for notifications and automatically re-subscribes to channels when the database connection is lost:

You can send notifications using Notifyopen in new window method:

See exampleopen in new window for details.

**Examples:**

Example 1 (sql):
```sql
LISTEN channel_name;
```

Example 2 (sql):
```sql
NOTIFY channel_name, 'optional payload';
```

Example 3 (sql):
```sql
CREATE FUNCTION users_after_update_trigger()
RETURNS TRIGGER AS $$
BEGIN
  PERFORM pg_notify('users:updated', NEW.id::text);
  RETURN NULL;
END;
$$
LANGUAGE plpgsql;

CREATE TRIGGER users_after_update_trigger
AFTER UPDATE ON users
FOR EACH ROW EXECUTE PROCEDURE users_after_update_trigger();
```

Example 4 (go):
```go
ln := pgdriver.NewListener(db)
if err := ln.Listen(ctx, "users:updated"); err != nil {
	panic(err)
}

for notif := range ln.Channel() {
	fmt.Println(notif.Channel, notif.Payload)
}
```

---
