"""
Gate definitions and business rules for the PRD Quality Gate flow.

Pure data module — 7 gate definitions with 20 total business rules,
extracted verbatim from PRDFlowBuilder._create_gate1_completeness
through _create_gate7_uat.

Rule distribution per gate: [4, 4, 3, 1, 4, 3, 1]

No internal imports. Validated at load time.
"""

# Required fields for each gate dict
REQUIRED_GATE_FIELDS = {"name", "description", "gate_config", "rules"}

# Required fields for each rule dict within a gate
REQUIRED_RULE_FIELDS = {"name", "rule_type", "condition", "priority"}


GATE_DEFINITIONS = [
    # Gate 1: Completeness Check (Automated - BRE)
    {
        "name": "gate1_completeness",
        "description": "Automated completeness validation",
        "gate_config": {
            "gate_number": 1,
            "gate_type": "automated",
            "decision_options": ["GO", "RECYCLE"],
            "recycle_target": "stage1_prd_creator",
            "pass_threshold": 100
        },
        "rules": [
            {
                "name": "Required Sections Present",
                "rule_type": "gate",
                "condition": {
                    "AND": [
                        {"field": "prd_document.problem_statement", "operator": "IS NOT NULL"},
                        {"field": "prd_document.target_users", "operator": "IS NOT NULL"},
                        {"field": "prd_document.success_metrics", "operator": "IS NOT NULL"},
                        {"field": "prd_document.technical_requirements", "operator": "IS NOT NULL"},
                        {"field": "prd_document.dependencies", "operator": "IS NOT NULL"},
                        {"field": "prd_document.timeline", "operator": "IS NOT NULL"}
                    ]
                },
                "action": {},
                "priority": 100,
                "metadata": {"weight": 40, "critical": True}
            },
            {
                "name": "Minimum Success Metrics",
                "rule_type": "gate",
                "condition": {
                    "field": "prd_document.success_metrics.length",
                    "operator": ">=",
                    "value": 3
                },
                "action": {},
                "priority": 90,
                "metadata": {"weight": 30}
            },
            {
                "name": "Problem Statement Quality",
                "rule_type": "gate",
                "condition": {
                    "field": "prd_document.problem_statement.length",
                    "operator": ">=",
                    "value": 100
                },
                "action": {},
                "priority": 80,
                "metadata": {"weight": 20}
            },
            {
                "name": "Timeline Specified",
                "rule_type": "gate",
                "condition": {
                    "AND": [
                        {"field": "prd_document.timeline.estimated_weeks", "operator": "IS NOT NULL"},
                        {"field": "prd_document.timeline.estimated_weeks", "operator": ">", "value": 0},
                        {"field": "prd_document.timeline.estimated_weeks", "operator": "<=", "value": 52}
                    ]
                },
                "action": {},
                "priority": 70,
                "metadata": {"weight": 10}
            },
        ]
    },

    # Gate 2: Technical Feasibility (Hybrid - Automated + Human)
    {
        "name": "gate2_technical_feasibility",
        "description": "Technical feasibility validation with optional human review",
        "gate_config": {
            "gate_number": 2,
            "gate_type": "hybrid",
            "decision_options": ["GO", "HOLD", "RECYCLE", "KILL"],
            "recycle_target": "stage1_prd_creator",
            "human_review_sla_hours": 48,
            "reviewers": ["tech_lead", "architect"]
        },
        "rules": [
            {
                "name": "No Critical Blockers",
                "rule_type": "gate",
                "condition": {
                    "field": "technical_review.feasibility",
                    "operator": "!=",
                    "value": "BLOCKER"
                },
                "action": {},
                "priority": 100,
                "metadata": {"critical": True, "auto_kill_if_fail": True}
            },
            {
                "name": "Reasonable Effort Estimate",
                "rule_type": "gate",
                "condition": {
                    "field": "technical_review.effort_weeks",
                    "operator": "<=",
                    "value": 16
                },
                "action": {},
                "priority": 90,
                "metadata": {"requires_human_if_fail": True}
            },
            {
                "name": "Complexity Within Bounds",
                "rule_type": "gate",
                "condition": {
                    "field": "technical_review.complexity_score",
                    "operator": "<=",
                    "value": 8
                },
                "action": {},
                "priority": 80,
                "metadata": {"requires_human_if_fail": True}
            },
            {
                "name": "High Complexity Requires Human Review",
                "rule_type": "routing",
                "condition": {
                    "OR": [
                        {"field": "technical_review.complexity_score", "operator": ">", "value": 7},
                        {"field": "technical_review.feasibility", "operator": "==", "value": "LOW"},
                        {"field": "prd_document.dependencies.external.length", "operator": ">", "value": 3}
                    ]
                },
                "action": {"route_to": "human_reviewer", "reviewer_role": "tech_lead"},
                "priority": 95,
                "metadata": {}
            },
        ]
    },

    # Gate 3: Business Value Validation (Hybrid)
    {
        "name": "gate3_business_value",
        "description": "Business value and strategic alignment validation",
        "gate_config": {
            "gate_number": 3,
            "gate_type": "hybrid",
            "decision_options": ["GO", "HOLD", "PIVOT", "KILL"],
            "requires_human_review": True,
            "reviewers": ["product_owner", "business_stakeholders"]
        },
        "rules": [
            {
                "name": "Positive ROI Projection",
                "rule_type": "gate",
                "condition": {
                    "field": "prd_document.roi_projection",
                    "operator": ">",
                    "value": 0
                },
                "action": {},
                "priority": 100,
                "metadata": {}
            },
            {
                "name": "Strategic Alignment Score",
                "rule_type": "gate",
                "condition": {
                    "field": "prd_document.strategic_alignment_score",
                    "operator": ">=",
                    "value": 7
                },
                "action": {},
                "priority": 90,
                "metadata": {"max_score": 10}
            },
            {
                "name": "Market Size Sufficient",
                "rule_type": "gate",
                "condition": {
                    "field": "prd_document.target_market_size",
                    "operator": ">",
                    "value": 1000
                },
                "action": {},
                "priority": 80,
                "metadata": {}
            },
        ]
    },

    # Gate 4: Executive Approval (Human Decision)
    {
        "name": "gate4_executive_approval",
        "description": "Executive/leadership approval gate",
        "gate_config": {
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
        },
        "rules": [
            {
                "name": "Information Package Complete",
                "rule_type": "validation",
                "condition": {
                    "AND": [
                        {"field": "prd_document", "operator": "IS NOT NULL"},
                        {"field": "technical_review", "operator": "IS NOT NULL"},
                        {"field": "stakeholder_feedback", "operator": "IS NOT NULL"},
                        {"field": "roi_projection", "operator": "IS NOT NULL"}
                    ]
                },
                "action": {},
                "priority": 100,
                "metadata": {"blocks_human_review_if_fail": True}
            },
        ]
    },

    # Gate 5: Resource Feasibility (Automated - BRE)
    {
        "name": "gate5_resource_feasibility",
        "description": "Validate resource availability and feasibility",
        "gate_config": {
            "gate_number": 5,
            "gate_type": "automated",
            "decision_options": ["GO", "QUEUE"],
            "queue_reason_field": "blocking_resource"
        },
        "rules": [
            {
                "name": "Team Capacity Available",
                "rule_type": "gate",
                "condition": {
                    "field": "resource_requirements.team_capacity_available",
                    "operator": "==",
                    "value": True
                },
                "action": {},
                "priority": 100,
                "metadata": {"critical": True}
            },
            {
                "name": "Budget Approved",
                "rule_type": "gate",
                "condition": {
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
                "action": {},
                "priority": 95,
                "metadata": {}
            },
            {
                "name": "Timeline Realistic",
                "rule_type": "gate",
                "condition": {
                    "field": "implementation_plan.timeline_feasible",
                    "operator": "==",
                    "value": True
                },
                "action": {},
                "priority": 90,
                "metadata": {}
            },
            {
                "name": "No Blocking Dependencies",
                "rule_type": "gate",
                "condition": {
                    "field": "implementation_plan.blocking_dependencies.length",
                    "operator": "==",
                    "value": 0
                },
                "action": {},
                "priority": 85,
                "metadata": {}
            },
        ]
    },

    # Gate 6: Success Criteria Met (Hybrid)
    {
        "name": "gate6_success_criteria",
        "description": "Validate success criteria achievement",
        "gate_config": {
            "gate_number": 6,
            "gate_type": "hybrid",
            "decision_options": ["PASS", "ITERATE"],
            "iterate_target": "stage5_task_flow_generator"
        },
        "rules": [
            {
                "name": "Success Metrics Achieved",
                "rule_type": "gate",
                "condition": {
                    "field": "evaluation_results.success_score",
                    "operator": ">=",
                    "value": 80
                },
                "action": {},
                "priority": 100,
                "metadata": {"max_score": 100}
            },
            {
                "name": "No Critical Defects",
                "rule_type": "gate",
                "condition": {
                    "field": "implementation_results.critical_defects_count",
                    "operator": "==",
                    "value": 0
                },
                "action": {},
                "priority": 95,
                "metadata": {}
            },
            {
                "name": "Performance Benchmarks Met",
                "rule_type": "gate",
                "condition": {
                    "field": "evaluation_results.performance_score",
                    "operator": ">=",
                    "value": 75
                },
                "action": {},
                "priority": 90,
                "metadata": {}
            },
        ]
    },

    # Gate 7: User Acceptance Test (Human Decision)
    {
        "name": "gate7_uat",
        "description": "User acceptance testing and final approval",
        "gate_config": {
            "gate_number": 7,
            "gate_type": "human",
            "decision_options": ["RELEASE", "FIX_ISSUES"],
            "decision_maker": "product_owner",
            "required_approvers": ["product_owner", "key_stakeholders"],
            "sla_hours": 48,
            "uat_scenarios_required": True
        },
        "rules": [
            {
                "name": "UAT Scenarios Completed",
                "rule_type": "validation",
                "condition": {
                    "AND": [
                        {"field": "uat_results.scenarios_executed", "operator": ">", "value": 0},
                        {"field": "uat_results.pass_rate", "operator": ">=", "value": 95}
                    ]
                },
                "action": {},
                "priority": 100,
                "metadata": {}
            },
        ]
    },
]


# --- Load-time validation ---
for _idx, _gate in enumerate(GATE_DEFINITIONS):
    _missing = REQUIRED_GATE_FIELDS - set(_gate.keys())
    if _missing:
        raise KeyError(
            f"Gate {_idx} ({_gate.get('name', 'UNNAMED')}): "
            f"missing required fields: {_missing}"
        )
    for _ridx, _rule in enumerate(_gate["rules"]):
        _missing_r = REQUIRED_RULE_FIELDS - set(_rule.keys())
        if _missing_r:
            raise KeyError(
                f"Gate {_idx} ({_gate['name']}), Rule {_ridx} "
                f"({_rule.get('name', 'UNNAMED')}): "
                f"missing required fields: {_missing_r}"
            )
