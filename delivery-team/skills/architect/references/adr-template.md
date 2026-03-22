# Architecture Decision Records (ADR) Reference

## What is an ADR

An Architecture Decision Record captures a single architectural decision along with its context and consequences. ADRs create a decision log that explains why a system is the way it is -- not just what was decided, but what alternatives were considered and what trade-offs were accepted.

---

## Nygard's Original Template

Michael Nygard's original template is intentionally minimal:

```markdown
# [ADR-NNNN] Title

## Status
[Proposed | Accepted | Deprecated | Superseded by ADR-NNNN]

## Context
What is the issue that we are seeing that motivates this decision or change?

## Decision
What is the change that we are proposing and/or doing?

## Consequences
What becomes easier or more difficult to do because of this change?
```

This format works well for teams just starting with ADRs. Its simplicity lowers the barrier to writing them.

---

## Extended Template

For teams that need more rigor, traceability, or governance:

```markdown
# [ADR-NNNN] Title (short noun phrase: "Use PostgreSQL for Order Data")

## Status
[Proposed | Accepted | Deprecated | Superseded by ADR-NNNN]

## Date
YYYY-MM-DD

## Deciders
List the people involved in making this decision (names or roles).

## Context
Describe the forces at play: technical constraints, business requirements, team
capabilities, timeline pressure, existing system state. Be specific. Include
quantitative data when available (expected load, data volumes, latency targets).

## Decision
State the decision as a definitive statement: "We will use X" or "We will adopt Y
pattern for Z." Include enough detail that someone unfamiliar with the discussion
can understand what was decided and implement it.

## Consequences

### Positive
- What becomes easier, faster, or more reliable

### Negative
- What becomes harder, slower, or introduces new risks

### Neutral
- Side effects that are neither clearly positive nor negative

## Alternatives Considered

| Alternative | Pros | Cons | Reason Rejected |
|-------------|------|------|-----------------|
| Option A | ... | ... | ... |
| Option B | ... | ... | ... |

## Related ADRs
- Supersedes: ADR-NNNN (if applicable)
- Relates to: ADR-NNNN
- Enabled by: ADR-NNNN
```

---

## When to Write an ADR

Write an ADR when the decision:
- **Is costly to reverse.** Choosing a database, a programming language, a messaging platform, a cloud provider.
- **Is cross-cutting.** Affects multiple teams, services, or modules. Authentication strategy, API versioning approach, logging standards.
- **Is contentious.** The team debated multiple options. Record the reasoning so the debate does not repeat in six months.
- **Sets a precedent.** Future decisions will follow this pattern. "All new services will use gRPC for inter-service communication."
- **Has significant trade-offs.** You are consciously accepting downsides. Document what you are giving up and why.

## When NOT to Write an ADR

- **Trivial decisions.** Choosing a logging library when only one option exists. Naming a variable.
- **Easily reversible decisions.** Using a particular test framework that can be swapped in a day.
- **No real alternatives.** If there is only one viable option and everyone agrees, a brief note in a commit message or ticket suffices.
- **Implementation details.** How a function is structured internally, which design pattern a single class uses.

---

## ADR Lifecycle

```
Proposed --> Accepted --> [Active indefinitely]
                      \-> Deprecated (no longer relevant, system changed)
                      \-> Superseded by ADR-NNNN (replaced by a new decision)
```

**Proposed:** The ADR is drafted and under review. Not yet binding.

**Accepted:** The team has agreed to this decision. It guides implementation.

**Deprecated:** The context that motivated this decision no longer applies. The system has changed enough that the decision is moot. The ADR stays in the log for historical reference.

**Superseded:** A new ADR explicitly replaces this one. The old ADR is updated with a link to its successor. Never delete old ADRs -- they document the evolution of thinking.

---

## Linking ADRs

- **Supersedes / Superseded by:** ADR-0015 replaces ADR-0003. Update ADR-0003's status to "Superseded by ADR-0015."
- **Relates to:** ADR-0012 (caching strategy) relates to ADR-0008 (database choice) because the caching approach depends on the database's read performance.
- **Enabled by:** ADR-0020 (use Kubernetes) is enabled by ADR-0018 (containerize all services).

Always link bidirectionally. If ADR-0015 supersedes ADR-0003, both should reference each other.

---

## Numbering and Naming Conventions

**Numbering:** Sequential integers, zero-padded to four digits: ADR-0001, ADR-0002, etc. Never reuse numbers, even for rejected or superseded ADRs.

**File naming:** `NNNN-short-description.md` in a dedicated `docs/adr/` or `docs/architecture/decisions/` directory.

Examples:
- `0001-use-postgresql-for-order-data.md`
- `0002-adopt-event-driven-communication.md`
- `0003-authentication-via-oauth2.md`

**Title format:** Short noun phrase describing the decision. "Use PostgreSQL for Order Data," not "We discussed databases and decided to go with PostgreSQL after considering MongoDB and DynamoDB."

---

## Example ADR 1: Technology Choice

```markdown
# ADR-0004: Use RabbitMQ for Asynchronous Messaging

## Status
Accepted

## Date
2025-09-14

## Deciders
Platform team (J. Torres, M. Chen, S. Park)

## Context
The order processing pipeline currently uses synchronous HTTP calls between
the API server and the fulfillment service. Under load (>500 orders/minute
during flash sales), the fulfillment service becomes a bottleneck, causing
cascading timeouts in the API server. We have a 99.9% availability SLA for
the order placement endpoint.

We need an asynchronous messaging solution to decouple order placement from
fulfillment processing. Requirements:
- At-least-once delivery guarantee
- Message persistence across broker restarts
- Support for dead-letter queues for failed message handling
- Operational simplicity (team has 2 infrastructure engineers)
- Throughput: sustain 2,000 messages/second peak

## Decision
We will use RabbitMQ (managed via Amazon MQ) as our message broker for
asynchronous communication between the API server and fulfillment service.
Messages will use the AMQP 0-9-1 protocol with durable queues and publisher
confirms enabled.

## Consequences

### Positive
- Order placement is no longer blocked by fulfillment processing time
- Failed fulfillment attempts can be retried via dead-letter queue without
  affecting the customer experience
- RabbitMQ's routing model (exchanges + bindings) supports future fan-out
  to additional consumers (analytics, notifications)

### Negative
- Introduces eventual consistency: order status is not immediately "fulfilled"
  after placement
- Team must learn AMQP concepts and RabbitMQ operational patterns
- Additional infrastructure to monitor and maintain (mitigated by using
  managed Amazon MQ)

### Neutral
- Message serialization adds ~2ms latency per message, negligible for this
  use case

## Alternatives Considered

| Alternative | Pros | Cons | Reason Rejected |
|-------------|------|------|-----------------|
| Apache Kafka | Higher throughput, built-in log retention, replay capability | Operational complexity too high for team size, overkill for current volume | Team lacks Kafka expertise; our throughput needs do not justify the overhead |
| Amazon SQS | Fully managed, zero ops | No routing/exchange model, limited message ordering, vendor lock-in | Need flexible routing for future consumers; want broker-level portability |
| Keep synchronous + add retries | No new infrastructure | Does not solve the coupling problem; retries increase load during incidents | Addresses symptoms, not root cause |

## Related ADRs
- Relates to: ADR-0002 (adopt event-driven communication)
- Enabled by: ADR-0001 (containerize services for independent deployment)
```

---

## Example ADR 2: Architectural Pattern

```markdown
# ADR-0007: Adopt Modular Monolith for New Platform

## Status
Accepted

## Date
2025-11-03

## Deciders
Architecture review board (R. Nguyen, L. Hoffman, D. Okafor, A. Petrov)

## Context
We are rebuilding our legacy platform from scratch. The current system is a
traditional monolith with no module boundaries -- any code can call any other
code, and the database has 400+ tables with undocumented cross-references.

The team has 12 engineers. Our previous attempt at microservices (2024) failed
due to operational overhead: the team spent more time debugging distributed
tracing and managing 23 deployment pipelines than building features.

We need strong architectural boundaries to prevent the new system from
becoming another big ball of mud, but without the operational cost of a
distributed system.

Domain analysis has identified 5 bounded contexts: Catalog, Orders,
Customers, Inventory, and Billing.

## Decision
We will build the new platform as a modular monolith. Each bounded context
will be a separate module within a single deployable unit, with the following
constraints enforced:

1. Each module owns its own database schema (separate PostgreSQL schemas)
2. Modules communicate only through a defined internal API (interfaces), never
   by direct database access across schemas
3. Module dependencies are declared explicitly and checked by the build system
   (ArchUnit tests for Java)
4. If a module needs to be extracted to a service in the future, its interface
   already defines the service contract

## Consequences

### Positive
- Single deployment pipeline reduces operational burden
- Strong module boundaries prevent cross-cutting coupling
- Easier debugging: everything runs in one process, standard stack traces
- Extraction to microservices is possible later with minimal refactoring
  because module interfaces are already defined

### Negative
- Entire application must be deployed together, even for single-module changes
- Scaling is all-or-nothing (cannot scale Billing independently of Catalog)
- Requires discipline: developers must resist the temptation to bypass module
  interfaces for convenience

### Neutral
- Technology choices (language, framework) are shared across all modules

## Alternatives Considered

| Alternative | Pros | Cons | Reason Rejected |
|-------------|------|------|-----------------|
| Microservices from day one | Independent deployment, independent scaling | Operational overhead exceeds team capacity; domain boundaries not yet validated | Previous failed attempt; team size does not support distributed ops |
| Traditional monolith (no module boundaries) | Simplest to start | Proven to degrade into a big ball of mud; this is exactly what we are replacing | Repeats the problem we are solving |
| Service-oriented with 2-3 large services | Less operational overhead than full microservices | Arbitrary grouping of bounded contexts; does not prevent coupling within each service | Module boundaries within services would still be needed, so start there |

## Related ADRs
- Supersedes: ADR-0003 (microservices architecture -- abandoned)
- Relates to: ADR-0005 (use PostgreSQL schemas for module isolation)
```

---

## Anti-Patterns in ADR Writing

**Vague context:** "We need a database" tells future readers nothing. State the workload characteristics, data model, consistency requirements, scale expectations, and team expertise.

**Post-hoc ADRs without real context:** Writing ADRs after the fact to satisfy a process checkbox. These ADRs describe what was done but not why. If you must write retroactively, interview the people who made the decision and reconstruct the context honestly.

**No alternatives listed:** An ADR that presents only the chosen option signals that either no analysis was done or the analysis is being hidden. Even obvious choices have alternatives worth documenting (even if the alternative is "do nothing").

**ADRs that are actually design documents:** An ADR captures a decision, not a complete design. If your ADR is 10 pages with UML diagrams and API specifications, extract the design into a separate document and keep the ADR focused on the decision.

**Never-updated status:** ADRs stuck in "Proposed" forever, or decisions that have clearly been reversed but the ADR still says "Accepted." Assign ADR maintenance as part of architecture review cadence.
