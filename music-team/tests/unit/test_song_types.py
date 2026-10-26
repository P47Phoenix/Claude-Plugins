"""Routing contract tests for the song-type fixtures (Wave 2).

Detection is prose-only (no Python classifier), so these tests check the
fixture shapes and that song-types.md / config-schema.md / prompt-allowances.json
carry the new types, in priority order.
"""
from __future__ import annotations

import json
import re
import unittest
from pathlib import Path

PLUGIN = Path(__file__).resolve().parents[2]
SHARED = PLUGIN / "references" / "shared"
FIXTURES = PLUGIN / "tests" / "fixtures"

PRIORITY = ["PARODY_ADAPT", "REVISE", "THEORY", "ADAPT_GENRE", "AUGMENT_LYRICS", "REWRITE",
            "TOPLINE", "INSTRUMENTAL", "JINGLE", "LYRICS_ONLY", "FULL_SONG"]
NEW = ["THEORY", "ADAPT_GENRE", "AUGMENT_LYRICS"]


def frontmatter(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    m = re.match(r"---\n(.*?)\n---\n", text, re.S)
    out = {}
    if m:
        for line in m.group(1).splitlines():
            k, _, v = line.partition(":")
            out[k.strip()] = v.strip()
    return out


class SongTypeTests(unittest.TestCase):
    def test_priority_sentence_lists_all_types_in_order(self):
        text = (SHARED / "song-types.md").read_text(encoding="utf-8")
        flat = " ".join(text.split())
        self.assertIn("this order wins: " + ", ".join(PRIORITY) + ".", flat)

    def test_sections_and_matrix_rows_exist(self):
        text = (SHARED / "song-types.md").read_text(encoding="utf-8")
        for t in NEW:
            self.assertIn(f"### {t}\n", text)
            self.assertRegex(text, rf"\| `{t}` \|")

    def test_matrix_stage_pattern(self):
        text = (SHARED / "song-types.md").read_text(encoding="utf-8")
        want = {"THEORY": "F | - | - | - | - | - | -", "ADAPT_GENRE": "F | I | I | L | I | I | F",
                "AUGMENT_LYRICS": "F | I | I | L | - | - | L"}
        for t, cells in want.items():
            row = next(l for l in text.splitlines() if l.startswith(f"| `{t}` |"))
            self.assertIn(f"| {cells} |", row, t)

    def test_force_type_enum(self):
        text = (SHARED / "config-schema.md").read_text(encoding="utf-8")
        for t in NEW:
            self.assertGreaterEqual(text.count(t), 2, t)
        self.assertIn("adaptation:", text)
        self.assertIn("max_changed_elements", text)

    def test_allowances(self):
        roles = json.loads((SHARED / "prompt-allowances.json").read_text(encoding="utf-8"))["roles"]
        self.assertEqual(roles["lyric-adapter"], {"genres": 2})
        self.assertEqual(roles["music-adapter"], {"genres": 2})
        self.assertEqual(roles["theorist"], {"genres": 0, "techniques": 3})
        self.assertEqual(roles["augmenter"], {"genres": 1, "techniques": 2})

    def test_brief_fixtures_match_expected(self):
        exp = json.loads((FIXTURES / "briefs" / "expected.json").read_text(encoding="utf-8"))
        for t in PRIORITY:
            self.assertIn(t, exp)
            self.assertEqual(exp[t]["song_type"], t)
        for t in NEW:
            self.assertEqual(frontmatter(FIXTURES / "briefs" / f"{t}.md")["song_type"], t)

    def test_provenance_paths_covered(self):
        adapt = frontmatter(FIXTURES / "briefs" / "ADAPT_GENRE.md")
        aug = frontmatter(FIXTURES / "briefs" / "AUGMENT_LYRICS.md")
        self.assertEqual(adapt["user_asserts_original_input"], "true")
        self.assertEqual(aug["public_domain"], "true")
        self.assertTrue(aug["public_domain_source"])
        self.assertTrue(adapt["target_genre"] and adapt["source_genre"])

    def test_negative_routing_cases(self):
        want = {"adapt-named-target": ("PARODY_ADAPT", True), "adapt-no-provenance": ("ADAPT_GENRE", True),
                "augment-fix-only": ("REWRITE", False)}
        for case, (song_type, refused) in want.items():
            d = FIXTURES / "negative" / case
            r = json.loads((d / "expected.json").read_text(encoding="utf-8"))["routing"]
            self.assertEqual((r["song_type"], r["refused"]), (song_type, refused), case)
            self.assertTrue((d / "brief.md").exists())
        fm = frontmatter(FIXTURES / "negative" / "adapt-no-provenance" / "brief.md")
        self.assertNotEqual(fm["user_asserts_original_input"], "true")
        self.assertNotEqual(fm["public_domain"], "true")


if __name__ == "__main__":
    unittest.main()
