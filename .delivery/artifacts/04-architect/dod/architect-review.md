# Architect DoD Self-Review — Orchestration Discipline Bundle (LIGHT)

**Reviewer**: Celebrimbor, Master Craftsman
**Stage**: 04 — Architect (FEATURE-light)
**Date**: 2026-04-05

> *"Before the work leaves the forge, the smith must turn it once more in the light."*

---

## 1. Architecture is internally consistent — PASS

Cross-checked load-bearing claims across the four documents:

- **Activation gating** (architecture §2.5, ADR-001) agrees verbatim: deny requires `schema_version >= 2.7` AND `pipeline.enforce_self_write_block: true`; default `true` for fresh v2.7, `false` under tolerantly-parsed v2.6.
- **Allowlist** (architecture §2.3, ADR-001) lists the same five path patterns in the same order.
- **Layered detection** (architecture §2.2, ADR-001) — three layers, identical fall-through, identical NFR-05 justification for soft-deny.
- **Convergence rules** (architecture §4.1, ADR-003) — two-clean, no-new-classes, hard cap; default `max_self_correction: 3`; `cap_reached` framed as documented exit, not failure, in both places.
- **Taxonomy** (architecture §4.2, ADR-003) — same seven classes, same `misc` fallback policy.
- **Migration matrix** (architecture §3.2, ADR-002) — five rows match cell-for-cell, including the both-keys-present tiebreaker.
- **NFR budget** (architecture §6) traces back to PRD NFR-01..NFR-08; each has a named architectural position.
- **Risk treatment** (architecture §7) covers R1–R8 and each response appears in either the architecture body or an ADR.
- The §5 edit map's FR column is consistent with the FRs each ADR claims to satisfy.

A minor internal tension is acknowledged but not a defect: ADR-003 §Consequences notes that with `max_self_correction: 3` plus the two-clean rule, only one true "fixing" loop exists before cap. Architecture forwards the tuning question to Design/Plan rather than hiding it. Acceptable for LIGHT.

## 2. ADRs capture real trade-offs, not just restate the decision — PASS

Each ADR has Context, an enumerated alternatives list, and a reasoned rejection per alternative:

- **ADR-001** weighs four mechanisms (env var, hook input metadata, stack inspection, allowlist-only) plus a hard-deny variant. Each rejection cites a specific failure mode (single point of failure, harness coupling, brittleness, NFR-05 violation). Negative consequences explicitly name the "missed dispatch site silently falls to Layer 3" correctness hole and document a mitigation path rather than waving it away.
- **ADR-002** weighs silent drop, warn-and-drop, preserve-as-alias, hard error. The Option C rejection is the sharpest — it names exactly *why* preserving the alias defeats issue #69 ("re-arms the v2.6 footgun"). Negatives acknowledge user friction and parser complexity without minimizing.
- **ADR-003** weighs five strategies (one-clean, two-clean, severity threshold, no-new-classes, hard cap) and explains why each *alone* fails. The combined two-clean + class-saturation choice is justified against C4's non-monotonicity argument with a concrete invariant (Architect revision sub-agent sees only the current loop's findings). Negatives include taxonomy-evasion risk and the "only one fixing loop before cap" tension.

These are genuine trade-off records — losing options have explicit failure modes rather than dismissive one-liners.

## 3. Origin detection strategy is implementable — PASS WITH PLAN-STAGE VERIFICATION

- **Layer 1 (env var)** — fully implementable today. `os.environ.get()` is stdlib. The orchestrator-side change is "set env var before every Agent dispatch," mitigated by ADR-001's centralized-dispatch requirement.
- **Layer 2 (hook input metadata)** — partially implementable. Architecture §8 PQ-1 explicitly forwards this as an open question to Plan. The architecture does *not* assume Layer 2 works; it treats Layer 1 as deterministic primary and Layer 2 as best-effort secondary. If Layer 2 turns out to be a no-op, Layer 3's soft-deny is the safety net.
- **Layer 3 (soft-deny)** — fully implementable. `systemMessage` JSON write is an existing pattern in the hook codebase.
- **Bash redirection coverage** — implementable as a single regex over the command string. Patterns enumerated in §2.4 (`>`, `>>`, `tee`, `cat <<EOF`, `dd of=`, `cp`/`mv`).
- **Allowlist** — trivial: module-level constant + `fnmatch.fnmatch`.
- **Activation gating** — depends on v2.7 schema fields delivered by the same bundle. No circular dependency because gating defaults to `false` under v2.6, so rollout cannot deadlock on itself.
- **Performance** — NFR-01 budget (50ms p95) has 35ms headroom after the 15ms architecture allocation. All ops are O(1) dict/string + one regex pass. Believable.

The strategy is implementable as specified, with one acknowledged unknown that is correctly forwarded to Plan rather than hand-waved.

## 4. Edit map covers all files in scope — PASS

Cross-referenced architecture §5 against the PRD's 16 FRs:

- FR-01 ✓ config-schema.md
- FR-02 ✓ config-schema.md
- FR-03 ✓ SKILL.md
- FR-04 ✓ setup-wizard.md
- FR-05 ✓ SKILL.md, project-types.md
- FR-06 ✓ SKILL.md
- FR-07 ✓ SKILL.md
- FR-08 ✓ SKILL.md
- FR-09 ✓ enforce_pipeline_scope.py, hooks.json, quality-gates.md
- FR-10 ✓ SKILL.md
- FR-11 ✓ pipeline-stages.md, team-patterns.md, quality-gates.md
- FR-12 ✓ audit_agent_prompt.py (correctly marked OPTIONAL/MAY)
- FR-13 ✓ team-patterns.md
- FR-14 ✓ pipeline-stages.md
- FR-15 ✓ config-schema.md
- FR-16 ✓ CLAUDE.md, README.md, marketplace.json, docs/**

All 16 FRs land on at least one file. The §5.4 explicit non-targets (other delivery-team skills, other plugins, no DB, no MCP) match the PRD scope statement. The MkDocs `docs/**` entry correctly expands C7's grep concern across 25 pages rather than scoping to a single file.

---

## Residuals Forwarded to Plan

- **PQ-1** Layer 2 verification against current harness (only correctness-bearing unknown).
- **PQ-2** legacy v2.6 fixture location (procedural).
- **PQ-3** `routing.force_type` enum parity (one-line clarification, defaultable).

None block the Architect → Plan handoff at LIGHT depth.

---

## Verdict

All four LIGHT-mode DoD criteria are satisfied.

*"The seams hold. The hammer is laid down. Pass it onward."*

— Celebrimbor
