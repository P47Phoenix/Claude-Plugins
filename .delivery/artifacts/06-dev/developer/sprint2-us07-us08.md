# Sprint 2 Development Artifact — US-07 & US-08

**Pipeline**: run-2026-04-04-w7m3
**Sprint**: 2 (Narrative Intelligence)
**Developer**: Gimli
**Date**: 2026-04-04
**Stories**: US-07 (5 SP), US-08 (1 SP)
**FRs**: FR-16, FR-17, FR-18, FR-19, FR-20

> *"I never thought I'd edit markdown side by side with a pipeline. And my code!"*

---

## Files Modified

| File | Changes | Story |
|------|---------|-------|
| `delivery-team/skills/presentation/SKILL.md` | Added 4 editorial passes to Step 4, updated Step 5 review criteria, updated Step 6 output sections, added `no reorder`/`restore` commands, added 4 narrative config keys | US-07, US-08 |
| `delivery-team/skills/presentation/references/narrative-patterns.md` | Added Audience Framing Rules section (5 audience types with per-aspect rule tables), Type-Specific Emphasis Weight Modifiers, Narrative Tension Patterns section (9 types with pattern/climax/arc), Reordering Rules | US-07 |
| `delivery-team/skills/delivery-flow/references/config-schema.md` | Added 4 `presentation.narrative.*` config keys, bumped version to 2.4 | US-08 |

---

## AC Traceability

### US-07

| AC | Status | Implementation |
|----|--------|---------------|
| AC-01 (Emphasis reorders by impact) | DONE | SKILL.md Step 4 — Pass 1 with impact signal taxonomy (5 signals), emphasis_log output |
| AC-02 (User can disable reorder) | DONE | SKILL.md — `no reorder`/`keep chronological` command + `presentation.narrative.emphasis: false` config |
| AC-03 (Cutting merges low-value) | DONE | SKILL.md Step 4 — Pass 2 with 4 cutting heuristics, confidence threshold < 3/5, cuts_log output |
| AC-04 (User can restore cuts) | DONE | SKILL.md — `restore {slide title}` command + `presentation.narrative.cutting: false` config |
| AC-05 (Audience framing restructures) | DONE | SKILL.md Step 4 — Pass 3 + narrative-patterns.md Audience Framing Rules (5 audience types with 6-aspect rule tables) |
| AC-06 (Tension at 60-70%) | DONE | SKILL.md Step 4 — Pass 4 + narrative-patterns.md Narrative Tension Patterns (9 types with climax identification) |
| AC-07 (Sequential ordering) | DONE | SKILL.md Step 4 — explicit "Order is strict (per architecture ADR-02): Emphasis > Cutting > Framing > Tension" |
| AC-08 (Empirical) | DEFERRED | Requires dogfooding run with 10+ slide presentation |

### US-08

| AC | Status | Implementation |
|----|--------|---------------|
| AC-01 (Review Gate narrative criteria) | DONE | SKILL.md Step 5 — TW criterion ("Does each slide earn its place?") + UX criterion ("Does the presentation build toward a clear climax?") |
| AC-02 (Narrative MUST-FIX auto-fix) | DONE | SKILL.md Step 5 — explicit "including narrative quality MUST-FIX issues — same auto-fix behavior" |
| AC-03 (Empirical) | DEFERRED | Requires dogfooding run |

---

## Config Keys Added (FR-20)

| Key | Type | Default | Effect When Disabled |
|-----|------|---------|---------------------|
| `presentation.narrative.emphasis` | boolean | true | Pass 1 skipped, original outline order preserved |
| `presentation.narrative.cutting` | boolean | true | Pass 2 skipped, all draft slides preserved |
| `presentation.narrative.framing` | boolean | true | Pass 3 skipped, no argument restructuring |
| `presentation.narrative.tension` | boolean | true | Pass 4 skipped, no climax repositioning |

Config schema version bumped from 2.3 to 2.4.

---

## Design Decisions

1. **Config key naming**: Used `presentation.narrative.*` (dot-nested) rather than `presentation.narrative_*` (underscore) to match the grouped nature of the 4 passes. All 4 are children of the narrative intelligence system.
2. **Framing as always-on default**: Unlike the architecture doc which had framing as non-disableable, we added a config toggle per FR-20 which specifies all 4 passes should be independently toggleable. Default is true so behavior matches architecture intent.
3. **Tension minimum threshold**: Kept at 6 slides per architecture doc section 2.3. This is hardcoded in the pass rules, not configurable.
4. **Step 6 additions**: Added Narrative Cuts and Emphasis Order as separate sections (items 3 and 4) in the user review output, before warnings and suggestions. This gives the user visibility into editorial decisions before approving.

---

## Diff Verification Checklist

- [x] SKILL.md Step 4: 4 editorial passes with full rules
- [x] SKILL.md Step 5: TW and UX narrative criteria added
- [x] SKILL.md Step 6: Narrative Cuts + Emphasis Order sections
- [x] SKILL.md User Commands: `no reorder`, `restore` added
- [x] SKILL.md Config: 4 `presentation.narrative.*` keys added
- [x] narrative-patterns.md: Audience Framing Rules (5 types)
- [x] narrative-patterns.md: Type-Specific Emphasis Weight Modifiers (9 types)
- [x] narrative-patterns.md: Narrative Tension Patterns (9 types + 5 reordering rules)
- [x] config-schema.md: 4 new keys + version bump to 2.4
