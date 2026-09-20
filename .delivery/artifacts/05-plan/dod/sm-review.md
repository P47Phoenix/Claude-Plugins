<!-- run: run-2026-05-28-o48m -->
---
verdict: DONE
role: sm
stage: 5
round: 1
blocking: []
---

# SM DoD review, Stage 5 Plan, run-2026-05-28-o48m

Note: file overwrites an older-run `sm-review.md` (run tk5); history in git. Skill `delivery-team:sm` unknown; role applied from brief.

## Verdict
DONE. Plan deliverable. 0 blocking.

## Blocking issues
None.

## Checks
- Ordering/deps: S1 -> S2 -> S3 -> S4 -> S5a -> S6, then S5b, S7, S7b. Deps in table: S2<-S1, S3<-S2, S4<-S1,S3, S5a<-S1,S4, S6<-S3, S5b<-S5a,S6,H2, S7<-all, S7b<-S7. No cycle. Stated order is a valid topo order.
- Sizing: biggest is S5a (L, 1.5-2 d), split in 3 sub-steps (P0 stub, red, fix). No story >2 d. Total 5-6 d matches row sums (~4.75-6.25 d).
- Executor != validator on every row. S7 executor devops vs S7b devops: plan says different agent id; OK. S6 devops/developer, S5b devops/qa fine.
- Stage assignment: S1-S4, S5a, S6 in Stage 6; S5b, S7, S7b in Stage 7. D1a skip list (AC-5.1, 5.4, 5.5, 5.5c, 5.6) matches section 3.1 rows for S5b (all "UAT"). Consistent. G5 closing at UAT stated in 5.8 exit checks.
- Serial commit rule workable: S2 three edit-only dispatches, orchestrator commits serially with pathspec + Dispatch-Id each. One tree, no parallel commits elsewhere. Workable.
- Gates: H1 before first paid fixture capture (<= $0.50), H2 before S5b after S6 hash MATCH and spend snippet, H2b conditional, H3 before push, H4 after S7b. No spend before a gate. Placement right.
- Cache re-freeze ordering: S6 after S3, re-freeze again on any later SKILL.md edit (5.5). Covers rework.

## Warnings (non-blocking)
1. S5a: qa is validator AND writes tests, fixture, gate scripts, then architect final review. Heavy for one qa dispatch; if it overruns, split fixture capture (H1) from gate work. Stage 6 DoD then runs qa again as separate dispatch; keep ids disjoint (plan covers via PA-13).
2. Stage 6 DoD list has 4 roles (developer, qa, architect, tech-writer) per unit round, 6 units; up to 3 rounds each. Worst case many dispatches; effort total does not include DoD rounds explicitly ("sub-agent time" only). Real calendar may run past 6 d.
3. S6 sits after S5a in order but depends only on S3; fine, but any S5a-triggered SKILL.md change forces re-freeze (plan covers). Keep S5a off SKILL.md.
4. H1 is asked mid-Stage 6 with no config checkpoint (`pipeline.checkpoints: []`); orchestrator must actually halt. Plan states real stop; note for runner.
5. `.delivery/artifacts/05-plan/dod/` holds old-run files with same names; reviewers must ignore them (plan notes this for 05-plan/ generally).
6. Plan section 6 says Stage 5 DoD not yet run; stage-summary `dod_rounds: 0`; orchestrator must update after this round.

## Evidence (verified in repo)
- `wc -l delivery-team/skills/delivery-flow/SKILL.md` = 499 (plan: 499, cap 500). `prompt-engineer/SKILL.md` = 520, `product-delivery/SKILL.md` = 300 (plan: 520, 300/300). OK.
- `.delivery/config.yml` lines 56-63: `plan: [sm, po, qa, developer, devops]`, `development: [developer, qa, architect, tech-writer]`, `uat: [qa, devops, po, tech-writer]`. Matches plan sections 5.2, 5.8, 6.
- `sha256sum` of delivery-flow SKILL.md starts `43067c9e`; `head -c 2048 | sha256sum` starts `8c2ebf97`. Match plan 5.5.
- `find` gives `delivery-team/references/shared/orchestrator-doctrine.md`; `smoke-test-architecture.md` and `telemetry-schema.md` exist at plan paths.
- `skill-line-budget.yml` `on:` has only `pull_request` (no push) -> D4 addition is real work in S1. `.githooks/` has only `pre-commit` -> pre-push is NEW as plan says.
- conftest.py has 4 `"model": "claude-opus-4-7"` lines (105, 117, 129, 151): matches "4 fixture model values". Arch doc lines 115/116 and telemetry-schema line 36 hold model ids as claimed.
- PRD line 508 is AC-5.1 loading baseline JSON: supports D1a.
- `delivery-team/tests/smoke/lib/` has metrics, runner, report, aggregator, baseline: S5a producer file list valid.
