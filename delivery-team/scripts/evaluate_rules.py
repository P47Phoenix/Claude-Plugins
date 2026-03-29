"""
Evaluation Script — CLI Entry Point (C4)

Single entry point invoked by the delivery-flow orchestrator via Bash tool.
Reads pipeline context from JSON, resolves rules through 4-layer resolution,
evaluates routing or gate decisions, and writes deterministic JSON to stdout.

Zero external dependencies — Python stdlib only.

Usage:
    python evaluate_rules.py --action route --context /tmp/context.json
    python evaluate_rules.py --action gate --context /tmp/context.json
    python evaluate_rules.py --action resolve --context /tmp/context.json --dry-run

Exit codes:
    0 — Success (decision JSON on stdout)
    1 — Argument or config error (error JSON on stderr)
    2 — Rule evaluation error (error JSON on stderr)
"""

import argparse
import json
import os
import sys
from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path

# ---------------------------------------------------------------------------
# Sibling imports — condition_evaluator, delivery_rules_adapter, yaml_to_rules
# live in the same directory as this script.
# ---------------------------------------------------------------------------
_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
if _SCRIPT_DIR not in sys.path:
    sys.path.insert(0, _SCRIPT_DIR)

from condition_evaluator import extract_relevant_context  # noqa: E402
from delivery_rules_adapter import (  # noqa: E402
    GateResult,
    StageRouting,
    ValidatorResult,
    evaluate_dod_gate,
    evaluate_stage_routing,
    get_resolved_rules,
    resolve_rules,
)
from yaml_to_rules import translate_config  # noqa: E402

__all__ = ["main"]

# ---------------------------------------------------------------------------
# Default paths (relative to repo root)
# ---------------------------------------------------------------------------
_DEFAULT_RULES_DIR = os.path.normpath(
    os.path.join(_SCRIPT_DIR, "..", "skills", "delivery-flow", "references", "rules")
)


# ---------------------------------------------------------------------------
# Error helpers
# ---------------------------------------------------------------------------

def _error_json(error_type: str, message: str, **extra) -> str:
    """Build a JSON error payload for stderr."""
    payload = {
        "error_type": error_type,
        "message": message,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
    payload.update(extra)
    return json.dumps(payload, indent=2)


def _exit_error(code: int, error_type: str, message: str, **extra):
    """Write error JSON to stderr and exit."""
    sys.stderr.write(_error_json(error_type, message, **extra) + "\n")
    raise SystemExit(code)


# ---------------------------------------------------------------------------
# Feature flag check
# ---------------------------------------------------------------------------

def _check_feature_flag(config_overrides: dict) -> bool:
    """
    If config has rules.enabled == false, return True (bypassed).
    The caller should exit 0 with a bypass payload.
    """
    return config_overrides.get("enabled") is False


# ---------------------------------------------------------------------------
# Context loading
# ---------------------------------------------------------------------------

def _load_context(path: str) -> dict:
    """Load and validate the context JSON file."""
    if not os.path.isfile(path):
        _exit_error(1, "file_not_found", f"Context file not found: {path}")

    try:
        with open(path, "r", encoding="utf-8") as fh:
            data = json.load(fh)
    except json.JSONDecodeError as exc:
        _exit_error(1, "json_parse_error", f"Malformed JSON in context file: {exc}")

    if not isinstance(data, dict):
        _exit_error(1, "invalid_context", "Context file must contain a JSON object")

    return data


# ---------------------------------------------------------------------------
# Config loading (optional Layer 3 overrides)
# ---------------------------------------------------------------------------

def _load_config_overrides(config_path: str, strict: bool) -> dict:
    """
    Load .delivery/config.yml rules section via yaml_to_rules translator.

    The config file may contain a ``rules`` key with structured overrides.
    Since we cannot import PyYAML (zero external deps), we accept a JSON
    file at --config-overrides containing the pre-parsed rules section.
    The orchestrator is responsible for extracting the YAML rules section
    and writing it as JSON before invoking this script.
    """
    if not config_path:
        return {}

    if not os.path.isfile(config_path):
        _exit_error(
            1, "file_not_found", f"Config overrides file not found: {config_path}"
        )

    try:
        with open(config_path, "r", encoding="utf-8") as fh:
            raw = json.load(fh)
    except json.JSONDecodeError as exc:
        _exit_error(
            1, "json_parse_error", f"Malformed JSON in config overrides: {exc}"
        )

    if not isinstance(raw, dict):
        _exit_error(
            1, "invalid_config", "Config overrides file must contain a JSON object"
        )

    # Run through the translation layer for validation + coercion detection
    result = translate_config(raw, strict_mode=strict)

    # Surface warnings on stderr (non-fatal)
    for warning in result.warnings:
        sys.stderr.write(warning + "\n")

    # Translation errors are fatal
    if result.errors:
        _exit_error(
            2,
            "config_translation_error",
            "; ".join(result.errors),
        )

    return result.rules


# ---------------------------------------------------------------------------
# Action: route
# ---------------------------------------------------------------------------

def _action_route(
    context: dict, rules: dict, preset: str, dry_run: bool, compare: bool
) -> dict:
    """Evaluate stage routing for a project type + stage + risk tolerance."""
    project_type = context.get("project_type")
    stage = context.get("stage")
    risk_tolerance = context.get("risk_tolerance", preset)

    if not project_type:
        _exit_error(2, "missing_field", "Context missing required field: project_type")
    if not stage:
        _exit_error(2, "missing_field", "Context missing required field: stage")

    try:
        routing = evaluate_stage_routing(project_type, stage, risk_tolerance, rules)
    except (ValueError, KeyError) as exc:
        _exit_error(2, "rule_evaluation_error", str(exc))

    result = {
        "decision_type": "routing",
        "action": "route",
        "stage": stage,
        "project_type": project_type,
        "risk_tolerance": risk_tolerance,
        "routing": {
            "depth": routing.depth,
            "dod_validators": routing.dod_validators,
            "collaboration_patterns": routing.collaboration_patterns,
            "max_iterations": routing.max_iterations,
            "scope_constraint": routing.scope_constraint,
        },
        "preset": preset,
        "determinism_category": "a",
    }

    # --compare: show default routing alongside overridden routing
    if compare and dry_run:
        try:
            defaults_path = os.path.join(
                _resolve_rules_dir(None), "stage-routing.json"
            )
            default_rules = resolve_rules(defaults_path, preset)
            default_routing = evaluate_stage_routing(
                project_type, stage, risk_tolerance, default_rules
            )
            result["comparison"] = {
                "default": {
                    "depth": default_routing.depth,
                    "dod_validators": default_routing.dod_validators,
                    "collaboration_patterns": default_routing.collaboration_patterns,
                    "max_iterations": default_routing.max_iterations,
                    "scope_constraint": default_routing.scope_constraint,
                },
                "current": result["routing"],
            }
        except Exception:
            # Comparison is best-effort; don't fail the whole invocation
            result["comparison"] = {"error": "Could not resolve default rules for comparison"}

    return result


# ---------------------------------------------------------------------------
# Action: gate
# ---------------------------------------------------------------------------

def _action_gate(context: dict, rules: dict, preset: str) -> dict:
    """Evaluate a DoD gate for a given stage + validator results."""
    stage = context.get("stage")
    if not stage:
        _exit_error(2, "missing_field", "Context missing required field: stage")

    raw_validators = context.get("validator_results", [])
    if not isinstance(raw_validators, list):
        _exit_error(
            2, "invalid_field", "validator_results must be a list of objects"
        )

    # Build ValidatorResult objects from the raw JSON
    validators = []
    for i, vr in enumerate(raw_validators):
        if not isinstance(vr, dict):
            _exit_error(
                2,
                "invalid_field",
                f"validator_results[{i}] must be an object",
            )
        role = vr.get("role")
        status = vr.get("status")
        if not role or not status:
            _exit_error(
                2,
                "missing_field",
                f"validator_results[{i}] missing required 'role' or 'status'",
            )
        validators.append(
            ValidatorResult(
                role=role,
                status=status,
                findings=vr.get("findings", []),
            )
        )

    try:
        gate_result = evaluate_dod_gate(stage, validators, rules)
    except (ValueError, KeyError) as exc:
        _exit_error(2, "rule_evaluation_error", str(exc))

    gate_id = context.get("gate_id", f"{stage}_dod")

    return {
        "decision_type": "gate",
        "action": "gate",
        "gate_id": gate_id,
        "stage": stage,
        "decision": gate_result.decision,
        "overall_score": gate_result.score,
        "passed": gate_result.decision == "GO",
        "passed_criteria": gate_result.passed_criteria,
        "failed_criteria": gate_result.failed_criteria,
        "reasons": gate_result.reasons,
        "determinism_category": gate_result.determinism_category,
        "preset": preset,
    }


# ---------------------------------------------------------------------------
# Action: resolve
# ---------------------------------------------------------------------------

def _action_resolve(rules: dict, preset: str) -> dict:
    """Output the fully resolved rule set for dry-run inspection."""
    return {
        "decision_type": "resolve",
        "action": "resolve",
        "preset": preset,
        "resolved_rules": rules,
        "determinism_category": "a",
    }


# ---------------------------------------------------------------------------
# Audit trail
# ---------------------------------------------------------------------------

def _write_audit_entry(result: dict, context: dict, pipeline_id: str):
    """
    Append a JSONL audit entry to .delivery/audit/audit-<pipeline_id>.jsonl.

    Only called on non-dry-run evaluations.
    """
    if not pipeline_id:
        # No pipeline_id means we cannot write a meaningful audit entry.
        return

    audit_dir = os.path.join(".delivery", "audit")
    os.makedirs(audit_dir, exist_ok=True)

    audit_path = os.path.join(audit_dir, f"audit-{pipeline_id}.jsonl")

    entry = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "pipeline_id": pipeline_id,
        "stage": result.get("stage", context.get("stage", "")),
        "action": result.get("action", ""),
        "decision": result.get("decision", result.get("routing", {}).get("depth", "")),
        "score": result.get("overall_score", None),
        "determinism_category": result.get("determinism_category", "a"),
        "resolution_layer": _infer_resolution_layer(result),
        "input_context": _extract_audit_context(context),
    }

    try:
        with open(audit_path, "a", encoding="utf-8") as fh:
            fh.write(json.dumps(entry, separators=(",", ":")) + "\n")
    except OSError as exc:
        # Audit write failure is non-fatal; warn on stderr
        sys.stderr.write(f"[WARN] Could not write audit entry: {exc}\n")


def _infer_resolution_layer(result: dict) -> int:
    """Infer the highest resolution layer that contributed to the decision."""
    # Simple heuristic: if config overrides were applied, layer >= 3
    resolution_layers = result.get("resolution_layers", {})
    if resolution_layers:
        return max(resolution_layers.values(), default=1)
    return 1


def _extract_audit_context(context: dict) -> dict:
    """Extract a minimal subset of context for the audit entry."""
    keys = [
        "project_type", "stage", "risk_tolerance", "pipeline_id",
        "gate_id", "iteration_count",
    ]
    return {k: context[k] for k in keys if k in context}


# ---------------------------------------------------------------------------
# Rules directory resolution
# ---------------------------------------------------------------------------

def _resolve_rules_dir(rules_dir: str) -> str:
    """Resolve the rules directory, falling back to the default."""
    if rules_dir:
        return rules_dir
    return _DEFAULT_RULES_DIR


# ---------------------------------------------------------------------------
# Argument parsing
# ---------------------------------------------------------------------------

def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Deterministic rules engine CLI for delivery-flow.",
        prog="evaluate_rules.py",
    )
    parser.add_argument(
        "--action",
        required=True,
        choices=["route", "gate", "resolve"],
        help="Action to perform: route (stage routing), gate (DoD gate), resolve (show resolved rules).",
    )
    parser.add_argument(
        "--context",
        required=True,
        help="Path to JSON file containing the pipeline context dictionary.",
    )
    parser.add_argument(
        "--rules-dir",
        default=None,
        help="Path to directory containing default rule JSON files. "
             "Defaults to delivery-team/skills/delivery-flow/references/rules/.",
    )
    parser.add_argument(
        "--preset",
        default=None,
        help="Preset profile name (solo, standard, strict). "
             "If omitted, read from context or config; falls back to 'standard'.",
    )
    parser.add_argument(
        "--config-overrides",
        default=None,
        help="Path to JSON file containing pre-parsed config rules section (Layer 3 overrides).",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Output decisions without writing audit entries or mutating state.",
    )
    parser.add_argument(
        "--compare",
        action="store_true",
        help="With --dry-run, show default vs overridden routing side-by-side.",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Enable strict mode: YAML coercions become hard errors, Layer 4 overrides blocked.",
    )
    return parser


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main(argv=None) -> int:
    """
    CLI entry point.

    Returns:
        Exit code (0, 1, or 2).
    """
    parser = _build_parser()

    try:
        args = parser.parse_args(argv)
    except SystemExit as exc:
        # argparse calls sys.exit on error; re-raise with code 1
        return 1

    # 1. Load context
    context = _load_context(args.context)

    # 2. Load config overrides (Layer 3)
    config_overrides = _load_config_overrides(args.config_overrides, args.strict)

    # 3. Feature flag: rules.enabled
    if _check_feature_flag(config_overrides):
        payload = {"bypassed": True, "reason": "rules.enabled is false"}
        sys.stdout.write(json.dumps(payload, indent=2) + "\n")
        return 0

    # 4. Determine preset: CLI arg > context > config > default
    preset = (
        args.preset
        or context.get("preset")
        or config_overrides.get("preset")
        or "standard"
    )

    # 5. Resolve rules directory
    rules_dir = _resolve_rules_dir(args.rules_dir)
    routing_defaults = os.path.join(rules_dir, "stage-routing.json")

    # 6. Resolve rules through 4-layer resolution
    try:
        run_overrides = context.get("run_overrides")
        rules = resolve_rules(
            defaults_path=routing_defaults,
            preset=preset,
            config_overrides=config_overrides if config_overrides else None,
            run_overrides=run_overrides,
        )
    except FileNotFoundError as exc:
        _exit_error(1, "file_not_found", str(exc))
    except ValueError as exc:
        _exit_error(1, "invalid_preset", str(exc))

    # 7. Dispatch action
    try:
        if args.action == "route":
            result = _action_route(
                context, rules, preset, args.dry_run, args.compare
            )
        elif args.action == "gate":
            result = _action_gate(context, rules, preset)
        elif args.action == "resolve":
            result = _action_resolve(rules, preset)
        else:
            _exit_error(1, "invalid_action", f"Unknown action: {args.action}")
    except SystemExit:
        raise
    except Exception as exc:
        _exit_error(2, "rule_evaluation_error", str(exc))

    # 8. Output result JSON to stdout
    sys.stdout.write(json.dumps(result, indent=2) + "\n")

    # 9. Write audit trail (unless dry-run or resolve)
    if not args.dry_run and args.action != "resolve":
        pipeline_id = context.get("pipeline_id", "")
        _write_audit_entry(result, context, pipeline_id)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
