"""
PRD Quality Gate Flow Builder

Thin orchestrator that builds the PRD quality gate flow using
data-driven definitions from stage_definitions.py and gate_definitions.py.

Based on:
- ReAcTree hierarchical decomposition
- Anthropic workflow patterns
- Business Rules Engine for deterministic gates
- Episodic memory for continuous learning
"""

import json
import sqlite3
from enum import Enum
from typing import Dict, List, Optional, Any
from datetime import datetime

from shared import DB_PATH, generate_timestamp_id
from schema import ensure_schema
from stage_definitions import STAGE_DEFINITIONS
from gate_definitions import GATE_DEFINITIONS


class NodeType(Enum):
    """Types of nodes in the flow tree"""
    ROOT = "root"
    AGENT = "agent"
    CONTROL_FLOW = "control_flow"
    GATE = "gate"


class WorkflowPattern(Enum):
    """Anthropic workflow patterns"""
    PROMPT_CHAINING = "prompt_chaining"
    ROUTING = "routing"
    PARALLELIZATION = "parallelization"
    ORCHESTRATOR_WORKERS = "orchestrator_workers"
    EVALUATOR_OPTIMIZER = "evaluator_optimizer"


# Pipeline sequence defines the exact node ordering.
# Each entry is (type, index) where type is "stage" or "gate"
# and index is into STAGE_DEFINITIONS or GATE_DEFINITIONS.
#
# Irregularities handled:
#   - Gates 3 and 4 are consecutive (no stage between them)
#   - Stages 5 and 6 are consecutive (no gate between them)
#   - Stage 3 uses CONTROL_FLOW, not AGENT
PIPELINE_SEQUENCE = [
    ("stage", 0),   # stage1_prd_creator
    ("gate", 0),    # gate1_completeness
    ("stage", 1),   # stage2_technical_reviewer
    ("gate", 1),    # gate2_technical_feasibility
    ("stage", 2),   # stage3_stakeholder_orchestrator (CONTROL_FLOW)
    ("gate", 2),    # gate3_business_value
    ("gate", 3),    # gate4_executive_approval  (consecutive gates)
    ("stage", 3),   # stage4_implementation_planner
    ("gate", 4),    # gate5_resource_feasibility
    ("stage", 4),   # stage5_task_flow_generator
    ("stage", 5),   # stage6_prd_evaluator      (consecutive stages)
    ("gate", 5),    # gate6_success_criteria
    ("gate", 6),    # gate7_uat                  (consecutive gates)
    ("stage", 6),   # stage7_retrospective
]


class PRDFlowBuilder:
    """Builder for creating the PRD Quality Gate agentic flow"""

    def __init__(self, db_path: str = DB_PATH):
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row
        ensure_schema(self.conn)

    def create_flow(self, name: str, description: str, metadata: Optional[Dict] = None) -> str:
        """Create a new flow"""
        flow_id = generate_timestamp_id("flow")
        self.conn.execute(
            "INSERT INTO flows (flow_id, name, description, metadata) VALUES (?, ?, ?, ?)",
            (flow_id, name, description, json.dumps(metadata or {})))
        self.conn.commit()
        return flow_id

    def create_node(self, flow_id: str, node_type: NodeType, name: str,
                    description: str, parent_id: Optional[str] = None,
                    config: Optional[Dict] = None) -> str:
        """Create a new node in the flow"""
        node_id = f"{name}_{datetime.now().strftime('%Y%m%d%H%M%S%f')}"
        self.conn.execute(
            "INSERT INTO nodes (node_id, flow_id, parent_id, node_type, name, description, config)"
            " VALUES (?, ?, ?, ?, ?, ?, ?)",
            (node_id, flow_id, parent_id, node_type.value, name, description,
             json.dumps(config or {})))
        self.conn.commit()
        return node_id

    def create_rule(self, flow_id: str, name: str, rule_type: str, condition: Dict,
                    gate_node_id: Optional[str] = None, action: Optional[Dict] = None,
                    priority: int = 0, metadata: Optional[Dict] = None) -> str:
        """Create a business rule"""
        rule_id = generate_timestamp_id("rule")
        self.conn.execute(
            "INSERT INTO business_rules (rule_id, flow_id, gate_node_id, name, rule_type,"
            " condition, action, priority, metadata) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (rule_id, flow_id, gate_node_id, name, rule_type, json.dumps(condition),
             json.dumps(action or {}), priority, json.dumps(metadata or {})))
        self.conn.commit()
        return rule_id

    def build_prd_flow(self) -> str:
        """Build the complete PRD Quality Gate flow. Returns flow_id."""
        print("\U0001f3d7\ufe0f  Building PRD Quality Gate Flow...")
        flow_id = self.create_flow(
            name="PRD Quality Gate System",
            description="End-to-end product requirements document workflow with 7 quality gates",
            metadata={
                "version": "1.0.0",
                "author": "System",
                "gates_count": 7,
                "agents_count": 8,
                "execution_mode": "hybrid"
            }
        )

        print(f"\u2713 Flow created: {flow_id}")

        # Create root node
        root_id = self.create_node(
            flow_id=flow_id,
            node_type=NodeType.ROOT,
            name="prd_root",
            description="PRD workflow entry point"
        )

        # Walk the pipeline sequence, chaining parent_id
        parent_id = root_id
        for entry_type, idx in PIPELINE_SEQUENCE:
            if entry_type == "stage":
                stage = STAGE_DEFINITIONS[idx]
                node_type = NodeType(stage["node_type"])
                parent_id = self.create_node(
                    flow_id=flow_id,
                    node_type=node_type,
                    name=stage["name"],
                    description=stage["description"],
                    parent_id=parent_id,
                    config=stage["config"]
                )
            else:  # gate
                gate = GATE_DEFINITIONS[idx]
                gate_id = self.create_node(
                    flow_id=flow_id,
                    node_type=NodeType.GATE,
                    name=gate["name"],
                    description=gate["description"],
                    parent_id=parent_id,
                    config=gate["gate_config"]
                )
                # Create business rules for this gate
                for rule in gate["rules"]:
                    self.create_rule(
                        flow_id=flow_id,
                        gate_node_id=gate_id,
                        name=rule["name"],
                        rule_type=rule["rule_type"],
                        condition=rule["condition"],
                        action=rule.get("action"),
                        priority=rule["priority"],
                        metadata=rule.get("metadata")
                    )
                parent_id = gate_id

        self.conn.commit()

        print("\u2713 Flow tree structure created")
        print(f"\u2713 Total nodes created: {self._count_nodes(flow_id)}")
        print(f"\u2713 Total rules created: {self._count_rules(flow_id)}")

        return flow_id

    def _count_nodes(self, flow_id: str) -> int:
        """Count total nodes in flow"""
        result = self.conn.execute(
            "SELECT COUNT(*) as count FROM nodes WHERE flow_id = ?",
            (flow_id,)
        ).fetchone()
        return result['count']

    def _count_rules(self, flow_id: str) -> int:
        """Count total rules in flow"""
        result = self.conn.execute(
            "SELECT COUNT(*) as count FROM business_rules WHERE flow_id = ?",
            (flow_id,)
        ).fetchone()
        return result['count']

    def export_flow_diagram(self, flow_id: str) -> str:
        """Export flow as text diagram"""
        nodes = self.conn.execute(
            "SELECT * FROM nodes WHERE flow_id = ? ORDER BY created_at",
            (flow_id,)).fetchall()
        diagram = "PRD Quality Gate Flow\n" + "=" * 60 + "\n\n"
        for node in nodes:
            indent = "  " * self._get_node_depth(node['node_id'])
            diagram += f"{indent}[{node['node_type'].upper()}] {node['name']}\n"
            diagram += f"{indent}    {node['description']}\n"
            if node['node_type'] == 'gate':
                cnt = self.conn.execute(
                    "SELECT COUNT(*) as count FROM business_rules WHERE gate_node_id = ?",
                    (node['node_id'],)).fetchone()['count']
                diagram += f"{indent}    Rules: {cnt}\n"
            diagram += "\n"
        return diagram

    def _get_node_depth(self, node_id: str, depth: int = 0) -> int:
        """Get depth of node in tree"""
        node = self.conn.execute(
            "SELECT parent_id FROM nodes WHERE node_id = ?", (node_id,)).fetchone()
        if not node or not node['parent_id']:
            return depth
        return self._get_node_depth(node['parent_id'], depth + 1)

    def close(self):
        """Close database connection"""
        self.conn.close()


if __name__ == "__main__":
    # Build the PRD flow
    builder = PRDFlowBuilder()

    try:
        flow_id = builder.build_prd_flow()

        print("\n" + "=" * 60)
        print("\u2705 PRD Quality Gate Flow Built Successfully!")
        print("=" * 60)
        print(f"\nFlow ID: {flow_id}")
        print(f"Database: {DB_PATH}")

        # Export diagram
        diagram = builder.export_flow_diagram(flow_id)
        print("\n" + diagram)

        # Save diagram to file
        with open("prd_flow_diagram.txt", "w") as f:
            f.write(diagram)

        print("\U0001f4c4 Flow diagram saved to: prd_flow_diagram.txt")
        print("\n\u2728 Next steps:")
        print("  1. Review the flow structure in prd_flow_diagram.txt")
        print("  2. Customize business rules as needed")
        print("  3. Run prd_execute.py to execute the flow")

    finally:
        builder.close()
