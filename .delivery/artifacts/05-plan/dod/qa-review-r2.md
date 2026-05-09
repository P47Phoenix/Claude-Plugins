<!-- run: run-2026-05-09-tk4 | stage: 05-plan | dod-round: 2 | depth: light | reviewer: qa-engineer (FRESH dispatch, Pippin Took persona) | lens: QA -->

# Plan DoD Review — QA Lens (run-2026-05-09-tk4, round 2)

**STATUS**: DONE
**ARTIFACT**: `.delivery/artifacts/05-plan/dod/qa-review-r2.md`
**SCOPE**: Stage 5 LIGHT DoD round 2, Wave 3 closure (BACKLOG-104) — re-verifies the QA test-strategy artifact after round-1 NOT_PASS on Gates 2, 3, and 5; confirms the three round-2 fixes land cleanly and Gates 1/4/6 do not regress.

## Inputs Reviewed

- `.delivery/artifacts/05-plan/po/stories.md` — 7 stories, 35 ACs (5 per story; Story 6 ACs at lines 246-250 verified by inspection)
- `.delivery/artifacts/05-plan/qa/test-strategy.md` — **16 TCs + 4 protocols** (Empirical Measurement, Tripwire Activation, **DoD Pass-Rate Regression — NEW**, **Defects-Per-Story Rolling Window — NEW**)
- `.delivery/artifacts/05-plan/sm/sprint-plan.md` — 7-story sequencing + DoD checklist
- `.delivery/artifacts/02-refine/po/prd.md` — 7 FRs (FR-1..FR-7) + 8 NFRs
- `.delivery/backlog/BACKLOG-104-skill-token-economy-delivery-team-wave-3.md` — **10 initiative-level ACs (lines 280-289 verified)**

## Independent ID Cross-Reference (QA gate validation, round 2)

| Source | Count claimed (round 2) | Count verified | Status |
|---|---:|---:|:-:|
| PRD FRs | 7 (FR-1..FR-7) | 7 | PASS |
| BACKLOG-104 init ACs | **10** (round-2 corrected) | 10 (AC-1..AC-10 at backlog lines 280-289) | PASS |
| Story ACs | 35 (5 × 7 stories) | 35 (Story 1=5, 2=5, 3=5, 4=5, 5=5, 6=5, 7=5) | PASS |
| Test Cases | **16** (was 14; TC-15 + TC-16 added) | 16 (TC-1..TC-16) | PASS |
| Protocols | **4** (was 2; DoD Pass-Rate + Defects-Per-Story added) | 4 | PASS |
| Total source lines to map | 7 + 10 + 35 = **52** | test-strategy line 45 claims **52** (round-2 corrected from 49) | **MATCH — denominator now correct** |

## Gate Criteria Results (6 binding checks)

### Gate 1 — Every PRD FR (1-7) has ≥1 TC

**PASS (regression check).** Coverage map at test-strategy lines 20-26 unchanged in substance; FR-6 mapping was extended to add TC-15 + TC-16 (the new fitness-review TCs):

- FR-1 → TC-1
- FR-2 → TC-2
- FR-3 → TC-3
- FR-4 → TC-4
- FR-5 → TC-5, TC-6, TC-7
- FR-6 → TC-8, TC-9, **TC-15, TC-16** (round-2 extension; correctly mapped)
- FR-7 → TC-10, TC-11, TC-12, TC-13, TC-14

All 7 FRs covered. No regression.

### Gate 2 — Every BACKLOG-104 init AC (10 ACs) has ≥1 TC OR Stage-7 dogfood activity (round-1 NOT_PASS — round-2 fix verification)

**PASS.** Round-1 gaps on init AC-8, AC-9, AC-10 are resolved. Re-verified row-by-row:

| Init AC | Backlog claim | Round-2 mapping | Status |
|---|---|---|:-:|
| AC-1 | `known_debt[]` empty | TC-6 | OK |
| AC-2 | CLAUDE.md ≤150 | TC-8 | OK |
| AC-3 | governance frontmatter on every SKILL.md | TC-5 | OK |
| AC-4 | 4 Wave-2 carry-forwards discharged | TC-10, TC-11, TC-12 | OK |
| AC-5 | 2 caveman-lite carry-forwards + DEFECT-006 close | TC-13, TC-14 | OK |
| AC-6 | paradigm pattern ≥3 axes | TC-4 | OK |
| AC-7 | ≥50% cumulative reduction | Empirical Measurement Protocol | OK |
| **AC-8** | **No DoD pass-rate regression** | **DoD Pass-Rate Regression Protocol (test-strategy lines 98-106)** with named runnable command `python3 scripts/dod_pass_rate.py --archive-glob '.delivery/memory/archive/*.md' --window 5 --include-current tk4 --output .delivery/telemetry/dod-pass-rate-tk4.txt` and explicit hand-tally fallback `grep -c "^STATUS: DONE" .delivery/artifacts/*/dod/*.md` | **OK (round-2 fix verified)** |
| **AC-9** | **Defects/story rolling 3-PR ≤0.4** | **Defects-Per-Story Rolling Window Protocol (test-strategy lines 108-116)** with named runnable command `python3 scripts/defects_per_story.py --pr-window 3 --story-source .delivery/artifacts/05-plan/po/stories.md --output .delivery/telemetry/defects-per-story-tk4.txt` and `gh issue list --label defect …` fallback | **OK (round-2 fix verified)** |
| **AC-10** | **Quarterly fitness review process operational (governance doc + scheduled GitHub Action)** | **TC-15 (governance doc — `test -f governance/fitness-review.md` + section-header grep) + TC-16 (workflow — `test -f .github/workflows/fitness-review-reminder.yml` + cron grep + DEFECT-004 injection-lint guard + synthetic dry-run opens issue)** | **OK (round-2 fix verified)** |

The two new protocols satisfy the Gate 4 runnability standard that the round-1 bare "cross-checked at retro" / "measured at retro" lines violated: each protocol declares Source, Window, Command (with primary script invocation AND hand-query fallback), Pass criterion, and binding Output artifact. Both are correctly framed as Stage 7 dogfood activities (consume post-Stage-6 telemetry not available at Plan time), which is the convention permitted by the gate criterion.

10/10 init ACs have a runnable TC or Stage-7 protocol. **PASS.**

### Gate 3 — Every Story-N AC (35 ACs) has ≥1 TC (round-1 NOT_PASS — round-2 fix verification)

**PASS.** Round-1 finding: Story 6 AC-2 (governance doc) and AC-3 (workflow) were claimed mapped to TC-8/TC-9 but the cited TCs verify CLAUDE.md and retro KPI — different content. Round-2 inspection of test-strategy line 42 shows the Story-6-row mapping is now split correctly:

> Story 6 ACs (5) | AC-1 KPI → TC-9; AC-2 governance doc → TC-15; AC-3 workflow + cron + injection-lint → TC-16; AC-4 CLAUDE.md ≤150 → TC-8; AC-5 stale-path side-fix → TC-8

Cross-checked against stories.md lines 246-250:

- Story 6 AC-1 (`context_tokens_per_pipeline_run` KPI) → TC-9 (retro template KPI integration) — content match.
- Story 6 AC-2 (`governance/fitness-review.md` cadence/owner/inputs/outputs/kill-criteria) → TC-15 (`test -f` + section-header grep ≥5; kill-criteria explicitly cites the "2 quarters in a row" threshold) — content match.
- Story 6 AC-3 (`.github/workflows/fitness-review-reminder.yml` weekly cron + opens issues + injection-lint passes) → TC-16 (`test -f` + cron grep + zero `${{ github.event.* }}` matches + synthetic dry-run opens issue for planted due-date) — content match.
- Story 6 AC-4 (CLAUDE.md ≤150 + one-hop discoverability) → TC-8 (`wc -l ≤150` + `grep -E "ARCHITECTURE.md|plugin-catalog.md"` ≥1) — content match.
- Story 6 AC-5 (stale `architect/skills/paradigms/` corrected) → TC-8 (`grep "architect/skills/paradigms/" CLAUDE.md` returns 0) — content match.

All 5 Story 6 ACs now map to TCs that verify the asserted content. Per-story re-verification of Stories 1, 2, 3, 4, 5, 7 (round-1 PASS_WITH_NOTES outcomes): no regressions; round-1 light-gate sharpening on Story 1 AC-4 head-120 boundary check remains a round-3 candidate, not round-2 binding (consistent with round-1 deferral).

35/35 Story ACs map to TCs verifying the asserted content. **PASS.**

### Gate 4 — Every TC's check command runnable with bash + python3 stdlib (regression check)

**PASS.** Independent regression scan via `grep -nE "(yq|jq|awk|sed|perl|node|npm|pip install|cargo|go run)"` returned zero hits across the round-2 test-strategy. New TC-15 and TC-16 use only `test -f`, `grep -E`, and synthetic-dry-run procedures consistent with the round-1 Gate 4 standard. The two new protocols use `python3 scripts/*.py` invocations with `gh` CLI fallback (note: `gh` is GitHub-CLI standard tooling assumed available in the dev environment; round-1 Gate 4 standard accepts this since the existing tripwire references `git log --merges` and the broader CI workflow shape already depends on `gh`). PyYAML remains the only stdlib-adjacent dep, consistent with PRD NFR-3.

No regression. **PASS.**

### Gate 5 — Coverage map gap-free (verify by independent ID cross-reference) (round-1 NOT_PASS — round-2 fix verification)

**PASS.** Round-1 finding: tally was "7 + 7 + 35 = 49" (under-counted by 3 init ACs); round-2 inspection of test-strategy line 45 shows:

> **Tally**: 7 PRD FRs + 10 initiative ACs + 35 story ACs = **52 source lines** mapped to 16 TCs + 4 Protocols (Empirical Measurement, Tripwire Activation, DoD Pass-Rate Regression, Defects-Per-Story Rolling Window). **Zero unmapped lines**; PO Plan-memory-lesson-2 satisfied (round-2 corrected denominator: 10 init ACs verified at BACKLOG-104 lines 280-289, not 7).

Independent enumeration confirms 7 + 10 + 35 = 52. Each row in the coverage map (lines 20-43) maps a source ID to a TC or Protocol; the three previously-missing init ACs (AC-8 / AC-9 / AC-10) now appear at lines 34-36 with explicit mappings. The Story-6-row at line 42 explicitly itemizes which TC verifies which Story 6 AC (no more umbrella "TC-8, TC-9" claim that papers over content mismatch). **Zero unmapped lines** claim is now consistent with the inputs.

PO Plan-memory-lesson-2 ("test cases MUST cover ALL [source items] explicitly; PO rejects any plan missing one") satisfied. **PASS.**

### Gate 6 — Tripwire activation protocol covers all 5 elements + Stage-7 verification step (regression check)

**PASS.** Tripwire Activation Protocol (test-strategy lines 87-96) re-inspected element-by-element; substance unchanged from round 1:

| Element | Coverage | Line |
|---|---|---|
| Source | `.delivery/telemetry/stop-rule-tk4.txt` existence check | step 1, line 91 |
| Calc | `python3 scripts/compute_token_reduction.py --baseline pre-caveman-lite --window 3 --output …` | step 2, line 92 |
| Baseline | `pre-caveman-lite` (named in command shape) | step 2, line 92 |
| Threshold | `<15%` reduction → tripwire DID FIRE | step 3, line 93 |
| Recovery | caveman-lite root-cause retro entry; BACKLOG-102 follow-up; Stage 4 round-3 / Wave 4 deferral decision | step 5, line 95 |
| Stage-7 verification step | QA writes finding to `.delivery/artifacts/07-uat/qa/tripwire-verification.md` citing FIRED / NOT FIRED path | step 6, line 96 |

All 5 elements + Stage-7 verification covered. No regression. **PASS.**

## Gate Summary

| # | Gate | Round 1 | Round 2 |
|--:|---|:-:|:-:|
| 1 | Every PRD FR (1-7) has ≥1 TC | PASS | **PASS** |
| 2 | Every BACKLOG-104 init AC (10) has ≥1 TC or Stage-7 dogfood | NOT_PASS | **PASS** |
| 3 | Every Story-N AC (35) has ≥1 TC | NOT_PASS | **PASS** |
| 4 | TC commands runnable via bash + python3 stdlib | PASS | **PASS** |
| 5 | Coverage map gap-free under independent cross-reference | NOT_PASS | **PASS** |
| 6 | Tripwire activation protocol covers 5 elements + Stage-7 step | PASS | **PASS** |

**Result**: 6 of 6 PASS — round-2 gate PASSES.

## Traceability Summary

- **PRD FR coverage**: 7/7 (100%)
- **BACKLOG-104 init AC coverage**: **10/10 (100%)** — round-1 7/10 → round-2 10/10 via TC-15 + TC-16 (init AC-10) and two new named protocols (init AC-8 + AC-9)
- **Story AC coverage**: **35/35 (100%)** — round-1 33/35 → round-2 35/35 via Story-6-row split into per-AC mappings
- **TC command runnability**: **16/16 (100%)** — round-1 14/14 + new TC-15 + TC-16 both runnable
- **Tripwire protocol completeness**: 6/6 elements (100%)
- **Total source lines**: 52 (7 PRD FRs + 10 init ACs + 35 story ACs); zero unmapped

## Verdict

The QA test-strategy artifact passes all 6 binding gates after round 2: TC-15 + TC-16 cleanly close the Story 6 AC-2/AC-3 + init AC-10 gap with runnable `test -f` + section-header grep + injection-lint guard + synthetic-dry-run checks; the two new named protocols (DoD Pass-Rate Regression, Defects-Per-Story Rolling Window) replace the round-1 bare "cross-checked at retro" / "measured at retro" lines with concrete script invocations, hand-query fallbacks, and binding output artifacts; the tally correction (49 → 52) restores PO Plan-memory-lesson-2 compliance under independent cross-reference. Round-1 Gates 1/4/6 hold without regression; Gate 5's "zero unmapped" claim is now consistent with the 7 + 10 + 35 = 52 enumeration. STATUS: DONE.

— Pippin Took (FRESH dispatch, DoD reviewer, round 2), QA Engineer, run-2026-05-09-tk4. The hobbits counted to ten this time, and every line found its TC; the road is plain and the gates are sharp.
