# Data Modeling Reference

## Relational Modeling

### Normalization

Normalization eliminates redundancy and update anomalies. In practice, go to 3NF for transactional systems. Beyond that is academic.

**1NF**: Every column holds atomic values. No repeating groups or arrays.
- Violation: `phone_numbers: "555-1234, 555-5678"` in a single column.
- Fix: Separate `phone_numbers` table with one row per phone number and a foreign key to the parent.

**2NF**: 1NF plus every non-key column depends on the entire composite key, not just part of it.
- Violation: Table `order_items(order_id, product_id, product_name, quantity)` -- `product_name` depends only on `product_id`, not on the full key `(order_id, product_id)`.
- Fix: Move `product_name` to a `products` table.

**3NF**: 2NF plus no transitive dependencies. Non-key columns depend only on the primary key, not on other non-key columns.
- Violation: `employees(id, department_id, department_name)` -- `department_name` depends on `department_id`, not directly on `id`.
- Fix: Move `department_name` to a `departments` table.

### When to Denormalize

- Read-heavy workloads where join cost dominates query time.
- Reporting/analytics tables that are populated via ETL (materialized views, summary tables).
- Caching layers where staleness is acceptable.
- When you have measured the join cost and it is the bottleneck. Not before.

Anti-pattern: premature denormalization based on theoretical performance concerns. Measure first.

### Indexing Strategy

**B-tree** (default in most RDBMS): Supports equality and range queries. Use for primary keys, foreign keys, columns in WHERE/ORDER BY/JOIN clauses. Composite indexes: leftmost prefix rule applies -- `INDEX(a, b, c)` supports queries on `(a)`, `(a, b)`, and `(a, b, c)` but not `(b)` or `(c)` alone.

**Hash indexes**: Equality-only lookups. Faster than B-tree for exact match but no range support. Use for lookup tables with exact-match access patterns.

**GIN (Generalized Inverted Index)**: For array containment, full-text search, JSONB queries in PostgreSQL. Use when querying inside composite values.

**GiST (Generalized Search Tree)**: For geometric data, range types, full-text search (alternative to GIN with smaller index size but slower reads).

**Covering indexes**: Include all columns needed by a query so the engine never touches the table (index-only scan). In PostgreSQL: `CREATE INDEX idx ON orders(customer_id) INCLUDE (total, status)`. Use for high-frequency queries where eliminating table access matters.

**Index maintenance**: Every index slows writes. Audit unused indexes quarterly. In PostgreSQL: `pg_stat_user_indexes.idx_scan = 0` indicates an unused index.

## Document/NoSQL Modeling

### Embedding vs Referencing

| Criterion | Embed | Reference |
|-----------|-------|-----------|
| Read pattern | Always read together | Read independently |
| Cardinality | One-to-few (< 20) | One-to-many or many-to-many |
| Update frequency | Rarely changes | Frequently changes |
| Document size | Stays under 16MB (MongoDB limit) | Would exceed limits |
| Data consistency | Tolerate duplication | Need single source of truth |

### Access-Pattern-Driven Design

Start from your queries, not your entities. List the top 10 queries the application will execute. Design documents so each query hits a single collection with no joins. This is the opposite of relational design.

Example: A blog platform. Query: "Show post with all comments." Relational: `posts` table + `comments` table + JOIN. Document: embed comments array inside the post document (if comments per post < 100 and comments are always read with the post).

### Handling Relationships in NoSQL

- **One-to-few**: Embed. Store addresses inside a user document.
- **One-to-many**: Embed if read together, reference if not. Store order line items embedded in orders, but reference products by ID.
- **Many-to-many**: Use reference arrays on both sides, or a junction collection. Denormalize the fields you need for display to avoid lookups.

## Event Sourcing Data Model

### Event Store Schema

```sql
CREATE TABLE events (
    event_id        UUID PRIMARY KEY,
    aggregate_type  VARCHAR(255) NOT NULL,
    aggregate_id    UUID NOT NULL,
    sequence_number BIGINT NOT NULL,
    event_type      VARCHAR(255) NOT NULL,
    event_data      JSONB NOT NULL,
    metadata        JSONB,       -- correlation_id, causation_id, user_id
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE (aggregate_id, sequence_number)
);

CREATE INDEX idx_events_aggregate ON events(aggregate_id, sequence_number);
CREATE INDEX idx_events_type ON events(event_type, created_at);
```

### Projections / Read Models

Projections consume events and build query-optimized read models. Each projection is an independent consumer that can be rebuilt from scratch by replaying all events. Store a checkpoint (last processed event position) per projection.

Design projections per use case. A "customer dashboard" projection denormalizes customer data differently than an "admin reporting" projection. Duplication is expected and intentional.

### Snapshots

After N events (typically 50-100), store a snapshot of the aggregate state. When loading, read the latest snapshot and replay only events after it. This bounds the replay cost.

```sql
CREATE TABLE snapshots (
    aggregate_id    UUID NOT NULL,
    sequence_number BIGINT NOT NULL,
    snapshot_data   JSONB NOT NULL,
    created_at      TIMESTAMPTZ NOT NULL,
    PRIMARY KEY (aggregate_id, sequence_number)
);
```

### Event Versioning and Upcasting

Events are immutable. When the schema of an event type changes:
1. Create a new event version (e.g., `OrderPlacedV2`).
2. Write an upcaster that transforms V1 events to V2 format at read time.
3. Never modify stored events.

Upcasters form a chain: V1 -> V2 -> V3. Keep them simple -- field renames, default values for new fields, field removals.

## Data Flow Diagrams

### Notation

Sources (external systems, users) -> Transformations (processes that change data) -> Sinks (data stores, external systems). Use arrows labeled with the data entity or event name.

### ETL vs ELT

**ETL** (Extract, Transform, Load): Transform before loading into the target. Use when the target system has limited compute (traditional data warehouse) or when you need to filter/clean before storage.

**ELT** (Extract, Load, Transform): Load raw data, then transform in-place. Use when the target has strong compute (cloud data warehouses like BigQuery, Snowflake, Redshift). Modern default.

### Streaming vs Batch

**Batch**: Scheduled runs (hourly, daily). Use for reporting, analytics, and data that tolerates latency. Simpler to build, debug, and retry.

**Streaming**: Continuous processing with seconds-level latency. Use for real-time dashboards, fraud detection, event-driven workflows. Higher operational complexity. Frameworks: Kafka Streams, Flink, Spark Structured Streaming.

Decision: if the business can wait an hour for the data, use batch. Streaming adds significant complexity.

## Data Governance

### Data Classification

| Level | Label | Examples | Handling |
|-------|-------|----------|----------|
| 1 | Public | Marketing content, public APIs | No restrictions |
| 2 | Internal | Employee directories, internal docs | Access control, no public exposure |
| 3 | Confidential | Customer PII, financial data | Encryption, audit logging, access review |
| 4 | Restricted | Payment card data, health records, credentials | Encryption, tokenization, strict access, regulatory compliance |

### Data Quality Dimensions

- **Accuracy**: Does the data reflect reality? Validate against source systems.
- **Completeness**: Are required fields populated? Measure null rates.
- **Consistency**: Do related records agree? Cross-system reconciliation checks.
- **Timeliness**: Is the data current enough for its use case? Measure lag from source.
- **Uniqueness**: Are duplicates controlled? Deduplication rules and monitoring.

### Data Lineage

Track where data originates, how it transforms, and where it lands. Minimum viable lineage: for every table in your data warehouse, document the source system and the transformation logic. Tools: dbt lineage graphs, Apache Atlas, or a manually maintained lineage catalog.

## Schema Evolution Strategies

**Backward compatible**: New schema can read old data. Achieved by: adding optional fields with defaults, not removing fields, not renaming fields.

**Forward compatible**: Old schema can read new data. Achieved by: consumers ignore unknown fields.

**Full compatibility**: Both backward and forward. Required for zero-downtime deployments where old and new versions coexist.

**Breaking changes**: Require a migration. Strategies: dual-write (write to old and new schema during transition), expand-contract (add new field, migrate data, remove old field), or versioned schemas (v1/v2 endpoints).

## CQRS Read Model Design

### Projection Patterns

- **Simple projection**: One event type maps to one read model update. `OrderPlaced` -> insert into `orders_view`.
- **Multi-stream projection**: Combines events from multiple aggregates. `OrderPlaced` + `PaymentReceived` + `ShipmentDispatched` -> update `order_status_view`.
- **Windowed projection**: Aggregates events over time. `PageViewed` events -> `daily_page_views` summary.

### Eventual Consistency Handling

The read model lags behind the write model. Strategies:
- **Read-your-writes**: After a command, query the write side directly (or use a version token to wait for the read model to catch up).
- **Causal consistency**: Include a version/sequence number in responses. Clients send it back, and the read side waits if it has not processed that version yet.
- **Staleness tolerance**: For many use cases, a few seconds of lag is acceptable. Design the UI to communicate this.

### Read Model Rebuilding

Every projection must be rebuildable from the event store. Procedure: drop the read model table, reset the projection checkpoint to zero, replay all events. This must be tested regularly and should complete in a bounded time (hours, not days).

## Data Partitioning

### Horizontal Partitioning (Sharding)

Split rows across partitions by a shard key. Choose the shard key carefully:
- High cardinality (many distinct values) to distribute evenly.
- Aligns with query patterns (most queries include the shard key).
- Avoids hotspots (do not shard by date if most queries hit today's data).

Common shard keys: tenant ID (multi-tenant SaaS), geographic region, customer ID.

### Vertical Partitioning

Split columns into separate tables/stores. Use when some columns are accessed frequently and others rarely (e.g., separate `user_profile` from `user_preferences`), or when some columns are very large (BLOBs).

### Functional Partitioning

Assign different data domains to different databases entirely. Orders in one database, inventory in another. This is the data side of domain-driven design and bounded contexts.

## Master Data Management

### Golden Record

A single authoritative version of each entity, reconciled from all source systems. Define which system is authoritative for each field. Example: CRM owns customer name and address; billing system owns payment method; identity system owns email.

### Data Deduplication

Match and merge records across systems using deterministic rules (exact match on email) and probabilistic rules (fuzzy match on name + address). Always keep source records linked to the golden record for audit and rollback.

### Cross-System Identity

Assign a universal identifier (UUID) at the MDM layer. Each source system keeps its own ID. Maintain a mapping table: `(universal_id, source_system, source_id)`. All downstream systems reference the universal ID.
