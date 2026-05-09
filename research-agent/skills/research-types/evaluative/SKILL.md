---
name: research-types-evaluative
description: Evaluative research type sub-skill. Router-dispatched from research-agent parent on signals like "Did X work", "Impact", "Is X effective", "Worth it", "Evaluate", "Assess". Loads the Impact Assessment pattern (Pattern D) with PICO framework and risk-of-bias summary. Not directly model-invocable.
license: Apache License 2.0 - See repository LICENSE file
disable-model-invocation: true
tier: C
parent_skill: research-agent/SKILL.md
axis: research-types
variant: evaluative
allowed-tools: [Read, Edit, Write, Bash, Skill, ToolSearch]
---

# Evaluative Research Sub-Skill

Router-dispatched paradigm sub-skill for **Evaluative** research. Not directly model-invocable; the `research-agent` parent loads this sub-skill only when Phase 1 detection classifies the question as Evaluative.

## When This Sub-Skill Loads

The parent router dispatches here when the input question contains signals like:

- "Did X work" / "Was X effective"
- "What was the impact of X"
- "Is X worth it"
- "Evaluate X" / "Assess X"
- Post-launch retrospectives, ROI assessments, "should we keep using X"

**Disambiguation rule** (from `research-agent/references/research-type-patterns.md`):
"What is the current adoption of X" (mapping a fact) → Descriptive. "Was X adoption successful" (judging merit) → Evaluative.

## Framework Selection

| Framework | Use When |
|---|---|
| **PICO** | Default for Evaluative — intervention X is being judged against a comparison C on outcome O |
| **PECO** | Population was exposed to X (not actively choosing); evaluating the resulting effect |
| **None** | Single-option pre-post evaluation with no comparison group available |

PICO is the canonical Evaluative framework. SPICE applies only when the evaluation is qualitative/experiential rather than outcome-based.

## Output Pattern: Impact Assessment

Use this pattern verbatim for the Findings section (parent skill's Phase 6 Synthesis output):

```
## Research Type: Evaluative
## Framework: PICO

P: [Population/context]
I: [Intervention/subject being evaluated]
C: [Comparison baseline]
O: [Outcomes measured]

## Inclusion/Exclusion Criteria
Include: [...]
Exclude: [...]
Date range: [from] to [to]

## Evidence Summary Table
| ID | Source | Design | Scope | Outcome Direction | GRADE |
|----|--------|--------|-------|-------------------|-------|
| S1 | ...    | ...    | ...   | + / - / neutral   | ⊕⊕⊕◯  |

## Outcome Synthesis
- Positive outcomes: [count / proportion of sources]
- Negative / neutral outcomes: [count / proportion]
- Heterogeneity: [Are results consistent or conflicting? Why?]

## Risk of Bias Summary
| Source | Selection | Performance | Detection | Attrition |
|--------|-----------|-------------|-----------|-----------|
| S1     | Low       | ...         | ...       | ...       |

## Verdict
[Conclusion with overall GRADE level and caveats]
```

## Phase Adaptations

The parent skill's 8-phase flow applies. Evaluative-specific notes:

- **Phase 3 (Scope)**: Inclusion/Exclusion criteria MUST be defined **before** Phase 5 gathering. Post-hoc criteria are bias-prone.
- **Phase 4 (Source Plan)**: Default depth = "Standard" (8-15 sources). Evaluative claims require multiple independent outcome reports — single-source verdicts are not deliverable.
- **Phase 5 (Gather)**: For each source, classify the outcome direction (positive / negative / neutral) at extraction time, not at synthesis time.
- **Phase 6 (Synthesis)**: Heterogeneity analysis is mandatory — when sources disagree, explain *why* (different population, different outcome measure, different time horizon).
- **Phase 7 (Bias)**: **Publication bias** is the highest risk for Evaluative work — successful interventions get published, failures often do not. Counter by deliberately searching for negative results and grey literature on failures.

## Risk of Bias Categories

The Risk of Bias Summary table evaluates each source on four dimensions (per Cochrane methodology):

| Category | Question |
|---|---|
| **Selection** | Was the population selected without bias toward outcome? |
| **Performance** | Was the intervention applied uniformly across the population? |
| **Detection** | Were outcomes measured without bias toward expected results? |
| **Attrition** | Did dropout/incomplete data systematically favor one outcome? |

Rate each as **Low / Moderate / High / Unclear**. Sources with multiple High ratings carry less weight in the verdict.

## Integrity Constraints (Evaluative-Specific)

- **Comparison baseline mandatory.** Evaluative output without an explicit C in PICO is incomplete. If no comparison exists, the work is Descriptive (state of X), not Evaluative (was X good).
- **Heterogeneity must be explained.** Conflicting outcome directions are not averaged away — the synthesis explicitly states why sources disagree.
- **Verdict cites GRADE.** Every verdict line includes the overall confidence level and the caveats that justify it. "X works" without a GRADE is unsupportable.
- **Negative-result hunt.** The Phase 4 source plan must include a deliberate negative-result search. A balanced evidence base is the entry condition for a defensible verdict.

## References

- Parent: `research-agent/SKILL.md` (Phase 1-8 flow, GRADE system, integrity constraints)
- `research-agent/references/research-type-patterns.md` § "Evaluative" - identification matrix, disambiguation rules
- `research-agent/references/systematic-review.md` - escalate to full systematic protocol when N sources > 15 or stakes are high (regulated/safety-critical claims)
- `research-agent/references/api-research.md` - applies when evaluating an API/SDK (Evaluative on a technology choice)
