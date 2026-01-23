# Bun-Uptrace - Advanced

**Pages:** 1

---

## # Tuning PostgreSQL settings for performance

**URL:** https://bun.uptrace.dev/postgres/performance-tuning.html

**Contents:**
- # Tuning PostgreSQL settings for performance
- # max_connections
- # shared_buffers
- # work_mem
- # maintenance_work_mem
- # effective_cache_size
- # Autovacuum
- # WAL
- # SSD
- # Timeouts

PostgreSQL has many configuration options that can be adjusted to improve performance. Here are some tips for tuning PostgreSQL performance.

Use a reasonably low number of connections so you can give each connection more RAM, disk time, and CPU. To not get FATAL too many connections error, use a connection pool in front of PostgreSQL, for example, PgBounceropen in new window is a good option.

On SSD, set max_connections to the number of concurrent I/O requests the disk(s) can handle * number_of_cpus.

shared_buffers controls how much memory PostgreSQL reserves for writing data to a disk. PostgreSQL picks a free page of RAM in shared buffers, writes the data into it, marks the page as dirty, and lets another process asynchronously write dirty pages to the disk in background.

PostgreSQL also uses shared buffers as a cache if the data you are reading can be found there. For proper explanation, see thisopen in new window.

Lowering shared buffers value too much may hurt write performance.

work_mem specifies the max amount of memory each PostgreSQL query can use before falling back to temporary disk files. Every query may request the value defined by work_mem multiple times so be cautious with large values.

If your queries often use temp files, consider increasing work_mem value and lowering the max number of concurrent queries via max_connections.

The optimal value for work_mem can vary depending on your specific workload, hardware resources, and available memory. Regular monitoring, benchmarking, and tuning are necessary to ensure optimal performance as your workload evolves over time.

maintenance_work_mem limits the max amount of memory that can be used by maintenance operations, for example, CREATE INDEX or ALTER TABLE.

effective_cache_size gives PostgreSQL a hint about how much data it can expect to find in the system cache or ZFS ARC.

Autovacuum is a background process responsible for removing dead tuples (deleted rows) and updating database statistics used by PostgreSQL query planner to optimize queries.

Default autovacuum settings are rather conservative and can be increased to let autovacuum run more often and use more resources:

You can also run less autovacuum workers but give each of them more memory:

PostgreSQL WAL stands for Write-Ahead Logging. The Write-Ahead Log is a transaction log that records changes made to the database before they are written to the actual data files.

When a transaction modifies the data in PostgreSQL, the changes are first written to the WAL before being applied to the actual database files. This process ensures that the changes are durably recorded on disk before considering the transaction committed.

The following WAL settings work well most of the time and the only downside is increased recovery time when your database crashes:

If you are using solid-state drives, consider tweaking the following settings:

You can tell PostgreSQL to cancel slow queries using the following settings:

Good logging can tell you when queries are too slow or there are any other problems:

Huge pages, also known as large pages, are a memory management feature in operating systems that allow applications to allocate and utilize larger page sizes than the standard small pages. In the context of databases like PostgreSQL, huge pages can offer performance benefits by reducing memory overhead and improving memory access efficiency.

If your servers have 128+ GB of RAM, consider using huge pages to reduce the number of memory pages and to minimize the overheadopen in new window introduced by managing large amount of pages.

Indexes can significantly speed up query performance by allowing PostgreSQL to quickly locate the data it needs. Ensure that your tables have appropriate indexes based on the queries being run.

Use the EXPLAIN command to analyze queries and identify areas for optimization.

If your tables are very large, consider partitioning them. Partitioning can improve query performance by allowing PostgreSQL to quickly access the relevant data.

See PostgreSQL Table Partitioning.

When dealing with large data sets, such as in a web application that needs to display a large number of records. consider using cursor pagination.

Regularly monitoring database activity can help identify performance issues. Use tables such as pg_stat_activity, pg_stat_database, and pg_stat_user_tables to monitor database activity and identify areas for optimization.

To monitor PostgreSQLopen in new window, you can use OpenTelemetry PostgreSQLopen in new window receiver that comes with OpenTelemetry Collector.

Uptrace is a OpenTelemetry APMopen in new window that supports distributed tracing, metrics, and logs. You can use it to monitor applications and troubleshoot issues.

Uptrace comes with an intuitive query builder, rich dashboards, alerting rules with notifications, and integrations for most languages and frameworks.

Uptrace can process billions of spans and metrics on a single server and allows you to monitor your applications at 10x lower cost.

In just a few minutes, you can try Uptrace by visiting the cloud demoopen in new window (no login required) or running it locally with Dockeropen in new window. The source code is available on GitHubopen in new window.

**Examples:**

Example 1 (bash):
```bash
max_connections = <4-8 * number_of_cpus>
```

Example 2 (bash):
```bash
shared_buffers = <20-40% of RAM>
```

Example 3 (bash):
```bash
work_mem = <1-5% of RAM>
```

Example 4 (bash):
```bash
maintenance_work_mem = <10-20% of RAM>
```

---
