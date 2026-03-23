# Volatility-Based Decomposition (IDesign Method)

Based on Juval Lowy's IDesign methodology. Decompose systems by axes of change -- isolate what's volatile from what's stable.

## Core Principle

Traditional decomposition (by domain, by layer, by function) breaks down when change patterns don't align with those boundaries. Volatility-based decomposition identifies WHAT CHANGES and encapsulates it behind stable interfaces. The result: changes to one axis of volatility don't cascade to other parts of the system.

## Volatility Analysis

How to identify axes of change:

- **Requirements volatility**: which business rules change frequently?
- **Technology volatility**: which technologies are likely to be replaced?
- **Integration volatility**: which external systems change their APIs?
- **Data volatility**: which data schemas evolve?
- **Policy volatility**: which regulatory/compliance rules change?

For each axis, ask: "If this changes, what else must change?" The answer defines the encapsulation boundary.

## IDesign Service Types (strict hierarchy)

| Service Type | Responsibility | Depends On | Example |
|-------------|---------------|-----------|---------|
| **Managers** | Workflow orchestration, sequence, state machine | Engines | OrderManager, CheckoutManager |
| **Engines** | Business logic, rules, calculations, algorithms | Accessors, Utilities | PricingEngine, TaxEngine, ValidationEngine |
| **Accessors** | Data access, external service integration, resource management | Utilities | CustomerAccessor, InventoryAccessor, PaymentGatewayAccessor |
| **Utilities** | Cross-cutting concerns, shared infrastructure | Nothing | Logger, Cache, Serializer, Cryptography |

### Dependency Rules (non-negotiable)

- Managers -> Engines -> Accessors -> Utilities (strict top-down)
- No skip-level calls (Manager cannot call Accessor directly)
- No peer calls (Engine A cannot call Engine B)
- No bottom-up calls (Accessor cannot call Engine)
- Utilities are stateless and have no dependencies

### Why This Hierarchy

- Managers encapsulate workflow volatility (if the checkout process changes, only CheckoutManager changes)
- Engines encapsulate business logic volatility (if pricing rules change, only PricingEngine changes)
- Accessors encapsulate data/integration volatility (if database changes, only the Accessor changes)
- Utilities encapsulate infrastructure volatility (if logging framework changes, only Logger changes)

## Decomposition Process

1. **List business capabilities** (not features -- capabilities)
2. **For each capability, identify volatility axes**: what changes, how often, why
3. **Group by volatility**: things that change for the same reason go in the same service
4. **Classify each service**: Manager, Engine, Accessor, or Utility
5. **Verify dependency rules**: no violations of the hierarchy
6. **Define interfaces**: stable contracts between services (change the implementation, not the interface)

## Volatility Assessment Matrix

For each component, rate on a 1-5 scale:

| Component | Requirements | Technology | Integration | Data | Policy | Total Score |
|-----------|-------------|-----------|-------------|------|--------|-------------|
| Checkout flow | 4 | 2 | 3 | 2 | 1 | 12 |
| Tax calculation | 2 | 1 | 2 | 1 | 5 | 11 |
| User auth | 1 | 3 | 4 | 1 | 2 | 11 |

High-scoring components need strong encapsulation. Low-scoring components can share boundaries.

## Interface Design

- Interfaces are the STABLE part -- they change rarely
- Implementations are the VOLATILE part -- they change frequently
- Every service exposes only its interface (not implementation details)
- Contracts: define input/output types, error types, and invariants
- Versioning: when interfaces must change, use semantic versioning

### Contract Design Guidelines

- Accept the most general type, return the most specific type
- Define explicit error types (not generic exceptions)
- Include idempotency keys for operations that modify state
- Document invariants (preconditions and postconditions)
- Never expose internal data structures through the interface

## When to Use Volatility-Based Decomposition

- High change rate: requirements change frequently, system must adapt
- Technology diversity: different components use different tech stacks
- Unclear domain boundaries: domain is evolving, can't clearly define bounded contexts yet
- Integration-heavy: many external systems with unstable APIs
- Long-lived systems: expected to evolve over years, need change resilience

## When NOT to Use

- Simple CRUD applications (over-engineering)
- Well-understood, stable domains (DDD is better)
- Small teams (< 3 people -- overhead not justified)
- Prototype/spike (too much ceremony)

## Comparison with Other Strategies

| Aspect | Volatility (IDesign) | DDD | Team Topology |
|--------|---------------------|-----|---------------|
| Decompose by | What changes | What the domain is | Who builds it |
| Best for | High change rate | Complex domains | Large organizations |
| Key artifact | Volatility analysis | Domain model | Team API |
| Risk | Over-isolation | Over-modeling | Over-splitting |

## Anti-Patterns

- **Layer-based decomposition pretending to be volatility-based**: API/BLL/DAL is NOT volatility decomposition -- it groups by technology layer, not by axis of change
- **Skip-level calls**: Manager calling Accessor directly breaks the hierarchy and couples workflow to data access
- **Fat Managers**: putting business logic in Managers (should be in Engines)
- **Anemic Engines**: Engines that just proxy to Accessors without adding business logic
- **Shared databases between services**: couples services through data, defeats encapsulation
- **Interface churn**: if interfaces change as often as implementations, the decomposition is wrong

## Applying IDesign to Microservices

Each IDesign service can be a microservice, but not all must be:

- Start with a modular monolith using IDesign structure
- Extract services when volatility analysis shows a clear boundary
- The dependency hierarchy maps to service communication patterns

### Extraction Criteria

Extract to a separate service when:
- The component's volatility is significantly different from its neighbors
- The component needs independent scaling
- The component uses a different technology stack
- Different teams own different sides of the interface

Do NOT extract when:
- The only reason is "microservices are better"
- The interface between components is chatty (high call frequency)
- The data model is tightly coupled (shared transactions)

## Practical Checklist

Before finalizing a volatility-based decomposition, verify:

- [ ] Every service has a clear volatility axis it encapsulates
- [ ] Dependency rules are followed with no exceptions
- [ ] Interfaces are stable (change less often than implementations)
- [ ] No shared mutable state between services
- [ ] Each service can be deployed independently
- [ ] Each service has a single team owner
- [ ] The decomposition survives at least three "what if X changes" scenarios
