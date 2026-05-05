#!/usr/bin/env python3
"""Read .delivery/telemetry/skill-loads.jsonl and print mean token counts per skill.

Usage:
    python3 delivery-team/hooks/telemetry_report.py [--last N]

    --last N   Consider only the last N rows per skill (default 5).

Prints a table to stdout.  Exits 0 always.
"""
import json
import sys
from collections import defaultdict
from pathlib import Path

TELEMETRY_FILE = ".delivery/telemetry/skill-loads.jsonl"
DEFAULT_LAST_N = 5
TOKEN_FIELDS = ("input_tokens", "cache_read_tokens", "cache_write_tokens")


def _parse_args() -> int:
    """Return the --last N value (default 5)."""
    args = sys.argv[1:]
    if "--last" in args:
        idx = args.index("--last")
        try:
            return int(args[idx + 1])
        except (IndexError, ValueError):
            pass
    return DEFAULT_LAST_N


def _load_rows(path: Path) -> list[dict]:
    """Load all valid JSONL rows from the telemetry file."""
    rows = []
    try:
        with open(str(path), encoding="utf-8") as fh:
            for line in fh:
                line = line.strip()
                if not line:
                    continue
                try:
                    rows.append(json.loads(line))
                except json.JSONDecodeError:
                    continue
    except FileNotFoundError:
        pass
    return rows


def _mean(values: list[float]) -> float:
    return sum(values) / len(values) if values else 0.0


def main() -> None:
    last_n = _parse_args()
    path = Path(TELEMETRY_FILE)
    rows = _load_rows(path)

    if not rows:
        print(f"No telemetry data found at {TELEMETRY_FILE}")
        print("Run at least one skill invocation to populate telemetry.")
        sys.exit(0)

    # Group by skill, keep last N rows per skill
    by_skill: dict[str, list[dict]] = defaultdict(list)
    for row in rows:
        skill = row.get("skill", "unknown")
        by_skill[skill].append(row)

    # Print header
    col_w = max(len(s) for s in by_skill) + 2
    header = (
        f"{'Skill':<{col_w}} {'Runs':>6}  "
        f"{'Mean input_tok':>16}  {'Mean cache_read':>16}  {'Mean cache_write':>17}"
    )
    print(header)
    print("-" * len(header))

    for skill in sorted(by_skill):
        recent = by_skill[skill][-last_n:]
        n = len(recent)
        means = {
            f: _mean([r.get(f, 0) for r in recent])
            for f in TOKEN_FIELDS
        }
        print(
            f"{skill:<{col_w}} {n:>6}  "
            f"{means['input_tokens']:>16.1f}  "
            f"{means['cache_read_tokens']:>16.1f}  "
            f"{means['cache_write_tokens']:>17.1f}"
        )

    print(f"\n(Last {last_n} rows per skill; total rows in file: {len(rows)})")


if __name__ == "__main__":
    main()
