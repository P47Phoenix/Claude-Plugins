<!-- run: run-2026-05-13-tk5 -->
<!-- stage: 6 development DoD -->
<!-- author: Celebrimbor (Solution Architect, dod-validation) -->
<!-- stories: S1, S2 -->
<!-- gate: architect conformance -->
# S1+S2 Architect DoD Review

> *"Let us forge something that will endure beyond the ages."* — Celebrimbor

Caveman speak: forge get measured against blueprint. Every rivet checked.

## Verdict

**STATUS: DONE** — S1 (W6-1) and S2 (W6-2, W6-5) implementations conform to ADR-tk5-001 across all nine gate criteria.

## Gate-by-Gate Conformance

### Gate 1 — Subprocess plumbing matches ADR's "spawn isolated Claude Code subprocess" decision (not SDK)

**PASS.** `delivery-team/tests/smoke/lib/runner.py:131-141` uses `subprocess.Popen` against the `claude` CLI binary, not the Anthropic SDK. Command built at `_build_claude_command` (lines 104-111) starts with `["claude", "--print", "--output-format", "stream-json"]`. No `import anthropic` anywhere in the smoke harness.

### Gate 2 — HOME-override + `--plugin-dir` plus fallback-copy pattern in `workspace.py`

**PASS.** Both code paths exist in `delivery-team/tests/smoke/lib/workspace.py`:
- HOME override: `setup()` at lines 29-54 creates `tempfile.mkdtemp(prefix="smoke-")` and `subprocess_env()` at lines 63-71 injects `env["HOME"] = str(self.home)` plus `XDG_CONFIG_HOME` and `XDG_DATA_HOME`.
- `--plugin-dir` primary path: probe sets `plugin_load_strategy = PLUGIN_LOAD_PLUGIN_DIR` (line 50); runner adds the flag at `runner.py:109-110`.
- Fallback copy path: `_install_plugin_into_home()` at lines 107-129 recursively copies `<repo>/delivery-team` into `<home>/.claude/plugins/<name>/` with a `_ignore` function that skips `tests/smoke` (lines 118-127) — matching architecture §4 "skipping tests/smoke/ itself to avoid recursive inclusion."

### Gate 3 — Capability probe at startup wired in `runner.py` (or `workspace.py`)

**PASS.** `workspace.py:_probe_plugin_load_strategy` at lines 89-105 runs `subprocess.run(["claude", "--help"], …)` and checks `"--plugin-dir" in haystack` (stdout + stderr). Architecture §4 specifies a help-text grep ("intentionally a help-text grep rather than a feature flag — stays correct across CLI versions"). Probe fires from `setup()` at line 50 before any subprocess spawn. Gate criteria explicitly allows wiring in `workspace.py` so we are within the architecture-doc's contract.

### Gate 4 — Metrics schema in `metrics.py` matches `smoke-test-architecture.md` §5 Metrics schema

**PASS.** `Metrics` dataclass (`metrics.py:21-32`) carries:
- `wall_clock_seconds: float` (matches §5 `wall_clock_seconds: 1234.5`)
- `cost_usd: float` (matches §5 `cost_usd: 1.42`)
- `tokens: dict` with keys `input`, `output`, `cache_creation`, `cache_read` (matches §5 `tokens.*` block exactly)
- `model_usage: list` of `ModelUsage(model, dispatches, input_tokens, output_tokens, cache_creation_tokens, cache_read_tokens)` (matches §5 `model_usage[]` shape; the per-model cache fields are a superset, acceptable)
- `dispatch_count: int` (matches §5 `pipeline.dispatch_count`)

Types are correct: float for time/cost, int for token counts, list for model usage. The `report.json`-level fields (`run_id`, `git_sha`, `claude_cli_version`, `plugin_load_strategy`, `outcome`, `skill_loads`, `pipeline`, `advisory_warnings`, `hard_failures`) are out of scope for the parser — those are S3/W6-4 `report.py` concerns per the component map.

### Gate 5 — Baseline format in `baseline.py` matches `smoke-test-architecture.md` §6 Baseline format

**PASS.** `init_baseline` (`baseline.py:138-177`) emits a dict with all required top-level keys: `schema_version`, `scenario`, `n_samples`, `last_captured_utc`, `last_captured_git_sha`, `last_captured_cli_version`, `metrics`. Per-metric entries include `mean`, `stddev`, `n`, `classification`, with `hard_max` only on hard-classed entries (lines 154-163) — exactly matching §6 ("only present for hard-class metrics"). `_hard_max_for` (lines 125-135) returns the §6 values: 1800 wall-clock, 3.00 cost, 16 dispatch_count, mean for stories_completed. Schema version "1" matches.

### Gate 6 — Hard-fail vs advisory-warn classification in `compare()` matches the architecture doc's regression-detector logic

**PASS.** `compare()` (`baseline.py:274-308`) delegates to `_check_hard_rules` (lines 180-213) and `_check_advisory_rules` (lines 216-271):
- Hard-fail triggers (§7): `outcome.success == false` (line 186), each HARD_METRIC_KEY exceeding `hard_max` (line 208), strict-equality check on `pipeline.stories_completed` against baseline mean (lines 200-205). Matches §7 hard-fail list exactly.
- Advisory triggers (§7): each ADVISORY_METRIC_KEY and each `skill_loads.<skill>` checked against `mean ± 2·stddev` (lines 264-269). Zero-stddev guard (lines 257-262) is a sensible architecture-faithful extension — §7's mean±2σ rule is undefined when stddev=0, and the implementation flags exact-mean drift instead, preserving "differs from baseline" semantics.
- Status mapping (lines 293-298): hard_failures → FAIL, else advisory_warnings → WARN, else PASS. Run-time exit-code intent documented in the `compare()` docstring matches §7 (PASS=0, FAIL=1, WARN=0).

### Gate 7 — Reuse boundary preserved (telemetry hooks untouched)

**PASS.** `git status delivery-team/hooks/` returned `nothing to commit, working tree clean` on the full repo. No edits to `telemetry.py` or `telemetry_run_summary.py`. The aggregator (W6-3) is S3 scope; S1+S2 do not include any code that imports or writes to those hooks.

### Gate 8 — Local-only constraint preserved (no smoke CI workflows)

**PASS.** `find .github/workflows -name "smoke-*.yml" -type f` returned empty. Only the three permitted lint/budget/metadata workflows live in `.github/workflows/` per ADR §"Local-Only Constraint" and architecture §9.

### Gate 9 — Producer-validator separation preserved (no meta-tests, README, or Makefile in this dispatch)

**PASS.** `find delivery-team/tests/smoke -type f` shows the S1+S2 deliverables only:
- `run_smoke.py` (W6-1 CLI)
- `lib/workspace.py`, `lib/runner.py` (W6-1)
- `lib/metrics.py` (W6-2)
- `lib/baseline.py` (W6-5)
- `lib/aggregator.py`, `lib/report.py` (S3 / W6-3 / W6-4 — out of S1+S2 scope but architecturally consistent so far)
- `fixtures/delivery_config_minimal.yml`, `prompts/hello_world_spike.txt`, `baselines/.gitkeep`

NOT present (correctly): `tests/test_meta.py`, `tests/fixtures/*.jsonl` (W6-7 fault-injection fixtures), `README.md` (W6-8), and no root `Makefile` changes. BC-03 producer-validator split is preserved — the meta-test author dispatch will write fixtures from the contract only, blind to `metrics.py` and `baseline.py` source.

## Conformance Summary Table

| Gate | Criterion | Result |
|---|---|---|
| 1 | Subprocess (not SDK) | PASS |
| 2 | HOME-override + `--plugin-dir` + fallback-copy | PASS |
| 3 | Capability probe at startup | PASS |
| 4 | Metrics schema matches §5 | PASS |
| 5 | Baseline format matches §6 | PASS |
| 6 | Hard-fail vs advisory in `compare()` | PASS |
| 7 | Telemetry hooks untouched | PASS |
| 8 | No smoke CI workflows | PASS |
| 9 | No meta-tests / README / Makefile in this dispatch | PASS |

## Observations (Non-Blocking)

1. **Probe location.** ADR §4 places the capability probe in `runner.py`; the implementation places it in `workspace.py:_probe_plugin_load_strategy` and surfaces `plugin_load_strategy` as a `Workspace` attribute. The gate criterion explicitly allows either location, and the resulting decoupling (workspace owns plumbing decisions, runner consumes them) is architecturally cleaner. Consider updating architecture §4 prose during a documentation pass to reflect actual location — not a defect, a doc-code drift item.
2. **Aggregator + Report already present.** `lib/aggregator.py` and `lib/report.py` exist on disk but are not in S1+S2 scope per the Stage-5 Plan. They appear to belong to S3 / W6-3 / W6-4. If a separate Dev dispatch is supposed to author those modules, the orchestrator should confirm dispatch assignment matches reality. Not a Stage-6 architect-DoD blocker for S1+S2.
3. **Cache-token fields in `ModelUsage`.** Per-model `cache_creation_tokens` and `cache_read_tokens` are tracked in the dataclass but `report.json` §5 example only shows aggregate cache fields. Acceptable superset — preserves data for future report-shape evolution without breaking §5 today.

## Architecture Risks (Acknowledged in ADR)

None new. Risks documented in ADR-tk5-001 "Consequences" (small-n stddev, $15 init envelope, subprocess fidelity loss to future in-process plugin loading, local-only friction, Stop-hook blocking) remain unchanged by S1+S2 implementation.

## Open Questions for Stage 7 UAT

1. Live-subprocess capability-probe exit (line 99 `FileNotFoundError, OSError`) returns `PLUGIN_LOAD_COPY_INTO_HOME` silently. UAT should confirm that on a developer machine without `claude` in `PATH`, the fallback path is intentional rather than masking a setup error. The runner will then fail at spawn (line 142-151 returns exit_code 4 / `plumbing-error:`), which is correct loud-fail behavior — but the probe's silent fallback could be logged.

## Conclusion

S1+S2 implementations match ADR-tk5-001 and `smoke-test-architecture.md` across every binding decision: subprocess plumbing, HOME-override + `--plugin-dir` + fallback-copy, capability probe, metrics schema, baseline format, regression-detector classification, telemetry reuse, local-only invocation, producer-validator separation. **Architect DoD: DONE.**

---

*— Celebrimbor, Stage 6 Architect DoD, run-2026-05-13-tk5. Forge holds true.*
