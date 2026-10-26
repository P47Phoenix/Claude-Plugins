"""Unit tests for music-team/scripts/resemblance_check.py (W1-2)."""
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

LYRICS = """[Verse 1]
I packed the car with every plate I own
the kettle rattled on the seat beside me

[Chorus]
Nobody knows my name here yet
the hallway light clicks on at six
"""
# Verse 1: 9 + 8 = 17 tokens -> 13 five-grams; Chorus: 6 + 7 = 13 tokens -> 9; total 22.
TOTAL_NGRAMS = 22

CORPUS_FAR = "a lighthouse keeper counts the ships that never dock tonight and sleeps\n"
CORPUS_NEAR = "someone said the kettle rattled on the seat beside me once\n"


class ResemblanceCheckTests(unittest.TestCase):
    def setUp(self):
        self.mod = load_script("resemblance_check")
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

    def test_help_exits_zero(self):
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf), self.assertRaises(SystemExit) as cm:
            self.mod.main(["--help"])
        self.assertEqual(cm.exception.code, 0)
        self.assertIn("--corpus", buf.getvalue())

    def test_pass_no_overlap(self):
        code, out = self._run("--corpus", self._write("c.txt", CORPUS_FAR), self._write("lyrics.md", LYRICS))
        self.assertEqual((code, out["status"]), (0, "PASS"), out)
        self.assertEqual(out["metrics"]["matching_ngrams"], 0)
        self.assertEqual(out["metrics"]["total_ngrams"], TOTAL_NGRAMS)
        self.assertEqual(out["thresholds"]["ngram_max_overlap"], 0.05)

    def test_fail_overlap_names_first_ngram(self):
        code, out = self._run("--corpus", self._write("c.txt", CORPUS_NEAR), self._write("lyrics.md", LYRICS))
        self.assertEqual((code, out["status"]), (1, "FAIL"))
        self.assertEqual(out["metrics"]["matching_ngrams"], 4)
        v = out["violations"][0]
        self.assertEqual(v["location"], "Verse 1:2")
        self.assertIn("the kettle rattled on the", v["reason"])
        self.assertAlmostEqual(v["observed"], 4 / TOTAL_NGRAMS, places=3)

    def test_ngrams_do_not_span_sections(self):
        # "seat beside me nobody knows" straddles Verse 1 -> Chorus; it must not be a lyric 5-gram.
        corpus = self._write("c.txt", "the seat beside me nobody knows my name\n")
        code, out = self._run("--corpus", corpus, self._write("lyrics.md", LYRICS))
        self.assertEqual(out["status"], "PASS", out)
        self.assertEqual(out["metrics"]["matching_ngrams"], 0)
        grams = [g for g, _ in self.mod.lyric_ngrams([("Verse 1:2", "the seat beside me"), ("Chorus:1", "nobody knows my name")])]
        self.assertEqual(grams, [])
        # lines inside one section still join
        grams = [g for g, _ in self.mod.lyric_ngrams([("Verse 1:1", "the seat beside me"), ("Verse 1:2", "nobody knows my name")])]
        self.assertEqual(len(grams), 4)
        self.assertEqual(grams[0], ("the", "seat", "beside", "me", "nobody"))

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

    def test_boundary_five_words_is_one_ngram(self):
        c = self._write("c.txt", CORPUS_FAR)
        code, out = self._run("--corpus", c, self._write("lyrics.md", "[Verse 1]\nexactly five words right here\n"))
        self.assertEqual((code, out["status"]), (0, "PASS"), out)
        self.assertEqual(out["metrics"]["total_ngrams"], 1)
        # four words split over two lines of one section still joins to 4 -> ERROR
        code, out = self._run("--corpus", c, self._write("lyrics.md", "[Verse 1]\ntwo words\ntwo more\n"))
        self.assertEqual((code, out["status"]), (3, "ERROR"))

    def test_error_bad_threshold_type(self):
        cfg = self._write("config.yml", "originality:\n  ngram_max_overlap: never\n")
        code, out = self._run("--config", cfg, "--corpus", self._write("c.txt", CORPUS_FAR), self._write("lyrics.md", LYRICS))
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

    def test_corpus_relative_paths_never_use_cwd(self):
        # corpus exists relative to the CWD but not relative to the config dir -> treated as missing
        self._write("sub/config.yml", "originality:\n  resemblance_corpus: [near.txt]\n")
        self._write("near.txt", CORPUS_NEAR)
        lyr = self._write("lyrics.md", LYRICS)
        old = os.getcwd()
        os.chdir(self.root)
        try:
            code, out = self._run("--config", "sub/config.yml", lyr)
        finally:
            os.chdir(old)
        self.assertEqual((code, out["status"]), (2, "SKIPPED"), out)
        self.assertEqual(out["metrics"]["missing_files"], 1)

    def test_corpus_relative_to_first_lyric_without_config(self):
        self._write("song/near.txt", CORPUS_NEAR)
        lyr = self._write("song/lyrics.md", LYRICS)
        mod = self.mod
        args = type("A", (), {"corpus": None, "config": None, "paths": [lyr]})()
        got = mod.resolve_corpus(args, {"originality": {"resemblance_corpus": ["near.txt"]}})
        self.assertEqual(got, [mod.gc.norm(self.root / "song" / "near.txt")])

    def test_genre_flag_is_ignored_for_originality(self):
        cfg = self._write("config.yml", "quality:\n  genre_overrides:\n    pop: { ngram_max_overlap: 0.9 }\n"
                                        "originality:\n  ngram_max_overlap: 0.02\n")
        code, out = self._run("--config", cfg, "--genre", "pop", "--corpus", self._write("c.txt", CORPUS_NEAR),
                              self._write("lyrics.md", LYRICS))
        self.assertEqual((out["thresholds"]["ngram_max_overlap"], out["status"]), (0.02, "FAIL"))

    def test_windows_style_path(self):
        c, l = Path(self._write("c.txt", CORPUS_FAR)), Path(self._write("lyrics.md", LYRICS))
        if os.name == "nt":
            c, l = c.as_posix().replace("/", "\\", 1), l.as_posix().replace("/", "\\", 1)
        code, out = self._run("--corpus", str(c), str(l))
        self.assertEqual(out["status"], "PASS", out)


if __name__ == "__main__":
    unittest.main()
