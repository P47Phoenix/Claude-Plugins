## Architecture: Agent Alias Themes

**Role**: Solution Architect
**Task**: design (light)

### Context & Drivers
Add themed aliases to all delivery team roles. Themes are cosmetic — they change names, personality, and communication style but not skill behavior or reference loading. Must integrate with existing config system (v1.3) and work across all 9 skills.

### Architecture Decision

**Approach**: Reference-based theme system (no code, no scripts)

Each theme is a YAML file with role mappings. When a sub-agent is spawned, the orchestrator (delivery-flow) or the skill itself reads the active theme, finds the role mapping, and prepends the personality injection to the sub-agent prompt.

### Component Design

```
.delivery/config.md          # aliases.theme setting (e.g., "lotr")
    |
    v
delivery-team/skills/
├── delivery-flow/
│   ├── SKILL.md              # Reads theme on pipeline start, passes to stages
│   └── references/
│       ├── aliases/           # Built-in theme files
│       │   ├── business.yml
│       │   ├── funny.yml
│       │   ├── lotr.yml
│       │   ├── marvel.yml
│       │   ├── mtg.yml
│       │   ├── dilbert.yml
│       │   ├── bulls-jordan.yml
│       │   ├── nfl.yml
│       │   ├── snl.yml
│       │   ├── star-wars.yml
│       │   ├── mandalorian.yml
│       │   ├── breaking-bad.yml
│       │   └── the-office.yml
│       └── config-schema.md  # aliases.* config keys
├── alias-creator/            # New skill for creating custom themes
│   ├── SKILL.md
│   └── references/
│       └── theme-format.md   # Theme file format documentation
└── [each skill]/
    └── SKILL.md              # Each skill reads alias for its role(s)

.delivery/aliases/            # Custom per-repo themes (user-created)
└── my-custom-theme.yml
```

### Theme File Format (YAML)

```yaml
theme: lotr
display_name: "Lord of the Rings"
personality_strength: moderate  # light | moderate | full
min_roles_version: 13

roles:
  product-owner:
    character: "Gandalf"
    personality: "Wise guide who sees the big picture. Speaks with gravitas and occasional humor."
    catchphrase: "A product owner is never late, nor early. They prioritize precisely when they mean to."
    style: "wise, measured, occasionally cryptic"
    examples:
      - "This story carries great weight. Let us ensure its acceptance criteria are forged true."
      - "I see the path through this backlog, though it winds through dark places."

  scrum-master:
    character: "Aragorn"
    personality: "Servant leader who rallies the team. Leads from the front but empowers others."
    catchphrase: "For the sprint."
    style: "noble, direct, encouraging"
    examples:
      - "Our velocity tells a tale of growing strength. Let us ride on."
      - "The impediment before us can be overcome. Together."

  # ... all 13 roles
```

### Theme Loading Flow

1. **Pipeline start (Phase 0)**: Read `aliases.theme` from `.delivery/config.md`
2. **Theme resolution**: Check `.delivery/aliases/<theme>.yml` first (custom), then `delivery-flow/references/aliases/<theme>.yml` (built-in). Custom overrides built-in.
3. **Cache**: Load theme once, store in working context for the pipeline run
4. **Per-stage injection**: When spawning a sub-agent, look up the role in the cached theme. Prepend personality block to the sub-agent prompt.
5. **Fallback**: If role not in theme, use `business.yml` mapping for that role

### Personality Injection Point

Each skill's sub-agent prompt template currently starts with:
```
You are an expert [ROLE]. Apply these [patterns/practices] to everything you produce:
```

With aliases active, it becomes:
```
You are [CHARACTER NAME] ([ROLE]).
[PERSONALITY NOTE]
[CATCHPHRASE — use occasionally, not every response]
Communicate in a [STYLE] style while performing your [ROLE] duties.
Your expertise and output quality must not change — only your personality and communication style.
Do not break character. If the user says "drop character" or "be professional", revert to standard professional tone.

[Few-shot examples if personality_strength is moderate or full:]
Example of your voice:
- "[EXAMPLE 1]"
- "[EXAMPLE 2]"

Now apply these [patterns/practices]:
```

### Config Schema Update (v1.4)

```yaml
aliases:
  theme: business       # active theme name
  custom_path: .delivery/aliases/  # where custom themes live
```

### Trade-Off Analysis

| Option | Pros | Cons | Decision |
|--------|------|------|----------|
| YAML theme files | Machine-parseable, simple to create | Less readable than markdown | CHOSEN — simpler parsing, config.md is already YAML |
| Markdown theme files | Human-readable | Hard to parse structured data | Rejected |
| Theme in config.md | One file | Config would be massive with 13 role mappings | Rejected |
| Inline in SKILL.md | No extra files | Bloats every skill, can't customize | Rejected |

### Risks & Mitigations

| Risk | Impact | Mitigation |
|------|--------|-----------|
| Personality degrades skill output quality | High | DoD validators check same criteria regardless of theme |
| Theme loading slows pipeline | Low | Load once, cache for run |
| Custom themes with missing roles | Medium | Fallback to Business for unmapped roles |

### Follow-Up
- Create the 13 built-in theme YAML files
- Create alias-creator skill
- Update config-schema.md to v1.4
- Update each skill's sub-agent prompt template to support personality injection
- Add `aliases.theme` to setup wizard
