# Strategic Domain-Driven Design

Strategic DDD for system decomposition. This reference covers high-level domain analysis -- bounded contexts, subdomains, and context mapping. For tactical patterns (aggregates, entities, value objects, repositories), see architecture-patterns.md.

## Strategic vs Tactical DDD

| Level | Focus | Output |
|-------|-------|--------|
| **Strategic** (this reference) | System-level decomposition, team boundaries, integration | Bounded context map, subdomain classification |
| **Tactical** (architecture-patterns.md) | Inside a bounded context: aggregates, entities, value objects | Domain model, repository interfaces |

Strategic DDD answers: "How should we decompose the system?" Tactical DDD answers: "How should we model within each piece?"

## Subdomain Classification

Every part of a business domain falls into one of three categories:

| Subdomain | Definition | Investment Strategy | Build vs Buy |
|-----------|-----------|-------------------|--------------|
| **Core** | What makes your business unique, your competitive advantage | Invest heavily, best developers, custom build | Always build -- this IS your product |
| **Supporting** | Necessary for the business but not differentiating | Moderate investment, could outsource | Build or use configurable platform |
| **Generic** | Commodity capabilities everyone needs | Minimize investment | Buy, use SaaS, open source |

### Examples

- **E-commerce**: Core = recommendation engine, pricing strategy. Supporting = order management, inventory. Generic = email sending, payment processing, authentication.
- **Game studio**: Core = game mechanics, AI. Supporting = matchmaking, leaderboards. Generic = auth, analytics, crash reporting.
- **SaaS**: Core = the unique product feature. Supporting = billing, user management. Generic = email, logging, monitoring.

### Business Value Assessment

For each subdomain, assess:

- Competitive differentiation (1-5): how much does this differentiate us?
- Domain complexity (1-5): how complex is the business logic?
- Change frequency (1-5): how often do requirements change?

Core subdomains score high on differentiation. Supporting score high on necessity but low on differentiation. Generic score low on everything.

## Bounded Context Discovery

### Event Storming (preferred method)

See event-storming.md for full protocol. Key output: domain events cluster into bounded contexts.

### Domain Storytelling

1. Domain experts tell stories about how work gets done
2. Record as pictographic stories (actors, work objects, activities)
3. Identify where the language changes (same term means different things)
4. Language boundaries = bounded context boundaries

### Context Mapping Workshop

1. List all systems/components that exist today
2. For each pair, identify: do they share a model? Who owns the model?
3. Map the relationships using context mapping patterns (below)
4. Identify pain points (where integration is fragile)

## Context Mapping Patterns

| Pattern | Relationship | When to Use |
|---------|-------------|-------------|
| **Shared Kernel** | Two contexts share a subset of the domain model | Teams collaborate closely, model overlap is small and well-defined |
| **Customer-Supplier** | Upstream supplies data/services to downstream | Upstream prioritizes downstream's needs, clear dependency |
| **Conformist** | Downstream adopts upstream's model as-is | Upstream won't change, downstream has no leverage (e.g., external API) |
| **Anti-Corruption Layer** | Downstream translates upstream's model into its own | Models are incompatible, need isolation from external changes |
| **Open Host Service** | Upstream provides a well-defined protocol for all consumers | Multiple consumers, stable API, versioned |
| **Published Language** | Shared standard language for integration | Industry standards (EDI, HL7, FHIR) |
| **Partnership** | Two contexts evolve together, mutual dependency | Both teams coordinate releases |
| **Separate Ways** | No integration -- each context is independent | Costs of integration outweigh benefits |

### Choosing a Pattern

- Same team, same release cycle -> Shared Kernel or Partnership
- Different teams, cooperative -> Customer-Supplier
- Different teams, external dependency -> Conformist or Anti-Corruption Layer
- Many consumers -> Open Host Service + Published Language
- No real dependency -> Separate Ways

## Aggregate Boundary Design

Aggregates define consistency boundaries within a bounded context:

- **Rule 1**: Aggregates are transactional boundaries -- everything inside is strongly consistent
- **Rule 2**: Between aggregates, use eventual consistency (domain events)
- **Rule 3**: Reference other aggregates by ID, not by object reference
- **Rule 4**: Keep aggregates small -- large aggregates create contention
- **Rule 5**: One aggregate = one repository = one transaction

### Sizing Heuristic

- If two entities MUST be consistent in the same transaction -> same aggregate
- If they can be eventually consistent -> different aggregates
- If in doubt -> separate aggregates (easier to merge later than to split)

## Domain Events as Integration

Between bounded contexts:

- Publish domain events when significant state changes occur
- Other contexts subscribe and update their own models
- Events are facts that happened -- immutable, past tense ("OrderPlaced", "PaymentReceived")
- Eventual consistency is the norm between bounded contexts
- Anti-corruption layer translates incoming events into local domain language

### Event Schema Guidelines

- Include the aggregate ID that emitted the event
- Include a timestamp and correlation ID
- Include only data relevant to the event (not the entire aggregate state)
- Version event schemas (consumers must handle old versions)
- Events are contracts -- treat schema changes as breaking changes

## Ubiquitous Language

The shared vocabulary between domain experts and developers within a bounded context:

- Each bounded context has its OWN ubiquitous language
- The same term can mean different things in different contexts ("Account" in Banking vs "Account" in Authentication)
- Code must use domain language (class names, method names, variable names)
- When the language is ambiguous, the model is wrong -- refine until precise
- Glossary: maintain a living glossary for each bounded context

## When to Use Strategic DDD

- Complex domains with rich business logic
- Multiple teams working on the same system
- Enterprise systems with many integration points
- Evolving business models where domain understanding is still forming
- Systems where "the same word means different things to different people"

## When NOT to Use

- Simple CRUD applications
- Technical infrastructure (use volatility-based instead)
- Systems where the domain is well-understood and stable
- Very small teams (1-2 people -- the overhead isn't justified)

## Common Mistakes

- **One bounded context per entity**: bounded contexts are not database tables -- they represent a cohesive area of the domain with consistent language
- **Shared database across contexts**: breaks encapsulation, creates hidden coupling
- **Context boundaries matching org chart**: Conway's Law is a force to manage, not always to follow
- **Skipping subdomain classification**: leads to over-investing in generic capabilities and under-investing in core
- **Treating context mapping as a one-time exercise**: relationships between contexts evolve -- revisit the map when integration pain appears
