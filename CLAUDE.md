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
├── scripts/           # Python implementation scripts
├── skills/            # Sub-skills (optional)
└── references/        # Supporting documentation and examples
```

The marketplace registry is at `.claude-plugin/marketplace.json`. Plugins must be registered there with a unique ID, display name, and description.

## Available Plugins

| Directory | Purpose |
|-----------|---------|
| `skill-creator/` | Guides creation of new skills (SKILL.md-based) |
| `plugin-creator/` | Guides creation of complete plugins (commands, agents, hooks, skills, MCPs) |
| `agentic-flow-builder/` | Builds multi-agent workflows using ReAcTree hierarchical decomposition |
| `prompt-engineer/` | Expert LLM prompt optimization |
| `prd-quality-gate-flow/` | 7-gate PRD quality workflow with SQLite persistence |

## Running Scripts

All scripts are Python with no external dependency management. Run directly:

```bash
# Skill creator utilities
python skill-creator/scripts/init_skill.py
python skill-creator/scripts/quick_validate.py
python skill-creator/scripts/package_skill.py

# Plugin creator utilities
python plugin-creator/scripts/init_plugin.py
python plugin-creator/scripts/package_plugin.py

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

**Agentic flow core components** (shared pattern between `agentic-flow-builder/` and `prd-quality-gate-flow/`):
- `database.py` — SQLite schema, DAL, execution tracking, audit logs
- `business_rules_engine.py` — Deterministic gate evaluation (AND/OR/NOT logic, no AI variance)
- `flow_orchestrator.py` — Hierarchical execution with episodic + working memory
- `agent_registry.py` — Dynamic agent discovery, assignment, and performance tracking

**Business Rules Engine** is intentionally deterministic — gate decisions must be rule-based, not AI-inferred, to ensure consistent and auditable workflow outcomes.

## Permissions

Allowed operations are defined in `.claude/settings.local.json` (git-ignored):
- WebFetch: github.com, raw.githubusercontent.com, arxiv.org, www.anthropic.com
- Bash: curl, mkdir, git operations, chmod, cat, python, sqlite3
- WebSearch: enabled
