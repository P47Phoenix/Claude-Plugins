# Cross-Skill Artifact Contracts

## Purpose

Artifact contracts define the exact structure each skill outputs and the next skill expects as input. They ensure that stage transitions are smooth: the upstream stage produces everything the downstream stage needs, and the downstream stage can validate its inputs before starting work.

---

## Contract Versioning

Contracts evolve with the pipeline. The contract version matches the config schema version in `references/config-schema.md`. When the config schema version increments, review contracts for any structural changes.

Current contract version: matches `config_version` in `.delivery/config.md`.

---

## Contracts by Stage Transition

### Stage 1 to Stage 2 (Idea to Refine)

**Artifact**: `.delivery/artifacts/01-idea/idea-brief.md`

**Output sections**:

| Section | Required for Next Stage | Description |
|---------|:-----------------------:|-------------|
| Problem Statement | YES | Clear description of the problem being solved |
| Target Users | YES (at least 1) | Who will use or benefit from this solution |
| Goals | YES (at least 1) | Measurable outcomes the project should achieve |
| Constraints | No | Known limitations (budget, timeline, technology, regulatory) |
| Initial Scope | No | High-level boundaries of what is and is not included |

**Validation at Stage 2 entry**: Problem Statement must exist and be non-empty. At least one Target User and one Goal must be listed.

---

### Stage 2 to Stage 3 (Refine to Design)

**Artifact**: `.delivery/artifacts/02-refine/prd.md`

**Output sections**:

| Section | Required for Next Stage | Description |
|---------|:-----------------------:|-------------|
| Problem | No | Refined problem statement (expanded from idea brief) |
| Goals | No | Measurable goals with success criteria |
| Personas | YES | User personas with demographics, needs, pain points |
| Stories | YES (with ACs) | User stories in standard format with acceptance criteria |
| NFRs | No | Non-functional requirements (performance, security, etc.) |
| Out of Scope | No | Explicitly excluded items |

**Validation at Stage 3 entry**: At least one Persona must exist. At least one Story with acceptance criteria must exist.

---

### Stage 2 to Stage 4 (Refine to Architect)

**Artifact**: `.delivery/artifacts/02-refine/prd.md` (same artifact as above)

**Required sections for Architect stage**:

| Section | Required for Next Stage | Description |
|---------|:-----------------------:|-------------|
| NFRs | YES | Non-functional requirements drive architecture quality attributes |
| Stories | YES | Functional scope informs component design |
| Constraints | YES | Technical and business constraints bound the solution space |
| Personas | No | Helpful for understanding scale and usage patterns |
| Goals | No | Helpful for prioritizing architectural trade-offs |

**Validation at Stage 4 entry (from Refine)**: NFRs section must exist with at least one requirement. Stories section must exist. Constraints section must exist (may be empty with explicit "none identified" statement).

---

### Stage 3 to Stage 4 (Design to Architect)

**Artifact**: `.delivery/artifacts/03-design/ux-design.md`

**Output sections**:

| Section | Required for Next Stage | Description |
|---------|:-----------------------:|-------------|
| User Flows | YES | Step-by-step flows for key user journeys |
| Wireframes | No | Low/mid-fidelity wireframe descriptions or references |
| Component Specs | No | UI component specifications (inputs, states, behaviors) |

**Validation at Stage 4 entry (from Design)**: User Flows section must exist with at least one complete flow.

---

### Stage 4 to Stage 5 (Architect to Plan)

**Artifact**: `.delivery/artifacts/04-architect/architecture.md`

**Output sections**:

| Section | Required for Next Stage | Description |
|---------|:-----------------------:|-------------|
| System Design | YES | Component breakdown, responsibilities, interactions |
| C4 Diagrams | No | Context, container, and/or component diagram descriptions |
| ADRs | YES | Architecture decisions with context, rationale, consequences |
| Trade-offs | No | Alternatives considered with pros/cons analysis |
| Quality Attributes | No | How NFRs are addressed architecturally |
| Risks | No | Architecture-level risks and mitigations |

**Validation at Stage 5 entry**: System Design section must exist with at least one component defined. ADRs section must exist with at least one decision recorded.

---

### Stage 5 to Stage 6 (Plan to Development)

**Artifact**: `.delivery/artifacts/05-plan/sprint-plan.md`

**Output sections**:

| Section | Required for Next Stage | Description |
|---------|:-----------------------:|-------------|
| Sprint Goal | No | Clear statement of what this sprint delivers |
| Stories | YES (with ACs + test cases) | Stories broken into implementable units with acceptance criteria and test cases |
| Capacity | No | Team capacity and story point allocation |
| Dependencies | No | External dependencies and their status |
| Technical Tasks | No | Non-story work (setup, infrastructure, spikes) |

**Validation at Stage 6 entry**: At least one Story must exist with both acceptance criteria and test cases defined.

---

### Stage 6 to Stage 7 (Development to UAT)

**Artifacts**:
- `.delivery/artifacts/06-dev/dev-notes.md`
- Code files (location varies by project)

**Output sections in dev-notes.md**:

| Section | Required for Next Stage | Description |
|---------|:-----------------------:|-------------|
| CODE_COMPLETE Items | YES | List of all items marked CODE_COMPLETE with file references |
| Implementation Notes | No | Design decisions made during development, deviations from plan |
| Known Issues | No | Issues discovered but not resolved, with severity |
| Test Results | No | Summary of tests run and their outcomes |
| Environment Setup | No | Any setup needed for UAT (environment variables, data, etc.) |

**Validation at Stage 7 entry**: dev-notes.md must exist. CODE_COMPLETE Items section must list at least one item.

---

## Validation Protocol

At each stage start, before invoking the worker skill:

1. **Check upstream artifacts exist** on disk at the expected paths.
2. **Parse required sections**: scan the artifact for the section headings listed as "Required for Next Stage".
3. **Validate non-empty**: required sections must contain substantive content (not just a heading with no body).
4. **Report result**:

### If all required sections present:
```
> Artifact validation passed: [artifact path]
> Required sections found: [list]
```
Proceed with stage execution.

### If any required sections missing:
```
> WARNING: Artifact validation failed for [artifact path]
> Missing required sections: [list]
>
> Options:
> 1. Re-run Stage [N] to produce the missing sections
> 2. Proceed anyway (risk: downstream quality may suffer)
> 3. Manually add the missing sections
```

The user chooses how to proceed. If they choose option 2, log the bypass in the pipeline state and memory for post-run analysis.

---

## Contract Summary Matrix

| Transition | Artifact | Required Sections |
|------------|----------|-------------------|
| 1 to 2 | idea-brief.md | Problem Statement, Target Users (1+), Goals (1+) |
| 2 to 3 | prd.md | Personas (1+), Stories with ACs (1+) |
| 2 to 4 | prd.md | NFRs (1+), Stories, Constraints |
| 3 to 4 | ux-design.md | User Flows (1+) |
| 4 to 5 | architecture.md | System Design (1+ component), ADRs (1+) |
| 5 to 6 | sprint-plan.md | Stories with ACs + test cases (1+) |
| 6 to 7 | dev-notes.md + code | CODE_COMPLETE Items (1+) |
