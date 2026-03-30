# Design Specification: Stage Health Hardening

**Version**: 1.0
**Date**: 2026-03-29
**Author**: UX Designer (Galadriel)
**Source PRD**: `.delivery/artifacts/02-refine/po/prd.md` v1.1
**Project Type**: FEATURE

---

## Open Question Resolutions

### OQ-1: Definition of "phantom" vs "planned" files (RESOLVED in PRD v1.1)

Already resolved. Design adopts the PRD's two-tier model:
- **Phantom**: A file path cited in a stage artifact that does not exist on disk AND is not annotated with `[PLANNED]`.
- **Planned**: A file path annotated with `[PLANNED]` in a Design artifact, indicating intentional future creation.
- At Design DoD (FR-05): phantoms generate WARNING; `[PLANNED]` paths are exempt.
- At Dev entry (FR-06): `[PLANNED]` is no longer an exemption -- files must exist on disk or appear in the sprint plan's task list.

### OQ-2: Definition of "shared module" for UAT review (RESOLVED in PRD v1.1)

Already resolved. Design adopts the PRD's artifact-traceable definition:
- **Shared module**: A file that is explicitly referenced (by path or name) in 2+ stage artifacts across the current pipeline run.
- Identification method: QA agent uses Glob/Read on `.delivery/artifacts/` directory to find file references, then identifies any file referenced in artifacts from 2+ different stages.
- This avoids language-level import analysis and is tool-agnostic.

### OQ-3: Format of empirical-items tracking artifact (DESIGN DECISION)

**Decision**: The empirical-items tracking artifact shall be a **dedicated section within the existing UAT test-plan artifact** (`.delivery/artifacts/07-uat/qa/test-plan.md`), not a standalone file.

**Rationale**:
1. The empirical-items classification is inherently part of the UAT test plan -- it determines which ACs need runtime validation vs. structural review.
2. A standalone file creates an additional artifact for validators to locate and cross-reference, increasing overhead without proportionate benefit.
3. The existing UAT test-plan template in `artifact-contracts.md` already has a natural insertion point after "Test Cases".
4. The validator in `quality-gates.md` can check for the section within the test-plan artifact rather than checking for a separate file.

**Template format**: See FR-03 specification below.

---

## Milestone M1: UAT Stage Hardening

### FR-01: Shared-module review checkpoint in pipeline-stages.md

**Target file**: `delivery-team/skills/delivery-flow/references/pipeline-stages.md` (verified on disk)

**Location**: Stage 7: UAT > Sub-Flow section, insert as new step between current step 4 (Exploratory testing sessions) and current step 5 (Invoke Supporting Agents). The new step becomes step 5, and all subsequent steps increment by 1.

**Change type**: ADD

**Exact content to add**:

```markdown
5. **Shared-module review** [SEQUENTIAL after step 4] [required] (quality skill, task_type: test-plan)
   - **Definition**: A shared module is a file referenced by path or name in 2+ stage artifacts across the current pipeline run.
   - **Identification**: QA agent scans `.delivery/artifacts/` using Glob/Read to collect all file path references across all stage artifacts. Any file path appearing in artifacts from 2+ different stages is flagged as a shared module.
   - **Review**: For each shared module modified during Development, the QA agent must:
     1. List all consuming contexts (stages/artifacts that reference the module)
     2. Verify test coverage exists for each consuming context
     3. Document the shared-module review results in the UAT test plan
   - Output: Shared-module review section within `.delivery/artifacts/07-uat/qa/test-plan.md`
   - **Light Mode**: Applies to all project types including BUG_FIX and DOCS_ONLY <!-- retro c8f2 -->
```

Also add to the Stage 7 DoD Validators section, append to the QA Engineer validator description:

```markdown
- QA Engineer [required]: all tests pass, no critical defects, shared-module review complete (if shared modules were modified)
```

**Integration notes**: This step runs after exploratory testing but before the review board, ensuring shared-module findings are available for the multi-perspective review. The QA agent already has Glob/Read tool access (Assumption #1 from PRD). The step uses the existing quality skill invocation pattern. Subsequent steps in Stage 7 Sub-Flow must be renumbered (current 5 becomes 6, 6 becomes 7, etc., through current 10 becoming 11).

---

### FR-02: Shared-module review guidance in quality/SKILL.md

**Target file**: `delivery-team/skills/quality/SKILL.md` (verified on disk)

**Location**: Insert a new section after the "Empirical Validation and CODE_COMPLETE Status" section (after line 311 of current file) and before the "Sub-Agent Interface" section.

**Change type**: ADD

**Exact content to add**:

```markdown
## Shared-Module Review Protocol

When performing UAT validation on pipeline runs where Development modified shared modules, the QA Engineer must perform a shared-module review. This protocol applies to all project types including Light Mode (BUG_FIX, DOCS_ONLY).

### Definition

A **shared module** is a file that is explicitly referenced (by path or name) in 2+ stage artifacts across the current pipeline run. This is an artifact-traceable definition -- it does not require language-level import analysis.

### Identification Steps

1. **Scan artifacts**: Use Glob to list all files in `.delivery/artifacts/` across all stages (01 through 07).
2. **Extract file references**: Read each artifact and collect all file paths mentioned (absolute or relative paths, including paths in code blocks, lists, and tables).
3. **Cross-reference**: For each referenced file, count how many distinct stage directories (01-idea, 02-refine, etc.) contain artifacts that reference it.
4. **Flag shared modules**: Any file referenced in artifacts from 2+ different stages is a shared module.
5. **Filter to modified**: From the flagged shared modules, identify which ones were modified during the Development stage (check git diff or dev-notes artifacts).

### Review Checklist

For each modified shared module:

- [ ] **Consuming contexts listed**: All stages/artifacts that reference this module are identified
- [ ] **Test coverage verified**: Each consuming context has test coverage that exercises the modified module's behavior
- [ ] **Integration impact assessed**: Changes to the shared module do not break assumptions made by consuming contexts
- [ ] **Cross-context regression tested**: If exploratory testing sessions were run, shared-module interactions were included in the cross-story interaction charter

### Output Format

Document the shared-module review as a section in the UAT test plan:

```
### Shared-Module Review <!-- retro c8f2 -->

**Shared modules identified**: [count]

| Module Path | Stages Referencing | Modified in Dev | Test Coverage | Status |
|---|---|---|---|---|
| [path] | [stage list] | Yes/No | [coverage description] | PASS/FAIL/N/A |

**Findings**: [any gaps or risks identified]
```

If no shared modules were modified during Development, document: "No shared modules modified -- review not applicable."
```

**Integration notes**: This section is additive only -- no existing QA skill content is removed or modified. The QA sub-agent will have this guidance in context when invoked for UAT validation. The protocol relies only on Glob/Read tools already available to the QA agent.

---

### FR-03: Empirical-items tracking template in artifact-contracts.md

**Target file**: `delivery-team/skills/delivery-flow/references/artifact-contracts.md` (verified on disk)

**Location**: In the "Stage 6 to Stage 7 (Development to UAT)" contract section, add a new row to the output sections table. Then add a new subsection after the "Contract Summary Matrix" section (end of file) defining the empirical-items tracking template.

**Change type**: ADD (two additions)

**Addition 1** -- Add row to the Stage 6 to Stage 7 output sections table (after the "CODE_COMPLETE Items" row):

```markdown
| Empirical Items Classification | YES | Classification of each AC as structural or empirical with justification |
```

**Addition 2** -- Add new section after the "Contract Summary Matrix" section:

```markdown
---

## Empirical-Items Tracking Template <!-- retros c8f2, k4m9 -->

The empirical-items tracking is a mandatory section within the UAT test plan (`.delivery/artifacts/07-uat/qa/test-plan.md`). The QA agent populates this section during UAT execution, classifying each acceptance criterion from the PRD as either structural (verifiable by inspection/static analysis) or empirical (requires runtime validation).

### Template

```
### Empirical-Items Classification <!-- retro k4m9 -->

| FR/AC ID | Acceptance Criterion (summary) | Classification | Justification | Validation Method |
|---|---|---|---|---|
| FR-01/AC-1 | [brief summary] | structural / empirical | [why this classification] | [how to validate: inspection, test, runtime] |

**Summary**:
- Total ACs: [count]
- Structural: [count] ([percentage]%)
- Empirical: [count] ([percentage]%)

**Empirical items requiring runtime validation**:
1. [AC ID]: [description] -- [recommended validation approach]
```

### Classification Rules

- **Structural**: Can be verified by reading code, inspecting artifacts, checking file existence, or static analysis. Examples: "section X exists in file Y", "table has columns A, B, C", "no hardcoded secrets".
- **Empirical**: Requires running the application, executing a pipeline, observing runtime behavior, or measuring performance. Examples: "API responds in < 200ms", "UI renders correctly on mobile", "pipeline completes without error".

### Integration with Pipeline

- The QA agent produces this classification during UAT Step 1 (test plan creation).
- Empirical items from Stage 6 CODE_COMPLETE carry forward as mandatory entries.
- The UAT DoD validator checks for the presence and completeness of this section (see quality-gates.md Gate 7).
- **Light Mode**: Applies to all project types including BUG_FIX and DOCS_ONLY.
```

**Integration notes**: The template follows the existing artifact-contracts.md conventions (table-based format, clear Required/No markers, validation instructions). The section-within-test-plan approach (per OQ-3 resolution) means no new artifact file path is introduced, keeping the artifact namespace clean. The Stage 6->7 contract update ensures validators know to expect this section.

---

### FR-04: Empirical-items tracking in UAT DoD validator criteria (quality-gates.md)

**Target file**: `delivery-team/skills/delivery-flow/references/quality-gates.md` (verified on disk)

**Location**: Gate 7: UAT Acceptance checklist, insert after the existing item "All pending empirical validations from Stage 6 included as mandatory UAT test cases [blocking]" (line 207 of current file).

**Change type**: ADD

**Exact content to add** (new checklist item):

```markdown
- [ ] Empirical-items classification section present in UAT test plan: every PRD acceptance criterion classified as "structural" or "empirical" with justification, and empirical items have documented validation method [blocking] <!-- retro k4m9 -->
```

**Integration notes**: This is additive to the existing Gate 7 checklist. The validator checks for the section within the UAT test plan artifact (not a separate file). The blocking severity ensures the submission is rejected if the classification is missing, consistent with the PRD's P0 priority. This criterion works in conjunction with the existing "All pending empirical validations from Stage 6 included as mandatory UAT test cases" criterion -- FR-04 ensures the classification exists, the existing criterion ensures the empirical items are actually tested.

---

## Milestone M2: Design Stage Hardening

### FR-05: Phantom reference WARNING at Design DoD in quality-gates.md

**Target file**: `delivery-team/skills/delivery-flow/references/quality-gates.md` (verified on disk)

**Location**: Gate 3: Design Completeness checklist, insert after the existing item "Design aligns with PRD requirements (every user story has a corresponding design element) [blocking]" (line 153 of current file).

**Change type**: ADD

**Exact content to add** (new checklist item):

```markdown
- [ ] File path references in Design artifacts verified: any file path cited in Design artifacts that does not exist on disk and is not annotated with `[PLANNED]` generates a WARNING finding. The WARNING is logged, surfaced to the author, and carried forward to downstream stages, but does NOT block stage completion. File paths annotated with `[PLANNED]` are exempt from phantom detection at this stage. [warning] <!-- retro k4m9 -->
```

**Integration notes**: The WARNING severity is intentional -- the PRD explicitly chose warning over blocking at Design to avoid false positives on GREENFIELD and FEATURE projects where Design routinely references files to be created later. The two-tier model (warn here, block at Dev entry via FR-06) catches phantoms before Development begins. The `[PLANNED]` annotation convention gives Design authors an explicit mechanism to mark intentionally-future files. Validators performing this check should use Glob to test file existence.

---

### FR-06: Filename reconciliation gate at Dev stage entry in pipeline-stages.md

**Target file**: `delivery-team/skills/delivery-flow/references/pipeline-stages.md` (verified on disk)

**Location**: Stage 6: Development > Entry Conditions section (after line 302 of current file, which currently reads "- At minimum: user stories with acceptance criteria must exist").

**Change type**: ADD

**Exact content to add** (new entry condition):

```markdown
- **Filename reconciliation gate** <!-- retro k4m9 -->: Before Development begins, all file paths referenced in Design (Stage 3) and Architect (Stage 4) artifacts are checked:
  1. Use Glob/Read to extract all file paths from `.delivery/artifacts/03-design/` and `.delivery/artifacts/04-architect/` artifacts
  2. For each referenced file path, check existence on disk using Glob
  3. **Pass criteria**:
     - Path exists on disk: PASS
     - Path appears in the sprint plan's task list as a planned deliverable: PASS
     - Path is annotated `[PLANNED]` in Design artifacts but does NOT appear in the sprint plan: FAIL
     - Path does not exist and is not in the sprint plan: FAIL
  4. **Any FAIL blocks Dev entry** with a list of non-existent references and their source artifacts
  5. Resolution: either create the missing files, add them to the sprint plan as planned deliverables, or remove the references from upstream artifacts
  - **Light Mode**: Applies to all project types including BUG_FIX and DOCS_ONLY
  - **Note**: `[PLANNED]` annotations from Design (FR-05) are NOT accepted as exemptions at Dev entry. This is the enforcement point where all referenced files must be accounted for.
```

**Integration notes**: This gate runs before any Development sub-flow steps begin. It uses the same Glob/Read tools already available to the orchestrator. The gate checks both Design and Architect artifacts because phantom references can be introduced at either stage. The sprint plan cross-reference ensures files planned for creation in the current sprint are not falsely flagged. This is the "hard block" complement to FR-05's "soft warn" at Design.

---

## Milestone M3: Plan Stage Guardrails

### FR-07: Capacity matrix in Plan stage template (project-templates.md)

**Target file**: `delivery-team/skills/delivery-flow/references/project-templates.md` (verified on disk)

**Location**: This file contains project type templates, not stage templates. The Plan stage artifact is produced by the Scrum Bag (SM) sub-agent using the sprint-plan format. The capacity matrix template should be added as a new section at the end of the file, defining a "Sprint Plan Extensions" section that the SM agent must include.

**Change type**: ADD

**Exact content to add** (new section at end of file):

```markdown
---

## Sprint Plan Mandatory Sections <!-- retros c8f2, k4m9 -->

The following sections are mandatory in every sprint plan artifact (`.delivery/artifacts/05-plan/sm/sprint-plan.md`), regardless of project template. These extend the base sprint plan format.

### Capacity Matrix Template

Every sprint plan must include a capacity matrix. The SM agent populates this during Plan stage execution.

```
### Capacity Matrix <!-- retro c8f2 -->

| Team Member | Role | Available Hours | Allocated Hours | Utilization % |
|---|---|---|---|---|
| [name/role] | [role] | [hours] | [hours] | [calculated] |
| **Total** | -- | [sum] | [sum] | [total %] |

**Utilization notes**: [any adjustments for ceremonies, PTO, known interruptions]
```

**Light Mode (BUG_FIX, DOCS_ONLY)**: Capacity matrix is WAIVED. Minimal plans for single-story fixes do not benefit from full matrix overhead.

### Coverage Matrix Template

Every sprint plan must include a coverage matrix mapping PRD FRs to planned tasks. The SM agent populates this during Plan stage execution.

```
### Coverage Matrix <!-- retro c8f2 -->

| PRD FR-ID | FR Description (summary) | Planned Task(s) | Story ID(s) | Status |
|---|---|---|---|---|
| FR-01 | [brief summary] | [task description] | [US-xxx] | Mapped / Unmapped |

**Unmapped FRs**: [list any FRs not covered, with justification]
```

**Light Mode (BUG_FIX, DOCS_ONLY)**: Coverage matrix is WAIVED. Minimal plans for single-story fixes do not benefit from full matrix overhead.
```

**Integration notes**: The project-templates.md file defines templates for different tech stacks. The sprint plan extensions are template-agnostic -- they apply to ALL sprint plans regardless of project type. By placing them as a separate "Sprint Plan Mandatory Sections" section, they are clearly separated from the per-template content. The SM agent (product-delivery skill, sprint_planning task) will reference these templates when producing the sprint plan.

---

### FR-08: Coverage matrix in Plan stage template (project-templates.md)

**Target file**: `delivery-team/skills/delivery-flow/references/project-templates.md` (verified on disk)

**Location**: Same section as FR-07 (the Coverage Matrix Template is defined in the same "Sprint Plan Mandatory Sections" section).

**Change type**: ADD (combined with FR-07 above)

**Exact content**: Included in the FR-07 specification above (the "Coverage Matrix Template" subsection).

**Integration notes**: FR-07 and FR-08 are implemented as a single addition to project-templates.md because both matrices are mandatory sprint plan sections with the same Light Mode waiver behavior. Separating them into different file locations would create unnecessary fragmentation.

---

### FR-09: Capacity and coverage matrix validation in pipeline-stages.md

**Target file**: `delivery-team/skills/delivery-flow/references/pipeline-stages.md` (verified on disk)

**Location**: Stage 5: Plan > DoD Validators section. Modify the Scrum Bag validator description (line 273 of current file).

**Change type**: MODIFY

**Current text**:

```markdown
- Scrum Bag [required]: process is sound, capacity realistic
```

**New text**:

```markdown
- Scrum Bag [required]: process is sound, capacity realistic, capacity matrix present with utilization calculated, coverage matrix present with all PRD FRs mapped to at least one task <!-- retros c8f2, k4m9 -->
```

Also ADD to Stage 5: Plan > Sub-Flow, after step 3 (Invoke Supporting Agents) and before step 4 (Consensus Protocol). Insert as new step 4, renumbering subsequent steps:

```markdown
4. **Matrix validation** [SEQUENTIAL after step 3] [required]: Verify the sprint plan includes both mandatory matrices:
   - **Capacity matrix**: must be present with all team members listed, available hours > 0, utilization % calculated
   - **Coverage matrix**: must be present with every PRD FR-ID mapped to at least one planned task; any unmapped FR causes a BLOCKING finding
   - **Light Mode (BUG_FIX, DOCS_ONLY)**: Both matrices are WAIVED -- skip this step
   <!-- retros c8f2, k4m9 -->
```

**Integration notes**: The matrix validation runs after the SM produces the sprint plan (step 3) but before consensus (current step 4, becoming step 5). This ensures consensus participants see validated matrices. The Light Mode waiver is explicit and consistent with PRD Section 9. Subsequent steps in Stage 5 Sub-Flow must be renumbered (current 4 becomes 5, etc.).

---

### FR-10: Layered sprint capacity threshold validation

**Target file 1**: `delivery-team/skills/delivery-flow/references/quality-gates.md` (verified on disk)

**Location**: Gate 5: Plan Readiness checklist. MODIFY the existing item "Commitment does not exceed 80% of available capacity [blocking]" (line 180 of current file).

**Change type**: MODIFY

**Current text**:

```markdown
- [ ] Commitment does not exceed 80% of available capacity [blocking]
```

**New text**:

```markdown
- [ ] Sprint capacity threshold (two-tier model) <!-- retros c8f2, k4m9 -->:
  - **>80% and <=100% utilization**: WARNING -- emits a warning stating the utilization percentage. Plan can pass DoD only after the warning is acknowledged with brief justification recorded in the sprint plan.
  - **>100% utilization**: BLOCKING -- plan cannot pass DoD until allocation is reduced to <=100% OR the PO provides explicit sign-off with justification recorded in the sprint plan.
  - **Light Mode**: Applies to all project types -- even single-story plans can be overscoped.
```

**Target file 2**: `delivery-team/skills/delivery-flow/references/pipeline-stages.md` (verified on disk)

**Location**: Stage 5: Plan > DoD Validators section. Add capacity threshold awareness to the Scrum Bag validator (already modified in FR-09).

**Change type**: MODIFY (extend the FR-09 modification)

The FR-09 modified text for the Scrum Bag validator becomes:

```markdown
- Scrum Bag [required]: process is sound, capacity realistic, capacity matrix present with utilization calculated, coverage matrix present with all PRD FRs mapped to at least one task. Capacity threshold enforcement: >80% utilization emits WARNING requiring acknowledgment; >100% utilization is BLOCKING <!-- retros c8f2, k4m9 -->
```

**Integration notes**: This replaces the existing "80% blocking" criterion with the two-tier model. The change is in quality-gates.md (where validators read criteria) and pipeline-stages.md (where the SM validator is described). The two-tier model is more permissive for teams planning at 85-95% but retains a hard block at >100%. The Light Mode applicability is explicit per PRD Section 9.

---

## Milestone M4: Dev Stage DoD

### FR-11: "Regenerate derived artifacts" checklist item in pipeline-stages.md

**Target file**: `delivery-team/skills/delivery-flow/references/pipeline-stages.md` (verified on disk)

**Location**: Stage 6: Development > DoD Validators section, specifically the Developer validator (line 329 of current file).

**Change type**: MODIFY

**Current text**:

```markdown
- Developer [required]: code is clean, follows language best practices
  - Writes to: `.delivery/artifacts/06-dev/dod/{story-id}-developer-review.md`
```

**New text**:

```markdown
- Developer [required]: code is clean, follows language best practices, derived artifacts regenerated from current sources <!-- retro c8f2 -->
  - Writes to: `.delivery/artifacts/06-dev/dod/{story-id}-developer-review.md`
  - **Derived artifact check**: If the story modifies source files that have derived artifacts (e.g., generated docs, compiled schemas, transformed configs, built outputs), the developer must confirm all derived artifacts have been regenerated from current sources before marking the story complete. The DoD review must include a "Derived Artifacts" section listing: each derived artifact path, its source file(s), and regeneration status (regenerated / not applicable).
```

Also ADD to Stage 6: Development > Sub-Flow, after step 4 (Technical Writer) and before step 5 (Commit suggestion). Insert as new step 5, renumbering subsequent steps:

```markdown
5. **Regenerate derived artifacts** [SEQUENTIAL per story] [required]: Before Dev DoD, check if any modified source files have derived artifacts. If so:
   1. Identify all derived artifacts (generated docs, compiled schemas, transformed configs, etc.)
   2. Regenerate each derived artifact from its current source
   3. Verify the regenerated artifact matches expectations (no unexpected diffs)
   4. Document the regeneration in the story's implementation notes
   - **Light Mode**: Applies to all project types <!-- retro c8f2 -->
```

**Integration notes**: The derived artifact regeneration step runs per-story, after implementation and technical writing but before commit suggestion. This ensures commits include fresh derived artifacts. The Developer DoD validator checks for the "Derived Artifacts" section, creating accountability. Subsequent steps in Stage 6 Sub-Flow must be renumbered (current 5 becomes 6, current 6 becomes 7).

---

### FR-12: Derived artifact regeneration validator criterion in quality-gates.md

**Target file**: `delivery-team/skills/delivery-flow/references/quality-gates.md` (verified on disk)

**Location**: Gate 6: Development Quality checklist, insert after the existing item "Empirical validation requirements identified..." (line 198 of current file).

**Change type**: ADD

**Exact content to add** (new checklist item):

```markdown
- [ ] Derived artifacts regenerated: if any modified source files have derived artifacts (generated docs, compiled schemas, transformed configs), all derived artifacts have been regenerated from current sources and the regeneration is documented in the story's DoD review [blocking] <!-- retro c8f2 -->
```

**Integration notes**: The blocking severity ensures developers cannot skip regeneration. The criterion works with FR-11's DoD validator modification -- FR-11 defines what the Developer must check, FR-12 defines what the gate validator enforces. This closes the "derived artifact drift" root cause identified in retro c8f2.

---

## NFR Compliance Notes

| NFR | Compliance |
|-----|-----------|
| NFR-01 (Markdown-only) | All changes are markdown edits to existing files. No `.py`, `.js`, `.sh`, or other executables created. |
| NFR-02 (Config schema backward compat) | No new config keys introduced. Schema remains at v2.3. |
| NFR-03 (No regression) | Changes are additive to existing gates. No existing criteria removed or weakened. |
| NFR-04 (Token budget) | Estimated per-stage additions: UAT ~80 lines, Design ~5 lines, Plan ~15 lines, Dev ~15 lines. At ~10 words/line x 1.3 tokens/word = ~104, 65, 195, 195 tokens respectively. All well under 500-token per-stage limit. Cross-file additions (quality/SKILL.md ~60 lines, artifact-contracts.md ~40 lines, project-templates.md ~40 lines) are loaded on-demand, not per-stage. |
| NFR-05 (Retro traceability) | Every added section includes `<!-- retro c8f2 -->` or `<!-- retro k4m9 -->` inline annotation. |

---

## FR Traceability Matrix

| FR | Design Spec | Target File | Verified |
|----|-------------|-------------|----------|
| FR-01 | M1: Shared-module review checkpoint in UAT sub-flow + DoD validator | `delivery-team/skills/delivery-flow/references/pipeline-stages.md` | YES -- file exists, Stage 7 section located, insertion point identified (after step 4) |
| FR-02 | M1: Shared-module review protocol section in QA skill | `delivery-team/skills/quality/SKILL.md` | YES -- file exists, insertion point identified (after "Empirical Validation and CODE_COMPLETE Status" section) |
| FR-03 | M1: Empirical-items tracking template + Stage 6->7 contract update | `delivery-team/skills/delivery-flow/references/artifact-contracts.md` | YES -- file exists, Stage 6->7 table located, end-of-file insertion point identified |
| FR-04 | M1: Empirical-items classification criterion in Gate 7 checklist | `delivery-team/skills/delivery-flow/references/quality-gates.md` | YES -- file exists, Gate 7 section located, insertion point identified (after line 207) |
| FR-05 | M2: Phantom reference WARNING criterion in Gate 3 checklist | `delivery-team/skills/delivery-flow/references/quality-gates.md` | YES -- file exists, Gate 3 section located, insertion point identified (after line 153) |
| FR-06 | M2: Filename reconciliation gate in Dev entry conditions | `delivery-team/skills/delivery-flow/references/pipeline-stages.md` | YES -- file exists, Stage 6 Entry Conditions section located (line 302) |
| FR-07 | M3: Capacity matrix template in Sprint Plan Mandatory Sections | `delivery-team/skills/delivery-flow/references/project-templates.md` | YES -- file exists, end-of-file insertion point identified |
| FR-08 | M3: Coverage matrix template (combined with FR-07) | `delivery-team/skills/delivery-flow/references/project-templates.md` | YES -- combined with FR-07, same insertion point |
| FR-09 | M3: Matrix validation step in Plan sub-flow + SM validator update | `delivery-team/skills/delivery-flow/references/pipeline-stages.md` | YES -- file exists, Stage 5 Sub-Flow and DoD sections located |
| FR-10 | M3: Two-tier capacity threshold in Gate 5 + SM validator | `delivery-team/skills/delivery-flow/references/quality-gates.md` + `pipeline-stages.md` | YES -- both files exist, Gate 5 line 180 and Stage 5 DoD section located |
| FR-11 | M4: Derived artifact regeneration step + Developer validator update | `delivery-team/skills/delivery-flow/references/pipeline-stages.md` | YES -- file exists, Stage 6 Sub-Flow and DoD sections located |
| FR-12 | M4: Derived artifact regeneration criterion in Gate 6 checklist | `delivery-team/skills/delivery-flow/references/quality-gates.md` | YES -- file exists, Gate 6 section located, insertion point identified (after line 198) |

**All 12 FRs mapped. All target files verified on disk. No phantom references.**

---

## Change Summary by File

| Target File | FRs | Changes |
|---|---|---|
| `delivery-team/skills/delivery-flow/references/pipeline-stages.md` | FR-01, FR-06, FR-09, FR-10, FR-11 | ADD: UAT shared-module step (FR-01), Dev entry gate (FR-06), Plan matrix validation step (FR-09), Dev derived artifact step (FR-11). MODIFY: Plan SM validator (FR-09/FR-10), Dev Developer validator (FR-11). Renumber affected sub-flow steps in Stages 5, 6, 7. |
| `delivery-team/skills/delivery-flow/references/quality-gates.md` | FR-04, FR-05, FR-10, FR-12 | ADD: Gate 7 empirical-items criterion (FR-04), Gate 3 phantom WARNING criterion (FR-05), Gate 6 derived artifact criterion (FR-12). MODIFY: Gate 5 capacity threshold (FR-10). |
| `delivery-team/skills/delivery-flow/references/artifact-contracts.md` | FR-03 | ADD: Stage 6->7 contract table row, Empirical-Items Tracking Template section at end of file. |
| `delivery-team/skills/delivery-flow/references/project-templates.md` | FR-07, FR-08 | ADD: Sprint Plan Mandatory Sections with Capacity Matrix Template and Coverage Matrix Template. |
| `delivery-team/skills/quality/SKILL.md` | FR-02 | ADD: Shared-Module Review Protocol section. |
