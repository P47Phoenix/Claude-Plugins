"""Unit tests for music-team/scripts/rhyme_check.py (W1-1)."""
from __future__ import annotations

import contextlib
import io
import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _helpers import load_script, mixed_path  # noqa: E402

STRUCTURE = """key: D
mode: major
bpm: 118
time_sig: 4/4
form_template: VC

| section | label | bars | meter_spec | rhyme_scheme |
|---------|-------|------|------------|--------------|
| 1 | Verse 1 | 8 | 8/uSuSuSuS; 8/uSuSuSuS; 8/uSuSuSuS; 8/uSuSuSuS | ABAB |
| 2 | Chorus | 8 | 7/SuSuSuS; 7/SuSuSuS; 7/SuSuSuS; 7/SuSuSuS | AxAx |
"""
GOOD_LYRICS = """[Verse 1]
I walked away before the morning light
# comment
I found the road and held it like a song
I kept the window open through the night
I knew the road would carry me along

[Chorus]
Nobody knows my name here yet
Nobody sees the way I came
Nobody holds the light I get
Nobody calls me by my name
"""
SLANT_LYRICS = GOOD_LYRICS.replace("the night", "the lime")
BAD_LYRICS = GOOD_LYRICS.replace("the night", "the door")


class RhymeCheckTests(unittest.TestCase):
    def setUp(self):
        self.mod = load_script("rhyme_check")
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

    def _pair(self, lyrics: str, structure: str = STRUCTURE) -> list[str]:
        return [self._write("lyrics.md", lyrics), self._write("structure.md", structure)]

    def test_rhyme_key_and_classify(self):
        self.assertEqual(self.mod.rhyme_key("light"), "It")
        self.assertEqual(self.mod.rhyme_key("Night!"), "It")
        self.assertEqual(self.mod.rhyme_key("sky"), "I")
        self.assertEqual(self.mod.rhyme_key("day"), "A")
        self.assertEqual(self.mod.rhyme_key("lime"), "Ime")   # trailing silent e stays in the tail
        self.assertEqual(self.mod.rhyme_key("be"), "E")
        self.assertEqual(self.mod.rhyme_key("bought"), "out")  # silent gh dropped
        self.assertEqual(self.mod.rhyme_key("through"), "U")   # exception table
        self.assertEqual(self.mod.rhyme_key("lonely"), "E")    # final y after another vowel group
        self.assertEqual(self.mod.classify("time", "lime"), "full")
        self.assertEqual(self.mod.classify("light", "night"), "full")
        self.assertEqual(self.mod.classify("light", "lime"), "slant")   # same vowel group
        self.assertEqual(self.mod.classify("night", "bought"), "slant")  # same consonant cluster
        self.assertEqual(self.mod.classify("light", "door"), "none")
        self.assertEqual(self.mod.classify("go", "see"), "none")

    def test_vowel_digraph_normalisation(self):
        for a, b in [("see", "be"), ("day", "weigh"), ("blue", "through"), ("blue", "you"),
                     ("high", "sky"), ("love", "of"), ("come", "some"), ("one", "done")]:
            self.assertEqual(self.mod.classify(a, b), "full", (a, b))
        self.assertEqual(self.mod.classify("go", "see"), "none")
        self.assertEqual(self.mod.classify("name", "day"), "slant")  # same vowel class, extra tail
        self.assertEqual(self.mod.last_word("held it like a song,"), "song")

    def test_pass_fixture(self):
        code, d = self._run(self._pair(GOOD_LYRICS))
        self.assertEqual((code, d["status"]), (0, "PASS"), d)
        self.assertEqual(d["script"], "rhyme_check")
        self.assertEqual(d["metrics"]["pairs_checked"], 3)  # ABAB = 2 pairs, AxAx = 1 pair
        self.assertEqual(d["metrics"]["slant_pairs"], 0)
        self.assertEqual(d["violations"], [])
        self.assertIs(d["thresholds"]["slant_rhyme_allowed"], True)

    def test_slant_tolerated_then_rejected(self):
        code, d = self._run(self._pair(SLANT_LYRICS))
        self.assertEqual((code, d["status"]), (0, "PASS"), d)
        self.assertEqual(d["metrics"]["slant_pairs"], 1)
        code, d = self._run(["--no-slant-rhyme"] + self._pair(SLANT_LYRICS))
        self.assertEqual((code, d["status"]), (1, "FAIL"))
        self.assertEqual(d["violations"][0]["location"], "Verse 1:3")

    def test_fail_fixture(self):
        code, d = self._run(self._pair(BAD_LYRICS))
        self.assertEqual((code, d["status"]), (1, "FAIL"))
        self.assertEqual(len(d["violations"]), 1)
        self.assertEqual(d["violations"][0]["location"], "Verse 1:3")
        self.assertEqual(d["violations"][0]["observed"], "light/door")

    def test_skipped_non_english(self):
        code, d = self._run(["--language", "fr"] + self._pair(BAD_LYRICS))
        self.assertEqual((code, d["status"]), (2, "SKIPPED"))
        self.assertEqual(d["violations"], [])
        brief = self._write("brief.md", "---\ntheme: x\nlanguage: de\n---\n")
        code, d = self._run(self._pair(BAD_LYRICS) + [brief])
        self.assertEqual((code, d["status"]), (2, "SKIPPED"))

    def test_error_fixtures(self):
        short = GOOD_LYRICS.replace("I knew the road would carry me along\n", "")
        code, d = self._run(self._pair(short))
        self.assertEqual((code, d["status"]), (3, "ERROR"))
        self.assertEqual(d["violations"][0]["location"], "Verse 1")
        code, d = self._run(self._pair(GOOD_LYRICS.replace("[Chorus]", "[Outro]")))
        self.assertEqual((code, d["status"]), (3, "ERROR"))
        code, d = self._run(self._pair("# empty\n"))
        self.assertEqual((code, d["status"]), (3, "ERROR"))
        code, d = self._run([self._write("lyrics.md", GOOD_LYRICS)])
        self.assertEqual((code, d["status"]), (3, "ERROR"))

    def test_windows_style_path(self):
        lyr, st = (mixed_path(x) for x in self._pair(GOOD_LYRICS))
        code, d = self._run([lyr, st])
        self.assertEqual((code, d["status"]), (0, "PASS"))
        empty = mixed_path(self._write("lyrics.md", "# empty\n"))
        code, d = self._run([empty, st])
        self.assertEqual((code, d["status"]), (3, "ERROR"))
        loc = d["violations"][0]["location"]
        self.assertTrue(loc.endswith("/lyrics.md"), loc)
        self.assertNotIn("\\", loc)

    def test_bad_config_value_is_error(self):
        cfg = self._write("config.yml", "quality:\n  slant_rhyme_allowed: maybe\n")
        code, d = self._run(["--config", cfg] + self._pair(GOOD_LYRICS))
        self.assertEqual((code, d["status"]), (3, "ERROR"))
        self.assertIn("slant_rhyme_allowed", d["violations"][0]["reason"])

    # --- boundaries ----------------------------------------------------------
    def test_empty_scheme_is_unconstrained(self):
        structure = STRUCTURE.replace("| AxAx |", "|  |")
        code, d = self._run(self._pair(BAD_LYRICS.replace("by my name", "by my door"), structure))
        self.assertEqual(d["status"], "FAIL")  # Verse 1 still checked
        self.assertEqual(len(d["violations"]), 1)
        code, d = self._run(self._pair(GOOD_LYRICS.replace("by my name", "by my door"), structure))
        self.assertEqual((code, d["status"]), (0, "PASS"), d)
        self.assertEqual(d["metrics"]["pairs_checked"], 2)

    def test_upper_case_x_is_unconstrained(self):
        structure = STRUCTURE.replace("| AxAx |", "| AXAX |")
        code, d = self._run(self._pair(GOOD_LYRICS.replace("by my name", "by my door"), structure))
        self.assertEqual((code, d["status"]), (0, "PASS"), d)
        self.assertEqual(d["metrics"]["pairs_checked"], 3)

    def test_line_count_mismatch_is_error(self):
        longer = GOOD_LYRICS.replace("by my name\n", "by my name\nOne line too many here\n")
        code, d = self._run(self._pair(longer))
        self.assertEqual((code, d["status"]), (3, "ERROR"))
        self.assertEqual(d["violations"][0]["location"], "Chorus")
        self.assertIn("5 differs from rhyme_scheme length 4", d["violations"][0]["reason"])

    def test_threshold_precedence(self):
        paths = self._pair(SLANT_LYRICS)
        cfg = self._write("config.yml", "quality:\n  slant_rhyme_allowed: false\n  genre_overrides:\n"
                                        "    pop:\n      slant_rhyme_allowed: true\n")
        _, d = self._run(paths)
        self.assertIs(d["thresholds"]["slant_rhyme_allowed"], True)
        code, d = self._run(["--config", cfg] + paths)
        self.assertIs(d["thresholds"]["slant_rhyme_allowed"], False)
        self.assertEqual(code, 1)
        code, d = self._run(["--config", cfg, "--genre", "pop"] + paths)
        self.assertIs(d["thresholds"]["slant_rhyme_allowed"], True)
        self.assertEqual(code, 0)
        code, d = self._run(["--config", cfg, "--genre", "pop", "--no-slant-rhyme"] + paths)
        self.assertIs(d["thresholds"]["slant_rhyme_allowed"], False)
        self.assertEqual(code, 1)

    def test_help_exits_zero(self):
        with contextlib.redirect_stdout(io.StringIO()):
            with self.assertRaises(SystemExit) as cm:
                self.mod.main(["--help"])
        self.assertEqual(cm.exception.code, 0)


if __name__ == "__main__":
    unittest.main()
