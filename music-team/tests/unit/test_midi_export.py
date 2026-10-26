"""Unit tests for music-team/scripts/midi_export.py (W8)."""
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
from _helpers import FIXTURES, load_script

FULL = FIXTURES / "songs" / "FULL_SONG"


def read_vlq(data: bytes, pos: int) -> tuple[int, int]:
    value = 0
    while True:
        b = data[pos]
        pos += 1
        value = (value << 7) | (b & 0x7F)
        if not b & 0x80:
            return value, pos


def parse_tracks(data: bytes) -> list[list[tuple[int, bytes]]]:
    """Return per track a list of (delta, raw event bytes) using running-status-free decoding."""
    tracks, pos = [], 14
    while pos < len(data):
        assert data[pos:pos + 4] == b"MTrk"
        (length,) = struct.unpack(">I", data[pos + 4:pos + 8])
        body, p, events = data[pos + 8:pos + 8 + length], 0, []
        while p < len(body):
            delta, p = read_vlq(body, p)
            status = body[p]
            if status == 0xFF:
                size, q = read_vlq(body, p + 2)
                events.append((delta, body[p:q + size]))
                p = q + size
            elif status & 0xF0 in (0xC0, 0xD0):
                events.append((delta, body[p:p + 2]))
                p += 2
            else:
                events.append((delta, body[p:p + 3]))
                p += 3
        tracks.append(events)
        pos += 8 + length
    return tracks


class MidiExportTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.mod = load_script("midi_export")
        cls.chords = (FULL / "chords.md").read_text(encoding="utf-8")
        cls.abc = (FULL / "melody.abc").read_text(encoding="utf-8")
        cls.structure = (FULL / "structure.md").read_text(encoding="utf-8")
        cls.data, cls.info = cls.mod.build_midi(cls.chords, cls.abc, cls.structure)

    def test_header_bytes(self):
        d = self.data
        self.assertEqual(d[:4], b"MThd")
        self.assertEqual(struct.unpack(">I", d[4:8])[0], 6)
        fmt, ntrk, ppq = struct.unpack(">HHH", d[8:14])
        self.assertEqual((fmt, ntrk, ppq), (1, 3, 480))

    def test_mtrk_length_integrity_and_end_marker(self):
        pos, count = 14, 0
        while pos < len(self.data):
            self.assertEqual(self.data[pos:pos + 4], b"MTrk")
            (length,) = struct.unpack(">I", self.data[pos + 4:pos + 8])
            end = pos + 8 + length
            self.assertLessEqual(end, len(self.data))
            self.assertEqual(self.data[end - 3:end], b"\xff\x2f\x00")
            pos, count = end, count + 1
        self.assertEqual(pos, len(self.data))
        self.assertEqual(count, 3)
        self.assertEqual(self.mod.verify_bytes(self.data), 3)

    def test_tempo_time_and_key_meta(self):
        conductor = parse_tracks(self.data)[0]
        raw = [e for _, e in conductor]
        tempo = next(e for e in raw if e[:2] == b"\xff\x51")
        self.assertEqual(int.from_bytes(tempo[3:6], "big"), round(60_000_000 / 118))
        timesig = next(e for e in raw if e[:2] == b"\xff\x58")
        self.assertEqual(list(timesig[3:5]), [4, 2])
        keysig = next(e for e in raw if e[:2] == b"\xff\x59")
        self.assertEqual((keysig[3], keysig[4]), (2, 0))  # D major: two sharps

    def test_chord_track_note_pairs_balance(self):
        events = [e for _, e in parse_tracks(self.data)[1] if e[0] & 0xF0 in (0x80, 0x90)]
        ons = [e for e in events if e[0] & 0xF0 == 0x90]
        offs = [e for e in events if e[0] & 0xF0 == 0x80]
        self.assertGreater(len(ons), 0)
        self.assertEqual(len(ons), len(offs))
        self.assertEqual(sorted(e[1] for e in ons), sorted(e[1] for e in offs))
        self.assertEqual(self.info["chord_bars"], 56)

    def test_first_chord_is_d_major(self):
        events = parse_tracks(self.data)[1]
        first_ons = sorted([e[1] for d, e in events if e[0] == 0x90][:3])
        self.assertEqual(first_ons, [50, 54, 57])  # D3 F#3 A3

    def test_melody_track_parses_without_warnings(self):
        self.assertEqual(self.info["warnings"], 0)
        self.assertGreater(self.info["melody_notes"], 100)
        abc = self.mod.parse_abc(self.abc)
        self.assertEqual(abc["warnings"], 0)
        first = abc["notes"][0]
        self.assertEqual((first[0], first[1], first[2]), (0, 480, 62))  # D4, quarter at L:1/8 length 2
        pitches = [n[2] for n in abc["notes"]]
        self.assertTrue(all(55 <= p <= 79 for p in pitches))

    def test_note_on_off_balance_melody(self):
        events = [e for _, e in parse_tracks(self.data)[2] if e[0] & 0xF0 in (0x80, 0x90)]
        self.assertEqual(sum(e[0] & 0xF0 == 0x90 for e in events), sum(e[0] & 0xF0 == 0x80 for e in events))

    def test_vlq(self):
        cases = {0: b"\x00", 0x7F: b"\x7f", 0x80: b"\x81\x00", 0x3FFF: b"\xff\x7f", 0x4000: b"\x81\x80\x00"}
        for value, expected in cases.items():
            self.assertEqual(self.mod.vlq(value), expected)

    def test_chord_spelling(self):
        self.assertEqual(self.mod.spell_chord("Bm"), [59, 62, 66])
        self.assertEqual(self.mod.spell_chord("G/B")[0], 47 - 12 + 12)
        self.assertEqual(self.mod.spell_chord("Fmaj7"), [53, 57, 60, 64])
        self.assertIsNone(self.mod.spell_chord("H7"))

    def test_abc_subset_and_warnings(self):
        abc = "X:1\nM:3/4\nL:1/8\nQ:90\nK:C\n^C,2 _B' =c z2 (3abc | x\n"
        parsed = self.mod.parse_abc(abc)
        self.assertEqual(parsed["bpm"], 90.0)
        self.assertGreaterEqual(parsed["warnings"], 1)  # the triplet marker
        self.assertEqual(parsed["notes"][0][2], 49)  # ^C, = C#3

    def run_cli(self, argv):
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            code = self.mod.main(argv)
        return code, buf.getvalue()

    def test_cli_writes_file_and_check_mode(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "package" / "song.mid"
            code, text = self.run_cli(["--json", "--out", str(out), "--chords", str(FULL / "chords.md"),
                                       "--melody", str(FULL / "melody.abc"), "--structure", str(FULL / "structure.md")])
            self.assertEqual(code, 0)
            self.assertEqual(json.loads(text)["status"], "PASS")
            self.assertEqual(out.read_bytes(), self.data)
            code, text = self.run_cli(["--json", "--check", str(FULL / "melody.abc"), str(FULL / "chords.md")])
            self.assertEqual(code, 0)
            self.assertEqual(json.loads(text)["thresholds"]["mode"], "check")

    def test_unreadable_input_is_error(self):
        code, _ = self.run_cli(["--out", "x.mid", "--chords", "/nonexistent/chords.md"])
        self.assertEqual(code, 3)

    def test_no_inputs_is_error(self):
        self.assertEqual(self.run_cli(["--check"])[0], 3)

    def test_empty_chords_is_error_on_write_and_fail_on_check(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / "chords.md"
            p.write_text("key: C major\n\n[Verse 1]\n| I |\n", encoding="utf-8")
            self.assertEqual(self.run_cli(["--out", str(Path(tmp) / "a.mid"), "--chords", str(p)])[0], 3)
            self.assertEqual(self.run_cli(["--check", "--chords", str(p)])[0], 1)

    def test_selftest(self):
        self.assertEqual(self.run_cli(["--selftest"])[0], 0)


if __name__ == "__main__":
    unittest.main()
