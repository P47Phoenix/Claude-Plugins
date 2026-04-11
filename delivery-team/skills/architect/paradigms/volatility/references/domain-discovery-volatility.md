# Volatility Domain Discovery — Quick Reference

Extracted from the shared domain-discovery interview protocol. Use these questions during the Architect stage when the volatility (IDesign) decomposition strategy is active. The full protocol lives in `delivery-team/skills/architect/references/domain-discovery.md`.

## Step 1: Business Process Walkthrough

1. "Walk me through how [core business process] works from start to finish."
2. "What are the steps? Who is involved at each step? What decisions are made?"
3. "What data moves between steps? In what format?"
4. "Are there variations of this process? When does the process branch?"
5. "What happens when things go wrong? How are errors handled?"

Document as: activity → decision → activity → outcome. Repeat per process.

## Step 2: Change History (the volatility axis)

6. "In the last 12 months, which parts of this process changed? Why?"
7. "Which changes stayed contained and which spread everywhere?"
8. "What's on the roadmap that will change these processes in the next 6-12 months?"
9. "Have any external integrations or regulations forced process changes?"

## Step 3: Commonality vs Volatility

10. "Which activities appear in multiple processes?" (commonalities → shared Engines/Accessors)
11. "Which steps change most often? Why?" (volatilities → encapsulation boundaries)
12. "If [step] changed, what else would need to change?" (ripple radius test)
13. "Which parts are commodity vs unique to your business?" (build vs buy signal)

## Step 4: Decomposition Validation

14. "If [real upcoming change] happens, here's what would change. Does that seem contained?"
15. "Does this component grouping make sense? Would changes stay isolated?"
16. "Are there changes I haven't considered that would break this structure?"

## Escalation Triggers

Escalate to human when:
- PO cannot walk through business processes (needs domain expert)
- Change history is unavailable (needs organizational knowledge)
- Validation scenarios reveal the decomposition doesn't contain changes

## Volatility-Axis Checklist

Before leaving discovery, confirm you have answers on all five axes:

| Axis | Key Question |
|------|-------------|
| Requirements | Which business rules change frequently? |
| Technology | Which technologies are likely to be replaced? |
| Integration | Which external systems change their APIs? |
| Data | Which data schemas evolve? |
| Policy | Which regulatory/compliance rules change? |

Reference: Juval Lowy, "Righting Software" (Addison-Wesley, 2019).
