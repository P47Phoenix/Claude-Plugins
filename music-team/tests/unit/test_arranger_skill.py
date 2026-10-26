"""Structural tests for music-team/skills/arranger (W8)."""
from __future__ import annotations

import re
import sys
import unittest
from pathlib import Path

PLUGIN = Path(__file__).resolve().parents[2]
SKILL_DIR = PLUGIN / "skills" / "arranger"
SKILL = SKILL_DIR / "SKILL.md"
REFS = SKILL_DIR / "references"
BLOCKED = PLUGIN / "references" / "shared" / "blocked-targets.txt"

EXPECTED_FM = {
    "name": "arranger",
    "license": "Apache License 2.0 - See repository LICENSE file",
    "model_awareness": "opus-4-7",
    "last_audited": "2026-10-26",
    "pattern_library_version": "4-7-1",
    "model": "sonnet",
    "tier": "B",
    "maintainer": "music-team-leads",
    "fitness_review_due": "2027-01-24",
    "context_budget": "300",
    "allowed-tools": "[Read, Write, Edit, Bash, Agent, Skill]",
}
MANIFEST_SECTIONS = ("## Role -> Reference Mapping", "## Detection Keywords", "## Task Type Routing Table",
                     "## Task Type Instructions", "## Guardrails")
TECHNIQUES = ("energy-mapping", "texture-and-register", "section-contrast", "production-language")
CONTRACTS = ("arrangement-output", "production-brief-output", "cross-role-tasks")


def frontmatter(path: Path) -> dict[str, str]:
    lines = path.read_text(encoding="utf-8").splitlines()
    assert lines[0] == "---"
    end = lines.index("---", 1)
    out = {}
    for line in lines[1:end]:
        k, _, v = line.partition(":")
        out[k.strip()] = v.strip()
    return out


class ArrangerSkillTests(unittest.TestCase):
    def test_frontmatter_exact(self):
        fm = frontmatter(SKILL)
        for key, value in EXPECTED_FM.items():
            self.assertEqual(fm.get(key), value, key)
        desc = fm["description"]
        for trigger in ("arrange this", "arrangement", "instrumentation", "what instruments", "dynamics",
                        "build and drop", "production brief", "production notes", "energy map", "stems",
                        "export MIDI"):
            self.assertIn(trigger, desc)
        self.assertNotIn("phase_1_detector_model", fm)

    def test_line_budget(self):
        self.assertLessEqual(len(SKILL.read_text(encoding="utf-8").splitlines()), 300)

    def test_no_model_ids(self):
        for path in SKILL_DIR.rglob("*.md"):
            self.assertIsNone(re.search(r"claude-[a-z0-9.-]*\d", path.read_text(encoding="utf-8")), str(path))

    def test_body_sections(self):
        text = SKILL.read_text(encoding="utf-8")
        for needle in ("## Phase 1", "## Phase 2", "Role: instrumentation | Task:", "SKILL_LOADED:",
                       "no active pipeline", "arrangement_check.py", "structure_check.py --consistency",
                       "midi_export.py", "## User Commands", "Input Contract", "Output Contract",
                       "ask before proceeding", "`dynamics`", "`production-brief`"):
            self.assertIn(needle, text, needle)

    def test_manifest_sections_and_routing(self):
        manifest = REFS / "roles" / "instrumentation.md"
        text = manifest.read_text(encoding="utf-8")
        self.assertLessEqual(len(text.splitlines()), 150)
        for section in MANIFEST_SECTIONS:
            self.assertIn(section, text, section)
        self.assertIn("| Request Signal | Task Type | References Loaded |", text)
        for task in ("**instrumentation**", "**dynamics**", "**production-brief**"):
            self.assertIn(task, text)
        fm = frontmatter(manifest)
        self.assertEqual((fm["loaded_by"], fm["level"], fm["last_reviewed"]), ("arranger", "L2", "2026-10-26"))
        rows = [l for l in text.splitlines() if l.startswith("| ") and "References Loaded" not in l and "---" not in l]
        for line in rows:
            techs = re.findall(r"([a-z-]+)\.md", line.split("|")[-2]) if line.count("|") >= 4 else []
            self.assertLessEqual(len([t for t in techs if t in TECHNIQUES]), 2, line)

    def test_contracts_and_techniques_exist_with_frontmatter(self):
        for name in CONTRACTS:
            path = REFS / "contracts" / f"{name}.md"
            self.assertTrue(path.exists(), path)
            self.assertLessEqual(len(path.read_text(encoding="utf-8").splitlines()), 150)
            self.assertEqual(frontmatter(path)["level"], "L2")
        for name in TECHNIQUES:
            path = REFS / "techniques" / f"{name}.md"
            self.assertTrue(path.exists(), path)
            self.assertLessEqual(len(path.read_text(encoding="utf-8").splitlines()), 150)
            self.assertEqual(frontmatter(path)["level"], "L3")

    def test_contract_grammar_matches_artifact_formats(self):
        arr = (REFS / "contracts" / "arrangement-output.md").read_text(encoding="utf-8")
        self.assertIn("| section | energy | instruments_in | instruments_out | texture_note |", arr)
        brief = (REFS / "contracts" / "production-brief-output.md").read_text(encoding="utf-8")
        positions = [brief.index(h) for h in ("## Tempo map", "## Vocal treatment", "## Mix priorities",
                                              "## Section notes")]
        self.assertEqual(positions, sorted(positions))

    def test_referenced_paths_exist(self):
        text = SKILL.read_text(encoding="utf-8")
        for rel in set(re.findall(r"`(references/(?:roles|contracts|techniques)/[\w./-]+\.md)`", text)):
            self.assertTrue((SKILL_DIR / rel).exists(), rel)
        for rel in set(re.findall(r"`(references/shared/[\w./<>-]+)`", text)):
            if "<" not in rel:
                self.assertTrue((PLUGIN / rel).exists(), rel)
        for script in ("arrangement_check.py", "midi_export.py", "structure_check.py"):
            self.assertTrue((PLUGIN / "scripts" / script).exists(), script)

    def test_no_blocked_targets(self):
        names = [l.strip() for l in BLOCKED.read_text(encoding="utf-8").splitlines()
                 if l.strip() and not l.startswith("#")]
        for path in SKILL_DIR.rglob("*.md"):
            text = path.read_text(encoding="utf-8")
            for name in names:
                # single-word entries are often ordinary words: match only in listed casing
                flags = re.I if " " in name else 0
                self.assertIsNone(re.search(r"(?<!\w)" + re.escape(name) + r"(?!\w)", text, flags),
                                  f"{name} in {path}")


if __name__ == "__main__":
    unittest.main()
