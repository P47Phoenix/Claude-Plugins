# Idea Brief: Batched Documentation Fix (Issues #63 + #64)

**Date**: 2026-04-04
**Author**: Product Owner
**Type**: DOCS_ONLY
**Priority**: High

---

## Problem Statement

The documentation has fallen behind the code -- a map drawn before the mountains moved. Two related gaps have opened, and a wise team mends both at once rather than traversing the same ground twice.

### Issue #63 — Config Reference Gap

The docs site config reference (`docs/user-guide/config.md`) is missing 13 config keys added across schema versions v2.4 through v2.6. Users consulting this page cannot find:

- PPTX branding keys (`presentation.pptx_template`, `presentation.pptx_font`, `presentation.pptx_accent_color`)
- Narrative intelligence toggles (`presentation.narrative.emphasis`, `.cutting`, `.framing`, `.tension`)
- Light mode setting (`presentation.light_mode`)
- Per-type threshold overrides (`presentation.thresholds`, `presentation.thresholds_default`)
- Presentation operational keys (`presentation.save_to_artifacts`, `presentation.marp_theme`, `presentation.staleness_warning_days`, `presentation.vocabulary_overrides`)
- Pipeline retry key (`pipeline.required_agent_retry_max`)

The source of truth (`delivery-team/skills/delivery-flow/references/config-schema.md` v2.6) has all these keys. The docs page does not.

### Issue #64 — Stale Documentation

Multiple docs pages and CLAUDE.md contain outdated information after recent feature work:

| What is Wrong | Where | Correct State |
|--------------|-------|--------------|
| Presentation skill says "4 types, 3 formats" | `CLAUDE.md` line 51 | 9 types, 4 formats (PPTX added) |
| Config version says v2.3 | `CLAUDE.md` line 124 | v2.6 |
| Architect Prior Art Analysis (#55) not mentioned | `docs/skills/architect.md` | Architect SKILL.md has full Prior Art Analysis section |
| Orchestrator theme surfacing (#59) not mentioned | `docs/skills/delivery-flow.md` | pipeline-stages.md references theme surfacing |
| SKILL.md deduplication (#62) changed delivery-flow structure | `docs/skills/delivery-flow.md` | Delivery-flow now uses single SKILL.md + references pattern |

---

## Scope

Five files require updates:

| # | File | Changes |
|---|------|---------|
| 1 | `CLAUDE.md` | Update presentation description (9 types, 4 formats), bump config version to v2.6, add Prior Art Analysis to architect description, mention theme surfacing in delivery-flow |
| 2 | `docs/user-guide/config.md` | Add 13 missing config keys from v2.4-v2.6 to Presentation section, add `pipeline.required_agent_retry_max` to Pipeline section, update full example config |
| 3 | `docs/skills/presentation.md` | Update to reflect current state: 9 types, 4 formats (PPTX), narrative intelligence editorial passes, light mode, per-type thresholds |
| 4 | `docs/skills/architect.md` | Add Prior Art Analysis section documenting the conditional spec-examination step |
| 5 | `docs/skills/delivery-flow.md` | Update to reflect deduplication refactor: SKILL.md as high-level orchestration guide, pipeline-stages.md as authoritative source for stage details |

## Out of Scope

- No changes to SKILL.md files or runtime code
- No schema changes (v2.6 is current)
- No new features

---

## Value

- Users and contributors get accurate, trustworthy documentation
- Config reference becomes complete -- every key a user can set is documented
- New features (Prior Art Analysis, PPTX output, narrative intelligence) become discoverable
- Reduces contributor confusion from stale information

## Risks

| Risk | Severity | Mitigation |
|------|----------|------------|
| Partial update leaves some docs still stale | Low | Batch all 5 files in one PR; verify cross-file consistency before merge |
| Docs drift again after next feature | Medium | Consider adding docs-update checklist to pipeline DoD (future improvement) |

## Success Criteria

1. All 5 files updated and internally consistent
2. Config reference matches `config-schema.md` v2.6 exactly -- zero missing keys
3. No stale version numbers, feature counts, or missing feature mentions remain
4. PR passes review with no factual inaccuracies found
