<!-- run: run-2026-05-13-tk5 -->
<!-- reviewer: Legolas (QA, Stage 4 DoD validation) -->
<!-- artifact-under-review: delivery-team/architecture/smoke-test-architecture.md + ADR-tk5-001 -->
<!-- backlog: BACKLOG-106 -->

# Stage 4 Architect DoD — QA Testability Review

> *"That bug still only counts as one."* — Legolas

**Status**: DONE
**Verdict**: All 7 testability gates PASS. Architecture and ADR are testable; Stage 7 UAT gate-set is artifact-mappable; producer-validator separation is observable from git artifacts.

Me Legolas. Me sharp-eyed. Me check each gate against actual file contents. No gate skipped, no metric un-classified, no gap papered over.

---

## Gate-by-Gate Findings

### Gate 1 — Metrics schema fields each have a concrete type (no TBD)

**Status**: PASS

Architecture §5 (`report.json` schema) inspected field by field. Every leaf is one of: string, int, float, bool, nullable-string, object, or array. Specifically:

| Field | Concrete Type |
|---|---|
| `schema_version` | string |
| `run_id` | string |
| `git_sha` | string |
| `claude_cli_version` | string (nullable per §5 last paragraph) |
| `plugin_load_strategy` | string enum (`"plugin-dir" \| "copy-into-home"`) |
| `outcome.success` | bool |
| `outcome.exit_code` | int |
| `outcome.reason` | string-or-null |
| `wall_clock_seconds` | float |
| `cost_usd` | float |
| `tokens.input` / `tokens.output` / `tokens.cache_creation` / `tokens.cache_read` | int |
| `model_usage[]` | array of objects (model: string, dispatches: int, input_tokens: int, output_tokens: int) |
| `pipeline.stages_completed` / `stories_completed` / `dispatch_count` / `defects_logged` | int |
| `skill_loads[]` | array of objects (skill: string, count: int, prose_tokens_mean: float) |
| `advisory_warnings[]` | array |
| `hard_failures[]` | array |

Grep for "TBD" across both architecture doc and ADR returns zero hits. §5 explicitly states fields that cannot be measured emit `null` rather than being omitted — schema shape stays stable. No placeholder types.

### Gate 2 — Regression detector logic distinguishes hard-fail from advisory-warn; each metric classified

**Status**: PASS

Architecture §7 splits the detector into two named classes ("HARD-FAIL (exit code 1)" vs "ADVISORY-WARN (exit code 0)") with explicit predicate lists for each. §6 baseline shape adds a per-metric `"classification": "hard" | "advisory"` field so classification is data-driven, not name-driven.

Every metric in §6 is classified explicitly:

| Metric | Classification |
|---|---|
| `wall_clock_seconds` | hard (hard_max: 1800) |
| `cost_usd` | hard (hard_max: 3.00) |
| `pipeline.dispatch_count` | hard (hard_max: 16) |
| `pipeline.stories_completed` | hard (hard_max: 1; strict equality since stddev=0) |
| `tokens.input` / `output` / `cache_creation` / `cache_read` | advisory (2σ band) |
| `skill_loads.delivery-team:product-delivery` / `:architect` / `:developer` | advisory (2σ band) |
| `outcome.success` | hard by structural definition (§6 last paragraph + §7 first bullet) |

§7 also defines missing-metric behavior: unknown metrics in report → `unknown_metric` log only; baseline metrics missing from report → hard-fail iff `classification == "hard"`, otherwise advisory. Both branches testable.

### Gate 3 — Baseline format supports 5-sample mean+stddev (n_samples field present)

**Status**: PASS

Architecture §6 baseline JSON has:
- Top-level `"n_samples": 5`
- Each per-metric entry carries `"n": 5`

Both fields present, so 5-sample mean+stddev calculation is statable AND verifiable per-metric (per-metric `n` allows partial-sample handling later). ADR §"Decision" item 3 also locks `--init-baseline` to 5× sequential runs with concurrency-of-1.

### Gate 4 — Meta-tests scope (W6-7) explicitly enumerates the 3 test scenarios

**Status**: PASS

Three scenarios enumerated in three independent places (cross-checked):

1. **Architecture §3 Component Map**, W6-7 row: "malformed-stream fault injection, baseline-comparison demo, aggregator-fixture parsing"
2. **BACKLOG-106 W6-7 acceptance**: same three, named identically
3. **User-seed AC-06**: same three, named identically

Cross-reference passes — no scenario added, removed, or renamed across artifacts.

### Gate 5 — Cost-cap test path is concrete (synthetic stream injection named)

**Status**: PASS

Cost-cap test path named in three layers:

1. **Detector predicate** (Architecture §7): `cost_usd > metrics.cost_usd.hard_max` — exact predicate, hard-class.
2. **Synthetic injection mechanism** (BACKLOG-106 W6-7 acceptance + architecture §3 component map): "baseline-comparison demo (synthetic inputs trip hard-fail and advisory-warn paths deterministically)" — synthetic inputs live in `tests/fixtures/baseline_*.json` per the file surface inventory.
3. **Fixture file enumeration** (BACKLOG-106 File Surface Inventory): `delivery-team/tests/smoke/tests/fixtures/baseline_*.json` (NEW, W6-7) — named, not hand-waved.

Meta-test reads a synthetic `report.json` with `cost_usd` set above `hard_max`, feeds it to `lib/baseline.py`, asserts exit code 1. Concrete: synthetic JSON fixture → baseline comparator → exit code assertion. No live Claude call needed.

### Gate 6 — Producer-validator separation between W6-7 and W6-2/W6-5 is testable from git/log artifacts

**Status**: PASS

Three observability surfaces:

1. **ADR §"Producer-Validator Separation"** (line 39): "Stage-7 UAT verifies the git history shows two separate Dev commits (or two separate commit authors within a squash) for the producer and validator halves."
2. **BACKLOG Stage 6 handoff** (line 191): "Each story = one PR-equivalent commit. Validator Dev MUST NOT read the producer Dev's `lib/metrics.py` or `lib/baseline.py` source while authoring fixtures."
3. **Architecture §3 Component Map**, W6-7 row: marks the row as "Validator side of producer-validator pair (BC-03) — different Dev dispatch than W6-2 / W6-5."

Separation testable post-merge via `git log --follow delivery-team/tests/smoke/lib/metrics.py` and `git log --follow delivery-team/tests/smoke/tests/test_meta.py` — distinct dispatch IDs (or distinct commit authors within a squash) must appear. Observable artifact-based test, not opinion-based.

### Gate 7 — Stage 7 UAT gate-set (8 gates) mappable to architecture deliverables

**Status**: PASS

User-seed AC-01 through AC-08 enumerated; each mapped to a named artifact in architecture or ADR. Discipline: every AC has a corresponding deliverable. Memory lesson applied — QA must enumerate ALL ACs by ID.

| AC | Statement (abbreviated) | Mapped Artifact |
|---|---|---|
| **AC-01** | `run_smoke.py` completes in < 30 min wall-clock | Architecture §3 (`run_smoke.py` + `lib/runner.py` with `--timeout`); §6 baseline `wall_clock_seconds.hard_max = 1800`; ADR Decision 1 |
| **AC-02** | Output to `artifacts/<utc-timestamp>/{report.json, summary.md, stream.jsonl}` | Architecture §3 `lib/report.py` row ("Schema in §5"); §5 schema header |
| **AC-03** | `report.json` fields (outcome, wall_clock, cost, tokens.*, model_usage, pipeline.*, skill_loads, git_sha, claude_cli_version) | Architecture §5 — every named field present |
| **AC-04** | `--init-baseline` runs 5× → `baselines/hello_world_spike.json` with mean+stddev | Architecture §6 (full schema, `n_samples: 5`); ADR Decision 3 |
| **AC-05** | Hard-fail / advisory-warn detector predicates | Architecture §7 (both classes with explicit predicate lists) |
| **AC-06** | Meta-tests (malformed-stream, baseline-demo, aggregator-fixture) pass | Architecture §3 W6-7 row; BACKLOG W6-7 acceptance |
| **AC-07** | NO `.github/workflows/smoke-*.yml` exists | Architecture §9 (binding); ADR Decision 4 + §"Local-Only Constraint" |
| **AC-08** | Architecture doc records local-only with memory file pointer | Architecture §9 (cites memory file by full path); ADR §"Local-Only Constraint" (cites same memory file) |

All 8 ACs mappable. No orphan ACs. No orphan architecture sections (every major section serves at least one AC).

---

## Producer-Validator Spot-Check (BC-03 reinforcement)

Me Legolas note this for Scrum Bag at Stage 5: BC-03 binding is the kind of rule that breaks silently if dispatch assignment slips. Architecture and ADR are CLEAR on the rule. Risk lives at Stage 5 Plan, not Stage 4 Architect. Stage 4 has done its job — contract is observable post-merge via git artifacts. Scrum Bag must honor it.

---

## Shared-Module Review

No shared modules modified during this stage. Stage 4 is design-only — no code touched. Review not applicable to this DoD pass. (Review will activate at Stage 7 UAT once Stage 6 Dev modifies any shared files.)

---

## Risks / Gaps Identified (informational, not blocking)

1. **Skill-load granularity gap** (Architecture §10 Open Question 1): If a future regression needs per-invocation token detail, the schema must grow. Architect explicitly defers. Acceptable — defer-with-rationale is a valid testable choice and the gap is documented.
2. **state.md schema-drift fragility** (Architecture §10 Open Question 2): Aggregator silently under-reports if `state.md` format changes. Architect commits to monitoring first 5 runs and adding a schema-version check via follow-up BACKLOG. Acceptable — has owner, has trigger.
3. **5-sample stddev underestimates variance** (ADR Consequences > Negative, BACKLOG Risk Register row 4): Mitigated by 2σ-then-1.5σ tightening policy after 20+ production runs. Acceptable — has explicit re-evaluation gate.

None of these block Stage 4 sign-off. All have documented owners and trigger conditions.

---

## Assumptions

- Stage 5 Plan will honor BC-03 dispatch assignment (validator Dev ≠ producer Dev). If Stage 5 collapses both halves into one dispatch, Stage 6 will violate BC-03 and Stage 7 UAT will hard-fail on git-history check.
- The `claude` CLI's `--plugin-dir` flag behavior matches the capability-probe assumption (help text grep). If the CLI changes its help-text format without changing flag semantics, probe misroutes to fallback — non-fatal but worth flagging in Stage 6 Dev review.
- The fixture corpus authored by the validator Dev covers malformed-stream cases the producer Dev did NOT consider. Whole point of producer-validator separation; cannot be verified at Stage 4 — will be verified at Stage 6 by code review of fixture diversity.

---

## Summary Scoreboard

| Gate | Verdict | Blocking? |
|---|---|---|
| 1. Metrics schema fields concrete-typed (no TBD) | PASS | — |
| 2. Detector splits hard-fail vs advisory-warn; every metric classified | PASS | — |
| 3. Baseline `n_samples` field present supports 5-sample mean+stddev | PASS | — |
| 4. Meta-tests scope enumerates 3 named scenarios (W6-7) | PASS | — |
| 5. Cost-cap test path concrete (synthetic stream injection named) | PASS | — |
| 6. Producer-validator separation observable from git/log artifacts | PASS | — |
| 7. Stage 7 UAT 8-gate set mappable to architecture deliverables | PASS | — |

**Overall STATUS: DONE.** Zero blocking gaps.

---

## Signal Block

STATUS: DONE
ARTIFACT: /var/home/meconnelly/Documents/GitHub/Claude-Plugins/.delivery/artifacts/04-architect/dod/qa-review.md
SUMMARY: All 7 gates pass. Schema fully typed, detector classes split, n_samples=5 present, 3 meta-tests enumerated, cost-cap synthetic injection named, producer-validator git-observable, 8 ACs all mapped.

*— Legolas, Stage 4 QA reviewer, run-2026-05-13-tk5. Bug still only counts as one; me count zero today.*
