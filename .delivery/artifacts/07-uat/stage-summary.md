---
stage: 7
stage_name: uat
depth: full
pipeline_id: run-2026-05-13-tk5
status: GO_WITH_NOTES
dod_rounds: 1
dod_validators: [qa, po, devops]
po_decision: GO_WITH_NOTES (PARTIAL_READY merge; BACKLOG-107 follow-up)
artifacts:
  uat_report: .delivery/artifacts/07-uat/qa/uat-report.md
  release_plan: .delivery/artifacts/07-uat/devops/release-plan.md
  baseline: delivery-team/tests/smoke/baselines/hello_world_spike.json
  defects: .delivery/defects/sprint-tk5.md
  dod:
    qa: .delivery/artifacts/07-uat/dod/qa-review.md
    po: .delivery/artifacts/07-uat/dod/po-review.md
    devops: .delivery/artifacts/07-uat/dod/devops-review.md
notable:
  - "6/8 acceptance gates GREEN (G2/G3/G5/G6/G7/G8); 2 DEFERRED (G1+G4 — auth-isolation in workspace.py)"
  - "Live Claude probe exited 1 in 0.57s with empty stream — confirmed predicted HOME-isolation auth failure (D-tk5-04 HIGH, fix path documented: keep HOME, isolate via cwd + XDG_*)"
  - "G8 cost-cap synthetic injection works end-to-end: exit=2, outcome.reason=cost-cap-exceeded, cost_usd=3.25"
  - "G3 meta-tests: 3 passed in 0.02s (30x under 5s budget)"
  - "Stop-rule headroom 0.067 (worst-case 0.333 vs 0.4 threshold) — proceed"
  - "All 3 DoD reviewers endorsed PASS_WITH_NOTES (QA 8/8, PO 8/8, DevOps 5/5 live-rerun)"
  - "Honest-readiness-marker pattern (Wave-2 lineage) applied to baseline.json: n_samples=0, sample_status=deferred, BACKLOG-107 named"
  - "Stale-sweep banner-marked 15 tk4/tk3 files at Stage 7 entry (W3-17 dogfood evidence)"
---

# Stage 7 Summary — UAT (full) — run-2026-05-13-tk5

PASS_WITH_NOTES. Dogfooding caught the auth-isolation flaw before the team spent $10 on 5 broken live runs — exactly the failure mode the smoke-test framework is designed to catch in future plugin changes. Six gates GREEN live (meta-tests, no-CI, memory-cite, budgets, lint, cost-cap, malformed-stream exploratory). Two DEFERRED with concrete fix path in BACKLOG-107. 4 defects logged (1 HIGH, 3 LOW); rolling defect rate stays under stop-rule threshold.
