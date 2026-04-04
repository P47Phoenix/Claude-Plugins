# UX Designer DoD Review — Gate 3: Design Completeness

**Reviewer**: Galadriel (UX Designer)
**Date**: 2026-04-04
**Artifact**: `.delivery/artifacts/03-design/ux/user-flows.md` v1.0
**PRD**: `.delivery/artifacts/02-refine/po/prd.md` v1.0

---

> *"Even the smallest flow may change the course of the presentation. I have seen it in the mirror."*

---

## Gate 3 UX Criteria

### 1. Flows complete [blocking]

**PASS**

Every user-facing flow is designed end-to-end. The user-flows document establishes the existing 6-step baseline and then documents ONLY the deltas -- a wise choice that avoids duplication and makes changes auditable.

| Flow Group | Flows Defined | End-to-End Coverage |
|------------|--------------|-------------------|
| Group A: New Types (5) | A.1 Investor Pitch, A.2 Roadmap, A.3 Product Demo, A.4 Onboarding, A.5 Retrospective Summary, A.6 Error Handling | Each type covers: trigger detection, Assemble (PO framework + slide sequence), Content Gate (required/enhancing), Draft (role dispatch), Compose through User Review. All 6 steps addressed per type. |
| Group B: PPTX Output | B.1 PPTX Generation, B.2 Template/Branding | Post-approval branch with dependency check, script invocation, fallback path, cleanup on abort. Branding resolution order defined with 5-level precedence. |
| Group C: 90-Second Fallback | C.1 Progress Indicators, C.2 Light Mode, C.3 Threshold/Degradation, C.4 Interaction Matrix | Timer lifecycle, 75%/100% threshold triggers, degradation effects, light mode + threshold independence matrix. |
| Group D: Narrative Intelligence | D.1 Compose with 4 Editorial Passes, D.2 Review Gate Expansion, D.3 User Review Transparency | 4 sequential editorial passes (Emphasis, Cutting, Framing, Tension) with per-pass config toggles, expanded review criteria, new User Review sections. |

The combined end-to-end journey (Investor Pitch + PPTX + all enhancements) demonstrates all four groups working together -- a critical integration validation.

### 2. Follows UX best practices [blocking]

**PASS**

| Best Practice | Assessment |
|--------------|------------|
| **Progressive disclosure** | The 6-step flow reveals complexity gradually. Users see outline first (Step 1), approve, then the system does its work. Narrative intelligence details surface only at User Review (Step 6) via Narrative Cuts and Emphasis Order sections -- not during processing. |
| **User control** | Two human checkpoints preserved (Step 1 outline approval, Step 6 final review). New `restore {slide}` and `no reorder` commands give users undo capability for narrative intelligence decisions. Config toggles (`narrative_reorder: false`, `narrative_cutting: false`) provide permanent overrides. |
| **Transparency** | Narrative Cuts section explains what was removed and why. Emphasis Order section explains what was reordered and why. Degradation warnings give users actionable guidance ("Consider using `--light` or adjusting thresholds"). No silent editorial decisions. |
| **Sensible defaults** | Light mode defaults to "auto" (data-driven activation). Thresholds default to 90 seconds. Onboarding defaults to "technical" audience. PPTX defaults to Calibri/#2d5aa0. Every default is documented and overridable. |
| **Consistency** | All 9 presentation types follow the same 6-step flow structure. Deltas are type-specific content (frameworks, slide sequences, role dispatch), not structural deviations. The user's mental model of the flow remains stable across types. |
| **Feedback and status** | Enhanced progress indicators (Flow C.1) show step number, action description, contextual detail, and quantified completion. This is a significant improvement over no progress indication. |

### 3. Edge cases addressed [blocking]

**PASS** (with one observation)

| Edge Case | How Addressed |
|-----------|--------------|
| **Empty states: no artifacts for Content Gate** | Each type defines required vs enhancing artifacts. Missing required = STOP. Missing enhancing = WARN with `[TBD]` placeholders. The system never silently proceeds without required data. |
| **Error: unknown presentation type** | Flow A.6 explicitly defines the updated error message listing all 9 supported types. Clean upgrade from 4-type error to 9-type error. |
| **Error: python-pptx not installed** | Flow B.1 defines graceful fallback: clear install instructions + automatic fallback to structured-markdown. No unhandled ImportError. |
| **First-time use** | Progress indicators (C.1) orient first-time users at every step. Sensible defaults mean no config is required. Type detection from natural language keywords lowers the barrier ("investor pitch" not `--type investor-pitch`). |
| **Ambiguous type detection** | Flow A.1 states: "ambiguous? ASK, never guess." This is the correct UX pattern -- explicit disambiguation over silent misclassification. |
| **Threshold exceeded** | Three-tier response: 75% warning, 100% confirmation, Step 6 notice with actionable advice. Degradation never skips steps -- light means reduced depth, NOT skipped. This aligns with the "no skip stages" principle. |
| **Light mode + threshold interaction** | Flow C.4 provides a 2x3 interaction matrix showing combined effects. Independent controls that converge gracefully -- no conflicting behaviors. |
| **Narrative tension on short presentations** | Flow D.1 Pass 4: "Slide count < 6? Skip." Correct -- forcing a tension arc on a 4-slide deck would distort content. |
| **User-specified order vs narrative reorder** | OQ-2 resolution: user order takes precedence. Locked slides are never moved. `narrative_reorder: false` suppresses all reordering. The user's intent is always respected. |
| **Retrospective sensitivity: wrong audience** | Sensitivity filter is audience-conditional (FR-05.4/FR-05.6). Executive/client-facing = filtered. Technical/casual = full detail. Disclaimer always shown regardless. |
| **Restore cut slides** | Flow D.3: `restore {slide title}` reinserts a cut slide. Users can undo the Composer's editorial judgment. |
| **Template layout name mismatch** | Flow B.2 / FR-09.3: layout name matching first, fallback to index. Handles corporate templates with non-standard layout names. |

**Observation** (non-blocking): The PPTX generation flow (B.1) does not explicitly address the edge case where the `composed-draft.json` intermediate file is malformed or missing (e.g., if a previous step crashed mid-write). The script should validate the JSON before attempting slide generation. This is an implementation detail rather than a flow gap -- the error handling pattern is consistent with FR-07.3 (clear error message, no crash) -- but the flow document could benefit from an explicit note. Filing as a SUGGESTION, not a blocker.

### 4. All PRD requirements have corresponding flow elements [blocking]

**PASS**

Systematic traceability check across all 20 functional requirements:

| FR | PRD Requirement | Flow Coverage |
|----|----------------|--------------|
| FR-01 (Investor Pitch) | 5 ACs: keyword detection, auto-detect, content gate, narrative framework, slide sequence | Flow A.1: all 5 ACs mapped to flow steps. Traction-Opportunity-Ask framework, 9-slide default sequence, Content Gate required/enhancing split. |
| FR-02 (Roadmap) | 4 ACs: keyword detection, content gate, narrative framework, slide sequence | Flow A.2: Now-Next-Later framework, temporal structure constraint ("do NOT reorder Now/Next/Later"), Content Gate artifacts defined. |
| FR-03 (Product Demo) | 5 ACs: keyword detection, content gate, narrative framework, `[DEMO]` placeholders, GAME_DEV adaptation | Flow A.3: Hook-Show-Impact framework, `[DEMO]` placeholder formatting with duration/key points, GAME_DEV adaptation with publisher milestone vocabulary. Speaker notes auto-enabled for demo slides. |
| FR-04 (Onboarding) | 5 ACs: keyword detection, content gate, narrative framework, default audience, slide sequence | Flow A.4: Context-Landscape-Pathways framework, default "technical" audience without asking, 7-slide sequence with Resources/Links. |
| FR-05 (Retro Summary) | 6 ACs: keyword detection, content gate, narrative framework, sensitivity filter, disclaimer, no-filter for team audiences | Flow A.5: Celebrate-Learn-Commit framework, audience-conditional sensitivity filter (boxed diagram), mandatory disclaimer, explicit no-filter for technical/casual. |
| FR-06 (Error Handling) | 2 ACs: new types proceed, error lists all 9 types | Flow A.6: before/after comparison showing updated error message with all 9 types. |
| FR-07 (PPTX Script) | 3 ACs: valid .pptx, slide mapping, python-pptx missing handling | Flow B.1: script invocation with input/output paths, dependency check with fallback, user confirmation message. |
| FR-08 (Slide Layouts) | 7 ACs: title, content, metrics, comparison, CTA, timeline, architecture | Flow B.1: layout mapping table with 7 layout types mapped to PowerPoint layouts with fallback-to-index. |
| FR-09 (Template Support) | 3 ACs: template arg, defaults, layout name matching | Flow B.2: 5-level branding resolution order with template > config > flags > config values > defaults. |
| FR-10 (PPTX Format Option) | 4 ACs: format flag, config default, help listing, fallback | Flow B.1: `--format pptx` triggers post-approval PPTX branch. Fallback to structured-markdown with install instructions. |
| FR-11 (Font/Color Config) | 3 ACs: config font, config color, defaults | Flow B.2: branding resolution levels 3-5 cover font/color from flags, config, and defaults (Calibri / #2d5aa0). |
| FR-12 (Progress Indicators) | 2 ACs: step-begin output, step-complete output | Flow C.1: full example showing all 6 steps with contextual progress and quantified completion lines. |
| FR-13 (Light Mode) | 5 ACs: auto activation, single reviewer, --full override, always config, never config | Flow C.2: role count evaluation (<=3 = light), Step 3 and Step 5 effects, --full override, config options (auto/always/never). |
| FR-14 (Per-Type Thresholds) | 3 ACs: per-type map, global default, zero = unlimited | Flow C.3: 4-step threshold resolution (per-type > global override > 90s default > 0 = no threshold). |
| FR-15 (Degradation) | 3 ACs: 75% warning, 100% degradation, Step 6 notice | Flow C.3: 75% warning with text, 100% effects (single reviewer, MUST-FIX only), Step 6 notice with actionable advice. |
| FR-16 (Emphasis) | 4 ACs: impact ranking, non-chronological, user override, config toggle | Flow D.1 Pass 1: impact signals with type-specific weights, locked slide constraints, `narrative_reorder: false` disables. |
| FR-17 (Cutting) | 4 ACs: low-value detection, Narrative Cuts section, restore command, config toggle | Flow D.1 Pass 2: cutting heuristics, cut recording, `narrative_cutting: false` disables. Flow D.3: Narrative Cuts section + `restore` command. |
| FR-18 (Audience Framing) | 4 ACs: investor framing, executive framing, technical framing, rules from narrative-patterns.md | Flow D.1 Pass 3: 5 audience lenses (investor, executive, technical, client-facing, casual) with argument restructuring, always-on (no toggle). |
| FR-19 (Narrative Tension) | 4 ACs: climax positioning, Feature Pitch pattern, Sprint Review pattern, <6 slides skip | Flow D.1 Pass 4: 60-70% climax positioning, type-specific tension patterns for all 9 types, <6 slides skip rule, locked slide respect. |
| FR-20 (Review Gate Quality) | 3 ACs: TW expanded criteria, UX expanded criteria, MUST-FIX auto-fix | Flow D.2: TW and UX expanded review questions quoted verbatim from PRD. MUST-FIX/SUGGESTION classification preserved. |

**20/20 FRs covered. 0 gaps found.**

---

## Summary of Findings

| # | Type | Finding |
|---|------|---------|
| 1 | SUGGESTION | Flow B.1 (PPTX Generation): Add explicit handling for malformed/missing `composed-draft.json`. The error pattern is implied by FR-07.3 but not diagrammed in the flow. Low risk -- implementation will naturally handle this -- but documenting it improves completeness. |

---

## Verdict

The user flows are thorough, well-structured, and fully traceable to the PRD. The delta-from-baseline approach is clean -- it avoids duplication while making every change auditable. Edge cases are addressed comprehensively. The combined end-to-end journey demonstrates integration across all four feature groups. The single suggestion is non-blocking.

The light of Earendil shines upon these flows. They shall not lead the Fellowship astray.

**STATUS: DONE**
