# Architecture Style and Decomposition from Config

This reference captures the config-driven architecture style and decomposition strategy selection. The parent SKILL.md retains a 4-line pointer table; the substantive content lives here so it loads only when the architect runs a `design` or `decompose` task.

## Architecture Style

If `.delivery/config.yml` exists, check `architecture.style`:

- `style: auto` (default) → detect from task context, use decision matrix in `references/architecture-patterns.md`
- `style: layered` → emphasize layered/n-tier patterns
- `style: hexagonal` / `style: clean` → emphasize ports-and-adapters, clean architecture
- `style: modular-monolith` → emphasize module boundaries, no microservices overhead
- `style: microservices` → emphasize service boundaries, data ownership, async communication
- `style: event-driven` → emphasize event sourcing, CQRS, event-driven topology
- `style: serverless` → emphasize function-as-a-service, managed services

Per-component overrides in `architecture.style_overrides`:
```yaml
architecture:
  style: hexagonal
  style_overrides:
    data-pipeline: event-driven
    admin-panel: layered
```

## Decomposition Strategy

The `architecture.decomposition` config value determines which decomposition reference is loaded for `decompose` and `design` tasks:

| Config Value | Reference Loaded | Method |
|-------------|-----------------|--------|
| `auto` | `references/architecture-patterns.md` (decision matrix) | Detect from context |
| `volatility` | `references/volatility-decomposition.md` | IDesign: decompose by axes of change |
| `ddd` | `references/strategic-ddd.md` + `references/architecture-patterns.md` | Strategic DDD: subdomains, bounded contexts |
| `team-topology` | `references/team-topology.md` | Inverse Conway: decompose by team cognitive load |
| `event-storming` | `references/event-storming.md` | Event-driven: discover boundaries from domain events |
| `business-capability` | `references/architecture-patterns.md` (microservices section) | Traditional: map capabilities to services |

## Decision Matrix Inputs

When `decomposition: auto`, use `architecture.decision_matrix_inputs` to guide the recommendation:

| Input | Low | Medium | High | Influences |
|-------|-----|--------|------|-----------|
| `team_size` | 1-3 | 4-8 | 9+ | Microservices viability, team topology applicability |
| `deploy_independence` | Monolith OK | Some independence | Full independence needed | Monolith vs microservices |
| `domain_complexity` | Simple CRUD | Moderate rules | Rich domain logic | DDD applicability |
| `change_rate` | Stable | Moderate change | Frequent change | Volatility decomposition applicability |

## Paradigm Router

When a `decompose` or `design` task is detected, the architect routes to a paradigm-specific sub-skill instead of executing decomposition inline. This achieves context isolation — the sub-agent loads only the references relevant to one paradigm, not the full monolithic set.

### Detection Priority Chain (ADR-002)

Paradigm selection follows a deterministic priority chain. At each level, if the signal is present and unambiguous, routing is immediate — no further levels are consulted:

1. **Explicit user intent** — If the user's prompt contains an unambiguous paradigm reference ("use volatility", "DDD decomposition", "IDesign"), that paradigm is selected. User intent overrides all other signals.
2. **Config value** — If no explicit intent is detected, read `architecture.decomposition` from `.delivery/config.yml`. If set to a specific paradigm (`volatility`, `ddd`, `team-topology`, `event-storming`, `business-capability`), use it.
3. **Decision matrix fallback** — If config is `auto` or absent, evaluate the decision matrix inputs (`domain_complexity`, `change_rate`, `team_size`, `deploy_independence`) to recommend a paradigm, then route to the detected paradigm sub-skill.

### Routing Mechanism

After paradigm detection, the architect dispatches an `Agent` with the paradigm sub-skill's SKILL.md loaded, plus the shared references declared in that SKILL.md's `shared_refs` frontmatter. The sub-agent receives ONLY the paradigm-scoped references — no implicit loading, no cross-paradigm context bleeding.

```
Agent(
  prompt = paradigm SKILL.md contents + shared_refs contents + task context,
  tools = [Read, Write, Edit, Glob, Grep]
)
```

**Non-decomposition bypass:** Task types that do not involve decomposition (`review`, `document`, `evaluate`, `model`, `compliance-checklist`, `security-requirements`, `incident-response-plan`, `privacy-assessment`, `audit-preparation`, `risk-assessment`, `policy-document`, `transformation-planning`) bypass paradigm routing entirely and execute through existing logic unchanged.

**Backwards compatibility:** If `paradigms/` does not exist or the paradigm has no `SKILL.md`, fall back to inline decomposition using existing references. No pipeline breaks.

### Paradigm Directory Structure

Each paradigm sub-skill lives under `paradigms/<paradigm-id>/SKILL.md` with frontmatter declaring `paradigm_id`, `display_name`, `shared_refs`, and `task_types`. Add paradigm-specific references under `paradigms/<id>/references/`. The router discovers paradigm sub-skills by directory — no registration in `plugin.json` required (ADR-001).
