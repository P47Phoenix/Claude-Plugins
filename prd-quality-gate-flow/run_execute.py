"""
Wrapper script to run PRD execution with proper encoding
"""
import sys
import io
import asyncio
import json
from datetime import datetime

# Set UTF-8 encoding for output
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

from prd_flow_builder import PRDFlowBuilder
from flow_orchestrator import FlowOrchestrator
from business_rules_engine import BusinessRulesEngine

# Example product ideas
EXAMPLE_PRODUCT_IDEAS = {
    "saas_platform": {
        "product_idea": {
            "title": "AI-Powered Customer Support Dashboard",
            "description": "An intelligent dashboard that helps support teams manage customer inquiries using AI-powered routing, suggested responses, and sentiment analysis.",
            "submitter": "john@company.com",
            "business_justification": "Reduce support response time by 40% and improve customer satisfaction scores",
            "target_users": "Customer support teams in mid-size SaaS companies",
            "urgency": "HIGH",
            "category": "SAAS"
        }
    },
    "api_service": {
        "product_idea": {
            "title": "Real-Time Analytics API",
            "description": "A REST API that provides real-time analytics and reporting capabilities for embedded dashboards in third-party applications.",
            "submitter": "sarah@company.com",
            "business_justification": "Enable partners to integrate analytics, creating new revenue stream",
            "target_users": "Third-party developers and integration partners",
            "urgency": "MEDIUM",
            "category": "API"
        }
    },
    "internal_tool": {
        "product_idea": {
            "title": "Automated Code Review Assistant",
            "description": "Internal tool that automatically reviews pull requests, identifies security vulnerabilities, suggests improvements, and enforces coding standards.",
            "submitter": "mike@company.com",
            "business_justification": "Reduce code review time by 30% and improve code quality",
            "target_users": "Engineering team (50+ developers)",
            "urgency": "MEDIUM",
            "category": "INTERNAL"
        }
    }
}

async def execute_prd_workflow(product_idea: dict):
    """Execute PRD workflow"""
    print("\n" + "=" * 80)
    print("PRD QUALITY GATE WORKFLOW EXECUTION")
    print("=" * 80)

    # Initialize
    builder = PRDFlowBuilder("prd_flows.db")

    # Get existing flow
    existing_flow = builder.conn.execute("""
        SELECT flow_id FROM flows
        WHERE name = 'PRD Quality Gate System'
        ORDER BY created_at DESC
        LIMIT 1
    """).fetchone()

    if existing_flow:
        flow_id = existing_flow['flow_id']
        print(f"\n+ Using existing flow: {flow_id}")
    else:
        print("\n! No flow found. Please run: python run_builder.py")
        return

    # Create orchestrator
    bre = BusinessRulesEngine(builder.conn)
    orchestrator = FlowOrchestrator("prd_flows.db", bre)

    print("\n" + "-" * 80)
    print("EXECUTING FLOW")
    print("-" * 80)

    # Execute
    execution_id = await orchestrator.execute_flow(
        flow_id=flow_id,
        initial_context=product_idea
    )

    print("\n" + "=" * 80)
    print("EXECUTION COMPLETED")
    print("=" * 80)

    # Get status
    status = orchestrator.get_execution_status(execution_id)

    print(f"\nExecution ID: {execution_id}")
    print(f"Status: {status['status']}")
    print(f"Started: {status['started_at']}")
    print(f"Completed: {status['completed_at']}")

    if status['error']:
        print(f"\nERROR: {status['error']}")
    else:
        print("\n+ Flow completed successfully!")

    # Get audit trail
    print("\n" + "-" * 80)
    print("AUDIT TRAIL")
    print("-" * 80)

    audit_trail = orchestrator.get_audit_trail(execution_id)
    for event in audit_trail:
        print(f"\n[{event['timestamp']}] {event['event_type']}")
        print(f"  Actor: {event['actor']}")

    # Get gate evaluations
    print("\n" + "-" * 80)
    print("GATE EVALUATIONS")
    print("-" * 80)

    gate_evals = builder.conn.execute("""
        SELECT g.*, r.name as rule_name, n.name as gate_name
        FROM gate_evaluations g
        JOIN business_rules r ON g.rule_id = r.rule_id
        JOIN nodes n ON g.gate_node_id = n.node_id
        WHERE g.execution_id = ?
        ORDER BY g.evaluated_at
    """, (execution_id,)).fetchall()

    current_gate = None
    for eval in gate_evals:
        if eval['gate_name'] != current_gate:
            print(f"\n{eval['gate_name']}:")
            current_gate = eval['gate_name']

        status_symbol = "[PASS]" if eval['evaluation_result'] else "[FAIL]"
        print(f"  {status_symbol} {eval['rule_name']}")
        print(f"     Score: {eval['score']:.1f} | Decision: {eval['status']}")
        print(f"     Reason: {eval['reason']}")

    # Export report
    report_path = f"prd_execution_{execution_id}.json"
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump({
            "execution": {
                "execution_id": status['execution_id'],
                "status": status['status'],
                "started_at": status['started_at'],
                "completed_at": status['completed_at']
            },
            "audit_trail": audit_trail,
            "gate_evaluations": [
                {
                    "gate": eval['gate_name'],
                    "rule": eval['rule_name'],
                    "passed": bool(eval['evaluation_result']),
                    "score": eval['score'],
                    "reason": eval['reason']
                }
                for eval in gate_evals
            ]
        }, f, indent=2)

    print(f"\n+ Execution report saved to: {report_path}")

    # Cleanup
    orchestrator.close()
    builder.close()

    return execution_id

async def main():
    """Main execution"""
    print("\nPRD Quality Gate Flow Executor")
    print("=" * 80)

    # Check arguments
    if len(sys.argv) > 1:
        idea_type = sys.argv[1]
        if idea_type in EXAMPLE_PRODUCT_IDEAS:
            product_idea = EXAMPLE_PRODUCT_IDEAS[idea_type]
            print(f"\n+ Using example: {idea_type}")
        else:
            print(f"\n! Unknown example: {idea_type}")
            print(f"Available: {', '.join(EXAMPLE_PRODUCT_IDEAS.keys())}")
            return
    else:
        product_idea = EXAMPLE_PRODUCT_IDEAS["saas_platform"]
        print("\n+ Using default example: saas_platform")

    print("\nProduct Idea:")
    print(json.dumps(product_idea, indent=2))

    # Execute
    try:
        execution_id = await execute_prd_workflow(product_idea)
        print(f"\n+ Workflow execution completed: {execution_id}")
    except Exception as e:
        print(f"\n! Workflow execution failed: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())
