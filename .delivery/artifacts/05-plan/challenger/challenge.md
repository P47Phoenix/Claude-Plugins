# Adversarial Review: Stage Health Hardening Sprint Plan

**Reviewer**: Challenger (Devil's Advocate)
**Date**: 2026-03-29
**Artifacts Reviewed**: Sprint Plan v1.0, User Stories v1.0, Test Strategy v1.0, Deployment Strategy v1.0
**Confidence**: 4/5

---

## Challenge 1: Capacity Is Acknowledged but Not Actually Mitigated

**Severity**: MEDIUM

The sprint plan commits 3.5L equivalent against a 2.4L 80% ceiling -- 117% of the soft limit. The justification is "markdown-only edits, low complexity despite volume." The plan acknowledges this breach but offers no mitigation beyond awareness.

**The problem**: Awareness is not a contingency. If any story takes longer than expected -- and US-04 alone touches 3 files with a sub-flow insertion, validator update, gate criterion replacement, AND template additions -- there is no defined shed-load plan. Which story gets cut? What is the priority order for descoping?

**Recommendation**: Define an explicit shed-load order. US-05 (S, M4, independent) is the obvious candidate for deferral. The plan should state: "If velocity drops below plan by Step 4, US-05 is deferred to next sprint." Without this, the team will either crunch to finish all 5 or deliver 5 stories at reduced quality -- both outcomes the 80% ceiling exists to prevent.

**Verdict**: NOT BLOCKING. The justification for markdown-only work is reasonable, but the plan needs an explicit descope trigger.

---

## Challenge 2: Estimates Conflate "Markdown Edits" with "Low Effort"

**Severity**: MEDIUM

US-04 is rated L. It modifies 3 files, inserts a sub-flow step with renumbering, updates a DoD validator, replaces an existing gate criterion (the only destructive edit in the sprint), and adds two template sections. That is 4 distinct insertion points across 3 files plus a deletion-and-replacement. Calling this "markdown-only" understates the coordination complexity.

US-03 is rated M. It adds a WARNING criterion to one gate and a 5-step reconciliation process to another file's entry conditions. The reconciliation process is substantively more complex than anything in US-05 (rated S). The M rating relies on "only 2 files" but the content being inserted is dense and structurally novel (no prior reconciliation gate exists to pattern-match against).

**The problem**: Story point estimates appear to be based on file count rather than insertion complexity. The risk table identifies step renumbering as "Medium likelihood, High impact" -- which contradicts an M rating for a story that introduces a new entry condition pattern.

**Recommendation**: No re-rating needed at this point, but the team should timebox US-03 and US-04. If US-03 takes longer than expected at the M estimate, it is a signal that US-04 (L, more complex) will also overrun.

**Verdict**: NOT BLOCKING. Estimates are defensible but optimistic. The ordering (US-03 before US-04) at least provides an early signal if complexity is underestimated.

---

## Challenge 3: Test Strategy Has a Structural-Empirical Gap

**Severity**: HIGH

The test strategy correctly identifies 4 empirical ACs (AC-05a, AC-05b, AC-06a, AC-06b) that require pipeline runtime validation. These are deferred entirely to dogfooding (Phase 5, step 24 of 24 -- literally the last thing tested).

**The problem**: Dogfooding is defined as a BUG_FIX pipeline. BUG_FIX projects use Light Mode, which waives capacity and coverage matrices (FR-07/08/09). This means dogfooding does NOT exercise:

1. **Capacity matrix validation** (FR-09, FR-10) -- waived for BUG_FIX
2. **Coverage matrix validation** (FR-08, FR-09) -- waived for BUG_FIX
3. **The two-tier threshold behavior** (>80% warn, >100% block) -- waived for BUG_FIX

US-04 is the largest story (L, 4 FRs, 7 ACs) and its runtime behavior is never exercised by dogfooding. The structural tests verify the text exists, but they cannot verify that a future FEATURE pipeline will correctly parse and enforce the two-tier capacity model.

**Additionally**: The dogfooding plan says it will verify "No regressions in non-modified stages" (DF-13), but a BUG_FIX pipeline uses Light Mode routing which may skip or reduce those stages entirely. A BUG_FIX pipeline cannot prove that a FEATURE pipeline's non-Light stages are intact.

**Recommendation**: Either (a) run a second dogfooding pass with a FEATURE project type to exercise the Plan stage guardrails at full depth, or (b) explicitly accept the risk that US-04's runtime behavior is untested until the next real FEATURE pipeline. Option (b) is acceptable if documented, but the test strategy currently claims "All 12 FRs covered. Zero gaps" which is misleading -- FR-09 and FR-10 have structural coverage only, no empirical/runtime coverage.

**Verdict**: NOT BLOCKING, but the test strategy should acknowledge that FR-09/FR-10 runtime behavior is unverified by dogfooding due to BUG_FIX Light Mode waivers. The "zero gaps" claim is overstated.

---

## Challenge 4: Dogfooding Plan Is Necessary but Not Sufficient

**Severity**: MEDIUM

The dogfooding plan (Sprint Plan Section 8, Test Strategy Section 5) runs a single BUG_FIX pipeline. It verifies 13 conditions. This is good -- it is more than most sprint plans include. But:

1. **Single-run validation**: One pipeline run is a smoke test, not a validation. The phantom reference detection (FR-05/06) has two distinct behaviors: WARNING at Design, BLOCK at Dev entry. Testing both in one pipeline run means the pipeline must be deliberately manipulated (insert phantom refs, then fix them, then re-attempt). This is a contrived test, not a natural usage dogfood.

2. **No negative testing**: The dogfooding plan tests that gates fire when they should. It does not test that gates do NOT fire when they should not. What happens when all references are valid? Does the reconciliation gate silently pass, or does it error on empty results? What happens when a BUG_FIX has zero shared modules? Does step 5 of Stage 7 silently pass or throw?

3. **No regression baseline**: The plan says "No regressions in non-modified stages" but there is no pre-implementation baseline to compare against. How will the team know if a non-modified stage regresses if they have not recorded its pre-change behavior?

**Recommendation**: Add explicit "happy path" checks to dogfooding: (a) all references valid should produce zero warnings/blocks, (b) zero shared modules should silently pass the shared-module review, (c) zero derived artifacts should silently pass the regeneration step. These are 3 additional checks that catch the most likely defect class: gates that break normal flow.

**Verdict**: NOT BLOCKING. The dogfooding plan is solid for positive-path testing. Adding negative/happy-path cases would significantly strengthen it.

---

## Challenge 5: Deployment Strategy Missing Conflict Resolution for Shared Files

**Severity**: LOW

The deployment strategy commits one story per commit and says "No cross-story file changes in a single commit." But 4 of 5 stories modify `pipeline-stages.md` and 4 of 5 modify `quality-gates.md`. This means:

- Commit 1 (US-03) edits `pipeline-stages.md` Stage 6 entry conditions
- Commit 3 (US-01) edits `pipeline-stages.md` Stage 7 sub-flow
- Commit 5 (US-05) edits `pipeline-stages.md` Stage 6 sub-flow

These are different sections of the same file. The implementation sequence in the sprint plan handles this correctly (US-03 before US-05 since both touch Stage 6). But the deployment strategy does not mention what happens if a mid-sprint course correction requires reordering stories. If US-05 were implemented before US-03, the Stage 6 step numbers would be wrong.

**Recommendation**: The sprint plan already addresses this in the risk table ("Execute US-03 before US-05 since both touch Stage 6"). The deployment strategy should cross-reference this constraint explicitly rather than implying commit ordering is flexible.

**Verdict**: NOT BLOCKING. The risk is already mitigated in the sprint plan; the deployment strategy just does not reference it.

---

## Challenge 6: Hidden Dependency -- plugin-dev:skill-development Loading

**Severity**: LOW

The sprint plan correctly identifies that `plugin-dev:skill-development` must be loaded before any file edits. It is listed in Section 9 and Step 1. However, the deployment strategy does not mention it at all. The pre-merge checklist includes "plugin-dev:skill-development was loaded before file edits" but there is no mechanism to verify this retroactively.

**The risk**: If the skill is not loaded, the edits may not follow plugin-dev conventions for reference file structure. This would not cause a build failure (there is no build), but it could introduce inconsistent formatting that fails a future plugin-dev:plugin-validator run.

**Recommendation**: Low risk. The team is aware. No action needed beyond the existing checklist item.

**Verdict**: NOT BLOCKING.

---

## Summary Assessment

| # | Challenge | Severity | Verdict |
|---|-----------|----------|---------|
| 1 | No explicit descope trigger for capacity breach | MEDIUM | Not blocking |
| 2 | Estimates based on file count not insertion complexity | MEDIUM | Not blocking |
| 3 | BUG_FIX dogfooding does not exercise US-04 Plan guardrails at runtime | HIGH | Not blocking (with acknowledgment) |
| 4 | Dogfooding lacks negative/happy-path testing | MEDIUM | Not blocking |
| 5 | Deployment strategy does not reference story ordering constraints | LOW | Not blocking |
| 6 | plugin-dev skill loading is unverifiable retroactively | LOW | Not blocking |

**Overall Verdict**: PASS WITH RECOMMENDATIONS

The sprint plan, test strategy, and deployment strategy are well-constructed and internally consistent. The highest-risk finding is Challenge 3: the BUG_FIX dogfooding pipeline cannot validate US-04's Plan stage guardrails at runtime because Light Mode waives them. This should be explicitly acknowledged in the test strategy as a known coverage gap rather than claimed as "zero gaps."

No challenges rise to blocking severity. The team should:
1. Add a descope trigger (US-05 deferred if velocity drops)
2. Acknowledge the FR-09/FR-10 runtime coverage gap in the test strategy
3. Add 3 happy-path/negative dogfooding checks (valid refs, zero shared modules, zero derived artifacts)

---

*The fellowship's plan is sound. The path is well-mapped. But the map claims to show every danger, and it does not -- there is a gap where the BUG_FIX road diverges from the FEATURE road, and the Plan stage guardrails stand untested in that gap. Name the gap. Then march.*
