<!-- run: run-2026-05-09-tk4 | stage: 05-plan | dod-round: 1 | depth: light | reviewer: qa-engineer (FRESH dispatch, Pippin Took persona) | lens: QA -->

# Plan DoD Review — QA Lens (run-2026-05-09-tk4, round 1)

**STATUS**: NOT_DONE
**ARTIFACT**: `.delivery/artifacts/05-plan/dod/qa-review.md`
**SCOPE**: Stage 5 LIGHT DoD round 1, Wave 3 closure (BACKLOG-104) — verifies the QA test-strategy artifact provides traceable runnable coverage for PRD FRs (1-7), BACKLOG-104 init ACs (10), and 35 Story ACs across 7 stories, plus tripwire activation protocol completeness.

## Inputs Reviewed

- `.delivery/artifacts/05-plan/po/stories.md` — 7 stories, 35 ACs (5 per story, verified by inspection)
- `.delivery/artifacts/05-plan/qa/test-strategy.md` — 14 TCs + 2 protocols (Empirical Measurement, Tripwire Activation)
- `.delivery/artifacts/05-plan/sm/sprint-plan.md` — 7-story sequencing + DoD checklist
- `.delivery/artifacts/02-refine/po/prd.md` — 7 FRs (FR-1..FR-7) + 8 NFRs + 7 PRD-level ACs
- `.delivery/backlog/BACKLOG-104-skill-token-economy-delivery-team-wave-3.md` — 10 initiative-level ACs (lines 280-289)

## Independent ID Cross-Reference (QA gate validation)

| Source | Count claimed | Count verified | Status |
|---|---:|---:|:-:|
| PRD FRs | 7 (FR-1..FR-7) | 7 | PASS |
| BACKLOG-104 init ACs | **task brief says 10** | **10** (AC-1..AC-10 at backlog lines 280-289) | PASS |
| Story ACs | 35 (5 × 7 stories) | 35 (Story 1=5, Story 2=5, Story 3=5, Story 4=5, Story 5=5, Story 6=5, Story 7=5) | PASS |
| Test Cases | 14 | 14 (TC-1..TC-14) | PASS |
| Total source lines to map | 7 + 10 + 35 = **52** | test-strategy claims **49** (7 PRD + 7 init + 35 story) | **MISMATCH — test-strategy maps only 7 of 10 init ACs** |

## Gate Criteria Results (6 binding checks)

### Gate 1 — Every PRD FR (1-7) has ≥1 TC
**PASS.** Coverage map at test-strategy lines 20-26:
- FR-1 → TC-1
- FR-2 → TC-2
- FR-3 → TC-3
- FR-4 → TC-4
- FR-5 → TC-5, TC-6, TC-7
- FR-6 → TC-8, TC-9
- FR-7 → TC-10, TC-11, TC-12, TC-13, TC-14

Cross-verified by inspection of TC content. All 7 FRs covered.

### Gate 2 — Every BACKLOG-104 init AC (10 ACs) has ≥1 TC OR Stage-7 dogfood activity
**NOT_PASS.** Coverage map (lines 27-33) maps init AC-1..AC-7 only. Three init ACs are unmapped or under-mapped:

| Init AC | Backlog claim | Mapping in test-strategy | Status |
|---|---|---|:-:|
| AC-1 | `known_debt[]` empty | TC-6 | OK |
| AC-2 | CLAUDE.md ≤150 | TC-8 | OK |
| AC-3 | governance frontmatter on every SKILL.md | TC-5 | OK |
| AC-4 | 4 Wave-2 carry-forwards discharged | TC-10, TC-11, TC-12 | OK |
| AC-5 | 2 caveman-lite carry-forwards + DEFECT-006 close | TC-13, TC-14 | OK |
| AC-6 | paradigm pattern ≥3 axes | TC-4 | OK |
| AC-7 | ≥50% cumulative reduction | Empirical Measurement Protocol | OK (protocol acceptable per Stage-7 deferred-data convention) |
| **AC-8** | **No regression in delivery-flow first-try DoD pass rate** | **Exit Criteria line 115: "cross-checked at retro" — no TC, no protocol** | **GAP** |
| **AC-9** | **Defects/story rolling 3-PR window ≤0.4** | **Exit Criteria line 116: "measured at retro" — no TC, no protocol** | **GAP** |
| **AC-10** | **Quarterly fitness review process operational (governance doc + scheduled GitHub Action live; first issue auto-opens)** | **Story 6 AC-2 (governance doc) and AC-3 (workflow + cron + injection-lint) — Story-6-AC-row in coverage map cites TC-8, TC-9, but TC-8 covers CLAUDE.md only and TC-9 covers retro KPI only. Neither TC verifies `governance/fitness-review.md` exists with required sections; neither TC verifies `.github/workflows/fitness-review-reminder.yml` exists, runs on cron, opens issues, or passes injection-lint** | **GAP** |

**Required corrections** (round-2 minimum):

1. Add a TC (e.g., TC-15) covering Story 6 AC-2 + AC-3 + BACKLOG-104 AC-10: verify `governance/fitness-review.md` exists with cadence/owner/inputs/outputs/kill-criteria sections, verify `.github/workflows/fitness-review-reminder.yml` exists + runs on weekly cron + opens issues 7 days before each `fitness_review_due:` date, AND verify the `workflow-injection-lint.yml` guard PASSES on the new workflow per DEFECT-004 regression guard.
2. Add explicit retro-stage protocol entries (named, runnable command shape) for init AC-8 (DoD pass-rate cross-check from `.delivery/memory/index.md`) and init AC-9 (defects/story rolling 3-PR window query). Today's bare "cross-checked at retro" / "measured at retro" lines violate the QA gate criterion that every init AC has ≥1 TC OR Stage-7 dogfood activity with a runnable check command — neither qualifies as runnable.

### Gate 3 — Every Story-N AC (35 ACs) has ≥1 TC
**PASS_WITH_NOTES.** Per-story verification:

- **Story 1 (5 ACs)**: AC-1 → TC-1, AC-2 → TC-1+TC-6, AC-3 → TC-1, AC-4 (cache invariant + head -120 line ≥111 check + ADR cite in PR body) → partially covered by TC-7 (cache-prefix hash regen) but the head-120 / extraction-line ≥111 explicit check is absent from TC-1 wording. AC-5 → TC-1 (`grep -c "references/roles" ≥11`). NOTE: Story 1 AC-4's "head -120 SKILL.md | tail -20 shows extracted-block boundary BELOW frontmatter + Phase 1 router" check is implied by cache-prefix invariance (TC-7) but not asserted as a runnable command in any TC. Acceptable for round-1 light gate; round-2 may sharpen.
- **Story 2 (5 ACs)**: All 5 → TC-2 (covers wc, 9+4 router, 3 ui, 3 ops, budget exit-0). PASS.
- **Story 3 (5 ACs)**: All 5 → TC-3 (covers quality + user-feedback + godot ≤197, including the round-2 zero-headroom binding `wc -l = 197` exactly + Wave-2 godot refs untouched + 15-input router). PASS.
- **Story 4 (5 ACs)**: All 5 → TC-4 (research-agent ≥5 sub-skills, persona =4, marketplace lint deliberate-violation path, cache invariant on parent, conditional presentation telemetry decision recorded). PASS.
- **Story 5 (5 ACs)**: All 5 → TC-5 (frontmatter lint + fault-injection FAIL path), TC-6 (budget + godot=200 exactly), TC-7 (cache-prefix regen + actual byte counts), Tripwire Activation Protocol (sequencing audit per AC-4; tripwire NOT-fired path per AC-5). PASS.
- **Story 6 (5 ACs)**: AC-1 → TC-9, AC-4+AC-5 → TC-8. **AC-2 (`governance/fitness-review.md` exists with required sections) and AC-3 (`.github/workflows/fitness-review-reminder.yml` exists + cron + opens issues + injection-lint passes) lack a dedicated TC.** Coverage-map row "TC-8, TC-9" is overstated. **GAP** (rolls up to init-AC-10 gap above).
- **Story 7 (5 ACs)**: AC-1 → TC-10+TC-11, AC-2 → TC-12 (covers both JSON↔Python lint AND pre-commit hook fail-path), AC-3 → TC-13 (DEFECT-006 close), AC-4 → TC-14 (telemetry placeholder route), AC-5 → TC-6 (`known_debt[]` empty). PASS.

**Story-AC outcome**: 33 of 35 explicitly mapped to runnable TC commands; 2 ACs (Story-6-AC-2 + Story-6-AC-3) are claimed mapped but the cited TCs (TC-8, TC-9) verify different content. **NOT_PASS** when cross-validated at the AC granularity.

### Gate 4 — Every TC's check command runnable with bash + python3 stdlib
**PASS.** Independent scan via `grep -nE "(yq|jq|awk|sed|perl|node|npm|pip install|cargo|go run)"` returned zero hits. All commands use `wc -l`, `grep`, `find`, `git log/diff`, `python3 scripts/*.py` (NFR-3 binding satisfied). PyYAML mentioned as the only stdlib-adjacent dep, consistent with PRD NFR-3.

Spot-check on representative commands:
- TC-1: `wc -l`, `grep -c`, spot-check (procedural) — runnable
- TC-3: `wc -l`, `git diff --name-only` — runnable
- TC-4: `find ... | wc -l`, `grep -L` — runnable
- TC-5: `grep -L`, `python3 scripts/lint_skill_frontmatter.py` — runnable (script ships in W3-9 per Story 5 Files Touched)
- TC-12: workflow trigger + fault-injection branch — runnable as CI workflow + `grep -E '\$\{\{[[:space:]]*github\.event\.'`
- TC-13: file plant + Stage-7 entry-step run — runnable

### Gate 5 — Coverage map gap-free (verify by independent ID cross-reference)
**NOT_PASS.** Independent enumeration finds:

- Coverage-map "Tally" line 42 says "7 PRD FRs + 7 initiative ACs + 35 story ACs = 49 source lines". The task brief (and BACKLOG-104 §Acceptance Criteria) has **10 init ACs**, not 7. The artifact under-counts by 3 init ACs (AC-8, AC-9, AC-10) and reports "Zero unmapped lines; PO Plan-memory-lesson-2 satisfied" on a wrong denominator. The true count is 52 source lines; 3 are unmapped. **The "zero gaps" claim is contradicted by the inputs.**
- Story-6-row mapping is overstated (TC-8 + TC-9 do not cover Story-6-AC-2 + AC-3). See Gate 3.

This gate is the binding round-1 failure: PO Plan-memory-lesson-2 ("test cases MUST cover ALL [source items] explicitly; PO rejects any plan missing one") is violated as written.

### Gate 6 — Tripwire activation protocol covers all 5 elements + Stage-7 verification step
**PASS.** Tripwire Activation Protocol (test-strategy lines 82-91) inspected element-by-element:

| Element | Coverage | Line |
|---|---|---|
| Source | `.delivery/telemetry/stop-rule-tk4.txt` existence check | step 1, line 86 |
| Calc | `python3 scripts/compute_token_reduction.py --baseline pre-caveman-lite --window 3 --output …` reading first-3-dispatch mean | step 2, line 87 |
| Baseline | `pre-caveman-lite` (named in step 2 command shape) | step 2, line 87 |
| Threshold | `<15%` reduction → tripwire DID FIRE | step 3, line 88 |
| Recovery | `.delivery/memory/` caveman-lite root-cause retro entry; BACKLOG-102 follow-up issue; Stage 4 round-3 / Wave 4 deferral decision recorded | step 5, line 90 |
| Stage-7 verification step | QA writes finding to `.delivery/artifacts/07-uat/qa/tripwire-verification.md` citing FIRED / NOT FIRED path with artifact lines | step 6, line 91 |

All 5 elements + Stage-7 verification covered. Additional sequencing audit (step 4) bridges the NOT-FIRED path to Story 5 AC-4. PASS.

## Gate Summary

| # | Gate | Result |
|--:|---|:-:|
| 1 | Every PRD FR (1-7) has ≥1 TC | **PASS** |
| 2 | Every BACKLOG-104 init AC (10) has ≥1 TC or Stage-7 dogfood | **NOT_PASS** (AC-8, AC-9, AC-10 gaps) |
| 3 | Every Story-N AC (35) has ≥1 TC | **NOT_PASS** (Story-6 AC-2 + AC-3 mis-mapped) |
| 4 | TC commands runnable via bash + python3 stdlib | **PASS** |
| 5 | Coverage map gap-free under independent cross-reference | **NOT_PASS** (denominator wrong: 49 claimed vs 52 actual; 3 unmapped) |
| 6 | Tripwire activation protocol covers 5 elements + Stage-7 step | **PASS** |

**Result**: 3 of 6 PASS, 3 of 6 NOT_PASS — round-1 gate FAILS.

## Traceability Summary

- **PRD FR coverage**: 7/7 (100%)
- **BACKLOG-104 init AC coverage**: 7/10 (70%) — AC-8, AC-9, AC-10 unmapped or under-mapped
- **Story AC coverage**: 33/35 (94.3%) — Story 6 AC-2 and AC-3 cited TC-8/TC-9 do not verify the asserted content
- **TC command runnability**: 14/14 (100%)
- **Tripwire protocol completeness**: 6/6 elements (100%)

## Required Round-2 Corrections (binding for round-2 PASS)

1. **Add TC-15** (or equivalent): "Fitness review process operational (Story 6 AC-2 + AC-3 + init AC-10)". Commands at minimum:
   - `test -f governance/fitness-review.md` returns 0
   - `grep -E "^(##|###) (Cadence|Owner|Inputs|Outputs|Kill[- ]criteria)" governance/fitness-review.md` returns ≥5 matches
   - `test -f .github/workflows/fitness-review-reminder.yml` returns 0
   - `grep -E "schedule:|cron:" .github/workflows/fitness-review-reminder.yml` returns ≥1 match
   - `grep -E '\$\{\{[[:space:]]*github\.event\.' .github/workflows/fitness-review-reminder.yml` returns 0 `run:`-block matches (DEFECT-004 regression guard)
   - Synthetic dry-run of the workflow opens an issue for the earliest `fitness_review_due:` date.
2. **Add named retro-stage protocol entries** for init AC-8 and init AC-9 with runnable command shapes (e.g., `python3 scripts/dod_pass_rate.py --window pre-W3 --window W3` and `python3 scripts/defects_per_story.py --window 3`). Bare "cross-checked at retro" is not runnable per Gate 4 standard.
3. **Correct the Coverage Map "Tally" line** from "7 + 7 + 35 = 49" to "7 + 10 + 35 = 52" and re-verify zero-gap claim.
4. **Tighten Story-6-row** mapping in the coverage map to cite TC-8, TC-9, and the new TC-15 — not just TC-8, TC-9.
5. **Optional sharpening** (round-3 candidate, not round-2 binding): add an explicit `head -120 delivery-team/skills/architect/SKILL.md | tail -20` boundary check to TC-1 to make Story 1 AC-4's "extraction lines start at line ≥111" assertion runnable in addition to inferred-from-cache-invariance.

## Verdict

The QA test-strategy artifact passes 3 of 6 binding gates and is well-structured (14 TCs are runnable, the godot-zero-headroom binding is doubly verified at TC-3 and TC-6, fault-injection paths are explicit, and the Tripwire protocol is element-complete) — but it under-counts BACKLOG-104 initiative ACs (49 mapped vs 52 actual; init AC-8/AC-9/AC-10 are not provided runnable checks) and overstates Story-6-row coverage (TC-8/TC-9 do not verify governance/fitness-review.md or the GitHub Action workflow). Round-1 fails on Gate 5 (coverage-map gap-free claim is contradicted by independent enumeration); add TC-15 + retro protocol entries + corrected tally for round-2 PASS.

— Pippin Took (FRESH dispatch, DoD reviewer), QA Engineer, run-2026-05-09-tk4. Three init ACs the tall folk would have skipped; the small folk count to ten, not seven.
