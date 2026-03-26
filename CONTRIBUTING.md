# Contributing to Claude-Plugins

## Overview

This repository is a marketplace of Claude Code plugins and skills that extend Claude's capabilities with specialized workflows. Each plugin lives in its own top-level directory and is registered in `.claude-plugin/marketplace.json`.

**Key distinction:**
- A **skill** is a `SKILL.md` file with optional scripts/references -- it adds specialized knowledge to Claude.
- A **plugin** bundles multiple components: slash commands, agents, hooks, skills, and/or MCP servers.

## Prerequisites

- [Claude Code CLI](https://docs.anthropic.com/en/docs/claude-code) installed and authenticated
- Git
- Python 3.10+
- (Optional) Godot 4.x if working on the `godot` skill

## Getting Started

```bash
# Clone the repository
git clone https://github.com/P47Phoenix/Claude-Plugins.git
cd Claude-Plugins

# Install the plugin collection locally
claude plugin add ./

# Verify plugins load
claude skill list
```

After installation, invoke any skill with `claude skill <plugin-name>:<skill-name>` (e.g., `delivery-team:developer`).

## Plugin Structure

Every plugin must follow this directory layout:

```
<plugin-name>/              # kebab-case naming required
├── SKILL.md                # Primary skill instructions (loaded when skill triggers)
├── LICENSE.txt             # Plugin license file
├── hooks/                  # Event-driven automation (optional)
│   └── hooks.json          # Hook definitions
├── scripts/                # Python implementation scripts
├── skills/                 # Sub-skills (optional)
│   └── <skill-name>/
│       └── SKILL.md
└── references/             # Supporting documentation and examples
```

### marketplace.json Registration

Every plugin must be registered in `.claude-plugin/marketplace.json`. Add an entry to the `plugins` array:

```json
{
  "name": "my-plugin",
  "description": "Concise description of what the plugin does",
  "source": "./",
  "strict": false,
  "skills": [
    "./my-plugin/skills/my-skill"
  ]
}
```

### SKILL.md Format

Each `SKILL.md` is the primary instruction set loaded when a skill triggers. It should contain:

1. **Role definition** -- who the skill acts as
2. **Capabilities** -- what the skill can do
3. **Constraints** -- boundaries and guardrails
4. **Workflow** -- step-by-step process
5. **Output format** -- expected deliverables

### hooks.json Format

Hooks automate behavior at specific lifecycle events. Supported events:

| Event | When it fires |
|-------|---------------|
| `SessionStart` | When a Claude session begins |
| `Stop` | When a session ends |
| `PreToolUse` | Before a tool is invoked |
| `PostToolUse` | After a tool completes |
| `SubagentStop` | After a sub-agent completes |

Each hook entry requires:
- `matcher` -- glob or regex pattern for what triggers the hook
- `hooks` -- array of hook actions (`type: "command"` or `type: "prompt"`)
- `timeout` -- max execution time in seconds

Example:

```json
{
  "PostToolUse": [
    {
      "matcher": "Write|Edit",
      "hooks": [
        {
          "type": "command",
          "command": "python ${CLAUDE_PLUGIN_ROOT}/hooks/validate_gdscript.py",
          "timeout": 15
        }
      ]
    }
  ]
}
```

## Development Workflow

### Use plugin-dev skills for all plugin work

This is a hard requirement. Before modifying plugin components, load the appropriate skill:

| Task | Skill to load first |
|------|---------------------|
| Creating/modifying hooks | `plugin-dev:hook-development` |
| Creating/modifying skills | `plugin-dev:skill-development` |
| Creating/modifying plugin structure | `plugin-dev:plugin-structure` |
| Reviewing a skill after creation | `plugin-dev:skill-reviewer` |
| Validating a plugin after creation | `plugin-dev:plugin-validator` |

### Use the delivery pipeline for non-trivial changes

All work routes through the Product Owner and the delivery-flow pipeline. Plans are prompts to the team, not implementation details.

Run `delivery-team:delivery-flow` to start the pipeline. The pipeline handles:
- Auto-detecting project type (GREENFIELD, FEATURE, BUG_FIX, GAME_DEV, SPIKE, DOCS_ONLY)
- Stage routing through Idea, Refine, Design, Architect, Plan, Development, UAT
- Team DoD validation

Light stages must execute. Light means reduced depth, not skipped.

### Dogfood before shipping

Validate changes by actually using them before submitting a PR. Code review alone is not sufficient. Run the plugin, invoke the skill, trigger the hook -- confirm it works end-to-end.

## Code Standards

### Python
- Standard library only. No external dependencies.
- Use `pathlib` for all file path operations.
- Cross-platform compatible (Linux, macOS, Windows).
- Scripts run directly: `python <script>.py`

### Markdown
- Consistent heading levels (no skipping from `##` to `####`).
- Use fenced code blocks with language tags.

### YAML
- Pure YAML files only. Do not use markdown files with YAML frontmatter.
- `.yml` extension (not `.yaml`).

## Testing

There is no automated test runner. Validation is manual and skill-assisted:

1. **After creating a plugin** -- run `plugin-dev:plugin-validator` to check structure, registration, and completeness.
2. **After creating a skill** -- run `plugin-dev:skill-reviewer` to review SKILL.md quality.
3. **Hooks** -- verify hooks fire correctly by triggering the matching event and checking output. Test both the happy path and edge cases (e.g., matcher misses, timeouts).
4. **Config validation** -- run the config check hook: `python delivery-team/hooks/check_config.py`
5. **GDScript** -- if modifying `.gd` files, the PostToolUse hook runs `godot --headless --check-only` automatically.

## Pull Request Process

### Templates

Use the PR templates in `.github/PULL_REQUEST_TEMPLATE/`:
- `enhancement.md` -- for new features and improvements
- `bug_fix.md` -- for bug fixes

### Commit conventions

Use conventional commit prefixes:
- `feat:` -- new feature
- `fix:` -- bug fix
- `refactor:` -- code restructuring
- `docs:` -- documentation only
- `chore:` -- maintenance tasks

### Requirements

- Reference the related issue (e.g., `fixes #40`).
- Fill out the PR template completely (Summary, Motivation, Changes, Test plan).
- Self-improvement PRs that fix defects discovered during pipeline runs must use the `[DEFECT-FIX]` prefix in the PR title.

## Config Extension Protocol

The `.delivery/config.yml` schema is versioned. The single source of truth for the format is:

```
delivery-team/skills/delivery-flow/references/config-schema.md
```

When adding new config keys:

1. Read `config-schema.md` to understand the current schema and version.
2. Follow the extension protocol documented there (backward compatibility, version bumping, validation rules).
3. Update the schema reference document alongside your config changes.
4. Run `python delivery-team/hooks/check_config.py` to validate.

Do not add keys ad hoc. All config changes go through the schema process.

## Issue Templates

Use the issue templates in `.github/ISSUE_TEMPLATE/`:

| Template | When to use |
|----------|-------------|
| `bug_report.md` | Something is broken or behaving incorrectly |
| `feature_request.md` | Proposing a new capability or enhancement |
| `defect_pattern.md` | Documenting a recurring defect pattern discovered during pipeline runs |

Blank issues are also enabled for anything that does not fit these categories.

## License

Each plugin includes its own `LICENSE.txt` file. See individual plugin directories for license details (Apache License 2.0).
