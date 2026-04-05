# Skills Overview

The delivery-team plugin provides 11 specialized skills. Each skill operates as an isolated sub-agent with its own reference files and domain knowledge.

## Skills Catalog

| Skill | Invocation | Roles | Purpose |
|-------|------------|-------|---------|
| [Delivery Flow](delivery-flow.md) | `delivery-team:delivery-flow` | Orchestrator | 7-stage pipeline with self-correction, quality gates, and memory |
| [Product Delivery](product-delivery.md) | `delivery-team:product-delivery` | PO, Scrum Master, Data Analyst | User stories, PRDs, retros, metrics, sprint planning |
| [Developer](developer.md) | `delivery-team:developer` | Developer | Code in 14 languages with paradigm-aware patterns |
| [Architect](architect.md) | `delivery-team:architect` | 11 architecture roles | System design, ADRs, decomposition, compliance, game architecture |
| [Quality](quality.md) | `delivery-team:quality` | QA Engineer | Test strategy, test cases, automation, quality metrics |
| [Operations](operations.md) | `delivery-team:operations` | DevOps, Release Manager, Tech Writer | CI/CD, deployment, releases, documentation |
| [UI/UX](ui.md) | `delivery-team:ui` | UX Designer, UI Designer, Game UI | User flows, wireframes, design systems, game UI |
| [User Feedback](user-feedback.md) | `delivery-team:user-feedback` | Persona agents | Simulated persona-based testing (20+ built-in personas) |
| [Godot](godot.md) | `delivery-team:godot` | Godot Developer | Godot 4.x GDScript and C# development |
| [Alias Creator](alias-creator.md) | `delivery-team:alias-creator` | Theme Creator | Create and manage character themes |
| [Presentation](presentation.md) | `delivery-team:presentation` | Presentation Composer | Team-collaborative presentations in 9 types |

## Invocation Syntax

Skills can be triggered directly or through the delivery pipeline:

```
delivery-team:<skill-name>
```

When invoked through the pipeline, skills receive upstream artifacts as file paths, memory lessons, and alias personality injection automatically.

## Context Isolation

Every skill follows the same architectural pattern:

1. **Detect** the relevant role or language from the request
2. **Load** only the relevant reference file(s) — never all references
3. **Spawn** a sub-agent with isolated context
4. **Return** the artifact and signal to the orchestrator

This ensures each agent works with only the knowledge it needs, keeping the main context window clear.
