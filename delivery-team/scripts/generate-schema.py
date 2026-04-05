#!/usr/bin/env python3
"""
Generate JSON Schema from config-schema.md markdown table.

The markdown table in config-schema.md is the single source of truth.
This script parses it and produces config-schema.json (JSON Schema Draft 2020-12).

Usage:
    python generate-schema.py
"""

import json
import re
from pathlib import Path


# Paths relative to this script
SCRIPT_DIR = Path(__file__).resolve().parent
SCHEMA_MD = SCRIPT_DIR.parent / "skills" / "delivery-flow" / "references" / "config-schema.md"
SCHEMA_JSON = SCHEMA_MD.parent / "config-schema.json"


def parse_markdown_table(text: str) -> list[dict]:
    """Parse the Complete Schema markdown table into a list of row dicts."""
    # Find the "## Complete Schema" section
    match = re.search(r"## Complete Schema\s*\n", text)
    if not match:
        raise ValueError("Could not find '## Complete Schema' section")

    section = text[match.end():]

    # Find table lines (start with |)
    lines = []
    for line in section.split("\n"):
        stripped = line.strip()
        if stripped.startswith("|"):
            lines.append(stripped)
        elif lines and not stripped.startswith("|"):
            # End of table
            break

    if len(lines) < 3:
        raise ValueError(f"Table too short: found {len(lines)} lines")

    # Parse header
    headers = [h.strip() for h in lines[0].split("|")[1:-1]]
    # lines[1] is the separator (|---|---|...)

    rows = []
    for line in lines[2:]:
        cells = [c.strip() for c in line.split("|")[1:-1]]
        if len(cells) < len(headers):
            cells.extend([""] * (len(headers) - len(cells)))
        row = {}
        for i, header in enumerate(headers):
            row[header] = cells[i] if i < len(cells) else ""
        rows.append(row)

    return rows


def clean_key(raw: str) -> str:
    """Strip backticks from key column."""
    return raw.strip().strip("`")


def parse_type(raw_type: str) -> dict:
    """Convert a type string from the table to a JSON Schema type definition."""
    t = raw_type.strip()

    if t == "string":
        return {"type": "string"}
    elif t == "integer":
        return {"type": "integer"}
    elif t == "boolean":
        return {"type": "boolean"}
    elif t == "string/null":
        return {"type": ["string", "null"]}
    elif t == "list[string]":
        return {"type": "array", "items": {"type": "string"}}
    elif t == "list[object]":
        return {"type": "array", "items": {"type": "object"}}
    elif t == "map[string, string]":
        return {"type": "object", "additionalProperties": {"type": "string"}}
    elif t == "map":
        return {"type": "object"}
    elif t.startswith("map["):
        # Generic map[K, V] — extract value type for additionalProperties
        map_match = re.match(r"^map\[\s*\w+\s*,\s*(\w+)\s*\]$", t)
        if map_match:
            value_type = map_match.group(1)
            return {"type": "object", "additionalProperties": {"type": value_type}}
        return {"type": "object"}
    elif t == "object":
        return {"type": "object"}
    else:
        # Fallback
        return {"type": "string"}


def parse_valid_values(raw: str, schema_type: dict) -> dict:
    """Add enum, minimum/maximum, or item constraints from Valid Values column."""
    v = raw.strip()
    result = dict(schema_type)

    if not v:
        return result

    # Check for range pattern like "1-5", "30-600", "50-500", "1+"
    range_match = re.match(r"^(\d+)-(\d+)$", v)
    range_open_match = re.match(r"^(\d+)\+$", v)

    if result.get("type") == "integer":
        if range_match:
            result["minimum"] = int(range_match.group(1))
            result["maximum"] = int(range_match.group(2))
            return result
        elif range_open_match:
            result["minimum"] = int(range_open_match.group(1))
            return result

    # Check for "subset of:" or "subset of the N patterns" pattern -> array items enum
    subset_match = re.match(r"^subset of:\s*(.+)$", v)
    if subset_match and result.get("type") == "array":
        items_str = subset_match.group(1)
        enum_values = [x.strip() for x in items_str.split(",")]
        result["items"] = {"type": "string", "enum": enum_values}
        return result

    # "subset of the N patterns" -- derive enum from the default value if available
    if re.match(r"^subset of the \d+ patterns$", v) and result.get("type") == "array":
        # Enum will be populated from the default value in post-processing
        result["_derive_enum_from_default"] = True
        return result

    # Check for comma-separated enum values (for strings)
    # Skip generic descriptions like "language names", "framework names", etc.
    generic_patterns = [
        "language names", "framework names", "database names",
        "role identifiers", "persona names from library",
        "glob patterns", "persona profile objects",
        "semver string", "ISO date or null", "ISO date",
        "any built-in or custom theme name", "directory path",
        "component", "language",
    ]

    is_generic = False
    v_lower = v.lower()
    for pattern in generic_patterns:
        if pattern in v_lower:
            is_generic = True
            break

    # Also skip if it contains parenthetical qualifiers suggesting it's a description
    if re.search(r"\(only when|each:|auto-detected\)", v):
        is_generic = True

    if not is_generic and result.get("type") == "string":
        # Looks like comma-separated enum values
        candidates = [x.strip() for x in v.split(",")]
        if len(candidates) >= 2 and all(len(c) < 40 for c in candidates):
            result["enum"] = candidates
            return result

    # For list[string] with specific enum items
    if not is_generic and result.get("type") == "array":
        candidates = [x.strip() for x in v.split(",")]
        if len(candidates) >= 2 and all(len(c) < 40 for c in candidates):
            result["items"] = {"type": "string", "enum": candidates}
            return result

    # "true/false" for booleans -- no extra constraints needed
    return result


def parse_default(raw: str, schema_type: dict) -> object:
    """Parse the default value from the table."""
    d = raw.strip()

    if not d or d == "auto" or d.startswith("auto ("):
        return None  # No static default to set

    # Handle specific patterns
    if d == "null":
        return None

    type_val = schema_type.get("type")

    if type_val == "boolean" or (isinstance(type_val, str) and type_val == "boolean"):
        # Handle "false (auto-detected from nx.json)" or "false (auto-detected)" etc.
        cleaned = d.split("(")[0].strip().lower()
        if cleaned == "true":
            return True
        elif cleaned == "false":
            return False

    if type_val == "integer":
        try:
            return int(d)
        except ValueError:
            return None

    if type_val == "string" or type_val == ["string", "null"]:
        # Strip surrounding quotes
        cleaned = d.strip('"').strip("'")
        return cleaned

    if type_val == "array":
        if d == "[]":
            return []
        # Parse bracketed lists like [refine, architect, plan, uat]
        bracket_match = re.match(r"^\[(.+)\]$", d)
        if bracket_match:
            items = [x.strip().strip('"').strip("'") for x in bracket_match.group(1).split(",")]
            return items
        return None

    if type_val == "object" or d == "{}":
        if d == "{}":
            return {}
        return None

    return None


def set_nested(root: dict, dotted_key: str, prop_schema: dict, required: bool):
    """Set a property in a nested JSON Schema structure using dot-notation key."""
    parts = dotted_key.split(".")

    # Navigate/create nested structure
    current = root
    for part in parts[:-1]:
        if "properties" not in current:
            current["properties"] = {}
        if part not in current["properties"]:
            current["properties"][part] = {
                "type": "object",
                "properties": {},
                "additionalProperties": False,
            }
        current = current["properties"][part]

    leaf_name = parts[-1]
    if "properties" not in current:
        current["properties"] = {}
    current["properties"][leaf_name] = prop_schema

    if required:
        if "required" not in current:
            current["required"] = []
        if leaf_name not in current["required"]:
            current["required"].append(leaf_name)


def generate_schema(rows: list[dict]) -> dict:
    """Build a JSON Schema from parsed table rows."""
    schema = {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "$id": "https://github.com/P47Phoenix/Claude-Plugins/delivery-team/config-schema.json",
        "title": "Delivery Pipeline Configuration",
        "description": "Schema for .delivery/config.yml -- generated from config-schema.md. Do NOT edit by hand.",
        "type": "object",
        "properties": {},
        "additionalProperties": False,
    }

    for row in rows:
        key = clean_key(row.get("Key", ""))
        if not key:
            continue

        raw_type = row.get("Type", "string")
        raw_required = row.get("Required", "no").strip().lower() == "yes"
        raw_default = row.get("Default", "")
        raw_valid = row.get("Valid Values", "")

        # Build property schema
        type_schema = parse_type(raw_type)
        prop_schema = parse_valid_values(raw_valid, type_schema)

        # Set default
        default_val = parse_default(raw_default, type_schema)
        if default_val is not None:
            prop_schema["default"] = default_val
        elif raw_default.strip() == "null":
            prop_schema["default"] = None

        # Derive item enum from default value when marked
        if prop_schema.pop("_derive_enum_from_default", False):
            if isinstance(default_val, list) and default_val:
                prop_schema["items"] = {"type": "string", "enum": default_val}

        # Place into nested structure
        set_nested(schema, key, prop_schema, raw_required)

    return schema


def main():
    print(f"Reading: {SCHEMA_MD}")
    text = SCHEMA_MD.read_text(encoding="utf-8")

    rows = parse_markdown_table(text)
    print(f"Parsed {len(rows)} schema rows")

    schema = generate_schema(rows)

    SCHEMA_JSON.write_text(
        json.dumps(schema, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(f"Wrote: {SCHEMA_JSON}")


if __name__ == "__main__":
    main()
