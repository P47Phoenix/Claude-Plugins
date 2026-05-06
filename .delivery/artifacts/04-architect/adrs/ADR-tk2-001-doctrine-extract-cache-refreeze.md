---
id: ADR-tk2-001
title: "Doctrine extraction from delivery-flow/SKILL.md + cache-prefix re-freeze"
status: Accepted
work_items: [W2-1, W2-4]
wave: 2
author: Architect (delivery-team:architect, Celebrimbor persona)
created: 2026-05-05
supersedes: governance/cache-prefix-hash.txt (Wave 1 hash aea33d57... becomes historical)
---

# ADR-tk2-001: Doctrine Extraction + Cache-Prefix Re-Freeze

## Context

`delivery-team/skills/delivery-flow/SKILL.md` stands at **999 lines** post-Wave-1 against
Tier-A budget ≤500. The 499-line over-budget is the largest target in Wave 2. Most over-budget
content is prose doctrine elaborating on routing anchors already inline.

Wave 1 cache prefix (bytes 0..2048) frozen at SHA-256
`aea33d5732e31ab6455dda3675f7ad536d5d0e440a52dd0c1802ec2dabf03db9`. Doctrine extraction
structurally alters the prefix region; this ADR governs the deliberate one-time re-freeze.

**F-08 risk (Opus 4.7):** Reduced default dispatch breadth means Phase 0–4 routing anchors
and the Stage Routing Matrix MUST stay inline as behaviourally load-bearing gates.
Prose elaborations (the "why" behind the anchors) are safe to move.

**W2-4 dependency:** Config/Commands/Manifest tables (~30 lines) MUST be in the same PR
or immediately sequenced to avoid a double hash-update cycle.

## Decision

### A. F-08 Anchor Preservation List (STAY inline in delivery-flow/SKILL.md)

The following content is load-bearing and MUST remain inline:

| Anchor | Location | Lines (est.) | Rationale |
|--------|----------|--------------|-----------|
| Phase 0 setup wizard skeleton (full) | Lines 80–214 | ~135 | Branch state machine; config-load; alias-load; all 4 config states |
| Phase 1 project-type detect (full signal table + detection rules + declaration) | Lines 216–261 | ~46 | Routing entrypoint; F-08 dispatch trigger |
| Phase 2 memory load (full tiered protocol + injection template) | Lines 263–294 | ~32 | Lesson injection wiring |
| Phase 3 routing (full Stage Routing Matrix table + Depth Definitions + CRITICAL note) | Lines 296–333 | ~38 | Stage dispatch selector |
| Phase 4 protocol (Steps 1–10 all named inline; behavioral detail included) | Lines 335–614 | ~280 | Prime Directive; One Role = One Sub-Agent invariant (1-line); Two-Channel constraint (1-line); DoD wiring; self-recovery |
| Stage Definitions pointer | Lines 617–624 | ~8 | Pointer to stages.yml + pipeline-stages.md |

All 10 Phase 4 steps MUST be named inline. Steps 6, 7, 9 retain inline prose — they
carry dispatch semantics Opus 4.7 uses for role-count enforcement.

### B. Doctrine Extraction List (MOVE to orchestrator-doctrine.md)

Move to `delivery-team/references/shared/orchestrator-doctrine.md`:

| Block | Current lines (est.) | Reason safe to move |
|-------|--------------------|---------------------|
| Design Principle intro paragraph + "never produces domain artifacts" elaboration | ~14 | Prose elaboration; pointer stays |
| Core Principles 1–7 full text (lines ~22–68) | ~47 | Prose; F-08 anchors preserved via Phase 4 inline steps |
| Model awareness note (Opus 4.7 F-08 intro, first occurrence lines ~71–77) | ~7 | Moved to doctrine; Phase 4 retains behavioural gate sentences |
| Common Orchestrator Anti-Patterns enumeration (lines ~628–680) | ~53 | Reference text; 1-line summary pointer stays inline |
| Team DoD Protocol full prose (lines ~681–717) | ~37 | Phase 4 Step 7 retains dispatch semantics; this is elaboration |
| Dynamic Escalation Protocol detail (triggers table + format template, lines ~720–765) | ~46 | Phase 4 Step 9 retains escalation trigger; format moves |
| Cross-Stage Artifact Flow narrative (lines ~768–789) | ~22 | Reference table; pointer stays |
| Memory and Self-Learning detail blocks (lines ~793–855) | ~63 | Operational protocol; Phase 4 Step 8.5 retains state write |
| Guardrails enumerated detail (lines ~860–914) | ~55 | 1-line summaries retained inline; elaborations move |
| Theme-Gated Reporting 4-paragraph protocol (inside Phase 4 Step 4 / Steps 9–10) | ~30 | Prose detail; behavioral anchors (3 output slots named) stay in Phase 4 |

**Total estimated extraction (W2-1): ~374 lines** + ~106 lines cleanup to hit target.

### C. Batching Math

```
delivery-flow/SKILL.md:
  baseline (post-Wave-1):        999 lines
  W2-1 doctrine extraction:     −480 lines  (374 doctrine + ~106 cleanup)
  W2-4 config/commands/manifest: −30 lines
  ─────────────────────────────────────────
  target:                        489 lines  (≤500 Tier-A ✓)
```

Stage 6 Dev MUST verify `wc -l` post-extraction. If >520 lines, restore anchors first — correctness > line count.

### D. Cache-Prefix Re-Freeze Contract

1. Wave 1 hash `aea33d5732e31ab6455dda3675f7ad536d5d0e440a52dd0c1802ec2dabf03db9`
   is **retired** as of this ADR. Recorded here for audit trail only.
2. After W2-1 merges (and W2-4 in the same PR or immediately after),
   compute new SHA-256 of bytes 0..2048 of `delivery-team/skills/delivery-flow/SKILL.md`:
   ```bash
   head -c 2048 delivery-team/skills/delivery-flow/SKILL.md | sha256sum
   ```
3. Write the new hash to `governance/cache-prefix-hash.txt`.
4. Re-baseline the CI hash-check script to the new hash value.
5. This is a **one-time deliberate prefix change**. All future SKILL.md edits that
   touch bytes 0..2048 REQUIRE a new ADR citing cache-cost impact before merging.
6. W2-4 (config/commands/manifest tables) touches the post-prefix region only —
   verify bytes 0..2048 are unchanged after W2-4 before closing the hash cycle.

### E. Dogfood-Validation Gate (Architect-mandated for W2-1)

BEFORE merging Story 1 (W2-1 + W2-4), Architect MUST validate the skeleton
`delivery-flow/SKILL.md` via a synthetic pipeline run covering:
- Phase 0: state detection → config detection → config load
- Phase 1: project-type detection (FEATURE signal)
- Phase 2: memory load (index.md read → lessons injected)
- Phase 3: Stage Routing Matrix → at least one stage dispatch (Stage 2 Refine)

**Acceptable dogfood:** This very Wave 2 pipeline continues without routing breakage
AFTER Story 1 merges (recursive dogfood). Routing misfires in any phase → restore
inline anchors; doctrine file absorbs growth to compensate.

### F. plugin-dev:skill-development

W2-1 MUST pre-load `plugin-dev:skill-development` before any SKILL.md or references
file is created/modified (per CLAUDE.md convention FR-12).

## Consequences

**Positive:**
- delivery-flow/SKILL.md: 999 → **~489 lines** (Tier-A ≤500 ✓)
- Cold-load token savings: ~480 lines × ~20 tok ≈ **9,600 tokens/load**; ≥30% pipeline reduction
- Cache prefix stabilized for Wave 3+; doctrine centralized for single-source-of-truth editing

**Negative / Historical:**
- Reviewers must consult `orchestrator-doctrine.md` for full behavioral intent
- One-time cache miss on post-freeze first load
- F-08 regression risk if Phase 4 behavioral gate removed → dogfood gate (§E) mitigates
- Wave 1 hash `aea33d57...` superseded; Wave 3+ SKILL.md work rebases on new hash

## Alternatives Considered

**1. Full SKILL.md rewrite (rejected):** Rewrite from scratch against a 500-line
target. Risk: destroys institutional memory, introduces behavioral regressions.
The partial extraction approach preserves the existing routing logic.

**2. Split delivery-flow/SKILL.md into two files (rejected):** Primary (≤500) +
overflow file. Requires changes to plugin-dev skill loading protocol. The doctrine
file pattern is already established (stages.yml precedent from Wave 1).

**3. Defer doctrine extraction to Wave 3 (rejected):** Would leave the heaviest
over-budget skill untouched for another wave, blocking the ≥30% token-reduction
goal and delaying the cache-prefix stabilization needed for W2-4 sequencing.
