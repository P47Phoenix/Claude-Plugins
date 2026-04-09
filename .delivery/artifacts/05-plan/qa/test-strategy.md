# Test Strategy — Paired Constraints Primitive

**Stage**: 5 Plan | **Role**: QA Engineer (Legolas) | **Date**: 2026-04-08
**Pipeline ID**: run-2026-04-08-a1f3 | **Feature**: `constraints.yml`

> *"A bug is a bug. That still only counts as one."*

My eyes are sharp. Every FR shall have a test; every test shall have an oracle. No fog, no guesses.

---

## 1. Traceability Matrix (FR → Test Case)

| PRD FR | Test Case ID | Test Type | Automation | Validates |
|---|---|---|---|---|
| FR-1 | TC-FR1-1 | Schema validation | auto | 8 fields, types, required markers |
| FR-1 | TC-FR1-2 | File presence | auto | `constraints-model-guide.md` exists |
| FR-2 | TC-FR2-1 | File presence | auto | Refine PO template loadable |
| FR-2 | TC-FR2-2 | Schema validation | auto | Refine template conforms to FR-1 schema |
| FR-3 | TC-FR3-1 | File presence | auto | Architect template loadable |
| FR-3 | TC-FR3-2 | Static grep | auto | Enumerated forbidden list present verbatim |
| FR-3 | TC-FR3-3 | Schema validation | auto | Architect template conforms to FR-1 schema |
| FR-4 | TC-FR4-1 | Citation presence | auto | "Golden Rule" header + Löwy citation in `volatility-decomposition.md` |
| FR-4 | TC-FR4-2 | Static grep | auto | Functional-decomposition-trap anti-pattern section present |
| FR-5 | TC-FR5-1 | Static grep | auto | "No Implementation Nouns" guardrail threaded Phases 1–4 of `strategic-ddd.md` |
| FR-6 | TC-FR6-1 | Static grep | auto | `pipeline-stages.md` names Architect in Stage 5 between steps 1 and 3 |
| FR-6 | TC-FR6-2 | Dogfood pipeline run | semi | `.delivery/artifacts/05-plan/architect/sequencing.md` emitted |
| FR-7 | TC-FR7-1 | Dogfood pipeline run | auto | DoD validator fires forbidden-vocab grep on `constraints.yml` |
| FR-7 | TC-FR7-2 | Dogfood pipeline run | auto | Mandatory-artifact presence check fires |
| FR-7 | TC-FR7-3 | Dogfood pipeline run | auto | Numeric-ceiling compliance check fires |
| FR-8 | TC-FR8-1 | File presence | auto | `.delivery/artifacts/02-refine/po/constraints.yml` exists (Exhibit A) |
| FR-8 | TC-FR8-2 | Schema validation | auto | Exhibit A conforms to FR-1 schema |
| FR-8 | TC-FR8-3 | Static grep | auto | Exhibit A passes forbidden-vocab oracle (§3) |
| NFR-1 | TC-NFR1-1 | Metric measurement | manual | Plan first-try ≥80% over 5 runs *(empirically deferred)* |
| NFR-2 | TC-NFR2-1 | Static grep | auto | Forbidden-vocab oracle — zero matches post-feature |
| NFR-3 | TC-NFR3-1 | Backwards compat | auto | Legacy run with no `constraints.yml` completes |
| NFR-4 | TC-NFR4-1 | Migration smoke | auto | v2.7 config loads under v2.8 schema without error |
| NFR-5 | TC-NFR5-1 | Metric measurement | manual | Refine token delta ≤15% *(empirically deferred)* |
| NFR-6 | TC-NFR6-1 | File sync check | auto | SessionStart hook asserts installed↔source parity |

**Coverage: 8/8 FRs, 6/6 NFRs, 24 test cases.**

---

## 2. Test Types In Play

- **Schema validation** — JSON Schema generated from architecture.md §3; `constraints.yml` conforms.
- **Static grep** — forbidden vocabulary absent from decomposition artifacts.
- **Citation presence** — `volatility-decomposition.md` §0 "Golden Rule" exists and is cited by dogfood.
- **Dogfood pipeline run** — this PRD's own `constraints.yml` is Exhibit A.
- **Metric measurement** — 5-run rolling window, post-UAT.
- **Migration smoke** — v2.7→v2.8 config load.
- **Backwards compat** — legacy no-`constraints.yml` run still completes.

---

## 3. Forbidden Vocabulary Test Oracle

Enumerated from ADR-003. Whole-word, case-insensitive. Run against decomposition artifact tree:

```bash
grep -rEiw \
  -e 'lambda|aws lambda|ecs|eks|fargate|ec2|azure functions|gcp|google cloud functions' \
  -e 'kubernetes|docker|ecr' \
  -e 'sqs|sns|eventbridge|kinesis|kafka' \
  -e 'dynamodb|s3|postgresql|mysql|mongodb|redis|elasticsearch' \
  -e 'python|node|node\.js|typescript|javascript|golang|rust|java|c#|ruby' \
  -e 'express|fastapi|django|flask|spring|rails|next\.js' \
  .delivery/artifacts/04-architect/ \
  --include='*.md' --include='*.yml'
```

**Oracle**: exit 1 (zero matches) = PASS. Any match = FAIL with file+line.
Stage scope: decomposition only. Plan/Dev artifacts are exempt (ADR-003 §Scope discipline).

---

## 4. Empirical Validation Plan (NFR-1, AC-6)

- **What counts as a run**: a real feature pipeline invocation reaching Stage 5 Plan DoD with `experimental.constraints_model: true`. Synthetic runs excluded.
- **Measurement**: Plan first-try pass = DoD gate passes on first submission, zero rework loop.
- **Cadence**: rolling 5-run window after UAT land.
- **Signal destination**: `.delivery/memory/stages/plan.md` stage health table — one row per run (run_id, first_try_pass: bool, rework_count).
- **Pass threshold**: ≥4/5 (80%).
- **Rollback trigger**: <3/5 passes in any 3-run window → flip `experimental.constraints_model: false`, reopen BACKLOG-001.
- **Auxiliary signal**: `.delivery/memory/topics/defect-patterns.md` receives any forbidden-vocab hit with artifact path + run ID.

---

## 5. Rollback Test

If `experimental.constraints_model: false` is set:
1. **TC-ROLL-1**: pipeline runs end-to-end without loading `constraints.yml`. Oracle: Stage 5 DoD completes; no grep gate fires.
2. **TC-ROLL-2**: grep for `constraints_model` references in runtime logs — zero active enforcement. Oracle: feature fully dormant.
3. **TC-ROLL-3**: pre-existing `constraints.yml` on disk is ignored, not errored. Oracle: exit 0.

Rollback clean = all three pass.

---

## 6. Known Untestable / Empirically Deferred

These are **not gaps** — they are deferred by physics:

- **AC-6 / NFR-1 — Plan first-try ≥80%.** Requires 5 post-land runs. Tracked as `[EMPIRICALLY DEFERRED — UAT + 5 runs]`.
- **NFR-5 — Refine token delta ≤15%.** Requires post-land token accounting over same window.
- **ADR-003 false-positive rate.** Cannot be bounded until authoring corpus accumulates.

All three carry explicit deferral flags in the UAT test report.

---

## 7. Test Effort Estimate

Markdown-tier-lower calibration (content work, not code).

| Bucket | Points |
|---|---|
| Schema + grep automation (TC-FR1..3, TC-FR8, TC-NFR2) | 3 |
| Citation/presence checks (TC-FR4..6) | 2 |
| Dogfood run harness (TC-FR7, TC-FR6-2) | 2 |
| Migration + backwards-compat + sync (TC-NFR3/4/6) | 2 |
| Rollback suite (TC-ROLL-1..3) | 1 |
| Metric measurement scaffolding (deferred signals) | 1 |
| **Total** | **11 points** |

---

```
STATUS: DONE
ARTIFACT: .delivery/artifacts/05-plan/qa/test-strategy.md
SUMMARY: Bow is strung. 24 TCs, 8/8 FRs + 6/6 NFRs covered. 3 empirically-deferred to UAT+5 runs. Forbidden-grep oracle is one command. 11 points.
```
