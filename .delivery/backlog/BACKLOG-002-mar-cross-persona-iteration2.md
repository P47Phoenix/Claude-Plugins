# BACKLOG-002: MAR cross-persona self-correction pilot (iteration-2 swap)

**Status**: MERGED into BACKLOG-003 (2026-04-08) — see redirect below
**Priority**: P3 (historical)
**Size**: S (historical)
**Created**: 2026-04-08
**Merged**: 2026-04-08
**Owner**: PO → Quality (pilot design + measurement)

## REDIRECT — Merged into BACKLOG-003

Per PO revision 2026-04-08 (`.delivery/artifacts/research/po-revision-research-integration.md`), this item is **merged into BACKLOG-003 (Configurable Architecture Board Review pattern)**.

**Rationale**: BACKLOG-003's "each review has its own context and perspective... configurable agentic loop" IS MAR's multi-persona debator + judge structure instantiated for architecture review. The architecture board is the higher-leverage site for the same pattern MAR proposes. Running BACKLOG-002 as a separate narrow iteration-2 swap pilot AND BACKLOG-003 as an architecture board would build two overlapping multi-persona-reflection patterns.

BACKLOG-003 now carries MAR's verdict, acceptance criteria (round-2 success ↑, zero 3-peat recurrences, token cost <25% per iteration), and the persona-swap mechanism — applied to the architecture review loop rather than to generic self-correction.

**Historical content preserved below for traceability.**

---

## Source
- **Paper**: "Multi-Agent Reflexion (MAR)", arXiv:2512.20845
- **Reviews**:
  - `.delivery/artifacts/research/architect-review-model-first-mar.md` (verdict: DEFER — 70% covered by existing Debate/Review Board/Adversarial)
  - `.delivery/artifacts/research/quality-review-model-first-mar.md` (verdict: INVESTIGATE — cross-run recurrence is real)
  - `.delivery/artifacts/research/po-synthesis-model-first-mar.md` (PO resolution: INVESTIGATE — narrow pilot only)

## Proposed Change
Do NOT add a new top-level pattern. Apply MAR's only genuinely novel idea (different persona for reflection) as a narrow refinement of the existing self-correction loop: on iteration-2 of any self-correction, route the correction attempt through a different alias/theme or through the adversarial challenger instead of the original author.

**Concrete file/skill changes (pilot scope):**
- `delivery-team/skills/delivery-flow/SKILL.md` — self-correction loop section: add "iteration-2 persona swap" rule (behind `experimental.mar_persona_swap: true`)
- `delivery-team/skills/delivery-flow/references/self-correction-guide.md` (or equivalent) — document swap policy: iteration-1 same agent (current behavior), iteration-2 different alias/challenger, iteration-3 unchanged
- No changes to Debate, Review Board, or Adversarial Review — explicitly out of scope per Architect's "70% already covered" finding

## Acceptance Criteria
1. Pilot runs on 5 pipelines that historically hit round-2 self-correction
2. Metric: round-2 success rate ↑ AND zero 3-peat recurrences in `topics/defect-patterns.md`
3. Specifically resolves the recurring "installed-vs-source sync gap" (3x) and "stale derived artifacts" (2x) classes noted in `team-review/sm-review.md`
4. Token cost increase <25% per iteration-2 (Architect's cost concern)
5. If criteria fail, close as REJECT and document that existing Debate coverage is sufficient

## Rationale
Architect is right that MAR is mostly duplicative with existing patterns — but QA's cross-run recurrence evidence (same mental model, same blind spot, across runs) is exactly what a different-persona reflection addresses. Narrow pilot respects both reviews.

## Links
- Memory: `.delivery/memory/team-review/sm-review.md`, runs c8f2 and p5v8 (recurrence pairs)
