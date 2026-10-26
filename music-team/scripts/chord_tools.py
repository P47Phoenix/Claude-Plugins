#!/usr/bin/env python3
"""chord_tools.py - chord spelling, transposition, Roman numerals, reharmonization,
and the Stage 5 chords.md gate (stage-gates.md section 3).

Two modes, stdlib only, safe under ``python -I``:

Tool mode (subcommands)
    chord_tools.py scale <tonic> <mode...>
    chord_tools.py chord <symbol>
    chord_tools.py transpose <chords...> --by P5|m3|--by=-M2   (or --to <key> [--from-key <key>])
    chord_tools.py diatonic <key> [--mode minor]
    chord_tools.py roman <key> <chords...>
    chord_tools.py reharmonize <key> <chords...> --style jazz|blues|gospel|bossa-nova|pop [--tritone]
    Every subcommand accepts --json.

Gate mode (default when the first argument is not a subcommand)
    chord_tools.py [--check] [--key K] [--config C] [--json] [--genre G] chords.md [structure.md]
    Exit codes follow gate_common: 0 PASS | 1 FAIL | 2 SKIPPED | 3 ERROR.

    chord_tools.py --selftest

Roman numerals are major-scale relative with accidentals (minor key: i, bIII, iv, v/V, bVI, bVII);
uppercase = major triad, lowercase = minor, ``°`` diminished, ``ø7`` half-diminished, ``+`` augmented.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))
import gate_common as gc  # noqa: E402

LETTERS = "CDEFGAB"
BASE_PC = {"C": 0, "D": 2, "E": 4, "F": 5, "G": 7, "A": 9, "B": 11}
MAJOR = [0, 2, 4, 5, 7, 9, 11]

MODES: dict[str, list[int]] = {
    "major": MAJOR,
    "minor": [0, 2, 3, 5, 7, 8, 10],
    "harmonic minor": [0, 2, 3, 5, 7, 8, 11],
    "melodic minor": [0, 2, 3, 5, 7, 9, 11],
    "dorian": [0, 2, 3, 5, 7, 9, 10],
    "phrygian": [0, 1, 3, 5, 7, 8, 10],
    "lydian": [0, 2, 4, 6, 7, 9, 11],
    "mixolydian": [0, 2, 4, 5, 7, 9, 10],
    "locrian": [0, 1, 3, 5, 6, 8, 10],
}
MODE_ALIASES = {
    "": "major", "maj": "major", "major": "major", "ionian": "major", "ion": "major",
    "m": "minor", "min": "minor", "minor": "minor", "aeolian": "minor", "aeo": "minor",
    "natural minor": "minor", "harmonic minor": "harmonic minor", "melodic minor": "melodic minor",
    "dorian": "dorian", "dor": "dorian", "phrygian": "phrygian", "phr": "phrygian",
    "lydian": "lydian", "lyd": "lydian", "mixolydian": "mixolydian", "mix": "mixolydian",
    "locrian": "locrian", "loc": "locrian",
}

Note = tuple[int, int]  # (letter index 0-6, pitch class 0-11)


# ---------------------------------------------------------------------------
# Spelling
# ---------------------------------------------------------------------------
def spell(note: Note) -> str:
    idx, pc = note
    letter = LETTERS[idx % 7]
    d = (pc - BASE_PC[letter]) % 12
    if d > 6:
        d -= 12
    return letter + ("#" * d if d > 0 else "b" * (-d))


def parse_note(text: str) -> Note:
    m = re.fullmatch(r"([A-Ga-g])([#b]*)", text.strip())
    if not m:
        raise ValueError(f"cannot parse note {text!r}")
    letter = m.group(1).upper()
    acc = m.group(2).count("#") - m.group(2).count("b")
    return LETTERS.index(letter), (BASE_PC[letter] + acc) % 12


def norm_mode(word: str) -> str:
    key = re.sub(r"[-_\s]+", " ", word.strip().lower())
    if key not in MODE_ALIASES:
        raise ValueError(f"unknown mode {word!r}")
    return MODE_ALIASES[key]


def parse_key(text: str, mode: str | None = None) -> tuple[Note, str]:
    """``'D'``, ``'Bb'``, ``'F#m'``, ``'D minor'``, ``'C:'`` -> (tonic note, canonical mode)."""
    s = text.strip().rstrip(":").strip()
    m = re.match(r"^([A-Ga-g])([#b]*)\s*(.*)$", s)
    if not m:
        raise ValueError(f"cannot parse key {text!r}")
    tonic = parse_note(m.group(1) + m.group(2))
    suffix = m.group(3).strip()
    if mode:
        return tonic, norm_mode(mode)
    return tonic, norm_mode(suffix)


def scale_notes(tonic: Note, mode: str) -> list[Note]:
    steps = MODES[mode]
    return [((tonic[0] + i) % 7, (tonic[1] + steps[i]) % 12) for i in range(7)]


def scale_pcs(tonic: Note, mode: str) -> set[int]:
    pcs = {n[1] for n in scale_notes(tonic, mode)}
    if mode in ("minor", "dorian", "phrygian", "locrian"):
        pcs.add((tonic[1] + 11) % 12)  # raised 7th: V and vii° are idiomatic in minor keys
    return pcs


# ---------------------------------------------------------------------------
# Chord model
# ---------------------------------------------------------------------------
def _q(*parts: tuple[int, int]) -> list[tuple[int, int]]:
    return list(parts)


_MAJ = _q((0, 0), (2, 4), (4, 7))
_MIN = _q((0, 0), (2, 3), (4, 7))
_DIM = _q((0, 0), (2, 3), (4, 6))
QUALITIES: dict[str, list[tuple[int, int]]] = {
    "": _MAJ, "m": _MIN, "dim": _DIM, "aug": _q((0, 0), (2, 4), (4, 8)),
    "sus2": _q((0, 0), (1, 2), (4, 7)), "sus4": _q((0, 0), (3, 5), (4, 7)), "5": _q((0, 0), (4, 7)),
    "6": _MAJ + _q((5, 9)), "m6": _MIN + _q((5, 9)),
    "7": _MAJ + _q((6, 10)), "maj7": _MAJ + _q((6, 11)), "m7": _MIN + _q((6, 10)),
    "m7b5": _DIM + _q((6, 10)), "dim7": _DIM + _q((6, 9)), "mMaj7": _MIN + _q((6, 11)),
    "add9": _MAJ + _q((1, 14)), "madd9": _MIN + _q((1, 14)),
    "9": _MAJ + _q((6, 10), (1, 14)), "maj9": _MAJ + _q((6, 11), (1, 14)), "m9": _MIN + _q((6, 10), (1, 14)),
    "11": _MAJ + _q((6, 10), (1, 14), (3, 17)), "m11": _MIN + _q((6, 10), (1, 14), (3, 17)),
    "13": _MAJ + _q((6, 10), (1, 14), (5, 21)), "m13": _MIN + _q((6, 10), (1, 14), (5, 21)),
    "7sus4": _q((0, 0), (3, 5), (4, 7), (6, 10)),
    "7b9": _MAJ + _q((6, 10), (1, 13)), "7#9": _MAJ + _q((6, 10), (1, 15)),
    "7#11": _MAJ + _q((6, 10), (3, 18)), "7b13": _MAJ + _q((6, 10), (5, 20)),
    "7b5": _q((0, 0), (2, 4), (4, 6), (6, 10)), "7#5": _q((0, 0), (2, 4), (4, 8), (6, 10)),
}
QUALITY_ALIASES = {
    "maj": "", "M": "", "min": "m", "-": "m", "o": "dim", "°": "dim", "+": "aug", "sus": "sus4",
    "M7": "maj7", "Δ": "maj7", "Δ7": "maj7", "major7": "maj7", "min7": "m7", "-7": "m7",
    "ø": "m7b5", "ø7": "m7b5", "m7-5": "m7b5", "o7": "dim7", "°7": "dim7",
    "mmaj7": "mMaj7", "mM7": "mMaj7", "minMaj7": "mMaj7", "mmaj": "mMaj7", "m-maj7": "mMaj7",
    "min6": "m6", "min9": "m9", "M9": "maj9", "Δ9": "maj9", "min11": "m11", "min13": "m13",
    "2": "sus2", "4": "sus4", "7+5": "7#5", "7-5": "7b5", "7-9": "7b9", "7+9": "7#9", "7+11": "7#11",
    "add2": "add9", "madd2": "madd9",
}


class Chord:
    __slots__ = ("root", "quality", "bass")

    def __init__(self, root: Note, quality: str = "", bass: Note | None = None):
        if quality not in QUALITIES:
            raise ValueError(f"unknown chord quality {quality!r}")
        self.root, self.quality, self.bass = root, quality, bass

    def tones(self) -> list[Note]:
        return [((self.root[0] + s) % 7, (self.root[1] + x) % 12) for s, x in QUALITIES[self.quality]]

    def pcs(self) -> set[int]:
        out = {n[1] for n in self.tones()}
        if self.bass:
            out.add(self.bass[1])
        return out

    def symbol(self) -> str:
        return spell(self.root) + self.quality + ("/" + spell(self.bass) if self.bass else "")

    def spelling(self) -> list[str]:
        names = [spell(n) for n in self.tones()]
        if self.bass and spell(self.bass) not in names:
            names.insert(0, spell(self.bass))
        elif self.bass:
            names.remove(spell(self.bass))
            names.insert(0, spell(self.bass))
        return names

    def has_minor_third(self) -> bool:
        return any(s == 2 and x == 3 for s, x in QUALITIES[self.quality])

    def has_seventh(self) -> bool:
        return any(s == 6 for s, _ in QUALITIES[self.quality])

    def triad_root_position(self) -> bool:
        return self.bass is None and self.quality in ("", "m")


def canon_quality(raw: str) -> str:
    s = raw.replace("(", "").replace(")", "").replace(" ", "")
    if s in QUALITIES:
        return s
    if s in QUALITY_ALIASES:
        return QUALITY_ALIASES[s]
    if s.lower() in QUALITY_ALIASES and s.lower() not in ("m", "M"):
        return QUALITY_ALIASES[s.lower()]
    raise ValueError(f"unknown chord quality {raw!r}")


def parse_chord(symbol: str) -> Chord:
    m = re.fullmatch(r"([A-G])([#b]*)([^/]*)(?:/([A-G])([#b]*))?", symbol.strip())
    if not m:
        raise ValueError(f"cannot parse chord symbol {symbol!r}")
    root = parse_note(m.group(1) + m.group(2))
    try:
        quality = canon_quality(m.group(3))
    except ValueError:
        raise ValueError(f"cannot parse chord symbol {symbol!r}") from None
    bass = parse_note(m.group(4) + m.group(5)) if m.group(4) else None
    return Chord(root, quality, bass)


# ---------------------------------------------------------------------------
# Roman numerals
# ---------------------------------------------------------------------------
ROMAN_RE = re.compile(r"^([b#]*)(VII|VI|IV|V|III|II|I|vii|vi|iv|v|iii|ii|i)(.*)$")
ROMAN_NUM = {"i": 0, "ii": 1, "iii": 2, "iv": 3, "v": 4, "vi": 5, "vii": 6}
ROMAN_NAMES = ["I", "bII", "II", "bIII", "III", "IV", "#IV", "V", "bVI", "VI", "bVII", "VII"]
DEGREE_NAMES = ["1", "b2", "2", "b3", "3", "4", "#4", "5", "b6", "6", "b7", "7"]
OFFSET_DEGREE = {0: (0, 0), 1: (1, -1), 2: (1, 0), 3: (2, -1), 4: (2, 0), 5: (3, 0), 6: (3, 1),
                 7: (4, 0), 8: (5, -1), 9: (5, 0), 10: (6, -1), 11: (6, 0)}
ROMAN_SUFFIX = {"": "", "m": "", "dim": "°", "aug": "+", "m7": "7", "maj7": "maj7", "7": "7", "m7b5": "ø7",
                "dim7": "°7", "mMaj7": "maj7", "m6": "6", "madd9": "add9", "m9": "9", "m11": "11", "m13": "13"}


def degree_note(tonic: Note, degree: int, acc: int) -> Note:
    return (tonic[0] + degree) % 7, (tonic[1] + MAJOR[degree] + acc) % 12


def chord_on_degree(tonic: Note, degree: int, acc: int, quality: str, bass: Note | None = None) -> Chord:
    return Chord(degree_note(tonic, degree, acc), quality, bass)


def _roman_quality(lower: bool, rest: str) -> str:
    if rest.startswith(("°", "dim", "o")) and not rest.startswith("omit"):
        tail = re.sub(r"^(°|dim|o)", "", rest)
        return canon_quality("dim" + tail)
    if rest.startswith("ø") or rest.startswith("m7b5"):
        return "m7b5"
    if rest.startswith("+") or rest.startswith("aug"):
        return "aug"
    if rest.startswith("sus"):
        return canon_quality(rest)
    if lower:
        if rest.startswith(("maj", "M")):
            return canon_quality("mMaj7" if rest in ("maj7", "M7") else "m" + rest)
        return canon_quality("m" + rest)
    return canon_quality(rest)


def roman_to_chord(token: str, tonic: Note) -> Chord:
    m = ROMAN_RE.match(token.strip())
    if not m:
        raise ValueError(f"cannot parse Roman numeral {token!r}")
    acc = m.group(1).count("#") - m.group(1).count("b")
    numeral = m.group(2)
    body, _, tail = m.group(3).partition("/")
    try:
        quality = _roman_quality(numeral.islower(), body)
        degree = ROMAN_NUM[numeral.lower()]
        bass: Note | None = None
        base_tonic = tonic
        if tail:
            tm = ROMAN_RE.match(tail)
            bm = re.fullmatch(r"([b#]?)([1-7])", tail)
            if tm and not tm.group(3):  # secondary function, e.g. V7/vi
                t_acc = tm.group(1).count("#") - tm.group(1).count("b")
                base_tonic = degree_note(tonic, ROMAN_NUM[tm.group(2).lower()], t_acc)
            elif bm:
                b_acc = {"b": -1, "#": 1, "": 0}[bm.group(1)]
                bass = degree_note(tonic, int(bm.group(2)) - 1, b_acc)
            elif re.fullmatch(r"[A-G][#b]*", tail):
                bass = parse_note(tail)
            else:
                raise ValueError(f"bad slash target {tail!r}")
    except ValueError as exc:
        raise ValueError(f"cannot parse Roman numeral {token!r}: {exc}") from None
    return chord_on_degree(base_tonic, degree, acc, quality, bass)


def chord_to_roman(chord: Chord, tonic: Note) -> str:
    off = (chord.root[1] - tonic[1]) % 12
    name = ROMAN_NAMES[off]
    q = chord.quality
    lower = chord.has_minor_third()
    if lower:
        name = re.sub(r"[IV]+", lambda mm: mm.group(0).lower(), name)
    suffix = ROMAN_SUFFIX.get(q, q)
    out = name + suffix
    if chord.bass:
        out += "/" + DEGREE_NAMES[(chord.bass[1] - tonic[1]) % 12]
    return out


def is_diatonic(chord: Chord, tonic: Note, mode: str) -> bool:
    return chord.pcs() <= scale_pcs(tonic, mode)


# ---------------------------------------------------------------------------
# Transposition
# ---------------------------------------------------------------------------
_SIMPLE = {1: 0, 2: 2, 3: 4, 4: 5, 5: 7, 6: 9, 7: 11}
_PERFECT = (1, 4, 5)


def parse_interval(text: str) -> tuple[int, int, int]:
    """``'P5'`` -> (1, 4, 7); ``'-M2'`` -> (-1, 1, 2). Returns (direction, letter steps, semitones)."""
    m = re.fullmatch(r"(-?)([PMmAd])(\d+)", text.strip())
    if not m:
        raise ValueError(f"cannot parse interval {text!r} (use e.g. P5, m3, M2, A4, d5, -M2)")
    quality, n = m.group(2), int(m.group(3))
    if n < 1:
        raise ValueError(f"cannot parse interval {text!r}")
    simple = ((n - 1) % 7) + 1
    semis = _SIMPLE[simple] + 12 * ((n - 1) // 7)
    perfect = simple in _PERFECT
    if quality == "P" and not perfect or quality in ("M",) and perfect or quality == "m" and perfect:
        raise ValueError(f"interval quality {quality} is not valid for a {n}th")
    adj = {"P": 0, "M": 0, "m": -1, "A": 1, "d": -1 if perfect else -2}[quality]
    return (-1 if m.group(1) else 1), n - 1, semis + adj


def shift_note(note: Note, direction: int, steps: int, semis: int) -> Note:
    return (note[0] + direction * steps) % 7, (note[1] + direction * semis) % 12


def transpose_chord(chord: Chord, direction: int, steps: int, semis: int) -> Chord:
    bass = shift_note(chord.bass, direction, steps, semis) if chord.bass else None
    return Chord(shift_note(chord.root, direction, steps, semis), chord.quality, bass)


# ---------------------------------------------------------------------------
# Diatonic harmony
# ---------------------------------------------------------------------------
def stacked_quality(tonic: Note, mode: str, degree: int, seventh: bool) -> str:
    notes = scale_notes(tonic, mode)
    pcs = [notes[(degree + k) % 7][1] for k in (0, 2, 4, 6)]
    third, fifth, sev = ((pcs[1] - pcs[0]) % 12, (pcs[2] - pcs[0]) % 12, (pcs[3] - pcs[0]) % 12)
    triad = {(4, 7): "", (3, 7): "m", (3, 6): "dim", (4, 8): "aug"}.get((third, fifth), "?")
    if triad == "?":
        return ""
    if not seventh:
        return triad
    table = {("", 11): "maj7", ("", 10): "7", ("m", 10): "m7", ("m", 11): "mMaj7", ("dim", 10): "m7b5",
             ("dim", 9): "dim7", ("aug", 11): "maj7#5", ("aug", 10): "7#5"}
    q = table.get((triad, sev), triad)
    return q if q in QUALITIES else triad


def diatonic_chords(tonic: Note, mode: str, seventh: bool) -> list[Chord]:
    notes = scale_notes(tonic, mode)
    return [Chord(notes[d], stacked_quality(tonic, mode, d, seventh)) for d in range(7)]


# ---------------------------------------------------------------------------
# Reharmonization
# ---------------------------------------------------------------------------
class Item:
    """One source chord analysed against the key: semitone offset from the tonic plus quality."""

    def __init__(self, src: str | None, off: int, quality: str):
        self.src, self.off, self.quality = src, off, quality


def _mk(tonic: Note, off: int, quality: str, bass_off: int | None = None) -> Chord:
    d, a = OFFSET_DEGREE[off % 12]
    bass = None
    if bass_off is not None:
        bd, ba = OFFSET_DEGREE[bass_off % 12]
        bass = degree_note(tonic, bd, ba)
    return chord_on_degree(tonic, d, a, quality, bass)


def _to_seventh(q: str) -> str:
    return {"": "maj7", "m": "m7", "dim": "m7b5", "aug": "7#5", "sus4": "7sus4", "6": "maj7", "m6": "m7",
            "add9": "maj7", "madd9": "m7", "sus2": "maj7"}.get(q, q)


def _jazz(items: list[Item], tonic: Note, minor: bool, tritone: bool) -> list[tuple[str | None, Chord, str]]:
    rows: list[tuple[str | None, Chord, str]] = []
    n = len(items)
    for i, it in enumerate(items):
        nxt = items[i + 1].off if i + 1 < n else None
        prv = items[i - 1].off if i > 0 else None
        off, q = it.off, it.quality
        if off == 5 and nxt == 7 and not minor:
            rows.append((it.src, _mk(tonic, 2, "m7"), "ii7 replaces IV: same predominant function, makes a ii-V"))
        elif off == 2 and q in ("", "m", "m7", "7"):
            rows.append((it.src, _mk(tonic, 2, "m7b5" if minor else "m7"),
                         "ii" + ("ø7" if minor else "7") + " with its 7th"))
        elif off == 7:
            pre = prv in (2, 5)
            if not pre and i > 0 and prv != 7 and not minor:
                rows.append((None, _mk(tonic, 2, "m7"), "inserted ii7 to lead into V7 (ii-V)"))
            if not pre and i > 0 and prv != 7 and minor:
                rows.append((None, _mk(tonic, 2, "m7b5"), "inserted iiø7 to lead into V7 (minor ii-V)"))
            dom = "7b9" if minor else "7"
            if tritone and nxt == 0:
                rows.append((it.src, _mk(tonic, 1, "7"), "tritone sub: bII7 shares V7's 3rd and 7th, bass slides down to I"))
            else:
                rows.append((it.src, _mk(tonic, 7, dom), "dominant 7th" + (" with b9 for minor-key pull" if minor else "")))
        elif off == 0:
            rows.append((it.src, _mk(tonic, 0, "m7" if minor else "maj7"), "tonic with its 7th colour"))
        elif off == 11 and q in ("dim", "m7b5", ""):
            rows.append((it.src, _mk(tonic, 11, "m7b5"), "vii° becomes half-diminished 7th (V7/rootless colour)"))
        else:
            tq = q if any(s == 6 for s, _ in QUALITIES[q]) else _to_seventh(q)
            if off == 5 and minor:
                tq = "m7"
            rows.append((it.src, _mk(tonic, off, tq), "add the 7th" if tq != q else "already a 7th chord"))
    if items and items[-1].off in (7, 11):
        rows.append((None, _mk(tonic, 0, "m7" if minor else "maj7"), "resolve the dominant: closing ii-V-I"))
    return rows


def _blues(items: list[Item], tonic: Note, minor: bool) -> list[tuple[str | None, Chord, str]]:
    rows = []
    for it in items:
        minor_chord = it.quality in ("m", "m7", "m6", "m9", "dim", "m7b5") or (minor and it.off in (0, 5))
        if it.off in (0, 5, 7) and not (minor_chord and it.off != 7) or it.off == 7:
            tq = "7" if it.off == 7 or not minor_chord else "m7"
            if it.quality in ("7", "9", "13", "7b9", "7#9"):
                tq = it.quality
            why = "dominant 7th on the I/IV/V of a blues" if tq != "m7" else "minor-blues m7"
        else:
            tq = "m7" if minor_chord else "7"
            why = "chromatic neighbour as a dominant 7th" if tq == "7" else "minor 7th colour"
        rows.append((it.src, _mk(tonic, it.off, tq), why))
    return rows


def _blues_sketch(tonic: Note, minor: bool) -> list[str]:
    def c(off: int, q: str) -> str:
        return _mk(tonic, off, q).symbol()
    one, four, five = ("m7", "m7", "7") if minor else ("7", "7", "7")
    if minor:
        bars = [c(0, one)] * 4 + [c(5, four)] * 2 + [c(0, one)] * 2 + [c(8, "7"), c(7, five), c(0, one), c(7, five)]
    else:
        bars = [c(0, one)] * 4 + [c(5, four)] * 2 + [c(0, one)] * 2 + [c(7, five), c(5, four), c(0, one), c(7, five)]
    return bars


def _gospel(items: list[Item], tonic: Note, minor: bool) -> list[tuple[str | None, Chord, str]]:
    rows: list[tuple[str | None, Chord, str]] = []
    n = len(items)
    for i, it in enumerate(items):
        nxt = items[i + 1].off if i + 1 < n else None
        prv = items[i - 1].off if i > 0 else None
        off, q = it.off, it.quality
        if nxt == 2 and off != 9 and prv != 9:
            rows.append((None, _mk(tonic, 9, "7"), "secondary dominant V7/ii leads into ii"))
        elif nxt == 9 and off != 4:
            rows.append((None, _mk(tonic, 4, "7"), "secondary dominant V7/vi leads into vi"))
        elif nxt == 7 and off not in (2, 5, 7):
            rows.append((None, _mk(tonic, 2, "7"), "secondary dominant V7/V leads into V"))
        if off == 0:
            rows.append((it.src, _mk(tonic, 0, "maj7" if not minor and q != "7" else ("m7" if minor else q)),
                         "tonic with a warm 7th" if not minor else "minor tonic with its 7th"))
            if nxt == 2:
                rows.append((None, _mk(tonic, 1, "dim7"), "passing diminished 7th I to ii (#i°7)"))
        elif off == 5:
            iv_minor = minor or it.quality.startswith("m")
            rows.append((it.src, _mk(tonic, 5, "m7" if iv_minor else "maj7"), "IV with a 7th for the plagal sway"))
            if nxt == 7:
                rows.append((None, _mk(tonic, 6, "dim7"), "passing diminished 7th IV to V (#iv°7)"))
        elif off == 7:
            if nxt == 0 and not minor:
                rows.append((it.src, _mk(tonic, 5, "", bass_off=7), "IV/V (IV over the dominant bass) pushes into I"))
            else:
                rows.append((it.src, _mk(tonic, 7, "7"), "dominant 7th"))
        elif off in (2, 4, 9):
            rows.append((it.src, _mk(tonic, off, "m7"), "minor 7th"))
        else:
            rows.append((it.src, _mk(tonic, off, _to_seventh(q)), "add the 7th"))
    return rows


def _bossa(items: list[Item], tonic: Note, minor: bool) -> list[tuple[str | None, Chord, str]]:
    rows: list[tuple[str | None, Chord, str]] = []
    n = len(items)
    for i, it in enumerate(items):
        nxt = items[i + 1].off if i + 1 < n else None
        off = it.off
        if nxt == 9 and off not in (4, 9):
            rows.append((None, _mk(tonic, 4, "7b9"), "ii-V chain step: III7b9 into vi"))
        if off == 0:
            rows.append((it.src, _mk(tonic, 0, "m9" if minor else "maj9"), "tonic with 9th colour"))
        elif off == 2:
            rows.append((it.src, _mk(tonic, 2, "m7b5" if minor else "m9"), "ii with 9th colour"))
        elif off == 5:
            minor_iv = minor or it.quality.startswith("m")
            rows.append((it.src, _mk(tonic, 5, "m6" if minor_iv else "maj7"),
                         "minor iv6 colour" if minor_iv else "IV with its maj7 colour"))
        elif off == 7:
            if (i > 0 and items[i - 1].off not in (2, 5)) and not minor:
                rows.append((None, _mk(tonic, 2, "m7"), "ii-V chain: ii7 into V"))
            rows.append((it.src, _mk(tonic, 7, "13" if not minor else "7b9"), "dominant with 13th colour" if not minor else "dominant 7b9"))
        elif off in (4, 9):
            rows.append((it.src, _mk(tonic, off, "m9" if off == 9 else "m7"), "minor 9th/7th colour"))
        else:
            rows.append((it.src, _mk(tonic, off, _to_seventh(it.quality)), "add the 7th"))
    return rows


def _pop(items: list[Item], tonic: Note, minor: bool) -> list[tuple[str | None, Chord, str]]:
    rows = []
    for it in items:
        off, q = it.off, it.quality
        if off == 2 and not minor:
            rows.append((it.src, _mk(tonic, 5, ""), "IV replaces ii: same function, stronger loop"))
        elif off == 4 and not minor:
            rows.append((it.src, _mk(tonic, 9, "m"), "vi replaces iii: diatonic, more common in pop"))
        elif off == 11:
            rows.append((it.src, _mk(tonic, 7, ""), "V replaces vii°"))
        else:
            minor_triad = q in ("m", "m6", "m7", "m9", "madd9", "mMaj7", "m11", "m13", "dim", "m7b5")
            tq = "m" if minor_triad or (minor and off in (0, 5)) else ""
            rows.append((it.src, _mk(tonic, off, tq), "diatonic triad" + (" (7th/extension removed)" if q not in ("", "m") else "")))
    return rows


def reharmonize(tonic: Note, mode: str, chords: list[Chord], style: str, tritone: bool = False) -> dict[str, Any]:
    minor = mode in ("minor", "harmonic minor", "melodic minor", "dorian", "phrygian", "locrian")
    items = [Item(c.symbol(), (c.root[1] - tonic[1]) % 12, c.quality) for c in chords]
    if style == "jazz":
        rows = _jazz(items, tonic, minor, tritone)
    elif style == "blues":
        rows = _blues(items, tonic, minor)
    elif style == "gospel":
        rows = _gospel(items, tonic, minor)
    elif style == "bossa-nova":
        rows = _bossa(items, tonic, minor)
    elif style == "pop":
        rows = _pop(items, tonic, minor)
    else:
        raise ValueError(f"unknown style {style!r} (jazz|blues|gospel|bossa-nova|pop)")
    out: dict[str, Any] = {
        "style": style, "key": f"{spell(tonic)} {mode}",
        "rows": [{"source": s or "(new)", "target": c.symbol(), "reason": r} for s, c, r in rows],
        "progression": [c.symbol() for _, c, _ in rows],
    }
    if style == "blues":
        out["sketch_12_bar"] = _blues_sketch(tonic, minor)
    if style == "pop" and len(chords) >= 4:
        shape = [_mk(tonic, o, "m" if o == 9 else "").symbol() for o in (9, 5, 0, 7)]
        out["loop_shape"] = shape
    return out


# ---------------------------------------------------------------------------
# Tool mode
# ---------------------------------------------------------------------------
def _key_from_args(key_text: str, mode: str | None) -> tuple[Note, str]:
    return parse_key(key_text, mode)


def _emit(obj: Any, as_json: bool, text: str) -> int:
    sys.stdout.write((json.dumps(obj, indent=2) if as_json else text) + "\n")
    return 0


def _table(rows: list[list[str]], header: list[str]) -> str:
    widths = [max(len(str(r[i])) for r in [header] + rows) for i in range(len(header))]
    fmt = lambda r: " | ".join(str(c).ljust(widths[i]) for i, c in enumerate(r)).rstrip()  # noqa: E731
    return "\n".join([fmt(header), "-+-".join("-" * w for w in widths)] + [fmt(r) for r in rows])


def _chords_in(tokens: list[str], tonic: Note) -> list[Chord]:
    out = []
    for t in tokens:
        out.append(roman_to_chord(t, tonic) if ROMAN_RE.match(t) and not re.match(r"^[A-G]", t) else parse_chord(t))
    return out


def tool_main(argv: list[str]) -> int:
    merged: list[str] = []
    for i, tok in enumerate(argv):
        if i > 0 and argv[i - 1] == "--by" and tok.startswith("-"):
            merged[-1] = "--by=" + tok
        else:
            merged.append(tok)
    p = argparse.ArgumentParser(prog="chord_tools.py", description="Chord and scale tools for music-team.")
    sub = p.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("scale", help="spell a scale")
    s.add_argument("tonic")
    s.add_argument("mode", nargs="+")
    c = sub.add_parser("chord", help="spell a chord symbol")
    c.add_argument("symbol")
    t = sub.add_parser("transpose", help="transpose chord symbols")
    t.add_argument("chords", nargs="+")
    t.add_argument("--by", metavar="INTERVAL", help="P5, m3, M2, ...; prefix - for down (use --by=-M2)")
    t.add_argument("--to", metavar="KEY")
    t.add_argument("--from-key", metavar="KEY", help="source key for --to (default: the first chord's root)")
    d = sub.add_parser("diatonic", help="diatonic triads and 7ths of a key")
    d.add_argument("key", nargs="+", help="e.g. Eb, or A minor")
    d.add_argument("--mode")
    r = sub.add_parser("roman", help="chord symbols -> Roman numerals")
    r.add_argument("key")
    r.add_argument("chords", nargs="+")
    r.add_argument("--mode")
    h = sub.add_parser("reharmonize", help="idiomatic chord substitution")
    h.add_argument("key")
    h.add_argument("chords", nargs="+")
    h.add_argument("--style", required=True, choices=["jazz", "blues", "gospel", "bossa-nova", "pop"])
    h.add_argument("--mode")
    h.add_argument("--tritone", action="store_true", help="jazz: tritone-substitute V7 before I")
    for sp in (s, c, t, d, r, h):
        sp.add_argument("--json", action="store_true")
    args = p.parse_args(merged)
    try:
        return _tool_dispatch(args)
    except ValueError as exc:
        sys.stderr.write(f"chord_tools: error: {exc}\n")
        return 3


def _tool_dispatch(a: argparse.Namespace) -> int:
    if a.cmd == "scale":
        tonic, mode = parse_key(a.tonic + " " + " ".join(a.mode))
        names = [spell(n) for n in scale_notes(tonic, mode)]
        return _emit({"tonic": spell(tonic), "mode": mode, "notes": names}, a.json, f"{spell(tonic)} {mode}: " + " ".join(names))
    if a.cmd == "chord":
        ch = parse_chord(a.symbol)
        return _emit({"symbol": ch.symbol(), "notes": ch.spelling()}, a.json, f"{ch.symbol()}: " + " ".join(ch.spelling()))
    if a.cmd == "transpose":
        if bool(a.by) == bool(a.to):
            raise ValueError("give exactly one of --by or --to")
        chords = [parse_chord(x) for x in a.chords]
        if a.by:
            direction, steps, semis = parse_interval(a.by)
        else:
            src = parse_key(a.from_key)[0] if a.from_key else chords[0].root
            dst = parse_key(a.to)[0]
            direction, steps, semis = 1, (dst[0] - src[0]) % 7, (dst[1] - src[1]) % 12
        out = [transpose_chord(x, direction, steps, semis).symbol() for x in chords]
        return _emit({"source": [x.symbol() for x in chords], "result": out}, a.json, " ".join(out))
    if a.cmd == "diatonic":
        tonic, mode = _key_from_args(" ".join(a.key), a.mode)
        tri, sev = diatonic_chords(tonic, mode, False), diatonic_chords(tonic, mode, True)
        rows = [[chord_to_roman(tri[i], tonic), tri[i].symbol(), sev[i].symbol(), " ".join(sev[i].spelling())] for i in range(7)]
        obj = {"key": f"{spell(tonic)} {mode}", "triads": [x.symbol() for x in tri], "sevenths": [x.symbol() for x in sev]}
        return _emit(obj, a.json, f"{spell(tonic)} {mode}\n" + _table(rows, ["numeral", "triad", "7th", "notes"]))
    if a.cmd == "roman":
        tonic, mode = _key_from_args(a.key, a.mode)
        rows, nums, flagged = [], [], []
        for tok in a.chords:
            ch = parse_chord(tok)
            rn, dia = chord_to_roman(ch, tonic), is_diatonic(ch, tonic, mode)
            nums.append(rn)
            rows.append([ch.symbol(), rn, "diatonic" if dia else "NON-DIATONIC"])
            if not dia:
                flagged.append(ch.symbol())
        obj = {"key": f"{spell(tonic)} {mode}", "romans": nums, "non_diatonic": flagged}
        return _emit(obj, a.json, _table(rows, ["chord", "roman", "status"]) + "\n" + " ".join(nums))
    if a.cmd == "reharmonize":
        tonic, mode = _key_from_args(a.key, a.mode)
        res = reharmonize(tonic, mode, _chords_in(a.chords, tonic), a.style, a.tritone)
        lines = [f"{res['style']} in {res['key']}", _table([[x["source"], x["target"], x["reason"]] for x in res["rows"]],
                                                          ["source", "target", "reason"]),
                 "Result: " + " | ".join(res["progression"])]
        if "sketch_12_bar" in res:
            lines.append("12-bar sketch: " + " | ".join(res["sketch_12_bar"]))
        if "loop_shape" in res:
            lines.append("Loop shape (vi-IV-I-V): " + " | ".join(res["loop_shape"]))
        return _emit(res, a.json, "\n".join(lines))
    raise ValueError(f"unknown command {a.cmd}")


# ---------------------------------------------------------------------------
# Gate mode
# ---------------------------------------------------------------------------
class ChordLine:
    def __init__(self, line_no: int, romans: list[str], concert: list[str] | None):
        self.line_no, self.romans, self.concert = line_no, romans, concert


def _cells(line: str) -> list[str]:
    inner = line.strip()
    if inner.startswith(">"):
        inner = inner[1:].strip()
    return [c.strip() for c in inner.strip("|").split("|")]


def parse_chords_md(text: str) -> tuple[str | None, list[tuple[str, list[ChordLine]]]]:
    """Return (header key string or None, [(section label, [ChordLine])])."""
    header = gc.parse_header_keys(text)
    key = header.get("key")
    sections: list[tuple[str, list[ChordLine]]] = []
    cur: list[ChordLine] | None = None
    last_roman = last_concert = None
    for no, raw in enumerate(text.splitlines(), 1):
        s = raw.strip()
        m = gc.SECTION_TAG.match(s)
        if m:
            cur = []
            sections.append((m.group(1).strip(), cur))
            continue
        if cur is None or not s or s.startswith("#"):
            continue
        if s.startswith("|"):
            cells = []
            for c in _cells(s):
                if c == "%":
                    if last_roman is None:
                        raise ValueError(f"line {no}: '%' with no previous cell")
                    c = last_roman
                if not c:
                    raise ValueError(f"line {no}: empty cell")
                last_roman = c
                cells.append(c)
            cur.append(ChordLine(no, cells, None))
        elif s.startswith(">"):
            if not cur or cur[-1].concert is not None:
                raise ValueError(f"line {no}: concert line without a preceding Roman line")
            cells = []
            for c in _cells(s):
                if c == "%":
                    if last_concert is None:
                        raise ValueError(f"line {no}: '%' with no previous concert cell")
                    c = last_concert
                last_concert = c
                cells.append(c)
            cur[-1].concert = cells
        else:
            raise ValueError(f"line {no}: unrecognised line {s[:40]!r}")
    return (str(key) if key is not None else None), sections


_CADENCES = {(7, 0), (5, 0), (7, 9), (10, 0), (11, 0)}


def gate_main(args: argparse.Namespace, config: dict[str, Any], res: gc.GateResult) -> gc.GateResult:
    paths = args.paths
    chords_path = gc.file_named(paths, "chords.md") or next(
        (p for p in paths if Path(p).suffix == ".md" and Path(p).name.lower() not in ("structure.md", "brief.md", "lyrics.md")), None)
    if not chords_path:
        return res.error("no chords.md path given")
    genre = gc.resolve_genre(args.genre, paths)
    min_ratio = gc.resolve_threshold("diatonic_min_ratio", config, genre, args.diatonic_min, kind=float)
    res.thresholds["diatonic_min_ratio"] = min_ratio
    header_key, sections = parse_chords_md(gc.read_text(chords_path))

    key_text = args.key
    struct_path = gc.file_named(paths, "structure.md")
    if not key_text and struct_path:
        sh = gc.parse_header_keys(gc.read_text(struct_path))
        if sh.get("key"):
            key_text = f"{sh['key']} {sh.get('mode', 'major')}"
    if not key_text:
        key_text = header_key
    if not key_text:
        return res.error("no key: chords.md has no 'key:' header and no structure.md or --key was given", "chords.md:key")
    tonic, mode = parse_key(key_text)
    hk = parse_key(header_key) if header_key else None
    if hk and (hk[0][1], hk[1]) != (tonic[1], mode):
        res.violate("chords.md:key", "chords.md key header differs from the song key", header_key, f"{spell(tonic)} {mode}")
    res.metrics["key"] = f"{spell(tonic)} {mode}"

    total = dia = 0
    concert_out: list[str] = []
    for label, lines in sections:
        flat: list[Chord] = []
        for idx, ln in enumerate(lines, 1):
            parsed = []
            for col, cell in enumerate(ln.romans, 1):
                try:
                    parsed.append(roman_to_chord(cell, tonic))
                except ValueError as exc:
                    raise ValueError(f"{label}:{idx}:{col}: {exc}") from None
            for col, ch in enumerate(parsed, 1):
                total += 1
                if is_diatonic(ch, tonic, mode):
                    dia += 1
                else:
                    res.warn(f"{label}:{idx}:{col}", "non-diatonic (borrowed or chromatic) chord",
                             f"{ln.romans[col - 1]} = {ch.symbol()}", f"{spell(tonic)} {mode}")
            flat.extend(parsed)
            if ln.concert is not None:
                if len(ln.concert) != len(parsed):
                    res.violate(f"{label}:{idx}", "concert line cell count differs from Roman line",
                                len(ln.concert), len(parsed))
                else:
                    for col, (cell, ch) in enumerate(zip(ln.concert, parsed), 1):
                        try:
                            got = parse_chord(cell)
                        except ValueError as exc:
                            raise ValueError(f"{label}:{idx}:{col}: {exc}") from None
                        if got.pcs() != ch.pcs() or got.root[1] != ch.root[1]:
                            res.violate(f"{label}:{idx}:{col}", "concert chord does not match its Roman numeral",
                                        cell, ch.symbol())
            concert_out.append(f"{label}:{idx} | " + " | ".join(c.symbol() for c in parsed))
        for a, b in zip(flat, flat[1:]):
            gap = (b.root[1] - a.root[1]) % 12
            if a.triad_root_position() and b.triad_root_position() and gap in (1, 2, 10, 11):
                res.warn(label, "adjacent root-position triads move by step: check for parallel fifths",
                         f"{a.symbol()} -> {b.symbol()}", None)
        if len(flat) >= 2:
            pair = ((flat[-2].root[1] - tonic[1]) % 12, (flat[-1].root[1] - tonic[1]) % 12)
            if pair not in _CADENCES:
                res.warn(label, "section ends without a V-I, IV-I, V-vi or bVII-I cadence",
                         f"{flat[-2].symbol()} -> {flat[-1].symbol()}", None)
    ratio = (dia / total) if total else 0.0
    res.metrics.update({"sections": len(sections), "chords": total, "diatonic_chords": dia,
                        "diatonic_ratio": round(ratio, 3), "concert": concert_out})
    res.metrics["warnings"] = len(res.warnings)
    if total == 0:
        res.violate("chords.md", "no chord cells found", 0, ">= 1")
    elif ratio < min_ratio:
        res.violate("chords.md:diatonic_ratio", "diatonic ratio below threshold", round(ratio, 3), min_ratio)
    return res


def gate_args(p: argparse.ArgumentParser) -> None:
    p.add_argument("--check", action="store_true", help="gate mode (default when no subcommand is given)")
    p.add_argument("--key", metavar="KEY", help="override the key (default: structure.md, else chords.md header)")
    p.add_argument("--diatonic-min", type=float, metavar="RATIO", help="override quality.diatonic_min_ratio")
    p.add_argument("--selftest", action="store_true", help="run the built-in self-test and exit")


# ---------------------------------------------------------------------------
# Self-test
# ---------------------------------------------------------------------------
def selftest() -> int:
    failures: list[str] = []

    def eq(name: str, got: Any, want: Any) -> None:
        if got != want:
            failures.append(f"{name}: got {got!r}, want {want!r}")

    def scale(t: str, m: str) -> list[str]:
        tn, md = parse_key(t, m)
        return [spell(n) for n in scale_notes(tn, md)]

    eq("C major", scale("C", "major"), list("CDEFGAB"))
    eq("F major has Bb", scale("F", "major"), ["F", "G", "A", "Bb", "C", "D", "E"])
    eq("G major has F#", scale("G", "major")[6], "F#")
    eq("D minor has Bb", scale("D", "minor")[5], "Bb")
    eq("Am7", parse_chord("Am7").spelling(), ["A", "C", "E", "G"])
    eq("Fmaj7", parse_chord("Fmaj7").spelling(), ["F", "A", "C", "E"])
    eq("G7", parse_chord("G7").spelling(), ["G", "B", "D", "F"])
    eq("Bb7", parse_chord("Bb7").spelling(), ["Bb", "D", "F", "Ab"])
    eq("C/E", parse_chord("C/E").spelling(), ["E", "C", "G"])
    d, s, x = parse_interval("P5")
    eq("up P5", [transpose_chord(parse_chord(c), d, s, x).symbol() for c in ("C", "F", "G")], ["G", "C", "D"])
    tonic, mode = parse_key("Eb")
    eq("Eb diatonic 7ths", [c.symbol() for c in diatonic_chords(tonic, mode, True)],
       ["Ebmaj7", "Fm7", "Gm7", "Abmaj7", "Bb7", "Cm7", "Dm7b5"])
    tonic, mode = parse_key("C")
    jz = reharmonize(tonic, mode, [parse_chord(c) for c in ("C", "C", "F", "G")], "jazz")["progression"]
    joined = " ".join(jz)
    eq("jazz ii-V-I", "Dm7 G7 Cmaj7" in joined, True)
    eq("jazz all 7ths", all(parse_chord(c).has_seventh() for c in jz), True)
    eq("roman C: Am F C G", " ".join(chord_to_roman(parse_chord(c), tonic) for c in ("Am", "F", "C", "G")), "vi IV I V")
    eq("roman->chord", [roman_to_chord(r, parse_key("D")[0]).symbol() for r in ("I", "V", "vi", "IV", "bVII")],
       ["D", "A", "Bm", "G", "C"])
    sample = "key: C major\n\n[Verse 1]\n| I | vi | IV | V |\n> | C | Am | F | G |\n"
    import tempfile
    with tempfile.TemporaryDirectory() as tmp:
        f = Path(tmp) / "chords.md"
        f.write_text(sample, encoding="utf-8")
        g = gc.GateResult("chord_tools")
        g = gate_main(argparse.Namespace(paths=[str(f)], genre=None, diatonic_min=None, key=None), {}, g)
        eq("gate PASS", g.status, gc.PASS)
    if failures:
        sys.stdout.write("chord_tools selftest: FAIL\n" + "\n".join("  " + f for f in failures) + "\n")
        return 1
    sys.stdout.write("chord_tools selftest: PASS\n")
    return 0


def main(argv: list[str] | None = None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    if argv and argv[0] in ("scale", "chord", "transpose", "diatonic", "roman", "reharmonize"):
        return tool_main(argv)
    if "--selftest" in argv:
        return selftest()
    return gc.run("chord_tools.py", "Validate chords.md: spelling, key, diatonic ratio.", gate_args, gate_main, argv)


if __name__ == "__main__":
    sys.exit(main())
