# Architecture Patterns Reference

## Layered / N-Tier Architecture

**When to use:** CRUD-heavy applications, small teams, well-understood domains, tight deadlines where simplicity wins.

**Standard layers (top-down):**
- **Presentation** -- UI, API controllers, view models. No business logic.
- **Application/Service** -- Orchestrates use cases, transaction boundaries, DTO mapping. Thin by design.
- **Domain/Business** -- Core rules, entities, value objects, domain services. Framework-agnostic.
- **Infrastructure/Persistence** -- Database access, external service clients, file I/O, messaging.

**The strict rule:** Each layer may only depend on the layer directly below it. Skip-layer calls (presentation calling persistence) indicate a breakdown.

**Anti-patterns:**
- **Leaky layers** -- ORM entities exposed to the API surface. Changes in schema ripple everywhere.
- **Anemic domain model** -- Domain layer is just data bags; all logic lives in services. You have a layered CRUD wrapper, not a layered architecture.
- **Layer bloat** -- Adding layers "for future flexibility." Every layer that doesn't carry its weight is friction.

---

## Hexagonal / Ports and Adapters

**Core concept:** The application defines ports (interfaces) for how it interacts with the outside world. Adapters implement those ports. The application core has zero knowledge of infrastructure.

**Port types:**
- **Driving (inbound):** Define how the outside world invokes the application -- HTTP controllers, CLI handlers, message consumers, test harnesses.
- **Driven (outbound):** Define what the application needs from the outside -- repository interfaces, notification gateways, payment processors, clock abstractions.

**Adapter examples:**
- `PostgresOrderRepository` implements `OrderRepository` port
- `StripePaymentGateway` implements `PaymentGateway` port
- `InMemoryOrderRepository` implements the same port for tests

**Key benefit:** You can swap any adapter without touching domain logic. Tests run against in-memory adapters at full speed.

**When it breaks down:** Over-engineering simple CRUD apps. If your "domain logic" is just save-and-retrieve, ports and adapters add ceremony without value.

---

## Clean Architecture

**The dependency rule:** Source code dependencies must point inward only. Nothing in an inner circle can reference anything in an outer circle.

**Layers (inside-out):**
1. **Entities** -- Enterprise-wide business rules, domain objects
2. **Use Cases** -- Application-specific business rules, orchestration
3. **Interface Adapters** -- Controllers, presenters, gateways (convert between use case and external formats)
4. **Frameworks & Drivers** -- Web framework, database driver, UI framework

**Boundaries are enforced by:** Dependency inversion. Use cases define interfaces; outer layers implement them.

**Practical reality:** Most teams collapse this to three layers (domain, application, infrastructure) and that works fine. The principle matters more than the exact ring count.

---

## Microservices

**Service boundary heuristics:**
- Aligned to a bounded context (DDD)
- Owned by a single team (Conway's Law)
- Independently deployable without coordinating with other services
- Has its own data store (no shared databases)

**Communication patterns:**

| Pattern | Use When | Watch Out For |
|---------|----------|---------------|
| Synchronous REST/gRPC | Query responses, low-latency needs | Temporal coupling, cascading failures |
| Async messaging (events) | Decoupled workflows, eventual consistency is acceptable | Message ordering, duplicate handling |
| Request/reply over messaging | Need async but caller needs a response | Correlation IDs, timeout handling |

**Decomposition strategies:**
- **By business capability:** "Order Management," "Inventory," "Shipping"
- **By subdomain:** Core, supporting, generic (DDD classification)
- **Strangler fig:** Incrementally extract from monolith -- route traffic to new service, retire old code

**Data ownership:** Each service owns its data. If Service A needs data from Service B, it either queries B's API or maintains a local projection via events. Sharing a database is the fastest path to a distributed monolith.

---

## Event-Driven Architecture

### Event Sourcing
Store state as a sequence of events rather than current state. Rebuild state by replaying events. Useful when audit trails are mandatory or you need temporal queries ("what was the account balance on March 3?").

**Cost:** Increased complexity in event schema evolution, snapshot management, and eventual consistency.

### CQRS (Command Query Responsibility Segregation)
Separate the write model (optimized for business rules) from the read model (optimized for queries). CQRS does not require event sourcing, and event sourcing does not require CQRS -- but they pair well.

### Saga Patterns

**Orchestration:** A central coordinator tells each participant what to do and handles compensations on failure. Easier to understand, but the orchestrator can become a god service.

**Choreography:** Each service reacts to events and publishes its own. No central coordinator. More decoupled, but harder to trace the full workflow and debug failures.

**Decision criteria:** Use orchestration when the workflow has complex branching or compensating logic. Use choreography when services are truly independent and the flow is linear.

---

## Modular Monolith

**What it is:** A single deployable unit with strictly enforced module boundaries. Modules communicate through well-defined interfaces, not shared internals.

**Module boundary rules:**
- Each module owns its database schema (separate schemas or table prefixes)
- Modules expose public APIs (interfaces/facades) and hide internals
- Cross-module calls go through these APIs, never direct database access
- Modules can be extracted to services later if needed

**Choose over microservices when:**
- Team is small (under 15-20 engineers)
- Deployment complexity of distributed systems is not justified
- You need the architectural discipline but not the operational overhead
- You are in the early stages and the domain boundaries are not yet clear

---

## Domain-Driven Design

### Bounded Contexts
A bounded context is a boundary within which a particular domain model is defined and applicable. The term "Customer" in billing and in shipping may have different attributes and behaviors -- that is fine and expected.

### Aggregates
A cluster of domain objects treated as a single unit for data changes. The aggregate root is the only entry point. Keep aggregates small -- one or two entities plus value objects. Large aggregates cause contention.

### Ubiquitous Language
The domain vocabulary shared between developers and domain experts, used in code, tests, and conversation. If the code says `OrderProcessor` but the business says "fulfillment," you have a language gap that will cause bugs.

### Context Mapping Strategies

| Pattern | Relationship | When to Use |
|---------|-------------|-------------|
| Shared Kernel | Two teams share a subset of the model | Tight collaboration, high trust |
| Customer-Supplier | Upstream supplies what downstream needs | Clear dependency, negotiation possible |
| Conformist | Downstream adopts upstream's model as-is | No leverage to influence upstream |
| Anti-Corruption Layer | Downstream translates upstream's model | Protecting your model from a legacy or external system |
| Open Host Service | Upstream provides a well-defined protocol | Multiple consumers, stable API needed |
| Published Language | A shared interchange format (e.g., canonical events) | Cross-system integration |

---

## API Gateway and BFF Patterns

**API Gateway:** A single entry point that handles cross-cutting concerns -- authentication, rate limiting, routing, protocol translation. Keep it thin. Business logic in the gateway is an anti-pattern.

**Backend for Frontend (BFF):** A dedicated backend per frontend type (mobile, web, third-party). Each BFF aggregates and transforms backend service responses for its specific client. Prevents a one-size-fits-all API that serves no client well.

**When to use BFF:** When different clients need significantly different data shapes, aggregation levels, or protocols. If all clients need the same thing, a single API gateway suffices.

---

## Decision Matrix

| Criteria | Layered | Hex/Clean | Modular Monolith | Microservices | Event-Driven |
|----------|---------|-----------|-------------------|---------------|--------------|
| Team size | Small | Small-Med | Small-Med | Large | Med-Large |
| Domain complexity | Low | Med-High | Med-High | High | High |
| Deployment independence | N/A | N/A | Low | High | High |
| Operational complexity | Low | Low | Low | High | High |
| Data consistency needs | Strong | Strong | Strong | Eventual OK | Eventual OK |
| Time to first release | Fast | Medium | Medium | Slow | Slow |
| Best starting point | Yes | Yes | Yes | No | No |

**Rule of thumb:** Start with a modular monolith using clean architecture principles. Extract to microservices when you have evidence (not speculation) that you need independent deployment or scaling.

---

## Anti-Patterns

**Distributed Monolith:** Microservices that must be deployed together, share databases, or require lockstep changes. You have all the complexity of distribution with none of the benefits.

**Shared Database:** Multiple services reading/writing the same tables. Schema changes require coordinating every service. Ownership boundaries dissolve.

**God Service:** One service that orchestrates everything, knows every other service, and accumulates logic that should live elsewhere. Often called "orchestrator" or "platform-service."

**Nano-services:** Services so small they cannot justify their operational overhead. A service that wraps a single function and adds network latency, deployment pipelines, and monitoring for no gain.

**Resume-Driven Architecture:** Choosing microservices, Kubernetes, event sourcing, and CQRS for a team of three building an internal tool. Match architecture to actual constraints, not aspirational ones.
