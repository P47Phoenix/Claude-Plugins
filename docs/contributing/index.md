# Contributing

How to contribute to the delivery-team plugin.

## Plugin Structure

The plugin follows this directory structure:

```
delivery-team/
├── hooks/
│   ├── hooks.json          # Hook definitions
│   └── *.py                # Hook implementation scripts
├── scripts/                # Shared Python utilities
├── skills/
│   ├── delivery-flow/
│   │   ├── SKILL.md        # Pipeline orchestrator instructions
│   │   └── references/     # 18+ reference files
│   ├── developer/
│   │   ├── SKILL.md
│   │   └── references/     # Language files, patterns
│   ├── architect/
│   │   ├── SKILL.md
│   │   └── references/     # Architecture patterns, compliance
│   └── ... (11 skills total)
├── LICENSE.txt
└── README.md
```

## Required Development Skills

!!! warning "Use plugin-dev skills"
    When modifying this repo, always use the relevant plugin-dev skill:

    - Creating/modifying hooks: load `plugin-dev:hook-development` first
    - Creating/modifying skills: load `plugin-dev:skill-development` first
    - Creating/modifying plugin structure: load `plugin-dev:plugin-structure` first
    - After creating a skill: use `plugin-dev:skill-reviewer` to review it
    - After creating a plugin: use `plugin-dev:plugin-validator` to validate it

## Key Conventions

### SKILL.md Files

Each skill has a `SKILL.md` file that serves as the primary instruction set. These files contain:

- Skill metadata (frontmatter with name, description, license)
- Design principles (context isolation, role detection)
- Phase protocols (detection, sub-agent invocation)
- Task type routing tables
- Output contracts and patterns
- Reference file mappings
- User commands

### Reference Files

Reference files contain domain-specific knowledge loaded on demand. Key rules:

- Sub-agents load **only** the references relevant to their task
- Never load all reference files into a single context
- Reference files are the single source of truth for domain knowledge

### Config Schema

The single source of truth for `.delivery/config.yml` format is `delivery-flow/references/config-schema.md` (currently v2.7).

When adding new config keys, follow the extension protocol:

1. Add the key to the schema table with type, default, valid values
2. Bump the version
3. Add a wizard question if interactive
4. Add to the pipeline config table in SKILL.md
5. Add a migration note
6. Regenerate JSON schema (`python delivery-team/scripts/generate-schema.py`)
7. Update the consuming skill

### Three-Level Context Loading

All skills follow this pattern:

1. **Metadata** (always loaded) — from marketplace.json
2. **SKILL.md** (loaded when skill triggers) — main instructions
3. **Resources** (loaded on demand) — scripts, references, assets

## Pull Request Process

1. Create a feature branch following the naming convention: `feature/<issue>-<description>`
2. Make your changes using the appropriate plugin-dev skills
3. Test by actually using the modified components (dogfooding)
4. Create a PR with a clear description of changes

## Adding a New Skill

1. Create the skill directory: `delivery-team/skills/<skill-name>/`
2. Write `SKILL.md` with frontmatter, design principles, and protocols
3. Add reference files under `references/`
4. Register in the marketplace if applicable
5. Review with `plugin-dev:skill-reviewer`
6. Update this documentation site

## Adding a New Hook

1. Add the hook definition to `delivery-team/hooks/hooks.json`
2. Implement the hook script in `delivery-team/hooks/`
3. Test the hook by triggering its event type
4. Document the hook in the [Hooks Reference](../reference/hooks.md)

## Adding a New Alias Theme

1. Create `delivery-flow/references/aliases/<theme-name>.yml`
2. Map all 13 roles (or mark as partial)
3. Set personality_strength (light, moderate, full)
4. Test by setting `aliases.theme` in config and running the pipeline
