# Adversarial Architecture Review: hardware-team Plugin (Loop 2)

**Reviewer:** Challenger (Loop 2, fresh review -- no prior context)
**Architecture Version:** 1.2 (post-loop-1 revisions)
**Date:** 2026-04-12
**Artifacts Reviewed:** architecture.md (v1.2), ADR-001, ADR-002, ADR-003, ADR-004

---

## Prior Finding Disposition

Loop-1 findings F-01 through F-08 have all been addressed in architecture v1.2. This review does not re-litigate resolved findings. All findings below are new.

---

## Findings

### F-09: Deduplication Board-Level Jaccard Similarity Threshold Is Arbitrary and Untested

**Class:** data-integrity
**Rating:** BLOCKING

**Issue:** Section 10.1.1 defines board-level finding deduplication using "description keyword overlap > 60% (word-level Jaccard similarity)." This is the only non-exact matching criterion in the otherwise deterministic deduplication algorithm. Several problems:

1. **60% is an arbitrary threshold with no justification.** The architecture does not explain why 60% was chosen over 50% or 70%. There are no test cases demonstrating that this threshold correctly separates true duplicates from distinct findings.

2. **Word-level Jaccard is sensitive to phrasing.** Two reviewers describing the same global decoupling problem will use overlapping but different vocabulary. "Insufficient bulk capacitance on the main power rail" vs. "Power rail lacks adequate decoupling capacitors" share only "power" and "rail" from content words (articles/prepositions excluded), yielding a Jaccard index well below 60%. These are the same finding but would be classified as distinct.

3. **No stopword definition.** Jaccard similarity on raw words including "the," "is," "a," "on" inflates overlap scores artificially. The architecture says "word-level" but does not specify whether stopwords are excluded, whether words are stemmed, or what tokenization rules apply.

4. **Conservative fallback weakens the gate.** The architecture says ambiguous results are treated as distinct. Combined with the phrasing sensitivity above, the practical effect is that board-level deduplication almost never merges findings. This means two reviewers who both identify the same global issue will produce two findings, both counted separately in the gate evaluation. If the finding is major, the gate report inflates the severity count, misleading the user about how many distinct problems exist.

5. **Contradicts the deterministic principle.** The rest of the deduplication algorithm is exact-match (component + category, net + category). The Jaccard step reintroduces variability -- different tokenization implementations could produce different scores for the same pair of descriptions.

**Fix:** Either (a) remove board-level deduplication entirely and always treat board-level findings as distinct (accept the over-counting trade-off for full determinism), or (b) replace Jaccard with a structured matching rule: require board-level findings to include a `board_issue_id` tag (e.g., "global-decoupling", "power-sequencing") and match on that tag exactly. Option (b) shifts deduplication responsibility to the reviewer prompts (each reviewer must classify board-level findings with a tag from a defined enum), which is more reliable than post-hoc text matching. If Jaccard is retained, define the tokenization rules explicitly (lowercase, split on whitespace and punctuation, exclude a defined stopword list, no stemming) and provide at least 3 test cases with expected outcomes.

---

### F-09b: No Rework Path from Pilot Run to Schematic

**Class:** docs
**Rating:** ADVISORY

**Issue:** Section 3.3 defines `Pilot Run --> DFM/DFA` as the only rework path from Stage 7. In real hardware production, a pilot run can reveal fundamental design issues that require schematic changes, not just DFM adjustments. Examples:

- Component thermal behavior under production soldering profiles differs from prototype hand-soldering (requires a different component rating or package -- schematic change)
- Production testing reveals a circuit behavior that was masked during prototype testing with bench supplies (requires adding a filter or protection circuit -- schematic change)
- Yield analysis reveals a component tolerance issue that requires a redesign with tighter-tolerance parts (schematic component substitution)

The current architecture forces all Pilot Run rework through DFM/DFA, which then may cascade to Layout or Schematic via DFM/DFA's own rework paths. This double-hop (Pilot Run --> DFM/DFA --> Schematic) adds an unnecessary intermediate stage re-execution when the root cause is clearly schematic-level.

**Fix:** Add `Pilot Run --> Schematic` as a rework path for cases where the pilot run reveals a fundamental circuit design issue. The trigger description: "Pilot run testing reveals circuit-level issue requiring component change or circuit modification." This avoids the double-hop through DFM/DFA. The existing `Pilot Run --> DFM/DFA` path remains for assembly/manufacturing process issues.

---

### F-10: Config Snapshot in State File Creates Unbounded State Growth

**Class:** performance
**Rating:** ADVISORY

**Issue:** Section 7.1 shows the state file includes a full `config_snapshot` -- a copy of the entire `.hardware/config.yml` content embedded in `state.md`. The resume protocol (Section 7.3) diffs this snapshot against the current config to detect drift.

This design has two problems:

1. **Snapshot is a full copy, not a hash.** Every time the pipeline starts, the entire config is duplicated into the state file. As the config schema grows in future versions (Phase 2 adds more fields), the state file grows proportionally. A diff against the current config could use a hash comparison for change detection and only store the full config if needed for replay.

2. **No snapshot versioning on rework.** When a rework event occurs, the state file records the rework event but does not re-snapshot the config. If the user modifies config between a rework trigger and the rework target stage execution (e.g., changes `target_fab` while the pipeline is active), the rework stage executes with the updated config but the snapshot still reflects the original config. On a future resume, the diff would show "config changed" even though the change was intentional mid-run.

**Fix:** (a) Replace the full config snapshot with a config hash (SHA-256 of the YAML content) for change detection. Store the full config only once, at pipeline creation, not in the state file but as a separate file (`.hardware/config-snapshot-<pipeline_id>.yml`). (b) Document that config changes during an active pipeline run are unsupported -- the pipeline always uses the config as snapshotted at start. If the user changes config mid-run, they must restart the pipeline.

---

### F-11: Convergence Check in Schematic Review May Terminate Prematurely

**Class:** testability
**Rating:** ADVISORY

**Issue:** Section 10.1 defines the convergence check as: "If pass N produces < 2 unique new findings not found in passes 1..(N-1), additional passes are unlikely to add value. Stop reviewing." With the default of 2 review passes, this convergence check never activates (it only applies to pass 3+).

However, if `review.schematic_review_passes` is set to 3 or higher, the convergence check creates a problem: a reviewer that focuses on different categories than previous reviewers will inherently produce "new" findings, delaying convergence. Conversely, a reviewer that happens to focus on the same categories will produce mostly duplicate findings, triggering early convergence and potentially missing categories that no reviewer has examined.

The convergence threshold (< 2 new unique findings) combined with forced-find (must find at least 2 candidates) creates a contradiction: if a reviewer is forced to find 2 issues and the convergence threshold is < 2 new unique findings, then a reviewer that finds exactly 2 issues that happen to overlap with previous findings will trigger convergence. But a reviewer that finds 2 genuinely new issues will NOT trigger convergence. The convergence check is effectively testing "did the reviewer find something new?" rather than "have we covered all review categories?"

**Fix:** Replace the convergence check with a coverage check: track which of the 7 review categories have been examined across all passes. Convergence is met when all 7 categories have been covered by at least one reviewer OR the configured number of passes is reached, whichever comes first. This ensures systematic coverage rather than relying on the coincidence of finding overlap.

---

### F-12: kicad-happy Output Contract Specifies Structure but Not Versioning

**Class:** coupling
**Rating:** ADVISORY

**Issue:** Section 5.5 defines explicit output contracts for each consumed kicad-happy skill (field names, types, consuming roles). This was a well-executed resolution of the loop-1 F-01 finding. However, the contracts are defined at a point in time and have no versioning mechanism:

1. **No contract version identifier.** The contracts in `kicad-integration.md` have no version number. When kicad-happy updates and changes its output structure (even in a backward-compatible way, such as adding a new field), there is no way to know which contract version hardware-team was written against.

2. **Contract evolution path is undefined.** If kicad-happy adds a new field to its output (e.g., `kicad-happy:kicad` adds a `recommendations[]` field to schematic analysis), hardware-team's contract assertion will pass (it checks for expected fields, not unexpected ones), but the consuming role will not know about or use the new field. This is acceptable for additive changes. But if kicad-happy renames a field or changes a type, the contract assertion catches it -- and then what? The error taxonomy says "Gate evaluates on available data." But the fix requires updating hardware-team's contracts to match kicad-happy's new interface. Who initiates this update?

3. **No contract negotiation.** kicad-happy has no awareness that hardware-team depends on specific output structures. There is no mechanism for kicad-happy to declare "these output fields are stable/public" vs. "these are internal and may change."

**Fix:** Add a `contract_version` field to each contract entry in `kicad-integration.md` (e.g., `contract_version: "1.0"`, `kicad_happy_target_version: "1.2.x"`). When the HW-KCH-004 error fires, include the contract version and installed kicad-happy version in the error message to help diagnose the mismatch. Document the update procedure: when kicad-happy releases a new version, run the test fixture to detect contract mismatches, then update `kicad-integration.md` contracts and increment the contract version. This is documentation-level, not code-level, but it closes the maintenance loop.

---

### F-13: Gate Strictness Enum Has No Behavioral Specification

**Class:** docs
**Rating:** ADVISORY

**Issue:** Section 6.1 defines `gate_strictness` as an enum with values `strict | standard | relaxed`. Section 6.2 validates it. But the architecture never defines what these values mean behaviorally. No section describes how gate evaluation changes between strict, standard, and relaxed modes.

Plausible interpretations:
- **strict**: minor findings also block the gate (not just critical/major)
- **standard**: only critical and major findings block (as described in Section 10.1)
- **relaxed**: only critical findings block; major findings are warnings

But this is speculation. The architecture mentions `gate_strictness` in the config schema but never references it in the gate evaluation logic (Section 10.1), the gate framework reference file list (Section 1.1), or the error taxonomy.

**Fix:** Define the behavioral impact of each strictness level in the gate evaluation section (10.1) or in the `gate-framework.md` reference file description. At minimum:

| Strictness | Critical Finding | Major Finding | Minor Finding |
|---|---|---|---|
| strict | BLOCKS | BLOCKS | BLOCKS |
| standard | BLOCKS | BLOCKS | PASS (logged) |
| relaxed | BLOCKS | PASS (logged) | PASS (logged) |

If gate strictness is deferred to Phase 2, remove it from the Phase 1 config schema to avoid shipping an inert config key.

---

### F-14: Test Engineer Role Has No Direct kicad-happy Skill Consumption

**Class:** testability
**Rating:** ADVISORY

**Issue:** Section 5.2 shows the Test Engineer role consumes zero kicad-happy skills directly ("(none directly) -- Uses gate outputs from other roles"). The Test Engineer is the primary role for Stage 4 (Prototype) and a support role for Stage 7 (Pilot Run). Both are human-execution stages.

The Test Engineer's responsibilities include generating test procedures, fixture design, and validation planning. In practice, test procedure generation for hardware requires understanding the board design: which test points are accessible, what signals to measure, what voltage levels to expect. This information is in the KiCad project files. Without `kicad-happy:kicad` access, the Test Engineer must rely entirely on artifacts produced by other roles (schematic review, layout review) rather than analyzing the design directly.

This creates an indirect coupling: the Test Engineer's test procedure quality depends on the completeness of the EE's and PCB Layout Engineer's artifact output. If those artifacts omit details needed for test planning (e.g., test point locations, debug connector pinouts), the Test Engineer has no way to discover them independently.

**Fix:** Add `kicad-happy:kicad` as an optional (not required) consumption for the Test Engineer role, used specifically to read test point locations, connector pinouts, and debug interfaces from the PCB design. This allows the Test Engineer to cross-reference design data directly rather than relying entirely on upstream artifacts. Mark this as optional -- if kicad-happy:kicad is unavailable, the Test Engineer falls back to artifact-based planning (current behavior).

---

## Summary Assessment

**Overall Confidence: 4 / 5 (Production-viable with targeted improvements)**

Architecture v1.2 has addressed all loop-1 findings substantively. The kicad-happy output contracts (F-01 resolution) and deterministic deduplication algorithm (F-02 resolution) are well-executed. The pipeline bypass hook (F-04), command-type PostToolUse hook (F-06), and memory archival (F-07) close real gaps identified in loop 1.

The one blocking finding in this loop (F-09) targets a residual weakness in the deduplication algorithm: the board-level Jaccard similarity step reintroduces the non-determinism that the rest of the algorithm was designed to eliminate. This is a localized fix -- either remove board-level deduplication or replace it with structured tag matching.

The advisory findings identify real but non-critical gaps: a missing rework path (F-09b), config snapshot growth (F-10), premature convergence risk (F-11), contract versioning gap (F-12), undefined gate strictness behavior (F-13), and Test Engineer capability limitation (F-14). None of these would prevent a successful Phase 1 implementation, but addressing them before implementation avoids rework later.

The architecture is materially stronger than v1.1. The error taxonomy, testability strategy, and staleness detection are particularly well-designed. The overall pattern of mirroring delivery-team conventions while adapting for hardware-specific needs is sound.

| Rating | Count | IDs |
|--------|-------|-----|
| BLOCKING | 1 | F-09 |
| ADVISORY | 6 | F-09b, F-10, F-11, F-12, F-13, F-14 |
