# Sprint Plan: Batched Documentation Fix (Issues #63 + #64)

**Sprint Goal**: Bring all documentation into alignment with the current codebase -- config reference complete to v2.6, presentation docs updated to v1.1, architect and delivery-flow docs reflecting recent features.
**Type**: DOCS_ONLY
**Velocity Ceiling**: 80%
**Sprint Capacity**: 2 stories, 5 SP
**Load**: 5 / 6.25 available = 80% (at ceiling)

---

## Story Sequence

| Order | Story ID | Title | SP | Dependencies | Assignee |
|-------|----------|-------|----|-------------|----------|
| 1 | DOC-63-001 | Update Config Reference with Missing v2.4-v2.6 Keys | 2 | None | Technical Writer |
| 2 | DOC-64-001 | Fix Stale Documentation Across CLAUDE.md and Docs Site | 3 | None (parallel-safe) | Technical Writer |

Both stories are independent and may execute in parallel. However, the Technical Writer should complete DOC-63-001 first, since the config key additions inform what the presentation docs page (DOC-64-001) references.

---

## Implementation Plan

### Story 1: DOC-63-001 — Config Reference Update

**File**: `docs/user-guide/config.md`

**Tasks**:

1. **Add missing Presentation keys to Presentation table** (13 keys)
   - PPTX branding: `pptx_template`, `pptx_font`, `pptx_accent_color`
   - Narrative intelligence: `narrative.emphasis`, `narrative.cutting`, `narrative.framing`, `narrative.tension`
   - Operational: `save_to_artifacts`, `marp_theme`, `staleness_warning_days`, `vocabulary_overrides`
   - Thresholds: `thresholds` (map), `thresholds_default` (integer) -- note: `thresholds_default` already exists but `thresholds` (per-type map) is missing
   - Light mode: `light_mode` -- verify already present (was added but verify completeness)
   - Source of truth: `delivery-team/skills/delivery-flow/references/config-schema.md` lines 83-99

2. **Add missing Pipeline key**
   - `pipeline.required_agent_retry_max` (integer, default 2, range 1-5, description: "Retry for required agents in parallel groups")
   - Source: config-schema.md line 39

3. **Update full example config YAML**
   - Add all new presentation keys with defaults
   - Add `pipeline.required_agent_retry_max: 2`

**Verification**: Run AC-1 through AC-4, TC-1 through TC-4.

---

### Story 2: DOC-64-001 — Stale Documentation Fix

**Files**: 4 files, ordered by dependency.

#### Task 2a: Update `CLAUDE.md`

| Line/Section | Current | Updated |
|-------------|---------|---------|
| Line 45 (architect row) | "11 roles: solution/enterprise/data/security/compliance/privacy/IR + 4 game architecture + 4 decomposition strategies" | Add "+ Prior Art Analysis" |
| Line 51 (presentation row) | "4 types: Sprint Review, Feature Pitch, Stakeholder Update, Technical Deep-Dive" | "9 types: Sprint Review, Feature Pitch, Stakeholder Update, Technical Deep-Dive, Investor Pitch, Roadmap, Product Demo, Onboarding, Retrospective Summary. 4 formats: structured-markdown, Marp, paste-ready, PPTX" |
| Line 41 (delivery-flow row) | Current description | Add mention of theme surfacing |
| Line 124 (config schema) | "currently v2.3" | "currently v2.6" |

#### Task 2b: Update `docs/skills/presentation.md`

- Update intro text to mention 9 types and 4 formats
- Presentation Types table: already has 9 types (verify)
- Output Formats: add PPTX with description of configurable template and branding
- Add Narrative Intelligence section: 4 editorial passes (emphasis, cutting, framing, tension) in the Compose step
- Add/verify Light Mode section with auto/always/never table
- Update Configuration example YAML to include new keys

#### Task 2c: Update `docs/skills/architect.md`

- Add "Prior Art Analysis" section after the Task Types table
- Document: condition (user-provided specs present), two phases (examine then classify), output (summary + classification table in architecture artifact)
- Source: `delivery-team/skills/architect/SKILL.md` Prior Art Analysis section

#### Task 2d: Update `docs/skills/delivery-flow.md`

- Update "What It Does" to mention single-source-of-truth pattern (SKILL.md + pipeline-stages.md)
- Add bullet about theme surfacing in pipeline orchestration
- Update structural description to reflect deduplication: SKILL.md is high-level orchestration guide, `references/pipeline-stages.md` is authoritative source for detailed stage sub-flows, agent invocations, and artifact paths

**Verification**: Run AC-1 through AC-10, TC-1 through TC-12.

---

## Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| Missing a key in config docs | Low | Medium | Diff config-schema.md keys against docs/user-guide/config.md keys programmatically |
| Introducing new factual error while fixing old ones | Low | Medium | Cross-reference every claim against source SKILL.md files |
| Forgetting to update the example YAML | Low | Low | TC-3 catches this explicitly |

---

## Branch Strategy

- Branch: `docs/fix-63-64-stale-docs`
- Conventional commit: `docs: update config reference and fix stale docs (#63, #64)`
- Single PR batching both issues

---

## Definition of Done

- [ ] All 14 ACs pass across both stories (4 from DOC-63-001 + 10 from DOC-64-001)
- [ ] All 16 TCs pass (4 + 12)
- [ ] No stale version numbers, feature counts, or missing features remain in any of the 5 files
- [ ] Config reference key count matches config-schema.md v2.6 exactly
- [ ] PR reviewed and merged
