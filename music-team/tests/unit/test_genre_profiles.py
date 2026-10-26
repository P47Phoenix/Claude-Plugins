"""Structure and hygiene tests for the shared genre profiles (Wave 4).

Each profile under references/shared/genres/ must stay within the 100-line cap,
carry the required frontmatter, expose the six H2 sections in order (so
dispatchers can slice by heading), avoid blocked style targets, and use
aliases that are unique across all profiles.
"""
from __future__ import annotations

import re
import unittest
from pathlib import Path

PLUGIN = Path(__file__).resolve().parents[2]
GENRES = PLUGIN / "references" / "shared" / "genres"
BLOCKED = PLUGIN / "references" / "shared" / "blocked-targets.txt"

SLUGS = ["folk", "pop", "rock", "blues", "jazz", "bossa-nova", "country",
         "hip-hop", "rnb", "electronic", "musical-theatre", "gospel"]
HEADINGS = ["Identity", "Lyric", "Harmony", "Rhythm", "Arrangement", "Adaptation notes"]
REQUIRED_KEYS = ["loaded_by", "level", "last_reviewed", "genre", "aliases"]
LINE_CAP = 100


def frontmatter(text: str) -> dict:
    m = re.match(r"---\n(.*?)\n---\n", text, re.S)
    if not m:
        return {}
    out = {}
    for line in m.group(1).splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            out[k.strip()] = v.strip()
    return out


def parse_aliases(raw: str) -> list[str]:
    inner = raw.strip().strip("[]")
    return [a.strip().strip("\"'").lower() for a in inner.split(",") if a.strip()]


def blocked_patterns() -> list[re.Pattern]:
    pats = []
    for line in BLOCKED.read_text(encoding="utf-8").splitlines():
        name = line.strip()
        if not name or name.startswith("#"):
            continue
        pats.append(re.compile(r"(?<!\w)" + re.escape(name) + r"(?!\w)", re.I))
    return pats


class GenreProfileTests(unittest.TestCase):
    def test_all_profiles_exist(self):
        for slug in SLUGS:
            self.assertTrue((GENRES / f"{slug}.md").is_file(), slug)

    def test_line_cap(self):
        for slug in SLUGS:
            n = len((GENRES / f"{slug}.md").read_text(encoding="utf-8").splitlines())
            self.assertLessEqual(n, LINE_CAP, f"{slug}: {n} lines")

    def test_frontmatter(self):
        for slug in SLUGS:
            fm = frontmatter((GENRES / f"{slug}.md").read_text(encoding="utf-8"))
            for key in REQUIRED_KEYS:
                self.assertIn(key, fm, f"{slug}: missing {key}")
            self.assertEqual(fm["genre"], slug)
            self.assertEqual(fm["level"], "L3")

    def test_h2_headings_in_order(self):
        for slug in SLUGS:
            text = (GENRES / f"{slug}.md").read_text(encoding="utf-8")
            found = re.findall(r"^## (.+?)\s*$", text, re.M)
            self.assertEqual(found, HEADINGS, slug)

    def test_no_blocked_targets(self):
        pats = blocked_patterns()
        self.assertTrue(pats)
        for slug in SLUGS:
            text = (GENRES / f"{slug}.md").read_text(encoding="utf-8")
            for pat in pats:
                self.assertIsNone(pat.search(text), f"{slug}: blocked term {pat.pattern}")

    def test_aliases_unique(self):
        seen: dict[str, str] = {}
        for slug in SLUGS:
            fm = frontmatter((GENRES / f"{slug}.md").read_text(encoding="utf-8"))
            aliases = parse_aliases(fm["aliases"])
            self.assertTrue(aliases, slug)
            for a in aliases:
                self.assertNotIn(a, seen, f"alias {a!r} in {slug} and {seen.get(a)}")
                seen[a] = slug


if __name__ == "__main__":
    unittest.main()
