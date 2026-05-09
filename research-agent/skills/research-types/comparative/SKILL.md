---
name: research-types-comparative
description: Comparative research type sub-skill. Router-dispatched from research-agent parent on signals like "Compare", "Which is better", "Alternatives", "Options", "vs.", "Trade-offs", "Choose between". Loads the Decision Matrix pattern (Pattern E) with weighted criteria, SWOT, and Qualitative Comparative Analysis. Not directly model-invocable.
license: Apache License 2.0 - See repository LICENSE file
disable-model-invocation: true
tier: C
parent_skill: research-agent/SKILL.md
axis: research-types
variant: comparative
allowed-tools: [Read, Edit, Write, Bash, Skill, ToolSearch]
---

# Comparative Research Sub-Skill

Router-dispatched paradigm sub-skill for **Comparative** research. Not directly model-invocable; the `research-agent` parent loads this sub-skill only when Phase 1 detection classifies the question as Comparative.

## When This Sub-Skill Loads

The parent router dispatches here when the input question contains signals like:

- "Compare X and Y"
- "Which is better"
- "Alternatives to X"
- "Options for X"
- "X vs. Y"
- "Trade-offs between"
- "Choose between"

**Disambiguation rule** (from `research-agent/references/research-type-patterns.md`):
"Compare X to understand Y" where understanding Y is the goal → **Exploratory**, not Comparative. Comparison is a method, not the purpose. Only route to Comparative when the user is choosing between identifiable options.

## Framework Selection

| Framework | Use When |
|---|---|
| **PICO** | Comparing interventions on a measurable outcome (e.g., "Redis vs Memcached for session storage on latency") |
| **None** | Multi-criteria comparison with no single dominant outcome; use Decision Matrix with weighted criteria |

SPICE applies if the comparison is experiential ("from the perspective of senior engineers, async vs sync code review"). PECO is rare — exposure-comparison maps better to Evaluative.

## Output Pattern: Decision Matrix

Use this pattern verbatim for the Findings section (parent skill's Phase 6 Synthesis output):

```
## Research Type: Comparative
## Framework: [None / PICO]

## Options Being Compared
[A], [B], [C]

## Evaluation Criteria (defined before gathering)
| Criterion | Weight | Rationale |
|-----------|--------|-----------|
| ...       | x%     | ...       |

## Decision Matrix
| Criterion | Weight | Option A | Option B | Option C | Evidence [citations] |
|-----------|--------|----------|----------|----------|----------------------|
| ...       | x%     | [score]  | [score]  | [score]  | [S1], [S2]           |

## Dimension Deep-Dives
[For each high-weight criterion: detailed comparison with supporting evidence]

## SWOT per Option (when strategic context applies)
**Option A:** Strengths / Weaknesses / Opportunities / Threats

## Qualitative Comparative Analysis
Necessary conditions for success: [...]
Sufficient conditions for success: [...]

## Recommendation
**Recommended:** [Option X]
**Rationale:** [Why this best fits stated needs - with citations]
**Risk trade-offs:** [What is given up]
**Conditions where this changes:** [Edge cases that favor a different option]
```

## Phase Adaptations

The parent skill's 8-phase flow applies. Comparative-specific notes:

- **Phase 3 (Scope)**: Evaluation criteria + weights MUST be defined **before** Phase 5 gathering. Post-hoc criteria selection lets the data choose the winner — that is bias, not analysis.
- **Phase 4 (Source Plan)**: Source mix must be **balanced across options** — N sources for Option A and 2 sources for Option B is a stacked deck. State source-count parity in the plan.
- **Phase 5 (Gather)**: For each option, gather evidence for the SAME criteria. Asymmetric criteria coverage invalidates the Decision Matrix.
- **Phase 6 (Synthesis)**: Recommendation must include "Conditions where this changes" — a recommendation that holds in all conditions either covers a trivial choice or hides important constraints.
- **Phase 7 (Bias)**: Watch especially for **researcher bias** — Comparative work often starts with a preferred option, and weights/criteria can be unconsciously tuned to favor it. Counter by stating a prior in Phase 1 ("I expect X will win because...") and checking the matrix against the prior.

## Decision Matrix Discipline

Scoring scale (use one and state which):

| Scale | Use When |
|---|---|
| 1-5 ordinal | Subjective criteria (e.g., DX, ergonomics) |
| 0-10 cardinal | Quantitative criteria with measured values normalized to 0-10 |
| Pass/Fail | Hard constraints (e.g., "GDPR-compliant: yes/no") |

Weighted score formula: `total = Σ (criterion_weight × option_score)`. Weights MUST sum to 100% (or 1.0). Sort options by total score; the highest is the recommendation candidate (subject to dimension deep-dives confirming no critical-criterion fail).

## Integrity Constraints (Comparative-Specific)

- **Criteria-before-gathering rule.** Defining criteria after gathering allows confirmation bias to drive criterion selection. Phase 3 outputs the criteria; Phase 5 gathers against them.
- **Balanced source mix mandatory.** Source-count parity per option is the entry condition for a defensible Decision Matrix.
- **Hard constraints come first.** A Pass/Fail criterion that any option fails eliminates that option before scoring — do not weight a fatal flaw.
- **Recommendation includes conditions.** Every Comparative output ends with "Conditions where this changes" — the audience needs to know when to revisit the decision.
- **Single-source dependency flag.** When a key criterion score rests on a single source for one option, flag `[Single-source dependency - seek corroboration]` per parent integrity constraint #3.

## References

- Parent: `research-agent/SKILL.md` (Phase 1-8 flow, GRADE system, integrity constraints)
- `research-agent/references/research-type-patterns.md` § "Comparative" - identification matrix, disambiguation rules
- `research-agent/references/api-research.md` - applies when comparing APIs/SDKs (Comparative on a technology choice)
- `research-agent/references/systematic-review.md` - escalate when N>15 sources or the comparison is regulated/safety-critical
