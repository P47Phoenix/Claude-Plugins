---
run: run-2026-05-28-o48m
stage: 5
role: devops
reviewer: fresh DoD validator (operations skill)
verdict: NOT_DONE
blocking_count: 3
warning_count: 7
note: overwrites an older-run file (run-2026-05-13-tk5) at this path; history in git (d0e0928)
---

# Stage 5 Plan DoD: DevOps review (BACKLOG-108)

Prose: caveman-lite. Read: plan.md, stage-summary.md, ADR-lmr-002, ADR-lmr-005, ADR-lmr-004 (spend lines only). `architecture.md` is at no `04-architect/architecture.md` path (grep failed); ADRs used as the Stage 4 source.

## Verdict: NOT_DONE (3 blocking, all cheap plan text fixes)

Plan is mostly operable. Ship path, CI additions and guard are well owned. Three gaps touch the exact things asked: spend ceiling, human-go enforcement, fix-forward.

## Blocking issues

### B1. Aggregate $15.00 ceiling is soft in the plan (regressed from ADR-lmr-004)
- Plan 5.6, PA-16, PA-22, H2: "`spent <= 15.00` printed before each S5b run".
- ADR-lmr-004 line 109: stop "if `spent + 3.00 > 15.00`".
- With the plan check, a run may start at spent=14.99 and finish at 17.99. H2b says "the harness stops first": false as written. Also 7 runs x $3 = $21 cannot fit $15, so run 6 and 7 are only legal when earlier runs were cheap; plan never says so.
- Fix: PA-16/PA-22/5.6/H2 use `spent + next_cap(3.00) <= 15.00` before every run, and the snippet also counts run dirs and stops at 8th. Restate in H2 text so Michael approves the true ceiling.

### B2. Human gates H1..H4 have no recorded, checkable go; background-job stop is undefined
- Gates are prose ("asked", "Owner: Michael"). ADR-lmr-004 line 107 requires `operator_go: <date>` copied from the user's message in the S5a/S5b dispatch prompt; ADR-lmr-005 step 9 requires it for the push. Plan drops this: no PA, no rule in 5.1/5.6/5.8 mentions `operator_go`. H1 (fixture, $0.50) and H4 have no recording step at all.
- Nothing says an agent-relayed "approved" is not a go, nor what a non-interactive background job does at a gate. Only "S5a stalls" (H1) and "does not start" (H2).
- Fix: add PA-23. Each of H1, H2 (and each re-run past 5), H3, H4 needs a line `operator_go: <gate> <date> <verbatim user message ref>` in the dispatch prompt and in the artifact (`s5b-spend.txt` head, ship log, S7b/H4 commit note). Dispatch stops and reports if absent. Only a direct human turn counts; no agent message, memory or plan text counts. At a gate the job writes `blocked_on: H<n>` into `state.md` and returns; it never polls or retries.

### B3. No fix-forward / rollback story, and no gate for a corrective push
- Only RR-1 acceptance (D20, R-3) and a PA-20 report sentence. ADR-lmr-005 item 8 gives the remedy (fix-forward through the whole gate, never force-push) but no plan story, AC or owner carries it.
- Gaps: (a) what happens if S7b returns FAIL or the post-push guard or budget workflow goes red; (b) H4 is "asked with the S7b verdict in hand" with no FAIL branch; (c) a fix-forward or `git revert` push to main is not covered by H3 (H3 says "Push to origin/main (ship)"), so it has no named gate; (d) S7b never checks that the `push` workflows (guard, budget) went green on `SHIP_SHA`.
- Fix: add story S8 (or S7c) "Post-ship recovery", owner devops, with ACs: on S7b FAIL or red workflow, no docs push (H4 not asked as PASS); open backlog defect; the corrective commit runs Block A/B again; push needs a fresh H3-class go (H3b); `git revert` of `SHIP_SHA` allowed as the fast option; no force-push, ever. Add to S7b: check workflow run conclusions for `SHIP_SHA` (`gh run list --commit`, or state "UNVERIFIED, manual" if `gh` absent).

## Warnings

- W1. H3 "no" says "nothing lands on main", but Block B does the ff-merge into LOCAL `main` before H3 (ADR-lmr-005: ff-merge, then steps 1-9). A denied H3 leaves local `main` ahead of origin; another session could push it. Add: on H3 "no" or gate failure, reset local main to `origin/main` (or ff-merge into a temp ref only after H3). Plan should also say who moves the squashed branch from this worktree (`worktree-backlog-108-o48m`) into the main checkout, and that Block B step 2 needs that checkout clean.
- W2. H4 docs-only commit: nothing proves it is docs-only. Add AC: `git diff --name-only SHIP_SHA..HEAD` lists only `.delivery/` paths, no `--no-verify`, pre-push hook and guard still run, S7b checked `HEAD == SHIP_SHA` BEFORE H4. Guard scope excludes `.delivery/` so the gate is not defeated, but it is untested. Also list `07-uat/dispatch-manifest-S7b.txt` in the H4 commit (ADR-005 item 8), and pick one report name: plan `s7b-report.md` vs ADR `ship-verification.txt`.
- W3. `core.hooksPath` install and `hooksPath=` log are in D6 and 5.8 entry but no PA/AC under S1 (PA-20 covers S7 only). Add to PA-7. `--local` writes the SHARED `.git/config`: it changes hooks for the main checkout and every worktree/session. Plan should say so and put the `git config --unset core.hooksPath` line in the S7 handoff report (D6 says handoff prints it; make it an AC).
- W4. Run-count cap "max 7" has no enforcing snippet step (only spend). Fold into B1 fix.
- W5. `Budget-Exception:` unusable on push is noted; good. Confirm S1 dry-run of the budget workflow with `PR_BODY` unset is an AC (D4 cites the arch run; PA-6 lacks the run).
- W6. 5.1.5 "no branch push before ship" vs ADR ("branch push harmless, push trigger is main only"): consistent as stricter; keep. Note Stage 6 branch push is never needed, so a pre-push hook stub test (PA-7) is the only exercise of that hook before ship.
- W7. Stage 5 reads `05-plan/dod/` holding old-run files (this path). Plan 5.1.9 covers `06-development/dod/` only; extend to `05-plan/dod/` so reviewers don't read stale verdicts.

## Checked and OK (evidence)

- Fixture cap: `--max-budget-usd 0.25`, max 2, after H1 (PA-16, 5.6, H1). Per-sample $3.00, 30 min wall, sequential (PA-22). `BAD_COST` and missing report = $3.00 (PA-16). Out-of-tree `$SMOKE_OUT`, tracked `s5b-spend.txt` (PA-22). Outcome-failed sample aborts `--init-baseline` (5.6).
- Ship gate: Block A step 0 pre-squash, Block B in MAIN checkout with `-- . ':!.claude/worktrees'`, flag check, `test "$(...)"` forms, `step=<n> exit=<rc> value=<v>`, out-of-tree teed log (PA-20 matches ADR-005 item 8). Single squashed push, S1..S3 never pushed (P14).
- S7b: different devops id, fresh clone, `HEAD == SHIP_SHA`, canary, transcript check with `RAN`/`SKIPPED layout-drift` (PA-21, PA-2).
- CI additions each owned in S1: guard workflow rewrite, push trigger on `skill-line-budget.yml`, `permissions: contents: read`, `persist-credentials: false` (PA-6); pre-push 7 stub cases (PA-7); pre-commit edit and strict/advisory test (PA-5); `workflow-injection-lint` green (PA-6).
- No `claude` in `.github/workflows/`: 5.6 line 1, FR-1.3/AC-1.3 in matrix (S1), U7 (tests patch `claude --version`), D7 workflow has no pip install and no claude. Paid runs are local only.
- Never `--no-verify` outside a tested case, never `git add -A`, never stash (5.1.5).
- `Budget-Exception:` route documented as `known_debt[]` + `target_wave:` committed before ship (PA-20).

## Path
/var/home/meconnelly/Documents/GitHub/Claude-Plugins/.claude/worktrees/backlog-108-o48m/.delivery/artifacts/05-plan/dod/devops-review.md
