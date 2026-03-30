# Adversarial Challenge: Stage Health Hardening PRD

**Challenger**: QA Engineer (Devil's Advocate)
**Date**: 2026-03-29
**PRD**: Stage Health Hardening v1.0
**Confidence Rating**: 3 / 5

---

## Challenge 1: The 50% to 80% Design Target Relies on a Single Mechanism

**Claim challenged**: G1 assumes Design first-try pass rate jumps from 50% to >=80% by elevating phantom references to blocking severity (FR-05) and adding a Dev-entry reconciliation gate (FR-06).

**Problem**: The PRD's own evidence says the Design stage has a 50% pass rate with a sample size of 6 attempts across 3 runs. That is extremely thin data. A single additional pass or fail swings the rate by ~17 percentage points. The baseline is statistically unreliable.

More critically, FR-05 elevates phantom references to blocking -- but phantom references are only *one* root cause of Design failures. The PRD does not demonstrate that phantom references account for enough of the failures to close the 30pp gap. If even one Design failure in those 6 attempts was caused by something other than phantom references (e.g., incomplete user flows, missing edge cases -- which are existing Gate 3 blocking criteria), FR-05 alone cannot reach 80%.

FR-06 is a *Dev-entry* gate, not a Design gate. It catches phantom references that survive past Design into Development. It does not improve Design's own first-try pass rate -- it prevents downstream damage. The PRD conflates "catching phantoms at Dev entry" with "Design passing on first try."

**Verdict**: The target is aspirational but undersupported. The causal chain from FR-05/FR-06 to a 30pp improvement is not established.

**Recommendation**: Either (a) reduce the target to >=70% for the first validation period and re-evaluate after 5 runs, or (b) add explicit evidence from retrospectives showing that phantom references were the root cause in at least 2 of the 3 Design failures, not merely a contributing factor.

---

## Challenge 2: OQ-1 (Planned vs. Phantom Files) Is Higher Risk Than Rated

**Claim challenged**: The QA evaluation rates OQ-1 as non-blocking, with a default of "treat all missing files as phantom."

**Problem**: This default is actively harmful. In a GREENFIELD or FEATURE project, the Design stage *routinely* references files that do not yet exist -- they are planned artifacts to be created in Development. Under the "treat all missing as phantom" default:

- FR-05 would block Design completion on every GREENFIELD project that references files to be created.
- FR-06 would block Dev entry on every project where Design and Architect stages plan new files.

This is not an edge case. It is the common case for the two most frequent project types. The PRD acknowledges this risk in Section 7 (Risk: "phantom reference elevation blocks stages on false positives"), rates it Low likelihood, and claims FR-06 "runs at Dev entry, giving teams Design+Architect stages to establish file paths." But FR-05 runs at *Design DoD* -- before Architect even starts. Planned files will not exist yet at that point.

**Verdict**: OQ-1 should be resolved before leaving Refine. The "treat all as phantom" default will cause false-positive blocking on the majority of pipeline runs.

**Recommendation**: FR-05 needs a mechanism to distinguish planned files from phantom files. Options: (a) require Design artifacts to annotate planned-but-not-yet-existing paths with a marker (e.g., `[PLANNED]`), (b) only flag phantom references for *existing* files that have been renamed or moved, or (c) limit FR-05 severity to WARNING and reserve BLOCKING for FR-06 at Dev entry where files should actually exist. Option (c) is simplest and avoids Design-stage false positives entirely.

---

## Challenge 3: Shared-Module Definition Ambiguity (OQ-2) Creates Enforcement Gaps

**Claim challenged**: FR-01 defines shared modules as "a file imported by 2+ other modules" but OQ-2 asks whether this should be directory-based instead.

**Problem**: The "imported by 2+ other modules" definition requires the QA sub-agent to perform cross-file import analysis at UAT time. This is:

1. **Language-dependent** -- import syntax varies across the 14 supported languages. Python uses `import/from`, TypeScript uses `import/require`, Go uses package paths, Rust uses `use/mod`. The QA agent would need language-aware static analysis.
2. **Fragile for markdown-only repos** -- this repository (Claude-Plugins) is almost entirely markdown. The concept of "imported by 2+ modules" does not map cleanly to markdown files that reference each other via file paths rather than language-level imports.
3. **Not enforceable via markdown changes alone** -- NFR-01 says "no new Python scripts or external dependencies." But reliably detecting shared modules requires tooling, not just a checklist item.

The PRD's own scope is markdown-only changes (NFR-01), yet FR-01's acceptance criteria assume the QA agent can determine import graphs. This is a scope/feasibility tension.

**Verdict**: The shared-module definition needs to be concrete and enforceable within the markdown-only constraint.

**Recommendation**: Define "shared module" as: a file that is explicitly referenced (by path or name) in 2+ stage artifacts across the current pipeline run. This makes it artifact-traceable rather than code-dependency-traceable, and the QA agent can verify it using Glob/Read on the artifact directory.

---

## Challenge 4: Regression Risk in Gate 5 (Plan Readiness) -- Contradictory Capacity Thresholds

**Claim challenged**: FR-10 adds a >100% allocation warning to the Plan stage.

**Problem**: Gate 5 already has a blocking criterion: "Commitment does not exceed 80% of available capacity [blocking]." This is in the current `quality-gates.md` (line 180 in pipeline-stages.md). FR-10 adds a *warning* at >100% allocation.

These two criteria are contradictory:
- Existing Gate 5: >80% is BLOCKING (hard stop).
- FR-10: >100% is WARNING (acknowledged override allowed).

If the existing 80% blocking criterion stays, FR-10's 100% warning is unreachable -- you cannot be at >100% if you are already blocked at >80%. If the intent is to *replace* the 80% criterion with the softer 100% warning, that is a regression in an existing gate.

The PRD does not address this conflict. Neither does the QA evaluation.

**Verdict**: This is a specification conflict that will cause implementation confusion or a silent regression in Plan stage rigor.

**Recommendation**: Explicitly state the relationship between the existing 80% blocking criterion and the new 100% warning. Options: (a) keep the 80% block and remove FR-10 as redundant, (b) replace the 80% block with the 100% warning (and document this as a deliberate relaxation with rationale), or (c) layer them: 80% emits a warning, 100% blocks. The PRD must choose.

---

## Challenge 5: NFR-04 Token Budget Claim Is Unverifiable at PRD Time

**Claim challenged**: NFR-04 says added content should not increase per-stage context load by more than 500 tokens.

**Problem**: The PRD modifies 5 files across 4 stages. Each file gets additions from multiple FRs. The token impact depends on how much markdown is actually added -- which is an implementation-time concern, not a PRD-time concern. There is no way to verify NFR-04 at the Refine stage. It is also unclear whether the 500-token budget is per-file, per-stage, or per-pipeline-run.

This NFR is well-intentioned but unenforceable without implementation, making it a toothless gate criterion.

**Verdict**: Minor concern. The NFR should clarify "per-stage" vs. "per-file" and be validated at Dev/UAT, not treated as a Refine-stage constraint.

**Recommendation**: Clarify that NFR-04 means "per-stage" (total new content loaded for any single stage does not exceed 500 tokens). Validation deferred to Dev stage DoD where actual line counts can be measured.

---

## Challenge 6: Missing Edge Case -- Light Mode Stages

**Claim challenged**: The PRD addresses standard pipeline flow but does not account for Light Mode.

**Problem**: Pipeline-stages.md defines Light Mode for BUG_FIX and DOCS_ONLY project types (visible in Stage 5 Light Mode section). Light Mode skips consensus protocol and adversarial review, and reduces Plan to a minimal plan. The PRD's FR-07/FR-08/FR-09/FR-10 (capacity matrix, coverage matrix) apply to Plan stage -- but in Light Mode, the SM produces a "minimal plan" not a full sprint plan.

Should Light Mode plans still require capacity and coverage matrices? If yes, the "minimal plan" is no longer minimal. If no, there is a bypass path that lets overcommitted plans through on BUG_FIX projects.

Similarly, FR-01 (shared-module review at UAT) -- does this apply to BUG_FIX UAT? Bug fixes are arguably *more* likely to touch shared modules (fixing a bug in a shared utility) yet Light Mode may not invoke the full UAT flow.

**Verdict**: Light Mode exemptions are a meaningful gap in the FRs.

**Recommendation**: Add a sentence per FR or a dedicated section clarifying Light Mode behavior. At minimum: FR-01 (shared-module review) should apply regardless of mode since shared-module bugs are high-risk. FR-07/FR-08 can be waived for BUG_FIX/DOCS_ONLY. FR-10 should still apply even in Light Mode since a single-story bug fix can still be overscoped.

---

## Challenge 7: Dogfooding Validation Creates a Circular Dependency

**Claim challenged**: Section 2 states dogfooding is a P0 UAT gate -- "the hardened stages must be validated by running an actual pipeline through them."

**Problem**: The dogfooding pipeline run will exercise the *modified* reference files. But the modifications are the deliverables of *this* pipeline. This means:

1. Implement changes in Dev stage (Stage 6).
2. UAT (Stage 7) requires running a pipeline with the changes.
3. That pipeline run uses the modified gates, which may themselves have issues.
4. If the dogfooding pipeline fails, is it a bug in the changes or a legitimate gate failure in the dogfooding project?

This is not a showstopper -- it is the nature of self-referential improvement. But the PRD should acknowledge the risk of confounding and define what "dogfooding success" looks like: does the dogfooding pipeline need to complete all 7 stages, or just exercise the modified stages (Design, Plan, Dev, UAT)?

**Verdict**: Minor gap. The dogfooding criterion needs a specific definition of success.

**Recommendation**: Define dogfooding as: "Run a BUG_FIX pipeline that exercises at least Design, Plan, and UAT stages. The pipeline must reach completion without regressions caused by the gate changes. Failures unrelated to the gate changes (e.g., unrelated DoD findings) do not count as dogfooding failures."

---

## Summary of Findings

| # | Area | Severity | Action Required |
|---|------|----------|-----------------|
| C1 | Design 50%->80% target | HIGH | Substantiate causal link or reduce target |
| C2 | OQ-1 planned vs. phantom files | HIGH | Resolve before leaving Refine -- false-positive risk on common project types |
| C3 | Shared-module definition | MEDIUM | Clarify definition within markdown-only constraint |
| C4 | Gate 5 capacity contradiction | HIGH | Resolve 80% blocking vs. 100% warning conflict |
| C5 | NFR-04 token budget | LOW | Clarify scope, defer validation to Dev |
| C6 | Light Mode gap | MEDIUM | Specify Light Mode behavior per FR |
| C7 | Dogfooding success criteria | LOW | Define what constitutes a successful dogfooding run |

---

## Confidence Rating: 3 / 5

**Rationale**: The PRD is well-structured, evidence-grounded, and thoroughly traced to retrospective items. The QA evaluation caught the right things at its level. However, three issues -- the planned-vs-phantom file false positive risk (C2), the capacity threshold contradiction (C4), and the unsubstantiated Design target (C1) -- represent specification-level problems that will surface during implementation. C2 and C4 in particular could cause regressions in currently-passing stages if implemented as written.

Confidence is not low enough to warrant immediate human escalation (that threshold is <=2), but the PO should address C2 and C4 before the PRD leaves Refine. C1 can be resolved by adjusting the target or providing evidence.
