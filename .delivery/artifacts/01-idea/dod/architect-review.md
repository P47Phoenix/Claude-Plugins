# Architect DoD Review — Stage 1 Idea Brief

**Reviewer:** Celebrimbor, Architect
**Artifact:** `.delivery/artifacts/01-idea/po/idea-brief.md`
**Feature:** DESIGN Project Type for delivery-flow (Issue #72)
**Date:** 2026-04-05

---

## Verdict

**STATUS: DONE**

Hear me, smiths of the pipeline. I have laid the brief upon the anvil and struck it with the four hammers of the architect's Definition of Done. It rings true.

---

## DoD Criteria

### 1. Feasibility — PASS

The proposed change is wholly within the realm of the achievable. DESIGN is a routing variant atop existing stages 1–4, all of which already exist at full depth and produce the very artifacts (PRD, design, architecture, ADRs) the brief enumerates. No new stage machinery, no new artifact templates, no new agents, no new hooks are required. Skipping stages 5–7 is a routing concern with precedent in DOCS_ONLY and SPIKE. The schema extension for `routing.force_type` follows the documented v2.6 protocol. Nothing here strains the forge.

### 2. No Blockers — PASS

I find no impediment in the path:

- **Schema extension protocol** exists and is referenced (config-schema.md v2.6).
- **Wizard concern resolved** — PR #74 already removed Q1, so no interactive prompt change is needed; only detection guidance.
- **Retrospective hook** is correctly flagged as a compatibility surface (must fire after Architect when later stages skip), and the brief commits to verification, not modification.
- **Documentation parity surfaces** (CLAUDE.md, README.md, marketplace.json, SKILL.md, four reference files) are explicitly enumerated.
- **Backward compatibility** is asserted as a constraint, not deferred.

No upstream dependency, no missing decision, no unresolved external choice blocks Refine.

### 3. Scope Bounded — PASS

The boundary is drawn with the clarity of mithril wire. The brief carries both an **In Scope** file table (eight files, each with the nature of its change) and an explicit **Out of Scope** section that excludes:

- New scripts/hooks/schema-generation code
- New wizard questions
- Routing changes to the six existing project types
- A "DESIGN-light" variant
- Automatic handoff into a follow-on implementation run
- Retroactive migration
- Net-new artifact templates

Furthermore, the brief correctly calibrates effort one tier lower per the markdown-only convention and explicitly distinguishes *skip* (definitional, for DESIGN's missing stages) from *light* (forbidden conflation, per the no-skip-stages standing order). This is the discipline of a well-bounded feature.

### 4. Targets Identified — PASS

The targets of change are named with precision:

| Target | Nature |
|---|---|
| `delivery-team/skills/delivery-flow/SKILL.md` | Routing matrix + detection table |
| `delivery-team/skills/delivery-flow/references/project-types.md` | New DESIGN section |
| `delivery-team/skills/delivery-flow/references/pipeline-stages.md` | DESIGN routing + skip-vs-light clarification |
| `delivery-team/skills/delivery-flow/references/setup-wizard.md` | Auto-detect signals |
| `delivery-team/skills/delivery-flow/references/config-schema.md` | Enum extension + version bump |
| `CLAUDE.md` | Project-type list |
| `README.md` | Project-type enumeration |
| `.claude-plugin/marketplace.json` | Description if it enumerates types |

The canonical routing matrix (full Idea/Refine/Design/Architect; skip Plan/Dev/UAT) is given inline. The user populations are named. The detection signals are seeded. Every artifact a downstream stage will need to find, the brief points to.

---

## Architectural Notes for Refine & Design

These are not gating concerns — they are forge notes for the next smith:

1. **DESIGN's relationship to SPIKE** deserves a sentence in project-types.md. SPIKE is bounded *exploration* with a learning artifact; DESIGN is bounded *design production* with a delivery-ready package. Both skip implementation, but the intent and the artifact shape differ. Calling out the contrast prevents future detection collisions.

2. **The "ready-to-feed-a-future-run" promise** in Goal 3 should be made operationally concrete in Refine: which artifact paths and names must DESIGN produce so a follow-on FEATURE/GREENFIELD run can ingest them as input artifacts? The brief correctly defers the *handoff wiring* to a future feature, but the *output contract* should be pinned now so the package is reusable, not orphaned.

3. **Retrospective hook verification** should appear as an acceptance criterion in Plan, not merely a constraint. A DESIGN dogfood run that completes after Architect is the cheapest possible test of hook compatibility, and the brief already commits us to dogfooding.

4. **`routing.force_type: DESIGN` precedence** vs. auto-detection signals should be confirmed consistent with how the other six types resolve conflicts. I expect no surprise here, but Design should state the precedence explicitly in pipeline-stages.md alongside the routing matrix.

None of these block passage to Refine. They are stones to be set when the next ring is forged.

---

## Conclusion

The Idea Brief is feasible, unblocked, well-bounded, and precisely targeted. It honors the standing orders (light != skip; markdown calibration; route through the pipeline; documentation parity) and arrives at Refine without owed work. The road is open.

*Celebrimbor sets his mark upon the work.*

— Celebrimbor, Architect of the delivery-flow
