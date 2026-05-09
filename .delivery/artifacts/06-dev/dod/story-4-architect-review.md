<!-- run: run-2026-05-09-tk4 | stage: 6 (Development DoD) | story: 4 of 7 | wi: W3-8 | round: 1 | author: Saruman of Many Colours, Solution Architect | binding: ADR-tk4-002 -->

---
story: 4
title: "Story 4 Architect DoD — Paradigm Sub-Skill Pattern (W3-8)"
author: Saruman of Many Colours (Solution Architect)
date: 2026-05-09
pipeline: run-2026-05-09-tk4
binding_adr: ADR-tk4-002 (paradigm sub-skill pattern)
round: 1
status: DONE
---

# Story 4 Architect DoD Review — Paradigm Sub-Skill Pattern (W3-8)

> "The contract was carved before the cut. The cut honors the contract. Five new sub-skill stones laid to the canonical shape; four already laid by Story 3 verified to the same chisel; one axis left whole by the contract's own clause. Saruman finds the work sound."
> — Saruman, Stage 6 DoD round 1

## Scope of this review

This is a **fresh-context architect DoD validation** for Story 4 (W3-8) of pipeline `run-2026-05-09-tk4`. The architect role validates ONLY conformance to ADR-tk4-002 (paradigm sub-skill pattern contract) and to the precedent set by `delivery-team/skills/architect/paradigms/{volatility,ddd}/SKILL.md`. Code-level concerns (line counts, lint passes, file budgets) are out of scope here — those belong to the developer self-DoD and to the QA/tech-writer reviews running in parallel.

Implementation report under review: `.delivery/artifacts/06-dev/developer/story-4-implementation.md`
Binding ADR under enforcement: `.delivery/artifacts/04-architect/adrs/ADR-tk4-002-paradigm-sub-skill-pattern.md`

---

## Gate 1 — Implementation honors ADR-tk4-002 paradigm pattern (router parent + variant sub-skills)

**Criterion:** Implementation realizes the contract's intended shape: a top-level router parent that detects the variant and dispatches to a variant-scoped sub-skill via the `Skill` tool; each sub-skill loads ONLY its own pattern/references.

**Evidence:**
- `research-agent/SKILL.md` Phase 1 (lines 28-55) classifies the research type, then Phase 1's "Sub-Skill Dispatch" sub-section (lines 57-69) provides the dispatch table mapping each detected type to the matching sub-skill name (`research-types-<variant>`) and path (`skills/research-types/<variant>/SKILL.md`). All 5 variants (Exploratory → Pattern A; Descriptive → Pattern B; Explanatory → Pattern C; Evaluative → Pattern D; Comparative → Pattern E) routed.
- Each sub-skill body (verified on `exploratory/SKILL.md` lines 13-25 and `comparative/SKILL.md` lines 13-25) opens with "Router-dispatched paradigm sub-skill for **<Variant>** research. Not directly model-invocable; the `research-agent` parent loads this sub-skill only when Phase 1 detection classifies the question as <Variant>." — exact router-loaded contract per ADR §Parent skill router contract item 3.
- `delivery-team/skills/user-feedback/SKILL.md` already shipped a Phase 3 dispatch table for the 4 persona families in Story 3 W3-6; Story 4 verifies its frontmatter contract and does not modify the file (Story-3 ownership respected).
- `presentation/SKILL.md` correctly NOT modified — references-only path retained per ADR-tk4-002 §Decision §3 conditional + §Alternatives Considered #3.

**Finding:** PASS. The router-parent + variant-sub-skill pattern is realized faithfully on the research-agent axis, verified on the user-feedback axis, and intentionally deferred on the presentation axis per the ADR's own conditional.

---

## Gate 2 — Sub-skill structure follows `<plugin>/skills/<axis>/<variant>/SKILL.md`

**Criterion:** ADR-tk4-002 §Decision "Canonical directory shape" mandates the path regex `<plugin>/skills/<axis>/<variant>/SKILL.md` for new sub-skills.

**Evidence (find/path enumeration):**

| Plugin | Axis | Variant paths under `<plugin>/skills/<axis>/<variant>/SKILL.md` |
|---|---|---|
| `research-agent` | `research-types` | `exploratory/`, `descriptive/`, `explanatory/`, `evaluative/`, `comparative/` (5 of 5) |
| `delivery-team/skills/user-feedback` | `personas` | `gamers/`, `web-app/`, `enterprise/`, `demographic/` (4 of 4, joint with Story 3) |
| `delivery-team/skills/presentation` | `types` | NONE — references-only path retained (correct per AC-5 option b) |

All 9 paradigm sub-skill files match the `.*/skills/[^/]+/[^/]+/SKILL\.md` regex declared in ADR §Marketplace discoverability invariant. None deviate from the canonical shape (no `<plugin>/skills/<variant>/` shortcut, no double-nesting, no lateral peers).

**Finding:** PASS. Canonical directory shape honored on every NEW and EXISTING paradigm sub-skill in scope.

---

## Gate 3 — Ruling 2 (`disable-model-invocation: true`) applied to sub-skills only, not parents

**Criterion:** ADR-tk4-002 §Sub-skill SKILL.md frontmatter contract requires `disable-model-invocation: true` on every paradigm sub-skill; ADR §Marketplace discoverability invariant requires that the flag NOT appear on top-level (parent) skills.

**Evidence (`grep -lr "disable-model-invocation: true" --include=SKILL.md`):**

Files matched (9):
- `research-agent/skills/research-types/{exploratory,descriptive,explanatory,evaluative,comparative}/SKILL.md` (5)
- `delivery-team/skills/user-feedback/skills/personas/{gamers,web-app,enterprise,demographic}/SKILL.md` (4)

Files NOT matched (parents — correctly absent):
- `research-agent/SKILL.md` ✓
- `delivery-team/skills/user-feedback/SKILL.md` ✓
- `delivery-team/skills/presentation/SKILL.md` ✓
- All other top-level plugin/skill SKILL.md files ✓

100% of matched paths satisfy the regex `.*/skills/[^/]+/[^/]+/SKILL\.md`. Zero top-level violations. The implementation report's CI-lint footnote about a prior prose-only false positive in `research-agent/SKILL.md` is correctly resolved (rewording to avoid the literal `: true` token outside frontmatter).

**Finding:** PASS. Ruling 2 marketplace-discoverability invariant fully honored.

---

## Gate 4 — Cache-prefix preserved on parents

**Criterion:** ADR-tk4-002 §Cache-prefix impact states that parent-router additions must land BELOW the 2k-byte cache-prefix region, and `governance/cache-prefix-hash.txt` must remain unchanged for any tracked file.

**Evidence:**
- `governance/cache-prefix-hash.txt` content: `f997ec25df5328329e431309f6dd6db948d354d5360dcb4c6ac409b8815a9eb9  delivery-team/skills/delivery-flow/SKILL.md` — single line, single tracked file (delivery-flow), unchanged by Story 4. The two parent skills modified or verified by Story 4 (`research-agent/SKILL.md`, `delivery-team/skills/user-feedback/SKILL.md`) are NOT in the tracked scope, so AC-4 ruling holds trivially per ADR-tk4-002 §Cache-prefix impact paragraph 1.
- `research-agent/SKILL.md` dispatch table sits at lines 57-69 — the description trim (655→454 chars) does touch the cache-prefix region (lines 1-11, frontmatter), but research-agent is not a tracked file in `cache-prefix-hash.txt`. ADR §Cache-prefix impact explicitly acknowledges this case ("research-agent is not in `governance/cache-prefix-hash.txt`, so AC-4 ruling holds. If Story 5 expands the hash scope to include research-agent, the re-freeze will pick up this trim alongside the +3 governance-frontmatter lines per ADR-tk4-003").
- `delivery-team/skills/user-feedback/SKILL.md` dispatch table sits at line 99, byte offset 6636 — well below the 2k threshold. No cache-prefix-region edits by Story 4 (Story-3 ownership).
- Story 5 (W3-9 governance frontmatter rollout per ADR-tk4-003) remains the SOLE cache-prefix re-freeze authorized in this wave.

**Finding:** PASS. Cache-prefix integrity preserved; the only tracked file (`delivery-flow/SKILL.md`) is untouched by Story 4, and the parent-router additions to non-tracked files land below the 2k-byte threshold.

---

## Gate 5 — Existing volatility/ddd precedent (architect/paradigms/) consistent with new sub-skills

**Criterion:** ADR-tk4-002 §Decision "Architect paradigms (volatility / ddd) backlog" explicitly grandfathers the existing `delivery-team/skills/architect/paradigms/{volatility,ddd}/SKILL.md` precedent for this wave, while declaring W4 follow-up to migrate them to `architect/skills/paradigms/<paradigm>/` and add `disable-model-invocation: true`. New sub-skills must be consistent with the *intent* of that precedent (router-only, variant-scoped, paradigm-axis-organized) even though the precedent's directory shape and frontmatter differ.

**Evidence — comparison of precedent vs. new shape:**

| Aspect | Existing volatility/ddd (grandfathered) | New research-types + personas (Story 4) | Consistent? |
|---|---|---|---|
| Directory shape | `architect/paradigms/<paradigm>/` (no `skills/` segment, single `<paradigm>` segment) | `<plugin>/skills/<axis>/<variant>/` (full canonical shape) | Intentionally divergent — ADR explicitly grandfathers existing shape; new shape is the canonical going-forward path. W4 backlog item logged. |
| Sub-skill scope | One paradigm = one sub-skill (volatility, ddd) | One axis variant = one sub-skill | Consistent — both isolate one variant of one axis |
| Frontmatter `disable-model-invocation` | Absent (legacy, pre-Ruling 2) | Present and `true` (mandated) | Intentionally divergent per ADR-tk4-002 grandfather clause; W4 will retrofit |
| Frontmatter `tier` | `tier: C` | `tier: C` | ✓ Consistent |
| Frontmatter `allowed-tools` | `[Read, Edit, Write, Bash, Skill, ToolSearch]` | `[Read, Edit, Write, Bash, Skill, ToolSearch]` | ✓ Consistent |
| Sub-skill loads only its own references | Yes (`shared_refs` declares parent shared set, then own `references/`) | Yes (sub-skill body loads only its own type-specific pattern + phase adaptations) | ✓ Consistent intent |
| Router-driven dispatch | Architect SKILL.md "Paradigm Router" §Detection Priority Chain dispatches via `Skill` tool | Parent SKILL.md "Sub-Skill Dispatch" table dispatches via `Skill` tool | ✓ Consistent dispatch model |
| Marketplace discoverability of parent | Architect parent SKILL.md remains discoverable | Each new parent (research-agent, user-feedback) remains discoverable | ✓ Consistent invariant |

The shape and frontmatter divergences are exactly what ADR-tk4-002 §Decision and §Alternatives both anticipate and authorize. The grandfather clause explicitly states "the existing `delivery-team/skills/architect/paradigms/{volatility,ddd}/SKILL.md` precedent is **explicitly grandfathered for this wave**. Migrating them to `architect/skills/paradigms/<paradigm>/` is mechanical (path move + add `disable-model-invocation: true` frontmatter key) but out of Wave 3 scope per BACKLOG-104 §Out of scope. Log as W4 follow-up." The Story 4 implementation correctly does NOT touch the grandfathered files.

**Finding:** PASS. New sub-skills are consistent with the *router-only, variant-scoped, paradigm-axis-organized intent* of the grandfathered precedent. The directory-shape and `disable-model-invocation` divergences are the precise improvements ADR-tk4-002 mandates for new work, with the grandfathered files explicitly excluded from this wave's scope and logged for W4. CLAUDE.md's stale `architect/skills/paradigms/` reference is opportunistically resolved in W3-12 per the ADR Context section.

---

## Cross-cutting architect observations (advisory; not blockers)

1. **W4 backlog candidate confirmed**: Migrate `architect/paradigms/{volatility,ddd}/` to `architect/skills/paradigms/<paradigm>/` and add `disable-model-invocation: true`. Mechanical work; do NOT bundle with another structural change to keep the diff atomic.
2. **CI-lint hardening (forward-look)**: The implementation report's Gate-3 footnote correctly identifies that raw `grep -lr "disable-model-invocation: true" --include=SKILL.md` is prose-fragile. Replacing it with a frontmatter-aware Python check in `.github/workflows/marketplace-discoverability-lint.yml` is a sound non-blocking refinement; defer to ops/CI lane per their workflow ownership.
3. **Presentation deferral integrity**: AC-5 option (b) is the right call this wave (parent already at 182/300 lines well under Tier-B ceiling; "smallest reversible step" honored). Re-evaluate at BACKLOG-106+ ONLY if telemetry shows references-only loads exceed budget; do not preemptively split.
4. **Decision rule for future axes** (now codified by this wave's ADR): ≥3-mutually-exclusive-variants AND variants don't share substantial code → paradigm sub-skill (this pattern). <3 variants OR variants share substantial code → reference extraction (ADR-tk4-001 pattern). Architect role should cite this rule when reviewing future axis-decomposition decisions.

---

## DoD Gate Results — round 1

| Gate | Criterion | Result |
|---|---|---|
| 1 | Implementation honors ADR-tk4-002 paradigm pattern (router parent + variant sub-skills) | **PASS** |
| 2 | Sub-skill structure follows `<plugin>/skills/<axis>/<variant>/SKILL.md` | **PASS** |
| 3 | Ruling 2 (`disable-model-invocation: true`) applied to sub-skills only, not parents | **PASS** |
| 4 | Cache-prefix preserved on parents | **PASS** |
| 5 | Existing volatility/ddd precedent (architect/paradigms/) consistent with new sub-skills | **PASS** |

**5 of 5 gates PASS — round 1, no rework required from architect role.**

---

## Status

**STATUS: DONE** — Story 4 (W3-8) honors ADR-tk4-002 in full on every gate the architect role owns. The paradigm sub-skill contract is now materialized on two production axes (research-types ×5, personas ×4) and intentionally deferred on the third (presentation types ×9) per the ADR's own conditional clause. The pattern is ready for Wave 4+ adoption on additional axes (developer 14-language, architect 11-role) per BACKLOG-106+.

— Saruman of Many Colours, Solution Architect, run-2026-05-09-tk4. *"The contract held; the cuts were clean; the precedent stands grandfathered until its own wave. Architect signs off."*
