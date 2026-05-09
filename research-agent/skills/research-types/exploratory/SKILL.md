---
name: research-types-exploratory
description: Exploratory research type sub-skill. Router-dispatched from research-agent parent on signals like "How does", "How can", "How might", "explore", "discover", "what factors". Loads the Discovery Report pattern (Pattern A) and SPICE framework guidance. Not directly model-invocable.
license: Apache License 2.0 - See repository LICENSE file
disable-model-invocation: true
tier: C
parent_skill: research-agent/SKILL.md
axis: research-types
variant: exploratory
allowed-tools: [Read, Edit, Write, Bash, Skill, ToolSearch]
---

# Exploratory Research Sub-Skill

Router-dispatched paradigm sub-skill for **Exploratory** research. Not directly model-invocable; the `research-agent` parent loads this sub-skill only when Phase 1 detection classifies the question as Exploratory.

## When This Sub-Skill Loads

The parent router dispatches here when the input question contains signals like:

- "How does X work / arise / unfold"
- "How can / How might"
- "Explore", "Discover", "Investigate the space of"
- "What factors influence / shape"
- Domain-mapping requests where the goal is *understanding*, not choosing

**Disambiguation rule** (from `research-agent/references/research-type-patterns.md`):
"Compare X to understand Y" where understanding Y is the goal → Exploratory (not Comparative). Comparison is a method here, not the purpose.

## Framework Selection

| Framework | Use When |
|---|---|
| **SPICE** | Lived-experience or context-bound exploration ("how do users in setting X experience Y") |
| **None** | Open-ended early-stage exploration; decompose into 3-5 sub-questions instead |

PICO and PECO are **not** typical for Exploratory work — both presuppose a defined intervention or exposure with a measurable outcome, which Exploratory research has not yet established.

## Output Pattern: Discovery Report

Use this pattern verbatim for the Findings section (parent skill's Phase 6 Synthesis output):

```
## Research Type: Exploratory
## Framework: [None / SPICE]

## Domain Boundaries
[What is in scope vs. out of scope for this exploration]

## Emerging Themes

Theme 1: [Name]
- Evidence: [S1], [S3]
- Frequency: [how often this theme appears across sources]
- Connections: [related to Theme 2 via ...]

Theme 2: [Name]
...

## Conceptual Relationships
[How themes connect - describe the emerging model]

## Theoretical Saturation Check
[Are additional sources still revealing new themes, or has saturation been reached?]

## Preliminary Model (Provisional)
[Draft conceptual model from discovered themes - explicitly labeled as provisional]

## Open Questions Generated
[What this exploration reveals we do NOT yet know]
```

## Phase Adaptations

The parent skill's 8-phase flow applies. Exploratory-specific notes:

- **Phase 3 (Scope)**: Default depth = "Standard" (8-15 sources). Surface scans risk premature theme closure.
- **Phase 4 (Source Plan)**: Bias source mix toward Primary + Secondary; Grey literature acceptable for emerging-trend signals but flag with `[Grey literature - signal only]`.
- **Phase 5 (Gather)**: Run ReAct cycles until **theoretical saturation** — when 2+ consecutive sources reveal no new themes, stop. Document saturation explicitly in the Discovery Report.
- **Phase 6 (Synthesis)**: Resist forcing a final model. Provisional models are the deliverable; certainty is out of scope for Exploratory.
- **Phase 7 (Bias)**: Watch especially for **availability bias** — exploration over-weights easy-to-find sources. Counter by deliberately seeking less-indexed sources in Phase 4 plan.

## Integrity Constraints (Exploratory-Specific)

- **No premature theme closure.** If a theme has only 1-2 supporting sources, label it `[EMERGING THEME - needs corroboration]` rather than promoting to a stable theme.
- **No causal claims.** Exploratory research surfaces phenomena; it does not explain them. Causal language belongs in Explanatory pattern.
- **Saturation check is mandatory.** The Discovery Report is incomplete without an explicit saturation statement.

## References

- Parent: `research-agent/SKILL.md` (Phase 1-8 flow, GRADE system, integrity constraints)
- `research-agent/references/research-type-patterns.md` § "Exploratory" - identification matrix, disambiguation rules
- `research-agent/references/systematic-review.md` - escalation path when Standard depth surfaces a question requiring full systematic protocol
