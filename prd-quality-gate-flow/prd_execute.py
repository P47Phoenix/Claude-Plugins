"""
PRD Quality Gate Flow Executor

This script executes a PRD through the complete quality gate workflow.
"""

import asyncio
import json
import sys
from datetime import datetime
from prd_flow_builder import PRDFlowBuilder
from flow_orchestrator import FlowOrchestrator
from business_rules_engine import BusinessRulesEngine


async def execute_prd_workflow(product_idea: dict):
    """
    Execute a product idea through the PRD quality gate workflow

    Args:
        product_idea: Dictionary with product idea details

    Returns:
        execution_id: ID of the execution
    """
    print("\n" + "=" * 80)
    print("PRD QUALITY GATE WORKFLOW EXECUTION")
    print("=" * 80)

    # Initialize database and flow
    builder = PRDFlowBuilder("prd_flows.db")

    # Check if flow already exists
    existing_flow = builder.conn.execute("""
        SELECT flow_id FROM flows
        WHERE name = 'PRD Quality Gate System'
        ORDER BY created_at DESC
        LIMIT 1
    """).fetchone()

    if existing_flow:
        flow_id = existing_flow['flow_id']
        print(f"\n✓ Using existing flow: {flow_id}")
    else:
        print("\n🏗️  Building flow for first time...")
        flow_id = builder.build_prd_flow()
        print(f"✓ Flow created: {flow_id}")

    # Create orchestrator
    bre = BusinessRulesEngine(builder.conn)
    orchestrator = FlowOrchestrator("prd_flows.db", bre)

    print("\n" + "-" * 80)
    print("EXECUTING FLOW")
    print("-" * 80)

    # Execute flow with product idea
    execution_id = await orchestrator.execute_flow(
        flow_id=flow_id,
        initial_context=product_idea
    )

    print("\n" + "=" * 80)
    print("EXECUTION COMPLETED")
    print("=" * 80)

    # Get execution status
    status = orchestrator.get_execution_status(execution_id)

    print(f"\nExecution ID: {execution_id}")
    print(f"Status: {status['status']}")
    print(f"Started: {status['started_at']}")
    print(f"Completed: {status['completed_at']}")

    if status['error']:
        print(f"\n❌ Error: {status['error']}")
    else:
        print("\n✅ Flow completed successfully!")

    # Get audit trail
    print("\n" + "-" * 80)
    print("AUDIT TRAIL")
    print("-" * 80)

    audit_trail = orchestrator.get_audit_trail(execution_id)

    for event in audit_trail:
        print(f"\n[{event['timestamp']}] {event['event_type']}")
        print(f"  Actor: {event['actor']}")
        if event['event_data']:
            print(f"  Data: {json.dumps(event['event_data'], indent=4)}")

    # Get gate evaluations
    print("\n" + "-" * 80)
    print("GATE EVALUATIONS")
    print("-" * 80)

    gate_evals = builder.conn.execute("""
        SELECT g.*, r.name as rule_name
        FROM gate_evaluations g
        JOIN business_rules r ON g.rule_id = r.rule_id
        WHERE g.execution_id = ?
        ORDER BY g.evaluated_at
    """, (execution_id,)).fetchall()

    current_gate = None
    for eval in gate_evals:
        gate_name = builder.conn.execute(
            "SELECT name FROM nodes WHERE node_id = ?",
            (eval['gate_node_id'],)
        ).fetchone()['name']

        if gate_name != current_gate:
            print(f"\n{gate_name}:")
            current_gate = gate_name

        status_emoji = "✅" if eval['evaluation_result'] else "❌"
        print(f"  {status_emoji} {eval['rule_name']}")
        print(f"     Score: {eval['score']:.1f} | Decision: {eval['status']}")
        print(f"     Reason: {eval['reason']}")

    # Export final report
    report_path = f"prd_execution_{execution_id}.json"
    with open(report_path, "w") as f:
        json.dump({
            "execution": status,
            "audit_trail": audit_trail,
            "gate_evaluations": [
                {
                    "gate": eval['gate_node_id'],
                    "rule": eval['rule_name'],
                    "passed": bool(eval['evaluation_result']),
                    "score": eval['score'],
                    "reason": eval['reason']
                }
                for eval in gate_evals
            ]
        }, f, indent=2)

    print(f"\n📄 Execution report saved to: {report_path}")

    # Cleanup
    orchestrator.close()
    builder.close()

    return execution_id


# Example product ideas for testing

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


async def main():
    """Main execution function"""
    print("\n🚀 PRD Quality Gate Flow Executor")
    print("=" * 80)

    # Check if product idea provided as argument
    if len(sys.argv) > 1:
        idea_type = sys.argv[1]

        if idea_type in EXAMPLE_PRODUCT_IDEAS:
            product_idea = EXAMPLE_PRODUCT_IDEAS[idea_type]
            print(f"\n Using example: {idea_type}")
        else:
            print(f"\n❌ Unknown example type: {idea_type}")
            print(f"Available examples: {', '.join(EXAMPLE_PRODUCT_IDEAS.keys())}")
            return
    else:
        # Use default example
        product_idea = EXAMPLE_PRODUCT_IDEAS["saas_platform"]
        print("\n✨ Using default example: saas_platform")

    print("\nProduct Idea:")
    print(json.dumps(product_idea, indent=2))

    # Execute workflow
    try:
        execution_id = await execute_prd_workflow(product_idea)
        print(f"\n✅ Workflow execution completed: {execution_id}")

    except Exception as e:
        print(f"\n❌ Workflow execution failed: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
