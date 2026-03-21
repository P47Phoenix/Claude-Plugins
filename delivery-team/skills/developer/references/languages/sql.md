# SQL Best Practices

Version baseline: ANSI SQL with PostgreSQL as the primary dialect reference

## Style & Formatting

- Use UPPERCASE for SQL keywords: `SELECT`, `FROM`, `WHERE`, `JOIN`, `ON`, `GROUP BY`, `ORDER BY`
- Use `snake_case` for table names, column names, index names, and constraint names
- Table names: plural nouns (`users`, `orders`, `line_items`)
- Prefix index names with `idx_`: `idx_users_email`; prefix foreign keys with `fk_`; constraints with `ck_` or `uq_`
- Align clauses vertically in multi-line queries for readability
- Terminate all statements with `;`

## Idioms & Patterns

- Always name columns explicitly — never `SELECT *` in production queries
- Use CTEs (`WITH` clauses) instead of deeply nested subqueries — they are readable and optimizable
- Use window functions (`ROW_NUMBER()`, `RANK()`, `LAG()`, `LEAD()`) over self-joins for analytical queries
- Prefer `EXISTS` over `IN` for correlated subquery checks — better performance with large sets
- Use `COALESCE(x, default)` to handle NULLs explicitly; do not rely on implicit NULL behavior
- Use `NULLIF(a, b)` to convert a specific value to NULL (e.g., prevent divide-by-zero: `x / NULLIF(y, 0)`)
- Use `RETURNING` (PostgreSQL) to retrieve affected rows from `INSERT`/`UPDATE`/`DELETE` without a second query
- Use `UPSERT` (`INSERT ... ON CONFLICT DO UPDATE`) instead of check-then-insert patterns
- Use `GENERATE_SERIES()` (PostgreSQL) or recursive CTEs to generate sequences without application-side loops

## Error Handling

- Wrap related statements in transactions (`BEGIN` / `COMMIT` / `ROLLBACK`) — never leave partial writes
- Use `SAVEPOINT` for nested rollback logic within a transaction
- Use application-layer parameterized queries — the database itself does not handle parameter injection
- Use `CHECK` constraints, `NOT NULL`, `UNIQUE`, and `FOREIGN KEY` constraints to enforce integrity at the DB layer — do not rely solely on application code
- Test constraint violations explicitly in integration tests

## Testing (Database)

- Use a real database in tests — not mocks (mocks do not catch SQL syntax errors, type mismatches, or constraint violations)
- Use `Testcontainers` (or similar) to spin up isolated DB instances per test run
- Apply migrations in test setup using the same migration tool as production (`Flyway`, `Liquibase`, `Alembic`)
- Seed test data explicitly in each test; avoid shared mutable state between tests
- Test edge cases: NULL inputs, empty results, constraint violations, concurrent writes

## Security

- **Always use parameterized queries or prepared statements** — never concatenate user input into SQL strings
- Never execute dynamic SQL built from user input; if unavoidable, whitelist all dynamic identifiers
- Grant minimal database privileges: application user should not have `DROP`, `TRUNCATE`, or DDL permissions in production
- Use row-level security (RLS) in PostgreSQL to enforce data access control at the database layer
- Encrypt sensitive columns (`pgcrypto` in PostgreSQL) for PII and credentials
- Audit sensitive queries using database-level logging or audit extensions

## Performance

- **Always check `EXPLAIN ANALYZE`** before deploying slow queries to production
- Index columns used in `WHERE`, `JOIN ON`, `ORDER BY`, and `GROUP BY` — but do not over-index (write performance)
- Use partial indexes for common filtered queries: `CREATE INDEX ON orders (user_id) WHERE status = 'pending'`
- Use covering indexes to avoid heap fetches: include needed columns in the index
- Avoid `SELECT DISTINCT` — it usually signals a join or data model problem
- Avoid functions on indexed columns in `WHERE` clauses: `WHERE LOWER(email) = ...` prevents index use; use a functional index instead
- Use `LIMIT` with `OFFSET` carefully for pagination — `OFFSET` scans rows; use keyset pagination for large datasets
- Use connection pooling (`PgBouncer`, HikariCP) — never open a new connection per query

## Anti-Patterns to Avoid

- **`SELECT *`:** always name columns; `*` breaks when schema changes
- **Implicit column ordering:** always specify `ORDER BY` when order matters
- **NULLs in comparisons:** `WHERE col = NULL` always returns false; use `IS NULL` / `IS NOT NULL`
- **Unconstrained deletes/updates:** always include a `WHERE` clause; test on a transaction before committing
- **Fat stored procedures for business logic:** keep business logic in the application; use DB for data integrity
- **String-typed IDs:** use `UUID` or `BIGSERIAL` for primary keys — string comparison is slower and error-prone
- **Wide tables:** rows with 50+ columns indicate a normalization problem; consider vertical partitioning

## Tooling

| Tool | Purpose |
|------|---------|
| `EXPLAIN ANALYZE` | Query execution plan analysis |
| `pgBadger` | Log-based slow query analysis |
| `Flyway` / `Liquibase` | Migration management |
| `pg_stat_statements` | Query performance statistics |
| `pgcrypto` | Column-level encryption |
| `psql` `\d+` | Schema inspection |
