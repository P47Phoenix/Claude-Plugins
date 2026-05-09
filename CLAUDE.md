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

| Directory | Purpose | Detail |
|-----------|---------|--------|
| `delivery-team/` | Full delivery team with 11 skills (orchestrator + 10 workers, 7 hooks) | `delivery-team/ARCHITECTURE.md` |
| `hardware-team/` | Hardware delivery pipeline over kicad-happy: 8 stages, 7 roles, 6 hooks | `hardware-team/ARCHITECTURE.md` |
| `agentic-flow-builder/` | Builds multi-agent workflows using ReAcTree hierarchical decomposition | `agentic-flow-builder/ARCHITECTURE.md` |
| `prompt-engineer/` | Expert LLM prompt optimization | — |
| `prd-quality-gate-flow/` | 7-gate PRD quality workflow with SQLite persistence | — |
| `research-agent/` | Research agent with 5 research types and academic frameworks | — |
| `mtg-commander/` | MTG Commander deck builder: synergy-first multi-agent pipeline, Scryfall integration, configurable price goals + adversarial Challenger agents via `.mtg-commander.yml` | — |

For per-skill rosters, hook tables, and pipeline internals, follow the `Detail` column. Plugin-level docs are the source of truth; this file stays a one-screen index.

**CI regression guards** (under `.github/workflows/`):
- `workflow-injection-lint.yml` — fails PRs that interpolate `${{ github.event.* }}` directly inside workflow `run:` blocks (DEFECT-004 regression guard).
- `skill-line-budget.yml` — enforces SKILL.md line budgets (`scripts/check_skill_budgets.py`, `governance/skill-budgets.json`).
- `fitness-review.yml` — weekly scan of `fitness_review_due:` frontmatter; opens reminder issues per `governance/fitness-review.md`.

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

**Delivery-flow pipeline (summary)**:
- 7 stages: Idea → Refine → Design → Architect → Plan → Development → UAT
- Auto-detect project type per run (GREENFIELD, FEATURE, BUG_FIX, DESIGN, GAME_DEV, SPIKE, DOCS_ONLY); `routing.force_type` is the opt-in pin
- Team DoD validation, 6 collaboration patterns (evaluator-optimizer, adversarial review, review board, decision ownership, debate, consensus), self-learning memory in `.delivery/memory/`
- Config-driven via `.delivery/config.yml` with versioned schema (currently v2.7); setup wizard with 9 questions
- Sub-workflows: Transformation Planning (AS-IS → TO-BE → Roadmap), Design Sprint (paradigm decomposition), Architecture Board (multi-persona review), Constraints primitive (shared `constraints.yml`)

For full pipeline internals (defect tracking, Feature Knowledge System, session keepalive, paradigm sub-skills, alias themes, analytics dashboard) see `delivery-team/ARCHITECTURE.md` and `delivery-team/skills/delivery-flow/references/`.

**Agentic flow core components** (shared between `agentic-flow-builder/` and `prd-quality-gate-flow/`):
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

**Config schema**: The single source of truth for `.delivery/config.yml` format is `delivery-team/skills/delivery-flow/references/config-schema.md` (currently v2.7). When adding new config keys, follow the extension protocol documented there.

**SKILL.md line budgets**: Enforced by `scripts/check_skill_budgets.py` against `governance/skill-budgets.json`. Tier A=500, Tier B=300, Tier C=200. Exceptions require a `Budget-Exception:` line in the PR body and a `known_debt[]` entry with `target_wave:`.

**Skill fitness reviews**: Quarterly per `governance/fitness-review.md`; due dates live in each SKILL.md `fitness_review_due:` frontmatter.

## Permissions

Allowed operations are defined in `.claude/settings.local.json` (git-ignored):
- WebFetch: github.com, raw.githubusercontent.com, arxiv.org, www.anthropic.com
- Bash: curl, mkdir, git operations, chmod, cat, python, sqlite3
- WebSearch: enabled

**Local pre-commit hook** (W3-16, opt-in): `git config core.hooksPath .githooks` — runs SKILL.md budget + KNOWN_DEBT lint on each commit. See `governance/git-hooks-install.md`.
