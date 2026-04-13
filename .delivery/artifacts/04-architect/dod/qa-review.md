# QA Review -- Stage 4 Architecture Artifacts (Gate 4 Re-Validation)

**Reviewer**: Legolas (QA Engineer)
**Stage**: 04 -- Architect
**Scope**: architecture.md v1.4 (post-security revision), ADR-001, ADR-002, ADR-003, ADR-004
**Date**: 2026-04-12
**Pipeline**: run-2026-04-12-hw01 | **Type**: GREENFIELD
**Review Type**: Re-validation after security revisions (SEC-01 through SEC-06)

> *"My eyes are sharp, and sharper still when the forge has been reworked. I count every change, every seam resealed. Let us see if the metal holds true."*

---

## Purpose

Re-validate that the security revisions introduced in v1.4 (SEC-01 through SEC-06) do not regress any previously-passing Gate 4 criteria, and confirm that testability -- my primary concern -- is preserved or strengthened by the security additions.

---

## Gate 4 Criteria Re-Evaluation

### [PASS] Trade-offs documented for every major technical decision [blocking]

**No regression.** The v1.3 trade-off table (8 rows) is preserved. No security revision removed or weakened a trade-off entry. The security additions introduce new trade-off decisions that are documented inline:

| Security Decision | Documentation Location | Trade-off Stated |
|---|---|---|
| Path sanitization: whitelist vs. blacklist | Section 7.2 | Whitelist chosen (`^[a-zA-Z0-9._-]+$`); rationale is implicit (whitelist is more restrictive). Adequate. |
| State tampering: enforce vs. accept risk | Section 7.2.1 | Accepted risk with lightweight integrity hash. Rationale explicit: local dev tool, user is primary actor. |
| BOM data: block commit vs. recommend .gitignore | Section 14.2 | Recommendation approach chosen; user may decline for private repos. Rationale clear. |
| Memory pricing filter: strict vs. best-effort | Section 14.2 | Best-effort pattern matching with prompt instruction as primary defense. Limitation stated: may miss obfuscated pricing. |
| Trust boundary: plugin-level vs. platform-level | Section 5.1 (SEC-04) | Platform responsibility. Limitation stated: semantic attacks undetectable. |

**Previous observation (still standing)**: The summary trade-off table still does not include the deduplication algorithm decision or the state file format decision. Non-blocking; recommend adding for completeness.

### [PASS] NFRs quantified with measurable targets and validation approach [blocking]

**No regression.** All previously-documented NFR targets (p95 < 2s memory retrieval, zero pip install, finding structure, context isolation, no reimplementation, rework termination, config forward-compat) are preserved.

**Security revisions add testable invariants.** The v1.4 security controls are specified with sufficient precision to be tested:

| New Invariant | Measurable | Testable | Test Method (from Section 12.1) |
|---|---|---|---|
| Path whitelist `^[a-zA-Z0-9._-]+$` | Yes (regex match) | Yes | Input/output pairs for safe/unsafe values (fully automated) |
| `safe_join()` sandbox check | Yes (resolved path prefix check) | Yes | Path traversal test cases (fully automated) |
| `yaml.safe_load()` mandate | Yes (call signature audit) | Yes | Malicious YAML fixture (fully automated) |
| No-pricing filter in memory | Yes (pattern detection) | Yes | Pricing pattern fixtures (fully automated) |
| Hook `json.loads()` only | Yes (code audit) | Yes | Malformed JSON + shell metacharacter fixtures (fully automated) |

**Previous observation (still standing)**: No latency budgets for hooks, config validation, state parsing, or gate evaluation beyond the memory p95 target. Non-blocking.

### [PASS] Failure modes addressed for each component [blocking]

**No regression.** All 26 error codes from v1.3 are preserved.

**Security revisions add 2 new error codes to the taxonomy:**

| Code | Error Condition | Detection | Severity | Response |
|---|---|---|---|---|
| `HW-STA-005` | Path traversal detected | `safe_join()` in `state_manager.py` | Critical | Path construction blocked. User must fix config value. |
| `HW-SEC-001` | Pricing data detected in memory entry | Orchestrator (memory write phase) | Warning | Entry redacted; pipeline continues. |

Both new error codes follow the existing taxonomy conventions (component code, severity, response behavior). Both are structurally detectable (regex match for STA-005, pattern match for SEC-001). Neither introduces LLM-dependent failure classification.

**Previous observation (still standing)**: No `HW-DIS-005` for role-stage mismatch detection. Non-blocking.

### [PASS] Data flows described [blocking]

**No regression.** All data flow descriptions from v1.3 are preserved.

**Security revisions add data flow constraints:**

1. **Path construction flow** (Section 7.2): New `sanitize_path_component()` and `safe_join()` functions are interposed on every path construction point. The data flow is: config/state value --> whitelist validation --> path join --> canonicalization check --> filesystem operation. This is a tighter flow than v1.3 (which had no validation step).

2. **Memory write flow** (Section 8.3, step 5 + Section 14.2): New no-pricing filter interposed between lesson capture and persistence. The flow is: pipeline event --> lesson extraction --> pricing pattern scan --> redaction if detected --> persistence. This adds a filter step that was absent in v1.3.

3. **Hook input flow** (Section 9.6): New explicit flow: `$TOOL_INPUT` env var --> `json.loads()` --> field extraction --> validation --> use. Template provided. This formalizes what was implicit in v1.3.

All new data flow constraints are deterministic (regex/pattern matching), not LLM-dependent.

### [PASS] Security addressed [blocking]

**This criterion was the focus of the v1.4 revision.** The security review (SEC-01 through SEC-06) identified 2 blocking and 4 advisory findings. All 6 have been addressed:

| Finding | Severity | Resolution | Section | Adequate |
|---|---|---|---|---|
| SEC-01: Path traversal | BLOCKING | Whitelist + canonicalization in `state_manager.py` | 7.2 | Yes. `safe_join()` API with sandbox check. `HW-STA-005` error code. Applied to all construction points (config snapshot, archives, artifact registry). |
| SEC-02: BOM data exposure | BLOCKING | SENSITIVE/INTERNAL/PUBLIC classification, `.gitignore` recommendations, no-pricing memory filter | 14.2 | Yes. Three-tier classification. Setup wizard integration. `HW-SEC-001` error code. Best-effort limitation acknowledged. |
| SEC-03: YAML injection | Advisory | `yaml.safe_load()` mandate | 7.1, 14.1 | Yes. Coding standard table. Security invariant note. |
| SEC-04: Cross-plugin trust | Advisory | Trust assumption documented | 5.1, 14.3 | Yes. Explicit statement of what is trusted and what is not. Limitation stated. |
| SEC-05: State tampering | Advisory | Accepted risk with integrity hash | 7.2.1, 14.4 | Yes. SHA-256 advisory hash. Warning-only on mismatch. Rationale for acceptance clear. |
| SEC-06: Hook input injection | Advisory | Coding standards + template | 9.6, 14.1 | Yes. `json.loads()` only, no `shell=True`, path validation. Template provided. |

**Testability of security controls:** Section 12.1 was updated with 4 new test rows covering the security additions: path sanitization (SEC-01), memory no-pricing filter (SEC-02), YAML safe_load enforcement (SEC-03), and hook input sanitization (SEC-06). All 4 are classified as "Fully automated" with specific test fixture descriptions. This is the strongest signal that testability was not regressed.

### [PASS with observations] ADRs written [warning]

**No regression.** All 4 ADRs from v1.3 are preserved. No ADR was modified or weakened by the security revisions. The Follow-Up section (Section 15 item 5) documents the security review findings and their resolution locations.

---

## Testability-Specific Regression Check

As QA Engineer, testability is my primary Gate 4 concern. The following checks verify that the security revisions did not degrade the architecture's testability posture:

| Testability Dimension | v1.3 Status | v1.4 Status | Regression? |
|---|---|---|---|
| Gate evaluation determinism | All gates use structural checks | Unchanged. New `gate_strictness` behavior (F-13) is a lookup table, not LLM inference | No |
| Deduplication determinism | Exact-match algorithm on component+category | Unchanged | No |
| Error detection mechanisms | 26 codes, all structurally detectable | 28 codes (+HW-STA-005, +HW-SEC-001), all structurally detectable | No (improved) |
| Test fixture coverage | 4 fixture components covering gates and BOM | Unchanged, plus 4 new automated security test categories | No (improved) |
| State file testability | CRUD operations testable via `state_manager.py` | New `validate_state()` function adds corruption recovery testing. Integrity hash adds tamper detection testing. | No (improved) |
| Memory system testability | Round-trip injection testing | New pricing filter adds redaction testing. New `MEMORY_APPLIED`/`MEMORY_NOTED` observability aids round-trip verification. | No (improved) |
| Hook testability | Exit-0 guarantee, informational only | New coding standard template provides consistent structure. New security test fixtures for hook input. | No (improved) |

**Verdict**: No testability regression detected. The security revisions strictly improved testability by adding 4 new automated test categories and 2 new error codes with deterministic detection.

---

## Observations (Non-Blocking, Carried Forward from v1.3 Review)

1. **Deduplication and state format trade-offs not in summary table**: The trade-off table covers 8 decisions but omits the deduplication algorithm decision (Section 10.1.1) and state file format decision (Section 7.1). Both have inline rationale; suggest surfacing them in the summary table.

2. **No latency budgets beyond memory retrieval**: Only NFR-008 (p95 < 2s memory retrieval) has a latency target. Hook timeouts in hooks.json (5s, 10s) are operational limits, not performance budgets. Suggest adding p95 targets for config validation and state parsing.

3. **No role-stage mismatch detection**: No error code for dispatching the wrong role to a stage (e.g., CompE for Schematic). Suggest adding HW-DIS-005 in a future revision.

4. **Config snapshot `.gitignore` entry**: Section 14.2 recommends `.hardware/config-snapshot-*.yml` in `.gitignore`. This is appropriate since config snapshots may contain sensitive values (e.g., `bom_budget`), but note that losing config snapshots from version control means resume-from-snapshot depends on local file integrity only. This is consistent with the local-tool design philosophy.

---

## Summary Verdict

| Gate 4 Criterion | v1.3 Result | v1.4 Result | Change |
|---|---|---|---|
| Trade-offs documented [blocking] | PASS | PASS | No regression |
| NFRs quantified [blocking] | PASS | PASS | No regression; 5 new testable invariants added |
| Failure modes addressed [blocking] | PASS | PASS | No regression; 2 new error codes added |
| Data flows described [blocking] | PASS | PASS | No regression; 3 new flow constraints added |
| Security addressed [blocking] | PASS | PASS | Strengthened; 6 security findings resolved |
| ADRs written [warning] | PASS | PASS | No regression |

**Status: DONE**

All blocking Gate 4 criteria pass. No testability regression from security revisions. The architecture v1.4 is stronger than v1.3 in both security posture and testability.

> *"The metal rings true. Six flaws in the forge have been sealed, and the blade is sharper for it. I see no cracks -- not one. This architecture may pass."*
