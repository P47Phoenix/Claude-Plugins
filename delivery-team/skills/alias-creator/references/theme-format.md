# Theme File Format Reference

Complete specification for alias theme YAML files.

## File Location

- **Built-in themes**: `delivery-team/skills/delivery-flow/references/aliases/<theme>.yml`
- **Custom themes**: `.delivery/aliases/<theme>.yml` (per-repo, checked first)

Custom themes with the same name as a built-in theme override the built-in.

## Required Fields

```yaml
theme: string              # kebab-case identifier (matches filename without .yml)
display_name: string       # human-readable name shown to users
personality_strength: string  # light | moderate | full
min_roles_version: integer    # current: 13 (number of delivery team roles)
```

## Optional Fields

```yaml
partial: boolean           # true if not all 13 roles are mapped (default: false)
author: string             # who created this theme
description: string        # 1-2 sentence theme description
```

## Role Mapping

```yaml
roles:
  <role-id>:
    character: string      # REQUIRED: character/person name
    personality: string    # REQUIRED: 1-2 sentence personality description
    catchphrase: string    # OPTIONAL: signature line (use "none" if not applicable)
    style: string          # REQUIRED: free-text communication style
    examples: list[string] # OPTIONAL for light, recommended for moderate, REQUIRED for full
```

### Role IDs (all 13)

```
product-owner
scrum-master
data-analyst
developer
architect
qa-engineer
devops
release-manager
tech-writer
ux-designer
ui-designer
game-ui-designer
user-feedback
```

## Personality Strength Behavior

| Field | light | moderate | full |
|-------|-------|----------|------|
| character | Injected | Injected | Injected |
| personality | Brief mention | Full injection | Full injection |
| catchphrase | Skipped | Occasional | Regular |
| style | Skipped | Injected | Injected |
| examples | Skipped | 1 example injected | 2 examples injected |
| "Do not break character" | Not added | Not added | Added to prompt |

## Prompt Injection Template

When a sub-agent is spawned with an active theme:

### Light
```
You are [CHARACTER] ([ROLE]).
[Continue with normal skill prompt...]
```

### Moderate
```
You are [CHARACTER] ([ROLE]).
[PERSONALITY]
Communicate in a [STYLE] style while performing your [ROLE] duties.
Your expertise and output quality must not change.

Example of your voice:
- "[EXAMPLE 1]"

[Continue with normal skill prompt...]
```

### Full
```
You are [CHARACTER] ([ROLE]).
[PERSONALITY]
[CATCHPHRASE — use occasionally, not every response]
Communicate in a [STYLE] style while performing your [ROLE] duties.
Your expertise and output quality must not change — only your personality.
Do not break character. If the user says "drop character" or "be professional", revert to standard tone.

Examples of your voice:
- "[EXAMPLE 1]"
- "[EXAMPLE 2]"

[Continue with normal skill prompt...]
```

## Theme Resolution Order

1. Check `.delivery/aliases/<theme>.yml` (custom, per-repo)
2. Check `delivery-flow/references/aliases/<theme>.yml` (built-in)
3. If theme not found, fall back to `business` with a warning

## Role Fallback

If a theme doesn't map a specific role:
1. Check `business.yml` for that role
2. Use the role's default name with no personality injection
