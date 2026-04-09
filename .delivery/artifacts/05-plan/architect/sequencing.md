# Implementation Sequencing — Paired Constraints Primitive

**Stage**: 5 (Plan) | **Role**: Solution Architect (Celebrimbor) | **Task**: implementation-sequencing
**Pipeline ID**: run-2026-04-08-a1f3 | **Date**: 2026-04-08 | **Mandate**: ADR-002 (first live dogfood)

> *"Let us forge something that will endure beyond the ages. I do not redraw the blade — I name the order of its tempering."*

---

## 1. Story ↔ Architecture Mapping

| Story | Architecture artifact / decision realized | ADR(s) |
|---|---|---|
| US-1 | §3 Schema (8 fields) + §7 R-REQUIRED rule | ADR-001 |
| US-2 | §5 NEW `constraints-model-guide.md` (canon of 8 fields) | ADR-001 |
| US-3 | §5 NEW `constraints-refine.yml` template + §6 Refine invocation | ADR-001 |
| US-4 | §5 NEW `constraints-architect.yml` template (pre-pop vocab + Löwy stub) | ADR-001, ADR-003 |
| US-5 | §5 UPDATED `volatility-decomposition.md` §0 Golden Rule insertion | ADR-003 |
| US-6 | §5 UPDATED `strategic-ddd.md` Decomposition Hygiene sidebar | ADR-003 |
| US-7 | §6 `pipeline-stages.md` Stage 5 Architect invocation | **ADR-002** |
| US-8 | §7 R-GREP / R-ARTIFACTS / R-INVARIANTS-REF / R-CITATIONS | ADR-001, ADR-003 |
| US-9 | §8 Backwards compat opt-in by file presence (the dogfood IS the opt-in) | ADR-001 |

**Orphans**: none. **Gaps**: §5 `config-schema.md` v2.7→v2.8 bump and §5 `SKILL.md` kickoff-line update have **no realizing story** — PO ruled both out of scope. Architectural ruling: both are truly deferrable (stub-on-load handles v2.7; kickoff lines are cosmetic). **Not a blocker.** Log as BACKLOG candidates post-UAT.

## 2. Volatility-Driven Sequencing Check

Least volatile (forge first): **US-1 schema**, **US-5 Golden Rule §0**, **US-6 DDD sidebar** — these are write-once canon.
Medium: **US-2 guide**, **US-3/US-4 templates** — will evolve with authoring experience.
Most volatile (forge last): **US-7 pipeline-stages.md surgery**, **US-8 validator rules**, **US-9 dogfood** — iteration expected.

SM's order: S1 {US-1, US-5} → S2 {US-2, US-3} → S3 {US-4, US-7, US-6} → S4 {US-8, US-9}. **Volatility discipline is honored.** Two minor frictions: (a) US-3 (medium) lands in S2 while US-4 (medium) waits until S3 — acceptable because US-3 depends only on US-2, not US-4; (b) US-6 (least volatile) is deliberately used as S3 ballast per SM's r4x2 analysis — I endorse this; a least-volatile 1-pointer is exactly the right shock absorber for a 100%-cap sprint. **Confirm.**

## 3. Interface / Contract Definitions

- **C-1 Schema contract (US-1 ↔ all).** The JSON Schema authored in US-1 is the frozen contract. **Lock point: end of S1.** After S1 ships, US-2/3/4/7/8 treat the schema as immutable within this feature; any field-shape change reopens US-1 and cascades.
- **C-2 `pipeline-stages.md` shared file (US-3 ↔ US-7).** Both stories edit this file. Section ownership:
  - **US-3 owns**: Stage 2 Refine PO invocation block (adds `constraints.yml` as mandatory artifact).
  - **US-7 owns**: Stage 5 Plan step-insertion between current lines 430–431 (new Architect step; renumber 2–9 → 3–10).
  - **Merge order**: US-3 lands first (S2), US-7 rebases onto US-3's landed diff at S3 start. No concurrent branches. (SM I-2 control is correct.)
- **C-3 Forbidden vocabulary list (US-4 ↔ US-8).** Canonical location: **the template file `constraints-architect.yml`** is the locked list; `constraints-model-guide.md` documents it descriptively but the template is the source of truth the validator reads. **Lock point: US-4 DoD.** US-8's R-GREP rule reads the list from the authored `constraints.yml` at gate-time, not from a hardcoded list — so the list is data, not code. This matters: late additions are author-scoped, not validator-scoped.
- **C-4 Citation contract (US-4 ↔ US-8).** Structured `{work, chapter, page}` per ADR-001. US-8's R-CITATIONS rule asserts `work == "Righting Software"` exactly — US-4 template must seed that literal string.

## 4. Coordination Overhead Estimate

SM estimated per-story effort (17 pts total). I add coordination overhead that per-story estimates do not capture:

- **+1 pt** — US-3/US-7 merge rebase on `pipeline-stages.md` (cross-sprint S2→S3 coordination, SM already flagged as I-2).
- **+0.5 pt** — US-1 schema freeze ceremony at S1 end (tag the schema, broadcast lock to US-3/4/7/8 authors).
- **+0.5 pt** — US-9 dogfood fan-in validation (US-9 depends on US-1/2/3/8; a 1-pt story with a 4-story fan-in deserves a half-point of integration-check slack).

**Total coordination overhead: ~2 pts, unpriced in the 17.** Honest view: this is absorbable inside S4's 1-pt headroom (4/5 cap) plus S1's 1-pt headroom — but only if S1 and S4 finish clean. If S3 spills, coordination overhead becomes schedule pressure. SM's rollback triggers already handle this; I do not ask for a fifth sprint.

## 5. Architectural Risks the Sprint Plan Has Not Priced In

- **AR-1 — Schema escape hatch.** If US-3/US-4 template authors discover 8 fields insufficient, ADR-001 permits **optional field additions only**. Action: US-1 schema validator must accept unknown optional fields gracefully (warn, not fail) so a field addition does not require a validator rev. **Not currently in US-1 AC.** Recommend: add AC-1.4 "unknown top-level keys warn, do not fail."
- **AR-2 — Forbidden vocabulary contention.** No process defined for adding tokens post-lock. Ruling: **additions flow through the Architect at future Stage-4 runs**, authored into that run's `constraints.yml`. The feature's locked template is a *default*, not a ceiling. Document this in US-4 DoD.
- **AR-3 — Config schema v2.7→v2.8 dropped.** PO out-of-scope ruling. **Architectural answer: not a blocker.** The new primitive adds files; it does not require config keys. §8 backwards-compat (stub-on-load) handles legacy runs. Confirmed safe.
- **AR-4 — Stale installed plugin cache masking source edits.** Pipeline runs may load cached skill files rather than edited sources, hiding US-3/4/5/6/7 changes during dogfood. **Architectural recommendation: US-9 AC must include an explicit cache-refresh step** (re-install or cache-bust) before the dogfood DoD run. Currently absent from US-9 ACs. Recommend: add AC-9.4 "dogfood run executes against freshly re-loaded plugin sources."

## 6. Recommended Implementation Order

My sequence matches SM's within sprints and differs only in emphasis:

1. **S1**: US-1 (schema + validator, freeze at sprint end) → US-5 (prose ballast, parallel).
2. **S2**: US-2 (guide) → US-3 (Refine template + `pipeline-stages.md` Stage 2 edit). Intra-sprint sequential.
3. **S3**: US-4 (Architect template, locks vocab list) ∥ US-7 (Plan step-insertion, rebases on US-3) → US-6 (DDD sidebar, ballast).
4. **S4**: US-8 (validator rules read US-4's list as data) → US-9 (dogfood with cache-refresh).

**Deviation from SM**: none in ordering. One augmentation: **US-4 must land before US-7 within S3** (not parallel). Rationale: US-7's new invocation references `constraints-architect.yml` as an input; if US-4 is not yet authored, US-7's integration test has no fixture to load. SM's text is ambiguous on S3 intra-order; I make it explicit.

## 7. Approval Signal

**I endorse the 4-sprint allocation AS-IS**, with three minor adjustments requested as non-blocking amendments:
- **A-1**: Add AC-1.4 to US-1 (unknown optional fields warn, not fail) — closes AR-1.
- **A-2**: Add AC-9.4 to US-9 (cache-refresh before dogfood run) — closes AR-4.
- **A-3**: Within S3, order US-4 before US-7 explicitly — closes C-2 fixture dependency.

The volatility discipline is sound. The hard-cap placement at S3 is correct. The r4x2 lesson has been applied upstream. Coordination overhead (~2 pts) is absorbable in current headroom. No fifth sprint requested.

> *"I have set my mark upon the order. The tempering will hold."*

---

STATUS: DONE
ARTIFACT: .delivery/artifacts/05-plan/architect/sequencing.md
SUMMARY: Endorse 4-sprint plan AS-IS with three minor AC amendments (AC-1.4 schema forward-compat, AC-9.4 cache-refresh, S3 intra-order US-4→US-7). Volatility discipline honored; +2 pts unpriced coordination overhead absorbable in headroom.
