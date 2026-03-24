# ADR Lifecycle Management

## Overview

Architecture Decision Records (ADRs) follow a structured lifecycle from proposal through acceptance, deprecation, or supersession. This reference defines statuses, transitions, cross-referencing, staleness detection, and the review protocol.

---

## ADR Location and Numbering

- **Location**: `.delivery/artifacts/04a-adrs/`
- **Numbering**: Sequential, zero-padded to three digits: ADR-001, ADR-002, ADR-003, etc.
- **Never reuse numbers.** If ADR-005 is deprecated, the next ADR is still ADR-006.
- **File naming**: `ADR-NNN-kebab-case-title.md` (e.g., `ADR-003-use-event-sourcing.md`)

---

## ADR Statuses

| Status | Meaning |
|--------|---------|
| **Proposed** | Under consideration. Open for discussion and review. Not yet binding. |
| **Accepted** | Approved and binding. The team follows this decision unless it is superseded or deprecated. |
| **Deprecated** | No longer relevant due to changed circumstances (e.g., technology sunset, feature removed). The decision was once valid but no longer applies. |
| **Superseded** | Replaced by a newer ADR. The superseding ADR explicitly references this one. |

---

## Status Transitions

| From | To | Who Can Trigger | When / Trigger |
|------|----|-----------------|----------------|
| Proposed | Accepted | Architect + at least one stakeholder listed in Deciders | After review, trade-off analysis complete, no unresolved objections |
| Proposed | Deprecated | Architect or Product Owner | Decision is no longer needed (e.g., feature cancelled before acceptance) |
| Accepted | Deprecated | Architect or Product Owner | Circumstances changed: technology sunset, feature removed, requirements shifted |
| Accepted | Superseded | Architect (must create the superseding ADR first) | A new decision contradicts or replaces this one |
| Deprecated | (terminal) | -- | Deprecated ADRs are not reactivated; create a new ADR instead |
| Superseded | (terminal) | -- | Superseded ADRs are not reactivated; the superseding ADR is the active decision |

**Rules:**
- Every transition must record the date and reason in the ADR body.
- Transitions from Accepted require notification to all original Deciders.
- Proposed ADRs that remain Proposed for more than 14 days should be escalated for a decision.

---

## Cross-Referencing

When a new ADR contradicts or replaces an existing one:

1. **New ADR** must include a `Supersedes:` field linking to the old ADR by number.
2. **Old ADR** must be updated to status `Superseded` with a `Superseded by:` field linking to the new ADR.
3. Both links are bidirectional so either ADR can be used to find the other.

### Cross-Reference Format

In the superseding ADR:
```
**Supersedes:** ADR-003 (Use Event Sourcing)
```

In the superseded ADR:
```
**Status:** Superseded
**Superseded by:** ADR-007 (Switch to CQRS Without Event Sourcing)
```

When an ADR is related to (but does not supersede) another ADR, use a `Related:` field:
```
**Related:** ADR-002, ADR-005
```

---

## ADR Template

```markdown
## ADR-[NNN]: [Decision Title]

**Status:** Proposed | Accepted | Deprecated | Superseded
**Date:** [YYYY-MM-DD]
**Deciders:** [who was involved in the decision]
**Supersedes:** [ADR-NNN (optional)]
**Superseded by:** [ADR-NNN (optional)]
**Related:** [ADR-NNN, ADR-NNN (optional)]
**Review by:** [YYYY-MM-DD -- date when this ADR should be reviewed for staleness]

### Context
[What is the issue? What forces are at play?]

### Decision
[What is the change that we're proposing and/or doing?]

### Consequences
[What becomes easier? What becomes harder?]

### Alternatives Considered
| Alternative | Pros | Cons | Why Rejected |
|-------------|------|------|--------------|
```

---

## Staleness Detection

ADRs can become stale when the context that drove the decision has shifted.

- **Default threshold**: 6 months from the `Date` field (or from last status change).
- **Configurable**: Set `architecture.adr_staleness_months` in `.delivery/config.md` to override.
- **Review-by date**: Each ADR includes a `Review by:` date. If set, this takes precedence over the threshold.
- **Detection**: The `adr review` command checks all Accepted ADRs against the threshold and flags those due for review.

### What "Stale" Means

A stale ADR is not automatically deprecated. It means:
1. The decision should be re-evaluated against current context.
2. If still valid, update the `Review by:` date to push the next review forward.
3. If no longer valid, transition to Deprecated or create a superseding ADR.

---

## Review Command: `adr review`

The `adr review` command produces a summary of all ADRs with actionable status.

### Process

1. Scan `.delivery/artifacts/04a-adrs/` for all ADR files.
2. Parse each ADR's frontmatter: status, date, review-by date, supersedes/superseded-by links.
3. Calculate age from the `Date` field.
4. Flag staleness: compare age or review-by date against threshold.
5. Validate cross-references: ensure all supersedes/superseded-by links are reciprocal.

### Output Format

```
## ADR Review Summary

| ADR | Title | Status | Age | Stale? | Action Needed |
|-----|-------|--------|-----|--------|---------------|
| ADR-001 | Use PostgreSQL | Accepted | 8 months | YES | Review: exceeds 6-month threshold |
| ADR-002 | REST over gRPC | Accepted | 3 months | No | -- |
| ADR-003 | Event Sourcing | Superseded | 11 months | -- | Superseded by ADR-007 |
| ADR-004 | Monorepo | Proposed | 18 days | -- | Proposed > 14 days: escalate for decision |

### Cross-Reference Issues
- [List any broken or non-reciprocal links]

### Recommendations
- [Specific actions: review ADR-001, decide on ADR-004, etc.]
```

---

## Memory Integration

ADRs are indexed in the delivery pipeline's self-learning memory system:

- **Index location**: `.delivery/memory/topics/team-decisions.md`
- **What is indexed**: ADR number, title, status, date, one-line summary of the decision.
- **When indexed**: After every status transition (Proposed, Accepted, Deprecated, Superseded).
- **Retrieval**: During pipeline stages (especially Stage 4: Architect), the orchestrator reads the team-decisions topic to surface prior ADRs relevant to the current task.
- **Format in index**:
  ```
  - ADR-001 (Accepted, 2025-09-15): Use PostgreSQL for all persistent storage
  - ADR-003 (Superseded, 2025-10-01): Use event sourcing for order service -> see ADR-007
  ```

This ensures that architecture decisions are available as context for future pipeline runs without loading all ADR files into context.
