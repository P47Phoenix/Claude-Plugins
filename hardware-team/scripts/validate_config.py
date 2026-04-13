#!/usr/bin/env python3
"""
Validate .hardware/config.yml against the hardware-team config schema v1.0.

Usage:
    python hardware-team/scripts/validate_config.py [path/to/.hardware/config.yml]

If no path is provided, defaults to .hardware/config.yml in the current directory.

Exit codes:
    0 -- Config is valid (or valid with warnings using defaults)
    1 -- Config file not found or not readable
    2 -- Config has structural errors (not valid YAML)

Note: Invalid field values produce WARNINGS but never cause exit code != 0,
because the pipeline must never fail due to config errors (FR-004, NFR-006).
"""

import sys
import os
import yaml  # stdlib (PyYAML is NOT required -- yaml is part of CPython... wait, no)

# ---------------------------------------------------------------------------
# PyYAML availability check
# yaml module is NOT in the Python stdlib. However, it is almost universally
# available. If missing, we fall back to a minimal YAML subset parser.
# ---------------------------------------------------------------------------
try:
    import yaml as _yaml

    def safe_load(text):
        return _yaml.safe_load(text)

except ImportError:
    # Minimal fallback: parse simple key-value YAML without PyYAML.
    # This handles the subset of YAML used by .hardware/config.yml.
    import json
    import re

    def safe_load(text):
        """Minimal YAML parser for simple config files. Handles scalars, lists, and
        one level of nesting. NOT a full YAML parser."""
        result = {}
        current_key = None
        for line in text.splitlines():
            stripped = line.strip()
            if not stripped or stripped.startswith("#"):
                continue
            # List item under a key
            if stripped.startswith("- "):
                if current_key and current_key in result and isinstance(result[current_key], list):
                    result[current_key].append(_parse_scalar(stripped[2:].strip()))
                continue
            # Nested key (indented)
            indent = len(line) - len(line.lstrip())
            if indent > 0 and ":" in stripped:
                parts = stripped.split(":", 1)
                key = parts[0].strip()
                val = parts[1].strip() if len(parts) > 1 else ""
                if current_key is not None:
                    if not isinstance(result.get(current_key), dict):
                        result[current_key] = {}
                    if val:
                        result[current_key][key] = _parse_scalar(val)
                continue
            # Top-level key
            if ":" in stripped:
                parts = stripped.split(":", 1)
                key = parts[0].strip()
                val = parts[1].strip() if len(parts) > 1 else ""
                if val:
                    result[key] = _parse_scalar(val)
                elif val == "":
                    # Could be a list or nested dict -- start as list
                    result[key] = []
                current_key = key
        return result

    def _parse_scalar(val):
        """Parse a YAML scalar value."""
        # Remove inline comments
        if " #" in val:
            val = val[:val.index(" #")].strip()
        # Remove quotes
        if (val.startswith('"') and val.endswith('"')) or (val.startswith("'") and val.endswith("'")):
            return val[1:-1]
        # Booleans
        if val.lower() in ("true", "yes"):
            return True
        if val.lower() in ("false", "no"):
            return False
        # Null
        if val.lower() in ("null", "~", ""):
            return None
        # Numbers
        try:
            if "." in val:
                return float(val)
            return int(val)
        except ValueError:
            pass
        # Inline list [a, b, c]
        if val.startswith("[") and val.endswith("]"):
            items = val[1:-1].split(",")
            return [_parse_scalar(i.strip()) for i in items if i.strip()]
        return val


# ---------------------------------------------------------------------------
# Schema definition
# ---------------------------------------------------------------------------

KNOWN_SCHEMA_VERSIONS = {"1.0"}

VALID_TARGET_FABS = {"jlcpcb", "pcbway", "custom"}
VALID_COMPLIANCE_REGIONS = {"fcc", "ce", "ul", "rohs", "reach", "none"}
VALID_PRODUCTION_VOLUMES = {"prototype", "small-batch", "production"}
VALID_BOARD_LAYERS = {1, 2, 4, 6, 8}
VALID_GATE_STRICTNESS = {"strict", "standard", "relaxed"}

DEFAULTS = {
    "schema_version": "1.0",
    "target_fab": "jlcpcb",
    "custom_fab_name": "",
    "compliance_regions": [],
    "bom_budget": None,
    "second_source_required": False,
    "production_volume": "prototype",
    "board_layers": 2,
    "dependencies": {"kicad_happy_version": ">=1.2.0"},
    "rework": {"max_rework_iterations": 3, "max_total_reworks": 10},
    "gate_strictness": "standard",
    "pipeline": {"staleness_warning_days": 7, "staleness_critical_days": 30},
    "review": {"schematic_review_passes": 2, "design_review_board": True},
    "memory": {"entries_limit": 100},
}


# ---------------------------------------------------------------------------
# Validation
# ---------------------------------------------------------------------------

class ValidationResult:
    def __init__(self):
        self.errors = []    # Structural errors (bad YAML, missing required fields)
        self.warnings = []  # Invalid values (pipeline uses defaults)
        self.info = []      # Informational messages

    @property
    def is_valid(self):
        """Config is valid if there are no structural errors.
        Warnings are acceptable -- pipeline uses defaults for invalid fields."""
        return len(self.errors) == 0

    def add_error(self, msg):
        self.errors.append(msg)

    def add_warning(self, msg):
        self.warnings.append(msg)

    def add_info(self, msg):
        self.info.append(msg)


def _get_nested(config, *keys, default=None):
    """Safely get a nested value from a dict."""
    current = config
    for key in keys:
        if not isinstance(current, dict):
            return default
        current = current.get(key, default)
        if current is default:
            return default
    return current


def validate_config(config):
    """Validate a parsed config dict against the schema.

    Returns a ValidationResult. Warnings indicate invalid values where
    defaults will be used. Errors indicate structural problems.
    """
    result = ValidationResult()

    if not isinstance(config, dict):
        result.add_error("Config must be a YAML mapping (dict), got: %s" % type(config).__name__)
        return result

    # --- Required fields ---
    schema_version = config.get("schema_version")
    if schema_version is None:
        result.add_error("Missing required field: schema_version")
    elif str(schema_version) not in KNOWN_SCHEMA_VERSIONS:
        result.add_warning(
            "Unknown schema_version: '%s'. Known versions: %s. "
            "Pipeline will attempt to proceed."
            % (schema_version, ", ".join(sorted(KNOWN_SCHEMA_VERSIONS)))
        )

    project_name = config.get("project_name")
    if project_name is None:
        result.add_error("Missing required field: project_name")
    elif not isinstance(project_name, str) or not project_name.strip():
        result.add_error("project_name must be a non-empty string, got: %r" % project_name)
    elif len(project_name) > 100:
        result.add_warning("project_name exceeds 100 characters (using first 100)")

    # --- Optional enum fields ---
    target_fab = config.get("target_fab")
    if target_fab is not None:
        if str(target_fab).lower() not in VALID_TARGET_FABS:
            result.add_warning(
                "Invalid target_fab: '%s'. Valid: %s. Using default: jlcpcb"
                % (target_fab, ", ".join(sorted(VALID_TARGET_FABS)))
            )
        elif str(target_fab).lower() == "custom":
            custom_name = config.get("custom_fab_name")
            if not custom_name or not isinstance(custom_name, str) or not custom_name.strip():
                result.add_warning(
                    "target_fab is 'custom' but custom_fab_name is empty. "
                    "Set custom_fab_name to identify your fab house."
                )

    # --- compliance_regions ---
    regions = config.get("compliance_regions")
    if regions is not None:
        if not isinstance(regions, list):
            result.add_warning(
                "compliance_regions must be a list, got: %s. Using default: []"
                % type(regions).__name__
            )
        else:
            for region in regions:
                if str(region).lower() not in VALID_COMPLIANCE_REGIONS:
                    result.add_warning(
                        "Invalid compliance region: '%s'. Valid: %s"
                        % (region, ", ".join(sorted(VALID_COMPLIANCE_REGIONS)))
                    )

    # --- bom_budget ---
    bom_budget = config.get("bom_budget")
    if bom_budget is not None:
        if not isinstance(bom_budget, (int, float)):
            result.add_warning(
                "bom_budget must be a positive number or null, got: %r. Using default: null"
                % bom_budget
            )
        elif bom_budget <= 0:
            result.add_warning(
                "bom_budget must be positive, got: %s. Using default: null" % bom_budget
            )

    # --- second_source_required ---
    ssr = config.get("second_source_required")
    if ssr is not None and not isinstance(ssr, bool):
        result.add_warning(
            "second_source_required must be a boolean, got: %r. Using default: false" % ssr
        )

    # --- production_volume ---
    pv = config.get("production_volume")
    if pv is not None and str(pv).lower() not in VALID_PRODUCTION_VOLUMES:
        result.add_warning(
            "Invalid production_volume: '%s'. Valid: %s. Using default: prototype"
            % (pv, ", ".join(sorted(VALID_PRODUCTION_VOLUMES)))
        )

    # --- board_layers ---
    bl = config.get("board_layers")
    if bl is not None:
        if not isinstance(bl, int) or bl not in VALID_BOARD_LAYERS:
            result.add_warning(
                "Invalid board_layers: %r. Valid: %s. Using default: 2"
                % (bl, ", ".join(str(x) for x in sorted(VALID_BOARD_LAYERS)))
            )

    # --- dependencies.kicad_happy_version ---
    dep_version = _get_nested(config, "dependencies", "kicad_happy_version")
    if dep_version is not None and not isinstance(dep_version, str):
        result.add_warning(
            "dependencies.kicad_happy_version must be a string, got: %r. Using default: '>=1.2.0'"
            % dep_version
        )

    # --- rework.max_rework_iterations ---
    mri = _get_nested(config, "rework", "max_rework_iterations")
    if mri is not None:
        if not isinstance(mri, int) or mri < 1:
            result.add_warning(
                "rework.max_rework_iterations must be a positive integer >= 1, got: %r. Using default: 3"
                % mri
            )

    # --- rework.max_total_reworks ---
    mtr = _get_nested(config, "rework", "max_total_reworks")
    if mtr is not None:
        if not isinstance(mtr, int) or mtr < 1:
            result.add_warning(
                "rework.max_total_reworks must be a positive integer >= 1, got: %r. Using default: 10"
                % mtr
            )

    # --- gate_strictness ---
    gs = config.get("gate_strictness")
    if gs is not None and str(gs).lower() not in VALID_GATE_STRICTNESS:
        result.add_warning(
            "Invalid gate_strictness: '%s'. Valid: %s. Using default: standard"
            % (gs, ", ".join(sorted(VALID_GATE_STRICTNESS)))
        )

    # --- pipeline.staleness_warning_days ---
    swd = _get_nested(config, "pipeline", "staleness_warning_days")
    if swd is not None:
        if not isinstance(swd, int) or swd < 1:
            result.add_warning(
                "pipeline.staleness_warning_days must be a positive integer >= 1, got: %r. Using default: 7"
                % swd
            )

    # --- pipeline.staleness_critical_days ---
    scd = _get_nested(config, "pipeline", "staleness_critical_days")
    if scd is not None:
        if not isinstance(scd, int) or scd < 1:
            result.add_warning(
                "pipeline.staleness_critical_days must be a positive integer >= 1, got: %r. Using default: 30"
                % scd
            )

    # Cross-field: critical > warning
    if swd is not None and scd is not None:
        if isinstance(swd, int) and isinstance(scd, int) and swd >= 1 and scd >= 1:
            if scd <= swd:
                result.add_warning(
                    "pipeline.staleness_critical_days (%d) must be greater than "
                    "staleness_warning_days (%d). Using defaults: warning=7, critical=30"
                    % (scd, swd)
                )

    # --- review.schematic_review_passes ---
    srp = _get_nested(config, "review", "schematic_review_passes")
    if srp is not None:
        if not isinstance(srp, int) or srp < 1 or srp > 5:
            result.add_warning(
                "review.schematic_review_passes must be an integer 1-5, got: %r. Using default: 2"
                % srp
            )

    # --- review.design_review_board ---
    drb = _get_nested(config, "review", "design_review_board")
    if drb is not None and not isinstance(drb, bool):
        result.add_warning(
            "review.design_review_board must be a boolean, got: %r. Using default: true" % drb
        )

    # --- memory.entries_limit ---
    mel = _get_nested(config, "memory", "entries_limit")
    if mel is not None:
        if not isinstance(mel, int) or mel < 10:
            result.add_warning(
                "memory.entries_limit must be a positive integer >= 10, got: %r. Using default: 100"
                % mel
            )

    # --- Info: report unknown top-level keys (forward compatibility -- ignored, not an error) ---
    known_top_keys = {
        "schema_version", "project_name", "target_fab", "custom_fab_name",
        "compliance_regions", "bom_budget", "second_source_required",
        "production_volume", "board_layers", "dependencies", "rework",
        "gate_strictness", "pipeline", "review", "memory",
    }
    unknown = set(config.keys()) - known_top_keys
    if unknown:
        result.add_info(
            "Unknown top-level keys (ignored for forward compatibility): %s"
            % ", ".join(sorted(unknown))
        )

    return result


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    # Determine config path
    if len(sys.argv) > 1:
        config_path = sys.argv[1]
    else:
        config_path = os.path.join(os.getcwd(), ".hardware", "config.yml")

    # Check file exists
    if not os.path.isfile(config_path):
        print("ERROR: Config file not found: %s" % config_path)
        print("Run `hw-setup` to create one.")
        sys.exit(1)

    # Read and parse
    try:
        with open(config_path, "r", encoding="utf-8") as f:
            content = f.read()
    except (IOError, OSError) as e:
        print("ERROR: Cannot read config file: %s" % e)
        sys.exit(1)

    try:
        config = safe_load(content)
    except Exception as e:
        print("ERROR: Invalid YAML in config file: %s" % e)
        sys.exit(2)

    if config is None:
        print("ERROR: Config file is empty.")
        sys.exit(2)

    # Validate
    result = validate_config(config)

    # Report
    if result.info:
        for msg in result.info:
            print("INFO: %s" % msg)

    if result.warnings:
        for msg in result.warnings:
            print("WARNING: %s" % msg)

    if result.errors:
        for msg in result.errors:
            print("ERROR: %s" % msg)
        print("\nConfig has %d error(s) and %d warning(s)." % (len(result.errors), len(result.warnings)))
        sys.exit(2)

    if result.warnings:
        print("\nConfig valid with %d warning(s). Pipeline will use defaults for invalid fields." % len(result.warnings))
    else:
        print("Config valid. All fields match schema v1.0.")

    sys.exit(0)


if __name__ == "__main__":
    main()
