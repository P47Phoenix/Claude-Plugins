# User Stories: Batched Documentation Fix (Issues #63 + #64)

**Sprint**: Docs Fix Sprint
**Type**: DOCS_ONLY
**Date**: 2026-04-04

---

## Story 1: Update Config Reference with Missing v2.4-v2.6 Keys

**ID**: DOC-63-001
**Priority**: High
**Estimate**: 2 SP
**References**: Issue #63

### Story

As a plugin user configuring my delivery pipeline, I need the config reference page (`docs/user-guide/config.md`) to document all available config keys including those added in v2.4-v2.6, so that I can discover and configure PPTX branding, narrative intelligence, light mode, and threshold settings without reading source code.

### Acceptance Criteria

| # | Criterion | Type | Verification |
|---|-----------|------|-------------|
| AC-1 | The Presentation section in `docs/user-guide/config.md` includes all 13 missing keys: `presentation.save_to_artifacts`, `presentation.marp_theme`, `presentation.staleness_warning_days`, `presentation.vocabulary_overrides`, `presentation.pptx_template`, `presentation.pptx_font`, `presentation.pptx_accent_color`, `presentation.narrative.emphasis`, `presentation.narrative.cutting`, `presentation.narrative.framing`, `presentation.narrative.tension`, `presentation.thresholds`, `presentation.thresholds_default` | Structural | Count presentation keys in docs vs config-schema.md -- must match |
| AC-2 | The Pipeline section includes `pipeline.required_agent_retry_max` (integer, default 2, range 1-5) | Structural | Grep for `required_agent_retry_max` in docs config page |
| AC-3 | The full example config YAML includes all new keys with their defaults | Structural | Compare example YAML keys against config-schema.md complete schema |
| AC-4 | Every key's type, default, valid values, and description match config-schema.md v2.6 exactly | Accuracy | Side-by-side comparison with config-schema.md |

### Test Cases

| TC | Covers AC | Test | Expected |
|----|-----------|------|----------|
| TC-1 | AC-1 | Count `presentation.*` keys in docs/user-guide/config.md Presentation table | 18 keys (5 existing + 13 new) |
| TC-2 | AC-2 | Grep `required_agent_retry_max` in docs/user-guide/config.md | 1 match in Pipeline table |
| TC-3 | AC-3 | Parse example YAML and compare key set to config-schema.md | All keys present |
| TC-4 | AC-4 | Spot-check 5 new keys for type/default/valid-values accuracy | All match source of truth |

---

## Story 2: Fix Stale Documentation Across CLAUDE.md and Docs Site

**ID**: DOC-64-001
**Priority**: High
**Estimate**: 3 SP
**References**: Issue #64

### Story

As a contributor reading the repo documentation, I need CLAUDE.md and the docs site pages to accurately reflect the current state of the presentation skill (9 types, 4 formats), config schema version (v2.6), architect Prior Art Analysis, orchestrator theme surfacing, and delivery-flow deduplication refactor, so that I am not misled by outdated information.

### Acceptance Criteria

| # | Criterion | Type | Verification |
|---|-----------|------|-------------|
| AC-1 | `CLAUDE.md` presentation skill row describes 9 types and 4 formats (structured-markdown, marp, paste-ready, pptx) | Structural | Inspect CLAUDE.md delivery-team skills table, presentation row |
| AC-2 | `CLAUDE.md` config schema reference says v2.6, not v2.3 | Structural | Grep `v2.3` in CLAUDE.md returns 0 matches; grep `v2.6` returns match in config schema line |
| AC-3 | `CLAUDE.md` architect skill row mentions Prior Art Analysis | Structural | Inspect architect row in delivery-team skills table |
| AC-4 | `docs/skills/presentation.md` lists all 9 presentation types with descriptions | Structural | Count type rows in the Presentation Types table |
| AC-5 | `docs/skills/presentation.md` lists all 4 output formats including PPTX | Structural | Inspect Output Formats section |
| AC-6 | `docs/skills/presentation.md` documents narrative intelligence editorial passes | Structural | Section or paragraph describing emphasis, cutting, framing, tension passes |
| AC-7 | `docs/skills/presentation.md` documents light mode with config values | Structural | Light Mode section with auto/always/never table |
| AC-8 | `docs/skills/architect.md` includes a Prior Art Analysis section describing the conditional spec-examination step | Structural | Section exists with condition, phases, output description |
| AC-9 | `docs/skills/delivery-flow.md` reflects the deduplication refactor: SKILL.md as high-level orchestration guide with pipeline-stages.md as authoritative source for stage details | Structural | Description mentions single-source-of-truth pattern |
| AC-10 | `docs/skills/delivery-flow.md` mentions theme surfacing capability | Structural | Grep for "theme" in delivery-flow docs page |

### Test Cases

| TC | Covers AC | Test | Expected |
|----|-----------|------|----------|
| TC-1 | AC-1 | Grep CLAUDE.md for presentation row | Contains "9 types" or lists all 9; contains "4 formats" or lists all 4 |
| TC-2 | AC-2 | Grep CLAUDE.md for "v2.3" | 0 matches |
| TC-3 | AC-2 | Grep CLAUDE.md for "v2.6" | At least 1 match in config schema context |
| TC-4 | AC-3 | Grep CLAUDE.md for "Prior Art" | At least 1 match in architect row |
| TC-5 | AC-4 | Count presentation type rows in docs/skills/presentation.md | 9 types |
| TC-6 | AC-5 | Grep docs/skills/presentation.md for "PPTX" | At least 1 match in Output Formats |
| TC-7 | AC-6 | Grep docs/skills/presentation.md for "narrative" | Matches describing editorial passes |
| TC-8 | AC-7 | Grep docs/skills/presentation.md for "light_mode" or "Light Mode" | Section present |
| TC-9 | AC-8 | Grep docs/skills/architect.md for "Prior Art Analysis" | Section heading present |
| TC-10 | AC-9 | Grep docs/skills/delivery-flow.md for "pipeline-stages" | Reference to single source of truth |
| TC-11 | AC-10 | Grep docs/skills/delivery-flow.md for "theme" | Theme surfacing mentioned |
| TC-12 | AC-1, AC-4 | Cross-check: CLAUDE.md presentation description is consistent with docs/skills/presentation.md | Same type count, same format list |
