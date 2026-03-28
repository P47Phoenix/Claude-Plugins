# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Purpose

A marketplace of Claude Code plugins and skills that extend Claude's capabilities with specialized workflows. Hosted at https://github.com/P47Phoenix/Claude-Plugins.

## Plugin Structure

Each plugin lives in its own top-level directory and follows this pattern:

```
<plugin-name>/         # kebab-case naming required
├── SKILL.md           # Primary skill instructions (loaded when skill triggers)
├── LICENSE.txt
├── hooks/             # Event-driven automation (optional)
│   ├── hooks.json     # Hook definitions (SessionStart, Stop, PreToolUse, PostToolUse, SubagentStop)
│   └── *.py           # Python hook implementation scripts
├── scripts/           # Python implementation scripts (shared utilities)
├── skills/            # Sub-skills (optional)
└── references/        # Supporting documentation and examples
```

The marketplace registry is at `.claude-plugin/marketplace.json`. Plugins must be registered there with a unique ID, display name, and description.

## Available Plugins

| Directory | Purpose |
|-----------|---------|
| `delivery-team/` | Full delivery team with 11 skills (see below) |
| `agentic-flow-builder/` | Builds multi-agent workflows using ReAcTree hierarchical decomposition |
| `prompt-engineer/` | Expert LLM prompt optimization |
| `prd-quality-gate-flow/` | 7-gate PRD quality workflow with SQLite persistence |
| `research-agent/` | Research agent with 5 research types and academic frameworks |

### delivery-team Plugin (11 skills)

| Skill | Roles / Purpose |
|-------|----------------|
| `delivery-flow/` | Pipeline orchestrator: 7 stages, team DoD, self-correction, adversarial review, debate, consensus, self-learning memory, setup wizard (18 reference docs + 13 alias themes) |
| `product-delivery/` | Product Owner, Scrum Bag, Data Analyst |
| `developer/` | 14 languages (Python, TypeScript, JavaScript, Go, Rust, C#, Java, SQL, Bash, R, F#, Elixir, Haskell, Scala) + OOP + FP + Frontend + Nx monorepo (paradigm-aware pattern loading from config) + foundational clean code standards (always-on, configurable guide) |
| `godot/` | Godot 4.x game dev (GDScript, C#, scenes, signals, validation) + foundational clean code standards |
| `architect/` | 11 roles: solution/enterprise/data/security/compliance/privacy/IR + 4 game architecture + 4 decomposition strategies |
| `quality/` | QA engineering: test strategy, test cases, automation, quality metrics, empirical validation |
| `operations/` | DevOps, Release Manager, Technical Writer |
| `ui/` | UX Designer, UI Designer, Game UI Designer |
| `user-feedback/` | Simulated persona-based testing (20+ built-in personas across gamers, web users, enterprise, demographics) |
| `alias-creator/` | Creates personality-injected aliases from 13 built-in themes |
| `presentation/` | Presentation Composer: team-collaborative presentations with 6-step flow (Assemble, Content Gate, Draft, Compose, Review Gate, User Review). 4 types: Sprint Review, Feature Pitch, Stakeholder Update, Technical Deep-Dive |

### delivery-team Hooks (7 hooks across 5 event types)

| Hook | Event | Purpose |
|------|-------|---------|
| Config check | SessionStart | Validates `.delivery/config.yml` exists and is current |
| Retrospective enforcement | Stop | Blocks session end if pipeline work occurred without retrospective |
| Pipeline bypass detection | PreToolUse (Skill) | Warns when developer/godot invoked outside delivery-flow |
| Agent prompt audit | PreToolUse (Agent) | Audits agent prompts for context isolation compliance |
| GDScript validation | PostToolUse (Write/Edit) | Parse-validates `.gd` files via `godot --headless --check-only` |
| Skill load verification | PostToolUse (Agent) | Verifies SKILL_LOADED signal in agent responses |
| Empirical validation | SubagentStop (developer/godot) | Detects runtime-only acceptance criteria |

## Running Scripts

All scripts are Python with no external dependency management. Run directly:

```bash
# PRD quality gate flow
python prd-quality-gate-flow/prd_flow_builder.py
python prd-quality-gate-flow/prd_execute.py
python prd-quality-gate-flow/check_db.py       # Inspect SQLite DB state
python prd-quality-gate-flow/fix_and_run.py    # Automated end-to-end run
```

No build step, linting config, or test runner is configured.

## Architecture Patterns

**Skill vs Plugin distinction**:
- A *skill* is a SKILL.md file with optional scripts/references — it adds specialized knowledge to Claude
- A *plugin* bundles multiple components: slash commands, agents, hooks, skills, and/or MCP servers

**Three-level context loading** (used by all skills):
1. Metadata (always loaded) — from `marketplace.json`
2. SKILL.md (loaded when skill triggers) — main instructions
3. Resources (loaded on demand) — scripts, references, assets

**Delivery-flow pipeline architecture**:
- 7 stages: Idea → Refine → Design → Architect → Plan → Development → UAT
- Auto-detect project type (GREENFIELD, FEATURE, BUG_FIX, GAME_DEV, SPIKE, DOCS_ONLY) with stage routing
- Team DoD validation (ALL validators must say DONE)
- 6 collaboration patterns: evaluator-optimizer, adversarial review, review board, decision ownership, debate, consensus
- Self-learning memory in `.delivery/memory/` (tiered chunked retrieval)
- Config-driven via `.delivery/config.yml` with versioned schema
- Setup wizard with 10 questions (auto-detect + smart options)
- Defect tracking with plugin self-improvement PR triggers
- Feature Knowledge System: Feature Knowledge Cards (FKCs), Impact Analysis Gate, decision trail for cross-cutting change tracking
- Session keepalive: cross-platform companion process for long-running sessions
- Pipeline state persistence and resume across sessions
- Git/GitHub integration: branching strategies, conventional commits, automated issue/PR creation
- 13 alias themes with personality injection (via alias-creator skill)
- Config validation toolchain: JSON Schema generation + validation scripts
- Pipeline analytics dashboard for delivery metrics

**Agentic flow core components** (shared pattern between `agentic-flow-builder/` and `prd-quality-gate-flow/`):
- `database.py` — SQLite schema, DAL, execution tracking, audit logs
- `business_rules_engine.py` — Deterministic gate evaluation (AND/OR/NOT logic, no AI variance)
- `flow_orchestrator.py` — Hierarchical execution with episodic + working memory
- `agent_registry.py` — Dynamic agent discovery, assignment, and performance tracking

**Business Rules Engine** is intentionally deterministic — gate decisions must be rule-based, not AI-inferred, to ensure consistent and auditable workflow outcomes.

## Key Conventions

**When modifying this repo, always use the relevant plugin-dev skills:**
- Creating/modifying hooks → load `plugin-dev:hook-development` first
- Creating/modifying skills → load `plugin-dev:skill-development` first
- Creating/modifying plugin structure → load `plugin-dev:plugin-structure` first
- After creating a skill → use `plugin-dev:skill-reviewer` to review it
- After creating a plugin → use `plugin-dev:plugin-validator` to validate it

**Config schema**: The single source of truth for `.delivery/config.yml` format is `delivery-flow/references/config-schema.md` (currently v2.3). When adding new config keys, follow the extension protocol documented there.

## Permissions

Allowed operations are defined in `.claude/settings.local.json` (git-ignored):
- WebFetch: github.com, raw.githubusercontent.com, arxiv.org, www.anthropic.com
- Bash: curl, mkdir, git operations, chmod, cat, python, sqlite3
- WebSearch: enabled
