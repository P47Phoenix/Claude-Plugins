# Idea Brief: DESIGN Project Type for delivery-flow

*"All we have to decide is what to do with the time that is given us — and sometimes, that decision is to think before we build."* — Gandalf

**Type:** FEATURE
**Source:** GitHub Issue #72
**Author:** Product Owner (Gandalf)
**Date:** 2026-04-05

---

## Problem

The delivery-flow pipeline carries every project type — GREENFIELD, FEATURE, BUG_FIX, GAME_DEV, SPIKE, DOCS_ONLY — straight through the mountain pass to implementation. There is no road for the fellowship that wishes only to *plan the journey*: to gather requirements, design the system, and architect the solution without yet drawing a sword of code.

Today, a team that wants a pure design engagement must either:

1. Run a full pipeline and manually abandon it after Architect (wasteful, leaves the pipeline state mid-stride and the retrospective hook unhappy), or
2. Run DOCS_ONLY (which skips the very design and architecture work they need), or
3. Work outside the pipeline entirely (violating the cardinal rule that all work routes through delivery-flow).

None of these are honest paths. The pipeline lacks a first-class mode for *design-only* engagements, and so design work either gets contaminated by half-built implementation pressure or escapes pipeline governance altogether.

## Target Users

- **Solution Architects** preparing a design package for a future implementation team or quarter.
- **Product Owners & Tech Leads** running discovery / pre-funding engagements where the deliverable is a coherent design, not running code.
- **Enterprise / Platform teams** producing reference architectures, ADRs, and PRDs that downstream teams will later implement.
- **Consultants and internal advisors** delivering design artifacts as the contractual outcome.
- **Plugin maintainers (us)** who want to dogfood design-only work through the same pipeline as everything else.

## Goals

1. **First-class DESIGN project type** registered alongside the existing six, with its own detection signals and routing.
2. **Stage routing** that runs Idea, Refine, Design, and Architect at *full* depth and *skips* Plan, Development, and UAT — producing a complete design package without implementation pressure.
3. **Coherent output package** comprising PRD, design artifacts, architecture documentation, and ADRs — ready to be handed to a future pipeline run as input artifacts.
4. **Documentation parity** across SKILL.md, references, CLAUDE.md, README.md, and marketplace.json so that the new type is discoverable and consistently described everywhere it appears.
5. **Configurable override** via `routing.force_type: DESIGN` in `.delivery/config.yml`, validated by the config schema.
6. **No regressions** to the six existing project types or their routing.

## Constraints

- **Light != skip:** This brief uses *skip* deliberately for Plan/Dev/UAT because DESIGN is definitionally a design-only mode. This is not "light Plan" — it is "no Plan." That distinction must be clear in pipeline-stages.md so it does not bleed into other types where light stages MUST execute.
- **Markdown-only edits calibrate one tier lower:** All file changes are documentation/configuration. No code, no scripts, no schema generators. Effort must be sized accordingly.
- **All work routes through the pipeline:** This feature itself must be delivered via delivery-flow, dogfooding the very mechanism it extends.
- **Documentation parity is non-negotiable:** CLAUDE.md, README.md, and marketplace.json must reflect the change in the same PR.
- **Schema versioning:** `config-schema.md` is the source of truth (currently v2.6). Adding DESIGN as a valid `routing.force_type` value follows the documented extension protocol.
- **Wizard:** PR #74 removed Q1, so no wizard *question* needs to be added. Detection guidance in setup-wizard.md must still be updated so the wizard's auto-detection knows the signals for DESIGN.
- **Backward compatibility:** Existing configs without DESIGN must continue to work unchanged.
- **Retrospective hook compatibility:** The Stop hook that enforces retrospectives must still fire correctly when a DESIGN run completes after Architect.

## Initial Scope

The following files are in scope for this feature:

| File | Change |
|---|---|
| `delivery-team/skills/delivery-flow/SKILL.md` | Add DESIGN to routing matrix and project-type detection table |
| `delivery-team/skills/delivery-flow/references/project-types.md` | Add DESIGN section with detection signals, examples, and rationale |
| `delivery-team/skills/delivery-flow/references/pipeline-stages.md` | Document DESIGN-specific routing (full Idea/Refine/Design/Architect; skip Plan/Dev/UAT) and clarify that *skip* here is intentional |
| `delivery-team/skills/delivery-flow/references/setup-wizard.md` | Add DESIGN detection guidance for the wizard's auto-detect logic |
| `delivery-team/skills/delivery-flow/references/config-schema.md` | Add DESIGN as a valid `routing.force_type` enum value; bump schema version per extension protocol |
| `CLAUDE.md` | Update the project-type list in the delivery-flow architecture section |
| `README.md` | Update any project-type enumeration so DESIGN appears alongside the others |
| `.claude-plugin/marketplace.json` | Update delivery-flow description if it enumerates project types |

**Routing matrix for DESIGN (the canonical table this feature ships):**

| Stage | Depth |
|---|---|
| 1. Idea | full |
| 2. Refine | full |
| 3. Design | full |
| 4. Architect | full |
| 5. Plan | skip |
| 6. Dev | skip |
| 7. UAT | skip |

**Detection signals (initial draft, to be refined in Stage 2):**

- User language: "design only," "no implementation," "design package," "architecture spike that produces docs," "pre-funding design," "reference architecture," "design the system but don't build it yet."
- Absence of an executable target, repo, or sprint commitment.
- Explicit handoff intent: "to be implemented later by team X."
- Deliverable framed as PRD + ADRs + architecture diagrams rather than working software.

## Out of Scope

- **New scripts, hooks, or schema-generation code.** This is a documentation and configuration change.
- **A new wizard question.** PR #74 removed Q1; we update detection guidance only, not interactive prompts.
- **Changes to other project types' routing.** GREENFIELD, FEATURE, BUG_FIX, GAME_DEV, SPIKE, and DOCS_ONLY are untouched.
- **A "DESIGN-light" variant.** One depth profile for DESIGN; future variants can be proposed separately.
- **Automatic handoff into a follow-on implementation run.** The output is *ready* to feed a future run; wiring that handoff is a separate feature.
- **Retroactive migration of existing in-flight pipelines** to DESIGN.
- **Changes to the retrospective hook's behavior** beyond verifying it still fires correctly after Architect when later stages are skipped.
- **Net-new artifacts or templates** for the design package — DESIGN reuses existing PRD, design, architecture, and ADR artifact formats produced by stages 1–4.

---

*Speak, friends, and proceed. The road to Refine is open.*
— Gandalf, Product Owner
