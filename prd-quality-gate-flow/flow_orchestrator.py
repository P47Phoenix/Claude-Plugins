"""
Flow Orchestrator

Executes agentic flows with hierarchical task decomposition,
quality gates, and memory management.
"""

import json
import sqlite3
from typing import Dict, Any, Optional, List
from datetime import datetime
from enum import Enum
from dataclasses import dataclass

from business_rules_engine import BusinessRulesEngine, GateEvaluationResult


class ExecutionStatus(Enum):
    """Execution status values"""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    BLOCKED = "blocked"


@dataclass
class ExecutionResult:
    """Result of flow execution"""
    execution_id: str
    status: ExecutionStatus
    output: Optional[Dict[str, Any]]
    error: Optional[str]
    gates_passed: int
    gates_failed: int
    total_cost_tokens: int


class FlowOrchestrator:
    """
    Orchestrates execution of agentic flows

    Handles:
    - Node-by-node execution following tree structure
    - Gate evaluation using BRE
    - Working memory management
    - Episodic memory retrieval and storage
    - Audit logging
    """

    def __init__(
        self,
        db_path: str,
        bre: Optional[BusinessRulesEngine] = None
    ):
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row
        self.bre = bre or BusinessRulesEngine(self.conn)

    async def execute_flow(
        self,
        flow_id: str,
        initial_context: Dict[str, Any],
        execution_id: Optional[str] = None
    ) -> str:
        """
        Execute a flow from start to finish

        Args:
            flow_id: ID of flow to execute
            initial_context: Initial context/input data
            execution_id: Optional execution ID (generated if not provided)

        Returns:
            execution_id: ID of the execution
        """
        # Generate execution ID if not provided
        if not execution_id:
            execution_id = f"exec_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

        # Create execution record
        self.conn.execute("""
            INSERT INTO executions (
                execution_id, flow_id, status, input_context, started_at
            )
            VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP)
        """, (
            execution_id,
            flow_id,
            ExecutionStatus.RUNNING.value,
            json.dumps(initial_context)
        ))
        self.conn.commit()

        # Initialize working memory with initial context
        self._init_working_memory(execution_id, initial_context)

        # Log start
        self._log_audit_event(
            execution_id,
            "execution_started",
            {"flow_id": flow_id, "initial_context_keys": list(initial_context.keys())}
        )

        try:
            # Get root node
            root_node = self.conn.execute("""
                SELECT * FROM nodes
                WHERE flow_id = ? AND node_type = 'root'
                LIMIT 1
            """, (flow_id,)).fetchone()

            if not root_node:
                raise ValueError(f"No root node found for flow {flow_id}")

            # Execute from root
            await self._execute_node(root_node['node_id'], execution_id)

            # Get final result from working memory
            final_result = self._get_working_memory(execution_id)

            # Update execution as completed
            self.conn.execute("""
                UPDATE executions
                SET status = ?, output_result = ?, completed_at = CURRENT_TIMESTAMP
                WHERE execution_id = ?
            """, (
                ExecutionStatus.COMPLETED.value,
                json.dumps(final_result),
                execution_id
            ))
            self.conn.commit()

            self._log_audit_event(
                execution_id,
                "execution_completed",
                {"status": "success"}
            )

            return execution_id

        except Exception as e:
            # Update execution as failed
            self.conn.execute("""
                UPDATE executions
                SET status = ?, error_message = ?, completed_at = CURRENT_TIMESTAMP
                WHERE execution_id = ?
            """, (
                ExecutionStatus.FAILED.value,
                str(e),
                execution_id
            ))
            self.conn.commit()

            self._log_audit_event(
                execution_id,
                "execution_failed",
                {"error": str(e)}
            )

            raise

    async def _execute_node(
        self,
        node_id: str,
        execution_id: str
    ) -> Dict[str, Any]:
        """
        Execute a single node and its children

        Args:
            node_id: ID of node to execute
            execution_id: Current execution ID

        Returns:
            Node output data
        """
        # Get node
        node = self.conn.execute(
            "SELECT * FROM nodes WHERE node_id = ?",
            (node_id,)
        ).fetchone()

        if not node:
            raise ValueError(f"Node not found: {node_id}")

        node_config = json.loads(node['config']) if node['config'] else {}
        node_type = node['node_type']

        print(f"\n{'='*60}")
        print(f"Executing: [{node_type.upper()}] {node['name']}")
        print(f"{'='*60}")

        # Create node execution record
        node_exec_id = f"node_exec_{datetime.now().strftime('%Y%m%d%H%M%S%f')}"

        self.conn.execute("""
            INSERT INTO node_executions (
                node_exec_id, execution_id, node_id, status, started_at
            )
            VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP)
        """, (node_exec_id, execution_id, node_id, "running"))
        self.conn.commit()

        try:
            # Execute based on node type
            if node_type == "root":
                output = await self._execute_root_node(node, execution_id, node_config)
            elif node_type == "agent":
                output = await self._execute_agent_node(node, execution_id, node_config)
            elif node_type == "gate":
                output = await self._execute_gate_node(node, execution_id, node_config)
            elif node_type == "control_flow":
                output = await self._execute_control_flow_node(node, execution_id, node_config)
            else:
                raise ValueError(f"Unknown node type: {node_type}")

            # Update node execution as completed
            self.conn.execute("""
                UPDATE node_executions
                SET status = ?, output_data = ?, completed_at = CURRENT_TIMESTAMP
                WHERE node_exec_id = ?
            """, ("completed", json.dumps(output), node_exec_id))
            self.conn.commit()

            return output

        except Exception as e:
            # Update node execution as failed
            self.conn.execute("""
                UPDATE node_executions
                SET status = ?, completed_at = CURRENT_TIMESTAMP
                WHERE node_exec_id = ?
            """, ("failed", node_exec_id))
            self.conn.commit()

            raise

    async def _execute_root_node(
        self,
        node: sqlite3.Row,
        execution_id: str,
        config: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Execute root node - simply proceed to children"""
        print("Starting flow execution from root")

        # Get first child
        children = self._get_child_nodes(node['node_id'])

        if not children:
            return {"status": "no_children"}

        # Execute first child (sequential by default)
        return await self._execute_node(children[0]['node_id'], execution_id)

    async def _execute_agent_node(
        self,
        node: sqlite3.Row,
        execution_id: str,
        config: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Execute agent node - simulated for now"""
        print(f"Agent: {config.get('agent_type', 'generic')}")
        print(f"Goal: {config.get('goal', 'No goal specified')[:100]}...")

        # Get working memory inputs
        working_memory = self._get_working_memory(execution_id)
        input_keys = config.get('working_memory_input', [])

        input_data = {
            key: working_memory.get(key)
            for key in input_keys
            if key in working_memory
        }

        print(f"Input keys: {list(input_data.keys())}")

        # TODO: Actually execute agent using Claude Code Task or other agent system
        # For now, simulate with placeholder
        print("⚠️  SIMULATED EXECUTION (implement actual agent calls)")

        # Simulate output based on agent type
        output = self._simulate_agent_output(config.get('agent_type'), input_data)

        # Store output in working memory
        output_keys = config.get('working_memory_output', [])
        for key in output_keys:
            if key in output:
                self._set_working_memory(execution_id, key, output[key])

        print(f"Output keys: {list(output.keys())}")

        # Get next child node
        children = self._get_child_nodes(node['node_id'])

        if children:
            return await self._execute_node(children[0]['node_id'], execution_id)

        return output

    async def _execute_gate_node(
        self,
        node: sqlite3.Row,
        execution_id: str,
        config: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Execute gate node - evaluate business rules"""
        gate_number = config.get('gate_number', '?')
        gate_type = config.get('gate_type', 'automated')

        print(f"Gate {gate_number}: {node['description']}")
        print(f"Type: {gate_type}")

        # Get current context from working memory
        context = self._get_working_memory(execution_id)

        # Evaluate gate
        result = self.bre.evaluate_gate(node['node_id'], context, execution_id)

        print(f"Decision: {result.decision}")
        print(f"Score: {result.overall_score:.1f}")
        print(f"Reason: {result.reason}")

        if result.recommendations:
            print("Recommendations:")
            for rec in result.recommendations:
                print(f"  - {rec}")

        # Handle decision
        if result.decision in ["GO", "PASS", "APPROVE", "RELEASE"]:
            # Proceed to next node
            children = self._get_child_nodes(node['node_id'])
            if children:
                return await self._execute_node(children[0]['node_id'], execution_id)
            return {"gate_passed": True, "decision": result.decision}

        elif result.decision == "RECYCLE":
            # Go back to recycle target
            recycle_target = config.get('recycle_target')
            if recycle_target:
                print(f"⟲ Recycling to: {recycle_target}")
                # TODO: Implement recycling logic
                return {"gate_passed": False, "decision": result.decision, "recycle_to": recycle_target}

        elif result.decision in ["HOLD", "QUEUE"]:
            # Queue for later
            print("⏸️  Execution queued")
            return {"gate_passed": False, "decision": result.decision}

        elif result.decision in ["KILL", "REJECT"]:
            # Stop execution
            print("⛔ Execution rejected")
            raise Exception(f"Gate {gate_number} rejected: {result.reason}")

        elif result.decision == "PENDING_HUMAN_REVIEW":
            # Wait for human review
            print("👤 Awaiting human review")
            return {"gate_passed": False, "decision": result.decision, "pending_review": True}

        else:
            raise ValueError(f"Unknown gate decision: {result.decision}")

    async def _execute_control_flow_node(
        self,
        node: sqlite3.Row,
        execution_id: str,
        config: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Execute control flow node - orchestration patterns"""
        pattern = config.get('pattern', 'prompt_chaining')

        print(f"Control Flow Pattern: {pattern}")

        # Get children
        children = self._get_child_nodes(node['node_id'])

        if pattern == "prompt_chaining":
            # Execute children sequentially
            result = {}
            for child in children:
                result = await self._execute_node(child['node_id'], execution_id)
            return result

        elif pattern == "parallelization":
            # Execute children in parallel (simulated)
            print("⚡ Parallel execution (simulated as sequential)")
            results = []
            for child in children:
                result = await self._execute_node(child['node_id'], execution_id)
                results.append(result)
            return {"parallel_results": results}

        elif pattern == "orchestrator_workers":
            # First child is orchestrator, rest are workers
            if not children:
                return {}

            # Execute orchestrator
            orchestrator_result = await self._execute_node(children[0]['node_id'], execution_id)

            # Execute workers (could be parallel)
            worker_results = []
            for child in children[1:]:
                result = await self._execute_node(child['node_id'], execution_id)
                worker_results.append(result)

            return {"orchestrator": orchestrator_result, "workers": worker_results}

        else:
            raise ValueError(f"Unknown control flow pattern: {pattern}")

    def _simulate_agent_output(
        self,
        agent_type: Optional[str],
        input_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Simulate agent output for testing (replace with actual agent execution)"""

        # This is a placeholder - in production, this would call actual agents
        if agent_type == "prd-creator":
            return {
                "prd_document": {
                    "problem_statement": "A comprehensive problem statement describing the user need and market opportunity in detail.",
                    "target_users": ["Product Managers", "Engineers", "Executives"],
                    "success_metrics": [
                        {"name": "User Adoption", "target": "500 users in 3 months"},
                        {"name": "Feature Usage", "target": "60% weekly active"},
                        {"name": "NPS Score", "target": ">40"}
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
                    },
                    "strategic_alignment_score": 8,
                    "roi_projection": 150000,
                    "target_market_size": 5000
                },
                "success_metrics": ["User Adoption", "Feature Usage", "NPS Score"],
                "dependencies": ["auth_service", "notification_service", "stripe", "sendgrid"]
            }

        elif agent_type == "technical-reviewer":
            return {
                "technical_review": {
                    "feasibility": "MEDIUM",
                    "complexity_score": 6,
                    "effort_weeks": 10,
                    "risk_matrix": [
                        {"risk": "Integration complexity", "severity": "Medium", "mitigation": "POC first"},
                        {"risk": "Scalability", "severity": "Low", "mitigation": "Load testing"}
                    ]
                },
                "feasibility_score": 75,
                "risk_matrix": []
            }

        elif agent_type == "implementation-planner":
            return {
                "implementation_plan": {
                    "epics": ["User Authentication", "Core Features", "Analytics"],
                    "timeline_feasible": True,
                    "blocking_dependencies": []
                },
                "resource_requirements": {
                    "team_capacity_available": True,
                    "budget_required": False,
                    "budget_approved": True
                }
            }

        elif agent_type == "prd-evaluator":
            return {
                "evaluation_results": {
                    "success_score": 85,
                    "performance_score": 80,
                    "metrics_achieved": 3,
                    "user_feedback_positive": True
                },
                "success_score": 85,
                "implementation_results": {
                    "critical_defects_count": 0
                }
            }

        else:
            # Generic agent output
            return {"status": "completed", "agent_type": agent_type}

    def _get_child_nodes(self, parent_id: str) -> List[sqlite3.Row]:
        """Get child nodes of a parent"""
        return self.conn.execute("""
            SELECT * FROM nodes
            WHERE parent_id = ?
            ORDER BY created_at
        """, (parent_id,)).fetchall()

    def _init_working_memory(
        self,
        execution_id: str,
        initial_data: Dict[str, Any]
    ):
        """Initialize working memory with initial data"""
        for key, value in initial_data.items():
            self._set_working_memory(execution_id, key, value)

    def _get_working_memory(self, execution_id: str) -> Dict[str, Any]:
        """Get all working memory for execution"""
        rows = self.conn.execute("""
            SELECT memory_key, value
            FROM working_memory
            WHERE execution_id = ?
            AND (expires_at IS NULL OR expires_at > CURRENT_TIMESTAMP)
        """, (execution_id,)).fetchall()

        return {row['memory_key']: json.loads(row['value']) for row in rows}

    def _set_working_memory(
        self,
        execution_id: str,
        key: str,
        value: Any,
        expires_at: Optional[str] = None
    ):
        """Set working memory value"""
        self.conn.execute("""
            INSERT OR REPLACE INTO working_memory (
                memory_key, execution_id, value, expires_at
            )
            VALUES (?, ?, ?, ?)
        """, (key, execution_id, json.dumps(value), expires_at))
        self.conn.commit()

    def _log_audit_event(
        self,
        execution_id: str,
        event_type: str,
        event_data: Dict[str, Any],
        actor: str = "system"
    ):
        """Log audit event"""
        log_id = f"audit_{datetime.now().strftime('%Y%m%d%H%M%S%f')}"

        self.conn.execute("""
            INSERT INTO audit_log (log_id, execution_id, event_type, event_data, actor)
            VALUES (?, ?, ?, ?, ?)
        """, (log_id, execution_id, event_type, json.dumps(event_data), actor))
        self.conn.commit()

    def get_execution_status(self, execution_id: str) -> Dict[str, Any]:
        """Get execution status and results"""
        execution = self.conn.execute("""
            SELECT * FROM executions WHERE execution_id = ?
        """, (execution_id,)).fetchone()

        if not execution:
            return {"error": "Execution not found"}

        return {
            "execution_id": execution['execution_id'],
            "flow_id": execution['flow_id'],
            "status": execution['status'],
            "started_at": execution['started_at'],
            "completed_at": execution['completed_at'],
            "output": json.loads(execution['output_result']) if execution['output_result'] else None,
            "error": execution['error_message']
        }

    def get_audit_trail(self, execution_id: str) -> List[Dict[str, Any]]:
        """Get complete audit trail for execution"""
        logs = self.conn.execute("""
            SELECT * FROM audit_log
            WHERE execution_id = ?
            ORDER BY timestamp
        """, (execution_id,)).fetchall()

        return [
            {
                "timestamp": log['timestamp'],
                "event_type": log['event_type'],
                "event_data": json.loads(log['event_data']),
                "actor": log['actor']
            }
            for log in logs
        ]

    def close(self):
        """Close database connection"""
        self.conn.close()
