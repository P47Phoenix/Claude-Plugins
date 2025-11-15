#!/usr/bin/env python3
"""
Complete Example: Customer Onboarding Flow with Multi-Gate Validation

This example demonstrates:
- Hierarchical agent tree structure
- Business rules engine for KYC gates
- Dynamic agent assignment
- Dual memory system
- Complete audit trail
- All 5 workflow patterns
"""

import asyncio
import sys
from pathlib import Path

# Add scripts to path
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

from database import FlowDatabase, NodeType
from business_rules_engine import BusinessRulesEngine
from flow_orchestrator import FlowOrchestrator, WorkflowPattern
from agent_registry import AgentRegistry


async def create_onboarding_flow():
    """
    Create a comprehensive customer onboarding flow.

    Flow Structure:
    Root
    ├── Gate: Age Verification (BRE)
    │   └── Control Flow: KYC Process (Orchestrator-Workers)
    │       ├── Agent: Orchestrator (Plan KYC steps)
    │       ├── Agent: Identity Verification
    │       ├── Agent: Address Verification
    │       └── Agent: Employment Verification
    ├── Gate: Credit Check (BRE)
    │   └── Agent: Credit Score Analyzer
    └── Control Flow: Account Setup (Prompt Chaining)
        ├── Agent: Generate Account Number
        ├── Agent: Create Welcome Email
        └── Agent: Schedule Onboarding Call
    """

    # Initialize database
    db = FlowDatabase("customer_onboarding.db")

    # Create flow
    flow_id = db.create_flow(
        name="Customer Onboarding Flow",
        description="Complete customer onboarding with KYC and compliance gates",
        metadata={
            "version": "1.0.0",
            "compliance": ["KYC", "AML", "Credit"],
            "industry": "financial_services"
        }
    )

    print(f"✓ Created flow: {flow_id}")

    # ==================== Build Tree Structure ====================

    # Root node
    root_id = db.create_node(
        flow_id=flow_id,
        node_type=NodeType.ROOT,
        name="onboarding_root",
        description="Customer onboarding entry point"
    )

    # ==================== Branch 1: Age Verification ====================

    age_gate_id = db.create_node(
        flow_id=flow_id,
        node_type=NodeType.GATE,
        name="age_verification_gate",
        description="Verify customer meets minimum age requirement",
        parent_id=root_id,
        position=1
    )

    # Age verification rule
    db.create_rule(
        flow_id=flow_id,
        name="Minimum Age Requirement",
        description="Customer must be at least 18 years old",
        rule_type="gate",
        condition={
            "field": "customer.age",
            "operator": ">=",
            "value": 18
        },
        priority=100
    )

    # KYC orchestrator (uses orchestrator-workers pattern)
    kyc_orchestrator_id = db.create_node(
        flow_id=flow_id,
        node_type=NodeType.CONTROL_FLOW,
        name="kyc_process",
        description="KYC verification process",
        parent_id=age_gate_id,
        config={
            "pattern": WorkflowPattern.ORCHESTRATOR_WORKERS.value
        }
    )

    # Orchestrator agent
    db.create_node(
        flow_id=flow_id,
        node_type=NodeType.AGENT,
        name="kyc_orchestrator",
        description="Plan and coordinate KYC verification steps",
        parent_id=kyc_orchestrator_id,
        position=1,
        config={
            "goal": "Analyze customer profile and determine required KYC verification steps",
            "required_tags": ["kyc", "compliance", "planning"],
            "store_episodic": True
        }
    )

    # Worker agents
    db.create_node(
        flow_id=flow_id,
        node_type=NodeType.AGENT,
        name="identity_verifier",
        description="Verify customer identity documents",
        parent_id=kyc_orchestrator_id,
        position=2,
        config={
            "goal": "Verify identity documents (passport, driver's license, etc.)",
            "required_tags": ["kyc", "identity", "documents"]
        }
    )

    db.create_node(
        flow_id=flow_id,
        node_type=NodeType.AGENT,
        name="address_verifier",
        description="Verify customer address",
        parent_id=kyc_orchestrator_id,
        position=3,
        config={
            "goal": "Verify customer residential address through utility bills or bank statements",
            "required_tags": ["kyc", "address", "documents"]
        }
    )

    db.create_node(
        flow_id=flow_id,
        node_type=NodeType.AGENT,
        name="employment_verifier",
        description="Verify customer employment",
        parent_id=kyc_orchestrator_id,
        position=4,
        config={
            "goal": "Verify customer employment status and income",
            "required_tags": ["kyc", "employment", "income"]
        }
    )

    # ==================== Branch 2: Credit Check ====================

    credit_gate_id = db.create_node(
        flow_id=flow_id,
        node_type=NodeType.GATE,
        name="credit_check_gate",
        description="Verify customer meets credit requirements",
        parent_id=root_id,
        position=2
    )

    # Credit check rules
    db.create_rule(
        flow_id=flow_id,
        name="Minimum Credit Score",
        description="Credit score must be at least 650",
        rule_type="gate",
        condition={
            "field": "customer.credit_score",
            "operator": ">=",
            "value": 650
        },
        priority=100
    )

    db.create_rule(
        flow_id=flow_id,
        name="Debt-to-Income Ratio",
        description="Debt-to-income ratio must be below 43%",
        rule_type="gate",
        condition={
            "field": "customer.debt_to_income_ratio",
            "operator": "<=",
            "value": 0.43
        },
        priority=90
    )

    db.create_rule(
        flow_id=flow_id,
        name="No Recent Bankruptcies",
        description="No bankruptcies in the last 7 years",
        rule_type="gate",
        condition={
            "field": "customer.bankruptcies_last_7_years",
            "operator": "==",
            "value": 0
        },
        priority=95
    )

    # Credit analyzer agent
    db.create_node(
        flow_id=flow_id,
        node_type=NodeType.AGENT,
        name="credit_analyzer",
        description="Analyze customer credit profile",
        parent_id=credit_gate_id,
        config={
            "goal": "Analyze credit report and provide detailed credit risk assessment",
            "required_tags": ["credit", "risk", "analysis"],
            "store_episodic": True
        }
    )

    # ==================== Branch 3: Account Setup ====================

    account_setup_id = db.create_node(
        flow_id=flow_id,
        node_type=NodeType.CONTROL_FLOW,
        name="account_setup",
        description="Set up customer account",
        parent_id=root_id,
        position=3,
        config={
            "pattern": WorkflowPattern.PROMPT_CHAINING.value
        }
    )

    # Chained agents for account setup
    db.create_node(
        flow_id=flow_id,
        node_type=NodeType.AGENT,
        name="account_number_generator",
        description="Generate unique account number",
        parent_id=account_setup_id,
        position=1,
        config={
            "goal": "Generate a unique account number following bank's format requirements",
            "required_tags": ["account", "generation"]
        }
    )

    db.create_node(
        flow_id=flow_id,
        node_type=NodeType.AGENT,
        name="welcome_email_creator",
        description="Create personalized welcome email",
        parent_id=account_setup_id,
        position=2,
        config={
            "goal": "Create personalized welcome email with account details and next steps",
            "required_tags": ["email", "writing", "personalization"]
        }
    )

    db.create_node(
        flow_id=flow_id,
        node_type=NodeType.AGENT,
        name="onboarding_call_scheduler",
        description="Schedule onboarding call",
        parent_id=account_setup_id,
        position=3,
        config={
            "goal": "Schedule onboarding call based on customer availability and preferences",
            "required_tags": ["scheduling", "calendar"]
        }
    )

    print(f"✓ Created tree structure with {len(db.get_flow_tree(flow_id))} nodes")

    return db, flow_id


async def execute_onboarding(db: FlowDatabase, flow_id: str):
    """Execute the onboarding flow with sample customer data."""

    # Initialize orchestrator with BRE and agent registry
    bre = BusinessRulesEngine(db)
    registry = AgentRegistry(db.db_path)
    orchestrator = FlowOrchestrator(db, bre, registry)

    # Sample customer data
    customer_data = {
        "customer": {
            "name": "Alice Johnson",
            "age": 32,
            "email": "alice.johnson@example.com",
            "phone": "+1-555-0123",
            "address": {
                "street": "123 Main St",
                "city": "San Francisco",
                "state": "CA",
                "zip": "94102"
            },
            "employment": {
                "status": "employed",
                "employer": "Tech Corp",
                "annual_income": 120000,
                "years_employed": 5
            },
            "credit_score": 720,
            "debt_to_income_ratio": 0.35,
            "bankruptcies_last_7_years": 0,
            "documents": {
                "passport": "provided",
                "utility_bill": "provided",
                "pay_stub": "provided"
            }
        }
    }

    print("\n" + "="*60)
    print("EXECUTING CUSTOMER ONBOARDING FLOW")
    print("="*60)
    print(f"Customer: {customer_data['customer']['name']}")
    print(f"Age: {customer_data['customer']['age']}")
    print(f"Credit Score: {customer_data['customer']['credit_score']}")
    print("="*60 + "\n")

    # Execute flow
    execution_id = await orchestrator.execute_flow(flow_id, customer_data)

    print(f"\n✓ Execution completed: {execution_id}")

    return orchestrator, execution_id


def print_audit_report(orchestrator: FlowOrchestrator, execution_id: str):
    """Print comprehensive audit report."""

    print("\n" + "="*60)
    print("AUDIT REPORT")
    print("="*60)

    # Get execution status
    status = orchestrator.get_execution_status(execution_id)

    # Get audit trail
    audit_trail = orchestrator.db.get_execution_audit_trail(execution_id)

    print(f"\nExecution Status: {status['execution']['status']}")
    print(f"Started: {status['execution']['started_at']}")
    print(f"Completed: {status['execution']['completed_at']}")

    print(f"\n--- Statistics ---")
    stats = audit_trail['statistics']
    print(f"Total Events: {stats['total_events']}")
    print(f"Event Types: {stats['event_types']}")

    print(f"\n--- Gate Evaluations ---")
    gate_evals = orchestrator.db.conn.execute("""
        SELECT ge.*, br.name as rule_name
        FROM gate_evaluations ge
        JOIN business_rules br ON ge.rule_id = br.rule_id
        WHERE ge.execution_id = ?
        ORDER BY ge.evaluated_at
    """, (execution_id,)).fetchall()

    for eval in gate_evals:
        status_symbol = "✓" if eval['status'] == 'pass' else "✗"
        print(f"{status_symbol} {eval['rule_name']}: {eval['status'].upper()}")
        print(f"  Reason: {eval['reason']}")

    print(f"\n--- Agent Assignments ---")
    agent_assignments = orchestrator.db.conn.execute("""
        SELECT aa.*, a.name as agent_name, n.name as node_name
        FROM agent_assignments aa
        JOIN agents a ON aa.agent_id = a.agent_id
        JOIN nodes n ON aa.node_id = n.node_id
        WHERE aa.execution_id = ?
        ORDER BY aa.assigned_at
    """, (execution_id,)).fetchall()

    for assignment in agent_assignments:
        success_symbol = "✓" if assignment['success'] else "✗"
        print(f"{success_symbol} Node: {assignment['node_name']}")
        print(f"  Agent: {assignment['agent_name']}")
        print(f"  Performance: {assignment['performance_score']}")

    print(f"\n--- Node Executions ---")
    for node_exec in status['node_executions']:
        status_symbol = "✓" if node_exec['status'] == 'completed' else "✗"
        print(f"{status_symbol} {node_exec['name']} ({node_exec['node_type']}): {node_exec['status']}")

    print("\n" + "="*60)


async def main():
    """Main example execution."""

    print("="*60)
    print("AGENTIC FLOW BUILDER - COMPLETE EXAMPLE")
    print("Customer Onboarding with KYC and Compliance")
    print("="*60 + "\n")

    # Create flow
    db, flow_id = await create_onboarding_flow()

    # Execute flow
    orchestrator, execution_id = await execute_onboarding(db, flow_id)

    # Print audit report
    print_audit_report(orchestrator, execution_id)

    # Show agent performance
    print("\n--- Agent Performance Summary ---")
    registry = orchestrator.agent_registry
    for agent in registry.list_agents():
        perf = registry.get_agent_performance(agent.agent_id)
        if perf['total_assignments'] > 0:
            print(f"\n{agent.name} ({agent.agent_type.value}):")
            print(f"  Total assignments: {perf['total_assignments']}")
            print(f"  Success rate: {perf['success_rate']*100:.1f}%")
            print(f"  Avg score: {perf['avg_score']:.2f}")

    # Close database
    db.close()

    print("\n✓ Example completed successfully!")
    print(f"\nDatabase saved to: customer_onboarding.db")
    print("You can inspect the database to see full audit trail.\n")


if __name__ == "__main__":
    asyncio.run(main())
