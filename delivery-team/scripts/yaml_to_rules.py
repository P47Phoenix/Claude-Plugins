"""
YAML-to-JSON Translation Layer (C3)

Translates structured config data (pre-parsed YAML dicts) into JSON rule
override structures consumable by DeliveryRulesAdapter.

Zero external dependencies — Python stdlib only.  This module does NOT parse
YAML itself; it receives Python dicts from the orchestrator.

Key responsibilities:
  1. Validate rule values against expected types.
  2. Detect YAML coercion artefacts (yes/no → bool, 3.10 → 3.1, on/off → bool).
  3. Convert config keys to the JSON override schema the adapter expects.
  4. In strict mode, coercion detections become hard errors.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

__all__ = [
    "translate_config",
    "translate_config_to_rules",
    "validate_rule_value",
    "TranslationResult",
    "CoercionWarning",
    "ValidationResult",
]

# ---------------------------------------------------------------------------
# Data classes
# ---------------------------------------------------------------------------

@dataclass
class CoercionWarning:
    """Record of a YAML type coercion detected during translation."""
    key: str
    raw_value: Any
    coerced_value: Any
    expected_type: str


@dataclass
class TranslationResult:
    """Result of translating config overrides to rule structures."""
    rules: Dict[str, Any] = field(default_factory=dict)
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    coercions: List[CoercionWarning] = field(default_factory=list)

    # Alias so downstream callers using the architecture name still work.
    @property
    def overrides(self) -> Dict[str, Any]:
        return self.rules


@dataclass
class ValidationResult:
    """Result of validating a single rule value."""
    valid: bool
    value: Any
    message: str


# ---------------------------------------------------------------------------
# Constants / schema expectations
# ---------------------------------------------------------------------------

VALID_PRESETS = ("solo", "standard", "strict", "none")

VALID_PROJECT_TYPES = (
    "GREENFIELD", "FEATURE", "BUG_FIX", "GAME_DEV", "SPIKE", "DOCS_ONLY",
)

VALID_STAGES = (
    "idea", "refine", "design", "architect", "plan", "development", "uat",
)

VALID_DEPTHS = ("full", "light", "skip")

VALID_ESCALATION_SENSITIVITIES = ("conservative", "balanced", "aggressive")

VALID_SEVERITIES = ("blocker", "critical", "major", "minor", "info")

# Map from config key path to expected Python type string.
_TYPE_MAP: Dict[str, str] = {
    "preset": "string",
    "enabled": "bool",
    "strict_mode": "bool",
    "escalation_sensitivity": "string",
    "pass_threshold": "map",
    "routing_overrides": "map",
    "gate_overrides": "map",
    "required_validators": "map",
    "escalation": "map",
    "dod_overrides": "map",
    "limits_overrides": "map",
    "custom": "list",
}

# Python type string → acceptable Python types
_PY_TYPES: Dict[str, tuple] = {
    "string": (str,),
    "int": (int,),
    "float": (int, float),
    "bool": (bool,),
    "list": (list,),
    "map": (dict,),
}


# ---------------------------------------------------------------------------
# YAML coercion detection helpers
# ---------------------------------------------------------------------------

# Values that YAML 1.1 silently coerces to booleans.
_YAML_BOOL_STRINGS = {
    "yes", "no", "on", "off", "true", "false",
    "Yes", "No", "On", "Off", "True", "False",
    "YES", "NO", "ON", "OFF", "TRUE", "FALSE",
    "y", "n", "Y", "N",
}


def _check_bool_coercion(key: str, value: Any, expected_type: str) -> Optional[CoercionWarning]:
    """Detect when YAML silently converted a string like 'yes' to a bool."""
    if isinstance(value, bool) and expected_type != "bool":
        # The value was likely a bare yes/no/on/off in the YAML source.
        return CoercionWarning(
            key=key,
            raw_value="yes/no/on/off (YAML boolean)",
            coerced_value=value,
            expected_type=expected_type,
        )
    return None


def _check_float_coercion(key: str, value: Any, expected_type: str) -> Optional[CoercionWarning]:
    """Detect trailing-zero float truncation (e.g. 3.10 → 3.1)."""
    if isinstance(value, float) and expected_type in ("float", "string"):
        # We can't know the original text, but if the float has no fractional
        # part beyond one decimal (like 3.1) it *might* have been 3.10.
        # We flag all floats when a string was expected, or floats that look
        # like they lost trailing zeros.
        if expected_type == "string":
            return CoercionWarning(
                key=key,
                raw_value=value,
                coerced_value=value,
                expected_type=expected_type,
            )
        # For numeric fields, check if the value looks like it lost precision
        # (e.g. 3.1 might have been 3.10 — we can't be certain, but we warn).
        str_val = str(value)
        if "." in str_val:
            decimals = str_val.split(".")[1]
            if len(decimals) == 1 and decimals != "0":
                return CoercionWarning(
                    key=key,
                    raw_value=f"{value} (possible trailing-zero truncation, e.g. {value}0)",
                    coerced_value=value,
                    expected_type=expected_type,
                )
    return None


def _detect_coercion(key: str, value: Any, expected_type: str) -> Optional[CoercionWarning]:
    """Run all coercion detectors and return the first match, or None."""
    c = _check_bool_coercion(key, value, expected_type)
    if c:
        return c
    c = _check_float_coercion(key, value, expected_type)
    if c:
        return c
    return None


# ---------------------------------------------------------------------------
# Public: validate a single rule value
# ---------------------------------------------------------------------------

def validate_rule_value(key: str, value: Any, expected_type: str) -> ValidationResult:
    """
    Type-check a single value against a schema expectation.

    Args:
        key: Dotted config key path (for error messages).
        value: The Python value to validate.
        expected_type: One of 'string', 'int', 'float', 'bool', 'list', 'map'.

    Returns:
        ValidationResult indicating whether the value is valid.
    """
    acceptable = _PY_TYPES.get(expected_type)
    if acceptable is None:
        return ValidationResult(
            valid=False,
            value=value,
            message=f"Unknown expected type '{expected_type}' for key '{key}'.",
        )

    # Special case: bool is subclass of int in Python, so reject bools when
    # an int or float is expected.
    if isinstance(value, bool) and expected_type in ("int", "float"):
        return ValidationResult(
            valid=False,
            value=value,
            message=f"{key} must be {expected_type}, got bool.",
        )

    if not isinstance(value, acceptable):
        return ValidationResult(
            valid=False,
            value=value,
            message=f"{key} must be {expected_type}, got {type(value).__name__}.",
        )

    return ValidationResult(valid=True, value=value, message="")


# ---------------------------------------------------------------------------
# Internal: config-to-JSON mapping functions
# ---------------------------------------------------------------------------

def _translate_preset(
    value: Any, result: TranslationResult, strict: bool,
) -> None:
    """Translate rules.preset."""
    # Check coercion BEFORE type validation — the whole point is that YAML
    # delivered the wrong type (e.g. bool True instead of string "yes").
    coercion = _detect_coercion("preset", value, "string")
    if coercion:
        result.coercions.append(coercion)
        msg = (
            f"[WARN] YAML type coercion detected for key preset: "
            f"value {coercion.raw_value} interpreted as {coercion.coerced_value}. "
            f"Use quotes for literal strings."
        )
        if strict:
            result.errors.append(msg.replace("[WARN]", "[ERROR]"))
            return
        result.warnings.append(msg)
        # In default mode, preserve the coerced value but still validate below.

    vr = validate_rule_value("preset", value, "string")
    if not vr.valid:
        # If coercion was detected, the type mismatch is expected — already warned.
        if not coercion:
            result.errors.append(vr.message)
        return

    if value not in VALID_PRESETS:
        result.errors.append(
            f"preset must be one of: {', '.join(VALID_PRESETS)}. Got '{value}'."
        )
        return

    result.rules["preset"] = value


def _translate_enabled(
    value: Any, result: TranslationResult, strict: bool,
) -> None:
    """Translate rules.enabled feature flag."""
    vr = validate_rule_value("enabled", value, "bool")
    if not vr.valid:
        result.errors.append(vr.message)
        return

    # Boolean coercion is expected for this key, but we still flag it.
    # Since bool IS the expected type here, no coercion is detected.
    result.rules["enabled"] = value


def _translate_pass_threshold(
    value: Any, result: TranslationResult, strict: bool,
) -> None:
    """Translate rules.pass_threshold → gates.<stage>_dod.pass_threshold."""
    vr = validate_rule_value("pass_threshold", value, "map")
    if not vr.valid:
        result.errors.append(vr.message)
        return

    gates = result.rules.setdefault("gates", {})

    for stage, threshold in value.items():
        full_key = f"pass_threshold.{stage}"

        # Detect coercion on the threshold value.
        coercion = _detect_coercion(full_key, threshold, "float")
        if coercion:
            result.coercions.append(coercion)
            msg = (
                f"[WARN] YAML type coercion detected for key {full_key}: "
                f"value {coercion.raw_value} interpreted as {coercion.coerced_value}. "
                f"Use quotes for literal strings."
            )
            if strict:
                result.errors.append(msg.replace("[WARN]", "[ERROR]"))
                continue
            result.warnings.append(msg)

        # Validate numeric type.
        vr_thresh = validate_rule_value(full_key, threshold, "float")
        if not vr_thresh.valid:
            result.errors.append(vr_thresh.message)
            continue

        gate_key = f"{stage}_dod"
        gate = gates.setdefault(gate_key, {})
        gate["pass_threshold"] = threshold


def _translate_routing_overrides(
    value: Any, result: TranslationResult, strict: bool,
) -> None:
    """Translate rules.routing_overrides → routing.<type>.<stage>."""
    vr = validate_rule_value("routing_overrides", value, "map")
    if not vr.valid:
        result.errors.append(vr.message)
        return

    routing = result.rules.setdefault("routing", {})

    for project_type, stage_map in value.items():
        if not isinstance(stage_map, dict):
            result.errors.append(
                f"routing_overrides.{project_type} must be map, "
                f"got {type(stage_map).__name__}."
            )
            continue

        type_routing = routing.setdefault(project_type, {})

        for stage, depth in stage_map.items():
            full_key = f"routing_overrides.{project_type}.{stage}"

            coercion = _detect_coercion(full_key, depth, "string")
            if coercion:
                result.coercions.append(coercion)
                msg = (
                    f"[WARN] YAML type coercion detected for key {full_key}: "
                    f"value {coercion.raw_value} interpreted as {coercion.coerced_value}. "
                    f"Use quotes for literal strings."
                )
                if strict:
                    result.errors.append(msg.replace("[WARN]", "[ERROR]"))
                    continue
                result.warnings.append(msg)

            vr_depth = validate_rule_value(full_key, depth, "string")
            if not vr_depth.valid:
                if not coercion:
                    result.errors.append(vr_depth.message)
                continue

            if depth not in VALID_DEPTHS:
                result.errors.append(
                    f"{full_key} must be one of: {', '.join(VALID_DEPTHS)}. "
                    f"Got '{depth}'."
                )
                continue

            type_routing[stage] = depth


def _translate_gate_overrides(
    value: Any, result: TranslationResult, strict: bool,
) -> None:
    """Translate rules.gate_overrides → gates.<stage>_dod.<criterion>."""
    vr = validate_rule_value("gate_overrides", value, "map")
    if not vr.valid:
        result.errors.append(vr.message)
        return

    gates = result.rules.setdefault("gates", {})

    for stage, criteria_map in value.items():
        if not isinstance(criteria_map, dict):
            result.errors.append(
                f"gate_overrides.{stage} must be map, "
                f"got {type(criteria_map).__name__}."
            )
            continue

        gate_key = f"{stage}_dod"
        gate = gates.setdefault(gate_key, {})
        criteria = gate.setdefault("criteria_overrides", {})

        for criterion, severity in criteria_map.items():
            full_key = f"gate_overrides.{stage}.{criterion}"

            coercion = _detect_coercion(full_key, severity, "string")
            if coercion:
                result.coercions.append(coercion)
                msg = (
                    f"[WARN] YAML type coercion detected for key {full_key}: "
                    f"value {coercion.raw_value} interpreted as "
                    f"{coercion.coerced_value}. Use quotes for literal strings."
                )
                if strict:
                    result.errors.append(msg.replace("[WARN]", "[ERROR]"))
                    continue
                result.warnings.append(msg)

            vr_sev = validate_rule_value(full_key, severity, "string")
            if not vr_sev.valid:
                if not coercion:
                    result.errors.append(vr_sev.message)
                continue

            if severity not in VALID_SEVERITIES:
                result.errors.append(
                    f"{full_key} must be one of: {', '.join(VALID_SEVERITIES)}. "
                    f"Got '{severity}'."
                )
                continue

            criteria[criterion] = severity


def _translate_escalation(
    value: Any, result: TranslationResult, strict: bool,
) -> None:
    """Translate rules.escalation.* → escalation thresholds."""
    vr = validate_rule_value("escalation", value, "map")
    if not vr.valid:
        result.errors.append(vr.message)
        return

    escalation = result.rules.setdefault("escalation", {})

    for sub_key, sub_value in value.items():
        full_key = f"escalation.{sub_key}"

        coercion = _detect_coercion(full_key, sub_value, "int")
        if coercion:
            result.coercions.append(coercion)
            msg = (
                f"[WARN] YAML type coercion detected for key {full_key}: "
                f"value {coercion.raw_value} interpreted as {coercion.coerced_value}. "
                f"Use quotes for literal strings."
            )
            if strict:
                result.errors.append(msg.replace("[WARN]", "[ERROR]"))
                continue
            result.warnings.append(msg)

        vr_sub = validate_rule_value(full_key, sub_value, "int")
        if not vr_sub.valid:
            result.errors.append(vr_sub.message)
            continue

        escalation[sub_key] = sub_value


def _translate_escalation_sensitivity(
    value: Any, result: TranslationResult, strict: bool,
) -> None:
    """Translate rules.escalation_sensitivity → escalation.sensitivity."""
    coercion = _detect_coercion("escalation_sensitivity", value, "string")
    if coercion:
        result.coercions.append(coercion)
        msg = (
            f"[WARN] YAML type coercion detected for key escalation_sensitivity: "
            f"value {coercion.raw_value} interpreted as {coercion.coerced_value}. "
            f"Use quotes for literal strings."
        )
        if strict:
            result.errors.append(msg.replace("[WARN]", "[ERROR]"))
            return
        result.warnings.append(msg)

    vr = validate_rule_value("escalation_sensitivity", value, "string")
    if not vr.valid:
        if not coercion:
            result.errors.append(vr.message)
        return

    if value not in VALID_ESCALATION_SENSITIVITIES:
        result.errors.append(
            f"escalation_sensitivity must be one of: "
            f"{', '.join(VALID_ESCALATION_SENSITIVITIES)}. Got '{value}'."
        )
        return

    escalation = result.rules.setdefault("escalation", {})
    escalation["sensitivity"] = value


def _translate_required_validators(
    value: Any, result: TranslationResult, strict: bool,
) -> None:
    """Translate rules.required_validators → gates.<stage>_dod.required_validators."""
    vr = validate_rule_value("required_validators", value, "map")
    if not vr.valid:
        result.errors.append(vr.message)
        return

    gates = result.rules.setdefault("gates", {})

    for stage, validators in value.items():
        full_key = f"required_validators.{stage}"
        vr_list = validate_rule_value(full_key, validators, "list")
        if not vr_list.valid:
            result.errors.append(vr_list.message)
            continue

        # Validate each validator entry is a string.
        for i, v in enumerate(validators):
            item_key = f"{full_key}[{i}]"
            vr_item = validate_rule_value(item_key, v, "string")
            if not vr_item.valid:
                result.errors.append(vr_item.message)
                # Don't skip the whole list for one bad entry.

        gate_key = f"{stage}_dod"
        gate = gates.setdefault(gate_key, {})
        gate["required_validators"] = validators


def _translate_dod_overrides(
    value: Any, result: TranslationResult, strict: bool,
) -> None:
    """Translate rules.dod_overrides → gates.<stage>_dod.dod_overrides."""
    vr = validate_rule_value("dod_overrides", value, "map")
    if not vr.valid:
        result.errors.append(vr.message)
        return

    gates = result.rules.setdefault("gates", {})

    for stage, dod_value in value.items():
        full_key = f"dod_overrides.{stage}"

        # dod_overrides can be a list of criteria or a merge-object dict.
        if not isinstance(dod_value, (list, dict)):
            result.errors.append(
                f"{full_key} must be list or map, got {type(dod_value).__name__}."
            )
            continue

        gate_key = f"{stage}_dod"
        gate = gates.setdefault(gate_key, {})
        gate["dod_overrides"] = dod_value


def _translate_limits_overrides(
    value: Any, result: TranslationResult, strict: bool,
) -> None:
    """Translate rules.limits_overrides → limits.<key>."""
    vr = validate_rule_value("limits_overrides", value, "map")
    if not vr.valid:
        result.errors.append(vr.message)
        return

    limits = result.rules.setdefault("limits", {})

    for limit_key, limit_value in value.items():
        full_key = f"limits_overrides.{limit_key}"

        coercion = _detect_coercion(full_key, limit_value, "int")
        if coercion:
            result.coercions.append(coercion)
            msg = (
                f"[WARN] YAML type coercion detected for key {full_key}: "
                f"value {coercion.raw_value} interpreted as {coercion.coerced_value}. "
                f"Use quotes for literal strings."
            )
            if strict:
                result.errors.append(msg.replace("[WARN]", "[ERROR]"))
                continue
            result.warnings.append(msg)

        vr_limit = validate_rule_value(full_key, limit_value, "int")
        if not vr_limit.valid:
            result.errors.append(vr_limit.message)
            continue

        limits[limit_key] = limit_value


def _translate_strict_mode(
    value: Any, result: TranslationResult, strict: bool,
) -> None:
    """Translate rules.strict_mode flag."""
    # Detect bool coercion — if the user wrote `yes` in YAML, it arrives as
    # True, which IS the correct type for a bool field.  However, if they
    # intended the string "yes", we can't distinguish.  We note it for
    # awareness but don't flag as coercion since bool IS the expected type.
    vr = validate_rule_value("strict_mode", value, "bool")
    if not vr.valid:
        result.errors.append(vr.message)
        return

    result.rules["strict_mode"] = value


def _translate_custom(
    value: Any, result: TranslationResult, strict: bool,
) -> None:
    """Translate rules.custom → custom_rules conditions."""
    vr = validate_rule_value("custom", value, "list")
    if not vr.valid:
        result.errors.append(vr.message)
        return

    custom_rules: list = []
    for i, rule_obj in enumerate(value):
        rule_key = f"custom[{i}]"

        if not isinstance(rule_obj, dict):
            result.errors.append(
                f"{rule_key} must be a map with field/operator/value keys, "
                f"got {type(rule_obj).__name__}."
            )
            continue

        # Support nested AND/OR/NOT condition trees as-is.
        if any(k in rule_obj for k in ("AND", "OR", "NOT")):
            custom_rules.append(rule_obj)
            continue

        # Simple condition: must have field + operator.
        if "field" not in rule_obj or "operator" not in rule_obj:
            result.errors.append(
                f"{rule_key} must contain 'field' and 'operator' keys."
            )
            continue

        custom_rules.append(rule_obj)

    if custom_rules:
        result.rules["custom_rules"] = custom_rules


# ---------------------------------------------------------------------------
# Key → translator dispatch table
# ---------------------------------------------------------------------------

_TRANSLATORS = {
    "preset": _translate_preset,
    "enabled": _translate_enabled,
    "strict_mode": _translate_strict_mode,
    "pass_threshold": _translate_pass_threshold,
    "routing_overrides": _translate_routing_overrides,
    "gate_overrides": _translate_gate_overrides,
    "escalation": _translate_escalation,
    "escalation_sensitivity": _translate_escalation_sensitivity,
    "required_validators": _translate_required_validators,
    "dod_overrides": _translate_dod_overrides,
    "limits_overrides": _translate_limits_overrides,
    "custom": _translate_custom,
}


# ---------------------------------------------------------------------------
# Public: main translation entry point
# ---------------------------------------------------------------------------

def translate_config(
    config_data: dict,
    strict_mode: bool = False,
) -> TranslationResult:
    """
    Translate a parsed YAML config rules section into JSON rule overrides.

    Args:
        config_data: The ``rules`` dict from the parsed ``.delivery/config.yml``.
            Expected top-level keys: preset, enabled, strict_mode, pass_threshold,
            routing_overrides, gate_overrides, escalation, escalation_sensitivity,
            required_validators, dod_overrides, limits_overrides, custom.
        strict_mode: When True, any YAML type coercion is promoted to an error
            and no coerced value reaches the output overrides.

    Returns:
        TranslationResult with rules (JSON overrides), warnings, errors, and
        coercion records.
    """
    result = TranslationResult()

    if not isinstance(config_data, dict):
        result.errors.append(
            f"Config data must be a dict, got {type(config_data).__name__}."
        )
        return result

    # Empty config is valid — no overrides.
    if not config_data:
        return result

    for key, value in config_data.items():
        translator = _TRANSLATORS.get(key)
        if translator is None:
            result.warnings.append(f"Unknown config key '{key}' — ignored.")
            continue
        translator(value, result, strict_mode)

    # In strict mode, if there were any errors, clear the overrides so that
    # no partial / coerced values leak through.
    if strict_mode and result.errors:
        result.rules = {}

    return result


# Alias matching the architecture document's naming convention.
translate_config_to_rules = translate_config
