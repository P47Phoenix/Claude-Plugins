"""
Delivery Rules Adapter

Wraps the condition evaluator for delivery-flow use. Provides 4-layer rule
resolution (defaults -> preset -> config -> runtime), stage routing evaluation,
and DoD gate evaluation with weighted scoring.

Zero external dependencies -- Python stdlib only, no SQLite.
"""

import copy
import json
import os
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from condition_evaluator import evaluate_condition, extract_relevant_context

__all__ = [
    "StageRouting",
    "GateResult",
    "ValidatorResult",
    "resolve_rules",
    "evaluate_stage_routing",
    "evaluate_dod_gate",
    "get_resolved_rules",
]


# ---------------------------------------------------------------------------
# Data Classes
# ---------------------------------------------------------------------------

@dataclass
class StageRouting:
    """Result of evaluating stage routing for a specific project type + stage + risk."""
    depth: str                              # "full", "light", "skip", "full+game"
    dod_validators: List[str]               # e.g. ["product_owner", "architect"]
    collaboration_patterns: List[str]       # e.g. ["evaluator_optimizer"]
    max_iterations: int                     # max self-correction loops
    scope_constraint: Optional[str]         # what "light" means, or None for full


@dataclass
class ValidatorResult:
    """Input to evaluate_dod_gate -- one validator's outcome."""
    role: str                               # e.g. "product_owner"
    status: str                             # "DONE", "NEEDS_WORK", "BLOCKED"
    findings: List[str] = field(default_factory=list)


@dataclass
class GateResult:
    """Result of evaluating a DoD gate."""
    decision: str                           # "GO", "RECYCLE", "HOLD", "ESCALATE"
    score: float                            # 0.0 - 100.0
    passed_criteria: List[str]
    failed_criteria: List[str]
    reasons: List[str]
    determinism_category: str               # "a" (fully deterministic)


# ---------------------------------------------------------------------------
# Internal: Merge helpers
# ---------------------------------------------------------------------------

def _deep_merge(base: dict, overlay: dict) -> dict:
    """
    Shallow-merge maps, replace scalars and lists (unless ``_merge: extend``).

    Returns a new dict -- does not mutate *base*.
    """
    merged = copy.deepcopy(base)
    for key, value in overlay.items():
        if key == "_merge":
            continue
        if (
            isinstance(value, dict)
            and isinstance(merged.get(key), dict)
        ):
            merged[key] = _deep_merge(merged[key], value)
        elif (
            isinstance(value, list)
            and isinstance(merged.get(key), list)
            and overlay.get("_merge") == "extend"
        ):
            merged[key] = merged[key] + value
        else:
            merged[key] = copy.deepcopy(value)
    return merged


def _load_json(path: str) -> dict:
    """Load a JSON file or return empty dict if the file does not exist."""
    if not os.path.isfile(path):
        return {}
    with open(path, "r", encoding="utf-8") as fh:
        return json.load(fh)


# ---------------------------------------------------------------------------
# Public API: Rule Resolution
# ---------------------------------------------------------------------------

def resolve_rules(
    defaults_path: str,
    preset: str,
    config_overrides: Optional[Dict[str, Any]] = None,
    run_overrides: Optional[Dict[str, Any]] = None,
) -> dict:
    """
    4-layer rule resolution.

    Layer 1 -- Load JSON from *defaults_path* (stage-routing.json or similar).
    Layer 2 -- Apply preset overlay (``presets/<preset>.json`` next to defaults).
    Layer 3 -- Apply *config_overrides* (from ``.delivery/config.yml`` ``rules.*``).
    Layer 4 -- Apply *run_overrides* (ephemeral, per-run). Blocked when the
               resolved rules contain ``strict_mode: true``.

    Merge semantics (per architecture DD2):
      - Scalars: last-writer-wins (higher layer replaces lower).
      - Lists: last-writer-wins by default; opt-in ``_merge: extend`` appends.
      - Maps: shallow-merge (higher-layer keys override, unmentioned keys kept).

    Args:
        defaults_path: Absolute path to the defaults JSON file.
        preset: One of "solo", "standard", "strict".
        config_overrides: Dict of per-repo overrides (Layer 3). May be None.
        run_overrides: Dict of ephemeral overrides (Layer 4). May be None.

    Returns:
        Fully merged rule dictionary.

    Raises:
        FileNotFoundError: If *defaults_path* does not exist.
        ValueError: If *preset* is not one of the recognised values.
    """
    valid_presets = {"solo", "standard", "strict"}
    if preset not in valid_presets:
        raise ValueError(
            f"Unknown preset '{preset}'. Must be one of: {sorted(valid_presets)}"
        )

    if not os.path.isfile(defaults_path):
        raise FileNotFoundError(f"Defaults file not found: {defaults_path}")

    # Layer 1: plugin defaults
    resolved = _load_json(defaults_path)

    # Layer 2: preset overlay
    defaults_dir = os.path.dirname(defaults_path)
    preset_path = os.path.join(defaults_dir, "presets", f"{preset}.json")
    preset_data = _load_json(preset_path)
    if preset_data:
        resolved = _deep_merge(resolved, preset_data)

    # Layer 3: per-repo config overrides
    if config_overrides:
        resolved = _deep_merge(resolved, config_overrides)

    # Layer 4: per-run runtime overrides (blocked under strict mode)
    if run_overrides:
        strict_mode = resolved.get("strict_mode", False)
        if not strict_mode:
            resolved = _deep_merge(resolved, run_overrides)

    return resolved


def get_resolved_rules(
    defaults_path: str,
    preset: str,
    config_overrides: Optional[Dict[str, Any]] = None,
) -> dict:
    """
    Dry-run inspection helper -- returns the merged rule set *without*
    Layer 4 runtime overrides.

    Useful for tooling that wants to show what rules are active before a
    pipeline run starts.
    """
    return resolve_rules(defaults_path, preset, config_overrides, run_overrides=None)


# ---------------------------------------------------------------------------
# Public API: Stage Routing Evaluation
# ---------------------------------------------------------------------------

def evaluate_stage_routing(
    project_type: str,
    stage: str,
    risk_tolerance: str,
    rules: dict,
) -> StageRouting:
    """
    Look up the routing cell for a specific project type + stage + risk tolerance.

    The *rules* dict must contain a ``routing`` key structured as::

        routing.<PROJECT_TYPE>.<risk_tolerance>.<stage> = {
            depth, dod_validators, collaboration_patterns,
            max_iterations, scope_constraint, [conditional_depth]
        }

    When a ``conditional_depth`` block is present, its conditions are evaluated
    against the *rules* dict itself (allowing feature-flag-style overrides).
    If no condition matches, the cell's ``depth`` value is used as the default.

    Args:
        project_type: E.g. "GREENFIELD", "BUG_FIX".
        stage: Stage id, e.g. "idea", "development".
        risk_tolerance: "solo", "standard", or "strict".
        rules: Fully resolved rule dict (output of :func:`resolve_rules`).

    Returns:
        A :class:`StageRouting` dataclass.

    Raises:
        ValueError: If the project type, stage, or risk tolerance is not found.
    """
    routing = rules.get("routing", {})

    if project_type not in routing:
        raise ValueError(
            f"Unknown project type '{project_type}'. "
            f"Valid types: {sorted(routing.keys())}"
        )

    type_routing = routing[project_type]
    if risk_tolerance not in type_routing:
        raise ValueError(
            f"Unknown risk tolerance '{risk_tolerance}' for project type "
            f"'{project_type}'. Valid: {sorted(type_routing.keys())}"
        )

    risk_routing = type_routing[risk_tolerance]
    if stage not in risk_routing:
        raise ValueError(
            f"Unknown stage '{stage}' for {project_type}/{risk_tolerance}. "
            f"Valid stages: {sorted(risk_routing.keys())}"
        )

    cell = risk_routing[stage]

    # Resolve conditional depth if present
    depth = cell.get("depth", "full")
    conditional = cell.get("conditional_depth")
    if conditional:
        depth = _resolve_conditional_depth(conditional, rules, depth)

    return StageRouting(
        depth=depth,
        dod_validators=list(cell.get("dod_validators", [])),
        collaboration_patterns=list(cell.get("collaboration_patterns", [])),
        max_iterations=cell.get("max_iterations", 2),
        scope_constraint=cell.get("scope_constraint"),
    )


def _resolve_conditional_depth(
    conditional: dict,
    context: dict,
    default: str,
) -> str:
    """
    Evaluate ``conditional_depth`` block.

    Checks ``full_when`` first (upgrade path), then ``skip_when``
    (downgrade path). Falls back to *default* if neither matches.
    """
    full_when = conditional.get("full_when")
    if full_when:
        condition = _normalise_shorthand(full_when)
        if evaluate_condition(condition, context):
            return "full"

    skip_when = conditional.get("skip_when")
    if skip_when:
        condition = _normalise_shorthand(skip_when)
        if evaluate_condition(condition, context):
            return "skip"

    return conditional.get("default", default)


def _normalise_shorthand(block: dict) -> dict:
    """
    Convert shorthand condition blocks (``any_of``, ``all_of``) used in the
    routing JSON into the canonical ``OR`` / ``AND`` format expected by
    :func:`evaluate_condition`.
    """
    if "any_of" in block:
        return {"OR": block["any_of"]}
    if "all_of" in block:
        return {"AND": block["all_of"]}
    # Already in canonical form
    return block


# ---------------------------------------------------------------------------
# Public API: DoD Gate Evaluation
# ---------------------------------------------------------------------------

def evaluate_dod_gate(
    stage: str,
    validator_results: List[ValidatorResult],
    rules: dict,
) -> GateResult:
    """
    Evaluate a Definition of Done gate for a pipeline stage.

    Uses the condition evaluator for individual criterion checks against a
    context built from *validator_results*. Applies weighted scoring with
    critical-rule override.

    Decision mapping:
      - score >= threshold -> GO
      - score >= threshold * 0.7 -> RECYCLE
      - otherwise -> HOLD
      - Any critical rule failure -> HOLD regardless of score

    The *rules* dict may contain a ``gates.<stage>_dod`` block with::

        pass_threshold: float (default 80.0)
        criteria: [
            {
                name: str,
                condition: <condition tree>,
                weight: float (default 10),
                critical: bool (default false)
            },
            ...
        ]

    If no gate block is found, the gate is evaluated purely on validator
    status (all DONE -> GO).

    Args:
        stage: Stage id, e.g. "design", "development".
        validator_results: List of :class:`ValidatorResult` from each validator.
        rules: Fully resolved rule dict (output of :func:`resolve_rules`).

    Returns:
        A :class:`GateResult` dataclass.
    """
    # Build context from validator results
    context = _build_gate_context(stage, validator_results)

    # Look up gate-specific rules
    gate_key = f"{stage}_dod"
    gates = rules.get("gates", {})
    gate_config = gates.get(gate_key, {})

    criteria = gate_config.get("criteria", [])
    pass_threshold = float(gate_config.get("pass_threshold", 80.0))

    # If no criteria defined, fall back to validator-status-only evaluation
    if not criteria:
        return _evaluate_validator_only_gate(stage, validator_results)

    # Weighted scoring
    total_weight = 0.0
    weighted_score = 0.0
    critical_failures: List[str] = []
    passed_criteria: List[str] = []
    failed_criteria: List[str] = []
    reasons: List[str] = []

    for criterion in criteria:
        if not criterion.get("enabled", True):
            continue

        name = criterion.get("name", "unnamed")
        condition = criterion.get("condition", {})
        weight = float(criterion.get("weight", 10))
        critical = criterion.get("critical", False)

        total_weight += weight

        passed = evaluate_condition(condition, context)
        if passed:
            weighted_score += weight * 100.0
            passed_criteria.append(name)
        else:
            failed_criteria.append(name)
            evaluated_fields = extract_relevant_context(context, condition)
            reasons.append(
                f"FAILED: {name} (fields: {evaluated_fields})"
            )
            if critical:
                critical_failures.append(name)

    # Calculate overall score
    overall_score = (
        weighted_score / total_weight if total_weight > 0 else 0.0
    )

    # Decision mapping
    if critical_failures:
        decision = "HOLD"
        reasons.insert(
            0,
            f"Critical failure(s): {', '.join(critical_failures)}"
        )
    elif overall_score >= pass_threshold:
        decision = "GO"
    elif overall_score >= pass_threshold * 0.7:
        decision = "RECYCLE"
    else:
        decision = "HOLD"

    return GateResult(
        decision=decision,
        score=round(overall_score, 2),
        passed_criteria=passed_criteria,
        failed_criteria=failed_criteria,
        reasons=reasons,
        determinism_category="a",
    )


def _build_gate_context(
    stage: str,
    validator_results: List[ValidatorResult],
) -> dict:
    """
    Assemble a context dict from validator results for condition evaluation.

    Produces a structure like::

        {
            "stage": {"name": "design"},
            "validators": {
                "product_owner": {"status": "DONE", "findings": [...]},
                ...
            },
            "all_done": True/False,
            "done_count": 3,
            "total_count": 4
        }
    """
    validators: Dict[str, Any] = {}
    done_count = 0
    for vr in validator_results:
        validators[vr.role] = {
            "status": vr.status,
            "findings": vr.findings,
        }
        if vr.status == "DONE":
            done_count += 1

    return {
        "stage": {"name": stage},
        "validators": validators,
        "all_done": done_count == len(validator_results),
        "done_count": done_count,
        "total_count": len(validator_results),
    }


def _evaluate_validator_only_gate(
    stage: str,
    validator_results: List[ValidatorResult],
) -> GateResult:
    """
    Fallback gate evaluation when no criteria rules are defined.
    Pure validator-status check: all DONE -> GO, otherwise RECYCLE.
    """
    passed = []
    failed = []
    reasons = []

    for vr in validator_results:
        if vr.status == "DONE":
            passed.append(vr.role)
        else:
            failed.append(vr.role)
            reasons.append(
                f"{vr.role}: {vr.status}"
                + (f" -- {'; '.join(vr.findings)}" if vr.findings else "")
            )

    all_done = len(failed) == 0
    score = (
        (len(passed) / len(validator_results) * 100.0)
        if validator_results
        else 0.0
    )

    if all_done:
        decision = "GO"
    elif score >= 80.0 * 0.7:
        decision = "RECYCLE"
    else:
        decision = "HOLD"

    return GateResult(
        decision=decision,
        score=round(score, 2),
        passed_criteria=passed,
        failed_criteria=failed,
        reasons=reasons,
        determinism_category="a",
    )
