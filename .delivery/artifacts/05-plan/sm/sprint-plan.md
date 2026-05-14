<!-- run: run-2026-05-13-tk5 -->
<!-- author: Aragorn (Scrum Bag, Stage 5 light, step 4) -->
<!-- backlog: BACKLOG-106 -->
<!-- inputs: stories.md (PO), prd.md (PO), ADR-tk5-001 (Architect), user-seed.md, config.yml -->
# Sprint Plan — run-2026-05-13-tk5 (BACKLOG-106 Smoke Test)

> *"I do not know what strength is in my backlog, but I swear to you I will not let the sprint fall."* — Aragorn

Me Aragorn. Me rally fellowship. One wave. One commit. Three stories bind the eight. Me lead from front.

---

## 1. Sprint Goal

Ship the smoke-test runner + 5-sample baseline + meta-tests in one wave; no CI workflow per local-only memory directive.

---

## 2. Capacity Matrix

Team size = 1 per `.delivery/config.yml` (`team.size: 1`, composition includes `developer`). Sprint window = 4 working days × 8h = 32h available per role. Ceremony overhead (planning, retro, refinement, Stop-hook minimal retro per BACKLOG-106 §Stop-hook risk) = 4h, subtracted from available. Net available = 28h. Producer dispatch (S1+S2) and validator dispatch (S3) are the SAME human team member but DIFFERENT Stage-6 Dev sub-agent contexts per BC-03 (validated:5) — capacity is a single pool.

| Role | Available hours | Allocated hours | Utilization % |
|------|-----------------|-----------------|---------------|
| Developer (sole team member; producer Dispatch A + validator Dispatch B) | 28h (32h − 4h ceremony) | 20h (S1: 9h L, S2: 6h M, S3: 5h M) | 71.4% |

Utilization = 71.4%. Under 80% WARN line. Under 100% BLOCKING line. Buffer of 8h (28.6%) absorbs interruption + the planned producer-to-validator context-switch tax between Dispatch A and Dispatch B (BC-03).

**Capacity verdict**: HEALTHY. No BLOCKING. No WARN. Proceed.

---

## 3. Coverage Matrix (FR -> Story -> Task)

Every PRD FR maps to >= 1 story. Verified against `02-refine/po/prd.md` §Functional Requirements (FR-01 through FR-08). No orphans.

| FR-ID | Story | Task (WI surface) | AC ref |
|-------|-------|-------------------|--------|
| FR-01 (isolated subprocess + `--plugin-dir` capability probe + mktemp HOME) | S1 | `lib/runner.py` subprocess + `lib/workspace.py` mktemp HOME; capability-probe `claude --help \| grep -q -- --plugin-dir` | AC-S1-03, AC-S1-04 |
| FR-02 (stream-json -> Metrics; pure; malformed warns) | S1 | `lib/metrics.py` pure-function `parse_stream(events)` returning Metrics dataclass | AC-S1-06 |
| FR-03 (aggregator reads telemetry hook outputs + state.md) | S1 | `lib/aggregator.py` reads `skill-loads.jsonl` + `run-summary-*.json` + `state.md`; fallback invokes `telemetry_run_summary.py` | AC-S1-07 |
| FR-04 (report writer: report.json + summary.md + stream.jsonl under timestamped dir) | S1 | `lib/report.py` writes 3 artifacts under `artifacts/<utc-timestamp>/`; schema per architecture §5 | AC-S1-02, AC-S1-08 |
| FR-05 (baseline detector: HARD/ADVISORY thresholds) | S2 | `lib/baseline.py:compare()` exit-code 0/1/2; HARD on outcome/cost/wall/dispatch/stories; ADVISORY on ±2σ tokens + skill_loads | AC-S2-03, AC-S2-04, AC-S2-05 |
| FR-06 (`--init-baseline` 5x sequential + mean/stddev write) | S2 | `lib/baseline.py` 5-run loop, concurrency-of-1; writes `baselines/hello_world_spike.json` | AC-S2-01, AC-S2-02, AC-S2-08 |
| FR-07 (pytest meta-tests in < 5s; no Claude calls) | S3 | `tests/test_meta.py` 3 tests: malformed-stream, baseline-compare demo, aggregator-fixture | AC-S3-01, AC-S3-02, AC-S3-03, AC-S3-04, AC-S3-08 |
| FR-08 (README + `Makefile` smoke target) | S3 | `tests/smoke/README.md` (local-only cite + flag ref); root `Makefile` `smoke` target | AC-S3-05, AC-S3-06; supporting fixture AC-S2-07 |

Cross-check: 8 FRs mapped; 24 ACs covered; 8 WIs covered (per stories.md WI audit). **Zero unmapped FRs. No BLOCKING.**

---

## 4. Story Sequencing

Architect's sequencing (encoded in ADR-tk5-001 §"Producer-Validator Separation" + stories.md §Cross-story matrix) proposes `S1 -> (S2 ∥ S3)`. PO directive in stories.md and BACKLOG-106 §Story Decomposition **overrides**: S3 sequential after S1+S2 to preserve validator-dispatch freshness (BC-03). Validator must NOT have read S1+S2 source while authoring fixtures.

Final sequence:

```
S1 (Dispatch A producer, L=9h)
  └─> S2 (Dispatch A producer, M=6h)        [same dispatch context as S1 per BACKLOG-106 §Story Decomposition]
        └─> S3 (Dispatch B validator, M=5h) [DIFFERENT dispatch context; fresh; reads PRD/BACKLOG/architecture only]
```

Dispatch ordering:
1. Dispatch A opens, authors S1 (`run_smoke.py`, `lib/{runner,workspace,metrics,aggregator,report}.py`), then S2 (`lib/baseline.py`, `baselines/hello_world_spike.json`, `prompts/hello_world_spike.txt`, `fixtures/delivery_config_minimal.yml`). Dispatch A closes.
2. Dispatch B opens fresh. Reads PRD, BACKLOG-106, `delivery-team/architecture/smoke-test-architecture.md` ONLY. Does NOT read S1+S2 source. Authors S3 (`tests/test_meta.py`, `tests/fixtures/`, `README.md`, root `Makefile`).
3. Stage-7 UAT verifies git log shows two distinct Dev commits (or two distinct authors within a squash).

**Parallelism rejected**: `max_parallel_agents: 3` in config supports parallel dispatch, but BC-03 binding (validated:5 past waves) forbids it here — concurrent S3 would let validator peek at producer source via filesystem.

---

## 5. Risk Register

Five risks pulled from PRD §Open Risks + user-seed §Open risks. Owners assigned per role-of-execution.

| # | Risk | Severity | Mitigation | Owner |
|---|------|----------|-----------|-------|
| R-01 | **Prompt drift** — orchestrator dispatches more than hello-world spike requires; inflates `dispatch_count`. | HIGH | `hard_max` on `dispatch_count` in baseline JSON (AC-S2-04 strict-equality on `stories_completed` + hard-cap on `dispatch_count`); prompt explicitly requests "skip personas, skip UAT, minimal retrospective" (AC-S2-06 + TC-S2-08 grep guard). | PO (Gandalf) — prompt authoring sits with PO/Dev producer; PO owns prompt fidelity. |
| R-02 | **Cost overrun** — single run exceeds $3 cap, or `--init-baseline` envelope exceeds $15. | HIGH | `--cost-cap 3.00` hard flag in runner (AC-S1-05); 30-min wall-clock SIGTERM (AC-S1-05); concurrency-of-1 on `--init-baseline` (AC-S2-01); $15 baseline envelope acknowledged in NFR-Cost. | Developer (Dispatch A) — owns runner enforcement. |
| R-03 | **`--plugin-dir` semantics drift** — flag absent or renamed in installed `claude` CLI version. | MEDIUM | Capability-probe at startup (`claude --help \| grep -q -- --plugin-dir`) writes `plugin_load_strategy` to report.json; fallback copy-into-`<tmp>/.claude/plugins/delivery-team/` path (AC-S1-04 + TC-S1-04). | Architect (Celebrimbor) — owns dispatch-strategy contract per ADR-tk5-001 Decision-1. |
| R-04 | **Stop hook blocks** — existing Stop hook enforces retro/memory completion; pipeline hangs mid-run. | MEDIUM | Prompt requests minimal retrospective so Stop hook has something to consume (AC-S2-06); runner captures stderr so blockage is visible in `report.json.hard_failures`; 30-min wall-clock SIGTERM is the backstop. | Developer (Dispatch A) — runner stderr capture; PO (Gandalf) — prompt minimal-retro language. |
| R-05 | **Variance > stddev budget** — 5-sample n underestimates true variance; advisory band trips on noise. | LOW (first month) | NFR-Reproducibility: advisory-only for first month on `tokens.*` and `skill_loads.*`; 2σ band, no exit-code escalation (AC-S2-05); tighten to 1.5σ AFTER 20+ accumulated production runs (deferred BACKLOG, OOS this initiative). | PO (Gandalf) — owns band-tightening BACKLOG once enough samples accrue. |

---

## 6. Stop-Rule Reminder

**Rule**: defects/story > 0.4 across any 3-PR window pauses subsequent work.

**Current rolling rate**: 0.111 (per PRD §Stop-rule + user-seed §Stop-rule).

**Headroom**: 0.400 − 0.111 = **0.289 defects/story remaining headroom before pause**. With 3 stories in this wave, that buys roughly 0.867 raw defects of room (3 × 0.289) before the rolling window crosses threshold. Wave will be re-measured after PR merge; rolling-window math runs against the most recent 3 PRs, not this initiative in isolation.

If the wave's PR introduces > 0.867 defects, the next initiative pauses. Aragorn flag the gate; me no breach.

---

## 7. Definition of Done (Initiative-Level — Stage 7 UAT Acceptance Gates)

Eight gates from `user-seed.md` §Acceptance criteria. Stage 7 UAT QA + DevOps + PO + Tech-Writer verify (per config `dod_validators.uat: [qa, devops, po, tech-writer]`). All eight must check before initiative closes.

- [ ] **DoD-1**: `python3 delivery-team/tests/smoke/run_smoke.py` completes on developer's machine in < 30 min wall-clock. *(Maps PRD AC-01.)*
- [ ] **DoD-2**: Output written to `delivery-team/tests/smoke/artifacts/<utc-timestamp>/{report.json, summary.md, stream.jsonl}`. *(Maps PRD AC-02 + AC-S1-02.)*
- [ ] **DoD-3**: `report.json` contains all of: `outcome.success`, `wall_clock_seconds`, `cost_usd`, `tokens.{input,output,cache_creation,cache_read}`, `model_usage` (per-model dispatches+tokens), `pipeline.{stages_completed, stories_completed, dispatch_count, defects_logged}`, `skill_loads` (from `.delivery/telemetry/skill-loads.jsonl`), `git_sha`, `claude_cli_version`. *(Maps PRD AC-03 + AC-S1-08.)*
- [ ] **DoD-4**: `--init-baseline` flag runs scenario 5x sequentially and writes `baselines/hello_world_spike.json` with mean+stddev per metric. *(Maps PRD AC-04 + AC-S2-01 + AC-S2-02.)*
- [ ] **DoD-5**: Regression detector HARD-FAILS on `outcome.success=false`, `cost > hard_max`, `wall_clock > hard_max`, `stories_completed` mismatch, `dispatch_count > hard_max`. ADVISORY-WARNS on `tokens.*` and `skill_loads.*` outside mean ± 2·stddev. *(Maps PRD AC-05 + AC-S2-04 + AC-S2-05.)*
- [ ] **DoD-6**: Meta-tests in `tests/test_meta.py` pass for malformed-stream fault injection, baseline-comparison demo, and aggregator-fixture parsing; no Claude calls; complete in < 5 sec. *(Maps PRD AC-06 + AC-S3-01 through AC-S3-04.)*
- [ ] **DoD-7**: NO `.github/workflows/smoke-*.yml` exists in the repo. *(Maps PRD AC-07 + BC-01; verified by grep + dir-listing.)*
- [ ] **DoD-8**: `delivery-team/architecture/smoke-test-architecture.md` records the local-only constraint with a pointer to the binding memory file (`/home/meconnelly/.claude/projects/-var-home-meconnelly-Documents-GitHub-Claude-Plugins/memory/feedback_claude_code_local_only.md`). *(Maps PRD AC-08 + ADR-tk5-001 §Local-Only Constraint; README cites same path per AC-S3-05.)*

**Wave-level cadence**: one wave, one commit (per memory `feedback_no_skip_stages` + user-seed §Hard PO directives "full scope in one initiative; not staged"). All 8 gates verified before PR merge; no partial-merge.

---

## Open Questions

None blocking. PRD §Open Questions states "None blocking" and all five open risks have mitigations encoded in ACs above.

## Downstream Notes (for Stage 6 Development orchestrator)

- Dispatch A handles S1+S2 in sequence (producer). Dispatch B handles S3 (validator) in a fresh context; do NOT pass S1+S2 source paths into Dispatch B's working set — pass only `prd.md`, `BACKLOG-106-*.md`, and `delivery-team/architecture/smoke-test-architecture.md`.
- Capacity buffer is 8h (28.6%). If S1 overruns, S3 has slack; if S3 overruns, escalate to PO before pulling from buffer — keep validator dispatch context-clean.
- Producer-validator git evidence: Stage-7 UAT will inspect commits. If wave squashes, ensure trailers attribute the two distinct dispatch authorships.
- Stop-rule headroom is 0.289/story. Aragorn flag if any single story introduces > 0.4 defects in QA — that one story alone could trip rolling window after merge.

---

— Aragorn, Scrum Bag, run-2026-05-13-tk5. The fellowship marches at dawn. The smoke-test gate shall not fall.
