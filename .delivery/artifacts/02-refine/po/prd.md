# PRD: DESIGN Project Type for delivery-flow

*"Even the smallest road, well-marked, leads the fellowship safely home."* — Gandalf

**Type:** FEATURE (markdown-only)
**Source:** Idea Brief — GitHub Issue #72
**Author:** Product Owner (Gandalf)
**Date:** 2026-04-05
**Depends on:** config-schema v2.7 (shipped in PR #74)

---

## 1. Problem Statement

The delivery-flow pipeline supports six project types — GREENFIELD, FEATURE, BUG_FIX, GAME_DEV, SPIKE, DOCS_ONLY — and every one of them marches through to implementation. There is no first-class path for a *design-only* engagement: a run that gathers requirements, designs the system, and architects the solution, then stops before Plan/Development/UAT.

Today, teams who want pure design work must run a full pipeline and abandon it (leaving state mid-stride and angering the retrospective hook), choose DOCS_ONLY (which skips the very design and architecture they need), or escape the pipeline entirely (violating the cardinal rule that all work routes through delivery-flow). None of these are honest paths.

## 2. Goals

1. Add **DESIGN** as a first-class project type in delivery-flow.
2. **Detect** DESIGN from explicit user signals (design-only language, handoff intent, no executable target).
3. **Route** DESIGN to run stages 1–4 at full depth and *skip* stages 5/6/7 entirely.
4. Achieve **documentation parity** across SKILL.md, references, CLAUDE.md, README.md, and marketplace.json.
5. Permit explicit override via `routing.force_type: DESIGN` in `.delivery/config.yml`.
6. Preserve **backward compatibility** — the six existing project types and their routing are untouched.

## 3. Non-Goals (Out of Scope)

- Design package handoff into a follow-on implementation run.
- New collaboration patterns, hooks, scripts, or schema-generation code.
- A "DESIGN-light" depth variant.
- A new wizard *question* (PR #74 removed Q1 — only detection guidance is updated).
- Changes to the retrospective hook beyond verifying it still fires after Architect.
- Net-new artifact templates — DESIGN reuses existing PRD/design/architecture/ADR formats.

## 4. Functional Requirements

**FR-01 — DESIGN added to project type enum.**
The canonical project type list (SKILL.md, project-types.md, config-schema.md) MUST include `DESIGN` alongside the existing six values.

**FR-02 — Detection signals defined in project-types.md.**
`project-types.md` MUST contain a DESIGN section with detection signals: phrases like "design only," "no implementation," "design package," "reference architecture," "pre-funding design," "design the system but don't build it yet"; explicit downstream-handoff intent; absence of executable target/repo/sprint commitment; deliverable framed as PRD + ADRs + architecture diagrams.

**FR-03 — Stage routing matrix updated.**
The routing matrix in SKILL.md and pipeline-stages.md MUST encode DESIGN as: Stage 1 Idea = full, Stage 2 Refine = full, Stage 3 Design = full, Stage 4 Architect = full, Stage 5 Plan = **skip**, Stage 6 Development = **skip**, Stage 7 UAT = **skip**. pipeline-stages.md MUST explicitly note that *skip* here is intentional and definitional, NOT a "light" variant — preserving the cardinal rule that light stages MUST execute elsewhere.

**FR-04 — SKILL.md Phase 1 detection table updated.**
The Phase 1 project-type detection table in `delivery-flow/SKILL.md` MUST list DESIGN with its signals and the resulting routing summary, in the same row format as the other six types.

**FR-05 — config-schema.md routing.force_type enum includes DESIGN.**
`config-schema.md` MUST add `DESIGN` to the `routing.force_type` enum, bump the schema version per the documented extension protocol, and add a changelog entry referencing this feature. Existing configs without `force_type: DESIGN` MUST validate unchanged.

**FR-06 — DESIGN referenced in CLAUDE.md, README.md, marketplace.json.**
All three discovery surfaces MUST enumerate DESIGN wherever they list project types: `CLAUDE.md` (delivery-flow architecture section), `README.md` (project-type list), and `.claude-plugin/marketplace.json` (delivery-flow plugin description, if it enumerates types).

**FR-07 — Setup wizard detection guidance mentions DESIGN.**
`setup-wizard.md` MUST update its detection guidance so the wizard's auto-detect logic recognizes DESIGN signals. No new interactive question is added.

**FR-08 — delivery-team/README.md project type list updated.**
`delivery-team/README.md` MUST list DESIGN alongside the other project types in any enumeration of supported types.

## 5. Non-Functional Requirements

- **NFR-01 — Backward compatibility.** Existing configs, in-flight pipelines, and the six existing project types' routing MUST remain unchanged. No migration required.
- **NFR-02 — Documentation parity.** Every surface that lists project types MUST list DESIGN in the same PR. No surface may lag.
- **NFR-03 — Schema versioning discipline.** The schema version bump in `config-schema.md` MUST follow the documented extension protocol (version + changelog).
- **NFR-04 — Retrospective hook compatibility.** The Stop hook MUST still fire correctly when a DESIGN run completes after Architect with stages 5/6/7 skipped. (Verification only — no hook code changes.)
- **NFR-05 — Markdown-only effort calibration.** All edits are documentation/configuration; story points are sized one tier lower than equivalent code changes.

## 6. Dependencies

- **config-schema v2.7** (shipped in PR #74) — provides the schema version baseline that this feature bumps from.
- **PR #74** (wizard Q1 removal) — confirms no new wizard question is required; only detection guidance.

## 7. Acceptance Criteria (Feature-Level)

- All eight functional requirements met and visible in the diff.
- Schema version incremented and changelog entry present in `config-schema.md`.
- `routing.force_type: DESIGN` validates against the schema.
- Existing project types' routing untouched (diff inspection).
- Retrospective hook fires correctly on a dogfood DESIGN run after Architect.

---

*"The road goes ever on. Now there is a path for those who would map it before they walk it."*
— Gandalf, Product Owner
