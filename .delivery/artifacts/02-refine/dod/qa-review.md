<!-- run: run-2026-05-13-tk5 -->
---
stage: 02-refine
role: Quality Engineer (Legolas)
run: run-2026-05-13-tk5
backlog: BACKLOG-106
artifacts:
  - .delivery/artifacts/02-refine/po/prd.md
  - .delivery/backlog/BACKLOG-106-delivery-team-smoke-test.md
  - .delivery/artifacts/01-idea/_input/user-seed.md
status: DONE
---

# QA DoD Review — run-2026-05-13-tk5 (BACKLOG-106)

> Me Legolas. Me count ACs sharp. Eight orcs, eight arrows, that bug still only counts as one.

## Verdict

**STATUS: DONE** — PRD + BACKLOG pass all seven QA DoD gate criteria. Eight initiative-level ACs map cleanly to FRs; perf + cost bounds enumerated; producer-validator separation named in two artifacts; baseline statistical method explicit; cost-cap synthetic-injection path covered under FR-07/AC-06 baseline-comparison demo.

One soft warning on Gate 5 (Stage-7 UAT gate-set is mapped via "AC-01..AC-08 = UAT gates" in BACKLOG line 192 rather than re-enumerated under a dedicated Stage-7 header). Non-blocking — every AC IS a runnable command, so the gate-set is materially executable.

## Counts (run grep before reviewing — dogfood discipline)

```
$ grep -cE "^- \*\*AC-[0-9]+" .delivery/artifacts/02-refine/po/prd.md
8

$ grep -cE "^- \*\*FR-[0-9]+" .delivery/artifacts/02-refine/po/prd.md
8

$ grep -cE "^- \*\*NFR" .delivery/artifacts/02-refine/po/prd.md
5
```

**AC count: 8 — matches user-seed "8 ACs per user-seed" exactly. (tk4 lesson applied: count before reviewing.)**

## AC → FR Coverage Map (every AC must map to ≥ 1 FR)

| AC ID | AC summary | Mapped FR(s) | Pass/fail predicate | Map status |
|-------|------------|--------------|---------------------|------------|
| AC-01 | `python3 run_smoke.py` < 30 min wall-clock | FR-01 (runner spawn), NFR-Performance | time-elapsed measurement < 1800s | MAPPED |
| AC-02 | Output `report.json / summary.md / stream.jsonl` under `artifacts/<utc-timestamp>/` | FR-04 (report writer) | `find delivery-team/tests/smoke/artifacts/*/report.json` returns non-empty | MAPPED |
| AC-03 | `report.json` contains specified fields | FR-02 (metrics parser), FR-03 (aggregator), FR-04 (writer) | `python3 -c "import json; r=json.load(open('report.json')); assert all(k in r for k in [...])"` | MAPPED |
| AC-04 | `--init-baseline` runs 5× sequentially, writes mean+stddev | FR-06 (init-baseline) | `jq '.metrics | to_entries | all(.value.mean and .value.stddev)' baselines/hello_world_spike.json` | MAPPED |
| AC-05 | Regression detector HARD/ADVISORY thresholds | FR-05 (baseline detector) | meta-test `test_baseline_comparison_demo` exit codes | MAPPED |
| AC-06 | Meta-tests pass < 5 sec, no Claude calls | FR-07 (pytest meta-tests) | `pytest delivery-team/tests/smoke/tests/ --durations=0` exits 0 in < 5s | MAPPED |
| AC-07 | NO `.github/workflows/smoke-*.yml` | FR-08 (README docs), BC-01 (binding constraint) | `find .github/workflows -name 'smoke-*.yml'` returns empty | MAPPED |
| AC-08 | `smoke-test-architecture.md` records local-only constraint with memory-file pointer | FR-08 (README docs) + cross-cutting Architect artifact | `grep -l "feedback_claude_code_local_only.md" delivery-team/architecture/smoke-test-architecture.md` | MAPPED |

**Unmapped ACs: 0. (tk4 caught 3 unmapped in BACKLOG-104 — me ran the count this time. None hide.)**

## Gate-by-Gate Verdict

### Gate 1 — Concrete pass/fail predicates per AC

**PASS.** Every AC carries an exit-code-checkable predicate:
- AC-01: time-elapsed < 1800s (numeric)
- AC-02: file-existence (`find` returns non-empty)
- AC-03: field-presence (JSON key assertion)
- AC-04: file-shape (jq mean+stddev check)
- AC-05: meta-test exit codes
- AC-06: pytest exit 0 + `--durations` < 5s
- AC-07: `find` returns empty (absence check)
- AC-08: `grep` returns the memory-file path

No vague "works correctly" in any AC. Predicates table above is the runner manifest.

### Gate 2 — AC count = exactly 8, each mapped to ≥ 1 FR

**PASS.** Grep verified 8 ACs (line above). AC→FR map above shows zero unmapped. Matches user-seed "8 work items, 8 ACs" framing precisely.

### Gate 3 — NFR perf bounds (< 30 min wall-clock; cost-cap 3.00)

**PASS.**
- PRD line 50: `NFR-Performance: < 30 min wall-clock per single run`
- PRD line 51: `NFR-Cost: hard --cost-cap 3.00 per single run; --init-baseline envelope acknowledged as 5× cap (max $15 per baseline capture)`
- BC-05 (PRD line 62) restates both as binding constraints.

Both bounds are numeric and machine-checkable.

### Gate 4 — Meta-tests (FR-07) producer-validator separation named

**PASS.** Constraint is named in BOTH artifacts and is binding:

- PRD line 60 (BC-03): *"meta-test fault-injection fixtures CANNOT be authored by the same Stage-6 Dev dispatch that authors `lib/metrics.py` or `lib/baseline.py`. Binding from past waves; applies to validator-style artifacts. (Memory: producer-validator separation validated:5.)"*
- BACKLOG line 80 (W6-7 acceptance): *"must be authored by a different Stage-6 Dev dispatch than the one that authors `lib/metrics.py` (W6-2) and `lib/baseline.py` (W6-5)."*
- BACKLOG line 147 (risk register): "Producer-validator separation violated" — mitigation: Stage-5 Plan assigns Story 3 to different Dev dispatch.
- BACKLOG line 161 (story decomposition): Story 3 = validator half, MUST be different agent.
- BACKLOG lines 190-191 (Stage 5/6 handoff): validator Dev MUST NOT read producer Dev's `lib/metrics.py` or `lib/baseline.py` source while authoring fixtures.

Five distinct enforcement points. No gap.

### Gate 5 — Stage 7 UAT gate-set enumerated (8 gates, each a runnable command)

**PASS WITH SOFT WARNING.** The gate-set IS enumerated — but as AC-01..AC-08 (mapped to UAT via BACKLOG line 192: *"UAT signs off when AC-01 through AC-08 are all met."*) rather than as a dedicated "Stage 7 UAT gates" section with a numbered list of commands.

Each AC is materially a runnable command (see Gate 1 predicate table above). Functionally equivalent. Recommendation (non-blocking): a future BACKLOG could promote the predicate table into the BACKLOG's "Stage 7 UAT" handoff section as an explicit numbered gate list. For this run, the mapping suffices.

### Gate 6 — Cost-cap test path named (synthetic stream injection for cost-cap test — FR-05/AC-08)

**PASS.** Cost-cap regression is covered under the FR-07 / AC-06 baseline-comparison demo meta-test:

- PRD AC-06: meta-tests include "baseline-comparison demo".
- BACKLOG line 78 (W6-7 acceptance): *"baseline-comparison demo (synthetic inputs trip hard-fail and advisory-warn paths deterministically)"*.
- AC-05 hard-fail list explicitly names `cost > hard_max` — the synthetic-injection test trips this path with a fixture stream where `cost_usd` exceeds `hard_max`.

Synthetic stream injection is the named mechanism. The test path is wired through fixtures, not live runs (preserves NO-Claude-call constraint in FR-07).

Minor note: gate-criterion text says "FR-05/AC-08" but cost-cap mechanically threads through FR-05 (detector) and AC-05 (hard-fail spec) + AC-06 (meta-test execution). AC-08 is the local-only architecture doc. Interpreting the gate as intent (cost-cap test path exists) rather than literal AC-08 reference. PASS on intent.

### Gate 7 — Baseline capture: 5-sample / mean+stddev statistical method explicit

**PASS.** Stated four times in PRD + four times in BACKLOG:

- PRD line 16 (TARGET framing): "committed 5-sample baseline"
- PRD line 21 (US-2): "5-sample baseline captured once"
- PRD line 33 (FR-06): *"--init-baseline runs scenario 5× sequentially (concurrency-of-1 enforced) and writes mean+stddev per metric"*
- PRD line 42 (AC-04): *"runs the scenario 5× sequentially and writes baselines/hello_world_spike.json with mean+stddev per metric"*
- BACKLOG line 62 (W6-5 acceptance), line 108 (file inventory), line 135 (story-2 acceptance), line 145 (risk register: "5-sample stddev underestimates true variance" — risk acknowledged, mitigated by advisory-only first month).

Statistical method is unambiguous: `mean` + `stddev` per metric across 5 sequential samples; 2σ advisory band on `tokens.*` and `skill_loads.*`. NFR-Reproducibility (PRD line 52) governs the band-tightening cadence.

## Findings (non-blocking, recorded for downstream stages)

1. **Soft warning on Gate 5**: Stage-7 UAT handoff section in BACKLOG (line 192) maps "AC-01..AC-08 → UAT gates" implicitly. Future BACKLOGs would benefit from promoting the AC predicate table into a dedicated "Stage 7 UAT gate-set" enumeration with each gate's literal shell command. Non-blocking for run-tk5; suggest as a Refine-template enhancement post-merge.

2. **Cost-cap test path slightly implicit**: the synthetic-stream-injection test for `cost > hard_max` lives under the "baseline-comparison demo" umbrella in W6-7 acceptance. Dev should name it `test_cost_cap_hard_fail` (or similar) in `tests/test_meta.py` so the predicate is grep-findable post-Stage-6. Not a Refine gate fail; just a hint for Stage-6 Dev.

3. **AC-07 absence-check predicate**: `find .github/workflows -name 'smoke-*.yml'` must return EMPTY. Dev should add a meta-test that asserts this OR document it as a manual UAT step. Currently the burden lives on AC-07's literal check — flagging for Stage-7 UAT runner.

## DoD Status

**STATUS: DONE.** PRD + BACKLOG-106 testable, ACs specific, every AC has a concrete pass/fail predicate, all 8 ACs map to FRs, perf + cost NFRs bounded, producer-validator separation explicit in two artifacts, baseline statistical method (5-sample mean+stddev) explicit, cost-cap synthetic-injection path named. No empirical-validation gaps for the Refine stage (all gates here are document-level; runtime validation lands at Stage 7 UAT).

Pipeline may advance to Stage 3 Design.

— Legolas, Quality Engineer, run-2026-05-13-tk5. Eight orcs, eight arrows, every count clean.

## Signal Block

STATUS: DONE
ARTIFACT: /var/home/meconnelly/Documents/GitHub/Claude-Plugins/.delivery/artifacts/02-refine/dod/qa-review.md
SUMMARY: 8 ACs all mapped to FRs. Perf+cost bounds named. Producer-validator separation explicit. 5-sample mean+stddev explicit. Soft warning Gate 5 (UAT gate-set via AC mapping not separate enum). PASS.
