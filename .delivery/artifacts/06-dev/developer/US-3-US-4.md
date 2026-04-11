# Dev Log — US-3 + US-4 (Paradigm Router + Design Sprint)

*By Gimli son of Gloin, dwarven developer. Pipeline: run-2026-04-10-d5e2.*

## US-3: Architect SKILL.md Paradigm Router Logic

**File:** `delivery-team/skills/architect/SKILL.md`
**Action:** ADDITIVE — inserted `### Paradigm Router` section after Decision Matrix Inputs, before Domain Discovery.

### ACs Satisfied

- **AC-3.1** Detection priority chain: (1) explicit user intent, (2) config, (3) decision matrix. Per ADR-002.
- **AC-3.2** Routes `volatility` -> `paradigms/volatility/SKILL.md`, `ddd` -> `paradigms/ddd/SKILL.md`.
- **AC-3.3** `auto`/unset triggers matrix, then routes to detected paradigm sub-skill.
- **AC-3.4** Non-decomposition task types bypass routing — existing logic unchanged.
- **AC-3.5** Routing table updated to point at paradigm sub-skills.
- **AC-3.6** Fallback: if `paradigms/` missing, inline execution preserved.
- **AC-3.7** Agent dispatch loads paradigm SKILL.md + declared `shared_refs` only.
- **AC-3.8** Internal sub-skills — no `plugin.json` registration (ADR-001).

Existing content (roles, task tables, references, contracts, guardrails) untouched.

---

## US-4: Design Sprint Reference Doc

**File:** `delivery-team/skills/delivery-flow/references/design-sprint.md` (NEW, 83 lines)

### ACs Satisfied

- **AC-4.1** File exists at specified path.
- **AC-4.2** Flow: PO scope/constraints -> Architect paradigm detection -> paradigm skill decomposes -> board review -> DoD.
- **AC-4.3** Trigger: Stage 4 when project has decomposition work.
- **AC-4.4** Integration: standard artifact paths, architecture board, DoD validators, pipeline-stages Stage 4.

Design Sprint is optional. Regular architect invocations unchanged. No new config keys.

---

Aye — the router's forged and the sprint's documented. Two clean strikes on the anvil.
