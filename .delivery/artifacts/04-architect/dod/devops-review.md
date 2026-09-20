---
verdict: DONE
role: devops
stage: 4-architect
run: run-2026-05-28-o48m
backlog: BACKLOG-108
blocking_issues: []
---

# DevOps DoD review, Stage 4 (rev 3)

Design operable. No blockers. Four warnings.

## Blocking issues

None.

## Checks and evidence

| Check | Result | Evidence |
|---|---|---|
| Guard triggers `push:main` + `pull_request` + `workflow_dispatch`, no `paths:` | OK | ADR-lmr-002 D7. Current file is `pull_request` + paths only (read). Rewrite needed and correct: direct push has no PR. |
| `push:main` on `skill-line-budget.yml` (U12) | OK | Current file `on: pull_request` + paths (read). Checker reads `PR_BODY` via `os.environ.get` default empty (ADR-005 item 8). Existing `env:` use is not in `run:`. |
| Push trigger collision with other workflows | OK | `version.yml` already `push: branches:[main]`; `release.yml` on `tags: v*`. Multiple push-main workflows already coexist. |
| workflow-injection-lint compliance | OK | Lint scans `run:` blocks for `github.event.*` (workflow-injection-lint.yml lines 20, 60). New guard job runs one script, no event interpolation. |
| No `claude` CLI in `.github/workflows/` | OK | `grep -rn "claude " .github/workflows` shows no invocation. Guard is static python scan, AC-1.3 forbids it. Smoke harness (`claude --print ...`) is local only (arch line 104). |
| Ship gate exit logic | OK | Reproduced in scratch repo: `grep -c` form prints 0 with rc=1 (clean case would wrongly fail); `grep -q` negated form rc=1 on clean tree, so `! ... grep -q` succeeds. Design uses the `-q` form. `git rev-list --count HEAD..HEAD` prints 0 rc=0 (bare count always rc 0), so `test "$(...)" = 0` wrapper is required and is used. |
| Pathspec `-- . ':!.claude/worktrees'` | OK | Scratch repo with nested worktree: raw status printed `?? .claude/worktrees/w1/`; pathspec form printed nothing; added stray file `b` then printed `?? b`. Matches ADR claim. |
| Block A/B ordering | OK | A (per-commit trailers, `--is-ancestor`) must precede squash; B after final commit and squash, before push, in main checkout. Single teed log outside repo (no dirtying step 2). Logical. |
| hooksPath install/log | OK | Existing `.githooks/pre-commit` header documents `git config core.hooksPath .githooks`. Design (P23, F14) requires install command plus `hooksPath=` log line, and states hooks inert otherwise. |
| Hooks advisory unless `MODEL_PIN_STRICT=1` | OK | D8 reference code: `pin_rc=0; ... || pin_rc=$?` survives `set -euo pipefail`; blocks only when strict. Existing budget checks stay blocking (`.githooks/pre-commit` lines 28-45); new call goes before the final OK line. Pre-push is strict for main only, passes other refs. |
| Live `--init-baseline` 5x budget | OK with W2 | 5 samples x `--max-budget-usd 3.00` = $15 ceiling (arch line 104). Aborts on any non-zero exit, so failed samples never averaged (ADR-004 s4/s5). Distinct session_id and hashes required. Baseline comparison disabled during init. Runs in Stage 7, after UAT plan confirmation. |
| RR-1 detect-not-prevent | Accepted | Honest: pin can land on main; detection by S7b clean-clone re-run and push workflow, both post-push. Owner PO, revisit triggers stated, remedy fix-forward (no force-push). Fits BINDING-5.1 (no PR). |

## Non-blocking warnings

- **W1, hook bypass is total.** `--no-verify` and unset `core.hooksPath` skip both hooks; only S7b and push workflow remain, both post-push. This is RR-1 by design. Suggest adding `hooksPath=` value to the S7 log as required (already planned) and treating an empty value as a logged waiver, not a pass.
- **W2, $15 is a per-sample cap, not an aggregate cap.** `--max-budget-usd` is checked between turns (P12, UNVERIFIED), so a sample can overshoot slightly; layer-2 post-check covers NFR-1 per run. Recommend the init flow also sum `total_cost_usd` and abort before sample n+1 if running total exceeds 5 x cap, and require an explicit go from the operator before the paid run. Non-blocking: worst case is a small overshoot of ~$15.
- **W3, budget workflow push has no exception path.** `Budget-Exception:` lives in the PR body, absent on push. Correct for direct push, but any known-debt change made by direct push will show red. Zero exceptions needed today (ADR-005). Plan should state this.
- **W4, WIP branch red.** From S1 to S4 the new guard workflow (pull_request and any pushed non-main branch is not triggered, since push is main only, but a PR would be) is red by design. Ship squashes S1 to S7 in one push, so main never goes red. Fine; keep that squash rule in the plan.
- P19 (Makefile and `.githooks/*` outside guard scope) is a latent hole, owned by PO; not a DevOps blocker.

## Verdict

DONE. 0 blocking issues, 4 warnings.
