# Role-Agent Dispatch

Moved verbatim from `SKILL.md` Steps 4 and 5 (Tier-A line budget). `SKILL.md` keeps a pointer in each step.

## Step 4: role-agent-first dispatch

If a `delivery-<role>` agent exists for the required SKILL (e.g. `delivery-developer`,
`delivery-architect`, `delivery-quality`, `delivery-operations`, `delivery-ui`,
`delivery-user-feedback`, `delivery-product-delivery`, `delivery-godot`,
`delivery-presentation`, `delivery-alias-creator` — see `agents/`), dispatch by
calling the `Agent` tool with that agent's name, passing it the same fields below as
its task. The role agent is a thin wrapper that calls the matching skill internally,
so this avoids constructing the full inline prompt in this context. If no matching
role agent exists, fall back to constructing the prompt directly using the Agent Invocation Template (see `references/pipeline-stages.md` for the exact fields per
stage). Required fields either way:
**SKILL**, **TASK_TYPE**, **ROLE**, **INPUT ARTIFACTS** (file paths only — not content),
**MEMORY LESSONS**, **ALIAS** (personality block if non-business theme; see
`references/pipeline-stages.md` for injection format), **OUTPUT** (namespaced path).

## Step 4: autonomous-run hand-off

For an autonomous/background run of the full pipeline, `delivery-flow` may instead
hand off entirely to the `delivery-orchestrator` agent (spawn via `Agent` tool, name
`delivery-orchestrator`), which owns the complete stage loop — including this dispatch
rule — off the calling conversation's context.

## Step 5: supporting agents

Same role-agent-first rule as Step 4: prefer dispatching to the matching `delivery-<role>`
agent by name over constructing an inline prompt, where one exists.
