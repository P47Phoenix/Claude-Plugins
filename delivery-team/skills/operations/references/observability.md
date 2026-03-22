# Observability

## Three Pillars

### Logs

**Structured logging** -- Emit logs as structured data (JSON), not free-form text. Every log entry includes a consistent set of fields.

Required fields:
- `timestamp` -- ISO 8601 format with timezone
- `level` -- ERROR, WARN, INFO, DEBUG (standardized across services)
- `service` -- Name of the emitting service
- `message` -- Human-readable description
- `correlation_id` / `trace_id` -- Links this log to the broader request context

Guidelines:
- Log at the right level: ERROR for failures requiring attention, WARN for degraded but functional, INFO for business events, DEBUG for developer diagnostics
- Never log sensitive data (passwords, tokens, PII) -- redact or mask before emitting
- Include enough context to diagnose without needing to reproduce: request parameters, response codes, duration, affected entity IDs
- Set log retention policies per environment: production logs retained longer (30-90 days), dev/staging shorter (7-14 days)

### Metrics

**RED Method** (for request-driven services):
- **Rate** -- Requests per second
- **Errors** -- Failed requests per second (and error rate as percentage)
- **Duration** -- Distribution of request latency (p50, p95, p99)

**USE Method** (for infrastructure resources):
- **Utilization** -- Percentage of resource capacity being used
- **Saturation** -- Amount of work queued or waiting (queue depth, thread pool exhaustion)
- **Errors** -- Error events on the resource (disk errors, network packet drops)

Guidelines:
- Use histograms for latency, not averages -- averages hide tail latency problems
- Define metric naming conventions and enforce them (e.g., `service_operation_metric_unit`)
- Emit custom business metrics alongside technical metrics (orders processed, user sign-ups, payment failures)
- Set metric retention: high-resolution (1s) for recent data (48 hours), downsampled for historical (90 days+)

### Traces

**Distributed tracing** connects a request's journey across multiple services into a single trace.

- Each service propagates trace context (trace ID, span ID, parent span ID) in request headers
- Every span records: service name, operation name, start time, duration, status code, and key attributes
- Instrument at service boundaries: incoming requests, outgoing HTTP calls, database queries, message queue operations
- Sample traces to control cost: 100% of errors, a configurable percentage of successful requests (1-10% is typical for high-volume services)
- Store traces for investigation: 7-14 days of retention is typical

**Span context propagation:**
- Use W3C Trace Context or B3 headers for inter-service propagation
- Ensure all services in the request path propagate context -- a single service that drops context breaks the trace
- Include trace ID in log entries for log-to-trace correlation

---

## SLI/SLO/SLA Definitions

### Service Level Indicators (SLIs)

Quantitative measurements of service behavior. Choose SLIs that reflect user experience.

| SLI Type | Measurement | Example |
|----------|-------------|---------|
| Availability | Successful requests / total requests | 99.95% of requests return non-5xx responses |
| Latency | Request duration at a percentile | p99 latency under 300ms |
| Error rate | Error responses / total responses | Less than 0.1% of requests return errors |
| Throughput | Successful operations per unit time | Process at least 1000 events/second |
| Freshness | Time since last successful data update | Data is no more than 5 minutes stale |

### Service Level Objectives (SLOs)

Target values for SLIs over a rolling time window. SLOs define the boundary between acceptable and unacceptable service.

- Define SLOs per critical user journey, not per microservice
- Use rolling windows (28 days or 30 days) rather than calendar months
- Express SLOs as a percentage over the window: "99.9% of requests complete in under 500ms over a 30-day rolling window"
- Calculate error budgets: if SLO is 99.9%, the error budget is 0.1% (43.2 minutes of downtime per 30 days)
- When error budget is exhausted, prioritize reliability work over feature work

### Service Level Agreements (SLAs)

Contractual commitments to external customers. SLAs are always less aggressive than internal SLOs.

- SLA = SLO minus a safety margin (e.g., internal SLO of 99.95%, external SLA of 99.9%)
- SLAs have financial or contractual consequences for violations (credits, penalties)
- Do not set SLAs without first establishing and measuring SLOs -- you cannot promise what you do not measure

---

## Alerting Philosophy

### Symptom-Based, Not Cause-Based

Alert on symptoms users experience, not on internal causes.

- **Good:** "Error rate exceeded 1% for 5 minutes" (symptom: users see errors)
- **Bad:** "Pod restarted" (cause: may or may not affect users)
- **Good:** "p99 latency exceeded 2 seconds for 10 minutes" (symptom: users experience slowness)
- **Bad:** "CPU utilization at 80%" (cause: may be normal for this workload)

### Severity Levels

| Severity | Definition | Response | Notification |
|----------|------------|----------|-------------|
| **SEV1 / Critical** | Service down or major degradation affecting most users | Immediate page, all hands on deck | PagerDuty/on-call page, war room |
| **SEV2 / Major** | Significant degradation affecting a subset of users | Respond within 15 minutes | Page on-call engineer |
| **SEV3 / Minor** | Minor degradation, workaround available | Respond within business hours | Slack/email notification |
| **SEV4 / Low** | Cosmetic or minor issue, no user impact | Address in next sprint | Ticket creation |

### Escalation

- Define escalation paths before incidents happen -- not during
- Primary on-call has 15 minutes to acknowledge before escalating to secondary
- If primary and secondary do not respond, escalate to engineering manager
- SEV1 incidents automatically escalate to senior leadership after 30 minutes

### Alert Fatigue Prevention

- Every alert must have a runbook linked in the alert metadata
- If an alert fires and requires no action, it should not be an alert -- make it a dashboard metric
- Review alert volume weekly: more than 2 pages per on-call shift that do not require action indicates alert noise
- Suppress known-transient alerts during maintenance windows
- Consolidate related alerts: 10 pod restarts should be one alert, not 10

---

## Dashboard Design

### Overview to Drill-Down

Structure dashboards in layers:

1. **Executive dashboard** -- Business health: revenue, user activity, error rates, SLO status. One screen. Green/yellow/red.
2. **Service dashboard** -- Per-service health: RED metrics, SLO burn rate, deployment markers. One per service.
3. **Investigation dashboard** -- Detailed metrics for debugging: per-endpoint latency, database query times, cache hit rates, queue depths. Used during incidents.

### Golden Signals Dashboard

Every service dashboard should display:

- **Latency** -- p50, p95, p99 request duration over time
- **Traffic** -- Requests per second over time
- **Errors** -- Error rate over time with breakdown by error type
- **Saturation** -- Resource utilization, queue depth, connection pool usage

### Dashboard Design Rules

- Every dashboard has a purpose statement: "Use this dashboard to [specific goal]"
- Graphs show time ranges that match the SLO window (30 days) with zoom capability
- Include deployment markers on time-series graphs to correlate changes with behavior shifts
- Use consistent color coding across all dashboards: green = healthy, yellow = warning, red = critical
- Do not put more than 12 panels on a single dashboard -- if more are needed, create a sub-dashboard

---

## Incident Classification

### Severity Assessment

| Factor | SEV1 | SEV2 | SEV3 | SEV4 |
|--------|------|------|------|------|
| User impact | Most/all users affected | Subset of users affected | Few users, workaround exists | No user impact |
| Revenue impact | Direct revenue loss | Potential revenue impact | Minimal financial impact | None |
| Data integrity | Data loss or corruption | Data delayed | Data cosmetically wrong | None |
| Duration | Ongoing or worsening | Stable but degraded | Intermittent | Not time-sensitive |

### Communication Cadence

| Severity | Internal Update | External Update |
|----------|----------------|-----------------|
| SEV1 | Every 15 minutes | Every 30 minutes via status page |
| SEV2 | Every 30 minutes | Every hour if customer-facing |
| SEV3 | At resolution | At resolution if reported by customer |
| SEV4 | In ticket | Not required |

---

## Postmortem Process

### Template

```
## Postmortem: [Incident Title]
## Date: [Date]
## Severity: [SEV level]
## Duration: [Start time - End time (total duration)]
## Author: [Name]

### Summary
[1-2 sentence description of what happened and impact]

### Impact
- Users affected: [number or percentage]
- Duration of impact: [time]
- Revenue impact: [if applicable]
- Data impact: [if applicable]

### Timeline
| Time (UTC) | Event |
|------------|-------|
| HH:MM | [First sign of issue] |
| HH:MM | [Alert fired / issue detected] |
| HH:MM | [Investigation started] |
| HH:MM | [Root cause identified] |
| HH:MM | [Fix deployed] |
| HH:MM | [Service restored] |
| HH:MM | [All-clear declared] |

### Root Cause
[Technical explanation of what caused the incident]

### Contributing Factors
- [Factor 1: what made the incident possible or worse]
- [Factor 2: what delayed detection or resolution]

### What Went Well
- [Things that worked as designed during the response]

### What Went Poorly
- [Things that did not work well during the response]

### Action Items
| Action | Owner | Priority | Due Date |
|--------|-------|----------|----------|
| [Preventive action] | [Name] | P1/P2/P3 | [Date] |

### Lessons Learned
[Key takeaways for the team and organization]
```

### Blameless Culture

- Focus on system failures, not individual mistakes
- Ask "what" and "how", not "who" -- "What allowed this to happen?" not "Who caused this?"
- Action items address systemic improvements (automation, guardrails, testing) not individual behavior
- Postmortem review is a learning exercise, not a blame assignment
- Share postmortems widely -- the value is in organizational learning

---

## On-Call Practices

### Rotation Design

- Minimum 2-person rotation: primary and secondary
- Rotation length: 1 week is typical; shorter rotations for high-volume services
- Follow-the-sun rotation for global teams -- no one should be on-call outside their working timezone if avoidable
- Compensate on-call duty: time off, stipend, or other compensation -- on-call is real work

### Runbook Access

- Every alert links to a runbook with diagnostic and resolution steps
- Runbooks are accessible from the alerting tool -- one click from alert to runbook
- Runbooks include escalation contacts and decision trees
- On-call engineers have all necessary access (dashboards, logs, deployment tools) before their rotation starts

### Escalation Paths

- Primary on-call: first responder, triage and initial investigation
- Secondary on-call: backup if primary is unavailable or needs help
- Subject matter expert: escalation for domain-specific issues
- Engineering manager: escalation for resource or communication decisions
- Define who can declare SEV1 and who leads the incident response

---

## Observability Anti-Patterns

- **Alert storms** -- A single failure triggers dozens of alerts because symptoms and causes all have independent alerts. Consolidate alerts and use dependency-aware alerting.
- **Dashboard overload** -- Dashboards with 50+ panels that no one can parse. Each dashboard should have a single purpose and fit on one screen.
- **Missing correlation** -- Logs, metrics, and traces exist but cannot be correlated. Include trace IDs in logs. Link metrics to traces. Without correlation, debugging is manual and slow.
- **Vanity metrics** -- Dashboards showing metrics that look good but do not reflect user experience. Focus on SLIs that map to user journeys.
- **Alert-and-forget** -- Alerts fire, get acknowledged, but no action is taken and no ticket is created. Every alert acknowledgment must result in either a fix or a ticket.
- **Monitoring only happy paths** -- Monitoring request success rate but not measuring error rates, timeout rates, or retry rates. Monitor failure modes explicitly.
- **No baseline** -- Alerting on absolute thresholds without knowing what normal looks like. Establish baselines from historical data before setting alert thresholds.
- **Observability as an afterthought** -- Adding monitoring after launch when problems appear. Instrument during development; observability is a feature, not a debugging tool.
