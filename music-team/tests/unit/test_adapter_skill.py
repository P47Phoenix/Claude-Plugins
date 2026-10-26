"""Structure tests for the adapter skill and its named agent (Wave 7)."""
from __future__ import annotations

import json
import re
import sys
import unittest
from pathlib import Path

PLUGIN = Path(__file__).resolve().parents[2]
SKILL_DIR = PLUGIN / "skills" / "adapter"
SKILL = SKILL_DIR / "SKILL.md"
AGENT = PLUGIN / "agents" / "adapter.md"
SHARED = PLUGIN / "references" / "shared"

sys.path.insert(0, str(PLUGIN / "scripts"))
import gate_common as gc  # noqa: E402

ROLES = ("lyric-adapter", "music-adapter")
CONTRACTS = ("lyric-adapt-output", "music-adapt-output", "arrangement-adapt-output", "adaptation-report",
             "cross-role-tasks")
TECHNIQUES = ("feel-conversion", "reharmonization-moves", "lyric-refit")
MANIFEST_SECTIONS = ("## Role -> Reference Mapping", "## Detection Keywords", "## Task Type Routing Table",
                     "## Task Type Instructions", "## Guardrails")


def frontmatter(path: Path) -> dict:
    fm, _ = gc.parse_frontmatter(path.read_text(encoding="utf-8"))
    return fm


class SkillTests(unittest.TestCase):
    def setUp(self):
        self.text = SKILL.read_text(encoding="utf-8")
        self.fm = frontmatter(SKILL)

    def test_frontmatter_values(self):
        want = {
            "name": "adapter", "license": "Apache License 2.0 - See repository LICENSE file",
            "model_awareness": "opus-4-7", "last_audited": "2026-10-26", "pattern_library_version": "4-7-1",
            "model": "sonnet", "phase_1_detector_model": "haiku", "tier": "B", "maintainer": "music-team-leads",
            "fitness_review_due": "2027-01-24", "context_budget": 300,
        }
        for key, value in want.items():
            self.assertEqual(str(self.fm.get(key)), str(value), key)
        self.assertEqual(self.fm.get("allowed-tools"), ["Read", "Write", "Edit", "Bash", "Agent", "Skill"])

    def test_description_triggers(self):
        desc = self.fm["description"]
        for phrase in ("adapt my song to", "turn my ballad into", "convert this to", "make it bossa nova",
                       "cross-genre", "reharmonize for", "re-fit these lyrics to", "genre adaptation",
                       "what would change if this were"):
            self.assertIn(phrase, desc)

    def test_line_budget(self):
        self.assertLessEqual(len(self.text.splitlines()), 300)

    def test_required_body_sections(self):
        for heading in ("## Phase 1: Detection", "## Phase 2: Sub-Agent Invocation", "## JSON I/O Contract",
                        "## User Commands", "### Pipeline Invocation", "### Standalone Invocation"):
            self.assertIn(heading, self.text)
        self.assertIn("SKILL_LOADED:", self.text)
        self.assertIn("No active pipeline", self.text)
        self.assertIn("Roles:", self.text)
        for cmd in ("`adapt <genre>`", "`report`", "`diff`"):
            self.assertIn(cmd, self.text)

    def test_four_step_spawn_text(self):
        for step in ("1. Detect the role(s)", "2. Read **only**", "3. Spawn a sub-agent using the `Agent` tool",
                     "4. Return the sub-agent's output directly"):
            self.assertIn(step, self.text)

    def test_no_model_ids_in_skill_tree(self):
        for p in [SKILL, AGENT, *SKILL_DIR.rglob("*.md")]:
            self.assertNotIn("claude-", p.read_text(encoding="utf-8"), str(p))

    def test_referenced_paths_exist(self):
        refs = set(re.findall(r"`(references/[\w./-]+\.md)`", self.text))
        self.assertTrue(refs)
        for ref in refs:
            self.assertTrue((SKILL_DIR / ref).is_file(), f"{ref} referenced but missing")

    def test_shared_paths_exist(self):
        for rel in re.findall(r"`music-team/(references/shared/[\w./-]+\.md)`", self.text):
            self.assertTrue((PLUGIN / rel).is_file(), rel)
        self.assertTrue((PLUGIN / "scripts" / "adapt_check.py").is_file())

    def test_no_blocked_targets_in_skill_tree(self):
        names = [l for l in gc.load_list_file(SHARED / "blocked-targets.txt") if len(l) >= 4]
        self.assertGreater(len(names), 50)
        files = [SKILL, AGENT, *SKILL_DIR.rglob("*.md")]
        for p in files:
            text = p.read_text(encoding="utf-8")
            for name in names:
                # single-word entries are also common English words: match them case-sensitively
                flags = 0 if " " not in name else re.I
                if re.search(r"(?<![\w-])" + re.escape(name) + r"(?![\w-])", text, flags):
                    self.fail(f"blocked target {name!r} appears in {p}")


class ManifestTests(unittest.TestCase):
    def test_role_manifests(self):
        for role in ROLES:
            path = SKILL_DIR / "references" / "roles" / f"{role}.md"
            with self.subTest(role=role):
                text = path.read_text(encoding="utf-8")
                self.assertLessEqual(len(text.splitlines()), 150)
                fm = frontmatter(path)
                self.assertEqual((fm.get("loaded_by"), fm.get("level"), str(fm.get("last_reviewed"))),
                                 ("adapter", "L2", "2026-10-26"))
                for heading in MANIFEST_SECTIONS:
                    self.assertIn(heading, text)
                self.assertIn("| Request Signal | Task Type | References Loaded |", text)

    def test_manifest_tasks_match_stages_yml(self):
        stages = gc.load_yaml((PLUGIN / "skills" / "music-flow" / "references" / "stages.yml").read_text(encoding="utf-8"))
        wanted: dict[str, set[str]] = {r: set() for r in ROLES}
        for st in stages["stages"].values():
            variant = (st.get("type_variants") or {}).get("ADAPT_GENRE")
            for node in ([st] if st.get("only_types") else []) + ([variant] if variant else []):
                if node.get("agent") == "adapter":
                    wanted[node["role"]].add(node["task_type"])
        self.assertTrue(all(wanted.values()), wanted)
        for role, tasks in wanted.items():
            text = (SKILL_DIR / "references" / "roles" / f"{role}.md").read_text(encoding="utf-8")
            for task in tasks:
                self.assertIn(f"**{task}**", text, f"{role} lacks task {task}")

    def test_manifest_references_exist(self):
        for role in ROLES:
            text = (SKILL_DIR / "references" / "roles" / f"{role}.md").read_text(encoding="utf-8")
            for ref in re.findall(r"((?:contracts|techniques)/[\w-]+\.md)", text):
                self.assertTrue((SKILL_DIR / "references" / ref).is_file(), f"{role}: {ref}")

    def test_allowance_two_genres(self):
        allowances = json.loads((SHARED / "prompt-allowances.json").read_text(encoding="utf-8"))
        for role in ROLES:
            self.assertEqual(allowances["roles"][role]["genres"], 2)


class ContractAndTechniqueTests(unittest.TestCase):
    def test_contracts(self):
        for name in CONTRACTS:
            path = SKILL_DIR / "references" / "contracts" / f"{name}.md"
            with self.subTest(contract=name):
                text = path.read_text(encoding="utf-8")
                self.assertLessEqual(len(text.splitlines()), 150)
                fm = frontmatter(path)
                self.assertEqual((fm.get("loaded_by"), fm.get("level")), ("adapter", "L2"))
                if name.endswith("-output"):
                    self.assertIn("## Adaptation notes", text)
                    self.assertIn("# Kept:", text)
                    self.assertIn("# Changed:", text)
                    self.assertIn("SKILL_LOADED:", text)

    def test_report_contract_grammar(self):
        text = (SKILL_DIR / "references" / "contracts" / "adaptation-report.md").read_text(encoding="utf-8")
        for needle in ("song_type: ADAPT_GENRE", "## Kept", "## Changed", "| Element | Source | Target | Why |",
                       "## Lyric re-fit", "## Risks", "adaptation.max_changed_elements", "adapt_check.py"):
            self.assertIn(needle, text)

    def test_techniques(self):
        for name in TECHNIQUES:
            path = SKILL_DIR / "references" / "techniques" / f"{name}.md"
            with self.subTest(technique=name):
                self.assertLessEqual(len(path.read_text(encoding="utf-8").splitlines()), 150)
                fm = frontmatter(path)
                self.assertEqual((fm.get("loaded_by"), fm.get("level")), ("adapter", "L3"))


class AgentTests(unittest.TestCase):
    def test_agent_shell(self):
        self.assertTrue(AGENT.is_file())
        fm = frontmatter(AGENT)
        self.assertEqual(fm.get("name"), "adapter")
        self.assertEqual(fm.get("model"), "sonnet")
        self.assertEqual(fm.get("tools"), "Read, Write, Edit, Bash, Glob, Grep")
        self.assertTrue(fm.get("description"))
        text = AGENT.read_text(encoding="utf-8")
        for needle in ("<!-- originality-policy -->", "<!-- memory-lessons -->", "SKILL_LOADED:", "STATUS: DONE | BLOCKED",
                       "SUMMARY: one sentence, max 200 characters"):
            self.assertIn(needle, text)

    def test_agent_has_no_craft_content(self):
        body = AGENT.read_text(encoding="utf-8")
        for word in ("syllable", "reharmon", "bossa", "tempo"):
            self.assertNotIn(word, body.lower())


if __name__ == "__main__":
    unittest.main()
