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

## IDesign Decomposition Process

Based on Juval Lowy's "Righting Software" (Addison-Wesley, 2019) and the IDesign methodology. The process starts with understanding business processes, NOT with asking "what changes?" directly. Volatility is discovered through analysis, not interrogation.

### Phase 1: Business Process Walkthrough

Document every business process end-to-end before analyzing anything:

1. Have the user/PO walk through each core business process from start to finish
2. Document as a sequence: activity → decision → activity → outcome
3. Capture for each step: who does it, what data flows in/out, what decisions are made
4. Record variations and branches ("when X happens, the process goes to Y instead")
5. Do NOT analyze or decompose yet — just document faithfully

**Output**: Complete business process documentation for every major workflow.

### Phase 2: Identify Commonalities and Volatilities

Across ALL documented processes, analyze:

**Commonalities** — activities or logic that appear in multiple processes:
- Same calculation used in multiple workflows → candidate for a shared Engine
- Same data accessed by multiple processes → candidate for a shared Accessor
- Same infrastructure concern everywhere → candidate for a Utility

**Volatilities** — activities or logic that change frequently or independently:
- Mark each activity as: Stable (rarely changes) or Volatile (changes often/independently)
- For volatile activities, identify the axis: WHY does it change? (business rules, regulation, technology, integration, data format)
- Group activities that change for the SAME REASON together

### Phase 3: Define Components by What They Handle

Map the analyzed activities to IDesign service types:

1. Group volatile workflow/sequencing activities → **Managers**
2. Group volatile business logic/rules/calculations → **Engines**
3. Group volatile data access/integration activities → **Accessors**
4. Group common infrastructure activities → **Utilities**
5. Name each component by the volatility it encapsulates (e.g., "PricingEngine" — encapsulates pricing rule volatility)
6. Verify the dependency hierarchy: Managers → Engines → Accessors → Utilities
7. If a component doesn't fit cleanly → re-examine the volatility analysis

### Phase 4: Validate with Real Use Cases

Test the decomposition against 3-5 real change scenarios:

1. Pick upcoming or recent changes: "Last quarter, [X] changed. Under our decomposition, which components would change?"
2. **Good result**: change affects 1-2 components only
3. **Bad result**: change spreads across 3+ components → decomposition is wrong, re-group
4. For each scenario, document: what changed, which components were affected, whether the change was contained
5. If validation fails, go back to Phase 2 and re-analyze the volatility axes

### Phase 5: Project Planning

The IDesign method includes project planning based on the decomposition:

**Implementation Sequencing** (bottom-up):
1. Utilities first (no dependencies, foundation for everything)
2. Accessors second (depend only on Utilities)
3. Engines third (depend on Accessors + Utilities)
4. Managers last (depend on Engines, orchestrate the whole workflow)

**Interface Design Before Implementation**:
- Design ALL interfaces before writing ANY implementation code
- Interface design reviews are mandatory — the interface IS the architecture
- Interfaces should be stable; if they change often, the decomposition is wrong

**Effort Estimation**:
- High-volatility components need more investment in interface design (more time upfront, less rework later)
- High-volatility components should be assigned to senior developers
- Stable/utility components can be assigned to junior developers or outsourced

**Design Reviews**:
- Every interface reviewed before implementation begins
- Every component reviewed for dependency rule compliance
- Validation scenarios reviewed with stakeholders

## Volatility Assessment Matrix

After Phase 2, rate each identified component on a 1-5 scale:

| Component | Requirements | Technology | Integration | Data | Policy | Total | Classification |
|-----------|-------------|-----------|-------------|------|--------|-------|---------------|
| Checkout flow | 4 | 2 | 3 | 2 | 1 | 12 | Manager |
| Tax calculation | 2 | 1 | 2 | 1 | 5 | 11 | Engine |
| User auth | 1 | 3 | 4 | 1 | 2 | 11 | Accessor |
| Logging | 1 | 2 | 1 | 1 | 1 | 6 | Utility |

High-scoring components need strong encapsulation and senior developers. Low-scoring components can share boundaries or be commoditized.

## Reference

For the complete IDesign methodology including detailed project planning, estimation techniques, design review protocols, and case studies, see: Juval Lowy, "Righting Software" (Addison-Wesley Professional, 2019).

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
