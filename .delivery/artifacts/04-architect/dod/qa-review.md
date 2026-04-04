# Gate 4 QA Review -- Architect Stage

**Reviewer**: Legolas (QA Engineer)
**Artifact**: `.delivery/artifacts/04-architect/solution/architecture.md`
**Date**: 2026-04-04
**Depth**: LIGHT

---

*"A keen eye sees not only the path ahead, but every branch where an arrow might fly true -- or miss its mark."*

---

## Criterion 1: Architecture Supports Testing

**PASS**

Each component in the architecture has a verifiable validation approach:

| Component | Testability Assessment |
|-----------|----------------------|
| **generate_pptx.py** | Deterministic script with CLI interface (Section 1.3). Input: JSON file. Output: .pptx file. Dependency check at import time enables isolated testing with/without python-pptx. Layout mapping table (Section 1.5) defines exact fallback indices -- each row is a test case. Template precedence chain (Section 1.4) has 5 ordered levels, each independently verifiable. |
| **JSON Intermediate Format** | Schema defined explicitly (Section 1.2) with typed fields per slide. The Composer produces it, the script consumes it -- contract boundary is clean and testable with schema validation. ADR-01 confirms this was chosen specifically to avoid brittle regex parsing. |
| **Narrative Editorial Passes** | Four sequential passes (Section 2.1), each with defined input/output transformations. Emphasis mutates order + writes emphasis_log. Cutting removes slides + writes cuts_log. Framing rewrites body content in-place. Tension repositions climax to 60-70% point. Each pass is independently testable because each reads/writes the same in-memory slide list with observable mutations. |
| **Fallback Degradation** | Decision tree (Section 3.1) is fully deterministic with binary branching at each node. Threshold resolution (Section 3.3) has a 4-level precedence chain with a hardcoded default. The interaction matrix (Section 3.4) enumerates all 4 scenarios with expected outcomes per lever -- each row is a test case. |
| **Config Toggles** | Three toggles (Section 2.4) with defined skip behavior when disabled. Framing is always-on. Tension has a slide-count threshold (< 6). Each toggle state is a distinct test scenario. |

---

## Criterion 2: Components Are Isolatable

**PASS**

| Boundary | Isolation Mechanism |
|----------|-------------------|
| Composer to Script | JSON file contract (ADR-01). The script is a "pure consumer" -- it never interprets markdown. These two components can be tested independently: feed the script any valid JSON, verify .pptx output. |
| Editorial Passes | Sequential but each pass operates on the same in-memory list with defined mutations (Section 2.3). A pass can be tested by providing a slide list and asserting the transformed output. Pass ordering is enforced by design (ADR-02), not by coupling. |
| Degradation Logic | Independent from editorial passes (Section 3.2 confirms Step 4 never degrades). Light mode and threshold degradation are independent controls (Section 3.4) -- testable in isolation and in combination. |
| Template/Branding | Precedence chain (Section 1.4) is a pure resolution function: given inputs at each level, output is deterministic. No side effects on other components. |
| PPTX Generation | Explicitly outside the threshold window (Section 3.3) -- post-approval, isolated from the timed flow. Dependency guard at import time (Section 1.3) provides clean fallback path. |

---

## Criterion 3: Decisions Are Verifiable

**PASS**

| Decision | Verification Path |
|----------|------------------|
| ADR-01: JSON over markdown parsing | Rationale is falsifiable: "markdown parsing is brittle." Verify by comparing error rates of JSON deserialization vs regex parsing on edge cases (nested bullets, Mermaid blocks, tables). |
| ADR-02: Sequential over parallel passes | Rationale states each pass depends on prior output. Verify by running passes out of order and confirming inconsistent results (e.g., cutting a slide that tension already repositioned). Dependency chain documented in Section 2.2 with per-pass justification. |
| ADR-03: Step 4 never degrades | Rationale: single-agent, rule-based, fast. Verify by timing Step 4 relative to Steps 3 and 5 under load. The claim "degradation reduces parallelism width, never processing depth" is a testable architectural invariant. |
| Layout fallback strategy | Section 1.5 states all non-title layouts use index 1. Rationale: "corporate templates rarely have 7+ custom layouts." Verify by testing against diverse .potx templates. |
| Threshold = 90s default | Section 3.3 defines the resolution chain. Verify each precedence level overrides the next. Value 0 disables threshold -- testable boundary condition. |

All three ADRs include explicit context, decision, rationale, and consequences -- the standard ADR structure that enables future verification and reversal if assumptions change.

---

## Verdict

**DONE**

The architecture is testable at every seam. Components communicate through defined contracts (JSON schema, in-memory slide list, CLI arguments). The degradation model is a pure function of two independent inputs (light mode, threshold). All design decisions are documented with falsifiable rationale. No blocking issues found.

```
STATUS: DONE
ARTIFACT: .delivery/artifacts/04-architect/dod/qa-review.md
SUMMARY: Architecture passes all 3 criteria -- testable components, clean isolation boundaries, verifiable ADRs.
```
