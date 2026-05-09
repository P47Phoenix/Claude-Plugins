# Cross-Role Tasks — Combined Reference Loading

When a task spans multiple architect roles (e.g., "design a multiplayer game with anti-cheat" or "design a data pipeline with security requirements"), the architect skill MUST follow the godot pattern: load multiple references into a single sub-agent rather than spawning separate sub-agents per role.

## Procedure

1. **Identify all roles involved** — re-read the request and tag every role implied by the request signals (Phase 1 routing tables in the per-role manifest under `references/roles/<role>.md`).
2. **Load all relevant reference files** — godot pattern: multiple references in one sub-agent prompt, separated by `---`.
3. **Spawn a single sub-agent** with combined references. Cross-cutting decisions stay coherent in one reasoning context.
4. **If concerns are truly independent** (e.g., the security review and the data design have no interaction surface), spawn separate sub-agents sequentially. The default is combined; sequential split requires justification.

Game and software roles can combine freely. The combination is a property of the task, not the role.

## Common Cross-Role Combinations

| Scenario | References Loaded |
|----------|-------------------|
| Multiplayer game with security | network-multiplayer.md + security-patterns.md |
| Game with cloud backend | game-systems.md + architecture-patterns.md |
| Data-heavy game (analytics, leaderboards) | game-systems.md + data-modeling.md |
| Enterprise system with data security | architecture-patterns.md + data-modeling.md + security-patterns.md |
| Compliance-driven system design | architecture-patterns.md + compliance-frameworks.md + security-requirements.md |
| Privacy-aware data architecture | data-modeling.md + privacy-patterns.md + compliance-frameworks.md |
| Incident-ready security architecture | security-patterns.md + incident-response.md + compliance-frameworks.md |
| Full system design | architecture-patterns.md + c4-model.md + quality-attributes.md |

## Sub-Agent Prompt Convention for Combined References

When loading >1 reference into a single sub-agent, separate the reference contents with `---` delimiters and prefix each with the source filename, so the sub-agent retains provenance:

```
You are an expert [combined ROLE] architect. Apply these architecture principles and patterns to everything you produce:

--- references/network-multiplayer.md ---
[FULL CONTENTS]
--- references/security-patterns.md ---
[FULL CONTENTS]
---

## Task
[TASK TYPE]: [DESCRIBE WHAT THE USER WANTS]
```

This convention preserves the existing single-reference prompt template (Phase 2 §Sub-Agent Prompt Template in the parent SKILL.md) while explicitly handling the multi-reference case.
