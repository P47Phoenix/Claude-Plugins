---
name: research-types-descriptive
description: Descriptive research type sub-skill. Router-dispatched from research-agent parent on signals like "What is", "What are", "Map", "Document", "Inventory", "Survey the field". Loads the Landscape Map pattern (Pattern B). Not directly model-invocable.
license: Apache License 2.0 - See repository LICENSE file
disable-model-invocation: true
tier: C
parent_skill: research-agent/SKILL.md
axis: research-types
variant: descriptive
allowed-tools: [Read, Edit, Write, Bash, Skill, ToolSearch]
---

# Descriptive Research Sub-Skill

Router-dispatched paradigm sub-skill for **Descriptive** research. Not directly model-invocable; the `research-agent` parent loads this sub-skill only when Phase 1 detection classifies the question as Descriptive.

## When This Sub-Skill Loads

The parent router dispatches here when the input question contains signals like:

- "What is the current state of X"
- "What exists in the X landscape"
- "Map / Document / Inventory / Survey / Catalogue"
- "List the available X"
- Field-survey or technology-landscape requests where the goal is to *describe what exists*

**Disambiguation rule** (from `research-agent/references/research-type-patterns.md`):
"What is the current adoption of X" (mapping a fact) → Descriptive. "Was X adoption successful" (judging merit) → Evaluative.

## Framework Selection

| Framework | Use When |
|---|---|
| **SPICE** | Context-specific landscape ("what is the state of testing tools in mobile-first teams") |
| **None** | Open-domain inventory or survey; no perspective filter needed |

PICO/PECO are not used for Descriptive work — there is no intervention or exposure being evaluated; the goal is enumeration.

## Output Pattern: Landscape Map

Use this pattern verbatim for the Findings section (parent skill's Phase 6 Synthesis output):

```
## Research Type: Descriptive
## Framework: [None / SPICE]

## Domain Boundaries
[Clear definition of what is and is not in scope]

## Entity Inventory
| Entity | Type | Key Properties | Source |
|--------|------|----------------|--------|
| ...    | ...  | ...            | [S1]   |

## Relationship Map
[Describe connections between entities - who uses what, what depends on what]

## State of the Field (as of [date])
- Mature / established: [...]
- Emerging: [...]
- Deprecated / declining: [...]

## Gaps in Documentation
[What exists but is undocumented, or documented inconsistently]
```

## Phase Adaptations

The parent skill's 8-phase flow applies. Descriptive-specific notes:

- **Phase 3 (Scope)**: Date range MUST be stated explicitly — "current state" is meaningless without a temporal anchor. Use "as of YYYY-MM-DD".
- **Phase 4 (Source Plan)**: Prioritize Primary sources (official docs, vendor pages, registries, standards). Secondary sources acceptable for cross-validation; Grey literature only for community-state signals (e.g., adoption surveys).
- **Phase 5 (Gather)**: Drive toward **inventory completeness**, not depth per item. Each entity gets a row; deep analysis belongs to Evaluative or Comparative follow-ups.
- **Phase 6 (Synthesis)**: The Entity Inventory is the deliverable. Avoid editorializing on what is "best" — that crosses into Evaluative.
- **Phase 7 (Bias)**: Watch for **selection bias** in entity inclusion (only well-known entities make the inventory). Counter by including a "long tail" or "lesser-known" section.

## Integrity Constraints (Descriptive-Specific)

- **No ranking or judgement.** Descriptive output describes what exists, not what is good. Comparative language ("X is better than Y") belongs in Comparative pattern.
- **Temporal anchor mandatory.** Every Descriptive output states "as of [date]" prominently. Field state changes; an undated landscape is misleading.
- **Inventory completeness over depth.** A Descriptive output that deeply covers 3 entities and ignores 12 others is mis-scoped — escalate to Evaluative or Comparative if depth is the user's goal.

## References

- Parent: `research-agent/SKILL.md` (Phase 1-8 flow, GRADE system, integrity constraints)
- `research-agent/references/research-type-patterns.md` § "Descriptive" - identification matrix, disambiguation rules
- `research-agent/references/api-research.md` - applies when the inventory includes APIs/SDKs (Descriptive landscape of an API surface)
