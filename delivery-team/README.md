# Delivery Team

A full software delivery team with 9 specialized skills covering the complete delivery lifecycle from idea to release.

## Overview

The delivery team orchestrates Product Owners, Developers, Architects, QA Engineers, DevOps, UX/UI Designers, and simulated end users through a structured pipeline with self-correction, adversarial review, and self-learning memory.

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
| **developer** | 14 languages + OOP + FP + Frontend + Nx | Code implementation with language context isolation and paradigm-aware pattern loading |
| **godot** | GDScript, C#, Scenes, Signals | Godot 4.x game dev with headless validation and defect prevention |
| **architect** | 11 roles + 4 decomposition strategies | Solution/Enterprise/Data/Security/Compliance/Privacy/IR + Game architecture. Config-driven style and decomposition (IDesign, DDD, Team Topology, Event Storming) |
| **quality** | QA Engineer | Test strategy, test cases, automation, quality metrics, empirical validation, exploratory testing, milestone testing |
| **operations** | DevOps, Release Manager, Technical Writer | CI/CD, deployment, infrastructure, release planning, API docs, runbooks |
| **ui** | UX Designer, UI Designer, Game UI Designer | User flows, wireframes, design systems, accessibility, HUD, game menus |
| **user-feedback** | 20+ simulated personas | Persona-based testing across gamers, web users, enterprise, and demographics |

## Hooks

| Hook | Event | Purpose |
|------|-------|---------|
| Pipeline bypass detection | PreToolUse (Skill) | Warns when developer/godot invoked outside delivery-flow |
| GDScript validation | PostToolUse (Write/Edit) | Parse-validates .gd files after write |
| Empirical validation | SubagentStop (developer/godot) | Detects runtime-only acceptance criteria |
| Retrospective enforcement | Stop | Blocks session end if pipeline work occurred without retrospective |

## Key Features

- **Setup wizard**: 10+ question config wizard with codebase auto-detection
- **Team DoD**: Every artifact validated by multiple roles before advancing
- **6 collaboration patterns**: Evaluator-optimizer, adversarial review, review board, decision ownership, debate, consensus
- **Self-learning memory**: Tiered chunked retrieval in `.delivery/memory/`
- **Defect tracking**: Self-improvement feedback loop that opens PRs to improve the plugin
- **Empirical validation**: Detects acceptance criteria requiring runtime verification (CODE_COMPLETE status)
- **Domain discovery**: Architect interviews PO with strategy-specific questions before design
- **Config-driven**: Architecture style, decomposition strategy, paradigm, personas all configurable

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
```

## License

Apache License 2.0 - See LICENSE.txt
