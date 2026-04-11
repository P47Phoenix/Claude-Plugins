# Sprint Plan — BACKLOG-005 Paradigm-as-Skill Restructure
**Role:** Aragorn (Scrum Bag)
**Stage:** 05-plan
**Capacity:** sprint ceiling 4 pts; hard cap 5 pts; markdown tier (one tier lower)
**Pipeline:** run-2026-04-10-d5e2 (FEATURE XL)

## Constraints
- Dependency order: {US-1, US-2} parallel -> US-3 + US-5 -> US-4 parallel -> US-6 -> US-7
- Sprint ceiling 4 pts (80%); hard cap 5 pts (never exceed)
- Markdown/content + file-move estimates are one tier lower than code
- Capacity declaration present in stories.md (validated)

## Allocation (9 pts -> 3 sprints)

### Sprint P1 — Paradigm Skill Creation (4 pts, at ceiling)
- US-1 Create volatility paradigm skill (1)
- US-2 Create DDD paradigm skill (1)
- US-3 Update architect SKILL.md with router logic (2)

**Sequencing:** US-1 and US-2 execute in parallel (independent file-move + content creation). US-3 starts after both complete (router needs paradigm dirs to exist). Within-sprint dependency is safe — US-1/US-2 are XS with no unknowns.
**Goal:** Both paradigm skills exist at new paths; router logic landed in SKILL.md.
**Headroom:** 0 pts — at ceiling but all three are low-risk markdown work.

### Sprint P2 — Reference Doc + Redirect Stubs (4 pts, at ceiling)
- US-4 Create design-sprint reference doc (1)
- US-5 Create redirect stubs (1)
- US-6 Dogfood volatility decomposition (2)

**Sequencing:** US-4 independent, starts immediately. US-5 depends on US-1/US-2 (completed P1) — stubs point at new paths. US-6 depends on US-1 + US-3 (completed P1) — needs paradigm skill + router to exist. All three can execute in parallel within-sprint.
**Goal:** Design sprint documented; old paths redirected; dogfood proves context isolation empirically.
**Headroom:** 0 pts — at ceiling. US-6 is the risk item (empirical validation may surface issues). Mitigation: US-6 failures feed directly into US-7 findings rather than blocking.

### Sprint P3 — Invariant Verification (1 pt)
- US-7 Invariant preservation verification (1)

**Sequencing:** Terminal story. Requires dogfood results (US-6) and all structural changes (US-1..US-5) to be in place.
**Goal:** All 10 invariants from constraints.yml verified with grep evidence. Clean ship.
**Headroom:** 3 pts — lightest sprint. If US-6 surfaced issues in P2, headroom absorbs rework.

## Critical Path
US-1/US-2 (P1) -> US-3 (P1) -> US-6 (P2) -> US-7 (P3)

Length: 3 sprints. Not shrinkable without violating dependency order.

## Adversarial Self-Check
- **Can P1 fit 4 pts?** Yes — US-1/US-2 are file-move + content extraction (XS each, near-zero unknowns). US-3 is the only S at 2 pts. All markdown-tier. No hard-cap invoked.
- **Can US-1 and US-2 truly parallel?** Yes — they touch different paradigm directories (`volatility/` vs `ddd/`). No shared file writes. Architecture.md section 5 confirms independence.
- **US-3 depends on US-1+US-2 within same sprint — risky?** Low risk. US-1/US-2 are XS file-moves completing in minutes. US-3 starts after, not simultaneously. Sprint structure accommodates.
- **Is US-6 (dogfood) realistic at S=2?** Tight but defensible — it is an invocation + measurement, not content authoring. Config already has `architecture.decomposition`. If router works, dogfood is mechanical.
- **P3 at 1 pt is wasteful headroom.** Intentional — invariant verification is terminal and must not be rushed. Headroom absorbs any P2 issues. Alternative (merge US-7 into P2 at 5 pts hard cap) is defensible but rejected: invariant check should see stable artifacts, not in-progress ones.
- **Memory lesson a1f3 (propagate amendments):** All Celebrimbor amendments merged directly into stories.md. Sprint plan reflects updated deps (US-5 depends on US-1/US-2, not independent).
- **Memory lesson r4x2 (adversarial self-check):** This section.
- **Memory lesson c8f2 (1:1 AC-FR trace):** Every AC in stories.md traces to an FR or constraints.yml invariant. Verified.
- **Memory lesson k3r9 (pre-load constraints into agent prompts):** Capacity declaration, markdown-tier rule, and sprint ceiling are embedded in stories.md header, not just validator prompts.
