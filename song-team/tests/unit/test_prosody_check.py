"""Unit tests for song-team/scripts/prosody_check.py (W1-1)."""
from __future__ import annotations

import contextlib
import io
import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _helpers import FIXTURES, load_script, mixed_path  # noqa: E402

GOLD = FIXTURES / "prosody-gold" / "gold.tsv"

STRUCTURE = """key: D
mode: major
bpm: 118
time_sig: 4/4
form_template: VC

| section | label | bars | meter_spec | rhyme_scheme |
|---------|-------|------|------------|--------------|
| 1 | Verse 1 | 8 | 8/uSuSuSuS; 8/uSuSuSuS | AA |
| 2 | Chorus | 8 | 7/SuSuSuS; 7/SuSuSuS | AA |
"""
GOOD_LYRICS = """[Verse 1]
I walked away before the dawn
# a comment line is ignored
I found the road and held it long

[Chorus]
Someone knows my name tonight
Someone holds the fading light
"""
BAD_LYRICS = """[Verse 1]
Morning sunlight falling golden river
Whisper softly shadow window silver

[Chorus]
Someone knows my name tonight
Someone holds the fading light
"""


class ProsodyCheckTests(unittest.TestCase):
    def setUp(self):
        self.mod = load_script("prosody_check")
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def _write(self, name: str, text: str) -> str:
        p = self.root / name
        p.write_text(text, encoding="utf-8")
        return str(p)

    def _run(self, argv: list[str]) -> tuple[int, dict]:
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            code = self.mod.main(argv + ["--json"])
        return code, json.loads(out.getvalue())

    # --- pure functions -------------------------------------------------
    def test_count_syllables(self):
        cases = {"the": 1, "table": 2, "fire": 1, "every": 3, "walked": 1, "wanted": 2,
                 "wishes": 2, "makes": 1, "beautiful": 3, "I'm": 1, "isn't": 2, "crying": 2,
                 "beyond": 2, "radio": 3, "nation": 2, "lonely": 2, "rhythm": 2, "strength": 1}
        for w, n in cases.items():
            self.assertEqual(self.mod.count_syllables(w), n, w)

    def test_stress_pattern(self):
        self.assertEqual(self.mod.stress_pattern("I walked away before the morning light"), "uSuSuSuSuS")
        self.assertEqual(self.mod.stress_pattern("I walked away before the dawn"), "uSuSuSuS")
        self.assertEqual(self.mod.stress_pattern("Nobody knows my name"), "SuuSuS")
        self.assertEqual(self.mod.syllables_in_line("I packed the car with everything I own"), 10)

    # --- lyrics mode ---------------------------------------------------------
    def test_pass_fixture(self):
        code, d = self._run([self._write("lyrics.md", GOOD_LYRICS), self._write("structure.md", STRUCTURE)])
        self.assertEqual(code, 0, d)
        self.assertEqual(d["status"], "PASS")
        self.assertEqual(d["script"], "prosody_check")
        self.assertEqual(d["violations"], [])
        self.assertIn("verse_1_mismatch_ratio", d["metrics"])
        self.assertIn("chorus_mismatch_ratio", d["metrics"])
        self.assertEqual(d["metrics"]["syllable_mismatch_lines"], 0)
        self.assertEqual(d["thresholds"]["prosody_tolerance"], 0.15)

    def test_fail_fixture(self):
        code, d = self._run([self._write("lyrics.md", BAD_LYRICS), self._write("structure.md", STRUCTURE)])
        self.assertEqual(code, 1)
        self.assertEqual(d["status"], "FAIL")
        self.assertGreater(d["metrics"]["verse_1_mismatch_ratio"], 0.15)
        self.assertEqual(len(d["violations"]), 1)
        self.assertRegex(d["violations"][0]["location"], r"^Verse 1:[12]$")
        self.assertEqual(d["violations"][0]["limit"], 0.15)

    def test_skipped_non_english(self):
        code, d = self._run(["--language", "fr", self._write("lyrics.md", GOOD_LYRICS),
                             self._write("structure.md", STRUCTURE)])
        self.assertEqual((code, d["status"]), (2, "SKIPPED"))
        brief = self._write("brief.md", "---\ntheme: x\nlanguage: es\n---\n## Brief\nx\n")
        code, d = self._run([self._write("lyrics.md", GOOD_LYRICS), self._write("structure.md", STRUCTURE), brief])
        self.assertEqual((code, d["status"]), (2, "SKIPPED"))
        self.assertEqual(d["violations"], [])

    def test_error_fixtures(self):
        lyrics = self._write("lyrics.md", GOOD_LYRICS.replace("[Chorus]", "[Bridge]"))
        code, d = self._run([lyrics, self._write("structure.md", STRUCTURE)])
        self.assertEqual((code, d["status"]), (3, "ERROR"))
        self.assertIn("Bridge", d["violations"][0]["reason"])
        code, d = self._run([self._write("lyrics.md", "# nothing here\n"), self._write("structure.md", STRUCTURE)])
        self.assertEqual((code, d["status"]), (3, "ERROR"))
        code, d = self._run([self._write("lyrics.md", GOOD_LYRICS), self._write("structure.md", "key: D\n")])
        self.assertEqual((code, d["status"]), (3, "ERROR"))
        code, d = self._run([self._write("lyrics.md", GOOD_LYRICS), str(self.root / "missing" / "structure.md")])
        self.assertEqual((code, d["status"]), (3, "ERROR"))

    def test_extra_lines_do_not_crash(self):
        lyrics = GOOD_LYRICS.replace("fading light\n", "fading light\nOne more line than the meter has\n")
        code, d = self._run([self._write("lyrics.md", lyrics), self._write("structure.md", STRUCTURE)])
        self.assertEqual(code, 1)
        self.assertGreater(d["metrics"]["chorus_mismatch_ratio"], 0.15)

    def test_windows_style_path(self):
        lyr = mixed_path(self._write("lyrics.md", GOOD_LYRICS))
        st = mixed_path(self._write("structure.md", STRUCTURE))
        code, d = self._run([lyr, st])
        self.assertEqual((code, d["status"]), (0, "PASS"))
        empty = mixed_path(self._write("lyrics.md", "# nothing here\n"))
        code, d = self._run([empty, st])
        self.assertEqual((code, d["status"]), (3, "ERROR"))
        loc = d["violations"][0]["location"]
        self.assertTrue(loc.endswith("/lyrics.md"), loc)
        self.assertNotIn("\\", loc)

    def test_bad_config_values_are_error(self):
        lyr, st = self._write("lyrics.md", GOOD_LYRICS), self._write("structure.md", STRUCTURE)
        cfg = self._write("config.yml", "quality:\n  prosody_tolerance: loose\n")
        code, d = self._run(["--config", cfg, lyr, st])
        self.assertEqual((code, d["status"]), (3, "ERROR"))
        self.assertIn("prosody_tolerance", d["violations"][0]["reason"])
        concept = self._write("concept.md", "---\nhook_line: Nobody knows my name\n---\n")
        cfg = self._write("config.yml", "quality:\n  hook_max_syllables: twelve\n")
        code, d = self._run(["--hook", "--config", cfg, concept])
        self.assertEqual((code, d["status"]), (3, "ERROR"))
        self.assertIn("hook_max_syllables", d["violations"][0]["reason"])

    # --- boundaries ----------------------------------------------------------
    def test_ratio_exactly_at_tolerance_passes(self):
        structure = STRUCTURE.replace("8/uSuSuSuS; 8/uSuSuSuS", "; ".join(["10/uSuSuSuSuS"] * 4))
        lyrics = """[Verse 1]
I walked away before the morning light
I found the road and held it like a song
I kept the window open through the night
I knew the road would carry me along

[Chorus]
Someone knows my name tonight
Someone holds the fading light
"""
        code, d = self._run([self._write("lyrics.md", lyrics), self._write("structure.md", structure)])
        self.assertEqual(d["metrics"]["verse_1_mismatch_ratio"], 0.15, d)
        self.assertEqual((code, d["status"]), (0, "PASS"))
        code, d = self._run(["--prosody-tolerance", "0.1499", self._write("lyrics.md", lyrics),
                             self._write("structure.md", structure)])
        self.assertEqual((code, d["status"]), (1, "FAIL"))

    def test_hook_exactly_at_limit_passes(self):
        hook = "I walked away before the morning light and then"  # 12 syllables
        self.assertEqual(self.mod.syllables_in_line(hook), 12)
        concept = self._write("concept.md", f"---\nhook_line: {hook}\n---\n")
        code, d = self._run(["--hook", concept])
        self.assertEqual((code, d["status"]), (0, "PASS"))
        self.assertEqual(d["metrics"]["hook_syllables"], 12)
        code, d = self._run(["--hook", "--hook-max-syllables", "11", concept])
        self.assertEqual((code, d["status"]), (1, "FAIL"))

    def test_empty_meter_section_is_unconstrained(self):
        structure = STRUCTURE.replace("| 8 | 7/SuSuSuS; 7/SuSuSuS | AA |", "| 8 |  |  |")
        lyrics = GOOD_LYRICS.replace("Someone knows my name tonight", "Morning sunlight falling golden river")
        code, d = self._run([self._write("lyrics.md", lyrics), self._write("structure.md", structure)])
        self.assertEqual((code, d["status"]), (0, "PASS"), d)
        self.assertEqual(d["metrics"]["chorus_mismatch_ratio"], 0.0)

    def test_threshold_precedence(self):
        lyr, st = self._write("lyrics.md", GOOD_LYRICS), self._write("structure.md", STRUCTURE)
        cfg = self._write("config.yml", "quality:\n  prosody_tolerance: 0.3\n  genre_overrides:\n"
                                        "    pop:\n      prosody_tolerance: 0.4\n")
        _, d = self._run([lyr, st])
        self.assertEqual(d["thresholds"]["prosody_tolerance"], 0.15)
        _, d = self._run(["--config", cfg, lyr, st])
        self.assertEqual(d["thresholds"]["prosody_tolerance"], 0.3)
        _, d = self._run(["--config", cfg, "--genre", "pop", lyr, st])
        self.assertEqual(d["thresholds"]["prosody_tolerance"], 0.4)
        _, d = self._run(["--config", cfg, "--genre", "pop", "--prosody-tolerance", "0.5", lyr, st])
        self.assertEqual(d["thresholds"]["prosody_tolerance"], 0.5)

    # --- hook mode -----------------------------------------------------------
    def test_hook_mode(self):
        concept = self._write("concept.md", "---\ntitle: T\nhook_line: Nobody knows my name here yet\n---\n")
        code, d = self._run(["--hook", concept])
        self.assertEqual((code, d["status"]), (0, "PASS"))
        self.assertEqual(d["metrics"]["hook_syllables"], 8)
        self.assertEqual(d["thresholds"]["hook_max_syllables"], 12)
        code, d = self._run(["--hook", "--hook-max-syllables", "6", concept])
        self.assertEqual((code, d["status"]), (1, "FAIL"))
        self.assertEqual(d["violations"][0]["location"], "hook_line")
        motif = self._write("concept.md", "---\ntitle: T\nmotif: rising fourths\n---\n")
        code, d = self._run(["--hook", motif])
        self.assertEqual((code, d["status"]), (2, "SKIPPED"))
        self.assertEqual(d["metrics"]["skipped_reason"], "instrumental motif")
        empty = self._write("concept.md", "---\ntitle: T\n---\n")
        code, d = self._run(["--hook", empty])
        self.assertEqual((code, d["status"]), (3, "ERROR"))
        code, d = self._run(["--hook", "--language", "de", concept])
        self.assertEqual((code, d["status"]), (2, "SKIPPED"))

    def test_help_exits_zero(self):
        with contextlib.redirect_stdout(io.StringIO()):
            with self.assertRaises(SystemExit) as cm:
                self.mod.main(["--help"])
        self.assertEqual(cm.exception.code, 0)

    # --- gold accuracy -------------------------------------------------------
    def test_gold_accuracy(self):
        if not GOLD.exists():
            self.skipTest(f"gold set not present: {GOLD}")
        rows = []
        for raw in GOLD.read_text(encoding="utf-8-sig").splitlines():
            if not raw.strip() or raw.lstrip().startswith("#"):
                continue
            parts = raw.split("\t")
            if len(parts) < 3:
                continue
            rows.append((parts[0].strip(), int(parts[1].strip()), parts[2].strip()))
        if not rows:
            self.skipTest("gold set has no rows")
        syl_ok = sum(1 for line, n, _ in rows if self.mod.syllables_in_line(line) == n)
        str_ok = sum(1 for line, _, st in rows if self.mod.stress_pattern(line) == st)
        syl_acc, str_acc = syl_ok / len(rows), str_ok / len(rows)
        print(f"\nprosody gold: {len(rows)} lines, syllable accuracy {syl_acc:.1%}, "
              f"stress accuracy {str_acc:.1%}")
        self.assertGreaterEqual(syl_acc, 0.90)
        self.assertGreaterEqual(str_acc, 0.85)


if __name__ == "__main__":
    unittest.main()
