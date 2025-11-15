#!/usr/bin/env python3
"""
Flow Orchestrator - Executes hierarchical agentic flows using ReAcTree architecture
and Anthropic's workflow patterns.

Supports:
- Hierarchical agent tree decomposition (ReAcTree)
- Five workflow patterns (Anthropic):
  1. Prompt Chaining
  2. Routing (via BRE)
  3. Parallelization
  4. Orchestrator-Workers
  5. Evaluator-Optimizer
- Dual memory system (episodic + working)
- Deterministic gate decisions via BRE
- Comprehensive audit trail
"""

import asyncio
import json
from typing import Dict, List, Optional, Any, Tuple
from enum import Enum
from dataclasses import dataclass
from datetime import datetime

from database import FlowDatabase, NodeType, NodeStatus, GateStatus
from business_rules_engine import BusinessRulesEngine, RuleEvaluation, RuleStatus
from agent_registry import AgentRegistry, AgentType


class ExecutionMode(Enum):
    """Execution mode for the flow."""
    WORKFLOW = "workflow"  # Predefined paths, deterministic
    AGENT = "agent"  # LLM-directed, autonomous
    HYBRID = "hybrid"  # Mix of both


class WorkflowPattern(Enum):
    """Anthropic's five workflow patterns."""
    PROMPT_CHAINING = "prompt_chaining"
    ROUTING = "routing"
    PARALLELIZATION = "parallelization"
    ORCHESTRATOR_WORKERS = "orchestrator_workers"
    EVALUATOR_OPTIMIZER = "evaluator_optimizer"


@dataclass
class NodeExecutionResult:
    """Result of executing a single node."""
    node_id: str
    status: NodeStatus
    output_data: Dict[str, Any]
    error: Optional[str] = None
    child_results: List['NodeExecutionResult'] = None


class FlowOrchestrator:
    """
    Orchestrates execution of hierarchical agentic flows.

    Combines:
    - ReAcTree's hierarchical decomposition
    - Anthropic's workflow patterns
    - BRE for deterministic decisions
    - Dual memory systems
    """

    def __init__(self, database: FlowDatabase, rules_engine: BusinessRulesEngine,
                 agent_registry: AgentRegistry = None):
        """
        Initialize orchestrator.

        Args:
            database: Database for persistence
            rules_engine: Business rules engine for gates
            agent_registry: Optional agent registry for dynamic agent assignment
        """
        self.db = database
        self.bre = rules_engine
        self.bre.database = database  # Link BRE to database for audit
        self.agent_registry = agent_registry or AgentRegistry(database.db_path)

    async def execute_flow(self, flow_id: str, initial_context: Dict = None) -> str:
        """
        Execute a complete flow.

        Args:
            flow_id: ID of flow to execute
            initial_context: Initial execution context

        Returns:
            execution_id
        """
        # Create execution record
        execution_id = self.db.create_execution(flow_id, initial_context or {})

        try:
            # Update status to in_progress
            self.db.update_execution_status(execution_id, "in_progress")

            # Get flow tree
            nodes = self.db.get_flow_tree(flow_id)

            # Find root nodes
            root_nodes = [n for n in nodes if n['parent_id'] is None]

            if not root_nodes:
                raise ValueError(f"No root node found for flow {flow_id}")

            # Initialize working memory with initial context
            for key, value in (initial_context or {}).items():
                self.db.store_working_memory(
                    execution_id=execution_id,
                    node_id=root_nodes[0]['node_id'],
                    key=key,
                    value=value
                )

            # Execute root nodes
            results = []
            for root in root_nodes:
                result = await self.execute_node(
                    execution_id=execution_id,
                    node_id=root['node_id'],
                    input_data=initial_context or {}
                )
                results.append(result)

            # Determine overall status
            if all(r.status == NodeStatus.COMPLETED for r in results):
                self.db.update_execution_status(execution_id, "completed")
            else:
                self.db.update_execution_status(
                    execution_id, "failed",
                    error="One or more nodes failed"
                )

            return execution_id

        except Exception as e:
            self.db.update_execution_status(execution_id, "failed", error=str(e))
            raise

    async def execute_node(self, execution_id: str, node_id: str,
                          input_data: Dict) -> NodeExecutionResult:
        """
        Execute a single node in the tree.

        This implements the core ReAcTree logic with BRE-based gating.

        Args:
            execution_id: Execution ID
            node_id: Node to execute
            input_data: Input data for node

        Returns:
            NodeExecutionResult
        """
        # Get node details
        node = self.db.get_node(node_id)
        if not node:
            raise ValueError(f"Node {node_id} not found")

        node_type = NodeType(node['node_type'])
        config = json.loads(node['config']) if node['config'] else {}

        # Create node execution record
        node_exec_id = self.db.create_node_execution(execution_id, node_id, input_data)

        try:
            # Execute based on node type
            if node_type == NodeType.GATE:
                result = await self._execute_gate_node(
                    execution_id, node_id, node, input_data, config
                )
            elif node_type == NodeType.CONTROL_FLOW:
                result = await self._execute_control_flow_node(
                    execution_id, node_id, node, input_data, config
                )
            elif node_type == NodeType.AGENT:
                result = await self._execute_agent_node(
                    execution_id, node_id, node, input_data, config
                )
            else:  # ROOT
                result = await self._execute_children(
                    execution_id, node_id, input_data
                )

            # Update node execution
            self.db.update_node_execution(
                node_exec_id,
                result.status.value,
                result.output_data,
                result.error
            )

            return result

        except Exception as e:
            self.db.update_node_execution(
                node_exec_id,
                NodeStatus.FAILED.value,
                error=str(e)
            )
            raise

    async def _execute_gate_node(self, execution_id: str, node_id: str,
                                 node: Dict, input_data: Dict,
                                 config: Dict) -> NodeExecutionResult:
        """
        Execute a gate node using BRE for deterministic decisions.

        This is where we avoid AI inconsistency by using business rules.
        """
        flow_id = node['flow_id']

        # Get current context from working memory
        working_memory = self.db.retrieve_working_memory(execution_id)
        context = input_data.copy()
        for mem in working_memory:
            context[mem['key']] = json.loads(mem['value'])

        # Evaluate gate using BRE
        passed, evaluations = self.bre.evaluate_gate(
            flow_id=flow_id,
            node_id=node_id,
            context=context,
            execution_id=execution_id
        )

        if passed:
            # Gate passed - execute children
            child_results = await self._execute_children(execution_id, node_id, input_data)
            return NodeExecutionResult(
                node_id=node_id,
                status=NodeStatus.COMPLETED,
                output_data={
                    "gate_passed": True,
                    "evaluations": [
                        {
                            "rule_id": e.rule_id,
                            "status": e.status.value,
                            "reason": e.reason
                        } for e in evaluations
                    ],
                    "child_results": [r.output_data for r in child_results.child_results]
                },
                child_results=child_results.child_results
            )
        else:
            # Gate failed - skip children
            return NodeExecutionResult(
                node_id=node_id,
                status=NodeStatus.SKIPPED,
                output_data={
                    "gate_passed": False,
                    "evaluations": [
                        {
                            "rule_id": e.rule_id,
                            "status": e.status.value,
                            "reason": e.reason
                        } for e in evaluations
                    ]
                }
            )

    async def _execute_control_flow_node(self, execution_id: str, node_id: str,
                                        node: Dict, input_data: Dict,
                                        config: Dict) -> NodeExecutionResult:
        """
        Execute a control flow node (orchestration).

        Supports Anthropic's workflow patterns.
        """
        pattern = WorkflowPattern(config.get('pattern', 'prompt_chaining'))

        if pattern == WorkflowPattern.PROMPT_CHAINING:
            return await self._execute_prompt_chaining(execution_id, node_id, input_data)
        elif pattern == WorkflowPattern.ROUTING:
            return await self._execute_routing(execution_id, node_id, input_data, config)
        elif pattern == WorkflowPattern.PARALLELIZATION:
            return await self._execute_parallelization(execution_id, node_id, input_data)
        elif pattern == WorkflowPattern.ORCHESTRATOR_WORKERS:
            return await self._execute_orchestrator_workers(execution_id, node_id, input_data)
        elif pattern == WorkflowPattern.EVALUATOR_OPTIMIZER:
            return await self._execute_evaluator_optimizer(execution_id, node_id, input_data, config)
        else:
            # Default: sequential execution
            return await self._execute_children(execution_id, node_id, input_data)

    async def _execute_agent_node(self, execution_id: str, node_id: str,
                                  node: Dict, input_data: Dict,
                                  config: Dict) -> NodeExecutionResult:
        """
        Execute an agent node (LLM-capable reasoning unit).

        This is where actual LLM calls happen with episodic memory retrieval
        and dynamic agent assignment.
        """
        flow_id = node['flow_id']
        goal = config.get('goal', node['description'])

        # 1. SELECT BEST AGENT dynamically based on task
        required_tags = config.get('required_tags', [])
        prefer_agent_type = config.get('prefer_agent_type')

        if prefer_agent_type:
            prefer_agent_type = AgentType(prefer_agent_type)

        selected_agent = self.agent_registry.find_best_agent(
            task_description=goal,
            required_tags=required_tags,
            prefer_agent_type=prefer_agent_type
        )

        if not selected_agent:
            # Fallback to default
            all_agents = self.agent_registry.list_agents()
            selected_agent = all_agents[0] if all_agents else None

        if not selected_agent:
            raise ValueError("No agents available for task execution")

        # 2. ASSIGN AGENT to this node execution
        assignment_id = self.agent_registry.assign_agent(
            execution_id=execution_id,
            node_id=node_id,
            agent_id=selected_agent.agent_id
        )

        # Log agent selection
        self.db.audit_log(execution_id, node_id, "agent_selected", {
            "agent_id": selected_agent.agent_id,
            "agent_name": selected_agent.name,
            "assignment_id": assignment_id,
            "selection_criteria": {
                "goal": goal,
                "required_tags": required_tags
            }
        })

        try:
            # 3. RETRIEVE EPISODIC MEMORIES for this goal type
            goal_signature = self._compute_goal_signature(goal)
            memories = self.db.retrieve_episodic_memory(flow_id, goal_signature, limit=3)

            # 4. GET WORKING MEMORY
            working_memory = self.db.retrieve_working_memory(execution_id)

            # 5. PREPARE CONTEXT for agent execution
            context = {
                "goal": goal,
                "input": input_data,
                "episodic_examples": [json.loads(m['example_data']) for m in memories],
                "working_memory": {m['key']: json.loads(m['value']) for m in working_memory},
                "agent_config": selected_agent.config
            }

            # 6. EXECUTE with selected agent
            # This is where you would call the actual agent
            # For Claude agents, would use Claude API with agent config
            # For task agents, would invoke Claude Code task
            # For external agents, would call their API

            output_data = await self._invoke_agent(
                selected_agent, goal, context, input_data
            )

            # 7. MARK ASSIGNMENT as completed successfully
            self.agent_registry.complete_assignment(
                assignment_id=assignment_id,
                success=True,
                performance_score=output_data.get('confidence', 0.9)
            )

        except Exception as e:
            # Mark assignment as failed
            self.agent_registry.complete_assignment(
                assignment_id=assignment_id,
                success=False
            )
            raise

        # Store observation in working memory
        self.db.store_working_memory(
            execution_id=execution_id,
            node_id=node_id,
            key=f"node_{node_id}_result",
            value=output_data
        )

        # Optionally store as episodic memory for future use
        if config.get('store_episodic', False):
            self.db.store_episodic_memory(
                flow_id=flow_id,
                goal_signature=goal_signature,
                example_data={"input": input_data, "output": output_data},
                node_id=node_id,
                success=True
            )

        # Execute children with output as input
        child_results = await self._execute_children(execution_id, node_id, output_data)

        return NodeExecutionResult(
            node_id=node_id,
            status=NodeStatus.COMPLETED,
            output_data=output_data,
            child_results=child_results.child_results if child_results else None
        )

    # ==================== Workflow Pattern Implementations ====================

    async def _execute_prompt_chaining(self, execution_id: str, node_id: str,
                                      input_data: Dict) -> NodeExecutionResult:
        """
        Execute prompt chaining pattern: sequential LLM calls where each
        processes prior output.
        """
        children = self.db.get_child_nodes(node_id)
        current_data = input_data
        results = []

        for child in children:
            result = await self.execute_node(execution_id, child['node_id'], current_data)
            results.append(result)

            if result.status != NodeStatus.COMPLETED:
                break

            # Output of this node becomes input to next
            current_data = result.output_data

        return NodeExecutionResult(
            node_id=node_id,
            status=NodeStatus.COMPLETED,
            output_data=current_data,
            child_results=results
        )

    async def _execute_routing(self, execution_id: str, node_id: str,
                              input_data: Dict, config: Dict) -> NodeExecutionResult:
        """
        Execute routing pattern: classify input and route to appropriate handler.

        Uses BRE for deterministic routing decisions.
        """
        flow_id = self.db.get_node(node_id)['flow_id']

        # Get routing rules
        routing_rules = self.db.get_rules_for_flow(flow_id, rule_type="routing")

        # Evaluate routing rules
        selected_child = None
        for rule in routing_rules:
            evaluation = self.bre.evaluate_rule(rule, input_data, execution_id, node_id)
            if evaluation.status == RuleStatus.PASS:
                # Route to child specified in rule action
                action = json.loads(rule['action'])
                child_name = action.get('route_to')

                # Find child by name
                children = self.db.get_child_nodes(node_id)
                for child in children:
                    if child['name'] == child_name:
                        selected_child = child
                        break
                break

        if selected_child:
            result = await self.execute_node(execution_id, selected_child['node_id'], input_data)
            return NodeExecutionResult(
                node_id=node_id,
                status=NodeStatus.COMPLETED,
                output_data={
                    "routed_to": selected_child['name'],
                    "result": result.output_data
                },
                child_results=[result]
            )
        else:
            return NodeExecutionResult(
                node_id=node_id,
                status=NodeStatus.FAILED,
                output_data={},
                error="No routing rule matched"
            )

    async def _execute_parallelization(self, execution_id: str, node_id: str,
                                      input_data: Dict) -> NodeExecutionResult:
        """
        Execute parallelization pattern: run children concurrently.
        """
        children = self.db.get_child_nodes(node_id)

        # Execute all children in parallel
        tasks = [
            self.execute_node(execution_id, child['node_id'], input_data)
            for child in children
        ]
        results = await asyncio.gather(*tasks, return_exceptions=True)

        # Aggregate results
        successful_results = [r for r in results if isinstance(r, NodeExecutionResult) and r.status == NodeStatus.COMPLETED]

        return NodeExecutionResult(
            node_id=node_id,
            status=NodeStatus.COMPLETED if successful_results else NodeStatus.FAILED,
            output_data={
                "parallel_results": [r.output_data for r in successful_results],
                "success_count": len(successful_results),
                "total_count": len(results)
            },
            child_results=successful_results
        )

    async def _execute_orchestrator_workers(self, execution_id: str, node_id: str,
                                           input_data: Dict) -> NodeExecutionResult:
        """
        Execute orchestrator-workers pattern: central LLM dynamically breaks
        tasks and delegates to workers.
        """
        # First child is orchestrator, rest are workers
        children = self.db.get_child_nodes(node_id)

        if not children:
            return NodeExecutionResult(
                node_id=node_id,
                status=NodeStatus.FAILED,
                output_data={},
                error="No orchestrator node found"
            )

        orchestrator = children[0]
        workers = children[1:]

        # Execute orchestrator to get task breakdown
        orchestrator_result = await self.execute_node(
            execution_id, orchestrator['node_id'], input_data
        )

        # Orchestrator output should specify which workers to use and with what input
        task_assignments = orchestrator_result.output_data.get('task_assignments', [])

        # Execute assigned workers
        worker_results = []
        for assignment in task_assignments:
            worker_name = assignment['worker']
            worker_input = assignment['input']

            # Find worker by name
            for worker in workers:
                if worker['name'] == worker_name:
                    result = await self.execute_node(
                        execution_id, worker['node_id'], worker_input
                    )
                    worker_results.append(result)
                    break

        return NodeExecutionResult(
            node_id=node_id,
            status=NodeStatus.COMPLETED,
            output_data={
                "orchestration": orchestrator_result.output_data,
                "worker_results": [r.output_data for r in worker_results]
            },
            child_results=[orchestrator_result] + worker_results
        )

    async def _execute_evaluator_optimizer(self, execution_id: str, node_id: str,
                                          input_data: Dict, config: Dict) -> NodeExecutionResult:
        """
        Execute evaluator-optimizer pattern: iterative generation and evaluation.
        """
        children = self.db.get_child_nodes(node_id)

        if len(children) < 2:
            return NodeExecutionResult(
                node_id=node_id,
                status=NodeStatus.FAILED,
                output_data={},
                error="Evaluator-optimizer requires generator and evaluator nodes"
            )

        generator = children[0]
        evaluator = children[1]

        max_iterations = config.get('max_iterations', 3)
        threshold = config.get('quality_threshold', 0.8)

        best_result = None
        best_score = 0
        iterations = []

        for i in range(max_iterations):
            # Generate
            gen_result = await self.execute_node(
                execution_id, generator['node_id'], input_data
            )

            # Evaluate
            eval_result = await self.execute_node(
                execution_id, evaluator['node_id'], gen_result.output_data
            )

            score = eval_result.output_data.get('score', 0)
            iterations.append({
                "iteration": i + 1,
                "generation": gen_result.output_data,
                "evaluation": eval_result.output_data,
                "score": score
            })

            # Track best
            if score > best_score:
                best_score = score
                best_result = gen_result.output_data

            # Check if threshold met
            if score >= threshold:
                break

        return NodeExecutionResult(
            node_id=node_id,
            status=NodeStatus.COMPLETED,
            output_data={
                "best_result": best_result,
                "best_score": best_score,
                "iterations": iterations,
                "total_iterations": len(iterations)
            }
        )

    # ==================== Helper Methods ====================

    async def _execute_children(self, execution_id: str, parent_id: str,
                               input_data: Dict) -> NodeExecutionResult:
        """Execute all children of a node sequentially."""
        children = self.db.get_child_nodes(parent_id)
        results = []

        for child in children:
            result = await self.execute_node(execution_id, child['node_id'], input_data)
            results.append(result)

        return NodeExecutionResult(
            node_id=parent_id,
            status=NodeStatus.COMPLETED,
            output_data={"child_count": len(results)},
            child_results=results
        )

    async def _invoke_agent(self, agent, goal: str, context: Dict, input_data: Dict) -> Dict:
        """
        Invoke the selected agent to execute the task.

        This is the integration point for actual agent execution.
        """
        agent_type = agent.agent_type

        if agent_type == AgentType.GENERAL:
            # Use Claude API
            # In production: call Claude API with agent.config['model']
            output_data = {
                "goal": goal,
                "agent_used": agent.name,
                "reasoning": f"[Agent {agent.name}] would execute task here",
                "result": "Placeholder result - would call Claude API",
                "confidence": 0.9,
                "context_used": {
                    "episodic_memories": len(context.get('episodic_examples', [])),
                    "working_memory_keys": list(context.get('working_memory', {}).keys())
                }
            }

        elif agent_type == AgentType.TASK:
            # Invoke Claude Code Task agent
            # In production: use Claude Code's task invocation API
            output_data = {
                "goal": goal,
                "agent_used": agent.name,
                "task_agent": agent.name,
                "result": f"Placeholder - would invoke task agent {agent.name}",
                "confidence": 0.85
            }

        elif agent_type == AgentType.EXTERNAL:
            # Call external API
            # In production: HTTP call to agent.config['endpoint']
            output_data = {
                "goal": goal,
                "agent_used": agent.name,
                "external_service": agent.config.get('endpoint', 'unknown'),
                "result": "Placeholder - would call external API",
                "confidence": 0.8
            }

        else:
            output_data = {
                "goal": goal,
                "agent_used": agent.name,
                "result": "Unknown agent type",
                "confidence": 0.0
            }

        return output_data

    def _compute_goal_signature(self, goal: str) -> str:
        """Compute signature for goal to use in episodic memory retrieval."""
        import hashlib
        # Simple hash-based signature
        # In practice, could use semantic similarity
        return hashlib.md5(goal.encode()).hexdigest()[:16]

    def get_execution_status(self, execution_id: str) -> Dict:
        """Get current execution status with full audit trail."""
        execution = self.db.conn.execute(
            "SELECT * FROM executions WHERE execution_id = ?",
            (execution_id,)
        ).fetchone()

        if not execution:
            return None

        # Get audit trail
        audit_trail = self.db.get_execution_audit_trail(execution_id)

        # Get node executions
        node_execs = self.db.conn.execute("""
            SELECT ne.*, n.name, n.node_type
            FROM node_executions ne
            JOIN nodes n ON ne.node_id = n.node_id
            WHERE ne.execution_id = ?
            ORDER BY ne.started_at
        """, (execution_id,)).fetchall()

        return {
            "execution": dict(execution),
            "node_executions": [dict(ne) for ne in node_execs],
            "audit_trail": audit_trail
        }


# Example usage function
async def example_usage():
    """Example of using the flow orchestrator."""
    db = FlowDatabase("example_flows.db")
    bre = BusinessRulesEngine(db)
    orchestrator = FlowOrchestrator(db, bre)

    # Create a simple flow
    flow_id = db.create_flow(
        name="User Onboarding Flow",
        description="Onboard new users with validation gates"
    )

    # Create root node
    root_id = db.create_node(
        flow_id=flow_id,
        node_type=NodeType.ROOT,
        name="onboarding_root",
        description="Root of onboarding flow"
    )

    # Create gate node
    gate_id = db.create_node(
        flow_id=flow_id,
        node_type=NodeType.GATE,
        name="age_verification_gate",
        description="Verify user is 18+",
        parent_id=root_id
    )

    # Create gate rule
    db.create_rule(
        flow_id=flow_id,
        name="Minimum Age Check",
        rule_type="gate",
        condition={"field": "user.age", "operator": ">=", "value": 18}
    )

    # Create agent node
    agent_id = db.create_node(
        flow_id=flow_id,
        node_type=NodeType.AGENT,
        name="welcome_message_generator",
        description="Generate personalized welcome message",
        parent_id=gate_id,
        config={"goal": "Generate welcoming onboarding message"}
    )

    # Execute flow
    execution_id = await orchestrator.execute_flow(
        flow_id,
        initial_context={"user": {"age": 25, "name": "Alice"}}
    )

    # Get status
    status = orchestrator.get_execution_status(execution_id)
    print(json.dumps(status, indent=2, default=str))

    db.close()


if __name__ == "__main__":
    asyncio.run(example_usage())
