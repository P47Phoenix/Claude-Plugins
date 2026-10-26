#!/usr/bin/env python3
"""abc_common.py - shared tokenizer for the ABC 2.1 subset used by ``melody.abc``
(artifact-formats.md) and consumed by ``abc_validate.py`` and ``midi_export.py``.

``parse_abc(text)`` returns::

    {"headers": {"X": "1", "T": ..., "M": "4/4", "L": "1/8", "Q": "1/4=118", "K": "D", ...},
     "header_counts": {"X": 1, ..., "V": 0},
     "key": "D", "mode": "major", "time_sig": "4/4", "bpm": 118, "unit_length": Fraction(1, 8),
     "sections": [{"label": "Verse 1", "line": 7,
                   "bars": [{"line": 8, "notes": [{"midi": 62, "dur_units": Fraction(2), "is_rest": False,
                                                   "tied_from_prev": False}, ...],
                             "chords": ["D"], "w_tokens": [{"kind": "syl"|"ext"|"skip", "text": "num"}, ...],
                             "has_w": True}, ...]}, ...]}

Subset: notes ``[\\^_=]?[A-Ga-g][,']*<dur>``; rests ``z``/``x`` with durations; bar
lines ``|``, ``||``, ``|]``, ``|:``, ``:|``, ``[|``; ties ``-`` after a note: when
the next note (across a bar line or a line break, with no rest between) has the
same pitch it is one sounding head with the previous note, so it carries
``tied_from_prev`` and is NOT counted as a note head for lyric alignment; a
``-`` between different pitches is a slur and the next note is a new head;
broken rhythm ``>``/``<``; tuplets ``(n`` (reset at the bar line; a nested
``(n`` raises); slurs ``(`` ``)``; chord symbols in quotes are ignored for the
melody but kept per bar in ``chords``; decorations ``!..!``/``+..+``, grace
notes ``{..}``, inline fields ``[K:..]`` and repeat endings ``[1``/``|1`` are
ignored; ``%`` comments are ignored except ``%%section <Label>``; a ``w:`` line
attaches to the preceding music line and a trailing ``\\`` continues it on the
next ``w:`` line. Key-signature accidentals from ``K:`` (major/minor/modes) are
applied; an explicit accidental persists for the rest of its bar. Durations are
in units of ``L:``. A leading UTF-8 BOM is stripped.

Any character outside the subset, a non-integer ``X:``, a ``w:`` line with no
preceding music line, a second ``w:`` for one music line, or a tie left
dangling at a ``%%section`` or at end of file raises ``AbcParseError`` with the
1-based line number. Stdlib only; ``python -I`` safe.
"""
from __future__ import annotations

import re
from fractions import Fraction
from typing import Any

_SHARPS = "FCGDAEB"
_FLATS = "BEADGCF"
_MAJOR_SHARPS = {"C": 0, "G": 1, "D": 2, "A": 3, "E": 4, "B": 5, "F#": 6, "C#": 7,
                 "F": -1, "Bb": -2, "Eb": -3, "Ab": -4, "Db": -5, "Gb": -6, "Cb": -7}
_MODE_OFFSET = {"major": 0, "ionian": 0, "minor": -3, "aeolian": -3, "dorian": -2,
                "mixolydian": -1, "lydian": 1, "phrygian": -4, "locrian": -5}
_MODE_ABBREV = {"m": "minor", "min": "minor", "maj": "major", "dor": "dorian", "mix": "mixolydian",
                "lyd": "lydian", "phr": "phrygian", "loc": "locrian", "aeo": "aeolian", "ion": "ionian"}
_BASE_MIDI = {"C": 60, "D": 62, "E": 64, "F": 65, "G": 67, "A": 69, "B": 71}
PC = {"C": 0, "D": 2, "E": 4, "F": 5, "G": 7, "A": 9, "B": 11}          # letter -> pitch class
SHARP_NAMES = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
FLAT_NAMES = ["C", "Db", "D", "Eb", "E", "F", "Gb", "G", "Ab", "A", "Bb", "B"]
MAJOR_SHARPS = _MAJOR_SHARPS
MODE_OFFSET = _MODE_OFFSET

REQUIRED_HEADERS = ("X", "T", "M", "L", "Q", "K")
SECTION_RE = re.compile(r"^%%section\s+(.+?)\s*$")
_FIELD_RE = re.compile(r"^([A-Za-z]):(.*)$")
_NOTE_RE = re.compile(r"(\^+|_+|=)?([A-Ga-g])([,']*)")
_DUR_RE = re.compile(r"(\d*)(/*)(\d*)")
_TUPLET_RATIO = {2: Fraction(3, 2), 3: Fraction(2, 3), 4: Fraction(3, 4), 5: Fraction(2, 5),
                 6: Fraction(2, 6), 7: Fraction(2, 7), 8: Fraction(3, 8), 9: Fraction(2, 9)}


class AbcParseError(ValueError):
    def __init__(self, message: str, line: int | None = None):
        super().__init__(message)
        self.line = line


# ---------------------------------------------------------------------------
# Keys and pitches
# ---------------------------------------------------------------------------
def parse_abc_key(value: str) -> tuple[str, str]:
    """``'D'`` -> ('D', 'major'); ``'Dm'``/``'D minor'``/``'Dmin'`` -> ('D', 'minor'); ``'D dorian'`` -> ('D', 'dorian')."""
    m = re.match(r"^\s*([A-Ga-g][#b]?)\s*([A-Za-z]*)", value)
    if not m:
        return value.strip(), ""
    tonic = m.group(1)[0].upper() + m.group(1)[1:]
    word = m.group(2).lower()
    if not word:
        return tonic, "major"
    if word in _MODE_OFFSET:
        return tonic, word
    return tonic, _MODE_ABBREV.get(word[:3], word)


def key_accidentals(tonic: str, mode: str) -> dict[str, int]:
    """Letter -> semitone offset implied by the key signature."""
    n = _MAJOR_SHARPS.get(tonic, 0) + _MODE_OFFSET.get(mode, 0)
    acc: dict[str, int] = {}
    if n > 0:
        for letter in _SHARPS[:n]:
            acc[letter] = 1
    elif n < 0:
        for letter in _FLATS[:-n]:
            acc[letter] = -1
    return acc


def abc_note_to_midi(token: str, key_acc: dict[str, int], bar_acc: dict[str, int] | None = None) -> int:
    """``'^F,'`` -> 66 etc. Explicit accidental > bar accidental > key signature."""
    m = _NOTE_RE.fullmatch(token.strip())
    if not m:
        raise AbcParseError(f"not an ABC note: {token!r}")
    acc_s, letter, octs = m.groups()
    upper = letter.upper()
    midi = _BASE_MIDI[upper] + (12 if letter.islower() else 0)
    midi += 12 * octs.count("'") - 12 * octs.count(",")
    if acc_s:
        offset = 0 if acc_s == "=" else (len(acc_s) if acc_s[0] == "^" else -len(acc_s))
        if bar_acc is not None:
            bar_acc[letter] = offset
    elif bar_acc is not None and letter in bar_acc:
        offset = bar_acc[letter]
    else:
        offset = key_acc.get(upper, 0)
    return midi + offset


def parse_fraction(value: str) -> Fraction | None:
    """``'1/8'`` -> Fraction(1, 8); ``None`` when not ``n/d``."""
    m = re.match(r"^\s*(\d+)\s*/\s*(\d+)\s*$", value or "")
    if not m or int(m.group(2)) == 0:
        return None
    return Fraction(int(m.group(1)), int(m.group(2)))


def parse_time_sig(value: str) -> tuple[int, int] | None:
    """``'4/4'`` -> (4, 4); ``C`` -> (4, 4); ``C|`` -> (2, 2)."""
    v = (value or "").strip()
    if v == "C":
        return 4, 4
    if v == "C|":
        return 2, 2
    f = re.match(r"^(\d+)/(\d+)$", v)
    return (int(f.group(1)), int(f.group(2))) if f and int(f.group(2)) else None


def parse_tempo_bpm(value: str) -> int | None:
    """``'1/4=118'`` -> 118; ``'118'`` -> 118."""
    m = re.search(r"=\s*(\d+)", value or "")
    if m:
        return int(m.group(1))
    m = re.match(r"^\s*(\d+)\s*$", value or "")
    return int(m.group(1)) if m else None


def parse_tempo_beat(value: str) -> Fraction | None:
    """Beat unit of ``Q:``: ``'3/8=50'`` -> Fraction(3, 8); ``'118'`` -> None (no unit given)."""
    m = re.match(r'^\s*(?:"[^"]*"\s*)?(\d+)\s*/\s*(\d+)\s*=', value or "")
    if not m or int(m.group(2)) == 0:
        return None
    return Fraction(int(m.group(1)), int(m.group(2)))


# ---------------------------------------------------------------------------
# w: lines
# ---------------------------------------------------------------------------
def parse_w_line(text: str) -> list[list[dict[str, str]]]:
    """Split a ``w:`` body into bar groups of tokens (``|`` advances a bar).

    Token kinds: ``syl`` (a syllable; ``-`` splits a word, ``~`` is kept as a
    space inside the text), ``ext`` (``_``, extends the previous syllable over
    one more note), ``skip`` (``*``, one note without a syllable)."""
    groups: list[list[dict[str, str]]] = [[]]
    for chunk in text.replace("|", " | ").split():
        if chunk == "|":
            groups.append([])
            continue
        cur = groups[-1]
        if chunk == "*":
            cur.append({"kind": "skip", "text": ""})
            continue
        if set(chunk) <= {"_"}:
            cur.extend({"kind": "ext", "text": ""} for _ in chunk)
            continue
        trailing = len(chunk) - len(chunk.rstrip("_"))
        body = chunk.rstrip("_")
        pieces = [p for p in body.replace("\\-", "\x00").split("-")]
        for piece in pieces:
            piece = piece.replace("\x00", "-")
            if piece == "":
                continue
            if piece == "*":
                cur.append({"kind": "skip", "text": ""})
            else:
                cur.append({"kind": "syl", "text": piece.replace("~", " ")})
        cur.extend({"kind": "ext", "text": ""} for _ in range(trailing))
    return groups


# ---------------------------------------------------------------------------
# Music lines
# ---------------------------------------------------------------------------
def _new_bar(line_no: int) -> dict[str, Any]:
    return {"line": line_no, "notes": [], "chords": [], "w_tokens": [], "has_w": False}


def _read_duration(s: str, i: int) -> tuple[Fraction, int]:
    m = _DUR_RE.match(s, i)
    num, slashes, den = m.groups()
    if not num and not slashes:
        return Fraction(1), i
    n = int(num) if num else 1
    if slashes:
        d = int(den) if den else 2 ** len(slashes)
        if d == 0:
            raise AbcParseError("zero duration denominator")
        return Fraction(n, d), m.end()
    return Fraction(n), m.end()


def _tokenize_music(s: str, line_no: int, key_acc: dict[str, int], bars: list[dict[str, Any]],
                    open_bar: dict[str, Any] | None, pending_tie: int | None = None,
                    last_note: dict[str, Any] | None = None,
                    ) -> tuple[dict[str, Any] | None, int | None, dict[str, Any] | None]:
    """Append the bars of one music line to ``bars``.

    Returns ``(open_bar, pending_tie, last_note)``: the still-open bar (or None),
    the line number of a ``-`` not yet resolved by a following note (or None),
    and the last note seen, so that a tie carries across the line break."""
    bar = open_bar if open_bar is not None else _new_bar(line_no)
    bar_acc: dict[str, int] = {}
    i, n = 0, len(s)
    broken: Fraction | None = None      # multiplier for the next note from '>' / '<'
    tuplet_left, tuplet_ratio = 0, Fraction(1)
    in_bar = False                      # a note has been read in the current bar

    def close_bar() -> None:
        nonlocal bar, bar_acc, in_bar, tuplet_left, tuplet_ratio
        if bar["notes"] or bar["chords"]:
            bars.append(bar)
        bar = _new_bar(line_no)
        bar_acc = {}
        in_bar = False
        tuplet_left, tuplet_ratio = 0, Fraction(1)

    while i < n:
        ch = s[i]
        if ch in " \t":
            i += 1
            continue
        if ch == "\\" and s[i + 1:].strip() == "":
            break                                            # line continuation
        if ch == "%":
            break                                            # trailing comment
        if ch == '"':
            j = s.find('"', i + 1)
            if j < 0:
                raise AbcParseError("unterminated chord symbol", line_no)
            sym = s[i + 1:j].strip()
            if sym and sym[0] not in "^_<>@":
                bar["chords"].append(sym)
            i = j + 1
            continue
        if ch in "!+":
            j = s.find(ch, i + 1)
            if j < 0:
                raise AbcParseError(f"unterminated decoration {ch!r}", line_no)
            i = j + 1
            continue
        if ch == "{":
            j = s.find("}", i)
            if j < 0:
                raise AbcParseError("unterminated grace group", line_no)
            i = j + 1
            continue
        if ch == "[":
            if i + 2 < n and s[i + 1].isalpha() and s[i + 2] == ":":
                j = s.find("]", i)
                if j < 0:
                    raise AbcParseError("unterminated inline field", line_no)
                i = j + 1
                continue
            if i + 1 < n and s[i + 1] == "|":
                close_bar()
                i += 2
                continue
            if i + 1 < n and s[i + 1].isdigit():
                i += 2
                continue
            raise AbcParseError(f"unsupported '[' at column {i + 1}", line_no)
        if ch == "|" or ch == ":" and i + 1 < n and s[i + 1] in "|:":
            close_bar()
            while i < n and s[i] in "|:]":
                i += 1
            while i < n and s[i].isdigit():
                i += 1
            continue
        if ch == "(":
            if i + 1 < n and s[i + 1].isdigit():
                if tuplet_left > 0:
                    raise AbcParseError(f"nested tuplet at column {i + 1}", line_no)
                p = int(s[i + 1])
                tuplet_left, tuplet_ratio = p, _TUPLET_RATIO.get(p, Fraction(2, p))
                i += 2
                while i < n and s[i] in ":0123456789":           # (p:q:r
                    i += 1
                continue
            i += 1                                               # slur start
            continue
        if ch == ")":
            i += 1
            continue
        if ch == "-":
            if last_note is None or last_note["is_rest"]:
                raise AbcParseError(f"tie '-' without a preceding note at column {i + 1}", line_no)
            pending_tie = line_no
            i += 1
            continue
        if ch in "><":
            if last_note is None or not in_bar:
                raise AbcParseError(f"broken rhythm {ch!r} without a preceding note", line_no)
            k = 1
            while i + k < n and s[i + k] == ch:
                k += 1
            factor = Fraction(1, 2 ** k)
            if ch == ">":
                last_note["dur_units"] *= (2 - factor)
                broken = factor
            else:
                last_note["dur_units"] *= factor
                broken = 2 - factor
            i += k
            continue
        if ch in "zx":
            dur, i = _read_duration(s, i + 1)
            note = {"midi": None, "dur_units": dur, "is_rest": True, "tied_from_prev": False}
            pending_tie = None                                   # a rest breaks a tie
        else:
            m = _NOTE_RE.match(s, i)
            if not m:
                raise AbcParseError(f"unexpected character {ch!r} at column {i + 1}", line_no)
            midi = abc_note_to_midi(m.group(0), key_acc, bar_acc)
            dur, i = _read_duration(s, m.end())
            # a tie joins two notes of the same pitch; '-' between different pitches is a slur
            tied = pending_tie is not None and last_note is not None and last_note["midi"] == midi
            note = {"midi": midi, "dur_units": dur, "is_rest": False, "tied_from_prev": tied}
            pending_tie = None
        if broken is not None:
            note["dur_units"] *= broken
            broken = None
        if tuplet_left > 0:
            note["dur_units"] *= tuplet_ratio
            tuplet_left -= 1
        bar["notes"].append(note)
        last_note = note
        in_bar = True
    if bar["notes"] or bar["chords"]:
        return bar, pending_tie, last_note
    return None, pending_tie, last_note


# ---------------------------------------------------------------------------
# Whole file
# ---------------------------------------------------------------------------
def parse_abc(text: str) -> dict[str, Any]:
    if text.startswith("﻿"):
        text = text[1:]
    headers: dict[str, str] = {}
    counts: dict[str, int] = {}
    sections: list[dict[str, Any]] = []
    key_acc: dict[str, int] = {}
    in_body = False
    open_bar: dict[str, Any] | None = None
    pending_tie: int | None = None                        # line of a '-' awaiting its note
    last_note: dict[str, Any] | None = None
    last_line_bars: list[dict[str, Any]] | None = None   # bars of the previous music line
    w_buffer: str | None = None                           # w: text continued by a trailing backslash

    def section() -> dict[str, Any]:
        if not sections:
            sections.append({"label": "", "line": 0, "bars": []})
        return sections[-1]

    def flush_open() -> None:
        nonlocal open_bar
        if open_bar is not None:
            section()["bars"].append(open_bar)
            open_bar = None

    def check_dangling() -> None:
        if pending_tie is not None:
            raise AbcParseError("tie '-' with no following note", pending_tie)
        if w_buffer is not None:
            raise AbcParseError("w: line ends with '\\' but no w: line follows", w_line)

    w_line = 0
    for idx, raw in enumerate(text.splitlines(), 1):
        line = raw.rstrip()
        if not line.strip():
            continue
        sm = SECTION_RE.match(line.strip())
        if sm:
            check_dangling()
            flush_open()
            in_body = True
            sections.append({"label": sm.group(1), "line": idx, "bars": []})
            last_line_bars = None
            last_note = None
            continue
        if line.lstrip().startswith("%"):
            continue
        fm = _FIELD_RE.match(line.strip())
        if w_buffer is not None and not (fm and fm.group(1) == "w"):
            raise AbcParseError("w: line ends with '\\' but no w: line follows", w_line)
        if fm and (not in_body or fm.group(1) in "KVLMQwWTPIN"):
            field, value = fm.group(1), fm.group(2).strip()
            if field == "w":
                if last_line_bars is None:
                    raise AbcParseError("w: line without a preceding music line", idx)
                if any(b["has_w"] for b in last_line_bars):
                    raise AbcParseError("second w: line for one music line is not supported", idx)
                if w_buffer is not None:
                    value = w_buffer + " " + value
                    w_buffer = None
                if value.endswith("\\"):                      # continued on the next w: line
                    w_buffer, w_line = value[:-1].rstrip(), idx
                    continue
                groups = parse_w_line(value)
                if groups and not groups[-1]:
                    groups.pop()                              # trailing '|'
                for b in last_line_bars:
                    b["has_w"] = True
                for gi, group in enumerate(groups):
                    if gi < len(last_line_bars):
                        last_line_bars[gi]["w_tokens"].extend(group)
                    elif group:
                        last_line_bars[-1]["w_tokens"].extend(group)   # surplus -> counts against last bar
                continue
            counts[field] = counts.get(field, 0) + 1
            headers.setdefault(field, value)
            if field == "X" and not re.fullmatch(r"\d+", value):
                raise AbcParseError(f"X: must be an integer, got {value!r}", idx)
            if field == "K":
                tonic, mode = parse_abc_key(value)
                key_acc = key_accidentals(tonic, mode)
                in_body = True
            continue
        # music line
        in_body = True
        bars_here: list[dict[str, Any]] = []
        open_bar, pending_tie, last_note = _tokenize_music(line, idx, key_acc, bars_here, open_bar,
                                                           pending_tie, last_note)
        sec = section()
        sec["bars"].extend(bars_here)
        last_line_bars = bars_here + ([open_bar] if open_bar is not None else [])
        if open_bar is not None:                              # close unterminated bars at line end
            sec["bars"].append(open_bar)
            open_bar = None
    check_dangling()
    flush_open()

    key, mode = parse_abc_key(headers["K"]) if "K" in headers else (None, None)
    out: dict[str, Any] = {
        "headers": headers,
        "header_counts": counts,
        "key": key, "mode": mode,
        "time_sig": headers.get("M"),
        "bpm": parse_tempo_bpm(headers.get("Q", "")),
        "unit_length": parse_fraction(headers.get("L", "")) or Fraction(1, 8),
        "sections": sections,
    }
    return out


def note_heads(bar: dict[str, Any]) -> int:
    """Non-rest note heads in a bar; a tied-into note is not a new head."""
    return sum(1 for n in bar["notes"] if not n["is_rest"] and not n["tied_from_prev"])


def all_pitches(parsed: dict[str, Any]) -> list[int]:
    return [n["midi"] for s in parsed["sections"] for b in s["bars"] for n in b["notes"] if not n["is_rest"]]


__all__ = [
    "AbcParseError", "REQUIRED_HEADERS", "SECTION_RE", "PC", "SHARP_NAMES", "FLAT_NAMES", "MAJOR_SHARPS",
    "MODE_OFFSET", "parse_abc", "parse_abc_key", "key_accidentals", "abc_note_to_midi", "parse_fraction",
    "parse_time_sig", "parse_tempo_bpm", "parse_tempo_beat", "parse_w_line", "note_heads", "all_pitches",
]
