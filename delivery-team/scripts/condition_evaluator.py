"""
Standalone Condition Evaluator

Pure condition evaluation logic extracted from the Business Rules Engine.
Zero external dependencies — Python stdlib only, no SQLite, no database references.

Evaluates nested logical conditions (AND/OR/NOT) against a context dictionary,
supporting field comparisons, null checks, pattern matching, and collection operations.
"""

import re
from typing import Any, Dict, List

__all__ = [
    "evaluate_condition",
    "get_field_value",
    "compare_values",
    "extract_field_paths",
    "extract_relevant_context",
]


def evaluate_condition(condition: dict, context: dict) -> bool:
    """
    Recursively evaluate a condition tree against a context dictionary.

    Supports:
    - Simple comparisons: {"field": "x", "operator": "==", "value": 5}
    - AND: {"AND": [cond1, cond2, ...]}  — all must be true
    - OR:  {"OR":  [cond1, cond2, ...]}  — at least one must be true
    - NOT: {"NOT": cond}                 — negation
    - MATCHES: {"MATCHES": {"field": "x", "pattern": "regex"}}

    Args:
        condition: A condition dictionary (may be nested arbitrarily deep).
        context: The data dictionary to evaluate against.

    Returns:
        True if the condition is satisfied, False otherwise.

    Raises:
        ValueError: If the condition dictionary has an unrecognised format.
    """
    # Logical operators
    if "AND" in condition:
        return all(evaluate_condition(c, context) for c in condition["AND"])

    if "OR" in condition:
        return any(evaluate_condition(c, context) for c in condition["OR"])

    if "NOT" in condition:
        return not evaluate_condition(condition["NOT"], context)

    # Pattern matching
    if "MATCHES" in condition:
        field = condition["MATCHES"]["field"]
        pattern = condition["MATCHES"]["pattern"]
        value = get_field_value(context, field)

        if value is None:
            return False

        return bool(re.match(pattern, str(value)))

    # Simple field comparison
    if "field" in condition and "operator" in condition:
        field = condition["field"]
        operator = condition["operator"]
        expected = condition.get("value")
        actual = get_field_value(context, field)

        return compare_values(actual, operator, expected)

    raise ValueError(f"Invalid condition format: {condition}")


def get_field_value(context: dict, field_path: str) -> Any:
    """
    Retrieve a value from *context* using dot-notation.

    Special accessor:
    - A path ending with ``.length`` returns ``len()`` of the resolved
      collection (or 0 when the value is ``None`` / not sized).

    Examples::

        get_field_value({"user": {"age": 30}}, "user.age")        # -> 30
        get_field_value({"items": [1, 2, 3]},  "items.length")    # -> 3

    Args:
        context: The data dictionary to traverse.
        field_path: Dot-separated path into *context*.

    Returns:
        The resolved value, or ``None`` if any segment is missing.
    """
    # Handle .length accessor
    if field_path.endswith(".length"):
        base_path = field_path[:-7]  # strip ".length"
        value = get_field_value(context, base_path)
        return len(value) if value is not None and hasattr(value, "__len__") else 0

    parts = field_path.split(".")
    value: Any = context

    for part in parts:
        if value is None:
            return None

        if isinstance(value, dict):
            value = value.get(part)
        else:
            value = getattr(value, part, None)

    return value


def compare_values(actual: Any, operator: str, expected: Any) -> bool:
    """
    Compare *actual* against *expected* using *operator*.

    Supported operators:
        ==, !=, >, <, >=, <=, IN, NOT IN, IS NULL, IS NOT NULL, MATCHES

    Numeric comparisons (>, <, >=, <=) coerce both operands to ``float``.

    Args:
        actual: The value obtained from the context.
        operator: One of the supported operator strings.
        expected: The reference value to compare against (unused for null checks).

    Returns:
        True if the comparison holds, False otherwise.

    Raises:
        ValueError: If *operator* is not recognised.
    """
    # Null checks
    if operator == "IS NULL":
        return actual is None

    if operator == "IS NOT NULL":
        return actual is not None

    # Everything else requires a non-None actual
    if actual is None:
        return False

    if operator == "==":
        return actual == expected

    if operator == "!=":
        return actual != expected

    if operator == ">":
        return float(actual) > float(expected)

    if operator == "<":
        return float(actual) < float(expected)

    if operator == ">=":
        return float(actual) >= float(expected)

    if operator == "<=":
        return float(actual) <= float(expected)

    if operator == "IN":
        return actual in expected

    if operator == "NOT IN":
        return actual not in expected

    if operator == "MATCHES":
        return bool(re.match(str(expected), str(actual)))

    raise ValueError(f"Unknown operator: {operator}")


def extract_field_paths(condition: dict) -> List[str]:
    """
    Recursively collect every field path referenced in a condition tree.

    Args:
        condition: A (possibly nested) condition dictionary.

    Returns:
        A list of field-path strings (may contain duplicates if a field
        appears in multiple sub-conditions).
    """
    fields: List[str] = []

    if "field" in condition:
        fields.append(condition["field"])

    if "AND" in condition:
        for c in condition["AND"]:
            fields.extend(extract_field_paths(c))

    if "OR" in condition:
        for c in condition["OR"]:
            fields.extend(extract_field_paths(c))

    if "NOT" in condition:
        fields.extend(extract_field_paths(condition["NOT"]))

    if "MATCHES" in condition and "field" in condition["MATCHES"]:
        fields.append(condition["MATCHES"]["field"])

    return fields


def extract_relevant_context(context: dict, condition: dict) -> Dict[str, Any]:
    """
    Return the subset of *context* referenced by *condition*.

    Useful for audit logging — captures only the fields that influenced
    a condition evaluation without exposing the entire context.

    Args:
        context: The full data dictionary.
        condition: The condition whose field paths to extract.

    Returns:
        A dict mapping each referenced field path to its resolved value.
    """
    fields = extract_field_paths(condition)
    return {field: get_field_value(context, field) for field in fields}
