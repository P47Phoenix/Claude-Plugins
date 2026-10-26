#!/usr/bin/env python3
"""validate_stages.py - validate music-flow's stages.yml against stages-schema.json.

Stdlib only; ``python -I`` safe. Loads the YAML with the subset loader in
``gate_common.py`` and checks a draft-07 subset of the schema: ``$ref`` into
``#/definitions``, ``type``, ``enum``, ``required``, ``properties``,
``additionalProperties`` (bool or schema), ``items``, ``minItems``, ``maxItems``,
``pattern``, ``minimum``, ``maximum``. Then runs cross-checks the schema cannot
express (sub-flow files exist, variant song types are known).

Usage:
  python -I music-team/scripts/validate_stages.py [--stages PATH] [--schema PATH] [--json]
Exit codes: 0 valid, 1 invalid, 3 unreadable input.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))
import gate_common as gc  # noqa: E402

REFS = Path(__file__).resolve().parents[1] / "skills" / "music-flow" / "references"
DEFAULT_STAGES = REFS / "stages.yml"
DEFAULT_SCHEMA = REFS / "stages-schema.json"


def _is_type(value: Any, name: str) -> bool:
    if name == "null":
        return value is None
    if name == "string":
        return isinstance(value, str)
    if name == "boolean":
        return isinstance(value, bool)
    if name == "integer":
        return isinstance(value, int) and not isinstance(value, bool)
    if name == "number":
        return isinstance(value, (int, float)) and not isinstance(value, bool)
    if name == "array":
        return isinstance(value, list)
    if name == "object":
        return isinstance(value, dict)
    return False


def _resolve(schema: dict, root: dict) -> dict:
    ref = schema.get("$ref")
    if not ref:
        return schema
    if not ref.startswith("#/"):
        raise ValueError(f"unsupported $ref {ref}")
    node: Any = root
    for part in ref[2:].split("/"):
        node = node[part]
    return node


def check(value: Any, schema: dict, root: dict, path: str, errors: list[str]) -> None:
    schema = _resolve(schema, root)
    types = schema.get("type")
    if types is not None:
        names = types if isinstance(types, list) else [types]
        if not any(_is_type(value, n) for n in names):
            errors.append(f"{path}: expected {'|'.join(names)}, got {type(value).__name__}")
            return
    if "enum" in schema and value not in schema["enum"]:
        errors.append(f"{path}: {value!r} not in {schema['enum']}")
    if isinstance(value, str) and "pattern" in schema and not re.search(schema["pattern"], value):
        errors.append(f"{path}: {value!r} does not match {schema['pattern']}")
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        if "minimum" in schema and value < schema["minimum"]:
            errors.append(f"{path}: {value} < minimum {schema['minimum']}")
        if "maximum" in schema and value > schema["maximum"]:
            errors.append(f"{path}: {value} > maximum {schema['maximum']}")
    if isinstance(value, list):
        if "minItems" in schema and len(value) < schema["minItems"]:
            errors.append(f"{path}: {len(value)} items < minItems {schema['minItems']}")
        if "maxItems" in schema and len(value) > schema["maxItems"]:
            errors.append(f"{path}: {len(value)} items > maxItems {schema['maxItems']}")
        if "items" in schema:
            for i, item in enumerate(value):
                check(item, schema["items"], root, f"{path}[{i}]", errors)
    if isinstance(value, dict):
        for key in schema.get("required", []):
            if key not in value:
                errors.append(f"{path}: missing required key '{key}'")
        props = schema.get("properties", {})
        extra = schema.get("additionalProperties", True)
        for key, sub in value.items():
            if key in props:
                check(sub, props[key], root, f"{path}.{key}", errors)
            elif extra is False:
                errors.append(f"{path}: unexpected key '{key}'")
            elif isinstance(extra, dict):
                check(sub, extra, root, f"{path}.{key}", errors)


def cross_checks(data: dict, schema: dict, stages_path: Path) -> list[str]:
    errors: list[str] = []
    types = schema["definitions"]["songType"]["enum"]
    base = stages_path.parent
    for sid, st in (data.get("stages") or {}).items():
        if not isinstance(st, dict):
            continue
        sub = st.get("sub_flow")
        if isinstance(sub, str) and not (base / sub).is_file():
            errors.append(f"stages.{sid}.sub_flow: file not found: {sub}")
        for t in st.get("type_variants") or {}:
            if t not in types:
                errors.append(f"stages.{sid}.type_variants: unknown song type '{t}'")
        for t in st.get("only_types") or []:
            if t not in types:
                errors.append(f"stages.{sid}.only_types: unknown song type '{t}'")
    return errors


def validate(stages_path: Path, schema_path: Path) -> list[str]:
    data = gc.load_yaml(gc.read_text(stages_path))
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    errors: list[str] = []
    check(data, schema, schema, "$", errors)
    if not errors:
        errors.extend(cross_checks(data, schema, stages_path))
    return errors


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Validate music-flow stages.yml against stages-schema.json")
    ap.add_argument("--stages", default=str(DEFAULT_STAGES))
    ap.add_argument("--schema", default=str(DEFAULT_SCHEMA))
    ap.add_argument("--json", action="store_true", help="emit a JSON result")
    args = ap.parse_args(argv)
    try:
        errors = validate(Path(args.stages), Path(args.schema))
    except (OSError, ValueError, KeyError) as exc:
        print(f"validate_stages: cannot read input: {exc}", file=sys.stderr)
        return 3
    status = "FAIL" if errors else "PASS"
    if args.json:
        print(json.dumps({"script": "validate_stages", "status": status, "violations": errors}))
    elif errors:
        for e in errors:
            print(f"FAIL {e}")
    else:
        print("PASS stages.yml valid")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
