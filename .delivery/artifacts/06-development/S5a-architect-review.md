# S5a Architect DoD review (P1 commit f391b0f)

Verdict: DONE (no blocking findings; 3 non-blocking follow-ups).

## Conformance to ADR-lmr-004 / 005
- Schema v2: SCHEMA_VERSION "2" in baseline.py and report.py. Baseline gains model_requested, model_resolved, model_pin_env, effort, host_context (bare + claude_code_version), samples[{stream_file, stream_sha256}], sample_status, last_captured_cli_version written from the same variable as host_context. cache_hit_ratio joined ADVISORY_METRIC_KEYS. Conforms.
- Model capture: primary from system/init.model, per-dispatch model from message.model, unknown excluded, primary first then by dispatches desc; ModelCaptureError on no init model or no observed model. Conforms (ADR s1 item 7).
- Dispatch counting: one dispatch per distinct message.id, last usage wins on split events; result.usage and result.total_cost_usd authoritative; legacy top-level shape still folded. Conforms.
- model_usage.* keys: collected as flat `model_usage.<model>.dispatches`, classified "informational", 0 for absent models; uses no dot split. Conforms.
- Consistency: check_model_consistency raises ModelMovedError naming both models; compare() emits `model moved: baseline=X run=Y` WARN, and FAIL (exit 1) under --strict-model. Conforms.
- Copied-stream rejection: sha256, session_id and message.id overlap all rejected in init_baseline; init flow now aborts on ANY non-zero exit (F9 widening), with init_mode skipping load_baseline/compare. Conforms.
- Flags/runner: --model (choices opus), --effort (default xhigh, sent only for opus), --strict-model; _build_claude_command adds --model/--effort/--max-budget-usd. Conforms.
- Exit codes: ModelCaptureError, BaselineSchemaError, ModelMovedError (via init_baseline exception) all map to 4; strict FAIL to 1. This is exactly the ADR s2 mapping, so exit 4 is permitted. The result classifier (_result_failure) is specified by ADR s4 (subtype containing "budget", "budget limit" text, is_error with cost >= 0.99 cap, cost over cap -> exit 2; other failures exit 1), so it is also permitted though untested by the red file.
- In-loop cost kill: _running_cost returns result total_cost_usd else the legacy sum; the in-loop kill therefore only fires for legacy/fixture streams, matching the ADR "legacy-only (F5)" statement. Real enforcement is --max-budget-usd plus the post-check.

## Behaviour change: committed baseline is schema 1
baselines/hello_world_spike.json has schema_version "1", so normal runs now exit 4 with a re-capture message until S5b. ADR-lmr-004 Consequences explicitly accepts this ("intended state, BINDING-4.4"); rejection lives at the load boundary, so compare() and test_meta.py fixtures are unaffected. Nothing in .github/workflows references the smoke runner or baseline (CLAUDE.md also says CLI is local-only). Other consumers: delivery-team/tests/smoke/tests/dry_run_baseline.py uses --init-baseline (init_mode skips load), so it is unaffected. No breakage found.

## Non-blocking findings
1. ADR s3 says the producer adds an explicit `startswith("model_usage.")` skip and comment in both _check_hard_rules and _check_advisory_rules. The P1 diff does not touch those functions. Behaviour is correct by construction (keys not in the HARD/ADVISORY lists), but the intent-preserving guard is missing; add in a follow-up (AC-5.7(ii) still passes).
2. Model-capture check is skipped when --stream-fixture is used and only runs at exit 0; fine per ADR item ordering, but it means fixture runs never surface exit 4 for missing model. Acceptable.
3. Optional `effort moved` WARN (ADR "recommended, not required") not implemented.

## Doc updates still owed
- delivery-team/architecture/smoke-test-architecture.md is stale: schema_version "1" at lines 96 and 143, exit-code diagram "0 / 1 / 2" (line 53, no 4), flag list (line 60) lacks --model/--effort/--strict-model, model_usage described as derived from top-level usage events (line 133), baseline load description lacks the schema-2 rejection. Owner: S6 (docs story); it is not an S5a defect.
- delivery-team/tests/smoke/README.md schema keys (line ~94) and exit code table should list v2 fields and exit 4 semantics (S6).
- delivery-team/references/telemetry-schema.md has no smoke/model_usage schema content, so no S5a-owed change; any note about model capture belongs to S6/S7 if scoped there.
- S5b re-capture replaces the schema-1 baseline; S7 ship gate and CHANGELOG cover the rest.
