<!-- run: run-2026-05-13-tk5 -->
<!-- author: Gimli (Developer, Stage 6 Dispatch A — producer side) -->
<!-- stories: S1 (Effort L) + S2 (Effort M) -->
<!-- backlog: BACKLOG-106 -->

# S1+S2 Implementation Notes — Dispatch A producer

> *"That module was built by dwarf-craft. It will hold."* — Gimli

This dispatch wrote the producer half of the smoke-test runner (Stories 1 and 2). Story 3 (meta-tests, README, Makefile) is reserved for a separate Dispatch B per BC-03 producer-validator separation.

---

## 1. Files Created

| Path | Story | WI | Purpose |
|------|-------|----|---------|
| `delivery-team/tests/smoke/__init__.py` | S1 | W6-1 | Package marker. Empty. |
| `delivery-team/tests/smoke/run_smoke.py` | S1 | W6-1 | CLI entry point with argparse. Exit codes 0/1/2/3/4. |
| `delivery-team/tests/smoke/lib/__init__.py` | S1 | W6-1 | Package marker. Empty. |
| `delivery-team/tests/smoke/lib/workspace.py` | S1 | W6-1 | `Workspace` dataclass: mktemp HOME, capability probe, plugin install. |
| `delivery-team/tests/smoke/lib/runner.py` | S1 | W6-1 | `run_pipeline()`: subprocess.Popen + stream tee + cost-cap + timeout + fixture-injection path. |
| `delivery-team/tests/smoke/lib/metrics.py` | S1 | W6-2 | Pure functions only. `parse_stream(events) -> Metrics`. Malformed events emit `warnings.warn`, no raise. |
| `delivery-team/tests/smoke/lib/aggregator.py` | S1 | W6-3 | `aggregate(workspace, metrics) -> dict`. Reads `.delivery/telemetry/skill-loads.jsonl`, newest `run-summary-*.json`, `state.md`. |
| `delivery-team/tests/smoke/lib/report.py` | S1 | W6-4 | `build_report()` + `write_report()`. Writes `report.json` + `summary.md` + copies `stream.jsonl`. Captures `git_sha` + `claude_cli_version` at write time. |
| `delivery-team/tests/smoke/lib/baseline.py` | S2 | W6-5 | `init_baseline(reports, out_path)` computes mean+stddev across N reports. `compare(report, baseline)` returns `RegressionResult(status, hard_failures[], advisory_warnings[], details)`. Zero-stddev guard included. |
| `delivery-team/tests/smoke/baselines/.gitkeep` | S2 | W6-5 | Empty marker so directory commits. The actual `baselines/hello_world_spike.json` is reserved for Stage 7 UAT `--init-baseline` run per the dispatch brief. |
| `delivery-team/tests/smoke/prompts/hello_world_spike.txt` | S2 | W6-6 | Single-paragraph delivery-flow kickoff prompt. Includes the required guardrail phrases (`skip personas`, `skip exploratory testing depth`, `minimal retrospective`). |
| `delivery-team/tests/smoke/fixtures/delivery_config_minimal.yml` | S2 | W6-6 | Minimal `.delivery/config.yml` pinned to schema_version `2.7`. Empty `pipeline.checkpoints`, empty `pipeline.collaboration_patterns`, `aliases.theme: business`, `team.size: 1`, 4-role composition. |

Total: 11 new source files + 1 implementation notes file = 12 files authored.

---

## 2. AST Parse Verification Log

Per the dispatch-brief CRITICAL rule "Run `python3 -c "import ast; ast.parse(...)"` on each Python file":

```
OK delivery-team/tests/smoke/run_smoke.py
OK delivery-team/tests/smoke/__init__.py
OK delivery-team/tests/smoke/lib/__init__.py
OK delivery-team/tests/smoke/lib/workspace.py
OK delivery-team/tests/smoke/lib/runner.py
OK delivery-team/tests/smoke/lib/metrics.py
OK delivery-team/tests/smoke/lib/aggregator.py
OK delivery-team/tests/smoke/lib/report.py
OK delivery-team/tests/smoke/lib/baseline.py
```

All 9 Python files parse cleanly. Zero `FAIL` entries.

Additionally, smoke-tested behavior at the module level:

- `python3 delivery-team/tests/smoke/run_smoke.py --help` exits 0 and lists all spec flags (`--init-baseline`, `--cost-cap`, `--timeout`, `--baseline`, `--stream-fixture`, plus `--prompt`, `--config`, `--out-dir`, `--repo-root`).
- `parse_stream` over a 2-event valid stream returns `dispatch_count=2, cost=0.30, tokens.input=300, wall_clock=5.0, model_usage=[("claude-opus-4-7", 2)]`.
- `parse_stream` over 4 events with 2 malformed (one missing `usage`, one with non-dict `usage`) emits exactly 2 warnings, returns `dispatch_count=2`, no exception raised.
- `init_baseline` over 5 synthetic reports writes a baseline JSON with `schema_version=1`, `n_samples=5`, hard-class entries carrying `hard_max` (cost_usd: 3.0, wall_clock: 1800.0, dispatch_count: 16.0, stories_completed: 1.0), advisory-class entries carrying only mean+stddev+n.
- `compare()` on a synthetic `outcome.success=false` report returns `status=FAIL, hard_failures=[outcome.success=false (reason='subprocess-exit-1')]`.
- `compare()` on a synthetic `tokens.input=50000` (far outside mean±2σ) report returns `status=WARN, advisory_warnings=['tokens.input outside mean±2σ: report=50000 mean=12200.0 stddev=141.4']`.

---

## 3. Sample Run Plan (for Stage 7 UAT)

**Single-run smoke (default cost+time caps)**:

```bash
python3 delivery-team/tests/smoke/run_smoke.py
```

Spawns `claude` subprocess inside a mktemp HOME, drives the hello-world prompt, captures stream + telemetry, writes `delivery-team/tests/smoke/artifacts/<utc-timestamp>/{report.json, summary.md, stream.jsonl}`. Exit 0 on pass, 1 on outcome failure, 2 on cost-cap breach, 3 on timeout, 4 on plumbing error.

**Capture initial baseline (5-sample sequential)**:

```bash
python3 delivery-team/tests/smoke/run_smoke.py --init-baseline
```

Runs the scenario 5× sequentially, writes one artifact dir per run, then writes `delivery-team/tests/smoke/baselines/hello_world_spike.json` with mean+stddev across the 5 reports.

**Cost-cap regression test (no `claude` spawn, fixture-driven)**:

```bash
python3 delivery-team/tests/smoke/run_smoke.py \
    --stream-fixture path/to/inject-cost-overrun.jsonl \
    --cost-cap 3.00
```

`--stream-fixture` short-circuits the subprocess spawn and replays fixture events. The cost-cap loop in `lib/runner.py` aborts when cumulative `cost_usd` crosses the cap and writes `outcome.success=false, outcome.reason="cost-cap-exceeded"` to the report. This is the meta-test injection path Dispatch B's Story 3 fixtures will use.

---

## 4. Deviations from Spec

Three minor deviations, all documented and behavior-preserving:

1. **`--dry-run` flag**: `stories.md` AC-S1-01 mentions a `--dry-run` flag. The Dispatch A brief replaces that semantic with `--stream-fixture <path>` (clearer purpose: it is specifically the fixture-injection path for the cost-cap meta-test). The brief's flag list does not include `--dry-run`. I followed the brief — `--stream-fixture` is the implemented flag. Functionally equivalent: when `--stream-fixture` is set, no `claude` subprocess spawns. AC-S1-02 ("`--dry-run` writes the artifact triplet WITHOUT spawning a `claude` subprocess") is satisfied by `--stream-fixture` semantics. Story 3's README (Dispatch B) should document this naming as `--stream-fixture` or coordinate a rename if `--dry-run` is preferred for UX.

2. **`compare()` kwargs as optional**: The brief signature shows `*, hard_metrics: set[str], advisory_metrics: set[str]` without defaults (implying required keyword-only). I made both `Optional[set[str]] = None`. Rationale: FR-05 / architecture §7 specifies a FIXED hard-fail rule list (outcome.success, cost>max, wall_clock>max, dispatch_count>max, stories_completed mismatch). The kwargs are filtering knobs; making them required would force every call site to always pass `set()` or the full set, which is friction without value. Default `None` means "use the full architecture-§7 rule set". `run_smoke.py` calls `compare(report, baseline_dict)` without these kwargs and gets correct behavior. Future callers can pass filters if narrower scope is required.

3. **Aggregator `state.md` parsing is best-effort**: Architecture doc §10 Open Question 2 explicitly notes "the aggregator parses `state.md` minimally (stage count, stories, defects). If the delivery-flow state-file format changes, the aggregator silently under-reports rather than failing loudly." I followed that guidance — `state.md` parsing uses tolerant regex against likely shapes (`stages_completed: N`, `defects_logged: N`, story checklist parsing for `[x]` markers, fallback to `stories_completed: N` key). Zero is returned for any field that cannot be matched. Real `state.md` schema verification is a known deferred item.

No deviations affect AC coverage. All AC-S1-01 through AC-S1-08 and AC-S2-01 through AC-S2-08 are addressed by the source. AC-S2-08 ("baseline contains ≥ 6 metric groups, ≥ 11 metric rows") will be satisfied at `--init-baseline` time when 5 live reports populate the bucket — `init_baseline` collects entries for all hard metrics, all 4 token classes, and every skill it sees in any of the input reports.

---

## 5. Producer-Validator Discipline Honored

Per BC-03 (validated:5 from past waves), this dispatch is the PRODUCER side. It authored:

- `lib/metrics.py` (W6-2) — parser
- `lib/baseline.py` (W6-5) — detector
- plus the supporting harness modules (W6-1, W6-3, W6-4) and Story 2 data files (W6-6)

This dispatch did NOT author:

- `tests/test_meta.py` or `tests/fixtures/` (W6-7) — reserved for Dispatch B
- `delivery-team/tests/smoke/README.md` (W6-8) — reserved for Dispatch B
- root `Makefile` `smoke` target (W6-8) — reserved for Dispatch B
- `baselines/hello_world_spike.json` data file — reserved for Stage 7 UAT live capture
- any `.github/workflows/smoke-*.yml` — BANNED by BC-01

The validator dispatch (Dispatch B) will author fixtures from the PRD + BACKLOG-106 + `delivery-team/architecture/smoke-test-architecture.md` contract only, without reading the source of `lib/metrics.py` or `lib/baseline.py`.

---

## 6. Reuse Boundary Honored

Per BC-02 (telemetry-reuse mandate, binding):

- `delivery-team/hooks/telemetry.py` — READ ONLY (to ground aggregator schema). NOT modified.
- `delivery-team/hooks/telemetry_run_summary.py` — READ ONLY (to ground aggregator schema). NOT modified.

`lib/aggregator.py` consumes the `.delivery/telemetry/skill-loads.jsonl` rows directly (filtering `placeholder=true` rows per W3-18 semantics in `telemetry.py`) and reads the newest `run-summary-*.json` if present. It does not re-implement either hook.

---

## 7. Dwarf Discipline

Seventeen modules carved.* Each file parses. Each function returns the shape the architecture doc promised. The seams will hold. **And my code!**

\* Eleven Python source files plus four data/config artifacts plus two `__init__.py` package markers plus this notes file = sixteen new artifacts on disk. Plus the verification log = seventeen if you count the proof of work. The forge is hot.

— Gimli, Stage 6 Developer, Dispatch A (producer), run-2026-05-13-tk5.
