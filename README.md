# Claude-Plugins

Claude-Plugins is a marketplace of plugins and skills that extend [Claude Code](https://code.claude.com) with specialized workflows — from a full software delivery team to an MTG Commander deck builder, research agents, prompt engineering tools, and multi-agent workflow builders. Pick one; take them all. The road goes as far as you care to walk it.

## Installation

Add the marketplace to your Claude Code configuration (via the `/plugin` browser or your `.claude/settings.json`):

```json
{
  "plugins": [
    "https://github.com/P47Phoenix/Claude-Plugins"
  ]
}
```

Then install the plugins you want:

```
/plugin install delivery-team
/plugin install mtg-commander
/plugin install agentic-flow-builder
/plugin install prompt-engineer
/plugin install prd-quality-gate-flow
/plugin install research-agent
```

Or browse interactively with `/plugin` inside a Claude Code session.

## Plugins

| Plugin | What it does |
|--------|--------------|
| [delivery-team](delivery-team/README.md) | 11 skills spanning the full software delivery lifecycle: pipeline orchestrator, product delivery, developer (14 languages), architect (11 roles), quality, operations, UI/UX, user feedback, alias themes, and presentations |
| [mtg-commander](mtg-commander/README.md) | MTG Commander deck builder with a multi-agent pipeline: synergy-first card selection, Scryfall integration, format legality, budget enforcement, and price-goal escalation |
| [agentic-flow-builder](agentic-flow-builder/README.md) | Build dynamic multi-agent workflows using ReAcTree hierarchical decomposition, deterministic business-rules gates, and SQLite audit trails |
| [prompt-engineer](prompt-engineer/README.md) | Expert LLM prompt optimization with model-specific techniques and full prompt transparency |
| [prd-quality-gate-flow](prd-quality-gate-flow/README.md) | Production-grade PRD workflow with 7 quality gates, episodic memory, and evidence-based Stage-Gate process |
| [research-agent](research-agent/README.md) | Research agent with 5 research types (Exploratory, Descriptive, Explanatory, Evaluative, Comparative) and academic frameworks (PICO, SPICE, PECO, GRADE, ReAct) |

## What's New

Recent shipments across the marketplace:

- **Paired Constraints Primitive** — a shared `constraints.yml` that travels with the pipeline so every stage reads the same non-negotiables (budget, compliance, quality bars). See `delivery-team/skills/delivery-flow/references/constraints-model-guide.md`.
- **Configurable Architecture Board** — a multi-persona review pattern with debators convened for material architecture decisions. See `delivery-team/skills/delivery-flow/references/architecture-board-personas.md`.
- **Transformation Planning** — an optional Architect sub-flow that walks brownfield migrations through AS-IS behavioural and structural analysis, a TO-BE design, and a sequenced roadmap. See `delivery-team/skills/architect/references/transformation-planning.md`.
- **Paradigm-as-skill restructure** — the Architect now routes to paradigm sub-skills (volatility decomposition, strategic DDD) based on the problem, so only the relevant context loads.
- **MTG Commander upgrades** — adversarial challenger agents, a user-authored `.mtg-commander.yml` config for price goals and escalation, and fixes for early-adopter defects.
- **Defect sweep** — all 4 known defects closed (wizard drift, CK pricing, color identity, CI injection) plus regression guards: `.github/workflows/workflow-injection-lint.yml` and a `--skip-declarations` flag on `check_dod_constraints.py` for safe self-comparison.

## Getting Started

Three common starting paths:

- **I want to use the delivery pipeline.** Install `delivery-team`, then open [delivery-team/skills/delivery-flow/](delivery-team/skills/delivery-flow/) or ask Claude Code to "start the delivery pipeline." The setup wizard handles the rest.
- **I want to build an MTG Commander deck.** Install `mtg-commander`, then read [mtg-commander/README.md](mtg-commander/README.md) and ask Claude Code to "build a commander deck." Drop a `.mtg-commander.yml` at your repo root if you want price controls.
- **I want to contribute a plugin.** Start with [CLAUDE.md](CLAUDE.md) for repo conventions and plugin architecture, then load one of the `plugin-dev` skills (`plugin-structure`, `skill-development`, `hook-development`, `command-development`, `agent-development`, `mcp-integration`) for guided scaffolding.

## Marketplace Version

Current marketplace version: **v2.22.0** (see [`.claude-plugin/marketplace.json`](.claude-plugin/marketplace.json)).

## License

Each plugin ships its own `LICENSE.txt` — see the individual plugin directories. Please review the license before using a plugin in production.

## See Also

- [CLAUDE.md](CLAUDE.md) — deeper architecture context, plugin inventory, hooks, conventions, and contributor guidance for working inside this repo.
- [CONTRIBUTING.md](CONTRIBUTING.md) — contribution workflow, plugin structure, PR process.
- [delivery-team/skills/delivery-flow/references/getting-started.md](delivery-team/skills/delivery-flow/references/getting-started.md) — zero-to-pipeline walkthrough with quick-start wizard and skill map.

---

*"Not all those who wander are lost" — but a well-marked path does no harm.*
