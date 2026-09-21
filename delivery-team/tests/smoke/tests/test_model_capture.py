"""S5a validator tests: model capture, real stream shape, baseline consistency.

Authored by the VALIDATOR (qa) dispatch, never the producer of `lib/`
(BINDING-4.5, FR-4.4, ADR-lmr-004 section 6 item 2, plan 5.3).

Rules this file follows:
* No module-level import of new names: every `lib` import is inside a test body,
  so the file collects against the P0 stub AND against `main` (red run gives
  exit 1, never a collection error).
* Value tests use bare `assert` with a message naming the defect; capture-failure
  tests use `pytest.raises(...)`. Against an inert stub that gives
  `AssertionError` or `Failed: DID NOT RAISE`, the only permitted red markers.
* Model strings are synthetic (`claude-opus-fixture`, ...), never real IDs.
* `claude` is never spawned (conftest guard); `_claude_cli_version` is patched
  wherever `build_report` or `init_baseline` is called.

Fixture status. `tests/fixtures/stream_real_shape.jsonl` is a REAL capture and
needs the operator paid-run go (gate H1). It is NOT fabricated here. Every
`real_shape` test therefore SKIPS with `blocked_on H1` until the fixture and its
provenance file are committed. The `synthetic_nested` tests cover the same
defect with an in-test stream that is labelled SYNTHETIC and never claims to be
real; they do not replace the real-shape tests (AC-5.9 is not satisfied by them).
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
from types import SimpleNamespace

import pytest

FIXTURE = Path(__file__).resolve().parent / "fixtures" / "stream_real_shape.jsonl"
BLOCKED = "blocked_on H1: stream_real_shape.jsonl (real capture, needs operator go) not committed"

MODEL_A = "claude-opus-fixture"
MODEL_B = "claude-haiku-fixture"


# ------------------------------------------------------------------ helpers

def _real_events() -> list[dict]:
    if not FIXTURE.is_file():
        pytest.skip(BLOCKED)
    prov = FIXTURE.with_suffix("").with_suffix(".provenance.txt")
    if not prov.is_file():
        pytest.skip(BLOCKED + " (provenance missing)")
    return [json.loads(x) for x in FIXTURE.read_text(encoding="utf-8").splitlines() if x.strip()]


def _usage(i=10, o=20, cc=5, cr=15):
    return {"input_tokens": i, "output_tokens": o,
            "cache_creation_input_tokens": cc, "cache_read_input_tokens": cr}


def _synthetic_events(*, init_model=MODEL_A, with_result=True, cost=0.42):
    """SYNTHETIC real-nested-shape stream (NOT a real capture)."""
    ev = [{"type": "system", "subtype": "init", "session_id": "sess-synth", "model": init_model}]
    ev.append({"type": "assistant", "parent_tool_use_id": None,
               "message": {"id": "msg-1", "model": MODEL_A, "usage": _usage(10, 20, 5, 15)}})
    # same message.id split across two events: last usage wins, one dispatch
    ev.append({"type": "assistant", "parent_tool_use_id": None,
               "message": {"id": "msg-1", "model": MODEL_A, "usage": _usage(10, 40, 5, 15)}})
    ev.append({"type": "assistant", "parent_tool_use_id": "toolu-x",
               "message": {"id": "msg-2", "model": MODEL_B, "usage": _usage(1, 2, 3, 4)}})
    if with_result:
        ev.append({"type": "result", "subtype": "success", "is_error": False, "total_cost_usd": cost,
                   "usage": _usage(11, 42, 8, 19),
                   "modelUsage": {MODEL_A: {"inputTokens": 10}, MODEL_B: {"inputTokens": 1}}})
    return ev


def _metrics(events):
    from lib.metrics import parse_stream
    import warnings
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        return parse_stream(events)


def _ws(strategy="copy"):
    return SimpleNamespace(plugin_load_strategy=strategy, plugin_path=Path("/nonexistent-plugin"))


def _report(model_resolved, monkeypatch=None, **extra):
    r = {
        "schema_version": "2",
        "outcome": {"success": True, "exit_code": 0, "reason": None},
        "wall_clock_seconds": 600.0, "cost_usd": 1.5,
        "tokens": {"input": 10000, "output": 5000, "cache_creation": 0, "cache_read": 0,
                   "cache_hit_ratio": 0.5},
        "pipeline": {"stages_completed": 7, "stories_completed": 1, "dispatch_count": 8, "defects_logged": 0},
        "skill_loads": [], "model_requested": "opus", "model_resolved": model_resolved,
        "model_usage": [{"model": m, "dispatches": 3} for m in model_resolved],
        "effort": "xhigh", "host_context": {"bare": False, "claude_code_version": "claude 0.0.0-test"},
        "model_pin_env": {}, "session_id": "s", "stream_file": None,
    }
    r.update(extra)
    return r


def _five_reports(tmp_path, *, same_streams=False, models=(MODEL_A,) * 5):
    reports = []
    for i in range(5):
        p = tmp_path / f"sample-{i + 1}.jsonl"
        body = json.dumps({"type": "system", "subtype": "init", "session_id": f"s{i}", "model": models[i]}) + "\n"
        body += json.dumps({"type": "assistant", "message": {"id": f"m{i}", "model": models[i]}}) + "\n"
        body += json.dumps({"type": "result", "total_cost_usd": 1.0 + i / 10}) + "\n"
        p.write_text(body if not same_streams else "same\n")
        reports.append(_report([models[i]], cost_usd=1.0 + i / 10, session_id=(f"s{i}" if not same_streams else "s"),
                               stream_file=str(p)))
    return reports


# ------------------------------------------------- real_shape (blocked on H1)

def test_real_shape_dispatch_count_and_tokens():
    """AC-5.9: dispatch_count == distinct message.id; input+cache tokens > 0."""
    events = _real_events()
    m = _metrics(events)
    ids = {e["message"]["id"] for e in events if e.get("type") == "assistant"}
    assert m.dispatch_count == len(ids), f"dispatch_count {m.dispatch_count} != distinct message.id {len(ids)}"
    t = m.tokens
    assert t["input"] + t["cache_creation"] + t["cache_read"] > 0, "real stream usage nested under message was not read (tokens 0)"
    by_model = {u.model: u.dispatches for u in m.model_usage}
    model = next(e["message"]["model"] for e in events if e.get("type") == "assistant")
    assert by_model.get(model) == len(ids), f"per-model dispatches {by_model}: expected {model!r} -> {len(ids)} (dispatches landed in `unknown`)"
    ru = [e for e in events if e.get("type") == "result"][-1]["usage"]
    assert t["input"] == ru["input_tokens"] and t["output"] == ru["output_tokens"], (
        f"tokens {t} != result.usage input {ru['input_tokens']} output {ru['output_tokens']} "
        "(result is authoritative; per-message usage summed on top double counts split message.id events)")


def test_real_shape_model_usage_keys_no_unknown():
    """AC-5.9: model_usage keys equal the set of model strings in the fixture, no `unknown`."""
    events = _real_events()
    m = _metrics(events)
    keys = {u.model for u in m.model_usage}
    fixture_models = {e["message"]["model"] for e in events if e.get("type") == "assistant" and e["message"].get("model")}
    assert "unknown" not in keys, f"`unknown` bucket present: {sorted(keys)}"
    assert keys == fixture_models, f"model_usage keys {sorted(keys)} != fixture models {sorted(fixture_models)}"


def test_real_shape_cost_equals_total_cost_usd():
    """AC-5.9: cost_usd equals the result event total_cost_usd (never 0.0 on a real stream)."""
    events = _real_events()
    total = [e for e in events if e.get("type") == "result"][-1]["total_cost_usd"]
    m = _metrics(events)
    assert m.cost_usd == pytest.approx(total), f"cost_usd {m.cost_usd} != total_cost_usd {total} (cost_usd 0.0 defect)"


def test_real_shape_primary_model_from_init():
    events = _real_events()
    init = next(e for e in events if e.get("type") == "system" and e.get("subtype") == "init")
    m = _metrics(events)
    assert m.model_primary == init["model"], f"model_primary {m.model_primary!r} != init model {init['model']!r}"


def test_real_shape_running_cost():
    """AC-5.4b: _running_cost on the real fixture equals total_cost_usd and is above 0."""
    from lib.runner import _running_cost
    events = _real_events()
    total = [e for e in events if e.get("type") == "result"][-1]["total_cost_usd"]
    got = _running_cost(events)
    assert got > 0 and got == pytest.approx(total), f"_running_cost {got} != total_cost_usd {total}"


# ------------------------------------------------- synthetic_nested parser

def test_synthetic_nested_model_usage_and_no_unknown():
    """SYNTHETIC nested stream: model comes from message.model, not top level."""
    m = _metrics(_synthetic_events())
    keys = {u.model for u in m.model_usage}
    assert "unknown" not in keys, f"`unknown` bucket present (top-level model read only): {sorted(keys)}"
    assert keys == {MODEL_A, MODEL_B}, f"model_usage keys {sorted(keys)}"


def test_synthetic_nested_dispatch_counted_per_distinct_message_id():
    m = _metrics(_synthetic_events())
    assert m.dispatch_count == 2, f"expected 2 distinct message.id, got {m.dispatch_count} (double count or zero)"
    by = {u.model: u.dispatches for u in m.model_usage}
    assert by.get(MODEL_A) == 1 and by.get(MODEL_B) == 1, f"per-model dispatches {by}"


def test_synthetic_nested_result_cost_and_no_double_count():
    m = _metrics(_synthetic_events(cost=0.42))
    assert m.cost_usd == pytest.approx(0.42), f"cost_usd {m.cost_usd} != result total_cost_usd 0.42 (cost_usd 0.0 defect)"
    assert m.tokens["input"] == 11 and m.tokens["output"] == 42, (
        f"tokens {m.tokens}: must come from result.usage, not per-message sum plus result")


def test_synthetic_nested_no_result_uses_last_usage_per_message_id():
    m = _metrics(_synthetic_events(with_result=False))
    # msg-1 last usage output 40, msg-2 output 2
    assert m.tokens["output"] == 42, f"output tokens {m.tokens['output']}: split events must keep the LAST usage per id"


def test_synthetic_nested_primary_model_from_init_not_subagent():
    m = _metrics(_synthetic_events(init_model=MODEL_A))
    assert m.model_primary == MODEL_A, f"model_primary {m.model_primary!r}"
    assert set(m.models_observed) == {MODEL_A, MODEL_B}, f"models_observed {m.models_observed}"


def test_synthetic_nested_cache_hit_ratio():
    m = _metrics(_synthetic_events())
    # result.usage: cache_read 19 / (19 + 8 + 11)
    assert m.cache_hit_ratio == pytest.approx(19 / 38), f"cache_hit_ratio {m.cache_hit_ratio}"


def test_cache_hit_ratio_reaches_report_tokens(monkeypatch, tmp_path):
    """PA-17: report['tokens']['cache_hit_ratio'] is computed (P0 is the constant 0.0)."""
    import lib.report as rep
    monkeypatch.setattr(rep, "_claude_cli_version", lambda: "claude 0.0.0-test")
    m = _metrics(_synthetic_events())
    r = rep.build_report(run_id="t", repo_root=tmp_path, plugin_load_strategy="copy",
                         outcome={"success": True, "exit_code": 0, "reason": None}, metrics=m, aggregator_dict={})
    assert r["tokens"]["cache_hit_ratio"] == pytest.approx(19 / 38), f"tokens.cache_hit_ratio {r['tokens']['cache_hit_ratio']}"


# ------------------------------------------------- AC-5.4b command and cost

def test_cmd_has_max_budget():
    from lib.runner import _build_claude_command
    cmd = _build_claude_command(_ws(), Path("p.txt"), model="opus", effort="xhigh", max_budget_usd=3.0)

    def follows(flag, val):
        return flag in cmd and cmd[cmd.index(flag) + 1] == val
    assert follows("--max-budget-usd", "3.00"), f"--max-budget-usd 3.00 missing in {cmd}"
    assert follows("--model", "opus"), f"--model opus missing in {cmd}"
    assert follows("--effort", "xhigh"), f"--effort xhigh missing in {cmd}"


def test_cmd_effort_only_for_opus():
    from lib.runner import _build_claude_command
    opus = _build_claude_command(_ws(), Path("p.txt"), model="opus", effort="xhigh")
    assert "--effort" in opus, f"opus command must carry --effort: {opus}"
    other = _build_claude_command(_ws(), Path("p.txt"), model="sonnet", effort="xhigh")
    assert "--effort" not in other and "--model" in other, f"non-opus must send --model but never --effort: {other}"


def test_running_cost_reads_total_cost_usd():
    """SYNTHETIC nested events; real-fixture twin is test_real_shape_running_cost."""
    from lib.runner import _running_cost
    got = _running_cost(_synthetic_events(cost=0.42))
    assert got == pytest.approx(0.42), f"_running_cost {got} != total_cost_usd 0.42 (cost 0.0 defect)"


def test_running_cost_result_not_added_to_per_event_sum():
    from lib.runner import _running_cost
    ev = [{"type": "assistant", "usage": {"cost_usd": 0.10}},
          {"type": "result", "total_cost_usd": 0.50, "modelUsage": {MODEL_A: {}}}]
    got = _running_cost(ev)
    assert got == pytest.approx(0.50), f"_running_cost {got}: result total replaces, never adds to, the per-event sum"


# ------------------------------------------------- AC-5.5b capture failures

def test_capture_fails_when_no_model_anywhere():
    from lib.metrics import ModelCaptureError, check_model_capture
    ev = [{"type": "system", "subtype": "init", "session_id": "s"},
          {"type": "assistant", "message": {"id": "m", "usage": _usage()}}]
    with pytest.raises(ModelCaptureError):
        check_model_capture(_metrics(ev))


def test_capture_fails_when_only_unknown_model():
    from lib.metrics import ModelCaptureError, check_model_capture
    ev = [{"type": "system", "subtype": "init", "session_id": "s", "model": "unknown"},
          {"type": "assistant", "message": {"id": "m", "model": "unknown", "usage": _usage()}}]
    with pytest.raises(ModelCaptureError):
        check_model_capture(_metrics(ev))


def test_capture_fails_when_init_has_no_model():
    from lib.metrics import ModelCaptureError, check_model_capture
    ev = [{"type": "system", "subtype": "init", "session_id": "s"},
          {"type": "assistant", "message": {"id": "m", "model": MODEL_A, "usage": _usage()}}]
    with pytest.raises(ModelCaptureError):
        check_model_capture(_metrics(ev))


def test_capture_fails_when_init_missing():
    from lib.metrics import ModelCaptureError, check_model_capture
    ev = [{"type": "assistant", "message": {"id": "m", "model": MODEL_A, "usage": _usage()}}]
    with pytest.raises(ModelCaptureError):
        check_model_capture(_metrics(ev))


def test_capture_returns_resolved_list_primary_first_then_by_dispatches():
    from lib.metrics import check_model_capture
    resolved = check_model_capture(_metrics(_synthetic_events()))
    assert resolved and resolved[0] == MODEL_A, f"model_resolved {resolved}: element 0 must be model_primary"
    assert resolved == [MODEL_A, MODEL_B], f"model_resolved {resolved}"


def test_two_samples_different_primary_model_init_baseline_raises(monkeypatch, tmp_path):
    """AC-5.5b(iv): two samples with different model_resolved[0] abort, naming both models."""
    import lib.baseline as bl
    from lib.baseline import ModelMovedError, init_baseline
    monkeypatch.setattr(bl, "_claude_cli_version", lambda: "claude 0.0.0-test")
    reports = _five_reports(tmp_path, models=(MODEL_A, MODEL_A, MODEL_B, MODEL_A, MODEL_A))
    with pytest.raises(ModelMovedError, match=f"(?s)(?=.*{MODEL_A})(?=.*{MODEL_B})"):
        init_baseline(reports, tmp_path / "b.json")
    assert not (tmp_path / "b.json").exists(), "no baseline may be written on a model change"


def test_check_model_consistency_names_both_models():
    from lib.baseline import ModelMovedError, check_model_consistency
    with pytest.raises(ModelMovedError, match=f"(?s)(?=.*{MODEL_A})(?=.*{MODEL_B})"):
        check_model_consistency([_report([MODEL_A]), _report([MODEL_B])])


# ------------------------------------------------- baseline schema v2 / load

def test_load_baseline_rejects_schema_v1(tmp_path):
    from lib.baseline import BaselineSchemaError, load_baseline
    p = tmp_path / "old.json"
    p.write_text(json.dumps({"schema_version": "1", "metrics": {}}))
    with pytest.raises(BaselineSchemaError, match="re-capture"):
        load_baseline(p)


def test_load_baseline_accepts_schema_v2(tmp_path):
    from lib.baseline import load_baseline
    p = tmp_path / "new.json"
    p.write_text(json.dumps({"schema_version": "2", "metrics": {}, "marker": 7}))
    got = load_baseline(p)
    assert got.get("marker") == 7, f"load_baseline returned {got!r} instead of the file content"


def test_init_baseline_writes_v2_fields(monkeypatch, tmp_path):
    """FR-5.5 / AC-5.1: schema 2, model fields, samples[] with hashes, model_usage.* informational, cache ratio advisory."""
    import lib.baseline as bl
    monkeypatch.setattr(bl, "_claude_cli_version", lambda: "claude 0.0.0-test")
    reports = _five_reports(tmp_path)
    out = tmp_path / "b.json"
    bl.init_baseline(reports, out)
    b = json.loads(out.read_text())
    assert b.get("schema_version") == "2", f"schema_version {b.get('schema_version')!r}"
    assert b.get("model_requested") == "opus", "model_requested missing from baseline"
    assert b.get("model_resolved") == [MODEL_A], f"model_resolved {b.get('model_resolved')}"
    assert b.get("effort") == "xhigh" and isinstance(b.get("host_context"), dict) and "model_pin_env" in b, "effort/host_context/model_pin_env missing"
    samples = b.get("samples") or []
    assert len(samples) == 5, f"samples has {len(samples)} entries"
    for s, r in zip(samples, reports):
        assert s.get("stream_sha256") == hashlib.sha256(Path(r["stream_file"]).read_bytes()).hexdigest(), "stream_sha256 mismatch"
    m = b["metrics"]
    key = f"model_usage.{MODEL_A}.dispatches"
    assert key in m and m[key]["classification"] == "informational", f"{key} missing or not informational: {m.get(key)}"
    assert "unknown" not in json.dumps(list(m)), "an `unknown` model key leaked into metrics"
    assert "tokens.cache_hit_ratio" in m and m["tokens.cache_hit_ratio"]["classification"] == "advisory", "tokens.cache_hit_ratio not advisory metric"
    assert "hard_max" not in m[key], "model_usage.* must have no hard_max"


def test_init_baseline_rejects_copied_stream(monkeypatch, tmp_path):
    """QA W4: a copied stream (same hash / session) is rejected by --init-baseline."""
    import lib.baseline as bl
    monkeypatch.setattr(bl, "_claude_cli_version", lambda: "claude 0.0.0-test")
    reports = _five_reports(tmp_path, same_streams=True)
    with pytest.raises(Exception):
        bl.init_baseline(reports, tmp_path / "b.json")
    assert not (tmp_path / "b.json").exists()


# ------------------------------------------------- AC-5.7 model moved

def _baseline_for(model):
    return {
        "schema_version": "2", "n_samples": 5, "last_captured_utc": "x", "model_resolved": [model],
        "metrics": {
            "cost_usd": {"mean": 1.5, "stddev": 0.2, "n": 5, "classification": "hard", "hard_max": 3.0},
            "wall_clock_seconds": {"mean": 600.0, "stddev": 50.0, "n": 5, "classification": "hard", "hard_max": 1800.0},
            "pipeline.dispatch_count": {"mean": 8.0, "stddev": 1.0, "n": 5, "classification": "hard", "hard_max": 16.0},
            "pipeline.stories_completed": {"mean": 1.0, "stddev": 0.0, "n": 5, "classification": "hard", "hard_max": 1.0},
            f"model_usage.{model}.dispatches": {"mean": 8.0, "stddev": 0.0, "n": 5, "classification": "informational"},
        },
    }


def test_model_moved_warn_default():
    from lib.baseline import compare
    res = compare(_report([MODEL_B]), _baseline_for(MODEL_A))
    text = "\n".join(res.advisory_warnings + res.hard_failures)
    assert f"model moved: baseline={MODEL_A} run={MODEL_B}" in text, f"no model-moved WARN in: {text!r}"
    assert res.status != "FAIL", f"status {res.status}: WARN alone must not fail without strict_model"
    assert "model_usage." not in text, f"model_usage.* reported as missing or a threshold breach: {text!r}"


def test_model_moved_strict_fails_and_says_recapture():
    from lib.baseline import compare
    res = compare(_report([MODEL_B]), _baseline_for(MODEL_A), strict_model=True)
    text = "\n".join(res.advisory_warnings + res.hard_failures)
    assert res.status == "FAIL", f"status {res.status}: strict_model must fail on a moved model"
    assert "re-captured" in text or "re-capture" in text, f"text must say the baseline must be re-captured: {text!r}"


# ------------------------------------------------- AC-5.2 best-effort WARNs

def _warn_text(monkeypatch, tmp_path):
    import lib.report as rep
    monkeypatch.setattr(rep, "_claude_cli_version", lambda: "claude 0.0.0-test")
    m = _metrics(_synthetic_events())  # lacks thinkingTokens, refusal_code and speed
    r = rep.build_report(run_id="t", repo_root=tmp_path, plugin_load_strategy="copy",
                         outcome={"success": True, "exit_code": 0, "reason": None}, metrics=m, aggregator_dict={})
    return r, rep._render_summary_md(r) + "\n" + "\n".join(r.get("advisory_warnings", []))


def test_warn_missing_thinking_tokens(monkeypatch, tmp_path):
    r, text = _warn_text(monkeypatch, tmp_path)
    assert "WARN missing thinking_tokens" in text, "literal WARN missing thinking_tokens absent from report text"
    assert r["outcome"]["success"] is True and r["outcome"]["exit_code"] == 0, "a WARN must not change the exit status"


def test_warn_missing_stop_details_refusal_code(monkeypatch, tmp_path):
    r, text = _warn_text(monkeypatch, tmp_path)
    assert "WARN missing stop_details.refusal_code" in text, "literal WARN missing stop_details.refusal_code absent"
    assert r["outcome"]["exit_code"] == 0, "a WARN must not change the exit status"


def test_warn_missing_speed_or_fast_indicator(monkeypatch, tmp_path):
    r, text = _warn_text(monkeypatch, tmp_path)
    assert "WARN missing speed_or_fast_indicator" in text, "literal WARN missing speed_or_fast_indicator absent"
    assert r["outcome"]["exit_code"] == 0, "a WARN must not change the exit status"


# ------------------------------------------------- report keys (P0-pinned shape)

def test_build_report_records_model_and_session_from_stream(monkeypatch, tmp_path):
    import lib.report as rep
    monkeypatch.setattr(rep, "_claude_cli_version", lambda: "claude 0.0.0-test")
    m = _metrics(_synthetic_events())
    r = rep.build_report(run_id="t", repo_root=tmp_path, plugin_load_strategy="copy",
                         outcome={"success": True, "exit_code": 0, "reason": None}, metrics=m, aggregator_dict={},
                         stream_path=str(tmp_path / "stream.jsonl"), session_id="sess-synth")
    assert r["model_resolved"] and r["model_resolved"][0] == MODEL_A, f"model_resolved {r['model_resolved']}"
    assert r["session_id"] == "sess-synth" and r["stream_file"] == str(tmp_path / "stream.jsonl"), "session_id/stream_file not recorded"
    assert set(r["model_pin_env"].values()) <= {"set", None}, f"model_pin_env carries values: {r['model_pin_env']}"
    assert r["model_pin_env"], "model_pin_env must list the four env vars (set or null), got empty"
