# QA Review: ADRs + Architecture Sketch — Legolas Gate Validation

**Status**: DONE  
**Date**: 2026-05-03  
**Reviewer**: Legolas (QA perspective — Stage 4 Architect DoD)

---

## Validation Summary

All 7 gate criteria **PASS**. ADRs are traceably complete, architecturally sound, and binding decisions are honored. That bug still only counts as one.

---

## Detailed Findings

### 1. FR/NFR Traceability ✓
- **ADR-tk0e-001**: FR-01, FR-02, FR-03, FR-04, FR-11, NFR-01, NFR-02 — all cited, all in PRD §4–5
- **ADR-tk0e-002**: FR-06, FR-07, FR-08, FR-09, FR-10, FR-12, NFR-03, NFR-04 — all cited, all in PRD
- **ADR-tk0e-003**: FR-06, FR-08, NFR-04 — all cited, all in PRD

### 2. Status Field ✓
All three ADRs: `Status: Accepted (Architect DoD — 2026-05-03)` — binary, not vague.

### 3. Alternatives Considered ✓
| ADR | Alternatives | Verdict |
|-----|--------------|---------|
| 001 | (a) disk-read vs (b) two-row defer | Substantive; rejection reasoning solid (late emission violates FR-11 early-write binding) |
| 002 | Hard-fail permissive / external YAML parser / deny-all / matrix matrix | 4 substantive alts; rationale clear (false-positive load, no deps, regression risk, complexity) |
| 003 | Classify user-feedback as C / godot as B / defer frontmatter to W1 | 3 substantive alts; rejection sound (multiplexer vs leaf, small overage, CI gate unlocked by frontmatter) |

### 4. Consequences Explicit ✓
- **ADR-001**: Positive (simple, auditable, early, stateless); Negative (token counts always 0 in Wave 0, disk read overhead ~1–3 ms)
- **ADR-002**: Positive (zero deps, allowlist survives refactor, warn-only avoids false positives); Negative (hard-coded known-debt list requires code change to update)
- **ADR-003**: Positive (13 files classified, Wave 1 has prioritized list, 2 files compliant); Negative (11 known-debt entries large but honest baseline)

### 5. Binding Decisions Honored ✓
- **Ruling 1 (cache-prefix freeze)**: ADR-001 line 99 — "prefix_hash is meaningful even before model responds; captures SKILL.md prefix stability" ✓
- **Ruling 3 (tier 500/300/200)**: ADR-003 line 49 — `TIER_LIMITS = {"A": 500, "B": 300, "C": 200}` ✓; PRD NFR-04 confirms exactly these values
- **gate-patterns lesson 4 (emit early)**: ADR-001 line 96 — "Single-row model is simple, auditable, and early (satisfies gate-patterns lesson 4)" ✓
- **gate-patterns lesson (allowlist-over-deny)**: ADR-002 line 36 — "paths-filter ensures job only runs when relevant files change... allowlist approach" ✓

### 6. Cross-ADR Conflict Check ✓
- ADR-001: ~2 ms disk read overhead vs ADR-002: allowlist paths-filter → no conflict; hook runs only on Skill PreToolUse (separate concern)
- ADR-002: Known-debt pre-registry (11 files) vs ADR-003: tier mapping (13 files, 11 over-budget) → consistent; all 11 are pre-registered
- ADR-003: Tier values (500/300/200) vs ADR-002: hardcoded TIER_LIMITS → exact match ✓

### 7. Architecture Sketch Completeness ✓
| Path | Mermaid | Interaction Notes | Completeness |
|------|---------|------------------|--------------|
| Hook → JSONL | Lines 31–36 (A→B→C→D flow) | Lines 60–70 (early write, failure isolation) | ✓ Covers PreToolUse event, disk read, row append, error handling |
| PR → CI gate | Lines 38–45 (F→G→H/I→J/K/L flow) | Lines 71–79 (paths-filter, exempt zones, hard-coded known-debt) | ✓ Covers workflow trigger, tier fallback, failures, known-debt bypass, permissive-warn |
| Shared surface | Subgraph 47–49 labeled "Shared Surface" | Lines 81–85 (tier: field in frontmatter) | ✓ Identifies SKILL.md tier field as binding surface; both W0-1 + W0-2 depend on it |

### Risk Carriage ✓
Architecture sketch §10 explicitly names 4 open risks (phantom references, false positives, AC-10 vs 11 files, zero token counts in Wave 0) with mitigations and status. Honest forward-pass.

---

## AC Coverage Against PRD

All runnable ACs (AC-1 through AC-12, PRD §8) are architecturally addressable via the ADRs:
- AC-1, AC-2: ADR-001 schema + hook implementation ✓
- AC-3: ADR-001 `telemetry-schema.md` v1 binding ✓
- AC-8, AC-9, AC-10, AC-11, AC-12: ADR-002 + ADR-003 script + frontmatter binding ✓

---

## Sign-off

**QA Verdict**: Architecture completes the design. All FRs have architectural coverage. No AMTs (ambiguous, missing, or trailing) requirements. Binding decisions are locked and traced. That bug still only counts as one.

