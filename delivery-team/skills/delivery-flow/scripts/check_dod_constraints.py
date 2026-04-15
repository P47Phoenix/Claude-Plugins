#!/usr/bin/env python3
"""DoD deterministic constraint checker (US-8).

Usage:
    python check_dod_constraints.py [--skip-declarations] \
        <constraints.yml> <artifact_to_check>

Runs four deterministic checks against a decomposition-stage artifact using a
`constraints.yml` file validated by US-1:

  1. Forbidden vocabulary (FAIL on match) — case-insensitive whole-word grep of
     every token in `forbidden_vocabulary` across the artifact. Matches are
     reported with 1-based line numbers.
  2. Mandatory artifact presence (FAIL on missing) — each path in
     `mandatory_artifacts` must exist on disk (resolved relative to CWD).
  3. Numeric ceilings (INFO only) — the dict is printed for manual
     cross-reference. Automated ceiling enforcement is out of MVP scope
     because the artifact would need to be a parseable structured doc.
  4. Löwy / "Righting Software" citation shape (WARN only) — if a matching
     entry appears in `citations`, confirm it has non-empty chapter and page.

Flags:
  --skip-declarations
      When set, strip the `forbidden_vocabulary:` YAML block (the key and its
      indented child lines) from the artifact BEFORE grepping. This avoids
      false-positive self-check hits when the artifact being scanned is the
      constraints.yml file itself (FIX-3, b2c7 UAT TC-12). No-op on artifacts
      that don't contain a `forbidden_vocabulary:` declaration at column 0.

Exit code: 0 iff Check 1 and Check 2 both pass. 1 otherwise.

stdlib-only. Mirrors US-1's PyYAML-with-fallback loader so CI without extras
still runs the gate deterministically.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import Any, List, Tuple


# ---------------------------------------------------------------------------
# YAML loading (mirrors validate_constraints.py fallback strategy)
# ---------------------------------------------------------------------------

def _load_yaml(path: Path) -> Tuple[Any, List[str]]:
    try:
        text = path.read_text(encoding="utf-8")
    except OSError as exc:
        return None, [f"cannot read {path}: {exc}"]

    try:
        import yaml  # type: ignore
    except ImportError:
        return _load_yaml_fallback(text)

    try:
        return yaml.safe_load(text), []
    except Exception as exc:  # noqa: BLE001
        return None, [f"YAML parse error: {exc}"]


def _load_yaml_fallback(text: str) -> Tuple[Any, List[str]]:
    """Narrow subset: top-level keys, simple list items, and 1-level nested
    mappings (enough for numeric_ceilings + citation entries used here)."""
    doc: dict = {}
    current_key: str | None = None
    current_list: list | None = None
    current_map: dict | None = None
    current_list_item_map: dict | None = None

    for raw_line in text.splitlines():
        line = raw_line.rstrip()
        if not line.strip() or line.lstrip().startswith("#"):
            continue

        if not line.startswith((" ", "\t")):
            if ":" not in line:
                return None, [f"fallback parser: malformed line: {raw_line!r}"]
            key, _, rest = line.partition(":")
            key = key.strip()
            rest = rest.strip()
            current_list_item_map = None
            if rest == "":
                # Could be list OR mapping — start as list; upgrade to dict on
                # first nested `k: v` we see.
                current_list = []
                current_map = None
                current_key = key
                doc[key] = current_list
            else:
                doc[key] = _strip_quotes(rest)
                current_key = None
                current_list = None
                current_map = None
        else:
            stripped = line.strip()
            if stripped.startswith("- "):
                current_list_item_map = None
                item_body = stripped[2:].strip()
                if current_list is None:
                    continue
                if ":" in item_body and not item_body.startswith('"'):
                    # Start of a mapping list item, e.g. `- work: Foo`
                    k, _, v = item_body.partition(":")
                    current_list_item_map = {k.strip(): _strip_quotes(v.strip())}
                    current_list.append(current_list_item_map)
                else:
                    current_list.append(_strip_quotes(item_body))
            elif ":" in stripped:
                k, _, v = stripped.partition(":")
                k = k.strip()
                v = _strip_quotes(v.strip())
                if current_list_item_map is not None:
                    current_list_item_map[k] = v
                elif current_key is not None:
                    # Upgrade current_key from list-placeholder to dict.
                    if isinstance(doc.get(current_key), list) and not doc[current_key]:
                        doc[current_key] = {}
                        current_list = None
                        current_map = doc[current_key]
                    if current_map is None and isinstance(doc.get(current_key), dict):
                        current_map = doc[current_key]
                    if current_map is not None:
                        current_map[k] = _try_number(v)
    return doc, []


def _strip_quotes(v: str) -> str:
    if len(v) >= 2 and v[0] == v[-1] and v[0] in ('"', "'"):
        return v[1:-1]
    return v


def _try_number(v: str):
    try:
        if "." in v:
            return float(v)
        return int(v)
    except ValueError:
        return v


# ---------------------------------------------------------------------------
# Checks
# ---------------------------------------------------------------------------

def _strip_forbidden_vocab_block(lines: List[str]) -> List[str]:
    """Blank out the `forbidden_vocabulary:` declaration block.

    Detects a line where `forbidden_vocabulary:` begins at column 0 and blanks
    that line plus every following line that is indented (starts with space or
    tab) OR is empty-within-the-block until a new non-indented line is reached.
    Blanking (vs. removing) preserves 1-based line numbers in any surviving
    hit messages so reports still line up with the artifact on disk.
    """
    out = list(lines)
    i = 0
    n = len(out)
    while i < n:
        line = out[i]
        if line.startswith("forbidden_vocabulary:"):
            out[i] = ""
            j = i + 1
            while j < n:
                nxt = out[j]
                if nxt == "" or nxt.startswith((" ", "\t")):
                    out[j] = ""
                    j += 1
                    continue
                break
            i = j
            continue
        i += 1
    return out


def check_forbidden_vocab(artifact: Path, tokens: List[str],
                          skip_declarations: bool = False) -> List[str]:
    """Return a list of 'line:col token' match strings. Empty == pass."""
    if not tokens:
        return []
    try:
        lines = artifact.read_text(encoding="utf-8").splitlines()
    except OSError as exc:
        return [f"cannot read artifact {artifact}: {exc}"]

    if skip_declarations:
        lines = _strip_forbidden_vocab_block(lines)

    # Longest tokens first so multi-word tokens win over sub-tokens.
    sorted_tokens = sorted({t for t in tokens if t and t.strip()},
                           key=len, reverse=True)
    # Build a single alternation, escaped, with word boundaries.
    alt = "|".join(re.escape(t) for t in sorted_tokens)
    pattern = re.compile(rf"(?<![A-Za-z0-9_])(?:{alt})(?![A-Za-z0-9_])",
                         re.IGNORECASE)

    hits: List[str] = []
    for lineno, line in enumerate(lines, start=1):
        for m in pattern.finditer(line):
            hits.append(f"{artifact}:{lineno}: matched forbidden token "
                        f"'{m.group(0)}'  >> {line.strip()}")
    return hits


def check_mandatory_artifacts(paths: List[str]) -> List[str]:
    missing: List[str] = []
    for p in paths or []:
        if not Path(p).exists():
            missing.append(p)
    return missing


def summarize_numeric_ceilings(nc) -> str:
    if not isinstance(nc, dict) or not nc:
        return "numeric_ceilings: (none)"
    parts = [f"{k}={v}" for k, v in nc.items()]
    return "numeric_ceilings (informational, not auto-enforced in MVP): " + \
           ", ".join(parts)


def check_lowy_citation(citations) -> List[str]:
    """Return warnings (not errors) about Löwy citation shape."""
    warns: List[str] = []
    if not isinstance(citations, list):
        return warns
    pat = re.compile(r"löwy|righting software", re.IGNORECASE)
    matched_any = False
    for i, c in enumerate(citations):
        if not isinstance(c, dict):
            continue
        work = str(c.get("work", ""))
        if pat.search(work):
            matched_any = True
            chap = str(c.get("chapter", "")).strip()
            page = str(c.get("page", "")).strip()
            if not chap or not page:
                warns.append(
                    f"citations[{i}] Löwy/Righting Software entry missing "
                    f"chapter or page (chapter={chap!r}, page={page!r})"
                )
    if not matched_any:
        warns.append("no Löwy / 'Righting Software' citation found "
                     "(warning only; volatility artifacts should cite it)")
    return warns


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main(argv: List[str]) -> int:
    parser = argparse.ArgumentParser(
        prog="check_dod_constraints.py",
        description="DoD deterministic constraint checker (US-8).",
    )
    parser.add_argument(
        "--skip-declarations",
        action="store_true",
        help=("Strip the `forbidden_vocabulary:` YAML block from the artifact "
              "before grepping. Use when the artifact IS the constraints.yml "
              "(self-check) to avoid false-positive hits on the declaration."),
    )
    parser.add_argument("constraints", help="path to constraints.yml")
    parser.add_argument("artifact", help="path to artifact to check")
    args = parser.parse_args(argv[1:])

    constraints_path = Path(args.constraints)
    artifact_path = Path(args.artifact)

    if not constraints_path.exists():
        print(f"error: constraints file not found: {constraints_path}",
              file=sys.stderr)
        return 1
    if not artifact_path.exists():
        print(f"error: artifact file not found: {artifact_path}",
              file=sys.stderr)
        return 1

    doc, load_errors = _load_yaml(constraints_path)
    if load_errors or not isinstance(doc, dict):
        for e in load_errors:
            print(f"error: {e}", file=sys.stderr)
        if not load_errors:
            print("error: constraints file did not parse as a mapping",
                  file=sys.stderr)
        return 1

    failed = False

    # --- Check 1: forbidden vocabulary -----------------------------------
    print("[check 1/4] forbidden vocabulary grep", file=sys.stderr)
    tokens = doc.get("forbidden_vocabulary") or []
    hits = check_forbidden_vocab(artifact_path, tokens,
                                 skip_declarations=args.skip_declarations)
    if hits:
        failed = True
        print(f"  FAIL: {len(hits)} forbidden-vocabulary match(es):",
              file=sys.stderr)
        for h in hits:
            print(f"    {h}", file=sys.stderr)
    else:
        print("  PASS: no forbidden tokens found", file=sys.stderr)

    # --- Check 2: mandatory artifacts ------------------------------------
    print("[check 2/4] mandatory artifact presence", file=sys.stderr)
    missing = check_mandatory_artifacts(doc.get("mandatory_artifacts") or [])
    if missing:
        failed = True
        print(f"  FAIL: {len(missing)} mandatory artifact(s) missing:",
              file=sys.stderr)
        for m in missing:
            print(f"    - {m}", file=sys.stderr)
    else:
        print("  PASS: all mandatory artifacts present", file=sys.stderr)

    # --- Check 3: numeric ceilings (info) --------------------------------
    print("[check 3/4] numeric ceilings (informational)", file=sys.stderr)
    print("  " + summarize_numeric_ceilings(doc.get("numeric_ceilings")),
          file=sys.stderr)

    # --- Check 4: Löwy citation shape (warn) -----------------------------
    print("[check 4/4] Löwy citation shape (warning only)", file=sys.stderr)
    warns = check_lowy_citation(doc.get("citations"))
    if warns:
        for w in warns:
            print(f"  WARN: {w}", file=sys.stderr)
    else:
        print("  OK: Löwy citation shape acceptable", file=sys.stderr)

    if failed:
        print("DoD: FAIL", file=sys.stderr)
        return 1
    print("DoD: PASS", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
