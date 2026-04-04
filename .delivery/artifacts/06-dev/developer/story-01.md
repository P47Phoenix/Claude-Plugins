# Development Artifact: US-01 — Orchestrator Theme Surfacing

**Story**: US-01 (Orchestrator Theme Surfacing)
**Issue**: #59
**Developer**: Gimli
**Date**: 2026-04-04

> "I said I'd carve this stone, and carved it is. Every chisel stroke accounted for. And my code!"

---

## File Modified

`delivery-team/skills/delivery-flow/SKILL.md`

---

## Changes Made

### 1. Theme-Gated Reporting Protocol (new section, after Two-Channel Communication)

Inserted a new `### Theme-Gated Reporting Protocol` section between "Two-Channel Communication" and "Plan-Mode Delegation" in Phase 4. This section defines:

- **Theme detection guard**: All themed behavior gated on `aliases.theme != business`. Business or unset = zero behavior change.
- **Three output slots** where theme surfaces:
  1. Stage Announcements (Step 1) — character name + thematic voice
  2. Human Checkpoint Summaries (Step 9) — quoted agent artifact line (max 280 chars)
  3. Stage Transitions (Step 10) — themed STATE ANCHOR with routing signals preserved
- **Quote format**: blockquote with character attribution (`> "text" — Character Name`)
- **Partial theme fallback**: roles missing from theme's `roles` map fall back to neutral format

### 2. Neutrality Preservation (sub-section within Theme-Gated Reporting Protocol)

Explicit rules that themed content NEVER appears in:
- `.delivery/state.md`
- `stage-summary.md` files
- Agent Invocation Template prompts (ALIAS block handles personality)
- DoD validator prompts
- Signal blocks (STATUS/ARTIFACT/SUMMARY format unchanged)

### 3. Step 1: Announce (conditional block added)

Added conditional logic:
- **Non-business theme + role in `roles` map**: Reference character name, use thematic vocabulary/tone per `personality_strength`
- **Business/unset/unmapped role**: Use existing neutral format (`## Stage [N]: [NAME]\nPurpose: ...`)

### 4. Step 9: Check for Human Checkpoint (conditional block added)

Added conditional logic:
- **Non-business theme**: Read primary agent artifact, select one themed quote (max 280 chars), include in checkpoint summary. Read scoped to quote selection only — no content forwarding to downstream agents. Omit quote if no themed language found.
- **Business/unset**: Standard neutral checkpoint summary, no artifact quotes.

### 5. Step 10: Advance (conditional block added)

Added conditional logic:
- **Non-business theme**: STATE ANCHOR carries thematic voice. Stage number, stage name, and continuation directive MUST be present.
- **Business/unset**: Neutral STATE ANCHOR format (unchanged from pre-feature behavior).

---

## Acceptance Criteria Coverage

| AC | Status | Notes |
|----|--------|-------|
| AC-01 | MET | Step 1 references character name from `roles` map |
| AC-02 | MET | Step 1 carries thematic vocabulary/tone per `personality_strength` |
| AC-03 | MET | Step 1 neutral format when business/unset |
| AC-04 | MET | Step 1 falls back to neutral when role not in `roles` map |
| AC-05 | MET | Step 9 includes quoted line (max 280 chars) from artifact |
| AC-06 | MET | Step 9 quote read scoped to user-facing output only, two-channel preserved |
| AC-07 | MET | Step 9 no quotes when business/unset |
| AC-08 | MET | Step 9 omits quote when no themed language found |
| AC-09 | MET | Step 10 STATE ANCHOR carries thematic voice |
| AC-10 | MET | Step 10 routing signals always present in themed message |
| AC-11 | MET | Step 10 neutral format when business/unset |
| AC-12 | MET | Neutrality Preservation: state.md excluded |
| AC-13 | MET | Neutrality Preservation: stage-summary.md excluded |
| AC-14 | MET | Neutrality Preservation: Agent Invocation Templates excluded |
| AC-15 | MET | Neutrality Preservation: DoD validator prompts excluded |
| AC-16 | MET | Neutrality Preservation: signal block format unchanged |
| AC-17 | MET | Neutrality Preservation: signal extraction logic unchanged |

---

## Source vs Installed Diff

Source file (`delivery-team/skills/delivery-flow/SKILL.md`) contains the new changes. Installed file (`~/.claude/plugins/marketplaces/.../delivery-team/skills/delivery-flow/SKILL.md`) reflects the pre-feature baseline. Diff confirms exactly the expected additions (Theme-Gated Reporting Protocol section + conditional blocks in Steps 1, 9, 10) with no unintended changes. The installed copy updates on next plugin sync after merge.

---

> "Every acceptance criterion met, every neutrality rule carved in mountain stone. The axe does not waver."
