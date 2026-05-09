<!-- run: run-2026-05-09-tk4 | stage: 6 (Development, full) | story: 7 admin / carry-forward closure | author: Gimli, Developer -->

# Story 7 Implementation — Admin / Carry-Forward Closure

*Gimli son of Glóin, Developer. Six small forge-strikes. The wave is closed; the carry-forwards are discharged; the telemetry runs straight.*

## Engagement

- **Pipeline**: `run-2026-05-09-tk4` — Wave 3 closure, Story 7 (last).
- **Scope**: 6 work items (W3-13..W3-18) + housekeeping verification.
- **Inputs**: Story 7 directive (`05-plan/po/stories.md` §Story 7); Story 5 AC-amendment; tk3 retro (W3-17/18 source); tk2 retro (W3-13/14/15/16 source); architecture-tk4-wave-3.md §Stop-Rule Tripwire Mechanics.
- **Constraints honored**: SKILL.md at-cap (499/500) — all SKILL.md-adjacent additions land in `references/`. No state.md modification. No other-Story file edits.

## Per-WI Implementation Table

| WI | Type | Deliverable | LOC | Verification |
|----|------|-------------|-----|--------------|
| W3-13 | new ref | `delivery-team/skills/delivery-flow/references/validator-prompt-template.md` (89 lines, spec-vs-impl framing + canonical-paths block) | 89 | exists; quality-gates.md has 1-line pointer to it |
| W3-13 | edit | `delivery-team/skills/delivery-flow/references/quality-gates.md` (+1-line pointer to template) | +1 | grep finds reference |
| W3-14 | new script | `scripts/lint_known_debt.py` (138 lines; verifies JSON↔Python KNOWN_DEBT consistency + Story-5 deferred frontmatter rollout completeness) | 138 | exit 0 clean |
| W3-14 | sync | `scripts/check_skill_budgets.py` KNOWN_DEBT cleared (post-Story-5 baseline; 7 entries removed; SoT now JSON registry) | -55 | budget check exit 0 (17 files, 0 known-debt) |
| W3-14 | new CI | `.github/workflows/lint-known-debt.yml` (32 lines; PR + push triggers; PR_BODY env-pattern correctness; DEFECT-004 guard PASS) | 32 | YAML valid; no `${{ github.event.* }}` in `run:` |
| W3-15 | new script | `scripts/extract_dod_status.py` (helper-script approach per directive: handles `STATUS:`, `**Status**:`, `**Gate Status**:`, YAML-quoted, pipe-separated variants) | 100 | 5/5 sample DoD reviews extract cleanly; 49/50 corpus extract (1 producer-format defect, not a parser miss) |
| W3-16 | new hook | `.githooks/pre-commit` (executable; runs `check_skill_budgets.py` + `lint_known_debt.py`; bypassable via `--no-verify`) | 41 | bash syntax OK; install instructions in `governance/git-hooks-install.md` + 1-line pointer in CLAUDE.md |
| W3-16 | new doc | `governance/git-hooks-install.md` (one-time `git config core.hooksPath .githooks` + bypass + uninstall) | 49 | exists |
| W3-17 | new script | `scripts/sweep_stale_artifacts.py` (Option A banner default; Option B archive opt-in; idempotent; always exits 0) | 130 | dogfood: identifies 13 tk3-stale files in `07-uat/` (verified, then reverted — not Story 7 scope to write to those artifacts); synthetic-fixture test confirms banner + idempotency + fresh-skip |
| W3-17 | edit | `delivery-team/skills/delivery-flow/references/pipeline-stages.md` Stage-7 entry-step (DEFECT-006 systemic fix; Option A per architect §Open questions #3) | +14 | section "Entry Step: Stale-Artifact Sweep (DEFECT-006 systemic fix, W3-17)" present |
| W3-18 | edit | `delivery-team/hooks/telemetry.py` (`placeholder=true` marker per FR-7.6; pipeline_id capture from env or hook input; prose_tokens / input / cache fields enriched when measurement is present) | +30 | unit test: empty input → placeholder=true; prose_tokens=1500 → placeholder=false; pipeline_id captured |
| W3-18 | new script | `delivery-team/hooks/telemetry_run_summary.py` (per-run summary emitter; legacy 0-token rows treated as placeholders; `placeholder_only` signal for tripwire fallback) | 113 | run-2026-05-09-tk4 summary written; 10 rows / 10 placeholder / placeholder_only=true (correct: pre-W3-18 telemetry is structurally placeholder) |
| W3-18 | new artifact | `.delivery/telemetry/stop-rule-tk4.txt` (Story 5 AC-5 carry-forward closure; documents chicken-and-egg case + first-effective-baseline-next-run) | 35 | exists; per-run summary at `run-summary-run-2026-05-09-tk4.json` referenced |
| housekeeping | re-baseline | `governance/skill-budgets.json` `known_debt[]` confirmed empty (cleared at Story 5 W3-9; verified post-Story-7 via JSON load) | 0 | `python3 -c '...known_debt==[]'` exits 0 |

**Totals**: 8 new files, 5 edited files, 0 deleted. Net +665 lines (mostly references + scripts). SKILL.md untouched (499/500 held).

## Verification (10 commands, all passing)

```
1. test -f delivery-team/skills/delivery-flow/references/validator-prompt-template.md       → PASS (89 lines)
2. python3 scripts/lint_known_debt.py                                                       → exit 0 ("LINT OK: known_debt JSON↔Python in sync; all SKILL.md frontmatter complete.")
3. python3 -c "import yaml; yaml.safe_load(open('.github/workflows/lint-known-debt.yml'))"  → YAML OK
4. grep -nE '\${{\s*github\.event\.' .github/workflows/lint-known-debt.yml                  → no match (DEFECT-004 guard PASS)
5. test -f scripts/extract_dod_status.py + 5-sample DoD review extract                       → 5/5 STATUS values extracted (DONE × 3, PASS × 2)
6. test -f .githooks/pre-commit                                                              → PASS (executable; bash -n syntax OK)
7. test -f scripts/sweep_stale_artifacts.py                                                  → PASS; --help renders
8. test -f .delivery/telemetry/stop-rule-tk4.txt                                             → PASS (Story 5 AC-5 closure)
9. python3 scripts/check_skill_budgets.py                                                    → exit 0 ("BUDGET CHECK PASSED: 17 file(s) checked, 0 known-debt, 0 exception(s).")
10. python3 -c "import json; d=json.load(open('governance/skill-budgets.json')); assert d.get('known_debt',[]) == []; print('clean')"  → "clean"
```

## Cache-prefix impact

ZERO impact across all 6 WIs. Verified by:

- `delivery-team/skills/delivery-flow/SKILL.md` line count UNCHANGED at 499/500 (Tier-A held exactly, with 1 line headroom intentionally preserved per architect §"Stage 7 entry sweep" Open question #3 + caveman-lite Tier-A binding).
- All W3-13 + W3-17 prose lands in `references/quality-gates.md` (now 292 lines) and `references/pipeline-stages.md` (now 708 lines) — both well past byte 2048, outside the cache-prefix region per ADR-tk1-002 boundary.
- New scripts (`lint_known_debt.py`, `extract_dod_status.py`, `sweep_stale_artifacts.py`, `telemetry_run_summary.py`) and the new workflow + hook do not participate in the SKILL.md prefix region at all.
- `governance/cache-prefix-hash.txt` — UNTOUCHED by Story 7 (last regenerated at Story 5 W3-9 end, hash `43067c9e...`).

## Adversarial-mode notes (defensive coverage applied)

1. **W3-14 lint catches BOTH directions of drift** — entries only in JSON OR only in Python both flagged ("DRIFT (JSON-only)" / "DRIFT (Python-only)"). Tested empirically: removing one source produces non-zero exit with named entry.
2. **W3-15 extractor is forgiving but not lenient** — accepts 6 historical format variants (canonical, **Status**, **Status**:**DONE**, plain Status, pipe-separated `... | **Status:** DONE`, `**Gate Status**:`, YAML-quoted `status: "PASS"`) but only matches a closed STATUS-token vocabulary (DONE / NOT_DONE / CODE_COMPLETE / PASS_WITH_NOTES / PASSED / PASS / FAIL). Does not match arbitrary "PASSED-the-test" prose.
3. **W3-16 hook fails LOUD when budget breached, silent when clean** — non-zero exit blocks commit, error message names the bypass syntax (`--no-verify` + `Budget-Exception:` PR-body token) so committers know the intentional escape hatch.
4. **W3-17 sweep is NEVER destructive by default** — banner mode (Option A) prepends a marker line; archive mode (Option B) is opt-in via `--mode archive`. Idempotent in both modes. Always exits 0 (entry-step warning, not gate).
5. **W3-18 telemetry distinguishes legacy-zero-token rows from PostToolUse-enriched rows** — pre-W3-18 rows lack the `placeholder` field; helper `_is_placeholder` treats them as placeholder by structural inference (zero/absent prose_tokens). Prevents false-baseline computation on the chicken-and-egg first run.

## Self-DoD against Story 7 ACs (5 ACs)

| AC | Description | Status | Evidence |
|----|-------------|--------|----------|
| AC-1 | [W3-13 + W3-15] validator-prompt-template + STATUS-format standardized — 5/5 sample DoD STATUS extracts cleanly | DONE | Template at `references/validator-prompt-template.md`; pointer in `quality-gates.md`; `extract_dod_status.py` extracts 5/5 sample DoD reviews; 49/50 historical corpus (98%) — single miss is producer-format defect (`**CONDITIONAL PASS**` with no Status: prefix), not a parser gap |
| AC-2 | [W3-14 + W3-16] CI workflow runs on PR + push to main; workflow-injection-lint passes; pre-commit hook fails commit on budget breach | DONE | `.github/workflows/lint-known-debt.yml` triggers on `pull_request` + `push: main`; YAML-valid; no `${{ github.event.* }}` in `run:` block (uses env-passed pattern correctly via the script-only step); `.githooks/pre-commit` runs `check_skill_budgets.py` + `lint_known_debt.py`; install via `git config core.hooksPath .githooks` |
| AC-3 | [W3-17] Stage-7 entry-step prescribed; synthetic stale Wave-N-1 file triggers banner; DEFECT-006 closes upon merge | DONE | `pipeline-stages.md` §"Entry Step: Stale-Artifact Sweep (DEFECT-006 systemic fix, W3-17)" added; `sweep_stale_artifacts.py` banner mode default (Option A per architect §Open questions #3); synthetic-fixture test PASSED (1 stale → BANNERED; fresh → skipped; idempotent on re-run); live-dogfood smoke test against current `07-uat/` identified 13 tk3-stale files (sweep verified, then reverted — out of Story 7 scope to ship modifications to other-stories' artifacts; orchestrator at next Stage 7 entry will perform the live sweep) |
| AC-4 | [W3-18] Telemetry hook either fails-loud OR marks zero-token rows `placeholder=true`; W3-10 KPI compute correctly excludes placeholder rows | DONE | `telemetry.py` updated: `placeholder=true` set when no measurement present (FR-7.6 route); `telemetry_run_summary.py` excludes `placeholder=true` rows + treats legacy zero-token rows as placeholders; unit tests confirm both behaviors; per-run summary at `run-summary-run-2026-05-09-tk4.json` correctly reports 10/10 rows as placeholder (pre-W3-18 baseline state, expected); `placeholder_only: true` signals tripwire to fall back to baseline (chicken-and-egg case documented in `stop-rule-tk4.txt`) |
| AC-5 | [Housekeeping] `known_debt[]` post-Story-7 empty; `check_skill_budgets.py` exits 0 for delivery-team scope | DONE | `governance/skill-budgets.json known_debt[] == []`; `scripts/check_skill_budgets.py` `KNOWN_DEBT = []` (synced); `python3 scripts/check_skill_budgets.py` exits 0 ("17 file(s) checked, 0 known-debt"); first time `known_debt[]` baselines empty since BACKLOG-100 |

**All 5 ACs PASS.** DEFECT-006 closure: pending orchestrator adoption of the new Stage-7 entry-step (procedure + helper now exist; closure conditional on orchestrator dispatch of `sweep_stale_artifacts.py` at next Stage 7 entry per the references/pipeline-stages.md prescription).

## Story-5 deferred carry-forward closures

Per `.delivery/artifacts/06-dev/dod/story-5-ac-amendment.md`:

- **Story 5 AC-1 lint script** → CLOSED by W3-14. `scripts/lint_known_debt.py` includes the deferred frontmatter rollout completeness check; verifies all 11 top-level `delivery-team/skills/*/SKILL.md` have `maintainer:` + `fitness_review_due:` + `context_budget:` + `tier:` keys, AND that `context_budget` matches the tier ceiling per `governance/skill-budgets.json tiers` (A=500 / B=300 / C=200). Pre-implementation audit confirmed all 11 files compliant; lint exit 0.
- **Story 5 AC-3 multi-file hash batch tool** → DEFERRED (out of scope for the Story 7 directive; cache-prefix anchor for `delivery-flow/SKILL.md` was already regenerated at Story 5 W3-9 end with hash `43067c9e...`; the multi-file batch tool is a Wave 4 item if/when other SKILL.md cache-prefix-impacting changes batch).
- **Story 5 AC-5 tripwire artifact** → CLOSED by W3-18. `stop-rule-tk4.txt` + `telemetry_run_summary.py` shipped; the artifact documents the chicken-and-egg case explicitly (telemetry hardening shipped THIS pipeline → no pre-W3-18 measurements can fire the tripwire) and names the next-run effective baseline. Future runs auto-generate `stop-rule-<pipeline-id>.txt` via the summary script at orchestrator's Stage 7 Post-Acceptance step.

## Wave 2 + caveman-lite carry-forwards (full register)

Cross-referenced against tk2 retro §"Action items" + tk3 retro §"Self-Improvement Actions for Next Wave":

| # | Action (source) | Owner | Status post-Story-7 |
|---|-----------------|-------|---------------------|
| tk2-1 | Standardized validator-prompt template citing canonical paths + spec-vs-impl framing | Architect | DISCHARGED (W3-13) |
| tk2-2 | CI lint validating JSON ↔ Python KNOWN_DEBT consistency | DevOps | DISCHARGED (W3-14) |
| tk2-3 | Standardize DoD review STATUS line format OR adopt flexible regex | TW | DISCHARGED (W3-15 flexible-regex helper per directive cheapness ruling) |
| tk2-4 | Pre-merge git hook for skill-budget local check | Gimli | DISCHARGED (W3-16) |
| tk2-5 | File issue: plugin-dev:skill-development invocation pattern | PO | DEFERRED (PO-owned post-Wave-2 item; not Story 7 scope) |
| tk3-1 | Stage 7 entry — stale-artifact sweep (DEFECT-006 systemic fix) | Architect + Dev | DISCHARGED (W3-17) |
| tk3-2 | Telemetry hook output quality hardening (no zero-token placeholder rows; fail-loud or placeholder marker) | DevOps | DISCHARGED (W3-18) |

**6 of 7 carry-forwards DISCHARGED on Story 7 (the wave that produced them).** The single deferral (tk2-5) is PO-owned and out of developer scope.

## Files Touched (Story-7 scope only)

**New files (8)**:
- `delivery-team/skills/delivery-flow/references/validator-prompt-template.md`
- `scripts/lint_known_debt.py`
- `.github/workflows/lint-known-debt.yml`
- `scripts/extract_dod_status.py`
- `.githooks/pre-commit`
- `governance/git-hooks-install.md`
- `scripts/sweep_stale_artifacts.py`
- `delivery-team/hooks/telemetry_run_summary.py`
- `.delivery/telemetry/stop-rule-tk4.txt`
- `.delivery/telemetry/run-summary-run-2026-05-09-tk4.json` (auto-generated)

**Edited files (5)**:
- `delivery-team/skills/delivery-flow/references/quality-gates.md` (+1-line pointer to validator-prompt-template.md)
- `delivery-team/skills/delivery-flow/references/pipeline-stages.md` (+14-line Stage-7 entry-step section)
- `scripts/check_skill_budgets.py` (KNOWN_DEBT cleared; comment updated to point to JSON SoT)
- `delivery-team/hooks/telemetry.py` (placeholder + pipeline_id + measurement-enrichment hardening)
- `CLAUDE.md` (+1 line under Permissions: pre-commit install pointer)

**No SKILL.md edits.** No state.md edits. No other-story file edits.

## SKILL_LOADED signals

Both bindings honored:
- `SKILL_LOADED: delivery-team:developer` — emitted at task entry per orchestrator binding
- `SKILL_LOADED: plugin-dev:skill-development` — invoked per pre-load directive (delivery-flow references/ edits in W3-13 + W3-17)

— Gimli, Developer, run-2026-05-09-tk4. *"Six strikes; six rings forged. The wave is sealed."*
