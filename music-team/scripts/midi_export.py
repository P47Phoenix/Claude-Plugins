#!/usr/bin/env python3
"""midi_export.py - hand-written Standard MIDI File (type 1) writer for the Stage 7c package.

Inputs
  chords.md    concert chords: lines prefixed ``>`` under ``[Label]`` tags, one bar per cell
  melody.abc   single-voice ABC subset (K/M/L/Q headers, notes, accidentals, octaves, lengths,
               rests, bar lines); anything unparsable is skipped and counted in ``metrics.warnings``
  structure.md optional header ``key/mode/bpm/time_sig`` (wins over ABC headers)

Tracks: 0 conductor (tempo, time signature, key signature) | 1 chords (block voicings, one chord
per bar cell) | 2 melody. A track is omitted when its input is absent; at least one of
``--chords`` / ``--melody`` is required.

Usage
  midi_export.py --out song.mid [--chords chords.md] [--melody melody.abc] [--structure structure.md] [--json]
  midi_export.py --check [--chords ...] [--melody ...] [--structure ...]    # gate mode, writes nothing
  midi_export.py melody.abc chords.md                                      # positional paths imply --check
  midi_export.py --selftest

Exit codes: 0 success/PASS | 1 FAIL (--check could not produce a valid file) | 3 unreadable input.
Stdlib only; safe under ``python -I``. No dependency on chord_tools.py.
"""
from __future__ import annotations

import contextlib
import io
import math
import re
import struct
import sys
from fractions import Fraction
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))
import gate_common as gc  # noqa: E402

PPQ = 480
DEFAULT_BPM = 120
CHORD_VELOCITY = 70
MELODY_VELOCITY = 90

_SHARPS_BY_TONIC = {"C": 0, "G": 1, "D": 2, "A": 3, "E": 4, "B": 5, "F#": 6, "C#": 7,
                    "F": -1, "Bb": -2, "Eb": -3, "Ab": -4, "Db": -5, "Gb": -6, "Cb": -7}
_MODE_SHIFT = {"major": 0, "ionian": 0, "minor": -3, "aeolian": -3, "dorian": -2,
               "mixolydian": -1, "lydian": 1, "phrygian": -4, "locrian": -5}
_MINOR_MODES = {"minor", "aeolian", "dorian", "phrygian", "locrian"}
_PC = {"C": 0, "D": 2, "E": 4, "F": 5, "G": 7, "A": 9, "B": 11}

# Chord-spelling table: suffix -> semitone intervals above the root.
CHORD_TABLE: dict[str, tuple[int, ...]] = {
    "": (0, 4, 7), "maj": (0, 4, 7), "M": (0, 4, 7), "m": (0, 3, 7), "min": (0, 3, 7), "-": (0, 3, 7),
    "dim": (0, 3, 6), "aug": (0, 4, 8), "+": (0, 4, 8),
    "sus2": (0, 2, 7), "sus4": (0, 5, 7), "sus": (0, 5, 7),
    "5": (0, 7), "6": (0, 4, 7, 9), "m6": (0, 3, 7, 9),
    "7": (0, 4, 7, 10), "maj7": (0, 4, 7, 11), "M7": (0, 4, 7, 11), "m7": (0, 3, 7, 10),
    "min7": (0, 3, 7, 10), "mmaj7": (0, 3, 7, 11), "dim7": (0, 3, 6, 9), "m7b5": (0, 3, 6, 10),
    "add9": (0, 4, 7, 14), "madd9": (0, 3, 7, 14), "9": (0, 4, 7, 10, 14), "maj9": (0, 4, 7, 11, 14),
    "m9": (0, 3, 7, 10, 14), "7sus4": (0, 5, 7, 10),
}
_CHORD_RE = re.compile(r"^([A-G])([#b]?)([^/]*)(?:/([A-G][#b]?))?$")


# ---------------------------------------------------------------------------
# Low-level MIDI encoding
# ---------------------------------------------------------------------------
def vlq(value: int) -> bytes:
    """MIDI variable-length quantity."""
    if value < 0:
        raise ValueError("negative delta time")
    out = [value & 0x7F]
    value >>= 7
    while value:
        out.append((value & 0x7F) | 0x80)
        value >>= 7
    return bytes(reversed(out))


def meta(delta: int, kind: int, data: bytes) -> bytes:
    return vlq(delta) + bytes([0xFF, kind]) + vlq(len(data)) + data


def track_chunk(events: list[tuple[int, int, bytes]], name: str, head: list[bytes] | None = None) -> bytes:
    """events: (abs_tick, order, raw_event_bytes); order 0 sorts before 1 at equal ticks
    (note-off before note-on). Returns an ``MTrk`` chunk ending in ``FF 2F 00``."""
    body = bytearray(meta(0, 0x03, name.encode("ascii", "replace")))
    for h in head or []:
        body += h
    last = 0
    for tick, _, raw in sorted(events, key=lambda e: (e[0], e[1])):
        body += vlq(tick - last) + raw
        last = tick
    body += meta(0, 0x2F, b"")
    return b"MTrk" + struct.pack(">I", len(body)) + bytes(body)


def note_events(channel: int, pitch: int, start: int, length: int, velocity: int) -> list[tuple[int, int, bytes]]:
    pitch = max(0, min(127, pitch))
    return [(start, 1, bytes([0x90 | channel, pitch, velocity])),
            (start + max(1, length), 0, bytes([0x80 | channel, pitch, 0]))]


def smf(tracks: list[bytes]) -> bytes:
    return b"MThd" + struct.pack(">IHHH", 6, 1, len(tracks), PPQ) + b"".join(tracks)


# ---------------------------------------------------------------------------
# Header resolution
# ---------------------------------------------------------------------------
def key_signature(tonic: str, mode: str) -> tuple[int, int]:
    """(sharps/flats -7..7, minor flag)."""
    n = _SHARPS_BY_TONIC.get(tonic, 0) + _MODE_SHIFT.get(mode, 0)
    return max(-7, min(7, n)), 1 if mode in _MINOR_MODES else 0


def parse_abc_key(value: str) -> tuple[str, str]:
    m = re.match(r"^\s*([A-G][#b]?)\s*([A-Za-z]*)", value)
    if not m:
        return "C", "major"
    word = m.group(2).lower()
    if not word or word in ("maj", "major", "ion"):
        return m.group(1), "major"
    if word in ("m", "min", "minor", "aeo"):
        return m.group(1), "minor"
    for full in _MODE_SHIFT:
        if full.startswith(word[:3]):
            return m.group(1), full
    return m.group(1), "major"


def key_acc(tonic: str, mode: str) -> dict[str, int]:
    n = _SHARPS_BY_TONIC.get(tonic, 0) + _MODE_SHIFT.get(mode, 0)
    acc: dict[str, int] = {}
    if n > 0:
        acc = {letter: 1 for letter in "FCGDAEB"[:n]}
    elif n < 0:
        acc = {letter: -1 for letter in "BEADGCF"[:-n]}
    return acc


# ---------------------------------------------------------------------------
# ABC subset parser
# ---------------------------------------------------------------------------
_ABC_TOKEN = re.compile(
    r"(?P<bar>\|\]|\[\||\|\||:\||\|:|\|)"
    r"|(?P<tuplet>\(\d)"
    r"|(?P<note>(?P<acc>\^{1,2}|_{1,2}|=)?(?P<letter>[A-Ga-g])(?P<oct>[,']*)(?P<len>\d*/*\d*))"
    r"|(?P<rest>[zx](?P<rlen>\d*/*\d*))"
    r"|(?P<ignore>[\s\-\.~\\\)\]:])"
    r"|(?P<other>.)")


def _length(spec: str) -> Fraction:
    m = re.fullmatch(r"(\d*)(/*)(\d*)", spec)
    if not m:
        return Fraction(1)
    num = int(m.group(1)) if m.group(1) else 1
    slashes, den_s = m.group(2), m.group(3)
    if not slashes:
        return Fraction(num)
    den = int(den_s) if den_s else 2 ** len(slashes)
    return Fraction(num, den or 1)


def parse_abc(text: str) -> dict[str, Any]:
    """Return {'tonic','mode','time_sig','bpm','notes':[(start,length_ticks,pitch)],'warnings':n}."""
    out: dict[str, Any] = {"tonic": None, "mode": None, "time_sig": None, "bpm": None,
                           "notes": [], "warnings": 0, "end_tick": 0}
    unit = Fraction(1, 8)
    unit_set = False
    acc: dict[str, int] = {}
    in_body = False
    tick = 0
    for raw in text.splitlines():
        line = raw.strip()
        if not line or line.startswith("%"):
            continue
        hm = re.match(r"^([A-Za-z]):\s*(.*)$", line)
        if hm and (not in_body or hm.group(1) in "KMLQ"):
            field, value = hm.group(1), hm.group(2).strip()
            if field == "K":
                out["tonic"], out["mode"] = parse_abc_key(value)
                acc = key_acc(out["tonic"], out["mode"])
                in_body = True
            elif field == "M":
                out["time_sig"] = value
                if not unit_set:
                    mm = re.match(r"(\d+)/(\d+)", value)
                    if mm:
                        unit = Fraction(1, 16) if int(mm.group(1)) / int(mm.group(2)) < 0.75 else Fraction(1, 8)
            elif field == "L":
                lm = re.match(r"(\d+)/(\d+)", value)
                if lm and int(lm.group(2)):
                    unit, unit_set = Fraction(int(lm.group(1)), int(lm.group(2))), True
            elif field == "Q":
                qm = re.search(r"=\s*(\d+(?:\.\d+)?)", value) or re.fullmatch(r"(\d+(?:\.\d+)?)", value)
                if qm:
                    out["bpm"] = float(qm.group(1))
            continue
        if not in_body or re.match(r"^[wW]:", line):
            continue
        line = re.sub(r'"[^"]*"', " ", line)
        line = re.sub(r"![^!]*!|\+[^+]*\+", " ", line)
        line = re.sub(r"\{[^}]*\}", " ", line)
        line = re.sub(r"\[[A-Za-z]:[^\]]*\]", " ", line)
        bar_acc: dict[str, int] = {}
        for m in _ABC_TOKEN.finditer(line):
            kind = m.lastgroup
            if m.group("bar"):
                bar_acc = {}
            elif m.group("tuplet") or m.group("other"):
                out["warnings"] += 1
            elif m.group("note"):
                letter, octs, a = m.group("letter"), m.group("oct"), m.group("acc")
                upper = letter.upper()
                pitch = 60 + _PC[upper] + (12 if letter.islower() else 0)
                pitch += 12 * octs.count("'") - 12 * octs.count(",")
                if a:
                    off = 0 if a == "=" else (len(a) if a[0] == "^" else -len(a))
                    bar_acc[upper] = off
                elif upper in bar_acc:
                    off = bar_acc[upper]
                else:
                    off = acc.get(upper, 0)
                ticks = round(PPQ * 4 * unit * _length(m.group("len")))
                out["notes"].append((tick, ticks, pitch + off))
                tick += ticks
            elif m.group("rest"):
                tick += round(PPQ * 4 * unit * _length(m.group("rlen")))
            elif kind == "ignore":
                continue
    out["end_tick"] = tick
    return out


# ---------------------------------------------------------------------------
# chords.md parser and chord spelling
# ---------------------------------------------------------------------------
def spell_chord(symbol: str) -> list[int] | None:
    """Chord symbol -> MIDI pitches (block voicing, root near C3, optional slash bass). None if unknown."""
    m = _CHORD_RE.match(symbol.strip())
    if not m:
        return None
    letter, acc, suffix, bass = m.groups()
    suffix = suffix.strip()
    if suffix not in CHORD_TABLE:
        return None
    root_pc = (_PC[letter] + (1 if acc == "#" else -1 if acc == "b" else 0)) % 12
    root = 48 + root_pc
    pitches = [root + i for i in CHORD_TABLE[suffix]]
    if bass:
        bpc = (_PC[bass[0]] + (1 if bass[1:] == "#" else -1 if bass[1:] == "b" else 0)) % 12
        pitches.insert(0, 36 + bpc)
    return pitches


def parse_chords(text: str) -> dict[str, Any]:
    """Return {'key': (tonic, mode)|None, 'bars': [[symbol,...], ...], 'warnings': n}."""
    head = gc.parse_header_keys(text)
    key = None
    if head.get("key"):
        parts = str(head["key"]).split()
        key = (parts[0], parts[1].lower() if len(parts) > 1 else "major")
    bars: list[list[str]] = []
    warnings = 0
    prev: list[str] = []
    for _, lines in gc.parse_sections(text):
        for line in lines:
            if not line.startswith(">"):
                continue
            for cell in [c.strip() for c in line[1:].strip().strip("|").split("|")]:
                if not cell:
                    continue
                if cell == "%":
                    bars.append(list(prev))
                    continue
                syms = cell.split()
                if any(spell_chord(s) is None for s in syms):
                    warnings += 1
                    syms = [s for s in syms if spell_chord(s) is not None]
                    if not syms:
                        continue
                prev = syms
                bars.append(syms)
    return {"key": key, "bars": bars, "warnings": warnings}


# ---------------------------------------------------------------------------
# Build
# ---------------------------------------------------------------------------
def build_midi(chords_text: str | None, abc_text: str | None, structure_text: str | None) -> tuple[bytes, dict[str, Any]]:
    """Return (smf bytes, info). Raises ValueError when there is nothing to write."""
    info: dict[str, Any] = {"warnings": 0, "chord_bars": 0, "melody_notes": 0}
    header = gc.parse_header_keys(structure_text) if structure_text else {}
    chords = parse_chords(chords_text) if chords_text is not None else None
    abc = parse_abc(abc_text) if abc_text is not None else None
    if chords is not None:
        info["warnings"] += chords["warnings"]
        if not chords["bars"]:
            raise ValueError("chords.md has no parseable concert-chord ('>') lines")
    if abc is not None:
        info["warnings"] += abc["warnings"]
        if not abc["notes"]:
            raise ValueError("melody.abc has no parseable notes")
    if chords is None and abc is None:
        raise ValueError("no chords.md or melody.abc given")

    bpm = header.get("bpm") or (abc or {}).get("bpm") or DEFAULT_BPM
    try:
        bpm = float(bpm)
    except (TypeError, ValueError):
        bpm = DEFAULT_BPM
    if bpm <= 0:
        bpm = DEFAULT_BPM
    time_sig = str(header.get("time_sig") or (abc or {}).get("time_sig") or "4/4")
    tm = re.match(r"^\s*(\d+)\s*/\s*(\d+)", time_sig)
    num, den = (int(tm.group(1)), int(tm.group(2))) if tm else (4, 4)
    if den & (den - 1) or den == 0 or num == 0:
        num, den = 4, 4
    tonic, mode = (header.get("key"), header.get("mode")) if header.get("key") else (None, None)
    if not tonic and abc and abc["tonic"]:
        tonic, mode = abc["tonic"], abc["mode"]
    if not tonic and chords and chords["key"]:
        tonic, mode = chords["key"]
    tonic, mode = str(tonic or "C"), str(mode or "major").lower()
    sf, mi = key_signature(tonic, mode)
    usec = round(60_000_000 / bpm)
    info.update(bpm=bpm, tempo_usec=usec, time_sig=f"{num}/{den}", key=f"{tonic} {mode}")

    conductor = [meta(0, 0x51, usec.to_bytes(3, "big")),
                 meta(0, 0x58, bytes([num, int(math.log2(den)), 24, 8])),
                 meta(0, 0x59, bytes([sf & 0xFF, mi]))]
    tracks = [track_chunk([], "conductor", conductor)]

    if chords is not None:
        bar_ticks = round(PPQ * 4 * num / den)
        ev: list[tuple[int, int, bytes]] = [(0, 0, bytes([0xC0, 0]))]
        for i, syms in enumerate(chords["bars"]):
            share = bar_ticks // len(syms)
            for j, sym in enumerate(syms):
                for p in spell_chord(sym) or []:
                    ev += note_events(0, p, i * bar_ticks + j * share, share, CHORD_VELOCITY)
        tracks.append(track_chunk(ev, "chords"))
        info["chord_bars"] = len(chords["bars"])
    if abc is not None:
        ev = [(0, 0, bytes([0xC1, 0]))]
        for start, length, pitch in abc["notes"]:
            ev += note_events(1, pitch, start, length, MELODY_VELOCITY)
        tracks.append(track_chunk(ev, "melody"))
        info["melody_notes"] = len(abc["notes"])
    info["tracks"] = len(tracks)
    data = smf(tracks)
    verify_bytes(data)
    info["bytes"] = len(data)
    return data, info


def verify_bytes(data: bytes) -> int:
    """Check header, track count, every MTrk length, and the end-of-track marker. Returns track count."""
    if data[:4] != b"MThd" or struct.unpack(">I", data[4:8])[0] != 6:
        raise ValueError("bad MThd header")
    fmt, ntrk, _ = struct.unpack(">HHH", data[8:14])
    if fmt != 1:
        raise ValueError(f"expected format 1, got {fmt}")
    pos, seen = 14, 0
    while pos < len(data):
        if data[pos:pos + 4] != b"MTrk":
            raise ValueError(f"missing MTrk at offset {pos}")
        (length,) = struct.unpack(">I", data[pos + 4:pos + 8])
        end = pos + 8 + length
        if end > len(data) or data[end - 3:end] != b"\xff\x2f\x00":
            raise ValueError(f"track {seen} length/end-of-track mismatch")
        pos, seen = end, seen + 1
    if seen != ntrk:
        raise ValueError(f"header declares {ntrk} tracks, found {seen}")
    return seen


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------
def add_args(p: Any) -> None:
    p.add_argument("--out", metavar="FILE.mid", help="write the Standard MIDI File here")
    p.add_argument("--chords", metavar="PATH", help="chords.md (concert chords)")
    p.add_argument("--melody", metavar="PATH", help="melody.abc")
    p.add_argument("--structure", metavar="PATH", help="structure.md (tempo, meter, key)")
    p.add_argument("--check", action="store_true", help="gate mode: validate a file can be produced, write nothing")
    p.add_argument("--selftest", action="store_true", help="write to a temp dir and verify bytes")


def main_fn(args: Any, config: dict[str, Any], res: gc.GateResult) -> gc.GateResult:
    chords, melody, structure = args.chords, args.melody, args.structure
    for p in args.paths:
        name = Path(p).name.lower()
        if name.endswith(".abc"):
            melody = melody or p
        elif name == "chords.md":
            chords = chords or p
        elif name == "structure.md":
            structure = structure or p
    if not (chords or melody):
        return res.error("give --chords and/or --melody (or positional melody.abc / chords.md)")
    texts = [gc.read_text(p) if p else None for p in (chords, melody, structure)]
    check_only = args.check or not args.out
    res.thresholds["mode"] = "check" if check_only else "write"
    try:
        data, info = build_midi(*texts)
    except ValueError as exc:
        if check_only:
            res.violate("midi_export", str(exc), None, "producible Standard MIDI File")
            return res
        return res.error(str(exc))
    res.metrics.update(info)
    if not check_only:
        out = Path(gc.norm(args.out))
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_bytes(data)
        res.metrics["out"] = gc.norm(out)
    if info["warnings"]:
        res.warn("input", f"{info['warnings']} unparsable item(s) skipped", info["warnings"], 0)
    return res


def selftest() -> int:
    import tempfile
    chords = "key: D major\n\n[Verse 1]\n| I | V | vi | IV |\n> | D | A | Bm | G/B |\n| I | % |\n> | D | % |\n"
    abc = "X:1\nT:t\nM:4/4\nL:1/8\nQ:1/4=100\nK:D\nD2 E2 F2 GA | B2 z2 ^c4 |\nw: a b c d e f g h i\n"
    structure = "key: D\nmode: major\nbpm: 118\ntime_sig: 4/4\n"
    failures = 0
    with tempfile.TemporaryDirectory() as tmp:
        tdir = Path(tmp)
        for name, text in (("chords.md", chords), ("melody.abc", abc), ("structure.md", structure)):
            (tdir / name).write_text(text, encoding="utf-8")
        out = tdir / "song.mid"
        with contextlib.redirect_stdout(io.StringIO()):
            code = main(["--out", str(out), "--chords", str(tdir / "chords.md"), "--melody", str(tdir / "melody.abc"),
                         "--structure", str(tdir / "structure.md")])
        data = out.read_bytes() if out.exists() else b""
        checks = {
            "exit 0": code == 0,
            "MThd+len6+fmt1": data[:4] == b"MThd" and data[4:8] == b"\x00\x00\x00\x06" and data[8:10] == b"\x00\x01",
            "3 tracks": data[10:12] == b"\x00\x03",
            "MTrk lengths": bool(data) and verify_bytes(data) == 3,
            "ends FF 2F 00": data[-3:] == b"\xff\x2f\x00",
            "tempo 118": (60_000_000 // 118).to_bytes(3, "big") in data or round(60_000_000 / 118).to_bytes(3, "big") in data,
        }
        with contextlib.redirect_stdout(io.StringIO()):
            bad = main(["--out", str(tdir / "x.mid"), "--chords", str(tdir / "missing.md")])
        checks["unreadable -> 3"] = bad == 3
        for label, ok in checks.items():
            print(f"selftest {label}: {'ok' if ok else 'MISMATCH'}")
            failures += 0 if ok else 1
    print("selftest: " + ("PASS" if failures == 0 else f"FAIL ({failures})"))
    return 0 if failures == 0 else 1


def main(argv: list[str] | None = None) -> int:
    args_in = sys.argv[1:] if argv is None else argv
    if "--selftest" in args_in:
        return selftest()
    return gc.run("midi_export.py", "Standard MIDI File (type 1) exporter and Stage 7c check.", add_args, main_fn, argv)


if __name__ == "__main__":
    sys.exit(main())
