# Product Owner Review -- Idea Brief (Gate 1)

**Reviewer**: Product Owner (Gandalf)
**Date**: 2026-04-05
**Artifact**: `.delivery/artifacts/01-idea/po/idea-brief.md`
**Project**: DESIGN Project Type for delivery-flow (FEATURE)
**Source**: GitHub Issue #72
**Verdict**: DONE

*"All we have to decide is what to do with the time that is given us -- and sometimes, that decision is to think before we build."*

---

## Criteria Evaluation

### [PASS] [blocking] Problem statement present and clear

The brief names the gap with precision: delivery-flow has no first-class mode for design-only engagements. It enumerates the three failing alternatives a team must currently choose from -- (1) running a full pipeline and abandoning after Architect (wasteful, leaves state mid-stride, upsets the retrospective hook), (2) using DOCS_ONLY (which skips the very design work needed), and (3) escaping the pipeline entirely (violating the route-through-pipeline rule). The compounding harm -- design work either contaminated by implementation pressure or escaping pipeline governance -- is named explicitly. A reader can reproduce the failure mode without further inquiry.

### [PASS] [blocking] Target users identified

Five distinct user groups are enumerated, each with the specific need this feature serves:

1. **Solution Architects** preparing design packages for future implementation teams or quarters.
2. **Product Owners and Tech Leads** running discovery / pre-funding engagements where the deliverable is a coherent design.
3. **Enterprise / Platform teams** producing reference architectures, ADRs, and PRDs for downstream consumption.
4. **Consultants and internal advisors** delivering design artifacts as the contractual outcome.
5. **Plugin maintainers (us)** dogfooding design-only work through the same pipeline as everything else.

Each group has a concrete reason to want a DESIGN type, and the dogfooding constituency ensures the feature has an internal champion.

### [PASS] [blocking] Goals are measurable

Six goals, each with an observable, binary acceptance signal:

| # | Goal | Measurable? |
|---|------|-------------|
| 1 | First-class DESIGN project type registered alongside the existing six | Yes -- inspect detection table and routing matrix |
| 2 | Stage routing: full Idea/Refine/Design/Architect; skip Plan/Dev/UAT | Yes -- run pipeline; verify which stages execute |
| 3 | Coherent output package (PRD + design + architecture + ADRs) ready as input for a future run | Yes -- inspect produced artifacts |
| 4 | Documentation parity across SKILL.md, references, CLAUDE.md, README.md, marketplace.json | Yes -- diff inspection on a single PR |
| 5 | Configurable override via `routing.force_type: DESIGN`, validated by config schema | Yes -- schema check + integration test |
| 6 | No regressions to the six existing project types | Yes -- regression check on routing matrix |

Each goal is testable in DoD without further refinement.

### [PASS] [blocking] Constraints documented

Eight well-targeted constraints, all of them honoring repo discipline and memory:

1. **Light != skip** -- the brief deliberately uses *skip* for Plan/Dev/UAT because DESIGN is definitionally a design-only mode. This is a called-out exception to the general rule, and the brief instructs `pipeline-stages.md` to fence the distinction so it does not bleed into other types. Honors the `feedback_no_skip_stages` memory directly.
2. **Markdown-only edits calibrate one tier lower** -- effort sized accordingly; no code, no scripts, no schema generators.
3. **All work routes through the pipeline** -- this feature dogfoods the very mechanism it extends.
4. **Documentation parity is non-negotiable** -- CLAUDE.md, README.md, marketplace.json updated in the same PR.
5. **Schema versioning** -- `config-schema.md` (v2.6) is the source of truth; extension protocol followed.
6. **Wizard** -- PR #74 removed Q1, so detection guidance updates only, no interactive prompt added.
7. **Backward compatibility** -- existing configs without DESIGN must continue to work unchanged.
8. **Retrospective hook compatibility** -- the Stop hook must still fire correctly when a DESIGN run terminates after Architect.

The constraints prevent scope drift, protect backward compatibility, and operationalize repo memory (light != skip, dogfooding, doc parity).

### [PASS] [blocking] Initial scope defined

Eight files in scope, each with an explicit per-file change description:

| File | Change |
|---|---|
| `delivery-team/skills/delivery-flow/SKILL.md` | Add DESIGN to routing matrix and detection table |
| `references/project-types.md` | New DESIGN section with detection signals, examples, rationale |
| `references/pipeline-stages.md` | Document DESIGN routing and fence the *skip* exception |
| `references/setup-wizard.md` | DESIGN detection guidance for auto-detect |
| `references/config-schema.md` | DESIGN as valid `routing.force_type` enum value; schema bump |
| `CLAUDE.md` | Update project-type list |
| `README.md` | Update project-type enumeration |
| `.claude-plugin/marketplace.json` | Update delivery-flow description if it enumerates types |

The canonical routing matrix (full Idea/Refine/Design/Architect; skip Plan/Dev/UAT) is included in the brief itself, making it the contract for downstream stages. Detection signals are seeded but flagged as "to be refined in Stage 2" -- appropriate for Idea depth.

### [PASS] [blocking] Out of scope defined

Seven explicit exclusions, each blocking a plausible scope-creep path:

1. New scripts, hooks, or schema-generation code -- documentation/configuration only.
2. New wizard question -- detection guidance only, no interactive prompt.
3. Changes to other project types' routing -- the existing six are untouched.
4. A "DESIGN-light" variant -- one depth profile; future variants proposed separately.
5. Automatic handoff into a follow-on implementation run -- output is *ready* but wiring is a separate feature.
6. Retroactive migration of existing in-flight pipelines.
7. Net-new artifacts or templates -- DESIGN reuses existing PRD, design, architecture, and ADR formats.

Boundaries are crisp. A developer tempted to "add a wizard question while we're in there" or "build the auto-handoff" knows those are out of bounds.

### [PASS] [blocking] Business value evident

The value is articulated explicitly and implicitly: DESIGN brings pure-design engagements *inside* pipeline governance for the first time, so they stop being either contaminated by implementation pressure or escaping pipeline governance entirely. It serves a real and named user population (Solution Architects, pre-funding discovery, reference-architecture teams), it enables dogfooding of design-only work through the same pipeline, and it produces a coherent output package ready to feed a future implementation run. The bundling rationale ("first-class mode") prevents the half-pipeline-then-abandon antipattern that today wastes effort and leaves the retrospective hook unhappy.

---

## Notes for Downstream Stages

- **Refine**: turn each of the six goals into explicit acceptance criteria. Refine the detection signals into a concrete decision rule (precedence order vs. existing types matters -- DESIGN must not poach signals from GREENFIELD or DOCS_ONLY).
- **Design**: the *skip* fence in `pipeline-stages.md` is the most delicate text in this feature. Draft it so a future maintainer cannot mistake DESIGN's intentional skipping for permission to skip light stages elsewhere.
- **Architect**: examine `references/config-schema.md` (v2.6) and the existing routing logic deeply before proposing the schema bump. Validate and build on the existing extension protocol; do not reimagine it.
- **Architect**: explicitly verify the Stop / retrospective hook still fires correctly when Architect is the terminal stage. This is the highest-risk integration point.
- **Plan / Tech Writer**: documentation parity (CLAUDE.md, README.md, marketplace.json) is a hard constraint -- first-class tasks, not afterthoughts.
- **No Dev / UAT stages will run** for this feature's own delivery if it itself is routed as DESIGN; however, this feature is FEATURE-typed (it ships markdown/config edits to a real repo), so the normal pipeline applies.

---

## Summary

*"A brief is judged not by its length, but by whether it lights the road ahead. This one does."*

All seven Gate 1 criteria pass. The brief is well-structured: a clearly named gap, five user groups with concrete needs, six measurable goals, eight discipline-honoring constraints (with the *light != skip* exception called out explicitly and fenced), an eight-file scope table with a canonical routing matrix, and seven crisp out-of-scope items. The brief honors repo memory directives (light != skip, route-through-pipeline, dogfooding, doc parity) and stays at the *what/why* layer without solutioning leakage.

*Speak, friends, and proceed. The road to Refine is open.*

-- Gandalf, Product Owner
