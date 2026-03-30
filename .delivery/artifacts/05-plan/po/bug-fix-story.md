# Bug Fix Story: Alias Personality Injection Is Inert (Issue #50)

**Project Type**: BUG_FIX
**Date**: 2026-03-29
**GitHub Issue**: #50
**Story Points**: S (Small)

---

## User Story

**As a** delivery-flow user who has configured `aliases.theme: lotr` in my project config,
**I want** sub-agent prompts to contain the correct LOTR character personality blocks (e.g., Gandalf as PO, Aragorn as Architect),
**So that** the alias theming system I configured actually works instead of silently falling back to "No alias active."

---

## Problem Summary

The SKILL.md orchestrator describes alias injection declaratively (Phase 0: load theme, Phase 4 Step 4: format and inject) but never includes imperative instructions to actually execute those steps. The `{alias_personality_block}` placeholder in 9 sub-agent prompt templates in `team-patterns.md` always resolves to its fallback default. The entire alias system -- 13 theme files, the alias-creator skill, config schema support -- is inert.

---

## Acceptance Criteria

### AC-1: Theme file loading during Phase 0 config load [structural]

**Given** `.delivery/config.yml` has `aliases.theme` set to a non-`business` value (e.g., `lotr`)
**When** the orchestrator executes Phase 0 (Config Load)
**Then** the orchestrator reads and parses the theme file from `references/aliases/{theme}.yml` (or `{aliases.custom_path}/{theme}.yml` for custom themes), storing the roles mapping and `personality_strength` in working memory

**Classification**: structural (verified by code inspection of SKILL.md instructions)

### AC-2: Personality block injection during Phase 4 prompt assembly [structural]

**Given** a theme has been loaded in Phase 0 with a roles mapping containing the dispatched agent's role ID
**When** the orchestrator assembles a sub-agent prompt in Phase 4 Step 4
**Then** the `{alias_personality_block}` placeholder is replaced with a formatted personality block that includes the alias name, style description, catchphrase, and example quotes -- formatted per the `personality_strength` setting (light/moderate/full)

**Classification**: structural (verified by code inspection of SKILL.md instructions)

### AC-3: Graceful fallback for missing role entries [structural]

**Given** a theme is loaded but does not contain a mapping for a particular role ID (partial theme)
**When** the orchestrator assembles a prompt for that unmapped role
**Then** the `{alias_personality_block}` placeholder is omitted entirely (no ALIAS section in the prompt), and no error is raised

**Classification**: structural (verified by code inspection of SKILL.md instructions)

### AC-4: Graceful fallback for missing or invalid theme files [structural]

**Given** `aliases.theme` is set to a value whose theme file does not exist or cannot be parsed
**When** the orchestrator executes Phase 0
**Then** the orchestrator emits a user-visible warning ("Theme file '{theme}.yml' not found, falling back to business theme"), falls back to `business` theme behavior (no personality injection), and continues pipeline execution normally

**Classification**: structural (verified by code inspection of SKILL.md instructions)

### AC-5: Business theme produces zero personality injection [structural]

**Given** `aliases.theme` is set to `business` (or is unset/defaulted)
**When** the orchestrator assembles sub-agent prompts
**Then** no `--- ALIAS ---` section appears in any dispatched prompt, and behavior is identical to pre-fix behavior

**Classification**: structural (verified by code inspection of SKILL.md instructions)

### AC-6: Personality strength levels are respected [structural]

**Given** a theme file specifies `personality_strength: light` (or `moderate` or `full`)
**When** the orchestrator formats the personality block
**Then** the block content matches the strength level:
- **light**: alias name + style only
- **moderate**: alias name + style + catchphrase
- **full**: alias name + style + catchphrase + example quotes + "Stay in character" directive

**Classification**: structural (verified by code inspection of SKILL.md instructions)

### AC-7: End-to-end dogfooding validation [empirical]

**Given** the fix has been applied to SKILL.md
**When** the delivery-flow pipeline is run with `aliases.theme: lotr` configured
**Then** dispatched sub-agent prompts contain the correct LOTR personality blocks (e.g., PO gets Gandalf personality, Architect gets Aragorn personality), observable in the `--- ALIAS ---` section of each prompt

**Classification**: empirical (requires runtime pipeline execution to verify)

---

## Test Cases

### TC-1: Theme file resolution and parsing (covers AC-1)

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Set `aliases.theme: lotr` in `.delivery/config.yml` | Config has non-business theme |
| 2 | Inspect SKILL.md Phase 0 instructions | Instructions explicitly direct reading `references/aliases/lotr.yml` |
| 3 | Verify instructions include parsing YAML roles mapping | Roles mapping and personality_strength are stored in working memory |
| 4 | Verify custom path fallback is documented | If primary path fails, `{aliases.custom_path}/{theme}.yml` is tried |

### TC-2: Placeholder substitution in prompt assembly (covers AC-2)

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Inspect SKILL.md Phase 4 Step 4 instructions | Instructions direct looking up dispatched role ID in stored theme map |
| 2 | Verify formatting instruction exists | Personality block formatted with name, style, catchphrase, examples per strength |
| 3 | Verify substitution instruction exists | `{alias_personality_block}` is replaced with the formatted block before dispatch |
| 4 | Confirm team-patterns.md is NOT modified | The `{alias_personality_block}` placeholder interface is unchanged |

### TC-3: Partial theme graceful handling (covers AC-3)

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Inspect SKILL.md instructions for role lookup | Instructions include "if role not found in theme" handling |
| 2 | Verify omission behavior | ALIAS section is omitted (not errored) for unmapped roles |
| 3 | Verify pipeline continues | No error, no stall, agent receives prompt without ALIAS block |

### TC-4: Missing theme file fallback (covers AC-4)

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Inspect SKILL.md Phase 0 for file-not-found handling | Instructions include fallback logic |
| 2 | Verify warning emission | A user-visible warning message is specified |
| 3 | Verify fallback to business | Orchestrator proceeds with no personality injection |
| 4 | Verify pipeline continues normally | No crash, no stall |

### TC-5: Business theme no-injection (covers AC-5)

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Inspect SKILL.md for business theme handling | Early-exit or skip logic present for `business` theme |
| 2 | Verify no ALIAS block generated | When theme is `business`, `{alias_personality_block}` resolves to empty/omitted |
| 3 | Compare with pre-fix behavior | Output is identical to current (broken) behavior when theme is business |

### TC-6: Personality strength formatting (covers AC-6)

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Inspect SKILL.md formatting instructions | Three distinct formatting paths exist for light/moderate/full |
| 2 | Verify light format | Contains only alias name + style |
| 3 | Verify moderate format | Contains name + style + catchphrase |
| 4 | Verify full format | Contains name + style + catchphrase + examples + stay-in-character directive |

### TC-7: Dogfooding end-to-end validation (covers AC-7)

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Configure `aliases.theme: lotr` in project config | Theme is set |
| 2 | Run delivery-flow pipeline for this bug fix (issue #50) | Pipeline executes with alias theming |
| 3 | Inspect dispatched sub-agent prompts | Each prompt's `--- ALIAS ---` section contains the correct LOTR character |
| 4 | Verify PO prompt contains Gandalf personality | Gandalf name, wise style, catchphrase present |
| 5 | Verify Architect prompt contains appropriate LOTR character | Correct character mapping from lotr.yml |
| 6 | Verify no regression on pipeline behavior | Pipeline completes all stages normally |

---

## Files to Modify

| File | Change | Constraint |
|------|--------|------------|
| `delivery-team/skills/delivery-flow/SKILL.md` | Add imperative instructions for Phase 0 theme loading + Phase 4 Step 4 placeholder substitution + fallback logic | Prompt-only fix; no new files |

## Files NOT to Modify

- `delivery-team/skills/delivery-flow/references/team-patterns.md` (placeholder interface preserved)
- `delivery-team/skills/delivery-flow/references/aliases/*.yml` (theme schema unchanged)
- `delivery-team/skills/delivery-flow/references/config-schema.md` (schema v2.3 already supports aliases)

---

## Definition of Done

- [ ] AC-1 through AC-6 verified via structural code inspection (TC-1 through TC-6)
- [ ] AC-7 verified via dogfooding run (TC-7)
- [ ] Zero changes to team-patterns.md placeholder interface
- [ ] Zero changes to alias theme YAML files
- [ ] Zero changes to config schema
- [ ] SKILL.md token count delta measured and documented
