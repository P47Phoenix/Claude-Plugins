# Technology Evaluation Reference

## Weighted Criteria Matrix Framework

A structured approach to comparing technology options that forces explicit trade-off decisions and reduces bias.

### Process

1. **Identify criteria**: List all factors that matter for the decision. Start broad, then consolidate to 8-12 criteria. More than 15 dilutes the analysis.
2. **Assign weights**: Each criterion gets a weight reflecting its relative importance. Weights must sum to 100%. Use stakeholder input -- different roles value different criteria. Resolve disagreements before scoring.
3. **Score candidates**: Rate each technology against each criterion on a 1-5 scale. Use evidence, not opinion. Document the rationale for each score.
4. **Calculate weighted totals**: For each candidate: sum(weight_i * score_i). The highest total is the recommendation, subject to interpretation.
5. **Sensitivity analysis**: Vary the weights of the top 2-3 criteria by +/- 10%. If the winner changes, the decision is sensitive to assumptions -- flag this.

### Weight Assignment Methods

**MoSCoW**: Classify criteria as Must-have, Should-have, Could-have, Won't-have. Must-haves become pass/fail gates (any candidate scoring 1 on a Must is eliminated). Remaining criteria get percentage weights.

**Pairwise comparison**: Compare every pair of criteria and ask "which matters more?" Tally wins per criterion. Normalize to percentages. Good for resolving disagreements in a group setting.

**Direct percentage**: Each stakeholder allocates 100 points across criteria. Average the allocations. Simple but prone to anchoring bias.

### Scoring Guidance

| Score | Meaning |
|-------|---------|
| 1 | Does not meet the criterion; significant gap |
| 2 | Partially meets; notable limitations |
| 3 | Adequately meets; some trade-offs |
| 4 | Strongly meets; minor gaps |
| 5 | Exceeds expectations; clear strength |

Require evidence for every score of 1 or 5. These extremes drive the outcome and must be defensible.

## Common Evaluation Dimensions

### Maturity and Stability

How long has the technology been in production use industry-wide? Is it past version 1.0? Is the API stable between releases? Check: release history, breaking changes between major versions, LTS (long-term support) availability. A 1.0 release last month is not the same as a 5-year-old project with quarterly releases.

### Community Size and Activity

Proxy for long-term viability and problem-solving resources. Metrics: GitHub stars (trend, not absolute), contributors (active vs total), Stack Overflow question volume and answer rate, conference talks and blog posts. Distinguish between hype-driven spikes and sustained organic growth.

### Performance Benchmarks

Only relevant benchmarks matter. A message broker's throughput at 1KB messages is irrelevant if your messages are 100KB. Run your own benchmarks against your access patterns. Published benchmarks are marketing material until proven otherwise. Test: throughput, latency (p50, p95, p99), resource consumption under load, behavior at saturation.

### Learning Curve

How long until a competent developer is productive? Factors: quality of getting-started documentation, similarity to technologies the team already knows, conceptual complexity (event sourcing has a steeper curve than CRUD), availability of training resources.

### Ecosystem

Libraries, tools, and integrations available. Check: ORM/driver support for your language, monitoring/observability integration (Prometheus, Datadog), CI/CD plugin availability, IDE support. A technology with a weak ecosystem will consume engineering time building glue code.

### Licensing Model

**Permissive** (MIT, Apache 2.0, BSD): Use freely, modify freely, minimal obligations. Preferred for most commercial use.

**Copyleft** (GPL, AGPL): Derivative works must use the same license. AGPL extends this to network use (SaaS). Legal review required before adoption.

**Commercial/Proprietary**: License fees, usage restrictions, vendor dependency. Evaluate total cost and exit cost.

**Source-available** (BSL, SSPL, Elastic License): Looks open source but restricts competitive use. Read the license carefully -- "open source" in marketing does not mean OSI-approved.

### Total Cost of Ownership

Include: license/subscription fees, infrastructure costs (compute, storage, network), engineering time for integration and maintenance, training costs, operational costs (monitoring, incident response), migration cost if replacing an existing system. Calculate over 3-5 years, not just year one.

### Vendor Health and Longevity

Is the vendor profitable or well-funded? What is the trajectory -- growing or declining? For open-source projects: is there a commercial backer? Is the project governed by a foundation (CNCF, Apache) or a single company? Single-company projects have higher abandonment risk.

### Security Track Record

Check: CVE history (count and severity), average time to patch disclosed vulnerabilities, security audit results (if public), whether the project has a security policy and responsible disclosure process.

### Documentation Quality

Evaluate: accuracy (does the documentation match the actual behavior?), completeness (are edge cases documented?), organization (can you find what you need?), examples (are they realistic or trivial?), API reference (auto-generated from code or hand-written?).

## Build vs Buy Decision Framework

### When to Build

- **Core differentiator**: The capability is central to your competitive advantage. Buying makes you identical to competitors.
- **Unique requirements**: Your needs diverge significantly from what available products offer. Customizing a product beyond 30% of its functionality is usually worse than building.
- **Control needed**: You need full control over the roadmap, SLAs, and implementation details. Regulated environments sometimes mandate this.

### When to Buy

- **Commodity capability**: Authentication, email delivery, payment processing. Building these from scratch is not a competitive advantage and introduces security risk.
- **Time-to-market**: You need the capability faster than you can build it. The product market exists because the problem is well-understood.
- **Maintenance burden**: Building means maintaining forever. A team of 4 engineers maintaining a custom solution is expensive compared to a SaaS subscription.

### Hidden Costs

**Build hidden costs**: Ongoing maintenance (budget 20% of initial build cost per year), knowledge concentration risk (what happens when the original builders leave?), security patching responsibility, feature requests from internal users becoming an internal product backlog.

**Buy hidden costs**: Integration engineering (APIs rarely do exactly what you need), vendor lock-in (switching cost grows over time), license cost escalation at renewal, customization limitations that force workarounds, data migration costs if you switch vendors.

### Hybrid Approaches

- **Build the orchestration, buy the components**: Build the workflow and business logic that differentiates you; use commercial/open-source components for commodity functions.
- **Start with buy, plan for build**: Use a purchased solution to validate the requirement, then build a custom replacement once requirements are proven and stable.
- **Open-source with commercial support**: Get the control of self-hosted with the safety net of vendor support.

## Proof of Concept Design

### What to Test

Test the riskiest assumptions first. A PoC that validates something you are already confident about is wasted effort. Identify the top 2-3 technical risks and design the PoC to answer them specifically.

Examples of valid PoC questions:
- "Can technology X sustain 10,000 concurrent connections with sub-100ms latency?"
- "Can we integrate technology X with our existing authentication system?"
- "Does the programming model of technology X work with our team's skill set?"

### Scope

- **Timeboxed**: 1-2 weeks maximum. If you cannot answer your question in that time, either the question is too broad or the technology is too complex for a PoC.
- **Minimal**: Build only what is needed to answer the question. No production-quality error handling, no CI/CD, no documentation.
- **Focused**: One PoC, one question. Do not combine "can it handle the load?" with "does the developer experience work?" into a single PoC.

### Success Criteria

Define before starting. Written down. Agreed upon by stakeholders. Examples:
- "P99 latency under 200ms at 5,000 req/sec sustained for 30 minutes."
- "Developer can implement a CRUD endpoint in under 2 hours without prior experience."
- "Data migration from system X completes within the 4-hour maintenance window."

### PoC Report Template

```
# PoC Report: [Technology] for [Use Case]

## Question
[What were we trying to answer?]

## Setup
[Environment, configuration, data volumes, and any relevant context.]

## Success Criteria
[What was defined as success before starting?]

## Results
[Measured outcomes against each success criterion. Include numbers.]

## Observations
[Unexpected findings, both positive and negative.]

## Recommendation
[Proceed / Do not proceed / Proceed with caveats]

## Next Steps
[If proceeding: what needs to happen before production use?]
```

## Technology Radar Integration

### Assessing Against Radar Rings

When evaluating a technology, determine its current ring position:
- Has anyone in the organization used it in production? (If no: Assess at best)
- Has it been used for more than 6 months without significant issues? (If yes: candidate for Trial -> Adopt)
- Have we encountered blocking problems? (If yes: candidate for Hold)

### Promotion and Demotion Triggers

**Assess to Trial**: Successful PoC, identified sponsor, defined pilot project scope.
**Trial to Adopt**: 6+ months in production, operational runbook exists, team can support it without the original sponsor, no critical issues.
**Any ring to Hold**: Security vulnerability with no fix timeline, vendor acquisition with uncertain roadmap, better alternative now available in Adopt ring, or critical production incidents traced to the technology.

## Migration Cost Estimation

### Cost Categories

| Category | What to Include |
|----------|----------------|
| Development | Code changes, new integrations, testing, refactoring |
| Testing | Regression testing, performance testing, security testing |
| Data migration | Schema conversion, data transformation, validation, rollback plan |
| Training | Team learning curve, documentation, workshops |
| Downtime | Revenue impact during cutover, customer communication |
| Risk | Contingency budget (15-25% of total estimate) |

### Common Underestimation Traps

- **Data migration**: Always takes 2-3x longer than expected. Edge cases in real data are invisible in schema analysis.
- **Integration testing**: Every system that integrates with the migrated component needs regression testing.
- **Dual-running costs**: During migration, you often run both old and new systems simultaneously. Budget for double infrastructure.
- **Knowledge transfer**: The team that built the old system and the team building the new system are often different people. Knowledge gaps cause rework.
- **Rollback planning**: A migration without a tested rollback plan is not ready. Rollback planning and testing is real work.

## Vendor Lock-in Assessment

### Portability Dimensions

**Data portability**: Can you export all your data in a standard format? Is there an API for bulk export? What format is the data in -- proprietary or standard (CSV, JSON, Parquet)?

**API portability**: Does the vendor use standard APIs (S3-compatible, SQL, OpenAPI) or proprietary interfaces? Can you swap the implementation behind an abstraction layer?

**Infrastructure portability**: Are you using vendor-specific services (Lambda, DynamoDB, Cloud Spanner) or portable technologies (Kubernetes, PostgreSQL, Kafka)? Can workloads move between clouds?

**Knowledge portability**: Are your team's skills specific to this vendor (Salesforce Apex, AWS CDK) or transferable (Python, SQL, Terraform)?

### Lock-in Severity Matrix

| Dimension | Low Lock-in | Medium Lock-in | High Lock-in |
|-----------|-------------|----------------|--------------|
| Data | Standard formats, easy export | Export possible with effort | No export API, proprietary format |
| API | Industry standard | Standard with proprietary extensions | Fully proprietary |
| Infrastructure | Portable (K8s, Postgres) | Cloud-specific but abstracted | Serverless/proprietary services |
| Knowledge | General skills | Vendor ecosystem skills | Proprietary language/tooling |

### Mitigation Strategies

- **Abstraction layers**: Wrap vendor-specific services behind interfaces. Trade-off: adds complexity and may limit access to vendor-specific features.
- **Standards compliance**: Prefer technologies that implement open standards (SQL, AMQP, OpenTelemetry, OCI containers).
- **Multi-cloud readiness**: Use portable infrastructure (Kubernetes, Terraform) for workloads where lock-in risk is unacceptable. Do not multi-cloud for its own sake -- it doubles operational complexity.
- **Contractual protections**: Negotiate data portability clauses, exit assistance, and price caps in vendor contracts.

## Complete Evaluation Example: Choosing a Message Broker

### Context

E-commerce platform needs asynchronous communication between order, inventory, and notification services. Requirements: at-least-once delivery, message ordering per customer, 5,000 messages/second peak, 3 consumer groups, messages retained for 7 days for replay.

### Criteria and Weights

| Criterion | Weight | Rationale |
|-----------|--------|-----------|
| Throughput at target load | 20% | Must handle peak volume |
| Message ordering guarantee | 15% | Business requirement |
| Operational complexity | 15% | Small ops team |
| Ecosystem and language support | 15% | Python and Go services |
| Message retention and replay | 10% | 7-day replay is a requirement |
| Cost (infrastructure) | 10% | Budget-constrained |
| Community and support | 10% | Long-term maintainability |
| Learning curve | 5% | Team has messaging experience |

### Scoring

| Criterion | Weight | Kafka | RabbitMQ | AWS SQS/SNS |
|-----------|--------|-------|----------|-------------|
| Throughput | 20% | 5 | 3 | 4 |
| Ordering | 15% | 4 (per-partition) | 3 (per-queue) | 3 (FIFO queues) |
| Ops complexity | 15% | 2 (ZooKeeper/KRaft) | 4 (simpler) | 5 (managed) |
| Ecosystem | 15% | 5 | 4 | 3 |
| Retention/replay | 10% | 5 (log-based) | 2 (not designed for) | 2 (limited) |
| Cost | 10% | 3 (self-hosted) | 4 (lighter infra) | 4 (pay-per-use) |
| Community | 10% | 5 | 4 | 3 (vendor docs) |
| Learning curve | 5% | 3 | 4 | 4 |

### Weighted Totals

- **Kafka**: (5x20)+(4x15)+(2x15)+(5x15)+(5x10)+(3x10)+(5x10)+(3x5) = 100+60+30+75+50+30+50+15 = **410**
- **RabbitMQ**: (3x20)+(3x15)+(4x15)+(4x15)+(2x10)+(4x10)+(4x10)+(4x5) = 60+45+60+60+20+40+40+20 = **345**
- **AWS SQS/SNS**: (4x20)+(3x15)+(5x15)+(3x15)+(2x10)+(4x10)+(3x10)+(4x5) = 80+45+75+45+20+40+30+20 = **355**

### Recommendation

Kafka scores highest, driven by throughput, retention/replay, and ecosystem strengths. The main risk is operational complexity (scored 2). Mitigation: use a managed Kafka service (Confluent Cloud, AWS MSK) to reduce ops burden, which would raise the ops score to 4 and strengthen the recommendation further.

### Sensitivity Check

If operational complexity weight increases from 15% to 25% (taking 10% from throughput): Kafka drops to 390, SQS/SNS rises to 375. Kafka still wins but the gap narrows, validating that managed Kafka is the right approach.
