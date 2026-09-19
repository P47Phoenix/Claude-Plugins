# Developer DoD Review: model-ID migration (PR #88)

Verdict: PASS (all criteria). No must-fix.

| # | Criterion | Result | Evidence |
|---|---|---|---|
| 1 | PRD per-site map S1-S14 migrated | PASS | agent_registry.py sonnet-4-6->sonnet-5, opus-4-7->opus-5, haiku line 174 untouched; conftest x4 opus-5; telemetry-schema:36 sonnet-5; smoke-arch opus-5/sonnet-5; prompt-engineer:368 opus-5 |
| 2 | Role tier preserved | PASS | opus->opus-5, sonnet->sonnet-5, haiku unchanged |
| 3 | Fable allowlisted, not adopted | PASS | `git grep claude-fable` outside guard/CHANGELOG/.delivery: none; ALLOW has fable-5-1 |
| 4 | Code clean, no stray live old IDs | PASS | git grep of live 4.x IDs outside # / > lines: none; only ID literals changed |
| 5 | Provenance comments correct | PASS | S1, S5 comments dated 2026-09-19, record prior IDs; prompt-engineer example date bumped with ID |
| 6 | Guard YAML well-formed | PASS | yaml.safe_load OK; on.pull_request.paths valid globs, `!.delivery/**` last |
| 7 | No github.event.* in run, no claude CLI | PASS | grep: 0 hits; workflow-injection-lint OK |
| 8 | ALLOW single-source | PASS | one `ALLOW=` def; strip regex uses $ALLOW |
| 9 | Guard run block on tree | PASS | exit 0 "No non-allowlisted model IDs found." |
| 9b | Guard negative test (temp repo) | PASS | flags opus-4-7, sonnet-5.1, opus-5-foo; accepts `opus-5.` (exit 1 overall as expected) |
| 10 | pytest delivery-team/tests/smoke | PASS | 3 passed |
| 11 | check_skill_budgets.py | PASS | 17 files, 0 debt, 0 exceptions |
| 12 | lint-known-debt cmd | PASS | LINT OK |
| 13 | skill-md-header-warn cmd | PASS | runs; warning-only by design (job never fails); needs GITHUB_OUTPUT/STEP_SUMMARY env locally |
| 14 | workflow-injection-lint cmd | PASS | OK |
| 15 | py_compile changed .py | PASS | agent_registry.py, conftest.py exit 0 |
| 16 | CHANGELOG | PASS | Unreleased entry added, history untouched |

Notes (non-blocking): guard excludes itself from scan (by design, holds ALLOW). CHANGELOG names claude-fable-5-1 on a non-blockquote line; CHANGELOG is excluded from FR-3 AC and guard allowlists it.

## Derived Artifacts
- .github/workflows/stale-model-id-guard.yml (rewritten guard)
- CHANGELOG.md (Unreleased entry)
- .delivery/artifacts/06-development/developer/us-1.md, dev/dev-notes.md, po/us-4-notes.md, qa/model-id-verification.md
- .delivery/backlog/BACKLOG-108..112
- scratch only under /tmp/g (no repo edits)
