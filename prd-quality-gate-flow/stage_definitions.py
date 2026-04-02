"""
Stage definitions for the PRD Quality Gate flow.

Pure data module — 7 stage definitions as Python dicts, extracted verbatim
from PRDFlowBuilder._create_stage1_creation through _create_stage7_completion.

No internal imports. Validated at load time.
"""

# Required fields for each stage dict — validated at module load
REQUIRED_STAGE_FIELDS = {"name", "description", "node_type", "config"}

# Required fields within each stage's config dict
REQUIRED_CONFIG_FIELDS = {"agent_type", "goal", "model"}


STAGE_DEFINITIONS = [
    # Stage 1: PRD Creation
    {
        "name": "stage1_prd_creator",
        "description": "Create comprehensive PRD from product idea",
        "node_type": "agent",
        "config": {
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
    },

    # Stage 2: Technical Review
    {
        "name": "stage2_technical_reviewer",
        "description": "Assess technical feasibility and risks",
        "node_type": "agent",
        "config": {
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
    },

    # Stage 3: Stakeholder Review Orchestration
    {
        "name": "stage3_stakeholder_orchestrator",
        "description": "Coordinate multi-stakeholder review process",
        "node_type": "control_flow",
        "config": {
            "pattern": "orchestrator_workers",
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
            "agent_type": "stakeholder-orchestrator",
            "store_episodic": False,
            "working_memory_input": ["prd_document", "technical_review"],
            "working_memory_output": ["stakeholder_feedback", "prd_document_updated"],
            "timeout_minutes": 60,
            "parallel_workers": True
        }
    },

    # Stage 4: Implementation Planning
    {
        "name": "stage4_implementation_planner",
        "description": "Convert PRD into actionable implementation plan",
        "node_type": "agent",
        "config": {
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
    },

    # Stage 5: Implementation (via Task Flow Generator)
    {
        "name": "stage5_task_flow_generator",
        "description": "Generate and execute custom implementation flow",
        "node_type": "agent",
        "config": {
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
            "timeout_minutes": 480
        }
    },

    # Stage 6: Evaluation
    {
        "name": "stage6_prd_evaluator",
        "description": "Measure outcomes against success criteria",
        "node_type": "agent",
        "config": {
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
    },

    # Stage 7: Completion & Retrospective
    {
        "name": "stage7_retrospective",
        "description": "Capture learnings and complete PRD",
        "node_type": "agent",
        "config": {
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
    },
]


# --- Load-time validation ---
for _idx, _stage in enumerate(STAGE_DEFINITIONS):
    _missing = REQUIRED_STAGE_FIELDS - set(_stage.keys())
    if _missing:
        raise KeyError(
            f"Stage {_idx} ({_stage.get('name', 'UNNAMED')}): "
            f"missing required fields: {_missing}"
        )
    _config = _stage["config"]
    _missing_cfg = REQUIRED_CONFIG_FIELDS - set(_config.keys())
    if _missing_cfg:
        raise KeyError(
            f"Stage {_idx} ({_stage['name']}): "
            f"config missing required fields: {_missing_cfg}"
        )
