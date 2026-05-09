# Step 1: Assemble (PO)

**Begin**: `[1/6] Assembling presentation outline... (type: {detected type}, audience: {audience mode})`

Spawn a sub-agent with `delivery-team:product-delivery` (Product Owner role). Provide:
- User request (type, audience, format)
- Config context from `.delivery/config.yml`
- Pipeline state from `.delivery/state/` (if exists)

The PO produces a **Presentation Outline**:

| Column | Content |
|--------|---------|
| # | Slide number |
| Slide Title | Descriptive title |
| Content Owner | Role(s) responsible |
| Source Artifacts | File paths to read |

**Narrative adaptation**: The PO checks for problem signals in source data:
- Completion <80%: lead with "what we learned"
- Unresolved defects >5: quality slide before metrics
- Missed sprint goal: reframe around adjusted scope + rationale

Show adaptation status to user. User can say "no adaptation" to override.

Present outline to user. Wait for approval before proceeding.

**Complete**: `Outline approved: {N} slides, {M} roles contributing`
