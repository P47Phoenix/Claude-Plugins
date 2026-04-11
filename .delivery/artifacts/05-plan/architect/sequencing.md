# Sequencing — BACKLOG-005 Paradigm-as-Skill Restructure
**Role:** Celebrimbor (Architect)
**Stage:** 05-plan
**Pipeline:** run-2026-04-10-d5e2 (FEATURE XL)

## Story <-> Architecture Mapping

| Story | Architecture Element | ADR |
|---|---|---|
| US-1 | Volatility paradigm sub-skill (internal) | ADR-001 |
| US-2 | DDD paradigm sub-skill (internal) | ADR-001 |
| US-3 | Architect SKILL.md router + detection priority chain | ADR-002 |
| US-4 | Design Sprint sub-workflow reference | -- |
| US-5 | Redirect stubs preserving cache compatibility | -- |
| US-6 | Empirical proof: context isolation + router function | ADR-002 |
| US-7 | Invariant preservation audit (10 invariants) | ADR-001, ADR-002 |

## Volatility Sequencing Check (per ADR-002)

Ordering follows stability: stable first, volatile last.

1. **Independent moves (lowest risk):** US-1 + US-2 — pure file-move + content extraction. No dependencies on each other. Touch different directories. Can execute in parallel.
2. **Router (depends on both):** US-3 — architect SKILL.md update. MUST see paradigm dirs at new paths to write correct routing. Depends on US-1 AND US-2.
3. **Independent reference + stubs:** US-4 (design-sprint, no deps) + US-5 (redirect stubs, depends on US-1/US-2 moves being complete so targets exist).
4. **Empirical (depends on router):** US-6 — dogfood requires paradigm skill + router to exist. Highest content volatility — exercise it last.
5. **Terminal audit:** US-7 — invariant check runs after everything is in place. Lowest volatility (checklist execution).

No sequencing inversion detected.

## Interface Contracts

| Producer | Consumer | Contract |
|---|---|---|
| US-1 `paradigms/volatility/SKILL.md` | US-3 router | Router reads `paradigm_id` from frontmatter |
| US-2 `paradigms/ddd/SKILL.md` | US-3 router | Router reads `paradigm_id` from frontmatter |
| US-1/US-2 (new paths) | US-5 (redirect stubs) | Stubs point to paths that MUST exist |
| US-3 (router) | US-6 (dogfood) | Router dispatches Agent with paradigm SKILL.md + shared_refs |
| US-6 (dogfood output) | US-7 (invariant check) | Dogfood proves context isolation; invariant check confirms the rest |

Key independence: US-1 and US-2 share NO files. US-4 shares NO files with any other story.

## Coordination Overhead
- Cross-story file conflicts: **0** (each story touches distinct paths)
- Handoffs: **1** (US-6 dogfood output informs US-7 invariant check)
- Overhead: negligible (~0 pts) — no co-authoring, no shared write targets
- Subsystem change: STEP-02 = 11%, STEP-03 = 16% (both under 20% ceiling)

## Amendments Proposed -> MERGED INTO stories.md AND sprint-plan.md THIS DISPATCH

1. **AC-1.5, AC-2.5** — paradigm_skill_max_references ceiling (5 refs) from constraints.yml added to US-1 and US-2 ACs.
2. **AC-3.7** — explicit `shared_refs` frontmatter loading contract added to US-3 (per architecture.md section 4, Q2 resolution).
3. **AC-3.8** — ADR-001 internal-only constraint added to US-3 (no plugin.json registration).
4. **AC-5.4** — US-5 dependency on US-1/US-2 tightened (redirect targets must exist before stubs replace originals).
5. **AC-6.5** — dogfood must validate ADR-002 priority chain routing via config level.
6. **Sprint plan US-5 deps updated** — moved from independent to US-1/US-2 dependent per amendment 4.

All amendments fused in this dispatch — no round-2 correction needed.

*"Seven stories, three sprints. Each paradigm bears only its own light. The router binds them without burdening them."* -- C.
