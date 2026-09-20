# ADR-lmr-004: Smoke harness model-capture contract (parser, interfaces, baseline schema, cost cap)

- **Status**: Proposed (flips to Accepted when Stage 4 DoD passes)
- **Date**: 2026-09-20
- **Run**: run-2026-05-28-o48m, BACKLOG-108
- **Owner**: Solution Architect (PRD S5: FR-5.1 to FR-5.10, FR-4.4, BINDING-4.5; Architect DoD round-2 findings F2, F3, F4, F6, F7)

## Context

The PRD fixes what S5 must achieve. Round-2 Architect review found four gaps the PRD leaves to the implementer, and reading the current `delivery-team/tests/smoke/` code (this stage) found four more constraints. This ADR pins the contract so the producer and the separate validator dispatch (BINDING-4.5) can work against the same interface, and so the red-first test can exist before the fix.

Evidence read in this stage:
- `lib/metrics.py::parse_stream` reads `event.get("usage")` and `event.get("model")` at top level only, counts every `assistant|message|tool_use|result` event that has usage as one dispatch, and buckets a missing model as `"unknown"`. Real streams (PRD S5 table, one local capture on CLI 2.1.278) nest model and usage under `message`, carry the model on `system/init`, and put cost only on the final `result` (`total_cost_usd`, `modelUsage`).
- `lib/runner.py::_running_cost` sums per-event `usage.cost_usd`; `_build_claude_command(workspace, prompt_path)` takes no model, effort or cap.
- `lib/baseline.py::_collect_metric_values` collects only `HARD_METRIC_KEYS`, `ADVISORY_METRIC_KEYS` and `skill_loads.*`; `_check_advisory_rules` already ignores every other key. Consequence: the PRD's "skip `model_usage.*` in the two check functions" is a no-op. The real work is to COLLECT the dynamic keys into `metrics` so AC-5.1 can find them, with a classification that never becomes hard or advisory.
- `run_smoke.py::_execute_single_run` loads `--baseline` from disk for every sample, including during `--init-baseline`, and calls `compare()` when the run exit is 0. During re-capture that would compare each new sample against the invalidated old baseline.
- `tests/test_meta.py` (must stay at exactly 3 tests, AC-4.2 requires it to pass) feeds legacy flat events (top-level `model` and `usage`, `assistant, assistant, result`) and asserts `dispatch_count == 3`, `cost_usd == 0.30` (summed `usage.cost_usd`), tokens summed. `tests/conftest.py` has an autouse fixture that makes any `subprocess` call whose first token is `claude` raise `AssertionError`. `lib/baseline.py::_claude_cli_version()` and `lib/report.py::_claude_cli_version()` run `claude --version`, so a test that calls `init_baseline` or `build_report` without patching them fails.
- `system/init` reports the model: docs https://code.claude.com/docs/en/headless ("The `system/init` event reports session metadata including the model, tools, MCP servers, and loaded plugins.", fetched 2026-09-20). The docs do not name the field; top-level `model` is OBSERVED on CLI 2.1.278 only (PRD table). Subagent messages appear in the stream as `assistant` and `user` messages whose `parent_tool_use_id` is the spawning tool call, `null` for the main conversation (same page). `message.id` on assistant events and the exact budget-stop result subtype (`error_max_budget_usd`; a summary of https://code.claude.com/docs/en/agent-sdk/typescript lists this subtype but the fetch was truncated) are UNVERIFIED and must be settled by the real-shape fixture, not assumed.

## Decision

### 1. Parser rules (`lib/metrics.py`) — additive, backward compatible

`parse_stream(events) -> Metrics` keeps its signature and the legacy behaviour, and adds real-shape handling:

1. **Legacy shape** (event has no `message` object and no `modelUsage`/`total_cost_usd`): unchanged. Each `assistant|message|tool_use|result` event with top-level `usage` is one dispatch; cost from `usage.cost_usd`; model from top-level `model`. This keeps `test_meta.py` green.
2. **Real shape, assistant events**: model = `message.model`, usage = `message.usage`. Dispatches are counted per DISTINCT `message.id`; when the same `message.id` appears on several events (one API message streamed as several events, Architect F3), keep the LAST usage seen for that id (usage on split events repeats or accumulates; taking the last never double counts). If `message.id` is absent on an event, fall back to counting the event (and the fixture test records that the real stream carries ids or not).
3. **Subagent attribution**: an assistant event with a non-null `parent_tool_use_id` belongs to a subagent. Its model is bucketed like any other model; it counts as a dispatch under its own `message.id`. The primary model is never inferred from these.
4. **Real shape, `result` event** (has `modelUsage` or `total_cost_usd`): it is the authoritative aggregate. It is NOT counted as a dispatch and its `usage` is NOT added on top of per-message usage. `cost_usd` = `total_cost_usd`. Top-level token totals and per-model tokens come from `result.usage` and `result.modelUsage` when present; per-message sums are the fallback when there is no result event. Cross-checks between per-message sums and result totals are recorded by the validator's fixture test as observed facts; equality is NOT asserted a priori (result totals may include subagent tokens the stream omits by default). AC-5.9's `dispatch_count` assertion is "equals the number of distinct `message.id` values in the fixture", not `>= 1`.
5. **Model absence**: an event or bucket with no model is not bucketed as `unknown`; it is reported as absent (a warning) and capture (item 7) fails. `unknown` in any case and the empty string are treated as absent everywhere.
6. **`Metrics` additions** (all with defaults so existing constructors work): `model_primary: str | None` (`system/init` top-level `model`), `models_observed: list[str]`, and a property or field for `tokens.cache_hit_ratio = cache_read / (cache_read + cache_creation + input)`, `0.0` on a zero denominator (FR-5.1). `model_usage` stays a list of `ModelUsage` so `report.py` output and `test_meta.py` keep working.
7. **Capture failure** raises `ModelCaptureError` (new, in `lib/metrics.py`) when: no model string observed; only `unknown`/empty observed; or `system/init` is missing or has no model. The CLI maps it to a non-zero exit (see 4).

### 2. Interfaces pinned before the validator starts (Architect F4)

These are the names, parameters and return shapes the validator tests against. The producer lands them as a **stub commit** first (signatures and legacy-compatible behaviour, no fix), so `lib/` is stable from `validator_start` to `validator_end`.

| Function (file) | Signature | Contract |
|---|---|---|
| `_build_claude_command` (`runner.py`) | `(workspace, prompt_path, *, model: str = "opus", effort: str = "xhigh", max_budget_usd: float \| None = None) -> list[str]` | Existing two-positional call still works. Adds `--model <model>`, `--effort <effort>`; when the cap is not None adds `--max-budget-usd <cap formatted "%.2f">` (so 3.00 becomes `3.00`). |
| `_running_cost` (`runner.py`) | `(events: list[dict]) -> float` | If a real-shape `result` event with numeric `total_cost_usd` exists, return that value; otherwise the legacy sum of per-event `usage.cost_usd`. Never both added. |
| `run_pipeline` (`runner.py`) | existing keyword args plus `model="opus"`, `effort="xhigh"` | Passes them to `_build_claude_command` with `max_budget_usd=cost_cap`. |
| `parse_stream` (`metrics.py`) | unchanged | Rules in section 1. |
| `check_model_capture` (`metrics.py`) | `(metrics: Metrics) -> list[str]` | Returns `model_resolved` (element 0 = `model_primary`, rest ordered by dispatch count descending, ties alphabetical, primary excluded from the tail). Raises `ModelCaptureError` under the failure rule. Pure, no I/O. |
| `check_model_consistency` (`baseline.py`) | `(reports: list[dict]) -> None` | Raises `ModelMovedError` naming both models when `model_resolved[0]` differs between samples. Pure. `init_baseline` calls it. |
| `load_baseline` (`baseline.py`) | `(path: Path) -> dict` | Raises `BaselineSchemaError` (message contains `re-capture`) when `schema_version != "2"`. Used by `run_smoke.py` only; `compare()` still accepts any dict, so `test_meta.py` fixtures with `schema_version "1"` keep passing. |
| `compare` (`baseline.py`) | signature unchanged; adds the `model moved: baseline=<X> run=<Y>` WARN | `strict_model: bool = False` keyword; when true and models differ the result status is FAIL and the text says the baseline must be re-captured. |

Exit-code mapping in `run_smoke.py` (existing table: 0 pass, 1 outcome-fail, 2 cost-cap, 3 timeout, 4 plumbing): `ModelCaptureError` maps to 4 with its message; `ModelMovedError` and `BaselineSchemaError` map to 4; a strict-model FAIL maps to 1. CLI budget stop maps to 2 (item 4).

### 3. Baseline schema version 2

`SCHEMA_VERSION` in `baseline.py` and `report.py` becomes `"2"`. The baseline is re-captured and never merged (FR-5.6), so there is no compatibility burden. New top-level fields (copied from the per-sample reports, not aggregated as numbers): `model_requested`, `model_resolved` (list), `model_pin_env` (four env vars, null when unset), `effort`, `host_context` (`{"bare": bool, "claude_code_version": str}`), `samples` (`[{"stream_file", "stream_sha256"}]`, 5 entries). `host_context.claude_code_version` is the authoritative CLI version for the baseline; the existing `last_captured_cli_version` stays as the same value for old readers (one source, written twice from one variable). `tokens.cache_hit_ratio` joins `ADVISORY_METRIC_KEYS`. Model keys are flat, `model_usage.<model>.dispatches`, with `classification: "informational"`: they are collected by a new collector in `_collect_metric_values` (per sample, value 0 when a model is absent from that sample), and `_classify` returns `informational` for any key starting `model_usage.`. Nothing splits these keys on `.`; code that needs the model or the suffix uses `removeprefix("model_usage.")` and `rsplit(".", 1)`, because provider-prefixed IDs contain dots and colons (Architect F2).

`model_usage.*` is excluded from per-key threshold comparison (FR-5.7) by construction: it has no `hard_max`, is not in `HARD_METRIC_KEYS`, and `_check_advisory_rules` only walks `ADVISORY_METRIC_KEYS` and `skill_loads.*`. The producer adds an explicit `startswith("model_usage.")` skip and a comment in both check functions so the intent survives a later refactor; AC-5.7(ii) tests it.

### 4. Cost cap, two layers, and budget-stop handling (Architect F6)

Layer 1: the runner passes `--max-budget-usd <cap>` (present in local `claude --help`, CLI 2.1.278). Layer 2: after the run, `_running_cost` reads `total_cost_usd`. Because the CLI checks budget between turns (behaviour UNVERIFIED), a sample can end slightly above the cap; NFR-1 is enforced by the layer-2 post-check. A `result` event whose `subtype` is not `success` or whose `is_error` is true is an outcome failure. If the subtype contains `budget` (the documented name `error_max_budget_usd` is UNVERIFIED, so match by substring) OR observed cost exceeds the cap, the exit is 2 (cost-cap), not 4, and the sample MUST NOT be passed to `--init-baseline` (the flow aborts on exit 2, as it already does for 2, 3 and 4). The model-capture failure check must not run on an aborted sample, so a budget stop is never reported as "no model".

### 5. `--init-baseline` and the old baseline

`--init-baseline` runs its 5 samples with the baseline comparison disabled (skip `compare()` and `load_baseline`), and writes a fresh file. It never merges. The per-sample raw stream (trimmed `system/init`: `type`, `subtype`, `model`, `session_id`) is written to `.delivery/artifacts/06-development/smoke-streams/sample-<n>.jsonl` with SHA-256 in `samples`. The five samples must have distinct `session_id` values and distinct hashes (QA W4; a copied stream is rejected by `--init-baseline`; AC-5.5c also checks it independently). Regression runs (not init) load with `load_baseline`.

### 6. Producer/validator ordering (BINDING-4.5, FR-4.4)

1. **P0 producer stub commit** (Dispatch-Id A): section 2 signatures and `ModelCaptureError`, `ModelMovedError`, `BaselineSchemaError` classes with legacy-compatible bodies. `test_meta.py` still passes.
2. **V validator dispatch** (Dispatch-Id B, `validator_start` = HEAD after P0): writes `tests/test_model_capture.py` and `tests/fixtures/stream_real_shape.jsonl` plus `stream_real_shape.provenance.txt`. Rules for the test file: no module-level import of new names (imports inside test bodies, as `test_meta.py` does), so the file collects against `main`'s unfixed `lib/` for the red run (AC-5.9b needs exit 1, not a collection error, which is exit 2); every `real_shape` assertion message states the defect it detects (`unknown` bucket, `cost_usd 0.0`), so QA W1's "fails for the right reason" is checkable; the conftest guard is respected by patching `lib.baseline._claude_cli_version` and `lib.report._claude_cli_version` where `init_baseline` or `build_report` is called; model strings come from the fixture or synthetic IDs, never literals; test names are the ones in AC-5.2, AC-5.4b, AC-5.5b, AC-5.7, AC-5.9 plus the capture-failure set QA W3 lists. `validator_end` = HEAD when V returns; `lib/` diff between start and end must be empty.
3. **P1 producer fix commit(s)** (Dispatch-Id A or A2, any producer ID, disjoint from B): implement sections 1, 3, 4, 5. The tests go green.
4. Ordering evidence: the first validator commit is an ancestor of the first P1 commit (`git merge-base --is-ancestor`). This closes QA W1 and is an addition to AC-4.4 for the Plan stage to write.

### 7. Live capture placement

Meta-tests and the fixture cost at most one cheap capture (the PRD's was $0.041). The 5-sample live baseline (about $15, NFR-2) is the expensive step. `state.md` routes it to Stage 7 UAT; see architecture.md section 6 for the sequencing consequence and why doing it last also satisfies Architect F8 (baseline representativeness) by construction.

## Alternatives rejected

| Alternative | Why rejected |
|---|---|
| Count every assistant event as a dispatch (as today) | Overstates dispatches and token sums when one message is split across events (F3). |
| Rebuild `cost_usd` and tokens purely from per-message sums | The real stream carries authoritative totals and per-model breakdown on `result`; summing risks double counting and misses subagent tokens. |
| Store `model_usage` as a nested object keyed by model | AC-5.1 asserts keys start with `model_usage.` inside `metrics`; the flat form satisfies the PRD as written. The nested form is safer against dotted IDs but changes the AC; the flat form plus "never split on `.`" removes the risk without changing the PRD. |
| Reject a v1 baseline inside `compare()` | Breaks the existing `test_meta.py` fixtures (`schema_version "1"`) and the 3-test contract. Rejection lives at the load boundary. |
| Keep schema `"1"` | Six top-level fields change meaning; a reader cannot tell an old partial baseline from a new one. |
| `--bare` in the runner | Bare mode authenticates only with `ANTHROPIC_API_KEY` or `apiKeyHelper` (local help; https://code.claude.com/docs/en/headless: "In bare mode, Claude Code never reads OAuth credentials or the system keychain"), so it changes the billing path. That is OQ-12, Michael's call; recommendation: no `--bare`, record `host_context`. New fact from the same page: "`--bare` is the recommended mode for scripted and SDK calls, and will become the default for `-p` in a future release." A CLI upgrade could therefore flip the default and change what a baseline measures; mitigated by `host_context` and re-recording the fixture on upgrade (risk U9). |
| Validator writes tests after seeing the fix | Violates BINDING-4.5 red-first; ordering in section 6 prevents it. |

## Consequences

- The parser is legacy-compatible (flat events keep working) and real-shape-correct. The cost is a two-mode parser; it is bounded by the fixture tests for both shapes.
- Behaviour that depends on undocumented stream fields (`message.id`, budget subtype, init model field) is pinned by a recorded real fixture and re-verified on a CLI upgrade (R11). Whether real events share `message.id` is the first thing the validator's red phase reveals; if ids are absent the per-event fallback applies and the fixture test records that.
- `--strict-model` is for release runs only; default runs WARN. An `effort moved` WARN mirroring `model moved` is a cheap optional addition (recommended, not required by the PRD).
- A baseline is host-specific unless `--bare` is used; documented, not solved (R13).
- Because the committed v1 baseline is rejected by `load_baseline`, a regression run between S5 and the UAT capture exits 4 with a re-capture message. That is the intended state (BINDING-4.4).

## Status rationale

Proposed until Stage 4 DoD passes; then Accepted.
