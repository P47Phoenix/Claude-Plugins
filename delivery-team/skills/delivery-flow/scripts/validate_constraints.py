#!/usr/bin/env python3
"""Headless validator for `constraints.yml` (ADR-001, US-1).

Usage:
    python validate_constraints.py <path/to/constraints.yml>

Exit 0 on pass, 1 on fail. Errors printed to stderr.

Validation rules (narrow, forward-compatible per AC-1.4):
  * File must parse as YAML and the top level must be a mapping.
  * `entities` required, must be a non-empty list of non-empty strings.
  * `invariants` required, must be a non-empty list of non-empty strings.
  * Known optional fields are shape-checked if present.
  * Unknown top-level fields are ignored (NOT rejected).

Prefers stdlib + PyYAML (already a delivery-flow dependency via BRE stack).
Falls back to a minimal line-based parser sufficient for the narrow check
if PyYAML is unavailable, so CI without extras still exits correctly.
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any, List, Tuple


# ---------------------------------------------------------------------------
# YAML loading
# ---------------------------------------------------------------------------

def _load_yaml(path: Path) -> Tuple[Any, List[str]]:
    """Return (doc, errors). doc is None if parsing failed."""
    try:
        text = path.read_text(encoding="utf-8")
    except OSError as exc:
        return None, [f"cannot read {path}: {exc}"]

    try:
        import yaml  # type: ignore
    except ImportError:
        return _load_yaml_fallback(text)

    try:
        doc = yaml.safe_load(text)
    except Exception as exc:  # yaml.YAMLError and friends
        return None, [f"YAML parse error: {exc}"]
    return doc, []


def _load_yaml_fallback(text: str) -> Tuple[Any, List[str]]:
    """Minimal YAML subset: top-level keys + simple list items.

    Only enough to answer: does the file look like a mapping, and do
    `entities`/`invariants` appear as non-empty lists? Unknown optional
    fields are parsed as opaque truthy markers — the narrow check only
    enforces the two required fields anyway.
    """
    doc: dict = {}
    current_key: str | None = None
    current_list: list | None = None

    for raw_line in text.splitlines():
        line = raw_line.rstrip()
        if not line.strip() or line.lstrip().startswith("#"):
            continue

        if not line.startswith((" ", "\t")):
            # top-level `key:` or `key: value`
            if ":" not in line:
                return None, [f"fallback parser: malformed line: {raw_line!r}"]
            key, _, rest = line.partition(":")
            key = key.strip()
            rest = rest.strip()
            if rest == "" or rest is None:
                current_key = key
                current_list = []
                doc[key] = current_list
            else:
                doc[key] = rest
                current_key = None
                current_list = None
        else:
            stripped = line.strip()
            if stripped.startswith("- ") or stripped == "-":
                if current_list is None:
                    # indented scalar under a mapping we don't track — ignore.
                    continue
                item = stripped[1:].strip()
                current_list.append(item if item else None)
            # indented `key: value` under an object we don't track — ignore.
    return doc, []


# ---------------------------------------------------------------------------
# Validation
# ---------------------------------------------------------------------------

KNOWN_LIST_OF_STRINGS = {
    "entities",
    "invariants",
    "state_variables",
    "actions",
    "mandatory_artifacts",
    "forbidden_vocabulary",
}


def _is_nonempty_string_list(value: Any) -> bool:
    if not isinstance(value, list) or not value:
        return False
    return all(isinstance(v, str) and v.strip() for v in value)


def validate(doc: Any) -> List[str]:
    errors: List[str] = []

    if not isinstance(doc, dict):
        return ["top-level of constraints.yml must be a mapping"]

    # Required fields.
    for required in ("entities", "invariants"):
        if required not in doc:
            errors.append(f"missing required field: {required}")
            continue
        if not _is_nonempty_string_list(doc[required]):
            errors.append(
                f"{required} must be a non-empty list of non-empty strings"
            )

    # Optional shape checks — only if present.
    for key in ("state_variables", "actions",
                "mandatory_artifacts", "forbidden_vocabulary"):
        if key in doc and doc[key] is not None:
            if not isinstance(doc[key], list):
                errors.append(f"{key} must be a list of strings if present")
            else:
                for i, v in enumerate(doc[key]):
                    if not isinstance(v, str) or not v.strip():
                        errors.append(f"{key}[{i}] must be a non-empty string")

    if "numeric_ceilings" in doc and doc["numeric_ceilings"] is not None:
        nc = doc["numeric_ceilings"]
        if not isinstance(nc, dict):
            errors.append("numeric_ceilings must be a mapping of name -> number")
        else:
            for k, v in nc.items():
                if not isinstance(k, str) or not k.strip():
                    errors.append(f"numeric_ceilings key {k!r} must be a non-empty string")
                if isinstance(v, bool) or not isinstance(v, (int, float)):
                    errors.append(f"numeric_ceilings[{k!r}] must be a number")

    if "citations" in doc and doc["citations"] is not None:
        cits = doc["citations"]
        if not isinstance(cits, list):
            errors.append("citations must be a list of objects")
        else:
            for i, c in enumerate(cits):
                if not isinstance(c, dict):
                    errors.append(f"citations[{i}] must be a mapping")
                    continue
                for req in ("work", "chapter", "page"):
                    if req not in c:
                        errors.append(f"citations[{i}] missing required key: {req}")

    # AC-1.4: unknown top-level fields are ignored, not rejected.
    return errors


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main(argv: List[str]) -> int:
    if len(argv) != 2:
        print("usage: validate_constraints.py <path/to/constraints.yml>",
              file=sys.stderr)
        return 1

    path = Path(argv[1])
    if not path.exists():
        print(f"error: file not found: {path}", file=sys.stderr)
        return 1

    doc, load_errors = _load_yaml(path)
    if load_errors:
        for e in load_errors:
            print(f"error: {e}", file=sys.stderr)
        return 1

    errors = validate(doc)
    if errors:
        print(f"error: {path} is INVALID against constraints schema:",
              file=sys.stderr)
        for e in errors:
            print(f"  - {e}", file=sys.stderr)
        return 1

    print(f"ok: {path} is valid against constraints schema")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
