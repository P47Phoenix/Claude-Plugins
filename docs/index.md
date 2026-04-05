# Delivery Team Plugin

A full delivery pipeline for Claude Code with **11 specialized skills**, a **7-stage pipeline**, **6 collaboration patterns**, and **13 alias themes**.

The delivery-team plugin coordinates an AI delivery team through structured stages — from idea capture through user acceptance testing — with self-correction loops, adversarial review, and self-learning memory.

---

## At a Glance

| Feature | Details |
|---------|---------|
| **Skills** | 11 specialized roles (PO, Developer, Architect, QA, and more) |
| **Pipeline Stages** | 7 stages: Idea, Refine, Design, Architect, Plan, Development, UAT |
| **Project Types** | 6 types with automatic detection and stage routing |
| **Collaboration Patterns** | 6 patterns including adversarial review and debate |
| **Alias Themes** | 13 built-in character themes (Lord of the Rings, Star Wars, etc.) |
| **Self-Learning Memory** | Tiered chunked retrieval that improves with every run |
| **Quality Gates** | Team Definition of Done with multi-role validation |

---

## Quick Links

- **New here?** Start with the [Installation Guide](getting-started/installation.md) and [Quick Start](getting-started/quick-start.md)
- **Looking for a skill?** Browse the [Skills Overview](skills/index.md)
- **Need a config key?** Check the [Configuration Reference](user-guide/config.md)
- **Want to contribute?** Read the [Contributing Guide](contributing/index.md)

---

## How It Works

1. **Start the pipeline** — Say "start a new feature" to trigger `delivery-team:delivery-flow`
2. **Setup wizard** — The wizard auto-detects your project and generates `.delivery/config.yml`
3. **Pipeline execution** — The orchestrator routes work through stages, invoking specialized skills as sub-agents
4. **Quality gates** — Each stage is validated by multiple team roles before advancing
5. **Self-correction** — When validation fails, the pipeline routes feedback back to the responsible agent (max 3 iterations)
6. **Memory** — Lessons from every run are stored and applied to future runs

Each skill operates as an isolated sub-agent — it receives only the artifacts and context relevant to its task, produces its output, and returns a signal to the orchestrator. The orchestrator never reads artifact content directly; it passes file paths between agents.
