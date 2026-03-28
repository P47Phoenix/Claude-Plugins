# Stage 7: Documentation

**Feature**: Clean Code Foundational Standards
**Date**: 2026-03-27
**Author**: Technical Writer (delivery-team)

---

## Part 1: Release Notes

### Clean Code Foundational Standards -- v2.3

**Release Date**: 2026-03-27

#### What's New

- **Foundational clean code loading**: A language-agnostic clean code reference (10 sections covering Meaningful Names, Functions, Comments, Formatting, Error Handling, Boundaries, Unit Tests, Classes, Emergent Design, and Code Smells) now loads automatically on every developer and Godot sub-agent task. No opt-in required. Loading order is: Language reference, then Clean code, then Conditional patterns (OOP/FP/Frontend/Nx).

- **Code review enforcement**: PR reviews via the code-reviewer and code-simplifier tools now check code against clean code principles using a condensed pass/fail checklist. Enforcement mode is configurable: `block` (default) prevents review from passing when violations are found; `warn` reports violations but allows review to pass. Violation messages cite the specific principle violated and reference the config key to change enforcement level.

- **Configurable clean code guide**: Teams can point to their own coding standards file via the `tech_stack.clean_code_guide` config key. Custom guides fully replace the default (no merging). The config check hook validates the custom guide path exists at session start and warns on files exceeding 4000 tokens.

- **Scaffold command**: A new `coding-standards` task type in the developer skill generates a starter template at `.delivery/standards/coding-standards.md` with all 10 sections and customization placeholders. Post-generation output instructs the user to set `tech_stack.clean_code_guide` to the generated file path.

#### Config Changes

Two new keys added under `tech_stack` in `.delivery/config.yml` (schema v2.3):

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| `tech_stack.clean_code_guide` | string | `""` (uses built-in default) | Path to a custom clean code standards file. When set, replaces the built-in `clean-code.md` entirely. |
| `tech_stack.clean_code_enforcement` | string | `"block"` | Enforcement level for code review. Valid values: `block`, `warn`. |

Config schema version bumped from v2.2 to v2.3.

#### Migration Notes

- **No breaking changes.** Existing configurations without the new keys continue to work with default behavior (built-in guide, block enforcement).
- Auto-upgrade: configs on v2.2 are forward-compatible. The new keys are optional and default-safe.
- No manual migration steps required.

#### Known Issues

| Issue | Description | Status |
|-------|-------------|--------|
| [#50](https://github.com/P47Phoenix/Claude-Plugins/issues/50) | Alias injection bug -- alias-creator theme injection may produce malformed output in certain edge cases | Open, pre-existing, not in scope for this release |

---

## Part 2: Documentation Updates

The following files require updates to reflect the Clean Code Foundational Standards feature.

### 1. CLAUDE.md

**File**: `/var/home/meconnelly/Documents/GitHub/Claude-Plugins/CLAUDE.md`

**Change**: Update the developer skill description in the Available Plugins table to mention clean code foundational loading.

**Current** (line in delivery-team skills table):
```
| `developer/` | 14 languages (Python, TypeScript, JavaScript, Go, Rust, C#, Java, SQL, Bash, R, F#, Elixir, Haskell, Scala) + OOP + FP + Frontend + Nx monorepo (paradigm-aware pattern loading from config) |
```

**Updated**:
```
| `developer/` | 14 languages (Python, TypeScript, JavaScript, Go, Rust, C#, Java, SQL, Bash, R, F#, Elixir, Haskell, Scala) + OOP + FP + Frontend + Nx monorepo (paradigm-aware pattern loading from config) + foundational clean code standards (always-on, configurable guide) |
```

**Additional change**: Add a note to the Godot skill entry:
```
| `godot/` | Godot 4.x game dev (GDScript, C#, scenes, signals, validation) + foundational clean code standards |
```

**Additional change**: In the "Config schema" bullet under Key Conventions, update:
> The single source of truth for `.delivery/config.yml` format is `delivery-flow/references/config-schema.md` (currently v2.3).

### 2. marketplace.json

**File**: `/var/home/meconnelly/Documents/GitHub/Claude-Plugins/.claude-plugin/marketplace.json`

**Change**: No version bump required at this time. The marketplace version (`2.8.0`) tracks the overall plugin collection, not individual config schema versions. A version bump would be appropriate when the full feature ships and is merged to main. If the team decides to bump, increment to `2.9.0`.

### 3. delivery-team/README.md

**File**: `/var/home/meconnelly/Documents/GitHub/Claude-Plugins/delivery-team/README.md`

**Change**: Update the developer and godot skill descriptions in the Skills table.

**Current developer row**:
```
| **developer** | 14 languages + OOP + FP + Frontend + Nx | Code implementation with language context isolation and paradigm-aware pattern loading |
```

**Updated developer row**:
```
| **developer** | 14 languages + OOP + FP + Frontend + Nx + Clean Code | Code implementation with language context isolation, paradigm-aware pattern loading, and foundational clean code standards |
```

**Current godot row**:
```
| **godot** | GDScript, C#, Scenes, Signals | Godot 4.x game dev with headless validation and defect prevention |
```

**Updated godot row**:
```
| **godot** | GDScript, C#, Scenes, Signals, Clean Code | Godot 4.x game dev with headless validation, defect prevention, and clean code standards |
```

### 4. config-schema.md (Already Updated)

**File**: `delivery-team/skills/delivery-flow/references/config-schema.md`

**Status**: Already updated during development (Sprint 2, Story 2.3). No further changes needed. Contains v2.3 schema with both new keys documented.

---

## Files Summary

| File | Action | Priority |
|------|--------|----------|
| `CLAUDE.md` | Update developer + godot skill descriptions, config schema version note | P0 |
| `delivery-team/README.md` | Update developer + godot rows in Skills table | P0 |
| `config-schema.md` | Already updated | Done |
| `marketplace.json` | Defer version bump to merge time | P1 |
