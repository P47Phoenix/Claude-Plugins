#!/usr/bin/env python3
"""arrangement_check.py - energy-curve gate for arrangement.md
(stage-gates.md section 3). Stdlib only; ``python -I`` safe.

Reads ``energy`` per section (table columns ``section``, ``energy``) in order.
Let ``C1..Cn`` be the chorus energies in order and ``G`` the global maximum.

``chorus_rising`` (default) PASSES iff all of:
  (a) ``Ci >= Ci-1`` for every ``i > 1``;
  (b) ``G`` occurs in the final chorus or in the bridge (ties count);
  (c) the final section's energy ``< G`` unless the final section is the last chorus;
  (d) every verse energy ``<`` the energy of the next chorus after it (a verse
      with no following chorus is unconstrained).
``strict_rising`` PASSES iff the sequence is non-decreasing up to the first
occurrence of ``G`` and non-increasing after it. ``free`` always PASSES.

Roles: ``Chorus``/``Drop`` are chorus-role, ``Bridge``/``B`` bridge-role,
``Verse N``/``A1``/``A2``/``A3`` verse-role; every other label is neutral. When no
chorus-role section exists, ``chorus_rising`` evaluates as ``strict_rising`` and
reports ``metrics.no_chorus: 1``. ERROR if there are no rows or any ``energy``
is not an integer in 1..10. One violation per failed condition; ``location`` is
the section label, suffixed ``:<n>`` for the n-th occurrence of a repeated label.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))
import gate_common as gc  # noqa: E402

CURVES = ("chorus_rising", "strict_rising", "free")
_CHORUS_RE = re.compile(r"^(chorus|drop)(\s+\d+)?$", re.I)
_BRIDGE_RE = re.compile(r"^(bridge(\s+\d+)?|b)$", re.I)
_VERSE_RE = re.compile(r"^(verse(\s+\d+)?|a\d+)$", re.I)


def role_of(label: str) -> str:
    s = label.strip()
    if _CHORUS_RE.match(s):
        return "chorus"
    if _BRIDGE_RE.match(s):
        return "bridge"
    if _VERSE_RE.match(s):
        return "verse"
    return "neutral"


def parse_arrangement(text: str) -> list[dict[str, Any]]:
    """[{'label', 'energy' (int|None), 'raw'}] in table order."""
    out: list[dict[str, Any]] = []
    for row in gc.parse_table(text):
        label = row.get("section", "").strip()
        if not label:
            continue
        raw = row.get("energy", "").strip()
        energy: int | None = int(raw) if re.fullmatch(r"-?\d+", raw) else None
        out.append({"label": label, "energy": energy, "raw": raw})
    return out


def locations(labels: list[str]) -> list[str]:
    """``<Label>`` for unique labels, ``<Label>:<n>`` for the n-th of a repeated one."""
    counts = {l: labels.count(l) for l in labels}
    seen: dict[str, int] = {}
    out: list[str] = []
    for l in labels:
        seen[l] = seen.get(l, 0) + 1
        out.append(f"{l}:{seen[l]}" if counts[l] > 1 else l)
    return out


def check_strict_rising(energies: list[int], locs: list[str], res: gc.GateResult, tag: str) -> None:
    g = max(energies)
    peak = energies.index(g)
    for i in range(1, len(energies)):
        if i <= peak and energies[i] < energies[i - 1]:
            res.violate(locs[i], f"({tag}) energy falls before the peak", energies[i], energies[i - 1])
        elif i > peak and energies[i] > energies[i - 1]:
            res.violate(locs[i], f"({tag}) energy rises after the peak", energies[i], energies[i - 1])


def check_chorus_rising(rows: list[dict[str, Any]], locs: list[str], res: gc.GateResult) -> None:
    energies = [r["energy"] for r in rows]
    roles = [role_of(r["label"]) for r in rows]
    g = max(energies)
    chorus_idx = [i for i, r in enumerate(roles) if r == "chorus"]
    # (a) choruses never fall
    for a, b in zip(chorus_idx, chorus_idx[1:]):
        if energies[b] < energies[a]:
            res.violate(locs[b], "(a) chorus energy falls below the previous chorus", energies[b], energies[a])
    # (b) the global maximum lands in the final chorus or the bridge
    last_chorus = chorus_idx[-1]
    allowed = {last_chorus} | {i for i, r in enumerate(roles) if r == "bridge"}
    if not any(energies[i] == g for i in allowed):
        first_peak = energies.index(g)
        res.violate(locs[first_peak], "(b) global maximum occurs outside the final chorus and the bridge",
                    g, energies[last_chorus])
    # (c) the final section sits below the peak unless it is the last chorus
    final = len(rows) - 1
    if final != last_chorus and energies[final] >= g:
        res.violate(locs[final], "(c) final section is not below the global maximum", energies[final], g)
    # (d) every verse sits below the next chorus
    for i, role in enumerate(roles):
        if role != "verse":
            continue
        nxt = next((c for c in chorus_idx if c > i), None)
        if nxt is not None and energies[i] >= energies[nxt]:
            res.violate(locs[i], "(d) verse energy is not below the next chorus", energies[i], energies[nxt])


def add_args(p: Any) -> None:
    p.add_argument("--energy-curve", choices=CURVES, metavar="CURVE",
                   help="override quality.energy_curve (chorus_rising | strict_rising | free)")


def main_fn(args: Any, config: dict[str, Any], res: gc.GateResult) -> gc.GateResult:
    genre = gc.resolve_genre(args.genre, args.paths)
    curve = gc.resolve_threshold("energy_curve", config, genre, args.energy_curve, kind=str)
    res.thresholds["energy_curve"] = curve
    if curve not in CURVES:
        return res.error(f"unknown energy_curve {curve!r}; expected one of {', '.join(CURVES)}")
    apath = gc.file_named(args.paths, "arrangement.md")
    if not apath:
        return res.error("arrangement.md not given")
    rows = parse_arrangement(gc.read_text(apath))
    if not rows:
        return res.error("no section rows with energy found in arrangement.md", "arrangement.md")
    locs = locations([r["label"] for r in rows])
    for r, loc in zip(rows, locs):
        if r["energy"] is None or not 1 <= r["energy"] <= 10:
            return res.error(f"energy must be an integer in 1..10, got {r['raw']!r}", loc)
    energies = [r["energy"] for r in rows]
    chorus_count = sum(1 for r in rows if role_of(r["label"]) == "chorus")
    res.metrics.update({"sections": len(rows), "global_max": max(energies), "chorus_count": chorus_count})
    if curve == "free":
        return res
    if curve == "chorus_rising" and chorus_count == 0:
        res.metrics["no_chorus"] = 1
        check_strict_rising(energies, locs, res, "strict_rising")
    elif curve == "chorus_rising":
        check_chorus_rising(rows, locs, res)
    else:
        check_strict_rising(energies, locs, res, "strict_rising")
    return res


def main(argv: list[str] | None = None) -> int:
    return gc.run("arrangement_check.py", "Energy-curve gate for arrangement.md.", add_args, main_fn, argv)


if __name__ == "__main__":
    sys.exit(main())
