#!/usr/bin/env python3
"""arrangement_check.py - Stage 6 gate for arrangement.md (stage-gates.md section 3).

Checks, in order:
  * table shape (ERROR 3 on a malformed table: missing columns, wrong cell count,
    non-integer or out-of-range energy, no rows)
  * every row has a non-empty instrumentation cell (``instruments_in`` and
    ``instruments_out``; ``-`` is allowed for ``instruments_out`` and for
    ``instruments_in`` on every section except the first)
  * section list equals structure.md (``--structure``): missing and extra sections
  * energy range: max - min >= ``--min-energy-range`` (config quality.min_energy_range, default 3)
  * energy curve per ``quality.energy_curve`` (chorus_rising | strict_rising | free)
  * text hygiene: no "sounds like" / "reference track" and no blocked-targets.txt phrase

Usage: arrangement_check.py [--config C] [--json] [--genre G] [--min-energy-range N]
                            [--energy-curve CURVE] [--structure structure.md] arrangement.md
Exit codes: 0 PASS | 1 FAIL | 2 SKIPPED | 3 ERROR. ``--selftest`` runs built-in cases.
Stdlib only; safe under ``python -I``.
"""
from __future__ import annotations

import re
import sys
from collections import Counter
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))
import gate_common as gc  # noqa: E402

COLUMNS = ("section", "energy", "instruments_in", "instruments_out", "texture_note")
CURVES = ("chorus_rising", "strict_rising", "free")
DEFAULT_MIN_RANGE = 3
BANNED_PHRASES = ("sounds like", "reference track")

_CHORUS = re.compile(r"^(chorus|drop)\b", re.I)
_VERSE = re.compile(r"^(verse\b|a\d\b)", re.I)
_BRIDGE = re.compile(r"^(bridge|b)$", re.I)


def role_of(label: str) -> str:
    """chorus | verse | bridge | other (Drop counts as chorus, AABA B as bridge)."""
    s = label.strip()
    if _CHORUS.match(s):
        return "chorus"
    if _BRIDGE.match(s):
        return "bridge"
    if _VERSE.match(s):
        return "verse"
    return "other"


def parse_arrangement(text: str) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    """Return (header, rows). Raises ValueError on a malformed table."""
    header = gc.parse_header_keys(text)
    cols: list[str] | None = None
    rows: list[dict[str, Any]] = []
    for lineno, line in enumerate(text.splitlines(), 1):
        s = line.strip()
        if not s.startswith("|"):
            continue
        cells = [c.strip() for c in s.strip("|").split("|")]
        if cols is None:
            cols = [c.lower() for c in cells]
            missing = [c for c in COLUMNS if c not in cols]
            if missing:
                raise ValueError(f"arrangement table missing column(s): {', '.join(missing)}")
            continue
        if gc.is_separator_row(cells):
            continue
        if len(cells) != len(cols):
            raise ValueError(f"line {lineno}: expected {len(cols)} cells, found {len(cells)}")
        row: dict[str, Any] = dict(zip(cols, cells))
        label = row["section"]
        if not label:
            raise ValueError(f"line {lineno}: empty section label")
        try:
            energy = int(row["energy"])
        except ValueError:
            raise ValueError(f"line {lineno}: energy {row['energy']!r} is not an integer") from None
        if not 1 <= energy <= 10:
            raise ValueError(f"line {lineno}: energy {energy} outside 1..10")
        row["energy"] = energy
        row["_line"] = lineno
        rows.append(row)
    if cols is None or not rows:
        raise ValueError("no arrangement table rows found")
    return header, rows


def _loc(rows: list[dict[str, Any]], i: int) -> str:
    return f"{rows[i]['section']} [row {i + 1}]"


def check_curve(rows: list[dict[str, Any]], curve: str, res: gc.GateResult) -> None:
    energies = [r["energy"] for r in rows]
    roles = [role_of(r["section"]) for r in rows]
    g = max(energies)
    res.metrics["energy_max"], res.metrics["energy_min"] = g, min(energies)
    if curve == "free":
        return
    chorus_idx = [i for i, r in enumerate(roles) if r == "chorus"]
    if curve == "chorus_rising" and not chorus_idx:
        res.metrics["no_chorus"] = 1
        curve = "strict_rising"
    if curve == "strict_rising":
        peak = energies.index(g)
        for i in range(1, peak + 1):
            if energies[i] < energies[i - 1]:
                res.violate(_loc(rows, i), "energy falls before the peak", energies[i], f">= {energies[i - 1]}")
        for i in range(peak + 1, len(energies)):
            if energies[i] > energies[i - 1]:
                res.violate(_loc(rows, i), "energy rises after the peak", energies[i], f"<= {energies[i - 1]}")
        return
    # chorus_rising
    for a, b in zip(chorus_idx, chorus_idx[1:]):
        if energies[b] < energies[a]:
            res.violate(_loc(rows, b), "chorus energy lower than the previous chorus", energies[b], f">= {energies[a]}")
    peak_ok = any(roles[i] == "bridge" or i == chorus_idx[-1] for i in range(len(rows)) if energies[i] == g)
    if not peak_ok:
        res.violate("energy_map", "global energy maximum is not in the final chorus or the bridge", g,
                    "peak in final chorus or bridge")
    last = len(rows) - 1
    if energies[last] >= g and last != chorus_idx[-1]:
        res.violate(_loc(rows, last), "final section ties the peak but is not the last chorus", energies[last],
                    f"< {g}")
    for i, role in enumerate(roles):
        if role != "verse":
            continue
        nxt = next((j for j in chorus_idx if j > i), None)
        if nxt is not None and energies[i] >= energies[nxt]:
            res.violate(_loc(rows, i), "verse energy is not below the next chorus", energies[i],
                        f"< {energies[nxt]}")


def check_text(text: str, rows: list[dict[str, Any]], res: gc.GateResult) -> None:
    targets = gc.load_list_file(gc.SHARED_DIR / "blocked-targets.txt")
    # Multi-word targets and the banned phrases match case-insensitively. Single-word targets
    # (many are ordinary words: Levels, Memory, Respect) match only in their listed casing so a
    # lowercase texture note such as "levels out" is not a false positive.
    patterns = [(p, re.compile(r"(?<!\w)" + re.escape(p) + r"(?!\w)", re.I)) for p in BANNED_PHRASES]
    for t in targets:
        flags = re.I if " " in t else 0
        patterns.append((t, re.compile(r"(?<!\w)" + re.escape(t) + r"(?!\w)", flags)))
    row_by_line = {r["_line"]: r for r in rows}
    for lineno, line in enumerate(text.splitlines(), 1):
        for phrase, pat in patterns:
            if pat.search(line):
                where = row_by_line.get(lineno)
                loc = where["section"] if where else f"arrangement.md:line {lineno}"
                kind = "banned phrase" if phrase in BANNED_PHRASES else "blocked target"
                res.violate(loc, f"{kind} in arrangement text (originality clause 3)", phrase, "technical language only")


def main_fn(args: Any, config: dict[str, Any], res: gc.GateResult) -> gc.GateResult:
    apath = gc.file_named(args.paths, "arrangement.md")
    if not apath:
        return res.error("arrangement.md not given")
    text = gc.read_text(apath)
    genre = gc.resolve_genre(args.genre, args.paths)
    min_range = gc.resolve_threshold("min_energy_range", config, genre, args.min_energy_range,
                                     default=DEFAULT_MIN_RANGE, kind=int)
    curve = str(gc.resolve_threshold("energy_curve", config, genre, args.energy_curve)).lower()
    if curve not in CURVES:
        raise ValueError(f"threshold energy_curve must be one of {', '.join(CURVES)}, got {curve!r}")
    res.thresholds.update({"min_energy_range": min_range, "energy_curve": curve})
    _, rows = parse_arrangement(text)
    res.metrics["sections"] = len(rows)

    # instrumentation cells
    for i, row in enumerate(rows):
        cin, cout = row["instruments_in"], row["instruments_out"]
        if cin == "" or (cin == "-" and i == 0):
            res.violate(_loc(rows, i), "empty instruments_in cell", cin, "at least one instrument")
        if cout == "":
            res.violate(_loc(rows, i), "empty instruments_out cell (use '-' for none)", cout, "list or '-'")

    # section list vs structure.md
    if args.structure:
        want = [s["label"] for s in gc.parse_structure(gc.read_text(args.structure))["sections"]]
        got = [r["section"] for r in rows]
        res.metrics["structure_sections"] = len(want)
        missing = Counter(want) - Counter(got)
        extra = Counter(got) - Counter(want)
        for lbl, n in missing.items():
            res.violate(lbl, "section in structure.md is missing from arrangement.md", f"{n} missing", "present")
        for lbl, n in extra.items():
            res.violate(lbl, "arrangement.md section is not in structure.md", f"{n} extra", "absent")
        if not missing and not extra and got != want:
            res.violate("arrangement.md:sections", "section order differs from structure.md", got, want)

    if curve != "free":
        energies = [r["energy"] for r in rows]
        span = max(energies) - min(energies)
        res.metrics["energy_range"] = span
        if span < min_range:
            low = rows[energies.index(min(energies))]["section"]
            res.violate(f"{low} [energy map]", "energy map is flat (max - min below minimum range)", span, min_range)
    check_curve(rows, curve, res)
    check_text(text, rows, res)
    return res


def add_args(p: Any) -> None:
    p.add_argument("--min-energy-range", type=int, metavar="N", help="minimum max-min energy spread (default 3)")
    p.add_argument("--energy-curve", metavar="CURVE", help="override quality.energy_curve")
    p.add_argument("--structure", metavar="PATH", help="structure.md to compare the section list against")
    p.add_argument("--selftest", action="store_true", help="run built-in checks and exit")


_GOOD = """key: D
mode: major
bpm: 118
time_sig: 4/4

| section | energy | instruments_in | instruments_out | texture_note |
|---------|--------|----------------|-----------------|--------------|
| Verse 1 | 3 | guitar, bass | - | sparse |
| Chorus | 7 | drums, pad | - | wide |
| Verse 2 | 4 | shaker | pad | thin |
| Chorus | 8 | keys | - | full |
| Bridge | 5 | piano | drums | stripped |
| Chorus | 9 | all backing vocals | - | peak |
"""


def selftest() -> int:
    import tempfile
    cases = [
        ("pass", _GOOD, [], gc.PASS),
        ("flat", _GOOD.replace("| 7 |", "| 3 |").replace("| 8 |", "| 3 |").replace("| 9 |", "| 3 |")
                      .replace("| 4 |", "| 3 |").replace("| 5 |", "| 3 |"), [], gc.FAIL),
        ("chorus-low", _GOOD.replace("| Chorus | 7 |", "| Chorus | 2 |"), [], gc.FAIL),
        ("sounds-like", _GOOD.replace("sparse", "sounds like a demo"), [], gc.FAIL),
        ("bad-energy", _GOOD.replace("| 3 |", "| x |"), [], gc.ERROR),
    ]
    failures = 0
    with tempfile.TemporaryDirectory() as tmp:
        for name, body, extra, want in cases:
            p = Path(tmp) / "arrangement.md"
            p.write_text(body, encoding="utf-8")
            res = gc.GateResult("arrangement_check.py")
            try:
                parser = gc.build_parser("arrangement_check.py", "selftest")
                add_args(parser)
                ns = parser.parse_args([str(p), *extra])
                ns.paths = [gc.norm(x) for x in ns.paths]
                res = main_fn(ns, {}, res)
            except ValueError as exc:
                res.error(str(exc))
            ok = res.status == want
            failures += 0 if ok else 1
            print(f"selftest {name}: {res.status} (want {want}) {'ok' if ok else 'MISMATCH'}")
    print("selftest: " + ("PASS" if failures == 0 else f"FAIL ({failures})"))
    return 0 if failures == 0 else 1


def main(argv: list[str] | None = None) -> int:
    args_in = sys.argv[1:] if argv is None else argv
    if "--selftest" in args_in:
        return selftest()
    return gc.run("arrangement_check.py", "Stage 6 arrangement energy and structure gate.", add_args, main_fn, argv)


if __name__ == "__main__":
    sys.exit(main())
