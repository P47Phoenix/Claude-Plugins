# Runbook Templates

## Operational Runbook Structure

### Standard Template

```
# Runbook: [RUNBOOK-ID] [Title]

## Purpose
[One sentence: what operational scenario this runbook addresses]

## When to Use
- [Trigger condition 1: what alert, symptom, or request initiates this runbook]
- [Trigger condition 2: if applicable]

## Prerequisites
- [ ] Access to [system/tool/dashboard]
- [ ] Permissions: [specific role or access level required]
- [ ] Knowledge of: [concepts or systems the operator should understand]

## Procedure

### Step 1: [Action]
[Specific command or action]

**Expected output:** [What the operator should see]

**If this fails:** [What to do if the step does not produce expected results]

### Step 2: [Action]
[Continue with each step...]

## Verification
[How to confirm the issue is resolved]
- [ ] [Check 1: specific metric or state to verify]
- [ ] [Check 2: second verification point]

## Rollback
[If the procedure made changes that can be undone, document the rollback steps]

## Escalation
- If unresolved after [time]: Contact [person/team] via [channel]
- If data integrity is at risk: Immediately contact [person/team]

## Metadata
- **Owner:** [Team or individual]
- **Last reviewed:** [Date]
- **Last tested:** [Date]
- **Related alerts:** [Alert names or IDs that link to this runbook]
```

### Runbook Design Rules

- Every step must be copy-paste ready -- no ambiguity about what to type or click
- Include expected output after every step -- the operator needs to know if the step worked
- Include failure branches -- what to do when a step does not produce the expected result
- Write for the operator who has never seen this runbook before -- assume no tribal knowledge
- Keep runbooks focused on one scenario -- a runbook that tries to cover everything covers nothing

---

## Alerting-to-Runbook Mapping

### One Alert, One Runbook

- Every production alert must link to a runbook that describes how to respond
- The runbook ID is included in alert metadata so operators can find it immediately
- If an alert fires and has no runbook, that is a documentation gap -- track and resolve

### Alert Metadata Format

```
alert:
  name: "high-error-rate-api-gateway"
  severity: SEV2
  runbook: "RUNBOOK-042"
  runbook_url: "https://docs.internal/runbooks/RUNBOOK-042"
  description: "API gateway error rate exceeded 5% for 10 minutes"
```

### Mapping Table

Maintain a mapping table as a reference for operations teams:

| Alert Name | Severity | Runbook ID | Last Updated |
|------------|----------|------------|-------------|
| high-error-rate-api-gateway | SEV2 | RUNBOOK-042 | 2025-03-01 |
| database-connection-pool-exhaustion | SEV1 | RUNBOOK-015 | 2025-02-15 |
| disk-space-critical | SEV2 | RUNBOOK-008 | 2025-01-20 |

### Gap Detection

- Weekly automated report: alerts that fired in the past 7 days without a linked runbook
- New alerts cannot be deployed without a corresponding runbook (enforced in CI)
- Stale runbooks (not reviewed in 90 days) are flagged for review

---

## Troubleshooting Trees

### Decision Tree Format

Structure complex diagnostics as a decision tree where each node is a check and each branch leads to the next check or a resolution.

```
## Troubleshooting: Service Returning 500 Errors

START: Check the service logs for error messages
  |
  +--> Error: "connection refused to database"
  |      |
  |      +--> Check database connectivity
  |             |
  |             +--> Database is down --> Follow RUNBOOK-015 (Database Recovery)
  |             |
  |             +--> Database is up --> Check connection pool settings
  |                    |
  |                    +--> Pool exhausted --> Restart service to reset pool,
  |                    |                       then investigate connection leaks
  |                    |
  |                    +--> Pool available --> Check network security groups
  |
  +--> Error: "out of memory"
  |      |
  |      +--> Check memory utilization
  |             |
  |             +--> Above 90% --> Restart service, investigate memory leak
  |             |
  |             +--> Below 90% --> Check for memory limit misconfiguration
  |
  +--> No errors in logs
         |
         +--> Check upstream service health
                |
                +--> Upstream degraded --> Issue is upstream, follow
                |                         relevant upstream runbook
                |
                +--> Upstream healthy --> Escalate to service owner
```

### Tree Design Guidelines

- Start with the most common cause -- put the 80% case first
- Each node has a clear check with a pass/fail outcome
- Leaf nodes are either a resolution or an escalation
- Keep trees to 3-4 levels deep -- deeper trees indicate the problem is too complex for a single runbook
- Include time estimates for each branch so operators can plan

---

## Escalation Matrices

### Severity-Based Escalation

| Severity | First Responder | Escalation (15 min) | Escalation (30 min) | Escalation (60 min) |
|----------|----------------|---------------------|---------------------|---------------------|
| **SEV1** | On-call primary | On-call secondary + Engineering Manager | VP Engineering | CTO |
| **SEV2** | On-call primary | On-call secondary | Engineering Manager | -- |
| **SEV3** | On-call primary | Team lead (business hours) | -- | -- |
| **SEV4** | Ticket created | Team sprint backlog | -- | -- |

### On-Call Rotation Integration

- Escalation matrix references on-call roles, not specific people
- On-call rotation tool (PagerDuty, OpsGenie) maintains the current mapping of roles to people
- Runbooks reference the escalation role: "Escalate to on-call secondary" not "Escalate to Jane"
- Contact information is in the on-call tool, not in the runbook (prevents staleness)

### Who Can Declare Severity

| Action | Who Can Do It |
|--------|--------------|
| Declare SEV4 | Any engineer |
| Declare SEV3 | Any engineer |
| Declare SEV2 | On-call engineer or team lead |
| Declare SEV1 | On-call engineer, team lead, or engineering manager |
| Upgrade severity | Incident commander or engineering manager |
| Downgrade severity | Incident commander with documented justification |

---

## Recovery Procedures

### Step-by-Step with Verification

Every recovery procedure follows a pattern: act, verify, proceed.

```
## Recovery: Restore Service After Database Failover

### Step 1: Verify database failover is complete
Run: `db-admin status --cluster production`
Expected: Primary node shows as `[new-primary-host]`, status: AVAILABLE
If not: Wait 2 minutes and retry. If still not available after 3 retries,
        escalate to DBA on-call.

### Step 2: Update application connection strings
Run: `kubectl set env deployment/api-service DB_HOST=[new-primary-host]`
Expected: Deployment rollout begins. Verify with:
         `kubectl rollout status deployment/api-service`
If rollout fails: Check pod logs for connection errors.

### Step 3: Verify application health
Check: https://api.example.com/health
Expected: Status 200, all dependencies "healthy"
Monitor: Error rate dashboard for 15 minutes. Error rate should return to baseline.

### Step 4: Confirm resolution
- [ ] Database primary is healthy and accepting connections
- [ ] Application pods are running and passing health checks
- [ ] Error rate is at baseline
- [ ] Latency is at baseline
- [ ] No new alerts firing
```

### Recovery Completeness

Every recovery procedure must address:
1. **What to do** -- the specific actions
2. **How to verify** -- confirmation that each step worked
3. **What to do if it fails** -- failure branch at each step
4. **When to escalate** -- clear trigger for calling in more help
5. **How to confirm full recovery** -- not just "service is up" but "service is healthy"

---

## Incident Communication Templates

### Status Page Updates

```
## Investigating
[HH:MM UTC] We are investigating reports of [symptom]. Some users may
experience [specific impact]. We will provide an update within 30 minutes.

## Identified
[HH:MM UTC] We have identified the root cause of [symptom] and are
implementing a fix. [Specific impact] is ongoing. Next update in 30 minutes.

## Fix Deployed
[HH:MM UTC] A fix has been deployed for [symptom]. We are monitoring
to confirm the issue is resolved. Some users may continue to experience
[residual impact] for the next [time period].

## Resolved
[HH:MM UTC] The issue causing [symptom] has been resolved. All services
are operating normally. Total impact duration: [time]. We will publish
a postmortem within [timeframe].
```

### Stakeholder Email Template

```
Subject: [SEV level] Incident: [Brief description] - [Status]

Summary: [1-2 sentences describing the incident and current impact]

Timeline:
- [HH:MM]: Issue detected
- [HH:MM]: Response initiated
- [HH:MM]: [Current status or resolution]

Impact: [Who is affected and how]
Current Status: [Investigating | Mitigating | Resolved]
Next Update: [Time]

Contact: [Incident commander name and channel]
```

### War Room Setup

When a SEV1 is declared:
1. Create a dedicated incident channel (Slack/Teams): `#incident-YYYY-MM-DD-brief-description`
2. Pin the incident summary with: severity, impact, timeline, current status
3. Designate roles: incident commander, communications lead, technical lead
4. Update the pinned summary every 15 minutes
5. All troubleshooting discussion happens in this channel -- keep other channels clear
6. After resolution, archive the channel and link from the postmortem

---

## Runbook Testing and Maintenance

### Review Cadence

| Runbook Category | Review Frequency | Reviewer |
|-----------------|-----------------|----------|
| SEV1 response runbooks | Monthly | On-call team lead |
| SEV2 response runbooks | Quarterly | Service owner |
| Operational procedures | Every 6 months | Team lead |
| Onboarding runbooks | With each new hire | New hire + buddy |

### Game Days

- Schedule quarterly game days where the team practices runbook execution
- Simulate realistic failure scenarios in a staging or isolated environment
- Measure time to detection, time to response, and time to resolution
- Identify runbook gaps: steps that are unclear, missing, or incorrect
- Update runbooks immediately after game day findings

### Staleness Detection

- Track "last reviewed" and "last tested" dates for every runbook
- Automated alert when a runbook exceeds its review cadence
- Runbooks that have not been reviewed in 6 months are flagged as potentially stale
- Stale runbooks are reviewed or archived -- a stale runbook is worse than no runbook because it creates false confidence

### Automation from Runbooks

- If a runbook procedure is executed more than 3 times per month, evaluate for automation
- Start by scripting individual steps, then compose into automated runbooks
- Automated runbooks still need a human trigger and verification -- full automation requires high confidence
- Keep the manual runbook alongside the automated version -- automation can fail
- Track which runbooks have been automated and the success rate of automated execution
