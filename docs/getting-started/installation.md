# Installation

## Prerequisites

- [Claude Code CLI](https://docs.anthropic.com/en/docs/claude-code) installed and authenticated
- A project directory where you want to use the delivery pipeline

## Install the Plugin

Install the delivery-team plugin from the Claude Plugins marketplace:

```bash
claude plugin install P47Phoenix/Claude-Plugins/delivery-team
```

## Verify Installation

After installation, start a Claude Code session in your project directory and check that the plugin is available:

```
delivery-team:delivery-flow
```

The orchestrator should activate and check for existing configuration. If no `.delivery/config.yml` exists, it will launch the setup wizard.

## What Gets Installed

The plugin adds these skills to your Claude Code environment:

| Skill | Purpose |
|-------|---------|
| `delivery-team:delivery-flow` | Pipeline orchestrator (start here) |
| `delivery-team:developer` | Code implementation (14 languages) |
| `delivery-team:architect` | System design and ADRs |
| `delivery-team:quality` | Test strategy and QA |
| `delivery-team:operations` | DevOps, releases, technical writing |
| `delivery-team:product-delivery` | User stories, PRDs, retrospectives |
| `delivery-team:ui` | UX/UI design |
| `delivery-team:godot` | Godot 4.x game development |
| `delivery-team:user-feedback` | Simulated persona-based testing |
| `delivery-team:alias-creator` | Custom character themes |
| `delivery-team:presentation` | Team-collaborative presentations |

The plugin also installs 7 hooks for session management, pipeline enforcement, and quality validation. See the [Hooks Reference](../reference/hooks.md) for details.

## Next Steps

- Run through the [Quick Start](quick-start.md) to set up your first pipeline
- Browse the [Commands Reference](commands.md) for available commands
