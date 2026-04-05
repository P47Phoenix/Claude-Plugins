# Developer Notes: DOC-63-001 + DOC-64-001

**Date**: 2026-04-04
**Developer**: Gimli (delivery-team:developer)
**Stories**: DOC-63-001 (config key docs), DOC-64-001 (staleness fixes)

---

## Story DOC-63-001: Config Reference Update

### Changes Made

**File: `docs/user-guide/config.md`**

1. **Presentation section** -- Added 13 missing config keys to the Presentation table:
   - `presentation.save_to_artifacts` (boolean, default true)
   - `presentation.marp_theme` (string, default "default")
   - `presentation.staleness_warning_days` (integer, default 7)
   - `presentation.vocabulary_overrides` (map, default {})
   - `presentation.pptx_template` (string, default "")
   - `presentation.pptx_font` (string, default "Calibri")
   - `presentation.pptx_accent_color` (string, default "#2d5aa0")
   - `presentation.narrative.emphasis` (boolean, default true)
   - `presentation.narrative.cutting` (boolean, default true)
   - `presentation.narrative.framing` (boolean, default true)
   - `presentation.narrative.tension` (boolean, default true)
   - `presentation.light_mode` (string, default "auto") -- was present but updated with full valid values
   - `presentation.thresholds` (map, default {})
   - `presentation.thresholds_default` (integer, default 90) -- was present but updated valid values description

2. **Pipeline section** -- Added `pipeline.required_agent_retry_max` (integer, default 2, range 1-5)

3. **Full example YAML** -- Updated to include all new presentation keys and missing pipeline keys (verify_skill_loading, delegation_retry_max, isolation_audit, metadata_max_chars, agent_timeout, required_agent_retry_max) matching config-schema.md v2.6 template exactly.

### Verification

- All key types, defaults, and valid values match config-schema.md v2.6 exactly
- Example YAML matches the Config File Template in config-schema.md

---

## Story DOC-64-001: Staleness Fixes

### Changes Made

**File: `CLAUDE.md`**

1. Presentation skill row: Updated from "4 types" to "9 types (...), 4 formats (...), narrative intelligence (4 editorial passes), light mode"
2. Config schema version: Updated from "v2.3" to "v2.6"
3. Architect skill row: Added "+ Prior Art Analysis"
4. Delivery-flow pipeline architecture: Added theme surfacing mention to alias themes bullet

**File: `docs/skills/presentation.md`**

1. All 9 presentation types were already listed (previous update) -- verified correct
2. All 4 output formats including PPTX were already listed -- verified correct
3. Added Narrative Intelligence section with table of 4 editorial passes (emphasis, cutting, framing, tension) and their config keys
4. Light Mode section was already present -- verified correct
5. Updated Configuration YAML block to include all 18 presentation config keys

**File: `docs/skills/architect.md`**

1. Added Prior Art Analysis section before Task Types, describing the 4-step conditional process (Read and Summarize, Classify Each Element, Build On Existing Design, Deviation Protocol)

**File: `docs/skills/delivery-flow.md`**

1. Added Architecture section describing SKILL.md as high-level orchestration guide with pipeline-stages.md as SSOT for stage details
2. Added theme surfacing bullet to "What It Does" list, noting user-facing output slots and neutrality preservation in internal surfaces

---

## AC Verification Summary

| AC | Status | Notes |
|----|--------|-------|
| DOC-63 AC-1 | PASS | 18 presentation keys in docs (5 existing + 13 new) |
| DOC-63 AC-2 | PASS | `required_agent_retry_max` present in Pipeline table |
| DOC-63 AC-3 | PASS | Example YAML includes all new keys with defaults |
| DOC-63 AC-4 | PASS | All types/defaults/valid-values match config-schema.md v2.6 |
| DOC-64 AC-1 | PASS | CLAUDE.md presentation row has 9 types, 4 formats |
| DOC-64 AC-2 | PASS | CLAUDE.md says v2.6, not v2.3 |
| DOC-64 AC-3 | PASS | CLAUDE.md architect row mentions Prior Art Analysis |
| DOC-64 AC-4 | PASS | docs/skills/presentation.md lists all 9 types |
| DOC-64 AC-5 | PASS | docs/skills/presentation.md lists all 4 formats including PPTX |
| DOC-64 AC-6 | PASS | Narrative Intelligence section with 4 editorial passes |
| DOC-64 AC-7 | PASS | Light Mode section with auto/always/never table |
| DOC-64 AC-8 | PASS | Prior Art Analysis section in docs/skills/architect.md |
| DOC-64 AC-9 | PASS | Architecture section in docs/skills/delivery-flow.md references pipeline-stages.md as SSOT |
| DOC-64 AC-10 | PASS | Theme surfacing mentioned in delivery-flow.md What It Does |

## Deviation from Plan

None. All acceptance criteria addressed as specified. And my code!
