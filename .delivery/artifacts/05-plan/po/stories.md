# Plan Stage — User Stories

**Pipeline**: run-2026-04-04-w7m3
**Project Type**: BUG_FIX
**Date**: 2026-04-04
**Author**: Product Owner (Gandalf)
**Issue**: #55

> "All we have to decide is what to build with the time that is given to us. And I decide we build the Prior Art Analysis step first — for the Architect has wandered from the path, proposing competing designs when the user's own map was already drawn."

---

## User Story: Mandatory Prior Art Analysis in Architect Skill

**As a** plugin developer who provides detailed specifications to the delivery pipeline
**I want** the Architect agent to perform a mandatory Prior Art Analysis of my provided specs before proposing any architecture
**So that** the Architect builds on my established design decisions instead of reimagining the solution from scratch, preserving my trust in the delivery pipeline

**Story Points:** 2 (markdown-only reference file changes — one tier below code)
**Priority:** P1 — Critical (trust issue: user-provided designs are being overridden)
**Issue:** #55

### Acceptance Criteria

**AC-01** — Prior Art Analysis step exists in architect skill *(structural)*

Given the architect skill SKILL.md and/or reference files in `delivery-team/skills/architect/`
When a reviewer inspects the architect skill instructions
Then a mandatory "Prior Art Analysis" step is documented that must execute before any design proposal work
And the step is positioned as the first action in the architect's workflow (before solution design)

**AC-02** — Prior Art Analysis requires spec summarization *(structural)*

Given the Prior Art Analysis step definition in the architect skill
When a reviewer inspects the step's instructions
Then the step requires the Architect to read and produce a written summary of all user-provided specifications before proceeding
And the summary must be included in the architect's output artifact

**AC-03** — Decisions-made vs. open-questions classification *(structural)*

Given the Prior Art Analysis step definition in the architect skill
When a reviewer inspects the step's instructions
Then the step requires the Architect to classify each element of the user-provided spec as either "decision already made" or "open question"
And the classification must be included in the architect's output artifact as a structured table or list

**AC-04** — Architect builds on existing design by default *(structural)*

Given the Prior Art Analysis step definition in the architect skill
When a reviewer inspects the step's instructions
Then the instructions explicitly state that the Architect must build architecture ON the existing design (validate feasibility, fill gaps, map to implementation)
And the instructions prohibit proposing alternative designs for elements classified as "decisions already made"

**AC-05** — Alternative proposals require documented technical blockers *(structural)*

Given the Prior Art Analysis step definition in the architect skill
When a reviewer inspects the step's instructions
Then the instructions state that the Architect may only propose alternatives to user decisions when clear, documented technical blockers exist
And the instructions require the Architect to document the specific technical blocker justifying each alternative proposal

**AC-06** — Backward compatibility with pipelines lacking user specs *(structural)*

Given the architect skill with the Prior Art Analysis step
When a pipeline runs without any user-provided specifications
Then the Prior Art Analysis step gracefully handles the absence (e.g., notes "no prior specs provided" and proceeds to normal design)
And existing pipeline behavior is not broken or degraded

**AC-07** — Dogfooding validation with user-provided spec scenario *(empirical)*

Given the updated architect skill deployed in this repository
When a delivery pipeline run includes a user-provided specification (e.g., a multi-agent system design)
Then the Architect agent executes the Prior Art Analysis step, produces a spec summary, classifies decisions vs. open questions, and builds on the existing design rather than proposing competing alternatives

### Test Cases

#### TC-01: Prior Art Analysis step presence (validates AC-01)

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Open the architect skill files in `delivery-team/skills/architect/` | Files are accessible |
| 2 | Search for "Prior Art Analysis" in SKILL.md and reference files | The step is documented with clear instructions |
| 3 | Verify the step is positioned before any design/solution proposal instructions | Prior Art Analysis appears before solution architecture steps |
| **Result** | **PASS if** the step exists and is ordered first in the architect workflow | |

#### TC-02: Spec summarization requirement (validates AC-02)

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Read the Prior Art Analysis step instructions | Instructions are present |
| 2 | Verify instructions require the Architect to read all user-provided specs | Explicit instruction to read user specs exists |
| 3 | Verify instructions require a written summary in the output artifact | Summary is a mandatory output, not optional |
| **Result** | **PASS if** summarization is a mandatory part of the step's instructions and output | |

#### TC-03: Decision classification requirement (validates AC-03)

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Read the Prior Art Analysis step instructions | Instructions are present |
| 2 | Verify instructions require classifying spec elements as "decision already made" or "open question" | Classification requirement exists with both categories named |
| 3 | Verify the classification must appear in the output artifact as a structured format | Structured table or list format is specified |
| **Result** | **PASS if** classification is mandatory and output format is specified | |

#### TC-04: Build-on-existing-design instruction (validates AC-04)

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Read the architect skill instructions following the Prior Art Analysis step | Instructions are present |
| 2 | Verify explicit language stating the Architect must build ON existing designs | Language such as "validate feasibility, fill gaps, map to implementation" exists |
| 3 | Verify explicit prohibition against proposing alternatives for settled decisions | Prohibition language exists for "decisions already made" elements |
| **Result** | **PASS if** both the positive instruction (build on) and negative instruction (do not override) are present | |

#### TC-05: Technical blocker requirement for alternatives (validates AC-05)

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Read the architect skill instructions for when alternatives are permitted | Instructions are present |
| 2 | Verify that proposing alternatives requires a documented technical blocker | Conditional language exists: alternatives only when blockers are documented |
| 3 | Verify the Architect must document the specific blocker for each alternative | Documentation requirement exists per-alternative, not just globally |
| **Result** | **PASS if** alternatives are gated behind documented technical blockers | |

#### TC-06: Backward compatibility — no user specs (validates AC-06)

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Read the Prior Art Analysis step instructions | Instructions are present |
| 2 | Verify instructions include a graceful fallback for when no user specs exist | Conditional handling exists (e.g., "if no prior specs, note absence and proceed") |
| 3 | Verify the fallback does not block or degrade the normal architect workflow | No mandatory failure or error when specs are absent |
| **Result** | **PASS if** the step handles missing specs gracefully without breaking existing flows | |

#### TC-07: Dogfooding — live pipeline run with user spec (validates AC-07)

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Run a delivery pipeline with a user-provided specification as input | Pipeline starts and reaches Architect stage |
| 2 | Observe the Architect agent's output artifact | Output includes a Prior Art Analysis section |
| 3 | Verify the output contains a spec summary | Summary of user-provided spec is present |
| 4 | Verify the output contains a decisions vs. open questions classification | Classification table/list is present with both categories |
| 5 | Verify the proposed architecture builds on the user's design, not competing with it | Architecture extends/validates the existing design; no competing alternatives for settled decisions |
| **Result** | **PASS if** all sub-steps pass — the Architect respects and builds on the user's spec | |

### AC Classification Summary

| AC | Type | Rationale |
|----|------|-----------|
| AC-01 | Structural | Verifiable by inspecting markdown files |
| AC-02 | Structural | Verifiable by inspecting markdown files |
| AC-03 | Structural | Verifiable by inspecting markdown files |
| AC-04 | Structural | Verifiable by inspecting markdown files |
| AC-05 | Structural | Verifiable by inspecting markdown files |
| AC-06 | Structural | Verifiable by inspecting markdown files |
| AC-07 | Empirical | Requires running the updated skill in a live pipeline |

### Definition of Ready Checklist

- [x] Story is understood by the team
- [x] Acceptance criteria are clear and testable
- [x] Dependencies identified (none — self-contained markdown changes)
- [x] Story is sized and fits within one sprint (2 SP — markdown-only)
- [x] No unresolved blockers

### INVEST Validation

| Criterion | Status | Notes |
|-----------|--------|-------|
| Independent | PASS | No dependencies on other stories; self-contained skill change |
| Negotiable | PASS | Exact wording/structure of Prior Art Analysis step is flexible |
| Valuable | PASS | Directly restores user trust by preventing design override |
| Estimable | PASS | Scoped to known files in `delivery-team/skills/architect/` |
| Small | PASS | 2 SP — markdown reference file edits only |
| Testable | PASS | 6 structural ACs verifiable by inspection + 1 empirical AC |

### Notes / Constraints

- **Scope boundary**: Changes are confined to `delivery-team/skills/architect/` (SKILL.md and/or reference files). No schema changes, no code changes, no new dependencies.
- **Backward compatibility**: Pipelines without user-provided specs must be unaffected. The Prior Art Analysis step must handle the absence gracefully.
- **Dogfooding required**: Per team convention, the fix must be validated by running the updated skill against a scenario with a user-provided spec before shipping (AC-07).
- **Sprint utilization**: At 2 SP for markdown-only changes, this fits well within the 80% velocity ceiling.
- **Issue tracking**: This story addresses GitHub Issue #55.

> "Do not propose where the road already leads, Architect. Walk the path the user has drawn, and speak only when the bridge is broken."

---

*Generated by Product Owner (Gandalf) — delivery-team:product-delivery*
