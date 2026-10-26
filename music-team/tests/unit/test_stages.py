"""Wave 3 tests: stages.yml routing data, its validator, and cross-file consistency."""
from __future__ import annotations

import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

PLUGIN = Path(__file__).resolve().parents[2]
SCRIPTS = PLUGIN / "scripts"
REFS = PLUGIN / "skills" / "music-flow" / "references"
STAGES = REFS / "stages.yml"
SONG_TYPES = PLUGIN / "references" / "shared" / "song-types.md"
STAGE_GATES = PLUGIN / "references" / "shared" / "stage-gates.md"
AGENTS = PLUGIN / "agents"

sys.path.insert(0, str(SCRIPTS))
import gate_common as gc  # noqa: E402

# Agents allowed to be absent until their wave lands. Wave 7 removed "adapter".
ALLOWED_MISSING_AGENTS: set[str] = set()


def run_validator(*args: str) -> subprocess.CompletedProcess:
    return subprocess.run([sys.executable, "-I", str(SCRIPTS / "validate_stages.py"), *args],
                          capture_output=True, text=True)


def load_stages() -> dict:
    return gc.load_yaml(STAGES.read_text(encoding="utf-8"))


def routing_table() -> dict[str, list[str]]:
    rows: dict[str, list[str]] = {}
    in_matrix = False
    for line in SONG_TYPES.read_text(encoding="utf-8").splitlines():
        if line.startswith("## "):
            in_matrix = line.strip() == "## Routing matrix"
            continue
        m = re.match(r"^\| `([A-Z_]+)` \|", line)
        if in_matrix and m:
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            rows[m.group(1)] = cells[2:9]  # type, signals, then 7 stage columns
    return rows


def not_yet_built() -> set[str]:
    text = STAGE_GATES.read_text(encoding="utf-8")
    m = re.search(r"^Not-yet-built:(.*)$", text, re.M)
    assert m, "stage-gates.md must list 'Not-yet-built:' scripts"
    return set(re.findall(r"`([a-z_]+\.py)`", m.group(1)))


class ValidatorTests(unittest.TestCase):
    def test_shipped_file_is_valid(self):
        r = run_validator()
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)

    def _tampered(self, old: str, new: str) -> Path:
        text = STAGES.read_text(encoding="utf-8")
        self.assertIn(old, text)
        tmp = Path(tempfile.mkdtemp())
        (tmp / "stages").mkdir()
        for p in (REFS / "stages").glob("*.md"):
            (tmp / "stages" / p.name).write_text("x", encoding="utf-8")
        out = tmp / "stages.yml"
        out.write_text(text.replace(old, new, 1), encoding="utf-8")
        return out

    def test_missing_required_key_fails(self):
        out = self._tampered("    task_type: hook-concept\n", "")
        r = run_validator("--stages", str(out))
        self.assertEqual(r.returncode, 1, r.stdout)
        self.assertIn("task_type", r.stdout)

    def test_bad_enum_fails(self):
        out = self._tampered("max_loops_key: concept", "max_loops_key: bogus")
        r = run_validator("--stages", str(out))
        self.assertEqual(r.returncode, 1, r.stdout)
        self.assertIn("max_loops_key", r.stdout)

    def test_wrong_matrix_width_fails(self):
        out = self._tampered("FULL_SONG: [F, F, F, F, F, F, F]", "FULL_SONG: [F, F, F]")
        self.assertEqual(run_validator("--stages", str(out)).returncode, 1)

    def test_unreadable_input_is_exit_3(self):
        self.assertEqual(run_validator("--stages", "/nonexistent/stages.yml").returncode, 3)


class MatrixTests(unittest.TestCase):
    def test_matrix_matches_song_types_table(self):
        table = routing_table()
        self.assertEqual(len(table), 11)
        matrix = load_stages()["matrix"]
        self.assertEqual(set(matrix), set(table))
        for t, cells in table.items():
            self.assertEqual(matrix[t], cells, t)


class ReferenceTests(unittest.TestCase):
    def setUp(self):
        self.stages = load_stages()["stages"]

    def _agents(self) -> set[str]:
        names: set[str] = set()
        for st in self.stages.values():
            for node in [st, *(st.get("type_variants") or {}).values()]:
                for key in ("agent", "critic_agent"):
                    if node.get(key):
                        names.add(node[key])
        return names

    def test_every_agent_has_a_file_or_is_allowlisted(self):
        agents = self._agents()
        self.assertTrue(agents)
        for name in agents:
            if name in ALLOWED_MISSING_AGENTS:
                continue
            self.assertTrue((AGENTS / f"{name}.md").is_file(), f"agents/{name}.md missing")

    def test_allowlist_has_no_stale_entries(self):
        for name in ALLOWED_MISSING_AGENTS:
            self.assertFalse((AGENTS / f"{name}.md").exists(),
                             f"{name} now exists; remove it from ALLOWED_MISSING_AGENTS")

    def test_every_gate_script_exists_or_is_not_yet_built(self):
        pending = not_yet_built()
        seen = set()
        for sid, st in self.stages.items():
            for gate in st["gates"]:
                script = gate.split()[0]
                seen.add(script)
                self.assertTrue((SCRIPTS / script).is_file() or script in pending,
                                f"{sid}: {script} neither built nor listed as not-yet-built")
        self.assertIn("prosody_check.py", seen)

    def test_not_yet_built_entries_really_absent(self):
        for script in not_yet_built():
            self.assertFalse((SCRIPTS / script).exists(),
                             f"{script} exists; remove it from stage-gates.md section 7")

    def test_roles_and_loop_keys(self):
        for sid, st in self.stages.items():
            if st["max_loops_key"] is not None:
                self.assertIn(st["max_loops_key"], ("concept", "structure", "lyrics", "music", "arrangement", "release"), sid)
            if st["dispatch"] == "agent":
                self.assertTrue(st["agent"], sid)
            self.assertTrue((REFS / st["sub_flow"]).is_file(), sid)


if __name__ == "__main__":
    unittest.main()
