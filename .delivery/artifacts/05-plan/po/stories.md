## User Stories

### Story 1: Remove Duplicated Stage Definitions from SKILL.md

**ID**: BF-62-001
**Priority**: High
**Estimate**: 2 SP (markdown refactoring -- one tier lower than standard BUG_FIX)
**References**: Issues #60, #61, #62

#### Story

As the delivery-flow orchestrator, I need SKILL.md to reference `references/pipeline-stages.md` as the single source of truth for detailed stage definitions, so that I follow one consistent set of agent invocations, artifact paths, and DoD templates instead of drifted duplicates.

#### Acceptance Criteria

| # | Criterion | Type | Verification |
|---|-----------|------|-------------|
| AC-1 | The "Stage Definitions" section (lines ~522-928) in SKILL.md is replaced with a concise summary per stage that references `references/pipeline-stages.md` for detailed sub-flows, agent invocations, and artifact paths | Structural | Inspect SKILL.md -- no detailed agent invocation steps, no specific artifact output paths per stage in the Stage Definitions section |
| AC-2 | SKILL.md retains: (a) the Stage Routing Matrix table, (b) high-level purpose and "Runs for" per stage, (c) collaboration pattern assignments per stage, (d) human checkpoint assignments per stage, (e) max self-correction limits per stage | Structural | Inspect SKILL.md -- all five elements present for each stage |
| AC-3 | All artifact paths remaining in SKILL.md use the namespaced convention `.delivery/artifacts/{NN}-{stage-name}/{role}/{artifact-name}.md`, matching pipeline-stages.md | Structural | Search SKILL.md for `.delivery/artifacts/` -- every occurrence uses namespaced format; zero flat paths like `01-idea-brief.md` or `02-prd.md` |
| AC-4 | The DoD validator template in the "Team Definition of Done Protocol" section no longer contains `[ARTIFACT CONTENT]` inline. Instead it references the DoD Validator Dispatch Template in `references/pipeline-stages.md` | Structural | Inspect the Team DoD Protocol section -- no `[ARTIFACT CONTENT]` block; contains explicit reference to pipeline-stages.md DoD Validator Dispatch Template |
| AC-5 | SKILL.md contains an explicit directive stating that `references/pipeline-stages.md` is the authoritative source for: (a) stage sub-flows and agent invocations, (b) artifact output paths (namespaced), (c) DoD validator dispatch templates | Structural | Search SKILL.md for the directive text referencing pipeline-stages.md as authoritative |
| AC-6 | The Cross-Stage Artifact Flow table in SKILL.md either uses namespaced paths or uses generic names without paths (deferring to pipeline-stages.md for exact paths) | Structural | Inspect the Cross-Stage Artifact Flow section -- no flat artifact paths |
| AC-7 | Pipeline execution is not broken: Phase 4 Step 3 still directs the orchestrator to load stage definitions from `references/pipeline-stages.md`, and Stage Routing Matrix is intact for routing decisions | Structural | Inspect Phase 4 Step 3 -- references pipeline-stages.md; Stage Routing Matrix table is present and unchanged |

#### Test Cases

| TC | Covers AC | Test | Expected Result |
|----|-----------|------|-----------------|
| TC-1 | AC-1, AC-5 | Search SKILL.md for any of: "Primary agent:", "Supporting agent:", "Input:", "Output:" patterns within Stage Definitions section | Zero matches in Stage Definitions. These details exist only in pipeline-stages.md |
| TC-2 | AC-3 | `grep -c 'artifacts/0[1-7]-[a-z]' SKILL.md` (flat path pattern matching `NN-word` without a following `/`) | Count = 0. No flat artifact paths remain |
| TC-3 | AC-3 | `grep 'artifacts/0[1-7]-' SKILL.md` | Every match uses namespaced format `{NN}-{stage-name}/{role}/` |
| TC-4 | AC-4 | Search SKILL.md for `[ARTIFACT CONTENT]` | Zero matches |
| TC-5 | AC-4 | Inspect Team DoD Protocol section for reference to pipeline-stages.md DoD Validator Dispatch Template | Reference is present |
| TC-6 | AC-2 | For each of stages 1-7, verify SKILL.md contains: purpose line, "Runs for" line, collaboration patterns, human checkpoint, max self-correction | All present for all 7 stages |
| TC-7 | AC-7 | Verify Phase 4 Step 3 text references pipeline-stages.md | Reference is present and unmodified |
| TC-8 | AC-6 | Inspect Cross-Stage Artifact Flow table | No flat artifact paths; either namespaced or generic names |
| TC-9 | AC-1 | Count lines in SKILL.md Stage Definitions section | Significantly fewer than the current ~400 lines (target: ~100-150 lines for summaries) |
| TC-10 | AC-5 | Grep SKILL.md Stage Definitions for "See `references/pipeline-stages.md`" or equivalent authoritative-source directive | Each stage definition references pipeline-stages.md as the authoritative source for sub-flows, agent invocations, and artifact paths |
