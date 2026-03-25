#!/usr/bin/env python3
"""
Validate a .delivery/config.yml file against the generated JSON Schema.

Usage:
    python validate-config.py [path/to/config.yml]

If no path is given, defaults to .delivery/config.yml in the current working directory.

Requires: pip install pyyaml jsonschema
"""

import json
import sys
from pathlib import Path


def check_dependencies():
    """Check that required third-party packages are available."""
    missing = []
    try:
        import yaml  # noqa: F401
    except ImportError:
        missing.append("pyyaml")

    try:
        import jsonschema  # noqa: F401
    except ImportError:
        missing.append("jsonschema")

    if missing:
        print(f"ERROR: Missing required packages: {', '.join(missing)}")
        print(f"Install them with: pip install {' '.join(missing)}")
        sys.exit(2)


def load_schema() -> dict:
    """Load the JSON Schema from config-schema.json next to the schema markdown."""
    script_dir = Path(__file__).resolve().parent
    schema_path = (
        script_dir.parent
        / "skills"
        / "delivery-flow"
        / "references"
        / "config-schema.json"
    )
    if not schema_path.exists():
        print(f"ERROR: Schema file not found at {schema_path}")
        print("Run generate-schema.py first to create it.")
        sys.exit(2)

    return json.loads(schema_path.read_text(encoding="utf-8"))


def load_config(config_path: Path) -> dict:
    """Load and parse a YAML config file."""
    import yaml

    if not config_path.exists():
        print(f"ERROR: Config file not found: {config_path}")
        sys.exit(2)

    text = config_path.read_text(encoding="utf-8")

    # Strip YAML frontmatter delimiters if present (legacy config.md format)
    lines = text.split("\n")
    if lines and lines[0].strip() == "---":
        # Find closing ---
        for i in range(1, len(lines)):
            if lines[i].strip() == "---":
                text = "\n".join(lines[1:i])
                break

    data = yaml.safe_load(text)
    if not isinstance(data, dict):
        print(f"ERROR: Config file did not parse as a YAML mapping: {config_path}")
        sys.exit(2)

    return data


def validate(config: dict, schema: dict) -> dict:
    """Validate config against schema, returning categorized errors."""
    import jsonschema

    validator_cls = jsonschema.Draft202012Validator
    validator = validator_cls(schema)

    errors_by_type = {
        "missing_required": [],
        "type_error": [],
        "enum_error": [],
        "range_error": [],
        "unknown_key": [],
        "other": [],
    }

    for error in sorted(validator.iter_errors(config), key=lambda e: list(e.path)):
        path = ".".join(str(p) for p in error.absolute_path) or "(root)"

        if error.validator == "required":
            errors_by_type["missing_required"].append({
                "path": path,
                "message": error.message,
            })
        elif error.validator == "type":
            errors_by_type["type_error"].append({
                "path": path,
                "message": f"Expected {error.validator_value}, got {type(error.instance).__name__}: {error.message}",
            })
        elif error.validator == "enum":
            errors_by_type["enum_error"].append({
                "path": path,
                "message": f"Invalid value '{error.instance}'. {error.message}",
            })
        elif error.validator in ("minimum", "maximum"):
            errors_by_type["range_error"].append({
                "path": path,
                "message": error.message,
            })
        elif error.validator == "additionalProperties":
            errors_by_type["unknown_key"].append({
                "path": path,
                "message": error.message,
            })
        else:
            errors_by_type["other"].append({
                "path": path,
                "message": f"[{error.validator}] {error.message}",
            })

    return errors_by_type


def print_errors(errors_by_type: dict) -> int:
    """Print categorized errors and return total count."""
    labels = {
        "missing_required": "Missing Required Keys",
        "type_error": "Type Errors",
        "enum_error": "Invalid Enum Values",
        "range_error": "Range Violations",
        "unknown_key": "Unknown Keys",
        "other": "Other Errors",
    }

    total = 0
    for key, label in labels.items():
        errs = errors_by_type.get(key, [])
        if not errs:
            continue
        total += len(errs)
        print(f"\n--- {label} ({len(errs)}) ---")
        for e in errs:
            print(f"  [{e['path']}] {e['message']}")

    return total


def main():
    check_dependencies()

    if len(sys.argv) > 1:
        config_path = Path(sys.argv[1]).resolve()
    else:
        config_path = Path.cwd() / ".delivery" / "config.yml"

    print(f"Config:  {config_path}")
    schema = load_schema()
    print(f"Schema:  loaded ({schema.get('title', 'unknown')})")

    config = load_config(config_path)

    errors_by_type = validate(config, schema)
    total = print_errors(errors_by_type)

    if total == 0:
        print("\nConfig is valid.")
        sys.exit(0)
    else:
        print(f"\nFound {total} validation error(s).")
        sys.exit(1)


if __name__ == "__main__":
    main()
