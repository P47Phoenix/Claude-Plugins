run: run-2026-05-28-o48m
story: S1 Guard (BACKLOG-108), devops review of commit 6560e64
reviewer: devops (independent of producer). Read-only. Skills loaded: delivery-team:operations, plugin-dev:hook-development (acknowledged).

# Verdict

`S1_DEVOPS: APPROVE` (no blocking defects; 3 non-blocking notes)

# Checks (raw evidence)

| Check | Result |
|---|---|
| actionlint on changed files | clean. Whole-dir run flags only pre-existing `workflow-injection-lint.yml` (SC2086, SC2181, expr type). Not touched by S1. |
| YAML parse, all 9 workflows | `yaml.safe_load` ok on all |
| Guard triggers | `push: branches:[main]`, `pull_request`, `workflow_dispatch`. No path filter. Good, cannot skip SKILL.md changes |
| Budget triggers | `push: branches:[main]` added; PR keeps paths `delivery-team/**/SKILL.md`, `governance/skill-budgets.json`. Matches script scope (`glob delivery-team/**/SKILL.md`) |
| `permissions: contents: read` | both workflows |
| `persist-credentials: false` | both checkouts |
| `${{ github.event.* }}` in run: | none. Only one in budget workflow, under `env:` (`PR_BODY`), not `run:`. Simulated injection-lint regex: passes |
| CLI agent invocation in CI | none (`claude` string absent in both files, python scan) |
| `set -uo pipefail` in run steps | no `-e`, so python rc not lost; last command in each step is the python call, step rc = python rc. Correct |
| PR_BODY on push | expression is empty string; `check_pr_body_exception()` uses `os.environ.get("PR_BODY","")`, so no crash, no exception granted. OK |
| Exec bits | `100755` for `.githooks/pre-commit`, `.githooks/pre-push`, `scripts/check_model_pins.py` |
| Hooks installed? | NO. `core.hooksPath` = `<repo>/.git/hooks` (default) in shared `.git/config`. Deviation confirmed: shared config untouched, hooks inert |

# Hook tests (temp repos under $CLAUDE_JOB_DIR/tmp, `git -c core.hooksPath=<abs>/.githooks`)

Script: `/home/meconnelly/.claude/jobs/af2deffc/tmp/ht.sh`. Temp dirs removed.

pre-commit:
- clean staged file: `guard-scope hits 0`, `budget + lint OK`, rc 0
- `--allow-empty` (zero staged): no abort under `set -euo pipefail`, rc 0 (PA-5 ok)
- staged pin, default: `pin a/SKILL.md:1 ... advisory`, commit succeeds, rc 0
- staged pin, `MODEL_PIN_STRICT=1`: `MODEL PIN VIOLATION - commit blocked`, rc 1

pre-push (stdin ref lines):

| Case | Strict=1 | Advisory |
|---|---|---|
| empty stdin | rc 0 | - |
| non-main ref | rc 0 | - |
| delete main (local sha zero) | rc 0 | - |
| main clean | guard + budgets run, rc 0 | - |
| sha not HEAD | rc 1 | rc 0 + warning |
| dirty tree | rc 1 | rc 0 + warning |
| untracked only under `.claude/worktrees/` | rc 0 (pathspec works, guard ran) | - |
| guard fail (tracked pin) | rc 1 | rc 0 + warning |
| multi refs, non-main then main | main handled, rc 1 on guard fail | - |
| last line without trailing newline | rc 0, guard NOT run (see N1) | - |

Matches PA-7's 7 stub cases. Note in advisory mode after a guard failure the budget check still runs (good, both reported).

# Current-tree behavior

- Guard: `python3 scripts/check_model_pins.py --list` now prints `files-scanned 486`, `guard-scope hits 85 files 30`, rc 1. Workflow would be RED on any PR or main push now. Expected: S2 (keystone prose), S3, S4 reword hits; turns green when S4 reaches zero hits (AC-1.2c / AC-1b). Also base floor `B=485` in base-sha.txt; 486 >= 485 ok. Hits are in `prompt-engineer/SKILL.md`, `research-agent/SKILL.md` etc. (prose/stamp/pin).
- Budget: `BUDGET CHECK PASSED: 17 file(s) checked` rc 0. Green now.
- Do not merge or push to main before S4 or the post-push run is red (PA-26 would FAIL). Ship gate ordering in plan already covers this.

# Defects

Blocking: none.

Non-blocking:
- N1 (pre-push, low): `while read -r ...` skips a final line with no trailing newline (read returns 1 at EOF). Git always sends newline-terminated lines, so real pushes are unaffected. Repro: `printf 'refs/heads/main <HEAD> refs/heads/main 000..0' | MODEL_PIN_STRICT=1 .githooks/pre-push` on a tree with a pin gives rc 0. Fix if wanted: `while read -r a b c d || [ -n "$a" ]; do`.
- N2 (budget workflow, info): on push to main, PR body is empty, so a PR merged with `Budget-Exception:` would make the main-push run red. Design tradeoff; document in S7 handoff. Also PR path filter does not cover `scripts/check_skill_budgets.py` edits (pre-existing).
- N3 (guard workflow, info): step has `set -uo pipefail` only and no `-e`; fine for a single command, but adding a second command later needs explicit rc handling. Also the pre-commit budget/lint failure hints reference `--no-verify` (pre-existing text).

# Hand off to S7 / human

1. Hooks are inert here: `core.hooksPath` not set (PA-9 said `--local` would write shared `.git/config`, affecting main checkout and all worktrees). Human/S7 decides. Install: `git config --local core.hooksPath .githooks`. Unset: `git config --unset core.hooksPath`. S7 report must print the unset command (PA-9 grep). S1 report should say `hooks inert`.
2. Ship gate must run scripts directly (`check_model_pins.py --list`, `check_skill_budgets.py`, canary) since hooks are not installed; pre-push pathspec `-- . ':!.claude/worktrees'` is verified.
3. Post-push (S7b / PA-26): `gh run list --commit $SHIP_SHA` must show both `Model-pin guard` and `SKILL.md line-budget gate` success; guard is red until zero hits.
4. `MODEL_PIN_STRICT=1` is opt-in for both hooks; default advisory. `--no-verify` bypasses (detection, not prevention).
5. `workflow-injection-lint` on the S1 workflows should pass (simulated); it has not run on GitHub. Its own pre-existing actionlint findings are out of scope.
6. Producer note: `scripts/model_pin_fixtures.json` is qa-owned; not in commit 6560e64 (expected per plan).
