"""Structure tests for the song-critic worker skill (Wave 9)."""
from __future__ import annotations

import json
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

PLUGIN = Path(__file__).resolve().parents[2]
SKILL_DIR = PLUGIN / "skills" / "song-critic"
SKILL = SKILL_DIR / "SKILL.md"
SHARED = PLUGIN / "references" / "shared"
ROLES = ["judges", "adaptation-fidelity", "listener-panel", "challenger"]
JUDGE_ROLES = ["hook-judge", "prosody-judge", "music-judge", "structure-judge"]
CONTRACTS = ["critique", "panel-report", "challenge-report"]
RUBRICS = ["hook", "prosody", "music", "structure", "adaptation-fidelity"]
PERSONAS = ["casual-radio-listener", "songwriter-peer", "genre-devotee"]
MANIFEST_SECTIONS = ["## Role -> Reference Mapping", "## Detection Keywords", "## Task Type Routing Table",
                     "## Task Type Instructions", "## Guardrails"]
EXPECTED_FRONTMATTER = {
    "name": "song-critic",
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
TRIGGERS = ["critique this song", "review my lyrics", "judge the chorus", "listener panel", "challenge this song",
            "is this original", "how faithful is this adaptation"]


def frontmatter(path: Path) -> dict:
    m = re.match(r"---\n(.*?)\n---\n", path.read_text(encoding="utf-8"), re.S)
    out = {}
    if m:
        for line in m.group(1).splitlines():
            k, _, v = line.partition(":")
            out[k.strip()] = v.strip()
    return out


def blocked_hits(text: str) -> list[str]:
    """Hook semantics: single-word entries case-sensitive, multi-word case-insensitive."""
    lines = (SHARED / "blocked-targets.txt").read_text(encoding="utf-8").splitlines()
    text = text.replace("<!-- memory-lessons -->", "")
    hits = []
    for t in (l.strip() for l in lines if l.strip() and not l.lstrip().startswith("#")):
        pat = r"(?<![A-Za-z0-9])" + re.escape(t) + r"(?![A-Za-z0-9])"
        if re.search(pat, text, 0 if " " not in t else re.I):
            hits.append(t)
    return hits


class SongCriticSkillTests(unittest.TestCase):
    def test_frontmatter(self):
        fm = frontmatter(SKILL)
        for key, want in EXPECTED_FRONTMATTER.items():
            self.assertEqual(fm.get(key), want, key)
        self.assertNotIn("phase_1_detector_model", fm)
        for phrase in TRIGGERS:
            self.assertIn(phrase, fm.get("description", ""), phrase)

    def test_line_budget(self):
        n = len(SKILL.read_text(encoding="utf-8").splitlines())
        self.assertLessEqual(n, 300, f"SKILL.md is {n} lines")

    def test_phase_structure(self):
        text = SKILL.read_text(encoding="utf-8")
        for needle in ["## Phase 1", "## Phase 2", "Role: [ROLE] | Task: [TASK_TYPE] | References:",
                       "SKILL_LOADED:", "No active pipeline", "challenge_gate.py", "User Commands",
                       "<!-- originality-policy -->", "<!-- memory-lessons -->", "user_asserts_original_input",
                       "public_domain", "clean context"]:
            self.assertIn(needle, text.replace("Clean context", "clean context"), needle)
        for role in JUDGE_ROLES + ["adaptation-fidelity", "listener-panel", "challenger"]:
            self.assertIn(role, text, role)
        for role in ROLES:
            self.assertIn(f"references/roles/{role}.md", text)

    def test_role_manifests(self):
        for role in ROLES:
            path = SKILL_DIR / "references" / "roles" / f"{role}.md"
            text = path.read_text(encoding="utf-8")
            fm = frontmatter(path)
            self.assertEqual(fm.get("loaded_by"), "song-critic")
            self.assertEqual(fm.get("level"), "L2")
            self.assertIn("last_reviewed", fm)
            for section in MANIFEST_SECTIONS:
                self.assertIn(section, text, f"{role}: {section}")
            self.assertIn("| Request Signal | Task Type | References Loaded |", text)
        judges = (SKILL_DIR / "references/roles/judges.md").read_text(encoding="utf-8")
        for r in JUDGE_ROLES:
            self.assertIn(f"**{r}**", judges)

    def test_role_names_match_stages_yml(self):
        stages = (PLUGIN / "skills/music-flow/references/stages.yml").read_text(encoding="utf-8")
        critics = set(re.findall(r"critic_role: ([a-z-]+)", stages)) - {"null"}
        self.assertEqual(critics, set(JUDGE_ROLES + ["adaptation-fidelity"]))
        for role in ("listener-panel", "challenger"):
            self.assertIn(f"role: {role}", stages)

    def test_contracts_rubrics_personas(self):
        for kind, names, level in [("contracts", CONTRACTS, "L2"), ("rubrics", RUBRICS, "L3"),
                                   ("personas", PERSONAS, "L3")]:
            for name in names:
                path = SKILL_DIR / "references" / kind / f"{name}.md"
                self.assertTrue(path.exists(), path)
                fm = frontmatter(path)
                self.assertEqual(fm.get("loaded_by"), "song-critic")
                self.assertEqual(fm.get("level"), level)
        for name in RUBRICS:
            text = (SKILL_DIR / f"references/rubrics/{name}.md").read_text(encoding="utf-8")
            rows = [l for l in text.splitlines() if l.startswith("| ") and "---" not in l]
            self.assertGreaterEqual(len(rows) - 1, 5, f"{name}: needs five criteria")
        for name in PERSONAS:
            text = (SKILL_DIR / f"references/personas/{name}.md").read_text(encoding="utf-8")
            self.assertIn(f"name: {name}", text)

    def test_reference_files_within_cap(self):
        for path in (SKILL_DIR / "references").rglob("*.md"):
            n = len(path.read_text(encoding="utf-8").splitlines())
            self.assertLessEqual(n, 150, f"{path.name}: {n} lines")

    def test_allowances_cover_every_role(self):
        roles = json.loads((SHARED / "prompt-allowances.json").read_text(encoding="utf-8"))["roles"]
        for r in JUDGE_ROLES + ["adaptation-fidelity", "listener-panel", "challenger"]:
            self.assertIn(r, roles, r)
        self.assertEqual(roles["listener-panel"]["personas"], 3)
        self.assertEqual(roles["challenger"]["shared"], 3)
        self.assertGreaterEqual(roles["adaptation-fidelity"]["rubrics"], 1)

    def test_challenge_contract_example_parses_in_gate(self):
        contract = (SKILL_DIR / "references/contracts/challenge-report.md").read_text(encoding="utf-8")
        report = re.search(r"```markdown\n(## Findings.*?)```", contract, re.S).group(1)
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / "challenge-report.md"
            p.write_text(report, encoding="utf-8")
            r = subprocess.run([sys.executable, "-I", str(PLUGIN / "scripts/challenge_gate.py"), "--json", str(p)],
                               capture_output=True, text=True)
        res = json.loads(r.stdout)
        self.assertEqual(r.returncode, 1)  # the example holds a BLOCKER row
        self.assertEqual(res["metrics"]["blocker"], 1)
        self.assertEqual(res["metrics"]["major"], 1)
        self.assertEqual(res["metrics"]["minor"], 1)

    def test_challenger_manifest_clause_four_blocker(self):
        text = (SKILL_DIR / "references/roles/challenger.md").read_text(encoding="utf-8")
        for needle in ["clause 4", "BLOCKER", "MAJOR", "MINOR", "Clean context", "never receives a critique".capitalize()]:
            self.assertIn(needle, text, needle)

    def test_panel_contract_grammar(self):
        text = (SKILL_DIR / "references/contracts/panel-report.md").read_text(encoding="utf-8")
        for needle in ["verdict:", "top_note:", "question:", "majority:", "200 characters"]:
            self.assertIn(needle, text, needle)

    def test_every_referenced_path_exists(self):
        text = SKILL.read_text(encoding="utf-8")
        found = set(re.findall(r"`(references/[A-Za-z0-9_./-]+\.(?:md|json|txt))`", text))
        self.assertTrue(found)
        for rel in sorted(found):
            base = PLUGIN if rel.startswith("references/shared/") else SKILL_DIR
            self.assertTrue((base / rel).exists(), rel)

    def test_no_blocked_targets_or_model_ids(self):
        for path in SKILL_DIR.rglob("*.md"):
            text = path.read_text(encoding="utf-8")
            self.assertNotIn("claude-", text, f"{path.name}: model id")
            self.assertEqual(blocked_hits(text), [], path.name)


if __name__ == "__main__":
    unittest.main()
