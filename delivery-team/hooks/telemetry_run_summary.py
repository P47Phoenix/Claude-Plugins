#!/usr/bin/env python3
"""telemetry_run_summary.py — Wave 3 W3-18 per-run summary emitter.

Reads `.delivery/telemetry/skill-loads.jsonl` and writes
`.delivery/telemetry/run-summary-<pipeline-id>.json` containing per-skill
and overall `prose_tokens` aggregates for ONE pipeline run.

Excludes rows with `placeholder == true` per PRD §FR-7.6 (W3-10 retro KPI
compute MUST exclude placeholder rows). Mean is computed over the
non-placeholder subset only; if all rows are placeholders, the field is
emitted as `null` and `placeholder_only: true` is set so the consumer
(stop-rule tripwire) knows to fall back to the prior baseline.

Designed to run at the orchestrator's post-pipeline step (Stage 7
Post-Acceptance, after retrospective). Always exits 0.

Usage:
    python3 delivery-team/hooks/telemetry_run_summary.py \\
        --pipeline-id run-2026-05-09-tk4
    python3 delivery-team/hooks/telemetry_run_summary.py \\
        --pipeline-id <id> --output .delivery/telemetry/run-summary-<id>.json
"""
from __future__ import annotations

import argparse
import json
import statistics
import sys
from collections import defaultdict
from pathlib import Path

DEFAULT_TELEMETRY = ".delivery/telemetry/skill-loads.jsonl"
DEFAULT_OUTPUT_TEMPLATE = ".delivery/telemetry/run-summary-{pipeline_id}.json"


def _load_rows(path: Path) -> list[dict]:
    rows: list[dict] = []
    if not path.is_file():
        return rows
    with path.open("r", encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            try:
                rows.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    return rows


def _filter_run(rows: list[dict], pipeline_id: str) -> list[dict]:
    """Return rows belonging to `pipeline_id`. Falls back to all rows if no row
    carries a pipeline_id field (legacy telemetry)."""
    tagged = [r for r in rows if r.get("pipeline_id") == pipeline_id]
    if tagged:
        return tagged
    # Legacy fallback: no pipeline_id captured pre-W3-18 hardening; warn caller.
    return rows


def _is_placeholder(row: dict) -> bool:
    """A row is a placeholder if explicitly flagged OR if pre-W3-18 legacy
    (no `placeholder` field AND prose_tokens == 0/absent — telemetry was
    structurally unable to capture prose_tokens before W3-18)."""
    if "placeholder" in row:
        return bool(row["placeholder"])
    # Legacy fallback: treat zero/absent prose_tokens as placeholder
    return not (row.get("prose_tokens") or 0)


def _summarize(rows: list[dict]) -> dict:
    real = [r for r in rows if not _is_placeholder(r)]
    placeholder_count = len(rows) - len(real)
    by_skill: dict[str, list[float]] = defaultdict(list)
    for r in real:
        by_skill[r.get("skill", "unknown")].append(float(r.get("prose_tokens") or 0))

    per_skill = {
        skill: {
            "rows": len(values),
            "mean_prose_tokens": statistics.fmean(values) if values else None,
            "total_prose_tokens": sum(values),
        }
        for skill, values in sorted(by_skill.items())
    }

    all_values = [v for vs in by_skill.values() for v in vs]
    overall = {
        "rows_total": len(rows),
        "rows_real": len(real),
        "rows_placeholder": placeholder_count,
        "mean_prose_tokens": statistics.fmean(all_values) if all_values else None,
        "total_prose_tokens": sum(all_values),
        "placeholder_only": len(real) == 0 and len(rows) > 0,
    }
    return {"overall": overall, "per_skill": per_skill}


def main() -> int:
    ap = argparse.ArgumentParser(description="Emit per-run telemetry summary.")
    ap.add_argument("--pipeline-id", required=True)
    ap.add_argument("--telemetry", default=DEFAULT_TELEMETRY)
    ap.add_argument("--output", default=None, help="default: run-summary-<pipeline-id>.json")
    args = ap.parse_args()

    telemetry_path = Path(args.telemetry)
    rows = _load_rows(telemetry_path)
    run_rows = _filter_run(rows, args.pipeline_id)
    summary = _summarize(run_rows)
    summary["pipeline_id"] = args.pipeline_id
    summary["telemetry_source"] = str(telemetry_path)

    out_path = Path(
        args.output or DEFAULT_OUTPUT_TEMPLATE.format(pipeline_id=args.pipeline_id)
    )
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")

    print(
        f"telemetry_run_summary: wrote {out_path} "
        f"(rows={summary['overall']['rows_total']}, real={summary['overall']['rows_real']}, "
        f"placeholder={summary['overall']['rows_placeholder']})"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
