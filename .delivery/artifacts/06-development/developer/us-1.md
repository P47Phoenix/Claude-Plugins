# US-1 developer notes

Skills loaded: delivery-team:developer; plugin-dev:skill-development (before prompt-engineer/SKILL.md:368 edit).
Not committed (awaits user approval). Scratch clone /tmp/scratch used for guard cases (committed copy of working tree).

## Edits
- agent_registry.py: S1/S5 provenance comments (148,189), S2 -> claude-sonnet-5, S6 -> claude-opus-5. S3/S4 untouched.
- conftest.py: 4x opus-4-7 -> opus-5 (values only).
- telemetry-schema.md:36 sonnet-5; smoke-test-architecture.md:115 opus-5, :116 sonnet-5.
- prompt-engineer/SKILL.md:368 -> claude-opus-5, date 2026-09-19 (1 add/1 del).
- stale-model-id-guard.yml: rewritten as positive allowlist per stories.md contract (ALLOW, TOK, D, strip-then-regrep, on.paths 7 globs + !.delivery/**).

## Results
| Check | Result |
|---|---|
| AC-01,05,07,11,18 | no output (pass) |
| AC-02 | conftest.py:4 |
| AC-03 | line 36 |
| AC-04 | line 174 only |
| AC-06 | 2 |
| AC-08 | 1 |
| AC-09 / smoke suite | 3 passed |
| AC-10 | 0 |
| AC-16 | 0 |
| AC-19 | 7 |
| AC-21 YAML load | rc 0 |
| AC-23 budgets | exit 0; numstat 1 1 |
| AC-24 | 0 |
| AC-12 clean clone | "No non-allowlisted model IDs found." rc 0 |
| T-N1..N8 | 8/8 rc 1 |
| T-N9 (json-in-md) | rc 1 |
| T-P1..P4 | 4/4 rc 0 |
| T-D1, T-D2 | rc 0; T-D3 rc 1 |
| AC-17 | `#` and `>` rc 0; bare and trailing-comment rc 1 |
| AC-20 scratch.json | scratch.json:1 hit, rc 1 |
| Guard on full tree (worktree) | rc 0 |
| workflow-injection-lint local | OK |
| lint-known-debt local | OK |
| skill-md-header-warn local | rc 0, warning-only; lists pre-existing persona/research-type SKILL.md files, none touched by US-1 |

## Not runnable pre-commit
AC-26, AC-27 (post-commit forms), AC-24 post-commit form, AC-23 post-commit form. AC-12/27 must be re-run on HEAD clone after commit.
No derived artifacts to regenerate (no cache-prefix files touched, BC-10).
No PRD AC found wrong.
