"""Unit tests for song-team/scripts/cliche_scan.py (W1-2)."""
from __future__ import annotations

import contextlib
import importlib.util
import io
import json
import os
import tempfile
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[2] / "scripts"


def _load(name: str):
    spec = importlib.util.spec_from_file_location(name, SCRIPTS / f"{name}.py")
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod


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
        self.mod = _load("cliche_scan")
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

    def test_windows_style_path(self):
        p = self._write("lyrics.md", CLEAN_LYRICS)
        if os.name == "nt":
            p = p.replace("/", "\\")
        code, out = self._run(p)
        self.assertEqual(out["status"], "PASS")

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
