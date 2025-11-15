---
name: agentic-flow-builder
description: Guide for building dynamic agentic flows using ReAcTree hierarchical decomposition and Anthropic's workflow patterns. This skill should be used when users want to create complex multi-step agent workflows with deterministic gates, business rules, and comprehensive audit trails.
license: MIT License - See repository LICENSE file
---

# Agentic Flow Builder

This skill provides comprehensive guidance for building production-grade agentic flows that combine:
- **ReAcTree** hierarchical agent tree decomposition for long-horizon task planning
- **Anthropic's workflow patterns** for effective agent design
- **Business Rules Engine (BRE)** for deterministic decision-making at gates
- **Dual memory system** (episodic + working) for context management
- **SQLite persistence** with full audit trails

## Core Philosophy

**Start simple, add complexity only when justified.** Many problems can be solved with a single optimized LLM call. Only use agentic flows when the task requires:
- Multi-step decomposition
- Dynamic routing based on conditions
- Iterative refinement
- Complex orchestration across multiple specialized agents

## When to Use Agentic Flows

Create an agentic flow when you need:

1. **Long-horizon task planning** - Complex goals requiring hierarchical decomposition
2. **Deterministic gating** - Business rule-based decisions (not AI guesswork)
3. **Workflow orchestration** - Coordinating multiple specialized agents
4. **Audit requirements** - Complete traceability of decisions and outcomes
5. **Memory across executions** - Learning from past successful/failed attempts

## Architecture Components

### 0. Dynamic Agent Assignment

The system automatically selects the best agent for each task based on:
- **Task description** - Semantic matching with agent capabilities
- **Required tags** - Specific skills needed (e.g., "code", "security", "data")
- **Agent type preference** - General Claude models, Task agents, or External services
- **Performance history** - Learns from past successes/failures

**Agents are discovered dynamically:**
- Claude models (Sonnet, Opus, Haiku)
- Claude Code Task agents (auto-discovered)
- Custom plugin agents
- External API services

**Hot-reload support:** New agents are automatically available without restarting.

**Configuration example:**
```python
agent_node_config = {
    "goal": "Review code for security vulnerabilities",
    "required_tags": ["code", "security", "review"],
    "prefer_agent_type": "task",  # Prefer task agents if available
    "store_episodic": True  # Learn from this execution
}
```

The orchestrator will:
1. Find all agents with "code", "security", "review" capabilities
2. Prefer task agents (like "code-reviewer" if available)
3. Fall back to general Claude models if no specialized agent exists
4. Track performance and improve selection over time

### 1. Hierarchical Agent Tree (ReAcTree)

The flow is represented as a tree where:
- **Root nodes** - Entry points to the flow
- **Agent nodes** - LLM-capable reasoning units handling specific subgoals
- **Control flow nodes** - Orchestration using workflow patterns
- **Gate nodes** - Deterministic decision points using BRE

Each node can dynamically expand into child nodes, enabling hierarchical decomposition.

### 2. Business Rules Engine (BRE)

Provides **deterministic** decision-making at gates to avoid AI inconsistency.

**Rule condition language:**
```python
# Simple comparison
{
    "field": "user.age",
    "operator": ">=",
    "value": 18
}

# Logical AND/OR
{
    "AND": [
        {"field": "status", "operator": "==", "value": "active"},
        {"field": "balance", "operator": ">", "value": 0}
    ]
}

# Pattern matching
{
    "MATCHES": {
        "field": "email",
        "pattern": "^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$"
    }
}
```

**Why BRE over AI decisions:**
- **Consistency** - Same input always produces same output
- **Explainability** - Clear audit trail of why decisions were made
- **Reliability** - No hallucination or temperature-based variance
- **Compliance** - Meets regulatory requirements for deterministic behavior

### 3. Workflow Patterns (Anthropic)

Five proven patterns for effective agent design:

#### Pattern 1: Prompt Chaining
Sequential LLM calls where each processes prior output.

**When to use:** Decomposable tasks where intermediate steps improve accuracy.

**Example:** Content generation → Translation → Fact-checking

**Implementation:**
```python
control_flow_node = {
    "node_type": "control_flow",
    "pattern": "prompt_chaining",
    "children": [
        {"name": "generate_content", "type": "agent"},
        {"name": "translate", "type": "agent"},
        {"name": "fact_check", "type": "agent"}
    ]
}
```

#### Pattern 2: Routing
Classify inputs and route to specialized handlers.

**When to use:** Multi-category problems where specialization improves performance.

**Example:** Support ticket routing (technical/billing/account)

**Implementation:** Use BRE routing rules to deterministically select the appropriate handler.

#### Pattern 3: Parallelization
Simultaneous execution via sectioning or voting.

**When to use:** Independent subtasks or when multiple perspectives improve confidence.

**Example:** Multi-file code analysis, consensus-based decision making

#### Pattern 4: Orchestrator-Workers
Central LLM dynamically breaks tasks and delegates to workers.

**When to use:** Unpredictable subtask requirements.

**Example:** Multi-file codebase modifications

#### Pattern 5: Evaluator-Optimizer
Iterative generation and evaluation loops.

**When to use:** Clear quality criteria exist and refinement improves output.

**Example:** Code generation with test-driven refinement

### 4. Dual Memory System

**Episodic Memory** - Goal-specific examples for context retrieval
- Stores successful (and failed) past executions
- Retrieved based on goal similarity
- Provides in-context learning examples

**Working Memory** - Shared observations during execution
- Stores intermediate results
- Shared across nodes in same execution
- Enables context passing without parameter threading

## Flow Creation Process

### Step 1: Define the Goal and Scope

Ask clarifying questions:
1. What is the overall goal?
2. Can this be solved with a single LLM call?
3. What are the distinct steps or decisions required?
4. Are there deterministic decision points (gates)?
5. Do you need audit trails for compliance?

**Example dialogue:**
- "What problem are you trying to solve?"
- "Walk me through the ideal workflow step by step"
- "Are there any yes/no decisions based on specific criteria?"
- "Do you need to track why certain paths were taken?"

### Step 2: Choose Execution Mode

**Workflow Mode** - Predefined paths with deterministic logic
- Predictable, testable, explainable
- Use when steps are known in advance
- Lower cost, faster execution

**Agent Mode** - LLM-directed autonomous execution
- Flexible, adapts to unexpected situations
- Use for open-ended exploration
- Higher cost, requires extensive testing

**Hybrid Mode** - Mix of both
- Workflows for known paths, agents for complex reasoning
- **Recommended** for most production use cases

### Step 3: Design the Tree Structure

Map out the hierarchical decomposition:

```
Root
├── Gate: Check Prerequisites
│   └── Agent: Validate Input Data
├── Control Flow: Main Process (Orchestrator-Workers)
│   ├── Agent: Orchestrator (Plan subtasks)
│   ├── Agent: Worker 1 (Execute subtask 1)
│   ├── Agent: Worker 2 (Execute subtask 2)
│   └── Agent: Synthesizer (Combine results)
└── Control Flow: Post-Process (Evaluator-Optimizer)
    ├── Agent: Generator (Create output)
    └── Agent: Evaluator (Validate quality)
```

### Step 4: Define Business Rules

For each gate node, define the business rules:

**Rule attributes:**
- **name** - Descriptive name
- **rule_type** - gate, validation, transformation, routing
- **condition** - Expression using BRE language
- **action** - What to do when rule fires (for routing/transformation)
- **priority** - Execution order (higher first)

**Example:**
```python
{
    "name": "Credit Approval Gate",
    "rule_type": "gate",
    "condition": {
        "AND": [
            {"field": "credit_score", "operator": ">=", "value": 650},
            {"field": "debt_to_income", "operator": "<=", "value": 0.43},
            {"field": "employment_verified", "operator": "==", "value": True}
        ]
    },
    "priority": 100
}
```

### Step 5: Configure Agent Nodes

For each agent node, specify:

**Goal** - Clear, specific objective for this agent
- ✓ "Extract all email addresses from the document and validate format"
- ✗ "Process the document"

**Episodic Memory** - Whether to store successful executions for future learning
- Enable for frequently repeated tasks
- Disable for one-off or sensitive operations

**Working Memory Keys** - What observations to share
- Be explicit about what downstream nodes need
- Use descriptive keys: `validated_emails`, `extracted_entities`

### Step 6: Implement Using Provided Scripts

Use the provided Python scripts to build your flow:

**Initialize database:**
```python
from database import FlowDatabase

db = FlowDatabase("my_flows.db")
```

**Create flow:**
```python
flow_id = db.create_flow(
    name="Credit Application Processing",
    description="End-to-end credit application with compliance gates"
)
```

**Create nodes:**
```python
from database import NodeType

root_id = db.create_node(
    flow_id=flow_id,
    node_type=NodeType.ROOT,
    name="application_root",
    description="Credit application entry point"
)

gate_id = db.create_node(
    flow_id=flow_id,
    node_type=NodeType.GATE,
    name="credit_score_gate",
    description="Verify minimum credit requirements",
    parent_id=root_id
)
```

**Create business rules:**
```python
db.create_rule(
    flow_id=flow_id,
    name="Minimum Credit Score",
    rule_type="gate",
    condition={"field": "credit_score", "operator": ">=", "value": 650}
)
```

**Execute flow:**
```python
from flow_orchestrator import FlowOrchestrator
from business_rules_engine import BusinessRulesEngine
import asyncio

bre = BusinessRulesEngine(db)
orchestrator = FlowOrchestrator(db, bre)

execution_id = await orchestrator.execute_flow(
    flow_id,
    initial_context={
        "applicant": {
            "credit_score": 720,
            "debt_to_income": 0.35,
            "employment_verified": True
        }
    }
)
```

**Retrieve audit trail:**
```python
status = orchestrator.get_execution_status(execution_id)
audit_trail = db.get_execution_audit_trail(execution_id)

# Get gate evaluation details
gate_evals = db.conn.execute("""
    SELECT * FROM gate_evaluations
    WHERE execution_id = ?
""", (execution_id,)).fetchall()

for eval in gate_evals:
    print(f"Rule: {eval['rule_id']}")
    print(f"Status: {eval['status']}")
    print(f"Reason: {eval['reason']}")
```

### Step 7: Test and Iterate

**Testing strategy:**
1. **Unit test rules** - Validate each business rule independently
2. **Integration test paths** - Test each possible path through the tree
3. **Audit review** - Manually review audit logs for correctness
4. **Load test** - Verify performance with realistic data volumes
5. **Failure scenarios** - Test error handling and recovery

**Iteration based on audit analysis:**
- Review failed executions to identify missing rules
- Analyze gate pass/fail rates to tune thresholds
- Check episodic memory usage to optimize retrieval
- Monitor execution times to identify bottlenecks

## Best Practices

### Rule Design

**✓ DO:**
- Use specific, measurable conditions
- Provide clear rule names that explain intent
- Document why each rule exists
- Test rules with boundary values
- Version control rule definitions

**✗ DON'T:**
- Use AI to make critical business decisions at gates
- Create overly complex nested conditions (refactor into multiple rules)
- Hard-code values (use configuration)
- Skip documentation of rule rationale

### Memory Management

**Episodic Memory:**
- Store only successful executions by default
- Include sufficient context for meaningful retrieval
- Prune old/irrelevant memories periodically
- Use semantic signatures for better matching

**Working Memory:**
- Use descriptive keys (`customer_risk_score` not `temp1`)
- Clean up sensitive data after use
- Set expiration for temporary values
- Document what each key represents

### Audit and Compliance

**Required for regulated industries:**
- Log all gate evaluations with full context
- Store immutable audit trail (append-only)
- Include timestamps, user IDs, execution IDs
- Retain logs per regulatory requirements
- Provide audit export capabilities

**Audit log queries:**
```python
# Find all failed gates for a flow
failed_gates = db.get_audit_logs(
    event_type="gate_evaluation",
    start_time="2024-01-01",
    end_time="2024-12-31"
)

# Analyze gate pass rates
stats = db.conn.execute("""
    SELECT rule_id, status, COUNT(*) as count
    FROM gate_evaluations
    WHERE evaluation_at >= ?
    GROUP BY rule_id, status
""", ("2024-01-01",)).fetchall()
```

### Performance Optimization

**Minimize LLM calls:**
- Use BRE for all deterministic decisions
- Cache episodic memories
- Batch parallel operations
- Avoid unnecessary re-evaluation

**Database optimization:**
- Index frequently queried fields
- Archive old executions
- Use transactions for atomic operations
- Regular VACUUM for SQLite maintenance

## Troubleshooting

### Issue: Gate always passes/fails

**Diagnosis:**
1. Check rule conditions match actual data structure
2. Verify field paths use correct dot notation
3. Review type coercion (string "18" vs int 18)
4. Check rule priority order

**Solution:**
```python
# Test rule independently
from business_rules_engine import BusinessRulesEngine

bre = BusinessRulesEngine()
rule = db.conn.execute(
    "SELECT * FROM business_rules WHERE rule_id = ?",
    (rule_id,)
).fetchone()

result = bre.evaluate_rule(dict(rule), test_context)
print(result.evaluation_details)
```

### Issue: Execution hangs or times out

**Diagnosis:**
1. Check for circular dependencies in tree
2. Review parallelization node child count
3. Check for infinite loops in evaluator-optimizer
4. Monitor database locks

**Solution:**
- Set max_iterations on evaluator-optimizer nodes
- Add execution timeouts
- Review node execution logs

### Issue: Memory not being retrieved

**Diagnosis:**
1. Verify goal signatures match
2. Check episodic memory was stored with success=True
3. Review retrieval limit (default 5)

**Solution:**
```python
# Debug memory retrieval
memories = db.conn.execute("""
    SELECT goal_signature, COUNT(*) as count
    FROM episodic_memory
    WHERE flow_id = ?
    GROUP BY goal_signature
""", (flow_id,)).fetchall()

print("Available memory signatures:", memories)
```

## Advanced Patterns

### Multi-tenant Flows

Add tenant_id to context and filter in rules:
```python
{
    "AND": [
        {"field": "tenant_id", "operator": "==", "value": "{{current_tenant}}"},
        {"field": "user.role", "operator": "==", "value": "admin"}
    ]
}
```

### Dynamic Rule Updates

Rules can be updated without code changes:
```python
db.conn.execute("""
    UPDATE business_rules
    SET condition = ?, updated_at = CURRENT_TIMESTAMP
    WHERE rule_id = ?
""", (json.dumps(new_condition), rule_id))
```

### Conditional Episodic Storage

Store memories only for specific outcomes:
```python
if result.confidence > 0.9:
    db.store_episodic_memory(
        flow_id=flow_id,
        goal_signature=goal_sig,
        example_data={"input": input_data, "output": output},
        success=True,
        metadata={"confidence": result.confidence}
    )
```

## References

- **ReAcTree Paper** - Hierarchical LLM agent trees with control flow
- **Anthropic Guide** - Building effective agents (workflow patterns)
- `references/rule_examples.md` - Comprehensive rule examples
- `references/flow_patterns.md` - Common flow patterns and templates
- `references/api_reference.md` - Complete API documentation

## Example Flows

See `references/examples/` for complete working examples:
- `customer_onboarding.py` - Multi-gate onboarding with KYC
- `document_processing.py` - Routing-based document classification
- `code_review.py` - Evaluator-optimizer for code quality
- `multi_agent_research.py` - Orchestrator-workers for research synthesis
