# Developer Review: hardware-team Architecture v1.3

**Reviewer:** Gimli (Developer Role)
**Date:** 2026-04-12
**Artifact:** `.delivery/artifacts/04-architect/solution/architecture.md` v1.3
**Focus:** Implementability -- can I build this? And my code!

---

## Gate 4 Criteria Evaluation

### [PASS] Trade-offs documented

The Trade-Off Analysis table in the architecture (Section after C4 diagrams) covers 8 key decisions, each with two options, the chosen option, and rationale with ADR cross-references. Every trade-off I care about as a builder is there: plugin structure, integration pattern, stage count, human stage pattern, namespace, rework model, model tier enforcement, and memory isolation.

No ambiguity. I know what was chosen and why. And my code can follow these decisions without guessing.

### [PASS] NFRs quantified

Quality Attributes table quantifies the following:

- **Modularity**: Each role loads only its own references (context isolation)
- **Portability**: Python standard library only, no pip install (NFR-001)
- **Reimplementation guard**: NFR-003 with explicit IS/IS NOT examples in Section 5.4
- **Usability**: NFR-005 -- gate messages include what/where/why/how-to-fix
- **Memory retrieval**: NFR-008 -- p95 < 2 seconds, achieved via index scan + per-stage partitioning + capped injection (top 5)
- **Rework termination**: 3 per path, 10 total (configurable)
- **Review passes**: 2 default, configurable 1-5
- **Staleness thresholds**: 7 days warning, 30 days critical (configurable)

These are concrete enough to test against. I can write validation logic for each.

### [PASS] Failure modes addressed

Section 13 (Error Taxonomy) is thorough -- 26 error codes across 10 components. Every error has a code, detecting component, severity, and response behavior. Specific callouts:

- **Dispatch failures** (Section 3.1.1): retry-once protocol, PAUSED_DISPATCH_ERROR state, 4 error type classifications
- **State file corruption** (Section 7.3): YAML parse failure and missing required fields both handled with Restart/Manual Fix options
- **kicad-happy unavailability** (Section 5.3): SKILL_UNAVAILABLE signal with graceful degradation
- **kicad-happy contract mismatch** (Section 5.5): HW-KCH-004 with runtime assertion, contract versioning, and update procedure
- **Reference file missing/corrupted** (Section 4.1): REFERENCE_MISSING/CORRUPTED signals with continued execution
- **Rework limit exceeded** (Section 3.3): per-path and total limits with escalation message format
- **Config staleness** (Section 3.4.1): warning and critical thresholds with three user options
- **Memory file issues** (Section 8): missing/unparseable memory files degrade gracefully

The severity definitions (Critical/Major/Warning/Info) with pipeline impact and user action are clear. I know exactly what behavior to implement for each error.

### [PASS] Data flows described

The data flows are well-documented:

1. **Pipeline flow**: 8-stage sequence with clear stage-to-role-to-gate mapping (Section 3.1 table)
2. **Skill invocation flow**: Orchestrator --> Agent tool --> Role sub-agent --> Skill tool --> kicad-happy (Section 2.3 with diagram)
3. **Context loading flow**: Level 1 (marketplace.json) --> Level 2 (SKILL.md) --> Level 3 (references on demand) with explicit example in Section 4
4. **Rework data flow**: Source stage gate failure --> rework path table --> target stage re-execution --> downstream gate re-validation (Section 3.3)
5. **Human stage flow**: Gate-in (AI prep) --> Human-action (pause) --> Gate-out (AI evaluate) (Section 3.4)
6. **State data flow**: Create --> Update --> Pause/Resume --> Complete/Abort with explicit operations table (Section 7.2)
7. **Memory data flow**: Write after pipeline completion --> Index + per-stage files --> Read at pipeline start and stage dispatch --> Inject top memories into sub-agent prompt (Section 8.3)
8. **Config data flow**: config.yml --> SHA-256 hash at start --> snapshot file --> hash comparison on resume (Section 7.1/7.3)
9. **Review data flow**: Independent reviewer passes --> deterministic deduplication (component+category matching) --> coverage check --> gate evaluation with strictness levels (Section 10.1)

The C4 Context and Container diagrams (Section 11) provide visual confirmation of component relationships.

---

## Implementability Assessment

### Things I can build right now without asking questions

1. **Plugin directory structure** (Section 1.1) -- fully specified down to every file
2. **hooks.json** (Section 9.1) -- exact JSON provided, copy-paste ready
3. **Config schema** (Section 6.1) -- full YAML schema with validation rules table
4. **State file format** (Section 7.1) -- complete YAML frontmatter schema with example
5. **Error taxonomy** (Section 13) -- every error code with detection and response
6. **Deduplication algorithm** (Section 10.1.1) -- deterministic matching rules with merge behavior
7. **Hook scripts** (Sections 9.2-9.5) -- logic spelled out step by step
8. **Memory entry format** (Section 8.2) -- YAML structure with all fields defined
9. **Artifact directory structure** (Section 7.4) -- every artifact file path listed

### Minor observations (non-blocking)

1. **`state_manager.py` parser requirement**: Section 7.1 specifies "robust frontmatter parser" and explicitly calls out NOT to use regex-based splitting. Clear enough -- I will use Python `yaml` with `---` delimiter detection. The trade-off is acknowledged (F-03). Solid.

2. **Board Issue ID enum extensibility**: The `board_issue_id` enum (Section 10.1.1) has 8 values with "other-<descriptor>" as fallback. The fallback means "other-" prefixed IDs are never deduplicated, which is the correct conservative behavior. I can implement this as a prefix match.

3. **Memory `relevance_decay` floor**: Section 8.6 specifies `max(score * relevance_decay, 0.05)` and archival at < 0.1. Math checks out -- with default decay of 0.95, a lesson starting at relevance 1.0 reaches 0.1 after ~44 runs (0.95^44 = 0.103), then archives. With floor 0.05, it takes ~58 runs without the floor vs guaranteed archival with the floor. Good design.

4. **Implementation sequence** (Follow-Up item 6): Epic 1 --> 2 --> 3 --> 4 --> 5 gives me a clear build order. I know what to build first.

---

## Verdict

This architecture is built like a dwarven stronghold -- deep foundations, clear corridors, every room labeled, every door accounted for. I can take this document and start forging code immediately. No ambiguities block implementation. The error taxonomy alone is worth its weight in mithril.

And my code!
