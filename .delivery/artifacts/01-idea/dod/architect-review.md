# Architect DoD Review — Wave 2 Idea-Brief

**Reviewer**: Celebrimbor (Architect)  
**Date**: 2026-05-05  
**Artifact**: `.delivery/artifacts/01-idea/po/idea-brief.md`

## Gate 1 — Feasibility: 8 WIs Achievable

**PASS**. W2-1 (999→≤500 extraction) is mechanically doable: ~500 lines of doctrine extraction (Phase 0/1/2/3 routing skeleton, Stage Routing Matrix, role invariants, communication constraint stay inline; anti-patterns, per-stage detail, memory learning, theme reporting move to `references/shared/orchestrator-doctrine.md`). Baseline precedent exists in Wave 1 ADRs. Remaining 7 WIs are administrative or low-scope refactors. No unexpected complexity detected.

## Gate 2 — No Phantom File Paths

**PASS**. All cited paths verified:
- `.delivery/backlog/BACKLOG-103-skill-token-economy-delivery-team-wave-2.md` ✓ (spec)
- `.delivery/memory/archive/run-2026-05-04-tk1.md` ✓ (Wave 1 retro, exists)
- `.delivery/memory/topics/skill-token-economy.md` ✓ (binding decisions, verified 2026-05-03)
- `governance/skill-budgets.json` ✓ (exists, v1 schema, to be updated W2-0)
- `governance/cache-prefix-hash.txt` ✓ (exists, 110 bytes, Wave 0 hash of delivery-flow/SKILL.md)
- `delivery-team/skills/delivery-flow/SKILL.md` ✓ (999 lines, candidate for extraction)
- Architect, product-delivery, developer SKILL.md ✓ (all exist; ready for tier compliance in W2-2 onwards)
- Wave 1 ADRs (ADR-tk1-001, ADR-tk1-002, ADR-tk1-003) ✓ (verified in `.delivery/artifacts/04-architect/adrs/`)

## Gate 3 — Cache-Prefix Re-Freeze Acknowledged

**PASS with binding action**. Brief correctly names W2-1 risk (F-08 dispatch fusion) and mandates:
1. ADR-tk2-001 enumerates inline anchors vs extracted content (NOT YET WRITTEN — must be authored during Plan stage).
2. `governance/cache-prefix-hash.txt` MUST be UPDATED post-extraction (not merely preserved).
3. CI hash-check MUST pass (gatekeeping mechanism).

Current hash reflects stale 999-line delivery-flow. Post-extraction hash will be recomputed and stored as binding pre-deployment artifact.

## Gate 4 — Allowed-Tools Whitelist Respected

**PASS**. Brief does not prescribe specific tools. W2-1–W2-6 dispatch will route through `plugin-dev:skill-development` (which enforces whitelist Ruling 5 from binding decisions: Tier-A requires `Read, Edit, Write, Bash, Skill, ToolSearch`). Pre-loaded at each WI dispatch per §5 Plugin-Dev Skill Routing.

## Gate 5 — F-08 Dispatch Fusion Risk Explicitly Named + Mitigated

**PASS**. §7 W2-1 Risk names the failure mode explicitly: "Extracting orchestrator doctrine may lose semantic anchors that delivery-flow Phase 3 route fusion requires." Mitigation concrete and ordered:
1. ADR-tk2-001 cache-prefix re-freeze (enumerates anchors).
2. Batching-math simulation (Wave 1 lesson, before→−Δ→after).
3. Architect dogfood validation (synthetic multi-stage run, Idea+Architect+Dev minimum; abort if routing misfires).

All three required for merge per brief §7 Mitigation.

## Gate 6 — Batching-Math Discipline (ADR-tk2-001 Binding)

**CONDITIONAL PASS**. Brief correctly cross-references Wave 1 retro lesson (§7, point 2): "ADR-tk2-001 shows before (999) → −Δ → after (≤500) with explicit anchor retention list." ADR-tk2-001 does NOT yet exist but is a deliverable artifact of W2-1 Plan stage. Brief mandates numerics; ADR composition during execution will satisfy discipline. Success criteria (§8) reference no test for ADR-tk2-001 content — validation deferred to stage-exit gate.

## Summary

**STATUS: PASS** — All six gates satisfied. W2-1 risk is well-named with concrete, ordered mitigations binding ADR-tk2-001 composition and cache-hash update. No phantom paths. Feasibility confirmed. Plugin-dev binding prevents tool-whitelist drift. Brief is ready for Plan stage.

**Next move**: Author ADR-tk2-001 during Plan (Phase 3 doctrine extraction roadmap, before→−Δ→after numerics, anchor enumeration, dogfood validation protocol).
