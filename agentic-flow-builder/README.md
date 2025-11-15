# Agentic Flow Builder

A production-grade plugin for building dynamic agentic workflows using ReAcTree hierarchical decomposition and Anthropic's proven workflow patterns.

## Overview

This plugin enables you to create sophisticated multi-agent workflows with:

- **ReAcTree** - Hierarchical agent tree decomposition for long-horizon task planning
- **Business Rules Engine** - Deterministic decision-making at gates (no AI guesswork)
- **Dynamic Agent Assignment** - Automatically selects best agent for each task
- **Dual Memory System** - Episodic + working memory for context management
- **Full Audit Trails** - Complete traceability for compliance
- **5 Workflow Patterns** - Proven patterns from Anthropic's engineering team

## Key Features

### 1. Deterministic Gates via BRE

Stop relying on inconsistent AI decisions. Use business rules for critical decision points:

```python
{
    "name": "Credit Approval",
    "condition": {
        "AND": [
            {"field": "credit_score", "operator": ">=", "value": 650},
            {"field": "debt_to_income", "operator": "<=", "value": 0.43}
        ]
    }
}
```

**Why this matters:**
- Same input = same output (always)
- Full audit trail of why decisions were made
- Meets regulatory compliance requirements
- No hallucinations or temperature variance

### 2. Dynamic Agent Assignment

Agents are automatically selected based on task requirements:

- Semantic matching with agent capabilities
- Performance history tracking
- Hot-reload of new agents
- Supports Claude models, Task agents, and external services

### 3. Hierarchical Task Decomposition

Break complex goals into manageable subgoals using a dynamic tree structure:

```
Root
├── Gate: Verify Prerequisites
│   └── Agent: Validation
├── Control Flow: Main Process
│   ├── Agent: Orchestrator
│   ├── Agent: Worker 1
│   └── Agent: Worker 2
└── Control Flow: Post-Process
    └── Agent: Quality Check
```

### 4. Five Proven Workflow Patterns

1. **Prompt Chaining** - Sequential processing with intermediate steps
2. **Routing** - Classify and route to specialized handlers
3. **Parallelization** - Concurrent execution for speed
4. **Orchestrator-Workers** - Dynamic task breakdown and delegation
5. **Evaluator-Optimizer** - Iterative refinement loops

### 5. Comprehensive Audit System

Every decision, every agent selection, every rule evaluation is logged:

```sql
SELECT * FROM gate_evaluations WHERE execution_id = ?
-- See exact why gates passed/failed

SELECT * FROM agent_assignments WHERE execution_id = ?
-- See which agents were used and their performance

SELECT * FROM audit_log WHERE execution_id = ?
-- Complete event timeline
```

## Installation

```bash
/plugin install agentic-flow-builder
```

## Quick Start

```python
from database import FlowDatabase, NodeType
from business_rules_engine import BusinessRulesEngine
from flow_orchestrator import FlowOrchestrator
from agent_registry import AgentRegistry
import asyncio

# Initialize
db = FlowDatabase("my_flow.db")
bre = BusinessRulesEngine(db)
registry = AgentRegistry(db.db_path)
orchestrator = FlowOrchestrator(db, bre, registry)

# Create flow
flow_id = db.create_flow(
    name="User Validation Flow",
    description="Validate user with age gate"
)

# Add gate with business rule
root_id = db.create_node(flow_id, NodeType.ROOT, "root")
gate_id = db.create_node(flow_id, NodeType.GATE, "age_gate", parent_id=root_id)

db.create_rule(
    flow_id=flow_id,
    name="Minimum Age",
    rule_type="gate",
    condition={"field": "user.age", "operator": ">=", "value": 18}
)

# Execute
execution_id = await orchestrator.execute_flow(
    flow_id,
    initial_context={"user": {"age": 25}}
)

# Get audit trail
audit = db.get_execution_audit_trail(execution_id)
print(audit)
```

## Components

### Scripts

- `database.py` - SQLite schema and data access layer
- `business_rules_engine.py` - Production-grade BRE for gates
- `flow_orchestrator.py` - Execution engine with workflow patterns
- `agent_registry.py` - Dynamic agent discovery and assignment

### Skills

- `flow-builder/SKILL.md` - Comprehensive guide for building agentic flows

### References

- `complete_example.py` - Full customer onboarding example
- `rule_examples.md` - Business rule examples
- `flow_patterns.md` - Common workflow patterns

## Architecture

### Based on Research

**ReAcTree** (arXiv:2511.02424)
- Hierarchical LLM agent trees with control flow
- Dual memory system (episodic + working)
- Achieved 61% success rate vs 31% baseline

**Anthropic's Building Effective Agents**
- Five proven workflow patterns
- Start simple, add complexity only when needed
- Workflows vs Agents decision framework

### Production-Grade Design

✓ **SQLite persistence** - No external dependencies
✓ **Type-safe** - Full type hints throughout
✓ **Async execution** - Non-blocking operations
✓ **Comprehensive testing** - Unit tests for BRE, integration tests for flows
✓ **Audit compliance** - Immutable audit logs
✓ **Hot-reload** - Add agents without restart

## Use Cases

### Financial Services
- KYC/AML compliance workflows
- Credit application processing
- Fraud detection pipelines
- Regulatory reporting

### Healthcare
- Patient intake workflows
- Clinical decision support
- Insurance claim processing
- Compliance validation

### Enterprise
- Multi-step approval workflows
- Document processing pipelines
- Customer onboarding
- Quality assurance processes

## Why Business Rules for Gates?

**AI Decision-Making Problems:**
- Inconsistent (temperature variance)
- Unexplainable (black box)
- Non-compliant (can't audit)
- Expensive (LLM call per decision)

**BRE Solution:**
- Deterministic (always consistent)
- Explainable (clear audit trail)
- Compliant (meets regulations)
- Free (no LLM calls)

**When to use BRE vs AI:**
- **BRE**: Binary decisions with clear criteria (age checks, credit scores, compliance rules)
- **AI**: Complex reasoning, subjective judgment, natural language understanding

## Performance

Typical execution times (example flow with 10 nodes):
- Flow setup: <10ms
- Gate evaluation: <1ms (BRE)
- Agent execution: Variable (depends on agent)
- Audit logging: <5ms

Database size:
- Base schema: ~100KB
- Per execution: ~50-200KB (depending on context size)
- Per episodic memory: ~10-50KB

## Requirements

- Python 3.8+
- SQLite 3 (included with Python)
- asyncio support

Optional:
- Claude API access (for AI agents)
- Claude Code (for task agents)

## License

MIT License - See LICENSE.txt

## Contributing

Contributions welcome! Areas of interest:
- Additional workflow patterns
- Agent integrations
- Performance optimizations
- Example flows for different industries

## References

- [ReAcTree Paper](https://arxiv.org/abs/2511.02424)
- [Anthropic: Building Effective Agents](https://www.anthropic.com/engineering/building-effective-agents)
- [Claude Code Documentation](https://code.claude.com/docs)

## Support

For issues or questions:
- Review the complete example in `references/complete_example.py`
- Check the skill documentation in `skills/flow-builder/SKILL.md`
- Open an issue in the repository
