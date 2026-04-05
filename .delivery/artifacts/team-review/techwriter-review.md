# Technical Writer Documentation Review

**Reviewer**: Bilbo (Technical Writer)
**Date**: 2026-04-04
**Scope**: delivery-team plugin documentation suite
**Verdict**: Documentation is structurally sound but has 27 actionable findings across staleness, inconsistency, and gaps.

---

## Executive Summary

The docs site has excellent structure and navigation. A new user can find their way from installation to running a pipeline in three clicks. However, today's pipeline runs (runs 10-13, presentation v1.1) introduced significant drift between source SKILL.md files and the docs site. The most critical issues are: CLAUDE.md references a stale config schema version (v2.3, should be v2.6), 13 config keys are missing from the docs config reference, and presentation type counts are inconsistent across 4 files.

---

## Findings

### CRITICAL: Source-of-Truth Drift

#### F-01: CLAUDE.md config schema version is stale
- **File**: `/var/home/meconnelly/Documents/GitHub/Claude-Plugins/CLAUDE.md`, line 124
- **Issue**: States "currently v2.3" but the actual schema is v2.6 (bumped through v2.4, v2.5, v2.6 today)
- **Fix**: Change "currently v2.3" to "currently v2.6"

#### F-02: CLAUDE.md says presentation has "4 types" -- should be 9
- **File**: `/var/home/meconnelly/Documents/GitHub/Claude-Plugins/CLAUDE.md`, line 51
- **Issue**: `4 types: Sprint Review, Feature Pitch, Stakeholder Update, Technical Deep-Dive` -- presentation SKILL.md now supports 9 types (5 added in v1.1: Investor Pitch, Roadmap, Product Demo, Onboarding, Retrospective Summary)
- **Fix**: Update to list all 9 types

#### F-03: Root README.md says presentation has "4 types, 3 output formats"
- **File**: `/var/home/meconnelly/Documents/GitHub/Claude-Plugins/README.md`, line 59 (approx)
- **Issue**: Same stale count. Also says "3 output formats" but PPTX was added (now 4 formats).
- **Fix**: Update to "9 types, 4 output formats"

#### F-04: delivery-team/README.md says "4 types, 3 output formats"
- **File**: `/var/home/meconnelly/Documents/GitHub/Claude-Plugins/delivery-team/README.md`, line 35
- **Issue**: Same staleness as F-03.
- **Fix**: Update to "9 types, 4 output formats"

#### F-05: docs/skills/index.md says "9 types" but CLAUDE.md says "4 types"
- **File**: `/var/home/meconnelly/Documents/GitHub/Claude-Plugins/docs/skills/index.md`, line 19
- **Issue**: The docs site is correct (9 types), but this creates an inconsistency with CLAUDE.md (F-02). The docs site was updated but CLAUDE.md was not.
- **Action**: Fix F-02 to resolve the inconsistency.

### CRITICAL: Missing Config Keys in Docs

#### F-06: 13 config keys present in source schema but missing from docs config reference
- **File**: `/var/home/meconnelly/Documents/GitHub/Claude-Plugins/docs/user-guide/config.md`
- **Source**: `/var/home/meconnelly/Documents/GitHub/Claude-Plugins/delivery-team/skills/delivery-flow/references/config-schema.md`
- **Missing keys** (89 in source vs 76 in docs):
  1. `pipeline.required_agent_retry_max` (added v2.0)
  2. `presentation.marp_theme` (added v2.2)
  3. `presentation.save_to_artifacts` (added v2.2)
  4. `presentation.staleness_warning_days` (added v2.2)
  5. `presentation.vocabulary_overrides` (added v2.2)
  6. `presentation.pptx_template` (added v2.6)
  7. `presentation.pptx_font` (added v2.6)
  8. `presentation.pptx_accent_color` (added v2.6)
  9. `presentation.narrative.emphasis` (added v2.4)
  10. `presentation.narrative.cutting` (added v2.4)
  11. `presentation.narrative.framing` (added v2.4)
  12. `presentation.narrative.tension` (added v2.4)
  13. `presentation.thresholds` (added v2.5, map type)
- **Fix**: Add all 13 keys to the docs config reference with type, default, valid values, and description. Group under a "Presentation (Advanced)" subsection.

### HIGH: Terminology Inconsistencies

#### F-07: "Scrum Bag" vs "Scrum Master" naming conflict
- **Source files** use "Scrum Bag": `CLAUDE.md` (line 42), `delivery-team/README.md` (line 26), `marketplace.json` (line 48), `product-delivery/SKILL.md` (throughout), `delivery-flow/SKILL.md` (lines 733, 754, 1080), `alias-creator/SKILL.md` (line 66)
- **Docs site** uses "Scrum Master" exclusively: `docs/skills/product-delivery.md`, `docs/skills/index.md`, `docs/user-guide/pipeline.md`, `docs/getting-started/commands.md`, `docs/reference/aliases.md`, `docs/skills/alias-creator.md` (line 25)
- **Impact**: A user reading the docs will see "Scrum Master" everywhere, then encounter "Scrum Bag" in actual skill output. This is confusing.
- **Fix**: Decide on ONE canonical name. If "Scrum Bag" is the intentional alias-friendly name, add a note in docs: "The Scrum Master role is referred to as 'Scrum Bag' in skill output and alias themes." If it was a typo that propagated, fix the source files.

#### F-08: Demographic overlay persona names differ between files
- **user-feedback/SKILL.md** (line 34, 147-148): `Millennial Mia`, `Gen X Xavier`, `Boomer Barbara`
- **persona-library.md** (lines 201, 206): `Millennial Mike`, `Gen X Grace`
- **config-schema.md** (line 67): `Millennial Mike`, `Gen X Grace`, `Boomer Bob`
- **setup-wizard.md** (line 270): `Millennial Mike`, `Gen X Grace`, `Boomer Bob`
- **config-schema.json** (line 529-530): `Millennial Mike`, `Gen X Grace`
- **docs/skills/user-feedback.md** (line 51): `Millennial Mia`, `Gen X Xavier`, `Boomer Barbara`
- **Impact**: Users who configure overlays by name will get errors if they use the wrong variant. The JSON schema validation will reject names that don't match `config-schema.json`.
- **Fix**: Reconcile all files to use one consistent set of names. The JSON schema and config-schema.md are the authority -- align SKILL.md, persona-library.md, and docs to match.

### HIGH: Missing Documentation

#### F-09: Architect "Prior Art Analysis" not documented in docs
- **File**: `/var/home/meconnelly/Documents/GitHub/Claude-Plugins/docs/skills/architect.md`
- **Source**: `/var/home/meconnelly/Documents/GitHub/Claude-Plugins/delivery-team/skills/architect/SKILL.md`, lines 36-80
- **Issue**: The architect SKILL.md has a detailed "Prior Art Analysis" phase (4 steps: Read and Summarize, Classify Each Element, Build On Existing Design, Deviation Protocol). The docs page has no mention of this feature.
- **Fix**: Add a "Prior Art Analysis" section to the docs page, covering the 4-step protocol and the classification table format.

#### F-10: Presentation docs page missing 5 new types' details
- **File**: `/var/home/meconnelly/Documents/GitHub/Claude-Plugins/docs/skills/presentation.md`
- **Issue**: The docs page correctly lists all 9 types in the table (line 29-33), but the source SKILL.md has much richer detail for each type that the docs page does not surface: Pipeline Auto-Detection mappings, Content Gate requirements per type, GAME_DEV vocabulary, Onboarding default audience behavior, Retrospective Summary sensitivity/disclaimer. These are user-facing behaviors that affect output.
- **Fix**: Add subsections for Pipeline Auto-Detection, Content Gate rules, and type-specific behaviors (GAME_DEV vocabulary, Onboarding defaults, Retro Summary sensitivity).

#### F-11: Presentation docs missing PPTX output format details
- **File**: `/var/home/meconnelly/Documents/GitHub/Claude-Plugins/docs/skills/presentation.md`, line 48
- **Issue**: Output Formats section lists PPTX as a bullet item but provides no detail. The source SKILL.md has extensive PPTX documentation: JSON intermediate file, `generate_pptx.py` script invocation, branding precedence (template > font > accent color), dependency checking (python-pptx), fallback behavior.
- **Fix**: Add a PPTX subsection under Output Formats with installation requirement, branding options, and fallback behavior.

#### F-12: Presentation docs missing editorial passes (Narrative Intelligence)
- **File**: `/var/home/meconnelly/Documents/GitHub/Claude-Plugins/docs/skills/presentation.md`
- **Issue**: The source SKILL.md (lines 235-308) has detailed documentation of 4 sequential editorial passes (Emphasis Selection, Information Cutting, Audience-Specific Framing, Narrative Tension) with impact signal taxonomy, cutting heuristics, framing rules by audience, tension patterns, user overrides (`no reorder`, `restore {slide}`). The docs page mentions none of this.
- **Fix**: Add an "Editorial Passes (Narrative Intelligence)" section summarizing the 4 passes, their purpose, and user override commands.

#### F-13: Presentation docs missing threshold/graceful degradation
- **File**: `/var/home/meconnelly/Documents/GitHub/Claude-Plugins/docs/skills/presentation.md`
- **Issue**: Source SKILL.md has threshold resolution, 75% warning behavior, 100% notice, and light mode + threshold interaction matrix. Docs page mentions none of this.
- **Fix**: Add a brief section on threshold behavior and degradation rules.

#### F-14: No docs page for "Feature Knowledge System"
- **Issue**: The Feature Knowledge System (FKCs, Impact Analysis Gate) is mentioned in `docs/architecture/overview.md` (lines 57-66) and `delivery-team/README.md` (line 64), but there is no dedicated reference page explaining how to use it, what an FKC looks like, or how the Impact Analysis Gate works.
- **Fix**: Create `docs/reference/feature-knowledge.md` with FKC format, Impact Analysis Gate protocol, and examples.

#### F-15: No docs page for "Session Keepalive"
- **Issue**: Session keepalive is listed in `delivery-team/README.md` (line 59) as a key feature with cross-platform support, but there is no documentation explaining what it does, how to enable/disable it, or troubleshooting.
- **Fix**: Add a section to `docs/user-guide/pipeline.md` or create `docs/reference/session-keepalive.md`.

#### F-16: No docs page for "Pipeline Analytics Dashboard"
- **Issue**: Listed in `delivery-team/README.md` (line 62) and `CLAUDE.md` (line 105) as a feature, but no documentation page exists.
- **Fix**: Create `docs/reference/analytics.md` or add a section to `docs/user-guide/pipeline.md`.

#### F-17: No docs page for "Defect Tracking"
- **Issue**: `docs/architecture/overview.md` mentions defect tracking briefly (lines 87-94), but there is no user-facing guide explaining defect rate targets, how to review defects, or how the self-improvement PR trigger works. Source: `delivery-flow/references/defect-tracking.md`.
- **Fix**: Create `docs/reference/defect-tracking.md` or add to the pipeline user guide.

### MEDIUM: Docs Config Reference Incomplete

#### F-18: Config reference example YAML is missing keys from v2.2-v2.6
- **File**: `/var/home/meconnelly/Documents/GitHub/Claude-Plugins/docs/user-guide/config.md`, lines 154-251
- **Issue**: The example config omits `save_to_artifacts`, `marp_theme`, `staleness_warning_days`, `vocabulary_overrides`, `pptx_template`, `pptx_font`, `pptx_accent_color`, `narrative.*`, `required_agent_retry_max`. These keys ARE present in the source config-schema.md template (lines 268-287).
- **Fix**: Sync the example YAML with the source schema template.

### MEDIUM: Docs-Source Mismatches

#### F-19: Quick-start wizard says "9+ questions" but getting-started.md says "10+ questions"
- **File**: `/var/home/meconnelly/Documents/GitHub/Claude-Plugins/docs/getting-started/quick-start.md`, line 7: "9+ questions"
- **File**: `/var/home/meconnelly/Documents/GitHub/Claude-Plugins/delivery-team/README.md`, line 51: "10+ question"
- **File**: `/var/home/meconnelly/Documents/GitHub/Claude-Plugins/docs/skills/delivery-flow.md`, line 35: "9+ questions"
- **Source**: `delivery-flow/references/setup-wizard.md` has 14 questions (Q1-Q14)
- **Fix**: Align all references. If the wizard asks 14 questions, say "14 questions" (or "10+ questions" if some are auto-skipped). Pick one number.

#### F-20: docs/skills/delivery-flow.md says "Setup wizard asks 10 questions" (line 33 of CLAUDE.md)
- **File**: `/var/home/meconnelly/Documents/GitHub/Claude-Plugins/CLAUDE.md`, line 98
- **Issue**: States "Setup wizard with 10 questions" but the wizard has 14 questions (Q1-Q14 in setup-wizard.md).
- **Fix**: Update to "14 questions" or "10+ questions (auto-detect + smart options)".

#### F-21: Alias creator docs page says "Scrum Master" but source says "Scrum Bag"
- **File**: `/var/home/meconnelly/Documents/GitHub/Claude-Plugins/docs/skills/alias-creator.md`, line 25
- **Source**: `/var/home/meconnelly/Documents/GitHub/Claude-Plugins/delivery-team/skills/alias-creator/SKILL.md`, line 66
- **Issue**: Source says `scrum-master | Scrum Bag | Process facilitation, retros, velocity, ceremonies`. Docs say `scrum-master | Scrum Master | Process facilitation, ceremonies`.
- **Fix**: Part of F-07 resolution. Also note the docs omit "retros, velocity" from the purpose column.

#### F-22: LOTR alias theme table in docs is incomplete
- **File**: `/var/home/meconnelly/Documents/GitHub/Claude-Plugins/docs/reference/aliases.md`, lines 27-37
- **Issue**: The LOTR example table only maps 8 of the 13 roles. Missing: Data Analyst (Elrond listed), UI Designer, Game UI Designer, User Feedback, Tech Writer. A user reading this might think themes only need 8 roles.
- **Fix**: Either show all 13 roles or add a note: "Showing 8 of 13 role mappings. See the full theme file for all roles."

### LOW: Navigation and Usability

#### F-23: docs/index.md "Quick Links" missing architecture and contributing details
- **File**: `/var/home/meconnelly/Documents/GitHub/Claude-Plugins/docs/index.md`, lines 24-28
- **Issue**: Quick Links has 4 items but does not link to the Architecture Overview or the Pipeline Stages guide. These are high-traffic pages.
- **Fix**: Add links to Architecture Overview and Pipeline Stages.

#### F-24: No docs site navigation file (mkdocs.yml or similar)
- **Issue**: The docs directory has a clear structure but no `mkdocs.yml` or equivalent config to define navigation order. This means if the docs are ever served as a static site, navigation is undefined.
- **Fix**: Consider adding a nav config file if static site generation is planned.

#### F-25: Contributing guide references "18+ reference files" for delivery-flow
- **File**: `/var/home/meconnelly/Documents/GitHub/Claude-Plugins/docs/contributing/index.md`, line 18
- **Issue**: Says "18+ reference files" but `delivery-flow/references/` actually contains 21 items (20 files + 1 directory `aliases/` + 1 directory `rules/`).
- **Fix**: Update to "20+ reference files" or remove the specific count.

#### F-26: Commands reference missing `present` command variants
- **File**: `/var/home/meconnelly/Documents/GitHub/Claude-Plugins/docs/getting-started/commands.md`, lines 87-90
- **Issue**: Only lists `present --full` and `present --light`. Source SKILL.md has additional commands: `present [type]`, `present --format [fmt]`, `present --audience [mode]`, `present --notes`, `approve`, `changes`, `abort`, `no reorder`, `restore {slide title}`, `regenerate`.
- **Fix**: Add the missing presentation commands to the reference table.

#### F-27: CLAUDE.md does not mention PPTX output format
- **File**: `/var/home/meconnelly/Documents/GitHub/Claude-Plugins/CLAUDE.md`, line 51
- **Issue**: Presentation description does not mention PPTX as an output format (added in v2.6 today).
- **Fix**: Add "PPTX" to the output format list in the presentation description.

---

## Summary Metrics

| Severity | Count | Category |
|----------|-------|----------|
| CRITICAL | 6 | Source-of-truth drift, missing config keys |
| HIGH | 9 | Terminology conflicts, missing documentation |
| MEDIUM | 4 | Config example drift, question count mismatches |
| LOW | 5 | Navigation gaps, incomplete command reference |
| **Total** | **27** | |

## Recommended Priority

1. **Immediate** (before next pipeline run): F-01, F-02, F-03, F-04, F-06 -- these cause user confusion right now
2. **This sprint**: F-07 (terminology decision), F-08 (persona names), F-09 through F-13 (missing docs for features already shipped)
3. **Next sprint**: F-14 through F-17 (new reference pages), F-18 through F-22 (medium fixes)
4. **Backlog**: F-23 through F-27 (navigation and polish)

---

*"I think I'm quite ready for another documentation adventure." -- but this one needs some tidying up at the Shire before we set out again.*
