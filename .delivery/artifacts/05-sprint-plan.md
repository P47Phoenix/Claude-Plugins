# Sprint Plan -- Issues #41 and #42: Pipeline Guardrail Gaps

**Type**: BUG_FIX | **Light Mode** | **Scrum Bag**: Aragorn
**Date**: 2026-03-25

**Sprint Goal**: Close the two guardrail gaps that let the pipeline silently degrade -- treating light as skip, and shipping without dogfooding.

---

## Story 1: Light Stages MUST Execute (#41)

**As a** delivery-flow orchestrator,
**I want** an explicit guardrail that forbids treating light-depth stages as skipped,
**So that** every routed stage produces an artifact, even at reduced depth.

### Acceptance Criteria

**AC-1: Guardrails section states the rule**

- Given the Guardrails section of `delivery-team/skills/delivery-flow/SKILL.md`
- When an orchestrator reads the guardrails
- Then there is a bullet stating: light stages MUST execute -- light means reduced depth, NOT skip. A light stage still produces an artifact, runs the primary agent, and passes blocking DoD criteria.

**AC-2: Depth Definitions section reinforces the distinction**

- Given the Depth Definitions section of `delivery-team/skills/delivery-flow/SKILL.md`
- When an orchestrator reads the Light definition
- Then the definition explicitly states that light stages execute and produce artifacts, and cross-references the guardrail to prevent conflation with skip.

### Test Cases

| ID | Scenario | Verification | Expected |
|----|----------|--------------|----------|
| T1 | Read Guardrails section | Search for "light" in Guardrails | Explicit statement that light != skip, with enforcement language ("MUST execute") |
| T2 | Read Depth Definitions | Compare Light vs Skip entries | Light says "executes" and "produces artifacts"; Skip says "does not execute". No ambiguity between them |
| T3 | Stage routing for BUG_FIX Plan stage | Check routing matrix row for BUG_FIX, Stage 5 | Marked "light" -- orchestrator must run it, not skip it |

### Implementation Approach

Two edits to `delivery-team/skills/delivery-flow/SKILL.md`:

1. **Guardrails section**: Add a new bullet after "No skipping DoD" that reads: *"Light stages MUST execute. Light depth means reduced ceremony (primary agent only, blocking criteria only) -- it does NOT mean skip. Every light stage produces an artifact and passes DoD validation. Treating light as skip is a pipeline violation."*

2. **Depth Definitions section**: Amend the Light bullet to add: *"Light stages always execute and always produce an artifact. Do not conflate light with skip."*

No other files touched.

---

## Story 2: Dogfooding Criterion in Gate 7 UAT (#42)

**As a** QA Engineer validating a pipeline change,
**I want** Gate 7 to require dogfooding as a blocking criterion,
**So that** changes to hooks, config, skills, and pipeline logic are validated by actual use before they ship.

### Acceptance Criteria

**AC-1: Gate 7 has a blocking dogfooding criterion**

- Given the Gate 7 criteria in `delivery-team/skills/delivery-flow/references/quality-gates.md`
- When a QA Engineer evaluates the gate
- Then there is a blocking criterion requiring that changes are validated by using them as an end user would, not solely by code review.

**AC-2: The criterion specifies what dogfooding means by change type**

- Given the dogfooding criterion in Gate 7
- When a team member reads it
- Then it specifies:
  - **Hooks**: trigger the hook in a real scenario and verify behavior
  - **Config changes**: run a pipeline with the new config and confirm it applies
  - **Skill changes**: invoke the skill and confirm instructions produce correct behavior
  - **Pipeline logic changes**: run at least one stage through the modified pipeline and verify output

### Test Cases

| ID | Scenario | Verification | Expected |
|----|----------|--------------|----------|
| T1 | Read Gate 7 criteria | Search for "dogfood" in quality-gates.md | Blocking criterion present with [blocking] tag |
| T2 | Hook change ships without dogfooding | Evaluate against Gate 7 | Fails -- dogfooding criterion not met |
| T3 | Config change validated only by code review | Evaluate against Gate 7 | Fails -- code review alone does not satisfy the criterion |
| T4 | Skill change tested by invoking the skill | Evaluate against Gate 7 | Passes -- skill was used as an end user would |

### Implementation Approach

One edit to `delivery-team/skills/delivery-flow/references/quality-gates.md`:

Add a new blocking criterion to Gate 7 after the "All defects found during UAT logged" line:

```
- [ ] Dogfooding completed: changes to hooks, config, skills, or pipeline logic
  have been validated by using them as an end user would -- not solely by code
  review. Hooks must be triggered in a real scenario; config changes must be
  applied in a pipeline run; skill changes must be invoked and output verified;
  pipeline logic changes must execute at least one stage end-to-end [blocking]
```

No other files touched.

---

## Commitment Summary

| Story | Points | Risk |
|-------|--------|------|
| #41 Light != Skip guardrail | 1 | Low -- two targeted text edits |
| #42 Dogfooding gate criterion | 1 | Low -- one targeted text edit |

Two stories, two total points. Well under capacity. Both are documentation-level changes with no code risk.

---

*The road is long, but these fences are short to build and will keep us from wandering off the path again.*
