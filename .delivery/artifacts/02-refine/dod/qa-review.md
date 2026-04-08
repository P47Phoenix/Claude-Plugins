# QA DoD Review — Stage 2 PRD (Orchestration Discipline Bundle)

**Reviewer**: Legolas (QA)
**Artifact**: `.delivery/artifacts/02-refine/po/prd.md`
**Verdict**: **DONE**

---

## QA Lens: Testability of Requirements

A keen eye sees far. I have walked the length of this PRD, arrow nocked, and tested each requirement against the QA Definition of Done: is it specific, is it verifiable, is it testable.

### 1. Functional Requirements (FR-01 through FR-16)

| FR | Testable? | Verification approach the PRD already names |
|----|-----------|----------------------------------------------|
| FR-01 | Yes | Fresh config contains no `project_type`, declares `schema_version: 2.7`. File inspection. |
| FR-02 | Yes | Three concrete acceptance scenarios (a/b/c): legacy bare key, v2.7 override, both-keys-present precedence. |
| FR-03 | Yes | Two consecutive runs with different request types produce two different routing decisions. |
| FR-04 | Yes | Wizard output is a 9-question flow producing a config with no `project_type`. |
| FR-05 | Yes | `grep project_type delivery-team/skills/delivery-flow/` returns only deprecation/Phase-1 hits. |
| FR-06 | Yes | Section exists, is first prose block, referenced from three named downstream sections. |
| FR-07 | Yes | Step 4.5 contains rejection clause and links to FR-08 anti-patterns section. |
| FR-08 | Yes | All six named anti-patterns present with name + description + alternative. |
| FR-09 | Yes | Five lettered acceptance scenarios (a–e): orchestrator-write block, sub-agent allow, Bash redirection block, fallback warn, known-gaps documented. Strongest acceptance set in the PRD. |
| FR-10 | Yes | Rule block exists, visually distinct, referenced by name from three named docs. |
| FR-11 | Yes | Each of three reference docs contains the dispatch rule in specified locations. |
| FR-12 | Yes (conditional) | Hook fires on synthetic compound-role prompt; does not fire on single-role prompt. Correctly marked MAY-not-MUST. |
| FR-13 | Yes | Pattern doc contains all four protocol steps + three convergence criteria + taxonomy + no-context-leak guarantee. |
| FR-14 | Yes | Stage 4 doc references the new pattern by name and bounds loop count. |
| FR-15 | Yes | `config-schema.md` v2.7 documents `max_self_correction` with Architect loop use listed. |
| FR-16 | Yes | `grep 2.6` across the four named files returns only changelog/historical hits. |

QA finding: every functional requirement names at least one observable, verifiable acceptance condition. Sixteen arrows, sixteen marks struck.

### 2. Non-Functional Requirements (NFR-01 through NFR-08)

| NFR | Measurable? | Notes |
|-----|-------------|-------|
| NFR-01 | Yes | p95 ≤ 50ms with named measurement method (wall-clock around hook entry/exit) and a v2.6 baseline. |
| NFR-02 | Yes | Stdlib-only — verifiable by import inspection. |
| NFR-03 | Yes | Tolerant load of v2.6 fixture is a single test. |
| NFR-04 | Yes | DoD validator named; grep is the verification. |
| NFR-05 | Yes | Wrap-and-exit-0 pattern is inspectable in source. |
| NFR-06 | Yes (process) | The dogfood run itself is the test, correctly elevated to acceptance. |
| NFR-07 | Yes (process) | Plugin-dev skill load is observable in transcript. |
| NFR-08 | Yes | Single PR / single merged change set is observable in git history. |

QA finding: NFRs are constraints, not vapour. Each one names how it will be checked.

### 3. PRD-Level Acceptance Criteria (Section 10)

The five PRD-level checkboxes are reviewable and gate-ready. Section 9's traceability table maps every FR to a source issue — no orphans, no inventions.

### 4. Open Questions

OQ-1 through OQ-7 are correctly marked as non-blocking and routed to specific downstream stages. OQ-1 is marked RESOLVED in FR-09 with the layered detection strategy spelled out. OQ-7 (test fixture location) lands at QA's feet; resolution in Plan: commit a static fixture under `delivery-team/tests/fixtures/legacy-v2.6-config.yml` rather than generate inline, because the repo lacks a test runner and a checked-in fixture is grep-able and reviewable without execution.

### 5. Risks Have Mitigations

All eight risks (R1–R8) carry an explicit mitigation. R3 (loops never converge) and R6 (origin detection unreliable) are the highest-stakes for QA, and both have concrete mechanical fallbacks (two-clean / no-new-classes / hard cap; layered detection with soft-deny degradation). Satisfied.

---

## What I Looked For And Did Not Find

- Vague verbs. No "should be robust", no "improve quality", no "where appropriate". Every requirement names an artifact, a file, or a behaviour.
- Untestable success metrics. All eight goal metrics in Section 2 are countable (percent, count, latency).
- Hidden coupling. The four issues live on shared files; the PRD calls this out in Section 1 and addresses it via NFR-08 (atomic merge) and the implementation-order recommendation in Section 9.
- Missing negative cases. FR-09 acceptance includes the *allow* path (sub-agent write) alongside the *block* path. FR-12 includes the *no false positive* case (single-role prompt). Both halves of the truth are present.

## Minor Observations (Non-Blocking)

These do not affect DoD pass; surfaced as input for Design/Plan:

1. FR-09(a) test data: the acceptance scenario writes to `.delivery/artifacts/02-refine/po/prd.md` — the very path this current PRD occupies. The PRD already gates the block on `schema_version >= 2.7` plus a config flag, so the dogfood run authoring this PRD is not self-blocked. Plan stage should still pick a different artifact path for the actual hook test fixture to avoid temporal confusion in test logs.
2. NFR-01 baseline: "v2.6 baseline" needs a concrete number captured before the change lands. Plan stage should add a task: "Capture v2.6 hook p95 latency on dogfood machine and record in PR description."
3. FR-13 taxonomy: the seven issue classes (`coupling`, `security`, `data-integrity`, `naming`, `testability`, `performance`, `docs`) are named but not defined. A one-line gloss per class in `team-patterns.md` would prevent reviewer drift between loops. Architect or Plan stage call.

None of these block PRD acceptance.

---

## Verdict

Sixteen functional requirements, eight non-functional requirements, eight risks with mitigations, seven open questions correctly routed, and a traceability table that closes every loop back to a source issue. Each FR carries at least one observable acceptance condition. Each NFR names its measurement.

The PRD is testable, specific, and verifiable. It passes the QA Definition of Done.

**STATUS: DONE**
