#!/usr/bin/env python3
"""lint_known_debt.py — Wave 3 W3-14 governance lint.

Verifies two invariants in a single pass; exits non-zero on any drift:

1. **JSON ↔ Python KNOWN_DEBT consistency** — `governance/skill-budgets.json`
   `known_debt[]` must match `scripts/check_skill_budgets.py` `KNOWN_DEBT`
   (single source of truth: same paths, same tiers, same target_wave values).
   Wave 2 retro lesson: registry consistency is multi-source.

2. **Frontmatter rollout completeness (Story 5 carry-forward)** — every
   top-level `delivery-team/skills/*/SKILL.md` must declare `maintainer:`,
   `fitness_review_due:`, `context_budget:`, and `tier:` in YAML frontmatter.
   `context_budget` must match the tier ceiling per
   `governance/skill-budgets.json tiers` (A=500 / B=300 / C=200).

Subsumes the Story-5 deferred lint per the AC amendment in
`.delivery/artifacts/06-dev/dod/story-5-ac-amendment.md`.

Usage:
    python3 scripts/lint_known_debt.py             # exit 0 = clean, 1 = drift
"""
from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
JSON_REGISTRY = REPO_ROOT / "governance" / "skill-budgets.json"
PY_CHECKER = REPO_ROOT / "scripts" / "check_skill_budgets.py"
SKILLS_GLOB = "delivery-team/skills/*/SKILL.md"
REQUIRED_KEYS = ("maintainer", "fitness_review_due", "context_budget", "tier")


def _load_json_registry() -> dict:
    if not JSON_REGISTRY.is_file():
        sys.exit(f"FAIL: missing {JSON_REGISTRY.relative_to(REPO_ROOT)}")
    return json.loads(JSON_REGISTRY.read_text())


def _load_python_known_debt() -> list[dict]:
    spec = importlib.util.spec_from_file_location("cs_budgets", PY_CHECKER)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return list(module.KNOWN_DEBT)


def _normalize(entry: dict) -> tuple:
    """Return a comparable tuple (path, tier, target_wave). `current` is allowed
    to drift between JSON registry and Python audit baseline (JSON tracks the
    last-baseline snapshot; Python tracks pre-baseline audit values)."""
    return (
        str(Path(entry["path"])),
        entry["tier"].upper(),
        int(entry.get("target_wave", -1)),
    )


def _parse_frontmatter(text: str) -> dict:
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}
    fm: dict[str, str] = {}
    for line in lines[1:]:
        if line.strip() == "---":
            break
        if ":" in line:
            key, _, val = line.partition(":")
            fm[key.strip()] = val.strip().strip('"').strip("'")
    return fm


def check_known_debt_drift() -> list[str]:
    failures: list[str] = []
    json_data = _load_json_registry()
    json_debt = {_normalize(e) for e in json_data.get("known_debt", [])}
    py_debt = {_normalize(e) for e in _load_python_known_debt()}

    only_json = json_debt - py_debt
    only_py = py_debt - json_debt

    for entry in sorted(only_json):
        failures.append(
            f"DRIFT (JSON-only): {entry[0]} tier={entry[1]} wave=W{entry[2]}"
        )
    for entry in sorted(only_py):
        failures.append(
            f"DRIFT (Python-only): {entry[0]} tier={entry[1]} wave=W{entry[2]}"
        )
    return failures


def check_frontmatter_rollout() -> list[str]:
    failures: list[str] = []
    json_data = _load_json_registry()
    tier_ceilings = {
        tier_name: tier_def["max_lines"]
        for tier_name, tier_def in json_data.get("tiers", {}).items()
    }
    if not tier_ceilings:
        failures.append("FAIL: governance/skill-budgets.json has no `tiers:` section")
        return failures

    skills = sorted(REPO_ROOT.glob(SKILLS_GLOB))
    if not skills:
        failures.append(f"FAIL: no SKILL.md found under {SKILLS_GLOB}")
        return failures

    for skill_path in skills:
        rel = skill_path.relative_to(REPO_ROOT)
        fm = _parse_frontmatter(skill_path.read_text(encoding="utf-8", errors="replace"))
        for key in REQUIRED_KEYS:
            if key not in fm:
                failures.append(f"MISSING-KEY: {rel} — `{key}:` not in frontmatter")
        if "tier" in fm and "context_budget" in fm:
            tier = fm["tier"].upper()
            try:
                budget = int(fm["context_budget"])
            except ValueError:
                failures.append(
                    f"INVALID-BUDGET: {rel} — context_budget '{fm['context_budget']}' not an integer"
                )
                continue
            ceiling = tier_ceilings.get(tier)
            if ceiling is None:
                failures.append(
                    f"UNKNOWN-TIER: {rel} — tier '{tier}' not in skill-budgets.json"
                )
            elif budget != ceiling:
                failures.append(
                    f"BUDGET-TIER-MISMATCH: {rel} — context_budget={budget} but Tier-{tier} ceiling={ceiling}"
                )
    return failures


def main() -> int:
    failures = check_known_debt_drift() + check_frontmatter_rollout()
    if failures:
        for line in failures:
            print(line, file=sys.stderr)
        print(
            f"\nLINT FAILED: {len(failures)} drift/missing entries (W3-14).",
            file=sys.stderr,
        )
        return 1
    print("LINT OK: known_debt JSON↔Python in sync; all SKILL.md frontmatter complete.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
