# Stories — BACKLOG-005 Paradigm-as-Skill Restructure
**Role:** Gandalf (PO)
**Stage:** 05-plan
**Source:** PRD FR-1..FR-7, constraints.yml, architecture.md, ADR-001, ADR-002
**Pipeline:** run-2026-04-10-d5e2 (FEATURE XL)
**Traced to:** roadmap.md STEP-02, STEP-03

---

## Capacity Declaration
- Sprint ceiling: **4 pts** (80%); hard cap: **5 pts** (never exceed)
- Estimate tier: **markdown/content + file-move** — ONE TIER LOWER than code per standing constraint
- Scale: XS=1, S=2, M=3 (markdown ceiling for this work type)
- Total budget: see Totals below
- Amendments from Celebrimbor sequencing pass: **merged in-line** per a1f3 lesson (no round-2 correction)
- Pre-loaded constraints: sprint ceiling, 1:1 AC-FR trace, markdown-tier estimates, propagate amendments, Architect-in-Plan sequencing per ADR-002

---

## Stories

### US-1 — Create volatility paradigm skill (XS=1)
**As** the architect **I want** a `paradigms/volatility/SKILL.md` with paradigm-specific instructions and references **so that** volatility decomposition loads in isolation without cross-paradigm context bleeding.

**AC-1.1** (->FR-1) `delivery-team/skills/architect/paradigms/volatility/SKILL.md` exists with frontmatter: `paradigm_id: volatility`, `display_name`, `shared_refs` list, `task_types: [decompose, design]`.
**AC-1.2** (->FR-1) Body contains: section-0 golden rule, Manager/Engine/Accessor/Utility hierarchy, dependency rules, volatility axis identification — extracted from monolithic SKILL.md.
**AC-1.3** (->FR-1) `paradigms/volatility/references/volatility-decomposition.md` exists (moved from `architect/references/`).
**AC-1.4** (->FR-1) `paradigms/volatility/references/domain-discovery-volatility.md` exists with volatility-specific interview questions extracted from `domain-discovery.md`.
**AC-1.5** (->FR-1, Celebrimbor amendment) Paradigm skill loads fewer than 5 reference files (constraints.yml ceiling `paradigm_skill_max_references: 5`).

**Deps:** none (independent). **Blocks:** US-3, US-5, US-6.

---

### US-2 — Create DDD paradigm skill (XS=1)
**As** the architect **I want** a `paradigms/ddd/SKILL.md` with paradigm-specific instructions and references **so that** DDD decomposition loads in isolation.

**AC-2.1** (->FR-2) `delivery-team/skills/architect/paradigms/ddd/SKILL.md` exists with frontmatter: `paradigm_id: ddd`, `display_name`, `shared_refs` list, `task_types: [decompose, design]`.
**AC-2.2** (->FR-2) Body contains: subdomain classification, bounded context discovery, context mapping patterns, aggregate boundaries — extracted from monolithic SKILL.md.
**AC-2.3** (->FR-2) `paradigms/ddd/references/strategic-ddd.md` exists (moved from `architect/references/`).
**AC-2.4** (->FR-2) `paradigms/ddd/references/domain-discovery-ddd.md` exists with DDD-specific interview questions.
**AC-2.5** (->FR-2, Celebrimbor amendment) Paradigm skill loads fewer than 5 reference files.

**Deps:** none (independent). **Blocks:** US-3, US-5, US-6.

---

### US-3 — Update architect SKILL.md with paradigm router logic (S=2)
**As** the orchestrator **I want** the architect SKILL.md to detect and route to paradigm sub-skills **so that** decomposition tasks dispatch to isolated paradigm agents.

**AC-3.1** (->FR-3) Router detects paradigm using ADR-002 priority chain: (1) explicit user intent, (2) `architecture.decomposition` config, (3) decision matrix fallback.
**AC-3.2** (->FR-3) `decomposition: volatility` routes to `paradigms/volatility/SKILL.md`; `decomposition: ddd` routes to `paradigms/ddd/SKILL.md`.
**AC-3.3** (->FR-3) `decomposition: auto` or unset triggers existing decision matrix, then routes to detected paradigm sub-skill.
**AC-3.4** (->FR-3) Non-decomposition task types (`review`, `document`, `evaluate`, `model`, `compliance-checklist`) bypass paradigm routing — existing logic unchanged.
**AC-3.5** (->FR-3) Decomposition strategy routing table updated to point at paradigm sub-skills for `volatility` and `ddd` entries.
**AC-3.6** (->FR-3, backwards compat) If `paradigms/` directory does not exist, router falls back to existing inline logic. No breakage for pre-migration state.
**AC-3.7** (->FR-3, Celebrimbor amendment) Router spawns `Agent` with paradigm SKILL.md + only the shared refs declared in that SKILL.md's `shared_refs` frontmatter. No implicit loading.
**AC-3.8** (->FR-3, ADR-001) Paradigm sub-skills are NOT registered in `plugin.json` — internal only.

**Deps:** US-1, US-2 (paradigm dirs must exist). **Blocks:** US-6.

---

### US-4 — Create design-sprint reference doc (XS=1)
**As** the delivery-flow orchestrator **I want** a `design-sprint.md` reference **so that** the PO+Architect Design Sprint sub-workflow is documented and discoverable.

**AC-4.1** (->FR-4) `delivery-team/skills/delivery-flow/references/design-sprint.md` exists.
**AC-4.2** (->FR-4) Documents flow: PO defines problem scope/constraints -> Architect detects paradigm -> paradigm skill produces decomposition -> architecture board review (if configured) -> handoff to Plan stage.
**AC-4.3** (->FR-4) Documents trigger: Design and Architect stages when project type involves decomposition.
**AC-4.4** (->FR-4) Documents integration points with existing pipeline stages.

**Deps:** none (independent). **Blocks:** US-6.

---

### US-5 — Create redirect stubs at original file paths (XS=1)
**As** an operator **I want** redirect stubs at the original reference paths **so that** installed caches referencing old paths do not break.

**AC-5.1** (->FR-5) `delivery-team/skills/architect/references/volatility-decomposition.md` replaced with redirect stub: single line pointing to `paradigms/volatility/references/volatility-decomposition.md`.
**AC-5.2** (->FR-5) `delivery-team/skills/architect/references/strategic-ddd.md` replaced with redirect stub: single line pointing to `paradigms/ddd/references/strategic-ddd.md`.
**AC-5.3** (->FR-5) Each stub contains "Load the paradigm skill directly" instruction.
**AC-5.4** (->FR-5, Celebrimbor amendment) Stubs created AFTER US-1/US-2 moves complete — redirect targets must exist first.

**Deps:** US-1, US-2 (files must be at new paths before stubs replace originals). **Blocks:** US-6.

---

### US-6 — Dogfood volatility decomposition through new paradigm skill (S=2)
**As** the team **I want** a volatility decomposition run through the new paradigm skill structure **so that** context isolation is empirically proven.

**AC-6.1** (->FR-6) Invoke architect skill with `decomposition: volatility` in config.
**AC-6.2** (->FR-6) Paradigm skill loads in isolation — only volatility references in prompt, no DDD/event-storming/game-architecture refs.
**AC-6.3** (->FR-6) Decomposition output conforms to architect output contract (artifacts land at `.delivery/artifacts/04-architect/`).
**AC-6.4** (->FR-6) Token count documented: paradigm skill prompt size vs. monolithic architect prompt size. Target: paradigm loads <5 refs vs. monolithic 27+.
**AC-6.5** (->FR-6, Celebrimbor amendment) Dogfood validates router selects volatility via ADR-002 priority chain level 2 (config).

**Deps:** US-1, US-3 (paradigm skill + router must exist). **Blocks:** US-7.

---

### US-7 — Invariant preservation verification (XS=1)
**As** the team **I want** all AS-IS invariants verified post-restructure **so that** no regression is introduced.

**AC-7.1** (->FR-7) Two-channel communication preserved — orchestrator signals separate from domain artifacts.
**AC-7.2** (->FR-7) Context isolation preserved — paradigm sub-agents receive only paradigm-scoped references.
**AC-7.3** (->FR-7) DoD validation multi-validator pattern unchanged.
**AC-7.4** (->FR-7) Orchestrator does not produce domain artifacts itself.
**AC-7.5** (->FR-7) Self-correction loops capped at 3 rounds.
**AC-7.6** (->FR-7) Retrospective mandatory at Stop — hook unchanged.
**AC-7.7** (->FR-7) Light stages reduce depth but never skip.
**AC-7.8** (->FR-7, constraints.yml) Paradigm sub-skill loads ONLY its own references — no cross-paradigm bleeding.
**AC-7.9** (->FR-7, constraints.yml) Existing pipelines without paradigm config continue to work unchanged.
**AC-7.10** (->FR-7, constraints.yml) No new config keys introduced — `architecture.decomposition` already exists.

**Deps:** US-6 (dogfood proves isolation empirically; invariant check confirms the rest). **Blocks:** none (terminal).

---

## Totals
- Stories: **7**
- Points: 1 + 1 + 2 + 1 + 1 + 2 + 1 = **9 pts**
- Sprints: **3** (see sprint-plan.md)
- All ACs 1:1 traced to FRs + constraints.yml invariants
- Subsystem change: STEP-02 = 11%, STEP-03 = 16%, both under 20% ceiling

## Amendments (merged from Celebrimbor sequencing pass — per a1f3 lesson)
1. **AC-1.5, AC-2.5 added** — paradigm_skill_max_references ceiling (5) enforced per constraints.yml.
2. **AC-3.7 added** — explicit shared_refs loading via frontmatter, no implicit loading (per architecture.md section 4).
3. **AC-3.8 added** — ADR-001 internal sub-skill rule (no plugin.json registration).
4. **AC-5.4 added** — redirect stubs depend on US-1/US-2 completing moves first.
5. **AC-6.5 added** — dogfood must validate ADR-002 priority chain routing.
6. **US-5 deps tightened** — depends on US-1+US-2 (not independent) per Celebrimbor sequencing.
