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

Each plugin should include an `ARCHITECTURE.md` with Mermaid diagrams documenting internal design for contributors.

## Available Plugins

| Directory | Purpose |
|-----------|---------|
| `delivery-team/` | Full delivery team with 11 skills (see below) |
| `agentic-flow-builder/` | Builds multi-agent workflows using ReAcTree hierarchical decomposition |
| `prompt-engineer/` | Expert LLM prompt optimization |
| `prd-quality-gate-flow/` | 7-gate PRD quality workflow with SQLite persistence |
| `research-agent/` | Research agent with 5 research types and academic frameworks |
| `mtg-commander/` | MTG Commander deck builder: synergy-first multi-agent pipeline, Scryfall integration, configurable price goals + adversarial Challenger agents via `.mtg-commander.yml` |

### delivery-team Plugin (11 skills)

| Skill | Roles / Purpose |
|-------|----------------|
| `delivery-flow/` | Pipeline orchestrator: 7 stages, team DoD, self-correction, adversarial review, debate, consensus, self-learning memory, setup wizard. Primitives include shared `constraints.yml` (Refine + Architect), configurable Architecture Board, and Transformation Planning sub-workflow orchestration |
| `product-delivery/` | Product Owner, Scrum Bag, Data Analyst |
| `developer/` | 14 languages (Python, TypeScript, JavaScript, Go, Rust, C#, Java, SQL, Bash, R, F#, Elixir, Haskell, Scala) + OOP + FP + Frontend + Nx monorepo (paradigm-aware pattern loading from config) + foundational clean code standards (always-on, configurable guide) |
| `godot/` | Godot 4.x game dev (GDScript, C#, scenes, signals, validation) + foundational clean code standards |
| `architect/` | 11 roles: solution/enterprise/data/security/compliance/privacy/IR + 4 game architecture + 4 decomposition strategies + Prior Art Analysis. Paradigm sub-skills under `skills/paradigms/` (e.g., `volatility/`, `ddd/`) with router-based dispatch so only the selected paradigm loads. Supports `transformation-planning` task type (AS-IS behavioral/structural → TO-BE → Roadmap) for brownfield migrations |
| `quality/` | QA engineering: test strategy, test cases, automation, quality metrics, empirical validation |
| `operations/` | DevOps, Release Manager, Technical Writer |
| `ui/` | UX Designer, UI Designer, Game UI Designer |
| `user-feedback/` | Simulated persona-based testing (20+ built-in personas across gamers, web users, enterprise, demographics) |
| `alias-creator/` | Creates personality-injected aliases from 13 built-in themes |
| `presentation/` | Presentation Composer: team-collaborative presentations with 6-step flow (Assemble, Content Gate, Draft, Compose, Review Gate, User Review). 9 types (Sprint Review, Feature Pitch, Stakeholder Update, Technical Deep-Dive, Investor Pitch, Roadmap, Product Demo, Onboarding, Retrospective Summary), 4 formats (structured-markdown, marp, paste-ready, pptx), narrative intelligence (4 editorial passes), light mode |

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

**CI regression guards** (under `.github/workflows/`):
- `workflow-injection-lint.yml` — fails PRs that interpolate `${{ github.event.* }}` directly inside workflow `run:` blocks (DEFECT-004 regression guard).

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
- Auto-detect project type (GREENFIELD, FEATURE, BUG_FIX, DESIGN, GAME_DEV, SPIKE, DOCS_ONLY) with stage routing (DESIGN terminates after Architect for design-only engagements)
- Team DoD validation (ALL validators must say DONE)
- 6 collaboration patterns: evaluator-optimizer, adversarial review, review board, decision ownership, debate, consensus
- Self-learning memory in `.delivery/memory/` (tiered chunked retrieval)
- Config-driven via `.delivery/config.yml` with versioned schema (currently v2.7)
- Project type is **detected per run** (Phase 1 always runs). Config no longer pins it; `routing.force_type` is an opt-in override
- Setup wizard with 9 questions (auto-detect + smart options). The former Project Type question was removed in v2.7 since the type is a runtime routing decision
- Defect tracking with plugin self-improvement PR triggers
- Feature Knowledge System: Feature Knowledge Cards (FKCs), Impact Analysis Gate, decision trail for cross-cutting change tracking
- Session keepalive: cross-platform companion process for long-running sessions
- Pipeline state persistence and resume across sessions
- Git/GitHub integration: branching strategies, conventional commits, automated issue/PR creation
- 13 alias themes with personality injection (via alias-creator skill) and theme surfacing in orchestrator output (stage announcements, checkpoint summaries, transitions)
- Config validation toolchain: JSON Schema generation + validation scripts
- Pipeline analytics dashboard for delivery metrics
- Constraints primitive: shared `constraints.yml` schema (entities, state_variables, actions, invariants, forbidden_vocabulary, etc.) used across Refine + Architect stages; see `delivery-flow/references/constraints-model-guide.md` and `constraints-schema.json`; validated via `delivery-flow/references/scripts/validate_constraints.py`
- Architecture Board: configurable multi-persona review pattern (Volatility / DDD / Risk / Chief Architect personas) with MAR iteration-2 cross-persona routing; personas defined in `delivery-flow/references/architecture-board-personas.md`
- Transformation Planning: AS-IS → TO-BE → Roadmap sub-workflow for brownfield migration planning (PO + Architect paired); reuses the Architecture Board for Phase 1A review. See `architect/references/transformation-planning.md` and the four phase docs (`transformation-phase-1a-behavioral.md`, `transformation-phase-1b-structural.md`, `transformation-phase-2-to-be.md`, `transformation-phase-3-roadmap.md`)
- Design Sprint sub-workflow: PO + Architect paired flow for decomposition decisions, routes to the appropriate paradigm skill (volatility, DDD, etc.); see `delivery-flow/references/design-sprint.md`

**Agentic flow core components** (shared pattern between `agentic-flow-builder/` and `prd-quality-gate-flow/`):
- `database.py` — SQLite schema, DAL, execution tracking, audit logs
- `business_rules_engine.py` — Deterministic gate evaluation (AND/OR/NOT logic, no AI variance)
- `flow_orchestrator.py` — Hierarchical execution with episodic + working memory
- `agent_registry.py` — Dynamic agent discovery, assignment, and performance tracking

**Business Rules Engine** is intentionally deterministic — gate decisions must be rule-based, not AI-inferred, to ensure consistent and auditable workflow outcomes.

Detailed flow documents in `delivery-team/architecture/` cover adversarial triggers, deterministic gating, hook timeline, DoD self-correction, empirical lifecycle, sub-agent dispatch.

## Key Conventions

**When modifying this repo, always use the relevant plugin-dev skills:**
- Creating/modifying hooks → load `plugin-dev:hook-development` first
- Creating/modifying skills → load `plugin-dev:skill-development` first
- Creating/modifying plugin structure → load `plugin-dev:plugin-structure` first
- After creating a skill → use `plugin-dev:skill-reviewer` to review it
- After creating a plugin → use `plugin-dev:plugin-validator` to validate it

**Config schema**: The single source of truth for `.delivery/config.yml` format is `delivery-flow/references/config-schema.md` (currently v2.7). When adding new config keys, follow the extension protocol documented there. Note: `project_type` was removed in v2.7 — Phase 1 project type detection now runs on every pipeline invocation. Use `routing.force_type` for an opt-in intentional pin.

## Permissions

Allowed operations are defined in `.claude/settings.local.json` (git-ignored):
- WebFetch: github.com, raw.githubusercontent.com, arxiv.org, www.anthropic.com
- Bash: curl, mkdir, git operations, chmod, cat, python, sqlite3
- WebSearch: enabled
