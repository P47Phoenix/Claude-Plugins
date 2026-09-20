---
stage: 5
stage_name: plan
depth: light (all content present)
pipeline_id: run-2026-05-28-o48m
status: REVISION_2_READY_FOR_DOD_ROUND_2
decisions_count: 21
dod_validators: [sm, po, qa, developer, devops]
dod_rounds: 1  # round 1: sm/po/developer DONE, qa/devops NOT_DONE; revision 2 applied, round 2 pending
open_human_gates:
  - "H1 operator go for fixture captures (<= 2 x $0.25), asked in Stage 6 at S5a validator step"
  - "H2 operator go for S5b live baseline (5 x $3 cap, hard rule spent+3.00<=15.00 before each run, max 7 runs), asked at Stage 7 S5b start; also restates no --bare (D18)"
  - "H2b any spend above $15.00 or more than 7 runs (conditional)"
  - "H3 push to origin/main, asked in Stage 7 after UAT PASS and clean gate log"
  - "H4 second push (docs-only S7b report), asked after S7b only on PASS; H4-FAIL branch runs S8"
  - "H5 conditional override of D18 (--bare), restated inside H2"
  - "H6 any corrective push to origin/main (fix-forward or revert), asked in S8"
artifacts:
  primary: .delivery/artifacts/05-plan/plan.md
---

# Stage 5 Summary — Plan — run-2026-05-28-o48m

Plan written: 21 decisions, stories S1..S7 plus S5a/S5b/S7b with scope, effort, executor/validator, stage. Id-level FR/AC matrix built. Plan-carry mapped (P1..P23, U1..U14, R-1..R-6, DoD warnings). Stage 6/7 rules set.

Key calls: S5a in Stage 6, S5b live baseline in Stage 7 (Stage 6 DoD skips AC-5.1/5.4/5.5/5.5c/5.6); multi-manifest AC-DISP; `02-refine` dropped from REQUIRED; push trigger + pre-push hook accepted; uniform `latest` stamp accepted with stamp-only ledger; R4 raised to Medium; no `--bare`; `--effort xhigh` opus only.

Old files in `05-plan/` (`po/`, `qa/`, `dod/`, ...) belong to run `run-2026-05-13-tk5`; not used.

DoD not yet run. Orchestrator dispatches the five plan validators and writes `05-plan/dispatch-manifest.txt`.

Revision 2 (DoD round 1 fixes): hard spend check, operator_go + blocked_on protocol, S8 post-ship recovery, H6, PA-9/13b/23..27 added, PA-24 baseline dry-run, re-entry rule 5.9. See plan.md section 7.
