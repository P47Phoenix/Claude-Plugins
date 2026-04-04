# QA DoD Review -- Presentation Skill v1.1

**Pipeline**: run-2026-04-04-w7m3
**Reviewer**: Legolas (QA Engineer)
**Date**: 2026-04-04
**Artifacts Reviewed**: SKILL.md, slide-structure.md, narrative-patterns.md, generate_pptx.py, config-schema.md

> "Every arrow has been inspected, every shaft true. Thirty-six acceptance criteria examined -- not one found wanting. The empirical tests await the proving ground, but the craft is sound."

---

## Review Summary

| Story | Structural ACs | Empirical ACs | Verdict |
|-------|---------------|---------------|---------|
| US-01 | 6/6 PASS | 1/1 CODE_COMPLETE | PASS |
| US-02 | 2/2 PASS | 1/1 CODE_COMPLETE | PASS |
| US-03 | 5/5 PASS | 1/1 CODE_COMPLETE | PASS |
| US-04 | 6/6 PASS | 1/1 CODE_COMPLETE | PASS |
| US-05 | 6/6 PASS | 1/1 CODE_COMPLETE | PASS |
| US-06 | 2/2 PASS | 1/1 CODE_COMPLETE | PASS |
| US-07 | 7/7 PASS | 1/1 CODE_COMPLETE | PASS |
| US-08 | 2/2 PASS | 1/1 CODE_COMPLETE | PASS |

**Overall**: CODE_COMPLETE -- all 36 structural ACs verified by file inspection, all 8 empirical ACs classified as CODE_COMPLETE (require dogfooding to close).

---

## US-01: Add 5 New Presentation Type Definitions

### AC-01 -- Investor Pitch type detection: PASS

- SKILL.md type detection table (line 29) contains "Investor Pitch" with keywords: "investor pitch", "fundraising deck", "pitch to investors"
- Pipeline auto-detection mapping for `audience: investor` at UAT stage present (line 44)

### AC-02 -- Investor Pitch content gate, narrative, slides: PASS

- Content Gate (SKILL.md line 166): requires idea brief or PRD, traction/metrics data; enhances with competitive analysis, financial projections, team bios
- Traction-Opportunity-Ask framework defined in narrative-patterns.md (lines 57-67) and mapped to Investor Pitch in the Default Framework table (line 138)
- Slide sequence in slide-structure.md (lines 159-168): 9-slide sequence matches AC spec exactly (Title, Traction/Problem Validation, Market Opportunity, Solution/Product, Business Model, Metrics/Traction Proof, Team optional, The Ask, CTA)

### AC-03 -- Roadmap type: PASS

- Keywords in SKILL.md type detection table: "roadmap", "quarterly plan", "what's coming next" (line 30)
- Content Gate (line 168): requires sprint plan or backlog, pipeline state; enhances with architecture roadmap, risk register, resource allocation
- Now-Next-Later framework in narrative-patterns.md (lines 69-82) with timeline slides as structural backbone, position-locked during narrative passes
- Slide sequence in slide-structure.md (lines 171-181): 8 slides including Now/Next/Later locked positions, Dependencies/Risks, Timeline Overview

### AC-04 -- Product Demo with DEMO placeholders and GAME_DEV: PASS

- Keywords in SKILL.md: "product demo", "feature demo", "show what we built", "demo for publisher" (line 31)
- Content Gate (line 167): requires at least 1 feature artifact; enhances with screenshots, user feedback, metrics
- Hook-Show-Impact framework in narrative-patterns.md (lines 84-97) with GAME_DEV variant instructions
- Slide sequence in slide-structure.md (lines 183-197): includes Demo/Screenshot slides with `[DEMO]` placeholder conventions, timing, fallback notes, and GAME_DEV vocabulary variant

### AC-05 -- Onboarding with technical default audience: PASS

- Keywords in SKILL.md: "onboarding", "project handoff", "team orientation", "getting started" (line 32)
- Content Gate (line 169): requires architecture overview or system documentation, at least 1 ADR or design decision doc; enhances with team topology, dev environment setup, glossary
- Context-Landscape-Pathways framework in narrative-patterns.md (lines 99-112)
- Slide sequence in slide-structure.md (lines 199-207): 7 slides matching AC spec
- Default audience mode "technical" documented in SKILL.md (lines 107-109) -- explicitly overrides global `presentation.default_audience` for this type

### AC-06 -- Retrospective Summary with sensitivity filter and disclaimer: PASS

- Keywords in SKILL.md: "retro summary", "retrospective presentation", "what we learned" (line 33)
- Content Gate (line 170): requires retrospective notes or action items; enhances with velocity trends, defect data, previous retro actions
- Celebrate-Learn-Commit framework in narrative-patterns.md (lines 114-128)
- Sensitivity filter rules documented in narrative-patterns.md (lines 275-300): active for executive/client-facing, inactive for technical/casual, with specific rules for individual feedback, named contributors, challenges, interpersonal friction, failure attribution, and action item owners
- Disclaimer text in SKILL.md (lines 113-115): exact text matches AC spec, always displayed regardless of audience

### AC-07 -- End-to-end dogfooding: CODE_COMPLETE

Empirical AC -- requires dogfooding runs with real pipeline artifacts for all 5 new types. Structural foundation is complete.

---

## US-02: Update Error Handling and Content Gate for New Types

### AC-01 -- New types do not trigger "Unknown type" error: PASS

- All 5 new types appear in the type detection table (SKILL.md lines 24-33) with keywords, pipeline auto-detection, and Content Gate configurations. None appear as error cases.

### AC-02 -- Unsupported type error lists all 9 types: PASS

- Error handling table (SKILL.md line 471) lists exactly 9 types: Sprint Review, Feature Pitch, Stakeholder Update, Technical Deep-Dive, Investor Pitch, Roadmap, Product Demo, Onboarding, Retrospective Summary

### AC-03 -- Error handling dogfooding: CODE_COMPLETE

Empirical AC -- requires dogfooding with unsupported type input.

---

## US-03: Implement python-pptx Generation Script

### AC-01 -- Script produces valid PPTX from JSON intermediate: PASS

- `generate_pptx.py` exists at `delivery-team/skills/presentation/scripts/` (477 lines)
- Script reads JSON, validates structure, creates Presentation object, populates slides, saves to output path
- Produces standard .pptx format via python-pptx library

### AC-02 -- Each JSON slide maps to exactly one PowerPoint slide: PASS

- Line 389: iterates `slides_data` list, calls `prs.slides.add_slide(layout)` once per JSON slide entry
- Titles set from `slide_data.get("title", "")`, body from `slide_data.get("body", [])`
- 1:1 mapping guaranteed by single-pass iteration

### AC-03 -- Slide layout mapping is correct: PASS

- `LAYOUT_MAP` (lines 70-78): `title` -> "Title Slide" (index 0), all others -> "Title and Content" (index 1)
- `resolve_layout` function (lines 87-109): name-first, index-fallback strategy per FR-08
- `populate_title_slide` (lines 137-160): sets title and subtitle from body items
- `populate_content_slide` (lines 229-302): handles content, metrics, comparison (table), cta (numbered), timeline (table), architecture (bullets + Mermaid fallback note)
- Comparison renders as table via `add_table_to_slide`
- CTA renders numbered list: `f"{i + 1}. {item}"`

### AC-04 -- Template support with branding precedence: PASS

- `--template`, `--font`, `--accent-color` CLI arguments (lines 419-457)
- Template loading (lines 370-378): uses `pptx.Presentation(template_path)` when template provided
- Defaults: `DEFAULT_FONT = "Calibri"`, `DEFAULT_ACCENT_COLOR = "#2d5aa0"` (lines 64-65)
- Font/color applied within template via `set_text_frame_font` and per-slide population functions

### AC-05 -- Graceful dependency error: PASS

- Import guard (lines 41-53): `try/except ImportError` at top of file, prints error message to stderr, exits with `sys.exit(1)`
- Error message: "Error: python-pptx is required. Install with: pip install python-pptx"
- No unhandled traceback -- the guard catches before any other imports

### AC-06 -- PPTX generation dogfooding: CODE_COMPLETE

Empirical AC -- requires running script with real composed-draft.json and opening output in LibreOffice.

---

## US-04: Add PPTX Format Config, Help Text, and Fallback

### AC-01 -- PPTX is a recognized output format: PASS

- SKILL.md Output Format Specifications section (lines 439-449): PPTX documented with JSON intermediate description
- `present --format pptx` in user commands table (line 489) alongside structured-markdown, marp, paste-ready
- Output path pattern: `.delivery/artifacts/presentations/{type}-{date}.pptx` (line 381)

### AC-02 -- Config default format supports PPTX: PASS

- SKILL.md config table (line 520): `presentation.default_format` accepts `pptx` as valid value
- config-schema.md updated to accept "pptx" (version 2.6 changelog)

### AC-03 -- Fallback to structured-markdown: PASS

- SKILL.md error handling table (line 473): `python-pptx missing` error with exact warning text: "PPTX output requires python-pptx. Install with: pip install python-pptx. Falling back to structured-markdown."
- Step 6 PPTX Generation section (lines 368-370): dependency check with fallback behavior

### AC-04 -- Help text lists PPTX: PASS

- SKILL.md user commands (line 489): `present --format [fmt]` lists `pptx` as valid format alongside structured-markdown, marp, paste-ready

### AC-05 -- Font, color, and template config keys: PASS

- config-schema.md (lines 90-92): `presentation.pptx_template` (string, default ""), `presentation.pptx_font` (string, default "Calibri"), `presentation.pptx_accent_color` (string, default "#2d5aa0")
- SKILL.md config table (lines 528-529): all three keys documented with matching defaults
- Version 2.6 changelog in config-schema.md confirms addition

### AC-06 -- JSON intermediate produced by Composer: PASS

- SKILL.md Step 4 (lines 312-313): when `format=pptx`, Composer produces both `composed-draft.md` and `composed-draft.json`
- JSON schema documented inline: slides array with number, title, layout, body, table, speaker_notes, citations, mermaid; metadata object
- generate_pptx.py docstring (lines 16-37) documents the full JSON schema

### AC-07 -- PPTX format dogfooding: CODE_COMPLETE

Empirical AC -- requires end-to-end dogfooding with and without python-pptx.

---

## US-05: Implement Light Mode and Threshold Degradation

### AC-01 -- Light mode activates for 3 or fewer contributing roles: PASS

- SKILL.md (lines 54-68): light mode activation documented. When `presentation.light_mode: auto` and type requires 3 or fewer contributing roles, light mode activates
- Step 3 behavior under light mode (line 185): only required roles dispatched, optional/enhancing skipped
- Step 5 behavior under light mode (lines 320-324): single reviewer (TW only), full scope

### AC-02 -- Light mode config options: PASS

- SKILL.md (lines 55-61): three config values (auto, always, never) documented in table
- `present --full` override (line 62, line 491)
- `present --light` force override (line 62, line 492)

### AC-03 -- Per-type threshold configuration: PASS

- SKILL.md (lines 74-79): threshold resolution order documented (per-type > thresholds_default > 90s hardcoded)
- Value 0 = unlimited (line 79)
- Config keys: `presentation.thresholds` (map), `presentation.thresholds_default` (integer)

### AC-04 -- Degradation at 75% and 100%: PASS

- 75% behavior (lines 82-84): warning message with elapsed/threshold, Step 5 reduced to TW only with MUST-FIX only scope
- 100% behavior (lines 86-87): Step 6 notice with elapsed/threshold and suggestion text

### AC-05 -- Light mode and threshold interaction matrix: PASS

- SKILL.md (lines 89-98): 4-scenario matrix (Full+under, Full+75%, Light+under, Light+75%) with Step 3 Roles, Step 5 Reviewers, Step 5 Scope columns
- Explicitly states effects are union not sum, reviewer count never drops below 1

### AC-06 -- Config keys in config-schema.md: PASS

- config-schema.md (lines 97-99): `presentation.light_mode`, `presentation.thresholds`, `presentation.thresholds_default` documented
- Version 2.5 changelog entry confirms addition

**Note**: Stories specified version bump to v2.4 for these keys, but implementation uses v2.5 (v2.4 was used for narrative intelligence keys from US-07/US-08, which shipped in Sprint 2). This is correct -- the schema was bumped incrementally as each group was implemented. No issue.

### AC-07 -- Light mode dogfooding: CODE_COMPLETE

Empirical AC -- requires dogfooding with simple type to verify auto light mode activation.

---

## US-06: Add Progress Indicators

### AC-01 -- Step begin indicator: PASS

- SKILL.md documents begin indicators for all 6 steps:
  - Step 1 (line 127): `[1/6] Assembling presentation outline... (type: {detected type}, audience: {audience mode})`
  - Step 2 (line 156): `[2/6] Validating source artifacts... ({N} required, {M} enhancing to check)`
  - Step 3 (line 183): `[3/6] Drafting slide content... ({N} roles contributing{, light mode if active})`
  - Step 4 (line 218): `[4/6] Composing final presentation... ({N} editorial passes enabled)`
  - Step 5 (line 319): `[5/6] Reviewing draft... ({reviewer names}, {scope: full | MUST-FIX only})`
  - Step 6 (line 347): `[6/6] Ready for your review.`
- Context varies appropriately per step (role count, reviewer names, scope, etc.)

### AC-02 -- Step completion summary: PASS

- Each step has documented completion output:
  - Step 1 (line 151): `Outline approved: {N} slides, {M} roles contributing`
  - Step 2 (line 179): `Content gate passed: {N} required found, {M} enhancing found, {W} warnings`
  - Step 3 (line 205): `Draft complete: {role names} contributed {N} slides`
  - Step 4 (line 313): `Compose complete: {N} slides, {M} editorial passes applied, {K} slides cut`
  - Step 5 (line 343): `Review complete: {N} MUST-FIX resolved, {M} suggestions preserved`
  - Step 6: user action (approve/changes/abort) -- no automatic completion summary needed

### AC-03 -- Progress indicators dogfooding: CODE_COMPLETE

Empirical AC -- requires generating a presentation and observing all indicators display.

---

## US-07: Implement Editorial Passes (Emphasis, Cutting, Framing, Tension)

### AC-01 -- Emphasis selection reorders by impact: PASS

- SKILL.md Step 4 (lines 239-255): Pass 1 documents impact signal taxonomy with 5 criteria (data-backed results first, external validation before internal, user impact over technical, breadth of usage, complexity resolved)
- Default is impact-ranked, not chronological
- Emphasis log output specified (line 254): `"{Slide title}" moved from position {N} to position {M} -- reason: {signal}"`

### AC-02 -- User can disable emphasis: PASS

- SKILL.md (line 256): `no reorder` / `keep chronological` commands documented
- Config key `presentation.narrative.emphasis: false` disables the pass
- User commands table (line 495): `no reorder` / `keep chronological` listed

**Note on config key naming**: Stories specified `presentation.narrative_reorder` but implementation uses `presentation.narrative.emphasis`. The nested namespace (`narrative.emphasis`, `narrative.cutting`, `narrative.framing`, `narrative.tension`) is more consistent and was adopted during architecture. This is an improvement, not a defect.

### AC-03 -- Information cutting merges low-value slides: PASS

- SKILL.md Step 4 (lines 259-275): cutting heuristics documented (no data + no decision, confidence threshold, obvious information, duplicate emphasis)
- Cuts log format: `"{Slide title} merged into {target slide} -- reason: {rationale}"` (line 268)
- Step 6 Narrative Cuts section (line 356) displays cuts log for user review

### AC-04 -- User can restore cut slides: PASS

- SKILL.md (line 275): `restore {slide title}` command documented
- Config key `presentation.narrative.cutting: false` disables cutting globally
- User commands table (line 496): `restore {slide title}` listed

### AC-05 -- Audience-specific framing: PASS

- SKILL.md Step 4 (lines 277-291): Pass 3 documented with framing rules by audience type
- narrative-patterns.md (lines 303-361): "Audience Framing Rules" section with detailed rules for investor, executive, technical, customer/client-facing, and casual audiences
- Each audience type has Lead, Features, Metrics, Technical detail, Framing verb, and Slide structure specifications

### AC-06 -- Narrative tension at 60-70%: PASS

- SKILL.md Step 4 (lines 293-308): Pass 4 documented with climax positioning at 60-70%
- narrative-patterns.md (lines 380-410): "Narrative Tension Patterns" section with type-specific patterns for all 9 types
- Minimum 6 slides threshold documented
- Reordering rules respect position-locked slides

### AC-07 -- Pass ordering is strictly sequential: PASS

- SKILL.md (lines 235-236): explicitly states "Order is strict (per architecture ADR-02): Emphasis > Cutting > Framing > Tension. No parallelism -- each pass depends on the previous pass's output."
- Passes numbered 1-4 in the documentation

### AC-08 -- Narrative intelligence dogfooding: CODE_COMPLETE

Empirical AC -- requires 10+ slide presentation with verification of all four pass outputs.

---

## US-08: Add Narrative Intelligence Config and Review Gate Criteria

### AC-01 -- Review Gate validates narrative quality: PASS

- SKILL.md Step 5 (lines 335-336): TW criterion documented: "Does each slide earn its place? Could any slide be cut without losing the argument?"
- UX criterion documented: "Does the presentation build toward a clear climax? Is the strongest content positioned for maximum impact?"

### AC-02 -- Narrative MUST-FIX issues auto-fixed: PASS

- SKILL.md Step 5 (line 339): "Composer fixes these automatically before Step 6 (including narrative quality MUST-FIX issues -- same auto-fix behavior as formatting issues)"

### AC-03 -- Review Gate dogfooding: CODE_COMPLETE

Empirical AC -- requires generating presentation and inspecting Review Gate output for narrative criteria.

---

## Coverage Assessment

| Area | Coverage | Notes |
|------|----------|-------|
| Type definitions (5 new) | Complete | All keywords, content gates, narratives, slides verified |
| Error handling | Complete | 9 types listed, unknown type error updated |
| PPTX script | Complete | Layout mapping, template, branding, dependency guard, speaker notes |
| PPTX config/format | Complete | Format option, fallback, JSON intermediate, config keys |
| Light mode + thresholds | Complete | Auto/always/never, degradation matrix, per-type thresholds |
| Progress indicators | Complete | All 6 steps have begin + completion indicators |
| Editorial passes | Complete | 4 passes with strict ordering, user overrides, config toggles |
| Narrative config + review | Complete | Review Gate criteria, auto-fix, 4 config keys |
| Config schema | Complete | 10 new keys across v2.4-v2.6, extension protocol followed |

## Critical Issues

None.

## Observations

1. **Config key naming refinement**: Stories specified flat keys (`narrative_reorder`, `narrative_cutting`) but implementation uses nested namespace (`narrative.emphasis`, `narrative.cutting`, `narrative.framing`, `narrative.tension`). The nested approach is more consistent and extensible. Not a defect -- this is an architectural improvement adopted during design.

2. **Schema versioning**: Stories expected a single bump to v2.4. Implementation correctly used incremental bumps (v2.4 for narrative passes, v2.5 for light mode/thresholds, v2.6 for PPTX branding) matching the sprint delivery order. This is proper schema evolution.

3. **SKILL.md metadata description**: The frontmatter (line 2) lists "9 types" with all type names and expanded trigger phrases. Verify marketplace.json registration reflects the updated description.

4. **generate_pptx.py quality**: Clean separation of concerns -- layout resolution, color parsing, slide population, and CLI all isolated. The import guard pattern (lines 41-53) is robust. Speaker notes support (OQ-5 resolution) implemented via `add_speaker_notes` function. No external dependencies beyond python-pptx.

---

```
STATUS: CODE_COMPLETE
ARTIFACT: .delivery/artifacts/06-dev/dod/qa-review.md
SUMMARY: All 36 structural ACs pass across 8 stories; 8 empirical ACs classified CODE_COMPLETE pending dogfooding.
```
