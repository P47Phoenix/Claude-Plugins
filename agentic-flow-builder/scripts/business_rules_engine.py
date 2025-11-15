#!/usr/bin/env python3
"""
Business Rules Engine (BRE) for deterministic decision-making in agentic flows.

This production-grade BRE provides:
- Declarative rule definition language
- Type-safe expression evaluation
- Priority-based rule execution
- Comprehensive audit trail
- Gate management without AI inconsistency
- Support for complex conditions and actions

Rule Condition Language supports:
- Comparison operators: ==, !=, <, >, <=, >=
- Logical operators: AND, OR, NOT
- Membership operators: IN, NOT IN
- Pattern matching: MATCHES, CONTAINS
- Null checks: IS NULL, IS NOT NULL
- Nested conditions and grouping
"""

import re
import operator
from typing import Any, Dict, List, Optional, Tuple
from enum import Enum
from dataclasses import dataclass
from datetime import datetime


class RuleType(Enum):
    """Types of business rules."""
    GATE = "gate"  # Decision gate (pass/fail)
    VALIDATION = "validation"  # Data validation
    TRANSFORMATION = "transformation"  # Data transformation
    ROUTING = "routing"  # Flow routing decision


class RuleStatus(Enum):
    """Result of rule evaluation."""
    PASS = "pass"
    FAIL = "fail"
    ERROR = "error"


@dataclass
class RuleEvaluation:
    """Result of a rule evaluation."""
    rule_id: str
    status: RuleStatus
    result: Any
    reason: str
    evaluated_at: datetime
    evaluation_details: Dict[str, Any]


class ExpressionEvaluator:
    """Evaluates rule condition expressions against context data."""

    # Supported operators
    COMPARISON_OPS = {
        '==': operator.eq,
        '!=': operator.ne,
        '<': operator.lt,
        '>': operator.gt,
        '<=': operator.le,
        '>=': operator.ge,
    }

    LOGICAL_OPS = {
        'AND': operator.and_,
        'OR': operator.or_,
        'NOT': operator.not_,
    }

    def __init__(self):
        """Initialize expression evaluator."""
        pass

    def evaluate(self, expression: Dict, context: Dict) -> Tuple[bool, Dict]:
        """
        Evaluate an expression against context data.

        Args:
            expression: Rule expression (nested dict structure)
            context: Execution context data

        Returns:
            Tuple of (result: bool, details: Dict)

        Expression format examples:
        {
            "field": "user.age",
            "operator": ">=",
            "value": 18
        }

        {
            "AND": [
                {"field": "status", "operator": "==", "value": "active"},
                {"field": "balance", "operator": ">", "value": 0}
            ]
        }
        """
        details = {"expression": expression, "context_keys": list(context.keys())}

        try:
            result = self._evaluate_node(expression, context, details)
            details["result"] = result
            return result, details
        except Exception as e:
            details["error"] = str(e)
            raise RuleEvaluationError(f"Expression evaluation failed: {e}", details)

    def _evaluate_node(self, node: Dict, context: Dict, details: Dict) -> bool:
        """Recursively evaluate expression node."""

        # Logical operators (AND, OR, NOT)
        if "AND" in node:
            results = [self._evaluate_node(child, context, details) for child in node["AND"]]
            return all(results)

        if "OR" in node:
            results = [self._evaluate_node(child, context, details) for child in node["OR"]]
            return any(results)

        if "NOT" in node:
            return not self._evaluate_node(node["NOT"], context, details)

        # Comparison expression
        if "field" in node and "operator" in node:
            return self._evaluate_comparison(node, context, details)

        # Special operators
        if "IN" in node:
            return self._evaluate_membership(node, context, details, in_set=True)

        if "NOT IN" in node:
            return self._evaluate_membership(node, context, details, in_set=False)

        if "MATCHES" in node:
            return self._evaluate_pattern_match(node, context, details)

        if "CONTAINS" in node:
            return self._evaluate_contains(node, context, details)

        raise RuleEvaluationError(f"Unknown expression node type: {node}")

    def _evaluate_comparison(self, node: Dict, context: Dict, details: Dict) -> bool:
        """Evaluate comparison expression."""
        field = node["field"]
        op = node["operator"]
        expected_value = node["value"]

        # Get actual value from context using dot notation
        actual_value = self._get_field_value(field, context)

        # Handle special cases
        if op == "IS NULL":
            return actual_value is None
        if op == "IS NOT NULL":
            return actual_value is not None

        # Get comparison operator
        if op not in self.COMPARISON_OPS:
            raise RuleEvaluationError(f"Unknown operator: {op}")

        compare_fn = self.COMPARISON_OPS[op]

        # Type coercion for comparison
        actual_value, expected_value = self._coerce_types(actual_value, expected_value)

        try:
            result = compare_fn(actual_value, expected_value)
            details[f"comparison_{field}"] = {
                "actual": actual_value,
                "expected": expected_value,
                "operator": op,
                "result": result
            }
            return result
        except Exception as e:
            raise RuleEvaluationError(
                f"Comparison failed for {field}: {actual_value} {op} {expected_value}: {e}"
            )

    def _evaluate_membership(self, node: Dict, context: Dict, details: Dict, in_set: bool) -> bool:
        """Evaluate IN / NOT IN membership."""
        field = node.get("IN") or node.get("NOT IN")
        values = node.get("values", [])

        actual_value = self._get_field_value(field, context)
        result = actual_value in values

        if not in_set:
            result = not result

        details[f"membership_{field}"] = {
            "actual": actual_value,
            "values": values,
            "result": result
        }
        return result

    def _evaluate_pattern_match(self, node: Dict, context: Dict, details: Dict) -> bool:
        """Evaluate regex pattern match."""
        field = node["MATCHES"]["field"]
        pattern = node["MATCHES"]["pattern"]

        actual_value = str(self._get_field_value(field, context))

        try:
            result = bool(re.match(pattern, actual_value))
            details[f"pattern_match_{field}"] = {
                "value": actual_value,
                "pattern": pattern,
                "result": result
            }
            return result
        except Exception as e:
            raise RuleEvaluationError(f"Pattern match failed: {e}")

    def _evaluate_contains(self, node: Dict, context: Dict, details: Dict) -> bool:
        """Evaluate CONTAINS check."""
        field = node["CONTAINS"]["field"]
        substring = node["CONTAINS"]["value"]

        actual_value = str(self._get_field_value(field, context))
        result = substring in actual_value

        details[f"contains_{field}"] = {
            "value": actual_value,
            "substring": substring,
            "result": result
        }
        return result

    def _get_field_value(self, field_path: str, context: Dict) -> Any:
        """
        Get value from context using dot notation.

        Examples:
            "user.name" -> context["user"]["name"]
            "items[0].id" -> context["items"][0]["id"]
        """
        parts = field_path.split('.')
        value = context

        for part in parts:
            # Handle array indexing
            if '[' in part:
                key, index = part.split('[')
                index = int(index.rstrip(']'))
                value = value[key][index]
            else:
                if isinstance(value, dict):
                    value = value.get(part)
                else:
                    return None

            if value is None:
                return None

        return value

    def _coerce_types(self, actual: Any, expected: Any) -> Tuple[Any, Any]:
        """Coerce types for comparison."""
        # If both are same type, no coercion needed
        if type(actual) == type(expected):
            return actual, expected

        # Try to coerce actual to expected type
        try:
            if isinstance(expected, int) and isinstance(actual, str):
                return int(actual), expected
            if isinstance(expected, float) and isinstance(actual, (str, int)):
                return float(actual), expected
            if isinstance(expected, str):
                return str(actual), expected
        except (ValueError, TypeError):
            pass

        return actual, expected


class RuleEvaluationError(Exception):
    """Raised when rule evaluation fails."""

    def __init__(self, message: str, details: Dict = None):
        super().__init__(message)
        self.details = details or {}


class BusinessRulesEngine:
    """
    Business Rules Engine for deterministic decision-making.

    This engine evaluates business rules against execution context to make
    deterministic decisions at gates, avoiding inconsistent AI decision-making.
    """

    def __init__(self, database=None):
        """
        Initialize BRE.

        Args:
            database: Optional FlowDatabase instance for audit logging
        """
        self.evaluator = ExpressionEvaluator()
        self.database = database
        self.rule_cache = {}  # Cache compiled rules

    def evaluate_rule(self, rule: Dict, context: Dict, execution_id: str = None,
                     node_id: str = None) -> RuleEvaluation:
        """
        Evaluate a single rule against context.

        Args:
            rule: Rule definition (from database)
            context: Execution context data
            execution_id: Optional execution ID for audit logging
            node_id: Optional node ID for audit logging

        Returns:
            RuleEvaluation result
        """
        rule_id = rule.get('rule_id', 'unknown')
        rule_name = rule.get('name', 'unnamed')
        condition = rule.get('condition')

        if isinstance(condition, str):
            import json
            condition = json.loads(condition)

        evaluation_start = datetime.now()

        try:
            # Evaluate condition
            result, details = self.evaluator.evaluate(condition, context)

            # Determine status
            status = RuleStatus.PASS if result else RuleStatus.FAIL

            # Generate reason
            reason = self._generate_reason(rule_name, status, details)

            evaluation = RuleEvaluation(
                rule_id=rule_id,
                status=status,
                result=result,
                reason=reason,
                evaluated_at=evaluation_start,
                evaluation_details=details
            )

            # Log to database if available
            if self.database and execution_id and node_id:
                from database import GateStatus
                gate_status = GateStatus.PASS if result else GateStatus.FAIL
                self.database.record_gate_evaluation(
                    execution_id=execution_id,
                    node_id=node_id,
                    rule_id=rule_id,
                    status=gate_status,
                    input_context=context,
                    evaluation_result={"result": result, "details": details},
                    reason=reason
                )

            return evaluation

        except Exception as e:
            error_reason = f"Rule evaluation error: {str(e)}"
            evaluation = RuleEvaluation(
                rule_id=rule_id,
                status=RuleStatus.ERROR,
                result=False,
                reason=error_reason,
                evaluated_at=evaluation_start,
                evaluation_details={"error": str(e)}
            )

            # Log error to database
            if self.database and execution_id and node_id:
                from database import GateStatus
                self.database.record_gate_evaluation(
                    execution_id=execution_id,
                    node_id=node_id,
                    rule_id=rule_id,
                    status=GateStatus.FAIL,
                    input_context=context,
                    evaluation_result={"error": str(e)},
                    reason=error_reason
                )

            return evaluation

    def evaluate_gate(self, flow_id: str, node_id: str, context: Dict,
                     execution_id: str = None) -> Tuple[bool, List[RuleEvaluation]]:
        """
        Evaluate all gate rules for a node.

        Args:
            flow_id: Flow ID
            node_id: Node ID
            context: Execution context
            execution_id: Execution ID for audit logging

        Returns:
            Tuple of (all_passed: bool, evaluations: List[RuleEvaluation])
        """
        if not self.database:
            raise ValueError("Database required for gate evaluation")

        # Get all gate rules for this flow
        rules = self.database.get_rules_for_flow(flow_id, rule_type="gate")

        evaluations = []
        all_passed = True

        for rule in rules:
            evaluation = self.evaluate_rule(rule, context, execution_id, node_id)
            evaluations.append(evaluation)

            if evaluation.status != RuleStatus.PASS:
                all_passed = False

        return all_passed, evaluations

    def execute_action(self, action: Dict, context: Dict) -> Dict:
        """
        Execute rule action (for transformation rules).

        Args:
            action: Action definition
            context: Execution context

        Returns:
            Modified context
        """
        action_type = action.get('type')

        if action_type == 'set_field':
            field = action['field']
            value = action['value']
            # Support for computed values
            if isinstance(value, dict) and 'compute' in value:
                value = self._compute_value(value['compute'], context)

            self._set_field_value(field, value, context)

        elif action_type == 'remove_field':
            field = action['field']
            self._remove_field(field, context)

        elif action_type == 'merge_data':
            data = action['data']
            context.update(data)

        elif action_type == 'transform':
            # Custom transformation function
            transform_fn = action.get('function')
            if transform_fn:
                # Would load and execute custom transform function
                pass

        return context

    def _generate_reason(self, rule_name: str, status: RuleStatus, details: Dict) -> str:
        """Generate human-readable reason for rule evaluation result."""
        if status == RuleStatus.PASS:
            return f"Rule '{rule_name}' passed: all conditions met"
        else:
            # Find which conditions failed
            failed_conditions = []
            for key, value in details.items():
                if isinstance(value, dict) and value.get('result') == False:
                    failed_conditions.append(f"{key}: expected {value.get('expected')}, got {value.get('actual')}")

            if failed_conditions:
                return f"Rule '{rule_name}' failed: {'; '.join(failed_conditions)}"
            return f"Rule '{rule_name}' failed"

    def _compute_value(self, compute_expr: str, context: Dict) -> Any:
        """Compute a value from expression (simplified)."""
        # This would support expressions like "{{field1}} + {{field2}}"
        # For now, just return as-is
        return compute_expr

    def _set_field_value(self, field_path: str, value: Any, context: Dict):
        """Set field value using dot notation."""
        parts = field_path.split('.')
        current = context

        for i, part in enumerate(parts[:-1]):
            if part not in current:
                current[part] = {}
            current = current[part]

        current[parts[-1]] = value

    def _remove_field(self, field_path: str, context: Dict):
        """Remove field using dot notation."""
        parts = field_path.split('.')
        current = context

        for part in parts[:-1]:
            if part not in current:
                return
            current = current[part]

        if parts[-1] in current:
            del current[parts[-1]]

    def validate_rule_syntax(self, condition: Dict) -> Tuple[bool, Optional[str]]:
        """
        Validate rule condition syntax without executing.

        Returns:
            Tuple of (is_valid: bool, error_message: Optional[str])
        """
        try:
            # Try to parse the condition
            self._validate_node(condition)
            return True, None
        except Exception as e:
            return False, str(e)

    def _validate_node(self, node: Dict):
        """Recursively validate expression node structure."""
        if not isinstance(node, dict):
            raise ValueError("Expression node must be a dictionary")

        # Check for logical operators
        if "AND" in node:
            if not isinstance(node["AND"], list):
                raise ValueError("AND operator requires a list of conditions")
            for child in node["AND"]:
                self._validate_node(child)
            return

        if "OR" in node:
            if not isinstance(node["OR"], list):
                raise ValueError("OR operator requires a list of conditions")
            for child in node["OR"]:
                self._validate_node(child)
            return

        if "NOT" in node:
            self._validate_node(node["NOT"])
            return

        # Check for comparison
        if "field" in node:
            if "operator" not in node:
                raise ValueError("Comparison expression requires 'operator'")
            if node["operator"] not in ExpressionEvaluator.COMPARISON_OPS and \
               node["operator"] not in ["IS NULL", "IS NOT NULL"]:
                raise ValueError(f"Unknown operator: {node['operator']}")
            if node["operator"] not in ["IS NULL", "IS NOT NULL"] and "value" not in node:
                raise ValueError("Comparison expression requires 'value'")
            return

        # Check for other valid operators
        if any(key in node for key in ["IN", "NOT IN", "MATCHES", "CONTAINS"]):
            return

        raise ValueError(f"Invalid expression node structure: {node}")


# Example rule definitions for reference
EXAMPLE_RULES = {
    "simple_comparison": {
        "name": "Check minimum age",
        "condition": {
            "field": "user.age",
            "operator": ">=",
            "value": 18
        }
    },
    "logical_and": {
        "name": "Check active user with balance",
        "condition": {
            "AND": [
                {"field": "user.status", "operator": "==", "value": "active"},
                {"field": "user.balance", "operator": ">", "value": 0}
            ]
        }
    },
    "complex_nested": {
        "name": "Premium user or high-value transaction",
        "condition": {
            "OR": [
                {"field": "user.tier", "operator": "==", "value": "premium"},
                {
                    "AND": [
                        {"field": "transaction.amount", "operator": ">", "value": 1000},
                        {"field": "transaction.verified", "operator": "==", "value": True}
                    ]
                }
            ]
        }
    },
    "pattern_match": {
        "name": "Valid email format",
        "condition": {
            "MATCHES": {
                "field": "user.email",
                "pattern": r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
            }
        }
    }
}
