---
name: alias-creator
description: This skill should be used when the user wants to create a custom agent alias theme, edit an existing theme, preview theme mappings, or manage alias configurations. Triggers on phrases like "create a theme", "new alias theme", "custom theme", "edit theme", "preview theme", "show themes", "list themes", "alias", "character theme", "personality theme", "add a theme".
license: Apache License 2.0 - See repository LICENSE file
---

# Alias Theme Creator

Create, edit, preview, and manage agent alias themes for the delivery team pipeline.

## What Are Alias Themes?

Alias themes give each delivery team role a themed character name and personality. When a theme is active, every sub-agent speaks in character — Gandalf gives wise product advice, Gimli builds code with directness, Legolas catches bugs with elven precision.

Built-in themes are in `delivery-flow/references/aliases/`. Custom themes are stored per-repo in `.delivery/aliases/`.

---

## Creating a Custom Theme

### Interactive Creation

Walk the user through creating a theme step by step:

1. **Theme identity**: Ask for theme name (kebab-case), display name, and personality strength (light/moderate/full)
2. **For each of the 13 roles**, ask:
   - Character name
   - Personality description (1-2 sentences)
   - Catchphrase (or "none")
   - Communication style (free text)
   - 2 example voice lines (how this character talks about delivery work)
3. **Validate**: All 13 roles mapped, all required fields present
4. **Write**: Save to `.delivery/aliases/<theme-name>.yml`

### Quick Creation from Description

If the user provides a theme concept (e.g., "Harry Potter theme"), generate all 13 role mappings automatically:

1. Map each role to the best-fitting character based on traits
2. Write personality notes that match the character's known behavior
3. Generate catchphrases adapted from source material
4. Present the full mapping for user review before saving
5. User can edit individual roles before finalizing

### Partial Themes

Themes don't need all 13 roles. Unmapped roles fall back to the Business theme. Mark partial themes:

```yaml
theme: my-partial-theme
display_name: "My Partial Theme"
personality_strength: moderate
min_roles_version: 13
partial: true  # indicates not all roles are mapped
```

---

## The 13 Delivery Team Roles

Every theme maps these roles:

| Role ID | Role Name | What They Do |
|---------|-----------|-------------|
| `product-owner` | Product Owner | Business value, user stories, PRDs, backlogs |
| `scrum-master` | Scrum Bag | Process facilitation, retros, velocity, ceremonies |
| `data-analyst` | Data Analyst | Metrics, analytics, A/B testing, dashboards |
| `developer` | Developer | Code implementation across 14 languages |
| `architect` | Architect | System design, ADRs, decomposition, C4 models |
| `qa-engineer` | QA Engineer | Test strategy, test cases, quality metrics |
| `devops` | DevOps Engineer | CI/CD, deployment, infrastructure, monitoring |
| `release-manager` | Release Manager | Release planning, versioning, rollback, feature flags |
| `tech-writer` | Technical Writer | API docs, user guides, runbooks, release notes |
| `ux-designer` | UX Designer | User flows, wireframes, usability, research |
| `ui-designer` | UI Designer | Design systems, components, accessibility, interactions |
| `game-ui-designer` | Game UI Designer | HUD, menus, inventory UI, game accessibility |
| `user-feedback` | User Feedback | Feedback facilitator (personas keep their own identities) |

**Note**: The `user-feedback` role alias applies only to the feedback facilitator, not the 20+ individual test personas.

---

## Theme File Format

```yaml
theme: my-theme                    # kebab-case, used in config
display_name: "My Custom Theme"    # human-readable name
personality_strength: moderate     # light | moderate | full
min_roles_version: 13              # current number of roles

roles:
  product-owner:
    character: "Character Name"
    personality: "1-2 sentence personality description."
    catchphrase: "Signature line or none"
    style: "communication style, free text"
    examples:
      - "Example of how this character talks about delivery work"
      - "Another example showing their voice"

  scrum-master:
    character: "..."
    personality: "..."
    catchphrase: "..."
    style: "..."
    examples:
      - "..."
      - "..."

  # ... repeat for all 13 roles
```

### Personality Strength

| Level | What It Means | Prompt Impact |
|-------|-------------|--------------|
| **light** | Name + occasional flavor | Character name used, personality note minimal, no examples injected |
| **moderate** | Consistent voice | Full personality note + style + 1 example injected |
| **full** | Deep character commitment | Full personality + catchphrase + 2 examples + "do not break character" |

### Style Examples

Style is free text. Good examples:
- "wise, measured, occasionally cryptic"
- "blunt, direct, uses construction metaphors"
- "sardonic, dry humor, references coffee addiction"
- "enthusiastic, uses exclamation points, sports metaphors"
- "calm, methodical, speaks in numbered steps"

---

## Theme Management Commands

| Command | Action |
|---------|--------|
| `create theme` | Start interactive theme creation |
| `create theme from [concept]` | Auto-generate theme from a concept description |
| `edit theme [name]` | Edit an existing custom theme |
| `preview theme [name]` | Show all 13 role mappings for a theme |
| `list themes` | List all available themes (built-in + custom) |
| `validate theme [name]` | Check theme for completeness and quality |
| `delete theme [name]` | Delete a custom theme (cannot delete built-ins) |

---

## Built-In Themes

These ship with the delivery-team plugin (in `delivery-flow/references/aliases/`):

| Theme | Display Name | Vibe |
|-------|-------------|------|
| `business` | Business | Professional defaults (current behavior) |
| `funny` | Funny | Comedy aliases (Scrum Bag, Code Monkey, Bug Hunter) |
| `lotr` | Lord of the Rings | Fellowship of the Delivery Team |
| `marvel` | Marvel (MCU) | Avengers assemble for shipping |
| `mtg` | Magic: The Gathering | Planeswalkers of the pipeline |
| `dilbert` | Dilbert | Office comic dysfunction |
| `bulls-jordan` | Chicago Bulls 1991-1998 | Dynasty-era basketball legends |
| `nfl` | NFL All-Time Greats | Football hall of famers |
| `snl` | Saturday Night Live | Live from the sprint review |
| `star-wars` | Star Wars | A long time ago in a codebase far away |
| `mandalorian` | The Mandalorian | This is the Way (of delivering software) |
| `breaking-bad` | Breaking Bad | Say my name (it's in the config) |
| `the-office` | The Office | Dunder Mifflin delivery team |

To activate: set `aliases.theme: lotr` in `.delivery/config.yml`.

---

## Validation Checklist

When validating a theme (built-in or custom):

- [ ] All 13 role IDs present (or marked as `partial: true`)
- [ ] Every mapped role has: character, personality, style (catchphrase and examples optional for light themes)
- [ ] No role mapped to a non-sentient object (must be a character/person)
- [ ] Character-role fit makes sense (character traits align with role function)
- [ ] For `full` personality strength: examples must be present for every role
- [ ] `min_roles_version` matches current role count (13)
- [ ] Theme name is kebab-case
- [ ] `user-feedback` note about facilitator-only applies

---

## References

- `references/theme-format.md` — Detailed theme file format documentation with field-by-field spec
