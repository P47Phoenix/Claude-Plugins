"""Unit tests for song-team/scripts/midi_export.py (W3-1)."""
from __future__ import annotations

import contextlib
import io
import json
import struct
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))  # noqa: E402
from _helpers import FIXTURES, load_script, mixed_path

FULL = FIXTURES / "songs" / "FULL_SONG"
NEG = FIXTURES / "negative"


def _last_tick(track: bytes) -> int:
    """Walk one MTrk body (channel + meta events only) and return the absolute tick of its last event."""
    pos, tick, status = 0, 0, 0
    while pos < len(track):
        delta = 0
        while True:
            b = track[pos]
            pos += 1
            delta = (delta << 7) | (b & 0x7F)
            if not b & 0x80:
                break
        tick += delta
        b = track[pos]
        if b == 0xFF:                                   # meta: FF type len data
            length = track[pos + 2]
            pos += 3 + length
            continue
        if b & 0x80:
            status = b
            pos += 1
        pos += 1 if (status & 0xF0) in (0xC0, 0xD0) else 2
    return tick


class MidiExportTests(unittest.TestCase):
    def setUp(self):
        self.mod = load_script("midi_export")
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def _run(self, *argv: str) -> tuple[int, dict]:
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            code = self.mod.main(["--json", *argv])
        return code, json.loads(buf.getvalue())

    def test_round_trip_full_song(self):
        out = self.root / "pkg" / "song.mid"
        code, res = self._run("--out", str(out), str(FULL / "melody.abc"), str(FULL / "chords.md"))
        self.assertEqual((code, res["status"], res["script"]), (0, "PASS", "midi_export"), res)
        self.assertEqual(res["metrics"]["tracks"], 3)
        self.assertGreater(res["metrics"]["melody_events"], 0)
        self.assertEqual(res["metrics"]["chord_events"], 56 * 3)       # one triad per bar, 56 bars
        self.assertEqual(res["metrics"]["bytes"], out.stat().st_size)
        data = out.read_bytes()
        self.assertEqual(data[:4], b"MThd")
        self.assertEqual(struct.unpack(">IHHH", data[4:14]), (6, 1, 3, self.mod.TICKS_PER_QUARTER))
        summary = self.mod.read_midi_summary(out)
        self.assertEqual((summary["format"], summary["ntrks"]), (1, 3))
        self.assertEqual(len(summary["track_lengths"]), 3)
        self.assertTrue(all(n > 0 for n in summary["track_lengths"]))
        self.assertGreater(summary["track_lengths"][1], summary["track_lengths"][0])
        # track 0 carries tempo 118 bpm (508475 us per quarter) and 4/4
        t0 = data[14 + 8:14 + 8 + summary["track_lengths"][0]]
        self.assertIn(b"\xff\x51\x03\x07\xc2\x3b", t0)
        self.assertIn(b"\xff\x58\x04\x04\x02\x18\x08", t0)
        # track 1: program change, then the first melody note-on is D4 (0x90 0x3E) at tick 0
        t1_start = 14 + 8 + summary["track_lengths"][0] + 8
        t1 = data[t1_start:t1_start + summary["track_lengths"][1]]
        self.assertEqual(t1[:3], b"\x00\xc0\x00")
        self.assertEqual(t1[3:6], b"\x00\x90\x3e")
        self.assertEqual(t1[6], self.mod.MELODY_VELOCITY)
        self.assertEqual(_last_tick(t1), 56 * 1920)                   # 56 bars of 8 eighths at 240 ticks

    def test_tempo_honours_beat_unit(self):
        melody = self.root / "melody.abc"
        text = (FULL / "melody.abc").read_text(encoding="utf-8").replace("Q:1/4=118\n", "Q:3/8=50\n")
        melody.write_text(text, encoding="utf-8", newline="\n")
        code, res = self._run(str(melody))
        self.assertEqual(code, 0, res)
        data = (self.root / "song.mid").read_bytes()
        # 50 dotted quarters per minute = 75 quarters per minute = 800000 us per quarter
        self.assertIn(b"\xff\x51\x03" + (800_000).to_bytes(3, "big"), data)
        self.assertEqual(self.mod.ac.parse_tempo_beat("3/8=50"), __import__("fractions").Fraction(3, 8))
        self.assertIsNone(self.mod.ac.parse_tempo_beat("118"))

    def test_tied_notes_merge_across_line_end(self):
        melody = self.root / "melody.abc"
        melody.write_text("X:1\nT:t\nM:4/4\nL:1/8\nQ:1/4=120\nK:C\n%%section A\nC4 E4- |\nE4 G4 |\n",
                          encoding="utf-8", newline="\n")
        code, res = self._run(str(melody))
        self.assertEqual(code, 0, res)
        self.assertEqual(res["metrics"]["melody_events"], 3)        # C, E (tied, 8 units), G

    def test_missing_melody_error_wording(self):
        chords = self.root / "chords.md"
        chords.write_text("key: C major\n\n[A]\n| I |\n", encoding="utf-8", newline="\n")
        code, res = self._run(str(chords))
        self.assertEqual((code, res["status"]), (3, "ERROR"))
        self.assertEqual(res["violations"][0]["reason"], "no argument whose basename is melody.abc")

    def test_default_out_beside_melody(self):
        melody = self.root / "melody.abc"
        melody.write_text((FULL / "melody.abc").read_text(encoding="utf-8"), encoding="utf-8", newline="\n")
        code, res = self._run(mixed_path(str(melody)))
        self.assertEqual(code, 0, res)
        self.assertTrue((self.root / "song.mid").exists())
        self.assertEqual(res["metrics"]["chord_events"], 0)          # no chords.md and no inline symbols

    def test_error_on_malformed_abc(self):
        code, res = self._run("--out", str(self.root / "x.mid"), str(NEG / "malformed-abc" / "melody.abc"))
        self.assertEqual((code, res["status"]), (3, "ERROR"))
        self.assertIn("parse error", res["violations"][0]["reason"])
        self.assertFalse((self.root / "x.mid").exists())

    def test_chord_spelling(self):
        f = self.mod.chord_to_pitches
        self.assertEqual(f("D"), [50, 54, 57])
        self.assertEqual(f("Bm"), [59, 62, 66])
        self.assertEqual(f("A7"), [57, 61, 64, 67])
        self.assertEqual(f("Bdim"), [59, 62, 65])
        self.assertEqual(f("Fmaj7"), [53, 57, 60, 64])
        self.assertEqual(f("G/B")[0], 55)
        self.assertEqual(f("Bb"), [58, 62, 65])
        self.assertEqual(f("Bm7b5"), [59, 62, 65, 69])     # diminished triad + minor seventh
        self.assertEqual(f("Bdim7"), [59, 62, 65, 68])     # diminished triad + diminished seventh
        self.assertEqual(f("B°7"), [59, 62, 65, 68])
        self.assertEqual(f("Bo7"), [59, 62, 65, 68])
        self.assertEqual(f("Em7"), [52, 55, 59, 62])
        with self.assertRaises(ValueError):
            f("H")

    def test_concert_chords_from_md(self):
        names = self.mod.concert_chords_from_md("key: D major\n\n[Verse 1]\n| I | V | % | IV |\n> | D | A | % | G |\n")
        self.assertEqual(names, ["D", "A", "A", "G"])

    def test_vlq(self):
        self.assertEqual(self.mod.vlq(0), b"\x00")
        self.assertEqual(self.mod.vlq(127), b"\x7f")
        self.assertEqual(self.mod.vlq(128), b"\x81\x00")
        self.assertEqual(self.mod.vlq(0x0FFFFFFF), b"\xff\xff\xff\x7f")

    def test_help_exits_zero(self):
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf), self.assertRaises(SystemExit) as cm:
            self.mod.main(["--help"])
        self.assertEqual(cm.exception.code, 0)
        self.assertIn("--out", buf.getvalue())


if __name__ == "__main__":
    unittest.main()
