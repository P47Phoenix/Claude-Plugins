# Quick Start Guide

Get started with the PRD Quality Gate Flow in 5 minutes.

## Step 1: Build the Flow (First Time Only)

```bash
cd prd-quality-gate-flow
python prd_flow_builder.py
```

**Output:**
```
🏗️  Building PRD Quality Gate Flow...
✓ Flow created: flow_20250115_143022
✓ Flow tree structure created
✓ Total nodes created: 17
✓ Total rules created: 24

✅ PRD Quality Gate Flow Built Successfully!

Flow ID: flow_20250115_143022
Database: prd_flows.db
```

This creates:
- `prd_flows.db` - SQLite database with complete flow definition
- `prd_flow_diagram.txt` - Visual flow structure

## Step 2: Review the Flow Structure

```bash
cat prd_flow_diagram.txt
```

You'll see the complete 7-gate workflow with all agents and decision points.

## Step 3: Run Your First PRD

```bash
python prd_execute.py
```

This executes the default example (AI-Powered Customer Support Dashboard) through all gates.

**You'll see:**
- ✅ Gates being evaluated
- 📊 Business rule checks
- 🤖 Agent executions (simulated)
- 📄 Final execution report

## Step 4: Try Different Examples

```bash
# SaaS Platform
python prd_execute.py saas_platform

# API Service
python prd_execute.py api_service

# Internal Tool
python prd_execute.py internal_tool
```

## Step 5: Review Results

After execution, you'll find:

1. **Console Output** - Real-time execution progress
2. **Execution Report** - JSON file `prd_execution_{id}.json`
3. **Database Records** - Full audit trail in `prd_flows.db`

### View Execution Report

```bash
# View last execution report
cat prd_execution_*.json | jq .
```

### Query Database

```bash
sqlite3 prd_flows.db

-- View all executions
SELECT execution_id, status, started_at FROM executions;

-- View gate evaluations for an execution
SELECT * FROM gate_evaluations WHERE execution_id = 'exec_xxx';

-- View audit trail
SELECT event_type, actor, timestamp FROM audit_log WHERE execution_id = 'exec_xxx';
```

## Understanding the Output

### Gate Evaluation Output

```
gate1_completeness:
  ✅ Required Sections Present
     Score: 100.0 | Decision: GO
     Reason: Condition satisfied

  ✅ Minimum Success Metrics
     Score: 100.0 | Decision: GO
     Reason: Condition satisfied
```

- ✅ = Rule passed
- ❌ = Rule failed
- **Score**: Individual rule score (0-100)
- **Decision**: Gate decision (GO, RECYCLE, HOLD, etc.)

### Execution Flow

1. **PRD Creation** → Agent drafts PRD
2. **Gate 1** → Validates completeness
3. **Technical Review** → Agent assesses feasibility
4. **Gate 2** → Checks technical viability
5. **Stakeholder Review** → Orchestrator collects feedback
6. **Gate 3** → Validates business value
7. **Gate 4** → Executive approval (human)
8. **Implementation Planning** → Agent creates plan
9. **Gate 5** → Resource check
10. **Implementation** → Task flow generation
11. **Evaluation** → Measure outcomes
12. **Gate 6** → Success criteria check
13. **Gate 7** → UAT approval (human)
14. **Retrospective** → Capture learnings

## Next Steps

### Customize Business Rules

Edit `prd_flow_builder.py` to modify gate criteria:

```python
# Example: Change Gate 1 success metrics requirement
self.create_rule(
    flow_id=flow_id,
    gate_node_id=gate_id,
    name="Minimum Success Metrics",
    rule_type="gate",
    condition={
        "field": "prd_document.success_metrics.length",
        "operator": ">=",
        "value": 5  # Changed from 3 to 5
    },
    priority=90
)
```

### Add Custom Product Idea

Create your own product idea:

```python
my_idea = {
    "product_idea": {
        "title": "Smart Analytics Dashboard",
        "description": "Real-time business intelligence dashboard with AI insights",
        "submitter": "you@company.com",
        "business_justification": "Improve decision-making speed by 50%",
        "target_users": "Business executives and analysts",
        "urgency": "HIGH",
        "category": "SAAS"
    }
}

# Execute
import asyncio
from prd_execute import execute_prd_workflow

execution_id = asyncio.run(execute_prd_workflow(my_idea))
```

### Integrate with Real Agents

Replace simulated execution in `flow_orchestrator.py`:

```python
# In _execute_agent_node method
# Replace this:
output = self._simulate_agent_output(agent_type, input_data)

# With your actual agent execution:
output = await your_agent_system.execute(
    agent_type=agent_type,
    goal=config['goal'],
    input=input_data
)
```

## Common Tasks

### View All Flows

```bash
sqlite3 prd_flows.db "SELECT flow_id, name, created_at FROM flows;"
```

### View Flow Nodes

```bash
sqlite3 prd_flows.db "SELECT name, node_type, description FROM nodes WHERE flow_id = 'flow_xxx';"
```

### View Business Rules

```bash
sqlite3 prd_flows.db "SELECT name, rule_type, priority FROM business_rules WHERE flow_id = 'flow_xxx' ORDER BY priority DESC;"
```

### Export Audit Trail

```python
from flow_orchestrator import FlowOrchestrator

orchestrator = FlowOrchestrator("prd_flows.db")
audit_trail = orchestrator.get_audit_trail("exec_xxx")

import json
print(json.dumps(audit_trail, indent=2))
```

## Troubleshooting

### "No module named 'business_rules_engine'"

Make sure you're in the correct directory:
```bash
cd prd-quality-gate-flow
```

### "Database is locked"

Close any other connections to `prd_flows.db`:
```bash
# Check for processes using the database
lsof prd_flows.db  # On Linux/Mac

# Or just delete and rebuild
rm prd_flows.db
python prd_flow_builder.py
```

### Gate Always Fails

Check the rule condition against your data:

```python
from business_rules_engine import BusinessRulesEngine

bre = BusinessRulesEngine()

# Test the rule
result = bre.evaluate_rule(rule_dict, your_context)
print(result.evaluation_details)
```

## Architecture Quick Reference

```
Components:
├── prd_flow_builder.py    → Builds flow structure
├── business_rules_engine.py → Evaluates gates
├── flow_orchestrator.py   → Executes flows
├── prd_execute.py         → Entry point
└── prd_flows.db          → SQLite database

Key Tables:
├── flows                  → Flow definitions
├── nodes                  → Tree structure
├── business_rules         → Gate rules
├── executions             → Execution instances
├── gate_evaluations       → Gate decisions
└── audit_log             → Complete audit trail
```

## What's Next?

1. **Review the full README.md** for detailed documentation
2. **Customize gates** for your organization
3. **Integrate with real agents** (Claude Code Task, etc.)
4. **Add human approval workflows** for Gates 4 & 7
5. **Set up monitoring** and analytics
6. **Connect to your tools** (JIRA, Slack, etc.)

## Getting Help

- Check `README.md` for comprehensive documentation
- Review code comments for implementation details
- Examine `prd_flow_diagram.txt` for flow structure
- Query `prd_flows.db` for execution data

Happy PRD management! 🚀
