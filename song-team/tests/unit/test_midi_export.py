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
        # track 0 carries tempo 118 bpm and 4/4
        t0 = data[14 + 8:14 + 8 + summary["track_lengths"][0]]
        self.assertIn(b"\xff\x51\x03" + (round(60_000_000 / 118)).to_bytes(3, "big"), t0)
        self.assertIn(b"\xff\x58\x04\x04\x02\x18\x08", t0)

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
