"""
Business Rules Engine (BRE)

Provides deterministic decision-making for quality gates.
Evaluates conditions against context data and returns clear pass/fail decisions.
"""

import json
import re
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime
import sqlite3


@dataclass
class RuleEvaluationResult:
    """Result of evaluating a single rule"""
    rule_id: str
    rule_name: str
    passed: bool
    score: float
    reason: str
    evaluation_details: Dict[str, Any]


@dataclass
class GateEvaluationResult:
    """Result of evaluating all rules for a gate"""
    gate_id: str
    gate_name: str
    decision: str  # GO, HOLD, RECYCLE, KILL, PASS, etc.
    overall_score: float
    passed: bool
    rule_results: List[RuleEvaluationResult]
    reason: str
    recommendations: List[str]


class BusinessRulesEngine:
    """
    Business Rules Engine for deterministic gate evaluation

    Supports:
    - Field comparisons (==, !=, >, <, >=, <=)
    - Null checks (IS NULL, IS NOT NULL)
    - Logical operators (AND, OR, NOT)
    - Pattern matching (MATCHES)
    - Collection operations (IN, length)
    """

    def __init__(self, db_connection: Optional[sqlite3.Connection] = None):
        self.conn = db_connection

    def evaluate_gate(
        self,
        gate_id: str,
        context: Dict[str, Any],
        execution_id: Optional[str] = None
    ) -> GateEvaluationResult:
        """
        Evaluate all rules for a gate and return decision

        Args:
            gate_id: ID of the gate node
            context: Current execution context data
            execution_id: Optional execution ID for logging

        Returns:
            GateEvaluationResult with decision and details
        """
        if not self.conn:
            raise ValueError("Database connection required for gate evaluation")

        # Get gate configuration
        gate = self.conn.execute(
            "SELECT * FROM nodes WHERE node_id = ?",
            (gate_id,)
        ).fetchone()

        if not gate:
            raise ValueError(f"Gate not found: {gate_id}")

        gate_config = json.loads(gate['config'])

        # Get all rules for this gate
        rules = self.conn.execute("""
            SELECT * FROM business_rules
            WHERE gate_node_id = ? AND enabled = TRUE
            ORDER BY priority DESC
        """, (gate_id,)).fetchall()

        if not rules:
            # No rules = automatic pass
            return GateEvaluationResult(
                gate_id=gate_id,
                gate_name=gate['name'],
                decision="GO",
                overall_score=100.0,
                passed=True,
                rule_results=[],
                reason="No rules configured, automatic pass",
                recommendations=[]
            )

        # Evaluate each rule
        rule_results = []
        total_weight = 0
        weighted_score = 0
        critical_failures = []
        recommendations = []

        for rule in rules:
            result = self.evaluate_rule(dict(rule), context)
            rule_results.append(result)

            # Get rule metadata
            metadata = json.loads(rule['metadata']) if rule['metadata'] else {}
            weight = metadata.get('weight', 10)
            is_critical = metadata.get('critical', False)

            total_weight += weight

            if result.passed:
                weighted_score += weight * result.score
            else:
                if is_critical:
                    critical_failures.append(result.rule_name)

                # Check for special actions
                if metadata.get('auto_kill_if_fail'):
                    return GateEvaluationResult(
                        gate_id=gate_id,
                        gate_name=gate['name'],
                        decision="KILL",
                        overall_score=0.0,
                        passed=False,
                        rule_results=rule_results,
                        reason=f"Critical failure: {result.rule_name}",
                        recommendations=[f"Fix: {result.reason}"]
                    )

                if metadata.get('requires_human_if_fail'):
                    recommendations.append(
                        f"Human review required for: {result.rule_name}"
                    )

        # Calculate overall score
        overall_score = (weighted_score / total_weight) if total_weight > 0 else 0

        # Determine decision based on gate type and score
        gate_type = gate_config.get('gate_type', 'automated')
        pass_threshold = gate_config.get('pass_threshold', 80)
        decision_options = gate_config.get('decision_options', ['GO', 'RECYCLE'])

        if gate_type == 'human':
            # Human gates always require review
            decision = "PENDING_HUMAN_REVIEW"
            passed = False
            reason = "Human review required"
        elif critical_failures:
            # Critical failures
            decision = "RECYCLE" if "RECYCLE" in decision_options else "HOLD"
            passed = False
            reason = f"Critical failures: {', '.join(critical_failures)}"
        elif overall_score >= pass_threshold:
            # Pass
            decision = "GO" if "GO" in decision_options else "PASS"
            passed = True
            reason = f"All checks passed (score: {overall_score:.1f})"
        elif overall_score >= pass_threshold * 0.7:
            # Partial pass - may need review or iteration
            if recommendations:
                decision = "PENDING_HUMAN_REVIEW"
                passed = False
                reason = f"Marginal score ({overall_score:.1f}), human review recommended"
            else:
                decision = "RECYCLE" if "RECYCLE" in decision_options else "HOLD"
                passed = False
                reason = f"Score below threshold ({overall_score:.1f} < {pass_threshold})"
        else:
            # Fail
            decision = "KILL" if "KILL" in decision_options else "REJECT"
            passed = False
            reason = f"Insufficient score ({overall_score:.1f})"

        # Log gate evaluation if execution_id provided
        if execution_id:
            self._log_gate_evaluation(
                execution_id,
                gate_id,
                rule_results,
                decision,
                overall_score,
                reason,
                context
            )

        return GateEvaluationResult(
            gate_id=gate_id,
            gate_name=gate['name'],
            decision=decision,
            overall_score=overall_score,
            passed=passed,
            rule_results=rule_results,
            reason=reason,
            recommendations=recommendations
        )

    def evaluate_rule(
        self,
        rule: Dict[str, Any],
        context: Dict[str, Any]
    ) -> RuleEvaluationResult:
        """
        Evaluate a single business rule against context

        Args:
            rule: Rule dictionary with condition
            context: Context data to evaluate against

        Returns:
            RuleEvaluationResult with pass/fail and details
        """
        rule_id = rule['rule_id']
        rule_name = rule['name']
        condition = json.loads(rule['condition'])

        try:
            passed = self._evaluate_condition(condition, context)
            score = 100.0 if passed else 0.0

            return RuleEvaluationResult(
                rule_id=rule_id,
                rule_name=rule_name,
                passed=passed,
                score=score,
                reason="Condition satisfied" if passed else "Condition not met",
                evaluation_details={
                    "condition": condition,
                    "context_snapshot": self._extract_relevant_context(condition, context)
                }
            )

        except Exception as e:
            return RuleEvaluationResult(
                rule_id=rule_id,
                rule_name=rule_name,
                passed=False,
                score=0.0,
                reason=f"Evaluation error: {str(e)}",
                evaluation_details={
                    "error": str(e),
                    "condition": condition
                }
            )

    def _evaluate_condition(self, condition: Dict[str, Any], context: Dict[str, Any]) -> bool:
        """
        Recursively evaluate a condition

        Supports:
        - Simple comparisons: {"field": "x", "operator": "==", "value": 5}
        - AND: {"AND": [cond1, cond2]}
        - OR: {"OR": [cond1, cond2]}
        - NOT: {"NOT": cond}
        - MATCHES: {"MATCHES": {"field": "x", "pattern": "regex"}}
        """
        # Handle logical operators
        if "AND" in condition:
            return all(self._evaluate_condition(c, context) for c in condition["AND"])

        if "OR" in condition:
            return any(self._evaluate_condition(c, context) for c in condition["OR"])

        if "NOT" in condition:
            return not self._evaluate_condition(condition["NOT"], context)

        # Handle pattern matching
        if "MATCHES" in condition:
            field = condition["MATCHES"]["field"]
            pattern = condition["MATCHES"]["pattern"]
            value = self._get_field_value(field, context)

            if value is None:
                return False

            return bool(re.match(pattern, str(value)))

        # Handle simple comparison
        if "field" in condition and "operator" in condition:
            field = condition["field"]
            operator = condition["operator"]
            expected_value = condition.get("value")

            actual_value = self._get_field_value(field, context)

            return self._compare_values(actual_value, operator, expected_value)

        # Unknown condition format
        raise ValueError(f"Invalid condition format: {condition}")

    def _get_field_value(self, field_path: str, context: Dict[str, Any]) -> Any:
        """
        Get value from context using dot notation

        Examples:
        - "user.age" -> context["user"]["age"]
        - "items.length" -> len(context["items"])
        """
        # Handle special .length accessor
        if field_path.endswith(".length"):
            base_path = field_path[:-7]  # Remove ".length"
            value = self._get_field_value(base_path, context)
            return len(value) if value is not None and hasattr(value, '__len__') else 0

        # Navigate dot notation
        parts = field_path.split(".")
        value = context

        for part in parts:
            if value is None:
                return None

            if isinstance(value, dict):
                value = value.get(part)
            else:
                # Try attribute access
                value = getattr(value, part, None)

        return value

    def _compare_values(self, actual: Any, operator: str, expected: Any) -> bool:
        """Compare two values using the specified operator"""

        # Handle NULL checks
        if operator == "IS NULL":
            return actual is None

        if operator == "IS NOT NULL":
            return actual is not None

        # If actual is None and we're not checking for null, fail
        if actual is None:
            return False

        # Handle operators
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

        raise ValueError(f"Unknown operator: {operator}")

    def _extract_relevant_context(
        self,
        condition: Dict[str, Any],
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Extract only the context fields referenced in condition"""
        fields = self._extract_field_paths(condition)
        return {
            field: self._get_field_value(field, context)
            for field in fields
        }

    def _extract_field_paths(self, condition: Dict[str, Any]) -> List[str]:
        """Recursively extract all field paths from condition"""
        fields = []

        if "field" in condition:
            fields.append(condition["field"])

        if "AND" in condition:
            for c in condition["AND"]:
                fields.extend(self._extract_field_paths(c))

        if "OR" in condition:
            for c in condition["OR"]:
                fields.extend(self._extract_field_paths(c))

        if "NOT" in condition:
            fields.extend(self._extract_field_paths(condition["NOT"]))

        if "MATCHES" in condition and "field" in condition["MATCHES"]:
            fields.append(condition["MATCHES"]["field"])

        return fields

    def _log_gate_evaluation(
        self,
        execution_id: str,
        gate_id: str,
        rule_results: List[RuleEvaluationResult],
        decision: str,
        score: float,
        reason: str,
        context: Dict[str, Any]
    ):
        """Log gate evaluation to database"""
        if not self.conn:
            return

        # Log each rule evaluation
        for result in rule_results:
            eval_id = f"eval_{datetime.now().strftime('%Y%m%d%H%M%S%f')}"

            self.conn.execute("""
                INSERT INTO gate_evaluations (
                    eval_id, execution_id, gate_node_id, rule_id,
                    status, evaluation_result, score, reason, context_snapshot
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                eval_id,
                execution_id,
                gate_id,
                result.rule_id,
                decision,
                result.passed,
                result.score,
                result.reason,
                json.dumps(result.evaluation_details)
            ))

        # Log audit event
        audit_id = f"audit_{datetime.now().strftime('%Y%m%d%H%M%S%f')}"

        self.conn.execute("""
            INSERT INTO audit_log (log_id, execution_id, event_type, event_data, actor)
            VALUES (?, ?, ?, ?, ?)
        """, (
            audit_id,
            execution_id,
            "gate_evaluation",
            json.dumps({
                "gate_id": gate_id,
                "decision": decision,
                "score": score,
                "reason": reason,
                "rules_evaluated": len(rule_results),
                "rules_passed": sum(1 for r in rule_results if r.passed)
            }),
            "BRE"
        ))

        self.conn.commit()


# Utility functions for creating common rule conditions

def field_equals(field: str, value: Any) -> Dict:
    """Create equality condition"""
    return {"field": field, "operator": "==", "value": value}


def field_not_equals(field: str, value: Any) -> Dict:
    """Create inequality condition"""
    return {"field": field, "operator": "!=", "value": value}


def field_greater_than(field: str, value: Any) -> Dict:
    """Create greater than condition"""
    return {"field": field, "operator": ">", "value": value}


def field_less_than(field: str, value: Any) -> Dict:
    """Create less than condition"""
    return {"field": field, "operator": "<", "value": value}


def field_is_null(field: str) -> Dict:
    """Create null check condition"""
    return {"field": field, "operator": "IS NULL"}


def field_is_not_null(field: str) -> Dict:
    """Create not null check condition"""
    return {"field": field, "operator": "IS NOT NULL"}


def all_of(*conditions) -> Dict:
    """Create AND condition"""
    return {"AND": list(conditions)}


def any_of(*conditions) -> Dict:
    """Create OR condition"""
    return {"OR": list(conditions)}


def none_of(condition: Dict) -> Dict:
    """Create NOT condition"""
    return {"NOT": condition}


def field_matches_pattern(field: str, pattern: str) -> Dict:
    """Create pattern matching condition"""
    return {"MATCHES": {"field": field, "pattern": pattern}}


# Example usage
if __name__ == "__main__":
    # Test the BRE
    bre = BusinessRulesEngine()

    # Test context
    context = {
        "prd_document": {
            "problem_statement": "This is a detailed problem statement that is more than 100 characters long to ensure it passes the minimum length requirement.",
            "target_users": ["developers", "product_managers"],
            "success_metrics": [
                {"name": "User adoption", "target": "80%"},
                {"name": "Response time", "target": "<200ms"},
                {"name": "User satisfaction", "target": ">4.5/5"}
            ],
            "technical_requirements": {"stack": "Python", "database": "PostgreSQL"},
            "dependencies": {"internal": ["auth_service"], "external": ["stripe"]},
            "timeline": {"estimated_weeks": 8},
            "strategic_alignment_score": 8
        },
        "technical_review": {
            "feasibility": "MEDIUM",
            "complexity_score": 6,
            "effort_weeks": 10
        }
    }

    # Test rule
    test_rule = {
        "rule_id": "test_1",
        "name": "Test Rule",
        "condition": json.dumps({
            "AND": [
                {"field": "prd_document.problem_statement", "operator": "IS NOT NULL"},
                {"field": "prd_document.success_metrics.length", "operator": ">=", "value": 3},
                {"field": "prd_document.strategic_alignment_score", "operator": ">=", "value": 7}
            ]
        }),
        "metadata": json.dumps({"weight": 30})
    }

    result = bre.evaluate_rule(test_rule, context)

    print("Rule Evaluation Result:")
    print(f"  Rule: {result.rule_name}")
    print(f"  Passed: {result.passed}")
    print(f"  Score: {result.score}")
    print(f"  Reason: {result.reason}")
    print(f"  Details: {json.dumps(result.evaluation_details, indent=2)}")
