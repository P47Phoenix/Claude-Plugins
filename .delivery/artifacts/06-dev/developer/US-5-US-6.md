# US-5 + US-6 — Transformation Phase 2/3 refs + templates

**Dev:** Gimli (developer alias) | **Run:** run-2026-04-09-c4d1 | **Stage:** 06-dev

## Delivered

1. `delivery-team/skills/architect/references/transformation-phase-2-to-be.md` (72 lines)
   - Architect-led TO-BE model on shared constraints.yml schema
   - Golden Rule citation requirement (Löwy Ch. 2) enforced by check_dod_constraints.py
   - Forbidden vocabulary enforcement per prior-run ADR-003
   - Diffable AS-IS vs TO-BE; anti-patterns covered
2. `delivery-team/skills/architect/references/transformation-phase-3-roadmap.md` (100 lines)
   - 8-field roadmap step schema verbatim from architecture.md §6
   - 30% no-big-bang formula + <4 subsystems edge case per ADR-002
   - Independently-shippable rule, 4-driver ordering rationale, preserved invariants contract
   - ≥3 step minimum; escape valve to 7
3. `delivery-team/skills/delivery-flow/references/templates/transformation-use-cases-template.md` (49 lines)
   - Phase 1A 7-field schema + worked example (plugin-registration use case, confidence=low)
4. `delivery-team/skills/delivery-flow/references/templates/transformation-roadmap-template.md` (59 lines)
   - Header block, 8-field per-step template, closing no-big-bang summary table
   - Worked example: pricing-policy extraction step at 14% subsystem change

## Inputs honored

- architecture.md §6 (roadmap step schema — all 8 fields copied verbatim into Phase 3 doc and template)
- architecture.md §7 (big-bang check formula + <4 subsystem edge case)
- ADR-002 (30% threshold, edge case, escape valve to 7)
- PRD FR-4 (TO-BE on shared schema, Golden Rule citation), FR-5 (roadmap, ≥3 steps, 30% rule, independently shippable)

## Line caps

All four files under their specified ceilings (160/180/80/100).

STATUS: DONE
ARTIFACT: .delivery/artifacts/06-dev/developer/US-5-US-6.md
SUMMARY: Forged TO-BE and roadmap refs plus both templates — 30% no-big-bang rule hammered in, Golden Rule citation chained, forbidden vocab warded. By me beard, the stonework holds.
