"""Structure tests for the lyricist worker skill (Wave 6)."""
from __future__ import annotations

import re
import unittest
from pathlib import Path

PLUGIN = Path(__file__).resolve().parents[2]
SKILL_DIR = PLUGIN / "skills" / "lyricist"
SKILL = SKILL_DIR / "SKILL.md"
FIXTURE = PLUGIN / "tests" / "fixtures" / "songs" / "AUGMENT_LYRICS"
ROLES = ["hook-writer", "verse-writer", "lyric-editor", "augmenter"]
CONTRACTS = ["concept-output", "lyrics-output", "revision-output", "augment-output", "cross-role-tasks"]
TECHNIQUES = ["hook-craft", "prosody-and-stress", "rhyme-schemes", "imagery-and-specificity",
              "section-roles", "editing-passes"]
MANIFEST_SECTIONS = ["## Role -> Reference Mapping", "## Detection Keywords", "## Task Type Routing Table",
                     "## Task Type Instructions", "## Guardrails"]
EXPECTED_FRONTMATTER = {
    "name": "lyricist",
    "license": "Apache License 2.0 - See repository LICENSE file",
    "model_awareness": "opus-4-7",
    "last_audited": "2026-10-26",
    "pattern_library_version": "4-7-1",
    "model": "sonnet",
    "phase_1_detector_model": "haiku",
    "tier": "B",
    "maintainer": "music-team-leads",
    "fitness_review_due": "2027-01-24",
    "context_budget": "300",
    "allowed-tools": "[Read, Write, Edit, Bash, Agent, Skill]",
}
TRIGGERS = ["write lyrics", "chorus lyrics", "verse", "hook line", "rhyme this", "rewrite this lyric",
            "tighten these lyrics", "add a verse", "write a bridge for my song", "extend my lyrics",
            "more verses in the same voice", "pre-chorus"]


def frontmatter(path: Path) -> dict:
    m = re.match(r"---\n(.*?)\n---\n", path.read_text(encoding="utf-8"), re.S)
    out = {}
    if m:
        for line in m.group(1).splitlines():
            k, _, v = line.partition(":")
            out[k.strip()] = v.strip()
    return out


def blocked_targets() -> list[str]:
    text = (PLUGIN / "references" / "shared" / "blocked-targets.txt").read_text(encoding="utf-8")
    return [l.strip() for l in text.splitlines() if l.strip() and not l.lstrip().startswith("#")]


class LyricistSkillTests(unittest.TestCase):
    def test_frontmatter(self):
        fm = frontmatter(SKILL)
        for key, want in EXPECTED_FRONTMATTER.items():
            self.assertEqual(fm.get(key), want, key)
        desc = fm.get("description", "")
        for phrase in TRIGGERS:
            self.assertIn(phrase, desc, f"trigger {phrase!r} missing from description")

    def test_line_budget(self):
        n = len(SKILL.read_text(encoding="utf-8").splitlines())
        self.assertLessEqual(n, 300, f"SKILL.md is {n} lines")

    def test_phase_structure(self):
        text = SKILL.read_text(encoding="utf-8")
        for needle in ["## Phase 1", "## Phase 2", "Role: [ROLE] | Task: [TASK_TYPE] | References:",
                       "SKILL_LOADED:", "No active pipeline", "prosody_check.py",
                       "rhyme_check.py", "cliche_scan.py", "User Commands", "user_asserts_original_input",
                       "public_domain"]:
            self.assertIn(needle, text, needle)
        for role in ROLES:
            self.assertIn(f"references/roles/{role}.md", text)

    def test_role_manifests(self):
        for role in ROLES:
            path = SKILL_DIR / "references" / "roles" / f"{role}.md"
            self.assertTrue(path.exists(), path)
            text = path.read_text(encoding="utf-8")
            fm = frontmatter(path)
            self.assertEqual(fm.get("loaded_by"), "lyricist")
            self.assertEqual(fm.get("level"), "L2")
            self.assertIn("last_reviewed", fm)
            for section in MANIFEST_SECTIONS:
                self.assertIn(section, text, f"{role}: {section}")
            self.assertIn("| Request Signal | Task Type | References Loaded |", text)

    def test_augmenter_manifest_content(self):
        text = (SKILL_DIR / "references" / "roles" / "augmenter.md").read_text(encoding="utf-8")
        for needle in ["<!-- new -->", "Kept:", "Added:", "verbatim", "clause 4", "provenance"]:
            self.assertIn(needle, text.replace("Provenance", "provenance"), needle)

    def test_contracts_and_techniques_exist(self):
        for name in CONTRACTS:
            path = SKILL_DIR / "references" / "contracts" / f"{name}.md"
            self.assertTrue(path.exists(), path)
            self.assertEqual(frontmatter(path).get("loaded_by"), "lyricist")
        for name in TECHNIQUES:
            path = SKILL_DIR / "references" / "techniques" / f"{name}.md"
            self.assertTrue(path.exists(), path)
            fm = frontmatter(path)
            self.assertEqual(fm.get("loaded_by"), "lyricist")
            self.assertEqual(fm.get("level"), "L3")

    def test_reference_files_within_cap(self):
        for path in (SKILL_DIR / "references").rglob("*.md"):
            n = len(path.read_text(encoding="utf-8").splitlines())
            self.assertLessEqual(n, 150, f"{path.name}: {n} lines")

    def test_contract_grammars(self):
        concept = (SKILL_DIR / "references/contracts/concept-output.md").read_text(encoding="utf-8")
        for key in ["title", "hook_line", "motif", "central_image", "arc", "title_rationale"]:
            self.assertIn(f"`{key}`", concept)
        lyrics = (SKILL_DIR / "references/contracts/lyrics-output.md").read_text(encoding="utf-8")
        for needle in ["meter_spec", "rhyme_scheme", "[Verse 1]", "Pre-Chorus N", "Bridge"]:
            self.assertIn(needle, lyrics)
        augment = (SKILL_DIR / "references/contracts/augment-output.md").read_text(encoding="utf-8")
        for needle in ["<!-- new -->", "## Augmentation", "Kept:", "Added:", "Meter check:", "Rhyme check:"]:
            self.assertIn(needle, augment)

    def test_every_referenced_path_exists(self):
        text = SKILL.read_text(encoding="utf-8")
        found = set(re.findall(r"`(references/[A-Za-z0-9_./-]+\.(?:md|json|txt))`", text))
        self.assertTrue(found)
        for rel in sorted(found):
            if "<" in rel:
                continue
            base = PLUGIN if rel.startswith("references/shared/") else SKILL_DIR
            self.assertTrue((base / rel).exists(), f"{rel} named in SKILL.md does not exist")

    def test_no_blocked_targets_or_model_ids(self):
        targets = blocked_targets()
        for path in SKILL_DIR.rglob("*.md"):
            text = path.read_text(encoding="utf-8")
            # the mandated marker is exempt from the blocked-target scan
            text = text.replace("<!-- memory-lessons -->", "")
            self.assertNotRegex(text, r"claude-[a-z0-9.-]*4-\d", f"{path.name}: dated model id")
            self.assertNotIn("claude-", text, f"{path.name}: model id")
            for t in targets:
                pat = r"(?<![A-Za-z0-9])" + re.escape(t) + r"(?![A-Za-z0-9])"
                self.assertIsNone(re.search(pat, text, re.I), f"{path.name}: blocked target {t!r}")


class AugmentFixtureTests(unittest.TestCase):
    def setUp(self):
        self.lyrics = (FIXTURE / "lyrics.md").read_text(encoding="utf-8")
        self.brief = (FIXTURE / "brief.md").read_text(encoding="utf-8")

    def test_files_present(self):
        for name in ["brief.md", "structure.md", "lyrics.md", "expected.json"]:
            self.assertTrue((FIXTURE / name).exists(), name)

    def test_markers(self):
        self.assertIn("<!-- new -->", self.lyrics)
        self.assertEqual(self.lyrics.count("<!-- new -->"), 1)
        self.assertIn("## Augmentation", self.lyrics)
        for label in ["Kept:", "Added:", "Meter check:", "Rhyme check:"]:
            self.assertIn(label, self.lyrics)

    def test_provenance(self):
        fm = frontmatter(FIXTURE / "brief.md")
        self.assertEqual(fm.get("song_type"), "AUGMENT_LYRICS")
        ok = fm.get("user_asserts_original_input") == "true" or (
            fm.get("public_domain") == "true" and fm.get("public_domain_source"))
        self.assertTrue(ok)

    def test_source_lines_verbatim_in_order(self):
        m = re.search(r"## Supplied input\s+```text\n(.*?)```", self.brief, re.S)
        self.assertIsNotNone(m)
        source = [l.strip() for l in m.group(1).splitlines() if l.strip() and not l.startswith("[")]
        self.assertTrue(source)
        body = [l.strip() for l in self.lyrics.splitlines()
                if l.strip() and not l.startswith(("[", "#"))]
        it = iter(body)
        for line in source:
            self.assertTrue(any(line == b for b in it), f"source line missing or out of order: {line!r}")

    def test_new_section_follows_marker(self):
        m = re.search(r"\[Bridge\]\n# <!-- new -->\n((?:[^\n#\[][^\n]*\n){4})", self.lyrics)
        self.assertIsNotNone(m, "marker must sit under the new tag followed by four lyric lines")


if __name__ == "__main__":
    unittest.main()
