# QA Architecture Evaluation -- Round 1

**Evaluator:** Legolas (QA Engineer)
**Target:** hardware-team plugin architecture (v1.0)
**Date:** 2026-04-12
**Pipeline:** run-2026-04-12-hw01

> "My eyes see far, and they see cracks in this forge-work that others might miss. That bug still only counts as one -- but left unaddressed, it becomes an army."

---

## Evaluation Criteria

For each architectural component:
1. **Isolation** -- Can it be tested in isolation?
2. **Failure Modes** -- Are failure modes defined?
3. **Observability** -- Can you tell if it is working?
4. **Integration Points** -- Are integration boundaries well-defined?

Rating: **PASS** or **FAIL** with actionable fix.

---

## Component Evaluations

### C1: Plugin Directory Structure (Section 1)

| Criterion | Rating | Assessment |
|-----------|--------|------------|
| Isolation | **PASS** | Each skill directory is self-contained with its own SKILL.md and references/. No shared references between roles. Mirrors proven delivery-team pattern. |
| Failure Modes | **PASS** | Missing directories handled by Claude Code harness discovery; plugin-validator catches structural errors. |
| Observability | **PASS** | `plugin-dev:plugin-validator` provides structural validation. Directory layout is inspectable via Glob. |
| Integration Points | **PASS** | marketplace.json entry defines the boundary. Skill paths are explicit. |

**Verdict: PASS.** The structure mirrors a proven template. No issues detected from this distance.

---

### C2: Pipeline Orchestrator -- 8-Stage Pipeline (Section 3.1)

| Criterion | Rating | Assessment |
|-----------|--------|------------|
| Isolation | **PASS** | Each stage is dispatched as a sub-agent. Orchestrator tracks state metadata, not stage content. Stages do not share context. |
| Failure Modes | **FAIL** | **Missing: no defined behavior when a sub-agent dispatch itself fails** (not a gate failure, but the Agent tool call failing -- timeout, context overflow, model error). The architecture defines gate failures and rework paths, but not agent dispatch failures. |
| Observability | **PASS** | State file tracks current_stage, stages_completed, gate results, timestamps. Pipeline progress is fully visible. |
| Integration Points | **PASS** | Stage-to-role mapping is explicit (Table 3.1). Gate ownership is clear. kicad-happy dispatch is documented per stage. |

**Fix for FAIL:** Define a "sub-agent dispatch failure" handling protocol: (a) retry once, (b) if retry fails, PAUSE pipeline with error details, (c) log the failure in state.md with stage number and error type, (d) offer user: Retry / Skip / Abort. This is distinct from a gate NOT_DONE -- it means the stage could not execute at all.

---

### C3: Rework Loops (Section 3.3)

| Criterion | Rating | Assessment |
|-----------|--------|------------|
| Isolation | **PASS** | Rework paths are stage-pair-specific. Each rework re-executes the target stage in a fresh sub-agent with rework context. |
| Failure Modes | **PASS** | Termination conditions are well-defined: max 3 per path, max 10 total. Escalation protocol includes user options (continue, abort, override). |
| Observability | **PASS** | Rework history in state.md records every event with: source/target stage, trigger reason, resolution, iteration count. Exemplary auditability. |
| Integration Points | **PASS** | The 6 defined rework paths are explicit with trigger examples. Downstream gate re-validation semantics are documented. |

**Verdict: PASS.** Rework is the hardest part to get right, and this architecture handles it well. The bounded DAG with per-path and total limits prevents infinite loops. The rework execution semantics (steps 1-6 in Section 3.3) are precise.

---

### C4: Human-Execution Stage Pattern (Section 3.4)

| Criterion | Rating | Assessment |
|-----------|--------|------------|
| Isolation | **PASS** | Three-phase pattern (gate-in / human-action / gate-out) cleanly separates AI preparation from human execution from AI evaluation. |
| Failure Modes | **PASS** | All three user responses defined (complete / failed / save). Rework on failure is explicit. Checkpoint invalidation semantics are clear. Artifact archival prevents data loss. |
| Observability | **FAIL** | **Missing: no timeout or staleness detection for PAUSED_AWAITING_HUMAN state.** The architecture notes the SessionStart hook detects paused state, but does not specify what it reports. If a pipeline has been paused for 30 days, what does the user see? Is there a staleness warning threshold? ADR-004 mentions "user discipline" as a risk but the mitigation ("SessionStart hook detecting paused state") lacks specificity. |
| Integration Points | **PASS** | Checkpoint state machine (PENDING -> COMPLETED or INVALIDATED) is well-defined. Artifact paths are explicit. |

**Fix for FAIL:** Specify the SessionStart hook behavior when paused state is detected: (a) calculate days since last_updated, (b) if > N days (configurable, default 7), emit staleness warning: "Pipeline paused for N days at stage X. Config may have drifted. Resume / Restart / Abandon?", (c) always show paused pipeline status at session start regardless of age. This makes the observability gap concrete and actionable.

---

### C5: Context Loading -- Three-Level Pattern (Section 4)

| Criterion | Rating | Assessment |
|-----------|--------|------------|
| Isolation | **PASS** | Each level loads independently. Roles load only their own references. Sub-agents do not inherit other roles' references. |
| Failure Modes | **FAIL** | **Missing: no defined behavior when a Level 3 reference file is missing or corrupted.** If `electrical-engineer/references/schematic-review.md` is accidentally deleted, what happens? The sub-agent reads it via the Read tool -- but the architecture does not specify: does the sub-agent report the missing file? Does it proceed without the reference? Does it fail the stage? |
| Observability | **PASS** | Context cost estimates are documented per level. The loading flow diagram (Section 4) shows exactly what loads when. |
| Integration Points | **PASS** | Marketplace.json defines Level 1. SKILL.md declares Level 2. References are explicitly listed in each SKILL.md. |

**Fix for FAIL:** Add a "reference availability check" to the sub-agent prompt template: before the sub-agent reads a reference, it checks the file exists via Glob. If missing, it reports `REFERENCE_MISSING: <path>` in its output, continues with degraded capability, and the orchestrator logs this as a warning. This parallels the kicad-happy `SKILL_UNAVAILABLE` pattern already defined in Section 5.3.

---

### C6: kicad-happy Integration (Section 5)

| Criterion | Rating | Assessment |
|-----------|--------|------------|
| Isolation | **PASS** | Cross-plugin boundary is clean. Role skills own the invocation decision. Orchestrator never calls kicad-happy directly. |
| Failure Modes | **PASS** | Graceful degradation protocol is well-defined (Section 5.3): catch error, report SKILL_UNAVAILABLE, document impact, pipeline continues. Pre-flight check via SessionStart hook provides early warning. |
| Observability | **PASS** | SessionStart hook reports N/11 skills available. Version compatibility checking is defined. |
| Integration Points | **PASS** | Role-to-skill mapping table (Section 5.2) is explicit. Reimplementation guard (Section 5.4) with IS/IS NOT examples provides clear boundaries. |

**Verdict: PASS.** The kicad-happy integration is the strongest component architecturally. Error handling, pre-flight checks, reimplementation guards, and version tracking are all defined. My Elven eyes find no fault here.

---

### C7: Config Schema (Section 6)

| Criterion | Rating | Assessment |
|-----------|--------|------------|
| Isolation | **PASS** | Config validation is a standalone script (validate_config.py). Schema rules are tabulated with types, defaults, and validation. |
| Failure Modes | **PASS** | Forward compatibility protocol (Section 6.3) is robust: missing keys use defaults, unknown keys ignored, invalid values warn and use defaults. Never fails the pipeline due to config errors. |
| Observability | **PASS** | SessionStart hook reports validation results. Schema version mismatch triggers migration guidance. |
| Integration Points | **PASS** | Config snapshot in state.md enables divergence detection on resume. Extension protocol (Section 6.4) is documented for future versions. |

**Verdict: PASS.** The "never fail on config errors" philosophy is exactly right for a user-facing plugin. Defensive defaults everywhere.

---

### C8: State Management (Section 7)

| Criterion | Rating | Assessment |
|-----------|--------|------------|
| Isolation | **PASS** | State file is self-contained with config snapshot, artifact registry, gate results, rework history, and checkpoints all in one file. |
| Failure Modes | **FAIL** | **Missing: no defined behavior for state file corruption or parse failure.** If `.hardware/state.md` has malformed YAML frontmatter (user accidentally edits it, disk error, partial write), what happens? The file says "Do not edit manually" but humans do. The resume protocol (Section 7.3) assumes the YAML parses successfully. |
| Observability | **PASS** | State is human-readable Markdown with YAML frontmatter. Every operation (create, update, pause, resume, complete, abort) is defined. |
| Integration Points | **PASS** | Artifact registry maps file paths to stage metadata. Resume protocol validates artifact existence on disk. |

**Fix for FAIL:** Add a "state file integrity check" to the resume protocol: (a) attempt YAML parse, (b) if parse fails, report "State file corrupted. Cannot resume." with options: Restart (archive corrupted file) / Manual Fix (show the parse error for the user), (c) if parse succeeds but required fields missing, report which fields and offer same options. The `state_manager.py` script should handle this.

---

### C9: Self-Learning Memory (Section 8)

| Criterion | Rating | Assessment |
|-----------|--------|------------|
| Isolation | **PASS** | Per-stage memory files. Index file for discovery. Clean separation from `.delivery/memory/`. |
| Failure Modes | **PASS** | Memory is additive and advisory -- missing memory files simply mean no lessons injected. Pipeline does not depend on memory to function. |
| Observability | **FAIL** | **Missing: no mechanism to observe whether memory injection actually influenced a stage outcome.** The architecture defines write (after run) and read (at dispatch) protocols, but there is no feedback loop. Did the injected lesson actually help? Was it relevant? Without this, memory relevance scores will drift without correction. |
| Integration Points | **PASS** | Tiering criteria (always inject, inject if relevant, available on request) are explicit. p95 retrieval target is documented. |

**Fix for FAIL:** This is a Phase 2 concern and I note it as such. For Phase 1, add a lightweight signal: each sub-agent that receives memory injection reports in its output whether any injected lesson was "APPLIED" (used in a decision) or "NOTED" (acknowledged but not applicable). The orchestrator logs this in the memory write phase to inform future relevance scoring. This is low-cost and high-signal.

---

### C10: Hooks (Section 9)

| Criterion | Rating | Assessment |
|-----------|--------|------------|
| Isolation | **PASS** | Each hook is a standalone Python script or prompt. hooks.json defines clear matchers and timeouts. |
| Failure Modes | **PASS** | All hooks exit 0 (informational, never blocking). Config validation hook handles missing, outdated, and invalid configs gracefully. |
| Observability | **PASS** | Hook output is visible to the user. kicad-happy check reports N/11 skills with specific missing list. |
| Integration Points | **PASS** | PostToolUse hook uses Write/Edit matcher for KiCad file detection. Timeout of 10 seconds is appropriate. |

**Verdict: PASS.** Hooks are appropriately scoped for Phase 1. The "informational only, never blocking" philosophy is correct -- blocking hooks in Phase 1 would be premature.

---

### C11: Iterative Review Agent Pattern (Section 10)

| Criterion | Rating | Assessment |
|-----------|--------|------------|
| Isolation | **PASS** | Each review pass runs as an independent sub-agent. No shared context between passes. Deduplication runs in orchestrator, not in a sub-agent. |
| Failure Modes | **PASS** | Convergence check prevents unbounded passes. Severity classification determines gate outcome (critical/major blocks, minor/warning passes). |
| Observability | **PASS** | Gate results include: reviewer count, total findings, deduplicated findings, per-validator results. The deduplication engine output is traceable. |
| Integration Points | **PASS** | Review categories (7) are explicit. Configuration parameters (passes, forced-find minimum, convergence threshold) are documented with sources. |

**Verdict: PASS.** The forced-find prompting technique is clever -- it combats the "LGTM" failure mode. The convergence check prevents wasted passes. The Design Review Board pattern (Section 10.5) extends this cleanly to multi-role review.

---

## Summary Scorecard

| Component | Isolation | Failure Modes | Observability | Integration | Overall |
|-----------|-----------|---------------|---------------|-------------|---------|
| C1: Plugin Structure | PASS | PASS | PASS | PASS | **PASS** |
| C2: Pipeline Orchestrator | PASS | **FAIL** | PASS | PASS | **FAIL** |
| C3: Rework Loops | PASS | PASS | PASS | PASS | **PASS** |
| C4: Human-Execution Stages | PASS | PASS | **FAIL** | PASS | **FAIL** |
| C5: Context Loading | PASS | **FAIL** | PASS | PASS | **FAIL** |
| C6: kicad-happy Integration | PASS | PASS | PASS | PASS | **PASS** |
| C7: Config Schema | PASS | PASS | PASS | PASS | **PASS** |
| C8: State Management | PASS | **FAIL** | PASS | PASS | **FAIL** |
| C9: Self-Learning Memory | PASS | PASS | **FAIL** | PASS | **FAIL** |
| C10: Hooks | PASS | PASS | PASS | PASS | **PASS** |
| C11: Iterative Review | PASS | PASS | PASS | PASS | **PASS** |

**Result: 6 PASS, 5 FAIL** (all FAILs are addressable with specific fixes documented above)

---

## ADR Review

### ADR-001: Plugin Structure (Mirror delivery-team vs Custom Layout)

| Criterion | Rating | Notes |
|-----------|--------|-------|
| Context complete | **PASS** | 5 requirements clearly stated. |
| Decision clear | **PASS** | Mirror with 4 documented deviations. |
| Trade-offs documented | **PASS** | "What becomes easier" and "What becomes harder" sections are honest. |
| Alternatives considered | **PASS** | 3 alternatives with pros, cons, and rejection rationale. |
| Reversibility noted | **FAIL** | **Missing: no statement on whether this decision is reversible.** Can the structure be changed later without breaking consumers? (Answer is yes -- marketplace.json skill paths would need updating, but it is doable. This should be stated.) |

### ADR-002: kicad-happy Integration Pattern

| Criterion | Rating | Notes |
|-----------|--------|-------|
| Context complete | **PASS** | Two primary options framed clearly. Verified working via live test. |
| Decision clear | **PASS** | Cross-plugin invocation. Error handling protocol. Reimplementation guard. |
| Trade-offs documented | **PASS** | External dependency and version coupling risks acknowledged. |
| Alternatives considered | **PASS** | 3 alternatives including thin wrappers and MCP server. |
| Reversibility noted | **FAIL** | **Missing: no statement on reversibility.** Switching from cross-plugin invocation to reference embedding would require significant rework of every role SKILL.md. This is a one-way door decision and should be flagged as such. |

### ADR-003: Pipeline Stage Count (8 Stages)

| Criterion | Rating | Notes |
|-----------|--------|-------|
| Context complete | **PASS** | Advisory challenge C3 referenced. All 8 stages described with execution mode classification. |
| Decision clear | **PASS** | Keep 8 stages with 4 supporting design elements. |
| Trade-offs documented | **PASS** | Perceived complexity, context management, and duration acknowledged. Phase 2 routing matrix as mitigation. |
| Alternatives considered | **PASS** | 4 alternatives spanning 5 to 10 stages, including variable stages. |
| Reversibility noted | **PASS** | Implicitly addressed: Phase 2 routing can reduce effective stage count without removing stages from the architecture. |

### ADR-004: Human-Execution Stage Pattern

| Criterion | Rating | Notes |
|-----------|--------|-------|
| Context complete | **PASS** | Three physical stages identified. The question is well-framed. |
| Decision clear | **PASS** | Gate-in/human-action/gate-out with 4 key design properties. |
| Trade-offs documented | **PASS** | User discipline, long pauses, and testing difficulty acknowledged. |
| Alternatives considered | **PASS** | 4 alternatives including simulated stages and timeout-based advancement. The rejection of timeout-based advancement ("silent failure is worse than a paused pipeline") demonstrates sound engineering judgment. |
| Reversibility noted | **FAIL** | **Missing: no reversibility statement.** This is a reversible decision (human-execution stages could later be converted to AI-execution if capabilities improve) and should say so. |

### ADR Summary: 3 of 4 ADRs missing reversibility statements.

**Fix:** Add a "Reversibility" subsection to each ADR stating whether the decision is a one-way door or a two-way door, and what the cost of reversal would be. This is a standard ADR best practice.

---

## Cross-Cutting Findings

### Finding X1: No End-to-End Testability Strategy

The architecture describes a test fixture (Story 4.0) with seeded defects for gate validation, but there is no documented strategy for testing the orchestrator itself end-to-end. How do you verify that:
- The full 8-stage pipeline completes without error?
- Rework paths trigger and resolve correctly?
- Human-execution stages pause and resume correctly?
- Memory injection works across runs?

**Rating: FAIL.** An architecture of this complexity needs an explicit testability section describing: (a) what can be tested automatically (gate evaluation against test fixtures), (b) what requires manual testing (human-execution flow), (c) what the test fixture covers and does not cover.

### Finding X2: No Error Taxonomy

Individual components define specific error behaviors (SKILL_UNAVAILABLE, gate NOT_DONE, rework escalation), but there is no unified error taxonomy. A QA engineer testing this system needs to know: what are ALL the error states, and what is the expected behavior for each?

**Rating: FAIL (minor).** This is addressable by adding an error taxonomy appendix to the architecture: enumerate every defined error condition across all sections, the component that detects it, and the response behavior.

---

## Overall Assessment

> "The forge-work is strong. The metal rings true in most places. But I count five cracks and two structural concerns that must be addressed before this architecture can withstand the weight of implementation. That bug still only counts as one -- but these seven findings count as seven."

The hardware-team architecture is fundamentally sound. It mirrors proven patterns from delivery-team, makes honest decisions about AI-vs-human boundaries, and demonstrates mature thinking about error handling in the kicad-happy integration and rework termination. The iterative review pattern and forced-find prompting show genuine innovation.

The failures are all in the same category: **undefined behavior for edge cases that WILL occur in production use** (sub-agent dispatch failure, reference file missing, state file corruption, paused pipeline staleness). These are not design flaws -- they are gaps in the specification that should be filled before implementation begins.

The ADRs are well-structured and thorough. The missing reversibility statements are a minor but consistent gap across 3 of 4.

**Recommendation:** Address the 5 component FAILs and 2 cross-cutting FAILs before proceeding to Plan stage. All fixes are additive (no architectural redesign required).
