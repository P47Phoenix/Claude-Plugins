<!-- run: run-2026-09-18-pr88 -->
# UAT DoD: Product Owner Review (PR #88 CI fix)

Verdict: PASS (all criteria). Independently re-ran commands, did not trust QA table alone.

## Independent runs
- `python3 scripts/check_skill_budgets.py` -> `BUDGET CHECK PASSED: 17 file(s) checked, 0 known-debt, 0 exception(s).` exit 0.
- `wc -l` delivery-flow SKILL.md -> 497 (was 514; main 499).
- `git diff --stat` (working tree): 3 source files touched (delivery-flow SKILL.md, references/manifest.yml, smoke-test-architecture.md) + new untracked references/role-agent-dispatch.md; rest is `.delivery/` artifacts. No change to governance/ or .github/.
- Line 116 of smoke-test-architecture.md now `claude-sonnet-4-6`; repo grep for `claude-sonnet-4-5` outside `.delivery/` in tracked .md returns nothing.
- SKILL.md:335 and :368 keep "prefer `delivery-<role>`" plus pointer to reference; `delivery-orchestrator` discoverable at :336.

## Criteria
| # | Criterion | Result | Note |
|---|-----------|--------|------|
| G1 | budget-check exits 0, <=500, no Budget-Exception | PASS | 497/500, 0 exceptions, 0 known-debt |
| G2 | stale-id-guard clean | PASS | One-line fix; guard workflow untouched; QA guard replica exit 0 |
| G3 | Dispatch semantics preserved, PR behavior unchanged | PASS | Text moved to reference; pointers keep prefer-role-agent + fallback + orchestrator handoff; lines 1-332 identical |
| G4 | lint + header-warn stay green | PASS | lint OK; header-warn lists only pre-existing untouched files |
| G5 | PR text discloses rewrite, test plan honest | PASS (see Story 3) | |
| Defect triage | DEFECT-008/009 prioritized, non-blocking | PASS | see below |

## Defects
- DEFECT-008 (P3): manifest.yml line 49 invalid YAML, same error on HEAD, so pre-existing. No CI parses it. Non-blocking. Rightly filed for separate PR. TC-1.7 marked FAIL-PREEXISTING honestly, good. Note: PR touches manifest.yml (adds a row), so reviewer may ask "why not fix?" Recommendation: keep out to keep diff tight; optionally one-line quote fix if maintainer wants. Team decision: separate PR.
- DEFECT-009 (P4): stale line anchor in docs + hash file. Docs-only, pre-existing, not regression. Non-blocking.
- Severity/priority ordering right (P3 above P4). Neither blocks any required check.

## Story 3 adequacy
Adequate. Discloses 7-role rewrite (with commit refs), verbatim move, pre-existing main defect fix, and test plan with concrete commands. Confirmed diff count: 7 role SKILL.md + delivery-flow = 8 files (99+/266-), matches the "8 SKILL.md" claim; "about -170" in text is net across the 7 role files only (idea brief figure), fine.
Conditions (non-blocking, do before/while editing PR):
1. Check the test-plan boxes only for commands QA actually ran (all 4 CI ones were run; "all 4 required checks green on the PR" only after push and CI runs, leave unchecked until then).
2. Add to disclosure: DEFECT-008/009 are known pre-existing, not fixed here.
3. Work is uncommitted in the worktree; new reference file is untracked. Must `git add` the reference file or CI will still fail (manifest points at it, budget only passes because the text moved). This is the top ship risk.

## Residual risk
Low. Main risk is forgetting to commit the untracked reference file. PR edit is maintainer action (AC-3.1).
