#!/usr/bin/env python3
"""challenge_gate.py - BLOCKER gate over challenge-report.md's severity table
(stage-gates.md section 3). Stdlib only; ``python -I`` safe.
"""
from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))
import gate_common as gc  # noqa: E402

HEADER = ["severity", "location", "finding", "suggested fix"]
SEVERITIES = ("BLOCKER", "MAJOR", "MINOR")


def _cells(line: str) -> list[str]:
    return [c.strip() for c in line.strip().strip("|").split("|")]


def find_table(text: str) -> tuple[int, list[tuple[int, list[str]]]] | None:
    """Return (header line number, [(line number, cells)]) for the first severity table."""
    lines = text.splitlines()
    for i, line in enumerate(lines):
        if not line.strip().startswith("|"):
            continue
        if [c.lower() for c in _cells(line)] != HEADER:
            continue
        rows: list[tuple[int, list[str]]] = []
        for j in range(i + 1, len(lines)):
            s = lines[j].strip()
            if not s.startswith("|"):
                break
            cells = _cells(s)
            if all(set(c) <= set("-: ") for c in cells):
                continue
            rows.append((j + 1, cells))
        return i + 1, rows
    return None


def main_fn(args: Any, config: dict[str, Any], res: gc.GateResult) -> gc.GateResult:
    path = gc.file_named(args.paths, "challenge-report.md") or (args.paths[0] if args.paths else None)
    if not path:
        return res.error("challenge-report.md not given")
    found = find_table(gc.read_text(path))
    if found is None:
        return res.error("no severity table (severity | location | finding | suggested fix)", gc.norm(path))
    _, rows = found
    counts = {s: 0 for s in SEVERITIES}
    blockers: list[tuple[str, str]] = []
    for lineno, cells in rows:
        loc = f"{gc.norm(path)}:{lineno}"
        if len(cells) < 4:
            return res.error(f"row has {len(cells)} cells, expected 4", loc)
        sev = cells[0].upper()
        if sev not in counts:
            return res.error(f"severity {cells[0]!r} not in BLOCKER/MAJOR/MINOR", loc)
        counts[sev] += 1
        if sev == "BLOCKER":
            blockers.append((cells[1], cells[2]))
    res.metrics.update({k.lower(): v for k, v in counts.items()})
    for location, finding in blockers:
        res.violate(location, finding, "BLOCKER", 0)
    return res


def main(argv: list[str] | None = None) -> int:
    return gc.run("challenge_gate.py", "Fail on any BLOCKER row in challenge-report.md.", None, main_fn, argv)


if __name__ == "__main__":
    sys.exit(main())
