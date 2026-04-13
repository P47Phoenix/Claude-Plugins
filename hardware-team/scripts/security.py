#!/usr/bin/env python3
"""Security controls for the hardware-team plugin.

Provides:
- Path sanitization (safe_join API preventing traversal outside .hardware/)
- yaml.safe_load enforcement wrapper
- BOM data classification utilities
- State file semantic validation

Architecture references: SEC-01 through SEC-06, Sections 7.2, 14.1, 14.2.

Usage:
    from security import safe_join, sanitize_path_component, safe_yaml_load
    from security import classify_bom_field, validate_state_integrity
"""
import hashlib
import json
import os
import re
import sys
from pathlib import Path


# ---------------------------------------------------------------------------
# SEC-01: Path Sanitization
# ---------------------------------------------------------------------------

# Whitelist: only alphanumerics, dots, hyphens, and underscores.
SAFE_PATH_COMPONENT = re.compile(r'^[a-zA-Z0-9._-]+$')


def sanitize_path_component(value: str) -> str:
    """Validate a single path component against the whitelist.

    Raises ValueError if the value contains unsafe characters.
    Only alphanumerics, dots, hyphens, and underscores are permitted.

    Args:
        value: A single path component (directory or file name).

    Returns:
        The validated value (unchanged).

    Raises:
        ValueError: If the value contains characters outside the whitelist,
            including '/', '\\', '..', null bytes, or other unsafe chars.
    """
    if not value:
        raise ValueError("Empty path component is not permitted.")
    if not SAFE_PATH_COMPONENT.match(value):
        raise ValueError(
            f"HW-STA-005: Unsafe path component: '{value}'. "
            f"Only alphanumerics, dots, hyphens, and underscores are permitted."
        )
    # Extra guard: reject '..' even though regex already blocks '/'
    if value == ".." or value == ".":
        raise ValueError(
            f"HW-STA-005: Unsafe path component: '{value}'. "
            f"Relative path components are not permitted."
        )
    return value


def safe_join(base_dir: str, *components: str) -> str:
    """Join path components with sandbox validation.

    All components are validated against the whitelist, then the resolved
    path is checked to ensure it does not escape the base_dir sandbox.

    Args:
        base_dir: The sandbox root directory (e.g., '.hardware/').
        *components: Path components to join (each individually validated).

    Returns:
        The joined path string (not resolved -- preserves relative form).

    Raises:
        ValueError: If any component fails whitelist validation or if the
            resolved path escapes the base_dir sandbox (HW-STA-005).
    """
    for c in components:
        sanitize_path_component(c)

    candidate = os.path.join(base_dir, *components)
    resolved = os.path.realpath(candidate)
    base_resolved = os.path.realpath(base_dir)

    if not resolved.startswith(base_resolved + os.sep) and resolved != base_resolved:
        raise ValueError(
            f"HW-STA-005: Path traversal detected: '{candidate}' resolves to "
            f"'{resolved}' which is outside sandbox '{base_resolved}'."
        )
    return candidate


# ---------------------------------------------------------------------------
# SEC-03: YAML Safe Load Enforcement
# ---------------------------------------------------------------------------

def safe_yaml_load(text: str) -> dict | list | None:
    """Load YAML text using yaml.safe_load() exclusively.

    This wrapper enforces SEC-03: never use yaml.load(), yaml.FullLoader,
    or yaml.UnsafeLoader. Falls back to a minimal regex parser if PyYAML
    is not installed.

    Args:
        text: YAML-formatted string.

    Returns:
        Parsed YAML content (dict, list, or None for empty documents).

    Raises:
        ValueError: If YAML contains unsafe constructs (!!python/object tags).
        RuntimeError: If the YAML cannot be parsed and no fallback is available.
    """
    # Pre-scan for dangerous YAML tags regardless of parser.
    dangerous_tags = re.findall(r'!!python/\w+', text)
    if dangerous_tags:
        raise ValueError(
            f"SEC-03: Unsafe YAML tags detected: {dangerous_tags}. "
            f"YAML deserialization attack blocked."
        )

    try:
        import yaml
        return yaml.safe_load(text)
    except ImportError:
        # Minimal fallback: parse simple key-value YAML.
        return _minimal_yaml_parse(text)


def _minimal_yaml_parse(text: str) -> dict:
    """Minimal YAML parser for simple config files without PyYAML.

    Handles single-level key: value pairs and simple lists.
    NOT a full YAML parser -- only for degraded-mode operation.
    """
    result = {}
    current_key = None

    for line in text.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue

        # List item under a key.
        if stripped.startswith("- ") and current_key is not None:
            if current_key not in result:
                result[current_key] = []
            if isinstance(result[current_key], list):
                result[current_key].append(stripped[2:].strip().strip('"').strip("'"))
            continue

        # Key-value pair.
        kv_match = re.match(r'^([a-zA-Z_][a-zA-Z0-9_]*)\s*:\s*(.*)', stripped)
        if kv_match:
            key = kv_match.group(1)
            val = kv_match.group(2).strip().strip('"').strip("'")
            current_key = key
            if val:
                # Try to parse as number or boolean.
                if val.lower() in ("true", "yes"):
                    result[key] = True
                elif val.lower() in ("false", "no"):
                    result[key] = False
                else:
                    try:
                        result[key] = int(val)
                    except ValueError:
                        try:
                            result[key] = float(val)
                        except ValueError:
                            result[key] = val
            else:
                result[key] = None
        else:
            current_key = None

    return result


# ---------------------------------------------------------------------------
# SEC-02: BOM Data Classification
# ---------------------------------------------------------------------------

# Classification levels for BOM fields.
class BOMClassification:
    """BOM data classification per SEC-02 / architecture Section 14.2."""
    SENSITIVE = "SENSITIVE"
    INTERNAL = "INTERNAL"
    PUBLIC = "PUBLIC"


# Field-to-classification mapping.
BOM_FIELD_CLASSIFICATION = {
    # SENSITIVE fields -- must not be committed to public repos or captured in memory.
    "unit_price": BOMClassification.SENSITIVE,
    "total_cost": BOMClassification.SENSITIVE,
    "account_id": BOMClassification.SENSITIVE,
    "negotiated_price": BOMClassification.SENSITIVE,
    "discount_rate": BOMClassification.SENSITIVE,
    "supplier_quote": BOMClassification.SENSITIVE,
    # INTERNAL fields -- may be committed to private repos.
    "supplier_name": BOMClassification.INTERNAL,
    "mpn": BOMClassification.INTERNAL,
    "datasheet_url": BOMClassification.INTERNAL,
    "stock_level": BOMClassification.INTERNAL,
    # PUBLIC fields -- no restrictions.
    "description": BOMClassification.PUBLIC,
    "package": BOMClassification.PUBLIC,
    "footprint": BOMClassification.PUBLIC,
    "reference": BOMClassification.PUBLIC,
    "quantity": BOMClassification.PUBLIC,
    "value": BOMClassification.PUBLIC,
}


def classify_bom_field(field_name: str) -> str:
    """Classify a BOM field by its data sensitivity level.

    Args:
        field_name: The BOM field name (e.g., 'unit_price', 'description').

    Returns:
        One of BOMClassification.SENSITIVE, INTERNAL, or PUBLIC.
        Unknown fields default to INTERNAL (safe default).
    """
    normalized = field_name.lower().replace(" ", "_").replace("-", "_")
    return BOM_FIELD_CLASSIFICATION.get(normalized, BOMClassification.INTERNAL)


def is_sensitive_bom_field(field_name: str) -> bool:
    """Check if a BOM field contains commercially sensitive data.

    Args:
        field_name: The BOM field name.

    Returns:
        True if the field is classified as SENSITIVE.
    """
    return classify_bom_field(field_name) == BOMClassification.SENSITIVE


# Pricing pattern detector for memory no-pricing filter (SEC-02).
PRICING_PATTERNS = re.compile(
    r'(?:'
    r'\$\s*\d+[\d,.]*'           # $0.12, $ 1,234.56
    r'|EUR\s*\d+[\d,.]*'         # EUR 1.50
    r'|GBP\s*\d+[\d,.]*'         # GBP 2.00
    r'|JPY\s*\d+[\d,.]*'         # JPY 150
    r'|\d+[\d,.]*\s*/\s*unit'    # 0.12/unit
    r'|quoted\s+at\s+\S+'        # quoted at $0.08
    r'|priced\s+at\s+\S+'        # priced at EUR 1.50
    r'|costs?\s+\$\S+'           # cost $1.20, costs $1.20
    r'|per\s+unit\s+\$?\d+'      # per unit $0.08
    r')',
    re.IGNORECASE,
)


def redact_pricing(text: str) -> tuple[str, int]:
    """Redact pricing data from text (memory no-pricing filter).

    Scans for patterns matching pricing data and replaces them with
    [PRICE REDACTED]. Logs HW-SEC-001 count.

    Args:
        text: The text to scan and redact.

    Returns:
        Tuple of (redacted_text, redaction_count).
    """
    count = len(PRICING_PATTERNS.findall(text))
    if count == 0:
        return text, 0

    redacted = PRICING_PATTERNS.sub("[PRICE REDACTED]", text)
    return redacted, count


# ---------------------------------------------------------------------------
# SEC-05: State File Semantic Validation
# ---------------------------------------------------------------------------

REQUIRED_STATE_FIELDS = ("pipeline_id", "status", "current_stage", "stages_completed")

VALID_STATUSES = (
    "in_progress", "paused", "paused_awaiting_human",
    "paused_dispatch_error", "completed", "aborted",
)


def compute_integrity_hash(stages_completed: list, gates: list | dict) -> str:
    """Compute SHA-256 integrity hash over state arrays.

    Used for lightweight tamper detection (SEC-05). The hash covers
    stages_completed and gates to detect manual edits.

    Args:
        stages_completed: List of completed stage names/numbers.
        gates: Gate results (list or dict).

    Returns:
        Hex-encoded SHA-256 hash string.
    """
    payload = json.dumps(
        {"stages_completed": stages_completed, "gates": gates},
        sort_keys=True,
        separators=(",", ":"),
    )
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def validate_state(state_path: str | Path) -> tuple[bool, list[str]]:
    """Validate a .hardware/state.md file for structural correctness.

    Checks:
    1. File is readable
    2. YAML frontmatter is parseable
    3. Required fields are present
    4. Status value is valid
    5. Integrity hash matches (advisory warning, not blocking)

    Args:
        state_path: Path to the state.md file.

    Returns:
        Tuple of (valid: bool, errors: list[str]).
        valid is True if the state file is structurally sound.
        errors contains any issues found (warnings are included but
        do not set valid=False if they are advisory-only).
    """
    state_path = Path(state_path)
    errors = []

    if not state_path.exists():
        return False, ["State file does not exist."]

    try:
        content = state_path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as exc:
        return False, [f"Cannot read state file: {exc}"]

    # Parse YAML frontmatter.
    fm_match = re.match(r'^---\s*\n(.*?)\n---', content, re.DOTALL)
    if not fm_match:
        return False, [
            "STATE_FILE_CORRUPTED: No YAML frontmatter found. "
            "Expected --- delimiters."
        ]

    fm_text = fm_match.group(1)
    try:
        state = safe_yaml_load(fm_text)
    except (ValueError, RuntimeError) as exc:
        return False, [
            f"STATE_FILE_CORRUPTED: YAML parse error: {exc}"
        ]

    if not isinstance(state, dict):
        return False, [
            "STATE_FILE_CORRUPTED: Frontmatter did not parse as a mapping."
        ]

    # Check required fields.
    missing = [f for f in REQUIRED_STATE_FIELDS if f not in state]
    if missing:
        errors.append(
            f"STATE_FILE_INCOMPLETE: Missing required fields: {missing}"
        )
        return False, errors

    # Validate status value.
    status = state.get("status", "")
    if status not in VALID_STATUSES:
        errors.append(
            f"Invalid status '{status}'. "
            f"Valid values: {', '.join(VALID_STATUSES)}"
        )

    # Integrity hash check (advisory).
    stored_hash = state.get("_integrity_hash", "")
    if stored_hash:
        stages = state.get("stages_completed", [])
        gates = state.get("gates", [])
        computed = compute_integrity_hash(stages, gates)
        if computed != stored_hash:
            errors.append(
                "WARNING: State file appears to have been manually edited. "
                "Gate results may not reflect actual pipeline execution."
            )

    # If we only have advisory warnings, file is still valid.
    blocking_errors = [
        e for e in errors
        if not e.startswith("WARNING:")
    ]
    return len(blocking_errors) == 0, errors


# ---------------------------------------------------------------------------
# CLI entry point for standalone validation.
# ---------------------------------------------------------------------------

def main():
    """Run security validation checks from the command line."""
    if len(sys.argv) < 2:
        print("Usage: python security.py <command> [args]")
        print("Commands:")
        print("  validate-state <path>    Validate a state.md file")
        print("  check-path <component>   Validate a path component")
        print("  redact-pricing <text>    Redact pricing from text")
        print("  classify-field <name>    Classify a BOM field")
        sys.exit(1)

    command = sys.argv[1]

    if command == "validate-state" and len(sys.argv) >= 3:
        valid, errors = validate_state(sys.argv[2])
        for e in errors:
            print(e)
        sys.exit(0 if valid else 1)

    elif command == "check-path" and len(sys.argv) >= 3:
        try:
            sanitize_path_component(sys.argv[2])
            print(f"OK: '{sys.argv[2]}' is a safe path component.")
        except ValueError as exc:
            print(str(exc))
            sys.exit(1)

    elif command == "redact-pricing" and len(sys.argv) >= 3:
        text = " ".join(sys.argv[2:])
        redacted, count = redact_pricing(text)
        print(f"Redactions: {count}")
        print(redacted)

    elif command == "classify-field" and len(sys.argv) >= 3:
        classification = classify_bom_field(sys.argv[2])
        print(f"{sys.argv[2]}: {classification}")

    else:
        print(f"Unknown command: {command}")
        sys.exit(1)


if __name__ == "__main__":
    main()
