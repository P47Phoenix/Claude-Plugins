# Architect

**Invocation**: `delivery-team:architect`

Architecture agent with 11 specialized roles spanning software and game development.

## Software Architecture Roles

| Role | Focus Areas |
|------|-------------|
| **Solution Architect** | System design, C4 diagrams, ADRs, quality attributes |
| **Enterprise Architect** | TOGAF, capability mapping, technology radar, portfolio management |
| **Data Architect** | Data modeling, schema design, event sourcing, CQRS, governance |
| **Security Architect** | Threat modeling, STRIDE, zero trust, OWASP, auth patterns |
| **Compliance Officer** | SOC 2, ISO 27001, HIPAA, PCI DSS, audit preparation |
| **Privacy Engineer** | GDPR, CCPA, DPIA, consent management, data retention |
| **Incident Responder** | IR lifecycle, severity classification, tabletop exercises |

## Game Architecture Roles

| Role | Focus Areas |
|------|-------------|
| **Game Systems Architect** | ECS, game loop, combat, inventory, progression, economy |
| **Level/World Architect** | World structure, spatial partitioning, streaming, procedural generation |
| **Network/Multiplayer Architect** | Netcode, rollback, state sync, lag compensation, matchmaking |
| **Graphics/Rendering Architect** | Render pipeline, shaders, LOD, lighting, post-processing |

## How to Trigger

- "design architecture", "system design", "ADR", "C4 diagram"
- "microservices", "event-driven", "data model", "threat model"
- "ECS", "game loop", "netcode", "render pipeline"
- "compliance checklist", "SOC 2", "GDPR", "incident response"

## Prior Art Analysis

When user-provided specifications, existing designs, or architectural artifacts are present in the input (PRD with architecture decisions, design documents, technical specifications, prior ADRs), the Architect executes a Prior Art Analysis before any design work:

1. **Read and Summarize** -- Read all user-provided specs. Summarize what the user has already designed or decided, the scope and boundaries, and key architectural elements.
2. **Classify Each Element** -- Produce a classification table categorizing every element as either "Decision Already Made" (Architect must not propose alternatives) or "Open Question" (Architect is free to propose designs).
3. **Build On Existing Design** -- Validate feasibility of user decisions, fill gaps for open questions, and map the design to implementation artifacts (C4 diagrams, component breakdowns, data flows).
4. **Deviation Protocol** -- Proposing alternatives to existing decisions is only permitted when a specific, documented technical blocker makes the original decision infeasible. The blocker must be concrete and verifiable.

If no user-provided specs exist, this step is skipped entirely.

## Task Types

| Type | What It Does |
|------|-------------|
| **design** | Complete architecture with components, interactions, data flows, C4 diagrams |
| **review** | Evaluate architecture against quality attributes with severity findings |
| **document** | Write Architecture Decision Record (ADR) |
| **evaluate** | Compare technologies with weighted criteria matrix |
| **decompose** | Break system into services/components with boundaries |
| **model** | Produce C4 diagram descriptions (Mermaid/PlantUML) |
| **analyze-quality** | Analyze quality attributes with measurable scenarios |
| **compliance-checklist** | Produce framework-specific compliance checklist |
| **security-requirements** | Generate security requirements with OWASP mapping |
| **incident-response-plan** | Create IR plan with severity classification |
| **privacy-assessment** | Conduct DPIA with GDPR/CCPA mapping |

## Decomposition Strategies

Configurable via `architecture.decomposition` in config:

| Strategy | Method |
|----------|--------|
| **auto** (default) | Detect from context using decision matrix |
| **volatility** | IDesign: decompose by axes of change |
| **ddd** | Strategic DDD: subdomains, bounded contexts |
| **team-topology** | Inverse Conway: decompose by team cognitive load |
| **event-storming** | Event-driven: discover boundaries from domain events |
| **business-capability** | Traditional: map capabilities to services |

## Architecture Guardrails

Every architecture output enforces:

- Trade-offs must be stated (no "no trade-offs" allowed)
- NFRs must be quantified ("p99 latency under 200ms", not "fast")
- Data flows must specify format, protocol, and error handling
- Security is mandatory (auth, authorization, data protection, audit)
- Failure modes must be addressed (circuit breakers, retries, fallbacks)
- Game architectures require performance budgets (frame time, memory, bandwidth)

## Example Usage

```
User: "Design the architecture for a real-time chat system"

Role: Solution Architect | Task: design
References: architecture-patterns.md, c4-model.md, domain-discovery.md

Output: Architecture document with C4 diagrams, component breakdown,
        trade-off analysis, quality attributes, and risks
```
