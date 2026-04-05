# Architect DoD Review: SKILL.md / pipeline-stages.md Refactoring

**Reviewer**: Celebrimbor (Solution Architect)
**Date**: 2026-04-04
**Artifact**: `delivery-team/skills/delivery-flow/SKILL.md`
**Companion**: `delivery-team/skills/delivery-flow/references/pipeline-stages.md`

---

## 1. Boundary Clarity: Orchestrator vs Sub-Flow

| Criterion | Verdict | Notes |
|-----------|---------|-------|
| SKILL.md = orchestrator routing decisions | PASS | SKILL.md defines Phases 0-4 (setup, detection, memory, routing, execution protocol), stage summaries with routing metadata only, guardrails, escalation, and commands. It explicitly delegates sub-flow details with "See `references/pipeline-stages.md`" at every stage summary. |
| pipeline-stages.md = sub-flow execution details | PASS | Contains detailed sub-flows per stage (entry conditions, agent invocations with SKILL/TASK_TYPE/ROLE, artifact paths, DoD validators, game dev additions), plus the three Agent Invocation Templates (Primary, Supporting, DoD Validator). |
| No duplication between the two files | PASS | SKILL.md Stage Definitions (lines 522-653) contain only routing metadata (runs-for, skipped-for, purpose, primary agent, upstream artifacts, collaboration patterns, DoD validators, checkpoints, max iterations, output paths). pipeline-stages.md contains the procedural sub-flows. The two are complementary, not redundant. |
| Authority declaration present | PASS | SKILL.md line 524-527 explicitly states: "Authoritative source: `references/pipeline-stages.md` is the single source of truth for stage sub-flows, agent invocation details, artifact output paths (namespaced), and DoD Validator Dispatch Templates." |

**Assessment**: The boundary is clean and well-defined. The orchestrator knows *what* to invoke and *when*; pipeline-stages.md knows *how* each stage executes internally.

---

## 2. Phantom File References

| Reference | Source File | Exists? | Verdict |
|-----------|------------|---------|---------|
| `references/pipeline-stages.md` | SKILL.md | Yes | PASS |
| `references/project-types.md` | SKILL.md | Yes | PASS |
| `references/quality-gates.md` | SKILL.md | Yes | PASS |
| `references/team-patterns.md` | SKILL.md | Yes | PASS |
| `references/memory-protocol.md` | SKILL.md | Yes | PASS |
| `references/setup-wizard.md` | SKILL.md | Yes | PASS |
| `references/config-schema.md` | SKILL.md | Yes | PASS |
| `references/defect-tracking.md` | SKILL.md | Yes | PASS |
| `references/git-integration.md` | SKILL.md, pipeline-stages.md | Yes | PASS |
| `references/github-integration.md` | SKILL.md, pipeline-stages.md | Yes | PASS |
| `references/getting-started.md` | SKILL.md | Yes | PASS |
| `references/analytics.md` | SKILL.md | Yes | PASS |
| `references/artifact-contracts.md` | SKILL.md | Yes | PASS |
| `references/monorepo.md` | SKILL.md | Yes | PASS |
| `references/notifications.md` | SKILL.md | Yes | PASS |
| `references/project-templates.md` | SKILL.md | Yes | PASS |
| `references/feature-knowledge.md` | SKILL.md, pipeline-stages.md | Yes | PASS |
| `references/pipeline-scope.md` | SKILL.md | Yes | PASS |
| `references/domain-discovery.md` | pipeline-stages.md (Stage 4, step 1) | Yes (architect skill) | PASS |
| quality skill `references/milestone-testing.md` | pipeline-stages.md (Stage 6) | Yes | PASS |
| quality skill `references/exploratory-testing.md` | pipeline-stages.md (Stage 6, 7) | Yes | PASS |
| **"architecture Section 3"** | SKILL.md line 368 | **NO** | **FAIL** |
| **"architecture document Section 6"** | pipeline-stages.md line 11 | **NO** | **FAIL** |

### Phantom References Found

Two references cite an "architecture document" with numbered sections that does not exist anywhere in the delivery-flow references directory:

1. **SKILL.md line 368**: `"see architecture Section 3 and references/pipeline-stages.md for the exact fields per stage"` -- There is no architecture document with a Section 3. The Agent Invocation Templates now live in `references/pipeline-stages.md` itself, making the "architecture Section 3" portion a phantom. The `references/pipeline-stages.md` reference alone is sufficient.

2. **pipeline-stages.md line 11**: `"See the architecture document Section 6 for the full namespace map"` -- There is no architecture document with a Section 6. The namespace convention is defined inline in pipeline-stages.md itself (lines 1-11), making this a self-referential phantom.

**Recommended fix**: Remove the phantom "architecture Section N" references. For SKILL.md line 368, keep only the `references/pipeline-stages.md` reference. For pipeline-stages.md line 11, remove the sentence or replace with "See the namespace convention above."

---

## 3. Cross-Reference Integrity

| Cross-Reference | Direction | Verdict | Notes |
|-----------------|-----------|---------|-------|
| SKILL.md -> pipeline-stages.md | SKILL -> reference | PASS | 10+ references, all valid. Each stage summary links correctly. |
| pipeline-stages.md -> SKILL.md Phase 4 Step 4 | reference -> SKILL | PASS | Line 25 correctly references SKILL.md's alias personality_strength protocol. |
| pipeline-stages.md -> SKILL.md (isolation rules) | reference -> SKILL | PASS | Agent templates reference "Your SKILL.md" meaning the invoked agent's own SKILL.md, not delivery-flow's. Correct usage. |
| defect-tracking.md -> pipeline-stages.md | reference -> reference | PASS | Line 110 references pipeline-stages.md for process gap fixes. |
| team-patterns.md -> Agent Invocation Template | reference -> reference | PASS | Line 322 references the template, which now lives in pipeline-stages.md where it belongs. |
| SKILL.md Phase 0 -> pipeline-stages.md aliases | SKILL -> reference | PASS | Phase 0 loads alias theme; pipeline-stages.md documents how aliases are injected into templates. Consistent. |

---

## 4. Architectural Drift Assessment

| Concern | Verdict | Notes |
|---------|---------|-------|
| Stage routing matrix consistency | PASS | SKILL.md Phase 3 matrix matches pipeline-stages.md stage definitions. |
| DoD validator lists consistency | PASS | SKILL.md stage summaries list the same validators as pipeline-stages.md detailed DoD sections. |
| Artifact path consistency | PASS | Both files use identical namespaced paths (e.g., `.delivery/artifacts/02-refine/po/prd.md`). |
| Collaboration pattern assignment | PASS | SKILL.md stage summaries match pipeline-stages.md sub-flow pattern invocations. |
| Human checkpoint numbering | PASS | SKILL.md: Checkpoints 1-4 at Refine/Architect/Plan/UAT. pipeline-stages.md: same stages, same numbering. |
| Agent Invocation Template ownership | PASS | Templates live in pipeline-stages.md (sub-flow execution detail). SKILL.md references them but does not duplicate their structure. |
| Post-acceptance protocol | PASS | Both files describe the same 7-step post-acceptance sequence (state cleanup, retro, archive, lessons, index, defect review, FKC update). |

---

## 5. Overall Verdict

| Criterion | Status |
|-----------|--------|
| No architectural drift | PASS |
| Complementary boundary (orchestrator vs sub-flow) | PASS |
| No phantom file references | **FAIL** (2 phantom "architecture Section N" references) |
| Cross-reference integrity | PASS |

### Summary

The refactoring achieves clean separation of concerns. SKILL.md governs orchestration routing; pipeline-stages.md governs sub-flow execution. Two phantom references to a nonexistent "architecture document" with numbered sections remain -- one in each file. These are the sole defects. All other file references, cross-references, and architectural invariants are intact and consistent.

---

```
STATUS: NOT_DONE
ARTIFACT: .delivery/artifacts/06-dev/dod/architect-review.md
SUMMARY: Clean boundary, no drift, but 2 phantom "architecture Section N" refs found in SKILL.md:368 and pipeline-stages.md:11.
FINDINGS:
- SKILL.md line 368 references "architecture Section 3" which does not exist -- remove phantom, keep pipeline-stages.md reference
- pipeline-stages.md line 11 references "architecture document Section 6" which does not exist -- remove or replace with inline reference
```
