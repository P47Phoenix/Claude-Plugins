---
name: research-types-explanatory
description: Explanatory research type sub-skill. Router-dispatched from research-agent parent on signals like "Why", "Root cause", "Caused by", "What led to", "Explain why". Loads the Causal Analysis pattern (Pattern C) with 5 Whys, Fishbone, and PECO framework. Not directly model-invocable.
license: Apache License 2.0 - See repository LICENSE file
disable-model-invocation: true
tier: C
parent_skill: research-agent/SKILL.md
axis: research-types
variant: explanatory
allowed-tools: [Read, Edit, Write, Bash, Skill, ToolSearch]
---

# Explanatory Research Sub-Skill

Router-dispatched paradigm sub-skill for **Explanatory** research. Not directly model-invocable; the `research-agent` parent loads this sub-skill only when Phase 1 detection classifies the question as Explanatory.

## When This Sub-Skill Loads

The parent router dispatches here when the input question contains signals like:

- "Why does X happen"
- "Root cause of X"
- "What caused X" / "What led to X"
- "Explain why" / "Because"
- Post-incident investigations, defect investigations, "RCA on X"

## Framework Selection

| Framework | Use When |
|---|---|
| **PECO** | Population is exposed (not actively choosing) and effect is measured ("why did the population exposed to dependency X experience outcome Y") |
| **None** | Direct causal investigation; use 5 Whys + Fishbone instead of a formal framework |

PICO is rare for Explanatory — Explanatory looks backward at why something happened; PICO looks forward at whether an intervention works.

## Output Pattern: Causal Analysis

Use this pattern verbatim for the Findings section (parent skill's Phase 6 Synthesis output):

```
## Research Type: Explanatory
## Framework: [PECO / None]

## Symptom Definition
[Precise statement of observed effect - what, when, where, severity]

## 5 Whys Chain
Why 1: [Symptom] -> Because [Cause 1] [S1]
Why 2: [Cause 1] -> Because [Cause 2] [S2]
Why 3: [Cause 2] -> Because [Cause 3] [S3]
Why 4: [Cause 3] -> Because [Cause 4]
Why 5: [Cause 4] -> Because [Root Cause]

## Fishbone Categories (Ishikawa)
| Category | Contributing Factors |
|----------|---------------------|
| People | [...] |
| Process | [...] |
| Technology | [...] |
| Environment | [...] |
| Data/Materials | [...] |

## Hypothesis Evidence Map
| Hypothesis | Supporting [Sx] | Opposing [Sx] | GRADE |
|------------|-----------------|---------------|-------|
| H1: [...]  | [S1], [S3]      | [S2]          | ⊕⊕⊕◯  |

## Most Probable Root Cause
[State with GRADE level]

## Counterfactual Test
[What would we expect if this cause were removed? Does evidence support that?]

## Validation Required
[What experiment or observation would confirm the root cause?]
```

## Phase Adaptations

The parent skill's 8-phase flow applies. Explanatory-specific notes:

- **Phase 3 (Scope)**: Symptom definition is the entry condition — precise what/when/where/severity statement required before Phase 4.
- **Phase 4 (Source Plan)**: Prioritize Primary sources tied to the incident (logs, code, telemetry, post-incident write-ups). Secondary sources used only for analogous cases.
- **Phase 5 (Gather)**: Drive each ReAct cycle toward a specific hypothesis confirmation or rejection. Avoid the "everything could be the cause" trap.
- **Phase 6 (Synthesis)**: 5 Whys is a discipline, not a checkbox — every step must cite evidence. Steps without `[Sx]` citations are invalid.
- **Phase 7 (Bias)**: Watch especially for **confirmation bias** — root-cause investigations naturally seek confirming evidence for the first plausible hypothesis. Counter by requiring opposing evidence in the Hypothesis Evidence Map.

## Integrity Constraints (Explanatory-Specific)

- **Correlation is not causation.** This is the cardinal rule. Every causal claim must include either an explicit causal mechanism or a `[INFERENCE]` label.
- **Counterfactual test is mandatory.** A root cause without a counterfactual ("if we removed X, the symptom would not occur because...") is a hypothesis, not a finding.
- **Validation step required.** Every Explanatory output ends with `Validation Required` — what experiment would confirm? Closed-loop validation distinguishes RCA from speculation.
- **Multiple-hypothesis discipline.** Do not collapse to a single root cause prematurely. The Hypothesis Evidence Map MUST list at least 2 alternatives unless a single-hypothesis is provably exhaustive.

## References

- Parent: `research-agent/SKILL.md` (Phase 1-8 flow, GRADE system, integrity constraints)
- `research-agent/references/research-type-patterns.md` § "Explanatory" - identification matrix, disambiguation rules
- `research-agent/references/systematic-review.md` § "Risk of bias" - bias categories that contaminate causal investigations
