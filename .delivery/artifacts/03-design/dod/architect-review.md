# Architect Review: User Flows — Presentation Skill v1.1

**Reviewer**: Celebrimbor (Solution Architect)
**Date**: 2026-04-04
**Artifact Under Review**: `.delivery/artifacts/03-design/ux/user-flows.md` v1.0
**PRD Reference**: `.delivery/artifacts/02-refine/po/prd.md` v1.0
**Gate**: 3 — Design DoD (Architect Validation)

---

> *"I have examined each ring of this design with the care one must give to works of binding power. The flows are well-forged. My assessment follows."*

---

## Assessment: DONE

The user flows are **implementable within the existing presentation skill structure**. No impossible interactions, no unrealistic assumptions, and no architectural violations were identified. The design is sound, additive, and structurally contained.

---

## Validation Criteria

### 1. Structural Containment (NFR-05)

**Verdict: PASS**

All changes described in the flows live within `delivery-team/skills/presentation/`. The flows introduce:

- Modifications to `SKILL.md` (type detection table, config keys, new step behaviors)
- Modifications to `references/narrative-patterns.md` (new frameworks, audience framing rules, type-specific tension patterns)
- New directory `scripts/` with `generate_pptx.py`
- New intermediate artifact `composed-draft.json` in `.drafts/`

No new top-level directories. No changes to other delivery-team skills. The contributing roles (PO, Developer, Architect, Data Analyst, QA, TW, UX) are consumed as-is via their existing skill invocations. This satisfies the plugin structure constraint.

### 2. Existing Flow Stability (NFR-01)

**Verdict: PASS**

The flows explicitly state they show "ONLY the delta from this baseline." The 6-step flow diagram is preserved verbatim as the foundation. All new behaviors are:

- **Additive branches** (PPTX generation post-approval, light mode evaluation pre-Step 3)
- **Insertions within existing steps** (four editorial passes inside Step 4 Compose)
- **Extended output sections** (Narrative Cuts, Emphasis Order in Step 6)

The four existing types (Sprint Review, Feature Pitch, Stakeholder Update, Technical Deep-Dive) are not modified. Their keyword detection, content gate rules, and narrative frameworks remain unchanged. This is genuinely additive enhancement.

### 3. New Type Implementability (FR-01 through FR-06)

**Verdict: PASS**

Each of the five new types follows the identical structural pattern as the existing four:

| Aspect | Pattern | All 5 New Types Conform? |
|--------|---------|--------------------------|
| Keyword detection triggers | String match list | Yes |
| Pipeline auto-detection mapping | Stage + context -> type | Yes (where applicable) |
| Narrative framework | Named pattern (e.g., Traction-Opportunity-Ask) | Yes |
| Default slide sequence | Ordered list of slide titles | Yes |
| Content Gate rules | Required + Enhancing artifact lists | Yes |
| Role dispatch | Subset of existing 5 roles | Yes |
| Step 4-6 behavior | Standard unless noted | Yes |

Specific observations:

- **Investor Pitch**: The Traction-Opportunity-Ask framework is new to `narrative-patterns.md` but follows the same structural shape as existing frameworks (SCR, Pyramid, Problem-Solution-Benefit, Before-After-Bridge). Implementable as a new section in the reference file.
- **Roadmap**: The Now-Next-Later temporal constraint ("Composer must NOT reorder Now/Next/Later") is a sensible locked-slide rule. The flows correctly note this interacts with narrative tension by constraining reordering to within time horizons, not across them. No conflict.
- **Product Demo**: The `[DEMO]` placeholder pattern is new but trivial to implement -- it is string formatting in the Compose step. Speaker notes auto-enable for demo slides is a conditional default, not a structural change.
- **Onboarding**: Default audience "technical" without prompting is a type-specific default override. The existing precedence chain (explicit request > config > type default > hardcoded default) already supports this pattern.
- **Retrospective Summary**: The sensitivity filter is the most complex addition. It is audience-conditional (executive/client-facing ON, technical/casual OFF) and applies during Compose. This is implementable as a conditional editorial pass in Step 4, similar in mechanism to the narrative intelligence passes. The disclaimer is an unconditional output append. No architectural concern.

### 4. PPTX Generation Path (FR-07 through FR-11)

**Verdict: PASS**

The PPTX flow is architecturally clean:

1. The intermediate JSON artifact (`composed-draft.json`) resolves OQ-1 correctly. Regex-based markdown parsing would have been a maintenance burden. The JSON structure is well-defined with clear per-slide fields (layout, title, body, table, speaker_notes, mermaid, citations).
2. The generation step occurs **post-approval** in Step 6, meaning it cannot interfere with the review flow. The Composer writes both `.md` and `.json` in Step 4; the script consumes `.json` only after user approval.
3. The `python-pptx` dependency is correctly isolated -- the check happens at generation time, not at flow start. Graceful fallback to structured-markdown preserves the user experience.
4. The branding resolution order (CLI flags > config > defaults) follows the existing precedence pattern used throughout the presentation skill. No novel resolution logic.
5. Layout mapping (layout name first, fall back to index) is the standard `python-pptx` pattern. The seven layout types (title, content, metrics, comparison, cta, timeline, architecture) map cleanly to the slide types already defined in `slide-structure.md`.

**One observation** (not a blocker): The architecture slide layout says `[Mermaid diagram]` as a text note. This is explicitly out of scope per PRD Section 7, and the flow correctly documents it. No concern, but the script should include a comment referencing this scope decision for future maintainers.

### 5. Light Mode and Threshold Degradation (FR-12 through FR-15)

**Verdict: PASS**

The light mode evaluation occurs before Step 3 (Draft), which is the correct insertion point -- it determines how many roles to dispatch. The interaction matrix (Flow C.4) between light mode and threshold degradation is well-defined and demonstrates the two controls converge rather than conflict.

Key architectural validation:

- **Light mode never skips steps.** This directly aligns with the project directive "Light stages MUST execute. Light means reduced depth, NOT skipped." The flows enforce this -- Step 5 still runs with a single reviewer, never zero.
- **Threshold degradation is progressive.** The 75% warning trigger followed by the 100% notice is a two-stage degradation that gives the user visibility without abruptly changing behavior.
- **Threshold = 0 means unlimited.** This is a clean sentinel value. No edge case concerns.
- **Timer scope**: The timer starts pre-flow and measures wall clock time. This is the correct approach since sub-agent dispatch is the dominant time cost, and reducing sub-agents (light mode) directly addresses it.

### 6. Narrative Intelligence (FR-16 through FR-20)

**Verdict: PASS**

The four editorial passes in Step 4 are the most significant architectural addition. They are:

1. **Sequential, not parallel.** Each pass reads the output of the previous one. This is correct -- emphasis reordering must happen before cutting (you cut after you know the order), cutting before framing (you frame what survives), and framing before tension (tension operates on framed content).
2. **Each pass is independently disableable.** `narrative_reorder: false` skips Pass 1, `narrative_cutting: false` skips Pass 2. Pass 3 (audience framing) always runs. Pass 4 (tension) has a natural gate (< 6 slides = skip). This granular control satisfies PRD constraint 5 ("rule-based, not ad-hoc").
3. **Locked slides are respected.** PO-sequenced slides and structural sequences (Now/Next/Later) are untouched by reordering and tension. This prevents the Composer from overriding the PO's explicit decisions.
4. **Review Gate expansion** (FR-20) adds narrative quality criteria to both reviewers without changing the MUST-FIX/SUGGESTION classification system. This is a scope expansion of existing behavior, not a structural change.
5. **User recovery** (restore, no reorder) provides escape hatches for all editorial decisions. The "restore {slide title}" command in Step 6 re-enters the flow at Step 4 with the cut slide reinstated. This is architecturally identical to the existing "changes" routing mechanism.

### 7. Open Question Resolutions

**Verdict: PASS** -- All five OQs are resolved.

| OQ | Resolution | Architect Assessment |
|----|-----------|---------------------|
| OQ-1 | Structured JSON intermediate | Correct. More robust than regex parsing. |
| OQ-2 | User order takes precedence; tension reorders only unconstrained groups | Correct. Respects PO authority. |
| OQ-3 | Universal rules with type-specific weight modifiers | Correct. Single rule set with per-type tuning avoids rule explosion. |
| OQ-4 | (Not resolved in UX flows -- deferred to Architect) | See note below. |
| OQ-5 | Speaker notes carry to PPTX via JSON field | Correct. Clean data path. |

**OQ-4 Note**: The flows define light mode activation as "3 or fewer contributing roles." This is a reasonable threshold. The minimum meaningful presentation is likely 3-4 slides (a Feature Pitch with only PO and Developer), and light mode still dispatches all required roles -- it only skips optional slots and reduces the review gate. I recommend the value of 3 as proposed. If empirical testing during dogfooding reveals this threshold is too aggressive or too conservative, it is a single integer change in SKILL.md with no architectural impact.

### 8. Cross-Cutting Concerns

**Config schema extension**: Eight new `presentation.*` keys are proposed. All are optional with sensible defaults. They follow the existing namespace pattern. Config schema version bump is required per the extension protocol in `config-schema.md` v2.3. No concern.

**Artifact lifecycle**: The `.drafts/` directory is cleaned up on approve and abort. The new `composed-draft.json` follows the same lifecycle as `composed-draft.md`. No orphan artifacts.

**Error handling**: Flow A.6 updates the error message to list all 9 types. The flows correctly show the before/after comparison. No missing error paths were identified.

---

## Issues Found

**None.** No blocking issues, no impossible interactions, no unrealistic assumptions.

---

## Recommendations (Non-Blocking)

1. **OQ-4 formalization**: Document the light mode threshold (3 roles) as a named constant in SKILL.md rather than embedding it in prose. This makes it discoverable for future tuning.

2. **Mermaid scope comment**: The `generate_pptx.py` script should include a code comment at the architecture slide handler referencing PRD Section 7 (out of scope) and the flow's `[Mermaid diagram]` text note pattern. This prevents a future contributor from attempting to add image rendering without understanding the scope decision.

3. **Degradation timer measurement**: The flows state the timer measures wall clock time. During implementation, consider logging both wall clock and approximate sub-agent dispatch count, so threshold tuning can be data-informed rather than purely time-based.

---

## Summary

The user flows are a faithful, implementable translation of the PRD's 20 functional requirements into interaction sequences. The existing 6-step flow is preserved as the backbone. All new behaviors are additive branches, conditional passes, or extended output sections. The `scripts/` directory and `composed-draft.json` intermediate are the only new structural elements, and both fit cleanly within the existing plugin structure. No architectural violations or impossible interactions were found.

The design is ready to proceed to the Architect stage for technical decomposition.

---

*"These flows bear the marks of careful craft. They shall endure the fires of implementation without fracture. I set my seal upon them."*
