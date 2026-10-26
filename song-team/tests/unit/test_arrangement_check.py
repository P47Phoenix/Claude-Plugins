"""Unit tests for song-team/scripts/arrangement_check.py (W3-1)."""
from __future__ import annotations

import contextlib
import io
import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))  # noqa: E402
from _helpers import FIXTURES, load_script, mixed_path

FULL = FIXTURES / "songs" / "FULL_SONG"
FLAT = FIXTURES / "negative" / "flat-energy"

HEADER = "key: D\nmode: major\nbpm: 118\ntime_sig: 4/4\n\n"
COLS = "| section | energy | instruments_in | instruments_out | texture_note |\n|---|---|---|---|---|\n"


def table(rows: list[tuple[str, object]]) -> str:
    return HEADER + COLS + "".join(f"| {label} | {energy} | - | - | - |\n" for label, energy in rows)


class ArrangementCheckTests(unittest.TestCase):
    def setUp(self):
        self.mod = load_script("arrangement_check")
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def _write(self, name: str, text: str) -> str:
        p = self.root / name
        p.write_text(text, encoding="utf-8", newline="\n")
        return str(p)

    def _run(self, *argv: str) -> tuple[int, dict]:
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            code = self.mod.main(["--json", *argv])
        return code, json.loads(buf.getvalue())

    def _arr(self, rows: list[tuple[str, object]]) -> str:
        return self._write("arrangement.md", table(rows))

    def test_help_exits_zero(self):
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf), self.assertRaises(SystemExit) as cm:
            self.mod.main(["--help"])
        self.assertEqual(cm.exception.code, 0)
        self.assertIn("--energy-curve", buf.getvalue())

    def test_full_song_fixture_passes(self):
        code, out = self._run(str(FULL / "arrangement.md"))
        self.assertEqual((code, out["status"]), (0, "PASS"), out)
        self.assertEqual(out["thresholds"]["energy_curve"], "chorus_rising")
        self.assertEqual(out["metrics"], {"sections": 8, "global_max": 9, "chorus_count": 3})
        self.assertEqual(out["violations"], [])

    def test_flat_energy_fixture_fails_rule_d_only(self):
        code, out = self._run(str(FLAT / "arrangement.md"))
        self.assertEqual((code, out["status"]), (1, "FAIL"))
        self.assertEqual([v["location"] for v in out["violations"]], ["Verse 1", "Verse 2"])
        self.assertTrue(all(v["reason"].startswith("(d)") for v in out["violations"]))

    # -- chorus_rising rules ------------------------------------------------
    def test_rule_a_chorus_falls(self):
        rows = [("Verse 1", 3), ("Chorus", 8), ("Verse 2", 4), ("Chorus", 7), ("Bridge", 5), ("Chorus", 9)]
        code, out = self._run(self._arr(rows))
        self.assertEqual(out["status"], "FAIL")
        self.assertEqual([(v["location"], v["reason"][:3]) for v in out["violations"]], [("Chorus:2", "(a)")])
        self.assertEqual((out["violations"][0]["observed"], out["violations"][0]["limit"]), (7, 8))

    def test_rule_b_peak_outside_final_chorus_and_bridge(self):
        rows = [("Verse 1", 3), ("Chorus", 7), ("Instrumental", 9), ("Chorus", 8)]
        code, out = self._run(self._arr(rows))
        self.assertEqual([(v["location"], v["reason"][:3]) for v in out["violations"]], [("Instrumental", "(b)")])
        self.assertEqual((out["violations"][0]["observed"], out["violations"][0]["limit"]), (9, 8))

    def test_rule_b_peak_in_bridge_ties_count(self):
        rows = [("Verse 1", 3), ("Chorus", 7), ("Bridge", 9), ("Chorus", 9), ("Outro", 2)]
        code, out = self._run(self._arr(rows))
        self.assertEqual(out["status"], "PASS", out)
        rows = [("Verse 1", 3), ("Chorus", 7), ("Bridge", 9), ("Chorus", 8), ("Outro", 2)]
        code, out = self._run(self._arr(rows))
        self.assertEqual(out["status"], "PASS", out)  # G in the bridge is allowed

    def test_rule_c_final_section_not_below_peak(self):
        rows = [("Verse 1", 3), ("Chorus", 7), ("Verse 2", 4), ("Chorus", 9), ("Outro", 9)]
        code, out = self._run(self._arr(rows))
        self.assertEqual([(v["location"], v["reason"][:3]) for v in out["violations"]], [("Outro", "(c)")])
        rows[-1] = ("Outro", 8)
        code, out = self._run(self._arr(rows))
        self.assertEqual(out["status"], "PASS", out)

    def test_rule_d_verse_without_following_chorus_unconstrained(self):
        rows = [("Verse 1", 3), ("Chorus", 7), ("Verse 2", 7), ("Outro", 2)]
        code, out = self._run(self._arr(rows))
        self.assertEqual(out["status"], "PASS", out)
        rows = [("Verse 1", 3), ("Chorus", 7), ("Verse 2", 7), ("Chorus", 7)]
        code, out = self._run(self._arr(rows))
        self.assertEqual([(v["location"], v["reason"][:3]) for v in out["violations"]], [("Verse 2", "(d)")])

    def test_drop_counts_as_chorus(self):
        rows = [("Intro", 2), ("Build", 5), ("Drop", 8), ("Breakdown", 4), ("Build", 6), ("Drop", 9), ("Outro", 3)]
        code, out = self._run(self._arr(rows))
        self.assertEqual(out["status"], "PASS", out)
        self.assertEqual(out["metrics"]["chorus_count"], 2)
        self.assertNotIn("no_chorus", out["metrics"])

    def test_aaba_labels_fall_back_to_strict_rising(self):
        rows = [("A1", 3), ("A2", 4), ("B", 7), ("A3", 5)]
        code, out = self._run(self._arr(rows))
        self.assertEqual(out["status"], "PASS", out)
        self.assertEqual(out["metrics"]["no_chorus"], 1)
        self.assertEqual(out["metrics"]["chorus_count"], 0)
        rows = [("A1", 5), ("A2", 4), ("B", 7), ("A3", 5)]
        code, out = self._run(self._arr(rows))
        self.assertEqual(out["status"], "FAIL")
        self.assertEqual(out["violations"][0]["location"], "A2")
        self.assertIn("strict_rising", out["violations"][0]["reason"])

    # -- other curves -------------------------------------------------------
    def test_strict_rising_pass_and_fail(self):
        rows = [("Verse 1", 3), ("Chorus", 7), ("Bridge", 9), ("Chorus", 9), ("Outro", 2)]
        code, out = self._run("--energy-curve", "strict_rising", self._arr(rows))
        self.assertEqual((code, out["status"]), (0, "PASS"), out)
        self.assertEqual(out["thresholds"]["energy_curve"], "strict_rising")
        # FULL_SONG dips in Verse 2 and Bridge: PASS under chorus_rising, FAIL under strict_rising
        code, out = self._run("--energy-curve", "strict_rising", str(FULL / "arrangement.md"))
        self.assertEqual((code, out["status"]), (1, "FAIL"))
        self.assertEqual([v["location"] for v in out["violations"]], ["Verse 2", "Bridge"])
        rows = [("Verse 1", 3), ("Chorus", 9), ("Verse 2", 4), ("Chorus", 6)]
        code, out = self._run("--energy-curve", "strict_rising", self._arr(rows))
        self.assertEqual([v["location"] for v in out["violations"]], ["Chorus:2"])
        self.assertIn("rises after the peak", out["violations"][0]["reason"])

    def test_free_always_passes(self):
        code, out = self._run("--energy-curve", "free", str(FLAT / "arrangement.md"))
        self.assertEqual((code, out["status"]), (0, "PASS"))
        self.assertEqual(out["metrics"]["global_max"], 5)
        rows = [("Verse 1", 9), ("Chorus", 1), ("Verse 2", 9), ("Chorus", 1)]
        code, out = self._run("--energy-curve", "free", self._arr(rows))
        self.assertEqual((code, out["status"]), (0, "PASS"))

    # -- errors -------------------------------------------------------------
    def test_energy_out_of_range_is_error(self):
        code, out = self._run(self._arr([("Verse 1", 3), ("Chorus", 11)]))
        self.assertEqual((code, out["status"]), (3, "ERROR"))
        self.assertEqual(out["violations"][0]["location"], "Chorus")
        code, out = self._run(self._arr([("Verse 1", 0), ("Chorus", 5)]))
        self.assertEqual((code, out["status"]), (3, "ERROR"))
        code, out = self._run(self._arr([("Verse 1", "loud"), ("Chorus", 5)]))
        self.assertEqual((code, out["status"]), (3, "ERROR"))
        self.assertIn("loud", out["violations"][0]["reason"])

    def test_no_rows_is_error(self):
        code, out = self._run(self._write("arrangement.md", HEADER + COLS))
        self.assertEqual((code, out["status"]), (3, "ERROR"))
        code, out = self._run(self._write("arrangement.md", HEADER))
        self.assertEqual((code, out["status"]), (3, "ERROR"))

    def test_unknown_curve_in_config_is_error(self):
        cfg = self._write("config.yml", "quality:\n  energy_curve: wavy\n")
        code, out = self._run("--config", cfg, str(FULL / "arrangement.md"))
        self.assertEqual((code, out["status"]), (3, "ERROR"))
        self.assertIn("wavy", out["violations"][0]["reason"])

    # -- thresholds and paths -----------------------------------------------
    def test_threshold_precedence(self):
        cfg = self._write("config.yml", "quality:\n  energy_curve: free\n  genre_overrides:\n"
                                        "    edm: { energy_curve: strict_rising }\n")
        flat = str(FLAT / "arrangement.md")
        code, out = self._run("--config", cfg, flat)
        self.assertEqual((out["thresholds"]["energy_curve"], out["status"]), ("free", "PASS"))
        code, out = self._run("--config", cfg, "--genre", "edm", flat)
        self.assertEqual((out["thresholds"]["energy_curve"], out["status"]), ("strict_rising", "PASS"))
        code, out = self._run("--config", cfg, "--genre", "edm", "--energy-curve", "chorus_rising", flat)
        self.assertEqual((out["thresholds"]["energy_curve"], out["status"]), ("chorus_rising", "FAIL"))

    def test_windows_style_path(self):
        code, out = self._run(mixed_path(str(FULL / "arrangement.md")))
        self.assertEqual(out["status"], "PASS", out)

    def test_role_detection(self):
        role = self.mod.role_of
        self.assertEqual([role(x) for x in ("Chorus", "Drop", "Bridge", "B", "Verse 1", "A2", "Intro", "Pre-Chorus 1")],
                         ["chorus", "chorus", "bridge", "bridge", "verse", "verse", "neutral", "neutral"])


if __name__ == "__main__":
    unittest.main()
