# Stories: DESIGN Project Type for delivery-flow

*"Each story is a stone on the path. Lay them well, and the road holds."* — Gandalf

**Stage:** 05 — Plan (PO sub-flow)
**Feature:** DESIGN Project Type
**PRD:** `.delivery/artifacts/02-refine/po/prd.md`
**Author:** Product Owner (Gandalf)
**Date:** 2026-04-05

**Sizing note:** All stories are markdown/configuration edits. Points are calibrated one tier lower than equivalent code work — a 1-pointer here is a single-file paragraph edit; a 2-pointer touches multiple sections or requires schema-version discipline.

---

## DS-01 — Add DESIGN to `routing.force_type` enum in config-schema.md

**Points:** 2
**Files:** `delivery-team/skills/delivery-flow/references/config-schema.md`
**Maps to:** FR-01, FR-05, NFR-03

**As a** delivery-flow user
**I want** `routing.force_type: DESIGN` to be a valid configuration value
**So that** I can explicitly force DESIGN routing in `.delivery/config.yml`.

**Acceptance Criteria:**

- **Given** the current `config-schema.md` at v2.7
  **When** I add `DESIGN` to the `routing.force_type` enum
  **Then** the enum reads: `[GREENFIELD, FEATURE, BUG_FIX, GAME_DEV, SPIKE, DOCS_ONLY, DESIGN]`.
- **Given** the schema version is being changed
  **When** the edit is committed
  **Then** the version is bumped per the extension protocol and a changelog entry referencing this feature is added.
- **Given** an existing config that does not set `force_type`
  **When** validated against the new schema
  **Then** it MUST validate unchanged (backward compatibility).

**Test Cases:**

1. Grep `config-schema.md` for `DESIGN` — appears in the `routing.force_type` enum row.
2. Grep for the new schema version string — appears in the version header and changelog.
3. Sample config with `routing.force_type: DESIGN` validates clean.
4. Sample config with no `force_type` key validates clean (regression).

---

## DS-02 — Add DESIGN to SKILL.md Phase 1 detection table + routing matrix

**Points:** 2
**Files:** `delivery-team/skills/delivery-flow/SKILL.md`
**Maps to:** FR-01, FR-03, FR-04

**As a** delivery-flow orchestrator
**I want** the Phase 1 project-type detection table and stage routing matrix to know about DESIGN
**So that** auto-detection routes design-only requests correctly.

**Acceptance Criteria:**

- **Given** the Phase 1 detection table in SKILL.md
  **When** I view the table
  **Then** a DESIGN row exists with detection signals and a routing summary, in the same format as the other six types.
- **Given** the stage routing matrix in SKILL.md
  **When** I view the matrix
  **Then** DESIGN is encoded as: Idea=full, Refine=full, Design=full, Architect=full, Plan=skip, Dev=skip, UAT=skip.
- **Given** the six existing rows
  **When** the diff is inspected
  **Then** none of them are modified (regression check).

**Test Cases:**

1. Grep SKILL.md for `DESIGN` — appears in detection table and routing matrix.
2. Diff against `main` shows only additions for DESIGN; existing rows unchanged.
3. Manual read confirms routing summary text matches "stages 1–4 full, 5–7 skip."

---

## DS-03 — Add DESIGN detection signals to project-types.md

**Points:** 2
**Files:** `delivery-team/skills/delivery-flow/references/project-types.md`
**Maps to:** FR-01, FR-02

**As a** Product Owner triaging an incoming request
**I want** project-types.md to document DESIGN's detection signals, examples, and rationale
**So that** I (and the orchestrator) can recognize design-only engagements consistently.

**Acceptance Criteria:**

- **Given** project-types.md
  **When** I view it
  **Then** a DESIGN section exists with: detection signals, example user phrases, rationale, and routing summary.
- **Given** the listed signals
  **When** I read them
  **Then** they include: "design only," "no implementation," "design package," "reference architecture," "pre-funding design," explicit downstream-handoff intent, absence of executable target, deliverable framed as PRD + ADRs + diagrams.
- **Given** the existing six type sections
  **When** the diff is inspected
  **Then** they are untouched.

**Test Cases:**

1. Grep `project-types.md` for `## DESIGN` — section exists.
2. Grep for at least 5 of the listed signal phrases.
3. Diff confirms existing six type sections unchanged.

---

## DS-04 — Update pipeline-stages.md with DESIGN-specific routing notes

**Points:** 2
**Files:** `delivery-team/skills/delivery-flow/references/pipeline-stages.md`
**Maps to:** FR-03, NFR-04

**As a** delivery-team member reading the stage reference
**I want** pipeline-stages.md to call out DESIGN's stage-5/6/7 skip behavior explicitly
**So that** "skip" is not confused with "light" elsewhere in the pipeline.

**Acceptance Criteria:**

- **Given** pipeline-stages.md
  **When** I read stages 5, 6, and 7
  **Then** each notes that DESIGN runs SKIP these stages, and that this is intentional/definitional, NOT a "light" variant.
- **Given** the cardinal rule that "light != skip"
  **When** I read the DESIGN note
  **Then** it explicitly affirms the rule and clarifies DESIGN as the sole exception by definition (no Plan/Dev/UAT to be light about).
- **Given** stages 1–4
  **When** I read them
  **Then** DESIGN is noted as running them at full depth.

**Test Cases:**

1. Grep `pipeline-stages.md` for `DESIGN` — appears in stage 5, 6, 7 sections.
2. Grep for "light" near DESIGN — confirms the distinction is called out.
3. Manual read confirms stages 1–4 mention DESIGN as full-depth.

---

## DS-05 — Update setup-wizard.md detection guidance for DESIGN

**Points:** 1
**Files:** `delivery-team/skills/delivery-flow/references/setup-wizard.md`
**Maps to:** FR-07

**As a** delivery-flow setup wizard
**I want** my detection guidance to recognize DESIGN signals
**So that** auto-detection routes design-only setups correctly without a new question.

**Acceptance Criteria:**

- **Given** setup-wizard.md
  **When** I view the detection guidance section
  **Then** DESIGN appears alongside the other types with its detection signals.
- **Given** PR #74 removed Q1
  **When** the diff is inspected
  **Then** no new interactive wizard question is added — only detection guidance text.

**Test Cases:**

1. Grep `setup-wizard.md` for `DESIGN` — appears in the detection guidance section.
2. Diff confirms no new "Q" or numbered question block was added.

---

## DS-06 — Update CLAUDE.md, README.md, marketplace.json with DESIGN

**Points:** 2
**Files:** `CLAUDE.md`, `README.md`, `.claude-plugin/marketplace.json`
**Maps to:** FR-06, NFR-02

**As a** developer or user discovering delivery-flow
**I want** every discovery surface to list DESIGN
**So that** the project type is visible everywhere it's enumerated.

**Acceptance Criteria:**

- **Given** `CLAUDE.md`'s delivery-flow architecture section
  **When** I view the project-type list
  **Then** DESIGN is listed alongside the existing six.
- **Given** the root `README.md`
  **When** I view any project-type enumeration
  **Then** DESIGN is listed.
- **Given** `.claude-plugin/marketplace.json`
  **When** the delivery-flow plugin description enumerates project types
  **Then** DESIGN is included; if no enumeration exists, the file is left unchanged and a note is added to the PR description.

**Test Cases:**

1. Grep `CLAUDE.md` for `DESIGN` in the project-type list.
2. Grep `README.md` for `DESIGN`.
3. Inspect `marketplace.json` — DESIGN added or non-applicability documented.
4. Diff inspection confirms no other project-type rows are altered.

---

## DS-07 — Update delivery-team/README.md project type list

**Points:** 1
**Files:** `delivery-team/README.md`
**Maps to:** FR-08, NFR-02

**As a** plugin maintainer browsing delivery-team
**I want** delivery-team/README.md to list DESIGN
**So that** plugin-level documentation is consistent with the references and root docs.

**Acceptance Criteria:**

- **Given** `delivery-team/README.md`
  **When** I view any project-type enumeration
  **Then** DESIGN is listed alongside the existing six types.
- **Given** the existing project-type entries
  **When** the diff is inspected
  **Then** they are untouched.

**Test Cases:**

1. Grep `delivery-team/README.md` for `DESIGN`.
2. Diff confirms no other type rows altered.

---

## Story Map Summary

| Story | Points | File(s) | FRs |
|---|---|---|---|
| DS-01 | 2 | config-schema.md | FR-01, FR-05, NFR-03 |
| DS-02 | 2 | SKILL.md | FR-01, FR-03, FR-04 |
| DS-03 | 2 | project-types.md | FR-01, FR-02 |
| DS-04 | 2 | pipeline-stages.md | FR-03, NFR-04 |
| DS-05 | 1 | setup-wizard.md | FR-07 |
| DS-06 | 2 | CLAUDE.md, README.md, marketplace.json | FR-06, NFR-02 |
| DS-07 | 1 | delivery-team/README.md | FR-08, NFR-02 |
| **Total** | **12** | | |

**Suggested execution order:** DS-01 → DS-03 → DS-02 → DS-04 → DS-05 → DS-06 → DS-07. (Schema first, then references the schema points to, then the orchestrator entry table, then surfacing.)

---

*"Twelve points, seven stories, one road. Walk it well."*
— Gandalf, Product Owner
