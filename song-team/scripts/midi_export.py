#!/usr/bin/env python3
"""midi_export.py - write a type-1 Standard MIDI File from melody.abc and chords.md
(stage-gates.md section 3; Stage 7 package step). Not a gate: exit 0 on success,
3 on parse failure.

usage: midi_export.py [--json] [--out PATH] melody.abc chords.md [structure.md]

Track 0: tempo (from ``Q:``) and time signature (from ``M:``). Track 1: the
melody on channel 0, ABC durations scaled by ``L:`` (tied notes merge into one
event). Track 2: one root-position block triad per bar on channel 1, built from
the concert chord names on the ``>`` lines of chords.md in section order (bars
beyond the chord list repeat the last chord; without chords.md the quoted chord
symbols in the ABC are used). ``--out`` defaults to ``song.mid`` beside melody.abc.
"""
from __future__ import annotations

import re
import struct
import sys
from fractions import Fraction
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))
import gate_common as gc  # noqa: E402
import abc_common as ac  # noqa: E402

SCRIPT = "midi_export"
TICKS_PER_QUARTER = 480
MELODY_CHANNEL, CHORD_CHANNEL = 0, 1
MELODY_VELOCITY, CHORD_VELOCITY = 96, 72
CHORD_OCTAVE_BASE = 48  # C3

_PC = {"C": 0, "D": 2, "E": 4, "F": 5, "G": 7, "A": 9, "B": 11}
_CHORD_RE = re.compile(r"^([A-Ga-g])([#b]?)(.*)$")


# ---------------------------------------------------------------------------
# Chords
# ---------------------------------------------------------------------------
def chord_to_pitches(name: str) -> list[int]:
    """``D`` -> [50, 54, 57]; ``Bm`` minor third; ``dim``/``aug``; ``sus2``/``sus4``;
    ``7`` adds a minor seventh, ``maj7`` a major seventh. A slash bass is ignored."""
    base = name.split("/", 1)[0].strip()
    m = _CHORD_RE.match(base)
    if not m:
        raise ValueError(f"unparseable chord name {name!r}")
    letter, acc, qual = m.group(1).upper(), m.group(2), m.group(3).lower()
    root = CHORD_OCTAVE_BASE + _PC[letter] + (1 if acc == "#" else -1 if acc == "b" else 0)
    third, fifth = 4, 7
    if "dim" in qual or qual.startswith("°") or qual.startswith("o"):
        third, fifth = 3, 6
    elif "aug" in qual or "+" in qual:
        third, fifth = 4, 8
    elif "sus2" in qual:
        third = 2
    elif "sus4" in qual:
        third = 5
    elif qual.startswith("min") or (qual.startswith("m") and not qual.startswith("maj")):
        third = 3
    pitches = [root, root + third, root + fifth]
    if "maj7" in qual:
        pitches.append(root + 11)
    elif "7" in qual:
        pitches.append(root + 9 if "dim" in qual else root + 10)
    return pitches


def concert_chords_from_md(text: str) -> list[str]:
    """Flat list of concert chord cells from every ``>`` line, in section order; ``%`` repeats."""
    out: list[str] = []
    for _, lines in gc.parse_sections(text):
        for line in lines:
            if not line.startswith(">"):
                continue
            cells = [c.strip() for c in line[1:].strip().strip("|").split("|")]
            for cell in cells:
                if cell == "%":
                    if out:
                        out.append(out[-1])
                elif cell:
                    out.append(cell)
    return out


# ---------------------------------------------------------------------------
# Byte writer
# ---------------------------------------------------------------------------
def vlq(value: int) -> bytes:
    if value < 0:
        raise ValueError("negative delta time")
    out = [value & 0x7F]
    value >>= 7
    while value:
        out.append(0x80 | (value & 0x7F))
        value >>= 7
    return bytes(reversed(out))


def _events_to_track(events: list[tuple[int, bytes]]) -> bytes:
    """``events`` are (absolute_tick, message); note-offs sort before note-ons at the same tick."""
    def order(ev: tuple[int, bytes]) -> tuple[int, int]:
        status = ev[1][0] & 0xF0
        return ev[0], 0 if status == 0x80 else 1

    data = bytearray()
    last = 0
    end_tick = 0
    for tick, msg in sorted(events, key=order):
        data += vlq(tick - last) + msg
        last = tick
        end_tick = tick
    data += vlq(0) + b"\xff\x2f\x00"
    return b"MTrk" + struct.pack(">I", len(data)) + bytes(data)


def _note(tick: int, channel: int, pitch: int, dur: int, velocity: int) -> list[tuple[int, bytes]]:
    pitch = max(0, min(127, pitch))
    return [(tick, bytes([0x90 | channel, pitch, velocity])),
            (tick + max(1, dur), bytes([0x80 | channel, pitch, 0]))]


def build_midi(abc: dict[str, Any], chord_names: list[str]) -> tuple[bytes, dict[str, int]]:
    unit = abc["unit_length"] * 4 * TICKS_PER_QUARTER     # ticks per L: unit
    bpm = abc["bpm"] or 120
    ts = ac.parse_time_sig(abc.get("time_sig") or "") or (4, 4)
    bar_ticks_default = int(Fraction(ts[0], ts[1]) * 4 * TICKS_PER_QUARTER)

    tempo = [(0, b"\xff\x51\x03" + struct.pack(">I", round(60_000_000 / bpm))[1:]),
             (0, b"\xff\x58\x04" + bytes([ts[0], ts[1].bit_length() - 1, 24, 8]))]

    melody: list[tuple[int, bytes]] = []
    chords: list[tuple[int, bytes]] = [(0, bytes([0xC0 | CHORD_CHANNEL, 0]))]
    melody.append((0, bytes([0xC0 | MELODY_CHANNEL, 0])))
    tick = 0
    bar_index = 0
    melody_events = chord_events = 0
    pending: tuple[int, int, int] | None = None     # (start, pitch, dur) for tie merging

    def flush() -> None:
        nonlocal pending, melody_events
        if pending is not None:
            melody.extend(_note(pending[0], MELODY_CHANNEL, pending[1], pending[2], MELODY_VELOCITY))
            melody_events += 1
            pending = None

    for sec in abc["sections"]:
        for bar in sec["bars"]:
            bar_start = tick
            for note in bar["notes"]:
                dur = int(note["dur_units"] * unit)
                if note["is_rest"]:
                    flush()
                elif note["tied_from_prev"] and pending is not None and pending[1] == note["midi"]:
                    pending = (pending[0], pending[1], pending[2] + dur)
                else:
                    flush()
                    pending = (tick, note["midi"], dur)
                tick += dur
            bar_len = tick - bar_start if tick > bar_start else bar_ticks_default
            if tick == bar_start:
                tick += bar_len
            if chord_names:
                name = chord_names[min(bar_index, len(chord_names) - 1)]
            elif bar["chords"]:
                name = bar["chords"][0]
            else:
                name = None
            if name:
                for p in chord_to_pitches(name):
                    chords.extend(_note(bar_start, CHORD_CHANNEL, p, bar_len, CHORD_VELOCITY))
                    chord_events += 1
            bar_index += 1
    flush()

    tracks = [_events_to_track(tempo), _events_to_track(melody), _events_to_track(chords)]
    header = b"MThd" + struct.pack(">IHHH", 6, 1, len(tracks), TICKS_PER_QUARTER)
    data = header + b"".join(tracks)
    return data, {"tracks": len(tracks), "melody_events": melody_events, "chord_events": chord_events,
                  "bars": bar_index, "bytes": len(data)}


def read_midi_summary(path: str | Path) -> dict[str, Any]:
    """Parse the MThd and walk the MTrk chunks: ``{format, ntrks, division, track_lengths}``."""
    data = Path(gc.norm(path)).read_bytes()
    if data[:4] != b"MThd":
        raise ValueError("not a MIDI file (no MThd)")
    hlen, fmt, ntrks, division = struct.unpack(">IHHH", data[4:14])
    pos = 8 + hlen
    lengths: list[int] = []
    while pos + 8 <= len(data):
        tag, length = data[pos:pos + 4], struct.unpack(">I", data[pos + 4:pos + 8])[0]
        if tag != b"MTrk":
            raise ValueError(f"unexpected chunk {tag!r} at byte {pos}")
        lengths.append(length)
        pos += 8 + length
    if pos != len(data):
        raise ValueError("trailing bytes after last MTrk")
    return {"format": fmt, "ntrks": ntrks, "division": division, "track_lengths": lengths}


# ---------------------------------------------------------------------------
# Entry
# ---------------------------------------------------------------------------
def add_args(p: Any) -> None:
    p.add_argument("--out", metavar="PATH", help="output .mid path (default: song.mid beside melody.abc)")


def main_fn(args: Any, config: dict[str, Any], res: gc.GateResult) -> gc.GateResult:
    mpath = gc.file_named(args.paths, "melody.abc")
    if not mpath:
        return res.error("melody.abc not given")
    try:
        abc = ac.parse_abc(gc.read_text(mpath))
    except ac.AbcParseError as exc:
        return res.error(f"ABC parse error: {exc}", f"melody.abc:{exc.line}" if exc.line else "melody.abc")
    for field in ("K", "L"):
        if field not in abc["headers"]:
            return res.error(f"required header {field}: missing", f"melody.abc:{field}")
    cpath = gc.file_named(args.paths, "chords.md")
    chord_names = concert_chords_from_md(gc.read_text(cpath)) if cpath else []
    data, metrics = build_midi(abc, chord_names)
    out = Path(gc.norm(args.out)) if args.out else Path(mpath).with_name("song.mid")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_bytes(data)
    res.metrics.update(metrics)
    res.metrics["chords_in_chart"] = len(chord_names)
    res.thresholds["out"] = out.as_posix()
    return res


def main(argv: list[str] | None = None) -> int:
    return gc.run(f"{SCRIPT}.py", "Write a type-1 MIDI file from melody.abc and chords.md.", add_args, main_fn, argv)


if __name__ == "__main__":
    sys.exit(main())
