# Backlog Management

Refinement process, grooming cadence, backlog health metrics, and ordering principles.

---

## Backlog Levels

Healthy backlogs have three tiers, each at a different level of detail:

| Level | Horizon | Detail Level | Owner |
|-------|---------|--------------|-------|
| **Strategic (Epics)** | 3–12 months | Outcome + rough sizing | PO + Leadership |
| **Tactical (Ready Stories)** | 1–4 sprints | Full story + ACs + sized | PO + Team |
| **Sprint (Committed)** | Current sprint | Assigned + in progress | Dev Team |

The "ready buffer" (tactical tier) should contain 2–3 sprints of refined stories at all times. If the buffer drops below 1 sprint, the team risks not having enough work for the next planning session.

---

## Refinement (Grooming) Process

### Cadence
- **Weekly refinement session:** 1 hour per sprint (10% of sprint capacity rule)
- **Pre-sprint refinement:** Ensure top-of-backlog stories are fully Ready before sprint planning
- **Async refinement:** PO adds ACs and context before sessions; team reviews async

### Refinement Session Flow

1. **PO presents story context** (5 min): What problem does this solve? Who is affected?
2. **Team asks clarifying questions** (10 min): Identify ambiguities in ACs
3. **ACs reviewed and tightened** (10 min): Ensure each is testable
4. **Dependencies called out** (5 min): Block or note dependencies
5. **Team estimates** (10 min): Planning poker or T-shirt sizing
6. **Ready check** (5 min): Run DoR checklist; mark Ready or flag blockers

### Who Attends Refinement
- Product Owner (required — owns the story)
- Dev team (required — estimates and flags technical concerns)
- QA (required — validates ACs are testable)
- Designer (as needed — if UX decisions are open)
- Tech lead (as needed — for architectural concerns)

---

## Backlog Ordering Principles

Backlog ordering is a PO decision. These principles guide it:

1. **Value density first** — highest value per unit of effort rises to the top
2. **Dependencies drive sequencing** — story B that unblocks 3 others is more urgent than its standalone value suggests
3. **Risk reduction** — high-uncertainty items often belong earlier to reduce downstream unknowns
4. **Cost of delay** — items with deadlines or market windows are time-sensitive regardless of size
5. **Team skill and availability** — if a specialist is available now but not later, their stories move up
6. **Quick wins** — small, high-value items can be interspersed to maintain team momentum

**Anti-patterns to avoid:**
- "Oldest item first" — age is not value
- Prioritizing by who asked loudest — RICE/WSJF protects against stakeholder pressure
- Never revisiting priority — backlogs decay; reassess at least each sprint

---

## Backlog Health Metrics

Use these to identify and address backlog problems proactively:

| Metric | Healthy Range | Warning Sign | Action |
|--------|-------------|-------------|--------|
| **Ready buffer** | 2–3 sprints | < 1 sprint | Emergency refinement session |
| **Story age (top 20%)** | < 4 sprints | > 8 sprints | Review and kill or commit aging items |
| **Average story size** | 3–5 points | > 8 average | Too little splitting; many stories need decomposition |
| **% stories Ready** | > 30% of backlog | < 10% | Not enough refinement happening |
| **Stories without ACs** | < 5% | > 20% | PO bandwidth issue; stories are being added without definition |
| **Blocked story count** | 0 in active work | > 2 at once | Dependencies unresolved; escalate |

### Backlog Grooming Signals

**Backlog needs purging when:**
- Stories have been in the backlog for > 2 quarters without movement
- The product direction has shifted and old stories no longer align
- Stories are smaller than 1 point (tasks masquerading as stories)
- Duplicate stories exist from different stakeholders

**Action:** Archive or delete stale items. A clean backlog is a manageable backlog.

---

## Sprint Velocity and Capacity Planning

### Velocity
- **Definition:** Average story points completed per sprint over the last 3–5 sprints
- **Use:** Input to sprint commitment — do not commit more than velocity
- **Warning:** Velocity is a team metric, not a productivity target; do not use to compare teams

### Capacity Calculation

```
Available capacity = Total sprint days × Team size
- Sprint ceremonies: Planning (2–4 hrs) + Review (1–2 hrs) + Retro (1–2 hrs) + Refinement (1 hr/person)
- PTO and holidays
- Support rotation (if applicable)

Effective capacity = Available capacity × 0.8 (20% buffer for interruptions)
```

### Sustainable Pace
- Commitment should be achievable without overtime
- If the team regularly completes > 110% of committed points, commitment is too conservative
- If < 70%, investigate: too-large stories, unplanned work, or blocker patterns

---

## Epic Lifecycle

| Stage | Definition | PO Action |
|-------|-----------|-----------|
| **Idea** | Problem articulated, no details | Write problem statement; validate with users |
| **Defined** | Success metrics and scope clear | Break into features; rough sizing |
| **Ready** | First sprint of stories is Ready | Begin sprint planning with first stories |
| **In Progress** | At least one story shipped | Track metrics; adjust scope based on learnings |
| **Done** | Success metrics achieved | Retro; measure against original metrics |
| **Cancelled** | Strategy change or invalidated | Document reason; archive stories |
