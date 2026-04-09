# QA Review — Information Architecture (Stage 3 Design)

**Reviewer**: Legolas (QA) | **Date**: 2026-04-08
**Artifact**: `.delivery/artifacts/03-design/ux/information-architecture.md`
**PRD**: `.delivery/artifacts/02-refine/po/prd.md`

> *"That bug still only counts as one."*

## Gate Findings (QA lens — testability of the design)

1. **Author flows observable (Flows A, B, C)** — PASS. Each flow names start state, input files, output path, and success signal (DoD rule-check line). A sub-agent run is scriptable: seed PRD → invoke PO → assert `constraints.yml` at path with required field count.

2. **Error paths reachable and recoverable** — PASS. §5 specifies single-line feedback, one next action, no silent failure. Induction tests: drop `invariants` → expect exact error string; malformed YAML → expect line+column; forbidden token in artifact → expect token + path.

3. **Flow D DoD check implementable** — PASS. Five deterministic steps enumerated: YAML load → required-field assert → forbidden-vocab grep → `mandatory_artifacts` path-exists → `citations` non-empty when volatility. Implementable as a Python rule-check today. Honors the Business Rules Engine philosophy (FR-7).

4. **Reference insertion points specific** — PASS. §7 names **§0 "The Golden Rule"** before Phases 1–4 in `volatility-decomposition.md` (exact heading), and **§P-Guard** sidebar repeated at head of each Phase 1–4 in `strategic-ddd.md`. Grep `## §0` post-implementation is a valid acceptance check. No "somewhere near."

5. **Cross-doc nav friction testable** — PASS. §6 gives a linear chain; friction points (1) template-vs-guide confusion, (2) PRD-by-habit, each with concrete mitigations (template renames, orchestrator citation-order). Broken-link grep trivial against the four named files.

6. **Naming clarity ratings justified** — PASS. §3 table carries reasoning per row (`state_variables` M: engineers conflate with program variables; `invariants` H: term of art authors should learn). Two M-rated fields flagged for Architect decision — correct ownership; not arbitrary.

## Observations (non-blocking)

- §9 Open Q4 (physical field order: enforced vs. conventional) should resolve before Dev stage; Architect's call.
- Flow E (human, first 20 lines) is aspirational rather than testable. Acceptable for IA; would need a line-count rule in FR-7 to enforce.

## Verdict

All six criteria met. Testable end-to-end by sub-agent run and deterministic grep. Bow lowered.

---

STATUS: DONE
ARTIFACT: .delivery/artifacts/03-design/dod/qa-review.md
SUMMARY: Six arrows loosed, six marks struck. Flows observable, errors inducible, Flow D implementable, insertion points named by heading. The design will bear a test.
