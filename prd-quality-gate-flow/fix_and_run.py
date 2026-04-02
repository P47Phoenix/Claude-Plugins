"""
Fix database issues and run a clean execution demonstration.

Restructured with named functions and main() guard.
Uses shared.get_connection() to ensure schema exists before DB operations,
fixing the latent ordering bug on fresh databases.
"""
import sys

from shared import DB_PATH, ensure_utf8_output, get_connection
from prd_flow_builder import PRDFlowBuilder
from business_rules_engine import BusinessRulesEngine


def clean_incomplete_executions(db_path=None):
    """Clean up incomplete executions from the database.

    Uses get_connection() which calls ensure_schema(), so this is safe
    to run even on a fresh database with no tables yet.

    Args:
        db_path: Path to SQLite database. Defaults to shared.DB_PATH.
    """
    if db_path is None:
        db_path = DB_PATH

    print("Cleaning up database for fresh execution...")

    conn = get_connection(db_path)
    try:
        conn.execute(
            "DELETE FROM audit_log WHERE execution_id IN "
            "(SELECT execution_id FROM executions WHERE status != 'completed')"
        )
        conn.execute(
            "DELETE FROM gate_evaluations WHERE execution_id IN "
            "(SELECT execution_id FROM executions WHERE status != 'completed')"
        )
        conn.execute(
            "DELETE FROM working_memory WHERE execution_id IN "
            "(SELECT execution_id FROM executions WHERE status != 'completed')"
        )
        conn.execute(
            "DELETE FROM node_executions WHERE execution_id IN "
            "(SELECT execution_id FROM executions WHERE status != 'completed')"
        )
        conn.execute("DELETE FROM executions WHERE status != 'completed'")
        conn.commit()
    finally:
        conn.close()

    print("+ Database cleaned")


def display_flow_structure(builder, flow_id):
    """Display the flow structure summary.

    Args:
        builder: PRDFlowBuilder instance with active connection.
        flow_id: The flow ID to inspect.
    """
    print(f"\nFlow: {builder.conn.execute('SELECT name FROM flows WHERE flow_id = ?', (flow_id,)).fetchone()['name']}")
    print(f"Flow ID: {flow_id}")

    nodes = builder.conn.execute("""
        SELECT node_type, COUNT(*) as count
        FROM nodes
        WHERE flow_id = ?
        GROUP BY node_type
    """, (flow_id,)).fetchall()

    print("\nFlow Structure:")
    for node in nodes:
        print(f"  - {node['node_type']}: {node['count']}")

    rules = builder.conn.execute("""
        SELECT COUNT(*) as count FROM business_rules WHERE flow_id = ?
    """, (flow_id,)).fetchone()

    print(f"  - business_rules: {rules['count']}")


def demonstrate_bre_evaluation(builder, flow_id):
    """Demonstrate the Business Rules Engine evaluation against Gate 1.

    Args:
        builder: PRDFlowBuilder instance with active connection.
        flow_id: The flow ID containing the gate to evaluate.
    """
    # Create test context (simulating PRD output)
    test_context = {
        "prd_document": {
            "problem_statement": (
                "This is a comprehensive problem statement that clearly defines "
                "the user need, market opportunity, and why this solution is "
                "necessary. It provides enough detail to ensure stakeholders "
                "understand the context and importance of this product."
            ),
            "target_users": ["Product Managers", "Engineers", "Executives"],
            "success_metrics": [
                {"name": "User Adoption", "target": "500 users in 3 months", "measurement": "Active user count"},
                {"name": "Feature Usage", "target": "60% weekly active", "measurement": "Weekly engagement rate"},
                {"name": "NPS Score", "target": ">40", "measurement": "Net Promoter Score"},
                {"name": "Response Time", "target": "<2 seconds", "measurement": "P95 latency"}
            ],
            "technical_requirements": {
                "platform": "Web",
                "stack": ["Python", "React", "PostgreSQL"],
                "apis": ["REST", "WebSocket"]
            },
            "dependencies": {
                "internal": ["auth_service", "notification_service"],
                "external": ["stripe", "sendgrid"]
            },
            "timeline": {
                "estimated_weeks": 10,
                "milestones": ["Design: 2w", "Dev: 6w", "Testing: 2w"]
            }
        }
    }

    print("\nTest Context (Simulated PRD Output):")
    print(f"  - Problem Statement: {len(test_context['prd_document']['problem_statement'])} chars")
    print(f"  - Success Metrics: {len(test_context['prd_document']['success_metrics'])} metrics")
    print(f"  - Timeline: {test_context['prd_document']['timeline']['estimated_weeks']} weeks")

    # Get Gate 1
    gate1 = builder.conn.execute("""
        SELECT * FROM nodes
        WHERE flow_id = ? AND name = 'gate1_completeness'
        LIMIT 1
    """, (flow_id,)).fetchone()

    if not gate1:
        print("\n! Gate 1 not found in flow")
        return

    print(f"\n{'-' * 80}")
    print(f"Evaluating: {gate1['name']}")
    print(f"Description: {gate1['description']}")
    print(f"{'-' * 80}")

    # Get rules for this gate
    rules = builder.conn.execute("""
        SELECT * FROM business_rules
        WHERE gate_node_id = ?
        ORDER BY priority DESC
    """, (gate1['node_id'],)).fetchall()

    print(f"\nBusiness Rules ({len(rules)} total):")

    bre = BusinessRulesEngine()

    all_passed = True
    total_score = 0

    for rule in rules:
        result = bre.evaluate_rule(dict(rule), test_context)

        status_symbol = "[PASS]" if result.passed else "[FAIL]"
        print(f"\n  {status_symbol} {rule['name']}")
        print(f"      Score: {result.score:.1f}/100")
        print(f"      Reason: {result.reason}")

        if not result.passed:
            all_passed = False
            print(f"      Details: {result.evaluation_details}")

        total_score += result.score

    avg_score = total_score / len(rules) if rules else 0

    print(f"\n{'-' * 80}")
    print(f"Gate 1 Overall Score: {avg_score:.1f}/100")
    print(f"Decision: {'GO' if avg_score >= 100 else 'RECYCLE'}")
    print(f"{'-' * 80}")


def display_all_gates(builder, flow_id):
    """Display overview of all gates in the flow.

    Args:
        builder: PRDFlowBuilder instance with active connection.
        flow_id: The flow ID to inspect.
    """
    gates = builder.conn.execute("""
        SELECT n.name, n.description, COUNT(r.rule_id) as rule_count
        FROM nodes n
        LEFT JOIN business_rules r ON n.node_id = r.gate_node_id
        WHERE n.flow_id = ? AND n.node_type = 'gate'
        GROUP BY n.node_id
        ORDER BY n.created_at
    """, (flow_id,)).fetchall()

    for i, gate in enumerate(gates, 1):
        print(f"\nGate {i}: {gate['name']}")
        print(f"  Description: {gate['description']}")
        print(f"  Rules: {gate['rule_count']}")


def display_summary():
    """Display the demonstration summary."""
    print(f"""
What was demonstrated:

1. Flow Structure:
   - 15 nodes orchestrated in a hierarchical tree
   - 7 quality gates with 20 business rules
   - Mix of automated and human decision points

2. Business Rules Engine:
   - Deterministic evaluation of gate conditions
   - Complex logic support (AND, OR, field comparisons)
   - Scoring and weighted evaluation
   - Clear pass/fail decisions with reasons

3. Gate 1 Evaluation:
   - All rules evaluated against simulated PRD data
   - Overall score calculated
   - Decision made (GO/RECYCLE)

4. Production-Ready Features:
   - SQLite database with full persistence
   - Audit trail capability
   - Working memory for context sharing
   - Episodic memory for learning (not shown)
   - Error handling and recovery (not shown)

Next Steps to see full execution:
   - Integrate actual Claude Code Task agents
   - Add human approval webhook system
   - Run complete end-to-end workflow

The system is ready for customization and integration!
""")


def main():
    """Run the complete fix-and-run demonstration."""
    ensure_utf8_output()

    # Step 1: Clean up incomplete executions
    clean_incomplete_executions()

    # Step 2: Demonstration header
    print("\n" + "=" * 80)
    print("PRD QUALITY GATE FLOW - DEMONSTRATION")
    print("=" * 80)

    # Step 3: Initialize builder and get flow
    builder = PRDFlowBuilder(DB_PATH)

    try:
        flow = builder.conn.execute(
            "SELECT * FROM flows ORDER BY created_at DESC LIMIT 1"
        ).fetchone()

        if not flow:
            print("! No flow found")
            sys.exit(1)

        flow_id = flow['flow_id']

        # Step 4: Display flow structure
        display_flow_structure(builder, flow_id)

        # Step 5: BRE demonstration
        print("\n" + "=" * 80)
        print("BUSINESS RULES ENGINE DEMONSTRATION")
        print("=" * 80)
        demonstrate_bre_evaluation(builder, flow_id)

        # Step 6: All gates overview
        print("\n" + "=" * 80)
        print("ALL GATES OVERVIEW")
        print("=" * 80)
        display_all_gates(builder, flow_id)

        # Step 7: Summary
        print("\n" + "=" * 80)
        print("DEMONSTRATION SUMMARY")
        print("=" * 80)
        display_summary()

    finally:
        builder.close()


if __name__ == "__main__":
    main()
