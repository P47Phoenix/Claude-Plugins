#!/usr/bin/env python3
"""SubagentStop hook: advisory gate summary for a stopping music-team agent.

Usage: subagent_gate.py --agent lyricist|composer|arranger|song-critic|adapter

Locates the run through ``.song/active`` (slug) and ``.song/<slug>/``, runs the gate scripts
that belong to the agent against the artifacts present, and reports their statuses in a
``systemMessage``. Advisory only: always exit 0. The orchestrator makes the gate decision
(stage-gates.md section 4). With no active run it exits silently.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _hook_common as hc  # noqa: E402

SCRIPTS = hc.PLUGIN_ROOT / "scripts"
TIMEOUT = 20


def find_root(start: Path) -> Path | None:
    for cand in [start, *list(start.parents)[:4]]:
        if (cand / ".song" / "active").is_file():
            return cand
    return None


def newest(d: Path, names: list[str]) -> str | None:
    present = [n for n in names if (d / n).is_file()]
    return max(present, key=lambda n: (d / n).stat().st_mtime) if present else None


def plan(agent: str, d: Path) -> list[tuple[str, list[str]]]:
    """Return [(label, argv-after-script-name-with-script first)] for the artifacts present."""
    has = lambda n: (d / n).is_file()  # noqa: E731
    out: list[tuple[str, list[str]]] = []
    if agent == "lyricist":
        which = newest(d, ["concept.md", "lyrics.md"])
        if which == "lyrics.md":
            out = [("prosody_check", ["prosody_check.py", "lyrics.md", "structure.md", "brief.md"]),
                   ("rhyme_check", ["rhyme_check.py", "lyrics.md", "structure.md"]),
                   ("cliche_scan", ["cliche_scan.py", "lyrics.md"])]
        elif which == "concept.md":
            out = [("cliche_scan", ["cliche_scan.py", "concept.md"]),
                   ("prosody_check --hook", ["prosody_check.py", "--hook", "concept.md"])]
    elif agent == "composer":
        if has("chords.md"):
            out.append(("chord_tools", ["chord_tools.py", "chords.md", "structure.md"]))
        if has("melody.abc"):
            out.append(("abc_validate", ["abc_validate.py", "melody.abc", "structure.md", "lyrics.md"]))
        if not out and has("structure.md"):
            out.append(("structure_check", ["structure_check.py", "structure.md"]))
    elif agent == "arranger":
        if has("arrangement.md"):
            present = [n for n in ("structure.md", "lyrics.md", "chords.md", "melody.abc", "arrangement.md") if has(n)]
            out = [("arrangement_check", ["arrangement_check.py", "arrangement.md"]),
                   ("structure_check --consistency", ["structure_check.py", "--consistency", *present])]
    elif agent == "song-critic":
        if has("challenge-report.md"):
            out = [("challenge_gate", ["challenge_gate.py", "challenge-report.md"])]
    elif agent == "adapter":
        if has("adaptation-report.md"):
            out = [("adapt_check", ["adapt_check.py", "adaptation-report.md", "structure.md", "lyrics.md"])]
    return out


def run_gate(root: Path, d: Path, label: str, argv: list[str]) -> str:
    script = SCRIPTS / argv[0]
    if not script.is_file():
        return f"{label} SKIPPED (script absent)"
    args = [a for a in argv[1:]]
    cmd = [sys.executable, "-I", str(script)]
    cfg = root / ".song" / "config.yml"
    if cfg.is_file():
        cmd += ["--config", str(cfg)]
    cmd += ["--json"]
    for a in args:
        cmd.append(a if a.startswith("--") else str(d / a))
    try:
        proc = subprocess.run(cmd, cwd=str(root), capture_output=True, text=True, timeout=TIMEOUT)
    except Exception as exc:  # noqa: BLE001
        return f"{label} ERROR ({type(exc).__name__})"
    status = {0: "PASS", 1: "FAIL", 2: "SKIPPED", 3: "ERROR"}.get(proc.returncode, "ERROR")
    detail = ""
    try:
        res = json.loads(proc.stdout)
        status = res.get("status", status)
        viol = res.get("violations") or []
        if status == "FAIL" and viol:
            detail = f" ({len(viol)} violation(s); first: {str(viol[0].get('location', ''))} {str(viol[0].get('reason', ''))[:60]})"
    except ValueError:
        pass
    return f"{label} {status}{detail}"


def main() -> None:
    ap = argparse.ArgumentParser(add_help=False)
    ap.add_argument("--agent", default="")
    args, _ = ap.parse_known_args()
    data = hc.read_input()
    agent = args.agent or str(data.get("agent_type") or data.get("subagent_type") or "")
    if agent not in hc.MUSIC_AGENTS:
        return
    cwd = data.get("cwd")
    start = Path(cwd) if isinstance(cwd, str) and cwd else Path.cwd()
    root = find_root(start)
    if root is None:
        return
    slug = (root / ".song" / "active").read_text(encoding="utf-8").strip()
    d = root / ".song" / slug
    if not slug or not d.is_dir():
        hc.emit_message(f"music-team gates ({agent}): SKIPPED (no run directory .song/{slug or '?'}/)")
        return
    steps = plan(agent, d)
    if not steps:
        hc.emit_message(f"music-team gates ({agent}, {slug}): SKIPPED (no artifact for this agent yet)")
        return
    results = [run_gate(root, d, label, argv) for label, argv in steps]
    hc.emit_message(f"music-team gates ({agent}, {slug}), advisory: " + "; ".join(results))


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:  # noqa: BLE001
        print(f"music-team subagent_gate: internal error ({exc}); continuing", file=sys.stderr)
    sys.exit(0)
