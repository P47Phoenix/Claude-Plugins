# Alias Creator

**Invocation**: `delivery-team:alias-creator`

Create, edit, preview, and manage agent alias themes for the delivery team pipeline.

## What Are Alias Themes?

Alias themes give each delivery team role a themed character name and personality. When a theme is active, every sub-agent speaks in character — Gandalf gives wise product advice, Gimli builds code with directness, Legolas catches bugs with elven precision.

Built-in themes are stored in `delivery-flow/references/aliases/`. Custom themes go in `.delivery/aliases/`.

## How to Trigger

- "create a theme", "new alias theme", "custom theme"
- "edit theme", "preview theme", "show themes", "list themes"

## The 13 Delivery Team Roles

Every theme maps these roles:

| Role ID | Role Name | Purpose |
|---------|-----------|---------|
| `product-owner` | Product Owner | Business value, stories, PRDs |
| `scrum-master` | Scrum Master | Process facilitation, ceremonies |
| `data-analyst` | Data Analyst | Metrics, analytics, experiments |
| `developer` | Developer | Code implementation |
| `architect` | Architect | System design, ADRs |
| `qa-engineer` | QA Engineer | Test strategy, quality |
| `devops` | DevOps Engineer | CI/CD, infrastructure |
| `release-manager` | Release Manager | Release planning, versioning |
| `tech-writer` | Technical Writer | Documentation |
| `ux-designer` | UX Designer | User flows, research |
| `ui-designer` | UI Designer | Design systems, components |
| `game-ui-designer` | Game UI Designer | HUD, game menus |
| `user-feedback` | User Feedback | Feedback facilitator |

## Creating Themes

### Interactive Creation

Walk through creating a theme step by step — theme identity, then character mapping for each of the 13 roles with personality, catchphrase, style, and example voice lines.

### Quick Creation

Provide a theme concept (e.g., "Harry Potter theme") and all 13 role mappings are generated automatically. Review and edit before saving.

### Partial Themes

Themes do not need all 13 roles. Unmapped roles fall back to the Business theme (professional, no personality injection).

## Personality Strength

| Level | What Gets Injected |
|-------|-------------------|
| **light** | Character name and personality only |
| **moderate** | Name, personality, style, and one example |
| **full** | Name, personality, style, catchphrase, two examples, "stay in character" |

## Theme File Format

```yaml
theme: my-theme
display_name: "My Custom Theme"
personality_strength: moderate
min_roles_version: 13

roles:
  product-owner:
    character: "Character Name"
    personality: "1-2 sentence personality description."
    catchphrase: "Signature line or none"
    style: "communication style"
    examples:
      - "Example of how this character talks"
      - "Another example showing their voice"
```

## Configuration

Set the active theme in `.delivery/config.yml`:

```yaml
aliases:
  theme: lotr           # built-in theme name
  custom_path: .delivery/aliases/  # custom theme directory
```

See [Alias Themes Reference](../reference/aliases.md) for all 13 built-in themes.
