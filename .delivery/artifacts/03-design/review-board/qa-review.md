# QA Testability Review: Hardware Delivery Team Plugin Design Artifacts

**Reviewer**: QA Engineer (Legolas)
**Date**: 2026-04-12
**Review Type**: Design-stage testability review (Multi-Perspective Review Board)
**Scope**: User flows, wireframes, component specs, accessibility review

---

> *"My eyes miss nothing from this perch. Every state undefined is an orc uncounted, every edge case ignored a shadow in the wood. That bug still only counts as one."*

---

## Artifact 1: User Flows (`ux/user-flows.md`)

### Rating: APPROVE

**Testability strengths:**

1. **States are clearly defined.** Every flow identifies explicit entry points (E1, E2, E3), a numbered happy path, alternative paths (2a-2d), and error paths (E1, E2). Each state transition has a defined trigger and output. I can write test cases directly from these flow definitions.

2. **Success/failure conditions are measurable.** Gate results are binary: PASS or NOT_DONE. Rework limits are numeric: current/limit. Config validation outputs specify which fields failed and why. There is no ambiguity about what constitutes success at any decision point.

3. **Edge cases are addressed.** The flows explicitly cover: kicad-happy not installed (2a), partially installed (2b), version mismatch (2c), config already exists (2d), invalid config fields (E1), outdated config schema (E2). The rework flow covers both per-path and total limit exhaustion. The resume flow covers stale state detection.

4. **Rework paths are enumerable.** Flow 4 defines a fixed table of 6 valid rework paths (Source Stage --> Target Stage). This is directly testable -- I can verify that only these paths are triggered and that undefined paths (e.g., Concept --> Production Release) are rejected.

5. **kicad-happy degradation is graceful, not fatal.** Flow 5C defines that a missing skill produces a WARNING and continues, with the gate potentially flagging the gap. This is testable: remove a skill, verify warning output, verify pipeline continues, verify gate behavior.

**Testability observations (non-blocking):**

- **COMMENT**: Flow 2 (Pipeline Execution) shows the happy path through all 8 stages but does not define what happens if the user types an unrecognized command at a human checkpoint (e.g., neither "prototype complete" nor "prototype failed" nor "save pipeline state"). The expected behavior for invalid input at checkpoints should be specified -- likely an error message prompting the user to use a recognized command. Without this, testers must guess the expected behavior.

- **COMMENT**: Flow 3C (Gate Failure Self-Correction Loop) states the loop is "bounded by session context" but does not define a numeric limit. This means the self-correction loop has no explicit exit condition other than gate pass or session end. For testability, a maximum self-correction attempt count (or a clear statement that the session context window is the only bound) would let me write a deterministic test for loop termination.

- **COMMENT**: Flow 6B (P2 Dynamic Pipeline Adaptation) is marked as "Future -- not in Phase 1." This is fine, but the boundary between P1 and P2 behavior should be tested: verify that in P1, all 8 stages always execute regardless of config values like `layers: 1` or `volume: prototype`. A test case asserting "pipeline does NOT skip stages in P1" prevents premature P2 behavior from leaking in.

---

## Artifact 2: CLI Wireframes (`ux/wireframes.md`)

### Rating: APPROVE

**Testability strengths:**

1. **Design tokens create a verifiable vocabulary.** The token table (box drawing characters, severity icons, status markers, width constraints) defines exact characters and their Unicode code points. I can write assertions that verify output contains exactly these tokens and no others (e.g., no Unicode box-drawing characters leak in).

2. **Width constraint is testable.** All output targets 60 characters wide, content wraps at 56. Every wireframe can be validated against this constraint programmatically. No line should exceed 60 characters.

3. **Theme token mapping is a lookup table.** The neutral-to-LOTR mapping is a finite, enumerable substitution table (14 entries). I can test that every neutral token has a themed counterpart and vice versa, and that switching themes produces the expected substitutions without data loss.

4. **Every wireframe references source flows and FR/Story coverage.** This traceability means I can verify that every flow decision point has a corresponding wireframe, and every wireframe traces back to a requirement.

5. **Dual-theme examples provided.** Every wireframe shows both neutral and LOTR theme variants. This gives me two concrete expected outputs per component for snapshot/golden-file testing.

**Testability observations (non-blocking):**

- **COMMENT**: Wireframe 1E (Config Already Exists) shows `Config already exists (schema v1.0). Overwrite? [y/N] _` as a bare line without box borders. This is the only wireframe without a box. The inconsistency is likely intentional (simple confirmation prompt), but a test should verify that this specific prompt is unboxed while all other outputs are boxed. The design should state explicitly whether this is intentional.

- **COMMENT**: The LOTR theme stage name mapping (Concept=Shire, Schematic=Rivendell, etc.) appears in Wireframe 2A but is not in the Design Token table. It is in the component specs' theme token map but only for token keys like `PIPELINE_TITLE`, not for individual stage names. The stage-to-themed-name mapping should be enumerated somewhere testable so that theme regression tests can verify all 8 stage names.

---

## Artifact 3: Component Specifications (`ui/component-specs.md`)

### Rating: APPROVE with COMMENT

**Testability strengths:**

1. **Every component has explicit states.** Each component defines a States table with State/Behavior pairs. For example, Component 3 (Gate Result) has 5 states: all pass, partial failure, all fail, DRB with dedup, pipeline complete. Each state has defined behavior. I can write a test for every state.

2. **Placeholder definitions are typed.** Every placeholder specifies Required (Yes/No), Type (string, integer, theme-token, severity-token, boolean, status-token, whitespace), and Description. This typing makes validation testable -- I can verify that integer placeholders receive integers, theme-tokens resolve to known values, etc.

3. **Theme injection points are numbered.** Each component lists exactly which placeholders are theme-sensitive. This means I can test that non-injection-point content remains unchanged across themes, and injection-point content changes correctly.

4. **Templates are structural contracts.** The templates for each variant define the exact line-by-line structure of the output. These can be converted directly into format-validation tests.

**Testability concerns (non-blocking):**

- **COMMENT**: Component 2 (Agent Status) defines `[!]` as the Error state prefix, but this indicator does not appear in the Design Token table (which lists `[>]`, `[~]`, `[+]` only). The `[!]` token is mentioned in the States table ("Error: Shows `[!]` prefix") but has no formal definition as a Progress Indicator Token. It should be added to the token table or explicitly documented as an extension. Without this, a tester cannot verify whether `[!]` is a valid progress indicator or an undefined symbol.

- **COMMENT**: Component 3, Variant D (Design Review Board Results) template ends with a Summary line but has no explicit `Result: PASS/NOT_DONE` line. The DRB output in the wireframes (5F) also lacks a Result line -- it shows findings and a summary tally but no gate result. The question is: does the DRB produce its own gate result, or does the unified severity ranking feed into a separate gate component? This ambiguity affects test design. If the DRB has no Result line, then the test expectation is "DRB output has no Result line; the subsequent gate component determines pass/fail." If it should have one, it is missing from the template.

- **COMMENT**: The Theme Injection Architecture section should define what happens when a themed token value exceeds `WIDTH_INNER` (56 chars). The LOTR tokens are generally shorter than 56 chars, but `THE FELLOWSHIP OF THE BOARD` is 28 characters, and combined with a project name like `sensor-board-v2` in the Pre-Flight Summary line `{{PIPELINE_TITLE}}: {{project_name}}`, the result is 48 characters -- within limits. However, a longer project name (e.g., 30+ chars) combined with a themed token could overflow. The truncation/wrapping behavior for this case should be specified for testability.

---

## Artifact 4: Accessibility Review (`ui/accessibility.md`)

### Rating: APPROVE

**Testability strengths:**

1. **Every finding has a severity rating.** The three-level system (BLOCKING, WARNING, SUGGESTION) with clear definitions makes it straightforward to verify that all BLOCKING issues are resolved before implementation and all WARNING issues are tracked.

2. **The Summary Matrix is a testable checklist.** 26 findings with finding number, severity, category, and fix-required status. This directly converts to a verification checklist: for each finding marked "Fix Required," verify the fix is implemented.

3. **Fixes are specific and implementable.** Each fix includes concrete before/after examples (e.g., plain-text mode, summary-first pattern, short-form commands). These examples are themselves test cases -- I can verify that the implementation matches the prescribed fix.

4. **No BLOCKING findings exist.** All 6 actionable findings are WARNING level. This means the design does not exclude any user group -- it has friction points but no barriers. The design can proceed to implementation with WARNINGs tracked as backlog items.

**Testability observations (non-blocking):**

- **COMMENT**: Finding 1B recommends a `display.plain_text_mode` config key, and Finding 2B recommends a `display.color_mode` config key. These are new config keys not present in the current schema (v1.0) defined in the user flows. These additions should be coordinated with the config schema -- either added to v1.0 before implementation or planned for v1.1. For testability, the config schema must include these keys so tests can toggle modes and verify behavior.

- **COMMENT**: The accessibility review references wireframe numbers (e.g., "Wireframe 5B", "Wireframe 5G", "Wireframe 7A") which I verified exist in the wireframes document. Good traceability. No phantom references detected.

---

## Cross-Artifact Testability Assessment

### Positive Patterns

1. **Consistent state vocabulary.** All four artifacts use the same status tokens (DONE, NOT_DONE, PASS, PAUSED, REWORK, COMPLETE, ABORTED). No artifact introduces conflicting terminology. This means test assertions can use a single vocabulary.

2. **Full traceability chain.** User flows reference FRs and Stories. Wireframes reference flows. Component specs reference wireframes. Accessibility review references wireframes and component specs. Every artifact traces backward to requirements and forward to implementation. Test cases can trace any failure back to a specific requirement.

3. **Dual-theme coverage.** Every visual artifact shows both neutral and LOTR theme variants. Theme testing is not an afterthought -- it is built into the design from the start.

4. **Enumerable gate behavior.** Gates are binary (PASS/NOT_DONE), validators are ALL-must-pass, rework paths are a fixed set, limits are numeric. All gate behavior is deterministic and testable without runtime judgment calls.

### Gaps for Test Planning

| Gap | Impact | Recommendation |
|-----|--------|----------------|
| Unrecognized command at checkpoint | Cannot test error handling for typos | Define expected response for invalid checkpoint input |
| Self-correction loop bound | Cannot test loop termination deterministically | Add explicit max self-correction attempts or document the implicit bound |
| `[!]` error indicator undefined in tokens | Ambiguous test expectation for error states | Add to Design Token table |
| DRB Result line ambiguity | Cannot determine whether DRB output includes a gate result | Clarify in Component 3 Variant D template |
| Config key additions from accessibility | Schema drift risk | Coordinate `display.*` keys with config schema before implementation |

---

## Final Verdict

> *"I have looked upon these designs from every vantage point. The states are clear, the transitions are defined, the edge cases are addressed with the care of a Mirkwood archer counting arrows before battle. The gaps I have found are observations, not blockers. That bug still only counts as one."*

| Artifact | Rating | Blocking Issues |
|----------|--------|-----------------|
| User Flows | APPROVE | 0 |
| Wireframes | APPROVE | 0 |
| Component Specs | APPROVE | 0 |
| Accessibility Review | APPROVE | 0 |

**Overall: APPROVE** -- All four design artifacts demonstrate strong testability. States are well-defined, success/failure conditions are measurable, and edge cases are thoughtfully addressed. The non-blocking comments above should be resolved during or before the Architect stage to prevent ambiguity during test case design.
