# Enterprise Architecture Patterns

## TOGAF ADM -- Practical Subset

The Architecture Development Method has 10 phases. In practice, five matter most. The others (Migration Planning, Implementation Governance, Architecture Change Management, Requirements Management) are process overhead that organizations fold into delivery governance.

### Architecture Vision (Phase A)

Produce a one-page architecture vision document that answers: What business problem are we solving? What are the constraints? What does success look like? The deliverable is not a diagram -- it is stakeholder alignment. Run a single workshop with business sponsors and technical leads. Output: problem statement, scope boundaries, key stakeholders, constraints, and a request for architecture work.

Anti-pattern: skipping this phase and jumping to technology selection. Every failed architecture engagement traces back to unclear scope or misaligned stakeholders.

### Business Architecture (Phase B)

Map business capabilities, value streams, and organizational structure. Do not model the entire enterprise -- scope to the domain under change. Identify which capabilities are affected, who owns them, and what processes cross capability boundaries. Output: capability map (scoped), value stream diagram, stakeholder map.

### Information Systems Architecture (Phase C)

Split into Application Architecture and Data Architecture. For applications: identify logical application components, their responsibilities, and integration points. For data: identify data entities, ownership, flow between systems, and data quality requirements. Output: logical application component diagram, data entity relationship diagram, data flow diagram.

### Technology Architecture (Phase D)

Map logical components to physical technology choices. This is where you make platform, infrastructure, and tooling decisions. Keep it decision-oriented: for each logical component, document the technology choice, rationale, and alternatives considered. Output: technology mapping table, deployment topology diagram.

### Opportunities and Solutions (Phase E)

Define the transition architectures -- how you get from current state to target state. Identify work packages, sequence them by dependency and risk, and define transition states. Output: roadmap with transition architectures, work package definitions, dependency matrix.

## Business Capability Mapping

A business capability is what the business does (not how). "Process Customer Orders" is a capability. "Use SAP ECC" is not.

### How to Build One

1. Start from the value chain. Identify primary activities (inbound logistics, operations, outbound logistics, marketing/sales, service) and support activities (HR, finance, technology, procurement).
2. Decompose each to level 2 (12-20 capabilities total for most organizations). Level 3 only where the architecture engagement requires it.
3. Map current systems to capabilities. Each system may support multiple capabilities. Each capability may be served by multiple systems.
4. Identify gaps (capabilities with no system support) and overlaps (capabilities served by multiple redundant systems).

### Using for Investment Decisions

Heat-map capabilities by: strategic importance (high/medium/low), current maturity (strong/adequate/weak), and investment need (high/medium/low). Capabilities that are strategically important but weak maturity are your investment priorities.

## Technology Radar

### Ring Definitions

| Ring | Meaning | Action |
|------|---------|--------|
| Adopt | Proven, default choice for its category | Use in production freely |
| Trial | Promising, validated in limited production use | Use in non-critical paths, gather data |
| Assess | Interesting, worth investigating | Run PoCs, evaluate fit |
| Hold | Do not start new work with this technology | Migrate away over time |

### Evaluation Criteria for Placement

- Production track record (internal and industry)
- Community/vendor health and trajectory
- Fit with existing skills and ecosystem
- Operational maturity (monitoring, debugging, deployment)
- Migration cost from current technology

### Maintenance Cadence

Review quarterly. Each review: promote or demote 3-5 items. Require a sponsor for any technology entering Trial or Adopt (someone who will own operational readiness). Publish the radar internally. Archive previous versions for trend analysis.

## Application Portfolio Management -- TIME Model

Assess every application in the portfolio on two axes: technical health (code quality, maintainability, security, scalability) and business value (revenue contribution, user satisfaction, strategic alignment).

| Quadrant | Technical Health | Business Value | Action |
|----------|-----------------|----------------|--------|
| Tolerate | Low | Low | Maintain minimally, do not invest |
| Invest | High | High | Fund enhancements, scale |
| Migrate | Low | High | Rewrite or replace -- the system matters but is failing |
| Eliminate | High or Low | Very Low | Decommission, consolidate users elsewhere |

### Assessment Process

1. Inventory all applications (include shadow IT).
2. Score each on technical health (0-5) and business value (0-5) using consistent rubrics.
3. Plot on the 2x2 matrix.
4. Validate with business and technical stakeholders.
5. Define action plans per quadrant with timelines.

Anti-pattern: putting everything in "Invest." If more than 30% of your portfolio is in Invest, your assessment criteria are too generous.

## Enterprise Integration Patterns

### ESB (Enterprise Service Bus)

Use when: you have dozens of legacy systems with heterogeneous protocols (SOAP, FTP, proprietary), need complex message transformation and routing, and have a centralized integration team. Declining pattern -- avoid for greenfield.

### API Gateway

Use when: you are exposing services to external consumers or internal front-ends, need rate limiting, authentication, and versioning at the edge. Modern default for synchronous request/response integration.

### Event Mesh

Use when: you need decoupled, asynchronous communication between domains, event-driven architecture, or cross-region event distribution. Implementations: Kafka (high throughput, log-based), RabbitMQ (flexible routing), cloud-native (EventBridge, Pub/Sub).

### Decision Matrix

| Criterion | ESB | API Gateway | Event Mesh |
|-----------|-----|-------------|------------|
| Coupling | Medium (central) | Low (edge) | Very Low |
| Latency | Higher | Low | Variable |
| Protocol translation | Strong | Limited | Limited |
| Best for | Legacy integration | API exposure | Domain decoupling |

## Governance

### Architecture Review Board (ARB)

**Composition**: Chief/Lead Architect (chair), domain architects (2-4), senior engineers (2-3 rotating), security representative, operations representative. Total: 6-10 people. Larger boards become rubber stamps.

**Cadence**: Biweekly for active portfolio. Monthly for steady-state organizations.

**Decision rights**: The ARB approves or rejects architecture decisions that cross domain boundaries, introduce new technologies (Trial or Adopt ring), or have estimated cost above a defined threshold. Within-domain decisions belong to domain architects.

**Process**: Teams submit an Architecture Decision Record (ADR) at least 3 business days before the review. The ARB reviews, asks questions, and decides: approved, approved with conditions, or rejected with rationale.

### Fitness Functions

Automated checks that validate architecture characteristics over time. Examples:
- No service may have more than 3 synchronous downstream dependencies (coupling)
- P99 latency for any API must stay under 500ms (performance)
- No cyclic dependencies between bounded contexts (modularity)
- All data stores must be encrypted at rest (security)

Implement as CI pipeline checks, monitoring alerts, or periodic audits. The point is making architecture constraints executable rather than aspirational.

### Architecture Principles Documentation

Each principle needs: name, statement (one sentence), rationale (why this matters), implications (what this means for teams), and exceptions (when this does not apply). Keep to 8-12 principles. More becomes noise.

Example: "Prefer managed services over self-hosted" -- Rationale: reduces operational burden and lets teams focus on business logic. Implication: teams must justify self-hosted infrastructure with a cost/control analysis. Exception: regulated workloads where data residency requires infrastructure control.

## Strategic Alignment

### Business Strategy to Technology Decisions

Chain: Business Strategy (grow market X, reduce cost Y) -> Business Capabilities needed -> Capability gaps -> Technology investments to close gaps.

Every technology investment should trace back to a capability gap that traces back to a strategic objective. If it cannot, it is infrastructure maintenance (valid, but fund differently) or pet project (eliminate).

### Heat Mapping for Prioritization

Create a matrix: rows are capabilities, columns are assessment dimensions (strategic importance, current maturity, competitive differentiation, risk exposure). Color-code red/amber/green. Capabilities that are red on importance and red on maturity are the top investment priorities.

## Standards Documentation Template

```
# Architecture Standard: [Name]

## Classification
- Category: [Infrastructure / Application / Data / Security / Integration]
- Status: [Draft / Active / Deprecated]
- Effective Date: [YYYY-MM-DD]
- Review Date: [YYYY-MM-DD]
- Owner: [Role/Team]

## Standard Statement
[One paragraph: what must be done and why.]

## Scope
[What systems, teams, or domains this applies to.]

## Requirements
[Numbered list of specific, testable requirements.]

## Approved Technologies
[List of technologies that satisfy this standard, with version constraints.]

## Exceptions Process
[How to request an exception, who approves, and documentation required.]

## Compliance Verification
[How adherence is checked: automated tests, audits, reviews.]
```
