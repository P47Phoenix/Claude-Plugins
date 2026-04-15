# Delivery Team

A full software delivery team with 11 specialized skills covering the complete delivery lifecycle from idea to release.

> See also: [ARCHITECTURE.md](./ARCHITECTURE.md) — internal design and Mermaid diagrams for contributors. Detailed flow docs in [architecture/](./architecture/).

## Overview

The delivery team orchestrates Product Owners, Developers, Architects, QA Engineers, DevOps, UX/UI Designers, and simulated end users through a structured pipeline with self-correction, adversarial review, and self-learning memory. 11 specialized skills cover the complete delivery lifecycle.

## Quick Start

New to the delivery team? Say:

```
delivery-team:delivery-flow
```

The setup wizard will guide you. For a faster setup, say "quick start" -- it asks just 3 questions.

See `skills/delivery-flow/references/getting-started.md` for a complete walkthrough.

## Skills

| Skill | Roles | Purpose |
|-------|-------|---------|
| **delivery-flow** | Pipeline orchestrator | 7-stage pipeline (Idea, Refine, Design, Architect, Plan, Dev, UAT) with setup wizard, team DoD, 6 collaboration patterns |
| **product-delivery** | Product Owner, Scrum Bag, Data Analyst | User stories, PRDs, backlogs, sprint plans, retrospectives, metrics, A/B testing |
| **developer** | 14 languages + OOP + FP + Frontend + Nx + Clean Code | Code implementation with language context isolation, paradigm-aware pattern loading, and foundational clean code standards |
| **godot** | GDScript, C#, Scenes, Signals, Clean Code | Godot 4.x game dev with headless validation, defect prevention, and clean code standards |
| **architect** | 11 roles + 4 decomposition strategies | Solution/Enterprise/Data/Security/Compliance/Privacy/IR + Game architecture. Config-driven style and decomposition (IDesign, DDD, Team Topology, Event Storming) |
| **quality** | QA Engineer | Test strategy, test cases, automation, quality metrics, empirical validation, exploratory testing, milestone testing |
| **operations** | DevOps, Release Manager, Technical Writer | CI/CD, deployment, infrastructure, release planning, API docs, runbooks |
| **ui** | UX Designer, UI Designer, Game UI Designer | User flows, wireframes, design systems, accessibility, HUD, game menus |
| **user-feedback** | 20+ simulated personas | Persona-based testing across gamers, web users, enterprise, and demographics |
| **alias-creator** | 13 built-in themes | Create and manage agent personality themes (LOTR, Marvel, Star Wars, Breaking Bad, The Office, etc.) |
| **presentation** | Presentation Composer | Team-collaborative presentations with 6-step gated flow (4 types, 3 output formats, narrative adaptation, source citations) |

## Hooks

| Hook | Event | Purpose |
|------|-------|---------|
| Config check | SessionStart | Validates .delivery/config.yml exists and is current |
| Retrospective enforcement | Stop | Blocks session end if pipeline work occurred without retrospective |
| Pipeline bypass detection | PreToolUse (Skill) | Warns when developer/godot invoked outside delivery-flow |
| Agent prompt audit | PreToolUse (Agent) | Audits agent prompts for context isolation compliance |
| GDScript validation | PostToolUse (Write/Edit) | Parse-validates .gd files via godot --headless --check-only |
| Skill load verification | PostToolUse (Agent) | Verifies SKILL_LOADED signal in agent responses |
| Empirical validation | SubagentStop (developer/godot) | Detects runtime-only acceptance criteria |

## Key Features

- **Setup wizard**: 9-question config wizard with codebase auto-detection (schema v2.8; project type detected per-run from GREENFIELD, FEATURE, BUG_FIX, DESIGN, GAME_DEV+, SPIKE, DOCS_ONLY — DESIGN supports design-only engagements terminating after Architect; not pinned in config; `routing.force_type` available as opt-in pin)
- **Team DoD**: Every artifact validated by multiple roles before advancing
- **6 collaboration patterns**: Evaluator-optimizer, adversarial review, review board, decision ownership, debate, consensus
- **Self-learning memory**: Tiered chunked retrieval in `.delivery/memory/`
- **Defect tracking**: Self-improvement feedback loop that opens PRs to improve the plugin
- **Empirical validation**: Detects acceptance criteria requiring runtime verification (CODE_COMPLETE status)
- **Domain discovery**: Architect interviews PO with strategy-specific questions before design
- **Config-driven**: Architecture style, decomposition strategy, paradigm, personas all configurable
- **Session keepalive**: Companion process keeps Claude active -- anti-idle nudges, rate-limit wait-and-resume, periodic monitoring. Cross-platform (Linux, macOS, Windows).
- **13 alias themes**: Personality injection with LOTR, Marvel, Star Wars, Breaking Bad, The Office, and more
- **Config validation toolchain**: JSON Schema generation + validation
- **Pipeline analytics dashboard**: Visualize pipeline metrics and team performance
- **Git/GitHub integration**: Branching, conventional commits, issue/PR creation
- **Feature Knowledge System**: FKCs, Impact Analysis Gate

## Installation

```
/plugin install delivery-team
```

## Usage

Start the delivery pipeline:
```
delivery-team:delivery-flow
```

Or use individual skills directly:
```
delivery-team:developer      # Code implementation
delivery-team:architect      # Architecture design
delivery-team:quality        # Test planning
delivery-team:operations     # DevOps, releases, docs
delivery-team:ui             # UX/UI design
delivery-team:user-feedback  # Persona-based testing
delivery-team:alias-creator  # Create/manage alias themes
delivery-team:presentation  # Team presentations
```

## License

Apache License 2.0 - See LICENSE.txt
