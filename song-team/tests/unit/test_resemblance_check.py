"""Unit tests for song-team/scripts/resemblance_check.py (W1-2)."""
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


LYRICS = """[Verse 1]
I packed the car with every plate I own
the kettle rattled on the seat beside me

[Chorus]
Nobody knows my name here yet
the hallway light clicks on at six
"""

CORPUS_FAR = "a lighthouse keeper counts the ships that never dock tonight and sleeps\n"
CORPUS_NEAR = "someone said the kettle rattled on the seat beside me once\n"


class ResemblanceCheckTests(unittest.TestCase):
    def setUp(self):
        self.mod = _load("resemblance_check")
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def _write(self, name: str, text: str) -> str:
        p = self.root / name
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text, encoding="utf-8", newline="\n")
        return str(p)

    def _run(self, *argv: str) -> tuple[int, dict]:
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            code = self.mod.main(["--json", *argv])
        return code, json.loads(buf.getvalue())

    def test_pass_no_overlap(self):
        code, out = self._run("--corpus", self._write("c.txt", CORPUS_FAR), self._write("lyrics.md", LYRICS))
        self.assertEqual((code, out["status"]), (0, "PASS"), out)
        self.assertEqual(out["metrics"]["matching_ngrams"], 0)
        self.assertEqual(out["metrics"]["total_ngrams"], 26)
        self.assertEqual(out["thresholds"]["ngram_max_overlap"], 0.05)

    def test_fail_overlap_names_first_ngram(self):
        code, out = self._run("--corpus", self._write("c.txt", CORPUS_NEAR), self._write("lyrics.md", LYRICS))
        self.assertEqual((code, out["status"]), (1, "FAIL"))
        self.assertEqual(out["metrics"]["matching_ngrams"], 4)
        v = out["violations"][0]
        self.assertEqual(v["location"], "Verse 1:2")
        self.assertIn("the kettle rattled on the", v["reason"])
        self.assertAlmostEqual(v["observed"], 4 / 26, places=3)

    def test_skipped_empty_corpus(self):
        code, out = self._run(self._write("lyrics.md", LYRICS))
        self.assertEqual((code, out["status"]), (2, "SKIPPED"))
        self.assertEqual(out["violations"], [])

    def test_skipped_all_missing(self):
        code, out = self._run("--corpus", str(self.root / "nope.txt"), self._write("lyrics.md", LYRICS))
        self.assertEqual((code, out["status"]), (2, "SKIPPED"))
        self.assertEqual(out["metrics"]["missing_files"], 1)

    def test_error_short_lyric(self):
        code, out = self._run("--corpus", self._write("c.txt", CORPUS_FAR), self._write("lyrics.md", "[Verse 1]\nfour words only here\n"))
        self.assertEqual((code, out["status"]), (3, "ERROR"))

    def test_corpus_from_config_relative_to_config_dir(self):
        self._write("corpus/near.txt", CORPUS_NEAR)
        cfg = self._write("config.yml", "originality:\n  resemblance_corpus: [corpus/near.txt, corpus/missing.txt]\n  ngram_max_overlap: 0.5\n")
        code, out = self._run("--config", cfg, self._write("lyrics.md", LYRICS))
        self.assertEqual(out["status"], "PASS")
        self.assertEqual(out["metrics"]["missing_files"], 1)
        self.assertEqual(out["thresholds"]["ngram_max_overlap"], 0.5)
        code, out = self._run("--config", cfg, "--ngram-max-overlap", "0.01", self._write("lyrics.md", LYRICS))
        self.assertEqual((out["thresholds"]["ngram_max_overlap"], out["status"]), (0.01, "FAIL"))

    def test_genre_flag_is_ignored_for_originality(self):
        cfg = self._write("config.yml", "quality:\n  genre_overrides:\n    pop: { ngram_max_overlap: 0.9 }\n"
                                        "originality:\n  ngram_max_overlap: 0.02\n")
        code, out = self._run("--config", cfg, "--genre", "pop", "--corpus", self._write("c.txt", CORPUS_NEAR),
                              self._write("lyrics.md", LYRICS))
        self.assertEqual((out["thresholds"]["ngram_max_overlap"], out["status"]), (0.02, "FAIL"))

    def test_windows_style_path(self):
        c, l = self._write("c.txt", CORPUS_FAR), self._write("lyrics.md", LYRICS)
        if os.name == "nt":
            c, l = c.replace("/", "\\"), l.replace("/", "\\")
        code, out = self._run("--corpus", c, l)
        self.assertEqual(out["status"], "PASS")


if __name__ == "__main__":
    unittest.main()
