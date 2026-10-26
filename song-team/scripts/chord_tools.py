#!/usr/bin/env python3
"""chord_tools.py - Roman-numeral chord chart gate for chords.md
(stage-gates.md section 3). Stdlib only; ``python -I`` safe.

Inputs: ``chords.md`` plus ``structure.md`` (key/mode). When structure.md is
absent the ``key: <tonic> <mode>`` header of chords.md is used; ERROR if neither
names a key.

Cell grammar (one chord per ``|`` cell):

    [b|#] <I..VII | i..vii> [dim|°|o|aug|+|maj7|m7|7|sus2|sus4|add9] [/<bass>]
    %                                  repeats the previous cell (counts again)

Upper-case numerals are major triads, lower-case minor; ``dim``/``°``/``o`` and
``aug``/``+`` override the triad quality; seventh/sus/add suffixes are tolerated
and do not change the triad quality test (``sus`` chords have no third and are
diatonic whenever their root is a scale degree). ``<bass>`` is a Roman numeral
(``V``, ``bVII``) or a scale-degree digit (``3``).

Root resolution: a numeral without an accidental names the *mode's* degree
(``VI`` in A minor is F, ``VII`` is G); a numeral with an accidental is spelled
against the major scale and shifted (``bVII`` is always two semitones below the
tonic, ``#iv`` always six above). A chord is diatonic when its root is a scale
degree of the mode and its triad quality is the one the mode builds there.

Concert-pitch spellings are emitted per cell under a top-level ``"concert"``
key of the ``--json`` output (``{"<Label>": [["D", "A", "Bm", "G"], ...]}``,
one list per chart line) and as ``> | D | A | ...`` lines in text mode.
Sharp keys spell with sharps, flat keys with flats; an accidental chord keeps
the spelling direction of its accidental (``bII`` in C is Db, ``#iv`` is F#m).

Warnings (never FAIL; ``metrics.warnings`` and a ``"warnings"`` list):
  * parallel fifths heuristic - two consecutive root-position major/minor
    triads whose roots lie a whole step apart (IV-V, bVII-I, V-IV) are flagged,
    since block voicings of such pairs move every voice in parallel;
  * a section whose last two cells form none of V-I, IV-I, V-vi, bVII-I
    (compared by root degree, ignoring quality).
"""
from __future__ import annotations

import re
import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))
import gate_common as gc  # noqa: E402

_NUMERALS = {"i": 1, "ii": 2, "iii": 3, "iv": 4, "v": 5, "vi": 6, "vii": 7}
_MAJOR_DEGREE_SEMITONES = {1: 0, 2: 2, 3: 4, 4: 5, 5: 7, 6: 9, 7: 11}

# mode -> ((semitone above tonic, triad quality) per degree 1..7)
MODE_TABLES: dict[str, tuple[tuple[int, str], ...]] = {
    "major": ((0, "maj"), (2, "min"), (4, "min"), (5, "maj"), (7, "maj"), (9, "min"), (11, "dim")),
    "minor": ((0, "min"), (2, "dim"), (3, "maj"), (5, "min"), (7, "min"), (8, "maj"), (10, "maj")),
    "dorian": ((0, "min"), (2, "min"), (3, "maj"), (5, "maj"), (7, "min"), (9, "dim"), (10, "maj")),
    "phrygian": ((0, "min"), (1, "maj"), (3, "maj"), (5, "min"), (7, "dim"), (8, "maj"), (10, "min")),
    "lydian": ((0, "maj"), (2, "maj"), (4, "min"), (6, "dim"), (7, "maj"), (9, "min"), (11, "min")),
    "mixolydian": ((0, "maj"), (2, "min"), (4, "dim"), (5, "maj"), (7, "min"), (9, "min"), (10, "maj")),
    "locrian": ((0, "dim"), (1, "maj"), (3, "min"), (5, "min"), (6, "maj"), (8, "maj"), (10, "min")),
}
MODE_TABLES["ionian"] = MODE_TABLES["major"]
MODE_TABLES["aeolian"] = MODE_TABLES["minor"]
_MODE_ABBREV = {"m": "minor", "min": "minor", "maj": "major", "dor": "dorian", "mix": "mixolydian",
                "lyd": "lydian", "phr": "phrygian", "loc": "locrian", "aeo": "aeolian", "ion": "ionian"}

_PC = {"C": 0, "D": 2, "E": 4, "F": 5, "G": 7, "A": 9, "B": 11}
_SHARP_NAMES = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
_FLAT_NAMES = ["C", "Db", "D", "Eb", "E", "F", "Gb", "G", "Ab", "A", "Bb", "B"]
_MAJOR_SHARPS = {"C": 0, "G": 1, "D": 2, "A": 3, "E": 4, "B": 5, "F#": 6, "C#": 7,
                 "F": -1, "Bb": -2, "Eb": -3, "Ab": -4, "Db": -5, "Gb": -6, "Cb": -7}
_MODE_OFFSET = {"major": 0, "ionian": 0, "minor": -3, "aeolian": -3, "dorian": -2,
                "mixolydian": -1, "lydian": 1, "phrygian": -4, "locrian": -5}

_ROMAN = r"VII|VI|IV|V|III|II|I|vii|vi|iv|v|iii|ii|i"
_CELL_RE = re.compile(
    r"^(?P<acc>[b#]?)(?P<num>" + _ROMAN + r")"
    r"(?P<qual>maj7|dim7|m7b5|sus2|sus4|add9|dim|aug|m7|7|°|o|\+)?"
    r"(?:/(?P<bass>[b#]?(?:" + _ROMAN + r"|[1-7])))?$"
)
CADENCES = ("V-I", "IV-I", "V-vi", "bVII-I")


# ---------------------------------------------------------------------------
# Parsing
# ---------------------------------------------------------------------------
def parse_roman(cell: str) -> tuple[int, int, bool, str, tuple[int, int] | None]:
    """``'bVII7/V'`` -> (accidental, degree, is_minor, quality, bass).

    accidental: -1 for ``b``, +1 for ``#``, else 0. degree: 1..7. is_minor: the
    numeral is lower-case. quality: the triad (``maj``/``min``/``dim``/``aug``)
    followed by any tolerated suffix (``maj7``, ``min7``, ``majsus4`` ...).
    bass: ``(accidental, degree)`` of the slash bass, or None.
    ValueError on anything else."""
    m = _CELL_RE.match(cell.strip())
    if not m:
        raise ValueError(f"unparseable chord cell {cell!r}")
    acc = {"b": -1, "#": 1}.get(m.group("acc"), 0)
    num = m.group("num")
    is_minor = num.islower()
    degree = _NUMERALS[num.lower()]
    suffix = m.group("qual") or ""
    if suffix in ("dim", "°", "o", "dim7", "m7b5"):
        triad = "dim"
    elif suffix in ("aug", "+"):
        triad = "aug"
    else:
        triad = "min" if is_minor else "maj"
    if suffix in ("dim", "°", "o", "aug", "+", ""):
        quality = triad
    elif suffix == "m7":
        triad, quality = "min", "min7"
    else:
        quality = triad + suffix
    bass: tuple[int, int] | None = None
    b = m.group("bass")
    if b:
        bacc = {"b": -1, "#": 1}.get(b[0], 0)
        core = b[1:] if b[0] in "b#" else b
        bass = (bacc, int(core) if core.isdigit() else _NUMERALS[core.lower()])
    return acc, degree, is_minor, quality, bass


def triad_of(quality: str) -> str:
    for t in ("maj", "min", "dim", "aug"):
        if quality.startswith(t):
            return t
    return quality


def normalise_mode(word: str | None) -> str:
    w = (word or "major").strip().lower()
    if w in MODE_TABLES:
        return w
    w = _MODE_ABBREV.get(w[:3], w)
    if w not in MODE_TABLES:
        raise ValueError(f"unknown mode {word!r}")
    return w


def root_semitone(mode: str, acc: int, degree: int) -> int:
    """Semitones above the tonic (see the module docstring for the two conventions)."""
    if acc == 0:
        return MODE_TABLES[mode][degree - 1][0]
    return (_MAJOR_DEGREE_SEMITONES[degree] + acc) % 12


def is_diatonic(mode: str, parsed: tuple) -> bool:
    acc, degree, _is_minor, quality, _bass = parsed
    root = root_semitone(mode, acc, degree)
    for semi, tri in MODE_TABLES[mode]:
        if semi == root:
            return True if quality.startswith("sus") else triad_of(quality) == tri
    return False


def _tonic_pc(tonic: str) -> int:
    t = tonic.strip()
    if not t or t[0].upper() not in _PC:
        raise ValueError(f"unknown key {tonic!r}")
    pc = _PC[t[0].upper()]
    for ch in t[1:]:
        if ch == "#":
            pc += 1
        elif ch == "b":
            pc -= 1
        else:
            raise ValueError(f"unknown key {tonic!r}")
    return pc % 12


def key_uses_flats(tonic: str, mode: str) -> bool:
    t = tonic.strip()
    t = t[:1].upper() + t[1:]
    return _MAJOR_SHARPS.get(t, 0) + _MODE_OFFSET.get(mode, 0) < 0


def _spell(pc: int, flats: bool) -> str:
    return (_FLAT_NAMES if flats else _SHARP_NAMES)[pc % 12]


def concert_name(key: str, mode: str, parsed: tuple) -> str:
    """Concert-pitch chord symbol for a parsed cell (``'Bm'``, ``'A7/C#'``)."""
    acc, degree, _is_minor, quality, bass = parsed
    mode = normalise_mode(mode)
    tonic = _tonic_pc(key)
    flats = key_uses_flats(key, mode)
    root = _spell(tonic + root_semitone(mode, acc, degree), flats if acc == 0 else acc < 0)
    tri = triad_of(quality)
    sym = root + {"maj": "", "min": "m", "dim": "dim", "aug": "aug"}[tri] + quality[len(tri):]
    if bass:
        bacc, bdeg = bass
        sym += "/" + _spell(tonic + root_semitone(mode, bacc, bdeg), flats if bacc == 0 else bacc < 0)
    return sym


def split_cells(line: str) -> list[str]:
    return [c.strip() for c in line.strip().strip("|").split("|") if c.strip() != ""]


def parse_chart(text: str) -> list[tuple[str, list[list[str]]]]:
    """``[Label]`` -> chart lines (each a list of raw cells). ``>`` concert lines
    and ``#`` comments are ignored; only ``|`` lines count."""
    return [(label, [split_cells(l) for l in lines if l.startswith("|")])
            for label, lines in gc.parse_sections(text)]


def _key_from_header(header: dict[str, Any]) -> tuple[str, str] | None:
    key = header.get("key")
    if not key:
        return None
    parts = str(key).split()
    mode = header.get("mode") or (parts[1] if len(parts) > 1 else "major")
    return parts[0], normalise_mode(str(mode))


def resolve_key(paths: list[str], chords_text: str) -> tuple[str, str]:
    """(tonic, mode) from structure.md, else the chords.md ``key:`` header."""
    spath = gc.file_named(paths, "structure.md")
    if spath:
        found = _key_from_header(gc.parse_header_keys(gc.read_text(spath)))
        if found:
            return found
    found = _key_from_header(gc.parse_header_keys(chords_text))
    if found:
        return found
    raise ValueError("no key found in structure.md or the chords.md header")


# ---------------------------------------------------------------------------
# Result with concert spellings
# ---------------------------------------------------------------------------
class ChordResult(gc.GateResult):
    def __init__(self, script: str):
        super().__init__(script)
        self.concert: dict[str, list[list[str]]] = {}

    def to_dict(self) -> dict[str, Any]:
        d = super().to_dict()
        if self.concert:
            d["concert"] = self.concert
        return d

    def emit(self, as_json: bool) -> int:
        code = super().emit(as_json)
        if not as_json and self.concert:
            for label, lines in self.concert.items():
                sys.stdout.write(f"  [{label}]\n")
                for cells in lines:
                    sys.stdout.write("  > | " + " | ".join(cells) + " |\n")
            sys.stdout.flush()
        return code


# ---------------------------------------------------------------------------
# Analysis
# ---------------------------------------------------------------------------
def _cadence_ok(mode: str, prev: tuple, last: tuple) -> bool:
    p = root_semitone(mode, prev[0], prev[1])
    l = root_semitone(mode, last[0], last[1])
    vi = MODE_TABLES[mode][5][0]
    return (l == 0 and p in (7, 5, 10)) or (p == 7 and l == vi)


def _parallel_fifths(mode: str, a: tuple, b: tuple) -> bool:
    if a[4] is not None or b[4] is not None:
        return False
    if triad_of(a[3]) not in ("maj", "min") or triad_of(b[3]) not in ("maj", "min"):
        return False
    return (root_semitone(mode, b[0], b[1]) - root_semitone(mode, a[0], a[1])) % 12 in (2, 10)


def analyse(chart: list[tuple[str, list[list[str]]]], key: str, mode: str, res: ChordResult,
            min_ratio: float) -> ChordResult:
    total = diatonic = 0
    non_diatonic: list[tuple[str, str]] = []
    for label, lines in chart:
        prev: tuple | None = None
        prev_loc = ""
        flat: list[tuple[str, tuple]] = []
        concert_lines: list[list[str]] = []
        for li, cells in enumerate(lines, 1):
            names: list[str] = []
            for ci, cell in enumerate(cells, 1):
                loc = f"{label}:{li}:{ci}"
                if cell == "%":
                    if prev is None:
                        return res.error("'%' repeat with no previous cell", loc)
                    parsed = prev
                else:
                    try:
                        parsed = parse_roman(cell)
                    except ValueError as exc:
                        return res.error(str(exc), loc)
                total += 1
                if is_diatonic(mode, parsed):
                    diatonic += 1
                else:
                    non_diatonic.append((loc, cell))
                names.append(concert_name(key, mode, parsed))
                if prev is not None and _parallel_fifths(mode, prev, parsed):
                    res.warn(loc, "possible parallel fifths: adjacent root-position triads a whole step apart",
                             f"{prev_loc} -> {loc}", None)
                flat.append((loc, parsed))
                prev, prev_loc = parsed, loc
            concert_lines.append(names)
        res.concert[label] = concert_lines
        if len(flat) >= 2 and not _cadence_ok(mode, flat[-2][1], flat[-1][1]):
            res.warn(flat[-1][0], "section does not end on a cadence", None, " | ".join(CADENCES))
    if total == 0:
        return res.error("no chord cells found in chords.md")
    ratio = diatonic / total
    res.metrics.update({"chords_total": total, "diatonic": diatonic, "diatonic_ratio": round(ratio, 4),
                        "sections": len(chart)})
    res.metrics.setdefault("warnings", 0)
    if ratio + 1e-9 < min_ratio:
        for loc, cell in non_diatonic:
            res.violate(loc, f"non-diatonic chord {cell!r} in {key} {mode}", round(ratio, 4), min_ratio)
        res.violate("chords.md", "diatonic ratio below diatonic_min_ratio", round(ratio, 4), min_ratio)
    return res


# ---------------------------------------------------------------------------
# Entry
# ---------------------------------------------------------------------------
def add_args(p: Any) -> None:
    p.add_argument("--diatonic-min-ratio", type=float, metavar="R", help="override quality.diatonic_min_ratio")


def main_fn(args: Any, config: dict[str, Any], res: gc.GateResult) -> gc.GateResult:
    out = ChordResult(res.script)
    genre = gc.resolve_genre(args.genre, args.paths)
    min_ratio = gc.resolve_threshold("diatonic_min_ratio", config, genre, args.diatonic_min_ratio, kind=float)
    out.thresholds["diatonic_min_ratio"] = min_ratio
    cpath = gc.file_named(args.paths, "chords.md")
    if not cpath:
        return out.error("chords.md not given")
    text = gc.read_text(cpath)
    try:
        key, mode = resolve_key(args.paths, text)
    except ValueError as exc:
        return out.error(str(exc), "chords.md:key")
    out.thresholds["key"] = f"{key} {mode}"
    return analyse(parse_chart(text), key, mode, out, min_ratio)


def main(argv: list[str] | None = None) -> int:
    return gc.run("chord_tools.py", "Roman-numeral chord chart gate (diatonic ratio, concert spellings).",
                  add_args, main_fn, argv)


if __name__ == "__main__":
    sys.exit(main())
