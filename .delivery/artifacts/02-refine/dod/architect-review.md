# Architect DoD Review — Stage 2 Refine, BACKLOG-108 PRD Revision 4

Validator role: Architect (technical feasibility, no obvious blockers). Gate 2 / Architect section. Judged target-vs-current: is the PRD well-formed and feasible, not whether ACs pass today.
Inputs read: prd.md (all 771 lines), constraints.yml; repo source checked: `.github/workflows/stale-model-id-guard.yml`, `.githooks/pre-commit`, `delivery-team/tests/smoke/lib/{metrics,baseline,runner}.py`, `run_smoke.py`, `governance/cache-prefix-hash.txt`, local `claude --help`.

## Gate-result table

| Criterion | Result | Class |
|-----------|--------|-------|
| Central alias design (`MODEL_TIER_ALIAS`, CLI aliases vs API IDs, one config value for API callers, FR-4.5 evidence) | PASS | - |
| Single guard script `scripts/check_model_pins.py`, patterns, self-scan cleanliness, workflow triggers push/pull_request/workflow_dispatch, no `paths:` filter | PASS | - |
| Local ship gate for a no-PR direct push (FR-1.5, FR-7.3) | PASS with warning (F1, F2) | warning |
| Smoke runner `--model`/`--effort` (both flags exist in local CLI 2.1.278 help) | PASS | - |
| Observed `system/init` model capture, `unknown` failure rule, consistency rule | PASS with warning (F3, F4) | warning |
| Parser fix for `unknown` bucket and real-shape fixture with provenance sidecar | PASS with warning (F3, F6) | warning |
| Baseline schema changes (`model_requested`, `model_resolved`, `model_pin_env`, `effort`, `host_context`) | PASS with warning (F4, F5) | warning |
| Cache fingerprint handling and byte-stability constraint | PASS with warning (F7) | warning |
| Story ordering S1..S7 and dependencies | PASS with warning (F2) | warning |
| CI/governance constraints (line budgets, KNOWN_DEBT lint, existing workflows, injection lint) | PASS | - |
| No blocking design hole | PASS (no blocker found) | - |

## Findings

1. **[Warning] Guard self-scan and fixtures verified feasible.** Inspected each of the four pattern strings against itself: none matches its own literal text (for example `PIN_RE` has `[` after `claude-`, so no digit or `-latest` follows), the fixture JSON is outside scope, and the workflow only names the script. AC-1.2c is achievable. No change required. Recorded so later stages do not re-derive it.

2. **[Warning] Opt-in pre-commit hook will block WIP commits from S1 until S4 (FR-1.5(b), story order).** The existing `.githooks/pre-commit` exits 1 on violation. Once the guard call is added in S1, every commit in S1..S3 fails while the tree still has hits (91 today, falling to 0 only at S4), for any clone with `core.hooksPath` set (this worktree currently uses the default `.git/hooks`, so it is not affected, but the maintainer's main clone may be). Required fix: FR-1.5 must state the behaviour in the interim, either (a) hook prints the hit count and blocks only when the `--paths` scan of staged files hits (staged-file scoping), or (b) S1 to S3 WIP commits use `--no-verify` and the S1 report records that. Option (a) is preferred and keeps the ship-time gate strict by running the full scan in FR-7.3.

3. **[Warning] Cost cap cannot trigger on a real stream (FR-5.4, FR-5.9).** `lib/runner.py:38-48` `_running_cost` sums `usage.cost_usd` per event and is used at lines 95 and 252 to kill the run. The real stream carries cost only as `total_cost_usd` on the final `result` event, so mid-stream enforcement never fires; the cap becomes a post-hoc check at best. FR-5.4/FR-5.9 fix only `metrics.py` and do not name `runner.py`. Required fix: name `runner.py` `_running_cost` in FR-5.9 scope, and additionally pass the CLI's own `--max-budget-usd <cost-cap>` (present in local `claude --help`) so the cap is enforced by the CLI during the run. Add an AC that the constructed command line contains it. Also add `runner.py` to the BC-07 producer list.

4. **[Warning] Baseline comparison keyed on dynamic model names (FR-5.1, `baseline.py`).** `model_usage.<model>.dispatches` keys vary with the resolved model. `_check_hard_rules` reports "missing from report" for hard-classed keys, and `_classify` treats all non-listed keys as advisory, so behaviour depends on `HARD_METRIC_KEYS`. When the model legitimately changes, the old key vanishes and a new one appears. Required fix: FR-5.7 should state that `model_usage.*` keys are excluded from per-key threshold comparison (compared as a set, or reported only via the `model moved` WARN), and an AC-5.7 case should cover a baseline and run with different model keys and `--strict-model` unset yielding exit unchanged with no spurious missing-key failure.

5. **[Warning] Plumbing of new fields through report and aggregator is unstated (FR-5.5).** `model_resolved` needs the `system/init` event, which `parse_stream` currently ignores (it only handles events with usage), and must reach per-sample reports so `init_baseline(reports, ...)` can run the consistency rule. `report.py`/`aggregator.py`/`runner.py` are not named as changed files; `_collect_metric_values` is numeric-only, so list and object fields (`model_resolved`, `model_pin_env`, `host_context`) need explicit top-level handling. Required fix: list the files touched in S5 (`metrics.py`, `runner.py`, `report.py`, `baseline.py`, `run_smoke.py`) and state that the new fields are copied top-level, not aggregated as numeric metrics.

6. **[Warning] Provenance sidecar and S5 docs fall inside guard scope (FR-5.10).** `stream_real_shape.provenance.txt` is `.txt` (scanned); `.jsonl` and `.json` are not. If the sidecar or README/ARCHITECTURE text records the concrete observed model ID (the PO capture shows a dated Haiku ID), the guard fails at S5. Required fix: add one line to FR-5.10 that the sidecar records the command and CLI version only, never a concrete model ID (the ID is already in the `.jsonl`), and that smoke docs describing `model_resolved` use synthetic examples.

7. **[Warning] Cache fingerprint byte-stability has one uncovered ordering risk (FR-6.1, FR-7.3).** `governance/cache-prefix-hash.txt` is checked only manually (no CI or hook consumer found), so nothing catches a later edit to `delivery-team/skills/delivery-flow/SKILL.md`. S6 sits before S7, yet S7 (memory, changelog, ship rebase) and any DoD-driven rework after S6 could touch it, silently breaking the frozen hash. Also `orchestrator-doctrine.md` mirrors the same 4.7 block and is edited in S2 but is outside the fingerprint scope (OQ-3). Required fix: add AC-6.1 to the FR-7.3 pre-push list, and have the ADR (FR-6.2) state explicitly whether the shared mirror is in scope. Pre-existing content-hash design is otherwise sound: the version-free file removes future churn.

8. **[Warning] `model-pin-ok` escape hatch is effectively unusable (FR-1.2 vs FR-1.6, R4/R12).** The marker is an allowlisted per-line escape, yet AC-1.6 forbids any use outside the script, and AC-1.6 is a ship-time local check, not CI. A future legitimate hit (for example a prose sentence such as "in 4.5 minutes", matched by BARE_RE with major 4 to 9) has no sanctioned escape and no CI-enforced rule about the marker. Required fix: either state that legitimate future hits must be rephrased (marker reserved for the fixtures' documentation), or make the workflow also run the AC-1.6 check so the policy is symmetric.

9. **[Warning] Tracked-tree versus `os.walk` scope difference.** FR-1.2 says the script scans the tracked tree; the canonical command uses `os.walk` (includes untracked files). New files (the script itself, fixtures, ADR, new docs) are untracked until `git add`, so the local ship gate and the canonical count can disagree. Required fix: in FR-7.3 require the gate to run after staging, or define the script to scan `git ls-files` plus untracked-not-ignored (`--others --exclude-standard`), and note the equivalence check for R12.

10. **[Suggestion] Story order S1..S7 is sound.** Dependencies check out: S1 script precedes AC-3.1b/AC-2.1 users; S3 stamps after prose (BINDING-2.3); S6 after all SKILL.md edits; S4 fixtures precede S5 validator tests. AC-2.1 and AC-2.5 use `git show main:` / `git diff main`, valid only before ff-merge; state that these ACs are evaluated pre-ship (FR-7.3 already orders them before the push).

11. **[Suggestion] OQ-11 (frontmatter `model: sonnet` vs Opus-conditional guidance).** Architect confirms the PO decision as feasible: leave frontmatter unchanged, conditional phrasing, spawn cap valid for any model. Nothing blocks Stage 4 on this.

12. **[Suggestion] OQ-5/OQ-12.** `xhigh` is acceptable (thinking-on cost risk R6 is bounded once finding 3 is fixed). Default no `--bare` is acceptable given billing-path change; `host_context` recording is the right mitigation.

## Verdict

PASS with 9 warnings, 0 blocking. The alias design, single guard script, triggers plus local ship gate, smoke-runner flags, observed-model capture, cache-fingerprint handling and story ordering are technically feasible. Findings 3 to 6 are design holes in S5 that the developer will hit and should be written into FR-5.4/5.5/5.7/5.9/5.10 before Stage 6; findings 2, 7, 8, 9 tighten the guard and ship path. None requires re-scoping.
