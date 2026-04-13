# Adversarial Architecture Review: hardware-team Plugin

**Reviewer:** Challenger (Loop 1, fresh review -- no prior context)
**Architecture Version:** 1.1
**Date:** 2026-04-12
**Artifacts Reviewed:** architecture.md, ADR-001, ADR-002, ADR-003, ADR-004

---

## Findings

### F-01: kicad-happy Version Coupling Has No Runtime Contract Validation

**Class:** coupling
**Rating:** BLOCKING

**Issue:** The architecture relies on cross-plugin skill invocation to kicad-happy (ADR-002 marks this as a one-way door), yet the only version compatibility mechanism is a string in config (`dependencies.kicad_happy_version: ">=1.2.0"`) and a SessionStart hook that compares version numbers. There is no validation that the kicad-happy skill interfaces (input/output contracts) actually match what hardware-team expects. A kicad-happy update from 1.2.0 to 1.3.0 could change the output format of `kicad-happy:kicad` (e.g., different finding structure, renamed fields) without changing the major version, and every gate downstream would silently consume malformed data.

The architecture states "integration layer documents expected input/output contracts" (Risks table) but no such integration layer or contract specification exists in the architecture. Section 5.2 maps roles to skills but says nothing about expected input schemas or output schemas. The sub-agents are told to invoke kicad-happy skills and "use the loaded skill's capabilities" -- but there is no structural validation that the capabilities returned match expectations.

**Fix:** Define explicit input/output contracts for each kicad-happy skill consumed. At minimum, document the expected output structure (fields, types) in `kicad-integration.md`. Add a lightweight contract assertion in each role sub-agent: after invoking a kicad-happy skill, verify the presence of expected output fields before processing. Report `HW-KCH-004: CONTRACT_MISMATCH` if the output structure does not match expectations. This transforms silent data corruption into a detectable, actionable error.

---

### F-02: Deduplication Engine Is Underspecified and Fragile

**Class:** data-integrity
**Rating:** BLOCKING

**Issue:** Section 10.1 defines a "Deduplication Engine (orchestrator logic, not a sub-agent)" that merges findings from parallel review passes. The deduplication criteria are: "location (same component + same net), category." This is critically underspecified:

1. **No matching algorithm defined.** What constitutes "same component"? If Reviewer 1 says "C7 has insufficient derating" and Reviewer 2 says "the 100nF cap on VCC_3V3 rail is underrated," are these the same finding? The architecture provides no fuzzy matching, synonym resolution, or matching threshold.
2. **Severity reconciliation is incomplete.** "Keep highest severity" is stated, but what happens when reviewers disagree on the category? Reviewer 1: category=derating, severity=critical. Reviewer 2: category=thermal, severity=major. Same component. Are these one finding or two?
3. **This is orchestrator logic, not a sub-agent** -- meaning the LLM performs deduplication in the orchestrator's context. The orchestrator is also managing pipeline state, rework tracking, memory injection, and stage dispatch. There is no guarantee the LLM will perform consistent deduplication across runs.

This matters because the gate decision depends on deduplication results. If the deduplication produces different results on a re-run (LLM non-determinism), the gate may flip between DONE and NOT_DONE for the same set of findings.

**Fix:** Either (a) define deduplication as a deterministic algorithm with explicit matching rules (component ID exact match + category exact match = duplicate; all else = distinct), or (b) make deduplication a separate sub-agent with a structured output contract and explicit instructions for edge cases. Option (a) is strongly preferred for gate reliability since gates should be deterministic per the Business Rules Engine principle in CLAUDE.md.

---

### F-03: State File Uses Markdown with YAML Frontmatter -- Fragile for Machine Parsing

**Class:** data-integrity
**Rating:** ADVISORY

**Issue:** Section 7.1 defines `state.md` as a Markdown file with YAML frontmatter. The architecture acknowledges state corruption is possible (HW-STA-001, HW-STA-002) and provides recovery protocols. However, the choice of Markdown-with-YAML-frontmatter for machine-critical state data introduces unnecessary fragility:

1. The YAML frontmatter delimiter (`---`) must be the first line. Any accidental text before it breaks parsing.
2. The Markdown body below the frontmatter serves no machine purpose -- it is "This file tracks the state..." informational text. It adds bytes with zero value for state operations.
3. The `state_manager.py` script must handle YAML-in-Markdown parsing rather than pure YAML parsing, adding complexity.
4. If a sub-agent or user edits the state file (despite the "do not edit manually" instruction), the Markdown portion could introduce YAML-breaking content.

The delivery-flow uses this pattern, so this mirrors established convention. But state data is fundamentally different from documentation -- it is machine-managed, machine-consumed data where parse reliability matters most.

**Fix:** Use pure YAML (`.hardware/state.yml`) for machine state. If human readability is desired, add a `hw-status` command that pretty-prints the state. This eliminates the frontmatter parsing layer and reduces corruption surface. If mirroring delivery-flow's `.md` pattern is considered more important than parse reliability, at minimum document this as a known trade-off and ensure `state_manager.py` uses a robust frontmatter parser (not regex-based `---` splitting).

---

### F-04: No Hook for Pipeline Bypass Detection

**Class:** testability
**Rating:** ADVISORY

**Issue:** The delivery-team plugin has a PreToolUse hook for "Pipeline bypass detection" that warns when `developer` or `godot` skills are invoked outside an active delivery-flow pipeline. The hardware-team architecture defines NO equivalent hook.

This means a user can invoke `hardware-team:electrical-engineer` or `hardware-team:pcb-layout-engineer` directly -- bypassing the pipeline orchestrator, gates, rework tracking, state management, and memory system. The role skills would execute without the orchestrator's quality guardrails. The architecture's entire value proposition (structured 8-stage pipeline with gates and rework) is bypassed.

The hooks.json in Section 9.1 contains only SessionStart hooks and a PostToolUse notification hook. There is no PreToolUse hook to guard against direct role invocation.

**Fix:** Add a PreToolUse hook matching `Skill` that checks if the invoked skill is a hardware-team role skill (electrical-engineer, pcb-layout-engineer, manufacturing-engineer, compliance-engineer, test-engineer, hw-product-owner). If no `.hardware/config.yml` exists, warn the user: "Role skills should be invoked through the hardware-flow pipeline for gate validation and quality tracking. Run hardware-team:hardware-flow first, or say 'skip pipeline' to proceed without quality gates." Mirror the delivery-team's pipeline bypass detection pattern.

---

### F-05: Rework DAG Has Missing Path from Compliance to Layout

**Class:** docs
**Rating:** ADVISORY

**Issue:** Section 3.3 defines 6 rework paths. The ASCII diagram shows backward edges but is inconsistent with the rework path table. Specifically:

- The diagram shows `Compliance --> Schematic` as a rework path.
- The table confirms `Compliance --> Schematic` ("EMC failure requires filtering/shielding redesign").
- **Missing:** There is no `Compliance --> Layout` rework path. In real hardware development, EMC compliance failures frequently require layout changes (ground plane modifications, trace rerouting for emission reduction, shielding zone additions) that do NOT require schematic changes. Forcing all compliance rework through the Schematic stage means the Layout stage re-executes as a downstream gate re-validation, but without the specific EMC-layout context that should drive the rework.

Additionally, the ASCII diagram is hard to parse and several backward edges are ambiguously drawn. The `Pilot Run --> DFM/DFA` path is in the table but barely visible in the diagram.

**Fix:** Add a `Compliance --> Layout` rework path for EMC failures that are layout-specific (trace routing, ground plane, shielding zones) vs. schematic-specific (filtering components, shielding redesign). Update the ASCII diagram for clarity or replace it with a cleaner representation. The rework path table should be the authoritative source, not the diagram.

---

### F-06: PostToolUse Hook Uses Prompt-Type for File Extension Checking

**Class:** performance
**Rating:** ADVISORY

**Issue:** Section 9.4 defines a PostToolUse hook for KiCad file modification notification as a `"type": "prompt"` hook. This means every Write or Edit operation in the session -- regardless of file type -- triggers an LLM inference call to check if the file extension is `.kicad_sch` or `.kicad_pcb`. For a session with hundreds of file edits (common during development stages), this adds hundreds of unnecessary LLM calls for a simple string suffix check.

The delivery-team uses a command-type hook (`validate_gdscript.py`) for its PostToolUse file validation, which is a Python script that can check the file extension in microseconds and exit silently when irrelevant.

**Fix:** Replace the prompt-type hook with a command-type hook (`check_kicad_file.py`). The Python script reads `$TOOL_INPUT` from the environment, checks for `.kicad_sch` or `.kicad_pcb` in the file path, and only outputs a message if a KiCad file was modified. This eliminates LLM overhead for non-KiCad file operations. Exit 0 always (informational).

---

### F-07: Memory Relevance Decay Has No Floor and No Cleanup Mechanism

**Class:** performance
**Rating:** ADVISORY

**Issue:** Section 8.2 defines `relevance_decay: 0.95` with a range of 0.0-1.0. Section 8.5 adds relevance boosts (+0.1) and penalties (-0.05). However:

1. **No decay floor:** A relevance score of 0.95 decayed per-run will approach zero over many runs but never reach it. Memory files will accumulate entries indefinitely with near-zero relevance scores that are never pruned.
2. **No cleanup/archival mechanism:** The architecture defines memory write and read protocols but no cleanup. Over many pipeline runs, `lessons-<stage>.md` files will grow unbounded. The p95 retrieval target of <2 seconds (NFR-008) depends on "small index file" and "capped injection (top 5 per tier)" -- but index scanning time grows linearly with entry count.
3. **Relevance penalty of -0.05 after 3 consecutive non-applications** is very conservative. A lesson that is never applied across 60 consecutive runs (3 years of weekly runs) would still have a relevance score above zero and remain in the index.

**Fix:** Define a memory archival threshold (e.g., relevance < 0.1 after N runs = archived). Archived entries move to `lessons-archived.md` and are excluded from index scanning. Add a `memory_entries_limit` config key (default: 100 per stage file) that triggers archival of lowest-relevance entries when exceeded.

---

### F-08: marketplace.json Skill Paths Use Relative Prefix Inconsistently

**Class:** naming
**Rating:** ADVISORY

**Issue:** Section 4 (Level 1 context) shows the proposed marketplace.json entry with skill paths like `"./hardware-team/skills/hardware-flow"`. Examining the actual marketplace.json, existing plugins use the same `"./"` prefix pattern (e.g., `"./agentic-flow-builder/skills/flow-builder"`). However, the architecture document also refers to skill paths as `skills/hardware-flow/` (Section 2.1, Type column), `skills/hw-product-owner/` etc. -- without the `./hardware-team/` prefix.

This is cosmetic but could cause confusion during implementation. The skill directory path within the plugin (`skills/hardware-flow/`) is different from the marketplace registration path (`./hardware-team/skills/hardware-flow`). The architecture should be consistent about which context uses which path format.

**Fix:** Add a note in Section 2.1 clarifying that the "Path" column shows paths relative to the plugin root (`hardware-team/`), while marketplace.json uses paths relative to the repository root (`./hardware-team/`). Minor but prevents implementation confusion.

---

## Summary Assessment

**Overall Confidence: 3.5 / 5 (Solid foundation with specific gaps to address)**

The architecture is well-structured, thorough, and clearly benefits from the delivery-team's proven patterns. The 8-stage pipeline with human-execution stages is an honest and pragmatic design. The cross-plugin kicad-happy integration is architecturally sound. The error taxonomy and testability strategy show mature engineering thinking.

However, two issues are blocking:

1. **F-01 (kicad-happy contract validation):** The architecture's most critical external dependency has no interface contract validation. For a one-way-door decision (ADR-002), this is an unacceptable gap. Silent data corruption from interface drift would be extremely difficult to diagnose.

2. **F-02 (deduplication engine underspecification):** The gate decision mechanism -- the core quality assurance feature -- depends on an underspecified, non-deterministic deduplication step. This undermines the deterministic gate evaluation principle.

The advisory findings (F-03 through F-08) are real but individually non-critical. F-04 (pipeline bypass) and F-06 (prompt-type hook overhead) are the most impactful of the advisories and should be addressed before implementation.

| Rating | Count | IDs |
|--------|-------|-----|
| BLOCKING | 2 | F-01, F-02 |
| ADVISORY | 6 | F-03, F-04, F-05, F-06, F-07, F-08 |
