# Dependency & Risk Tracking Across Stories

## Purpose

Track inter-story dependencies and risks at the Plan stage to prevent blocked work, surface hidden ordering constraints, and maintain a living risk register throughout the pipeline.

---

## Dependency Notation

Use arrow notation to express ordering constraints between stories:

```
Story A -> Story B    (A must complete before B can start)
```

### Dependency Types

| Type | Symbol | Meaning | Example |
|------|--------|---------|---------|
| **Hard** | `->` | Blocking: B cannot start until A is DONE | "Auth API -> User Dashboard" (dashboard calls auth endpoints) |
| **Soft** | `~>` | Preferred ordering: B can start without A, but rework is likely | "Design system ~> Feature UI" (UI can use placeholders) |
| **External** | `=>` | Third-party or external team dependency | "Payment provider API => Checkout flow" |

### Notation Rules

- One dependency per line
- Use story IDs when available: `US-003 -> US-007`
- Chain dependencies: `US-001 -> US-003 -> US-005`
- Multiple predecessors: `US-001, US-002 -> US-005`
- Annotate with reason: `US-003 -> US-007  # shared data model`

---

## Dependency Graph Artifact

Store the dependency graph in `.delivery/artifacts/05a-dependencies.md` (Plan stage artifact).

### Format

```markdown
# Story Dependencies — Sprint [N] / Epic [Name]

## Dependency List

US-001 -> US-003        # Auth endpoints needed by profile page
US-001 -> US-004        # Auth endpoints needed by settings page
US-002 ~> US-005        # Design tokens preferred before UI build
US-006 => US-007        # Stripe webhook setup (external, ETA: [date])

## Critical Path

US-001 -> US-003 -> US-008 -> US-010

## External Dependencies

| ID | External Party | What We Need | ETA | Status | Escalation Contact |
|----|---------------|-------------|-----|--------|-------------------|
| EXT-01 | Stripe | Webhook endpoint provisioned | 2026-04-01 | Pending | payments-team@example.com |

## Orphan Stories (no dependencies)

US-009, US-011 — can be started in any order
```

---

## Risk Register

Maintain a risk register alongside the dependency graph. Each identified risk gets a unique ID and a designated owner responsible for mitigation.

### Risk Register Format

```markdown
# Risk Register — [Project / Sprint / Epic]

| Risk ID | Description | Likelihood | Impact | Severity | Mitigation | Owner | Status |
|---------|-------------|-----------|--------|----------|-----------|-------|--------|
| RISK-001 | External payment API may not be ready by sprint start | High | High | Critical | Implement mock API; design fallback flow | @backend-lead | Open |
| RISK-002 | New team member unfamiliar with auth module | Medium | Medium | Moderate | Pair programming on US-001; knowledge transfer session | @tech-lead | Mitigating |
| RISK-003 | Performance regression from new ORM queries | Low | High | Moderate | Add load test to US-008 acceptance criteria | @qa-lead | Open |
```

### Severity Matrix

| | Low Impact | Medium Impact | High Impact |
|---|-----------|--------------|-------------|
| **High Likelihood** | Moderate | High | Critical |
| **Medium Likelihood** | Low | Moderate | High |
| **Low Likelihood** | Informational | Low | Moderate |

### Risk Status Values

- **Open** — identified, not yet acted on
- **Mitigating** — mitigation actions in progress
- **Accepted** — risk acknowledged, no further action planned
- **Resolved** — risk no longer applies
- **Occurred** — risk materialized, handling in progress

---

## Pipeline Integration

### At Plan Stage (Stage 5)

1. **Product Owner** identifies story dependencies based on business logic and user flow ordering
2. **Architect** validates technical dependencies — adds hard dependencies where shared infrastructure, data models, or API contracts create ordering constraints
3. Pipeline generates `.delivery/artifacts/05a-dependencies.md` with the merged dependency list
4. **Critical path** is calculated: the longest chain of hard dependencies determines minimum elapsed time

### Dependency Validation During Development (Stage 6)

When a story is selected for development:

1. Check all hard predecessors (`->`) — if any are not DONE, warn:
   ```
   [DEPENDENCY WARNING] US-007 has unmet hard dependency: US-003 (status: IN_PROGRESS)
   Proceeding may cause rework. Continue anyway? [y/N]
   ```
2. Check soft predecessors (`~>`) — if any are not DONE, note:
   ```
   [DEPENDENCY NOTE] US-005 has unmet soft dependency: US-002 (status: NOT_STARTED)
   Preferred ordering suggests completing US-002 first to reduce rework.
   ```
3. Check external dependencies (`=>`) — if ETA has passed without resolution, escalate:
   ```
   [EXTERNAL DEPENDENCY OVERDUE] EXT-01 (Stripe webhook) — ETA was 2026-04-01, today is 2026-04-03
   Status: Pending | Escalation contact: payments-team@example.com
   ```

### At UAT Stage (Stage 7)

- Verify all hard dependencies in the critical path are DONE
- Flag any external dependencies that remain unresolved
- Include dependency completion status in the UAT summary

---

## Visualization

Dependencies are rendered as a text-based list (no graphing library required). For complex projects, the critical path is highlighted.

### Example Output

```
Dependency Graph (6 stories, 4 dependencies):

  US-001 (Auth API)
    -> US-003 (Profile Page)
    -> US-004 (Settings Page)
  US-002 (Design Tokens)
    ~> US-005 (Feature UI)
  US-006 (Stripe Setup)  [EXTERNAL]
    => US-007 (Checkout Flow)
  US-009 (About Page)          [no dependencies]
  US-011 (Error Pages)         [no dependencies]

Critical Path: US-001 -> US-003 (2 stories, estimated 8 points)
```

---

## Anti-Patterns

- **Circular dependencies**: A -> B -> A is invalid. If detected, escalate to architect to redesign the boundary.
- **Everything depends on everything**: If more than 60% of stories have hard dependencies, the epic may need re-decomposition.
- **Ignoring soft dependencies**: Treating all soft dependencies as hard inflates the critical path. Treating them all as optional increases rework risk. Use judgment.
- **Stale risk register**: Risks must be reviewed at each stage transition. A risk register that is never updated provides false confidence.
