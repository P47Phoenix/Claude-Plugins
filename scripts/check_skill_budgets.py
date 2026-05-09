#!/usr/bin/env python3
"""
check_skill_budgets.py — SKILL.md line-budget CI gate (W0-2)

Walks delivery-team SKILL.md files, parses YAML frontmatter for `tier:` field,
compares line count to tier budget. Exits non-zero on violation.

Tier budgets (exactly these three values, TIER_LIMITS):
  A <= 500 lines  (orchestrators)
  B <= 300 lines  (role multiplexers)
  C <= 200 lines  (leaf / paradigm sub-skills)

Usage:
  python3 scripts/check_skill_budgets.py                  # full check of all SKILL.md files
  python3 scripts/check_skill_budgets.py --check <path>   # check a single file
  python3 scripts/check_skill_budgets.py --check <path> --tier <A|B|C>  # override tier
  python3 scripts/check_skill_budgets.py --known-debt-report             # print known-debt list, exit 0
  python3 scripts/check_skill_budgets.py --warn-permissive [<path>]      # warn-only permissive scan
"""

import argparse
import os
import re
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Tier budget constants — exactly A=500 / B=300 / C=200 (ADR-tk0e-002)
# ---------------------------------------------------------------------------
TIER_LIMITS = {"A": 500, "B": 300, "C": 200}

# ---------------------------------------------------------------------------
# Known-debt pre-registration — synchronized with governance/skill-budgets.json
# (single source of truth verified by scripts/lint_known_debt.py — W3-14).
#
# Wave 3 Story 5 (W3-9) cleared the final 7 Wave-2 entries:
#   architect (500→294), presentation (545→185), ui (496→222),
#   operations (420→219), quality (418→289), user-feedback (399→272),
#   godot (236→200).
# All 11 top-level delivery-team SKILL.md are now compliant; known_debt[]
# baselines empty for the first time since BACKLOG-100 (Wave 0). Re-additions
# require an entry in BOTH this list AND governance/skill-budgets.json.
# ---------------------------------------------------------------------------
KNOWN_DEBT: list[dict] = []

# ---------------------------------------------------------------------------
# Budget-Exception token (ADR-tk0e-002 Ruling 3 escape hatch)
# ---------------------------------------------------------------------------
BUDGET_EXCEPTION_TOKEN = "Budget-Exception: known-debt-tk0e"


def parse_frontmatter(text: str) -> dict:
    """Parse YAML frontmatter from SKILL.md content.

    Extracts key: value pairs from the first --- ... --- block.
    Pure stdlib; no external YAML parser required.
    """
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}
    fm = {}
    for line in lines[1:]:
        if line.strip() == "---":
            break
        if ":" in line:
            key, _, val = line.partition(":")
            fm[key.strip()] = val.strip().strip('"').strip("'")
    return fm


def count_lines(path: str) -> int:
    """Count lines in a file."""
    with open(path, "r", encoding="utf-8", errors="replace") as fh:
        return sum(1 for _ in fh)


def is_known_debt(norm_path: str) -> dict | None:
    """Return the known-debt entry for a path if it exists, else None."""
    for entry in KNOWN_DEBT:
        # normalise separators for comparison
        if Path(entry["path"]) == Path(norm_path):
            return entry
    return None


def resolve_tier(frontmatter: dict, path: str, tier_override: str | None) -> str | None:
    """Resolve tier from frontmatter → governance registry → override → None."""
    if tier_override:
        return tier_override.upper()
    if "tier" in frontmatter:
        return frontmatter["tier"].upper()
    # Fallback: look up governance/skill-budgets.json registry
    registry_path = Path("governance/skill-budgets.json")
    if registry_path.exists():
        import json
        try:
            registry = json.loads(registry_path.read_text())
            for entry in registry.get("known_debt", []):
                if Path(entry["path"]) == Path(path):
                    return entry["tier"].upper()
        except Exception:
            pass
    return None


def check_pr_body_exception() -> bool:
    """Return True if PR body (from env var PR_BODY) contains the exception token."""
    pr_body = os.environ.get("PR_BODY", "")
    return BUDGET_EXCEPTION_TOKEN in pr_body


# ---------------------------------------------------------------------------
# Permissive-language sub-check
#
# EXEMPT ZONES (must NOT be scanned — ADR-tk0e-002):
#   1. Fenced code blocks: content between ``` delimiters (any language tag)
#   2. Blockquotes: lines beginning with > (after optional whitespace)
#   3. Table rows: lines beginning with | (after optional whitespace)
#
# RATIONALE: adversarial, debate, and compliance skills legitimately use
# these words in quoted prose (e.g., "challenger may propose...").
# Hard-fail would produce systemic false positives. Warn-only preserves
# signal without blocking.
#
# PATTERN: \bshould\b|\bcan\b|\bmay\b|\bmight\b|\bcould\b|\btry to\b
# ---------------------------------------------------------------------------
PERMISSIVE_PATTERN = re.compile(
    r"\bshould\b|\bcan\b|\bmay\b|\bmight\b|\bcould\b|\btry to\b",
    re.IGNORECASE,
)


def scan_permissive_language(path: str) -> list[tuple[int, str, str]]:
    """Scan a SKILL.md for permissive language outside exempt zones.

    Returns list of (line_number, line_text, matched_word) tuples.
    Never raises; always exits 0.
    """
    hits = []
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as fh:
            lines = fh.readlines()
    except OSError:
        return hits

    in_code_block = False
    in_frontmatter = False
    frontmatter_seen = False

    for lineno, raw in enumerate(lines, start=1):
        line = raw.rstrip("\n")

        # Track frontmatter block (first ---...--- section)
        if lineno == 1 and line.strip() == "---":
            in_frontmatter = True
            continue
        if in_frontmatter:
            if line.strip() == "---":
                in_frontmatter = False
                frontmatter_seen = True
            continue  # skip all frontmatter lines

        # Track fenced code blocks (exempt zone 1)
        if line.strip().startswith("```"):
            in_code_block = not in_code_block
            continue
        if in_code_block:
            continue

        # Exempt zone 2: blockquotes
        if re.match(r"^\s*>", line):
            continue

        # Exempt zone 3: table rows
        if re.match(r"^\s*\|", line):
            continue

        # Scan prose line
        m = PERMISSIVE_PATTERN.search(line)
        if m:
            hits.append((lineno, line, m.group(0)))

    return hits


def find_skill_files(base: str = ".") -> list[str]:
    """Walk delivery-team for all SKILL.md files."""
    results = []
    base_path = Path(base)
    for p in base_path.glob("delivery-team/**/SKILL.md"):
        results.append(str(p))
    return sorted(results)


def check_file(
    path: str,
    tier_override: str | None = None,
    pr_exception: bool = False,
) -> tuple[bool, str]:
    """Check a single SKILL.md file against its tier budget.

    Returns (passed: bool, message: str).
    """
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as fh:
            content = fh.read()
    except OSError as exc:
        return False, f"ERROR: Cannot read {path}: {exc}"

    frontmatter = parse_frontmatter(content)
    tier = resolve_tier(frontmatter, path, tier_override)

    if tier is None:
        return False, (
            f"MISSING TIER: {path} — add `tier: A|B|C` to frontmatter"
        )

    if tier not in TIER_LIMITS:
        return False, f"INVALID TIER '{tier}': {path} — must be A, B, or C"

    limit = TIER_LIMITS[tier]
    actual = count_lines(path)

    if actual <= limit:
        return True, f"OK: {path} {actual}/{limit} lines (Tier-{tier})"

    # Over budget — check known-debt first
    debt_entry = is_known_debt(path)
    if debt_entry is not None:
        return True, (
            f"KNOWN-DEBT: {path} {actual}/{limit} lines — target wave: W{debt_entry['target_wave']}"
        )

    # Check PR-body exception
    if pr_exception:
        return True, (
            f"EXCEPTION ACKNOWLEDGED: {path} — budget override active "
            f"({actual}/{limit} lines Tier-{tier})"
        )

    return False, (
        f"BUDGET VIOLATION: {path} {actual}/{limit} lines (Tier-{tier})"
    )


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Check SKILL.md line budgets against tier limits."
    )
    parser.add_argument(
        "--check",
        metavar="PATH",
        help="Check a single SKILL.md file instead of walking delivery-team/",
    )
    parser.add_argument(
        "--tier",
        metavar="TIER",
        choices=["A", "B", "C", "a", "b", "c"],
        help="Override tier for --check (ignores frontmatter tier)",
    )
    parser.add_argument(
        "--known-debt-report",
        action="store_true",
        help="Print the known-debt list and exit 0",
    )
    parser.add_argument(
        "--warn-permissive",
        nargs="?",
        const="__all__",
        metavar="PATH",
        help=(
            "Scan for permissive language (warn-only, always exits 0). "
            "Optionally pass a single file path."
        ),
    )
    # Positional path for --warn-permissive convenience (e.g. --warn-permissive <path>)
    parser.add_argument(
        "positional_path",
        nargs="?",
        metavar="PATH",
        help="Path for use with --warn-permissive when passed as positional arg",
    )
    args = parser.parse_args()

    # --known-debt-report — print all 7 entries and exit 0
    if args.known_debt_report:
        for entry in KNOWN_DEBT:
            limit = TIER_LIMITS[entry["tier"]]
            print(
                f"KNOWN-DEBT: {entry['path']} {entry['current']}/{limit} lines"
                f" — target wave: W{entry['target_wave']}"
            )
        return 0

    # --warn-permissive — scan and warn, always exit 0
    if args.warn_permissive is not None:
        scan_target = args.warn_permissive
        if scan_target == "__all__":
            # Use positional arg if provided
            if args.positional_path:
                scan_target = args.positional_path
            else:
                scan_target = "__all__"

        if scan_target == "__all__":
            files = find_skill_files()
        else:
            files = [scan_target]

        total_hits = 0
        for fpath in files:
            hits = scan_permissive_language(fpath)
            if hits:
                total_hits += len(hits)
                for lineno, line_text, word in hits:
                    print(
                        f"PERMISSIVE-LANGUAGE: {fpath}:{lineno}: '{word}' — {line_text.strip()}",
                        file=sys.stderr,
                    )

        if total_hits:
            # Write to GitHub Actions step summary if available
            summary_path = os.environ.get("GITHUB_STEP_SUMMARY")
            if summary_path:
                try:
                    with open(summary_path, "a") as sf:
                        sf.write(
                            f"\n## Permissive Language Warnings ({total_hits} hits)\n\n"
                        )
                        sf.write(
                            "These are advisory only — they do NOT block merge.\n\n"
                        )
                except OSError:
                    pass

        return 0  # always exit 0 (warn-only per ADR-tk0e-002)

    # Budget check — single file or full walk
    pr_exception = check_pr_body_exception()

    if args.check:
        paths = [args.check]
        tier_override = args.tier.upper() if args.tier else None
    else:
        paths = find_skill_files()
        tier_override = None

    violations = []
    known_debt_hits = []
    ok_hits = []
    exceptions = []

    for path in paths:
        passed, message = check_file(path, tier_override=tier_override, pr_exception=pr_exception)
        if message.startswith("KNOWN-DEBT:"):
            known_debt_hits.append(message)
        elif message.startswith("EXCEPTION ACKNOWLEDGED:"):
            exceptions.append(message)
            print(message, file=sys.stderr)
        elif passed:
            ok_hits.append(message)
        else:
            violations.append(message)
            print(message)

    # Print known-debt lines (informational)
    for msg in known_debt_hits:
        print(msg)

    # Summary
    total = len(paths)
    if violations:
        print(
            f"\nBUDGET CHECK FAILED: {len(violations)} violation(s) in {total} file(s)."
        )
        return 1

    print(
        f"\nBUDGET CHECK PASSED: {total} file(s) checked, "
        f"{len(known_debt_hits)} known-debt, {len(exceptions)} exception(s)."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
