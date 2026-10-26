"""Unit tests for music-team/scripts/cliche_scan.py (W1-2)."""
from __future__ import annotations

import contextlib
import io
import json
import os
import tempfile
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))  # noqa: E402
from _helpers import load_script

CLEAN_LYRICS = """[Verse 1]
I packed the car with every plate I own
# a comment that would otherwise count
the kettle rattled on the seat beside me

[Chorus]
Nobody knows my name here yet
the hallway light clicks on at six
"""

CLICHE_LYRICS = """[Verse 1]
I packed the car, my heart of gold!
Dance all night till the end of time

[Chorus]
Nobody knows my name here yet
"""


class ClicheScanTests(unittest.TestCase):
    def setUp(self):
        self.mod = load_script("cliche_scan")
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

    def test_help_exits_zero(self):
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf), self.assertRaises(SystemExit) as cm:
            self.mod.main(["--help"])
        self.assertEqual(cm.exception.code, 0)
        self.assertIn("--cliche-list", buf.getvalue())

    def test_pass_clean_lyrics(self):
        code, out = self._run(self._write("lyrics.md", CLEAN_LYRICS))
        self.assertEqual((code, out["status"]), (0, "PASS"), out)
        self.assertEqual(out["metrics"]["hits"], 0)
        self.assertEqual(out["metrics"]["words"], 30)  # comment and tags excluded
        self.assertEqual(out["thresholds"]["cliche_max_per_100_words"], 2)

    def test_fail_lyrics_with_locations(self):
        code, out = self._run(self._write("lyrics.md", CLICHE_LYRICS))
        self.assertEqual((code, out["status"]), (1, "FAIL"))
        self.assertEqual(out["metrics"]["hits"], 3)
        found = {(v["location"], v["reason"]) for v in out["violations"]}
        self.assertIn(("Verse 1:1", "cliche: 'heart of gold'"), found)
        self.assertIn(("Verse 1:2", "cliche: 'dance all night'"), found)
        self.assertIn(("Verse 1:2", "cliche: 'till the end of time'"), found)

    def test_word_boundary_not_substring(self):
        lyrics = "[Verse 1]\nthe hearts of goldfinches sing\n"
        code, out = self._run(self._write("lyrics.md", lyrics))
        self.assertEqual(out["metrics"]["hits"], 0)

    def test_nested_phrases_count_once(self):
        lst = self._write("nested.txt", "take my breath away\nyou take my breath away\nbreath away\n")
        lyr = self._write("lyrics.md", "[Verse 1]\nyou take my breath away tonight\n")
        code, out = self._run("--cliche-list", lst, lyr)
        self.assertEqual(out["metrics"]["hits"], 1)
        self.assertEqual(out["violations"][0]["reason"], "cliche: 'you take my breath away'")
        # same list, lyric only contains the shorter phrase: still exactly one hit
        code, out = self._run("--cliche-list", lst, self._write("lyrics.md", "[Verse 1]\nthey take my breath away\n"))
        self.assertEqual(out["metrics"]["hits"], 1)
        self.assertEqual(out["violations"][0]["reason"], "cliche: 'take my breath away'")

    def test_two_distinct_phrases_on_one_line(self):
        lst = self._write("two.txt", "heart of gold\ndance all night\n")
        lyr = self._write("lyrics.md", "[Verse 1]\nmy heart of gold will dance all night\n")
        code, out = self._run("--cliche-list", lst, lyr)
        self.assertEqual(out["metrics"]["hits"], 2)
        self.assertEqual({v["reason"] for v in out["violations"]},
                         {"cliche: 'heart of gold'", "cliche: 'dance all night'"})

    def test_boundary_exactly_at_limit_passes(self):
        # 1 hit in 50 words = exactly 2.0 per 100 -> PASS (limit is inclusive)
        lst = self._write("one.txt", "heart of gold\n")
        filler = " ".join(["word"] * 47)
        lyr = self._write("lyrics.md", f"[Verse 1]\nheart of gold {filler}\n")
        code, out = self._run("--cliche-list", lst, lyr)
        self.assertEqual(out["metrics"]["words"], 50)
        self.assertEqual(out["metrics"]["per_100_words"], 2.0)
        self.assertEqual((code, out["status"]), (0, "PASS"), out)
        # one word fewer tips it over
        lyr = self._write("lyrics.md", f"[Verse 1]\nheart of gold {' '.join(['word'] * 46)}\n")
        code, out = self._run("--cliche-list", lst, lyr)
        self.assertEqual((code, out["status"]), (1, "FAIL"))

    def test_concept_scans_only_three_fields(self):
        concept = ("---\ntitle: Heart of Gold\nhook_line: nobody knows my name here yet\n"
                   "central_image: a key that fits no door\narc: [broken heart, turn, end]\n"
                   "title_rationale: tears in the rain are fine here\n---\n## Notes\nlove is blind\n")
        code, out = self._run(self._write("concept.md", concept))
        self.assertEqual(out["metrics"]["hits"], 1)
        self.assertEqual(out["metrics"]["words"], 15)
        self.assertEqual(out["status"], "FAIL")
        self.assertEqual(out["violations"][0]["location"], "title")

    def test_plain_text_location(self):
        code, out = self._run(self._write("notes.txt", "# heading ignored\nplain words here\nhold on tight now\n"))
        self.assertEqual(out["violations"][0]["location"], "text:3")

    def test_error_empty_text(self):
        code, out = self._run(self._write("lyrics.md", "# only a comment\n[Verse 1]\n"))
        self.assertEqual((code, out["status"]), (3, "ERROR"))
        self.assertIn("empty", out["violations"][0]["reason"])

    def test_error_bad_threshold_type(self):
        cfg = self._write("config.yml", "quality:\n  cliche_max_per_100_words: lots\n")
        code, out = self._run("--config", cfg, self._write("lyrics.md", CLEAN_LYRICS))
        self.assertEqual((code, out["status"]), (3, "ERROR"))
        self.assertIn("cliche_max_per_100_words", out["violations"][0]["reason"])

    def test_windows_style_path(self):
        p = Path(self._write("lyrics.md", CLEAN_LYRICS))
        arg = p.as_posix().replace("/", "\\", 1) if os.name == "nt" else str(p)
        code, out = self._run(arg)
        self.assertEqual(out["status"], "PASS", out)

    def test_threshold_precedence(self):
        cfg = self._write("config.yml", "quality:\n  cliche_max_per_100_words: 50\n  genre_overrides:\n"
                                        "    country: { cliche_max_per_100_words: 1 }\n")
        lyr = self._write("lyrics.md", CLICHE_LYRICS)
        code, out = self._run("--config", cfg, lyr)
        self.assertEqual((out["thresholds"]["cliche_max_per_100_words"], out["status"]), (50, "PASS"))
        code, out = self._run("--config", cfg, "--genre", "country", lyr)
        self.assertEqual((out["thresholds"]["cliche_max_per_100_words"], out["status"]), (1, "FAIL"))
        code, out = self._run("--config", cfg, "--genre", "country", "--cliche-max-per-100-words", "99", lyr)
        self.assertEqual((out["thresholds"]["cliche_max_per_100_words"], out["status"]), (99.0, "PASS"))

    def test_custom_list_override(self):
        lst = self._write("mine.txt", "# custom\nkettle rattled\n")
        code, out = self._run("--cliche-list", lst, self._write("lyrics.md", CLEAN_LYRICS))
        self.assertEqual(out["metrics"]["hits"], 1)


if __name__ == "__main__":
    unittest.main()
