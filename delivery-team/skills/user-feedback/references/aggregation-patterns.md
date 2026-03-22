# Feedback Aggregation Patterns

How to synthesize feedback from multiple personas into an actionable report.

---

## Aggregation Process

After all persona agents produce independent feedback:

### Step 1: Collect

Gather all persona feedback into a single view. Each persona's feedback is independent -- they haven't seen each other's responses.

### Step 2: Theme Extraction

Group feedback items across personas by theme:
- **Usability**: navigation confusion, unclear labels, wrong hierarchy
- **Accessibility**: missing accommodations, color-only indicators, keyboard gaps
- **Missing Features**: things personas expected but didn't find
- **Confusion Points**: where personas got stuck or misunderstood
- **Performance**: speed, responsiveness, resource usage concerns
- **Delight**: things personas genuinely liked (important to preserve)

### Step 3: Consensus Detection

| Persona Count | Priority | Label |
|--------------|----------|-------|
| 4+ personas flag same issue | CRITICAL | Universal problem -- affects most users |
| 3 personas | HIGH | Widespread -- likely affects majority |
| 2 personas | MEDIUM | Notable -- affects a segment |
| 1 persona | LOW | Segment-specific -- may still matter |

**Exception**: Any issue from an accessibility persona is automatically MEDIUM or higher, even if only flagged by one persona. Accessibility is non-negotiable.

### Step 4: Conflict Detection

When personas disagree on the same element:

**Example**: Power User Pat wants keyboard shortcuts exposed; First-Timer Fran finds the interface overwhelming.

**Resolution approach**:
- Document the tension explicitly -- don't average or pick sides
- Recommend: progressive disclosure, configurable views, beginner/advanced modes
- If conflict is fundamental (can't satisfy both): note which persona is in the primary target audience and weight accordingly
- Never hide the conflict -- design tensions are valuable product decisions

### Step 5: Weighting

Not all personas carry equal weight:

| Weight | Persona Type | Rationale |
|--------|-------------|-----------|
| **1.5x** | Primary target audience | These are who we're building for |
| **1.5x** | Accessibility personas | Accessibility is non-negotiable |
| **1.2x** | Custom/project-specific personas | Tailored to this project's needs |
| **1.0x** | Built-in library personas | Generic, useful but less specific |
| **0.8x** | Demographic overlays only | Perspective without domain depth |

Weight affects priority ranking in the final report. A HIGH issue from a 1.5x persona ranks above a HIGH from a 1.0x persona.

### Step 6: Report Generation

Produce the aggregated report (see SKILL.md output contract):

```markdown
## User Feedback Report: [Product/Feature]
**Stage**: [which pipeline stage]
**Personas consulted**: [count]
**Date**: [date]

### Executive Summary
[3-5 sentences: overall sentiment, top concerns, biggest wins]

### Satisfaction Scores
| Persona | Category | Rating | Key Concern |
|---------|----------|--------|-------------|
[sorted by rating, lowest first]

### Consensus Issues (2+ personas)
| Priority | Issue | Personas | Recommendation |
|----------|-------|----------|----------------|
[sorted by priority: CRITICAL -> HIGH -> MEDIUM]

### Design Tensions
| Element | Perspective A | Perspective B | Recommendation |
|---------|--------------|---------------|----------------|

### Per-Persona Detail
[Full feedback from each persona -- see feedback-protocols.md]

### Recommendations (Prioritized)
1. [CRITICAL] [Actionable recommendation]
2. [HIGH] [Actionable recommendation]
...

### What to Preserve
[Things personas liked -- don't break these in future iterations]
```

---

## When Aggregation Flags Issues for Escalation

Automatically escalate to human if:
- Average satisfaction < 2.5/5 across all personas
- Any CRITICAL consensus issue with no clear fix
- 3+ deal-breakers identified across personas
- Accessibility persona gives satisfaction 1/5
- All personas say "would not recommend"

Escalation format follows the delivery-flow dynamic escalation protocol.

---

## Cross-Stage Trend Analysis

When persona feedback runs at multiple stages (2, 3, 6, 7), track improvement:

| Issue | Stage 2 | Stage 3 | Stage 6 | Stage 7 |
|-------|---------|---------|---------|---------|
| Navigation confusion | Flagged | Partially addressed | Fixed | -- |
| Missing keyboard shortcuts | -- | Flagged | Flagged | Still open |

This shows which issues were addressed during development and which persisted to UAT.
