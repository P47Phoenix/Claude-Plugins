# Architect DoD Review -- PRD: Presentation Skill v1.1 Enhancement Batch

**Reviewer**: Architect (Celebrimbor)
**Date**: 2026-04-04
**Artifact**: `.delivery/artifacts/02-refine/po/prd.md` (v1.0)
**Status**: DONE

---

> *"I perceive four works of craft before me -- each well-forged in purpose, each sound in design. The rings of power were built in sequence; so too shall these enhancements be."*

## Gate 2 Architect Criteria

### 1. Technically Feasible, No Blockers

- [x] **Technically feasible, no blockers** [blocking]

| Feasibility Area | Assessment |
|-----------------|------------|
| Group A: FR-01 through FR-06 (5 Deferred Types) | **Feasible.** The existing skill already supports 4 types with keyword detection, pipeline auto-detection, content gate rules, slide sequencing, and narrative framework mapping. Each new type follows the identical pattern -- a new row in detection tables, a new content gate rule set, a new narrative framework, and a new slide sequence. The SKILL.md, `narrative-patterns.md`, and `slide-structure.md` files accept additive entries. No structural changes to the 6-step flow are required. The Retrospective Summary sensitivity filter (FR-05.4) is a conditional rule on audience mode -- straightforward branching logic in the Composer step. |
| Group B: FR-07 through FR-11 (PPTX Output) | **Feasible.** `python-pptx` is a mature, pure-Python library (PyPI, MIT licensed, widely used). Slide layout mapping (FR-08) uses `python-pptx`'s `slide_layouts` collection with name-based matching and index fallback -- a documented pattern. Template consumption (FR-09) is native to `python-pptx` via `Presentation(template_path)`. The script parses a structured markdown file (composed-draft.md) using regex or section parsing -- bounded complexity. Font and color configuration (FR-11) maps directly to `python-pptx` font and color API. The script lives in `scripts/` within the existing plugin directory -- no structural novelty. |
| Group C: FR-12 through FR-15 (90-Second Fallback) | **Feasible.** Progress indicators (FR-12) are output strings at step boundaries -- already partially implemented as `[N/6]` prefixes. Light mode (FR-13) reduces sub-agent dispatch count, which is a conditional filter on the existing parallel dispatch logic in Step 3. Per-type thresholds (FR-14) are config lookups. Degradation behavior (FR-15) is conditional logic at 75% and 100% of threshold -- no timer infrastructure needed since each step is sequential and elapsed time is trackable within the flow. |
| Group D: FR-16 through FR-20 (Narrative Intelligence) | **Feasible.** Emphasis selection (FR-16) adds a ranking pass before slide ordering in Step 4 -- the Composer already reads all draft files and assembles them. Information cutting (FR-17) adds an evaluation pass that flags low-value slides -- implementable as rules in `narrative-patterns.md`. Audience framing (FR-18) extends the existing tone normalization with structural reframing rules per audience mode. Narrative tension (FR-19) adds a climax-positioning rule for 6+ slide presentations. Review Gate criteria expansion (FR-20) adds new evaluation dimensions to the TW and UX reviewer prompts. All changes are additive to the Compose step. |
| Cross-cutting: Config Schema Extension | **Feasible.** 8 new keys in the `presentation.*` namespace. The config-schema.md v2.3 extension protocol exists and has been exercised before. All keys are optional with defaults. A version bump to the config schema is required but routine. |
| Cross-cutting: Plugin Structure Compliance | **Feasible.** All changes are within `delivery-team/skills/presentation/`. New files: one Python script in `scripts/`, extended content in `references/narrative-patterns.md` and `references/slide-structure.md`, and updated SKILL.md. No new top-level directories. |

**No technical blockers identified.** The enhancement batch is entirely additive to an existing, stable skill. Group A extends lookup tables and reference documentation. Group B adds an optional output path via a mature third-party library. Group C adds conditional logic around existing step boundaries. Group D extends the Compose step with rule-based passes that operate on the same data the Composer already reads.

### 2. NFRs Realistic

- [x] **NFRs realistic** [blocking]

| NFR | Assessment |
|-----|-----------|
| NFR-01 (Backward compatibility) | **Realistic.** All changes are additive -- new type entries in detection tables, new config keys with defaults, new optional output format. The 6-step flow structure is unchanged. Existing types, formats, and config keys are not modified. |
| NFR-02 (Generation speed -- light mode, <60s) | **Realistic.** Light mode dispatches 3 or fewer sub-agents in Step 3 and a single reviewer in Step 5. Reducing from 5 parallel agents + 2 reviewers to 3 + 1 is a meaningful reduction. Sub-agent dispatch is the primary time cost. 60 seconds is achievable for simple types. |
| NFR-03 (Generation speed -- full mode, <120s) | **Realistic with caveat.** Complex types with 5 contributing roles and 10+ slides require 5 parallel sub-agent dispatches + 2 reviewer dispatches + Compose step. 120 seconds is tight but achievable if sub-agents run in parallel as designed. The per-type threshold override (FR-14) provides an escape valve for types that consistently exceed 120s. |
| NFR-04 (Single new dependency) | **Realistic.** `python-pptx` is the sole addition. It is optional -- all core functionality works without it. The fallback behavior (FR-10.4) is specified. No transitive dependency concerns for a pure-Python library. |
| NFR-05 (Plugin structure compliance) | **Realistic.** Verified: `delivery-team/skills/presentation/` exists with the expected structure (`SKILL.md`, `references/` with 4 files). Adding `scripts/` is a standard pattern used elsewhere in the repo. |
| NFR-06 (Config schema extension) | **Realistic.** The extension protocol exists in config-schema.md v2.3. Eight optional keys with defaults is a modest extension. Schema generation and validation scripts exist at `delivery-team/scripts/generate-schema.py` and `validate-config.py`. |
| NFR-07 (Dogfooding validation) | **Realistic.** Each new type has explicit acceptance criteria that require end-to-end execution. The pipeline itself can produce artifacts to feed each presentation type. This is a process requirement, not a technical one. |
| NFR-08 (PPTX output quality) | **Realistic.** The "good enough to edit" bar is appropriate for programmatic generation. `python-pptx` produces structurally correct files. The disclaimer (section 12) sets expectations correctly. Mermaid-to-text fallback (FR-08.7) avoids an impossible rendering problem. |

**All 8 NFRs are achievable within the stated scope.** NFR-03 carries a minor risk for the most complex types, but the per-type threshold override mitigates this adequately.

---

## Open Questions Assessment (Architect-Relevant)

| OQ | Pre-Assessment | Feasibility Risk |
|----|---------------|-----------------|
| OQ-1 (Structured intermediate format vs regex parsing) | Both approaches are feasible. Structured intermediate (JSON/YAML) is more robust and simplifies the PPTX script but adds an artifact to the Compose step. Regex parsing of composed-draft.md is simpler but brittle against formatting variations. **Recommendation**: Structured intermediate -- the composed-draft.md format is already well-defined with consistent heading patterns; a parallel JSON output is low cost. Solvable in Design. | None |
| OQ-2 (Narrative tension vs user-specified order) | Solvable with precedence rule: explicit user outline overrides auto-reorder. The PRD already includes FR-16.3 (`"no reorder"` command) and FR-16.4 (`narrative_reorder: false` config). These provide sufficient escape hatches. Design should clarify default precedence. | None |
| OQ-3 (Type-specific vs universal emphasis/cutting rules) | Both approaches are feasible. Type-specific rules are more accurate but add reference file complexity. **Recommendation**: Start with universal rules, add type-specific overrides where dogfooding reveals inadequacy. Solvable in Design. | None |
| OQ-4 (Minimum slide count for light mode) | This is a threshold question, not a feasibility question. The PRD already gates light mode on "3 or fewer contributing roles" (FR-13.1), which is type-driven, not slide-driven. Slide count is a secondary signal. Solvable in Architect stage. | None |
| OQ-5 (Speaker notes in PPTX) | `python-pptx` supports speaker notes via `slide.notes_slide.notes_text_frame`. The existing skill supports speaker notes as optional. Carrying this through to PPTX is trivial. Solvable in Design. | None |

All five open questions are tractable with zero feasibility risk. None require changes to the PRD scope.

---

## Architectural Observations

1. **Delivery sequence is sound.** Group A first (unblocks type definitions), Group D second (narrative rules apply to all types), Group C third (thresholds need type definitions), Group B last (output script consumes composed artifacts from all types). The noted parallelism between A/B and C/D after A completes is valid.

2. **The Composer's role expansion is the key architectural concern.** Groups C and D both add logic to Step 4 (Compose). The Composer currently handles: reference loading, narrative arc, opening/closing slides, tone normalization, density enforcement, transitions, format application, citations, and speaker notes. Adding emphasis ranking, information cutting, audience framing, and narrative tension is a meaningful expansion. The SKILL.md instructions will need clear ordering of these new passes to avoid conflicts (e.g., cutting a slide that was positioned as the climax). Design should define a Compose sub-step ordering.

3. **The sensitivity filter for Retrospective Summary (FR-05.4) is a content transformation, not just a formatting rule.** It anonymizes and generalizes individual feedback. This is qualitatively different from tone normalization. Design should treat this as a distinct Compose sub-step with clear transformation rules, not embed it in general tone normalization.

---

## Verdict

**DONE.** The PRD for Presentation Skill v1.1 is technically feasible with zero blockers across all four groups (20 functional requirements). All 8 NFRs are realistic and achievable. The existing skill structure (`SKILL.md`, `references/`, and the 6-step flow) accommodates every proposed enhancement through additive changes. The sole new dependency (`python-pptx`) is mature, optional, and well-scoped. All 5 open questions are tractable with no feasibility risk. Three architectural observations are noted for the Design and Architect stages -- none are blockers.

```
STATUS: DONE
ARTIFACT: .delivery/artifacts/02-refine/dod/architect-review.md
SUMMARY: Gate 2 DONE. All 20 FRs feasible (additive to existing skill). 8 NFRs realistic. python-pptx sole dependency, optional. 5 OQs tractable. 3 observations for Design.
```
