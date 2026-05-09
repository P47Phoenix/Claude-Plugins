<!-- run: run-2026-05-09-tk4 | stage: 07-uat | depth: full | author: QA Engineer (Legolas Greenleaf) | role: qa-engineer | task: test-plan | wave: 3 — final -->

# UAT Test Plan — Wave 3 (run-2026-05-09-tk4, BACKLOG-104 closure)

> "The leaves are counted, the road is marked, the last ridge is in sight. Five waves walked; the trees stand straighter than when we found them."
> — Legolas, surveying the field at the end of the road.

Stage 7 UAT for the final wave of the Skill Token-Economy initiative. Seven stories, 35 story-ACs, 10 initiative-ACs, 7 PRD FRs — all converged on Stage 6 with developer + qa + architect + tech-writer DoD reviews PASS. UAT verifies the integration: every test case from the test-strategy executes against the merged-but-unreleased tree, the cumulative token-economy delta is computed against the pre-Wave-0 baseline, the caveman-lite AC-13 close-out is honestly attempted, and the stop-rule status is recomputed.

## Scope

**In**:
1. Empirical execution of all 16 test cases from `.delivery/artifacts/05-plan/qa/test-strategy.md` against the post-Story-7 tree.
2. Cumulative reduction calculation across Waves 0+1+2+caveman-lite+3 vs the pre-Wave-0 baseline (BACKLOG-104 §6 AC-6 / NFR-4 — target ≥50%).
3. caveman-lite AC-13 close-out attempt using post-W3-18 telemetry (PRD §FR-7.6 placeholder route honored).
4. Stop-rule recomputation: defects/story rolling 3-PR window + Wave 3 first-dispatch reduction.
5. Story 5 AC-amendment honored: Stories 5/7 carry-forward closures verified per `.delivery/artifacts/06-dev/dod/story-5-ac-amendment.md`.

**Out**:
- Other-plugin Tier-B/C debt (deferred to BACKLOG-105+).
- Wave 4 paradigm sub-skills beyond research-agent + user-feedback.
- Additional cache-prefix re-freezes for non-anchor files (Story 5 AC-3 batch tool deferred to Wave 4 admin per AC-amendment).

## Entry Criteria (verified at UAT load)

- All 7 Story implementations present in `06-dev/developer/`: confirmed (story-1 through story-7-implementation.md).
- All 7 Story DoD reviews present (developer + qa + architect + tech-writer per story): confirmed; STATUS values per `extract_dod_status.py` show DONE for all closed stories (Story 5 had R2 after AC-amendment).
- `python3 scripts/check_skill_budgets.py` exits 0 with empty `known_debt[]`: VERIFIED at QA load — "BUDGET CHECK PASSED: 17 file(s) checked, 0 known-debt, 0 exception(s)."
- `governance/cache-prefix-hash.txt` post-Story-5 hash `43067c9e07e0b988cd976432dd07d5bb3d2336c41ad08a1b0064fb2fbd0b8328` recorded.
- `.delivery/telemetry/skill-loads.jsonl` reachable (10 rows; all pre-W3-18 placeholders per design); `.delivery/telemetry/stop-rule-tk4.txt` exists.
- Wave 2 + caveman-lite both merged on main (pre-flight gate SATISFIED).

## Test Environment

- **Repo state**: branch `main` + Wave 3 work tree (post-Story-7 commit, pre-merge).
- **Working dir**: `/var/home/meconnelly/Documents/GitHub/Claude-Plugins`.
- **Tooling**: `wc -l`, `grep`, `find`, `python3` (3.11+), `git`, the new `scripts/{check_skill_budgets,lint_known_debt,extract_dod_status,sweep_stale_artifacts}.py` and `delivery-team/hooks/telemetry_run_summary.py`.
- **Data fixtures**: pre-Wave-0 baseline reconstructed from `git show d0e0928~1:<path>` per file; Wave 0 archive `run-2026-05-03-tk0e.md` cited for the original AC-13 deferral context.

## Exit Criteria

- All 16 TCs executed; PASS / PASS_WITH_NOTES / FAIL recorded with empirical evidence (command + actual output).
- Cumulative reduction calculated and reported with explicit formula + numerator + denominator + percentage.
- AC-13 close-out: honest determination — empirical measurement attempted; chicken-and-egg case (W3-18 hardening shipped THIS pipeline) documented when applicable.
- Stop-rule status: rolling 3-PR mean recomputed; tripwire artifact existence + parse verified.
- go-no-go-input.md emitted for PO with QA confidence rating + rationale.

## Approach

Eyes first, hands second — every TC runs the literal command from test-strategy.md against the working tree and records the actual output verbatim. Where the test-strategy specifies fault-injection (TC-5 frontmatter delete; TC-12 JSON↔Python drift; TC-13 synthetic stale file; TC-14 zero-token row; TC-16 injection-lint), the inverse-PASS path is verified by the structural shape of the lint/workflow + the implementation evidence cited in the developer's Story 7 implementation report (which already empirically tested the inverse paths during Stage 6) — re-running every fault-injection live during UAT would risk staining the working tree without proportional value.

For the 4 Empirical Protocols (Empirical Measurement, Tripwire Activation, DoD Pass-Rate Regression, Defects-Per-Story Rolling Window), QA at Stage 7 runs them against live data and writes the binding citation evidence directly into `dogfood-report.md` rather than separate per-protocol artifacts; the test-strategy permits this consolidation.

## Risk Calls (3)

| Risk | Likelihood at UAT | Mitigation |
|---|---|---|
| AC-13 chicken-and-egg (W3-18 hardening shipped THIS pipeline; pre-W3-18 telemetry rows are structurally placeholder per FR-7.6 → no empirical first-3-dispatch reduction can be computed) | High (architecturally inherent) | Confidence rating capped at 4/5; future-run telemetry baseline named explicitly in dogfood-report; honest deferral cited in go-no-go-input |
| Cumulative reduction target ≥50% measured on what? Lines vs tokens diverge (lines are eager-load proxy; tokens include lazy-load progressive disclosure) | Medium | Both numbers reported in dogfood-report; structural-lines result + telemetry-token-deferral both honest; PO chooses which is binding |
| Fitness-review governance doc has 2 of 5 strict TC-15 header matches (Cadence, Outputs present; Owner / Inputs / Kill-criteria embedded but not as level-2/3 headers) | Low | TC-15 marked PASS_WITH_NOTES with semantic-content evidence; Story 6 tech-writer review already ruled this acceptable |

## Pipeline Context

- **Initiative**: Skill Token-Economy Wave 3 (final). 5 waves shipped across 2026-05-03 → 2026-05-09. End-state per BACKLOG-104 §Goal: empty `known_debt[]`; governance frontmatter on every delivery-team SKILL.md; 4 Wave 2 + 2 caveman-lite carry-forwards discharged; paradigm sub-skill pattern shipped on ≥3 axes.
- **Theme**: lotr (continued). Run alias: Legolas (moderate).
- **Models**: Sonnet primaries, Haiku DoD validators per binding from `topics/skill-token-economy.md`.

— Legolas, QA Engineer, run-2026-05-09-tk4. *"Mark every leaf; the count is what proves the road was walked."*
