# Alias Themes

The delivery team supports 13 built-in character themes that inject personality into agent responses.

## Built-In Themes

| Theme | Display Name | Personality Strength | Description |
|-------|-------------|---------------------|-------------|
| `business` | Business (default) | none | Professional tone, no personality injection |
| `lotr` | Lord of the Rings | full | Middle-earth characters (Gandalf as PO, Gimli as Developer, Legolas as QA) |
| `star-wars` | Star Wars | full | Star Wars characters across the galaxy |
| `mandalorian` | The Mandalorian | full | Characters from the Mandalorian series |
| `marvel` | Marvel | full | Marvel universe heroes and characters |
| `the-office` | The Office | full | Dunder Mifflin characters |
| `breaking-bad` | Breaking Bad | full | Characters from Breaking Bad |
| `dilbert` | Dilbert | full | Dilbert workplace comic characters |
| `funny` | Funny | full | Comedic personalities |
| `snl` | Saturday Night Live | full | SNL characters and performers |
| `bulls-jordan` | Chicago Bulls (Jordan Era) | full | 1990s Bulls dynasty players |
| `nfl` | NFL | full | Football legends |
| `mtg` | Magic: The Gathering | full | Planeswalkers and MTG characters |

## Lord of the Rings Theme (Example)

The LOTR theme maps delivery team roles to Middle-earth characters:

| Role | Character | Style | Catchphrase |
|------|-----------|-------|-------------|
| Product Owner | Gandalf | Wise | "A product owner is never late, nor early. They prioritize precisely when they mean to." |
| Scrum Master | Aragorn | Warm | "I do not know what strength is in my backlog, but I swear to you I will not let the sprint fall." |
| Data Analyst | Elrond | Formal | "I was there three thousand sprints ago, when the metrics last failed." |
| Developer | Gimli | Blunt | "And my code!" |
| Architect | Celebrimbor | Formal | "Let us forge something that will endure beyond the ages." |
| QA Engineer | Legolas | Precise | "That bug still only counts as one." |
| DevOps | Samwise Gamgee | Warm | "I can't deploy the feature for you, Mr. Frodo, but I can carry the pipeline." |
| Release Manager | Frodo | Wise | "I will ship the release, though I do not know the way." |

## How Themes Are Applied

When a non-business theme is active, the orchestrator injects personality into agent prompts based on the `personality_strength` setting:

| Level | Injected Content |
|-------|-----------------|
| **light** | Character name + personality description |
| **moderate** | + communication style + one example voice line |
| **full** | + catchphrase + two examples + "stay in character" instruction |

Theme personality appears in:

- **Agent responses** — sub-agents speak in character
- **Stage announcements** — orchestrator references character names
- **Checkpoint summaries** — quotes from agent artifacts

Theme personality **never** appears in:

- Pipeline state files (`.delivery/state.md`)
- Stage summary files
- DoD validator prompts
- Signal blocks (STATUS/ARTIFACT/SUMMARY)

## Activating a Theme

Set the theme in `.delivery/config.yml`:

```yaml
aliases:
  theme: lotr
```

Or change it to any built-in theme name from the table above.

## Custom Themes

Create custom themes using the [Alias Creator](../skills/alias-creator.md) skill. Custom themes are stored in `.delivery/aliases/` (configurable via `aliases.custom_path`).

### Theme File Location

1. Built-in themes: `delivery-flow/references/aliases/{theme}.yml`
2. Custom themes: `{aliases.custom_path}/{theme}.yml` (default: `.delivery/aliases/`)
3. If not found in either location, falls back to `business` (no personality)

### Creating a Custom Theme

Say "create a theme" to trigger the alias-creator skill. You can:

- **Interactive**: Step through each of the 13 roles
- **Quick**: Provide a concept (e.g., "Harry Potter") and get auto-generated mappings
- **Partial**: Map only some roles — unmapped roles fall back to Business

See the [Alias Creator skill](../skills/alias-creator.md) for full details.
