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


def parse_stream(events: Iterable[dict]) -> Metrics:
    """Fold an iterable of stream-json events into a Metrics dataclass.

    Malformed events emit warnings.warn() and are skipped — never raise.
    """
    metrics = Metrics()
    first_ts: float | None = None
    last_ts: float | None = None

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
        if evt_type not in ("assistant", "message", "tool_use", "result"):
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

        in_tok = _coerce_int(usage.get("input_tokens"))
        out_tok = _coerce_int(usage.get("output_tokens"))
        cache_creation = _coerce_int(usage.get("cache_creation_input_tokens"))
        cache_read = _coerce_int(usage.get("cache_read_input_tokens"))
        cost = _coerce_float(usage.get("cost_usd"))

        metrics.tokens["input"] += in_tok
        metrics.tokens["output"] += out_tok
        metrics.tokens["cache_creation"] += cache_creation
        metrics.tokens["cache_read"] += cache_read
        metrics.cost_usd += cost
        metrics.dispatch_count += 1

        model_name = event.get("model") or "unknown"
        bucket = _find_model_usage(metrics.model_usage, str(model_name))
        bucket.dispatches += 1
        bucket.input_tokens += in_tok
        bucket.output_tokens += out_tok
        bucket.cache_creation_tokens += cache_creation
        bucket.cache_read_tokens += cache_read

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
