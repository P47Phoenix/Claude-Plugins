# QA DoD Review: Development (US-1..US-3, PR #88 model-ID guard)

Status: DONE. 28/28 ACs PASS. No FAIL, no must-fix.

Method: ran each AC on live working tree (WT). Post-commit ACs run in scratch clone `/tmp/qa` (clone of worktree, `git apply` diff, untracked copied, one commit `fbf9a34` atop 337edb5). Guard runner `/tmp/g.sh` extracted verbatim from workflow `steps[1].run`. AC count confirmed: FR table 4+2+2+2+1+5+2+3+1+3+3 = 28 (AC-01..AC-28).

## Per-AC results

| AC | Where | Expected | Actual | Result |
|---|---|---|---|---|
| 01 | WT | no output | none (rc 1) | PASS |
| 02 | WT | conftest.py:4 | `conftest.py:4` | PASS |
| 03 | WT | line 36 | `telemetry-schema.md:36` | PASS |
| 04 | WT | line 174 | `agent_registry.py:174` | PASS |
| 05 | WT | no output | none | PASS |
| 06 | WT | 2 | 2 | PASS |
| 07 | WT | no output | none | PASS |
| 08 | WT | >=1 | 1 | PASS |
| 09 | WT+clone | 3 passed | 3 passed | PASS |
| 10 | WT (git diff) + clone (git show) | 0 | 0 / 0 | PASS |
| 11 | WT | no output, rc 1 | none, rc 1 | PASS |
| 12 | clone | msg + 0 | `No non-allowlisted model IDs found.` 0 | PASS |
| 13 | clone | 8 IDs + json line rc 1 | all 9 rc 1 | PASS |
| 14 | clone | 4 allowed rc 0 | all rc 0 | PASS |
| 15 | clone | haiku-20251001 0; multi 0; opus-5.1 1 | 0, 0, 1 | PASS |
| 16 | WT | 0 | 0 | PASS |
| 17 | clone | `#`/`>` 0; bare 1; mid-line 1 | 0,0,1,1 | PASS |
| 18 | WT | no output rc 1 | none, rc 1 | PASS |
| 19 | WT | 7 | 7 | PASS |
| 20 | clone | scratch.json hit, rc 1 | `scratch.json:1:...` rc 1 | PASS |
| 21 | WT | 0 | 0 | PASS |
| 22 | WT | 0, no MISSING | 0, none | PASS |
| 23 | WT+budgets; clone | budget rc 0; `1 1` | PASSED 17 files rc 0; `1 1` both | PASS |
| 24 | clone (337edb5..HEAD) | 0 | 0 | PASS |
| 25 | WT | >=1 | 2 | PASS |
| 26 | clone | 2 and 1 | 2 and 1 (plain rev-list also 1) | PASS |
| 27 | clone HEAD | msg + 0 | msg + 0 | PASS |
| 28 | WT / clone | >=1 ; 0 | 2 ; 0 | PASS |

## Guard matrix (single line appended to root README.md in clone)

- 8 stale, exit 1: claude-opus-4-7, sonnet-4-6, sonnet-4-5, opus-4-8, opus-5.1, haiku-4-5, sonnet-4-5-20250929, opus-4-20250514 -> all 1.
- JSON-style `{"model": "claude-opus-4-7"}` in README.md -> 1.
- Allowed 4 (fable-5-1, opus-5, sonnet-5, haiku-4-5-20251001) -> all 0.
- Trailing punct: `opus-5.` 0, `opus-5,` 0, `haiku-4-5-20251001.` 0, multi-ID list 0, `opus-5.1` 1, `opus-5.1.` 1.
- `# prior: ...opus-4-8` 0; `> prior: ...opus-4-8` 0; bare `prior: ...` 1; `MODEL = "claude-sonnet-5"  # prior: claude-opus-4-7` 1 (mid-line comment not exempt).
- Root README.md injection detected (exit 1): no F-1 false pass.
- scratch.json tracked injection -> `scratch.json:1` exit 1.
- After cleanup: clean tree exit 0.

## Other
- Smoke tests: 3 passed (WT and clone).
- `scripts/check_skill_budgets.py`: PASSED, 17 files, 0 debt, rc 0.

## Notes (non-blocking)
- Post-commit ACs simulated with a single commit incl. `.delivery` files; AC-26 uses `:!.delivery` pathspec so a separate artifacts commit still counts 1.
- AC-25 dev-notes.md and AC-22 verification file present as untracked; they must be staged in the ship commit(s).
