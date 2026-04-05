## Sprint Plan

**Sprint Goal**: Eliminate SKILL.md stage definition duplication, fixing artifact path drift and DoD template violation (Issues #60, #61, #62)
**Velocity Ceiling**: 80%
**Sprint Capacity**: 1 story, 2 SP
**Load**: 2 / 2.5 available = 80% (at ceiling)

---

### Story Sequence

| Order | Story ID | Title | SP | Dependencies |
|-------|----------|-------|----|-------------|
| 1 | BF-62-001 | Remove Duplicated Stage Definitions from SKILL.md | 2 | None |

---

### Implementation Approach

**Single file**: `delivery-team/skills/delivery-flow/SKILL.md`

**Sections to modify** (in order of operation):

1. **Stage Definitions section (lines ~522-928)**
   - Remove detailed agent invocations, input/output specifications, supporting agent details
   - Keep per stage: purpose (1-2 lines), "Runs for" with depth, collaboration patterns, human checkpoint, max self-correction, game dev additions (summary only)
   - Add per stage: explicit reference to `references/pipeline-stages.md` for detailed sub-flow, agent invocations, and artifact paths
   - Fix any remaining artifact path references to use namespaced convention

2. **Team Definition of Done Protocol section (lines ~930-980)**
   - Remove the inline DoD validator template containing `[ARTIFACT CONTENT]`
   - Replace with reference to the DoD Validator Dispatch Template in `references/pipeline-stages.md`
   - Keep: the execution steps (identify validators, evaluate votes, self-correction on NOT_DONE, track iterations, escalate on exhaustion)

3. **Cross-Stage Artifact Flow table (lines ~1031-1050)**
   - Replace flat artifact names (e.g., "idea brief", "PRD") with either namespaced paths or add a note deferring to pipeline-stages.md for exact paths

4. **Any remaining flat artifact paths throughout SKILL.md**
   - Search and replace all instances of flat paths with namespaced equivalents

**What NOT to change**:
- Phase 0 (Setup Wizard) -- no stage definitions here
- Phase 1 (Project Type Detection) -- no stage definitions here
- Phase 2 (Memory Retrieval) -- no stage definitions here
- Phase 3 (Stage Routing) -- the Stage Routing Matrix table stays as-is
- Phase 4 (Pipeline Execution Protocol) -- the step-by-step protocol stays; only Step 3 is verified (already references pipeline-stages.md)
- Guardrails section -- stays as-is
- User Commands section -- stays as-is
- References table -- stays as-is

---

### Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| Removing too much from stage definitions, breaking orchestrator flow | Low | Medium | Keep all routing-relevant info (runs-for, depth, checkpoints, collaboration patterns). Only remove what is duplicated in pipeline-stages.md |
| Missing a flat artifact path in a non-Stage-Definitions section | Low | Low | Run TC-2 and TC-3 grep tests to catch all occurrences |
| Cross-Stage Artifact Flow table changes confuse orchestrator | Low | Low | Table already uses generic names; just ensure no flat paths leak in |

---

### Definition of Done

- All 7 ACs pass (structural verification)
- All 9 TCs pass
- SKILL.md still loads and parses correctly (no broken markdown)
- `references/pipeline-stages.md` is NOT modified (single-file change)
