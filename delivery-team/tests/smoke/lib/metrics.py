"""Stream-json event parser. Pure functions only — no I/O."""
from __future__ import annotations

import warnings
from dataclasses import dataclass, field
from typing import Iterable


@dataclass
class ModelUsage:
    """Per-model dispatch + token accumulator."""
    model: str
    dispatches: int = 0
    input_tokens: int = 0
    output_tokens: int = 0
    cache_creation_tokens: int = 0
    cache_read_tokens: int = 0


@dataclass
class Metrics:
    """Aggregated stream-json metrics for a single smoke run."""
    wall_clock_seconds: float = 0.0
    cost_usd: float = 0.0
    tokens: dict = field(default_factory=lambda: {
        "input": 0,
        "output": 0,
        "cache_creation": 0,
        "cache_read": 0,
    })
    model_usage: list = field(default_factory=list)
    dispatch_count: int = 0
    model_primary: str | None = None
    models_observed: list = field(default_factory=list)
    cache_hit_ratio: float = 0.0
    session_id: str | None = None
    observed_fields: list = field(default_factory=list)


class ModelCaptureError(Exception):
    """Raised when no usable model string was captured (ADR-lmr-004 s1 item 7)."""


def check_model_capture(metrics: Metrics) -> list[str]:
    """Return model_resolved (primary first, rest by dispatches desc) or raise.

    Raises ModelCaptureError when init carried no usable model or no non-unknown
    model was observed on any dispatch (ADR-lmr-004 s1 item 7).
    """
    primary = metrics.model_primary
    if not primary or primary == "unknown":
        raise ModelCaptureError("no model on the system/init event of the stream; cannot record the resolved model")
    observed = [m for m in metrics.models_observed if m and m != "unknown"]
    if not observed:
        raise ModelCaptureError("no model string observed on any assistant message (only `unknown`)")
    return [primary] + [m for m in observed if m != primary]


def _coerce_int(value) -> int:
    if value is None:
        return 0
    try:
        return int(value)
    except (TypeError, ValueError):
        return 0


def _coerce_float(value) -> float:
    if value is None:
        return 0.0
    try:
        return float(value)
    except (TypeError, ValueError):
        return 0.0


def _find_model_usage(usage_list: list, model: str) -> ModelUsage:
    for entry in usage_list:
        if entry.model == model:
            return entry
    new_entry = ModelUsage(model=model)
    usage_list.append(new_entry)
    return new_entry


def _usage_tokens(usage: dict) -> tuple[int, int, int, int]:
    return (
        _coerce_int(usage.get("input_tokens")),
        _coerce_int(usage.get("output_tokens")),
        _coerce_int(usage.get("cache_creation_input_tokens")),
        _coerce_int(usage.get("cache_read_input_tokens")),
    )


def parse_stream(events: Iterable[dict]) -> Metrics:
    """Fold an iterable of stream-json events into a Metrics dataclass.

    Real shape (ADR-lmr-004 s1): `assistant` events nest `message.{id,model,usage}`;
    one dispatch is one distinct `message.id` (split events: last usage wins);
    `result.usage` and `result.total_cost_usd` are authoritative for tokens and cost;
    `system/init.model` is the primary model. Legacy shape (top-level `usage`,
    `usage.cost_usd`) is still folded per event. Malformed events emit
    warnings.warn() and are skipped, never raise.
    """
    metrics = Metrics()
    first_ts: float | None = None
    last_ts: float | None = None

    per_msg: dict = {}          # message key -> {"model": str, "usage": tuple}
    legacy_usage: list = []     # ModelUsage buckets for legacy per-event events
    result_usage: tuple | None = None
    total_cost: float | None = None
    legacy_cost = 0.0
    observed: set = set()

    def _scan_usage(u: dict) -> None:
        if "thinking_tokens" in u or "thinkingTokens" in u:
            observed.add("thinking_tokens")
        if "speed" in u or "fast_mode" in u:
            observed.add("speed_or_fast_indicator")

    for idx, event in enumerate(events):
        if not isinstance(event, dict):
            warnings.warn(
                f"parse_stream: event {idx} not a dict (type={type(event).__name__}); skipping",
                stacklevel=2,
            )
            continue

        ts = event.get("timestamp_seconds")
        if isinstance(ts, (int, float)):
            if first_ts is None:
                first_ts = float(ts)
            last_ts = float(ts)

        evt_type = event.get("type")

        if evt_type == "system" and event.get("subtype") == "init":
            m = event.get("model")
            if isinstance(m, str) and m and metrics.model_primary is None:
                metrics.model_primary = m
            sid = event.get("session_id")
            if isinstance(sid, str) and sid and metrics.session_id is None:
                metrics.session_id = sid
            if "fast_mode_state" in event:
                observed.add("speed_or_fast_indicator")
            continue

        if evt_type not in ("assistant", "message", "tool_use", "result"):
            continue

        if evt_type == "result" and ("total_cost_usd" in event or "modelUsage" in event):
            tc = event.get("total_cost_usd")
            if tc is not None:
                total_cost = _coerce_float(tc)
            ru = event.get("usage")
            if isinstance(ru, dict):
                result_usage = _usage_tokens(ru)
                _scan_usage(ru)
            mu = event.get("modelUsage")
            if isinstance(mu, dict):
                for entry in mu.values():
                    if isinstance(entry, dict):
                        if "thinkingTokens" in entry or "thinking_tokens" in entry:
                            observed.add("thinking_tokens")
            continue

        msg = event.get("message")
        if evt_type == "assistant" and isinstance(msg, dict):
            usage = msg.get("usage")
            if not isinstance(usage, dict):
                warnings.warn(
                    f"parse_stream: event {idx} type={evt_type!r} message missing 'usage' dict; skipping usage extraction",
                    stacklevel=2,
                )
                continue
            _scan_usage(usage)
            sd = msg.get("stop_details")
            if isinstance(sd, dict) and "refusal_code" in sd:
                observed.add("stop_details.refusal_code")
            mid = msg.get("id")
            key = mid if isinstance(mid, str) and mid else ("anon", idx)
            model_name = msg.get("model")
            if not (isinstance(model_name, str) and model_name):
                model_name = "unknown"
            per_msg[key] = {"model": model_name, "usage": _usage_tokens(usage)}
            continue

        usage = event.get("usage")
        if usage is None:
            warnings.warn(
                f"parse_stream: event {idx} type={evt_type!r} missing 'usage' key; skipping usage extraction",
                stacklevel=2,
            )
            continue

        if not isinstance(usage, dict):
            warnings.warn(
                f"parse_stream: event {idx} 'usage' not a dict (type={type(usage).__name__}); skipping",
                stacklevel=2,
            )
            continue

        in_tok, out_tok, cache_creation, cache_read = _usage_tokens(usage)
        legacy_cost += _coerce_float(usage.get("cost_usd"))
        metrics.dispatch_count += 1
        bucket = _find_model_usage(legacy_usage, str(event.get("model") or "unknown"))
        bucket.dispatches += 1
        bucket.input_tokens += in_tok
        bucket.output_tokens += out_tok
        bucket.cache_creation_tokens += cache_creation
        bucket.cache_read_tokens += cache_read

    # Fold per-message (real shape) records into per-model buckets.
    sums = [0, 0, 0, 0]
    for u in legacy_usage:
        metrics.model_usage.append(u)
        sums[0] += u.input_tokens
        sums[1] += u.output_tokens
        sums[2] += u.cache_creation_tokens
        sums[3] += u.cache_read_tokens
    for rec in per_msg.values():
        i, o, cc, cr = rec["usage"]
        bucket = _find_model_usage(metrics.model_usage, rec["model"])
        bucket.dispatches += 1
        bucket.input_tokens += i
        bucket.output_tokens += o
        bucket.cache_creation_tokens += cc
        bucket.cache_read_tokens += cr
        metrics.dispatch_count += 1
        sums[0] += i
        sums[1] += o
        sums[2] += cc
        sums[3] += cr

    final = result_usage if result_usage is not None else tuple(sums)
    metrics.tokens["input"], metrics.tokens["output"] = final[0], final[1]
    metrics.tokens["cache_creation"], metrics.tokens["cache_read"] = final[2], final[3]
    metrics.cost_usd = total_cost if total_cost is not None else legacy_cost

    denom = final[0] + final[2] + final[3]
    metrics.cache_hit_ratio = (final[3] / denom) if denom else 0.0

    known = [u for u in metrics.model_usage if u.model != "unknown"]
    known.sort(key=lambda u: (-u.dispatches, u.model))
    metrics.models_observed = [u.model for u in known]
    metrics.observed_fields = sorted(observed)

    if first_ts is not None and last_ts is not None and last_ts >= first_ts:
        metrics.wall_clock_seconds = last_ts - first_ts

    return metrics


def parse_jsonl_lines(lines: Iterable[str]) -> list[dict]:
    """Convert raw JSONL lines to event dicts; malformed lines emit warn + skip.

    Helper for runners that read stream.jsonl from disk. NOT used by parse_stream.
    """
    import json

    out: list[dict] = []
    for idx, raw in enumerate(lines):
        text = raw.strip()
        if not text:
            continue
        try:
            obj = json.loads(text)
        except json.JSONDecodeError as exc:
            warnings.warn(
                f"parse_jsonl_lines: line {idx} not valid JSON ({exc}); skipping",
                stacklevel=2,
            )
            continue
        if isinstance(obj, dict):
            out.append(obj)
        else:
            warnings.warn(
                f"parse_jsonl_lines: line {idx} not a JSON object (type={type(obj).__name__}); skipping",
                stacklevel=2,
            )
    return out
