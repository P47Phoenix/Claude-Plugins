## Idea Brief

**Project Type**: FEATURE
**Date**: 2026-03-24

### Problem Statement
The delivery team roles (Product Owner, Scrum Bag, QA Engineer, Architect, etc.) are functional but impersonal. Users want themed aliases that give each role a personality — making the team feel like characters from LOTR, Marvel, Dilbert, the Jordan-era Bulls, etc. This makes long delivery sessions more engaging and memorable.

### Target Users
- **Plugin user**: developer using the delivery-team plugin daily who wants a more fun, personalized experience
- **Team lead**: someone configuring the plugin for their team, picking a theme that fits team culture
- **Community contributor**: someone creating and sharing new alias themes

### Goals
1. Every delivery team role can have a themed alias with character-appropriate personality
2. Alias themes are selectable via config (per-project, in `.delivery/config.md`)
3. Built-in themes ship with the plugin (Business, Funny, LOTR, Marvel, MTG, Dilbert, Bulls Jordan Years, NFL, SNL, + more)
4. Users can create custom alias themes via a dedicated skill
5. Custom themes are stored per-repo so different projects can have different themes
6. The alias affects how the agent presents itself (name, personality flavor) but NOT the underlying skill behavior

### Constraints
- Aliases are cosmetic — they change names and personality flavor, not architecture or skill references
- Must be backward compatible — "Business" theme is the default, matches current role names
- Custom themes must be simple to create (a mapping file, not code)
- The system must support partial themes (only some roles aliased, rest fall back to Business)

### Initial Scope
- Alias system with theme selection in config
- 10+ built-in themes with full role mappings
- Custom alias skill for creating/editing themes
- Per-repo theme storage in `.delivery/aliases/`

### Out of Scope (initial)
- AI-generated character art/avatars
- Voice/tone changes to the actual skill output (just the name/intro changes)
- Multi-theme per session (one theme active at a time)
