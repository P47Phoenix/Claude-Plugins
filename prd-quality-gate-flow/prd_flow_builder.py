"""
PRD Quality Gate Flow Builder

This script creates a production-grade agentic flow for managing
Product Requirements Documents (PRDs) through a 7-gate quality system.

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


class PRDFlowBuilder:
    """Builder for creating the PRD Quality Gate agentic flow"""

    def __init__(self, db_path: str = "prd_flows.db"):
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row
        self._create_schema()

    def _create_schema(self):
        """Create database schema for flow, nodes, rules, and execution tracking"""

        # Flows table
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS flows (
                flow_id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                description TEXT,
                version TEXT DEFAULT '1.0.0',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                metadata JSON
            )
        """)

        # Nodes table
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS nodes (
                node_id TEXT PRIMARY KEY,
                flow_id TEXT NOT NULL,
                parent_id TEXT,
                node_type TEXT NOT NULL,
                name TEXT NOT NULL,
                description TEXT,
                config JSON,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (flow_id) REFERENCES flows(flow_id),
                FOREIGN KEY (parent_id) REFERENCES nodes(node_id)
            )
        """)

        # Business rules table
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS business_rules (
                rule_id TEXT PRIMARY KEY,
                flow_id TEXT NOT NULL,
                gate_node_id TEXT,
                name TEXT NOT NULL,
                rule_type TEXT NOT NULL,
                condition JSON NOT NULL,
                action JSON,
                priority INTEGER DEFAULT 0,
                enabled BOOLEAN DEFAULT TRUE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                metadata JSON,
                FOREIGN KEY (flow_id) REFERENCES flows(flow_id),
                FOREIGN KEY (gate_node_id) REFERENCES nodes(node_id)
            )
        """)

        # Executions table
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS executions (
                execution_id TEXT PRIMARY KEY,
                flow_id TEXT NOT NULL,
                status TEXT NOT NULL,
                input_context JSON,
                output_result JSON,
                started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                completed_at TIMESTAMP,
                error_message TEXT,
                metadata JSON,
                FOREIGN KEY (flow_id) REFERENCES flows(flow_id)
            )
        """)

        # Node executions table
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS node_executions (
                node_exec_id TEXT PRIMARY KEY,
                execution_id TEXT NOT NULL,
                node_id TEXT NOT NULL,
                status TEXT NOT NULL,
                input_data JSON,
                output_data JSON,
                started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                completed_at TIMESTAMP,
                agent_used TEXT,
                cost_tokens INTEGER,
                FOREIGN KEY (execution_id) REFERENCES executions(execution_id),
                FOREIGN KEY (node_id) REFERENCES nodes(node_id)
            )
        """)

        # Gate evaluations table
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS gate_evaluations (
                eval_id TEXT PRIMARY KEY,
                execution_id TEXT NOT NULL,
                gate_node_id TEXT NOT NULL,
                rule_id TEXT NOT NULL,
                status TEXT NOT NULL,
                evaluation_result BOOLEAN,
                score DECIMAL(5,2),
                reason TEXT,
                evaluated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                context_snapshot JSON,
                FOREIGN KEY (execution_id) REFERENCES executions(execution_id),
                FOREIGN KEY (gate_node_id) REFERENCES nodes(node_id),
                FOREIGN KEY (rule_id) REFERENCES business_rules(rule_id)
            )
        """)

        # Episodic memory table
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS episodic_memory (
                memory_id TEXT PRIMARY KEY,
                flow_id TEXT NOT NULL,
                goal_signature TEXT NOT NULL,
                example_data JSON NOT NULL,
                success BOOLEAN NOT NULL,
                execution_id TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                metadata JSON,
                FOREIGN KEY (flow_id) REFERENCES flows(flow_id),
                FOREIGN KEY (execution_id) REFERENCES executions(execution_id)
            )
        """)

        # Working memory table (execution-specific)
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS working_memory (
                memory_key TEXT NOT NULL,
                execution_id TEXT NOT NULL,
                value JSON NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                expires_at TIMESTAMP,
                PRIMARY KEY (memory_key, execution_id),
                FOREIGN KEY (execution_id) REFERENCES executions(execution_id)
            )
        """)

        # Audit log table
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS audit_log (
                log_id TEXT PRIMARY KEY,
                execution_id TEXT NOT NULL,
                event_type TEXT NOT NULL,
                event_data JSON,
                actor TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (execution_id) REFERENCES executions(execution_id)
            )
        """)

        # Create indexes
        self.conn.execute("CREATE INDEX IF NOT EXISTS idx_nodes_flow ON nodes(flow_id)")
        self.conn.execute("CREATE INDEX IF NOT EXISTS idx_nodes_parent ON nodes(parent_id)")
        self.conn.execute("CREATE INDEX IF NOT EXISTS idx_rules_flow ON business_rules(flow_id)")
        self.conn.execute("CREATE INDEX IF NOT EXISTS idx_rules_gate ON business_rules(gate_node_id)")
        self.conn.execute("CREATE INDEX IF NOT EXISTS idx_executions_flow ON executions(flow_id)")
        self.conn.execute("CREATE INDEX IF NOT EXISTS idx_gate_evals_exec ON gate_evaluations(execution_id)")
        self.conn.execute("CREATE INDEX IF NOT EXISTS idx_episodic_goal ON episodic_memory(goal_signature)")

        self.conn.commit()

    def create_flow(self, name: str, description: str, metadata: Optional[Dict] = None) -> str:
        """Create a new flow"""
        flow_id = f"flow_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

        self.conn.execute("""
            INSERT INTO flows (flow_id, name, description, metadata)
            VALUES (?, ?, ?, ?)
        """, (flow_id, name, description, json.dumps(metadata or {})))

        self.conn.commit()
        return flow_id

    def create_node(
        self,
        flow_id: str,
        node_type: NodeType,
        name: str,
        description: str,
        parent_id: Optional[str] = None,
        config: Optional[Dict] = None
    ) -> str:
        """Create a new node in the flow"""
        node_id = f"{name}_{datetime.now().strftime('%Y%m%d%H%M%S%f')}"

        self.conn.execute("""
            INSERT INTO nodes (node_id, flow_id, parent_id, node_type, name, description, config)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            node_id,
            flow_id,
            parent_id,
            node_type.value,
            name,
            description,
            json.dumps(config or {})
        ))

        self.conn.commit()
        return node_id

    def create_rule(
        self,
        flow_id: str,
        name: str,
        rule_type: str,
        condition: Dict,
        gate_node_id: Optional[str] = None,
        action: Optional[Dict] = None,
        priority: int = 0,
        metadata: Optional[Dict] = None
    ) -> str:
        """Create a business rule"""
        rule_id = f"rule_{datetime.now().strftime('%Y%m%d%H%M%S%f')}"

        self.conn.execute("""
            INSERT INTO business_rules (
                rule_id, flow_id, gate_node_id, name, rule_type,
                condition, action, priority, metadata
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            rule_id,
            flow_id,
            gate_node_id,
            name,
            rule_type,
            json.dumps(condition),
            json.dumps(action or {}),
            priority,
            json.dumps(metadata or {})
        ))

        self.conn.commit()
        return rule_id

    def build_prd_flow(self) -> str:
        """
        Build the complete PRD Quality Gate flow

        Returns:
            flow_id: The ID of the created flow
        """
        print("🏗️  Building PRD Quality Gate Flow...")

        # Create the flow
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

        print(f"✓ Flow created: {flow_id}")

        # Create root node
        root_id = self.create_node(
            flow_id=flow_id,
            node_type=NodeType.ROOT,
            name="prd_root",
            description="PRD workflow entry point"
        )

        # Stage 1: PRD Creation
        stage1_id = self._create_stage1_creation(flow_id, root_id)

        # Gate 1: Completeness Check
        gate1_id = self._create_gate1_completeness(flow_id, stage1_id)

        # Stage 2: Technical Review
        stage2_id = self._create_stage2_technical_review(flow_id, gate1_id)

        # Gate 2: Technical Feasibility
        gate2_id = self._create_gate2_technical(flow_id, stage2_id)

        # Stage 3: Stakeholder Review
        stage3_id = self._create_stage3_stakeholder_review(flow_id, gate2_id)

        # Gate 3: Business Value Validation
        gate3_id = self._create_gate3_business_value(flow_id, stage3_id)

        # Gate 4: Executive Approval
        gate4_id = self._create_gate4_approval(flow_id, gate3_id)

        # Stage 4: Implementation Planning
        stage4_id = self._create_stage4_implementation_planning(flow_id, gate4_id)

        # Gate 5: Resource Feasibility
        gate5_id = self._create_gate5_resources(flow_id, stage4_id)

        # Stage 5: Implementation (via agentic flow builder)
        stage5_id = self._create_stage5_implementation(flow_id, gate5_id)

        # Stage 6: Evaluation
        stage6_id = self._create_stage6_evaluation(flow_id, stage5_id)

        # Gate 6: Success Criteria Met
        gate6_id = self._create_gate6_success(flow_id, stage6_id)

        # Gate 7: User Acceptance Test
        gate7_id = self._create_gate7_uat(flow_id, gate6_id)

        # Stage 7: Completion & Retrospective
        stage7_id = self._create_stage7_completion(flow_id, gate7_id)

        self.conn.commit()

        print("✓ Flow tree structure created")
        print(f"✓ Total nodes created: {self._count_nodes(flow_id)}")
        print(f"✓ Total rules created: {self._count_rules(flow_id)}")

        return flow_id

    def _create_stage1_creation(self, flow_id: str, parent_id: str) -> str:
        """Stage 1: PRD Creation with agent"""
        node_id = self.create_node(
            flow_id=flow_id,
            node_type=NodeType.AGENT,
            name="stage1_prd_creator",
            description="Create comprehensive PRD from product idea",
            parent_id=parent_id,
            config={
                "agent_type": "prd-creator",
                "goal": """Create a comprehensive Product Requirements Document (PRD) from the provided product idea.

Your tasks:
1. Analyze the product idea and extract key information
2. Research market context and competitors (use WebSearch if needed)
3. Define clear success metrics (minimum 3)
4. Identify target users and personas
5. Outline technical requirements
6. Document dependencies (internal and external)
7. Create realistic timeline estimates
8. Draft complete PRD following the template

Return a structured PRD document with all required sections:
- Problem Statement
- Target Users
- Success Metrics (with specific KPIs)
- Technical Requirements
- Dependencies
- Timeline
- Risks and Mitigations

Store the PRD in working_memory with key 'prd_document'.""",
                "model": "claude-sonnet",
                "tools": ["Read", "Write", "WebSearch", "Grep"],
                "store_episodic": True,
                "episodic_goal_signature": "create_prd",
                "working_memory_output": ["prd_document", "success_metrics", "dependencies"],
                "max_retries": 2,
                "timeout_minutes": 30
            }
        )
        return node_id

    def _create_gate1_completeness(self, flow_id: str, parent_id: str) -> str:
        """Gate 1: Completeness Check (Automated - BRE)"""
        gate_id = self.create_node(
            flow_id=flow_id,
            node_type=NodeType.GATE,
            name="gate1_completeness",
            description="Automated completeness validation",
            parent_id=parent_id,
            config={
                "gate_number": 1,
                "gate_type": "automated",
                "decision_options": ["GO", "RECYCLE"],
                "recycle_target": "stage1_prd_creator",
                "pass_threshold": 100
            }
        )

        # Create business rules for Gate 1
        # Rule 1: Required sections present
        self.create_rule(
            flow_id=flow_id,
            gate_node_id=gate_id,
            name="Required Sections Present",
            rule_type="gate",
            condition={
                "AND": [
                    {"field": "prd_document.problem_statement", "operator": "IS NOT NULL"},
                    {"field": "prd_document.target_users", "operator": "IS NOT NULL"},
                    {"field": "prd_document.success_metrics", "operator": "IS NOT NULL"},
                    {"field": "prd_document.technical_requirements", "operator": "IS NOT NULL"},
                    {"field": "prd_document.dependencies", "operator": "IS NOT NULL"},
                    {"field": "prd_document.timeline", "operator": "IS NOT NULL"}
                ]
            },
            priority=100,
            metadata={"weight": 40, "critical": True}
        )

        # Rule 2: Success metrics count
        self.create_rule(
            flow_id=flow_id,
            gate_node_id=gate_id,
            name="Minimum Success Metrics",
            rule_type="gate",
            condition={
                "field": "prd_document.success_metrics.length",
                "operator": ">=",
                "value": 3
            },
            priority=90,
            metadata={"weight": 30}
        )

        # Rule 3: Problem statement quality
        self.create_rule(
            flow_id=flow_id,
            gate_node_id=gate_id,
            name="Problem Statement Quality",
            rule_type="gate",
            condition={
                "field": "prd_document.problem_statement.length",
                "operator": ">=",
                "value": 100
            },
            priority=80,
            metadata={"weight": 20}
        )

        # Rule 4: Timeline defined
        self.create_rule(
            flow_id=flow_id,
            gate_node_id=gate_id,
            name="Timeline Specified",
            rule_type="gate",
            condition={
                "AND": [
                    {"field": "prd_document.timeline.estimated_weeks", "operator": "IS NOT NULL"},
                    {"field": "prd_document.timeline.estimated_weeks", "operator": ">", "value": 0},
                    {"field": "prd_document.timeline.estimated_weeks", "operator": "<=", "value": 52}
                ]
            },
            priority=70,
            metadata={"weight": 10}
        )

        return gate_id

    def _create_stage2_technical_review(self, flow_id: str, parent_id: str) -> str:
        """Stage 2: Technical Review"""
        node_id = self.create_node(
            flow_id=flow_id,
            node_type=NodeType.AGENT,
            name="stage2_technical_reviewer",
            description="Assess technical feasibility and risks",
            parent_id=parent_id,
            config={
                "agent_type": "technical-reviewer",
                "goal": """Perform comprehensive technical review of the PRD.

Your tasks:
1. Assess technical feasibility of proposed solution
2. Identify potential technical risks and blockers
3. Estimate effort and resource requirements
4. Validate proposed architecture approach
5. Review all dependencies for availability
6. Calculate complexity score

Provide technical review report with:
- Feasibility assessment (HIGH/MEDIUM/LOW/BLOCKER)
- Risk matrix with mitigation strategies
- Effort estimate (in weeks)
- Architecture recommendations
- Dependency analysis
- Complexity score (1-10)

Store in working_memory with key 'technical_review'.""",
                "model": "claude-sonnet",
                "tools": ["Read", "Grep", "Bash"],
                "required_tags": ["code", "architecture", "review"],
                "prefer_agent_type": "task",
                "store_episodic": True,
                "episodic_goal_signature": "technical_review",
                "working_memory_input": ["prd_document"],
                "working_memory_output": ["technical_review", "feasibility_score", "risk_matrix"],
                "timeout_minutes": 20
            }
        )
        return node_id

    def _create_gate2_technical(self, flow_id: str, parent_id: str) -> str:
        """Gate 2: Technical Feasibility (Hybrid - Automated + Human)"""
        gate_id = self.create_node(
            flow_id=flow_id,
            node_type=NodeType.GATE,
            name="gate2_technical_feasibility",
            description="Technical feasibility validation with optional human review",
            parent_id=parent_id,
            config={
                "gate_number": 2,
                "gate_type": "hybrid",
                "decision_options": ["GO", "HOLD", "RECYCLE", "KILL"],
                "recycle_target": "stage1_prd_creator",
                "human_review_sla_hours": 48,
                "reviewers": ["tech_lead", "architect"]
            }
        )

        # Automated rules
        self.create_rule(
            flow_id=flow_id,
            gate_node_id=gate_id,
            name="No Critical Blockers",
            rule_type="gate",
            condition={
                "field": "technical_review.feasibility",
                "operator": "!=",
                "value": "BLOCKER"
            },
            priority=100,
            metadata={"critical": True, "auto_kill_if_fail": True}
        )

        self.create_rule(
            flow_id=flow_id,
            gate_node_id=gate_id,
            name="Reasonable Effort Estimate",
            rule_type="gate",
            condition={
                "field": "technical_review.effort_weeks",
                "operator": "<=",
                "value": 16
            },
            priority=90,
            metadata={"requires_human_if_fail": True}
        )

        self.create_rule(
            flow_id=flow_id,
            gate_node_id=gate_id,
            name="Complexity Within Bounds",
            rule_type="gate",
            condition={
                "field": "technical_review.complexity_score",
                "operator": "<=",
                "value": 8
            },
            priority=80,
            metadata={"requires_human_if_fail": True}
        )

        # Human review trigger rules
        self.create_rule(
            flow_id=flow_id,
            gate_node_id=gate_id,
            name="High Complexity Requires Human Review",
            rule_type="routing",
            condition={
                "OR": [
                    {"field": "technical_review.complexity_score", "operator": ">", "value": 7},
                    {"field": "technical_review.feasibility", "operator": "==", "value": "LOW"},
                    {"field": "prd_document.dependencies.external.length", "operator": ">", "value": 3}
                ]
            },
            action={"route_to": "human_reviewer", "reviewer_role": "tech_lead"},
            priority=95
        )

        return gate_id

    def _create_stage3_stakeholder_review(self, flow_id: str, parent_id: str) -> str:
        """Stage 3: Stakeholder Review Orchestration"""
        node_id = self.create_node(
            flow_id=flow_id,
            node_type=NodeType.CONTROL_FLOW,
            name="stage3_stakeholder_orchestrator",
            description="Coordinate multi-stakeholder review process",
            parent_id=parent_id,
            config={
                "pattern": WorkflowPattern.ORCHESTRATOR_WORKERS.value,
                "orchestrator_agent": "stakeholder-orchestrator",
                "worker_agents": ["feedback_collector", "conflict_resolver", "prd_updater"],
                "goal": """Orchestrate stakeholder review process.

Tasks:
1. Identify required stakeholders based on PRD scope
2. Distribute PRD to all stakeholders
3. Collect feedback asynchronously
4. Identify conflicts or concerns
5. Facilitate alignment discussions
6. Update PRD with incorporated feedback

Return consolidated feedback and updated PRD.""",
                "model": "claude-haiku",
                "store_episodic": False,
                "working_memory_input": ["prd_document", "technical_review"],
                "working_memory_output": ["stakeholder_feedback", "prd_document_updated"],
                "timeout_minutes": 60,
                "parallel_workers": True
            }
        )
        return node_id

    def _create_gate3_business_value(self, flow_id: str, parent_id: str) -> str:
        """Gate 3: Business Value Validation (Hybrid)"""
        gate_id = self.create_node(
            flow_id=flow_id,
            node_type=NodeType.GATE,
            name="gate3_business_value",
            description="Business value and strategic alignment validation",
            parent_id=parent_id,
            config={
                "gate_number": 3,
                "gate_type": "hybrid",
                "decision_options": ["GO", "HOLD", "PIVOT", "KILL"],
                "requires_human_review": True,
                "reviewers": ["product_owner", "business_stakeholders"]
            }
        )

        # Automated checks
        self.create_rule(
            flow_id=flow_id,
            gate_node_id=gate_id,
            name="Positive ROI Projection",
            rule_type="gate",
            condition={
                "field": "prd_document.roi_projection",
                "operator": ">",
                "value": 0
            },
            priority=100
        )

        self.create_rule(
            flow_id=flow_id,
            gate_node_id=gate_id,
            name="Strategic Alignment Score",
            rule_type="gate",
            condition={
                "field": "prd_document.strategic_alignment_score",
                "operator": ">=",
                "value": 7
            },
            priority=90,
            metadata={"max_score": 10}
        )

        self.create_rule(
            flow_id=flow_id,
            gate_node_id=gate_id,
            name="Market Size Sufficient",
            rule_type="gate",
            condition={
                "field": "prd_document.target_market_size",
                "operator": ">",
                "value": 1000
            },
            priority=80
        )

        return gate_id

    def _create_gate4_approval(self, flow_id: str, parent_id: str) -> str:
        """Gate 4: Executive Approval (Human Decision)"""
        gate_id = self.create_node(
            flow_id=flow_id,
            node_type=NodeType.GATE,
            name="gate4_executive_approval",
            description="Executive/leadership approval gate",
            parent_id=parent_id,
            config={
                "gate_number": 4,
                "gate_type": "human",
                "decision_options": ["APPROVE", "DEFER", "REJECT"],
                "decision_maker": "product_leadership",
                "sla_hours": 48,
                "escalation_path": "ceo",
                "information_package": [
                    "prd_document",
                    "technical_review",
                    "stakeholder_feedback",
                    "roi_projection",
                    "risk_assessment"
                ]
            }
        )

        # No automated rules - purely human decision
        # But we can add validation that all required info is present
        self.create_rule(
            flow_id=flow_id,
            gate_node_id=gate_id,
            name="Information Package Complete",
            rule_type="validation",
            condition={
                "AND": [
                    {"field": "prd_document", "operator": "IS NOT NULL"},
                    {"field": "technical_review", "operator": "IS NOT NULL"},
                    {"field": "stakeholder_feedback", "operator": "IS NOT NULL"},
                    {"field": "roi_projection", "operator": "IS NOT NULL"}
                ]
            },
            priority=100,
            metadata={"blocks_human_review_if_fail": True}
        )

        return gate_id

    def _create_stage4_implementation_planning(self, flow_id: str, parent_id: str) -> str:
        """Stage 4: Implementation Planning"""
        node_id = self.create_node(
            flow_id=flow_id,
            node_type=NodeType.AGENT,
            name="stage4_implementation_planner",
            description="Convert PRD into actionable implementation plan",
            parent_id=parent_id,
            config={
                "agent_type": "implementation-planner",
                "goal": """Create detailed implementation plan from approved PRD.

Tasks:
1. Break down PRD into epics and user stories
2. Estimate timelines for each component
3. Assign resource requirements
4. Define key milestones
5. Map dependencies between tasks
6. Create project plan with Gantt timeline

Return comprehensive implementation plan with:
- Epic/story breakdown
- Timeline with milestones
- Resource allocation
- Dependency graph
- Risk mitigation plans

Store in working_memory with key 'implementation_plan'.""",
                "model": "claude-sonnet",
                "tools": ["Read", "Write"],
                "store_episodic": True,
                "episodic_goal_signature": "implementation_planning",
                "working_memory_input": ["prd_document", "technical_review"],
                "working_memory_output": ["implementation_plan", "resource_requirements"],
                "timeout_minutes": 30
            }
        )
        return node_id

    def _create_gate5_resources(self, flow_id: str, parent_id: str) -> str:
        """Gate 5: Resource Feasibility (Automated - BRE)"""
        gate_id = self.create_node(
            flow_id=flow_id,
            node_type=NodeType.GATE,
            name="gate5_resource_feasibility",
            description="Validate resource availability and feasibility",
            parent_id=parent_id,
            config={
                "gate_number": 5,
                "gate_type": "automated",
                "decision_options": ["GO", "QUEUE"],
                "queue_reason_field": "blocking_resource"
            }
        )

        # Resource availability rules
        self.create_rule(
            flow_id=flow_id,
            gate_node_id=gate_id,
            name="Team Capacity Available",
            rule_type="gate",
            condition={
                "field": "resource_requirements.team_capacity_available",
                "operator": "==",
                "value": True
            },
            priority=100,
            metadata={"critical": True}
        )

        self.create_rule(
            flow_id=flow_id,
            gate_node_id=gate_id,
            name="Budget Approved",
            rule_type="gate",
            condition={
                "OR": [
                    {"field": "resource_requirements.budget_required", "operator": "==", "value": False},
                    {
                        "AND": [
                            {"field": "resource_requirements.budget_required", "operator": "==", "value": True},
                            {"field": "resource_requirements.budget_approved", "operator": "==", "value": True}
                        ]
                    }
                ]
            },
            priority=95
        )

        self.create_rule(
            flow_id=flow_id,
            gate_node_id=gate_id,
            name="Timeline Realistic",
            rule_type="gate",
            condition={
                "field": "implementation_plan.timeline_feasible",
                "operator": "==",
                "value": True
            },
            priority=90
        )

        self.create_rule(
            flow_id=flow_id,
            gate_node_id=gate_id,
            name="No Blocking Dependencies",
            rule_type="gate",
            condition={
                "field": "implementation_plan.blocking_dependencies.length",
                "operator": "==",
                "value": 0
            },
            priority=85
        )

        return gate_id

    def _create_stage5_implementation(self, flow_id: str, parent_id: str) -> str:
        """Stage 5: Implementation (via Task Flow Generator)"""
        node_id = self.create_node(
            flow_id=flow_id,
            node_type=NodeType.AGENT,
            name="stage5_task_flow_generator",
            description="Generate and execute custom implementation flow",
            parent_id=parent_id,
            config={
                "agent_type": "task-flow-generator",
                "goal": """Generate custom agentic flow for implementation.

Tasks:
1. Use the agentic-flow-builder skill to create implementation flow
2. Configure hierarchical task decomposition
3. Set up quality checkpoints
4. Configure defect tracking
5. Execute the generated flow
6. Monitor progress and handle issues

This agent will invoke the agentic-flow-builder skill to create
a tailored implementation workflow based on the implementation plan.

Store execution results in working_memory with key 'implementation_results'.""",
                "model": "claude-sonnet",
                "tools": ["Read", "Write", "Skill", "Task"],
                "skill_to_invoke": "agentic-flow-builder:flow-builder",
                "store_episodic": True,
                "episodic_goal_signature": "implementation_execution",
                "working_memory_input": ["implementation_plan", "prd_document"],
                "working_memory_output": ["implementation_results", "defects"],
                "timeout_minutes": 480  # 8 hours for implementation
            }
        )
        return node_id

    def _create_stage6_evaluation(self, flow_id: str, parent_id: str) -> str:
        """Stage 6: Evaluation"""
        node_id = self.create_node(
            flow_id=flow_id,
            node_type=NodeType.AGENT,
            name="stage6_prd_evaluator",
            description="Measure outcomes against success criteria",
            parent_id=parent_id,
            config={
                "agent_type": "prd-evaluator",
                "goal": """Evaluate implementation against PRD success criteria.

Tasks:
1. Collect all defined success metrics
2. Measure actual performance against targets
3. Analyze user feedback
4. Compare to initial projections
5. Calculate success score

Return evaluation report with:
- Each success metric with actual vs target
- Overall success score
- User feedback summary
- Performance analysis
- Recommendations

Store in working_memory with key 'evaluation_results'.""",
                "model": "claude-haiku",
                "tools": ["Read", "Grep", "Bash"],
                "store_episodic": True,
                "episodic_goal_signature": "prd_evaluation",
                "working_memory_input": ["prd_document", "implementation_results"],
                "working_memory_output": ["evaluation_results", "success_score"],
                "timeout_minutes": 20
            }
        )
        return node_id

    def _create_gate6_success(self, flow_id: str, parent_id: str) -> str:
        """Gate 6: Success Criteria Met (Hybrid)"""
        gate_id = self.create_node(
            flow_id=flow_id,
            node_type=NodeType.GATE,
            name="gate6_success_criteria",
            description="Validate success criteria achievement",
            parent_id=parent_id,
            config={
                "gate_number": 6,
                "gate_type": "hybrid",
                "decision_options": ["PASS", "ITERATE"],
                "iterate_target": "stage5_task_flow_generator"
            }
        )

        # Automated success checks
        self.create_rule(
            flow_id=flow_id,
            gate_node_id=gate_id,
            name="Success Metrics Achieved",
            rule_type="gate",
            condition={
                "field": "evaluation_results.success_score",
                "operator": ">=",
                "value": 80
            },
            priority=100,
            metadata={"max_score": 100}
        )

        self.create_rule(
            flow_id=flow_id,
            gate_node_id=gate_id,
            name="No Critical Defects",
            rule_type="gate",
            condition={
                "field": "implementation_results.critical_defects_count",
                "operator": "==",
                "value": 0
            },
            priority=95
        )

        self.create_rule(
            flow_id=flow_id,
            gate_node_id=gate_id,
            name="Performance Benchmarks Met",
            rule_type="gate",
            condition={
                "field": "evaluation_results.performance_score",
                "operator": ">=",
                "value": 75
            },
            priority=90
        )

        return gate_id

    def _create_gate7_uat(self, flow_id: str, parent_id: str) -> str:
        """Gate 7: User Acceptance Test (Human Decision)"""
        gate_id = self.create_node(
            flow_id=flow_id,
            node_type=NodeType.GATE,
            name="gate7_uat",
            description="User acceptance testing and final approval",
            parent_id=parent_id,
            config={
                "gate_number": 7,
                "gate_type": "human",
                "decision_options": ["RELEASE", "FIX_ISSUES"],
                "decision_maker": "product_owner",
                "required_approvers": ["product_owner", "key_stakeholders"],
                "sla_hours": 48,
                "uat_scenarios_required": True
            }
        )

        # Validation that UAT is ready
        self.create_rule(
            flow_id=flow_id,
            gate_node_id=gate_id,
            name="UAT Scenarios Completed",
            rule_type="validation",
            condition={
                "AND": [
                    {"field": "uat_results.scenarios_executed", "operator": ">", "value": 0},
                    {"field": "uat_results.pass_rate", "operator": ">=", "value": 95}
                ]
            },
            priority=100
        )

        return gate_id

    def _create_stage7_completion(self, flow_id: str, parent_id: str) -> str:
        """Stage 7: Completion & Retrospective"""
        node_id = self.create_node(
            flow_id=flow_id,
            node_type=NodeType.AGENT,
            name="stage7_retrospective",
            description="Capture learnings and complete PRD",
            parent_id=parent_id,
            config={
                "agent_type": "retrospective",
                "goal": """Conduct retrospective and complete PRD lifecycle.

Tasks:
1. Document lessons learned
2. Identify process improvements
3. Store episodic memory for future PRDs
4. Archive PRD with final status
5. Generate completion report

Return retrospective report and mark PRD as COMPLETED.""",
                "model": "claude-haiku",
                "tools": ["Read", "Write"],
                "store_episodic": True,
                "episodic_goal_signature": "prd_completion",
                "working_memory_input": ["prd_document", "evaluation_results", "implementation_results"],
                "working_memory_output": ["retrospective_report"],
                "timeout_minutes": 10
            }
        )
        return node_id

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
        nodes = self.conn.execute("""
            SELECT * FROM nodes WHERE flow_id = ? ORDER BY created_at
        """, (flow_id,)).fetchall()

        diagram = "PRD Quality Gate Flow\n"
        diagram += "=" * 60 + "\n\n"

        for node in nodes:
            indent = "  " * self._get_node_depth(node['node_id'])
            node_type = node['node_type'].upper()
            diagram += f"{indent}[{node_type}] {node['name']}\n"
            diagram += f"{indent}    {node['description']}\n"

            if node['node_type'] == 'gate':
                rules_count = self.conn.execute("""
                    SELECT COUNT(*) as count FROM business_rules
                    WHERE gate_node_id = ?
                """, (node['node_id'],)).fetchone()['count']
                diagram += f"{indent}    Rules: {rules_count}\n"

            diagram += "\n"

        return diagram

    def _get_node_depth(self, node_id: str, depth: int = 0) -> int:
        """Get depth of node in tree"""
        node = self.conn.execute(
            "SELECT parent_id FROM nodes WHERE node_id = ?",
            (node_id,)
        ).fetchone()

        if not node or not node['parent_id']:
            return depth

        return self._get_node_depth(node['parent_id'], depth + 1)

    def close(self):
        """Close database connection"""
        self.conn.close()


if __name__ == "__main__":
    # Build the PRD flow
    builder = PRDFlowBuilder("prd_flows.db")

    try:
        flow_id = builder.build_prd_flow()

        print("\n" + "=" * 60)
        print("✅ PRD Quality Gate Flow Built Successfully!")
        print("=" * 60)
        print(f"\nFlow ID: {flow_id}")
        print(f"Database: prd_flows.db")

        # Export diagram
        diagram = builder.export_flow_diagram(flow_id)
        print("\n" + diagram)

        # Save diagram to file
        with open("prd_flow_diagram.txt", "w") as f:
            f.write(diagram)

        print("📄 Flow diagram saved to: prd_flow_diagram.txt")
        print("\n✨ Next steps:")
        print("  1. Review the flow structure in prd_flow_diagram.txt")
        print("  2. Customize business rules as needed")
        print("  3. Run prd_execute.py to execute the flow")

    finally:
        builder.close()
