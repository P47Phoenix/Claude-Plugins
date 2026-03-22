# Quality Attributes Reference

## ISO 25010 Quality Model

The ISO 25010 standard defines 8 product quality characteristics. Each has sub-characteristics that make it concrete and measurable.

| Characteristic | Sub-characteristics | Practical Description |
|---------------|--------------------|-----------------------|
| **Functional Suitability** | Completeness, Correctness, Appropriateness | Does it do what users need? Are calculations right? Are features appropriate for the task? |
| **Performance Efficiency** | Time behavior, Resource utilization, Capacity | Response times under load. CPU/memory consumption. Maximum throughput before degradation. |
| **Compatibility** | Co-existence, Interoperability | Can it run alongside other systems without interference? Can it exchange data with other systems? |
| **Usability** | Learnability, Operability, Error protection, Accessibility | How fast can new users become productive? How well does it prevent and recover from user errors? |
| **Reliability** | Maturity, Availability, Fault tolerance, Recoverability | How often does it fail? What percentage of time is it operational? How does it behave during failures? How fast does it recover? |
| **Security** | Confidentiality, Integrity, Non-repudiation, Accountability, Authenticity | Data protected from unauthorized access. Data not tampered with. Actions are traceable and attributable. |
| **Maintainability** | Modularity, Reusability, Analysability, Modifiability, Testability | How easy is it to understand, change, and test? Can components be reused? Can you diagnose problems? |
| **Portability** | Adaptability, Installability, Replaceability | Can it run in different environments? How easy is it to install? Can it replace another system? |

---

## Quality Attribute Scenario Format

A quality attribute scenario makes a vague requirement ("the system should be fast") into something testable and measurable.

**Structure:**

| Element | Description | Example |
|---------|-------------|---------|
| **Source** | Who or what generates the stimulus | End user, external system, attacker, scheduled job |
| **Stimulus** | The event or condition | Request arrives, component fails, code change needed |
| **Artifact** | What part of the system is affected | API endpoint, database, authentication module |
| **Environment** | Under what conditions | Normal operation, peak load, degraded mode, after deployment |
| **Response** | How the system should behave | Process the request, failover, reject invalid input |
| **Measure** | Quantified acceptance criteria | 95th percentile latency < 200ms, recovery within 30 seconds |

---

## Example Quality Attribute Scenarios

### Latency
**Source:** Customer. **Stimulus:** Submits a product search query. **Artifact:** Search API endpoint. **Environment:** Peak load (10x normal traffic during sale event). **Response:** Returns relevant results. **Measure:** 95th percentile response time under 300ms; 99th percentile under 800ms.

### Availability
**Source:** Internal monitoring. **Stimulus:** Primary database instance becomes unreachable. **Artifact:** Order processing service. **Environment:** Normal operation. **Response:** Traffic fails over to read replica; write operations are queued. **Measure:** No more than 10 seconds of degraded service; zero data loss; full recovery within 5 minutes.

### Security
**Source:** Unauthenticated external user. **Stimulus:** Attempts SQL injection via search input field. **Artifact:** Web application input handler. **Environment:** Normal operation. **Response:** Input is sanitized; malicious query is rejected; attempt is logged with source IP and payload. **Measure:** Zero successful injections; alert triggered within 60 seconds for repeated attempts from same source.

### Modifiability
**Source:** Development team. **Stimulus:** Business requests adding a new payment provider. **Artifact:** Payment processing module. **Environment:** Design time. **Response:** New provider is integrated by implementing an existing interface, with no changes to order processing logic. **Measure:** Integration completed and tested within 3 developer-days; no modifications to existing payment provider code.

### Scalability
**Source:** Marketing campaign. **Stimulus:** Traffic increases 20x over 15 minutes. **Artifact:** API tier and web application. **Environment:** Auto-scaling enabled, cloud deployment. **Response:** New instances provision automatically; load balancer distributes traffic. **Measure:** No requests dropped; latency SLA maintained throughout scale-up; scale-up completes within 3 minutes.

### Recoverability
**Source:** Operations team. **Stimulus:** Corrupt deployment causes service crash loop. **Artifact:** Production environment. **Environment:** Failed deployment. **Response:** Automated rollback to last known good version triggers. **Measure:** Rollback completes within 2 minutes; zero manual intervention required; all in-flight requests handled gracefully.

---

## Architecture Tradeoff Analysis Method (ATAM) -- Practical Steps

ATAM is a structured method for evaluating architecture against quality attribute requirements. Simplified for practical use:

**Step 1: Present the architecture.** Walk through the key architectural decisions, ideally using C4 Level 1 and Level 2 diagrams.

**Step 2: Identify quality attribute drivers.** List the top 5-8 quality attributes that matter most. Use the scenario format above. Prioritize ruthlessly -- you cannot optimize for everything.

**Step 3: Map decisions to quality attributes.** For each architectural decision, identify which quality attributes it supports and which it works against.

**Step 4: Identify sensitivity points.** A sensitivity point is an architectural element where a small change significantly affects a quality attribute. Example: the database connection pool size is a sensitivity point for both performance and availability.

**Step 5: Identify trade-off points.** A trade-off point is where an architectural decision affects two or more quality attributes in opposing directions. Example: adding encryption improves security but reduces performance.

**Step 6: Catalog risks.** Any trade-off or sensitivity point that is unresolved or has unacceptable consequences is a risk. Rank risks by impact and likelihood.

**Step 7: Decide and document.** For each risk, decide whether to accept, mitigate, or change the architecture. Record decisions as ADRs.

---

## Common Trade-off Pairs

| Trade-off | Guidance |
|-----------|----------|
| **Consistency vs. Availability** | CAP theorem is real in distributed systems. Strong consistency requires coordination (latency, reduced availability during partitions). If your business domain tolerates stale reads (product catalog, social feed), favor availability. If it requires correctness (financial transactions, inventory counts), favor consistency. |
| **Performance vs. Maintainability** | Optimized code is often harder to read and modify. Premature optimization creates maintenance debt. Optimize only after profiling identifies actual bottlenecks. Keep hot paths optimized and cold paths readable. |
| **Security vs. Usability** | Every security measure adds friction. MFA, CAPTCHAs, short session timeouts -- all improve security, all annoy users. Risk-based approaches help: require MFA for sensitive actions, not for browsing. Use adaptive authentication that escalates based on threat signals. |
| **Cost vs. Reliability** | Redundancy costs money. Multi-region deployments, hot standbys, and N+1 capacity all increase spend. Calculate the cost of downtime and compare. A 99.99% SLA costs dramatically more than 99.9%. Make sure the business actually needs (and will pay for) the extra nine. |
| **Flexibility vs. Complexity** | Every abstraction layer, plugin system, or configuration option adds complexity. Build for known requirements, not speculative ones. Prefer simple, replaceable components over complex, flexible ones. |

---

## Architectural Tactics by Quality Attribute

### Performance
| Tactic | Description | When to Apply |
|--------|-------------|---------------|
| **Caching** | Store computed results for reuse. Levels: in-process, distributed (Redis), CDN, browser. | Read-heavy workloads with cacheable responses. Define TTL and invalidation strategy upfront. |
| **Concurrency** | Process requests in parallel using thread pools, async I/O, or worker processes. | I/O-bound workloads (database queries, API calls). Measure thread pool sizing empirically. |
| **Resource pooling** | Reuse expensive resources (database connections, HTTP clients) across requests. | Any system making repeated connections to external resources. |
| **Lazy loading** | Defer computation or data loading until actually needed. | Large object graphs, expensive initializations, paginated data. |
| **Data partitioning** | Split data across shards to distribute load. | Single-node storage capacity or throughput is insufficient. High complexity cost. |

### Availability
| Tactic | Description | When to Apply |
|--------|-------------|---------------|
| **Redundancy** | Run multiple instances; no single point of failure. Active-active or active-passive. | Any production system with an availability SLA above 99%. |
| **Circuit breaker** | Stop calling a failing dependency; return fallback response. Prevents cascade failures. | Any synchronous call to an external service or database. |
| **Health checks** | Expose liveness and readiness endpoints for orchestrators to monitor. | Every deployable service. Readiness checks should verify downstream dependencies. |
| **Graceful degradation** | Serve reduced functionality when a subsystem is down. Show cached data, disable non-critical features. | User-facing systems where partial service is better than total outage. |
| **Bulkheads** | Isolate failures to a single component. Separate thread pools, separate processes, separate infrastructure. | When a failure in one subsystem must not take down others. |

### Security
| Tactic | Description | When to Apply |
|--------|-------------|---------------|
| **Authentication** | Verify identity. Tokens (JWT, OAuth2), certificates, API keys. | Every system boundary. Use established protocols, never roll your own. |
| **Authorization** | Enforce permissions. RBAC, ABAC, policy engines (OPA). | Every API endpoint and data access path. Default deny. |
| **Encryption** | Protect data in transit (TLS) and at rest (AES-256). | Always for transit. At rest for sensitive data (PII, financial, health). |
| **Audit logging** | Record who did what, when, from where. Immutable, tamper-evident. | Any action that modifies state, accesses sensitive data, or affects other users. |
| **Input validation** | Validate and sanitize all external input at the boundary. Allowlists over denylists. | Every input from users, external systems, files, message queues. |

### Modifiability
| Tactic | Description | When to Apply |
|--------|-------------|---------------|
| **Loose coupling** | Minimize dependencies between components. Communicate through interfaces, not implementations. | Always. This is a default architectural principle. |
| **High cohesion** | Group related functionality together. A module should have a single reason to change. | Always. If a module changes for multiple unrelated reasons, split it. |
| **Dependency injection** | Supply dependencies from outside rather than constructing them internally. | When components need to be testable, swappable, or configurable. |
| **Plugin architecture** | Define extension points where new behavior can be added without modifying existing code. | When the system needs to support third-party extensions or frequent feature additions to a stable core. |
| **API versioning** | Support multiple API versions simultaneously during transition periods. | Public APIs, APIs consumed by mobile apps (cannot force upgrades). |

### Scalability
| Tactic | Description | When to Apply |
|--------|-------------|---------------|
| **Horizontal scaling** | Add more instances rather than bigger instances. Requires stateless design. | When vertical scaling hits limits or cost efficiency favors commodity hardware. |
| **Partitioning/Sharding** | Distribute data and processing across multiple nodes by a partition key. | When a single node cannot handle the data volume or throughput. |
| **Async processing** | Move non-critical work to background queues. Respond immediately, process later. | Any operation where the user does not need to wait for completion (emails, reports, analytics). |
| **CQRS** | Separate read and write models. Scale reads independently with optimized projections. | Read-heavy systems where read and write patterns differ significantly. |
| **Edge computing / CDN** | Move computation and content closer to users. | Static content delivery, latency-sensitive global applications. |

---

## NFR Specification Template

| ID | Quality Attribute | Requirement | Target | Measurement Method | Priority |
|----|------------------|-------------|--------|-------------------|----------|
| NFR-001 | Performance | API response time for product search | p95 < 200ms under 1000 req/s | Load test with k6, measured at API gateway | Must have |
| NFR-002 | Availability | System uptime | 99.95% monthly (< 22 min downtime/month) | Synthetic monitoring (Datadog) | Must have |
| NFR-003 | Scalability | Handle traffic spikes | Auto-scale to 10x baseline within 5 min | Load test simulating spike pattern | Must have |
| NFR-004 | Security | Data encryption | All PII encrypted at rest (AES-256) and in transit (TLS 1.3) | Security audit, automated compliance scan | Must have |
| NFR-005 | Recoverability | Recovery from data center failure | RTO < 15 min, RPO < 1 min | Disaster recovery drill (quarterly) | Should have |
| NFR-006 | Modifiability | Add new payment provider | < 5 developer-days, no changes to existing providers | Measured during integration of most recent provider | Should have |

**Key terms:**
- **RTO (Recovery Time Objective):** Maximum acceptable downtime after a failure.
- **RPO (Recovery Point Objective):** Maximum acceptable data loss measured in time.
- **p95/p99:** The latency at the 95th/99th percentile of requests.

---

## Fitness Functions

A fitness function is an automated test that continuously validates an architectural quality attribute. The concept comes from evolutionary architecture -- architecture that supports guided, incremental change.

**How to make quality attributes testable:**

| Quality Attribute | Fitness Function | Tooling |
|------------------|-----------------|---------|
| Performance | Load test in CI that fails if p95 > threshold | k6, Gatling, Locust |
| Availability | Chaos engineering: kill instances, verify recovery | Chaos Monkey, Litmus, Gremlin |
| Security | Dependency vulnerability scan, SAST/DAST in pipeline | Snyk, Trivy, OWASP ZAP |
| Modifiability | ArchUnit/ArchGuard tests enforcing dependency rules | ArchUnit (Java), Dependency Cruiser (JS), pytestarch (Python) |
| Coupling | Measure afferent/efferent coupling per module; fail if above threshold | SonarQube, custom static analysis |
| API compatibility | Contract tests that verify backward compatibility | Pact, Schemathesis |
| Data integrity | Reconciliation jobs comparing source and projection data | Custom scripts, Great Expectations |

**Principles for effective fitness functions:**
- Run automatically, ideally in CI/CD pipeline
- Produce a clear pass/fail result with a quantified threshold
- Cover the quality attributes that matter most to your system
- Start with 2-3 critical fitness functions, not 20 aspirational ones
- Treat fitness function failures as build-breaking -- do not allow exceptions to accumulate
